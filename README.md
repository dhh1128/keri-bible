# KERI Bible

A synthesized doctrine reference for KERI, CESR, and ACDC, built up from primary
sources (specs, papers, security analysis, and the keripy reference
implementation) into a single adversarial-reviewer-ready reference.

## Folder layout

- **`raw/`** — per-source doctrine-mining notes, one file per source (specs,
  papers, security-analysis corpus, keripy knowledge base and code). These are
  the working extraction notes that the synthesized sections are distilled from.
- **`bible/`** — the ~5k-word synthesized sections, one file per topic. Each is a
  self-contained chapter written for an adversarial reviewer, separating what is
  well-established from what is contested or load-bearing.
- **`keri-bible.md`** — the assembled reference: all `bible/` sections
  concatenated in sorted order with a title and an auto-generated table of
  contents. This is the mechanically built artifact; edit the section files in
  `bible/`, not this file.
- **`keri-doctrine.md`** — the ~6.5k-word panel-ready distillation of the whole
  corpus (marked **DRAFT**, pending endorsement). This file is **consumed by the
  `keri-review-panel` workflow**, where every persona loads it first; the panel keeps
  its own copy alongside a `reference/bible/` synced from `bible/`. Editing it here
  does not change what a review reads until the panel is synced — run
  `./sync-reference.sh` in `~/code/wot/keri-review-panel`.

## Sections (in `bible/`, sorted)

1. 01 — Foundations and Worldview
2. 02 — Security Model and Threat Posture
3. 03 — Key Management and Identifier Lifecycle
4. 04 — CESR & the Wire
5. ACDC & Verifiable Data
6. Governance, Ecosystems & Interop
7. 07 — Shibboleths and Anti-Patterns
8. Presentation Architectures & the IPEX Disclosure Model
9. KRAM & Request Authentication
10. Presentation Registries & Issuee-Side Detectability

## Building

`python3 build-bible.py > keri-bible.md` regenerates the assembled reference from
`bible/*.md`. Run it after editing any section file.

## Keeping it current

`refresh/` holds the monthly refresh: a manifest of every source with a pin recording how far it
has been read, a deterministic detector that reports what has moved since those pins, and the
prompts and standards the model phases are bound by. It runs from cron on the 3rd of each month
and delivers a draft PR against this repo. See [`refresh/README.md`](refresh/README.md) — and
[`refresh/prompts/standards.md`](refresh/prompts/standards.md), which is the citation contract for
anyone editing the corpus by hand as well.
