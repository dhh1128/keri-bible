#!/usr/bin/env python3
"""site_source.py — assemble the Zensical site source in _site/src from the corpus.

Usage:  python3 site/site_source.py [--commit SHA]

The chapters and the doctrine are copied as they are, so a link that resolves in the repository
resolves on the site: chapters sit in bible/, the doctrine at the root, as in the repository. The
front page and the marker legend are generated, the legend from docs/house-style.md so it is
written in one place only. Every page ends with the commit it was built from, so a citation of the
site can be tied to exact text.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site" / "src"
REPO = "https://github.com/dhh1128/keri-bible"
HEADING = re.compile(r"^# (.*?)\s*\{#[a-z0-9-]+\}\s*$")


def commit_of(arg: str | None) -> str:
    if arg:
        return arg
    return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()


def footer(sha: str, path: str) -> str:
    return f"\n\n---\n\nBuilt from commit [`{sha[:9]}`]({REPO}/blob/{sha}/{path}). Cite a section by its anchor URL on this site, or by this commit for the exact text.\n"


def legend() -> str:
    style = (ROOT / "docs/house-style.md").read_text(encoding="utf-8")
    body = re.split(r"\n## Provenance markers[^\n]*\n", style, maxsplit=1)[1].split("\n## ", 1)[0]
    body = body.replace(" This section is the legend that `build-bible.py` and the site generate from.", "")
    return "# Provenance markers {#legend}\n" + body.rstrip("\n") + "\n"


def front_page(chapters: list[tuple[str, str]], sha: str) -> str:
    lines = [
        "# The KERI Bible {#home}",
        "",
        "A synthesized reference for KERI, CESR and ACDC, built from primary sources (the specifications, the reference implementation, papers, security analysis, conference talks and the maintainers' own rulings) and written for an adversarial reviewer. It separates what is specified from what is implemented, proposed or merely practiced, and marks each claim with the kind of evidence it rests on; the [marker legend](legend.md) explains the marks. Its primary readers are AI review agents; this site is the same text for people.",
        "",
        "## Chapters {#chapters}",
        "",
    ]
    lines += [f"- [{title}](bible/{name})" for name, title in chapters]
    lines += [
        "",
        "## The doctrine {#doctrine-link}",
        "",
        "The [doctrine](keri-doctrine.md) distills the chapters into thirty rules a reviewer loads before reading anything else.",
        "",
        "## Citing this work {#citing}",
        "",
        f"Cite a section by its anchor URL on this site, which survives renumbering, and add the commit shown at the foot of the page when the exact text matters. For example: KERI Bible, chapter 02, Duplicity-evident, not duplicity-resistant, commit `{sha[:9]}`, `{REPO}`. The text is licensed CC BY 4.0; quoted passages remain under their sources' terms.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit")
    sha = commit_of(ap.parse_args().commit)

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "bible").mkdir(parents=True)

    chapters = []
    for src in sorted((ROOT / "bible").glob("*.md")):
        text = src.read_text(encoding="utf-8").rstrip("\n")
        chapters.append((src.name, HEADING.match(text.split("\n", 1)[0]).group(1)))
        (OUT / "bible" / src.name).write_text(text + footer(sha, f"bible/{src.name}"), encoding="utf-8")

    doctrine = (ROOT / "keri-doctrine.md").read_text(encoding="utf-8").rstrip("\n")
    (OUT / "keri-doctrine.md").write_text(doctrine + footer(sha, "keri-doctrine.md"), encoding="utf-8")
    (OUT / "legend.md").write_text(legend() + footer(sha, "docs/house-style.md"), encoding="utf-8")
    (OUT / "index.md").write_text(front_page(chapters, sha) + footer(sha, "README.md"), encoding="utf-8")
    shutil.copytree(ROOT / "site" / "stylesheets", OUT / "stylesheets")


if __name__ == "__main__":
    main()
