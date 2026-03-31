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

## Future extensions

The architecture must support:

* distributed or remote backends
* multiple concurrent pipelines
* model/plugin systems
* research workflow extensions
* advanced observability and tracing

The current design should not block these capabilities.
