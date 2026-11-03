# Refresh report — 2026-11

Run directory `refresh/state/2026-11`. Phases 2–5 run by the model, unattended; phase 1 (detect, 2026-11-03 05:23 UTC) and phase 6 (commit, PR) are the shell script's. Monthly sources only: November is not a quarterly month, so the quarterly sources (kf-profile, keri-foundation-web, conf26-subtitles, keri-foundation-recordings, bakobo-schema, public-schema, origin-platform, keri-one, utah-sedi-statute) were not scanned. Written incrementally: a section still marked *(pending)* did not happen, and the triage that drove the run is in the appendix.

## 1. Sources advanced

`last_scanned` advanced to the 2026-11-03 head for all 21 monthly git sources, and `since` to 2026-11-03 for the four GitHub sources. `last_mined` advanced only where a note was re-read against the new commit; for the partial readings the manifest caveat now says which files the pin covers.

| Source | `last_scanned` | `last_mined` | Reading |
|---|---|---|---|
| dossier-spec | `3ff1b3202` → `6fcf84127` | `b9227753c` → `6fcf84127` | raw/04: body and head in full; schemas and six of 29 glossary files at cited lines only |
| keripy-code | `80f77b73b` → `94f5423a3` | `80f77b73b` → `94f5423a3`, partial | raw/09: chaining.py, verifying.py, scheming.py in full, ipexing.py in full except two stretches, changed regions elsewhere; coring/indexing/helping/serdering not re-read. raw/16: the registry paths. raw/21: the out-of-order escrow path. raw/15 not re-read (kraming.py unchanged) |
| signify-ts | `5a174b545` → `6e07dc926` | `5a174b545` → `6e07dc926`, partial | raw/10: parsing.ts in full, matter.ts code tables, exports.ts; the rest stays at `ffba8406e`/`5a174b545` |
| tsp-spec | `5599b4556` → `ccda6b331` | `5599b4556` → `ccda6b331` | raw/17: spec.md L1–1580 in full; test vectors not mined |
| kf-witness-hk | `39e1c3fc7` → `48bb46a24` | `39e1c3fc7` → `48bb46a24` | raw/18: the one changed file read; nothing else changed |
| kf-observer | `d6368aef9` → `f7d7a8fd2` | `d6368aef9` → `f7d7a8fd2` | README.md only, as before; byte-identical |
| kf-registrar | `bf14eac4d` → `32dcbd712` | `bf14eac4d` → `32dcbd712` | README.md only, as before; byte-identical |
| kf-boot | `14c8f616e` → `ab0e3c296` | unchanged, `14c8f616e` | README install section changed; quoted lines resolve but the README was not re-read |
| keri-spec, cesr-spec, acdc-spec (both lines), keripy-knowledge, keria, papers, keri-security-analysis, smithsamuelm-papers, did-webs-spec, kf-watcher-hk | no movement | unchanged | — |
| keripy-discussions, keripy-prs, keripy-issues, spec-issues-prs | `since` → 2026-11-03 | n/a | #1740 mined into raw/16; KERI #327 and keripy #1681 into raw/21 |

