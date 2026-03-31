#!/usr/bin/env bash
# Starts Glossa Lab in development mode on Linux/macOS.
# Activates the Python virtual environment and starts the backend server.
# Usage:
#   ./scripts/run.sh              # backend only (default)
#   ./scripts/run.sh --frontend   # frontend only
#   ./scripts/run.sh --all        # both backend and frontend

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

RUN_BACKEND=false
RUN_FRONTEND=false

# Parse arguments
if [ $# -eq 0 ]; then
    RUN_BACKEND=true
fi

for arg in "$@"; do
    case "$arg" in
        --backend)  RUN_BACKEND=true ;;
        --frontend) RUN_FRONTEND=true ;;
        --all)      RUN_BACKEND=true; RUN_FRONTEND=true ;;
        *)          echo "Unknown argument: $arg"; exit 1 ;;
    esac
done

# --- Backend ---
if [ "$RUN_BACKEND" = true ]; then
    VENV_PATH="$REPO_ROOT/backend/venv"

    if [ ! -f "$VENV_PATH/bin/activate" ]; then
        echo "[ERROR] Virtual environment not found. Run './scripts/setup.sh' first."
        exit 1
    fi

    # shellcheck disable=SC1091
    source "$VENV_PATH/bin/activate"

    echo "[..] Starting Glossa Lab backend ..."

    if [ "$RUN_FRONTEND" = true ]; then
        # Start backend in background if we also need frontend
        (cd "$REPO_ROOT/backend" && python -m uvicorn glossa_lab.main:app --host 127.0.0.1 --port 8000 --reload) &
        echo "[OK] Backend started in background on http://localhost:8000"
    else
        echo "[OK] Backend running on http://localhost:8000 (Ctrl+C to stop)"
        cd "$REPO_ROOT/backend"
        exec python -m uvicorn glossa_lab.main:app --host 127.0.0.1 --port 8000 --reload
    fi
fi

# --- Frontend ---
if [ "$RUN_FRONTEND" = true ]; then
    if [ ! -f "$REPO_ROOT/frontend/package.json" ]; then
        echo "[ERROR] No frontend/package.json found. Run './scripts/setup.sh' first."
        exit 1
    fi

    echo "[..] Starting frontend dev server ..."
    cd "$REPO_ROOT/frontend"
    exec npm run dev
fi
