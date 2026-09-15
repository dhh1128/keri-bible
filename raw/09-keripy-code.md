# KERI/ACDC/CESR Doctrine — Ground Truth from the keripy Reference Implementation

Source: keripy, `src/keri` (Python reference implementation), repo `~/code/wot/keripy`. Mandate: what the code ACTUALLY enforces vs. what prose claims. Every "code does X" claim carries a quote and a `file:line` hint. Read-only pass; nothing modified.

## Pin and coverage

**Pinned commit: `b8f60166b`** (`main`, 2026-09-14, "Merge pull request #1668 from evanja57/compactor-disclosure-test"). Mining date 2026-09-15. Prior pin for this note was `3a8e01ae` (2026-07-17).

**Version fact that scopes every `[K]` claim in this corpus.** `__version__ = '2.1.0-dev1' # also change in setup.py` (`src/keri/__init__.py` L3 @`b8f60166b`). The corpus's older keripy material was tagged against 2.0.0-dev6; the line has moved to the 2.1 development series. Nothing here is a release.

**Modules actually re-read at `b8f60166b` in this pass** — claims below carrying that pin rest on reading the file at that commit: `vdr/verifying.py` (whole file), `acdc/ipexing.py` (L1–300, L330–1230, L1604–1622), `core/mapping.py` (`Compactor.trace`/`_trace`/`compact`, L930–1245), `peer/exchanging.py` (L95–360, L440–475), `db/basing.py` (L525–610, L1100–1140), `vc/protocoling.py` (L1–135, L478–483), `core/serdering.py` (`.iseaid` property, L2823–2855), `src/keri/__init__.py`.

**Modules NOT re-read at `b8f60166b`.** Everything in §1–§5 and §8 below — `core/coring.py`, `core/eventing.py`, `core/counting.py`, `vdr/eventing.py` — still stands at `3a8e01ae` and its line hints are hints as of that commit. Those claims were not re-verified in this pass and should not be read as pinned to `b8f60166b`. Likewise not re-read: `app/habbing.py`, `core/signing.py`, `acdc/regeventing.py`, `acdc/messaging.py`, `acdc/acdcing.py`, `acdc/containing.py`, `core/structing.py`. `core/kraming.py` belongs to `raw/15`; registry/TEL status (`acdc/regeventing.py`, `acdc/messaging.py`, `acdc/regbasing.py`) belongs to `raw/16` — findings that touch them are flagged as cross-references, not recorded here as the primary record.

**What this pass covered.** The `dp` (disclosure-path) construct as landed in code; the IPEX rework in the new `acdc/ipexing.py`; edge-operator and graph-semantics validation; EXN evidence handling and the durable exchange stores; the version line; and a set of named negative results.

**A note on quote form.** keripy wraps its comments and docstrings at ~80 columns. Where a quote below is longer than one source line, the words are verbatim and only the source's own line breaks and comment markers have been removed; the line hint then names the range the quote spans. No quote joins text across a blank line, a different comment block, or an intervening statement.

---

## 1. What KERI/ACDC/CESR fundamentally IS — as embodied in the verifier

### AID = self-certifying autonomic identifier, root of trust is the key state itself
- `Prefixer` is "Matter subclass for autonomic identifier AID prefix" (`core/coring.py:3807-3809`). An AID prefix is a fully-qualified cryptographic primitive (CESR `Matter`) — either a **basic** derivation (public key embedded, non-transferable) or a **self-addressing** derivation (digest of the inception event). There is NO external authority, registry, or CA; the identifier IS its own cryptographic material.
- Derivation codes (`core/coring.py:244-294`): `B` = "Ed25519 verification key non-transferable, basic derivation"; `E` = "Blake3 256 bit digest self-addressing derivation". `1AAA`/`1AAC`/`1AAI` = non-transferable ECDSA/Ed448/secp256r1. The code prefix (the leading selector char) tells the verifier the crypto suite — **crypto agility is structural**, not negotiated.
- `PreDex` gate: `Prefixer.__init__` raises `InvalidCodeError` if code not in `PreDex` (`coring.py:3830-3831`). Only prefixive codes may be AIDs.

### SAID = Self-Addressing IDentifier: content-hash self-reference, computed by dummy-fill
Ground-truth mechanism (`core/coring.py:4058-4096`, `Saider._derive`):
1. Copy the `sad` dict; **fill the id field with dummy chars** to the exact full size of the digest: `sad[label] = clas.Dummy * Matter.Sizes[code].fs` (`coring.py:4085`). `Dummy = "#"` — "dummy spaceholder char for said. Must not be a valid Base64 char" (`coring.py:3949`).
2. If versioned, recompute the version-string size over the dummied serialization (`sizeify`, `coring.py:4088`).
3. Optionally delete `ignore` fields from the digest input (`coring.py:4091-4093`) — supports fields excluded from the SAID.
4. Digest the serialization; inject the result back into `sad[label]` (`saidify`, `coring.py:4052-4055`).
- **Verification** (`Saider.verify`, `coring.py:4117-4160`): re-derives with dummy fill using `self.code`, compares `qb64b`; if `prefixed`, ALSO checks the label field literally equals `.qb64` (`coring.py:4154`); if `versioned`, checks the `v` field matches the derived size (`coring.py:4150-4152`). Any exception → `return False` (fail-closed, `coring.py:4157-4158`).
- Doctrine: the SAID is a **tamper-evident commitment to exact serialized content at exact size**. Change any non-ignored byte and verification fails. This is the ACDC/KEL integrity primitive — no external hash registry needed.

### KEL = the append-only, self-verifying key-event log
- Inception (`icp`/`dip`) establishes state; the AID's authority derives ONLY from its own KEL. `Kever.incept` (`core/eventing.py:2323`) sets `verfers`, `tholder` (signing threshold), `ndigers` (next-key digests), witnesses, from the event body itself.

---

## 2. Security & threat-model positions (the load-bearing doctrine)

