# CESR Spec — Doctrine Mining Notes

**Primary source:** `/home/daniel/code/me/kswg-cesr-specification`, file `spec/spec-body.md` (ToIP KSWG CESR Specification). CESR = Composable Event Streaming Representation. Read-only pass. Citations are `file §heading` plus a line hint at a named commit; line hints drift and are hints, not identifiers.

**Pinned commits (mined 2026-09-15):**

- **`main`** — the standardizing line, marker **`[N]`** — at **`bad6edd84`** (`bad6edd84f928fe1e77a722edbdd829e0878377f`, 2026-08-28, "Merge pull request #174 from kordwarshuis/fix/fixed-spec-up-t-version"). 1,565 lines.
- **`v1.1`** — the forward branch, marker **`[N1.1]`** — at **`65fd7518b`** (`65fd7518b6fa318ef3fc700a824b18112b8392e2`, 2026-08-26, "Merge pull request #172 from kordwarshuis/v1.1"). 1,634 lines. `main` and `v1.1` are **divergent**, not ancestor/descendant; their merge base is `7a6adca67`. Neither is reachable from the other.

**Marker key for this note.** Most of this note predates tier marking and its claims are `[N]` — present on the standardizing line. Where a claim is marked explicitly, the marker is load-bearing and the distinction was checked at both pins in this pass. Unmarked claims in sections listed below as *re-anchored* are `[N]` at `bad6edd84`; unmarked claims in sections listed as *not re-read* still carry line hints from the retracted `d35125e` pin and should be treated as unverified line numbers with unverified tier, though their substance was not contradicted by anything read in this pass.

## What the 2026-09-15 pass covered

**The headline is a provenance failure in this note's own post-quantum material, now corrected in §13 and §14.** The note's previous pin, `d35125e`, is **unreachable from every ref** in the source repo — `git branch -a --contains d35125e` returns nothing, `git for-each-ref --contains d35125e` returns nothing, and it is an ancestor of neither `bad6edd84` nor `65fd7518b`. It survives only as a dangling object in one local clone. It is a PR-branch commit ("simplify - only fixed-len sigs, no hash-of-pubkey primitives", Daniel Hardman, 2026-03-18) that was never merged in that form. Everything this note recorded as FN-DSA code assignments therefore rested on a commit that cannot be cited, and none of it is on the standardizing line today. See §13 and §14 for the superseded claims and what replaced them.

**Re-anchored to `main` `bad6edd84`** — these sections were re-read in the source at the commit and their quotes re-verified verbatim, with line hints updated: §Composability (L5, L87), §Conversions / 24-bit alignment (L198), §Stable Framing Codes in the text domain (L202), §Stable value encoding (L216), §Code characters and lead bytes (L232, L234), §Multiple code table approach (L240), §Interleaved non-CESR serializations (L374), §Stream parsing rules (L427, L438), §Compact fixed-size codes (L446), §Code table selectors (L484), §Count Code tables (L581, L591), §Protocol genus/version table and codes (L609, L611, L615, L618, L620, L622), §Universal Code table genus/version codes that allow genus/version override (L812, L816, L818), §Code table entry policy (L783), §Master code table (L865, L866, L874, L926, L949–L1040), §Version String field (L1123, L1125, L1131, L1160), §Self-addressing identifier (SAID) (L1178, L1180, L1182, L1190), §Order-Preserving Data Structures (L1244), §Self-addressing Data (SAD) Path Signatures (L1390, L1393, L1396, L1400, L1404), §Post-Quantum Security (L1501–L1506). The table-structure prose at L519, L523, L539, L545, L553, L563, L569 and the `::: issue` block at L559–L560 were also read at the commit.

**Not re-read this pass** — these still carry `d35125e`-era line hints and were not verified at either new pin: §Text Code Size pad-size arithmetic (the L252–L280 block), §Pre-padding worked examples (L286–L358), §Cold start Stream parsing problem and the tritet table (L380–L420), §Small/Large Count Code table row detail (L594–L605), §OpCode tables (L626–L628), §Encoding scheme table and symbols (L640–L676), §Parsing via table design (L718–L778), the universal and KERI/ACDC count-code row inventories (L826–L854, L909–L946), the two-character matter code rows beyond `0S`, the §Examples nested-group walkthrough (L1101–L1126), the Version String part-by-part breakdown (L1132–L1154), the SAID generation/verification steps and worked examples (L1192–L1382), and the SAD Path Language detail (L1408–L1504). Their substance is unchallenged by anything read this pass, but the line numbers will be wrong by roughly the offsets noted in §17.

---

## 1. What CESR fundamentally IS / IS NOT (worldview & design intent)

- **CESR is a dual text-binary encoding format whose defining, "unique property" is text-binary *concatenation composability*.** (§Self-addressing Data (SAD) Path Signatures intro, L1390; §Composability L5 — both re-verified at `main` `bad6edd84`.) This is the root claim from which everything else derives.
- **CESR is NOT limited to cryptographic material.** "The CESR protocol, however, is not limited to merely encoding Cryptographic Primitives but any primary data type (numbers, text, datetimes, lists, maps) may be encoded in a composable way." (§Abstract Domain representations, L11.) It is a *general* primary-datatype encoding, not a crypto-only wire format.
- **CESR was developed FOR KERI.** "CESR was developed for the KERI protocol." (§Self-addressing identifier (SAID), L1180, re-verified — it is the closing sentence of the derivation-code paragraph); "The CESR specification not only provides the definition of the streaming format but also the attachment codes needed for differentiating the types of cryptographic material...used as attachments on all event types for the KERI." (§Self-addressing Data (SAD) Path Signatures, L1390, re-verified.) CESR is the encoding substrate of the KERI/ACDC/TSP stack.
- **The encoding is an EXTERNAL INTEROP CONTRACT, not an implementation detail.** The whole "Composability" contract (L5–7) is that *any compliant implementation* must round-trip *any* set of concatenated primitives T↔B losslessly, en masse. "All compliant encoded Primitives MUST be Composable. All compliant encoded Primitives MUST be self-framing." (L5.) "All compliant implementations MUST support the transformations between all three domains." (L31.) Interop is normative, not best-effort.
- **Design aesthetic: minimally-sufficient strength, no waste.** "there is minimally sufficient cryptographic strength and more cryptographic strength just wastes computation and bandwidth." (§Compact fixed-size codes, L446.) 128 bits of entropy is the accepted floor.
- **Text-first design for human usability; binary purely for compactness.** "A primary design goal of CESR is to select an encoding approach that provides high usability, readability, or human friendliness in the 'T' domain. This type of usability goal simply is not realizable in the 'B' domain. The 'B' domain's purpose is merely to provide convenient compactness at scale." (§Stable Framing Codes, L202.)

---

## 2. The Three Domains (T, B, R) — precise terminology

- **Text domain 'T'** = streamable text; **Binary domain 'B'** = streamable binary; **Raw domain 'R'** = non-streamable binary, represented as a *pair/two-tuple* `(text code, raw binary)` a.k.a. `(code, raw)`. (§Abstract Domain representations, L11.)
- Composability is defined ONLY between T and B. R is special: "The actual use of Cryptographic Primitives happens in the 'R' domain using the raw binary element of the `(code, raw)` pair." (L11.)
- **Six transformations** among three domains, one per direction: `T(B)`, `B(T)`, `T(R)`, `R(T)`, `B(R)`, `R(B)` — each pair is dual. (§Transformations between Domains, L17–31.) Full circuits possible, e.g. `R->T(R)->T->B(T)->B->R(B)->R` (L40).
- Key interop payoff: `T(B)` is naive Base64 *encode*, `B(T)` is naive Base64 *decode* — "CESR Primitives are compatible with existing Base64 (RFC-4648) tooling." Only R↔T and R↔B need new tooling. (§Text Code Size, L266.)
- Notation: `t`, `b`, `r` for a primitive in each domain; `t[k]`, `b[k]`, `r[k]` for indexed members. (L13.)

---

## 3. Composability — the core invariant

- **Definition:** "An encoding has Composability when any set of Self-Framing concatenated Primitives expressed in either the Text domain or Binary domain may be converted as a group to the other Domain and back again without loss." (§Composability, L5.)
- **Formal (concatenation) statement:** `T(B)` and `B(T)` are jointly concatenation composable iff `T(cat(b[k]))=cat(T(b[k]))` and `B(cat(t[k]))=cat(B(t[k]))` for all k. (§Concatenation composability property, L70.) I.e. "the transformation of a set (as a whole) of concatenated Primitives is equal to the concatenation of the set of individually transformed Primitives." (L73.)
- **INVARIANT:** "Each and every Primitive or Count Code group of primitives MUST satisfy the Concatenation Composability property." (L73.) "All Count Code groups...MUST be Composable...MUST be self-framing." (L7.)
- **Self-framing is what enables de-concatenation.** "The self-framing property of the primitives enables de-concatenation." (L87.) A parser reads the first char/byte → index into a lookup table → knows how many remaining chars/bytes to consume. "This makes the Primitive self-framing." (§Examples of pre-padding, L358.)
- **Why naive Base64 fails composability:** standard Base64 pads each individual conversion to a multiple of 4 chars, giving only "one-way composability" (separable but not round-trippable en masse). "standard (naive) Base64 does not provide two-way or true Composability." (§Text Code Size, L252; also L95, L139.) En-masse conversion of concatenated binary can put bits from two adjacent primitives into one text char (L184) — boundaries are lost.
- **CESR does NOT use the `=` pad character for any purpose** "because all CESR-encoded Primitives are composable." (§Concrete Domain representations, L93.)

