# Doctrine Mining — keripy-knowledge (distilled contributor knowledge base)

**Source root:** `/home/daniel/code/wot/keripy-knowledge/` (the path recorded in earlier passes, `/home/daniel/code/keripy-knowledge/`, no longer exists — the repos moved under `~/code/wot/`). It is a git **worktree** of `~/code/wot/keripy`, not a separate repo; that checkout's `origin` is `dhh1128/keripy`, with `provdev`/`provenant` pointing at `provenant-dev/keripy`. It sits on the orphan branch **`knowledge`**. The KB describes its own home as the fork's orphan branch and adds that it is **"Never pushed to any remote without explicit approval."** (`README.md` §intro, ~L8–10) — so every quote below cites a **private, unpublished** artifact. Nothing here may be presented as a public or citable keripy document.

**Pin: `9489ac9bd`** — "SCOPE: 1.x KB (1.2.13) is now built at ../keripy-1x-knowledge", committed **2026-07-02**, the tip of `knowledge`. **Mined 2026-09-15.** The manifest previously carried pin `unknown` with mining date 2026-06-05; that date cannot have been right, because the note's §8 quotes `92-refresh-2026-06-05.md`, and that file was **added to the repo on 2026-07-02** in commit `d7cea1023` (`git log --diff-filter=A`). The earlier pass therefore read a tree at or after `d7cea1023`; its date was taken from the file's *name*, not from the commit. This is the first genuinely anchored pin.

**Files re-read in full at `9489ac9bd` (2026-09-15):** `SCOPE.md`, `README.md`, `00-lens.md`, `10-map.md`, `20-crosswalk.md`, `30-invariants.md`, `31-landmines.md`, `92-refresh-2026-06-05.md`, `91-validation.md`, `freshness.sh`. **Read only in part:** `PLAN.md` (§7 effort table and §9 open decisions), `PROGRESS.md` (the 2026-07-02 log entries). **Not read:** `90-twin-study.md`, `40-deep-dives/README.md`. Claims below sourced from the unread files are none; where §6/§7 rest on `20-crosswalk.md`/`10-map.md` those files were re-read this pass.

**Nature of source:** an ALREADY-DISTILLED doctrine artifact written for a keripy contributor (Daniel Hardman). It carries three things a synthesizer wants — (a) eight "load-bearing claims" (the worldview reduced to code-decision rules), (b) invariants §A–§J ("the crown jewels" — rules keripy enforces but never announces), (c) landmines L1–L20 (leaky abstractions / traps where a naive change breaks security or wire-interop while tests stay green). Plus a spec-term→code crosswalk and a module map.

**Scope tagging convention (load-bearing for reuse):** the source explicitly tags each item `[protocol]` = version-independent (safe on any keripy line, 1.x or 2.0), vs `[2.0-code]`/`[2.0-wire]` = code-specific and pinned to a keripy commit. This distinction is preserved below because a synthesizer must not treat a 2.0 code detail as an eternal protocol truth. The KB states the legend itself: **"`[protocol]` — true of KERI-the-protocol; version-independent. ... Safe on any line or commit."** (`SCOPE.md` §Tag legend, ~L38–40) and **"`[2.0-wire]` — 2.0 CESR/format/code-table facts ... Line-specific; the 2.0 spec is still moving."** (`SCOPE.md` §Tag legend, ~L41–43).

The source is deliberately written in a **hedged register**: "KERI's real guarantees are conditional; overclaiming costs credibility with a security-skeptic maintainer." (`00-lens.md` §The load-bearing claims intro, ~L11–12). This register is itself doctrine — see anti-pattern section.

---

## 0. Version scope, and the two-step staleness this source imposes on the corpus

**This is the frame for every `[2.0-*]` claim the corpus takes from here. Read it before citing anything below.**

The KB declares a version scope, verbatim: **"This knowledge base describes KERI `2.0.0-dev6`, originally compiled against `keripy@d34a1014` and RE-VERIFIED current as of HEAD `60ab9e08`"** (`SCOPE.md` §opening, ~L3–4). It adds that it **"does not describe the 1.x line."** (`SCOPE.md` §opening, ~L5–6) and that the rule is **"never mix 1.x and 2.0 claims in one file. A 1.x KB, if generated, is a separate tree."** (`SCOPE.md` §The two lines, ~L52–53).

**F-08A — the corpus cites the KB; the KB cites keripy; both hops are stale, and they are stale by different amounts.** Name this when quoting any `[2.0-code]`/`[2.0-wire]` item.

- *Hop 1 (corpus → KB).* The KB's tip is `9489ac9bd`, 2026-07-02. Nothing has been committed to the `knowledge` branch since. So the KB itself has not moved in two and a half months; hop 1 is clean at this pin.
- *Hop 2 (KB → keripy).* The KB's code baseline is keripy `60ab9e08` (2026-07-02). keripy `main` is at `b8f60166b` (2026-09-14), **493 commits later**, and its `__version__` is now **`2.1.0-dev1`** (`src/keri/__init__.py` at `b8f60166b`) against the KB's declared `2.0.0-dev6`. Every `[2.0-code]`/`[2.0-wire]` claim below therefore describes a **superseded dev line**. That is a scope fact, not a doctrine change: none of it is known to be wrong, but none of it may be cited as *current keripy behavior* without re-checking the file at `b8f60166b`. `[protocol]` items are unaffected — the KB's own legend says so.

**F-08B — the KB's own re-verification date is internally impossible, and the commit date is the reliable one.** Every banner in the KB reads "RE-VERIFIED 2026-06-05 @ HEAD `60ab9e08`" (e.g. `31-landmines.md` §banner, ~L3). But `60ab9e08` is dated **2026-07-02** in keripy, so it did not exist on 2026-06-05, and the KB commit that wrote those banners (`d7cea1023`) is also 2026-07-02. The original compilation date is consistent (`d34a1014` is 2026-06-04), so the pattern is that the refresh inherited the build's date label. **Read "2026-06-05" in any KB banner as "2026-07-02".** The 65-commit count `d34a1014..60ab9e08` does check out exactly.

**F-08C — the KB's freshness guard is inoperative on this box, so its "just run `./freshness.sh`" reassurance is not a live check.** `freshness.sh` defaults to `REPO="${1:-/home/daniel/code/keripy}"` (~L7) and `~/.claude/keripy-kb-select.sh`'s registry points at `/home/daniel/code/keripy-knowledge` and `/home/daniel/code/keripy-1x-knowledge` (~L32–33). None of those three paths exists any more; the repos are under `~/code/wot/`. The script errors out rather than reporting staleness. This is an environment fact, not a doctrine fact, but it explains why the KB could sit 493 commits behind without anyone being told.

**F-08D — a sibling 1.x KB exists and has never been mined.** `SCOPE.md` §The two lines records the 1.x line as **"BUILT 2026-06-05 → `../keripy-1x-knowledge`"** (~L48–50). It is real: `/home/daniel/code/wot/keripy-1x-knowledge`, branch `knowledge-1x`, tip `6886ea483` (2026-07-02), carrying its own `00`–`31` tier files plus `92-1x-deltas.md`. The corpus's manifest does not list it. Whether to add it is a manifest decision — proposed, not applied.

**F-08E — the eight load-bearing claims are still an unendorsed draft.** `00-lens.md` carries **"STATUS: DRAFT — needs Daniel's endorsement."** (`00-lens.md` §banner, ~L5) and its endorsement checklist (~L104–113) is entirely unticked at `9489ac9bd`. The claims are the corpus's most-reused material from this source. They are one contributor's distillation of the primer / `background.md` / wtbo / x509-prob, not a ratified statement, and their tier is `[K]`-adjacent at best — **a distillation of primary sources, not itself a primary source**. Where a chapter leans on a lens claim, prefer citing the canonical source the claim cites.

