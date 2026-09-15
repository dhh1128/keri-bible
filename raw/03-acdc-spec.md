# ACDC Specification — Doctrine Mining Notes

**Primary source:** `/home/daniel/code/me/kswg-acdc-specification/spec/spec-body.md` (ToIP KSWG ACDC spec; repo `trustoverip/kswg-acdc-specification`). This file begins at "## ACDC Structure" (front-matter intro/terminology live in sibling files not covered here). Citations below are `spec-body.md §<heading>` with a line-number hint; line hints drift and are expected to.

**Pinned commits.** The spec now has two live lines and they have diverged, so every citation in this note must name its branch.

- **`main` — the standardizing line, tier `[N]` — at `f0bd097de`** (long form of the `f0bd097` pin already used in `raw/16`; `main` has not moved since that pin). 5258 lines.
- **`v1.1` — the forward line, tier `[N1.1]` — at `2362e48a1`** ("Merge pull request #214 from dhh1128/v11-parity-with-main"). 5459 lines. `v1.1` is ahead of `main` by 346 insertions / 145 deletions in `spec-body.md`.

**How to read this note.** Sections 1–20 were mined from `main` and are `[N]` unless a marker says otherwise. Sections 21–22 are `v1.1`-only and are `[N1.1]` throughout: **new thinking that is likely, not certain, to fold into the next standard.** Nothing in §21–22 may be cited as normative today. Section 23 is `[N]` material that is new to this note but already in `main`. Sections 24–25 hold negative results and unresolved tensions.

**Mining pass of 2026-09-15 — what was actually re-read, and at which pin.** Under-claimed deliberately.