### 3a. The 24-bit alignment rule (the math backbone)
- **INVARIANT:** "all Primitives MUST be aligned on 24-bit boundaries to satisfy the Composability property." (§Conversions, L198.) 24 = LCM(6,8) = least common multiple of Base64's 6 bits/char and a byte's 8 bits. (L196.)
- Therefore: every B-domain primitive length MUST be an integer multiple of **3 bytes** (min 3); every T-domain primitive length MUST be an integer multiple of **4 Base64 chars** (min 4). (L198.)
- **Pad-size formula:** `ps = (3 - (N mod 3)) mod 3`, where `ps` = pad size and `N` = raw binary length in bytes. (§Text Code Size, L264.) The number of leading pre-pad zero *bytes* equals the number of trailing post-pad *characters* for the same N. (L260.)
- Pad-size → code-size table: pad 0 → code `4•M`; pad 1 → `4•M+1`; pad 2 → `4•M+2`; min code sizes 4,1,2 chars respectively. (§Example of pad size computation, L276–280.)

### 3b. Mid-padding (a "never do" design choice)
- Two ways to hit 24-bit alignment: (1) post-pad trailing `=` chars (naive Base64), or (2) **pre-pad leading zero bytes to the raw before conversion** ("lead bytes"). CESR chose (2). (§Code characters and lead bytes, L220–232.)
- Term "lead bytes" used deliberately instead of "pad" to avoid confusion; # lead bytes (pre-conversion) == # pad chars (post-conversion). (L226.)
- **INVARIANT:** "all CESR primitives MUST employ mid-padding as defined." (L234.) Consequence: any zero padding appears in the *middle* of the primitive — after the type code, before the value. (§Stable value encoding, L214.) This keeps the value right-aligned and readable.

---

## 4. Stable Framing Codes — usability doctrine

- **Stable type coding (INVARIANT):** "The type portion of all compliant prepended Framing Codes MUST be stable in the Text domain." "the leading characters that determine the type do not change when any other portion of the primitive changes." (§Stable type encoding, L202, L206.) Type MUST come first and consume a fixed integral number of T-domain chars (L210). Type never shares information bits with length/value coding in any T-domain char.
- Stability is imposed on the **T domain, not B**, deliberately: binary parsers handle bit-fields/shifts easily, text parsers only whole chars. "This is another reason to impose a stability constraint on the 'T' domain type coding instead of the 'B' domain." (L208.) T→stable type translates to B stable type "except that the type coding portion...MAY or MAY NOT respect byte boundaries."
- **Stable value coding (INVARIANT):** "the value portion of any primitive MUST be right aligned." (§Stable value encoding, L216.) Readable small numbers: decimal `0,1,2` ↔ Base64 `A,B,C` (L214).
- **Each code table is keyed by the first char:** "Each code table MUST be uniquely indicated by the first character of the type code in the 'T' domain." (§Multiple code table approach, L240.) Single integrated parse+conversion table; parsing = read the type selector, then you know how to parse/convert the rest. (L238.)

---

## 5. Multiple code table design + crypto agility (how a new algorithm claims a slot without desync)

- **Rationale for multiple tables:** minimize framing-code size for *popular* codes while supporting a comprehensive/extensible set for all foreseeable future codes. Achieved with multiple tables each optimized differently — not one-size-fits-all. (§Multiple code table approach, L238.)
- **The "sweet spots":** 32-byte raw (pad 1 → 1-char code) and 64-byte raw (pad 2 → 2-char code) are the cryptographic sweet spots (EdDSA/ECDSA keys, digests, signatures). Optimized 1- and 2-char tables target these. (§Compact fixed-size codes, L450–474.)
- **Code table selectors (§Code table selectors, L476–487):** 64 Base64 chars; only 12 needed as table selectors → 52 chars left for 1-char type codes in default table → 13 tables total. Assignment:
  - `-` = Count Code table selector (MUST).
  - `_` = Op Code table selector (MUST, reserved TBD).
  - `[A-Z,a-z]` = single-char type codes (default table, 52 codes, pad size 1).
  - `[0-9]` = selectors for the other 10 tables.
  - "The first character of any Primitive MUST be either a selector or a 1-character code type." (L484.)
- **CRYPTO AGILITY doctrine — how a new algorithm claims an unused slot:** The derivation/type code encodes the crypto suite. "The CESR derivation code enables cryptographic digest algorithm agility in systems that use SAIDs as content addresses. Each serialization may use a different cryptographic digest algorithm as indicated by its derivation code. This provides interoperable future-proofing." (§Self-addressing identifier (SAID), L1180 at `main` `bad6edd84`, re-verified.) A new algorithm = a new *entry* (previously-unused code point) in a table; old parsers that don't know the code simply don't recognize that primitive but the *framing math is unchanged*, so the stream doesn't desync for primitives they DO know.
- **Backward-compat semantics of adding codes `[N]` (§Protocol genus/version codes, L618–L622 at `main` `bad6edd84`, all three re-verified verbatim and unmoved):** this is the asymmetry the rest of the corpus leans on, and it is the reason §14a's post-quantum codes are a *minor* change rather than a major one, if and when they land.
  - "Any addition of a new code to the code table is backward-breaking in at least one direction... New implementations with the new codes can accept streams from old implementations, but old ones will break if they receive the new ones." (L618.)
  - **Major change** = "a code's meaning changes" → increment MAJOR version → breaks BOTH directions. (L620.)
  - **Minor change** = "a code is added to a table" → increment MINOR → only breaks new-sender→old-receiver; new receiver still handles old streams. (L622.) More minor room than major deliberately (4096 minor per major).
- **Entry policy `[N]` (§Code table entry policy, L783 at `main` `bad6edd84`):** first-needed-first-entered; compact tables require ≥128-bit crypto strength — "This precludes the entry of many weak cryptographic suites into the compact tables." — and admit "only best-of-class cryptographic operations along with common non-Cryptographic Primitive types."
  - On post-quantum, the standardizing line as of `bad6edd84` says only: "there is the expectation that the National Institute of Standards and Technology (NIST) soon will approve standardized post-quantum resistant cryptographic operations." Falcon is named once, as a candidate: "Falcon appears to be among the leading candidates with open-source code already available."
  - ~~Post-quantum FN-DSA (Falcon) primitives are being introduced "in successive updates" — chosen for most-compact PQ sigs/keys, "of particular interest to bandwidth-sensitive protocols such as KERI."~~ **SUPERSEDED 2026-09-15.** Both quoted fragments came from the unreachable `d35125e`, not from any branch tip, and neither string appears anywhere in `spec/spec-body.md` at `main` `bad6edd84`. The standardizing line's wording is *older*, not newer, than what this note recorded — it still anticipates NIST approval that in fact landed in August 2024. The forward branch replaced this paragraph outright with a scarcity argument and a normative placement rule; see §5a and §13a.

### 5a. Compact-table scarcity as normative policy `[N1.1]` (v1.1 `65fd7518b`, §Code table entry policy, L785–L791)

This is new doctrine on the forward branch and has **no counterpart on `main` at `bad6edd84`**. It converts what was an aesthetic preference (§1, "minimally sufficient strength, no waste") into a normative allocation rule for the code-table namespace itself.

