# 12 — Origin Security: KERI/ACDC/CESR Doctrine in a Real Zero-Trust Deployment

**Sources** (all under `/home/daniel/code/origin-platform/docs/`):
- `origin-security.md` (OS) — threat model + zero-trust philosophy
- `general-origin-characteristics.md` (GOC) — platform-wide auth/authz patterns
- `authorizing-services-and-automation-users.md` (ASAAU) — AU model, RFC 9421, sponsorship, encryption
- `authorization-caching-strategies.md` (ACS) — ADR on caching layer
- `identifiers-for-users.md` (IFU) — client AID vs agent AID vs user ID vs Origin user AID
- `how-we-generate-aliases.md` (HWGA) — alias-generation algorithm
- `managing-aliases.md` (MA) — identity theory + why aliases matter

This is *doctrine-in-practice*: how a production platform (Provenant/Origin) applies KERI/ACDC worldview to a shipping zero-trust system. It is the applied counterpart to KERI's abstract spec — showing which pieces they keep, which they simplify (direct-mode AU-AIDs, no KEL), and the deployment tradeoffs.

---

## 1. What KERI-based security fundamentally IS and IS NOT (worldview / design intent)

### Perimeter security is the anti-pattern being rejected
- Traditional security = "secure perimeter: *Keep bad stuff out, and only trust what's inside*" — mental model is "a castle under siege." (OS §1)
- **This depends on "a superbly maintained perimeter — an assumption that the history of warfare (and cybersecurity) tells us will eventually be wrong."** (OS §1) Also susceptible to malicious *insiders* (hacked systems, rogue sysadmin).
- **"If our business grows, we will eventually be hacked."** (OS §1) — survivability-not-invulnerability stance: plan for breach, don't pretend it won't happen.
- Named perimeter technologies rejected as embodiments of perimeter thinking: **"IAM, SAML, OAuth, OIDC, LDAP, AD, API keys — are mostly embodiments of perimeter security."** (OS §1)
- The perimeter ceremony: "A person or a piece of software goes through a high-friction ceremony to convince a gatekeeper to let them in... once they're inside, they're never challenged again." (OS §1)
- The token critique (core to the OAuth/JWT/session rejection): re-challenges are satisfied merely by "produce a token that the sentry gave them. Internal challengers don't do any deep checking of their own... because the token is too lossy to support deep checking anyway. The token is thus **faster but less safe and far more opaque than verification at the perimeter.**" (OS §1)

### The core diagnosed weakness (the thesis sentence)
> *"too much trust depends, with flawed alignment, too much effort, and too little justification, on what was (supposedly) guaranteed at a perimeter."* (OS §1)

- This flaw "has victimized some of the most carefully maintained systems in the world" (cites the China-backed Microsoft signing-key theft). (OS §1)
- Cascade of perimeter "solutions" that compound rather than fix: specialized gatekeeper layers → **confused deputy problems**; stale tokens → short-lived tokens → renewal churn; centralization abuse locus/silos → aggressive federation. **"When you combine these 'solutions', you get the worst of all worlds, not the best."** (OS §1)
- Federation is explicitly a symptom, not a cure: "centralization provides a locus for abuse, and creates silos. This is typically solved by aggressive federation (centralization hierarchies)." (OS §1) — outsider-tell: KERI people see federation as compounding centralization, not decentralizing.

### Zero-trust as the KERI-correct reframing
- **"assume everything — outside OR inside the perimeter — is unsafe until proven otherwise."** (OS §4 / GOC §1) The single load-bearing zero-trust axiom.
- Not perimeter-abandonment; perimeter-plus: "Provenant *does* make meaningful investments in secure perimeters. However, we *also* think outside the box (perimeter)." (OS §1) They "only relax this posture in a handful of cases where a careful analysis of costs and benefits... shows us that a risk is not worth its countermeasures." (OS §1)
- Zero-trust's effect on risk (the treasure metaphor): instead of one guarded room, "what if the treasure were distributed in a thousand places... active rather than passive... intelligent rather than dumb... could attack a thief or teleport... including after it had been stolen?" (OS §4)
- Verify, don't gate: **"We achieve high security by making everything verifiable by anyone (and actually doing that verification), not just by adding more and better-defended, centralized perimeters."** (ASAAU §2.2)

