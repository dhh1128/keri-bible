#!/usr/bin/env python3
"""detect.py — phase 1 of the bible refresh. Deterministic, no model.

Reads refresh/sources.yaml, works out what has moved since each source's pin, and writes a
delta report to refresh/state/<YYYY-MM>/. Everything downstream (triage, mining, synthesis)
reads that report rather than re-deriving it, so the expensive phases never run on a month
where nothing happened.

Exit codes are the gate:
    0   material delta — there is something to mine; the refresh should proceed
    10  quiet — nothing material moved; no PR, no tokens spent
    2   error — a source could not be read at all

Two failure modes this is written against, both learned the hard way:

  * A DEAD CONFIG LOOKS EXACTLY LIKE A QUIET MONTH. keri-review-panel's freshness.sh spent six
    weeks pointing at pre-reorg paths, and a missing root was skipped silently, so the check
    reported nothing wrong while checking nothing at all. Here, a source that cannot be read is
    an ERROR that makes the run material — a human sees it. Never a silent skip.

  * A SUBPROCESS THAT FAILS CAN STILL PRINT SOMETHING. `gh api` writes its 404 body to stdout,
    so "non-empty output" is not "it worked". Every subprocess here is checked on exit status.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "refresh" / "state"
QUARTER_MONTHS = {1, 4, 7, 10}


# --------------------------------------------------------------------------- shell helpers

class SourceError(Exception):
    """A source could not be read. Loud by construction — never swallowed into an empty result."""


def run(cmd, cwd=None, check=True):
    """Run a command and return stdout. Raises SourceError on failure, with stderr attached."""
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SourceError(f"{' '.join(cmd)} (exit {p.returncode}): {p.stderr.strip()[:400]}")
    return p.stdout


def git(args, cwd, check=True):
    return run(["git", "-C", str(cwd)] + args, check=check)


def short(sha):
    return (sha or "")[:9]


# --------------------------------------------------------------------------- git sources

def resolve_path(src, code_root: Path) -> Path:
    path = code_root / src["path"]
    if not (path / ".git").exists():
        raise SourceError(f"not a git checkout: {path}")
    return path


def fetch(path: Path, remote: str):
    out = run(["git", "-C", str(path), "remote"], check=True).split()
    if remote not in out:
        raise SourceError(f"remote '{remote}' not configured in {path} (have: {', '.join(out)})")
    # Explicit wildcard refspec rather than a bare `git fetch <remote>`, for two reasons. A repo can
    # have a NARROWED refspec configured — keria's upstream was pinned to refs/heads/development,
    # a branch that no longer exists, so a bare fetch died on a branch we do not even track. And
    # untracked-branch detection needs every remote head present locally; that is how a v1.1 doing
    # all the work while main sits still becomes visible at all.
    run(["nice", "-n", "19", "ionice", "-c", "3", "git", "-C", str(path), "fetch", "--quiet",
         remote, f"+refs/heads/*:refs/remotes/{remote}/*"])


def branch_commits(path: Path, remote: str, branch: str, since_commit: str, watch: list[str]):
    """Commits on <remote>/<branch> after since_commit that touch the watched paths."""
    ref = f"{remote}/{branch}"
    if subprocess.run(["git", "-C", str(path), "rev-parse", "--verify", "--quiet", ref],
                      capture_output=True).returncode != 0:
        # A branch can be local-only — a worktree checkout with no remote counterpart. Fall back
        # rather than erroring, but only to an exact local branch of the same name.
        if subprocess.run(["git", "-C", str(path), "rev-parse", "--verify", "--quiet", branch],
                          capture_output=True).returncode != 0:
            raise SourceError(f"neither {ref} nor local branch {branch} exists in {path}")
        ref = branch
    head = git(["rev-parse", ref], path).strip()

    if not since_commit or since_commit == "unknown":
        return head, None, [], False   # unknown pin: a full re-anchor, not a delta

    probe = subprocess.run(["git", "-C", str(path), "merge-base", "--is-ancestor",
                            since_commit, ref], capture_output=True, text=True)
    if probe.returncode == 128:
        raise SourceError(f"pinned commit {since_commit} is not in {path} — history rewritten "
                          f"or the pin is wrong. Refusing to guess.")
    diverged = probe.returncode != 0   # pin not an ancestor: branch was rebased or retargeted

    sep = "\x1e"
    fmt = f"%h{sep}%an{sep}%ad{sep}%s"
    log = git(["log", f"{since_commit}..{ref}", f"--format={fmt}", "--date=short",
               "--no-merges", "--"] + watch, path)
    commits = []
    # NOT splitlines(): Python treats \x1e (record separator) as a line boundary, which shreds
    # each record into its four fields and then fails to unpack them. Split on newline only.
    for line in log.split("\n"):
        if not line.strip():
            continue
        sha, author, date, subject = line.split(sep, 3)
        commits.append({"sha": sha, "author": author, "date": date, "subject": subject})

    stat = git(["diff", "--stat", f"{since_commit}..{ref}", "--"] + watch, path).strip()
    return head, (stat.splitlines()[-1] if stat else ""), commits, diverged





def untracked_branches(path: Path, remote: str, tracked: set[str], newest_tracked_date: str):
    """Upstream branches more recent than anything we track. This is how v1.1 would have surfaced."""
    out = git(["for-each-ref", "--sort=-committerdate",
               "--format=%(committerdate:short)\t%(refname:short)", f"refs/remotes/{remote}"], path)
    found = []
    for line in out.splitlines():
        date, ref = line.split("\t", 1)
        name = ref.split("/", 1)[1] if "/" in ref else ref
        if name in tracked or name in ("HEAD", "gh-pages") or ref == remote:
            continue
        if date > newest_tracked_date:
            found.append({"branch": name, "date": date})
    return found[:6]


def cross_branch_diff(path: Path, remote: str, standardizing: str, forward: str, watch: list[str]):
    """Diff of the standardizing line against the forward line, over watched paths only.

    Comparing this run's diff with the previous run's is what detects a TIER UPGRADE: text that
    left the diff has (almost always) landed in the standardizing branch. The word 'almost' is
    why the report says 'verify' rather than asserting it — the hunk could equally have been
    dropped from the forward branch, and only reading it tells you which.
    """
    return git(["diff", f"{remote}/{standardizing}...{remote}/{forward}", "--"] + watch, path,
               check=False)


def hunk_headers(diff_text: str) -> set[str]:
    """Identify hunks by file + the @@ context line, which survives line-number churn better
    than the body does."""
    out, current = set(), None
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            current = line[4:].strip()
        elif line.startswith("@@") and current:
            ctx = line.split("@@")[-1].strip()
            if ctx:
                out.add(f"{current} :: {ctx}")
    return out


# --------------------------------------------------------------------------- github sources

def gh_json(args):
    out = run(["gh"] + args)
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        raise SourceError(f"gh returned non-JSON for {' '.join(args)}: {out[:200]}") from e


DISCUSSION_QUERY = """
query($owner:String!, $name:String!, $cursor:String) {
  repository(owner:$owner, name:$name) {
    discussions(first:25, orderBy:{field:UPDATED_AT, direction:DESC}, after:$cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { number title url updatedAt createdAt lastEditedAt
              author { login } category { name } comments { totalCount } }
    }
  }
}"""


def discussions_since(repo: str, since: str):
    owner, name = repo.split("/")
    cursor, hits, stop = None, [], False
    while not stop:
        data = gh_json(["api", "graphql", "-f", f"query={DISCUSSION_QUERY}",
                        "-F", f"owner={owner}", "-F", f"name={name}"] +
                       (["-F", f"cursor={cursor}"] if cursor else []))
        page = data["data"]["repository"]["discussions"]
        for n in page["nodes"]:
            if n["updatedAt"][:10] < since:
                stop = True
                break
            hits.append({"number": n["number"], "title": n["title"], "url": n["url"],
                         "updated": n["updatedAt"][:10], "created": n["createdAt"][:10],
                         "edited": (n["lastEditedAt"] or "")[:10],
                         "author": (n["author"] or {}).get("login", "?"),
                         "category": n["category"]["name"], "comments": n["comments"]["totalCount"]})
        if stop or not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return hits


def merged_prs_since(repo: str, since: str):
    rows = gh_json(["search", "prs", "--repo", repo, "--merged", "--merged-at", f">={since}",
                    "--limit", "100", "--json", "number,title,url,author,closedAt"])
    return [{"number": r["number"], "title": r["title"], "url": r["url"],
             "author": (r.get("author") or {}).get("login", "?"),
             "merged": (r.get("closedAt") or "")[:10]} for r in rows]


def gh_repo_commits(repo: str, branch: str, since_date: str, watch: list[str]):
    hits = []
    for p in (watch or [""]):
        q = f"repos/{repo}/commits?sha={branch}&since={since_date}T00:00:00Z"
        if p:
            q += f"&path={p}"
        for c in gh_json(["api", q]):
            hits.append({"sha": c["sha"][:9], "date": c["commit"]["author"]["date"][:10],
                         "author": c["commit"]["author"]["name"],
                         "subject": c["commit"]["message"].splitlines()[0], "path": p})
    return hits


def page_hash(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "keri-bible-refresh/1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", "replace")
    # Strip scripts/styles and collapse whitespace so a cache-buster or a rotating nonce does not
    # read as a content change.
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"(?s)<[^>]+>", " ", body)
    return hashlib.sha256(re.sub(r"\s+", " ", body).strip().encode()).hexdigest()[:16]


# --------------------------------------------------------------------------- freshness

def freshness(repo: Path):
    script = repo / "refresh" / "freshness.py"
    if not script.exists():
        return {"status": "missing", "detail": f"{script} not found"}
    p = subprocess.run(["python3", str(script)], capture_output=True, text=True, cwd=str(repo))
    m = re.search(r"freshness: (\d+) live / (\d+) missing of (\d+)", p.stdout)
    if not m:
        return {"status": "error", "detail": (p.stderr or p.stdout).strip()[-400:]}
    live, missing, total = (int(x) for x in m.groups())
    n = re.search(r"new misses: (\d+)", p.stdout)
    new = int(n.group(1)) if n else None
    # The NEW misses are the signal. The standing backlog is a known quantity recorded in
    # refresh/freshness-baseline.json, and re-reporting it every month teaches everyone to ignore
    # the whole section.
    fresh = [l.strip("! ").strip() for l in p.stdout.splitlines() if l.strip().startswith("! [")]
    return {"status": "ok", "live": live, "missing": missing, "total": total,
            "new": new, "new_misses": fresh}


# --------------------------------------------------------------------------- run

def previous_state_dir(current: Path):
    dirs = sorted(d for d in STATE.glob("*") if d.is_dir() and d.name != current.name)
    return dirs[-1] if dirs else None


def selected_tiers(args, now):
    if args.tiers:
        return set(args.tiers.split(","))
    tiers = {"hot", "warm"}
    if now.month in QUARTER_MONTHS:
        tiers.add("cold")
    return tiers


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true", help="skip git fetch (offline / testing)")
    ap.add_argument("--tiers", help="comma list, e.g. hot,warm,cold (default hot,warm + cold quarterly)")
    ap.add_argument("--run", help="state directory name (default YYYY-MM)")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    manifest = yaml.safe_load((REPO / "refresh" / "sources.yaml").read_text())
    code_root = Path(os.path.expanduser(os.environ.get("CODE_ROOT", manifest["code_root"])))
    tiers = selected_tiers(args, now)

    run_dir = STATE / (args.run or now.strftime("%Y-%m"))
    (run_dir / "crossdiff").mkdir(parents=True, exist_ok=True)
    prev = previous_state_dir(run_dir)

    report = {"generated": now.isoformat(timespec="seconds"), "tiers": sorted(tiers),
              "previous_run": prev.name if prev else None, "sources": [], "errors": []}

    for src in manifest["sources"]:
        if src.get("tier", "hot") not in tiers:
            continue
        entry = {"id": src["id"], "kind": src["kind"], "tier": src.get("tier"),
                 "feeds": src.get("feeds", []), "chapters": src.get("chapters", []),
                 "caveat": src.get("caveat", ""), "branches": [], "items": [],
                 "new_branches": [], "tier_upgrades": [], "material": False}
        try:
            if src["kind"] == "git":
                path = resolve_path(src, code_root)
                if not args.no_fetch:
                    fetch(path, src["remote"])
                newest_pin_date = "0000-00-00"
                for b in src["branches"]:
                    pin = (b.get("last_scanned") or {}).get("commit", "unknown")
                    head, stat, commits, diverged = branch_commits(
                        path, src["remote"], b["name"], pin, src.get("watch", ["."]))
                    newest_pin_date = max(newest_pin_date,
                                          str((b.get("last_scanned") or {}).get("date", "0000-00-00")))
                    entry["branches"].append({
                        "name": b["name"], "role": b.get("role"), "marker": b.get("marker"),
                        "from": pin, "to": short(head), "stat": stat,
                        "diverged_from_pin": bool(diverged),
                        "full_reanchor": pin == "unknown",
                        "commits": commits})
                    if commits or pin == "unknown" or diverged:
                        entry["material"] = True

                tracked = {b["name"] for b in src["branches"]}
                entry["new_branches"] = untracked_branches(path, src["remote"], tracked,
                                                           newest_pin_date)
                if entry["new_branches"]:
                    entry["material"] = True

                std = next((b["name"] for b in src["branches"] if b.get("role") == "standardizing"), None)
                fwd = next((b["name"] for b in src["branches"] if b.get("role") == "forward"), None)
                if std and fwd:
                    diff = cross_branch_diff(path, src["remote"], std, fwd, src.get("watch", ["."]))
                    dst = run_dir / "crossdiff" / f"{src['id']}.diff"
                    dst.write_text(diff)
                    old = prev / "crossdiff" / f"{src['id']}.diff" if prev else None
                    if old and old.exists():
                        gone = hunk_headers(old.read_text()) - hunk_headers(diff)
                        if gone:
                            entry["tier_upgrades"] = sorted(gone)[:25]
                            entry["material"] = True
                    entry["crossdiff_size"] = len(diff.splitlines())

            elif src["kind"] == "gh-discussions":
                hits = discussions_since(src["repo"], str(src["since"]))
                primary = set(src.get("primary_authors", []))
                for h in hits:
                    h["primary"] = h["author"] in primary
                entry["items"] = hits
                entry["material"] = bool(hits)

            elif src["kind"] == "gh-prs":
                hits = merged_prs_since(src["repo"], str(src["since"]))
                entry["items"] = hits
                entry["material"] = bool(hits)

            elif src["kind"] == "gh-repo":
                b = src["branches"][0]
                since = str((b.get("last_scanned") or {}).get("date") or "2026-01-01")
                hits = gh_repo_commits(src["repo"], b["name"], since, src.get("watch", []))
                entry["items"] = hits
                entry["material"] = bool(hits)

            elif src["kind"] == "web":
                prev_hashes = {}
                if prev and (prev / "webhashes.json").exists():
                    prev_hashes = json.loads((prev / "webhashes.json").read_text()).get(src["id"], {})
                cur = {}
                for url in src["urls"]:
                    cur[url] = page_hash(url)
                    if prev_hashes.get(url) and prev_hashes[url] != cur[url]:
                        entry["items"].append({"url": url, "was": prev_hashes[url], "now": cur[url]})
                        entry["material"] = True
                    elif not prev_hashes.get(url):
                        entry["items"].append({"url": url, "was": None, "now": cur[url]})
                entry["hashes"] = cur

            else:
                raise SourceError(f"unknown kind '{src['kind']}'")

        except SourceError as e:
            entry["error"] = str(e)
            entry["material"] = True          # an unreadable source is a finding, not a skip
            report["errors"].append({"id": src["id"], "error": str(e)})
        except Exception as e:                # noqa: BLE001 — same rule, wider net
            entry["error"] = f"{type(e).__name__}: {e}"
            entry["material"] = True
            report["errors"].append({"id": src["id"], "error": entry["error"]})

        report["sources"].append(entry)

    # persist web hashes for the next run's comparison
    webhashes = {s["id"]: s["hashes"] for s in report["sources"] if "hashes" in s}
    if webhashes:
        (run_dir / "webhashes.json").write_text(json.dumps(webhashes, indent=2))

    report["freshness"] = freshness(REPO)
    if report["freshness"].get("status") in ("error", "missing"):
        report["errors"].append({"id": "freshness", "error": report["freshness"].get("detail", "")})
    report["material"] = (any(s["material"] for s in report["sources"])
                          or bool(report["freshness"].get("new"))
                          or bool(report["errors"]))

    (run_dir / "delta.json").write_text(json.dumps(report, indent=2))
    (run_dir / "delta.md").write_text(render(report))
    print(f"wrote {run_dir / 'delta.md'}")
    print(f"material={report['material']} errors={len(report['errors'])}")

    if report["errors"] and not any(s["material"] for s in report["sources"] if "error" not in s):
        return 2 if all("error" in s for s in report["sources"]) else 0
    return 0 if report["material"] else 10


def render(r) -> str:
    L = [f"# Refresh delta — {r['generated'][:10]}", "",
         f"Tiers scanned: {', '.join(r['tiers'])}. Previous run: {r['previous_run'] or 'none'}.", ""]

    if r["errors"]:
        L += ["## Errors — read these first", "",
              "A source that cannot be read is reported, never skipped. A quiet month and a dead "
              "config look identical from the outside, and only one of them is good news.", ""]
        L += [f"- **{e['id']}** — {e['error']}" for e in r["errors"]] + [""]

    ups = [(s, s["tier_upgrades"]) for s in r["sources"] if s.get("tier_upgrades")]
    if ups:
        L += ["## Tier movement — forward text that left the standardizing diff", "",
              "Each hunk below was in the `main`↔`v1.1` diff last run and is not now. Usually that "
              "means it landed in the standardizing branch and the claim resting on it moves "
              "`[N1.1]` → `[N]`. It can also mean the hunk was dropped from the forward branch, "
              "which moves the claim the other way. Read it before marking it.", ""]
        for s, hunks in ups:
            L.append(f"### {s['id']} → chapters {', '.join(s['chapters'])}")
            L += [f"- `{h}`" for h in hunks] + [""]

    L += ["## Sources", ""]
    for s in r["sources"]:
        flag = "MOVED" if s["material"] else "quiet"
        if s.get("error"):
            flag = "ERROR"
        L.append(f"### {s['id']} — {flag}")
        if s.get("error"):
            L += ["", f"> {s['error']}", ""]
            continue
        if s["feeds"]:
            L.append(f"Feeds `{'`, `'.join(s['feeds'])}` → chapters {', '.join(s['chapters'])}.")
        if s.get("caveat"):
            L.append(f"Caveat: {s['caveat'].strip()}")
        L.append("")
        for b in s.get("branches", []):
            head = f"**{b['name']}** ({b['role']}, {b['marker']}) `{b['from']}` → `{b['to']}`"
            if b.get("full_reanchor"):
                head += " — **no pin of record; treat as a full re-anchor, not a delta**"
            if b.get("diverged_from_pin"):
                head += " — **pin is not an ancestor of the head; branch rebased or retargeted**"
            L.append(head)
            if b.get("stat"):
                L.append(f"  - {b['stat']}")
            for c in b["commits"][:20]:
                L.append(f"  - `{c['sha']}` {c['date']} {c['author']}: {c['subject']}")
            if len(b["commits"]) > 20:
                L.append(f"  - …and {len(b['commits']) - 20} more")
            L.append("")
        for nb in s.get("new_branches", []):
            L.append(f"- **Untracked branch** `{nb['branch']}` ({nb['date']}) is newer than "
                     f"anything tracked here. Propose adding it in the PR body; do not retarget "
                     f"automatically.")
        for it in s.get("items", [])[:40]:
            if "number" in it:
                star = " ⭐primary" if it.get("primary") else ""
                when = it.get("updated") or it.get("merged")
                edited = f", edited {it['edited']}" if it.get("edited") else ""
                L.append(f"- [#{it['number']}]({it['url']}) {it['title']} — {it['author']}, "
                         f"{when}{edited}{star}")
            elif "sha" in it:
                L.append(f"- `{it['sha']}` {it['date']} {it['author']}: {it['subject']}")
            elif "url" in it:
                L.append(f"- {it['url']} content hash {it['was']} → {it['now']}")
        L.append("")

    f = r["freshness"]
    L += ["## Quote freshness", ""]
    if f.get("status") == "ok":
        L.append(f"{f['live']} live / {f['missing']} missing of {f['total']} quotes checked, of "
                 f"which **{f.get('new', '?')} are new** since the baseline in "
                 f"`refresh/freshness-baseline.json`. The standing backlog is a known quantity and "
                 f"mixes three classes — illustrative quotes that were never citations, sources "
                 f"with no local checkout, and real drift nobody has re-anchored. The new ones are "
                 f"the signal: a source moved under a citation since last month.")
        if f.get("new_misses"):
            L += [""] + [f"- {d}" for d in f["new_misses"][:40]]
    else:
        L.append(f"Freshness check did not run cleanly: {f.get('detail', '')}")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main())
