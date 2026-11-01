#!/usr/bin/env bash
# Glossa Lab — install the supervised backend + tray (Linux).
#
# One installer for both halves, following the Syncyard spec 007
# pattern (windowless supervision):
#
#   * backend  -> systemd unit "glossa-lab-backend" (user manager by
#                 default; --system for machines with no user manager,
#                 e.g. headless VMs), Restart=on-failure with a
#                 3-starts-per-hour cap; on cap/failure an alert unit
#                 records OWNER_NEEDED in the state directory.
#   * tray     -> per-user autostart entry + the Glossa Lab brand
#                 icon installed into the user's icon theme.
#
# The install is idempotent: re-running re-renders the same files,
# re-enables the same unit, and re-verifies backend identity.
#
# Usage:
#   services/linux/install.sh [--system] [--no-start]
#                             [--skip-dependencies] [--no-tray]
#                             [--repo-root PATH] [--venv-python PATH]
#                             [--port N] [--render-only]
#
# --render-only writes every file but touches no service manager
# (used by tests and scratch verification). All waits are bounded.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODE="user"
START=1
SKIP_DEPS=0
RENDER_ONLY=0
INSTALL_TRAY=1
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VENV_PYTHON=""
PORT=8001
STATE_DIR=""
SERVICE_DIR=""
SUPPORT_DIR=""
AUTOSTART_DIR="${HOME}/.config/autostart"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"

while [ $# -gt 0 ]; do
    case "$1" in
        --system) MODE="system" ;;
        --user) MODE="user" ;;
        --no-start) START=0 ;;
        --skip-dependencies) SKIP_DEPS=1 ;;
        --render-only) RENDER_ONLY=1 ;;
        --no-tray) INSTALL_TRAY=0 ;;
        --repo-root) REPO_ROOT="$2"; shift ;;
        --venv-python) VENV_PYTHON="$2"; shift ;;
        --port) PORT="$2"; shift ;;
        --state-dir) STATE_DIR="$2"; shift ;;
        --service-dir) SERVICE_DIR="$2"; shift ;;
        --support-dir) SUPPORT_DIR="$2"; shift ;;
        --autostart-dir) AUTOSTART_DIR="$2"; shift ;;
        --icon-dir) ICON_DIR="$2"; shift ;;
        *) echo "[ERROR] Unknown option: $1" >&2; exit 2 ;;
    esac
    shift
done

[ -n "$VENV_PYTHON" ] || VENV_PYTHON="$REPO_ROOT/backend/venv/bin/python"

if [ "$MODE" = "system" ]; then
    [ -n "$SERVICE_DIR" ] || SERVICE_DIR="/etc/systemd/system"
    [ -n "$SUPPORT_DIR" ] || SUPPORT_DIR="/usr/local/lib/glossa-lab"
    [ -n "$STATE_DIR" ] || STATE_DIR="/var/lib/glossa-lab"
    SYSTEMCTL=(systemctl)
    WANTED_BY="multi-user.target"
else
    [ -n "$SERVICE_DIR" ] || SERVICE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
    [ -n "$SUPPORT_DIR" ] || SUPPORT_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/glossa-lab/supervisor"
    [ -n "$STATE_DIR" ] || STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/glossa-lab"
    SYSTEMCTL=(systemctl --user)
    WANTED_BY="default.target"
fi

UNIT_NAME="glossa-lab-backend.service"
LEGACY_UNIT="glossa-lab.service"

render() {
    # render TEMPLATE OUTPUT — substitute install-time placeholders.
    sed -e "s|__REPO_ROOT__|${REPO_ROOT}|g" \
        -e "s|__VENV_PYTHON__|${VENV_PYTHON}|g" \
        -e "s|__STATE_DIR__|${STATE_DIR}|g" \
        -e "s|__SUPPORT_DIR__|${SUPPORT_DIR}|g" \
        -e "s|__PORT__|${PORT}|g" \
        -e "s|__WANTED_BY__|${WANTED_BY}|g" \
        "$1" > "$2"
}

echo "[INSTALL] Glossa Lab supervised install (mode: $MODE)"
echo "          repo:    $REPO_ROOT"
echo "          python:  $VENV_PYTHON"
echo "          state:   $STATE_DIR"

# ── Dependencies ────────────────────────────────────────────────
if [ "$SKIP_DEPS" -eq 0 ] && [ "$RENDER_ONLY" -eq 0 ]; then
    if [ ! -x "$VENV_PYTHON" ]; then
        echo "[1/4] Creating virtual environment..."
        python3 -m venv "$(dirname "$(dirname "$VENV_PYTHON")")"
    fi
    echo "[1/4] Installing backend + tray dependencies..."
    "$VENV_PYTHON" -m pip install --quiet -e "$REPO_ROOT/backend[tray]"