### End-verifiability vs opaque tokens
- KERI gives "**end-verifiability** (cheap but thorough verification anywhere, with minor staleness concerns and no need for expiration, rather than opaque and perishable tokens)." (OS §4.1) — captures the doctrine that KERI verification is (a) doable *anywhere* by *anyone*, (b) needs no expiration, (c) has only *staleness* (not forgeability) as its residual concern.
- Features unlocked by authenticating with KERI (OS §4.1): decentralization (frictionless, self-service, uncoordinated yet ultra-secure; eliminates some malicious-sysadmin attacks), special-purpose/disposable AIDs with narrowed privileges, **prerotation (recovery from key compromise)**, post-quantum support, end-verifiability, multisig (redundancy + checks and balances), **witnesses (duplicity detection)**, low-latency revocation, delegation, "**the same basis of security everywhere**."
- "**It's hard to overstate how dramatically this changes the landscape.**" (OS §4.1)

---

## 2. Security & threat-model positions

### Threat model (OS §2) — six non-crisp, non-exhaustive categories
1. **Manipulate people (social engineering)** — convince a LAR to sign something the org doesn't intend; AI impersonating a real person; social-engineer support into a disallowed change.
2. **Cause damage** — delete records, deface website, artificially inflate bills.
3. **Corrupt data** — "Poison a cache so we make bad decisions when verifying or revoking. Add to or delete history to ruin an org's reputation. **Send bogus events to a witness to trigger duplicity conditions.**"
4. **Steal data** — learn a competitor's customers; steal a passcode or private key.
5. **Escalate privileges** — steal a passcode to issue/revoke credentials; call an inadequately secured API.
6. **Distort behavior** — DoS/DDoS; exhaust disk to force a crash.

- Explicitly **de-prioritized:** "Attempting to crack cryptography is a theoretical threat, but it's not mentioned because it's unlikely." (OS §2)
- **"Other potential threats are drastically mitigated by KERI, making them less prominent in our thinking than they would be for a general SaaS architecture."** (OS §2) — KERI shrinks the threat surface.
- Categories are fuzzy/interacting: "Social engineering often leads to escalation of privilege — and vice versa." (OS §2)
- **"All of these threat categories can originate either inside or outside Provenant's perimeter."** (OS §2) — the insider-threat invariant.

### Layered perimeter defenses (OS §3) — each layer paired with an explicit assume-breach caveat
Metaphor: guarded treasure = "the safety and reputation of our customers and of Provenant itself." Each boundary is followed by "But we must assume that enemies may arise inside…":
1. **Network boundary** (guarded wall/kingdom): VPCs (filtered NATing), network groups, no external IPs, load balancer rate-limiting. (OS §3.1)
2. **Cell boundary** (moated castle): k8s cluster edge; LB rate-limits, reachability rules, health/auto-repair, horizontal autoscale. (OS §3.2)
3. **Docker container boundary** (locked keep): isolated container per service instance; disables unneeded OS features; microservices specialized/narrow. (OS §3.3)
4. **Service boundary** (sentry): JVM + Spring Boot protections, GC, stack guards, https-only, circuit breakers. **"But we must assume that the sentry may be disloyal, co-opted, or defeated."** (OS §3.4)
5. **Database schema boundary** (differently-locked treasure rooms): per-service DB accounts, DBMS restricts each account to its data subset. (OS §3.5)
6. **Tenant/org/user boundary** (treasurer with a sword): custom authorization code restricts features by tenant/org/user. "But we must assume that the treasurer could be tricked or drugged." (OS §3.6)

**Doctrine:** even a maximally layered castle gets robbed; history is "*full* of accounts where treasure has been stolen, even from a guarded, locked room at the top of a keep." (OS §4) → detection/survivability techniques added *on top of* prevention.

### Duplicity detection (detection-not-prevention)
- KERI's role: **"Witnesses checking for and reporting duplicity. Super watcher. Reports from branch cells help."** (OS §4.2)
- Reiterated: "**Duplicity detection**: Witnesses check for and report forking." (GOC §9)
- Threat #3 explicitly names attacking a witness "to trigger duplicity conditions" — the adversary tries to *manufacture* duplicity, so the deployment must treat witness inputs as adversarial. (OS §2)