- **Re-anchored at `f0bd097de` (`main`):** §Top-Level Fields, §Other Reserved Fields, §Compact Labels, §Registry SAID Field, §Universally Unique Identifier (UUID) Fields, §Edge (the unary-operator table and its following prose), §Edge-group (the m-ary operator table and its following prose), §IPEX Protocol Messages (the route table), §Registry-Dependent Issuance Lifecycle, §Graduated Disclosure (the worked examples one). These bear on note §2, §8, §14 and the new §23.
- **Read in full at `2362e48a1` (`v1.1`):** §Field Label Restrictions, §Unique Entropy (UE) Fields, §Other Reserved Fields, the whole of §Disclosure Paths and all its subsections, §Disclosure Paths in `apply` and `offer`, §IPEX Protocol Messages, the Edge unary-operator table and prose, §Registry SAID Field.
- **NOT re-read this pass, and therefore still standing at `11832a3`:** everything else in §§1, 3–7, 9–13, 15–20 of this note — SAIDification, schema doctrine, ACDC variants, attribute/aggregate mechanics, rule section, key-state binding, registrars/observers, the privacy model, TEL/blindable-state internals, bulk issuance, extensibility, CESR-native message types, cryptographic strength, and the selective-disclosure annex. The line hints in those sections predate a large growth in `main` (the note's original header recorded ~4715 lines; `main` is now 5258) and will be badly drifted.

---

## 1. What ACDC fundamentally IS / IS NOT (worldview, design intent)

- **ACDC = Authentic Chained Data Container.** Modeled abstractly as an **ordered nested field map** (`key:value`), serializable in JSON, CBOR, MGPK, or CESR — but crucially every field map MUST contain a **SAID** field, making it a **SAD (Self-Addressed Data structure)**. "One important feature of the fields maps used by ACDC is that they all MUST include a field with a SAID." (§ACDC Message Fields, L2982)
- **Type-is-schema.** "Notably, no top-level field types exist in an ACDC. This is because the Schema, `s`, field itself is the type field." (§Type-is-schema, L182). Design principle: **separation of concerns between payload data and type info — "type information is metadata, not data."** Repeated for edges/rules: "This is in accordance with the design principle of ACDCs succinctly expressed as 'type-is-schema.'" (L1130, L1283).
- **ACDCs are fragments of a globally distributed property graph (PG).** "A set of ACDCs as nodes connected by edges forms a labeled property graph." Each ACDC node is "universally uniquely identified by the SAID of its ACDC." → "securely attributed fragments of a globally distributed property graph… a global verifiable knowledge graph that crosses trust domains." (§ACDCs as secure graph fragments, L1060-1068).
- **Portable, decentralized, cross-trust-domain.** "The use of AIDs enables ACDCs to be used in a portable but securely attributable, fully decentralized manner in an ecosystem that spans trust domains." (§AID Fields, L95). "No shared or trusted relationship between the Controllers and Verifiers is REQUIRED." (L95).
- **Zero-trust / end-verifiable.** Static schema requirement is "securely end-verifiable (zero-trust) because a cryptographic commitment to the SAID of a SAIDified schema is equivalent to a commitment to the detailed associated schema itself (SAD)." (§Static Schema, L222). Extensibility section: "This is completely decentralized and zero-trust." (§Extensibility, L2934).
- **Minimally sufficient means.** Selective disclosure "does not require any more complex cryptography than digests and digital signatures or anchors in TELs or KELs… This satisfies the KERI design ethos of 'minimally sufficient means.'" (§Basic selective disclosure, L686). Trades size/verbosity for "ease, simplicity, and the adoptability of implementation."
- **Not privacy-per-se; protection from exploitation.** "the primary design goal is not data privacy protection per se but the more general goal of protection from the unpermissioned exploitation of data." (§Disclosure Mechanisms, L1659). Privacy mechanisms are means, not ends.
- **Resource-constrained by design.** Compact one/two-char labels: "the over-the-wire verifiable signed serialization consumes a minimum amount of bandwidth" for "supply chain or IoT" apps; a verbose semantic overlay can be applied AFTER verification (§Compact Labels, L58).
- **Bow-tie model of Ricardian Contracts.** SAID hierarchical commitments "support the well-known bow-tie model of Ricardian Contracts" — extended "not merely for contracts, but for all data authenticated, authorized, referenced, or conveyed by ACDCs." (L81, §Performance L2703).

## 2. Top-level structure, fields, invariants

**Top-level field order (MUST):** `[v, t, d, u, i, rd, s, a, A, e, r]` (§Field Ordering, L32).
**Required fields (MUST appear):** `[v, d, i, s]` (§Required Fields, L36). (Note: CESR-native `acm` variant lists required as `[v,t,d,i,s]`, L2970.)

Field meanings (§Top-Level Fields, L16-28):
- `v` Version String — regexable `ACDCMmmGggKKKKSSSS.` → protocol type, version, CESR genus version, serialization type, size, terminator. MUST be first field. Protocol field MUST be `ACDC`.
- `t` Message Type — 3-char; optional only for `acm` non-CESR-native; default type `acm`.
- `d` SAID of enclosing map (self-referential digest).
- `u` UUID — high-entropy salty nonce (blinding factor).
- `i` Issuer AID — control authority via KERI verifiable Key State.
- `rd` Registry Digest SAID — issuance/revocation/transfer/retraction registry (TEL) for the ACDC. (Re-anchored 2026-09-15 at `main` @`f0bd097de` L23 and §Registry SAID Field L83-85; **the nested-`rd` gloss and its "application-specific or Issuer-specific" open-endedness are byte-identical in `v1.1` @`2362e48a1` L48/L96** — see §24.1.)
- `s` Schema — SAID of JSON Schema or the block itself.
- `a` Attribute section (partially disclosable).
- `A` Attribute Aggregate section (selectively disclosable).
- `e` Edge section.
- `r` Rule section.

**Hard invariants / "never do X":**
- **`a` and `A` are mutually exclusive.** "An ACDC MUST not have both an `a` field and an `A` field." (L106); "MUST not have both a non-empty `a` value and a non-empty `A` value." (L110).
- Optional fields that appear MUST appear in the defined order (L14).
- **Insertion-ordered field maps MUST be used** for canonical serialization (not lexicographic) (§Ordered Nested Field Maps, L10).
- Schemas MUST be static/SAIDified — dynamic schema references MUST NOT be used (see §4).
- Non-local URI subschema references MUST NOT be used (not end-verifiable) (L206).
- Top-level `$id` MUST be a **bare SAID** (not a URI) (L210).

## 3. SAIDs & SAIDification (core cryptographic machinery)

- A **SAID** is "a special type of cryptographic digest of its encapsulating field map (block)." The block is a **SAD**. Using a SAID as a value = "compact but secure representation." (§SAID Fields, L77).
- **Commitment equivalence (foundational doctrine):** "A digital signature on a SAID makes a verifiable cryptographic non-repudiable commitment that is equivalent to a commitment on the full serialization of the associated block from which the SAID was derived." Requires "sufficient cryptographic strength, including collision resistance." (L81). Hierarchical: "a digest of a data block that… contains digests of yet other data blocks, makes a compact, hierarchical, verifiable cryptographic commitment." (L81).
- Special SAID fields: `d`, `rd` always SAIDs; `s`, `a`, `e`, `r` MAY be replaced by their SAID → "compact form" (L79).
- Schema SAID uses field label **`$id`** (not `d`) — repurposed JSON Schema keyword; value MUST be the schema SAID. Digest MUST have ~128-bit strength, generated per ToIP SAID draft, CESR-encoded (§Schema ID Field Label, L186-188).

### Most compact form SAID algorithm (§Most compact form SAID, L130-151)
- **There MUST be one and only one unambiguous way to compute the SAID of a compactifiable section/block** — the "most compact form" SAID. Computed by **depth-first search**: compute SAIDs of expanded leaf nodes, compact them, ascend computing enclosing-block SAIDs, until the trunk (ACDC top-level `d`).
- Verification reverses: expand a block, verify its SAID, expand enclosed blocks, verify theirs, recurse. "enables verification of portions of a set of nested compactifiable subblocks against their SAIDs without requiring that the whole tree be exposed. This is essential to Graduated Disclosure." (L136).
- Compact form of a SAIDed block "MUST appear as the first variant in the `oneOf` subschema list for its labeled field." (L140).
- The "most compact form" SAID is "what is used to reference an ACDC as the node value of an Edge or to reference a section." (L151).

### UUID (`u`) = blinding factor (§UUID Fields, L89-91)
- Without `u`, "an adversary may be able to reconstruct the block contents merely from the SAID… and the Schema… using a rainbow or dictionary attack." The power-set of schema-allowed field values may be far smaller than the digest strength. Sufficient entropy in `u` "ensures that the cardinality of the power set allowed by the schema is at least as great as the entropy of the SAID digest algorithm."
- `u` at top level → SAID blinds the WHOLE ACDC (correlation-minimizing / "privacy-preserving") (L91).

## 4. Static / immutable Schema doctrine + two named attacks

- "For security reasons, the full Schema of an ACDC MUST be completely self-contained and statically fixed (immutable)… dynamic Schema references or dynamic Schema generation mechanisms MUST NOT be used." (§Static Schema, L194).
- **Schema revocation attack:** attacker changes a dynamic schema resource → schema validation fails on all ACDCs using it → "effectively revokes all the ACDCs that use that dynamic Schema reference." (L196).
- **Semantic malleability attack** (a transaction-malleability variant): attacker "shift[s] the semantics of the dynamic Schema" so the ACDC still validates but downstream processing behavior changes. (L198).
- Prevention: "all Schemas MUST be static, i.e., Schemas MUST be SADs and therefore verifiable against their SAIDs." (L200).
- Schema dialect MUST be **JSON Schema 2020-12**. `$schema` URI is "simply an identifier" — dereferencing it for validation code "would be an attack vector"; Validator MUST control the tooling dialect; mismatch SHOULD fail validation. (§Schema dialect, L226).
- Allowed non-local reference schemes (all end-verifiable via embedded SAID): `sad:`, KERI **OOBI** URLs, `did:` (did:webs / did:keri) (L214-218).
- **Two meanings of schema "version":** `$id` (a SAID) is the "cryptographically verifiable" / "normative determiner"; `version` field (semver "major.minor.patch") is "informative" and NOT used in validation. Any change to schema → new SAID → MUST also bump `version`. (§Schema Versioning, L230-234).
- Availability ≠ security: "Unavailable does not mean insecure or unverifiable. ACDCs MUST be verifiable when available." Availability solved by redundancy; EGF may impose availability constraints (§Schema Availability, L242).
- **Composable schema:** `oneOf` for compact/expanded variants. "a composable schema is a verifiable bundle of metadata (composed) about content that can then be verifiably unbundled (decomposed) later. The Issuer makes a single verifiable commitment to the bundle." (L246). Validator uses composed base schema pre-disclosure, decomposed (compact option removed) post-disclosure to force Full Disclosure.

## 5. ACDC Variants (§ACDC Variants, L120-174)

Primary variants: **public, private, metadata, bespoke.** Each MAY be **Targeted / Untargeted**. Each has **compact / non-compact** forms.
- **Public ACDC** = no top-level `u`. SAID does NOT securely blind contents (rainbow attack possible given schema). "an ACDC without a top-level UUID… SHOULD be considered a public (non-confidential) ACDC." (L160). Compact ≠ private — "It only provides compactness, not privacy." (L501).
- **Private ACDC** = top-level `u` with sufficient entropy. SAID blinds contents. Enables **Partial Disclosure** — a commitment to the top-level SAID before disclosing contents "without leaking those contents." (§Private ACDC, L164).
- **Metadata ACDC** = *empty* top-level `u`. Lets a Discloser commit to metadata of a yet-to-be-disclosed private ACDC "without providing any point of correlation to the actual top-level SAID." Metadata = Issuer, Schema, Edges, Rules; the `a`/`A` value MAY be empty/missing. Used to get agreement to Rules/waiver BEFORE issuance/disclosure; "should the Issuee refuse… the Issuer has not leaked the SAID of the actual ACDC… nor the Attribute values." (§Metadata ACDC, L168-170).
- **When metadata ACDC is disclosed, only Discloser commitments attach, NOT Issuer commitments** — prevents Issuer commitments becoming a correlation point until after Disclosee agrees to Rules (L172).

## 6. Attribute Section `a` — Targeted vs Untargeted (§Attribute Section, L260-657)

- Reserved nested labels: `d, u, i, dt` (+ `rd`); top-level-only: `cargo`. **Cargo** = opaque embedded/encapsulated data — lets an ACDC "convey some other data format, including other types of verifiable credentials." (L286).
- **Targeted** = presence of **Issuee `i`** at top of `a`. The Issuee AID is "a provably controllable identifier that is the Target." Makes ACDC usable as a **Verifiable Credential** ("evidence of authority, status, rights, entitlement"). (L312-314).
  - "The ACDC MUST be 'issued by' an Issuer and MUST be 'issued to' an Issuee." Precise terms chosen to not "bias or color the role" — Issuee may be Holder/Subject depending on use case (L316-318).
  - Issuee control enables: non-repudiable presentation by Issuee; pre-issuance contract/waiver agreement; **delegation chains** — "the Issuee in one ACDC may become the Issuer of another ACDC" (L322-324).
  - `i` nested in `a` (not top-level) so the Issuee AID is **partially disclosable** / correlatable only after Chain-Link Confidentiality accepted (L316, L344).
- **Untargeted** = no Issuee. "issued 'to whom it may concern.'" Verifiable authorship/attestation only, no counterparty, no delegation. Example: a sensor controlling an AID publishing "verifiable, nonrepudiable measurements." Chains of untargeted ACDCs → "verifiable data supply chain… a verifiable digital twin of a physical supply chain." (§Untargeted, L330-334).
- Variant combos: Targeted/Untargeted × private/public (presence of `i` × presence of `u`) (L304-308).
- **Nested Partial Disclosure:** each nested sub-block carries its own `d` + `u` → branches disclosable at different nesting levels; compact form of a subblock uses its expanded `d` value (worked "grades" example L633-649).

## 7. Aggregate Section `A` — Selective Disclosure (§Aggregate Section, L659-1045)

- `A` (capital) is **distinct** from `a`: its compact value is an **aggregate / AGID (Aggregate ID), NOT a SAID.** (L661).
- Selective disclosure (SD) = "disclosing some information… in a way that does not leak other information." Uses a list of **blinded attribute blocks**, each with its own `d` + `u`. "All fields in a given block MUST be disclosed together as a set" — fields within a block are NOT independently selectively disclosable (L692).
- **Field labels themselves are blinded** (they only appear inside the blinded block); `anyOf` ordering "is not correlated to the actual order" → prevents inference by position and correlation of localized/i18n variants (L694-696).
- **AGID computation** (§L712-747): zeroth list element `a₀` is the aggregate; dummied with `#` chars = length of the digest type in qb64; remaining N elements are block SAIDs; serialize the list in the ACDC's serialization kind; digest (Blake3-256) → qb64 replaces the dummy → AGID. `AGID = H(C(aᵢ for i in {0..N}))`.
- **Inclusion proof:** disclose (1) the detailed block at index j, (2) full list `[a₀..aₙ]`, (3) compact ACDC with `A`=AGID, (4) issuance seal in Issuer's KEL (direct or via TEL). Disclosee verifies by recomputing aⱼ, checking membership, recomputing AGID, matching, computing top-level SAID, confirming KEL seal (L734-750).
- Security rests on: "sufficient cryptographic entropy of the blinding factors, collision resistance of the digests, and unforgeability of the non-repudiable digital commitments." Digest-of-ordered-concatenation is "not subject to a birthday attack." (L688, L728).
- Alternative aggregates: **Merkle-tree root** (more efficient, needs 2nd-preimage protection) or **cryptographic accumulator** — "beyond the scope of this version." (L686, §Inclusion proof via Merkle L2747).
- Schema uses `oneOf` (compact AGID vs array) + `anyOf` (per-element selectivity) + inner `oneOf` (block SAID vs detail) (L757).
- SD vs Partial Disclosure difference (§L1777, L2731): a partially-disclosed block "when fully disclosed, exposes, at the very least, the labels of other fields in its enclosing block." A selectively-disclosed block "does not expose any information about other yet-to-be-exposed fields, including their labels." SD = "separating a 'stew' of 'ingredients' into its constituent ingredients without correlating them via the stew." (L2733).

## 8. Edge Section `e` — property-graph edges & operators (§Edge Section, L1047-1235)

- Edges connect ACDCs into a **DAG** (directed acyclic graph); near node = enclosing ACDC, far node = ACDC referenced by `n` (SAID) (L1172).
- Two block types: **Edges** and **Edge-groups.** An Edge MUST have a node `n` field; an Edge-group MUST NOT (L1058, L1085). Each Edge's block SHOULD have its own SAID `d` so edges are globally resolvable (local labels are not universally unique) (L1066).
- Edge reserved labels: `[d, u, n, s, o, w]` (order fixed) (L1149).
- `s` (schema) on an edge = additional constraint: far node MUST validate against BOTH its own schema AND the edge's `s`. Enables forward-compatibility constraints without adding each minor version to `oneOf`; enables self-deprecating old schemas (L1176-1182).

### m-ary operators (Edge-group `o`) (§L1099-1116)
| Op | Meaning | Default |
|---|---|---|
| `AND` | group valid iff all members valid | **Yes** |
| `OR` | valid if one member valid | No |
| `NAND` | valid iff not all valid | No |
| `NOR` | valid iff all invalid | No |
| `AVG` | arithmetic average of a member property | No |
| `WAVG` | weighted average (uses `w`) | No |

Default when `o` missing = `AND`. Chains = provenance chain/tree: "all links from the node at the head… to the tail… MUST be valid in order for the node (head) to be valid." Validity logic is **EGF-dependent** (L1112-1116).

### unary operators (Edge `o`) (§L1188-1211)
| Op | Meaning | Default |
|---|---|---|
| `I2I` | **Issuer-To-Issuee**: this ACDC's Issuer AID MUST be the Issuee AID of the node the edge points to | **Yes** (for targeted far node) |
| `NI2I` | **Not-Issuer-To-Issuee**: no such requirement | Yes (for untargeted far node) |
| `DI2I` | **Delegated-Issuer-To-Issuee**: this Issuer MUST be the Issuee AID *or a delegated AID of* the Issuee | No |
| `NOT` | logical NOT — inverts far node validity | No |

Re-anchored 2026-09-15: the four rows above are verbatim in `main` @`f0bd097de` §Edge, L1190-1195, and the m-ary table in §Edge-group, L1101-1107, is unchanged from what §8 already records. **`v1.1` adds a fifth unary operator, `E1E` — see §22.2.** Do not read that addition back into this table.

- Default inference: if far node **targeted** (has Issuee) → `I2I` appended; if **untargeted** → `NI2I` appended (L1197-1201). `I2I`/`DI2I` require the far node to be Targeted. (`main` @`f0bd097de` L1197 gates this on the operator list not including "any of the `I2I`, `NI2I` or `DI2I` Operators"; `v1.1` adds `E1E` to that gate — §22.2.)
- "A chain of Issuer-To-Issuee-To-Issuer Targeted ACDCs… can be used to provide a chain-of-authority… a delegation chain for authorization." (L1203).
- Multiple unary ops → list; on conflict "the latest Operator… in the list takes precedence." (L1186).
- **Weight `w`**: for weighted directed edges — "degrees of confidence or likelihood… machine learning or reasoning under uncertainty." Top-level Edge-group MUST NOT have `w` (L1120-1122).
- **Compact edge** (edge block → its SAID; public if no `u`, private if `u`) and **simple compact edge** (edge with only `n` → value is the far-node SAID; always public) (L1156-1158, L1223-1225).
- Discovery via **OOBI** or issuance-time attachment → **Percolated Discovery**: after a successful exchange, the Issuee "will have everything it needs to make a successful disclosure." (L1070).

## 9. Rule Section `r` — Ricardian Contracts (§Rule Section, L1237-1655)

- Rules = a **Ricardian Contract (RC)**: "both human and machine-readable and referenceable by a cryptographic digest." Rule section top-level SAID `d` provides the digest → "supports the bow-tie model of RC." (L1239).
- Rules (terminal, MUST have legal `l`) and Rule-groups (intermediate, MAY nest). Reserved labels `[d, u, l]` (L1265, L1298). A Rule MUST NOT have fields other than `d, u, l` (L1300).
- **Compact Rule** / **Simple Compact Rule** (single `l` field → value is the legal language string, always public) (L1305-1307, L1321-1323).
- Private/confidential rules: a Rule or Rule-group with both `d` and high-entropy `u` "protects the compact form… from discovery via a rainbow table attack merely from its SAID and subschema… may be kept hidden until later disclosure." (L1313).
- **Rule discovery** via SAID + OOBI or issuance attachment = Percolated Discovery (L1253).
- Worked examples: `disclaimers` (warrantyDisclaimer, liabilityDisclaimer) + `permittedUse` rule ("MAY only use this ACDC for non-commercial purposes") (L1512-1541).

## 10. Binding ACDC state to Issuer Key State (§Binding to Key State, L1661-1689)

- **Core anti-forgery doctrine.** To protect against future signing-key compromise, the Issuer "must anchor an *issuance* proof digest seal to the ACDC in its KEL." Two cases:
  - **Direct:** seal anchored in KEL, no registry; ACDC has one state (*issued*/*anchored*); seal digest = ACDC SAID (or bulk aggregate).
  - **Indirect:** state maintained by a **TEL**; registry inception `rip` SAID anchored as Registry proof seal; update events also anchored.
- "ACDCs are not directly signed by the Issuer… bound to the Issuer's Key State… and the Issuer's Key State is signed. This enables the Key State of the Issuer to change independently of the ACDC state." (L1673).
- **Contrast with other VC schemes** (explicit anti-pattern): "other verifiable credential schemes, where the credentials are signed directly; in such schemes, a key rotation forces all the credentials signed with a given set of keys to be revoked; otherwise, a key compromise would enable the compromiser to issue… forged [credentials]." (L1675).
- **Detection-not-prevention / firewall:** "the only way to publish an event in the Issuer's KEL is to verifiably sign the event, which means the forger must first compromise the issuer's private signing keys. This makes any forgery attempt detectable, and such an attempt makes the key compromise detectable." Only exploitable "in an Interaction Event in a KEL that has not yet recovered… via a Rotation Event" → "both detectable and recoverable." (L1687-1689).

## 11. TEL Registrars & Observers — no forced phone-home (§TEL Registrars and TEL Observers, L1691-1695)

- **Registrar** = component under the ACDC Issuer maintaining/publishing the Registry (TEL).
- **Observer** = component under one or more Validators that caches the Registry so Validators "validate the state… without exposing a point of validation (PoV)." Key feature: "it can mask the usage of a given ACDC from the Issuer."
- **Point of Validation (PoV)** = when an ACDC is presented to a Validator. Observer↔Registrar sync happens on state changes, NOT at PoV → "protects against forced validator-to-issuer correlation of ACDC usage, i.e., no forced phone home validation." (L1693). (Direct anti-pattern rejection of OCSP/CRL-style phone-home revocation checking.)
- Observers poll or subscribe; "because ACDC state changes are rare," batch sync; race conditions mitigated by "timed grace periods on revocations." (L1695).

## 12. Data privacy / three-party exploitation model (§Data Privacy, L1703-1736)

- ToIP privacy question: "will the expectations of each party with respect to the usage of shared information be honored by the other parties?" (L1706).
- **Three-party model** (from Sustainable Privacy): **1st party** = data subject/Discloser; **2nd party** = intended Disclosee; **3rd party** = any non-intended Observer. "any unintended usage by any party is potentially exploitive. Intent is with respect to the person (data subject)." (L1712-1726).
- "any use of 1st party data by a 3rd party is likewise, by definition, exploitive." (L1718). 2nd→2nd sharing is non-exploitive only if permitted by 1st party.
- 3rd-party protection = encryption (SPAC / TSP protocols cited, out of scope) (L1728).

## 13. Exploitation-protection mechanisms (§L1738-1792)

- **Least Disclosure:** "disclose only the minimum amount of information… needed to facilitate a transaction, and no more." (L1743).
- **Graduated Disclosure** = recursive/incremental least disclosure: "disclose enough to enable more disclosure, which in turn may enable even more disclosure." (L1747). Mechanisms (L1749-1774):
  - **Compact Disclosure** — SAID commitment, `oneOf` compact/full.
  - **Metadata Disclosure** — metadata ACDC (empty `u`).
  - **Partial Disclosure** — SAID + salty nonce (UUID); SAID+schema not enough to discover content.
  - **Nested Partial Disclosure** — each nested block has `d`+`u`, per-level `oneOf`.
  - **Full Disclosure** — no hiding.
  - **Selective Disclosure** — `anyOf`+`oneOf`, order-independent, membership via SAID set.
  - **Bulk-issued Instance Disclosure** — multiple instances, unique instance IDs, non-correlatable.
  - "All the Graduated Disclosure mechanisms MAY be used in combination." (L1775).
- **Contractually Protected Disclosure (CPD)** — two kinds (L1783-1792):
  - **Chain-Link Confidentiality (CLC)** [ref 44]: offer = Partial Disclosure of metadata + terms; Full Disclosure only after Disclosee agrees ("permissioned disclosure"). "the disclosed data has 'strings attached.'" Chains *Disclosees* (distinct from edge-chaining of ACDCs): "each Disclosee… in turn is the Discloser to the next," terms-of-use MUST propagate. "impose conditions and limitations on the further disclosure and/or use."
  - **Contingent Disclosure:** obligation in Rules to disclose when a contingency is met (e.g., breach); responsible party may be Discloser or an escrow agent; references a private ACDC. Enables **latent accountability**: "Recourse via Full Disclosure of PII is latent… but never realized until the conditions of the contingency is satisfied." Limits PII to "just-in-time, need-to-know basis." (L1792).

## 14. IPEX — Issuance and Presentation Exchange (§L1795-1866) — NOTE: this section is *non-normative*

- "all exchanges (both issuance and presentation) MAY be modeled as the disclosure of information by a Discloser to a Disclosee." (L1797). "The difference between exchange types is the information disclosed, not the mechanism." One protocol → security (well-delimited, analyzable) + convenience.
- Baseline = routed KERI **`exn` messages**. **Message routes** (§IPEX Protocol Messages, L1809-1818):
  | Route | By | Purpose |
  |---|---|---|
  | `apply` | Disclosee | (initiate) defines wanted disclosure: schema/SAID, attribute label list, aggregate element list, signature |
  | `spurn` | either | rejects `apply` / `offer` / `agree` |
  | `offer` | Discloser | (initiate) proposes acceptable disclosure: **Metadata ACDC** or SAID, schema, partial disclosure, signature |
  | `agree` | Disclosee | accepts `offer` (signature/anchored seal) |
  | `grant` | Discloser | (initiate) discloses agreed `offer`: **Full or Selective Disclosure ACDC**, signature |
  | `admit` | Disclosee | confirms received `grant` disclosure |

  Re-anchored 2026-09-15: this table is verbatim in `main` @`f0bd097de` §IPEX Protocol Messages, L1809-1818. **Superseded in `v1.1` for the `apply` and `offer` rows only** — see §21.7. At `main` the `apply` contents are "Schema or its SAID, Attribute field label list, Aggregate element label list, signature on `apply` or its SAID" (L1811) and the `offer` contents are "Metadata ACDC or its SAID, Schema or its SAID, partial disclosure, Aggregate element label list, signature on `offer` or its SAID" (L1813). In `v1.1` @`2362e48a1` both label lists are replaced by the Disclosure Paths, `dp`, field. The `spurn`/`agree`/`grant`/`admit` rows are unchanged on both branches.

- Full apply→offer→agree→grant→admit flow; either side may `spurn`. Note `grant`/`offer`/`apply` can each *initiate* (issuance starts at `grant`; presentation can start at `apply`).
- **Commitments via SAID (cross-variant verifiability)** (L1820-1832): a commitment (signature or KEL-anchored seal) to ANY variant commits to the shared top-level section fields of ALL variants, because each section value is SAD-or-SAID. "a signature on any variant MAY be used to verify the Issuer's commitment to any other variant… on a top-level section-by-section basis." Metadata variant = "a partial manifest." Two proofs: **Proof of Issuance (PoI)** and **Proof of Disclosure (PoD)** (L1832).
- **Variants form a hash tree (using SAIDs).** "A commitment to the top-level SAID of the compact version… is equivalent to a commitment to the hash tree root (trunk)." Different variants = different paths through the tree; verifying nested SAD against SAID = proving inclusion of that branch. **Issuer MUST provide a signature or seal on the SAID of the most compact form variant.** (§Issuer Commitment Rules, L1843-1856).
- **Bespoke / disclosure-specific ACDCs** (§L1860-1866): a Discloser issues its OWN ACDC referencing another via an edge → augment with context-specific contractual obligations, name the Disclosee as Issuee, enable "rich presentation" (combining attributes from multiple edge-referenced ACDCs) "without requiring any new tooling." Attributes referenced via JSON Pointer / CESR-SAD-Path relative to edge node SAID. Worked example: restaurant one-time-admittance ACDC with an anti-assimilation "Assimilation" rule clause (L1872-1908).

## 15. TELs as ACDC state registries (§L1914-2695)

- **TEL** = "hash-chained data structure of sealed transaction events" tracking ACDC transaction states; events sealed/anchored in a **KEL** via seals (seal = event SAID, optionally + sequence number). "TELs, which are thereby bound to KELs, [are] also securely attributable to the KEL's controller." (L1918).
- "verifiable but decorrelatable extensibility to KEL semantics… The seals need no semantics beyond their secure attributability." Transaction state can be public or private (SAID + UUID) (L1918).
- **Persistence property:** "the verifiability of transaction events in the TEL persists in spite of changes to Key States in the sealing KEL." (L1920).
- Validation: any Validator verifies the authoritative state by "validating the presence of the seal in the associated KEL." TEL events need not be signed — "the digest in the seal in the KEL is cryptographically equivalent to signing the transaction event itself." (L1946).
- **VC / VCR / VDR terminology** (§Verifiable Container/Credential Registry, L1948-1950): "ACDCs may be rightly generically referred to as Verifiable Containers (VCs)"; as entitlements = Verifiable Credentials; a **VCR** is a type of TEL, a form of **VDR (Verifiable Data Registry)**; a TEL tracking issuance/revocation = **Revocation Registry**.
- **Registry event types** (§Registry Message Types, L1954-1962):
  | Ilk | Name | Description |
  |---|---|---|
  | `rip` | Registry Inception | registry init |
  | `bup` | Blindable Update | blindable state update |
  | `upd` | Update | non-blindable state update |
  - "A given Registry could switch between using blindable and unblindable update messages." Generic — private (blinded) or public (unblinded).
- Field orders: `rip` = `[v,t,d,u,i,n,dt]`; `bup` = `[v,t,d,rd,n,p,dt,b]`; `upd` = `[v,t,d,rd,n,p,dt,ta,ts]` (L1985-1993). Sequence number `n` = hex, zero-based, strictly monotonic, no leading zeros; `p` = prior event SAID (backward hash-chain).
- `i` (Issuer) in `rip`: distinguishes an Issuer's non-repudiable commitment from a mere endorsement — "A transaction event seal that appears in a KEL with a different Controller AID is merely a nonrepudiable endorsement… not a duplicity-evident nonrepudiable commitment by the Issuer." Also prevents Observer **DDoS** in blinded registries (L2015).
- `rd` (Registry SAID) = SAID of `rip`; binds registry to Issuer AID; enables secure discovery. "When correlation minimization is more important than secure discovery, then the ACDC's `rd` field may be empty or missing." (L2019).
- `td` (transaction ACDC SAID) binds ACDC↔TEL; "hierarchical binding binds the key-state of the issuer to the TEL, which in turn is bound to the ACDC itself… survives changes in the keystate of the Issuer." (L2037).
- `ts` (transaction state) = string from small finite set, e.g. `issued`/`revoked`.

### Blindable state / BLID (§Blinded State Disclosure, L2043-2363)
- **BLID** = blinding SAID of the blinded attribute block `[d(BLID), u, td, ts]` (order fixed); labels are "virtual" (never appear in CESR serialization — fixed-field concatenation). Computed SAID-style on fixed-field concatenation with 44 `#` dummy chars for Blake3-256. (L2047-2066, worked examples L2148-2232).
- Blinded state registry = private registry; only the Issuer-designated **Discloser** (usually the Issuee) can unblind state to a Disclosee (L2129).
- Blind derived from a **shared secret salt** (Issuer + Discloser) via **hierarchically-deterministic derivation** with sequence number as path. "Each new event published by the Issuer… MUST increment the sequence number and hence the blinding factor, but MAY or MAY not change the actual blinded state… an observer cannot correlate state to event updates." (L2135).
- Discloser recovers state by trying all combinations of possible `td` (empty placeholder `1AAP` or real SAID) × possible `ts` (e.g. `1AAP`, `0Missued`, `Yrevoked`) until the BLID matches — only 6 combinations in the revocation example (L2288, L2319).
- **Placeholder decorrelation:** empty state + empty ACDC SAID published before any real ACDC exists; disuse hidden by continuing to update blind "for some time after the ACDC has been revoked or abandoned." (L2137).
- Revocation timing decorrelation: keep updating the blind without changing `ts` "decorrelates the time of revocation." (L2324).
- **CESR count codes:** `BlindedStateQuadruples` `-a##` / `BigBlindedStateQuadruples` `--a######`; empty value primitive `1AAP`; `issued`→`0Missued`, `revoked`→`Yrevoked`. Transaction event seal couple count code `-T##` / `--T#####` (L1931).

### Bound blinded attribute block (§L2427-2695)
- Adds `bn` (bound Issuee key-event sequence number) + `bd` (bound Issuee key-event SAID). Block = `[d,u,td,ts,bn,bd]`. Count codes `BoundStateSextuples` `-b##` / `--b######`.
- Purpose: "better support chains of authority using delegated chained ACDCs" — binds ACDC state to the Issuee's key state at publication, proving the Issuee "had an authorization to issue its own delegated ACDCs… not yet been revoked at the time of anchoring its own delegated issuance." (L2431-2433).

## 16. Bulk-issued private ACDCs & unlinkability doctrine (§L2765-2930)

- Purpose: "use ACDCs with unique SAIDs more efficiently to isolate and minimize correlation across different usage contexts." Each member = "essentially the same ACDC but with a unique SAID" (differ only in top-level `d`,`u`). Shared template + shared salt + index `k` → generated on the fly; Issuee stores only template + salt (L2767, L2803).
- HD derivation paths: top-level UUID path = `k`; attribute-section UUID = `k/0`; aggregate element `j` = `k/j` (L2799-2801).
- **Bulk aggregate `B`** = `H(C(bₖ))` where `bₖ = H(vₖ + dₖ)`, `vₖ` = a *separate* blinding UUID (not the ACDC's `u`), path `k`. Concatenation (not XOR) chosen for CESR crypto-agility / length-independence (L2809-2818). Issuer anchors an issuance proof seal committing to `B` → forgery detectable/recoverable exactly as single-ACDC case (L2805, L2879).
- **Correlation strategies** for the Issuee (L2777): one copy per presentation (one-time-use), one per Verifier, one per Verifier-group.
- **`rd` disclosure hygiene** (three methods, L2842-2848): empty top-level `rd` in metadata ACDC; nest `rd` inside `a`/`A`; omit `rd` entirely and convey OOB (but then Issuer duplicity re: registry is harder to detect).
- **Unlinkability terminology (key doctrine, L2785):** cryptographically-provable correlation resistance = **unlinkability** — but this is "a weak form… as it does not prevent statistical correlation from contextual information." **Contextual linkability** may defeat cryptographic unlinkability. "there is no cryptographic mechanism that precludes statistical correlation among a set of colluding Verifiers." → advanced cryptographic unlinkability can be "an exercise in diminishing returns" without CPD.
- CLC vs technical measures: "Chain-link Confidentiality does not sufficiently deter provable correlation due to unpermissioned malicious collusion" in some apps → use **Independent AID / Independent Registry bulk-issued ACDCs** (unique Issuee AID and/or unique TEL per copy) for stronger technical anti-correlation, at storage/compute cost (L2887-2911).
- **Herd privacy via Sparse Merkle Trees (SMT):** Issuer amalgamates all registry transaction-event seals into one SMT (from Certificate Transparency lineage); one root seal in KEL; efficient `O(log N)` inclusion proofs that don't reveal other members. "A given seal in the KEL… no longer provides a point of correlation to any other transaction event." Issuer may inject random no-op state updates to guarantee a herd-privacy level (L2914-2924).
- 3rd-party vs 2nd-party unlinkability: blinded `B`/`bup` → "3rd party unlinkability"; contractual protection → "2nd party unlinkability via contractual disincentives to link." (L2854).

## 17. Extensibility doctrine (§Extensibility, L2932-2936)

- Built on "append-only verifiable data structures, named KELs and TELs" → "permission-less extensibility by Issuers, presenters, and/or Verifiers… no shared governance… completely decentralized and zero-trust." (L2934).
- Extend already-issued ACDCs by chaining custom ACDCs (custom schema, type-is-schema) "without modifying pre-issued credential types in place." (L2934).
- "no need for centralized permissioned name-space Registries to resolve name-space collisions" — universal content-address + content-addressable schema = the namespace. A registry of ACDC types becomes "merely Schema discovery or schema blessing for a given context or ecosystem." (L2936).

## 18. CESR-native message types (§ACDC Protocol Message Types, L2938-3303)

- Message ilks: TEL = `rip`, `upd` (also `bup`); ACDC top-level = `acm` (field map, default/implied), `act` (fixed-field w/ Attribute), `acg` (fixed-field w/ Aggregate); section messages = `sch`, `att`, `agg`, `edg`, `rul`.
- Message type `t` MUST appear in all native-CESR messages; MAY be omitted only for `acm` non-CESR-native. Default = `acm` ("ACdc field Map").
- CESR count codes: field-map top-level `-G##`/`--G#####`; fixed-field `-F##`/`--F#####`. Fixed-field: all fields required but MAY be empty; empty string `4BAA`, empty map `-IAA`, empty list `-JAA`, null primitive `1AAK`, empty `u`/`rd` primitives per type.
- **Section messages** let sections travel/cache independently of the ACDC (schema & rule sections often reused across many ACDCs). The embedded section's `d` matches the ACDC's most-compact section value; the section-message's own top-level `d` is NOT most-compact-algorithm-computed (L3082-3092).

## 19. Cryptographic strength & Information-Theoretic / Perfect Security (§L2705-2719)

- **128 bits of entropy** is the baseline for perfect-security seeds/keys to resist brute force. Worked estimate: a million supercomputers → ~2⁹⁵ tries/year → ~2³³ ≈ 8.6 billion years to brute a 128-bit value. Non-perfect-security systems (signatures) may need larger keys to preserve 128-bit strength (L2709-2715).
- **Information-Theoretic Security** = "cannot be broken algorithmically even if the adversary has nearly unlimited computing power including quantum." **Perfect Security** = "the ciphertext provides no information about the key" (one-time-pad / Vernam, secret-splitting) (L2717-2719).
- HD derivation "MUST preserve… approximately 128 bits of cryptographic strength" — derived UUID typically 2× the salt length (256-bit) (L2079, L2282).

## 20. Selective-disclosure design philosophy (§Selective Disclosure annex, L2721-2745)

- **Chaining reduces the need for SD:** "Many non-ACDC verifiable credentials provide bundled credentials because there is no other way to associate the attributes… These bundled credentials could be refactored into a graph of ACDCs. Each… separately disclosable and verifiable thereby obviating the need for Selective Disclosure." (L2739).
- **Universality mandate:** "not all instances of an ACDC MUST employ the minimal Selective Disclosure mechanisms… but all ACDC implementations MUST support any instance… that employs the minimal Selective Disclosure mechanisms." (L2735).
- Tiered SD tools: SD-attribute ACDCs (bundled attributes) → bulk-issued ACDCs (bundled usage contexts) → independent-TEL bulk-issued ACDCs (Issuee-across-contexts correlation) (L2737-2745).
- Salt sharing: X25519 keys derived from Ed25519 keys, interactive (DH) or non-interactive (encrypt+sign salt) — the latter "more scalable for AIDs… controlled with a multi-sig group" (L2757-2761).

---

## 21. Disclosure Paths and the `dp` field — `[N1.1]`, `v1.1` @`2362e48a1` only

**Tier warning.** Every claim in this section is `[N1.1]`. `## Disclosure Paths` does not exist on `main` at `f0bd097de` — the string "Disclosure Paths" occurs zero times there. This is the largest single addition in `v1.1`: a new `##`-level major section, `v1.1` L1809-1986, sitting between §Contractually Protected Disclosure and §IPEX. The bible's chapter 08 currently carries this construct at the `[P]` tier from keripy discussion #1627; **this section is the evidence that upgrades it to `[N1.1]`, and no further.**

The section declares its own normativity: "This section is normative. It defines the path syntax that designates the parts of an ACDC, or of a DAG of chained ACDCs" (§Disclosure Paths, `v1.1` L1811). It is explicit that this is a separation of concerns from IPEX: the IPEX section "which is non-normative, binds the `dp` field to particular messages," and "The syntax and semantics defined here apply wherever a `dp` field appears" (L1811).

**`dp` is not an ACDC field.** "The `dp` field is not an ACDC field. It appears in the messages that negotiate a disclosure, not in the ACDCs that are disclosed." (§Disclosure Paths, L1813). It is therefore deliberately *not* added to the reserved-label table — unlike `_`, which is (§22.1).

### 21.1 DAG of ACDCs (§DAG of ACDCs, L1815-1833)

- **An ACDC is a graph fragment holding exactly one node.** "An ACDC holds no Edges incoming to its own node, only outgoing ones; its incoming Edges belong to other fragments." (L1817). The node part is "its top level plus its Schema, Attribute, Aggregate, and Rule sections" (L1817) — i.e. everything except the Edge section.
- **Exactly one origin.** "That DAG MUST have exactly one source node, called the origin node." (L1821). A source node "MUST either have no Edges at all or only outgoing Edges" (L1819).
- **Bespoke ACDC as the normalizer.** "Where a single exchange is to convey several unchained ACDCs, a DAG MUST be formed by issuing a bespoke ACDC whose node is the origin" (L1823). "This gives every exchange the same normalized structure, on which the `dp` field depends." (L1823). This gives the bespoke-ACDC mechanism already in §14 a second, structural job.
- **Ordering is load-bearing and derives from insertion-ordered field maps.** "A well-ordered DAG with a single source node linearizes into a unique, reproducible order." (§Ordering, L1831). The chosen order is breadth-first: "One such order is that of a breadth-first search from the origin node." (L1833). The stated reason is readability rather than correctness — depth-first "yields a unique, reproducible order too", but in a dossier using joint issuance the joint-issued ACDCs "fall together in breadth-first order and scatter in depth-first" (L1833). "Where the DAG is a single chain, the two orders agree." (L1833).
- **Graph-of-subgraphs framing.** "A DAG of ACDCs is therefore a graph of subgraphs, one subgraph per ACDC. So in what follows, node may mean a node of the DAG of ACDCs or a node of one ACDC's subgraph." (§DAG of Subgraphs, L1827). This is the ambiguity the reader must hold: "node" is overloaded on purpose.

### 21.2 Path syntax (§Path Syntax, L1835-1841)

- "A path is a tuple of components." (L1837). A component is a field label, or a zero-based integer offset where the collection is an array/tuple/list rather than a field map.
- **Two serializations, two delimiters.** "the components are separated by the path delimiter, `/`, and when serialized compactly as a CESR primitive, by `-`" (L1837). This is the whole reason for §22.1's label restrictions.
- **Labels preferred over indices.** "for readability a path SHOULD use field labels wherever they exist, that is, except where it traverses an array" (L1837).
- **Two rootings.** "A path that begins with the path delimiter, `/` (equivalently, whose first component in tuple form is an empty string), is a DAG-absolute path" (L1839), rooted at the origin ACDC's top level. A path not beginning with the delimiter "is an ACDC-relative path, rooted at the top level of its associated ACDC." (L1841).

### 21.3 Traversing edges (§Traversing Edges, L1843-1851)

- "A path that traverses one or more Edges MUST be in DAG-absolute form, and MUST therefore begin with `/e`" (L1845) — the origin node's Edge Section.
- **The hop is a virtual component `_`, not the `n` label.** "The hop from that Edge to the top level of the far-side ACDC is denoted by the virtual path component `_`" (L1845); "The Edge block's node, `n`, field label is not a path component; `_` stands for the traversal that `n` designates." (L1845).
- Worked form: `/e/reports/project/_/a/author` descends origin → Edge Section → Edge-group `reports` → Edge `project` → hop → far ACDC's `a` → `author` (L1847). Two hops nest the same way: `/e/evidence/_/e/reports/project/_/a/author` (L1849).
- **The requirements bind the *effective* path.** "The requirements of this section apply to the effective path, that is, to the prefix and the path taken together." (L1851).

### 21.4 Node paths vs leaf paths (§Node Paths and Leaf Paths, L1853-1861)

- **Node path = trailing delimiter = whole subtree.** "Such a path designates the disclosure of that node and the full expansion of every branch beneath it." (L1855). It "also requires disclosure of enough of the branch leading to that node to validate the SAIDs along the path." (L1855).
- **Leaf path = no trailing delimiter = one value.** "A path ending in a non-empty field label or index component designates a single leaf." (L1857). "It requires no sibling branch." (L1857).
- **A `d` node path is the expansion of the compacted value.** "`a/d/` and `a/` designate the same block", and a top-level `d/` "designates the whole of that ACDC" (L1859).
- The spec's own slogan: "The node form is a hammer, the leaf form a scalpel." (L1861).

### 21.5 Closures — what a path actually discloses (§Closures, L1863-1877)

This is the semantic core, and the part most likely to be misread.

- "A disclosure path translates into a closure over the fields or array elements it implies." (L1865); "The disclosure designated by a set of paths is the union of their closures." (L1865). A closure "MAY span several ACDCs where the path traverses Edges." (L1865).
- **Closure size depends on how the reached section blinds.** "What a leaf path closes over depends on the section it reaches, because the sections differ in how they blind their contents." (L1867).
  - **Partially disclosable sections (Attribute, Edge, Rule)** share one SAID and one UUID per block, so "A leaf path into such a block therefore closes over every simple field of that block. Its nested sub-blocks stay compacted as their SAIDs." (L1869). Consequence for edges: a leaf path into an Edge block "closes over that Edge's node, `n`, and other simple fields together, which is what verifying the Edge against the far-side ACDC requires" (L1869).
  - **Selectively disclosable Aggregate Section** blocks each carry their own `d` and `u`, so "A leaf path to one such block therefore closes over that block alone and tells nothing of any sibling." (L1871). The closure is "the whole block and no more, together with the unblinded AGID at the head of the array, against which the block's inclusion is proved" (L1871).
- **Schema is always free.** "The top-level Schema Section of an ACDC is always disclosed, so no path need designate it." (L1873).
- **Rules are not free.** "The Rule Section is usually disclosed in full, but rules MAY be blinded, so it too supports Partial Disclosure and MUST NOT be assumed fully disclosed. A path MUST designate it when it is wanted." (L1875).
- **A closure is not a use restriction.** "A closure states what a path discloses. It does not bound what the Disclosee may then do with what it holds." (L1877). Unblinding an Edge yields the far-side SAID and so "enables a further request for that ACDC, but that request is a separate disclosure with a closure of its own." (L1877). This is the boundary between the path mechanism and Chain-Link Confidentiality; the paths do not do CLC's job.

### 21.6 The `dp` field itself (§Disclosure Paths, `dp`, Field, L1879-1917)

- **Shape: a list of 3-tuples.** "The value of the Disclosure Paths, `dp`, field is a list of tuples." (L1881). "Each tuple represents one ACDC in the DAG that is the object of the exchange and is of the form `(ACDCSchemaSAID, PathPrefix, [paths])`." (L1881). The first element is "the qb64-encoded SAID of the Schema of the associated ACDC" (L1881). "In a serialization that has no distinct tuple type, such as JSON, each tuple MUST be represented as a three-element array." (L1881).
- **Why a list and not a map.** "A list of tuples is used rather than a field map keyed by Schema SAID so that a Schema SAID MAY appear more than once." (L1883) — two ACDCs of the same type can appear in one DAG, and the spec's own worked example is such a case (the research-report and project-report ACDCs share a Schema).
- **Path prefix** (§Path Prefix, L1885-1897): "The path prefix of a tuple is the DAG-absolute route to the ACDC that the tuple's ACDCSchemaSAID names." (L1889). It "MUST be either the empty string or a DAG-absolute path that both begins and ends with the path delimiter, `/`" (L1889); for the origin node it is the bare `/`. "A prefix MUST NOT reach past the top level of the ACDC it names." (L1889).
  - Concatenation rule: the effective path is prefix + entry "with no delimiter inserted between them", and "An entry of a path list MUST NOT begin with the path delimiter." (L1891) — so the concatenation is always well-formed, "This holds equally of the compact serialization, in which the delimiter is `-`." (L1891).
  - Empty-entry asymmetry: with a non-empty prefix, an empty entry `""` designates the whole named ACDC (L1895); with an empty prefix, "an empty entry designates nothing" and the shortest whole-ACDC path is `d/` (L1897).
- **Identifying each tuple's ACDC** (§Identifying Each Tuple's ACDC, L1899-1913): "The elements of the `dp` list MUST appear in the breadth-first search order of the DAG from its origin node." (L1901). "The zeroth element MUST represent the origin node ACDC." (L1901).
  - First contact is handled by making the requester define the shape: "in practice the requester defines the shape of the DAG it will accept, and that shape fixes the origin node's Schema" (L1903); failing that it "names a deliberately permissive origin Schema, one constraining little beyond the Issuer and Issuee" (L1903).
  - Ordering is required even when prefixes make it redundant, on a cost argument: "Any party that generates a `dp` value must already linearize the DAG in order to walk it, so ordering the list costs nothing" (L1905).
  - **Completeness depends on which identifier is in play.** With empty prefixes "the list MUST hold one element for every ACDC of the DAG in breadth-first order, and an element from which nothing is requested carries an empty path list"; with non-empty prefixes "the list MAY omit any ACDC from which nothing is requested" (L1907).
  - **Optional edges force explicit prefixes.** Where a Schema makes an Edge or Edge-group optional, "a party that knows only the Schema cannot generate a total ordering… The ordering then has gaps. In that case the prefix of every element after the zeroth MUST be non-empty" (L1911).
- **Solicited response** (§Solicited Response, L1915-1917): "an empty list, `[]`, means that the answering path list is the same as the one it answers." (L1917). "Where the answering list differs, or where the message is unsolicited, the `dp` value MUST NOT be an empty list." (L1917).

### 21.7 `dp` in the IPEX exchange — `[N1.1]` (§Disclosure Paths in `apply` and `offer`, `v1.1` L2013-2019)

Chapter 08 material. This is the only place `dp` touches a wire protocol, and the subsection sits inside the **non-normative** IPEX section, so its normativity is inherited from §Disclosure Paths, not asserted here.

- **Both `apply` and `offer` carry `dp`.** The `v1.1` route table gives the `apply` contents as "Disclosure Paths, `dp`, signature on `apply` or its SAID" and the `offer` contents as "Metadata ACDC or its SAID, Disclosure Paths, `dp`, partial disclosure, signature on `offer` or its SAID" (§IPEX Protocol Messages, L2004/L2006). This **supersedes** the `main` rows, which listed a Schema SAID plus an "Attribute field label list" and an "Aggregate element label list" (§14 above).
- **`dp` goes in the query section, not the attribute section.** "An exchange, `exn`, message carries both a query section, `q`, and an attribute section, `a`, so that it can model a ReST request" (L2015) — route `r` is the path, `q` the query string, `a` the body. "A request to disclose names which parts of which ACDCs are wanted. It is a query." (L2015). Therefore "it MUST appear in that message's query section, `q`, and not in its attribute section, `a`." (L2015).
- **Solicited-response semantics carry through.** "An `offer` answering an `apply` is a solicited response in the sense defined above, so an empty `dp` list in such an `offer` means the offered disclosure is the one the `apply` requested." (L2017). An `offer` proposing something different, or an unsolicited one, "MUST NOT carry an empty `dp` list." (L2017).
- **CLC ordering is stated as usual practice, not a requirement.** "The `offer` usually carries a Metadata ACDC disclosing the Rule Section of the ACDC on offer" (L2019), so the Disclosee can `agree` before any attribute value is disclosed.

### 21.8 Special cases (§Special Cases, `v1.1` L1919-1939)

- **Aggregate Section pathing by label, not offset.** A Disclosee does not know a blinded block's offset, but each block carries a uniquely labeled field, so "A path MAY therefore name a block by that label in place of its offset, as in `A/over21`." (L1923). The labeled form "is therefore a shorthand for the indexed form and expands to it": `A/over21` and `A/1/over21` designate the same closure (L1925). Disambiguation rests on a label rule: "Nothing is ambiguous between the two forms, because a field label MUST NOT begin with a numeral." (L1925).
  - Such a path "designates the block that holds the labeled field, not the field alone, and closes over the whole of it" (L1925).
  - **The shorthand cannot reach inside a block, and the refusal is doctrinal.** A path like `A/over21/issued` "MUST be rejected when expanded" (L1929), because "Disclosing part of the inside of a selectively disclosed block mixes Partial Disclosure into Selective Disclosure, and a Schema that calls for it is better rewritten as a DAG of ACDCs." (L1929). This is the §20 "chaining reduces the need for SD" argument reappearing as a validation rule.
  - The AGID at index 0 "is not blinded, and an inclusion proof is verified against it, so it is disclosed in any closure that discloses any element of the section." (L1931). `A/0` designates it alone; `A/` designates the whole section expanded.
- **Simple compact Edge.** Its value is the far node SAID rather than an Edge-block SAID, but "A simple compact Edge is represented differently within the ACDC, but the path syntax for traversing it is the same." (L1935) — label, then `_`.
- **Private Edge, and the two-step negotiation.** The Edge block label is known from the Schema, but the Schema SAID of a private Edge block "may not be available until an earlier step of the exchange has unblinded that Edge. A private Edge MAY therefore require a two-step negotiation" (L1939) — an earlier `agree` releases an enhanced `offer` that uncovers the private Edge's Schema, and a later request designates the ACDC behind it.

### 21.9 Worked `dp` example (§Disclosure Paths Example, `v1.1` L1941-1985)

Four ACDCs from the spec's own complete example: transcript (origin) → `accreditation` Edge, and a `reports` Edge-group holding `research` and `project` Edges. Breadth-first order: transcript, accreditation, research report, project report (L1943). Requesting Issuer, Issuee/author and the whole Rule Section from each yields, in ACDC-relative form, four tuples each of the shape `["<SchemaSAID>", "", ["i", "a/i", "r/"]]` (L1947-1954). The last two tuples repeat one Schema SAID — "This is the case that a field map keyed by Schema SAID could not express." (L1956).

The prose on closures for that request is the clearest statement of what a path costs (L1958-1960): the leaf `i` closes over "every top-level field in compact form, which is what validates the ACDC's top-level SAID"; the leaf `a/i` closes over every simple field at the top of the Attribute Section "and leaves the nested `grades` block compacted as its SAID"; the node `r/` closes over the Rule Section "expanded all the way down"; and "Together these closures reach no part of the Edge Section." Reaching a non-origin ACDC additionally pulls in the branch of the origin's Edge Section that verifies the Edge SAID leading to it.

The DAG-absolute form of the same request differs only in the prefixes (`/`, `/e/accreditation/_/`, `/e/reports/research/_/`, `/e/reports/project/_/`) — "the route to each ACDC has been factored out of its paths and into its prefix" (L1962). "Were the transcript Schema to make any of the three Edges optional, a non-empty prefix would be REQUIRED" (L1973).

## 22. Other `v1.1`-only changes — `[N1.1]`, `v1.1` @`2362e48a1`

### 22.1 Field Label Restrictions — a new `###` section, and a new reserved label `_`

`### Field Label Restrictions` (`v1.1` L61-69) does not exist on `main` at `f0bd097de`. It exists to make labels safe as path components.

- **`-` is forbidden in a field label.** The compact CESR serialization of a path replaces `/` with `-` "so that the result is pure Base64 and no character has to be expanded into a Base64 equivalent. A field label in an ACDC MUST NOT, therefore, contain the character `-`." (L63). The cost argument: most languages disallow `-` in an attribute name anyway.
- **A lone `_` is reserved as the DAG-hop component.** "With `-` reserved as the compact path delimiter, the only Base64 character left to denote a hop across an Edge is `_`." (L65). "The label `_` MUST therefore be reserved as a virtual path component denoting that hop" (L65), and "A field in an ACDC MUST NOT be labeled with a single `_`." Narrowly scoped: "Only that label is forbidden; `_` MAY appear within a longer label, such as `first_name`." (L65).
- **`_` is a real field in the DAG expansion.** "In such an expansion, each Edge block gains a field labeled `_` whose value is the subgraph contributed by the far-side ACDC named by that Edge's Node, `n`, field." (L67). The point is that a value is then extracted from a DAG expansion "just as it is from within a single ACDC" — one path machinery, not two.
- **Scope excludes the Schema Section.** "They do not reach the labels within the Schema Section." (L69), because those labels come from the JSON Schema vocabulary, "and no disclosure path descends into that section, which is always disclosed."
- **`_` is added to the reserved-fields table**, with the title "DAG Hop": "Virtual label that denotes the traversal (hop) from an Edge in the near-side ACDC to the top level of the far-side ACDC" (§Other Reserved Fields, `v1.1` L55). The table's preamble also weakens from `main`'s "These MAY appear at other levels besides the top-level of an ACDC" (`main` L41) to "Most of these MAY appear at other levels besides the top-level of an ACDC" (`v1.1` L41) — because `_` must not appear as a field label at all.

### 22.2 `E1E` — a fifth unary Edge operator

`v1.1` adds one row to the unary-operator table (§Edge, `v1.1` L1206) that is absent from `main` at `f0bd097de` (`E1E` occurs zero times there). Chapters 05 and 07 depend on this family.

| Op | Meaning | Default | Branch |
|---|---|---|---|
| `E1E` | **IssueE-To-IssueE** — "The Issuee AID of this ACDC MUST be the Issuee AID of the node this Edge points to." | No | `v1.1` only |

- **It is an identity relation, not a delegative one.** "This is an identity relation on the two ACDCs' Issuees and places no constraint on either ACDC's Issuer." (L1206). Expanded at L1223: "Unlike `I2I` and `DI2I`, which are delegative Operators that constrain the Issuer AID of the current ACDC relative to the Issuee AID of the node the Edge points to, `E1E` is an identity relation between the two ACDCs' Issuee AIDs."
- **Both ends must be Targeted.** "both the ACDC in which the Edge resides and the node to which the Edge points MUST be Targeted ACDCs (each MUST have an Issuee), and the Edge is valid when, and only when, those two Issuee AIDs are equal." (L1223).
- **The motivating case is same-subject, different-issuer.** "An example is a core identity credential and a separate entitlement credential issued to the same Issuee by different Issuers: `E1E` binds them as being about the same subject, a relationship the delegative `I2I` Operator cannot express" (L1223), because `I2I` "would instead require the entitlement ACDC's Issuer to be the core credential's Issuee."
- **It joins the default-inference gate.** `v1.1` L1209 reads "does not include any of the `I2I`, `NI2I`, `DI2I`, or `E1E` Operators"; `main` L1197 omits `E1E`. The `I2I`-for-targeted / `NI2I`-for-untargeted defaults themselves are unchanged, and `E1E` is never a default.
- The m-ary operator table (`AND`/`OR`/`NAND`/`NOR`/`AVG`/`WAVG`) is **unchanged** between the two branches — checked at `v1.1` L1112-1119 against `main` L1101-1107.

### 22.3 UUID → Unique Entropy (UE): terminology only

`main`'s `### Universally Unique Identifier (UUID) Fields` (L87) becomes `### Unique Entropy (UE) Fields` in `v1.1` (L98), and the field tables change the `u` title from "UUID" to "UE", with the description going from "Random Universally Unique Identifier as fully qualified high entropy pseudo-random string, a salty nonce" (`main` L46) to "Random unique entropy as fully qualified high entropy pseudo-random string, a salty nonce" (`v1.1` L46).

**This is a rename and nothing more.** The two paragraphs of substance (rainbow/dictionary attack on the power set of schema-allowed values; `u` as blinding factor; top-level `u` blinding the whole ACDC) are word-for-word identical on both branches once "UUID" is swapped for "unique-entropy". §3's UUID doctrine therefore stands unchanged; only the name moves. The same substitution runs through the Edge, Edge-group and Rule sections (`##### Unique Entropy, `u` field` in `v1.1` L1171 vs `##### UUID, `u` field` in `main`).

## 23. Worked lifecycle and graduated-disclosure examples — `[N]`, `main` @`f0bd097de`

**Tier correction, recorded 2026-09-15.** These two subsections are new *to this note*, and new since the note's `11832a3` pin, but they are **not** `v1.1`-only: both are present in `main` at `f0bd097de` and are substantively identical on `v1.1` (the only deltas in the region are the UUID→UE substitutions of §22.3). Cite them as `[N]`. They sit in the Annex's Working ACDC Examples region — `main` L4852-4986 and L4988-5098 respectively, `v1.1` L5053-5187 and L5189-5299. Chapters 05 and 10 need them.

### 23.1 §Registry-Dependent Issuance Lifecycle (`main` L4852-4986)

A five-step worked lifecycle filling a gap the earlier examples left: "The examples above reference each issuer's registry by its identifier (for example `regAmy`) as though it already existed." (L4854-4856). The walk is "it creates the registry, issues a credential bound to it, records the credential's issued state in the registry, lets a verifier confirm that state," and finally revokes it (L4856-4859). "Amy (a school) issues to Bob (a student) using Amy's registry." (L4859-4860).

- **Step 1, `rip`.** "The registry identifier is the SAID of this event, so it is *derived* from the event rather than chosen." (L4863-4865). "The inception commits to no credential state: it is a vacuous placeholder that reveals nothing about what will later be issued." (L4865-4867). (This is the sentence `raw/16 §6` already identified as the origin of #1613's "latest non-vacuous event" phrasing — now re-anchored at `f0bd097de`.)
- **Step 2, `acm`.** The ACDC's `rd` references the `rip` SAID; the top-level `d` is over the most compact form. "Because the SAID is derived from the credential's content, it is not known in advance; it is produced by issuance, not assumed." (L4890-4892).
- **Step 3, `bup`.** The blinded state block is `{d, u, td, ts}` with `ts: "issued"`, blinded by a nonce "that Amy derives from a salt shared with Bob and the update's sequence number." (L4916-4917). "Only the blinded block's SAID travels in the `bup`; neither the credential SAID nor the word `issued` appears." (L4917-4918).
- **Step 4, verification.** The verifier "recomputes the blinded block's SAID over the candidate states (`issued`, `revoked`) and the credential SAID it was shown, using the salt and the update's sequence number." (L4951-4953) — the trial-unblinding procedure of §15, in a two-candidate instance.
- **Step 5, revocation.** A second `bup` at the next sequence number. "The blinding nonce is independent of the one at sequence 1 (both derive from the salt and their own sequence numbers), so the two updates' blinded SAIDs are unrelated" (L4961-4963). A verifier that once confirmed `issued` "cannot later read the `revoked` state by watching the registry: it would need the salt to derive the sequence-2 nonce." (L4979-4981).
- **The boundary is stated plainly, and is doctrine.** "The registry *events* remain public and chained (the `rd` and prior links are in the clear); it is the state *content* each event commits to that is protected." (L4981-4983). And: "This is confidentiality of registry state, not anonymity of the credential — issuer, registry, and issuance chronology remain linkable, which is the intended, auditable trade-off." (L4983-4985).
- **The registry is Issuer-controlled throughout, with no Issuee-controlled variant anywhere in it.** See §24.2 — this is a load-bearing negative result for chapter 10.

### 23.2 §Graduated Disclosure worked examples (`main` L4988-5098)

Two flows, framed as "how an issuer *plans* for disclosure by the way it structures the credential, and how a holder *performs* disclosure at presentation while a verifier checks it." (L4991-4993).

- **Selective disclosure via an aggregate section.** Each attribute gets its own element with its own `u` and `d`; the AGID is element 0. At presentation the holder "discloses only the chosen elements as full blocks and leaves the rest as their bare SAIDs" (L5031-5032), and the verifier "recomputes the AGID over the mix of disclosed blocks and undisclosed SAIDs and confirms it still equals the committed AGID" (L5048-5049).
  - **The leak that remains, stated without hedging:** "The verifier does still learn how many elements the section has and which were withheld — the count and positions are structural, not blinded" (L5051-5053); "only the withheld values themselves are protected." This is a concrete boundary on the §7 selective-disclosure claim and belongs wherever the corpus states SD's guarantees.
- **Partial disclosure via compaction.** A private ACDC circulates most-compact. "Because the top-level SAID is computed over the most compact form, it is identical whether the credential is held compact or expanded." (L5058-5060). The CLC ordering is shown concretely: "Under Chain-Link Confidentiality the rule (terms-of-use) section is disclosed first — so a potential Disclosee can agree to the terms" (L5078-5080) while the attribute section stays a bare SAID.
  - Closing invariant: "Every disclosure level — including disclosure of a nested block within a section, or a mix of disclosed and withheld sibling blocks — verifies to the same top-level SAID, so what the credential commits to never changes as disclosure progresses." (L5095-5098; hard-wrapped in source, joined on spaces).

## 24. Negative results — what was looked for and NOT found, at the named commits

A negative result is a finding. Each of these was checked by full-text search of `spec/spec-body.md` at the stated commit.

1. **`v1.1` does not change the `rd`-in-attribute-section language at all.** `raw/16 §6` and `raw/16 §8` item 2 record an unresolved tension: at `main`, nested `rd` is glossed "or usage registry for ACDC when not at top-level" and the prose is explicitly open-ended. At `v1.1` @`2362e48a1` §Registry SAID Field (L96) and the reserved-fields table row (L48) are **byte-identical to `main` @`f0bd097de`** (L85 and L48), typo included. The open-ended sentence still reads "a registry SAID, `rd` field that appears nested in the Attributed, `a`, or Aggregate, `A`, section MAY be used for some other registry, such as an application-specific or Issuer-specific registry." So `v1.1` neither restricts nested `rd` to presentation registries nor forbids the ACDC-state-registry reading. **`raw/16 §8` item 2 is therefore still open, and this is the negative answer to the specific question it poses about v1.1.**
2. **No Issuee-controlled registry anywhere in `v1.1`.** "Issuee-controlled", "Issuee controlled", "Issuee's registry" and "registry controlled by the Issuee" occur zero times at `2362e48a1`. The §Registry-Dependent Issuance Lifecycle (§23.1) is Issuer-controlled end to end: Amy incepts the registry, Amy issues, Amy appends every `bup`. Bob's only role is holding the shared salt. `raw/16 §6`'s statement that the spec "does not contemplate an *Issuee*-controlled registry" **holds unchanged at `v1.1` @`2362e48a1`**, not merely at `main` @`f0bd097`.
3. **"presentation registry" occurs zero times** at `2362e48a1` (and zero times at `f0bd097de`).
4. **"usage registry" occurs exactly once** at `2362e48a1` — the reserved-fields table gloss at L48, identical to `main`. It is still "the only trace of this design in any specification", as `raw/16 §6` says.
5. **"Disclosure Paths" occurs zero times** at `f0bd097de`. The whole of §21 is `v1.1`-only; there is no `main` text to upgrade it with.
6. **`E1E` occurs zero times** at `f0bd097de`.
7. **`### Field Label Restrictions` does not exist** at `f0bd097de`.

## 25. Open questions and unresolved tensions

1. **Will `dp` land in the standardizing line, and in what shape?** `## Disclosure Paths` is a ~180-line normative section living only on `v1.1` at `2362e48a1`. The bible's chapter 08 may now describe it at `[N1.1]`. **Nothing here licenses `[N]`.** Re-check `main` every refresh; the moment the section appears there, §21 gets re-tiered wholesale and this note's §14 IPEX table must be rewritten rather than annotated.
2. **`dp` is normative but its only binding is non-normative.** §Disclosure Paths declares itself normative (L1811), yet the sole place it meets a wire format is §Disclosure Paths in `apply` and `offer`, inside the IPEX section that opens "This section is non-normative" (L1990). So the syntax is normative and its use is not. Worth naming in chapter 08 rather than smoothing over.
3. **The `_` reservation is a backward-incompatible constraint on existing ACDCs.** `v1.1` L65 says a field "MUST NOT be labeled with a single `_`", and L63 says no label may contain `-`. Any already-issued ACDC with such a label becomes non-conforming under `v1.1`. The spec argues the cost is low but does not address migration. Unresolved.
4. **`E1E` has no implementation evidence in this note.** It is `[N1.1]` on the spec side only; whether keripy recognizes it is a `[K]` question this pass did not touch. Chapter 07's operator-family material should not imply support.
5. **Aggregate-section label pathing assumes uniqueness the Schema must enforce.** §Aggregate Section Pathing (L1923) rests on each blinded block carrying "a field whose label appears in no other block", but nothing quoted states *who* guarantees that or what happens when it fails. The expansion from `A/over21` to an offset is undefined if two blocks share a label.
6. **Blinded-block label pathing sits awkwardly against the aggregate's anti-correlation design.** §7 records that in the Aggregate Section "Field labels themselves are blinded" and `anyOf` ordering "is not correlated to the actual order". A `dp` path that names `A/over21` presupposes the requester knows that label. The two claims are reconcilable (the label is known from the Schema, not from the instance) but the spec does not reconcile them in either place, and a reader of chapter 07 plus chapter 08 will hit the seam.
7. **`raw/16 §8` item 2 remains open** — see §24.1. `v1.1` at `2362e48a1` settles nothing about nested-`rd` disambiguation.

---

## Exact short quotes (<=25 words) with citations

**Every quote in the first list below is from `main`, tier `[N]`, and its line hint is at `11832a3` unless this pass re-anchored it (see the header). The second list is `v1.1` only, tier `[N1.1]`, at `2362e48a1`; the third is `main` at `f0bd097de`. Never move a quote between lists without the text in the destination branch at a named commit.**

### `main` — `[N]` (line hints at `11832a3`)
- "no top-level field types exist in an ACDC… the Schema, `s`, field itself is the type field." — §Type-is-schema, L182
- "type information is metadata, not data." — §Type-is-schema, L182
- "ACDCs MUST use insertion-ordered field maps for canonical serialization/deserialization." — §Ordered Nested Field Maps, L10
- "No shared or trusted relationship between the Controllers and Verifiers is REQUIRED." — §AID Fields, L95
- "all Schemas MUST be static, i.e., Schemas MUST be SADs and therefore verifiable against their SAIDs." — §Static Schema, L200
- "dynamic Schema references or dynamic Schema generation mechanisms MUST NOT be used." — §Static Schema, L194
- "This is essential to Graduated Disclosure." — §Most compact form SAID, L136
- "It only provides compactness, not privacy." — §Targeted Public-attribute, L501
- "The ACDC MUST be 'issued by' an Issuer and MUST be 'issued to' an Issuee." — §Targeted Attribute Section, L318
- "the primary design goal is not data privacy protection per se but the more general goal of protection from the unpermissioned exploitation of data." — §Disclosure Mechanisms, L1659
- "disclose only the minimum amount of information about a given party needed to facilitate a transaction, and no more." — §Least Disclosure, L1743
- "disclose enough to enable more disclosure, which in turn may enable even more disclosure." — §Graduated Disclosure, L1747
- "the disclosed data has 'strings attached.'" — §Contractually Protected Disclosure, L1790
- "no forced phone home validation." — §TEL Registrars and TEL Observers, L1693
- "This makes any forgery attempt detectable, and such an attempt makes the key compromise detectable." — §Binding to Key State, L1687
- "the verifiability of transaction events in the TEL persists in spite of changes to Key States." — §TEL Overview, L1920
- "This is completely decentralized and zero-trust." — §Extensibility, L2934
- "all exchanges (both issuance and presentation) MAY be modeled as the disclosure of information by a Discloser to a Disclosee." — §IPEX, L1797
- "there is no cryptographic mechanism that precludes statistical correlation among a set of colluding Verifiers." — §Bulk-issued, L2785
- "This satisfies the KERI design ethos of 'minimally sufficient means.'" — §Basic selective disclosure, L686
- "any use of 1st party data by a 3rd party is likewise, by definition, exploitive." — §Three-party, L1718

### `v1.1` — `[N1.1]` only, at `2362e48a1`. **MUST NOT be cited as normative.**
- "This section is normative. It defines the path syntax that designates the parts of an ACDC, or of a DAG of chained ACDCs" — §Disclosure Paths, L1811
- "The `dp` field is not an ACDC field. It appears in the messages that negotiate a disclosure, not in the ACDCs that are disclosed." — §Disclosure Paths, L1813
- "That DAG MUST have exactly one source node, called the origin node." — §DAG of ACDCs, L1821
- "Where a single exchange is to convey several unchained ACDCs, a DAG MUST be formed by issuing a bespoke ACDC whose node is the origin" — §DAG of ACDCs, L1823
- "A well-ordered DAG with a single source node linearizes into a unique, reproducible order." — §Ordering, L1831
- "One such order is that of a breadth-first search from the origin node." — §Ordering, L1833
- "A path is a tuple of components." — §Path Syntax, L1837
- "the components are separated by the path delimiter, `/`, and when serialized compactly as a CESR primitive, by `-`" — §Path Syntax, L1837
- "A path that begins with the path delimiter, `/` (equivalently, whose first component in tuple form is an empty string), is a DAG-absolute path" — §Path Syntax, L1839
- "A path that traverses one or more Edges MUST be in DAG-absolute form, and MUST therefore begin with `/e`" — §Traversing Edges, L1845
- "The hop from that Edge to the top level of the far-side ACDC is denoted by the virtual path component `_`" — §Traversing Edges, L1845
- "Such a path designates the disclosure of that node and the full expansion of every branch beneath it." — §Node Paths and Leaf Paths, L1855
- "A path ending in a non-empty field label or index component designates a single leaf." — §Node Paths and Leaf Paths, L1857
- "The node form is a hammer, the leaf form a scalpel." — §Node Paths and Leaf Paths, L1861
- "A disclosure path translates into a closure over the fields or array elements it implies." — §Closures, L1865
- "The disclosure designated by a set of paths is the union of their closures." — §Closures, L1865
- "A leaf path into such a block therefore closes over every simple field of that block. Its nested sub-blocks stay compacted as their SAIDs." — §Closures, L1869
- "A leaf path to one such block therefore closes over that block alone and tells nothing of any sibling." — §Closures, L1871
- "The top-level Schema Section of an ACDC is always disclosed, so no path need designate it." — §Closures, L1873
- "A closure states what a path discloses. It does not bound what the Disclosee may then do with what it holds." — §Closures, L1877
- "The value of the Disclosure Paths, `dp`, field is a list of tuples." — §Disclosure Paths, `dp`, Field, L1881
- "Each tuple represents one ACDC in the DAG that is the object of the exchange and is of the form `(ACDCSchemaSAID, PathPrefix, [paths])`." — §Disclosure Paths, `dp`, Field, L1881
- "In a serialization that has no distinct tuple type, such as JSON, each tuple MUST be represented as a three-element array." — §Disclosure Paths, `dp`, Field, L1881
- "A list of tuples is used rather than a field map keyed by Schema SAID so that a Schema SAID MAY appear more than once." — §Disclosure Paths, `dp`, Field, L1883
- "The path prefix of a tuple is the DAG-absolute route to the ACDC that the tuple's ACDCSchemaSAID names." — §Path Prefix, L1889
- "A prefix MUST NOT reach past the top level of the ACDC it names." — §Path Prefix, L1889
- "An entry of a path list MUST NOT begin with the path delimiter." — §Path Prefix, L1891
- "The elements of the `dp` list MUST appear in the breadth-first search order of the DAG from its origin node." — §Identifying Each Tuple's ACDC, L1901
- "The zeroth element MUST represent the origin node ACDC." — §Identifying Each Tuple's ACDC, L1901
- "The ordering then has gaps. In that case the prefix of every element after the zeroth MUST be non-empty" — §Identifying Each Tuple's ACDC, L1911
- "an empty list, `[]`, means that the answering path list is the same as the one it answers." — §Solicited Response, L1917
- "Where the answering list differs, or where the message is unsolicited, the `dp` value MUST NOT be an empty list." — §Solicited Response, L1917
- "A path MAY therefore name a block by that label in place of its offset, as in `A/over21`." — §Aggregate Section Pathing, L1923
- "Nothing is ambiguous between the two forms, because a field label MUST NOT begin with a numeral." — §Aggregate Section Pathing, L1925
- "Disclosing part of the inside of a selectively disclosed block mixes Partial Disclosure into Selective Disclosure" — §Aggregate Section Pathing, L1929
- "A simple compact Edge is represented differently within the ACDC, but the path syntax for traversing it is the same." — §Simple Compact Edge, L1935
- "A private Edge MAY therefore require a two-step negotiation" — §Private Edge, L1939
- "An exchange, `exn`, message carries both a query section, `q`, and an attribute section, `a`, so that it can model a ReST request" — §Disclosure Paths in `apply` and `offer`, L2015
- "it MUST appear in that message's query section, `q`, and not in its attribute section, `a`." — §Disclosure Paths in `apply` and `offer`, L2015
- "The `offer` usually carries a Metadata ACDC disclosing the Rule Section of the ACDC on offer" — §Disclosure Paths in `apply` and `offer`, L2019
- "A field label in an ACDC MUST NOT, therefore, contain the character `-`." — §Field Label Restrictions, L63
- "The label `_` MUST therefore be reserved as a virtual path component denoting that hop" — §Field Label Restrictions, L65
- "Only that label is forbidden; `_` MAY appear within a longer label, such as `first_name`." — §Field Label Restrictions, L65
- "They do not reach the labels within the Schema Section." — §Field Label Restrictions, L69
- "Virtual label that denotes the traversal (hop) from an Edge in the near-side ACDC to the top level of the far-side ACDC" — §Other Reserved Fields, L55
- "`E1E`| IssueE-To-IssueE, The Issuee AID of this ACDC MUST be the Issuee AID of the node this Edge points to." — §Edge, L1206
- "This is an identity relation on the two ACDCs' Issuees and places no constraint on either ACDC's Issuer." — §Edge, L1206
- "both the ACDC in which the Edge resides and the node to which the Edge points MUST be Targeted ACDCs" — §Edge, L1223
- "`E1E` binds them as being about the same subject, a relationship the delegative `I2I` Operator cannot express" — §Edge, L1223

### `main` — `[N]`, re-anchored or newly mined at `f0bd097de`
- "a registry SAID, `rd` field that appears nested in the Attributed, `a`, or Aggregate, `A`, section MAY be used for some other registry" — §Registry SAID Field, L85 (**identical at `v1.1` L96**)
- "The inception commits to no credential state: it is a vacuous placeholder that reveals nothing about what will later be issued." — §Registry-Dependent Issuance Lifecycle, L4865-4867
- "Because the SAID is derived from the credential's content, it is not known in advance; it is produced by issuance, not assumed." — §Registry-Dependent Issuance Lifecycle, L4890-4892
- "Only the blinded block's SAID travels in the `bup`; neither the credential SAID nor the word `issued` appears." — §Registry-Dependent Issuance Lifecycle, L4917-4918
- "The registry *events* remain public and chained (the `rd` and prior links are in the clear); it is the state *content* each event commits to that is protected." — §Registry-Dependent Issuance Lifecycle, L4981-4983
- "This is confidentiality of registry state, not anonymity of the credential — issuer, registry, and issuance chronology remain linkable" — §Registry-Dependent Issuance Lifecycle, L4983-4985
- "The verifier does still learn how many elements the section has and which were withheld — the count and positions are structural, not blinded" — §Graduated Disclosure, L5051-5053
- "Under Chain-Link Confidentiality the rule (terms-of-use) section is disclosed first — so a potential Disclosee can agree to the terms" — §Graduated Disclosure, L5078-5080
- "verifies to the same top-level SAID, so what the credential commits to never" — §Graduated Disclosure, L5097

**How to verify the third list.** The Working ACDC Examples region of `spec-body.md` is hard-wrapped in the source at roughly 80 columns, so most of these quotes span two or three physical lines. Each is verbatim once the wrap newlines are replaced by single spaces; every one was checked that way against `f0bd097de` on 2026-09-15. A quote cited to a single line number is verbatim on that line as-is.

## Anti-patterns / outsider-tells the spec explicitly corrects
1. **Direct-signing of credentials (W3C-VC / SD-JWT style):** rejected because key rotation then forces mass revocation and key compromise enables forgery. ACDC binds state to Key State instead (L1673-1675).
2. **Phone-home revocation (OCSP/CRL):** rejected via Observer/Registrar split — no forced Validator→Issuer correlation at PoV (L1693).
3. **Dynamic / URL-dereferenced schemas & schema libraries:** rejected — enable schema-revocation and semantic-malleability attacks; only SAIDified static schema allowed (L194-220).
4. **`$schema` dereferenced for validation code:** "would be an attack vector"; Validator controls tooling dialect (L226).
5. **Treating compact form as private:** a public (no-`u`) compact ACDC is still rainbow-attackable — "compactness, not privacy" (L501).
6. **Bundled multi-claim credentials:** reframed as refactorable into a graph of separately-disclosable chained ACDCs, "obviating the need for Selective Disclosure" (L2739).
7. **Centralized namespace/attribute registries:** unnecessary — content-address + content-addressable schema is the namespace; registries reduce to "schema discovery or blessing" (L2936).
8. **Over-investing in cryptographic unlinkability:** "diminishing returns" without contractually-protected disclosure, because contextual/statistical linkability defeats it (L2785).
9. **Privacy-as-end-goal framing:** reframed to exploitation-protection; privacy is a means (L1659).
