# Services and Startup

## Purpose

This document defines startup and background-service expectations for Glossa Lab.

## Core requirement

The application must support:

- foreground development mode
- background service mode
- cross-platform startup flows (Windows, Linux, macOS)
- tray-aware local control

---

## Windows expectations

### Required behavior
- the tray starts automatically on Windows startup / user login
- the tray can open the application UI
- the tray can start, stop, or ensure background services are running
- service status is visible from the tray

### Notes
Exact implementation may use:
- Startup folder entry
- Run registry entry
- scheduled task
- Windows service model
- another documented approach

The implementation choice MUST be explicit and documented.

---

## Linux expectations

### Required behavior
- background services can be started via systemd
- service units are defined under `services/linux/`
- user-service and/or system-service behavior is documented clearly

### Notes
- systemd user services are preferred for developer/local installs
- system services may be used for system-wide installs
- tray behavior depends on desktop environment and packaging
- Linux tray support MUST be documented explicitly and not assumed equivalent to Windows

---

## macOS expectations

### Required behavior
- background services can be started using macOS-native mechanisms
- tray behavior is supported and documented
- login/startup behavior is explicitly defined
- service lifecycle is deterministic (start, stop, restart)

### Notes
Implementation may use:
- LaunchAgent (user-level)
- LaunchDaemon (system-level)
- login item integration (for tray app)
- another documented macOS-native approach

The implementation choice MUST be explicit and documented.

---

## Service separation

The backend service is the **primary runtime authority**.

- the backend owns application logic and state
- the tray is a controller and status surface
- the frontend is a UI layer

Rules:
- the tray MUST NOT contain core backend logic
- the frontend MUST NOT assume direct process ownership
- service lifecycle must remain explicit and inspectable

---

## Tray ↔ Service interaction

The tray interacts with services via **explicit interfaces only**, such as:

- local HTTP API
- IPC (named pipes, sockets, etc.)
- CLI/service wrapper commands

Implicit coupling (shared memory, hidden process assumptions) is not allowed.

---

## Development mode vs installed mode

### Development mode
- backend runs in foreground or dev-managed process
- frontend runs from dev server or local build
- tray may be optional
- services are NOT required but should be emulatable

### Installed mode
- backend runs in background service mode
- tray starts at login where supported
- frontend is reachable via stable local endpoint
- logs and configuration locations are explicit and documented

---

## Observability requirements

All service implementations MUST support:

- clear startup success/failure signals
- structured logs
- deterministic shutdown behavior
- inspectable status (via API or command)

---

## Resolved decisions

- **Windows startup mechanism:** Startup folder shortcut via `services/windows/install.cmd`
- **Tray framework:** pystray (DEC-005, accepted 2026-04-01)
- **Linux service:** systemd user unit via `services/linux/install.sh`
- **macOS service:** LaunchAgent plist via `services/macos/install.sh`
- **Backend ↔ tray IPC:** HTTP REST API (health endpoint polling)

## Still to be decided

- exact Linux packaging format
- exact macOS packaging format
- exact service supervisor structure (for production deployments)