### Data-centric security — move security *with the data*, not with the transport
This is the deployment's strongest applied-KERI doctrine, elaborated at length in ASAAU §3.6:
- **"Move Security with the Data, Not the Transport."** (GOC §8)
- Critique of "secure pipes" (VPN/TLS): they "embody a *perimeter mindset*." (ASAAU §3.6)
- **"The walls of a pipe may be a secure perimeter, but every place where a pipe ends is a gap."** Physical analogy: leaky pipe joints. A simple 2-endpoint pipe already has "2 gaps"; a realistic routed path has "at least 8 — or possibly more." (ASAAU §3.6)
- Joints as active attack sites: "What looks like a secure joint might actually be a **T-shaped connection where data is siphoned off, trust rules change, or trust input data changes while holding rules constant!**" (ASAAU §3.6)
- Real-world MITM-by-design: **SSL visibility appliances** deliberately MITM TLS; and the EU eIDAS reforms "appears to be planning legislation that allows the same attack to be carried out by national governments." (ASAAU §3.6) — treated as a live threat, not hypothetical.
- **"Secure pipes protect data in motion, but not data at rest."** An attacker inside the perimeter around A or B reads/tampers freely. (ASAAU §3.6)
- Signing's scope and limits: "By signing everything, we eliminate the possibility that a man in the middle could tamper. However, **signing can't prevent eavesdroppers.**" (ASAAU §3.6) → encryption is the complement to signatures.
- The essential insight named: this is IETF **MLS (message-level security)** vs TLS transport-level, and ToIP's **Trust Spanning Protocol (TSP)**. "our architecture will begin to adopt it when that's practical." (ASAAU §3.6)
- Pragmatic honesty about keeping TLS anyway: HTTPS/VPCs/Kafka security give "moderate protection at low cost... It is easier to use them than to explain to our customers' IT departments why they are insecure." But "we do not expend massive effort guaranteeing that our secure pipes are perfectly leak-proof." (ASAAU §3.6)

### Guarantees stated relative to explicit assumptions
- Auth mechanism MUST "**Be no less secure than KERI itself**" (ASAAU §2.1) — rationale: "There is no point in building organizational identity with weak security; that's just recreating the status quo." A guarantee framed relative to KERI's own security floor.
- Cross-cell confidentiality guarantee is conditional/scoped: sealed-box encryption applied only where it matters. "**it's not worth using inside a k8s cluster, because if an attacker is inside the k8s cluster, other vulnerabilities will be exploitable anyway.** However, it is definitely worth doing any time data moves from one cell to another." (ASAAU §3.6 / GOC §8) — an explicit cost/benefit-bounded guarantee.

---

## 3. Invariants and "never do X" rules

- **NEVER use sessions, cookies, tokens (short-lived or otherwise), JWTs, OAuth, OIDC, or SAML to secure calls to Origin.** (ASAAU item 0 / GOC §2) The one possible minor exception: the web portal UI's calls to its own backend. "Maybe." (ASAAU footnote 1)
- **Every request is cryptographically signed and verified independently; authentication happens at every hop.** (GOC §2) No "trust after entry."
- **Never do direct DB access to another service's data — must call the native service API.** "Foreign services must call the native service API to read/write that data—never direct DB access." (GOC §4)
- **Never hand-edit generated files** (`frontend/src/api/*`, `docs/api-doc.yaml`). (GOC §12)
- **No hardcoding** of API endpoints, credentials, deploy environment, or feature flags — all from env vars. (GOC §11)
- **Aliases MUST NEVER be parsed for meaning and MUST NOT be treated as identifiers.** Full-caps in source: "*ALIASES ARE **NOT** UNIQUE, AND THEY CAN CHANGE OVER TIME. THEY MUST NEVER BE PARSED FOR MEANING, AND THEY **MUST NOT** BE TREATED AS IDENTIFIERS. MAKING SUCH MISTAKES WILL INTRODUCE BROKEN LOGIC...*" (MA §2)
- **AIDs (globally unique) MUST be used in all system logic**, never aliases. "it is globally unique AIDs that MUST be used in all system logic." (HWGA step 9)
- **Never reuse an identifier for AUs understood to be different.** "We never reuse the same identifier for AUs that we understand to be different." (ASAAU §3.2 rule B)
- **Never confuse guessed identity with proved/verified identity.** "Confusing guesses with something that's been verified undermines the trust and authenticity of the system... This is the very attack surface that hackers exploit to create man-in-the-middle attacks." (MA §4) → enforced structurally via the `{caveat}` field ("?" = unverified vs "(verified)").
- **Never expose unverifiable semantics to users.** "If our system doesn't have a good answer to any of these questions, then neither do our users, and we MUST NOT give our users additional semantics that are unverifiable." (MA §4)
- **All publicly verifiable actions MUST be linked to an AID.** "when we delegate authority, the source and the recipient of the authority must both be identified by an AID... when we issue a credential like a vLEI, both the issuer and the issuee... must be identified by an AID." (MA §1)
- **A separate AID per identity facet / per role grant.** "Each facet of an identity really should have its own AID... we automatically create a separate AID each time a person is granted a new Origin role." "Having granular AIDs... guarantees that security and trust never cross-contaminate." (MA §1)
- **An OOR-vLEI-bearing AID MUST be dedicated to its role** and "MUST not be used to register Cecilia for the 5k company fun run." (MA §3)
- **An AU is permanently identified by exactly one UUID and exactly one AID.** (ASAAU §3.3) An agent AID cannot exist without a client AID (but not vice versa). (IFU)
- **Passcode never shared with Provenant code** — "a passcode that has never been shared with any Provenant code, not even once for a millisecond." (OS §4.1.1)
- Sealed box, **NOT** secret box, for cross-cell encryption. (ASAAU item 7) Sealed box "prevents even the sender from decrypting (one-time use; ephemeral key pair)." (GOC §8)

