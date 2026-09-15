# Refresh delta — 2026-09-15

Tiers scanned: hot, warm. Previous run: none.

## Sources

### keri-spec — MOVED
Feeds `raw/01-keri-spec.md` → chapters 01, 02, 03, 04, 06, 07, 09.
Caveat: raw/01 carries no pin of its own; 4df80aa is the corpus-wide 2026-07-17 stamp recorded in keri-doctrine.md. Its line-number hints (L33, L89, L1836…) are hints as of that commit only.

**main** (standardizing, [N]) `4df80aa` → `fbdd4a615`
  -  2 files changed, 28 insertions(+), 14 deletions(-)
  - `0fce77c` 2026-08-05 Daniel Hardman: Fix "hexidecimal" typo in the Event seal field descriptions
  - `547cb7e` 2026-05-29 Kevin Griffin: updates to well-known oobis for provisional IANA registration of .well-known/oobi
  - `37ded2a` 2026-02-10 henkvancann: tref installed

**v1.1** (forward, [N1.1]) `unknown` → `3753f3797` — **no pin of record; treat as a full re-anchor, not a delta**


### cesr-spec — MOVED
Feeds `raw/02-cesr-spec.md` → chapters 04, 07.

**main** (standardizing, [N]) `d35125e` → `bad6edd84` — **pin is not an ancestor of the head; branch rebased or retargeted**
  -  1 file changed, 1 insertion(+), 17 deletions(-)

**v1.1** (forward, [N1.1]) `unknown` → `65fd7518b` — **no pin of record; treat as a full re-anchor, not a delta**


### acdc-spec — MOVED
Feeds `raw/03-acdc-spec.md` → chapters 05, 07, 08, 10.
Caveat: Partially re-anchored at f0bd097 on 2026-09-01 for the bible 09/10 material only (rd, rip, blindable state registries). The rest of raw/03 still stands at 11832a3.

**main** (standardizing, [N]) `f0bd097` → `f0bd097de`

**v1.1** (forward, [N1.1]) `unknown` → `2362e48a1` — **no pin of record; treat as a full re-anchor, not a delta**


### dossier-spec — MOVED
Feeds `raw/04-dossier-spec.md` → chapters 05, 06, 08.

**main** (standardizing, [N]) `3900e62` → `b9227753c` — **pin is not an ancestor of the head; branch rebased or retargeted**
  -  9 files changed, 118 insertions(+), 49 deletions(-)
  - `b922775` 2026-08-25 Daniel Hardman: Correct signing language in the schemas and recompute their SAIDs
  - `b97c2f2` 2026-08-25 Daniel Hardman: Distinguish anchoring from signing throughout the spec
  - `5906e8c` 2026-08-12 Daniel Hardman: Normalize heading capitalization to title case
  - `7aeadc2` 2026-08-06 henkvancann: first try amendments and comments to the Dossier spec
  - `c2d261c` 2026-06-30 Daniel Hardman: Prune obsolete qualification-operator term; link live glossary terms
  - `ff5b0a4` 2026-06-09 Daniel Hardman: Replace the `m` threshold field with weighted-unity thresholds
  - `e99878d` 2026-06-09 Daniel Hardman: Use a single threshold field name `m` across all four operators
  - `9d8f9a0` 2026-06-09 Daniel Hardman: Consolidate endorsement/declination/qualified schemas into one
  - `4dae85a` 2026-06-09 Daniel Hardman: Replace M/Q/FIN joint-issuance model with MxN/RMxN/MxQ/RMxQ operators


### keripy-code — MOVED
Feeds `raw/09-keripy-code.md`, `raw/15-kram.md`, `raw/16-presentation-registries.md` → chapters 03, 04, 05, 08, 09, 10.
Caveat: last_mined is deliberately the OLDER pin. raw/15 and raw/16's implementation-status sections were verified at 4df8e4a8 (2026-09-01) and kraming.py at fe161709; raw/09 has not been re-read since the 2026-07-17 corpus stamp. Under-claim rather than over-claim.

