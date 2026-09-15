# Doctrine-mining notes: Decentralization purity vs. SD-JWT / W3C-VC / DID drift

## Pin and provenance

Source corpus: Daniel Hardman's "Codecraft Papers", repo `~/code/me/papers` (the note previously recorded this as `/home/daniel/code/papers`, which is not where the repo lives; corrected 2026-09-15). **Pinned at `181569b64`** on `main`, mined 2026-09-15. Previous pin `f94f50f`, mined 2026-07-17.

**Provenance class: none of the tier markers apply.** These are *authored positions, not normative text*. The manifest marks this source `[N]`, and that marker is wrong here in the specification sense; `refresh/sources.yaml` says so in its own caveat and the field is unused. Every claim below is Daniel Hardman's framing of KERI/ACDC and of the things he compares it to, and chapters must cite it as such. Where a paper states a comparative verdict — that SD-JWTs will need centralized issuer registries, that most DID methods cannot answer historical questions — that is the author's assessment, not a surveyed result, and the corpus repeats it as one.

Primary sources read in full at `181569b64`: `keri-primer.md`, `was.md`, `x509-prob.md`, `sdjwt-acdc.md`, `acdc-vc-diff.md`, `acdc-and-mtc.md`, `oia.md`, `who-sign.md`, `sign-author.md`, `authenticity-vs-veracity.md`, `bes.md`, `sda.md`. Read this pass for comparative material the note had not previously carried: `wtbo.md`, `amp-diff.md`, `m-glance.md`, `active-discovery.md` §1, `crna.md` §Conclusion.

## What the 2026-09-15 pass covered, and what it did not

Of the twelve papers this note's claims rest on, **eleven are byte-identical between `f94f50f` and `181569b64`**, and the twelfth (`sda.md`) changed only by the addition of a `pdf_url:` line to its frontmatter. No quote in this note was superseded by a source change, and no quote was cut. That is a real negative result, not an absence of work: it means the note's citation base is stable, and the changes in the window land on papers the note had not yet mined.

