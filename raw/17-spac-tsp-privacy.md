# Doctrine Mining: Confidentiality, metadata privacy and secure channels — SPAC, ESSR, TSP, sustainable privacy, bulk-issuance privacy

Mining date: 2026-10-14. Role: mine-spac. This note is new; nothing in `raw/01`-`16` mined these sources.

Primary sources, all in `SmithSamuelM/Papers` at `master` @`b47f21597` (2026-08-11) unless stated. Each line gives the last commit that touched the file, which dates the content.

- `whitepapers/SPAC_Message.md`, "Secure Privacy, Authenticity, and Confidentiality (SPAC)", Version 0.5.3 (original draft 2023-03-25). Last substantive commit `cd2661f` (2025-06-11); last touch `b8cc11a` (2026-04-30, a one-character typo fix, TOD to TOA). The CESR appendix was added 2025-04-21 (`9d163d6`). Read in full.
- `whitepapers/TSP_CESR_Implementation.md`, undated, last touched `24db805` (2025-07-09). A near-duplicate of the SPAC paper's CESR appendix written for ToIP TSP, with VID open/closed modes. Read in full.
- `whitepapers/ACDCConfidentialDataManagement.md`, undated fragment, last touched `6fa71dd` (2026-01-16). Read in full.
- `whitepapers/SustainablePrivacy.pdf`, v1.2.8 2026/08/11 (original 2023/09/18), last touched `b47f215` (2026-08-11). Read in full.
- `presentations/SPAC_Overview.web.pdf`, title slide 2023/06/17, last touched `b4e21b8` (2023-11-17). 79 slides, read in full.
- `presentations/SPAC_Strawman.web.pdf`, title slide 2023/06/17, `db2d2ad` (2023-06-17). Same deck in an earlier order; diffed against the Overview line by line and found to add nothing (§0).
- `presentations/KERI_PAC_Theorem.pdf`, "version 2.60 2021/04/23", `f9cae65` (2022-04-08). 228 slides; slides 1-32 and 79-92 read in full, the KERI-tutorial middle skimmed by title.
- `presentations/TSPSlides20230308.web.pdf`, title slide still dated 2023/02/08, `6f0ab85` (2023-03-08). 97 slides, read in full. `presentations/TSPSlides20230208.web.pdf` (61 slides) diffed against it by slide title (§0).
- `presentations/SevenPrivacies.web.pdf`, undated, last touched `da3cde9` (2025-09-11). 53 slides, read in full.
- `presentations/SustainablePrivacySlides.pdf`, title slide 2023/06/17, `fdf420b` (2023-10-12). 101 slides; the lines not already present in the decks above were read.
- `presentations/BulkIssuancePrivacy.pdf` and `presentations/BulkIssuanceSynergyDataLoyalty.pdf`, both added `b8cc11a` (2026-04-30, commit message `added IIW presentations`), undated. Read in full (the second as a diff against the first).

Specification sources:

- ToIP `trustoverip/tswg-tsp-specification`, `main` @`5599b4556` (2026-09-30), `spec/spec.md`. Status line: "Experimental Implementor's Draft Rev 3 with Errata (September 30, 2026)". Authors Wenjing Chu and Samuel Smith. Fetched by shallow clone 2026-10-14 into the session scratchpad (not vendored). Sections 1-5, 7 (relationship forming, padding, key update), 8, 9 (envelope and payload encoding) and the Security and Privacy Considerations read in full; the test-vector appendix was not read.
- `trustoverip/kswg-cesr-specification` `main` @`bad6edd84` and `v1.1` @`65fd751`, local clone `~/code/me/kswg-cesr-specification`, grepped for the ESSR and TSP count codes and cipher codes only.

