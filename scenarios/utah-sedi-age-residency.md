# Proving "legal Utah resident, over 18" with SEDI credentials

*Operational walkthrough, 2026-10-01. Grounded in the keripy worked-example tests and the doctrine in `bible/`. Tier-marked and pinned because one of the two tests is still on a branch, not in `upstream/main`.*

## Provenance and tiers

Two keripy tests carry this scenario, and they sit at different points on the privacy spectrum and in the repo's history:

- **`tests/acdc/test_bulk_issuance.py`** — present on `upstream/main` (synced 2026-10-01, `upstream/main` at `2caefe53`). Models *how Utah plans to issue*: ACDC-spec §15.4 bulk-issued private ACDCs. The State of Utah has indicated it intends to use bulk-issued ACDCs for SEDI (test docstring, lines 21–41).
- **`tests/acdc/test_cp_disclosure.py`** — **on branch `feat-dp-disclosure-paths` only, not yet in `upstream/main`.** It is the former CLC-disclosure test, renamed to `cp_disclosure` and rebuilt on the settled `dp` disclosure-paths / origin-tuple construct (branch commits `d011dd01`, `740ad066`, `b303471c`). Models *how the citizen presents* under Chain-Link Confidentiality. If this file is absent from a checkout, you are on `main`; check out the branch to follow §5.

Both tests deliberately model at the **data-structure level** — real v2 primitives from `keri.core` / `keri.acdc.messaging` (`Salter`, `Noncer`, `Diger`, `acdcmap`/`acdcagg`, `Aggor`, `Blinder`, `blindate`, `exchange`), validating every ACDC against a real JSON-Schema Draft 2020-12 — but they do **not** stand up a `Habery`/keystore, witnesses, or the registrar/observer infrastructure. `tests/acdc/test_ipexing.py` is the counterpart that routes through the real v2 IPEX builders (`keri.acdc.ipexing`) and a live `Habery`/`Exchanger`.

Doctrine basis in `bible/`: §3–4 of `06-governance-ecosystems-and-interop.md` (SEDI, data loyalty, correlation-resistance as a layered property), §8–10 of `05-acdc-and-verifiable-data.md` (contractually-protected disclosure, registries/TELs, the Registrar/Observer split, IPEX), §4 and §11 of `08-presentation-architectures-and-ipex.md` (the `dp` field, the two SEDI recipes), and `10-presentation-registries.md` (the pre-normative issuee-side presentation registry).

**Terminology.** The string "SMAID" appears nowhere in keripy or in this knowledge base. The "master credential a citizen uses to interact with Utah" maps onto **`sedi-id`**, the state-endorsed *core-identity* credential; the age proof is **`sedi-age`** (called `age` in `test_cp_disclosure.py`). This document uses `sedi-id`/`sedi-age` and notes where "SMAID" is the owner's framing.

## 1. The two credentials

**`sedi-id` — attributive (`acm`), the "master" credential.** Issued by the State, it carries exactly the four statutory attributes Utah Code §63A-20 permits — name, birth date, image (state-endorsed photo), and Utah residence address — and nothing more; everything richer is a *separate* credential that chains back to it. Its `a` section decomposes name and residence into **separate individually-blinded nested blocks**, each `oneOf(block-SAID, block-detail{d, u, <attr>})`. That decomposition is the whole privacy point: a single residence block would force over-disclosure on every verifier who needs only jurisdiction, so the statute's minimization duty is made *un-satisfiable to violate at the schema level* rather than merely promised. "Prove Utah resident" therefore reveals the jurisdiction block **without the street line** — which protects at-risk classes (DV victims, LEOs). (`test_cp_disclosure.py:188–246`; `bible/06` §3.)

**`sedi-age` — aggregative (`acg`), the age proof.** A homogeneous boolean vector `ageOver13/16/18/21/55/65`. Element 0 is the AGID, a commitment to every block's SAID; every threshold block is present, so revealing `over18` discloses nothing about whether the holder is over 55 or 65. This is the ISO-mDL `age_over_NN` model — "a poor man's sparse Merkle tree" — and it satisfies the statutory "prove a minimum age without disclosing age or birth date" (§63A-20-301(1)(e)) with no special cryptography, keeping the birth date out of the transaction entirely. (`test_cp_disclosure.py:248–304`.)

