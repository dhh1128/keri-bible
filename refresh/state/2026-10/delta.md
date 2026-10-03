# Refresh delta — 2026-10-03

Tiers scanned: cold, hot, warm. Previous run: 2026-09.

## Sources

### keri-spec — quiet
Feeds `raw/01-keri-spec.md` → chapters 01, 02, 03, 04, 06, 07, 09.
Caveat: Both lines mined 2026-09-15 and the note now carries its own pins. The branches have DIVERGED — neither commit is an ancestor of the other — so a citation here must name its branch. Note also that spec-head.md reads "Specification Status: v1.1" on BOTH branches, so this corpus's [N]/[N1.1] split tracks the git line, not the document's own version label.

**main** (standardizing, [N]) `fbdd4a615` → `fbdd4a615`

**v1.1** (forward, [N1.1]) `3753f3797` → `3753f3797`


### cesr-spec — MOVED
Feeds `raw/02-cesr-spec.md` → chapters 04, 07.
Caveat: The previous pin d35125e is UNREACHABLE from every ref in the repo — `git branch -a --contains` returns nothing — so the 2026-07-17 citations rested on a commit that no longer exists on any branch. Both lines re-mined 2026-09-15. A pin that cannot be resolved is worse than no pin, because it reads as provenance; check reachability when recording one.

**main** (standardizing, [N]) `bad6edd84` → `bad6edd84`

**v1.1** (forward, [N1.1]) `65fd7518b` → `65fd7518b`

- **Untracked branch** `revert-165-pq` (2026-09-22) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### acdc-spec — quiet
Feeds `raw/03-acdc-spec.md` → chapters 05, 07, 08, 10.
Caveat: Fully re-mined 2026-09-15 on both lines; the 2026-09-01 partial re-anchor is superseded. f0bd097de is the long form of the old f0bd097 pin — main has not moved since 2026-08-28 — while v1.1 is ahead by 346 insertions / 145 deletions in spec-body.md.

**main** (standardizing, [N]) `f0bd097de` → `f0bd097de`

**v1.1** (forward, [N1.1]) `2362e48a1` → `2362e48a1`


### dossier-spec — quiet
Feeds `raw/04-dossier-spec.md` → chapters 05, 06, 08.

**main** (standardizing, [N]) `b9227753c` → `3ff1b3202`


### keripy-code — MOVED
Feeds `raw/09-keripy-code.md`, `raw/15-kram.md`, `raw/16-presentation-registries.md` → chapters 03, 04, 05, 08, 09, 10.
Caveat: Mined 2026-09-15 at b8f60166b, but PARTIALLY, and raw/09 says which parts: vdr/verifying.py, acdc/ipexing.py, core/mapping.py and core/kraming.py were re-read at that commit; core/coring.py, core/eventing.py, core/counting.py and vdr/eventing.py were NOT, and the claims resting on them still stand at 3a8e01ae (2026-07-17) with line hints valid only there. The version also moved: every [K] claim written before this pass was tagged against 2.0.0-dev6, and the line is now 2.1.0-dev1.

**main** (standardizing, [K]) `b8f60166b` → `80f77b73b`
  -  25 files changed, 1339 insertions(+), 696 deletions(-)
  - `b7c170f93` 2026-09-25 Keanu: remove grantor requisite
  - `a71ea5f35` 2026-09-22 Keanu: adapt unary op for test_sedi examples, revert issuerStates and presentationStates
  - `b10b3e4e5` 2026-09-21 Daniel Hardman: Fix dead KEL likely-duplicitous escrow (escrowLDEvent AttributeError)
  - `d9ba3d9da` 2026-09-11 Daniel Hardman: Cite the ACDC spec by section rather than by line number
  - `790797bcd` 2026-09-21 Keanu: add multiply endorse support, add presentation registry support
  - `56c43fd2b` 2026-09-17 Evan Asakawa: Rebuild KRAM cache policy after database clean
  - `32effb27b` 2026-09-16 Evan Asakawa: clarify mailbox forwarding versions and framing
  - `ced845e91` 2026-09-14 Evan Asakawa: fix V2 mailbox forwarding
  - `6f5912186` 2026-09-16 Samuel M Smith: added CESR streamable attachments
  - `606b7092e` 2026-09-15 Samuel M Smith: added sealing interaction events to guy and gal for SEDI example
  - `87ba6a56d` 2026-09-15 Evan Asakawa: preserve KRAM caches during database clean
  - `e6a038586` 2026-08-04 Daniel Hardman: Render bulk-issuance derivation-path indices in hex, not decimal
  - `da82a6422` 2026-09-15 Samuel M Smith: updated test_sedi example to use SealNonce
  - `d8bb23308` 2026-09-14 Samuel M Smith: changed v2 -N code freed up from deprecating TransReceiptIdxSigGroup for NonceSealSingles
  - `e24ade8c7` 2026-09-14 Samuel M Smith: removed TransReceiptIdxSigGroups -D from v1 count code tables
  - `9762d6bb4` 2026-09-14 Samuel M Smith: retire use of TransReceiptIdxSigGroups group code
  - `a4d69a028` 2026-09-14 Daniel Hardman: Make the revocation path aggregate-aware when resolving the issuee
  - `bb74f3995` 2026-09-14 Daniel Hardman: Make the grant path aggregate-aware when resolving the issuee
  - `4d5535717` 2026-09-14 Samuel M Smith: Changed cast type of SealKind structor d field to be Noncer not Diger
  - `8a4f3f0c4` 2026-09-14 Samuel M Smith: changed TDCS to be Noncer from Diger to support other types of "digests" as generated salty nonces etc for different derivations not simply for content addresses
  - …and 1 more

