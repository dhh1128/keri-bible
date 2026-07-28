# CESR Spec — Doctrine Mining Notes

Source: `/home/daniel/code/kswg-cesr-specification/spec/spec-body.md` (ToIP KSWG CESR Specification, ~26k words). CESR = Composable Event Streaming Representation. Read-only pass. Citations are `file §heading` plus line ranges.

---

## 1. What CESR fundamentally IS / IS NOT (worldview & design intent)

- **CESR is a dual text-binary encoding format whose defining, "unique property" is text-binary *concatenation composability*.** (§SAD Path Signatures intro, L1394; §Composability L5.) This is the root claim from which everything else derives.
- **CESR is NOT limited to cryptographic material.** "The CESR protocol, however, is not limited to merely encoding Cryptographic Primitives but any primary data type (numbers, text, datetimes, lists, maps) may be encoded in a composable way." (§Abstract Domain representations, L11.) It is a *general* primary-datatype encoding, not a crypto-only wire format.
- **CESR was developed FOR KERI.** "CESR was developed for the KERI protocol." (§SAID, L1186); "The CESR specification not only provides the definition of the streaming format but also the attachment codes needed for differentiating the types of cryptographic material...used as attachments on all event types for the KERI." (§SAD Path Signatures, L1396.) CESR is the encoding substrate of the KERI/ACDC/TSP stack.
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
- **CRYPTO AGILITY doctrine — how a new algorithm claims an unused slot:** The derivation/type code encodes the crypto suite. "The CESR derivation code enables cryptographic digest algorithm agility in systems that use SAIDs as content addresses. Each serialization may use a different cryptographic digest algorithm as indicated by its derivation code. This provides interoperable future-proofing." (§SAID, L1186.) A new algorithm = a new *entry* (previously-unused code point) in a table; old parsers that don't know the code simply don't recognize that primitive but the *framing math is unchanged*, so the stream doesn't desync for primitives they DO know.
- **Backward-compat semantics of adding codes (§Protocol genus/version codes, L618–622):**
  - "Any addition of a new code to the code table is backward-breaking in at least one direction... New implementations with the new codes can accept streams from old implementations, but old ones will break if they receive the new ones." (L618.)
  - **Major change** = "a code's meaning changes" → increment MAJOR version → breaks BOTH directions. (L620.)
  - **Minor change** = "a code is added to a table" → increment MINOR → only breaks new-sender→old-receiver; new receiver still handles old streams. (L622.) More minor room than major deliberately (4096 minor per major).
- **Entry policy (Annex A, L782):** first-needed-first-entered; compact tables require ≥128-bit crypto strength ("precludes...many weak cryptographic suites"), "only best-of-class cryptographic operations." Post-quantum FN-DSA (Falcon) primitives are being introduced "in successive updates" — chosen for most-compact PQ sigs/keys, "of particular interest to bandwidth-sensitive protocols such as KERI."

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

- **INVARIANT:** interleaved JSON/CBOR/MGPK MUST have a Version String as the first field, label `v` (lowercase). (§Version String field, L1131, L1135.) It's the regex target for serialization type + size.
- **v2 format: `PPPPMmmGggKKKKBBBB.`** — 19 chars, five parts: (L1137)
  - `PPPP` protocol (e.g. `KERI`, `ACDC`)
  - `Mmm` protocol major/minor version (base-64 numeric; `M`=major, `mm`=minor)
  - `Ggg` CESR genus-table version (base-64 numeric)
  - `KKKK` serialization kind: `JSON`|`CBOR`|`MGPK`|`CESR`
  - `BBBB` total serialization length in Base64 (inclusive)
  - `.` terminator (v2). Max size `64**4 = 2**24 = 16,777,216` chars; larger → chain via SAIDs. (L1156.)
