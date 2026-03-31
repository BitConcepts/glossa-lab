# Architecture

## High-level system

Glossa Lab is a cross-platform application composed of four primary layers:

1. Python backend
2. React frontend
3. tray application
4. OS-specific service/startup integrations

The system is designed as a **service-first architecture** where:

- the backend is the **runtime authority**
- the tray is a **control and visibility layer**
- the frontend is a **user interaction layer**
- the platform layer manages **startup and lifecycle**

---

## System model

At runtime, the system behaves as:

```text
[ Tray ] ─────┐
              │
[ Frontend ] ─┼──→ [ Backend Service ] ───→ [ Pipelines / Jobs / Models ]
              │
[ CLI / Dev ] ┘
````

Key rule:

> All meaningful application state and logic lives in the backend.

The frontend and tray **do not own state**, they interact with it.

---

## Component model

### 1. Python backend

The backend is the **core system authority**.

#### Responsibilities

* core application logic
* language/script analysis pipelines
* translation orchestration
* research workflows
* local APIs
* background task execution
* config and state management

#### Expected characteristics

* cross-platform
* runnable in foreground (development mode)
* runnable in background (service mode)
* deterministic startup and shutdown
* structured logs
* explicit configuration
* observable state (health, status, jobs)

#### Design expectation

* all long-running work happens here
* all pipelines are orchestrated here
* all system truth is derived from here

---

### 2. React frontend

The frontend is the **primary user interface**.

#### Responsibilities

* dashboards
* configuration
* workflow/job management
* result inspection
* service visibility

#### Rules

* communicates only via explicit backend interfaces (HTTP/IPC)
* contains no core business logic
* does not assume process ownership
* does not directly manage services

---

### 3. Tray application

The tray is a **local control and status surface**.

#### Responsibilities

* display system status
* open the UI
* open logs or status views
* start/stop/restart backend services
* provide quick access to core actions

#### Rules

* MUST NOT contain backend logic
* MUST NOT act as hidden runtime
* MUST communicate via explicit interfaces (API, IPC, CLI)
* MUST remain replaceable without affecting backend behavior

---

### 4. Service integrations

The service layer is responsible for **process lifecycle management**.

#### Responsibilities

* start backend in background
* stop and restart services cleanly
* integrate with OS-native startup mechanisms
* ensure deterministic lifecycle behavior

#### Rules

* service logic is isolated under `services/`
* no platform-specific logic leaks into backend core
* development mode must NOT depend on installed services

---

## Platform expectations

### Windows

Target behavior:

* tray launches automatically at user login/startup
* tray ensures backend service availability
* tray exposes service control (start/stop/restart)
* backend runs in a stable background service or managed process

---

### Linux

Target behavior:

* backend supports systemd-based startup
* user services preferred for local installs
* system services optional for system-wide installs
* tray behavior is environment-dependent and must be documented explicitly

---

### macOS

Target behavior:

* tray support is a first-class experience
* backend uses macOS-native service mechanisms (e.g., LaunchAgent)
* login/startup behavior is explicit and documented
* service lifecycle is deterministic and observable

---

## Boundary rules

### Backend vs frontend

* backend owns all processing and state
* frontend owns presentation only
* no shared hidden state
* no duplicated logic

---

### Backend vs tray

* backend owns runtime authority
* tray is a controller and observer
* tray interacts via explicit APIs or IPC
* tray never embeds backend logic

---

### Platform vs application

* platform-specific startup logic lives in `services/`
* application logic lives in `backend/`, `frontend/`, `tray/`
* platform behavior must be explicitly documented per OS

---

## Interaction model

### Backend interfaces

The backend must expose:

* health/status endpoint
* job/workflow endpoints
* service lifecycle endpoints (where appropriate)
* logs or diagnostics access

---

### Tray ↔ backend

Communication must use one of:

* local HTTP API
* IPC (sockets, pipes)
* CLI/service wrapper commands

No implicit coupling is allowed.

---

### Frontend ↔ backend

Communication must use:

* explicit API endpoints
* versioned or stable interfaces where possible

---

## Runtime modes

### Development mode

* backend runs in foreground
* frontend runs via dev server
* tray is optional
* services are not required

---

### Installed mode

* backend runs in background service mode
* tray starts automatically where supported
* frontend connects to stable local endpoint
* logs and config paths are explicit

---

## Design principles

* service-first architecture
* explicit ownership of state
* deterministic lifecycle behavior
* cross-platform clarity over shortcuts
* explicit interfaces over implicit coupling
* documentation as part of implementation

---

## Constraints

* no hidden service startup logic
* no tray-controlled business logic
* no platform assumptions copied between OSes
* no undocumented backend ↔ tray coupling
* no implicit state outside backend authority

---

## API boundary specification

The backend exposes a local HTTP REST API. This is the sole interface for frontend and tray communication.

### Base URL

* Development mode: `http://localhost:8000`
* Installed mode: `http://localhost:8000` (same, stable local endpoint)

