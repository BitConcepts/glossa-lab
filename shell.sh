#!/usr/bin/env bash
# Glossa Lab Shell Wrapper (POSIX)
# ALL tool invocations MUST go through this file.
# NEVER call venv/bin/* directly.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$REPO_ROOT/backend/venv/bin/python"

# Bootstrap if venv missing
if [ ! -f "$VENV_PYTHON" ]; then
    echo "[SETUP] Creating venv ..."
    PYTHON_CMD="python3"
    command -v "$PYTHON_CMD" &>/dev/null || PYTHON_CMD="python"
    "$PYTHON_CMD" -m venv "$REPO_ROOT/backend/venv"
    "$VENV_PYTHON" -m pip install --quiet --upgrade pip
    "$VENV_PYTHON" -m pip install --quiet -e "$REPO_ROOT/backend[dev]"
    echo "[SETUP] Done."
fi

if [ $# -eq 0 ]; then
    echo "Usage: shell.sh <command> [args]"
    echo "  test [args]    pytest"
    echo "  lint [args]    ruff check"
    echo "  format [args]  ruff format"
    echo "  run [args]     uvicorn backend"
    echo "  python [args]  python in venv"
    echo "  setup          install/update deps"
    echo "  tray           start tray app"
    exit 0
fi

CMD="$1"
shift

case "$CMD" in
    test)
        exec "$VENV_PYTHON" -m pytest "$@"
        ;;
    lint)
        exec "$VENV_PYTHON" -m ruff check "$@"
        ;;
    format)
        exec "$VENV_PYTHON" -m ruff format "$@"
        ;;
    run)
        echo "[OK] Backend running on http://localhost:8000 (Ctrl+C to stop)"
        exec "$VENV_PYTHON" -m uvicorn glossa_lab.main:app \
            --host 127.0.0.1 --port 8000 --reload \
            --app-dir "$REPO_ROOT/backend" "$@"
        ;;
    python)
        exec "$VENV_PYTHON" "$@"
        ;;
    setup)
        "$VENV_PYTHON" -m pip install --upgrade pip
        "$VENV_PYTHON" -m pip install -e "$REPO_ROOT/backend[dev]"
        if [ -f "$REPO_ROOT/tray/requirements.txt" ]; then
            "$VENV_PYTHON" -m pip install -r "$REPO_ROOT/tray/requirements.txt"
        fi
        if [ -f "$REPO_ROOT/frontend/package.json" ]; then
            (cd "$REPO_ROOT/frontend" && npm install)
        fi
        echo "[OK] Dependencies updated."
        ;;
    tray)
        exec "$VENV_PYTHON" -m glossa_tray "$@"
        ;;
    *)
        exec "$VENV_PYTHON" -m "$CMD" "$@"
        ;;
esac