**main** (standardizing, [K]) `4df8e4a8` → `b8f60166b`
  -  13 files changed, 1964 insertions(+), 452 deletions(-)
  - `c9b2b55cc` 2026-09-11 Keanu: tighten anchor validation
  - `5384edc8d` 2026-09-10 Samuel M Smith: upgraded to version 2.1.0.dev1
  - `74d431c34` 2026-09-10 Keanu: add KEL anchoring for ax
  - `90ee99bef` 2026-09-08 Evan Asakawa: fix EXN evidence handling
  - `1914bce5a` 2026-09-08 Evan Asakawa: Fix IPEX proof verification and escrow
  - `d70f670c7` 2026-09-02 Evan Asakawa: Verify EXN evidence and clear KRAM partials
  - `e46fd026a` 2026-08-31 Evan Asakawa: Clarify and test EXN evidence handling
  - `f7c5723d6` 2026-08-31 Evan Asakawa: Persist verified IPEX evidence
  - `72131e52f` 2026-09-07 Samuel M Smith: created ACDCs for guy and gal guardian IARs
  - `fbc6bcaf9` 2026-09-07 Keanu: adjust docstring anda comments
  - `30825b63d` 2026-09-04 Evan Asakawa: Simplify targeted Compactor disclosure
  - `30be2cf07` 2026-09-04 Samuel M Smith: blindate now raises ValueError when it gets sn < 1. Fixed unit tests. Added snh sn and sner properties to SerderACDC  for convenience access for registry event messages More setup detail for sedi ACDCs more work to be done
  - `feb2cb707` 2026-09-04 Evan Asakawa: add dp path support to Compactor
  - `f09d49e91` 2026-09-03 Keanu: tighten edge group and edge leaf validation
  - `c155edf34` 2026-09-03 Keanu: fix sn to num, bound and blind proof serialization, add registry validation to regeventing
  - `85fc3616f` 2026-09-03 Keanu: add verifyGraphSemantics function
  - `028a20137` 2026-09-02 Keanu: add dp validation for bare offer
  - `05bad5e3e` 2026-09-02 Keanu: tighten dp field validation
  - `4b79f8f43` 2026-09-02 Daniel Hardman: Correct the SigVerifyResult docstring's key state ref
  - `06bfa0bc8` 2026-09-02 Keanu: fix dp field shape, add proof logic in verify issuer auth
  - …and 14 more

- **Untracked branch** `v1.2.14` (2026-09-02) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `v1.2.15` (2026-09-02) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `revert-1614-fix/witness-transmission-draining-v1.2.14` (2026-09-02) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### keripy-knowledge — MOVED
Feeds `raw/08-keripy-kb.md` → chapters 03, 04, 07.
Caveat: A git worktree of dhh1128/keripy on branch `knowledge`, not a separate repo. Already-distilled doctrine — its own scope tags ([protocol] vs [2.0-code]/[2.0-wire]) must survive mining, since a 2.0 code detail is not an eternal protocol truth. Re-verified 2026-06-05 against keripy 60ab9e08.

**knowledge** (standardizing, [K]) `unknown` → `9489ac9bd` — **no pin of record; treat as a full re-anchor, not a delta**

- **Untracked branch** `fix-stale-spec-refs` (2026-09-11) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `feat-di2i-direct-delegates` (2026-09-10) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `feat-indep-registry-bulk-issuance` (2026-09-10) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `main` (2026-09-09) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `feat-edge-group-traversal` (2026-09-08) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `feat-dnd-cli-visibility` (2026-09-08) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### keria — MOVED
Feeds `raw/10-keria-signify.md` → chapters 03, 06.

**main** (standardizing, [K]) `unknown` → `7e685edaa` — **no pin of record; treat as a full re-anchor, not a delta**

- **Untracked branch** `development` (2024-01-23) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### signify-ts — MOVED
Feeds `raw/10-keria-signify.md` → chapters 03, 06.

**development** (standardizing, [K]) `unknown` → `4c0072f62` — **no pin of record; treat as a full re-anchor, not a delta**

- **Untracked branch** `main` (2026-09-10) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `docs` (2023-08-23) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `reg-poc-demo` (2023-07-18) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### papers — MOVED
Feeds `raw/05-papers-priority.md`, `raw/06-papers-di-drift.md` → chapters 01, 02, 03, 04, 05, 06, 07.
Caveat: Daniel's own framing. Marker [N] is wrong here in the specification sense — these are authored positions, not normative text. Chapters cite them as the author's framing and should keep doing so; the marker field is unused for this source.

