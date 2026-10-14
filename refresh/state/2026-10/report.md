# Bible refresh — 2026-10

Run directory `refresh/state/2026-10`. Phases 2–5 executed by the model; phase 1 (detect) and phase 6 (commit/PR) are the shell script's. Tiers scanned: hot, warm, cold (October is a cold month). Written incrementally — a section still marked *(pending)* did not happen. The triage that drove the run is in the appendix at the end.

## 1. Sources advanced

`last_scanned` advanced for every source on 2026-10-03. `last_mined` advanced only where a note was re-read against the new commit.

| Source | Line | `last_scanned` | `last_mined` | Note |
|---|---|---|---|---|
| keri-spec | main / v1.1 | `fbdd4a615` / `3753f3797` (no movement) | unchanged, 2026-09-15 | — |
| cesr-spec | main / v1.1 | `bad6edd84` / `65fd7518b` (no movement) | unchanged, 2026-09-15 | open revert PR #178 on `v1.1`, see §7 |
| acdc-spec | main / v1.1 | `f0bd097de` / `2362e48a1` (no movement) | unchanged, 2026-09-15 | — |
| dossier-spec | main | `b9227753c` → `3ff1b3202` | unchanged, `b9227753c` | build/CSS only; not re-read, so not advanced |
| keria | main | `7e685edaa` → `928ce26a4` | → `928ce26a4` (delta) | raw/10 §11; only the changed files were read, and the 2026-09 "not re-read" list still stands |
| signify-ts | main | `ffba8406e` → `5a174b545` | → `5a174b545` (delta) | raw/10 §11c; one commit, one file |
| papers | main | `181569b64` → `68a5e2f76` | → `68a5e2f76` (delta) | raw/05, raw/06; every changed hunk read, unchanged files byte-identical |
| keripy-knowledge | knowledge | `9489ac9bd` (no movement) | unchanged | — |
| keri-security-analysis | main | `149fa6c35` (no movement) | unchanged, 2026-07-17 | — |
| smithsamuelm-papers | master | `67550b477` (confirmed by API: `kram.md` last touched 2026-03-06) | unchanged | — |
| conf26-subtitles | main | `unknown` → `15f1e91a7` (head since 2026-08-23) | unchanged, `unknown` | see §7: the 2026-09-01 mining necessarily read `15f1e91a7`, but this run did not re-read it |
| keripy-code | main | `b8f60166b` → `80f77b73b` | → `80f77b73b` (**partial**) | raw/09 (ipexing.py, verifying.py in full; count-code/seal/receipt paths), raw/16 (registry paths), raw/15 (changed KRAM hunks + `Baser.clean()`). `vdr/eventing.py`, `app/habbing.py`, most of `kraming.py` NOT re-read; claims there keep older stamps. Manifest caveat rewritten to say so. |
| bakobo-schema | main | `unknown` → `cfcbdcc7a` | `8db57eb` → `cfcbdcc7a` (full re-anchor of raw/11's claims; working tree verified clean at the pin) | the old `8db57eb` pin is a **public-schema** commit, not a bakobo one — see §7 |
| public-schema | main | `unknown` → `95a07e544` | `unknown` → `95a07e544` (partial: the claims raw/11 cites; other schema files only searched) | `ovc-org-vet/` and `tn/` removed upstream; claims resting on them superseded |
| origin-platform | main | `unknown` → `cb758b1b5` | **unchanged, `unknown`** — re-read in full, but the re-anchored note is held out of the commit (§7, first item), so the committed note does not carry that reading | first pin of record is in the held-out file |
| keri-one | web | first content hashes recorded | n/a (no pin field) | raw/13 re-verified against the live pages; five quotes struck (§6) |
| keripy-discussions / keripy-prs | — | `since` → 2026-10-03 | — | — |

## 2. Doctrinal changes

Per chapter, what a reader of the 2026-09 version would now say differently. All `[K]` claims are keripy `80f77b73b` unless named; the specs did not move.

**Chapter 10 — presentation registries.** The status changes from "pre-normative, unbuilt" to "pre-normative, and partly built in keripy only." On every `/ipex/grant`, keripy's V2 IPEX module now requires each `(i, rd)` registry declared in a disclosed `a`/`A` to be Issuee-incepted and to bind that grant before the receiver's KRAM acceptance time, and refuses the grant otherwise — including when an aggregate entry is undisclosed or `a` is compact. The requirement is unconditional once an Issuer declares it, and since `b7c170f93` a registry binding authenticates the Issuee **without** the Issuee endorsing the grant, contrary to #1613's "the grant message must be endorsed by each Grantor." No foreign-registry retrieval exists, no spec text exists, and the V2 handler has no caller in `src/keri`. #1098 adds a purpose statement: unlinkable ZKPs are refused because they would defeat Issuer- and Issuee-side compromise detection.

**Chapter 09 — KRAM.** KRAM is no longer only a replay filter in keripy: it now records `rdt`, the time it accepted a complete message, and the presentation-registry check requires that record and uses it as the cutoff. `Baser.clean()` now preserves replay caches (closing a replay window a clean used to reopen) while dropping cache types and partial multisig state.

**Chapter 08 — IPEX.** `ax` on a grant can be satisfied by the sender, the origin's Issuee or Issuer, or a registry binding; `agree`/`admit` still need the sender. Multiply-endorsed grants are implemented on `grant` only, but `verify` discards the endorsement signatures — only seals count, and only toward `ax`. Every disclosed node must now pass exactly one of three Issuer-authentication checks. The two keripy verifiers disagree on edge-operator semantics in three ways. "`dp` is negotiated, not enforced" and "V2 is unwired" both re-verified true.

**Chapter 04 — CESR.** keripy retired `TransReceiptIdxSigGroups` (`-D`) from v1; transferable endorsements travel as `TransIdxSigGroups`. keripy reassigned v2 `-N` to `NonceSealSingles` while **both** CESR spec branches still define `-N` as transferable receipt quadruples — an implementation-first divergence. keripy's own parser and event serializer do not handle `-N`, but verification found that v2 `messagize` appears able to emit a `-N` attachment its parser cannot read (code reading, not run; no caller found). Typed-digest seals may now carry a nonce. The post-quantum `[N1.1]` claims gain a hedge: open PR #178 proposes reverting them from `v1.1`.

**Chapter 05 — ACDC.** The SEDI Age credential, as Sam's keripy fixtures shape it, cannot be presented selectively through keripy's IPEX: it requires `rd`, and an undisclosed aggregate element fails a registry-backed grant, so proving over-21 reveals the other thresholds. keripy reads an aggregate's issuee only from `A[1]`, which the schema does not pin. The Utah "delegation chain" is a credential chain (`I2I` edges, plain `incept`), not KERI delegation. `I1I`/`DI1I` are proposed (#1515, 2026-10-01) and unimplemented. GCD's cooperative-delegation binding is now "the exemplar", not a precondition.

**Chapter 06 — governance.** SEDI's state-issued family is now IAR/Core/Residence/Age and `sedi-id` is historical; the "stack composes cleanly" claim is hedged by the Age finding. There are now three divergent dossier bases (spec, public-schema, bakobo). Parity section gains KERIA's keripy-line pin and signify-ts's hex bug.

**Chapter 03 — key management.** KERIA runs keripy's 1.2.x line (`keri==1.2.14`), so keripy `main` behaviour is not evidence about a KERIA deployment; the September establishment-event convergence between keripy and KERIA was therefore literally independent. signify-ts's `messagize` violated the hex-sequence-number invariant until 2026-09-16.

**Chapter 07 — shibboleths.** The unlinkability tell now rests on detectability (#1098) rather than diminishing returns. New tells: "the edge operator means X" (which keripy module?), and "keripy does X, so deployments do X". The presentation-registry residual is restated as `[K]` verifier-side with no spec text.

**Chapter 02 — security.** No change to the argument. The Origin citation is relabelled as one deployment's evidence and pinned at `cb758b1b5`.

**Chapter 01** — one fidelity fix: the keri.one quote "[It's m]uch easier to secure one's own keys well…" restored to the page's wording.

**`keri-doctrine.md` — a load-bearing claim moved; a panel sync is owed.** Claim 14 said presentation registries are "opt-in, pre-normative, and unimplemented", and that keripy enforced a rule the design violates by construction. Both are now wrong for keripy: an appended, dated passage records what is built, its three boundaries (no spec text, library-only, KERIA does not run it) and that the election now happens at issuance rather than per presentation. The I2I table row is sharpened with the three-way verifier split. The citation-durability paragraphs carry the new pins and what was not re-read. **Run `./sync-reference.sh` in `~/code/wot/keri-review-panel` after merge.**

## 3. Tier movement

No specification line moved this month, so there is **no `[N1.1]` → `[N]` upgrade**: nothing became standard. Every movement below is `[P]` → `[K]` (a design reaching code) or a new `[K]`/`[P]`, and each was re-checked against code at the pin by a verifier that did not write it.

**Presentation registries: `[P]` → `[K]`, verifier-side on `/ipex/grant`, keripy `80f77b73b`. Upheld.** The design from #1095/#1613/#1618 is now partly code — and only in keripy's V2 IPEX module, which has no caller in `src/keri`. Specifically:

- Issuee control of the registry — "if controller is not None and record.issuer != controller:" (`acdc/regeventing.py:714`). (bible/10 §2)
- Every declared registry in the DAG must bind the grant — "Verify every presentation registry declared across the DAG." (`acdc/ipexing.py:609`), with `target=serder.said` per declaration (`:1532-1545`). (bible/10 §3)
- Independence from `ax`, and registry-authenticated Issuees counting as `ax` anchorers — "Restrict default qualification to sender, Issuee, or issuer." (`ipexing.py:647`). (bible/10 §6, bible/08)
- `rd`-in-`a` disambiguation in code only — "hidden issuer registry, not a presentation registry." (`ipexing.py:1419`). The spec ambiguity stays open. (bible/10 §4)
- #1618 leg 2 (registry as an authentication factor). (bible/10 §7.4)

Still `[P]`: foreign-registry retrieval, #1095's acceptance delay, a registry without a top-level `rd`, the correlation-protected bespoke origin, any tethering check, threshold-checking of non-sender endorsements.

**Multiply-endorsed grants: `[P]` → `[K]` in part.** Non-sender signatures and seal triples are accepted on `grant` only and validated after KRAM, per #1613; `verify` then discards the signatures (`_, _, extraSeals = evidence`), so only seals count, and only toward `ax`. (bible/08)

**Issuer authentication per disclosed node: new `[K]`.** Exactly one of issuer registry, issuer seal anchor, or signature under current keys. (bible/08)

**KRAM acceptance time feeding presentation validity: new `[K]`.** `rdt` (`recording.py:505`; `kraming.py:1658-1661`) consumed at `ipexing.py:1524`, `:1543`. (bible/09)

**SEDI Age not selectively presentable through keripy IPEX: new `[K]` finding.** (bible/05 §4.1, bible/06 §4) Verifier-upheld; boundary stated (no test presents Age; V2 handler unwired). A related narrowing from verification: Sam's Age schema does not itself require `E1E` — only his fixture uses it.

**`I1I` / `DI1I`: new `[P]`.** #1515, 2026-10-01; nothing in `src/keri` implements them. (bible/05, 07, 08)

**`TransReceiptIdxSigGroups` (`-D`): existing `[K]` superseded.** Retired from keripy v1; v2 `-N` reassigned to `NonceSealSingles` against both spec lines. (bible/04)

**Considered and refused:** `E1E` stays `[N1.1]` + `[K]`; the refreshed keripy comment claiming it is normative on `v1.1` was written by Daniel in `d9ba3d9da` and is not independent evidence. The marker rests on ACDC `v1.1` spec text at `2362e48a1` (L1206, L1209, L1223), re-confirmed by a verifier, and on its absence at `f0bd097de`. The CESR post-quantum `[N1.1]` markers do not move; they gain a pending-revert hedge.

## 4. Re-anchored only

- **papers** (`raw/05`, `raw/06`): every `wtbo.md` line hint is still valid at `68a5e2f76` (body edits are line-count-neutral); reference numbers shifted by one after a new `[24]`. Versions recorded: wtbo 1.9, was 1.1, x509-prob 1.4, acdc-and-mtc 1.1. The Apple-MTC sentences were added as corroboration only.
- **bakobo-schema / public-schema** (`raw/11`): a full re-anchor with no prior pin; most claims re-stamped at `cfcbdcc7a` / `95a07e544`, with supersessions where the schemas themselves changed (listed in `raw/11`'s header).
- **origin-platform** (`raw/12`): re-read in full at `cb758b1b5`; no source text disappeared since 2026-05. Only the pin, a citation-location fix, two struck unsourced expansions and a quote-free corrections list are committed; the full re-anchor is held out (§7).
- **keri.one** (`raw/13`): re-verified against the live pages; first content hashes recorded.
- **KRAM** (`raw/15`): line hints past `kraming.py:1460` drift by +2 to +5 at `80f77b73b`; flagged, not individually re-stamped.
- **keripy** (`raw/09`): §1–§3 and §4/§6b line hints remapped to `80f77b73b`.

## 5. Reviewed and dismissed

Counts by class (full list in the appendix): doctrinal 7, corroborative 5, tier-movement candidates 4, full re-anchors 4, noise across 9 sources.

Things a reader might have expected to matter:

- **dossier-spec moved** (`b9227753c` → `3ff1b3202`) — `.gitignore`, CSS and `package*.json` only. Not re-read; `last_mined` not advanced.
- **keripy escrowLDEvent fix** (#1692) — a crash fix in the likely-duplicitous escrow; the corpus describes that escrow but makes no code-level claim the fix changes.
- **keripy V2 mailbox forwarding** (#1680), **`SECURITY.md`** (#1691), **spec-citation-by-section** (#1676) — no doctrine.
- **KERIA tocks/scheduling** — when escrows are processed, not what is accepted. Recorded in `raw/10` §11b for completeness only.
- **"Challenge refactored to a digest"** (`370a656a8`) — docstrings only in `src/keri`; the challenge is a nonce seal in tests.
- **smithsamuelm-papers and conf26-subtitles** — confirmed quiet by direct GitHub API reads, so the empty delta is not a broken config.
- **`snapshot-discussions.py`**: 8 snapshots, **0 drifted**, 0 errors. #1098 and #1515 snapshotted for the first time.
- **Untracked branches** (keripy `webbaser`; Daniel's fork branches seen through keripy-knowledge; bakobo-schema `sedi-repin-guardians`, `gcd-targets`, `tick`, `sedi-guardian-no-gcd`; public-schema `brand-owner`; four origin-platform branches) — none proposed except CESR `revert-165-pq`, which is an open PR rather than a line to track (§7).

## 6. Cuts

**How verification ran.** Every quoted span in lines added this run (≈1,576) was checked mechanically against a corpus built from every pinned commit touched — including keripy `tests/`, older pins cited for removed text, both branches of each spec, the discussion snapshots, kids#1 comments and today's keri.one fetch. 276 did not match and were split across five fresh verifier agents, none of which had mined or synthesized, each owning a disjoint file set. They also re-read the source behind every tier-marker change. Over the 276: 80 confirmed (hard wraps, escaping), 15 corrected, 4 cut, 177 false positives (glue text, the corpus's own phrasing, titles). Beyond the list, verifiers cut 3 more and corrected about 20 counts and line hints.

Quotes removed for failing verification, and what each supported:

- `raw/16` §7.6 and `bible/10` §3 — "one anchor … proves the whole DAG", attributed to #1613. **Not in the #1613 snapshot.** It supported the reading that one registry on the root SEDI credential covers every presentation; that reading still stands on code and tests.
- `bible/06` — "as derivative artifacts wrapped/bridged, not as native roots of trust", cited to `acdc-vc-diff.md`. **A raw-note summary, not in the paper.** The "not roots of trust" half is now marked unsupported.
- `bible/07` — the same "derivative artifacts wrapped/bridged" wording, cited "notes 05 §5". Same verdict, same consequence.
- `bible/06` — "enables forward-compatibility constraints without adding each minor version to `oneOf`" and "enables self-deprecating old schemas", cited to ACDC §Edge Section. **Compressions presented as quotes**, absent at both pins. The schema-evolution claim is marked unsupported (see §7).
- `bible/06` — "is NOT used in validation" (ACDC §Schema Versioning). Not verbatim; the cut note quotes the real sentence at L230, which supports the claim as it stands.
- `bible/07` §8.5 — "no single observer both detects AND rules", cited to notes 07 §5. **Not in keri-security-analysis at `149fa6c35`.** The stated reason for separating the roles is now unsupported; that the roles are distinct still rests on Sam's kids#1 sentence.

Struck during mining (unverifiable at the source, recorded in place):

- `raw/13` — five keri.one quotes not on any of the four pages: two pre-rotation sentences (no source named), two About-page paraphrases ("reputation systems require authentic, verifiable content sources"; "content spoofing, gamification, and hacking"), and "digital signing and automated verification of corporate caller IDs". None was used by a chapter or the doctrine.
- `raw/12` — the BADA-RUN expansion "Best Available Data Acceptance – Read Update Nonce" (unsourced and wrong) and the GCD expansion "grant/capability-delegation". Neither reached a chapter.
- `raw/11`, `bible/05`, `bible/06` — several first-pass schema quotes not found at `cfcbdcc7a` ("The single most important rule…", "transparent representation", "the classic impersonation/commingling failure", "a medical-only guardian is not authority…", and four non-verbatim GCD/SEDI/FAA quotes in bible/06) were struck or turned into prose; `raw/11` lists them.

Narrowed rather than cut: "Sam's Age schema requires `E1E`" (only his fixture uses it); "`-N` is not wired anywhere in keripy" (v2 `messagize` appears able to emit it); the `-N` spec row's marker `[N1.1]` → `[N]` (the row is identical on `main`).

## 7. JUDGMENT NEEDED

**1. Provenant material in a public repo — decided conservatively; needs your call.** `provenant-dev/origin-platform` is **private**; `dhh1128/keri-bible` is **public**. The raw/12 re-anchor added about 68 new verbatim quotes from Origin's internal docs (governance framework, watcher service, passcode caching, replay design). I could not reach you (confer `ask` was not permitted in this run), so I **did not commit them**. The full re-anchored note is at `.ignored/refresh-2026-10/raw-12-origin-security.reanchored.md` (gitignored, local only). The committed `raw/12` carries the pin, a citation-location fix, two struck unsourced expansions and a quote-free list of findings. origin-platform's `last_mined` stays `unknown`. The Origin quotes already in `raw/12`, `bible/02` and `bible/06` were public before this run and are unchanged. Decide whether "never quoted outward" means "never published" (then those older quotes should go too) or "never presented as KERI doctrine" (then the held-out file can be committed).

**2. Doctrine changed — panel sync owed.** Three parts of `keri-doctrine.md` changed: claim 14 (presentation registries are no longer unimplemented, and the election now happens at issuance), the I2I table row (two verifiers disagree three ways), and the citation-durability paragraphs. After merge, run `./sync-reference.sh` in `~/code/wot/keri-review-panel`.

**3. Upstream, for you to raise if you choose. Nothing was posted anywhere.**

- **CESR spec PR #178** (https://github.com/trustoverip/kswg-cesr-specification/pull/178), opened 2026-09-22 by Kor Dwarshuis, reverts your PQ PR #165 from `v1.1`. Its body is one line, with no rationale and no reviews. It is unmerged, so no marker moved. If it merges, the `[N1.1]` PQ claims in bible/04 and raw/02 become "proposed then withdrawn".
- **v2 `-N` collision.** keripy assigns `-N` to `NonceSealSingles`; both CESR branches define it as "Transferable identifier receipt quadruples". Verification also found that keripy's v2 `messagize` appears able to emit a `-N` attachment its own parser cannot read. That comes from reading the code, not running it, so confirm it by running it before raising.
- **Presentation registry vs. #1613.** `b7c170f93` lets a registry binding authenticate the Issuee without the Issuee endorsing the grant, against #1613's "must be endorsed by each Grantor". The requirement is unconditional, so an ACDC with a declared Issuee registry cannot be presented as third-party evidence without that Issuee's cooperation.
- **SEDI Age cannot be presented selectively through keripy IPEX.** Two facts combine: Sam's Age schema requires `rd`, and an undisclosed aggregate element fails a registry-backed grant. Separately, the schema does not pin the issuee position `A[1]`. No keripy test exercises either; your own selective-disclosure examples bypass `IpexHandler.verify`.
- **#1515.** Sam's 2026-10-01 "add I2I operator" reads like a slip for I1I. It is recorded uncorrected.

**4. Unresolved tensions.**

- **Which keripy edge-operator verifier is right** (`vdr/verifying.py` or `acdc/ipexing.py`). It turns on a spec "latest wins" citation that raw/03 has not checked; that check is first on next month's ACDC-spec list.
- **bible/06's schema-evolution claim** is unsupported after a cut. ACDC spec L1180 at `f0bd097de` supports it in its own words. Citing that is a new citation rather than a rewording, so I left it to you.
- **bible/02 §9 L155** (pre-existing) attributes "no single observer both detects duplicity and rules on it" to `background.md` §6.2, which does not say it. It has the same origin as the bible/07 cut and was not changed this run.
- **raw/11 governance tensions.** The governance rule `noOverAssertion` conflicts with Core treating `legalPresenceStatus` as endorsed on the strength of an email that cannot be cited. There are now three dossier bases (spec, public-schema, bakobo). Five bakobo pages are stale against bakobo's own decisions.
- **KRAM disabled.** The claim that disabling KRAM makes registry-declaring grants unacceptable is inference. It is partly corroborated by `test_ipexing.py:6169-6176`.

**5. Proposed manifest changes, not applied (reviewed fields, or structural).**

- **keripy-code `watch`:** add `tests/sedi`. This month's SEDI findings live in test fixtures the watch list cannot see.
- **`chapters` mapping:**
  - keripy-code now feeds 06 and 07.
  - keria and signify-ts now feed 04, 07 and 09.
  - keripy-discussions now feeds 05 (#1098, #1515).
- **conf26-subtitles `last_mined`** can be resolved to `15f1e91a7`, because the head has not moved since 2026-08-23, before the 2026-09-01 mining. This is the same reasoning applied to keri-security-analysis last month; not applied here.
- **bakobo-schema's old `last_mined` `8db57eb`** was a public-schema commit attributed to the wrong repo. It is now superseded by `cfcbdcc7a`.
- **Discussion #1555** (*Multiply Endorsed*) has never been mined, and PR #1693 now implements part of it. Mine it next run.
- **Untracked branches:** none proposed. CESR `revert-165-pq` is an open PR, so watch the PR rather than track the branch.

**6. Not done this run.** `raw/03` (ACDC spec) was not re-mined, since the spec did not move. In keripy `80f77b73b`, `vdr/eventing.py`, `app/habbing.py` and most of `kraming.py` were not re-read.

**Freshness.** `freshness.py` reported 368 new misses against the old baseline and 77 healed. Its corpus excludes keripy `tests/`, discussion snapshots, commit messages and hard-wrapped bakobo text, and it splits on unbalanced quotes, so most of the 368 are glue text. The adjudication that counts is the phase-5 pass in §6. The baseline was refreshed (`--update-baseline`, 1,317 known misses), so next month's NEW list starts clean. `snapshot-discussions.py`: 8 snapshots, 0 drift.

---

## Appendix — Phase 2 triage

Every candidate in `delta.md`, in exactly one class.

### Doctrinal

| # | What moved | Note | Chapters |
|---|---|---|---|
| D1 | **keripy IPEX: multiply-endorsed grants and presentation-registry authentication** (#1693, `790797bcd`), then "remove grantor requisite" (`b7c170f93`). `acdc/ipexing.py` +913. This is the first code for the presentation-registry design that `raw/16` and chapter 10 carry as `[P]`. | raw/16 (registry), raw/09 (IPEX mechanics) | 08, 10 |
| D2 | **keripy retired `TransReceiptIdxSigGroups`** (`-D`) from the v1 count-code table and reassigned the v2 `-N` code to `NonceSealSingles` (#1683; `9762d6bb4`, `e24ade8c7`, `d8bb23308`); `SealKind.d` and TDCS cast to `Noncer` rather than `Diger` (`4d5535717`, `8a4f3f0c4`). Touches `counting.py`, `eventing.py`, `parsing.py`, `structing.py` — three of the four files the 2026-09 pass did *not* re-read. Needs a check against both CESR spec lines for whether the spec still carries `-D`. | raw/09 | 04, 03 |
| D3 | **Discussion #1515 *New Unary Edge Operators to Support SEDI*** gained a 2026-10-01 comment proposing `I1I` (issuer-is-issuer) and `DI1I` operators, with a SEDI leaf-to-core use case. #1515 is also where keripy's own code traces `E1E`; `raw/09` open question 2 says the note never read it. Not yet snapshotted. | raw/09 | 05, 08 |
| D4 | **Discussion #1098 *ACDC with Static Age Predicate Proof SMT*** edited in place 2026-09-26 (20 KB, created 2025-10-27, zero comments). Argues unlinkable ZKPs are precluded because they defeat issuer-compromise detection and, via presentation registries, issuee-compromise detection. Uncited anywhere in the corpus. The quiet-thread trap: zero comments, live design. | raw/16 (detectability argument), raw/11 (age mechanism) | 05, 07, 10 |
| D5 | **keripy SEDI worked examples** (`tests/sedi/`, #1686–#1705): core SEDI schema with `primary` and `nameSuffix`, residence, age, Utah delegation-chain, AID-replacement and ward/guardian-edge ACDCs; issuee presentation registries added (#1689) then *removed from population* for linked ACDCs (#1697, `64458b7de`: "Still allowed in schema but not populated"). Test code, so evidence about intended use rather than library behaviour. | raw/11 (schemas), raw/16 (registry population) | 05, 06, 10 |
| D6 | **CESR spec: open PR #178 proposes reverting the post-quantum primitives (#165) from `v1.1`.** Branch `revert-165-pq` (`487fab7`, 2026-09-22) removes 70 lines of `spec-body.md`; no stated reason, no reviews. Not merged — `v1.1` head is unchanged at `65fd7518b` — so no marker moves, but every `[N1.1]` PQ claim is at risk. | — (no mining; JUDGMENT) | 04 |
| D7 | **KERIA pins keripy `==1.2.14`** (`8945173`), tightening `>=1.2.13,<1.3`. The corpus does not record which keripy line KERIA runs; this makes explicit that none of keripy `main`'s 2.x work (IPEX V2, KRAM, `E1E`) reaches KERIA deployments. | raw/10 | 03, 06 |

### Corroborative

| # | What moved | Note | Chapters |
|---|---|---|---|
| C1 | signify-ts `5a174b5` (#417): seal sequence number in `messagize` now parsed as hex (`Seqner({snh: …})`), was `parseInt` decimal. Corroborates the hex-`sn` interop invariant in `raw/10 §7` by fixing a violation of it. | raw/10 | 03, 06 |
| C2 | keripy KRAM: caches preserved and policy rebuilt after database clean (#1684; `87ba6a56d`, `56c43fd2b`), `kraming.py` +29. Operational, but `raw/15` records cache behaviour. | raw/15 | 09 |
| C3 | keripy aggregate-aware issuee resolution in the grant and revoke paths (#1678). | raw/09 | 05, 08 |
| C4 | papers: Apple root-program PQC/MTC announcement cited in `wtbo` (→1.9), `acdc-and-mtc` (→1.1) and `x509-prob` (→1.4); `was.md` typo and version →1.1. References renumbered in `wtbo`. | raw/05, raw/06 | 01–07 |
| C5 | keripy `regeventing.py` +180 / `registraring.py` +24 and the independent-registry bulk-issuance examples (#1576, Daniel's). | raw/09, raw/16 | 08, 10 |

### Tier movement (candidates — confirmed or refused in §3 after verification)

| # | Candidate | Evidence needed |
|---|---|---|
| T1 | Presentation registry: `[P]` → `[K]` for whatever part #1693 actually implements | code at `80f77b73b`, not the PR title |
| T2 | Multiply-endorsed IPEX grants (#1555/#1613 design): `[P]` → `[K]` | code at `80f77b73b` |
| T3 | `TransReceiptIdxSigGroups` `-D`: existing `[K]` claims superseded | code at `80f77b73b`; spec text at both CESR pins |
| T4 | `I1I`/`DI1I`: new `[P]` | #1515 comment text, snapshotted |

### Re-anchor (full, no prior pin)

| # | Source | Note |
|---|---|---|
| R1 | bakobo-schema `unknown`/`8db57eb` → `cfcbdcc7a` | raw/11 |
| R2 | public-schema `unknown` → `95a07e544` | raw/11 |
| R3 | origin-platform `unknown` → `cb758b1b5` | raw/12 |
| R4 | keri-one: first content hashes recorded; no prior hash, so "changed" cannot be told from "never hashed" | raw/13 |

### Noise

- **dossier-spec** `b9227753c` → `3ff1b3202`: two commits, `.gitignore`, `assets/custom.css`, `package*.json`. No spec text.
- **keripy**: `SECURITY.md` (#1691), spec-citation-by-section docs (#1676), escrowLDEvent `AttributeError` fix (#1692 — a crash fix in an escrow the corpus describes but does not characterize at code level), V2 mailbox forwarding framing (#1680), `webbaser` sync (#1673), CLI tweaks, test-only refactors.
- **keria**: agent "tocks" scheduling configuration (`scheduling.py`, `agenting.py`, `Anchorer` escrow cadence), 0.4.1 release metadata, workflow. Operational cadence, not doctrine.
- **cesr-spec / keri-spec / acdc-spec / keri-security-analysis / keripy-knowledge**: no movement on any tracked line.
- **smithsamuelm-papers**: quiet, confirmed by direct API read — `whitepapers/kram.md` last touched by `67550b477` (2026-03-06), the commit already mined. Not an unread source.
- **conf26-subtitles**: quiet, confirmed by direct API read — head `15f1e91a7` (2026-08-23) predates the 2026-09-01 mining.
- **Untracked branches**: keripy `webbaser`; keripy-knowledge `feat-indep-registry-bulk-issuance`, `patch-1`, `fix-stale-spec-refs`, `feat-edge-operators-status-axis` (Daniel's PR branches in his fork, which the worktree sees); bakobo-schema `sedi-repin-guardians`, `gcd-targets`, `tick`, `sedi-guardian-no-gcd`; public-schema `brand-owner`; origin-platform four branches. None proposed for tracking except as noted in §7.

### Traps checked

- **Quiet thread**: #1098 has zero comments in eleven months and was edited in place on 2026-09-26. #1515's new comment arrived ten weeks after the previous one.
- **Two vocabularies**: the registry is "presentation registry" in #1693's title and in #1098, "issuee presentation registries" in #1689, and "issuee usage registry" in #1095. Miners were told to search all three, plus whatever field name the code uses for it.

### Work list

Mining, one agent per note: raw/09, raw/16, raw/11, raw/12, raw/15, raw/10, raw/05, raw/06, raw/13.
Synthesis, one agent per chapter: decided after mining from what actually moved.
