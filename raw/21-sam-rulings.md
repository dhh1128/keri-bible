# Doctrine Mining: Samuel M. Smith's rulings on GitHub, 2025-10-14 to 2026-10-14

Sources: every issue, pull request, PR review, PR review comment and discussion in which GitHub user SmithSamuelM authored the item or a comment during the window, across four repositories: `WebOfTrust/keripy`, `trustoverip/kswg-keri-specification`, `trustoverip/kswg-acdc-specification` and `trustoverip/kswg-cesr-specification`.

Fetch: read-only `gh api` GETs and `gh api graphql` queries, run 2026-10-14 (fetch start recorded in `.ignored/sam-rulings-cache/FETCHED_AT`). Raw responses are cached under `/home/daniel/code/me/keri-bible/.ignored/sam-rulings-cache/`: `search/` (the issue searches), `items/` (per item: issue, comments, PR, review comments, reviews), `disc/` (one GraphQL dump per discussion, with comments and replies), and `corpus.md`, a derived reading file that interleaves every in-window Sam text with the comment it answers. Nothing was written to any GitHub conversation.

Specification pins, all equal to the upstream branch heads on 2026-10-14 (checked with `gh api repos/trustoverip/<repo>/branches/<b>`): KERI `main` @`fbdd4a615`, `v1.1` @`3753f3797`; ACDC `main` @`f0bd097de`, `v1.1` @`2362e48a1`; CESR `main` @`bad6edd84`, `v1.1` @`65fd7518b`. These are the pins in `refresh/sources.yaml`, so at-the-pin and at-current-upstream are the same statement for every spec check below.

Implementation pins: keripy `main` @`80f77b73b` (the `sources.yaml` pin, read from the local clone at `~/code/wot/keripy`). keripy upstream `main` had moved to `c102367ea` (2026-10-14); where a ruling bears on code that changed after the pin, the file was read at `c102367ea` through the GitHub contents API and the citation says so.

Mining date: 2026-10-14.

Scope statistics: the issue search returned 212 distinct issues and PRs (66 issues, 146 PRs) where SmithSamuelM authored, commented or reviewed and the item was updated in the window; GraphQL returned 36 discussions updated in the window. Of these 248 items, 224 carry at least one Sam text created or edited in the window, and those texts number 362 (bodies, comments, replies, reviews and review comments). Most are review mechanics on the 2026 database refactor ("Please resolve conflicts", "Looks good") and carry no ruling. Rulings kept: 78, numbered R-001 to R-078 below. Five large Sam bodies were not re-mined in depth because other notes own them: #1095 and #1613 (`raw/16`), #1627 (`raw/16`, `bible/08`), #1299 (its body is the KRAM whitepaper v0.7.6, owned by `raw/15`) and #934 (`raw/15`; no Sam comment in it falls in the window).

---

## 0. Provenance and how to read this note

A GitHub comment is `[P]` in this corpus's tier scheme, however confident its author: it is a position stated in a discussion, not specification text and not code (`refresh/prompts/standards.md` §2). Sam is a spec editor for all three specifications, so his rulings in those repositories forecast the text more reliably than anyone else's, but they are still forecasts until the text lands. Each ruling below says whether it has reached a spec branch, and which, with the line at the pin.

Comment bodies are moving targets. Sam edits in place: #1613's body carries the in-body version "v1.5 2026/08/18" and was last edited 2026-09-02; #1549's body was edited after its own comment stream superseded parts of it. Every ruling therefore records the comment URL and its `created_at` and `updated_at` from the cached API response. Where the two differ, the quote was read at the cached (updated) text.

Quotes are verbatim, including Sam's typing errors, which are frequent ("halluciantion", "aggrative", "Aggree"). Nothing inside a straight double quote has been corrected, with two mechanical exceptions: runs of spaces in the original are collapsed to one, and typographic apostrophes are rendered straight. Where a quote stops short of the original sentence, it stops; nothing has been elided from inside a quote. Where a typo could mislead, the sentence after the quote says what it means.

A ruling here is a statement that settles or clarifies how KERI, ACDC or CESR is meant to work: an intended semantics, a rejected design and its reason, a bug-or-design verdict, a deprecation, a naming decision, a correction of a misunderstanding, or what ambiguous spec text means. Scheduling, thanks, merge mechanics and review nits were read and discarded. A handful of keripy-internal rulings are kept because they bind the reference implementation's storage or wire behavior in ways a reimplementer would otherwise guess at.

The window catches one live dynamic that colors many rulings. On 2026-08-07, on keripy PR #1564, Sam wrote that he would stop answering AI-generated issues (R-073). Several rulings after that date are shorter and some decline to engage. This note records what he ruled, not why he ruled less.

---

## 1. KEL and key events

### R-001 Delegated inception may carry anchoring seals; dropping them was a bug

Ruling: "This is a bug. Good catch." Comment https://github.com/WebOfTrust/keripy/issues/1544#issuecomment-5070932782, created and updated 2026-07-24T14:26:44Z, followed by "fixed with #1545" (same thread, 2026-07-24T20:45:26Z).

Question settled: whether a delegated inception (`dip`) is forbidden to carry seals in its `a` field, given that `BaseHab.incept` passed `data=` to `incept()` but not to `delcept()`. It is not forbidden; the omission was a defect.

Cross-check: `[K]` at keripy `80f77b73b`, `src/keri/app/habbing.py` L1107-1115 now passes `data=data` to `eventing.delcept`. Not in the bible, which never says either way whether a `dip` may anchor seals. Belongs in `bible/03` §delegation as a one-line fact.

### R-002 A KEL event's own version is permanent; attachments can be newer

Ruling: "Key event messages, because they are signed and must be verifiable indefinitely, can't be upgraded." Comment https://github.com/WebOfTrust/keripy/pull/1519#issuecomment-5060786324, created 2026-07-23T16:20:34Z, updated 2026-07-23T16:47:20Z.

The same comment separates the two version numbers that travel with a message: "there should be no reason that attachments can't be version 2 even when the message is V1, except when talking to a V1-only parser." And it states the migration consequence plainly: "there is no backward-compatible path for new v2 key event messages."

Question settled: whether replay should derive the attachment genus from each event's own `pvrsn` (dhh1128's review had called that "the right direction"). Sam's answer is no as a default: the attachment version follows the receiving parser, not the message.

Cross-check: consistent with `bible/04` on genus/version as a stream-level property, but the bible does not state the rule that a v1 key event may travel with v2 attachments, nor that v1-only parsers are a dead end. Missing; belongs in `bible/04` near the genus/version discussion. Not checked in code.

### R-003 Key-state currency for a signature group is the last establishment event, read from the Kever

Ruling: "The seal reference should be to the keystate determined by the latest establishment event." And: "These type of checks should always be aginst the Kever instance" and "not by looking at the values inside the serialized event." Comment https://github.com/WebOfTrust/keripy/pull/1658#issuecomment-5514292225, created 2026-09-02T18:19:37Z, updated 2026-09-02T18:22:27Z.

Corrected the same day: "My bad halfway through the writeup I forgot this was a signature group code not a seal reference." Comment https://github.com/WebOfTrust/keripy/issues/1667#issuecomment-5516149525, created and updated 2026-09-02T20:45:08Z. Its consequence: "When the authentication factor is a seal reference then its always pointing to the exact event that holds the anchoring seal".

Question settled: whether KRAM's `tsg` currency test compares against the last event of any kind or the last establishment event. Establishment. The paragraph in the first comment allowing a later interaction event was withdrawn for signature groups by the second.

Cross-check: already in the bible at `bible/09-kram-and-request-authentication.md:88` (the currency rule) and :137 (all ten sites read `kever.lastEst`), from `raw/15`. The self-correction in #1667 is not recorded there and should be, because #1667 is still open and its title still describes the withdrawn wider case.

### R-004 An effectively non-transferable AID is a transferable code with an empty next-key list

Ruling: "An effectively non-transferable AID is an AID that uses a transferable code but has a specially defined inception event." And: "non-transferable AIDS (both effective and and code) may only ever have an inception event in their kel." Comment https://github.com/trustoverip/kswg-cesr-specification/pull/165#issuecomment-4085555336, created 2026-03-18T21:01:41Z, updated 2026-03-18T21:38:00Z.

Question settled: whether post-quantum public keys, too large for a compact non-transferable prefix, need a new non-transferable code meaning a digest of a public key. They do not: the existing effectively non-transferable AID already gives a compact identifier with a one-event KEL as its key cache.

Cross-check: `[K]` keripy `80f77b73b` `src/keri/core/eventing.py` L2121-2127 documents `transferable` as "Returns True if identifier does not have non-transferable derivation code and .nextor is not None". The general principle is already in the bible at `bible/03-key-management-and-identifier-lifecycle.md:47`, which corrects the prior that non-transferability is a property of the prefix code. The ruling's consequence for post-quantum codes reached CESR `v1.1` (R-019). Not in CESR `main`.

### R-005 Delegated superseding recovery is implemented in keripy, not necessarily in agents

Ruling: "The keripy library includes these rules, but don't know if KERIA understands them or what to do to recover." Comment https://github.com/WebOfTrust/keripy/issues/26#issuecomment-3560827768, created and updated 2025-11-21T00:49:15Z.

Question settled: whether issue #26 (delegated superseding recovery rules A0-C1) is done. In the library, yes; in wallets and agents that must generate a superseding recovery rotation, unknown.

Cross-check: the rules themselves are in the bible at `bible/03-key-management-and-identifier-lifecycle.md:146` (§10 Recovery). The agent-side gap is Sam's assessment, not a survey, and is not recorded. It belongs in `bible/03` §KERIA as a stated limit.

### R-006 A sender is always one AID; AID allow and deny lists filter, they do not authenticate

Ruling: "When an AID is multisig/multikey The sender is still just one AID, Its always one AID." And: "The AID based denail/accept lists are not authenticating they are filtering." Comment https://github.com/WebOfTrust/keripy/pull/1360#issuecomment-4122133697, created and updated 2026-03-24T23:43:23Z.

Question settled: a KRAM contributor wrote that identifying the sender AID needed "more work" for multisig and delegated senders. It does not: identifying the sender and authenticating the message are separate tasks, and the list check is only the first.

Cross-check: not stated in `bible/09`. It is a short corrective worth a sentence in `bible/09` beside the sender-identification step, and a candidate shibboleth (identity filtering mistaken for authentication).

### R-007 A controller may legitimately send a signed receipt of its own event

Ruling: "in general a controller should be able to send a signed receipt of one of its own events to someone else". Issue body https://github.com/WebOfTrust/keripy/issues/1469, created 2026-06-27T17:34:17Z, updated 2026-06-27T18:06:36Z.

Question settled: whether `processReceipt`'s refusal of a receipt in which the receiptor is the event's own controller is correct. Sam reads the refusal as an assumption that "controller would always sign locally so a remote receipt must be a fraud attempt", and rules the assumption too narrow.

Cross-check: `[P]`, an open issue. Not in the bible. Not checked in code. Low priority.

---

## 2. Witnesses, watchers and discovery

### R-008 Witnesses cannot be watchers, and delegation is where it shows

Ruling: "witnesses are being used as ersatz watchers in the wild, but witnesses cannot be watchers, and delegation is where this difference is most pronounced." And: "An event should not be Seeable by a second party unless a watcher can see it, not if a witness can see it." Comment https://github.com/WebOfTrust/keripy/issues/1559#issuecomment-5138781953, created 2026-07-31T03:04:08Z, updated 2026-07-31T03:11:51Z.

The mechanism, in the same comment: a witness validates a delegated establishment event before the delegator's seal exists, "because witnessess are witnesses to only the controller's commitment not the Delegator's committment to that event." And the assessment, which is his and not a survey: "implementations that do not use watchers cannot get it right. This includes the GLEIF ecosystem in general."

