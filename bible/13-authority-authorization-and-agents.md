# 13 — Authority, Authorization and Agents {#authority}

## Thesis {#thesis}

KERI carries authority the way it carries everything else: as data whose authenticity a stranger can check from the data and key state alone. A targeted ACDC is the vehicle. Its Issuer conveys authority to its Issuee, the Issuee may become the Issuer of the next ACDC, and the resulting chain of issuer-to-issuee credentials, each anchored in its Issuer's key event log, is the authority. The party asked to honor an act walks that chain itself; no identity provider, token service or authorization server stands between them. That much is specification text. On top of it Sam Smith has built, in 2026, a superstructure of proposals: Edge Verifiable Access Control (EVAC), which turns ACDCs into access grants; a cure for broken delegation chains, in three parts of which one is specified; a revocation doctrine explaining why bare signatures pushed the industry into federation; and an account of AI agents whose whole content is that agents need nothing new, because an agent is a delegate and delegation is already specified.

Three claims organize the chapter. First, two different operations share the word delegation. Delegating an identifier is a KEL operation ([chapter 03, section 8](03-key-management-and-identifier-lifecycle.md#delegation)); delegating authority is an ACDC chain. They compose but are not the same, and a review that confuses them will look for guarantees in the wrong log. Second, authority that must be revocable must be read at verification time, and that does not make it a phone-home. The line falls between fetching state the verifier then checks against key state, which KERI's registry design requires, and asking a service for a verdict, which it forbids ([section 5](#state-not-verdict)). Third, an AI agent is a delegate with its own identifier, acting under authority an accountable party granted and can revoke. Everything else said about agents is advocacy, and the chapter carries it as Sam's assessment.

## Status {#status}

Most of this chapter is [proposal]. The normative floor is narrow and it is all in the ACDC specification's standardizing line: the targeted ACDC as a vehicle for authorization, the chain of authority, attenuation, and the bound blinded attribute block that binds a registry update to the Issuee's key state ([section 1](#normative-floor), [section 6](#broken-chains)). The bound block's data structure is also [code] in keripy at `80f77b73b`; nothing there uses it to judge a downstream issuance.

Everything above the floor is [proposal] or weaker: EVAC, reversion of authority, the registry transfer event, the revocation doctrine of Sam's June 2026 white paper, group issuance, the agent pattern, and the shape-of-authority model in Daniel Hardman's `sda.md`. Sam calls EVAC a proposal whose white paper is unwritten, reversion an unspecified modification, and transfer an addition planned for v1.1 that neither branch carries. Several sources are slide decks and conference captions. Decks are quoted by page from extracted text whose ligatures are damaged; captions are quoted only as the captions read, for intent and framing. The applied patterns in [section 11](#applied-patterns) are vendor and demonstration claims, spoken only, with no code read. The AI material in [section 9](#agents) rests on a deck that asks questions and a video that answers them, and the documents it responds to (a Five Eyes statement and an OWASP report) were not read for this chapter.

Where this chapter overlaps another, it links rather than restates: KEL delegation and its traits are in [chapter 03, section 8](03-key-management-and-identifier-lifecycle.md#delegation); edges, operators, registries, registry transfer and bulk revocation in [chapter 05, section 5](05-acdc-and-verifiable-data.md#edges) and [chapter 05, section 9](05-acdc-and-verifiable-data.md#registries); the Issuee's usage registry in [chapter 10](10-presentation-registries.md#asymmetry).

## 1. The normative floor: a targeted ACDC conveys authority {#normative-floor}

The ACDC specification makes the Issuee field the hinge between authentic data and authority. In a targeted ACDC, "the Issuer MAY use the ACDC as a contractual vehicle for conveying authorization to the Issuee." (ACDC spec > Top-level ACDC Sections > Attribute Section > Attribute Section Variants > Targeted Attribute Section, L324). The same paragraph states the chain and the attenuation in one sentence: "an Issuer MAY delegate authority to an Issuee who MAY then become a verifiably authorized Issuer" who may pass on "that authority (or attenuation of that authority)" (L324). The edge section names the pattern: "A common use case of a chain-of-authority is a delegation chain for authorization." (ACDC spec > Top-level ACDC Sections > Edge Section > Edge > Operator, `o` field, L1203). Both passages are on `v1.1` @`2362e48a1` (L335, L1215) unchanged in substance. [spec]

The converse is also specified, and it is the guard against a common misreading. An untargeted ACDC is "not authentic data as an authorization or entitlement to a specified party" (ACDC spec > Top-level ACDC Sections > Attribute Section > Attribute Section Variants > Untargeted Attribute Section, L334). An untargeted chain carries provenance, not authority; a hybrid chain that ends in untargeted ACDCs carries "delegated authorized attestations" at its head (L334). A reviewer who finds authority being inferred from an untargeted credential has found a defect. [spec]

### What the floor gives a verifier {#floor-guarantees}

Three properties follow from the floor and the anchoring doctrine of [chapter 05, section 9](05-acdc-and-verifiable-data.md#key-state-binding), each with its assumptions. Each link in a chain is attributable to its Issuer's key state at the anchor, so a later rotation by any party does not invalidate the chain, provided the anchors were verified as of their position in each Issuer's log ([chapter 03, section 11](03-key-management-and-identifier-lifecycle.md#as-of-anchor)). Each link is separately revocable by its own Issuer, and revocation propagates downward: keripy raises `RevokedChainError` on a revoked far node ([chapter 05, section 5.1](05-acdc-and-verifiable-data.md#chain-revocation)). And each link names, through its edge operator, how the near node's Issuer must relate to the far node's Issuee; `I2I` is the delegative case ([chapter 05, section 5](05-acdc-and-verifiable-data.md#edges)).

What the floor does not give is as important. The specification does not say how a verifier decides whether an attenuated grant covers a requested act; the rules section carries terms that are not machine-enforced ([chapter 05, section 6](05-acdc-and-verifiable-data.md#rules)). Edge operators check identity relations between adjacent nodes, not multi-hop authority semantics ([chapter 07, section 10.5](07-shibboleths-and-anti-patterns.md#edge-operators)). And what happens to an issuance made by a delegate whose own grant is later revoked is not settled by the propagation rule. Sam's overview deck states the rule with a hedge: revoking a link "breaks the chain and thereby may invalidate any authorizations or attestations that are chained from their credential." (AlphaOmega deck, p48). The word "may" is the open problem [section 6](#broken-chains) addresses.

### The vLEI as the deployed instance {#vlei-instance}

The vLEI chain (GLEIF, Qualified vLEI Issuer, Legal Entity, role credentials) is the deployed instance of this floor, and the overview deck uses it as the example: "Anyone in the chain-of-authority can revoke the credential issued-by them." (AlphaOmega deck, p48). The same deck names the property set the chain exhibits: "This provides TADAAA! (tail authenticated, delegated, attenuable, aggregable authorization)" (AlphaOmega deck, p30). Seven months later the EVAC deck's list had grown to "Delegable Attenuable Aggrable Revocable Transferable Authority" (EVAC deck, p3). The two added properties, revocable and transferable, are the ones the 2026 proposals in [section 6](#broken-chains) exist to deliver, which is the most compact evidence that those proposals are new design rather than a repackaging. [architect]

## 2. Two delegations, one word {#two-delegations}

### Delegating an identifier {#identifier-delegation}

KEL delegation creates a new AID whose inception is approved by a seal in its delegator's log. It is cooperative, two-sided, and it bounds what an attacker gains from compromising either party alone ([chapter 03, section 8](03-key-management-and-identifier-lifecycle.md#joint-compromise)). What it conveys is control, not a scope: the delegate holds signing authority over its own identifier and the delegator holds the power to approve or block its establishment events. The 2022 DAD deck draws the distinction that the 2026 registry proposals extend one layer up: "Delegation of identifier (revokable). This creates a new identifier with its own set of keys" as against "Transfer of control (non-revokable)." (DAD deck, p10). [architect]

### Delegating authority {#authority-delegation}

An ACDC chain conveys a scope: what the Issuee may do, under what constraints, for whom. It needs no KEL delegation at all. Sam: "Delegated AIDs should work without there being an ACDC." ([chapter 03, section 8](03-key-management-and-identifier-lifecycle.md#delegation-trait-rulings), R-013), and the reverse holds in practice. The Utah SEDI fixture calls its chain a three-level delegation chain, but every AID in it is made with plain `incept`, and the chain is credentials joined by `I2I` edges ([chapter 05, section 11](05-acdc-and-verifiable-data.md#utah-delegation-chain)). Bakobo's GCD schema made the same choice explicit, treating KEL delegation as the exemplar of delegated authority rather than a precondition for it ([chapter 05, section 11](05-acdc-and-verifiable-data.md#gcd)). [practice]

### Where the two meet {#delegation-composition}

They meet in three places, and each is a place a reviewer should check.

- The `DI2I` edge operator lets the near node's Issuer be the far node's Issuee or any AID delegated from it. Sam ruled that this reaches delegated AIDs at any depth and that depth is bounded by inception-time traits, not by the operator ([chapter 05, section 5](05-acdc-and-verifiable-data.md#di2i-depth)). keripy at `80f77b73b` fails `DI2I` closed. [proposal], [code]
- The `DND` trait limits authority by construction. `sda.md` puts the point in authorization terms: "a delegate configured never to sub-delegate produces no sub-delegation any verifier will honor" (sda.md > 7. Open loop, not closed, L121). keripy enforces `DND` in key-state validation, so the forbidden event is dropped rather than refused by policy ([chapter 03, section 8](03-key-management-and-identifier-lifecycle.md#delegation-enforcement)). [spec], [code]
- The `DID` trait asserts that delegator and delegate are one controller, so that reputation can cross the delegation. What a relying party does with that is left to it and to its governance framework ([chapter 03, section 8](03-key-management-and-identifier-lifecycle.md#did-effect-unspecified)). [spec], with the consequence [proposal]

The rule a reviewer should apply: a design that says "delegation" must say which one. A design that relies on KEL delegation for scope will find no scope in the KEL; a design that relies on an ACDC chain for the joint-compromise property will not get it, because an ACDC's Issuee can be any AID.

## 3. Lossless trust transfer, and the attack it is meant to remove {#trust-domains}

The framing slide of the EVAC deck sets two chains side by side: "perpetual identity → perpetual issuances → lossless trust transfer (KERI Suite)" against "ephemeral identity → ephemeral issuances → lossy trust transfer (DNS/CA, OAuth/OIDC)" (EVAC deck, p4). Its conclusion is the thesis of the authorization work: "ACDC lossless conveyor of trust → bridging ephemeral trust domains" (p4). The intermediary class disappears because every party authenticates itself: "With KERI, each AID controller is its own identity provider" and "No third-party IdPs, no relying parties, no trusted intermediaries" (EVAC deck, p5). [architect]

### Recursive privilege escalation {#rpea}

The threat named is the recursive privilege escalation attack (RPEA), which the deck says ACDC bridging "eliminates" (EVAC deck, p4). The argument is spoken, not written. In the talk, systems that cannot bridge trust domains enlarge them instead: "since you can't bridge trust domains, make your trust domain bigger. And that means now that you can do recursive privilege escalation" (KERIConf26 caption, Samuel Smith, The Future of KERI, 03:39). The idea is older than the name. In 2017 Sam described the same perimeter failure: "Any mechanism that allows for lower priviledged users to access a network layer provides an attack vector for that user to elevate their priviledges" (ManyCubed.md > The Many-to-Many-to-Many Problem > Security, L26). [architect]

Two cautions for a reviewer. No written source in this corpus defines RPEA formally, so it should be treated as Sam's name for a class of attack, not as a defined threat model with a stated adversary. And "eliminates" is an assessment; the mechanism offered is mutual authentication at every edge plus small trust domains, which removes the foothold an escalation needs only where every hop actually verifies. A deployment that verifies at the boundary and trusts inside has the old perimeter back, with ACDCs at the gate ([chapter 07, section 5.1](07-shibboleths-and-anti-patterns.md#authn-before-authz)).

### Legacy servers may stay, on one condition {#legacy-condition}

Sam does not demand that OAuth infrastructure be torn out. In the talk he tolerates it inside its own domain: "You got to have an OAuth server. Fine, Leave it in there. But don't use it to expand its trust domain." (KERIConf26 caption, Samuel Smith, The Future of KERI, 06:37), and the bridging itself should be done with KERI and ACDCs (06:43). No written source in this set carries that conditional tolerance. It is the test [section 11](#applied-patterns) applies to the OAuth bridge, and it is how this chapter reads the categorical rejection of tokens in [chapter 07, section 5.2](07-shibboleths-and-anti-patterns.md#bearer-tokens): what is rejected is the bearer secret and the identity provider as root of trust, not every component that happens to be called a token server. [architect], caption only

## 4. EVAC: edge verifiable access control {#evac}

### The rule {#evac-rule}

EVAC places the authority to grant access with whoever controls the resource: "Authorization to access a resource is granted by the resource's controller (authority)" (EVAC deck, p6). Any node in an ACDC graph can hold both roles: "Each Issuer in an ACDC graph may be both a resource authority and an edge." (p6). Impersonation is handled by authentication at both ends: "Mutually authenticated edge (accessor) and authority prevent impersonation attacks" (p6). [proposal]

### The mechanism {#evac-mechanism}

An EVAC grant is an ordinary ACDC whose attribute section carries a resource map. The slide lists the attribute block's fields as "SAID UUID Issuee AID Registry Resource Map", with rows pairing a route to a capability set, and adds that the "Attribute section could convey a policy engine rule set" (EVAC deck, p14). Two registries back the grant. The issuance registry is the Issuer's ordinary blindable registry, published by a Registrar and cached by the verifier's Observer (p15). The usage registry is the Issuee's, and each presentation is anchored there, so that "ACDC Issuee Presentation state is verifiably bound to Issuee’s key state despite rotations" (p16). EVAC adds no registry type. It composes the Issuer's state registry of [chapter 05, section 9](05-acdc-and-verifiable-data.md#registries) with the Issuee usage registry of [chapter 10](10-presentation-registries.md#asymmetry). [proposal]

The `Registry` field in the attribute block is the Issuee's, distinct from the Issuer's top-level `rd`. Sam says in the talk that such a field is already in the specification (KERIConf26 caption, Samuel Smith, The Future of KERI, 11:55). That is partly supported. The specification permits an `rd` inside `a`, but for a different purpose: it "may better facilitate contractually protected disclosure of the bulk-issued registry" (ACDC spec > Top-level ACDC Sections > Attribute Section > Attribute Section Variants > Targeted Attribute Section, L326). Its use as an Issuee usage registry is keripy behavior and proposal, not specification ([chapter 10, section 7](10-presentation-registries.md#keripy-verifier)).

### Who enforces {#evac-enforcement}

Nothing written says how a verifier evaluates a resource map against a request. Asked how least privilege is enforced, Sam put enforcement with the verifier or with a policy engine of its choosing: "Otherwise, what you're going to have to have is a policy engine that the verifier asks to enforce it for them." (KERIConf26 caption, Samuel Smith, The Future of KERI, 49:41). Whether that policy engine is the verifier's own component or an outside service decides which side of the line in [section 5](#state-not-verdict) it falls on. [architect], caption only

### Where it stands {#evac-status}

EVAC is in neither ACDC branch and not in keripy at `80f77b73b`. Sam's own status statement, in the talk: "This is a proposal. I haven't written a white paper on it yet." (KERIConf26 caption, Samuel Smith, The Future of KERI, 10:07), and again in August 2026, "I started an EVAC white paper but have yet to publish it." ([keripy conversations > discussion #1550](https://github.com/WebOfTrust/keripy/discussions/1550#discussioncomment-17909785), comment of 2026-08-05). [proposal]

## 5. Verification-time state: fetching state versus asking for a verdict {#state-not-verdict}

### The tension {#state-tension}

Two statements in this corpus appear to conflict, and an adversarial reviewer will find the conflict whether or not the corpus resolves it.

On one side, [chapter 07, section 3.2](07-shibboleths-and-anti-patterns.md#status-endpoint) carries as a shibboleth Daniel Hardman's rule: "A registry consulted at verification time is a phone-home in disguise." (sda.md > 7. Open loop, not closed, L119), with its corollary that "any registry or log is an issuance-time and audit-time convenience, never a verification-time dependency" (L119).

On the other, revocable authority cannot be honored without reading its current state. EVAC's verifier reads two registries before granting access (EVAC deck, p15, p16). The ACDC specification itself puts a registry read at the point of validation: "A validator queries its Observer, not the Registrar, at a point of validation (PoV) for an ACDC." (ACDC spec > Disclosure Mechanisms and Exploitation Protection > TEL Registrars and TEL Observers, L1693). And `sda.md` relies on the same read in its own section 8, answering the standing-authority objection with "revocation is real-time, so a grant whose justification has lapsed can be ended before its next use" (sda.md > 8. What is settled, and what is open, L129). Read literally, the section 7 sentence forbids what section 8 depends on.

### The resolution {#state-resolution}

The line falls elsewhere, and KERI's own sources draw it. End-verifiability already allows a service to supply what a verifier needs, so long as the verifier checks what it is given ([chapter 01, section 4](01-foundations-and-worldview.md#end-verifiability)). What it forbids is verification that needs a service's answer rather than its data. Applied to registries, the distinction has three parts, and the evidence for each is in the ACDC specification and Sam's papers.

#### What comes back: data the verifier checks, or an answer it must believe {#what-comes-back}

The phone-home KERI rejects is the one Sam describes as the origin of federation. When credentials are proven by bare signatures, "the party who is presented with an issuance, no longer verifies the signature directly but asks the issuer to verify on its behalf." (Revocation.md > Proofing Mechanism Tradespace, L76), and recipients "become relying parties that phone home to the issuer/verifier" (L76). What comes back is a verdict. The relying party cannot check it; it can only trust whoever gave it.

A TEL read is different in kind, because the verifier checks what it receives against key state it has already verified. "Any Validator can cryptographically verify the authoritative state of the transaction by validating the presence of the seal in the associated KEL." (ACDC spec > Transaction event logs (TELs) as ACDC state registries > Validating transaction events, L1946). The source of the bytes then does not matter, which is the same rule KERI applies to KELs served by witnesses and to OOBIs ([chapter 02, section 9](02-security-model-and-threat-posture.md#observer-layer)). For blinded state the verifier goes one step further and recomputes the commitment: keripy rejects a disclosed state block that "does not reproduce blid, so it proves nothing about the registry's state" (keripy acdc/regeventing.py, vetBlind, L460 @80f77b73b), and the function recomputes the block's SAID and raises unless it equals the anchored BLID (L476-485). [spec], [code]

#### Who learns that verification happened {#who-learns}

Fetching verifiable state can still leak. A verifier that reads the Issuer's Registrar at each presentation tells the Issuer where and when its credential was used, which is a correlation harm even when the answer is checkable. The specification solves this separately, by putting the Observer under the verifier's control and decoupling its synchronization from use: "the interactions between the Observer and Registrar occur when there are ACDC state changes, not when there is a PoV" (ACDC spec > Disclosure Mechanisms and Exploitation Protection > TEL Registrars and TEL Observers, L1693), which "protects against forced validator-to-issuer correlation of ACDC usage, i.e., no forced phone home validation." (L1693). Bulk updates close the residual timing channel ([chapter 05, section 9](05-acdc-and-verifiable-data.md#bulk-updates)). [spec]

So the specification's own phrase "phone home" covers two harms, and the Observer answers both: the verifier checks state rather than believing an answer, and the Issuer never sees the point of validation. A design can fail either test independently. A status service that returns a signed yes or no fails the first even if it is private. A Registrar queried per presentation fails the second even though its answer is verifiable.

#### How fresh the state must be {#freshness}

Reading state at verification time leaves a freshness question that no read can close: the cache may lag the Registrar. The specification answers with policy, not with a callback: timed grace periods on revocations, so that "a revocation does not go into effect until a specified date and time after the state update." (ACDC spec > Disclosure Mechanisms and Exploitation Protection > TEL Registrars and TEL Observers, L1695). A verifier whose Observer synchronizes within the grace period sees every revocation before it takes effect. That is an assumption about synchronization latency, set by policy and not proven by anything, and a verifier that cannot meet it must treat its cache as stale. It is a dependency on data being available, of the same kind every KERI verifier has on receiving KEL events, and not a dependency on any party's honesty. [spec]

#### The rule, restated {#state-rule}

Verification may read state at verification time, from any source, including the verifier's own cache, provided the verifier checks that state against key state itself and the read does not disclose the point of validation to the Issuer. It may never accept a service's answer in place of that check. This chapter reads `sda.md`'s sentence as aimed at the second case; its literal wording also forbids the first, and is stricter than either KERI's registry design or `sda.md`'s own section 8. [chapter 07, section 3.2](07-shibboleths-and-anti-patterns.md#status-endpoint) quotes the literal sentence; the endorsed doctrine's summary row for that shibboleth already states the narrower form.

### Applying the rule {#state-applications}

To EVAC: both registry reads pass, provided both go through the verifier's Observer and both are verified against the relevant KEL. The Issuee's usage registry is the harder case, because the verifier must first obtain a registry controlled by a party other than the Issuer, and keripy at `80f77b73b` does not retrieve a foreign registry at all; the verifier must already hold it ([chapter 10, Status](10-presentation-registries.md#status)). [proposal]

To EVAC's policy engine ([section 4](#evac-enforcement)): an engine the verifier runs, on rules it can read, is the verifier deciding. An outside engine that returns permit or deny is a verdict service, and passes only if its rule set is published and its result reproducible by the verifier, which is the condition `sda.md` sets for open-loop authorization: "any two verifiers compute the same gate from the same credential" (sda.md > 7. Open loop, not closed, L117). [proposal]

To bridges ([section 11](#applied-patterns)): an OAuth resource server that validates a token by calling an introspection endpoint is receiving a verdict. Whether the healthKERI bridge works that way was not stated in the talk and is open.

To demonstrations: Cole Davis's simulated smart lock is a clean illustration of the permitted case. Given a revocation event in the lessor's TEL, "the smart lock just walks the cryptographic operations all the way back" (KERIConf26 caption, Cole Davis, Contract Credentials and Verifiable Identity, 19:46). He states that the demonstration was simulated rather than built on the KERI stack (22:50), so it is illustration only.

## 6. Broken chains: bound state, reversion, transfer {#broken-chains}

### The problem {#broken-chain-problem}

Sam poses it as two questions. "When a delegatee's authority to issue authorizations is revoked, what is the status of any authorizations/entitlements issued before the authority was revoked?" (EVAC deck, p17). And for the verifier: "How can a validator securely verify the status of prior valid issuances from a chain-of-" authority once the chain is broken (p17). In April 2026 he gave the failure a name: dynamically revocable issuances "that become zombies if the delegating ACDC is revoked." ([keripy conversations > discussion #1082](https://github.com/WebOfTrust/keripy/discussions/1082#discussioncomment-16688843), comment of 2026-04-23, edited 2026-04-26, R-037). A downstream credential whose issuer has lost its authority is still valid on its face, and nobody holds the power to revoke it. Three answers are offered, in increasing order of novelty.

### Bound blinded state: specified {#bound-blinded-state}

The bound blinded attribute block adds two fields, `bn` and `bd`, to the blinded state block a registry update commits to. They name the Issuee's key event (sequence number and SAID) at the moment of the update, so a state change in the Issuer's registry is bound to the Issuee's key state as well as the Issuer's. The specification states the purpose in authorization terms: "The purpose of the bound blinded attribute block is to better support chains of authority using delegated chained ACDCs." (ACDC spec > Transaction event logs (TELs) as ACDC state registries > Registry Message Types and Fields > Bound Blinded Attribute Block, L2433). What it proves is that a delegate "had an authorization to issue its own delegated ACDCs, which authorization had been issued but not yet been revoked" (L2433) at the time it anchored its own issuance. The same text is on `v1.1` @`2362e48a1` at L2634. [spec]

The mechanism, read from the specification's description and the deck's diagram (EVAC deck, p18): the Issuer's revocation of a delegate's grant records the delegate's key state at revocation. A downstream issuance the delegate anchored in its own KEL after the key event bound at issuance and before the one bound at revocation was made while the grant stood; one anchored later was not. The verifier compares positions in one log, the delegate's, which is the as-of-anchor reasoning of [chapter 03, section 11](03-key-management-and-identifier-lifecycle.md#as-of-anchor) applied across a credential chain. The deck's caption for the result: "Breaking the chain-of-authority while preserving validity of prior valid issuances" (EVAC deck, p18).

Two limits. Sam calls the binding "an assertion by the issuer of issuer's intent." ([keripy conversations > discussion #1566](https://github.com/WebOfTrust/keripy/discussions/1566#discussioncomment-17846317), comment of 2026-07-30, R-039), and says that what it does is "allow broken delegation chains to break more intelligently and also to be repaired more intelligently." (same). It does not make the surviving issuances revocable again: once the delegate is gone, nobody can revoke what it issued, so in the talk Sam ties the approach to issuances that expire on their own, with a food handler's permit as the example (KERIConf26 caption, Samuel Smith, The Future of KERI, 40:02, 40:18). And no verifier implements the comparison. keripy at `80f77b73b` defines the structure, "bn = bound issuee key event hex sequence number bnh at time of state update" (keripy core/structing.py, L99 @80f77b73b), carries it as an IPEX proof and checks a disclosed block against its BLID, but a search of `src` for consumers of the bound fields finds none outside `core/structing.py`; only tests read them. [code], negative by search

### Reversion of authority: proposed {#reversion}

Reversion makes the zombies revocable again by returning their registries to the delegator. Sam's written statement of it: "when the ACDC of the delegatee is revoked, authority over any down stream ACDC state reverts to the delegator (State)." ([keripy conversations > discussion #1082](https://github.com/WebOfTrust/keripy/discussions/1082#discussioncomment-16688843), comment of 2026-04-23, R-037). The edge that already points from the delegate's grant to the delegator's is what lets a verifier trace it: "a verifier can cryptographically verify and trace the reversion of authority triggered by a revocation." (same). In the talk he says reversion can climb any number of levels (KERIConf26 caption, Samuel Smith, The Future of KERI, 25:10), and gives its status: "it's not written up in the spec but this is an easy modification of the spec" (22:27). The ease is his estimate. Neither ACDC branch has it and keripy has no trace of it. [proposal]

What reversion leaves unspecified is how a verifier evaluates a reverted registry: which signatures it accepts on updates after the revocation, how it finds the revocation that triggered reversion, and what it does when the delegator itself has been revoked. The deck's diagram (EVAC deck, p19) shows the registry's subsequent updates bound to the delegator's key state, which suggests the answer to the first; no written rule says so.

### Registry transfer: approved, not specified {#transfer}

Transfer hands a registry to a new controller instead of leaving the delegator holding it. The deck's bullet: "Replace the controller of registry without reverting the authority to delegator" (EVAC deck, p20). The event's history, from `rxr` in April to `xfr` in July, its "doubly anchored" requirement and Sam's report of community approval for ACDC v1.1, are recorded in [chapter 05, section 9](05-acdc-and-verifiable-data.md#registry-transfer). Neither branch has it at the pins, and keripy has neither ilk. The two proposals compose: in the talk, the transfer event is issued after reversion, by the authority control has reverted to (KERIConf26 caption, Samuel Smith, The Future of KERI, 27:26), and asked whether transfer of this kind needs reversion in place, Sam answered yes (38:32). He also bounded it: "This is reversion for a hierarchy of authorizations and delegation, not a replacement for asset transfer." (38:46). [proposal]

#### A written source that overstates the status {#transfer-drift}

One written source describes transfer as if it existed. Sam's June 2026 revocation paper says registry control "can be transferred via a transfer event in the registry." (Revocation.md > Proofing Mechanism Tradespace > Proofing Applied to Revocation Registries, L118). The registry event tables on both branches list `rip`, `bup` and `upd`, and nothing else. Read the sentence as an informal paper describing a planned event in the present tense, not as evidence that the event advanced; if a later specification commit adds it, the upgrade is recorded then.

## 7. Why authority must be revocable, and anchored {#revocation-doctrine}

Sam's revocation white paper (self-versioned V0.4, June 2026) is the most substantial written argument in this area. It is framed for SEDI, but its argument is about authority in general, and it explains why the anchoring doctrine of [chapter 05, section 9](05-acdc-and-verifiable-data.md#key-state-binding) is an authorization requirement, not only an integrity one. All of it is [proposal].

### Long-lived entitlements must be revocable {#must-be-revocable}

"Therefore, with rare exception, if any, as a matter of policy, if not law, all state issuances MUST be revocable." (Revocation.md > Revocability Properties, L35). Short lifetimes do not escape the requirement when reissuance is automatic, because the reissued series is itself a long-lived entitlement (L27). This is the premise the rest of the chapter depends on: if authority must be revocable, it must be read at verification time, and [section 5](#state-not-verdict) is not optional.

### Bare signatures force revocation, and federation followed {#signatures-force-revocation}

The core argument: "when the authenticity proofing mechanism is a bare attached digital signature, all issuances must be revocable, and are forceably revoked whenever the keys are rotated." (Revocation.md > Proofing Mechanism Tradespace, L70). The paper's metaphor is that signatures are "like signing in dissappearing ink that fades over time due to exposure to air." (L74). From that it derives a causal account of federated identity that [chapter 07, section 5.4](07-shibboleths-and-anti-patterns.md#federation) lacks: hiding constant reissuance behind issuer-side verification "is the driver behind the architecture of federated identity systems such as OAuth/OIDC" (L76). Anchoring removes the cause: "Issuances themselves are not individually signed; a hash of the issuance is anchored in the log." (L94). A delegate's authority anchored this way survives the delegator's rotations, which is what lets a chain of authority outlive the key management of every party in it.

### One registry per issuance {#registry-per-issuance}

Against bitstring status lists the paper argues governance, not efficiency: a bitstring "encodes the status of all issuances into a single data structure. This co-mingles the governance." (Revocation.md > Proofing Mechanism Tradespace, L106). ACDC's alternative: "ACDCs use independent registries, one per issuance." (L110), and the inversion a reviewer should be able to state: "ACDCs are not signed; they are bound (anchored) to a registry, which in turn is bound (anchored) to a KEL." (L114). Per-issuance registries are also what make reversion and transfer possible at the granularity of one grant. Revocation of a bulk-issued set is all or nothing ([chapter 05, section 9](05-acdc-and-verifiable-data.md#bulk-revocation), [chapter 07, section 3.4](07-shibboleths-and-anti-patterns.md#bulk-copy-revocation)).

### The claims an outsider will contest {#contested-revocation-claims}

Several claims in the paper are Sam's assessment and will draw objection. On unlinkability: "Therefore, unlinkability is largely an exercise in privacy theater." (Revocation.md > Tradespace of Proofing mechanisms, L190), though in the same paragraph he keeps it as a requirement for adoption. On anonymous credentials: "So revocation requirements alone obviate one of the main reasons to use anonymous signatures as a proofing mechanism." (L192), and a censure, that systems which "ignore the ephemerality problem of bare attached signatures, including ZkP anonymous signatures, are fundamentally flawed from a security perspective." (L186). The paper dismisses accumulator-based revocation on performance grounds, "These have proven to be impractical for performance reasons." (L192), with no citation. A reviewer may contest that dismissal on its merits; the chapter reports it as his assessment, and pairs it with the counter-position the paper does not engage. The doctrine's position on unlinkability as one tool among several is in [chapter 06, section 4](06-governance-ecosystems-and-interop.md#layered-privacy).

## 8. Group authority: membership, anchoring and joint issuance {#group-authority}

When the authority is a group, KERI's group issuance white paper (KAGI, February 2025) supplies three answers. All are [proposal].

### Membership is private unless declared {#group-membership}

"the KEL does not publicize the single-sig member AIDs that contribute to a group multi-sig AID." (KAGI > Background > Group Multi-Sig AID, L61). Where a relying party needs to know who stands behind a group, the group discloses it by credential, "for the group multi-sig AID to issue an ACDC that discloses its member AIDs at the time of its issuance" (L65), revoked and reissued when membership changes. Multisig encodes a group's decision rule; it does not say who the members are ([chapter 03, section 7](03-key-management-and-identifier-lifecycle.md#multisig)).

### Anchoring is an access-control cost {#anchoring-cost}

KAGI states the trade plainly. Anchoring gives "non-ephemeral authentication by binding issuances to the key state at the time of issuance" (KAGI > Background > KEL Sealed (Anchored) Issuances, L177), but the cost lands on the enforcement layer: "perimeter protection mechanisms now have to walk KELs to look up and find anchors" (L183). An authorization design that verifies anchored grants at a load balancer pays that cost per request unless it caches key state, which is what KRAM's monotonic caches are for ([chapter 09, section 3](09-kram-and-request-authentication.md#full-kram)).

### Joint issuance as a threshold root {#joint-issuance}

"Joint issuance is a new concept." (KAGI > Problems and Solutions > Other Options > Joint Issued ACDCs, L281). Each member issues its own copy, anchored in its own KEL, and a validator requires a threshold of identical copies, the threshold fixed by a designated key state of the group. `sda.md` names this as the mechanism for the root of an authority chain: it "lets a grant be satisfied by a weighted threshold of endorsements, each owner signing from their own identifier, asynchronously and with no shared key." (sda.md > 8. What is settled, and what is open, L127). Whether the Dossier specification makes joint issuance normative was not checked for this chapter.

## 9. Agents are delegates {#agents}

### The doctrine {#agents-doctrine}

The EVAC deck's agentic slide is the whole position in a few lines: "Agent has its own AID", "Realizes the original meaning of the word agent", "ACDC mechanisms are the same for AI, person, or entity agents." and "Multi-sig enables thresholded group agents" (EVAC deck, p7). The slide retitles the acronym Edge Verifiable Agentic Control. In the talk, the agent's identifier is a delegated one: "You just give the agent an AID, a delegated AID, right?" (KERIConf26 caption, Samuel Smith, The Future of KERI, 41:50), and the mechanism does not change: "The ACDC mechanisms are exactly the same. They don't change." (42:03). [architect]

So an AI agent, under this doctrine, is a delegate in both senses of [section 2](#two-delegations): an identifier of its own, typically delegated from its principal's so that its establishment events need the principal's approval, and authority conveyed by a targeted ACDC from its principal, scoped, revocable and anchored. Its depth is limited by construction, through `DND` on the delegated identifier and through the chain of grants (KERIConf26 caption, Samuel Smith, The Future of KERI, 43:12). Nothing in the protocol distinguishes a software agent from a human one. The slide's last line floats one place a distinction might enter, as a disclosed attribute: "Maybe regulations should require attributes that indicate the type of agent. (AI vs person)" (EVAC deck, p7). That is a governance suggestion, not a protocol requirement.

### The same pattern a year earlier {#agents-kagi}

The pattern predates the AI framing by more than a year. KAGI proposed delegated agents to avoid running a multisig group through every stage of an IPEX negotiation: "Avoid multi-sig on each stage of IPEX by using a delegated agent" (KAGI > Problems and Solutions > Other Options > Agent Delegated Negotiation, L256). Its safety rule is that an agent's output binds the group only through an anchored grant: "Agent-issued `agree` for one side and `grant` for the other are valid only if they include a verifiable reference to a corresponding anchored ACDC." (L257), and "This protects the group members from malicious agents." (L257). The design driver is a division of labor that applies directly to AI agents: "Validation (which includes business logic and cryptographic verification) may be largely automatable, whereas signing requires human intervention." (KAGI > Problems and Solutions > Other Options, L250). [proposal]

### The word agent already means a delegate in KERIA {#keria-agent}

In the KERIA/Signify architecture the cloud agent is a delegated AID whose delegator is the controller's client AID, and it never holds the controller's signing keys ([chapter 03, section 12](03-key-management-and-identifier-lifecycle.md#two-aid-spine)). That is the same shape the AI doctrine proposes, and it is why the custody rule, that a cloud agent never holds or uses the controller's signing keys, applies to AI agents without amendment ([chapter 07, section 5.3](07-shibboleths-and-anti-patterns.md#custodial-cloud)). An AI agent given its principal's keys, or a bearer secret, has been given control, not authority. A reviewer should keep the two senses apart in prose, because KERIA's agent relays and stores while an AI agent acts, but the security rule is one rule.

### Containment by construction {#agent-containment}

`sda.md` adds a pattern the EVAC deck lacks, and it is aimed at agent orchestrators: "Give a powerful orchestrator broad authority to authorize but an empty act surface, and its blast radius on compromise collapses" (sda.md > 5. The relationship the act is performed under, L93). Under KERI, that is an orchestrator holding grants it may re-issue in attenuated form but no grant that any resource honors directly. Its compromise yields only the power to propose further delegations, each of which is itself checked. Whether any deployment does this is not known to the corpus. [proposal]

### What remains a judgment {#agent-judgment}

Two boundaries are the doctrine's, and a design for AI agents must not erase them. KERI proves which keys signed, not that the signer meant it ([chapter 07, section 9](07-shibboleths-and-anti-patterns.md#signature-authorship)). For an AI agent, the gap between an authorized act and a faithful one is exactly that gap. `sda.md` states it as a bound on what any authority model can do: "Sincerity stays gate-able and auditable, never provable." (sda.md > 8. What is settled, and what is open, L131). And the corpus holds that verification may be automated while reliance may not ([chapter 07, section 9.3](07-shibboleths-and-anti-patterns.md#automated-trust)). An AI agent that relies on credentials on its principal's behalf is that automated reliance. The doctrine does not yet say whether delegating reliance to an agent, under a scoped and revocable grant, satisfies the rule or breaks it. This chapter records it as open.

### The KERI-or-surveillance thesis, as Sam's assessment {#surveillance-thesis}

Sam's 2026 framing of KERI in an AI world is advocacy, and the corpus carries it as his. The written source is a deck of questions prompted by a Five Eyes statement. It contrasts AI-based identity, a "Digital persona derived from the continuous tracking & statistical correlation of one's behavior and biometric expression." (AI deck, p5), with a KERI-based alternative, and asks what mechanisms would ensure that every significant AI action "remains attributable to accountable humans and organizations" (AI deck, p10). It asks rather than asserts that there is no middle ground: "Why do you believe there may be no stable middle ground between these two futures?" (AI deck, p18). The written echo of the accountability argument is in the revocation paper, where AI and aggregators act "as super correlators to defeat any and all technical attempts at digital anonymity." (Revocation.md > Digital Identity System Goals > Privacy, L172), so that the protection that remains is legal recourse. [architect]

The assessment boundary. The dichotomy is argued, not demonstrated. The strongest objection is that most deployments will run a mixed regime, cryptographic identity for authority plus behavioral fraud detection, and the thesis does not engage it. Sam himself once proposed behavioral AI as an authorization input inside one's own infrastructure: "Dynamic policy modification that uses AI to first profile and detect anamalous behavior and then restrict the authorization of that user prevents discovery." (ManyCubed.md > The Many-to-Many-to-Many Problem > Security, L40). Profiling inside one's own perimeter is not behavioral identity across society, so this is a boundary the 2026 thesis leaves implicit rather than a contradiction. The documents the deck answers were not read for this chapter.

## 10. What a grant should contain: one proposal {#grant-shape}

KERI carries a grant; it does not say what a grant should express. EVAC's resource map is a route plus a capability list. `sda.md`, Daniel Hardman's paper (version 1.2, July 2026), is the one source in the corpus that models the content of authority, and it names KERI and ACDC as its identity layer. It is an authored position, not community doctrine, and its author owns this corpus. [proposal]

Its main additions over a capability list:

- Acts are located by effect over a kind of state, not by route, so a grant can bound the full surface of what a delegate might do rather than the interfaces it touches. Bakobo's GCD schema implements this grid ([chapter 05, section 11](05-acdc-and-verifiable-data.md#gcd)). [practice]
- A separate relationship facet names principal, relationship type, liable party and presented identity, because "Beneficiary, actor, and liable party can be three different parties" (sda.md > 5. The relationship the act is performed under, L89).
- Authority to act is separated from authority to authorize, which yields the containment pattern of [section 9](#agent-containment).
- Open-loop verification forces full disclosure of every constraint, because a stranger "cannot ask the issuer what was meant" (sda.md > 7. Open loop, not closed, L117). GCD therefore does not support graduated disclosure of its constraints ([chapter 05, section 11](05-acdc-and-verifiable-data.md#gcd)).

### Standing authority {#standing-authority}

The objection `sda.md` concedes is the one most often raised against delegation credentials: a persistent grant "is granted once and weighed against the conditions that held at issuance, not those that hold at the moment an act takes effect." (sda.md > 8. What is settled, and what is open, L129). Its answer is two properties: the gate is recomputed per act at the execution boundary, and revocation is real-time. It rejects per-act minting of authority as the closed loop in other dress. What it leaves open is termination on completion, an authority that ends when its purpose is done. This is the strongest available framing of why EVAC needs dynamic revocation, and why the broken-chain proposals of [section 6](#broken-chains) matter.

## 11. Applied patterns and bridges {#applied-patterns}

Every pattern in this section is a spoken claim by a vendor or a demonstrator at KERIConf26. None was checked against code. They are evidence of how the doctrine is being applied, not of what it requires. [practice], caption only

### An ACDC-backed OAuth authorization server {#healthkeri-bridge}

Phil Feairheller described healthKERI's authorization server for FHIR, where OAuth is mandated. A client registers by presenting a vLEI through IPEX, its client identifier becomes the credential's SAID, and "there's no client secret. Every token request from here on out is a signed request." (KERIConf26 caption, Phil Feairheller, ACDCs for Authorization, 13:25). Key state is tracked by a local watcher run as a sidecar (22:14). The server is configured by which schemas and root issuers it trusts, which he calls an identity provider appliance (25:33). His stated lesson is commercial: a KERI-native gateway found no adopters, so the company is "meeting the customer where they are" (07:27).

#### Reading it against the doctrine {#healthkeri-reading}

[chapter 07, section 5.2](07-shibboleths-and-anti-patterns.md#bearer-tokens) quotes an applied doctrine that rejects OAuth and tokens categorically. The bridge is reconcilable with it in one direction and not yet in the other. What it removes are the two things the doctrine actually objects to: the shared client secret, and the identity provider as root of trust, since the client's identity is a credential the server verifies from key state its own watcher tracks. That satisfies Sam's condition in [section 3](#legacy-condition): the OAuth server stays, and the bridging is done with ACDCs. What it does not settle is downstream. If the access token the server issues is a bearer token honored by resource servers without further proof, the trust domain behind the server still runs on a bearer secret, and if resource servers validate it by introspection, they are asking for a verdict ([section 5](#state-applications)). The talk does not say which. Open.

### Contract credentials, execution trust, delegated signing {#other-patterns}

Cole Davis presented contract credentials: a credential derived from a legal contract, with authority composed by edges and a lessee issuing itself an access credential that a smart lock verifies; termination of the lease revokes everything downstream (KERIConf26 caption, Cole Davis, Contract Credentials and Verifiable Identity, 14:15). The normative hook is real, the specification's "contractual vehicle for conveying authorization" ([section 1](#normative-floor)); the demonstration was simulated (22:50).

Alan Davies presented execution trust: a verification gate inserted immediately before a high-value action in an existing system, as the near-term route into enterprises (KERIConf26 caption, Alan Davies, ACDCs for Enterprises, 13:13). Its doctrinal content is where verification happens, at execution rather than at login, which is the same move `sda.md` makes when it recomputes the gate at the execution boundary ([section 10](#standing-authority)).

Daniel Hardman presented an enterprise credential that delegates the right to sign calls to a communications platform (KERIConf26 caption, Daniel Hardman, Open Verifiable Communications, 06:19), with a transit operator failing a call whose credential chain does not verify (10:02). It is the one proof-of-concept instance of chained delegated authority in the conference set; its detail belongs to a telecom scenario rather than here.

### Guardianship {#guardianship}

Guardianship is authority over another person's authority, and Sam's SEDI modeling treats it as a chain of grants rather than a key-management trick. A ward has "a limited set of citizen rights, which rights are held by their parents and must be delegated back to their child" ([keripy conversations > discussion #1550](https://github.com/WebOfTrust/keripy/discussions/1550), body of 2026-07-28, R-072), in diagrams labeled as notional and not State of Utah policy. On a parent's control over a child's social-media access, he lists five key arrangements and picks the one where the platform accepts authorization only from the parent's AID as "the minimally sufficient means for the parent to have control over the childs access to social media." ([keripy conversations > discussion #1573](https://github.com/WebOfTrust/keripy/discussions/1573#discussioncomment-17935861), comment of 2026-08-07, R-071). Divorce and remand to child services were among the cases he gave for registry transfer ([section 6](#transfer)). The custody-from-birth position is in [chapter 06, section 3](06-governance-ecosystems-and-interop.md#sedi-architecture). [proposal]

## 12. Established, contested and open {#conceded-weaknesses}

### Established {#established}

- A targeted ACDC conveys authority to its Issuee; chains of targeted ACDCs are chains of authority, with attenuation; untargeted ACDCs convey no authority. [spec]
- Each link is anchored in its Issuer's KEL and judged as of that anchor, so chains survive rotation. [spec]
- The bound blinded attribute block binds a registry update to the Issuee's key state, for chains of authority. [spec]; its structure is [code] and nothing consumes it.
- `DND` limits delegation depth by construction and keripy enforces it in key-state validation. [spec], [code]
- The verifier reads registry state through its own Observer, synchronized on state change, not at the point of validation. [spec]; the Observer is unbuilt ([chapter 05, section 9](05-acdc-and-verifiable-data.md#registrar-observer-status)).

### Contested, or Sam's assessment {#contested}

- That ACDC bridging eliminates recursive privilege escalation, an attack with no written definition in the corpus.
- That bare-signature ephemerality caused federation, and that unlinkability is largely theater.
- That accumulators are impractical for revocation.
- That no stable middle ground exists between KERI-based and surveillance-based identity.

### Open {#open-questions}

1. How a verifier evaluates an EVAC resource map against a request, and what language a policy rule set in the attribute section uses.
2. How a verifier validates a reverted registry, and whether reversion recurses when the delegator is itself revoked.
3. Which two logs anchor the `xfr` event, and its fields; the deck's `rxr` diagram and its `xfr` bullet differ.
4. Whether any chain-walking verifier will use `bn` and `bd`, and what it does with an issuance anchored at the same key event as the revocation.
5. Whether an OAuth access token minted by an ACDC-backed authorization server is a bearer token downstream, and whether resource servers introspect it.
6. Whether delegating reliance to an AI agent satisfies the rule that reliance is not automated ([section 9](#agent-judgment)).
7. How a verifier obtains an Issuee's usage registry it does not already hold, without telling the Issuee or Issuer where verification happened.
8. Whether joint issuance is normative in the Dossier specification.
9. Termination of authority on completion of its purpose, which `sda.md` leaves open.

## Sources {#sources}

- ACDC spec — Authentic Chained Data Containers (ACDC) specification, Trust Over IP. trustoverip/kswg-acdc-specification, spec/spec-body.md. `main` @`f0bd097de` (2026-08-28) supports every [spec] claim; `v1.1` @`2362e48a1` (2026-09-11) was checked for the passages named in [section 1](#normative-floor) and [section 6](#bound-blinded-state), and for the absence of EVAC, reversion, `xfr` and `rxr`. Mined in raw/03 and raw/19.
- AI deck — KERI: The last best hope for individual-controlled digital ID in an AI world, Samuel M. Smith. SmithSamuelM/Papers, presentations/KERI_AI_Cyber_2026.pdf, master @`b47f21597` (2026-08-11), added `b218b5b` (2026-06-29). A list of questions, not a position paper; its answers are spoken. Quoted by page from text extracted to `.ignored/papers-text/`, whose ligatures (fi, ff) are damaged. Mined in raw/19.
- AlphaOmega deck — KERI general overview deck, Samuel M. Smith. SmithSamuelM/Papers, presentations/KERI_AlphaOmega.20250903.pdf, master @`b47f21597`, added `e0b2718` (2025-09-03). Quoted by page from extracted text. Mined in raw/19.
- DAD deck — Authentic Data Supply Chains, DAD architecture, Samuel M. Smith. SmithSamuelM/Papers, presentations/AuthenticDataSupplyChains_DAD_Arch.web.pdf, master @`b47f21597`, last touched `c949ebc` (2022-05-20). Lineage only. Mined in raw/19.
- EVAC deck — ACDCs for Delegable Authorization, Samuel M. Smith, the deck behind the KERIConf26 talk The Future of KERI. SmithSamuelM/Papers, presentations/AuthorizationEVAC.pdf, master @`b47f21597`, added and last touched `3ec04c2` (2026-04-30). Slide text, not specification prose; quoted by page from extracted text with damaged ligatures. Mined in raw/19.
- KAGI — KERI Architectures for Group Issuance, Samuel M. Smith. SmithSamuelM/Papers, whitepapers/KERIArchGroupIssuance.md, master @`b47f21597`, last changed `e8a56a9` (2025-02-05). Only its group-issuance half is used here; its KRAM half is in raw/15. Mined in raw/19.
- KERIConf26 caption — edited auto-captions of the KERI Conference 2026 talks, keri-foundation/CONF26-subtitles, subtitles/*.fixed.srt, read at `006042d39` (2026-10-04). Talks quoted or cited: Samuel Smith, The Future of KERI; Phil Feairheller, ACDCs for Authorization; Cole Davis, Contract Credentials and Verifiable Identity (the caption file's title uses an ampersand); Alan Davies, ACDCs for Enterprises; Daniel Hardman, Open Verifiable Communications. A weak provenance class: near-wording only, quoted only for intent and framing; read raw/14 section 0 before quoting any of it onward. Mined in raw/14 and raw/19.
- keripy — KERI reference implementation, WebOfTrust/keripy, `main` @`80f77b73b` (2026-10-01). Read for this chapter: `src/keri/core/structing.py` (the `BoundState` structure and its properties) and `src/keri/acdc/regeventing.py` (`vetBlind`), plus a `git grep` over `src` and `tests` for consumers of the bound fields. Other [code] claims are linked to the chapters that read them. Mined in raw/09, raw/19 and raw/21.
- keripy conversations — Sam Smith's comments in WebOfTrust/keripy discussions: #1082 (comment of 2026-04-23), #1550 (body of 2026-07-28 and comment of 2026-08-05), #1566 (comment of 2026-07-30), #1573 (comment of 2026-08-07). Read from the 2026-10-14 fetch cached under `.ignored/sam-rulings-cache/`, at their edited text where edited. [proposal] throughout. Mined in raw/21.
- ManyCubed.md — Many Cubed, Samuel M. Smith. SmithSamuelM/Papers, whitepapers/ManyCubed.md, master @`b47f21597`, last changed `667c79b` (2017-07-13). Lineage only. Mined in raw/19.
- Revocation.md — Revocation, Samuel M. Smith, self-versioned V0.4 2026/06/13. SmithSamuelM/Papers, whitepapers/Revocation.md, master @`b47f21597`, last changed `3854b8d` (2026-06-14). States the registry transfer event in the present tense; it is in neither ACDC branch ([section 6](#transfer-drift)). Mined in raw/19.
- sda.md — The Shape of Delegated Authority, Daniel Hardman, version 1.2, revised 2026-07-14. dhh1128/papers, sda.md, read at repository `main` @`68a5e2f76` (2026-09-28), file last changed `24c18bb` (2026-07-30). An authored position by the corpus's owner, not community doctrine; on one point ([section 5](#state-rule)) its literal wording is stricter than KERI's registry design and than its own section 8. Mined in raw/06 and raw/19.
