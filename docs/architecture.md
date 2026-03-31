# Architecture

## High-level system

Glossa Lab is planned as a cross-platform application composed of four primary layers:

1. Python backend
2. React frontend
3. tray application
4. OS-specific service/startup integrations

## Component model

### 1. Python backend
Responsibilities:
- core application logic
- language/script analysis pipelines
- translation orchestration
- research workflows
- local APIs
- background task execution
- config and state management

Expected characteristics:
- cross-platform
- runnable in foreground for development
- runnable in background for service mode
- structured logs
- explicit config

### 2. React frontend
Responsibilities:
- user interface
- dashboards
- settings
- workflow/job management
- result inspection
- service visibility

The frontend should communicate with the backend through explicit local interfaces.

### 3. Tray application
Responsibilities:
- display local application status
- open the UI
- open logs or status pages
- start/stop/restart background services
- provide quick access to common actions

### 4. Service integrations
Responsibilities:
- start backend in background
- support clean startup and shutdown
- integrate with Windows and Linux startup expectations
- keep service behavior distinct from frontend or tray logic

## Platform expectations

### Windows
Target behavior:
- tray launches automatically at user login/startup
- tray can ensure background services are available
- tray can open the UI and expose service controls

### Linux
Target behavior:
- backend supports systemd startup
- documented user service and/or system service units
- tray support may depend on desktop environment and should be explicitly documented

### macOS
Target behavior:
- tray support is expected
- background services must have a documented macOS launch model
- startup/login behavior must be explicit and separate from Windows and Linux assumptions

## Boundary rules

### Backend vs frontend
- backend owns processing and stateful runtime behavior
- frontend owns user interaction and presentation
- no hidden shared mutable logic across layers

### Backend vs tray
- tray is a controller/status surface
- backend remains the service/process owner for application logic
- tray should talk to backend or service layer through documented interfaces

### Platform layer vs app layer
- platform-specific startup logic belongs under `services/`
- application behavior belongs under `backend/`, `frontend/`, or `tray/`

## Design principles

- keep service mode and development mode separate but compatible
- prefer explicit startup scripts over implicit behavior
- prefer documented IPC/API boundaries
- prefer stable local interfaces for tray <-> backend coordination
- document every platform assumption
