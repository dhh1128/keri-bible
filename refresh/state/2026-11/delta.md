# Refresh delta — 2026-11-03

Checks run: monthly. Previous run: 2026-10.

## Sources

### keri-spec — quiet
Feeds `raw/01-keri-spec.md` → chapters 01, 02, 03, 04, 06, 07, 09.
Caveat: Both lines mined 2026-09-15 and the note now carries its own pins. The branches have DIVERGED — neither commit is an ancestor of the other — so a citation here must name its branch. Note also that spec-head.md reads "Specification Status: v1.1" on BOTH branches, so this corpus's [spec]/[spec-next] split tracks the git line, not the document's own version label.

**main** (standardizing, [spec]) `fbdd4a615` → `fbdd4a615`

**v1.1** (forward, [spec-next]) `3753f3797` → `3753f3797`


### cesr-spec — quiet
Feeds `raw/02-cesr-spec.md` → chapters 04, 07.
Caveat: The previous pin d35125e is UNREACHABLE from every ref in the repo — `git branch -a --contains` returns nothing — so the 2026-07-17 citations rested on a commit that no longer exists on any branch. Both lines re-mined 2026-09-15. A pin that cannot be resolved is worse than no pin, because it reads as provenance; check reachability when recording one.

**main** (standardizing, [spec]) `bad6edd84` → `bad6edd84`

**v1.1** (forward, [spec-next]) `65fd7518b` → `65fd7518b`


### acdc-spec — quiet
Feeds `raw/03-acdc-spec.md` → chapters 05, 07, 08, 10.
Caveat: Fully re-mined 2026-09-15 on both lines; the 2026-09-01 partial re-anchor is superseded. f0bd097de is the long form of the old f0bd097 pin — main has not moved since 2026-08-28 — while v1.1 is ahead by 346 insertions / 145 deletions in spec-body.md.

**main** (standardizing, [spec]) `f0bd097de` → `f0bd097de`

**v1.1** (forward, [spec-next]) `2362e48a1` → `2362e48a1`


### dossier-spec — MOVED
Feeds `raw/04-dossier-spec.md` → chapters 05, 06, 08.

**main** (standardizing, [spec]) `3ff1b3202` → `6fcf84127`
  -  4 files changed, 213 insertions(+), 10 deletions(-)
  - `6d3bcc7` 2026-10-13 Daniel Hardman: Point the graph-root rule at the ACDC single-origin-node requirement
  - `8e92520` 2026-09-24 Daniel Hardman: Rewrite the serving section around three named times
  - `11ea842` 2026-09-23 Daniel Hardman: Point verification steps 1 and 7 at the served stream
  - `a1fa69c` 2026-09-23 Daniel Hardman: Say what a citation serves, and what a served snapshot can prove
  - `599a607` 2026-09-24 Daniel Hardman: Require CESR for packages, and make the policy state a reference-time rule
  - `6cc1c99` 2026-09-24 Daniel Hardman: Restate the graph-root rule so it does not read as a ban on cycles
  - `14401dd` 2026-09-15 Daniel Hardman: Wire the submission profile to the constructs it depends on
  - `813c8d5` 2026-09-15 Daniel Hardman: Distinguish declaring a schema is a dossier from recognizing one
  - `e7fe8b8` 2026-09-15 Daniel Hardman: Describe presentation as a self-contained package
  - `769544c` 2026-09-15 Daniel Hardman: Say how a dossier binds the authority it was issued under
  - `177796c` 2026-09-15 Daniel Hardman: Require the dossier to be the unique root of its presentation
  - `88a660f` 2026-09-15 Daniel Hardman: Define three verification outcomes and the policy that decides them
  - `9bdc415` 2026-09-15 Daniel Hardman: Profile regulatory filing as the Attested Submission Dossier
  - `f747799` 2026-09-15 Daniel Hardman: Note the case where the verifier is also the root of trust
  - `ae2066a` 2026-09-15 Daniel Hardman: Let a dossier attest to its own negative space
  - `bc244a1` 2026-09-15 Daniel Hardman: Make the verification algorithm check artifact digests
  - `a545902` 2026-09-15 Daniel Hardman: Require a filename on wrappers that carry an xSAID


### keripy-code — MOVED
Feeds `raw/09-keripy-code.md`, `raw/15-kram.md`, `raw/16-presentation-registries.md`, `raw/17-spac-tsp-privacy.md`, `raw/18-infrastructure-ops.md`, `raw/19-authorization-and-agents.md`, `raw/21-sam-rulings.md` → chapters 03, 04, 05, 08, 09, 10, 11, 12, 13.
Caveat: Mined 2026-10-03 at 80f77b73b, PARTIALLY, and each note's header says which parts: raw/09 read acdc/ipexing.py and vdr/verifying.py in full, counting.py/structing.py/exchanging.py in part, and only the cited passages of coring.py/eventing.py/parsing.py; vdr/eventing.py and app/habbing.py were NOT re-read. raw/16 read the presentation-registry paths of ipexing.py and regeventing.py; raw/15 read only the changed hunks of kraming.py and Baser.clean(). Claims outside those regions keep their older stamps (b8f60166b or 3a8e01ae). Version line still 2.1.0-dev1. KERIA consumes keripy 1.2.x (keri==1.2.14), not this line — see raw/10 §11a. raw/17 (spac/, app/forwarding.py, app/keeping.py, peer/exchanging.py, core/counting.py) and raw/18 (app/agenting.py, app/indirecting.py) cite the files they read at 927c0cb87, which is ahead of last_mined; those readings cover only the files named.

