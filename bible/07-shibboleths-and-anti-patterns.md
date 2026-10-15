# 07 — Shibboleths and Anti-Patterns {#shibboleths}

## Thesis {#thesis}

Every technical community has shibboleths — framings that instantly mark a speaker as an insider or an outsider — and KERI's are unusually load-bearing, because the whole architecture is a deliberate, point-by-point correction of the priors that PKI, IAM, blockchain, and mainstream verifiable-credentials work install in the people who grew up on them. A reviewer who reasons from those priors will produce critiques that KERI's core contributors recognize instantly as category errors: criticizing a duplicity-evident system for not being duplicity-resistant, asking who the trusted authority is, wanting global consensus or finality, treating a witness as a CA, treating revocation as a blocklist, treating a credential as a signed envelope, or treating "decentralized" as a synonym for "on a ledger." This section is a catalog of those outsider-tells. For each, it states the generic framing the outsider brings, explains precisely why that framing is a category error in KERI's own terms, gives the KERI-correct reframing, and cites the source. It closes with the single most important habit an adversarial reviewer of this codebase can cultivate — the reflex to check what the code actually enforces before believing what the prose claims — because KERI's implementations contain real, documented gaps between the doctrine and the machine. The goal is inoculation: after this section, a reviewer should be able to hear their own PKI/blockchain/OAuth reflexes firing and catch them before they reach the page.

## Status {#status}

This chapter is about framings rather than about pins, so it carries tier markers only in the handful of places where a tier is load-bearing — where the correction to a shibboleth lives on one branch of a specification and not the other, or where the evidence is code rather than text. Two applications of the rule against upgrading a marker bite in this chapter: text that exists only on a `v1.1` branch is not [N] however obviously it reads as a correction, and an unmerged branch on a personal fork is not [K].

---

## 1. How a shibboleth works here, and why it matters {#how-shibboleths-work}

A shibboleth is not merely jargon. It is a framing whose shape encodes an assumption. When an outsider says "how does KERI revoke a certificate," the words "certificate" and "revoke" smuggle in the entire X.509 model — an issued artifact with a validity window, a separate revocation list, a phone-home check — none of which exists in KERI. The question cannot be answered on its own terms; it must first be reframed, and the need to reframe it is the tell.

This matters for a review panel for two reasons. First, a critique built on a smuggled assumption is not just wrong, it is unfalsifiable from inside the outsider's model — the reviewer will keep finding "missing" features that were deliberately never there. The security-analysis corpus makes this the first rule of its analysis method: an analyst "MUST restate the claim verbatim... If you cannot do so, stop and ask," and must "name the objective function first," precisely because "outsider critiques smuggle in unstated invulnerability goals" (standard-analysis.md > 0). Second, KERI's own advocates are candid that some outsider critiques survive reframing — the observer/watcher infrastructure really is immature, the formal literature really is thin — so a reviewer who cannot separate the category errors from the genuine residuals will either dismiss KERI wholesale or swallow it wholesale, and both are failures of the same discipline (dg-c02-claude.md, sections 5-6; wtbo.md, sections 5-6).

The catalog below is organized by the outsider's home domain, because that is how the reflex fires. Each entry follows the same shape: the framing, why it is a category error, the reframing, all cited.

---

## 2. PKI / X.509 / CA tells {#pki-tells}

### 2.1 "Who is the trusted authority / who vouches for the identifier?" {#trusted-authority}

#### The framing {#trusted-authority-framing}

In PKI the root of trust is an administrator: a CA signs a certificate that asserts a binding between an identifier and a key, and relying parties trust the CA's operational process. The outsider reflexively asks who plays that role in KERI.

#### Why it is a category error {#trusted-authority-error}

KERI's foundational move is to eliminate the role, not to fill it. "The fundamental flaw... is the separation of the identifier from the cryptographic keys that control it"; in X.509 the binding is "merely an assertion — a digital certificate — signed by a third party," creating "a root of trust that is external to the identity itself" (keri-primer.md > 1). The KERI spec states the same flaw as a verifiability failure: the CA's certificate "is not made with the controlling keypairs of the identifier but made with keypairs controlled by the CA," giving "evidence of authenticity of the assignment... but not evidence of the veracity of the mapping" (KERI spec > Overcoming existing security overlay flaws, L81).

#### The reframing {#trusted-authority-reframing}

"The identifier is the root of trust" (keri-primer.md > 1.3). An AID is self-certifying — cryptographically derived from its own controlling keys — so its authenticity "can be verified without any external authority" by replaying its KEL (cr-ad-trust.md > 4). There is no authority to vouch for it because the mathematics vouches for it. Asking "who is the CA" is like asking who notarizes a hash: the question presumes an administrative layer the design deletes.

### 2.2 "The strength of the system is the rigor of the CA's vetting." {#ca-vetting}

#### The framing {#ca-vetting-framing}

PKI experts locate assurance in how carefully the issuer vets applicants. The reflex is to evaluate KERI by asking how rigorously its issuers vet.

#### Why it is a category error {#ca-vetting-error}

It targets the wrong locus of risk. "*Certificate authorities aren't the ones that choose or manage the keys in certs.* Holders of certs do that. It's the key management of *holders* that's the ubiquitous locus of the risk" (x509-prob.md > Governance). The CA vets an applicant once; thereafter the security of every certificate depends on the holder's opaque, unauditable key custody — the "missile silo" guarded by "one opaquely managed secret" (x509-prob.md > Governance). All the CA machinery "guarantees... is that someone provided a public key before the certificate was created" (x509-prob.md > Governance).

#### The reframing {#ca-vetting-reframing}

KERI moves assurance into observable key management: pre-rotation, weighted multisig, witnessing, and anchoring are all declared in the public KEL and are continuously verifiable. "KERI's real innovation in multisig is less about inventing and more about exposing: multisig is optional and infinitely variable, but defining and following policy about it is required" (keri-primer.md > 2.4). The right question is not "how good is the vetting" but "what does the key-state history actually show, and can I replay it myself."

### 2.3 "Renew the credential / rotate to a new certificate." {#renewal}

#### The framing {#renewal-framing}

Certificates expire and are renewed; a compromised key is handled by issuing a fresh, unrelated certificate.

#### Why it is a category error {#renewal-error}

It conflates identity with privilege. "Identity means *sameness*: the thing that holds constant across contexts" (wtbo.md > 1); "An organization incorporated in 1975 doesn't renew its identity every ninety days" (cr-ad-trust.md > 1). X.509's mandatory Validity field means "Evidence of identity expires by design, not by necessity" (cr-ad-trust.md > 1). Renewal, moreover, "proves less than it appears": it "demonstrates that a CA is willing to re-assert a binding, not that the underlying key was rotated, that the old key was retired, or that any meaningful change in key management occurred" (wtbo.md > 1). Re-issuing after compromise "is essentially the same as starting over by creating a brand-new independent mapping" (KERI spec, L83), with "no cryptographically Verifiable way to link the new... key(s) to the prior" (KERI spec, L83).

#### The reframing {#renewal-reframing}

A transferable AID persists across every key change: "The identifier string remains constant even as the keys change... Identity survives key rotation" (keri-primer.md > 2.1). Rotation is a linked event in the KEL, cryptographically chained to the prior state, not a fresh unrelated artifact. "Renewing an *identity* is a non-sequitur" (x509-prob.md > Lifespans). The dynamic thing that should expire — a privilege, a role grant — is carried by a separate ACDC, not by the identity itself.

### 2.4 "Pin the key / pin the certificate for continuity." {#pinning}

#### The framing {#pinning-framing}

To get continuity across a connection, pin the key you saw last time.

#### Why it is a category error / the tell {#pinning-error}

In 2026 Google Cloud advised customers not to pin certificates because pinning "will cause your application to break during routine certificate rotations" (x509-prob.md > Prerotation). That advice is itself the tell: "there is no cryptographic thread joining the old key to the new one, so a relying party that pinned the old key pinned nothing durable — the only continuity on offer is the CA's say-so" (x509-prob.md > Prerotation; wtbo.md > 1). The industry's own guidance concedes that X.509 continuity is administrative, not cryptographic.

#### The reframing {#pinning-reframing}

"Prerotation is exactly what would let a relying party commit to a durable cryptographic anchor *and* survive the rotation" (x509-prob.md > Prerotation). A relying party pins the AID — which is stable across all rotations — and follows the KEL forward; the durable anchor and rotation survival are the same fact. Notably, the fix here is to "trust *more* administrative anchors, not fewer" in PKI, versus KERI's single cryptographic anchor (wtbo.md > 1).

### 2.5 "Trust ultimately bottoms out somewhere administrative anyway." {#administrative-bottom}

#### The framing {#administrative-bottom-framing}

All trust chains end at some human authority; KERI just moves the humans around.

#### Why it is a category error {#administrative-bottom-error}

The claim is about where the chain bottoms out, and the answer is genuinely different in kind. "CT's chain of assurance bottoms out in administrators... KERI's bottoms out in mathematics: the self-certifying identifier derives from the initial public key, and the KEL's validity can be checked by anyone who replays its hash chain, without querying any authority" (wtbo.md > 3). This is not rhetorical: the KEL replay requires no trusted third party at any step.

#### The reframing {#administrative-bottom-reframing}

