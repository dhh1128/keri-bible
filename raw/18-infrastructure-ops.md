# Doctrine Mining: Operating KERI Infrastructure

Primary normative source: `trustoverip/kswg-keri-specification` `spec/spec-body.md`, `main` @`fbdd4a615` (upstream remote, 2026-08-28; the local clone's `origin` is a fork whose `main` is stale at `4df80aa`, so cite `upstream/main`). Used only to state what is normative: §Indirect exchange via witnesses and watchers (L39-49), §Reserve Rotation (L1503), §Dead-Attacks (L1632-1662), §Validator Roles and Event Locality (L1756-1766), §KAWA (L1830-1890), §Out-Of-Band-Introduction (L2627-2860). Searched `upstream/main` and `upstream/v1.1` @`3753f3797` for "mailbox": zero hits on either branch.

Papers (Sam Smith's `SmithSamuelM/Papers`, `master` @`b47f21597`), all [P]:

- `presentations/KERI_Percolation_OOBI.web.pdf`, title slide Invasion Percolation Discovery, OOBIs (Out-Of-Band-Introductions), Spanning Trust Layer, dated "IIW 20201 B" (sic); added in commit `0c1c874` (2021-10-14), never revised. 28 slides.
- `presentations/KERIVerifiableTrustBases.web.pdf`, Verifiable Trust Bases, Renewing the Web of Trust, "version 2.53", 2020/10/20; added `90cbb3a` (2020-10-21).
- `presentations/Hio.web.pdf`, "Hierarchical Asynchronous Coroutines & I/O"; added `f7e5459` (2024-09-10), but several slides carry a 2013 date ("10/25/13") and the content is an assembly of older ioflo/RAET-era material.
- `whitepapers/keridemlia.pdf`, PDF metadata title WIP: Keridemlia White Paper, Ryan W. West and Samuel M. Smith, PDF created 2021-02-26; added `508b287` (2021-04-09). 10 pages.
- `presentations/CensorshipResistance_IIW_2019_B.pdf`, Censorship Resistance of Permissioned Ledgers, Survivability Analysis, Phil Windley and Samuel M. Smith, IIW Fall 2019 (2019/10/01); added `82ee0f3` (2019-10-03). 7 slides.

KERI Foundation repos (`github.com/keri-foundation`, all Apache-2.0, fetched 2026-10-14 through the GitHub API at the pinned commits):

| repo | pin (main) | commit date | what was read |
|---|---|---|---|
| `witness-hk` (package `witopnet`) | `39e1c3fc7` | 2026-09-29 | README, `docs/developer-guide.rst`, `ansible/README.md`, `src/witopnet/core/witnessing.py` (shallow clone) |
| `watcher-hk` (package `watopnet`) | `9be717f8a` | 2026-09-25 | README, `docs/developer-guide.rst`, `src/watopnet/app/watching.py` (shallow clone) |
| `kf-boot` | `14c8f616e` | 2026-09-11 | README, `setup-guide.md`, `docs/developer-guide.rst` |
| `kf-observer` | `d6368aef9` | 2026-10-08 | README |
| `kf-registrar` | `bf14eac4d` | 2026-10-09 | README |
| `observer` | `ffe586bf2` | 2026-02-28 | README (placeholder) |
| `registrar` | `725ed5a67` | 2026-02-28 | README (placeholder) |
| `witness` | `3e73b604b` | 2025-01-24 | listed only |
| `.github` | `68a0d8883` | 2024-07-20 | `profile/README.md` |

Implementation: `WebOfTrust/keripy` `upstream/main` @`927c0cb87` (2026-10-10), read via `git show` for `src/keri/app/indirecting.py`, `src/keri/kering.py`, `src/keri/cli/commands/witness/authenticate.py`, `src/keri/app/agenting.py`.

Web: `https://keri.foundation/` and `/about/services/`, `/faq/`, fetched 2026-10-14 with curl, HTML stripped to text. PyPI JSON API for `witopnet` and `watopnet`, queried 2026-10-14.

Conference captions: `keri-foundation/CONF26-subtitles` @`006042d` (2026-10-04), joined text in `.ignored/conf26/text/`. Talks used: Phil Feairheller, Infrastructure for Security; Ryan Hansen, Witnesses & Watchers (and his hallway interview); Samuel Smith, State of the KERI Suite; Thomas Mayfield, KERI Infrastructure & the 5 W's; Evan Asawaka, Mobile Wallet (Q&A with Phil Feairheller and Karla McKenna); Kent Bull, KERIA Tutorial; Jay Alexander Elliot, Open KERI Infrastructure; Keanu Pahio, KERI Development & Deployment; the closing panel, What KERI allows us to do that we couldn't before. These are the talks the coverage report (`.ignored/coverage-gaps-2026-10.md` §2.2) lists as operations-heavy.

Mining date: 2026-10-14.

---

## 0. Provenance notes, read before citing

Five source classes are mixed in this note, and the ordering between them is the point of the note. The assignment was to keep doctrine and vendor practice apart, so every section below states which class each claim belongs to.

[N] means the KERI specification's standardizing line says it, at `fbdd4a615`. Very little of operations is normative. The spec fixes the roles (witness designated by the controller, watcher chosen by the validator), KAWA's threshold arithmetic, the eclipse-attack obligation on controllers, the witness-as-second-factor pattern, and OOBI/BADA discovery. It says nothing about pool size beyond KAWA's inequality, nothing about geography, vendors, or hosting, and nothing at all about mailboxes.

[P] means a Papers presentation or whitepaper. Three of the five are slide decks, which are terse and sometimes lay out text in an order the extractor scrambles. Quotes from them were taken only from runs that are contiguous in the extracted text. Two typographic ligatures (fi, fl) in the Trust Bases deck are rendered here as plain letters. `keridemlia.pdf` uses a font whose text layer extracts as garbage, so it was OCR'd with tesseract at 200 dpi; its quotes are from the OCR text and each was checked by eye against the page image. Treat its word-level fidelity as one notch below the others.

[K] means code or code-adjacent documentation in a repository at a named commit. A README describing a service is vendor documentation about that vendor's code; I mark it [K] only where I read the code, and [V] (below) where I read only the README.

[V] is a marker this note introduces for vendor or deployment practice: what healthKERI, the KERI Foundation, Veridian, or GLEIF do or say they do. It is not one of the corpus's four tiers. It records a deployment choice, not a protocol rule, and a [V] claim must never be cited as KERI doctrine. Where a vendor's choice instantiates a normative pattern, the two are cited separately.

Conference captions are the fifth class and carry no marker. Per `refresh/prompts/standards.md` §2 they are usable for status and intent only and are never a quotation. In this note a caption excerpt is always introduced with the word caption and set in a code span, never in double quotes, so that it is string-checkable against the caption text without being presented as the speaker's words. Several are secondhand inside the talk (one person reporting what Sam said), and those are flagged as such.

One prior note is directly superseded. `raw/14-kericonf-2026.md` §5 (checked 2026-09-01) recorded `keri-foundation/observer` and `registrar` as one-line placeholders and said neither service is implemented. That was true of those two repos and still is. But two new repos, `kf-observer` and `kf-registrar`, were pushed on 2026-10-08 and 2026-10-09 with substantive READMEs; see §8. raw/14 §5 should be marked superseded in its own text when it is next touched.

---

## 1. The doctrine: infrastructure is separated control over shared data

The oldest statement of the operational architecture in these sources is the 2020 Trust Bases deck, which describes KERI infrastructure as two services under two different controllers. [P] "Shared data = good, shared control = bad." and "KERI = separated control over shared data." (`KERIVerifiableTrustBases.web.pdf`, slide following "Indirect Mode with Ledger Oracles"). The deck's justification for the split is stated as a trade, not a security claim: [P] "Separated control between controllers and validators may provide better decentralization, more flexibility, better scalability, lower cost, higher performance, and more privacy at comparable security." (same slide). The deck labels the two halves "Key Event Promulgation Service" (witnesses) and "Key Event Confirmation Service" (watchers), one designated by the controller and one by the validator (slide "Promulgation and Confirmation Services"). Those labels appear in the extracted text only in scrambled layout, so I cite the slide rather than quote the labels.

The specification states the same split normatively. [N] "The controller chooses how the witnesses are hosted." and, for watchers, "the pool is under the ultimate control of the AID's event validator. To clarify, it is not under the control of the AID's controller." (KERI spec §Indirect exchange via witnesses and watchers, L43, L45 @`fbdd4a615`). The spec names the two networks the deck named: [N] "an AID's witness pool constitutes a highly available and secure promulgation network for that AID" and a validator's watcher pool "constitutes a highly available and secure confirmation network" (L43, L47).

Sam's 2026 restatement is the governance version of the same idea, and raw/14 §1 already carries it from the Tradespace talk, where Sam says the witness/watcher split was a lesson against shared governance. At the conference he made the operational corollary explicit: caption `I'm trying to emphasize that I stands for infrastructure.` and caption `KERI doesn't exist without infrastructure.` (State of the KERI Suite). This is status and intent, not design: the KERI Foundation's stated reason to exist is that nobody adopts a protocol whose infrastructure they must build themselves (caption `nobody wants to build their own infrastructure`, same talk). Ryan Hansen put the security reason in his hallway interview: caption `the witness and watcher network infrastructure is critical for being able to assert and prove that something is true` (INTERVIEW Ryan-Hansen).

What this section establishes for the rest of the note: the split between promulgation (controller's) and confirmation (validator's) infrastructure is [N]. Everything about how many, where, run by whom, and sold how is outside the spec and is either [P] argument or [V] practice.

## 2. The "five Ws" are a program framing, not a protocol concept

The five Ws (wallet, witness, watcher, web, wizard) are the KERI Foundation's organizing frame for its work program. They appear in no specification. Their earliest dated appearance in these sources is the Foundation's GitHub org profile, last committed 2024-07-20: [V] "through the 5 W's: Wallet, Witness, Watcher, Web, and Wizard." (`keri-foundation/.github` `profile/README.md` §Why? @`68a0d8883`). The Foundation's services page attributes the decomposition to Sam and gives one-line definitions: [V] "Wallet – inception and further key management Witness – promulgation of key state Watchers – validation of authoritative key state" and "Web – infrastructure -> 3W leverage it -> API Wizard – Guiderails & bumpers -> 10 page manual" (keri.foundation/about/services/, §Open-source development, under "Reduce complication by: Sam Smith", fetched 2026-10-14). The order matters to that page; it calls them "five consecutive W’s".

The term "One-click KERI" travels with it, and is a goal, not a deliverable: [V] the profile says "we hope to finish One-click-KERI in a year" (§When?, a 2024 statement). At the 2026 conference Sam described the same goal: caption `One click, it'll install KERI infrastructure for you.` (State of the KERI Suite).

The definitions drift between speakers, and the drift is worth recording because a reviewer may meet any of them.

- Web. The services page treats it as the infrastructure layer the first three Ws are reached through ("3W leverage it -> API"). Sam glossed it as simply caption `so it's all on the web`. Thomas Mayfield made it the discovery layer: caption `This is the discovery and transport layer of KERI.`, covering OOBIs, mailboxes and endpoints, and insisted it is transport-agnostic (KERI Infrastructure & the 5 W's).
- Wizard. Services page: "Guiderails & bumpers". Sam: UIs that hide key management, plus a second sense, agent interfaces (the caption sentence carries editor markup, so it is not reproduced; see talks-A.md §2 paraphrase). Mayfield: safe defaults, with the canonical example caption `the majority of users are not going to understand how to set their witness threshold.`
- Watcher. Services page: "validation of authoritative key state". This is broader than the spec's watcher, which detects duplicity and nothing else. Mayfield's gloss is closer to the spec: watchers catch two conflicting versions of a KEL.

Mayfield's claim of independence is a design aspiration worth holding vendors to: caption `Each of these five roles are independently operated, independently verified and uniquely can be independently replaced.` He was presenting Veridian (Cardano Foundation) as an implementation of all five; the Q&A raised whether two organizations building the same five Ws is wasted effort, and Phil Feairheller's answer is the doctrinal reason it is not (§3).

Classification. "Five Ws" is [V] vocabulary from a funding and work program. It maps onto spec roles only partly: wallet is the controller's key-management side, witness and watcher are spec roles, web is OOBI discovery plus transports, and wizard has no protocol content at all. A chapter should present it as the community's map of the deployment problem, not as architecture.

## 3. Witness pools: sizing, placement, and common-mode failure

### 3.1 What is normative

[N] KAWA fixes the arithmetic and nothing else. The controller designates N witnesses and a tally; the guarantee is that "at most one sufficient agreement occurs or none at all" provided "at most F* = N-M of the witnesses are potentially unavailable and at most F < M is duplicitous" (KERI spec §Immunity and Availability, L1866). bible/02 §8 and bible/03 §9 already carry the TOAD bounds and the M > F discipline. The spec says nothing about where witnesses run, who runs them, or how many is enough for a given risk. The phrase "common-mode" occurs once in the spec, and in a different context: reserve rotation keys held by a custodian "may be used to prevent types of common-mode failures without burdening the provisional participants" (§Reserve Rotation, L1503). That is about controller key custody, not witness placement. So the witness-diversity doctrine below has no normative text behind it.

### 3.2 The diversity argument

The argument in Sam's own voice is a 2026 conference statement, and therefore usable here for intent only: caption `Users benefit from witness pools that have no common mode failure sources.` followed by caption `if your witnesses all come from the same vendor, the vendor is a common mode failure source.` (State of the KERI Suite). He tied it to a business-model claim in the same talk (caption `So, we want to incentivize multiple vendors. No single vendor lock-in.`). Phil Feairheller stated the vendor-side consequence in Mayfield's Q&A: caption `we tell our customers, you can't just get your witnesses from us.` and, on Utah's procurement position, caption `They need multiple vendors and the way we synchronize with each other is the KERI protocol.`

This is the right place to say what the argument rests on, because no source states it as a derivation. KAWA's F < M guarantee assumes witness faults are independent. A pool whose N witnesses share one operator, one cloud, one region, or one codebase can fail or be coerced together, so the effective N is one. The doctrine follows from KAWA's assumption, not from any rule KAWA states. That inference is mine; the corpus already names the failure mode ("correlated witness failure (same cloud provider)", bible/02 §9 last paragraph, citing `cr-ad-trust.md` §5).

There is an older antecedent in the Papers repo. The 2019 censorship-resistance deck argues that a permissioned ledger's known validator set is a censorship target ([P] "In a permissioned ledger, because the validator nodes are known, the government could mount a censorship attack against the validator nodes within its jurisdiction", `CensorshipResistance_IIW_2019_B.pdf`, slide 3) and its closing slide, "Mesh Anchoring", diagrams anchoring and re-anchoring the same content across several blockchains (slide 7, a diagram; the only text is the title and "Anchor" / "Re-anchor" labels, OCR at 150 dpi). Its attack list (slide 6) is the same list a witness pool defends against: block writes, block verification, delete anchors, disrupt operation. I record this as lineage, not as doctrine; the deck predates KERI's witness design and is about ledgers.

### 3.3 How many witnesses: there is no normative number

Several numbers circulate, none normative, and the best-attested one is secondhand.

- Sam's recommendation, relayed by Evan Asawaka during his Q&A: caption `It was either one or four cuz he says when you have three or four as your signing threshold for witnesses you can't be eclipsed` (Mobile Wallet). "three or four" is almost certainly the captioner's rendering of "three of four". This is a secondhand report of a spoken recommendation; do not attribute it to Sam in public without the video.
- GLEIF runs five, per Karla McKenna in the same Q&A: caption `That's the same amount of witnesses that GLEIF maintains in the infrastructure` [V], and she said QVIs are required to contribute to that pool. She proposed putting witness-count guidance into the vLEI credential governance frameworks (caption `a recommendation of how many witnesses should be associated with`), which is [V] roadmap, not something any EGF says yet that this pass checked.
- The KERI Foundation's boot service hardcodes the choice: [V] "witness profile is `1-of-1` or `3-of-4`" (`kf-boot` README §Product Rules @`14c8f616e`). Phil Feairheller's healthKERI UI instead lets the user pick N per region and defaults the threshold by the KAWA formula (caption `our user interface will default to the most logical threshold based on the What's the name of that algorithm? The Kawa algorithm.`, Infrastructure for Security).

The 1-or-4 pairing is coherent with KAWA: 3-of-4 is the smallest pool where M > F with F = 1 and one witness may also be down (F* = N - M = 1). One witness is "less secure because one could be compromised" in the same relayed answer. A chapter can state the arithmetic as [N] and the recommendation as reported practice.

### 3.4 Placement as deployed

[V] healthKERI runs four regions, caption `We have New York, Frankfurt, Singapore, and Sydney.`, lets the user place witnesses per region, and spreads witness processes round-robin across hosts within a region (Infrastructure for Security). The KERI Foundation's guides say plainly that a single host is a demo: [V] the setup guide is titled "Set up kf-boot on Ubuntu 24.04 -- Single Host (not very practical)" and says the layout does not "provide geographic or operator separation; production should use" four hosts or more (`kf-boot` `setup-guide.md` §Scope; the source marks "four hosts" with emphasis, so the quote stops before it). Hansen said the same in his talk: caption `We would not say do that in production. It doesn't really give you much help.` and described the production ideal as spreading across providers as well as regions: caption `you could choose from multiple different providers to spread your witness surface out as far as you can` (Witnesses & Watchers).

Multi-vendor in practice: Evan Asawaka demonstrated the desktop wallet rotating in witnesses from two provider plugins on one AID (talks-B.md §9 paraphrase; the caption's own description of the demo is not specific enough to quote). That is the only demonstrated multi-vendor witness pool in these sources.

## 4. Witnesses as a second authentication factor (TOTP)

This is the clearest case in the topic where a vendor feature is a direct instance of normative text, and the bible has the normative half without the instance.

[N] The spec defines the pattern: a witness pool acts as a threshold structure when "each witness only accepts local events that are protected by a unique authentication factor in addition to the controller's signatures on the event", and an attacker would then have to "compromise not merely the controller's set of private key(s) but also the unique second factor on each of a threshold number of witnesses" (§Validator Roles and Event Locality, L1764). bible/03 §9 carries the keripy docstring version of this (`eventing.py:3043-3057`).

[K] keripy ships an instance. `kli witness authenticate` is described as "Perform authentication against an witness to get a OTP code" (`src/keri/cli/commands/witness/authenticate.py`, argparse description @`927c0cb87`), and the receiptor takes "map of witness AIDs to (time,auth) tuples for providing TOTP auth for witnessing" (`src/keri/app/agenting.py`, `WitnessReceiptor` docstring, L62 @`927c0cb87`). Phil Feairheller says he added it: caption `actually I added, to KERI core, at the very beginning of my work at healthKeri, the ability for a two-factor auth for witnesses.` (Infrastructure for Security).

[K] The KERI Foundation witness requires it. [K] "Witnesses are provisioned dynamically via the boot API and secured with TOTP-based two-factor authentication before receipting events." (`witness-hk` README @`39e1c3fc7`). The developer guide's Step 7 reads "Before the witness will receipt events, the controller must register its AID with two-factor authentication" (`docs/developer-guide.rst` §Step 7: Authenticate with TOTP).

The design rationale given is about lock-in, not security: caption `we thought that was more vendor lock-in than we really were comfortable with, so we went with this one-time password solution.` (Infrastructure for Security; the alternative he rejected was a proprietary ESSR-authenticated API). And the usability cost is acknowledged: per-witness codes at four witnesses are caption `really onerous`, so healthKERI offers one batch code for all of an AID's witnesses [V]. A batch code shared across the pool is a weaker second factor than the spec's "unique authentication factor" per witness, because one stolen code then satisfies every witness. That is my analysis, not a source's; it is the kind of trade a chapter should name.

## 5. Non-promiscuous witnesses: one witness per controller AID

[V] healthKERI's witnesses serve exactly one AID each: caption `They are non-promiscuous. They will only witness for the people for the one AID that you reserve them for.` and each has its own keystore (Infrastructure for Security). [K] The open code keeps that shape: a provisioned witness holds "list of controller AIDs this witness serves (currently one)." (`witopnet/core/witnessing.py`, `Witness` class docstring @`39e1c3fc7`), provisioning is `POST /witnesses` with one controller AID in the body (README §Boot server), and the guide notes "it rejects AIDs it does not recognize." (`docs/developer-guide.rst` §Step 7).

Nothing in the spec requires or recommends this. A witness in the spec is a non-transferable AID designated in some controller's KEL; nothing stops one witness AID being designated by many controllers. The arguments for one-per-AID are vendor arguments: isolation (no shared key store), simple scaling, and the "currently one" in the docstring signals it is a present implementation choice rather than a fixed rule. A plausible privacy benefit (a shared witness learns which AIDs share an operator) is not argued in any source I read; recorded as an open question.

## 6. Eclipse attacks

Two different things are called eclipse attacks in these sources, and a chapter should not let them merge.

The spec's eclipse is an attack on a validator. [N] A non-establishment dead attack must reach the validator before the original event does, "This looks like what is commonly known as an [[24](#EclipsAttack)] on a validator." and the obligation falls on the controller: "a controller MUST propagate the event sufficiently widely enough that the attacker cannot eclipse all components, such as Watchers, that the validator may consult." (§Non-establishment Dead-attack, L1638). The defence is time plus breadth: "This may be very difficult given a sufficiently widespread watcher network." (L1652), and witnesses raise the cost further because the attacker must also compromise "a threshold-satisficing number of witnesses protecting that event" (L1638). The general principle is the defender's asymmetry: "a successful dead attack requires the isolation of a validator from ambient sources of the KERL" (§KAWA Security Properties, L1884). bible/02 §9 quotes L1884; the bible has zero hits for "eclipse" (coverage report §2.2, re-checked 2026-10-14 by grep over `bible/`).

The vendor's eclipse is an attack on the witness pool's reachability. Phil Feairheller after placing four witnesses in four regions: caption `So, someone would immediately now have to attack four different places around the world to eclipse` (Infrastructure for Security; the captioner inserted "[attack, red.]" after it). The relayed Sam recommendation in §3.3 is in the same register (3-of-4 cannot be eclipsed). This is a reasonable informal use: an attacker who can isolate a validator from enough witnesses can feed it a forged KEL if the controller's keys are also compromised. But it conflates network isolation of witnesses with the spec's isolation of a validator, and the spec's actual MUST is about propagation to watchers, which geographic witness spread does not by itself satisfy.

What the spec does not do: it gives no quantitative propagation target, no watcher count, and no guidance on how a validator chooses watchers to make eclipse expensive. Geography and operator diversity of watchers (§7) is where the spec's eclipse defence actually lives, and that is entirely [V].

## 7. Watchers and watcher networks as deployed

### 7.1 Normative frame

[N] Watchers are validator-chosen and deliberately off-KEL: "Watchers are not explicitly managed by key events." so that a validator's watcher infrastructure "MAY be kept confidential and, therefore, unknown to potential attackers." (§Indirect exchange, L45). They have an incentive to share: "Watchers have a strong incentive to share all the KELs they watch." because of first-seen, and this "strongly incentivizes both parties to support a widespread low-latency global network of watchers and watcher pools that share their first-seen KELs." (L49). Sam restated the incentive at the conference (caption `There's a huge incentive for watchers to cooperate.`, State of the KERI Suite), and his slide described two parties each with their own witnesses and watchers plus caption `There's a shared watcher network.`

So the spec asks for two things that pull against each other operationally: a validator's own watcher set should be confidential, and watchers should share widely. A shared network that a validator subscribes to satisfies the second and weakens the first, because the network operator knows which AIDs each subscriber watches. No source resolves this.

### 7.2 What the vendors built

[V] healthKERI first rented per-customer watchers, then switched to a pooled network on Sam's advice: caption `He said it's no more secure giving them VMs inside of our infrastructure than if I just created a global watcher network.` and now assigns caption `We do four watchers. So, pick them at random, one in each region.`, in data centres separate from the witnesses (Infrastructure for Security, talk and Q&A). A key-state change triggers a notification to the subscriber.

[V] The KERI Foundation's boot service makes a watcher mandatory: "one hosted watcher is required before onboarding completes" (`kf-boot` README §Product Rules). Note the number: one hosted watcher, against healthKERI's four.

[V] Veridian announced watcher services as roadmap: caption `we are deploying highly available watcher infrastructure services in the second half of this year.` (Mayfield, KERI Infrastructure & the 5 W's).

### 7.3 What the open watcher code does

[K] `watopnet` is a validator-owned watcher that compares an observed AID's witnesses. The README: it "monitors Autonomic Identifiers (AIDs) and verifies key-event consistency across witnesses" and "answers signed key-state queries from authorised controllers" (`watcher-hk` README @`9be717f8a`). The core loop, `Sentinal`, "Detects even, behind, ahead, and duplicitous conditions" by fetching each witness's key state notice (`src/watopnet/app/watching.py`, `Sentinal` docstring, L806-816). On duplicity it logs and stops: the branch is `logger.info(f"{len(dups)} witnesses have a duplicitous event")` followed by `return True` (L967-974).

Negative result, scoped: a search of `watcher-hk/src` at `9be717f8a` for `gossip`, `peer` and `share` found no watcher-to-watcher exchange and no evidence publication. So the open watcher detects duplicity among an AID's witnesses but does not participate in the spec's "global network of watchers" that shares first-seen KELs, and does not act as a juror (no duplicitous event log). It also only sees what the AID's own witnesses serve, so it cannot detect a fork that a compromised controller served to a different audience through a disjoint channel. These are maturity facts at a pin, not defects in a spec sense, and bible/02 §9's candid paragraph on observer immaturity (which `refresh/prompts/standards.md` §4 says is doctrine and stays: "immature observer tooling") is the right place for them.

[K] The dependency is one-way and stated: "Witnesses must exist first." (`watcher-hk` README §Relationship to witopnet).

### 7.4 Local watchers and the wish list

Two deployment patterns surfaced that the spec permits but does not name.

- A local watcher inside the controller's own wallet, watching its own witnesses. [N] The spec already allows it: a validator "MAY use its own watcher pool to watch its own witness pool of the AID that it itself controls" to "detect external attacks on its witnesses" (L45). The closing panel proposed it as the answer to the question of what an ordinary user does when duplicity is found on their key: caption `you should have a local watcher that is informing your wallet of any changes to your key state that you didn't source`, plus a one-button remediation UX (closing panel). The kf-boot README explicitly excludes it from the boot service's scope: [V] "local watcher or sidecar behavior" is listed under "`kf-boot` does not own" (§Scope).
- A server-side sidecar watcher for enterprise relying parties (Phil Feairheller, Infrastructure for Security; detail deferred to his ACDCs for Authorization talk, not mined here).
- An ambient, decorrelated watcher cache was a panelist's wish (caption `an ambient watcher network cache where you can just propagate key state to there`, Nicholas Racz, closing panel). [ROADMAP-wish, not a design.]

bible/02 §9 already records the wtbo.md recommendation that the default watcher be an in-process local resolver, and the "super watcher" scope concern. The global randomly-assigned vendor network of §7.2 is a concrete instance of the scope concentration that paragraph warns about: one operator's watchers cover every subscriber's counterparties.

## 8. The observer layer as deployed (registrar and observer)

raw/14 §1-§6 carries Sam's design intent for Registrar/Observer from the talks. What is new since raw/14's 2026-09-01 check is code-adjacent documentation.

[V] `kf-observer` describes itself in exactly the doctrine's terms: "It is the ACDC counterpart of a watcher. Watchers serve KELs; this process serves TELs." and "Wallets and verifiers must not talk to the registrar — they talk to an observer (anti-correlation). For SEDI, observers are not optional." (`kf-observer` README, intro @`d6368aef9`). It ingests bulk TEL from a registrar, verifies each event against the issuer KEL and "stores a verified copy" (intro), and falls back to a witness's `GET /log` when the bulk feed lacks the issuer KEL (§Running).

[V] `kf-registrar` is "the ACDC counterpart of a witness. Witnesses serve KELs; this process serves TELs." (`kf-registrar` README, intro @`bf14eac4d`). Its external port is "authenticated with KRAM and restricted to configured observer AIDs" (§Dual HTTP), and the README is explicit about what it does not replicate from witnesses: "There is no registrar pool, no TEL receipts" (§Dual HTTP).

Two observations, both mine. First, the registrar keeps an allow-list of observer AIDs, and the observer README says "This node’s AID must be allow-listed on each registrar" (§Running). That makes the registrar-observer relationship permissioned on the registrar's side, which has no analogue in the witness-watcher relationship (any watcher may query any witness). It is a reasonable anti-scraping control, but it means a verifier's choice of observer is constrained by issuers' allow-lists, which cuts against the framing in raw/14 §1 that the observer is controlled by the verifier. Second, "no registrar pool, no TEL receipts" means a TEL currently has no KAWA-style availability or duplicity accountability of its own; its integrity rests on the KEL anchors, which is consistent with Sam's Q&A answer, caption `They depend on watchers, but they aren't watchers` (State of the KERI Suite; raw/14 §1), but its availability rests on one registrar. Neither README was checked against code this pass.

## 9. Mailboxes, and the witness/mailbox conflation

### 9.1 Status: not a spec concept

The KERI specification has no mailbox. A search of `spec/` on both `upstream/main` @`fbdd4a615` and `upstream/v1.1` @`3753f3797` returned zero hits. Everything below is [K] or [V].

### 9.2 What a mailbox is, as the community uses the word

A mailbox is store-and-forward for messages to a controller that is not always online. Kent Bull's definition: caption `Mailbox is a store and forward mechanism.` and the motivating case is a phone that is off (KERIA Tutorial). In KERIA the agent is the mailbox: caption `An agent functions as a mailbox.` (same talk). He was careful that this does not make the agent a witness or watcher: caption `What I'm saying is that the agent is not a witness. The agent is not a watcher.`

### 9.3 The conflation and its history

Two practitioners describe bundling mailboxes into witnesses as an accident.

- Kent Bull: caption `because of an artifact of accident of history, witnesses in the beginning of GLEIF's implementation of the the KERI spec, witnesses and mailboxes were combined.` and caption `HealthKERI actually did witnesses the right way in the sense that it's only a witness.` (KERIA Tutorial).
- Phil Feairheller, answering an audience assumption that offline messages go to witnesses: caption `So that's a common misconception.` then caption `we did make mailboxes a part of the witness deployment simply because we were moving very fast and had nowhere else to hang them` and caption `So, we have since moved away from that.` He said healthKERI now rents standalone mailboxes extracted from keripy's mailbox code (Mobile Wallet Q&A). That is [V].

[K] keripy at `927c0cb87` shows both the separation and the conflation. The role exists separately: `Roles` includes `mailbox` alongside `witness` and `watcher` (`src/keri/kering.py` L378-380, the `Rolage` namedtuple). But `setupWitness` builds a mailbox into every witness, `mbx = mbx if mbx is not None else Mailboxer(name=alias, base=hby.base, temp=hby.temp)` (`src/keri/app/indirecting.py` L62), and the controller-side `MailboxDirector` defaults to `witnesses=True` (L513) and in `addPollers` will "add mailbox pollers for every witness for this prefix identifier" (L621), polling every witness in `hab.kever.wits` as a mailbox in addition to any endpoint authorized in the `mailbox` role (L625-638). So in the reference implementation a witness is a mailbox by default, and a client treats its witnesses as mailboxes by default.

[K] A tension the talks do not mention. The KERI Foundation's witness, which is healthKERI's donated code, still carries a mailbox per witness: its README lists the witness server's job as "KERI event processing, receipting, OOBI resolution, and mailbox services" (`witness-hk` README @`39e1c3fc7`), the developer guide says "Each provisioned witness gets its own non-transferable KERI identifier (Hab), its own keystore, and its own mailbox." (`docs/developer-guide.rst` §Architecture), and the code constructs a `Mailboxer` per witness and serves `qry` with route `mbx` as server-sent events (`witopnet/core/witnessing.py` L497; `witopnet/app/indirecting.py` L280-284). So "did witnesses the right way" and "moved away from that" are true of healthKERI's product offering (standalone rentable mailboxes) but not of the open witness code, which remains witness-plus-mailbox. Either the mailbox is vestigial and harmless, or the role separation the speakers describe is not yet reflected in the code the Foundation distributes. This should go to a maintainer as a question, not into the bible as a defect.

### 9.4 Why the separation matters (doctrine, inferred)

No source states the argument for separation as doctrine; I reconstruct it and mark it as interpretive. A witness is designated in the controller's KEL and is therefore public and tied to the AID. A mailbox holds the controller's inbound traffic. Bundling them means the infrastructure that the controller publishes for availability of its key state also sees who is sending it messages and when, which is metadata the SPAC/ESSR line of work (coverage report §2.1) is trying to protect. It also couples two different availability requirements: a witness must be up for key events to be accepted, while a mailbox must be up for messages to be received. The spec's silence means a chapter can only present this as an argued position, citing Kent and Phil for the history.

## 10. OOBI discovery and percolation

bible/01 §Discovery is separated from trust, bible/06 (Bootstrap Configuration) and bible/07 §2.6 and §8.5 already carry the core: an OOBI is untrusted, BADA authenticates what it leads to. This section adds the operational and historical layer.

[N] The spec's position is that KERI needs no discovery network of its own: "KERI does not, therefore, need its own dedicated discovery network; OOBIs with URLs will do." (§Out-Of-Band-Introduction, L2635). Percolated discovery makes intermediaries untrusted: "Percolation means that each discoverer, in turn, may share what it discovers with any subsequent discoverers." and "Percolating intermediaries do not need to be trusted." (§SPED, L2843). Just-in-time/need-to-know discovery "avoids the need to have a dedicated global infrastructure for the discovery of verifiable data and the associated proofs." (§JIT/NTK Discovery, L2847).

[P] The 2021 Percolation deck is where this was first argued, and it states the result more sharply than the spec does: "KERI End-Verifiability means zero-trust in the percolation path." and "Discovery becomes an availability not a security problem." (`KERI_Percolation_OOBI.web.pdf`, slide "User Permission Percolated Discovery", second of that title). On the next slide: "End-to-end verifiability means any discovery source is as good as any other." and "No need for a globally trusted discovery bootstrap resolver" (slide "Zero Trust Percolated Discovery"). The deck's theory claim is that honest information wins when authenticity gives it an advantage, and that "User permissioning means honest nodes self-isolate dishonest-nodes." (first "User Permissioned (web-of-trust) Percolated Discovery" slide). That last sentence is the deck's stated defence against an eclipse of discovery, and it is a claim from percolation theory, not a demonstrated property of any deployment.

[P] Two lines of the deck matter for §11 and have not reached the spec. SPED "Replaces or Augments User Permissioned DHT" and "Watcher Network may provide super Nodes for aggregated discovery if desirable" (slide "Zero Trust Percolated Discovery"). So in October 2021 Sam treated a DHT as something percolated discovery could augment rather than something it ruled out, and he anticipated watcher networks doubling as discovery aggregators. bible/07 §8.5 records Sam's 2023 objection to describing watchers as "merely discovery mechanisms"; the two are compatible (a watcher may aggregate discovery without that being its security role) but a chapter should cite both.

[N] Operationally relevant parts of the OOBI section the bible does not foreground: the self (blind) OOBI exists for bootstrapping infrastructure, so that a controller's witness AIDs need appear only in its KEL, "Just SOOBIs will do." with the rationale "Redundancy for security is best applied in the context of a self-healing or resilient threshold structure" rather than as unmanaged redundancy in config files (§Self (Blind) OOBI, L2827). And the bounded downside of a hostile OOBI: "an OOBI may be part of a DDOS attack but not as part of a service endpoint cache poison attack." (§OOBI Forwarding, L2831).

[V] The KERI Foundation boot service applies percolated discovery to itself: "clients verify the service by percolated discovery" and "clients do not need preinstalled boot-server inception material" because "signed replies prepend the boot-server KEL" (`kf-boot` README §Transport And Auth). Its business routes are signed `exn` under KRAM, and "This service does not use ESSR." (same section), which is consistent with bible/09.

## 11. KERIdemlia: DHT discovery, and whether it fits the untrusted-discovery doctrine

### 11.1 What the paper proposes [P]

KERIdemlia is a 2021 work-in-progress paper, co-authored by Ryan W. West (first author) and Sam Smith, describing a prototype. It proposes a Kademlia DHT that "stores key state for identifiers, which maps identifiers to witness identifiers and witness identifiers to witness IP addresses" (abstract, p.1) and claims "Keridemlia may serve as an end-verifiable replacement for DNS." (p.3). Its write path is meant to be gated by signatures: "It only allows signed, verified data to be published to the network, discarding all unverified data." (abstract). Concretely it exposes four HTTP endpoints, publish/get for AID-to-key-event-state and for witness-AID-to-IP (Table 1, p.7), and witness IP mappings must carry "a signature from the witness" (p.8).

The paper is candid about the limits of what it stores. It stores a key event state (KES), not the KEL, and says a client must still go to a witness, because "a malicious Keridemlia node could publish false KES data to mislead clients" and "Replaying the KEL also verifies the signatures of each event and allows the caller to detect any dishonesty." (p.8). Its security claim for stored signatures is bounded the right way: storing signatures and returning them "limits attacks by malicious Keridemlia servers to only dropping data entries or denying service." (p.8). And the prototype did not do the verification its design depends on: "It does not completely implement the third step of verifying the authenticity of all data before publishing it to the ledger" (p.8, §Potential Optimizations).

The same design appears a year earlier in the Trust Bases deck as a slide sequence on DHT discovery, with the steps "Resolve Node Prefix to IP Mapping", "Extract Witness Prefixes from Event", "Witness Prefix to IP Mapping", "KERL Query to Witness Node" (`KERIVerifiableTrustBases.web.pdf`, final slides; quoted as step labels, with the deck's fi ligature normalized). So the DHT idea is 2020 Sam, and KERIdemlia is a student-scale prototype of it.

### 11.2 Did it go anywhere?

Not into the spec and not into keripy. [N] The spec's OOBI section chose OOBIs with URLs and says KERI does not need "its own dedicated discovery network" (L2635); the word DHT does not appear in §Out-Of-Band-Introduction. [K] A `git grep -i 'kademlia\|dht'` over keripy `src/` at `927c0cb87` returns one false positive (a base64 string in `eventing.py`). The repository the paper's reference list implies was not found: `ryanwwest/keridemlia` returns 404 from the GitHub API (2026-10-14), and a repo search for `keridemlia` returned nothing. The 2021 Percolation deck repositioned the DHT as something SPED "Replaces or Augments" (§10). I found no later source that revisits it. The paper should be cited as superseded in practice by OOBI/SPED, not as rejected; no source rejects it.

### 11.3 Compatibility with untrusted discovery (analysis, interpretive)

The question the assignment poses is whether a DHT is compatible with KERI's doctrine that discovery is untrusted. My answer, flagged as interpretation rather than any source's position: compatible in principle, and the paper is right about why, but it leaves out the two attacks that matter most for a DHT.

What makes it compatible: nothing a DHT returns is trusted. The paper itself requires KEL replay from a witness after lookup (p.8), which is exactly the spec's rule that information from an OOBI "MUST be verified by some other mechanism" (§OOBI, L2629). Under that rule a DHT is one more untrusted OOBI source, and the Percolation deck's "any discovery source is as good as any other" applies to it.

What the paper does not address:

- Eclipse and Sybil attacks on the DHT itself. Kademlia's routing is known to be vulnerable to an attacker who places many node IDs near a target key and answers lookups for it. The paper's own bound ("only dropping data entries or denying service") is precisely the capability an eclipse needs: denying a validator the original KEL is the precondition for a dead attack (spec L1652, §6 above). So a DHT shifts discovery from a security problem to an availability problem, as the Percolation deck says, but in KERI availability of the original KEL to a validator is itself security-relevant. The spec's mitigation is breadth of watchers, not the discovery layer, so this does not make the DHT unsafe; it means the DHT cannot be the only path.
- Lookup privacy. A global DHT reveals to the nodes on the lookup path which AIDs a querier is resolving and when. The Percolation deck stresses "Privacy preserving or public discovery as needed" and user permissioning, and the spec's JIT/NTK discovery percolates proofs along the path that already exists between exchanger and exchangee. KERIdemlia's only privacy discussion is a comparison with Handshake (p.9). This is the stronger reason, in my reading, that the community moved to percolation: it discloses nothing to third parties that the exchange did not already disclose.

A chapter can present KERIdemlia as the clearest worked example of the doctrine's boundary: a discovery network is admissible only as an untrusted availability layer, and that is a real cost because availability of first-seen history is part of KERI's security.

## 12. Verifiable trust bases and ledger-backed witness networks

[P] The Trust Bases deck (2020, v2.53) is where Sam presented witness pools as pluggable onto very different substrates. Its "Indirect Mode with Ledger Oracles" slide shows the same promulgation/confirmation split with "Ledger Oracle" components on both sides, and the following slides show a root AID whose witness networks are "Internal Witnesses" and "External Witnesses" on "Sovrin", "Indy X", "Ethereum" and "Ledger X" (slide labels; layout-scrambled, so cited by slide rather than quoted as sentences). The deck's root-of-trust claim is the one that makes all of this safe: [P] "End user alone may verify. Zero trust in intervening infrastructure." (slide "KEY Event Based Provenance of Identifiers").

This is the origin of the spec's "backer" (a ledger-registrar alternative to a witness), which bible/02 §8 and bible/03 §9 cover at [N]. What the deck adds for an operations chapter is the multi-level picture: internal delegates for horizontally scaled infrastructure, each with its own witness pool, under a root AID (slides "Horizontally Scaled Infrastructure" and "Multi-layer Multi-Valent Delegation"). That is the design ancestor of the per-AID, per-region pools vendors now sell. No source between 2020 and 2026 that I read describes a deployed ledger-backed witness network; Mayfield's Q&A said Veridian is entirely off-chain (talks-C.md §6 paraphrase).

## 13. hio and the infrastructure software stack

[P] hio is Sam's structured-concurrency runtime, and keripy and the Foundation services run on it. The Hio deck's relevance to operations is its last section, "Zero Trust Computing", which states the security premises the infrastructure is written against: "The network is always hostile, internally & externally; Locality is not trustworthy." and "Every network interaction or data flow must be authenticated and authorized" and "Data is signed/encrypted in motion and at rest." (`Hio.web.pdf`, slide "Diffuse trust perimeter-less security principles").

A terminology collision to flag. The deck's "Locality is not trustworthy" means network position (being inside a perimeter grants nothing). The spec's "local event" means an event "sourced locally on a device under the supervision of the validator or was received via some protected channel using some form of MFA" (§Validator Roles and Event Locality, L1762). These are consistent (spec locality is earned by authentication, not by network position) but a reader skimming both will think they contradict.

[K] The Foundation services are hio programs. kf-boot "runs under one root HIO `Doist`" with Falcon served by an hio HTTP server doer (`kf-boot` README §Runtime Shape). Kent Bull's KERIpy Async Architecture talk is the community's tutorial on the Doist/Doer/DoDoer model (talks-B.md §6); it is not mined further here because it is about programming model, not operations.

Deployment stack [V]: Python 3.14, libsodium, Falcon, nginx TLS termination, Circus under systemd (`kf-boot` setup guide; `witness-hk` `ansible/README.md` §Architecture). Sam's objection to containers is relayed, not argued: caption `Don't tell Sam though because he does not like Docker for this kind of a deployment for security reasons` and caption `Sam's pretty adamant that there's some major security concerns about that approach.` (Hansen, Witnesses & Watchers). No source I read states what the concerns are. This is a gap: a doctrine-level claim, that KERI infrastructure should not be containerized, that exists only as hearsay in one talk.

One oddity in the Foundation's own deployment code, recorded without interpretation. `witness-hk`'s Ansible pilot, which lives in the `witopnet` repository, deploys a process tree ending in "run-keripy-witness.sh → keri runWitness(...)" with "editable checkouts of `keripy` and `hio`" (`ansible/README.md` §Architecture). That reads as running keripy's built-in witness rather than `witopnet`, the package the same repository ships. Hansen's talk reports the audience view that keripy's built-in witness was an early, non-production addition (talks-B.md §2). Which witness the pilot actually runs was not checked; open question.

## 14. The KERI Foundation's operational offerings, as of 2026-10-14

[V] throughout. What exists:

- Open witness (`witness-hk`/`witopnet`), watcher (`watcher-hk`/`watopnet`), and boot/provisioning service (`kf-boot`), all derived from healthKERI's donated code. Sam: caption `HealthKERI had developed Locksmith wallet, watchers and witnesses for their proprietary products.` donated and rebranded (State of the KERI Suite).
- Desktop wallet `locksmith`, plus `fortweb`/`fortios`/`fortoid` wallet builds (repo list, 2026-10-14). Jay Alexander Elliot's argument for the wallet/provider plugin boundary is the Foundation's openness claim: caption `the system may still look open on paper, but it becomes less open in practice` if the wallet is absorbed into one provider's stack (Open KERI Infrastructure).
- New in October 2026: `kf-registrar` and `kf-observer` (§8).
- Hosted test networks were promised: caption `we'll be providing some witness and watcher networks on our own servers so that people who want to test it out can test it out` (State of the KERI Suite). Whether they are live was not checked.

How it is provisioned. The boot service is a private control plane with public data planes: caption `the boot server is private. So it's not publicly accessible.` and caption `But the witness server and the watcher server, those two are public.` (Pahio, KERI Development & Deployment). [V] The witness README says to keep the boot host on localhost: `WITOPNET_BOOT_HOST` defaults to `127.0.0.1` with the note "Keep on localhost in production." (`witness-hk` README §witopnet-sample.sh). The kf-boot onboarding flow allocates the witness pool and a hosted watcher, then the wallet rotates its account AID onto the pool (README §Onboarding Flow).

Packaging claim that does not hold. Both READMEs say `pip install witopnet` / `pip install watopnet` under "From PyPI" (`witness-hk` and `watcher-hk` README §Installation). The PyPI JSON API returned HTTP 404 for both names on 2026-10-14. Hansen and Pahio said in April that they were not yet on PyPI (talks-B.md §2, §4). The README is ahead of the release.

Governance claims on the website. [V] "The chain of all implementations together is as strong as the weakest link. That’s why we certify all code offered." (keri.foundation/about/services/, §Availability and security). No certification process or certified-code list was found on the pages fetched. And the Foundation's reason for separate repos rather than contributing to WebOfTrust: [V] "The KERI Foundation decided to maintain its own repositories to focus more on further maturing the KERISuite" (keri.foundation/faq/, §3. Projects).

Ecosystem recommendations as roadmap: Phil Feairheller expects the Foundation to publish per-ecosystem deployment recommendations (caption `I suspect that KERI Foundation will be a central location for that stuff.`, Mobile Wallet Q&A; see also talks-B.md §9). Nothing of the kind was found in the repos or pages read.

## 15. Open questions

1. Is the per-witness mailbox in `witness-hk` vestigial, or is the open witness still intended to serve as a mailbox? Two speakers described the separation as done; the code at `39e1c3fc7` still bundles it (§9.3).
2. What are Sam's security concerns about containerized witness and watcher deployment? The only source is relayed hearsay (§13).
3. Does any watcher implementation share first-seen KELs or duplicity evidence with other watchers, as the spec's incentive argument assumes? `watopnet` at `9be717f8a` does not (§7.3).
4. How does a validator reconcile the spec's confidential-watcher-set guidance (L45) with subscribing to a vendor's shared watcher network (§7.1)?
5. Is a batch TOTP code across all of an AID's witnesses an acceptable instance of the spec's "unique authentication factor" per witness (§4)?
6. Does one witness per controller AID have a privacy rationale anyone has written down, or is it purely operational (§5)?
7. Why does the registrar allow-list observers, and how does a verifier obtain an observer that every relevant issuer's registrar will serve (§8)?
8. Which witness does the `witness-hk` Ansible pilot deploy, keripy's `runWitness` or `witopnet` (§13)?
9. Witness-count guidance: will the vLEI EGFs carry it, as Karla McKenna proposed, and will the Foundation publish the recommendation Sam reportedly gives (one or four)? Neither exists in a written source this pass found (§3.3).
10. KERIdemlia: was it ever evaluated against Kademlia eclipse/Sybil attacks or lookup privacy, or simply set aside when SPED arrived (§11)?

---

## Already in the bible

- Witness/watcher role split, TOAD bounds, M > F, non-transferable witness AIDs: bible/02-security-model-and-threat-posture.md:140-151 (§8); bible/03-key-management-and-identifier-lifecycle.md:132-144 (§9).
- Witness as second factor via local/remote events, from keripy docstrings: bible/03-key-management-and-identifier-lifecycle.md:142 (§9, "Local versus remote"). Missing: the spec's own L1764 text and the TOTP instance (§4 here).
- Watcher, juror, judge, ambient duplicity detection, the super-is-scope framing, local-resolver default, and the candid immaturity paragraph naming "correlated witness failure (same cloud provider)": bible/02-security-model-and-threat-posture.md:153-173 (§9). Missing: eclipse (zero hits), any deployed watcher network, local watcher in wallet, the open watcher's actual behaviour.
- KERIA agent as mailbox and custody split: bible/03-key-management-and-identifier-lifecycle.md:179-193 (§12). The word "mailbox" does not appear in that section; the role is described as "blind store + relay".
- OOBI untrusted, OOBIs-with-URLs, observer layer is not discovery: bible/07-shibboleths-and-anti-patterns.md:324-332 (§8.5); bible/01-foundations-and-worldview.md:71 (discovery separated from trust); Bootstrap Configuration buckets: bible/06-governance-ecosystems-and-interop.md:117-121.
- Witness/watcher/backer role confusions: bible/07-shibboleths-and-anti-patterns.md:286-322 (§8.1-8.4).
- Registrar/Observer intent and usage registries: raw/14-kericonf-2026.md §1-§6 (not yet in a chapter beyond bible/10).
- Not in the bible at all: five Ws, One-click KERI, pool sizing guidance, geographic or vendor diversity, eclipse attacks, witness TOTP, non-promiscuous witnesses, mailbox as a role and its conflation history, percolation theory's origin, KERIdemlia, Trust Bases ledger-oracle witness networks, hio's zero-trust premises, the Foundation's repos and offerings, Docker position.

## Proposed chapter outline

A new chapter, 11, Infrastructure and Operations. It needs tier markers plus the [V] class from §0, and a status paragraph saying that almost none of it is normative. Proposed sections:

1. Thesis and status. Infrastructure is separated control over shared data; only the role split, KAWA arithmetic, the eclipse obligation, witness-as-second-factor and OOBI/BADA are [N]. Supported by §1 (Trust Bases deck; spec L43-L47) and §0. Cross-link bible/02 §8-§9, bible/06.
2. The roles as operated: promulgation network (witnesses, controller's) and confirmation network (watchers, validator's); registrars and observers one layer up. Supported by §1, §8 (`kf-observer`, `kf-registrar` READMEs). Cross-link bible/02 §9, bible/10, raw/14.
3. The five Ws as a map, not an architecture. Supported by §2 (`.github` profile, services page; Sam, Mayfield captions as intent). Cross-link bible/07 §8.
4. Witness pools: arithmetic, sizing, diversity. KAWA [N]; the common-mode argument as inferred doctrine from KAWA's independence assumption; reported numbers (1-of-1, 3-of-4, five at GLEIF) as [V]. Supported by §3 (spec L1866; kf-boot product rules; captions; censorship deck lineage). Cross-link bible/02 §7-§8.
5. Witnesses as authentication factors: spec L1764, keripy TOTP, witness-hk requirement, the batch-code trade. Supported by §4. Cross-link bible/03 §9.
6. Eclipse attacks: the spec's validator-isolation sense versus the vendor's witness-reachability sense, and why watcher breadth is the actual defence. Supported by §6 (spec L1638, L1652, L1884). Cross-link bible/02 §9.
7. Watchers as deployed: confidential versus shared, vendor networks, what the open watcher does and does not do, local watcher in wallet. Supported by §7 (spec L45, L49; watopnet code; captions). Cross-link bible/02 §9 (super = scope), bible/07 §8.2, §8.5.
8. Mailboxes: not a spec concept; the conflation history; the separation argument as interpretive; the open witness still bundles one. Supported by §9 (keripy `Rolage`, `setupWitness`, `MailboxDirector`; witness-hk docs; captions). Cross-link bible/03 §12, and the SPAC/TSP chapter if one is made (coverage report §2.1).
9. Discovery: OOBI/SPED/JIT-NTK as the chosen design, percolation theory's 2021 statement, and KERIdemlia as the boundary case (a DHT admissible only as an untrusted availability layer; eclipse and lookup-privacy costs). Supported by §10-§11 (spec L2629-L2847; Percolation deck; keridemlia.pdf). Cross-link bible/01, bible/07 §8.5, bible/06 Bootstrap Configuration.
10. Software and hosting: hio's zero-trust premises, bare-metal posture, the unexplained Docker objection, terminology collision on "local". Supported by §13. Cross-link bible/09 (KRAM on the boot service).
11. The KERI Foundation and vendor landscape, dated: repos, pins, what is live, what is promised, what does not hold (PyPI). Supported by §14. This section should carry an explicit as-of date and be the first thing each refresh re-checks.
12. What is established, what is contested, open questions. From §15.

## Proposed sources.yaml entries

Not applied. Shapes follow the existing `gh-repo` and `web` entries. The Papers repo is already present as `smithsamuelm-papers` watching only `whitepapers/kram.md`; the proposal widens its `watch` and `feeds` rather than adding a duplicate, which is a change to a reviewed field and so belongs in the PR body.

```yaml
  # proposed change to the existing entry (reviewed fields: watch, feeds, chapters)
  - id: smithsamuelm-papers
    kind: gh-repo
    repo: SmithSamuelM/Papers
    branch: master
    watch: [whitepapers/kram.md, whitepapers/keridemlia.pdf,
            presentations/KERI_Percolation_OOBI.web.pdf,
            presentations/KERIVerifiableTrustBases.web.pdf,
            presentations/Hio.web.pdf,
            presentations/CensorshipResistance_IIW_2019_B.pdf]
    tier: warm
    branches:
      - {name: master, role: standardizing, marker: "[P]",
         last_scanned: {commit: b47f21597, date: 2026-10-14},
         last_mined:   {commit: b47f21597, date: 2026-10-14}}
    feeds: [raw/15-kram.md, raw/18-infrastructure-ops.md]
    chapters: ["09", "11"]
    caveat: >-
      Five infrastructure PDFs mined 2026-10-14 from the local clone at ~/code/wot/Papers. keridemlia.pdf
      has a broken text layer and was OCR'd; treat its quotes as one notch weaker. The decks are
      2019-2021 except Hio (committed 2024, content partly 2013).

  - id: kf-witness-hk
    kind: gh-repo
    repo: keri-foundation/witness-hk
    branch: main
    watch: [README.md, docs, ansible/README.md, src/witopnet]
    tier: warm
    branches:
      - {name: main, role: standardizing, marker: "[K]",
         last_scanned: {commit: 39e1c3fc7, date: 2026-10-14},
         last_mined:   {commit: 39e1c3fc7, date: 2026-10-14}}
    feeds: [raw/18-infrastructure-ops.md]
    chapters: ["11"]
    caveat: >-
      Vendor code donated by healthKERI. [K] only for what was read in src/; README claims are [V].
      Still bundles a mailbox per witness at this pin (raw/18 §9.3).

  - id: kf-watcher-hk
    kind: gh-repo
    repo: keri-foundation/watcher-hk
    branch: main
    watch: [README.md, docs, src/watopnet]
    tier: warm
    branches:
      - {name: main, role: standardizing, marker: "[K]",
         last_scanned: {commit: 9be717f8a, date: 2026-10-14},
         last_mined:   {commit: 9be717f8a, date: 2026-10-14}}
    feeds: [raw/18-infrastructure-ops.md]
    chapters: ["11"]
    caveat: >-
      No watcher-to-watcher sharing found at this pin (negative search, raw/18 §7.3). Re-check each run.

  - id: kf-boot
    kind: gh-repo
    repo: keri-foundation/kf-boot
    branch: main
    watch: [README.md, setup-guide.md, docs]
    tier: warm
    branches:
      - {name: main, role: standardizing, marker: "[V]",
         last_scanned: {commit: 14c8f616e, date: 2026-10-14},
         last_mined:   {commit: 14c8f616e, date: 2026-10-14}}
    feeds: [raw/18-infrastructure-ops.md]
    chapters: ["11"]
    caveat: >-
      Product rules (1-of-1 or 3-of-4 witnesses, one hosted watcher) are vendor policy, not doctrine.
      [V] is a marker raw/18 introduces; adopting it is a manifest decision.

  - id: kf-observer-registrar
    kind: gh-repo
    repo: keri-foundation/kf-observer
    also: [keri-foundation/kf-registrar]
    branch: main
    watch: [README.md, src]
    tier: hot
    branches:
      - {name: main, role: standardizing, marker: "[V]",
         last_scanned: {commit: d6368aef9, date: 2026-10-14},
         last_mined:   {commit: d6368aef9, date: 2026-10-14}}
    feeds: [raw/18-infrastructure-ops.md, raw/14-kericonf-2026.md]
    chapters: ["10", "11"]
    caveat: >-
      kf-registrar pinned separately at bf14eac4d (2026-10-09). Both repos created October 2026 and
      moving fast; READMEs read, code not read. Supersedes raw/14 §5's "placeholder" status, which
      referred to the older keri-foundation/observer and /registrar repos (still placeholders).

  - id: keri-foundation-web
    kind: web
    urls:
      - https://keri.foundation/
      - https://keri.foundation/about/services/
      - https://keri.foundation/faq/
    tier: cold
    feeds: [raw/18-infrastructure-ops.md]
    chapters: ["11"]
    caveat: >-
      WordPress site; fetched 2026-10-14 with curl and stripped to text. The five Ws definitions on
      /about/services/ are attributed to Sam Smith. Detect by content hash.
```

`conf26-subtitles` needs no new entry, but its `feeds` should add `raw/18-infrastructure-ops.md` and its `last_mined` can be set to `006042d` for the talks listed in the header, since this pass read them at that commit. The `keri-spec` entry's `last_mined` should not move on this note's account: this pass read only the sections listed in the header at `fbdd4a615`, which is already the recorded pin.
