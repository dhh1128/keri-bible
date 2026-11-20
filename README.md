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

## Using it with an AI assistant

The corpus is also packaged as an Agent Skill, `keri-bible`, that does two jobs. It answers questions about KERI, CESR and ACDC from the chapters, citing each section and the primary sources it quotes and carrying the provenance markers through. And it guides other work, such as a design, a review, a threat model or a plan, by reading the doctrine first and letting it shape how the work is framed and judged.

### Installing it

- Claude Code: `claude plugin marketplace add dhh1128/keri-bible`, then `claude plugin install keri-bible@keri-bible`.
- claude.ai, the Claude desktop app and ChatGPT: download https://dhh1128.github.io/keri-bible/keri-bible-skill.zip and upload it in the product's skills settings, which some plans and organizations have to turn on first.
- Codex, or Claude Code without the plugin: unzip the same file into your skills directory (`~/.codex/skills/` or `~/.claude/skills/`).

### Asking a question

Ask in plain words; the assistant picks the skill up when the question is about KERI, CESR or ACDC. For example, "What does a witness receipt threshold protect against, and what doesn't it?" or "Can an ACDC be revoked without a registry?" The answer comes back with links to the chapter sections it rests on, the spec or code quotes behind them, and a marker such as `[spec]` or `[proposal]` that says what kind of evidence each claim has. When the bible doesn't cover something, the answer says so rather than filling the gap.

### Guiding a design or review

Name the skill along with the task, so the assistant applies it even when the task doesn't mention KERI by name. In Claude Code, put `/keri-bible:keri-bible` in front of the prompt; elsewhere, start with "Using the keri-bible skill". For example:

- `/keri-bible:keri-bible Design how our mobile wallet should check an issuer's key state before accepting a credential.`
- `/keri-bible:keri-bible Review this architecture for a credential status service:` followed by the document or a path to it.
- `Using the keri-bible skill, draft a threat model for delegated identifiers in our agent platform.`

The assistant does the task you asked for, framed in KERI's terms. Where the work relies on a doctrine rule it cites the section behind it, and where the request assumes something KERI rejects, such as a central service that vouches for a key, it says so, explains why with a citation, and carries on from the corrected premise. It presents KERI's position as KERI's, including the weaknesses the bible records, so it also works when you are evaluating KERI rather than adopting it. It is one voice applying a lens, not an adversarial review, so its agreement with a design is weak evidence that the design is sound.

### Keeping it current

The skill carries a copy of the corpus, because hosted assistants run skills in a sandbox that cannot read a clone or rely on reaching the site. The stamp at the top of its `SKILL.md` names the commit it was built from, and the Pages workflow rebuilds it on every push to `main`. Claude Code does not auto-update third-party marketplaces by default: turn it on under `/plugin` > Marketplaces, or run `claude plugin update keri-bible`. An uploaded copy never updates itself, so download it again after a refresh.

`skill/SKILL.md` holds the skill's instructions and `skill/build_skill.py` packages it; `python3 skill/build_skill.py` builds it locally into `_skill/`.

## Building

`python3 build-bible.py > keri-bible.md` regenerates the assembled reference from `bible/*.md`. Run it after editing any section file.

## Published site

The chapters, the doctrine and the marker legend are published at https://dhh1128.github.io/keri-bible/ by `.github/workflows/pages.yml` on every push to `main`. `site/site_source.py` assembles the source and `zensical.toml` configures the build; to preview locally, run `python3 site/site_source.py` and then `zensical build --clean --strict` with the generator pinned in `requirements-site.txt`, and serve `_site/html`. A new chapter must also be added to the nav in `zensical.toml`; a unit test fails until it is.

## Checks

`.github/workflows/corpus-qa.yml` runs on every push to `main` and every pull request: the tooling unit tests (`python3 -m unittest discover -s tests`), a check that `keri-bible.md` is exactly what `build-bible.py` produces, and `tools/lint_corpus.py`, which enforces the parts of `docs/house-style.md` a script can check. Run all three locally before pushing. Quote freshness needs private sources, so it runs with the monthly refresh rather than in CI.

## Keeping it current

`refresh/` holds the monthly refresh: a manifest of every source with a pin recording how far it has been read, a deterministic detector that reports what has moved since those pins, and the prompts and standards the model phases are bound by. It runs from cron on the 3rd of each month and delivers a draft PR against this repo. See [`refresh/README.md`](refresh/README.md) — and [`refresh/prompts/standards.md`](refresh/prompts/standards.md), which is the citation contract for anyone editing the corpus by hand as well.