- **The compact tables are declared a scarce resource, with the numbers stated.** "The one- and two-character code tables are a scarce resource. The one-character table provides only 52 codes in total, and the two-character table only 64." (L785.) Against 262,144 codes per four-character table.
- **The admission test for a compact code is relative overhead, not importance.** "entries in the one- and two-character tables MUST be reserved for Primitives whose raw size is small enough that a longer code would materially increase the size of the encoded Primitive." (L785.) A four-character code on an 892-character primitive is "a relative overhead below one half of one percent."
- **Normative exclusion of PQ from the compact tables (INVARIANT):** "Post-quantum codes MUST therefore be placed in the four-character fixed tables given by the `1`, `2`, and `3` selectors, and MUST NOT consume entries in the one- or two-character tables." (L785.) The stated second reason is namespace headroom: the policy "accommodates the large number of parameter sets that post-quantum algorithm families define, without exhausting the compact tables."
- **Which of the three four-character tables a primitive lands in is arithmetic, not design.** "Which of the three four-character fixed tables a given Primitive occupies is not a matter of choice. It is determined by the raw size of the Primitive modulo 3." (L787.) Raw size ≡ 0 mod 3 → 0 lead bytes → selector `1`; ≡ 2 mod 3 → 1 lead byte → selector `2`; ≡ 1 mod 3 → 2 lead bytes → selector `3`. This is the 24-bit alignment rule of §3a surfacing as a table-assignment constraint.
- **Consequence the spec draws out itself:** "the Primitives belonging to a single algorithm are commonly distributed across more than one table" (L787), the analogy given being that an Ed25519 public verification key uses `D` while an Ed25519 signature uses `0B`. So "which table is this code in" carries no semantic information about the algorithm — only about the raw length mod 3. A reader who infers an algorithm grouping from a selector is reading the wrong thing.
- **Parameter-set admission is deliberately restrictive, on an ecosystem-scrutiny argument.** "Admitting every variant of an algorithm invites the use of variants that have received little implementation scrutiny, which weakens rather than strengthens the security of the ecosystem." (L791.) Of the twelve SLH-DSA parameter sets FIPS 205 defines, "Only the six `s` parameter sets have entries below." (L791.) The `f` (fast-signing) variants are rejected on a traffic argument: they "trade roughly a factor of two to three in signature size for signing speed" (L791), which the spec calls "the wrong trade for a protocol whose signatures are transmitted and archived far more often than they are generated" (L791).

---

## 6. Sizing math — the table taxonomy

Two major raw-primitive types: **fixed-length** and **variable-length**. Plus count-code, genus/version, opcode, and context-specific tables. (§Table types, L493–499.)

### Fixed-length raw-size tables (§L503–531)
- **1-char table** (`[A-Z,a-z]`): 52 codes, pad size 1 (32-byte sweet spot). No selector char per se.
- **2-char table** (selector `0`): 64 codes, pad size 2 (64-byte sweet spot).
- **Large fixed, selectors `1`/`2`/`3`** = 0/1/2 lead bytes (pad 0/1/2); 4-char codes; 3 type chars → 262,144 (`64**3`) codes each. Selector "implicitly encodes the number of lead bytes."

### Variable-length raw-size tables (§L533–577)
- Size measured in **Quadlets** (4 T-chars) / **Triplets** (3 B-bytes) — the 24-bit unit. T count = size×4 chars; B count = size×3 bytes.
- **Small var, selectors `4`/`5`/`6`** (0/1/2 lead bytes): 4-char code = selector + 1 type + 2 size chars. 64 types; size up to 4095 quadlets (`64**2−1`) = 16,380 chars / 12,285 bytes.
- **Large var, selectors `7`/`8`/`9`** (0/1/2 lead bytes): 8-char code = selector + 3 type + 4 size chars. 262,144 types; size up to 16,777,215 quadlets (`64**4−1`) = 67,108,860 chars / 50,331,645 bytes. First 62 entries mirror the small-var types so one type can use the shorter 4-char code when small.

### Encoding Scheme Table (§L640–658) — format symbols
- `*` selector-code char also gives type; `$` type-code char; `%` lead byte; `#` Base64 digit (size/count); `&` value char. (§Encoding scheme symbols, L668–676.) E.g. small-var-0-lead format `*$##&&&&`; large-var-2-lead `*$$$####%%&&`.
- Special fixed-size codes may carry the value *inside* the code's value-size part (compact tags/versions) — raw part MAY be empty. (L660.)

### Parse tables (§L718–778)
- Parser flow: first-char selector → hard-size (`hs`) → extract hard chars → index parse-size table → get remaining sizes → extract/convert. Same table works in B domain (each size = sextets not chars). (L720.)
- Parse part labels (L765–778): `hs` hard size (fixed), `ss` soft size (variable), `os` other size, `ms` main size (`ss−os`), `cs` code size (`hs+ss`), `vs` value size, `fs` full size (`hs+ss+vs`), `ls` lead size (bytes), `ps` pad size, `rs` raw size (from `R(T)`), `bs` binary size (`ls+rs`).

---

## 7. Count / Group Framing Codes (grouping, pipelining)

- **Count Codes (a.k.a. Group Codes) count Quadlets/Triplets in a group, not primitives.** "always counts the number of quadlets/triplets in the group not the number of primitives." (§Count Code tables, L591.) They enable pipelining (multiplex/demultiplex), core-affinity offloading, and hierarchical (group-of-groups) composition. (§Count or Group Framing Codes, L362; §Composability L7.)
- A Count Code is itself a composable Primitive with **no raw value, only its text code**; pad size always 0; length is a multiple of 4 chars / 3 bytes. (L364, L591.)
- **INVARIANT — count is domain-invariant:** because the count is in quadlets/triplets (both = 24 bits), "the count value is invariant between 'T' and 'B' Domains...MUST be the number of Quadlets in the 'T' domain and the number of Triplets in the 'B' domain." (L581.) This lets a parser "extract the number of characters/bytes in a group from the Stream without parsing the group's contents; it is therefore pipeline-able." (L583.)
- **INVARIANT:** "Count Codes MUST NOT have a value component but MUST have only type and size components." "Each element in content of a Count Code group MUST be aligned on a 24-bit boundary. Thus the only elements allowed in the contents of a Count Code group are other primitives or groups." (L591.)
- Nested selectors: first selector always `-`. Second char: letter `[A-Z,a-z]` → single-char count code (52 total); numeral/`-`/`_` → secondary table selector. (L594.)
- **Small Count Code table:** `-` + type letter + 2 size chars = 4 chars; counts 0–4095. (§Small Count Code table, L599.)
- **Large Count Code table:** `--` + 1 type + 5 size chars = 8 chars; 64 types; counts 0–1,073,741,823 (`64**5−1`) → groups up to ~4.29e9 chars / 3.22e9 bytes. (§Large Count Code table, L605.)

---

## 8. Protocol genus/version table (versioning the code tables themselves)

- **The genus/version code does NOT count anything — it MODIFIES which code tables the parser uses.** "A protocol genus and version code itself MUST NOT provide a count of the following Quadlets or triplets but MUST modify the protocol genus and Version of all the following Count Codes." (§Protocol genus/version table, L609.)
- Format: **`-_GGGVVV`** (8 chars) — `-_` selector, `GGG` = 3-char genus (262,144 possible genera), `VVV` = version where first `V` = major, last `VV` = minor. E.g. `CAA` = 2.00, `CAQ` = 2.16. Up to 64 majors × 4096 minors. (§Protocol genus/version codes, L615.)
- **Purpose (twofold):** (1) lets CESR serve different protocols/stacks each with their own code tables; (2) versions the code tables for a given protocol. "The only table that all protocols MUST share (i.e., has identical values) is the protocol genus and version table." All small/large count tables must share the *universal* count codes; everything else MAY vary by protocol. (L611.)
- **Scope/override rule (INVARIANT):** a genus/version code applies to following count codes at top level *until another genus/version code appears*, OR inside a special enclosing count code group. Only THREE universal enclosing count codes allow an embedded genus/version override. (L609.)
- **Override only fires in overrideable universal count codes.** "the parser MUST only treat the genus/version count code, especially as an override, when it appears as the first count code within the framed material of an overrideable universal count code. Otherwise, there MUST be no special override meaning." (Universal genus/version override, L816.) Inside a *list* (universal but non-overrideable), a genus/version code as first element has NO override semantics. (L818.)

---

## 9. Streaming, cold start, and interleaving (the elegant parse formula)

- **Cold-start problem:** after cold start a parser looks for framing info; ambiguity → confusion → forced re-cold-start (TCP: close/reopen; UDP: ack/nack). "Good cold start re-synchronization is essential to robust performant Stream processing." Goal: resync by skipping to next well-defined boundary, not flushing buffers. (§Cold start Stream parsing problem, L380–384.)
- **A CESR parser MUST support three interleaved non-CESR serializations: JSON, CBOR, MGPK.** (§Performant resynchronization, L388.)
- **Unique start-bits doctrine (BOM-analogue):** boundary start bits for interleaved text-CESR, binary-CESR, JSON, CBOR, MGPK "MUST be mutually distinct." (L390.) This gives a UTF-BOM-like ability to tell T vs B domain from the first tritet. (L390, L402.)
- **The 8 starting Tritets (3 bits) — Top-level Stream Starting Tritets table (L411–420):**
  - `0b000` Annotated 'T' domain (whitespace: LF/CR/tab all start `0b000`) (L404)
  - `0b001` CESR 'T' Count Code — char `-`
  - `0b010` CESR 'T' Op Code — char `_`
  - `0b011` JSON — `{` (0x7b)
  - `0b100` MGPK FixMap
  - `0b101` CBOR Map "Major Type 5"
  - `0b110` MGPK Map16/Map32
  - `0b111` CESR 'B' domain Count Code or Op Code
  - Rationale: JSON/CBOR/MGPK map objects consume tritets `011,100,101,110`; the free ones are `000,001,010,111`. Base64 `-`(0x2d, `001`) and `_`(0x5f, `010`) fit for T-domain; their binary forms (positions 62/63 → `0b111`) mark B-domain. (L392–404.)