- **"base 64 numerical notation" ≠ "string encoded in Base64":** a base-64 *number* where each digit is 0–63 (`A`=0, `_`=63), positionally weighted. (L1152.)
- **CESR-native field maps carry NO embedded version string.** They use `-G##`/`--G#####` count codes for map-ness + size; unique start bits mean no regex version string is needed. A native map has a *protocol version field* (protocol+version, not size/kind). In-memory it may inject a placeholder `v` with kind `CESR` so re-serialization knows to emit native CESR. "there is no normative indication that the in-memory object was deserialized from a CESR native field map." (L1154.)
- **v1 legacy format: `PPPPvvKKKKllllll_`** — 17 chars; `vv` two-char hex major/minor; `llllll` length in lowercase hex; `_` terminator. v2 implementations MUST support v1 to verify 1.XX events. (§Legacy Version 1.XX, L1164–1180.)
- The `.` terminator's purpose: let future versions change the version-string size while preserving regex extractability. (L1158.)

---

## 11. SAID — Self-Addressing Identifier (definition + doctrine)

- **Definition:** "A SAID (Self-Addressing Identifier) is a special type of content-addressable identifier based on an encoded cryptographic digest that is self-referential." (§SAID, L1184.) It is embedded *inside* the very serialization it identifies.
- **Why a special derivation is needed:** a naive content-address is a digest of the finished content, so it "must not be self-referential" — you can't put a digest inside the thing you're digesting without changing the digest. SAID solves this with a dummy-string derivation protocol. (L1190, L1192.)
- **Root-of-trust claim:** "The primary advantage of a content-addressable identifier is that it is cryptographically bound to the content...thus providing a secure root-of-trust for reasoning about that content. Any sufficiently strong cryptographic commitment to a content-addressable identifier is functionally equivalent to a cryptographic commitment to the content itself." (L1188.)
- **Security argument against non-bound self-referential IDs (anti-pattern):** an identifier that is self-referential but NOT cryptographically bound is "a security vulnerability" — "Anyone can place such an identifier inside some other serialization and claim that the other serialization is the correct serialization." SAID removes the two-identifier ambiguity by being both self-referential AND bound. (§SAID discussion, L1194–1196.)
- **Immutability:** "a SAID will verify if and only if its encompassing serialization has not been mutated, which makes the content immutable." Enables tamper-evident reasoning and reference-by-SAID instead of embedding. (L1196.)
- **SAID MUST be a CESR primitive** with a prepended derivation code (crypto agility). (L1186, L1192.)
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
- **KERI/ACDC uses INSERTION ORDER (field-creation order), NOT lexicographic ordering.** "The natural canonical ordering for such mappings is insertion order." Insertion order lets field presence/absence and priority carry meaning; lexicographic ordering "appears un-natural" and forces "oddly-labeled fields...merely to ensure that the lexicographic ordering matches a given logical ordering." (§Order-Preserving Data Structures, L1250–1252.) This is a pointed rejection of JCS-style lexicographic canonicalization.
- Modern languages preserve insertion order natively (Python 3.6+ dict, Ruby 1.9+ Hash, JS ES6 Map / ES11 stringify) → "there is no need for any canonical serialization but natural insertion order." (L1256.)

---

## 12. SAD Path Signatures (transposable nested signatures)

- Extension to CESR for **transposable cryptographic signature attachments on SADs.** A signed SAD embedded in another SAD keeps integrity; the attachment's paths update by changing only the root path. (§SAD Path Signatures, L1394, L1402, L1406.)
- **Nested partial signatures:** sign any subset(s) of a SAD, up to the whole; grouped under one attachment via a new Count Code + a SAD Path. (L1402.)
- **Motivation:** KERI events (`exn`, `rpy`, `exp`) carry embedded SADs; a normally CESR-signed SAD isn't embeddable in JSON/CBOR/MGPK maps, so transposable path-signatures solve it. (§Transposable Signature Attachments, L1406.)
- **SAD Path Language (§L1408–1440):** single reserved char `-` (dash) as path separator (like `/` in URLs), chosen because it's Base64-valid. Root path = `-`. Components are field labels OR integer indices (indices exploit static field ordering → works even when labels aren't Base64-safe). No wildcards. Root context is always a map. Error if a sub-path resolves to non-map/non-array. Chosen over JSONPtr/JSONPath for compactness — "Alternative syntaxes would need to be Base64 encoded...incurring the additional bandwidth cost." (L1504.)
- **CESR encoding:** SAD Paths use small variable-size codes `4A##`/`5A##`/`6A##` (0/1/2 lead bytes), reserved for Base64-only text values; up to 16,380 chars / 12,285 bytes. (L1443.)
- **Worked ACDC example** (Fig 1, L1449–1500) shows paths like `-a-personal` → `4AADA-a-personal`, `-5-3-name` → `6AADAAA-5-3-name`.

