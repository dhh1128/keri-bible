# KERI Specification — Doctrine Mining Notes

Source: `/home/daniel/code/kswg-keri-specification/spec/spec-body.md` (~48k words) plus `spec/termdefs.md`, `spec/terms-definitions/*`. Line numbers below are into `spec-body.md`.

---

## 1. What KERI fundamentally IS / IS NOT (worldview, root of trust)

- **Mission statement.** By exchanging KELs, each controller can validate the other's key state and "securely attribute (authenticate) any signed statements or any sealed issuances of data. This bootstraps the use of authentic data in any interaction... This is the mission of KERI." (§Direct exchange, L33)
- **Root of trust is cryptographic, not administrative.** "This root-of-trust is cryptographic, i.e. not administrative, because it does not rely on any trusted third-party administrative process but is established with cryptographically verifiable data structures alone." (§End-verifiable, L89)
- **No security dependency on any other infrastructure.** "everything in KERI or that depends on KERI is also end-verifiable; therefore, KERI has no security dependency on any other infrastructure, including conventional PKI. It also does not rely on security guarantees that may or may not be provided by web or internet infrastructure." (L88)
- **Self-certifying, self-administering, self-governing.** KERI gives each identifier "a primary root-of-trust based on self-certifying, self-administering, self-governing AIDs and ANs." (L89) "Autonomic means self-governing, self-regulating, or self-managing." (§AID, L111)
- **Decentralized derivation independent of DNS/IP.** "KERI AIDs are derived in a completely decentralized manner. The root-of-trust of a KERI AID is completely independent of the Internet and DNS addressing infrastructure." (§OOBI, L2631)
- **Purpose of the security overlay.** "The function of KERI's identifier-system security overlay is to establish the authenticity of the message payload in an IP Packet by verifiably attributing it to a Cryptonymous SCID (an AID) via an attached set of one or more asymmetric keypair-based nonrepudiable digital signatures." (L69)
- **Shared data but no shared governance.** The bifurcated architecture (promulgation vs confirmation) "is more succinctly characterized as shared data but no shared governance. This naturally supports a no-shared-secret approach to authentication." (L103)
- **Signed-everything / no-shared-secret.** "KERI takes a signed-everything approach to data both in motion and at rest. This enables a no-shared-secret approach to primary authentication." Passwords, bearer tokens, shared encryption keys are "all vulnerable to exploitation." (L101)
- **The secure binding triad → tetrad.** Overlay binds a triad: identifier ↔ keypairs ↔ controllers. (§KERI's secure bindings, L129) For transferable AIDs a fourth element, the KEL, is added to make a **tetrad** (KEL, identifier, keypairs, controllers) that persists bindings across rotation. (§Tetrad bindings, L162-182) "The essence of the KERI protocol is a strongly bound tetrad." (L182)
- **Goal = trust-spanning layer / universal DKMI.** "universal duplicity detectability and ambient verifiability with the goal of providing a universal DKMI in support of a trust-spanning layer for the internet." (§Ecosystem, L61)
- **Ambient verifiability.** "the source of any data can be verified anywhere, at any time, by anybody. Ambient verifiability removes any need to trust any of the components in the middle, i.e., the whole internet." (L97) End goal: "nearly anyone, anywhere, at any time, can become a verifiable controller of a verifiable identity that is protected by ambient verifiability." (L1884)
- **Identity meta-system enabling portability, not just interop.** AIDs build "an identity (identifier) meta-system... adds decentralized control... This enables portability, not just interoperability." → transitive trust → "an identity meta-platform for commerce." (§ANs, L214)
- **Design ethos: minimally sufficient means; many thin layers (Hourglass model).** "This also follows the design ethos of KERI of minimally sufficient means." "This approach follows the many thin layers approach of the Hourglass protocol model. BADA-RUN is a thin layer on top of KERI authenticity." (L2940, L2942)

## 2. Anti-patterns / outsider-tells KERI explicitly corrects (GOLD)

### PKI / X.509 / CA
- **Flaw 1 — mapping is merely ASSERTED, not verifiable.** "the mapping between the identifier (domain name) and the controlling keypair(s) is merely asserted by a trusted entity (a certificate authority or CA)... a Verifier cannot verify cryptographically the mapping... but must trust the operational processes of the CA." The cert "is not made with the controlling keypairs of the identifier but made with keypairs controlled by the CA." → evidence of authenticity of the assignment "but not evidence of the veracity of the mapping." (§Overcoming existing security overlay flaws, L81)
- **Flaw 2 — no cryptographic link across rotation.** "when rotating the valid signing keys, there is no cryptographically Verifiable way to link the new (rotated in) controlling/signing key(s) to the prior (rotated out)." CRL (RFC5280) + OCSP (RFC6960) "does not provide a cryptographically Verifiable connection between the old and new keys; This merely is asserted." (L83)
- **Rotation-by-assertion = starting over.** "Rotation by assertion with a new certificate... is essentially the same as starting over by creating a brand-new independent mapping." "could well be one of the main reasons that other key assignment methods, such as PGP's web-of-trust failed." (L83)
- **Ambiguity of multiple CAs.** "The lack of a single universal CRL or registry means that multiple potential replacements could be valid... for a given identifier, any or all assertions made by some set of CAs could be potentially valid." (L83)
- **KERI vs certificate transparency.** "Unlike certificate transparency, KERI enables the detection of Duplicity in the Key state via nonrepudiable cryptographic proofs of Duplicity, not merely the detection of inconsistency... that MAY or MAY NOT be duplicitous." (L85) Without KERI verifiability "the detection of potential ambiguity requires yet another bolt-on security overlay, such as the certificate transparency system." (L115)

### Blockchain / consensus / global ordering
- **Local ordering suffices; no global consensus needed.** "because the controller is the sole source of truth for the creation of any and all key events, it alone, is sufficient to order its own key events... a key event history does not need to provide double spend proofing of an account balance, merely consistency." Key events are "idempotent authorization operations as opposed to non-idempotent account balance decrement or increment operations. Total or global ordering may be critical for non-idempotency, whereas local ordering may be sufficient for idempotency." (§KAWA insight, L1836)
- **Single-phase agreement, not multi-phase commit.** "fault tolerance may be provided with a single-phase agreement by the set of witnesses instead of a much more complex multi-phase commit among a pool of replicants... security guarantees from KAWA may approach that of other BFT algorithms but without their scalability, cost, throughput, or latency limitations." (L1836)
- **KEL is "somewhat like a blockchain" that manages ONE AID.** "Each KEL is somewhat like a 'blockchain' that manages the key state for one and only one AID." (L31)
- **A duplicitous KEL is like a detectable 51% attack.** "A malicious controller producing a detectably duplicitous event history is tantamount to a detectable total exploit... analogous to a total but detectable exploit of any BFT ledger such as a detectable 51% attack on a proof-of-work ledger." (L1842)
- **Ledger only as last-resort tiebreaker.** In the extreme total-dead-exploit case, priority "may be through the use of anchor transactions on a distributed consensus ledger... would only require minimal use of a distributed consensus ledger." (L1888)

### Client/server, CRUD, CA-issued record IDs
- **RUN replaces CRUD.** "in a zero-trust (end-verifiable) decentralized peer-to-peer architecture, there is no client/server. Every host is a Peer. Each Peer MUST be the source of truth for its own data." CRUD (Create Read Update Delete) → **RUN (Read, Update, Nullify)**. "there is no Create action, only an Update action." "there is no Delete. Instead of Delete, Peers Nullify." (§RUN off the CRUD, L2923-2927)
- **Never truly delete (GDPR caveat).** Naive total erasure "exposes the data controller to a replay attack of erased data." Nullify keeps the record but marks it invalid (null value or boolean flag). (L2870, L2927)

### DNS/web/OOBI as untrusted bootstrap only
- **An OOBI is NOT trusted.** "an OOBI itself is not trusted but MUST be verified... any information obtained from the service endpoint provided in the OOBI MUST be verified by some other mechanism." (L2629) "a KERI OOBI by itself is considered insecure with respect to KERI." (L2633)
- **KERI needs no dedicated discovery network.** "KERI does not, therefore, need its own dedicated discovery network; OOBIs with URLs will do." (L2635) OOBIs may "safely use DNS/CA, web search engines, social media, email, and messaging as discovery mechanisms. The worst case is the OOBI fails." (L2942)

## 3. Security & threat-model doctrine

- **Survivability via detection, not prevention/invulnerability.** Overlay is "highly invulnerable to attack" only when bindings are cryptographically strong (~128 bits). (L135) But the core stance is duplicity-EVIDENCE + recovery, not prevention. "KERI thus enables the duplicity-evident exchange of data." (L51)
- **Zero-trust = never trust, always verify.** "end-verifiability is a prerequisite for true zero-trust computing infrastructure, where zero-trust means never trust always verify." (L103) "KERI follows a 'zero-trust' security model for authentic or securely attributable data. That means that data is signed both in motion and at rest." (L2864)
- **Malicious-controller stance.** Threat models split: malicious third party (honest controller) vs malicious controller. "the controller may also be malicious and, in some ways, may be indistinguishable from a successful malicious third party." (L1723) Duplicity by a controller is "potentially completely self-destructive with respect to the identifier." (L1842)
- **Observer/validator-dependent validity (LOCAL validity).** "Ultimately, a validator decides whether or not to trust the key state of a given AID based on the evidence or lack thereof of duplicity." "An honest validator MUST trust when there is no evidence of duplicity and MUST NOT trust when there is any evidence of duplicity unless and until the duplicity has been reconciled." (L53) A validator "MAY choose to use Judge and Jury services." Whether to treat its own first-seen copy as authoritative is "at the validator's discretion." (L1842)
- **Three protection axes.** "susceptibility to being attacked, vulnerability to harmfulness given an attack, and recoverability given a harmful attack. Security design involves making trade-offs between these three." (L1727)
- **Two harm cases.** Controller harm = loss/encumbrance of control authority; Validator harm = "acceptance of inconsistent verifiable events produced by a malicious entity." (L1728-1729)
- **Live vs Dead exploits.** Live = attacks on current/recent events (needs availability + consistency). Dead = attacks on past events (mitigated by duplicity detection/consistency). "One verifiable copy of a KEL (more specificly a KERL) is enough to detect duplicity in any other verifiable but inconsistent copy." (L1719)
- **Edge security > middle security.** "if the edges of the network are secure, then the security of the middle does not matter." "protecting one's private keys is much easier than protecting all internet infrastructure." (L99)
- **Cryptographic strength target ≈128 bits.** For perfect-security systems the seed/key needs ~128 bits entropy; brute force of 128 bits is computationally infeasible (worked example: a million supercomputers need ~2^33 ≈ 8.6 billion years). (§Annex A, L1698-1704) For signatures (not perfect-security) seed may need to be larger to preserve 128-bit strength. (L1698)
- **Ambient verifiability → asymmetry favoring defender.** "a successful dead attack requires the isolation of a validator from ambient sources of the KERL... isolation... may be prohibitively expensive. Consequently, ambient verifiability provides asymmetry between the attacker and the defender in favor of the defender." (L1884)

### Pre-rotation as firewall
- **Split control authority: signing vs rotation.** "control authority is split between keypairs that hold signing authority and keypairs that hold rotation authority." (§Pre-rotation, L1364) Each establishment event names current (signing) + next (pre-rotated, hidden as digests) sets and two thresholds. (L1364-1368)
- **Forward blind commitment.** "each pre-rotation makes a cryptographic future commitment to a set of one-time first-time rotation keys, later exploit of the current authoritative signing key(s) may not capture key rotation authority as it has already been transferred via the pre-commitment to a new unexposed set of keys." (L1628)
- **Attack surface reduced to the key STORE, not signing infra.** "an attacker cannot forge and sign a Verifiable Rotation operation without first unblinding the pre-rotated keys... the only attack surface available to the adversary is a side-channel attack on the private key store itself and not on signing infrastructure." (L1391)
- **One-time, first-time, only-time keys.** Pre-rotated keypairs "serve as first-time, one-time, and only-time rotation keys in the next rotation operation." "administrative (establishment operation) keys are first-time, one-time, and only-time use." (L1628, L1630)
- **No recovery once ROOT keys fully captured (unlike admin systems).** "In administrative identity systems, the binding... may be established by administrative fiat... used as a recovery mechanism... when the binding... is purely cryptographic (decentralized)... there is no recovery mechanism once the keys for the root control authority have been fully captured." (L1630)
- **Post-quantum via hidden pre-rotated keys.** Digests of public keys are post-quantum (Bernstein: quantum gives no advantage on hash collision). "a post-quantum attack that may practically invert the one-way public key generation... must first invert the digest of the public key using non-quantum computation. Pre-quantum cryptographic strength is, therefore, not weakened post-quantum." (L1711-1713) Blake2/Blake3/SHA3-256 keep 128-bit strength post-quantum. Controller can rotate to stronger quantum-safe functions over time → "computationally infeasible indefinitely." (L1680)
- **SQAR (Surprise Quantum Attack Recovery).** Partial+Augmented rotation to post-quantum-safe signing keys; assumes current signing keys & prior-next keys are NOT PQ-safe but prior-next DIGESTS are; rotation keys given weight 0 in new current signing threshold (rotation authority only). (§SQAR, L1578-1606)

### Dead-attacks (past events)
- Two types: **non-establishment dead-attack** (compromise stale signing keys → forge stale interaction event) and **establishment dead-attack** (compromise stale pre-rotated keys → forge stale rotation event). (L1634)
- Both need an **eclipse attack** (ref [24]) — get ahead of first-seen propagation. "Network propagation times are, at most, seconds and may be as little as milliseconds." (L1638, L1650)
- **Pre-rotation blocks establishment dead-attack:** "A subsequent rotation event that was not signed with the pre-committed next keys from the prior rotation would not be verifiable." (L1644) BUT witness pool gives no protection here — attacker can rotate in its own witnesses. (L1644)
- **Mitigation — one-time rotation keys via partial rotation.** Don't repurpose pre-rotated keys as signing keys; expose them only once for the rotation. (L1644-1646)
- **Deletion attacks always partially detectable.** "A partial deletion attack will always be detectable." A controller can replay a validator's own signed receipt to recover it from a deletion attack. (L1654)
- **Coincident inception+rotation trick.** To protect initial inception keys, create icp+rot together, emit as one, discard the incepting keys before emission. (L1658)

### Live-attacks (current events)
- **Non-establishment live-attack** recoverable via recovery rotation; witness pool helps only if witnesses require a unique secondary auth factor for local events. (L1670)
- **Establishment live-attack** (compromise unexposed next keys at/before first use) — "primary reason for pre-rotation is to mitigate the possibility." May "effectively and irreversibly capture control" if successful; witness pool gives no protection (attacker rotates in own witnesses). "protection... comes exclusively from the difficulty of compromising a set of pre-rotated keys before or at the time of their first use." (L1674-1676)
- **Delegated events get an EXTRA layer.** Attacker who compromises Delegatee's pre-rotated keys still needs the delegator's anchoring seal → "must either induce the delegator to issue a seal or must also compromise the delegator's signing keys." And superseding recovery is possible for delegated establishment live-attack (not possible for non-delegated). (§Delegated Event Live-attacks, L1688-1690)

## 4. Invariants and "never do X" / MUST rules

- **At most ONE valid KEL per AID (or none).** "In KERI, there MUST be at most one valid KEL for any identifier or none at all." "either there is one-and-only-one valid KEL or none at all, which also protects the Validator by removing any potential ambiguity about the Key state." (L178)
- **First-seen is permanent.** "first seen, always seen, never unseen." (§First seen, L49, L1788) Basis for duplicity detection. Any later compromise cannot supplant the first-seen version. (L49)
- **KEL is a doubly (backward + forward) hash-chained, nonrepudiably signed, append-only verifiable data structure.** (L176) Backward = digest of previous event; forward = commitment to next keys' digests (pre-rotation). (L31)
- **Exactly one inception.** "There MUST be only one Establishment event that is an Inception event. All subsequent Establishment events MUST be Rotation events." (L1378)
- **icp/dip sequence number MUST be 0**; every subsequent event `s` MUST be exactly 1 greater. Max sn = `ffff...f` = 2^128−1. (L323)
- **Version string `v` MUST be first field.** Regexable format `KERIMmmGggKKKKSSSS.` (protocol, major/minor version, genus, serialization, size, terminator). (L265) v2 impls MUST still support v1 version strings. (L273)
- **Drop unsigned messages.** "A Validator that receives a key event or non-key-event message that does not have attached at least one verifiable Controller signature MUST drop that message (i.e., not escrow or otherwise accept it). This protects the Validator from a DDoS attack." (L1266) Also L541.
- **Threshold satisfaction rules.** icp/ixn: sigs MUST satisfy current signing threshold. (L1258) rot/drt: MUST satisfy BOTH current signing threshold AND prior-next rotation threshold. (L1262) Witness-indexed sigs MUST satisfy current witness threshold ("threshold of accountable duplicity") when witness list non-empty. (L1264)
- **Abandonment signal.** Rotating to a null (empty) next key list signals the controller has abandoned the AID; "no more key events MUST be allowed in its KEL." (L340, L174) Empty `n` in inception → non-transferable. (L340)
- **Non-transferable = ephemeral, MUST be abandoned on key weakness.** A basic SCID "does not support Rotation... and therefore MUST be abandoned once the controlling private key becomes weakened or compromised." (L107)
- **AID = digest → `d` and `i` identical.** For a self-addressing inception, `d` and `i` MUST have the same value and same derivation code; validation requires `d` == `i` if `i` is a digest type. (L1380-1381)
- **Field labels: fixed type, fixed order.** A label "MAY have different values in different contexts but MUST NOT have a different field value type." (L251) Top-level fields MUST appear in the specified order; all REQUIRED; no extra top-level fields allowed. (L261, per-message ordering L556, L623, L627, L665, L746, L815)
- **Witnesses MUST be non-transferable.** Backer AIDs, when witnesses, "MUST be non-transferable, fully qualified public keys" so a validator can verify a witness signature straight from the AID; witness needs no KEL. (L353, L1252)
- **AID MUST NOT appear twice in a backer / backer-add / backer-remove list;** removes processed before adds. (L358, L362)
- **Establishment-Only (`EO`) config trait** forbids interaction events → all events signed by first-time one-time pre-rotated keys → repeated signing-key exposure impossible. Validator MUST drop non-establishment events. (L377)
- **Do-Not-Delegate (`DND`)** — validator MUST drop delegated events whose delegator has this trait. (L379)
- **Controller MUST validate its own events / be its own validator.** "every controller MUST also be a validator for its own AID." (L1758) Local (protected) vs remote (untrusted): controllers/witnesses/delegators SHOULD NOT sign or accept REMOTE events. (§Validation Rules, L1772-1782)
- **Delegator approval bound to witness change.** "The approval logic of the delegator SHOULD NOT automatically approve a delegable rotation event unless that event's change to the witness pool is below the witness pool's prior threshold." (L1778)

## 5. Precise terminology / definitions

- **AID (Autonomic Identifier)** — "a self-managing cryptonymous identifier that must be self-certifying (self-authenticating) and must be encoded in CESR as a qualified Cryptographic primitive." (termdefs) Generalized enhanced SCID that is persistent via pre-rotation. (L111)
- **SCID (Self-Certifying Identifier)** — a Cryptonym uniquely cryptographically derived from the public key of an asymmetric keypair. Basic SCID is ephemeral (non-rotatable). (L107, termdefs)
- **AN (Autonomic Namespace)** — a namespace with an AID as prefix; self-certifying → self-administering. "All derived AIDs in the same AN share the same root-of-trust, source-of-truth, and locus-of-control (RSL)." (termdefs)
- **AIS (Autonomic Identity System)** — identity system with primary root-of-trust in self-certifying identifiers strongly bound at issuance to a signing keypair. (termdefs)
- **Controller** — "an entity that can cryptographically prove the control authority over an AID and make changes on the associated KEL." Can be multi-sig (multiple entities). (termdefs) Controller app has 5 functions: keypair generation, keypair storage, key event generation, key event signing, key event validation. (L10)
- **Validator** — "determines that a given signed event associated with an AID was valid at the time of its issuance." MUST first act as a verifier. (L1740)
- **Verifier** — "cryptographically verifies an event message's structure and its signature(s)"; establishes control authority for the event at issuance. (L1737) (Verifier ⊂ Validator: validator adds witnessing/delegation validation + acceptance into KEL.)
- **KEL (Key Event Log)** — "a Verifiable data structure that is a backward and forward chained, signed, append-only log of key events for an AID. The first entry... must be the one and only Inception event." (termdefs) DAG of events; undisputed path = **trunk**, superseded branches = **disputed**. (L1788)
- **KERL (Key Event Receipt Log)** — a KEL that also includes all consistent key event receipt messages from the witnesses. (termdefs) Deletion-proof immutable log provided by witnesses. (L1846)
- **Key event** — serialized entry in a KEL. Types: `icp`, `rot`, `ixn`, `dip`, `drt`. (L1748)
- **Establishment event** — a key event that establishes or changes key state (icp, rot, dip, drt). **Non-establishment event** = ixn (anchors data, no key-state change). (L1751-1752) Sub-class: delegated establishment (dip, drt). (L1754)
- **Key state** — current public keys + thresholds + pre-rotated key digests + thresholds + witnesses + thresholds + configuration. Time-dependent; established at inception, evolves via rotation. (termdefs)
- **Duplicity** — "the existence of more than one Version of a Verifiable KEL for a given AID." (termdefs) "A duplicitous event is defined as a verified but different version of an event at the same location." (L1744) Requires TWO fully-signed-and-witnessed versions → only possible via key compromise or controller acting duplicitously (indistinguishable to a watcher). (L51)
- **Version** — "an instance of a KEL... in which at least one event is unique between two instances." (termdefs)
- **First-seen (`fn`)** — first instance of an event received; always seen, never unseen. A monotonic ordinal `fn` stored alongside each event, distinct from `sn`; different KEL copies may assign different `fn` to same-`sn` events. (termdefs, L1788, L1799)
- **Witness** — entity/component DESIGNATED (trusted) by the controller; verifies, signs (receipts), keeps events. Controller of its own non-transferable AID. Under ultimate control of the AID's controller; controller may change witness pool at will. (termdefs, L43)
- **Backer** — alternative to a witness, commonly using DLT to store the KEL. Ledger registrar backers anchor key events (or their SAIDs) on a ledger; require `RB` config trait + Registrar Backer Seal. (termdefs, L345, L494)
- **Watcher** — keeps a copy of a KERL but is NOT designated by the controller. Under control of the VALIDATOR, not the controller. Not AID-specific, not managed by key events (kept confidential/unknown to attackers). Follows first-seen. (termdefs, L45)
- **Juror / Jury** — a watcher that records & provides evidence of duplicity (keeps a Duplicitous Event Log, DEL) to other watchers; may be a fault-tolerant pool (Jury). (L51, L1858)
- **Judge** — a watcher that evaluates key events based on duplicity evidence from Juries. (L51)
- **Seal** — "a cryptographic commitment in the form of a cryptographic digest or hash tree root (Merkle root) that anchors arbitrary data... to a particular event in the key event sequence." (termdefs) "evidence of authenticity" while maintaining confidentiality; binds external data to key state at the seal's location; ordering of seals = verifiable ordering of endorsements. (L395)
- **SAID (Self-Addressing Identifier)** — content-addressable + self-referential digest; the SAID is included in the data (SAD) it identifies. (termdefs, L302) A signature on a SAID ≡ a signature on the full serialization (collision resistance). (L306)
- **SAD (Self-Addressed Data)** — the block/serialization from which a SAID is derived and which encapsulates it. (termdefs, L302)
- **Cryptographic primitive** — serialization of a value from a crypto operation (digest, salt, seed, private key, public key, signature). **Qualified** primitive prepends a CESR derivation code (proem). ALL primitives in KERI MUST be CESR-expressed and are qualified by construction. (§Qualified Cryptographic Primitives, L119)
- **DKMI** — decentralized key management infrastructure not reliant on a single entity; disparate entities agree on key state. (termdefs)
- **KAWA** — KERI's Algorithm for Witness Agreement, a type of BFT algorithm; single-phase; provides high availability + fault tolerance. (termdefs, L1830)
- **OOBI** — Out-Of-Band Introduction; associates a URI/URL with an AID/SAID; not trusted, must be verified; bootstraps Percolated Information Discovery (PID). (L2629)
- **EGF** — not found in spec-body (ecosystem governance framework is a ToIP term, not defined here). GAP.

## 6. Data structures, fields, message types

- **Reserved field labels** (L232): `v` version string, `t` message type (3-char), `d` digest SAID (of enclosing block), `i` identifier/controller AID, `s` sequence number (hex, no leading zeros), `p` prior SAID, `kt` signing threshold, `k` signing keys, `nt` next threshold, `n` next key digests, `bt` backer threshold, `b` backer list, `br` backers-to-remove, `ba` backers-to-add, `c` config traits, `a` anchors/seals, `di` delegator AID. Routed adds: `u` UUID salty nonce, `ri` receiver AID, `x` exchange SAID, `dt` ISO datetime, `r` route, `rr` return route, `q` query map. (L949)
- **Message classes/types** (L281): Key events `icp` (inception), `rot` (rotation), `ixn` (interaction), `dip` (delegated inception), `drt` (delegated rotation); Receipt `rct`; Routed `qry`/`rpy` (query/reply), `pro`/`bar` (prod/bare), `xip`/`exn` (exchange inception / exchange).
- **Compact labels rationale.** One/two-char labels minimize over-the-wire signed bytes for resource-constrained (IoT/supply-chain) apps; a verbose semantic overlay can be applied AFTER verification. (L257)
- **Serializations.** JSON, CBOR, MGPK, or native CESR; each top-level message body in a stream MAY use a different serialization; version string enables deterministic stream parsing. (L224, L269) Canonical serialization relies on insertion-ordered field maps. (L222)
- **Seals** — count codes (L407): `-Q` DigestSeal `[d]`, `-R` MerkleRootSeal `[rd]`, `-S` SealSourceCouples `[s,d]`, `-T` SealSourceTriples `[i,s,d]` (key event seal), `-U` SealSourceLastSingles `[i]` (latest establishment event), `-V` BackerRegistrarSeal `[bi,d]`, `-W` TypedDigestSeal `[t,d]`; each has a big-size `--` variant.
- **Seals hide data but bind it.** A seal is a digest → binding is public, data is not; with a salty-nonce (UUID) even a rainbow-table attack can't discover the data → "sealed confidential." (L931)
- **Indexed signatures.** CESR indexes a signature to a public key in the establishment-event key list → only the index attaches, not the key. Controller-indexed (into current signing list ± prior-next digest list; rot needs up to TWO indices) vs witness-indexed (into effective witness list). (L1246-1256) Second index looks up prior-next digest, first index the exposed key, verify digest, then verify signature. (L1256)
- **Endorsements** — non-controller, non-witness signatures (e.g., a watcher endorsing the version it saw); attachment must include the endorser's AID. (L1276)
- **Sealing = indirect signature that persists across key-state change** — the big advantage over a direct endorsement: validity "persists in spite of later changes to the key state... essential for unbounded term but verifiable issuances," and enables issuance under one key state with revocation under another. (L1280, L395)
- **Receipts** — a receipt (`rct`) is NOT a key event; it references a key event's SAID; the attached signature is on the referenced key event, not the receipt body. Enables asynchronous distribution of signatures. (L882, L1286)

## 7. Delegation (cooperative)

- **Cooperative = two-event, two-way peg.** A delegation = a delegating event in the delegator's KEL (containing a seal of the delegated event) + a delegated event in the Delegatee's KEL (containing the delegator's AID via `di`). "Both MUST participate." (§Cooperative Delegation, L1610-1612)
- **Delegatee AID = digest of its dip event (which references delegator's AID)** → cryptographically binds Delegatee to delegator. (L1616)
- **Delegator retains establishment control authority;** Delegatee gets "revokable signing authority." (L1618) Enables horizontal scalability of signing.
- **Joint-compromise requirement (distinctive security feature).** "any exploiter that merely compromises only the delegate's authoritative keys may not capture the control authority... A successful exploiter must also compromise the delegator's authoritative keys." Conversely compromising only the delegator's signing keys can't force a delegated rotation without the Delegatee's pre-rotated keys. "Both sets of keys must be compromised simultaneously." (L1622)
- **Config traits:** `DID` (Delegate-Is-Delegator) treats delegatee as equivalent to delegator (horizontal scaling); `DND` (Do-Not-Delegate) prevents delegation. Delegation seals in interaction events are less secure (ixn less secure than rot). (L379-381)

## 8. Superseding recovery & reconciliation

- **KEL is a DAG; reconciliation finds the trunk.** If validators cannot universally find the same undisputed path, the KEL is **irreconcilable** → not trusted. (§Reconciliation, L1790)
- **Recovery ≠ escaping accountability.** "Because events are signed nonrepudiably, any key compromise is still the responsibility of the controller... still may be held accountable for any harm." Recovery only repairs the KEL for FUTURE validators; those who already first-saw the compromised events still saw them. (L1792)
- **Superseding rules (L1804-1825):**
  - A0: a rotation may supersede an interaction at the same `sn` (if that ixn is not before another rotation). A1: a non-delegated rotation may NOT supersede another rotation. A2: an interaction may NOT supersede any event.
  - B: a delegated rotation may supersede the LATEST-SEEN delegated rotation at same `sn` under conditions B1/B2/B3 (delegating event later in delegator's KEL; or same delegating event but seal appears later; or superseding delegating event is a rotation superseding the superseded's delegating interaction).
  - C: recurse up delegation chain to the root (non-delegated) KEL; if neither A nor B satisfied at root, discard the superseding rotation.
- **Latest-seen constraint limits delegated recovery.** "recovery can not happen for any compromise of pre-rotated keys, only the latest-seen." An attacker who does a compromised delegated rotation AND a following (approved, non-superseding) rotation makes recovery impossible. (L1825)

## 9. KAWA (witness agreement) doctrine

- **Controller is sole source of truth → local ordering suffices** (see §2 anti-blockchain).
- **Immunity constraint.** For N witnesses there is a threshold M<N guaranteeing at most one sufficient agreement (or none), despite a dishonest controller, when at most F*=N−M unavailable and F<M duplicitous. "the service may not produce multiple divergent but proper KERL." (L1866-1868) Validator selects M to make the service immune → protects itself.
- **Threshold of accountable duplicity.** Controller declares tally M in inception config; "the controller accepts accountability for an event when any subset M of the N witnesses confirms that event." (L1846, L1850)
- **Round-robin dissemination scales linearly (2·N); gossip scales N·log N.** (L1860-1862)
- **Ambient duplicity detection.** Observers (watchers/jurors/judges) may be under validators' control not controllers' → "a malicious alternate (duplicitous) event history may be eminently detectable by any validator." (L1842)
- **Colluding controller + witnesses** violates the ≤F assumption; KAWA can't protect — protection then comes from validator-side duplicity detection across a large diverse observer set. (L1874)
- **Proof of priority via mutual interaction.** A validator anchoring the controller's interaction event in the validator's own event → "A total compromise of the controller and all witnesses would not be able to forge the validator's signature." (L1886)
- **Direct vs indirect mode.** Direct: validator ≈ implicit witness, receives KELs directly. Indirect: via witnesses (promulgation) and watchers (confirmation). (L27-47, L1846)

## 10. OOBI / BADA-RUN / discovery doctrine

- **Percolated discovery (SPED).** OOBI bootstraps Percolated Information Discovery based on Invasion Percolation Theory. "Because the information so discovered is end-verifiable, the percolation mechanism does not need to be trusted. Percolating intermediaries do not need to be trusted." (L2841) JIT/NTK: exchanger must already have verified data before exchanging → percolates proofs just-in-time; avoids global discovery infra. (L2845)
- **OOBI forms:** basic `(url, aid)` tuple; IURL (AID in path, role/name in query); well-known `/.well-known/keri/oobi/<AID>`; CID+EID verbose; MOOBI (multi-URL); reply-message OOBI (`r` starts `/oobi`); SOOBI (bare URL, blind self-introduction). (L2639-2827)
- **SOOBI security value.** Only place a witness AID (WID) MUST appear is the KEL, not every config file → avoids config-based DDoS from "corrupted, inconsistent, redundant configuration information." (L2827) "Redundancy for security is best applied in the context of a self-healing or resilient threshold structure." (L2827)
- **OOBI worst case = failed discovery or DDoS, never cache-poison.** "an OOBI may be part of a DDOS attack but not as part of a service endpoint cache poison attack." (L2831) OOBI+MFA (OOBA) mitigates DDoS. (L2836)
- **BADA (Best-Available-Data-Acceptance).** Guarantees MONOTONICITY of updates to signed data at rest → protects against replay attacks. (L2858) Two attacks on data-at-rest: **replay** and **deletion**. Non-interactive monotonic ordering (sequence number / datetime) preferred over interactive nonce exchange (which adds latency/scaling limits). (L2866)
- **BADA acceptance rules.** KEL-anchored updates: accept if no prior, else accept if update's anchor is later in the KEL than the prior's anchor. (L2887-2895) Signed-not-anchored updates: accept if no prior; else compare key-states, later key-state wins; if same key-state location, later datetime wins (datetimes relative to CONTROLLER's clock). (L2907-2918)
- **Deletion mitigation = redundancy.** Keep redundant copies (only digest/signature needed for stale-replay detection); compare hosts to expose deletion. (L2872)
- **OKEA (OOBI KERI Endpoint Authorization).** Principal Controller authorizes a Player (component AID) to act in a Role; Player signs its endpoint URL; both under BADA-RUN. Some players (witness/registrar backers) implicitly authorized by KEL designation but still need an explicit signed endpoint (URL/scheme) message. (L2930-2936)

## 11. Worked examples / real-world usage

- Cast of characters: **Ean** (issuer AID `EPR7FWsN3tOM8PqfMap2FRfF4MFQ4v3ZXjBUcMVtvhmB`), **Fay** (delegatee AID `EHqSsH1Imc2MEcgzEordBUFqJKWTcRyTz2GRc2SG3aur`, delegator=Ean). Ean's icp uses `kt=2` of 3 keys, `nt=2`, 4 witnesses `bt=3`, config `["DID"]`. (L562-619)
- Full JSON examples for icp/dip/ixn/rot/drt/rct/qry/rpy/pro/bar/xip/exn message bodies with exact serializations (L562-1238). Delegated events use fractional thresholds `["1/2","1/2","1/2"]`. drt does NOT carry `di` (inherits from dip). (L815)
- Two-way peg example: Ean's ixn (`s=1`) seals Fay's dip via a SealEvent `[i,s,d]` in the anchor list; Ean's rot (`s=2`) seals Fay's drt. (L661, L742)
- Exchange transaction (IPEX-style): `xip` offer (Fay sells Rembrant $300000) → `exn` agree (Ean buys); `x` = SAID of xip binds the set, `p` chains order. (L1152-1238) Route `/ipex/offer` example: head defines transaction type, full path defines the step. (L992)
- **Reproducibility setup.** Examples generated by unit tests in `tests/spec/keri` in keripy. Deterministic non-random salt `b'kerispecworkexam'` (and `b'acdcspecworkexam'`); Salter → Argon2 (crypto_pwhash, ARGON2ID13) stretches salt+path → Ed25519 seed → Signer/Verfer. Witness salt `b'acdcspecworkwits'`, non-transferable. (§Working Examples Setup, L1900-1985)

## 12. Threshold mechanics (detail)

- **Simple M-of-N** (hex integer) or **fractionally weighted** (list of clauses of rational fractions). (L327) Clauses ANDed; a clause is satisfied when its verified-signature weights sum to ≥1. Rational fractions avoid float rounding errors. (L1419) `[1/2,1/2,1/2]` ≡ "2 of 3." (L1421) Nested weighted lists for multi-device contributors (normalize a contributor's own fractional threshold to a single weight). (L1466)
- **General pre-rotation:** Partial rotation (hold some pre-rotated keys in reserve) + Augmented rotation (add new non-pre-rotated keys). A rotation's current key list MUST be satisfiable w.r.t. BOTH prior-next and current thresholds. (§General Pre-rotation, L1470-1498)
- **Reserve rotation** — reserve keypairs contribute to availability/fault-tolerance without needing to participate unless a non-reserve member is unavailable; enables provisional/custodial/escrow control authority. (§Reserve Rotation, L1501-1543)
- **Custodial rotation** — custodian holds signing authority (current keys), owner holds exclusive rotation authority (next keys, weight 0 for exposed rotation keys in new current threshold) → owner can revoke custodian's signing authority unilaterally. (§Custodial Rotation, L1545-1576)

---

## Gaps / not covered by this source
- **CESR internals** — the spec repeatedly defers all primitive/derivation-code/domain (Text/Binary/Raw) details and the version-string grammar to the separate CESR specification [ref 1]. Composability, 24-bit alignment mentioned only in summary (L119-125). Native CESR message encodings (L2063-2626) skimmed, not deeply mined — that section has the CESR field-encoding tables and count codes.
- **ACDC / TEL / IPEX** — referenced (TELs monotonically ordered vs KEL anchoring seals, L2868; ACDC revocation registries) but defined in the ACDC spec, not here. IPEX only appears as a route example.
- **EGF (ecosystem governance framework)** — not defined in this source (ToIP-layer term).
- **Multisig group inception mechanics** (how multiple controllers jointly form one AID) discussed abstractly via thresholds but no worked multi-controller-coordination example.
- **Witness rotation cut/graft receipts protocol details** and exact KAWA agreement message flow are described narratively, not as a formal state machine.
- **Full bibliography** (L3091+) not transcribed; references cited by number [1]=CESR, [4]=KERI-WP, [24]=EclipseAttack, [25-28]=Percolation theory.
- Line references are approximate (into spec-body.md as of this read); headings are stable anchors.
