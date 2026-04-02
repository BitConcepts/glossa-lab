# Environment & Platform

## Environment Requirements

The project MUST be environment-controlled and system-agnostic.

---

## Python Environment (Required)

* use virtual environment
* do not rely on global Python
* environment must be reproducible

### Expected structure

```text
backend/
  venv/
```

or

```text
.venv/
```

---

## Env Bootstrap

Environment setup must be split:

### 1. Python-level

* dependency install
* environment config
* runtime setup

### 2. OS-level

Scripts must exist for:

* Windows (`.cmd`)
* Linux/macOS (`.sh`)

---

## Shell Wrapper (Critical)

All tool invocations MUST go through the unified shell wrapper:

```text
# Windows
shell.cmd <command> [args]

# Linux/macOS
./shell.sh <command> [args]
```

### Available commands

* `shell.cmd run` — start backend (dev mode, foreground)
* `shell.cmd test [args]` — run pytest
* `shell.cmd lint [args]` — run ruff check
* `shell.cmd format [args]` — run ruff format
* `shell.cmd setup` — re-run setup (install/update deps)
* `shell.cmd python [args]` — run Python in venv

### Why this exists

On Windows, calling venv `Scripts/*.exe` files directly (e.g. `ruff.exe`, `pytest.exe`) **hangs the PTY**. PowerShell `.ps1` wrappers also hang. The `.cmd` shell wrapper routes all invocations through `python.exe -m <module>` which does not hang.

### ABSOLUTELY FORBIDDEN

* ❌ `backend\venv\Scripts\ruff.exe ...`
* ❌ `backend\venv\Scripts\pytest.exe ...`
* ❌ `backend\venv\Scripts\uvicorn.exe ...`
* ❌ Any direct invocation of executables under `venv/Scripts/` or `venv/bin/`
* ❌ Any `.ps1` PowerShell script for tool invocation (causes PTY hangs)

### REQUIRED (safe, uses python -m)

* ✅ `shell.cmd test`
* ✅ `shell.cmd lint`
* ✅ `shell.cmd run`
* ✅ `shell.cmd python <script>`

### Auto-bootstrap

If the venv does not exist, `shell.cmd` / `shell.sh` will create it and install all dependencies automatically on first run.

---

## Additional Scripts

```text
scripts/
  setup.cmd
  setup.sh
  run.cmd
  run.sh
```

These are convenience wrappers. The canonical entry point is `shell.cmd` / `shell.sh` at the repo root.

---

## Platform Expectations

### Backend

* Python
* cross-platform
* service-compatible

### Frontend

* React
* API-driven

### Tray

* control surface only

### Services

* Windows + Linux + macOS support required

---