---

## 4. Anti-patterns / outsider-tells / misconceptions explicitly corrected

- **Perimeter fixation** (castle-under-siege) → zero-trust "unsafe until proven otherwise." (OS §1)
- **Opaque bearer tokens** (JWT/session/API key): "faster but less safe and far more opaque than verification at the perimeter." Replaced by end-verifiable signatures. (OS §1, §4.1)
- **Federation as a fix for centralization** → treated as compounding the disease. (OS §1)
- **Auth-then-authz as a single indivisible login (the sentry model)** — explicitly challenged. "In traditional views of security, authorization is preceded by authentication, and the two occur together as a single indivisible process. This is a natural consequence of a perimeter-oriented mindset... all the way back to... a sentry challenged someone approaching the gate." (ASAAU Appendix)
  - KERI-correct reframing = **Attribute-Based Authorization (ABA):** "someone can receive permission if they can prove certain characteristics, even if a sentry does not (*yet*, or maybe *ever*) know who they are." (ASAAU Appendix) Examples: voting booth (prove citizenship, not identity, with once-only enforcement); pharmacy (any licensed doctor may browse prescriber pages, authenticates only when submitting a prescription for accountability); **EBA** (banks/QVIs do authentication, EBA does only authorization → "For EBA, authentication happens *after* authorization"). Origin "partially dissociate[s] the authentication and authorization processes."
- **"Secure pipes" (VPN/TLS) as sufficient** → leaky-joint critique; move security into the data (MLS/TSP). (ASAAU §3.6)
- **X.509 / SSH keys haven't solved identity** — "SSH keys and X509 certificates are mature technologies, deployed and supported almost everywhere. Yet ['on the internet, nobody knows you're a dog'] is still as true today as it was in 1993." Diagnosis: **"the hard problem with combining cryptography and identity is not technological — it's UX."** (MA intro)
- **The surveillance economy / over-identification anti-pattern:** login-with-Google leaks address, full name, age, photo, timezone, phone for a dog-food purchase. "most of us are terribly over-identified." Privacy solved by per-facet AIDs, not by a central IdP. (MA §"The need for boundaries")
- **KERI ≠ a UX solution by itself:** DHS/Evernym spent ~$1M on the DKMS UX problem, "still remains mostly unimplemented, and **KERI does little to help.**" (MA intro) — Origin's aliases fill the gap KERI leaves.
- **AID ≠ UUID.** Two properties make an AID different: (1) verifiable key state — "resolved to its cryptographic keys, including their chain of custody and any evolution... at any given point in time, kind of like how a domain name can be resolved to an IP address"; (2) can prove (1) **"without relying on an external system like a database or a blockchain."** (MA §1)
- **AID ≠ blockchain address.** "People have used blockchains to achieve something like this... a payment address on Bitcoin or Ethereum has most of these same properties. However, the word 'autonomic' suggests... without the help of an external system. This is one of the unique features of KERI." (MA §1) — the explicit rejection of blockchain/consensus/global-ordering as the root of trust.
- **Multi-sig ≠ organization (a common misread):** "it is not a generally true equivalence that multi-sig = org. Some orgs consist of only one person, so their AIDs are single-sig." Categorize by *signature type* first (biggest UX effect), then personal-vs-org. (HWGA)
- **Client AID ≠ agent AID ≠ user ID ≠ Origin user AID** (four-identifier confusion, IFU): client AID identifies a *wallet* (signify side); agent AID identifies the *cloud agent* (keria side); user ID (UUID) identifies a *human*; Origin user AID (alias "alice-as-user-at-origin") is what signs traffic when logged in. "Properly understood, the client AID identifies a wallet, NOT a human being or an agent." Client/agent AIDs are keria/signify internals — "we should not be using them directly."
- **"Introducing" ≠ "proving" (no-MITM):** "*introducing* is not the same thing as *proving* there is no man in the middle. We will automatically *introduce*. We won't automatically prove." (MA §7) Humans must still make trust decisions.

