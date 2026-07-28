# Dossier Doctrine Dossier (KSWG Dossier Specification + KERI/ACDC/CESR primer & refs)

Sources:
- `spec/dossier-spec-body.md` — the normative Dossier spec body
- `.ref/keri-primer.md` — "A Primer on KERI, ACDCs, and CESR" (19 Dec 2025)
- `.ref/issuance-ref.md` — issuance/multisig/coordination technical summary
- `.ref/operators-ref.md` — ACDC Edge Operators reference

---

## 1. What a Dossier fundamentally IS / IS NOT (worldview & design intent)

- **A dossier IS itself an ACDC.** "A dossier MUST be a valid Authentic Chained Data Container (ACDC)" (dossier-spec-body.md §"Core Structure"). It is not a new container format — it is a *usage pattern* of ACDC.
- **A dossier is a curated BUNDLE of evidence, not a set of direct claims.** "The primary payload of a dossier is not a set of direct claims, but rather a graph of references to external evidence" (§"The Edges Attribute"). The substance of the assertion enters *exclusively through edges*.
- **The dossier's `a` (attributes) section is inverted vs. a normal credential.** In a conventional credential the `a` section carries the issuer's claims about a subject; in a dossier the substance is the evidence graph and "The `a` section MUST NOT be used to carry primary evidence" — it is reserved for *proximate metadata* (facts about the dossier itself) (§"The Attributes Section"). Concrete illustration: crash photos/diagram/witness statements are edges (evidence); the adjuster's name, case number, assembly date, governance framework are `a`-section metadata.
- **What the issuer's signature attests is composition/integrity, NOT veracity.** "The issuer does not necessarily attest to the veracity of the claims within the evidence, but rather to the integrity and composition of the collection itself" (§"The Role of the Issuer"). The signature asserts: at issuance time, this collection is exactly the collection the issuer intended to present.
- **A dossier is intentionally HEAVY, designed for REUSE.** "A dossier is intentionally heavy... This cost is acceptable because a dossier is designed for reuse: curation happens once, and the resulting artifact serves as an authoritative reference for many later transactions" (§"Dossiers and Derivative References"). Curation is amortized across many transactions.
- **Dossiers are persistent, evolving artifacts** with a lifecycle: "curation, iterative assembly, state management, citation, and verification" (§"The Operational Lifecycle").
- **Design purpose:** aggregate "an arbitrary quantity and variety of evidence" (§"The Edges Attribute"); a dossier MAY contain an unbounded number of edges.

## 2. Invariants and "never do X" rules (dossier spec)

