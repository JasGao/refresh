#!/bin/bash
# Remove the daily BscScan refresh LaunchAgent.
set -euo pipefail

LABEL="com.renaiss.refresh.daily"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
rm -f "$PLIST"
echo "Removed LaunchAgent: $LABEL"
