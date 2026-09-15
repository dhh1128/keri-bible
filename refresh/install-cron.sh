#!/usr/bin/env bash
# install-cron.sh — add (or show) the monthly refresh crontab entry.
#
# Deliberately NOT run by anything automatically: a job that schedules unattended model runs is
# yours to install. Run it yourself, or copy the line it prints.
#
#   ./install-cron.sh            # show the line and whether it is installed
#   ./install-cron.sh --install  # add it to your crontab (idempotent)
#   ./install-cron.sh --remove   # take it out again
#
# Why a system crontab and not Claude Code's own CronCreate: that scheduler's recurring jobs
# auto-expire after 7 days and only fire while a REPL is idle, so "once a month" never happens.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$DIR/run-refresh.sh"
MARK="# keri-bible monthly refresh"
# 3rd of the month, 05:23 local. A couple of days in so the month's merges have settled, and off
# the hour because everything else in the world fires at :00.
LINE="23 5 3 * * $SCRIPT >> \${XDG_STATE_HOME:-\$HOME/.local/state}/keri-bible-refresh/cron.log 2>&1 $MARK"

current() { crontab -l 2>/dev/null || true; }

case "${1:-}" in
  --install)
    if current | grep -Fq "$MARK"; then
      echo "already installed:"; current | grep -F "$MARK"; exit 0
    fi
    mkdir -p "${XDG_STATE_HOME:-$HOME/.local/state}/keri-bible-refresh"
    { current; echo "$LINE"; } | crontab -
    echo "installed:"; crontab -l | grep -F "$MARK"
    ;;
  --remove)
    current | grep -Fv "$MARK" | crontab -
    echo "removed."
    ;;
  *)
    echo "The line:"; echo; echo "  $LINE"; echo
    if current | grep -Fq "$MARK"; then echo "Status: installed."
    else echo "Status: NOT installed. Run '$0 --install' to add it."; fi
    echo
    echo "Before the first unattended run, check by hand:"
    echo "  $SCRIPT --dry-run     # detect only; prints the delta, changes nothing"
    ;;
esac
