# KERI Doctrine {#doctrine}

Status: DRAFT, pending Daniel's endorsement rule by rule. Rewritten 2026-10-15 from the 9,100-word version, under three rules agreed that day: a sentence stays only if no monthly refresh could change it; grounding is a link to the bible section that holds the quotes, not a quote; and the result serves as a lens, not a digest.

## How to use this file {#use}

This file makes a reviewer reason in KERI's own terms before reading anything else. It is not a summary of KERI and not a source. Every rule links to the bible section that grounds it; cite that section, or the primary source it quotes, never this file. Pins, commit-level behavior and the state of designs still in motion live in the bible, which is refreshed monthly. This file should not need to change when they do.

The provenance markers used in the bible (`[N]`, `[N1.1]`, `[K]`, `[P]`, `[V]`, `[SAM-DIRECT]`) are defined in the legend at the top of `keri-bible.md`.

## Trust and identity {#trust}

1. The root of trust is the identifier's own key-event history. An AID is derived from its inception event, and anyone can establish who controls it by replaying its key event log. No authority, registry, ledger or federation stands behind it, and a critique that asks who vouches for the identifier is asking KERI to fill a role it removed. [chapter 01, section 3](bible/01-foundations-and-worldview.md#root-of-trust)

2. Verification is end-to-end and ambient. Anyone, anywhere, at any time can verify a log from the data alone. A service may supply the data, but a design in which verification needs a service's answer, rather than its data, has reintroduced the dependency KERI exists to remove. [chapter 01, section 4](bible/01-foundations-and-worldview.md#end-verifiability)