### Local (protected) vs. remote (unprotected) — the zero-trust firewall
The single richest doctrinal block is `Kever.valSigsWigsDel` / `validateDelegation` docstrings (`core/eventing.py:3040-3135`):
- Every event is processed as **local (protected)** or **remote (unprotected)** (`eventing.py:2015-2016, 3042-3049`). "A local event may assume that the event only came via a protected transmission path... via some protected channel using some form of MFA. A remote event is received in an unprotected manner." (`eventing.py:3043-3047`).
- Purpose: "to allow increased security on local events where a threshold structure is imposed" (`eventing.py:3048-3049`).
- **Witness pool AS a threshold/MFA structure**: "each witness only accepts local events... making the controller's signature(s) the first factor and the set of unique witness factors a secondary threshold factor. An attacker therefore has to compromise not merely the controller's private key(s) but also the unique second factor on each of a threshold satisfycing number of witnesses." (`eventing.py:3051-3057`). Delegator adds a third factor (`eventing.py:3059-3068`).
- **Concrete enforcement of the firewall** (`eventing.py:2780-2791`): when source is remote and the Kever's pre is a locally-membered group, signatures from locally-contributed indices are STRIPPED before threshold counting — "So that attacker can't source remotely compromised but locally membered signatures to satisfy threshold." Emits `remoteMemberedSig` cue.
- **Never-do rule**: "The delegator MUST NOT accept a delegable event unless it is locally sourced, fully signed by its controller, and fully witnessed by its controller's designated witness pool." (`eventing.py:3087-3089`).
- Validator (3rd party, not controller/witness/delegator) has NO protected relationship, so "The logic should be the same for both local and remote event because the validator is not one of the protected parties" (`eventing.py:3133-3135`). Validator must wait for full signing + full witnessing + anchored delegation seal (`eventing.py:3128-3132`).

### Survivability / recovery-not-prevention — superseding recovery
`Kever` superseding docstring (`core/eventing.py:3137-3207`):
- "Supersede means that after an event has already been accepted as first seen into a KEL that a different event with the same sequence number is accepted that supersedes the pre-existing event... This enables the **recovery of events signed by compromised keys**." (`eventing.py:3139-3142`).
- Result: "the KEL is **forked** at the sn of the superseding event. All events in the superseded branch of the fork still exist but, by virtue of being superseded, are **disputed**." (`eventing.py:3143-3145`). The superseding fork is "the authoritative branch." Superseded events are NOT deleted — "still remain in the KEL and may be viewed in order of their original acceptance" (`eventing.py:3148-3150`). This is **duplicity-evident by construction**: the fork is preserved and visible.
- `fn` (first-seen ordinal) ≠ `sn`: "Each event accepted into a KEL has a unique fn but multiple events due to recovery forks may share the same sn." (`eventing.py:3153-3155`).
- Superseding rules (`eventing.py:3158-3207`): A0 rotation may supersede an interaction at same sn; A1 non-delegated rotation may NOT supersede another rotation at same sn; A2 interaction may never supersede anything. B rules govern delegated-rotation superseding via delegator's KEL ordering (B1/B2/B3), recursively climbing (C) to the non-delegated root; if unsatisfied the superseding rotation is discarded (`eventing.py:3195-3206`).

### Detection-not-prevention for delegation compromise
- "A malicious attacker that compromises the pre-rotated keys of the delegatee may issue a rotation that changes its witness pool in order to bypass the local security logic" — mitigation is a delegator time-window so the delegate can DETECT: "give the delegate enough time to detect a comprimised or duplicitious superseding rotation" (`eventing.py:3099-3104, 3225-3238`). The design assumes compromise WILL happen and optimizes for detectability, not for making compromise impossible.

### TOAD = Threshold Of Accountable Duplicity
- `toader (Number): instance of TOAD (threshold of accountable duplicity)` (`core/eventing.py:1945`). The witness threshold is literally named for duplicity accountability, not for consensus/finality. Witnesses provide accountability, not global ordering.

### Pre-rotation firewall — the strongest cryptographic guarantee, and exactly how it is checked
Pre-rotation: inception commits to **digests of the next keys** (`ndigers`), not the keys themselves; the signing keys are exposed only at rotation. Enforcement:
- Non-transferable AIDs MUST have empty next: `if not self.prefixer.transferable and ndigs:` → ValidationError "Invalid inception next digest list not empty for non-transferable prefix" (`eventing.py:2352-2355`). Non-trans also forbids witnesses (`:2362`) and anchored data (`:2383`) at inception.
- Rotation forbidden if no prior next: `if not self.ndigers: raise ValidationError("Attempted rotation for nontransferable prefix...")` (`eventing.py:2650-2653`).
- The firewall check itself: `Kever.exposeds` (`eventing.py:2940-2984`) — for each signature, take the prior next digest at `siger.ondex`, recompute `Diger(ser=siger.verfer.qb64b, code=diger.code).qb64` and require it equal the committed digest (`eventing.py:2980-2982`). Only matching ondices are returned.
- Threshold on the exposed prior-next: `if not self.ntholder.satisfy(indices=ondices):` → escrow + `MissingSignatureError` "Failure satisfying prior nsith" (`eventing.py:2853-2863`). So a rotation is valid ONLY if the newly-exposed keys hash to the previously-committed next digests AND satisfy the prior NEXT threshold. An attacker holding only current signing keys cannot rotate — they do not know the pre-images. Digest-agility is per-digest: "all digests in .digers may use a different algorithm" (`eventing.py:2954-2956`).
- Prior-event chaining: non-recovery event must match prior said `if not self.serder.compare(said=prior)` → "Mismatch event dig" (`eventing.py:2644-2647`); recovery events verify against fetched prior event (`eventing.py:2623-2641`).

### Fail-closed threshold semantics
- "must have a least one verified sig" else ValidationError "No verified signatures" (`eventing.py:2799-2801`).
- Witness toad bounds enforced: out-of-bounds toad rejected; under-threshold witnessing escrows as `MissingWitnessSignatureError` and cues a receipt query (`eventing.py:2869-2896`).

---

## 3. Invariants and "never do X" rules (machine-enforced)

- Non-transferable prefix ⇒ empty next-digest list, empty witness list, empty anchored data at inception (`eventing.py:2352, 2362, 2383`).
- Inception sn MUST be 0: `if self.sner.positive: raise ValidationError(f"Nonzero sn... in inception event")` (`eventing.py:2335-2336`).
- Signing threshold size ≤ number of keys: `if len(self.verfers) < self.tholder.size` → "Invalid sith" (`eventing.py:2340`); rotation likewise (`eventing.py:2657`).
- Witness sets: no duplicates; cuts must be a subset of current wits; cuts∩adds and wits∩adds must be empty (`eventing.py:2696-2726`). Ordered-set math preserves witness index stability for indexed receipts (`eventing.py:2661-2665`).
- NoBackers registry trait: `if TraitDex.NoBackers in cnfg and len(baks) > 0: raise ValueError("...backers specified for NB vcp, 0 allowed")` (`vdr/eventing.py:89-90`).
- SAID dummy char must not be valid Base64 (`coring.py:3949`); Saider must be a digestive code else ValueError (`coring.py:3980-3994`).

