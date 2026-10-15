# Doctrine Mining: ACDCs as authorization, delegated authority, and KERI for AI agents

Primary sources (Sam Smith, `SmithSamuelM/Papers`, cloned at `/home/daniel/code/wot/Papers`, branch `master`, HEAD `b47f21597`; every Papers quote below is pinned to that commit). Last commit touching each file, and first commit, so supersession can be judged:

- `presentations/AuthorizationEVAC.pdf`, deck titled ACDCs for Delegable Authorization. Added and last touched `3ec04c2` (2026-04-30), one week after KERIConf26; it is the deck behind the talk The Future of KERI. Cited by page.
- `presentations/KERI_AI_Cyber_2026.pdf`, deck titled KERI: The last best hope for individual-controlled digital ID in an AI world. Added and last touched `b218b5b` (2026-06-29). It is a question list, not a position paper: most slides pose questions that the spoken video answers. Cited by page.
- `presentations/KERI_AlphaOmega.20250903.pdf`, general overview deck, `e0b2718` (2025-09-03). Relevant pages only (p4, p30, p47-48, p54).
- `presentations/AuthenticDataSupplyChains_DAD_Arch.web.pdf`, `c949ebc` (2022-05-20). Relevant pages only (p10-13). Lineage, not current doctrine.
- `whitepapers/Revocation.md`, self-versioned "V0.4 2026/06/13", commits `6fc4a63` and `3854b8d` (both 2026-06-14). The newest written source here.
- `whitepapers/KERIArchGroupIssuance.md` (KAGI), first `2025-01-30`, last `e8a56a9` (2025-02-05). Its KRAM half is already mined in `raw/15-kram.md` (as keripy discussion #934); this note takes only the group-issuance half.
- `whitepapers/ManyCubed.md`, last `667c79b` (2017-07-13). Lineage only.
- `whitepapers/VC_Enhancement_Strategy.md`, self-versioned 1.2.8, last `4b32dd0` (2022-04-04). Two passages only.
- `whitepapers/XORA.md`, self-versioned 0.04, last `6ca3181` (2022-02-28). Checked for relevance: one sentence touches revocation; otherwise out of scope.

Daniel Hardman, The Shape of Delegated Authority, `sda.md` in `dhh1128/papers` (local `/home/daniel/code/me/papers`), repo HEAD `68a5e2f76`, file last changed `24c18bb` (2026-07-30); front matter says version 1.2, revision 2026-07-14, first dated 2026-07-11.

Specification and code checked for tier: `kswg-acdc-specification` `main` @`f0bd097de` and `v1.1` @`2362e48a1` (both the manifest pins; `upstream/v1.1` re-fetched 2026-10-14 and unmoved). keripy `main` @`80f77b73b` (the bible pin), with a negative search repeated at local HEAD `0f1966f88` (2026-10-08).

Spoken sources: KERIConf26 edited captions, `keri-foundation/CONF26-subtitles` HEAD `006042d39`, joined text in `.ignored/conf26/text/`. Talks used: Samuel Smith, The Future of KERI; Phil Feairheller, ACDCs for Authorization; Cole Davis, Contract Credentials & Verifiable Identity; Alan Davies, ACDCs for Enterprises; Daniel Hardman, Open Verifiable Communications; the Ryan Hansen panel. Also Sam Smith's standalone video It's KERI or Surveillance, whose caption text sits in `.ignored/conf26/text/SAM Its-KERI-or-Surveillance.txt` but comes from `keri-foundation/recordings-and-subtitles` (`subtitles/sam-smith/`), which is not cloned locally; its pin is unknown. Caption locators below are byte offsets into the joined text file, because the talks carry no section structure.

Mining date: 2026-10-14. Worker role mine-authz.

---

## 0. Provenance notes, read before citing

Everything about EVAC, reversion of authority, the registry transfer event and agentic control is [proposal], and Sam says so himself. In The Future of KERI he calls EVAC a proposal whose white paper he has started but not published (caption, byte ~7800), calls reversion of authority not written up in the spec but an easy modification (byte ~16300), and proposes the transfer event for version 1.1 of the ACDC spec (byte ~24400). Those are caption paraphrases, usable for status and intent only (standards §2). The written source for the same material is the deck `AuthorizationEVAC.pdf`, and it is slide text, not specification prose.

One written source states a proposal as fact, and that is a hazard. `Revocation.md` (June 2026) says, in present tense, that registry control "can be transferred via a transfer event in the registry." (§Proofing Applied to Revocation Registries, L118). No such event exists in either ACDC branch: the registry event table at `main` @`f0bd097de` lists exactly `rip`, `bup` and `upd` (L1958-1960), and `v1.1` @`2362e48a1` lists the same three (L2159-2161). keripy has no `xfr` or `rxr` at `80f77b73b` or at `0f1966f88` (a case-insensitive `git grep` over `src` for xfr, rxr, transfer registry and TransferEvent, zero hits). A reader must not take the Revocation.md sentence as evidence that transfer exists. The only spec trace is the reserved-field description for `rd`, which already anticipates the category: "Issuance and/or revocation, transfer, retraction, or usage registry for ACDC when not at top-level" (`main` L48). That is a label, not a mechanism.

The part of this story that is normative is the bound blinded attribute block, which reached `main` [spec] and keripy's data structures [code]; see §4.1. Everything built on top of it is [proposal].

The AI-agent material is advocacy, and the corpus should carry it as Sam's assessment. The written source (`KERI_AI_Cyber_2026.pdf`) is a list of questions prompted by a Five Eyes statement; its answers exist only in the video's captions. The coverage report (`.ignored/coverage-gaps-2026-10.md` §2.5) already cautions that the Five Eyes advisory and the OWASP report it leans on were not checked; they were not checked here either.

Daniel Hardman is both an author of a source here (`sda.md`) and the bible's owner. `sda.md` is an authored position, not KERI doctrine, and on one point (§10.3) it is stricter than KERI's own registry design. Treat it as a peer framework the chapter can cite, not as the community's view.

House-style note: per the mining brief this file uses no bold or italics, and straight double quotes only for verbatim quotations. Caption material is paraphrased, never quoted.

---

## 1. The thesis: ACDCs carry authority across trust domains without loss

The deck's framing slide sets two chains side by side. [proposal] "perpetual identity → perpetual issuances → lossless trust transfer (KERI Suite)" against "ephemeral identity → ephemeral issuances → lossy trust transfer (DNS/CA, OAuth/OIDC)" (`AuthorizationEVAC.pdf` p4). The conclusion drawn on the same slide is the doctrinal hook for this whole note: "ACDC lossless conveyor of trust → bridging ephemeral trust domains" and "eliminates recursive privilege escalation attack vulnerabilities" (p4).

The property list that makes an ACDC graph usable as an authority structure is stated on p3 as a single line: "Delegable Attenuable Aggrable Revocable Transferable Authority", followed by "High Fidelity Modeling of Real World Authority Structures" (p3). Compare the September 2025 overview deck, which had the first half of that list and not the second: "This provides TADAAA! (tail authenticated, delegated, attenuable, aggregable authorization)" (`KERI_AlphaOmega.20250903.pdf` p30). Revocable and Transferable were added between September 2025 and April 2026, and they are exactly the two properties the broken-chain proposals in §4 exist to deliver. That is the most compact evidence that §4 is new thinking, not a repackaging.

Recursive privilege escalation attack (RPEA) is the named threat. The deck asserts elimination; the spoken argument (caption, The Future of KERI, byte ~2600 and ~7700) is that systems unable to bridge trust domains respond by enlarging one domain, and that strong mutual authentication at every edge leaves no foothold to escalate from. Status: Sam's assessment, [proposal]. No written source in this set defines RPEA formally; that is a gap (§12).

The idea is older than the name. In 2017 Sam described the perimeter failure in the same shape: "Any mechanism that allows for lower priviledged users to access a network layer provides an attack vector for that user to elevate their priviledges" (`ManyCubed.md` §Security), with per-flow authentication as the cure: "Escalation opportunities are minimized." (§Security). The 2026 contribution is the claim that ACDCs, rather than per-flow channel security, are the bridging mechanism.

Keys at the edge removes the intermediary class entirely: "With KERI, each AID controller is its own identity provider" and "No third-party IdPs, no relying parties, no trusted intermediaries" (`AuthorizationEVAC.pdf` p5).

## 2. EVAC: Edge Verifiable Access Control

### 2.1 The rule

[proposal] "Authorization to access a resource is granted by the resource's controller (authority)" (`AuthorizationEVAC.pdf` p6). Every node in an ACDC graph can play both roles: "Each Issuer in an ACDC graph may be both a resource authority and an edge." (p6). Impersonation is prevented by authentication at both ends: "Mutually authenticated edge (accessor) and authority prevent impersonation attacks" (p6).

### 2.2 The mechanism

An EVAC authorization is an ordinary ACDC whose attribute section carries a resource map. The slide's field list for the attribute block is "SAID UUID Issuee AID Registry Resource Map" followed by rows `route1 capabilities1`, `route2 capabilities2` (p14). The slide adds that the same section "could convey a policy engine rule set" (p14). The spoken gloss (caption, byte ~8000 onward) likens the route-plus-capability rows to object capabilities with read, write and execute. The attribute-section `Registry` field is the issuee's registry, distinct from the top-level issuer `rd`; Sam says in the talk that it is already in the spec though rarely read. The spec does allow an `rd` nested inside `a` ("the presence of registry SAID, `rd` field inside the attribute, `a`, section may better facilitate contractually protected disclosure", `main` L326), but its stated purpose there is bulk-issuance disclosure, not an issuee usage registry. The talk's claim is therefore stronger than the spec text; record it as [proposal].

Two registries back an EVAC grant (p15, p16). The issuance registry is the issuer's ordinary blindable TEL, served by a Registrar and cached by a verifier's Observer. The usage registry is the issuee's, and every presentation is anchored there: "ACDC Issuee Presentation state is verifiably bound to Issuee’s key state despite rotations" (p16). This is the presentation registry of `bible/10-presentation-registries.md` (Sam's earlier name, issuee usage registry, keripy #1095), applied to access control. EVAC adds no new registry type; it composes two that already exist in the corpus.

### 2.3 Where it stands

[proposal] throughout. EVAC appears in neither ACDC branch (`grep -i evac` over `spec-body.md` at both pins, zero hits) nor in keripy `src` at `80f77b73b`. The white paper is unpublished (caption, byte ~7800). Enforcement of least privilege rests with the verifier or a policy engine it consults (caption, byte ~37700, answering Ned Smith); nothing in the written sources specifies how a verifier evaluates a resource map against a request.

## 3. Delegated authority through credential chains: the normative baseline

### 3.1 What the spec already says [spec]

The issuee field is what turns an ACDC from authentic data into authority: "the Issuer MAY use the ACDC as a contractual vehicle for conveying authorization to the Issuee." (ACDC `main` @`f0bd097de` §Attribute section, L324). The chain follows directly: "an Issuer MAY delegate authority to an Issuee who MAY then become a verifiably authorized Issuer" (L324), with attenuation named in the same sentence. The edge section closes the loop: "A common use case of a chain-of-authority is a delegation chain for authorization." (L1203). Untargeted ACDCs are explicitly not authorizations: an Untargeted ACDC is "not authentic data as an authorization or entitlement to a specified party" (L334). These are the citations a chapter should use for the [spec] floor, ahead of any deck.

### 3.2 Revocation propagates down the chain

The vLEI slides state the propagation rule: "Anyone in the chain-of-authority can revoke the credential issued-by them." and "This breaks the chain and thereby may invalidate any authorizations or attestations that are chained from their credential." (`KERI_AlphaOmega.20250903.pdf` p48). Note the hedge, "may invalidate". Whether downstream issuances survive a broken link is exactly the open problem §4 attacks.

Cole Davis's demo (caption, Contract Credentials, byte ~29490) shows the same cascade from a lease to a self-issued access credential to a smart lock. He states that his demo was a simulation, not the real KERI stack (caption, byte ~21070), so it is illustration, not evidence of implementation.

### 3.3 Why X.509 cannot do this

The overview deck quotes the X.509 article it cites: "Delegation of authority within an organization cannot be handled at all, as in common business practice." (`KERI_AlphaOmega.20250903.pdf` p54, sourced on the slide to en.wikipedia.org/wiki/X.509). That is Sam relaying Wikipedia, not a surveyed result; a chapter should cite it as his framing or find the primary.

### 3.4 Lineage: transfer versus delegation

The 2022 DAD deck already separated the two control operations EVAC depends on: "Transfer of control (non-revokable)." and "Delegation of identifier (revokable). This creates a new identifier with its own set of" keys (`AuthenticDataSupplyChains_DAD_Arch.web.pdf` p10). The 2026 registry transfer event in §4.3 is that distinction applied one layer up, to TELs.

## 4. Broken delegation chains: bound state, reversion, transfer

The problem as Sam poses it: "When a delegatee's authority to issue authorizations is revoked, what is the status of any authorizations/entitlements issued before the authority was revoked?" (`AuthorizationEVAC.pdf` p17). And the verifier's version: "How can a validator securely verify the status of prior valid issuances" once the chain of authority is broken (p17).

Three answers are offered, in increasing order of novelty.

### 4.1 Bound blinded state registry [spec] and [code]

The bound blinded attribute block adds two fields, `bn` and `bd`, binding each registry state update to the issuee's key state at the time of the update. Its purpose, in the specification's words: "The purpose of the bound blinded attribute block is to better support chains of authority using delegated chained ACDCs." (ACDC `main` §Bound Blinded Attribute Block, L2433). It proves that a delegate "had an authorization to issue its own delegated ACDCs, which authorization had been issued but not yet been revoked at the time of anchoring" (L2433). The same section is at `v1.1` L2628-2634. In keripy the structure exists: `BoundState = namedtuple("BoundState", 'd u td ts bn bd')` (`src/keri/core/structing.py:102` @`80f77b73b`), with the comment "bn = bound issuee key event hex sequence number bnh at time of state update" (:99). That is [code] for the data structure only; this pass did not check whether any verifier walks a chain using it.

The deck labels the result "Breaking the chain-of-authority while preserving validity of prior valid issuances" (`AuthorizationEVAC.pdf` p18). Its limit, from the talk (caption, byte ~16000): issuances made by a revoked delegate stay valid but can no longer be dynamically revoked by anyone, so they must be given expirations. Sam's example was a food-handler permit.

### 4.2 Reversion of authority [proposal]

When a delegate is revoked, responsibility for its still-valid issuances reverts to the delegator through the chaining edge: "Reverting authority to delegator when delegatee's authority is revoked" (`AuthorizationEVAC.pdf` p19). The spoken claim is that reversion can ascend the chain any number of levels (caption, byte ~18000). Status: not in either spec branch (`grep -i -E 'revert|reversion'` over both `spec-body.md` pins, zero hits), not in keripy. Sam calls it an easy modification of the spec (caption, byte ~16300); that is his estimate, not a measured one.

### 4.3 Registry transfer event [proposal]

Transfer differs from reversion in where control lands: "Replace the controller of registry without reverting the authority to delegator" (`AuthorizationEVAC.pdf` p20). The deck notes that KERI can already do this the heavy way: "Key rotation can already transfer control of AID and hence registry to new controllers" (p20). The proposal is a lighter, registry-scoped event: "New registry transfer xfr event to transfer control of registry only." (p20). The same slide's diagram names it "Registry Blinded Transfer Event (rxr)" with fields `v t d i rd n p dt` (p20). So the written source carries two different ilks, `xfr` in the bullet and `rxr` on the diagram, which is an inconsistency a spec draft would have to settle.

In the talk Sam treats the TEL as gaining a pair of meta-control events, inception and transfer, analogous to a KEL's inception and rotation, and says validators would check approval by both the reverting and the new authority (caption, byte ~19100 to ~19700). He targets ACDC v1.1 (byte ~24400). At `v1.1` @`2362e48a1` it has not landed (§0). The motivating cases are spoken only: QVI exit, where Karla McKenna said GLEIF had been considering taking control rather than relying on a fixed grace period (byte ~25300); guardianship after divorce; a fired purchasing agent. Status for all three: intent, not design.

Who else named it. The Ryan Hansen panel includes a remark that the transfer registry primitive will unlock new opportunities (caption, byte ~14544). The coverage report attributes this to Hardman; the caption does not make the speaker unambiguous, so leave it unattributed.

### 4.4 The supersession question

`Revocation.md` (two months after the deck) writes about transfer as settled (§0). Read that as drift in an informal paper, not as evidence the proposal advanced. If a later spec commit adds the event, record the upgrade then.

## 5. Revocation doctrine (Revocation.md, V0.4, June 2026)

This is the most substantial new written doctrine in the set, and the bible does not have it. It is framed for SEDI but its arguments are general. All [proposal].

### 5.1 Dynamic revocation is mandatory for long-lived entitlements

"with rare exception, if any, as a matter of policy, if not law, all state issuances MUST be revocable." (§Revocability Properties, L35). Short-lived credentials do not escape this, because automatic reissuance recreates the long-lived entitlement: "the automatic reissuance of repeated instances provides an ersatz long-lived issuance that requires dynamic revocability nonetheless." (L27). Suspension is treated as a subset of dynamic revocation, implementable either as binary revoke-and-reissue or as an m-ary state (L29).

### 5.2 Bare signatures force revocation, and federation is the workaround

The core argument: "when the authenticity proofing mechanism is a bare attached digital signature, all issuances must be revocable, and are forceably revoked whenever the keys are rotated." (§Proofing Mechanism Tradespace, L70). The metaphor: "digital signatures are like signing in dissappearing ink that fades over time due to exposure to air." (L74).

From that, a causal account of OAuth/OIDC that the bible's anti-pattern section lacks. Hiding reissuance behind phone-home verification "is the driver behind the architecture of federated identity systems such as OAuth/OIDC, that consistes of identity providers (IdPs) and relying parties." (L76). And "the practical problems of automated reissuance that arise from using bare attached signatures as the proofing mechanism drives the system architecture to be more centralized." (L76). The bible currently says federation is bad (`bible/07-shibboleths-and-anti-patterns.md:174-180`); this says why it arose, which is the stronger argument and the one that explains what a bridge (§8) must not reintroduce.

Anchored issuance is the fix, and it changes the issuer's economics: "Issuances themselves are not individually signed; a hash of the issuance is anchored in the log." (L94).

### 5.3 Registry design: one registry per issuance, not a bitstring

Against bitstring status lists: "A bitstring encodes the status of all issuances into a single data structure. This co-mingles the governance." (L106). ACDC's alternative: "ACDCs use independent registries, one per issuance. The registries are vacuous at creation; they are not bound to any specific issuance." (L110). And the inversion that a reviewer should be able to state: "ACDCs are not signed; they are bound (anchored) to a registry, which in turn is bound (anchored) to a KEL." (L114). This matches the bible's anchoring doctrine (`bible/05-acdc-and-verifiable-data.md` §9) and adds the anti-bitstring argument it lacks.

### 5.4 Unlinkability, ZKPs and revocation

The sharpest claim in the paper, and the one most likely to draw outsider objection: "Therefore, unlinkability is largely an exercise in privacy theater." (§Tradespace of Proofing mechanisms, L190). He does not dismiss it outright; he keeps it as an adoption requirement in the same paragraph. On ZKP credentials: "So revocation requirements alone obviate one of the main reasons to use anonymous signatures as a proofing mechanism." (L192). And a verdict stated as a censure: "Verifiable credential systems that ignore the ephemerality problem of bare attached signatures, including ZkP anonymous signatures, are fundamentally flawed from a security perspective." (L186). That is Sam's assessment; the chapter must present it as such and pair it with the counter-position that the paper does not engage (accumulator-based revocation is dismissed on performance grounds at L192 with no citation).

The replacement is bulk issuance with herd-private bulk registry updates: "Each member of a bulk-issued set has its own revocation registry, and the Issuer bulk-updates its revocation registries across all citizens" (L198). The EVAC deck's bulk-issuance slides make the same point with a single sparse-Merkle-tree seal per batch (`AuthorizationEVAC.pdf` p30-32); `bible/05` §9 already has the bulk-update-as-privacy claim from captions.

XORA (2022) once proposed an accumulator route: selective disclosure mechanisms "and/or a revocation registry of one-time-use ACDCs" (`XORA.md` §XORA as a Cryptographic Accumulator, L105). Revocation.md's dismissal of accumulators supersedes it as Sam's current position.

### 5.5 Control first, accountability, and duty of loyalty

"the principal property of a digital identity can't be privacy first; it must be control first." (§Privacy, L165). Perpetual identity is what makes accountability possible: "If one can abandon an identity at will to avoid accountability, then that identity is not reputable." (§Control over Value, L157). The contract-law premise behind accountability is stated plainly: "A valid contract needs 1) an agreement, 2) an exchange of consideration, and 3) an intention to create legal relations." (L155). The downstream mechanism: "chain-link confidentiality attaches strings to the downstream use of disclosed data. With ACDCs, these strings are cryptographically verifiable." (§Bulk Issuance and Duty-of-Data-Loyalty Enforcement, L206).

## 6. Group issuance architecture (KAGI, February 2025)

KAGI's KRAM material is in `raw/15`. What follows is the part about who issues when the issuer is a group, which is an authorization question.

### 6.1 Group membership is private by default

"the KEL does not publicize the single-sig member AIDs that contribute to a group multi-sig AID." (§Group Multi-Sig AID, L61). Where publicity is wanted, the group discloses by credential, "for the group multi-sig AID to issue an ACDC that discloses its member AIDs at the time of its issuance" (L65), revoked and reissued when membership changes. That declaration is not optional decoration in the joint-issuance design: "The AID member list declaration ACDC is really just a more normative discovery mechanism that avoids an ambiguity attack." (§Joint Issued ACDCs).

### 6.2 Anchoring versus signing as an authorization choice

"KERI supports non-ephemeral authentication by binding issuances to the key state at the time of issuance via seals (anchors) in the KEL" (§KEL Sealed (Anchored) Issuances). The cost is operational and lands on the access-control layer: "perimeter protection mechanisms now have to walk KELs to look up and find anchors" (same section). The suggested hybrid is an ephemerally signed wrapper around an anchored payload, so a load balancer can drop cheaply while the threshold protects the content.

### 6.3 Agents in negotiation, 2025 version

KAGI already has the agent-as-delegate pattern, a year before the AI framing: "Avoid multi-sig on each stage of IPEX by using a delegated agent" (§Agent Delegated Negotiation). The safety rule is that an agent's output binds the group only through an anchored authorization: "Agent-issued `agree` for one side and `grant` for the other are valid only if they include a verifiable reference to a corresponding anchored ACDC." (same section). "This protects the group members from malicious agents." (same section). The design driver, credited to a point Hardman raised: "Validation (which includes business logic and cryptographic verification) may be largely automatable, whereas signing requires human intervention." (§Other Options). This is the earliest written source in the set for agents acting under ACDC-granted authority, and it predates the agentic-AI framing of §9.

### 6.4 Joint issuance

"Joint issuance is a new concept." (§Joint Issued ACDCs). Each member issues its own copy, and a validator requires a threshold of copies identical below the top level, with the threshold fixed by a designated key state of the group AID. "joint ssuances by the group are a set of single-sig issuances anchored separately in each members KELs/TELs" (same section, typo in source). `sda.md` §8 treats joint issuance as the mechanism for a threshold root of authority (§10.4 below), citing the dossier work. Status: [proposal] in KAGI; whether the dossier specification makes it normative was not checked in this pass (the coverage report §2.11 flags the same gap).

## 7. Contract credentials and execution trust

Both are spoken only, [proposal] at best, and the chapter should treat them as applied patterns, not doctrine.

Contract credentials (Cole Davis, caption): a credential derived one-to-one from a legal contract, with the legal prose or its SAID in the rules section, deal points in attributes, and edges composing authority; the lessee issues itself an access credential under an `I2I` edge; termination of the lease revokes everything downstream. The normative hook is real and already cited in §3.1, the spec's "contractual vehicle for conveying authorization" (ACDC `main` L324). Davis's own caveat (caption) is that he could not stand up the real stack and simulated it.

Execution trust (Alan Davies, caption): a verification gate inserted immediately before a high-value action in an existing system, wrapping the request in an ACDC signed by the authorized party, as the near-term wedge toward a signed-intent world. Its doctrinal content is the point of verification, at execution rather than at login, which is the same move `sda.md` makes when it recomputes the gate at the execution boundary (§10.5). Davies's long-run vision has device-resident AI agents signing each request; that is a vendor's forecast.

OVC delegated signer (Hardman, caption): an enterprise's fourth credential delegates the right to sign calls to a platform (Infobip, Twilio, Vonage named), and a transit carrier rejects a call in real time when a credential is revoked. This is the one deployed (proof-of-concept) instance of chained delegated authority in the conference set; detail belongs to a telecom scenario.

## 8. Bridges to OAuth, OIDC and UDAP

### 8.1 Sam's position on legacy servers

The written sources put OAuth/OIDC on the lossy side (`AuthorizationEVAC.pdf` p4, quoted in §1) and explain it as the product of ephemeral signatures (`Revocation.md` L76, §5.2). The overview deck dates the shift: "Result: federated identity: IDPs with PKI-DNS/CA, OAuth" for the era before 2015, against "Now: identity based on user-managed private key(s)" (`KERI_AlphaOmega.20250903.pdf` p4). In the talk he concedes that an OAuth server may stay where someone insists on it, on condition that it not be used to expand its trust domain, and that the bridging itself be done with KERI and ACDCs (caption, The Future of KERI, byte ~5175). Status: intent, spoken. That conditional tolerance is not in any written source in this set.

### 8.2 healthKERI's ACDC authorization server (Feairheller)

Spoken only; implementation claims by a vendor, unverified against code. The pattern, from the caption: UDAP dynamic client registration (RFC 7591) carrying an IPEX presentation of a vLEI; server identity published as an OOBI in `.well-known`; the client ID set to the SAID of the presented credential, with no client secret and every subsequent token request signed (byte ~12650); an authorization server that is also an OIDC identity provider, configured by accepted schemas and root issuers, which he calls a distributed identity provider appliance (byte ~18750 and ~19760); key state tracked by a local sidecar watcher, with hourly rotation exercised in a pilot (byte ~14925). His stated lesson is to meet the customer where they are, after their KERI-native gateway (RACK) found no adopters because it was not interoperable (byte ~7000 to ~7700).

### 8.3 The tension the chapter must resolve

`bible/07-shibboleths-and-anti-patterns.md:160` quotes Provenant's applied doctrine as categorical: "We do not use sessions, cookies, tokens, JWTs, OAuth, OIDC, SAML, or any similar technologies to secure calls". healthKERI issues OAuth tokens. These are reconcilable, and the reconciliation is the doctrine: what 07 §5 rejects is the bearer secret and the IdP as trust root, and what the healthKERI bridge removes is exactly those two (no client secret, signed token requests, credential SAID as client identity, verifier-run watcher). The token survives as a compatibility envelope inside one trust domain. Sam's condition in §8.1 is the test: a bridge is sanctioned when it does not enlarge a trust domain. Whether an OAuth access token issued by such a server is itself a bearer token downstream is not addressed in the caption, and is the obvious objection; record it as open (§12).

## 9. KERI for AI agents

### 9.1 Agents need no new mechanism

The deck's agentic slide is the doctrine in five lines: "Agent has its own AID", "Realizes the original meaning of the word agent", "ACDC mechanisms are the same for AI, person, or entity agents.", "Multi-sig enables thresholded group agents", and "Maybe regulations should require attributes that indicate the type of agent. (AI vs person)" (`AuthorizationEVAC.pdf` p7). The slide retitles the acronym Edge Verifiable Agentic Control. The talk adds that an agent receives a delegated AID (caption, byte ~31400). Combined with KAGI's 2025 agent pattern (§6.3), the corpus position is consistent across eighteen months: an AI agent is a delegate, and delegation is already specified. A 07 shibboleth follows directly: the prior that agentic AI needs a new identity primitive.

### 9.2 The KERI-or-surveillance thesis

The written source is a question deck. Its framing contrasts two identities. AI-based identity is a "Digital persona derived from the continuous tracking & statistical correlation of one's behavior and biometric expression." (`KERI_AI_Cyber_2026.pdf` p5), "Inevitably centralized with zero privacy" (p7). KERI-based identity is "fault-tolerant survivable to AI cyber attack." (p6), "decentralized with best possible privacy" (p8). The trigger is a quoted Five Eyes statement: "The timeline is not years, it is months." (p2). The deck asks rather than asserts: "Why do you believe there may be no stable middle ground between these two futures?" (p18), and "Should AI be trusted to protect human freedom," (p21).

The answers are spoken (caption, It's KERI or Surveillance; status and intent only): no stable middle ground exists; current DNS/CA, TLS, OAuth and OIDC systems rest on shared secrets, which feed RPEA; KERI's duplicity evidence cuts breach detection from months to propagation time; an AI agent's authority should be traceable by delegation back to an accountable person; and the control layer around an agent, which he calls safety jackets, must be computationally different from the model it constrains, a point he draws from his autonomous-vehicle work. The written echo of the accountability argument is in Revocation.md: AI and aggregators act "as super correlators to defeat any and all technical attempts at digital anonymity." (L172), so the only real protection is legal recourse.

Assessment boundary. Every one of these is Sam's position. The dichotomy is argued, not demonstrated; the detection-time comparison relies on industry averages he cites aloud without a source in this set; the Five Eyes and OWASP documents were not read here. The chapter should state the thesis as his and give the strongest objection (a mixed regime of cryptographic identity plus behavioural fraud detection is what most deployments will actually run) alongside it.

### 9.3 Lineage of the safety-jacket idea, and a tension

The term predates the AI framing. In 2022: "antifragility comes from supervisory, adaptive, and learning layer safety-jackets." (`VC_Enhancement_Strategy.md` §Dealing With Uncertainty). In 2017 Sam went the other way on behavioural AI: "Dynamic policy modification that uses AI to first profile and detect anamalous behavior and then restrict the authorization of that user prevents discovery." (`ManyCubed.md` §Security), and the 2022 DAD deck kept the principle as "Authorization is behavioral." (`AuthenticDataSupplyChains_DAD_Arch.web.pdf` p13). Behavioural profiling inside one's own infrastructure is not the same thing as behavioural identity across society, so this is not a contradiction. It is a boundary the 2026 thesis leaves implicit, and a reviewer quoting the thesis should know that Sam once recommended AI profiling as an authorization input.

### 9.4 What a world of delegated agents asks

The deck's own closing question for agents: "What would a world look like where every AI agent operates under cryptographically" verifiable "authority by delegation and thus accountability?" (`KERI_AI_Cyber_2026.pdf` p22; the word between the two quoted fragments is damaged by a ligature in the extraction). The upcoming 2026-11 programme reportedly titles a Sam talk on SEDI as bootstrap for AI agent surveillance protection (coverage report §2.4); not verified here.

## 10. The Shape of Delegated Authority (Hardman, v1.2, July 2026)

`sda.md` is the only source in the set that models what an authority is, rather than how it is carried. KERI carries the grant; `sda.md` says what should be in it. It names KERI and ACDC as the identity layer and cites cooperative delegation for construction-time constraints. Authored position, not community doctrine.

### 10.1 The problem statement

The bearer critique already in 07 §5.2 comes from here: "Possession of an API key does not authorize one bounded act" (§1). The bound the paper sets on itself: "Name the category, gate the boundary, audit the remainder" (§1), and "Sincerity stays gate-able and auditable, never provable." (§8).

### 10.2 What it adds that EVAC lacks

EVAC's resource map is a route plus a capability list. `sda.md` locates acts by effect over a kind of state (§4) and carries a separate relationship facet naming principal, relationship type, liable party, presented identity and revocation terms (§5): "Beneficiary, actor, and liable party can be three different parties" (§5). It distinguishes authority to act from authority to authorize, with a containment pattern for orchestrators that matters for agents: "Give a powerful orchestrator broad authority to authorize but an empty act surface, and its blast radius on compromise collapses" (§5). None of this appears in the EVAC deck. A chapter can present EVAC as the transport and `sda.md` as one proposal for the payload, both [proposal].

### 10.3 Open loop, and a tension with KERI's registries

`sda.md` frames credentials versus capabilities as open versus closed loop: "Authority is analyzed by a stranger." (§7). It then sets a rule stricter than KERI's own design: "A registry consulted at verification time is a phone-home in disguise." and "any registry or log is an issuance-time and audit-time convenience, never a verification-time dependency." (§7). The bible already adopts that rule as a shibboleth (`bible/07-shibboleths-and-anti-patterns.md:92-98`).

But EVAC's verifier checks both the issuer's TEL and the issuee's usage registry before honoring an access (§2.2), and `sda.md` §8 itself relies on real-time revocation. Those are reconcilable only through the Observer split, in which the verifier reads its own cache, synced on state change rather than per presentation (ACDC `main` §TEL Registrars and TEL Observers, as quoted at `bible/05-acdc-and-verifiable-data.md:193`). Under that reading, the registry is consulted at verification time, but the party consulted is the verifier's own observer, not the issuer. The literal `sda.md` sentence does not make that distinction, and the 07 row that quotes it does not either. Flag for the chapter: either sharpen the rule to forbid only a verification-time dependency on the issuer, or state that revocation status is the one sanctioned verification-time read. This note does not resolve it.

### 10.4 Threshold root by joint issuance

Joint issuance "lets a grant be satisfied by a weighted threshold of endorsements, each owner signing from their own identifier, asynchronously and with no shared key." (§8). This links §6.4 (KAGI) to a concrete use: the root of an authority chain.

### 10.5 Standing authority

The objection the paper concedes: a persistent grant "is granted once and weighed against the conditions that held at issuance, not those that hold at the moment an act takes effect." (§8). Its answer is per-act derived gates plus real-time revocation, with termination on completion left open. This is the strongest available framing of why EVAC needs dynamic revocation and why §4's broken-chain proposals matter.

### 10.6 Construction-time constraint

"a delegate configured never to sub-delegate produces no sub-delegation any verifier will honor" (§7). This is KERI's `DND` trait read as an authorization control; see `bible/03-key-management-and-identifier-lifecycle.md:120` for the [spec] trait. The talk makes the same point about edges or delegated-AID configuration limiting depth (caption, The Future of KERI; summary at `.ignored/conf26/talks-A.md:187`).

## 11. Lineage summary

2017 (`ManyCubed.md`): perimeter escalation named; every flow authenticated and authorized; AI profiling proposed as a dynamic authorization input. 2022 (DAD deck): transfer versus delegation of control; "Authorization is behavioral." 2022 (`VC_Enhancement_Strategy.md`): safety-jackets in automated reasoning. 2025-02 (KAGI): agent-delegated negotiation, joint issuance, group membership declaration. 2025-09 (AlphaOmega): TADAAA; chain-of-authority revocation. 2026-04 (EVAC deck and talk): EVAC, agentic control, bound blinded state, reversion, transfer. 2026-06 (Revocation.md, AI deck): revocation doctrine and the KERI-or-surveillance framing. 2026-07 (`sda.md`): the shape of the grant.

## 12. Open questions and gaps

1. RPEA has no written definition in this source set. Find one (perhaps in a Sam paper not mined here) before the chapter treats it as a defined attack.
2. The transfer event's ilk is `xfr` in one place and `rxr` in another on the same slide (`AuthorizationEVAC.pdf` p20). Neither is in a spec or keripy.
3. The spoken claim that an issuee registry field is already in the spec (caption) is only partly supported: `main` L326 allows `rd` inside `a` for a different stated purpose. Re-check if v1.1 moves.
4. No source specifies how a verifier evaluates an EVAC resource map against a request, or how reversion is validated recursively.
5. Whether an OAuth access token minted by an ACDC authorization server is a bearer token downstream (§8.3).
6. The `sda.md`/Observer tension (§10.3).
7. Joint issuance's normative status in the dossier specification: not checked.
8. The KERI-or-Surveillance video's subtitle repo is not cloned; pin unknown. Clone `keri-foundation/recordings-and-subtitles` to pin it.
9. healthKERI's implementation claims are spoken; no code was read. If the code is public (the talk says code was donated to the KERI Foundation; see `.ignored/conf26/talks-A.md`, State of the KERI Suite), a later pass should pin it.
10. Whether keripy's `BoundState` is consumed by any chain-walking verifier at `80f77b73b`: not checked.

---

## Already in the bible

- Chain-of-authority structure, edge operators, and the `I2I` misreading: `bible/05-acdc-and-verifiable-data.md:80-104`, `bible/07-shibboleths-and-anti-patterns.md:416-430`. Does not cite ACDC `main` L324 (contractual vehicle for authorization) or L1203 directly as the authorization basis; the new chapter should.
- Registries, TELs, blindable state, Registrar/Observer, bulk updates, usage registries: `bible/05-acdc-and-verifiable-data.md:183-216` and all of `bible/10-presentation-registries.md`. The bound blinded attribute block (`bn`, `bd`) is not mentioned anywhere in `bible/` (grep `bound blind`, zero hits); nor are reversion or transfer.
- Delegation of AIDs and the `DND`/`DID` traits: `bible/03-key-management-and-identifier-lifecycle.md:114-131`.
- GCD as the applied delegation credential: `bible/05-acdc-and-verifiable-data.md:250-252`.
- OAuth/OIDC/bearer/federation as anti-patterns: `bible/07-shibboleths-and-anti-patterns.md:146-190`, including the `sda.md` signet-ring quotes at :160 and :162. No sanctioned-bridge counterpart exists.
- Registry at verification time as anti-pattern, from `sda.md`: `bible/07-shibboleths-and-anti-patterns.md:92-98` (see §10.3 for the tension).
- SD-JWT/OIDC4VC scorecard: `bible/06-governance-ecosystems-and-interop.md:157-177`.
- AI as a subject: absent, per the coverage report §2.5; re-confirmed (`grep -i -E 'agentic|AI agent'` over `bible/`, zero hits).
- Provenance warning: `bible/05-acdc-and-verifiable-data.md:195` and :199-201 quote KERIConf26 captions inside double quotes as Sam's words. Standards §2 says captions are never a quotation. Not this note's file to fix; flagged for the synthesis pass.

## Proposed chapter outline

Recommendation: one new chapter, titled Authority, authorization and agents, with AI agents as a section inside it, not a chapter of their own. The doctrinal content of the agent material is that agents need no new mechanism (§9.1); giving them their own chapter would contradict that. The advocacy half (KERI or surveillance) belongs as a short, caveated section in `bible/01` on why the community frames KERI as the answer to AI-era impersonation, plus one shibboleth in `bible/07`. Status paragraph required: nearly everything past the [spec] baseline is [proposal].

1. Thesis and status. Authority is delegated through credential chains; enforcement is the verifier's; keep trust domains small and bridge them losslessly. Support: §1 (p3, p4 quotes), §3.1 (L324, L1203). Status: [spec] floor, [proposal] superstructure.
2. The normative floor: targeted ACDCs as authorization, chains of authority, attenuation, revocation cascade. Support: §3.1, §3.2. Cross-link `bible/05` §5 and 07 §10.5.
3. Lossless versus lossy trust transfer, and RPEA. Support: §1 (p4, ManyCubed). Mark RPEA undefined in writing (§12 item 1).
4. EVAC: rule, resource map, issuance plus usage registry. Support: §2. Cross-link `bible/10`.
5. Broken chains: bound blinded state [spec][code], reversion [proposal], transfer [proposal], with the `Revocation.md` drift warning. Support: §4, §0. Cross-link `bible/05` §9.
6. Revocation doctrine: why bare signatures force revocation, why federation followed, one registry per issuance, the unlinkability and ZKP critique as Sam's assessment. Support: §5. Cross-link 07 §3 and §5.4.
7. Group and joint issuance, and agents in negotiation. Support: §6, §10.4. Cross-link `raw/15` and `bible/09`.
8. What a grant should contain: the `sda.md` model as one proposal (acts, relationship facet, authority to act versus authorize, standing authority). Support: §10. Flag the §10.3 tension.
9. Agents as delegates. Support: §9.1, §6.3, §10.2. Shibboleth candidate for 07: the prior that agentic AI needs a new identity primitive.
10. Applied patterns: OAuth/OIDC/UDAP bridge (healthKERI), contract credentials, execution trust, OVC delegated signer. Support: §7, §8. Mark all as spoken or vendor claims. Add a pointer from 07 §5 saying the bridge is sanctioned when it removes the bearer secret and does not enlarge a trust domain.
11. Honest residuals. Support: §12.

Cross-links to add in existing chapters: 01 (AI-era framing, §9.2 with its assessment boundary); 03 §8 (`DND` as authorization control, §10.6); 05 §9 (bound blinded attribute block, absent today); 07 §3.2 (the §10.3 tension) and §5 (pointer to the bridge section).

## Proposed sources.yaml entries

Not applied. The `smithsamuelm-papers` change retargets an existing entry, which standards §6 reserves for review.

```yaml
  # Proposed change to an existing entry: the repo is now cloned locally, and
  # more than kram.md is mined. Keep last_mined for kram.md as it was.
  - id: smithsamuelm-papers
    kind: git
    path: wot/Papers
    remote: origin
    watch:
      - whitepapers/kram.md
      - whitepapers/Revocation.md
      - whitepapers/KERIArchGroupIssuance.md
      - presentations/AuthorizationEVAC.pdf
      - presentations/KERI_AI_Cyber_2026.pdf
    tier: warm
    branches:
      - {name: master, role: standardizing, marker: "[proposal]",
         last_scanned: {commit: b47f21597, date: 2026-10-14},
         last_mined:   {commit: b47f21597, date: 2026-10-14}}
    feeds: [raw/15-kram.md, raw/19-authorization-and-agents.md]
    chapters: ["05", "07", "09"]
    caveat: >-
      Sam's whitepapers and decks. All [proposal]. Decks are slide text; quote by page, and
      expect ligature damage in extracted text (fi, ff). Revocation.md states the
      proposed TEL transfer event in present tense; it is not in either ACDC branch.
      KAGI's KRAM half overlaps keripy discussion #934, mined in raw/15.

  # Existing entry: add the new feed only.
  - id: papers
    feeds: [raw/05-papers-priority.md, raw/06-papers-di-drift.md, raw/19-authorization-and-agents.md]

  # Existing entry: add the new feed only.
  - id: conf26-subtitles
    feeds: [raw/14-kericonf-2026.md, raw/19-authorization-and-agents.md]

  # New entry.
  - id: keri-foundation-recordings
    kind: gh-repo
    repo: keri-foundation/recordings-and-subtitles
    branch: main
    watch: [subtitles/sam-smith]
    tier: cold
    branches:
      - {name: main, role: standardizing, marker: "[proposal]",
         last_scanned: {commit: unknown, date: 2026-10-14},
         last_mined:   {commit: unknown, date: 2026-10-14}}
    feeds: [raw/19-authorization-and-agents.md]
    chapters: ["01", "07"]
    caveat: >-
      Edited auto-captions of standalone videos, including It's KERI or Surveillance.
      Same weak provenance class as conf26-subtitles: near-wording only, status and
      intent only. Not cloned when raw/19 was mined, so the pin is unknown; the text
      used came from a pre-joined copy in .ignored/conf26/text/. No LICENSE file
      (raw/14 §0).
```
