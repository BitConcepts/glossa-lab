#!/usr/bin/env bash
# ============================================================
# Glossa Lab — OS Integration Setup Tool (Linux / macOS)
# ============================================================
#
# Usage:
#   ./setup-os.sh install    Install deps + register system service
#   ./setup-os.sh uninstall  Remove system service
#   ./setup-os.sh start      Start the backend service
#   ./setup-os.sh stop       Stop the backend service
#   ./setup-os.sh restart    Restart the backend service
#   ./setup-os.sh status     Show current integration status
#
# Linux  : systemd user unit  (services/linux/)
# macOS  : LaunchAgent plist  (services/macos/)
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
OS="$(uname -s)"
HEALTH_URL="http://127.0.0.1:8001/api/v1/health"
LOG_DIR="$REPO_ROOT/logs"

# ── Helpers ───────────────────────────────────────────────────

check_health() {
    if curl -sf --max-time 3 "$HEALTH_URL" >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

wait_for_backend() {
    local tries=0
    echo "    Waiting for backend to start..."
    while ! check_health; do
        sleep 1
        tries=$((tries + 1))
        if [ "$tries" -ge 20 ]; then
            echo "[ERROR] Backend did not start within 20 seconds."
            echo "        Check logs at: $LOG_DIR/backend.log"
            return 1
        fi
    done
    echo "[OK] Backend running at $HEALTH_URL (${tries}s)"
}

# ── Install ───────────────────────────────────────────────────

do_install() {
    echo ""
    echo "[INSTALL] Installing Glossa Lab OS integration..."
    echo ""

    # 1. Install dependencies
    echo "[1/3] Installing dependencies..."
    chmod +x "$REPO_ROOT/shell.sh"
    "$REPO_ROOT/shell.sh" setup
    echo "[OK] Dependencies installed."

    # 2. Ensure logs directory
    mkdir -p "$LOG_DIR"
    echo "[2/3] Log directory: $LOG_DIR"

    # 3. Register service
    echo "[3/3] Registering service..."
    if [ "$OS" = "Linux" ]; then
        bash "$REPO_ROOT/services/linux/install.sh"
    elif [ "$OS" = "Darwin" ]; then
        bash "$REPO_ROOT/services/macos/install.sh"
    else
        echo "[WARN] Unknown OS '$OS' — skipping service registration."
        echo "       Supported: Linux (systemd), Darwin (LaunchAgent)"
    fi

    echo ""
    echo "[INSTALL COMPLETE]"
    echo "  Backend will start automatically via your OS service manager."
    echo "  To start it right now: ./setup-os.sh start"
    echo ""
}

# ── Uninstall ─────────────────────────────────────────────────

do_uninstall() {
    echo "[UNINSTALL] Removing Glossa Lab OS integration..."

    # Try graceful stop first
    do_stop 2>/dev/null || true

    if [ "$OS" = "Linux" ]; then
        bash "$REPO_ROOT/services/linux/uninstall.sh"
    elif [ "$OS" = "Darwin" ]; then
        bash "$REPO_ROOT/services/macos/uninstall.sh"
    else
        echo "[WARN] Unknown OS — nothing to uninstall."
    fi

    echo "[UNINSTALL COMPLETE]"
}

# ── Start ─────────────────────────────────────────────────────

do_start() {
    if check_health; then
        echo "[OK] Backend already running at $HEALTH_URL"
        return 0
    fi

    mkdir -p "$LOG_DIR"

    if [ "$OS" = "Linux" ]; then
        echo "[START] Starting via systemd..."
        systemctl --user start glossa-lab.service
        wait_for_backend
    elif [ "$OS" = "Darwin" ]; then
        echo "[START] Starting via launchctl..."
        PLIST="$HOME/Library/LaunchAgents/com.glossalab.backend.plist"
        if [ -f "$PLIST" ]; then
            launchctl load -w "$PLIST"
        else
            echo "[WARN] LaunchAgent plist not found at $PLIST"
            echo "       Run: ./setup-os.sh install"
        fi
        wait_for_backend
    else
        # Fallback: start directly in background
        echo "[START] Starting backend directly (no OS service manager)..."
        nohup "$REPO_ROOT/shell.sh" run >> "$LOG_DIR/backend.log" 2>&1 &
        wait_for_backend
    fi
}

# ── Stop ──────────────────────────────────────────────────────

do_stop() {
    echo "[STOP] Stopping Glossa Lab backend..."

    # Graceful shutdown via API
    if check_health; then
        curl -sf -X POST "http://127.0.0.1:8001/api/v1/shutdown" >/dev/null 2>&1 || true
        sleep 2
    fi

    if [ "$OS" = "Linux" ]; then
        systemctl --user stop glossa-lab.service 2>/dev/null || true
    elif [ "$OS" = "Darwin" ]; then
        PLIST="$HOME/Library/LaunchAgents/com.glossalab.backend.plist"
        [ -f "$PLIST" ] && launchctl unload "$PLIST" 2>/dev/null || true
    else
        # Kill by port as fallback
        PID=$(lsof -ti tcp:8001 2>/dev/null || true)
        [ -n "$PID" ] && kill -TERM "$PID" 2>/dev/null || true
    fi

    echo "[OK] Stop complete."
}

# ── Restart ───────────────────────────────────────────────────

do_restart() {
    echo "[RESTART] Restarting..."
    do_stop
    sleep 1
    do_start
}

# ── Status ────────────────────────────────────────────────────

do_status() {
    echo ""
    echo "── Glossa Lab Integration Status ─────────────────────────────"

    if [ "$OS" = "Linux" ]; then
        if systemctl --user is-enabled glossa-lab.service >/dev/null 2>&1; then
            echo "  Service (systemd) : enabled"
            systemctl --user is-active glossa-lab.service >/dev/null 2>&1 \
                && echo "  Service state     : active (running)" \
                || echo "  Service state     : inactive"
        else
            echo "  Service (systemd) : NOT installed (run: ./setup-os.sh install)"
        fi
    elif [ "$OS" = "Darwin" ]; then
        PLIST="$HOME/Library/LaunchAgents/com.glossalab.backend.plist"
        if [ -f "$PLIST" ]; then
            echo "  Service (LaunchAgent): installed at $PLIST"
        else
            echo "  Service (LaunchAgent): NOT installed (run: ./setup-os.sh install)"
        fi
    fi

    if check_health; then
        JSON="$(curl -sf --max-time 3 "$HEALTH_URL" 2>/dev/null || echo '{}')"
        echo "  Backend health    : RUNNING at $HEALTH_URL"
        echo "                      $JSON"
    else
        echo "  Backend health    : NOT RESPONDING at $HEALTH_URL"
    fi

    echo "──────────────────────────────────────────────────────────────"
    echo ""
}

# ── Main ──────────────────────────────────────────────────────

CMD="${1:-}"
case "$CMD" in
    install)   do_install ;;
    uninstall) do_uninstall ;;
    start)     do_start ;;
    stop)      do_stop ;;
    restart)   do_restart ;;
    status)    do_status ;;
    *)
        echo ""
        echo "Glossa Lab OS Integration Tool (Linux / macOS)"
        echo ""
        echo "Usage: ./setup-os.sh <command>"
        echo ""
        echo "Commands:"
        echo "  install    Install deps + register OS service"
        echo "  uninstall  Remove OS service"
        echo "  start      Start backend"
        echo "  stop       Stop backend"
        echo "  restart    Restart backend"
        echo "  status     Show integration status"
        echo ""
        if [ -n "$CMD" ]; then
            echo "[ERROR] Unknown command: $CMD"
            exit 1
        fi
        exit 0
        ;;
esac
