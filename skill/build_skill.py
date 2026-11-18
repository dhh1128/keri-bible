#!/usr/bin/env python3
"""build_skill.py — package the corpus as an Agent Skill, and as a Claude Code plugin around it.

Usage:  python3 skill/build_skill.py [--out DIR]

Writes three things into DIR (default _skill/):

  keri-bible/               the skill folder: SKILL.md, plus the chapters, the doctrine, the marker
                            legend and a generated section index under references/
  keri-bible-skill.zip      that folder, for uploading to claude.ai or ChatGPT, or unpacking into a
                            Claude Code or Codex skills directory
  keri-bible-plugin.zip     a Claude Code plugin holding the same skill, which the marketplace in
                            .claude-plugin/marketplace.json installs

The chapters and the doctrine are copied unchanged into the same relative layout they have in the
repository (doctrine beside bible/), so every link between them still resolves inside the skill.

The stamp names the last commit that changed anything the skill is built from, not HEAD, and the
zips are byte-for-byte reproducible. Claude Code versions an unpinned archive plugin by the digest
of the download, so an unrelated commit must not produce a new digest, or every installed copy
would update for nothing.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://dhh1128.github.io/keri-bible/"
REPO = "https://github.com/dhh1128/keri-bible"
NAME = "keri-bible"
INPUTS = ["bible", "keri-doctrine.md", "docs/house-style.md", "skill"]

HEADING = re.compile(r"^(#{1,4}) (.*?)\s*\{#([a-z0-9-]+)\}\s*$")
MARKER = re.compile(r"\[(spec-next|spec|code|proposal|practice|architect)\]")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def stamp() -> str:
    """'Corpus stamp: commit <sha>, <date>.' for the last commit that touched an input."""
    out = subprocess.run(
        ["git", "-C", str(ROOT), "log", "-1", "--format=%H %cs", "--", *INPUTS],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    if len(out) != 2:
        raise SystemExit("build_skill: no commit touches the skill's inputs; is this a shallow clone?")
    sha, date = out
    return (
        f"Corpus stamp: commit [`{sha[:9]}`]({REPO}/tree/{sha}), {date}. "
        f"The published text at {SITE} may be newer."
    )


def legend() -> str:
    style = (ROOT / "docs/house-style.md").read_text(encoding="utf-8")
    body = re.split(r"\n## Provenance markers[^\n]*\n", style, maxsplit=1)[1].split("\n## ", 1)[0]
    body = body.replace(" This section is the legend that `build-bible.py` and the site generate from.", "")
    return "# Provenance markers {#legend}\n" + body.rstrip("\n") + "\n"


def sections(text: str) -> list[tuple[int, str, str, set[str]]]:
    """(level, title, anchor, markers) for each anchored heading outside code fences.

    The markers are those that appear between this heading and the next heading at any level, so a
    section's entry describes its own text and not its subsections'.
    """
    out: list[tuple[int, str, str, set[str]]] = []
    fence = False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = HEADING.match(line)
        if m:
            out.append((len(m.group(1)), m.group(2), m.group(3), set()))
        elif out:
            out[-1][3].update(MARKER.findall(line))
    return out


def index(chapters: list[Path]) -> str:
    lines = [
        "# Section index {#index}",
        "",
        "Every chapter, section and subsection, with its anchor and the provenance markers used in its own text. To read a section, open the chapter file and search for `{#anchor}`. To cite it, append `#anchor` to the chapter's published URL. Markers in brackets are the kinds of evidence the section's text carries, strongest claims and weakest alike, so a section listing `[proposal]` contains at least one claim that binds nobody.",
        "",
    ]
    for path in chapters:
        text = path.read_text(encoding="utf-8")
        secs = sections(text)
        level, title, anchor, _ = secs[0]
        url = f"{SITE}bible/{path.stem}/"
        lines += [f"## {title}", "", f"File `references/bible/{path.name}`, published at {url}", ""]
        for level, title, anchor, markers in secs[1:]:
            tag = " " + " ".join(f"[{m}]" for m in sorted(markers)) if markers else ""
            indent = "  " * max(level - 2, 0)
            lines.append(f"{indent}- {title} `#{anchor}`{tag}")
        lines.append("")
    return "\n".join(lines)


def build_folder(dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    refs = dest / "references"
    (refs / "bible").mkdir(parents=True)

    chapters = sorted((ROOT / "bible").glob("*.md"))
    for path in chapters:
        shutil.copyfile(path, refs / "bible" / path.name)
    shutil.copyfile(ROOT / "keri-doctrine.md", refs / "keri-doctrine.md")
    (refs / "markers.md").write_text(legend(), encoding="utf-8")
    (refs / "index.md").write_text(index(chapters), encoding="utf-8")
    shutil.copyfile(ROOT / "LICENSE", dest / "LICENSE")

    skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
    (dest / "SKILL.md").write_text(skill.replace("{{STAMP}}", stamp()), encoding="utf-8")


def plugin_manifest() -> str:
    return (
        "{\n"
        f'  "name": "{NAME}",\n'
        '  "description": "Answers about KERI, CESR and ACDC grounded in the KERI Bible, with citations and provenance markers, and a doctrine lens for design and review work.",\n'
        '  "author": { "name": "Daniel Hardman" },\n'
        f'  "homepage": "{SITE}",\n'
        f'  "repository": "{REPO}",\n'
        '  "license": "CC-BY-4.0"\n'
        "}\n"
    )


PLUGIN_README = f"""# KERI Bible plugin

This plugin carries one skill, `keri-bible`, which grounds work on KERI, CESR and ACDC in the KERI Bible ({SITE}). Ask a question about these protocols and the answer cites the chapter sections it rests on, the primary sources they quote, and the provenance marker that says what kind of evidence each claim has. Invoke it alongside another task, such as `/keri-bible:keri-bible review this witness pool design`, and KERI's doctrine shapes the work instead.

The plugin is rebuilt from {REPO} whenever the corpus changes, and the stamp at the top of `skills/keri-bible/SKILL.md` names the commit it was built from. The text is licensed CC BY 4.0; quoted passages remain under their sources' terms.
"""


def write_zip(zpath: Path, entries: list[tuple[str, bytes]]) -> None:
    """A zip whose bytes depend only on the entries: fixed times, fixed modes, sorted names."""
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data, compresslevel=9)


def files_under(folder: Path, prefix: str) -> list[tuple[str, bytes]]:
    return [
        (prefix + p.relative_to(folder).as_posix(), p.read_bytes())
        for p in sorted(folder.rglob("*")) if p.is_file()
    ]


def build(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    folder = out / NAME
    build_folder(folder)
    skill_files = files_under(folder, f"{NAME}/")
    write_zip(out / f"{NAME}-skill.zip", skill_files)
    plugin = [(f"skills/{name}", data) for name, data in skill_files]
    plugin.append((".claude-plugin/plugin.json", plugin_manifest().encode("utf-8")))
    plugin.append(("README.md", PLUGIN_README.encode("utf-8")))
    write_zip(out / f"{NAME}-plugin.zip", plugin)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "_skill"))
    build(Path(ap.parse_args().out))


if __name__ == "__main__":
    main()