- **INVARIANT:** "The starting tritet of any cold start (restart) MUST begin with one of eight cases." (L406.) "Each Stream MUST start (restart) with one of eight cases." (§Stream parsing rules, L427.)
- **The parse formula:** examine the first tritet of the first byte → determine which of 8. If Count Code, the rest of the code carries what's needed to parse the group. If JSON/CBOR/MGPK, "the mapping's first field MUST be a Version String" providing type+length for regex extraction. (L438.) "This provides an extremely compact and elegant Stream parsing formula." (L442.)
- **Interleaving rule (INVARIANT):** non-native (JSON/CBOR/MGPK) serializations may be interleaved with native CESR **only at the top level** of a stream. "This is NOT true for non-native serializations nested inside CESR groups." When nested, "a non-native CESR serializations MUST be encoded as a CESR primitive and then enclosed in a special count code for non-native messages." (§Interleaved non-CESR serializations, L374–376.)

---

## 10. Version String (interleaved non-CESR framing)

- **INVARIANT:** interleaved JSON/CBOR/MGPK MUST have a Version String as the first field, label `v` (lowercase). (§Version String field, L1123, L1125 at `main` `bad6edd84`, re-verified.) It's the regex target for serialization type + size.
- **v2 format: `PPPPMmmGggKKKKBBBB.`** — 19 chars, five parts: (L1131, re-verified; the part-by-part breakdown below was *not* re-read)
  - `PPPP` protocol (e.g. `KERI`, `ACDC`)
  - `Mmm` protocol major/minor version (base-64 numeric; `M`=major, `mm`=minor)
  - `Ggg` CESR genus-table version (base-64 numeric)
  - `KKKK` serialization kind: `JSON`|`CBOR`|`MGPK`|`CESR`
  - `BBBB` total serialization length in Base64 (inclusive)
  - `.` terminator (v2). Max size `64**4 = 2**24 = 16,777,216` chars; larger → chain via SAIDs. (L1156.)
- **"base 64 numerical notation" ≠ "string encoded in Base64":** a base-64 *number* where each digit is 0–63 (`A`=0, `_`=63), positionally weighted. (L1152.)
- **CESR-native field maps carry NO embedded version string.** They use `-G##`/`--G#####` count codes for map-ness + size; unique start bits mean no regex version string is needed. A native map has a *protocol version field* (protocol+version, not size/kind). In-memory it may inject a placeholder `v` with kind `CESR` so re-serialization knows to emit native CESR. "there is no normative indication that the in-memory object was deserialized from a CESR native field map." (L1154.)
- **v1 legacy format: `PPPPvvKKKKllllll_`** — 17 chars; `vv` two-char hex major/minor; `llllll` length in lowercase hex; `_` terminator. v2 implementations MUST support v1 to verify 1.XX events. (§Legacy Version 1.XX string field format, L1160 at `main` `bad6edd84`, header and format line re-verified; the parts breakdown through ~L1174 was not re-read.)
- The `.` terminator's purpose: let future versions change the version-string size while preserving regex extractability. (L1158.)

---

## 11. SAID — Self-Addressing Identifier (definition + doctrine)

- **Definition:** "A SAID (Self-Addressing Identifier) is a special type of content-addressable identifier based on an encoded cryptographic digest that is self-referential." (§Self-addressing identifier (SAID), L1178 at `main` `bad6edd84`, re-verified.) It is embedded *inside* the very serialization it identifies.
- **Why a special derivation is needed:** a naive content-address is a digest of the finished content, so it "must not be self-referential" — you can't put a digest inside the thing you're digesting without changing the digest. SAID solves this with a dummy-string derivation protocol. (L1190, L1192.)
- **Root-of-trust claim:** "The primary advantage of a content-addressable identifier is that it is cryptographically bound to the content...thus providing a secure root-of-trust for reasoning about that content. Any sufficiently strong cryptographic commitment to a content-addressable identifier is functionally equivalent to a cryptographic commitment to the content itself." (L1182, re-verified. The two sentences are 24 and 25 words respectively — quote one, not both.)
- **Security argument against non-bound self-referential IDs (anti-pattern):** an identifier that is self-referential but NOT cryptographically bound is "a security vulnerability" — "Anyone can place such an identifier inside some other serialization and claim that the other serialization is the correct serialization." SAID removes the two-identifier ambiguity by being both self-referential AND bound. (L1190, re-verified; this and the immutability claim below are now the same paragraph.)
- **Immutability:** "a SAID will verify if and only if its encompassing serialization has not been mutated, which makes the content immutable." Enables tamper-evident reasoning and reference-by-SAID instead of embedding. (L1190, re-verified.)
- **SAID MUST be a CESR primitive** with a prepended derivation code (crypto agility). (L1180, re-verified; L1192 not re-read.)
- **Verification protocol (INVARIANT sequence, §Generation and Verification Protocols, L1200–1206):**
  1. Copy the embedded SAID.
  2. Replace SAID field value with dummy `#` (ASCII 35/0x23) of same length.
  3. Compute digest of dummied serialization using the algorithm from the copied SAID's derivation code.
  4. CESR-encode the digest → same total length.
  5. Compare; identical → verified.
- **Worked examples:** fixed-field 76-char string → Blake3-256 SAID `ENI2bDYghiu1KYYkFrPofH8tJ5tNiNt8WrTIc4s_5IIH` (44 chars, first char `E`=Blake3-256) (L1210–1237); Python dict `{said,first,last,role}` → `EJymtAC4piy_HkHWRs4JSRv0sb53MZJr8BQ4SMixXIVJ` with `json.dumps(..., separators=(",",":"), ensure_ascii=False)` (L1262–1310); JSON Schema `$id` SAIDification → `EGU_SHY-8ywNBJOqPKHr4sXV9tOtOwpYzYOM63_zUCDW` (L1332–1382).
- **SAD = Self-Addressing Data:** "When a SAID is used for some field map data structure the enclosing data-structure is called self-addressing data (SAD)." (L1385.)

### 11a. Canonicalization / field ordering doctrine
- **Reproducibility requires fixed field ordering & sizing.** "The crucial consideration in SAID generation is reproducibility. This requires the ordering and sizing of fields in the serialization to be fixed." (L1246.)
- **KERI/ACDC uses INSERTION ORDER (field-creation order), NOT lexicographic ordering.** "The natural canonical ordering for such mappings is insertion order." Insertion order lets field presence/absence and priority carry meaning; lexicographic ordering "appears un-natural" and forces "oddly-labeled fields...merely to ensure that the lexicographic ordering matches a given logical ordering." (§Order-Preserving Data Structures, L1244 at `main` `bad6edd84` for the insertion-order sentence, re-verified; the "un-natural" and "oddly-labeled fields" fragments sit later in the section and were *not* re-read this pass.) This is a pointed rejection of JCS-style lexicographic canonicalization.
- Modern languages preserve insertion order natively (Python 3.6+ dict, Ruby 1.9+ Hash, JS ES6 Map / ES11 stringify) → "there is no need for any canonical serialization but natural insertion order." (L1256.)

---

## 12. SAD Path Signatures (transposable nested signatures)

- Extension to CESR for **transposable cryptographic signature attachments on SADs.** A signed SAD embedded in another SAD keeps integrity; the attachment's paths update by changing only the root path. (§Self-addressing Data (SAD) Path Signatures, L1390, L1396, L1400 at `main` `bad6edd84`, re-verified.)
- **Nested partial signatures:** sign any subset(s) of a SAD, up to the whole; grouped under one attachment via a new Count Code + a SAD Path. (§Nested Partial Signatures, L1396, re-verified.)
- **Motivation:** KERI events (`exn`, `rpy`, `exp`) carry embedded SADs; a normally CESR-signed SAD isn't embeddable in JSON/CBOR/MGPK maps, so transposable path-signatures solve it. (§Transposable Signature Attachments, L1400, re-verified.)
- **SAD Path Language (§SAD Path Language, L1402 heading / L1404–L1435 body at `main` `bad6edd84`; heading and opening paragraph re-verified, the detail below *not* re-read):** single reserved char `-` (dash) as path separator (like `/` in URLs), chosen because it's Base64-valid. Root path = `-`. Components are field labels OR integer indices (indices exploit static field ordering → works even when labels aren't Base64-safe). No wildcards. Root context is always a map. Error if a sub-path resolves to non-map/non-array. Chosen over JSONPtr/JSONPath for compactness — "Alternative syntaxes would need to be Base64 encoded...incurring the additional bandwidth cost." (L1504.)
- **CESR encoding:** SAD Paths use small variable-size codes `4A##`/`5A##`/`6A##` (0/1/2 lead bytes), reserved for Base64-only text values; up to 16,380 chars / 12,285 bytes. (L1443.)
- **Worked ACDC example** (Fig 1, L1449–1500) shows paths like `-a-personal` → `4AADA-a-personal`, `-5-3-name` → `6AADAAA-5-3-name`.