---

## 4. ANTI-PATTERNS / outsider-tells the code contradicts

- **"Revocation = deletion/blocklist" (X.509 CRL / OCSP mindset) is WRONG.** The verifier explicitly SAVES a revoked credential: on revoked state it logs and *continues* rather than raising — "Log this and continue instead of the previous exception so we save a revoked credential" (`vdr/verifying.py:129-132`). Revocation is a TEL state transition (`Ilks.rev`/`brv`), not a delete. State is queried from the TEL (`vcState`, `verifying.py:117`), not from a central revocation list.
- **"A CA/registry vouches for the identifier"** — contradicted: authority is self-certifying via the KEL; there is no issuer authority external to the AID's own key state.
- **"Consensus / global ordering / one true log"** — contradicted: recovery FORKS the KEL and keeps disputed branches (`eventing.py:3143-3149`); ordering is per-AID `sn`+`fn`, and validity is observer-relative (local vs remote, `eventing.py:3040-3135`). TOAD is "accountable duplicity" (`eventing.py:1945`), not Byzantine finality.
- **"Witness = blockchain validator / consensus node"** — contradicted: witnesses are a per-controller threshold/second-factor structure (`eventing.py:3051-3057`); a registry may even have zero backers (`vdr/eventing.py:89`).
- **"Verification is globally objective"** — contradicted: the same event yields different acceptance depending on whether the observer is controller/witness/delegator/validator and whether the source is local or remote (`eventing.py:3040-3135, 2780-2791`). Validity is observer-dependent.
- **"Peer disclosure messages get logged like credentials / like a VC exchange endpoint"** — IPEX is a strict state machine (below); out-of-order or duplicate-response messages are rejected, not merged.

---

## 5. Terminology — precise, as the code uses it

- **AID**: autonomic identifier = `Prefixer` (`coring.py:3807`). Transferable (rotatable, digest or trans key code) vs non-transferable (`B`/`1AAC`… codes).
- **SAID**: `Saider` (`coring.py:3922`) — content-addressing self-reference via dummy-fill digest.
- **KEL**: key event log (`db.kels`, `Kever` maintains state). **KERL** = fully-witnessed receipted KEL (receipt couples/quadruples, `eventing.py:124-273`).
- **TEL**: transaction event log for a registry; managed by `Tevery`/`Tever`; VC state via `tever.vcState(vcid)` (`verifying.py:117, 374-376`). Events: `vcp` (registry inception), `iss`/`rev` (backerless issue/revoke), `bis`/`brv` (backer issue/revoke) (`vdr/eventing.py:84, 253, 295, 325, 378`).
- **Witness / backer**: non-transferable AIDs that receipt events; witnesses for KELs, backers for TEL registries. TOAD = threshold of accountable duplicity (`eventing.py:1945`).
- **Prefixer/Verfer/Diger/Siger/Cigar**: CESR primitive wrappers. `Siger` has DUAL index (`.index` into current keys, `.ondex` into prior-next digests) — the mechanism enabling pre-rotation exposure (`eventing.py:2942-2984`).
- **Tholder**: threshold object; `.satisfy(indices)` decides fractional/weighted/multi-clause thresholds (`eventing.py:2854`).
- **exn**: peer-to-peer exchange message (`Exchanger`, `peer/exchanging.py:28`); carries **pathed CESR attachments** (`ptds`, SAD-path attachments, `exchanging.py:77`).
- **IPEX**: Issuance and Presentation EXchange protocol over exn.

---

## 6. ACDC edge operators — GROUND TRUTH vs. prose gloss (`vdr/verifying.py:336-380`) — **SUPERSEDED 2026-09-15, see §6c**

**Status as of 2026-09-15.** This section describes `Verifier.verifyChain` as it stood at `3a8e01ae`. At `b8f60166b` the method was rewritten: the operator table grew from three to five, list-valued `o` is resolved, a new `E1E` operator is enforced, DI2I now raises `ValidationError` rather than `NotImplementedError`, and the edge `s` field is enforced. The bullets below are kept as the record of what was true at `3a8e01ae` and what the corpus believed; **§6c is the current record**. Individual bullets that are now false are struck inline.

`Verifier.verifyChain(nodeSaid, op, issuer)` is what ACTUALLY enforces edge semantics:
- ~~Only three operators recognized: `['I2I', 'DI2I', 'NI2I']` (`verifying.py:354`).~~ **Superseded 2026-09-15**: five are recognized at `b8f60166b`, and the default-inference test now reads `.iseaid` rather than `attrib['i']`. See §6c.
- **I2I** is enforced as **plain AID string equality** — *still true at `b8f60166b`*, with the far side resolved through `.iseaid` instead of `attrib['i']`. At `3a8e01ae`: `if op == 'I2I' and issuer != creder.attrib['i']: return None` (`verifying.py:365-366`). Semantics: the issuer of THIS credential must equal the issuee of the node credential it points to. That is the entirety of the I2I check — an equality of qb64 AID strings. No chain-of-authority reasoning beyond it.
- ~~**DI2I is NOT IMPLEMENTED**: `if op == "DI2I": raise NotImplementedError()` (`verifying.py:368-369`)~~ — **partly superseded 2026-09-15**. DI2I is *still* unimplemented at `b8f60166b`, so the doctrinal point survives, but the mechanism changed: it now raises `ValidationError`, deliberately, rather than crashing with `NotImplementedError`. See §6c.
- **NI2I** ("not-issuer-to-issuee") skips the issuer/issuee binding entirely (the `if op != 'NI2I':` guard, `verifying.py:357`) — it only requires the node credential exists and is in issued state. It is a non-authority reference.
- For I2I/DI2I the node MUST have a subject: `if 'i' not in creder.attrib: return None` (`verifying.py:358-359`), and its subject must be indexed (`subjs`, `verifying.py:361-363`).
- Node must be in a known registry (`creder.regid not in self.tevers → None`, `verifying.py:371`) and its TEL state non-None (`verifying.py:376-378`).
- **Chain revocation propagates**: if node state is `Ilks.rev`/`brv`, `RevokedChainError` (`verifying.py:178-180`). A revoked node invalidates the chain — but note the ROOT credential itself is still saved even when revoked (§4).
- Edge block housekeeping: labels `d` (SAID) and `o` (operator of the block) are skipped; each other label is an edge with `node["n"]` = target SAID and optional `node["o"]` operator (`verifying.py:158-164`).

