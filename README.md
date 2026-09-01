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
- **`keri-doctrine.md`** — the ~5k-word panel-ready distillation of the whole
  corpus (marked **DRAFT**, pending endorsement).

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

## Building

`python3 build-bible.py > keri-bible.md` regenerates the assembled reference from
`bible/*.md`. Run it after editing any section file.
