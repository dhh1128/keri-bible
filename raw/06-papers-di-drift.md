# Doctrine-mining notes: Decentralization purity vs. SD-JWT / W3C-VC / DID drift

Source corpus: Daniel Hardman's "Codecraft Papers" (`/home/daniel/code/papers/*.md`). Primary sources read in full: `sdjwt-acdc.md`, `acdc-vc-diff.md`, `acdc-and-mtc.md`, `authenticity-vs-veracity.md`, `oia.md`, `who-sign.md`, `sda.md`, `bes.md`. Supporting sources read for threat-model doctrine: `x509-prob.md`, `was.md`, `sign-author.md`, `keri-primer.md`. All citations below are `file.md §section` with exact <=25-word quotes where load-bearing.

---

## 1. What KERI / ACDC / CESR fundamentally IS and IS NOT (worldview, design intent, root of trust)

### 1.1 The identifier itself is the root of trust (self-certifying), not an administrator
- The defining break from PKI: shift the root of trust from administrator to cryptographic controller. `keri-primer.md §1.3`: *"The identifier is the root of trust: The binding between the ID and the key must be mathematical ... not administrative"*.
- The X.509 "fundamental flaw" is **separation of the identifier from the keys that control it**; the binding is "merely an assertion—a digital certificate—signed by a third party. This creates a root of trust that is external to the identity itself." (`keri-primer.md §1`).
- AID = *autonomic identifier* = a *self-certifying identifier* (SCID). "The identifier derives cryptographically from the initial public key (or set of keys) that controls it." (`keri-primer.md §2.1`). Contrast: a domain name is "rent-seeking text," a UUID is "arbitrary entropy."
- Transferable derivation is KERI's core innovation: the identifier derives from the entire **inception event** (initial keys + pre-rotation commitment), so "The identifier string remains constant even as the keys change ... Identity survives key rotation" (`keri-primer.md §2.1`).

### 1.2 KERI is NOT a blockchain; it rejects global consensus / global ordering
- "KERI rejects the need for global consensus regarding identity. Instead, it uses microledgers called *key event logs* (KELs)." Each identifier has its own independent KEL (`keri-primer.md §2`).
- Ordering matters only *relative to that identifier*: "Event 5 for Identifier A must come after Event 4 for Identifier A, but it has no required ordering relative to Event 5 for Identifier B." (`keri-primer.md §2`). No central choke point → horizontal scale, cross-jurisdiction ease, decayed hacking incentives (breach scoped to one identifier).
- KELs/TELs are "tiny, standalone files specific to a single identifier ... none of the scale and performance bottlenecks, none of the centralized governance challenges" of a blockchain (`sdjwt-acdc.md §2.3`). Resemble "microledgers ... discussed in Hyperledger Indy circles" (`was.md §Solution`).
- The anchoring requirement is *weaker* than blockchain by design: "We don't need to know the relative order of two signing events — only how any one event relates to its key state. That means no total ordering, and no cumbersome consensus algorithm." (`was.md §Solution`).

### 1.3 ACDC IS a lossless "methodology," not merely a credential format
- "ACDCs are not just a format — they're a *methodology* for creating verifiable evidence." (`x509-prob.md §Much better alternatives exist`).
- ACDC handles the "What" (data); KERI handles the "Who" (identity); CESR is "the language they speak" (`keri-primer.md §3, §4`).
- ACDC = *Authentic Chained Data Container*; the "C" (chained) = link credentials into a graph tracing "derived authority to issue" (`keri-primer.md §3.4`). An ACDC is "not a mutable document; it is a crystallized fact" (`keri-primer.md §3.2`).
- LOSSLESS-vs-LOSSY is the central metaphor: ACDC = RAW/FLAC (archival source of truth); W3C-VC / SD-JWT / ISO mDL = JPEG/MP3 (lossy distribution). "once you've chosen a lossy format as your primary evidence, you cannot reconstruct what you've lost." (`acdc-vc-diff.md §Lossless vs. Lossy`). Ideal: keep lossless ACDC authoritative, *generate* W3C VCs from it when needed (`acdc-vc-diff.md §The Right Format for the Job`).

### 1.4 Authenticity vs. veracity — the crisp doctrinal distinction
- Authenticity = "truthfulness of an imputed origin"; veracity = "truthfulness of claimed facts in content." They "must be analyzed primarily as *orthogonal*." (`authenticity-vs-veracity.md §Formal definitions, §Independence`).
- KEY doctrine: authenticity is mechanizable, veracity is not. "Judgments about authenticity can — *if managed very carefully* — be reduced to an objective mathematical computation, whereas judgments about veracity inherently require subjective assessments of reputation." (`authenticity-vs-veracity.md §Independence`).
- Credited to Sam Smith / KERI community for "emphasizing the distinction" (in KERI, ACDC, did:webs specs). Example: a notary "witnesses the authenticity of your affidavit, but makes no commitment as to its veracity."

