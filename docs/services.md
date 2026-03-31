# Services and Startup

## Purpose

This document defines startup and background-service expectations for Glossa Lab.

## Core requirement

The application must support:

- foreground development mode
- background service mode
- cross-platform startup flows
- tray-aware local control

## Windows expectations

### Required behavior
- the tray starts automatically on Windows startup / user login
- the tray can open the application UI
- the tray can open, control, or ensure the background services are running
- service status should be visible from the tray

### Notes
Exact implementation may use:
- Startup folder entry
- Run registry entry
- scheduled task
- Windows service model
- another documented approach

The implementation choice must be explicit and documented.

## Linux expectations

### Required behavior
- background services can be started via systemd
- service units are documented under `services/linux/`
- user-service and/or system-service behavior is documented clearly

### Notes
Tray behavior on Linux depends on desktop environment and packaging choices. Linux tray support should be documented carefully and not assumed to behave identically to Windows.

## Service separation

The backend service should be treated as the primary background runtime.

The tray is not the backend.
The frontend is not the backend.
The service layer should remain explicit and inspectable.

## Development mode vs installed mode

### Development mode
- backend runs in foreground or dev-managed process
- frontend runs from dev server or local build
- tray may be optional during early development

### Installed mode
- backend runs in background service mode
- tray starts at login where supported
- frontend is reachable in a stable local form
- logs and configuration locations are documented

## To be decided later

- exact Windows startup mechanism
- exact tray framework
- exact Linux packaging format
- exact service supervisor structure
- exact backend/tray IPC mechanism