---

## 13. Post-Quantum Security (doctrine + pre-rotation link)

### 13a. The hash-firewall doctrine — this part is `[N]` and unchanged

Present verbatim on both branches. §Post-Quantum Security, L1501–L1506 at `main` `bad6edd84`; identical text at L1544–L1549 on `v1.1` `65fd7518b`.

- **Definition:** post-quantum / quantum-safe crypto maintains strength against quantum attackers, designed for a future when practical quantum computers exist. (L1502.)
- **Hash-based PQ argument (Bernstein):** "quantum computation provides no advantage over non-quantum techniques" for collision resistance of hashes. So hiding material behind a digest gives PQ security. (L1502.)
- **Pre-rotation as PQ firewall:** "Instead of a pre-rotation making a cryptographic pre-commitment to a public key, it makes a pre-commitment to a digest of that public key." (L1504.) A PQ attacker must first invert the digest (non-quantum) before inverting the key (quantum) — so "Pre-quantum cryptographic strength is, therefore, not weakened post-quantum. A surprise quantum capability may no longer be a vulnerability." (L1506.) 256-bit Blake2/Blake3/SHA3 keep 128-bit strength post-quantum. Hiding keys imposes NO extra storage burden (controller must reproduce private keys anyway).
- **Scope boundary the standardizing line does not state, and the forward branch does.** At `main` `bad6edd84` the section stops here. Everything CESR says about post-quantum on the standardizing line is the hash firewall; there is no PQ signature primitive of any kind. The word "FN-DSA" does not occur in the file, nor does "FIPS", nor any of `1AAQ`, `1AAR`, `2AAA`. Verified by exhaustive search at the commit.

### 13b. ~~FN-DSA (Falcon) codes (L1514)~~ — SUPERSEDED 2026-09-15

~~PQ keys/sigs use fixed-length encodings per FIPS 206. Pubkeys: `1AAQ` (FN-DSA-512, 897B raw/1200 qb64), `b` (FN-DSA-1024, 1793B/2392). Sigs zero-padded to max & fixed-size: `1AAR` (FN-DSA-512, 666B/892), `e` (FN-DSA-1024, 1280B/1708). Seeds: `c`/`d` (both 32B/44). Compact AID from FN-DSA key = apply existing digest code (e.g. `E` Blake3-256) to the pubkey; context determines meaning.~~

**Why it is superseded, and how it got in.** This paragraph was mined from `d35125e:spec/spec-body.md` L1514, and it is an accurate reading of that file. The failure is upstream of the reading: `d35125e` is reachable from no ref, so the claim was never confirmable as standardizing-line text at a nameable commit. It should never have been recorded as if it were. **Two things replaced it, and they point in opposite directions:**

1. **On `main` `bad6edd84`, nothing replaced it.** There is no FN-DSA material at all. A reader who took this note's word for it would have believed the standardizing line carried PQ codes it has never carried.
2. **On `v1.1` `65fd7518b`, a much larger treatment replaced it — and reversed the compact-code half of it.** The one-character assignments `b`, `c`, `d`, `e` are gone; the one-character table still ends at `a` (blinding factor) on both branches. Their contents moved to the four-character `2` table under the new normative rule of §5a. The replacement map, read at `v1.1` L1036–L1039:
   - `b` FN-DSA-1024 public verification key → **`2AAA`** (2396 qb64, not 2392 — the four-char code and the one lead byte change the arithmetic)
   - `e` FN-DSA-1024 signature → **`2AAB`** (1712 qb64, not 1708)
   - `c` Seed of FN-DSA-512 private key → **`2AAC`** (48 qb64, not 44)
   - `d` Seed of FN-DSA-1024 private key → **`2AAD`** (48 qb64, not 44)
   - `1AAQ` and `1AAR` survive unchanged, at the same sizes, because 897 and 666 are both ≡ 0 mod 3.

**The general lesson, and it is not a small one.** A pin that resolves is not a pin that is citable. `git rev-parse` succeeds on any object still in the local store, including one on a deleted PR branch, and a mining pass that only checks "does this SHA resolve" will happily anchor a claim to a commit nobody else can fetch. The reachability check — `git branch -a --contains <sha>`, or `git for-each-ref --contains <sha>` — is the one that answers "can a reader get here". Run it on every pin before mining, not after.

### 13c. The v1.1 post-quantum treatment `[N1.1]` (§Post-Quantum Cryptographic Primitives, L1551–L1559 at `65fd7518b`)

A subsection with no counterpart on `main`. Its argumentative shape matters as much as its codes: it opens by naming the limit of the hash firewall rather than by announcing new codes.

- **The firewall's limit, stated plainly.** "Hiding pre-rotated keys behind digests, as described above, protects the next key pair but does not protect the currently exposed one." (L1553.) A protocol "that must resist a quantum adversary in the present tense needs post-quantum signature Primitives directly." This is the first place in the corpus where CESR concedes that pre-rotation alone is not a complete PQ answer.
- **The two mechanisms are stacked, not substituted.** "The two mechanisms are complementary, not alternatives; pre-rotation continues to provide defense in depth for whichever signature scheme is in use." (L1553.)
- **Three schemes admitted, one deferred.** Codes are defined for FN-DSA (FIPS 206), ML-DSA (FIPS 204) and SLH-DSA (FIPS 205). (L1553.)
- **Fixed-size encoding is the rule, and FN-DSA is the only case where it costs anything.** "Every post-quantum signature code defined in this specification encodes a signature of fixed raw size. FN-DSA is the only one of the three schemes whose native signature encoding is variable in length." (L1555.) The codes encode the FIPS 206 *padded* format — 666 bytes for FN-DSA-512, 1280 for FN-DSA-1024.
- **Three reasons a variable-length FN-DSA encoding was rejected (L1555), each worth keeping separate:**
  1. **Parser burden.** "A variable-length encoding obliges the parser to consult a length field rather than the code alone" — in order, the sentence continues, to determine both how many bytes to consume and which verification routine to dispatch to. This is the self-framing property of §3 defended by name: a variable-length signature code would make the code insufficient to frame the primitive.
  2. **Fixed-field embedding.** "it prevents a signature from occupying a fixed-size field in an enclosing verifiable data structure."
  3. **A side channel, hedged.** "Signature length in the variable-length format has also been examined as a possible side channel, although the significance of that finding is contested." The spec's own hedge; repeat it as one.
  - The trade is priced: "A fixed encoding forecloses all three questions at a cost of at most a few hundred bytes," against a variable format that "would save a few percent on average."
- **The MTU argument — why FN-DSA is first among the three.** "Its raw signatures, at 666 and 1280 bytes, are the only post-quantum signatures defined here that are smaller than a standard 1500-byte Ethernet MTU" (L1557); the same sentence adds that "the smallest ML-DSA signature is 2420 bytes." And: "This matters for protocols that aim to carry a signed message in a single datagram." (L1557.) This is the surviving, citable form of the retracted "of particular interest to bandwidth-sensitive protocols such as KERI" — same argument, `[N1.1]` rather than `[N]`, and with the number attached.
- **Diversity of security argument is the reason to keep ML-DSA despite its size.** Its "Module-LWE construction with Fiat-Shamir-with-aborts rests on a different security argument than FN-DSA's NTRU-lattice hash-and-sign construction, so the two do not fail together." (L1557.) A cryptanalytic break of one lattice family is not assumed to take both.
- **SLH-DSA is the conservative floor, priced out of the hot path.** It is "the most conservative of the three, resting only on the security of its underlying hash function" (L1557), "but its signatures range from 7,856 to 29,792 bytes in the parameter sets defined here" (L1557). The spec's own conclusion: "That makes it impractical for high-volume streams and appropriate mainly for long-lived, infrequently exercised keys." (L1557.)

### 13d. No code for "digest of a post-quantum public key" — a deliberate refusal `[N1.1]` (L1559)

The clearest statement in either branch of CESR's separation between what a primitive *is* and what it is *for*, and directly relevant to how an AID over a large PQ key is meant to be built.