---

## 2. Security & threat-model positions

### 2.1 Detection-not-prevention; duplicity-evident-not-resistant
- "Detection (rather than prevention) allows KERI to operate with low latency while ensuring that any dishonesty is provable." (`keri-primer.md §2.6`).
- Duplicity = "KERI's term for the double-spend problem in identity: a controller signing two different events with the same sequence number" (`keri-primer.md §2.6`).
- Contrast with PKI's own detection tool: "CT is a detection mechanism, not a prevention mechanism; fraudulent certificates may be usable for a time." (`keri-primer.md §1`) — and CT ironically re-centralized trust in "a few tech giants."
- Duplicity detection is *fatal*: watcher broadcasts conflicting events as "cryptographic proof of fraud ... this proof is fatal to the reputation of the identifier." (`keri-primer.md §2.6`).

### 2.2 Zero-trust / malicious-controller / adversarial-witness stance
- "The trust model is adversarial: witnesses are assumed to be potentially malicious." (`keri-primer.md §2.6`).
- Witnesses ≠ CAs: "A CA is trusted to attest to identity ... A witness makes no such assertion. A witness simply stores and serves events." (`keri-primer.md §2.6`). "Malicious witnesses can't fake the data they notarize." (`sdjwt-acdc.md §2.3`).
- Witnesses guarantee *detection* of malicious signers "who attempt to fork their key state or signing history." (`sdjwt-acdc.md §2.3`). "Arbitrary observers can poll or subscribe to witnesses to compile their own records" (observer-dependent validity).

### 2.3 Pre-rotation as a firewall (survivability, not invulnerability)
- Pre-rotation = commit *now* (as a hash) to the next key, managed separately/offline. "Pre-rotation establishes a firewall between day-to-day use and occasional governance." (`keri-primer.md §2.3`).
- The asymmetry: attacker who steals K1 "cannot produce even the public key portion of K2." So "If the server is breached, the attacker steals K1 but cannot rotate to assume control ... The legitimate owner can retrieve K2, rotate ... and regain control." (`keri-primer.md §2.3`).
- Survivability framing: "even if a hacker can abuse a current key, they can't rotate to new keys and take permanent control without accomplishing a second hack somewhere else. The identity owner thus has a failsafe" (`x509-prob.md §Prerotation is missing`).
- Recovery is self-service by construction: "The recovery logic is baked into the math of the identifier itself." (`keri-primer.md §2.4`, break-glass recovery). System is "antifragile ... gets stronger with more keys, not more complex." (`keri-primer.md §5`).

### 2.4 Retrograde attack (the deepest threat-model contribution) — anchored signatures
- Core claim: bare digital signatures are "much weaker evidence than casual thinkers might imagine" because they are "difficult to sequence relative to a compromise or revocation event." (`was.md` intro).
- Retrograde attack anatomy: attacker who *ever* gets key K can forge evidence "that looks like it originated in the past, *forever*" — and remains possible "even if she rotates or revokes K before Malfoy steals it." (`was.md §Retrograde attack`). Backdating window has "no end point."
- Three flawed mitigations catalogued: (1) contextual clues (unreliable), (2) retroactive revocation ("dangerous and foolish"; lets Alice cheat/repudiate her own acts), (3) "verify against current key state only" = **pyrrhic victory** — "After-the-fact audits are impossible, because anything in the past can be faked with compromised keys." (`was.md §Mitigation 3`).
- Solution = *anchored signatures*: "Keep tamper-evident records that can prove how a given signing event relates in time to changes in the associated key state." (`was.md §Solution`). Implemented via KELs + TELs; "KERI anchors (records the hashes of) signed TEL events in the KEL to make sequence unambiguous."
- Payoff = time-independent verification: "An analysis of an anchored signature will produce the same result no matter when it happens, which makes historical audits ... possible." Evidence stays valid across "any number of key rotations, making it effectively permanent." (`was.md §Conclusion`).
- Anchored ≠ paired signatures. Paired = signature bundled in the container because "the format says so" (VC `proof`, JWT bundle, X.509 `signature` over `tbsCertificate`). Anchored = provable association via the KEL, "independent of any container context." (`keri-primer.md §3.3`). Verify by extracting AID → retrieving KEL from witness → traversing to the sequence number → confirming the ACDC digest is anchored there.
- NIST SP 800-102 cited: a signed message "provides no assurance that the private key was used to sign the message at that time." KERI's native anchoring removes the need for external Time-Stamp Protocols (`keri-primer.md §3.3`).