### Versioning

* All API routes are prefixed with `/api/v1/`
* Version bumps require a documented migration path

### Core endpoints

* `GET /api/v1/health` — health and readiness
* `GET /api/v1/status` — detailed system status (jobs, pipelines, uptime)
* `GET /api/v1/config` — current configuration (read-only, no secrets)
* `POST /api/v1/jobs` — submit a job
* `GET /api/v1/jobs` — list jobs
* `GET /api/v1/jobs/{id}` — job detail
* `DELETE /api/v1/jobs/{id}` — cancel a job

Additional endpoints will be added as pipelines and workflows are implemented.

---

## Health and status contract

### `GET /api/v1/health`

Returns:

```json
{
  "status": "healthy" | "degraded" | "down",
  "version": "0.1.0",
  "uptime_seconds": 3600
}
```

Rules:

* MUST return within 1 second
* MUST return HTTP 200 even when status is "degraded" (use body to convey state)
* MUST return HTTP 503 only when the service cannot respond at all
* `version` MUST match the version in `pyproject.toml`

---

## Configuration model

### Format

Configuration uses TOML as the primary format.

### Load order (later overrides earlier)

1. Built-in defaults (in code)
2. Config file at platform-specific path (see below)
3. Environment variables prefixed with `GLOSSA_`
4. CLI flags (if running from command line)

### Platform-specific config paths

* **Development mode (all platforms):** `./config/glossa.toml` (relative to repo root)
* **Windows installed:** `%APPDATA%\GlossaLab\config.toml`
* **Linux installed:** `$XDG_CONFIG_HOME/glossa-lab/config.toml` (default: `~/.config/glossa-lab/config.toml`)
* **macOS installed:** `~/Library/Application Support/GlossaLab/config.toml`

### Secrets

Secrets (API keys, tokens) are NEVER stored in the config file. They are loaded from:

* Environment variables
* A `.env` file (development mode only, gitignored)
* OS-native secret stores (future)

---

## Logging model

### Format

Structured JSON logging to both console and file.

### Log levels

* `DEBUG` — verbose, development only
* `INFO` — normal operation
* `WARNING` — recoverable issues
* `ERROR` — failures requiring attention
* `CRITICAL` — system-level failures

### Log file paths

* **Development mode (all platforms):** `./logs/glossa.log` (relative to repo root)
* **Windows installed:** `%LOCALAPPDATA%\GlossaLab\logs\glossa.log`
* **Linux installed:** `$XDG_STATE_HOME/glossa-lab/logs/glossa.log` (default: `~/.local/state/glossa-lab/logs/glossa.log`)
* **macOS installed:** `~/Library/Logs/GlossaLab/glossa.log`

### Rules

* Default log level: `INFO` in installed mode, `DEBUG` in development mode
* Log rotation: daily, retain 7 days
* Logs MUST include timestamp, level, module, and message
* Logs MUST NOT contain secrets

---

## State model

The backend owns all persistent state.

### Storage

* SQLite for structured data (jobs, config state, pipeline metadata)
* Filesystem for large artifacts (model files, analysis outputs, uploads)

### State file paths

