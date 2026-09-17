# What can be discovered in the vLEI ecosystem today

*Field notes, 2026-09-14. This is a record of measurements, not doctrine — every claim was verified against a live endpoint on that date and any of them can rot. The reproduction commands are inline so a later reader can re-measure rather than trust.*

Companion to a census of which QVIs publish a `.well-known` surface, which lives in a private repo because it names organisations — `../../../bakobo/infra/docs/vlei-qvi-wellknown-census.md` on the author's machine. This document covers what each public data source contains, what it does not, and the two techniques that bridge the gap; it is public because it is method, and because everything it measures is GLEIF's own published behaviour or one's own.

## The shape of the problem

**Witness endpoints are published per AID, never per witness.** You can learn where a witness is by asking about an identifier it witnesses. There is no way to ask about the witness itself.

That asymmetry is architecturally defensible — a witness is meaningful relative to the identifier that designated it, so anchoring discovery to the AID is a reasonable default. It becomes a problem in the cases where the witness AID is all you have: you hold a receipt and want to check it against the witness that produced it; you want to know who operates a given witness; you want to know whether a witness seen in one KEL is the same one seen in another.

A related and larger gap sits one level up. **No public GLEIF source contains an AID of any kind.** The dashboard, the credential API and the LEI API are keyed on LEI and SAID. So for eight of the nine QVIs, the identifier you would need to start from is not obtainable at all.

> **How this document was nearly wrong.** An earlier version of this research concluded that nothing published says where a witness is. That was false. GLEIF's catalog entry for a *witness* is an inception event with no endpoint field — true — and the conclusion was generalised from it without ever opening an entry for an *AID*, which is an `rpy` on route `/oobi/witness` carrying five witness URLs and has been since 2022-11-21. Checking one class of entry and concluding something about the surface is the error. If you are re-deriving this, open every class of entry before generalising.

## Source by source

### GLEIF's vLEI dashboard — <https://vlei.gleif.org/dashboard>

Static HTML, no JavaScript API calls, pre-rendered. Carries global counts (128 credentials, 9 QVI, 69 LE, 50 OOR as of 2026-09-14), and for each credential the LEI, legal name, issuance date, status, and SAID.

The SAIDs link to `https://vlei.gleif.org/api/v1/qvi-credentials/<SAID>` — the API referred to below.

**Contains 124 KERI-shaped identifiers and all of them are credential SAIDs.** Zero `B` prefixes, so no witnesses; and no issuer or issuee AIDs either. Grep the HTML for `\b[EB][A-Za-z0-9_-]{43}\b` and check the prefix distribution before assuming otherwise.

### GLEIF's APIs

| Endpoint | Gives | Contains AIDs? |
|---|---|---|
| `api.gleif.org/api/v1/vlei-issuers` | 8 QVIs: `lei`, `name`, `website`, `marketingName`, `qualificationDate` | no |
| `api.gleif.org/api/v1/lei-records/{lei}` | legal name, jurisdiction, address, registration status | no |
| `vlei.gleif.org/api/v1/qvi-credentials/{said}` | `{lei, said, issuedAt, revokedAt}` + link to child LE credentials | no |
| `vlei.gleif.org/api/v1/qvi-credentials/{said}/le-credentials` | the LE credentials issued under it, same four attributes each | no |

`?format=cesr` is accepted and ignored — it returns the identical JSON-API envelope. Every `Accept: application/json+cesr` variant likewise returns `application/vnd.api+json`.

**GLEIF publishes the credential's identity and never the credential.** That single sentence is the biggest structural finding here. The issuee AID — the QVI's identifier — exists only inside the ACDC, and the ACDC is held by the issuer and the holder, not by GLEIF's public surface.

### `.well-known` on QVI websites

One QVI in nine publishes one, measured 2026-09-14. The per-organisation results are in the private census. The one that does publish, Provenant, is the only public source anywhere binding a QVI's name to its AID:

```
https://provenant.net/.well-known/keri/oobi/index.json
  → {"aids": {"GLEIF RoOT": "EDP1vHcw…", "Provenant as QVI": "ED88Jn6C…"}}
```

GLEIF's own surface at `gleif-it.github.io/.well-known/` (mirrored byte-identically at `weboftrust.github.io`) carries three AIDs, eight schemas and ten witnesses. Its entry shapes are the thing to understand:

| `/.well-known/oobi/{id}/index.json` where id is | returns |
|---|---|
| an **AID** (`E…`) | `rpy`, route `/oobi/witness`, with that AID's witness URLs |
| a **witness** (`B…`) | the witness's `icp` event — **no endpoint** |
| a **schema** (`E…`) | the schema JSON |

The field is named `oobi` but holds a path to a local document, not a resolvable OOBI. That naming is the single most effective trap in this whole surface.

### Credential dumps

A vLEI credential downloaded from a QVI's web portal is a CESR stream containing the full issuance chain — every KEL, the TEL events, the ACDCs, and the receipts. The specimen examined here was 383 KB, 365 messages, four chained ACDCs running GLEIF External → Provenant QVI → GLEIF Internal → Provenant QVI → a fourth AID.

**It contains zero endpoint records.** No `/loc/scheme`, no `/end/role`, no `rpy` of any kind, and no `http` URL outside two specification links in the ACDC body. Verified by plain text search as well as by parsing, and the parse accounted for all 365 JSON messages — the remaining two thirds of the bytes are CESR attachments, signatures and receipts.

This is worth stating precisely because the artifact is production output, not somebody's export: **what a QVI portal hands a relying party carries everything needed to verify offline and nothing needed to reach any witness named in it.** Verification and discovery are genuinely different problems and the dump solves only the first, which may well be correct design — a verifier that already holds the events needs no endpoints.

What the dump *does* give, and it is the only route to this: the issuee AID of each credential, from the ACDC's `a.i` field. That is how a QVI's AID becomes known at all.

### Witness HTTP endpoints

keripy witnesses serve `/`, `/receipts`, and `/query` (`src/keri/app/indirecting.py:100-104`). `QueryEnd` at line 1191 accepts:

```
/query?typ=kel&pre=<AID>[&sn=<n>]
/query?typ=tel&reg=<registry-AID>
/query?typ=tel&vcid=<credential-SAID>
```

Measured behaviour, which differs by operator:

- **GLEIF's witnesses** serve `/query`. The KEL form works (28 KB for the External AID). **The TEL form returns HTTP 200 with zero bytes** — for GLEIF's own QVI-credential registry `EM5S-xbxpG6qWG6doRcu9plZEVNexVliKgDQPASTb4rU`, and for a known-good credential SAID. The witnesses hold KELs, not credential registries.
- **Provenant's witnesses** return 404 on `/query` entirely — older keripy, or disabled.
- **Bakobo's witnesses** serve it (current keripy).

So the TEL query endpoint cannot currently be used to enumerate issuances. And even a populated TEL would not close the AID gap: an `iss` event carries the credential SAID and the registry, never the issuee. The issuee lives in the ACDC.

Witnesses answer **406** for an identifier they do not serve and **200** for one they do. That discrimination is load-bearing for the technique below, and it is an implementation detail rather than a contract — Provenant's witnesses return 200 on every form tried, so behaviour already varies.

## Technique 1: the cross product (crude, reliable, rude)

To bind witness AIDs to endpoints when nothing publishes the binding.

1. Take the host prefixes from an AID's published `/oobi/witness` reply — the `a.urls` array. Each URL is absolute, carrying scheme, host and port explicitly.
2. Take the witness AIDs from that AID's KEL: `b` from the inception event, then apply `br`/`ba` from every rotation in sequence order to get the *current* set.
3. Cross them. For each `(host, witnessAID)` pair, fetch `http://<host>/oobi/<witnessAID>/controller`.
4. Keep the 200s. Each response is an `icp` event whose `i` equals its sole `k` — self-proving, so a wrong guess cannot produce a false positive.