**Line hints re-anchored:** every quote in §8 now carries a `L<n>` hint verified against the working tree at `181569b64` (`HEAD` == pin, tree clean, so working-tree line numbers are the pin's line numbers). §11's newly mined claims carry hints from the same read. Selected body claims in §§1–7 that do not appear in §8 carry hints added inline this pass.

**Line hints NOT re-anchored:** the majority of the body claims in §§1–7. The note as originally written carried **no line hints at all**, so there was nothing to re-anchor for them — this is a standing §1-of-standards gap, not drift. Every one of those claims was re-verified verbatim against its source at `181569b64` this pass; what they lack is the positional hint, and §8 plus the inline hints cover the load-bearing subset. Treat an unhinted body claim as verified-at-pin but unlocated.

**Three quotes were silently corrected by an earlier pass and are now restored to the source's spelling.** See §10.2. None was a fabrication; each was a typo in the source that the note had tidied. Under standards §7 a quote that cannot be found verbatim is not a quote, so they now carry `[sic]`.

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
- Retrograde attack anatomy: attacker who *ever* gets key K can forge evidence "that looks like it originated in the past, *forever*" — and remains possible "even if she rotates or revokes K before Malfoy steals it" (`was.md`, untitled opening, L33; the note previously cited a `§Retrograde attack` heading that does not exist — see §8 item 9). Backdating window has "no end point."
- Three flawed mitigations catalogued: (1) contextual clues (unreliable), (2) retroactive revocation ("dangerous and foolish"; lets Alice cheat/repudiate her own acts), (3) "verify against current key state only" = **pyrrhic victory** — "After-the-fact audits are impossible, because anything in the past can be faked with compromised keys." (`was.md §Mitigation 3`).
- Solution = *anchored signatures*: "Keep tamper-evident records that can prove how a given signing event relates in time to changes in the associated key state." (`was.md §Solution`). Implemented via KELs + TELs; "KERI anchors (records the hashes of) signed TEL events in the KEL to make sequence unambiguous."
- Payoff = time-independent verification: "An analysis of an anchored signature will produce the same result no matter when it happens, which makes historical audits ... possible." Evidence stays valid across "any number of key rotations, making it effecitvely [sic] permanent." (`was.md §Conclusion` L86). The `[sic]` is the source's own typo; the note previously quoted this with the spelling corrected, which made the quote unfindable. See §10.2.
- Anchored ≠ paired signatures. Paired = signature bundled in the container because "the format says so" (VC `proof`, JWT bundle, X.509 `signature` over `tbsCertificate`). Anchored = provable association via the KEL, "independent of any container context." (`keri-primer.md §3.3`). Verify by extracting AID → retrieving KEL from witness → traversing to the sequence number → confirming the ACDC digest is anchored there.
- NIST SP 800-102 cited: a signed message "provides no assurance that the private key was used to sign the message at that time." KERI's native anchoring removes the need for external Time-Stamp Protocols (`keri-primer.md §3.3`).

### 2.5 Local / observer-dependent validity; offline verification
- Verification is offline-capable and does not phone home. In MTC comparison: KERI/ACDC "verification can be offline"; freshness is "about continuity and completeness of key state" rather than recency (`acdc-and-mtc.md §2 table, §5.1`).
- Contrast: OCSP / CRL / trust registries are "phone home" models; "A registry consulted at verification time is a phone-home in disguise." (`sda.md §7` L119).
- Open-loop verification (see §5.3 below) is the architectural statement of observer-independence: "a stranger can check authority without consulting its issuer."

### 2.6 Guarantees stated relative to explicit assumptions
- Anchoring closes the *future* attack window but not the pre-detection window: "Alice is still vulnerable to mischief until she notices a compromise. However, during this time Malfoy is forced to create evidence with new dates" (`was.md §Solution`).
- bes.md §3.6 Threat Model and Limitations is a model of explicit-assumption discipline: bytewise/externalized SAIDs "do not provide confidentiality, access control, or resistance to format-aware semantic transformations." (`bes.md §3.6` L150). Assumes author inserts insertion point at creation time and handling preserves bytes; "any byte-changing transformation is treated as producing a new identity" (`bes.md §abstract` L9).
- sda.md §8 is explicit about what the delegation model does NOT do: it makes an act's *category* checkable but "cannot tell whether the agent attempting it is faithful. Sincerity stays gate-able and auditable, never provable. That is not a defect ... it is a property of the world."

---

## 3. Invariants and "never do X" rules

- **Never confuse proved with guessed.** The "single most dangerous mistake in the whole design" (`oia.md` abstract). "The gap between proved and guessed is the gap a **man-in-the-middle** attacker lives in." (`oia.md §Proved versus guessed`).
- **Never automate the final verification of a proof.** "Automate the introduction. Automate the proof where you can. But never automate the verification of the proof." (`oia.md §Connections, and the line between introducing and proving` L86 — the note previously cited this as `§Connections`, which is not the heading's text). The human must take "the last step — the moment a human weighs that evidence and decides it is good enough to trust *this* party, for *this* purpose, now." **Qualified 2026-09-15 by `amp-diff.md` — see §11.3: the human step this invariant protects is, by the author's own later analysis, broken against an adversary unless it is run as a seeded commit-and-reveal walk.**
- **Never parse a stranger's alias for meaning.** "An alias must never be parsed for meaning by anyone but its creator." Doing so "has trusted a private note it had no business trusting. The name is a memory aid, not evidence." (`oia.md §An alias is a private nickname`).
- **Never mistake an alias for an identifier.** "treat an alias as an identifier and you get collisions; cache it ... and you get staleness; parse a stranger's alias for meaning and you get an attack surface." (`oia.md`).
- **Never assume a signature means authorship.** "People often treat a signature as if it were a claim of authorishop [sic]. That is sometimes true. But it is not what signatures *are* in general" (`sign-author.md` L18; the source's typo, see §10.2). A signature "is evidence that a signing mechanism ran" (L58); meaning comes from role/ceremony/policy/protocol (L50, L62–63).
- **Never present a single clean answer to "who is signing?"** "Asking the question is insightful. Expecting a single, clean answer is usually a mistake." (`who-sign.md` L22). Control, authority, responsibility, and attribution "overlap but do not coincide" (L41).
- **Never collapse the key vs. affordance ("errand vs. signet ring") distinction.** Don't hand over the ring for an errand: "Possession of an API key ... makes the holder indistinguishable from the account it belongs to, free to do anything that account can." (`sda.md §1`).
- **Never verify against a registry/callback.** "verification must succeed from the credential and key-state alone, and any registry or log is an issuance-time and audit-time convenience, never a verification-time dependency." (`sda.md §7`).
- **SAID invariant:** any change to SAD or SAID breaks correspondence; "Any change to the byte stream after saidification necessarily produces a different SAID and is therefore treated as a new version" (`bes.md §3.6` L152). A bytewise SAD "MUST contain exactly one primary insertion point"; leftmost match is primary, others are echoes (`bes.md §3.2.2` L91 — the note previously cited `§3.2`; the sentence sits in the ABNF/regex subsection, and the echo rule it points forward to is `§3.5.1` L136).
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
- **X.509 rotation severs continuity.** In May 2026 Google Cloud told customers to expect an RSA→ECDSA chain switch on `googleapis.com` and warned them not to pin certificates, because pinning "will cause your application to break during routine certificate rotations" — proof there is "no cryptographic thread joining the old key to the new one" (`x509-prob.md §Prerotation is missing` L107; `keri-primer.md §1.2`). `wtbo.md §6` L149 reads the same episode as a scale preview: a *voluntary* swap "still triggered a global, deadline-driven scramble across every custom trust store and pinning client".

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
- Cryptographic systems "inherited a bias to assume signing was an assertion of authoriship [sic] from early message-signing use cases." (`who-sign.md §Signing can have several meanings` L75; the source's typo, see §10.2). Counter-examples: petitions (stance not authorship), autographs, notaries (certify identity+procedure). UNCITRAL Model Law: a signature can express intent-to-be-bound, endorsement, association, or attestation-of-presence.
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

Every entry below was re-read verbatim in its source at **`181569b64`** on 2026-09-15 and carries a line hint as of that commit. Line hints drift and are expected to; the quoted text is the citation of record. Where an entry's heading has been corrected this pass, the correction is stated inline — an unfindable heading is as much a broken citation as an unfindable quote.

1. "The identifier is the root of trust: The binding between the ID and the key must be mathematical ... not administrative" — `keri-primer.md §1.3 Requirements for a new stack` L45.
2. "Detection (rather than prevention) allows KERI to operate with low latency while ensuring that any dishonesty is provable." — `keri-primer.md §2.6 Witnesses and the watcher network` L159.
3. "The trust model is adversarial: witnesses are assumed to be potentially malicious." — `keri-primer.md §2.6` L155.
4. "A witness makes no such assertion. A witness simply stores and serves events." — `keri-primer.md §2.6` L153.
5. "Pre-rotation establishes a firewall between day-to-day use and occasional governance." — `keri-primer.md §2.3 Pre-rotation` L92.
6. "An ACDC is not a mutable document; it is a crystallized fact." — `keri-primer.md §3.2 SAIDs` L188.
7. "KERI rejects the need for global consensus regarding identity." — `keri-primer.md §2 KERI` L57.
8. "no total ordering, and no cumbersome consensus algorithm." — `was.md §Solution` L78.
9. "Malfoy can keep generating new evidence that looks like it originated in the past, *forever*!" — `was.md`, untitled opening before §Mitigation 1, L33. **Heading corrected 2026-09-15:** the note previously cited this as `§Retrograde attack`, and `was.md` has no such heading at any commit in range; the retrograde-attack anatomy sits in the paper's unheaded opening (L18–L33).
10. "Keep tamper-evident records that can prove how a given signing event relates in time to changes in the associated key state." — `was.md §Solution` L72 (a blockquote).
11. "renewing an *identity* is a non-sequitur." — `x509-prob.md §Lifespans don't match` L40. The source italicizes *identity*; the note previously dropped the emphasis markers.
12. "*Certificate authorities aren't the ones that choose or manage the keys in certs.* Holders of certs do that." — `x509-prob.md §Governance is opaque, centralized, and inconsistent` L65. **Heading corrected:** previously cited as `§Governance`.
13. "ACDCs are not just a format &mdash; they're a *methodology* for creating verifiable evidence." — `x509-prob.md §Much better alternatives exist` L164. The source uses the `&mdash;` entity, not a literal em dash.
14. "These are a band aid; they just move the centralization back to a different level of the architecture." (trust registries) — `x509-prob.md §Much better alternatives exist` L158.
15. "most DIDs, including crowd favorites like did:web, can only be resolved to the current key state" — `was.md §Mitigation 3 (pyrrhic victory)` L60.
16. "AIDs can be transformed to DIDs, but the opposite transformation is typically impossible." — `sdjwt-acdc.md §2.2 Identifiers` L41 (in the indented Note block).
17. "SD-JWTs will need registries of trusted issuers." — `sdjwt-acdc.md §2.4 Chaining` L63. The full sentence continues "...because verifiers are limited to asking whether a particular envelope is valid in isolation".
18. "Judgments about authenticity can ... be reduced to an objective mathematical computation, whereas judgments about veracity inherently require subjective assessments of reputation." — `authenticity-vs-veracity.md §Independence` L35. The elision covers the source's parenthetical "&mdash; *if managed very carefully* &mdash;", which is load-bearing and should not be dropped when the claim is used.
19. "The gap between proved and guessed is the gap a **man-in-the-middle** attacker lives in" — `oia.md §Proved versus guessed` L66.
20. "Automate the introduction. Automate the proof where you can. But never automate the verification of the proof." — `oia.md §Connections, and the line between introducing and proving` L86. **Heading corrected:** previously cited as `§Connections`.
21. "An alias must never be parsed for meaning by anyone but its creator." — `oia.md §An alias is a private nickname` L46.
22. "Expecting a single, clean answer is usually a mistake." (who is signing) — `who-sign.md`, untitled opening before §A human analogy, L22.
23. "*Opaque control collapses meaningful distinctions*" — `who-sign.md §Delegation is normal—opacity is the risk` L106.
24. "A Merkle inclusion proof establishes placement in a history. A SAID establishes identity of content." — `acdc-and-mtc.md §3.2 Trees, structure, and meaning` L86.
25. "a third party who is *not* the issuer can verify authority *without* consulting the issuer" — `sda.md §7 Open loop, not closed` L115. Followed three clauses later by "Authority is analyzed by a stranger."
26. "The key authorizes an act; the ring authorizes a person to stand in your place." — `sda.md §1 A model simpler than the problem` L25.
27. "Sincerity stays gate-able and auditable, never provable." — `sda.md §8 What is settled, and what is open` L131.
28. "once you've chosen a lossy format as your primary evidence, you cannot reconstruct what you've lost" — `acdc-vc-diff.md §Lossless vs. Lossy: A Choice That Matters` L29.
29. "The entire graph is self-certifying." (vLEI) — `acdc-vc-diff.md §Real-World Validation` L117.
30. "A signature is evidence that a signing mechanism ran." — `sign-author.md §The practical lesson` L58.

---

## 9. Cross-cutting doctrinal synthesis (the "purity vs. drift" thesis)

- The corpus frames a lineage: X.509/PKI = identity evidence 1.0; DIDs+VCs = 2.0 ("next-generation X509," praised but half-finished); ACDC/KERI = 3.0, in production since Dec 2022 (`x509-prob.md`). The "drift" critique is that SD-JWT, W3C-VC, and most DID methods imported PKI/OAuth assumptions (issue-to-key thinking, current-key-state-only verification, standalone envelopes, trust registries, `@context` link-rot, three-party holder bias) and thereby re-created centralization one level up while losing time, trust-chain, and key-history fidelity.
- The "purity" position: trust must be *cryptographic and local*, not *administrative and global*; verification must be *offline / open-loop / observer-independent*; security is *survivable and duplicity-evident* (detect + recover), never claimed as invulnerable/prevented; identity is *facet-granular and uncorrelatable*; and every guarantee is stated against explicit assumptions with honest scope limits (bes.md and sda.md are the models of this discipline).
- Recurring rhetorical moves worth noting for a synthesizer: right-tool-for-the-job disclaimers ("I am not down on certs" — `x509-prob.md` L22; VCs "are not bad technology" — `acdc-vc-diff.md §When Lossy Formats Make Sense` L105), analog-world grounding (Pharaoh's ring, Hammurabi, notaries, RAW-vs-JPEG), and consistent insistence that the human keeps the final verification judgment. **That last move is the one the 2026-09-15 pass qualified — see §11.3.**

---

## 10. The 2026-09-15 pass: what did not change, and what was corrected

### 10.1 Negative results at `181569b64` (recorded because a quiet month and a broken config look identical)

Searched for and **not found**, at `181569b64`:

- **No change to any source this note quotes.** `keri-primer.md`, `was.md`, `x509-prob.md`, `sdjwt-acdc.md`, `acdc-vc-diff.md`, `acdc-and-mtc.md`, `oia.md`, `who-sign.md`, `sign-author.md`, `authenticity-vs-veracity.md` and `bes.md` are byte-identical to `f94f50f`. `sda.md` differs by one added frontmatter line (`pdf_url:`) and no body text. Consequently **zero quotes superseded and zero quotes cut** this pass.
- **No dangling reference to `ppred.md`.** `ppred.md` was withdrawn from the archive in this window and delisted from `index.md`. Nothing in this note, in any other `raw/` note, in `bible/`, or in `keri-doctrine.md` refers to it — checked by a tree-wide search of the bible repo on 2026-09-15. The withdrawal breaks no citation.
- **No reference anywhere in the bible to `crna.md`, `amp-diff.md`, `m-glance.md`, `entviz` or `randomart`** before this pass. The corpus had never mined the perceptual-verification papers, so the crna erratum and the amp-diff/m-glance revisions could not have invalidated anything the corpus says. They are additions, not corrections to the corpus.
- **No rename or retitle in `index.md` that breaks a citation.** The catalogue changes in this window are: `ppred.md` removed; `prog-a.md` and `active-discovery.md` added; two reorderings; and `Canonical Quoted Text` re-dated from 2023-06-01 to 2026-08-24 and given the parenthetical `(CQT)`. No paper this note cites was renamed or re-versioned in a way that breaks a `file §heading` citation.
- **`cfa-paper.md` and `intent-monograph.md` touch no quote the corpus uses.** Their only changes in this window are frontmatter: a DOI normalized to `10.2139/ssrn.5940195` and two `pdf_url` values repointed from SSRN delivery URLs to `dhh1128.github.io`. Neither paper is cited anywhere in the bible.

### 10.2 Three quotes the note had silently corrected

Standards §7 says a quote that cannot be found verbatim is cut, not reworded into something findable. Three of this note's quotes had been tidied by an earlier pass, each fixing a typo in the source, and each thereby made unfindable by search:

1. `was.md §Conclusion` L86 reads "making it **effecitvely** permanent"; the note had "effectively".
2. `sign-author.md` L18 reads "a claim of **authorishop**"; the note had "authorship".
3. `who-sign.md §Signing can have several meanings` L75 reads "an assertion of **authoriship**"; the note had "authorship".

None is a fabrication and no claim depends on the spelling, so none is cut. All three now carry `[sic]` at their point of use. Recorded because the failure mode is worth naming: a quote silently improved is a quote a later reader cannot verify, and the improvement is invisible precisely because it looks correct.

### 10.3 Heading citations corrected

`was.md §Retrograde attack` does not exist and never did — the material sits in the paper's unheaded opening. `x509-prob.md §Governance` is `§Governance is opaque, centralized, and inconsistent`. `oia.md §Connections` is `§Connections, and the line between introducing and proving`. `bes.md §3.2` for the one-primary-insertion-point rule is `§3.2.2`. Each is corrected at its point of use and in §8.

---

## 11. Newly mined 2026-09-15: comparative material this note had not carried

§11.1 and §11.2 are cross-references, deliberately thin. §11.3 and §11.4 are this note's own, and are new to the whole bible.

### 11.1 `wtbo.md` — owned by `raw/05`, cited from here, not re-mined

`wtbo.md` ("Where Trust Bottoms Out: X.509, Certificate Transparency, and KERI's DPKI Architecture", v1.8, revised 2026-08-20) is the corpus's most direct head-to-head comparative paper. It is squarely on this note's subject, and the instinct on finding it unmined here was to mine it — but it is already mined, thoroughly and with line hints, in **`raw/05-papers-priority.md`**, which owns it. Duplicating it would mean two notes independently maintaining the same quotes, which is how a corpus acquires two versions of one claim. **So: for the X.509/CT comparison, cite `raw/05`.** Specifically, `raw/05` already carries the browser-vendors-as-ultimate-arbiter claim, the renewal-proves-less claim, the invisible-forgery-window claim, the "constraints of *youth*, not of *architecture*" candor, the thin-formal-literature candor, the eIDAS legal-standing gap, the load-bearing-complexity claim, and the EU/ENISA Annex Ia agility argument.

Two claims in `wtbo.md` that `raw/05` does *not* carry, and that belong on this note's drift axis:

- **Expiry is a property of the standard, not of practice.** X.509's mandatory `Validity` field (`NotBefore`/`NotAfter`) means "Evidence of identity expires by design, not by necessity." (`wtbo.md §1` L34). This sharpens §4.1's lifespan-mismatch argument from `x509-prob.md`, which argues from deployment convention, into a statement about what the standard mandates. The drift it names is not that operators chose short lifetimes; it is that the format has no way to express non-expiring evidence.
- **The Google 2026 episode as a scale preview.** §4.2 records the RSA→ECDSA warning from `x509-prob.md §Prerotation is missing` L107 as evidence that X.509 rotation severs continuity. `wtbo.md §6` L149 reads the same episode for a second thing: a *voluntary* swap on one provider's endpoints "still triggered a global, deadline-driven scramble across every custom trust store and pinning client", which the paper calls "a preview in miniature" of the mandatory post-quantum transition.

### 11.2 `active-discovery.md` — the retraction is `raw/05`'s; what it does to §9 is this note's

`active-discovery.md` (published 2026-08-12, this window) contains the author retracting, in print, a claim he had made in talks: that a privacy-preserving discovery design should leave no aggregator at all. **`raw/05` §"An author retracting his own prior claim, in print" carries the quotes** (`active-discovery.md §What the design must deliver` L51 and L57 at `181569b64`) and draws the methodological lesson — that a design Hardman advocated in a talk is not a stable citation. Do not re-quote them from here.

What `raw/05` does not draw, and what belongs on this note's axis, is the consequence for §9's purity thesis. §9 characterizes the corpus's position as trust that is cryptographic and local rather than administrative and global, with verification observer-independent. The retraction is the author drawing a boundary on that position from the inside: for discovery among strangers, decentralization-*by-absence* is unachievable for reasons he calls structural, and what is achievable is decentralization-*by-split* — no party able to act on the linkage alone, each holder blinded to its meaning. That is a materially weaker property, and unlike absence it still depends on the restraint and governance of the parties holding the pieces. §9's framing is not wrong, but it must not be read as claiming absence is attainable wherever it is wanted. **Carried into §12.3 as an unresolved tension.**

### 11.3 `amp-diff.md` and `m-glance.md` — the human comparison step, and a downward revision

These two are the papers `oia.md` L70 and L100–L102 cite (as its references [4] and [5]) for the claim that the honest way to clear a COIA `0` flag is to "change the task from reading to *recognizing*" by rendering the identifier as a picture. They are therefore the evidentiary base under the note's §3 invariant about never automating the final verification of a proof, and they had never been mined.

**The anti-pattern (§4-class material).** "Visual hash" names two classes of algorithm with opposite goals: "**perceptual hashing** for machine similarity detection, and **authentication visualization** for human difference detection" (`amp-diff.md §3` L146), and "Conflating them is a design error with security consequences" (same line). The abstract states it harder — the paper sets out to "show that conflating them is a security bug" (`amp-diff.md §abstract` L16). The paper is explicit that this framing is its own: "The labels are our framing rather than settled field terminology" (L146), which is exactly the author's-assessment-not-surveyed-result distinction standards §4 requires.

**The downward revision (v1.2 → v1.3 in this window).** `amp-diff.md`'s habituated perceptual-entropy estimate moved from "roughly **20–40 bits**" to a split reading: a summed ceiling of "roughly **28–50 bits**" plus an operative one-glance figure "between a few bits and the low teens" (`amp-diff.md §4.3.9` L310, L320; §6.3 L397). The conclusion drawn is blunt: "Casual comparison is not marginally weak against such an adversary; it is broken." (`amp-diff.md §4.3.9` L324), and therefore "wherever an adversary is in scope, the seeded walk of §5.2 is a requirement, not an enhancement for high-assurance settings" (same line).

**A second retraction inside the same revision.** v1.2 said two pooled human nonces comfortably reach the seed-entropy threshold the verification walk needs; v1.3 says "Two pooled human nonces do **not** comfortably reach that." (`amp-diff.md §5.2` L362), and quantifies the damage — two one-digit nonces cap a "once in twenty-five hundred" survival bound at "once in ninety-seven".

**The provenance correction, which is the most transferable finding.** `m-glance.md` v1.1 described its adversarial reviews as "two independent adversarial expert reviews, one in vision science, one in security usability". v1.2/1.3 retracts that: "Those passes were conducted by AI models prompted to argue from a named lens, not by human domain experts" (`m-glance.md §1` L71–L72, soft-wrapped in source), and "They are a structured way to attack one's own assumptions, not independent validation" (L73–L74). `amp-diff.md`'s self-characterization moved correspondingly from "internally adversarially reviewed" to "*theoretically motivated, adversarially self-reviewed, and empirically untested*" (`amp-diff.md §6.3` L405). **The general lesson, which applies to this corpus's own methods: an adversarial review run by AI personas is a structured self-attack, not independent validation, and describing it as the latter is a provenance error of exactly the kind standards §2 exists to prevent.**

**The comparative result, stated with its hedge.** "*At the involuntary glance, the two are comparable.*" (`m-glance.md §8` L303) — entviz and SSH randomart both in the low-to-mid teens of bits. The paper reports "the first habituated figure for any randomart" (`m-glance.md §abstract` L16) and immediately bounds it: "Every perceptual tolerance here is modeled, not measured on people" (same line). The published ~22-bit randomart figure is "a whole-image, careful-regime number, not this one" (`m-glance.md §8` L304–L305) and cannot be read as evidence randomart is stronger at a glance.

### 11.4 `crna.md` erratum — what it is and, more usefully, what it is not

`crna.md` went 1.0 → 1.1 in this window (`57843b6`), gaining a closing paragraph: "*Added August 2026.* The three techniques above were sketches, and I have since worked out what it takes to build one of them." pointing to *Building Active Discovery*, and closing "The result depends less on new invention than I expected and more on governance — which is the argument of this paper, arriving somewhere I did not anticipate when I wrote it." (`crna.md §Conclusion` L133).

**It corrects no published claim.** The commit that added it describes a retraction — of the no-aggregator claim — but that retraction lives in `active-discovery.md` (§11.2 above), not in `crna.md`, and the crna paragraph does not mention it. The commit message is not the source, so the note records the erratum as what the file says: a forward pointer plus a self-assessment that the problem turned out to be governance-shaped rather than invention-shaped. The corpus repeats no crna claim, so nothing needed correcting.

---

## 12. Open questions, unresolved tensions, and drift flags

### 12.1 Comparative claims whose *external* half may have moved (unverifiable from this repo)

Every claim below was verified as *still said by the paper* at `181569b64`. What cannot be checked from the papers repo is whether the thing being compared to still behaves that way. Each is flagged rather than guessed at.

- **SD-JWT's standards status.** `sdjwt-acdc.md §2.7` L82 says SD-JWTs "are not standards yet, but they do have sponsoring workgroups, and they are likely to become public standards-oriented RFCs at some point in the future." The paper has not been revised since. If SD-JWT has since been published as an RFC, several downstream framings in §4.3 — immaturity, registry dependence, the IANA schema path — are arguing against a moving target. **Highest-priority external check.**
- **W3C VC Data Model version.** `acdc-vc-diff.md` argues six losses against "W3C VCs" without naming a version, and its Loss 2 ("W3C VCs are generally verifiable only in the present", L45) and Loss 6 (`@context` link rot, L99) are the two most version-sensitive. If VCDM 2.0's validity-period and securing-mechanism work changes either, the loss survives only in the form the paper's own text supports.
- **DID Core version.** `was.md §Mitigation 3` L60 links `versionId`/`versionTime` to `https://www.w3.org/TR/did-1.1/#did-parameters`. The *claim* ("most DIDs, including crowd favorites like did:web, can only be resolved to the current key state") is a survey assertion about the DID method landscape, and the landscape is exactly the sort of thing that drifts. It remains the author's assessment, not a counted result, and should be cited as one.
- **CA/Browser Forum 47-day schedule.** `x509-prob.md §Lifespans don't match` L33 and `wtbo.md §1` L36 both cite the 2025 ballot reducing TLS lifetimes to 47 days by 2029. A revised ballot would move the number the argument leans on.
- **The ENISA catalogue and EU Regulation 2026/1731** (the claim lives in `raw/05`; flagged here because it is the most drift-exposed comparative claim in the source set). `wtbo.md §6` L147 is explicitly about a document that changes without notice — the paper's own argument is that "When the file at that URL changes, the obligation changes." The draft third version was "in public review through July 2026", a window that has closed as of this pin. Whether v3 was adopted, and in what form, is unknown from here and directly affects the paragraph's force. This is the one claim in the source set *designed* to go stale.
- **GSMA Open Verifiable Calling.** `wtbo.md §5` L135 records the October 2025 launch with "twenty companies"; `acdc-and-mtc.md §7.1` L184 records the project as ongoing. Participation counts drift.

### 12.2 Standing gaps in this note

- **Line hints are absent for most of §§1–7** (see the header). Closing that gap is mechanical but was not attempted wholesale this pass; §8 and the inline additions cover the load-bearing subset.
- **Watcher-network taxonomy** (juror, judge) is still not covered by this corpus — carried forward from the previous pass. `wtbo.md §4` L109 adds the deployment distinction (in-process buffer vs. shared remote service, plus an archival "super watcher" variant) but not the taxonomy.
- **EGF** is still referenced via GLEIF's vLEI EGF without being defined anywhere in this corpus.

### 12.3 Unresolved tensions

1. **Decentralization-by-absence vs. decentralization-by-split.** §11.2. The author has retracted, for discovery among strangers, the claim that a design can leave no aggregator at all, and replaced it with a split-knowledge invariant that depends on governance. §9's purity framing should not be read as asserting absence is attainable generally. Unresolved: whether the same structural argument bites anywhere else the corpus claims observer-independence — the note's §2.5 "open-loop verification" claim in particular rests on a stranger verifying *from artifacts he already holds*, which is a different situation from discovering a stranger, but nobody has written down where the line falls.
2. **The human verification step is the weak one.** §11.3 against §3. `oia.md` L86 makes the unautomated human judgement the load-bearing final step and L70 offers eyeball comparison of an entviz as the way to clear a `0` flag. `amp-diff.md` L324, revised in this window, says casual eyeball comparison "is broken" against an adversary who has ground offline, and that the seeded commit-and-reveal walk is then obligatory. `oia.md` has not been revised to match, and still describes the pipeline as "the parties compare their identifiers over a trusted channel ... by eye". **These two papers now disagree about a procedure the corpus treats as doctrine.** The disagreement is one-sided in time (the newer paper qualifies the older) and neither paper acknowledges it.
3. **An author's own confidence is not the corpus's.** Two of the three revisions mined this pass move a number *down* or a provenance claim *weaker* — the habituated-entropy estimate, the human-nonce entropy, the "independent expert review" description. That pattern is a reason to treat every quantitative comparative figure in these papers as the author's current best estimate, revisable, rather than as a settled result, and to prefer his hedges over his headlines when a chapter quotes him.
