# Refresh report — 2026-09

Run directory `refresh/state/2026-09`. Phases 2–5 executed by the model; phase 1 (detect) and phase 6 (commit/PR) are the shell script's.

**Status: IN PROGRESS.** Written incrementally. Anything below a heading marked *(pending)* did not happen.

This is the **first run of the procedure**, and it shows. Five sources carried `unknown` pins and two carried pins that are not ancestors of their branch head, so a large part of this month's work is establishing a watermark rather than reacting to a month's movement. Read the per-source notes in §1 before treating any pin as a month-over-month delta.

---

## Phase 2 — triage

Scanned: hot + warm tiers, 12 sources plus two GitHub conversation feeds. Below, every candidate in `delta.md` in exactly one class.

### Doctrinal

| # | What moved | Note | Chapters |
|---|---|---|---|
| D1 | **CESR post-quantum codes moved off the standardizing line.** `main` at `bad6edd84` has *no* FN-DSA codes and no FIPS bibliography; the pin `d35125e` is not reachable from any ref in the repo, so the FN-DSA material the corpus records as `[N]` was never on `main` at a commit we can name. `v1.1` at `65fd7518b` defines ~33 PQ primitives across the four-character `1`/`2`/`3` tables under a new normative placement policy. | raw/02 | 04, 06, 07 |
| D2 | **signify-ts implemented the CESR v1.1 PQ code sizes** (`4ed767b`, 2026-09-05), plus a v1 and v2 stream parser and genus dispatch. An `[N1.1]` construct with a `[K]`. | raw/10 | 03, 04, 06 |
| D3 | **KERI spec `main` repathed the Well-Known OOBI**: `/.well-known/keri/oobi/{aid}` → `/.well-known/oobi/{aid}`, RFC5785 → RFC8615, with new normative text on authentication, scheme and media type. raw/01 records the old path. | raw/01 | 01, 06 |
| D4 | **KERI spec `main` added an OOBA pattern and a bootstrap-configuration section**: the same AID published at two or more independently controlled `/.well-known/oobi/{aid}` namespaces as multi-factor bootstrap, and the `iurls`/`durls`/`wurls` buckets. | raw/01 | 06 |
| D5 | **KERI spec `v1.1` added the `DID` (Delegate-Is-Delegator) config trait** — a Delegatee asserting it shares a Controller with its Delegator, for horizontal scaling of signing infrastructure. | raw/01 | 03, 07 |
| D6 | **ACDC spec `v1.1` added Disclosure Paths (`dp`)** — a ~185-line normative section: DAG-of-ACDCs, path syntax, edge traversal, node/leaf paths, closures, the `dp` field, tuple identification, solicited response, and `dp` in `apply`/`offer`. | raw/03 | 05, 08, 10 |
| D7 | **ACDC spec `v1.1` added a Registry-Dependent Issuance Lifecycle** (~250 lines) and a Graduated Disclosure subsection to the examples. | raw/03 | 05, 10 |
| D8 | **ACDC spec `v1.1` added Field Label Restrictions and Unique Entropy (UE) Fields**, and changed the unary-operator table. | raw/03 | 05, 07 |
| D9 | **keripy implemented `dp`**: `mapping.py` Compactor disclosure-path support, `dp` field-shape and validation tightening, `dp` for bare offer. | raw/09 | 05, 08 |
| D10 | **keripy reworked IPEX**: EXN evidence verification and persistence, durable IPEX stores, proof verification and escrow, single-DAG nesting and origin walk. `ipexing.py` +1118, `exchanging.py` +534, `basing.py` rewritten. | raw/09 | 08 |
| D11 | **keripy changed KRAM's key-state currency rule**: `tsg` currency and partial-multisig key state are decided against the *last establishment event*, not the last event (`kraming.py` +265; PRs #1658, #1662). | raw/15 | 09 |
| D12 | **keria made the same change independently** for `endrole` + `locschemes` `tsg`s (`b57780a`, 2026-09-07), plus ESSR byte-transparency and 401-on-malformed fixes. | raw/10 | 03, 06, 09 |
| D13 | **keripy tightened graph validation**: `verifyGraphSemantics`, edge-group and edge-leaf validation, registry validation in the new `regeventing.py`, anchor validation, KEL anchoring for `ax`. Bears directly on the standing "edge operators are read but unenforced" claim. | raw/09, raw/16 | 05, 08, 10 |
| D14 | **Dossier spec replaced its joint-issuance model**: M/Q/FIN → `MxN`/`RMxN`/`MxQ`/`RMxQ` operators, the `m` threshold field → weighted-unity thresholds, and anchoring is now distinguished from signing throughout, with schema SAIDs recomputed. | raw/04 | 05, 06, 08 |
| D15 | **Discussion #1613 *Authentication Factors in IPEX*** (v1.5, 69 KB, last edited 2026-09-02) — states it supersedes much of #1555 *Multiply Endorsed*. | raw/16 | 08, 09 |
| D16 | **Discussion #1627 *ACDC Presentation Architectures*** (26 KB, 5 comments) — partially tracked already; the list form was captured on 2026-09-02, the argument was not. | raw/16 | 08, 10 |
| D17 | **Papers moved substantially**: `wtbo.md` revised to 1.8 (46 lines), `kspqs.md` to 1.2, `crna` errata, two new papers (*Building Active Discovery*; *Progressive Assurance*, prog-a v0.9), and `ppred.md` **withdrawn from the archive**. `wtbo` is the corpus's second-most-cited paper. | raw/05, raw/06 | 01–07 |

### Corroborative

| # | What moved | Note | Chapters |
|---|---|---|---|
| C1 | keripy-knowledge's four 2026-07-02 commits re-verify the KB "current @ `60ab9e08`", scope it to KERI 2.0.0-dev6 @ `d34a1014`, and split the 1.x KB to a separate tree. Corroborates raw/08's own caveat and dates it. | raw/08 | 03, 04, 07 |
| C2 | keripy's version line moved to **2.1.0.dev1** (`5384edc8d`). raw/08 is scoped to 2.0.0-dev6, so its `[2.0-code]`/`[2.0-wire]` tags now describe a superseded dev line. A scope fact, not a doctrine change. | raw/08 | 03, 04, 07 |

### Tier movement

