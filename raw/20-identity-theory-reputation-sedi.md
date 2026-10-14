# Doctrine Mining: identifier theory, reputation and identity assurance, SEDI as law, the no-KERI-light doctrine, and KERI's lineage

Primary sources, with pins:

- Samuel M. Smith, Papers repository (`SmithSamuelM/Papers`, local clone `~/code/wot/Papers`), branch `master` at `b47f21597` (last commit 2026-08-11). Every Papers quote below is pinned to that commit unless a different commit is named. PDFs were read through the pre-extracted text in `.ignored/papers-text/`; citations give the PDF's repo path and its page or slide heading.
  - `whitepapers/UniversalIdentifierTheory.pdf` and `whitepapers/IdentifierTheory_web.pdf`, v1.40 dated 2025/09/14 (the two paths are one blob; see §0.2). The prior v1.32 (2020/10/23) was read at Papers `416b7ac` for the diff in §1.8.
  - `whitepapers/Identity-System-Essentials.pdf` (2016-03-29, with Dmitry Khovratovich, Evernym).
  - `whitepapers/SelfIdentifyingData.md` (2017/10/27), `whitepapers/DecentralizedAutonomicData.md` (2018/03/07), `whitepapers/A_DID_for_everything.md` (RWOT VII, 2018), `whitepapers/IdentityAndReputation.md` (2018), `whitepapers/CooperationBeatsAggregation.md` (v1.6, 2019/11/19; markdown added 2024-02-07).
  - `presentations/ReputationAlgorithms.pdf` (2016), `presentations/ReputationIIW2017.pdf` (2017), `presentations/ReputationDisintermediation_IIW_20180405.pdf` (2018-04-05), `presentations/AR_ACDC_Rep.web.pdf` (added 2022-05-10), `presentations/DuplicityGame_IIW_2020_A.pdf` (IIW Spring 2020).
  - `presentations/SEDI_Tradeoff.web.pdf` (dated 2025/10/01; last changed `d00f260`, 2025-10-11) and `presentations/SecurityThreatsMitigationsSEDI.web.pdf` (added `144829e` 2025-11-04, last changed `6fa71dd` 2026-01-16).
  - Read only for a header line, to date the lineage: `whitepapers/open-reputation-low-level-whitepaper.pdf` and `whitepapers/open-reputation-high-level-whitepaper.pdf`.
- Utah Code Title 63A Chapter 20, State-Endorsed Digital Identity, as the official PDF `C63A-20_2026050620260506.pdf` (13 pages) held in the private repo `bakobo/sedi` at `91402ae99` (same bytes as `legislation.pdf` there). Text extracted with `pdftotext -layout`. Public copy to verify against: https://le.utah.gov/xcode/Title63A/Chapter20/63A-20.html (not fetched in this pass).
- did:webs specification, `trustoverip/kswg-did-method-webs-specification` (local `~/code/wot/kswg-did-method-webs-specification`), branch `main` at `2d84ef2b0` (2026-08-11), `spec/header.md` and `spec/body.md`. The spec header reads v0.10.3.
- KERI and ACDC specifications, only for negative results and one cross-reference: KERI spec `main` at `fbdd4a615`, ACDC spec `main` at `f0bd097de`, `spec/spec-body.md` in each.
- KERI Conference 2026 captions, `keri-foundation/CONF26-subtitles` at `006042d39` (2026-10-04), read as the joined per-talk text in `.ignored/conf26/text/` and the summaries in `.ignored/conf26/talks-A.md` and `talks-D.md`. Conference: Lehi, Utah, 22-23 April 2026. The same repo carries 22 clips from the Utah SEDI Summit of 2025-10-17 (files prefixed `SEDI25`).

Mining date: 2026-10-14. Miner: mine-identity worker, against the coverage-gap report `.ignored/coverage-gaps-2026-10.md` §2.4, §2.8, §2.9, §2.10 and the lineage paragraph of §2.11.

---

## 0. Provenance notes, read before citing

### 0.1 Tiers

Nothing in this note is `[N]` or `[N1.1]` except where a spec is quoted directly, and the spec quotes are almost all negative results (§9). Every Papers claim is `[P]`: Sam's position, or a co-authored position, stated in a whitepaper or slide deck. None of the identifier-theory, reputation or no-half-measures ideas below has reached the KERI or ACDC specification, and none is a keripy feature (§9 gives the grep evidence). The Utah statute is enacted law and is quoted as law, which is a different kind of authority from any tier marker: it binds the State of Utah and parties dealing with a state-endorsed digital identity, and says nothing about KERI by name.

### 0.2 The two Identifier Theory PDFs are one document

`whitepapers/UniversalIdentifierTheory.pdf` and `whitepapers/IdentifierTheory_web.pdf` have the same blob, `c39bd466ba129f586096d128bca008279873c9f1`, at `b47f21597`. Commit `e2e995f` (2025-09-14, "added UniversalIdentifierTheory updated") added the first path and replaced the second with the same bytes. Either path is current. Cite `UniversalIdentifierTheory.pdf`, because its name matches the document's own title and the older path's history begins with a different version. The document's title page reads "v1.40 2025/09/14, Original 2020/10/20". The v1.32 text that the older path held from 2020-10-23 differs from v1.40 almost entirely in copy-editing; the three substantive changes are recorded in §1.8.

### 0.3 Caption material uses a different mark

Conference captions are edited auto-captions. Following `refresh/prompts/standards.md` §2 and `raw/14 §0`, they are usable for status and intent only and are never quotations. In this note, straight double quotes mean a verbatim quotation from a written source. Caption near-wording is set in guillemets, «like this», with the talk file named. A guillemet passage is the caption text as it appears in the joined file, given so that a reader can find the spot in the video; it is not a record of what the speaker said and must not be promoted to a quotation without checking the video.

### 0.4 Authorship of the papers

Several lineage papers are not Sam's alone, and the corpus should not attribute their sentences to him without saying so. Identity System Essentials is by Smith and Khovratovich. A DID for Everything lists seven presenters, Smith among them. Cooperation Beats Aggregation is by Shea, Smith and Stöcker, with Caballero as editor. The high-level Open Reputation paper is by Lincoln Cannon; the low-level framework paper is Sam's. The keri.one About page's founding sentence (`raw/13-keri-one-web.md`:40) comes verbatim from the co-authored 2019 paper (§2.6).

### 0.5 What a slide deck can and cannot carry

The 2025 SEDI decks are slides, extracted to text with diagrams flattened. Quotes below are taken only from lines of prose on a slide. Where a slide's line was cut by the extractor, the quote stops before the cut. A slide line is a bullet, not an argued paragraph, so these are Sam's positions as headlines; the reasoning is in the talks and in the SPAC and Sustainable Privacy papers, which are not mined here.

---

## 1. Universal Identifier Theory: the identifier model KERI sits inside

Status: `[P]`, Sam's whitepaper, v1.40. None of its named constructs (LID, the aid|lid couplet, primary/secondary/tertiary identifiers, trust basis, well-known reputational association, the PAC trilemma) appears in the KERI or ACDC specification at the pins (§9).

### 1.1 Identity is an identifier plus attributes, and the identifier comes first

The paper says it speaks of identifier systems rather than identity systems in its first sentence on the subject: "We use the term identifier system instead of identity system" (`whitepapers/UniversalIdentifierTheory.pdf` §1.1, p.1), because the identifier's properties come first. Its definition is narrow on purpose: "We formally define a (digital) identity to be a (digital) identifier plus attributes." (§1.1, p.1). The model "takes a security-first approach" (§1.1, p.2), and the paper names the mechanism it treats as the universal basis for identifier security: self-certification (§1.2, p.2-3). This is the theoretical root of the security-first-always motto Sam repeats in the 2026 talks (`raw/14`; Tradespace summary in `.ignored/conf26/talks-A.md` §3).

### 1.2 Three trust bases

The paper classifies every identifier system by its trust basis: autonomic (a self-certifying root of trust), algorithmic (a ledger) and administrative (a trusted entity). Of the ledger: "One may characterize a ledger as a centralized logical construct that is governed in a decentralized manner." (§1.2, p.4). Of the administrative basis: "Security may be dependent on something as nebulous as employee morale." (§1.2, p.5). The trust basis is what the 2025 SEDI deck later reduces to one slide, contrasting a root of trust "in verifiable cryptographic proofs of infrastructure with no shared governance" with the other two (`presentations/SEDI_Tradeoff.web.pdf`, slide "Trust Basis of a Trust Domain"). Bible 01 §2-3 already argues autonomic over administrative; it does not use the three-way classification or the ledger sentence, which is the sharpest one-line statement of KERI's objection to ledgers in the corpus.

### 1.3 The trust domain

