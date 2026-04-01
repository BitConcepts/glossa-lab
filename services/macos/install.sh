#!/usr/bin/env bash
# Glossa Lab — Install macOS LaunchAgent
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
AGENT_DIR="$HOME/Library/LaunchAgents"
PLIST="$AGENT_DIR/com.glossalab.backend.plist"

mkdir -p "$AGENT_DIR"

# Copy template and substitute repo root
sed "s|__REPO_ROOT__|${REPO_ROOT}|g" "$SCRIPT_DIR/com.glossalab.backend.plist" > "$PLIST"

echo "[OK] Installed: $PLIST"
echo "     Load with:   launchctl load $PLIST"
echo "     Unload with: launchctl unload $PLIST"