---

## 1. What KERI/ACDC/CESR fundamentally IS and IS NOT (worldview / root of trust)

*Line hints re-anchored at `9489ac9bd`, `00-lens.md` §The load-bearing claims: claim 1 ~L24, claim 2 ~L30, claim 3 ~L38, claim 4 ~L44, claim 5 ~L52, claim 6 ~L60, claim 7 ~L67, claim 8 ~L75. Pre-change checklist ~L87–97; endorsement checklist ~L104–113. All eight claim headings and every quote below were re-read verbatim this pass and are unchanged from the previous pass. Scope banner `[protocol]` at ~L3 — it is new since the earlier mining and confirms the whole file is version-independent.*

**Root of trust = the identifier's own key-event history. No authority.** [protocol]
> "The root of trust is the identifier's own key-event history — no authority." (`00-lens.md`, claim 1)
A verifier establishes "who controls this AID right now" by **replaying its KEL from inception**, not by querying any trusted directory or CA (cites primer §2.2; wtbo §4). Code consequence: a verification path must **never acquire a *trust* dependency on an external service.** Witnesses and OOBIs are sources of **data, never sources of authority** — their output is re-verified locally (background §2.3–2.4). (`00-lens.md` claim 1)

**Detection, not prevention.** [protocol] The canonical slogan:
> "duplicity-evident, not duplicity-resistant." (`00-lens.md`, claim 2 heading)
KERI is a **decentralized key-state *continuity* mechanism, not a consensus protocol, ledger, or global-ordering system** (background §1.1). It does **not** make a malicious controller's fork *impossible*; it makes it **detectable and attributable by observers** (background §4.5, §6; wtbo §4). (`00-lens.md` claim 2)

**Correctness is LOCAL to a validator and observer-dependent.** [protocol]
> "Correctness is **local to a validator** and observer-dependent; a valid KERL is not necessarily unique" (`00-lens.md`, claim 2, cites background §3.3, §7.4)
Code consequence: "never assume 'the protocol guarantees one global history.'" Importing blockchain-consensus expectations is, **in the security model's own words, a *category error*.** (`00-lens.md` claim 2)

**Zero-trust verifier / malicious-controller stance.** [protocol]
> "The controller may be malicious; the verifier assumes nothing." (`00-lens.md`, claim 3 heading)
Verifiers do NOT assume controller honesty — only **cryptographic soundness of signatures and hashes until a key is shown compromised** (background §2.1, assumptions A1/A3). Code consequence: "every externally supplied event, signature, key, receipt, or credential is **hostile input until verified**. Parsing/validation code is adversarial-input code; 'looks well-formed' is not 'is authorized.'" (`00-lens.md` claim 3)

**Identity is sameness across time — bound to a rotating identifier, not to a key.** [protocol]
> "Evidence binds to a rotating identifier, not a key; signatures are anchored and sequenced." (`00-lens.md`, claim 7 heading)
> "Identity is *sameness across time*; a key is not" (`00-lens.md` claim 7, cites x509-prob "lifespans")
ACDC/credential validity is judged against key state **as of the signature's KEL/TEL anchor position**, not against current key state or wall-clock time — "this is what defeats retrograde attacks" (primer §3.3; x509-prob "signatures aren't sequenced"; `was.md`). (`00-lens.md` claim 7)

**Complexity is load-bearing (not incidental).** [protocol]
> "Apparent redundancy — multiple signatures, witness receipts, escrows, pre-rotation, anchoring — is usually encoding a security guarantee that simpler systems cannot offer and cannot retrofit" (`00-lens.md`, claim 6, cites wtbo note [d])
Code consequence: "do not 'simplify away' a guard you don't fully understand; treat an unexplained check as protecting an invariant until proven otherwise." Aligns with maintainer's minimal-surgery ethos — "the smallest correct change, not the cleverest." (`00-lens.md` claim 6)

**keripy is a REFERENCE IMPLEMENTATION; the spec is exogenous.** [protocol → 2.0-wire in specifics]
> "keripy's 'intent layer' is exogenous: the CESR / KERI / ACDC specifications." (`00-lens.md`, claim 5)
keria, signify-ts, and others must interoperate on the wire. "A change that passes keripy's own tests but diverges from the spec/wire format is a **defect**, because it silently breaks interop." CESR code-table entries and sizing, field names and order, SAID derivation, version strings, count codes are **external contracts**. (`00-lens.md` claim 5)

**Crypto agility is designed-in.** [protocol] A new algorithm enters "by claiming an unused CESR code-table slot; non-upgraded parsers still frame the stream correctly (read code → look up length → read bytes)" (primer §4.3; wtbo §3). KERI's quantum posture is **hybrid ECC+PQ multisig plus the hash-hidden next key** (primer §2.5). The Falcon/PQ work is "exercising designed-in agility"; getting the code-table entry and sizing math exactly right is "the highest-risk surface in the flagship." (`00-lens.md` claim 8)

**Canonical sources the KB defers to (read-first, do-not-re-derive):** `papers/keri-primer.md` (worldview, all three layers); `keri-security-analysis/background.md` ("the rigorous, section-numbered security model — the authority for what KERI does and does *not* guarantee"); `papers/wtbo.md` and `papers/x509-prob.md` (PKI contrast, honest tradeoffs). Vocabulary lives in the three spec glossaries. (`00-lens.md` intro)

---

## 2. Security & threat-model positions (survivability, firewall, guarantees-relative-to-assumptions)

**Pre-rotation is the firewall; the next key is the crown jewel.** [protocol]
> "Pre-rotation is the firewall; the next key is the crown jewel." (`00-lens.md`, claim 4 heading)
Each establishment event commits only a **digest of the next key; the key itself stays offline** (primer §2.3). Asymmetry (design property, invariant C2): "**Compromise of *current* keys is survivable; compromise of *pre-rotation* keys is catastrophic and unrecoverable**" (background §3.4–3.5). Code consequence: "never weaken or short-circuit the 'revealed key hashes to the prior commitment' check; never log or persist next-key material where current-key material lives." (`00-lens.md` claim 4; `30-invariants.md` C1/C2)