## 6b. Credential processing pipeline (`vdr/verifying.py:94-186`)
Order of enforcement in `processCredential`: (1) registry known? else escrow MRE + telquery cue (`:112-115`); (2) VC state exists? else escrow (`:117-121`); (3) freshness vs `CredentialExpiry` (`:123-128`); (4) revoked → log+continue (`:129-132`); (5) **schema validation** — resolve schema, `Schemer.verify(creder.raw)`, else `FailedSchemaValidationError` (`:134-148`); (6) walk edges via `verifyChain` (`:158-184`); (7) save + `saved` cue (`:185-186`). Escrows: MRE (missing registry), MCE (missing chain), MSE (missing schema) — each re-driven by `processEscrows` with per-type timeouts and staleness eviction (`:251-300`).

---

## 6c. Edge operators at `b8f60166b` — the operator table grew, and part of it is now enforced

This is the section that moves doctrine. All quotes are from `src/keri/vdr/verifying.py` at `b8f60166b` unless otherwise marked.

**Five unary operators, not three.** `UnaryOps = ('I2I', 'NI2I', 'DI2I', 'E1E', 'NOT')` (`Verifier.UnaryOps`, L41). The class comment above it is explicit about why the unimplemented ones are listed rather than omitted: "DI2I and NOT are recognized but unimplemented: they are listed so they fail closed diagnosably instead of being dropped and silently defaulting." (L38-39). `E1E` carries its own provenance caveat: "E1E is a keripy extension not yet in the spec's normative operator table." (L40). Treat `E1E` as `[K]`-only — it is implementation-led, and this note has not verified it against any spec text.

**A second, narrower table.** `DelegativeOps = ('I2I', 'NI2I', 'DI2I')` (`Verifier.DelegativeOps`, L47), described as operators that "constrain the near ACDC's issuer relative to the far node's issuee, so they are mutually exclusive" (L44-45).

**`o` may now be a list, and conflict resolution is latest-wins within the delegative subset only.** `op = next((cand for cand in reversed(ops) if cand in self.DelegativeOps), None)` (`Verifier.verifyChain`, L433), preceded by a comment citing the spec: latest-wins applies only "among the conflicting Operators" (ACDC spec-body.md L1186) (L425) — a citation the code makes, which this note has NOT independently checked against the ACDC spec at any commit. Unrecognized tokens are dropped: `ops = [cand for cand in ops if cand in self.UnaryOps]` (L432).

**Default inference changed.** `op = 'I2I' if creder.iseaid is not None else 'NI2I'` (L440), applied only when the list is "absent, empty, or nothing recognized" (L435). The predicate moved from `'i' in creder.attrib` to `.iseaid`, which resolves an aggregate (`acg`) far node's issuee at `.sad["A"][1]["i"]` as well as an attributive one's at `.sad["a"]["i"]` (`core/serdering.py` `.iseaid`, L2824-2841 @`b8f60166b`). So the silent-default behavior the corpus flagged at §9 persists, but it now sees aggregate credentials too.

**DI2I and NOT fail closed, diagnosably.** `if 'NOT' in ops:` → `ValidationError` (L446-448); `if op == 'DI2I':` → `ValidationError` carrying "DI2I validation is not implemented" (L450-452). The choice of exception is deliberate and is the load-bearing part: "escrowing would promise a retry that can never succeed." (L445). A reviewer must not "simplify" either branch into a `MissingChainError` or into silent skipping.

**`E1E` IS enforced.** "the issuee AID of the near ACDC (the one carrying this edge) MUST equal the issuee AID of the far node." (L455-456), implemented at L461-463: `farIssuee = creder.iseaid` then `if farIssuee is None or issuee is None or issuee != farIssuee: return None`. The comment draws the distinction that matters: "Unlike the delegative I2I, this says nothing about the issuer, so the common SEDI case -- both credentials issued by a third party to the same subject" (L457-459) is valid, and is exactly what I2I rejects. `E1E` composes (AND) with the delegative winner rather than overriding it — "E1E constrains the near issuee instead, so it does not conflict with them and composes (AND)" (L428-429).

**I2I is still string equality.** `if op == 'I2I' and issuer != farIssuee:` → `return None` (L478-479). Nothing multi-hop; the doctrine survives unchanged.

**New: the edge `s` field is enforced, and its semantics are "satisfy", not "equal".** In `processCredential` (not `verifyChain`), an edge's declared far-node schema is checked: "the edge 's' is a schema the far node must *satisfy*" (L194-195, citing S. Smith, keripy issue #1534). A direct SAID match short-circuits; otherwise the far node is validated against the edge's schema and a failure raises `MissingChainError` (L219-227). A schema not yet cached escrows and cues a query rather than failing (L211-218) — transient vs. permanent is distinguished here.

**New: an ACDC's `e` section may be a list of edge blocks.** `if isinstance(prov, list): edges = prov` / `elif isinstance(prov, dict): edges = [prov]` / else `ValidationError` (L163-169).

**Doctrinal bottom line.** "Edge operators are read but unused" is **no longer accurate** as a blanket statement at `b8f60166b`, and the corpus's shibboleth table (`keri-doctrine.md` L98, L107, L132) needs resyncing. The accurate replacement: of five recognized unary operators, **I2I and E1E are enforced, NI2I is by construction a no-op binding check, and DI2I and NOT are recognized-but-unimplemented and fail closed with `ValidationError`**; the edge `s` constraint is now enforced; and the operator is still silently inferred when `o` is absent.

---

## 7. IPEX — the presentation/issuance state machine (`vc/protocoling.py`)

**Re-verified at `b8f60166b`, and the claims below still hold — with one scoping correction.** Every claim in this section was re-read against `src/keri/vc/protocoling.py` at `b8f60166b` and is still true; line hints shift by a few (`IpexHandler.verify` now spans L55-106, `PreviousRoutes` L16-22, `response` L108-121, `loadHandlers` L478-483). The correction is that **this is now one of two IPEX implementations in the tree**. `vc/protocoling.py` is the V1 handler and is the one keripy's own CLI wires up (`src/keri/cli/commands/ipex/list.py` L25: `from ....vc import loadHandlers, Ipex` @`b8f60166b`). The V2 handler is the new `acdc/ipexing.py`, covered in §7b. Where the two disagree, this section describes V1 only.