**main** (standardizing, [N]) `f94f50f` → `181569b64`
  -  16 files changed, 448 insertions(+), 222 deletions(-)
  - `181569b` 2026-09-15 Daniel Hardman: Publish Progressive Assurance (prog-a) as v0.9
  - `ab7d4d2` 2026-08-24 Daniel Hardman: spell out the CQT abbreviation in its title
  - `463f50a` 2026-08-24 Daniel Hardman: date Canonical Quoted Text to its 2.17 release
  - `3ec6424` 2026-08-20 Daniel Hardman: Revise "Where Trust Bottoms Out" to 1.8
  - `5c81915` 2026-08-20 Daniel Hardman: Revise "KERI's Strategy for Post-Quantum Security" to 1.2
  - `ccbb04b` 2026-08-14 Daniel Hardman: Revise "Building Active Discovery" to 1.1
  - `57843b6` 2026-08-14 Daniel Hardman: Publish "Building Active Discovery"; add errata to crna
  - `2f569a9` 2026-08-07 Daniel Hardman: Withdraw the PPreD paper from the archive
  - `9fec44f` 2026-08-06 Daniel Hardman: Generate amp-diff.md from upstream instead of hand-copying it
  - `465230e` 2026-07-31 Daniel Hardman: Republish m-glance v1.3 with a halved abstract
  - `bde75bb` 2026-07-31 Daniel Hardman: Republish amp-diff v1.3 and m-glance v1.2 from revised upstreams
  - `8306c68` 2026-07-30 Daniel Hardman: Guard doi/pdf_url format so the SSRN mistakes cannot recur
  - `24c18bb` 2026-07-30 Daniel Hardman: Fix SSRN DOIs; point pdf_url at our own copy, not SSRN


### keri-security-analysis — MOVED
Feeds `raw/07-security-analysis.md` → chapters 01, 02, 07.
Caveat: Carries the assumption catalog A1-A13 and the survivability framing that keri-doctrine.md's load-bearing claims 2, 3 and 5 rest on. A change here moves doctrine, not just a chapter.

**main** (standardizing, [N]) `unknown` → `149fa6c35` — **no pin of record; treat as a full re-anchor, not a delta**


### smithsamuelm-papers — MOVED
Feeds `raw/15-kram.md` → chapters 09.
Caveat: KRAM whitepaper v0.7.6. Not cloned locally; read via the GitHub API. WebOfTrust/kram's README is an earlier, shorter subset — superseded, cite the Papers version.

- `6ed1ceff4` 2026-03-06 Samuel M Smith: Merge remote-tracking branch 'origin/master'
- `67550b477` 2026-03-06 Samuel M Smith: updated KRAM spec to clarify that we leave the partially signed database entries in place until prune time

### keripy-discussions — MOVED
Feeds `raw/15-kram.md`, `raw/16-presentation-registries.md`, `raw/08-keripy-kb.md` → chapters 07, 08, 09, 10.
Caveat: The most doctrinally live source in the corpus and the one least visible to any local check. Sam edits posts in place — #1095 and #1613 both show "last edited" — so a quote can drift with no commit anywhere. Snapshotting (refresh/snapshot-discussions.py) is what makes those quotes re-verifiable. Watch BOTH vocabularies for a topic: "presentation registry" misses #1095, which invents the idea under the name "issuee usage registry".