- **Untracked branch** `webbaser` (2026-09-16) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### keripy-knowledge — MOVED
Feeds `raw/08-keripy-kb.md` → chapters 03, 04, 07.
Caveat: A git worktree of dhh1128/keripy on branch `knowledge`, not a separate repo. Already-distilled doctrine — its own scope tags ([protocol] vs [2.0-code]/[2.0-wire]) must survive mining, since a 2.0 code detail is not an eternal protocol truth. Re-mined 2026-09-15 at 9489ac9bd, whose tip is dated 2026-07-02. The previously recorded mining date of 2026-06-05 cannot have been right; raw/08 records why.

**knowledge** (standardizing, [K]) `9489ac9bd` → `9489ac9bd`

- **Untracked branch** `feat-indep-registry-bulk-issuance` (2026-09-23) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `patch-1` (2026-09-21) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `fix-stale-spec-refs` (2026-09-21) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `feat-edge-operators-status-axis` (2026-09-16) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### keria — MOVED
Feeds `raw/10-keria-signify.md` → chapters 03, 06.
Caveat: First anchoring, 2026-09-15; the pin was `unknown` before. Upstream renamed `development` to `main`, which is why a bare `git fetch upstream` failed here until the refspec was made explicit.

**main** (standardizing, [K]) `7e685edaa` → `928ce26a4`
  -  6 files changed, 338 insertions(+), 57 deletions(-)
  - `2703b32` 2026-09-29 Kent Bull: Prepare KERIA 0.4.1 release notes and publishing metadata
  - `06ca59b` 2026-09-21 Kent Bull: Remove unnecessary Anchorer local default
  - `73fb151` 2026-09-17 Kent Bull: clean up agenting tocks tests
  - `f6b4bb0` 2026-09-15 Kent Bull: feat: configure KERIA Agent tocks with legacy compatibility
  - `8945173` 2026-09-14 Kent Bull: build: upgrade KERIpy to the published 1.2.14 release


### signify-ts — MOVED
Feeds `raw/10-keria-signify.md` → chapters 03, 06.
Caveat: RETARGETED 2026-09-15, development -> main, by hand after the refresh flagged it. `development` is a real branch and genuinely the head of that name, but it has not moved since 2024-04-12; the project develops on `main` (ffba8406e, 2026-09-10). A pin on a dormant branch is the failure this manifest exists to prevent, wearing a valid commit hash. ffba8406e was SPOT-CHECKED, not fully re-read — raw/10 says which claims that covers. Note also that the CESR post-quantum and stream-parser work is NOT upstream: those commits live only on feat/cesr-pq-codes and feat/cesr-stream-parser* in Daniel's fork.