**How they are joined: an `E1E` identity edge, not a stored edge to the root.** `sedi-age` carries one edge, `identity`, pointing at `sedi-id`, with its operator **const-pinned by schema to `E1E`** ("issuee-to-issuee"). `E1E` asserts *same subject* — `near.iseaid == far.iseaid`, both resolved via `SerderACDC.iseaid`, which reads `a.i` for an attributive credential and `A[1].i` for an aggregative one — while saying **nothing about the issuer.** That is exactly why it holds even though the State issues `sedi-id` and the endorser issues `sedi-age` (issuer ≠ issuee in both). A delegative `I2I` ("my issuer is the far node's issuee") would wrongly reject this pairing. The subtlety with teeth: `E1E` alone is satisfied by *any* un-revoked credential naming that subject, including a self-issued bogus one, so the "chains to the core identity" guarantee also binds the far node's **schema** via an edge `s`-constraint — the verifier checks both that the edge names the core-identity schema SAID and that the far node actually is that schema. (`test_cp_disclosure.py:167–186`, `615–646`, `1404–1442`; keripy discussion #1515, PR #1523 adds the real `E1E` branch to `verifyChain`. A pre-#1527 verifier silently coerces unknown operators to `I2I`/`NI2I`; for this edge shape that coercion fails closed, so the graph validates only against a #1527+ verifier.)

**Why `sedi-age` has no stored edge the other direction.** An `I2I` edge *from* `sedi-age` *to* `sedi-id` would hold only if the holder self-issued the age attestation — which would carry no state endorsement. So `sedi-age` carries no edge to the root; the same-holder binding is established at *presentation* time instead. Doctrine: don't force an edge whose operator semantics you can't satisfy; bind at presentation. (`bible/05` §5.2.)

## 2. The three AIDs, and how the master differs from the bulk-issued credentials

This is the crux. Three distinct autonomic identifiers are in play:

- **Issuer AID — the State.** Utah's digital-government office. One stable, public identifier, shared by the whole population, so it singles out no one. In every copy of both credentials `sad['i'] == STATE`. (`test_bulk_issuance.py:476–478`, `696–697`.)
- **The "SMAID" master AID — the citizen's standing identifier.** The AID the citizen uses to *hold and manage the endorsement relationship with Utah*. SEDI's inversion lives here: the issuer field names the State, but the subject is bound by the holder's own KERI AID — withdraw the endorsement and the identity persists, because the holder, not the state, holds the key. (`bible/06` §3.)
- **The bulk-issued per-context holder AIDs — `ALICE_k`.** The key move in Utah's plan: the bulk-issued credentials are **not** issued to the standing master AID.

In `test_bulk_issuance.py` the State mints a *set* of M semantically-identical copies of each credential (`BULK_SIZE = 5` for readability; a real deployment sizes M to the expected number of distinct verifier contexts), generated on demand from one shared salt plus a template with **no per-copy storage.** Copy *k* is issued to its own fresh per-context holder AID `ALICE_k`, derived from a **holder-only secret salt the issuer never sees** — the holder supplies the public AIDs and the State commits to AIDs it cannot forge (`test_bulk_issuance.py:382–392`). Copy *k* of `sedi-id` and copy *k* of `sedi-age` share the same `ALICE_k` (same subject, one context), index-aligned across the two sets. The holder spends a *different* copy at each verifier.

