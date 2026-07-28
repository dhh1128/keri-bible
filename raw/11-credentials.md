# ACDC in Practice — SEDI, GCD, vLEI, and the general-purpose credential corpus

Doctrine-mining notes from two ACDC schema repos:
- `bakobo/schema` — general-purpose ACDC schemas (GCD + the SEDI family), a hard-fork of `provenant-dev/public-schema` at commit `8db57eb`.
- `public-schema` (provenant-dev) — vLEI, telco/tn, org-vet, brand-owner, bindkey, proof-of-control, citation, FAA, dossier-base.

These are the *applied* face of ACDC: what real schemas enforce, what they leave open, and the design doctrine authors wrote down while making those calls. Citations give file path + section heading.

---

## 1. What an ACDC credential fundamentally IS (as embodied by these schemas)

### The ACDC envelope is fixed and sacred
Every credential carries the fixed field set `v / d / u / i / ri / s / a / e / r` (version, SAID, blinding nonce, issuer AID, registry, schema SAID, attributes, edges, rules). House style: **"Never restyle the ACDC envelope … fixed by ACDC. Their terseness earns its keep (universal, and in the compact form they are all that ships)."** (`bakobo/schema/docs/style.md` §Rules 5). Domain fields (members of `a`/`e`/`r` beyond the envelope) use camelCase and appear only in the *expanded* form, "so their verbosity costs nothing on the wire" (same).

