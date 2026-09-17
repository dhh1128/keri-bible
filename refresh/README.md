# Refreshing the bible

The bible is a synthesis of sources that keep moving. This directory is the machinery that keeps it current without letting it get sloppier: a monthly job that finds what changed, mines only what matters, re-verifies every quote it touches, and opens a draft PR for Daniel to read.

**The standards are in [`prompts/standards.md`](prompts/standards.md).** Read that first if you are editing the corpus by hand, too — it is not just prompt text.

## Why this exists

Before it, the bible had no watermark. `raw/14`–`16` recorded a mining date and a source commit; `raw/01`–`13` recorded neither, and several named pre-reorg paths that had not existed since the repos moved into `~/code/<org>/` buckets. The only pins of record lived in one paragraph of `keri-doctrine.md`, which already admitted it was stale.

The finding that shaped the design, measured 2026-09-15: the ACDC specification's `main` had not moved since the last pin, while its **`v1.1` branch was 491 lines of `spec-body.md` ahead** and nothing tracked it. A job watching `main` alone would have reported "no spec movement" — a silent false negative, which is the worst outcome available here, because the bible's whole value is that a claim in it is believed.

## The two spec lines are not interchangeable

`main`/v1.0 is what the community is actively standardizing: that is what "normative" means today. `v1.1` is new thinking, likely but not certain to fold into the next standard. A claim resting on v1.1 is stronger than a GitHub discussion and weaker than the standardizing text, so it gets its own marker:

    [K]  implementation behaves this way at a named commit
    [P]  proposed in a discussion or whitepaper
    [N1.1]  in the v1.1 branch, not yet in the standardizing line
    [N]  in the line being standardized

Both lines are pinned separately in `sources.yaml`, and the `main`↔`v1.1` diff is recomputed every run. **Text that leaves that diff has landed** — a `[N1.1]` → `[N]` tier upgrade, mechanically detectable, and the single most valuable thing this job catches. (It can also mean the hunk was dropped from `v1.1`, which moves the claim the other way, so the report says "verify" rather than asserting.)

## The pieces

| File | What it does |
|---|---|
| `sources.yaml` | The manifest and watermark. Every source, its tracked branches, its pins, which note it feeds, which chapters depend on it. |
| `detect.py` | Phase 1. Deterministic, no model. Writes `state/<YYYY-MM>/delta.md`. Exit 0 = material, 10 = quiet, 2 = error. |
| `freshness.py` | Quote-drift checker. Source roots generated from `sources.yaml`, not hardcoded. Reports what is NEWLY broken against `freshness-baseline.json` rather than re-listing a standing backlog. |
| `freshness-baseline.json` | Quotes known not to resolve, so a run can report new breakage. Not absolution — it holds real drift nobody has re-anchored yet. |
| `snapshot-discussions.py` | Caches cited GitHub discussions locally and tracks their hashes, so their quotes are verifiable and in-place edits are visible. |
| `prompts/standards.md` | The contract every phase is bound by. |
| `prompts/refresh.md` | Phases 2–5, the model's instructions. |
| `run-refresh.sh` | Cron entry point. Runs phase 1, the model, then phase 6. |
| `install-cron.sh` | Shows or stages the schedule (`../cron/70-keri-bible-refresh.cron`) via devenv's `cron-link`. |
| `state/<YYYY-MM>/` | Per-run audit trail, tracked. A month with no PR still leaves a record of what was looked at and dismissed. |

## The six phases

1. **detect** — shell. Fetch every source, diff against its pin, query GitHub for discussions and merged PRs, hash the web sources, run the quote-drift check. Gate: nothing material → log and exit, no PR, no tokens.
2. **triage** — one agent. Classify each candidate: doctrinal, corroborative, tier movement, re-anchor, noise. This is the budget valve; most of a hundred keripy commits are noise and saying so is the job.
3. **mine** — one agent per affected `raw/` note, ≤4 concurrent, disjoint file sets. Re-read the **primary source** at the new commit, never the diff alone.
4. **synthesize** — one agent per affected `bible/` chapter, same isolation. Tier markers re-evaluated, `@commit` stamps refreshed, `keri-doctrine.md` touched only where a load-bearing claim actually moves.
5. **verify** — a fresh agent that did not do the mining. Every new or changed quote re-read at its pinned commit; anything unconfirmable is **cut**, not reworded. Then `freshness.py`, `snapshot-discussions.py`, and `build-bible.py`.
6. **deliver** — shell. Rebuild, commit signed off, push, open a draft PR, notify over confer.

Phases 1 and 6 are shell on purpose. The model edits files and writes a report; everything that leaves the machine is deterministic, so the model's blast radius stays "file contents in this repo".

## What the job may not do unattended

- **Create a `bible/` chapter.** That is a structural decision about what the bible is. It proposes; you decide. A new `raw/` note for a newly found topic is fine.
- **Retarget its own manifest.** `branches`, `chapters` and `tier` are reviewed fields. Untracked branches newer than the tracked ones are reported, never adopted.
- **Advance `last_mined` for a source it did not re-read.** `last_scanned` advances every run; `last_mined` only where a note was genuinely re-read. Under-claim, always.
- **Write to a WebOfTrust or trustoverip conversation.** Nothing here files an issue, comments on a discussion, or opens a PR anywhere but `dhh1128/keri-bible`. Findings worth raising upstream go in the PR body for Daniel to raise himself.

## Running it

```sh
./refresh/run-refresh.sh --dry-run     # phase 1 only: prints the delta, changes nothing
./refresh/run-refresh.sh               # the whole thing; opens a draft PR
./refresh/run-refresh.sh --force       # run the model phases even on a quiet month
./refresh/install-cron.sh --install    # 23 5 3 * * — 3rd of the month, 05:23 local
```

It refuses to start on a dirty working tree or off `main`, holds an flock so two runs cannot overlap, and logs to `~/.local/state/keri-bible-refresh/<YYYY-MM>.log`.

Not Claude Code's own `CronCreate`: its recurring jobs auto-expire after 7 days and only fire while a REPL is idle, so monthly never happens.

## Cost

Roughly zero on a quiet month — phase 1 is shell and the gate stops there. On a month with real movement, something like 100–400k output tokens: one triage agent, three or four miners, three or four synthesizers, a verifier.

## After a merge

If the PR changed `keri-doctrine.md`, the review panel is still reading the old copy. Run `./sync-reference.sh` in `~/code/wot/keri-review-panel`. The PR body says so when it applies.
