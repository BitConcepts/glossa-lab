#!/usr/bin/env bash
# Glossa Lab — Remove macOS LaunchAgent
set -euo pipefail

PLIST="$HOME/Library/LaunchAgents/com.glossalab.backend.plist"

if [ -f "$PLIST" ]; then
    launchctl unload "$PLIST" 2>/dev/null || true
    rm "$PLIST"
    echo "[OK] LaunchAgent removed."
else
    echo "[OK] No LaunchAgent found — nothing to remove."
fi