Normative MUSTs / MUST NOTs / SHOULDs:
- Dossier **MUST** be a valid ACDC.
- Schema **MUST** be an `allOf` array with one member a `$ref` to the base dossier schema *by SAID* (base dossier schema SAID `ECpZgR2Ybj2QCfFZrnNQUqhbLnZuMl5cjL2MtgDaxMbY`). The `$ref` "signals that the schema is for a dossier and should be processed using the dossier semantics."
- **MUST** use the ACDC `e` (edges) section to bind the dossier to all *evidenta*, and **MUST NOT** place any evidenta in the `a` section.
- **MUST** define `a`-section fields for proximate-metadata.
- **SHOULD NOT** include an issuee field (a dossier is issuee-less).
- **SHOULD** set `additionalProperties: true` at root and for the edges object, so issuers can add arbitrary application-specific edges without invalidating against the base schema.
- **MAY** include ordinary (non-evidenta) ACDC-relationship edges too.
- Foreign Artifact wrapper **MUST** be a valid ACDC with no issuee; its `a` section **MUST** contain `content_digest` (CESR-encoded hash) and `content_type` (IANA MIME type); `content_digest` **SHOULD** be a bSAID or xSAID.
- Derivative **MUST** cryptographically bind to the dossier (minimally by including the dossier SAID under the derivative's signature); a derivative **MUST NOT** be treated as independent evidence — "its authority derives entirely from the dossier, and its trust value collapses to that of the dossier alone if the binding cannot be checked."
- When evaluating a derivative, a verifier **MUST** consult the dossier's revocation state effective at *verification time*, not derivative-issuance time. "A token issued before its referenced dossier was revoked is not valid after the revocation event, even if the token's own `exp` has not yet passed."
- Any protocol citing a dossier **MUST** incorporate ephemeral, context-specific signed data (timestamps, originator/destination IDs, nonces) to defeat replay.
- To manage evidence state transitions, dossiers **MUST** use Annotation Edges (because ACDCs are immutable, an issuer "cannot simply modify the metadata of an existing edge"). Verifiers **MUST** traverse the graph to resolve the "effective state" of each evidence item, applying the latest annotations.
- To include dynamic data, issuers **MUST** use Temporal Pinning (never link a live API directly — "Direct links to live APIs are unverifiable in a static context").
- An active "no" in joint issuance **MUST** be a signed declination, "never as a null or unsigned slot" (a pending slot and an absent slot are equivalent in trust terms).

**Anti-pattern explicitly corrected — direct reference to non-ACDC material:** "Direct reference to non-ACDC material without a wrapper is NOT RECOMMENDED, as it places an untenable burden on the verifier to parse and validate an arbitrary foreign format, understand its lifecycle, and locate its revocation mechanism" (§"Incorporating Evidence"). RECOMMENDED approach: wrap foreign material in a new ACDC before linking.

## 3. Incorporating evidence — three evidence categories

1. **ACDC-native evidence** — edge value MUST be a JSON object with at least `n` (SAID of referenced ACDC — "direct, tamper-evident link") and `s` (SAID of its schema — lets verifier parse/interpret). Exemplified by VVP.
2. **Opaque file artifacts** (photos, audio/video, PDFs, genomic data, spreadsheets, binaries) — "cannot participate in authenticated data graphs using the standard ACDC saidification algorithm, because that algorithm assumes JSON content that can be canonicalized and rewritten." Solution: give the artifact a cryptographic identity via bytewise/externalized SAID algorithms, then issue a **Foreign Artifact ACDC** wrapper.
   - **bSAID (bytewise SAID):** for artifacts whose bytes *can* be rewritten (JPEG Exif, Markdown comment). SAID intrinsic to byte stream via a `SAID:` insertion point; recoverable by scanning raw bytes.
   - **xSAID (externalized SAID):** for artifacts that *cannot* be safely rewritten (compressed archive, encrypted file, PDF with cross-reference table). SAID carried in the filename under a constraint expressed via `XSAID:` delimiter inside the file.
   - Fallback: plain CESR-encoded hash in `content_digest` — "the integrity guarantee is weaker: the hash cannot be discovered by inspecting the artifact itself, only by consulting the wrapper."
   - CESR encoding of `content_digest` is self-describing — "the primitive code identifies the hash algorithm, so no separate algorithm field is required."
3. **Foreign credentials** (W3C VC, ISO mDL) — a designated **bridging party** verifies the foreign credential per its native rules, then issues a **bridge wrapper** ACDC attesting: "I, the bridging party, successfully verified the attached foreign credential on date X according to policy Y." Two caveats: (1) trust depends on the bridging party's reputation/security/policies; (2) "the revocation lifecycles of the original foreign credential and of the bridge wrapper are decoupled unless a specific governance framework explicitly links them." This "transforms the problem of verifying a foreign format into the problem of trusting the attestation of the bridging party."

## 4. Operational lifecycle (curation → citation → verification)

**Curation steps (normative):** (1) Evidence acquisition from authoritative sources; (2) Assembly — build edges block of named links; (3) Iterative assembly & versioning — new versions link to previous via a `prev` edge; "This creates a verifiable chain of the dossier's history, allowing verifiers to traverse back through the lineage of the evidence collection"; (4) Issuance initiation — single-issuer: collector signs; joint: collector hands drafted ACDC to a coordinator; (5) Signing & anchoring — collector/finalizer signs with KERI AID private keys; "This act creates a non-repudiable attestation"; anchored in a KEL; joint anchors may be distributed across KELs or consolidated in a finalization event; (6) Publication — signed ACDC published at a stable resolvable location (HTTP URLs).

**Roles (leader-follower joint issuance):**
- **Collector:** assembles evidence artifacts, defines initial dossier structure.
- **Coordinator:** once collection finished, initiates issuance action, distributes candidate dossier for endorsement.
- **Finalizer:** any entity that, observing threshold met, submits a finalization event to a KEL.
- Also **assembler** (curator; may differ from issuer), **oracle/observer** (temporal pinning), **bridging party**.

**State management — Annotation Edges:** an edge in a new dossier version pointing to an artifact (or edge) in a previous version, carrying the new state/ruling. Example: "Court Case Dossier v2" edge `ruling_101` points to SAID of `exhibit_A` (v1) with `status: "admitted"`.

**Temporal Pinning:** oracle observes dynamic state at Time T → wraps in a signed ACDC ("Observation Attestation") → anchors it in a KEL. Dossier links to the static timestamped attestation. "freezes" the data stream: asserts "had $50,000 at the exact moment this dossier was assembled" rather than "has $50,000 now."

**Citation:** dossiers are "generally not transmitted in their entirety within real-time communication protocols. Instead, they are cited." A citation MUST be a resolvable identifier enabling fetch of the complete, unmodified dossier ACDC. Canonical implementation: **OOBI URL** in the `evd` (evidence) claim of a VVP passport. "An OOBI is a specialized URL that points to a resource serving the ACDC and its associated KERI proofs."

**Verification algorithm (inputs: citation + referenceTime):**
1. Fetch dossier (resolve citation).
2. Validate integrity — recompute SAID, match expected SAID from citation.
3. Determine issuance model — inspect `a` for `fi` (finalization identifier) and edges for joint-issuance threshold operator (`MxN`, `RMxN`, `MxQ`, `RMxQ`) in an edge group's `o`.
4. Validate signatures/anchors: (a) if `fi` present/non-null, find finalization event in that AID's KEL, verify threshold-satisfying endorsements; (b) if `fi` absent but threshold operator present, evaluate each slot — a slot is **Endorsed** only when it references a signed Endorsement ACDC with `disp` `"endorse"` and appropriate `act`, issued by the expected endorser and anchored in that endorser's KEL; Endorsed weights must sum to ≥ unity; qualified operators additionally require each endorsement carry a qualification proof (`e.qp`) validating against the operator's `qs` schema; (c) single-issuer: retrieve issuer KEL, verify signature against keys authoritative *at the referenceTime*.
5. Recursive graph traversal — for each edge, fetch referenced artifact and validate recursively.
6. Check revocation status — for the dossier and *every node* in the graph, consult KELs/status registries for revocation effective at the referenceTime.
7. Apply semantic rules — application-specific policy after cryptographic validation completes.

**Layered verification doctrine:** verification is a two-layer process. Layer 1 = cryptographic validation, universal, defined by this spec ("confirming signatures, SAIDs, and KEL consistency"). Layer 2 = semantic validation, "necessarily application-specific and requires context-dependent business logic." A generic verifier "can verify that an edge labeled 'lunarPropertyDeed' is cryptographically linked, but it cannot know what that means or how to process it." This separation is what makes the dossier a "universal building block for evidence aggregation."

## 5. Joint issuance (the doctrinal heart of multi-party dossiers)

- **Framing:** joint issuance is "not a single, uniform approach... but a family or style of approval strategies" mapping onto "coordinated control in multi-agent systems" studied in robotics/AI/military science. Three cooperative-control variants cited: **leader-follower**, **behavior-based control**, **virtual structures**.
- **Key contrast vs. group multisig:** "Unlike group multisig, which requires synchronous agreement on key event log (KEL) sequence numbers, joint issuance relies on logic within the ACDC layer. This lets members contribute signatures or seals to a dossier at different times and via different channels without immediate impact on a shared KEL." Validity is decoupled from key management → more flexible issuance/verification.
- **Threshold mechanics:** a weighted threshold operator in the `o` field of an edge group; member edges are **slots**; each slot carries a weight in reserved `w`; group satisfied when weights of Endorsed slots sum to **≥ unity (1)**. "This is the same fractionally weighted threshold KERI uses for key-event signing thresholds (`kt`): the threshold itself is the fixed constant 1, so there is no separate count field." For m-of-n equal endorsers, each of n slots gets weight `1/m`. Unequal weights express weighted governance (senior endorser `2/m`); grouped weights express nested AND/OR-of-threshold rules (like KERI's nested `kt` lists).

**Slot dispositions (only a signature authenticates a decision):**
- **Pending:** references an unsigned meta ACDC naming the candidate but carrying no signature (or slot is null). Contributes nothing; records only that an endorsement is anticipated.
- **Endorsed:** references a signed Endorsement ACDC issued by candidate with `disp` `"endorse"` and a `said` attribute equal to the dossier's SAID. Weight added to sum.
- **Declined:** same signed Endorsement ACDC but `disp` `"decline"` — a declination. Weight not added, but "records attributable dissent — distinguishing a candidate who was asked and refused from one who has not yet acted."
- Doctrine: "a pending slot and an absent slot are equivalent in trust terms: neither attributes any act to the candidate. An active 'no' MUST therefore be expressed as a signed declination."

**Four threshold operators** (all use single Endorsement schema SAID `EAfn0gRMUnp6d1hyE5qJCN86kBFBp80JwMdm0BqiC1B0`; distinguished by `disp` (endorse/decline), `act` (issue/revoke), and optional qualification-proof edge `e.qp`):
- **`MxN`** ("M of N") — issuance operator, exactly N slots (one per candidate); each counted endorsement carries `act` `"issue"`, `disp` `"endorse"`, omits `e.qp`. Candidates enumerated structurally as slots (each names its expected endorser via the issuer `i` of the referenced ACDC) — "embodies an m of n pattern without any separate enumeration of potential signers." Example: judicial decision by m of n named justices.
- **`RMxN`** ("Revocation M of N") — same mechanics, `act` `"revoke"`. Revocation slot set MAY be identical/overlapping/disjoint from issuance slots; weights MAY differ — "the authority to revoke can be configured independently of the authority to issue."
- **`MxQ`** ("M of Qualified") — issuance for an *open-ended* set of qualified endorsers; slot count NOT fixed in advance (slots added as qualified endorsers act). Declares a *uniform member weight* in its own `w`; satisfied when at least `1/w` qualified endorsers endorse. Each counted endorsement carries `act` `"issue"`, `disp` `"endorse"`, and a qualification-proof edge `e.qp`. Edge group MUST carry a `qs` field naming the schema each qualification proof must satisfy. Models "any licensed physician in good standing."
- **`RMxQ`** ("Revocation M of Qualified") — same, `act` `"revoke"` + `e.qp`; qualified revoker set/weights configurable independently.

**Finalization (`fi` field):** optional aid to verifiers that don't do recursive traversal, signaled in `a`, not by an edge operator. When `fi` present/non-null → holds the AID (typically a group AID) whose KEL is expected to carry the finalization event; verifier SHOULD use it as definitive proof. When absent/null → "no finalization event is promised. A verifier MUST instead gather the endorsements from the participants' individual KELs and confirm directly that the threshold is met."

**Revocation:** defined independently of issuance. Default: "if no revocation operator is present, the threshold required to revoke a dossier is identical to the threshold required to issue it." Asymmetric thresholds allowed (e.g., majority to issue, single admin AID at weight-1 to revoke).

## 6. Derivatives — Citation vs. Token (separating two conflated questions)

Two derivative forms:
- **Citation:** resolvable identifier (canonically OOBI URL) → fetch full dossier + run algorithm.
- **Token:** short-lived signed object carrying enough context for an immediate decision, embedding the dossier SAID as evidence pointer (`evd`). Sample fields: `iss`, `iat`, `exp`, `aud`, `nonce`, `evd`. "The token asserts that, between `iat` and `exp`, its bearer is acting under the authority of the dossier whose SAID is given in `evd`." A verifier with a cached validated dossier MAY accept without re-traversing; one requiring fresh assurance dereferences `evd`, runs full algorithm, caches result.

The split separates two questions "conflated in conventional bearer credentials":
- *What was attested, and by whom?* — lives in the dossier, curated once, amortized.
- *Who is presenting it now, in what session, under what immediate constraints?* — lives in the derivative, bound to the transaction via ephemeral fields (`iat`, `exp`, `aud`, `nonce`).

Derivatives inherit the dossier's revocation lifecycle (evaluated at verification time).

## 7. Security & threat-model positions

- **Detection over prevention / duplicity-evident (primer §2.6):** "Duplicity is KERI's term for the double-spend problem in identity" — a controller signing two different events with the same sequence number. Witnesses provide availability + duplicity detection; **watchers** poll witnesses and, if two witnesses report different head hashes for the same sequence, "the watcher has detected duplicity... can broadcast the conflicting events as cryptographic proof of fraud... this proof is fatal to the reputation of the identifier." Doctrine quote: "Detection (rather than prevention) allows KERI to operate with low latency while ensuring that any dishonesty is provable."
- **Adversarial / malicious-controller trust model:** "The trust model is adversarial: witnesses are assumed to be potentially malicious" (primer §2.6). Witnesses ≠ CAs: "A witness makes no such assertion. A witness simply stores and serves events" — a CA is trusted to attest to identity; a witness is not.
- **Decentralized / plural root of trust (dossier §"Verifier Trust"):** "The dossier model operates on a decentralized root of trust. A verifier does not rely on a single authority but makes explicit trust decisions about a plurality of evidence issuers." In joint issuance trust is distributed across member AIDs. Verifiers SHOULD consult multiple witnesses "to ensure they have a consistent and complete view of an issuer's KEL, thereby protecting against duplicity and compromise."
- **Distributed root of trust in VVP (Compositional Dossier):** "Trust is derived from the leaf nodes (the authorities), not merely from the dossier issuer." The assembler does not generate the evidence — bundles credentials from distinct domain-specific roots of trust (LEI issuer for legal identity, carrier/regulator for number authority, trademark steward for brand).
- **Integrity via SAID:** "A SAID is a cryptographic hash of an object's canonical content. Any modification to the data results in a different SAID, making tampering immediately evident."
- **Non-repudiation via KEL anchoring:** signatures "cryptographically anchored in a key event log (KEL), which serves as a permanent, publicly auditable, and tamper-evident log."
- **Pre-rotation firewall (primer §2.3):** "Pre-rotation establishes a firewall between day-to-day use and occasional governance." Current key K1 on a production server; next key K2 generated, hashed, stored air-gapped. "If the server is breached, the attacker steals K1 but cannot rotate to assume control of the identity." Security "comes from the asymmetry in knowledge: the controller knows or has access to K2, while the world only sees its hash." In standard PKI "there is no defense against this; a signature from the compromised key looks exactly like a signature from the legitimate owner."
- **Historical / point-in-time verifiability (dossier §"Long-term Auditability"):** because KELs give a complete sequenced history, "a verifier can perform validation for any arbitrary point in the past... An auditor can determine if a dossier and its entire evidence graph were valid at the time of a transaction, based on the key states and revocation information known at that moment." (Observer-relative / referenceTime-dependent validity.)
- **Anchored (not paired) signatures & retrograde attacks (primer §3.3):** ACDCs use anchored signatures — a provable KEL association independent of container context. "The credential was issued *during* the active window of a specific key... This eliminates timestamp ambiguity." Cites NIST SP 800-102: a signed message "provides no assurance that the private key was used to sign the message at that time." Without native anchoring, "simple paired signatures are vulnerable to 'retrograde attacks,' where a compromised key is used to forge historical events."
- **Replay mitigation:** the dossier is stable/long-lived, so "the primary risk of replay attacks exists at the level of the protocol that cites it."

## 8. Privacy doctrine

- **Graduated disclosure (dossier §"Graduated Disclosure"):** ACDC SAID is computed recursively — "the hash of a parent object is derived from its scalar values and the SAIDs of its child objects." So "any child object within an ACDC can be replaced by its SAID without altering the SAID of the parent object and without invalidating the digital signature." Enables redacted-but-verifiable versions. "In joint issuance, redaction does not affect the validity of member seals... as those seals point to the immutable SAID of the root dossier."
- **Selective disclosure (primer §3.5):** payload structured into sections, each with a random salt + digest; holder reveals only chosen sections via Merkle-proof style strategy.
- **Right to be forgotten (primer §3.5):** "the KEL stores only the anchors (hashes) of the credentials"; payload is off-chain. Deleting the payload leaves an irreversible hash; identity history intact, personal data removed. Contrasted with blockchain: "'forgetting' an identifier requires a hard fork of the entire chain."
- **Correlation vectors (dossier):** (1) Dossier SAID — persistent unique identifier; (2) Citation signer AID — links all messages signed by same identifier; (3) Explicit brand information — intentional correlator.
- **Mitigations:** rotate the citation-signing AID frequently (independent of the long-lived issuer AID); maintain a pool of AIDs for "herd privacy"; use a trusted blinding service that verifies an original dossier and issues a short-lived derivative attesting validity "without revealing its SAID to the end verifier." Also contractually protected disclosure — serve redacted version to anonymous requests, require signed request (tied to T&Cs) for expanded version, creating an audit trail of who accessed sensitive data.

## 9. Anti-patterns / outsider-tells the material explicitly corrects (from primer)

These are the doctrinal reframings against PKI/blockchain/VC priors:

- **PKI/X.509 root-of-trust flaw:** "The fundamental flaw... is the separation of the identifier from the cryptographic keys that control it." In X.509 an identifier "is a lease entry in a database"; binding is "merely an assertion — a digital certificate — signed by a third party," creating "a root of trust that is external to the identity itself." KERI reframing: "The identifier is the root of trust" — binding must be "mathematical (and therefore, objectively provable and permanent), not administrative."
- **CA fragility:** "If a CA is compromised, coerced, or negligent, it can issue valid certificates that assert bindings that are not true" (DigiNotar, Symantec distrust, TrustCor). "the security of the leaf (the user) is entirely dependent on the security of the root (the administrator)."
- **Jurisdictional non-universality of CA trust:** "a CA-based ecosystem has different trust profiles in different jurisdictions" (SHAKEN not accepted in Europe/Asia). The CA/Browser Forum is "a new centralization."
- **Revocation-list critique (CRL/OCSP):** "X.509 standard also lacks a native, low-latency, enforceable mechanism for revocation." CRLs "heavy, bandwidth-intensive... scale poorly." OCSP "requires the client to query a central responder for every validation, creating a privacy leak (the CA knows every site you visit)." Fail-open: "browsers often 'fail open', meaning they accept the unverifiable certificate as valid." KERI requirement: "Revocation is immediate and safe... without privacy leaks or 'fail open' risks."
- **CT is detection not prevention, and re-centralizes:** "CT is a detection mechanism, not a prevention mechanism; fraudulent certificates may be usable for a time." And "the implementation of CT has introduced a new form of centralization."
- **The persistence / identity-continuity problem:** certificates expire/rotate to a "mathematically unrelated" new cert; "The only link between them is the administrative procedure of the CA." ACME continuity "exists only in the eyes of the CA." Requirement: "Identity survives key rotation... without having to trust a party who claims it's safe to ignore a gap."
- **KERI is NOT a blockchain (rejection of global consensus):** "Traditional blockchains rely on a global consensus model, where every node must agree on the total ordering of all transactions." "KERI rejects the need for global consensus regarding identity. Instead, it uses microledgers called key event logs (KELs)." "The ordering of events matters only relative to that specific identifier." "KERI naturally scales horizontally because there is no central choke point." "Hacking incentives decay because any breach is likely to be limited in scope to a single identifier."
- **AID is NOT a domain name or UUID:** "Unlike a domain name, which is rent-seeking text, or a UUID, which is arbitrary entropy, an AID is a self-certifying identifier (SCID)."
- **SAID vs. UUID:** "The problem with a UUID is that it has no relationship to the data." A SAID is content-addressable — "An ACDC is not a mutable document; it is a crystallized fact."
- **Multisig — KERI's innovation is EXPOSING, not inventing:** in X.509/PKI multisig governance "is not knowable or verifiable by the public... This makes it impossible to distinguish between sloppy and robust management of secrets... Hackers thrive on opacity." KERI "requires a definition of the identifier's fractionally weighted thresholds directly in the public KEL." "KERI's real innovation in multisig is less about inventing and more about exposing: multisig is optional and infinitely variable, but defining and following policy about it is required."
- **JSON canonicalization / JSON-LD critique (CESR rationale):** `{"a":1,"b":2}` vs `{"b":2,"a":1}` "are semantically identical but have different cryptographic hashes." JCS "normalization logic is brittle." "In complex environments like JSON-LD, this fragility has led to 'term redefinition' vulnerabilities, where the meaning of a signed credential can be altered without invalidating the signature." (Direct swipe at W3C VC data integrity.)
- **W3C VC / JWT / X.509 = paired signatures** (a limitation) vs. ACDC anchored signatures. Foreign VCs belong as *derivative artifacts* wrapped/bridged, not as native roots of trust.

## 10. Precise terminology & definitions

From primer / refs:
- **AID (Autonomic Identifier):** core KERI primitive, a self-certifying identifier (SCID) derived cryptographically from initial key(s). Two derivation modes:
  - *Basic derivation:* identifier = digest of a single public key; brittle, non-rotatable, "suitable only for ephemeral, short-lived use cases."
  - *Transferable derivation:* identifier derived from the entire *inception event* (initial keys + pre-rotation commitment to next keys); "The identifier string remains constant even as the keys change." KERI's primary innovation for persistent identity.
- **KEL (Key Event Log):** "the authoritative source of truth for an AID," an append-only signed chain of events; a *microledger*. Verified by replaying history from inception. Three event types: **inception (`icp`)** (birth), **rotation (`rot`)** (key/config change), **interaction (`ixn`)** (anchoring data/seals without changing keys). (KERL = the receipted KEL, implied.)
- **Establishment events:** icp + rot (define control); carry `k` (public keys) and `kt` (signing threshold).
- **Pre-rotation:** committing *now* (via hash of K2) to the next key; revealing K2 only at rotation time and re-committing to K3.
- **`kt` fractionally weighted threshold:** list(s) of fractional weights; a clause is satisfied when the sum of signing weights ≥ 1.0; lists-of-lists = AND/OR (clauses joined by OR). Example `[["1/2","1/2","1/2"], ["1/3","1/3","1/3","1/3"]]`.
- **Signature indexing (CESR):** each signature attachment carries a code specifying which key in `k` produced it, mapping signatures to weights.
- **Witness:** "a server designated by the controller to store and serve the KEL"; signs receipts; provides availability + duplicity detection. Threshold of witnesses (e.g. 2 of 3) makes an event stable. (a.k.a. backer.)
- **Watcher:** entity run by verifiers/auditors that polls witnesses to detect duplicity (conflicting head hashes).
- **SAID (Self-Addressing Identifier):** content-addressable cryptographic hash of a data structure, embedded in the `d` field via the dummy-character derivation (44 `#` chars for Base64 256-bit, digest computed then overwritten).
- **ACDC (Authentic Chained Data Container):** protocol for attestations/VCs prioritizing security, compactness, provenance; "C" = chained (any number of chains, arbitrary weight/semantics → verifiable DAG). Fixes the "copy-paste vulnerability."
- **Anchored signature:** provable KEL association (issuer digest sealed in a KEL event) vs. paired signature.
- **TEL (Transaction Event Log):** specialized log for credential status/revocation; "ACDCs anchored in TELs allow for real-time status checks without privacy leaks."
- **IPEX (Issuance and Presentation Exchange):** protocol over KERI for handing over ACDCs; `exn` messages — **`apply`** (holder requests), **`offer`** (issuer offers), **`agree`** (both agree), **`grant`** (issuer sends). (Primer §3.1 gives offer/request/grant three-step; issuance-ref §3.2 gives the four `exn` types.) Mutual anchoring: issuer logs "I issued", holder logs "I accepted" — "prevents spam (you can't force a credential into someone's wallet) and provides non-repudiation of receipt."
- **Endorsement (issuance-ref §4):** "a signature provided by an AID that is not the controller of the KEL" — external, additive, non-mutating. "You can add 100 endorsements to a single KERI event... These endorsements do not change the digest of the event." Witness receipts and watcher confirmations are forms of endorsement. This is the technical precursor to join-issuance: members endorse a *fixed artifact's SAID* rather than signing a *proposal in escrow*.
- **CESR (Composable Event Streaming Representation):** the serialization "language"; self-framing via framing-code prefix; concatenation composability (Base64 ↔ raw binary without breaking signatures); enables pipelining (route by first 1–4 bytes) and crypto agility (assign new meaning to an unused code-table prefix — old parsers still Read-Code→Lookup-Length→Read-Bytes). Sample codes: `A`=Ed25519 seed (44), `E`=Blake3-256 digest (44), `0B`=Ed25519 signature (88), `-A##`=pipeline group counter.
- **DKMI (Decentralized Key Management Infrastructure):** what the stack enables.
- **OOBI (Out-of-Band Invitation):** resolvable URL pointing to a resource serving an ACDC + KERI proofs; canonical dossier citation.

**ACDC edge operators (operators-ref):**
- Reserved edge field labels: `d` (SAID of edge block), `u` (UUID), `n` (SAID of target far-node ACDC), `s` (SAID of schema target must validate against), `o` (operator), `w` (weight).
- **Unary (edge-level):** `I2I` Issuer-To-Issuee (issuer of current MUST be issuee of target; *default*; standard for delegation), `NI2I` Not-Issuer-To-Issuee (may or may not), `DI2I` Delegated-Issuer-To-Issuee (issuer must be issuee or a delegated rep), `NOT` (inverts validation truthiness). "If multiple unary operators... conflict, the latest in the list takes precedence."
- **M-ary (edge-group level):** `AND` (*default*; all valid), `OR` (≥1 valid), `NAND` (not all valid), `NOR` (all invalid), `AVG` (arithmetic average of a member property), `WAVG` (weighted average using `w`).
- Doctrine: "ACDCs act as fragments of a distributed property graph. Operators allow the graph to perform 'reasoning'" — delegation chains (`I2I`), thresholds (`OR`/weighted averages), negation (`NOT` for revocation/blacklisting).

## 11. Worked examples / use-case architectural patterns (dossier §"Use Cases")

- **VVP — Compositional Dossier:** assemble a "permission slip" from independent authorities. Distributed root of trust; verifier recursively checks issuers of edge credentials; trust from leaf authorities. Ideal for access control, licensing, regulatory compliance.
- **Law enforcement/adjudication — Procedural Dossier:** tamper-evident chain of custody + procedural evolution. Phase 1 (Investigation) = immutable "bag" of artifacts, focus on completeness/provenance; Phase 2 (Adjudication) = state changes (Marked/Offered/Admitted/Stricken) via Annotation Edges. To "strike," Clerk issues a new version with an edge targeting the original SAID + `status:"stricken"` — preserves original (for appeals) while excluding from "effective" facts.
- **Investigative journalism — Redacted Dossier:** prove provenance without revealing source. Private graph (unredacted "Source Asset") vs. public graph (Redacted Asset). Public dossier links to Redacted Asset; internally linked to Source Asset via a "blinded" edge (hash). Uses "precursor" (Cross-File Association) relationships. Lets journalist prove later (declassification) that redacted text derived from the specific original recording.
- **Mortgage qualification — Snapshot Dossier:** verify dynamic/volatile data (bank balance, credit score) via Temporal Pinning + Oracle/Observer role. "Observation Attestation" says "I observed Account X having Balance Y at Block Height Z"; dossier links the static attestation. Verify "Funds Available" at exact application moment.
- **Clinical trials — Predicate Dossier:** prove eligibility without disclosing sensitive data (HIPAA/GDPR). Zero-Knowledge Predicates via a **Predicate Edge** pointing to a ZKP/derived claim. Dossier asserts `inclusion_criteria_met: true`; evidence is a ZKP proving "Subject Age > 18 AND HIV_Status == Positive" without revealing birthdate/markers. Verifier validates the proof, not the document.
- **Petition — Open-Endorsement Dossier:** collect a threshold of endorsements from a large/unenumerable signer set. Asynchronous threshold satisfaction; any AID meeting schema criteria can contribute. Uses `MxQ`; qualification proved via `qs` schema; participants issue a qualified Endorsement ACDC anchored in their own KELs. Coordinator may set `fi` and finalize when threshold reached.

## 12. Proximate metadata fields (dossier `a` section — all optional unless schema requires)

`assembly_dt` (ISO 8601 assembly time; distinct from envelope issuance date), `assembler` (AID/name of curator, useful when ≠ issuer), `purpose` (human-readable, not machine-interpreted), `ref` (external reference/case/docket/txn ID, untyped), `gov` (SAID/URI of governance framework/rulebook), `evt_dt` (ISO 8601 time of the documented event — crash/crime/filing — distinct from assembly_dt), `evt_loc` (where the event occurred; no single mandated format; SHOULD follow domain standards e.g. ISO 6709), `jur` (legal/regulatory jurisdiction as ISO 3166-1 alpha-2, optionally +3166-2; MAY be an array), `cls` (type/category of matter; domain-dependent controlled vocabulary), `phase` (procedural maturity: preliminary/factual/final, or investigation/adjudication/closed; new version SHOULD be issued on phase transition), `gov_rules` (SAID/URI of the specific ruleset governing evidence collection — more specific than `gov`; both may coexist: `gov` = who oversees, `gov_rules` = what procedural constraints applied). Also `fi` (finalization identifier — AID whose KEL carries the finalization event).

## 13. Escrow model & why joint issuance is an evolution (issuance-ref)

- **Group AID:** a multisig entity whose control keys are member AIDs; the Group KEL represents the collective; every Group KEL event must be signed per the group's `kt`.
- **Wait-for-Signature (WFS) Escrow:** partial-sig events held in a "Partial Signature Escrow," "effectively 'invisible' to the authoritative state of the KEL," until weights reach threshold, then "promoted" to the KEL.
- **Core limitation — Synchronous Serialization Requirement:** "Because KERI events are chained by digests, the group must coordinate on the *content* of the event before signing." Any metadata/timestamp difference makes signatures incompatible. "This 'tight' coordination creates high friction in distributed environments." → motivates the loose, ACDC-layer, endorsement-based joint issuance where the artifact is fixed and members endorse its SAID asynchronously.
- **Issuance = anchoring/sealing** (issuance-ref §3.1): "an 'Issuance' is not just a signature on a document. It is the act of Anchoring or Sealing the credential's digest (SAID) into the Issuer's KEL." ACDC is valid only if a verifier can find that seal in a finalized establishment/interaction event.

## 14. Engineering-mindset doctrine (primer §5)

- Resilience via pre-rotation + weighted multisig makes identity "antifragile. It gets stronger with more keys, not more complex."
- Verification cost is O(n) in history but O(Δn) in practice via incremental verification / cached state.
- Mental-model shift: "We stop thinking about certificates (static assertions) and start thinking about event streams (dynamic histories). We stop building admin panels for identity and start building agents that manage keys. Trust is not granted by a corporation or a government, but established by the mathematical consistency of the identifier itself."
- Quantum posture: rotation authority always hidden behind a hash until used-and-discarded; hybrid governance (require both ECC and post-quantum signatures in threshold) → "The ecosystem has a straightforward, calm response to any quantum apocalypse."