- Verbs: `Ipexage(apply, offer, agree, grant, admit, spurn)` (`protocoling.py:15-16`).
- **Legal predecessor table (invariant)** `PreviousRoutes` (`protocoling.py:17-23`):
  - `offer` ← `apply`; `agree` ← `offer`; `grant` ← `agree`; `admit` ← `grant`; `spurn` ← any of `apply/offer/agree/grant`.
- `IpexHandler.verify` (`protocoling.py:60-113`) enforces the machine:
  - `apply` may ONLY start an exchange (must have empty prior `p`) (`:76-78`).
  - `offer`/`grant` may start (no prior) OR must reference a prior whose verb is in `PreviousRoutes[verb]` (`:79-95`).
  - `admit`/`agree`/`spurn` may NEVER start an exchange (`if not dig: return False`) (`:96-98`).
  - Prior message must exist (`cloneMessage` else `return False`, `:83-85, 100-102`).
  - **No double-response**: `return self.response(pserder) is None` — reject if a response to that prior already exists (`:94, 111`); response lookup via `db.erpy` (`:124-127`).
  - Unmatched route ⇒ `return False` (fail-closed, `:113`).
- Handlers registered per route on the `Exchanger` (`protocoling.py:514-519`). exn messages themselves are signed & threshold-verified in `Exchanger.processEvent` before behavior verification (`peer/exchanging.py:92-170`); failure escrows as partially-signed (`escrowPSEvent`, `exchanging.py:195`).

---

## 7b. IPEX V2 — `acdc/ipexing.py` at `b8f60166b`

The file roughly tripled between `4df8e4a8` and `b8f60166b` (+1118 lines). All quotes are from `src/keri/acdc/ipexing.py` at `b8f60166b`.

**Scoping caveat that bounds every claim in this section.** `acdc.ipexing.loadHandlers` has **no caller anywhere in `src/keri` at `b8f60166b`**. The module is exported (`src/keri/acdc/__init__.py` L12) and exercised by tests, but keripy's own CLI still loads the V1 handler from `vc/protocoling.py`. So these are `[K]` claims about *code that exists and is tested in the reference implementation*, not about behavior any shipped keripy command performs. Do not upgrade them past that.

**The predecessor table changed.** `Ipex.grant: (Ipex.apply, Ipex.agree),` (L34) — a grant may now reply directly to an `apply`, skipping `offer`/`agree`. V1 still has `Ipex.grant: (Ipex.agree,)` (`vc/protocoling.py` L19 @`b8f60166b`). The rest of the table is unchanged. `spurn` gains one restriction: a spurn of a thread-opening grant is rejected — `if verb == Ipex.spurn and pverb == Ipex.grant and pserder.ked.get("p", ""):` → `return None` (L608-609).

**Role symmetry is now checked, not just verb order.** "Replies must target the prior sender and come from the prior receiver" (L611), implemented as three equality tests on `ri`/`i` plus a fourth on the exchange id `x` (L612-619). The single-response rule survives: `if self.response(pserder) is not None: return None` (L622-623), still via `db.erpy`.

**Verification is staged, and the stages are numbered in the source.** `IpexHandler.verify` (L368-550) runs six labelled stages: shape (L406), disclose-paths (L414), reply-chain resolution (L449), anchoring negotiation (L474), graph disclosure (L532), and per-node issuer-auth proof (L545). Every failure path is `return False` — fail-closed, matching V1.

**Anchoring (`ax`) is a negotiated bit that a reply may not silently change.** "Binding replies must exactly preserve the negotiated state." (L484) — for `agree`/`grant`/`admit`, `if messageRequiresAnchor != priorRequiresAnchor: return False` (L485-486). An offer is allowed to turn anchoring on but not off: "An offer may initiate anchoring, but may not drop it." (L487-490). This is an invariant a reviewer must not relax into a one-sided check.

**When anchoring is required, the sender's KEL is checked for a real seal.** The message's source-seal couple must name an event at or after the sender's last establishment event (`if number.sn < lastEst.s:` with the source's own typo comment "# Reject if reference is older thant the current key state", L504), must match that event's SAID when at the same `sn` (L508-509), must be an `ixn` when beyond it (`if number.sn > lastEst.s and event.ilk != Ilks.ixn:`, L525-526), and that event must actually seal this exn: `seal.get("d") == serder.said` over `event.seals` (L527-530). Missing KEL evidence raises `MissingSenderKeyStateError` (L500, L514, L521) rather than returning False — retryable, not a rejection.

**A grant discloses one closed DAG; an offer may disclose a reachable subgraph.** "grant must disclose one fully closed reachable DAG rooted at the message's `a.o[0]`." (L533-534). `_walkGraph(origin, nests, closed=)` (L627) is a BFS from the origin. With `closed=True` a dangling edge target aborts the walk (`if edgeSaid not in nodes: if closed: return None`, L699-701); with `closed=False` it is skipped. Either way orphan nests are rejected: "every carried nest must still be part of the root-reachable disclosed graph." (L714-715), enforced by `if len(seen) != len(nodes): return None` (L716-717).

**One nest per node, and only ACDC nodes.** `_validNodeNest` (L552) requires each nest to verify, to be an ACDC of a disclosed-node ilk (`if nserder.proto != Protocols.acdc or nserder.ilk not in DisclosedNodeIlks: return None`, L571-572, where `DisclosedNodeIlks = (None, Ilks.acm, Ilks.ace, Ilks.act, Ilks.acg)` at L39), and to be unique: "Each disclosed DAG node must occupy exactly one nest so the node body cannot appear twice with conflicting attachment groups." (L575-576). This last is an anti-substitution guard — do not simplify it away.

**Graph semantics are evaluated over the walked DAG — this is `verifyGraphSemantics`.** `_verifyGraphSemantics(nodes, order)` (L905) walks every disclosed node's `e` section and reduces an edge tree to one boolean; `if matched is not True: return False` (L952-953). The tri-state return convention is the design: a leaf returns `True`/`False` for satisfied/unsatisfied and `None` for malformed, and malformed always fails closed.

