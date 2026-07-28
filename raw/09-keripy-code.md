# KERI/ACDC/CESR Doctrine — Ground Truth from the keripy Reference Implementation

Source: `/home/daniel/code/keripy/src/keri` (Python reference verifier).
Mandate: what the code ACTUALLY enforces vs. what prose claims. Every "code does X" claim carries `file:line`.
Read-only pass; nothing modified.

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

## 6. ACDC edge operators — GROUND TRUTH vs. prose gloss (`vdr/verifying.py:336-380`)

`Verifier.verifyChain(nodeSaid, op, issuer)` is what ACTUALLY enforces edge semantics:
- Only three operators recognized: `['I2I', 'DI2I', 'NI2I']` (`verifying.py:354`). If the edge's `o` is not one of these, it is INFERRED from data: `op = 'I2I' if 'i' in creder.attrib else 'NI2I'` (`verifying.py:355`). So "issuer-to-issuee" is the default whenever the far node has a subject `i` field.
- **I2I** is enforced as **plain AID string equality**: `if op == 'I2I' and issuer != creder.attrib['i']: return None` (`verifying.py:365-366`). Semantics: the issuer of THIS credential must equal the issuee (`attrib['i']`) of the node credential it points to. That is the entirety of the I2I check — an equality of qb64 AID strings. No chain-of-authority reasoning beyond it.
- **DI2I is NOT IMPLEMENTED**: `if op == "DI2I": raise NotImplementedError()` (`verifying.py:368-369`). Any prose describing delegated-issuer-to-issuee edge behavior is a **gloss with no machine behavior** in this verifier — it will crash if exercised.
- **NI2I** ("not-issuer-to-issuee") skips the issuer/issuee binding entirely (the `if op != 'NI2I':` guard, `verifying.py:357`) — it only requires the node credential exists and is in issued state. It is a non-authority reference.
- For I2I/DI2I the node MUST have a subject: `if 'i' not in creder.attrib: return None` (`verifying.py:358-359`), and its subject must be indexed (`subjs`, `verifying.py:361-363`).
- Node must be in a known registry (`creder.regid not in self.tevers → None`, `verifying.py:371`) and its TEL state non-None (`verifying.py:376-378`).
- **Chain revocation propagates**: if node state is `Ilks.rev`/`brv`, `RevokedChainError` (`verifying.py:178-180`). A revoked node invalidates the chain — but note the ROOT credential itself is still saved even when revoked (§4).
- Edge block housekeeping: labels `d` (SAID) and `o` (operator of the block) are skipped; each other label is an edge with `node["n"]` = target SAID and optional `node["o"]` operator (`verifying.py:158-164`).

## 6b. Credential processing pipeline (`vdr/verifying.py:94-186`)
Order of enforcement in `processCredential`: (1) registry known? else escrow MRE + telquery cue (`:112-115`); (2) VC state exists? else escrow (`:117-121`); (3) freshness vs `CredentialExpiry` (`:123-128`); (4) revoked → log+continue (`:129-132`); (5) **schema validation** — resolve schema, `Schemer.verify(creder.raw)`, else `FailedSchemaValidationError` (`:134-148`); (6) walk edges via `verifyChain` (`:158-184`); (7) save + `saved` cue (`:185-186`). Escrows: MRE (missing registry), MCE (missing chain), MSE (missing schema) — each re-driven by `processEscrows` with per-type timeouts and staleness eviction (`:251-300`).

---

## 7. IPEX — the presentation/issuance state machine (`vc/protocoling.py`)

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

## 8. CESR framing (structural doctrine, `core/counting.py`)

- CESR is genus/version-aware: `GenusCodex`/`GenDex` map protocol genera to code tables (`counting.py:24-44`); counters differ across `Vrsn_1_0`/`Vrsn_2_0` (`CounterCodex_1_0`, `counting.py:50`).
- Counter codes ARE the attachment doctrine (`counting.py:58-78`): `-A` ControllerIdxSigs, `-B` WitnessIdxSigs, `-C` NonTransReceiptCouples (pre+cig), `-D` TransReceiptIdxSigGroups (pre+snu+dig+sigs), `-E` FirstSeenReplayCouples (fnu+dts), `-F` TransIdxSigGroups, `-G` SealSourceCouples (snu+dig of delegator/issuer/tx event — the anchoring couple), `-I` SealSourceTriples (pre+snu+dig anchoring source), `-L` PathedMaterialQuadlets (SAD-path attachments), `-Z` ESSRPayloadGroup. Everything is quadlet-aligned (4-char units).
- Sizing is exact and self-describing: `Matter.Sizes[code].fs` gives full size (used for SAID dummy fill, `coring.py:4085`); the leading selector char(s) determine parse length — no delimiters, no ambiguity. Verifier fail-closed on any size/parse mismatch (SAID `versioned` check, `coring.py:4150-4152`).

---

## 9. Notes on prose-vs-machine gaps found

- **DI2I edge operator**: documented meaning exists in ACDC prose, but the verifier raises `NotImplementedError` (`verifying.py:368-369`). No machine behavior — a pure gloss today.
- **Edge `o` operator inference**: when omitted, the verifier silently defaults I2I/NI2I from presence of `attrib['i']` (`verifying.py:354-355`) — the "explicit operator" story is softer than prose implies.
- **Revoked-credential handling**: prose framing of revocation as invalidation is nuanced by the code choosing to SAVE revoked credentials (root) while propagating revocation only along edges (`verifying.py:129-132` vs `:178-180`).
- **I2I as "chain of authority"**: machine reality is a single AID string equality (`verifying.py:365`), not multi-hop authority evaluation; multi-hop is left to the recursive edge walk in `processCredential`, which does not re-derive delegated authority.
- **`CacheResolver` schema trust**: schema is fetched from a local cache/resolver (`verifying.py:70, 135`); if absent it escrows and queries — the verifier does not itself fetch trust roots from any global authority.