### 2.5 Local / observer-dependent validity; offline verification
- Verification is offline-capable and does not phone home. In MTC comparison: KERI/ACDC "verification can be offline"; freshness is "about continuity and completeness of key state" rather than recency (`acdc-and-mtc.md §2 table, §5.1`).
- Contrast: OCSP / CRL / trust registries are "phone home" models; "A registry consulted at verification time is a phone-home in disguise." (`sda.md §7`).
- Open-loop verification (see §5.3 below) is the architectural statement of observer-independence: "a stranger can check authority without consulting its issuer."

### 2.6 Guarantees stated relative to explicit assumptions
- Anchoring closes the *future* attack window but not the pre-detection window: "Alice is still vulnerable to mischief until she notices a compromise. However, during this time Malfoy is forced to create evidence with new dates" (`was.md §Solution`).
- bes.md §3.6 Threat Model is a model of explicit-assumption discipline: bytewise/externalized SAIDs "do not provide confidentiality, access control, or resistance to format-aware semantic transformations." Assumes author inserts insertion point at creation time and handling preserves bytes; "any byte-changing transformation is treated as producing a new identity."
- sda.md §8 is explicit about what the delegation model does NOT do: it makes an act's *category* checkable but "cannot tell whether the agent attempting it is faithful. Sincerity stays gate-able and auditable, never provable. That is not a defect ... it is a property of the world."

---

## 3. Invariants and "never do X" rules

- **Never confuse proved with guessed.** The "single most dangerous mistake in the whole design" (`oia.md` abstract). "The gap between proved and guessed is the gap a **man-in-the-middle** attacker lives in." (`oia.md §Proved versus guessed`).
- **Never automate the final verification of a proof.** "Automate the introduction. Automate the proof where you can. But never automate the verification of the proof." (`oia.md §Connections`). The human must take "the last step — the moment a human weighs that evidence and decides it is good enough to trust *this* party, for *this* purpose, now."
- **Never parse a stranger's alias for meaning.** "An alias must never be parsed for meaning by anyone but its creator." Doing so "has trusted a private note it had no business trusting. The name is a memory aid, not evidence." (`oia.md §An alias is a private nickname`).
- **Never mistake an alias for an identifier.** "treat an alias as an identifier and you get collisions; cache it ... and you get staleness; parse a stranger's alias for meaning and you get an attack surface." (`oia.md`).
- **Never assume a signature means authorship.** "People often treat a signature as if it were a claim of authorship. That is sometimes true. But it is not what signatures *are* in general." (`sign-author.md`). A signature "is evidence that a signing mechanism ran"; meaning comes from role/ceremony/policy/protocol.
- **Never present a single clean answer to "who is signing?"** "Asking the question is insightful. Expecting a single, clean answer is usually a mistake." (`who-sign.md`). Control, authority, responsibility, and attribution "overlap but do not coincide."
- **Never collapse the key vs. affordance ("errand vs. signet ring") distinction.** Don't hand over the ring for an errand: "Possession of an API key ... makes the holder indistinguishable from the account it belongs to, free to do anything that account can." (`sda.md §1`).
- **Never verify against a registry/callback.** "verification must succeed from the credential and key-state alone, and any registry or log is an issuance-time and audit-time convenience, never a verification-time dependency." (`sda.md §7`).
- **SAID invariant:** any change to SAD or SAID breaks correspondence; "Any change to the byte stream after saidification necessarily produces a different SAID and is therefore treated as a new version" (`bes.md §3.6`). A bytewise SAD "MUST contain exactly one primary insertion point"; leftmost match is primary, others are echoes (`bes.md §3.2`).
- **Never give one key sole authority over org reputation.** Multi-attestation for high stakes is millennia-old wisdom (Code of Hammurabi law 7, Deuteronomy 19:15, double-entry accounting): "why are we imagining ... it's safe to use the single-signature mechanism of X509 certs as the only gate on unlocking the entire reputation of modern corporations?" (`x509-prob.md §One key isn't realistic`).
- **Basic (non-transferable) AIDs only for ephemeral use;** you cannot rotate them without abandoning the identifier (`keri-primer.md §2.1`).

---

## 4. ANTI-PATTERNS / outsider-tells / misconceptions explicitly corrected (the gold)

