#!/usr/bin/env bash
# Glossa Lab — remove the supervised backend unit + tray autostart.
# State and logs under the state directory are kept (they are the
# supervisor's record); remove them by hand if they are not wanted.
set -euo pipefail

MODE="user"
SERVICE_DIR=""
AUTOSTART_DIR="${HOME}/.config/autostart"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
while [ $# -gt 0 ]; do
    case "$1" in
        --system) MODE="system" ;;
        --user) MODE="user" ;;
        --service-dir) SERVICE_DIR="$2"; shift ;;
        --autostart-dir) AUTOSTART_DIR="$2"; shift ;;
        --icon-dir) ICON_DIR="$2"; shift ;;
        *) echo "[ERROR] Unknown option: $1" >&2; exit 2 ;;
    esac
    shift
done

if [ "$MODE" = "system" ]; then
    [ -n "$SERVICE_DIR" ] || SERVICE_DIR="/etc/systemd/system"
    SYSTEMCTL=(systemctl)
else
    [ -n "$SERVICE_DIR" ] || SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
    SYSTEMCTL=(systemctl --user)
fi

for unit in glossa-lab-backend.service glossa-lab.service; do
    if [ -f "$SERVICE_DIR/$unit" ]; then
        "${SYSTEMCTL[@]}" stop "$unit" 2>/dev/null || true
        "${SYSTEMCTL[@]}" disable "$unit" 2>/dev/null || true
        rm -f "$SERVICE_DIR/$unit"
        echo "[OK] Removed $unit"
    fi
done
rm -f "$SERVICE_DIR/glossa-lab-backend-alert.service"
rm -f "$AUTOSTART_DIR/glossa-lab-tray.desktop"
rm -f "$ICON_DIR/glossa-lab.png"
"${SYSTEMCTL[@]}" daemon-reload 2>/dev/null || true
echo "[OK] Glossa Lab supervision removed (state and logs kept)."