**main** (standardizing, [code]) `80f77b73b` → `94f5423a3`
  -  25 files changed, 3333 insertions(+), 728 deletions(-)
  - `0d43a6828` 2026-10-30 Evan Asakawa: docstring cleanup
  - `c98015569` 2026-10-30 Evan Asakawa: Exclude inactive endpoints from sender routing
  - `e00d66a48` 2026-10-29 Keanu: add SAID-only Offer for IPEX
  - `bd5a0bb7a` 2026-10-27 Daniel Hardman: Add Parser.parseOneBare, which raises instead of logging (#1718)
  - `a77e1b0e7` 2026-10-26 Keanu: keep presentation registry semantics to a
  - `c72d648bc` 2026-10-26 Keanu: fix registry check for linked registries during issuance:
  - `3c11a4215` 2026-10-26 Keanu: simplify registry check
  - `1f1dd54c0` 2026-10-23 Keanu: fix circular check for registry
  - `1a072b61d` 2026-10-23 Keanu: document full disclosure offer, add sscs for auth instead of always signing outer ipex msg
  - `89d950824` 2026-10-23 Keanu: fix selective disclosure for Aggregate
  - `8a7f33e0c` 2026-10-22 Keanu: add grantors check and fix the signature requirement
  - `ff324474d` 2026-10-21 Keanu: fix proxy grant
  - `84d4529ee` 2026-10-20 Keanu: fix rotation invalidate seal, remove duplicate validation
  - `abbfb3e42` 2026-10-19 Keanu: add type check for empty u field
  - `3f99a83d0` 2026-10-16 Keanu: check for no proofs in offer
  - `999d226d5` 2026-10-15 Kent Bull: Fix introduction receipt lookup for the target peer
  - `b0a1471a7` 2026-10-14 Daniel Hardman: Record a disclosed node's registry state on the v2 IPEX path instead of judging it
  - `81337f18d` 2026-10-14 Keanu: add offer to grant validation
  - `dfe59ba11` 2026-10-14 Daniel Hardman: Drop two private ledger marks from edge-operator comments
  - `ee7c4d4d2` 2026-10-14 Daniel Hardman: docs(kering): MisdigestError on a KEL is not permanent; test the recovery site
  - …and 40 more

- **Untracked branch** `v1.2.15` (2026-10-14) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### keripy-knowledge — MOVED
Feeds `raw/08-keripy-kb.md` → chapters 03, 04, 07.
Caveat: A git worktree of dhh1128/keripy on branch `knowledge`, not a separate repo. Already-distilled doctrine — its own scope tags ([protocol] vs [2.0-code]/[2.0-wire]) must survive mining, since a 2.0 code detail is not an eternal protocol truth. Re-mined 2026-09-15 at 9489ac9bd, whose tip is dated 2026-07-02. The previously recorded mining date of 2026-06-05 cannot have been right; raw/08 records why.

**knowledge** (standardizing, [code]) `9489ac9bd` → `9489ac9bd`

- **Untracked branch** `feat-edge-operators` (2026-10-30) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `feat-edge-operators-next` (2026-10-14) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `feat-di2i-direct-delegates` (2026-10-13) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `contributing-naming` (2026-10-05) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### keria — quiet
Feeds `raw/10-keria-signify.md` → chapters 03, 06.
Caveat: First anchoring, 2026-09-15; the pin was `unknown` before. Upstream renamed `development` to `main`, which is why a bare `git fetch upstream` failed here until the refspec was made explicit.

**main** (standardizing, [code]) `928ce26a4` → `928ce26a4`


### signify-ts — MOVED
Feeds `raw/10-keria-signify.md` → chapters 03, 06.
Caveat: RETARGETED 2026-09-15, development -> main, by hand after the refresh flagged it. `development` is a real branch and genuinely the head of that name, but it has not moved since 2024-04-12; the project develops on `main` (ffba8406e, 2026-09-10). A pin on a dormant branch is the failure this manifest exists to prevent, wearing a valid commit hash. ffba8406e was SPOT-CHECKED, not fully re-read — raw/10 says which claims that covers. Note also that the CESR post-quantum and stream-parser work is NOT upstream: those commits live only on feat/cesr-pq-codes and feat/cesr-stream-parser* in Daniel's fork.

**main** (standardizing, [code]) `5a174b545` → `6e07dc926`
  -  3 files changed, 844 insertions(+), 2 deletions(-)
  - `52534a9` 2026-09-05 Daniel Hardman: feat(codes): add the CESR 1.1 post-quantum primitive codes
  - `44d2801` 2026-10-12 Daniel Hardman: docs(parsing): map ParseErrorCode onto keripy's extraction errors
  - `3d7825f` 2026-10-12 Daniel Hardman: refactor(parsing): split CesrMessage into body and attachments
  - `5bb2e55` 2026-10-12 Daniel Hardman: refactor(parsing): name versions as keripy does: smell, Smellage, pvrsn, gvrsn
  - `10e8849` 2026-10-12 Daniel Hardman: fix(parsing): take the version string only from the message's start
  - `405da39` 2026-10-12 Daniel Hardman: fix(parsing): read v1 version digits as hex
  - `43c6172` 2026-10-12 Daniel Hardman: feat(parsing): carry the full CESR genus version, minor included
  - `eba4a1e` 2026-09-05 Daniel Hardman: fix(parsing): read `s` as a sequence number only under KERI
  - `cde22de` 2026-07-21 Daniel Hardman: feat(parsing): frame CESR 2.0 (v2) streams via genus dispatch
  - `16747fe` 2026-09-03 Daniel Hardman: fix(parsing): reject variable-size primitive codes by VALUE, not by type
  - `8344d5d` 2026-09-03 Daniel Hardman: fix(parsing): bounds-check every declared length; incomplete is recoverable
  - `7f7c541` 2026-07-21 Daniel Hardman: feat(parsing): add a CESR v1 stream parser


### papers — quiet
Feeds `raw/05-papers-priority.md`, `raw/06-papers-di-drift.md`, `raw/19-authorization-and-agents.md` → chapters 01, 02, 03, 04, 05, 06, 07.
Caveat: Daniel's own framing. Marker [spec] is wrong here in the specification sense — these are authored positions, not normative text. Chapters cite them as the author's framing and should keep doing so; the marker field is unused for this source.

**main** (standardizing, [spec]) `68a5e2f76` → `68a5e2f76`


### keri-security-analysis — quiet
Feeds `raw/07-security-analysis.md` → chapters 01, 02, 07.
Caveat: Carries the assumption catalog A1-A13 and the survivability framing that keri-doctrine.md's load-bearing claims 2, 3 and 5 rest on. A change here moves doctrine, not just a chapter. The `unknown` pin was RESOLVED rather than re-mined on 2026-09-15: the repo has exactly one commit, 149fa6c35 (2026-04-23), so the content read on 2026-07-17 is necessarily that commit. last_mined keeps the original reading date because no re-reading happened.

**main** (standardizing, [spec]) `149fa6c35` → `149fa6c35`


### smithsamuelm-papers — quiet
Feeds `raw/15-kram.md`, `raw/17-spac-tsp-privacy.md`, `raw/18-infrastructure-ops.md`, `raw/19-authorization-and-agents.md`, `raw/20-identity-theory-reputation-sedi.md` → chapters 01, 02, 05, 06, 07, 08, 09, 11, 12, 13, 14.
Caveat: Sam Smith's whitepapers and decks: the author's positions, never normative, all [proposal]; several are co-authored (raw/20 §0.4). last_mined b47f21597 covers the files raw/17-20 read. kram.md is the exception: raw/15 read it at 67550b477 (2026-09-15), kram.md changes after that (8 insertions, 4 deletions by b47f21597), and raw/15 is not re-read against the change. WebOfTrust/kram's README is an earlier, shorter subset of kram.md; cite the Papers version. PDFs are read as `pdftotext -layout` renders them, so cite a page or slide rather than a line, and expect the extractor to split a sentence or drop fi/ff ligatures. keridemlia.pdf has a broken text layer, so raw/18 quotes it from OCR and freshness cannot match those quotes. The open-reputation papers are read for their headers only, so treat them as unread. UniversalIdentifierTheory.pdf and IdentifierTheory_web.pdf are the same blob. SPAC_Message.md's version string (0.5.3) does not track its content; cite by commit. Revocation.md states a TEL transfer event in the present tense that is in neither ACDC branch. SPAC_Strawman, TSPSlides20230208 and SustainablePrivacySlides are superseded by the decks watched here and are not watched. ManyCubed.md, KERI_AlphaOmega and the DAD architecture deck (raw/19) and KERI_PAC_Theorem (raw/17) are read in part, for lineage or for named pages, and are watched because chapters 12 and 13 quote them.

**master** (standardizing, [proposal]) `b47f21597` → `b47f21597`


### tsp-spec — MOVED
Feeds `raw/17-spac-tsp-privacy.md` → chapters 04, 06, 07, 12.
Caveat: Trust Spanning Protocol, Experimental Implementor's Draft Rev 3 with Errata (2026-09-30), wire version 0.2. [spec] means present in the line ToIP is standardizing, and that line calls itself experimental. Only spec/spec.md is rendered (specs.json markdown_paths); the other spec/*.md files are template residue. The test-vector appendix is not mined.

**main** (standardizing, [spec]) `5599b4556` → `ccda6b331`
  -  1 file changed, 269 insertions(+), 239 deletions(-)
  - `57c18be` 2026-10-21 Wenjing Chu: update test vectors
  - `9cc6bf3` 2026-10-21 Wenjing Chu: minor text revision
  - `55a79eb` 2026-10-21 Wenjing Chu: Update to version 1.0. Make VID_sndr non-optional for hpke-base.
  - `65be672` 2026-10-08 Wenjing Chu: Clarify appraisal requirements citing standards

- **Untracked branch** `rev3-work` (2026-10-21) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### did-webs-spec — quiet
Feeds `raw/20-identity-theory-reputation-sedi.md` → chapters 01, 06, 14.
Caveat: ToIP KSWG did:webs method specification, v0.10.3 at this pin. It is on its own standards track, separate from the KERI suite lines the [spec] marker names, so its text carries [proposal] here. raw/20 mines it for its framing only: last_mined covers header.md and the body.md passages raw/20 cites, and the delegation, versionId, BADA and multisig rules are unread. The local clone also has a `fork` remote (dhh1128); `origin` is the trustoverip repo.

**main** (standardizing, [proposal]) `2d84ef2b0` → `2d84ef2b0`


### kf-witness-hk — MOVED
Feeds `raw/18-infrastructure-ops.md` → chapters 11.
Caveat: Vendor code donated by healthKERI. [code] holds only for what raw/18 read in src/; README claims are [practice]. At this pin it bundles a mailbox with each witness (raw/18 §9.3).

**main** (standardizing, [code]) `39e1c3fc7` → `48bb46a24`
  -  1 file changed, 18 insertions(+)
  - `f4b4729` 2026-10-13 arilieb: Support for multisig TOTP.


### kf-watcher-hk — quiet
Feeds `raw/18-infrastructure-ops.md` → chapters 11.
Caveat: raw/18 §7.3 finds no watcher-to-watcher sharing at this pin, by a negative search; re-check it whenever the pin moves.

**main** (standardizing, [code]) `9be717f8a` → `9be717f8a`


### kf-boot — MOVED
Feeds `raw/18-infrastructure-ops.md` → chapters 11.
Caveat: Its product rules (1-of-1 or 3-of-4 witnesses, one hosted watcher) are vendor policy, not doctrine.

**main** (standardizing, [practice]) `14c8f616e` → `ab0e3c296`
  -  2 files changed, 23 insertions(+), 22 deletions(-)
  - `e44948c` 2026-09-18 Evan Asakawa: Lock development and CI dependencies with uv


### kf-observer — MOVED
Feeds `raw/18-infrastructure-ops.md`, `raw/14-kericonf-2026.md` → chapters 10, 11.
Caveat: Created October 2026 and moving fast. raw/18 reads the README, not the code, so last_mined covers README.md only. It is not the older keri-foundation/observer repo, which is a placeholder; raw/14 §5's "placeholder" status refers to that one.

**main** (standardizing, [practice]) `d6368aef9` → `f7d7a8fd2`
  -  5 files changed, 299 insertions(+), 161 deletions(-)
  - `68e35f2` 2026-10-19 Jay-Alexander Elliot: feat(observer): introduce remote signer KEL history via PUT
  - `9b9334b` 2026-10-19 Jay-Alexander Elliot: fix(observer): handle malformed responses and query sequence numbers
  - `e4a611c` 2026-10-19 Jay-Alexander Elliot: fix(observer): recover from HTTP client setup failures
  - `873dd35` 2026-10-12 Jay-Alexander Elliot: fix(http): simplify cooperative observer requests
  - `6fc5a85` 2026-10-09 Jay-Alexander Elliot: test: cover bounded witness fallback
  - `07bbe78` 2026-10-09 Jay-Alexander Elliot: fix(observer): preserve TEL history and cooperative pulls

- **Untracked branch** `observer-replay-fixes` (2026-10-30) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### kf-registrar — MOVED
Feeds `raw/18-infrastructure-ops.md`, `raw/14-kericonf-2026.md` → chapters 10, 11.
Caveat: Created October 2026 and moving fast. raw/18 reads the README, not the code, so last_mined covers README.md only. It is not the older keri-foundation/registrar repo, which is a placeholder; raw/14 §5's "placeholder" status refers to that one.

**main** (standardizing, [practice]) `bf14eac4d` → `32dcbd712`
  -  1 file changed, 129 insertions(+), 20 deletions(-)
  - `4af546a` 2026-10-13 Jay-Alexander Elliot: fix: preserve independent TEL submissions and repair replay heads
  - `0e7e206` 2026-10-09 Jay-Alexander Elliot: style: format TEL integrity changes
  - `a31cb8f` 2026-10-09 Jay-Alexander Elliot: fix(registrar): preserve TEL history and pending recovery

- **Untracked branch** `observer-introductions` (2026-10-30) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### keripy-discussions — MOVED
Feeds `raw/15-kram.md`, `raw/16-presentation-registries.md`, `raw/08-keripy-kb.md`, `raw/21-sam-rulings.md` → chapters 03, 05, 06, 07, 08, 09, 10, 12, 13, 14.
Caveat: The most doctrinally live source in the corpus and the one least visible to any local check. Sam edits posts in place — #1095 and #1613 both show "last edited" — so a quote can drift with no commit anywhere. Snapshotting (refresh/snapshot-discussions.py) is what makes those quotes re-verifiable. Watch BOTH vocabularies for a topic: "presentation registry" misses #1095, which invents the idea under the name "issuee usage registry". #1515, #1550, #1566, #1570, #1573, #1574 and #1598 carry delegation, registry and bulk-issuance rulings (raw/21), and the #1512 body is stale against its own later comments (raw/21 R-027).

- [#1740](https://github.com/WebOfTrust/keripy/discussions/1740) Auxiliary Messages for IPEX with Blindable State Registries — SmithSamuelM, 2026-11-01, edited 2026-10-30 ⭐primary

### keripy-prs — MOVED
Caveat: Merged PRs are the signal that a [proposal] became [code]. They feed triage rather than a note of their own; the note that moves is whichever one carries the design they implement.

- [#1741](https://github.com/WebOfTrust/keripy/pull/1741) Exclude inactive endpoints from sender routing — evanja57, 2026-10-30
- [#1735](https://github.com/WebOfTrust/keripy/pull/1735) Add SAID-only Offer option for IPEX — KeaxD, 2026-10-30
- [#1734](https://github.com/WebOfTrust/keripy/pull/1734) Fix IPEX proxy grants using presentation registries — KeaxD, 2026-10-26
- [#1733](https://github.com/WebOfTrust/keripy/pull/1733) Preserve IPEX source seal validity across key rotations — KeaxD, 2026-10-20
- [#1729](https://github.com/WebOfTrust/keripy/pull/1729) Bump multidict to 6.9.1 — evanja57, 2026-10-19
- [#1721](https://github.com/WebOfTrust/keripy/pull/1721) Fix introduction receipt lookup for the target peer — kentbull, 2026-10-26
- [#1719](https://github.com/WebOfTrust/keripy/pull/1719) Bind Grant to accepted Offer commitments — KeaxD, 2026-10-19
- [#1718](https://github.com/WebOfTrust/keripy/pull/1718) Add Parser.parseOneBare, which raises instead of logging — dhh1128, 2026-10-27
- [#1715](https://github.com/WebOfTrust/keripy/pull/1715) feat(kever): raise MisdigestError for a broken KEL prior-event digest — dhh1128, 2026-10-14
- [#1714](https://github.com/WebOfTrust/keripy/pull/1714) fixed typo for Guy IAR — SmithSamuelM, 2026-10-11
- [#1713](https://github.com/WebOfTrust/keripy/pull/1713) Harden ACDC schema validation and add missing-schema escrow — KeaxD, 2026-10-13
- [#1712](https://github.com/WebOfTrust/keripy/pull/1712) removed primary field from guardianship credential — SmithSamuelM, 2026-10-06
- [#1711](https://github.com/WebOfTrust/keripy/pull/1711) Tel handling for registrar service — ryan-hansen, 2026-10-06
- [#1710](https://github.com/WebOfTrust/keripy/pull/1710) added image edge to bespoke schema — SmithSamuelM, 2026-10-06
- [#1709](https://github.com/WebOfTrust/keripy/pull/1709) Added schema and example for High Resolution Image Proof biometric SEDI ACDC — SmithSamuelM, 2026-10-06
- [#1708](https://github.com/WebOfTrust/keripy/pull/1708) Bespoke Presentation ACDC examples that show how to create single DAG presentation to include multiple SEDI ACDCs — SmithSamuelM, 2026-10-06
- [#1707](https://github.com/WebOfTrust/keripy/pull/1707) Working SEDI Guardianship related credential examples.  Also example using new 'I1i' 'Di1I' operator — SmithSamuelM, 2026-10-05
- [#1706](https://github.com/WebOfTrust/keripy/pull/1706) Contributing: point at ref/naming.md and ref/ErrorHandling.md — dhh1128, 2026-10-05
- [#1704](https://github.com/WebOfTrust/keripy/pull/1704) Error handling doc — ryan-hansen, 2026-10-05
- [#1702](https://github.com/WebOfTrust/keripy/pull/1702) Preserve group membership and member linkage across reload — kentbull, 2026-10-06
- [#1701](https://github.com/WebOfTrust/keripy/pull/1701) Preserve group membership and member linkage across reload — kentbull, 2026-10-14
- [#1698](https://github.com/WebOfTrust/keripy/pull/1698) Add dp validation for Grants — KeaxD, 2026-10-08
- [#1688](https://github.com/WebOfTrust/keripy/pull/1688) improve input validation and harden some code paths affected by input — dhh1128, 2026-10-08
- [#1681](https://github.com/WebOfTrust/keripy/pull/1681) Make the Edge section rules agree across both verification paths — dhh1128, 2026-10-30

### keripy-issues — MOVED
Feeds `raw/21-sam-rulings.md` → chapters 03, 04, 05, 08, 09.
Caveat: Sam's rulings in issue and pull-request comment threads, which neither keripy-discussions nor keripy-prs (merged-PR titles) captures. A thread is flagged when an `involves:` search finds him in it; whether GitHub counts a PR review comment as involvement is unverified. Rulings reverse within days (raw/21 §11), so a scan reads the whole thread, not the first reply. Invisible to freshness.py.

- [#1681](https://github.com/WebOfTrust/keripy/pull/1681) Make the Edge section rules agree across both verification paths — dhh1128, 2026-10-30 ⭐primary
- [#1718](https://github.com/WebOfTrust/keripy/pull/1718) Add Parser.parseOneBare, which raises instead of logging — dhh1128, 2026-10-27 ⭐primary
- [#1732](https://github.com/WebOfTrust/keripy/pull/1732) Fix persisted signer lookup after restart — jaelliot, 2026-10-20 ⭐primary
- [#1132](https://github.com/WebOfTrust/keripy/pull/1132) Update python-app-ci.yml  brew install libsodium — SmithSamuelM, 2026-10-15 ⭐primary
- [#1131](https://github.com/WebOfTrust/keripy/pull/1131) Update python-app-ci.yml changed to macos-latest — SmithSamuelM, 2026-10-15 ⭐primary
- [#1138](https://github.com/WebOfTrust/keripy/pull/1138) Update python-app-ci.yml added package find for libsodium — SmithSamuelM, 2026-10-15 ⭐primary
- [#1028](https://github.com/WebOfTrust/keripy/pull/1028) Update python-app-ci.yml — SmithSamuelM, 2026-10-15 ⭐primary
- [#1685](https://github.com/WebOfTrust/keripy/pull/1685) let witnesses serve some declared metadata to aid discovery — dhh1128, 2026-11-03
- [#1744](https://github.com/WebOfTrust/keripy/pull/1744) Fix: Use XIP messages to open IPEX transactions — KeaxD, 2026-11-02
- [#1743](https://github.com/WebOfTrust/keripy/issues/1743) CLI preserves `-` in passcodes at keystore creation but strips it on reopen — sovrel, 2026-11-02
- [#1742](https://github.com/WebOfTrust/keripy/issues/1742) Refresh and harden the published `weboftrust/keri` image — sovrel, 2026-11-02
- [#1638](https://github.com/WebOfTrust/keripy/pull/1638) Close direct connections without Reactants immediately — kentbull, 2026-11-01
- [#1124](https://github.com/WebOfTrust/keripy/pull/1124) test: fix the flakiness of kli tests by reloading parser context — kentbull, 2026-11-01
- [#1701](https://github.com/WebOfTrust/keripy/pull/1701) Preserve group membership and member linkage across reload — kentbull, 2026-11-01
- [#1121](https://github.com/WebOfTrust/keripy/pull/1121) fix: allow tests to use temp=True properly for Configer — kentbull, 2026-11-01
- [#1125](https://github.com/WebOfTrust/keripy/pull/1125) test: fix the flakiness of kli tests by reloading parser context — kentbull, 2026-11-01
- [#984](https://github.com/WebOfTrust/keripy/pull/984) fix: lmdb.MapFullError: mdb_txn_commit: MDB_MAP_FULL on Mailboxer — kentbull, 2026-11-01
- [#1115](https://github.com/WebOfTrust/keripy/pull/1115) test: fix the flakiness of kli tests by reloading parser context — kentbull, 2026-11-01
- [#1741](https://github.com/WebOfTrust/keripy/pull/1741) Exclude inactive endpoints from sender routing — evanja57, 2026-10-30
- [#1735](https://github.com/WebOfTrust/keripy/pull/1735) Add SAID-only Offer option for IPEX — KeaxD, 2026-10-30
- [#1737](https://github.com/WebOfTrust/keripy/pull/1737) Treat accepted delegated rotations as duplicate events (v1.2.15) — kentbull, 2026-10-30
- [#1738](https://github.com/WebOfTrust/keripy/pull/1738) Treat accepted delegated rotations as duplicate events (v1.3.6) — kentbull, 2026-10-30
- [#1739](https://github.com/WebOfTrust/keripy/pull/1739) Treat accepted delegated rotations as duplicate events — kentbull, 2026-10-30
- [#1736](https://github.com/WebOfTrust/keripy/issues/1736) Replaying the latest accepted delegated rotation incorrectly enters recovery validation — kentbull, 2026-10-30
- [#1734](https://github.com/WebOfTrust/keripy/pull/1734) Fix IPEX proxy grants using presentation registries — KeaxD, 2026-10-26
- [#1724](https://github.com/WebOfTrust/keripy/issues/1724) introduce() reverses event-owner and receiptor identities in receipt lookups — kentbull, 2026-10-26
- [#1723](https://github.com/WebOfTrust/keripy/issues/1723) introduce() crashes for transferable destinations: db.vrc does not exist — kentbull, 2026-10-26
- [#1721](https://github.com/WebOfTrust/keripy/pull/1721) Fix introduction receipt lookup for the target peer — kentbull, 2026-10-26
- [#1702](https://github.com/WebOfTrust/keripy/pull/1702) Preserve group membership and member linkage across reload — kentbull, 2026-10-25
- [#1733](https://github.com/WebOfTrust/keripy/pull/1733) Preserve IPEX source seal validity across key rotations — KeaxD, 2026-10-20
- [#1719](https://github.com/WebOfTrust/keripy/pull/1719) Bind Grant to accepted Offer commitments — KeaxD, 2026-10-19
- [#1727](https://github.com/WebOfTrust/keripy/pull/1727) fix(receipting): consume completed witness escrow cues — jaelliot, 2026-10-19
- [#1731](https://github.com/WebOfTrust/keripy/issues/1731) Deferred: consume completed Counselor and Anchorer witness cues — jaelliot, 2026-10-19
- [#1729](https://github.com/WebOfTrust/keripy/pull/1729) Bump multidict to 6.9.1 — evanja57, 2026-10-19
- [#1730](https://github.com/WebOfTrust/keripy/issues/1730) Verifier.processCredential accepts a credential whose issuer does not control its registry — dhh1128, 2026-10-16
- [#1395](https://github.com/WebOfTrust/keripy/pull/1395) Mailbox impl — kentbull, 2026-10-16
- [#1728](https://github.com/WebOfTrust/keripy/pull/1728) fix(cli): handle aggregate issuance timestamps — jaelliot, 2026-10-16
- [#1725](https://github.com/WebOfTrust/keripy/pull/1725) Fix introduction receipt identities on v1.2.15 — kentbull, 2026-10-15
- [#1726](https://github.com/WebOfTrust/keripy/pull/1726) Fix introduction receipt identities on v1.3.6 — kentbull, 2026-10-15
- [#1154](https://github.com/WebOfTrust/keripy/pull/1154) V1.2.7 runner — m00sey, 2026-10-15
- …and 11 more, none of them by a primary author

### spec-issues-prs — MOVED
Feeds `raw/21-sam-rulings.md` → chapters 03, 04, 05, 08.
Caveat: Editor rulings that forecast spec text: ACDC #205 (default operator), #204 (bulk issuance normative), #200 (bulk B derivation, landed), #191 (unique entropy, landed in v1.1); CESR #165 (PQ codes, landed in v1.1), #175 (Ed448 seed, open). A ruling here is [proposal] until the text is in a branch at a named commit; raw/21 §12 lists the ones that have not landed. The spec repos' discussions carry no Sam rulings, which is why they have no source of their own.

- [#327](https://github.com/trustoverip/kswg-keri-specification/issues/327) is out-of-order escrow valid? — dhh1128, 2026-11-03 ⭐primary
- [#168](https://github.com/trustoverip/kswg-cesr-specification/pull/168) fix: rapid scroll bug fixed by v1.6.21 of Spec Up T — kentbull, 2026-11-01 ⭐primary
- [#175](https://github.com/trustoverip/kswg-cesr-specification/issues/175) tweak Ed448 code? — dhh1128, 2026-10-21 ⭐primary
- [#326](https://github.com/trustoverip/kswg-keri-specification/issues/326) Errata: examples that contradict the specification — mitfik, 2026-10-22
- [#325](https://github.com/trustoverip/kswg-keri-specification/issues/325) `/loc/scheme` example is signed by the wrong AID — mitfik, 2026-10-22
- [#324](https://github.com/trustoverip/kswg-keri-specification/issues/324) End-role values are not enumerated — mitfik, 2026-10-22
- [#323](https://github.com/trustoverip/kswg-keri-specification/issues/323) Key state notice (`/ksn`) format is unspecified — mitfik, 2026-10-22
- [#322](https://github.com/trustoverip/kswg-keri-specification/issues/322) Routed messages: the `i` field is missing from the field lists — mitfik, 2026-10-22
- [#321](https://github.com/trustoverip/kswg-keri-specification/issues/321) Source seal groups with more than one couple — mitfik, 2026-10-22
- [#320](https://github.com/trustoverip/kswg-keri-specification/issues/320) Backer list edge cases — mitfik, 2026-10-22
- [#319](https://github.com/trustoverip/kswg-keri-specification/issues/319) Non-transferable prefix with a non-empty next key list — mitfik, 2026-10-22
- [#318](https://github.com/trustoverip/kswg-keri-specification/issues/318) Weighted threshold validity — mitfik, 2026-10-22
- [#317](https://github.com/trustoverip/kswg-keri-specification/issues/317) Repeated keys in the key or next key digest list — mitfik, 2026-10-22
- [#316](https://github.com/trustoverip/kswg-keri-specification/issues/316) Integer threshold wording in "Pre-rotation" reads as M = N and conflicts with the M-of-N definition — mitfik, 2026-10-22
- [#196](https://github.com/trustoverip/kswg-acdc-specification/pull/196) fix: rapid scroll bug fixed by v1.6.21 of Spec Up T — kentbull, 2026-11-01
- [#186](https://github.com/trustoverip/kswg-acdc-specification/pull/186) update tswg- to kswg- — kentbull, 2026-11-01
- [#184](https://github.com/trustoverip/kswg-cesr-specification/pull/184) Fix errata in the code tables — mitfik, 2026-10-21
- [#183](https://github.com/trustoverip/kswg-cesr-specification/pull/183) Describe count code sizes as quadlets/triplets throughout — mitfik, 2026-10-21
- [#182](https://github.com/trustoverip/kswg-cesr-specification/issues/182) Define what the index and ondex of an indexed signature refer to, and the ondex of current-only codes — mitfik, 2026-10-21
- [#181](https://github.com/trustoverip/kswg-cesr-specification/issues/181) `-U##` "Last event seal source singles `aid+dig`" describes two values for a single — mitfik, 2026-10-21
- [#180](https://github.com/trustoverip/kswg-cesr-specification/issues/180) `-N##` / `--N#####` mean different things in the spec and in keripy — mitfik, 2026-10-21
- [#179](https://github.com/trustoverip/kswg-cesr-specification/issues/179) Indexed signature codes for ECDSA secp256r1 (P-256) are missing — mitfik, 2026-10-21

## Quote freshness

4120 live / 1302 missing of 5422 quotes checked, of which **900 are new** since the baseline in `refresh/freshness-baseline.json`. The standing backlog is a known quantity and mixes three classes — illustrative quotes that were never citations, sources with no local checkout, and real drift nobody has re-anchored. The new ones are the signal: a source moved under a citation since last month.

- [01-foundations-and-worldview.md] can validate the other's key state and securely attribute (authenticate) any signed statements or any sealed issuances of data
- [01-foundations-and-worldview.md] There is a saying in crypto. Too much agility is a bad thing. There is a goldilocks amount of agility.
- [01-foundations-and-worldview.md] in production since December 2022, when the first global-scale systems went to production
- [01-foundations-and-worldview.md] re-created centralization one level up while losing time, trust-chain, and key-history fidelity
- [02-security-model-and-threat-posture.md] If our business grows, we will eventually be hacked.
- [02-security-model-and-threat-posture.md] Global consistency may only matter after A and B need to interact not before.
- [02-security-model-and-threat-posture.md] to not inform the caller why a given message sent to the service failed
- [02-security-model-and-threat-posture.md] In my mind what makes a watcher, juror, or judge 'super' is the scope of the KELs it is watching therefore we could have super watchers or super jurors or super judges.
- [02-security-model-and-threat-posture.md] a vLEI Super Watcher would have the scope of all AIDs in that ecosystem.
- [02-security-model-and-threat-posture.md] doesn't require trusting any authority's interpretation -- only the mathematics of the signatures.
- [02-security-model-and-threat-posture.md] The worst a dishonest watcher can do is stay silent about duplicity it has seen -- a risk addressed by running your own watcher or consulting multiple independent ones.
- [02-security-model-and-threat-posture.md] witnesses are being used as ersatz watchers in the wild, but witnesses cannot be watchers, and delegation is where this difference is most pronounced.
- [02-security-model-and-threat-posture.md] An event should not be Seeable by a second party unless a watcher can see it, not if a witness can see it.
- [02-security-model-and-threat-posture.md] implementations that do not use watchers cannot get it right. This includes the GLEIF ecosystem in general.
- [03-key-management-and-identifier-lifecycle.md] from the event body itself.
- [03-key-management-and-identifier-lifecycle.md] MUST have the same value and same derivation code
- [03-key-management-and-identifier-lifecycle.md] persist bindings across rotation,
- [03-key-management-and-identifier-lifecycle.md] an indirect signature that persists across key-state change
- [03-key-management-and-identifier-lifecycle.md] An attacker holding only current signing keys cannot rotate -- they do not know the pre-images.
- [03-key-management-and-identifier-lifecycle.md] Second index looks up prior-next digest, first index the exposed key, verify digest, then verify signature.
- [03-key-management-and-identifier-lifecycle.md] A rotation's current key list MUST be satisfiable w.r.t. BOTH prior-next and current thresholds.
- [03-key-management-and-identifier-lifecycle.md] provisional/custodial/escrow control authority.
- [03-key-management-and-identifier-lifecycle.md] revoke custodian's signing authority unilaterally.
- [03-key-management-and-identifier-lifecycle.md] majority of Founders OR supermajority of Investors,
- [03-key-management-and-identifier-lifecycle.md] Yeah, putting DID in a plain, non-delegated ICP, as an example, was an oversight.
- [03-key-management-and-identifier-lifecycle.md] THE DID sits in a Delegatee Inception event.
- [03-key-management-and-identifier-lifecycle.md] Delegated AIDs should work without there being an ACDC.
- [03-key-management-and-identifier-lifecycle.md] Because the custodian is a different controller, then DID is not used.
- [03-key-management-and-identifier-lifecycle.md] Because they are the same and the controller wants the world to know they are the same, then the controller uses DID.
- [03-key-management-and-identifier-lifecycle.md] Delegation depth is controlled via config traits in the inception event.
- [03-key-management-and-identifier-lifecycle.md] This then allows reputation to be transitive across a delegation relationship.
- [03-key-management-and-identifier-lifecycle.md] What a second party does with this declaration of controller equivalence between two AIDs (delegator and delegate) is up to the second party.
- [03-key-management-and-identifier-lifecycle.md] There is no code support yet for
- [03-key-management-and-identifier-lifecycle.md] because DID enforcement comes at the EGF level AFAIK
- [03-key-management-and-identifier-lifecycle.md] will be dropped and hence never be seen by anyone anywhere.
- [03-key-management-and-identifier-lifecycle.md] recon found no call to `Tever.verifyAnchor` here -- anchor validation appears to happen only in `Tevery` when a TEL event is received, not when a credential + proof is verified.
- [03-key-management-and-identifier-lifecycle.md] All client tasks/calls are signed 'at the edge', not in the hosted KERIA instance.
- [03-key-management-and-identifier-lifecycle.md] a remote cloud agent that never has access to the decryption keys,
- [03-key-management-and-identifier-lifecycle.md] asymmetric-by-role but symmetric-in-mechanism: client signs every request with the Client AID; agent signs every response with the Agent AID.
- [03-key-management-and-identifier-lifecycle.md] To provide post-quantum secure passcode recovery, a passcode recovery must be accompanied by partial rotation of the Client AID.