- Leaf operators use the same five-name table as the verifier: `UnaryEdgeOps = ("I2I", "NI2I", "DI2I", "E1E", "NOT")` (L43), `DelegativeEdgeOps = ("I2I", "NI2I", "DI2I")` (L44).
- An absent `o` is legal and unconstrained; an unrecognized `o` is malformed, not defaulted: `elif op not in UnaryEdgeOps: return None` (L765-766). Note this differs from `vdr/verifying.py`, which *drops* unrecognized tokens (L432) — the two modules disagree on strictness. Recorded as an open tension in §10.
- DI2I and NOT here fail as *unsatisfied*, not malformed: `if recognizedOp == "NOT" or dop == "DI2I": return False` (L776-777). Different mechanism from `vdr/verifying.py`'s `ValidationError`, same outcome: unimplemented means unsatisfiable.
- I2I: `elif dop == "I2I" and nserder.israid != fserder.iseaid:` → unmatched (L793-794). Still string equality, now near-issuer against far-issuee resolved via `.iseaid`.
- E1E: `if recognizedOp == "E1E":` requires both `.iseaid` present and equal (L782-786).
- **M-ary group operators are implemented.** `EdgeGroupOps = ("AND", "OR")` (L45), defaulting to AND (`groupOp = group.get("o", "AND")`, L870) and reduced at L903: `return any(results) if groupOp == "OR" else all(results)`. An empty group is malformed (`if not results: return None`, L899-900). This is genuinely new machine behavior for m-ary edge operators.
- **Edge schema pins inherit down groups.** A group's `s` becomes the default for every child (L875); a leaf's own `s` overrides it (L798). An inline schema map must be self-consistent: `if edgeSchemer.said != declared: return None` (L811-812).
- Label sets are closed and checked: `EdgeSectionLabels = ("d", "u", "o", "w")`, `EdgeGroupLabels = ("d", "u", "s", "o", "w")`, `EdgeNodeLabels = ("d", "u", "n", "s", "o", "w")` (L40-42); an unknown label in a leaf is malformed (L744-746).

**Per-node issuer-auth proof.** `_verifyIssuerAuthNode` (L982) fires only for registry-backed nodes (`regk = serder.sad.get("rd")`, L1025). Its model of a disclosed node is stated as an equation: "one disclosed DAG node is: ``ACDC body + that node's issuer-auth attachment group``" (L989-991). Exactly one blinded state is allowed — "The proof group must disclose exactly one blinded state for the registry's root event." (L1043), `if len(proofs) != 1: return False` (L1044-1045). The trust assumption is written down: "IPEX verification assumes the disclosee has already learned the foreign TEL chain" (L1047-1048), and with no injected `Regery` the node simply fails (`if self.rgy is None: return False`, L1051-1052). Verification itself delegates to `regeventing.vet(...)` (L1067-1071) — **cross-reference: `acdc/regeventing.py` is `raw/16`'s territory; the split of retryable vs. permanent failure there (`MissingAnchorError` → `MissingChainError` retry, L1074-1075; eight named refusals → permanent `False`, L1078-1081) is recorded here only because IPEX depends on it.**

**Evidence policy per verb.** `verifyEvidence` (L1085): "Grant evidence is optional, so retain the valid subset despite invalid extras." (L1099-1100) — a grant returns whatever verified; every other verb rejects any non-sender evidence at all (`if tsgs or cigars or sourceSeals or invalid: return None`, L1103-1104).

---

## 7c. `dp` — disclosure paths as landed in code, and the sharp limit on what "landed" means

This is the month's headline tier movement, and the honest answer is **partial**: the `dp` field exists on the wire and its *shape* is validated, but nothing in keripy at `b8f60166b` checks that a grant's disclosed DAG actually satisfies the `dp` plan that was negotiated, and the `Compactor` machinery that could produce a targeted disclosure has no production caller.

**What IS implemented — wire shape and syntax.** `dp` lives in the exn query/modifier section `q`, and is required on `apply` and `offer`: `if ("dp" not in q or not _validSingleDagList(q["dp"], list) or not _validDisclosurePath(q["dp"][0])): return False` (`acdc/ipexing.py` `IpexHandler.verify` L420-423 @`b8f60166b`). The outer list is a single-DAG container that is explicitly future-proofing: "We currently only support one DAG (until Multi DAG), so exactly one entry is required." (L223). An offer that opens a thread must carry a non-empty plan (L424-425).

**The path grammar.** `_validDisclosurePath` (L233) requires each entry to be a triple: "disclosure-path triples of ``[schema SAID, DAG path, ACDC paths]`` for one DAG" (L240-241). The DAG path is either the root `"/"` or a prefix that "terminates at the far-node hop ``\"_/\"`` such as ``\"/e/holder/_/\"``" (L243-244), enforced by `if segments[-1] != "_": return False` (L269-270) plus a start/end-slash check (L263-264). The third element is a list of non-empty field-path strings (L272-275). The generator side raises rather than returning False: `raise ValueError("modifiers['dp'] is required and must carry one disclose-path list per DAG")` (`apply`, L1184; similarly `offer`, L1288).

**What is NOT implemented, at `b8f60166b`, and these are the findings that matter.**

1. **No verb checks a disclosed DAG against a `dp` plan.** `dp` is validated only for `apply` and `offer` (L419). `grant` — the verb that actually discloses — never reads `dp`; its stage-5 check is `_walkGraph(..., closed=True)` plus `_verifyGraphSemantics`, both of which are about the DAG's internal shape and edge semantics, not about whether it matches what was asked for. So the disclosure plan is **negotiated but not enforced**. A grant disclosing more or less than the agreed paths is accepted by this code.
2. **`Compactor` targeted disclosure has no production caller.** `Compactor.compact(paths=None, root=None)` (`core/mapping.py` L1114 @`b8f60166b`) is the machinery for producing a partial: "ACDC-relative SAD paths whose combined closure remains expanded in one saved partial. A trailing path separator keeps the whole node expanded." (L1129-1131), with numeric components selecting "mapping fields by ordinal" (L1132-1133). The only calls to `.compact()` in `src/keri` are two bare, argument-less calls in `core/serdering.py` (L3058, L3112 — `sector.compact()  # only compact do not expand`). The `paths=` form appears nowhere in `src/`; the only file in the repo that exercises it is `tests/core/test_mapping.py`. So the disclosure-path→partial-ACDC bridge is library capability, not a wired pipeline.
3. **The `dp` path syntax and the `Compactor` path syntax are not obviously the same language, and nothing in the tree reconciles them.** `_validDisclosurePath` speaks of `/e/holder/_/` hops across a DAG; `Compactor.compact` takes SAD paths resolved by `Pather(path=path, relative=True).rparts` within one mapping (L1156). No code at `b8f60166b` translates one into the other. Recorded as an open question in §10.

