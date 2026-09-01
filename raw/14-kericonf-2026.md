# Doctrine Mining: KERI Conference 2026 talks — Registrar, Observer, bulk updates, usage registries

**Sources:** hand-edited subtitle transcripts of the KERI Conference 2026 talks, `github.com/keri-foundation/CONF26-subtitles`, `subtitles/*.fixed.srt` (49 talks + 14 speaker interviews). Videos with a transcript search at https://keri.foundation/confs/2026/videos/.
**Conference:** Lehi, Utah, 22–23 April 2026 (eve event 21 April).
**Mining date:** 2026-09-01, against CONF26-subtitles HEAD as of that date.
**Regenerate:** `git clone --depth 1 https://github.com/keri-foundation/CONF26-subtitles`, then strip index/timestamp lines from each `.srt` and join the caption text into one flowing paragraph per talk. Grepping the `.srt` files directly is nearly useless — captions break mid-sentence across cue boundaries, so every phrase of interest spans two or three records.

---

## 0. Provenance — read this before quoting anything below

This file is a new provenance class for the corpus, and it needs its own handling rules.

**These are `[SAM-DIRECT]`, and that is why they matter.** `README.md`'s tier scheme notes that the corpus holds only two `[SAM-DIRECT]` instances — the keri.one site material and one personal communication about PQ integration — and that **neither touches registries**. Everything the corpus says about registries, blindable state, and bulk issuance is Sam-as-spec-author, relayed through `raw/03-acdc-spec.md`. The KERIcon talks are the first source in this corpus where Sam speaks about registries in his own voice, unmediated by spec prose. Three talks carry it: *The Digital Identity Tradespace*, *State of the KERI Suite*, and *The Future of KERI*.

**But the text is not his.** These are YouTube auto-generated captions that volunteers have hand-corrected. Three consequences, all of which bite:

1. **Transcription artifacts survive the editing pass.** Real examples from the passages quoted below: "it hosted by a service called registrar", "what are you registries you have?", "observers can't collude between each others". The sense is unambiguous but the words are not exactly his.
2. **The editors interpolate.** Bracketed insertions like "[synchronization]" and "[applause]" are the volunteers' additions, not speech.
3. **Therefore: never attribute a quotation from this file to Sam in public without checking it against the video.** Quote it here as evidence of his framing; verify before it goes into a spec issue, a PR comment, or anything he will read. The corpus's standing rule that only quoted text plus a section anchor is a citation of record applies with extra force to a source whose text is machine-derived.
4. **Talks are undated within the corpus and unversioned.** A talk is a snapshot of April 2026 thinking. Where it conflicts with the ACDC spec at a later commit, the spec wins on normative questions and the talk wins on *intent* questions — which is most of what this file is for.

**Licensing.** `keri-foundation/CONF26-subtitles` and `keri-foundation/recordings-and-subtitles` carry **no LICENSE file**, unlike the Foundation's code repos (`observer`, `witness-hk`, `watcher-hk` are all Apache-2.0). Absent a license, default copyright applies to the recordings and to the transcripts derived from them. Quotation with attribution for commentary is the ordinary scholarly use and is what this file does; wholesale vendoring of the transcripts into this repo is not covered and is not done here. See §7.

---

## 1. Registrar and Observer — the governance split, in Sam's framing

The central claim, and the one the spec does not make explicitly, is that **Registrar/Observer deliberately reproduces the witness/watcher governance structure one layer up**, as a lesson learned rather than a coincidence (*The Digital Identity Tradespace*):

> "The issuer creates a registry of the state of the ACDC, it hosted by a service called registrar, and then an observer, which is controlled by the verifier, the registrar is controlled by the issuer, notice that this models the witness watcher governance structure. So, we learned a lesson. We shouldn't have shared governance. So, we have witnesses that are controlled by controllers, watchers that are controlled by verifiers. We split the verification between two places. We do the same thing with ACDCs. We have registrars controlled by the issuers, and observers controlled by the verifiers, and the ACDC state goes to the observer, the observer gets it from the registrar, the verifier checks the state against the presentation."

"We shouldn't have shared governance" is the load-bearing sentence. The split is not about caching or load; it is the same anti-shared-governance argument that produced watchers, applied to TEL state. Compare `raw/03-acdc-spec.md` §TEL Registrars and TEL Observers (L1693), which gives the mechanism and the no-phone-home property but never says *why the components are divided this way*.

The Observer's job description is deliberately thin (*Tradespace*):

> "All our observer is doing is it's keeping track of the registry state. So, it's asking the registrar, what are you registries you have? What state do you have? And now it has a local cache copy, and then when a verifier wants to verify something, he goes to his observer and says, 'Tell me what the state of this ACDC is.'"

And the distinction from a watcher, from the Q&A in *State of the KERI Suite* — this is the crispest statement of it anywhere:

> "watchers watch the KEL. That's all they watch. They're looking for duplicity in your KEL. Observers are watching the state of issuances that are anchored to the KEL. […] Via the TEL. […] So, it's a TEL observer."

