#!/usr/bin/env bash
# Sets up the Glossa Lab development environment on Linux/macOS.
# Creates a Python virtual environment, installs backend dependencies,
# and installs frontend dependencies. Idempotent — safe to run multiple times.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== Glossa Lab Setup ==="

# --- Python backend setup ---
VENV_PATH="$REPO_ROOT/backend/venv"
PYTHON_CMD="python3"

# Verify Python is available
if ! command -v "$PYTHON_CMD" &>/dev/null; then
    echo "[ERROR] python3 not found. Install Python 3.11+ and ensure it is on PATH."
    exit 1
fi

PY_VERSION=$("$PYTHON_CMD" --version 2>&1)
echo "[OK] Found $PY_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "[..] Creating virtual environment at backend/venv ..."
    "$PYTHON_CMD" -m venv "$VENV_PATH"
    echo "[OK] Virtual environment created."
else
    echo "[OK] Virtual environment already exists."
fi

# Activate and install dependencies
# shellcheck disable=SC1091
source "$VENV_PATH/bin/activate"

if [ -f "$REPO_ROOT/backend/pyproject.toml" ]; then
    echo "[..] Installing backend dependencies ..."
    pip install -e "$REPO_ROOT/backend[dev]" --quiet 2>&1
    echo "[OK] Backend dependencies installed."
else
    echo "[WARN] No backend/pyproject.toml found. Skipping backend deps."
fi

# --- Frontend setup ---
if [ -f "$REPO_ROOT/frontend/package.json" ]; then
    if command -v npm &>/dev/null; then
        echo "[..] Installing frontend dependencies ..."
        (cd "$REPO_ROOT/frontend" && npm install --silent 2>&1)
        echo "[OK] Frontend dependencies installed."
    else
        echo "[WARN] npm not found. Skipping frontend deps. Install Node.js 18+."
    fi
else
    echo "[WARN] No frontend/package.json found. Skipping frontend deps."
fi

echo ""
echo "=== Setup complete ==="
echo "Run './scripts/run.sh' to start the application."