"The trust domain of an AID is the set of statements that may be securely verified as being issued by the controller of that AID" (§1.3, p.6). Authorizations "inhabit and are protected by this trust domain" (§1.3, p.6). The trust domain is the unit the rest of the paper builds on, and it is the construct that lets a human-meaningful name become secure.

### 1.4 LIDs and the aid|lid couplet

Human-meaningful identifiers are insecure by construction: "there is no inherent security property of a human-meaningful identifier. This makes them insecure by default." (§1.4, p.6). The paper's answer is to legitimize a name inside a trust domain: "This gives rise to a new class of identifier, a legitimized or authorized human meaningful identifier, and uses the acronym LID." (§1.4, p.6-7), written as the couplet `aid|lid`, where the bar is the legitimizing authorization (§1.4, p.7). The scarcity that makes names contested is localized: "Scarcity only occurs within the trust domain of each AID but is completely managed by the controller of that trust domain (AID)." (§1.4, p.7). This is the paper's claimed resolution of Zooko's triangle. Its stated objection to the earlier ledger-based resolutions is that they needed "not one identifier but a combination of identifiers", which "hints that the identifier model therein employed is incomplete" (§1.1, p.2). The aid|lid couplet is itself a combination of two identifiers, so the paper's claim amounts to saying the combination is principled when the bar is a verifiable authorization. That is Sam's argument; the corpus has no outside assessment of it.

The paper's own examples make the point concrete: "GLEIF's Legal Entity Identifier (LEI) may be viewed as a type of LID" (§1.7, p.11), legitimized by a GLEIF root AID, and GS1 GTIN, SGTIN and GLN codes are treated the same way (§1.7, p.11).

### 1.5 Primary, secondary and tertiary identifiers

AIDs are primary, LIDs secondary, and everything else tertiary: "tertiary identifiers are unsecured and may only be used internally or where security is unimportant" (§1.4, p.7). "Secondary identifiers are LIDs and are not self-certifying but are secured under the aegis of an associated primary identifier's trust domain." (§1.4, p.7). Interpretation, mine: this gives the bible's alias doctrine a theoretical home. Bible 07 §9.4 (`bible/07-shibboleths-and-anti-patterns.md`:360-366) says an alias is "a memory aid, not evidence" and that only AIDs may drive system logic. In UIT terms that is the rule for tertiary identifiers. A LID is different: it is a name made verifiable by an anchored authorization, and the did:webs designated-aliases ACDC (§6) is a working instance of one. A reviewer should not let 07 §9.4 be read as forbidding LIDs, and should not let a LID be treated as a bare alias.

### 1.6 Reputational trust, and authenticity before veracity

The paper splits trust into two kinds. Cryptographic attribution lets us trust who said something and whether they were consistent: "But we may not trust in the veracity of what was said. For this, we need the second type of trust." (§1.5, p.8). It defines reputation narrowly: "Reputation is a measure of accumulated consistent behavior." (§1.5, p.8). And it orders the two: "First, authenticity (AID), and then veracity (LID)." (§1.5, p.8), closing the loop with "Provable trust in the AID mechanism enables provable trust in the entity behind the LID mechanism." (§1.5, p.9).

This is the same split the bible already rests on through Hardman's authenticity-vs-veracity paper (`bible/06-governance-ecosystems-and-interop.md`:25; `bible/01-foundations-and-worldview.md`:153), and the UIT version predates the version the bible cites, in its 2020 v1.32 form. Two differences are worth recording. First, UIT makes veracity depend on authenticity rather than treating them as independent axes. Hardman's paper calls them orthogonal "primarily" (bible 06:25), and the two framings are compatible: independence of judgment, dependence of usefulness. Second, UIT's pairing of veracity with the LID is loose. A LID is a name, and the veracity in question is the veracity of the authorizer's act of legitimizing it, not of the name. The bible should cite UIT for the dependency and keep Hardman's terms for the analysis.

### 1.7 Root AID establishment by well-known reputational association

The paper confronts the bootstrap problem directly: a self-certifying identifier is unique but unrecognizable. "The process that establishes an AID as the root identifier with an organization may be called a well-known reputational association." (§1.6, p.9). Redundancy is the mechanism: "The strength of the well-known establishment is multiplied by the number of such associations, i.e., it provides a reputational source of trust." (§1.6, p.9), and "Consistent common knowledge is the root of reputational trust" (§1.6, p.10). It names RFC 8615 `/.well-known/` paths as one such mechanism (§1.6, p.10).

This is the conceptual ancestor of the KERI specification's OOBI-with-MFA pattern, which the bible quotes at `bible/06-governance-ecosystems-and-interop.md`:41-43: the same AID published at several independently controlled `/.well-known/oobi/{aid}` locations, accepted only on threshold agreement `[N]` (KERI spec §OOBI with MFA, L2838 at `fbdd4a615`). The spec draws a boundary UIT does not draw as clearly. The spec says the arrangement governs only the recipient's willingness to bootstrap and leaves the trust model unchanged (bible 06:43). UIT calls the multiplied associations "a reputational source of trust" for the root AID. Both are right about different things. Which AID belongs to an entity is a reputational, Layer-2 question, and that is what UIT is answering. Whether a given event was signed by that AID's keys is Layer 1, and nothing in the well-known process touches it. The bible's §1 already enforces this boundary; this note adds that the spec's pattern is the formalization of a 2020 whitepaper idea.

### 1.8 The PAC trilemma, and what v1.40 changed

The paper's last theoretical section states a trilemma for identifier system security overlays: privacy, authenticity and confidentiality, two at most at the highest degree. v1.40 states it as "One must make a trade. This is a trilemma for identifier system security overlays." (§1.8, p.12) and adds a choice the 2020 text did not make: KERI picks complete authenticity and confidentiality "because this best protects all participants from impersonation fraud." (§1.8, p.12). The v1.32 text at Papers `416b7ac` said only that KERI provides the highest authenticity, called it "a trilemma for identifier systems" (§1.8, p.11/39), and labelled the figure the "Triangle/Trilemma of Identifier System Properties"; v1.40 renames it "PAC Trilemma" and the diagram "Smith's Triangle" (§1.8, p.12). The 2025 SEDI deck makes the trilemma its opening frame: "An interaction between two parties may be two of the three, private, authentic, and confidential at the highest degree" (`presentations/SEDI_Tradeoff.web.pdf`, slide "PAC Theorem — Trilemma").

The other two substantive v1.40 changes. On DIDs, v1.32 said "AIDs may be used as a type of DID." (v1.32 §1.3, p.6/39 at `416b7ac`); v1.40 replaces that with "A given DID may be a type of AID but not all DIDs are AIDs." and "KERI itself is name space agnostic" (v1.40 §1.3, p.6). The newer text stops treating DID as KERI's namespace, which matches the did:webs position in §6. On delegation, v1.40 deletes the v1.32 sentence "In the worst case the delegator may re- voke the delegates identifier prefix and replace it with a new one." (v1.32 §5, p.24/39; quoted with the extractor's line-break hyphen). The deletion is unexplained. A reasonable reading, not confirmed, is that delegator-side replacement of a delegate's prefix no longer matches how delegated recovery works in the spec, where a superseding recovery rotation keeps the delegate's identifier.

Bible coverage of the trilemma is indirect: bible 06 §4 says KERI-core "does not promise unlinkability, and cannot" (`bible/06-governance-ecosystems-and-interop.md`:61). The trilemma is the reason, and the bible does not state it.

### 1.9 Two further UIT constructs, briefly

The paper names two authorization models after a key rotation, and the first is the one KERI anchoring serves: "Any signed statement that is signed with the set of authoritative keys at the time of its signing is valid until revoked" (§4.1, p.20, Rule 1, the persistent authorization model). The bible covers the mechanism as anchored signatures (`bible/03-key-management-and-identifier-lifecycle.md`:171) without the persistent/ephemeral naming. And it proposes verifiable algorithms for automated LID issuance, where a verifiable algorithm "is both an explainable algorithm and a transparent algorithm", built on a provenanced chain of DAD items (§8, p.35). That is the 2018 DAD idea (§7.4) carried forward and is a thread to the AI-agent material the coverage report ranks fifth; it is not developed further here.

---

## 2. Reputation: the doctrine KERI was built to serve

Status: `[P]` throughout. No spec or keripy artifact implements reputation computation, and the KERI and ACDC specs at the pins do not contain the word reputation (§9).

### 2.1 The definition has been stable for a decade

Sam's reputation decks from 2016 to 2022 carry one definition: reputation is "A considered evaluation (measure) of past behavior used to predict future behavior." (`presentations/AR_ACDC_Rep.web.pdf`, slide "REPUTATION"; the same line is in `presentations/ReputationIIW2017.pdf` and `presentations/ReputationDisintermediation_IIW_20180405.pdf`). Its qualification is context: "Confidence improves with contextual similarity." (AR_ACDC_Rep, same slide; the 2017 deck spells it "simularity"). UIT v1.40 repeats the dictionary root and the past-predicts-future reading (§1.5, p.8-9), and the 2025 SEDI deck compresses it: "Reputation is a behavior-based contextual predictor that enables an interaction." (`presentations/SEDI_Tradeoff.web.pdf`, slide "Reputable Authenticatable Pseudonymity (RAP)").

