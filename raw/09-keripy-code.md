# KERI/ACDC/CESR Doctrine — Ground Truth from the keripy Reference Implementation

Source: keripy, `src/keri` (Python reference implementation), repo `~/code/wot/keripy`, remote `upstream` (WebOfTrust/keripy). Mandate: what the code actually enforces versus what prose claims. Every "code does X" claim carries a quote and a line hint at a named commit. Read-only pass; nothing in keripy was modified.

## Pin and coverage {#pin}

Pinned commit: `94f5423a3` (`main`, 2026-10-30, the merge of keripy PR #1681 from `dhh1128/feat-edge-operators`). Mining date 2026-11-03. Earlier pins whose stamps survive below: `80f77b73b` (2026-10-01, mined 2026-10-03), `b8f60166b` (2026-09-15), `3a8e01ae` (2026-07-17).

### What was read at `94f5423a3` {#read-at-pin}

Read in full: `acdc/chaining.py` (new, 267 lines); `vdr/verifying.py`; `acdc/scheming.py` (rewritten, the whole file is the diff); `acdc/ipexing.py` L1–2305 and L2375–2774, which is every verification path and the `offer`, `agree` and `grant` builders. Not read in `acdc/ipexing.py`: the `apply` builder (L2306–2374) and the `admit`, `spurn` and `loadHandlers` bodies past L2774, except one grep hit at L2823.

Read in the changed regions only: `vdr/eventing.py` (the new edge-walk helpers, L49–181; the two `Reger` call sites rewritten onto `edgesOf`; and, for section 3 and section 10 item 11, the NoBackers check L220–221 and `Tever.update`/`Tever.rotate` L991–1130); `peer/exchanging.py` (L140–219, L372–440, L515–560, L624–634, L748–757); `kering.py`, `core/eventing.py`, `core/counting.py`, `acdc/regeventing.py`, `acdc/registering.py`, `acdc/registraring.py`, `db/basing.py`, `app/habbing.py`, `acdc/__init__.py` and `vdr/__init__.py` (diffs from `80f77b73b`); `core/parsing.py` (the `parseOneBare` docstring L467–520 and the ACDC dispatch L1670–1705).

Grep only, at `94f5423a3`: `DI2I`, `I1I`/`DI1I`, `cycle`/`acyclic`, post-quantum code names, `NonceSeal`, `TransReceiptIdxSigGroups`, `loadHandlers`, `ipexing`, `chaining` and `scheming` across `src/keri`, and `I1I`/`DI1I` across `tests` and `docs`.

Not re-read at `94f5423a3`, so their claims keep older stamps: `core/coring.py`, `core/indexing.py` and `help/helping.py` (their hardening diffs were not examined); `core/serdering.py`; `recording.py`; `app/forwarding.py`; `cli/commands/vc/export.py`; `core/kraming.py` (`raw/15`); the bodies of `acdc/regeventing.py` and `acdc/registraring.py` beyond their diffs (`raw/16`). `vc/protocoling.py`, `core/mapping.py` and `core/structing.py` are unchanged between `80f77b73b` and `94f5423a3` (absent from `git diff --stat`), so section 7, the `Compactor` invariants in section 7c and the `structing.py` claims in section 8b carry forward without a fresh read.

### Which sections carry which stamp {#stamps}

Sections 1–5 rest on `core/coring.py`, `core/eventing.py` and `vdr/eventing.py` as read at `80f77b73b` (passages cited) or `3a8e01ae` (inline hints); only the prior-digest claim in section 2 was re-read at `94f5423a3`. Sections 6 and 6b are at `94f5423a3`. Section 7 is at `b8f60166b` and holds unchanged. Sections 7b and 7c are at `94f5423a3`, except the `Compactor` invariants (`b8f60166b`, file unchanged since). Section 7d is at `80f77b73b` with the passages listed above re-read at `94f5423a3`. Sections 8 and 8b are at `80f77b73b`; the `counting.py` diff since then touches only `Counter` decoding, not the code tables. Sections 10 and 11 are at `94f5423a3`.

### Version and provenance facts that scope every claim {#scope}

`__version__ = '2.1.0-dev1' # also change in setup.py` (`src/keri/__init__.py` L3, unchanged at `94f5423a3`). The corpus's older keripy material was tagged against 2.0.0-dev6; the line is the 2.1 development series. Nothing here is a release.

The edge-reduction work merged in #1681 (`50ecb8767` through `b2fcf937f`, plus `500edb2eb`, `dfe59ba11` and `b0a1471a7`) was authored by Daniel Hardman, the corpus's own author. Its comments cite the ACDC specification by section, and those citations are the implementation's claims about the spec, written by an interested party. They are not independent evidence of what the spec says, and this note has not checked them against `kswg-acdc-specification` at any commit; that belongs to `raw/03`. The IPEX revisions in the same window (`131692820` through `e00d66a48`) are Keanu's.

### A note on quote form {#quote-form}

keripy wraps comments and docstrings at about 80 columns. Where a quote is longer than one source line, the words are verbatim and only the source's own line breaks and comment markers have been removed; the line hint then names the range. No quote joins text across a blank line, a different comment block or an intervening statement. `refresh/freshness.py` cannot see through a removed `#` marker, so it reports such quotes as missing; each multi-line quote below was checked by reading the file at its pin.

---

## 1. What KERI/ACDC/CESR fundamentally is — as embodied in the verifier {#fundamentals}

The bullets in sections 1–3 were written against `3a8e01ae` and their inline line hints are hints as of that commit. At `80f77b73b` each quoted phrase was found verbatim and the surrounding code read to confirm the claim is not reversed. Current hints at `80f77b73b`, old → new:

- `core/coring.py`: `Prefixer` docstring 3807 → 3638; `PreDex` gate `if self.code not in PreDex:` / `InvalidCodeError` 3830 → 3656–3657; derivation codes 244–294 → 235–286 (`Ed25519N` 'B' L236, `Blake3_256` 'E' L239, `ECDSA_256k1N` '1AAA' L278, `Ed448N` '1AAC' L280, `ECDSA_256r1N` '1AAI' L286); `Saider` 3922 → 3744; `Dummy = "#"` 3949 → 3771; dummy fill 4085 → 3899; `sizeify` 4088 → 3902; `ignore` deletion 4091–4093 → 3905–3907; `saidify` 4052–4055 → 3841–3871; `Saider.verify` 4117–4160 → 3930–3972 (version check 3962–3964, prefixed check 3966–3967, fail-closed `except Exception` 3969–3970); digestive-code checks 3980–3994 → 3800–3801 and 3812–3814.
- `core/eventing.py`: `toader` docstring 1945 → 1940; `Kever.incept` 2323 → 2301; nonzero-sn check 2335 → 2312–2313; inception sith 2340 → 2317; non-transferable next/wits/data checks 2352/2362/2383 → 2329–2332/2339–2342/2360–2363; recovery prior fetch 2623–2641 → 2596–2614; prior-digest check 2644–2647 → 2617–2620 (L2619 at `94f5423a3`); "Attempted rotation for nontransferable" 2650–2653 → 2623–2626; rotation sith 2657 → 2630; witness cuts/adds set math 2696–2726 → 2668–2699 (in `deriveBacks`); remote-membered stripping 2780–2791 → 2753–2764; "No verified signatures" 2799–2801 → 2772–2774; prior-nsith check 2853–2863 → 2826–2836; toad and witness escrow 2869–2896 → 2842–2869; `exposeds` 2940–2984 → 2913–2956 (digest recompute 2952–2954); local/remote docstring 3040–3135 → 3007–3104; witness-pool-as-second-factor 3051–3057 → 3020–3026; delegator third factor 3059–3068 → 3028–3037; delegator never-do rule 3087–3089 → 3056–3058; witness-pool-change attacker 3099–3104 → 3068–3073; validator rule 3128–3135 → 3097–3104; superseding 3137–3207 → 3108–3208.
- `vdr/eventing.py`: NoBackers check 89–90 → 86–87 at `80f77b73b`, and L220–221 at `94f5423a3`.

Two qualifications. `Kever.incept` takes keys, thresholds and next digests from serder properties rather than raw `ked` lookups — `self.verfers = serder.verfers` (L2315 @`80f77b73b`), `self.ndigers = serder.ndigers` (L2333) — which does not change the claim. And out-of-bounds toad at inception and rotation raises `ValueError`, not `ValidationError` (`raise ValueError(f"Invalid toad = {toader.num} for backers "`, L2351 and L2643 @`80f77b73b`); the in-validation toad bounds check in `valSigsWigsDel` raises `ValidationError` (L2852–2853) and is skipped when the Kever is locally owned, membered or witnessed (L2849–2850).

### AID = self-certifying autonomic identifier, root of trust is the key state itself {#aid}

- `Prefixer` is "Matter subclass for autonomic identifier AID prefix" (`core/coring.py:3807-3809`). An AID prefix is a fully qualified cryptographic primitive (CESR `Matter`): either a basic derivation (public key embedded, non-transferable) or a self-addressing derivation (digest of the inception event). There is no external authority, registry or CA; the identifier is its own cryptographic material.
- Derivation codes (`core/coring.py:244-294`): `B` = "Ed25519 verification key non-transferable, basic derivation"; `E` = "Blake3 256 bit digest self-addressing derivation". `1AAA`/`1AAC`/`1AAI` = non-transferable ECDSA/Ed448/secp256r1. The leading selector character tells the verifier the crypto suite, so crypto agility is structural, not negotiated.
- `PreDex` gate: `Prefixer.__init__` raises `InvalidCodeError` if the code is not in `PreDex` (`coring.py:3830-3831`). Only prefixive codes may be AIDs.

### SAID = Self-Addressing IDentifier: content-hash self-reference, computed by dummy fill {#said}

Mechanism (`core/coring.py:4058-4096`, `Saider._derive`):

1. Copy the `sad` dict and fill the id field with dummy characters to the full size of the digest: `sad[label] = clas.Dummy * Matter.Sizes[code].fs` (`coring.py:4085`). `Dummy = "#"` — "dummy spaceholder char for said. Must not be a valid Base64 char" (`coring.py:3949`).
2. If versioned, recompute the version-string size over the dummied serialization (`sizeify`, `coring.py:4088`).
3. Optionally delete `ignore` fields from the digest input (`coring.py:4091-4093`), which supports fields excluded from the SAID.
4. Digest the serialization and inject the result into `sad[label]` (`saidify`, `coring.py:4052-4055`).

- Verification (`Saider.verify`, `coring.py:4117-4160`) re-derives with dummy fill using `self.code` and compares `qb64b`; if `prefixed`, it also checks the label field literally equals `.qb64` (`coring.py:4154`); if `versioned`, it checks the `v` field matches the derived size (`coring.py:4150-4152`). Any exception returns `False` (fail-closed, `coring.py:4157-4158`).
- Doctrine: the SAID is a tamper-evident commitment to exact serialized content at exact size. Change any non-ignored byte and verification fails. No external hash registry is needed.

### KEL = the append-only, self-verifying key-event log {#kel}

- Inception (`icp`/`dip`) establishes state; the AID's authority derives only from its own KEL. `Kever.incept` (`core/eventing.py:2323`) sets `verfers`, `tholder` (signing threshold), `ndigers` (next-key digests) and witnesses from the event body itself.

---

## 2. Security and threat-model positions {#threat-model}

### Local (protected) versus remote (unprotected) {#local-remote}

The richest doctrinal block is the `Kever.valSigsWigsDel` / `validateDelegation` docstrings (`core/eventing.py:3040-3135`):

- Every event is processed as local (protected) or remote (unprotected) (`eventing.py:2015-2016, 3042-3049`). "A local event may assume that the event only came via a protected transmission path... via some protected channel using some form of MFA. A remote event is received in an unprotected manner." (`eventing.py:3043-3047`).
- Purpose: "to allow increased security on local events where a threshold structure is imposed" (`eventing.py:3048-3049`).
- The witness pool is a threshold, second-factor structure (`eventing.py:3051-3057`, unquoted; see open questions). The delegator adds a third factor (`eventing.py:3059-3068`).
- Enforcement of the firewall (`eventing.py:2780-2791`): when the source is remote and the Kever's prefix is a locally membered group, signatures from locally contributed indices are stripped before threshold counting — "So that attacker can't source remotely compromised but locally membered signatures to satisfy threshold." — and a `remoteMemberedSig` cue is emitted.
- Never-do rule: "The delegator MUST NOT accept a delegable event unless it is locally sourced, fully signed by its controller, and fully witnessed by its controller's designated witness pool." (`eventing.py:3087-3089`).
- A validator (not controller, witness or delegator) has no protected relationship, so "The logic should be the same for both local and remote event because the validator is not one of the protected parties" (`eventing.py:3133-3135`). The validator must wait for full signing, full witnessing and an anchored delegation seal (`eventing.py:3128-3132`).

### Survivability: recovery, not prevention {#superseding}

`Kever` superseding docstring (`core/eventing.py:3137-3207`):

- Superseding is defined as accepting, after an event is first seen, "a different event with the same sequence number … that supersedes the pre-existing event" (`eventing.py:3139-3141`), which "enables the recovery of events signed by compromised keys" (`eventing.py:3141-3142`).
- The KEL forks at the superseding event's sn: "All events in the superseded branch of the fork still exist but, by virtue of being superseded, are disputed." (`eventing.py:3143-3145`). Superseded events are not deleted; they "still remain in the KEL and may be viewed in order of their original acceptance" (`eventing.py:3148-3150`). The fork is preserved and visible, so the KEL is duplicity-evident by construction.
- `fn` (first-seen ordinal) is not `sn`: "Each event accepted into a KEL has a unique fn but multiple events due to recovery forks may share the same sn." (`eventing.py:3153-3155`).
- Superseding rules (`eventing.py:3158-3207`): A0, a rotation may supersede an interaction at the same sn; A1, a non-delegated rotation may not supersede another rotation at the same sn; A2, an interaction may never supersede anything. The B rules govern delegated-rotation superseding through the delegator's KEL ordering, climbing recursively (C) to the non-delegated root; if unsatisfied, the superseding rotation is discarded (`eventing.py:3195-3206`).

### Detection, not prevention, for delegation compromise {#delegation-detection}

- "A malicious attacker that compromises the pre-rotated keys of the delegatee may issue a rotation that changes its witness pool in order to bypass the local security logic"; the mitigation is a delegator time window to "give the delegate enough time to detect a comprimised or duplicitious superseding rotation" (`eventing.py:3099-3104, 3225-3238`). The design assumes compromise will happen and optimizes for detectability.

### TOAD = Threshold Of Accountable Duplicity {#toad}

- `toader (Number): instance of TOAD (threshold of accountable duplicity)` (`core/eventing.py:1945`). The witness threshold is named for duplicity accountability, not consensus or finality.

### Pre-rotation, and exactly how it is checked {#pre-rotation}

Inception commits to digests of the next keys (`ndigers`), not the keys; the keys are exposed only at rotation.

- Non-transferable AIDs must have an empty next list: `if not self.prefixer.transferable and ndigs:` → `ValidationError` "Invalid inception next digest list not empty for non-transferable prefix" (`eventing.py:2352-2355`). Non-transferable inception also forbids witnesses (`:2362`) and anchored data (`:2383`).
- Rotation is forbidden with no prior next: `if not self.ndigers: raise ValidationError("Attempted rotation for nontransferable prefix...")` (`eventing.py:2650-2653`).
- The check itself is `Kever.exposeds` (`eventing.py:2940-2984`): for each signature, take the prior next digest at `siger.ondex`, recompute `Diger(ser=siger.verfer.qb64b, code=diger.code).qb64` and require it to equal the committed digest (`eventing.py:2980-2982`). Only matching ondices are returned.
- The threshold applies to the exposed prior next: `if not self.ntholder.satisfy(indices=ondices):` → escrow and `MissingSignatureError` "Failure satisfying prior nsith" (`eventing.py:2853-2863`). A rotation is valid only if the newly exposed keys hash to the committed next digests and satisfy the prior next threshold, so an attacker holding only current signing keys cannot rotate. Digest agility is per digest: "all digests in .digers may use a different algorithm" (`eventing.py:2954-2956`).
- Prior-event chaining: a non-recovery event whose prior digest does not match the accepted state raises `MisdigestError`, a `ValidationError` subclass (`raise MisdigestError("Mismatch event dig = {} with"`, `core/eventing.py` `Kever.rotate`, L2619 @`94f5423a3`; the same check in `Kever.update` at L2515 and, for a recovery event's prior, in `Kever.rotate` at L2609). Its class docstring says it is not permanent on a KEL: "On a KEL this is not permanent, because a superseding recovery rotation" (`kering.py` `MisdigestError`, L822 @`94f5423a3`) "can replace the accepted prior event" (L823), and it is "Raised before signatures are verified, so it says nothing about who produced the event." (L826–827). Recovery events verify against the fetched prior event (`eventing.py:2623-2641` @`3a8e01ae`).

### Fail-closed threshold semantics {#fail-closed-thresholds}

- "must have a least one verified sig" else `ValidationError` "No verified signatures" (`eventing.py:2799-2801`).
- Witness toad bounds are enforced, with the scoping in the qualification under section 1; under-threshold witnessing escrows as `MissingWitnessSignatureError` and cues a receipt query (`eventing.py:2869-2896`).

---

## 3. Invariants and never-do rules (machine-enforced) {#invariants}

- Non-transferable prefix ⇒ empty next-digest list, empty witness list, empty anchored data at inception (`eventing.py:2352, 2362, 2383`).
- Inception sn must be 0: `if self.sner.positive: raise ValidationError(f"Nonzero sn... in inception event")` (`eventing.py:2335-2336`).
- Signing threshold size ≤ number of keys: `if len(self.verfers) < self.tholder.size` → "Invalid sith" (`eventing.py:2340`); rotation likewise (`eventing.py:2657`).
- Witness sets: no duplicates; cuts must be a subset of current witnesses; cuts∩adds and wits∩adds must be empty (`eventing.py:2696-2726`). Ordered-set math preserves witness index stability for indexed receipts (`eventing.py:2661-2665`). Registry backers follow the same rules in `Tever.rotate` (`vdr/eventing.py` L1094–1126 @`94f5423a3`).
- NoBackers registry trait: `if TraitDex.NoBackers in cnfg and len(baks) > 0:` → `raise ValueError("{} backers specified for NB vcp, 0 allowed".format(len(baks)))` (`vdr/eventing.py` `incept`, L220–221 @`94f5423a3`).
- The SAID dummy character must not be valid Base64 (`coring.py:3949`); a `Saider` must carry a digestive code, else `ValueError` (`coring.py:3980-3994`).

---

## 4. Anti-patterns and outsider tells the code contradicts {#anti-patterns}

- Revocation as deletion or blocklist (the X.509 CRL / OCSP mindset) is wrong. The verifier saves a revoked credential: on revoked state it logs and continues rather than raising — "Log this and continue instead of the previous exception so we save a revoked credential." (`vdr/verifying.py` `Verifier.processCredential`, L207 @`94f5423a3`). Revocation is a TEL state transition (`Ilks.rev`/`brv`), not a delete, and state is read from the TEL (`self.tevers[regk].vcState(vcid)`, L193), not from a central list. A revoked far node is a different matter; see section 6.
- "A CA or registry vouches for the identifier" is contradicted: authority is self-certifying through the KEL, and there is no issuer authority external to the AID's own key state.
- "Consensus, global ordering, one true log" is contradicted: recovery forks the KEL and keeps disputed branches (`eventing.py:3143-3149`); ordering is per-AID `sn` plus `fn`, and validity is observer-relative (`eventing.py:3040-3135`). TOAD is accountable duplicity (`eventing.py:1945`), not Byzantine finality.
- "Witness = blockchain validator or consensus node" is contradicted: witnesses are a per-controller threshold second-factor structure (`eventing.py:3051-3057`), and a registry may have zero backers (section 3).
- "Verification is globally objective" is contradicted: the same event yields different acceptance depending on whether the observer is controller, witness, delegator or validator and whether the source is local or remote (`eventing.py:3040-3135, 2780-2791`).
- "Peer disclosure messages get logged like a VC exchange endpoint" is contradicted: IPEX is a strict state machine (section 7, section 7b); out-of-order or duplicate-response messages are rejected, not merged.

---

## 5. Terminology as the code uses it {#terminology}

- AID: autonomic identifier, `Prefixer` (`coring.py:3807`). Transferable (rotatable, digest or transferable key code) versus non-transferable (`B`, `1AAC` and the other non-transferable codes).
- SAID: `Saider` (`coring.py:3922`), a content-addressed self-reference by dummy-fill digest.
- KEL: key event log (`db.kels`, state in `Kever`). KERL: a fully witnessed, receipted KEL (receipt couples and quadruples, `eventing.py:124-273`).
- TEL: transaction event log for a registry, managed by `Tevery`/`Tever`; credential state via `tever.vcState(vcid)`. Events: `vcp` (registry inception), `iss`/`rev` (backerless issue and revoke), `bis`/`brv` (backer issue and revoke). The registry's controlling AID is `self.pre = ked["ii"]` (`vdr/eventing.py` `Tever`, L880 @`94f5423a3`).
- Witness and backer: non-transferable AIDs that receipt events, witnesses for KELs and backers for TEL registries.
- `Siger` carries a dual index, `.index` into current keys and `.ondex` into prior-next digests, which is what makes pre-rotation exposure checkable (`eventing.py:2942-2984`).
- `Tholder`: threshold object; `.satisfy(indices)` decides fractional, weighted and multi-clause thresholds (`eventing.py:2854`).
- exn: peer-to-peer exchange message, handled by `Exchanger` in `peer/exchanging.py`, carrying pathed CESR attachments.
- IPEX: Issuance and Presentation EXchange over exn; two implementations, section 7 and section 7b.
- Edge verdict: the three-valued result an edge or Edge-group evaluates to in both of keripy's ACDC evaluators, `Verdicts = Verdictage(valid='valid', invalid='invalid', unknown='unknown')` (`acdc/chaining.py`, L43 @`94f5423a3`); section 6.
- `Parser.parseOneBare` processes one message "like .parseOne but raises any error to the caller instead of logging it." (`core/parsing.py` `Parser.parseOneBare`, L470–471 @`94f5423a3`), for a caller vetting a stream rather than a service facing the open internet (L473–477).

---

## 6. ACDC edge evaluation at `94f5423a3` — one lattice, two evaluators {#edges}

All quotes in this section are at `94f5423a3`. The two evaluators are `Verifier` in `vdr/verifying.py` (the v1 credential path, which the CLI uses) and `IpexHandler` in `acdc/ipexing.py` (the v2 IPEX grant path, which nothing in `src/keri` calls; section 7b). Both now reduce an Edge Section through `acdc/chaining.py`, and on the three axes where they used to disagree they now agree.

### The shared module, and how far it goes {#chaining}

`acdc/chaining.py` holds the verdict type and the m-ary reductions and nothing else: "So this module holds no storage and no evidence." (L16). The division of labour is stated: "the mapping and the disposition stay with the callers while the algebra lives here." (L20–21). Each evaluator still walks the Edge Section, evaluates unary operators and disposes of the result in its own code. So the shared layer is the algebra only; there is no single edge evaluator that both paths call. Sam's direction that edge logic should become its own layer is recorded, with his words, in raw/21 R-080; this note records only that the code does not yet have one beyond the algebra: the operator tables are a class attribute in one module and module constants in the other, and only the m-ary table is a swappable policy object.

The lattice has three values, with a retryability bit on unknown: "Three values, not four." (L30). `unknown(reason, *, retryable, cause=None)` makes retryability a required keyword "because defaulting it either way silently converts one of those cases into the other." (L107–109).

The reductions are Kleene strong logic. AND: "one invalid member decides the group however many are unknown" (`reduceAnd` docstring, L135–136), and a group's unknown is retryable only if every unknown member is (L138). OR: "One valid member decides the group" (`reduceOr` docstring, L164–165), and its unknown is retryable if any unknown member is (L168–169).

The module states that this is keripy policy, not protocol: "the Kleene reading below is keripy's default rather than protocol." (L26–27), on the ground that ACDC assigns edge-validity logic to the Ecosystem Governance Framework (L24–26). Both callers reach the table through an attribute, `MAryReducers = chaining.MAryReducers` (`vdr/verifying.py` `Verifier`, L105; `acdc/ipexing.py` `IpexHandler`, L501), so a profile can override it. The default table is `MAryReducers = dict(AND=reduceAnd, OR=reduceOr)` (L189).

NAND and NOR are deliberately not registered. The reason given is the specification's two-valued m-ary rows, under which a literal reader "counts a member it does not have as not-valid" (L209–210); keripy refuses them, and "failing closed until then is the conservative side of a disagreement this module cannot settle on its own." (L213–214). AVG and WAVG "return a number over a schema-defined member property rather than a validity" (L216–217). `reduce` raises `ValidationError` for any unregistered token and for an empty group (L260–265). This is keripy's reading of the spec's m-ary table, written by an interested party (see the scope note in the header), and has not been checked against the spec here.

### Where the two evaluators now agree {#agreement}

- Unrecognized unary token: both refuse to read past it, and both treat it as an unknown no arrival can settle, not as malformed. v1: "A token outside this set cannot be evaluated, so an edge carrying one is refused rather than validated under a substituted operator" (`Verifier` class comment, L59–61), raising `UnsupportedOperatorError` before the far-node lookup (`verifyChain`, L827–832), which `evaluateEdge` maps to `chaining.unknown(reason, retryable=False, cause=cause)` (L444). v2: `unrecognized = [cand for cand in ops if cand not in UnaryEdgeOps]` (`_evaluateLeafEdge`, L1480), returned as an unknown with `retryable=False` (L1545–1548). So an unrecognized operator refuses a section that needs the edge, and is outvoted by a satisfied sibling under OR. One residual difference: v2 conjoins that unknown with the far node's own verdict (L1531–1543), v1 does not reach the far node at all. Under AND and OR, the only reducers keripy registers, both readings refuse in the same cases; this is an inference from the lattice, not a test run.
- A list of operators: both resolve latest-wins among the delegative three and compose `E1E` alongside. v1 `op = next((cand for cand in reversed(ops) if cand in self.DelegativeOps), None)` (`verifyChain`, L846); v2 `dop = next((cand for cand in reversed(ops) if cand in DelegativeEdgeOps), None)` (L1565), with `DelegativeEdgeOps = ("I2I", "NI2I", "DI2I")` (L56). `["I2I", "NI2I"]` is NI2I to both.
- Absent or empty `o`: both apply the default unary operator, keyed on the same suppressing set, `('I2I', 'NI2I', 'DI2I', 'E1E')` (`Verifier.DefaultSuppressingOps`, L78; `DefaultSuppressingEdgeOps`, `acdc/ipexing.py` L65). v1: `op = 'I2I' if creder.iseaid is not None else 'NI2I'` (L861). v2: `ops = ops + ["I2I" if fserder.iseaid is not None else "NI2I"]` (L1557), under the comment "a bare edge is not an unconstrained edge." (L1550).
- DI2I and NOT: both recognized, both unimplemented, both an unknown with `retryable=False`. v1 raises `UnsupportedOperatorError` (L867–873); v2 collects them as `unevaluable` (L1572–1578). The class docstring explains why "cannot evaluate" is kept apart from "does not hold": under NAND, NOR or NOT "that collapse inverts into acceptance" (`kering.py` `UnsupportedOperatorError`, L1154–1155).
- `E1E`: both require equal issuees, near and far, resolved through `.iseaid` (v1 L885–889, raising `EdgeRefusalError`; v2 L1584–1590, an invalid verdict). The v1 comment draws the distinction from I2I: the SEDI case "both credentials issued by a third party to the same subject, issuer != issuee -- is valid (and is exactly what I2I rejects)." (L879–880).
- I2I: still single-hop AID string equality on both, near issuer against far issuee. v1 `if op == 'I2I' and issuer != farIssuee:` → `EdgeRefusalError` (L909–912); v2 `elif nserder.israid != fserder.iseaid:` → invalid (L1599–1603). A targeted operator against an untargeted far node is decided against on both (v1 L897–900; v2 L1595–1598).
- A decided edge is not escrowed. `EdgeRefusalError` is for a constraint "decided against evidence already in hand" (`kering.py` `EdgeRefusalError`, L1130–1131), and "A refusal must not escrow: it would promise a retry that cannot succeed." (L1137–1138).
- Edge-groups: both walk nested groups, default an absent group `o` to AND (v1 `DefaultMAryOp = 'AND'`, L110; v2 `groupOp = group.get("o", "AND")`, L1683), refuse a non-string group `o` as malformed (v1 `verifyGroup`, L625–628; v2 L1691–1692), treat NAND, NOR, AVG, WAVG and any unknown string token as a non-retryable unknown (v1 `reduceGroup`, L399–406; v2 L1745–1759), and refuse an authored empty group as malformed (v1 L383–386; v2 L1738–1743).
- Schema pins: an `s` on any enclosing group, the Edge Section included, binds every edge below it, and pins compose as a conjunction. v1: "Conjunction, not override: an inherited pin is a floor" (`evaluateEdge`, L464–465). v2: "A group's own pin is added to those already in force rather than replacing them" (`_evaluateGroupEdge`, L1695–1696). Both modules call the group-level `s` a keripy extension; the v1 comment says ACDC "reserves [d, u, o, w] on a group and defines no `s` there" (L276).
- A compact Edge (a non-reserved label whose value is a SAID string) is an unknown with `retryable=False` on both, because keripy does not store Edge blocks apart from the ACDC that carries them (v1 L309–330; v2 L1704–1714).

### Where they still differ {#divergence}

- A revoked far node. v1 decides against it: `if state.et in (Ilks.rev, Ilks.brv):` → `chaining.invalid(...)` with `RevokedChainError` (`evaluateEdge`, L516–519). v2 does not judge registry state at all: "No registry-state policy lives here." (`IpexHandler` class comment, L484), and the handler "authenticates each registry proof, records the state it carries in `Baser.exrs`, and leaves judging it to an application or EGF evaluator" (L489–491). The records are written only after a grant is accepted (L820–831), keyed by "exchange message SAID and disclosed node SAID" (`db/basing.py` docstring for `.exrs`). So a chain through a revoked credential fails credential processing and passes IPEX grant verification, with the state left in `exrs` for someone else to read.
- A pin naming the far node's own schema. v1 skips it: `if farCreder.schema != nodeSchema:` gates the check (L485). v2 validates anyway, because skipping "would let a pin be satisfied by the far node asserting its own type, which is the constraint's whole content." (L1612–1613).
- An inline schema-document pin. v2 accepts one whose recomputed SAID equals its `$id` (L1517–1527). v1 cannot read it and returns a non-retryable unknown (L469–482).
- Schema validation itself. v1 builds `schemer = Schemer(raw=scraw)` and verifies the credential with it (`Verifier.processCredential`, L217–219) and for a pin (L496). v2 uses `scheming.validateSchema` (L1625–1626, L1772), which enforces a stricter profile (section 6b).
- Far-node evidence. v1's far node must already be a saved credential (`self.reger.saved.get(keys=nodeSaid)`, L834), and I2I additionally needs the far issuee in the local `subjs` index, a miss being transient (L902–907). v2's far node is a disclosed nest in the same grant, evaluated recursively with its own issuer authentication conjoined (`_evaluateNode`, L1419; `withFarNode`, L1531–1543).
- A compact Edge Section inside a list-valued `e`. v1 yields no group to reduce and returns valid without walking it (`evaluateSection`, L342–349). v2 refuses any `e` that is not a mapping or a list of mappings (`_evaluateNode`, L1385–1391; `_walkGraph`, L1283–1288).
- Nesting depth. v1 bounds it, `MaxEdgeGroupDepth = 8` (`vdr/eventing.py`, L73), raising `ValidationError` past it (`walkEdgeSection`, L129–131). A search of `acdc/ipexing.py` for a depth bound finds none.
- Disposition. v1 raises a typed exception and writes "Exactly one row, even when the members are outstanding on different kinds of evidence." (`disposeSection`, L566–567), cueing a query for every pending member (L574–578). v2 returns False, or raises `MissingSchemaError` or `MissingChainError` to the Exchanger, which escrows (L771–777; section 7d).

### The v1 pipeline (`Verifier.processCredential`) {#v1-pipeline}

Order at `94f5423a3`: (1) registry known, else escrow MRE and cue a TEL query (L188–191); (2) credential state exists, else escrow MRE (L193–197); (3) freshness against `CredentialExpiry` (L199–204); (4) revoked: log and continue (L205–208); (5) schema resolved and `Schemer.verify` passes, else `MissingSchemaError` with escrow MSE or `FailedSchemaValidationError` (L211–224); (6) `e` normalized to a list of blocks, else `ValidationError` (L226–232); (7) each block reduced to one verdict and the blocks conjoined, "the same conjunction a list-valued `e` has always meant here." (L235–236), `chaining.reduceAnd(...)` at L237; (8) one disposition on the reduced verdict (L239); (9) save and `saved` cue (L241–242). Escrows MCE, MSE and MRE are replayed by `processEscrows` with timeouts (L693–700).

Two things `processCredential` does not do are recorded in section 10 item 11: it never compares the credential's issuer with the registry's controller, and it never verifies the anchoring source triple the parser hands it.

The v1 refusal of unrecognized tokens carries an unresolved marker in the shipped code: "Reverses #1552's skip; needs S. Smith's buy-in via ACDC #201" (`verifyChain`, L826). See section 11 item 1.

---

## 7. IPEX V1 — the state machine in `vc/protocoling.py` {#ipex-v1}

All claims here were read at `b8f60166b`; the file is byte-identical at `80f77b73b` and `94f5423a3`. This is one of two IPEX implementations, and it is the one keripy's CLI loads: `cli/commands/ipex/list.py` L25 still reads `from ....vc import loadHandlers, Ipex`, and `grant.py` L22, `admit.py` L22 and `spurn.py` L22 import `loadHandlers` from `....vc.protocoling` (all @`94f5423a3`). Where V1 and V2 differ, this section describes V1 only.

- Verbs: `Ipexage(apply, offer, agree, grant, admit, spurn)` (`protocoling.py:15-16`).
- Legal predecessor table `PreviousRoutes` (`protocoling.py` L16–22): `offer` ← `apply`; `agree` ← `offer`; `grant` ← `agree` (`Ipex.grant: (Ipex.agree,)`, L19); `admit` ← `grant`; `spurn` ← any of `apply`/`offer`/`agree`/`grant`.
- `IpexHandler.verify` (L55–106) enforces the machine: `apply` may only start an exchange; `offer` and `grant` may start one or must reference a prior whose verb is in `PreviousRoutes[verb]`; `admit`, `agree` and `spurn` may never start one; the prior must exist; a prior that already has a response is rejected — `return self.response(pserder) is None` — with the lookup through `db.erpy` (`response`, L108–121); an unmatched route returns False.
- Handlers are registered per route on the `Exchanger` (`loadHandlers`, L478–483 @`b8f60166b`; L471 @`94f5423a3`). exn messages are signed and threshold-verified in `Exchanger.processEvent` before behavior verification, and failure escrows as partially signed.

---

## 7b. IPEX V2 — `acdc/ipexing.py` at `94f5423a3` {#ipex-v2}

All quotes in this section are from `src/keri/acdc/ipexing.py` at `94f5423a3`.

### Scope: tested, not wired {#v2-unwired}

`acdc.ipexing.loadHandlers` (L2851) has no caller in `src/keri`. The only references to the module are the `acdc/__init__.py` re-export (L12) and the module's own docstring; every CLI IPEX command loads V1 (section 7). So the claims here are `[code]` claims about code that exists and is tested in the reference implementation, not about behavior any shipped keripy command performs.

### The machine {#v2-machine}

- The predecessor table differs from V1 in one row: `Ipex.grant: (Ipex.apply, Ipex.agree),` (L41), so a grant may answer an `apply` directly.
- Replies are bound by role and thread: "Replies must target the prior sender and come from the prior receiver" (`_verifyReplyChain`, L942), as equality tests on `ri`/`i` plus the exchange id `x` (L943–951). The single-response rule stands: `if self.response(pserder) is not None:` (L953), through `db.erpy` (L2278).
- Only a flow-starting grant may be spurned: `if verb == Ipex.spurn and pverb == Ipex.grant and pserder.ked.get("p", ""):` → `return None` (L939–940); the builder states the rule, `raise ValueError("only flow-starting grants may be spurned")` (L2823).
- Anchoring (`ax`) is negotiated state. "Binding replies must exactly preserve the negotiated state." (L641) for `agree`, `grant` and `admit`, and "An offer may initiate anchoring, but may not drop it." (L645). `agree` and `admit` satisfy a required anchor only through their sender: "Agree and Admit satisfy anchoring directly through their sender." (L652), checked by `_verifySourceAnchor` (L653–662), which raises `MissingSenderKeyStateError` when the KEL event is not yet local (L843–845).
- A grant with `ax` true needs one qualifying anchorer among the sender, the origin's issuee and the origin's issuer: `candidates = (serder.pre, origin.iseaid, origin.israid)` (L816), drawn from the issuees a presentation registry authenticated (`anchorers = set(tethered)`, L801), the sender if its own seal verifies (L803–807) and every non-sender seal that verifies against that AID's KEL (L809–814). A vacuous grant can be anchored only by its sender: "With no credential AID, only the sender can satisfy Grant ax." (L705).
- The sender authenticates with a seal or a signature, not both. The builder's comment: "A direct sender KEL anchor already authenticates the outer EXN. Sign only when no sender anchor was created so the wire carries one sender factor." (`_sign`, L437–438).

### What an Offer may carry {#v2-offer}

- An Offer may name its origin by SAID with no body. In `verify`, an offer with `a.o` must carry a valid one-element SAID list, and an offer without `a.o` must carry no nests (L592–601). The builder: "A bare SAID creates a commitment-only Offer and cannot be combined with ``artifacts``." (`offer` docstring, L2384–2385), enforced by `raise ValueError("a SAID-only offer origin cannot carry artifacts")` (L2479).
- An Offer that does carry nodes may disclose a reachable subgraph (`_walkGraph(..., closed=False)`, L666), every node must pass its schema (L682), and no node may carry issuer-auth attachments: "Keep issuer proofs on the later Grant." (L671), with `NodeAttachmentFields` listing the forbidden parsed fields (L68–71) and the check at L673–680.

### `dp` — disclosure paths are now enforced on the grant {#dp}

- `dp` is required on `apply`, `offer`, `agree` and `grant` (L582–586), and "Agree changes no disclosure terms; its empty plan always means ditto." (L588), so a non-empty `dp` on an agree is refused (L589–590). An empty plan inherits: `_resolveDisclosurePlan` walks prior messages "until we find a non-empty dp" (L963) and returns `[]` when the thread opener's plan is also empty (L985–987).
- "A Grant may repeat but may not renegotiate an accepted prior plan." (L691), enforced by `if priorPlan is None or plan != priorPlan: return False` (L694–695).
- An empty effective plan means a vacuous grant: "With nothing to disclose, both the origin and body are empty." (L701), `if origins != [] or nests: return False` (L702–703).
- A non-empty plan requires one disclosed origin and a fully closed DAG (`_walkGraph(..., closed=True)`, L722), then is checked against what was disclosed: "First enforce what was requested, then enforce what the accepted Offer promised before authenticating the Grant." (L735–736). `_verifyDisclosurePlan` (L992) follows each entry's DAG path through virtual `_` hops to a node (L1010–1032), requires the entry's schema to equal that node's schema (L1036–1041), and for a field list builds the canonical partial with `compactor.compact(paths=paths, root=root)` and requires the disclosed section to equal it (L1073–1087). The closing check makes the plan exhaustive: "The plan must account for every disclosed node in canonical BFS order." (L1089), `return selected == order` (L1090). Field-list semantics are in the docstring: "An empty field list ([]) permits any valid compaction level, a sole empty-string path ([""]) requires the whole ACDC" (L996–997).
- So a grant that discloses a node the plan does not name, or a section expanded beyond the canonical closure of the requested paths, is refused. This is the first production caller of `Compactor.compact(paths=...)` in `src/keri`, and it is also the bridge between the `dp` path language and the `Compactor` path language: field paths are parsed with `Pather(path=field, relative=True)` (L1059) and grouped by top-level section (L1064–1066) before compaction.
- The path grammar is unchanged in shape: each entry is a triple "of ``[schema SAID, DAG path, ACDC paths]`` for one DAG" (`_validDisclosurePath` docstring, L293–294), the DAG path is `"/"` or a prefix ending at the far-node hop (L311–323), and a field path may not start with `/` and must parse as a relative `Pather` (L331–337).
- A grant may not pass off field-map metadata as the credential: "A Grant may not replay field-map metadata as the credential." (L727), refusing any disclosed node whose ilk is in `FieldMapIlks` with `u` equal to `""` (L728–733).

### A grant must keep the accepted Offer's promise {#offer-fulfillment}

`_verifyOfferFulfillment` (L1136) follows the Agree to the Offer it accepted (L1155–1160). An Offer with no origin promises nothing in particular (L1162–1165). "The same root SAID directly fulfills the Offer." (L1171). A different root is allowed only when the Offer disclosed field-map metadata: "Only field-map metadata can promise a different credential root." (L1198), after which the grant must match the offered issuer (L1208–1210), any non-empty offered `rd` (L1212–1215), and the canonical commitment of every non-empty offered section among `s`, `a`, `A`, `e`, `r` (L1217–1231). A SAID-only Offer whose root differs from the grant's has no metadata body to compare and raises `MissingChainError` (L1180–1182), which the Exchanger escrows; whether such a grant can ever succeed depends on the metadata arriving later, which this pass did not trace.

### Graph shape and node integrity {#graph-shape}

- `_walkGraph` (L1235) is a BFS from the origin. With `closed=True` a dangling edge target aborts the walk (L1307–1310); with `closed=False` it is skipped. Either way "every carried nest must still be part of the root-reachable disclosed graph." (L1330–1331), `if len(seen) != len(nodes): return None` (L1331–1332).
- `_validNodeNest` (L849) requires each nest to verify, to be an ACDC of a disclosed-node ilk (`if nserder.proto != Protocols.acdc or nserder.ilk not in DisclosedNodeIlks:`, L868), to have every expanded section and aggregate element SAID match its content (L871–902), and to be unique: "Each disclosed DAG node must occupy exactly one nest so the node body cannot appear twice with conflicting attachment groups." (L906–907).

### The grant DAG evaluates to one verdict {#v2-verdict}

Stage 6 of `verify` evaluates the disclosed DAG from the origin. "A node's verdict is its own issuer-auth proof conjoined with its reduced Edge Section" (L748–749), `memo[said] = chaining.reduceAnd([auth, section])` (`_evaluateNode`, L1419). An unknown the recipient can still resolve is escalated for escrow — a missing schema as itself, anything else as `MissingChainError` — and every other non-valid verdict refuses (L761–777). The issuer-auth of each node is itself a verdict "so an Operator that does not need this node is not made to wait on it or fail because of it." (`_verifyIssuerAuthNode` docstring, L1802–1803). This means a node behind an OR branch the grant does not need may fail its issuer authentication without failing the grant. The memo placeholder is not a cycle check: "The disclosed graph is digest-linked and so cannot contain a cycle" (L1365–1366).

### Issuer authentication: three factors, one selected {#issuer-auth}

`_authenticateIssuer` (L1821) tries the factors in order and does not fall through once one is selected.

- Factor 1, registry, when the node carries a top-level `rd` (L1836–1842), vetted by `_vetRegistry` → `regeventing.vetBinds` (L2062–2071), which must name the declared registry (L2074–2077). `vetBinds`'s rule, owned by `raw/16`, is that every blinded update "from the verified head back through the latest non-vacuous update must have exactly one matching disclosure" (`acdc/regeventing.py` `vetBinds` docstring, L651–652).
- Factor 2, seal anchor: issuer source couples, or source triples naming the issuer, verified against the issuer's KEL (L1866–1891), and "An invalid anchor must not silently downgrade the ACDC to signature authentication." (L1889–1890).
- Factor 3, signatures, and only current ones: explicit groups are kept "that already name the current state" (L1927), bare and last-establishment signatures are bound to the current `lastEst` (L1919–1934), and the node passes on `return bool(validTsgs or validCigars)` (L1953). An ACDC signed under issuer keys that have since rotated, with no registry and no anchor, does not authenticate under factor 3; this is read from L1911–1934, not run.
- Failure classes in `_vetRegistry`: `MissingAnchorError` becomes a retryable `MissingChainError` (L2082–2083); `MisanchorError` is retryable only when a required source was unresolved (L2086–2090); seven named errors are permanent, among them `MisdigestError` (L2093–2096). A missing inception, head or sequence gap in the local TEL raises `MissingChainError` (L1989–2001), and with no injected `Regery` the factor fails (L1981–1982).

### Endorsements, anchorers and source seals across rotation {#endorsement}

- Endorsers are "Additional local habitats that sign the same outer exchange as non-sender endorsers (e.g. principal AIDs)." (`_sign` docstring, L354–355); in the grant builder, "The sender remains the Discloser and KRAM-authenticated outer sender." (`grant` docstring, L2608). Anchorers are "Additional local transferable habitats whose KELs seal the same outer exchange." (L356–357), each named in a source triple (L430–431), and an empty `anchorers` list "leaves anchoring to a presentation registry." (`grant` docstring, L2611).
- `verifyEvidence` (L2210) keeps a grant's non-sender signature endorsements only at the endorser's current establishment event — "Require exact current establishment coordinates." (L2239) — but keeps every verified source seal regardless of later rotation: "A later key rotation does not invalidate that permanent commitment." (L2247–2248). A valid seal displaces a signature endorsement from the same AID (L2251–2256). Every other verb rejects any supplemental evidence (L2261–2263).
- `verify` then discards the endorsement signatures: `_, _, extraSeals = evidence` (L784). Only seals count, and only toward anchoring. Endorsement signatures are persisted and indexed by the Exchanger (section 7d) but play no part in deciding whether a grant is valid under the default policy.

### Presentation registries, as IPEX consumes them {#presentation-registries}

The semantics belong to `raw/16`; this records only the mechanism. Every disclosed node's presentation-registry declaration is required, with one exemption: "Only the origin being issued is exempt. Linked credentials are existing disclosures whose presentation requirements still apply." (`_verifyPresentationAuthGraph`, L2168–2169), where an issuance is a grant from the origin's issuer to its issuee (L2147–2148). A requirement needs a completed KRAM acceptance: "A presentation requirement needs a completed KRAM acceptance." (L2181), read from `self.hby.db.kramTMSC` (L2178–2179). Each registry is vetted with `controller=issuee`, `cutoff=cache.rdt` and `requireSource=True` (L2192–2198). A declaration is refused when it might be hidden (`_presentationRegistries`, L2099–2138).

### Schema validation and the missing-schema escrow {#schema-validation}

`acdc/scheming.py` is rewritten as a local-only JSON Schema validator. `validateSchema(acdc, db, schema=None)` (L426) validates against the ACDC's own `s` or a supplied pin, and "Draft 2020-12 validation uses only locally available schemas." (docstring, L431–432). A schema by SAID that is not cached raises `MissingSchemaError` (L466–468); every schema must recompute to its claimed SAID (`_verifySchemer`, L238–288), must use its bare SAID as `$id` and carry a plain `major.minor.patch` version (`_checkProfile`, L291 onward; `_checkVersion`, L105), and may not use dynamic references (`_inspectSchema`, L204–208). External references are accepted only when "statically SAID-bound" (`_referenceSaid`, L101), and the local registry "never downloads a schema" (`_registry` docstring, L343).

Callers at `94f5423a3`: IPEX V2 (every Offer node, every grant node and every edge pin, L682, L1625, L1772); blind issuance in `acdc/regeventing.py`, under the comment "Reject malformed credentials before deriving or staging an issuance event." (`_RegEventer.blind`, L1000), so a malformed ACDC is refused before any TEL event is staged. Not the v1 `Verifier`, which still calls `Schemer.verify` (section 6).

On the exchange side, a `MissingSchemaError` from behavior verification escrows the message under `(exchange SAID, schema SAID)` in the new `Baser.emse` and cues a schema query (`peer/exchanging.py` `Exchanger.processEvent`, L409–427). One deadline covers every missing schema of one exchange, "Keep one deadline for all missing schemas in this exchange" (`escrowMSEvent`, L535), stored in `Baser.emsd`, and taken from the KRAM cache when there is one (L536–546).

---

## 7c. `Compactor` invariants (`core/mapping.py`, unchanged since `b8f60166b`) {#compactor}

Quotes at `b8f60166b`; the file is unchanged at `94f5423a3`. A targeted disclosure cannot be taken from an already compacted mapping — `raise InvalidValueError("Cannot disclose from compact mapping")` (L1146) — and the call is destructive: "A targeted call consumes the expanded mapping. Use a new Compactor instance to create another targeted partial." (L1125–1126). IPEX's `_verifyDisclosurePlan` respects this by building a fresh `Compactor` per section (`acdc/ipexing.py` L1073–1076 @`94f5423a3`). Whole-node disclosure preserves descendants: "Preserve every nested mapping for whole-node disclosure." (L1192). Restoration order is load-bearing: "Restore marked ancestors before descendants from canonical leaves." (L1224), implemented by sorting the marked paths by length (L1226).

---

## 7d. EXN evidence and the durable exchange stores (`peer/exchanging.py`, `db/basing.py`) {#exn-evidence}

Claims at `80f77b73b`; the `peer/exchanging.py` passages named in the header were re-read at `94f5423a3` and the hints below are current there. `db/basing.py` hints are at `80f77b73b` except where marked.

- A route opts into an evidence policy, and the absence of one is itself a policy. `evidenceVerifier = getattr(behavior, "verifyEvidence", None)` (L142). Routes without one keep the old precedence: "Routes without an evidence policy preserve the existing TSG-over-cigar precedence. A sender TSG causes all cigars to be ignored." (L187–189).
- Sender authentication has two independent satisfiers. "A valid sender seal authenticates the EXN. Retain only valid optional sender TSGs and do not fail on invalid ones." (L215–216). Once a seal authenticates, a bad optional TSG is tolerated rather than fatal; do not simplify this into a conjunction.
- Missing sender-KEL evidence escrows only for handlers that opted in: "IPEX uses sender seals as required workflow evidence, so retain the complete message until the referenced sender KEL arrives." (L204–205), gated on `acceptsSscs` (L206), which `IpexHandler` sets (`acdc/ipexing.py` L480).
- Foreign key state is frozen before escrow: "Freeze foreign last-establishment references before sender escrow can return, so replay retains the evidence and its original keys." (L149–150), so a replayed message is judged against the keys current when it arrived.
- A route can opt out of fail-closed handling of unresolved foreign evidence: "Opted routes request the KEL and continue with known factors." (L170). In IPEX only the grant route opts in, `self.acceptsMissingEvidence = resource == "/ipex/grant"` (`acdc/ipexing.py` L523).
- Only a handler that sets `acceptsEvidence` receives the policy-selected evidence: "Pass selected evidence only to handlers that advertise support." (L386), `verifyKwa["evidence"] = (tsgs, cigars, sourceSeals)` (L389).
- IPEX preserves what it defers on and drops what it refuses. A `MissingChainError` from behavior verification escrows and cues a proof fetch, returning `None`: "Registry-backed IPEX grants may arrive before the disclosee has fetched the issuer's TEL history from observers." (L396–398). A `MissingSchemaError` escrows in `emse` (section 7b). A behavior `verify` returning False returns False before `logEvent` (L391–394 precede L431–434), so a refused message is not persisted.
- Escrow replay trims before rewriting: "The same stores hold escrowed and accepted evidence. Remove the temporary branches so processEvent writes back only the evidence that passes current verification and policy." (L628–630), executed as `esigs.trim` / `ecigs.rem` / `ests.trim` (L631–633).
- Accepted non-sender evidence is reverse-indexed by AID in `.eidx`, and source-seal anchorers now enter it alongside signers: "Include each approved source-seal anchorer." (L373). The writer states its boundary: "Only behavior-approved non-sender endorsements enter this durable reverse index; sender authentication and escrow evidence do not." (L752–753).
- Durable stores (`db/basing.py`): `.enst` "for exchange message nested child substreams." (L573–575), `.essrs` "for exchange message event source records." (L578–580), and `.ests` "for resolved exchange source seals." (L583–585). `.ests` names which table is authoritative: "The exchange message in ``exns`` remains the acceptance marker." (L588–589), so presence in an evidence table is not acceptance. New at `94f5423a3`: `.emse`/`.emsd` (missing-schema escrow and its deadline) and `.exrs` (registry state per accepted grant node), the last described as "Recorded, never judged on the protocol path." (`Baser` docstring for `.exrs`). The single-response pointer is unchanged: `self.erpy = subing.CesrSuber(db=self, subkey="erpy.", klas=coring.Saider)` (L1130).

---

## 8. CESR framing (`core/counting.py`) {#cesr-framing}

Claims at `80f77b73b` unless marked; the code tables are unchanged at `94f5423a3`.

- CESR is genus- and version-aware: `GenusCodex`/`GenDex` map protocol genera to code tables (`counting.py:24-44` @`3a8e01ae`); counters differ across `Vrsn_1_0`/`Vrsn_2_0` (`CounterCodex_1_0`).
- The counter codes are the attachment doctrine. The v1 table (L56–76 @`80f77b73b`): `-A` ControllerIdxSigs, `-B` WitnessIdxSigs, `-C` NonTransReceiptCouples (pre+cig), `-E` FirstSeenReplayCouples (fnu+dts), `-F` TransIdxSigGroups, `-G` SealSourceCouples (snu+dig, the anchoring couple), `-I` SealSourceTriples (pre+snu+dig), `-L` PathedMaterialCouples (SAD-path attachments; `PathedMaterialCouples: str = '-L'  # Composed Grouped Pathed Material Quadlet (4 char each)`, L64), `-Z` ESSRPayloadGroup. Everything is quadlet-aligned. `-D` TransReceiptIdxSigGroups is gone from the v1 table; see section 8b.
- Sizing is exact and self-describing: `Matter.Sizes[code].fs` gives full size (the SAID dummy fill, `coring.py` L3899 @`80f77b73b`), and the leading selector determines parse length, so there are no delimiters. The verifier fails closed on a size mismatch (the SAID `versioned` check, L3962–3964 @`80f77b73b`).

---

## 8b. Count-code and seal changes, and where the CESR spec stands {#count-codes}

All keripy quotes in this section are at `80f77b73b`; `core/counting.py` and `core/structing.py` are unchanged in their tables at `94f5423a3`, and a grep there confirms `NonceSeal` appears only in `counting.py` L228–229 and `structing.py` L75, L468 and L1249. The commits are Sam Smith's, merged in PR #1683 (merge commit `13cafb5d3`): `9762d6bb4`, `e24ade8c7`, `d8bb23308`, `8a4f3f0c4`, `4d5535717`, `370a656a8` and `da82a6422`.

### `TransReceiptIdxSigGroups` is gone from keripy, in both versions {#trans-receipts}

`CounterCodex_1_0` runs `-A`, `-B`, `-C`, then `-E` (`counting.py` L56–59); `-D` appears nowhere in it, nor in `QuadTripCodex_1_0` (L94–105). The v1 size table keeps the line only as a comment, `#'-D': Cizage(hs=2, ss=2, fs=4),` (L618). Because `Counter.Sizes` has no live `'-D'` entry for v1, a CESR v1 stream carrying a `-D` group has no size to parse against; this pass did not run a parse to see the exact failure. The parser handlers `_TransReceiptIdxSigGroups1`/`2` and their `Methods` registrations were deleted, and the `rsgs` field survives only as a comment (`parsing.py` L52, still so at `94f5423a3`). `structing.TransReceipts` was deleted, and `messagize` lost its `rsgs` parameter (`eventing.py` L1563–1564).

### What replaced it: transferable endorsements travel as `TransIdxSigGroups` {#tsgs}

Attached non-controller signatures on a key event arrive as `tsgs` and go to the handler that used to take `rsgs`: `if exts['tsgs']:  # tsgs  TransIdxSigGroups (was trqs)` → `kvy.processAttachedReceiptSigGroups(**exts)` (`parsing.py` L1412–1413). A receipt message needs one of `cigars`, `wigers` or `tsgs` (L1422). The handler's signature became `def processAttachedReceiptSigGroups(self, serder, tsgs, *, firner=None,` (`eventing.py` L4872), its docstring calls each group "an endorsement from a transferable AID that is not the controller. Maybe a watcher." (L4874–4875), and `messagize` describes `tsgs` as "controller or non-controller idx sigs or endorsements" (L1576). The `rsgs` loop in `Kevery.processReceipt` is commented out (L4571–4627). A transferable receipt is no longer a distinct wire type in keripy; it is a `TransIdxSigGroups` group — `-F` in v1, `-X` in v2 (`counting.py` L60, L248) — whose signer is not the event's controller.

### v2 `-N` was reassigned {#nonce-seal}

`NonceSealSingles: str = '-N'  # Nonce Seal Single(s), nonce as sealed data, nonce or dig.` (`counting.py` L228; `--N` big form L229). The structure behind it: `SealNonce = namedtuple("SealNonce", 'nd')` with the comment "nd = nonce or digest qb64 as data" (`structing.py` L73–76), cast `SealNonce(nd=Castage(Noncer))` (L240, L435), and mapped `ClanToCodens[AClanDom.SealNonce.__name__] = Codens.NonceSealSingles` (L468; also `Sealer.ClanCodens`, L1249). The comment above it says `uniple (d,)` while the field is `nd`, a small inconsistency in the source.

`-N` is defined but not wired into CESR-native event serialization or stream parsing: `NonceSealSingles` is absent from `SealCodex_2_0` (`counting.py` L392–405), absent from `Serder.ClanCodes` (`serdering.py` L342–348), and has no entry in `Parser.Methods`. The `structing.py` maps are not inert, though: the generic `Structor.enclose`/`extract` read `ClanCodens`/`CodenClans` (`structing.py` L601–602, L646–652, L687, L700), and v2 `messagize` accepts any bond whose clan is in `AClanDom` (`if (structor.clan not in AClanDom):`, `eventing.py` L1851), which includes `SealNonce` (`structing.py` L396), framing each clan group with `Structor.enclose` (`eventing.py` L1859–1860). So, read from the code and not run, keripy's v2 `messagize` appears able to emit a `-N` attachment group that keripy's own `Parser` could not parse. No `src/keri` caller was found passing a `SealNonce` bond. The SEDI tests use the seal in JSON event bodies — `data=[dict(nd=challenge)]` (`tests/sedi/test_ipex_sedi.py` L214) and `SealNonce(nd=guyChallenge)` round-tripped through `Structor` (`tests/sedi/test_sedi.py` L3709–3713) — which does not exercise the CESR-native path.

### `SealKind.d` and TDCS are `Noncer`, not `Diger` {#noncer}

"d = digest or nonce using custom derivation given by type field (Noncer)" (`structing.py` L69), cast `d=Castage(Noncer)` (L239, L434), and the TDCS parser does `noncer = self.extract(ims=gims, klas=Noncer, cold=cold)` (`parsing.py` L2198). `Noncer` admits every digest code plus salts and an empty value: `NonceCodex` lists `Empty` '1AAP', `Salt_128` '0A', `Salt_256` 'a' and nine digest codes (`coring.py` L470–487). So a typed-digest seal may carry a salty nonce rather than a content digest. The comment on the line above has a stray token, `# t = type of digest as (Verser)moo` (L68).

The "refactored challenge so its a digest" commit (`370a656a8`) has no behavioral footprint in `src/keri`: it touched a `core/coring.py` docstring typo, a `core/signing.py` docstring reflow and `tests/sedi/test_sedi.py`. The challenge lives in the tests, where it is a 128-bit salty nonce anchored as a `SealNonce`: `guyCns = SealNonce(nd=guyChallenge)` (`tests/sedi/test_sedi.py` L3709), with `guyChallenge == '0ABndXlzZWRpY2hhbGxlbmdl'  # CESR encoded 128 bit nonce` (L3706).

### CESR specification cross-check (read-only, both spec pins) {#cesr-spec-check}

The spec defines a count-code table only for v2: its sole master table is "Master code table for genus/version `-_AAACAA` (KERI/ACDC protocol stack Version 2.00)" (`spec/spec-body.md` L872 @`bad6edd84` on `main`; L880 @`65fd7518b` on `v1.1`). Neither branch contains a v1 count-code table, so keripy's removal of v1 `-D` has no spec text to diverge from. In the v2 universal table `-D` is "Datagram Stream Segment up to 4,095 quadlets/triplets" (L840 @`bad6edd84`, L848 @`65fd7518b`), matching keripy's `DatagramSegmentGroup: str = '-D'` (`counting.py` L208).

On v2 `-N` the spec and keripy diverge at both spec pins. Both branches define `-N##` as "Transferable identifier receipt quadruples pre+snu+dig+sig up to 4,095 quadlets/triplets" (`spec/spec-body.md` L915 @`bad6edd84`; L923 @`65fd7518b`), and keripy assigns the same code to `NonceSealSingles`. A v2 stream produced by keripy with a `-N` group would be read by a spec-following parser as transferable receipt quadruples, and the reverse. This is `[code]` against `[spec]`; the row is identical on `main` and `v1.1`. A milder version of the pattern: the spec's `-W` row reads "Typed digest seal couples `type+dig`" (L933 @`bad6edd84`; L941 @`65fd7518b`), while keripy casts the second element to `Noncer`, which accepts nonces as well as digests.

---

## 9. Prose-versus-machine gaps {#gaps}

- DI2I: the ACDC prose gives it a meaning; keripy evaluates neither half of it. Both evaluators recognize it and return a non-retryable unknown (`vdr/verifying.py` L871–873, `acdc/ipexing.py` L1573–1578 @`94f5423a3`). Sam's account of why it exists is on record in [#1515](https://github.com/WebOfTrust/keripy/discussions/1515): a QVI horizontally scaling its signing hosts, "This came up in discussions with QVIs in the context of the EBA pilot, so we put it in the spec.  But the EBA backed out", and "That use case has yet been implemented by anyone AFAIK." (comment of 2026-07-18T15:08:31Z). That is his assessment, not a survey.
- I2I as "chain of authority": the machine reality is one AID string equality (section 6), not multi-hop authority evaluation. Multi-hop is the recursive walk — v1 reaches only one hop per credential and relies on the far node having been processed itself; v2 recurses through the disclosed DAG — and neither re-derives delegated authority. The point was put to Sam in #1515 — the deployed I2I "is computed as that equality and nothing more" (Daniel Hardman, 2026-07-18T00:01:13Z) — and his reply did not dispute the mechanism: "The short answer is I don't know yet for sure.  Its something to be sussed out." (2026-07-18T14:50:25Z).
- The default operator: an edge with no `o` is checked as I2I or NI2I by both evaluators (section 6). An "explicit operator" reading of the prose is softer than the code, which supplies one.
- Revocation: v1 saves a revoked root credential and refuses a chain through a revoked far node (section 4, section 6); v2 records far-node registry state without judging it (section 6). Revocation as invalidation is therefore a v1 behavior on chains only, and a policy left open on the v2 path.
- Schema trust: both evaluators resolve schemas from a local cache only. v1 escrows and cues a query when a schema is absent (`vdr/verifying.py` L211–215); v2 raises `MissingSchemaError` and the Exchanger escrows (section 7b). Neither fetches trust roots from a global authority.

---

## 10. Named negative results at `94f5423a3` {#negative-results}

Each was looked for deliberately at `94f5423a3` and not found. Each is a claim about the code at this commit and should be re-tested at the next pin.

1. No evaluation of DI2I anywhere in `src/keri`. A search for `DI2I` returns the two operator tables in each evaluator, the two default-suppressing sets, comments, and the two sites that return a non-retryable unknown (`vdr/verifying.py:871-873`, `acdc/ipexing.py:1573-1578`).
2. No DAG acyclicity check. `_walkGraph` is a BFS with a `seen` set (`acdc/ipexing.py:1263-1275`), and `_evaluateNode` installs a memo placeholder against re-entry (L1368–1369), so a cycle would terminate rather than be reported. Both modules now state why they do not check: "SAID-based references make a cycle infeasible to construct, so this is not a cycle guard" (`vdr/eventing.py` L69–70), and "The disclosed graph is digest-linked and so cannot contain a cycle" (`acdc/ipexing.py` L1365–1366). A search for `acyclic` or the word `cycle` in `src/keri` finds only those comments, scheduler cycle-time docstrings, "Import lazily to avoid the ACDC module cycle." (`acdc/ipexing.py` L2017) and the `db/subing.py` diamond-graph docstring (L11).
3. No post-quantum signature codes. A case-insensitive search of `src/keri` for `dilithium|ml-dsa|mldsa|slh-dsa|slhdsa|fn-dsa|fndsa|sphincs|kyber|ml-kem|post.?quantum` returns nothing. (`falcon` was left out of the pattern this time because it matches only the HTTP framework.)
4. The V2 IPEX handler is not wired into keripy's CLI. `acdc.ipexing.loadHandlers` (L2851) has no caller in `src/keri`; every `cli/commands/ipex/*` command loads V1 (section 7).
5. No `I1I` or `DI1I` in `src/keri`. Both are absent from both operator tables (`vdr/verifying.py` L66, `acdc/ipexing.py` L55). They now appear in test data: six SEDI leaf edges in `tests/sedi/test_sedi.py` carry `"o": ["E1E", "DI1I", "NI2I"]` (L5876 and five more), and `tests/vdr/test_verifying.py` uses `I1I` as its example of an unrecognized token (L2321–2328). `test_sedi.py` calls neither evaluator (no `IpexHandler`, `Verifier(` or `processCredential` in the file), so those fixtures are built and never evaluated. Under either evaluator at this pin, an edge carrying `DI1I` is an unknown no arrival settles, so a SEDI leaf whose only edge to the core carries that list would be refused unless an OR sibling decides the group (section 6, inference from the code). keripy PR #1707 used the operators in SEDI examples; that is test data, not an implementation.
6. `NonceSealSingles` (`-N`) is not wired into stream parsing: no `NonceSeal` match in `core/parsing.py`. The narrowing in section 8b, that v2 `messagize` could emit a `-N` attachment group, was not re-read at this pin.
7. IPEX grant verification does not use endorsement signatures (`_, _, extraSeals = evidence`, `acdc/ipexing.py:784`; section 7b).
8. No `TransReceiptIdxSigGroups` in live keripy code: the only `src/keri` occurrence is the `rsgs` comment (`core/parsing.py:52`).
9. No registry-state judgement on the V2 path: `IpexHandler` records the state of each disclosed node's registry in `exrs` and refuses nothing on its basis (section 6).
10. No explicit Edge-group nesting bound on the V2 path: a search of `acdc/ipexing.py` for a depth limit finds none, while v1 stops at `MaxEdgeGroupDepth = 8` (section 6).
11. The v1 `Verifier` does not check that a credential's issuer controls the registry it names. keripy issue #1730 (Daniel Hardman, open) reports this; the code at `94f5423a3` confirms it. `processCredential` reads `creder.israid` in two places only, a TEL query cue (`vdr/verifying.py` L190) and the issuer index in `saveCredential` (`issuer = creder.israid.encode("utf-8")`, L760), and the edge check (L431). It never compares it with the registry's controller, `self.pre = ked["ii"]` (`vdr/eventing.py` `Tever`, L880), and never verifies the source triple the parser passes in (`prefixer, number, diger = exts['ssts'][-1]`, `core/parsing.py` L1693), which it only stores (`self.reger.logCred(creder, prefixer, seqner, saider)`, L757). The TEL does bind the credential SAID to an issuance anchored in the registry controller's KEL, so what goes unchecked is the credential's own `i` field: a credential naming issuer X, issued in a registry controlled by Y, is saved and indexed under X. V2 differs: factor 1 requires `vetBinds` with the ACDC passed in (section 7b), and `raw/16` owns whether `vetBinds` checks the issuer.

---

## 11. Open questions and unresolved tensions {#open-questions}

1. Is refusing an unrecognized unary operator keripy's position, or only the v1 code's? Both evaluators now treat an unrecognized token as a non-retryable unknown (section 6), but the v1 site carries "Reverses #1552's skip; needs S. Smith's buy-in via ACDC #201" (`vdr/verifying.py` L826). The behavior is merged; the comment says the buy-in it depends on is not recorded. `raw/21` should check kswg-acdc-specification issue #201 for a ruling. Until one exists, the refusal is `[code]` and the spec's silence on a fifth token is what the comment itself says it is.
2. The spec citations in the edge code are unverified. Latest-wins "among the conflicting Operators", the default rule's suppressing list with `E1E` "on the ACDC v1.1 line" (`acdc/ipexing.py` L58–63), the m-ary table's wording (`acdc/chaining.py` L132–133, L162–163) and `E1E` "normative on the spec's v1.1 branch (kswg-acdc-specification#197)" (`vdr/verifying.py` L63) are all the implementation's claims, written by the corpus's author. `raw/03` must confirm each against `kswg-acdc-specification` before any chapter cites them as `[spec]` or `[spec-next]`.
3. Is `E1E` anywhere but keripy? Its provenance is a `[proposal]` in [#1515](https://github.com/WebOfTrust/keripy/discussions/1515), "New Unary Edge Operators to Support SEDI", opened by Sam Smith on 2026-07-17: "E1E which means near side IssueE AID must equal far side IssueE AID." The same post proposes `I1I`, `I1E`, `E1I`, the "3" equivalence operators `I3I`/`E3E`, and `DI1I`. After Daniel Hardman argued for adopting `E1E` alone (2026-07-18T00:01:13Z), Sam narrowed the proposal: "The only concrete use case we have is for E1E, and we want to avoid it falling into the unknown operator trap." (2026-07-18T15:08:31Z). He deferred the "3" class and left `I1E` open. `E1E` is `[code]` in keripy; whether it is `[spec-next]` turns on the ACDC spec's `v1.1` branch (item 2).
4. `I1I` and `DI1I` have a use case and test fixtures but no implementation (`[proposal]`). Sam's comment "Concrete Use Case in SEDI for I1I and DI1I operators" (#1515, 2026-10-01T19:58:12Z) says "the leaf edge to the core is both E1E and I1I  that is issuee is issuee and issuer is issuer.", and that DI1I replaces I1I when "the delegation edge for the core is DI2I". keripy's SEDI fixtures now carry `["E1E", "DI1I", "NI2I"]` (section 10 item 5), which neither evaluator can satisfy. Either an implementation is coming, or the fixtures encode a design the reference code would refuse; the tests do not say which, because they never evaluate those edges.
5. Sam's last paragraph on 2026-10-01 says "I2I" where the context seems to call for "I1I": "the issuer can add I2I operator to the one E1E edge in the former case or leave out the I1I operator" (#1515, 2026-10-01T19:58:12Z). "The former case" is the same-issuer case, where the preceding paragraphs want I1I. This note reads it as a probable slip for I1I and does not correct it. If deliberate, it means adding a delegative I2I to an E1E edge, a different design. The fixtures in item 4 do not settle it, since they carry neither I1I nor I2I.
6. Should a revoked far node fail a presentation? v1 refuses it and v2 records it for "an application or EGF evaluator" (section 6). The v2 comment grounds this in the spec's per-registry transaction states and EGF-assigned edge validity; the v1 behavior predates that reasoning. Neither file acknowledges the other on this point, and the same chain therefore passes one path and fails the other.
7. Is "current keys only" the intended rule for issuer-signature authentication in IPEX? Factor 3 keeps only signatures that name the issuer's current establishment event (section 7b), while `verifyEvidence` keeps a source seal across rotation because "A later key rotation does not invalidate that permanent commitment." (`acdc/ipexing.py` L2247–2248). The asymmetry between seals and signatures is explicit for endorsements and reasoned there; for factor 3 the filter is stated without a reason. If intended, an issuer's rotation invalidates every registry-less, unanchored ACDC it signed, for IPEX purposes.
8. Does a SAID-only Offer followed by a different-root grant ever succeed? `_verifyOfferFulfillment` raises `MissingChainError` when the accepted Offer has no metadata body (`acdc/ipexing.py` L1180–1182), and the Exchanger escrows on that. If nothing ever delivers a body for a SAID-only Offer, the escrow ages out and the grant is effectively bound to the exact offered root. This pass did not trace whether any path supplies one.
9. Does the V2 grant's freedom to reply directly to an `apply` (`acdc/ipexing.py` L41) reflect a spec change or an implementation convenience? V1 still requires `agree` first (`vc/protocoling.py` L19).
10. Are the seven named `vetBinds` refusals the right permanent/retryable split? `_vetRegistry` hard-codes `MissingAnchorError` as retryable, `MisanchorError` as conditionally retryable, and seven others as permanent (`acdc/ipexing.py` L2082–2096). `MisdigestError` is on the permanent list there, while its class docstring says it "is not permanent" on a KEL (`kering.py` L822); for a TEL the code treats it as permanent, and whether a TEL can recover the way a KEL can is `raw/16`'s question.
11. Is the v2 `-N` reassignment going to the CESR spec, and in which branch? keripy's `-N` is `NonceSealSingles`; the CESR spec on both `main` `bad6edd84` and `v1.1` `65fd7518b` still says "Transferable identifier receipt quadruples" (section 8b). Nothing in the spec repos at those pins records an intent. A candidate for Daniel to raise on the CESR spec repo himself.
12. Should IPEX V2 bound Edge-group nesting the way v1 does? v1 stops at depth 8 "so a pathologically deep (or hand-crafted) Edge Section cannot exhaust the stack" (`vdr/eventing.py` L71–72); v2 recurses with no bound found (section 10 item 10). Python's recursion limit would stop it eventually, which is a crash rather than a refusal.
13. The witness-pool second-factor claim in section 2 is unsupported by a quote in this note. The `Kever` docstring it rests on has irregular wording at `94f5423a3`, "thereby making the controller's" then "signature (s): the first factor" (`core/eventing.py` L3023–3024), which a quote must reproduce exactly. The claim needs a fresh verbatim quote from that docstring (L3021–3027 @`94f5423a3`); the KERI specification states the same structure on `main` (`spec/spec-body.md` L1764 @`fbdd4a615`), which `raw/01` owns.