---

## 13. Post-Quantum Security (doctrine + pre-rotation link)

- **Definition:** post-quantum / quantum-safe crypto maintains strength against quantum attackers, designed for a future when practical quantum computers exist. (§Post-Quantum Security, L1508.)
- **Hash-based PQ argument (Bernstein):** "quantum computation provides no advantage over non-quantum techniques" for collision resistance of hashes. So hiding material behind a digest gives PQ security. (L1508.)
- **Pre-rotation as PQ firewall:** "Instead of a pre-rotation making a cryptographic pre-commitment to a public key, it makes a pre-commitment to a digest of that public key." A PQ attacker must first invert the digest (non-quantum) before inverting the key (quantum) — so "Pre-quantum cryptographic strength is, therefore, not weakened post-quantum. A surprise quantum capability may no longer be a vulnerability." (L1510–1512.) 256-bit Blake2/Blake3/SHA3 keep 128-bit strength post-quantum. Hiding keys imposes NO extra storage burden (controller must reproduce private keys anyway).
- **FN-DSA (Falcon) codes (L1514):** PQ keys/sigs use fixed-length encodings per FIPS 206. Pubkeys: `1AAQ` (FN-DSA-512, 897B raw/1200 qb64), `b` (FN-DSA-1024, 1793B/2392). Sigs zero-padded to max & fixed-size: `1AAR` (FN-DSA-512, 666B/892), `e` (FN-DSA-1024, 1280B/1708). Seeds: `c`/`d` (both 32B/44). Compact AID from FN-DSA key = apply existing digest code (e.g. `E` Blake3-256) to the pubkey; context determines meaning.

---

## 14. Key code-table entries (KERI/ACDC genus `-_AAACAA`, v2.00)

- **Genus/version codes:** `-_AAABAA` = KERI/ACDC v1.00; `-_AAACAA` = v2.00. (L865–866.) "Hopefully, there will never be a Version 3.00 because 2.00 was designed properly." (L874.)
- **Universal count codes (all genera MUST have):** overrideable — `-A`/`--A` generic pipeline, `-B`/`--B` message+attachments, `-C`/`--C` attachments-only. Non-overrideable — `-D` datagram stream segment, `-E` ESSR wrapper signable, `-F` native fixed-field signable, `-G` native field-map signable, `-H` enclosed non-native message, `-I` generic field map mixed types, `-J` generic list mixed types. (L826–854.)
- **KERI/ACDC genus-specific count codes** (L909–946): `-K` indexed controller sig group, `-L` indexed witness sig group, `-M` nontransferable receipt couples (pre+sig), `-N` transferable receipt quadruples (pre+snu+dig+sig), `-O` first-seen replay couples (fnu+dt), `-P` pathed material group, `-Q` digest seal singles, `-R` Merkle tree root seal, `-S` issuer/delegator/transaction event seal source couple (snu+dig), `-T` anchoring event seal triple (pre+snu+dig), `-U` last event seal singles (aid+dig), `-V` backer registrar identifier seal couples (brid+dig), `-W` typed digest seal couples (type+dig), `-X` transferable indexed sig group, `-Y` transferable last indexed sig group, `-Z` ESSR/TSP payload, `-a`/`-b`/`-c` blinded state groups.
- **Primitive matter codes (1-char, L951–981):** `A` Ed25519 seed, `B` Ed25519 non-transferable prefix pubkey, `C` X25519 enc key, `D` Ed25519 verification key, `E` Blake3-256 digest, `F` Blake2b-256, `G` Blake2s-256, `H` SHA3-256, `I` SHA2-256, `J` secp256k1 seed, `K` Ed448 seed. `M/N/R/S/T/U` = various fixed b2 numbers; `X/Y/Z` = Tag3/Tag7/Tag11 special values; `a` blinding factor; `b/c/d/e` = FN-DSA PQ material.
- **2-char (L983–1001):** `0A` salt/seed/nonce/sn 128-bit, `0B` Ed25519 signature, `0C` secp256k1 sig, `0D` Blake3-512… `0J`–`0S` tags/gram-heads.
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