---

## 5. Precise terminology / definitions

- **AID (autonomic identifier):** "a long, unfriendly-to-humans string... a globally unique identifier... like a UUID on steroids." Example `ENBYrQqWyRLAYqMLYv_qm-qP7eKN81Wmjyz5nXQvYLYz` = Provenant as a legal entity. Two defining properties: verifiable key state + self-service proof without external system. (MA §1)
- **AU (automated user):** "software and/or hardware that has formal status (an account) with the platform and that normally operates with limited real-time guidance from humans." Examples: Origin microservices, customer scripts, external integrations. **"AU does not mean AI."** Always has a *controller* (human or org) legally accountable. (ASAAU §3.1)
- **AU-AID:** the single AID identifying an AU; associated with the "X-as-Origin-user" alias and the `wallet_aid` field. **Direct-mode, non-transferable:** no KEL, no witnesses, cannot rotate keys — "essentially, the AID is just an Ed25519 key that has been transformed slightly." Verify by converting AID → public key via trivial transformation. **"No KERI or ACDC knowledge is required to act as an AU or to authenticate an AU."** Yet behavior remains "auditable by KERI- and ACDC-aware software, because it obeys the rules." (ASAAU §3.3 / GOC §2)
- **Sponsor:** the party who onboards an AU — **"not an *approver*... but rather an *introducer*."** Must have `do org.onboard-au` permission for the org AND be identity-verified (`verification_id` non-null), OR be a delegated AID empowered by a **GCD credential** with `c_goal = origin.org.onboard-au`. "sponsors can be decentralized." (ASAAU §3.4, item 2)
- **Controller:** individual or org accountable for an AU's actions; org accepts responsibility by allowing sponsorship. AUs tied to exactly one org for accountability clarity. (ASAAU §3.1, §3.4)
- **User ID (UUID):** internal, centralized, DB-stored, never shown to humans; 1-to-1 with a human. Exists "before we know whether a human being already has a wallet"; enables merging/splitting user records. (IFU, ASAAU comparison table)
- **Origin user AID:** the AID (alias "alice-as-user-at-origin") that signs traffic when a human is logged in. (IFU)
- **Client AID** (signify/wallet) vs **agent AID** (keria/cloud agent): keria/signify constructs; agent signs to client with agent AID keys, client signs to agent with client AID keys; normally 1-to-1 but "NOT automatically true." (IFU)
- **Alias:** "a friendly name for an AID" e.g. "Cecilia as CEO at Acme." Not unique, mutable, never an identifier. (MA §2, HWGA)
- **Three defining properties of an AID (= the three alias questions):** **who** (whose self is partially identified), **role** (responsibility/posture/behavior pattern), **context/scope** (in what scope the who+role are relevant). A new AID is created for any new combination. (HWGA §Method, MA §4)
- **BADA-RUN semantics** (Sam Smith): "Best Available Data Acceptance – Read Update Nonce"-style — signed requests carry a nonce making them idempotent/replay-safe; resending the same request with the same nonce yields the same result. (ASAAU items 2, 5, §3.4 test 5; GOC §2)
- **Nonce:** time-based within ±2 seconds (in `signify-timestamp` header), OR fetched from `/nonce` endpoint valid for ±10 seconds (for clients with clock skew). (ASAAU §3.4, GOC §2)
- **RFC 9421** (HTTP Message Signatures): `Signature-Input` (which elements: `@method`, `@path`, named headers), `Signature` (Ed25519 over signing base + nonce), a named header carrying the AID (`Signify-Resource` or `AU-AID`). (GOC §2)
- **Native service pattern:** each service type owns specific DB schema/tables; foreign services call its API, never touch its tables. (GOC §4)
- **Audience classifications** (GOC §3): **Allic** (actively publicized to everyone — revocations, QVI AIDs); **Anyic** (public but not proactively publicized — legal-entity AIDs); **Selfic** (only the owner — passphrases, wallet data); **Relatic** (tightly-defined relationships only — pairwise AIDs); **Haptic** (anyone with business need + roles/permissions — invoices, employee AIDs); **Boundic** (owner-defined boundaries excluding specific parties — NDAs, competitor restrictions).
- **Cells / clerk / data movement:** root cells publish to Kafka; branch cells subscribe via **Clerk** service. Movement: **direct-to-center** (branch→root) → **outward** (root→branches); **allic** items also move **extraward** (to witnesses/external parties). (GOC §4)
- **GCD credential:** grant/capability-delegation credential (public-schema `gcd`) whose `c_goal` authorizes a delegated AID to act (e.g., onboard AUs). (ASAAU §3.4)

