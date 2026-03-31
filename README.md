# glossa-lab

Agentic research lab for decoding, translating, and modeling languages and scripts across ancient and modern systems through structure discovery, semantic analysis, and explainable workflows.

---

## Overview

Glossa Lab is a cross-platform system designed for both research and product-style language workflows.

It combines:

- a **Python backend (runtime authority)**
- a **React frontend UI (user interaction layer)**
- a **tray application (local control surface)**
- **Windows, Linux, and macOS service/startup support**

The system is built to support:

- modern translation and language tooling
- ancient script analysis and decipherment
- structure-aware semantic modeling
- explainable hypothesis testing
- long-running background processing
- local-first services with deterministic behavior

---

## System architecture

Glossa Lab follows a **service-first architecture**:

```text
[ Tray ] ─────┐
              │
[ Frontend ] ─┼──→ [ Backend Service ] ───→ [ Pipelines / Jobs / Models ]
              │
[ CLI / Dev ] ┘
````

### Key principles

* the backend is the **source of truth**
* the tray and frontend are **interfaces**, not runtime owners
* all communication occurs through **explicit interfaces**
* service lifecycle is **deterministic and observable**

---

## Components

### Backend (Python)

The backend is the core system.

Responsibilities:

* APIs and orchestration
* background jobs and pipelines
* translation and analysis workflows
* config and state management
* logging, health, and observability

Characteristics:

* cross-platform
* service-friendly
* deterministic startup/shutdown
* explicit configuration

---

### Frontend (React)

The frontend is the primary UI layer.

Responsibilities:

* dashboards and configuration
* workflow and job management
* results and visualization
* service status visibility

Rules:

* communicates only via backend APIs
* contains no core application logic
* does not manage services

---

### Tray

The tray is a local control surface.

Responsibilities:

* quick system status
* open UI
* service control (start/stop/restart)
* fast local access to common actions

Rules:

* does not contain backend logic
* does not own application state
* communicates via explicit interfaces

---

## Platform behavior

### Windows

* tray starts automatically on login/startup
* tray can control backend services
* backend runs in a stable background service or managed process

### Linux

* backend supports systemd-based startup
* user services preferred for local installs
* tray behavior depends on desktop environment and is documented explicitly

### macOS

* tray is a first-class experience
* backend uses macOS-native startup mechanisms (e.g., LaunchAgent)
* startup/login behavior is explicit and documented

---

## Repository structure

```text
glossa-lab/
├─ AGENTS.md
├─ README.md
├─ .gitignore
├─ .gitattributes
├─ docs/
│  ├─ architecture.md
│  ├─ workflow.md
│  └─ services.md
├─ backend/
├─ frontend/
├─ tray/
├─ services/
│  ├─ windows/
│  ├─ linux/
│  └─ macos/
└─ scripts/
```

---

## Development model

This repository follows a **specification-first, proposal-driven workflow**.

Before non-trivial work:

1. load context
2. restate objective
3. define scope and constraints
4. produce proposal
5. execute bounded task
6. verify results
7. document outcomes and uncertainty

See `AGENTS.md` and `docs/workflow.md` for full rules.

---

## Design principles

* service-first architecture
* explicit ownership of state
* deterministic lifecycle behavior
* cross-platform clarity over shortcuts
* explicit interfaces over implicit coupling
* documentation as part of implementation
* no silent architectural drift

---

## Documentation

* `docs/architecture.md` — system architecture
* `docs/workflow.md` — development workflow
* `docs/services.md` — service and startup expectations
* `AGENTS.md` — agent operating rules

---

## Near-term goals

1. scaffold Python backend
2. scaffold React frontend
3. define backend ↔ frontend API boundary
4. define tray ↔ backend interaction model
5. implement Windows startup and tray behavior
6. implement Linux systemd service support
7. implement macOS startup model
8. add packaging and smoke-test workflows

---

## Status

This repository is currently a scaffold.

It is safe to:

* clone
* organize
* stage architecture and workflow
* begin bounded implementation

Major runtime features are not yet implemented.
