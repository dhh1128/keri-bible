# Doctrine Mining: keri.one (the web)

**Source:** https://keri.one (homepage, /keri-resources/, /131-2/ About Samuel Smith, /keri-in-production-for-gleifs-vlei/, keynote archive pages)
**Mining date:** 2026-07-17
**Character of the site:** keri.one is a small WordPress site authored by Samuel M. Smith. Its **original doctrinal content is thin and concentrated on the homepage plus the About page**; the bulk of the site (`/keri-resources/`) is a **curated outbound-link directory** pointing to the very whitepapers, specs, presentations, and third-party explainers that a synthesis project will already have from primary sources. Treat this file as: (a) the homepage's compressed marketing-grade doctrine statements (useful as quotable, canonical one-liners in Sam Smith's own site voice), and (b) a **map of what keri.one considers canonical reading** (the resource directory), so a synthesizer can see the officially-blessed corpus and spot anything not yet covered.

---

## 1. What KERI fundamentally IS (homepage doctrine)

The homepage (https://keri.one/) is organized under the banner headings: *Welcome to KERI / Truly Decentralized Identity / Supports GDPR Compliance / Self-Certifying Identifiers / Scalability / Key Management Infrastructure / Open Apache2 / Best Practices / Security*.

Core canonical framing, verbatim where quoted:

- **The headline definition:** "Key Event Receipt Infrastructure (KERI) is the first truly fully decentralized identity system." (https://keri.one/ — Welcome to KERI). Note the emphatic "truly fully" — the site's rhetorical posture is that other systems calling themselves decentralized are *not*.
- **Root of trust:** KERI provides a "decentralized secure root-of-trust based on cryptographic self-certifying identifiers." (homepage — Self-Certifying Identifiers). The root of trust is the **key(pair) itself / self-certifying identifier**, not any external authority, registry, CA, or ledger.
- **Ledger-independence, stated as a dual property:** KERI is "Ledger-less which means it doesn't need to use a ledger at all or ledger-portable which means that its identifiers are not locked to any given ledger." (homepage). Doctrine: KERI does **not** require a distributed ledger / blockchain / global consensus; where a ledger is used it must be non-locking.
- **Portability:** "KERI identifiers are truly portable." (homepage — Truly Decentralized Identity). Identifiers are not bound to any host, ledger, or provider.
- **Separable control over shared data:** "each person or entity truly controls their own identifiers" — "Separable control over shared data." (homepage). Control is separable from the data and from any infrastructure operator.
- **Non-intertwined trust bases (privacy/erasure):** "Non-intertwined identifier trust bases which means that a given identifier's data may be erased and truly forgotten." (homepage — Supports GDPR Compliance). This is the **GDPR / right-to-be-forgotten** doctrinal hook: because trust bases are not entangled (unlike a shared immutable ledger), data associated with one identifier can be truly erased. Directly contrasts with blockchain's immutable-ledger problem for privacy law.

## 2. Ambient verifiability and Key Event Logs

- KERI uses "hash chained data structures called Key Event Logs that enable ambient cryptographic verifiability." (homepage — Self-Certifying Identifiers).
- **The ambient-verifiability slogan, verbatim:** "Any log may be verified anywhere at anytime by anybody." (homepage). This is a load-bearing doctrinal claim: verifiability is *ambient* (not gated by an issuer being online, a CA responding, an OCSP endpoint, or a ledger query) — anyone, anywhere, anytime can verify a KEL from the data alone.
- KELs are hash-chained (each event chains to the prior via digest), giving append-only, tamper-evident history without a global ledger.

## 3. Key management / pre-rotation (the "hard problem")

- KERI is a "Decentralized key management infrastructure based on key change events." (homepage — Key Management Infrastructure).
- **The core problem statement:** KERI "Solves the hard problem of key management, that is key rotation." (homepage). Doctrine: key *rotation*, not mere key generation/storage, is THE hard problem of PKI, and it is what KERI exists to solve.
- **Pre-rotation** is named as the "novel key rotation scheme." (homepage). (The site links out to the whitepaper for the mechanism.) From the ecosystem framing surfaced alongside: pre-rotation lets an entity "persistently maintain or regain control over an identifier in spite of the exposure-related weakening over time or even compromise of the current set of controlling (signing) keypairs" — control is re-established "by rotating to a one-time use set of unexposed but pre-committed rotation keypairs that then become the current signing keypairs." This is the **pre-rotation firewall**: the next keys are pre-committed (as a digest/hash) but never exposed until used, so compromise of current signing keys does not enable takeover.
- Supports "attestable key events and consensus based verification of key events." (homepage). Note "consensus" here means the witness Agreement Algorithm (KACE), NOT blockchain global consensus.
- Supports "delegated identifiers that support hierarchical key management infrastructure." (homepage — cooperative delegation enabling org hierarchies).
- **Post-quantum secure:** flatly asserted on the homepage ("Post-quantum secure"), with a dedicated linked paper "KERI's Strategy for Post Quantum Security." The PQ story rests on pre-rotation hiding next public keys behind hashes (only a digest is exposed until rotation), plus large-seed/strong-hash strategy.

## 4. Design-intent philosophy (the "secure your own keys" thesis)

- **The site's single most quotable philosophy statement, verbatim:** "Much easier to secure one's own keys well than to secure everyone else's internet computing infrastructure well." (homepage — Best Practices/Security). This is the KERI worldview in one line: the security burden should be **self-contained to the controller's own key custody**, not dependent on the security of the whole surrounding internet/CA/host infrastructure. It reframes the trust problem from "trust the infrastructure" to "trust (only) your own keys."
- **Reputation → identity motivation (About page, https://keri.one/131-2/):** Smith's founding insight, verbatim: "A reputation is meaningless without an underlying identity and an identity is valueless without a credible reputation." KERI was developed because "reputation systems require authentic, verifiable content sources" — i.e., to prevent "content spoofing, gamification, and hacking." So KERI's origin story is: **authentic provenance of content** is the prerequisite for any meaningful reputation, and that requires a cryptographic, spoofing-proof identity substrate.
- Smith bio: Ph.D. EE/CE, Brigham Young University (1991); 10 years full professor at Florida Atlantic University; 100+ peer-reviewed publications in machine learning, autonomous systems, automated reasoning, decentralized systems; Lindon, Utah. (About page.) Author of the KERI whitepaper (arXiv 1907.02143, first published July 2019).

## 5. Standards / licensing posture

- "Open Apache2" — permissively licensed open source. (homepage).
- "Project working toward IETF standardization." (homepage). (Also being developed under the ToIP ACDC Task Force; the resources page links "KERI Suite of Protocol Specifications Final.")
- Scalability is claimed as a first-class property: "Compatible with data intensive event streaming and event sourcing applications." (homepage — Scalability). KERI is positioned as an **event-sourcing / event-streaming** architecture, which is why CESR (Composable Event Streaming Representation) matters.

## 6. Real-world deployment doctrine (GLEIF vLEI)

From https://keri.one/keri-in-production-for-gleifs-vlei/ (Sam Smith, May 1, 2023):
- "The Global Legal Entity Identifier Foundation (GLEIF) is now using KERI and ACDCs in production for their vLEI (verifiable Legal Entity Identifier) credentials."
- Framed as "a global adoption vector for the underlying open source standards that are KERI and ACDC." Doctrine: GLEIF/vLEI is treated as the flagship production proof point and the on-ramp for standards adoption.
- vLEI use case cited: "digital signing and automated verification of corporate caller IDs."

## 7. What keri.one points to as CANONICAL reading (resource directory map)

This catalogs the officially-blessed corpus (https://keri.one/keri-resources/) so a synthesizer can (a) confirm coverage and (b) spot additive material. Grouped:

**Foundational Smith papers/decks (likely already in a specs/papers corpus — flag for dedup):**
- KERI White Paper (KERI_WP_2.x.web.pdf) and its slide deck (KERI_Overview).
- SPAC — "Secure Privacy Authenticity Confidentiality" (SPAC_Message.md) + SPAC_Overview deck.
- "KERI's Strategy for Post Quantum Security" (KeriStrategyPostQuantumSecurity.pdf).
- CESR_Overview deck; "CESR for First Years" (Google Slides).
- ACDC whitepaper (ACDC.web.pdf), ACDC_Overview deck ("ACDC for Wizards"), "ACDC for Muggles" slides, "CESR Proof Signatures and ACDC."
- "Universal Identifier Theory with KERI" (IdentifierTheory_web.pdf) — a foundational theory paper worth checking for additive worldview material.
- "Sustainable Privacy" (SustainablePrivacy.pdf) — privacy doctrine paper.
- "The Duplicity Game" (DuplicityGame_IIW_2020_A.pdf) — **directly relevant to duplicity-evident doctrine; check if covered.**
- "KERI for Muggles" (Smith & Drummond Reed, IIW #33) — the canonical gentle intro.
- Manning SSI Book Ch.10 "Key Management" (10-ssi-key-management.pdf).
- RWOT papers: "A DID for Everything" (RWOT VII), "Decentralized Autonomic Data (DAD) and the three R's of Key Management" (RWOT VI), "Quantum Secure DIDs" (RWOT X), "Decentralized Identity as a Meta-platform: How Cooperation Beats Aggregation" (RWOT IX), "Identity System Essentials," Open Reputation whitepapers.

**Daniel Hardman papers the site treats as canonical ACDC doctrine (dhh1128.github.io/papers) — high-value, likely ADDITIVE:**
- "Trust with KERI, X.509, and CT" (wtbo.html) — KERI vs X.509/Certificate-Transparency comparison.
- "Why Anchored Signatures?" (was.html).
- "Why x509 Certs are Problematic" (x509-prob.html) — **anti-pattern / PKI-critique doctrine.**
- "Comparing ACDC with SD-JWT" (sdjwt-acdc.html) — **directly the SD-JWT drift KERI people reject; anti-pattern gold.**
- "Verifiable Voice Protocol" (VVP draft).

**Third-party explainers keri.one blesses (potentially additive framing):**
- Finema "Hitchhiker's Guide to KERI" Parts 1–3 (Nuttawut Kongsuwan, medium.com/finema) — notably Part 2 subtitled "what exactly is KERI."
- "PKI is for machines and not humans — KERI" (medium, asecuritysite) — titled doctrine that **"KERI is for Humans."**
- Doc Searls (Harvard blog): "On KERI: A Way Not to Reveal More Personal Info Than You Need To" — data-minimization framing.
- Human Colossus Foundation: "Thinking of DID? KERI On."
- "SSI can do just fine, blockchain-less" (ksoeteman.nl) — **explicit anti-blockchain positioning.**
- Windley: "The Architecture of Identity Systems," "Provisional Authenticity & Functional Privacy."
- Podcast "E4: SSI vs Federation, with Steve Wilson" — **anti-federation positioning.**
- vLEIDA "Why We Like KERI"; Spherity "A More Performant Ledger for Trust Identities."
- KERISSE.org / WOT-terms — the WebOfTrust terminology glossary (authoritative definitions source).

**Adoption / governance (SEDI, vLEI, EGF):**
- "State Endorsed Digital Identity (SEDI)" — Utah privacy office PDF, Windley SEDI pieces, "SEDI and Data Loyalty" (Technometria). SEDI is an emerging doctrine term: state-*endorsed* (not state-issued/controlled) identity, preserving self-certifying control.
- GLEIF "Ecosystem Governance Framework for vLEI" (EGF) with ToIP — the canonical EGF example.
- vLEI.wiki, WebOfTrust/vLEI schemas & credentials repo.
- GSMA "Open Verifiable Calling," telecom/VVP, EBA Pillar-3 data hub, FSB cross-border payments — sectoral adoption vectors.

**Implementation:**
- Community & reference implementation: github.com/WebOfTrust (and WebOfTrust/keri).

---

## 8. Anti-patterns / outsider-tells the site's framing corrects

Although keri.one's own prose is terse, its rhetoric and its curated corpus stake out these KERI-correct reframings (each contrasts an outsider prior):

- **"Truly fully decentralized"** (homepage) — implicit tell that systems marketed as decentralized (blockchain DIDs, federated SSI) are, in KERI's view, not truly decentralized. Root of trust in self-certifying keys, not in a ledger, CA, or federation.
- **Ledger-less / blockchain-not-required** — KERI rejects the assumption that decentralized identity needs a blockchain/global consensus/global ordering ("Ledger-less... doesn't need to use a ledger at all"; blessed article "SSI can do just fine, blockchain-less"). Witness "consensus" (KACE) is local agreement among a controller's chosen witnesses, NOT global chain consensus.
- **GDPR / erasure vs immutable ledger** — "data may be erased and truly forgotten" (homepage) directly answers the immutable-ledger privacy problem; KERI's non-intertwined trust bases make erasure possible where a shared ledger cannot.
- **Secure-your-own-keys vs secure-the-whole-infrastructure** — "Much easier to secure one's own keys well than to secure everyone else's internet computing infrastructure well" reframes away from the PKI/CA trust-the-infrastructure model.
- **PKI's key-rotation gap** — KERI's whole pitch ("Solves the hard problem of key management, that is key rotation") frames rotation as the unsolved PKI problem; pre-rotation is the answer.
- **X.509 / CA critique** — blessed papers "Why x509 Certs are Problematic," "Trust with KERI, X.509, and CT," "PKI is for machines and not humans" carry the explicit anti-X.509/anti-CA doctrine.
- **SD-JWT / W3C-VC drift** — blessed paper "Comparing ACDC with SD-JWT" and the ACDC-vs-VC framing (ACDC as the KERI-native alternative to mainstream VC formats) mark the SD-JWT/VC drift KERI people reject.
- **Anti-federation** — blessed podcast "SSI vs Federation" positions KERI/SSI against OAuth/OIDC-style federation.
- **KERI is for humans, not just machines** — recurring blessed framing.

---

## 9. Terminology surfaced on-site (definitions to cross-check against primary specs)

- **KERI** = Key Event Receipt Infrastructure.
- **KEL** = Key Event Log — hash-chained data structure enabling ambient verifiability.
- **KERL** = Key Event Receipt Log (witnessed variant; used in indirect mode).
- **Self-certifying identifier / AID** (Autonomic Identifier) — identifier whose authority derives from its own keypair.
- **Pre-rotation** — pre-committed, one-time, unexposed next-key set (the rotation firewall).
- **KACE** — KERI's Agreement Algorithm for Control Establishment (witness consensus in indirect mode). (Surfaced via ecosystem search alongside site; site links whitepaper for detail.)
- **Direct mode** (one-to-one, controller signatures) vs **Indirect mode** (one-to-any, witnessed KERLs).
- **CESR** = Composable Event Streaming Representation (dual text/binary encoding).
- **ACDC** = Authentic Chained Data Container (KERI-native verifiable credential variant).
- **vLEI** = verifiable Legal Entity Identifier (GLEIF's KERI/ACDC production credential).
- **SEDI** = State Endorsed Digital Identity.
- **EGF** = Ecosystem Governance Framework (e.g., GLEIF/ToIP vLEI EGF).

---

## 10. Gaps / caveats

- keri.one hosts almost NO original long-form doctrine. Deep mechanism claims (KACE detail, witness thresholds, duplicity-evidence, watcher/juror/judge roles, TEL, IPEX, edge operators, EGF internals, SAID construction) are **not on the site itself** — they live in the linked whitepaper/specs/papers that a specs-and-papers pass will already cover.
- The homepage marketing copy is compressed and occasionally imprecise ("consensus based verification" could mislead a reader toward blockchain consensus; the actual meaning is witness-agreement KACE). Cross-check against primary specs before citing as mechanism.
- The keynote/news archive pages (e.g., the "New Conformist Innovation Summit" keynote) are **link/landing stubs** — the actual talk content (video/transcript) is not on-page and could not be extracted; would require fetching the YouTube keynote (youtu.be/8shbJbdXdis) or the "NonconformistKeynoteWeb20200702.pdf" slides.
- The site's most *additive* pointers not necessarily in a standard spec corpus: the **Daniel Hardman dhh1128 papers** (x509-prob, wtbo, was, sdjwt-acdc), **"Universal Identifier Theory,"** **"Sustainable Privacy,"** **"The Duplicity Game,"** and the **SEDI** materials — worth mining directly if not already covered.
- keri.one appears not to expose the identity.foundation/keri/docs "KERI made easy" and "Q-and-A" explainers in its directory; those are strong plain-language doctrine sources hosted elsewhere (DIF) and are NOT covered here.