Cross-check against the KERI spec: consistent. At `main` @`fbdd4a615` L1774 (and `v1.1` @`3753f3797` L1773) a witness "MUST first verify the event's controller signatures before it can sign (witness)", with no delegator-seal requirement, while a non-controller, non-witness validator MUST verify the "delegator anchoring seal (if delegated)" (`main` L1780, `v1.1` L1779). Already in the bible as an invariant: `bible/02-security-model-and-threat-posture.md:171` and `bible/07-shibboleths-and-anti-patterns.md:308` ("A witness is NOT a watcher"), both sourced to keripy-knowledge. Missing from the bible: Sam's statement that this is a live deployment fault (witnesses used as watchers in production, patched around with old witness code), and the operational rule that a second party must look "through the eyes of a watcher". Belongs in `bible/02` §witness/watcher and in the infrastructure chapter the coverage report proposes.

### R-009 Transferable receipt groups should carry indexed signature groups, for watcher receipts

Ruling: "The use case would be a watcher receipt so that BADA-RUN can be used for watched events from watchers that have transferable AIDs". Issue body https://github.com/WebOfTrust/keripy/issues/1450, created 2026-06-23T14:00:56Z, updated 2026-06-23T15:11:50Z.

Question settled: what `TransReceiptQuadruples` (`-N`) is for, given that nothing used it. Sam proposed renaming it to an indexed-signature-group form, or deleting it.

Later status: keripy PR #1683 (Sam, merged 2026-09-15) is titled "Finished refactor to remove now reduandant TransReceiptIdxSigGroup usage. Replace with NonceSealSingles"; that title is not a ruling and its code was not read for this note. `bible/04-cesr-and-the-wire.md` already cites #1683 (per the reference index); whether it records the watcher-receipt rationale was not checked. Low priority.

### R-010 Witness receipting is only logically parallel within one process

Ruling: "Multiple doers running in a single process are only logically parallel. They are still sequential within the one process." Comment https://github.com/WebOfTrust/keripy/issues/855#issuecomment-3607600921, created 2025-12-03T16:06:28Z, updated 2025-12-03T16:11:49Z, followed by "HIO now supports multiprocessing." in the same comment.

Question settled: whether a parallel receipting doer would deliver the latency gain issue #855 estimated. Only partly, unless the doers run as separate processes.

Cross-check: `bible/03` cites #855 (per the reference index); this engineering ruling is not there. Belongs in the infrastructure chapter, not in doctrine.

### R-011 An OOBI bootstraps the controller AID, and redirects to witnesses

Ruling: "Ultimately what the User cares about iOut of Band is to be given the controller AID of interest not its witness AIDs". And: "OOBIs themselves are insecure discovery mechanisms, whatever you discover you must still verify". Comment https://github.com/trustoverip/kswg-cesr-specification/pull/165#issuecomment-4090031232, created 2026-03-19T13:10:45Z, updated 2026-03-19T13:53:14Z.

Question settled: whether 1000-character post-quantum witness AIDs make OOBI URLs unusable. No: the bootstrap OOBI names the compact controller AID, and its endpoint serves a JSON multi-OOBI that redirects to the witnesses, however long their AIDs.

Cross-check: the verify-after-discovery principle is in the bible (OOBI appears 28 times; `bible/02-security-model-and-threat-posture.md:42` area). The redirect pattern, and the rule that the bootstrap names the controller AID rather than a witness AID, are not. Belongs in the infrastructure chapter (coverage gap 2).

---

## 3. Delegation and configuration traits

### R-012 `DID` sits in the delegatee's `dip`, and the Ean example was an oversight

Ruling: "THE DID sits in a Delegatee Inception event." And: "Putting DID in a delegator would be ambiguous since a delegator could also be a delegatee of a higher level delegator." Comment https://github.com/WebOfTrust/keripy/discussions/1570#discussioncomment-17896521, created 2026-08-04T16:37:23Z, updated 2026-08-04T16:55:46Z.

Then, on the KERI spec's own worked example: "Yeah, putting DID in a plain, non-delegated ICP, as an example, was an oversight." Reply https://github.com/WebOfTrust/keripy/discussions/1570#discussioncomment-17898407, created and updated 2026-08-04T20:13:03Z.

Cross-check against the KERI spec: the placement rule is in `v1.1` @`3753f3797` L381 (the trait "MUST NOT appear in a non-delegated Inception, `icp` event", per `bible/03`), and Ean's `v1.1` trait list is empty (L618). On `main` @`fbdd4a615` Ean's plain `icp` still carries `"c": ["DID"],` at L591. So the ruling is carried into `v1.1` and not into `main`.

This settles an open tension in the bible. `bible/03-key-management-and-identifier-lifecycle.md:126` carries two readings of the Ean example, a defect being fixed or a genuine disagreement between branches, and says that no source in the corpus settles it. Sam's reply is that source: the `main` example is an oversight. `bible/03:126` and `bible/07-shibboleths-and-anti-patterns.md:312` (§8.4) should cite it. The placement half of §8.4 can then stop being carried as `[N1.1]`-only intent and be stated as the spec editor's ruling, still tiered `[N1.1]` for text.

### R-013 Delegated AIDs work without ACDCs; `DND` limits depth, `DID` asserts one controller

Ruling: "It is invalid to assume that delegated AIDs can only be used in concert with delegated ACDCs." And: "The DND flag limits how far down a given delegated AID is allowed to go." Comment https://github.com/WebOfTrust/keripy/discussions/1570#discussioncomment-17896622, created 2026-08-04T16:46:04Z, updated 2026-08-04T16:57:18Z.

The two use cases he distinguishes, in the same comment: custodial key management by a different controller, where `DND` is used and `DID` is not, and horizontal scaling by one controller, which "uses DID".

Cross-check: `bible/03-key-management-and-identifier-lifecycle.md:120` has both traits in one sentence each. The custodial-versus-horizontal-scaling rule for when `DID` applies is missing, and it is the practical decision an implementer faces. Belongs in `bible/03` beside :120.

### R-014 `DND` is enforced in key-state validation, not in tooling

Ruling: "The Kever won't validate the event so it will be dropped and hence never be seen by anyone anywhere." Comment https://github.com/WebOfTrust/keripy/pull/1572#issuecomment-5184545123, created and updated 2026-08-04T20:58:20Z. Followed by: "There is no code support yet for "DID" because DID enforcement comes at the EGF level AFAIK" (https://github.com/WebOfTrust/keripy/pull/1572#issuecomment-5184567539, 2026-08-04T21:00:40Z).

Cross-check: `[K]` keripy `80f77b73b` `src/keri/core/eventing.py` L3251, "if dkever.doNotDelegate:  # drop event if delegation not allowed". Consistent. The bible says `DID`'s consequence is unspecified on both branches (`bible/03:124`, `bible/07:312`). The second comment adds Sam's answer to where that consequence lives: the EGF, with no protocol-level enforcement. That is an assessment ("AFAIK") and should be recorded as one, in `bible/03` §8 and `bible/07` §8.4.

### R-015 `DI2I` reaches delegated AIDs at any depth; depth is controlled by `DND` and `DID` (a reversal)

First position: "I agree that the safe choice is to limit DI2I to one layer children not all the way down." Comment https://github.com/WebOfTrust/keripy/pull/1564#issuecomment-5137135970, created 2026-07-30T23:00:05Z, updated 2026-07-30T23:02:17Z.

Reversed three days later: "After some thought, I am revising my previous comments." And: "DI2I is a permission that enables AID Delegation All the Way Down". And: "This is how we are safe, not by interpreting the `DI2I` operator as only being for children not grandchildren." Comment https://github.com/WebOfTrust/keripy/pull/1564#issuecomment-5158683549, created 2026-08-02T14:55:02Z, updated 2026-08-02T14:59:52Z.

Then, on what the operator inspects: "DI2I has to do with the delegated inception event. that is the only event where the delegators AID is included in an establishement event." Comment https://github.com/WebOfTrust/keripy/pull/1564#issuecomment-5220496025, created and updated 2026-08-07T18:08:49Z.

Cross-check against the ACDC spec: `v1.1` @`2362e48a1` L1221 says `DI2I` admits "any delegated AIDs of the Issuee", silent on depth; `main` @`f0bd097de` is the same in substance. Sam says that silence needs filling: "the spec language needs to include the qualification that the a delegated AID in the context of `DI2I` is any layer of delegation." Not carried into either branch. `[K]` keripy `80f77b73b` still fails `DI2I` closed by design (`bible/08-presentation-architectures-and-ipex.md:128`); PR #1564, which implements the any-depth reading, is open.

Already in the bible: `DI2I`'s existence and fail-closed status (`bible/08:122`, :128). Missing: the any-depth ruling, the reversal, and the rule that depth is governed by inception-time traits rather than by the operator. Belongs in `bible/05` §5 (operators) and `bible/03` §delegation. This is one of the most important missing rulings, because a reader of the spec text alone would implement the narrower reading that Sam first proposed and then withdrew.

### R-016 `DID` makes reputation transitive across a delegation

Ruling: the trait is there "to formally signal that the controller of the delegated AID is identical to the controller of the delegating AID." And: "What a second party does with this declaration of controller equivalence between two AIDs (delegator and delegate) is up to the second party." Discussion body https://github.com/WebOfTrust/keripy/discussions/1598, created 2026-08-09T12:33:24Z, updated 2026-08-09T12:39:13Z.

Question settled: why `DID` exists at all. To let reputation, and identity assurance in particular, pass to the delegatee, and consequences pass back to the delegator.

Cross-check: `bible/03:124` and `bible/07:312` record that no spec says what a validator does with the equivalence. This ruling agrees that the protocol does not say, and says it deliberately leaves it to the relying party. That turns a gap the bible flags into a stated design choice. `raw/20` covers the reputation theory from the papers; this is the GitHub statement tying it to `DID`. Belongs in `bible/03` §8 and the proposed reputation section of `bible/06`.

---

## 4. CESR and the wire

### R-017 Fixed codes cost at most two bytes; post-quantum primitives go in the large tables

Ruling: "So at worst case there is never more than 2 bytes of overhead no matter the length of the primitive." And: "Since PQ codes are so large, there is no reason to consume the limited code space from the compact code tables." Comment https://github.com/trustoverip/kswg-cesr-specification/pull/165#issuecomment-4085555336 (as R-004). The reason is that fixed codes are chosen by the primitive's length modulo 3 to keep 24-bit alignment.

Question settled: whether variable-length codes would save space on large signatures. They would not, and the fixed code doubles as the dispatch key to the right library call.

Cross-check: PR #165 merged into CESR `v1.1` (`bible/04` cites it). The rationale is not in the bible. Belongs in `bible/04` §code tables.

### R-018 Cryptographic agility has a right amount, and Falcon should be fixed-length

Ruling: "There is a saying in crypto. Too much agility is a bad thing. There is a goldilocks amount of agility." Comment https://github.com/trustoverip/kswg-cesr-specification/pull/165#issuecomment-4086516133, created 2026-03-19T00:14:14Z, updated 2026-03-19T01:30:53Z.

Its application: support only the fixed-length (padded) Falcon signatures, citing timing-attack exposure of the variable-length form and the lesson of ECDSA versus Ed25519. dhh1128 revised the PR accordingly ("Only fixed-len sigs, no primitives for hash-of-pubkey", 2026-03-19).

Cross-check: the bible's agility material (`bible/01-foundations-and-worldview.md:90`) presents agility as an unqualified virtue. Sam's counterweight, that too many variants is itself a vulnerability, is missing and belongs beside it, and in `bible/07` as the guard against the opposite shibboleth, that CESR should carry every variant of every algorithm.

### R-019 A CESR code says how a primitive is encoded, never what it is used for

Ruling: "The CESR code defines the encoding not the usage semantics." And: "the only exception we make in CESR for cryptographic primitives that encode some semantic is the non-trans versus trans codes for public keys as AIDs." Comment https://github.com/trustoverip/kswg-cesr-specification/pull/165#issuecomment-4087093269, created 2026-03-19T02:12:01Z, updated 2026-03-19T02:21:57Z.

