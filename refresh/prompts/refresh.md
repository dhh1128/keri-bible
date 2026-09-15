# Monthly bible refresh — phases 2 through 5

You are running the model phases of the KERI bible's monthly refresh, unattended, from cron. Phase 1 (detect) has already run and phase 6 (commit, push, PR) will be done by the shell script after you exit. **You edit files and write a report. You do not run git, you do not push, you do not open a PR.**

Read `refresh/prompts/standards.md` first and treat it as binding. Read `refresh/state/<RUN>/delta.md` — the run directory is named in your instructions — for what moved. Read `refresh/sources.yaml` for the manifest.

Write your report to `refresh/state/<RUN>/report.md` as you go, not at the end. If you run out of context or die mid-run, that file is what tells the next person how far you got.

## Phase 2 — triage

Classify every candidate in `delta.md` into exactly one class, with a one-line reason:

- **doctrinal** — changes what the bible asserts, or adds something it lacks. Goes to mining.
- **corroborative** — new evidence for a claim already made. Goes to mining, usually cheaply.
- **tier movement** — same claim, different provenance: v1.1 text reaching the standardizing branch (`[N1.1]` → `[N]`), a discussion design reaching a spec (`[P]` → `[N1.1]`), an implementation landing (`[P]` → `[K]`). Cheap to apply and easy to miss by hand — this is much of why the job exists.
- **re-anchor** — the claim stands, the line numbers moved. Skip mining, go straight to phase 4.
- **noise** — CI, dependencies, typos, formatting, unrelated subsystems. Advances `last_scanned` only.

Be willing to call most of it noise. A hundred keripy commits with four that matter is a normal month, and triage earns its keep by saying so rather than by finding work.

Two triage traps specific to this corpus:

- **A quiet thread is not a dead idea.** keripy #1095 sat ten months with zero comments while the design it invented was actively intended. Silence is not a signal.
- **One concept, several names.** Search both vocabularies before concluding a topic is untouched — "presentation registry" misses #1095, which invents the thing under "issuee usage registry". When a topic has a spoken name too, note it.

Output a work list: each item → the `raw/` note it changes → the `bible/` chapter(s) that depend on it, taken from the manifest's `feeds` and `chapters`.

## Phase 3 — mine

One subagent per affected `raw/` note, at most 4 concurrent, each owning exactly one file so their writes cannot collide. Tell each agent to run any heavy search under `nice -n 19`.

Each agent: open the **primary source at the new commit** and read the passages that changed, plus enough context to know the quote is not reversed by its surroundings. Never mine from the diff alone. Then update its note:

- Update the header: source, pinned commit, mining date, and what this pass covered.
- Add claims in the note's existing register — verbatim quote ≤25 words, `file §heading`, line hint, commit.
- Mark superseded claims superseded with the date and what replaced them. Do not delete.
- Record what you looked for and did not find. A negative result at a named commit is a real finding and this corpus already uses them ("no code recognizes the three-part presentation-registry signal").
- Add unresolved tensions to the note's open-questions section rather than smoothing them over.

If a topic has no note and clearly warrants one, create `raw/NN-<topic>.md` following the existing house format. Do not create a `bible/` chapter.

## Phase 4 — synthesize

One subagent per affected chapter, at most 4 concurrent, each owning exactly one file.

- Update `bible/NN-*.md` from its notes. Re-evaluate tier markers against the new pins, update `@<commit>` stamps and any status paragraph, and add `[N1.1]` to the chapter's marker key where the chapter now needs it.
- Update the shibboleth table in `bible/07-shibboleths-and-anti-patterns.md` when a refresh creates, retires, or sharpens one.
- Update `keri-doctrine.md` **only where a load-bearing claim actually moves**. It is a house-style file a review panel reasons in, not a changelog; most months it needs nothing but a citation-durability stamp. When it does change, say so prominently in your report — a sync into `~/code/wot/keri-review-panel` is owed, and the PR body has to ask for it.
- Refresh the citation-durability paragraph in `keri-doctrine.md` with the new pins, including a partial-re-anchor note if only part of the corpus was re-read. Being specific about what was *not* re-checked is the point of that paragraph.

## Phase 5 — verify

Adversarial, and the phase that protects the standard. Use a fresh subagent that did not do the mining — a verifier checking its own work is not a check.

For **every new or changed quote** in the working tree: re-read the source at its pinned commit and confirm the quote is verbatim, the `§heading` exists, and the surrounding text supports the use it is being put to. A quote that cannot be confirmed is **cut**, and the cut is recorded. Then:

- Confirm every tier marker change against the evidence class the standards require.
- Sweep for assertions that gained no citation.
- Run `refresh/snapshot-discussions.py` and report any DRIFT lines — an in-place edit to a discussion invalidates quotes with no commit anywhere.
- Run `python3 refresh/freshness.py` and check the NEW-miss list, which is the actionable part; the standing backlog in `refresh/freshness-baseline.json` is known. If you re-anchored citations, refresh the baseline with `--update-baseline` and say in the report how many healed.
- Run `python3 build-bible.py > keri-bible.md` to rebuild the assembled reference.

Anything you cannot settle goes under `JUDGMENT NEEDED` in the report rather than being resolved by guesswork.

## The report

`refresh/state/<RUN>/report.md`, in this order, because the shell script turns it into the PR body:

1. **Sources advanced** — `old → new` per source, `last_mined` distinguished from `last_scanned`.
2. **Doctrinal changes** — per chapter, what a reader of the old version would now say differently.
3. **Tier movement** — every marker change, with its evidence. A `[N1.1]` → `[N]` upgrade is a statement that something became standard; write it as one.
4. **Re-anchored only** — citations whose line numbers moved and whose claims did not.
5. **Reviewed and dismissed** — counts by class, and the one-line reason for anything a reader might expect to have mattered.
6. **Cuts** — quotes removed for failing verification, and what each used to support.
7. **JUDGMENT NEEDED** — proposed new chapters, proposed manifest changes (untracked branches, `chapters` mapping), doctrine changes owing a panel sync, unresolved tensions, anything upstream that Daniel may want to raise himself.

Then update the pins in `refresh/sources.yaml`: `last_scanned` for every source scanned, `last_mined` **only** for notes actually re-read. If you are unsure whether a note was genuinely re-read against a commit, it was not.