- **The rule:** "No code in this specification encodes a digest of a post-quantum public key as a distinct Primitive type." (L1559.) A digest of a public key uses "the ordinary digest codes, such as `E` for Blake3-256" (L1559), and the same sentence continues that "the context in which the Primitive appears determines whether that digest is a SAID, an AID, a hidden pre-rotation commitment" (L1559) — the enumeration ends "or a digest of a public key."
- **Reason one, layering.** "Introducing a code that means 'digest of a public key' would mix the semantics of a Primitive's use with the semantics of its cryptographic algorithm, which this specification otherwise avoids." (L1559.) The derivation code names the algorithm; context names the role. Compare §5's crypto-agility doctrine, which is the same separation seen from the other side.
- **Reason two, and it is the sharper one: such a code would not buy what it appears to buy.** "A compact identifier derived from a large post-quantum public key is already available" (L1559). The identifier it means is one "whose derivation is a digest of an inception event, rather than a digest of a key" (L1559), which the spec says "is exactly as compact, requires no new code, and carries the key itself in an event that is already defined" (L1559). The self-addressing inception AID already solves "compact identifier for a large key"; a digest-of-key code would be a second, worse mechanism for a solved problem.

### 13e. Open items the forward branch flags itself `[N1.1]`

Two `::: issue` blocks at the end of the PQ subsection, L1561–L1567 at `65fd7518b`:

- **`[Codes for SQIsign and other on-ramp signature candidates]`** — <https://github.com/trustoverip/kswg-cesr-specification/issues/170>. SQIsign is an isogeny-based scheme in NIST's additional-signatures on-ramp, with far smaller keys and signatures than any of the three lattice/hash schemes; no code is defined for it.
- **`[Indexed signature codes for post-quantum signature schemes]`** — <https://github.com/trustoverip/kswg-cesr-specification/issues/171>. See §14a — this one has teeth, because it means PQ signatures currently cannot appear in KERI's indexed multisig groups at all.

A third, older `::: issue` block — "[Post-quantum cryptographic operations]", <https://github.com/trustoverip/kswg-cesr-specification/issues/14> — sits in §Large Variable-length Raw-size Tables at **L559–L560 on both branches**, unchanged. It is the pre-existing placeholder; nothing in this pass closed it.

### 13f. Bibliography additions `[N1.1]` (L1595–L1601 at `65fd7518b`)

Four normative entries with no counterpart on `main` (the string "FIPS" does not appear anywhere in `spec/spec-body.md` at `bad6edd84`):

- `FIPS203` (ref 25) — Module-Lattice-Based Key-Encapsulation Mechanism Standard, NIST, August 2024, <https://doi.org/10.6028/NIST.FIPS.203>
- `FIPS204` (ref 26) — Module-Lattice-Based Digital Signature Standard, NIST, August 2024, <https://doi.org/10.6028/NIST.FIPS.204>
- `FIPS205` (ref 27) — Stateless Hash-Based Digital Signature Standard, NIST, August 2024, <https://doi.org/10.6028/NIST.FIPS.205>
- `FIPS206` (ref 28) — FIPS 206: FN-DSA (Falcon), NIST, <https://csrc.nist.gov/presentations/2025/fips-206-fn-dsa-falcon>. Note the citation is to a *presentation*, not a published standard, consistent with L789's statement that FIPS 206 "is in active standardization and had not been published as of this writing."

---

## 14. Key code-table entries (KERI/ACDC genus `-_AAACAA`, v2.00)

- **Genus/version codes `[N]`:** `-_AAABAA` = KERI/ACDC v1.00; `-_AAACAA` = v2.00. (§KERI/ACDC protocol genus version table, L865–L866 at `main` `bad6edd84`, re-verified.) "Hopefully, there will never be a Version 3.00 because 2.00 was designed properly." (L874, re-verified.)
- **Universal count codes (all genera MUST have):** overrideable — `-A`/`--A` generic pipeline, `-B`/`--B` message+attachments, `-C`/`--C` attachments-only. Non-overrideable — `-D` datagram stream segment, `-E` ESSR wrapper signable, `-F` native fixed-field signable, `-G` native field-map signable, `-H` enclosed non-native message, `-I` generic field map mixed types, `-J` generic list mixed types. (L826–854.)
- **KERI/ACDC genus-specific count codes** (L909–L946; row inventory *not* re-read this pass, but the region was spot-checked at `main` `bad6edd84` and `-S#####` still sits at L926): `-K` indexed controller sig group, `-L` indexed witness sig group, `-M` nontransferable receipt couples (pre+sig), `-N` transferable receipt quadruples (pre+snu+dig+sig), `-O` first-seen replay couples (fnu+dt), `-P` pathed material group, `-Q` digest seal singles, `-R` Merkle tree root seal, `-S` issuer/delegator/transaction event seal source couple (snu+dig), `-T` anchoring event seal triple (pre+snu+dig), `-U` last event seal singles (aid+dig), `-V` backer registrar identifier seal couples (brid+dig), `-W` typed digest seal couples (type+dig), `-X` transferable indexed sig group, `-Y` transferable last indexed sig group, `-Z` ESSR/TSP payload, `-a`/`-b`/`-c` blinded state groups.
- **Primitive matter codes (1-char, L951–L985 at `main` `bad6edd84`):** `A` Ed25519 seed, `B` Ed25519 non-transferable prefix pubkey, `C` X25519 enc key, `D` Ed25519 verification key, `E` Blake3-256 digest, `F` Blake2b-256, `G` Blake2s-256, `H` SHA3-256, `I` SHA2-256, `J` secp256k1 seed, `K` Ed448 seed, `L` X448 public encryption key, `O` X25519 private decryption key/seed, `P` X25519 cipher of qb64 seed, `Q` secp256r1 seed. `M/N/R/S/T/U` = various fixed b2 numbers; `V/W` = Label1/Label2; `X/Y/Z` = Tag3/Tag7/Tag11 special values; **`a` blinding factor is the last entry in the table.**
  - ~~`b/c/d/e` = FN-DSA PQ material.~~ **SUPERSEDED 2026-09-15.** Read at both pins: the one-character table ends at `a` on `main` `bad6edd84` (L985, next row is the "Basic Two Character Codes" header) and equally on `v1.1` `65fd7518b` (L985). `b`, `c`, `d` and `e` are **unassigned on both branches**. The assignment existed only in the unreachable `d35125e` (L978–L981), and `v1.1` deliberately withdrew it — the PQ placement rule of §5a now forbids a post-quantum code in the one-character table by MUST NOT. Replacements are `2AAA`/`2AAC`/`2AAD`/`2AAB`; see §13b for the map.
- **2-char (L986–L1005 at `main` `bad6edd84`):** `0A` salt/seed/nonce/sn 128-bit, `0B` Ed25519 signature, `0C` secp256k1 sig, `0D` Blake3-512, `0E` Blake2b-512, `0F` SHA3-512, `0G` SHA2-512, `0H` long 4-byte number, `0I` secp256r1 signature, `0J`–`0O` tags, `0P`–`0S` gram heads. Table ends at `0S` on both branches; no PQ entries.
- **4-char fixed, `1` selector, at `main` `bad6edd84` (L1007–L1011ff):** `1AAA`–`1AAN` are the pre-existing entries (secp256k1 and Ed448 keys/sigs, Tag4, DateTime, X25519 salt cipher, secp256r1 keys, Null, No, Yes, Tag8). `1AAO` and `1AAP` are consumed by the Variable Raw Size Codes group (escape code; empty value). **`1AAQ` onward is unassigned on `main`.** This is why the v1.1 PQ block starts at `1AAQ`.

### 14a. Post-quantum code-table entries `[N1.1]` (v1.1 `65fd7518b`, §Master code table for genus/version `-_AAACAA`)

These rows exist **only on `v1.1`**. The last column is total qb64 length in characters, which is what a chapter should quote when it wants to make the size argument concrete. Table assignment follows raw-size-mod-3 per §5a, which is why a single algorithm's key and signature usually land in different tables.

**Basic Four Character Codes (selector `1`, 0 lead bytes), L1021–L1034:**

| Code | Primitive | qb64 chars |
|---|---|---|
| `1AAQ` | FN-DSA-512 public verification key [FIPS206] | 1200 |
| `1AAR` | FN-DSA-512 signature [FIPS206] | 892 |
| `1AAS` | ML-DSA-87 public verification key [FIPS204] | 3460 |
| `1AAT` | ML-DSA-65 signature [FIPS204] | 4416 |
| `1AAU` | SLH-DSA-SHA2-192s public verification key [FIPS205] | 68 |
| `1AAV` | SLH-DSA-SHAKE-192s public verification key [FIPS205] | 68 |
| `1AAW` | SLH-DSA-SHA2-192s signature [FIPS205] | 21636 |
| `1AAX` | SLH-DSA-SHAKE-192s signature [FIPS205] | 21636 |
| `1AAY` | Seed of SLH-DSA-SHA2-128s private key [FIPS205] | 68 |
| `1AAZ` | Seed of SLH-DSA-SHAKE-128s private key [FIPS205] | 68 |
| `1AAa` | Seed of SLH-DSA-SHA2-192s private key [FIPS205] | 100 |
| `1AAb` | Seed of SLH-DSA-SHAKE-192s private key [FIPS205] | 100 |
| `1AAc` | Seed of SLH-DSA-SHA2-256s private key [FIPS205] | 132 |
| `1AAd` | Seed of SLH-DSA-SHAKE-256s private key [FIPS205] | 132 |

