# Feature Specification: Supervised Backend + Tray Installation

**Feature Branch**: `fix/backend-tray-supervision`
**Created**: 2026-10-27
**Status**: Implemented (pending CI + live cutover record)
**Input**: Owner directive 2026-10-27: "fix glossa-lab to use similar
backend [supervision] as Syncyard for how it starts. and make sure we
have installer and that it installs the tray as well. and make sure we
have icon for it, the correct one for glossa-labs."
**Reference pattern**: AXIOVEX/syncyard spec 007 "windowless
supervision" — tray/service supervisor starts components hidden,
restarts with a cap (3 per hour), then alerts the owner; Linux
components run under systemd units (its FR-005).

## Audit findings (before the build)

1. **Three disagreeing startup paths.** The systemd unit
   (`glossa-lab.service`) ran `shell.sh run`, which started
   `glossa_lab.main:app` on port **8000 with auto-reload**; the tray
   expected a unit named `glossa-lab-backend`; the live Muse VM
   backend actually runs on port **8001** via
   `glossa_lab.main:create_app --factory` under a nohup recipe kept
   alive by a 20-minute cron watchdog. The unit the installer
   installed could never have supervised the real backend.
2. **Tray icon was not the project's mark.** The tray generated a
   plain coloured circle at runtime. No Glossa Lab logo asset existed
   anywhere in the repository; the project's own application mark is
   the blue gradient tile (`#2563eb` → `#60a5fa`) with a white "G"
   rendered in `frontend/src/App.tsx`. (The BitConcepts company mark
   and the Syncyard logo are different projects' marks.)
3. **Installers were split and partial.** The Linux installer
   installed only the (misnamed, wrong-command) backend unit; the
   tray had no Linux install path at all; `shell.sh tray` omitted
   `PYTHONPATH` so the Linux tray launch failed; the Windows Startup
   shortcut installer never set an icon.
4. **The tray had never run on Linux.** Its window title contained
   an em dash ("Glossa Lab — …"), which pystray's Xorg backend
   encodes as latin-1 — the tray crashed at startup on Linux
   (found by running it under Xvfb during this change; titles are
   now plain ASCII). The health check written for this change had
   the mirror-image bug — it crashed on connection-refused instead
   of retrying — caught by the scratch end-to-end run and fixed.
5. **This VM has no user manager.** As root there is no
   `/run/user/0` and `user@0.service` fails to start, so
   `systemctl --user` supervision is impossible here; the system
   manager is healthy. The repo pattern therefore needs a system
   mode (Syncyard's FR-005 puts Linux agents under systemd units;
   the unit manager choice follows where the component lives).

## User Scenarios & Testing

### User Story 1 — Backend stays up under supervision (Priority: P1)

The backend is started by systemd, restarts automatically when it
crashes, and stops crash-looping after a bounded number of attempts,
at which point the owner is told instead of the failure repeating
silently.

**Acceptance Scenarios**:

1. **Given** an installed unit, **When** the backend process is
   killed, **Then** systemd restarts it and the identity health
   check passes again.
2. **Given** a backend that fails on every start, **When** it has
   started 3 times within an hour, **Then** systemd stops restarting
   it and the alert unit records `OWNER_NEEDED` in the state
   directory.

### User Story 2 — One installer installs backend and tray (Priority: P1)

Running the documented install path once installs the supervised
backend unit AND the tray (autostart entry + icon), and re-running
it changes nothing (idempotent).

### User Story 3 — The tray shows the Glossa Lab icon (Priority: P2)

The tray icon is the project's own mark with a small status badge;
the Windows shortcut and the Linux icon theme both use the same
packaged asset.

## Requirements

- **FR-001**: The backend MUST run under a systemd unit named
  `glossa-lab-backend` executing the production entry point
  (`create_app --factory`, port 8001, no reload, no shell wrapper).
- **FR-002**: The unit MUST restart on failure with a cap of 3
  starts per hour; on cap/failure an alert unit MUST record an
  `OWNER_NEEDED` marker and a supervisor log line.
- **FR-003**: A single Linux installer MUST install the backend
  unit and the tray (autostart + icon) in one run, be idempotent,
  retire the legacy `glossa-lab.service` unit so no two supervisors
  race, and support user and system manager modes.
- **FR-004**: Install verification MUST check backend identity
  (HTTP 200 on `/docs`, healthy `/api/v1/health`, `/openapi.json`
  title and version match) with bounded waits — never liveness only.
- **FR-005**: The tray icon MUST be the packaged Glossa Lab brand
  asset (PNG/ICO/SVG) with a status badge; the Windows shortcut
  installer MUST set the icon location, and the Windows install path
   MUST fail loudly if the icon asset is missing.
- **FR-006**: The tray's Linux start/stop MUST target the same unit
  name the installer installs, and the tray launcher MUST set
  `PYTHONPATH` on Linux as it already does on Windows.
- **FR-007**: After the supervised start is verified live, the
  20-minute cron watchdog's restart duty MUST be stood down in the
  same change so the watchdog and systemd never race.

## Assumptions

- The VM cutover uses system mode (no user manager exists for root
  on this VM); desktop Linux installs default to user mode.
- macOS LaunchAgent supervision is unchanged by this spec.
- The status colours and health-endpoint contract are unchanged.
