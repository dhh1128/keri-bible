#!/usr/bin/env bash
# install-cron.sh — schedule (or unschedule) the monthly refresh on this box.
#
# Deliberately NOT run by anything automatically: a job that schedules unattended model runs is
# yours to install. Run it yourself.
#
#   ./install-cron.sh            # show the schedule and whether it is staged here
#   ./install-cron.sh --install  # stage it (idempotent)
#   ./install-cron.sh --remove   # unstage it
#
# This no longer edits the crontab directly. The schedule lives in
# ../cron/70-keri-bible-refresh.cron, which names the boxes it belongs on; `cron-sync` stages it
# there by itself, and this script is for opting a box in by hand regardless. Either way the
# fragment is symlinked into ~/.config/crontab.d and the crontab is rebuilt from what is staged.
# The old version
# appended its line with `crontab -`, which worked but left the schedule in a file no repo
# owned, and left its recipient to whatever MAILTO happened to sit above it in the crontab.
# See ~/code/me/devenv/cron/README.md.
#
# Why a system crontab and not Claude Code's own CronCreate: that scheduler's recurring jobs
# auto-expire after 7 days and only fire while a REPL is idle, so "once a month" never happens.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$DIR/run-refresh.sh"
FRAGMENT="$DIR/../cron/70-keri-bible-refresh.cron"
STAGED_AS="70-keri-bible-refresh.cron"
STAGING="${CRONTAB_D:-$HOME/.config/crontab.d}"

cron_link() {
  if command -v cron-link >/dev/null 2>&1; then command cron-link "$@"
  elif [ -x "$HOME/code/me/devenv/cron/cron-link" ]; then "$HOME/code/me/devenv/cron/cron-link" "$@"
  else
    echo "cron-link not found. It comes from devenv: bash ~/code/me/devenv/cron/install.sh" >&2
    echo "(Not recreating it here — see devenv/cron/README.md for what it does.)" >&2
    exit 1
  fi
}

case "${1:-}" in
  --install)
    mkdir -p "${XDG_STATE_HOME:-$HOME/.local/state}/keri-bible-refresh"
    cron_link "$FRAGMENT"
    ;;
  --remove)
    cron_link --unlink "$STAGED_AS"
    ;;
  *)
    echo "The schedule:"; echo
    grep -vE '^#' "$FRAGMENT" | grep -vE '^\s*$' | sed 's/^/  /'
    echo
    if [ -L "$STAGING/$STAGED_AS" ]; then echo "Status: staged on this box."
    else echo "Status: NOT staged. Run '$0 --install' to add it."; fi
    echo
    echo "Before the first unattended run, check by hand:"
    echo "  $SCRIPT --dry-run     # detect only; prints the delta, changes nothing"
    ;;
esac
