#!/usr/bin/env bash
# Glossa Lab — Install systemd user service
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE_FILE="$SERVICE_DIR/glossa-lab.service"

mkdir -p "$SERVICE_DIR"

# Copy template and substitute repo root
sed "s|__REPO_ROOT__|${REPO_ROOT}|g" "$SCRIPT_DIR/glossa-lab.service" > "$SERVICE_FILE"

systemctl --user daemon-reload
systemctl --user enable glossa-lab.service

echo "[OK] Installed: $SERVICE_FILE"
echo "     Start with: systemctl --user start glossa-lab"
echo "     Status:     systemctl --user status glossa-lab"