| # | Movement | Evidence needed |
|---|---|---|
| T1 | `dp` disclosure paths: `[P]` (#1627) → `[N1.1]` (ACDC v1.1 `2362e48a1`) **and** `[K]` (keripy `b8f60166b`) | spec section text + code |
| T2 | CESR PQ primitives: recorded `[N]` → actually `[N1.1]` (CESR v1.1 `65fd7518b`), with a `[K]` in signify-ts `4c0072f62`. A **downgrade** of a marker the corpus already asserts. | spec text at both branch heads + orphan-pin finding |
| T3 | Well-Known OOBI repath and the OOBA/bootstrap sections: new `[N]` | KERI spec `main` `fbdd4a615` |
| T4 | `DID` config trait: new `[N1.1]` | KERI spec `v1.1` `3753f3797` |
| T5 | Edge-operator enforcement: standing `[K]` claim ("read but unused", "DI2I raises `NotImplementedError`") re-checked at `b8f60166b` | code, both ways — a negative result is still a result |
| T6 | Dossier joint-issuance operators: `[N]`, replacing a previously-`[N]` model | Dossier `main` `b9227753c` |

### Re-anchor only

| # | What | Action |
|---|---|---|
| R1 | KERI spec `main`: `hexidecimal` → `hexadecimal` in two seal descriptions; example IPs `8.8.5.x` → RFC5737 `192.0.2.x` throughout the OOBI section. No claim changes; every raw/01 line hint past L449 shifts. | re-anchor |
| R2 | ACDC spec `main`: `f0bd097` and `f0bd097de` are **the same commit**, short vs long. `main` did not move at all this period. | pin normalization only |
| R3 | keri-security-analysis: the repo has exactly one commit, `149fa6c35` (2026-04-23). The content mined on 2026-07-17 *is* that commit. The `unknown` pin can be resolved without re-reading. | pin resolution |

### Noise

- **Spec repo build churn** (all four spec repos): `package-lock.json`, `package.json`, `docs/index.html` and `docs/versions/**` regeneration, `menu-wrapper.sh`/`menu-wrapper.js`, `package-backup.json` removal, `tref` install, `.gitignore`. Roughly 20,000 lines across the four, none of it spec text.
- **keripy 1.2.x maintenance line**: PRs #1647, #1648, #1649 (three reverts), #1650, #1651, #1653, #1655, #1657 (witness-transmission and messenger lifecycle), #1659 (version bump), #1660 (CLI paths), #1675 (version bump), #1677 (Python 3.14 patch bound). Release engineering on the 1.x line; no 2.x doctrine.
- **keripy untracked branches** `v1.2.14`, `v1.2.15`, `revert-1614-fix/witness-transmission-draining-v1.2.14` — the same maintenance line. Not proposed for tracking (see §7).
- **papers tooling**: `scripts/`, `tests/`, `requirements.txt`, SEO and DOI metadata, PDF regeneration, `generate_vendored.py`. The prose changes are D17; this is the machinery around them.
- **keria/signify-ts stale branches** `development` (2024-01-23), `docs` (2023-08-23), `reg-poc-demo` (2023-07-18).
- **smithsamuelm-papers**: the two listed commits are from 2026-03-06 and predate raw/15's 2026-09-01 mining. Nothing has moved since KRAM v0.7.6 was mined.

### Traps checked

Both traps the procedure names were live this month.

- **Quiet thread.** #1613 has one comment in a month and is 69 KB of design at v1.5 — and it declares that it supersedes #1555. Comment count said nothing.
- **Two vocabularies.** Searched `presentation registry`, `issuee usage registry`, `usage registry`, `presentation architecture`, and `dp`/`disclosure path` separately. The `dp` construct reaches the corpus under three names across three tiers: "disclosure paths" in the ACDC v1.1 spec, "paths into the graph" in #1627, and `dp` in keripy. Searching any one of them alone would have found roughly a third of the month's largest story.

### Work list

Mining, one agent per note: **raw/01, 02, 03, 04, 05, 06, 08, 09, 10, 15, 16** (11 notes).
Synthesis, one agent per chapter: **01–10** — every chapter is downstream of something above.

---

## Phase 3 — mining *(in progress)*

Discussion drift check run ahead of mining, so that quotes taken from #1613 and #1627 today rest on verified text: `refresh/snapshot-discussions.py --check` → **6 snapshots, 0 drifted, 0 errors**. The snapshots were refetched by phase 1 this morning, so the cached bodies are current as of 2026-09-15.

### raw/03-acdc-spec.md — mined at `main` `f0bd097de` and `v1.1` `2362e48a1`

~48 new `[N1.1]` claims from the `v1.1` branch and 9 new `[N]` claims from `main`.

- **Disclosure Paths (`dp`) is normative on `v1.1` and absent from `main`.** The section declares itself normative; `dp` is *not* an ACDC field — "It appears in the messages that negotiate a disclosure, not in the ACDCs that are disclosed". A `dp` is a list of three-tuples `(ACDCSchemaSAID, PathPrefix, [paths])`, ordered breadth-first with the origin at the zeroth element, and it **MUST** be carried in an `exn`'s query section `q`, not `a`. Path syntax, edge traversal (`/e`, with the hop spelled as the virtual component `_`), node-vs-leaf forms, and closure semantics are all specified.
- **A fifth unary edge operator, `E1E` (Issuee-to-Issuee).** An identity relation on the two Issuees that constrains neither Issuer, requiring both ends Targeted — motivated by the same-subject/different-issuer case, "a relationship the delegative `I2I` Operator cannot express". `v1.1` only, never a default.
- **The IPEX route table changed on `v1.1`.** `apply` and `offer` no longer carry attribute and aggregate label lists; both are replaced by `dp`. The `main` wording is preserved in the note and marked superseded rather than deleted.
- **New `v1.1` sections: Field Label Restrictions and Unique Entropy (UE) Fields.** `-` MUST NOT appear in a field label and a lone `_` is reserved for the DAG hop. The UE rename is a **rename only** — the two substantive UUID paragraphs are word-for-word identical once the term is swapped, and the note records it as such rather than as a doctrinal change.
- **Correction to triage (D7).** The Registry-Dependent Issuance Lifecycle and Graduated Disclosure sections are **not** `v1.1`-only. Both are in `main` at `f0bd097de` and are substantively identical on `v1.1`. They are new since the note's old `11832a3` pin, which is what made them look like `v1.1` material. They tier **`[N]`**, which makes chapter 10 and chapter 05 stronger than triage predicted, not weaker.

Negative results recorded at the pins, all of which chapter 10 depends on:

- `v1.1` does **not** touch the `rd`-in-attribute-section ambiguity. §Registry SAID Field and the reserved-fields row are byte-identical to `main`, typo included. `raw/16 §8` item 2 stays open, and this is its negative answer for `v1.1`.
- **No Issuee-controlled registry anywhere in `v1.1`**: zero hits for "Issuee-controlled", "Issuee controlled" or "Issuee's registry" at `2362e48a1`. The new lifecycle is Issuer-controlled end to end. `raw/16 §6`'s finding now holds at `v1.1` as well as `main`.
- "presentation registry": **0 occurrences** at either pin. "usage registry": exactly one, the same reserved-fields gloss as before.

Coverage is stated honestly in the note header: sections 1, 3–7, 9–13 and 15–20 **still stand at `11832a3`** and were not re-read. `main` has grown from ~4,715 to 5,258 lines, so their line hints are badly drifted.

### raw/09-keripy-code.md — mined at `main` `b8f60166b`

The largest single movement of the month, and it invalidates a standing doctrinal claim.

- **keripy now recognizes five unary edge operators, not three**, and the "read but unenforced" characterization is no longer accurate. `Verifier.UnaryOps` is `('I2I', 'NI2I', 'DI2I', 'E1E', 'NOT')`. **I2I and E1E are enforced**, NI2I is a no-op binding check, and **DI2I and NOT fail closed** — deliberately, not accidentally: "DI2I and NOT are recognized but unimplemented: they are listed so they fail closed diagnosably instead of being dropped and silently defaulting." The **edge `s` constraint is now enforced** too — "the edge 's' is a schema the far node must *satisfy*".
- **`E1E` is implemented and enforced** in both `verifying.py` and `ipexing.py`: the issuee AID of the near ACDC must equal the issuee AID of the far node.
- **m-ary edge-group operators are implemented** — `EdgeGroupOps = ("AND", "OR")`, with `any()`/`all()` evaluation. A `[P]` → `[K]` movement.
- **`dp` landed for wire shape and syntax only.** It is required on `apply` and `offer` and validated as a triple `[schema SAID, DAG path, ACDC paths]` — but **no verb checks a disclosed DAG against its `dp` plan**; `grant` never reads it. `dp` is negotiated, not enforced. That distinction is the whole tier story and chapter 08 must carry it.
- **IPEX now has two divergent implementations.** The V2 `acdc/ipexing.py` is library-and-tests only — `loadHandlers` has no caller in `src/keri` — while the V1 `vc/protocoling.py` handler is the one keripy's CLI actually wires. The corpus's existing §7 claim about V1 was re-verified true and **rescoped** rather than superseded.
- **Version line moved to 2.1.0-dev1**, which rescopes every `[K]` claim in the corpus; the keripy-knowledge material is tagged 2.0.0-dev6.

Superseded, all dated 2026-09-15: the three-operator list; the operator-inference source (`'i' in creder.attrib` → `creder.iseaid is not None`); and, partly, **"DI2I raises `NotImplementedError`"** — still unimplemented, so the doctrine survives, but the mechanism is now a `ValidationError` and a fail-closed `return False`. Right in substance, wrong in mechanism. The "IPEX rejects what it preserves" claim was qualified rather than cut: it **preserves what it defers on** and **drops what it refuses**.

Negative results at `b8f60166b`, stated as findings:

- **No DAG acyclicity check.** `_walkGraph`'s `seen` set is a termination guard, not a validity check. The corpus's existing claim is **confirmed still true** at the new pin.
- **No post-quantum codes in keripy at all.** A repo-wide search for FN-DSA / ML-DSA / SLH-DSA / Dilithium / Falcon / SPHINCS / Kyber / ML-KEM hits only the `falcon` web framework. signify-ts's 2026-09-05 CESR v1.1 PQ code sizes have **not** landed in the reference implementation. That asymmetry between the two implementations is a finding in its own right.
- **`Compactor.compact(paths=…)` has no caller in `src/`** — only in tests.

Coverage stated in the note: `core/coring.py`, `core/eventing.py`, `core/counting.py` and `vdr/eventing.py` were **not** re-read and still stand at `3a8e01ae`, as do `core/signing.py` and `app/habbing.py` — both of which changed in this window.

**Cross-agent resolution.** `verifying.py:40` asserts "E1E is a keripy extension not yet in the spec's normative operator table". The `raw/03` agent found `E1E` defined on ACDC `v1.1` at `2362e48a1`. Both are right about different lines: `E1E` is `[N1.1]`, absent from `main`, so keripy's comment is accurate about the standardizing line and stale about the forward branch. Recorded rather than left as an open question.

### raw/02-cesr-spec.md — mined at `main` `bad6edd84` and `v1.1` `65fd7518b`

**The post-quantum finding is worse than a stale pin, and it generalizes.** `d35125e` is reachable from **no ref at all** — `branch -a --contains` and `for-each-ref --contains` are both empty, and it is an ancestor of neither branch head. It is one of Daniel's own PR-branch commits ("simplify - only fixed-len sigs, no hash-of-pubkey primitives", 2026-03-18) surviving as a **dangling object in one local clone**; it will vanish on any `git gc`. Every FN-DSA claim in the corpus was mined from it. The note now records the general lesson, which is worth more than the incident: `git rev-parse` resolves dangling objects, so **reachability, not resolvability, is the check that makes a pin citable** — a pin that resolves can still be uncitable, and detect.py's ancestry probe is what surfaced it.

Four claims marked superseded, dated 2026-09-15, none deleted:

- The entry-policy quotes "being introduced in successive updates" and "of particular interest to bandwidth-sensitive protocols such as KERI" — **neither string exists at either pin**. `main` L783 carries *older* text than the corpus records: NIST "soon will approve", Falcon "among the leading candidates".
- The whole FN-DSA code paragraph, and the claim that `b`/`c`/`d`/`e` are FN-DSA material in the one-character table. Both branches' one-character table ends at `a`. Replacement map recorded: `b`→`2AAA`, `e`→`2AAB`, `c`→`2AAC`, `d`→`2AAD`, **with different sizes** (2392→2396, 1708→1712, 44→48). Only `1AAQ` and `1AAR` survive, at identical sizes.

New `[N1.1]` material at `65fd7518b`, roughly 33 PQ primitives plus the policy that governs them:

- **Compact-table scarcity is now a normative allocation rule.** "The one- and two-character code tables are a scarce resource", and PQ codes **MUST** go in the four-character `1`/`2`/`3` tables and **MUST NOT** consume compact entries.
- **Table selection is arithmetic, not design** — "Which of the three four-character fixed tables a given Primitive occupies is not a matter of choice", determined by raw size mod 3. The corollary a chapter should carry: a selector encodes lead-byte alignment, not algorithm semantics.
- **A concession the corpus has never recorded**: hiding pre-rotated keys behind digests "protects the next key pair but does not protect the currently exposed one", and the two mechanisms are "complementary, not alternatives". This is the first place CESR admits pre-rotation is not a complete post-quantum answer. It is `[N1.1]`; the hash-firewall claim itself stays `[N]` and is unmoved.
- Parameter-set admission is deliberately narrow — only the six SLH-DSA `s` variants, because admitting every variant "invites the use of variants that have received little implementation scrutiny".
- ML-DSA and FN-DSA "do not fail together" by construction; SLH-DSA is "the most conservative of the three" at 7,856–29,792-byte signatures; FN-DSA signatures are the only ones under a 1500-byte Ethernet MTU.
- **No code encodes a digest of a post-quantum public key as a distinct primitive type**, deliberately — a compact identifier over a large PQ key is a digest of the *inception event*, not of the key.

Negative results at the named pins:

- **`main` at `bad6edd84` has zero post-quantum codes.** Exhaustive search returns nothing for FN-DSA, ML-DSA, SLH-DSA, ML-KEM, FIPS, `1AAQ` or `1AAR`. "Falcon" appears once, at L783, as a candidate.
- **No ML-KEM code on either branch**, explicitly deferred. CESR as pinned has **no post-quantum key-encapsulation primitive at all** — every PQ code is a signature, verification key, or seed.
- **No post-quantum indexed signature code on either branch.** As pinned, a PQ signature cannot appear in any KERI multisig or witness-receipt group.
- Spec issue #14 on post-quantum operations is **still open on both branches** — the v1.1 work did not close it.

The backward-compatibility asymmetry at L618 that `keri-doctrine.md` claim 13 rests on was re-verified **verbatim and unmoved** at `main`. Most other load-bearing hints shifted by −6 to −8 lines and are re-anchored in the note.

### raw/01-keri-spec.md — mined at `main` `fbdd4a615` and `v1.1` `3753f3797`

**Two triage calls were wrong, and the note records the corrections rather than the guesses.**

- **The OOBI material is on *both* branches**, verbatim. The repath, the OOBA pattern and the Bootstrap Configuration section are `[N]`, not `[N1.1]`. Calling them "new" invites the wrong marker.
- **The `DID` config trait is not new in `v1.1`.** `main` already carries a one-sentence form — it "enables the Controller to signal to validators that any Delegate (Delegatee) AIDs are to be treated as equivalent to the Delegator". What `v1.1` adds is the elaborated rationale, and *that* is the `[N1.1]` material: the placement rule (`dip` only, MUST NOT appear in a non-delegated `icp`), consent-by-anchoring, non-transitivity ("It says nothing about any Delegatees that the Delegatee may itself delegate"), the referent-ambiguity argument for why it cannot live in a Delegator's inception, and the stated purpose — "horizontal scaling of a Controller's signing infrastructure by making the equivalence of the AIDs that Controller operates verifiable from their KELs".

Superseded, dated 2026-09-15, old text kept:

- **The Well-Known OOBI path.** `raw/01:179` recorded `/.well-known/keri/oobi/<AID>` under RFC5785. The `keri/` segment is gone, the path is `/.well-known/oobi/{aid}`, the reference is RFC8615 (new bibliography entry 42, "Obsoletes RFC5785"; the RFC5785 entry was kept), `may` became `MAY`, and four new rules attach — the AID "MAY identify any KERI role", the request "is unauthenticated and the response is untrusted at the transport layer" so material "MUST be verified in-band before use", hosts "SHOULD make responses reachable over both `http` and `https`", and media type follows the CESR-compatible serialization. **The trust model did not change; only the plumbing.**
- **"Ean's icp config is `["DID"]`"** — true on `main`, **false on `v1.1`**, where it is `[]`. Both readings kept side by side and labelled by branch.

New `[N]` material the corpus had nowhere: the OOBA pattern (the same AID published at two or more independently controlled `/.well-known/oobi/{aid}` namespaces, each delivered over an independently compromisable channel, accepted only when "a configured threshold of namespaces returns a consistent OOBI for the same AID") with its own careful limit — it "does not change the trust model of an OOBI" and governs "only whether the recipient is willing to bootstrap"; and the `iurls`/`durls`/`wurls` buckets, hedged in the spec itself as "a deployment convention" that "SHOULD NOT be treated as distinct wire forms".

Negative results at the pins:

- **`v1.1` does not carry the `hexidecimal` → `hexadecimal` fix.** The typo is *back* on the forward branch at L452 and L467, and the divergence is bidirectional — a naive forward-merge of `v1.1` reintroduces it.
- **`main` carries none of the elaborated `DID` rationale** — one sentence and one table clause. It cannot be cited `[N]`.
- **`EGF` / "ecosystem governance": zero occurrences** in `spec-body.md` at `fbdd4a615`. Still a gap.
- No new message type, reserved field label or config trait on either branch since `4df80aa`. The `x` and `bi` fields that appeared in the crossdiff are **pre-existing**; only their example values changed.

The note carries a verified file-wide line mapping rather than guessed per-hint offsets: `4df80aa` → `fbdd4a615` is identical for every line ≤ 2837, `+2` for 2838–2846 and `+12` for ≥ 2847; `fbdd4a615` → `3753f3797` is identical ≤ 474 and `−1` above. Roughly 22 load-bearing hints were individually re-confirmed; `termdefs.md` and `terms-definitions/*` citations were **not** re-verified and the note says so.

### raw/15-kram.md — mined at keripy `b8f60166b`, KRAM whitepaper `6ed1ceff4`, KERIA `7e685edaa`

**The key-state currency rule changed, and it is the month's most consequential doctrinal movement.** KRAM used to decide whether an attached `tsg` was current by comparing it against the sender's **latest KEL event of any kind**; at `b8f60166b` it compares against the sender's **last establishment event**, at all ten sites. The module now states the reason in one sentence: "Signing keys change only at establishment events, so the key state ref names the last establishment event rather than the last event of any kind."

The old rule's failure mode is worth recording because it explains why this was found: under it, **any AID that had anchored anything** — a registry inception, an issuance, a revocation, so every credential issuer — had every correctly formed signature refused, and a multisig sender could never reach threshold. Two tests now pin the new behavior.

**Partials are no longer held to prune time.** The note relayed the whitepaper's policy — "the partially signed database entries will remain until the prune window closes" — as implemented, and it *was* true at `fe161709`. At `b8f60166b` four earlier clearing sites exist. The whitepaper and the code now **disagree**, and the note records both with both pins rather than reconciling them: the whitepaper deliberately keeps partials past threshold so a receiver can learn the *full* endorser set ("It is desirable to know all who signed, not just the first who meet the threshold"), while keripy deletes them at handoff on replay-safety grounds. Observable difference: a late co-signer's endorsement of an already-accepted multisig message is silently discarded.

Both of the corpus's load-bearing negatives were re-checked and **both hold, one of them more strongly**:

- **KRAM is absent from any specification.** At KERI spec `main` `fbdd4a615`, a case-insensitive search for `kram` returns **zero hits under `spec/`**. The named residual in `keri-doctrine.md` is intact — and the gap *widened*, since `kraming.py` gained 95 net lines and a new doctrinal rule this month that no specification states.
- **KERIA enforces no request freshness.** The auth path was refactored into `SignedHeaderAuthenticator` and a new `ESSRAuthenticator`, and **both** bind a timestamp without checking it against a clock. The negative now holds across two authenticator classes rather than one.

Window classes are unchanged and still unguided: `kraming.py` ships **no default window values at all**, and validation enforces only ordering and non-negativity — no ceiling, no non-trivial floor, no warning at any magnitude. Both gap attacks in `bible/09 §4` are unaffected. The class-default-off vs runtime-on distinction in `§7` survives verbatim.

Also found: a code comment in `kraming.py` justifies a policy by citing **PR #1788, which does not exist** — the repository is in the 1600s and the API returns 404. The policy is implemented; its provenance is unresolvable.

**Coverage gap to fix next run.** The agent reported the ACDC and CESR spec repos as "not cloned under `~/code/wot/`" and therefore left one cross-check unpinned. They *are* cloned, under `~/code/me/`. The negative was correctly marked unverified rather than carried forward silently, which is the right failure, but the brief should carry the paths next time.

### raw/16-presentation-registries.md — mined at keripy `b8f60166b`, ACDC `f0bd097de`/`2362e48a1`, discussions fetched 2026-09-15

**The note's "one notable silence" is struck.** §0 recorded that #1627 does not mention presentation or usage registries at all, a silence the note had resolved only by a first-hand call report. #1627 **does** now mention them — in a SmithSamuelM comment of 2026-09-02: "This anchor in the KEL only applies when their is not a presentation registry being used by DAG ACDCs". The note replaces the claim with a narrower true one: the **body** still has zero occurrences through its 2026-09-11 edit; every mention is in the comment stream. The call report is retained but **downgraded from sole evidence to corroboration**, which is the right direction for a provenance class the standards call weak.

**A quote-integrity defect from a previous pass was caught and corrected.** §3 rendered #1618's three authentication factors as a single quotation with "1.", "2.", "3." inserted; the source list is unnumbered. The numbering was the note's own, presented as the author's words. Fixed, with the correction recorded inline rather than silently repaired.

Implementation status at `b8f60166b` — all three of §7's negatives re-checked, and **one has changed**:

- **Presentation-registry anchoring is still not implemented.** Every `rd` read in `src/keri` is top-level, across six enumerated sites; **no read of `rd` from an `a` section exists anywhere**. `iseaid` (the Issuee `i` in `a`) *is* now read, but only for I2I/DI2I edge semantics — so keripy understands both halves of the three-part signal and **combines them nowhere**. No code compares a registry's state to a `grant` SAID.
- **The third negative hardened into its opposite.** "Nothing distinguishes an Issuee-controlled registry from an Issuer-controlled one" was true *by indifference* at `4df8e4a8`. At `b8f60166b`, `vetBindings` gained an `issuer` parameter and now **requires** the ACDC's `i` to equal the registry incepter's — "the ACDC's own issuer must match the issuer that incepted the presented registry". A presentation registry violates that by construction. Recorded as a hardening with the old statement preserved.
- **KRAM's silence on registries is conformance, not a gap** — #1613 states that "KRAM does not recognize or process a presentation registry-based authentication factor for the grant message".

Tier movement: **`ax` KEL anchoring moves leg 3 of #1618's three-factor framing `[P]` → `[K]`; leg 2, the presentation registry, does not move.** That distinction is the load-bearing one and §3 now states it explicitly. PR #1674's body says so in as many words — "This PR does not implement presentation-registry anchoring or observer-based TEL retrieval. It will come in a follow up PR" — used for status and intent only, and marked as such. Separately, the `o`/`ax` one-item-list form is now `[K]`, closing a reconciliation dhh1128 raised on #1627 on 2026-09-01.

**A second trusted-third-party relaxation, which the corpus has never recorded.** The existing named residual rests on #1095. #1613 adds a distinct one: the presentation registry is itself "an Issuer-Verifier-protected mechanism to detect compromise of its signing keys" — it requires a non-colluding third-party Issuer *and* an enforcing Verifier. **The mechanism offered as Issuee self-protection is two-party-dependent at both ends.** The residual should name both. A review-panel sync is owed on the residual; doctrine claim 14's verdict itself does not move, though its basis does — "unimplemented" now sits next to a written, dated statement of intent, so a reader inferring *abandoned* from *unimplemented* is demonstrably wrong.

Three new open questions were added rather than smoothed: #1555 *Multiply Endorsed* is load-bearing in both #1613 and #1627 but absent from the manifest; two incompatible bespoke-origin ACDCs share a name (#1613 requires a blinded registry, #1627 requires none); and the eight-way `vet` refusal split is unaudited.

### raw/04-dossier-spec.md — mined at `main` `b9227753c`

**Triage item D14 was wrong, and the way it was wrong is the finding.** `3900e62` *is* reachable — but only from `refs/heads/schema-base-dossier`, a feature branch. It is not an ancestor of `main`. So the note never described the old M/Q/FIN model; it already described `MxN`/`RMxN`/`MxQ`/`RMxQ` and weighted-unity thresholds, because the feature branch already contained them. What carried M/Q/FIN was **`main` itself**, until 2026-06-09.

**The defect was therefore a tier overclaim, not staleness**: joint-issuance material marked `[N]` was only ever supported by a feature-branch commit. It has since resolved in the note's favour — that content is genuinely `[N]` at `b9227753c` — but the corpus was right by luck for three months. `keri-doctrine.md:19` lists "Dossier spec `3900e62`" among its durability pins and carries the same defect.

**This is the second pin-reachability failure this month, in a different shape from the CESR one.** CESR's `d35125e` was reachable from *nothing*; Dossier's `3900e62` is reachable from *the wrong branch*. The generalized rule the corpus now needs is stronger than "check reachability": **verify reachability from the declared branch**, not merely that the hash resolves or that some ref contains it.

**A structural defect that fails standards §1 outright.** `.ref/` is the last line of `.gitignore` and **has never been tracked** — `git ls-tree -r b9227753c -- .ref` is empty. Note sections 9, 10, 13, 14 and part of 7 rest entirely on `.ref/keri-primer.md`, `issuance-ref.md` and `operators-ref.md`, which are **unpinnable to any commit**. Each section is now flagged in place rather than quietly cited. `refresh/sources.yaml:99` also watches `.ref`, where it can never fire.

Superseded, dated 2026-09-15:

- **Both schema SAIDs changed** — base dossier `ECpZgR2Y…` → `EKuLzS_o…`, endorsement `EAfn0gRM…` → `ECRjgun8…`. These are **wire-format changes, not editorial ones**: any schema whose `allOf` `$ref` names an old SAID no longer resolves.
- **What the issuer's signature attests.** A reader of the old bible would say the issuer signs the dossier and the signature attests composition. They must now say: **nothing signs the dossier**; the issuer anchors its SAID, and the anchor attests composition. "A dossier is not a signed document… The signature exists on the anchoring key event, not on the dossier."
- **The threshold field is gone.** There is no threshold field; the threshold is the constant 1 and everything lives in per-slot weights — "so that any *m* of them sum to unity while any *m*−1 fall short". The intermediate unified `m` field survived two commits on one day and is **not citable**; only the endpoint is.
- Verification step 4 now reverses the old note: verify against key state **at the anchoring event's log position**, explicitly *not* at `referenceTime`.

Negative results: `7aeadc2` ("first try amendments", henkvancann) contains **zero prose changes** — six deleted rendering directives — and a later commit reverted essentially all of its head-file substance; what survives is the Contributors credit. `c2d261c` pruned a term the note never cited. `9d8f9a0` consolidated three schemas the note already treated as one.

Every `§heading` in the note was re-anchored. Worth carrying forward: **the title-case normalization is incomplete** — `#### Slot dispositions` is still sentence case — so next month's pass must not assume it.

**This bears on doctrine claim 8 and the "signed envelope" shibboleth row, and a review-panel sync is owed.** A standardizing specification sweeping *itself* for the signing/anchoring conflation is a different kind of evidence than an assertion, and the Dossier text is the better citation to hand an outsider because it states the negative flatly and justifies it by key rotation rather than ACDC internals. Two refinements the row does not currently carry, both usable against an over-absolute reading: the partition is drawn on **lifespan, not artifact kind** — key events and sub-minute tokens *are* signed, and the spec says so — and an attached signature on a dossier is **explicitly permitted** in the ephemeral case, guarded by "A verifier MUST NOT treat an attached signature as equivalent to an anchor when evaluating a dossier as of any referenceTime other than the present". "ACDCs are never signed" overstates it; the accurate form is that nothing expected to outlive a key rotation is authenticated by an attached signature.

### raw/10-keria-signify.md — mined at KERIA `7e685edaa` and signify-ts `ffba8406e` (NOT the manifest pin)

**Triage item D2 does not survive checking, and the correction matters more than the original claim.** Two facts, both verified at source:

1. **The signify-ts pin names a dead branch.** `4c0072f62` is genuinely the head of `development` — but that branch has not moved since **2024-04-12**. The live branch is `main`, at `ffba8406e` (2026-09-10). Mining "at the pin" would have anchored every claim to an April-2024 tree. The agent mined against `ffba8406e` and labelled each claim with the commit it came from.
2. **The post-quantum and CESR-parser work is not upstream signify-ts.** All seven commits are authored by Daniel, and `git branch -a --contains 4ed767b` returns **only** `feat/cesr-pq-codes` and `origin/feat/cesr-pq-codes`, where `origin` is `dhh1128/signify-ts`. They are contained in no `upstream/*` branch, and `upstream/main` at `ffba8406e` has **zero** post-quantum codes.

So the proposed finding — that the reference implementation and the TypeScript client disagree about the post-quantum code table — **is false**. Combined with the other two agents' results (CESR `main` has no PQ codes; keripy has none), the correct statement is: **no shipped implementation carries the CESR 1.1 post-quantum code table.** They agree, in that none of them have it. **This does not move `keri-doctrine.md` claim 9**, which is what the original framing would have implied. The agent coined a provisional `[K-fork]` marker for fork-branch material and flagged it as needing a corpus-wide tier decision rather than asserting one.

**This is the third pin failure of the month, and the three together are a pattern**: CESR's pin was reachable from nothing, Dossier's from the wrong branch, signify-ts's from a branch abandoned two and a half years ago. Each would have produced confident, wrong `[K]`/`[N]` claims.

The corpus's sharpest negative **holds and is now symmetric**: KERIA does not enforce timestamp freshness at `7e685edaa` — `fromIso8601` does not appear in `authing.py` at all, the only two time calls are outbound stamps, `inputage.expires` and `inputage.nonce` are signed but never checked, and there is **no replay cache**. New this pass: **the client half does not enforce it either** — signify-ts folds `expires` into the signature params and never compares it, and checks the ESSR timestamp is *present*, not fresh. This sharpens the bearer-token shibboleth row rather than overturning it, and the note now states the boundary explicitly: the protection is that a request cannot be replayed against a *different* method and path; the same method and path replay indefinitely.

Other negative results: **KERIA serves no `/.well-known/` route at all** (all 41 `add_route` calls enumerated), so this month's spec repath is moot for KERIA and live only for keripy and witness hosts. **No `wurls`** anywhere. **Neither implementation implements `dp`.**

One quote **cut** under standards §7: the note carried *"This **enpoint** allows all KERI clients…"*, which does not match the source — the README reads `endpoint`. Replaced with the verbatim line. The `SignatureValidationComponent` class the note quoted **no longer exists**; both implementations refactored in lockstep, the behavior survives, and the quote is re-anchored rather than cut.

The cloud-agent shibboleth row **strengthens from README prose to code**: `decrypt` occurs exactly three times in all of `src/keria`, all in `authing.py`, only one a live call, and `keeping.py` has **zero** `decrypt` and zero `.sign(`.

### raw/05-papers-priority.md — mined at papers `181569b64`

**Zero cuts, zero supersessions, no doctrine claim or shibboleth row moves.** Every quote the note takes from `wtbo.md` and `kspqs.md` was located verbatim at `181569b64`; both revisions are purely **additive** to the prose the corpus relies on. That is the useful answer to a month where the corpus's second-most-cited paper was revised — the revision did not disturb anything load-bearing.

**Three fidelity defects from earlier passes were corrected**, and they are the same class of problem as the fabricated numbering found in `raw/16`: a previous pass had **silently fixed two typos inside quotations** (`kspqs` "blockain", "commitment precede exposure") and **spliced a phrase from one section into a quote attributed to another** (`wtbo` §2 text inside a Note [b] citation). A quote that has been tidied is no longer verbatim, and a standards §1 citation that has been tidied is no longer a citation. All three are restored with `[sic]` where the source is wrong, and the spliced attribution is split correctly.

New material, mostly regulatory and mostly a hedge the corpus lacked:

- **ENISA contests the "effective 128 bits" figure** the corpus repeats — "a 256-bit output's quantum security level could arguably drop below 128 bits" — and recommends 384-bit hashes. This lands on doctrine **claim 7**, but as an addition rather than a contradiction: Hardman's answer is an agility argument, not a defence of the number. It needs a hedge in chapters 02/03, not a panel re-run.
- The EU roadmap and ENISA v3 demote classical signatures to *admissible*, "leaving only ML-DSA, XMSS, LMS and SLH-DSA recommended" — explicitly **not a ban**, but "a rationale owed for every new system rather than a wall met on a date".
- **"A trust architecture's real agility is the distance between those two costs"**, sharpened by the observation that the governing annex is an undated URL — "A regulator can now revise its cryptographic requirements by editing a file".
- From the new *Progressive Assurance* paper, the tightest statement of anchored-signature doctrine in the whole set: the credential is "provably bound to the identifier's keystate at a particular sequence number".
- From *Building Active Discovery*, a cost the corpus nowhere concedes: a signed presentation is "a durable correlator", and an "unlinkable presentation that still permits counting is not a solved problem". The paper also **retracts a prior claim of the author's in print**, which is worth having as evidence that the corpus's sources self-correct.

Negative results at `181569b64`:

- **The `ppred` withdrawal is a clean no-op.** A case-insensitive repo-wide search hits only this run's own state directory. No chapter, note, doctrine claim, shibboleth row or baseline entry cites it. Confirmed and recorded so a future run does not re-investigate.
- **`sda.md`'s prose did not change** — the single changed line is a frontmatter `pdf_url`. Both shibboleth rows citing it are unaffected.
- **`active-discovery.md` does not intersect OOBIs at all**: zero matches for `OOBI|OOBA|iurls|durls|wurls` across the *entire* papers corpus. Its "discovery" means finding an unknown person by attributes; the spec's means resolving a known AID to endpoints. They neither agree nor disagree, and the note says explicitly that **synthesis must not manufacture a correspondence** — which is exactly the trap the brief set for it.
- `x509-prob.md`, `was.md` and `keri-primer.md` are **byte-identical between the two pins**, so their `last_mined` must not advance past the commit at which they were actually read.

The note previously carried **no line hints at all**. Verified hints were added at `181569b64` for every claim the doctrine and shibboleth rows lean on.

### raw/08-keripy-kb.md — mined at keripy-knowledge `9489ac9bd`

**Two-step staleness is the headline, and it is now a named property of this source.** The knowledge base's own tip is unchanged since 2026-07-02, so the corpus→KB hop is clean. But the KB→keripy hop is **493 commits** (`60ab9e08`, 2026-07-02 → `b8f60166b`, 2026-09-14) and the version line moved **2.0.0-dev6 → 2.1.0-dev1**. Every `[2.0-code]` and `[2.0-wire]` claim the corpus draws from here describes a **superseded dev line** and must not be cited as current keripy behavior. The `[protocol]`-tagged claims are unaffected, which is exactly why the manifest insists those scope tags survive mining.

Superseded, dated 2026-09-15:

- **Landmine L16** as a description of keripy. The substance survives — DI2I is still unimplemented — but the mechanism is wrong three ways: the operator set is five unary operators, not the boolean `&&`/`||` the KB describes; "read but unused" is wrong, since I2I and E1E are enforced; and "not enforced" is wrong **in the safety-relevant direction**, because DI2I and NOT raise `ValidationError` and fail closed deliberately.
- **L17** partially — NI2I is now handled explicitly; the acyclicity half was not re-verified and stands.
- **L1/L5/L6 were scope-corrected rather than superseded.** The shadow-table discipline stands untouched. What changes is the urgency framing: "the Falcon PR must touch every shadow table" is advice about **work that has not started**, since keripy has no post-quantum codes at all, and the KB's own plan records the underlying design question as unresolved — two conflicting Falcon design documents, with resolving them listed as a prerequisite.

**No quotes were cut.** Every quote the previous pass carried was found verbatim at `9489ac9bd`.

Negative results at `9489ac9bd`, whole-tree searches — this is a dated knowledge base and saying so is the finding:

- **No `dp` or disclosure-path material at all.** Zero matches for `dp`, "disclosure path", "nested path", "SAID path". The entire disclosure treatment is one crosswalk row.
- **No `E1E` and no `DI2I`.** Zero matches. The KB does not know these operators exist.
- **No KRAM material whatsoever** — zero matches, and no invariant on replay protection or query freshness.
- No post-quantum material beyond the Falcon planning documents.

**A dead freshness guard, and it is the same failure class this whole procedure was built against.** The KB's own `freshness.sh` defaults to `/home/daniel/code/keripy`, and its session-selector registry points at `/home/daniel/code/keripy-knowledge` and `/home/daniel/code/keripy-1x-knowledge`. **None of those three paths has existed since the repos moved under `~/code/<org>/`.** That is why the KB could fall 493 commits behind without anything saying so — a dead config looking exactly like a quiet month, which is the incident `refresh/detect.py`'s own docstring cites as its reason for existing. Fixing it is outside this repo.

Two provenance corrections worth carrying: the manifest's `last_mined` date of **2026-06-05 was wrong** — it was taken from a filename, and the file it names was added to the repo on 2026-07-02. And the KB's own banners carry an impossible date, claiming re-verification on 2026-06-05 against a keripy commit dated 2026-07-02; read them all as 2026-07-02. The 65-commit count in them does check out.

**A tier question the note raises and does not settle.** This source is marked `[K]` wholesale, but the KB is a **distillation**. Its `[2.0-code]` items are genuine code observations; its protocol-level material is a summary of the primer, `background.md`, `wtbo` and `x509-prob`. Quoting the KB for those is relaying a summary as the source, which standards §1 forbids in as many words. The note writes in a provisional rule — cite the KB for code observations and its own framings, cite the papers directly for protocol claims — and flags it for a corpus-wide decision.

### raw/06-papers-di-drift.md — mined at papers `181569b64`

**Zero quotes superseded, zero cut.** Eleven of the note's twelve source papers are byte-identical between the two pins; `sda.md` changed only by an added frontmatter line. The note's entire citation base survives.

**But the same quote-integrity class appeared again, and this time it reaches `keri-doctrine.md` itself.** Three quotes were **restored rather than cut** — they existed, but the note had silently fixed a typo, which made them unfindable by search and, more importantly, made them not verbatim: `was.md` "effecitvely", `sign-author.md` "authorishop", `who-sign.md` "authoriship". All three now carry `[sic]`. Four heading citations were corrected, **one of them to a heading that never existed**: the note cited `was.md §Retrograde attack`, and `was.md` has no such heading at either pin — the material is in the unheaded opening.

That last one is not confined to the note. **`keri-doctrine.md`'s load-bearing claim 8 cites `was.md` intro, §Retrograde attack** — the same non-existent heading. And the doctrine's DIDs/SD-JWT shibboleth row renders its quote as "AIDs can be transformed to DIDs, but the opposite is typically impossible", where the source reads "the opposite **transformation** is typically impossible". Both are orchestrator-owned fixes and are recorded in §6 below.

Negative results at `181569b64`:

- **No dangling `ppred` reference** anywhere in `raw/`, `bible/` or `keri-doctrine.md`. The withdrawal breaks nothing — independently confirmed by both papers agents.
- **The crna erratum corrects no published claim.** The commit message describes a retraction, but the retraction lives in `active-discovery.md`, not in `crna.md`. Standards §1 applied exactly as written: the commit message is not the source.
- `cfa-paper.md` and `intent-monograph.md` touch no corpus quote — frontmatter only, and neither is cited anywhere in the bible.

**Two papers by the same author now disagree about a procedure the corpus treats as doctrine.** `oia.md` makes eyeball comparison of an entviz the honest way to clear a flag, with the human's final judgement load-bearing. `amp-diff.md`, revised *in this window*, says casual eyeball comparison "is broken" against an adversary — "Casual comparison is not marginally weak against such an adversary; it is broken" — and that the seeded commit-and-reveal walk is then "a requirement, not an enhancement". `oia.md` has not been revised and neither paper acknowledges the other. This qualifies the corpus's "never automate the verification of the proof" invariant: **the unautomated step it protects is the weak one.**

**A provenance finding that reflects on this repository's own methods.** `m-glance.md` v1.1 described its adversarial reviews as "two independent adversarial expert reviews". v1.2/1.3 **retracts that**: they were "AI models prompted to argue from a named lens, not by human domain experts", and "They are a structured way to attack one's own assumptions, not independent validation". `amp-diff.md` made the parallel move from "internally adversarially reviewed" to "adversarially self-reviewed". Given that this repository runs AI persona panels and that `keri-doctrine.md` exists to configure one, that retraction is worth carrying as doctrine about what a panel result is evidence of.

Six comparative claims were flagged as having an **external half that may have drifted and cannot be verified from this repository**. The one that matters most: `sdjwt-acdc.md` still says SD-JWTs "are not standards yet", and if SD-JWT has since become an RFC, several framings argue against a moving target.

One brief-premise correction: `amp-diff.md` and `m-glance.md` are **not** the KERI-vs-DID comparative papers I described them as — they are about perceptual entropy in hash visualization. They belong to this note legitimately, but via a different route, and the agent said so rather than mining to fit the brief.

**Phase 3 complete: 11 of 11 notes mined.**

---

## Phase 4 — synthesis *(in progress)*

### bible/09-kram-and-request-authentication.md

The chapter's new centrepiece is the key-state currency rule, landed in §4 with the superseded rule kept beside it and its failure mode spelled out — every AID that anchors without rotating, which is every credential issuer, had correctly formed signatures refused, and a multisig sender could never reach threshold because the escrow's pinned reference is never refreshed. The agent added the tell in one line: **the prose was right and the code was wrong.**

§5 carries the convergent-correction finding with both quads quoted at both pins, and a detail that strengthens it: **fourteen KERIA sites already did it correctly**, so this was a straggler class rather than a novel design. One observation is offered hedged and explicitly unexplained — the two wrong KERIA handlers serve exactly the two routes keripy denies to BADA.

§7 gained the ten `lastEst` sites enumerated, the foreign-endorser freeze with its generalized principle (an escrow holding signatures across time must record the key state each was made under), and the partials divergence with both sources quoted at both pins, both rationales, the observable consequence, and **the divergence left standing rather than reconciled**. The sub-database count was corrected 14 → 19 and **labelled as an undercount when written** rather than presented as a record of a smaller table — which is the §3 discipline applied to the corpus's own error rather than a source's.

§9's Q3 was rewritten as the symmetric negative, with the boundary stated in both directions. Nothing was cut; two claims were demoted to flagged-unverified rather than carried silently.

**On doctrine claim 8, the agent pushed back on the framing `raw/15` proposed, and I accept its reading.** "Validated against key state as of their KEL anchor" is not *incorrect* — you resolve the key state in force at the anchor's sequence position, which is the state established by the last establishment event at or before it. The defect is that the phrasing lets a reader hear "the anchoring event supplies the key state", and this month produced **empirical proof that competent implementers make exactly that conflation — twice, independently, in six days.** So the fix is a one-clause tightening, not a rewrite. The agent adds a distinction worth keeping: claim 8 and the KRAM rule answer different questions that share vocabulary — claim 8 is about historical key state at a position for evidence at rest; the KRAM rule is about which *current* key state a live message's `tsg` must name. Conflating those two questions is a separate error from conflating anchor with establishment event. And the supporting gloss is `[K]`-only: no specification states it.

### bible/10-presentation-registries.md

The status paragraph was rebuilt around the three-way split the month produced: the **substrate hardened** (IPEX DAG walk, per-node Issuer-registry verification, `ax` KEL anchoring), the **feature is still unbuilt** (no `rd` read from an `a` section, no grant-SAID comparison), and the **intent is now citable** in writing rather than resting on an unquotable call.

§7's third negative is superseded and replaced by its inversion: keripy has moved from *not supporting* presentation registries to **enforcing a rule they break by construction**. §8's silence argument is struck in place, dated, and replaced with the narrower true statement — #1627's *body* still has zero occurrences through its 2026-09-11 edit; every mention is in the comment stream — with the first-hand call report demoted from sole evidence to corroboration and the lesson it taught kept intact.

**One label was cut, and the reasoning is worth recording.** The old §8 described the call report as "`[SAM-DIRECT]` in substance". That token is used elsewhere for KERIcon's edited captions, and standards §2 explicitly separates the unmarked fifth class from those — so borrowing the marker blurred exactly the line the standard draws. The token is gone; the substance it supported is preserved in full.

New `[N]` ground: the Registry-Dependent Issuance Lifecycle, with its boundary statement landed verbatim — "This is confidentiality of registry state, not anonymity of the credential — issuer, registry, and issuance chronology remain linkable, which is the intended, auditable trade-off." New `[N1.1]`: the single-origin-node rule and the bespoke-origin construction, with the observation that `v1.1` specifies the object but **not** the blinded-registry constraint #1613 attaches to it.

A disambiguation was added that prevents a marker error rather than fixing one: the `grant`'s `o` field and the ACDC spec's Edge Operator `o` are different things, "so nobody upgrades the wrong one".

**On doctrine:** claim 14's verdict does not move, but the agent argues its closing clause now *undersells its own case* — "unimplemented" is an understatement when keripy actively enforces a rule a presentation registry violates, and "pre-normative" is now backed by dated negatives on **both** spec lines rather than one. It recommends the no-trusted-third-party residual **append** #1613's relaxation rather than rewrite #1095's. I'm adopting both.

Where the brief and `raw/16` disagreed on how many negative-search terms returned zero, the agent **declined to state either count** and reported only what is independently checkable — no issues at all, exactly two PRs, neither implementing one. That is the right failure.

### bible/03-key-management-and-identifier-lifecycle.md

**The chapter had no marker key at all** — it cited sources inline with no tier markers. One was added, since the chapter now needs `[N1.1]` via `DID`.

The `DID` treatment grew from one sentence to four paragraphs: the `[N]` text from `main` quoted in full and left standing, the `[N1.1]` elaboration from `v1.1`, the **unspecified-consequence boundary** (neither branch says what a validator MUST do with the equivalence, whether it survives the delegatee's rotations, or what revocation does — and no example anywhere shows `DID` in a `dip`), and the Ean tension carried with both readings and **adjudicated neither**.

§4 gained the lifecycle statement of the rule two implementations got wrong: **the key state in force at a position is the one established by the last establishment event at or before it; interleaved interaction events do not move it.** §11 ties that back to the as-of-anchor material with a consequence the chapter did not previously draw — an as-of-anchor check that resolves key state off the latest event **silently degrades into a current-key-state check the moment the issuer emits an `ixn`**.

The Falcon framing was reframed rather than deleted, with the honest summary: *"Nothing is blocked, because nothing has been written."*

**A deliberate deviation from my brief, and the agent was right.** I asked for `[K]` stamps to move wholesale to keripy `b8f60166b`. `raw/09` states plainly that `core/eventing.py`, `core/coring.py`, `vdr/eventing.py`, `app/habbing.py` and `core/signing.py` were **not** re-read there and still stand at `3a8e01ae` — and nearly every code claim in this chapter lives in those files. Blanket-moving them would have over-claimed against standards §6. §0 now carries **both pins** and says which claims earn which. This is the run's clearest case of a subagent refusing an instruction that would have broken the standard it was given.

**Nothing was cut.** One quote was corrected: the chapter carried "commitment precedes exposure" where the source reads "commitment precede exposure" — restored with `[sic]` and a note that the typo is preserved so the quote stays findable. That is a sixth instance of the silently-tidied-quote pattern.

**On doctrine claim 7** the agent recommends: keep the primitive claim, **retarget its citation from `kspqs` to `wtbo` §4** (read alone, `kspqs` states an unconditional guarantee where `wtbo` states a detection-and-rotation race), add the CESR `v1.1` concession as an `[N1.1]` qualifier, and note the ENISA parameter caveat without weakening the claim — ENISA independently supports the primitive. I'm adopting that.

**On the proposed new shibboleth** ("`DID` means the delegator vouches for all its delegatees") the agent supports it with a condition worth honouring: **the refutation is `[N1.1]`-only.** Granularity and non-transitivity exist nowhere on `main`, so this would be a shibboleth whose correction is not yet normative — unusual for that table and to be marked as such rather than smoothed. It proposes pairing it with the `[N]`-safe half: **`DID` has no specified consequence on either branch**, so "vouches" asserts something no specification text supports in either direction.

**One verification I performed myself.** That agent's Bash access to the KERI spec repo was denied mid-run, so its `v1.1` `DID` quotes rested on `raw/01` at one remove. I read both branches directly: `main` `fbdd4a615` L381 and `v1.1` `3753f3797` L381 both match the mined text **verbatim**, at the recorded line hints. That JUDGMENT item is closed.

### bible/04-cesr-and-the-wire.md

The chapter gained a "How to read this chapter" key it did not have, and the post-quantum material was cut and rebuilt. It supplied most of this month's cuts — **four, two of which are quote-integrity defects nobody was looking for**:

1. **All the `d35125e` FN-DSA assignments.** The agent verified the unreachability itself rather than taking it on my word: `cat-file -t` returns `commit`, while `branch -a --contains` and `for-each-ref --contains` both return nothing. This used to be the chapter's **only concrete evidence that crypto agility was being exercised**.
2. **"being introduced in successive updates"** — on neither branch. Supported the "post-quantum is landing incrementally" framing.
3. **"breaks triplet/quadlet alignment and desyncs parsers silently"** — **a composite of two separate knowledge-base sentences quoted as one.** Replaced with the two real sentences.
4. **"Order of ops matters (`*3//4` before `- ls`)", attributed to a keripy code comment** — the string exists nowhere in `coring.py` at `b8f60166b` *or* `3a8e01ae`. It is the knowledge base's own wording. Attribution corrected rather than cut, since the arithmetic itself is verbatim in source.

Rebuilt in their place: the two new `[N1.1]` allocation rules, with the corollary given its own load-bearing turn — **a selector encodes lead-byte alignment, not algorithm semantics**; the retirement map with sizes (`b`→`2AAA` 2392→2396, `e`→`2AAB` 1708→1712, `c`/`d`→`2AAC`/`2AAD` 44→48), and the neat reason `1AAQ`/`1AAR` survive unchanged — 897 and 666 are both ≡ 0 mod 3; and the finding that **no shipped implementation carries the table**. A new ranked risk item was added for the post-quantum indexed-signature gap, which `raw/02` had flagged as an editorial call and I ruled belongs in the ranked list.

**Two agents made opposite calls on the same `[K]` pin question, and both were right.** Chapter 03 declined to move stamps for modules `raw/09` had not re-read, and carried both pins. Chapter 04 **read those modules itself at `b8f60166b`** and re-anchored every hint against source, with the key saying plainly that this is the chapter's own anchoring rather than the note's. The shared principle holds in both: **anchor only what was actually read.** Worth settling as a corpus rule — whether a chapter may anchor ahead of its raw note when it does the reading — and it goes to JUDGMENT NEEDED.

**On doctrine:** claim 13 is **strengthened, not moved** — its anchor quote at L618 is verbatim and unmoved, and the evidence beneath it improved from keripy-only to an independent second implementation framing 33 unfamiliar primitives with no parser change. Claim 9 does not move, with a nuance worth keeping: the post-quantum indexed-signature gap is a genuine interop limit, but a **spec-side** one rather than an instance of implementation divergence — it supports claim 9's premise without being an example of it.

One item needs a deliberate decision rather than a refresh's judgement: **`d35125e` will vanish on the next `git gc`** in the local CESR clone. The chapter records what it contained; nothing preserves the file.

### bible/08-presentation-architectures-and-ipex.md

**The chapter was over-tiering `v1.1`-only material as `[N]`, and the correction is downward.** The whole `dp` apparatus, the one-DAG/one-origin premises and `E1E` were all marked `[N]`; none of them exists on `main` at `f0bd097de`, verified by zero-occurrence searches. All are now `[N1.1]`, and the over-tiering is **recorded as an error rather than silently fixed**. The tier-flip warning now says explicitly that `dp` moved **one tier, not two**.

A new status paragraph states plainly what is actually normative, and it is a much smaller set than the chapter implied: §6–§9 appear in **no specification branch at all**, §2 and §4 are `v1.1`-only, and what is genuinely `[N]` is the bespoke ACDC, four unary operators, the m-ary family, edge `s`, and an attribute-label-list route table.

Two facts are landed as the ones most easily stated wrongly: `dp` is **not an ACDC field**, and it lives in `q`, **not `a`** — with the note that getting the placement backwards collides with `ax` and `o`. The keripy finding replaces the old "keripy implements none of this": `dp` is implemented for **wire shape only** and is **negotiated, not enforced**.

A new §5a documents the two IPEX implementations. The V1 claims were **re-verified true and rescoped** rather than superseded — they describe one of two handlers now, and the V2 module has no caller in `src/keri`.

**One claim cut, and it was demoted rather than deleted**: the `KeyError: 'n'` finding that supported "every edge-group proposal is unbuildable in keripy". `raw/09` did not re-verify it at the new pin, so it now stands explicitly at `42db8991b` rather than being asserted as current — and two negatives it used to support are replaced by verified positives. Three further table cells were softened from asserted negatives to "not checked this pass".

**Two findings that are candidates for Daniel to raise upstream, both recorded and neither acted on:**

- **keripy and `v1.1` are already out of step on `dp`'s own shape.** `v1.1` says a `dp` value is a list of triples; keripy requires a one-element outer list wrapping that list — #1627's nested form — "until Multi DAG". The code presumes a break the branch text has not taken.
- **The unrecognized-operator inconsistency is a conformance question with no text behind it.** `verifying.py` drops the token and applies the default; `ipexing.py` calls it malformed and fails closed. Same edge, two verdicts, neither file aware of the other, and **neither spec branch says anything**. The agent calls this the sharpest finding of its pass.

**On doctrine, the edge-operator shibboleth row survives but its evidence is stale in three places.** The row's outsider tell — "multi-hop authority reasoning" — is still correct, because I2I is still plain AID string equality. What is wrong is the support: DI2I raises `ValidationError`, not `NotImplementedError`, and the distinction *is* the doctrinal point (fail-closed on purpose, not a crash). The same correction is owed in the "the prose says the code does X" row and in the Evidence-standard clause. The agent supplied a one-line accurate replacement, which I will use.

**A manifest inconsistency worth more than it looks.** The chapter cites KERI spec `main` @`be618e7` and Dossier @`6037adf`; `refresh/sources.yaml` records `4df80aa` and `3900e62`. Neither was re-read this pass and both are labelled as such — but **the chapter and the manifest disagree about which commits the corpus has read, and only one of them can be right.**

### bible/05-acdc-and-verifiable-data.md

The chapter had **no marker key and used no tier markers at all**; adding markers required adding the key. `E1E` is landed as `[N1.1]` + `[K]` and never `[N]`, the unary table gained a **Tier column**, and the default-inference gate is presented **side by side** for `main` and `v1.1` with the `main` row preserved rather than overwritten.

§5.1's sharpest claim was superseded with the right-in-substance / wrong-in-mechanism distinction drawn explicitly, plus a warning I think is the most useful sentence in the chapter: **a reader expecting an unhandled `NotImplementedError` will now see a `ValidationError` and wrongly infer that DI2I is implemented.** DAG acyclicity is recorded as a **confirmed** negative at the new pin rather than an unexamined one.

New `[N]` material: the selective-disclosure leak (count and withheld positions "are structural, not blinded"), the Graduated Disclosure worked examples, and the Registry-Dependent Issuance Lifecycle with its own boundary statement. The Dossier corroboration of anchored-not-paired signatures landed with **both guards attached**, so a reviewer cannot over-read it.

**Nothing was cut** — every quote placed was checked at its pinned commit, and the agent spot-verified the keripy and spec quotes against the trees itself rather than relying on the notes.

**On doctrine, one row gets genuinely sharper rather than merely corrected.** The "the prose says the code does X, so it does" row is **strengthened, and becomes bidirectional**: the chapter now supplies a fresher illustration in the opposite direction — keripy's *code comment* says "E1E is a keripy extension not yet in the spec's normative operator table", which is true of `main` and false of `v1.1`. **Trusting a code comment about a spec is the same error as trusting spec prose about code.** That is a real addition to the doctrine, not a pin bump.

The agent also answered a question `raw/04` left open: chapters 05 and 08 never carried the retired Dossier `M`/`RM`/`Q`/`FIN` model — §11 already described the `MxN` family. The prior `[N]` marking was **unearned at the time and is now earned**, so nothing in-chapter is marked superseded, because the chapter's text was never wrong. That is the correct handling and it is worth noting that it required resisting the tidier option.

### bible/06-governance-ecosystems-and-interop.md

The chapter carried **no tier markers at all**; it now carries three, with a key that states something none of the other chapters say outright — the CESR and KERI branches are **divergent in both directions**, so nothing in this chapter promotes on a merge expectation.

§6 was rebuilt around the governance reading rather than the wire mechanics: **allocation is now administered rather than first-come-first-served**, and **placement is removed from negotiation entirely** because table selection is arithmetic. That is a versioning-governance change, and framing it that way is what earns it a place in this chapter rather than chapter 04.

The Dossier double-SAID recompute lands as the concrete migration-cost instance, with the trade stated in four words — **"from ambiguity to coordination"**. The Well-Known OOBI repath lands with its governance reading: **the trust model did not move, only the plumbing.**

**One claim cut**, and the agent was precise about what it cost: the "being introduced in successive updates" sentence "supported the *concreteness* of the chapter's crypto-agility argument — it was the only worked instance of a named algorithm claiming named code slots", and it fed both the §9 migration-cost assessment and the §8 scorecard row. The abstract mechanism it illustrated is untouched and re-verified verbatim.

Two framings worth keeping from this pass. The parity finding is recorded as **"discipline preserved by inaction"** — the implementations agree because none of them has the table, which is not the same as having agreed. And the `kspqs` "couple of hours" migration figure was **demoted from corroboration to a status-only report**, since it describes a conversation about work that does not exist in keripy at `b8f60166b`.

The dead knowledge-base freshness guard is landed here as an **ecosystem-maturity data point**, which is the right chapter for it.

**On doctrine, claim 13 warrants a refinement rather than a correction.** Its load-bearing quote is `[N]`, unmoved and verbatim, and its caveat that "sizing is a pure function of the code" is now **positively corroborated by an independent implementation** — the first affirmative evidence the corpus has for it. But one clause should be added and marked `[N1.1]`: on `v1.1` a new suite may **not** claim just any unused slot. Claim 9 does not move, and the agent adds an argument I had not considered — the `wurls` finding, if anything, *supports* it, since the spec deliberately keeps the buckets out of wire-form status, so a convention that has not converged is not a wire-format failure.

The agent verified its own quotes against source at the named commits and **listed precisely which it could not** — all keripy-knowledge quotes, the fork-branch observations, and the KERIA route count (it confirmed the negative directly, not the count). That list is what makes the pass auditable.

### bible/02-security-model-and-threat-posture.md

**A light pass that stayed light.** §2, §3, §6, §7, §9, §10, §11 and §13 were changed **not at all** — the assumption catalog A1–A13, the KAWA P1–P8 material, the observer layer, local-versus-global validity and the DG bindings all stand as recorded, because `keri-security-analysis` did not move. The agent said so in its report rather than inventing work, which is the correct outcome for a source with one commit in its entire history.

That pin is now resolved: the repository has **exactly one commit ever**, `149fa6c35` (2026-04-23), so the text read on 2026-07-17 *is* that commit. The chapter states it as "unmoved, verified by history, **not re-read**" — the honest form.

Two real additions. §4 gained the fail-closed design decision and, beside it, **the fail-open/fail-closed seam** — landed in §4 rather than §5 because "hostile input until verified" is the rule both paragraphs are about. §5 gained the post-quantum hedge with the SQAR/hash claim **restated and explicitly not weakened**, ENISA's contest of the number, the author's agility answer identified as an *assessment*, and both counterweights in the same breath.

**Nothing was cut**, and §8's two code claims were **upgraded from knowledge-base relay to the chapter's own anchoring** — the agent read `eventing.py`, `habbing.py`, `agenting.py` and `verifying.py` at `b8f60166b` itself rather than citing a 493-commit-stale distillation for machine behavior. That is the `raw/08` tier question being answered in practice rather than deferred.

§12 gained the adversarial-review provenance finding, with a consequence I had not drawn: the `dg-c0X-claude.md` adjudications the chapter leans on are **model-authored**, so they are a structured self-attack on the thesis rather than a second opinion. The agent hedged this to "their filenames mark them as", flagged the inference as circumstantial, and asked for a ruling rather than asserting it.

### bible/01-foundations-and-worldview.md

Another deliberate light pass: §2, §3 and §5 changed **nothing**. The agent also **declined to introduce tier markers** into a marker-free chapter, on the grounds that doing so would require adding a "How to read this chapter" key, which is structural rather than a light pass. Instead the Sources block states plainly that KERI-spec citations mean the standardizing line. I think that judgement is right.

The real work was §8, the established-versus-contested ledger, which gained three contested-side entries and one hedge on the established side — the post-quantum bullet now says that what is established is the **shape** of the Grover/Shor argument, not the number, "pointing forward rather than carrying the shaky sentence inside the confident one", which is standards §4 executed precisely.

**Three more broken heading citations were found beyond the three I briefed** — `x509-prob.md §Lifespans`, `§Prerotation` and `§Much better alternatives` are truncated prefixes of longer headings. The agent graded them: a truncated heading is **a milder defect than a nonexistent one**, because a reader can still find it, so those three were expanded and recorded once rather than annotated at each site. **Six heading corrections in one chapter**, none from this month's sources.

**Nothing was cut.** Two of the agent's own draft quotes ran over the 25-word ceiling and were trimmed **before** it finished — the standard applied to its own output, not just to inherited text.

It reports a clean "nothing moves" for doctrine claims 1, 2, 3, 6 and the CT, blockchain and federation rows, with the reasoning shown: every one rests on KERI spec text below L2837, where the only edits this month are two same-line typo fixes, or on papers that are byte-identical between the pins. That is a verified negative rather than an absence of checking.

Two items it raises are mine to act on: **the heading corrections may need propagating to other chapters** (it owns only chapter 01 and did not look), and many KERI-spec citations across that chapter are bare `(KERI spec, L88)` with **no `§heading`**, which standards §1 requires. Closing that gap is mechanical but larger than a refresh.