**Compactor invariants worth not simplifying away.** A targeted disclosure cannot be taken from an already-compacted mapping — `raise InvalidValueError("Cannot disclose from compact mapping")` (L1146) — and the call is destructive: "A targeted call consumes the expanded mapping. Use a new Compactor instance to create another targeted partial." (L1125-1126). Whole-node disclosure preserves descendants: "Preserve every nested mapping for whole-node disclosure." (L1192). Restoration order is load-bearing: "Restore marked ancestors before descendants from canonical leaves." (L1224), implemented by sorting the marked paths by length (L1226).

---

## 7d. EXN evidence and the durable exchange stores (`peer/exchanging.py`, `db/basing.py`)

All quotes at `b8f60166b`.

**A route now opts into an evidence policy, and the absence of one is itself a policy.** `Exchanger.processEvent` looks up `evidenceVerifier = getattr(behavior, "verifyEvidence", None)` (`peer/exchanging.py` L155). Routes without one keep the old precedence: "Routes without an evidence policy preserve the existing TSG-over-cigar precedence. A sender TSG causes all cigars to be ignored." (L157-159), and they reject foreign evidence outright rather than ignoring it (L235-241, L256-262). Routes with one receive only the *validated* foreign subset and get to accept or refuse it (L308-314); refusing returns `False` and the message is not persisted (L315-319).

**Sender authentication now has two independent satisfiers.** A valid source seal is sufficient on its own: "A valid sender seal authenticates the EXN. Retain only valid optional sender TSGs and do not fail on invalid ones." (L184-186). This is a deliberate asymmetry — once a seal authenticates, a bad optional TSG is tolerated rather than fatal. Do not "simplify" it into a conjunction.

**Missing sender-KEL evidence escrows only for handlers that opted in.** "IPEX uses sender seals as required workflow evidence, so retain the complete message until the referenced sender KEL arrives." (L174-175), gated on `if getattr(behavior, "acceptsSscs", False):` (L176). `IpexHandler.acceptsSscs = True` (`acdc/ipexing.py` L348).

**Foreign key-state is frozen before escrow, not re-resolved after.** "Freeze foreign last-establishment references before sender escrow can return, so replay retains the evidence and its original keys." (L125-126). The reason is replay correctness: an escrowed message replayed later must be judged against the keys that were current when it arrived, not the keys current at replay.

**"Rejects what it preserves" — the precise version.** The handler distinguishes three outcomes, and only one of them is a rejection with preservation. A `MissingChainError` from behavior verification escrows the message and cues a proof fetch, returning `None`: "Registry-backed IPEX grants may arrive before the disclosee has fetched the issuer's TEL history from observers." (L340-341), escrow at L343-346. A behavior `verify` returning False returns False **before** `logEvent`, so a permanently-invalid message is *not* persisted (L335-338 precedes L352-353). Acceptance is unconditional at that point: `# Always persist events` / `self.logEvent(serder, ptds, tsgs, cigars, essrs, ...)` (L352-353). So the corpus's shorthand needs qualifying: **IPEX preserves what it defers on, and drops what it refuses.**

**Escrow replay trims before rewriting.** "The same stores hold escrowed and accepted evidence. Remove the temporary branches so processEvent writes back only the evidence that passes current verification and policy." (L460-462), executed as `esigs.trim` / `ecigs.rem` / `ests.trim` before the replayed `processEvent` (L463-468). A reviewer removing the trim would leave stale evidence permanently attached to an accepted message.

**Durable exchange stores (`db/basing.py`).** The V2 workflow added subDBs beside the existing `exns`/`erpy`/`esigs`/`ecigs`/`epath`: `.enst` "for exchange message nested child substreams." (L573-575), `.essrs` "for exchange message event source records." (L578-580), and `.ests` "for resolved exchange source seals." (L583-585) keyed by "exchange message SAID and sealing AID" (L586). `.ests` carries the invariant that names which table is authoritative: "The exchange message in ``exns`` remains the acceptance marker." (L588-589) — evidence tables may hold escrowed material, so presence in `ests` is not acceptance. The single-response forward pointer is unchanged: `self.erpy = subing.CesrSuber(db=self, subkey="erpy.", klas=coring.Saider)` (L1125).

---

## 8. CESR framing (structural doctrine, `core/counting.py`)

- CESR is genus/version-aware: `GenusCodex`/`GenDex` map protocol genera to code tables (`counting.py:24-44`); counters differ across `Vrsn_1_0`/`Vrsn_2_0` (`CounterCodex_1_0`, `counting.py:50`).
- Counter codes ARE the attachment doctrine (`counting.py:58-78`): `-A` ControllerIdxSigs, `-B` WitnessIdxSigs, `-C` NonTransReceiptCouples (pre+cig), `-D` TransReceiptIdxSigGroups (pre+snu+dig+sigs), `-E` FirstSeenReplayCouples (fnu+dts), `-F` TransIdxSigGroups, `-G` SealSourceCouples (snu+dig of delegator/issuer/tx event — the anchoring couple), `-I` SealSourceTriples (pre+snu+dig anchoring source), `-L` PathedMaterialQuadlets (SAD-path attachments), `-Z` ESSRPayloadGroup. Everything is quadlet-aligned (4-char units).
- Sizing is exact and self-describing: `Matter.Sizes[code].fs` gives full size (used for SAID dummy fill, `coring.py:4085`); the leading selector char(s) determine parse length — no delimiters, no ambiguity. Verifier fail-closed on any size/parse mismatch (SAID `versioned` check, `coring.py:4150-4152`).

---

## 9. Notes on prose-vs-machine gaps found