So the difference, stated precisely: **the master/SMAID AID is the correlation anchor that must never reach a verifier; bulk issuance shatters the holder identity into M disposable per-context AIDs and substitutes those as the credential issuees.** There is no single standing holder AID in the bulk-issued credentials at all. This is what defeats the cross-verifier join — see §4. (Sam, keripy #1532: "we need bulk issuance because then one has a unique AID per context.")

**Note the two examples differ here.** `test_cp_disclosure.py` holds both source credentials under *one* holder AID (it is demonstrating the CLC/safe-harbor mechanism, and its own docstring, lines 12–19, names the standing-SAID correlator that bulk issuance is needed to kill). `test_bulk_issuance.py` is where the per-context `ALICE_k` partition is realized. The full Utah story **composes the two**: bulk-issued per-context credentials (§2–4) presented through a CLC bespoke presentation per verifier (§5).

## 3. Registries, pre-creation, and revocation

Each source credential is registry-bound via its top-level `rd` field, pointing at a registry whose SAID is *derived from* a `rip`/`regcept` inception event. That inception is a **vacuous placeholder that commits to no credential state and reveals nothing about what will later be issued** — that is the "pre-created registry." The registry identifier is the SAID of the event, so it is derived from the event rather than chosen, and it is independent of the bulk aggregate `B`, which avoids a circular dependency (copies bind `rd`, `B` is computed over the copy SAIDs, then the update commits `B`). (`test_bulk_issuance.py:430–451`; `bible/05` §9; ACDC spec §Registry-Dependent Issuance Lifecycle.)

**One shared blindable registry per *set*, not per copy and not per citizen.** There are two sets (`sedi-id`, `sedi-age`), so two registries. A single **blindable update (`bup`)** commits the whole set — identified by its blinded aggregate `B` — as `issued`. Revocation is a second `bup` at sn=2 chaining onto the issuance (`revoked.sad['p'] == issued.said`), flipping the set to `revoked`; it is a *set-level* operation. (`test_bulk_issuance.py:446–451`, `1103–1118`.)

**Blindable state is what makes the shared registry safe and defeats phone-home correlation.** The state word (`issued`/`revoked`) and the aggregate never appear in clear on the wire — only the blinded block's SAID travels. The blinding salt is shared **issuer↔holder only**; a verifier handed one event's blind can read *that* event's status and nothing past or future (a verifier who had the salt could read the entire state history). The spec's own boundary is the quotable part: **this is confidentiality of registry state, not anonymity of the credential — issuer, registry, and issuance chronology remain linkable, the intended, auditable trade-off.** (`test_examples.py:460–570`; ACDC spec §Registry-Dependent Issuance Lifecycle, L4981–4985.)

**What the verifier checks, and what the examples omit.** A status-checking verifier unblinds the current set state to decide honor/refuse, and walks the `I2I`/`E1E` edges to each source credential's registry TEL to reject a revoked source even when the presentation is otherwise perfect. Both tests **explicitly omit this fourth, live check** (`test_cp_disclosure.py:711–716`), because running it means `keri.vdr`'s `Tevery`/`Reger` over a `Habery` — above the data-structure altitude. In the real IPEX tooling the grant carries the machinery inline: `iss = update(regid=…, acdc=acdc.said, state="issued")` plus the KEL anchoring event `anc`, nested as `[acdc.said, iss.said, anc.said]` (`test_ipexing.py:242–246`).

**The presentation itself is deliberately *not* registry-bound.** The bespoke presentation ACDC Alice issues carries no `rd` (`assert 'rd' not in bespoke.sad`, `test_cp_disclosure.py:867`). A one-time presentation is not logged, which is what keeps the State — or anyone — from correlating where and when she presents.

## 4. How correlation is defeated — a stack, not a single trick

**Disclosure layer (cryptographic).**
- *Attributive partial disclosure*: reveal the photo and the jurisdiction block in full; withhold birth date, name, street line as **bare block SAIDs**, each carrying its own blinding nonce `u` so its low-entropy value cannot be brute-forced from the SAID. Every mix recomputes to the same committed section SAID, so the withheld values provably never cross the wire.
- *Aggregative selective disclosure*: reveal issuee + `over18`/`over21`; withhold every other threshold as a bare SAID. Because all thresholds are present, disclosing one reveals nothing about the others.
- *Bulk per-copy SAIDs + per-context AIDs*: the headline. The correlator set each verifier receives — holder AID, `sedi-id` SAID, `sedi-age` SAID, AGID, presentation SAID — is provably **disjoint** from any other verifier's: `corr1.isdisjoint(corr2)` (`test_bulk_issuance.py:853–942`). The only identifier *not* partitioned is the schema SAID, shared by all copies — which is why a disclosure request keys on schema, never on copy SAID.
- *Unlogged, non-registry-bound presentation* (§3) and withholding stable correlators until after agreement (§5).

**Governance/contractual layer — the safe-harbor trigger (§5).** For what crypto cannot reach, the duty of data loyalty binds the parties the technical layer cannot. This is the SEDI `chainLinkConfidentiality` rule, grounded in Utah Code.

**Deployment layer.** Per-context AIDs and un-logged one-time presentations.

**The honest residuals — what these examples do *not* close.** The spec is blunt that **no cryptographic mechanism precludes statistical correlation among colluding verifiers**; advanced unlinkability without contractually-protected disclosure is "an exercise in diminishing returns." Bulk issuance defeats *provable* third-party correlation via public SAIDs; the rest is **decorrelation-by-enforcement** — a partitioned identifier set makes any downstream reappearance *prima facie* evidence of a §63A-20-701 data-loyalty violation. Named residuals (`test_bulk_issuance.py:59–73`, `876–879`, `928–932`):
- The full `[b_k]` membership list disclosed for the aggregate proof is itself a byte-identical cross-verifier join key; removable only by a Merkle-*inclusion* variant.
- Even with per-context AID strings, witnessing the M holder AIDs on a **shared witness pool / mailbox** re-links them via KEL-discovery metadata (spec L2891). The witness topology for the `ALICE_k` AIDs is itself a correlation surface that must be designed, not assumed away.
- The shared registry and aggregate `B` recur across contexts as a **contract-gated 2nd-party correlator — present, not hidden.** Full 3rd-party decorrelation needs independent/herd registries (a Sparse-Merkle-Tree root), a deliberate follow-on.

## 5. The contractually-protected presentation, and electing the safe harbor

To enter the club (the worked example's "Alcove Club", Salt Lake City), Alice runs CLC **as a credential** rather than as an out-of-band agreement: she (Issuer/Discloser) issues a **bespoke presentation ACDC** to the club (Issuee/Disclosee), with two `I2I` edges back to her `sedi-id` and `sedi-age`, carrying the terms in its **Rules section** (`r`), unblinded because the terms are meant to be read. Three clauses (`test_cp_disclosure.py:389–409`):

- **Purpose** — one-time verification that the Discloser is over 21 and matches the state-endorsed photo, for the sole purpose of admittance on the stated date.
- **Assimilation** (the not-to-correlate promise) — the verifier agrees **not to "assimilate, aggregate, correlate, sell, or otherwise combine"** the disclosed data with anything else, *including information collected by independent means and anything recursively referenced through the edge section.*
- **SafeHarbor** — references a published SEDI governance-framework provision **by SAID**; states that **by accepting the terms — sending a signed IPEX `agree` referencing this container's SAID — the verifier *elects* the statutory safe harbor against liability under Utah Code §63A-20-701, conditioned on compliance with Purpose and Assimilation. Breach forfeits the safe harbor and is evidence under §63A-20-801.**

The schema *requires* all three clauses and pins the edge operator to `I2I` (rejecting `NI2I`), so a well-formed presentation cannot omit the terms. Because the terms are hashed into the ACDC's SAID and the `agree` commits to that SAID, **the terms follow the data** — weaken a clause and you get a different SAID the verifier rejects (`test_cp_disclosure.py:1258–1343`).

**The IPEX gate makes the election happen before any PII is disclosed.** The exchange is strictly ordered `apply → offer → agree → grant → admit` (a real state machine; out-of-order or duplicate responses are rejected, not merged):

| Route | By | What crosses |
|---|---|---|
| `apply` | club | the request, as a `dp` disclosure-paths list in the `q` (query) section — **no PII** |
| `offer` | Alice | commits only her fresh bespoke-presentation SAID + the governance ref — **no PII, and not even the source-credential SAIDs** |
| `agree` | club | **signed** — *this is the safe-harbor election*, binding the offer SAID |
| `grant` | Alice | the only message with PII: the state-endorsed photo, the age flag, the jurisdiction block, the membership proof |
| `admit` | club | confirms receipt |

Withholding the issuer-committed source SAIDs until *after* the signed `agree` is deliberate: attaching them earlier would let the club spurn and walk away with stable holder correlators (panel review PRV-F2). So the club **legally binds itself before it sees any endorsed attribute.** (`test_cp_disclosure.py:904–1197`.)

**The `dp` disclosure-paths request** (the branch's flagship construct; keripy #1549, ACDC `v1.1`). `dp` rides the `q` section, not `a`, because a disclosure request is a query. It is an **ordered list of `(schemaSAID, [paths])` tuples** — a list, not a dict keyed by schema SAID, so that two credentials of the *same* schema (common: one's own identity alongside a spouse's) stay distinct. The **zeroth tuple is the DAG's origin node** — Alice's bespoke presentation ACDC — which the club may name by schema even though Alice issues it, because the origin's *shape* is governance, not Alice's invention; the club asks the origin for its issuer, its issuee, and its full rules (`r/`, trailing slash = "the whole node," so it can read the terms it is agreeing to). Cross-edge paths are DAG-absolute and cross an edge via the virtual **`_` hop** component: `/e/identity/_/a/photo` descends the origin's edge section to the `identity` edge, hops to the far ACDC, and lands on `a/photo`. Omitting `_` does not merely misroot the path, it makes it meaningless (`/e/identity/a/i` names an `a` field inside the near-side *edge* block, which has none). A **solicited** offer answers with an empty `dp`, meaning "the same paths the apply asked for," so the two messages cannot drift. Note the implementation tier: at the current pin `dp` is validated for *wire shape* on `apply`/`offer`, and the `_` component round-trips through qb64, but **no verb yet checks a disclosed DAG against its `dp` plan, and no `Pather` method yet resolves `_` across an edge** — `dp` is negotiated, not enforced (`bible/08` §4; `test_cp_disclosure.py:978–1070`, `1200–1255`).

## 6. Witnesses, registrars, observers, watchers

Sam's framing (KERIcon 2026, via `bible/05` §9 and `bible/10` §6) is that verification is split across two parties at *each* layer, deliberately — a governance decision, not a caching optimization: **"witnesses controlled by controllers, watchers controlled by verifiers; registrars controlled by issuers, observers controlled by verifiers."** The KEL layer gets witness/watcher; the TEL/registry layer replays the same split one level up with registrar/observer.

**Issuer side (Utah).**
- **Witnesses** receipt Utah's KEL events — its inception, rotations, and the seals that anchor every TEL/registry event — giving accountable duplicity-detection for the State's own key state (enough witnesses to reliably detect and recover from duplicity is what an LoA-3 ceremony requires).
- **Registrars** maintain and publish the registries — the `sedi-id` and `sedi-age` set TELs — and append the blindable issuance/revocation updates.

**Verifier side (the club).**
- **Observers** cache/mirror registry state so the verifier can check issuance/revocation status **without phoning home to Utah at the point of validation.** This is the explicit rejection of OCSP/CRL: a registry consulted at verification time is a phone-home in disguise, and would let Utah learn every bar and dispensary the citizen visits. Observer↔registrar sync happens on state changes, **batched** (batching is a privacy requirement, not a performance one — synchronized bulk updates stop an observer correlating which registries changed when), never at the point of validation.
- **Watchers** watch Utah's KEL for duplicity, confirming the State key state that the credentials' authenticity ultimately bottoms out in. Watchers watch *KELs* (looking for duplicity); observers watch *TEL state anchored to a KEL*. They depend on watchers but are not watchers.

**Build-status tiers — hold these, they bound everything above.**
- Registrar and observer are **architecturally committed but operationally unbuilt**: `keri-foundation/observer` and `/registrar` are placeholder repos (LICENSE + one-line README), `registraring.py` is a stub, and keripy has no observer module. What *is* built is the layer beneath — the blindable `bup` update and `BlindState` structures. Treat "the observer handles that" as a non-answer to a live design question.
- There is a proposed **third leg: an issuee-controlled presentation (usage) registry** in which the holder's own presentations are anchored, letting the *citizen* detect a compromise of her presenting keys (the mirror of the issuer-side anti-forgery story). It is **pre-normative and unimplemented** (keripy #1095/#1613); the one word "usage" in the ACDC spec's `rd` field-kind list is its only trace there. keripy at `b8f60166b` now *walks the disclosed DAG and authenticates each node against its issuer's registry*, but nothing compares a registry's state to a `grant` SAID, and one check that landed (`vetBindings`: the ACDC's issuer must match the registry incepter) **excludes a presentation registry by construction**, because a presentation registry is incepted by the issuee. See `bible/10`.
- The caution from §4 restated as infrastructure: for Utah's bulk plan, the **witness/mailbox topology for the M `ALICE_k` AIDs** can re-link the per-context partition if shared, so it is part of the correlation-resistance design, not an afterthought.

## Source anchors

- keripy tests: `tests/acdc/test_bulk_issuance.py` (`upstream/main`), `tests/acdc/test_cp_disclosure.py` (branch `feat-dp-disclosure-paths`), `tests/acdc/test_ipexing.py`, `tests/acdc/test_examples.py`.
- `bible/`: `05-acdc-and-verifiable-data.md` §§8–10, `06-governance-ecosystems-and-interop.md` §§3–4, `08-presentation-architectures-and-ipex.md` §§3–4 & 11, `10-presentation-registries.md`.
- keripy discussions/PRs: #1515 (SEDI core-identity ↔ entitlement = `E1E`), #1532 (bulk issuance → unique AID per context), #1523 (real `E1E` branch), #1527 (operator-coercion fix), #1549/#1542 (`dp`, `_` hop, origin node), #1095/#1613 (issuee usage / presentation registry), panel review PRV-F2.
- Statute: Utah Code §63A-20 (SEDI), §63A-20-301 (minimum-age proof), §63A-20-701 (data loyalty / safe harbor), §63A-20-801 (evidentiary consequence).
