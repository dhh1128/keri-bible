# KERI Bible

A synthesized doctrine reference for KERI, CESR, and ACDC, built up from primary sources (specs, papers, security analysis, and the keripy reference implementation) into a single adversarial-reviewer-ready reference.

## Folder layout

- `raw/` — per-source doctrine-mining notes, one file per source (specs, papers, security-analysis corpus, keripy knowledge base and code, conference talks, GitHub rulings). These are the working extraction notes the chapters are distilled from.
- `bible/` — the chapters, one file per topic, each written for an adversarial reviewer and separating what is established from what is contested or load-bearing. They run from about 7,500 to 19,000 words.
- `keri-bible.md` — the assembled reference: every chapter in order, with a table of contents and the provenance-marker legend, built by `build-bible.py`. Edit the chapters in `bible/`, not this file.
- `keri-doctrine.md` — the distillation of the corpus that the `keri-review-panel` workflow loads first in every persona. The panel keeps its own copy alongside a `reference/bible/` synced from `bible/`; run `./sync-reference.sh` in `~/code/wot/keri-review-panel` after changing either.
- `docs/house-style.md` — how the corpus is written: markup, headings and anchors, citation locators, Sources entries, and the provenance-marker legend. `refresh/prompts/standards.md` says what may be claimed and on what evidence.
- `scenarios/` and `field/` — worked scenarios and field measurements that apply the doctrine.

## Chapters

The table of contents at the top of `keri-bible.md` is generated from the chapter titles and is the authoritative list.

## Building

`python3 build-bible.py > keri-bible.md` regenerates the assembled reference from `bible/*.md`. Run it after editing any section file.

## Published site

The chapters, the doctrine and the marker legend are published at https://dhh1128.github.io/keri-bible/ by `.github/workflows/pages.yml` on every push to `main`. `site/site_source.py` assembles the source and `zensical.toml` configures the build; to preview locally, run `python3 site/site_source.py` and then `zensical build --clean --strict` with the generator pinned in `requirements-site.txt`, and serve `_site/html`. A new chapter must also be added to the nav in `zensical.toml`; a unit test fails until it is.

## Checks

`.github/workflows/corpus-qa.yml` runs on every push to `main` and every pull request: the tooling unit tests (`python3 -m unittest discover -s tests`), a check that `keri-bible.md` is exactly what `build-bible.py` produces, and `tools/lint_corpus.py`, which enforces the parts of `docs/house-style.md` a script can check. Run all three locally before pushing. Quote freshness needs private sources, so it runs with the monthly refresh rather than in CI.

## Keeping it current

`refresh/` holds the monthly refresh: a manifest of every source with a pin recording how far it has been read, a deterministic detector that reports what has moved since those pins, and the prompts and standards the model phases are bound by. It runs from cron on the 3rd of each month and delivers a draft PR against this repo. See [`refresh/README.md`](refresh/README.md) — and [`refresh/prompts/standards.md`](refresh/prompts/standards.md), which is the citation contract for anyone editing the corpus by hand as well.