Verified against GLEIF: 50 combinations, exactly 5 hits, one per host, no ambiguity.

Its costs are real. It is quadratic — 5 hosts by 10 AIDs to learn 5 facts, and a few thousand requests at ecosystem scale. Every miss is an unsolicited request to somebody's production witness. It only finds witnesses already designated by an AID you know, so a witness AID arriving from a receipt or another KEL is no better off. And it depends on the 406/200 discrimination, which nobody promised.

## Technique 2: order alignment (efficient, unguaranteed)

**The `a.urls` array and the KEL's current `b` array are in the same order.** Zip them and the mapping falls out with zero probe requests.

Verified on two independent operators: GLEIF 5/5 positions, Provenant 5/5 positions with every pair confirmed by fetch. It also received accidental third-party corroboration — GLEIF's three AIDs have overlapping witness sets, and five witnesses appearing in two different AIDs' lists landed on the same address both times (`BGYJwPA…` at `102.37.159.99` from root and External; likewise `BM4Ef3z…`, `BDwydI_…`, `BLo6wQR…`, `BNfDO63…`).

The invariant is almost certainly not a coincidence: both lists are generated from the same ordered witness set by keripy, so the ordering is shared implementation rather than agreement.

**Treat it as a strong heuristic and never as a guarantee.** Three ways it breaks silently:

- A witness set rotates. `br`/`ba` changes `b`; if the `rpy` is not regenerated in the same operation the lists stay the same length and now mean different things.
- An operator hand-edits the `rpy`, or generates it with something other than keripy, and orders URLs differently.
- Counts diverge — a witness added without its URL published — and `zip` truncates silently rather than erroring.

In every case the mapping is wrong, nothing detects it, and the endpoint still serves a valid self-proving OOBI for *some* witness, so even a careful consumer gets a coherent-looking answer. **Verify with one fetch per pair.** That reduces the cross product from quadratic to linear while keeping the proof.

## What was actually reconstructed

24 witnesses, all verified live and self-proving on 2026-09-14.

| Operator | Witness AIDs known | Endpoints resolved | Endpoint form |
|---|---|---|---|
| GLEIF | 10 | 10 | bare IPv4, port 5623, `http` |
| Provenant | 20 (published) | 10 | hostnames, port 5631, `http` |
| Bakobo | 4 | 4 | hostnames, 443, `https` |

GLEIF's ten required all three of its AIDs, since no single AID designates more than five. Provenant's ten came from the two AIDs in the credential chain; the other ten of their published twenty have no endpoint obtainable from public data. Bakobo is the only operator publishing a per-witness endpoint field directly, which is why its four needed no technique at all.

**The remaining QVIs are entirely unmapped**, because their AIDs are not published anywhere reachable. Reaching them requires either that QVI publishing a `.well-known` of its own, or a credential from them in CESR. Which ones, and what each site does return, is in the private census.

The honest summary, and the strongest argument for changing something: **an enumeration of the vLEI ecosystem's witnesses, attempted from GLEIF's own published surface, reaches three operators out of nine — because that surface contains no AID anywhere.**

## Two changes that would close this

Both are additive, neither is a specification change, and each is one field.

**Bind the witness to its URL in the `rpy`.** The `/oobi/witness` reply is a bare `urls` array whose association with `b` is positional and undocumented. Naming the witness beside each URL makes an invariant everyone already depends on into something a consumer can check and a generator can get wrong loudly. Scheme and port come along free, since the URLs are already absolute.

**Put the issuee AID in the dashboard API.** One field on `qvi-credentials`, a record that already exists, would make the entire ecosystem's witness topology derivable by anyone using the techniques above.
