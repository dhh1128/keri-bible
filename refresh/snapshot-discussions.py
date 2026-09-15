#!/usr/bin/env python3
"""snapshot-discussions.py — make GitHub-discussion quotes verifiable and drift-detectable.

GitHub discussions are among the most doctrinally live sources the bible has (#934, #1095, #1613,
#1618, #1627) and the only major ones with no local checkout. Two consequences, both bad:

  * freshness.py can never find a quote from one, so every discussion citation reports missing
    forever and the signal drowns in known-benign noise.
  * Sam edits posts in place. #1095 and #1613 both carry a "last edited" stamp. A quote can go
    stale with no commit anywhere, and nothing would say so.

This fetches every discussion cited anywhere in the bible into .cache/discussions/ (UNTRACKED —
the repo is public and the prose is Sam's) and records a TRACKED manifest of URL, fetch date and
SHA-256. So the text is re-verifiable by anyone who runs this, drift is detectable by comparing
hashes, and nothing of his is republished here.

Usage:
    ./snapshot-discussions.py            # snapshot everything cited, report drift
    ./snapshot-discussions.py --check    # report drift only; write nothing
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / ".cache" / "discussions"
MANIFEST = REPO / "refresh" / "discussion-snapshots.json"
CITE = re.compile(r"github\.com/([\w.-]+)/([\w.-]+)/discussions/(\d+)")

QUERY = """
query($owner:String!, $name:String!, $number:Int!) {
  repository(owner:$owner, name:$name) {
    discussion(number:$number) {
      number title url createdAt updatedAt lastEditedAt bodyText
      author { login } category { name }
      comments(first:100) {
        totalCount
        nodes { author { login } createdAt lastEditedAt bodyText
                replies(first:50) { nodes { author { login } createdAt bodyText } } }
      }
    }
  }
}"""


def cited() -> set[tuple[str, str, int]]:
    found = set()
    for p in list(REPO.glob("bible/*.md")) + list(REPO.glob("raw/*.md")) + [REPO / "keri-doctrine.md"]:
        if p.exists():
            for owner, name, num in CITE.findall(p.read_text(encoding="utf-8")):
                found.add((owner, name, int(num)))
    return found


def fetch(owner: str, name: str, number: int) -> dict:
    p = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}",
                        "-F", f"owner={owner}", "-F", f"name={name}", "-F", f"number={number}"],
                       capture_output=True, text=True)
    # gh writes error bodies to stdout, so exit status is the only honest check.
    if p.returncode != 0:
        raise RuntimeError(f"gh api failed for {owner}/{name}#{number}: {p.stderr.strip()[:300]}")
    d = json.loads(p.stdout)["data"]["repository"]["discussion"]
    if d is None:
        raise RuntimeError(f"{owner}/{name}#{number} not found or not visible")
    return d


def render(d: dict) -> str:
    out = [f"# {d['title']}", "",
           f"{d['url']} — {(d['author'] or {}).get('login', '?')}, category {d['category']['name']}",
           f"created {d['createdAt'][:10]}, updated {d['updatedAt'][:10]}"
           + (f", last edited {d['lastEditedAt'][:10]}" if d["lastEditedAt"] else ""),
           "", "---", "", d["bodyText"].strip(), ""]
    for c in d["comments"]["nodes"]:
        out += ["", "---", "",
                f"## comment — {(c['author'] or {}).get('login', '?')}, {c['createdAt'][:10]}"
                + (f" (edited {c['lastEditedAt'][:10]})" if c["lastEditedAt"] else ""),
                "", c["bodyText"].strip()]
        for r in c["replies"]["nodes"]:
            out += ["", f"### reply — {(r['author'] or {}).get('login', '?')}, {r['createdAt'][:10]}",
                    "", r["bodyText"].strip()]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report drift; write nothing")
    args = ap.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"snapshots": {}}
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    drifted, added, errors = [], [], []
    for owner, name, number in sorted(cited()):
        key = f"{owner}/{name}#{number}"
        try:
            d = fetch(owner, name, number)
        except RuntimeError as e:
            errors.append(str(e))
            continue
        text = render(d)
        digest = hashlib.sha256(text.encode()).hexdigest()
        prior = manifest["snapshots"].get(key)

        if prior and prior["sha256"] != digest:
            drifted.append(f"{key} — content changed since {prior['fetched']} "
                           f"(GitHub says last edited {d['lastEditedAt'] or 'never'}). "
                           f"Re-verify every quote citing it.")
        elif not prior:
            added.append(key)

        if not args.check:
            (CACHE / f"{owner}-{name}-{number}.md").write_text(text)
            manifest["snapshots"][key] = {
                "url": d["url"], "title": d["title"],
                "author": (d["author"] or {}).get("login", "?"),
                "created": d["createdAt"][:10], "updated": d["updatedAt"][:10],
                "last_edited": (d["lastEditedAt"] or "")[:10],
                "comments": d["comments"]["totalCount"],
                "fetched": today, "sha256": digest,
                "file": f".cache/discussions/{owner}-{name}-{number}.md",
            }

    if not args.check:
        manifest["note"] = ("Snapshots live in .cache/discussions/ and are deliberately untracked: "
                            "this repo is public and the text is other people's writing. The hashes "
                            "here are what makes a quote re-verifiable and an in-place edit visible. "
                            "Regenerate with refresh/snapshot-discussions.py.")
        MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    for a in added:
        print(f"new snapshot: {a}")
    for d in drifted:
        print(f"DRIFT: {d}")
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    print(f"{len(manifest['snapshots'])} snapshots, {len(drifted)} drifted, {len(errors)} errors")
    return 2 if errors else (1 if drifted else 0)


if __name__ == "__main__":
    sys.exit(main())