Implementation: `WebOfTrust/keripy` `upstream/main` @`927c0cb87` (2026-10-10), local clone `~/code/wot/keripy` (remote `upstream`; not fetched this session, so this is the tip as of the clone's last fetch). Files read: `src/keri/spac/payloading.py`, `src/keri/app/forwarding.py` (`StreamPoster`), the ESSR passages of `src/keri/peer/exchanging.py`, `src/keri/core/counting.py`, `src/keri/app/keeping.py` (`Manager.decrypt`).

Talks: KERI Conference 2026 caption text at `.ignored/conf26/text/` (CONF26-subtitles HEAD `006042d`): the SPAC & TSP talk read in full; the State of the KERI Suite talk, the Future of KERI talk, the Digital Identity Tradespace talk and the It's KERI or Surveillance talk grepped for SPAC, TSP, ESSR, tunnel and metadata passages and read around each hit; topic summaries `talks-A.md`-`talks-D.md` grepped for ESSR, TSP and SPAC.

Coverage-gap report that motivated this note: `.ignored/coverage-gaps-2026-10.md` §2.1.

---

## 0. Provenance and status — read before citing

Everything in the Papers repo is `[P]`: Sam's position, in his voice, at the pinned commit. Several of these papers say so about themselves. The SPAC paper opens its central claim with "In my opinion" (`SPAC_Message.md` §PAC Trilemma, L11). The PAC theorem is posited, not proved, and no paper here offers a proof.

The reach of each idea is different, and the differences are the most useful thing this note records.

- ESSR as a construction reached two specifications. The CESR spec carries the ESSR count codes `-E##` and `-Z##` on both `main` and `v1.1` `[N]` (§11). The ToIP TSP draft adopts ESSR by name, with a modification for HPKE-Base (§11). The draft is an experimental implementor's draft, so its `[N]` marks in this note mean present in the line ToIP is standardizing, and that line is explicitly experimental.
- SPAC's three-level nesting, routed mode, relationship forming and padding reached the ToIP TSP draft in recognizable form. The PAC trilemma, the three-party exploitation model, the covert/clandestine argument and the time-value-of-information argument did not reach any spec. The ACDC spec carries the three-party model and defers third-party protection to SPAC/TSP (`raw/03` §L1728, cited at `bible/06-governance-ecosystems-and-interop.md:73`).
- keripy implements one ESSR sender path and the SPAC payload-type primitive `[K]` (§12). It implements no hop routing, no relationship forming, no padding payload and no `/essr/req` receive handler.
- The conference captions are edited auto-captions. Per `raw/14` §0 and `standards.md` §2 they support status and intent only. Section 13 paraphrases them and never puts them in quotation marks.

Five source-handling facts bite.

1. The SPAC paper is a living document whose version string did not move. It still says 0.5.3 while the git log shows content changes through June 2025, including the whole CESR appendix. Cite it by commit, not by version.
2. The decks lag their file dates. `SPAC_Overview.web.pdf` and `SustainablePrivacySlides.pdf` both carry a 2023/06/17 title slide though their files were committed in November and October 2023. `TSPSlides20230308.web.pdf` carries a 2023/02/08 title slide.
3. The SPAC Strawman adds nothing. A line-level diff against the Overview found only cosmetic differences (one relationship label, one "(reprise)" slide title). The Overview is the version to cite.
4. The two TSP decks differ in substance. The 2023-02-08 deck is only the hourglass and spanning-layer argument. The 2023-03-08 deck inserts 43 slides in front of it: overlays, end-only viewability, the PAC theorem, the threat model and the risk ranking. So the privacy and confidentiality framing entered the TSP proposal between those two dates.
5. The PDF text extraction loses ligatures in three decks (`KERI_PAC_Theorem`, `SustainablePrivacySlides`, the two bulk-issuance decks). "confidential" extracts as "con dential". Quotes below avoid ligature words in those decks, or restore the ligature and say so. Hyphenated line breaks in `SustainablePrivacy.pdf` are rejoined in quotes; the self-check (M4) normalizes the same way.

---

## 1. The trade space: the PAC trilemma and its ordering

Sam's statement of the trilemma, as of the SPAC paper `[P]`:

> "One can have any two of the three (privacy, authenticity, confidentiality) at the highest level but not all three." (`SPAC_Message.md` §PAC Trilemma, L13)

The wording has moved, and the moves matter for anyone who cites it. The 2021 deck reads "A conversation may be two of the three, private, authentic, and con dential to the same degree, but not all three at the same degree." (`KERI_PAC_Theorem.pdf` slide 2; ligature lost in the source, so the bible should restore "confidential" and say so). That deck also carries "May exhibit any two at the highest level but not all three at the highest level" (slide 81, "Smith's Triangle"). The 2023 SPAC paper and Overview deck use "at the highest level" (`SPAC_Overview.web.pdf` slide 3). The 2025 Seven Privacies deck reverts to "to the same degree", now for an interaction rather than a conversation: "An interaction between two parties may be two of the three, private, authentic, and confidential to the same degree" (`SevenPrivacies.web.pdf` slide 8). The two phrasings are not equivalent: "highest level" bounds the corner of the space, "same degree" bounds any symmetric interior point. Nothing in the corpus reconciles them. Open question 1.

The ordering comes from ToIP, not from Sam, and Sam distinguishes priority from layering. The ToIP design goals indicate "one should start with high authenticity, then high confidentiality, and then as high as possible privacy" (`SPAC_Message.md` §PAC Trilemma, L17). Priority does not fix the order of layers in a message (L29, too long to quote whole). The quotable form is: "the ordering of the ToIP design goals ... may be different from the ordering of layers that employ these three in a given protocol" (L31). Sam says this distinction "is a source of much confusion in prior discussions" (L33).

Why privacy is last is argued as an asymmetry between two kinds of war `[P]`. "Authenticity and confidentiality are like a cold war." (§Cold War versus Hot War, L116). "In comparison, privacy is like a hot war." (L118). The cold war is winnable because "there need be no casualties in this cold war" (L116); the hot war is not, because "casualties are unavoidable" (L118). Hence: "In the hot war of privacy, we have to Pareto optimize protection mechanisms." (L128). The SPAC paper's subtitle states the design objective in one line: "The Best Privacy Possible Given the Strongest Authenticity and Confidentiality" (L3).

The PAC deck of 2021 adds the reasoning that makes the trilemma bite between authenticity and privacy. "Non-repudiation means any party to conversation can proof to any other party exactly what was said by whom." (`KERI_PAC_Theorem.pdf` slide 9). "Transitive value transfer will violate complete privacy." (same slide). It also gives the only formal definitions of strong and weak privacy in the corpus: strong privacy is "un-correlated interactions over unbounded time and space", weak privacy is "un-correlated interactions over bounded time and space" (slide 12, "De nition" ligature-damaged in the source; the quoted spans are clean). The weak definition is the seed of the later time-value argument (§7).

---

## 2. Vocabulary: privacy is not confidentiality

Sam's working definitions `[P]`, stable from the 2021 deck through the 2023 paper:

> "Privacy is primarily about control over the disclosure of who participated in the conversation (non-content meta-data = identifiers)." (`SPAC_Overview.web.pdf` slide 10)

> "Confidentiality is primarily about control over the disclosure of what (content data) was said in the conversation and to whom it was said (partitioning)." (same slide)

The paper puts the same split in a sentence: "privacy is about protecting the knowledge of who is a party to a given conversation" and confidentiality is "about protecting the knowledge of what was said in that conversation" (`SPAC_Message.md` §Privacy and Confidentiality, L78). The paper's version of the privacy definition adds that identifiers include "conversation (interaction) identifiers" (L48), which is what later makes interaction IDs a privacy problem (§6).

There are two definitions of privacy in play and Sam picks one for protocol design `[P]`. The ToIP definition is about the receiver honoring the sender's expectations; the surveillance definition is about the "correlatability of the publically viewable metadata included in the communication" (L57). "for the purposes of protocol design the definitions of confidentiality and privacy that are most suitable are the surveillance definitions" (L78). The legal footing is US Fourth Amendment doctrine, which Sam summarizes as "Relatively weak legal protection (subpoena) for identifiers" and "Relatively strong legal protection (warrant) for content" (L73, L75). Seven Privacies extends the legal history back through Katz (1967) and Entick (1765) (`SevenPrivacies.web.pdf` slides 9-11).

The three-party exploitation model frames everything else `[P]`. Privacy toward the third party "is protected if the 3rd party has no knowledge of the identifiers used by the 1st and 2nd parties" (`SPAC_Message.md` §Three-Party Exploitation Model, L142). "An intermediary may be considered a 1st, 2nd, or 3rd party depending on how and by whom it is trusted or not." (L140). The Sustainable Privacy paper widens first-party data on purpose: it "may or may not reference or be about the data subject" (`SustainablePrivacy.pdf` §1.1, p.1), and "any use of 1st party data by a 3rd party is, by definition, unpermissioned and therefore exploitative" (§1.1, p.2).

The vocabulary shifted toward the word confidential between 2023 and 2026, and that shift is the newest doctrine in this section `[P]`. The January 2026 fragment says of shared data that "the difference is in name only" between private and confidential (`ACDCConfidentialDataManagement.md` opening paragraph). It explains why the word matters: the word privacy "carries an emotional bonus compared to" the word confidentiality (second paragraph). And it draws the hard conclusion: "once shared, there is no technology that by itself protects the first party's interests" (§Three-Party Model). The Seven Privacies deck turns this into a taxonomy: "Information that is not-shared = private (one party data)" and "Information that is shared with restrictions = confidential" (`SevenPrivacies.web.pdf` slide 13). Its "Combinations" slide (slide 15) lists exactly seven states, from "not shared" through "shared cryptographically un-linkable but re-identifiable" to "private (not shared, not surveilled, and not identified)". Reading that list as the seven privacies of the deck's title is this note's inference; the deck does not number them. The deck's charge is equivocation: "Using privacy as a sledgehammer to imbue technology with the emotion of privacy but without the actual qualities of privacy" (slide 7).

---

## 3. Effective privacy: protect against exploitation, not correlation

This is the move that makes the rest of SPAC tractable `[P]`:

> "Protection against exploitation via correlation provides a more gentle trade space than mere protection against correlation." (`SPAC_Message.md` §Effective Privacy, L103)

"The former is practical and amenable to cost-benefit analysis, but the latter is largely impractical." (same paragraph). The target becomes "exploitably correlatable identifiers" and the goal "effective privacy" (L101). Without the qualifier, any design loses to a sufficiently resourced adversary: "One can always play the equivalent of a trump card" (L122).

Exploiters are ranked by incentive `[P]`. State actors are out of scope "for the time being" because "to attempt state-actor proof mitigations would likely take us down rabbit holes that we can never return from" (§Exploiters, L155). Identity thieves monetize through asset theft and "do not monetize aggregated content data or metadata" (§Identity Theft, L177). Aggregators sell to advertisers and come in third-party (search, cloud, ISP), second-party (platforms) and inadvertent first-party (cookies) forms (L160-169).

The risk ranking that follows is the doctrinal punchline and it inverts the usual privacy-first ordering `[P]`. "Identity theft has very high harm magnitude with moderate likelihood but potentially low cost of mitigation via strong authentication and strong confidentiality" (`SPAC_Overview.web.pdf` slide 62). "The internet is broken primarily because of identity theft." (same slide). "The infrastructure changes needed to fix identity theft will enable easier adoption of the changes needed to better protect against aggregators." (same slide). The TSP deck adds that ToIP's TSP "can take mantle of teaching and leading in best practices for securing trust over the internet" (`TSPSlides20230308.web.pdf` slide 35).

The privilege-escalation argument places identity theft in authentication, not privacy: BOLA and BUA "are not privacy weaknesses but authentication-based authorization weaknesses" (`SPAC_Message.md` §Threats, L179). "a given trust domain is only as strong as the weakest connected trust domain" (L185). The mitigation: "any step that has strong authentication with individually signed requests for authorization will stop the attack from proceeding" (§Mitigations, L195). This connects to `bible/09` (KRAM) and to `bible/07`'s bearer-token row.

Where SPAC fits in that ranking `[P]`: "the most fruitful application of SPAC-based protocols with regards to exploitably correlatable identifiers may be in improving VPNs" (§Summary Threats and Mitigations, L256), while "protection from 2nd party aggregators may be best provided by higher layer protocols that provide contractually protected disclosure" (same paragraph). Sam also writes, of WireGuard, "We should not reinvent that wheel." (L109). The SPAC paper goes on to design intermediated routing anyway (§6), so the VPN remark should be read as an endorsement of the delivery-van model, not as advice to use a VPN and stop there.

---

## 4. The cryptographic baseline: ESSR

### 4.1 Building blocks

The baseline is chosen for adoptability: "only highly adoptable, well-proven, cryptographic operations from broadly supported libraries be used" (`SPAC_Message.md` §Adoptability via Dumb Crypto, L323). In this paper "we only consider pre-quantum safe algorithms" (L327). For signing, "the baseline for strong authenticity is to use the libsodium Ed25519 signature scheme" (§Best Authenticity, L343), because it has SUF-CMA where "the popular ECDSA signature scheme only has the weaker EUF-CMA" (L331). For encryption, the baseline is the libsodium sealed box, an IND-CCA2 ECIES with "the end-only viewability of asymmetric public key encryption" (§Best Confidentiality, L351). The sealed box "has equivalent properties to RFC-9180 base mode" (L356). All of this is `[P]`; the claims about ECDSA, Ed25519 and sealed-box security are relayed from the cited literature, which this note did not read.

### 4.2 Why HPKE alone is not enough

> "IND-CCA2, by itself, is insufficient to provide strong authenticity of the ciphertext." (§Best Confidentiality, L361)

Sam relays RFC 9180 §9.1.1: all HPKE variants are "vulnerable to key-compromise impersonation attacks" (L361), and the RFC's own remedy is "using a digital signature generated with the sender's private key over the HPKE container" (L361). The SPAC deck states the conclusion as a slide title: "HPKE is not Authenticity" (`SPAC_Overview.web.pdf` slide 23).

### 4.3 ESSR and the four unforgeability properties

Encrypt-then-sign is not enough either: "An attacker can strip the signature and resign the ciphertext with the attacker's key but has never seen the plaintext of the cipher." (§Best Combined Authenticity and Confidentiality, L366). The fix binds both ends: "we must not only bind the recipient's public key to the signature in plaintext but also bind the sender's public key inside the ciphertext" (L366). That construction is ESSR, "Encrypt Sender's key and then Sign Receiver's key" (§Modified ESSR, L370), from An, ePrint 2001/079.

The property table (L378-381) is the citation to carry: encrypt-then-sign provides TUF-PTXT, TUF-CTXT and RUF-CTXT; ESSR provides all four. In words: "Simply using the encrypt then sign approach provides TUF-PTXT, TUF-CTXT, and RUF-CTXT but not RUF-PTXT." (L372). The claim is Sam's reading of An's paper `[P]`; the ToIP TSP spec states the same result independently and more carefully (§11.3).

The strongest form of the claim, and the one most likely to be challenged, is in the "too clever by half" appendix `[P]`:

> "The ESSR framework basically tells us that there is really only one secure approach to mixing encryption with signatures." (§Appendix: Using Crypto in a way that is Too-Clever-By-Half, L1165)

This is Sam's assessment, not a surveyed result. An's paper analyses the generic compositions; "only one secure approach" goes beyond that. The bible should state it as Sam's position and pair it with the ToIP spec's narrower statement that the naive compositions "each fail at least one of these notions" (TSP spec §Cryptographic Algorithms, L957).

### 4.4 KERI's modification: AIDs instead of keys

"We apply ESSR to KERI by modifying the basic ESSR approach to support unbounded-term identifiers by replacing the sender's long-term public key with its AID" (§Baseline KERI ESSR, L388). The motivation is in the unbounded-term section: a long-term public key "is only long-term not unbounded-term" (§Unbounded-Term AIDs, L266, where "only" is italicized in the source) and NIST cryptoperiods force abandonment after one to two years. With an AID, stale-key use becomes detectable: "If the provided message is using stale keys for a given AID the associated cryptographic operations will fail against the current key state" (L274). The encryption key need not be managed separately: "with certain caveats, the encrypting public key may be cryptographically derived from the signing public key" (L272). keripy does exactly this (§12).

The AID substitution has a cost the SPAC paper does not discuss and the ToIP spec does: the signature binds the receiver's identifier, but the identifier's key state can change. The ToIP spec says TSP "provides no means to establish which key state was current when a signature was made" (TSP spec §Binding of identifiers, L1480) and argues receiver unforgeability survives anyway because the two bindings compose (L1482). That argument is the spec's, not Sam's paper's.

### 4.5 Variants and what each gives up

The paper treats every departure from full ESSR as an explicit trade `[P]`. "Any variation from the full ESSR policy may make a security trade-off induced by removing one of its protections." (§KERI ESSR Summary, L435).

- Plaintext-sourceless. Dropping the plaintext sender AID trades DDoS protection and public verifiability for privacy: "DDOS or firewall protection (security) could be traded for not exposing the sender's AID (privacy) without compromising the authenticity or confidentiality of the message" (§Plaintext Sourceless Variant, L401). With a one-relationship-identifier policy (OORI), "a given receiver AID, is only used for one given sender AID" (L407), and public verifiability can be restored by sharing the mapping upstream.
- Sourceless. Removing the sender from the ciphertext too, even under OORI, "still exposes the receiver to an attack when the approved sender is malicious" (§Sourceless Variant, L411).
- Destinationless. Possible because "an attacker can't purport any plaintext to have been encrypted to a different key pair other than the one that appears in the receiver's KEL" (§Destinationless Variant, L421). The argument rests on a birthday-style analysis Sam sketches but does not complete: a malicious receiver "may not gain any appreciable advantage" (L423). This is the weakest-supported claim in the ESSR section and the bible should flag it as unproven.

Replay is left open in the base construction. The simple mechanism is to "adopt a policy that once the key state has been updated no messages signed with stale keys may be accepted" (§Replay Attack Protection, L431). The stronger alternative anchors a digest of the message in the sender's KEL. Neither is KRAM; the 2026 talk points to KRAM for duplicate and replay detection (§13).

### 4.6 End-verifiability and end-only-viewability

The architectural principle predates SPAC and is restated here `[P]`: "If the edges (ends) are secure, then the security of the middle doesn't matter." (§End-Verifiabilty and End-Only-Viewability, L282). The confidentiality dual of ambient verifiability is "end-only viewability", under which confidential data "is only viewable one-where, one-time by one-other-body" (L297). The authenticity overlay must underpin the confidentiality overlay, not merely sit beside it: "the encryption key state must be securely attributable to the intended identifier for confidentiality to work" (`TSPSlides20230308.web.pdf` slide 15; also `SPAC_Overview.web.pdf` slide 73).

The paper lists six properties of strong end-only-viewable confidentiality (L313-318). The one with no counterpart elsewhere in the corpus is 1st-party non-viewability. Public-key encryption lets the encryptor delete the plaintext and keep only ciphertext it cannot read: "This is the zero-trust principle of encrypted-at-rest, not merely encrypted-in-motion." (§Appendix: 1st Party Non-Viewability, L1175). Applied to a distributed first party, "it can enforce on itself a policy of end-part-only viewability by using PKE" (L1177).

### 4.7 DDoS efficiency as a design constraint

The appendix makes DDoS cost a first-class constraint on how encryption and signatures may nest `[P]`. "Any protocol that requires decryption in order to make a drop decision can only make that drop decision at the edge host" (§DDOS Protection Efficiency, L1135). Nesting multiplies the cost: "So multiplying nesting layers directly impacts DDOS efficiency." (L1133). The conclusion favors signatures in plaintext: "if no decrypt must be done in order to drop (as in at end-only-viewability) then we can have very efficient DDOS protection" (L1137). The same appendix argues mix networks lower DDoS efficiency and are open to sleeper attacks (§Security-by-obscurity, L1145), and gives JSON-LD URDNA-2015 as an amplification-attack example (§Amplification Attacks, L1152). The JSON-LD claim is Sam's; the bible already has adjacent material in chapter 07.

---

## 5. Relationships, contexts and partitions

This section contains the formal core of the SPAC privacy model `[P]`, given as a list of properties (`SPAC_Message.md` §Relationships, L471-485; identical text on `SPAC_Overview.web.pdf` slide 31).

- "A cryptonym is a cryptographically derived pseudonym with at least 128 bits of entropy in the derivation." (L471)
- "A relationship is a pairing of two AIDs, one each from a different controller." (L473)
- "A context is a set of events." (L475)
- "A partition is a set of contexts with mutually disjoint relationships." (L478)
- "Any set of relationships using ORIs (One Relationship Identifiers) may form a partition." (L479)
- The limit is stated: two contexts in a partition "may be correlatable due to other information associated with any pair of contexts" (L480).
- Within a context, correlation is wanted: "The secure attributability of an AID, together with its perfect correlatability within a context, enables secure reputational trust" (L482).
- And the balance: partitions trade "strong authenticity and strong confidentiality within a context" against "sufficiently strong privacy between contexts" (L484-485).

The doctrinal consequence is that the identifier is not the correlator; the context is. The paper states the information-theoretic half: "Two different AIDs are by themselves uncorrelated in an information-theoretic security sense" (L474). The 2026 talk states the other half as a slogan (§13); it has no written source in the corpus, so the bible can cite the paper for the property and the talk only for emphasis.

Relationship direction matters. A relationship may be bidirectional or one-way, and "for any two AIDs there are three different relationships" (L442). One-way relationships let A-to-B and B-to-A traffic use different routes, which the paper later exploits (L863).

Every protocol needs at least one out-of-band authentication factor `[P]`. Any secure protocol "requires at least one out-of-band-authentication (OOBA) factor in order to protect against a man-in-the-middle (MITM) attack" (§OOB Setup, L573). The same factor answers cheap pseudonymity: "Requiring an OOBA factor for any given identifier makes that identifier relatively expensive." (L577). And it need not cost privacy: "an OOBA (out-of-band-authentication) may be simultaneously strongly authentic, confidential, and private" (L579). This is the SPAC paper's version of `bible/07`'s OOBA material and agrees with it: OOBA raises the cost of a fresh identifier; it does not create a binding.

---

## 6. The protocols: from direct to triple-nested

The paper builds the protocol in five steps `[P]`. Each deck slide ends with a one-line verdict, and the verdicts are the summary.

1. Direct. ESSR between `A0` and `B0` with IP addresses in clear. "Strongly Authentic and Confidential but not Private" (`SPAC_Overview.web.pdf` slide 36).
2. Direct protocol as wrapper. A business-deal relationship `(A1, <>, B1)` is carried inside the ciphertext of the communication relationship `(A0, <>, B0)`. "No 3rd party observer can view that there is a relationship" (`SPAC_Message.md` §Direct Protocol as Wrapper, L630). Verdict: "Strongly Authentic and Confidential and Somewhat Private" (slide 37). The paper names the two kinds of context here: a hop-wise communication context and an end-wise interaction context (L632).
3. Relationship formation. An existing relationship acts as "a 3rd party reference or reputable letter of introduction" for a new one (§Relationship Formation Protocol, L637). Sam calls this an OOBI in a sense wider than KERI's discovery OOBI: "We call this an Out-Of-Band-Introduction (OOBI) because the reputable relationship authentication was established Out-Of-Band with respect to the new relationship." (L651). The bible should note the overload: KERI's OOBI is a discovery URL with no trust; this OOBI is a reputable introduction.
4. One shared intermediary `C`. Third parties see only `A` talking to `C` and `B` talking to `C`; `C` sees `(A1, B1)` but never the content, and "The AIDS in (A1, <>, B1) are never stored on disk by C. They are only ever in memory." (`SPAC_Overview.web.pdf` slide 41). Verdict: "Strongly Authentic and Confidential and Mostly Private" (slide 40). The listed limits: both parties must trust `C`, and `C`'s ISP can correlate timing and size (`SPAC_Message.md` L705-707).
5. Non-shared intermediaries `C` and `D`, one trusted by each end. Verdict: "Strongly Authentic and Confidential and Very Private" (slide 42). Neither end needs to know the other end's intermediary relationship, so "An attacker has to get that by successfully attacking both C and D." (`SPAC_Message.md` §Discussion, L792). The routing tables are signed at rest, so "This approach is fully zero-trust" (L796). The paper's conclusion: "we can have secure authenticity, confidentiality, and privacy (identifier correlation), as well as DDOS protection" (L800).

The final step nests a third relationship `(A3, <>, B3)` inside the end-wise routed one, so that even the intermediaries cannot see it. "This makes the existence of this new end-wise relationship (A3, <>, B3) hidden from not just 3rd parties but also the 2nd party trusted intermediaries." (§Cross Relationship Context Interaction Contexts, L865, with the italics markers of the source dropped). The paper names the result "a three-level nested communication protocol" (L873) and walks it hop by hop in a shorthand notation (§Shorthand Notation, §Three-Level Nested Protocol, L877-1041). The deck verdict for this case drops the qualifier: "Strongly Authentic and Confidential and Private" (slide 44).

Routing splits into two halves that no single party holds `[P]`. "The non-shared intermediary protocols above use a combination of both source vector routing and table routing." (§Combined Source Vector and Table Routing as Dead Drop, L1045). The far-side intermediary becomes "a dead drop controlled by the far-side destination" (L1049).

Interaction identifiers get the same treatment as AIDs. Using the SAID of a nonce-salted first message as the interaction ID makes it "cryptographically universally unique to a given interaction" (§iSAIDs as IIDs, L813), and putting it inside the ciphertext makes interactions private: "if the relationship context is private, then any of its interaction contexts are also private (QED)" (§Privacy by Isolating Interaction Contexts, L827). Chained iSAIDs are preferred over a repeated one: "the latter form is more secure" (L832).

Multisig is sketched, not specified. For encryption "each key in a multi-sig provides a unique encryption destination" and the ciphertext "must appear as a list of ciphertexts" (§Multi-sig Extension, L1057). keripy does not do this (§12).

---

## 7. Sustainable privacy

### 7.1 The time value of information

Sam's answer to the objection that everything leaks eventually is economic, not cryptographic `[P]`. "In general, privacy dissipates over time." (`SPAC_Message.md` §Time Value of Information, L1064). But the value of correlated information decays too, so there is "a sweet spot for sustainable privacy protection that is governed by the time constant of the time value of exploitable correlation" (L1066). Partitioned contexts make that time constant controllable: "Once a context has become leaky, however, a new isolated context can be created that restarts the clock on time value correlatability." (L1068). The 2026 Sustainable Privacy paper names TSP as the protocol that does this: "The TSP protocol enables control over the exploitable time window of the correlatable information that can be leaked from a given context." (`SustainablePrivacy.pdf` §3.3, p.9).

The decision rule is symmetric `[P]`: "If the cost of protection exceeds the cost due to the harm of exploitation, then it's not worth protecting" and "If the cost of correlation in order to exploit exceeds the time value return of exploitation, then it's not worth exploiting" (`SPAC_Message.md` L1066). No paper estimates either time constant for any real market. The argument is qualitative. Open question 3.

### 7.2 Covert versus clandestine

This is the analogy Sam leans on most in 2026, and it originates in the SPAC paper `[P]`. A covert operative has a public cover identity; a clandestine operative has none. "As a result, a given clandestine operation is unsustainable long-term." (§Sustainable Management of Contexts, L1084). Internet privacy tools "have tended to look like clandestine operations where the whole operation must be concealed" (L1086), which makes them fragile. The prescription is to nest: The long-term generic communication and routed contexts are the covert layers, and they "provide nested covers to the really valuable private short-term interaction contexts (clandestine)" (L1088). The deck compresses it to "Use Covert to hide in plain sight." and "Nest clandestine contexts inside covert contexts" (`SPAC_Overview.web.pdf` slide 51).

The covert model has a herd requirement that is easy to miss. If most of an intermediary's users use it only for things they want hidden, "they make the mere use of C itself a correlatable signal" (`SPAC_Message.md` L1086). A covert intermediary is only as good as its legitimate traffic.

### 7.3 Re-identification and the contextual linkability attack

The SPAC paper introduced, and Sustainable Privacy develops, a named attack on selective disclosure `[P]`:

> "the use of a set of non-selectively disclosed attributes obtained from the context of the disclosure that is sufficient to re-identify the discloser" (`SPAC_Message.md` §Contextual Linkability Re-identification Attack, L1101)

Sam frames selective disclosure as self-administered k-anonymity: "Correctly understood, selective disclosure is a naive form of K-anonymity performed by the discloser (presenter)." (L1104). The act of presenting singles out the presenter, so "the receiver of bare, selectively disclosed data must treat it as personal data or may be in violation of GDPR" (L1104). The 2026 paper softens the legal half to a normative claim: selective disclosure "should not provide a safe harbor", and "Unfortunately, current regulatory policy does not respect this distinction." (`SustainablePrivacy.pdf` §2.3, p.5). That is a correction the bible should carry: the 2023 text reads as if GDPR already requires this, and the 2026 text says it does not yet.

The 2026 paper adds two arguments the 2023 paper lacks `[P]`.

- ZKP selective disclosure has a security cost, not just a weak privacy benefit. If the issuer's ZKP signing key is compromised, "This creates a largely undetectable impersonation attack on the issuer." (`SustainablePrivacy.pdf` §2.4, p.7). And the bounded cryptoperiod caps a bare ZKP credential's lifespan: "at most, a bare ZKP VC can be used only for applications with a VC lifespan of no more than two years" (§2.4, p.7). The bible already carries the detectability half from discussion #1098 (`bible/07-shibboleths-and-anti-patterns.md:388`, :499); the cryptoperiod half is new.
- Not all de-identification is broken. K-anonymity is, but "The only allowable de-identification approach is either a differential privacy or a synthetic data privacy-based mechanism." (§1.2, p.3). This applies to aggregated data from many first parties; for non-aggregated data the answer remains contractual (§3.1, p.8).

The 2025 Seven Privacies deck pushes the selective-disclosure critique to its sharpest form: "Therefore, counter-intuitively, selective disclosure increases the traceability of individuals" (`SevenPrivacies.web.pdf` slide 22), and providing unlinkability "is not a viable policy goal" (slide 23). Both are Sam's assessments. The first rests on the claim that every disclosure adds the act of disclosure to an aggregator's corpus; the deck does not quantify it.

### 7.4 Accountability as the remedy: chain-link confidentiality and data loyalty

The constructive half of sustainable privacy is legal `[P]`. "the only sustainable privacy protection mechanism for 1st-party data disclosed to a 2nd party" ... "is some form of contractually protected disclosure" (`SustainablePrivacy.pdf` §3.1, p.8). The SPAC paper's 2023 version of this sentence names only chain-link confidentiality (`SPAC_Message.md` L1110, where the sentence is printed twice, a duplication in the source); the 2026 version adds the duty of data loyalty.

Data loyalty is defined by reference to Hartzog and Richards: "The 2nd party data holder must act as a loyal agent of the 1st party." (`SustainablePrivacy.pdf` §4, p.10). Consent is not the mechanism, because "the act of consent can be easily socially engineered against the best interests of the consenter" (§4, p.10). The fiduciary framing reaches dark patterns: "Exploitation also includes using data for nudging and manipulation, or incorporating dark patterns into system design" (§4, p.10). The 2026 IIW deck quotes Hartzog and Richards directly, including "Data loyalty has three key features—it is a (1) relational duty (2) that prohibits self-dealing (3) at the expense of a trusting party." (`BulkIssuanceSynergyDataLoyalty.pdf` slide 2; a quotation of the law review article, not Sam's words). The same deck extends chain-link from confidentiality to loyalty via contractual privity (slide 3).

Accountability, not hiding, is the 2026 thesis. "Any interaction system that does not enable" first parties "to hold second parties accountable is fundamentally incompatible with privacy" (`BulkIssuanceSynergyDataLoyalty.pdf` slide 24; the source breaks this across lines and the word first is ligature-damaged, so it is left outside the quotation). The Seven Privacies deck says the same from the other side: "Cryptographic un-linkability defeats legal, contractual, and economic accountability" (`SevenPrivacies.web.pdf` slide 26). This is consistent with `bible/06` §4 and sharper than it: §4 treats the contractual layer as one of three; Sam's 2026 position is that without it the other two cannot hold.

---

## 8. Bulk-issuance privacy (IIW, April 2026)

The two IIW decks are the newest material here and the least developed `[P]`. They connect bulk issuance to "Control over Context", which the talks call RAP-C3 (§13). The threats are named on slide 2 of `BulkIssuancePrivacy.pdf`: identity theft, attention theft, intimidation. The mitigations on slide 3 include "Control over Context".

What is new relative to the ACDC spec's bulk-issuance section (mined in `raw/03`, summarized at `bible/05-acdc-and-verifiable-data.md:215`):

- Per-member derivation. "Each member of a bulk-issued set has a unique AID with unique keys derived using an HDKey algorithm" (`BulkIssuancePrivacy.pdf` slide 18). The UUIDs are derived from a path that "contains a shared secret salt, the member index, and the UUID index" (same slide).
- A shared blinded registry as an alternative to one registry per member: "a given Issuer could use one blinded state tel for multiple di erent ACDCs, thereby providing herd privacy across all issuances" (slide 18; "different" is ligature-damaged in the source). The second deck narrows it to ACDCs "issued to the same issuee" (`BulkIssuanceSynergyDataLoyalty.pdf` slide 11, same ligature caveat). Slide 13 of the first deck shows the shared registry with two ACDCs interleaved.
- Herd privacy via placeholder and random updates. "Placeholder updates provide herd privacy wrt correlation to date time of actual state changes" (`BulkIssuancePrivacy.pdf` slide 23). The issuer "could randomly issue update events that do not change state, across all its registries" (slide 21).
- An SMT predicate proof as an alternative to a ZKP for age. The comparison slide is explicit about the trade: ZKP has "relatively large computation, defeats detectability of issuer key compromise"; SMT has "relatively large storage, relatively small computation, enables detectability of issuer key compromise" (slide 31). The sizing is "Number of leaves: 100 years * 365 days = 36,500" (slide 31). This is the deck form of discussion #1098's proposal, which the bible already carries (`bible/05-acdc-and-verifiable-data.md:76`).
- An identity-assurance credential ahead of bulk issuance. "An in-person session that binds identity assurance to cryptographic identity" is labeled "NIST IAL3 Compliant" (slide 17), and "This enables dynamic sizing of SEDI bulk issuance sets" (same slide). The Tradespace talk adds that the in-person session is where the bulk-issuance salt can be exchanged out of band (§13).

None of this is in keripy beyond the blindable-state machinery the bible already records (`bible/05` §9). The `-a` and `-b` blinded-state count codes appear in keripy's codex next to the ESSR codes (`counting.py`:254-256 @`927c0cb87`), which is the only overlap.

---

## 9. Positioning against other approaches

These are Sam's comparisons `[P]` and should be cited as his.

- Onion and mix routing. The SPAC paper lists TOR and DIDComm routing as mitigations but says a decentralized overlay "is difficult to incentivize and as a result, may have relatively low adoptability when compared to a VPN" (`SPAC_Message.md` §Aggregation, L232). Sustainable Privacy adds that TOR is "vulnerable to timing attacks" (§2.3, p.5).
- DIDComm. "This seems to be the area where some of the patterns in DIDComm would benefit from being recast from an AID discovery or setup perspective." (§Relationship Discovery Protocols, L1118). That is the only constructive mention of DIDComm in the corpus.
- DNS/CA as a trust spanning layer. "DNS/CA is badly broken." (`TSPSlides20230308.web.pdf` slide 78). PGP's web of trust fails for lack of "in-band Key Rotation mechanism" (slide 79).
- Thick interoperability. Sam warns against thickening the spanning layer "in order to support everyone's preferred application as is" (slide 82). The cited cases are "DID method proliferation interoperability resulting in thick wallets" (same slide).

The hourglass argument is the TSP deck's reason for existing, and it reached the ToIP spec only as framing. "Minimally sufficient means (satisfies hourglass theorem's weakness property) for trust spanning layer is an identity (identifier) system security overlay." (slide 72). The ToIP spec says TSP "stands as the spanning layer protocol within the Trust over IP technology architecture" (TSP spec §Overview, L52) but does not carry the weakness argument.

---

## 10. The CESR wire format in the papers

Both `SPAC_Message.md` (§Appendix: CESR Implementation, L1183 onward) and `TSP_CESR_Implementation.md` specify the same wrapper `[P]`. SPAC is "a tunneling routing protocol that is meant to be transparent to any other message protocol that is tunneled as a payload" (L1187). Its native fields are fixed-field CESR; "all tunneled payload messages (i.e. non-native SPAC payloads) are encoded as sniffable CESR streams" (L1191).

The structure is head, body, tail. The head is plaintext and deliberately uniform: "This is by design so that the head contains no correlatable metadata besides the source and destination AIDs." (§Head, L1207). The wrapper count code is `-E##` or `--E#####`; the payload group is `-Z##` or `--Z#####`. The body is either ciphertext or a plaintext payload group, and a parser tells them apart by the first character: if it is `-` the payload is a plaintext group, otherwise a cipher primitive (§Determining if the payload field value is a ciphertext CESR primitive or a plaintext CESR group, L1549). Every control payload carries a pad field "to pad the total packet size to some desired minimum length" (§Padding Control Message Payloads, L1265), and a whole `PAD` payload type exists to "whiten the stream of packets by injecting pad packets" (§Pad Payload, L1485). Relationship formation needs no replay protection because "relationship formations are treated as idempotent actions" (§Replay Attack, L1436).

The payload types are `CTL`, `HOP`, `RFI`, `RFA`, `RFD`, `PAD`, `SCS` (L1246-1254). The KERI extension table maps every KERI and ACDC v2 message type into a SPAC payload type by prefixing `X`, using case to avoid collisions: "If we adopt the convention that native SPAC message types be uppercase then we make it easy to avoid collisions." (L1557).

The two papers diverge in ways the bible must not paper over.

- Identifier encoding. The TSP paper has open and closed modes: in open mode "all VIDs must be either URNs or DIDs encoded as variable-length CESR UTF-8 byte strings" (`TSP_CESR_Implementation.md` §VID fields in Open Mode). In closed mode a KERI AID is used bare. The SPAC paper removed the modes on 2025-04-21 (`702796a`, commit message `removed closed mode and open mode references`) and uses bare AIDs throughout.
- The version field. The SPAC paper uses a 10-character field with an explicit genus version, example `0OSPACAABCAA` (`SPAC_Message.md` L1226), added 2025-06-11 (`77cc6f7`). The TSP paper uses a 7-character field with an implied genus, `YTSP_AAB` (`TSP_CESR_Implementation.md` §TSP ESSR Wrapper), where "The CESR Genus table version is implied." The ToIP spec uses `YTSP-AAC` with a hyphen, version 0.2 (§11).
- The hop-list code. The SPAC paper's prose says "The hop list group code is `-K##`." (`SPAC_Message.md` §Hop Payload, L1377) while its own example tables use `-J##` (L1390), and `-K##` is the indexed-signature group code in the same tables. The TSP paper and the ToIP spec both use `-J##`. The SPAC prose is a defect in the source. Open question 5.
- Example drift. The SPAC paper's hop-payload examples still show version values `YSPACABA` and `YSPACAAB` (L1390, L1537), the pre-June 2025 form.

The `HOP` payload has a proposed variant, explicitly "for Discussion", that encrypts the inner message to the final destination rather than letting the last intermediary form it from a private table. The trade is stated as one of trust: "Between whom does one trust more?" (§Hop Payload Encrypted to Final Destination, L1398). The paper also proposes mitigating intermediary observation "by using ephemeral VIDs generated from a verifiable random process" (same paragraph). The ToIP spec settled differently (§11.4).

---

## 11. What reached a specification

### 11.1 CESR codes `[N]`

The CESR master table on both branches carries the wrapper code: "| `-E##` | ESSR wrapper signable up to 4,095 quadlets/triplets |" (`kswg-cesr-specification` `spec/spec-body.md` L842 @`main` `bad6edd84`; L850 @`v1.1` `65fd751`). The payload group is named for TSP: "ESSR (TSP) Payload `version+messagtype+...` up to 4,095 quadlets/triplets" (L939 @`main`; L947 @`v1.1`; "messagtype" sic). The X25519 sealed-box cipher codes `4C`-`9AAC` and HPKE-Base codes `4F`-`9AAF` are present (L1028-1050 @`main`). One drift: the CESR spec describes `4F` as "HPKE Base cipher bytes of QB2 plaintext" (L1046 @`main`), while both papers describe it as "HPKE Base cipher bytes of sniffable stream plaintext" (`SPAC_Message.md` L1316). Which one the TSP spec means is not stated; it refers to its codes only by prefix. Open question 6.

### 11.2 The ToIP TSP draft: status and shape `[N]`, experimental

Status, verbatim: "Experimental Implementor's Draft Rev 3 with Errata (September 30, 2026)" (`tswg-tsp-specification` `spec/spec.md` L4 @`5599b4556`). The version on the wire is 0.2: "The current experimental draft's version is `0.2`." (L245).

TSP defines the three properties per directional relationship and renames Sam's privacy "metadata privacy" to keep it separate from confidentiality: the protection "is termed metadata privacy, differentiating it from the narrower understanding of privacy" (§Authenticity, Confidentiality, and Metadata Privacy, L105; "metadata privacy" is italicized in the source). "TSP messages always assure authenticity, optionally confidentiality, and if utilized, metadata privacy." (L107). Metadata privacy comes from exactly the two SPAC mechanisms: "The metadata privacy protections are achieved by nested TSP messages and routed messages through intermediaries." (L107).

The SPAC formal properties survive almost word for word. VIDs must be "cryptographically non-correlatable in an information-theoretic security context" (§Cryptographic Non-Correlation, L152). Inner VIDs in nested relationships "do not require same level of verification as public VIDs, and do not require transport layer address resolution of their own" (§Nested Relationships, L418, italics markers of the source dropped).

### 11.3 ESSR in the spec, with an HPKE-Base modification

The spec adopts ESSR explicitly and argues for it more carefully than the SPAC paper: "No naive composition of public-key encryption and signature achieves authenticated encryption in the public-key setting." (§Cryptographic Algorithms, L957). It then makes two changes Sam's paper does not.

- HPKE-Base is mandatory; the sealed box is optional and on notice. "TSP implementations MUST support HPKE-Base mode as defined in this document." (L993). Of the sealed box: "implementors SHOULD consider migrating to the HPKE option specified in this document. We MAY remove this option in the future." (L1052). The SPAC paper's baseline was the sealed box, because RFC 9180 implementations were "not yet broadly available" (`SPAC_Message.md` L359). The spec reverses that baseline.
- Under HPKE-Base, the sender-in-ciphertext half of ESSR moves into the associated data. "the binding of the ciphertext to the sender identity required by the ESSR construction is provided by the associated data `aad`" (TSP spec §HPKE-Base Mode, L1010). The in-payload sender VID becomes optional: "In HPKE-Base mode the VID_sndr confidential field is NULL VID by default." (L1041). Under the sealed box it remains mandatory: "the `VID_sndr` field MUST be present in the Confidential Control Fields (as required by [[ref:ESSR]])" (L1102).

Whether AAD binding gives RUF-PTXT in An's sense is the spec's argument, not the paper's. The spec makes it in §Binding of identifiers (L1478-1482) and says that an implementation wary of relying on "the associated-data handling of a newer HPKE implementation obtains the same property from the payload check alone" (L1482). The bible should record this as a spec-level refinement of SPAC's ESSR, not as a contradiction.

Post-quantum entered the spec and is absent from the paper. The spec supports ML-DSA-65 signatures and an MLKEM768-X25519 hybrid KEM: "Post-quantum support in TSP is not a separate mode — it is HPKE-Base with the post-quantum/traditional hybrid KEM MLKEM768-X25519" (L1048). The SPAC paper deliberately considered "only ... pre-quantum safe algorithms" (§Adoptability via Dumb Crypto, L327).

### 11.4 Routing, nesting and relationship forming

Routed mode follows the SPAC non-shared-intermediary design. "A typical three hop pattern of TSP routed messages will traverse from source endpoint `A` to its intermediary `P`", then to the destination's intermediary `Q`, then to `B`. (§Metadata Privacy in Routed Mode, L464). Three relationship types are named: direct neighbor, endpoint-to-endpoint, and "Nested private endpoint-to-endpoint relationship" (L462). The last hop is identified by a VID the destination chose, so that "an intermediary cannot oblige its clients to re-establish their routing information with every correspondent" (L469). This is the spec's answer to the SPAC paper's open "for Discussion" variant: the final hop is a destination-chosen exit VID, not an encryption to the final destination.

Relationship forming became mandatory before application traffic, which SPAC did not require. "It is not permissible that one endpoint which has learned a VID of the other simply starts with an application level message" (§Direct Relationship Forming, L713). The most private response to an unwanted invitation is no response: "The most private option is to remain silent." (L733). The `TSP_RFI` carries a nonce and a SAID-style digest (L684-701), matching the paper's salty nonce and iSAID.

### 11.5 What the spec says TSP does not do

The spec is more candid than the papers about limits, and these sentences belong in the bible as stated `[N]`.

- No forward secrecy. "TSP does not provide forward secrecy: an adversary that has recorded earlier messages and later obtains the decryption key can read them." (§Limits, L1515).
- Metadata privacy is not cryptographic. "The properties that require no judgement about an operator are authenticity and confidentiality, which are cryptographic." Then: "Metadata privacy and availability in routed mode are not among them." (§What An Intermediary Is Trusted For, L1558).
- Timing and size survive everything. "Timing, size, and frequency survive encryption, nesting, and routing alike." (§What Remains Observable, L1527). "TSP itself does not batch, reorder, or delay messages to frustrate this" (same paragraph). This contrasts with the 2026 talk's intent that intermediaries keep uniform traffic (§13): in the spec that is an intermediary arrangement, not a protocol property.
- Intermediary non-retention is a promise. Not storing endpoint-to-endpoint VIDs "is not enforced by any mechanism in TSP; it is a commitment by the operator." (L1554). The SPAC paper's "only ever in memory" property (§6) is therefore, in the spec, an operator commitment.
- Freshness belongs above TSP. "An application requiring ordering, delivery, or freshness of its own obtains them from the layer that understands what its messages mean" (§Security and Privacy Considerations, L1473). For KERI that layer is KRAM (`bible/09`).
- A verified VID is not an identity. "A verified VID is an identifier that can be relied upon consistently, not an identity." (§Introductions, L1566).
- Rotation is the VID type's business. "Because the resolution and verification of key state is VID type specific, TSP does not define a rotation mechanism of its own." (§Handling Changes, L196). The spec does require of public VIDs what KERI provides natively: "The authority to rotate a VID's keys MUST be separate from the VID's signing key" (§VID General Requirements, L144). Its recovery-limits paragraph describes KERI's three defenses without naming KERI: pre-commitment to next keys, delegation, and first-seen with conflict treated as evidence (§Limits, L1511).

### 11.6 Where the spec departs from KERI usage

Identifier syntax is the sharpest friction. "we require that the VID format be either compliant DID format [[ref:DID]] or compliant URN format [[ref:RFC8141]]" (§VID Syntax, L158). Yet the same spec's example list says of a KERI AID: "An AID is not a DID; it is used directly" (§Examples, L206). Read together, a bare AID in an envelope would violate §VID Syntax unless it is carried as a URN or as `did:webs`. Sam's TSP CESR paper anticipated this with its closed mode; the spec has no closed mode. Open question 4.

---

## 12. What reached keripy `[K]` @`927c0cb87`

keripy has a `keri.spac` package containing one primitive, the payload-type tag: `PayloadTypes = PayloadTypage(HOP='HOP', RFI='RFI', RFA='RFA', RFD='RFD', SCS='SCS')` (`src/keri/spac/payloading.py`:15). It omits `CTL` and `PAD`, which both papers and the ToIP spec define. It was added by Fergal O'Connor in `a6e12a74b` (2025-09-02, commit message `feat: SPAC message types and optionally encrypted StreamPoster (#1068)`).

The same commit added an ESSR send path to `StreamPoster` (`src/keri/app/forwarding.py`:270). When `essr=True` the plaintext is a SPAC `SCS` payload: the payload-type tag, the sender's AID, and an empty pad (`forwarding.py`:314-318). The source comment on the pad reads `# bext field can be randomized to reduce correlation based on packet size, empty for now` (:317). So the pad slot exists and is never filled.

`_essrWrapper` (`forwarding.py`:408-430) does the ESSR:

- It derives the receiver's X25519 key from the receiver's first signing key, `verfer = rkever.verfers[0]` (:414) and `pubkey = pysodium.crypto_sign_pk_to_box_pk(verfer.raw)` (:416), as the SPAC paper permits ("derived from the signing public key", §4.4).
- It seals the plaintext with the libsodium sealed box, `raw = pysodium.crypto_box_seal(bytes(msg), pubkey)` (:417).
- It signs an outer `exn` on route `/essr/req` whose modifiers name both ends, `modifiers=dict(src=hab.pre, dest=ctrl)` (:423), and whose body carries a Blake3 digest of the ciphertext, `diger = Diger(ser=raw, code=MtrDex.Blake3_256)` (:420). The signature therefore covers the destination AID and the ciphertext; the sender AID is inside the ciphertext. That is ESSR in shape.
- It attaches the ciphertext under the `ESSRPayloadGroup` count code (:427).

Four boundaries on that `[K]`, each checked at the pin:

1. It is not the SPAC/TSP wire format. The outer wrapper is a KERI `exn` built by `specialExchange` with `version=Vrsn_1_0` (:421-425), not the `-E##` ESSR wrapper with a `SPAC` or `TSP` version field. keripy's codex defines `ESSRWrapperGroup: str = '-E'` (`src/keri/core/counting.py`:210) but `forwarding.py` does not use it.
2. Multisig receivers are not handled. Only `verfers[0]` is used, so a multi-key receiver gets one ciphertext to one key, not the per-key list the SPAC paper's multisig extension calls for (§6).
3. There is no receive handler in keripy. A grep for `/essr/req` across `src/` at the pin finds only the sender (`forwarding.py`:422). The `Exchanger` verifies that the attached ciphertext matches the signed digest, `raise ValidationError(f"essr diger={diger.qb64} is invalid against content")` (`src/keri/peer/exchanging.py`:337), but nothing in keripy routes `/essr/req` to a decrypt-and-dispatch handler. `Manager.decrypt` (`src/keri/app/keeping.py`:1431) can open a sealed box with a signing-key-derived X25519 key; no caller ties it to `/essr/req`. Per the 2026 talks (status only, §13) the receive side lives in a Veridian fork of KERIA, with an upstream PR pending.
4. No routing. There is no `HOP` processing, no relationship forming (`RFI`/`RFA`/`RFD` exist only as tag values), no padding message, and no HPKE. The tests exercise the send path only (`tests/app/test_forwarding.py`:467, :578 construct `StreamPoster(..., essr=True)`).

So keripy implements direct-mode ESSR from sender to agent or mailbox, with SPAC's payload framing inside the ciphertext. It implements none of the metadata-privacy machinery. The bible should say that keripy has ESSR, not TSP.

---

## 13. The 2026 talks: status and intent only

These are paraphrases of edited auto-captions (`raw/14` §0). None is a quotation. They support status and intent, never a design detail.

- Intent: SPAC is the name of the whitepaper's protocol, and TSP is ToIP's generic version of it (the SPAC & TSP talk; `talks-A.md` §1 summary agrees). In the State of the KERI Suite talk Sam describes the SPAC white paper as now a ToIP task force in roughly its third draft, built on a three-layer tunnel.
- Intent: the design objective is unchanged from 2023, the best privacy obtainable without compromising authenticity or confidentiality, justified by the claim that compromises on those two leak more in the end (the SPAC & TSP talk).
- Intent: the triple tunnel uses three uncorrelated AID pairs per end and exactly two intermediaries with high fan-out, and Sam says he found three tunnels sufficient after working through the metadata exposure by hand (the SPAC & TSP talk). This restates `SPAC_Message.md` §6.
- Intent: the context, not the identifier, is what correlates, and cryptographic unlinkability frames the problem at the wrong level (the SPAC & TSP talk). The written support is `SPAC_Message.md` L474 and L480 (§5).
- Intent: uniform traffic and uniform packet size at intermediaries, and colluding intermediaries can only drop traffic, which multi-route sending addresses (the SPAC & TSP talk; the Digital Identity Tradespace talk). Note the ToIP spec's contrary framing: batching and reordering are not TSP properties (§11.5).
- Intent: replay and duplicate detection for TSP traffic is to be KRAM's job (the SPAC & TSP talk, during Q&A). No written source in this note says so; the TSP spec only places freshness above TSP (§11.5).
- Intent: the relationship formation subprotocol is meant to create one-time-use contexts, potentially daily, with fresh intermediaries (the SPAC & TSP talk). The written form is §6 step 3 and §10.
- Intent: deniability (Signal-style) is rejected in favor of accountability, with voting named as a case where a different protocol is appropriate (the SPAC & TSP talk, Q&A). There is no written source for this in the Papers repo.
- Intent: RAP-C3, pronounced as rhapsody, reputable autonomic pseudonymity with control over confidential contexts, is offered as the one-line summary of KERI's privacy stance (the State of the KERI Suite talk; the Digital Identity Tradespace talk). The written trace is `BulkIssuancePrivacy.pdf` slide 42, whose ligature-damaged labels read "Reputable Control", "Autonomic Con dential", "Pseudonymity Contexts", "RAP-C 3", "Rapsody". The expansion of the acronym is this note's reading of that slide.
- Status: ESSR is in use, not just proposed. Veridian's fork has tunneled client-to-agent HTTP through ESSR for over a year, with agent-to-agent CESR streams wrapped in basic TSP form; the keripy part is merged and the KERIA part is not yet upstream (the Signify Security Architecture talk, O'Connor; `talks-B.md`:220). healthKERI's RACK gateway wrapped each transaction in ESSR and was not adopted for lack of interoperability (`talks-C.md`:94). Feairheller says ESSR protects plugin-to-SaaS traffic (`talks-B.md`:31). These are status claims by speakers and are not verified against any code but keripy's.