---

## 6. Worked examples, schemas, real-world usage patterns

### RFC 9421 + AU-AID verification (identical across all services) — GOC §2
1. Extract `Signature-Input` and `Signature` headers.
2. Check nonce within acceptable time range.
3. Reconstruct signing base from `@method`, `@path`, named headers.
4. Look up signing AID in authorized-caller cache (fall back to user DB).
5. `Ed25519.verify(public_key, signature, signing_base)`.
6. Check AID has permission for this endpoint (via grants).

### AU onboarding request (JSON) — GOC §2 / ASAAU §3.4
```json
{ "aid": "<AU-AID → wallet_aid in DB>", "org": "<org UUID>",
  "name": "<friendly name → personal_names>", "grants": [<proposed grants>],
  "inactive_date": "<datetime (optional)>", "webhook_url": "<url (optional)>" }
```
Signed by sponsor over body + nonce. Verification tests in order (ASAAU §3.4):
1. Nonce within time range? 2. Signature verifies for claimed signer? 3. Signer an approved caller (cache or DB)? 4. JSON well-formed? 5. **AU-AID doesn't already exist? (test 5 → BADA-RUN idempotency)** 6. Signer has `do org.onboard-au` for org + is ID-verified?
On success: write `user` row, assign UUID, return UUID + **HTTP 202** (not 200 — grant-application work remains). `automation` role always assumed; `person` role always disallowed. If sponsor can't approve a grant → approval workflow kicks off; AU can't use that permission until approved. (ASAAU §3.4)

### AU-AID generation (client-side only, no Signify dependency) — ASAAU §3.4
Generate Ed25519 keypair → hash the public key → base64 encode with proper CESR prefix → AID. UI runs "only on the client side, in javascript" (like AWS keypair UI), forcing the user to save the private key; "a handful of lines of code in javascript that depend on a cryptography library like libsodium.js" — publishable so external devs replicate it. (ASAAU §3.4)

### Authorized-caller cache — ASAAU §3.5 / GOC §2
In-memory map: AU-AID → callable endpoints → cache date. Miss → look up `wallet_aid` in `user` table; if found and `inactive_date` NULL/future → read `grant` table → derive endpoints → cache. Hit → if cache date > 1 hour, evict & re-derive; else honor. **No public-key column needed** — direct-mode AIDs convert to public key by trivial transformation. Open question (TBD): invalidation via SSE vs internal Kafka/ZeroMQ vs 10-minute polling. (ASAAU §3.5)

### Multi-recipient encryption scheme — ASAAU §3.6 / GOC §8
Single recipient: Curve25519 **sealed box**. Multiple: generate random AES key K; `AES(K, body)` once; Curve25519-encrypt K per recipient; append encrypted-key blob:
```
encrypted msg A→B,C,D = AES(K, body·10MB) + curve25519(A,B,K) + curve25519(A,C,K) + curve25519(A,D,K)
```
Each recipient finds the suffix it can decrypt, recovers K, decrypts body. Library: **libsodium (NaCl)**. (ASAAU §3.6, GOC §8)

### Alias-generation algorithm — HWGA §Method
Single-sig pattern (English): `{shadow}{who} as {role}{ctx_suffix}{variant}{caveat}`
Multi-sig pattern: `{shadow}{who} (group) as {role}{ctx_suffix}{variant}{caveat}`
- **who** = user's full name (from `user.firstName`/`lastName`) if a facet of the user; else org's friendly name (`organization.name`).
- **role** = role's friendly name from cell DB.
- **ctx_suffix** = empty if global; else "at {name}".
- **caveat** = empty if own alias; else "?" (unverified) or " (verified)" — verified only after challenge/response or credential proof.
- **shadow** = ⬤ (U+2B24) in shadow mode; else empty.
- **variant** = random "A"/"B"/"C" only to disambiguate identical aliases in the same meeting; never for logic.
Examples: "Cecilia as user at Origin"; "Cecilia Garrón as CEO at Acme" / "…como Director General para Acme"; remote unverified "Cecilia as CEO at Acme?" → "…(verified)" after seeing her OOR vLEI; "Acme (group) as legal entity"; "Acme (group) as signer of telecom traffic." (HWGA §Examples)

