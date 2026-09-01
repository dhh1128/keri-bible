# Doctrine Mining: KRAM — the KERI Request Authentication Mechanism

**Primary source:** `SmithSamuelM/Papers`, `whitepapers/kram.md`, **v0.7.6**, branch `master`. Last substantive commit `67550b47` (2026-03-06, "updated KRAM spec to clarify that we leave the partially signed database entries in place until prune time"). Fetch with `gh api repos/SmithSamuelM/Papers/contents/whitepapers/kram.md --jq .content | base64 -d`.
**Second primary source:** WebOfTrust/keripy discussion [#934](https://github.com/WebOfTrust/keripy/discussions/934), *KERI Architectures for Group Issuance (KAGI) and KRAM*, SmithSamuelM, 2025-01-30. This is Sam in his own voice on *why* KRAM exists and why only the weak version shipped.
**Third source:** `WebOfTrust/kram` `README.md` (repo last pushed 2024-07-06). An earlier, shorter subset of the same text — the "Interactive vs. Non-interactive", "Replay Attack Protection" and "Timeliness and Caching" sections, without simple/full KRAM, without the multisig treatment, without the v0.7 redesign. Superseded; cite the Papers version.
**Implementation:** `WebOfTrust/keripy` `upstream/main` @`4df8e4a8` (2026-09-01); `src/keri/core/kraming.py` @`fe161709` (2026-08-20), 2224 lines; `tests/core/test_kraming.py`, 5768 lines. Implementation-tracking issues: [#937](https://github.com/WebOfTrust/keripy/issues/937) *KRAM Implementation* (open, arilieb, 2025-02-22, which names the whitepaper as the target), [#1302](https://github.com/WebOfTrust/keripy/issues/1302) *KRAM: Current state and gaps* (KeaxD, closed 2026-03-25).
**Mining date:** 2026-09-01.

---

## 0. Provenance and status — read before citing

Four things about this source set are load-bearing, and three of them are easy to get wrong.

**KRAM is not in the KERI specification, and the near-miss is a glossary entry.** A search for "kram" across `trustoverip/kswg-keri-specification` returns exactly one file, `docs/versions/v1/index.html`, and the hit is not spec text: it is an external cross-reference entry pulled from `trustoverip/kerisuite-glossary` (declared as `external_spec: "keri1"` in `specs.json:26`). The whole of it is one sentence — *"All requests from a web client must use KRAM (KERI Request Authentication Method) for replay attack protection. The method is essentially based on each request body needing to include a date time string field in ISO-8601 format that must be within an acceptable time window relative to the server's date time"* — followed by a link to the `WebOfTrust/kram` repo. `spec/spec-body.md` does not mention it. So the spec's only account of KRAM is a glossary gloss of *simple* KRAM, sourced outside the spec repo, in a rendered v1 artifact.

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

---

## 5. keripy implementation status — verified at `upstream/main` @`4df8e4a8` (2026-09-01)

**The redesign is built.** `src/keri/core/kraming.py` is 2224 lines with a 5768-line test file, and it tracks v0.7.6 closely rather than the older strata:

- `AuthTypeCodex` with exactly `asr`/`assk`/`asmk` (`kraming.py:38-51`).
- `Kramer.intake` implements the whitepaper's denial-check-then-`kramit` shape almost line for line (`kraming.py:963-969`), including the `md.startswith(d)` prefix match.
- `_fetchCacheType` implements the reduced three-level cascade — `msgType.R.route`, then `msgType`, then a default catchall (`kraming.py:276-308`). The catchall key is `"~"`, chosen so it sorts last in LMDB, where the whitepaper says "default".
- 14 KRAM sub-databases in `basing.py:737-856`: cache-type `ctyp.`, message cache `msgc.`, transactioned cache `tmsc.`, transaction-opener datetimes `xdt.`, partially signed message/signature/sender-key-state `pmkm./pmks./pmsk.`, plus one per non-authenticator attachment type (`kramTSGS`, `kramSSCS`, `kramSSTS`, `kramTRQS`, `kramFRCS`, `kramTDCS`, `kramPTDS`, `kramBSQS`, `kramBSSS`, `kramTMQS`).
- Multi-key accumulation with key-state-change detection: a stored `(sn, said)` establishment reference is compared against the current kever and the message is dropped if the sender rotated mid-collection (`kraming.py:1094-1103`).
- Reconfiguration safety is implemented, not just specified: `changeConfig`, `reconcileConfig`, `_buildCoverageGraph`, `_computeCoverageDiff`, `_computeWorstCaseDelta`, `_validateCoverage` (`kraming.py:1552-2093`) — i.e. someone did work out the granularity case the whitepaper left open.
- `Pruner`, an hio `Doer` on a 1 s period, driving `_pruneMessages` and `_pruneExchanges` (`kraming.py:2162-2221`).

**The `processMsg` refactor the whitepaper asks for exists.** `Kevery.processMsg` (`eventing.py:4681`) is the consolidated entry point for `qry, rpy, pro, bar, xip, exn`, documented with the whitepaper's exact three steps: AID allow/deny, then `self.kramer.intake()`, then message-specific dispatch. `processXip`, `processPro` and `processBar` are stubs (`eventing.py:4816-4826`).

**Enablement.** `Kevery.__init__` takes `enableKram=False` (`eventing.py:4136`) — so KRAM is off unless asked for — but the two runtimes that matter pass `enableKram=True`: `directing.py:470` and `indirecting.py:76`. **"Default-disabled" is true of the class and misleading about deployments.**

**Built-in OOBI carve-out.** `Kramer.OobiDenials` hard-codes `rpy /end/role` and `rpy /loc/scheme` as denials merged in whenever KRAM is enabled (`kraming.py:98-147`), because *"OOBI endpoint discovery replies rely on BADA acceptance rather than KRAM replay protection"*. This is §4.4's BADA conflict, resolved in code.

**Implementation history.** #1302 (closed 2026-03-25) records that PR #1288 landed the core "aligned with the v0.7.5 whitepaper" and lists as *gaps*: attachment databases, the pruning doer, keystate-retrieval cueing, AID allow/deny, and keeping signature collection alive until the prune window. Every one of those is present at `upstream/main` today.

**Two divergences worth checking.**

1. **Cache-type route matching is exact, denial route matching is a prefix.** `_fetchCacheType` compares `key == f"{msgType}.R.{route}"`; `intake` uses `md.startswith(d)`. So a cache-type configured for route `/end` does not govern a message routed `/end/role`, while a denial configured for `/end` does deny it. The whitepaper's "most specific matching" language does not settle which was intended.
2. **The v0.7.6 gap-attack machinery assumes windows only ever change through `changeConfig`.** Cache entries store their own `(d, ml, pml, xl, pxl)` at creation precisely so in-flight caches are immune to reconfiguration; that invariant is worth a test if one does not exist.

---

## 6. Where KRAM is *not*

- **Not in the KERI spec.** See §0. A glossary xref describing simple KRAM is the whole of it.
- **Not in the ACDC or CESR specs.** No mention.
- **No timeliness enforcement in KERIA's admin auth.** `WebOfTrust/keria` main signs over `Signify-Timestamp` as one of `Authenticater.DefaultFields` (`src/keria/core/authing.py:81`) and stamps responses with `nowIso8601()` (`:180`), but no window comparison against the server clock appears in `authing.py`, `httping.py` or `agenting.py` (searched 2026-09-01). The request is *bound* to a timestamp by the signature; nothing observed *rejects* a stale one. This is a negative search result, so treat it as a question for a maintainer rather than a finding — but it is the exact shape of "simple KRAM without the window."
- **No module in keripy named for simple KRAM.** The deployed simple-KRAM behavior Sam describes is distributed across message handling and the HTTP layer rather than centralized, which is part of why full KRAM needed the `processMsg` consolidation before it could be wired in.

## 7. Open questions

1. Does KRAM get a normative home, and where — the KERI spec, or a standalone specification? It is load-bearing for every non-key-event message and currently specified only in a personal repo.
2. Simple KRAM is what the glossary defines and what deployments run; full KRAM is what keripy now implements and what multiply-endorsed presentation needs. Nothing states the migration path or what a mixed network does.
3. The gap-attack analysis for cache-type *granularity* changes is marked unfinished in the whitepaper; keripy has an implementation. Which is authoritative?
4. `xip`/`pro`/`bar` pass through KRAM and then hit stubs. What is the intended downstream processing?
5. How does a receiver choose window classes in practice? The whitepaper gives constraints and example numbers but no policy guidance, and the choice is a security parameter.