**main** (standardizing, [K]) `ffba8406e` → `5a174b545`
  -  1 file changed, 1 insertion(+), 4 deletions(-)
  - `5a174b5` 2026-09-16 Patrick Vu: fix: parse seal sequence number as hex in messagize (#417)


### papers — MOVED
Feeds `raw/05-papers-priority.md`, `raw/06-papers-di-drift.md` → chapters 01, 02, 03, 04, 05, 06, 07.
Caveat: Daniel's own framing. Marker [N] is wrong here in the specification sense — these are authored positions, not normative text. Chapters cite them as the author's framing and should keep doing so; the marker field is unused for this source.

**main** (standardizing, [N]) `181569b64` → `68a5e2f76`
  -  4 files changed, 44 insertions(+), 40 deletions(-)
  - `68a5e2f` 2026-09-28 Daniel Hardman: Revise "Why Anchored Signatures?" to 1.1
  - `bc4a743` 2026-09-28 Daniel Hardman: Fix typo in was.md: verballing -> verbally
  - `4eb495c` 2026-09-22 Daniel Hardman: Cite Apple's MTC PQC announcement in wtbo, acdc-and-mtc, x509-prob


### keri-security-analysis — quiet
Feeds `raw/07-security-analysis.md` → chapters 01, 02, 07.
Caveat: Carries the assumption catalog A1-A13 and the survivability framing that keri-doctrine.md's load-bearing claims 2, 3 and 5 rest on. A change here moves doctrine, not just a chapter. The `unknown` pin was RESOLVED rather than re-mined on 2026-09-15: the repo has exactly one commit, 149fa6c35 (2026-04-23), so the content read on 2026-07-17 is necessarily that commit. last_mined keeps the original reading date because no re-reading happened.

**main** (standardizing, [N]) `149fa6c35` → `149fa6c35`


### smithsamuelm-papers — quiet
Feeds `raw/15-kram.md` → chapters 09.
Caveat: KRAM whitepaper v0.7.6. Not cloned locally; read via the GitHub API. WebOfTrust/kram's README is an earlier, shorter subset — superseded, cite the Papers version.


### keripy-discussions — MOVED
Feeds `raw/15-kram.md`, `raw/16-presentation-registries.md`, `raw/08-keripy-kb.md` → chapters 07, 08, 09, 10.
Caveat: The most doctrinally live source in the corpus and the one least visible to any local check. Sam edits posts in place — #1095 and #1613 both show "last edited" — so a quote can drift with no commit anywhere. Snapshotting (refresh/snapshot-discussions.py) is what makes those quotes re-verifiable. Watch BOTH vocabularies for a topic: "presentation registry" misses #1095, which invents the idea under the name "issuee usage registry".

- [#1515](https://github.com/WebOfTrust/keripy/discussions/1515) New Unary Edge Operators to Support SEDI — SmithSamuelM, 2026-10-01, edited 2026-07-21 ⭐primary
- [#1098](https://github.com/WebOfTrust/keripy/discussions/1098) ACDC with Static Age Predicate Proof SMT — SmithSamuelM, 2026-09-26, edited 2026-09-26 ⭐primary

### keripy-prs — MOVED
Caveat: Merged PRs are the tier-movement signal for [P] → [K]. They feed triage rather than a note of their own; the note that moves is whichever one carries the design they implement.

- [#1705](https://github.com/WebOfTrust/keripy/pull/1705) Flesh out examples more fully. Revise core schema to inlcude optional guaridan edges for wards — SmithSamuelM, 2026-10-02
- [#1700](https://github.com/WebOfTrust/keripy/pull/1700) Added working test example for AID Replacement SEDI ACDC — SmithSamuelM, 2026-09-30
- [#1697](https://github.com/WebOfTrust/keripy/pull/1697) Removed population of presentation registry for linked ACDCs in SEDI examples. Fixed some typos. — SmithSamuelM, 2026-09-29
- [#1696](https://github.com/WebOfTrust/keripy/pull/1696) Added SEDI ACDCs:  Age, Delegation Chain Organizational Unit and Issuing Agent — SmithSamuelM, 2026-09-28
- [#1695](https://github.com/WebOfTrust/keripy/pull/1695) Add tests for SEDI credentials through IPEX — KeaxD, 2026-09-30
- [#1694](https://github.com/WebOfTrust/keripy/pull/1694) Fixed typos, bugs in SEDI examples.  Added oneOf so attribute field schema so can partial disclose — SmithSamuelM, 2026-09-24
- [#1693](https://github.com/WebOfTrust/keripy/pull/1693) Add multiply endorsed IPEX Grants and presentation registry authentication — KeaxD, 2026-09-28
- [#1692](https://github.com/WebOfTrust/keripy/pull/1692) Fix dead KEL likely-duplicitous escrow (escrowLDEvent AttributeError) — dhh1128, 2026-09-25
- [#1691](https://github.com/WebOfTrust/keripy/pull/1691) Suggest security policy with reporting guidelines — dhh1128, 2026-09-22
- [#1689](https://github.com/WebOfTrust/keripy/pull/1689) added support for issuee presentation registries to SEDI ACDCs — SmithSamuelM, 2026-09-18
- [#1687](https://github.com/WebOfTrust/keripy/pull/1687) working example of residence ACDCs for guy and gal — SmithSamuelM, 2026-09-18
- [#1686](https://github.com/WebOfTrust/keripy/pull/1686) Sedi test example now has support for the Core SEDI ACDC for both Guy and Gal (parents) — SmithSamuelM, 2026-09-18
- [#1684](https://github.com/WebOfTrust/keripy/pull/1684) Preserve KRAM caches during database clean — evanja57, 2026-09-22
- [#1683](https://github.com/WebOfTrust/keripy/pull/1683) Finished refactor to remove now reduandant TransReceiptIdxSigGroup usage.  Replace with NonceSealSingles — SmithSamuelM, 2026-09-15
- [#1680](https://github.com/WebOfTrust/keripy/pull/1680) fix V2 mailbox forwarding — evanja57, 2026-09-16
- [#1678](https://github.com/WebOfTrust/keripy/pull/1678) Improve aggregate support when resolving an ACDC's issuee — dhh1128, 2026-09-16
- [#1676](https://github.com/WebOfTrust/keripy/pull/1676) Cite the ACDC spec by section rather than by line number — dhh1128, 2026-09-21
- [#1673](https://github.com/WebOfTrust/keripy/pull/1673) Update webbaser from main for Python 3.14 and Pyodide 314 — evanja57, 2026-09-16
- [#1576](https://github.com/WebOfTrust/keripy/pull/1576) add the independent-registry bulk-issuance worked examples: co-created and pre-created (SEDI) — dhh1128, 2026-09-25

### conf26-subtitles — quiet
Feeds `raw/14-kericonf-2026.md` → chapters 06, 08, 10.
Caveat: Edited auto-captions of spoken talks. A WEAK provenance class: near-wording only, never exact. See raw/14 §0 before any quote reaches a chapter. A conference corpus is near-static, hence cold.


### bakobo-schema — MOVED
Feeds `raw/11-credentials.md` → chapters 05, 06.

**main** (standardizing, [K]) `unknown` → `cfcbdcc7a` — **no pin of record; treat as a full re-anchor, not a delta**

- **Untracked branch** `sedi-repin-guardians` (2026-10-02) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `gcd-targets` (2026-10-02) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `tick` (2026-10-02) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `sedi-guardian-no-gcd` (2026-08-05) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### public-schema — MOVED
Feeds `raw/11-credentials.md` → chapters 05, 06.

**main** (standardizing, [K]) `unknown` → `95a07e544` — **no pin of record; treat as a full re-anchor, not a delta**

- **Untracked branch** `brand-owner` (2024-12-30) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### origin-platform — MOVED
Feeds `raw/12-origin-security.md` → chapters 02, 06.
Caveat: Provenant client work, read locally and never quoted outward from here. Doctrine-in-practice: useful as evidence of how the worldview survives a shipping deployment, not as normative text.

**main** (standardizing, [K]) `unknown` → `cb758b1b5` — **no pin of record; treat as a full re-anchor, not a delta**

- **Untracked branch** `chore/rename-review-panel-to-origin-review-panel` (2026-07-11) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `tick` (2026-06-17) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `feat-archiving-github-repos` (2026-06-10) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.
- **Untracked branch** `fix/review-panel-verify-null-crash` (2026-06-08) is newer than anything tracked here. Propose adding it in the PR body; do not retarget automatically.

### keri-one — quiet
Feeds `raw/13-keri-one-web.md` → chapters 01, 06.
Caveat: Thin original content on the homepage and About page; the rest is an outbound-link directory. Detected by content hash, since there is no commit to diff. Mined 2026-07-17.

- https://keri.one/ content hash None → 7cae5f92ed96de10
- https://keri.one/keri-resources/ content hash None → e20b997ea8d4f1f6
- https://keri.one/131-2/ content hash None → 9ee9070c39f93630

## Quote freshness

1929 live / 1026 missing of 2955 quotes checked, of which **11 are new** since the baseline in `refresh/freshness-baseline.json`. The standing backlog is a known quantity and mixes three classes — illustrative quotes that were never citations, sources with no local checkout, and real drift nobody has re-anchored. The new ones are the signal: a source moved under a citation since last month.

- [02-security-model-and-threat-posture.md] names scope, not a feature set, and it attaches to all three roles.** Where this corpus has said
- [02-security-model-and-threat-posture.md] Philip Feairheller concurred and supplied the concrete case:
- [02-security-model-and-threat-posture.md] It depends on observer presence, diligence, information overlap, and time. (`background.md` §6.3) The spec ties this to the asymmetry it creates for the defender:
- [05-acdc-and-verifiable-data.md] The club's accepted shape and the holder's issued presentation are one schema viewed from two sides
- [07-shibboleths-and-anti-patterns.md] The observer layer is KEL discovery / caching, and a 'super watcher' is a bigger cache.
- [07-shibboleths-and-anti-patterns.md] a convenient way to centralize how state is *queried*
- [07-shibboleths-and-anti-patterns.md] The watcher, judge, and jurors each play distinct important roles in the KERI security posture of a validator[;] they are not merely discovery mechanisms for KELs[,] so having amnesia about why their roles are distinct is going to be problematic
- [07-shibboleths-and-anti-patterns.md] ** → Discovery is OOBIs, untrusted by design; watcher/juror/judge are three security roles held apart, and
- [11-credentials.md] The club's accepted shape and the holder's issued presentation are **one schema viewed from two sides**
- [keri-doctrine.md] The observer layer is KEL discovery / caching; a 'super watcher' is a bigger cache.
- [keri-doctrine.md] not merely discovery mechanisms for KELs.
