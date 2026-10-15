# 07 — Security Analysis: Survivability, Threat Model, and the Del Giudice Claim Bindings

Raw doctrine-mining notes. **Sources:** `/home/daniel/code/wot/keri-security-analysis/` (path corrected 2026-10-14; this line previously named `/home/daniel/code/keri-security-analysis/`, the pre-reorg location; pin 149fa6c35, the repo's only commit; second pass in §13) — primarily `cr-ad-trust.md` (Cryptographic vs. Administrative Trust paper), `standard-analysis.md` (the analysis-method template), `background.md` (canonical background, "already digested" — used here only to anchor section/assumption/property numbers and exact quotes), and the six per-claim analyses `dg-c01-claude.md` … `dg-c06-claude.md`. Citations give file + section heading (or § / line). Quotes are ≤25 words, verbatim.

---

## 1. What KERI/ACDC/CESR fundamentally IS and IS NOT (worldview, root of trust)

### The core problem KERI addresses
- The internet has **no native identity layer**; it "addresses endpoints, not the people or organizations that control them." (`cr-ad-trust.md` §1). PKI was built to fill this void via centralized CAs.
- **The core flaw of PKI is the separation of identifier from key.** In X.509 an identifier "is a record in a database. The key is a separate artifact. The binding between them is an assertion" — a cert signed by a third party. "This places the root of trust outside the identity itself." (`cr-ad-trust.md` §1).
- KERI's foundational move: **make the identifier self-certifying.** A controller "derives their identifier mathematically from their initial public key." The result is an **Autonomic Identifier (AID)**: "an identifier whose authenticity can be verified without any external authority." (`cr-ad-trust.md` §4).

### The defining contrast — administrative vs. cryptographic root of trust
- "Where they diverge is not in mechanism but in the *root of trust*." CT/PKI "bottoms out in administrators… KERI's bottoms out in mathematics." (`cr-ad-trust.md` §3).
- The KEL "validity can be checked by anyone who replays its hash chain, without querying any authority." (`cr-ad-trust.md` §3).
- **The head of the log IS the current state.** "To check the current state of an AID, a verifier doesn't query a directory. They obtain the KEL and replay it. The head of the log *is* the current state, and anyone can verify it offline, at any time." (`cr-ad-trust.md` §4).

### High-level security objective (what KERI is FOR)
Per identifier (`background.md` §1.2 "Security Objective"):
- Enable third parties to verify **which keys are currently authoritative**;
- Make equivocation (duplicity) **detectable**;
- Provide **recovery** mechanisms following key compromise;
- Preserve verifiability **even when the controller is offline**.
- Pursued "via *event chaining*, *pre-rotation commitments*, and *witnessed agreement*, rather than via global ordering or consensus." (`background.md` §1.2).

### Identity vs. dynamic privilege (anti-expiration doctrine)
- X.509 bakes in a mandatory Validity field (NotBefore/NotAfter): "Evidence of identity expires by design, not by necessity." (`cr-ad-trust.md` §1).
- **Identity means sameness.** "It means *sameness*: the thing that holds constant across contexts. An organization incorporated in 1975 doesn't renew its identity every ninety days." (`cr-ad-trust.md` §1).
- Dynamic privilege tokens (business license, domain registration) *should* expire; **identity should not.** Forcing identity evidence to churn on a schedule creates "a structural incentive to *defer* revocation when a key is actually compromised" — "the organizations most in need of urgent revocation are the ones most likely to wait." (`cr-ad-trust.md` §1).

---

## 2. Security & threat-model positions (the doctrinal core)

### 2.1 Survivability, NOT invulnerability
This is the single most load-bearing frame in the corpus. The analysis method *requires* every analyst to first declare which objective function a claim assumes (`standard-analysis.md` §0 "Objective-Function Alignment"):
- **Invulnerability-oriented framing** "assumes that security requires prevention of entire classes of attack (e.g., forks, equivocation, conflicting histories) via mechanisms such as global ordering or consensus." (`standard-analysis.md` §0).
- **Survivability-oriented framing** "does value prevention" but "assumes that some adversarial behaviors are inevitable and evaluates security in terms of a gestalt… invulnerability, detectability, evidence preservation, recoverability, and mission-level continuity under disturbance." (`standard-analysis.md` §0).
- **"KERI, as specified, adopts a survivability-oriented security model."** (`standard-analysis.md` §0).
- Doctrinal source: "KERI is explicitly **not** designed around invulnerability. Its security posture is more accurately understood through the lens of **mission survivability**." (`background.md` §4.5.1). It is "a framework common in military and safety-critical systems engineering."
- Survivable-secure system properties (`background.md` §4.5.1): continue functioning during/after adversarial disturbance; make hostile actions observable and attributable; preserve evidence enabling recovery/containment/governance; **"Avoid abortive mission failure even when attacks succeed."**
- Reframing rule: "Forks and equivocation by malicious controllers are *anticipated disturbances*, not protocol failures." (`background.md` §4.5.1).
- **Category-error warning (the outsider tell):** "Failure to align the evaluator's objective function with KERI's stated survivability-oriented goals risks category errors that systematically mischaracterize KERI's security properties." (`background.md` §4.5.1). Analogy from the analyses: criticizing KERI for not preventing malicious-controller duplicity "is analogous to criticizing a smoke detector for not preventing fires." (`dg-c02-claude.md` §5).

### 2.2 Detection, NOT prevention
- "**Prevention**: making an attack impossible / **Detection**: making an attack observable." (`background.md` §4.5).
- "KERI is fundamentally a **detection-oriented system** with optional response mechanisms." (`background.md` §4.5).
- "Any claim that implies *prevention* must be scrutinized for hidden assumptions." (`background.md` §4.5).
- Both CT and KERI are "fundamentally **detection-oriented**. Neither prevents a bad actor." (`cr-ad-trust.md` §3). Rationale: "guaranteeing prevention requires global consensus at a cost in latency and scalability that both systems deliberately decline to pay." (`cr-ad-trust.md` §3).

### 2.3 Duplicity-EVIDENT, not duplicity-RESISTANT
- KERI's posture "is best described as *duplicity-evident* rather than *duplicity-resistant*. It doesn't try to make duplicity impossible… It makes duplicity *provable and attributable*." (`cr-ad-trust.md` §4).
- The Del Giudice-sourced verbatim: **"KERI is therefore not duplicity-resistant but only duplicity-evident."** (thesis Ch.4 §4.1 p.38, quoted in `background.md` §8.2 DG-C03 and `dg-c03-claude.md`).
- **Interpretation caveat / terminological trap:** whether this is a *criticism* depends entirely on reading of "resistant." If "resistant"=prevention, the statement is accurate/faithful; if "resistant"=detection+response (survivability), the phrasing *understates* KERI's model. The word "only" subtly imports an invulnerability bias. (`dg-c03-claude.md` §2, §5).
- Duplicity definition context: duplicity = a controller signing two conflicting events at the same sequence number (`cr-ad-trust.md` §4; `background.md` §4.1). Distinguish **duplicity** (conflicting-but-valid) from **invalidity** (`background.md` §4.1.2).

### 2.4 Zero-trust / malicious-controller stance
- "Verifiers do **not** assume controller honesty." (`background.md` §2.1 Controller, Trust assumptions). Controllers "May be honest or malicious (analysis distinguishes both cases)."
- Explicit non-goal: **"Protection against a fully malicious controller."** (`background.md` §1.3 Explicit Non-Goals).
- "KERI doesn't provide any native way of protecting validators from duplicity…" (thesis Ch.4 §4.1 p.38, in `background.md` §8.2 DG-C02).
- When controller is malicious (`background.md` §5.8): controller may produce multiple conflicting KELs; **each may independently achieve sufficient agreement**; "Witness thresholding alone does not prevent this." Security "shifts from **consistency** to **detectability**."
- A malicious controller "can simply run its own witnesses" (thesis Ch.3 §3.1.4 p.26, in `background.md` §8.2 DG-C02) — i.e. witness thresholds don't bind an attacker who controls the witnesses.
- Key insight from DG-C06 analysis: **the "honest controller" assumption is a proof-technique simplification, NOT a KERI deployment requirement.** "Removing it does not break KERI's security—it shifts the focus from prevention to detection and recovery." (`dg-c06-claude.md` §3). Malicious behavior "does not 'break' KERI; it triggers detection mechanisms." (`dg-c06-claude.md` §5).

### 2.5 Local / observer-dependent validity (no global convergence)
Convergence disambiguation (`background.md` §7.4):
- **Local Consistency** — "Its accepted KERL is internally consistent / No conflicts observed within its view." "Local consistency is always achievable." (§7.4.1).
- **Global Convergence** — "All validators accept the same KERL for an identifier." **"KERI does not guarantee global convergence."** (§7.4.2).
- **Eventual Awareness** — "Conflicts become observable to some validators over time." "This is possible, not guaranteed." (§7.4.3).
- **Permanent Divergence** — "Validators accept different KERLs indefinitely." **"Permanent divergence is an allowed outcome."** (§7.4.4).
- Safety reframed (`background.md` §7.5.1): "Safety in KERI means: Validators do not accept *invalid* histories." Safety does **not** mean validators agree on a single history.
- Liveness reframed (`background.md` §7.5.2): "Liveness in KERI means: Honest controllers can continue to append events." It does **not** mean prompt observation or conflict resolution.
- Validators are autonomous: "Validators do not share state by default," "May have disjoint trust relationships," "May never interact directly." (`background.md` §7.1, quoted in `dg-c03-claude.md` §2).
- KAWA consistency is **local to the witness set**, not global across validators — a reader might wrongly assume it "extends globally across all validators." (`dg-c01-claude.md` §4).

### 2.6 Pre-rotation firewall
- "**Pre-rotation** is KERI's most important security innovation." When creating any event the controller includes the current key's public value but for the next key "only a cryptographic hash of its public key. The next key itself stays offline, in cold storage." (`cr-ad-trust.md` §4).
- **The firewall property:** "An attacker who steals the current key can sign events, but cannot rotate to take permanent control: they don't know the next key's value, only its hash." (`cr-ad-trust.md` §4). Compromise of current keys is **survivable** (`background.md` §3.4).
- Vault metaphor: "like a sealed succession document held in a vault… If the reigning key is stolen, the attacker can act in the present, but cannot seize the future." (`cr-ad-trust.md` §4).
- Recovery loop: on detecting compromise via one's own watcher, the controller executes "a recovery rotation using the pre-committed key, issue a new pre-rotation commitment… and keep going. The identifier persists. The history persists." (`cr-ad-trust.md` §4).
- Pre-rotation validity (P1) "Relies on unforgeability of signatures and secrecy of pre-rotation keys." (`background.md` §5.6 P1).

### 2.7 Post-quantum posture (architectural, not migratory)
- Hashes resist quantum far better than signatures: "Grover's algorithm provides only a quadratic speedup against hashes, not the exponential speedup Shor's algorithm provides against RSA and ECC." (`cr-ad-trust.md` §3).
- A 256-bit hash "retains roughly 128 bits of post-quantum security, well beyond any feasible attack." (`cr-ad-trust.md` §4).
- A quantum adversary breaking the current signing key "gains the ability to forge interaction events — but not to rotate, because the pre-rotation commitment is protected by a hash." (`cr-ad-trust.md` §4).
- Crypto-agility: "When signing algorithms need upgrading, KERI controllers can do so without changing their identifier, without re-issuing credentials… The upgrade is an event in the KEL. Not a global infrastructure project." (`cr-ad-trust.md` §6).
- "KERI has nothing to unwind. There is no installed base of classically-keyed infrastructure that must migrate before the system can be trusted." (`cr-ad-trust.md` §6).

### 2.8 Guarantees stated RELATIVE to explicit assumptions
Doctrinal insistence: "Security properties must be stated **relative to assumptions**." (`background.md` §4.7). "Agreement thresholds do not imply global safety." Each KAWA property is bound to a dependency list and scope (see §4 below). "Failure to state these boundaries results in overstated guarantees." (`background.md` §5.10).

---

## 3. The Assumption Catalog (A1–A13)

Each assumption is the axis along which a KERI security claim is conditional. Verbatim/near-verbatim from `background.md` §4.6, §5.3, §6.4, §7.4.5/7.6.

| ID | Name | Statement | Source |
|---|---|---|---|
| **A1** | Cryptographic Soundness | "Hash functions and signature schemes are secure." | §4.6 |
| **A2** | Bounded Witness Faults | "At most `f` witnesses behave arbitrarily for a given identifier." | §4.6 |
| **A3** | Honest Controller (Conditional) | "The controller follows the protocol except where explicitly stated." Note: "Many analyses, including Del Giudice's KAWA analysis, implicitly rely on A3." | §4.6 |
| **A4** | Witness Non-Equivocation | "Correct witnesses do not sign conflicting events for the same sequence number, except as explicitly allowed by recovery rotation rules." | §4.6 / §5.4 |
| **A5** | Observer Presence | "At least some validators employ watchers that compare histories across sources." **Qualification: "A5 is optional in practice and MUST NOT be silently assumed."** | §4.6 |
| **A6** | Network Liveness | "Messages between honest parties are eventually delivered." | §4.6 |
| **A7** | Threshold Discipline | "Controllers configure `M` such that `M > f`, where `f` is the maximum number of faulty witnesses tolerated." (M = toad; common but not required: N=3f+1, M=2f+1) | §5.3 |
| **A8** | Observer Coverage | "At least some observers monitor identifiers of interest." | §6.4 |
| **A9** | Observer Diligence | "Observers actively fetch, compare, and update KERLs." | §6.4 |
| **A10** | Information Flow | "Observers obtain KERLs from sufficiently diverse sources." | §6.4 |
| **A11** | Evidence Integrity | "Observers preserve and share evidence accurately." | §6.4 |
| **A12** | Validator Diversity | "Validators may observe different subsets of the network and data sources." | §7.x (line 905) |
| **A13** | Policy Variance | "Validators may apply incompatible fork-handling policies." | §7.6 |

**Critical note on A8–A11:** "None of A8–A11 are enforced by KERI." (`background.md` §6.4). Observer assumptions are *optional deployment properties*, never protocol guarantees.

---

## 4. KAWA — KERI's Algorithm for Witness Agreement (properties P1–P4, non-properties P5–P8)

- KAWA is "a single-phase agreement protocol that provides fault tolerance without the multi-phase commit overhead of classical Byzantine Fault Tolerant algorithms like PBFT." (`cr-ad-trust.md` §4). Contrast: KERI provides availability without a blockchain.
- Thresholds: `N`=total witnesses, `M`=receipt threshold (**toad**). Common-but-not-required: N=3f+1, M=2f+1. KERI is *less prescriptive* than BFT — a controller may set M=N, simple majority, or even M=1 (`dg-c01-claude.md` §2). Treating BFT thresholds as mandatory overstates KERI's constraint.

**Provided properties (all scoped to HONEST controller unless noted):** (`background.md` §5.6)
- **P1 — Validity (Event Authenticity):** "If a correct witness accepts an establishment event, that event was authorized by the controller." Depends A1, A3, A4.
- **P2 — Consistency (No Forks Under Honest Control):** "Two correct witnesses will not accept different establishment events at the same sequence number." Depends A2, A3, A4, A7. **"This is the strongest KAWA property and is *conditional*. It does not hold if the controller is malicious."**
- **P3 — Durability (Immutability After Agreement):** "Once an event has a sufficient agreement, it cannot be removed or replaced." Depends A2, A4, A6. "Durability is local to witnesses and does not imply global convergence."
- **P4 — Availability:** "Validators can retrieve the KERL even if the controller is offline." Depends A2, A6. "Availability degrades with witness churn or witness set mismanagement."

**Explicitly NOT provided by KAWA** (`background.md` §5.7):
- **P5 — Fork Prevention for Malicious Controllers**
- **P6 — Global Consistency Across Validators**
- **P7 — Timely Fork Detection**
- **P8 — Automatic Fork Resolution**
- "Any claim implying these properties must introduce **additional mechanisms** (e.g., observers, governance, social response)."

**KAWA↔observer division of labor:** "KAWA alone determines *local durability*. Observers determine *global detectability*." (`background.md` §5.9). Without observers, KAWA guarantees degrade to: "Each validator sees *a* consistent history." (`background.md` §5.9).

**Formal-analysis three properties** (as stated in `cr-ad-trust.md` §4, from Del Giudice): *validity* (accepted events genuinely authorized), *consistency* (no two correct witnesses accept conflicting events at same sequence number), *reliability* (controller can progress while witness faults stay below threshold).

---

## 5. Observer layer — Watchers, Jurors, Judges (roles + what they do/don't provide)

Roles (`background.md` §6.2):
- **Watcher:** "monitors identifiers by: Collecting KERLs from multiple sources / Comparing observed histories / Detecting conflicts at identical sequence numbers." Validator-selected; "No required coverage or completeness / No protocol-mandated response."
- **Juror:** "records evidence of duplicity, including: Conflicting events / Witness receipts / Proofs of equivocation." "No authority to resolve conflicts / Enables post hoc accountability."
- **Judge:** "applies policy or governance rules to: Rank conflicting KERLs / Recommend acceptance or rejection / Trigger recovery or remediation." "Policy-driven / Non-universal / May disagree across validators."
- The three roles map onto **detection, evidence-preservation, and policy-adjudication** respectively — deliberately separated so no single observer both detects AND rules.

**Ambient Duplicity Detection:** "the emergent property that equivocation becomes observable *somewhere* in the network, given sufficient observer activity and information flow. This is **not** guaranteed by protocol mechanics." Depends on observer presence, diligence, information overlap, and time. (`background.md` §6.3).

Observer-enabled conditional properties (`background.md` §6.5): **O1** Duplicity Detection (depends A8,A9,A10; "may be delayed or incomplete"); **O2** Evidence-Based Accountability ("Observed duplicity can be proven to third parties"; depends A1,A11; "Proof does not imply remediation"); **O3** Validator-Informed Choice ("Choices may diverge permanently").

**What observers do NOT provide** (`background.md` §6.6): "Global convergence / Guaranteed detection / Timely detection / Automatic resolution / Enforcement against controllers or witnesses." **"Observers increase *visibility*, not *control*."**

Watcher detection mechanic (`cr-ad-trust.md` §4): if a watcher "asks two witnesses for the head of the same identifier and gets different hash values, it has detected *duplicity*… The watcher can broadcast both events as cryptographic proof of fraud. That proof doesn't require trusting any authority's interpretation — only the mathematics of the signatures."

---

## 6. Precise terminology / definitions

- **AID (Autonomic Identifier):** self-addressing identifier "derived from the inception event of a Key Event Log." Cryptographically bound to its inception event; "Immutable once established"; may be transferable or non-transferable; "the anchor for all subsequent event verification." (`background.md` §2.2). Verifiable "without any external authority." (`cr-ad-trust.md` §4).
- **KEL (Key Event Log):** "an append-only chain of signed events, each linked by hash to its predecessor." Three event types: **inception** (creation), **rotation** (updating controlling keys), **interaction** (anchoring data without changing keys). (`cr-ad-trust.md` §4; `background.md` §3.2).
- **Establishment vs Non-Establishment events:** establishment = inception + rotation (change key state); non-establishment = interaction (anchor only). (`background.md` §3.4). Recovery rotation is the special interaction-then-conflicting-rotation case.
- **KERL (Key Event Receipt Log):** the KEL plus witness receipts; what witnesses "Store and retransmit." (`background.md` §2.3, §3.3).
- **SAID:** self-addressing identifier (hash-based content commitment) — the hash-chaining/pre-rotation primitive underlying AID derivation (implied throughout; pre-rotation "hides the next controlling key behind a hash," `cr-ad-trust.md` §3).
- **Witness / backer:** "a server the controller designates to store and serve the KEL." Returns a signed receipt on validating an event; once a **threshold (toad)** of receipts is collected, "the event is stable." **"Witnesses make no assertion about identity… That is a fundamentally different role than a CA."** (`cr-ad-trust.md` §4). Normative constraint: witnesses appearing as backers in the `b` list **MUST be non-transferable** (the fully-qualified public key itself), so validators verify receipts directly from the witness AID with no witness KEL needed. Treating this as a discretionary simplification is "a characterization error *about KERI-as-specified*." (`background.md` §2.3).
- **toad (M):** the witness receipt threshold. (`background.md` §5.3).
- **Watcher / Juror / Judge:** see §5 above.
- **Duplicity:** controller signing two conflicting events at the same sequence number (`background.md` §4.1; `cr-ad-trust.md` §4).
- **Recovery rotation:** a witness signs a non-establishment event then later a conflicting establishment (rotation) event at the same seq no., under narrow conditions (no intervening establishment events; conforms to pre-rotation commitments). Purpose: "Enable recovery after compromise of current keys." (`background.md` §5.5).
- **KAWA:** KERI's Algorithm for Witness Agreement — single-phase, non-PBFT witness-agreement protocol (§4 above).
- (Cross-ref: EGF/IPEX/edge-operators are NOT covered by these sources — see Gaps.)

---

## 7. Recovery rotation — the deliberate formal-elegance tradeoff (DG-C04)

- Mechanics (faithful to spec): under recovery rotation "correct witnesses may sign both an attacker's fraudulent event and the legitimate owner's recovery event — because KERI prioritizes the ability to reclaim a compromised identity over strict uniqueness of history at every moment." (`cr-ad-trust.md` §5).
- Consequence: "validators may see multiple mathematically valid KELs for the same identifier, and no cryptographic mechanism alone can determine which is legitimate." (`cr-ad-trust.md` §5). Thesis verbatim: "This allows for 'forked' KERLs where both… forks are fully verifiable…" (Ch.3 §3.2.2 p.28).
- **The tradeoff stated:** "the alternative would be an identity you cannot recover from compromise without involving a trusted third party — which brings back exactly the administrative dependency KERI was designed to escape." (`cr-ad-trust.md` §5). "buys real-world recoverability at the cost of formal elegance in edge cases."
- It "narrows the strength of DG-C01" (weakens strict non-equivocation) — a "limitation on **provability of uniqueness**, not on validity." (`background.md` §8.2 DG-C04).
- Analyst framing (`dg-c04-claude.md` §5.1): treating "inability to prove uniqueness" as insecurity is a **category error** — "KERI's security model is **evidence-based** rather than **proof-based**." Validators make "risk-informed judgments," not defer to proofs. Formal uniqueness is unprovable, but "**duplicity remains detectable**."

---

## 8. Del Giudice claim bindings DG-C01…DG-C06 — what KERI DOES and does NOT guarantee

Source: 2025 ETH Zurich Master's thesis *A Security Analysis of KERI* (Del Giudice) — "the most rigorous formal analysis of KERI's consensus mechanics," but "not peer-reviewed research." (`cr-ad-trust.md` §5). Normalized claims + verbatim excerpts from `background.md` §8.2; per-claim verdicts from `dg-c0X-claude.md`.

- **DG-C01 — KAWA provides fork-resistance for honest controllers (under strong assumptions).** Normalized: KAWA gives validity, consistency, reliability for *honest controllers* during establishment events, under BFT-style quorum sizing + bounded faults. Assumptions: A1,A2,A3,A4,A7. Verdict: **faithful within scope; a positive (not critical) claim.** Risk: casual reader may (a) over-generalize to all deployments, (b) under-appreciate the detection layer, (c) assume BFT thresholds are mandatory. (`dg-c01-claude.md`). Thesis verbatim: "Consistency: If two correct witnesses accept two events… with same ID, then ε = ε′." (Ch.3 §3.1.5 p.27).
- **DG-C02 — KERI does not prevent duplicity by malicious controllers.** Normalized: no native prevention; at best detectable via evidence propagation; neither prevention nor timely detection guaranteed. Verdict: **faithful to mechanics but misaligned with KERI's objectives** — "criticizes KERI for lacking a capability… that is **explicitly outside KERI's design goals**." Category error: non-goal treated as failure. Makes KERI "appear **less secure than it is**." Residual *legitimate* criticism (survives realignment): detection is delegated to an *optional* observer layer — "a critique of *deployment readiness and ecosystem maturity*, not of KERI's protocol design." (`dg-c02-claude.md` §2, §5, §6). Verbatim: "We don't have any guarantees however on if and when this duplicity will be exposed." (Ch.4 §4.1 p.38).
- **DG-C03 — Validators may accept conflicting KERLs indefinitely.** Normalized: different validators may accept different valid KERLs; divergence may persist indefinitely with no protocol resolution → "not duplicity-resistant but only duplicity-evident." Assumptions: A12, A13. Verdict: **descriptive portion faithful** (permanent divergence is a *permitted outcome*, §7.4.4); the evaluative "only" risks importing invulnerability expectation. **"No criticism survives objective-function alignment"** when KERI is evaluated as survivability-oriented. Note: divergence is a *protocol-level property*, not merely a deployment artifact — "permitted *even with observers present*." (`dg-c03-claude.md` §2, §3, §6). Verbatim: "Two disjoint parts of the network… could be using two different versions of a KERL…" (Ch.4 §4.1 p.38).
- **DG-C04 — Recovery rotation blocks proof of a single authoritative KERL.** (See §7.) Assumptions: "None beyond the base model" — the fork occurs *even when all actors behave correctly*. Verdict: technically correct; category error to equate unprovability with insecurity; "affects formal verification more than operational security." (`dg-c04-claude.md`). Verbatim: "prevents us from proving stronger properties that only allow for one version…" (Ch.3 §3.2.2 p.28).
- **DG-C05 — Practical mitigation requires governance and monitoring.** Normalized: effective mitigation "likely requires governance, monitoring, or centralized archival services (e.g., a 'super watcher'), which introduce additional trust assumptions." Assumptions: A8–A11. Verdict: **faithful and survivability-aligned** — "not a failure of KERI's design but an acknowledgment that survivability properties emerge from **system composition** (protocol + observers + governance), not protocol alone." Caveat: "additional trust assumptions" is better read as *operational dependencies + incentive/coverage assumptions*, except the super-watcher case which IS genuine trust centralization. (`dg-c05-claude.md` §2, §5, §6). Verbatim: "it requires a centralized component that needs to be trusted…" (Ch.4 p.39).
- **DG-C06 — Strong security results depend on narrow scope + strong assumptions.** Normalized: strongest proofs hold only for honest controllers, bounded witness faults, reliable communication, uncompromised pre-committed rotation keys; malicious-controller behavior breaks termination/liveness. Verdict: **faithful as a statement about the PROOFS' scope**, but misleading if read as "KERI requires honest controllers." Key correction: observer mechanisms are "explicitly excluded from Del Giudice's formal analysis" (`background.md` §8.3) yet "central to KERI's security model." Malicious controllers "trigger detection, not failure." Honest-controller = "a **proof technique assumption**… not a KERI deployment assumption." (`dg-c06-claude.md` §3, §4, §5).

**Meta-pattern across DG analyses:** every apparent "weakness" resolves to one of: (a) a *deliberate non-goal* (DG-C02, DG-C03), (b) a *proof-scope limitation* not a protocol limitation (DG-C01, DG-C06), or (c) a *deployment/ecosystem-maturity* gap not a design flaw (DG-C05, and the residual of DG-C02). The genuinely surviving residuals are all about **observer/watcher infrastructure immaturity**, never about the protocol.

---

## 9. Anti-patterns / outsider tells / misconceptions the material corrects (GOLD)

These are the priors from PKI/IAM/blockchain that the corpus explicitly reframes.

1. **"Root of trust must be an authority (CA/administrator)."** → KERI's root is mathematics: a self-certifying AID replayable offline, "without querying any authority." Witnesses "make no assertion about identity… a fundamentally different role than a CA." (`cr-ad-trust.md` §3–§4).
2. **"Identity credentials should expire like everything else."** → Conflates identity (sameness, permanent) with dynamic privilege (contingent, should expire). Mandatory X.509 Validity is "evidence [that] expires by design, not by necessity" and creates a perverse incentive to defer revocation. (`cr-ad-trust.md` §1).
3. **"Revocation = CRL/OCSP lists."** → KERI has *no separate revocation layer*; key state lives in the KEL, "continuously current." OCSP "fail[s] open" — "most vulnerable precisely when it is most needed." (`cr-ad-trust.md` §2, table §3).
4. **"Transparency logs / CT already solve this."** → CT is "detection, not prevention" with an MMD latency window and a privacy price on gossip; and it "redistributes administrative trust rather than eliminating it" (log operators + browser root programs + CA/Browser Forum). "The result is not a decentralized trust hierarchy. It is a more elaborate one." (`cr-ad-trust.md` §2).
5. **"Security = invulnerability / prevent all forks."** → Category error. KERI is survivability-oriented; forks by malicious controllers are "*anticipated disturbances*, not protocol failures." Criticizing lack of prevention = "criticizing a smoke detector for not preventing fires." (`background.md` §4.5.1; `dg-c02-claude.md` §5).
6. **"You need blockchain / global consensus / global total ordering."** → Explicit non-goal: "Global total ordering of events across identifiers." (`background.md` §1.3). Global consensus is "a cost in latency and scalability that both systems deliberately decline to pay." (`cr-ad-trust.md` §3). Blockchain-background readers "may interpret 'not duplicity-resistant' as a criticism… Misunderstanding KERI as 'weaker than a blockchain' when it solves a different problem." (`dg-c03-claude.md` §6).
7. **"All validators converge on one truth (finality)."** → No. Permanent divergence is *allowed*; safety ≠ agreement on a single history; validators are autonomous and "may never interact directly." (`background.md` §7.4, §7.5, §7.1).
8. **"A threshold of witnesses = global safety."** → "Agreement thresholds do not imply global safety." (`background.md` §4.7). KAWA gives *local* durability; global detectability needs observers.
9. **"If a formal proof assumes an honest controller, the system is insecure against dishonest ones."** → The honest-controller premise is a *proof simplification*, not a deployment requirement; dishonesty triggers detection, not failure. (`dg-c06-claude.md` §3, §5).
10. **"Unprovable uniqueness = broken."** → KERI is evidence-based, not proof-based; recovery rotation deliberately trades provable uniqueness for real-world recoverability without a trusted third party. (`dg-c04-claude.md`; `cr-ad-trust.md` §5).
11. **"Detection is inferior to prevention."** → Equivocation between detectability and impossibility; "'at best, duplicity may become detectable' treats detectability as inferior to prevention without arguing *why* prevention is required given KERI's threat model." (`dg-c02-claude.md` §5).
12. **Method-level tell:** the standard-analysis template *forces* the analyst to name the objective function first and restate the claim verbatim, precisely because outsider critiques smuggle in unstated invulnerability goals. (`standard-analysis.md` §0; header comment: "you MUST restate the claim verbatim… If you cannot do so, stop and ask.").

---

## 10. Invariants / "never do X" rules

- **Never assume controller honesty** at the verifier. (`background.md` §2.1).
- **Never silently assume observer presence (A5).** "A5 is optional in practice and MUST NOT be silently assumed." (`background.md` §4.6).
- **Never state a security property without its assumptions/scope.** "Security properties must be stated relative to assumptions." "Failure to state these boundaries results in overstated guarantees." (`background.md` §4.7, §5.10).
- **Correct witnesses issue at most one receipt per event ID** and "Reject conflicting events, except as permitted by recovery rotation." (`background.md` §5.4).
- **Witness backers in `b` MUST be non-transferable** (public-key-as-AID). (`background.md` §2.3).
- **Never confuse detection with prevention** — a standing analytical hygiene rule. (`background.md` §4.5, §5.10).
- **Never treat a stated non-goal as a failure** (category-error guard). (`background.md` §4.5.1).
- **Threshold must satisfy M > f** (A7); M=1 provides no fault tolerance and "can be trivially broken by a single malicious witness." (`background.md` §5.3; `dg-c01-claude.md` §3).
- **Observers increase visibility, not control** — never expect enforcement/resolution from them. (`background.md` §6.6).

---

## 11. Worked context / real-world usage patterns

- **The witness/watcher split is the CT analogue:** witnesses ≈ CT logs (SCT ≈ signed receipt); watchers ≈ CT monitors/auditors closing the split-view window. "In both cases, the protocol provides the mechanism for detection; the deployment provides the actual detection." (`cr-ad-trust.md` §3).
- **Shared primitives with CT:** append-only hash-chained structures (KEL ↔ Merkle tree); cryptographically signed receipts; detection-orientation; hash-based PQ anchors; an actively-operated observer layer. (`cr-ad-trust.md` §3).
- **Early production deployments:** ISO 17442-3 verifiable LEIs (vLEIs) via GLEIF; GSMA Open Verifiable Calling (voice-fraud prevention). "the governance and operational frameworks KERI requires are developing in practice, not waiting on theory." (`cr-ad-trust.md` §5).
- **The "super watcher" pattern (GLEIF):** a centralized archival service giving broad coverage — "This works, but it reintroduces a centralized trust dependency that KERI was designed to avoid." (`cr-ad-trust.md` §5; DG-C05). Watch for **practical centralization pressure**: markets "gravitating toward identifiers backed by centralized resolution authorities." (`dg-c04-claude.md` §7.5).
- **CISO deployment realities** (across all `dg-c0X` §7 non-normative notes): assume controller compromise is inevitable; enforce strong default thresholds; **treat observer/watcher infrastructure as a first-class security control, not an optional add-on**; expect early-deployment detection to be "delayed rather than immediate," "probabilistic rather than deterministic," "coverage-dependent," "action-dependent" on governance. Real failure modes: correlated witness failure (same cloud provider), weak thresholds chosen for convenience, siloed/lazy watchers, alert fatigue.
- **The watcher burden = KERI's chief current limitation:** "A KERI deployment without robust watchers and governance is not a secure system." But "these are the weaknesses of something still growing into its design, not something whose design is running out of time." (`cr-ad-trust.md` §5, §7).

---

## 12. Trajectory / strategic doctrine

- "Both systems make fraud provable rather than impossible. Both require monitoring, accountability, and human judgment." (`cr-ad-trust.md` §7).
- KERI's constraints are "constraints of *immaturity*, not of *architecture*." PKI's are architectural — "baked into a standard that mandates certificate expiration, relies on administrators for continuity, and was designed before quantum computing was an engineering concern." (`cr-ad-trust.md` §6).
- "No trust architecture escapes the burdens of monitoring and accountability." (`cr-ad-trust.md` §5).

---

## 13. Second pass, 2026-10-14: sections the first pass skipped

### 13.0 Pin, scope and provenance of this pass

Source: `/home/daniel/code/wot/keri-security-analysis` at 149fa6c35 (commit subject: first rounds of analysis), the repository's only commit and unchanged since the first pass. Mining date 2026-10-14. Every quote below was read at that commit. Quotes from `background.md` drop the source's markdown emphasis and backtick markers and join its hard-wrapped lines; the words and their order are unchanged. Line numbers are hints. The two PDFs and `prompt-standard-analysis.md` were not read for this pass.

What this pass adds. A grep of `bible/` and `raw/` on 2026-10-14 found no citation of `background.md` §4.3, §4.4, §5.1-5.2, §6.7-6.9, §7.2, §7.3, §7.7, §8.1 or §8.4, and no citation of any `-chatgpt` or `-gemini` file. The bible's source list (`bible/01-foundations-and-worldview.md:197`) names the `background.md` ranges it drew on, and these sections fall outside them. Three partial overlaps exist and are not repeated here. The residual of §4.4.1, that pre-rotation compromise is catastrophic, is already carried at `bible/02-security-model-and-threat-posture.md:76`, via `00-lens.md` citing `background.md` §3.4-3.5. The A12 and A13 statements from §7.2 and §7.6 are already in the assumption table at `bible/02-security-model-and-threat-posture.md:105-106`, where A12 is cited only as "§7.x"; §13.5 below gives its section. The §7 CISO notes of the six Claude analyses were summarised in one paragraph at `bible/02-security-model-and-threat-posture.md:173` and in §11 above; §13.8 quotes them and says where they conflict with doctrine.

Provenance. `background.md` is this project's own analytical model, not a specification. It says so: "This document is the canonical background for KERI security analysis in this project." (`background.md` header comment, L4). Its claims are the corpus's reading of KERI and belong in the bible as analysis, never at `[spec]`. The `dg-c0X` files are per-claim analyses, and the filename suffix appears to name the model that produced each one; that is an inference, supported by the `-gemini` files ending in a chat assistant's offer, e.g. "Would you like me to analyze DG-C02, which addresses the Malicious Controller case?" (`dg-c01-gemini.md` L79). Their §7 sections describe themselves as non-normative.

### 13.1 What agreement does and does not guarantee (`background.md` §4.3)

The positive list is conditional on the §4.6 assumptions: "Given appropriate assumptions (enumerated below), sufficient agreement can provide:" (§4.3.1 L278). It names "Event durability: once sufficiently witnessed, an event cannot be retroactively removed" (L279), "Fork resistance under honest conditions: honest controllers cannot be forked by external attackers" (L280), and "Availability: witnesses can retransmit KERLs while controllers are offline" (L281).

The negative list is stated against agreement alone. "Witness agreement alone does not guarantee:" (§4.3.2 L287) fork prevention by malicious controllers, global convergence, "Timely detection of duplicity" (L290), and "Agreement across disjoint validator populations" (L291). The section closes on the locality rule: "Agreement is local to a controller’s witness set." (L293). This is the same content as the KAWA non-properties P5-P8 in §4 of this note, stated before KAWA is introduced, which is why a chapter can use it as the one-paragraph version.

### 13.2 Threat surfaces: threat, mitigation, residual (`background.md` §4.4)

§4.4 is the corpus's only threat enumeration in threat-mitigation-residual form, and its shape is the point: two of the four surfaces have no protocol mitigation at all.

Controller key compromise (§4.4.1). Threat: "Adversary obtains current signing keys" (L304). Mitigation: "Pre-rotation commitments" and "Recovery rotation" (L307-308). Residual: "Compromise of pre-rotation keys is catastrophic" (L311), already in the bible as noted in §13.0.

Malicious controller (§4.4.2). Threat: "Controller intentionally produces multiple conflicting KELs" (L318). In place of a mitigation the section records an observation: "KERI does not attempt to prevent this" (L321) and "Security relies on detectability and consequences, not impossibility" (L322). The scope sentence reconciles two things the bible states separately: "This threat is in scope, but must be analyzed separately from honest-controller cases." (L324). The threat is in scope for analysis while protection against it is an explicit non-goal (§1.3, carried in §2.4 above and at `bible/02-security-model-and-threat-posture.md:54-64`). The word consequences matters too: it puts governance response inside the security claim, which the bible's §4 does not currently say.

Witness misbehaviour (§4.4.3). Threats: "Signing conflicting events", "Withholding receipts", "Colluding with controller" (L331-333). Mitigation: "Thresholding" and "Assumptions on maximum faulty witnesses" (L336-337). Residual: "Witness sets are controller-chosen" and "No global witness reputation or enforcement" (L340-341). The second residual is not in the bible. It is the threat-model root of the witness-diversity and watcher-incentive material that the gap study assigns to an infrastructure chapter.

Observer absence or degradation (§4.4.4). Threat: "Watchers/jurors/judges are absent, lazy, siloed, or non-overlapping" (L348). Impact: "Duplicity may remain undetected indefinitely" and "Validators may accept conflicting histories permanently" (L351-352). The section ends: "This threat is explicitly acknowledged and not mitigated by protocol mechanics alone." (L354). This is the surface on which the one surviving residual of the Del Giudice bindings lands (§8 above, meta-pattern).

### 13.3 KAWA's purpose, inputs, outputs and state (`background.md` §5 preamble, §5.1-5.2)

Framing: "KAWA is analyzed as a controller-scoped agreement mechanism, not as a global consensus protocol." (§5 L444-445). Its three functions are event durability, availability, and "Fault tolerance: tolerate some fraction of faulty or unavailable witnesses." (§5.1 L457). What it does not attempt: "Establish global agreement among validators", "Prevent intentional equivocation by controllers", "Enforce witness honesty beyond threshold assumptions" (L460-462). The third item is new to the bible, and it is the protocol-side statement of §4.4.3's residual.

§5.2 gives KAWA a contract. Inputs for an event: "The event data (including prior event digest)", "Controller signature(s)", "Witness receipts" (L471-473). Outputs: "A sufficient agreement for E", "Inclusion of E in witnesses’ local copies of the KERL", "Retrievability of E + receipts by validators" (L477-479). Witness state is kept "per identifier" (L483): "A local copy of the KERL", "Receipt history", "Rules preventing disallowed equivocation" (L484-486). My reading, not the source's: because all witness state is per identifier, nothing in KAWA can relate two identifiers' histories, which is the mechanical reason agreement is witness-scoped.

### 13.4 Observer failure modes, literature, implications (`background.md` §6.7-6.9)

Failure modes (§6.7). Observer effectiveness degrades under "Sparse deployment", "Lazy or siloed observers", "Non-overlapping validator trust domains" and "Economic or governance disincentives" (L822-825). In the extreme case "Duplicity may persist indefinitely without detection." (L828), and the section classifies that outcome: "This is an acknowledged design tradeoff, not a protocol failure." (L830).

A reading rule for the literature (§6.8). Claims that duplicity cannot be helped, that validators are unavoidably vulnerable, or that forks are unavoidable "must be evaluated relative to assumptions A8–A11." (L841). "Claims that omit observer mechanisms implicitly assume:" observer absence or observer irrelevance (L843-845), and "Such assumptions must be made explicit to avoid overstated conclusions." (L847). This is a shibboleth in reverse: a critique that never mentions observers has assumed them away.

Implications (§6.9). "Observer mechanisms are core but optional" (L853); "Detection is probabilistic and time-dependent" (L855); "Absence of observers is a deployment choice, not an inevitability" (L856). The prescribed claim form is "Under observer assumptions A8–A11, property O# holds." (L859). The phrase core but optional is the one the bible lacks. It reconciles the protocol-level statement that the observer layer is enabled but not mandated (`bible/02-security-model-and-threat-posture.md:155`) with the deployment-level insistence that it is not an add-on (`bible/02-security-model-and-threat-posture.md:173`): optional to the protocol, core to the security outcome.

### 13.5 Validator inputs and acceptance rules (`background.md` §7.2, §7.3)

Inputs (§7.2). "A validator may rely on:" (L899) "Controller-provided KERLs", "Witness-provided KERLs", "Observer-provided evidence", "Cached or historical data" (L900-903). A12, "Validators may observe different subsets of the network and data sources." (L906), is defined here, so the "§7.x" at `bible/02-security-model-and-threat-posture.md:105` should read §7.2.

Acceptance (§7.3). "Validators typically accept a KERL if:" (L912) "It is internally valid", "It has sufficient witness receipts", "It conforms to local policy" (L913-915). Local policy "may consider:" "Witness reputations", "Observer reports", "Governance rules", "Risk tolerance" (L917-921). Then: "There is no protocol-mandated acceptance rule." (L923).

Tension with the specification, unresolved. That last sentence is stronger than the spec. The spec mandates validator behaviour on duplicity: an honest validator "MUST trust when there is no evidence of duplicity and MUST NOT trust when there is any evidence of duplicity" (KERI spec `spec/spec-body.md` L53 at `kswg-keri-specification` main 4df80aa, re-read for this pass; quoted at `bible/02-security-model-and-threat-posture.md:186`). `background.md` §7.3 is best read as saying that no rule chooses among valid histories or fixes the policy inputs, not that validators may accept anything. A chapter should carry the spec's rule as `[spec]` and §7.3 beneath it as analysis. The same tension recurs in §13.6.

### 13.6 Fork handling (§7.6) and the consensus-term translation (§7.7)

Fork handling (§7.6). "When a validator encounters duplicity:" (L995) "It may reject the identifier", "It may select one branch", "It may await further evidence" (L996-998). The middle option sits uneasily with the spec's "MUST NOT trust when there is any evidence of duplicity unless and until the duplicity has been reconciled" (KERI spec L53, as above), unless selecting a branch is read as reconciliation under the spec's first-seen discretion ("It is at the validator’s discretion", KERI spec `spec/spec-body.md` L1842 at main 4df80aa). Neither source settles which reading is intended. Recorded as an open question; not resolved here.

The translation table (§7.7). "Claims that use consensus language must be reframed:" (L1007)

| Consensus Term | KERI Interpretation |
|---|---|
| Safety | Cryptographic validity |
| Liveness | Controller progress |
| Agreement | Witness-scoped |
| Finality | Local durability |
| Consistency | View-relative |

(§7.7 L1009-1015, cells verbatim.) "Failure to perform this translation leads to category errors." (L1017). The bible already reframes safety and liveness in prose (`bible/02-security-model-and-threat-posture.md:184`) and addresses finality as a tell (`bible/07-shibboleths-and-anti-patterns.md:260-266`), but it has no term-for-term table, and the pairings Finality to Local durability and Consistency to View-relative appear nowhere in it.

### 13.7 Del Giudice's declared scope and terminology (`background.md` §8.1, §8.4)

Declared scope (§8.1). The thesis's modelling choices are listed: "Primary focus on KAWA (witness agreement for event generation)" (L1075), "Primary security posture: honest controllers under attack" (L1076), "Malicious controllers treated only insofar as they demonstrate limits" (L1077), "Delegation and multisignature controllers declared out of scope" (L1078), "Non-transferable identifiers assumed for witnesses" (L1079), and observers "described but not analyzed as primary security contributors" (L1080-1081). The verdict: "These choices are consistent internally, but they constrain the domain of validity for many claims." (L1083-1084). The consequence the bible does not yet state: no Del Giudice result can be cited for a delegated or multisig identifier, so the delegation doctrine at `bible/03-key-management-and-identifier-lifecycle.md:114-163` has no formal-analysis backing from this thesis.

Terminology (§8.4). "Several terms used in the thesis correspond to more precise concepts in this document:" (L1292-1293)

| Thesis Term | Model Mapping |
|---|---|
| Consistency | P2 (Section 5.6) |
| Safety | Cryptographic validity (Section 7.5.1) |
| Liveness | Controller progress (Section 7.5.2) |
| Agreement | Witness-scoped agreement (Section 5) |
| Eventual consistency | Eventual awareness (Section 7.4.3) |

(§8.4 L1295-1301, cells verbatim.) "This mapping should be applied before comparative or critical analysis." (L1303). Two notes. The Consistency rows of §7.7 and §8.4 differ, View-relative against P2, and they are not in conflict: §7.7 translates generic consensus language, while §8.4 maps the thesis's specific use, which is the witness-level property P2. A chapter should not flatten them into one row. And the last row is the useful one for reviewers: a reviewer who calls KERI eventually consistent is claiming more than it provides, since eventual awareness "is possible, not guaranteed" (§7.4.3, at `bible/02-security-model-and-threat-posture.md:181`).

### 13.8 The CISO notes, condensed (`dg-c01..c06-claude.md` §7)

Status. These are one analyst's view, model-generated, and non-normative by their own labels: "This section is explicitly non-normative and does not assess protocol correctness." (`dg-c01-claude.md` §7 L187); "This section is explicitly non-normative and non-argumentative." (`dg-c04-claude.md` §7 L144). Where a note pulls against doctrine, doctrine wins, and the note is recorded as deployment opinion. None of the empirical-sounding claims (how often compromise is holistic, how deployments choose thresholds) cites evidence.

Consistent with doctrine, and the substance an operations chapter could use:

- Assume compromise. "Treat controller compromise as inevitable and design for graceful degradation." (`dg-c01-claude.md` §7 L195).
- Witness diversity against common-mode failure: "if witnesses are all hosted by the same cloud provider or operated by the same organization, correlated failures become likely." (`dg-c01-claude.md` §7 L199).
- Threshold defaults and validator policy: "Provide strong default thresholds in tooling." and validators "refusing to accept identifiers with weak thresholds" (`dg-c01-claude.md` §7 L211). Against this, "Real deployments may use minimal witness sets (e.g., 1-of-2 or 2-of-3) for cost or convenience" (`dg-c06-claude.md` §7 L124).
- Observer infrastructure as a primary control: "Deploy watcher infrastructure as a first-class operational concern." (`dg-c01-claude.md` §7 L238).
- Named watcher failure modes: "Inconsistent polling frequencies (watchers check weekly instead of continuously)", "Misconfiguration (watchers poll wrong witness sets, fail to aggregate evidence)", "Alert fatigue (evidence of duplicity exists but is not acted upon)" (`dg-c02-claude.md` §7 L132-134).
- The incentive problem: "Running watchers has costs but diffuse benefits; free-rider problems likely" (`dg-c05-claude.md` §7 L175).
- The tools-versus-deployment line: "The protocol provides the tools for detection; operational reality determines whether those tools are deployed." (`dg-c02-claude.md` §7 L151).
- Fail-closed validator default: "Reject identifiers on detection of duplicity (fail-closed)" (`dg-c03-claude.md` §7 L238). This agrees with the spec's MUST NOT trust rule (`bible/02-security-model-and-threat-posture.md:186`).
- Controller honesty as the common case: "most controllers are likely to be honest (they have no incentive to fork their own identities and invite detection)." (`dg-c06-claude.md` §7 L119).
- User expectation: network disruption "may surprise users expecting instant finality." (`dg-c06-claude.md` §7 L134).
- Custody of next keys. "Attackers who obtain current keys frequently have broader access (credential stores, backups, build pipelines), making pre-rotation key security questionable." (`dg-c04-claude.md` §7.1 L150). This is a tension rather than a conflict: the firewall assumes "The next key itself stays offline, in cold storage" (`bible/02-security-model-and-threat-posture.md:72`), and the note is a warning that operations can void that assumption. It belongs in an operations chapter as a custody requirement, not in chapter 02 as a weakening of the firewall.

Where the notes conflict with doctrine. The first two are the clearest; the rest are this pass's reading and are marked as such.

1. Recovery escrow. "Controllers registering recovery intentions with trusted third parties before compromise" (`dg-c04-claude.md` §7.4 L176). This contradicts the bible's account of why recovery rotation exists, that it gives "real-world recoverability without a trusted third party" (`bible/02-security-model-and-threat-posture.md:226`), and the root-of-trust doctrine that KERI "does not rely on any trusted third-party administrative process" (KERI spec `spec/spec-body.md` L89 at main 4df80aa; quoted at `bible/01-foundations-and-worldview.md:47`). Pre-rotation already is the sealed recovery commitment (§2.6 above). Do not carry escrow as a recommendation; if cited at all, cite it in chapter 07 as an example of the administrative-trust reflex.
2. Authoritative KELs. "Publish authoritative KELs for high-stakes identifiers (e.g., root authorities)" (`dg-c03-claude.md` §7 L235). This conflicts with the invariant that witnesses and OOBIs are "sources of data, never sources of authority" (`bible/02-security-model-and-threat-posture.md:42`). A KEL's authority is its signatures; a publisher can make one available but cannot make it authoritative. Publishing KELs is fine; the adjective is the error.
3. Governance as mandatory. "Governance is not optional" (`dg-c03-claude.md` §7 L259). This pulls against "Observer mechanisms are core but optional" (§13.4) and the bible's "enables but does not mandate" (`bible/02-security-model-and-threat-posture.md:155`). Reconcilable if read as a deployment requirement for high-stakes use, which is how a chapter should state it; not as a protocol requirement.
4. Higher thresholds against malicious recovery. "Higher M values make recovery rotation harder to execute maliciously (but also harder to execute legitimately)" (`dg-c04-claude.md` §7.4 L175). My reading, not adjudicated by any source: the authority for a recovery rotation is the pre-committed keys, and a correct witness receipts a properly authorised event whatever the threshold (P1, §4 above; recovery rule, `background.md` §5.5), so raising M changes receipting fault tolerance, not who can rotate. Unsupported; do not carry without a source.
5. Time-windowed recovery acceptance. "Validators only accepting recent recovery rotations with fresh evidence" (`dg-c04-claude.md` §7.4 L177). No time window appears in the recovery rules this corpus carries (`bible/03-key-management-and-identifier-lifecycle.md:155-163`). A validator could impose one as local policy (§13.5), at the cost of rejecting legitimate late recoveries. My reading; record as policy, not doctrine.
6. The super watcher as fork resolver. dg-c04 expects validators to "defer to external governance" through GLEIF's super watcher "for fork resolution" (`dg-c04-claude.md` §7.3 L168). The note presents this as a centralisation risk, not a recommendation, so the conflict is terminological: fork resolution is judge work, and the bible records maintainer usage in which super names scope and attaches to all three roles (`bible/02-security-model-and-threat-posture.md:161`). A useful example of the role collapse that paragraph warns about.
7. M = 1 and a single witness. "A controller with M = 1 can have its history forked by a single compromised witness." (`dg-c01-claude.md` §7 L209). My reading: a witness cannot author controller-signed events (P1), so a fork needs compromised or duplicitous controller keys as well; M = 1 removes the witness check, it does not by itself create the fork. The bible repeats the looser form as "M = 1 is trivially breakable" (`bible/02-security-model-and-threat-posture.md:214`, from `dg-c01-claude.md` §3). Open question: tighten that line, or find a source that supports it as written.

### 13.9 Corroboration from the ChatGPT and Gemini variants (dg-c01, dg-c02)

Cited as corroboration only. Neither file adds a doctrinal claim the Claude analyses lack, and both are lower-fidelity exports: `dg-c01-gemini.md` lost its inline mathematics ("quorum sizing ()", L9).

Same verdicts, independently reached. On DG-C01: "Within its stated scope, the claim is faithful to KERI-as-specified." (`dg-c01-chatgpt.md` §2 L13); "The claim is faithful to KERI-as-specified regarding the local mechanics of witness agreement" (`dg-c01-gemini.md` §2 L25). On non-transferable witnesses, corroborating `background.md` §2.3 (§6 above): the backer-list choice "is normative in KERI-as-specified" (`dg-c01-chatgpt.md` §2 L21). On DG-C02: "a non-goal (preventing malicious controllers from equivocating) is treated as a shortcoming rather than as a scoped exclusion." (`dg-c02-chatgpt.md` §5 L68); the claim "borders on a category error by framing a deliberate non-goal (fork prevention)" as missing protection (`dg-c02-gemini.md` §5 L63). On operations: "Deployments that omit them will experience materially weaker security without violating the spec." (`dg-c01-chatgpt.md` §7 L84); "Even if duplicity is detected, the protocol doesn't tell you what to do." (`dg-c02-gemini.md` §7 L82), which restates O2's "Proof does not imply remediation" (`bible/02-security-model-and-threat-posture.md:167`).

Where the variants go further, and should not be carried. ChatGPT says "KAWA’s guarantees are brittle under partial failure: they do not degrade gracefully" (`dg-c01-chatgpt.md` §7 L83). That is fair about the threshold proofs and misleading about the system, where detection takes over as consistency fails (§2.1, §2.4 above). Gemini cites "the Swiss e-ID case" (`dg-c02-gemini.md` §7 L81) with no source; uncorroborated.

### 13.10 Routing

Chapter 02, security model:

- §13.1 agreement guarantees and §13.3 KAWA's purpose and contract feed §7 (KAWA), as the short statement before P1-P8.
- §13.2's malicious-controller entry (§4.4.2: in scope for analysis, consequences as part of security) feeds §4.
- §13.4's core-but-optional and the A8–A11 claim template feed §9.
- §13.5 and §13.6's fork handling feed §10. The spec tension is an open question for that section, and the A12 citation at line 105 should become §7.2.
- §13.7's declared scope feeds §11, with a sentence that the bindings say nothing about delegated or multisig identifiers.
- §13.8 conflict 7 (M = 1) is a proposed correction to line 214.
- §13.9 supplies corroboration footnotes for §11 only.

Chapter 07, shibboleths:

- §13.6's consensus-term table and §13.7's thesis-term table feed §7 and the quick-reference in §13.
- §13.4's reading rule, that a critique omitting observers has assumed their absence, feeds §7.
- §13.8 conflicts 1 and 2 (recovery escrow, authoritative KELs) are examples for §2, the administrative-trust tells. Conflict 6 belongs in §8, role confusion.

Planned infrastructure and operations chapter, fed by `raw/18`:

- §13.2's witness residuals (controller-chosen witness sets, no global witness reputation or enforcement) and the observer-degradation surface.
- §13.4's failure-mode list (§6.7).
- The consistent half of §13.8: witness diversity, threshold defaults, watcher failure modes and incentives, fail-closed defaults, and custody of next keys.
- §13.8 conflicts 3 to 5, as policy options with their doctrinal limits stated.

Open questions carried from this pass: whether `background.md` §7.3's "no protocol-mandated acceptance rule" and §7.6's "select one branch" can be squared with the spec's MUST NOT trust rule (§13.5, §13.6); and whether the M = 1 claim at `bible/02-security-model-and-threat-posture.md:214` has a source that supports it as written (§13.8 item 7).