### 4.1 PKI / X.509 / CA / OCSP / CRL priors
- **"To a PKI expert, every verification problem looks like a place for certs."** "screws are drastically better than nails, for certain carpentry tasks. Likewise, ACDCs are drastically better than certs, as primary proof of organizational identity." (`x509-prob.md §intro`).
- **Certs prove privilege, not identity — the lifespan mismatch.** "renewing an *identity* is a non-sequitur." Org identity is "measured in decades"; certs' "sweet spot and lifespans measured in weeks or months." CA/Browser Forum is pushing TLS certs to 47 days by 2029. (`x509-prob.md §Lifespans don't match`). "The identity of organizations is defined in the legal system where they're incorporated; anything a certificate authority says is inherently secondary."
- **Focusing on CA vetting is the wrong locus.** "*Certificate authorities aren't the ones that choose or manage the keys in certs.* Holders of certs do that." Risk lives in *holder* key management, which is opaque and unauditable ("the missile silo" analogy). (`x509-prob.md §Governance is opaque`).
- **Certs = one opaquely-managed secret.** "All the tech guarantees ... is that someone provided a public key before the certificate was created." (`x509-prob.md §Governance`).
- **Revocation is disincentivized by design.** Cost/effort of cert fabric creates "a strong incentive to avoid revocation"; ephemerality just trades window size for 52x maintenance burden while still leaving days of compromised operation (`x509-prob.md §Revocation is disincented`).
- **OCSP/CRL "fail open" and phone-home.** "If the OCSP responder is offline, browsers often 'fail open'" (`keri-primer.md §1.1`); certs "support only queries about *now*" (`was.md §Mitigation 3`).
- **CA-rooted trust is jurisdiction-bound.** "assertions rooted in the SHAKEN ecosystem mandated by US regulators are not accepted in Europe or Asia." (`keri-primer.md §1.1`). SHAKEN/STIR is implemented "country by country, not globally" because it depends on CA approval per country; ACDC chains to a global root and crosses borders (`acdc-vc-diff.md §Real-World Validation`).
- **X.509 rotation severs continuity.** Google Cloud (2026) told customers NOT to pin certs because rotation breaks pinning — proof there is "no cryptographic thread joining the old key to the new one" (`x509-prob.md §Prerotation is missing`; `keri-primer.md §1.2`).

### 4.2 W3C VC / DID "decentralized" drift
- **VCs are lossy; six enumerated losses** (`acdc-vc-diff.md`): (1) **Trust chain** — VC captures only "University → You," broader chain "becomes implicit"; the rise of trust registries "is proof that this conceptual gap needs plugging." (2) **Time** — "W3C VCs are generally verifiable only in the present." (3) **Edge weights / conditional logic** — RDF triples can't attach properties to edges; "triple bloat" / reification; ACDCs use a property graph with native `w`/`o`/`s`/`n` edge fields. (4) **Use cases beyond credentials** — VCs assume the three-party issuer→holder→verifier model; "For pure attestation, VCs are the wrong shape" (affidavits, crime-scene evidence, journalism have no "holder"). (5) **Key management transparency** — VC issuer key history is "opaque"; can't tell if a key was compromised before/after issuance; cryptoperiod risk. (6) **Schema stability** — VC `@context` URLs cause "link rot"; redefining a term ("bankAccount"→"savingsAccount") changes signed meaning "without breaking the cryptographic signature."
- **DIDs solved half the problem, then stalled.** DIDs/VCs create indirection (issued to an identifier not a key) — "I worked on both of these standards, and I remain proud of their virtues." BUT: "Evidence is also *issued by* an identifier ... If the issuer updates their identifier, old evidence is invalidated" — "This risk is poorly understood in SSI circles." (`x509-prob.md §Much better alternatives exist`).
- **Most DIDs can only resolve to *current* key state.** "*most DIDs, including crowd favorites like did:web, can only be resolved to the current key state*" — so historical actions are unprovable unless the method supports `versionId`/`versionTime` (`was.md §Mitigation 3`). Issuer key compromise then "invalidates all the evidence they have ever created" — the "driver's license bureau whose recover-from-breach plan required all current license holders to come back to the office."
- **Trust registries are a band-aid that re-centralizes.** "These are a band aid; they just move the centralization back to a different level of the architecture ... immature and fragmented ... primarily address governance for issuers, not issuees." (`x509-prob.md`). ACDC chaining "eliminates the need for trust registries."
- **Blockchain-for-DID has unsolved centralization/regulatory tradeoffs.** "Anybody who tells you the problems are happily solved is either uninformed or disingenuous." (`x509-prob.md`).
- **AID→DID is one-way.** "AIDs can be transformed to DIDs, but the opposite transformation is typically impossible." (`sdjwt-acdc.md §2.2`).

### 4.3 SD-JWT / OAuth / OIDC priors
- **"Selective disclosure" is a bad term.** Has "a long and unpleasant history in financial regulation, where it refers to ... illegal behavior." ACDC's "graduated disclosure" is preferred (`sdjwt-acdc.md §1`).
- **SD-JWTs are standalone envelopes → force centralized issuer registries.** "SD-JWTs will need registries of trusted issuers ... Such registries will need to be centralized, governed, and managed for scale." This "reinforce[s] boundaries between verticals." ACDCs instead "prove the bona fides of issuers by chaining to other ACDCs." (`sdjwt-acdc.md §2.4`).
- **SD-JWT `iat` is self-asserted; tokens verified only vs. current key state.** "*tokens are only designed to be evaluated against current key state*. If keys change, all existing tokens become invalid." Historical/audit questions unanswerable (`sdjwt-acdc.md §2.3`). "OAuth2 and OIDC and SD-JWTs use JWTs as tokens; they inherit the same limitation." (`was.md §Mitigation 3`).
- **SD-JWT signs a *key*, not an *identifier*.** `kid` points at the key, not the identifier, so key rotation invalidates historical signatures and there's no multisig-group signing (`sdjwt-acdc.md §2.3`). Ties cert to X.509 baggage.
- **Identifier flexibility is a false virtue.** SD-JWT allows DID/URL/URN/etc.; "it makes it much more difficult to predict or enforce security properties ... theoretical and practical interop diverge." ACDC is stricter: issuers MUST be AIDs (`sdjwt-acdc.md §2.2`).

### 4.4 Blockchain / consensus / global-ordering priors
- **"Sounds like blockchain" is a lazy tell.** Anchoring needs only per-identifier ordering, not total ordering or consensus: "no permissioning problem, no big central *anything* in the sky, no scale or performance bottlenecks, and no regulatory problems with data locality, privacy, or erasure." (`was.md §Solution`).
- **Right-to-be-forgotten:** blockchain requires "a hard fork of the entire chain" to forget; KERI micro-ledgers let a user "exercise the right to be forgotten by deleting their specific Key Event Log ... without disrupting the global ecosystem." (`keri-primer.md §3.5`).

### 4.5 Merkle-vocabulary confusion (ACDC vs. Merkle Tree Certificates)
- Shared hash/Merkle vocabulary "can obscure as much as it reveals." (`acdc-and-mtc.md §8`). Two *distinct proof obligations*:
  - ACDC graduated disclosure: proof obligation is **semantic** — "that a particular view corresponds to a specific underlying claim"; motive = privacy/correlation-minimization (`acdc-and-mtc.md §4.1`).
  - MTC inclusion proofs: proof obligation is **historical/membership** — "is this object a member of a committed set"; motive = efficiency/scalability (`acdc-and-mtc.md §4.2`).
- "A Merkle inclusion proof establishes placement in a history. A SAID establishes identity of content." (`acdc-and-mtc.md §3.2`). In ACDC "the tree is implicit in the schema" (shape reflects *meaning*); in MTC "the tree is literal" (shape reflects *chronology*).
- Framed explicitly as NOT a bake-off / orthogonal, not competitive.

### 4.6 Signing-semantics anti-patterns
- Cryptographic systems "inherited a bias to assume signing was an assertion of authorship from early message-signing use cases." (`who-sign.md §Signing can have several meanings`). Counter-examples: petitions (stance not authorship), autographs, notaries (certify identity+procedure). UNCITRAL Model Law: a signature can express intent-to-be-bound, endorsement, association, or attestation-of-presence.
- **Opacity, not delegation, is the risk.** "Delegation is unavoidable ... The real question is not whether delegation exists, but *whether it is inspectable*." Single-key governance means "externally, the result is indistinguishable from a lone script with a leaked secret." "*Opaque control collapses meaningful distinctions*." (`who-sign.md §Delegation is normal`).

---

## 5. Precise terminology / definitions

- **AID (Autonomic Identifier):** a KERI self-certifying identifier deriving from its inception event; supports pre-rotation, weighted multisig, witnesses, PQ migration, self-certification (`sdjwt-acdc.md §2.2`, `keri-primer.md §2.1`).
- **SCID (self-certifying identifier):** identifier cryptographically derived from its controlling key material.
- **KEL (Key Event Log):** append-only, controller-signed microledger; "the authoritative source of truth for an AID." Verified by replaying history from the inception event; each event hash-chained to predecessor (`keri-primer.md §2.2`). Event types: `icp` inception, `rot` rotation, `ixn` interaction (anchoring seals without key change).
- **KERL:** (implied) key event *receipt* log — KEL plus witness receipts (corpus uses KEL + witness receipts).
- **TEL (Transaction Event Log):** identifier-specific log for credential status/revocation; TEL events are anchored (hash-recorded) in the KEL (`was.md §Solution`, `keri-primer.md §3.1`). Provides "built-in, realtime revocation support" (`sdjwt-acdc.md §2.3`).
- **SAID (Self-Addressing Identifier):** content hash of a data structure embedded in the structure's own `d` field via the dummy-`#`-placeholder → hash → overwrite algorithm. "An ACDC is not a mutable document; it is a crystallized fact." (`keri-primer.md §3.2`). Enables linking → decentralized authenticated graphs.
- **SAD (Self-Addressing Data):** the data structure that holds its own SAID (`bes.md §1`).
- **bSAID / xSAID (bytewise / externalized SAID):** bes.md extensions of SAIDs to opaque/arbitrary byte streams — bytewise embeds `SAID:<placeholder>` at an insertion point; externalized writes the SAID into the *filename* under a content-embedded regex constraint (*exsertion instruction*), for compressed/encrypted/offset-sensitive formats (`.docx`, PDF). "Echoes" allow one SAID to appear in multiple places (frontmatter, title, HTML comment).
- **Witness:** controller-designated server that stores/serves the KEL and signs receipts; makes NO identity assertion; assumed potentially malicious (`keri-primer.md §2.6`).
- **Backer:** (corpus uses "witness"; backer = ledger-backed witness variant, not elaborated here).
- **Watcher:** verifier/auditor-run entity that polls witnesses to detect duplicity by comparing log heads (`keri-primer.md §2.6`). (Juror/judge roles: part of the KERI watcher-network taxonomy — NOT covered in this corpus; see gaps.)
- **Duplicity:** two validly-signed conflicting events at the same sequence number; the identity-layer "double-spend."
- **Pre-rotation:** commit (as a hash) to the next key set in advance; the "firewall between day-to-day use and occasional governance."
- **Weighted multisig:** fractionally-weighted thresholds declared in-KEL (e.g., `kt` = `[["1/2","1/2","1/2"],["1/3","1/3","1/3","1/3"]]`), clauses joined by OR; makes governance "explicit, auditable, and comparable." KERI's innovation "is less about *inventing* and more about *exposing*." (`keri-primer.md §2.4`).
- **IPEX (Issuance and Presentation EXchange protocol):** offer→request→grant credential exchange; issuer and holder *each* anchor the transaction in their own KEL → prevents spam and gives "non-repudiation of receipt" (`keri-primer.md §3.1`).
- **Graduated disclosure:** ACDC's privacy mechanism; can elide substructures down to their SAIDs (down to a ~44-byte identifier for an arbitrarily large structure/tree). A fully-expanded and a partially-disclosed ACDC "verify the same way" (`acdc-and-mtc.md §4.1`, `sdjwt-acdc.md §2.5`).
- **CESR (Composable Event Streaming Representation):** dual text/binary serialization; a single signature (over one representation) verifies both because they're isomorphic. Self-framing via code-prefix (Read Code → Lookup Length → Read Bytes) → pipelining ("cryptographic traffic cop"). Text form = "JSON with a few additional rules"; crypto primitives are "self-describing strings, not JSON subobjects" (`sdjwt-acdc.md §2.5`, `keri-primer.md §4`).
- **Crypto agility (CESR):** PQ upgrade = "associating new meaning to an unused prefix slot in an existing code table"; old parsers still work (e.g., `D` prefix = Falcon-512 public key) (`keri-primer.md §4.3`).
- **EGF (Ecosystem Governance Framework):** referenced via GLEIF vLEI EGF but not defined in this corpus (see gaps).
- **Edge operators (`o`), weight (`w`), schema (`s`), node (`n`):** native ACDC edge fields making edges first-class property-graph objects (`acdc-vc-diff.md §Loss 3`).
- **Alias / petname:** local, non-unique, changeable private nickname over an opaque identifier; "never to be mistaken for the identifier itself." COIA = the naming convention; leading `0` flag = "unconfirmed: there may be a man in the middle here." (`oia.md`).
- **Facet-granular identity:** one AID per facet = triple `(who, role, context)`; "Cecilia as chief executive at Acme" etc. are "uncorrelatable identifiers for one person." Parallels the act-side triple `(telos, effect, state-kind)` (`sda.md §6`).