* **Development mode (all platforms):** `./data/glossa.db` and `./data/` (relative to repo root)
* **Windows installed:** `%LOCALAPPDATA%\GlossaLab\data\`
* **Linux installed:** `$XDG_DATA_HOME/glossa-lab/` (default: `~/.local/share/glossa-lab/`)
* **macOS installed:** `~/Library/Application Support/GlossaLab/data/`

### Rules

* No state lives outside the backend
* Frontend and tray are stateless with respect to application data
* State paths MUST be configurable via config file
* State paths MUST be created automatically if they do not exist

---

## IPC and communication model

### Frontend ↔ backend

* HTTP REST API (see API boundary specification above)
* Frontend connects to `http://localhost:8000` by default
* CORS enabled for `localhost` origins in development mode

### Tray ↔ backend

* HTTP REST API for status queries and service control
* Same API as frontend — no separate tray-specific API
* Tray MAY additionally use CLI subprocess invocation for service start/stop/restart

### Rules

* No shared memory between components
* No implicit IPC (pipes, signals) between frontend/tray and backend
* All communication goes through documented HTTP endpoints or explicit CLI commands

---

## Process lifecycle contract

### Startup sequence

1. Load configuration (config file → env vars → CLI flags)
2. Initialize logging
3. Initialize database (create if not exists, run migrations)
4. Start HTTP server
5. Report health as "healthy"

### Shutdown sequence

1. Stop accepting new requests
2. Finish in-progress jobs (with configurable timeout, default 30s)
3. Close database connections
4. Flush and close log files
5. Exit with code 0 (clean) or 1 (error)

### Signal handling

* `SIGTERM` / `SIGINT` — initiate clean shutdown
* `SIGHUP` — reload configuration (future)
* On Windows: `CTRL_C_EVENT` and `CTRL_BREAK_EVENT` initiate clean shutdown

### Rules

* Startup MUST complete within 10 seconds or report failure
* Shutdown MUST complete within 60 seconds or force-exit
* All lifecycle transitions MUST be logged

---

## Security model

### Scope

Glossa Lab is a **local-first application**. All communication is localhost-only by default.

### Rules

* Backend binds to `127.0.0.1` only (not `0.0.0.0`)
* No authentication required for local API access (local trust model)
* Secrets are never logged, never returned in API responses, never stored in config files
* If remote access is needed in future, it MUST be behind explicit opt-in configuration with authentication

---

## Technology decisions

### DEC-001 — Backend framework: FastAPI

* **Date:** 2026-03-31
* **Status:** accepted
* **Rationale:** async support, automatic OpenAPI docs, lightweight, Python-native, good ecosystem
* **Alternatives considered:** Flask, Django, Litestar

### DEC-002 — Frontend framework: React + Vite

* **Date:** 2026-03-31
* **Status:** accepted
* **Rationale:** React specified in project scope, Vite is fast and modern, good TypeScript support
* **Alternatives considered:** Create React App (deprecated), Next.js (overkill for local app)

### DEC-003 — Configuration format: TOML

* **Date:** 2026-03-31
* **Status:** accepted
* **Rationale:** Python-native (tomllib in stdlib), human-readable, good for app config
* **Alternatives considered:** YAML, JSON, INI

### DEC-004 — Database: SQLite

* **Date:** 2026-03-31
* **Status:** accepted
* **Rationale:** zero-dependency, file-based, cross-platform, sufficient for local-first app
* **Alternatives considered:** PostgreSQL (overkill), JSON files (no query support)

### DEC-005 — Tray framework: TBD

* **Date:** 2026-03-31
* **Status:** proposed — awaiting decision
* **Candidates:** Tauri, Electron, pystray, native per-platform
* **Notes:** decision deferred until Milestone 3

### DEC-006 — Package manager (frontend): npm

* **Date:** 2026-03-31
* **Status:** accepted
* **Rationale:** universal, no additional install, lockfile support
* **Alternatives considered:** pnpm, yarn

---

## Future extensions

The architecture must support:

* distributed or remote backends
* multiple concurrent pipelines
* model/plugin systems
* research workflow extensions
* advanced observability and tracing

The current design should not block these capabilities.