Invariant C2 verbatim-enough: "Compromise of pre-rotation (next) keys is catastrophic; current-key compromise is survivable. This is a *design property*, not a runtime check — it constrains where next-key material may live." (background §3.4; termdefs *live-attack*/*dead-attack*) (`30-invariants.md` C2) [protocol]

**Guarantees stated relative to explicit assumptions.** The verifier assumes only "cryptographic soundness of signatures and hashes until a key is shown compromised (background §2.1, A1/A3)." (`00-lens.md` claim 3) The whole register is conditional-guarantee, anti-overclaim.

**Retrograde-attack defense = anchor-position validity (invariant H1).** [protocol]
> "An anchored signature/credential is validated against the issuer key state AS OF its KEL anchor's sequence position, not current key state or wall-clock." (`30-invariants.md` H1)
Enforced in `vdr/eventing.py:Tever.verifyAnchor`: `db.kels.getLast(pre, on=seqner.sn)` then `assert eserder.said == saider.qb64` — "the anchor must be the issuer KEL event at exactly that sn." (primer §3.3; x509-prob; `was.md`). WARNING: "the credential `Verifier` does not re-run this — see L15." (`30-invariants.md` H1)

**Witness ≠ watcher (role-boundary as a security position).** [protocol] Invariant D3:
> "A witness is NOT a watcher. A witness may serve a delegate's KEL without the delegator's seal/KEL; a validator must independently obtain the delegator's KEL (OOBI) before validating." (`30-invariants.md` D3; background §2.3, §6; twin #842 `970d2fbc`)
"Witnesses store/serve, they do not vouch for cross-AID anchors." (`31-landmines.md` L4) A validator "must be independently introduced to / OOBI'd with the delegator before it can validate the delegate's KEL." (L4)

**Duplicity detection semantics.** [protocol] "First-seen is immutable and is the basis for duplicity detection. 'The first-seen event is always seen and can never be unseen.'" (`30-invariants.md` E1; termdefs *first-seen*, *duplicity*) "Duplicity = two distinct valid events at the same sn for one AID." (E2) A **valid KERL is not necessarily unique** (B6): duplicate event = same SAID at same sn → merge signatures; different SAID at same sn → duplicity. "Code must never assume 'one global history.'" (`30-invariants.md` B6)

**Recovery / superseding rotation — the ONE narrow exception to first-seen dominance.** [protocol] Invariant C3:
> "Recovery / superseding rotation is the ONE narrow exception where correct witnesses may sign a conflicting establishment event at a seen sn" (`30-invariants.md` C3)
Only a `rot` superseding an `ixn` (no intervening establishment event), linking to the prior event at its sn, and conforming to the pre-rotation commitment. (background §5.5)

---

## 3. Invariants §A–§J (verbatim-enough, with scope tags)

Framing: "Rules keripy maintains but does not announce. Violating one is a security or wire-interop defect **even if tests pass**." (`30-invariants.md` §intro, ~L20–21) Provenance: spec glossaries + `background.md` + P1b subsystem recon. Line numbers "age; verify against HEAD."

*Line hints re-anchored at `9489ac9bd`, `30-invariants.md`: scope banner + §-status table ~L3–18; §A ~L29–64 (A9 ~L59, Falcon shadow-table note ~L53–57); §B ~L66–85; §C ~L87–102 (C1 ~L89, C2 ~L94); §D ~L104–114 (D3 ~L112); §E ~L116–124; §F ~L126–132; §G ~L134–141; §H ~L143–150 (H1 ~L145); §I ~L152–167; §J ~L169–179. Every §A sizing invariant A1–A9, plus C1, C2, C3, D3, E1, F2 and H1, was re-read verbatim this pass and is unchanged.*

**F-08F — the KB's own cross-references between the two T2 files are off by one entry in two places, and this note has silently been correcting them.** `30-invariants.md` E2 says "(See `31-landmines.md` L7 — an out-of-order *first* event at a sn can be mis-flagged as duplicitous.)" (~L123–124), but that landmine is **L8**; L7 is the SAID-overwrite trap. `30-invariants.md` D2 says the `fons` caveat is "see `31-landmines.md` L8" (~L110–111), but the escrowed-`fons` trap is **L13**. `31-landmines.md` itself is self-consistent and its own cross-refs point the right way (L8 §Rule-it-protects cites E2, ~L109). The numbering below follows `31-landmines.md`, which is the authoritative side. Flagging it because a reader who follows the KB's invariant-side pointers lands on the wrong landmine twice.

### §A — CESR wire-format & sizing `[2.0-wire]` (the Falcon-critical layer)
"A new primitive code is an **external contract**. Get the sizing math wrong and a parser that predates your code desyncs the entire stream — silently, because CESR is self-framing (read code → look up length → read bytes)." (`30-invariants.md` §A intro)
- **A1** — Fixed-size codes: `fs % 4 == 0`. qb64 length a multiple of 4 (24-bit alignment). `coring.py:Matter._infil`. Source: CESR termdefs *quadlet*, *self-framing*.
- **A2** — `cs % 4 ≠ 3` where `cs = hs + ss`. "Remainder-3 breaks the pad calculation."
- **A3** — Variable-size codes: `(ls + rs) % 3 == 0` (lead+raw 24-bit aligned for clean round-trip). termdefs *variable-length*, *composability*.
- **A4** — Lead size `ls ∈ {0,1,2}`, computed `ls = (3 - (rize % 3)) % 3`. "The double-modulo is intentional (0→0, 1→2, 2→1). A 'simplification' here breaks triplet alignment."
- **A5** — Raw length must match the code: `len(raw) == ((fs - cs) * 3 // 4) - ls`. "Order of ops matters (`*3//4` before `- ls`)." `Matter._rawSize`.
- **A6** — Special soft (`ss > 0`) ⟹ `fs ≠ None` (special-value soft codes must be fixed-size).
- **A7** — Counters: `hs + ss == fs` always (count codes carry no padding); soft encodes quadlet/triplet count via `intToB64`. `counting.py:Counter`.
- **A8** — Composability round-trip is lossless: `encodeB64(decodeB64(qb64)) == qb64` and qb2 mirror; `Matter.composable` must be `True` for every primitive. "this is the property the whole format rests on." (termdefs *composability*)
- **A9** `[2.0-wire]` — 2.0-dev wire additions (as of `60ab9e08`). A Falcon/PQ PR must also respect: (a) **`BodyUniversalCodex`** (`BUDex_1_0/2_0`) + **`Counter.BUCodes`** for CESR-native body framing (a new body code registers in BOTH — extends L5's shadow-table rule); (b) **GramHead** is now a single soft-code **`'b'`** (`Sizage(hs=1, ss=3, xs=0, fs=8, ls=0)`), replacing old `0P/0Q/0R/0S`; (c) receipt groups use **`TransReceiptIdxSigGroups`** (`-D`/`-N`, indexed-sig-group semantics); (d) use **`Number.onkey`** for ordinal DB keys.

**Falcon shadow-table discipline (§A note, cross-ref L5):** adding a digest/key/sig code also requires updating the *other* tables that shadow `MatterCodex` — `Saider.Digests` and `Serder.Digests` for digest codes, and the relevant `*Dex` sets (`PreDex`, `DigDex`, `SmallVrzDex`/`LargeVrzDex`). "Registering only in `MatterCodex` + `Matter.Sizes` is not enough and fails late/silently."

### §B — KEL structure & key-state `[protocol]` + code-refs
- **B1** — Exactly one inception (sn=0) per AID. A second sn=0 with a different SAID → likely-duplicitous (escrow + raise). (background §3.2)
- **B2** — Sequence numbers strictly increase; no gaps. `rot`/`drt` require `sn == lastEst.s + 1`; out-of-order escrows. (background §3.1–3.2)
- **B3** — Backward/forward hash chaining via prior-SAID `p` field: each non-inception event's `p` must equal previous event's `said`. (termdefs *Verifiable*; background §3.2)
- **B4** — Establishment events gate authority. Current keys come from last establishment event; a message is authorized only if signatures satisfy current `Tholder` threshold. (background §3.4)
- **B5** — SAID derivation: **dummy-then-digest.** The `d` field filled with placeholder chars sized to the digest, whole serialization digested, then field overwritten. "Changing field order/serialization changes the SAID." `serdering.py:Serder.makify/_compute`. (termdefs *SAID/SAD*; primer §3.2)
- **B6** — A valid KERL is not necessarily unique (see §2 above). (background §3.3, §7.4)

### §C — Pre-rotation & recovery `[protocol]` (maximum sensitivity)
- **C1** — Pre-rotation commitment check: on rotation, each revealed signing key, digested with the committed digest's code, must equal the prior next-key digest (`ndiger`) at the matching `ondex`. `eventing.py:exposeds`. "**Never weaken or short-circuit this.**" (termdefs *Pre-rotation*; background §3.5; primer §2.3) — can go permissive on digest-code mismatch, see L6.
- **C2** — (see §2) catastrophic-vs-survivable asymmetry.
- **C3** — (see §2) recovery/superseding rotation, the one narrow exception.
- **C4** — Non-transferable AID constraints: empty next-key digests, empty witness list, empty data. `eventing.py:Kever.incept`.

### §D — Delegation `[protocol]` + code-refs
- **D1** — A delegated event is authorized only by a **seal in the *delegator's* KEL.** Validation locates the anchoring event via the seal source couple `(delseqner = sn, delsaider = SAID)`. `Kever.validateDelegation`.
- **D2** — The delegating event must be **first-seen in the delegator's KEL before the delegate event is accepted** (checked against `db.fons`). Caveat: relies on `fons` presence — could be merely escrowed (L8/L13).
- **D3** — (see §2) A witness is NOT a watcher.

### §E — Duplicity & first-seen `[protocol]` + code-refs
- **E1** — First-seen is immutable, basis for duplicity detection. Append-only. (termdefs *first-seen*, *duplicity*)
- **E2** — Duplicity = two distinct valid events at the same sn for one AID; conflicting SAID → escrow + `LikelyDuplicitousError`. (out-of-order ≠ duplicitous — L8)

### §F — Witness threshold (TOAD) `[protocol]`
- **F1** — TOAD bounds: non-empty witness list ⟹ `1 ≤ toad ≤ len(wits)`; empty ⟹ `toad == 0`. (background §4.2, §5.3, `M`/toad)
- **F2** — **Sufficient agreement = receipts meeting TOAD, not all witnesses.** "This is the spec rule; keripy's `WitnessReceiptor` currently waits for ALL witnesses instead — that is a defect, not the invariant." (see L9)

### §G — Key management (keeping) `[2.0-code]`
- **G1** — Deterministic salty derivation: a key is reproducible from `(salt, path, tier)` via Argon2; `path = stem + hex(ridx) + hex(kidx)`. `keeping.py:SaltyCreator.create`. "The missing delimiter is a recovery-breaking landmine" (L10, twin #928).
- **G2** — Key-state advances atomically (old → new → nxt) and erases old on advance. "Advance happens *before* the rotation event is validated — recovery requires `replay(advance=False)` on rejection." (L11)

### §H — Anchored signatures `[protocol]` (credential / TEL layer)
- **H1** — (see §2) anchor-position validity; the retrograde-attack defense. WARNING credential `Verifier` gap (L15).

### §I — Storage / DB (basing, dbing) `[2.0-code]`
- **I1** — The FEL is strictly append-only. `.fels` maps first-seen ordinal `fn → dig`, never mutated/deleted; immutable basis for replay & duplicity.
- **I2** — Ordinal keys sort numerically only because of fixed-width zero-padded hex. `snKey/fnKey` encode `sn` as `{sn:032x}`; "the 32-char zero-pad makes lexical order == numeric order. A naive width change silently corrupts ordering."
- **I3** — Set writes (IoSet/IoDup) are idempotent. `put`/`add` of an existing `(key,val)` is a no-op returning `False`; "callers must not treat `False` as an error."
- **I4** — Escrows are transient and discardable across migrations. First migration clears all escrows via low-level `.trim()` (bypassing key parsing). (twin #863; L2)
- **I5** — Delegation seal source couples persist in `.aess` (`dgKey → (Number, Diger)` = delegating event's sn + SAID). The store open twin **#1317** says a delegatee's witness fails to populate.

### §J — Credential / TEL (vdr) `[protocol]` + code-refs
- **J1** — Anchor-to-KEL (H1 at the TEL layer). Registry/issuance/revocation events must anchor to issuer's KEL at recorded sn; `Tever.verifyAnchor` enforces.
- **J2** — TEL ordering: iss/rev chain to the prior TEL event (sn-1). "Cannot issue a credential twice or revoke an unissued one; the new event's `p` must match the stored prior."
- **J3** — **An ACDC SAID is computed over its most-compact form**, not its uncompacted serialization, "so the SAID is stable across compaction/disclosure." `vc/proving.py` (`Saider.saidify`).
- **J4** — Backer issuance/revocation (bis/brv) require ≥ TOAD backer signatures; plain iss/rev rely on the KEL anchor only. `Tever.valAnchorBigs`.

---

## 4. Landmines L1–L20 (anti-patterns / traps; all `[2.0-code]`)

Framing: "Leaky abstractions, hardcoded assumptions, and 'looks generic but isn't' traps. A naive change near one of these breaks security or wire-interop while tests stay green." (`31-landmines.md` §intro, ~L7–9) The file's banner claims "All L1–L20 confirmed still present and valid (none fixed in the 65-commit delta)." (`31-landmines.md` §banner, ~L3–4) — true at keripy `60ab9e08`, **not** re-tested at `b8f60166b`. Scope for the whole file is `[2.0-code]`, so §0's hop-2 staleness applies to every entry.

*Line hints re-anchored at `9489ac9bd`, `31-landmines.md`: L1 ~L16, L2 ~L28, L3 ~L42, L4 ~L56, L5 ~L77, L6 ~L90, L7 ~L98, L8 ~L104, L9 ~L112, L10 ~L119, L11 ~L125, L12 ~L133, L13 ~L140, L14 ~L145, L15 ~L151, L16 ~L162, L17 ~L168, L18 ~L174, L19 ~L181, L20 ~L187. L1, L5, L6, L7, L9, L15, L16, L17, L18 were re-read verbatim this pass.*

**F-08G — the PQ urgency framing around L1/L5/L6 is out of date, though the discipline itself stands. `[2.0-code]`, scope correction 2026-09-15.** These three entries are the note's most-cited material (`bible/03`, `bible/04`, `bible/06`, `keri-doctrine.md`), and they are written as advice about **work in flight** — "The Falcon PR must touch every shadow table" (`31-landmines.md` L5, ~L83–84). At keripy `b8f60166b` there are **no post-quantum codes in keripy at all**: a search of `src/` for FN-DSA, ML-DSA, SLH-DSA, Dilithium, Falcon, SPHINCS, Kyber and ML-KEM returns only the `falcon` **web framework** (`app/httping.py`, `app/indirecting.py`, `app/oobiing.py`, `app/signaling.py`, `app/specing.py`, `core/routing.py`, `end/ending.py`); `src/keri/core/` has zero matches. Cross-referenced from `raw/09`, which owns the keripy-side claim and also found none on CESR `main` — the PQ code table exists only on the CESR `v1.1` branch and an unmerged signify-ts fork branch. The KB is candid about why the work has not started: its own open decision asks which of two conflicting in-repo Falcon designs is canonical — **"`falcon-impl-plan.md` fixed-size sigs + `b/c/d/e` + `1AAQ/1AAR`, no digest-AIDs; vs `prompt-falcon-pr.md` variable-size sigs + digest-AID `e/f/g/h`"** (`PLAN.md` §9 Decisions to confirm at approval, ~L189–190), and it defers the flagship entirely: "P5 | Flagship (Falcon/PQ) ... **Prereq:** resolve the two conflicting Falcon spec docs first." (`PLAN.md` §7 effort table, ~L170). **So: the shadow-table discipline is unaffected and remains correct as forward-looking advice. The framing that a Falcon PR is imminent, and that L1 is "directly blocking" it, is not — nothing is blocked because nothing has been written.** Chapters citing L1/L5/L6 should keep the discipline and drop the urgency.

- **L1 — `Ed25519N` hardcoded as prefix code for *any* non-transferable AID.** `habbing.py:Hab.incept` line 2931 & `GroupHab.incept` line 3728. When `transferable=False`, sets `code = MtrDex.Ed25519N` regardless of actual signing key type. Correct for Ed25519, wrong for Falcon (needs digest-based prefix). KEY DOCTRINE: "**Non-transferability in KERI is expressed by an empty next-key commitment (`ncount=0`, `nsith='0'`), not by a special prefix code**" — except where a basic non-transferable code like `Ed25519N` legitimately carries the key itself. Intersects spec rule: witness/backer AIDs MUST be non-transferable. **Directly blocks Falcon non-transferable AIDs.** (Falcon plan Stage 3)

- **L2 — DB key formats are version-dependent; high-level iterators crash on old formats.** `db/basing.py`. Pre-1.2.0 `qnfs`/escrow keys lack the insertion-order suffix (`PRE.SAID` vs `PRE.SAID.00000000`); suffix-parsing iterators do `int(SAID,16)` → `ValueError`. Fix `_trimAllEscrows()` clears all **22 escrow DBs** via low-level `.trim()`. Rule: "never iterate version-mismatched DB keys with format-assuming iterators; treat escrow contents as discardable across migrations." (twin #863, `3eb1b679`)

- **L3 — `wits=[]` into witness-selection paths → `random.choice([])` IndexError.** `cli/commands/ipex/admit.py`. Passing `hab.kevers[issr].wits` sends empty list when issuer has no witnesses. Fix passes `pre=issr` so endpoints resolve via `hab.endsFor(pre=pre)`. Rule: "for queries, resolve endpoints by `pre=` (endsFor), not by random selection from a possibly-empty `wits` list." (twin #1160, `bce397bc`; family: open twin #865)

- **L4 — A witness is NOT a watcher (see §2/D3).** `eventing.py:Kever.valSigsWigsDel`. A witness may return a delegated AID's KEL without the authorizing event-source-seal couple and without the delegator's KEL. "Code that assumes a witness performs watcher functionality ... will fail." Open twins **#1317**, **#846**. (twins #842/#975, `970d2fbc`)

- **L5 — Digest/key/sig codes live in *multiple* tables; registering one isn't enough (Falcon).** `coring.py` `MatterCodex`+`Matter.Sizes`, ALSO `Saider.Digests`, `Serder.Digests` (serdering.py), and `*Dex` sets (`PreDex`, `DigDex`, `SmallVrzDex`/`LargeVrzDex`). A code comment near `coring.py:460` literally says "when add new to DigCodes update Saider.Digests and Serder.Digests." Add a code only to `MatterCodex`+`Sizes` → round-trips as primitive but invisible to SAID derivation / prefix validation → "fails late and silently. The Falcon PR must touch every shadow table." **2.0 update:** now also applies to **`BodyUniversalCodex`** — register in both `BUDex` and `Counter.BUCodes`. GramHead's old `0P/0Q/0R/0S` shadow case is gone.

- **L6 — Pre-rotation verification can go *permissive* on a digest-code mismatch ⚠ HIGH.** `eventing.py:exposeds` — `Diger(ser=verfer.qb64b, code=diger.code)`. The revealed key is re-digested using the *committed* digest's code; if that code is wrong/mismatched, recomputed digest won't match and the `ondex` is "**silently excluded from threshold satisfaction** rather than failing closed — weakening the pre-rotation check (the firewall, C1). New digest codes (Falcon/PQ) widen this surface."

- **L7 — SAID overwrite doesn't validate the digest code against the message ⚠ HIGH.** `serdering.py:Serder._compute`. SAID field overwritten from raw bytes; if code ∉ `DigDex` or dummied span mismatches, it can silently skip — "a wrong digest code yields an invalid SAID with no error." Pairs with L5.

- **L8 — An out-of-order *first* event at a sn can be mis-flagged as duplicitous ⚠ HIGH.** `eventing.py:Kevery.processEvent`. Duplicity detection compares incoming SAID to `db.kels.getLast(pre, sn)`; if no prior event at that sn (e.g. out-of-order sn=100 arrives first), `getLast` returns `None` and the check can raise `LikelyDuplicitousError` instead of escrowing as out-of-order. Rule: "duplicity = conflicting events at a *seen* sn (E2); out-of-order ≠ duplicitous."

- **L9 — Receipting waits for ALL witnesses, not TOAD → blocks on any witness downtime.** `app/agenting.py:WitnessReceiptor.receiptDo` — `completed = len(wigers) == len(wits)`; loops `while len(wigers) != len(wits)`; no reference to `hab.kever.toader`. "Spec says sufficient agreement = TOAD receipts (F2); waiting for the full set blocks indefinitely if a single witness is down or slow. **Likely root of open twins #855 and #912.**"

- **L10 — Salty key path has no delimiter → seed collisions (recovery break).** `keeping.py:SaltyCreator.create` — `path = f"{stem}{ridx:x}{kidx+i:x}"`. No separator; "when `stem` ends in a hex digit, distinct `(stem,ridx,kidx)` tuples can map to the same path → same derived seed." Confirms **twin #928** (Signify Salty path delimiters → recovery break).

- **L11 — Keystore advances + erases old keys BEFORE the rotation event is validated.** `keeping.py:Manager.rotate/replay`; `habbing.py` Hab.rotate comment. `mgr.rotate()`/`replay(advance=True)` mutate `PreSit` (old→new→nxt) and erase old private keys before `Kever.processEvent` validates. "On rejection you need an explicit `replay(advance=False)` recovery; a naive caller can strand the keystore ahead of the KEL." (cross-ref G2)

- **L12 — Delegated inception has no confirmation loop; assumes delegator KEL already present.** `habbing.py` silences `MissingSignatureError` on delegated incept; confirmation marked TODO. "If the delegator's anchoring event arrives later, the dual-seal can be out of order with no retry/confirm. **Plausibly underlies open twin #1087** (`kli delegate confirm` hangs)." (cross-ref L4, D1–D3)

- **L13 — `validateDelegation` trusts `db.fons` even if the delegating event is only escrowed.** `eventing.py:validateDelegation`. "A `db.fons` entry for the delegator's event may exist while that event is still in a partial-signature escrow (PSE), falsely validating the delegate."

- **L14 — Indexed-signature code silently switches at index ≥ 63 (multisig).** `signing.py` Siger code selection (`Ed25519_Crt_Sig` vs `Ed25519_Big_Crt_Sig`) keyed on hardcoded `index < 63` threshold. "A group/rotation with >63 keys changes the Siger encoding; consumers that don't handle the 'big' indexed codes may reject."

- **L15 — Credential `Verifier` may not re-validate the anchor against the issuer's KEL ⚠ HIGH (verify!).** `vdr/verifying.py:Verifier.processCredential`. Checks TEL registry existence + credential state (iss/rev) + schema + chain edges, but recon found **no call to `Tever.verifyAnchor`** here — anchor validation appears to happen only in `Tevery` when a TEL *event* is received, not when a credential + proof is verified. "A credential presented with a forged `(seqner, saider)` proof could pass schema + TEL-state checks without the anchor being confirmed against the issuer's actual KEL at that sn — undermining invariant H1." Explicitly flagged as a **recon hypothesis with uncertainty** (confidence medium) — confirm by tracing upstream TEL ingest.

- **L16 — ACDC edge operator semantics (`&&`/`||`) are not enforced (#885).** ~~`vdr/verifying.py` edge loop; operator read but unused. "Chained-credential validation checks each source credential's iss/rev state but does not apply the edge operator (`&&` = all sources valid, `||` = at least one)."~~ Open twin **#885**. The quoted text is still present in the KB at `9489ac9bd` (`31-landmines.md` L16, ~L162–166) — **SUPERSEDED as a description of keripy 2026-09-15; right in substance, wrong in mechanism, and wrong about which operators exist.** See F-08H below.

- **L17 — Edge/provenance DAG acyclicity & NI2I chaining not validated (#1040).** ~~`vdr/verifying.py:verifyChain`. "No observable check that edge chains are acyclic / well-formed; NI2I (non-issuer-to-issuee) operator usage isn't fully validated."~~ Open twin **#1040** (`NI2I` in `kli vc create` never completes). Still present in the KB at `9489ac9bd` (`31-landmines.md` L17, ~L168–172) — **partially SUPERSEDED 2026-09-15**: NI2I is now handled explicitly. The acyclicity half is not re-verified this pass and stands unchallenged. See F-08H.

**F-08H — the L16/L17 edge-operator landmines are superseded as of keripy `b8f60166b` (2026-09-14). `[2.0-code]` → the KB's statement is now historical.** The KB's substance survives — **DI2I is still unimplemented** — but three things it says about the mechanism are no longer true, and the corpus has been citing the mechanism.

1. **The operator vocabulary is wrong.** The KB describes boolean combinators, "`&&` = all sources valid, `||` = at least one" (L16, ~L165–166), and `10-map.md` repeats it (~L84–85). keripy's model is a set of **unary per-edge operators**: `UnaryOps = ('I2I', 'NI2I', 'DI2I', 'E1E', 'NOT')` (`src/keri/vdr/verifying.py`, L41 at `b8f60166b`). There are five, not two, and they constrain the issuer/issuee relation rather than combining source validity.
2. **"Read but unused" is wrong.** I2I and E1E are **enforced**; NI2I is a no-op binding check.
3. **"Not enforced" is wrong in the direction that matters most.** DI2I and NOT are not dropped — they **fail closed**, deliberately and with a diagnosable error, and the source says so in as many words: **"they fail closed diagnosably instead of being dropped and silently defaulting."** (`src/keri/vdr/verifying.py` §`UnaryOps` comment, ~L38–39 at `b8f60166b`). Both raise `ValidationError`, not `NotImplementedError`, and the code explains the choice: "Deliberately not a MissingChainError: the chain is present and retrying cannot help" (~L443–444). `E1E` is flagged in-source as "a keripy extension not yet in the spec's normative operator table" (~L40). The edge `s` constraint is now enforced too.

The keripy-side claims belong to `raw/09` and were cross-referenced against it; this note owns only the fact that **the KB's statement of them is dated**. The practical effect: a "the prose says X, the code does Y" argument built on L16 now points the wrong way — the code is *ahead* of the KB, and ahead of the spec on E1E. Nothing here has been fixed in the KB itself; `31-landmines.md` at `9489ac9bd` still reads as originally written.

- **L18 — `Komer` records have no schema versioning → adding a field breaks old stores.** `db/koming.py:Komer`; `KeyStateRecord`, `HabitatRecord`. Dataclass-backed, no migration/versioning; adding a field can fail to deserialize pre-existing entries. "Any new field on a persisted record needs a migration."

- **L19 — `getVal`/`Suber.get` return `None` on miss — can't distinguish 'absent' from 'empty'.** `dbing.py:getVal`; `subing.py:Suber.get`. "`if (val := db.get(k)):` is falsey for both a missing key and a stored empty/falsey value." Truthiness branching silently mis-handles the empty case.

- **L20 — `.fons` vs `.qnfs` lookup ambiguity (#847).** `db/basing.py` (`.fons` = `dgKey → fn`, `.qnfs` = queued-not-first-seen). "Code resolving an event's first-seen ordinal via `.fons[dgKey]` without falling back to `.qnfs`/`.fels` can miss still-queued events." Intertwined with pre-1.2.0 `qnfs` key-format issue (L2). Twin **#847**.

---

## 5. Anti-patterns / outsider-tells / PKI-and-blockchain misconceptions the KB corrects

- **PKI/CA reflex → "query a trusted directory/CA":** WRONG. Root of trust is the KEL replay; "a verification path must never acquire a *trust* dependency on an external service." Witnesses/OOBIs = data, not authority. (claim 1)
- **X.509 "a key = an identity" reflex:** WRONG. "Identity is *sameness across time*; a key is not." Evidence binds to a rotating identifier. (claim 7, x509-prob "lifespans")
- **Validate a signature against *current* key state:** WRONG (retrograde attack). Validate against key state as of the anchor's sequence position. "signatures aren't sequenced" is the X.509 flaw KERI fixes. (claim 7; H1)
- **Blockchain/consensus reflex → "the protocol guarantees one global history/ordering":** explicitly a **"category error."** KERI is continuity, not consensus; a valid KERL is not necessarily unique; correctness is local + observer-dependent. (claim 2; B6)
- **"Prevent forks / duplicity-resistant":** WRONG framing. KERI is duplicity-**evident**, detection-not-prevention; forks are made detectable & attributable, not impossible. (claim 2)
- **Trust the controller / assume honesty:** WRONG. Malicious-controller stance; every external input is hostile until verified. "'looks well-formed' is not 'is authorized.'" (claim 3)
- **"Simplify away" redundant-looking guards:** WRONG. Complexity is load-bearing; an unexplained check protects an invariant until proven otherwise. (claim 6)
- **Passing keripy's own tests = correct:** WRONG when the wire/spec diverges — that is a defect (interop break). Spec is the external contract. (claim 5)
- **Non-transferability via a special prefix code:** WRONG. Expressed by an empty next-key commitment (`ncount=0`, `nsith='0'`). (L1)
- **Treating a witness as a watcher:** WRONG (role-boundary). Witnesses store/serve; they don't vouch for cross-AID anchors; validator must independently OOBI the delegator. (D3, L4)
- **Register a new CESR code in one table:** WRONG — shadow tables (`Saider.Digests`, `Serder.Digests`, `*Dex`, `BUDex`+`Counter.BUCodes`) fail late/silently. (L5)
- **"Simplify" CESR sizing arithmetic (double-modulo, order-of-ops):** breaks triplet/quadlet alignment and desyncs parsers silently. (A4, A5)
- **Register/overclaim register:** the KB itself warns against advocacy tone — "overclaiming costs credibility with a security-skeptic maintainer." Doctrine is stated conditionally. (`00-lens.md` intro; endorsement checklist item "Register is right (hedged, not advocacy)")

---

## 6. Terminology / crosswalk (spec term → keripy symbol)

Doctrine on vocabulary: "We author the **mapping**, never the definitions. Each term is defined canonically in a spec glossary (`kswg-{cesr,keri,acdc}-specification/spec/terms-definitions/`)." Symbols are stable; cite `file:Symbol`, not line numbers. (`20-crosswalk.md` intro)

**CESR layer (encoding):** Primitive → `coring.py:Matter`. Derivation code (hard `hs` + soft `ss`) → `MatterCodex`; `Matter.Hards`/`Bards`. Sizing record → `Sizage(hs,ss,xs,fs,ls)`; `Matter.Sizes`. Lead bytes/mid-padding → `Sizage.ls`; `Matter._infil`. Fixed vs variable-length → `Sizage.fs` (`None`=variable); `SmallVrzDex`/`LargeVrzDex`. Self-framing → `Matter._infil`/`_exfil` (code→length→raw). Composability → `Matter.composable`. Quadlet/triplet → `counting.py:Counter`. Framing/count code → `Counter`, `CounterCodex_1_0/_2_0`. Indexed signature (index/ondex) → `indexing.py:Siger`, `Indexer`, `Xizage`. Version string → `kering.py:Versionage`.

**KERI layer (identity/key-state):** AID/SCID → `coring.py:Prefixer`; `Hab.pre`. Controller → `Hab`/`GroupHab` (multisig). Key event → `serdering.py:SerderKERI`. Key-state → `eventing.py:Kever`; db `.states` (`KeyStateRecord`). Inception/rotation/interaction → `eventing.py:incept/rotate/interact`; `Ilks`. Delegated inception/rotation (dip/drt) → `eventing.py:delcept/deltate`. Establishment event → `Kever.incept/rotate`. Current/next threshold → `coring.py:Tholder` (`Kever.tholder`/`.ntholder`). Pre-rotation (next-key digest) → `eventing.py:exposeds`; `keeping.py:PreSit.nxt`. **KEL** → `db/basing.py` `.evts`+`.kels`+`.fels`. **KERL** → KEL + `.rcts`/`.vrcs`/`.ures`/`.vres` + `.wits`. First-seen → db `.fels`/`.fons`; `Kever.logEvent`. Duplicity → `Kevery.processEvent` (`LikelyDuplicitousError`); `db.ldes`. Receipt → `eventing.py:receipt`; db `.rcts`/`.wigs`. Witness/backer → `app/agenting.py`; `db.wits`; `Kever.toader`. Watcher → `app/indirecting.py` (observers); `db.obvs`. Seal → `serdering.py` seals; `db.aess` (delegation seal couple `(Number,Diger)`). OOBI → `app/.../oobiing`; `indirecting.py:Oobiery`. Salt/seed → `signing.py:Salter`/`Signer`. KAWA (witness agreement) → `agenting.py` (receipting) + `Kever` toad checks.

**ACDC layer (credentials/disclosure):** ACDC (Authentic Chained Data Container) → `vc/proving.py:credential()` → `SerderACDC`. Issuer → `creder.issuer`. Issuee/subject → `creder.a.i`. Schema → `creder.schema` (SAID); via `Schemer`. Edge → `creder.edge`; `Verifier.verifyChain`. Rules → `creder.rules`; `acdc/messaging.py:sectrule`. Verifiable data registry (TEL) → `vdr/eventing.py:Tever` (`.regk`); `vdr/credentialing.py:Registry`/`Regery`. Registry inception (vcp) → `vdr/eventing.py:incept`. Issuance/revocation (iss/rev/bis/brv) → `vdr/eventing.py:issue/revoke/backerIssue/backerRevoke`. SAID (most-compact form) → `vc/proving.py` (`Saider.saidify` on compact). Anchor/proof → `(seqner.sn, saider.said)`; `Tever.verifyAnchor`. **IPEX (apply/offer/agree/grant/admit/spurn)** → `vc/protocoling.py` (`ipexGrantExn`/`ipexAdmitExn`). Compact/partial/selective/graduated disclosure → `acdc/messaging.py`; `creder.rules` (⚠ disclosure rules not enforced in `Verifier`).

Note: "several terms recur across layers (AID, primitive, SAID, duplicity, key-state) — the spec repos cross-reference each other; the keripy symbol is the same regardless of which glossary defines the term." (`20-crosswalk.md` closing note)

---

## 7. Architecture / data-flow spine (worked structural example)

**Three layers → packages** (`10-map.md`): CESR (encoding substrate) = `core/coring.py`, `counting.py`, `indexing.py`, `structing.py`, `mapping.py`. KERI (identity/key-state) = `core/eventing.py`, `serdering.py`, `signing.py`. Storage = `db/basing.py`, `dbing.py`, `subing.py`, `koming.py`. App = `app/habbing.py`, `keeping.py`, `agenting.py`, `indirecting.py`. ACDC = `vdr/*`, `vc/*`, `acdc/*`.

**Inception/rotation spine:** `makeHab` (`Habery.makeHab`) → `Hab.incept` (⚠ Ed25519N hardcode L1) → `Manager.incept` (derive keys Creatory→SaltyCreator→Salter.signer, Argon2; stores `PrePrm`+`PreSit` old/new/nxt) → `eventing.incept/delcept` (build KED) → `Serder.makify` (dummy-# SAID → digest → overwrite, B5) → `Signer.sign` → `Kevery.processEvent` (validate: sigs≥Tholder; pre-rotation digest match `exposeds`/C1; prior-SAID chain B3; seq B2; toad F1; delegation seal D1) → `Kever.logEvent` → db (kels/fels/fons/evts/dtss/sigs/wigs/aess) → `WitnessReceiptor.receiptDo` (⚠ waits for ALL, L9).

DOCTRINE restated at the spine: "Verification (someone else's KEL) runs the same `Kevery.processEvent` path over events fetched from witnesses/OOBI — **re-verified locally, never trusted as authority** (Lens claim 1)." (`10-map.md`)

**ACDC stack (anchored to the KEL):** `proving.credential()` → `SerderACDC` (SAID over most-compact form) → `Credentialer.issue` (`Registry.anchorMsg` stores (issuer KEL sn, said) in `reger.ancs`) → `eventing.issue/backerIssue` (build TEL iss/bis) → `Tever.update`→`Tever.issue` → `verifyAnchor(serder, seqner, saider)`: `db.kels.getLast(pre, on=seqner.sn)`, `assert eserder.said == saider.qb64` (H1). Then `Verifier.processCredential` (schema + TEL state + chain edges) — ⚠ does NOT re-call verifyAnchor (L15). IPEX: `ipexGrantExn` → `ipexAdmitExn`.

**Credential trust chain.** The KB states it as a chain ending in past key state: **"ACDC → TEL (registry) event → **anchor seal** in the issuer's KEL at a specific sn → the issuer's key state as it was *then*"** (`10-map.md` §ACDC stack, ~L82–83), glossed as the retrograde-attack defense (H1). It then adds that "Edges link credentials into a provenance DAG (`verifyChain`)" and that ~~"operator semantics (`&&`/`||`) and DAG acyclicity are **not** fully enforced"~~ (~L84–85) — the second half **SUPERSEDED 2026-09-15**, same correction as L16/L17; see F-08H. The chain statement itself is unaffected and was re-read verbatim this pass.

---

## 8. Version-delta / 2.0-dev awareness (`92-refresh-2026-06-05.md`)

Refresh `d34a1014` → `60ab9e08` (65 commits, KERI 2.0.0-dev6) — the commit count checks out exactly, but the file's self-reported date of 2026-06-05 does not; it was written 2026-07-02 (F-08B). **Verdict: "the KB held."** (`92-refresh-2026-06-05.md` §opening, ~L3) That verdict is about the 65-commit window ending at `60ab9e08` and says nothing about the 493 commits since (§0). All invariants §A–§J and all landmines L1–L20 remain valid and present — none of the landmines were fixed. "The churn was mostly docstring/Sphinx reformatting, exception-handling tightening, and *additive* 2.0 features; **no breaking changes** to sizing rules, KEL validation, pre-rotation, delegation, duplicity, or storage invariants."

2.0-dev additive changes (Falcon-relevant, `[2.0-wire/code]`):
- **GramHead consolidated:** `0P/0Q/0R/0S` → single soft-code `'b'` (`Sizage(hs=1, ss=3, xs=0, fs=8, ls=0)`; 3 PVI + 4 count). Old codes removed.
- **`TransReceiptQuadruples` → `TransReceiptIdxSigGroups`** (codes `-D`/`-N` unchanged; now indexed-sig-group semantics).
- **NEW `BodyUniversalCodex`** (`BUDex_1_0`/`_2_0`) + `Counter.BUCodes` — CESR-native message-body framing (v2: `-F`/`-G`/`-H` = fix/map/nonnative body groups). New dual-registration requirement extends L5.
- **NEW `Number.onkey`** (`coring.py` ~1906) — ordinal→32-char-hex for DB keys (use this, not ad-hoc formatting).
- **NEW structing tuples:** `FirstSeen`, `TransReceipts`, `TransSigs`, `TransLastSigs` — transfer-layer attachment schemas.
- **`messagize(nests=...)`** — V2 message-nesting envelope (validated by `Reb64`, non-cryptographic); orthogonal to V1 paths.
- **`vrcsNew`** — experimental parallel validated-receipt table (both `vrcs`+`vrcsNew` written; no cutover yet). `vrcs.add` now keyed by `(pre, ldig)` tuple, not `dgKey(...)`.
- **`.ssgs` → `.tsgs` rename** (transferable SAD signature store; kwa param `ssgs`→`lsgs` in `eventing.processMsg`).

"Bottom line: the Falcon-relevant surface (§A + L1 + L5) is the only place with material 2.0 additions."

---

## 9. Meta / how the KB says to use itself

- Pre-change checklist (`00-lens.md`): **Whose authority?** (external trust dependency = stop, violates claim 1). **Adversarial input?** (verified, not just parsed — claim 3). **Which invariant does this guard protect?** ("Can't name it? Assume it's load-bearing"). **External contract?** (wire codes/sizes/field order/SAID/version → cite the spec). **Anchor-relative?** (judge signature against the anchor's key state, not "now").
- "If a change can't answer these cleanly, it is not yet understood well enough to defend."
- Invariants file: "If you can't map your change to the invariants here, you don't yet understand the blast radius — which is the signal to slow down (Lens claim 6)."
- Line numbers age; symbols are stable — cite `file:Symbol`. "Enforced where" is recon's best locating, "a pointer, not gospel."
- The KB's freshness ritual, in its own words: **"Run `./freshness.sh` ... at the start of any KB-using session or before a PR."** (`SCOPE.md` §Freshness ritual, ~L55–56) — see F-08C: on this box it cannot run.

---

## 10. What the KB is silent about, at `9489ac9bd` (negative results)

Four things moved in the wider corpus this month. A source that says nothing about them is a dated source, which is worth recording as findings rather than leaving a later reader to discover by absence. All four searches were run with `git grep` over the whole tree at `9489ac9bd`.

**F-08J — the KB has no material on `dp` / disclosure paths.** Zero matches for `dp` as a token, "disclosure path", "nested path" or "SAID path". Its entire treatment of the disclosure family is one crosswalk row — "Compact / partial / selective / graduated disclosure | `acdc/messaging.py`; `creder.rules`" (`20-crosswalk.md` §ACDC layer, ~L69) — which maps the terms to a module and adds only that disclosure rules are "not enforced in `Verifier`". There is no path-addressing notion in the KB at all.

**F-08K — the KB has no material on the `E1E` operator.** Zero matches for `E1E`, and zero for `DI2I`. `NI2I` appears only inside L17 and the twin-study row for #1040. So the KB's edge-operator model predates both the extension operator and the fail-closed set (F-08H) — it does not merely describe them wrongly, it does not know they exist.

**F-08L — the KB has no material on KRAM or on a key-state currency rule.** Zero matches for `KRAM`. There is no invariant covering replay protection, query-message freshness, or how a verifier decides its copy of key state is current; §H covers anchor-position validity (retrograde defense) and stops there. The KAWA row in the crosswalk (~L51) is the only witness-agreement entry and points at `agenting.py` plus `Kever` toad checks.

**F-08M — the KB has no post-quantum material beyond Falcon planning.** Zero matches for Dilithium, SPHINCS, Kyber, ML-KEM, ML-DSA, FN-DSA or SLH-DSA. "quantum" occurs once, in lens claim 8's hybrid posture sentence (~L77), and "post-quantum" once, in `PLAN.md` (~L12). Everything else PQ-shaped in this KB is Falcon-specific planning, and that planning rests on an unresolved question about which of two in-repo designs is canonical (quoted in F-08G). The corpus should not treat this source as evidence about the PQ code table in either direction.

---

## 11. The KB's own validation result, and the depth gaps it admits (`91-validation.md`, first mined 2026-09-15)

Not mined in earlier passes. It bears directly on how much weight the corpus should put on this source, so it belongs in the record.

The KB was tested by a blind drill: a fresh-context agent got only `00`–`31` plus `90` and the *title* of an open keripy issue, and was forbidden from reading keripy source or the fix. **"Result: PASS for localization."** (`91-validation.md` §Method/Result, ~L8) The conclusion the KB draws is scoped carefully, and the scoping is the point: **"the KB is self-sufficient for localization — a fresh session can find *where to look* and *what's at risk*"** (~L19–20).

That is a claim about navigation, not about correctness, and the file names what it does not cover: **"The KB localizes but lacks depth on multisig dynamics."** (~L24), listing five specific holes — group-state assembly, member join/leave, catch-up/sync for a late-joining member, out-of-order/escrow handling for group rotation, and group-threshold signature orchestration (~L25–31). It classes these as **"*depth* gaps, not localization gaps"** (~L35).

**F-08N — treat this source as a map, not an oracle, on its own testimony.** One passed localization drill on one issue is thin evidence, and the KB claims nothing more from it. Where the corpus needs a behavioral claim about keripy rather than a pointer to where behavior lives, the citation should be keripy at a named commit (`raw/09`), not this KB.

---

## 12. Open questions and unresolved tensions

- **Q-08A — is `31-landmines.md`'s "all L1–L20 still present" claim still true?** It was verified at keripy `60ab9e08` and is 493 commits stale (§0). L16/L17 are now known to be wrong (F-08H), which is one counterexample to the banner's confidence. L15 was always hedged by the KB itself as "a recon hypothesis with explicit uncertainty" (`31-landmines.md` L15, ~L158–159). The other eighteen are neither confirmed nor refuted at `b8f60166b`. **The corpus should not repeat "all twenty landmines hold" without qualification.** Re-verifying them is a keripy-side job and belongs to whoever owns `raw/09`, not here.
- **Q-08B — should the 1.x KB (F-08D) become a source?** It is a second, differently-scoped distillation of the same subject at keripy 1.2.13, unmined, sitting one directory over. Adding it is a manifest change and therefore out of scope for an unattended refresh. Argument for: the corpus has no 1.x-line material at all, and Provenant production runs 1.x. Argument against: the KB's own rule is "never mix 1.x and 2.0 claims in one file", so it would need a separate note, and the corpus's chapters are written on the 2.0/standardizing line.
- **Q-08C — what tier does a distilled secondary source carry?** This whole note is marked `[K]`, but the KB is not keripy; it is one contributor's reading of keripy plus four papers. Its `[2.0-code]` items are genuine `[K]`-class observations about code at a named commit, now 493 commits stale. Its `[protocol]` items are a *summary of* `background.md`, the primer, wtbo and x509-prob — which the corpus mines directly elsewhere. Quoting the KB for a protocol claim is relaying someone's summary as though it were the source, which standards §1 forbids in so many words. **Provisional resolution, for review: cite the KB for code observations and for its own framings (the landmines, the invariant catalogue, the pre-change checklist); cite the canonical papers directly for anything in §1, §2 or §5 that the KB is itself citing.** Recorded rather than applied — it touches every chapter that uses this note.
- **Q-08D — the KB names two conflicting in-repo Falcon designs and asks which is canonical (F-08G, `PLAN.md` ~L189–190).** Unresolved at `9489ac9bd`, and unresolvable from this source. Neither design has landed in keripy. If the corpus says anything about KERI's PQ plans it should say that the design question is open, not pick one.