---

## 6. Delegated-authority model (sda.md) — doctrine for agentic/AI trust

- **Signet-ring vs. key distinction:** "The key authorizes an act; the ring authorizes a person to stand in your place." API keys/bearer tokens are "a signet ring handed out for an errand" (`sda.md §1`).
- **Three modern reductions of one old art:** (1) formal access-control/capabilities (SPKI→macaroons→biscuit→UCAN; RAR/GNAP) — rigorous on acts, silent on "for whom"; (2) action taxonomies (O*NET, MIT Process Handbook, FrameNet) — MECE act-surfaces but single-actor, no delegation; (3) SSI identity/guardianship — kept the relationship, "never built the acts." Each dropped (a) the full act surface and (b) the "on behalf of · in whose interest · who bears the obligation" dimension (`sda.md §2`).
- **Four forms of indirect identity control** distinguished by whose interest governs: delegation, guardianship, controllership, stewardship (`sda.md §1`).
- **Act = vector of (effect, state-kind) coordinates.** Five effects: `observe`, `create`, `modify`, `preserve`, `destroy`. Six state-kinds: `information`, `record`, `commitment`, `authority`, `resource`, `relationship`. Gate = the *join* (strictest coordinate). Gates are *derived*, not hand-maintained; a gate signals boundary-crossing, not distrust (`sda.md §4`).
- **Authority to act vs. authority to authorize** are independent; "Power at the top is *allocative, not executive*." A powerful orchestrator with empty act-surface is "contained not by watching it but by construction" (`sda.md §5`).
- **Open-loop vs. closed-loop verification** — THE architectural fork:
  - Closed-loop (object capabilities): "the party that *issues* authority is the same party that *checks* it" (OS kernel; macaroon third-party caveats = "a phone-home").
  - Open-loop (verifiable credentials): "a third party who is *not* the issuer can verify authority *without* consulting the issuer ... Authority is analyzed by a stranger." Forces full disclosure, published gate function, and self-verifiable proofs traveling *with* the act (`sda.md §7`).
