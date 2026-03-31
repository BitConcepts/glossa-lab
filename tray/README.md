# Tray

This directory contains the tray application for Glossa Lab.

The tray is a **local control and visibility layer**. It provides quick access to application status and common actions, but it does not own core runtime logic. The backend remains the primary runtime authority.

## Responsibilities

The tray may provide:

- quick system status
- open UI action
- open logs or diagnostics
- service controls (start/stop/restart)
- startup/login integration where supported
- fast access to common local actions

## Expected characteristics

- desktop-oriented
- lightweight
- explicit in behavior
- connected to backend or service interfaces through documented boundaries
- replaceable without changing backend behavior

## Design rules

- the tray does **not** contain backend business logic
- the tray does **not** become a hidden runtime
- the tray does **not** own persistent application state
- the tray communicates through explicit interfaces such as:
  - local HTTP API
  - IPC
  - CLI/service wrapper commands

## Platform expectations

### Windows
Windows is the first-class tray target.

Expected behavior:
- tray starts automatically at user login/startup
- tray can open the local UI
- tray can check service status
- tray can start, stop, or restart background services
- tray behavior is tightly integrated with Windows startup/service expectations

### Linux
Linux tray support must be documented explicitly per desktop/runtime constraints.

Expected behavior:
- tray support may vary by desktop environment
- any limitations must be documented clearly
- tray behavior must not assume parity with Windows

### macOS
macOS tray support is expected as a first-class desktop experience.

Expected behavior:
- tray/login behavior is documented explicitly
- tray integrates cleanly with macOS-native startup expectations
- tray controls backend/service behavior only through documented interfaces

## Development expectations

The tray should support at least two modes:

### Development mode
- may run independently during development
- may connect to a locally running backend
- should be optional during early backend/frontend work

### Installed mode
- starts automatically where supported
- reflects backend/service status
- provides stable quick-access control surface for local users

## Planned future additions

Expected future additions include:

- tray application scaffold
- backend status integration
- service control integration
- startup/login integration
- platform-specific packaging notes
- diagnostics/log access actions
- tests or smoke checks where practical

## Boundary reminder

The tray is a controller and observer.

It is not:
- the backend
- the frontend
- the service manager of record
- the source of application truth
