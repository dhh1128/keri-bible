# Doctrine Mining: Presentation Registries (a.k.a. Issuee Usage Registries)

**Primary source:** WebOfTrust/keripy discussion [#1095](https://github.com/WebOfTrust/keripy/discussions/1095), *ACDC Issuee Usage Registry for Detection of Issuee Key State Compromise with Regard to Presentations*, SmithSamuelM, created 2025-10-13, last edited 2025-11-11, category Ideas, ~1,350 words, two diagrams, **zero comments**. This is the concept's origin document.
**Second primary source:** keripy discussion [#1613](https://github.com/WebOfTrust/keripy/discussions/1613), *Authentication Factors in IPEX*, SmithSamuelM, last updated 2026-08-19. Five subsections carry the developed design: *Registry Anchored Granted ACDCs*, *Hiding ACDC State Registry*, *Presentation Registry*, *Fraud Protected Registry*, *Correlation Protected Registry*, plus *New Anchored Exchange `ax` Field*.
**Supporting:** keripy discussion [#1618](https://github.com/WebOfTrust/keripy/discussions/1618) (ryan-hansen, 2026-08-13) for the authentication-factor framing; [#1550](https://github.com/WebOfTrust/keripy/discussions/1550) *Guardianship for SEDI* (SmithSamuelM, 2026-08-05) for a non-presentation use; `raw/14-kericonf-2026.md` §"user presentation registry" for Sam's spoken framing.
**Normative substrate:** `trustoverip/kswg-acdc-specification` `spec/spec-body.md` @`f0bd097` (2026-08-28) — `rd`, `rip`, blindable state registries.
**Implementation:** `WebOfTrust/keripy` `upstream/main` @`4df8e4a8` (2026-09-01).
**Mining date:** 2026-09-01.

---

## 0. Provenance — the vocabulary split is the headline

**The same concept has two names, and searching one misses the other.** Sam calls it an **Issuee Usage Registry** in #1095 (October 2025) and a **presentation registry** in #1613 (August 2026). `grep -i "presentation registr"` over the discussion corpus returns #1613, #1618 and #1550 — and **not** #1095, which is the document that invents it. Any survey of this topic must search both terms plus "issuee registry". A third name exists in speech: at KERIcon 2026 Sam called it a **"user presentation registry"** (`raw/14` §, from an edited auto-caption).

**Status: design only, and less converged than it looks.** #1095 has **zero comments** in ten months. Across all of keripy there are **no issues and no pull requests** proposing to implement it (searched 2026-09-01 for "presentation registry", "presentation registries", "issuee usage registry", "usage registry"). The one PR hit is `#1505` *Worked example of contractually-protected disclosure* (dhh1128, merged 2026-07-17), and its mentions are notes explaining that the example deliberately does **not** use one — "**No presentation registry** for the one-time bespoke presentation — appropriate here. A high-stakes flow would populate `rd` to force verification against an issuee-controlled presentation registry (a follow-up example)." That is our own prior work, so it is not independent corroboration of anything.

**One notable silence.** [#1627](https://github.com/WebOfTrust/keripy/discussions/1627) *ACDC Presentation Architectures* — Sam's newest architecture discussion, updated 2026-09-01 — does not mention presentation or usage registries at all. Whether that means the idea is settled, parked, or superseded is not determinable from the corpus.

---

## 1. #1095 — the origin document and its security argument

The frame is the tripartite Issuer–Holder–Verifier model, with the Issuee as Holder ("This imbues the ACDC with what others call strong Holder binding"). The Verifier must verify two things, and #1095's whole contribution is that **these two are not symmetric**:

> "1) That Issuance came from the Issuer (Issuer impersonation fraud) 2) The Presenter of the ACDC at the time of presentation is indeed the Issuee. (Issuee impersonation fraud)"

**Issuer-side: rampant, so detectability is mandatory.**

> "the worst form of fraud with the most widespread potential of harm would be rampant impersonation fraud that could result when the Issuer's signing keys are compromised. This could annihilate trust in the ecosystem… The ROI to an attacker for compromising the Issuer keys could be huge, especially if that Issuer is a root-of-trust for Identity assurance for an ecosystem."

The mitigation is the existing TEL-anchored-in-KEL structure, and Sam states the resulting property in strong terms: "an impersonator cannot impersonate the Issuer of an ACDC merely by compromising the signing keys of the Issuer. The impersonator MUST anchor the ACDC in a TEL that is anchored in the Issuer's KEL. This anchor enables the Issuer to detect any fraudulent issuances without requiring the cooperation of any other party." Plus a claim worth flagging as a claim: "AFAIK, only KERI/ACDC provides such protection in a decentralized identity system."

The reasoning is explicitly the detect-and-recover posture: "Issuer key compromise has both high susceptibility and non-zero vulnerability, therefore protection comes from recoverability. Detect and recover."

**Issuee-side: localized, so protection is optional and elective.** Three reasons given:

1. **Low ROI.** "Because the fraud is localized to a single Issuee, the ROI to the attacker for compromising the Issuee's keys is low." Plus a note that prophylactic rotation is available and effective, "because the verifier always checks the presentation as being signed by the latest keys of the Issuee."
2. **Use-case-specific mitigations are acceptable here.** A Verifier could require a key rotation as part of the presentation. Sam concedes the cost openly: "This violates the maxim that security not be dependent on a trusted third party, but for localized harm, the party most likely to be harmed is the Verifier… which provides incentives for them to protect themselves." He also names the underlying capability as distinctive: the Issuee's ability "to rotate signing keys without reissuing the ACDC is a unique super-power of KERI/ACDC as a decentralized identity system."
3. **The Issuee can add its own detectability** — which is the usage registry.

### The mechanism as first stated

> "The ACDC must include a requirement that the ACDC is only verifiable when the presentation of the ACDC by the Issuee is anchored as the latest state in an Issuee-controlled *usage registry*. The verifier won't accept the credential if it's also not anchored in the Issuee's (in addition to the Issuer's) registry. The anchor enables the Issuee to detect fraudulent presentations of its credentials. The Issuee can then do a rotation recovery of its keys and also dispute the fraudulent presentations."

Four properties that #1613 does not restate and that the bible has nowhere:

- **One registry, many ACDCs, no leak.** "A *usage registry* can be employed to track the usage of one or more ACDCs by the Issuee… This means that the registry does not leak specific usage of a given ACDC to third parties." The blindable state registry is what makes many-to-one safe.
- **Linkability caveat, with its escape.** "A given usage registry is bound to the AID of the Issuee, so it is linkable. A bulk-issued ACDC with independent AIDs can remove this linkage." So the correlation story is *conditional on* independent-registry bulk issuance, which ties this directly to that workstream.
- **The verifier's time-delay trick.** "by adding a time delay from presentation anchor to acceptance, the verifier can assume that a compromised Issuee would do a recovery, invalidating the fraudulent presentation." This converts detection into prevention at the cost of latency, and it appears nowhere else in the corpus.
- **The Issuee needs its own Registrar.** "the Issuee must have its own Registrar to manage its usage registries." That is real infrastructure, and it is why the last sentence of the section reads: "This is an optional protection measure. Many Issuees will feel that their key management is sufficient… and therefore would not want the extra protection and friction of a usage Registrar."

**Incentive design.** The Verifier is given a reason to enforce: "The verifier has a vested interest in not accepting unanchored presentations as the presentation of an Issuee unanchored ACDC that declares it must be Issuee usage anchored, must be considered fraudulent."

**Provisioning, and the tentativeness of the field choice.** "An Issuee could request at the time of Issuance that their ACDC be backed by an Issuee usage registry. In response, the Issuer issues a variant of the ACDC that designates that it is to be Issuee presentation protected. **That designation needs to be defined. This could be an `rd` field in the attribute section.**" As of #1095 the field is a suggestion, not a design.

**Diagrams (not vendored here):** `PresentationUsageRegistrarObserver` and `PresentationUsageRegistryTEL`, attached to the discussion body.

---

## 2. #1613 — the developed design

### 2.1 The trigger is a three-part test

> "The issuer of a given ACDC can signal to a verifier that the `grant` message in an IPEX MUST be anchored in a presentation registry controlled by the Issuee of that ACDC at the time of presentation… That signal is provided when both a non-empty `rd` field and a valid AID as the Issuee in the issuee `i` field are provided at the top level of the ACDCs attribute `a` section (not the top level of the ACDC itself) **and the `rd` field at the top level of the ACDC is not empty**."

All three conditions. If there is no Issuee `i` in `a`, an `rd` in `a` imposes no anchoring requirement. If the ACDC's *top-level* `rd` is empty or missing, then the `rd` in `a` "refers to an ACDC state registry, not an IPEX presentation registry." The top-level `rd` is doing disambiguation work, which is easy to miss.

### 2.2 What the registry must contain

> "the value of the registry `rd` field in the attribute `a` section MUST be the SAID of the `rip` event of the associated presentation Registry. The Issuee of the associated ACDC, who is also a Grantor of that IPEX, MUST control this registry. The value of the ACDC SAID field in the blinded attribute block of the latest non-vacuous event in that presentation Registry must be the SAID of the `grant` message."

Note the field reuse: the slot that normally holds an ACDC SAID holds a `grant` SAID instead.

**KRAM couples to this.** "in order to pass KRAM, a `grant` message anchor must happen in a timely fashion relative to the IPEX exchange. The `grant` message… must be created, then anchored, and then pass the receiver's KRAM." So a presentation registry inserts a registry write into the critical path of a freshness window — see `bible/09-kram-and-request-authentication.md`.

### 2.3 Two benefits, only one of which is fraud protection

**Fraud protection, and its precondition.** "an imposter that merely compromises the Grantor's signing infrastructure can't avoid the requirement without also compromising the Issuer." The Issuer must be a *different party*, and Sam states the self-issued hole explicitly: "For ACDCs that the Grantor self-issues, this is only a vulnerability if the Issuance authentication factor is merely an unanchored signature. An imposter who controls the Grantor's signing infrastructure can create ACDCs whose authentication factor is an unanchored signature."

Multi-ACDC DAGs multiply the work: "When multiple ACDCs in the granted DAG each have a different presentation registry ID field value… the verifier must verify all of the anchors." And a precise limit on what one anchor buys: because the `grant`'s `o` field names the DAG's origin, "anchoring the exchange in one presentation registry provides a perpetually verifiable proof of the presentation of all ACDCs in that DAG, **but not necessarily a fresh proof of control for all Issuee AIDs in that DAG**. Multiple anchors in different registries provide multiple vectors of detectability and multiple fresh proofs-of-control; the perpetual verifiability is redundant."

**Correlation resistance, which works even when fraud protection cannot.** If a Grantor directly anchors a `grant` SAID in its public KEL and the Grantee does the same, "a third party… would be able to detect the same grant SAID in both the Grantor's KEL and the Grantee's KEL, thereby correlating the IPEX." Anchoring in a blinded presentation registry instead means "neither the grant SAID nor any other artifacts of the granted DAG appear in the KEL of the Grantor," so "a Grantee could anchor every message in the IPEX without providing a point of correlation between the KELs of the Grantor and Grantee."

**The self-issued bespoke pattern.** A Grantor can get correlation resistance with no cooperating Issuer by self-issuing a bespoke origin ACDC carrying `i` and `rd` in its `a` section — "This means the Grantor is both Issuer and Issuee of that bespoke ACDC." With a hard constraint attached: "the bespoke ACDC itself must use a blinded state Registry for its Issuer authentication so that the SAID of its ACDC is not correlatable. If it uses a direct KEL anchor, then that anchor itself would be correlatable. If it used a bare attached signature… then the ACDC itself would not be perpetually verifiable despite using a perpetually verifiable presentation registry."

### 2.4 The `rd`-in-`a` ambiguity, and Sam's own doubt

The v1 spec also allows `rd` in `a` as a *hidden ACDC state registry*. #1613 proposes EGF-declared disambiguation with "The default, if not otherwise specified, should be for anchoring presentation exchanges," floats "We may want to limit the use case to only presentation registries in the v1.1 spec," and then argues the hiding case down: its only benefit arises "when the ACDC in compact form is made public, independent of any given presentation, and the fact of it having a registry must remain undisclosed. It is not clear that this is a worthy use case… Given the potentially dubious value, we might want to forbid using the `rd` field in the attribute section for an ACDC state registry." The section ends genuinely unresolved: "Not sure if either is a worthy use case."

### 2.5 Interaction with `ax`

The presentation-registry requirement is **independent of and stronger than** `ax`: "Notwithstanding the presence or absence of the `ax` field, when an ACDC in a granted DAG meets the requirements for a Issuer signaled presentation anchor registry… then that `grant` message MUST be anchored in that registry for the `grant` to be valid. Otherwise, the presumption is that the grant is fraudulent." With a liability claim attached: "Any verifier (Disclosee) accepting such a `grant` is presumptively in violation of any contractual or regulatory protection afforded to the real Grantor by colluding with a fraudulent grantor."

And a scoping judgment about which registry may be used: "There is no security advantage to using a presentation registry specified by the Grantor, as the main purpose of a presentation registry is to allow the Grantor to detect a compromise of its signing key infrastructure… Thus, the main use case for impersonation fraud detection of the Grantor requires a pre-specified presentation registry **by an Issuer different from the Grantor**, which must be prespecified in one of the ACDCs not in the `grant` message." On tooling: "we should not add special tooling for this special case; instead, we should use the existing tooling for a bulk-issued ACDC to handle it."

---

## 3. #1618 — presentation registries as one authentication factor of three

ryan-hansen restates the design space symmetrically for issuance and presentation:

> "The same three factors apply to the presentation (the grant / exn), not only to issuance: 1. Grant is signed (normal) 2. Grant is anchored in a presentation registry (issuee-controlled; rd on the origin ACDC can force the check) 3. Grant is anchored in a KEL without a presentation registry (a case V1 did not really specify)"

Two useful observations from the same post: seals are "deliberately opaque, so it is not always obvious whether a seal is for the ACDC, the grant, or something else"; and "An exchange anchored in a presentation registry would also need an rd on the exchange" — a field-placement consequence nobody else raises.

---

## 4. #1550 — the same registry, used for something else

In *Guardianship for SEDI*, an "Edge Verifiable Agent Control" diagram legend reads:

```
d = SAID
i = Issuee
rd = issuee usage registry SAID
rc = resource capabilities map
```

So the Issuee usage registry appears as the state mechanism for **agent capability control**, not presentation. Worth carrying: the primitive is "an Issuee-controlled blindable state registry," and presentation anchoring is one application of it. That widens the concept and is an argument against naming the general thing "presentation registry."

---

## 5. KERIcon 2026 — the spoken framing

From `raw/14-kericonf-2026.md` (edited auto-caption; see that file's §0 before quoting to anyone):

> "We also have something called a user presentation registry, which is also a new thing that nobody else does as far as I've never seen anybody do it, which allows presenters to detect compromise of their proofs that are in their credentials that they're presenting. So they themselves will protect it from fraud, not just the issuer."

The novelty claim is stated more strongly here than anywhere in the written corpus. "Not just the issuer" is the crisp one-line statement of the whole idea.

---

## 6. What is normative in the ACDC specification

`spec/spec-body.md` @`f0bd097` (2026-08-28). **"Presentation registry" and "usage registry" do not appear.** What does:

- **The nested-`rd` slot exists and its purpose list already includes usage.** Top-level `rd` is glossed "Issuance and/or revocation, transfer, or retraction registry for ACDC" (`:23`); the *not-at-top-level* entry reads "Issuance and/or revocation, transfer, retraction, **or usage** registry for ACDC when not at top-level" (`:48`). That single word is the only trace of this design in any specification.
- **Nested `rd` is explicitly open-ended.** "When the registry SAID, `rd` field is used at the top level for the Issuer's registry, a registry SAID, `rd` field that appears nested in the Attributed, `a`, or Aggregate, `A`, section MAY be used for some other registry, such as an application-specific or Issuer-specific registry" (`:85`). Note "Issuer-specific" — the spec does not contemplate an *Issuee*-controlled registry.
- **The motivating rationale in the spec is bulk issuance and graduated disclosure**, not fraud detection: nesting "may better facilitate contractually protected disclosure of the bulk-issued registry" (`:326`).
- **`rd` binds to a `rip` event.** "The Registry SAID, `rd` field value MUST be the value of the SAID, `d` field of the Registry Inception, `rip` event. Because the Issuer `i` field appears in the `rip` event, the Registry SAID, `rd` field value cryptographically binds the Registry to the Issuer AID" (`:2019`). **This is a live tension**: the `rip` binds the registry to *its own* incepting AID. For a presentation registry that AID is the Issuee, so the sentence's use of "Issuer" is about the registry's issuer, not the ACDC's — worth stating carefully in any spec text.
- **Blindable state registries are normative** and there is a worked "Registry-Dependent Issuance Lifecycle" walking `rip` → issuance → state → verification → revocation. The spec calls a `rip` "a vacuous placeholder that reveals nothing about what will later be issued" — the origin of #1613's "latest non-vacuous event" phrasing.

---

## 7. keripy implementation status @`4df8e4a8` (2026-09-01)

**The substrate is built; the feature is not.**

Present:
- `src/keri/acdc/regeventing.py` (1,204 lines) — v2 registry event layer: `_validateRip`, `_validateUpdate` for blindable registry updates, `vet()` producing verified registry state.
- `src/keri/acdc/registraring.py` (400 lines) — `Regery` ("Local manager for V2 ACDC blindable state registries"), `Registry`, `Registrar` ("facade for V2 registry inception and blindable state updates").
- `src/keri/acdc/messaging.py` — ACDC builders that accept `regid` (top-level `rd`) and `iseaid` (Issuee `i` into the attribute section).

Absent:
- **No code recognizes the three-part presentation-registry signal** (`rd`+`i` in `a` plus non-empty top-level `rd`). `acdcatt`'s `regid` parameter is the *top-level* `rd`; a caller wanting `rd` in `a` must hand-build the attribute dict.
- **No grant-anchor enforcement.** `src/keri/acdc/ipexing.py` (722 lines: `IpexHandler` plus `apply`/`offer`/`agree`/`grant`/`admit` builders) contains no reference to a registry or an anchor check.
- **Nothing distinguishes an Issuee-controlled registry from an Issuer-controlled one.** A `Registrar` is a `Registrar`; who incepted it is the only difference, and nothing consumes that difference.

So an Issuee could stand up a usage registry today with existing tooling, and no verifier would look at it.

---

## 8. Open questions and unresolved tensions

1. **Name.** "Issuee usage registry" (#1095, #1550) vs "presentation registry" (#1613, #1618) vs "user presentation registry" (KERIcon). #1550 shows the primitive is used beyond presentation, which argues the general name should be the usage one.
2. **`rd`-in-`a` disambiguation.** EGF-declared, restricted to presentation registries in v1.1, or left ambiguous? #1613 argues both directions and settles neither. This blocks any normative text.
3. **Is the ten-month silence meaningful?** #1095 has no comments; #1627 does not mention the idea. Parked, settled, or superseded is not determinable from the corpus, and it is the first thing to ask a maintainer.
4. **The `rip`-binds-to-Issuer wording** (spec `:2019`) needs care before a presentation registry can be specified, since the incepting AID is the Issuee.
5. **Latency.** A presentation registry inserts a registry write between message creation and KRAM acceptance, and the verifier's time-delay trick from #1095 adds more deliberately. What window class does that imply? Nothing connects the two designs numerically.
6. **The trusted-third-party concession.** #1095 admits Verifier-specific protection "violates the maxim that security not be dependent on a trusted third party" and justifies it by localized harm and aligned incentives. That is a real doctrinal exception and should be recorded as one rather than smoothed over.
7. **Correlation resistance is conditional.** It requires blinded registry state *and*, for unlinkability of the registry itself, bulk issuance with independent AIDs. A plain usage registry is "bound to the AID of the Issuee, so it is linkable."