Asked why the two must be separate components rather than one:

> "they have different purposes. So, separation of concerns means you design protocols so that everything has […] it's layered. So, it's a layer, right? They depend on watchers, but they aren't watchers."

**"They depend on watchers, but they aren't watchers"** is worth carrying forward: an Observer's TEL state is only as good as the KEL anchoring it, so an Observer is a consumer of watcher-grade KEL assurance, not a substitute for it. The spec does not state this dependency.

Positioned as new-in-2026 infrastructure (*State of the KERI Suite*):

> "There's two other pieces of infrastructure that are new; that we're building this year: Registrar and Observer. And the reason these are important is that they are how we do this concept what I call control over context."

## 2. Bulk updates — the sync discipline, and why it is not an optimization

The spec mentions "optimized batch synchronization" (L1695) in a performance register. In the talks, batching is a **privacy requirement**, and the reason is stated plainly (*Tradespace*):

> "So for this to work, you want to use bulk updates. That means you don't update instantaneously, you update like say once every 24 hours. Otherwise, if you update it instantly, then the observer could correlate a change to some registries and not others. But if all the registries, 100% of them update at the same clock time, because that's when they broadcast the bulk update, then there's [synchronization] in the time of update."

Generalized in the same talk to a design law:

> "Every time you do anything, if you want to make it so that it's not statistically correlatable, you have to do it in a bulk or herd privacy protected way. You can't do things one-on-one because the act of doing any kind of interaction one-on-one leaks correlatable metadata and it can't be defeated."

From *State of the KERI Suite*, tying batching to the point of validation:

> "The key here is the bulk update. Bulk update means that the observer and the issuer can't correlate back to the point of validation because that's the point of use […] a change in state by the issuer can't be correlated forward because of the bulk update, and the observer's not allowed and doesn't need to communicate to the issuer because they get an update of all the information that they need to do verification. The verification happens at the observer, and observers can't collude between each others if you're using bulk issued credentials."

Note the two directions being closed separately: *backward* correlation (observer → issuer, from a validation to the state change that preceded it) and *forward* correlation (issuer → observer, from a state change to the validations that follow it). The batch window is what breaks both.

**The residual weakness, named by Sam himself** (*Tradespace*) — this is the honest bit a reviewer should quote:

> "The weakness here is that if an observer is malicious and the issuer is malicious, they can collude and the observer can say, 'Did you issue this? Did you change the state of this particular point?' […] but there's no phone home here. The issuer can't force an observer because there's no phone home. Because all it needs is the information in the registry to do the verification. So, there's no built-in mechanism for the observer to trace anything in the system. It requires criminals to get together and form a criminal thing […] There's no technical thing that makes it impossible in this, but what it does is it means that there's no easy way for them to do it."

So the claim is not that collusion is prevented — it is that collusion is *unforced, out-of-band, and legally repressible*, which is the same "technical mechanisms plus legal recourse" posture as the rest of the ACDC privacy story (cf. `bible/06` on three-party exploitation).

## 3. Blinded state and signal whitening

Asked in *State of the KERI Suite* Q&A whether a registrar should inject random noise so a revocation is not a correlatable event, Sam confirmed it is designed in, and gave the scale example:

> "The blinded state TEL, which is the thing that we use — not the current version 1, [which] does not have that — allows you to do updates because they're blinded that don't change the state, they're just there to […] whiten the signal. So, you can as a registrar, you can whiten your signal. You can issue random updates to registries that don't change the state. And so, that means that a state update doesn't necessarily mean the state changed."

> "you could roll out 4 million registries for birth certificates and update them. And then when somebody's born, the fact that there's an update to a registry doesn't correlate to the fact that they were born and you then started using that registry for their birth certificate."

This is the intent behind the spec's mechanical rule that every event increments the blinding factor "regardless of any actual change of state or not" (`raw/03-acdc-spec.md`, §L2135) and behind placeholder decorrelation. The "4 million birth certificates" framing also shows the target deployment scale for the Registrar/Observer pair: state-issued entitlements at population scale, not enterprise credentialing.

Note the explicit version boundary: **blinded-state TEL is not in v1**. A v1-only reading of registries has no signal-whitening story at all.

## 4. Usage registries — where compromise detection actually lives

This is the piece most likely to be misattributed to Observers. Observers cache state; they do not detect compromise. Detection of a *presenter's* key compromise comes from a second registry, controlled by the issuee, in which every presentation is anchored (*The Future of KERI*):

> "let's say someone has stolen my private keys. They can then present my authorization someplace and I don't know that they've stolen my private keys unless I require that a verifier check that the presentation is anchored in my registry. So every time I do a presentation I anchor in the registry. […] if somebody steals my private keys as a presenter, I know that they stole them because the only way that they can gain access is to anchor it in my registry that I control. And so that allows me to detect compromise of my credentials."

The two-registry verification model:

> "if I'm doing a usage registry […] the presentation itself gets anchored in a registry that's controlled by the issuee. So this registrar is the issuee's registrar and now the verifier checks here. So the verifier would have to check two registries; has to check the issuer's registry and the presenter's registry. But that makes it so that both the issuer and the user can detect if either one has been compromised and the verifier knows it."

> "any presentation gets anchored in the issuee's registry and you can see the state of the presentation and you can share one registry for all your presentations because it's one controller of the registry."

Sam is explicit that this is opt-in and costs ephemerality: "Makes the presentation less ephemeral" — an anchored presentation is no longer a bare-signed throwaway, and the presenter chooses it by demanding "ultra security when I present."

Named in *The Digital Identity Tradespace* as the **user presentation registry**, with a novelty claim:

> "We also have something called a user presentation registry, which is also a new thing that nobody else does as far as I've never seen anybody do it, which allows presenters to detect compromise of their proofs that are in their credentials that they're presenting. So they themselves will protect it from fraud, not just the issuer."

**Spec status: thin.** The only trace in the ACDC spec is the `rd` field description, which lists the registry kinds as "Issuance and/or revocation, transfer, retraction, or **usage** registry" (§Top-level fields, L48). There is no usage-registry section. Everything above is talk-only.

Distinguish this cleanly from the *issuer*-side compromise story, which the spec does cover and which is older doctrine: a forger must publish an anchoring seal in the issuer's KEL, so the forgery attempt is detectable, recoverable by rotation if the KEL has not rotated past the forged interaction event, and duplicity if it has (§L1687-1689). Both are "detect compromise via anchoring", applied at the two ends of a presentation.

*The Future of KERI* continues from usage registries into a chained-authorization problem Sam says is in the spec but was not solved this way for the vLEI: what happens to authorizations a delegate issued before the delegate's own authority was revoked. Not mined here; flagged as a thread.

## 5. Ecosystem and implementation status as of the conference

- Registrar and Observer were presented as **things the KERI Foundation is building in 2026**, alongside the donated healthKERI witness/watcher/wallet code that the Foundation debranded and re-released.
- Phil Feairheller (*Infrastructure for Security*) on Locksmith's credential publishing: "we're going to do a lot more with that in the future once the KERI Foundation starts working on observers and registrars. This is just kind of a lightweight version of that."
- Evan Asakawa's mobile-wallet Q&A shows the concept was new to the room: an audience member asks what "observer registrar" is — "Are they just extensions of witnesses and watchers?" — and is told "They monitor a different thing. Those monitor your credentials." Nobody in the exchange could describe the plugin surface, and Evan's answer is "we haven't gone down that road yet."
- Repository status (checked 2026-09-01, outside the transcripts): `keri-foundation/observer` and `keri-foundation/registrar` exist publicly, created and last pushed 2026-02-28, each containing only a LICENSE and a one-line README ("Observer of ACDC state" / "Registrar of ACDC State"). Both are placeholders.
- keripy status (checked 2026-09-01): `src/keri/acdc/registraring.py` is a docstring-only stub — "Registrar service support for managing Registries of ACDC state" — created by Sam on 2026-07-02 in "started stubbing out new v2 ACDC support package", as is `registring.py`. **There is no observer module in keripy.** What does exist is the layer beneath: the blindable `bup` update event and `BlindState` structures (`src/keri/core/structing.py`, `blindate()` in `src/keri/acdc/messaging.py`) and the registry stores `RegBaser`/`WebRegBaser` (`src/keri/acdc/regbasing.py`, `webregbasing.py`).

So: the wire format for what a Registrar would publish and an Observer would cache is partly implemented; neither service is.

## 6. What is NOT in these talks

Worth stating, because the absence is itself information for anyone planning to build one:

- **No wire protocol.** Nothing on how an Observer discovers a Registrar (OOBI?), how it subscribes, what a bulk-update payload looks like, or how sync is authenticated.
- **No trust-establishment story for Observers.** A validator "controls" its Observer by analogy to a watcher, but nothing states how a validator selects, pools, or cross-checks Observers — no analogue of duplicity detection across multiple Observers, and no juror/judge equivalent.
- **No batch-window guidance beyond "say once every 24 hours"**, offered as illustration. The revocation-latency-versus-herd-privacy trade is not analyzed anywhere.
- **No treatment of the grace-period race** that the spec raises at L1695.
- **Nothing on Observer storage cost** at the "4 million registries" scale the same talk invokes.

## 7. Vendoring question

Do not vendor the transcript corpus into this repo. The recordings are the KERI Foundation's, the subtitle repos carry no license, and a verbatim transcript is a reproduction of the speaker's copyrighted speech rather than a new work — the volunteers' editing adds only a thin editorial layer on top. Quoting load-bearing passages with attribution, as this file does, is the ordinary commentary use and is also what the corpus already does with the specs. The regeneration recipe at the top of this file makes the full text reproducible in under a minute, which is a better dependency than a stale copy.

If the full corpus becomes worth holding locally, the clean fix is a license on `keri-foundation/CONF26-subtitles` — the Foundation's code repos are already Apache-2.0, so it is plausibly an oversight rather than a decision.
