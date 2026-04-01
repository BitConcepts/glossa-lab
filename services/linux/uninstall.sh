#!/usr/bin/env bash
# Glossa Lab — Remove systemd user service
set -euo pipefail

SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE_FILE="$SERVICE_DIR/glossa-lab.service"

if [ -f "$SERVICE_FILE" ]; then
    systemctl --user stop glossa-lab.service 2>/dev/null || true
    systemctl --user disable glossa-lab.service 2>/dev/null || true
    rm "$SERVICE_FILE"
    systemctl --user daemon-reload
    echo "[OK] Service removed."
else
    echo "[OK] No service file found — nothing to remove."
fi
