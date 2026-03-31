# Backend

This directory contains the Python backend for Glossa Lab.

The backend is the **primary runtime authority** for the application. It owns core logic, system state, orchestration, and long-running work. Frontend and tray layers interact with the backend through explicit interfaces and do not replace backend responsibilities.

## Responsibilities

- local APIs
- background jobs and task orchestration
- language and script analysis pipelines
- translation and interpretation workflows
- research workflow execution
- config and state management
- structured logging and diagnostics
- service-friendly runtime behavior
- health, status, and readiness reporting

## Expected characteristics

- cross-platform
- runnable in foreground for development
- runnable in background for installed/service mode
- deterministic startup and shutdown behavior
- explicit configuration
- observable runtime state
- clear interfaces for frontend and tray integration

## Design rules

- core application logic lives here
- meaningful runtime state lives here
- long-running processing lives here
- tray and frontend communicate through explicit API or IPC boundaries
- platform-specific startup logic does **not** belong here unless it is truly backend-runtime-specific

## Planned structure

Planned future additions include:

- Python project configuration
- application package
- API layer
- service entrypoint
- job runner / worker layer
- pipeline modules
- config module
- logging and diagnostics
- tests

## Development expectations

The backend should support at least two modes:

### Development mode
- runs in foreground
- easy local startup
- service installation not required

### Installed mode
- runs as a background service or managed process
- stable local endpoint for frontend and tray communication
- explicit logs, config paths, and health checks

## Near-term implementation targets

1. Python project scaffold
2. backend entrypoint
3. config and logging setup
4. health/status endpoint
5. background job model
6. first pipeline interface
7. service-friendly startup contract