---

## 14. Open questions and gaps

1. Which form of the PAC trilemma is current, "at the highest level" (2023) or "to the same degree" (2021, 2025)? They make different claims. No source reconciles them.
2. An's ePrint 2001/079 was not read. The ESSR property table (§4.3) is relayed through Sam and through the ToIP spec. Before the bible states it as established, someone should read An's paper.
3. The time-value argument (§7.1) has no numbers. No source estimates a correlation time constant for any market, so the claim that partitioned contexts make privacy "sustainably protectable indefinitely" (`SPAC_Message.md` L1068) is a conditional with an unmeasured condition.
4. VID syntax (§11.6): does the ToIP spec require a bare KERI AID to be wrapped as a URN or DID? §VID Syntax and §Examples point different ways at `5599b4556`. This is worth raising with Sam, who co-authors both.
5. The SPAC paper's `-K##` hop-list code (L1377) contradicts its own tables and the ToIP spec. Probably a typo; worth a one-line fix upstream.
6. `4F`: QB2 plaintext (CESR spec) or sniffable-stream plaintext (papers)? The two describe different payloads under the same code.
7. Is the destinationless ESSR variant (§4.5) sound? The birthday-attack argument is sketched, not made.
8. keripy's ESSR receive path. The KERIA PR named in the talks was not located or read. Until it is, the statement that ESSR is implemented holds for the send side only `[K]`.
9. The Seven Privacies title. The deck never enumerates seven privacies; this note's mapping to the "Combinations" slide is an inference and should be checked with Sam before the bible uses the phrase as a defined term.
10. Gaps in reading, recorded as such: the TSP spec's test-vector appendix and the 2021 PAC deck's slides 33-78 and 93-228 (KERI tutorial material) were skimmed by title only. No other source in the assignment went unread.

