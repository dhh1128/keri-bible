#!/usr/bin/env python3
"""lint_corpus.py — check the rules in docs/house-style.md that a script can check.

Usage:  python3 tools/lint_corpus.py [--root DIR]
Exit:   0 clean, 1 violations (one line each, file:line: rule: detail)

Two scopes, because the raw mining notes predate the house style and are working notes rather
than published text:

  * Every tracked markdown file except generated refresh output must not be hard-wrapped.
  * The published text (bible/, docs/, keri-doctrine.md) must also follow the markup, heading,
    anchor and link rules.

Quotations and code spans are exempt from the emphasis and section-sign rules, because a quote
must match its source byte for byte and a code span is literal.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

GENERATED = ("refresh/state/",)
PUBLISHED_DIRS = ("bible/", "docs/")
PUBLISHED_FILES: tuple[str, ...] = ("keri-doctrine.md",)

HEADING = re.compile(r"^(#{1,6}) (.*)$")
ANCHOR_AT_END = re.compile(r"\s\{#([a-z0-9]+(?:-[a-z0-9]+)*)\}\s*$")
CODE_SPAN = re.compile(r"`[^`\n]*`")
QUOTE = re.compile(r'"[^"\n]*"')
LINK_TARGET = re.compile(r"\]\(([^)\s]*)\)")
STRUCTURAL = re.compile(r"^\s*(#|```|\||>|[-*+] |\d+[.)] |---\s*$|<|\[\^)")
BOLD = re.compile(r"\*\*[^*\n]+\*\*|(?<![\w.])__(?=\S)[^_\n]+(?<=\S)__(?!\w)")
ITALIC = re.compile(r"(?<![\w*])\*(?![\s*])[^*\n]+?(?<![\s*])\*(?![\w*])|(?<![\w_])_(?![\s_])[^_\n]+?(?<![\s_])_(?![\w_])")
CHAPTER_H1 = re.compile(r"^\d\d — [^&]+$")
NUMBERED_H2 = re.compile(r"^\d+\. ")
NUMBERED_H3 = re.compile(r"^\d+\.\d+ ")
BODY_LIMIT = 7500  # docs/house-style.md, Length


def strip_literals(line: str) -> str:
    """Blank out code spans and quotations so their contents are never linted."""
    line = CODE_SPAN.sub(lambda m: " " * len(m.group(0)), line)
    return QUOTE.sub(lambda m: " " * len(m.group(0)), line)


def prose_lines(text: str):
    """Yield (lineno, line, in_fence) for every line, tracking fenced code blocks."""
    fence = False
    for n, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            yield n, line, True
            continue
        yield n, line, fence


def check_wrap(path: str, text: str) -> list[str]:
    out, prev = [], ""
    for n, line, fence in prose_lines(text):
        plain = lambda s: s.strip() and not STRUCTURAL.match(s) and not s.startswith((" ", "\t"))
        if not fence and plain(line) and plain(prev) and not prev.endswith("  "):
            out.append(f"{path}:{n}: hard-wrap: paragraph continues from the previous line")
        prev = "" if fence else line
    return out


def heading_info(text: str):
    for n, line, fence in prose_lines(text):
        if fence:
            continue
        m = HEADING.match(line)
        if m:
            yield n, len(m.group(1)), m.group(2)


def check_published(path: str, text: str, anchors_by_file: dict[str, set[str]]) -> list[str]:
    out = []
    for n, line, fence in prose_lines(text):
        if fence:
            continue
        bare = strip_literals(line)
        if BOLD.search(bare):
            out.append(f"{path}:{n}: emphasis: bold outside a quotation or code span")
        elif ITALIC.search(bare.replace("\\*", "").replace("\\_", "")):
            out.append(f"{path}:{n}: emphasis: italics outside a quotation or code span")
        if "§" in bare:
            out.append(f"{path}:{n}: section-sign: write the locator or cross-reference in words")
        if " -- " in bare:
            out.append(f"{path}:{n}: dash: use an em dash, not --")

    seen: dict[str, int] = {}
    prev_level = 0
    for n, level, text_ in heading_info(text):
        m = ANCHOR_AT_END.search(text_)
        if not m:
            out.append(f"{path}:{n}: anchor: heading has no {{#anchor}}")
        else:
            a = m.group(1)
            if a in seen:
                out.append(f"{path}:{n}: anchor: '{a}' already used at line {seen[a]}")
            seen[a] = n
            text_ = text_[: m.start()]
        if "&" in strip_literals(text_):
            out.append(f"{path}:{n}: heading: no ampersands; write 'and'")
        if prev_level and level > prev_level + 1:
            out.append(f"{path}:{n}: heading: skips from H{prev_level} to H{level}")
        prev_level = level

    if path.startswith("bible/"):
        heads = [(lvl, ANCHOR_AT_END.sub("", t).strip()) for _, lvl, t in heading_info(text)]
        if not heads or heads[0][0] != 1 or not CHAPTER_H1.match(heads[0][1]):
            out.append(f"{path}:1: skeleton: first line must be '# NN — Title {{#anchor}}'")
        h2 = [t for lvl, t in heads if lvl == 2]
        if not h2 or h2[0] != "Thesis":
            out.append(f"{path}:1: skeleton: the first H2 must be Thesis")
        if not h2 or h2[-1] != "Sources":
            out.append(f"{path}:1: skeleton: the last H2 must be Sources")
        sources_line = next((n for n, lvl, t in heading_info(text) if lvl == 2 and ANCHOR_AT_END.sub("", t).strip() == "Sources"), None)
        lines = text.split("\n")
        body_words = len(" ".join(lines[: sources_line - 1] if sources_line else lines).split())
        if body_words > BODY_LIMIT:
            out.append(f"{path}:1: length: body is {body_words} words; the budget is 6,000 and the limit {BODY_LIMIT:,}")
        for t in h2:
            if t not in ("Thesis", "Status", "Sources") and not NUMBERED_H2.match(t):
                out.append(f"{path}:1: skeleton: unexpected unnumbered H2 '{t}'")

    here = Path(path)
    for n, line, fence in prose_lines(text):
        if fence:
            continue
        for target in LINK_TARGET.findall(strip_literals_keep_links(line)):
            if "://" in target or target.startswith("mailto:") or "#" not in target:
                continue
            file_part, anchor = target.split("#", 1)
            key = str((here.parent / file_part).as_posix()) if file_part else path
            key = str(Path(key))
            if key in anchors_by_file and anchor not in anchors_by_file[key]:
                out.append(f"{path}:{n}: link: #{anchor} not found in {key}")
    return out


def strip_literals_keep_links(line: str) -> str:
    return CODE_SPAN.sub(lambda m: " " * len(m.group(0)), line)


def anchors_of(text: str) -> set[str]:
    return set(re.findall(r"\{#([a-z0-9-]+)\}", text))


def tracked_markdown(root: Path) -> list[str]:
    r = subprocess.run(["git", "-C", str(root), "ls-files", "*.md"], capture_output=True, text=True, check=True)
    return [p for p in r.stdout.split() if p]


def lint(root: Path, files: list[str] | None = None) -> list[str]:
    files = files if files is not None else tracked_markdown(root)
    texts = {f: (root / f).read_text(encoding="utf-8") for f in files}
    published = [f for f in files if f.startswith(PUBLISHED_DIRS) or f in PUBLISHED_FILES]
    anchors = {str(Path(f)): anchors_of(texts[f]) for f in published}
    out = []
    for f in files:
        if f.startswith(GENERATED) or f == "keri-bible.md":
            continue
        out += check_wrap(f, texts[f])
        if f in published:
            out += check_published(f, texts[f], anchors)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    problems = lint(Path(args.root))
    for p in problems:
        print(p)
    print(f"lint_corpus: {len(problems)} problem(s)", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