**Basic Four Character Codes with 1 Lead Byte (selector `2`), L1036–L1050:** `2AAA` FN-DSA-1024 pubkey (2396), `2AAB` FN-DSA-1024 signature (1712), `2AAC` seed of FN-DSA-512 (48), `2AAD` seed of FN-DSA-1024 (48), `2AAE` ML-DSA-65 pubkey (2608), `2AAF` ML-DSA-44 signature (3232), `2AAG`/`2AAH`/`2AAI` seeds of ML-DSA-44/65/87 (48 each), `2AAJ`/`2AAK` SLH-DSA-SHA2-128s / SHAKE-128s pubkeys (48), `2AAL`/`2AAM` SLH-DSA-SHA2-128s / SHAKE-128s signatures (10480), `2AAN`/`2AAO` SLH-DSA-SHA2-256s / SHAKE-256s signatures (39728).

**Basic Four Character Codes with 2 Lead Bytes (selector `3`), L1052–L1055:** `3AAA` ML-DSA-44 pubkey (1756), `3AAB` ML-DSA-87 signature (6176), `3AAC` SLH-DSA-SHA2-256s pubkey (92), `3AAD` SLH-DSA-SHAKE-256s pubkey (92). **This is the first population of the `3` table for any algorithm** — it was structurally defined but empty of crypto suites before.

**The indexed code table is untouched, and that is load-bearing.** Read in full at `v1.1` `65fd7518b` L1109–L1131 (§Indexed code table for genus/version `--AAACAA`): the table still contains only `A#`/`B#` Ed25519, `C#`/`D#` secp256k1, `0A##`/`0B##` Ed448, and the big forms `2A####`–`2D####`, `3A######`/`3B######`. **No post-quantum indexed signature code exists.** The consequence is concrete and should not be softened: KERI's indexed signature groups — `-K` controller idx sigs, `-L` witness idx sigs, `-X`/`-Y` transferable indexed sig groups — have no code that can carry an FN-DSA, ML-DSA or SLH-DSA signature, so on the forward branch as pinned, **post-quantum signatures cannot participate in multi-key or multi-witness KERI events at all.** The spec flags this itself as open issue 171 (§13e). The single-key, single-signature path is unaffected.
- **Worked nested-group example (§Examples, L1109–1126):** `-XBf` TransIndexedSigGroups (Bf quadlets) → AID + sn + SAID + `-KBC` ControllerIdxSigs → indexed sigs `A#`. Shows recursive count-code composition.

---

## 15. Anti-patterns / outsider-tells the spec explicitly corrects

- **Don't reach for naive Base64 with `=` padding.** It gives only "one-way composability" — separable but NOT losslessly round-trippable en masse; CESR forbids `=` entirely. (L93, L139, L252.)
- **Don't assume content-addressable IDs can't be self-referential.** SAID's whole point is a bound *and* embedded identifier; the "naive" view (ID must live outside the content) is precisely what SAID's dummy-derivation transcends. (L1190–1196.)
- **Don't use a self-referential identifier that isn't cryptographically bound** (the W3C-VC / plain-`id` failure mode) — "a security vulnerability" allowing content substitution. (L1194.)
- **Don't use lexicographic canonicalization (JCS-style).** KERI/ACDC canonicalization is *insertion order*; lexicographic ordering is called "un-natural" and criticized for forcing artificial field names. (L1250–1256.)
- **Don't nest raw JSON/CBOR/MGPK inside CESR count-code groups.** Interleaving is a *top-level-only* privilege; nested non-native must be wrapped as a CESR primitive in a special count code. (L374–376.)
- **Don't treat "more crypto strength" as better.** Over-provisioning strength "just wastes computation and bandwidth"; 128 bits is the target floor. Weak suites are excluded from compact tables. (L446, L782.)
- **Don't count primitives — count quadlets/triplets.** A recurring correction: count codes measure 24-bit units, never primitive counts, so they're pipeline-able without parsing contents. (L581, L591.)
- **Blockchain/global-ordering NOT required for immutability** — SAID gives tamper-evident content-addressing and immutability with no ledger/consensus (implicit throughout §SAID). CESR is a streaming format, not a chain.

---

## 16. Notable exact short quotes (<=25 words, with citation)

### 16a. `[N]` — all re-verified verbatim at `main` `bad6edd84`, line hints current

- "CESR is a dual text-binary encoding format that has the unique property of text-binary concatenation composability." — §Self-addressing Data (SAD) Path Signatures, L1390.
- "All compliant encoded Primitives MUST be Composable. All compliant encoded Primitives MUST be self-framing." — §Composability, L5.
- "all Primitives MUST be aligned on 24-bit boundaries to satisfy the Composability property." — §Conversions, L198.
- "all CESR primitives MUST employ mid-padding as defined." — §Code characters and lead bytes, L234.
- "The type portion of all compliant prepended Framing Codes MUST be stable in the Text domain." — §Stable Framing Codes, L202.
- "the value portion of any primitive MUST be right aligned." — §Stable value encoding, L216.
- "the count value MUST be invariant in either Domain and MUST be the number of Quadlets in the 'T' domain" — §Count Code tables, L581. (Full sentence continues "and the number of Triplets in the 'B' domain" and runs 31 words; the clause above is 20.)
- "New implementations with the new codes can accept streams from old implementations, but old ones will break if they receive the new ones." — §Protocol genus/version codes, L618.
- "The CESR derivation code enables cryptographic digest algorithm agility in systems that use SAIDs as content addresses." — §Self-addressing identifier (SAID), L1180. (The source renders "agility" as the glossary reference `[[ref: agility]]`.)
- "a SAID will verify if and only if its encompassing serialization has not been mutated, which makes the content immutable." — §Self-addressing identifier (SAID), L1190.
- "A SAID (Self-Addressing Identifier) is a special type of content-addressable identifier based on an encoded cryptographic digest that is self-referential." — §Self-addressing identifier (SAID), L1178.
- "The natural canonical ordering for such mappings is insertion order or sometimes called field creation order." — §Order-Preserving Data Structures, L1244.
- "Non-CESR serializations, namely, JSON, CBOR, and MGPK when interleaved in a CESR Stream MUST have a Version String as their first field" — §Version String field, L1125.
- "to clarify, the first character of any Primitive MUST be either a selector or a 1-character code type." — §Code table selectors, L484. (Sentence begins "To clarify".)
- "A minor change occurs when a code is added to a table; this only breaks backward compatibility when a new sender sends to an old receiver" is 26 words, one over — quote instead "A minor change occurs when a code is added to a table" — §Protocol genus/version codes, L622.
- "A Major change occurs when a code's meaning changes. When a Major change occurs, the Major version number MUST be incremented." — §Protocol genus/version codes, L620.
- "the parser MUST only treat the genus/version count code, especially as an override, when it appears as the first count code within the framed material" — §Universal Code table genus/version codes that allow genus/version override, L816.

### 16b. `[N1.1]` — new at `v1.1` `65fd7518b`, absent from `main` at `bad6edd84`

- "Post-quantum codes MUST therefore be placed in the four-character fixed tables given by the `1`, `2`, and `3` selectors" — §Code table entry policy, L785. The sentence continues "and MUST NOT consume entries in the one- or two-character tables"; quote whichever half the argument needs, since the full sentence runs 30 words.
- "Which of the three four-character fixed tables a given Primitive occupies is not a matter of choice." — §Code table entry policy, L787.
- "The one- and two-character code tables are a scarce resource." — §Code table entry policy, L785.
- "Admitting every variant of an algorithm invites the use of variants that have received little implementation scrutiny" — §Code table entry policy, L791. Continues: "which weakens rather than strengthens the security of the ecosystem."
- "ML-KEM is a key-encapsulation mechanism rather than a signature scheme; codes for it are not defined here and are left to a later version." — §Code table entry policy, L789.
- "Hiding pre-rotated keys behind digests, as described above, protects the next key pair but does not protect the currently exposed one." — §Post-Quantum Cryptographic Primitives, L1553.
- "The two mechanisms are complementary, not alternatives; pre-rotation continues to provide defense in depth for whichever signature scheme is in use." — §Post-Quantum Cryptographic Primitives, L1553.
- "Every post-quantum signature code defined in this specification encodes a signature of fixed raw size." — §Post-Quantum Cryptographic Primitives, L1555.
- "Signature length in the variable-length format has also been examined as a possible side channel, although the significance of that finding is contested." — §Post-Quantum Cryptographic Primitives, L1555.
- "the two do not fail together." — §Post-Quantum Cryptographic Primitives, L1557. (Tail of the ML-DSA vs FN-DSA construction-diversity sentence; quote the fuller form where the argument matters.)
- "No code in this specification encodes a digest of a post-quantum public key as a distinct Primitive type." — §Post-Quantum Cryptographic Primitives, L1559.
- "Introducing a code that means \"digest of a public key\" would mix the semantics of a Primitive's use with the semantics of its cryptographic algorithm" — §Post-Quantum Cryptographic Primitives, L1559.
- "Each Stream MUST start (restart) with one of eight cases." — §Stream parsing rules, L427.
- "The 'B' domain's purpose is merely to provide convenient compactness at scale." — §Stable Framing Codes, L202.
- "there is minimally sufficient cryptographic strength and more cryptographic strength just wastes computation and bandwidth." — §Compact fixed-size codes, L446.

