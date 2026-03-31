# glossa-lab

Agentic research lab for decoding, translating, and modeling languages and scripts across ancient and modern systems through structure discovery, semantic analysis, and explainable workflows.

## Overview

Glossa Lab is intended to be a cross-platform platform with:

- a **Python backend**
- a **React frontend UI**
- a **tray application**
- **Windows startup + background-service support**
- **Linux background-service support via systemd**
- **macOS startup + background-service support**

The project is designed to support both research and product-style workflows:
- modern translation and language tooling,
- ancient script analysis and decipherment,
- structure-aware semantic modeling,
- explainable hypothesis testing,
- long-running background tasks and local services.

## Planned architecture

### Backend
A Python backend will provide:
- API endpoints
- local orchestration
- background jobs
- language-processing pipelines
- data/model management
- service-friendly execution

### Frontend
A React frontend will provide:
- local UI
- research and workflow controls
- service status visibility
- configuration and job views
- results visualization

### Tray
A desktop tray component will provide:
- quick service status
- open UI action
- start/stop/restart background services
- fast local access without opening a terminal

### Windows behavior
Windows support is expected to include:
- automatic tray startup on Windows login/startup
- the tray opening or controlling the background services
- a Windows-friendly local service model

### Linux behavior
Linux support is expected to include:
- systemd-based service startup
- documented user-service and/or system-service flows
- explicit notes for desktop/tray differences

### macOS behavior
macOS support is expected to include:
- tray support
- documented startup/login behavior
- documented background-service support

## Initial repository structure

```text
glossa-lab/
├─ AGENTS.md
├─ README.md
├─ .gitignore
├─ .gitattributes
├─ docs/
├─ backend/
├─ frontend/
├─ tray/
├─ services/
└─ scripts/
````

## Development principles

* specification first
* bounded tasks
* explicit service boundaries
* cross-platform awareness
* explainable workflows
* no silent architectural drift

## Documentation

* `docs/architecture.md` — system architecture
* `docs/workflow.md` — repo workflow conventions
* `docs/services.md` — service and startup expectations
* `AGENTS.md` — agent operating rules

## Near-term goals

1. scaffold Python backend
2. scaffold React frontend
3. define backend/frontend API boundary
4. define tray/service boundary
5. implement Windows startup + tray behavior
6. implement Linux systemd service flow
7. add packaging and smoke-test workflows

## Notes

This repo is currently a starter scaffold. It is intended to be safe to clone, organize, and begin staging before major implementation begins.