Cross-check against the CESR spec: carried into `v1.1` @`65fd7518b` L1559, which says a "digest of a public key" code "would mix the semantics of a Primitive's use with the semantics of its cryptographic algorithm, which this specification otherwise avoids." Absent from `main` @`bad6edd84` (1565 lines; the PQ material is `v1.1`-only). The principle is not stated in the bible; `bible/04` should state it with the `v1.1` citation as `[N1.1]` and Sam's comment as its rationale.

### R-020 The Ed448 seed code should be fixed, and implemented with tests, before more codes land

Ruling: "So I would rather fix the ed448 before putting in the PQC codes". Comment https://github.com/trustoverip/kswg-cesr-specification/issues/175#issuecomment-5496520050, created and updated 2026-09-01T15:43:13Z. And: "We should actually implement 448 with unit test in keripy so we know that the codes are right." (https://github.com/trustoverip/kswg-cesr-specification/issues/175#issuecomment-5496535050, 2026-09-01T15:44:22Z). And on what matters: "What is important is how they are serialized and stored outside the crypto operations as raw bytes." (https://github.com/trustoverip/kswg-cesr-specification/issues/175#issuecomment-5497714395, created 2026-09-01T17:19:46Z, updated 2026-09-01T17:23:27Z.)

Question settled: issue #175 reports that CESR's Ed448 seed code `K` holds 56 raw bytes while RFC 8032 and the `cryptography` library use 57-byte private keys. Sam's last comment in the thread demonstrates the 57-byte length in Python and so accepts the premise.

Cross-check: not carried. The `K` row is unchanged on both branches, "Seed of Ed448 private key" with a one-character code and 76 text characters (`main` L961, `v1.1` L969), which is 56 bytes. The PQ codes had already merged into `v1.1`, so the preferred order did not happen. Issue #175 is open. `bible/04` mentions Ed448 three times and does not record the defect. It belongs in `bible/04` as a known table defect, carried as open.

### R-021 The parser swallows exceptions on purpose, so a service is not an oracle

Ruling: "In a long running service that faces the open internet, best practice for "security" related protocols is to not inform the caller why a given message sent to the service failed". And: "So the approach is to swallow and log all exceptions, not bubble them up." Comment https://github.com/WebOfTrust/keripy/pull/1580#issuecomment-5221176507, created 2026-08-07T19:25:00Z, updated 2026-08-07T19:35:25Z.

Question settled: whether `groupParsator`'s blanket `ExtractionError` should be made granular in the main path. No; callers who need the exceptions (to pre-qualify outgoing messages) should get a separate non-swallowing wrapper.

Cross-check: not in the bible. A short security-posture point for `bible/02` (no failure oracle; restart timing as a side channel) and `bible/04` (parser behavior).

### R-022 v2 does not embed messages; it attaches them as nested substreams

Ruling: "This embedding requires that embedded messages share the same serialization of the embedding message. Which breaks down for v2 with 4 serialization types." And: "So the fix in version two is not to embed but to attach nested substreams that have the otherwise embedded message." Comment https://github.com/WebOfTrust/keripy/pull/1441#issuecomment-4772533040, created and updated 2026-06-22T20:06:28Z.

Question settled: why IPEX tests that use `specialExchange` must stay on v1. Embedding is a v1 construct and v2 replaces it.

Cross-check: `[K]` keripy `80f77b73b` `src/keri/peer/exchanging.py` L801-815, `specialExchange` defaults to `version=Vrsn_1_0` and `kind=Kinds.json`. Not in the bible (zero hits for "substream" or "specialExchange"). Belongs in `bible/04` (message composition) and `bible/08` (why a v2 `grant` carries its ACDCs as attachments, not as `e` embeds).

### R-023 Signatures go in insertion-ordered sets, not LMDB duplicates, because post-quantum signatures are too large

Ruling: "I changed .rcts to Used CatCesrIoSetSuber because it includes signature which may be too big for dup space when post quantum." Comment https://github.com/WebOfTrust/keripy/issues/1163#issuecomment-3842006990, created and updated 2026-02-03T15:27:45Z. The same reasoning recurs in issue #1355 for `.uwes` (body, created 2026-03-20T14:48:03Z).

Question settled: storage layout for signature-bearing sub-databases in keripy, given LMDB's 511-byte limit on duplicate values. keripy-internal, kept because a reimplementer copying keripy's earlier `dupsort` layout would hit the same wall with post-quantum keys.

