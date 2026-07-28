# ACDC Specification — Doctrine Mining Notes

Source: `/home/daniel/code/kswg-acdc-specification/spec/spec-body.md` (ToIP KSWG ACDC spec, ~4715 lines / ~57k words). This file begins at "## ACDC Structure" (front-matter intro/terminology live in sibling files not covered here). Citations below are `spec-body.md §<heading>` with line numbers.

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
- `rd` Registry Digest SAID — issuance/revocation/transfer/retraction registry (TEL) for the ACDC.
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

- Default inference: if far node **targeted** (has Issuee) → `I2I` appended; if **untargeted** → `NI2I` appended (L1197-1201). `I2I`/`DI2I` require the far node to be Targeted.
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

## Exact short quotes (<=25 words) with citations
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
