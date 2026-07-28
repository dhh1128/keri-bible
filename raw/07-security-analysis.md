# 07 — Security Analysis: Survivability, Threat Model, and the Del Giudice Claim Bindings

Raw doctrine-mining notes. **Sources:** `/home/daniel/code/keri-security-analysis/` — primarily `cr-ad-trust.md` (Cryptographic vs. Administrative Trust paper), `standard-analysis.md` (the analysis-method template), `background.md` (canonical background, "already digested" — used here only to anchor section/assumption/property numbers and exact quotes), and the six per-claim analyses `dg-c01-claude.md` … `dg-c06-claude.md`. Citations give file + section heading (or § / line). Quotes are ≤25 words, verbatim.

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
