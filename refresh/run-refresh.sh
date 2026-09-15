#!/usr/bin/env bash
# run-refresh.sh — the monthly bible refresh, end to end. Cron entry point.
#
#   crontab:  23 5 3 * * /home/daniel/code/me/keri-bible/refresh/run-refresh.sh
#
# Phase 1 (detect) and phase 6 (commit/push/PR) run HERE, in shell. Phases 2-5 run inside one
# `claude -p` invocation driven by refresh/prompts/refresh.md. That split is deliberate: the model
# edits files and writes a report, and the deterministic part does everything that leaves the
# machine. The model's blast radius stays "file contents in this repo".
#
# Flags:
#   --dry-run     run detect only, print what would happen, change nothing
#   --force       run the model phases even if detect says the month was quiet
#   --no-fetch    pass through to detect.py (offline testing)
set -euo pipefail

# cron hands you a PATH of roughly /usr/bin:/bin and nothing else, so `claude` (in ~/.local/bin)
# is not found and the model phases die with a bare "command not found" halfway through a run
# that already spent its detect budget. Prepend rather than replace, so an interactive run keeps
# whatever the shell gave it.
export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}/keri-bible-refresh"
LOCK="$STATE_HOME/run.lock"
RUN="$(date +%Y-%m)"
LOG="$STATE_HOME/$RUN.log"
TIMEOUT="${REFRESH_TIMEOUT:-7200}"

DRY_RUN=0; FORCE=0; DETECT_ARGS=()
for a in "$@"; do
  case "$a" in
    --dry-run) DRY_RUN=1 ;;
    --force)   FORCE=1 ;;
    --no-fetch) DETECT_ARGS+=(--no-fetch) ;;
    *) echo "unknown flag: $a" >&2; exit 64 ;;
  esac
done

mkdir -p "$STATE_HOME"
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "another refresh is already running (lock $LOCK); exiting" >&2
  exit 0
fi

log() { printf '%s  %s\n' "$(date -Is)" "$*" | tee -a "$LOG" >&2; }
fail() { log "FAILED: $*"; notify "KERI bible refresh FAILED for $RUN: $* — see $LOG"; exit 1; }

notify() {
  # Agent-side notification is an MCP tool, not a CLI, so it takes one cheap headless turn.
  # Never let a notification failure fail the run.
  timeout 300 claude -p --permission-mode acceptEdits \
    --allowedTools "mcp__confer__notify" \
    "Use the confer notify tool to tell Daniel exactly this, then stop: $1" \
    >>"$LOG" 2>&1 || log "(notify failed; continuing)"
}

cd "$REPO"

# --- guards ------------------------------------------------------------------------------------
# Never run on top of work in progress. An unattended job that commits someone's half-finished
# edits is worse than one that does not run.
[ -z "$(git status --porcelain)" ] || fail "working tree is dirty; refusing to run"
[ "$(git rev-parse --abbrev-ref HEAD)" = "main" ] || fail "not on main; refusing to run"
command -v gh >/dev/null || fail "gh not on PATH"
gh auth status >/dev/null 2>&1 || fail "gh is not authenticated"

log "=== refresh $RUN starting (repo $REPO)"
nice -n 19 ionice -c 3 git fetch --quiet origin || fail "git fetch origin failed"
git merge-base --is-ancestor origin/main HEAD 2>/dev/null || log "NOTE: local main is behind origin/main"

# --- phase 1: detect ---------------------------------------------------------------------------
set +e
nice -n 19 ionice -c 3 python3 "$REPO/refresh/detect.py" --run "$RUN" "${DETECT_ARGS[@]}" \
  >>"$LOG" 2>&1
DETECT_RC=$?
set -e
log "detect exit $DETECT_RC"

case "$DETECT_RC" in
  0)  log "material delta — proceeding" ;;
  10) if [ "$FORCE" = 1 ]; then log "quiet month, but --force given"
      else log "quiet month — no PR, no tokens spent"; exit 0; fi ;;
  2)  fail "detect could not read any source (see $LOG)" ;;
  *)  fail "detect exited $DETECT_RC" ;;
esac

