#!/bin/bash
# Install (or reinstall) a daily macOS LaunchAgent that runs run_workflow.py.
#
# The agent runs in your GUI login session (gui/<uid> domain) so Selenium can
# drive Chrome and Cloudflare Turnstile can pass. Keep the Mac awake + logged
# in + screen unlocked at run time (Amphetamine "closed-display mode", etc.).
#
# Usage:
#   scripts/install_schedule.sh [HH:MM] [-- <run_workflow.py args>]
#
# Examples:
#   scripts/install_schedule.sh 09:30                 # full pipeline daily at 09:30 local
#   scripts/install_schedule.sh 09:30 -- --crawl-only # crawl only
#   scripts/install_schedule.sh                       # defaults to 09:00, full pipeline
set -euo pipefail

LABEL="com.renaiss.refresh.daily"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_DIR="$HOME/Library/LaunchAgents"
PLIST="$AGENT_DIR/$LABEL.plist"
PYTHON_BIN="$(command -v python3 || true)"

if [ "$(uname)" != "Darwin" ]; then
  echo "This installer targets macOS (launchd). Detected: $(uname)." >&2
  exit 1
fi
if [ -z "$PYTHON_BIN" ]; then
  echo "python3 not found on PATH. Install it (and 'pip install selenium undetected-chromedriver') first." >&2
  exit 1
fi

TIME="${1:-09:00}"
if [ "$#" -gt 0 ]; then shift; fi
if [ "${1:-}" = "--" ]; then shift; fi
WF_ARGS=("$@")

case "$TIME" in
  [0-2][0-9]:[0-5][0-9]|[0-9]:[0-5][0-9]) : ;;
  *) echo "Time must be HH:MM (24h), got: $TIME" >&2; exit 1 ;;
esac
HOUR=$((10#${TIME%%:*}))
MIN=$((10#${TIME##*:}))

# Warn early if deps are missing for this interpreter.
if ! "$PYTHON_BIN" -c "import selenium, undetected_chromedriver" >/dev/null 2>&1; then
  echo "WARNING: $PYTHON_BIN is missing selenium/undetected-chromedriver." >&2
  echo "         Run: $PYTHON_BIN -m pip install selenium undetected-chromedriver" >&2
fi

mkdir -p "$AGENT_DIR" "$REPO_DIR/logs"

# Build the <ProgramArguments> list: wrapper first, then any workflow args.
prog_args="        <string>$REPO_DIR/scripts/run_daily.sh</string>"
for a in "${WF_ARGS[@]:-}"; do
  [ -n "$a" ] || continue
  prog_args="$prog_args
        <string>$a</string>"
done

cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
$prog_args
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>REFRESH_REPO_DIR</key>
        <string>$REPO_DIR</string>
        <key>REFRESH_PYTHON</key>
        <string>$PYTHON_BIN</string>
    </dict>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>$HOUR</integer>
        <key>Minute</key>
        <integer>$MIN</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
    <key>ProcessType</key>
    <string>Interactive</string>
    <key>StandardOutPath</key>
    <string>$REPO_DIR/logs/launchd.out.log</string>
    <key>StandardErrorPath</key>
    <string>$REPO_DIR/logs/launchd.err.log</string>
</dict>
</plist>
PLIST

DOMAIN="gui/$(id -u)"
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST"
launchctl enable "$DOMAIN/$LABEL"

echo "Installed LaunchAgent: $PLIST"
echo "  schedule : daily at $(printf '%02d:%02d' "$HOUR" "$MIN") (local time)"
echo "  command  : run_daily.sh ${WF_ARGS[*]:-<full pipeline>}"
echo "  python   : $PYTHON_BIN"
echo
echo "Run it once now to verify:"
echo "  launchctl kickstart -k $DOMAIN/$LABEL"
echo "  tail -f $REPO_DIR/logs/daily-*.log"