---

## Already in the bible

- `bible/06-governance-ecosystems-and-interop.md:59-78` (§4). Correlation-resistance as a layered stack, the three-party exploitation model (:73), data loyalty, and the explicit deferral: "Third-party protection is encryption (out of scope, deferred to SPAC/TSP)" (:73). This note fills exactly that deferred layer. §4 should gain a forward pointer.
- `bible/06-governance-ecosystems-and-interop.md:55`. Duty of data loyalty via SEDI's governance framework. This note adds Sam's own data-loyalty argument (§7.4).
- `bible/05-acdc-and-verifiable-data.md:175-181` (§8). Chain-link confidentiality, contingent disclosure, latent accountability, and the weakness of cryptographic unlinkability against contextual correlation. Consistent with §7.3-7.4 here.
- `bible/05-acdc-and-verifiable-data.md:199` and :215. Bulk updates as a privacy requirement, blindable state, placeholder decorrelation, SMT herd privacy. §8 here adds the 2026 IIW material.
- `bible/05-acdc-and-verifiable-data.md:76`. The SMT age predicate from #1098. §8 adds the deck's ZKP-versus-SMT comparison.
- `bible/07-shibboleths-and-anti-patterns.md:388` and :499. Unlinkable ZKPs defeat detectability of issuer compromise. §7.3 adds the cryptoperiod-lifespan argument from Sustainable Privacy v1.2.8.
- `bible/07-shibboleths-and-anti-patterns.md:485` and `keri-doctrine.md:85`. "Secure the pipe" reframed as "Move security with the data (MLS/TSP), not the transport". One line each; this note supplies the mechanism.
- `bible/04-cesr-and-the-wire.md:29`. CESR is "the encoding substrate beneath KERI, ACDC, and TSP". §10-11.1 supply the codes.
- `bible/09-kram-and-request-authentication.md`. KRAM's scope is non-key-event messages. §11.5 and §13 tie TSP freshness to it.
- `bible/01-foundations-and-worldview.md:177`. A signed presentation is a durable correlator. Compatible with §5: within a context, correlation is the point.
- Absent from the bible: SPAC as a name, the PAC trilemma, ESSR as a mechanism, end-only viewability, the relationship/context/partition definitions, the nesting and routing protocols, covert versus clandestine, the time value of information, the contextual linkability attack by that name, the ToIP TSP spec's status and its candid limits, and keripy's ESSR implementation.