### 2.2 Reputes, not ratings

The design rule from the Open Reputation period is that reputation is computed from recorded behavior, not from scores people give each other. "Computational generation of a reputation is to aggregate relevant instances of behavior." (AR_ACDC_Rep, slide "COMPUTATIONAL REPUTATION"). The instance is a repute, and the advantage is re-evaluation: "Reputation from reputed behavior allows for re-scoping, re-weighting, re-combination, and re-evaluation of collected reputes (not so for ratings)" (same slide). Three properties rank predictors: "Contextual predictors are more powerful", "Behavior based predictors are more credible", "Transitive predictors are more portable" (AR_ACDC_Rep, slide "WHAT IS REPUTATION AI?").

Reputation and credentials are related but not the same thing: "Reputation is not a set of verifiable claims but a set of verifiable claims can contribute to a reputation" (`presentations/ReputationIIW2017.pdf`, slide "ISSUES", text extracted with ligatures). That sentence is worth carrying into the bible, because the commonest outsider prior is that a credential is a reputation.

### 2.3 Curation, platforms and the meta-platform

The economic argument runs through every deck from 2016 to 2022: "Curation is applied reputation" (AR_ACDC_Rep, slide "CURATION"; also `presentations/ReputationAlgorithms.pdf`), and "Portable Reputation is a potential meta-platform" (AR_ACDC_Rep, slide "META-PLATFORM"; the 2016 deck says "candidate"). The 2018 short note states the dependency in one line: "decentralized identity is essential to decentralized reputation which is essential to decentralized 2 sided networks." (`whitepapers/IdentityAndReputation.md`, paragraph 2), and adds "This inverts the architecture of block-chain applications." (same). The 2018 disintermediation deck gives the political version: "Seek disintermediation, not justice." (`presentations/ReputationDisintermediation_IIW_20180405.pdf`, slide "Disintermediation Theory").

### 2.4 Reputation by reference and by behavior

Sam's State of the KERI Suite talk lists UIT's contributions as including «be a reputation by reference» (caption, `Samuel Smith ｜ State of the KERI Suite ｜ KERI Conference 2026.txt`). The UIT text does not use the phrase; it describes the mechanism without the name (§1.6-1.7 above: a chain of trust from a well-known root AID through legitimizing authorizations). Windley's talk gives the clearest statement of the pair, as status only: reputation by reference is «essentially how we bootstrap things», illustrated by a diploma chained through accreditors (caption, `Phil Windley ｜ Digital Identity Needs a Legal Foundation ｜ KERI Conference 2026.txt`), while reputation by behavior is the credit-bureau model, which he imagines replaced by receipts as credentials and a marketplace of scoring algorithms (same file; `.ignored/conf26/talks-A.md` §6). An exchange in the Q&A, speaker attribution uncertain, sharpens it: «In reputation you explicitly trust the reputer.» and «Trust requires vulnerability.» (same file).

The two framings line up with Sam's older vocabulary. Reputation by reference is the indirect, intermediated reputing of the 2017 deck, where a reputery is an "Indirect Source (Implied Reputer) or Intermediate Source" (`presentations/ReputationIIW2017.pdf`, slide "INDIRECT AND INTERMEDIATED REPUTING"). Reputation by behavior is the direct repute. What is new in 2025-2026 is that ACDC chaining is named as the carrier for the first kind: "Verifiable reputation via ACDC chained evidence dossiers" and "Multiple roots-of-trust for reputation" (`presentations/SEDI_Tradeoff.web.pdf`, slide "Unique features of KERI/ACDC that require Issuer linkability").

### 2.5 Reputable authenticatable pseudonymity, and the cheap-pseudonymity problem