---

## Gaps / not covered
- This is the **CESR encoding spec only.** It defines the wire/encoding contract but is largely silent on KERI's higher-level *security posture* narrative (survivability-not-invulnerability, duplicity-evidence, witness/watcher/juror/judge roles, zero-trust/malicious-controller stance, local/observer-dependent validity, EGF/IPEX). Those live in the KERI and ACDC specs, not here. Pre-rotation appears ONLY through the PQ-firewall lens (§13), not as a full key-management doctrine.
- No definitions here of AID, KEL/KERL, TEL, witness/backer, watcher, controller-as-root-of-trust as *concepts* — CESR references them only as code-table entry semantics (receipt couples, seals, indexed sigs).
- Op Code table is explicitly **TBD/reserved** (`_` selector, L628, L948) — a whole virtual-machine/stream-processing capability is gestured at but unspecified.
- Large-variable and many context tables are enumerated by structure but not exhaustively populated. ~~PQ (ML-KEM/ML-DSA/SLH-DSA) codes noted as "being introduced in successive updates" — not all present.~~ **SUPERSEDED 2026-09-15**, same retracted-pin failure as §13b: that quoted phrase is from `d35125e` and is on neither branch. The accurate statement is now branch-dependent — no PQ algorithm codes at all on `main` `bad6edd84`; FN-DSA, ML-DSA and SLH-DSA populated and ML-KEM explicitly deferred on `v1.1` `65fd7518b` (§14a).
- The `::: issue` marker at L559–L560 flags post-quantum operations as an open GitHub issue (#14) — indicates this area is still in flux. Re-verified present and unchanged at **both** pins, including on `v1.1`, where the new PQ codes did *not* close it.
- Minor internal inconsistencies noticed (not doctrinal), both still present at `main` `bad6edd84`: `6A` table text says "Only raw binaries with a pad size of 0 are encoded with this table" while the same paragraph ends "All are raw binary Primitives with a pad size of 2 that each includes 2 lead bytes" (L553); the `-S#####` large count code appears to be missing a leading `-` (L926). Likely typos in the source; not raised upstream by this pass.

## Negative results — things looked for and NOT found, at the named commits

Recorded because a reader is entitled to know the difference between "we did not check" and "we checked and it is not there."

- **No post-quantum code of any kind on the standardizing line.** At `main` `bad6edd84`, exhaustive search of `spec/spec-body.md` for `FN-DSA`, `ML-DSA`, `SLH-DSA`, `ML-KEM`, `FIPS`, `1AAQ`, `1AAR` returns **zero hits** for every term except a single occurrence of "Falcon" at L783, in the older entry-policy paragraph, as "among the leading candidates". The fixed four-character table ends at `1AAN`, with `1AAO`/`1AAP` used by the variable-size group. The one-character table ends at `a`. The two-character table ends at `0S`.
- **No `ML-KEM` code on either branch, and the deferral is explicit rather than accidental.** `v1.1` `65fd7518b` L789: "ML-KEM is a key-encapsulation mechanism rather than a signature scheme; codes for it are not defined here and are left to a later version." So CESR as pinned has **no post-quantum key-encapsulation primitive at all** — every PQ code in §14a is a signature, public verification key, or private-key seed. Any chapter claiming CESR has PQ *encryption* support is wrong at both pins.
- **No post-quantum indexed signature code on either branch.** Verified by reading the full §Indexed code table at `v1.1` `65fd7518b` L1109–L1131 and confirming the same table on `main` `bad6edd84` L1066ff. Consequence in §14a; flagged upstream as issue 171.
- **No `b`, `c`, `d` or `e` entry in the one-character matter code table on either branch.** Both tables end at `a`. See §14.
- **No SQIsign code on either branch**, and no on-ramp signature candidate of any kind; only the open `::: issue` at `v1.1` L1561–L1563 (issue 170).
- **No new section on `main` relative to what this note already covered.** The full heading list at `bad6edd84` was read and matches the note's §1–§15 structure; nothing was added to the standardizing line that this note is silent about. `v1.1`'s only structural addition is `#### Post-Quantum Cryptographic Primitives` (L1551) plus the Annex A entry-policy expansion and the PQ table rows.

## Line-hint offsets — `d35125e`-era hints vs `main` `bad6edd84`

For the sections **not** re-read this pass, use these observed offsets as a starting guess, then confirm by searching the quoted text rather than by trusting the number.

- Everything up to and including §Master code table's one-character rows (roughly L1–L985): **offset 0** at every point checked (L5, L87, L198, L202, L216, L232, L234, L240, L374, L427, L438, L446, L484, L553, L559, L581, L591, L609, L611, L615, L618, L620, L622, L812, L816, L818, L865, L874, L926 all unmoved). The one exception is §Code table entry policy, which moved from L782 to **L783** (+1).
- §Version String field onward: about **−6** (L1131→L1123, L1135→L1125, L1137→L1131, L1164→L1160).
- §SAID and §Order-Preserving: about **−6** (L1184→L1178, L1186→L1180, L1188→L1182, L1250→L1244). The two SAID-discussion hints L1194 and L1196 both now resolve into a single paragraph at **L1190**.
- §SAD Path Signatures onward: about **−6** (L1396→L1390, L1402→L1396, L1406→L1400, L1408→L1404).
- §Post-Quantum Security: **−6** (L1508→L1502, L1510→L1504, L1512→L1506).
- For `v1.1` `65fd7518b`, add roughly **+43** to a `bad6edd84` line number past the Annex A entry-policy expansion (e.g. §Post-Quantum Security L1501→L1544), and about **+2** to **+8** between Annex A and there.

## Open questions and unresolved tensions

1. **Does the `v1.1` post-quantum work reach `main`, and on what timetable?** The branches are divergent (merge base `7a6adca67`), and `main` was merged as recently as 2026-08-28 without any of it. Nothing read this pass states an intent to merge. Until it does, every PQ code in §14a is `[N1.1]` and **must not** be cited as normative. This is the single most likely place for a future refresh to over-claim.
2. **Why is the standardizing line's entry-policy paragraph *older* than reality?** At `bad6edd84` it still says NIST "soon will approve" post-quantum standards that were finalized in August 2024, and names Falcon as a candidate. That is not a stale line number; it is stale content on the branch the community is standardizing. Worth watching whether it is a merge oversight or a deliberate freeze.
3. **The `f`-variant exclusion is an argument, not a measurement.** `v1.1` L791 rejects the SLH-DSA fast-signing variants because signatures are "transmitted and archived far more often than they are generated". That is plausible for KERI's event stream and much less obviously true for a high-frequency signer with constrained CPU. The spec states it as settled; the corpus should repeat it as the spec's reasoning, not as an established fact about all deployments.
4. **The side-channel claim is hedged by the spec itself and must stay hedged.** L1555: the finding's "significance ... is contested". Do not let a chapter promote this to a reason the variable-length format is insecure.
5. **What does an FN-DSA-keyed AID actually look like end to end?** §13d says the answer is an inception-event digest rather than a key digest, which is a design position with real consequences for non-transferable identifiers (a non-transferable prefix *is* the key, so a 1200-character FN-DSA key would be the whole AID). The spec does not work this case. Unresolved; flagged for the KERI-spec and keripy notes rather than settled here.
6. **No implementation evidence was sought this pass.** Whether keripy or signify-ts recognizes any of the §14a codes is unknown and unclaimed. Nothing here is `[K]`.
7. **`d35125e` remains readable in one local clone only.** It is a dangling object in `/home/daniel/code/me/kswg-cesr-specification` and will disappear on any `git gc`. If the record of what it contained matters beyond the supersession notes in §13b and §14, it needs preserving deliberately; this note does not preserve the file, only the claims.