---

## Proposed chapter outline

A new chapter, provisionally `bible/11-confidentiality-metadata-privacy-and-secure-channels.md`. Per `standards.md` §6 this is a proposal for the PR body, not an action. Status paragraph: almost everything is `[P]`; the ESSR codes are `[N]` in CESR; the TSP draft is `[N]` but experimental; keripy is `[K]` for direct-mode ESSR send only.

1. Thesis and status. KERI's privacy argument begins where key state ends: strongest authenticity and confidentiality first, then the best privacy those allow, defended by contexts and accountability rather than by hiding. Supports: §1 (L3, L13), §3 (L103), §7.4 (slide 24). Cross-link 06 §4.
2. The trade space. PAC trilemma, its wording history, priority versus layering, cold war versus hot war. Supports: §1. Flag open question 1.
3. Vocabulary. Privacy versus confidentiality, surveillance versus data-rights definitions, the three-party exploitation model, the 2026 drift toward "confidential". Supports: §2. Cross-link 06 §4 (:73), 05 §8.
4. Effective privacy and the threat ranking. Exploitation not correlation; exploiters; identity theft first. Supports: §3. Cross-link 09 (signed requests stop privilege escalation), 07 bearer-token row.
5. ESSR. Building blocks, HPKE's KCI gap, the four unforgeability properties, KERI's AID substitution and its key-state caveat, variants, end-only viewability, 1st-party non-viewability, DDoS efficiency. Supports: §4, §11.3. Cross-link 04 (cipher codes), 03 (key state). Flag open questions 2 and 7.
6. Relationships, contexts and partitions. The formal definitions; the context, not the identifier, correlates; OOBA and cheap pseudonymity; OOBI overload. Supports: §5, §6 step 3. Cross-link 07 (OOBA row), 01 (OOBI).
7. Nesting and routing. Direct, wrapper, shared and non-shared intermediaries, three-level nesting, iSAIDs, dead-drop routing, what intermediaries learn. Supports: §6, §11.4, §11.5.
8. Sustainable privacy. Time value, covert versus clandestine, contextual linkability, ZKP cryptoperiod argument, differential privacy and synthetic data, chain-link confidentiality and data loyalty, accountability as the thesis. Supports: §7. Cross-link 05 §8, 06 §4, 07 ZKP rows, 10 (presentation registries as accountability).
9. Bulk-issuance privacy. HD-derived members, shared blinded registries, placeholder updates, SMT predicate versus ZKP, IAPC. Supports: §8. Cross-link 05 §9, 10.
10. The wire. SPAC/TSP CESR wrapper, payload types, pad, plaintext/cipher sniffing, the divergences between papers and spec. Supports: §10, §11.1. Cross-link 04. Flag open questions 5 and 6.
11. What is specified. ToIP TSP Rev 3: shape, ESSR with HPKE-Base AAD, PQ, routed mode, mandatory relationship forming, and the explicit limits (no forward secrecy, metadata privacy is not cryptographic, timing survives, non-retention is a promise, freshness above TSP). Supports: §11. Flag open question 4.
12. What is implemented. keripy direct-mode ESSR send path and its four boundaries; deployments by status only. Supports: §12, §13. Flag open question 8.
13. Shibboleths this chapter retires or adds, for chapter 07: encrypt-then-sign is enough; HPKE authenticates the sender; cryptonyms are supercookies; unlinkability is the privacy goal; selective disclosure is a safe harbor; TSP gives forward secrecy (it does not, §11.5).