3. An identifier is not its current key. Identity is continuity of control across rotations, which is why renewing, re-issuing or pinning a key are the wrong frames. [chapter 01, section 6](bible/01-foundations-and-worldview.md#pki-problem)

4. KERI, CESR and ACDC are separate layers with separate promises. KERI promises key-state continuity and duplicity evidence. CESR promises a composable, self-framing encoding. ACDC promises authentic, chained data with graduated disclosure. Above them, governance frameworks decide what verified data means and whether to rely on it. A finding must name the layer it faults, because a common category error is a property demanded of the wrong layer. [chapter 01, section 5](bible/01-foundations-and-worldview.md#three-layer-stack)

## Security model {#security}

5. The objective function is survivability, not invulnerability. KERI expects attacks to succeed sometimes and aims to keep the identifier alive, make the misbehavior evident and attributable, and allow recovery. Before evaluating a criticism, name the objective function it assumes. [chapter 02, section 1](bible/02-security-model-and-threat-posture.md#survivability)

6. KERI is "duplicity-evident, not duplicity-resistant". A controller can sign two versions of its log; KERI guarantees that anyone who sees both can prove it and attribute it. A critique that faults KERI for allowing forks assumes a consensus system KERI deliberately is not. Whether anyone sees both is a deployment question: it depends on watchers, which is where honest critiques of duplicity detection belong. [chapter 02, section 3](bible/02-security-model-and-threat-posture.md#duplicity-evident)

7. A verifier assumes nothing, including that the controller is honest. Every event, signature, receipt and credential is checked before it is believed. KERI cannot stop a controller from lying, for example by signing two conflicting histories, but it makes the lie provable, so anyone relying on that controller can stop. [chapter 02, section 4](bible/02-security-model-and-threat-posture.md#zero-trust)

8. Validity is local. Each validator decides from the evidence it has, and two honest validators can hold different views until evidence reaches them. There is no global order across identifiers and no global finality, and KERI needs neither: each identifier's log orders its own events. [chapter 02, section 10](bible/02-security-model-and-threat-posture.md#local-validity)

9. Witnesses do not decide what gets recorded; the controller records the event in its own log before any witness sees it. Each witness keeps the first version it sees, so a threshold of witnesses makes conflicting versions hard to get receipted and easy to expose. That is durability and evidence, not global safety. [chapter 02, section 7](bible/02-security-model-and-threat-posture.md#kawa)

10. Roles do not blur. A witness stores and serves a controller's events, and its receipt says only that it saw this version first, never that the event is true or authorized. A watcher observes and reports; only the relying party decides what to rely on. Discovery is untrusted by design: an OOBI tells you where to look, not what to believe. [chapter 02, section 9](bible/02-security-model-and-threat-posture.md#observer-layer)

11. Every guarantee is conditional on named assumptions. A statement of a KERI security property that omits its assumptions overstates it, and a deployment that silently fails an assumption is where real findings live. [chapter 02, section 6](bible/02-security-model-and-threat-posture.md#assumptions)

## Keys {#keys}

12. Pre-rotation separates the authority to sign from the authority to rotate. The next keys are committed as digests before they are needed, so stealing the current signing keys does not let an attacker take the identifier, provided the next keys were kept apart from them. This is the firewall the whole recovery story rests on. [chapter 03, section 5](bible/03-key-management-and-identifier-lifecycle.md#pre-rotation)

13. A signature is judged against the key state in force where it is anchored in the signer's log, not against the signer's latest state. That defeats the retrograde attack: someone who later obtains a retired key cannot forge signatures that appear to date from when the key was valid, because an unanchored signature cannot be placed in time at all. [chapter 03, section 11](bible/03-key-management-and-identifier-lifecycle.md#as-of-anchor) and [chapter 07, section 11](bible/07-shibboleths-and-anti-patterns.md#retrograde-attack)

14. Multisig and delegation encode an organization's existing decision rules in its keys; they do not supply the rules. Every delegated event needs a seal in its delegator's log, so a validator checks each link of a delegation chain. Whether anything carries across a link, as the `DID` trait declares, is a stated property of the identifier, never an assumption. [chapter 03, section 8](bible/03-key-management-and-identifier-lifecycle.md#delegation)

15. Signing keys stay with their controller. A cloud agent may store, relay and coordinate without ever holding them, and a custodian acts through delegation to its own identifier. A design that gives an agent the controller's signing keys has given away control. [chapter 03, section 12](bible/03-key-management-and-identifier-lifecycle.md#keria-signify)

## Wire {#wire}

16. The wire format is the interop contract. A change that passes one implementation's tests but diverges from the specified encoding is a defect, because it silently breaks every other implementation. Because CESR is self-framing, a wrong size does not fail loudly; it mis-frames everything after it. [chapter 04, section 12](bible/04-cesr-and-the-wire.md#interop-risks)

17. Composability is the core invariant: any concatenation of primitives converts between text and binary in one step, with no separators or length prefixes, and splits back into the same primitives. The 24-bit alignment arithmetic exists to keep that true, and a simplification that breaks it is a regression however clean it looks. [chapter 04, section 3](bible/04-cesr-and-the-wire.md#composability)

18. Crypto agility is designed in. A new algorithm claims an unused code, and an identifier moves to it by rotating, one identifier at a time, so a new algorithm is an event in a log, not an infrastructure project. The cost falls on old receivers. Every code announces its own length, but only a variable-size code also carries its value's length; a new fixed-size code leaves an old parser unable to find the next primitive, so it breaks detectably rather than misreading. New parsers still accept old streams. [chapter 04, section 5](bible/04-cesr-and-the-wire.md#code-tables)

19. Complexity is load-bearing. Treat an unexplained check as protecting an invariant until shown otherwise, and do not simplify away a guard you do not understand. [chapter 07, section 12](bible/07-shibboleths-and-anti-patterns.md#verify-the-code)

## Data and disclosure {#data}

20. An ACDC is a node in a graph, not an envelope. Its content commits to itself by SAID and its edges are typed. Its issuance is anchored in the issuer's key event log, so it stays verifiable after the issuer rotates keys, which a credential carried only by a signature does not. [chapter 05, section 1](bible/05-acdc-and-verifiable-data.md#what-an-acdc-is)

21. Schemas are static. A schema may come from anywhere, because it is checked against its SAID; it is never resolved from an address whose content can change. [chapter 05, section 3](bible/05-acdc-and-verifiable-data.md#static-schema)

22. The ACDC specification states its goal as protection from the unpermissioned exploitation of data, not privacy for its own sake. Graduated and contractually protected disclosure are its mechanisms. KERI's authors treat cryptographic unlinkability as one tool with diminishing returns rather than the yardstick; a reviewer may contest that assessment, but must not measure ACDC against a goal it does not claim. [chapter 05, section 7](bible/05-acdc-and-verifiable-data.md#graduated-disclosure)

23. Correlation resistance and data loyalty are layered properties of ACDC and governance, not promises of KERI's core. Data loyalty is a fiduciary duty, imposed by contract or statute, that whoever holds a person's data act as that person's loyal agent. A critique that faults key management for correlation is attacking the wrong layer. [chapter 06, section 4](bible/06-governance-ecosystems-and-interop.md#layered-privacy)

24. Issuance is anchored in the issuer's log, so an issuer can always detect credentials issued in its name, and a compromised issuer cannot hide what it did. An issuee has no such way to detect misuse of its credentials, such as a thief presenting them. KERI's authors argue that issuee-side detection should be optional, because a compromised issuee's harm is local and rotating its keys already cuts the thief off. Presentation registries are the proposed mechanism for an issuee who opts in. [chapter 10, section 1](bible/10-presentation-registries.md#asymmetry)

## Governance and meaning {#governance}

25. Cryptography reaches authenticity, not veracity. KERI proves who said something and that it was not altered; whether it is true, and whether to rely on it, is a judgment a governance framework or a human makes. [chapter 06, section 1](bible/06-governance-ecosystems-and-interop.md#authenticity-veracity)

26. A signature proves that the controller's keys signed, which makes the controller accountable for it. It does not prove that the controller meant or authored the content; meaning comes from role, ceremony and policy. [chapter 07, section 9](bible/07-shibboleths-and-anti-patterns.md#signature-authorship)

27. An alias is a human claim about who stands behind an AID. The AID itself leaves no room for a man in the middle; the alias creates that room, because cryptography cannot check the mapping it asserts. So logic keys on the AID, and an alias is treated as unverified until something establishes the mapping. [chapter 07, section 9](bible/07-shibboleths-and-anti-patterns.md#aliases)

## Evidence discipline {#evidence-discipline}

28. Tiers are never upgraded for convenience. A discussion is not a specification, a forward branch is not the standard, an implementation is evidence about the implementation, and a vendor's practice is evidence about that vendor. The newest and most contested material in the bible (presentation, request authentication, presentation registries) is exactly where this rule matters most; read those chapters at review time and check their dates. [chapter 08, status](bible/08-presentation-architectures-and-ipex.md#status)

29. When the specification and the reference implementation disagree, neither silently wins. The specification governs what conformance requires; the code governs what deployed software actually does; and the disagreement itself is a finding, a bug in one or a gap in the other, to be reported rather than resolved by assumption. Prose describing either, including a code comment describing the specification, is checked against what it describes before it is believed. [chapter 07, section 12](bible/07-shibboleths-and-anti-patterns.md#verify-the-code)

30. The corpus states its own residuals, and a reviewer may press them. The no-trusted-third-party maxim is knowingly relaxed for issuee-side protection. A review by AI personas configured with this file is a structured self-attack, not independent validation. [chapter 07, section 14](bible/07-shibboleths-and-anti-patterns.md#residuals)

## Shibboleths {#shibboleths}

Each row is a framing whose shape encodes a prior KERI rejects. Hear the reflex fire and catch it before it reaches the page. The full treatment is in chapter 07.

| The tell | The reframing | Where |
|---|---|---|
| Who vouches for the identifier? | Nobody; the log is the root of trust. | [07, 2.1](bible/07-shibboleths-and-anti-patterns.md#trusted-authority) |
| Renew or re-issue the certificate. | Rotate; identity persists across keys. | [07, 2.3](bible/07-shibboleths-and-anti-patterns.md#renewal) |
| Pin the key. | Pin the AID. | [07, 2.4](bible/07-shibboleths-and-anti-patterns.md#pinning) |
| Where is the CRL or OCSP responder? | Status is anchored state, verified without a callback. | [07, 3.1](bible/07-shibboleths-and-anti-patterns.md#crl-ocsp) |
| Consult a status endpoint at verification time. | A runtime callback is a phone-home in disguise. | [07, 3.2](bible/07-shibboleths-and-anti-patterns.md#status-endpoint) |
| Certificate Transparency already solved this. | CT redistributes administrative trust; KERI removes it. | [07, 3.3](bible/07-shibboleths-and-anti-patterns.md#certificate-transparency) |
| You need a ledger or global consensus. | Per-identifier order suffices. | [07, 4.1](bible/07-shibboleths-and-anti-patterns.md#global-consensus) |
| How do you honor the right to be forgotten? | Only a shared ledger cannot forget. | [07, 4.4](bible/07-shibboleths-and-anti-patterns.md#right-to-be-forgotten) |
| Use a bearer token or session. | Prove control freshly; a bearer credential is replayable. | [07, 5.2](bible/07-shibboleths-and-anti-patterns.md#bearer-tokens) |
| The cloud holds and uses my keys. | Sign at the edge. | [07, 5.3](bible/07-shibboleths-and-anti-patterns.md#custodial-cloud) |
| Federation decentralizes. | Federation moves centralization; self-certification removes it. | [07, 5.4](bible/07-shibboleths-and-anti-patterns.md#federation) |
| Secure the pipe and the data is safe. | Secure the data; pipes have joints. | [07, 5.5](bible/07-shibboleths-and-anti-patterns.md#secure-pipe) |
| A credential is a signed envelope. | An ACDC is anchored to key state, not to the moment of signing. | [07, 6.1](bible/07-shibboleths-and-anti-patterns.md#signed-envelope) |
| DIDs already solved this. | Not for issuer rotation or historical key state. | [07, 6.2](bible/07-shibboleths-and-anti-patterns.md#dids-solved-it) |
| Canonicalize the JSON. | Commit to exact bytes with a SAID. | [07, 6.4](bible/07-shibboleths-and-anti-patterns.md#json-canonicalization) |
| A secure system prevents forks. | A survivable one makes them evident and recoverable. | [07, 7.1](bible/07-shibboleths-and-anti-patterns.md#preventing-forks) |
| A witness threshold gives global safety. | It gives durability of the controller's view. | [07, 7.4](bible/07-shibboleths-and-anti-patterns.md#witness-threshold) |
| A witness is a notary or validator. | A witness stores and serves; it asserts nothing. | [07, 8.1](bible/07-shibboleths-and-anti-patterns.md#witness-not-ca) |
| A watcher can distrust an identifier. | A watcher reports; the relying party decides. | [07, 8.2](bible/07-shibboleths-and-anti-patterns.md#watcher-enforcement) |
| The delegator vouches for every delegatee. | Each delegation is checked, not inherited. | [07, 8.4](bible/07-shibboleths-and-anti-patterns.md#did-trait) |
| Verification proves the claim is true. | It proves authenticity, not veracity. | [07, 9.2](bible/07-shibboleths-and-anti-patterns.md#authenticity-veracity) |
| Automate the final trust decision. | Mechanize verification; leave reliance to judgment. | [07, 9.3](bible/07-shibboleths-and-anti-patterns.md#automated-trust) |
| A compact credential is private. | Compact is not blinded. | [07, 10.2](bible/07-shibboleths-and-anti-patterns.md#compact-not-private) |
| Dereference the schema to validate. | Schemas are static and verified by SAID. | [07, 10.3](bible/07-shibboleths-and-anti-patterns.md#schema-dereference) |
| Bundle every claim, then selectively disclose. | Issue small credentials and disclose by graduation. | [07, 10.1](bible/07-shibboleths-and-anti-patterns.md#bundled-credentials) |

## Evidence standard {#evidence-standard}

No finding may rest only on a generic best practice or an analogy from PKI, IAM, consensus or zero-knowledge work. An analogy is a hypothesis, not a finding. Every finding must do three things.

1. Cite ground truth: a specification section, a paper section, the security analysis, or a line in the reference code. When the claim is about what software does, read the code.
2. State its objective function (survivability or invulnerability) and the layer it faults (KERI's core, ACDC disclosure, governance, or deployment).
3. Say which kind of weakness it is: a deliberate non-goal, a limit on what a proof covers, or a gap in deployment or ecosystem maturity. Only the third kind is a defect in KERI as designed, and the first two are findings only if KERI's own text claims otherwise.

Do not swing the other way and treat every KERI reframing as unassailable. A finding lands when it targets a real seam: a guard that does not fail closed; a wire format not honored byte for byte across implementations; layers that do not compose as claimed; an assumption silently granted; a simplification that desynchronizes parsers; a check that goes permissive on an unfamiliar code. Press those hard.

Before emitting a finding, ask whether a KERI core contributor would recognize it as reasoning in KERI's terms or dismiss it as an imported prior. If the latter, cut it or reframe it.

## Lens routing {#lens-routing}

Each reviewer lens reads the chapters that give its concerns depth.

- Security — chapter 02 and [chapter 03, sections 5, 10 and 11](bible/03-key-management-and-identifier-lifecycle.md#pre-rotation).
- Relation algebra — [chapter 05, section 5](bible/05-acdc-and-verifiable-data.md#edges) and chapter 08's edges and DAG sections.
- Privacy — [chapter 06, section 4](bible/06-governance-ecosystems-and-interop.md#layered-privacy) and chapter 05's disclosure and registry sections.
- Specification precision — chapter 04 throughout and [chapter 01, section 8](bible/01-foundations-and-worldview.md#load-bearing-assumptions).
- First-principles skepticism — [chapter 02, section 11](bible/02-security-model-and-threat-posture.md#dg-bindings), [chapter 01, sections 6 to 8](bible/01-foundations-and-worldview.md#pki-problem) and [chapter 07, section 14](bible/07-shibboleths-and-anti-patterns.md#residuals).
- Governance and interoperability — chapter 06 throughout.
- CESR and wire format — chapter 04 end to end.
- Every lens reviewing presentation, request authentication or registries — chapters 08, 09 and 10, read at review time, with the tier rule (28) in force.
