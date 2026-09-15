# Doctrine Mining: KRAM — the KERI Request Authentication Mechanism

**Primary source:** `SmithSamuelM/Papers`, `whitepapers/kram.md`, **v0.7.6**, branch `master`. Last substantive commit `67550b477` (2026-03-06, "updated KRAM spec to clarify that we leave the partially signed database entries in place until prune time"); most recent commit of any kind touching the path is the merge `6ed1ceff4` (2026-03-06). **Confirmed unmoved as of 2026-09-15** — nothing between March and September, so every `[P]` claim below stands at its original pin. Not cloned locally; fetch with `gh api repos/SmithSamuelM/Papers/contents/whitepapers/kram.md?ref=6ed1ceff4 --jq .content | base64 -d`.
**Second primary source:** WebOfTrust/keripy discussion [#934](https://github.com/WebOfTrust/keripy/discussions/934), *KERI Architectures for Group Issuance (KAGI) and KRAM*, SmithSamuelM, 2025-01-30. This is Sam in his own voice on *why* KRAM exists and why only the weak version shipped.
**Third source:** `WebOfTrust/kram` `README.md` (repo last pushed 2024-07-06). An earlier, shorter subset of the same text — the "Interactive vs. Non-interactive", "Replay Attack Protection" and "Timeliness and Caching" sections, without simple/full KRAM, without the multisig treatment, without the v0.7 redesign. Superseded; cite the Papers version.
**Implementation:** `WebOfTrust/keripy` `main` @**`b8f60166b`** (2026-09-15); `src/keri/core/kraming.py` at that commit is 2319 lines, `tests/core/test_kraming.py` 6187 lines. Prior pins, retained because superseded claims are cited against them: `upstream/main` @`4df8e4a8` (2026-09-01) and `kraming.py` @`fe161709` (2026-08-20, 2224 lines). Implementation-tracking issues: [#937](https://github.com/WebOfTrust/keripy/issues/937) *KRAM Implementation* (open, arilieb, 2025-02-22, which names the whitepaper as the target), [#1302](https://github.com/WebOfTrust/keripy/issues/1302) *KRAM: Current state and gaps* (KeaxD, closed 2026-03-25), [#1661](https://github.com/WebOfTrust/keripy/issues/1661) *KRAM: partial-multisig escrow drops later deliveries when the sender anchors anything* (closed by PR #1662).
**Mining dates:** 2026-09-01 (first pass); **2026-09-15** (refresh).

**What the 2026-09-15 pass covered.** `kraming.py` was the most concentrated change in keripy this month: six commits between `fe161709` and `b8f60166b`, net 2224 → 2319 lines, with the test file growing 5768 → 6187. The six, oldest first: `8870ea6a0` (PR [#1658](https://github.com/WebOfTrust/keripy/pull/1658), merged), `72b034073` (PR [#1662](https://github.com/WebOfTrust/keripy/pull/1662), merged, fixes #1661), `4b79f8f43`, `f7c5723d6`, `e46fd026a`, `d70f670c7`. The pass re-read the whole of `kraming.py` at `b8f60166b` for the regions §5 cites, established the new key-state currency rule (§3.1, new), recorded a code/whitepaper divergence on partials (§4.7, new), re-verified every `[K]` claim in §5 at the new pin, and re-checked three negative results at named commits (§6). The whitepaper was confirmed unmoved. Nothing in `acdc/ipexing.py`, `peer/exchanging.py`, `db/basing.py` beyond the KRAM sub-database declarations, or `acdc/regeventing.py` was mined here — those belong to `raw/09` and `raw/16`.

---

## 0. Provenance and status — read before citing

Four things about this source set are load-bearing, and three of them are easy to get wrong.

**KRAM is not in the KERI specification, and the near-miss is a glossary entry.** *Re-verified unchanged at `kswg-keri-specification` `main` @`fbdd4a615`, 2026-09-15 — see §6.* A search for "kram" across `trustoverip/kswg-keri-specification` returns exactly one file, `docs/versions/v1/index.html`, and the hit is not spec text: it is an external cross-reference entry pulled from `trustoverip/kerisuite-glossary` (declared as `external_spec: "keri1"` in `specs.json:26`). The whole of it is one sentence — *"All requests from a web client must use KRAM (KERI Request Authentication Method) for replay attack protection. The method is essentially based on each request body needing to include a date time string field in ISO-8601 format that must be within an acceptable time window relative to the server's date time"* — followed by a link to the `WebOfTrust/kram` repo. `spec/spec-body.md` does not mention it. So the spec's only account of KRAM is a glossary gloss of *simple* KRAM, sourced outside the spec repo, in a rendered v1 artifact.

**The name is unstable.** The whitepaper title is "Keri Request Authentication **Mechanism**", and so is the `WebOfTrust/kram` repo description; the glossary says "**Method**". keripy's module docstring says Mechanism. Both expansions are in circulation; the whitepaper's is the one to use.

**It is actively maintained, not archival.** The whitepaper is a living design spec at v0.7.6 with a commit stream through March 2026, and it is *implementation-directive*: it names Python modules and classes (`keri.core.kraming`, `Kramer`, `Kramer.intake`), specifies LMDB table layouts and config-file keys, and in one place (`§Configuration`, final paragraphs) drops into first person about a redesign Sam worked out overnight. Read it as a spec-in-progress for keripy, not as a paper.

**It has internal strata.** v0.7.6 opens with "Full KRAM with Multisig Support" — a *redesign* — then carries the older material behind it (`§Background`, `§Simple KRAM`, `§Full KRAM`) and ends with an explicitly `## Obsolete` section. Where the front matter and the later sections disagree, the front matter wins. Two examples: the older `§Full KRAM` describes a cache holding *the last message from a client* keyed by an attribute vector, whereas the redesign caches *per message ID* with no monotonic comparison between different message IDs; and the older sections propose eight cache types (`MessageType.R.Route.X.XID.M.MID` and friends), which the redesign cuts down to three.

---

## 1. Why KRAM exists — the argument, in Sam's voice (#934 §KRAM)

The premise is KERI's sign-everything posture, and the observation that a signature's authority is *ephemeral*:

> "KERI is a sign-everything approach to authentication. […] when a given message is signed by the private key(s) and verified with the associated public key(s) from the current key state of the AID then that verifier can reasonable attribute that message as being sourced by the controller of that AID. We call this secure attribution to the source AID."

> "Should the key state change between the time of origination and the time of verification, then the verifier can no longer assume the signature as a secure form of attribution because one of the primary reasons for a given controller to change its key state is to recover from key compromise. This means that by default, any signatures produced with the stale key states are not trustworthy."

Then the gap that KRAM fills, stated as a division of labor between message classes:

> "KERI Key Event messages and their associated KELs have built-in ordering mechanisms that are tied to the current key state, so they are self-protecting from replay attacks. However, the generic exchange, query, reply, prod, and bare messages do not have any built-in replay attack protection. For this purpose, the KRAM (KERI Request Authentication Mechanism) was designed."

**This is the sentence to remember.** KRAM's scope is exactly the non-key-event message set — `qry`, `rpy`, `pro`, `bar`, `xip`, `exn` — because key events carry their own ordering (sequence number, prior digest, first-seen) and these do not.

The choice of mechanism is argued by elimination:

> "The three main types of replay attack protections are: 1. Authenticated sessions on a dedicated synchronous channel. 2. Interactive challenge-response authentication 3. Timeliness ordered authentication. Obviously, 1. is precluded for asynchronous networks, and 2. is fundamentally less scalable than 3. since it requires a minimum of two times the message traffic for each message to be authenticated."

The whitepaper's `§Background` adds the historical claim behind that preference: nonce challenge-response is an artifact of an era without network time servers, cheap CSPRNGs, or asymmetric signatures, taught onward by habit — *"Often, CS professors teach simple (but impractical) mechanisms as academic exercises that are then adopted in the real world by former students, not because they were well thought out, but because they were familiar."* And the payoff line for the design: *"implementing a solution that supports asynchronous networks at scale and eliminates 1/2 of the packets is a huge design win."*

The whitepaper positions KRAM against FIDO2/WebAuthn as the nearest comparable (`§Interactive vs. Non-interactive`): the difference is that WebAuthn has no in-stride verifiable key rotation, so *"given one already has a KERI verified key state, using FIDO2/WebAuthn to authenticate replay requests would be going backwards."* Prehistory: the mechanism was first built for Indigo-BluePea (`github.com/reputage/bluepea`), a lost-and-found registry proof of concept.

**The generic property claim** (`§Replay Attack Protection`): *"In general replay attack protection imposes some form of timeliness to any signed request and some form of uniqueness to any signed request."* Everything in KRAM is one of those two.

---

## 2. Simple KRAM — what is deployed, and why that is a problem

Definition (#934, repeated verbatim in the whitepaper `§Simple KRAM`):

> "simple KRAM works by including in the over-the-wire message a timestamp referenced to the network time clock of the recipient. […] Because the timestamp is referenced to the time as seen by the recipient, the originator of the message can't lie about time. The recipient has a moving time window whose size is some small multiple of the average network latency and drift of network time and surrounds the current time as seen by the recipient. If the timestamp of the received message lies outside this window, it is dropped."

Window: `[t-d-m*l, t+d]`, with typical `d = .01` s (drift/skew), `l = 1` s (latency), `m = 3`. **No cache is required** — that is the whole of its appeal, and its limit: *"A replay attack is only possible inside the time window synchronized to the host clock. […] Therefore the protective efficacy of simple KRAM is better the smaller the window."*

Why it shipped and nothing better did — the most quotable admission in the corpus about KERI's uneven maturity (#934 §Simple KRAM):

> "Unfortunately, due to the exigency of limited resources in implementing support for the vLEI, only the most expedient version of KRAM, called simple KRAM, was implemented. This has now become problematic and is largely the root cause of the associated issues and discussions."

The surrounding `§Exigency and Expediency` section generalizes it: GLEIF's vLEI delivery under time and budget pressure produced "bare-bones features needed for the vLEI" and left everything else at a lower readiness level, and the unevenness persists because contribution is measured in developer time that the project has not had.

**The multisig collision, which is the actual root problem** (`§Simple Kram MultiSig`):

> "For simple KRAM, with multisig messages, the only practical policy is to accept the message if it is signed by any one of the group members and its timestamp lies within the much tighter time window. But then the message is not protected by the threshold of the group multi-sig. Employing an escrow to collect signatures after acceptance does not help because all the to-be escrowed signatures must still arrive within the narrow time window, which means the coordination of the group members must be tight enough to fit in this window."

A three-second window cannot hold open long enough for three humans on three devices to sign. So a multisig `exn` either loses threshold protection or cannot be sent.

**The workaround in production: two-level simple KRAM** (`§Two-Level Simple KRAM`). The over-the-wire `exn` wrapper is single-signed by any one member and is subject to simple KRAM; the *embedded payload* is separately signed and is not subject to KRAM, and goes into a signature-collecting escrow once past it. *"The embedded payload may be a tunneled exchange message that just leverages the processing of exchange messages. The tunnel is meant to cross through simple KRAM."* Sam labels this **"the current supported approach"**, and names its cost: every member signs twice, and the escrow must hold partially signed payloads for as long as the group takes. The variant with a pre-protocol that collects payload signatures before sending is the motivation for HAMI ([keripy#911](https://github.com/WebOfTrust/keripy/issues/911)).

---

## 3. Full KRAM — the mechanism

> "Full KRAM employs strictly monotonically ordered timeliness caches to protect from replay attacks. It includes protection from retrograde attacks on the recipient's clock." (`§Full KRAM`)

**Core rule.** A timeliness cache stores the timestamp of the last message from a source; a new message must be *later* than the cached one and inside the receiver's window `[t-d-l, t+d]`, where `t` is the receiver's current time, `d` is clock drift/skew, `l` is the lag. Monotonicity supplies uniqueness; the window supplies pruning, i.e. bounded memory. The whitepaper is explicit that these roles are separable: *"the monotonicity of the cache protects against a replay attack and the time window merely bounds the memory requirements"*.

**Why that separation matters.** Because the window is only a memory bound, it can be long — *"days or weeks"* — where simple KRAM's window must be short to be safe. That is the entire answer to the multisig problem: a window of hours or days lets a receiver-side escrow collect member signatures at human speed while still refusing every replay. Typical redesign values: `d = 100` ms, `sl` (short lag) `2000` ms, `ll` (long lag) `7200000` ms = 2 h, `xl` (exchange lag) `172800000` ms = 48 h.

**Retrograde clock protection.** *"the receiver persists to durable storage a single timestamp of the latest time it sees. If the network time is even older than the latest saved time, the receiver can refuse to accept messages until the clock catches up."* Monotonic caches already defeat a rewound clock for messages they still hold; the persisted high-water mark covers the rest.

**Detectability, not just prevention** (`§Replay Attack Protection`). Under the "tight" mechanism the receiver answers a given signed request exactly once, so a successful interception is *visible to the requester*: either no response arrives, or it arrives redirected from a host that is not the requestee. This is a KERI-shaped argument — duplicity detection rather than prevention — applied to request authentication.

**Granularity.** A cache key is a vector drawn from `[source AID, message type, route, exchange ID, message ID]`, and finer keys stop interleaved transactions from colliding. One constraint is stated as a rule with teeth: *"When using per-transaction ID or per-message ID caching, the window size must be per transaction type, not per transaction ID/message ID, to avoid a cache-prune replay attack."* If a sender could set its own window, it could either DDoS the receiver's memory with an unprunable cache or open a replay gap at prune time. **Window class is the receiver's decision, always.**

**Throughput** (`§Time Resolution and Throughput`). Microsecond timestamps give 1M monotonic slots per second *per cache entry*, so granularity is also parallelism. Worst case analysis: with `d = 100` ms and zero network latency, a sender has ~90 ms of slots ahead of the receiver's leading edge — ~90,000 messages — before it must block; each millisecond of real latency adds another 1,000 slots. Conclusion: *"microsecond clock resolution on our timeliness caches is more than adequate for the foreseeable future."*

**Out-of-order delivery is treated as a separate failure mode from replay** (`§Asynchronous Out-of-order Messages`). Interactive transactions self-order because the parties take turns, so one cache entry per transaction is the recommendation on asynchronous transport; pipelining many transactions through one cache entry is only safe on an in-order channel or with a reliable retry mechanism.

### 3.1 Which key state authenticates a signature — the currency rule (new 2026-09-15)

**This is the doctrinally sharpest change of the month, and it is not a bug report.** It is a statement about what a signature means, made in code, and it was made twice independently in two implementations within six days.

The question. A transferable signature arrives as a `tsg` — a `TransIdxSigGroup` quad `(prefixer, number, sdiger, sigers)` — whose `(number, sdiger)` names an event in the signer's KEL. A verifier must decide whether that reference is *current*: does it name the key state the signature should be checked against? Two candidate answers exist, and they are the same answer right up until a non-establishment event is interleaved. **"The sender's latest event" and "the sender's last establishment event" diverge exactly when the sender has anchored something — a registry inception, a credential issuance, a revocation — without rotating keys.**

**The rule as of `b8f60166b` is: the last establishment event.** The `SigVerifyResult` module docstring states the reasoning in one sentence `[K]` (`kraming.py`, module docstring above `class Kramer`, :70-75, `b8f60166b`):

> "Signing keys change only at establishment events, so the key state ref names the last establishment event rather than the last event of any kind."

In code, at every site `[K]` (`kraming.py` `Kramer._verifyAttachedSigs`, tsgs pool gate, :706-707, `b8f60166b`):

> `if (number.sn != kever.lastEst.s or sdiger.qb64 != kever.lastEst.d): continue`

**Superseded, 2026-09-15.** At `fe161709` the same gate read `[K]` (`kraming.py` `Kramer._verifyAttachedSigs`, :697-698, `fe161709`):

> `if (number.sn != kever.sner.num or sdiger.qb64 != kever.serder.said): continue`

`kever.sner` / `kever.serder.said` is the sender's **latest event of any kind**. Replaced by `kever.lastEst.s` / `kever.lastEst.d` in `8870ea6a0` (PR #1658, merged). Ten sites in `kraming.py` carry the reference at `b8f60166b` — :460-461 (`_normalizeCurrentSenderTsgs`), :553-554 (`_scrubSameSenderPriorEventTsgs`), :609-610 (`_scrubFailedVerification`), :632-633 (`_setVerifiedSenderTsg`), :706-707 (`_verifyAttachedSigs`), :854-855 (`_storeNonAuthAttachments`), and the four partial-multisig key-state pins at :1159-1160, :1331-1332, :1407-1408 and :1669-1670 — and all ten now read `lastEst`. At `fe161709` the equivalent sites read `kever.sner` / `kever.serder.said`.

**The prose was right and the code was wrong, which is the tell.** At the old pin the docstring immediately above the offending comparison already stated the establishment-event rule `[K]` (`kraming.py` `Kramer._normalizeCurrentSenderTsgs` docstring, :442-445, `fe161709`):

> "When prefixer.qb64 == senderId and (number, sdiger) references the sender's current establishment event, those sigers are also added to ``sigers``"

That docstring is unchanged at `b8f60166b` (:444-447). So the design intent was recorded correctly in the module the whole time; only the expression of it drifted. A rule that lives in a docstring and not in a specification is a rule that can drift this way without anything catching it.

**What a reader of the old bible would now state differently.** Before: KRAM checks a `tsg` against the sender's current key state, meaning the state established by the sender's latest KEL event. After: KRAM checks a `tsg` against the state established by the sender's **last establishment event**, which is the same thing only when no interaction event has intervened. The old phrasing was not merely imprecise — under it, an issuer that had anchored anything had every correctly formed signature refused, because the quad's reference and the KEL tip no longer matched.

**The blast radius is the argument for why this is doctrine and not a defect note.** Per standards §1 a commit message is not a source, so this is not quoted: the author of `8870ea6a0` records in its message that the affected population is every AID that has anchored a registry inception, a credential issuance or a revocation — i.e. every credential issuer — and that KRAM's scope is exactly the message set those issuers use. Treat that as **status and intent, not a citation about the design**; the design claim above rests on the code and the module docstring. The analytic point stands on its own: the two candidate rules diverge precisely on AIDs that anchor without rotating, and the population that anchors without rotating is the issuer population, which is the population whose `exn` traffic KRAM governs. The mis-stated rule therefore failed on exactly the users it exists to serve, not on an edge case. Two tests now pin the behavior by name `[K]` (`tests/core/test_kraming.py`, `b8f60166b`): `test_tsgs_current_when_latest_event_is_non_establishment` (:6000) and `test_partial_multisig_survives_an_anchor_during_collection` (:6093). `test_stale_tsgs` is still present at :2598, which is the guard that genuine staleness after a *rotation* is still detected — the rule loosens what counts as current without loosening what counts as stale. (Presence verified at the pin; the test body was not diffed against `fe161709`.)

**The second half: the partial-multisig escrow pins the same reference.** The `asmk` escrow stores the sender's key state when collection begins and compares it on every later delivery, dropping the accumulated signatures on a mismatch, so that a rotation part-way through invalidates what was gathered under the old keys. That stored couple was built from the same latest-event reference and is now built from `lastEst` `[K]` (`kraming.py` `Kramer.kramit`, non-transactioned multi-key accumulation, :1159-1160, `b8f60166b`):

> `currentKeyState = (Number(num=kever.lastEst.s), Diger(qb64=kever.lastEst.d))`

The consequence of the old form was worse here than on the verification gate, because nothing refreshes the stored value: one anchor mid-collection and the escrow could never again match, so it sat until it pruned. **The long window exists so a group can collect signatures at human speed — the whitepaper suggests two hours — and an issuer anchoring something inside that window is ordinary.** The case the long window is there to serve was the case the old rule broke. Changed by `72b034073` (PR #1662, fixes #1661).

**A third application, and the one that shows the rule is a rule and not a patch: foreign endorsers are frozen at receipt.** When a partially-signed multisig message carries a last-sig group from *someone other than the sender* — an endorser whose signature is not an authenticator for this message but must be forwarded with it — keripy now resolves that group to the endorser's last establishment event at the moment of receipt and stores it in explicit `(prefixer, number, diger, siger)` form `[K]` (`kraming.py` `Kramer._storeNonAuthAttachments` docstring, :828-830, `b8f60166b`):

> "This freezes the establishment reference so a later endorser rotation before the sender reaches its signature threshold does not reinterpret the escrowed signatures."

The code performs the resolution at :849-857, falling back to `kramULGS` when the endorser's KEL is not yet resolved. The generalization worth carrying: **an escrow that holds signatures across time must record the key state each signature was made under, not consult the current one at release** — otherwise the meaning of a signature changes while it sits in the escrow. That is the same principle as the sender-side pin in the previous paragraph, applied to a party whose rotations the receiver does not control.

**The same correction happened independently in KERIA, six days later** — cross-reference for `raw/10`, which owns the KERIA note. `WebOfTrust/keria` `b57780a` (Patrick Vu, 2026-09-07, *"fix: seal endrole + locschemes tsgs to last establishment event"*) changes the **sender** side of the same question: the `tsg` KERIA constructs when it submits an `/end/role` or `/loc/scheme` reply. At `7e685edaa` `[K]` (`keria` `src/keria/app/aiding.py`, end-role handler, :1663-1668):

> `tsg = (hab.kever.prefixer, coring.Seqner(sn=hab.kever.lastEst.s), coring.Saider(qb64=hab.kever.lastEst.d), rsigers)`

Immediately before that commit the same quad read `[K]` (`keria` `src/keria/app/aiding.py`, :1665-1666, `b57780a^`):

> `coring.Seqner(sn=hab.kever.sn), coring.Saider(qb64=hab.kever.serder.said),`

keripy fixed the receiver's currency test; KERIA fixed the sender's construction. **Two implementations, two codebases, two authors, opposite ends of the same wire, same month, same substitution.** That is evidence about the design rather than about either bug: the convention "a `tsg`'s `(sn, said)` names the establishment event that established the signing keys" was underspecified enough that both ends independently got it wrong in the same direction, and both had to discover it from failures rather than from a document. Where that convention is written down normatively is an open question — see §7.

---

## 4. The v0.7.6 redesign — what changed and why

The redesign is a deliberate simplification. Sam's own account of why, at the end of `§Configuration`:

> "One of the problems is that we added a lot of flexibility to allow resource tuning that may be overkill. And that is complicating the logic for dynamic window sizes. […] Moreover, in hindsight, I think single-key and multi-key controlled identifiers are sufficiently different that a different logic split would benefit."

### 4.1 Three authentication types, chosen by cardinality

`asr` attached seal reference, `assk` attached signature single-key, `asmk` attached signature multi-key. The split is deliberately *cheap to compute*:

> "The separation between single-key and multi-key is determined by the cardinality of the current key list for the sender AID, not by whether the attached signature(s) satisfy the threshold. […] This is important because threshold satisfication requires verifying the attached signatures first, which is a much heavier operation than merely counting the elements in the key list."

Seal-reference authentication needs no signature collection at all — the message was already authenticated by its anchoring seal in the sender's KEL — so it takes the short window regardless of key-list cardinality. When both a seal and signatures are attached, the seal is checked first because it is cheaper; if it validates, the signatures are dropped.

**Only `asmk` waits.** That is the point of the taxonomy: short windows for everything that cannot need to wait, long windows only where signature collection genuinely requires them.

### 4.2 Two levels of window: message ID and exchange ID

Inner window, per message ID: `[rdt-d-l, rdt+d]` on the receiver's clock. Outer window, per exchange ID: `[xdt, xdt+xl]`, where `xdt` is the `dt` of the `xip` that opened the transaction. A transactioned message must satisfy both. The outer window exists because *"a transaction may not advance until a message is authenticated"*, and without it an exchange cache could never be released.

**Caching is per message ID, and the consequences are good.** Since a message's SAID digests its `dt`, two messages with different datetimes are different message IDs with different caches — so a sender needs no cross-device synchronization to avoid tripping its own monotonicity, and out-of-order arrivals from different network paths do not collide. The stated price: *"the lower storage limit required for full KRAM is higher"*, and the only storage knob left is window size.

**v2 dependency.** *"This redesign of KRAM assumes v2 KERI"* — transactioned `exn` needs a non-empty `x`. A v1 `exn` is treated as non-transactioned even when its `p` field is populated.

### 4.3 Accept lag vs prune lag, and the two gap attacks

Each cache type carries paired lags: `sl/ll/xl` for accepting and `psl/pll/pxl` for pruning, with `prune >= accept` and typically equal. The pair exists to make *reconfiguration* safe, and the attacks it defends are the sharpest new material in the redesign:

- **Gap replay.** A message is accepted, then pruned; the accept window is then lengthened; the pruned message is replayed and now falls inside the new window with no cache entry left to refuse it.
- **Gap first-play.** A message is *rejected* as too old, so it was never cached; the accept window is later lengthened; an attacker submits it as a first play. The whitepaper's worked case: the sender, seeing no response, reissues the same content with a new datetime and new message ID, so the victim suffers the effect twice ("double access") from two messages that differ only in `dt`.

The mitigation is a staged two-step change: raise the prune lag immediately, and delay raising the accept lag by `delta = new - old` so any message that could exploit the gap has aged out first. Decreases are safe and immediate. Changing the *granularity* of cache types (adding a route-specific type, say) is the hard case, and the whitepaper says so: *"This logic has yet to be worked out"* — the worst case must be computed against the shortest existing accept window for the same message type.

### 4.4 Configuration: enabled flag plus a denials firewall

Rooted at a `"kram"` dictionary in the HJSON config, injected into the `Habery` and thence to each `Kevery`'s `Kramer`. `"caches"` prepopulates the cache-type table. `"enabled"` is a global boolean, and `"denials"` is a list of `(version, ilk, route-prefix)` triples that read as *"a set of explicit firewall denial rules"* — a match disables KRAM for that message. Compacted to `Mmm.iii.route` strings for fast prefix matching.

The stated purpose is backward compatibility "for both pre-KRAM applications and message-type-route combinations, **such as BADA-RUN endpoints, that conflict with KRAM**". That conflict is worth flagging: BADA accepts data-at-rest updates by monotonic key-state-then-datetime comparison, which is a *different* acceptance rule from KRAM's window, and the two cannot both govern the same message.

### 4.5 KEL availability: drop and cue, do not escrow

A change from existing keripy behavior, argued on latency grounds:

> "In most cases, the time required to notify and then retrieve the KEL exceeds the KRAM message window, causing the message to be dropped, even after the KEL is retrieved. Which makes moot the use of the escrow. […] Therefore, the most practical approach is to drop the message and create a cue that notifies the receiver to obtain the appropriate KEL or KEL event from the sender."

Also noted in passing: *"There is also a bug in the escrow logic that can cause a loop that repeatedly reescrows."*

### 4.6 DDoS surface

Stripping attachments to force a drop is a weak DoS (a presence check is cheap); stripping and reattaching invalid signatures is stronger; attaching a bogus seal reference *alongside* valid signatures is an amplification attempt. The answer is ordering: accept if either authenticator is valid, and check the cheapest first. Transport encryption is named as a complementary mitigation.

### 4.7 Partials at threshold: the code and the whitepaper now disagree (new 2026-09-15)

**This is a live divergence between the two primary sources, and it is recorded as one rather than reconciled.** The whitepaper says partially-signed database entries survive until prune time so that signatures can keep accumulating after the threshold is met. keripy at `b8f60166b` deletes them the instant the threshold is met. Both statements are quoted below at their pins; the corpus does not pick between them.

**The whitepaper's rule**, stated identically at three places in the processing pseudocode `[P]` (`kram.md` §Full KRAM processing steps, repeated at :306, :353 and :427, `6ed1ceff4` / content unchanged since `67550b477`):

> "the partially signed database entries will remain until the prune window closes, upon which all the partially signed database entries will be deleted"

and, immediately following in the same sentence run `[P]` (`kram.md`, same passage, :306, `6ed1ceff4`):

> "This allows signatures to continue to be collected even after the threshold is reached."

And the stated reason, which is a design intent and not an implementation detail `[P]` (`kram.md`, same passage, :306, `6ed1ceff4`):

> "It is desirable to know all who signed, not just the first who meet the threshold."

The `67550b477` commit that introduced this wording is titled *"updated KRAM spec to clarify that we leave the partially signed database entries in place until prune time"* — so it is a deliberate clarification, not incidental phrasing.

**keripy's rule at `b8f60166b`.** On threshold satisfaction, the accumulated state is rehydrated onto the outgoing message and then the three partial-multisig stores plus every non-auth attachment store are removed `[K]` (`kraming.py` `Kramer.kramit`, non-transactioned multi-key threshold branch, :1215-1220, `b8f60166b`):

> `# The cache remains as the replay marker. Partial state is no longer retryable after the accepted handoff.`

followed by `self.db.kramPMKM.rem(key)`, `self.db.kramPMKS.rem(key)`, `self.db.kramPMSK.rem(key)`, `self._remNonAuthAttachments(key)`. The transactioned branch does the same at :1463-1468. A third site clears them on key-state change (:1166-1171, :1414-1418), which the whitepaper does *not* authorize either — its key-state-change step says only *"drop the event and exit. This prevents the message from ever being validated while keeping the timeliness cache in place"* (`kram.md` :301, `6ed1ceff4`), and says nothing about deleting the partial stores.

**Superseded, 2026-09-15.** The note previously recorded, on the whitepaper's authority, that partially-signed entries are held to prune time and that keripy implements "keeping signature collection alive until the prune window" (§5's reading of issue #1302). At `fe161709` that was true of the code: the only `kramPMKM.rem` / `kramPMKS.rem` / `kramPMSK.rem` / `_remNonAuthAttachments` calls in the whole file were the two pruner bodies, at :2155-2160 and :2187-2192. At `b8f60166b` the pruners still clear them (:2250-2252, :2282-2284) but four earlier clearing sites now exist. Changed by `d70f670c7` *"Verify EXN evidence and clear KRAM partials"* (Evan Asakawa, 2026-09-02).

**What is at stake, and why it is not a bug report.** The whitepaper's rationale is an *evidentiary* one: on a group-signed message you may want the full membership that endorsed it, not merely the first `k` of `n` whose signatures happened to arrive. keripy's comment gives a *replay-safety* rationale: the timeliness cache alone is the replay marker after handoff, and leaving retryable partial state around is a liability. Both are coherent policies and they answer different questions. Which one governs is unsettled: the whitepaper is the design of record and Sam clarified it on purpose; the implementation is the thing that runs, and its author had a reason. Note also the direction of the tradeoff — under keripy's rule, a late co-signer's endorsement of an already-accepted multisig message is silently discarded, which is exactly the information the whitepaper says some cases want. See §7 open question 6.

---

## 5. keripy implementation status — re-verified at `main` @`b8f60166b` (2026-09-15)

Every item below was re-read in `kraming.py` at `b8f60166b`, not carried forward from the `4df8e4a8` / `fe161709` pass. Line hints are at the new pin.

**The redesign is built.** `src/keri/core/kraming.py` is 2319 lines with a 6187-line test file, and it tracks v0.7.6 closely rather than the older strata:

- `AuthTypeCodex` with exactly `asr`/`assk`/`asmk` (`kraming.py:38-51`). Unchanged; the inline comments still encode the window policy directly — `asr` and `assk` are marked "Short lag window", `asmk` "Long lag window. Accumulates sigs."
- `Kramer.intake` implements the whitepaper's denial-check-then-`kramit` shape almost line for line (`kraming.py:1028-1034`), including the `md.startswith(d)` prefix match. Unchanged in substance; moved from :963-969 by the intervening additions.
- `_fetchCacheType` implements the reduced three-level cascade — `msgType.R.route`, then `msgType`, then a default catchall (`kraming.py:293-313`). The catchall key is `"~"`, chosen so it sorts last in LMDB, where the whitepaper says "default". Unchanged.
- **19 KRAM sub-databases** in `basing.py:1310-1388` (declared in the `Baser` docstring at :745-895): cache-type `ctyp.`, message cache `msgc.`, transactioned cache `tmsc.`, transaction-opener datetimes `xdt.`, partially signed message/signature/sender-key-state `pmkm./pmks./pmsk.`, plus one per non-authenticator attachment type (`kramTRQS`, `kramTSGS`, **`kramULGS`**, **`kramCIGS`**, `kramSSCS`, `kramSSTS`, `kramFRCS`, `kramTDCS`, `kramPTDS`, `kramBSQS`, `kramBSSS`, `kramTMQS`). **Corrected 2026-09-15:** this bullet previously said "14", which was wrong at the time — the list it gave already enumerated 17. Two are genuinely new since `fe161709`: `kramULGS` (`ulgs.`, `CesrIoSetSuber` of `Prefixer`, holding foreign last-sig-group prefixers whose KEL is not yet resolved) and `kramCIGS` (`cigs.`, non-sender cigars). `basing.py` itself belongs to `raw/09`; only the KRAM sub-database declarations were read here.
- Multi-key accumulation with key-state-change detection: a stored `(sn, said)` establishment reference is compared against the current kever and the message is dropped if the sender rotated mid-collection (`kraming.py:1157-1171`). **The reference is now `kever.lastEst`, not the sender's latest event — see §3.1.** The drop now also clears the partial stores, which it did not at `fe161709` — see §4.7.
- Reconfiguration safety is implemented, not just specified: `changeConfig`, `reconcileConfig`, `_buildCoverageGraph`, `_computeCoverageDiff`, `_computeWorstCaseDelta`, `_validateCoverage` (`kraming.py:1684-2225`) — i.e. someone did work out the granularity case the whitepaper left open. Unchanged in substance.
- `Pruner`, an hio `Doer` on a 1 s period, driving `_pruneMessages` and `_pruneExchanges` (`kraming.py:2227-2318`). Unchanged in substance; both pruners still clear the partial stores (`:2250-2252`, `:2282-2284`).

**The `processMsg` refactor the whitepaper asks for exists.** `Kevery.processMsg` (`eventing.py:4683`) is the consolidated entry point for `qry, rpy, pro, bar, xip, exn`, documented with the whitepaper's exact three steps: AID allow/deny, then `self.kramer.intake()` (`eventing.py:4741`), then message-specific dispatch. `processXip`, `processPro` and `processBar` are **still stubs** at `b8f60166b` `[K]` (`eventing.py` `Kevery.processXip`, :4818-4819):

> `"""Stub: KERI v2 exchange transaction; no processing yet."""`

with `processPro` (:4822-4823) and `processBar` (:4826-4827) identical in form. A month of concentrated KRAM work did not advance them, which keeps §7 open question 4 open.

**Enablement — unchanged, and the distinction `bible/09 §7` turns on still holds.** `Kevery.__init__` takes `enableKram=False` (`eventing.py:4136`) — so KRAM is off unless asked for — but the two runtimes that matter pass `enableKram=True`: `directing.py:470` and `indirecting.py:76`. **"Default-disabled" is true of the class and misleading about deployments.** Re-verified at `b8f60166b`; the three sites are the only `enableKram` occurrences in `src/keri`.

**Window classes — no change, and still unguided.** Re-checked at `b8f60166b`: `kraming.py` ships **no default window values at all**. Every `(d, sl, ll, xl, psl, pll, pxl)` septuple comes from the `"kram"` config's `"caches"` dictionary via `_populateCtyp` (:196-208), and `_parseValidateCtyp` (:151-188) enforces ordering and sign only `[K]` (`kraming.py:170-185`, `b8f60166b`): `d >= 0`, `0 < sl <= ll <= xl`, `psl >= sl`, `pll >= ll`, `pxl >= xl`. The only absolute bounds are the trivial ones — a window must be non-negative and the short lag must be positive. **No ceiling, no non-trivial floor, and no warning at any magnitude:** a deployer may configure a one-millisecond `sl` or a thirty-day one and the code accepts both silently. `_fetchCacheType` raises `KramError` when nothing matches and no `"~"` catchall is configured (:312-313), so a receiver that configures nothing gets an error rather than a safe default. The whitepaper's example numbers (`d = 100` ms, `sl = 2000` ms, `ll = 2` h, `xl = 48` h, §3) remain examples in prose with no counterpart in code. **Window class remains a security parameter chosen by the deployer with no guidance from either source**, which is §7 open question 5 and is unmoved.

**Built-in OOBI carve-out.** `Kramer.OobiDenials` hard-codes `rpy /end/role` and `rpy /loc/scheme` as denials merged in whenever KRAM is enabled (`kraming.py:98-147`), because *"OOBI endpoint discovery replies rely on BADA acceptance rather than KRAM replay protection"*. This is §4.4's BADA conflict, resolved in code.

**Implementation history.** #1302 (closed 2026-03-25) records that PR #1288 landed the core "aligned with the v0.7.5 whitepaper" and lists as *gaps*: attachment databases, the pruning doer, keystate-retrieval cueing, AID allow/deny, and keeping signature collection alive until the prune window. Every one of those was present at `4df8e4a8`. **Amended 2026-09-15:** the last of the five no longer holds as written. Signature collection is still alive *until threshold*, and the pruners still bound it, but partial state is deleted at threshold satisfaction rather than at prune time, so collection does not continue past acceptance — see §4.7.

**Two divergences worth checking — both re-checked at `b8f60166b`, both still open.**

1. **Cache-type route matching is exact, denial route matching is a prefix.** `_fetchCacheType` compares `key == exactRoute` where `exactRoute = f"{msgType}.R.{route}"` (`kraming.py:294,299`); `intake` uses `md.startswith(d)` (`kraming.py:1031`). So a cache-type configured for route `/end` does not govern a message routed `/end/role`, while a denial configured for `/end` does deny it. The whitepaper's "most specific matching" language does not settle which was intended. Unchanged at the new pin.
2. **The v0.7.6 gap-attack machinery assumes windows only ever change through `changeConfig`.** Cache entries store their own `(d, ml, pml, xl, pxl)` at creation precisely so in-flight caches are immune to reconfiguration. **Partly closed:** `test_existing_caches_unchanged_on_config_update` (`tests/core/test_kraming.py:3628`, `b8f60166b`) now exercises exactly that invariant, so it is tested; whether any path other than `changeConfig` can mutate a live window is still not established.

**A third, new at `b8f60166b`: a dangling PR reference in the source.** `_scrubSameSenderPriorEventTsgs` justifies its policy by quoting "KRAM PR #1788" (`kraming.py:525-528`). `WebOfTrust/keripy` has no PR #1788 — `gh api repos/WebOfTrust/keripy/pulls/1788` returns 404 as of 2026-09-15, and the repo's PR numbers are in the 1600s. The quoted decision ("scrubbing same-sender prior-event tsgs since they cannot be used for authentication") is implemented and coherent; only its citation is unresolvable. Recorded because the corpus's own rule is that a citation must lead somewhere, and this one is a design rationale whose provenance cannot be checked.

---

## 6. Where KRAM is *not* — negative results, each at a named commit

A negative that still holds at a new pin is a real finding, and these were re-run on 2026-09-15 rather than carried forward.

- **Not in the KERI spec. Re-verified at `fbdd4a615`** (`trustoverip/kswg-keri-specification` `main`, 2026-09-15), and **unchanged** — the named residual in `keri-doctrine.md` is intact. A case-insensitive search for `kram` across the repo at that commit returns **exactly one file**, `docs/versions/v1/index.html`, and **zero hits anywhere under `spec/`**. The hit is still the imported glossary xref quoted in full in §0, word for word, carrying no tier marker because it is not specification text (`docs/versions/v1/index.html:2661`, `fbdd4a615`):

  > "KRAM (KERI Request Authentication Method) for replay attack protection. The method is essentially based on each request body needing to include a date time"

  — the sentence continues as §0 gives it, and is followed by the same link to `WebOfTrust/kram`'s `README.md`. So after the busiest month KRAM's implementation has ever had, its standing in the standardizing line is unchanged: one sentence, imported from `trustoverip/kerisuite-glossary`, describing the *weak cache-less* variant, in a rendered v1 artifact. **The gap between what is implemented and what is specified widened this month rather than narrowing** — `kraming.py` gained 95 net lines and a doctrinal rule about key-state currency that no specification states anywhere.
- **Not in the ACDC or CESR specs — NOT re-verified this pass.** `kswg-acdc-specification` and `kswg-cesr-specification` are not cloned under `~/code/wot/`, so this negative still rests on the 2026-09-01 search and carries no commit pin. Under-claimed deliberately: treat it as unverified until a pin exists.
- **No timeliness enforcement in KERIA's request auth. Re-verified at `7e685edaa`** (`WebOfTrust/keria` `main`, 2026-09-15), and **the negative holds — now across two authenticator classes rather than one.** The auth path was refactored since the 2026-09-01 search: the old `Authenticater` is now `SignedHeaderAuthenticator`, joined by an `ESSRAuthenticator`. Both bind a timestamp and neither compares it to a clock.
  - `SignedHeaderAuthenticator.DefaultFields` still lists `Signify-Timestamp` (`src/keria/core/authing.py:81`), and `outbound` still stamps `helping.nowIso8601()` (`:180`). Its `inbound` (`:95-167`) reconstructs the RFC-9421 signature base from the named fields and the `@signature-params`, verifies it with `ckever.verfers[0].verify(...)` (`:162`), and returns. `inputage.expires` appears only as a value **folded into the signature base string** (`:143-144`) — it is signed over, never evaluated against the server clock.
  - `ESSRAuthenticator.inbound` reads `dt = self.getRequiredHeader(request, "SIGNIFY-TIMESTAMP")` (`:233`) and places it in the signed payload as `dt=dt` (`:253`) before verifying. Again bound, never checked.
  - A search of `authing.py`, `httping.py` and `agenting.py` at `7e685edaa` for `fromIso8601`, `timedelta`, `datetime`, `expire`, `clockSkew`, `maxAge`, `freshness` and `toleran` returns three hits total, all accounted for: the two `inputage.expires` lines above, and `agenting.py:1576`, which is an **agent-idle eviction timer**, not request freshness.

  **The request is bound to a timestamp by the signature; nothing rejects a stale one.** This is the exact shape of "simple KRAM without the window" — and simple KRAM's own stated protection is *entirely* the window (§2: "If the timestamp of the received message lies outside this window, it is dropped"), so a signed-but-unchecked timestamp supplies none of it. Two qualifications keep this honest. First, it remains a negative search result over three files, not a maintainer's statement, so it is a question to put to a maintainer rather than a defect claim. Second, the surviving replay protection here is not nothing: the signature is over `@method` and `@path`, so a replay is confined to reissuing the identical request to the identical endpoint. That is a narrower exposure than an unauthenticated bearer token, and the corpus should not conflate them. `raw/10` owns the KERIA note; recorded here only as it bears on KRAM and freshness.
- **No module in keripy named for simple KRAM.** The deployed simple-KRAM behavior Sam describes is distributed across message handling and the HTTP layer rather than centralized, which is part of why full KRAM needed the `processMsg` consolidation before it could be wired in. Not re-searched at `b8f60166b`; carried forward from 2026-09-01.
- **No whitepaper movement. Verified 2026-09-15.** `SmithSamuelM/Papers` `whitepapers/kram.md` has not changed since the note's first pass: the GitHub commits API for that path returns `6ed1ceff4` (2026-03-06, a merge) as the most recent, with `67550b477` (2026-03-06) the last substantive edit. Nothing between March and September. So every `[P]` claim in this note stands at its original pin, and the §4.7 divergence is entirely a movement of the code away from a stationary design document.

## 7. Open questions

1. Does KRAM get a normative home, and where — the KERI spec, or a standalone specification? It is load-bearing for every non-key-event message and currently specified only in a personal repo.
2. Simple KRAM is what the glossary defines and what deployments run; full KRAM is what keripy now implements and what multiply-endorsed presentation needs. Nothing states the migration path or what a mixed network does.
3. The gap-attack analysis for cache-type *granularity* changes is marked unfinished in the whitepaper; keripy has an implementation. Which is authoritative?
4. `xip`/`pro`/`bar` pass through KRAM and then hit stubs. What is the intended downstream processing? **Still open at `b8f60166b`** — all three remain one-line `pass` stubs after a month of concentrated KRAM work (§5).
5. How does a receiver choose window classes in practice? The whitepaper gives constraints and example numbers but no policy guidance, and the choice is a security parameter. **Still open at `b8f60166b`** — `kraming.py` ships no defaults at all and validates only ordering and sign, so there is not even an implicit recommendation to read off the code (§5).

### Added 2026-09-15

6. **Do partially-signed entries survive threshold satisfaction?** The whitepaper says yes, deliberately, so that a receiver can learn the full set of endorsers rather than the first `k` of `n`; keripy at `b8f60166b` says no, deleting them at handoff on replay-safety grounds. Both are quoted at their pins in §4.7. This is the sharpest code-versus-design divergence the note currently holds, and it is not a formatting or vocabulary difference — the two policies produce different observable behavior for a late co-signer. Which governs? Was the whitepaper's rationale considered and rejected in `d70f670c7`, or not seen?
7. **Where is the rule that a `tsg`'s `(sn, said)` names the last establishment event written down normatively?** §3.1 shows two implementations getting it wrong in the same direction and correcting it independently within six days, each from failures rather than from a document. The rule is stated in a keripy docstring and nowhere in the KERI specification, the ACDC specification, or the KRAM whitepaper that this pass could find. Independent convergent error is the classic signature of an underspecified interface, and this one governs what a signature *means* — which key state it is checked against. A second implementation getting it wrong is evidence about the specification, not about the implementer.
8. **Does §3.1's rule interact with delegated or multi-sig rotation in a way not yet tested?** `lastEst` is well-defined for a linear KEL, but `test_stale_tsgs` covers the rotation case and the new tests cover the interaction case; superseding/recovery events and delegated establishment were not examined this pass. Flagged as unexamined, not as a problem.
9. **What is "KRAM PR #1788"?** A design decision quoted verbatim in `kraming.py:525-528` cites a PR that does not exist in `WebOfTrust/keripy` (404 as of 2026-09-15, and the repo is in the 1600s). The policy it justifies is implemented; its provenance is unresolvable. Possibly a typo, possibly a reference to another repository's numbering.