- [#1627](https://github.com/WebOfTrust/keripy/discussions/1627) ACDC Presentation Architectures — SmithSamuelM, 2026-09-11, edited 2026-09-11 ⭐primary
- [#1613](https://github.com/WebOfTrust/keripy/discussions/1613) Authentication Factors in IPEX — SmithSamuelM, 2026-09-02, edited 2026-09-02 ⭐primary

### keripy-prs — MOVED
Caveat: Merged PRs are the tier-movement signal for [P] → [K]. They feed triage rather than a note of their own; the note that moves is whichever one carries the design they implement.

- [#1677](https://github.com/WebOfTrust/keripy/pull/1677) fix(setup): allow Python 3.14 patch releases below 3.14.7 — jaelliot, 2026-09-11
- [#1675](https://github.com/WebOfTrust/keripy/pull/1675) upgraded to version 2.1.0.dev1 — SmithSamuelM, 2026-09-10
- [#1674](https://github.com/WebOfTrust/keripy/pull/1674) Add direct KEL anchoring for truthy ax exchanges — KeaxD, 2026-09-11
- [#1672](https://github.com/WebOfTrust/keripy/pull/1672) SEDI example Added schema checks and ACDC creation to example for Identity Assurance Receipt Example — SmithSamuelM, 2026-09-07
- [#1670](https://github.com/WebOfTrust/keripy/pull/1670) Work  on SEDI examples and some convenience updates to SerderACDC as a result — SmithSamuelM, 2026-09-04
- [#1668](https://github.com/WebOfTrust/keripy/pull/1668) Add disclosure path support to Compactor — evanja57, 2026-09-14
- [#1662](https://github.com/WebOfTrust/keripy/pull/1662) KRAM: pin partial-multisig key state to the last establishment event — dhh1128, 2026-09-04
- [#1660](https://github.com/WebOfTrust/keripy/pull/1660) Correct KLI challenge file and mailbox request paths — kentbull, 2026-09-02
- [#1659](https://github.com/WebOfTrust/keripy/pull/1659) Bump KERIpy version to 1.2.14 — kentbull, 2026-09-02
- [#1658](https://github.com/WebOfTrust/keripy/pull/1658) KRAM: decide tsg currency against last establishment event, not last event — dhh1128, 2026-09-04
- [#1657](https://github.com/WebOfTrust/keripy/pull/1657) Fix messenger idle accounting — kentbull, 2026-09-02
- [#1655](https://github.com/WebOfTrust/keripy/pull/1655) Avoid scheduling messengers for completed receipts — kentbull, 2026-09-02
- [#1653](https://github.com/WebOfTrust/keripy/pull/1653) Fix #1654: Admit TCP stream payloads — kentbull, 2026-09-02
- [#1651](https://github.com/WebOfTrust/keripy/pull/1651) fix: resolve WitnessPublisher lifecycle bugs (#1652) — kentbull, 2026-09-02
- [#1650](https://github.com/WebOfTrust/keripy/pull/1650) fix: read witness AIDs from config mapping — kentbull, 2026-09-02
- [#1649](https://github.com/WebOfTrust/keripy/pull/1649) Revert "fix: make witness transmission teardown deterministic" — kentbull, 2026-09-02
- [#1648](https://github.com/WebOfTrust/keripy/pull/1648) Revert "Close direct connections without Reactants immediately" — kentbull, 2026-09-02
- [#1647](https://github.com/WebOfTrust/keripy/pull/1647) Revert "Use gleif_hio 0.6.20rc2 on v1.2.14" — kentbull, 2026-09-02
- [#1644](https://github.com/WebOfTrust/keripy/pull/1644) Add durable IPEX stores — evanja57, 2026-09-08
- [#1643](https://github.com/WebOfTrust/keripy/pull/1643) Add single-DAG IPEX nesting, origin walk, and node verification — KeaxD, 2026-09-08
- [#1640](https://github.com/WebOfTrust/keripy/pull/1640) Preserve non-Ed25519 key algorithm across rotations — dhh1128, 2026-09-01
- [#1637](https://github.com/WebOfTrust/keripy/pull/1637) Split local TEL eventing into regeventing.py — KeaxD, 2026-09-01
- [#1577](https://github.com/WebOfTrust/keripy/pull/1577) Add the ward-presents guardianship worked example (sibling to #1530) — dhh1128, 2026-09-04
- [#1561](https://github.com/WebOfTrust/keripy/pull/1561) Adopt the settled `dp` disclosure-paths construct in the IPEX examples — dhh1128, 2026-09-09
- [#1530](https://github.com/WebOfTrust/keripy/pull/1530) Add SEDI guardianship represented-presentation worked example — dhh1128, 2026-09-08

## Quote freshness

1435 live / 994 missing of 2429 quotes checked, of which **0 are new** since the baseline in `refresh/freshness-baseline.json`. The standing backlog is a known quantity and mixes three classes — illustrative quotes that were never citations, sources with no local checkout, and real drift nobody has re-anchored. The new ones are the signal: a source moved under a citation since last month.