else
    echo "[1/4] Dependencies skipped."
fi

# ── Supervisor support files ────────────────────────────────────
echo "[2/4] Installing supervisor files..."
mkdir -p "$SERVICE_DIR" "$SUPPORT_DIR" "$STATE_DIR"
install -m 0755 "$SCRIPT_DIR/healthcheck.py" "$SUPPORT_DIR/healthcheck.py"
install -m 0755 "$SCRIPT_DIR/record-owner-needed.sh" "$SUPPORT_DIR/record-owner-needed.sh"
render "$SCRIPT_DIR/glossa-lab-backend.service" "$SERVICE_DIR/$UNIT_NAME"
render "$SCRIPT_DIR/glossa-lab-backend-alert.service" "$SERVICE_DIR/glossa-lab-backend-alert.service"

# ── Tray + icon ─────────────────────────────────────────────────
ICON_SHA256=""
if [ "$INSTALL_TRAY" -eq 1 ]; then
    echo "[3/4] Installing tray autostart + Glossa Lab icon..."
    mkdir -p "$AUTOSTART_DIR" "$ICON_DIR" "$SUPPORT_DIR/assets"
    render "$SCRIPT_DIR/glossa-lab-tray.desktop" "$AUTOSTART_DIR/glossa-lab-tray.desktop"
    install -m 0644 "$REPO_ROOT/tray/glossa_tray/assets/glossa-lab.png" "$ICON_DIR/glossa-lab.png"
    install -m 0644 "$REPO_ROOT/tray/glossa_tray/assets/glossa-lab.png" "$SUPPORT_DIR/assets/glossa-lab.png"
    install -m 0644 "$REPO_ROOT/tray/glossa_tray/assets/glossa-lab.ico" "$SUPPORT_DIR/assets/glossa-lab.ico"
    ICON_SHA256="$(sha256sum "$ICON_DIR/glossa-lab.png" | awk '{print $1}')"
    echo "          icon:    $ICON_DIR/glossa-lab.png sha256=$ICON_SHA256"
else
    echo "[3/4] Tray install skipped (--no-tray)."
fi

if [ "$RENDER_ONLY" -eq 1 ]; then
    echo "[OK] Render-only install complete (service manager untouched)."
    echo "     unit: $SERVICE_DIR/$UNIT_NAME"
    exit 0
fi

# ── Service manager ─────────────────────────────────────────────
echo "[4/4] Enabling supervised backend..."
# Retire the legacy unit name so two supervisors never race.
if [ -f "$SERVICE_DIR/$LEGACY_UNIT" ]; then
    "${SYSTEMCTL[@]}" stop "$LEGACY_UNIT" 2>/dev/null || true
    "${SYSTEMCTL[@]}" disable "$LEGACY_UNIT" 2>/dev/null || true
    rm -f "$SERVICE_DIR/$LEGACY_UNIT"
    echo "          legacy unit $LEGACY_UNIT retired"
fi
"${SYSTEMCTL[@]}" daemon-reload
"${SYSTEMCTL[@]}" enable "$UNIT_NAME" >/dev/null

if [ "$START" -eq 1 ]; then
    if "${SYSTEMCTL[@]}" is-active --quiet "$UNIT_NAME"; then
        "${SYSTEMCTL[@]}" restart "$UNIT_NAME"
    else
        "${SYSTEMCTL[@]}" start "$UNIT_NAME"
    fi
    echo "          verifying backend identity (bounded, 30 attempts)..."
    # Spec 082 (T012): /docs and /openapi.json are token-gated; the
    # install-time check presents this install's token file (the
    # supervised unit's data dir is the repo's backend/data).
    GLOSSA_TOKEN_FILE="$REPO_ROOT/backend/data/api_token" \
    "$VENV_PYTHON" "$SUPPORT_DIR/healthcheck.py" \
        --base-url "http://127.0.0.1:${PORT}" \
        --attempts 30 --interval 1 --timeout 3 \
        --state-dir "$STATE_DIR"
    echo "[OK] Backend supervised and identity-verified on port $PORT."
else
    echo "[OK] Installed and enabled; not started (--no-start)."
fi
echo "     unit:    $SERVICE_DIR/$UNIT_NAME"
echo "     logs:    $STATE_DIR/backend.log"
echo "     status:  ${SYSTEMCTL[*]} status $UNIT_NAME"
