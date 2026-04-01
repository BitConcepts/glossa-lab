# Requirements

Formal, numbered requirements for Glossa Lab. Each requirement is testable and traceable to the architecture.

**Naming convention:** `REQ-<COMPONENT>-<NUMBER>`

Components:
- `BE` — Backend
- `FE` — Frontend
- `TRAY` — Tray application
- `SVC` — Service/startup layer
- `API` — API boundary
- `CFG` — Configuration
- `LOG` — Logging/diagnostics
- `SEC` — Security
- `XP` — Cross-platform
- `INT` — Integration/boundary

**Status values:** `draft` → `accepted` → `implemented` → `verified`

---

## Backend

### REQ-BE-001 — Backend starts in foreground mode

The backend MUST be runnable in foreground mode for development. It MUST start an HTTP server, initialize logging, and report health within 10 seconds.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-BE-001
- **Status:** draft

### REQ-BE-002 — Backend starts in background/service mode

The backend MUST be runnable in background mode for installed deployments. Behavior must be identical to foreground mode except for process detachment and log routing.

- **Priority:** P2
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-BE-002
- **Status:** draft

### REQ-BE-003 — Backend clean shutdown

The backend MUST shut down cleanly on SIGTERM/SIGINT (POSIX) or CTRL_C_EVENT (Windows). Shutdown MUST complete within 60 seconds, finishing in-progress jobs, closing database connections, and flushing logs.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-BE-003
- **Status:** draft

### REQ-BE-004 — Backend database initialization

The backend MUST create the SQLite database file and run migrations automatically on first startup if the database does not exist. State paths MUST be created automatically.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-BE-004
- **Status:** draft

---

## API

### REQ-API-001 — Health endpoint

The backend MUST expose `GET /api/v1/health` returning JSON with `status`, `version`, and `uptime_seconds`. Response MUST arrive within 1 second. HTTP 200 for healthy/degraded, HTTP 503 only when unresponsive.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-API-001
- **Status:** draft

### REQ-API-002 — Status endpoint

The backend MUST expose `GET /api/v1/status` returning detailed system status including job counts and pipeline states.

- **Priority:** P2
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-API-002
- **Status:** draft

### REQ-API-003 — API versioning

All API endpoints MUST be prefixed with `/api/v1/`. Version bumps MUST follow a documented migration path.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-API-003
- **Status:** draft

### REQ-API-004 — CORS for development

The backend MUST enable CORS for `localhost` origins when running in development mode to support the frontend dev server.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-API-004
- **Status:** draft

---

## Configuration

### REQ-CFG-001 — TOML configuration file

The backend MUST load configuration from a TOML file at the platform-specific path. Missing config file MUST result in safe defaults, not a crash.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-CFG-001
- **Status:** draft

### REQ-CFG-002 — Environment variable overrides

Configuration values MUST be overridable by environment variables prefixed with `GLOSSA_`.

- **Priority:** P2
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-CFG-002
- **Status:** draft

### REQ-CFG-003 — Platform-specific config paths

Config file paths MUST follow platform conventions: `%APPDATA%` on Windows, `$XDG_CONFIG_HOME` on Linux, `~/Library/Application Support/` on macOS. Development mode MUST use `./config/glossa.toml`.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-CFG-003
- **Status:** draft

---

## Logging

### REQ-LOG-001 — Structured JSON logging

The backend MUST produce structured JSON log output to both console and file. Logs MUST include timestamp, level, module, and message.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-LOG-001
- **Status:** draft

### REQ-LOG-002 — Platform-specific log paths

Log file paths MUST follow platform conventions: `%LOCALAPPDATA%` on Windows, `$XDG_STATE_HOME` on Linux, `~/Library/Logs/` on macOS. Development mode MUST use `./logs/glossa.log`.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-LOG-002
- **Status:** draft

### REQ-LOG-003 — No secrets in logs

Logs MUST NOT contain secrets, API keys, tokens, or passwords under any circumstances.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-LOG-003
- **Status:** draft