---

## Proposed sources.yaml entries

Not applied. `smithsamuelm-papers` exists with `watch: [whitepapers/kram.md]`; the proposal widens `watch` and `feeds` (a reviewed-field change for the PR body) rather than adding a duplicate id. The TSP spec is a new source.

```yaml
  - id: smithsamuelm-papers
    kind: gh-repo
    repo: SmithSamuelM/Papers
    branch: master
    watch:
      - whitepapers/kram.md
      - whitepapers/SPAC_Message.md
      - whitepapers/TSP_CESR_Implementation.md
      - whitepapers/ACDCConfidentialDataManagement.md
      - whitepapers/SustainablePrivacy.pdf
      - presentations/SPAC_Overview.web.pdf
      - presentations/TSPSlides20230308.web.pdf
      - presentations/SevenPrivacies.web.pdf
      - presentations/BulkIssuancePrivacy.pdf
      - presentations/BulkIssuanceSynergyDataLoyalty.pdf
    tier: warm
    branches:
      - {name: master, role: standardizing, marker: "[P]",
         last_scanned: {commit: b47f21597, date: 2026-10-14},
         last_mined:   {commit: b47f21597, date: 2026-10-14}}
    feeds: [raw/15-kram.md, raw/17-spac-tsp-privacy.md]
    chapters: ["05", "06", "07", "09"]
    caveat: >-
      last_mined b47f21597 applies to the files mined for raw/17 on 2026-10-14. kram.md was last
      mined at 67550b477 on 2026-09-15 and was not re-read; keep its pin in raw/15. Now cloned
      locally at wot/Papers; PDFs are read via pre-extracted text, which loses fi/ff ligatures in
      several decks. SPAC_Message.md's version string (0.5.3) has not moved since 2023 despite
      content changes through 2025-06; cite by commit. SPAC_Strawman, KERI_PAC_Theorem,
      TSPSlides20230208 and SustainablePrivacySlides are superseded or subsumed; read, not watched.

  - id: tsp-spec
    kind: gh-repo
    repo: trustoverip/tswg-tsp-specification
    branch: main
    watch: [spec/spec.md]
    tier: warm
    branches:
      - {name: main, role: standardizing, marker: "[N]",
         last_scanned: {commit: 5599b4556, date: 2026-10-14},
         last_mined:   {commit: 5599b4556, date: 2026-10-14}}
    feeds: [raw/17-spac-tsp-privacy.md]
    chapters: ["04", "06", "07"]
    caveat: >-
      Experimental Implementor's Draft Rev 3 with Errata (2026-09-30); wire version 0.2. [N] here
      means present in the line ToIP is standardizing, and that line calls itself experimental.
      Not cloned under ~/code; read from a shallow clone on 2026-10-14. Only spec/spec.md is
      rendered (specs.json markdown_paths); the other spec/*.md files are template residue. The
      test-vector appendix was not mined.
```

The keripy source entry would need `src/keri/spac/` and `src/keri/app/forwarding.py` added to its `watch` list, feeding `raw/17`; that is a reviewed-field change and is left to the PR body.