Cross-check: not in the bible, and it belongs in `raw/08`/`raw/09` rather than a chapter. A related portability ruling, also internal: `OnIoSetSuber` exists because "Other b-tree like databases such as IndexedDB do not support the convenience methods of LMDB" (PR #1218 body, created 2026-02-23T20:22:33Z), which is the WASM/browser storage path.

### R-024 `Saider` is for non-message SADs; KERI and ACDC message digests are `Diger`

Ruling: "Want to leave Saider for the special cases of SADs that are not KERI or ACDC message types." Issue body https://github.com/WebOfTrust/keripy/issues/1209, created 2026-02-19T22:22:36Z, updated 2026-07-15T21:27:41Z.

Cross-check: a keripy naming rule; carried out across the 2026 refactor PRs (#1211, #1222, #1242). Not doctrine. Record in `raw/09` only.

---

## 5. ACDC: sections, edges and operators

### R-025 The issuee of an aggregative ACDC is the `i` of the second block

Ruling: "The issuee in an ACDC with Agg section (selectively disclosable) is the "i" field in the second (index 1) attribute block. This could/should be better clarified in the spec." Comment https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4981932724, created and updated 2026-07-15T14:47:58Z. Repeated in the #1512 body (created 2026-07-16T15:44:30Z).

Cross-check against the ACDC spec: not carried as a rule on either branch. `v1.1` @`2362e48a1` shows an issuee block at index 1 in its JSON example (L920-924) and notes "the value of the `i` field is the Issuee of the ACDC" (L941), but states no positional requirement. `[K]` keripy reads `A[1].i` (`bible/05-acdc-and-verifiable-data.md:74`, Finding 2). The bible's Finding 2 says "nothing requires the issuee block to sit at index 1"; that remains true of spec and schema, and Sam's ruling says the intent is that it does sit there and the spec should say so. `bible/05:74` should add the ruling so the finding reads as a spec gap against a stated intent rather than an open design question.

A related ruling on `dt`: "unlike issuee where the index 1 is for the issuee when there is one, there is no preferred index to place the dt." Comment https://github.com/WebOfTrust/keripy/issues/1679#issuecomment-5671060930, created 2026-09-14T21:28:58Z, updated 2026-09-14T21:31:42Z.

### R-026 Issuee binding is boolean; ACDCs have no weak holder binding

Ruling: "IN an ACDC either you have cryptographically verifiable binding via an "i" field with the issuee aid or you have no binding. Its boolean." Comment https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4981932724 (as R-025). The #1095 body (edited 2025-11-11) says the same: "ACDCs do not support weak binding. It's either all or nothing."

Also in that comment: "An ACDC can only be either attributive or aggregative not both (mutually exclusive)".

Cross-check: Targeted versus Untargeted is in `bible/05-acdc-and-verifiable-data.md:56` from the spec. The explicit rejection of W3C-style weak holder binding is not stated as such and is a natural `bible/07` shibboleth (the W3C reflex that ACDC holder binding comes in strengths).

### R-027 The SEDI core identity credential should be attributive, not aggregative (a reversal)

First position, 2026-07-15: "I believe for the core SEDI identity credential the appropriate choice is to use the selectively disclosable Aggregate section." (#1505 comment of R-025.)

Reversed the next day: "So I now think that the SEDI core identity core identity credential should be an attribute credentials." And on when the aggregate earns its cost: "The use case that I can think of is an array of Boolean flags for age thresholds." And: "An aggrative array in this case is a poor mans sparse merkle tree." Comment https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4992155156, created 2026-07-16T13:00:47Z, updated 2026-07-16T13:20:46Z. Then: "So now I am admitting I got it wrong." (https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4992746261, created 2026-07-16T13:57:05Z, updated 2026-07-16T14:12:24Z.)

The reason given is first-principles: the aggregate's only advantage is unlabeled, position-blinded blocks, which a well-known fixed field set does not need, while it costs label-based pathing.

A stale copy survives. The body of discussion #1512 (created 2026-07-16T15:44:30Z, never edited according to the API's `lastEditedAt`) still contains the pre-reversal sentence "I believe for the core SEDI identity credential, the appropriate choice is to use the selectively disclosable Aggregate section." A reader who finds #1512 first gets the withdrawn answer.

Cross-check: `bible/05-acdc-and-verifiable-data.md:58-62` already reaches the same choice from the applied corpus and notes that "Sam reached the attribute-versus-aggregate choice independently"; keripy's SEDI fixtures (`sedi-age` as an aggregate of boolean thresholds) match the reversed position. Missing: the reversal itself and the #1512 staleness warning. Belongs in `bible/05` §4 as a dated note.

### R-028 An edge schema that differs from the far node's schema means two validations

Ruling: "two schema validations must be performed and both must be valid." Comment https://github.com/WebOfTrust/keripy/issues/1534#issuecomment-5040429900, created and updated 2026-07-22T00:22:43Z. The condition is an edge schema SAID that differs from the far node's own schema SAID; the far node must then satisfy both.

The purpose: "The allows near side nodes to require backwards compatible schema versions (essentially upgrading) via backwards compatible edge schema without having to reissue far node's ACDCs." Same comment.

Cross-check: `[K]` enforced with "satisfy" rather than "equal" semantics at `bible/08-presentation-architectures-and-ipex.md:128`. The upgrade-without-reissue purpose is not in the bible and belongs in `bible/05` §5 beside the edge `s` field.

### R-029 `I2I` was misapplied to an identity relation; edges need non-delegative operators

Ruling: "The mistake is that for the worked example, the `I2I` unary edge operator is misapplied." And: "So the edge defines an an identity relation not a delegation relation." Comment https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-5004919975, created 2026-07-17T15:39:38Z, updated 2026-07-17T19:29:26Z.

Cross-check: the result, `E1E`, is `[N1.1]` in ACDC `v1.1` and enforced in keripy; the full lineage through #1515 is already in the bible at `bible/08-presentation-architectures-and-ipex.md:144` and :122. The framing that `I2I` encodes delegation, not same-holder binding, is in tension with `bible/07-shibboleths-and-anti-patterns.md:428`, which calls `I2I`'s doctrinal meaning "issuer-to-issuee same-holder binding". See Contradictions T-09.

### R-030 The empty-operator default should become `NI2I` in ACDC v1.1, behind a version switch

Ruling (issue body): "If the vLEI ecosystem has fully moved to specifying edge operators i.e. explicit I2I and Ni2i for each far side targeted edge then we could change the default in v1.1 to be 'N121` for an empty unary operator list." Issue https://github.com/trustoverip/kswg-acdc-specification/issues/205, created 2026-08-11T15:43:36Z, updated 2026-08-31T15:26:56Z. "N121" and "Ni2i" are typing slips for `NI2I`.

Decision recorded: "Based on the discussion in the maintainer call yesterday. The change of default is to land in v1.1 of the ACDC spec." And: "the v1.1 code must have a version switch that changes the default for v1.1 ACDCs but not for prior versions of the ACDC protocol." Comment https://github.com/trustoverip/kswg-acdc-specification/issues/205#issuecomment-5268897690, created and updated 2026-08-12T15:29:09Z.

Cross-check against the ACDC spec: not carried. `v1.1` @`2362e48a1` L1209-1213 still appends `I2I` for a targeted far node and `NI2I` for an untargeted one; the only change from `main` is that `E1E` joined the gate. Issue #205 is open. `[K]` keripy `80f77b73b` still infers `I2I` in `vdr/verifying.py` and applies no default in `acdc/ipexing.py` (`bible/08:140`). The bible records the #1556 proposal for group-scoped defaults (`bible/08:229`) but not this decided change of the global default. This is important and missing: it reverses the edge default that every vLEI credential in production relies on, for v1.1 ACDCs only. Belongs in `bible/05` §5 and `bible/08` §5, tiered `[P]` with the maintainer-call decision noted.

### R-031 An unrecognized operator token should not be silently defaulted (assent only)

Ruling: "This seems right." Comment https://github.com/trustoverip/kswg-acdc-specification/issues/201#issuecomment-5138898171, created and updated 2026-07-31T03:21:02Z, on dhh1128's issue that the spec does not say what a validator MUST do with an operator token it does not recognize and can be read as mandating fail-open defaulting.

This is the weakest ruling kept: three words of assent to a diagnosis, with no stated remedy. Not carried; `v1.1` has no rule for unrecognized tokens (no match for "unrecogni" or "unknown" in `spec-body.md` at `2362e48a1`). `bible/08-presentation-architectures-and-ipex.md:385` (open question 11) carries the question; it can cite this as the editor agreeing the gap exists.

### R-032 `I1I` and `DI1I` have a concrete SEDI use

Already in the bible in full at `bible/08-presentation-architectures-and-ipex.md:146`, from the #1515 comment of 2026-10-01 (https://github.com/WebOfTrust/keripy/discussions/1515#discussioncomment-18704575). Listed here for completeness and not re-mined.

### R-033 Equivalence operators wait for a use; `E1E` alone is adopted now

Already in the bible at `bible/08:144` ("The only concrete use case we have is for E1E", #1515 comment of 2026-07-18). Not re-mined. One addition from the same thread that the bible lacks: "One thing that same AID implies is the same controller the same key state because of the no-duplicity property of KERI." (https://github.com/WebOfTrust/keripy/discussions/1515#discussioncomment-17681543, created 2026-07-18T14:50:25Z, updated 2026-07-18T18:33:45Z.) It is the argument that AID equality is already the strongest equivalence KERI can offer, and it belongs in `bible/05` §5.

### R-034 Same issuer means a nested block; different issuers mean separate ACDCs joined by an edge

Ruling: "If two pieces of information have different issuers then they must be in different ACDCs and then a blindable edge enables graduated disclosure." And: "If the two pieces of information have the same issuer then a blindable sub black in the attribute section is all that is needed." Comment https://github.com/WebOfTrust/keripy/discussions/1550#discussioncomment-17909785, created 2026-08-05T17:33:56Z, updated 2026-08-05T18:25:25Z. "sub black" is a slip for "sub block".

Also in that comment, on cycles: the guardian ACDC cannot carry an edge back to the ward when the ward's ACDC already points to the guardian, "(not a DAG not possible with SAID calculation)".

Cross-check: not in the bible as a design rule. It is the cleanest statement anywhere of when to split a credential, and belongs in `bible/05` §4 (attribute versus aggregate versus DAG).

### R-035 Edge groups are not used by the vLEI

Ruling: "Not surprised. The vlei doesn't use edge groups," Same comment as R-034, answering a report that edge groups crash in keripy's credential path.

Cross-check: consistent with `bible/08:148` (m-ary operators implemented only in the V2 module). Useful as the reason edge-group bugs went unnoticed. Low priority.

---

## 6. ACDC: registries, bulk issuance and blinding

### R-036 The `upd` event is deprecated; v2 registries have only `rip` and `bup`

Ruling: "We are deprecating the 'upd' event so no reason to implement it. Only do the 'bup'". And: "We are going to drop support for `upd` in v1.1". Comment https://github.com/WebOfTrust/keripy/pull/1612#issuecomment-5259378594, created 2026-08-11T22:04:47Z, updated 2026-08-12T15:26:45Z. Restated with its reason: "This was because a blindable update can be unblinded by merely attaching the unblinded attribute block." (https://github.com/WebOfTrust/keripy/discussions/1566#discussioncomment-17846317, created 2026-07-30T23:26:36Z, updated 2026-07-30T23:33:36Z.) The idea first appears as a question at the end of the #1082 body ("We only really need the blindaable state update.").

Cross-check against the ACDC spec: not carried. `v1.1` @`2362e48a1` still defines `upd` (route row L2161, "non-blindable transaction event state update"; field order L2194), identically to `main`. `[K]` keripy `80f77b73b`: the V2 registry module says "The v2 ACDC TEL only supports registry inception and blind updates" (`src/keri/acdc/regeventing.py` L121), but `src/keri/acdc/messaging.py` L80-104 still builds an `upd`. Not in the bible (zero hits for `upd`). Missing and important: a reader of `v1.1` will implement an event the spec editor has deprecated. Belongs in `bible/05` §registries. See T-03.

### R-037 Registry transfer: proposed as `rxr`, renamed `xfr`, approved, not yet specified

First form, 2026-04-23: "New message that enables transfer of control of registry to a different delegatee." with the event type `rxr`, and the principle "when the ACDC of the delegatee is revoked, authority over any down stream ACDC state reverts to the delegator (State)." Comment https://github.com/WebOfTrust/keripy/discussions/1082#discussioncomment-16688843, created 2026-04-23T19:12:22Z, updated 2026-04-26T16:55:56Z.

Second form, 2026-07-30: "The second planned change is to add a transfer `xfr` event". And: "This event must doubly anchored." (#1566 comment of R-036.) Then: "I already discussed `xfr` with the community and got approval. so was planning to add it to ACDC v1.1." (https://github.com/WebOfTrust/keripy/discussions/1566#discussioncomment-17856451, created and updated 2026-07-31T17:31:32Z.)

Cross-check: not in either ACDC branch (no match for `xfr` or `rxr` in `spec-body.md` at `f0bd097de` or `2362e48a1`); not in keripy `80f77b73b` (no match under `src/keri`). `raw/19-authorization-and-agents.md` §4.3 covers the `xfr` proposal from the EVAC deck and records the same absence; what this note adds is the GitHub record of the name change from `rxr`, the "doubly anchored" requirement, and the statement of community approval. The bible has neither the event nor reversion of authority (zero hits). Belongs in `bible/05` §registries, or in the authorization chapter the coverage report proposes.

### R-038 TEL anchors follow KEL first-seen: keep the first verified anchor

Ruling: "anchoring TEL events should follow the idempotent first seen rule used for KEL events." And: "So put not pin." And: "it does not clobber a previously verified anchor" Comment https://github.com/WebOfTrust/keripy/pull/1612#issuecomment-5373529636, created and updated 2026-08-21T18:08:50Z.

Cross-check: partly carried. `[K]` keripy `80f77b73b` and upstream head `c102367ea` both have `putAnchor` in `src/keri/acdc/registering.py` L58-64, which refuses a new anchor whose sealing sequence number is not lower than the stored one ("Keep the earliest verified sealing event for this TEL event") but then writes with `pin`, so a later-arriving anchor with a lower sequence number does replace a previously verified one. Sam's ruling says a verified anchor is not clobbered. See T-08. The first-seen principle for KELs is in the bible (`bible/03:148`); its extension to TEL anchors is not. Belongs in `bible/05` §registries.

### R-039 The registry is general; a `bup`'s state string is unrestricted

Ruling: "The set of state strings and the semantics of those is not limited." And: "the ACDC said field could be a SAID (or merkle tree root) of something else as long as it serializes as a CESR digest." Comment https://github.com/WebOfTrust/keripy/discussions/1566#discussioncomment-17846317 (as R-036).

Question settled: whether an application may define its own TEL event types. It may ("its a free country"), but the existing blindable registry already carries any state expressible as a string over any digest, which covers most needs without new event types. Also in the comment: the bound blinded attribute block "allow broken delegation chains to break more intelligently and also to be repaired more intelligently."

Cross-check: the blinded attribute block is in `bible/05-acdc-and-verifiable-data.md:215`; its use as a general extension surface is not. Belongs in `bible/05` §registries.

### R-040 Independent registries for bulk issuance: the decorrelated case is the one that matters

Ruling: "This enables the Issuer to fully decorrelate the registry state updates from any data in the ACDC." And: "The `rd` field value is not derivable from the salt with a path." Comment https://github.com/WebOfTrust/keripy/pull/1576#issuecomment-5195334135, created 2026-08-05T17:52:40Z, updated 2026-08-05T18:04:56Z.

The mechanism, same comment: registries are pre-created with `rip` events whose `u` is a salty nonce, unassociated with any ACDC; the issuer hands the holder an indexed list of registry SAIDs at bulk issuance; and "for SEDI the use case the State has confirmed they want is the decorrelatable registrities". The co-created alternative, where the `rip` `u` is derived from the bulk salt, "does not provide the third party decorrelation". A week later Sam doubted the second case is worth specifying: "I wonder if there is any point in even specifying the second case." (https://github.com/WebOfTrust/keripy/pull/1576#issuecomment-5273063343, created 2026-08-12T21:35:14Z, updated 2026-08-12T23:47:52Z.)

Cross-check: not carried. `v1.1` @`2362e48a1` §Independent Registry Bulk-Issued ACDCs (L3098) predates the distinction; ACDC PR #204, which would specify it, is open. Not in the bible: `bible/05` and `bible/06` mention bulk issuance but not the pre-created versus co-created distinction or SEDI's stated choice. Belongs in `bible/05` §bulk issuance.

### R-041 Bulk updates with vacuous updates give herd privacy against third parties

Ruling: "The State would only update registries in bulk." And, as his assessment: "one of the most innovative privacy protectsion of blindable state registries." Comment https://github.com/WebOfTrust/keripy/pull/1576#issuecomment-5195334135 (as R-040). The thing so described is "this ability to statistically whiten registries" against third parties as well as verifiers.

Cross-check: the bible has vacuous updates and bulk updates as privacy requirements (`bible/05-acdc-and-verifiable-data.md:199`, :215; `raw/17` §8 per its own index). Partly present. The concrete herd sizing (12 million pre-created registries, minimum 100,000 updates per batch) is an illustration, not a requirement, and should be quoted only as such.

### R-042 Revoking authority revokes the whole bulk-issued set; key compromise is fixed by rotation

Ruling: "An issuer when it revokes authority revokes it universally. In a bulk issued set this means that all members of the set MUST be revoked." And: "if the keys get compromised then the keystate is changed not the ACDC state." Comment https://github.com/WebOfTrust/keripy/discussions/1574#discussioncomment-17938568, created 2026-08-07T21:49:26Z, updated 2026-08-07T22:38:26Z.

The same comment separates the two registries the question had conflated: an issuer registry tracks ACDC state, while "A presentation registry on the other hand is not tracking ACDC state, but is merely logging presentations". It also names the one case that sinks a whole set: compromise of the private salt used to derive the bulk set's keys, after which "the whole set has to be abandoned."

Cross-check: not in the bible. `bible/10-presentation-registries.md` has the issuer-versus-presentation distinction from #1095; the bulk-revocation rule and the salt-compromise boundary are missing and belong in `bible/05` §bulk issuance. This is also a correction of a misunderstanding (per-copy revocation as a feature), so it is a `bible/07` shibboleth candidate.

### R-043 One shared salt per bulk set: `v_k` derives at path `k.`, concatenation is qb64, digest defaults to Blake3-256

Ruling: "there is only one shared secret salt", so "the derivation of the vk for each constituent of B can't use the same path as the top level UUID". And: "The concatenation should be of the text domain qb64." And: "So the preferred default should be Blake256." Comment https://github.com/trustoverip/kswg-acdc-specification/pull/200#issuecomment-5063392427, created 2026-07-23T21:01:26Z, updated 2026-07-23T21:38:35Z. "Blake256" means Blake3-256.

Cross-check against the ACDC spec: carried into both branches. `main` @`f0bd097de` L2811 and `v1.1` @`2362e48a1` L3012 say the derivation path for `v_k` "is therefore `k.`"; `main` L2818 says the concatenation operators "operate on the fully qualified CESR (qb64 text) representations of their operands" and "unless a different algorithm is negotiated out of band, H is Blake3-256". This is the one bulk-issuance ruling that reached the standardizing line. Not in the bible; belongs in `bible/05` §bulk issuance, tiered `[N]`.

A follow-on ruling from the same thread: "From a SEDI perspective they want to do Independent registry bulk issuance which does not use B." (https://github.com/trustoverip/kswg-acdc-specification/pull/200#issuecomment-5063821231, created and updated 2026-07-23T21:42:01Z.)

### R-044 Blinding factors for a bulk set's registries can derive from the bulk salt by index

Ruling: "the blinding factor for each registry could be HDKey-derived from the same shared secret salt used for bulk issuance". Comment https://github.com/WebOfTrust/keripy/pull/1576#issuecomment-5273063343 (as R-040). The condition is that the ACDCs of the bulk-issued set are indexed, and the benefit is "only one shared secret salt has to be exchanged."

Then, reviewing dhh1128's spec text that pins the path as `k.s`: "Do we need the "k.s," or isn't "k." sufficient to disambiguate?" Review https://github.com/trustoverip/kswg-acdc-specification/pull/204#pullrequestreview-4922214480, submitted 2026-08-13T00:10:45Z. The same review proposes `k|` "to follow the convention that path components are variables, not literals". So the path for the registry blinding salt is unsettled between `k.s`, `k.` and `k|`.

The comment also prefers keyed Blake3 over Argon2 inside `Salter` for bulk issuance when the salt is genuinely high-entropy, on performance grounds, and keeps Argon2 as the default because "we anticipate that many users will cheat and not use a high enough entropy salt".

Cross-check: not carried; PR #204 is open. Not in the bible. Belongs in `bible/05` §bulk issuance as open.

### R-045 Bulk issuance should leave the annex and become normative in v1.1

Ruling: "For the v1.1 spec I would think we will want to move Bulk issuance from the annex so as to be normative." And: "But yes lets make the language normative." Comment https://github.com/trustoverip/kswg-acdc-specification/pull/204#issuecomment-5273991502, created and updated 2026-08-12T23:27:46Z.

Cross-check against the ACDC spec: not carried. At `v1.1` @`2362e48a1`, `### Bulk-issued Private ACDCs` is at L2966, under `## Annex` at L2898, as on `main` (L2765). The status question this settles matters to every bulk-issuance MUST in the spec: until the move, those MUSTs sit in an annex whose normative status neither branch declares (dhh1128's question on PR #204). Not in the bible. Belongs in `bible/05` §bulk issuance as a status note.

### R-046 The `u` field term is "unique entropy", not UUID

Ruling: "UUID has baggage so we retain "u" but change the term to unique entropy" Comment https://github.com/trustoverip/kswg-acdc-specification/issues/191#issuecomment-4928770228, created and updated 2026-07-09T19:26:41Z.

Cross-check: carried into `v1.1` only. `v1.1` @`2362e48a1` L98 is `### Unique Entropy (UE) Fields`; `main` @`f0bd097de` L87 is still `### Universally Unique Identifier (UUID) Fields`. Already in the bible at `bible/05-acdc-and-verifiable-data.md:44`.

### R-047 SEDI's architecture: an IAL3 management ACDC, then per-disclosee bulk-issued credentials

Ruling: "the proposed architecture for SEDI is the the IAL3 identity assurance process issues a SEDI management ACDC." And: "The SEDI management ACDC is only used in one context and that is to request bulk issued SEDI credentials." Comment https://github.com/WebOfTrust/keripy/issues/1532#issuecomment-5061387439, created and updated 2026-07-23T17:26:31Z. And: "a simple rule of don't reuse a bulk issued aid unless its with the same disclosee".

Cross-check: `[P]`, Sam's proposal for a state program, not a spec matter. Not in the bible or in `scenarios/utah-sedi-age-residency.md` as far as a grep for "management ACDC" shows. Belongs in `bible/06` §SEDI and the SEDI scenario.

### R-048 Unlinkable ZKPs are precluded because they defeat detectability

Already in the bible at `bible/07-shibboleths-and-anti-patterns.md:388`, :499, `bible/05-acdc-and-verifiable-data.md:76` and `bible/10-presentation-registries.md:40`, from the #1098 body (created 2025-10-27T23:37:01Z, last edited 2026-09-26 per the API). Not re-mined. One sentence the bible does not carry, from the same body: "The disease is the use of shared secrets for authentication, and KERI cures that disease." It is Sam's framing of why birthdate privacy is a symptom, and belongs beside `bible/07:388` as his assessment.

---

## 7. IPEX and presentation

### R-049 An agree binds; an admit only removes the easy defense

Ruling: "An agree is legally binding not sending an admit does not convey backing out." And: "The admit is a corner case that enables easy enforcement by removing plausible deniablity." Comment https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4997904242, created 2026-07-17T00:49:04Z, updated 2026-07-17T01:52:59Z.

The balancing mechanism, same comment: "The grantor gets an escape clause unless the admitter verifiably admits." And the link to regulation: "So CLC and DDL are mutually reinforcing." (DDL is the duty of data loyalty.)

Question settled: whether a disclosee who never admits a grant is released from the terms it agreed. No.

Cross-check: `bible/08-presentation-architectures-and-ipex.md:271` quotes #1613 that anchoring `admit` "removes plausible deniability". The rulings that the agree is the binding act, that a missing admit is not a withdrawal, and that the grantor's escape clause is what incentivizes the admit are missing. Belongs in `bible/08` §9 and `bible/06` §contractually protected disclosure.

### R-050 Anchoring the tail of an exchange anchors the whole of it

Ruling: "What we are anchoring is the tail of the transaction not the head." And: "anchoring the tail also anchors the whole transation including the head." Comment https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4996894599, created 2026-07-16T21:47:01Z, updated 2026-07-16T22:21:19Z. The reason given is that the events of an exchange transaction are hash-chained. And: "Multiple anchors are not meant to anchor multiple transactions but as continencies for the transaction to proceed." ("continencies" means contingencies.)

The same comment gives the sequence-of-commitments argument for apply-offer-agree-grant-admit without a trusted third party: "So the Offer/Agree/Grant/Admit removes plausible deniability which is the bane of peer-to-peer interactions."

Cross-check: not in the bible. Belongs in `bible/08` §9 as the reason multiple anchors in one IPEX are contingencies rather than redundancy.

### R-051 An unsolicited grant may be spurned

Ruling: "I agree. an unsolicited grant i.e using a xip message should be spurnable. that is nuance i did not anticipate." Comment https://github.com/WebOfTrust/keripy/issues/1628#issuecomment-5349282926, created 2026-08-19T23:35:12Z, updated 2026-08-19T23:49:09Z.

Question settled: issue #1628 notes that #1517 had removed `grant` from the routes a `spurn` can answer, on Sam's earlier reasoning that a grant after an agree cannot be taken back. That reasoning is kept for a grant that answers an agree; a flow-starting grant, which nobody agreed to, may be refused.

Cross-check against the ACDC spec: not carried. The `v1.1` route table (L2005-2009) lists `spurn` as rejecting `apply`, `offer` and `agree`, with no row for `grant`, on both branches. `[K]` keripy `80f77b73b` agrees with Sam: `src/keri/acdc/ipexing.py` L761 rejects a spurn whose prior is a grant only when that grant has a prior (`if verb == Ipex.spurn and pverb == Ipex.grant and pserder.ked.get("p", ""):`), and the builder at L2120-2121 raises "only flow-starting grants may be spurned". The bible states the opposite of the code: see T-01, the most consequential finding of this pass.

### R-052 An empty `dp` copies the prior plan; with no prior it asks for nothing

Ruling: "An empty [] for dp field means ditto the prior dp field from the apply or offer not give me everything." And: "If there is no prior message then an empty [] means give me nothing. To get everything their must be a path." Comment https://github.com/WebOfTrust/keripy/pull/1698#issuecomment-5937132701, created 2026-10-01T17:47:09Z, updated 2026-10-01T17:49:39Z.

This refines Sam's own earlier text. The #1549 body (created 2026-07-25, edited 2026-08-04) said: "When the `offer` is different or is unsolicited, then the `dp` field value must not be an empty list."

Cross-check against the ACDC spec: contradicted. `v1.1` @`2362e48a1` L1917: "Where the answering list differs, or where the message is unsolicited, the `dp` value MUST NOT be an empty list." `[K]` keripy upstream head `c102367ea` (read via the GitHub API; PR #1698 merged 2026-10-08, after the `80f77b73b` pin) implements Sam's version: "An empty plan inherits from a prior message and means no disclosure" when the message opens a thread (`src/keri/acdc/ipexing.py` L513-514 at `c102367ea`), and it now validates `dp` on `agree` and `grant` as well as `apply` and `offer` (L515-519). See T-02.

### R-053 An offer's `o` is the origin SAID of a metadata-ACDC DAG

Ruling: "The offer `o` is just the SAID of the Metadata ACDC DAG origin. The actual metadata ACDCs are attached in a substream." Review comment https://github.com/WebOfTrust/keripy/pull/1629#discussion_r3832392219, created 2026-08-21T17:40:24Z, updated 2026-08-21T17:41:58Z.

The reason, same comment: the metadata ACDC discloses the rule section but not the attributes, so "the only way for the agreent to know what it is agreeing to is for it to see the metadata ACDC DAG". An earlier review on the same PR set the requirement: "The offer message also needs to have an origin `o` field to replace the ACDC field." (https://github.com/WebOfTrust/keripy/pull/1629#pullrequestreview-4987948288, submitted 2026-08-20T22:17:34Z.)

Cross-check: not in either ACDC branch. `bible/08` describes `o` on the `grant` (§9, §12 row "Origin `o` field in `grant`") but not on the `offer`. Belongs in `bible/08` §9 and the §12 matrix.

### R-054 The receiver AID is never empty; participation is not correlation

Ruling: "The `ri` field is meant to carry the receiver AID." And: "Proof of participation is not the same as correlation." Comment https://github.com/WebOfTrust/keripy/discussions/1542#discussioncomment-17755467, created 2026-07-23T19:02:51Z, updated 2026-07-23T19:29:10Z.

The argument, same comment: an authenticated negotiation needs a pair of AIDs; the verifier can correlate on the presenter's negotiating AID but "can't prove it is the same as the Issuee until the Grant"; and contract law needs "a clear intent to engage in legal relations", which needs identity. So the negotiating AID's exposure is the price of a binding contract, and graduated disclosure governs only the ACDC content.

Cross-check: not in the bible. Belongs in `bible/08` §6 (authentication factors) and `bible/06` §4 (correlation as layered).

### R-055 Predefined DAG shapes are the norm; freeform exchanges are impractical

Ruling: "In my experience totally free-form credential exchanges are largely impractical." And: "So predefined shapes will be the norm." Comment https://github.com/WebOfTrust/keripy/discussions/1542#discussioncomment-17842586, created 2026-07-30T16:25:08Z, updated 2026-07-30T18:04:23Z. Also: "The current spec is very unrestrictive. This is because hardening means having an opinion, and I didn't have a strong opinion." (same comment).

From the comment before it, on an offer whose origin schema differs from the apply's: "it is functionally the same as if the Offerer spurned the apply and then initiated a new IPEX with an unsolicited offer." (https://github.com/WebOfTrust/keripy/discussions/1542#discussioncomment-17841472, created 2026-07-30T14:38:11Z, updated 2026-07-30T21:52:03Z.) And: "A valid IPEX can start on the Offerer side with an offer or a grant. It does not have to start with an apply."

Cross-check against the ACDC spec: partly carried. `v1.1` @`2362e48a1` L1903 says "in practice the requester defines the shape of the DAG it will accept", which is the first half. The rule that an offer with a different origin schema is a spurn plus a new offer is not there. Not in the bible as a design principle. Belongs in `bible/08` §4 and `bible/06` (EGF-defined shapes as the interoperability mechanism).

### R-056 `dp` belongs in ACDC v1.1 for now; IPEX will likely become its own spec

Ruling: "I think we add it to the ACDC v1.1 spec draft." And: "IPEX probably gets its own spec." Comment https://github.com/WebOfTrust/keripy/discussions/1542#discussioncomment-17841472 (as R-055).

Cross-check: the first half is done (`dp` is `[N1.1]`, `bible/08:78`). The forecast that IPEX splits into a separate specification at an IETF working group is not in the bible and bears on `bible/08` §13 open question 15 (dp's syntax is normative while its only binding sits in a non-normative IPEX section).

### R-057 Only v2 exchanges will be anchored

Ruling: "Its only with v2 exchange messages that we plan to anchor exchanges. We really don't want to be anchoring v1 exchanges." Comment https://github.com/WebOfTrust/keripy/pull/1492#issuecomment-5093267019, created and updated 2026-07-27T15:25:30Z.

Cross-check: consistent with `[K]`: anchoring (`ax`) exists only in the V2 module (`bible/08:259`). The policy statement, that v1 exchanges will never be anchored and production branches must upgrade, is missing and belongs in `bible/08` §5a.

### R-058 Disclosure reasons about exposure, not meaning; schema is type only

Ruling: "So disclosure is reasoning about exposure. What parts to expose when. Not what those parts mean." Comment https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4992746261 (as R-027). Restated in the #1512 body: "One of the prime motivations for ACDCs was to invert that layering." And the dismissal of the alternative: "I found the W3C approach of attempting to bolt on security to RDF graph expansions a pathological mess (excuse my strong language)." (#1512 body.)

Cross-check: the bible has "schema is type" in several places but not this layering argument for why disclosure requests are paths over a graph rather than schema decompositions. Belongs in `bible/01` (worldview: security layers below semantic layers) and `bible/08` §4 as the rationale for `dp`.

### R-059 Closure rules differ by section and must extend to edges and rules

Ruling: "We need to extend that to the Edge and Rule sections." Comment https://github.com/WebOfTrust/keripy/discussions/1512#discussioncomment-17666795, created and updated 2026-07-16T22:48:39Z. The motivating case, same comment: blinded rule-section terms "in domestic abuse situations where the legally enforceable terms would leak sensitive information".

Cross-check: `v1.1` @`2362e48a1` defines closures for the partially disclosable sections including Edge and Rule (`bible/08:94`). Carried. The domestic-abuse motivation for blinded rules is not in the bible; it is a useful concrete case for `bible/05` §rules.

### R-060 Nested partial disclosure inside a selectively disclosed block is an anti-pattern

Ruling: "But such a partially disclosable subblock is an anti-pattern for using selective disclosure, as we are mixing partial disclosure inside a selectively disclosed array." Reply https://github.com/WebOfTrust/keripy/discussions/1549#discussioncomment-17991999, created 2026-08-12T17:47:13Z, updated 2026-08-12T19:04:11Z.

Cross-check: carried into `v1.1` and already in the bible at `bible/08-presentation-architectures-and-ipex.md:106` ("partial disclosure inside selective disclosure is an anti-pattern"). Listed for completeness.

### R-061 The `dp` design history, settled in v1.1

Already in the bible in full at `bible/08` §4 (`bible/08:78-106`): `disclose` renamed `dp`, dictionary replaced by a list of tuples so a schema SAID may repeat (#1512 comment of 2026-07-21; #1542 comment of 2026-07-23), breadth-first ordering with the origin first, `/` for DAG-absolute paths, `_` as the virtual edge hop (approved at the developers' meeting, #1549 comment of 2026-08-04), the `(ssaid, prefix, paths)` triple (#1549 comment of 2026-08-04), and the whole-ACDC forms (#1549 reply of 2026-08-12). Not re-mined. Two superseded intermediate forms are worth recording because they appear in quotable bodies: the #1512 reply of 2026-07-24 wrote edge-traversal paths through the `n` field (`/e/accreditation/n/a/i`), which #1549 replaced (the `n` label is not a path component), and #1549's first body used two-element tuples.

### R-062 Four tiers of IPEX, from signed-only to anchored-with-registry

Ruling (diagram captions): "Only the granted ACDC is itself perpetually verifiable, Not the IPEX transaction" for the low-stakes signed-only tier, and for the high tier: "The Agree, and Admit exchange messages are anchored by the Disclosee. The Grant is anchored by the Discloser." Comment https://github.com/WebOfTrust/keripy/discussions/1512#discussioncomment-17737728, created 2026-07-22T16:20:10Z, updated 2026-07-22T17:13:08Z.

Cross-check: the anchoring rules are in `bible/08` §9 from #1613, which came later. The four-tier taxonomy as a decision aid (low-stakes, low-stakes plus presentation registry, high-stakes anchored, high-stakes anchored plus registry) is not. Belongs in `bible/08` §9 or `bible/10`.

### R-063 Constructors, not schemas, should stop a premature leak in apply and offer

Ruling: "Schemas are not rich enough by design to handle all those." And: "using contructors that limit what gets put there for sensitive message that want to avoid inadvertent leakage is an easy fix." Comment https://github.com/WebOfTrust/keripy/issues/1532#issuecomment-5052264212, created 2026-07-22T22:28:38Z, updated 2026-07-22T23:21:13Z.

Then: "each type of use case needs a specific workflow that defines by construction what is disclosed at what stage." And: "There is no universal set of rules." (https://github.com/WebOfTrust/keripy/issues/1532#issuecomment-5058749739, created 2026-07-23T13:08:08Z, updated 2026-07-23T13:35:20Z.)

Cross-check: not in the bible. It is Sam's answer to whether the protocol should guarantee that apply and offer leak nothing: no, that is EGF-defined workflow, enforced by construction in tooling. Belongs in `bible/08` §13 as the editor's position on open question 12's neighbor, and in `bible/06` (EGF as the business-logic umbrella).

### R-064 Human-readable purpose belongs in the rule section, not in an exchange `m` field

Ruling: "But I am always worried when we do stuff like that , that we are not following the design ethos of minimally sufficient means." And: "The advantage of putting it in the DAG is that it gets all the security, perpetuality, etc of the DAG". Comment https://github.com/WebOfTrust/keripy/discussions/1617#discussioncomment-18006490, created 2026-08-13T19:03:46Z, updated 2026-08-13T19:04:28Z.

Status: not a ruling for removal. Phil Feairheller replied that Locksmith uses `m`; Sam asked whether it reaches the UX and did not decide. Recorded as Sam's stated preference only.

Cross-check: not in the bible. Belongs in `bible/08` as a note on the `m` field's open status.

### R-065 Unlinkability is not uncorrelatability; the achievable goal is decorrelation

Ruling: "So the viable goal can not be uncorrelatability it must be decorrelation." Comment https://github.com/WebOfTrust/keripy/discussions/1515#discussioncomment-17682212, created 2026-07-18T16:57:51Z, updated 2026-07-18T18:00:04Z. And on why bulk issuance is still worth doing against a super-correlator: "One cogent reason to use bulk issuance despite its eventual defeat by a super correlator (an AI) is that partitioning identifier sets makes enforcement easier." (same comment).

Cross-check: the layered view is in the bible (`bible/06-governance-ecosystems-and-interop.md:59-73`; `keri-doctrine.md:53`, claim 11). The term "decorrelation" for functional non-exploitation, and the enforcement argument for bulk issuance, are not (two hits for "decorrelat" in the bible, neither this). `raw/17` covers the SPAC privacy material. Belongs in `bible/06` §4.

### R-066 Standing edges are a correlation point; bulk issuance and blinded edges answer it

Ruling: "With bulk issuance, each presentation context consisting of discloser and disclosee gets its own set of SEDI credentials and standing edges." Comment https://github.com/WebOfTrust/keripy/discussions/1515#discussioncomment-17681089, created 2026-07-18T13:20:03Z, updated 2026-07-18T13:22:49Z. And: "an edge can also be blinded, which means that disclosure of the edge itself can be held back" until the disclosee has agreed not to exploit it (https://github.com/WebOfTrust/keripy/discussions/1515#discussioncomment-17682012, created 2026-07-18T16:13:32Z, updated 2026-07-18T16:17:56Z).

Cross-check: `bible/05` has standing edges and blinding separately; the pairing as the answer to standing-edge correlation is missing. Belongs in `bible/05` §5.

### R-067 A multiply-endorsed presentation lives on the grant

Already in the bible at `bible/08-presentation-architectures-and-ipex.md:227-245`, from the #1555 body (created 2026-07-29T21:03:22Z) and #1613. Not re-mined.

### R-068 What an offer's `ax` asks for

Already in the bible at `bible/08-presentation-architectures-and-ipex.md:299`, from the #1627 comment of 2026-09-02 (https://github.com/WebOfTrust/keripy/discussions/1627#discussioncomment-18254506). Not re-mined.

---

## 8. KRAM

### R-069 The human-agreement multisig protocol (HAMI) is obsolete; KRAM replaces it

Ruling: "Obsoleted by new multisig KRAM design" Comment https://github.com/WebOfTrust/keripy/issues/911#issuecomment-3930371630, created and updated 2026-02-19T21:59:36Z. Companion: "See new kram design" on the KRAM implementation issue (https://github.com/WebOfTrust/keripy/issues/937#issuecomment-3930374154, 2026-02-19T22:00:12Z).

Cross-check: `bible/09` cites #911 and #937 (per the reference index). The supersession is recorded in `raw/15`; not re-mined. The #1555 body states the replacement mechanism: the receiver's KRAM escrow collects multisig signatures, "without requiring a pre-protocol to collect signatures", already quoted at `bible/08:192`.

### R-070 Log every key-state retrieval cue

Ruling: "Whenever you create a cue to get keystate, also do a logger.info so that someone watching the logs can do analytics on missing keystate." Review https://github.com/WebOfTrust/keripy/pull/1323#pullrequestreview-3939540930, submitted 2026-03-12T20:27:32Z.

Cross-check: an operational rule for KRAM implementations. Not in the bible; belongs in the infrastructure chapter if anywhere.

---

## 9. Agents, wallets and guardianship

### R-071 A parent's control over a child's social-media access needs no key-management trick

Ruling: "the minimally sufficient means for the parent to have control over the childs access to social media." Comment https://github.com/WebOfTrust/keripy/discussions/1573#discussioncomment-17935861, created 2026-08-07T16:23:16Z, updated 2026-08-07T16:44:25Z. "The last case" is the fifth of five key-management arrangements he lists (parent holds rotation keys; parent signs for the child; shared multisig pre-rotation; child as delegated AID; child holds everything), in which the social network accepts the authorization only from the parent's AID.

And on policy: "policy may reach down to the key management layer of the Issuee (citizen) not merely the Issuer (State)." (https://github.com/WebOfTrust/keripy/discussions/1573#discussioncomment-17935891, created 2026-08-07T16:26:14Z, updated 2026-08-07T17:11:04Z.) He calls this "unprecedented" and leaves the emancipation ceremony open.

Cross-check: not in the bible. `raw/19` covers guardianship from the EVAC material. Belongs in `bible/03` §custody (the five arrangements) and `bible/06` §SEDI guardianship.

### R-072 A child's identity starts in the parent's custody

Ruling: "So if the State issued a SEDI to the Baby they are issuing it to an AID controlled by the parents not the Baby." Discussion body https://github.com/WebOfTrust/keripy/discussions/1550, created 2026-07-28T20:09:10Z, last edited 2026-07-28T23:43:06Z. The body labels its diagrams "notional arrangements for discussion and do not reflect any as yet to be specified State of Utah policy", so this is a modeling position, not policy.

Also in the body: guardianship credentials model a ward with "a limited set of citizen rights, which rights are held by their parents and must be delegated back to their child", and "no one single set of ACDCs is likely to fit them all." The EVAC white paper the body points to is unpublished ("I started an EVAC white paper but have yet to publish it.", #1550 comment of R-034).

Cross-check: `bible/08` cites #1550 for ward and guardian authorization; the custody-from-birth position is not recorded. Belongs in `bible/06` §SEDI guardianship.

---

## 10. Process and versioning

### R-073 A pull request's author must read every AI-generated change

Ruling: "You need to personally read every change made by an AI tool to verify that it makes sense." Comment https://github.com/WebOfTrust/keripy/pull/1401#issuecomment-4390509469, created and updated 2026-05-06T17:35:07Z. Context: a docs PR whose AI tooling had changed code ("Changes that fix doc strings should never change actual code.").

Then on PR #1564: "this is the second issue that feels like halluciantion. As a result I am not going to rewspond to any more issues created by A.I" (https://github.com/WebOfTrust/keripy/pull/1564#issuecomment-5220496025, created and updated 2026-08-07T18:08:49Z). And the stated principle: "Somewhere some human has to be the quality control on the AI. The AI by construction can't be." (https://github.com/WebOfTrust/keripy/pull/1564#issuecomment-5220803176, created 2026-08-07T18:43:36Z, updated 2026-08-07T19:01:24Z.) And on discussion #1573: "I really don't like waisting time answering halluciantions" (https://github.com/WebOfTrust/keripy/discussions/1573#discussioncomment-17936454, created and updated 2026-08-07T17:25:16Z).

This is a process ruling, not doctrine, and it has a corpus consequence: the next refresh should expect fewer and shorter Sam rulings on AI-drafted threads, and a question raised upstream should be raised in the human's own words.

### R-074 Examples come in layers, from bare data structures up

Ruling: "Having layered examples also helps implementers in other languages as they want to see the bare bones." Comment https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4981932724 (as R-025). Also: "One of the reason to do these examples is to force exploring the tradespace in a concrete way." (#1505 comment of 2026-07-16T13:57:05Z.)

Cross-check: a method statement about worked examples as design tools. Not in the bible; relevant to `scenarios/` and `field/` conventions.

### R-075 Specification merges need a qualified reviewer

Ruling: "Kor should not be merging these pull requests. He is not a reviewer for this." Comment https://github.com/trustoverip/kswg-cesr-specification/issues/175#issuecomment-5496504739, created and updated 2026-09-01T15:42:01Z.

Cross-check: process. It explains why PR #165's merge into CESR `v1.1` preceded the Ed448 fix Sam wanted first (R-020).

### R-076 The normative spec URLs moved with the working group

Ruling: "I suggest that GLEIF should at least update their current published links to reflect the now permanent URLs." Comment https://github.com/trustoverip/kswg-keri-specification/issues/274#issuecomment-3543733832, created and updated 2025-11-17T20:35:54Z.

Cross-check: the `tswg-*` GitHub Pages URLs no longer resolve; the `kswg-*` ones are permanent. Relevant to the bible's source citations: any `tswg-` URL in the corpus is dead. A grep of `bible/` and `raw/` for `tswg-` was not run for this note.

### R-077 Do not hide call parameters behind packing indirection

Ruling: "a custom property was created which obscures the call parameters making it hard to read the code." Issue body https://github.com/WebOfTrust/keripy/issues/1488, created 2026-07-11T20:38:30Z, updated 2026-07-11T20:39:59Z. Same rule in issue #1485 and the "anti pattern for packing" paragraph of https://github.com/WebOfTrust/keripy/pull/1481#issuecomment-4926709614 (created 2026-07-09T15:20:11Z, updated 2026-07-09T15:45:37Z).

Cross-check: keripy code style, not doctrine. Recorded for anyone contributing upstream. Not for the bible.

### R-078 ACDC v2 support lives in a new `acdc` subpackage beside v1's `vc`

Ruling: "This provides a place to support the new features in acdc v2 while leaving support for acdc v1 in the vc subpackage." PR body https://github.com/WebOfTrust/keripy/pull/1170, created 2026-02-04T21:11:58Z, updated 2026-02-04T22:08:02Z.

Cross-check: this is the origin of the V1/V2 split `bible/08-presentation-architectures-and-ipex.md:154` (§5a) documents under the heading "Two IPEX state machines, and only one of them runs". The bible does not say the split was deliberate from February. Belongs in `bible/08` §5a as one sentence.

---

## 11. Rulings later reversed or corrected by Sam himself

- R-015, `DI2I` depth: children only (2026-07-30) reversed to all the way down (2026-08-02).
- R-027, SEDI core identity credential: aggregate (2026-07-15) reversed to attributive (2026-07-16). The #1512 body was never updated and still carries the first answer.
- R-052, empty `dp` on an unsolicited message: "must not be an empty list" (#1549 body, July) refined to "means give me nothing" (2026-10-01). The `v1.1` spec text follows the first version.
- R-003, KRAM `tsg` currency: a paragraph allowing a later interaction event (2026-09-02T18:19) withdrawn for signature groups the same afternoon (#1667).
- R-037, registry transfer: named `rxr` (2026-04-23), renamed `xfr` (2026-07-30).
- R-029, the worked example's edge operator: `I2I` endorsed (2026-07-15, "The operator I2I is meant to work for either att or agg ACDCs") then ruled misapplied (2026-07-17).
- R-061, `dp` syntax: `disclose` to `dp`; dictionary to list of tuples; edge paths through `n` to the `_` hop; two-tuples to three-tuples. All already recorded in `bible/08` §4.
- R-033, the identity and equivalence operator family: proposed whole (2026-07-17), narrowed to `E1E` (2026-07-18), `I1I` and `DI1I` revived with a use case (2026-10-01). Recorded in `bible/08:144-146`.
- keripy `Suber` counting (#1362 reviews of 2026-03-25): "Ok I changed my mind." on `cnt` versus `cntAll`. Internal; noted only so a reader of that PR knows the last review is the ruling.

---

## 12. Contradictions and tensions

### T-01 The bible inverts keripy's spurn-of-grant rule, and the code follows Sam

`bible/08-presentation-architectures-and-ipex.md:164` says V2 adds "a refusal to spurn a thread-opening grant", and `raw/09-keripy-code.md:207` says "a spurn of a thread-opening grant is rejected". The code at `80f77b73b` (`src/keri/acdc/ipexing.py` L761) rejects the spurn only when the spurned grant carries a non-empty `p`, that is, when it is not thread-opening; the builder (L2120-2121) raises "only flow-starting grants may be spurned". So keripy permits spurning exactly the grants the bible says it refuses, and refuses the ones the bible implies it permits. The code's rule is Sam's ruling R-051 (2026-08-19). Neither ACDC branch lists `spurn` as answering a `grant` at all (`v1.1` L2005-2009), so the spec is silent on the case both Sam and the code allow. Fix `bible/08:164` and `raw/09:207`; add the spec gap to `bible/08` §13.

### T-02 Empty `dp` on an unsolicited message: spec forbids it, Sam and the code give it a meaning

`v1.1` @`2362e48a1` L1917 says an unsolicited message's `dp` "MUST NOT be an empty list". Sam (R-052, 2026-10-01) says an empty list with no prior "means give me nothing", and keripy at `c102367ea` implements that. The spec text follows Sam's own July wording, so the spec lags the editor. A second divergence rides with it: at `c102367ea` keripy validates `dp` on `agree` and `grant`, while `v1.1` (and `bible/08:100`, "`dp` appears in `apply` and `offer` only. It does not appear in a `grant`") place it in `apply` and `offer` only. Sam's ruling text ("ditto the prior dp field from the apply or offer") presupposes a `dp` on a later message, which supports the code. `bible/08:100` is correct about `v1.1` and stale about keripy.

### T-03 `upd` is deprecated by the editor and still defined in v1.1

Sam (R-036, 2026-07-30 and 2026-08-11) deprecates `upd` and says support drops in v1.1. `v1.1` @`2362e48a1` L2161 and L2194 still define it, identically to `main`. keripy's V2 registry processing supports only `rip` and `bup` (`regeventing.py` L121) while `messaging.py` L80-104 still builds `upd`. The spec is the stale party.

### T-04 `xfr` is approved for v1.1 and absent from it

Sam (R-037, 2026-07-31) reports community approval and a plan to add `xfr` to ACDC v1.1. Neither branch has it, and keripy has no `xfr` or `rxr`. Not a contradiction of text, but a stated intent the spec has not met; `raw/19` §4.3 records the same absence.

### T-05 The empty-operator default: decided to change in v1.1, unchanged in v1.1

Sam (R-030, 2026-08-12) records a maintainer-call decision that the empty-operator default becomes `NI2I` in v1.1, with a version switch for older ACDCs. `v1.1` @`2362e48a1` L1209-1213 keeps the `I2I`-if-targeted rule. keripy's two modules disagree with each other on the absent-`o` case already (`bible/08:140`), so the decision, once landed, would align the spec with `acdc/ipexing.py`'s no-default behavior for targeted far nodes only if the switch is implemented as Sam describes.

### T-06 Bulk issuance: to be normative in v1.1, still in the annex

Sam (R-045, 2026-08-12): "lets make the language normative." `v1.1` @`2362e48a1` keeps `### Bulk-issued Private ACDCs` (L2966) under `## Annex` (L2898). Every MUST in that section therefore has the unclear status dhh1128 asked about, including the two that did land (`k.` and the qb64/Blake3 pin, R-043).

### T-07 The aggregate issuee position is intended, not specified

Sam (R-025) says the aggregate issuee is the `i` of index 1 and that the spec should say so. Neither branch does; the `v1.1` example happens to place it there (L920-924). keripy reads `A[1].i` (`bible/05:74`). The bible's Finding 2 is right that nothing enforces the position; the ruling settles which way the gap should close.

### T-08 TEL anchor storage: "does not clobber" versus keep-earliest-by-sequence

Sam (R-038): a new anchor "does not clobber a previously verified anchor". keripy `registering.py` L58-64 (at `80f77b73b` and `c102367ea`) replaces a stored anchor when a newly verified one has a lower sealing sequence number, using `pin`. That is a different rule: first-verified versus earliest-in-the-KEL. For a TEL event sealed twice in one KEL, the two rules pick different anchors when the later seal is verified first. Whether that case can arise in practice was not tested.

### T-09 What `I2I` means: delegation, or same-holder binding

Sam frames `I2I` throughout the window as delegative: "the number `2` is used to symbolize delegation" (#1515 body) and, in the worked example, an identity relation was a misuse of it (R-029). `bible/07-shibboleths-and-anti-patterns.md:428` and `keri-doctrine.md:103` call `I2I`'s real meaning "same-holder binding". Both readings compute the same check (near issuer equals far issuee), and dhh1128 pressed exactly this point on #1515 (reply of 2026-07-18). Sam's answer there is that the operator's presence triggers validation at the edge layer and its delegative meaning is what the chain-of-authority builds from it. The bible's phrasing is not wrong about the computation and is at odds with the editor's stated semantics. The shibboleth row should say both.

### T-10 `DID` placement: settled by the editor, still wrong in `main`'s example

R-012. `main` @`fbdd4a615` L591 places `DID` in Ean's plain `icp`; Sam calls that "an oversight"; `v1.1` fixes it. `bible/03:126` currently declines to call `main` wrong for want of a source. It now has one.

### T-11 Ed448's seed code: the editor wanted it fixed first, and it was not

R-020. Sam preferred fixing the 56-byte `K` seed code before the post-quantum codes landed; the PQ codes merged into CESR `v1.1` and `K` is unchanged on both branches. Issue #175 is open, so the defect is acknowledged and unfixed.

### T-12 The #1512 body contradicts its author

R-027. The never-edited #1512 body recommends the aggregate form for the SEDI core identity credential, which Sam withdrew on #1505 before #1512 was posted the same afternoon (#1505 reversal at 13:00 UTC, #1512 body at 15:44 UTC, copied from his earlier #1505 text). Anyone citing #1512 for the aggregate choice is citing a retracted position.

---

## 13. Already in the bible

These rulings are stated, with the same substance, at the locations given. Line numbers are at the worktree's current text.

- R-003 KRAM currency against `lastEst`: `bible/09-kram-and-request-authentication.md:88`, :137.
- R-004 non-transferability by empty next-key list: `bible/03-key-management-and-identifier-lifecycle.md:47`.
- R-005 delegated superseding recovery rules: `bible/03-key-management-and-identifier-lifecycle.md:146-152`.
- R-008 witness is not a watcher: `bible/02-security-model-and-threat-posture.md:171`; `bible/07-shibboleths-and-anti-patterns.md:308`.
- R-012 `DID` placement in a `dip` (from the spec, not the ruling): `bible/03-key-management-and-identifier-lifecycle.md:122`; `bible/07-shibboleths-and-anti-patterns.md:312`.
- R-014 `DND` drops delegated events: `bible/03-key-management-and-identifier-lifecycle.md:120` (spec rule).
- R-015 `DI2I` exists and fails closed in keripy: `bible/08-presentation-architectures-and-ipex.md:122`, :128.
- R-025 keripy reads the aggregate issuee from `A[1]`: `bible/05-acdc-and-verifiable-data.md:74`.
- R-027 attribute versus aggregate choice for SEDI, and age as the aggregate case: `bible/05-acdc-and-verifiable-data.md:58-62`.
- R-028 edge `s` enforced with "satisfy" semantics: `bible/08-presentation-architectures-and-ipex.md:128`.
- R-029, R-032, R-033 `E1E`, `I1I`, `DI1I` lineage: `bible/08-presentation-architectures-and-ipex.md:122`, :144, :146.
- R-046 unique entropy: `bible/05-acdc-and-verifiable-data.md:44`.
- R-048 ZKPs precluded by detectability: `bible/07-shibboleths-and-anti-patterns.md:388`, :499; `bible/05-acdc-and-verifiable-data.md:76`; `bible/10-presentation-registries.md:40`.
- R-059 closures over Edge and Rule sections: `bible/08-presentation-architectures-and-ipex.md:94`.
- R-060 nested partial inside selective is an anti-pattern: `bible/08-presentation-architectures-and-ipex.md:106`.
- R-061 the whole `dp` design: `bible/08-presentation-architectures-and-ipex.md:78-106`.
- R-067 multiply-endorsed presentation: `bible/08-presentation-architectures-and-ipex.md:227-245`.
- R-068 `ax` in an offer: `bible/08-presentation-architectures-and-ipex.md:299`.
- R-069 KRAM escrow collects multisig signatures: `bible/08-presentation-architectures-and-ipex.md:192`.
- Group-scoped operator defaults and `IAND` (#1556): `bible/08-presentation-architectures-and-ipex.md:229`.
- The QVI horizontal-scaling origin of `DI2I` and `DID` (#1515 comment of 2026-07-18): `bible/08-presentation-architectures-and-ipex.md:130`.

From the threads `raw/15` and `raw/16` own (#1095, #1515, #1613, #1618, #1627, KRAM), the rulings the bible lacks are: R-033's addition (same AID implies same controller and key state), R-065 and R-066 (decorrelation; bulk issuance and blinded edges against standing-edge correlation), all from #1515 comments; and from #1095's body, the explicit rejection of weak holder binding (R-026). #1613, #1618 and #1627 are fully reflected in `bible/08` and `bible/10` as far as rulings go.

---

## 14. Missing from the bible, ranked by importance

Ranked by how likely the absence is to make a reader build the wrong thing, then by how settled the ruling is.

1. T-01 / R-051, the spurn-of-grant inversion in `bible/08:164` and `raw/09:207`. The bible currently misstates the reference implementation, and the misstatement points opposite to the editor's ruling. Chapter `bible/08` §5a and §13.
2. R-015, `DI2I` reaches any depth, with `DND`/`DID` as the depth control, and the reversal. The spec text supports the narrower reading Sam withdrew. Chapters `bible/05` §5 and `bible/03` §delegation.
3. R-030 / T-05, the empty-operator default changes to `NI2I` for v1.1 ACDCs behind a version switch. It changes the meaning of every operator-less edge. Chapters `bible/05` §5, `bible/08` §5.
4. R-052 / T-02, empty `dp` semantics and `dp` on `agree`/`grant` in keripy; the `v1.1` text lags. Chapter `bible/08` §4 and §12.
5. R-036 / T-03, `upd` deprecated while `v1.1` still defines it. Chapter `bible/05` §registries.
6. R-012 / T-10, the Ean `DID` example is an oversight; resolves `bible/03:126` and `bible/07:312`. Chapter `bible/03` §8.
7. R-042, issuer revocation is universal across a bulk set; key compromise is answered by rotation, not revocation; salt compromise abandons the set. Chapter `bible/05` §bulk issuance, plus a `bible/07` shibboleth.
8. R-040, R-044, R-045, R-043, the bulk-issuance cluster: decorrelated pre-created registries as SEDI's chosen case, the registry blinding-salt path left open, the annex-to-normative move, and the one part that landed in `main` (`k.`, qb64 concatenation, Blake3-256). Chapter `bible/05` §bulk issuance; a new subsection is warranted.
9. R-049 and R-050, the contractual logic of IPEX: agree binds, admit removes deniability, the grantor's escape clause, tail anchoring, multiple anchors as contingencies. Chapters `bible/08` §9 and `bible/06` §contractually protected disclosure.
10. R-025 / T-07, the aggregate issuee is intended at index 1. Chapter `bible/05` §4.1 (amend Finding 2).
11. R-002 and R-022, version rules on the wire: KEL events never upgrade, attachments follow the receiving parser, v2 attaches nested substreams instead of embedding, v1-only parsers are a dead end. Chapter `bible/04`.
12. R-008's deployment half: witnesses used as watchers in production, and the "eyes of a watcher" rule. Chapters `bible/02` and the proposed infrastructure chapter.
13. R-037, registry transfer (`rxr` then `xfr`, doubly anchored, approved) and reversion of authority. Chapter `bible/05` §registries or the proposed authorization chapter (with `raw/19`).
14. R-055, R-054, R-063, R-057, the IPEX design posture: predefined DAG shapes, receiver AID always present and participation not correlation, constructors not schemas against premature leaks, v2-only anchoring. Chapter `bible/08`, with `bible/06` for the EGF angle.
15. R-019, R-017, R-018, R-020, CESR code-table doctrine: codes encode encoding not usage, fixed codes cost at most two bytes, goldilocks agility, the Ed448 seed defect. Chapter `bible/04`.
16. R-013, R-014, R-016, delegation traits in practice: custodial versus horizontal scaling, `DND` enforcement in the Kever, `DID` consequence left to the relying party and to EGFs. Chapter `bible/03` §8.
17. R-034, same issuer means a nested block, different issuers mean separate ACDCs. Chapter `bible/05` §4.
18. R-065, R-066, decorrelation as the achievable goal; bulk issuance and blinded edges against standing-edge correlation. Chapter `bible/06` §4 and `bible/05` §5.
19. R-047, R-071, R-072, SEDI architecture and guardianship: IAL3 management ACDC, per-disclosee bulk credentials, custody from birth, five parent-child key arrangements. Chapter `bible/06` §SEDI and `scenarios/`.
20. R-038 / T-08, TEL anchors follow first-seen; keripy's keep-earliest rule differs. Chapter `bible/05` §registries.
21. R-011, OOBI bootstrap with the controller AID and redirect to witnesses. Proposed infrastructure chapter.
22. R-006, filtering is not authentication. Chapter `bible/09`.
23. R-021, the parser swallows exceptions to avoid becoming an oracle. Chapter `bible/02` or `bible/04`.
24. R-053, R-062, R-064, R-056, R-058, smaller IPEX facts: offer `o`, the four-tier taxonomy, the `m` field's open status, IPEX's likely separate spec, the exposure-not-meaning rationale. Chapter `bible/08`.
25. R-001, R-007, R-009, R-010, R-078, small facts and history. Chapters `bible/03`, `bible/04`, `bible/08` §5a.

Process rulings (R-073 to R-077) belong in `refresh/README.md` or `field/` notes rather than in a chapter.

---

## 15. Proposed sources.yaml entries

Not applied. The `gh-issues` kind does not exist in `refresh/detect.py` today; the first two entries need it added, or the PR source needs widening to cover issue comments. The discussion sources for the three spec repositories had no Sam comments in the window (10 discussions read, 0 Sam texts), which is itself worth tracking: rulings on the specifications land in keripy discussions and in spec issues and PRs, not in spec discussions.

```yaml
  - id: keripy-issues
    kind: gh-issues
    repo: WebOfTrust/keripy
    tier: hot
    since: 2026-10-14
    primary_authors: [SmithSamuelM]
    feeds: [raw/21-sam-rulings.md]
    chapters: ["03", "04", "05", "08", "09"]
    caveat: >-
      Sam's rulings in issue and PR comment threads, including PR review comments, which neither
      keripy-discussions nor keripy-prs (merged-PR titles) captures. 224 items with in-window Sam
      text on 2026-10-14; raw API responses cached in .ignored/sam-rulings-cache/. Several rulings
      reverse within days (raw/21 §11), so a scan must read the whole thread, not the first reply.

  - id: spec-issues-prs
    kind: gh-issues
    repos:
      - trustoverip/kswg-keri-specification
      - trustoverip/kswg-acdc-specification
      - trustoverip/kswg-cesr-specification
    tier: hot
    since: 2026-10-14
    primary_authors: [SmithSamuelM]
    feeds: [raw/21-sam-rulings.md]
    chapters: ["03", "04", "05", "08"]
    caveat: >-
      Editor rulings that forecast spec text: ACDC #205 (default operator), #204 (bulk issuance
      normative), #200 (bulk B derivation, landed), #191 (unique entropy, landed in v1.1);
      CESR #165 (PQ codes, landed in v1.1), #175 (Ed448 seed, open). A ruling here is [P] until
      the text is in a branch at a named commit; raw/21 §12 lists the ones that have not landed.

  - id: keripy-discussions
    kind: gh-discussions
    repo: WebOfTrust/keripy
    tier: hot
    since: 2026-10-03
    primary_authors: [SmithSamuelM]
    feeds: [raw/15-kram.md, raw/16-presentation-registries.md, raw/08-keripy-kb.md, raw/21-sam-rulings.md]
    chapters: ["03", "05", "07", "08", "09", "10"]
    caveat: >-
      Existing entry; proposed change is to add raw/21 to feeds and chapters 03 and 05, because
      #1515, #1550, #1566, #1570, #1573, #1574 and #1598 carry delegation, registry and bulk-issuance
      rulings, not only presentation material. The #1512 body is stale (raw/21 R-027, T-12).
```

---

## 16. Gaps and things not read

- PR #1683's code (the `TransReceiptIdxSigGroup` to `NonceSealSingles` change) was not read; R-009's later status rests on its title only.
- keripy code was checked for R-001, R-004, R-014, R-022, R-036, R-038, R-051 and R-052 only. The other rulings with a code dimension (R-007, R-015's PR #1564, R-023, R-025) were not re-verified at a pin for this note and rely on `bible/` and `raw/09` where cited.
- The grep for dead `tswg-` URLs in the corpus (R-076) was not run.
- Discussion bodies created before the window and edited inside it (#934 on 2025-12-01, #1082 on 2026-04-27, #1095 on 2025-11-11) were read in their current form; the edits themselves cannot be isolated from the API, so it is not known which sentences changed in the window.
- Reactions, emoji and the per-commit history of PR review threads were not fetched.
