#!/bin/bash
# Wrapper invoked by the macOS LaunchAgent for the daily BscScan refresh run.
#
# It normalizes the environment launchd provides (minimal PATH, no shell
# profile), exports the unattended-friendly BscScan tuning knobs, then runs
# run_workflow.py. Any arguments are passed straight through to the workflow
# (e.g. --crawl-only, --skip-reset).
#
# Manual test on the Mac:
#   scripts/run_daily.sh --crawl-only
set -uo pipefail

REPO_DIR="${REFRESH_REPO_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
PYTHON_BIN="${REFRESH_PYTHON:-python3}"

# launchd starts jobs with a minimal PATH; add the usual Homebrew/system
# locations so python3, chromedriver, etc. resolve.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${PATH:-}"

# Unattended defaults (see README "OpenClaw / unattended cron"). Any value
# already set in the environment or scripts/schedule.local.env wins.
export BSCSCAN_CAPTCHA_WAIT="${BSCSCAN_CAPTCHA_WAIT:-120}"
export BSCSCAN_LOGIN_RETRIES="${BSCSCAN_LOGIN_RETRIES:-5}"
export BSCSCAN_CHROME_USER_DATA="${BSCSCAN_CHROME_USER_DATA:-$HOME/.refresh/chrome-bscscan}"
export BSCSCAN_CHROME_PROFILE="${BSCSCAN_CHROME_PROFILE:-Default}"

# Optional per-machine overrides (gitignored), e.g. BSCSCAN_ACCOUNT=refresh1
LOCAL_ENV="$REPO_DIR/scripts/schedule.local.env"
if [ -f "$LOCAL_ENV" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$LOCAL_ENV"
  set +a
fi

mkdir -p "$REPO_DIR/logs" "$BSCSCAN_CHROME_USER_DATA"
LOG="$REPO_DIR/logs/daily-$(date +%Y%m%d-%H%M%S).log"

cd "$REPO_DIR" || { echo "cannot cd to $REPO_DIR"; exit 1; }

{
  echo "=== refresh daily run: $(date) ==="
  echo "repo=$REPO_DIR"
  echo "python=$PYTHON_BIN ($($PYTHON_BIN --version 2>&1))"
  echo "args=${*:-<full pipeline>}"
  "$PYTHON_BIN" run_workflow.py "$@"
  code=$?
  echo "=== exit $code at $(date) ==="
  exit $code
} >>"$LOG" 2>&1