Trust bottoms out in the controller's custody of its own keys plus the soundness of the hash and signature primitives — assumptions A1 (cryptographic soundness) and the controller's key secrecy — and nothing else (background.md > 4.6). Governance and reputation still matter for veracity (see [section 9](#semantic-tells)), but the authenticity chain is closed cryptographically. A reviewer should insist on this distinction: KERI does not claim to abolish human judgment, only to remove it from the authentication path.

### 2.6 "Publishing the same AID at several well-knowns strengthens the AID binding." {#multiple-well-knowns}

#### The framing {#multiple-well-knowns-framing}

Corroboration across independent sources makes a binding stronger. This is the reflex behind multi-perspective domain validation, DNS CAA checks, and the ordinary advice to look a fingerprint up in a second place — and it fires hard on KERI's OOBA pattern, where a controller publishes the same AID at two or more `/.well-known/oobi/{aid}` URLs on independently controlled namespaces. The outsider reads agreement across the namespaces as evidence about the identifier.

#### Why it is a category error {#multiple-well-knowns-error}

The binding was never in the well-knowns to be strengthened. [N] The KERI specification states the limit itself, and states it as a limit: "This pattern does not change the trust model of an OOBI", because "the AID binding produced by resolution is still cryptographically verified through KERI in the usual way", and "The multi-factor arrangement governs only whether the recipient is willing to bootstrap from the OOBIs at all" (KERI spec > OOBI with MFA, L2838 @`fbdd4a615`; present verbatim on `v1.1` too). This is the [section 2.5](#administrative-bottom) error in a new costume: administrative corroboration reasserting itself where a cryptographic anchor already closes the chain. An OOBI's worst case was never a false binding — "an OOBI may be part of a DDOS attack but not as part of a service endpoint cache poison attack" (KERI spec > OOBI Forwarding, L2831) — so agreement across namespaces cannot improve a property that resolution verifies unconditionally.

#### The reframing {#multiple-well-knowns-reframing}

OOBA is a willingness-to-bootstrap control, and the thing it multiplies is the attacker's cost of denying or flooding discovery, not the confidence in what discovery returns. The independence requirement makes this legible: it is required of the delivery channel and not merely of the namespace — "Each well-known OOBI URL is delivered to the recipient through a channel whose compromise is independent of the others" (L2838) — so two URLs in one email are one factor, which is a statement about channels, not about identifiers. The tell to catch is any sentence in which the count of well-knowns appears as an input to an authenticity judgment. Note also that the recipient's threshold has no encoding anywhere and no owner in the protocol, deliberately: the controller declares its witness threshold in its KEL because that threshold is about accountability, and declares nothing about `wurls` because this one is about the recipient's own willingness.

---

## 3. Revocation, CRL, OCSP, and phone-home tells {#revocation-tells}

### 3.1 "How does KERI revoke — where is the CRL / OCSP responder?" {#crl-ocsp}

#### The framing {#crl-ocsp-framing}

Revocation is a separate subsystem: a list you download (CRL) or an endpoint you query at verification time (OCSP).

#### Why it is a category error {#crl-ocsp-error}

There is no separate revocation layer to point at. Key state "lives in the KEL" and is "continuously current"; a revoked or abandoned identifier is signaled inside the log itself by rotating to a null next-key list (cr-ad-trust.md, sections 2 and 4; KERI spec, L340). Worse, the outsider's model is actively criticized: OCSP "requires the client to query a central responder for every validation, creating a privacy leak (the CA knows every site you visit)," and when the responder is offline browsers "fail open," so "The system is most vulnerable precisely when it is most needed" (keri-primer.md > 1.1; wtbo.md > 2). CRLs are "heavy, bandwidth-intensive... scale poorly" (keri-primer.md > 1.1).

#### The reframing {#crl-ocsp-reframing}

For key state, revocation is just the current head of the replayed KEL. For credential status, KERI uses a TEL (Transaction Event Log) whose state is anchored in the issuer's KEL, checked "without privacy leaks or 'fail open' risks" (cr-ad-trust.md > 3). The ground truth is even sharper than the prose: the reference verifier, on encountering a revoked credential, does not raise — it logs and continues so it can "save a revoked credential"; revocation is a TEL state transition (`Ilks.rev`/`brv`), queried from the TEL, not a delete or a blocklist (keripy vdr/verifying.py, L129-132; raw/09 section 4).

### 3.2 "A registry / status endpoint is consulted at verification time." {#status-endpoint}

#### The framing {#status-endpoint-framing}

Verification legitimately reaches out to an authority to confirm current status.

#### Why it is a category error {#status-endpoint-error}

Any verification-time callback reintroduces exactly the runtime trust dependency that end-verifiability exists to eliminate. "A registry consulted at verification time is a phone-home in disguise" (sda.md > 7). The ACDC spec builds the rejection into its architecture: the Observer/Registrar split lets a Validator check an ACDC's status "without exposing a point of validation (PoV)" and syncs on state changes rather than at presentation — "no forced phone home validation" (ACDC spec > TEL Registrars and Observers, L1693). This is a direct, named rejection of the OCSP/CRL model.

#### The reframing {#status-endpoint-reframing}

"Verification must succeed from the credential and key-state alone, and any registry or log is an issuance-time and audit-time convenience, never a verification-time dependency" (sda.md > 7). Applied design corroborates: a download URL in a credential is "phone-home by another name... and creates an availability chokepoint," which is why SEDI commits an image by digest and has the holder carry the bytes rather than linking to a resolvable location (sedi-id/index.md > Image). The tell to watch for in a deployment review is any credential field that resolves to a live endpoint at verification time.

### 3.3 "Certificate Transparency already solved this." {#certificate-transparency}

#### The framing {#certificate-transparency-framing}

Append-only public logs plus monitors give detection; KERI is reinventing CT.

#### Why it is a partial truth that becomes a category error {#certificate-transparency-error}

The corpus is explicit that CT and KERI share DNA — both are "fundamentally detection-oriented. Neither prevents a bad actor" (wtbo.md > 3), both use append-only hash-chained structures and signed receipts. But CT "is a detection mechanism, not a prevention mechanism; fraudulent certificates may be usable for a time" and, decisively, it "redistributes administrative trust rather than eliminating it" (keri-primer.md > 1.1; wtbo.md, abstract). The ultimate arbiter of CT remains "a handful of browser vendors" with "immediate, global effect... no formal appeals process" (wtbo.md > 1, Note [b]). "The result is not a decentralized trust hierarchy. It is a more elaborate one" (cr-ad-trust.md > 2).

#### The reframing {#certificate-transparency-reframing}

KERI keeps CT's detection orientation but changes what detection bottoms out in. "Unlike certificate transparency, KERI enables the detection of Duplicity in the Key state via nonrepudiable cryptographic proofs of Duplicity, not merely the detection of inconsistency... that MAY or MAY NOT be duplicitous" (KERI spec, L85). The witness/watcher split is the CT analogue (witnesses ≈ CT logs, watchers ≈ monitors), but a KERI watcher makes "an observation — surfacing cryptographic evidence," whereas a browser root program makes "an enforcement decision... with immediate global consequences" (wtbo.md > 4). Detection without re-centralized enforcement is the distinction; a reviewer who says "just use CT" has missed the re-centralization critique.

---

### 3.4 "Revoke just the compromised copy of a bulk-issued credential." {#bulk-copy-revocation}

#### The framing {#bulk-copy-revocation-framing}

A bulk-issued set gives each verifier its own copy, so a copy compromised at one verifier can be revoked while the copies presented elsewhere keep verifying, and that granularity is a feature.

#### Why it is a category error {#bulk-copy-revocation-error}

It conflates three different repairs. The specification's editor answered exactly this framing [P]: "An issuer when it revokes authority revokes it universally. In a bulk issued set this means that all members of the set MUST be revoked." What a holder can lose at one verifier is a key, not a credential, and "if the keys get compromised then the keystate is changed not the ACDC state" (keripy GitHub > #1574, comment of 2026-08-07, R-042, https://github.com/WebOfTrust/keripy/discussions/1574#discussioncomment-17938568). The framing also confuses the two kinds of registry: an issuer registry tracks the credential's state, while "A presentation registry on the other hand is not tracking ACDC state, but is merely logging presentations". Per-copy revocation is the X.509 instinct, revoke the artifact that leaked, carried into a system where the artifact is not what leaked.

#### The reframing {#bulk-copy-revocation-reframing}

Three events, three remedies. Withdrawn authority: the issuer revokes every member of the set, and the registries' state moves in lock step even though vacuous updates keep their event histories uncorrelated. A compromised issuee key: that one AID rotates, and the other AIDs in the set are uninvolved. A compromised private salt from which the whole set's keys were derived: per the same comment, "the whole set has to be abandoned". The property that makes the middle case work, repairing either party's key state without touching the authority the credential grants, is the one [section 6.1](#signed-envelope) credits to anchoring over bare signatures. This is the editor's account in a discussion thread, not specification text; the bulk-issuance section of the ACDC specification was not checked for it here.

## 4. Blockchain / consensus / global-ordering tells {#blockchain-tells}

### 4.1 "You need a ledger / global consensus / total ordering." {#global-consensus}

#### The framing {#global-consensus-framing}

Decentralized identity needs a blockchain so that everyone agrees on one history.

#### Why it is a category error {#global-consensus-error}

Global total ordering across identifiers is an explicit non-goal (background.md > 1.3). The reasoning is precise: key events are "idempotent authorization operations as opposed to non-idempotent account balance decrement or increment operations. Total or global ordering may be critical for non-idempotency, whereas local ordering may be sufficient for idempotency" (KERI spec > KAWA insight, L1836). Because "the controller is the sole source of truth for the creation of any and all key events, it alone, is sufficient to order its own key events" (KERI spec, L1836). "KERI rejects the need for global consensus regarding identity. Instead, it uses microledgers called key event logs (KELs)" (keri-primer.md > 2). Del Giudice-background readers who "interpret 'not duplicity-resistant' as a criticism" are "Misunderstanding KERI as 'weaker than a blockchain' when it solves a different problem" (dg-c03-claude.md > 6).

#### The reframing {#global-consensus-reframing}

Each AID has its own microledger; "Event 5 for Identifier A must come after Event 4 for Identifier A, but it has no required ordering relative to Event 5 for Identifier B" (keri-primer.md > 2). This yields horizontal scaling, cross-jurisdiction ease, and decayed hacking incentives (a breach is scoped to one identifier). Where a ledger is ever used it is only a last-resort tiebreaker in the total-compromise case, requiring "minimal use of a distributed consensus ledger" (KERI spec, L1888). The reference implementation embodies this: recovery forks the KEL and keeps the disputed branch visible (keripy eventing.py, L3143-3149; raw/09 section 4) — the opposite of a single globally-agreed chain.

### 4.2 "Anchoring signatures in time sounds like a blockchain." {#anchoring-not-blockchain}

#### The framing {#anchoring-not-blockchain-framing}

To prove when a signature was made you need a total order, hence a chain.

#### Why it is a category error {#anchoring-not-blockchain-error}

The anchoring requirement is strictly weaker than a ledger. "We don't need to know the relative order of two signing events — only how any one event relates to its key state. That means no total ordering, and no cumbersome consensus algorithm... no permissioning problem, no big central *anything* in the sky, no scale or performance bottlenecks, and no regulatory problems with data locality, privacy, or erasure" (was.md > Solution). KERI implements it with "tiny, identifier-specific files called KELs... and TELs" that anchor the hashes of signed events (was.md > Solution).

#### The reframing {#anchoring-not-blockchain-reframing}

Anchoring establishes the position of a signature relative to its own identifier's key-state history, which is all that is needed to defeat the retrograde attack (see [section 11](#retrograde-attack)). "Sounds like blockchain" is a lazy tell precisely because it assumes the strong property (global order) when only the weak one (per-identifier order) is required.

### 4.3 "Immutability requires a chain." {#immutability}

#### The framing {#immutability-framing}

Tamper-evidence and immutability are blockchain properties.

#### Why it is a category error {#immutability-error}

A SAID gives tamper-evident content-addressing and immutability with no ledger and no consensus: "a SAID will verify if and only if its encompassing serialization has not been mutated, which makes the content immutable" (CESR spec > SAID, L1196). CESR is "a streaming format, not a chain" (raw/02 section 15).

#### The reframing {#immutability-reframing}

Immutability is a property of a cryptographic commitment, not of a distributed agreement protocol. "A Merkle inclusion proof establishes placement in a history. A SAID establishes identity of content" (acdc-and-mtc.md > 3.2) — different proof obligations, only one of which needs a chain.

### 4.4 "But then how do you honor the right to be forgotten?" {#right-to-be-forgotten}

#### The framing {#right-to-be-forgotten-framing}

A shared immutable ledger and GDPR erasure are fundamentally incompatible, so KERI must have the same problem.

#### Why it is a category error {#right-to-be-forgotten-error}

KERI's "non-intertwined trust bases" mean "a given identifier's data may be erased and truly forgotten" (keri.one homepage). Because KELs are per-identifier microledgers, "'forgetting' an identifier requires a hard fork of the entire chain" only on a blockchain; in KERI a user can delete "their specific Key Event Log... without disrupting the global ecosystem" (keri-primer.md > 3.5). And ACDC payloads are held off-chain: the KEL stores only anchors (hashes), so deleting the payload "leaves an irreversible hash; identity history intact, personal data removed" (keri-primer.md > 3.5).

#### The reframing {#right-to-be-forgotten-reframing}

RUN replaces CRUD: "there is no Delete. Instead of Delete, Peers Nullify" — but naive total erasure "exposes the data controller to a replay attack of erased data," so a nullified record is kept as an invalidity marker while its confidential payload is discarded (KERI spec > RUN off the CRUD, L2870, L2927). Erasure is a first-class outcome by construction, not a fatal contradiction.

---

## 5. OAuth / OIDC / SAML / IAM / perimeter / federation tells {#iam-tells}

### 5.1 "Authentication precedes authorization as one indivisible login." {#authn-before-authz}

#### The framing {#authn-before-authz-framing}

A user logs in once (auth), gets a session/token, and is thereafter authorized (authz) by presenting that token — the sentry-at-the-gate model.

#### Why it is a category error {#authn-before-authz-error}

This is "a natural consequence of a perimeter-oriented mindset... all the way back to... a sentry challenged someone approaching the gate" (ASAAU > Appendix). The perimeter re-challenge is satisfied merely by producing "a token that the sentry gave them," and internal challengers "don't do any deep checking of their own... because the token is too lossy to support deep checking anyway. The token is thus faster but less safe and far more opaque than verification at the perimeter" (OS > 1). The named technologies — "IAM, SAML, OAuth, OIDC, LDAP, AD, API keys — are mostly embodiments of perimeter security" (OS > 1).

#### The reframing {#authn-before-authz-reframing}

Zero-trust: "assume everything — outside OR inside the perimeter — is unsafe until proven otherwise" (OS > 1). Every request is independently signed and verified at every hop; there is no "trust after entry" (GOC > 2). Authentication and authorization are partially dissociated into Attribute-Based Authorization: "someone can receive permission if they can prove certain characteristics, even if a sentry does not (yet, or maybe ever) know who they are" (ASAAU > Appendix). The voting-booth example (prove citizenship, not identity) and the pharmacy example (any licensed doctor may browse; authenticate only when accountability attaches) show authz preceding auth.

### 5.2 "Use a bearer token / session / API key to call the service." {#bearer-tokens}

#### The framing {#bearer-tokens-framing}

Hold a bearer credential; possession is authorization.

#### Why it is a category error {#bearer-tokens-error}

A bearer token is "a signet ring handed out for an errand": "Possession of an API key... makes the holder indistinguishable from the account it belongs to, free to do anything that account can" (sda.md > 1). It is opaque, replayable, long-lived, and exfiltratable from the server. The applied doctrine is categorical: "We do not use sessions, cookies, tokens, JWTs, OAuth, OIDC, SAML, or any similar technologies to secure calls" (ASAAU, item 0; GOC > 2).

#### The reframing {#bearer-tokens-reframing}

Identity is an AID; proof is a fresh signature per request over the method, path, resource header, and a timestamp (RFC 9421 message signatures) (GOC > 2; raw/10 section 7a). "A stolen header set can't be replayed against a different method/path, and there is no long-lived secret to exfiltrate from the server" (raw/10 section 4). The signet-ring/errand distinction is the doctrine: "The key authorizes an act; the ring authorizes a person to stand in your place" — never hand over the ring for an errand (sda.md > 1).

#### The boundary {#bearer-tokens-boundary}

The boundary runs in both directions and must be stated whenever this row is used. The signature is better than a bearer token in two respects a token cannot match: the stolen header set is scoped to one method and path pair, and to one key state. It is not better in the respect an outsider will assume, because neither side of the channel enforces freshness, and on that one pair the captured request therefore replays indefinitely. [K] In KERIA at `7e685edaa`, `Signify-Timestamp` is folded into the signed byte string alongside every other covered field and is never parsed into a datetime — `fromIso8601` does not appear in `authing.py` at all, and the file's only two time calls are outbound stamps. The RFC-9421 `expires` and `nonce` params are appended to the signature-params string, so they are cryptographically bound, but `expires` is never compared to a clock and there is no replay cache: nothing in `src/keria` stores a seen nonce (raw/10 section 2). [K] signify-ts at `ffba8406e` is the same on the client half — `authing.ts` folds `input.expires` into the params string and never compares it, and its ESSR path checks only that a timestamp is present, which is a presence check and not a freshness check (raw/10 section 2). What the signature buys is therefore request integrity and origin authentication, not replay protection, and what retires a stolen header set is key rotation, not expiry. The fields needed to enforce freshness are present and signed, so enforcement would be a verifier change with no wire change — which is a reason not to read this as a design flaw, and not a reason to read "the fields exist" as "the protocol resists replay."

### 5.3 "The server is trusted infrastructure; the cloud holds my keys." {#custodial-cloud}

#### The framing {#custodial-cloud-framing}

A cloud agent, KMS, or HSM-as-a-service holds and uses your private keys and is the authority (custodial-wallet / cloud-KMS mental model).

#### Why it is a category error {#custodial-cloud-error}

In the KERIA/Signify architecture the cloud agent "never has access to the decryption keys" and holds "only the public keys and blake3 hash of the next keys" in cleartext (signify-ts README; raw/10 section 2). "Agents... don't have the secrets of the client" (keria README). The custodian is "a blind store + relay, not a signer." Inverting the usual asymmetry, the client authenticates the server: the agent signs every response, and the client rejects a response "from a different remote agent" or one whose signature fails (signify-ts clienting.ts, L240-255).

#### The reframing {#custodial-cloud-reframing}

"Signing at the edge": key generation and event signing happen on the client; the cloud does event storage (encrypted) and validation only (signify-ts README; raw/10 section 1). Externally the agent is "just another KERI node relaying edge-signed CESR" and "contributes no authority to the controller's events" (raw/10 section 4). A cloud agent adding authority is the CA/federation prior reasserting itself.

### 5.4 "Federation decentralizes." {#federation}

#### The framing {#federation-framing}

Centralization is cured by federating — a hierarchy of trust domains.

#### Why it is a category error {#federation-error}

KERI people see federation as compounding the disease, not curing it. Centralization "provides a locus for abuse, and creates silos. This is typically solved by aggressive federation (centralization hierarchies)," and "When you combine these 'solutions', you get the worst of all worlds, not the best" (OS > 1). Trust registries get the same verdict: "a band aid; they just move the centralization back to a different level of the architecture" (x509-prob.md).

#### The reframing {#federation-reframing}

Decentralization comes from self-certifying roots plus chaining, not from federated hierarchies. In the vLEI graph "A verifier receiving an employee's credential can traverse the chain back to GLEIF without consulting a trust registry. The entire graph is self-certifying" (acdc-vc-diff.md > Real-World Validation). Chaining "eliminates the need for trust registries" (x509-prob.md).

### 5.5 "Secure the pipe (VPN/TLS) and the data inside is safe." {#secure-pipe}

#### The framing {#secure-pipe-framing}

Transport-layer security (TLS/VPN) protects data end to end.

#### Why it is a category error {#secure-pipe-error}

"The walls of a pipe may be a secure perimeter, but every place where a pipe ends is a gap"; a realistic routed path has "at least 8" joints where "data is siphoned off, trust rules change, or trust input data changes while holding rules constant" (ASAAU > 3.6). This is not hypothetical: SSL-visibility appliances deliberately MITM TLS, and eIDAS reforms "appear to be planning legislation that allows the same attack to be carried out by national governments" (ASAAU > 3.6). And "Secure pipes protect data in motion, but not data at rest" (ASAAU > 3.6).

#### The reframing {#secure-pipe-reframing}

"Move Security with the Data, Not the Transport" (GOC > 8) — sign (and where needed encrypt) the payload itself, so authenticity travels with the data through every joint. This is message-level security (IETF MLS) and ToIP's Trust Spanning Protocol, not transport-level. The honest caveat, which a reviewer should preserve: KERI deployments still keep TLS for cheap defense-in-depth, but "do not expend massive effort guaranteeing that our secure pipes are perfectly leak-proof" (ASAAU > 3.6).

---

## 6. SD-JWT / W3C-VC / DID "decentralized" drift tells {#vc-drift-tells}

This family is the subtlest, because the outsiders here believe they are already doing decentralized identity. The KERI position is that SD-JWT, W3C-VC, and most DID methods imported PKI/OAuth assumptions and thereby re-created centralization one level up while losing fidelity.

### 6.1 "A credential is a signed envelope (paired signature)." {#signed-envelope}

#### The framing {#signed-envelope-framing}

A verifiable credential is data plus a `proof` block; the signature travels with the container because the format says so (W3C-VC `proof`, JWT bundle, X.509 `tbsCertificate` + `signature`).

#### Why it is a category error {#signed-envelope-error}

A paired signature binds to the container context and only to the current verification moment. ACDCs are not directly signed at all: they are "bound to the Issuer's Key State... and the Issuer's Key State is signed. This enables the Key State of the Issuer to change independently of the ACDC state" (ACDC spec > Binding to Key State, L1673). The explicit contrast: in schemes "where the credentials are signed directly... a key rotation forces all the credentials signed with a given set of keys to be revoked; otherwise, a key compromise would enable the compromiser to issue... forged [credentials]" (ACDC spec, L1675).

#### The reframing {#signed-envelope-reframing}

ACDCs use anchored signatures: a provable KEL association independent of container context. Validity is judged against "the issuer key state AS OF its KEL anchor's sequence position, not current key state or wall-clock" (keripy-knowledge invariant H1; keri-primer.md > 3.3). NIST SP 800-102 is the grounding: a signed message "provides no assurance that the private key was used to sign the message at that time" (keri-primer.md > 3.3). Anchoring removes that ambiguity without an external timestamp authority.

#### The citation to hand an outsider, and two guards on it {#signed-envelope-citation}

The Dossier specification swept its own text for this exact conflation and now states the correction more flatly than the ACDC spec does. [N] "A dossier is not a signed document. The issuer does not compute a signature over the dossier ACDC and attach that signature to it as proof of authenticity" (Dossier spec > How a Dossier Is Issued: Anchoring, Not Attached Signatures, L13-14 @`b9227753c`); "The signature exists on the anchoring key event, not on the dossier. What binds the issuer to the dossier is the anchor: a commitment to the dossier's SAID" (L27-28). The schemas carry it too, which is the useful part for an implementer: an endorsement "is authenticated by anchoring... It is not signed and carries no attached signature" (Dossier spec schemas/endorsement.json, `description`, L5). It is the better citation for an outsider than the ACDC spec's Binding to Key State section because it argues from key rotation and log properties rather than from ACDC internals: an attached signature can be checked "only against the key that produced it, and nothing in the signature itself establishes when it was made" (L32-34), so "once that key is rotated or compromised, a verifier has no way to distinguish a signature made while the key was authoritative from one made afterward" (L34-36). Two guards, because a reviewer who arrives at this row from the slogan will over-read it. First, the partition is drawn on lifespan, not on artifact kind: the same spec says "key events are signed, and so are the short-lived transactional objects... Dossiers, endorsements, and other ACDCs are anchored" (L45-55), so "ACDCs are never signed" overstates the doctrine and misstates its reason. Second, an attached signature is explicitly permitted in the ephemeral case — a dossier that "lives only for the duration of a single interaction, and that will never be verified after the issuer's next key rotation, MAY be authenticated by an attached signature" (L59-62) — guarded by the sentence that makes the permission safe: "A verifier MUST NOT treat an attached signature as equivalent to an anchor when evaluating a dossier as of any referenceTime other than the present" (L77-79). The doctrine is about what survives a rotation, not about which bytes may carry a signature.

### 6.2 "DIDs already solved decentralized issuance." {#dids-solved-it}

#### The framing {#dids-solved-it-framing}

DIDs create indirection — issue to an identifier, not a key — so holder key rotation is handled; the problem is solved.

#### Why it is a category error {#dids-solved-it-error}

They solved half the problem. "Evidence is also *issued by* an identifier... If the issuer updates their identifier, old evidence is invalidated" — "This risk is poorly understood in SSI circles" (x509-prob.md > Much better alternatives). Worse, "*most DIDs, including crowd favorites like did:web, can only be resolved to the current key state*," so historical actions are unprovable unless the method supports `versionId`/`versionTime`, which most lack (was.md > Mitigation 3). An issuer key compromise then "invalidates all the evidence they have ever created" — "the driver's license bureau whose recover-from-breach plan required all current license holders to come back to the office" (was.md).

#### The reframing {#dids-solved-it-reframing}

A transferable AID resolves to key state at any point in time via KEL replay, so issuer-side rotation does not invalidate historical evidence. "AIDs can be transformed to DIDs, but the opposite transformation is typically impossible" (sdjwt-acdc.md > 2.2) — the AID is the richer, lossless form. This is the RAW-vs-JPEG doctrine: keep the lossless ACDC authoritative and generate a VC when an ecosystem needs one; "once you've chosen a lossy format as your primary evidence, you cannot reconstruct what you've lost" (acdc-vc-diff.md > Lossless vs. Lossy).

### 6.3 "SD-JWT gives you selective disclosure and issuer flexibility." {#sd-jwt}

#### The framing {#sd-jwt-framing}

SD-JWT is a standard, flexible, standalone token supporting selective disclosure and any identifier type.

#### Why it is a category error {#sd-jwt-error}

SD-JWTs are standalone envelopes, so they "will need registries of trusted issuers... centralized, governed, and managed for scale," which "reinforce[s] boundaries between verticals" (sdjwt-acdc.md > 2.4). They sign a key, not an identifier (`kid` points at the key), so "*tokens are only designed to be evaluated against current key state*. If keys change, all existing tokens become invalid" (sdjwt-acdc.md > 2.3). And `iat` is self-asserted (sdjwt-acdc.md > 2.3). Identifier flexibility, far from a virtue, "makes it much more difficult to predict or enforce security properties" (sdjwt-acdc.md > 2.2). "OAuth2 and OIDC and SD-JWTs use JWTs as tokens; they inherit the same limitation" (was.md > Mitigation 3).

#### The reframing {#sd-jwt-reframing}

ACDCs "prove the bona fides of issuers by chaining to other ACDCs" instead of registries (sdjwt-acdc.md > 2.4); they anchor to a rotating identifier's key state, not a static key; and they mandate AID issuers so security properties are predictable. Even the term is corrected: "selective disclosure" has "a long and unpleasant history in financial regulation, where it refers to... illegal behavior"; KERI prefers "graduated disclosure" (sdjwt-acdc.md > 1).

### 6.4 "Canonicalize the JSON (JCS / JSON-LD) so the signature is stable." {#json-canonicalization}

#### The framing {#json-canonicalization-framing}

To hash a credential, normalize its JSON with a canonicalization algorithm (JCS, or JSON-LD's URDNA2015).

#### Why it is a category error {#json-canonicalization-error}

`{"a":1,"b":2}` and `{"b":2,"a":1}` "are semantically identical but have different cryptographic hashes," and JCS "normalization logic is brittle" (keri-primer.md > 4.1). In JSON-LD "this fragility has led to 'term redefinition' vulnerabilities, where the meaning of a signed credential can be altered without invalidating the signature" (keri-primer.md > 4.1, citing W3C vc-data-integrity issue #272; acdc-vc-diff.md > Loss 6). And `@context` URLs "cause link rot" (acdc-vc-diff.md > Loss 6).

#### The reframing {#json-canonicalization-reframing}

KERI/ACDC canonicalization is insertion order — "The natural canonical ordering for such mappings is insertion order" — and lexicographic ordering is called "un-natural," forcing "oddly-labeled fields... merely to ensure that the lexicographic ordering matches a given logical ordering" (CESR spec > Order-Preserving Data Structures, L1250-1252). Schemas are referenced "by its cryptographic content, not its location" (a SAID), so "there is no link that can rot" (acdc-vc-diff.md > Loss 6). A reviewer who reaches for JCS is importing exactly the fragility KERI designed out.

### 6.5 "A self-referential identifier can't be cryptographically bound / a UUID is fine." {#uuid-identifiers}

#### The framing {#uuid-identifiers-framing}

A content identifier must live outside the content (you can't hash a thing that contains its own hash); a UUID is a perfectly good identifier.

#### Why it is a category error {#uuid-identifiers-error}

The SAID dummy-derivation transcends the "can't be self-referential" assumption: fill the id field with dummy characters, digest, then overwrite (CESR spec > Generation and Verification Protocols, L1200-1206). And an identifier that is self-referential but not cryptographically bound "is a security vulnerability" — "Anyone can place such an identifier inside some other serialization and claim that the other serialization is the correct serialization" (CESR spec > SAID discussion, L1194) — which is precisely the plain-`id`/UUID failure mode. "The problem with a UUID is that it has no relationship to the data" (keri-primer.md > 3.2).

#### The reframing {#uuid-identifiers-reframing}

A SAID is both self-referential and bound, so "An ACDC is not a mutable document; it is a crystallized fact" (keri-primer.md > 3.2). "An AID is a self-certifying identifier (SCID)," not a "domain name, which is rent-seeking text, or a UUID, which is arbitrary entropy" (keri-primer.md > 2.1).

---

## 7. "Security means invulnerability / prevention / finality" tells {#invulnerability-tells}

This cluster is the one the security-analysis corpus treats as the single most dangerous, because it is invisible to the reviewer holding it.

### 7.1 "A secure system prevents forks / equivocation." {#preventing-forks}

#### The framing {#preventing-forks-framing}

Security means preventing entire classes of attack (forks, conflicting histories), typically via consensus.

#### Why it is a category error {#preventing-forks-error}

"KERI, as specified, adopts a survivability-oriented security model" (standard-analysis.md > 0). "KERI is explicitly not designed around invulnerability" (background.md > 4.5.1). Forks and equivocation by malicious controllers are "*anticipated disturbances*, not protocol failures" (background.md > 4.5.1). The named failure mode: "Failure to align the evaluator's objective function with KERI's stated survivability-oriented goals risks category errors that systematically mischaracterize KERI's security properties" (background.md > 4.5.1). The canonical analogy: criticizing KERI for not preventing malicious-controller duplicity "is analogous to criticizing a smoke detector for not preventing fires" (dg-c02-claude.md > 5).

#### The reframing {#preventing-forks-reframing}

Security is a gestalt of "invulnerability, detectability, evidence preservation, recoverability, and mission-level continuity under disturbance" (standard-analysis.md > 0). "Detection (rather than prevention) allows KERI to operate with low latency while ensuring that any dishonesty is provable" (keri-primer.md > 2.6). The correct question is "not 'can duplicity occur?' — it can — but 'how quickly is it detected, and what happens when it is?'... a deployment question, not a protocol question" (wtbo.md > 5).

### 7.2 "Not duplicity-resistant? Then it's broken." {#duplicity-evident}

#### The framing {#duplicity-evident-framing}

The thesis line "KERI is therefore not duplicity-resistant but only duplicity-evident" reads as an admission of weakness.

#### Why it is a category error {#duplicity-evident-error}

Whether it is a criticism "depends entirely on reading of 'resistant.' If 'resistant'=prevention, the statement is accurate/faithful; if 'resistant'=detection+response (survivability), the phrasing *understates* KERI's model. The word 'only' subtly imports an invulnerability bias" (dg-c03-claude.md, sections 2 and 5). "No criticism survives objective-function alignment" when KERI is evaluated as survivability-oriented (dg-c03-claude.md).

#### The reframing {#duplicity-evident-reframing}

"It doesn't try to make duplicity impossible — that would require global consensus... It makes duplicity *provable and attributable*" (wtbo.md > 4). Duplicity by a controller is "potentially completely self-destructive with respect to the identifier" — a detected fork is "fatal to the reputation of the identifier" (KERI spec, L1842; keri-primer.md > 2.6). Evident-and-fatal is a stronger deterrent posture than the outsider's resistant-but-opaque one, not a weaker one.

### 7.3 "All validators must converge on one truth (finality)." {#finality}

#### The framing {#finality-framing}

A correct system reaches finality — every validator agrees on a single history.

#### Why it is a category error {#finality-error}

"KERI does not guarantee global convergence" (background.md > 7.4.2); "Permanent divergence is an allowed outcome" (background.md > 7.4.4). Validators "do not share state by default," "May have disjoint trust relationships," and "May never interact directly" (background.md > 7.1). Safety is redefined: "Safety in KERI means: Validators do not accept *invalid* histories" — it "does not mean validators agree on a single history" (background.md > 7.5.1). Crucially, divergence is a protocol-level property, "permitted even with observers present," not merely a deployment artifact (dg-c03-claude.md > 3).

#### The reframing {#finality-reframing}

Correctness is local to a validator and observer-dependent; "a valid KERL is not necessarily unique" (00-lens.md, claim 2). Importing blockchain-finality expectations is, "in the security model's own words, a category error" (00-lens.md, claim 2). A reviewer expecting finality is measuring against a property KERI deliberately declines to provide because providing it would require the global consensus KERI rejects.

### 7.4 "A threshold of witnesses gives global safety." {#witness-threshold}

#### The framing {#witness-threshold-framing}

If M-of-N witnesses agree, the event is globally safe.

#### Why it is a category error {#witness-threshold-error}

"Agreement thresholds do not imply global safety" (background.md > 4.7). KAWA's consistency property "is the strongest KAWA property and is *conditional*. It does not hold if the controller is malicious" (background.md > 5.6, P2). A malicious controller "can simply run its own witnesses" (thesis via background.md > 8.2). "KAWA alone determines *local durability*. Observers determine *global detectability*" (background.md > 5.9).

#### The reframing {#witness-threshold-reframing}

Witness agreement is a per-controller, local second-factor structure named the Threshold Of Accountable Duplicity — literally "threshold of accountable duplicity," not Byzantine finality (keripy eventing.py, L1945; raw/09 section 4). Global detectability is a separate, optional observer-layer property (assumptions A8-A11, "None of A8-A11 are enforced by KERI," background.md > 6.4). Conflating the two is how a threshold gets mistaken for finality.

### 7.5 "If a proof assumes an honest controller, it's insecure against dishonest ones." {#honest-controller}

#### The framing {#honest-controller-framing}

Del Giudice's strongest results assume an honest controller, so KERI requires honest controllers.

#### Why it is a category error {#honest-controller-error}

The honest-controller premise is "a proof-technique simplification, NOT a KERI deployment requirement... Removing it does not break KERI's security — it shifts the focus from prevention to detection and recovery" (dg-c06-claude.md, sections 3 and 5). Observer mechanisms are "explicitly excluded from Del Giudice's formal analysis" yet "central to KERI's security model" (background.md > 8.3). Malicious controllers "trigger detection, not failure" (dg-c06-claude.md).

#### The reframing {#honest-controller-reframing}

Verifiers assume nothing about controller honesty: "Protection against a fully malicious controller" is an explicit non-goal handled by the observer layer, not by the KAWA proofs (background.md, sections 1.3 and 2.1). A reviewer must distinguish "the proofs' scope" from "the protocol's model" — the corpus's meta-pattern is that every apparent weakness resolves to a deliberate non-goal, a proof-scope limitation, or a deployment-maturity gap (dg-c06-claude.md; raw/07 section 8).

---

## 8. Role-confusion tells: witness, watcher, backer, agent {#role-confusion-tells}

### 8.1 "A witness is a CA / a blockchain validator / a notary." {#witness-not-ca}

#### The framing {#witness-not-ca-framing}

The witness vouches for the identity or participates in consensus.

#### Why it is a category error {#witness-not-ca-error}

"A witness makes no such assertion... A witness simply stores and serves events" (keri-primer.md > 2.6). "Witnesses make no assertion about identity — they don't claim 'this key belongs to this entity.'... That is a fundamentally different role than a CA" (wtbo.md > 4). The trust model is inverted from a CA's: "witnesses are assumed to be potentially malicious" (keri-primer.md > 2.6). The ground truth: a registry may even have zero backers (keripy vdr/eventing.py, L89; raw/09 section 4).

#### The reframing {#witness-not-ca-reframing}

A witness is a controller-designated, non-transferable AID that provides availability plus duplicity accountability — a per-controller threshold/second-factor structure, not a consensus node (keripy eventing.py, L3051-3057; raw/09 section 2). The normative constraint that witnesses "MUST be non-transferable" so a validator can verify receipts directly (KERI spec, L353; background.md > 2.3) is part of KERI-as-specified, not a discretionary simplification.

### 8.2 "A watcher enforces / can distrust an identifier." {#watcher-enforcement}

#### The framing {#watcher-enforcement-framing}

The detection layer has teeth — like a browser root program distrusting a CA.

#### Why it is a category error {#watcher-enforcement-error}

"A KERI watcher that detects duplicity is making an observation — surfacing cryptographic evidence that the relying party confirms independently," whereas a browser vendor distrusting a CA is "making an enforcement decision... with immediate global consequences" (wtbo.md > 4). "Watchers cannot unilaterally 'distrust' an identifier... The worst a dishonest watcher can do is stay silent about duplicity it has seen" (wtbo.md > 4). "Observers increase *visibility*, not *control*" (background.md > 6.6).

#### The reframing {#watcher-enforcement-reframing}

Watchers, jurors, and judges cleanly separate detection, evidence-preservation, and policy-adjudication so "no single observer both detects AND rules" (raw/07 section 5). The relying party keeps the enforcement decision. The default and recommended pattern is a local resolver — an in-process watcher in the verifier's own stack querying multiple witnesses — so "the verifier trusts its own code," and depending only on a shared "super watcher" "is undesirable, as it encourages centralization" (wtbo.md > 5).

### 8.3 "A witness can serve a delegate's KEL, so it vouches for the delegation." {#witness-delegation}

#### The framing {#witness-delegation-framing}

If a witness serves a delegated AID's events, the delegation is thereby validated.

#### Why it is a category error {#witness-delegation-error}

"A witness is NOT a watcher. A witness may serve a delegate's KEL without the delegator's seal/KEL; a validator must independently obtain the delegator's KEL (OOBI) before validating" (keripy-knowledge invariant D3; landmine L4). "Witnesses store/serve, they do not vouch for cross-AID anchors" (31-landmines.md, landmine L4). A delegated event is authorized only by a seal in the delegator's KEL (keripy-knowledge invariant D1).

#### The reframing {#witness-delegation-reframing}

Delegation is cooperative and two-sided: the delegatee's `dip`/`drt` references the delegator, and the delegator anchors a seal to it — "Both MUST participate" (KERI spec > Cooperative Delegation, L1610). A validator must OOBI the delegator independently; treating a witness as having done that work is a role-boundary violation the code explicitly warns against (landmine L4, open twins #1317/#846).

### 8.4 "`DID` means the delegator vouches for all its delegatees." {#did-trait}

#### How this row differs {#did-trait-difference}

This row is unlike the others in the chapter, and the difference is stated first because it is load-bearing. Its refutation rests on [N1.1] text alone, together with an editor's ruling that is [P] ([section 8.4](#did-trait-settled)). A reviewer may press this framing as a question; they may not yet be told they are wrong on the standardizing line's authority.

#### The framing {#did-trait-framing}

The `DID` (Delegate-Is-Delegator) configuration trait says a delegated AID may be treated as its delegator. The outsider reads that as underwriting, and reads underwriting as transitive — the delegator vouches for the delegatee, and therefore for whatever the delegatee goes on to delegate. This is the X.509 path-validation reflex in a new field name: in PKI a CA's signature does propagate down the subtree, and a reviewer who grew up on chain-building will supply that propagation here without noticing they supplied it.

#### Why it is a category error, in the half that is safe to assert {#did-trait-error}

[N] `DID` has no specified consequence on either branch. Both say a validator may treat the AIDs as equivalent; neither says what a validator MUST or MUST NOT do with the equivalence — not whether a signature under the delegatee's key state satisfies a policy written against the delegator's AID, not whether the equivalence survives the delegatee's own rotations, not what happens when the delegator later revokes the delegation. So "vouches" asserts something no specification text supports in either direction. It is not that the trait means less than the outsider thinks; it is that the trait's operational meaning is an open gap, and a critique or a design that leans on a reading of it — broad or narrow — is leaning on nothing. That much holds on the standardizing line today.

#### The half that is not yet normative {#did-trait-forward}

[N1.1] On `v1.1` the one-sentence trait acquires a nine-sentence rationale that forecloses the transitive reading explicitly: "The assertion is granular and applies only to the delegation relationship established by the event in which it appears", and "It says nothing about any Delegatees that the Delegatee may itself delegate" — rather, "each such delegation makes or withholds the assertion in its own delegated inception event" (KERI spec > Configuration traits field, v1.1 L381 @`3753f3797`). The same rewrite grounds the trait's warrant in cooperative delegation rather than in a new mechanism: the delegator already approves the `dip` by anchoring a seal, and "the Delegator thereby also consents to the appearance of the `DID` config trait in that event." [N] `main` at `fbdd4a615` carries none of this — one sentence, one table row, no placement rule and no granularity language.

#### Why this row belongs in the chapter {#did-trait-why-here}

So the broad reading is reasonable from the standardizing line, and that is why this belongs in the chapter rather than being quietly corrected. The honest statement to a reviewer is: the transitive reading will be wrong, on the evidence of the branch most likely to become the next standard, and it is not wrong yet. Two further facts keep it unsettled. `v1.1` also makes `DID` `dip`-only — it "MUST NOT appear in a non-delegated Inception, `icp` event" — while `main`'s own worked example places it in exactly that position, so the branches disagree about placement as well as about scope. And no worked example on either branch shows the trait in the position `v1.1` prescribes, so an implementer has no serialization to check against. ~~Whether `main`'s example is a defect the rewrite is fixing, or the two branches genuinely disagree about what `DID` means, is not something the corpus has a source for.~~ Superseded 2026-10-15; the next subsection gives the source.

#### The placement question, settled by the editor {#did-trait-settled}

The corpus now has a source, and it settles the placement half. Sam Smith, the specification's editor, on `main`'s worked example: "Yeah, putting DID in a plain, non-delegated ICP, as an example, was an oversight." (keripy GitHub > #1570, reply of 2026-08-04, R-012, https://github.com/WebOfTrust/keripy/discussions/1570#discussioncomment-17898407) [P]. Earlier in the same thread he gave the rule and its reason: "THE DID sits in a Delegatee Inception event.", because "Putting DID in a delegator would be ambiguous since a delegator could also be a delegatee of a higher level delegator." (https://github.com/WebOfTrust/keripy/discussions/1570#discussioncomment-17896521). So `main`'s example is a defect that `v1.1` fixes, not a second meaning of the trait. The placement rule is now the editor's ruling as well as [N1.1] text, and it is still not [N], because `main` at `fbdd4a615` keeps the example (`"c": ["DID"],`, KERI spec, L591). The scope half moves in the same direction, though the comment is not specification text: a `DID` in a delegatee's inception "means the controller of the Delegator of that delegatee and the Delegatee is the same", an assertion about one pair of AIDs and one controller, which is not an endorsement that propagates. The general lesson the struck sentence carried survives: a gap in this corpus's sources is not evidence that a question is open upstream, and the place to look first was the discussion thread, not the specification.

### 8.5 "The observer layer is KEL discovery / caching, and a 'super watcher' is a bigger cache." {#observer-not-cache}

#### The framing {#observer-not-cache-framing}

Watchers, jurors and judges exist to make KELs findable and queryable at scale — a CDN or a read replica sitting in front of the witnesses. On that reading the three names are three points on one feature curve, and "super" marks whichever end of it has the most features.

#### Why it is a category error {#observer-not-cache-error}

Discovery in KERI is already solved, and solved somewhere else entirely: an OOBI is deliberately untrusted — "a KERI OOBI by itself is considered insecure with respect to KERI" — and KERI "does not, therefore, need its own dedicated discovery network; OOBIs with URLs will do" (KERI spec, L2633, L2635) [N]. The observer layer is not what fills that gap. Samuel Smith made the objection directly, against a draft KID that had described watchers as "a convenient way to centralize how state is *queried*": "The watcher, judge, and jurors each play distinct important roles in the KERI security posture of a validator[;] they are not merely discovery mechanisms for KELs[,] so having amnesia about why their roles are distinct is going to be problematic" (WebOfTrust/kids#1, 2023-11-05) [P]. ~~The roles are held apart precisely so that "no single observer both detects AND rules" (raw/07 section 5);~~ Cut 2026-10-03 (verification): not found in `keri-security-analysis` at `149fa6c35` (searched all files, including background.md); the wording is raw/07's own summary. That the roles are distinct stands on Smith's kids#1 sentence above; the stated reason for the separation is now unsupported. A cache has no such structure to preserve, so the infrastructure reading quietly discards it. It also demotes the honest limits [chapter 02, section 9](02-security-model-and-threat-posture.md#observer-layer) records — O1 detection "may be delayed or incomplete," O2 "Proof does not imply remediation," and observers supply no "Guaranteed detection... Automatic resolution... Enforcement" whatsoever (background.md, sections 6.5 and 6.6) — from security properties into performance caveats, which is the register in which a reviewer will then fail to take them seriously.

#### The reframing {#observer-not-cache-reframing}

Watcher, juror and judge are three security roles — detection, evidence-preservation, policy-adjudication — deliberately separated, and "super" is a statement about the scope of KELs one of them covers, not about extra features, so super jurors and super judges are as coherent as super watchers ([chapter 02, section 9](02-security-model-and-threat-posture.md#observer-layer); kids#1) [P]. Query convenience may be a by-product of running one at scale; it is never the reason the role exists. The reviewer's discipline is the same one [section 8.3](#witness-delegation) enforces one boundary further down: ask which role a component actually performs before accepting the noun it is labelled with.

---

## 9. Semantic tells: authorship, authenticity, meaning, aliases {#semantic-tells}

### 9.1 "A signature means the signer authored / asserts the content." {#signature-authorship}

#### The framing {#signature-authorship-framing}

To sign is to claim authorship or to assert the truth of what is signed.

#### Why it is a category error {#signature-authorship-error}

"People often treat a signature as if it were a claim of authorship. That is sometimes true. But it is not what signatures *are* in general" (sign-author.md). "A signature is evidence that a signing mechanism ran" (sign-author.md); meaning comes from role, ceremony, policy, or protocol. Cryptographic systems "inherited a bias to assume signing was an assertion of authorship from early message-signing use cases" (who-sign.md). UNCITRAL's Model Law lists intent-to-be-bound, endorsement, association, and attestation-of-presence as distinct signature meanings.

#### The reframing {#signature-authorship-reframing}

"Asking [who is signing] is insightful. Expecting a single, clean answer is usually a mistake" — control, authority, responsibility, and attribution "overlap but do not coincide" (who-sign.md). Applied: a dossier issuer's signature "does not necessarily attest to the veracity of the claims within the evidence, but rather to the integrity and composition of the collection" (Dossier spec > Role of the Issuer). A citation ACDC "MUST NOT be construed as an endorsement" (citation/index.md).

### 9.2 "Cryptographic verification proves the claim is true." {#authenticity-veracity}

#### The framing {#authenticity-veracity-framing}

A verified credential means its contents are true.

#### Why it is a category error {#authenticity-veracity-error}

Authenticity and veracity are "orthogonal." "Judgments about authenticity can — if managed very carefully — be reduced to an objective mathematical computation, whereas judgments about veracity inherently require subjective assessments of reputation" (authenticity-vs-veracity.md > Independence). The ACDC validation algorithm — "fetching key state, verifying a signature, testing revocation, and comparing data and structure to a schema" — "can prove that an issuer remains committed to a citation — but only the interaction context... plus governance... establishes what proposition is true" (citation/index.md).

#### The reframing {#authenticity-veracity-reframing}

KERI proves who said it and that it wasn't tampered with, not whether it is true. A notary "witnesses the authenticity of your affidavit, but makes no commitment as to its veracity" (authenticity-vs-veracity.md). A reviewer who treats a green checkmark as a truth oracle has collapsed the two axes.

### 9.3 "Automate the whole verification, including the final trust decision." {#automated-trust}

#### The framing {#automated-trust-framing}

If verification is cryptographic, automate it end to end.

#### Why it is a category error {#automated-trust-error}

"The gap between proved and guessed is the gap a man-in-the-middle attacker lives in" (oia.md > Proved versus guessed). "Introducing is not the same thing as proving there is no man in the middle. We will automatically introduce. We won't automatically prove" (MA > 7).

#### The reframing {#automated-trust-reframing}

"Automate the introduction. Automate the proof where you can. But never automate the verification of the proof" (oia.md). A human "weighs that evidence and decides it is good enough to trust *this* party, for *this* purpose, now." Structurally, deployments encode the distinction in a `{caveat}` field ("?" = unverified vs "(verified)"), because "Confusing guesses with something that's been verified... is the very attack surface that hackers exploit" (MA > 4).

### 9.4 "An alias / petname is an identifier." {#aliases}

#### The framing {#aliases-framing}

A human-friendly name can be used in logic, cached, and parsed for meaning.

#### Why it is a category error {#aliases-error}

"Treat an alias as an identifier and you get collisions; cache it... and you get staleness; parse a stranger's alias for meaning and you get an attack surface" (oia.md). "An alias must never be parsed for meaning by anyone but its creator" (oia.md). The applied rule is shouted in source: "ALIASES ARE NOT UNIQUE, AND THEY CAN CHANGE OVER TIME. THEY MUST NEVER BE PARSED FOR MEANING, AND THEY MUST NOT BE TREATED AS IDENTIFIERS" (MA > 2).

#### The reframing {#aliases-reframing}

"It is globally unique AIDs that MUST be used in all system logic" (HWGA, step 9). An alias is "a memory aid, not evidence." A reviewer should flag any logic that keys on a display name.

### 9.5 "Multisig means it's an organization; one key is enough for org identity." {#multisig-org}

#### The framing {#multisig-org-framing}

Single-signature suffices for an organization's identity, and multisig ≈ organization.

#### Why it is a category error {#multisig-org-error}

"It is not a generally true equivalence that multi-sig = org. Some orgs consist of only one person, so their AIDs are single-sig" (HWGA). And single-key org identity is a millennia-old anti-pattern: multi-attestation for high stakes appears in "Code of Hammurabi law 7, Deuteronomy 19:15, double-entry accounting"; "why are we imagining... it's safe to use the single-signature mechanism of X509 certs as the only gate on unlocking the entire reputation of modern corporations?" (x509-prob.md > One key isn't realistic). In X.509 multisig governance "is not knowable or verifiable by the public... Hackers thrive on opacity" (keri-primer.md > 2.4).

#### The reframing {#multisig-org-reframing}

"Multisig is optional and infinitely variable, but defining and following policy about it is required" — KERI's innovation "is less about inventing and more about exposing," publishing fractionally-weighted thresholds directly in the KEL (keri-primer.md > 2.4). "Opaque control collapses meaningful distinctions" (who-sign.md).

---

## 10. Data-modeling and disclosure tells {#disclosure-tells}

### 10.1 "Bundle all the claims into one big credential, then selectively disclose." {#bundled-credentials}

#### The framing {#bundled-credentials-framing}

A credential carries many claims; privacy comes from a fancy selective-disclosure crypto layer over the bundle.

#### Why it is a category error {#bundled-credentials-error}

"Many non-ACDC verifiable credentials provide bundled credentials because there is no other way to associate the attributes... These bundled credentials could be refactored into a graph of ACDCs. Each... separately disclosable and verifiable thereby obviating the need for Selective Disclosure" (ACDC spec > Selective Disclosure annex, L2739). And over-investing in cryptographic unlinkability is "an exercise in diminishing returns" because "there is no cryptographic mechanism that precludes statistical correlation among a set of colluding Verifiers" (ACDC spec > Bulk-issued, L2785).

#### The reframing {#bundled-credentials-reframing}

Chaining reduces the need for exotic selective-disclosure crypto; graduated disclosure ("disclose enough to enable more disclosure") uses only "digests and digital signatures or anchors," satisfying "minimally sufficient means" (ACDC spec > Graduated Disclosure, L1747; ACDC spec > Basic selective disclosure, L686). Where statistical linkability is the real threat, the answer is Contractually Protected Disclosure (chain-link confidentiality) plus independent-AID bulk issuance — legal "strings attached" plus technical measures — not more cryptography alone (ACDC spec, L1790, L2887).

#### Sharpened 2026-10-03: detectability, not cost {#bundled-credentials-detectability}

The stronger objection is to detectability, not cost. The spec text above argues that cryptographic unlinkability buys little. Samuel Smith's discussion [#1098](https://github.com/WebOfTrust/keripy/discussions/1098) [P] argues something harder: that unlinkable zero-knowledge proofs cost a security property KERI treats as non-negotiable. With an unlinkable ZKP, "the Issuer of the credential is unable, by virtue of that unlinkability, to detect that a credential has been fraudulently issued"; "Detection requires that the Issuer collude with or cooperate with the verifier and/or holder, which cooperation breaks unlinkability"; so "the use of unlinkable ZKPs is therefore precluded to preserve the detectability of an Issuer signing infrastructure compromise" — a sentence that ends by calling it one of "the inviolable properties of KERI/ACDCs" (raw/16 section 1a). The Issuee half follows: "Likewise, the key compromise of an Issuee (Holder) can be made detectable using a presentation registry. Which would also be defeated by an unlinkable ZKP." (raw/16 section 1a). The verdict is "a static SMT predicate proof preserves KERI's security properties, whereas a dynamic ZKP predicate proof defeats them" (raw/11, #1098). So the outsider who proposes layering unlinkable ZKPs over a credential to make it "more private" is not offering a free upgrade. In KERI's terms they are trading away detect-and-recover ([section 7.1](#preventing-forks)) at both ends of the credential, which is the property that makes KERI's survivability posture work at all.

Three boundaries keep this from being over-read. First, it is one author's position in one discussion, which has zero comments, and not a surveyed or community result; repeat it as Sam's argument. Second, its Issuee half rests on a mechanism whose status is uneven: the presentation registry is [K] verifier-side on `/ipex/grant` at keripy `80f77b73b`, Issuee-controlled and fail-closed, with no specification text on either branch (raw/16 section 7; [chapter 10](10-presentation-registries.md)), and #1098 says Issuee detectability "can be made" available, not that it must be used — so the argument is that a credential format must not foreclose the registry, not that every presentation uses one (raw/16 section 1a). Third, the body was last edited 2026-09-26, and the corpus cannot say whether the Issuee sentence was in the October 2025 original, so it is evidence of Sam's position at that date, not of when he first held it (raw/16 section 1a).

### 10.2 "A compact / SAID-only credential is private." {#compact-not-private}

#### The framing {#compact-not-private-framing}

If a block is elided to its SAID, its contents are hidden.

#### Why it is a category error {#compact-not-private-error}

A public (no top-level `u`) ACDC is still rainbow-attackable from its SAID plus schema: "an adversary may be able to reconstruct the block contents merely from the SAID... and the Schema... using a rainbow or dictionary attack" (ACDC spec > UUID Fields, L89). Compact form "only provides compactness, not privacy" (ACDC spec > Targeted Public-attribute, L501).

#### The reframing {#compact-not-private-reframing}

Privacy requires a high-entropy blinding factor (`u`) so "the cardinality of the power set allowed by the schema is at least as great as the entropy of the SAID digest algorithm" (ACDC spec, L89). A reviewer who equates compaction with confidentiality has missed the blinding requirement.

### 10.3 "Dereference the schema `$schema`/`$id` to validate." {#schema-dereference}

#### The framing {#schema-dereference-framing}

Schema validation fetches and runs the schema the URL points to.

#### Why it is a category error {#schema-dereference-error}

Dynamic schema references enable a schema-revocation attack (change the resource → invalidate every ACDC using it) and a semantic-malleability attack (shift the semantics so the ACDC still validates but downstream behavior changes) (ACDC spec > Static Schema, L196-198). Dereferencing `$schema` for validation code "would be an attack vector" (ACDC spec > Schema dialect, L226).

#### The reframing {#schema-dereference-reframing}

"All Schemas MUST be static, i.e., Schemas MUST be SADs and therefore verifiable against their SAIDs" (ACDC spec, L200). `$id` is a bare SAID; the validator controls the tooling dialect. The applied corpus enforces this: "`$id` is a SAID... Never invent or hand-patch a SAID" (bakobo/schema/KNOWLEDGE_TRANSFER.md).

### 10.4 "Wrap or ingest a foreign credential (X.509, W3C-VC, mDL) as a native root of trust." {#foreign-credentials}

#### The framing {#foreign-credentials-framing}

Import foreign credentials directly into the trust graph.

#### Why it is a category error {#foreign-credentials-error}

"Direct reference to non-ACDC material without a wrapper is NOT RECOMMENDED, as it places an untenable burden on the verifier to parse and validate an arbitrary foreign format, understand its lifecycle, and locate its revocation mechanism" (Dossier spec > Incorporating Evidence). ~~Foreign VCs belong as "*derivative artifacts* wrapped/bridged, not as native roots of trust" (raw/05 section 5).~~ Cut 2026-10-03 (verification): not found in acdc-vc-diff.md (or any paper) at papers `68a5e2f76`, and not in notes 05; the wording is raw/04 section 9's own summary, the same text cut from [chapter 06](06-governance-ecosystems-and-interop.md) this pass. The claim that foreign VCs are derivative, not native roots of trust, is now unsupported here; the dossier quote before it carries the "wrap, don't reference directly" point on its own.

#### The reframing {#foreign-credentials-reframing}

Bridge, don't adopt: a designated bridging party verifies the foreign credential per its native rules and issues a Foreign Artifact ACDC attesting "I verified this on date X per policy Y" — which "transforms the problem of verifying a foreign format into the problem of trusting the attestation of the bridging party" (Dossier spec > 3). Trust is explicit and issuer-scoped (fields like `art_posture` and `rev_latency`), "not systemic" (faa/index.md). This is the "not-a-CA" interop stance: KERI bridges other ecosystems rather than becoming one of them.

### 10.5 "I2I / edge operators do multi-hop authority reasoning." {#edge-operators}

#### The framing {#edge-operators-framing}

The `I2I` edge operator performs chain-of-authority evaluation.

#### Why it is a category error — and a prose/machine gap {#edge-operators-error}

[K] I2I is enforced as plain AID string equality and nothing more: the issuer of this ACDC must equal the issuee of the node it points to (`if op == 'I2I' and issuer != farIssuee: return None`, keripy vdr/verifying.py, L478-479 @`b8f60166b`; re-verified at L481 @`80f77b73b`; raw/09 section 9), which is the entirety of the check — an equality of qb64 AID strings, with no chain-of-authority reasoning beyond it. That has been true across every commit the corpus has pinned, and it is what makes "the operator does multi-hop authority reasoning" a genuine outsider tell rather than a claim about one release.

#### Support restated 2026-09-15 {#edge-operators-restated}

The support for this row was restated on 2026-09-15; the row itself did not change. The accurate statement of the operator family at `b8f60166b` is this: of five recognized unary operators (`UnaryOps = ('I2I', 'NI2I', 'DI2I', 'E1E', 'NOT')`, keripy vdr/verifying.py, L41), I2I and E1E are enforced, NI2I is by construction a no-op binding check, and DI2I and NOT are recognized-but-unimplemented and fail closed with `ValidationError`; the edge `s` constraint is now enforced, with the far node required to satisfy the declared schema rather than match it; and the operator is still silently inferred when `o` is absent. Two corrections inside that. The exception DI2I raises is `ValidationError`, not `NotImplementedError`, and the difference is doctrinal rather than cosmetic: the unimplemented operators are named in the table on purpose, because "they are listed so they fail closed diagnosably instead of being dropped and silently defaulting" (keripy vdr/verifying.py, L38-39), and the exception choice is deliberate too, because "escrowing would promise a retry that can never succeed" (L445). An earlier reading of this row as "it will crash if exercised" had the mechanism backwards: it refuses, by design. And the family is five, not four — `E1E` is the fifth, present in the ACDC specification's `v1.1` branch ([N1.1], ACDC spec > Edge, L1206 @`2362e48a1`) and absent from `main`, where the unary table has four rows. Re-verified 2026-10-03: at `80f77b73b` `vdr/verifying.py` changed only in comments, the table is unchanged (`UnaryOps`, L43) and no operator was added (raw/09 section 6c).

#### A second tell: which verifier {#edge-operators-two-verifiers}

A second tell, added 2026-10-03: "the operator means what the verifier says it means." keripy now has two edge-operator evaluators, and [K] at `80f77b73b` they disagree on three axes (raw/09, section 11 item 1, sections 7e and 9). On an unrecognized token, `vdr/verifying.py` drops it — `ops = [cand for cand in ops if cand in self.UnaryOps]` (L435) — and applies its default, while the V2 IPEX evaluator in `acdc/ipexing.py` treats the edge as malformed (`if any(operator not in UnaryEdgeOps for operator in recognizedOps): return None`, L921–922). On conflicting operators in a list, `vdr/verifying.py` resolves latest-wins among the delegative ones (`op = next((cand for cand in reversed(ops) if cand in self.DelegativeOps), None)`, L436), while `ipexing.py` deleted its delegative subset and enforces every operator present, so `["I2I", "NI2I"]` is NI2I to the first and I2I to the second. On an edge with no `o`, `vdr/verifying.py` infers I2I or NI2I (`op = 'I2I' if creder.iseaid is not None else 'NI2I'`, L443) and `ipexing.py` checks no relation at all (L910–911). The same edge can therefore pass one and fail the other, and the SEDI fixtures use `["E1E", "NI2I"]`, which both evaluate identically, so keripy's tests do not exercise the divergence. The reviewer's discipline is to ask which verifier, at which commit, before accepting any statement of what an operator does. Do not resolve the disagreement by picking a side: `vdr/verifying.py` cites the ACDC specification for latest-wins, and that citation has not been checked against the specification (raw/09 section 11 item 3), so the corpus does not yet know which module is right, or whether the specification decides it. Two scoping facts bound the stakes: the V2 IPEX handler has no caller in `src/keri` (raw/09 section 7b), and neither module is in KERIA's `keri==1.2.14` dependency ([section 12](#verify-the-code)).

#### The unknown-operator trap {#unknown-operator-trap}

The unknown-operator trap is where this bites next. Sam named the hazard himself when narrowing #1515 to `E1E` alone: "we want to avoid it falling into the unknown operator trap" (#1515, 2026-07-18; raw/09 section 11 item 2) [P]. On 2026-10-01 he gave a concrete SEDI use case for `I1I` ("issuer is issuer") and its delegated variant `DI1I` on leaf-to-core edges (#1515; raw/09 section 11 item 2) [P]. Corrected 2026-10-03 (verification): this sentence previously said he "proposed" them on 2026-10-01; both operators were already proposed in the discussion's opening post of 2026-07-17 ("I1I which means near side Issuer AID must equal far side Issuer AID", #1515 body), and the 2026-10-01 comment is headed "Concrete Use Case in SEDI for I1I and DI1I operators". Neither exists in `src/keri` at `80f77b73b` — they appear only in comments in `tests/sedi/test_sedi.py` — and an edge carrying `o: "I1I"` today is filtered out by `vdr/verifying.py` (L435) and then defaulted, but is malformed to `acdc/ipexing.py` (L921–922) (raw/09 section 10 item 7). A proposed operator is the trap in its purest form: an Issuer who writes it before both verifiers know it gets a silent downgrade from one and a refusal from the other.

#### The reframing {#edge-operators-reframing}

The doctrinal meaning of `I2I` (issuer-to-issuee same-holder binding) is real and useful — "it is what distinguishes 'Alice presenting *her own* credentials' from 'two credentials that merely share an AID'" (sedi-present-age-portrait/index.md) — but multi-hop authority is assembled by the recursive edge walk, not by any one operator. `E1E` sharpens the point rather than blunting it, because it is an identity relation and not a delegative one: [N1.1] "Unlike `I2I` and `DI2I`, which are delegative Operators... `E1E` is an identity relation between the two ACDCs' Issuee AIDs" (ACDC spec > Edge, L1223 @`2362e48a1`), which makes it less authority-like than the operator an outsider already over-read. This is the bridge to [section 12](#verify-the-code): believe the schema and the prose about what an edge means, but verify against the code what the verifier actually does — and, as [section 12](#verify-the-code) now records, verify the code's comments about the spec the same way.

#### Two readings of I2I {#i2i-two-readings}

"Same-holder binding" above is this corpus's gloss, and the specification's editor frames the operator differently [P]. In his operator proposal "the number `2` is used to symbolize delegation" (keripy GitHub > #1515, discussion body opened 2026-07-17 and edited through 2026-10-01, read as cached on 2026-10-14, https://github.com/WebOfTrust/keripy/discussions/1515), and when a worked example used `I2I` for a relation between two credentials' issuees he ruled it misapplied: "So the edge defines an an identity relation not a delegation relation." (keripy GitHub > #1505, comment of 2026-07-17, R-029, https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-5004919975). The fix was a non-delegative operator, `E1E`. Both readings compute the same check, the string equality of near issuer and far issuee quoted above, so this row's correction of the outsider holds under either. What differs is the intended meaning, and it matters when an issuer chooses an operator: on the editor's account `I2I` is a link in a chain of delegated authority, and an edge that only asserts that two credentials concern the same party wants `E1E` or no operator at all. Added 2026-10-15 from raw/21 contradiction T-09. The gloss is kept because it describes the computation correctly; this paragraph records whose semantics it is not.

---

## 11. The one attack you must be able to name: the retrograde attack {#retrograde-attack}

A reviewer who cannot articulate the retrograde attack will mistake KERI's most important structural feature (anchored, sequenced signatures) for gratuitous complexity — so it earns its own section as the deepest anti-pattern KERI corrects.

### The outsider prior {#retrograde-prior}

A digital signature, on its own, is strong evidence of who signed and that the content is intact.

#### Why that is dangerous {#retrograde-danger}

"By themselves, digital signatures are much weaker evidence than casual thinkers might imagine," because they are "difficult to sequence relative to a compromise or revocation event" (was.md, intro). If an attacker ever obtains a key, they can forge evidence "that looks like it originated in the past, *forever*" — and this remains possible "even if she rotates or revokes K before Malfoy steals it" (was.md > Retrograde attack). The backdating window "has no end point." X.509, JWTs, OAuth2, OIDC, SD-JWTs, and current-key-state-only DIDs (did:web) all "embrace this limitation — you can ask whether one is valid *now*... but you can't ask whether it was valid a week ago" (was.md > Mitigation 3). All three intuitive mitigations fail: contextual clues are unreliable, retroactive revocation is "dangerous and foolish" and lets the signer repudiate their own acts, and "verify against current key state only" makes after-the-fact audits impossible (was.md > Mitigations 1-3).

#### The KERI reframing {#retrograde-reframing}

Anchored signatures: "Keep tamper-evident records that can prove how a given signing event relates in time to changes in the associated key state" (was.md > Solution). Validity is judged against key state "AS OF its KEL anchor's sequence position, not current key state or wall-clock" (keripy-knowledge invariant H1). Then "once Alice rotates her key, Malfoy's attack window closes forever," and "An analysis of an anchored signature will produce the same result no matter when it happens" (was.md > Conclusion). The ground truth: `Tever.verifyAnchor` does `db.kels.getLast(pre, on=seqner.sn)` then asserts the anchored event's SAID matches — "the anchor must be the issuer KEL event at exactly that sn" (keripy-knowledge invariant H1; keripy vdr/eventing.py). NIST SP 800-102 is the external grounding (keri-primer.md > 3.3). And the load-bearing caveat for a reviewer: the credential `Verifier` may not re-run this anchor check (landmine L15, HIGH, flagged as a recon hypothesis) — so the defense is real at the TEL-event layer but should be confirmed at the credential-presentation layer.

---

## 12. The master reflex: verify the code, distrust the prose {#verify-the-code}

Everything above concerns priors an outsider brings to KERI. This final discipline concerns a prior a reviewer might bring about KERI's own implementations — namely, that the elegant prose is faithfully realized in the code. It often is; sometimes it is not. The single most valuable habit for an adversarial reviewer of this codebase is to check what the code actually enforces before believing the prose.

The keripy contributor knowledge base states this as a worldview claim: "every externally supplied event, signature, key, receipt, or credential is *hostile input until verified*... 'looks well-formed' is not 'is authorized'" (00-lens.md, claim 3). But it applies reflexively to the prose about the code, too. The documented prose/machine gaps are concrete and load-bearing:

- `DI2I` is documented but unimplemented. [K] At `b8f60166b` it raises `ValidationError` carrying "DI2I validation is not implemented" (keripy vdr/verifying.py, L450-452), and the IPEX leaf evaluator independently returns an unsatisfied edge for it (keripy acdc/ipexing.py, L776-777). A repo-wide search returns only those two rejection sites plus the two tables that name it. The gap survives; the mechanism is a deliberate closed door, not a crash. Re-verified unchanged at `80f77b73b` (keripy vdr/verifying.py, L453-455, keripy acdc/ipexing.py, L926-927; raw/09 section 9).
- Credential anchor re-validation may be missing at the presentation layer, undermining the retrograde defense the prose celebrates (landmine L15, HIGH — and hedged by its own author as a recon hypothesis, which is how it should be carried).
- Witness receipting waits for ALL witnesses, not TOAD — "the spec rule; keripy's `WitnessReceiptor` currently waits for ALL witnesses instead — that is a defect, not the invariant" (30-invariants.md, F2; landmine L9).
- Pre-rotation verification can go permissive on a digest-code mismatch, "silently excluded from threshold satisfaction rather than failing closed — weakening the pre-rotation check (the firewall)" (landmine L6, HIGH).
- A new CESR code registered in one table but not its shadow tables "round-trips as primitive but invisible to SAID derivation... fails late and silently" (landmine L5). The discipline is permanent; the urgency that used to be attached to it is not. See the note below.

Two of those bullets used to say something this chapter no longer says, and the retraction is more instructive than the bullets were. Edge-operator grouping (`&&`/`||`), DAG acyclicity and `NI2I` chaining were listed here as "read but not enforced" on the authority of landmines L16/L17. That is superseded as of keripy `b8f60166b`. [K] The boolean-combinator vocabulary was never keripy's model in the first place — the operators are unary and per-edge — and m-ary grouping is now genuinely implemented in the V2 IPEX path (`EdgeGroupOps = ("AND", "OR")`, defaulting to AND, reduced at keripy acdc/ipexing.py, L903), where an empty group is malformed rather than vacuously true. The code moved toward the prose while the citation stood still. That is the same failure this section warns about, pointing the other way, and it is why a reviewer should date a prose/machine gap rather than assert it.

### The reflex is bidirectional {#bidirectional-reflex}

And the reflex is bidirectional, which is the sharpening this section needed. A code comment about a specification is exactly as much a piece of prose as a specification's claim about code, and deserves the same treatment. The live example: keripy's own operator table is annotated [K] "E1E is a keripy extension not yet in the spec's normative operator table" (keripy vdr/verifying.py, L40 @`b8f60166b`), tracing the idea to a discussion rather than to spec text. That is true of the standardizing line, where `E1E` occurs zero times — and false of `v1.1`, where [N1.1] the operator is defined with its own table row and a paragraph distinguishing it from the delegative operators (ACDC spec > Edge, L1206 and L1223 @`2362e48a1`). A reviewer who trusted the comment would conclude that `E1E` has no specification behind it at all, and would be wrong in a way that matters for tiering: it is not backed by keripy alone, it is [K] and [N1.1] together, which is a different claim about how likely it is to survive. Trusting a code comment about a spec is the same error as trusting spec prose about code, and it is the harder one to catch, because a comment sits next to the code it describes and inherits the code's credibility without having earned it.

Superseded 2026-10-03, and the example is kept because the lesson survives it. At `80f77b73b` the comment no longer says what the paragraph above quotes. It now reads "E1E is normative on the spec's v1.1 branch (kswg-acdc-specification#197). It is absent from the 1.0 text currently under ToIP ratification" (keripy vdr/verifying.py, L40-41 @`80f77b73b`; raw/09 section 6c). So the comment now agrees with the `v1.1` reading this chapter gives. The provenance is the instructive part: the change landed in commit `d9ba3d9da`, a comments-only commit authored by Daniel Hardman, the corpus's own author (raw/09 section 6c). A comment the corpus wrote is not independent evidence for what the corpus already believed, so the [N1.1] tier for `E1E` still rests on the specification text cited above and not on the comment. The rule this section teaches applies to friendly comments as much as to wrong ones.

#### keripy main is not the deployed stack {#main-not-deployed}

One more conflation to refuse: keripy `main` is not the deployed stack. [K] KERIA pins `"keri==1.2.14",` (KERIA pyproject.toml, L30 @`928ce26a4`), tightened from `"keri>=1.2.13,<1.3",` at `7e685edaa` (raw/10 section 11a). keripy `main` is on the `2.1.0-dev1` line (raw/09 section Pin), and the work this chapter cites at `b8f60166b` and `80f77b73b` — IPEX V2, `E1E` enforcement, the edge-operator divergence of [section 10.5](#edge-operators), presentation-registry verification — is on that line and not in KERIA's dependency. "keripy does X" at a `main` commit is therefore not evidence that a KERIA deployment does X; where KERIA matches keripy `main` it reimplemented the behavior in its own code, which is separate evidence (raw/10 section 11a). A further boundary sits inside keripy itself: the V2 IPEX handler in `acdc/ipexing.py` has no caller in `src/keri`, so its [K] claims are about code that exists and is tested, not about anything a shipped keripy command does (raw/09 section 7b). A reviewer who reads "the reference implementation enforces it" should ask which line, which module, and whether anything calls it.

#### Shadow tables: discipline without urgency {#shadow-table-discipline}

The shadow-table discipline stands; the urgency attached to it does not. The landmine is written as advice about work in flight — "The Falcon PR must touch every shadow table" — and that framing is now wrong in a way worth stating, because nothing is blocked when nothing has been written. [K] keripy at `b8f60166b` has no post-quantum codes at all: a search of `src/` for FN-DSA, ML-DSA, SLH-DSA, Dilithium, Falcon, SPHINCS, Kyber and ML-KEM returns only the `falcon` web framework, and `src/keri/core/` has zero matches. The knowledge base is candid about why: its own plan defers the flagship work behind an unresolved question — which of two conflicting in-repo Falcon design documents is canonical — and neither design has landed. So keep the discipline and drop the deadline: a digest, key or signature code registered only in `MatterCodex` and `Matter.Sizes`, and not in `Saider.Digests`, `Serder.Digests` and the relevant `*Dex` sets, will round-trip as a primitive while being invisible to SAID derivation, and will fail late and silently. That will be true of whatever PQ codes eventually arrive, and it is true today of any new code at all. A reviewer should also refuse the adjacent overstatement: [N] the CESR specification's `main` at `bad6edd84` carries zero post-quantum codes — no FN-DSA, no FIPS reference, none of `1AAQ`/`1AAR`/`2AAA` — and everything CESR says about post-quantum on the standardizing line is the hash firewall of pre-rotation. The code table is [N1.1] work on `v1.1` at `65fd7518b`, and no shipped implementation carries it; the only implementation anywhere is an unmerged branch on a personal fork, which is not [K] and must never be cited as evidence about the ecosystem.

#### Knowledge-base staleness {#kb-staleness}

A staleness warning attaches to every citation of the knowledge base in this section. The KB is pinned at `9489ac9bd`, and its own declared code baseline is keripy `60ab9e08d` — 493 commits behind `b8f60166b`, against a version string that has moved from `2.0.0-dev6` to `2.1.0-dev1`. Its banner that all twenty landmines still hold was verified at that baseline, and can no longer be repeated unqualified: L16 and L17 are known to be superseded (above), which is one counterexample, and the remaining eighteen are neither confirmed nor refuted at the current pin. The KB remains a good map of where behavior lives and a good catalogue of the shapes a defect takes. It is not, at this distance, evidence about what keripy does today — for that, cite keripy at a named commit. The reflex this whole section teaches applies to the KB as readily as to any other prose, and the corpus has been slower to apply it there because the KB is written in the register of someone who has already applied it.

#### The reviewer's checklist {#reviewer-checklist}

The corresponding reviewer discipline is the KB's pre-change checklist, reframed as a critique checklist: Whose authority? (any external trust dependency is a violation of the root-of-trust claim). Adversarial input? (is this input verified or merely parsed?). Which invariant does this guard protect? — "Can't name it? Assume it's load-bearing." External contract? (wire codes, sizes, field order, SAID derivation, version strings are external contracts — a change that passes keripy's own tests but diverges from the spec is a defect, because it "silently breaks interop," 00-lens.md, claim 5). Anchor-relative? (judge a signature against the anchor's key state, not "now"). And a corollary from claim 6: "do not 'simplify away' a guard you don't fully understand; treat an unexplained check as protecting an invariant until proven otherwise" — because "Complexity is load-bearing" (00-lens.md, claim 6; wtbo.md, Note [d]).

#### Why this is the master shibboleth {#master-shibboleth}

The reason this reflex is the master shibboleth: KERI's guarantees are real but conditional, and the conditions live partly in the spec's assumptions and partly in whether the code honors them. A reviewer who reads only the prose will over-credit the system; a reviewer who reads only the code will miss the intent that tells them which discrepancies are bugs versus design. The insider move is to hold both — "graph = fast structure; disk artifacts = ground truth; use both, trust accordingly."

---

## 13. Quick-reference: the tell → the reframing {#quick-reference}

For rapid triage during a review, the recurring tells and their one-line corrections:

- "Who's the trusted authority/CA?" → The identifier is the root of trust; replay the KEL, no authority (keri-primer.md > 1.3; cr-ad-trust.md > 4).
- "Revoke the cert / where's the CRL/OCSP?" → Key state lives in the KEL; credential status is an anchored TEL state, no phone-home (ACDC spec, L1693; cr-ad-trust.md > 2).
- "Revoke just the compromised copy of a bulk-issued credential." → [P] Revocation of authority is universal across the set; a compromised key is repaired by rotation; only a compromised derivation salt sinks the set (#1574, R-042; [section 3.4](#bulk-copy-revocation)).
- "CESR should encode every variant of every algorithm." → [P] "Too much agility is a bad thing. There is a goldilocks amount of agility." (CESR spec GitHub > #165, comment of 2026-03-19, R-018); admitting little-scrutinized variants weakens the ecosystem ([chapter 04, section 5.6](04-cesr-and-the-wire.md#goldilocks-agility)).
- "Consult the registry at verify time." → "A registry consulted at verification time is a phone-home in disguise" (sda.md > 7).
- "You need a blockchain / global order / consensus / finality." → Per-identifier local ordering suffices; global ordering is an explicit non-goal (KERI spec, L1836; background.md > 1.3).
- "Renew / rotate to a new cert." → Identity is sameness; a transferable AID persists across rotation (keri-primer.md > 2.1; cr-ad-trust.md > 1).
- "Bearer token / session / API key." → Fresh per-request signature over an AID; no long-lived server secret. Scoped to one method+path and one key state, where a token is scoped to neither — but neither side enforces freshness, so on that pair it replays until a rotation (GOC > 2; sda.md > 1; KERIA @`7e685edaa`, signify-ts @`ffba8406e`).
- "Federation decentralizes." → Federation re-centralizes; chaining to self-certifying roots decentralizes (OS > 1; acdc-vc-diff.md).
- "Secure the pipe (TLS/VPN)." → Move security with the data (MLS/TSP), not the transport (ASAAU > 3.6).
- "Sign the credential (paired signature)." → Anchor to key state. The partition is lifespan, not artifact kind: "The signature exists on the anchoring key event, not on the dossier" (Dossier spec @`b9227753c`, L27-28; ACDC spec, L1673).
- "DIDs/SD-JWTs already do this." → They verify against current key state only and re-introduce issuer registries (was.md > Mitigation 3; sdjwt-acdc.md, sections 2.3-2.4).
- "Canonicalize the JSON (JCS/JSON-LD)." → Insertion order, not lexicographic; schema by SAID, not URL (CESR spec, L1250; acdc-vc-diff.md > Loss 6).
- "A UUID / plain `id` is fine." → A self-referential-but-unbound id is a substitution vulnerability; use a SAID (CESR spec, L1194).
- "Security = preventing forks." → Survivability, not invulnerability; "a smoke detector doesn't prevent fires" (background.md > 4.5.1; dg-c02-claude.md > 5).
- "Not duplicity-resistant = broken." → Duplicity-evident and fatal-to-reputation is the stronger deterrent (wtbo.md > 4; KERI spec, L1842).
- "Everyone converges on one truth." → Permanent divergence is allowed; safety ≠ agreement (background.md, sections 7.4-7.5).
- "A witness is a CA / validator." → A witness stores and serves, makes no identity assertion, is assumed possibly malicious (keri-primer.md > 2.6; keripy eventing.py, L1945).
- "A watcher enforces." → A watcher observes; the relying party enforces (wtbo.md > 4).
- "The observer layer is discovery / caching." → Discovery is OOBIs, untrusted by design; watcher/juror/judge are three security roles held apart, and "super" names scope, not features (KERI spec L2633-2635; WebOfTrust/kids#1 [P]; [chapter 02, section 9](02-security-model-and-threat-posture.md#observer-layer)).
- "A signature = authorship/truth." → A signature is evidence a mechanism ran; authenticity ≠ veracity (sign-author.md; authenticity-vs-veracity.md).
- "Publish the AID at two well-knowns to strengthen the binding." → OOBA governs willingness to bootstrap, not authenticity; it "does not change the trust model of an OOBI" (KERI spec, L2838).
- "`DID` means the delegator vouches for its delegatees' delegatees." → No specified consequence on either branch; [N1.1] "It says nothing about any Delegatees that the Delegatee may itself delegate" (KERI spec v1.1, L381).
- "Add unlinkable ZKPs for privacy." → [P] Sam's argument: unlinkability defeats detectability of Issuer signing-infrastructure compromise and, via a presentation registry, of Issuee key compromise, so "the use of unlinkable ZKPs is therefore precluded" — his position in #1098, not a surveyed result (raw/16 section 1a; [section 10.1](#bundled-credentials)).
- "The edge operator means X." → Ask which verifier at which commit. [K] at `80f77b73b` keripy's two evaluators disagree on unknown tokens, on conflicting operators in a list, and on an absent `o`, and the corpus has not established which is right; proposed `I1I`/`DI1I` are unimplemented and would hit that split (raw/09 section 11 items 1–2; [section 10.5](#edge-operators)).
- "The prose says the code does X." → Verify, in both directions and with a date. `DI2I` fails closed with `ValidationError`, not unimplemented-by-crash; receipting waits for all witnesses; and a code comment about a spec is prose too — at `b8f60166b` keripy called `E1E` a non-spec extension, which was false of `v1.1`; at `80f77b73b` the comment agrees with `v1.1`, written by the corpus's own author, so it corroborates nothing (keripy vdr/verifying.py, L40 @`b8f60166b`, L40–41 @`80f77b73b`; ACDC spec v1.1, L1206; landmines L9/L15).
- "keripy does X, so deployments do X." → keripy `main` is the 2.1.0-dev line; KERIA pins `keri==1.2.14`, and the V2 IPEX handler has no caller in `src/keri` (raw/10 section 11a; raw/09 section 7b; [section 12](#verify-the-code)).

---

## 14. Load-bearing assumptions and honest residuals {#residuals}

A reviewer inoculated against outsider tells must not swing to the opposite failure of treating every KERI reframing as unassailable. The reframings above are correct within KERI's stated objective function, but several rest on assumptions a reviewer is entitled to probe, and a few outsider critiques survive the reframing intact.

### What the reframings are conditional on {#reframing-conditions}

The reframings are conditional on: cryptographic soundness (A1); the controller keeping pre-rotation keys secret (compromise of both current and pre-rotated keys is "catastrophic and unrecoverable" — the identifier must be abandoned, 00-lens.md, claim 4; wtbo.md > 5); and, for the detection story, the optional observer layer (A5, A8-A11 — "None of A8-A11 are enforced by KERI," background.md > 6.4). The detection-not-prevention posture is only as good as the watcher/observer infrastructure actually deployed, and "A KERI deployment without robust watchers and governance is not a secure system" (cr-ad-trust.md > 5).

#### The genuinely surviving residuals {#surviving-residuals}

The genuinely surviving residuals — the outsider critiques that do not dissolve on reframing — are, per the security-analysis corpus, all about ecosystem maturity, never about the protocol: the observer/watcher infrastructure is immature; the "super watcher" pattern (as at GLEIF) reintroduces "a centralized trust dependency that KERI was designed to avoid" (cr-ad-trust.md > 5; DG-C05); the formal literature is thin (the strongest analysis is "a 2025 ETH Zürich Master's thesis... not peer-reviewed," wtbo.md > 5); and KERI lacks the legal standing (eIDAS) X.509 enjoys — "a gap of legal recognition, not of technical capability" (wtbo.md, Note [c]). KERI's advocates frame these as "constraints of *youth*, not of *architecture*" (wtbo.md > 6) — which is itself a claim a reviewer should treat as an assertion to be tested against trajectory, not a proven fact.

#### The trusted-third-party relaxation is two concessions {#two-concessions}

A residual sharpened this pass: the trusted-third-party relaxation is two concessions, not one. The corpus has long recorded the first. In the presentation-registry origin document, a Verifier that requires a key rotation as part of a presentation is conceded to "violate[] the maxim that security not be dependent on a trusted third party", justified on the grounds that the harm is localized and "the party most likely to be harmed is the Verifier… which provides incentives for them to protect themselves" [P]. The second is sharper, has never been written down here, and attaches to the very mechanism offered as the answer to the first. A presentation registry gives the Issuee [P] "an Issuer-Verifier-protected mechanism to detect compromise of its signing keys" — which is to say it requires an Issuer that is a different party and does not collude, and a Verifier that actually enforces, since "The verifier then enforces the protection by not accepting presentations (grant messages) that are not so anchored". The mechanism offered as Issuee self-protection is therefore two-party-dependent at both ends. Neither concession is an oversight and both are stated plainly by their author; the point is that a reviewer pressing KERI on third-party dependence is entitled to both, and that the answer to the first one does not escape the critique. ~~Note the tier: this is [P] throughout — a design in two discussions with no implementation and several unsettled questions, whose substance belongs to the presentation-registry chapter, not here.~~ Superseded 2026-10-03. The argument is still [P], but the mechanism is no longer unbuilt. [K] keripy at `80f77b73b` verifies presentation registries verifier-side on `/ipex/grant`: every Issuee registry declared across the disclosed DAG must bind the `grant`, the registry must be incepted by that Issuee, the binding must be dated no later than the receiver's KRAM acceptance, and any failure rejects the `grant` — "Reject any malformed, missing, or invalid presentation factor." (keripy acdc/ipexing.py, L616 @`80f77b73b`; raw/16 sections 7.1–7.2). There is no specification text on either ACDC branch (raw/16 section 7.8), the V2 handler has no caller in `src/keri`, and KERIA's `keri==1.2.14` does not carry it ([section 12](#verify-the-code)). The code bears on the second concession in one respect worth noting: the Verifier's enforcement, which the design merely asked for, is now what keripy's verifier does when a declaration is present, and the declaration itself is "the issuer's signal that this Issuee must" authenticate the grant through the registry (keripy ipexing.py, L1516; raw/16 section 7.2). So both ends of the two-party dependence are visible in the code, which is the reverse of escaping it. The substance belongs to [chapter 10](10-presentation-registries.md), not here. The shibboleth table still has no row for it, deliberately, though the reason has narrowed. The code has settled on "presentation registry" (raw/16 section 7.7), but the discussions still use two names, the specifications say nothing, and the code departs from the developed design in two places that [chapter 10](10-presentation-registries.md) carries as divergences rather than settled design. A framing cannot be an outsider tell while the insiders' own sources still disagree about what the thing requires.

#### A provenance residual in the corpus's own method {#provenance-residual}

This residual bears on this corpus's own method, and on how much weight any adversarial review carries. One of the papers in the corpus retracted a claim about its own review process in this window. An earlier version described its analysis as having had "two independent adversarial expert reviews, one in vision science, one in security usability"; the current version corrects that to say those passes "were conducted by AI models prompted to argue from a named lens, not by human domain experts", and adds that "They are a structured way to attack one's own assumptions, not independent validation" (m-glance.md > 1). A sibling paper made the same move, restating itself as "theoretically motivated, adversarially self-reviewed, and empirically untested" (amp-diff.md > 6.3). The generalization is uncomfortable and is stated here because it applies inward as well as outward: an adversarial review run by AI personas arguing from named lenses is a structured self-attack, and reporting it as independent validation is a provenance error of exactly the kind the tier markers exist to prevent. This corpus's own panels are that kind of exercise. Their output is worth what a disciplined self-attack is worth, which is not nothing — and it does not license any claim that survived one of them being treated as externally checked.

#### An unresolved disagreement inside the corpus's own doctrine {#doctrine-disagreement}

This disagreement is unresolved, which is why it is here and not in the table. [Section 9.3](#automated-trust) gives the rule that the final verification step is never automated, and the paper it rests on offers eyeball comparison of an identifier visualization as the honest way for a human to take that step. A second paper, revised in this window, concludes that casual eyeball comparison of such a visualization is not marginally weak against an adversary who has ground offline but "is broken" — and that a seeded commit-and-reveal walk is therefore "a requirement, not an enhancement" wherever an adversary is in scope (amp-diff.md > 4.3.9). The first paper has not been revised to match, and neither acknowledges the other. A reviewer should know the disagreement exists before relying on either. It is deliberately not a shibboleth row: "compare the identifier by eye" is not an outsider tell, because the insider source recommends it, and the paper that would refute it describes itself as empirically untested. That is a live question in the doctrine, not a category error to catch.

#### Holding both {#holding-both}

The disciplined reviewer, then, holds two things at once: the outsider tells in [sections 2 to 11](#pki-tells) are category errors that should be caught and reframed, and the residuals in this section are legitimate and should be pressed. Confusing the two — dismissing a real maturity critique as a category error, or accepting a category error as a real critique — is the failure mode this entire section exists to prevent. The tell that a reviewer has internalized the doctrine is not that they praise KERI, but that they can state, for any given critique, whether it survives objective-function alignment — and cite why.

---

## Sources {#sources}

- #1098 — WebOfTrust/keripy discussion #1098, ACDC with Static Age Predicate Proof SMT, Samuel M. Smith, https://github.com/WebOfTrust/keripy/discussions/1098, created 2025-10-27, last edited 2026-09-26, fetched 2026-10-03. Where a [P] here is an argument rather than a mechanism, as with [section 10.1](#bundled-credentials)'s case against unlinkable proofs, it is its author's position, not a surveyed or community result. Mined in raw/16 (section 1a) and raw/11.
- #1515 — WebOfTrust/keripy discussion #1515, on edge operators (`E1E`, `I1I`, `DI1I`), Samuel M. Smith, https://github.com/WebOfTrust/keripy/discussions/1515, opening post 2026-07-17, comments cited from 2026-07-18 and 2026-10-01. Mined in raw/09 (section 11).
- 00-lens.md — keripy-knowledge load-bearing claims, a file in keripy-knowledge (see that entry), 00-lens.md, at the same pin, `9489ac9bd` (2026-07-02). Mined in raw/08.
- 30-invariants.md — keripy-knowledge invariants, a file in keripy-knowledge (see that entry), 30-invariants.md, at the same pin, `9489ac9bd` (2026-07-02). Mined in raw/08.
- 31-landmines.md — keripy-knowledge landmines, a file in keripy-knowledge (see that entry), 31-landmines.md, at the same pin, `9489ac9bd` (2026-07-02). Mined in raw/08.
- ACDC spec — Authentic Chained Data Containers (ACDC) specification, Trust Over IP. trustoverip/kswg-acdc-specification, spec/spec-body.md, main @`f0bd097de` (2026-08-28) for unmarked and [N] citations; v1.1 @`2362e48a1` (2026-09-11) for the [N1.1] `E1E` citations in [section 10.5](#edge-operators) and [section 12](#verify-the-code). Mined in raw/03.
- acdc-and-mtc.md — Comparison: ACDCs and Merkle Tree Certificates, Daniel Hardman. dhh1128/papers, acdc-and-mtc.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- acdc-vc-diff.md — ACDCs and W3C VCs: Lossless vs. Lossy, Daniel Hardman. dhh1128/papers, acdc-vc-diff.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- amp-diff.md — Amplifying Difference: Perceptual Design and Verification of Human-Centric Entropy Visualizations, Daniel Hardman. dhh1128/papers, amp-diff.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- ASAAU — Authorizing Services and Automation Users, Provenant. provenant-dev/origin-platform, docs/authorizing-services-and-automation-users.md, main @`cb758b1b5` (2026-08-26). A private client repository; vendor practice, [V]. Mined in raw/12.
- authenticity-vs-veracity.md — Authenticity vs. Veracity, Daniel Hardman. dhh1128/papers, authenticity-vs-veracity.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- background.md — KERI: Canonical Background for Security Analysis (v0). dhh1128/keri-security-analysis, background.md, main @`149fa6c35` (2026-04-23, the repository's only commit; mined 2026-07-17). Security analysis, not specification text; it carries no provenance marker. Mined in raw/07.
- bakobo/schema/KNOWLEDGE_TRANSFER.md — Knowledge transfer notes for the schema repository. bakobo/schema, KNOWLEDGE_TRANSFER.md, main @`cfcbdcc7a` (2026-10-02). Applied schema corpus, [V]. The quoted sentences were re-checked at `cfcbdcc7a` on 2026-10-15; the file was removed from the repository afterwards, in `4267478` ("Remove references to private repositories"), so it is citable at this pin and not at the repository head. Mined in raw/11.
- CESR spec — Composable Event Streaming Representation (CESR) specification, Trust Over IP. trustoverip/kswg-cesr-specification, spec/spec-body.md, main @`bad6edd84` (2026-08-28) for unmarked and [N] citations; v1.1 @`65fd7518b` (2026-08-26) for the [N1.1] post-quantum code table mentioned in [section 12](#verify-the-code). Mined in raw/02.
- CESR spec GitHub — Sam Smith's comment of 2026-03-19 on trustoverip/kswg-cesr-specification pull request #165 (R-018), read from the read-only API cache of 2026-10-14 (`.ignored/sam-rulings-cache/`) and checked against the cached text. [P]. Mined in raw/21.
- citation/index.md — Citation credential documentation. Present in both bakobo/schema (main @`cfcbdcc7a`, 2026-10-02) and provenant-dev/public-schema (main @`95a07e544`, 2026-06-16), and the quoted text is in both; the chapter does not say which was read. Applied schema corpus, [V]. Mined in raw/11.
- cr-ad-trust.md — Cryptographic vs. Administrative Trust: KERI's Witness/Watcher Architecture and X.509 Certificate Transparency. dhh1128/keri-security-analysis, cr-ad-trust.md, main @`149fa6c35` (2026-04-23, the repository's only commit; mined 2026-07-17). Security analysis, not specification text; it carries no provenance marker. Mined in raw/07.
- dg-c02-claude.md — Analysis of DG-C02, a claim from Del Giudice's thesis. dhh1128/keri-security-analysis, dg-c02-claude.md, main @`149fa6c35` (2026-04-23, the repository's only commit; mined 2026-07-17). Security analysis, not specification text; it carries no provenance marker. Mined in raw/07.
- dg-c03-claude.md — Analysis of DG-C03, a claim from Del Giudice's thesis. dhh1128/keri-security-analysis, dg-c03-claude.md, main @`149fa6c35` (2026-04-23, the repository's only commit; mined 2026-07-17). Security analysis, not specification text; it carries no provenance marker. Mined in raw/07.
- dg-c06-claude.md — Analysis of DG-C06, a claim from Del Giudice's thesis. dhh1128/keri-security-analysis, dg-c06-claude.md, main @`149fa6c35` (2026-04-23, the repository's only commit; mined 2026-07-17). Security analysis, not specification text; it carries no provenance marker. Mined in raw/07.
- Dossier spec — Dossier specification, Trust Over IP. trustoverip/kswg-dossier-specification, spec/dossier-spec-body.md and schemas/endorsement.json, main @`b9227753c` (2026-09-03). Mined in raw/04.
- faa/index.md — Foreign Artifact ACDC documentation. Present in both bakobo/schema (main @`cfcbdcc7a`, 2026-10-02) and provenant-dev/public-schema (main @`95a07e544`, 2026-06-16); the chapter does not say which was read. Applied schema corpus, [V]. Mined in raw/11.
- GOC — General Origin Platform Characteristics, Provenant. provenant-dev/origin-platform, docs/general-origin-characteristics.md, main @`cb758b1b5` (2026-08-26). A private client repository; vendor practice, [V]. Mined in raw/12.
- HWGA — How We Generate Aliases, Provenant. provenant-dev/origin-platform, docs/how-we-generate-aliases.md, main @`cb758b1b5` (2026-08-26). A private client repository; vendor practice, [V]. Mined in raw/12.
- KERI spec — Key Event Receipt Infrastructure (KERI) specification, Trust Over IP. trustoverip/kswg-keri-specification, spec/spec-body.md, main @`fbdd4a615` (2026-08-28) for unmarked and [N] citations; v1.1 @`3753f3797` (2026-08-26) for the [N1.1] `DID` trait citations in [section 8.4](#did-trait). Mined in raw/01.
- keri-primer.md — A Primer on KERI, ACDCs, and CESR, Daniel Hardman. dhh1128/papers, keri-primer.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- keri.one — keri.one homepage, Samuel M. Smith, https://keri.one/. Mined 2026-07-17 and re-verified against the live page 2026-10-03. Mined in raw/13.
- KERIA — KERIA, WebOfTrust/keria, src/keria (including authing.py), README and pyproject.toml. main @`7e685edaa` (2026-09-11) for the request-freshness claims in [section 5.2](#bearer-tokens); main @`928ce26a4` (2026-09-30) for the `keri==1.2.14` dependency pin in [section 12](#verify-the-code). Mined in raw/10.
- keripy — keripy, the KERI reference implementation, WebOfTrust/keripy, src/keri and tests/sedi. main @`80f77b73b` (2026-10-01, mined 2026-10-03) for the claims re-read in that pass, which carry that stamp; main @`b8f60166b` (2026-09-14) for claims not re-read since, which keep theirs; code locators with no commit come from earlier passes of raw/09. A keripy [K] is a claim about keripy main, on its 2.1.0-dev line, and not about KERIA, which pins keri==1.2.14 ([section 12](#verify-the-code)). Mined in raw/09 and raw/16.
- keripy GitHub — Sam Smith's comments in WebOfTrust/keripy conversations: pull request #1505 (2026-07-17, R-029), and discussions #1515 (body), #1570 (2026-08-04, R-012) and #1574 (2026-08-07, R-042). Read from the read-only API cache of 2026-10-14 (`.ignored/sam-rulings-cache/`), quotes checked against the cached text; Sam's typing errors are kept as written. [P]: an editor's comment, not specification text. Mined in raw/21.
- keripy-knowledge — keripy-knowledge, a distilled contributor knowledge base for keripy, on the orphan branch knowledge of dhh1128/keripy, @`9489ac9bd` (2026-07-02, mined 2026-09-15). Cited here for its invariants (H1, D1, D3) and landmines (L4, L5, L6, L9, L15, L16, L17). Its declared code baseline is keripy `60ab9e08d`, 493 commits behind `b8f60166b`; [section 12](#verify-the-code) says what that means for its claims. Mined in raw/08.
- kids#1 — WebOfTrust/kids#1, a GitHub conversation on a draft KERI Improvement Document about watchers, never merged; Samuel M. Smith's comment of 2023-11-05. Maintainer statements, [P]. No raw note mines it; [chapter 02, section 9](02-security-model-and-threat-posture.md#observer-layer) quotes the same thread.
- m-glance.md — Measuring the Glance: An Adversarial Estimate of Habituated Perceptual Entropy in entviz and SSH Randomart, Daniel Hardman. dhh1128/papers, m-glance.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- MA — Managing Aliases, Provenant. provenant-dev/origin-platform, docs/managing-aliases.md, main @`cb758b1b5` (2026-08-26). A private client repository; vendor practice, [V]. Mined in raw/12.
- oia.md — Opaque Identifier Aliases, Daniel Hardman. dhh1128/papers, oia.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- OS — Origin Security, Provenant. provenant-dev/origin-platform, docs/origin-security.md, main @`cb758b1b5` (2026-08-26). A private client repository; vendor practice, [V]. Mined in raw/12.
- sda.md — The Shape of Delegated Authority, Daniel Hardman. dhh1128/papers, sda.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- sdjwt-acdc.md — How SD-JWT and ACDC are similar and different, Daniel Hardman. dhh1128/papers, sdjwt-acdc.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- sedi-id/index.md — SEDI identity credential documentation. bakobo/schema, sedi-id/index.md, main @`cfcbdcc7a` (2026-10-02). Applied schema corpus, [V]. Mined in raw/11.
- sedi-present-age-portrait/index.md — SEDI Age and Portrait Presentation. bakobo/schema, sedi-present-age-portrait/index.md, main @`cfcbdcc7a` (2026-10-02). Applied schema corpus, [V]. Mined in raw/11.
- sign-author.md — Signing Doesn't Always Claim Authorship, Daniel Hardman. dhh1128/papers, sign-author.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- signify-ts — signify-ts, the TypeScript Signify client, WebOfTrust/signify-ts, src (including authing.ts and clienting.ts) and README, main @`ffba8406e` (2026-09-10). Mined in raw/10.
- standard-analysis.md — Standard Analysis Template for KERI Security Claims. dhh1128/keri-security-analysis, standard-analysis.md, main @`149fa6c35` (2026-04-23, the repository's only commit; mined 2026-07-17). Security analysis, not specification text; it carries no provenance marker. Mined in raw/07.
- was.md — Why Anchored Signatures?, Daniel Hardman. dhh1128/papers, was.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- who-sign.md — Who Is Signing?, Daniel Hardman. dhh1128/papers, who-sign.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- wtbo.md — Where Trust Bottoms Out: X.509, Certificate Transparency, and KERI's DPKI Architecture, Daniel Hardman. dhh1128/papers, wtbo.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
- x509-prob.md — Why X509 Certs Should Be Secondary Evidence of Org Identity, Daniel Hardman. dhh1128/papers, x509-prob.md, main @`68a5e2f76` (2026-09-28). Mined in raw/05 and raw/06.