### Auto-selecting the right AID+alias without asking — MA §5
Role rules in workflow definitions (task requires a specific role, e.g. a `qar`) + known beneficiary let Origin pick the correct AID+alias **~95% of the time without asking the user**. The other ~5% = genuinely ambiguous operations (signing a loan is valid as private individual OR as CEO); the system knows when it's ambiguous and asks a question that "will actually make perfect sense," showing aliases as options. vLEI issuance is always in the 95% (GLEIF rules are specific). (MA §5)

### Automatic introductions — MA §7
Origin auto-introduces AID+aliases within an org where collaboration is predictable (all employees ↔ CEO; all LARs ↔ each other; LARs ↔ QARs). Eliminates contact-list busywork. But auto-introduce ≠ auto-prove.

### Caching strategies ADR (ACS) — deployment-specific tradeoffs
- **Default = Classic Caching** (TTL-based synchronous, Caffeine): fine for standard UI services where occasional minor delay is acceptable.
- Problem: high-throughput signing/verification services saw **100–200ms latency spikes** when a cache entry expired and the thread blocked on a synchronous DB/user-mgmt lookup. Traffic profiles: **Heavy Hitters** (24/7, 10–100 RPS), **Shift Workers** (bursty), **Infrequent Visitors** (~1 req/day — spike almost every request).
- **Decision = Proactive Refresh-Ahead Caching with Scheduled Forced Updates** for latency-critical (signing/verification) services. Balances zero latency spikes / security (revoked perms not cached indefinitely) / stability (no DB overload for inactive users).
- Mechanisms: Caffeine `refreshAfterWrite` returns stale value at 0ms + triggers background refresh (isolated `AuthCacheRefresh-` thread pool); `@Scheduled AuthCacheRefresher` force-refreshes all active keys to close the between-shifts revocation gap.
- Security/eviction: revoked user → CacheLoader catches AuthorizationException → returns null → Caffeine evicts key. Non-existent org-id → null → never cached (**"Self-DDoS protection"**). DB transient error during background refresh → Caffeine swallows, retains old value (stays operational).
- Observability: `Average Period = force-refresh-ms / cache_size`; if below `min-refresh-period-ms` (default 1000ms) → WARNING. Config knobs: `ttl-ms` 180000, `refresh-ms` 60000, `force-refresh-ms` 180000, `request.expiration-seconds` 30, `offset-seconds` 2.
- **Architectural rule:** "Whenever introducing a more complex caching mechanism, the system must retain fallbacks to the previous, simpler variants." Evolution path: first batch/bulk the refresh query, keep classic TTL as an option. (ACS §6)

---

## 7. Deployment-specific tradeoffs & simplifications (applied-KERI)

- **Direct-mode AU-AIDs deliberately drop KEL/witnesses/rotation** — the platform trades away KERI's full key-management power for AUs to gain "lightweight" portability (Req 2.4) and zero KERI-knowledge dependency. Explicitly reversible: "One of the benefits of using AIDs as identifiers is that we could change this decision in the future." (ASAAU footnote 4)
- **Why two identifiers (UUID + AID) instead of just the AID:** keeps human and AU identification rules uniform (else "data integrity constraints and replication policies would have to be different... more code to write, debug, test, and maintain"); AUs may need privacy from other tenants ("to prevent tenants of Origin from observing and correlating what other tenants do"); human-vs-AU boundary "may get messy over time." (ASAAU footnote 2)
- **Portability requirement (2.3):** solution must work in customer-colocated cells with no global internet — "we can't derive security from Cognito or similar services that depend on global internet access" — and interoperate with the KERI/WOT ecosystem and ToIP Trust Spanning Protocol.
- **Sameness rules for AUs** (ASAAU §3.2): two instances are "the same" only if same user ID or same AID; different software / different device / different human controller ⇒ different AU (different risk profiles, different accountability). Same software+device+controller across restart/data-evolution/IP-change ⇒ same AU. OS change: patch = same; Mac↔Windows = different. Swarm/cluster acting as a unit is a possible exception.
- **1-to-N humans:AIDs, 1-to-1 humans:UUID:** N includes zero (users tracked before they can handle keys, before/without wallets, for invitations); N>1 for identity facets. (ASAAU comparison table, §3.3)
- **Beyond cells / external security:** Provenant's own emails/SMS signed (DKIM, SPF, DMARC) so Provenant can't be impersonated; plus vault, DNSSEC, UI key-material isolation. (OS §5)
- **Known implementation gaps/divergences to watch** (GOC §15): services using JWT/OAuth instead of RFC 9421; centralized approver instead of decentralized sponsors; no AU model; weak/hardcoded nonces (no timestamp check); missing cache invalidation; incomplete key rotation; missing revocation endpoints; TLS-only cross-cell (missing Curve25519); wild-open CORS in dev/staging. These are the concrete outsider-tells the platform tells reviewers to flag.

