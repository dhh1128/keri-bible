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
import sys
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


def norm(s: str) -> str:
    s = s.lower().translate(_EMPH)
    s = _DASH.sub(" ", s)
    s = _SLASH.sub("/", s)
    return _WS.sub(" ", s)


def source_roots() -> list[Path]:
    m = yaml.safe_load((REPO / "refresh" / "sources.yaml").read_text())
    root = Path(os.path.expanduser(os.environ.get("CODE_ROOT", m["code_root"])))
    roots = []
    for s in m["sources"]:
        if s["kind"] != "git":
            continue                 # GitHub and web sources have no checkout; see class 2 below
        base = root / s["path"]
        for w in s.get("watch", ["."]):
            roots.append(base if any(c in w for c in "*?[") else base / w)
    # Snapshotted discussions, if any. Without them every #1613 quote reports missing forever,
    # and the real signal drowns in known-benign noise.
    cache = REPO / ".cache" / "discussions"
    if cache.is_dir():
        roots.append(cache)
    return roots


def build_corpus(roots: list[Path]) -> tuple[str, int, int]:
    live, chunks = 0, []
    for r in roots:
        if not r.exists():
            print(f"WARNING: source root missing, skipping: {r}", file=sys.stderr)
            continue
        live += 1
        files = [r] if r.is_file() else (
            p for p in r.rglob("*")
            if p.is_file() and p.suffix in EXTS
            and not (SKIP_DIRS & set(p.relative_to(r).parts)))
        for f in files:
            try:
                chunks.append(norm(f.read_text(encoding="utf-8", errors="replace")))
            except OSError:
                continue
    return " ".join(chunks), live, len(roots)


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

    roots = source_roots()
    print("building normalized source corpus...", file=sys.stderr)
    corpus, live_roots, all_roots = build_corpus(roots)

    # A dead config looks exactly like total citation rot. Refuse to report that as a result.
    if live_roots == 0:
        print("ERROR: no source roots exist. Check refresh/sources.yaml (or set CODE_ROOT). "
              "Not reporting drift.", file=sys.stderr)
        return 2
    if live_roots < all_roots / 2:
        print(f"WARNING: only {live_roots}/{all_roots} source roots resolved; counts unreliable.",
              file=sys.stderr)
    print(f"corpus: {len(corpus)} bytes from {live_roots}/{all_roots} roots", file=sys.stderr)

    baseline = load_baseline()
    total = live = 0
    missing: list[tuple[str, str, str]] = []      # (key, file, quote)
    for tf in targets:
        if not tf.is_file():
            continue
        for span in _QUOTED.findall(tf.read_text(encoding="utf-8")):
            if len(span) > MAXLEN or "\n" in span or "](" in span:
                continue            # mis-paired quotes and link-bearing prose, not citations
            frag = longest_fragment(span)
            if len(frag) < MINLEN:
                continue
            needle = norm(frag).strip(" \t.,;:!?()[]{}…")
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