DELTA="$REPO/refresh/state/$RUN/delta.md"
[ -f "$DELTA" ] || fail "detect produced no delta.md"

if [ "$DRY_RUN" = 1 ]; then
  log "dry run — stopping before the model phases"
  echo "--- $DELTA"; cat "$DELTA"
  exit 0
fi

# --- branch ------------------------------------------------------------------------------------
BRANCH="refresh/$RUN"
n=1
while git show-ref --quiet "refs/heads/$BRANCH" || git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; do
  n=$((n+1)); BRANCH="refresh/$RUN-$n"
done
git switch -c "$BRANCH" >>"$LOG" 2>&1 || fail "could not create branch $BRANCH"
log "working on $BRANCH"

# --- phases 2-5: the model ---------------------------------------------------------------------
# --permission-mode acceptEdits plus a named tool allowlist, NOT bypassPermissions: the hooks stay
# active (no-post-to-upstream in particular) and nothing outside this list can run unattended.
PROMPT="$(cat "$REPO/refresh/prompts/refresh.md")

---

Your run directory is refresh/state/$RUN. Read refresh/state/$RUN/delta.md for what moved, and
refresh/prompts/standards.md for the rules you are bound by. Write refresh/state/$RUN/report.md as
you go. Do not run git, do not push, do not open a pull request — the calling script does that
after you exit. Cap concurrent subagents at 4 and tell each to run heavy searches under nice -n 19."

set +e
timeout "$TIMEOUT" nice -n 19 ionice -c 3 claude -p "$PROMPT" \
  --permission-mode acceptEdits \
  --add-dir "$HOME/code" \
  --allowedTools "Read Glob Grep Edit Write Agent TodoWrite Bash(git:*) Bash(gh api:*) Bash(gh search:*) Bash(python3:*) Bash(bash refresh/*) Bash(nice:*) Bash(rg:*) Bash(grep:*) Bash(sed:*) Bash(head:*) Bash(tail:*) Bash(wc:*) Bash(ls:*) Bash(find:*) Bash(diff:*)" \
  >>"$LOG" 2>&1
MODEL_RC=$?
set -e
log "model phases exit $MODEL_RC"
[ "$MODEL_RC" = 124 ] && log "WARNING: model phases hit the ${TIMEOUT}s timeout; committing whatever landed"

REPORT="$REPO/refresh/state/$RUN/report.md"
[ -f "$REPORT" ] || { git switch main >>"$LOG" 2>&1; git branch -D "$BRANCH" >>"$LOG" 2>&1
                      fail "model wrote no report.md — nothing to deliver"; }

# --- phase 6: deliver --------------------------------------------------------------------------
python3 "$REPO/build-bible.py" > "$REPO/keri-bible.md" || fail "build-bible.py failed"

if [ -z "$(git status --porcelain)" ]; then
  git switch main >>"$LOG" 2>&1; git branch -D "$BRANCH" >>"$LOG" 2>&1
  log "model changed nothing — no PR. See $REPORT for why."
  notify "KERI bible refresh $RUN found movement but changed nothing. Report: $REPORT"
  exit 0
fi

git add -A
git commit -s -q -m "Refresh $RUN: re-anchor the bible against current sources

Automated monthly refresh. See refresh/state/$RUN/report.md for what moved,
what was dismissed, and what needs judgment." || fail "commit failed"

git push -q -u origin "$BRANCH" || fail "push failed"

BODY="$STATE_HOME/$RUN-pr-body.md"
{
  cat "$REPORT"
  echo; echo "---"; echo
  echo "<details><summary>Phase 1 delta report</summary>"; echo
  cat "$DELTA"
  echo; echo "</details>"
} > "$BODY"

PR_URL="$(gh pr create --draft --base main --head "$BRANCH" \
  --title "Bible refresh $RUN" --body-file "$BODY")" || fail "gh pr create failed"
log "opened $PR_URL"

git switch main >>"$LOG" 2>&1
notify "KERI bible refresh $RUN is ready for review: $PR_URL (draft PR; see JUDGMENT NEEDED at the end of the body)"
log "=== refresh $RUN done"