---

## Security

### REQ-SEC-001 — Localhost binding only

The backend MUST bind to `127.0.0.1` only. Binding to `0.0.0.0` or any external interface requires explicit opt-in configuration.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-SEC-001
- **Status:** draft

### REQ-SEC-002 — No secrets in API responses

API responses MUST NOT contain secrets, API keys, tokens, or passwords. The `/api/v1/config` endpoint MUST return configuration without secret values.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-SEC-002
- **Status:** draft

---

## Frontend

### REQ-FE-001 — Frontend connects to backend API

The frontend MUST connect to the backend via the documented HTTP REST API at `http://localhost:8000/api/v1/`. It MUST NOT contain core application logic.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-FE-001
- **Status:** draft

### REQ-FE-002 — Frontend displays health status

The frontend MUST display the backend health status (healthy/degraded/down) obtained from the health endpoint.

- **Priority:** P2
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-FE-002
- **Status:** draft

### REQ-FE-003 — Frontend dev server

The frontend MUST be runnable via a local development server that supports hot reload and proxies API requests to the backend.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-FE-003
- **Status:** draft

---

## Tray

### REQ-TRAY-001 — Tray displays backend status

The tray application MUST display the current backend status (running/stopped/error) obtained from the health API.

- **Priority:** P2
- **Platform:** windows, macos
- **Testable:** yes
- **Test:** TEST-TRAY-001
- **Status:** draft

### REQ-TRAY-002 — Tray does not contain backend logic

The tray application MUST NOT contain core backend logic. It MUST communicate with the backend only through HTTP API or CLI commands.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-TRAY-002
- **Status:** draft

---

## Service/Startup

### REQ-SVC-001 — Windows startup

On Windows, the tray MUST start automatically at user login via a documented mechanism (Startup folder, registry, or scheduled task).

- **Priority:** P2
- **Platform:** windows
- **Testable:** yes
- **Test:** TEST-SVC-001
- **Status:** draft

### REQ-SVC-002 — Linux systemd service

On Linux, the backend MUST be manageable via a systemd user service unit. The unit file MUST be provided under `services/linux/`.

- **Priority:** P2
- **Platform:** linux
- **Testable:** yes
- **Test:** TEST-SVC-002
- **Status:** draft

### REQ-SVC-003 — macOS LaunchAgent

On macOS, the backend MUST be manageable via a LaunchAgent plist. The plist MUST be provided under `services/macos/`.

- **Priority:** P2
- **Platform:** macos
- **Testable:** yes
- **Test:** TEST-SVC-003
- **Status:** draft

---

## Cross-Platform

### REQ-XP-001 — Cross-platform backend

The backend MUST run on Windows, Linux, and macOS without platform-specific code in the core application. Platform-specific behavior MUST be isolated to configuration and service layers.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-XP-001
- **Status:** draft

### REQ-XP-002 — Bootstrap scripts

Setup and run scripts MUST exist for both Windows (`.cmd`) and POSIX (`.sh`). Scripts MUST be idempotent and create virtual environments automatically.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-XP-002
- **Status:** draft

### REQ-XP-003 — Environment isolation

The project MUST use a Python virtual environment. It MUST NOT depend on globally installed Python packages. The environment MUST be reproducible from a clean clone.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-XP-003
- **Status:** draft

---

## Integration/Boundary

### REQ-INT-001 — Frontend does not manage services

The frontend MUST NOT directly start, stop, or manage backend processes. Service lifecycle is the responsibility of the tray, service layer, or explicit CLI commands.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-INT-001
- **Status:** draft

### REQ-INT-002 — Version consistency

The `version` field in the health endpoint response MUST match the version declared in `backend/pyproject.toml`.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-INT-002
- **Status:** draft

---

## Analysis Pipelines

Components: `PIPE` — Pipeline/analysis engine

### REQ-PIPE-001 — Block entropy pipeline