- "CESR is a dual text-binary encoding format that has the unique property of text-binary concatenation composability." — §SAD Path Signatures, L1396.
- "All compliant encoded Primitives MUST be Composable. All compliant encoded Primitives MUST be self-framing." — §Composability, L5.
- "all Primitives MUST be aligned on 24-bit boundaries to satisfy the Composability property." — §Conversions, L198.
- "all CESR primitives MUST employ mid-padding as defined." — §Code characters and lead bytes, L234.
- "The type portion of all compliant prepended Framing Codes MUST be stable in the Text domain." — §Stable Framing Codes, L202.
- "the value portion of any primitive MUST be right aligned." — §Stable value encoding, L216.
- "the count value MUST be invariant in either Domain and MUST be the number of Quadlets in the 'T' domain and the number of Triplets in the 'B' domain." — §Count Code tables, L581.
- "New implementations with the new codes can accept streams from old implementations, but old ones will break if they receive the new ones." — §Protocol genus/version codes, L618.
- "The CESR derivation code enables cryptographic digest algorithm agility in systems that use SAIDs as content addresses." — §SAID, L1186.
- "a SAID will verify if and only if its encompassing serialization has not been mutated, which makes the content immutable." — §SAID, L1196.
- "The natural canonical ordering for such mappings is insertion order or sometimes called field creation order." — §Order-Preserving Data Structures, L1250.
- "Each Stream MUST start (restart) with one of eight cases." — §Stream parsing rules, L427.
- "The 'B' domain's purpose is merely to provide convenient compactness at scale." — §Stable Framing Codes, L202.
- "there is minimally sufficient cryptographic strength and more cryptographic strength just wastes computation and bandwidth." — §Compact fixed-size codes, L446.

---

## Gaps / not covered
- This is the **CESR encoding spec only.** It defines the wire/encoding contract but is largely silent on KERI's higher-level *security posture* narrative (survivability-not-invulnerability, duplicity-evidence, witness/watcher/juror/judge roles, zero-trust/malicious-controller stance, local/observer-dependent validity, EGF/IPEX). Those live in the KERI and ACDC specs, not here. Pre-rotation appears ONLY through the PQ-firewall lens (§13), not as a full key-management doctrine.
- No definitions here of AID, KEL/KERL, TEL, witness/backer, watcher, controller-as-root-of-trust as *concepts* — CESR references them only as code-table entry semantics (receipt couples, seals, indexed sigs).
- Op Code table is explicitly **TBD/reserved** (`_` selector, L628, L948) — a whole virtual-machine/stream-processing capability is gestured at but unspecified.
- Large-variable and many context tables are enumerated by structure but not exhaustively populated; PQ (ML-KEM/ML-DSA/SLH-DSA) codes noted as "being introduced in successive updates" — not all present.
- The `::: issue` marker at L559 flags post-quantum operations as an open GitHub issue (#14) — indicates this area is still in flux.
- Minor internal inconsistencies noticed (not doctrinal): `6A` table text says "pad size of 0" but header says 2 lead bytes (L553); `-S#####` large code missing a leading `-` (L926) — likely typos in the source.