- **Contain-by-construction:** a delegate's very identifier "commits to its delegator" so forbidden acts are "not merely against the rules but outside the space of possible moves" (KERI cooperative delegation). "Where a credential says 'a verifier will refuse this,' construction says 'this cannot be built.'" (`sda.md §7`).
- **Standing authority vs. exhaustible authority:** open-loop answer to authority-drift is not per-act minting (that's a reference monitor / closed loop) but derived-per-act gates recomputed at the execution boundary + real-time revocation (`sda.md §8`).
- **Joint issuance** (from Verifiable Dossier work): a grant satisfied by a "weighted threshold of endorsements, each owner signing from their own identifier, asynchronously and with no shared key" — refines KERI multisig into something "lighter and composable" (`sda.md §8`).

---

## 7. Worked examples, schemas, real-world usage

- **vLEI / GLEIF trust graph:** GLEIF → Qualified vLEI Issuers → legal entities → role credentials (CEO/CFO) → individuals; each links via SAID; "A verifier receiving an employee's credential can traverse the chain back to GLEIF without consulting a trust registry. The entire graph is self-certifying." Production, global, cross-jurisdiction, "without certificate authorities or blockchains." (`acdc-vc-diff.md §Real-World Validation`). First ACDC global standard = ISO 17442-3 (vLEIs), finalized Oct 2024 (`sdjwt-acdc.md §2.7`).
- **Verifiable Voice Protocol (VVP):** ACDC-based improvement on STIR/SHAKEN; chains trust to a *global* root, crossing borders without per-country intermediary approval (`acdc-vc-diff.md`).
- **Supply-chain conflict-mineral chain:** Mine(ACDC1, schema A, SAID X, edges→legal-ID + RMI certification) → Refiner(ACDC2, B, Y, edge→X) → Manufacturer(ACDC3, C, Z, edge→Y) → Retailer(ACDC4, edge→Z). Consumer scans QR, software "follows all edges in the entire evidence graph" for "*transitive trust*." "no party in the middle can swap out a bad component for a good one without breaking the chain." (`keri-primer.md §3.4`).
- **Journalist evidence graph:** weighted attestations (0.9 leaked memo, 0.6 anonymous tip, 0.95 independent audit); readers "trace the evidence graph." (`acdc-vc-diff.md §Loss 1`).
- **Corporate-board & break-glass multisig** scenarios (`keri-primer.md §2.4`).
- **Schemas:** ACDC schemas are JSON-Schema (an existing standard), embedded-by-SAID; "Schemas do not require standardization — just publication and consensus on use within an ecosystem." vs. SD-JWT's IANA registration (`sdjwt-acdc.md §2.7`). ACDC schema referenced "by its cryptographic content, not its location" → "no link that can rot" (`acdc-vc-diff.md §Loss 6`).
- **Institutional roots:** ACDC from Sam Smith + Phil Feairheller (ToIP/WoT/Linux Foundation), sponsored via GLEIF ← G20 Regulatory Oversight Committee → "more connected to global banking and less connected to big tech." SD-JWT from JWT inventors + Microsoft/Ping, "closely affiliated with OpenID Connect and OAuth2." (`sdjwt-acdc.md §2.6`). Also GSMA Open Verifiable Calling; ToIP Dossier Task Force builds a composition layer *on* ACDCs (`acdc-and-mtc.md §7.1`).

---

## 8. Exact short quotes with citations (<=25 words)

1. "The identifier is the root of trust: The binding between the ID and the key must be mathematical ... not administrative" — `keri-primer.md §1.3`.
2. "Detection (rather than prevention) allows KERI to operate with low latency while ensuring that any dishonesty is provable." — `keri-primer.md §2.6`.
3. "The trust model is adversarial: witnesses are assumed to be potentially malicious." — `keri-primer.md §2.6`.
4. "A witness makes no such assertion. A witness simply stores and serves events." — `keri-primer.md §2.6`.
5. "Pre-rotation establishes a firewall between day-to-day use and occasional governance." — `keri-primer.md §2.3`.
6. "An ACDC is not a mutable document; it is a crystallized fact." — `keri-primer.md §3.2`.
7. "KERI rejects the need for global consensus regarding identity." — `keri-primer.md §2`.
8. "no total ordering, and no cumbersome consensus algorithm." — `was.md §Solution`.
9. "Malfoy can keep generating new evidence that looks like it originated in the past, forever!" — `was.md §Retrograde attack`.
10. "Keep tamper-evident records that can prove how a given signing event relates in time to changes in the associated key state." — `was.md §Solution`.
11. "renewing an identity is a non-sequitur." — `x509-prob.md §Lifespans don't match`.
12. "Certificate authorities aren't the ones that choose or manage the keys in certs. Holders of certs do that." — `x509-prob.md §Governance`.
13. "ACDCs are not just a format — they're a methodology for creating verifiable evidence." — `x509-prob.md`.
14. "These are a band aid; they just move the centralization back to a different level of the architecture." (trust registries) — `x509-prob.md`.
15. "most DIDs, including crowd favorites like did:web, can only be resolved to the current key state." — `was.md §Mitigation 3`.
16. "AIDs can be transformed to DIDs, but the opposite transformation is typically impossible." — `sdjwt-acdc.md §2.2`.
17. "SD-JWTs will need registries of trusted issuers." — `sdjwt-acdc.md §2.4`.
18. "Judgments about authenticity can ... be reduced to an objective mathematical computation, whereas judgments about veracity inherently require subjective assessments of reputation." — `authenticity-vs-veracity.md`.
19. "The gap between proved and guessed is the gap a man-in-the-middle attacker lives in." — `oia.md §Proved versus guessed`.
20. "Automate the introduction. Automate the proof where you can. But never automate the verification of the proof." — `oia.md`.
21. "An alias must never be parsed for meaning by anyone but its creator." — `oia.md`.
22. "Expecting a single, clean answer is usually a mistake." (who is signing) — `who-sign.md`.
23. "Opaque control collapses meaningful distinctions." — `who-sign.md`.
24. "A Merkle inclusion proof establishes placement in a history. A SAID establishes identity of content." — `acdc-and-mtc.md §3.2`.
25. "a third party who is not the issuer can verify authority without consulting the issuer" — `sda.md §7`.
26. "The key authorizes an act; the ring authorizes a person to stand in your place." — `sda.md §1`.
27. "Sincerity stays gate-able and auditable, never provable." — `sda.md §8`.
28. "you cannot reconstruct what you've lost." (lossy primary evidence) — `acdc-vc-diff.md`.
29. "The entire graph is self-certifying." (vLEI) — `acdc-vc-diff.md`.
30. "A signature is evidence that a signing mechanism ran." — `sign-author.md`.

---

## 9. Cross-cutting doctrinal synthesis (the "purity vs. drift" thesis)

- The corpus frames a lineage: X.509/PKI = identity evidence 1.0; DIDs+VCs = 2.0 ("next-generation X509," praised but half-finished); ACDC/KERI = 3.0, in production since Dec 2022 (`x509-prob.md`). The "drift" critique is that SD-JWT, W3C-VC, and most DID methods imported PKI/OAuth assumptions (issue-to-key thinking, current-key-state-only verification, standalone envelopes, trust registries, `@context` link-rot, three-party holder bias) and thereby re-created centralization one level up while losing time, trust-chain, and key-history fidelity.
- The "purity" position: trust must be *cryptographic and local*, not *administrative and global*; verification must be *offline / open-loop / observer-independent*; security is *survivable and duplicity-evident* (detect + recover), never claimed as invulnerable/prevented; identity is *facet-granular and uncorrelatable*; and every guarantee is stated against explicit assumptions with honest scope limits (bes.md and sda.md are the models of this discipline).
- Recurring rhetorical moves worth noting for a synthesizer: right-tool-for-the-job disclaimers ("I am not down on certs"; VCs "are not bad technology"), analog-world grounding (Pharaoh's ring, Hammurabi, notaries, RAW-vs-JPEG), and consistent insistence that the human keeps the final verification judgment.