The system MUST compute normalised block entropy H_N/ln(L) for block sizes N=1..6 on any uploaded text corpus. Results MUST include raw (nats) and normalised values.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-PIPE-001
- **Status:** implemented
- **Reference:** Rao et al. (2009), Science 324:1165

### REQ-PIPE-002 — Character frequency pipeline

The system MUST compute symbol frequencies, rank-frequency distribution, and Zipf exponent for any uploaded text corpus.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-PIPE-002
- **Status:** implemented

### REQ-PIPE-003 — Pipeline engine

The system MUST process queued jobs asynchronously via a background engine. Jobs MUST transition through pending → running → completed/failed states. Results MUST be stored and retrievable.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-PIPE-003
- **Status:** implemented

---

## Kandles Phonetic-Visual Analysis

Components: `KDL` — Kandles system (per US 2024/0248922 A1, Merkur)

### REQ-KDL-001 — Kandles phonetic mapping

The system MUST implement the Kandles phonetic-to-color mapping: 7 consonant sound groups mapped to 7 colors (Yellow, Grey, Red, Blue, Green, Purple, Brown). Vowel-initial words MUST be mapped to a distinct group (group 0).

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-KDL-001
- **Status:** draft
- **Patent:** US 2024/0248922 A1 [0109]-[0110]

### REQ-KDL-002 — Kandles color-coded text

The system MUST generate color-coded text output where each word is assigned a color based on the phonetic sound at the beginning of the word, per the Kandles mapping.

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-KDL-002
- **Status:** draft
- **Patent:** US 2024/0248922 A1 [0007], [0117]

### REQ-KDL-003 — Kandles color grid

The system MUST generate a color-coded grid (equal rows and columns) from any text, where each cell corresponds to a word and is colored by the Kandles system. The grid MUST also encode the Kandles number (1-7).

- **Priority:** P1
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-KDL-003
- **Status:** draft
- **Patent:** US 2024/0248922 A1 [0124]-[0125], FIG. 29 step 2916

### REQ-KDL-004 — Cross-language Kandles comparison

The system MUST be able to generate Kandles grids for texts in different languages/scripts and compare the resulting color patterns. The comparison MUST produce a similarity metric.

- **Priority:** P2
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-KDL-004
- **Status:** draft
- **Patent:** US 2024/0248922 A1 [0110], FIG. 20

---

## Hierarchical Text Decomposition

Components: `HTD` — Hierarchical text decomposition (per US 2024/0248922 A1, Merkur)

### REQ-HTD-001 — Text decomposition into stories and slices

The system MUST support organizing a written work into one or more stories, where each story is comprised of one or more slices. Each slice MUST be independently addressable.

- **Priority:** P2
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-HTD-001
- **Status:** draft
- **Patent:** US 2024/0248922 A1 [0072], [0095], FIG. 29 steps 2902-2904

### REQ-HTD-002 — Slice filtering by clusters and tags

The system MUST support filtering slices by user-selected semantic clusters and/or manual tags. Multiple clusters MUST be combinable (AND/OR).

- **Priority:** P2
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-HTD-002
- **Status:** draft
- **Patent:** US 2024/0248922 A1 [0095]-[0098], FIG. 29 step 2906

---

## Semantic Cluster Tagging

Components: `SEM` — Semantic analysis

### REQ-SEM-001 — Configurable semantic taxonomy

The system MUST support a configurable taxonomy of semantic clusters. Default clusters MUST include at least: Culture, Nations, Nature, Religion, People, and Spiritual.

- **Priority:** P2
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-SEM-001
- **Status:** draft
- **Patent:** US 2024/0248922 A1 [0010], [0080]

### REQ-SEM-002 — Manual tagging

The system MUST support manual tagging of text segments with user-defined labels.

- **Priority:** P3
- **Platform:** all
- **Testable:** yes
- **Test:** TEST-SEM-002
- **Status:** draft
- **Patent:** US 2024/0248922 A1 [0011], [0104]