### `$id` is a SAID — content-addressed, self-certifying schemas
"**`$id` is a SAID.** It is derived from the saidified schema content. Edit content → the SAID changes → `registry.json` and any credential referencing the old SAID must be updated. **Never invent or hand-patch a SAID.**" (`bakobo/schema/KNOWLEDGE_TRANSFER.md` §Hard facts). `registry.json` is "the crawl-free index of released schemas (`SAID → path`)" — discoverability "without crawling" (`README.md` §What's here). keri is the pinned "SAID oracle."

### The compact/expanded `oneOf` pattern (graduated disclosure at the structural level)
"Each block (`a`, `e`, `r`) is either a SAID string (compact) or the full object (expanded). Preserve both arms." (`KNOWLEDGE_TRANSFER.md` §Hard facts 3). This is *the* recurring shape: every disclosable block is `oneOf(block-SAID, block-detail)`. A withheld field travels as its bare SAID; a revealed one as the full object. The verifier hashes disclosed blocks, substitutes withheld SAIDs, and recomputes the parent's `d` to confirm authenticity (`sedi-id/index.md` §Selective disclosure).

### Two graduated-disclosure mechanisms: attribute (`a`) vs aggregate (`A`)
The single most reusable design doc in the corpus. Both blind each withheld field with a per-block nonce "so its value can't be brute-forced from its SAID" (`docs/choosing-attribute-vs-aggregate.md` §The two mechanisms). They differ in top-level block shape:
- **Attribute section (`a`)** — a **labeled field map**; each attribute a nested block under a meaningful key (`a.dob`, `a.residenceState`). "Field labels are public (they're in the schema)." → **partial disclosure.**
- **Aggregate section (`A`)** — an **ordered array of unlabeled blinded blocks, committed by a zeroth-element AGID**. "The block labels live *inside* each block, so they're blinded; array position is arbitrary." → **selective disclosure.**

**The deciding question:** *"Does hiding the field labels or positions buy you anything?"* (§The deciding question). The only thing the aggregate provides is that its blocks carry no outward labels, valuable in exactly two cases: (1) "the presence or identity of a field is itself sensitive"; (2) "the field set is variable or homogeneous." Otherwise the aggregate is **"pure cost, because you lose label-based pathing"** — graduated-disclosure negotiation (apply/offer path lists via keri's `Pather`) "wants to name a field as `a/residenceState`. In an aggregate you can't." Rule of thumb table (§The rule of thumb):
- fixed set of heterogeneous, meaningfully-labeled attributes → **attribute `a`** (labels are the natural handle)
- homogeneous vector you disclose a subset of → **aggregate `A`** ("matches mDL, upgrades to a sparse Merkle tree")
- set where *which fields are present is itself secret* → **aggregate `A`** (label/position blinding hides the shape)

Caveat worth quoting: **"Attribute-form partial disclosure forces the issuee (`a.i`) and the `a`-section metadata to be revealed on any disclosure; an aggregate can disclose one element with no issuee."** (§Caveats).

---

## 2. Edges, chaining, and the operators (I2I / NI2I)

### Edges are typed pointers with operators that bind identity
An edge names a far node by SAID (`n`), pins the required schema SAID of that node (`s`, often `const`), and carries an operator `o`. The two operators seen:
- **`I2I` ("Issuer-To-Issuee")** — holds only when *the issuer of this ACDC equals the issuee of the node the edge points to*. Quoted from GCD schema: "Operator indicating issuer AID of this ACDC MUST be the Issuee AID of the node this Edge points to." (`gcd/gcd.schema.json` e.issuer.o).
- **`NI2I` ("Not-Issuer-To-Issuee")** — the far node need not be issued to this issuer (used when a guardian points at a ward's credential the guardian did not receive).

### I2I as same-holder binding — the presentation pattern
The sharpest doctrinal statement is in `sedi-present-age-portrait/index.md` §What the schema enforces: **"I2I holds only when the issuer of this presentation is the issuee of the credential the edge points to … it is what distinguishes 'Alice presenting *her own* credentials' from 'two credentials that merely share an AID,' which anyone could assemble."** In a holder-issued presentation the holder is the *issuer* and is the issuee of both source credentials, so I2I edges to both are the same-holder proof. A non-I2I operator is rejected (`const "I2I"`).

### Why sedi-age has NO edge to sedi-id (a subtle chaining trap)
"An `I2I` edge from `sedi-age` to `sedi-id` would hold only if the issuer of `sedi-age` equalled the issuee of `sedi-id` — i.e. only if the *holder* self-issued the age attestation, which would carry no state endorsement. So `sedi-age` carries no edge to the root." (`sedi-age/index.md` §Why there is no edge). The same-holder binding is instead established at *presentation* time by a holder-issued presentation whose I2I edges point at both sources. **Doctrine: don't force an edge whose operator semantics you can't actually satisfy; bind at presentation instead.**

### vLEI chaining: the AUTH/OOR/ECR ladder
vLEI shows real multi-hop chaining with schema-pinned edges:
- **Legal Entity vLEI** (`ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY`) has edge `qvi` → the QVI credential, with `s` const-pinned to the QVI schema (`legal-entity-vLEI-credential.json` e.qvi.s).
- **ECR Authorization vLEI** (issued by a Legal Entity to a QVI to authorize an ECR credential) has edge `le` → the LE vLEI credential, `s` const-pinned to the LE schema SAID (`ecr-authorization-vlei-credential.json` e.le.s). Chain: QVI → LE → AUTH → (role credential).
- Attribute `AID` = "AID of the intended recipient of the ECR credential" — the auth credential names the future issuee.

### Edges ≠ constraints (a load-bearing distinction in GCD)
GCD's `proofs` constraint "identifies schemas for proof requests … *This constraint should not be confused with ACDC edges (chained credentials), which justify the delegator's status in the first place, and which are the SAIDs of concrete credentials rather than identifiers of schemas which could satisfy a constraint.*" (`gcd/index.md` §Constraints, proofs bullet).

---

## 3. GCD — Generalized Cooperative Delegation (the crown jewel)

### What GCD is and is NOT
"The delegation relationship itself is **not embodied in a credential**, but rather in a special delegate AID bound to the delegator's AID via an inception event on the delegate side, and an interaction event in the KEL on the delegator side … This interlocking two-way binding is what gives rise to the term 'cooperative delegation,' and it is significantly more secure and flexible than many other delegation mechanisms." (`gcd/index.md` §Purpose). **The AID binding proves the *state* of the delegation and how it's controlled; it does NOT say which actions are expected or what constrains them — that is GCD's job.**

### Authority is always proved by a signature
"In the digital world, authority may be asserted in many ways, but it is always proved by a digital signature. A delegate always signs something … The fact that they've signed is easily verified; the question GCD credentials answer is whether the delegate had the authority to act." (§Types of authority). Contrast the physical world where affordances constrain (a vault key can't sign a treaty) — digital signatures have no such natural affordance limits, so constraints must be explicit.

### The v2.0 shape: named containers, not flat prefixes
`a` block holds `facet` (descriptive) + `constraints` (gating) + siblings `terminatingEvents` (voiding) + `disclosables` (outbound). `r` block holds five disclaimers + first-class `duties`.

**`facet`** (descriptive, forward-compatible, NOT fail-closed — "Unknown keys here are safe to ignore"):
- `role` — a label; **has NO enforceable semantics unless `gfw` is defined** (rule `noRoleSemanticsWithoutGfw`).
- `relationType` enum: `delegation` (delegate acts for a *self-sovereign* delegator) / `guardianship` (acts for a *non-sovereign dependent*) / `controllership` (acts *over a thing*) / `stewardship` ("guardianship's fiduciary posture applied to a domain the steward runs as their own"). (schema facet.relationType.description).
- `liableParty` — "Who answers OUTWARD if an act … goes wrong — the party the world holds responsible … distinct from the grantor (issuer i), the beneficiary (relationType), the actor (the delegate), and the inward accountability expressed by the duties." (renamed from the paper's `obligationBearer`).
- `presentsAs` — "The facet-AID the act is presented under … **Presenting-as without this granted capability is impersonation. The signer is always the actor's own key; presentsAs governs only the presented identity, not the signature.**"
- `exerciseMode` enum: `act` (authority-to-act) / `authorize` (authority-to-authorize — the pure delegator, empty goals, sanctions others' acts but performs none) / `both`. **"authority-to-act vs authority-to-authorize as independent axes."**

**`constraints`** — the enabling "may", **FAIL-CLOSED** (`additionalProperties: false`): an unrecognized key here MUST deny. Fields (each optional; absent = that dimension unconstrained):
- `goals` — Hyperledger Aries goal codes, matched with implicit trailing `.*` wildcard, case-insensitive.
- `acts` — **the (effect, state-kind) points a delegate may act on.** effect ∈ {observe, create, modify, preserve, destroy}; state-kind ∈ {info, record, commitment, authority, resource, relationship}. **"the two axes of one coordinate, neither meaningful alone"** — "'create' is create *what*, 'commitment' is do *what* to it." Entry syntax: `"create commitment"`, or one-sided brace enumeration `"observe {info, record}"` / `"{create, modify} record"`. Two-sided braces and wildcards intentionally forbidden. "An act is authorized only if **every** (effect, state-kind) point it occupies is covered" (filing a return is `create record` AND `create commitment` in one move). The gate (auto/rule/human) is **derived** per act via `gfw`, not enumerated.
- `domains`, `jurisdictions` (ISO 3166), `physGeos` (strong presence test), `virtGeos` (weak geolocation), `icals` (RFC 5545 fragments), `monetaryLimit`, `protos`, `proofs` (IPEX proof-request SAIDs, ORed), `validFrom`/`validUntil`, `humanReview`.
- `monetaryLimit` is **"money-locked — it is NOT a general 'stakes' quantity. Non-money or unquantifiable stakes route to the governance gate."** Pattern: magnitude + space + unit (`"25 CHF"`, `"0.3 BTC"`, `"4 OZ-XAU"`).
- `humanReview` — "**Any GCD credential that has this field MUST NOT be verified without human judgment.**"

**Boolean logic of constraints (invariant):** *within* a field values are ORed; *across* fields they are ANDed (`gcd/index.md` §Constraints rules 2–3). Consequence: **"Because of the third rule, these credentials do not support graduated disclosure. All constraints must be disclosed every time a verifier is evaluating delegated authority."** (§Constraints, closing). Authority credentials are shown *whole*.

**`terminatingEvents`** (voiding polarity, sibling of constraints): SAIDs of proof-requests for attested events; ANY one firing ends authority (OR). **"These are proof-shaped attested facts, not live predicates, so the credential's meaning stays static and any two verifiers replay to the same result."** A GCD carrying `terminatingEvents` **MUST also carry `constraints.validUntil` as a hard backstop** — enforced by JSON-Schema `if/then` (schema lines 316–332), "so a never-fired termination signal cannot leave authority alive forever."

**`disclosables`** (outbound axis): credential-SCHEMA SAIDs the delegate MAY reveal about its principal — an allow-list at schema granularity. "Intra-credential selective disclosure remains ACDC's job."

### The five disclaimers (rules block, all required) — quotable doctrine
From `gcd/rules.json` (SAID `ENiUyBCG2MjCHa9djlgHiogd6uZHECc09ZELmQ3fEMzR`):
1. **`noRoleSemanticsWithoutGfw`** — "the role field has no enforceable semantics unless the gfw field is also defined."
2. **`issuerNotResponsibleOutsideConstraints`** — you can't use the credential as proof of authority "under conditions when the constraints say otherwise."
3. **`noConstraintOutsideConstraints`** — "**enforceable constraints exist only inside the constraints container** … Nothing outside … constrains … and an unrecognized key inside the constraints container MUST be treated as fail-closed." (Renamed from `noConstraintSansPrefix`.)
4. **`useStdIfPossible`** — express constraints in the predefined way, not in notes/custom fields, "so verifiers can be confident that when one of the pre-defined constraints is absent, delegated authority is unconstrained in its corresponding dimension."
5. **`onlyDelegateHeldAuthority`** — "Issuers agree to only delegate authority that they reasonably believe they hold."

### Duties (the "must", first-class in `r`)
"Duties are disclosure and accountability — **a stranger-verifier does not gate on them** — so they live here in `r`, not in `a.constraints`." (schema duties.description). Two shapes keyed by `bearer`: a `delegate` duty `{bearer, effect, goal, cadence?, priority}`; an `issuer` duty `{bearer, rule, l?, priority}`. Baseline ships `timelyReviewAndRevoke` — "review each delegation on a cadence appropriate to its stakes, and revoke or narrow it promptly once the conditions that justified the grant no longer hold. **This duty does not extend authority.**" `priority` is for "fail-loud conflict resolution: … ties escalate rather than being silently dropped." **The reciprocal "must" is the GCD's own `r`-block, not a second credential.**

### gfw — governance framework hook
`gfw` is a SAID naming a supplemental rules block. "When defined, a verifier MUST NOT impute a delegator's approval of delegated authority to a delegate without understanding and enforcing the rules of these extra rules." (schema a.gfw.description). "The act of issuing or receiving a GCD credential constitutes binding acceptance of the rules." (`gcd/index.md` §Governance) — recurs verbatim across org-vet, citation.

### GCD worked examples (the gallery — each SAID-minted and linter-validated)
`gcd/examples/` (from `gcd/index.md` §Worked examples):
- **real-estate-agent** (delegation/act): goals, jurisdictions + physGeos, monetaryLimit, proofs (license), a delegate duty.
- **guardian-of-minor** (guardianship/both): humanReview, terminatingEvents (reached-majority) with validUntil backstop, disclosables, presentsAs. (Actual JSON: `acts` uses one-sided braces `"observe {commitment, resource, relationship}"`; `monetaryLimit: "10000 USD"`; both an issuer `timelyReviewAndRevoke` duty and a delegate `preserve care.medical` duty.)
- **ai-deploy-agent** (delegation/act): containment via no-`destroy` effects, domains, cloud-spend monetaryLimit, 30-day window, kill-switch terminatingEvent, humanReview for prod, restrictive disclosables allow-list. **(AI-agent delegation is a first-class use case.)**
- **platform-manager** (stewardship/authorize): the pure delegator — **empty `goals`**, issuer-only duties, no gfw so `role` is a bare label.
- **iot-fleet-controller** (controllership/both): authority over a *thing* — icals maintenance windows, virtGeos, protos, decommission terminatingEvent.

---

## 4. SEDI — Self/State-Endorsed Digital Identity (the applied privacy doctrine)

### Founding inversion: the state endorses, it does not create
"SEDI's founding premise inverts the usual state-ID relationship: identity is *'innate to the individual's existence and independent of the state… fundamental and inalienable'* (§63A-20-101(1)). **The state endorses an identity; it does not create one.**" (`sedi-id/index.md` §Purpose). Mechanics: the issuer field names the State, but "the subject is bound by the holder's own personal digital identifier (a KERI AID) — **withdraw the endorsement and the identity persists, because the holder, not the state, holds the key.**" This is the KERI root-of-trust (key holder = controller) applied to civil identity.

### Minimalism enforced by schema, not policy
The statute lets the department endorse "**exactly four attributes — name, birth date, image, and Utah residence address**" and forbids collecting anything unnecessary. "`sedi-id` carries those four and nothing more; everything richer … is a *separate* credential that chains to this one." (§Purpose). This is deliberate: keep the root minimal, push richness to chained credentials.

### Decomposition for minimization (a schema-level privacy teeth)
Name and residence are split into **separate nested blocks** — "decomposed is the *sole* production shape." "Because a block discloses atomically, a single residence block would force over-disclosure on every verifier who only needs jurisdiction, **making the statute's minimization duty … un-satisfiable at the schema level.**" (§Name and residence). Keep the street line whole (parsing PO boxes/rural routes is brittle) but split city/state/postal/county. **"Prove Utah resident" without the street line** protects at-risk voter classes (DV victims, LEOs). Naming is "**semantic interop, not field-name interop**" — align component semantics with ISO 18013-5 mDL but keep the statute's vocabulary ("residence" not "resident"). Labels are flat and **dot-free on purpose** — "a dotted key like `residence.street` signals a nesting the model doesn't have and is a cross-tooling footgun in jq/JSONPath/JS/MongoDB."

### Image: committed by digest, bytes holder-carried
"The `image` block carries a content digest plus minimal metadata … the actual portrait bytes are **holder-carried** and attached to a presentation under chain-link confidentiality, verified against the digest." A **download locator was rejected** — "it breaks mandatory offline presentation …, is phone-home by another name …, and creates an availability chokepoint." Inlining raw bytes rejected as bloat. (§Image). **Anti-pattern flagged: a resolvable URL in a credential is "phone-home" surveillance and an availability single-point-of-failure.**

### sedi-age: the aggregate done right
Homogeneous boolean vector `ageOver13/16/18/21/55/65`; element 0 is the **AGID** committing to every block's SAID. Holder reveals only the block(s) needed. "This is exactly the ISO mDL `age_over_NN` model … a poor man's sparse Merkle tree" — leaves room to upgrade to a sparse Merkle tree with no schema change (`sedi-age/index.md` §Why an aggregate). Directly satisfies statutory "**prove a minimum age without disclosing age or birth date**" (§63A-20-301(1)(e)). "A genuine zero-knowledge alternative to a predicate proof … keeps the birth date out of the transaction entirely, with no special cryptography." `asOf` records the point-in-time posture (no continuous monitoring).

### sedi-guardian: holder ≠ subject (the anti-impersonation invariant)
**"The single most important rule … is that the guardian holds the credential and the ward is named only by edge."** (`sedi-guardian/index.md` §The load-bearing invariant). The issuee (`a.i`) is the *guardian*; the ward is a `subject` edge to the ward's `sedi-id`. "This is what keeps guardianship *transparent* representation, never impersonation … **Collapsing the two (guardian-as-subject) is the classic impersonation/commingling failure the whole field warns against.**" Prior art cited: Sovrin *Guardianship in SSI V2*, Aries RFC 0103 "Indirect Identity Control." Four machine-checkable statutory `basis` values (courtGuardianIncapacitated / courtGuardianMinor / custodialParent / designatedRepresentative). "Scope must be explicit" — `powers` required (`plenary` or an enumerated limited set); "a medical-only guardian is not authority for a financial act." **Registry-bound (`ri` mandatory): "guardianship terminates dynamically (majority, restored capacity, death, court order), so a verifier MUST check current status, not just the signature and dates."** Two-layer factoring: **GCD for the generic relationship machinery, sedi-guardian for the legal specifics** (reachable via optional `scope` edge → a GCD with `relationType: guardianship`). Supported-decision-making supporters are *deliberately excluded* — "a supporter cannot decide *for* the principal."

### sedi-present-age-portrait: holder-issued presentation as a named pattern
Holder is the *issuer* (Discloser), verifier is the *issuee* (Disclosee). "The presentation does not copy any identity data; it **references** the holder's two source credentials by SAID through I2I edges." **Deliberately NOT registry-bound (`rd` disallowed via `additionalProperties: false`): "a one-time presentation is not logged, which is what keeps the state (and anyone else) from correlating where and when the holder presents."** Doctrine on why it's a schema at all: "'Bespoke' describes an *issuance pattern* … not a credential *type* — so there is no useful generic 'bespoke' schema. What *is* reusable is a **named verification pattern**." "The club's accepted shape and the holder's issued presentation are **one schema viewed from two sides**"; the verifier's request stays an IPEX `apply` query.

### IPEX presentation flow (gated disclosure)
"runs as a gated IPEX exchange (`apply → offer → agree → grant → admit`): the verifier accepts the governance terms (a signed `agree` referencing the presentation's SAID) **before** any PII … crosses the wire, and a decline never opens the gate." (§Presentation flow). The photo is delivered as a *partial* disclosure of just the `image` block (attributive), the over-21 flag as a *selective* disclosure of just `ageOver21` (aggregate). Executable reference: keripy `tests/acdc/test_clc_disclosure.py`.

### SEDI governance framework (chain-link confidentiality in force)
`sedi-id/rules.json` (SAID `EA5O9z0TB932sm8kJIVdAIpwLpEWRWC5--VNS5r69frn`), referenced by SAID from every SEDI credential's `r`. Key clauses (each grounded in Utah Code):
- **`chainLinkConfidentiality`** — verifier MUST NOT "assimilate, aggregate, correlate, sell, or otherwise combine disclosed attributes … for any purpose beyond the disclosed purpose. **This binds each downstream recipient reached through the edge section of a presentation.**"
- **`dataMinimization`** — MUST honor selective disclosure "rather than requiring fuller disclosure."
- **`noSurveillance`** — no using a presentation "to enable monitoring, surveillance, profiling, tracking, or persistent correlation."
- **`noDeviceSurrender`**, **`respectRevocation`** (revoke only on statutory grounds: compromise, error/fraud, holder request), **`safeHarbor`** (accepting the presentation = electing the statutory safe harbor; breach forfeits it and is evidence).
- **`noOverAssertion`** — "the state endorses only name, birth date, image, and Utah residence address … derived credentials assert only their stated claim."
"Issuing or accepting a SEDI credential is binding acceptance of it." (`sedi-id/index.md` §Governance).

---

## 5. Anti-patterns and outsider-tells the corpus explicitly corrects

- **Resolvable/download URLs in credentials = "phone-home by another name"** — availability chokepoint and surveillance vector; images are committed by digest and holder-carried instead (`sedi-id/index.md` §Image).
- **Registry-logging a one-time presentation** = a correlation leak; presentations are deliberately un-registered (`sedi-present-age-portrait/index.md`).
- **Dotted JSON keys implying nesting the model lacks** = "a cross-tooling footgun" (`sedi-id/index.md`).
- **Guardian-as-subject (collapsing holder and subject)** = "the classic impersonation/commingling failure the whole field warns against" (`sedi-guardian/index.md`).
- **Treating a Citation/reference as an endorsement** — "Verifiers MUST NOT make this mistake." A citation "embodies a cryptographically provable reference by the issuer, and nothing more. It MUST NOT be construed as an endorsement." Citations are meaningful only when contextualized by a *referencing* ACDC's edge (`citation/index.md` §Semantic precision). The same signature-≠-endorsement care applies broadly.
- **Existence of a citation ≠ truth of the cited proposition** — the ACDC validation algorithm ("fetching key state, verifying a signature, testing revocation, and comparing data and structure to a schema") "can prove that an issuer remains committed to a citation — but only the interaction context … plus governance, plus possible validation external to the world of ACDCs" establishes what proposition is true (`citation/index.md`). **Clean statement of what cryptographic verification does and does NOT prove.**
- **Confusing constraint-schemas (`proofs`) with edges (concrete chained credentials)** (`gcd/index.md`).
- **Assuming a signature proves affordance-limited authority** — digital signatures have no natural affordance limit (unlike a physical vault key), so authority must be constrained explicitly (`gcd/index.md` §Types of authority).
- **Role labels as if self-describing** — a `role` string carries *no* enforceable meaning without a `gfw` (`noRoleSemanticsWithoutGfw`).
- **presentsAs without the granted capability = impersonation** (GCD schema).
- **Forcing an edge whose operator can't be satisfied** — sedi-age deliberately omits the edge to sedi-id because I2I would not hold; bind at presentation (`sedi-age/index.md`).

### Foreign-artifact bridging (FAA) — the "not-a-CA" interop stance
FAA "gives non-ACDC data the attributes needed to participate fully in an ACDC data graph … an efficient, tamper-evident envelope with predictable metadata." Explicitly lists the *other* ecosystems ACDC bridges rather than adopts: "X509 certs, W3C VCs, SD-JWTs, AnonCreds, ISO mDOC/mDL, remote attestations …, various flavors of signed PDF" plus physical artifacts (`faa/index.md`). Tamper-evidence via **hash/SAID → CESR-encoded digest** in `art_digest`. **"In and of itself, a FAA makes no claim about the *meaning* or *significance* of its artifact."** Notable fields: `art_posture` (did the issuer merely record the digest, witness the artifact directly, or verify its integrity?) and `rev_latency` (does the FAA issuer track and mirror the foreign credential's revocation, and how fast?) — a bridge issuer with non-zero `rev_latency` "allows verifiers to treat the FAA as a proxy for the foreign credential, assuming they trust the FAA issuer." **Trust in a bridge is explicit and issuer-scoped, not systemic.**

---

## 6. Levels of assurance (org-vet) — LoA as verifier-chosen threshold, not CA hierarchy

`org-vet/index.md`: LoA is "a positive number, where larger numbers map to higher levels of assurance." **"This allows verifiers to decide what level of assurance will satisfy them, and accept any credential having an LoA ≥ their threshold."** Ladder: 1 bronze (basic proof of control + DNS record claiming the AID), 2 silver (cryptographic control + legal accountability, eIDAS substantial / NIST IAL2, GCD/delegated-AID authorization proof, ≥1 witness), 3 gold ("legal signing authority … multisig signing committee … a ceremony where it is proved that there is **no MITM between any two members** of the signing committee, and … at least one external observer … **enough witnesses to reliably detect and recover from duplicity**" — maps to GLEIF LE vLEI). **Duplicity detection-and-recovery, MITM-freeness, and external observers are the LoA-3 primitives — a KERI-native reframing of CA "high assurance."** "The LE vLEI is essentially an org-vet credential at LoA 3." bindkey exists precisely because some ecosystems (SPF/DKIM/DMARC) demand RSA keys KERI wouldn't otherwise control: "We don't really want identifiers to be controlled by RSA crypto, but it could be useful for orgs to announce … they are using an RSA key" (`bindkey/index.md`).

### proof-of-control — "parties are only identifiers; there is no 'man' to impersonate"
"As far as the semantics of these credentials are concerned, issuer and issuee are simply identifiers that resolve to cryptographic keys … **Because of this primitive perspective, many of the common man-in-the-middle attacks … are out of scope … there is no 'man' to impersonate**" (assuming robust identifier-to-key resolution) (`proof-of-control/index.md` §Parties are only identifiers). Combining with an identity credential (via common issuee) re-introduces MITM, which the identity credential must then handle. Security stance is explicitly **assumption-relative**: "Issuers should make reasonable efforts to ensure that certain assumptions hold … Verifiers should judge their confidence … with these assumptions in mind." Challenge/response over "any secure or insecure channel" using unpredictable entropy; data-source (writable only by controller) vs data-sink (readable only by controller) split. Known limitation: an issuee colluding with the real controller "is indistinguishable from the real controller … Proof-of-control credentials don't distinguish these cases."

---

## 7. What real schemas ENFORCE vs leave OPEN (the negative corpus)

The repos validate a "should-reject" corpus in CI — schema teeth made explicit:
- **GCD** rejects (`gcd/invalid/`): bad `effects`/`stateKinds` enum, **unknown key inside `constraints` (fail-closed)**, `terminatingEvents` without a `validUntil` backstop, `exerciseMode: delegated-only` (a rejected pre-reconciliation token), malformed `monetaryLimit`, unknown duty `bearer`, delegate duty missing `effect`, non-integer duty `priority`, two-sided brace in `acts`, unknown `acts` token.
- **sedi-id** rejects (`sedi-id/invalid/`): top-level extra prop, missing `a`, missing issuee, missing required attribute, block extra prop, **block missing its blinding nonce**, non-date `dob`, image missing `digest`, non-string `residenceState`.
- **sedi-age** rejects: extra top prop, missing/mistyped `A`, block extra prop, block missing nonce, non-boolean `ageOver21`, malformed `asOf`.
- **sedi-present-age-portrait** rejects: registry-bound (`rd`) presentation, missing `r`, **non-I2I edge operator**, missing edge block, missing/non-boolean `ageOver21`, edge missing far-node SAID, malformed `occurredAt`.
- **sedi-guardian** rejects: missing/mistyped `basis`, empty/bad `powers`, `recognition` missing a required field or bad `authorityType`, bad edge operator, malformed date.

**Left OPEN by design:** GCD's top-level `additionalProperties: true` (extension is allowed *outside* constraints, but by the disclaimers such fields *don't constrain*); `facet` is open/forward-compatible (unknown keys safe to ignore) while `constraints` is closed/fail-closed — **the open-vs-closed choice tracks descriptive-vs-gating.** FAA explicitly: "Implementers MAY define additional fields in the `a` section." Custom governance frameworks via `gfw` and rule override via a different `r` value are open extension points, but issuing/accepting = binding acceptance.

---

## 8. Cross-cutting design doctrine (reusable rules of thumb)

- **Fail-closed where a verifier gates; forward-compatible/safe-ignore where it merely describes.** `constraints.additionalProperties=false` vs `facet` open.
- **Authority/legal credentials are disclosed WHOLE; identity/attribute credentials support graduated disclosure.** (GCD, sedi-guardian whole; sedi-id/sedi-age selective.) Because ANDed constraints or basis+scope+validity are only meaningful together.
- **Extract-at-the-second-pattern discipline:** don't build a shared base schema (e.g. `presentation-base`, `sedi-legal-authority`) until a *second* real instance proves the shared shape (`sedi-present-age-portrait/index.md`; `sedi-guardian/index.md`).
- **Two-layer factoring:** generic machinery (GCD's act grid, duties, terminating events) lives once; domain-specific legal-recognition layers (sedi-guardian) carry only what law makes relationship-specific and edge into the generic layer.
- **Intent-first methodology:** "A decision not in `this.i` is not yet made" — every schema change is preceded by a recorded decision commit (`KNOWLEDGE_TRANSFER.md` §House rules). Not doctrine about ACDC per se but about how this corpus is governed.
- **Point-in-time, replayable semantics:** terminatingEvents are "proof-shaped attested facts, not live predicates, so … any two verifiers replay to the same result." Static credential meaning is a KERI value — no live oracle in the trust decision.

---

## Gaps / not covered
- I read index.md + schema + rules for the load-bearing schemas but did NOT open every `example.json`/`invalid/*.json` body (I read `guardian-of-minor.json` in full and summarized the rest of the galleries from the index tables — the invalid corpora were captured by their documented reject-reasons, not by reading each fixture).
- `this.i` (the intent tree, the authoritative decision log referenced everywhere via `@`-codes) was NOT read — it is the primary source for *why* each decision was made and would deepen every section here.
- `AGENTS.md`, `tools/py` (the SAID/linter tooling), and `../../papers/sda.md` (*The Shape of Delegated Authority*, GCD's theory source) were not read.
- Deep CESR/SAID *algorithm* detail (bytewise/externalized SAID, the `Aggor`/AGID computation) is referenced but lives in keripy, not these repos.
- public-schema: read vLEI LE + ECR-auth schemas, org-vet/tn/bindkey/proof-of-control/citation/faa indexes; did NOT read the OOR/QVI/iXBRL vLEI schemas in depth, nor tn/brand-owner/a2p-campaign/tcr-vetting/aegis-std-vetting schema bodies (telco-specific, lower doctrinal density).
