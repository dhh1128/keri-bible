#!/usr/bin/env python3
"""freshness.py — quote-drift checker for the bible.

The corpus cites sources with exact QUOTES as the durable anchor and bare line numbers only as
hints. This checks whether each quoted span still exists in the live sources. A quote no longer
found is a fail-LOUD signal that the source drifted and the citation needs re-verifying.

Descended from ~/code/wot/keri-review-panel/freshness.sh, with two changes that matter:

  * SOURCE ROOTS COME FROM refresh/sources.yaml, not a hardcoded list. The panel copy's list
    pointed at pre-reorg paths for about six weeks; because a missing root was skipped silently,
    it either reported total citation rot or was never run, and nobody could tell which. One
    manifest, one place to be wrong.

  * IT IS PYTHON, because the corpus outgrew the shell. The bash version ran one `grep -F` per
    quote over a multi-megabyte corpus: fine for the panel's few hundred quotes, quadratic and
    unusable for the bible's whole raw/ + bible/ set. Here the corpus is normalized once into
    memory and each quote is a substring test.

Usage:  ./freshness.py [file.md ...]   (defaults to bible/*.md, raw/*.md, keri-doctrine.md)
Exit:   0 = every quote found, 1 = some missing, 2 = config is dead (refuses to report drift)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from fnmatch import fnmatch
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
BASELINE = REPO / "refresh" / "freshness-baseline.json"
MINLEN = 24                      # skip short quoted spans: terms and framings, not citations
# Cap the upper end too. The standards cap a citation at 25 words (~200 chars); a longer "span"
# is almost always the regex pairing one sentence's closing quote with a later sentence's opening
# one, which then reports a whole paragraph as drifted. That false positive buried the real signal
# in the bash predecessor — 2,039 of 3,331 quotes "missing", nearly all of them artifacts.
MAXLEN = 320
EXTS = {".md", ".py", ".ts", ".txt", ".json"}
# Matched against a path RELATIVE to its root, never the absolute path. An earlier version tested
# absolute parts and carried "docs" in this set, which silently excluded every file under
# origin-platform/docs — a watched root — and reported 84 perfectly good quotes as drifted. That is
# precisely the "dead config looks like citation rot" failure this script is supposed to refuse.
SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv"}

_EMPH = str.maketrans("", "", "*_`\"'")
_DASH = re.compile(r"[—–]")
_SLASH = re.compile(r" */ *")
_WS = re.compile(r"\s+")
_QUOTED = re.compile(r'"([^"]{%d,})"' % MINLEN)
_GLUE = re.compile(r"@`[0-9a-f]{7,}`|\bL\d+[,.)]|^\s*\w+\.md\s+§")
_EDITORIAL = re.compile(r"\[(sic|emphasis added|emphasis mine|\.\.\.|…)\]", re.I)
# A genuine quotation opens with a word, a digit, or an opening mark. A span that opens with a
# comma, a closing bracket or a dash is the regex having paired one quote's closing mark with the
# next quote's opening one, and the text between them is the citation, not the quotation.
_OPENS = re.compile(r"[\w*_`'\"(\[“‘]")


def norm(s: str) -> str:
    s = s.lower().translate(_EMPH)
    s = _DASH.sub(" ", s)
    s = _SLASH.sub("/", s)
    return _WS.sub(" ", s)


def tracked_refs() -> list[tuple[Path, str, list[str]]]:
    """(repo, ref, watch-paths) for every tracked branch of every git source.

    The corpus is read from the REF, not from the working tree. Reading the tree means the check
    silently depends on whichever branch each repo happens to be sitting on — the first real run
    hit exactly that: keripy was parked on a feature branch, so "verified against keripy" meant
    "verified against somebody's work in progress". Every tracked line is read, so a quote living
    only in v1.1 resolves too; which TIER it belongs to is the report's job, not this one's.
    """
    m = yaml.safe_load((REPO / "refresh" / "sources.yaml").read_text())
    root = Path(os.path.expanduser(os.environ.get("CODE_ROOT", m["code_root"])))
    out = []
    for s in m["sources"]:
        if s["kind"] != "git":
            continue                 # GitHub and web sources have no checkout; see class 2 below
        base = root / s["path"]
        watch = s.get("watch", ["."])
        for b in s.get("branches", []):
            out.append((base, f"{s['remote']}/{b['name']}", watch))
            out.append((base, b["name"], watch))     # local-only branch fallback (worktrees)
    return out


def read_ref(repo: Path, ref: str, watch: list[str]) -> str | None:
    """Concatenated text of the watched paths at `ref`, or None if the ref does not resolve."""
    if subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", ref],
                      capture_output=True).returncode != 0:
        return None
    # List the whole tree and filter in Python. `git ls-tree -- '*.md'` matches NOTHING — the
    # pathspec is not globbed the way a shell would glob it — and a watch entry of ["*.md"] then
    # yields an empty, perfectly quiet result. That silently emptied `papers` and
    # `keri-security-analysis` out of the corpus and reported ~150 sound quotes as drifted.
    files = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", ref],
                           capture_output=True, text=True)
    if files.returncode != 0:
        return None
    literals = [w.rstrip("/") for w in watch if not any(c in w for c in "*?[") and w != "."]
    globs = [w for w in watch if any(c in w for c in "*?[")]
    everything = not literals and not globs      # watch: ["."] means the whole tree

    def wants(f: str) -> bool:
        if everything:
            return True
        if any(f == w or f.startswith(w + "/") for w in literals):
            return True
        return any(fnmatch(f, g) or fnmatch(Path(f).name, g) for g in globs)

    wanted = [f for f in files.stdout.split("\n")
              if f and wants(f) and Path(f).suffix in EXTS
              and not (SKIP_DIRS & set(Path(f).parts))]
    # A watched path can be real on disk and absent from the tree. The Dossier spec's `.ref/`
    # directory is untracked, so reading refs alone dropped 96 of that note's quotes — a corpus
    # gap wearing the costume of citation rot. Fall back to the working copy for exactly those
    # paths, because there is no ref to read them from.
    extra = []
    for w in literals:
        if any(f == w or f.startswith(w + "/") for f in wanted):
            continue
        ondisk = repo / w
        if ondisk.is_dir():
            extra += [q for q in ondisk.rglob("*")
                      if q.is_file() and q.suffix in EXTS
                      and not (SKIP_DIRS & set(q.relative_to(ondisk).parts))]
        elif ondisk.is_file() and ondisk.suffix in EXTS:
            extra.append(ondisk)

    chunks = []
    for i in range(0, len(wanted), 200):           # keep the argv under the exec limit
        batch = wanted[i:i + 200]
        cat = subprocess.run(["git", "-C", str(repo), "show"] + [f"{ref}:{f}" for f in batch],
                             capture_output=True, text=True, errors="replace")
        chunks.append(cat.stdout)
    for q in extra:
        chunks.append(q.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(chunks)


def build_corpus() -> tuple[str, int, int]:
    chunks, resolved, repos = [], 0, set()
    for repo, ref, watch in tracked_refs():
        if not (repo / ".git").exists():
            continue
        text = read_ref(repo, ref, watch)
        if text is None:
            continue                 # this branch does not exist here; a sibling entry may
        resolved += 1
        repos.add(str(repo))
        chunks.append(norm(text))

    for repo in {r for r, _, _ in tracked_refs()}:
        if not (repo / ".git").exists():
            print(f"WARNING: source not a git checkout, skipping: {repo}", file=sys.stderr)

    # Snapshotted discussions, if any. Without them every #1613 quote reports missing forever,
    # and the real signal drowns in known-benign noise. These are files, not refs.
    cache = REPO / ".cache" / "discussions"
    if cache.is_dir():
        for f in cache.glob("*.md"):
            chunks.append(norm(f.read_text(encoding="utf-8", errors="replace")))
        resolved += 1
    return " ".join(chunks), resolved, len(repos)


def longest_fragment(span: str) -> str:
    """Elided quotes ("A... B") match on their longest fragment."""
    return max((p.strip() for p in span.split("...")), key=len, default="")


def load_baseline() -> dict:
    if BASELINE.exists():
        return json.loads(BASELINE.read_text())
    return {"generated": None, "misses": {}}


def key_of(needle: str) -> str:
    return hashlib.sha1(needle.encode()).hexdigest()[:12]


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    update = "--update-baseline" in sys.argv
    targets = [Path(a) for a in args]
    if not targets:
        targets = sorted(REPO.glob("bible/*.md")) + sorted(REPO.glob("raw/*.md"))
        targets.append(REPO / "keri-doctrine.md")

    print("building normalized source corpus from tracked refs...", file=sys.stderr)
    corpus, refs, repos = build_corpus()

    # A dead config looks exactly like total citation rot. Refuse to report that as a result.
    if refs == 0:
        print("ERROR: no source ref resolved. Check refresh/sources.yaml (or set CODE_ROOT). "
              "Not reporting drift.", file=sys.stderr)
        return 2
    print(f"corpus: {len(corpus)} bytes from {refs} refs across {repos} repos", file=sys.stderr)

    baseline = load_baseline()
    total = live = 0
    missing: list[tuple[str, str, str]] = []      # (key, file, quote)
    for tf in targets:
        if not tf.is_file():
            continue
        for span in _QUOTED.findall(tf.read_text(encoding="utf-8")):
            if len(span) > MAXLEN or "\n" in span or "](" in span:
                continue            # mis-paired quotes and link-bearing prose, not citations
            # Citation glue: the regex happily pairs one quote's closing mark with the next
            # quote's opening one, capturing the parenthetical between them — `(wtbo §4, L91
            # @`181569b64`).` is not a quotation and can never be found in a source.
            if _GLUE.search(span) or not _OPENS.match(span.strip()):
                continue
            frag = longest_fragment(span)
            if len(frag) < MINLEN:
                continue
            # Editorial insertions — [sic], [emphasis added], [the Issuee] — are the quoter's
            # words, not the source's, so they must come out before matching.
            needle = norm(_EDITORIAL.sub(" ", frag)).strip(" \t.,;:!?()[]{}…")
            total += 1
            if needle in corpus:
                live += 1
            else:
                missing.append((key_of(needle), tf.name, frag))

    fresh = [m for m in missing if m[0] not in baseline["misses"]]
    healed = [k for k in baseline["misses"] if k not in {m[0] for m in missing}]

    if update:
        BASELINE.write_text(json.dumps(
            {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
             "note": ("Quotes known not to resolve against the live sources, so that a run can "
                      "report what is NEWLY broken instead of re-reporting a standing backlog. A "
                      "baseline entry is not absolution — most of these are class 1 or 2, but some "
                      "are real drift nobody has re-anchored yet. Refresh with "
                      "refresh/freshness.py --update-baseline, and only after you have looked."),
             "misses": {k: {"file": f, "quote": q[:160]} for k, f, q in missing}},
            indent=2, sort_keys=True) + "\n")
        print(f"baseline updated: {len(missing)} known misses recorded")

    print(f"freshness: {live} live / {len(missing)} missing of {total} checked quotes "
          f"(minlen {MINLEN}, markup-normalized)")
    if update:
        print("new misses: n/a (baseline was just rewritten from this run)")
        fresh = []
    else:
        print(f"new misses: {len(fresh)} (not in baseline); healed since baseline: {len(healed)}")

    if fresh:
        print()
        print("NEW MISSES — these resolved at the last baseline and do not now. This is the "
              "actionable signal: a source moved under a citation.")
        for k, f, q in fresh:
            print(f"  ! [{f}] {q}")

    if missing:
        print()
        print("MISSING — not found in live sources; re-verify these citations.")
        print("A miss falls into one of three classes, and only the third is actionable:")
        print("  1. NOT A CITATION. Illustrative 'outsider-framing' quotes in the shibboleth table")
        print("     are hypothetical text. They can never be found.")
        print("  2. NOT ON DISK. A source with no local checkout — an unsnapshotted GitHub")
        print("     discussion, keri.one, the KERIcon captions.")
        print("  3. REAL DRIFT. A quote that should be in a spec/paper/code root and is not. This")
        print("     is the signal: re-read the source and re-anchor the citation.")
        print("This script cannot tell the three apart, so treat the total as an upper bound.")
        for _, f, q in missing:
            print(f"  - [{f}] {q}")
    return 1 if fresh else 0


if __name__ == "__main__":
    sys.exit(main())
