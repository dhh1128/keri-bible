# 08 — Presentation Architectures and the IPEX Disclosure Model {#presentation}

## Thesis {#thesis}

An ACDC presentation discloses not a credential but a directed acyclic graph of credentials, normalized to have exactly one source node, the origin, and negotiated by naming paths into that graph rather than attributes. That commitment lets ACDC absorb the other verifiable-credential architectures: a one-node DAG is a portable data lake, and a bespoke origin with N edges is a credential soup made cryptographically rigid. The hard part is a problem the graph does not answer. A DAG commits to data, and a presentation must also establish who is presenting, now, and with what authority. Freshness (KRAM), multiple endorsement, anchoring (`ax`), tethering and presentation registries all answer that authentication-factor problem, and none is in any specification branch. The commonest errors here are quoting a design discussion as spec, and quoting a spec's forward branch as its standardizing one.

## Status {#status}

This is the least-settled area of the KERI/ACDC design space, revised in public and in place; read it as a map of a live argument, not a conformance reference. Before relying on a claim, check keripy discussion [#1627](https://github.com/WebOfTrust/keripy/discussions/1627), then [#1613](https://github.com/WebOfTrust/keripy/discussions/1613), whose body still carries the self-declared version string "v1.5 2026/08/18" although GitHub records later edits, then the open keripy and `kswg-acdc-specification` pull requests in [Sources](#sources).

The distance from normative is uneven. The authentication half, [section 7](#authentication-factors) through [section 10](#anchoring), is in no specification. The structural half, [section 2](#one-dag-one-origin) and [section 4](#disclosure-paths), is in the ACDC `v1.1` branch only, so it is [spec-next]; `main` at `f0bd097de` does not contain the words Disclosure Paths. [spec] covers the bespoke ACDC, four of the five unary edge operators, the m-ary operators, the edge `s` constraint, and an IPEX route table that negotiates by naming attributes. keripy at `94f5423a3` is ahead of both branches in places, in a V2 IPEX module its CLI does not run ([section 6](#two-ipex)).

## 1. The four presentation architectures {#architectures}

[proposal] The taxonomy is from #1627, ACDC Presentation Architectures (SmithSamuelM, 2026-08-19).

### Portable Datalake {#portable-datalake}

One document holds all attributes about one subject from one issuer, and the holder discloses a subset: mDoc/mDL and mainstream W3C VC. It cannot express delegation; everything comes from "one and only one Issuer"; the issuer must pull from every relevant database, inviting the consolidated data lake that maximizes breach blast radius; and reissuance runs at the rate of the most volatile attribute.

### Credential Soup {#credential-soup}

Attributes come at presentation time from several credentials, issuers and issuees, as in Sovrin. It allows partitioned issuer databases, but negotiation is ambiguous, each source needs its own fresh proof of control, nothing proves several issuee AIDs are one party, and a soup "cannot support delegation in any normative secure way."

### Verifiable DAG {#verifiable-dag}

ACDC's default. Edges carry digests of their far nodes, so "A verifiable cryptographic commitment to the origin ACDC of that DAG is a verifiable commitment to every node in the DAG," and typically only the origin's issuer or issuee needs a fresh authentication factor. Delegation is native, and forgery "must be in totality, and not piecemeal," unlike in a soup. The costs are verification complexity and the reissuance cascade of [section 12](#sedi-recipes).

### DAG Soup {#dag-soup-architecture}

Several disconnected DAGs, each with its own origin, in one exchange under a multiply-endorsed grant; the subject of #1627's only concrete proposal ([section 11](#dag-soup)).

### ACDC subsumes the other two {#subsumption-claim}

"the ACDC DAG, as a special case, can mimic either a portable data lake or a credential soup as needed." One ACDC with a selectively disclosable aggregate is a data lake; a bespoke origin with N edges is a soup with a verifiable spine. It is #1627's strongest argument.

## 2. The normalized structure: one DAG, one origin {#one-dag-one-origin}

[spec-next] An ACDC is a graph fragment, a node and its outgoing edges only, and the exchanged graph is normalized: "That DAG MUST have exactly one source node, called the origin node" (ACDC spec > Disclosure Paths > DAG of ACDCs, L1821 @2362e48a1). Where the material is not already connected, "a DAG MUST be formed by issuing a bespoke ACDC whose node is the origin, with Edges chaining back to every other ACDC the exchange includes" (ACDC spec > Disclosure Paths > DAG of ACDCs, L1823 @2362e48a1).

The origin is a source, not a root of authority. Edges point near to far and carry the far node's digest, so authority flows toward the origin while commitment flows from it. #1627 uses "root of the DAG" for the far, deepest node, the opposite end; translate when reading it beside the spec.

The DAG is well-ordered, so "A well-ordered DAG with a single source node linearizes into a unique, reproducible order" (ACDC spec > Disclosure Paths > DAG of ACDCs > Ordering, L1831 @2362e48a1), breadth-first by choice. That lets `dp` identify an ACDC by position rather than by SAID, so a disclosure request adds no correlator of its own. The branch overloads "node" on purpose: "node path" in [section 4](#disclosure-paths) means a block within one ACDC, "origin node" a node of the DAG.

### The Dossier spec's graph-root rule {#dossier-graph-root}

[spec] The Dossier spec normalizes a presented dossier the same way: "the dossier under evaluation MUST be the only ACDC that no other ACDC in the set points to" (Dossier spec > Dossier Data Model > The Edges Attribute > The Dossier as Graph Root, L98 @6fcf84127). Its claim that ACDC "already requires" one origin (L100) holds for `v1.1` only. It names this chapter's second problem too: "The act of delivery SHOULD itself be authenticated, separately from the dossier's own anchor" (Dossier spec > The Operational Lifecycle > Presentation as a Self-Contained Package, L349 @6fcf84127).

## 3. The bespoke origin ACDC {#bespoke-origin}

[spec] A bespoke (disclosure-specific) ACDC is issued by the Discloser for one exchange: "A given Discloser issues its own bespoke ACDC referencing some other ACDC via an Edge. This means that the normal validation logic and tooling for a chained ACDC can be applied without complicating the presentation exchange logic" (ACDC spec > Disclosure-specific (Bespoke) Issued ACDCs, L1862 @f0bd097de; identical at L2063 @2362e48a1). It carries presentation-specific terms in its rule section, such as anti-assimilation and one-time-purpose clauses, and names the Disclosee as Issuee, so that "Signing the agreement to the offer of that bespoke ACDC consummates a contract between the named Issuer and the named Issuee." Its structural job as origin is [spec-next]; conflating the two makes the origin apparatus look standardized.

### A purpose clause belongs in the bespoke origin {#purpose-clause}

[proposal] Asked whether an exchange message should state its purpose in `m`, Sam pointed to the origin's rule section: "The advantage of putting it in the DAG is that it gets all the security, perpetuality, etc of the DAG" (keripy discussion #1617, comment of 2026-08-13, R-064, https://github.com/WebOfTrust/keripy/discussions/1617#discussioncomment-18006490). It is a preference, not a ruling.

### The bespoke origin as recipe {#recipe}

[proposal] Unchained ACDCs from one root of trust to one issuee, the SEDI shape, are a degenerate soup, since "All the ingredients came from the same cupboard." A bespoke origin with one edge per ingredient makes them a DAG, and needs no registry or anchor: "It merely needs to be signed and have attached signatures because it's a one-time use ACDC." Its schema is not one-time: "It acts as a permanent recipe for the soup... an EGF can define the schema of the bespoke ACDC for all its seminal use cases."

#1627 justifies the recipe edge correctly, "each edge from the recipe ACDC can use the I2I edge operator", and then misstates it: "the Issuer of the recipe is the citizen AID, and the Issuer of all the far node ACDCs is also the citizen AID" is wrong, because the State issues the far nodes and the citizen is their Issuee.

## 4. Disclosure paths: the `dp` field {#disclosure-paths}

[spec-next] `dp` is how a disclosure is requested. It grew out of discussions #1512, #1542 and #1549 into a `v1.1` section that begins "This section is normative." (ACDC spec > Disclosure Paths, L1811 @2362e48a1). Its only binding to a message sits inside the IPEX section, which opens "This section is non-normative.", so the syntax is normative and its only use is not ([question 10](#q-dp-normative-seam)).

### Shape {#dp-shape}

"The `dp` field is not an ACDC field. It appears in the messages that negotiate a disclosure, not in the ACDCs that are disclosed" (ACDC spec > Disclosure Paths, L1813 @2362e48a1). Its value is a list of tuples, each "of the form `(ACDCSchemaSAID, PathPrefix, [paths])`" (ACDC spec > Disclosure Paths > Disclosure Paths, `dp`, Field, L1881 @2362e48a1), a list rather than a map because "Two ACDCs of the same type, that is, of the same Schema SAID, MAY appear in one DAG, and a field map could not tell them apart" (ACDC spec > Disclosure Paths > Disclosure Paths, `dp`, Field, L1883 @2362e48a1).

A request is a path rather than a schema because of Sam's layering: "So disclosure is reasoning about exposure. What parts to expose when. Not what those parts mean." (keripy PR #1505, comment of 2026-07-16, R-058, https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4992746261). [proposal]

### Path syntax and closures {#path-syntax}

A path beginning with `/` is DAG-absolute; others are ACDC-relative. Edge traversal "MUST therefore begin with `/e`", and the hop to the far ACDC is the virtual component `_`, as in `/e/reports/project/_/a/author` (ACDC spec > Disclosure Paths > Path Syntax > Traversing Edges, L1845 @2362e48a1). The compact CESR form separates components with `-`, which is why `v1.1` restricts field labels ([chapter 05, section 1](05-acdc-and-verifiable-data.md#field-label-restrictions)). A path ending in `/` designates a whole node and everything beneath it; one ending in a component "designates a single leaf" (ACDC spec > Disclosure Paths > Path Syntax > Node Paths and Leaf Paths, L1855-1861 @2362e48a1).

"The disclosure designated by a set of paths is the union of their closures" (ACDC spec > Disclosure Paths > Path Syntax > Closures, L1865 @2362e48a1). In a partially disclosable section one SAID and UUID cover the block, so a leaf path discloses all its simple fields; in the selectively disclosable Aggregate Section a leaf path "closes over that block alone and tells nothing of any sibling." The rule section "MUST NOT be assumed fully disclosed," so it is designated when wanted. Paths are not permissions: "A closure states what a path discloses. It does not bound what the Disclosee may then do with what it holds."

### Prefixes and ordering {#dp-ordering}

A prefix is empty or a DAG-absolute path to the tuple's ACDC, and the effective path is prefix plus entry (ACDC spec > Disclosure Paths > Disclosure Paths, `dp`, Field > Path Prefix, L1889-1891 @2362e48a1). Elements are breadth-first and "The zeroth element MUST represent the origin node ACDC" (ACDC spec > Disclosure Paths > Disclosure Paths, `dp`, Field > Identifying Each Tuple's ACDC, L1899 @2362e48a1). With empty prefixes position identifies each tuple; where a schema makes an edge optional, "The ordering then has gaps. In that case the prefix of every element after the zeroth MUST be non-empty" (ACDC spec > Disclosure Paths > Disclosure Paths, `dp`, Field > Identifying Each Tuple's ACDC, L1911 @2362e48a1). In the Aggregate Section a path may name a blinded block by its unique field label, `A/over21`, but not reach inside it (ACDC spec > Disclosure Paths > Special Cases > Aggregate Section Pathing, L1923-1931 @2362e48a1).

### Placement and the route table {#dp-placement}

"So where a `dp` field appears in an `apply` or `offer`, it MUST appear in that message's query section, `q`, and not in its attribute section, `a`" (ACDC spec > IPEX Protocol Messages > Disclosure Paths in `apply` and `offer`, L2015 @2362e48a1). `a` is where `ax` and the origin `o` are proposed to live ([section 10](#anchoring)).

The route table differs by branch. On `main` the `apply` row reads "Schema or its SAID, Attribute field label list, Aggregate element label list, signature on `apply` or its SAID" (ACDC spec > IPEX Protocol Messages, L1811-1813 @f0bd097de) [spec]; on `v1.1` both label lists in `apply` and `offer` become `dp` (ACDC spec > IPEX Protocol Messages, L2004-2006 @2362e48a1) [spec-next]. The other rows match. A row quoted without its branch misstates the protocol.

### An empty `dp` {#empty-dp}

In an answer, an empty list means "the answering path list is the same as the one it answers"; unsolicited, it "MUST NOT be an empty list" (ACDC spec > Disclosure Paths > Disclosure Paths, `dp`, Field > Solicited Response, L1917 @2362e48a1). [spec-next] Sam has ruled otherwise, so the branch lags its editor: "If there is no prior message then an empty [] means give me nothing. To get everything their must be a path." (keripy PR #1698, comment of 2026-10-01, R-052, https://github.com/WebOfTrust/keripy/pull/1698#issuecomment-5937132701). [proposal] keripy follows him, "An empty plan inherits from a prior message and means no disclosure when the message opens a thread.", and requires `dp` on `agree` and `grant` too (keripy acdc/ipexing.py, IpexHandler.verify, L580-586 @94f5423a3). [code]

### Predefined shapes {#predefined-shapes}

[proposal] Sam expects the general machinery to be used narrowly: "So predefined shapes will be the norm." (keripy discussion #1542, comment of 2026-07-30, R-055, https://github.com/WebOfTrust/keripy/discussions/1542#discussioncomment-17842586), with shapes defined by EGFs. He adds a rule no branch carries: an `offer` whose origin schema differs from the `apply`'s "is functionally the same as if the Offerer spurned the apply and then initiated a new IPEX with an unsolicited offer", and an IPEX may start with an `offer` or a `grant` (same discussion, https://github.com/WebOfTrust/keripy/discussions/1542#discussioncomment-17841472).

### `dp` in keripy: negotiated, then enforced on the grant {#dp-in-keripy}

[code] V2 requires `dp` in `q` of all four disclosure verbs, as one triple in a one-element list: "We currently only support one DAG (until Multi DAG), so exactly one entry is required." (keripy acdc/ipexing.py, _validSingleDagList, L269 @94f5423a3). An `agree` may not change the plan, and "A Grant may repeat but may not renegotiate an accepted prior plan." (IpexHandler.verify, L691). Each disclosed section must equal the `Compactor` partial for its requested paths, and "The plan must account for every disclosed node in canonical BFS order." (IpexHandler._verifyDisclosurePlan, L1089). A grant disclosing more or less than agreed is refused. V1, which the CLI runs, has no `dp` check; `vc/protocoling.py` never mentions it ([question 8](#q-dp-enforcement)).

### A grant must keep the Offer's promise {#offer-fulfillment}

[code] An Offer may name its origin by SAID alone, a "commitment-only Offer" (keripy acdc/ipexing.py, offer, L2384 @94f5423a3), or carry nodes without issuer proofs. A grant answering an `agree` must deliver that origin, or, where the Offer carried field-map metadata, a root matching its issuer, `rd` and non-empty sections: "Only field-map metadata can promise a different credential root." (IpexHandler._verifyOfferFulfillment, L1198). A SAID-only Offer answered by a different root escrows, and nothing traced releases it ([question 8](#q-dp-enforcement)).

## 5. Edges and operators, as presentation uses them {#edges}

`I2I` closes the bespoke recipe, and every proposal to signal multiple endorsement in the ACDC is a new edge-group operator ([section 9](#multiple-endorsement)). The operators, their keripy enforcement, `E1E`, the proposed `I1I` and `DI1I`, and the decided v1.1 change of the empty-operator default to `NI2I` live in [chapter 05, section 5](05-acdc-and-verifiable-data.md#edges). [code] keripy's `vdr/verifying.py` and V2 `acdc/ipexing.py` now share one `AND`/`OR` algebra and agree on unrecognized, listed and absent operators, but each walks the Edge Section itself: "So this module holds no storage and no evidence." (keripy acdc/chaining.py, module docstring, L16 @94f5423a3). They still differ on schema pins, the schema validator, compact Edge Sections and nesting depth, which v1 bounds at 8 and V2 does not ([chapter 05, section 5.1](05-acdc-and-verifiable-data.md#module-disagreement)). The difference that matters most here is revocation. v1 refuses a chain through a revoked far node, while in V2 "No registry-state policy lives here." (keripy acdc/ipexing.py, IpexHandler, L484 @94f5423a3): a V2 grant whose DAG holds a revoked credential is accepted, the state recorded in `exrs` for an application or EGF to judge.

The operator namespace has no registry. The Dossier spec writes `MxN`, `RMxN`, `MxQ` and `RMxQ` into it, "defined for the `o` field of an edge group to support joint issuance" (Dossier spec > Joint Issuance > Threshold Operators, L624 @6fcf84127). Nothing prevents a future collision.

### Edge validation as its own layer {#edge-layer}

[proposal] "I agree that the edge logic should be at its own layer and have its one verification function" (keripy PR #1681, comment of 2026-10-15, R-080, https://github.com/WebOfTrust/keripy/pull/1681#issuecomment-6201960001), "one" reading as "own", staged with `I2I` kept in IPEX `verify` meanwhile. No such layer exists at `94f5423a3`. [code]

## 6. Two IPEX state machines, and only one of them runs {#two-ipex}

### V1 and V2 {#ipex-v1}

[code] keripy has two IPEX implementations, and every [code] claim must say which. V1, `vc/protocoling.py`, is what the CLI loads (keripy cli/commands/ipex/list.py, L25 @94f5423a3). Its legal-predecessor table runs `apply`, `offer`, `agree`, `grant`, `admit`, with `spurn` answering any of the first four; it rejects a second response to one prior and fails closed on an unmatched route (keripy vc/protocoling.py, PreviousRoutes and verify, L16-22 and L55-106 @b8f60166b; byte-identical at `94f5423a3`). V2, `acdc/ipexing.py`, is library and tests only: its `loadHandlers` (L2851 @94f5423a3) has no caller in `src/keri`. V2 claims are about code that exists, not behavior keripy performs, and every authentication mechanism in sections 7, 9 and 10 is in V2.

### The split is deliberate {#split-deliberate}

[proposal] The `acdc` subpackage "provides a place to support the new features in acdc v2 while leaving support for acdc v1 in the vc subpackage." (keripy PR #1170, body of 2026-02-04, R-078, https://github.com/WebOfTrust/keripy/pull/1170), and "Its only with v2 exchange messages that we plan to anchor exchanges. We really don't want to be anchoring v1 exchanges." (keripy PR #1492, comment of 2026-07-27, R-057, https://github.com/WebOfTrust/keripy/pull/1492#issuecomment-5093267019). V2 is meant to survive; when the CLI moves to it is unsaid.

### Where V1 and V2 disagree {#v1-v2-differences}

[code] V2 lets a `grant` answer an `apply` directly, `Ipex.grant: (Ipex.apply, Ipex.agree),` (keripy acdc/ipexing.py, PreviousRoutes, L41 @94f5423a3); V1 requires `agree` first; neither ACDC branch specifies predecessors. V2 adds role symmetry between prior and reply, rejection of orphan nests and dangling edges, "Grant fails closed on dangling references" (IpexHandler._walkGraph, L1267), a one-nest-per-node guard against substitution, edge-group evaluation, the plan and Offer checks of [section 4](#dp-in-keripy), per-node schema validation, and the checks of sections 7 and 10.

### Spurning a grant {#spurn-grant}

[code] V2 refuses a spurn only of a grant that answers a prior: `if verb == Ipex.spurn and pverb == Ipex.grant and pserder.ked.get("p", ""):` (keripy acdc/ipexing.py, IpexHandler._verifyReplyChain, L939 @94f5423a3). V1 lets a spurn answer any grant. The rule is Sam's: "an unsolicited grant i.e using a xip message should be spurnable. that is nuance i did not anticipate." (keripy issue #1628, comment of 2026-08-19, R-051, https://github.com/WebOfTrust/keripy/issues/1628#issuecomment-5349282926). A disclosee who never asked can refuse a credential; one who agreed cannot repudiate after the grant. [proposal] Neither branch's route table has a row for spurning a `grant` (ACDC spec > IPEX Protocol Messages, L1812-1816 @f0bd097de; L2005-2009 @2362e48a1) ([question 11](#q-spurn-grant)).

### Deferral and refusal {#defer-vs-refuse}

[code] The exchange handler escrows a message whose chain is missing, because "Registry-backed IPEX grants may arrive before the disclosee has fetched the issuer's TEL history from observers", and drops one whose behavior check fails before it is logged (keripy peer/exchanging.py, Exchanger.processEvent, L390-406 @94f5423a3). A message whose schema is not cached escrows separately, under its exchange and schema SAIDs, while the schema is queried (L408-427). Only the grant route opts out of waiting on missing foreign evidence: "Opted routes request the KEL and continue with known factors." (keripy peer/exchanging.py, Exchanger.processEvent, L170 @94f5423a3).

## 7. Authentication factors: the second problem {#authentication-factors}

[proposal] The DAG does not prove the sender controls anything now. #1613, Authentication Factors in IPEX, treats this.

### Two purposes, three ranked factors {#factor-ranking}

Each ACDC in a granted DAG needs an Issuer factor; the `grant` needs a fresh Grantor factor; "For a given ACDC, a Grantor may be the Issuee, Issuer, both, or neither." Factors rank registry (TEL) anchor, KEL anchor, bare signature, because anchors "enable perpetual verifiability and detectability of impersonation fraud. Whereas a bare signature does not," and the highest supplied factor is used. A bare signature dies with the issuer's key state: such ACDCs "become unverifiable and must be reissued" after rotation, so a signature-only bespoke origin suits a one-time recipe and not later proof of what was presented.

### The issuer factor in keripy {#issuer-factor-every-node}

[code] V2 authenticates each node by "its declared issuer authentication factor" (keripy acdc/ipexing.py, IpexHandler._authenticateIssuer, L1822 @94f5423a3), without fallthrough: registry if a top-level `rd` is present, else an issuer-KEL seal, where "An invalid anchor must not silently downgrade the ACDC to signature authentication." (L1889-1890), else signatures that "already name the current state" (L1927). The result is a verdict member, "so an Operator that does not need this node is not made to wait on it or fail because of it." (IpexHandler._verifyIssuerAuthNode, L1801-1803): a node behind an unneeded `OR` branch may fail without failing the grant, while the origin's factor is always required. By inference from the code, not a run, an unanchored ACDC signed under since-rotated keys no longer authenticates in a V2 grant ([question 9](#q-current-keys)).

### Vocabulary and the receiver AID {#receiver-aid}

The Discloser sends `offer` and `grant`; the Disclosee sends `apply`, `agree` and `admit`. "In common parlance, a Grantor is a Presentor, and the grant is a presentation." (keripy discussion #1613 > Introduction). Every message names both parties, and Sam treats the negotiating AIDs as the price of a binding contract rather than a leak: "Proof of participation is not the same as correlation." (keripy discussion #1542, comment of 2026-07-23, R-054, https://github.com/WebOfTrust/keripy/discussions/1542#discussioncomment-17755467). [proposal] V2 refuses a reply whose prior names no receiver (keripy acdc/ipexing.py, IpexHandler._verifyReplyChain, L945-947 @94f5423a3). [code]

## 8. Freshness: KRAM, and what rests on it {#freshness-kram}

KRAM is treated in [chapter 09](09-kram-and-request-authentication.md); this section covers how IPEX depends on it. A signature is a bearer token, "Any holder of both the document and its signature can replay them, and the signature will verify" (#1613), and KRAM gives one play or none within a window on the receiver's clock, collecting a multisig sender's signatures in its escrow. It uses monotonic receiver-clock datetimes, not the nonce #1613 describes ([chapter 09, section 8](09-kram-and-request-authentication.md#load-bearing)), and it is in no KERI specification ([chapter 09, section 5](09-kram-and-request-authentication.md#normative-status)), so the freshness the multiply-endorsed design needs is absent at the specification layer.

### The evidence policy {#evidence-policy}

[code] keripy's `Kramer` passes non-sender attachments through, and each route decides their fate: a route without a `verifyEvidence` policy rejects foreign evidence (keripy peer/exchanging.py, Exchanger.processEvent, L283-287 @94f5423a3). In V2, "Only Grant accepts supplemental grantor evidence." (keripy acdc/ipexing.py, IpexHandler.verifyEvidence, L2232 @94f5423a3). It keeps non-sender signatures only under the endorser's current establishment event, but a verified source seal survives rotation: "A later key rotation does not invalidate that permanent commitment." (L2247-2248). A valid seal displaces the same AID's signatures, and accepted signers and anchorers are indexed by AID in `eidx`. V1 has no policy and refuses. A valid source seal authenticates an `exn` sender on its own, after which an invalid optional sender signature group is tolerated; do not simplify that into a conjunction. The V2 builder signs "only when no sender anchor was created so the wire carries one sender factor." (keripy acdc/ipexing.py, _sign, L437-438 @94f5423a3).

V2 also reads KRAM's acceptance time: "A presentation requirement needs a completed KRAM acceptance." (keripy acdc/ipexing.py, IpexHandler._verifyPresentationAuthGraph, L2181 @94f5423a3), with the receiver time `rdt` as the registry-history cutoff ([chapter 10, section 6](10-presentation-registries.md#rdt-coupling)).

### Tethering {#tethering}

[proposal] The `grant` carries the origin SAID in an origin `o` field, and an ACDC is tethered "when any Grantor AID appears anywhere in the DAG of ACDCs originating at the origin ACDC"; "Tethering implies no other relationship besides fresh (timely) proof-of-control over an AID so tethered." The case is entitlement replay: Cal must know that Bob, not a thief, presents Bob's coupon. V2's set named `tethered` holds registry-authenticated Issuees and is not this; #1613's tethering is unimplemented. [code]

## 9. Multiply endorsed presentation {#multiple-endorsement}

### #1555 and #1556 {#proposal-1555}

[proposal] #1555 lets non-sender AIDs attach signature groups to a single `grant`, under KRAM's timeliness, and puts the signal in the ACDC because "There is no normative cryptographic commitment in an exchange message to a given schema." Its mechanism is a new m-ary edge-group operator, `ME`, on a bespoke origin: each far ACDC must be endorsed by its issuee. #1613 supersedes most of it, but not `ME`. Its companion #1556 makes unary defaults depend on the enclosing group (`NI2I` under `ME`) and adds an `IAND` group defaulting to `E1E`, rather than changing a global default that "might break vLEIs in the wild." A maintainer call has since decided a global `NI2I` default for v1.1 ACDCs ([chapter 05, section 5](05-acdc-and-verifiable-data.md#default-gate)).

### #1613, the current proposal {#proposal-1613}

[proposal] #1613 "solves for the proxy negotiator for another AID use case without needing a new edge operator." It "does not supersede the proposal for a new edge operator" and leaves several AIDs negotiating in concert unsolved. The motive is correlation: a controller uses one AID as proxy "so that this other AID is not disclosed until after contractual protection is in place". The IPEX processor "MUST validate all non-sender endorsements after KRAM" against each endorser's current key state and threshold, preferring a seal source to signatures. Endorsement attaches to the `grant` alone, since "A valid IPEX could consist of only a `grant` message." A non-sender multisig endorser gets no help from KRAM's escrow, so "the Grantor must employ some pre-protocol to collect a threshold-satisfying set of signatures and then attach them to the grant"; the offered mitigation, that proxy and principal share a controller, constrains deployment topology.

### What keripy does with endorsements {#keripy-endorsement}

[code] V2's `grant` generator takes endorsers, "Additional local habitats that sign the same outer exchange as non-sender endorsers (e.g. principal AIDs).", and anchorers (keripy acdc/ipexing.py, _sign, L354-357 @94f5423a3), #1613's shape of a proxy sender and an endorsing principal. The verifier filters and stores endorsements as [section 8](#evidence-policy) describes, then unpacks `_, _, extraSeals = evidence` (keripy acdc/ipexing.py, IpexHandler.verify, L784 @94f5423a3) and discards the signatures: only seals count, and only toward `ax`. #1613's per-Grantor endorsement requirement has no consumer, the multisig pre-protocol is moot in the code, and whether non-sender signatures are threshold-checked is unverified ([question 6](#q-endorsement-signatures)).

### Live co-presence versus durable consent {#copresence-vs-consent}

`ME` needs every issuee online at presentation time, so it does not cover an offline party such as a guardian's dependent. That case closes under plain `I2I` with a consent ACDC between: `bespoke(issuer=A, issuee=V) --I2I--> consent(issuer=B, issuee=A) --I2I--> credential(issuer=HA, issuee=B)`, which A cannot forge because B must issue the consent. This was measured against keripy's v2 code in #1555's comments.

## 10. Anchoring: `ax`, presentation registries, origin-AID anchoring {#anchoring}

This comes from #1613, in neither ACDC branch; all three anchoring legs are [code] in keripy's unwired V2 module.

### The `ax` field {#ax-field}

[proposal] KRAM gives no way "to signal to the IPEX that the relevant messages MUST be perpetually verifiable and hence anchored." `ax` is a boolean in the `a` section of `apply`, `offer` and `grant`. Satisfying it means the Grantor anchors the `grant` and the Applicant anchors `agree` and `admit`. Unlike `dp`, which sits in `q`, `ax` and the origin `o` sit in `a` and do appear in a `grant`.

### `ax` in keripy {#ax-keripy}

[code] Anchoring is negotiated state: replies preserve it, and an `offer` may initiate it but not drop it (keripy acdc/ipexing.py, IpexHandler.verify, L640-647 @94f5423a3); that one-sidedness is an invariant. "Agree and Admit satisfy anchoring directly through their sender." (keripy acdc/ipexing.py, IpexHandler.verify, L652 @94f5423a3), by a seal in the sender's KEL whose digest is the exn's SAID; missing KEL evidence defers rather than refuses. For a grant, "A truthy ax requires one permitted Grant anchorer." (keripy acdc/ipexing.py, IpexHandler.verify, L797 @94f5423a3): any anchoring AID among `candidates = (serder.pre, origin.iseaid, origin.israid)` (L816), the sender or the origin's Issuee or Issuer, including Issuees a presentation registry authenticated. So a grant can satisfy `ax` with no sender anchor. `o` and `ax` are one-item lists on the wire, "until Multi DAG" ([section 11](#dag-soup)).

### An origin `o` on the `offer` {#offer-origin}

[proposal] "The offer message also needs to have an origin `o` field to replace the ACDC field." (keripy PR #1629, review of 2026-08-20, R-053, https://github.com/WebOfTrust/keripy/pull/1629#pullrequestreview-4987948288), naming the metadata ACDC DAG whose rule section the agreent must see before agreeing. Neither branch has it. keripy V2 has it as an optional one-SAID list on the `offer`, and holds the grant to it ([section 4](#offer-fulfillment)). [code]

### Presentation registries {#presentation-registries}

[Chapter 10](10-presentation-registries.md) is their home. An Issuee-controlled registry binds the `grant` SAID, signalled by the issuer through `rd` and `i` in the ACDC's attribute section. V2 will "Verify every presentation registry declared for this disclosure." (keripy acdc/ipexing.py, IpexHandler.verify, L788 @94f5423a3) on every `grant`, reading declarations from `a` only and exempting the origin of an issuance grant, Issuer to Issuee. A binding authenticates its Issuee without an endorsement, where #1613 says such a grant is "always double-authenticated" ([chapter 10, section 7](10-presentation-registries.md#keripy-verifier)). [code] #1613 also floats restricting `rd` in `a` to presentation registries ([question 5](#q-rd-restriction)).

### Auxiliary registry exchanges: `/ipex/dhke` and `/ipex/unblind` {#aux-registry-exchanges}

[proposal] #1740, Sam's draft of 2026-10-30, concerns the Issuer's blindable state registry. It adds two signed `qry`/`rpy` pairs beside an IPEX, kept out of its hash chain so the DHKE is not publicly correlatable: `/ipex/dhke`, agreeing a salt per registry between Issuer and Issuee, and `/ipex/unblind`, by which a verifier holding later `bup` events asks the presenter to unblind them. "This ephemerally binds the auxiliary message pair to the associated IPEX issuance exchange without changing the IPEX exchange messages." (keripy discussion #1740 > Auxiliary Mechanism for DHKE). It adds that "the Disclosee (verifier) MUST NOT send an `admit` message until it has fully verified the state of any ACDCs in the disclosure." (#1740 > Auxiliary Mechanism for Unblinding Registry State), a duty on the sender that keripy has no hook for. Nothing implements either exchange. [code]

The in-band order clashes with keripy: "The Issuer sends the query after its `grant` message." (#1740 > Auxiliary Mechanism for DHKE), so the issuing `bup` follows the grant, but "A grant with rd must carry exactly one node-local registry proof group." (keripy tests/acdc/test_ipexing.py, L5721 @94f5423a3), and V2 refuses one without it ([question 12](#q-dhke-order)). [code]

### Why anchor, and the contractual logic {#contract-logic}

[proposal] Anchoring `agree` proves agreement before disclosure; anchoring `grant` proves "what was granted and, as importantly, what was not granted"; anchoring `admit` "removes plausible deniability regarding the Disclosee's knowledge of the disclosed information and could trigger safe harbor protections." The `agree` binds: "An agree is legally binding not sending an admit does not convey backing out." (keripy PR #1505, comment of 2026-07-17, R-049, https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4997904242). Because the messages are hash-chained, "anchoring the tail also anchors the whole transation including the head" (keripy PR #1505, comment of 2026-07-16, R-050, https://github.com/WebOfTrust/keripy/pull/1505#issuecomment-4996894599), so multiple anchors are contingencies, letting each peer require the other's anchor before its next step without a trusted third party.

### Four tiers of IPEX {#four-tiers}

[proposal] Sam's decision aid (keripy discussion #1512, comment of 2026-07-22, R-062, https://github.com/WebOfTrust/keripy/discussions/1512#discussioncomment-17737728) has four tiers: signed only, where "Only the granted ACDC is itself perpetually verifiable, Not the IPEX transaction"; signed with a presentation registry, letting the presenter detect use of compromised keys; anchored, where "The Agree, and Admit exchange messages are anchored by the Disclosee. The Grant is anchored by the Discloser."; and anchored with a registry, the ACDC requiring anchoring through the `rd` in its attribute section.

### Origin-AID anchoring {#origin-aid-anchoring}

[proposal] With several Grantors, #1613 rules that "either the sender must anchor the grant or the Issuee or Issuer of the origin ACDC of the grant must anchor the grant," in that priority, so the sender can stay out of the disclosed DAG. keripy implements set membership, not priority. [code] The rule is "a loose business logic requirement" below EGF policy: a grant can satisfy `ax` and still be refused by the verifier's own rules, such as one that Bob specifically must anchor.

## 11. DAG soup: the list form, and what remains open {#dag-soup}

### Why it is needed {#why-dag-soup}

[proposal] #1627 argues that when "each have different Issuee, then the presentation must be multiply endorsed", and that several DAGs in one exchange beat a series of IPEXes, which "requires a meta IPEX protocol." With anchoring, signalling by edge operator would need yet another operator, so "the complications of a combination of multiply-endorsed and multiply-anchored presentations may flip the trade-space away from using edge operators as the primary way to signal either or both."

### The list form {#list-form-amendment}

[proposal] #1627's preferred option makes `dp` "a list of a list of tuples," `o` "a list of SAIDs," and `ax` "a list of Booleans," one element per DAG, presented as needed now because "the `dp` field is already a list. So it would be ambiguous". A field-map form with an informative label per DAG is offered as deferrable. dhh1128 endorsed the list form. keripy carries its single-DAG case, so the multi-DAG generalization needs no type change ([section 10](#ax-keripy)). [code]

Position avoids a leak: a meaningful label, sent before terms are agreed, describes the evidence to a disclosee who may walk away, while position discloses only a count. A positional gap, though, cannot say which DAG is missing.

### What the list form does not settle {#list-form-open}

No message carries both `dp` and `o`, so the disclosee's order in an `apply` and the discloser's in a `grant` are unbound, and an `ax` list in an `apply` indexes nothing. Sam's reply on the discussion, that the KEL anchor "only applies when their is not a presentation registry being used by DAG ACDCs", says which obligation falls on which AID, not what the index means. `ax` also binds the `agree` and `admit`, of which there is one each per exchange, so a per-DAG `ax` has no reading for the disclosee's half ([question 3](#q-dag-ordering)).

The "ambiguous" claim may not hold, since each field is type-discriminable with one probe, the argument #1627 uses for the field map. keripy adopted the nested form anyway while `v1.1` says a `dp` value is a list of tuples, so code and branch disagree on its shape. Of the three fields, only `ax` gains a capability from multi-DAG: a negotiated anchoring obligation bound to one body of evidence, which a single bespoke origin cannot express.

## 12. The two SEDI recipes, and the reissuance cascade {#sedi-recipes}

[proposal] #1627's applied section offers a genuine trade. A bespoke origin as recipe forms relationships only at presentation time, so data changes "do not trigger a cascade of reissuance of other ACDCs", at the cost of a bespoke ACDC per presentation and no memorialization of the graph's state. A chained ontology pre-builds the DAG with non-delegative edges (`NI2I` or `E1E`), so "All presentations are just branches of this master recipe." It is simplest for tooling and interop, at the cost of a cascade: changes in upper branches force reissuance below, so volatile data belongs in the leaves. Delegation is not tradeable: "secure delegation requires a DAG that represents the authority structure. A bespoke ACDC can not replace it. The delegation chain is inescapable."

### Which node is the origin {#ontology-origin-tension}

Under the ontology recipe a presentation is a branch whose source is not the ontology's origin, yet anchoring and tethering are stated against "the origin ACDC" of the grant. If the branch root is the origin, who can satisfy `ax` changes with the branch; if the ontology's source must be, every presentation drags the upper graph along. #1627 does not say ([question 2](#q-ontology-origin)).

## 13. Ground-truth matrix {#ground-truth}

keripy at `94f5423a3` unless a cell says otherwise; V2 means `acdc/ipexing.py`, which nothing in `src/keri` calls. Operator rows are in [chapter 05, section 5.1](05-acdc-and-verifiable-data.md#verifying-ground-truth).

| Construct | ACDC `main` | ACDC `v1.1` | Proposed in | keripy |
|---|---|---|---|---|
| One DAG, one origin | absent | present | #1549 | grant must disclose one closed DAG from `a.o[0]` (V2) |
| Bespoke origin | present | present | #1627 | named, not built |
| `dp` paths in `q` | absent | present | #1512, #1542, #1549, PR #1698 | required on `apply`, `offer`, `agree`, `grant`; grant must match the plan exactly (V2) |
| `apply`/`offer` route rows | label lists | `dp` | — | `dp` (V2) |
| Spurn of `grant` | no row | no row | issue #1628 | V2: flow-starting only; V1: any |
| Predecessor table | none | none | — | V1: `agree` before `grant`; V2: `grant` may answer `apply` |
| KRAM | absent from KERI spec | — | KRAM whitepaper, #1613 | see [chapter 09](09-kram-and-request-authentication.md#keripy) |
| Non-sender endorsements | — | — | #1555, #1613 | V2 `grant` keeps current-key signatures and seals across rotation, then discards signatures from the verdict |
| Issuer factor per node | — | — | #1613 | V2: one of registry, KEL seal, current-key signature, as a verdict an unneeded `OR` branch may lose |
| `ax`, origin `o` in `grant` | — | — | #1613 | one-item lists; `grant` anchored by sender or origin Issuee or Issuer (V2) |
| Origin `o` in `offer` | — | — | PR #1629 | optional SAID; grant must keep the Offer's promise (V2) |
| Presentation registry | `rd` in `a` permitted | same | #1095, #1613 | verified on V2 `grant`, issuance origin exempt ([chapter 10](10-presentation-registries.md#keripy-verifier)) |
| Disclosed node's registry state | — | — | #1740 | V2 records in `exrs`, never judges; v1 refuses a revoked far node |
| `/ipex/dhke`, `/ipex/unblind` | — | — | #1740 | absent |
| Tethering | — | — | #1613 | absent |
| `ME`, `IAND`, group-scoped defaults | — | — | #1555, #1556 | absent at `42db8991b`, not re-tested |

Absences last tested at `42db8991b` are not current negatives. The authentication rows are empty in both spec columns and fullest in code keripy's CLI does not load.

## 14. Open questions and known tensions {#open-questions}

### Question 1: Where does the multi-endorsement signal live? {#q-signal-home}

#1555 says the ACDC; #1627 leans toward the `exn`. `ME` is not superseded, so both are live.

### Question 2: Under the ontology recipe, which node is the origin? {#q-ontology-origin}

It fixes who can satisfy `ax` ([section 12](#ontology-origin-tension)).

### Question 3: What binds the DAG ordering across messages? {#q-dag-ordering}

Nothing yet ([section 11](#list-form-open)).

### Question 4: What is KRAM's normative home? {#q-kram-home}

It is load-bearing for sections 8 through 10 and in no specification ([chapter 09, section 9](09-kram-and-request-authentication.md#open-questions)).

### Question 5: Should `rd` in the attribute section be restricted to presentation registries? {#q-rd-restriction}

Disambiguation, the EGF declaring the purpose, breaks nothing, because a presentation registry needs `rd`+`i` in `a` and a non-empty top-level `rd` while the hiding case needs the top-level `rd` absent. Forbidding strikes the spec's method of providing "the `rd` field nested inside either the Attribute or Aggregate section" (ACDC spec > Annex > Bulk-issued Private ACDCs > Basic Bulk Issuance Procedure, L3049 @2362e48a1). #1613 calls the hiding case useless under independent-registry bulk issuance, and pending `kswg-acdc-specification` #204 rebuts it: the Registry SAID "remains, however, a stable identifier for the copy itself, and hence for the context in which that copy is used."

### Question 6: Are endorsement signatures meant to count? {#q-endorsement-signatures}

Either a policy layer reading `eidx` is coming or anchoring has replaced #1613's endorsement requirement ([section 9](#keripy-endorsement)).

### Question 7: What should a validator do with an unrecognized operator token? {#q-unknown-operator}

keripy's two modules now both refuse to read past one, but the v1 site says the refusal "needs S. Smith's buy-in via ACDC #201" (keripy vdr/verifying.py, Verifier.verifyChain, L826 @94f5423a3). Sam assents to the diagnosis that neither branch says: "This seems right." (kswg-acdc-specification issue #201, comment of 2026-07-31, R-031, https://github.com/trustoverip/kswg-acdc-specification/issues/201#issuecomment-5138898171). No remedy is stated ([chapter 05, section 5.1](05-acdc-and-verifiable-data.md#module-disagreement)).

### Question 8: Does `dp` enforcement belong in the verifier? {#q-dp-enforcement}

keripy V2 enforces it there ([section 4](#dp-in-keripy)). Sam's view on a neighboring question is that "each type of use case needs a specific workflow that defines by construction what is disclosed at what stage." (issue #1532, comment of 2026-07-23, R-063, https://github.com/WebOfTrust/keripy/issues/1532#issuecomment-5058749739), which points to EGF workflow tooling; the inference is this chapter's. Whether a SAID-only Offer answered by a different root can succeed is untraced, and KERIA and signify are unchecked.

### Question 9: Is "current keys only" intended for issuer signatures? {#q-current-keys}

If so, rotation silently invalidates every unanchored, registryless ACDC an issuer signed, for IPEX; if not, it is a bug ([section 7](#issuer-factor-every-node)). The same module keeps an endorser's seal across rotation and says why ([section 8](#evidence-policy)); for issuer signatures it gives no reason.

### Question 10: `dp`'s syntax is normative and its only binding is not {#q-dp-normative-seam}

Sam forecasts, assuming an IETF working group, that "IPEX probably gets its own spec" (keripy discussion #1542, comment of 2026-07-30, R-056, https://github.com/WebOfTrust/keripy/discussions/1542#discussioncomment-17841472). [proposal]

### Question 11: Should the route table say a flow-starting grant may be spurned? {#q-spurn-grant}

Sam and V2 say so; the spec has no row and V1 differs ([section 6](#spurn-grant)).

### Question 12: How does #1740's issuance order meet keripy's grant? {#q-dhke-order}

The in-band `bup` follows the `grant`, which keripy V2 then refuses ([section 10](#aux-registry-exchanges)); the out-of-band salt exchange fits. Either the issuance grant may lack its node's registry proof, or keripy must defer it; neither source says which.

## Sources {#sources}

- ACDC spec — Authentic Chained Data Containers (ACDC) specification, Trust Over IP. trustoverip/kswg-acdc-specification, spec/spec-body.md, on two lines; the branch is part of the citation. `main` @`f0bd097de` (2026-08-28) for [spec] claims (route table L1809-1818, Bespoke Issued ACDCs L1860). `v1.1` @`2362e48a1` (2026-09-11) for [spec-next] claims (Disclosure Paths L1809-1986, `dp` in `apply`/`offer` L2013-2019, route table L2004-2009, bulk issuance L3049). Mined in raw/03.
- Dossier spec — KSWG Dossier specification, v0.7 Draft, Trust Over IP. trustoverip/kswg-dossier-specification, spec/dossier-spec-body.md, `main` @`6fcf84127` (2026-10-13): The Dossier as Graph Root (L92-102), Presentation as a Self-Contained Package (L338-351), Threshold Operators (L623-633). Mined in raw/04.
- keripy — KERI reference implementation, WebOfTrust/keripy, src/keri and tests. `main` @`94f5423a3` (2026-10-30) for [code] claims not stamped otherwise (`acdc/ipexing.py`, `acdc/chaining.py`, `peer/exchanging.py`, `vdr/verifying.py`, `cli/commands/ipex/list.py`, `tests/acdc/test_ipexing.py`). `upstream/main` @`b8f60166b` (2026-09-14) for `vc/protocoling.py` (byte-identical at `94f5423a3`). @`42db8991b` (2026-08-25) for the `ME`, `IAND` and group-default absences. The edge-reduction code merged in PR #1681 was written by Daniel Hardman, the corpus's author, so its comments' readings of the ACDC spec are an interested party's. Mined in raw/09, raw/15, raw/16 and raw/21.
- keripy discussions — WebOfTrust/keripy discussions, https://github.com/WebOfTrust/keripy/discussions, by SmithSamuelM; bodies are revised in place, so quote, do not cite by line; snapshots of 2026-09-15, #1740 of 2026-11-03, ruling comments from the raw/21 cache of 2026-10-14. #1512 (R-062), #1542 (R-054 to R-056), #1549, #1555, #1556, #1613 (body says v1.5 2026-08-18), #1617 (R-064), #1627 (last edited 2026-09-11), #1740 (a draft, Sam still adding examples on 2026-11-01), #1095. Mined in raw/09, raw/15, raw/16 and raw/21.
- keripy issues and PRs — WebOfTrust/keripy, https://github.com/WebOfTrust/keripy/issues and https://github.com/WebOfTrust/keripy/pulls, cited for Sam's rulings by comment URL from the raw/21 cache of 2026-10-14 and its scan of 2026-11-03: PR #1170 (R-078), PR #1492 (R-057), PR #1505 (R-049, R-050, R-058), issue #1532 (R-063), issue #1628 (R-051), PR #1629 (R-053), PR #1681 (R-080), PR #1698 (R-052). Mined in raw/21.
- KRAM whitepaper — KERI Request Authentication Mechanism, v0.7.6, Samuel M. Smith. SmithSamuelM/Papers, whitepapers/kram.md, `master` @`67550b477`. Treated in [chapter 09](09-kram-and-request-authentication.md). Mined in raw/15.
- kswg-acdc-specification issues and PRs — trustoverip/kswg-acdc-specification, https://github.com/trustoverip/kswg-acdc-specification/issues. Issue #201 (R-031), mined in raw/21; PR #204 (pending), not mined in a raw note.
