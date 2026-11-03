# 10 — Presentation Registries and Issuee-Side Detectability {#registries}

## Thesis {#thesis}

KERI answers key compromise with detect and recover, and for the Issuer that answer is built: an ACDC's state is anchored in a TEL that is anchored in the Issuer's KEL, so an Issuer can see issuances it did not make without anyone's cooperation. The Issuee has no equivalent. A thief with an Issuee's keys can present its credentials, and the real Issuee has nowhere to look. A presentation registry, which Sam first called an Issuee usage registry, closes that asymmetry: the Issuee keeps its own blindable state registry, a presentation must be anchored in it, and the Issuee can detect presentations it did not make and rotate to invalidate them.

Two things set it apart. It is deliberately optional, on a quantitative argument: Issuer compromise is rampant and high-ROI, Issuee compromise localized and low-ROI, so Issuee-side detectability is something an Issuee elects and pays for. And one mechanism does two unrelated jobs, impersonation-fraud detection and correlation resistance, with different preconditions, so a design can satisfy one and not deliver the other. Confusing them is the likeliest error in this area.

## Status {#status}

Pre-normative, and partly built in keripy only. The markers must be held apart because code and specification say different things.

- [code] at keripy `94f5423a3`, for `/ipex/grant` only. The verifier check exists and fails closed: every Issuee registry declared in a disclosed node's attribute section must bind the `grant`, as of the receiver's KRAM acceptance time, and the requirement is read from issuance metadata on every `grant`, independent of `ax`. The one exemption is the origin's own declaration when the `grant` is that credential's issuance to its Issuee. The Issuee's write path exists. The V2 IPEX handler that does this has no caller in `src/keri`, so this is tested code in the reference implementation, not behavior any shipped keripy command performs ([section 7](#keripy-verifier)).
- [proposal]: retrieval of a foreign registry, #1095's acceptance delay, a presentation registry on an ACDC with no Issuer state registry, the correlation-protected self-issued bespoke origin, and the design's whole rationale.
- No [spec] or [spec-next] text, beyond one word ([section 5](#normative)). A peer implementation built from either specification line will produce `grant`s keripy refuses, with no normative text to say why ([section 8](#adversarial)).

The code is a subset of #1613 that departs from it twice: a registry binding authenticates the `grant` without the Issuee's endorsement, where #1613 says "the grant message must be endorsed by each Grantor", and the requirement applies to every declaration whoever sends, issuance apart, where #1613 conditions it on the Issuee being the Grantor ([section 6](#registrar-and-kram), questions 8 and 9).

### Two names, and searching one misses the other {#two-names}

Sam calls it an Issuee usage registry in [#1095](https://github.com/WebOfTrust/keripy/discussions/1095) (October 2025), the document that invents the idea and carries most of its security reasoning, and a presentation registry in [#1613](https://github.com/WebOfTrust/keripy/discussions/1613) (August 2026). A search for "presentation registry" misses #1095. In speech he has said "user presentation registry" (KERIConf26 caption, Samuel Smith, The Digital Identity Tradespace, 14:36). keripy uses the narrow vocabulary: "presentation registry" in `ipexing.py`, "issuee-controlled registry" in the registry facade (keripy acdc/registraring.py, Registrar.present, L419 @94f5423a3), a binding kind `'presentation'` with TEL state `"presented"`, and a `tethered` set for the Issuees a registry authenticates; "Usage registry" occurs nowhere in keripy's `src/` or `tests/`. A survey needs all of these terms. This chapter uses "presentation registry" for the IPEX-anchoring application and "usage registry" for the general primitive ([question 1](#q-name)).

A neighboring vocabulary is easy to mistake for this one. [proposal] [#1740](https://github.com/WebOfTrust/keripy/discussions/1740) (Auxiliary Messages for IPEX with Blindable State Registries, 2026-10-30) proposes `/ipex/dhke` and `/ipex/unblind` exchanges because "Both an IPEX issuance exchange and an IPEX presentation exchange need the exchange of auxiliary data related to the blindable state registries" (#1740 > Introduction). Its registries are the Issuer's state registries, and it never says "presentation registry", "usage registry" or "issuee-controlled". Its "presentation exchange" is an IPEX presentation, not a presentation registry. [chapter 08](08-presentation-architectures-and-ipex.md) is its home. Nothing in keripy implements either exchange.

## 1. The asymmetry that motivates it {#asymmetry}

### Issuer-side detectability {#issuer-detectability}

[proposal] #1095 names the catastrophic failure as Issuer key compromise: "The ROI to an attacker for compromising the Issuer keys could be huge, especially if that Issuer is a root-of-trust for Identity assurance for an ecosystem." Anchoring answers it: "The impersonator MUST anchor the ACDC in a TEL that is anchored in the Issuer's KEL. This anchor enables the Issuer to detect any fraudulent issuances without requiring the cooperation of any other party, such as the Verifier." Detection with no dependency on a counterparty is the KERI-shaped part. Sam's comparative claim, "AFAIK, only KERI/ACDC provides such protection in a decentralized identity system", is his assessment, not a surveyed result.

### Issuee-side detectability {#issuee-detectability}

[proposal] "If a given Issuee's keys are compromised, the impersonation fraud is localized to that specific Issuee. It does not have rampant potential." #1095 draws three consequences.

1. Low susceptibility, with a cheap mitigation: prophylactic rotation, effective "because the verifier always checks the presentation as being signed by the latest keys of the Issuee." Rotating without reissuing "is a unique super-power of KERI/ACDC as a decentralized identity system."
2. Localized harm licenses localized measures, such as a Verifier requiring a rotation as part of a presentation, and Sam concedes the doctrinal cost: "This violates the maxim that security not be dependent on a trusted third party, but for localized harm, the party most likely to be harmed is the Verifier (Validator), which provides incentives for them to protect themselves." This is a knowing relaxation of the no-trusted-third-party maxim, and [section 8](#ttp-concessions) records a second one.
3. The Issuee can elect its own detectability. That is the usage registry.

It costs infrastructure: "the Issuee must have its own Registrar to manage its usage registries", and "Many Issuees will feel that their key management is sufficient to protect against key compromise and therefore would not want the extra protection and friction of a usage Registrar." Any argument that it should be mandatory has to answer that cost.

### Rotate, do not revoke {#rotate-not-revoke}

[proposal] A compromised Issuee key is answered by key state, not credential state: "if the keys get compromised then the keystate is changed not the ACDC state." And the two registries differ in kind: "A presentation registry on the other hand is not tracking ACDC state, but is merely logging presentations" (keripy discussion #1574, comment of 2026-08-07, R-042, https://github.com/WebOfTrust/keripy/discussions/1574#discussioncomment-17938568). It makes presentations, not the ACDC, perpetually verifiable, so impersonation at presentation time becomes detectable by the Issuee.

### Where it sits among the tiers of IPEX {#ipex-tiers}

[proposal] Sam's four tiers of IPEX ([chapter 08, section 10](08-presentation-architectures-and-ipex.md#four-tiers)) place the registry as an add-on at either stakes level: "This enables the presenter to detect if anyone has compromised the Presenter's keys and is fraudulently using those keys" (keripy discussion #1512, comment of 2026-07-22, R-062, https://github.com/WebOfTrust/keripy/discussions/1512#discussioncomment-17737728). An Issuee or EGF that does not want it still has the signed-only and anchored tiers.

### Optional to use, but not to be foreclosed {#not-foreclosed}

[proposal] [#1098](https://github.com/WebOfTrust/keripy/discussions/1098) (ACDC with Static Age Predicate Proof SMT, last edited 2026-09-26) rejects unlinkable ZKP predicate proofs on detectability grounds, for the Issuer and then the Issuee: "Likewise, the key compromise of an Issuee (Holder) can be made detectable using a presentation registry. Which would also be defeated by an unlinkable ZKP." `raw/16` section 1a reads this as consistent with optionality, since detectability "can be made" available, while treating the possibility of a presentation registry as something a cryptographic choice may not foreclose; that reading is the note's, not Sam's. Without the edit history, the sentence is evidence of his position at 2026-09-26 only.

## 2. The mechanism {#mechanism}

### The rule {#original-rule}

[proposal] #1095: "The ACDC must include a requirement that the ACDC is only verifiable when the presentation of the ACDC by the Issuee is anchored as the latest state in an Issuee-controlled *usage registry*." In IPEX terms the anchored object is the `grant`: "the value of the registry `rd` field in the attribute `a` section MUST be the SAID of the `rip` event of the associated presentation Registry. The Issuee of the associated ACDC, who is also a Grantor of that IPEX, MUST control this registry. The value of the ACDC SAID field in the blinded attribute block of the latest non-vacuous event in that presentation Registry must be the SAID of the `grant` message." (#1613). The slot that normally carries an ACDC SAID carries a `grant` SAID.

### Three of four requirements in keripy {#requirements-in-keripy}

[code] At `94f5423a3` three of those requirements hold and one does not (`raw/16` section 2.2). The `rd` must be the registry's `rip` SAID, or `_vetRegistry` raises `MisregistryError`. The Issuee must control the registry: `vetBinds` checks "if controller is not None and record.issuer != controller:" (keripy acdc/regeventing.py, vetBinds, L714 @94f5423a3), with the `a`-section `i` as controller. The latest non-vacuous event must bind the `grant` SAID (keripy acdc/ipexing.py, IpexHandler._verifyPresentationAuthGraph, L2195 @94f5423a3). The clause "who is also a Grantor of that IPEX" is not enforced; the registry alone authenticates the Issuee ([question 9](#q-single-vs-double)). The Issuee writes with `Registrar.present`, "Bind a grant message SAID in an issuee-controlled registry." (keripy acdc/registraring.py, Registrar.present, L419 @94f5423a3), and `vacate` writes a vacuous update. `present` does not check that its caller is anyone's Issuee; only the verifier's incepter check enforces control.

### One registry for many credentials {#many-to-one}

[proposal] "A *usage registry* can be employed to track the usage of one or more ACDCs by the Issuee… This means that the registry does not leak specific usage of a given ACDC to third parties" (#1095). Blinding is what makes many-to-one safe; unblinded, a shared registry would be a correlation engine.

### Detection converted to prevention {#acceptance-delay}

[proposal] #1095 alone offers this: "by adding a time delay from presentation anchor to acceptance, the verifier can assume that a compromised Issuee would do a recovery, invalidating the fraudulent presentation." It is the only proposal in the corpus that turns Issuee-side detection into prevention, and its cost, that every honest presentation waits, is a tradeoff an EGF should set. keripy does not implement it.

### Incentive alignment {#incentive-alignment}

[proposal] #1613 puts it as liability: a verifier accepting an unanchored grant "is presumptively in violation of any contractual or regulatory protection afforded to the real Grantor by colluding with a fraudulent grantor."

## 3. Two jobs, two different preconditions {#two-jobs}

The mechanism is the same in both jobs and the guarantees are not.

### Job one: impersonation-fraud detection {#job-fraud-detection}

[proposal] This requires that the Issuer is not the Grantor. The requirement is baked in by a party the attacker has not compromised: "an imposter that merely compromises the Grantor's signing infrastructure can't avoid the requirement without also compromising the Issuer." The Grantee refuses an unanchored grant, and the real Issuee sees registry events it did not create and rotates. The hole is self-issuance, which #1613 states: "An imposter who controls the Grantor's signing infrastructure can create ACDCs whose authentication factor is an unanchored signature." So fraud detection is a property of the three-party arrangement, not of the registry.

[code] keripy builds the verifier half, including the property that the Grantor cannot opt out: "The disclosed Issuee registry makes its proof mandatory for this proxy presentation; omitting it must not disable the check." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_presentation_registry_binds_proxy_grant, L8213-8214 @94f5423a3). Compacting the attribute section cannot hide the declaration, because a registry-backed ACDC whose `a` is compact is refused: "A compact attribute commits to the same ACDC but hides whether the issuer mandated this presentation registry." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_presentation_registry_binds_proxy_grant, L8291-8292 @94f5423a3). The aggregate section plays no part in this ([question 10](#q-aggregate-disclosure)). The requirement binds whoever presents, the Issuer included: "When the Issuer discloses the credential to someone other than its Issuee, it is a presentation and the declaration applies." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_presentation_registry_binds_proxy_grant, L8252-8253 @94f5423a3). Only the Issuer's issuance `grant` to its own Issuee is exempt, and only for the origin being issued ([section 7.2](#fails-closed)). Nothing checks that Issuer and Issuee differ, so the self-issuance hole is present in code exactly as #1613 concedes it.

### Job two: correlation resistance {#job-correlation}

[proposal] This works even self-issued. If Grantor and Grantee each anchor the same `grant` SAID in their public KELs, "a third party… would be able to detect the same grant SAID in both the Grantor's KEL and the Grantee's KEL, thereby correlating the IPEX." In a blinded presentation registry, "neither the grant SAID nor any other artifacts of the granted DAG appear in the KEL of the Grantor," which removes the join point. A Grantor needs no cooperating Issuer for this: it self-issues a bespoke origin carrying `i` and `rd` in its attribute section. One constraint is easy to violate: "the bespoke ACDC itself must use a blinded state Registry for its Issuer authentication so that the SAID of its ACDC is not correlatable. If it uses a direct KEL anchor, then that anchor itself would be correlatable." Nothing in keripy forbids this construction and no test builds one, so whether it composes is untested.

The single-origin rule this relies on, that one anchor covers a DAG because committing to the origin commits to everything reachable, is [spec-next]: "That DAG MUST have exactly one source node, called the origin node" (ACDC spec > Disclosure Paths > DAG of ACDCs, L1821 @2362e48a1), with a bespoke origin where the ACDCs are unchained ([chapter 08, section 2](08-presentation-architectures-and-ipex.md#one-dag-one-origin)). `v1.1` does not say such an origin needs a blinded state registry ([question 7](#q-two-bespoke-origins)).

### Correlation resistance is itself conditional {#correlation-conditional}

[proposal] The registry is "bound to the AID of the Issuee, so it is linkable. A bulk-issued ACDC with independent AIDs can remove this linkage" (#1095). Full unlinkability needs blinded state and independent-registry bulk issuance; used naively, a presentation registry hides which credential was presented while advertising that the Issuee presented something.

### Multi-ACDC DAGs {#multi-acdc}

[proposal] Because the `grant`'s origin `o` names the DAG origin, one registry anchor "provides a perpetually verifiable proof of the presentation of all ACDCs in that DAG, but not necessarily a fresh proof of control for all Issuee AIDS in that DAG. Multiple anchors in different registries provide multiple vectors of detectability and multiple fresh proofs-of-control; the perpetual verifiability is redundant." That `o` is an exchange-message field defined in no ACDC branch, where `o` is the edge Operator; the concept it names is [spec-next] and the field is [proposal] and [code].

[code] keripy implements the strict form: "One valid presentation registry cannot replace the child's proof." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_verifies_presentation_registries_for_different_issuees, L8521 @94f5423a3). Each binding is also a fresh proof of control for its Issuee, so a declared registry cannot be ignored. Declarations are honored on any node, and the SEDI examples cover the DAG with one anchor by practice rather than rule: "Residence needs only issuer proof; Core owns the presentation proof." (keripy tests/sedi/test_ipex_sedi.py, test_residence_sedi_uses_nested_core_presentation_registry, L2739 @94f5423a3).

## 4. The trigger, and the ambiguity blocking it {#trigger}

### The signal is a three-part test {#three-part-signal}

[proposal] Per #1613 the requirement fires when a non-empty `rd` and a valid Issuee `i` sit at the top level of the ACDC's attribute section and the ACDC's own top-level `rd` is non-empty. With no Issuee in `a`, an `rd` there imposes nothing; with the top-level `rd` empty or missing, the inner `rd` "refers to an ACDC state registry, not an IPEX presentation registry." The top-level `rd` does disambiguation work that a quick reading misses.

### Why disambiguation is needed {#why-disambiguate}

[proposal] The v1 spec also permits `rd` in `a` as a hidden ACDC state registry, so one slot carries two meanings. #1613 offers EGF-declared purpose with presentation as the default, then argues the hiding case down, since its only benefit arises "when the ACDC in compact form is made public, independent of any given presentation", and floats: "Given the potentially dubious value, we might want to forbid using the `rd` field in the attribute section for an ACDC state registry." It ends "Not sure if either is a worthy use case", and a trigger cannot be specified on a field whose meaning is contested.

The choice is permanent per ACDC: "a presentation registry may not be used with an ACDC that uses the `rd` field in the attribute `a` section as an Issuer-controlled ACDC state." An Issuer choosing the hiding case forecloses Issuee-side detectability on that credential, while #1613 judges hiding "is not useful with full independent Registry bulk issuance since each presentation could use a different member of the bulk issued set". `v1.1` has not taken up any of #1613's options: its Registry SAID Field section and reserved-fields row are byte-identical to `main` ([question 2](#q-disambiguation)).

### keripy has made the choice {#keripy-choice}

[code] keripy implements the three-part test on the attribute section only: "Only the top-level attribute pair declares a presentation registry." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_finds_attribute_presentation_registry, L7977 @94f5423a3), so each node declares at most one presentation registry. That matches #1613, which names the attribute `a` section and no other. It refuses the hiding case. Without a top-level `rd`, an inner `rd` is a "hidden issuer registry, not a presentation registry." (keripy acdc/ipexing.py, IpexHandler._presentationRegistries, L2110 @94f5423a3) and the ACDC fails, with no fallback to a signature (keripy tests/acdc/test_ipexing.py, test_ipex_v2_rejects_hidden_issuer_registry_signature_fallback, L5504 @94f5423a3). That is an implementation choice, not a resolution, and it means a v1-conformant ACDC using `a.rd` as a hidden state registry is rejected by keripy's V2 verifier.

#1618 suggests an anchored exchange "would also need an `rd` on the exchange". keripy does not do that: the registry is found from the DAG, as #1613 requires, "the registry must be pre-specified in one of the ACDCs in the granted DAG". The question stays open for the specifications.

## 5. What is normative: one word {#normative}

[spec] In the ACDC specification on `main` @`f0bd097de` and `v1.1` @`2362e48a1`, "Presentation registry" has zero occurrences and "usage registry" occurs once. What exists:

- The nested-`rd` purpose list includes usage: "Issuance and/or revocation, transfer, retraction, or usage registry for ACDC when not at top-level" (ACDC spec > ACDC Structure > Other Reserved Fields, L48 @f0bd097de). That word is the only trace of this design in any specification.
- Nested `rd` "MAY be used for some other registry, such as an application-specific or Issuer-specific registry" (ACDC spec > ACDC Structure > Registry SAID Field, L85 @f0bd097de); its stated rationale is bulk issuance and graduated disclosure, not fraud detection. Neither branch contemplates an Issuee-controlled registry: "Issuee-controlled", "Issuee controlled" and "Issuee's registry" occur zero times at `2362e48a1`. keripy has one, so this is now a gap between the specifications and the reference implementation.
- Blindable state registries and `rip` are fully normative. A `rip` is "a vacuous placeholder that reveals nothing about what will later be issued," the source of #1613's "latest non-vacuous event".

### The worked lifecycle states the correlation boundary {#correlation-boundary}

[spec] The Registry-Dependent Issuance Lifecycle states what a blindable registry buys: "This is confidentiality of registry state, not anonymity of the credential — issuer, registry, and issuance chronology remain linkable, which is the intended, auditable trade-off." That is the normative form of #1095's caveat in [section 3](#correlation-conditional): linkability of the registry is the chosen trade, not an oversight, and spec text for presentation registries will need to say the same of an Issuee's registry. The lifecycle runs Issuer-side end to end; the Issuee only holds the shared salt.

### One wording tension {#wording-tension}

[spec] "Because the Issuer `i` field appears in the `rip` event, the Registry SAID, `rd` field value cryptographically binds the Registry to the Issuer AID" (ACDC spec > Transaction event logs (TELs) as ACDC state registries > Registry SAID, `rd` field, L2019 @f0bd097de). For a presentation registry the incepter is the Issuee. The sentence is about the registry's own incepting controller and is not wrong, but it assumes Issuer and incepter coincide. keripy reads it the way this design needs: the check that the ACDC's "issuer must match the issuer that incepted the presented registry" (keripy acdc/regeventing.py, vetBindings, L494 @94f5423a3) runs only for a top-level `rd`, and the presentation path checks the Issuee as incepter instead ([question 5](#q-rip-text)).

## 6. Where this sits against Registrar/Observer and KRAM {#registrar-and-kram}

### It extends the governance split to a third party {#governance-split}

[Chapter 05, section 9](05-acdc-and-verifiable-data.md#registries) records Sam's framing that the Registrar/Observer split replays witness/watcher one layer up: "We have registrars controlled by the issuers, and observers controlled by the verifiers" (KERIConf26 caption, Samuel Smith, The Digital Identity Tradespace, 16:58). A presentation registry adds an Issuee-controlled Registrar, so the Holder, previously the one party running no state infrastructure, now runs some. "We shouldn't have shared governance" (KERIConf26 caption, Samuel Smith, The Digital Identity Tradespace, 16:54), applied consistently, gives every party to a transaction its own state service; that synthesis is this chapter's. Sam's own phrasing is that it "allows presenters to detect compromise of their proofs that are in their credentials that they're presenting" (KERIConf26 caption, Samuel Smith, The Digital Identity Tradespace, 14:44). These are edited auto-captions; read `raw/14` section 0 before quoting them.

### It sits inside KRAM's window {#kram-window}

[proposal] "in order to pass KRAM, a `grant` message anchor must happen in a timely fashion relative to the IPEX exchange." (#1613). A registry write thus enters the critical path of a freshness window, and #1095's acceptance delay adds latency on top; nothing in the corpus connects the two numerically ([chapter 09, section 3](09-kram-and-request-authentication.md#full-kram)).

### keripy couples the two differently {#rdt-coupling}

[code] In keripy the registry check depends on KRAM rather than the write having to pass it. KRAM's transactioned-message cache records `rdt`, "receiver datetime when KRAM accepted the complete message" (keripy recording.py, TxnMsgCacheRecord, L532 @94f5423a3), set for a multi-key sender only once its threshold is met. The registry check refuses without it, "A presentation requirement needs a completed KRAM acceptance." (keripy acdc/ipexing.py, IpexHandler._verifyPresentationAuthGraph, L2181 @94f5423a3), and cuts the registry history off at it: "Require a valid binding anchored before the KRAM-accepted send." (keripy acdc/ipexing.py, IpexHandler._verifyPresentationAuthGraph, L2200 @94f5423a3). Three consequences follow (`raw/16` section 2.2): the test compares the TEL event's own `dt`, which the Issuee asserts, against the receiver's clock; the KEL event anchoring that TEL event may arrive later, through escrow; and since the bound target is this `grant`'s SAID, the binding is made after the `grant` body is fixed. `raw/15` section 4.8 infers, untested, that a deployment with KRAM disabled cannot accept a `grant` carrying a declaration. No specification mentions a receiver acceptance time consumed by another protocol.

### The registry anchor adds to the ordinary one {#double-authentication}

[proposal] "KRAM does not recognize or process a presentation registry-based authentication factor for the grant message," so "a presentation registry-anchored grant message is always double-authenticated," which is "unavoidable because the processing of presentation registry validation happens higher up in the stack than grant message authentication." (#1613). The registry write adds to the signature or KEL anchor rather than replacing either, and a verifier that treats it as a replacement will err one way or the other. keripy's `kraming.py` has no presentation-registry logic beyond `rdt`, and the check sits in `ipexing.py`, above KRAM, as #1613 says it should.

### keripy confirms the layering for the sender only {#sender-layering}

[code] When the declared Issuee also sends the `grant`, as in every SEDI test, double authentication holds by construction. When it does not, keripy does not require the Issuee to endorse: "The proxy signature authenticates the sender while the timely Issuee TEL supplies Bob's fresh proof without multiple endorsement." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_presentation_registry_binds_proxy_grant, L8186-8187 @94f5423a3), and the test asserts that no Issuee signature or seal was stored. #1613 says the opposite: "To be accepted by KRAM, the grant message must be endorsed by each Grantor". A check requiring the endorsement was written and withdrawn inside PR #1693: "A registry supplements, but never replaces, a Grant endorsement." (keripy acdc/ipexing.py, IpexHandler._verifyPresentationAuthGraph, L1564 @790797bcd) is gone at `b7c170f93`, so `main` never enforced it. The positions can be reconciled, since a registry anchor is a KEL-anchored commitment to the exact `grant` SAID and in effect makes the Issuee a Grantor without an endorsement, but #1613 does not record that design change. A side effect follows from the code, untested: the endorser index `eidx` (keripy db/basing.py, Baser, L608 @94f5423a3) is filled from accepted non-sender endorsements only, so a registry-only Issuee is not indexed against the `grant` ([question 9](#q-single-vs-double)).

### Independent of `ax`, and counted toward it {#independent-of-ax}

[proposal] #1613 makes the anchor independent of `ax` ("Notwithstanding the presence or absence of the ax field") where an Issuer-signaled presentation registry applies and the Grantor is the Issuee: "then that grant message MUST be anchored in that registry for the grant to be valid." (#1613 > New Anchored Exchange ax Field). `ax` lets a party request perpetual verifiability; a presentation registry lets an Issuer impose it at issuance, and the Grantor cannot opt out ([chapter 08, section 10](08-presentation-architectures-and-ipex.md#anchoring)). keripy runs the check on every presentation `grant` whether or not `ax` is present. [code]

[code] A registry anchor also counts toward `ax`. Under "A truthy ax requires one permitted Grant anchorer." (keripy acdc/ipexing.py, IpexHandler.verify, L797 @94f5423a3), the anchorer set starts from the registry-authenticated Issuees, "anchorers = set(tethered)" (L801), and is accepted if it contains any of "candidates = (serder.pre, origin.iseaid, origin.israid)" (L816), the sender and the origin's Issuee and Issuer. That realizes #1613's origin-AID anchoring rule as set membership, so its "order of priority" has no operational effect.

### Which registry may be used {#which-registry}

[proposal] "There is no security advantage to using a presentation registry specified by the Grantor, as the main purpose… is to allow the Grantor to detect a compromise of its signing key infrastructure". keripy agrees in effect: it recognizes only registries declared in a DAG node, and nothing on the `grant` can name one. [code] #1613 would reuse "the existing tooling for a bulk-issued ACDC"; the Issuee's write path reuses the `_blind` path of Issuer issuance, and whether bulk-issuance tooling serves presentation registries was not examined.

## 7. keripy: the verifier side is built, for `grant` only {#keripy-verifier}

[code] at `94f5423a3` throughout (`raw/16` section 7). The verification, the `present`/`vacate` pair and non-sender `grant` endorsements came in PR #1693 (merged 2026-09-28), PRs #1689 and #1697 put Issuee presentation registries into the SEDI example schemas, and PR #1734 (merged 2026-10-26) reworked proxy `grant`s that use presentation registries; those titles are used for status only. One boundary bounds every claim here: `acdc/ipexing.py` is the V2 IPEX handler, its `loadHandlers` has no caller in `src/keri`, keripy's CLI wires the V1 handler, and the v1 `vdr` verifier has no presentation registry ([chapter 08, section 6](08-presentation-architectures-and-ipex.md#two-ipex)).

### 7.1 What is implemented {#implemented}

On every `/ipex/grant` that discloses a DAG, after the DAG walk, the disclosure-plan and Offer-fulfillment checks, the evaluation of the disclosed DAG and per-node schema validation pass, `IpexHandler.verify` runs `_verifyPresentationAuthGraph`: "Verify every presentation registry declared for this disclosure." (keripy acdc/ipexing.py, IpexHandler.verify, L788 @94f5423a3). For each node with a top-level `rd`, it reads the `(i, rd)` pair at the top level of a disclosed `a`; aggregate entries are not consulted. When the `grant` is an issuance, its sender the origin's Issuer and its recipient `ri` the origin's Issuee, the origin's own declaration is skipped and every other node's still applies. For each remaining pair it requires that the registry is incepted by that `i`, that its latest non-vacuous update as of KRAM acceptance binds this `grant`'s SAID, and that the node carries a KEL source reference from the Issuee to the binding event. Any failure rejects the `grant`. The Issuees so authenticated form the `tethered` set and count as anchorers for `ax`. No other verb consults a presentation registry, matching #1613's statement that the `grant` is "the presentation".

Beside this check sits a separate one for the Issuer's state registry named by a node's top-level `rd`. Its chain is still authenticated, but the state it discloses is written to the `exrs.` table for an application or EGF to judge: "Recorded, never judged on the protocol path." (keripy db/basing.py, Baser, L596 @94f5423a3). That applies to Issuer-registry state only. The presentation registry's binding requirement is not a state judgment and is enforced in full, and `_verifyPresentationAuthGraph` writes nothing to `exrs` ([chapter 08](08-presentation-architectures-and-ipex.md) covers the state axis).

### 7.2 Where it fails closed {#fails-closed}

Each step refuses rather than skipping (`raw/16` section 7.2): a registry-backed node with a compact `a`, or a malformed `rd` or `i` in it; an inner `rd` without a top-level one ([section 4](#keripy-choice)); a `grant` without completed KRAM acceptance. The TEL must be held locally — "Registry verification requires an injected local Regery." (keripy acdc/ipexing.py, IpexHandler._registryEvidence, L1980 @94f5423a3) — and a missing `rip` or update raises a retryable `MissingChainError`. Updates after KRAM acceptance are ignored, so a later presentation cannot displace an accepted one. The binding event must be sealed in the Issuee's KEL: "Presentation timing requires the Grant to carry this bup's KEL source." (keripy acdc/regeventing.py, vetBinds, L750 @94f5423a3). A valid registry cannot be substituted for the declared one (keripy tests/acdc/test_ipexing.py, test_ipex_v2_rejects_substituted_presentation_registry, L8346 @94f5423a3). Nothing falls back to a weaker factor.

One case is exempt, and the line is drawn narrowly. The exemption is "Only the origin being issued is exempt." (keripy acdc/ipexing.py, IpexHandler._verifyPresentationAuthGraph, L2168 @94f5423a3), where issuance means the `grant`'s sender is the origin's Issuer and its recipient the origin's Issuee. The proxy test shows both sides: "The same declaration is inactive while the Issuer grants the credential to its Issuee." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_presentation_registry_binds_proxy_grant, L8236-8237 @94f5423a3), while the same Issuer sending the credential to anyone else is presenting it ([section 3](#job-fraud-detection)). A linked credential in an issuance `grant` is not exempt: "Omitting the child's declared registry must not be excused by the fact that the origin is undergoing original issuance." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_verifies_presentation_registries_for_different_issuees, L8588-8589 @94f5423a3).

A presentation registry does not meet the edge case #1740 proposes `/ipex/unblind` for, a verifier holding registry events later than the presenter disclosed, because its history is cut off at KRAM acceptance and its controller is the Issuee who writes it (`raw/16` section 8 item 17).

### 7.3 Who must act, and what is still absent {#still-absent}

The Issuee writes through `Registrar.present` and `vacate`, and `grant(..., anchorers=[])` omits the sender KEL anchor: "empty list leaves anchoring to a presentation registry." (keripy acdc/ipexing.py, grant, L2611 @94f5423a3). `grant()` also takes non-sender endorsers and anchorers, validated after KRAM, and the declared Issuee need not be among them. Whether non-sender signature groups are threshold-checked was not established, and #1613's tethering is not implemented. PR #1693 implements multiply endorsed grants against #1555, which this corpus compares only through #1613's restatement.

Still absent: retrieval of a foreign registry — the tests "Simulate the future observer retrieval layer by preloading the" foreign TEL (keripy tests/acdc/test_ipexing.py, test_ipex_v2_full_authentication_flow_across_three_haberies, L8954 @94f5423a3), so in deployment such a `grant` escrows or fails unless the TEL arrived out of band; a presentation registry on an ACDC without an Issuer state registry; a presentation registry declared in an aggregate entry; a tested self-issued bespoke origin; #1740's `/ipex/dhke` and `/ipex/unblind`; and any specification text. A registry an Issuee stands up without an Issuer's declaration is ignored.

### 7.4 The three-factor framing {#three-factor-framing}

#1618 states symmetrically that three factors apply to the presentation: "Grant is signed (normal)", "Grant is anchored in a presentation registry (issuee-controlled; `rd` on the origin ACDC can force the check)", and "Grant is anchored in a KEL without a presentation registry (a case V1 did not really specify)". The list is unnumbered in the source, and its author withdrew it the same day as a duplicate of #1613, so it is a compact restatement, not corroboration. All three legs are [code] in V2. The framing's parenthesis is narrower than the code, which honors a declaration on any node, not only the origin. The KEL-anchor leg shipped first, in PR #1674, which said presentation-registry anchoring "will come in a follow up PR"; that the cheaper leg came first is what cost predicts and says nothing about either design's merits.

## 8. Reading this adversarially {#adversarial}

### The origin document has had no engagement {#no-engagement}

#1095 has zero comments in eleven months. That silence does not reflect the design's status: Sam names presentation registries in a #1627 comment of 2026-09-02, "This anchor in the KEL only applies when their is not a presentation registry being used by DAG ACDCs", PR #1674 promised the work in writing, and keripy has built the verifier. #1627's body, through its 2026-09-11 edit, never mentions a presentation registry; Sam's own survey of the presentation tradespace reaches for one only when asked about anchoring. A dead thread is not a dead idea.

### The novelty claim is unverified {#novelty-claim}

"nobody else does as far as I've never seen anybody do it" (KERIConf26 caption, Samuel Smith, The Digital Identity Tradespace, 14:40) and "AFAIK, only KERI/ACDC provides such protection" (#1095) are hedged by their author. Holder-side presentation logging is not unheard of in the wider VC world. The defensible narrower claim is that here the log is cryptographically required by the credential and enforced by the verifier, not a courtesy audit trail; the broad claim is unchecked.

### Two trusted-third-party concessions {#ttp-concessions}

The first is [section 1](#issuee-detectability)'s, in Sam's words. The second lands on the mechanism itself. #1613 describes what the registry gives the Grantor as "an Issuer-Verifier-protected mechanism to detect compromise of its signing keys". It needs an Issuer that is a different, non-colluding party, the only reason an imposter cannot self-issue a credential demanding nothing ([section 3](#job-fraud-detection)), and a Verifier that enforces: "The verifier then enforces the protection by not accepting presentations (grant messages) that are not so anchored." So the Issuee's self-protection depends on two other parties. Both concessions are stated by their author; a reviewer who quotes the no-trusted-third-party maxim against this design is right about the tension, and the corpus's residuals should name both.

### Refusals no specification states {#unspecified-refusals}

[code] keripy's V2 verifier rejects three kinds of `grant` on presentation-registry grounds (`raw/16` section 8 item 13): one whose ACDC declares an Issuee registry that does not bind it; one with an `a`-section `rd` and no top-level `rd`, which v1 allows as a hidden state registry; and one carrying a registry-backed ACDC whose `a` is compact. The third follows from the first, since a verifier cannot tell an omitted requirement from a hidden one. None has a [spec] or [spec-next] counterpart. A peer built from either specification line will produce `grant`s keripy rejects, which is a conformance hazard; that the handler is not yet shipped, and that `E1E` was also implemented first, does not change what an interoperating implementer faces ([question 8](#q-unspecified-refusals)).

### Code and design document disagree {#code-vs-design}

#1613 conditions the requirement on the Issuee being the Grantor and requires every Grantor to endorse; keripy applies it to every presentation, exempting only the origin of an issuance `grant`, and accepts a registry binding in place of an endorsement ([section 6](#sender-layering)). A reader of #1613 will expect checks the code does not make and miss a refusal it does make, and neither document says the other has moved.

## 9. Open questions {#open-questions}

### Question 1: What is it called? {#q-name}

"Issuee usage registry" (#1095), "presentation registry" (#1613, #1618), "user presentation registry" (caption). #1550's Guardianship for SEDI uses the same primitive for agent capability control, with a legend reading `rd = issuee usage registry SAID`, and #1627 proposes a "transfer registry where a state change is not to revoke an ACDC but to provide a forward reference" to a replacement; the spec's `rd` gloss lists four purposes. With presentation only one use, the general name should probably be the usage one. keripy has chosen the narrow name, which sets the vocabulary most implementers meet first ([section 1](#rotate-not-revoke), [Status](#two-names)).

### Question 2: Does `rd` in `a` get disambiguated, and how? {#q-disambiguation}

Resolved in keripy, open in both specifications ([section 4](#trigger)). The readings are exclusive per ACDC and permanent. Tracked as [chapter 08, section 14, question 5](08-presentation-architectures-and-ipex.md#q-rd-restriction).

### Question 3: Does the exchange need its own `rd`? {#q-exchange-rd}

keripy says no, finding the registry from the DAG; the specifications are silent ([section 4](#keripy-choice)).

### Question 4: What is the latency budget? {#q-latency}

There is no number anywhere. keripy's rule is looser than "must pass KRAM": the Issuee-asserted TEL `dt` must precede KRAM acceptance, and the anchoring KEL event may arrive later ([section 6](#rdt-coupling)). A compromised signer could backdate `dt`, but the backdated event would then be anchored in the real Issuee's KEL and detectable, so the looseness may be acceptable; nobody has written that argument down. Nothing implements #1095's delay.

### Question 5: What would `rip` spec text say? {#q-rip-text}

The spec binds a registry to "the Issuer AID"; for a presentation registry the incepter is the Issuee. keripy reads it as whoever incepted the registry, and the spec text does not say so ([section 5](#wording-tension)).

### Question 6: Who verifies, and against what? {#q-who-verifies}

The Grantee checks against a TEL it must already hold. Retrieval is unbuilt, and whether it should go through the Issuee's Registrar or a verifier-controlled Observer, which watches registrar state exactly as this needs ([chapter 05, section 9](05-acdc-and-verifiable-data.md#registries)), is connected by no source. PR #1674 names "presentation-registry anchoring or observer-based TEL retrieval" as follow-up work without connecting them.

### Question 7: Two incompatible bespoke origin ACDCs share a name {#q-two-bespoke-origins}

#1613's self-issued bespoke origin must use a blinded state registry or hand correlation back at the origin ([section 3](#job-correlation)); #1627's SEDI recipe origin uses no registry, no anchor and bare signatures, because it is one-time use ([chapter 08, section 3](08-presentation-architectures-and-ipex.md#bespoke-origin)). Each is coherent for its job, neither mentions the other, and a worked example combining a presentation registry with a recipe origin yields a correlatable presentation whose perpetual verifiability the origin cannot carry. keripy builds neither combination.

### Question 8: keripy refuses `grant`s for reasons no specification states {#q-unspecified-refusals}

Which side moves: the specifications adopting the three refusals of [section 8](#unspecified-refusals), or keripy relaxing those a peer cannot be expected to know?

### Question 9: Single versus double authentication, and for whom {#q-single-vs-double}

#1613 applies the requirement "when the Issuee is the Grantor of that IPEX" (#1613 > Registry Anchored Granted ACDCs) and requires every Grantor to endorse; keripy applies it to every declaration whoever sends, exempting only the origin's own declaration in an issuance `grant`, and accepts the registry binding alone. They agree when a holder presents its own credential. Under keripy's rule, an ACDC presented as third-party evidence, where "an ACDC is presented as evidence, but the Issuee AID is unrelated to the Discloser's AID", cannot be presented unless its Issuee binds this `grant`, and the same holds for an Issuer presenting a credential it issued to anyone but its Issuee. The choice was made in code and reversed in code: a Grantor-scoped version, commented "Merely appearing in an ACDC does not assign that role." (keripy acdc/ipexing.py, IpexHandler._verifyPresentationAuthGraph, L1900 @8a7f33e0c), is absent at `3c11a4215`. Neither #1613 nor the code says whether unusability as third-party evidence was weighed, and `eidx` misses registry-only Issuees. Should #1613 move to match the code, or the reverse?

### Question 10: What does an `i`/`rd` pair in an aggregate entry mean? {#q-aggregate-disclosure}

Nothing, to keripy. Declaration discovery reads only the attribute section: "Aggregate disclosure state cannot add, remove, or hide that presentation requirement." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_finds_attribute_presentation_registry, L8014-8015 @94f5423a3). A compact or partially disclosed `A` yields no declaration rather than a refusal, so a registry-backed ACDC's aggregate can be selectively disclosed without failing the presentation check. The SEDI Age credential, with a top-level `rd` and an `A`, is therefore not blocked by declaration discovery, though no IPEX test presents it ([chapter 05, section 4.1](05-acdc-and-verifiable-data.md#age-credential)). The open part is the converse, which nothing documents: an Issuer that places an `i`/`rd` pair in an aggregate entry expecting a presentation requirement gets none, silently, "Aggregate registries have application-specific semantics and do not become presentation requirements merely from an i/rd pair." (keripy tests/acdc/test_ipexing.py, test_ipex_v2_finds_attribute_presentation_registry, L7991-7992 @94f5423a3). keripy matches #1613, which speaks only of the attribute section; the hazard is for a schema author who reads the specification's permission that a nested `rd` in the Attributed or Aggregate section "MAY be used for some other registry" ([section 5](#normative)) as license to put a presentation registry in `A`. Should a specification say so?

## Sources {#sources}

- ACDC spec — Authentic Chained Data Containers (ACDC) specification, Trust Over IP. trustoverip/kswg-acdc-specification, spec/spec-body.md. `main` @`f0bd097de` (2026-08-28) for [spec] claims: Other Reserved Fields, Registry SAID Field, Registry-Dependent Issuance Lifecycle, TELs as ACDC state registries. `v1.1` @`2362e48a1` (2026-09-11) for [spec-next] claims: Disclosure Paths > DAG of ACDCs. The negatives in [section 5](#normative) are taken at both pins. Mined in raw/03 and raw/16.
- KERIConf26 caption — edited auto-captions of the KERI Conference 2026 talks (Lehi, Utah, April 2026), keri-foundation/CONF26-subtitles, subtitles/*.fixed.srt, @`006042d39`; this chapter quotes Samuel Smith, The Digital Identity Tradespace. Captions preserve near-wording, never exact speech, and are quoted only for intent and framing. Mined in raw/14.
- keripy — KERI reference implementation, WebOfTrust/keripy, `main` @`94f5423a3` (2026-10-30): `src/keri/acdc/ipexing.py`, `acdc/regeventing.py`, `acdc/registraring.py`, `recording.py`, `db/basing.py`, and the tests `tests/acdc/test_ipexing.py` and `tests/sedi/test_ipex_sedi.py`. Earlier commits on PR branches, each read at its own pin for the one check it carried: `790797bcd` and `b7c170f93` (the Issuee-endorsement check, [section 6](#sender-layering)), `8a7f33e0c` and `3c11a4215` (the Grantor-scoped declaration check, [question 9](#q-single-vs-double)). Mined in raw/16, with raw/09 for the IPEX rework and raw/15 section 4.8 for KRAM's `rdt`.
- keripy discussions — WebOfTrust/keripy GitHub discussions, https://github.com/WebOfTrust/keripy/discussions. [#1095](https://github.com/WebOfTrust/keripy/discussions/1095) (ACDC Issuee Usage Registry, SmithSamuelM, October 2025), [#1613](https://github.com/WebOfTrust/keripy/discussions/1613) (Authentication Factors in IPEX, SmithSamuelM, August 2026), [#1098](https://github.com/WebOfTrust/keripy/discussions/1098) (last edited 2026-09-26, fetched 2026-10-03), [#1618](https://github.com/WebOfTrust/keripy/discussions/1618), [#1550](https://github.com/WebOfTrust/keripy/discussions/1550), [#1627](https://github.com/WebOfTrust/keripy/discussions/1627), [#1740](https://github.com/WebOfTrust/keripy/discussions/1740) (Auxiliary Messages for IPEX with Blindable State Registries, SmithSamuelM, last edited 2026-10-30, fetched 2026-11-03). Cited for Sam's rulings by comment URL from the raw/21 cache of 2026-10-14: [#1512](https://github.com/WebOfTrust/keripy/discussions/1512) (R-062) and [#1574](https://github.com/WebOfTrust/keripy/discussions/1574) (R-042). Mined in raw/16 and raw/21.
- keripy PRs — WebOfTrust/keripy pull requests, cited for status and intent only: [#1674](https://github.com/WebOfTrust/keripy/pull/1674) (merged 2026-09-11), [#1689](https://github.com/WebOfTrust/keripy/pull/1689), [#1693](https://github.com/WebOfTrust/keripy/pull/1693) (merged 2026-09-28), [#1697](https://github.com/WebOfTrust/keripy/pull/1697) and [#1734](https://github.com/WebOfTrust/keripy/pull/1734) (merged 2026-10-26). Mined in raw/16.