---

## Selected exact quotes (≤25 words, with citation)

- "assume everything — outside OR inside the perimeter — is unsafe until proven otherwise." — OS §1 (Philosophy)
- "If our business grows, we will eventually be hacked." — OS §1
- "too much trust depends, with flawed alignment, too much effort, and too little justification, on what was (supposedly) guaranteed at a perimeter." — OS §1
- "When you combine these 'solutions', you get the worst of all worlds, not the best." — OS §1
- "end-verifiability (cheap but thorough verification anywhere, with minor staleness concerns and no need for expiration, rather than opaque and perishable tokens)" — OS §4.1
- "We do not use sessions, cookies, tokens, JWTs, OAuth, OIDC, SAML, or any similar technologies to secure calls to Origin." — ASAAU item 0
- "We achieve high security by making everything verifiable by anyone (and actually doing that verification)" — ASAAU §2.2
- "The walls of a pipe may be a secure perimeter, but every place where a pipe ends is a gap." — ASAAU §3.6
- "Secure pipes protect data in motion, but not data at rest." — ASAAU §3.6
- "By signing everything, we eliminate the possibility that a man in the middle could tamper. However, signing can't prevent eavesdroppers." — ASAAU §3.6
- "No KERI or ACDC knowledge is required to act as an AU or to authenticate an AU." — ASAAU §3.3
- "A sponsor is not an approver of the AU, but rather an introducer of it." — ASAAU §3.4
- "the hard problem with combining cryptography and identity is not technological — it's UX." — MA intro
- "the US government spent nearly \$1M on this UX problem... and KERI does little to help." — MA intro (paraphrase-adjacent; quote: "KERI does little to help")
- "It can prove property A without relying on an external system like a database or a blockchain." — MA §1
- "This is one of the unique features of KERI." — MA §1 (re: autonomic self-service proof)
- "ALIASES ARE NOT UNIQUE... THEY MUST NEVER BE PARSED FOR MEANING, AND THEY MUST NOT BE TREATED AS IDENTIFIERS." — MA §2
- "introducing is not the same thing as proving there is no man in the middle." — MA §7
- "AU does not mean AI." — ASAAU §3.1
- "Witnesses checking for and reporting duplicity. Super watcher." — OS §4.2
- "it's not worth using inside a k8s cluster, because if an attacker is inside... other vulnerabilities will be exploitable anyway." — ASAAU §3.6

---

## Gaps / not covered
- OS doc is explicitly WIP past §4.1.2: §4.2 (duplicity detection), §4.3 (encryption), §4.4 (SAIDs) are stubs/one-liners; §3 subsections have placeholder `<details: tables, diagrams>` and unfilled "ways to get inside" lists. Deep witness/watcher/juror/judge mechanics are NOT elaborated here.
- **Watcher / juror / judge / EGF / IPEX / edge operators / KERL / TEL / SAID** terminology is largely *absent* from these deployment docs — they reference KERI concepts (witnesses, duplicity, delegation, prerotation) but don't define the full KERI vocabulary. SAIDs mentioned only as "self-addressing identifiers on data prevent tampering" (GOC §9, OS §4.4 stub).
- Referenced-but-unread docs that would deepen this: `data-in-origin.md` (audience/movement detail), `users-orgs-permissions-and-capacities-in-origin.md` (roles/grants/automation role), `workflows-in-origin.md`, Sam Smith's BADA-RUN HackMD, the GCD public-schema.
- Cache-invalidation mechanism is an open TBD in the primary doc (SSE vs Kafka vs polling) — not resolved.
- The relationship between the `wallet_aid` field and the "X-as-Origin-user" alias for *human* users vs AUs is flagged as uncertain even by the author (ASAAU footnote 3).
- No coverage of actual cryptographic threat quantification, PQ specifics, or how prerotation is operationalized for transferable (non-AU) AIDs — the docs assert prerotation as a benefit but don't work an example.