The 2025 decks name the target state RAP: "RAP = Trust based on contextual behavior that is securely cryptonymously attributable but without linkage to an actual person or legal entity." (`presentations/SEDI_Tradeoff.web.pdf`, slide "Reputable Authenticatable Pseudonymity (RAP)"). The same slide states the limit: "there is no practical pseudonymity without strong counterincentives for 2nd parties to share contextual behavior data." In the 2026 talks RAP becomes RAP-C3, with the A read as autonomic and C3 as control over confidential contexts, and Sam offers it as his one-line summary of KERI (`.ignored/conf26/talks-A.md` §2, §3; caption «RAP-C3 and if you say it really fast it's a rhapsody» in the State of the KERI Suite file). The A changes between the deck (authenticatable) and the talk (autonomic); the corpus should not normalize it.

The obverse is the cheap-pseudonymity problem, stated only in speech. In the Tradespace talk, identity assurance «solves one problem. It's called the cheap pseudonymity problem», because anyone can mint and abandon AIDs, so «nobody can trust an AID that anybody can create» (caption, `Samuel Smith ｜ The Digital Identity Tradespace ｜ KERI Conference 2026.txt`). The transcript ends a sentence later, just as he begins the GLEIF analogy (`talks-A.md` front matter notes the truncation). This is a status-and-intent source: the argument is clear, the details of how SEDI's assurance answers it are not in any written source mined here.

### 2.6 The founding sentence and its real source

The keri.one About page carries Sam's founding insight, which `raw/13-keri-one-web.md`:40 records verbatim from the page. The sentence predates the page. It is in the 2019 RWOT9 paper Cooperation Beats Aggregation: "a reputation is meaningless without an underlying identity and an identity is valueless without a credible reputation." (`whitepapers/CooperationBeatsAggregation.md` §Identity and reputation systems as trust brokerages, line 132). That paper is by Shea, Smith and Stöcker. The corpus should keep attributing the founding insight to Sam as his stated position, and cite the paper as its earliest written form with its co-authors named. The same section supplies the economic frame: "Trust and reputation are truly paramount to commerce as we know it" (§Accounting for trust in current and future systems), and a decentralized identity and reputation system "enables trust to be transitive between contexts to some degree" (§Identity and reputation systems as trust brokerages; the source bolds the middle phrase).

### 2.7 The ACDC reputation deck promises more than it delivers

`presentations/AR_ACDC_Rep.web.pdf` is titled "Automated Reasoning and ACDCs", subtitled "Secure Decentralized Reputation Algorithms" and "Leveraging Property Graphs in ACDC" (title slide). Read in full, its content is the 2016-2018 reputation and platform material plus Sam's symmetric multiple elastic constraint (SMEC) reasoning slides, whose claimed features include "Works well with sparse data." and "Elastic constraint network is explicable. GDPR compliant." (slide "SMEC Features"). No slide shows an ACDC property graph used as reputation input, an ACDC schema for reputes, or any mechanism specific to ACDC. The deck is evidence that Sam linked ACDC to reputation in 2022, not evidence of a design. Record it as such; do not cite it for an ACDC reputation mechanism.

---

## 3. Identity assurance and proofing

Status: the statute is law; the rest is `[P]` or caption.

### 3.1 Assurance as accumulated weak bindings

The 2025 SEDI deck has one slide, "Identity Assurance and Reputation", whose diagram shows several assurers each asserting a weak binding between a natural or legal person and an AID's controller, and whose caption line is "Relatively weak binding reinforced by multiple bindings = reputation" (`presentations/SEDI_Tradeoff.web.pdf`; repeated in `presentations/SecurityThreatsMitigationsSEDI.web.pdf`). This is the same argument as UIT's well-known reputational association (§1.7), applied to people instead of organizations: no single proofing act is strong, and redundancy across independent assurers is what makes the binding credible. The feature list adds a durability claim: "Strongest Identity assurance amortized over the lifespan of unbounded term (persistence) AIDs" (SEDI_Tradeoff, slide "Unique features of KERI/ACDC that require Issuer linkability"). The economics are the point: proof once, at high cost, against an identifier that survives key rotation, rather than re-proof at every key or device change.

### 3.2 What the statute requires of proofing

Utah's statute defines identity proofing as "the process of collecting, validating, and verifying information about an individual to establish confidence in the individual's claimed identity." (Utah Code §63A-20-201(12)). The department must follow "a generally accepted identity proofing standard" (§63A-20-303(1)(a)(i)) and must define by rule "in-person, remote, or hybrid methods" (§63A-20-303(4)(b)(ii)(A)). Two provisions matter for KERI's design. The endorsement "reflects verification at a point in time; and" must not require "continuous monitoring" or "tracking" (§63A-20-303(1)(d)). And proofing is the gate to the credential: an applicant must "successfully complete the department's identity proofing process" (§63A-20-302(6)(c)). The statute does not name an IAL. The IAL3 reference is Sam's, in speech: if SEDI proofing is «IAL level three identity assurance, it has to be an in-person thing», which makes it a natural out-of-band point to exchange the salt that drives blinded registry updates (caption, Tradespace file). That pairing of the proofing ceremony with the blinding-salt exchange is a design suggestion, not a requirement in any written source.

### 3.3 Point-in-time assurance in the bible already

The bible already holds the verifier-side version of point-in-time assurance: org-vet's `assuranceIsPointInTime` clause and its levels of assurance (`bible/06-governance-ecosystems-and-interop.md`:37-39). The statute's §63A-20-303(1)(d) is the same doctrine stated by a legislature for persons. A bible section on assurance should put them side by side.

---

## 4. SEDI as law and policy

Status: statute quotes are law at Chapter 436, 2026 General Session, effective 2026-05-06 (statute PDF, every section footer "Enacted by Chapter 436, 2026 General Session"; header "Effective 5/6/2026"). Talks are status and intent. Sam's decks are `[P]`.

### 4.1 Which law, and a naming hazard

The talks call the SEDI law SB 260 (`.ignored/conf26/talks-D.md`, SEDI-LegPanel and SEDI-Chang summaries, both from the 2025-10-17 summit; Windley's April 2026 talk describes the statute's rights without a bill number). The statute text read here is the 2026 enactment, Chapter 436 of the 2026 General Session. This note did not establish whether SB 260 names the 2025 bill that the summit discussed, the 2026 bill that became Chapter 436, or both. A chapter citing the law should cite the Utah Code sections and the session-law chapter, and use a bill number only after checking it at le.utah.gov.

### 4.2 The bill of rights

The founding right, already quoted in the bible from the schema documentation (`bible/06-governance-ecosystems-and-interop.md`:47), is in the enacted text: "An individual possesses an individual identity innate to the individual's existence and independent of the state, which identity is fundamental and inalienable." (§63A-20-101(1)). The other ten rights in §101 are absent from the bible. The ones that bear on KERI's design:

- A right to a physical alternative and against compulsion: "a right to not be compelled by the state to possess, use, or rely upon a digital form of identity assertion" (§101(4)), backed by a ban on governmental entities conveying "a material benefit upon an individual for using a state digital identity instead of a physical identity" (§63A-20-304(1)(a)).
- A right against arbitrary revocation of the endorsement (§101(5)), made concrete by §301(5), which allows revocation only for compromise, error or fraud, or at the holder's request: "The department may only revoke an individual's state-endorsed digital identity if:" (§63A-20-301(5)).
- A right to transparency of the standards and technical specifications (§101(7)).
- A right to choose which attributes are disclosed (§101(8)).
- A right to be "free from surveillance, profiling, tracking, or persistent monitoring of the individual's assertions of digital identity by the state" (§101(10)).
- A right not to surrender one's device to present (§101(11)), repeated as a duty on verifiers and relying parties (§63A-20-501(3), §63A-20-601(3)).

### 4.3 The statute writes KERI's properties as requirements without naming KERI

Interpretation, mine, with the text to check it against. The statute is technology-neutral, and the legislative panel said so (`talks-D.md`, SEDI-LegPanel). But several of its definitions and requirements are the properties of a KERI AID stated in legal language:

- A "personal digital identifier" must be "created by or at the direction of an individual;", "mathematically provable to be under a holder's control; and", and "transportable to technical infrastructure of the holder's choosing." (§63A-20-201(20)(b)-(d)). Those are self-certification, end-verifiable control, and portability across infrastructure, which UIT lists as the three properties of a SCID (UIT §1.2, p.3) plus KERI's portability claim.
- A state-endorsed digital identity must "incorporate state-of-the-art safeguards for protecting an individual's identity, including compromise detection, recovery mechanisms, and cross-context correlation protections" (§63A-20-301(1)(a)). Compromise detection and recovery are what pre-rotation and duplicity detection provide; the statute does not say how.
- A digital identity by definition "does not include an electronic record that only relies on shared authentication information to verify an individual's identity" (§63A-20-201(4)(b)). That excludes the shared-secret model KERI's doctrine rejects.
- The state may not build in surveillance: the identity "may not include a mechanism that allows the department to monitor, surveil, or track the presentation of a state-endorsed digital identity to another entity." (§63A-20-301(3)). This is the no-phone-home property that registrar/observer and blinded registries exist to provide (`raw/14` §1-2).
- The infrastructure controlling issuance and revocation must be "maintained within a state-controlled data center located within the state" (§63A-20-301(2)(c)). For KERI this constrains where the state's issuer keys, witnesses and registrar live, not where holders' infrastructure lives.

The fit is close but should not be overstated. The statute permits other technologies that meet these requirements, and the Utah CTO said no SEDI technology had been chosen as of October 2025 (`talks-D.md`, SEDI-Jackson). Sam's position is that only KERI meets them (§5.1); that is his assessment.

### 4.4 Guardianship, wallets, verifiers and loyalty

The statute defines a "digital guardian" as "a person authorized to act in the best interest and on behalf of another individual." (§63A-20-201(3)(a)), including custodial parents and court-appointed guardians (§201(3)(b)). Wallets, verifiers and relying parties must each support presentation by a digital guardian (§63A-20-401(1)(h), §501(1)(e), §601(1)(e)). The bible's guardianship content is schema-level and partly struck (`bible/05-acdc-and-verifiable-data.md`:248). The talks supply the design intent: weighted M-of-N multisig for family arrangements, with a court able to hold weight (`talks-D.md`, SEDI-Ruff), a live guardianship demo on KERI and ACDC (`talks-D.md`, SEDI-Mayfield), and a «glass break» for revoking a contested parent-child endorsement (caption, `George McEwan ｜ The Landscape of SEDI ｜ KERI Conference 2026.txt`). Sam's deck lists dynamically revocable delegated chains of authority as the mechanism, with "= secure guardianship" on the same slide (`presentations/SEDI_Tradeoff.web.pdf`, slide "Unique features of KERI/ACDC that require Issuer linkability").

Wallets must keep a secure log of what was disclosed to whom, "accessible only to the holder;" (§63A-20-401(1)(f)(ii)), and must let the holder choose a conforming wallet (§301(1)(f)) and migrate between wallets (§301(2)(g)(i)(E)).

The duty of loyalty binds the department, wallet providers, verifiers, relying parties and digital guardians, who "shall refrain from practices or activities related to the processing of an individual's identity attributes from a digital identity that:" conflict with the individual's best interests, "take advantage of or otherwise exploit an individual;", or cause disproportionate risk, detriment or harm (§63A-20-701). The bible treats data loyalty through the SEDI rules file (`bible/06-governance-ecosystems-and-interop.md`:55) and as a layer of correlation resistance (bible 06 §4). It does not cite the statute, which is the stronger authority. Note that the statute's word is "exploit". Sam's 2025 deck reframes privacy as protection from exploitation (§5.3 below), and the ACDC spec says the goal is "protection from the unpermissioned exploitation of data" (bible 06:63). The statute, the spec and the deck converge on exploitation as the harm. Unlinkability is not the harm in any of them.

### 4.5 Enforcement

Enforcement runs through a state officer and the attorney general, not a private suit. "An individual may submit a complaint to the data privacy ombudsperson alleging a violation of this chapter" (§63A-20-801(1)), who may refer it to the attorney general, who may "bring a civil action in a court of competent jurisdiction to:" enjoin, obtain declaratory relief, or recover damages and restitution on behalf of an injured individual (§801(4)(b)). The audience at Windley's talk noted the absence of a private right of action (`talks-A.md` §6). The Legislative Auditor General must audit the program, including whether the department met the anti-surveillance restrictions, beginning 2028-01-01 (§63A-20-802).

### 4.6 The state's self-limits, as stated by its officials

These are policy statements in speech, not statute. McEwan (Utah privacy architect): «We are not the wallet. We're not your key escrow. We're not your key recovery.», and on escrow, «it's not your identity if somebody else has full access to your keys and can perform rotations without your permission» (caption, McEwan Landscape file). Rep. Cutler at the 2025 summit: «The role of the state is to endorse, verify, authenticate, protect, and guarantee an individual's digital identity.» and «the role of the state is not to own, create, control, gatekeep, or surveil an individual's digital identity.» (caption, `SEDI25 02-21-20--02-32-35-Paul-Cutler.txt`). Windley: «These are legal rights, not terms of service.» (caption, Windley file).

McEwan's escrow remark is a governance statement of a KERI property the bible already holds: custodial and multisig arrangements are acceptable only if the controller keeps the ability to rotate away (`bible/03-key-management-and-identifier-lifecycle.md`:97, custodial rotation). The statute does not contain it.

### 4.7 Roadmap items that are not law

Two items in the talks are intentions, not statute or rule, and a chapter must label them so. Wallet attestation: the state expects «hash and a signature of the application you're using» at endorsement, will recognize audited wallets, and will issue to a self-built wallet only after the holder affirmatively consents (caption, McEwan Landscape file; `talks-D.md`, GM-SEDI). The statute says only that the holder may choose "a digital wallet that conforms with the requirements established by the department" (§63A-20-301(1)(f)). Personas, preset disclosure bundles for routine contexts, are McEwan's term (caption, same file); the statute's nearest provision is the right to choose disclosed attributes (§101(8)).

### 4.8 Sam's threat model for SEDI

Sam's SEDI decks are a security argument addressed to the state as issuer. The threat he leads with is not to holders but to the issuer's signing infrastructure. The persistence and scale of SEDI raise its value to attackers: it has "Potential to replace existing decentralized identity assurance mechanisms with single universal State endorsement." (`presentations/SecurityThreatsMitigationsSEDI.web.pdf`, title slides), so the "Issuer Signing Infrastructure is a single point of failure for the whole ecosystem" (same deck, slide on insider threats). The weak point is authorization to sign, not the HSM: "Weakest vulnerability is the AuthZ infrastructure not the signing hardware." (same deck, slide "Conventional Enterprise Signing Infrastructure").

His conclusion is that recovery has to be specific, which requires anchoring, which requires linkability. "Revoking and reissuing millions or tens of millions of Government issuances due to likely or potential key compromise is impractical." (SEDI_Tradeoff, slide "Why key compromise is the hard problem for SEDI"). "Anchored issuances are linkable and thereby enable the detection of specific forgery and the specific recovery of forged issuances." (same slide), so "Specific recovery is a viable and practical solution to the hard problem of key compromise for SEDI" (same slide). Bible 10 and the SEDI scenario already explain anchoring and registries; what they do not carry is this argument from the issuer's recovery cost at state scale, which is the reason Sam rejects issuer-unlinkable signatures for SEDI.

### 4.9 A tension between the statute and Sam's privacy doctrine

The statute requires "cross-context correlation protections" (§301(1)(a)) and defines cross-context correlation as "the ability of a person to link, associate, or infer that the presentation of a state-endorsed digital identity" relates to the same individual (§63A-20-201(1)). Sam's decks argue that cryptographic unlinkability is the wrong goal (§5.3). These are reconcilable, and the reconciliation is the bible's existing layered account (bible 06 §4): the statute asks for protection, not for a specific mechanism, and KERI supplies it through bulk issuance, blinded registries, contractually protected disclosure and the duty of loyalty, rather than through ZKP unlinkability of the issuer. A reviewer who reads §301(1)(a) as mandating BBS-style unlinkable signatures is reading in a mechanism the statute does not name. A reviewer who reads Sam's decks as rejecting correlation protection is also wrong; he rejects one mechanism for it.

---

## 5. The no-KERI-light doctrine

Status: in writing, `[P]` in the SEDI decks, where the target is narrower than in speech. In speech, a position shared by Sam, Mayfield, Rayback, the closing panel and a Utah official, which is status and intent only.

### 5.1 What the written sources actually say

The written form of the doctrine is in Sam's 2025 SEDI decks, and its target there is cryptographic unlinkability as a substitute for a comprehensive approach, not partial implementations of KERI. The general principle: "Insufficient half-measure may defeat a sufficient full measure" (`presentations/SEDI_Tradeoff.web.pdf`, slide "Logical Entailment and Policy"). The rationale it rejects: "The best we can do is a slippery slope. It is the rationale used to justify half-measures." (same deck, slide "What is the Policy Goal that defines sufficiency"). The application: "Why crypto un-linkability is a self-defeating half-measure" (same deck, slide title). The deck's subtitle frames the whole argument as "Comprehensive Solutions vs. Incremental Solutions" (title slide).

The principle that would justify applying it to partial KERI is in the later deck, as a survivability maxim: "Remove even one component protecting a vital area and the adversary will target the unprotected area to the exclusion of all else." (`presentations/SecurityThreatsMitigationsSEDI.web.pdf`, slide "Preventing wounds especially fatal wounds").

### 5.2 What the talks add

In speech the doctrine is aimed at partial KERI. Sam, opening the conference: «if you don't have all of KERI, I guarantee you there are vulnerabilities that you'll be exposed to», then «So, no more half measures» and «It's all KERI or no KERI» (caption, State of the KERI Suite file). In his standalone video, the target is named: systems that are «partial KERI or they do some of KERI but not all of KERI stuff», which «leave out important things you need to protect against the AI threat. So they're half measures» (caption, `SAM Its-KERI-or-Surveillance.txt`).

The Swiss e-ID is the named case. Mayfield, during Q&A on the five Ws: Switzerland is «using a KERI-like method for the digital identity program verifiable history», which uses DID verifiable history (did:webvh), and «we don't believe that KERI Light exists in general because you will have to trade off security» (caption, `Thomas Mayfield ｜ KERI Infrastructure & the 5 W's ｜ KERI Conference 2026.txt`). Rayback on did:webvh: «So they tried to do KERI light and now they have to bolt on.», referring to its new witness and watcher sections (caption, `Jonathan Rayback ｜ KERI Bridge to the DID World ｜ KERI Conference 2026.txt`; the speaker of that line may be an audience member). The closing panel: «Anything but real full KERI with all of the five W's is a risk.» for people- and government-scale identifiers (caption, `Ryan Hansen Pannel ｜ What KERI allows us to do that we couldn't before ｜ KERI Conference 2026.txt`; speaker probably Mayfield per `talks-D.md`). A Utah official at the 2025 summit, on the security of state identity systems that must trust each other: «incomplete and half measures with regard to the security of these systems are not acceptable» (caption, `SEDI25 00-10-05--00-16-06-Alan-Fuller.txt`).

### 5.3 The privacy half of the doctrine

The SEDI decks are the fullest written statement of Sam's case against unlinkability-first design, which the bible covers only at the ACDC-spec level (bible 06 §4). The thesis: "KERI/ACDC postulates that the end goal is not unlinkability, but rather unexploitability through the strongest security." (`presentations/SEDI_Tradeoff.web.pdf`, slide "KERI's Paradigm Shift: Security First"). The diagnosis: "The concept of unlinkability is attractive primarily because it purports to provide a largely technological solution" to a problem that is economic, legal, regulatory and social (same deck, slide "The false attraction of unlinkability"). The security cost of ZKP unlinkability for long-lived issuances is the same argument as §4.8: issuer-key compromise cannot be recovered specifically when forged issuances cannot be linked. The alternative is contractually protected disclosure with chain-link confidentiality (same deck; bible 06:68 already covers the mechanism). The 2025 deck also treats the EU wallet's anonymous-credential choice as premature, citing a 2025 result against BBS+ (same deck, slide "Black Magic Crypto is a Security, Policy, and Adoption Risk"). That citation is Sam's reading of a paper not read here.

### 5.4 The author's own reversal

The closing panel records a reversal by the corpus's author, which the coverage report flags as worth keeping. Hardman: «I once proposed a KERI light posture in our ecosystem and there's certain conditions under which you could operate with less than what KERI provides, but I don't think they apply at an ecosystem level. I think that was a mistake.» (caption, Hansen panel file). Two things follow. The doctrine has a scope: the panel's claim is about people-scale and government-scale ecosystems, and Hardman explicitly allows narrower conditions. And the bible should record the reversal as a dated change of position, in the manner of standards.md §3, rather than as a quotation.

### 5.5 What a shibboleth entry would say

The tell is a design that adopts some KERI mechanisms (a hash-chained log, pre-rotation, a key-event history behind a DID document) and omits others (witness receipting under a threshold, verifier-controlled watchers, duplicity detection, delegation). Sam's 2025 property list gives the losses to name, one per omitted part. Without witnesses there is no controller-side availability: "Controller Key state may be made highly available via its own witness pool" (`presentations/SEDI_Tradeoff.web.pdf`, slide "KERI/ACDC Security Properties"). Without watchers the validator loses protection from dead-key attacks: "Validators are protected from dead (stale) key compromise via the first-seen policy enforced by their own watcher network" (same slide). Without duplicity evidence it loses protection from live compromise: "Validators are protected from live key compromise via duplicity evident property with respect to the controller's key state" (same slide; the source has a curly apostrophe). Shared governance between the two networks defeats the split: "Infrastructure must be highly portable, with no shared governance between the controller's witness network and the validator's watcher network." (same slide). The reframing is §5.1's maxim: the adversary targets the omitted part. The honest residual is §5.4: the claim is scoped to ecosystem scale, and its proponents allow that narrower deployments may accept less. Where to put it: bible 07 §6 (DID drift, `bible/07-shibboleths-and-anti-patterns.md`:192), since the named instance is a DID method.

---

## 6. did:webs: KERI's bridge to the DID world

Status: the spec text is a ToIP KSWG specification at v0.10.3, `main` at `2d84ef2b0`. It is not part of the KERI or ACDC spec lines this corpus tracks, so it has no tier marker of its own here; treat it as `[P]`-plus, a specification in its own standards track whose status the talk describes as final draft under review. The bible mentions did:webs nowhere (coverage report §2.9, verified by grep for this note).

### 6.1 What it separates

The spec's framing is the discoverability/verifiability split: "Information about DIDs is still published on the web, but its trustworthiness derives from mechanisms entirely governed by individual DID controllers." (`spec/header.md`, introduction, at `2d84ef2b0`; the source italicizes two phrases). Its root of trust is stated against did:web's: "Unlike did:web, this method's trust is not rooted in DNS, webmasters, X509, and certificate authorities." (`spec/header.md` §Scope; the source sets `did:web` as code). The web host is demoted to a dumb pipe: "any given target system in isolation can be viewed by this method as a dumb, untrusted server of content." (`spec/body.md`, informative note "Target system and KERI verifiability"). Rayback states the same split in speech: did:webs «separates discoverability from verifiability» (caption, Rayback file).

This answers a critique the bible already makes without the answer. Bible 01 §7 says did:web resolves only current key state and so cannot verify historical actions (`bible/01-foundations-and-worldview.md`:139). did:webs resolves through the `keri.cesr` event stream beside `did.json`, so historical key state is available by construction (`spec/body.md` §Target System(s), L120, which requires replacing the trailing `/did.json` with `/keri.cesr`).

### 6.2 Designated aliases: a LID in practice

The spec requires the controller to authorize the web location: the controller "MUST authorize the full did:webs identifier as a designated alias ACDC anchored to the KERI AID" (`spec/body.md` §Create, L287 at `2d84ef2b0`, `did:webs` set as code in the source). In UIT terms (§1.4) this is an aid|lid couplet: the host-and-path name is a human-meaningful identifier legitimized by an anchored authorization in the AID's trust domain. Rayback calls this the differentiator from the other did:web variants, which authorize the host and path only implicitly (caption, Rayback file).

### 6.3 What it excludes

The spec draws the bible's Layer-1/Layer-2 line itself: "the term decentralized trust includes verifiability, confidentiality, and privacy, but excludes veracity of the content." (`spec/header.md`, introduction; the source italicizes the term). The next sentence assigns veracity to "(personal) evaluation of available reputational data and verifiable credentials (VCs)" (same). That is the authenticity/veracity split (bible 06:25) and the reputational trust of UIT §1.5, stated in a DID method spec.

### 6.4 Status and neighbours, from the talk only

Status in speech, April 2026: a final draft «being reviewed at under the KERI stack working group» and «a new IANA media type registered» (caption, Rayback file). did:keri exists but is «mostly stub» and was written before OOBIs (caption, same file). did:webvh is described as working «the other way around», deriving verifiable history from DID-document state rather than deriving the DID document from KERI events (caption, same file), which is the structural form of the KERI-light critique in §5.2. The ACDC spec mentions did:webs once, as a resolver example for SAID namespacing (ACDC spec `main` `f0bd097de`, `spec/spec-body.md`:218). Mining the did:webs spec in full (delegation, `versionId`, BADA rules, the multisig verification-method mapping) is left for a dedicated pass; this note establishes only the doctrinal frame.

---

## 7. KERI's intellectual lineage, as the papers record it

Status: the papers are `[P]` and dated; Sam's narrative of them is caption. Where the papers and the narrative differ, the papers are the record.

### 7.1 Sam's own account

In the State of the KERI Suite talk Sam narrates the path in order: RAET in 2013-2014 («I wrote a protocol called RAET»), Open Reputation («It defined reputation as a modulator for trust for online interactions»), Identity System Essentials («it introduced the concept of self-sovereignty for identity», with the claim «as far as I know, that was the first. And I stole it from Phil.»), the ledger wars («blockchain is too centralized for truly portable identity»), the three R's paper («this is where I defined the concept of pre-rotation»), A DID for Everything, the KERI v1 and v2 whitepapers, GLEIF, UIT, ACDC, SPAC and Sustainable Privacy (all caption, State of the KERI Suite file; summary in `talks-A.md` §2). The claim to have coined the SSI usage of self-sovereign is his assessment and is not tested here.

### 7.2 Open Reputation, 2015

The low-level framework paper is Sam's: "Open Reputation Framework Samuel M. Smith PhD" and "Draft Revision 1.2 2015/05/13" (`whitepapers/open-reputation-low-level-whitepaper.pdf`, title page; read for the header only). The high-level platform paper is by Lincoln Cannon of The World Table, "Draft Revision 1.1 13 May 2015" (`whitepapers/open-reputation-high-level-whitepaper.pdf`, title page). Both predate everything else in this section and are the source the 2016-2022 reputation decks cite on almost every slide. Neither was mined; they are the obvious next read for the reputation chapter.

### 7.3 Identity System Essentials, 2016

Smith and Khovratovich, Evernym, dated 29 March 2016 (`whitepapers/Identity-System-Essentials.pdf`, title page). Three ideas survive into KERI. The cryptonym: "A public identifier, which corresponds to a (potentially confidential) set of attributes, is called a cryptonym." (§Identifiers). The alias as a secondary identifier, the ancestor of the UIT LID: an alias "is a human friendly globally unique string of text that may be associated with an identity in addition to its primary cryptonym." and "It is a secondary identifier." (§Aliases). And control of the identifier as the core of sovereignty: "A key part of sovereignty is control over the identifiers not just the attributes." (§Control over Attributes and Identifiers). The survivability triad that bible 02 uses as KERI's security frame is already here: "Survivability can be broken up into three aspects, these are, susceptibility, vulnerability, and recoverability." (§Security). It reappears unchanged in the 2025 SEDI decks (slide "Survivable Systems: AUVs, Ships, Critical Infrastructure").

Superseded in ISE: its security rests on BFT ledgers. "Using diffuse trust distributed consensus enables the decentralized and highly secure management of many parts of the identity system" (§Hybrid Ledgers). KERI's later doctrine reverses this (UIT §1.2; §7.4 below). The paper is the record of the position Sam held before the ledger wars, and the bible should cite it as such, not as KERI doctrine.

### 7.4 From four R's to three R's, 2017-2018

Sam's talk dates pre-rotation to the 2018 three-R's paper, and the papers confirm it, with one step he does not mention. The 2017 Self-Identifying Data paper lists four: "The four R's of key managment are:" rotation, reproduction, recovery, revocation (`whitepapers/SelfIdentifyingData.md` §Identifier Key Management; the misspelling is the source's), and its Key Recovery and Key Revocation sections are empty headings. Its rotation design is a key list inside the data item, with no pre-commitment. Five months later the DAD paper folds revocation into rotation, "We call these the essential three R's of key management." (`whitepapers/DecentralizedAutonomicData.md` §Key Management), on the argument that revocation without replacement is "the same as revoking and then replacing with a null key." (§Key Rotation). The UIT keeps that rule: a bare key revocation is a rotation to a null key (UIT §4, p.20).

DAD introduces pre-rotation: "The approach presented here is to pre-rotate the DID key and declare the pre-rotation at the inception of the DID." (§Basic Pre-rotation), with the next key in a field named `ensuer`. It also contains the earliest form of witnesses and of the no-ledger argument. Its "Replicants" are redundant log hosts that each allow "one and only one inception event per event history" (§Replayability), and the design rejects a ledger as more than is needed: a distributed consensus ledger "is not the minimally sufficient means of providing this capability" (§Replayability). The paper's abstract calls its pre-rotation and hybrid recovery methods "somewhat novel" (§Abstract). The motto "minimally sufficient means", which Sam repeats in the 2026 talks (`talks-A.md` §2), is this paper's recurring phrase.

### 7.5 A DID for Everything, 2018

Submitted to RWOT VII, Toronto, September 2018, seven presenters (`whitepapers/A_DID_for_everything.md`, front matter). Its contribution to the lineage is chaining: "Data flows may be provenanced via a self-referential blockchain", defined as a list of signed DAD items in which each item carries the identifier and signature of the previous one (§Motivation). Sam's talk calls this the core idea now in ACDC (caption, State of the KERI Suite file). The paper also states the diffuse-trust principles the UIT later lists as zero-trust computing (§Data Provenance; UIT §2.6), while calling zero-trust "a misnomer" because "There is still trust, it is just diffused" (§Data Provenance). KERI's later literature uses zero-trust without that caveat, so the term has moved; the bible should not treat the 2018 objection as current.

### 7.6 Cooperation Beats Aggregation, 2019

RWOT9, version 1.6 dated 2019/11/19 (`whitepapers/CooperationBeatsAggregation.md`, front matter). It supplies the founding sentence (§2.6) and the meta-platform economics. Superseded in it: its closing endorsement of ledgers, "The authors agree that blockchain-anchored decentralized identity infrastructure is one such application." (§Conclusion), written the year the KERI v1 whitepaper argued for doing without one.

### 7.7 What the lineage explains

Each doctrine in the bible has a dated origin in these papers. Security first: ISE's survivability triad (2016), UIT §1.1 (2020). Pre-rotation: DAD (2018), after the four-R's attempt (2017). Witnesses: DAD's Replicants (2018). The no-ledger stance: DAD's minimally-sufficient-means argument (2018), formalized as UIT's three trust bases (2020), after ISE's ledger-based design (2016) and with CBA's ledger endorsement (2019) as a co-authored lag. ACDC chaining: A DID for Everything (2018). Identifier theory, LIDs and reputational trust: UIT (2020), from ISE's aliases (2016). Reputation as the reason for all of it: Open Reputation (2015) and the 2016-2018 decks. The coverage report ranked lineage low priority but useful for explaining why the doctrines exist; the dates above are what make that explanation citable.

---

## 8. The Duplicity Game deck: mostly redundant, one addition

`presentations/DuplicityGame_IIW_2020_A.pdf` (IIW Spring 2020) defines duplicity and contrasts KERI with Certificate Transparency. Both are covered: duplicity's definition and its role at `bible/02-security-model-and-threat-posture.md`:48-52, and the CT contrast at bible 02:40 and `bible/07-shibboleths-and-anti-patterns.md`:106. The deck's definitions match the 2025 SEDI threats deck slide for slide, which reuses them.

The deck's one idea the bible lacks is its ladder of consistency promises, from a local guarantee for one-to-one interactions to a global one for public interactions, and the point that global consistency need only hold when it is checked. The extractor splits those slide lines, so they are quoted here as the fragments that survive: "Global consistency may only matter" and "after A and B need to interact not before." and, on enforcement, "Breaking the promise of global" with "consistency is a provable liability." (deck, Duplicity Game slides for the global-consistency case). A further slide summarizes KERI's composition, again split: "KERI = self-cert root-of-trust + certificate transparency + KA CE +" and "recoverable + post-quantum." (summary slide; KA CE is the extractor's rendering of KA2CE). Recommendation: a short paragraph in bible 02 §3 on lazy global consistency, not a section here.

---

## 9. Negative results, each at a named commit

- The KERI spec `main` at `fbdd4a615` contains no occurrence of "legitimi", "human-meaningful", "human meaningful", "trilemma", "identity assurance", "guardian" or "reputation" (case-insensitive grep of `spec/spec-body.md`; the only "reput" hit is "non-reputable" at L1654, a different word). It also contains no "did:".
- The ACDC spec `main` at `f0bd097de` contains none of "legitimi", "human-meaningful", "human meaningful", "reput", "trilemma", "identity assurance" or "guardian". It mentions did:webs once (L218).
- So the UIT model, the reputation doctrine, identity assurance and guardianship are all outside the specifications. Guardianship lives in schemas and fixtures (bible 05:248) and in the Utah statute; reputation lives in papers and talks.
- The Utah statute at `bakobo/sedi` `91402ae99` contains no occurrence of KERI, ACDC, AID or IAL (the statute is technology-neutral by design; §4.3).

---

## 10. Open questions and gaps

- Bill number. Whether SB 260 in the talks names the 2025 bill, the 2026 bill enacted as Chapter 436, or both (§4.1). Check at le.utah.gov before any chapter uses it.
- Public pin for the statute. This note read the PDF from a private repo. The le.utah.gov page should be fetched and hashed as a web source (proposed below).
- The end of the Tradespace talk. The caption file stops at the start of the identity-assurance section, so the GLEIF analogy and the rest of Sam's identity-assurance argument are unread. The video, or Sam's slides for that talk if they reach the Papers repo, would close this.
- Open Reputation. Both papers were read for their headers only (§7.2). A reputation chapter should mine the low-level framework paper.
- RAET and ZeroTrustRaet. `presentations/ZeroTrustRaet.pdf` (added 2017-07-13) was not read. Sam names RAET as the start of the path; the lineage section rests on his spoken account of it.
- The v1.40 delegation deletion (§1.8). Unexplained; worth asking Sam, through Daniel, only if a chapter relies on it.
- AR_ACDC_Rep (§2.7). If a later deck or paper does show ACDC property graphs as reputation input, it supersedes the finding here.
- did:webs spec. Only its framing was mined (§6). Its delegation, `versionId`, BADA and multisig rules need their own pass, against `2d84ef2b0` or later.

---

## Already in the bible

- Authenticity versus veracity as orthogonal axes, from Hardman's paper: `bible/06-governance-ecosystems-and-interop.md`:25, `bible/01-foundations-and-worldview.md`:153, `keri-doctrine.md`:55. UIT §1.5 is an earlier written form with a dependency ordering the bible lacks (§1.6 here).
- Levels of assurance as a verifier's threshold, and point-in-time assurance in org-vet: `bible/06-governance-ecosystems-and-interop.md`:37-39. The statute's §303(1)(d) is the legislative counterpart (§3.3 here).
- OOBI with MFA, with its boundary: `bible/06-governance-ecosystems-and-interop.md`:41-43. UIT §1.6 is its conceptual ancestor (§1.7 here).
- SEDI through schemas: endorsement not issuance, the four attributes, the credential chain, data loyalty via rules, the `legalPresenceStatus` tension: `bible/06-governance-ecosystems-and-interop.md`:45-57; `bible/05-acdc-and-verifiable-data.md`:242-252; `scenarios/utah-sedi-age-residency.md` §1-§6. The founding right quoted there via `sedi-id/index.md` is confirmed in the enacted statute §63A-20-101(1); the four attributes are confirmed at §63A-20-301(2)(f).
- Unlinkability as a weak, higher-layer property and contractually protected disclosure: `bible/06-governance-ecosystems-and-interop.md`:59-75. Sam's SEDI decks are the fuller written argument (§5.3 here).
- Custodial rotation, the basis of McEwan's escrow remark: `bible/03-key-management-and-identifier-lifecycle.md`:97.
- Anchored signatures, UIT's Rule 1 without the name: `bible/03-key-management-and-identifier-lifecycle.md`:171.
- The alias doctrine, which UIT classifies as the rule for tertiary identifiers: `bible/07-shibboleths-and-anti-patterns.md`:360-366.
- did:web resolving only current key state: `bible/01-foundations-and-worldview.md`:139. did:webs is the answer, absent from the bible (§6.1 here).
- Duplicity and the CT contrast: `bible/02-security-model-and-threat-posture.md`:40, :48-52; `bible/07-shibboleths-and-anti-patterns.md`:106.
- Survivability framing: `bible/02-security-model-and-threat-posture.md`:24-26. ISE §Security (2016) is its earliest written form in the corpus.
- Registrar/observer and no-phone-home: `raw/14-kericonf-2026.md` §1-§2, and bible 10.
- The founding reputation sentence: `raw/13-keri-one-web.md`:40, which cites the About page; its 2019 written source is §2.6 here.
- Absent, verified by grep of `bible/*.md` and `keri-doctrine.md`: LID, legitimized identifier, PAC trilemma, Zooko, trust basis, reputation as a doctrine, reputation by reference or behavior, RAP, cheap pseudonymity, IAL, the statute's rights other than §101(1), digital guardian as a legal role, the duty of loyalty statute, the ombudsperson, half measure, KERI light, did:webvh, did:webs, did:keri, Open Reputation, Identity System Essentials, three R's, A DID for Everything, meta-platform.

---

## Proposed chapter outline

The material does not fit one chapter cleanly. I propose one new chapter for the theory and reputation, sections in three existing chapters for the rest, and a lineage appendix. Reasons follow each item.

### A. New chapter 11, Identifiers, trust bases and reputation

Reason: the identifier theory and the reputation doctrine are the layer the bible's Layer-1/Layer-2 split points to without populating (coverage report §2.10). They are a coherent body of `[P]` theory with a decade of continuity, and splitting them across 01 and 06 would separate the definition of reputational trust from its use. Standards.md §6 forbids creating a chapter unattended; this is a proposal for Daniel.

1. Thesis and status. Thesis: KERI secures identifiers, not identities, and everything human-meaningful or reputational is built on that in a trust domain. Status: entirely `[P]`; no construct here is in a spec (§9). Supports: UIT §1.1 quotes (§1.1 here); negative results (§9).
2. Identity as identifier plus attributes; security first. Supports: §1.1.
3. Three trust bases. Supports: §1.2. Cross-link: 01 §2-3 (autonomic identity), 07 §4 (blockchain tells).
4. The trust domain, LIDs and the aid|lid couplet; primary, secondary and tertiary identifiers. Supports: §1.3-§1.5, ISE aliases (§7.3). Cross-link: 07 §9.4 (aliases), and did:webs designated aliases in 06.
5. Bootstrapping a root AID by well-known reputational association, and its formalization as OOBI with MFA. Supports: §1.7. Cross-link: 06 §1 (OOBI with MFA and its boundary).
6. Reputational trust: authenticity before veracity. Supports: §1.6. Cross-link: 06 §1 (Hardman's split).
7. Reputation as measured behavior: reputes not ratings, context, transitivity; reputation is not a set of credentials. Supports: §2.1-§2.2.
8. Reputation by reference and by behavior; ACDC chains as the carrier for the first. Supports: §2.4 (decks, with Windley caption as status only). Cross-link: 05 (chaining), 10 (presentation registries, since behavior evidence is presentation evidence).
9. Pseudonymity: RAP, and the cheap-pseudonymity problem that identity assurance answers. Supports: §2.5, §3.1.
10. The PAC trilemma and why KERI picks authenticity and confidentiality. Supports: §1.8. Cross-link: 06 §4 (correlation resistance as layered).
11. Load-bearing assumptions and honest residuals: no reputation mechanism is specified or implemented; AR_ACDC_Rep is not a design (§2.7); the end of Sam's assurance argument is unread (§10).

### B. Chapter 06, expand §3 into SEDI: statute, roles and limits

Reason: the coverage report's preferred placement (§2.4), and SEDI is already in 06. The statute, not the talks, should be the spine.

1. Which law: Chapter 436, 2026 General Session, effective 2026-05-06; the bill-number hazard. Supports: §4.1.
2. The bill of rights, all eleven, with the five that constrain design called out. Supports: §4.2.
3. The statute's requirements read as KERI properties, with the counterweight that the statute is technology-neutral. Supports: §4.3.
4. Identity proofing at a point in time; assurance as accumulated weak bindings. Supports: §3.1-§3.3.
5. Guardianship as a legal role and its KERI mechanisms (multisig, delegated chains, glass-break). Supports: §4.4. Cross-link: 05:248, 08 (delegation in presentations), `scenarios/` (a guardianship scenario, proposed by the coverage report).
6. Wallets, verifiers, relying parties and the duty of loyalty; enforcement through the ombudsperson and attorney general. Supports: §4.4-§4.5. Cross-link: 06 §4 (data loyalty as a layer).
7. The state's self-limits and roadmap items that are not law (wallet attestation, personas). Supports: §4.6-§4.7, all caption, marked as intent.
8. Sam's issuer-side threat model and the case for anchored, linkable issuance at state scale; the reconciliation with the statute's correlation-protection requirement. Supports: §4.8-§4.9. Cross-link: 10 (presentation registries), raw/14 (registrar/observer).

### C. Chapter 06, new section on bridges to foreign identifier systems: did:webs

Reason: coverage report §2.9; 06 already holds interop. It should be mined from the spec, which this note only begins.

1. Discoverability versus verifiability; the web host as untrusted pipe. Supports: §6.1.
2. Designated aliases as a LID in practice. Supports: §6.2, cross-link to chapter 11 §4.
3. Veracity excluded from decentralized trust. Supports: §6.3.
4. Status and neighbours (did:keri, did:webvh), labelled as caption. Supports: §6.4.
5. Answering 01 §7's did:web critique. Cross-link: `bible/01-foundations-and-worldview.md`:139.

### D. Chapter 07, new shibboleth under §6: we will take the parts of KERI we need

Reason: coverage report §2.8; the named case is a DID method, so §6 (DID drift) is the right neighbourhood.

1. The tell. Supports: §5.2 (captions, as status).
2. Why it is a category error: the adversary targets the omitted part. Supports: §5.1 (written maxim).
3. What each omitted part costs. Supports: §5.5 (Sam's property list).
4. The reframing, and the privacy variant (unlinkability as a half-measure). Supports: §5.3.
5. Honest residual: scoped to ecosystem scale; Hardman's dated reversal. Supports: §5.4.

### E. Appendix to chapter 01: where the doctrines came from

Reason: lineage is low priority but explains the doctrines; an appendix keeps it out of the argument while making it citable. Supports: §7.1-§7.7, with dates. Cross-links: 02 (survivability), 03 (pre-rotation), 05 (chaining), chapter 11.

### F. Chapter 02, one paragraph on lazy global consistency

Supports: §8. Not a section.

---

## Proposed sources.yaml entries

Not applied. The `smithsamuelm-papers` entry already exists as a `gh-repo` source watching only `kram.md`; since the repo is now cloned locally at `wot/Papers`, the cleaner change is a `git` entry, with the existing KRAM watch folded in by whoever reviews the manifest. `branches`, `chapters` and `tier` are reviewed fields; everything here is a proposal for the PR body.

```yaml
  - id: papers-identity
    kind: git
    path: wot/Papers
    remote: origin
    watch:
      - whitepapers/UniversalIdentifierTheory.pdf
      - whitepapers/IdentifierTheory_web.pdf
      - whitepapers/Identity-System-Essentials.pdf
      - whitepapers/IdentityAndReputation.md
      - whitepapers/SelfIdentifyingData.md
      - whitepapers/DecentralizedAutonomicData.md
      - whitepapers/A_DID_for_everything.md
      - whitepapers/CooperationBeatsAggregation.md
      - whitepapers/open-reputation-low-level-whitepaper.pdf
      - whitepapers/open-reputation-high-level-whitepaper.pdf
      - presentations/ReputationAlgorithms.pdf
      - presentations/ReputationIIW2017.pdf
      - presentations/ReputationDisintermediation_IIW_20180405.pdf
      - presentations/AR_ACDC_Rep.web.pdf
      - presentations/SEDI_Tradeoff.web.pdf
      - presentations/SecurityThreatsMitigationsSEDI.web.pdf
      - presentations/DuplicityGame_IIW_2020_A.pdf
    tier: cold
    branches:
      - {name: master, role: standardizing, marker: "[P]",
         last_scanned: {commit: b47f21597, date: 2026-10-14},
         last_mined:   {commit: b47f21597, date: 2026-10-14}}
    feeds: [raw/20-identity-theory-reputation-sedi.md]
    chapters: ["01", "02", "06", "07"]
    caveat: >-
      Sam's whitepapers and decks: author's positions, never normative. PDFs are read through
      pdftotext, so a quote can be split by the extractor; cite the page or slide, not a line.
      UniversalIdentifierTheory.pdf and IdentifierTheory_web.pdf are the same blob (c39bd46) since
      e2e995f; v1.32 at 416b7ac was read only for the diff. The open-reputation papers were read for
      their headers only, so last_mined over-claims for them; under-claim by treating them as unread.
      Several papers are co-authored (raw/20 §0.4). Lines in the 2025 SEDI decks are slide bullets.

  - id: utah-sedi-statute
    kind: web
    urls:
      - https://le.utah.gov/xcode/Title63A/Chapter20/63A-20.html
    tier: cold
    feeds: [raw/20-identity-theory-reputation-sedi.md]
    chapters: ["06"]
    caveat: >-
      Utah Code 63A-20, enacted by Chapter 436, 2026 General Session, effective 2026-05-06. Mined
      2026-10-14 from the official PDF C63A-20_2026050620260506.pdf in the private repo bakobo/sedi at
      91402ae99, NOT from this URL, which was not fetched; the first run should hash the page and
      confirm the text matches before last_mined is recorded here. Law, not a tier: no [N]/[P] marker.
      The talks call it SB 260; the bill number is unverified (raw/20 §4.1).

  - id: did-webs-spec
    kind: git
    path: wot/kswg-did-method-webs-specification
    remote: origin
    watch: [spec/header.md, spec/body.md, spec/terms-definitions]
    tier: warm
    branches:
      - {name: main, role: standardizing, marker: "[P]",
         last_scanned: {commit: 2d84ef2b0, date: 2026-10-14},
         last_mined:   {commit: 2d84ef2b0, date: 2026-10-14}}
    feeds: [raw/20-identity-theory-reputation-sedi.md]
    chapters: ["01", "06"]
    caveat: >-
      ToIP KSWG did:webs spec, v0.10.3 at this pin. Mined for its framing only (raw/20 §6); delegation,
      versionId, BADA and multisig rules are unread, so last_mined covers header.md and the cited
      body.md passages, not the whole spec. Its own standards track, so the [N] marker would mislead.
```

Proposed change to an existing entry, also not applied: `conf26-subtitles` should add `raw/20-identity-theory-reputation-sedi.md` to `feeds` and `"07"` to `chapters`, and its `last_scanned` should move to `006042d39`. Its `last_mined` stays `unknown` for the commit, because raw/14 was mined without one; this note was read at `006042d39`, which the reviewer may record if they accept the per-note pin.