`refresh/snapshot-discussions.py` took 19 snapshots with 0 drift and 0 errors. Eleven were first snapshots (#1740 and ten discussions raw/21 cites), so freshness now sees them.

## 2. Doctrinal changes

Per chapter, what a reader of the 2026-10 version would now say differently. keripy claims are at `94f5423a3` unless named.

Chapter 05, ACDC. keripy's two edge verifiers no longer "disagree on three axes". They agree on an unrecognized operator (undecidable, not malformed), on a list of operators (latest-wins among I2I/NI2I/DI2I, E1E alongside) and on an absent `o` (defaults to I2I/NI2I). They still differ on six things: a revoked far node (v1 refuses; V2 records it in `exrs.` and does not judge it), a schema pin naming the far node's own schema, inline schema-document pins, which validator, a compact Edge Section, and nesting depth (v1 stops at 8, V2 has no bound). `acdc/chaining.py` shares the verdict algebra only, so there is still no single edge layer; Sam's direction that there should be one is recorded as [proposal] (R-080). `I1I`/`DI1I` are refused by both evaluators, so Sam's SEDI fixtures using `["E1E","DI1I","NI2I"]` cannot be satisfied. keripy now validates schemas (local-only, JSON Schema 2020-12, version required, before blind issuance) and escrows exchange messages awaiting a schema. The SEDI Age finding is reversed: keripy no longer reads `A` for presentation-registry declarations, so selective disclosure of one age threshold is not blocked there, though no test exercises it. Issue #1730 is confirmed from code: the v1 verifier never compares a credential's issuer with its registry's controller. Dossier: new base SAID, `filename` on xSAID wrappers, the graph-root rule.

Chapter 08, IPEX. `dp` is enforced in keripy V2, not merely negotiated: a grant must match the agreed plan exactly, in breadth-first order, and keep the accepted Offer's promise; SAID-only Offers exist. A V2 grant containing a revoked credential is accepted, and the state is only recorded. Each node's issuer-authentication factor is one input to the edge verdict, so a node behind an OR branch the grant does not need can fail authentication without failing the grant. Seals survive key rotation; signatures do not. New [proposal] section on #1740's auxiliary `/ipex/dhke` and `/ipex/unblind` exchanges for blindable state registries, with its ordering tension (question 12): under #1740's order the `bup` follows the `grant`, which a keripy V2 verifier refuses. Dossier presentation: self-contained packages, the graph-root rule, three outcomes. IPEX V2 still has no caller in `src/keri`.

Chapter 10, presentation registries. Declarations come only from the top level of a disclosed `a`; `A` plays no part, so an undisclosed aggregate entry no longer causes a refusal (Question 10 is rewritten around what is still open: an `i`/`rd` pair in an aggregate entry silently imposes nothing). The origin of an issuance grant is exempt; an Issuer presenting its own credential to a third party is bound. Issuer-registry state is recorded in `exrs.`, never judged; the presentation-registry binding is separate and still enforced. Three refusals that no specification states, not four. Status unchanged: partly built in keripy's library, no spec text.

Chapter 03, key management. New section on out-of-order events. The spec's MUST-drop (main L1266, v1.1 L1265) turns on "at least one verifiable Controller signature", and neither branch mentions out-of-order escrow. Sam ruled on KERI #327 that a signed out-of-order event goes to escrow and only an unsigned one is dropped ([proposal]; no text has landed). keripy does exactly that ([code]: `Parser.msgProcess` drops, `Kevery.processEvent` escrows, `TimeoutOOE` bounds it).

Chapter 04, CESR. signify-ts upstream `main` frames all 33 CESR v1.1 post-quantum codes, matching `v1.1` row for row, but cannot sign or verify with any of them, and no tagged release contains them. keripy and CESR `main` have none. signify-ts's new v1/v2 stream parser is exported but not called internally. It frames an in-stream genus counter without switching tables, short of the spec's "MUST modify" (this is a reading of the code, not a run). It also no longer lifts `s`, so `sad.s` is an ACDC's schema SAID unless the caller checks `proto`. keripy has `Parser.parseOneBare`, the non-swallowing wrapper Sam asked for. The Ed448 `K` defect gains a second implementation that carries it (cesrox).

Chapter 12, confidentiality. TSP calls itself "Release 1.0", wire version 1.0 (`YTSP-BAA`), and the chapter now reads it as the editors' label with no ToIP approval recorded. Both PKAE modes are now full ESSR: `VID_sndr` MUST be in the confidential payload, and HPKE-Base adds an AAD binding on top. The NULL VID survives only in non-confidential payloads. TSP now splits verifiability into cryptographic verification and appraisal against the endpoint's own policy. That 0.2 and 1.0 do not interoperate is labelled inference.

Chapter 06, governance. The dossier spec's VALID/INVALID/INDETERMINATE outcomes, its required acceptance policy, the `authority` edge, the verifier-is-root case and the Attested Submission profile. The base SAID is `ENroDvI…`, so the three divergent dossier bases are now spec `ENroDvI…`, public-schema `EHxI61…` and bakobo `EFf_1u…` (the last two not re-verified). The parity section covers signify-ts's PQ framing and parser. §4.6 is rewritten for the `A` change.

Chapter 07, shibboleths. Created: "a validator drops any event it cannot verify yet" (4.5) and "a verifier that cannot decide has rejected" (9.6). Narrowed: the two-verifier subsection (10.5) to the six remaining differences, and its quick-reference row. The presentation-registry residual and the TSP status wording are rewritten. `dp` enforcement and signify-ts's PQ gap are added as section 12 paragraphs.

Chapter 11, infrastructure. witness-hk now encrypts the TOTP secret whole to each member key of a multi-key AID. Open question 5 gains a within-witness half: any one member key holds the whole second factor. That is labelled raw/18's reading.

`keri-doctrine.md` did not change, so no panel sync is owed. No load-bearing rule moved. Two wording questions are in section 7. The prompt's "citation-durability paragraph" no longer exists in that file: the 2026-10-15 rewrite moved pins out of it on purpose ("Pins, commit-level behavior and the state of designs still in motion live in the bible").

## 3. Marker change

No specification line moved, so nothing became standard this month and there is no `[spec-next]` → `[spec]` change.

- signify-ts PQ codes and stream parser: from absent upstream to [code] at `6e07dc926`, for framing only. The codes stay [spec-next] in CESR, and open PR #178 proposes reverting them from `v1.1`. bible/04's load-bearing-assumption claim moves from [proposal] to [code] on that evidence. The chapter verifier checked it, with one limit: it shows new parsers accept the new rows, not that old parsers reject them.
- TSP: still [spec], with "experimental" dropped from the chapter text because the spec's own status line no longer says it.
- New [proposal] entries: R-079 (KERI #327 ruling), R-080 (edge layer), #1740 (auxiliary IPEX exchanges).
- raw/18: the kf-boot README claim was relabelled from [code] to [practice], which the manifest caveat requires for README claims.
- No [proposal] → [code] upgrade for presentation registries, `exrs.` or IPEX V2. These were already [code]; what changed is what the code does.

## 4. Re-anchored only

About 30 claims in raw/09, 30 in raw/16, 60 in raw/04 (an estimate), 28 in raw/17, 6 in raw/18 and 2 in raw/10 had their line hints moved with no change to the claim. In the chapters, the synthesizers re-anchored about 30 in 05, 30 in 08, 24 in 10, 14 in 12, 12 in 07, 9 in 04, 9 in 11, 4 in 06 and 4 in 03.

freshness: 4,538 live and 1,146 missing of 5,684 quotes, against 4,120 / 1,302 of 5,422 at detect time. The baseline was refreshed with `--update-baseline`, and 933 entries healed. It now records the current 1,146 misses. Most are class 1 or 2 rather than drift: 178 rest on the missing `~/code/provenant/` checkouts (section 7), about 155 are raw/21 issue-thread quotes no source holds on disk, and the rest are web, caption, OCR and test-file quotes. Every quote the refresh added that freshness cannot see was checked by hand by the verifiers.

## 5. Reviewed and dismissed

Triage counts: 10 doctrinal, 6 corroborative, 4 marker-change candidates, 0 pre-identified re-anchor-only, and roughly 45 noise items. The noise was 10 quiet sources, kf-boot tooling, the kf-observer and kf-registrar code with unchanged READMEs, about 35 keripy PRs and issues with no doctrinal content or no Sam involvement, four 2023 CI PRs bulk-closed on 2026-10-15, three spec tooling PRs, and the mitfik errata issues. The full list is in the appendix. Items a reader might expect to have mattered:

- KERI #316–#326 and CESR #179–#184 (mitfik's errata, 2026-10-21/22): open, with no editor reply, so they are not rulings. Several name defects the bible may repeat. See section 7.
- keripy #1685 (Daniel, witness `/decl/tags`): open, with no ruling.
- keripy hardening series (Tholder caps, `b64ToInt`, Pather, `_exfil`): coring/indexing/helping were not re-read, so raw/09 makes no new claim about them.
- keripy #1741 (inactive endpoints excluded from routing) and #1721 (`introduce()` receipt lookup): raw/18 makes no claim either change touches.
- CESR #175: no new Sam text. R-020 was re-verified.

## 6. Cuts

Quotes that failed verification and were removed. In every case the claim survives on a replacement quote that was verified at the same pin, except where noted.

- raw/09 §2 (Local vs remote): "each witness only accepts local events... making the controller's signature(s) the first factor and the set of unique witness factors a secondary threshold factor". It is not verbatim; the source reads "signature (s): the first factor". It supported the claim that the witness pool acts as a threshold second factor. That claim is now unquoted in raw/09, and open question 13 names KERI spec `main` L1764 @`fbdd4a615` as the candidate citation.
- bible/05: `sad[label] = Dummy * …` @`80f77b73b` L4085 is not the code (it is `clas.Dummy`, L3899). The verbatim code replaced it.
- bible/05 and raw/09: `Schemer(raw=scraw).verify(creder.raw)` is two statements joined into one. Replaced by `schemer = Schemer(raw=scraw)` (L217).
- bible/10 and raw/16: the #1613 "Notwithstanding…" quote ran to 42 words, and its elision dropped the condition "when the Grantor of the IPEX is the Issuee". Replaced by two short verbatim fragments with the condition stated.
- bible/04: "a disciplined additive extension that old parsers reject cleanly…" is in neither the CESR spec nor the lens files. Replaced by the spec's own L618 sentence @`bad6edd84`.
- bible/06: "validity logic is EGF-dependent" is not verbatim. Replaced by the full L1112 sentence.
- bible/03: "Second index looks up prior-next digest…" is a paraphrase of KERI spec L1256. Replaced by the verbatim fragment. The landmine L15 quote was 28 words with altered punctuation, and is now trimmed to the verbatim text.
- bible/03: "An attacker holding only current signing keys cannot rotate -- they do not know the pre-images." raw/09 rewrote the passage it came from. The claim stays as an unquoted conclusion from the `exposeds` code.
- Quotes removed because the code changed rather than because they were wrong: in raw/16, bible/05, bible/06, bible/07, bible/08 and bible/10, "Every inspected aggregate entry must be a mapping.", "A verifier cannot distinguish an omitted requirement…", "Presentation anchoring is mandatory…", "Restrict default qualification…", "Default IPEX policy deliberately stops…" and "Reject any malformed, missing, or invalid presentation factor." No longer exist at `94f5423a3`; each claim was rewritten to what the code now does.
- 16 new quotes over 25 words (14 in raw/04, 2 in raw/09) were trimmed by deleting words only.

For four of the bible cuts above (05 ×2, 03 ×2), the verifier asks whether swapping in the source's real text from the same passage is acceptable, because it sits close to the "never reword" rule. Each replacement is a different, verbatim span, not an edit of the failed one.

## 7. JUDGMENT NEEDED

Errors to fix:

- `~/code/provenant/` does not exist on this box. public-schema and origin-platform cannot be read, so 178 quotes in raw/11, raw/12, bible/02 and bible/06 report missing. Both are quarterly sources and were not scheduled this month, but the checkout has to come back before January, or the job has to fail loudly. Today freshness only warns.
- freshness.py reads the local branch as well as `<remote>/<branch>`, and accepts a quote found in either. In `wot/tswg-tsp-specification`, local `main` sits at `5599b4556`, a month behind, so a quote TSP has since dropped still passes. That fails open in the case the tool exists to catch. Consider reading the local branch only when the remote ref is absent, and fast-forwarding the stale clone.
- freshness does not see keripy `tests/`, dossier `spec/dossier-spec-head.md` or `schemas/`, or signify-ts and KERIA README/docs, because `watch` excludes them, and several chapters now quote them. Proposed: add `tests` to keripy's `watch`, add `spec/dossier-spec-head.md` and `schemas` to dossier-spec's, and drop dossier-spec's dead `.ref` entry, which is gitignored.

Proposed manifest changes (reviewed fields, not applied):

- keripy-code: the untracked branch `v1.2.15` (2026-10-14). KERIA consumes keripy 1.2.x (`keri==1.2.14`), so this line, not `main`, is what KERIA deployments run. Tracking it would let the bible say what deployed KERIA does.
- keripy-knowledge: the four "untracked branches" detect lists (`feat-edge-operators`, `feat-edge-operators-next`, `feat-di2i-direct-delegates`, `contributing-naming`) are dhh1128/keripy feature branches, visible only because `keripy-knowledge` is a worktree of that fork. They are not knowledge-branch candidates. detect.py should scope its untracked-branch check for a worktree source to the source's own branch family.
- tsp-spec `rev3-work`: 0 ahead and 6 behind `main`, already merged. Nothing to track.
- kf-observer `observer-replay-fixes` and kf-registrar `observer-introductions`: newer than `main`. raw/18 reads only READMEs, so tracking them buys nothing until the code is mined.
- dossier-spec `chapters`: add 07, 13 and 14, which also cite the dossier spec.

Doctrine (`keri-doctrine.md` unchanged; both of these would need Daniel's endorsement and a panel sync):

- Rule 5 says "ESSR, standardized as TSP". TSP now calls itself Release 1.0, but no approving body or date is recorded. "specified in ToIP's TSP" claims less.
- Rule 31, last sentence. The bible/10 synthesizer proposes "Presentation registries are the mechanism for an issuee who opts in, declared by the issuer at issuance; they are a proposal in discussion, partly built in keripy's library, with no specification text." That is closer to keripy, where the Issuer's declaration triggers the check. The current sentence is not wrong.

Upstream, for Daniel to raise himself if he wants to:

- KERI #327. Sam answered the question but did not engage the proposed clarifying sentence, and the spec text on both branches still reads as MUST-drop. R-073 records that Sam will not answer AI-drafted issues, so any follow-up should be in Daniel's own words. Separately, the chapter 03 synthesizer notes that Annex A (main L1692–L3102) declares no normative status, and many of bible/03's unmarked [spec] citations sit inside it.
- keripy #1681 follow-up: Sam's "an option to verify" is ambiguous between a caller switch and making I2I optional, and the PR merged before he answered.
- keripy #1730 is confirmed from code: the v1 verifier never compares issuer with registry controller and never checks the anchoring source triple.
- #1740: under its in-band order the `bup` follows the `grant`, but a keripy V2 verifier refuses that `grant`, because the registry proof must travel on the `grant` itself. The `/ipex/unblind` case is likewise a permanent refusal in keripy, not something it waits on.
- keripy registry binding (raw/16 question 11): keripy requires the Issuee's registry binding on every presentation of a registry-backed credential, so the credential cannot be presented as third-party evidence unless the Issuee binds that grant. A Grantor-only version existed at `8a7f33e0c` and was removed at `3c11a4215`. Possibly one for Keanu.
- Dossier spec (Daniel's own) open question 8: it says ACDC "already requires" a single origin node, but that text exists only on ACDC `v1.1` (L1821, [spec-next]). Questions 9–14 list six smaller internal inconsistencies, including stale section references and an offline-VALID tension with `referenceTime`.
- mitfik's errata (KERI #316–#326, CESR #179–#184) are open and unanswered. None was checked against the bible this run. A future pass should check whether bible/03 and bible/04 repeat any of the defects they name.

Unresolved tensions and housekeeping:

- Over the 6,000-word target, all under the 7,500 lint ceiling: bible/05 ~6,850, bible/08 6,859, bible/07 6,983, bible/06 ~7,400, bible/12 6,496. bible/08's synthesizer asks whether to move the #1740 material to chapter 10 or cut elsewhere. Trimming claims whose evidence did not move was out of scope.
- The chapter verifier flagged three older items it did not change. bible/11 uses a caption ("We do four watchers… one in each region") for a deployment detail, though captions are for status and intent only. bible/05 attributes wtbo's "constraints of youth" to ACDC, where the paper says it of KERI's tooling. bible/08's Status section mixes markers placed before and after their claims.
- bible/05 rests seven coring.py/serdering.py/test_sedi.py claims on `@80f77b73b`. raw/09's own reading suggests some coring.py line numbers are stale even at that pin. coring.py was not re-read.
- raw/21: R-008, R-010, R-011 and R-070 still say "the infrastructure chapter"; only the ranking lines were updated to name bible/11.
- raw/17's "Already in the bible" and "Proposed chapter outline" sections predate bible/12 and are stale. raw/04 dates `6fcf84127` 2026-10-13 where git says 2026-10-20.
- About 20 over-25-word quotes carried over unchanged in raw/04 and raw/09. The limit has never been enforced on carry-overs. Decide whether a refresh should.
- The 900 "new misses" detect reported were mostly artifacts (appendix). With the baseline now current, next month's new-miss count should mean drift again.

## Appendix — triage

### Freshness, read before anything else

detect reported 900 new misses. That number is not a month of drift, and the report would mislead if it were taken at face value. Two causes account for nearly all of it:

- The baseline was written on 2026-10-03, and raw/19, raw/20 and raw/21 were added on 2026-10-14. Every quote in those notes that cannot be resolved from disk — raw/21's 193 come almost entirely from keripy and spec issue threads, which no source checks — is "new" only because the baseline never saw it.
- `~/code/provenant/` does not exist on this box. freshness.py warns "source not a git checkout, skipping" for `provenant/public-schema` and `provenant/origin-platform`, so every quote resting on them reports missing: 116 in raw/12, 62 in raw/11, and most of the misses in bible/06 and bible/02. That is a source that cannot be read, and it is reported as an error in section 7.

A text-based comparison against the baseline (rather than the hash keys, which changed when freshness.py's normalization changed on 2026-10-15) still finds 899 quotes missing that the baseline did not list, so the hash churn is not the explanation; the two causes above are. The actionable part is the misses in notes whose sources moved this month — raw/04 (21), raw/09 (36), raw/10 (40), raw/16 (33), raw/17 (4), raw/18 (19) — and the miners were told to resolve those.

### Classification

Doctrinal (goes to mining):

- dossier-spec `3ff1b3202` → `6fcf84127`: 17 commits by Daniel rewriting serving, verification, the graph-root rule, CESR-required packages, three verification outcomes, the Attested Submission Dossier profile, negative-space attestation. → raw/04.
- keripy-code, edge-operator reduction (#1681, merged 2026-10-30): both verification paths reduce the Edge Section through one policy-aware entry point; registry state recorded rather than judged on the v2 IPEX path (`b0a1471a7`, new `exrs.` table). → raw/09, raw/16.
- keripy-code, IPEX revisions by Keanu (#1698, #1719, #1733, #1734, #1735): `dp` validation on grants, grant bound to the accepted offer's commitments, source-seal validity across rotation, proxy grants through presentation registries, SAID-only offer, `sscs` for authentication instead of always signing the outer message, grantors check. → raw/09 (IPEX) and raw/16 (registry paths).
- keripy-code, schema validation and missing-schema escrow (#1713, `scheming.py` +492, new `emse.`/`emsd.` tables, schema validated before blind issuance). → raw/09.
- keripy-code, new `acdc/chaining.py` (267 lines). → raw/09.
- keripy discussion #1740 (Sam, 2026-10-30, edited same day): auxiliary `qry`/`rpy` sidecar exchanges `/ipex/dhke` and `/ipex/unblind` for blindable state registries, and a proposed rule that `admit` MUST NOT be sent until the registry state is verified. → raw/16; feeds bible/08 and bible/10.
- spec issue KERI #327 (Daniel, Sam answered 2026-11-03): Sam rules that an out-of-order event with at least one signature goes to out-of-order escrow and an unsigned one is dropped. → raw/21.
- keripy #1681 thread: Sam agrees edge logic belongs in its own layer and suggests staging I2I as an option to `verify`. → raw/21.
- tsp-spec `5599b4556` → `ccda6b331`: "Update to version 1.0. Make VID_sndr non-optional for hpke-base", plus appraisal requirements. The status the corpus states (Rev 3, experimental, wire 0.2) is now in question. → raw/17.
- signify-ts `5a174b545` → `6e07dc926`: CESR 1.1 post-quantum codes and the CESR v1/v2 stream parser are now on upstream `main`, which contradicts the manifest caveat that they live only in Daniel's fork. → raw/10.

Corroborative:

- keripy #1707 (Sam, merged 2026-10-05): SEDI guardianship examples "using new 'I1i' 'Di1I' operator". bible/05 says `I1I`/`DI1I` are proposed and unimplemented; the raw/09 miner checks whether `src/keri` now recognises them. → raw/09.
- keripy #1715 / `0072353ef`: a broken KEL prior-event digest now raises `MisdigestError`, documented as not permanent. → raw/09 (cheap).
- keripy #1718 `Parser.parseOneBare`. → raw/09 (cheap).
- keripy hardening series (`251fd24da`…`d5d3ea4b2`: Tholder recursion and product caps, `b64ToInt`, Pather, Matter `_exfil`, DoS caps documented as tunable). → raw/09 only where the note already makes a claim about these paths.
- kf-witness-hk `48bb46a24`: multisig TOTP — the TOTP is encrypted to each member key of a multi-key AID. raw/18 §4 carries the TOTP claim. → raw/18.
- keripy `forwarding.introduce()` receipt-lookup fix (#1721) and inactive-endpoint exclusion from sender routing (#1741). → raw/18, only if raw/18 makes a claim about either.

Marker change candidates (each to be confirmed by the miner against the code, not the PR title):

- signify-ts PQ codes and stream parser: absent upstream → `[code]` at `6e07dc926`.
- keripy registry-state handling on the v2 IPEX path: what raw/16 and bible/10 call `[code]` enforcement may have become record-not-judge.
- keripy edge operators: the "two verifiers disagree three ways" `[code]` claim may no longer hold after #1681.
- TSP: Experimental Implementor's Draft → version 1.0, if the text says so.

Re-anchor only: none identified in advance. The specification lines did not move (keri, cesr, acdc on both branches), so no `[spec-next]` → `[spec]` change is possible this month.

Noise (advances `last_scanned` only):

- keri-spec, cesr-spec, acdc-spec, keripy-knowledge, keria, papers, keri-security-analysis, smithsamuelm-papers, did-webs-spec, kf-watcher-hk: quiet.
- kf-boot `ab0e3c296`: uv lockfile, CI, install instructions. The product rules raw/18 cites are untouched.
- kf-observer `f7d7a8fd2` and kf-registrar `32dcbd712`: source and test changes only; README.md, the only file raw/18 reads for either, did not change. Reviewed, not mined.
- keripy `basing.py`, `regeventing.py`, `registraring.py`: the hunks are the new tables and schema-validation call sites already covered above.
- keripy PRs and issues with no Sam involvement and no doctrinal content: #1729 (multidict), #1714, #1712, #1710, #1709, #1708 (SEDI example schemas and fixtures by Sam, outside `src/keri`), #1706, #1704, #1702, #1701, #1688, #1711, #1727, #1728, #1731, #1736–#1739, #1742, #1743, #1744, #1723, #1724, #1725, #1726, #1154, #1395, #1638.
- keripy #1028, #1131, #1132, #1138: 2023 CI PRs by Sam, touched 2026-10-15 by a bulk close; no new content.
- keripy #1685 (Daniel, witness `/decl/tags`): open, no Sam ruling in the thread.
- keripy #1730 (Daniel): `Verifier.processCredential` accepts a credential whose issuer does not control its registry. Open, no ruling. Passed to the raw/09 miner as a negative claim to check.
- spec PRs CESR #168, ACDC #186, ACDC #196: render tooling and repo renames.
- spec errata issues by mitfik (KERI #316–#326, CESR #179–#184): open, no Sam reply. Not rulings, so not raw/21 material; listed in section 7 because several name defects the bible may repeat.
- CESR #175 (Ed448 seed): Sam's comments are from 2026-09-01 and raw/21 R-020 already carries them; touched 2026-10-21 without a ruling.

### Miner results, as they came in

raw/21 (done): R-079 (KERI #327 — a signed out-of-order key event goes to out-of-order escrow, only an unsigned one is dropped; spec text on both branches does not say this, recorded as T-13, not landed; keripy `94f5423a3` matches the ruling) and R-080 (keripy #1681 — Edge Section validation should be its own layer, staged with I2I kept in `verify()`; `[proposal]`; no separate layer exists at `94f5423a3`, the edge verdict is still computed inside `IpexHandler.verify`). R-020 re-verified at both CESR pins and gains mitfik's note that cesrox carries the 56-byte `K` defect too. R-021 notes `Parser.parseOneBare` (#1718) is the wrapper Sam asked for.

raw/04 (done): rewritten against dossier spec `6fcf84127`; body and head read in full; `last_mined` advanced. Base schema SAID now `ENroDvI_lXRUa3p1UCxU6Pxp0DWDS1yZNexCq_1TQlcj` (bible/05 L315, bible/06 L187 still give `EKuLzS…`); graph-root rule; VALID/INVALID/INDETERMINATE plus required acceptance policy; ten-step algorithm (every old step number moved); self-contained packages and served CESR streams; three named times; `authority` edge; xSAID wrappers need `filename`; schema-allowlist recognition; `attest`/`manifest` negative-space fields; verifier-is-root-of-trust; Attested Submission profile; status v0.7 Draft. The note also shed strike-throughs and dated narration that standards §3 forbids, and two misquotes were made verbatim. Open questions 8–14 added; item 8 (dossier `[spec]` text leans on ACDC `[spec-next]` single-origin-node text) is a candidate for Daniel to raise upstream.

raw/09 (done): rewritten for keripy `94f5423a3`. The two verifiers now agree on an unrecognized operator (undecidable, not malformed), on a list of operators (latest-wins among I2I/NI2I/DI2I, E1E alongside), and on an absent `o` (defaults to I2I/NI2I). They still differ on a revoked far node (v1 refuses, V2 records in `exrs.`), a schema pin naming the far node's own schema, inline schema-document pins, which validator, a compact Edge Section, and nesting depth (v1 stops at 8, V2 unbounded). `acdc/chaining.py` holds the shared three-valued verdicts and AND/OR rules, but each verifier still walks edges itself. `dp` is now enforced on grants (exact plan match, breadth-first order, must keep the accepted Offer's promise); SAID-only Offers exist. Schema validation is new: local-only, JSON Schema 2020-12, version required, before blind issuance, with a missing-schema escrow. `MisdigestError` on a broken KEL prior digest. No marker changes; IPEX V2 still has no caller in `src/keri`. I1I/DI1I still unimplemented. Issue #1730 confirmed from code. Read in full: chaining.py, verifying.py, scheming.py, ipexing.py except `apply` builder (L2306–2374) and `admit`/`spurn`/`loadHandlers` (L2775 on); changed regions of vdr/eventing.py and peer/exchanging.py; coring/indexing/helping/serdering not re-read.

raw/17 (done): TSP `ccda6b331` read in full through Security and Privacy Considerations (L1–1580); `last_mined` advanced; caveat rewritten. Status "Release 1.0" (L4), version `1.0` (L245), `YTSP-BAA` (L1130), hedged with the same file's "Latest Draft:" label, placeholder contributor list, HPKE Internet-Draft normative reference and provisional `1AAQ` code; no ToIP approval recorded. `VID_sndr` MUST be in the confidential payload for all PKAE schemes (L286, L367); NULL VID survives only in signed-only payloads. New split of verification into cryptographic verification and appraisal (L148). The miner's inference, labelled as such in the note: 0.2→1.0 is wire-breaking. `rev3-work` is 0 ahead / 6 behind main, i.e. already merged. Q11 added (who released 1.0).

raw/16 (done): keripy `94f5423a3` registry paths (ipexing.py `IpexHandler` through `verifyEvidence`, `_sign`, `grant` docstring; regeventing `vetBinds`/`present`/`vacate`/`issue`; registering, registraring, recording, `Baser.exrs`, exchanging endorser index; registry tests) and #1740 at its 2026-10-30T18:03:58Z edit. Declarations now come only from `a`; `A` is ignored, so a compact or partial `A` no longer refuses (answers bible/10 Q10). The origin of an issuance grant is exempt; linked credentials still apply. Registry-only authentication of a non-sender Issuee still holds. Issuer-registry state recorded in `exrs.`, never judged; the presentation-registry binding is separate and still enforced. #1740 concerns the Issuer's blindable state registry, not presentation registries (new §4b); nothing implements `/ipex/dhke` or `/ipex/unblind`. V2 still has no caller. Seven quotes no longer in the code were cut or replaced. freshness cannot see keripy `tests/` (watch is `src/keri`), so the miner checked test quotes by hand.

raw/18 (done, corroborative): witness-hk `48bb46a24` — full diff plus `AidCollectionEnd.on_post` in full; the only changed file, so `last_mined` advances. New [code] claim: `totps` gives a multi-key AID the TOTP secret encrypted whole to each member key; the miner labels as its own reading that this does not touch the across-witness question, and splits open question 5 in two. kf-observer and kf-registrar READMEs byte-identical, so `last_mined` (which covers README.md only) advances. kf-boot README changed in its install section; the quoted lines resolve but the README was not re-read, so `last_mined` stays. keripy files raw/18 cites are unchanged through `94f5423a3`; citations keep `927c0cb87`. No claim about #1741 routing or `introduce()`.

raw/10 (done): signify-ts `6e07dc926` (ancestor of `upstream/main`; no tag contains the PQ commit). `parsing.ts` read in full; `matter.ts` code tables and `exports.ts` diff in part; `last_mined` advanced with a caveat scoping it to those files. All 33 CESR v1.1 PQ codes framed, matching CESR `v1.1` `65fd7518b` row for row — ahead of keripy `94f5423a3` and CESR `main`, which have none. Sizes only: `VERFER_CODES` and `Signer` support no PQ algorithm. The parser sizes by code-table lookup, picks v1/v2 framing from the version string's genus version, reports but does not act on an in-stream genus counter, and no longer lifts `s`. Nothing in `src` calls it; it is only re-exported. The eight fork-only quotes were replaced. bible/04 §5.7, its fork Sources entry and "nothing shipped implements" are now wrong.

bible/10 (done): 24 keripy locators re-anchored to `94f5423a3`. Declarations come only from the top level of a disclosed `a`; compact `a` still refused; `A` plays no part (Q10 rewritten to what is still open: an `i`/`rd` pair in an aggregate entry silently imposes nothing). Issuance-grant origin exempt; linked credentials are not; an Issuer presenting its own credential to a third party is bound. §8 lists three refusals no spec states, not four. State recorded in `exrs.`, binding enforced. #1740 appears only as a vocabulary trap. No marker changes. Proposed doctrine claim 31 wording and four shibboleth candidates, below.

bible/04 (done): §5.7 now says signify-ts `main` `6e07dc926` frames all 33 PQ rows matching `v1.1` but cannot sign or verify with them, in no tagged release; keripy has none; #178 hedge kept. §5.3 cites upstream `parsing.ts`. §8 gains the two meanings of "genus": signify-ts frames an in-stream `-_AAA` counter without switching tables, short of the spec's "MUST modify" (read from code, not run). §10 cites `Parser.parseOneBare`. §12 item 11 (Ed448) gains the cesrox report; new item 12 on `sad.s`. Marker: the load-bearing-assumption claim [proposal] → [code] at signify-ts `6e07dc926`. 9 re-anchored; the fork parser quote replaced by the upstream one.

bible/05 (done): §5.1 "disagree on three axes" replaced by agreement on three shapes and six remaining differences; shared `chaining.py` is algebra only; R-080 added as [proposal]; chain revocation holds on the v1 path only; `I1I`/`DI1I` refused by both evaluators, so the SEDI fixtures' `["E1E","DI1I","NI2I"]` cannot be satisfied. New [code] paragraph on the V2 schema validator. Dossier base SAID, `filename` rule, graph-root rule (with ACDC v1.1 L1821 as [spec-next]). #1730 resolves the old L15 hypothesis. Outside its brief, and read at `94f5423a3`: §4.1 Finding 1 (selective Age disclosure blocked by `A`) was false now that `A` is not read, and was rewritten; `registraring.py` is a local manager, not a stub. ~30 re-anchored.

bible/08 (done): `dp` enforced on V2 apply/offer/agree/grant (exact match, breadth-first; v1 never mentions `dp`); new `#offer-fulfillment` (SAID-only Offers); edges share an AND/OR module and agree on three cases; a V2 grant containing a revoked credential is accepted, state only recorded in `exrs.`; each node's issuer factor is one input to the edge verdict, so a node behind an unneeded OR branch can fail authentication without failing the grant; seals survive rotation, signatures do not; declarations only from `a`; new `#dossier-graph-root`. New [proposal]: `#edge-layer` (R-080), `#aux-registry-exchanges` (#1740) with question 12 `#q-dhke-order`. ~30 re-anchored. Body 6,859 words, over the 6,000 target, under the 7,500 lint ceiling.

bible/12 (done): §10 `#tsp-hpke` — both PKAE modes are full ESSR, HPKE-Base adds an AAD sender binding; NULL VID only in non-confidential payloads. `#tsp-shape` gains the verification/appraisal split (RFC 9334, TCG-AF not read). Non-retention MUST NOT (L599) beside "not enforced by any mechanism" (L1554). §9 `YTSP-BAA`, with the 0.2/1.0 non-interop labelled as inference. Status "[spec], experimental" → "[spec]", "Release 1.0" as the editors' label with no recorded ToIP approval. 14 stamps re-anchored to `ccda6b331`. Body 6,496 words.

bible/03 (done): new `#out-of-order-escrow` in §1 — spec MUST-drop (main L1266 / v1.1 L1265) and its DDoS reason, the Verifier definition in Annex A (L1737 / L1736; normative status undeclared), no out-of-order escrow on either branch; R-079 as [proposal]; keripy [code] drops unsigned, escrows signed, times out at `TimeoutOOE`. §11 landmine L15 holds at `94f5423a3`. 4 re-anchored (KERIA 401 citation to `AuthenticationMiddleware.process_request` @`7e685edaa`; signify-ts guard to `core/authing.ts` L83 @`ffba8406e`). One quote cut: "An attacker holding only current signing keys cannot rotate -- they do not know the pre-images." (raw/09 rewrote it); the claim stays, unquoted, as a conclusion from code.

bible/11 (done): §5 `#second-factor-instances` gains two [code] quotes from `aiding.py` @`48bb46a24` (caller-supplied batch secret, L96; secret encrypted to each key "in inception key order", L53); `#second-factor-trade` adds the within-witness question (any one member key holds the whole second factor), labelled raw/18's reading. Open question 5 rewritten. R-079 does not fit the chapter. 9 locators re-anchored.

bible/06 (done): §1 three dossier verdicts (INDETERMINATE for an unevaluated Layer-2 schema) and TSP's verification/appraisal split; §2 acceptance policy, `authority` edge, new `#verifier-is-root` (Attested Submission profile, `manifest`, `withheld`); §6 base SAID `ENroDvI…` and allowlist recognition; §7 signify-ts PQ framing (no signing) and parser; §4.6 rewritten for `94f5423a3`: the aggregate no longer triggers the registry check, so an over-21 proof is not forced to disclose every threshold (heading retitled, anchor kept). 4 re-anchored. Body ~7,400 words against the 6,000 budget.

bible/07 (done): created 4.5 `#out-of-order-drop` and 9.6 `#indeterminate` with quick-reference rows; `dp` enforcement and the signify-ts PQ gap added as section 12 paragraphs, not rows; 10.5 narrowed to the six remaining verifier differences (revoked-grant case folded in); quick-reference row "the operator means X" replaced; §14 presentation-registry residual rewritten; TSP wording now "Release 1.0" @`ccda6b331`. Four quotes replaced (registry-enforcement, I2I, DI2I, `EdgeGroupOps` → `MAryReducers`). 12 re-anchored. Body 6,983 words.

raw/ verifier (done, fresh agent): 528 new quotes across the seven notes, 527 confirmed at their pins, 1 cut (raw/09, below), 16 new over-25-word quotes trimmed by deletion only (2 raw/09, 14 raw/04), 0 line hints wrong, #1740 unedited since 2026-10-30T18:03:58Z. Limits it stated: the `§heading` check confirmed file, not heading; context was read for raw/18 §4, raw/21 R-079/R-080 and raw/16's open questions only; ~86 carried quotes that merely moved were not chased. Two follow-ups applied by the orchestrator: raw/09's sentence relaying "the refresh brief" now points at raw/21 R-080's quotes; raw/18's kf-boot README claim relabelled [code] → [practice], which the manifest's own caveat requires.

### Work list

| Item | raw note | chapters |
|---|---|---|
| Edge-operator reduction, IPEX revisions, schema escrow, chaining.py, MisdigestError, parseOneBare, #1730 | raw/09 | 03, 04, 05, 08 (07 shibboleth) |
| Registry state recorded not judged, proxy grants, linked-registry check, #1740 | raw/16 | 08, 10 |
| Dossier spec rewrite | raw/04 | 05, 06, 08 |
| Sam rulings KERI #327, keripy #1681 | raw/21 | 03, 05, 08 |
| TSP 1.0 | raw/17 | 04, 06, 07, 12 |
| signify-ts PQ codes and parser upstream | raw/10 | 03, 06 (04 for the PQ codes) |
| Witness multisig TOTP; introduce() and routing fixes if cited | raw/18 | 11 |