- **DI2I edge operator**: documented meaning exists in ACDC prose, but ~~the verifier raises `NotImplementedError` (`verifying.py:368-369`)~~ — **updated 2026-09-15**: at `b8f60166b` it raises `ValidationError` instead (`verifying.py:450-452`), and the leaf evaluator returns an unsatisfied edge (`acdc/ipexing.py:776-777`). The gap itself survives: still no machine behavior, now failing closed on purpose rather than by accident.
- **Edge `o` operator inference**: when omitted, the verifier silently defaults I2I/NI2I ~~from presence of `attrib['i']` (`verifying.py:354-355`)~~ — **updated 2026-09-15**: from `creder.iseaid is not None` (`verifying.py:440` @`b8f60166b`), which also covers aggregate ACDCs. The "explicit operator" story is still softer than prose implies.
- **Revoked-credential handling**: prose framing of revocation as invalidation is nuanced by the code choosing to SAVE revoked credentials (root) while propagating revocation only along edges (`verifying.py:129-132` vs `:178-180`).
- **I2I as "chain of authority"**: machine reality is a single AID string equality (`verifying.py:365` @`3a8e01ae`; `verifying.py:478` @`b8f60166b`), not multi-hop authority evaluation; multi-hop is left to the recursive edge walk in `processCredential`, which does not re-derive delegated authority. **Re-verified 2026-09-15 — unchanged.**
- **`CacheResolver` schema trust**: schema is fetched from a local cache/resolver (`verifying.py:70, 135`); if absent it escrows and queries — the verifier does not itself fetch trust roots from any global authority. **Re-verified 2026-09-15 — unchanged** (`verifying.py:83, 148` @`b8f60166b`), and now extended to edge-declared schemas, which escrow the same way (`verifying.py:211-218`).

---

## 10. Named negative results at `b8f60166b`

These are findings, not absences. Each was looked for deliberately and not found; each is a claim about the code at this commit, and each should be re-tested at the next pin rather than assumed to persist.

1. **No enforcement of DI2I anywhere in `src/keri`.** Two independent sites reject it rather than evaluate it: `vdr/verifying.py:450-452` (`ValidationError`) and `acdc/ipexing.py:776-777` (`return False`). A repo-wide search for `DI2I` at `b8f60166b` returns only these two sites plus the two operator tables that name it. The ACDC prose meaning of delegated-issuer-to-issuee remains unrealized in the reference implementation.

2. **No DAG acyclicity check.** `_walkGraph` (`acdc/ipexing.py:627-719`) is a BFS with a `seen` set, so a cycle among disclosed nodes terminates the walk rather than triggering a rejection — the set is a termination guard, not a validity check, and no code path reports a cycle. `vdr/verifying.py`'s edge walk does not recurse at all (`verifyChain` resolves one hop). A repo-wide search for `acyclic`/`cycle` in `src/keri` at `b8f60166b` returns only `hio` scheduler cycle-time docstrings. The corpus's standing claim that DAG acyclicity is unchecked (`keri-doctrine.md` L132) is **confirmed still true at `b8f60166b`**.

3. **No post-quantum signature codes in keripy.** A case-insensitive repo-wide search of `src/keri` at `b8f60166b` for `dilithium|falcon|ml-dsa|mldsa|slh-dsa|slhdsa|fn-dsa|fndsa|sphincs|kyber|ml-kem|post.?quantum` returns **only** hits on the `falcon` HTTP framework in `app/httping.py` and `app/indirecting.py`. `MatterCodex` in `core/coring.py` has no FN-DSA / ML-DSA / SLH-DSA entries. So the CESR v1.1 PQ code sizes that signify-ts added on 2026-09-05 have **not** landed in keripy as of `b8f60166b`. This is the answer another chapter needed; it is a point-in-time fact and cheap to re-check.

4. **`Compactor` targeted disclosure is not wired to anything.** `compact(paths=…)` has no caller in `src/` at `b8f60166b`; the only file in the repo exercising it is `tests/core/test_mapping.py`. See §7c item 2.

5. **A `dp` plan is never checked against a disclosed DAG.** `dp` is validated for `apply` and `offer` only, and only for shape. See §7c item 1.

6. **The new V2 IPEX handler is not wired into keripy's own CLI.** `acdc.ipexing.loadHandlers` has no caller in `src/keri`; the only references to the module in `src/keri` are its own docstring and the `acdc/__init__.py` re-export. See §7b.

---

## 11. Open questions and unresolved tensions

1. **Two modules disagree on how to treat an unrecognized edge operator.** `vdr/verifying.py:432` filters unrecognized tokens out of the list and then applies the default rule; `acdc/ipexing.py:765-766` treats an unrecognized `o` as malformed and fails closed. The same edge could therefore pass credential processing and fail IPEX grant verification, or vice versa. Nothing in either file acknowledges the other. Unresolved: which is intended, and whether the ACDC spec says anything about unrecognized operators.

2. **Is `E1E` anywhere but keripy?** The code itself hedges — "E1E is a keripy extension not yet in the spec's normative operator table." (`vdr/verifying.py:40`) — and traces the idea to a discussion rather than a spec: "Identity relation (discussion #1515)" (`vdr/verifying.py:455`). This note has not read that discussion and has not checked the ACDC spec's v1.1 branch for `E1E`. If it is absent there, `E1E` is `[K]`-only and must not be cited as `[N1.1]`. Worth a `raw/03` cross-check.

3. **The latest-wins rule cites a spec line this note did not read.** `vdr/verifying.py:427-428` attributes latest-wins-among-conflicting-operators to "ACDC spec-body.md L1186". Verifying that citation belongs to `raw/03`; until then this note repeats it as the code's own claim, not as a spec fact.

4. **How does a `dp` path resolve to a `Compactor` path?** §7c item 3. The two path languages are not reconciled anywhere in the tree at `b8f60166b`, and there is no code that consumes a negotiated `dp` to produce a partial ACDC. Either a piece is still to be written, or the bridge lives outside keripy (KERIA/signify) — unchecked.

5. **Does the V2 grant's freedom to reply directly to an `apply` (`ipexing.py:34`) reflect a spec change or an implementation convenience?** The V1 table still requires `agree` first. Not settled here.

6. **Are the eight named `regeventing.vet` refusals the right permanent/retryable split?** `acdc/ipexing.py:1074-1081` hard-codes `MissingAnchorError` as retryable and eight other named errors as permanent. Whether that enumeration is complete is a question for `raw/16`, which owns `acdc/regeventing.py`.

7. **Not re-read this pass, and therefore not re-verified:** `core/eventing.py`, `core/coring.py`, `core/counting.py`, `vdr/eventing.py` (all of §1–§5 and §8 above), plus `app/habbing.py`, `core/signing.py`, `acdc/acdcing.py`, `acdc/containing.py`, `core/structing.py`. `core/signing.py` and `app/habbing.py` both changed in the window this pass covers and were not examined.
