# Feature Specification: Desktop Host Migration — Glossa Lab on TRISTEN-DESKTOP

**Feature Branch**: `spec/080-desktop-host-migration`
**Created**: 2026-10-28
**Status**: Draft — claims frozen before code (spec-kit + AEE flow)
**Input**: Owner directive 2026-10-28 00:15 EDT: "we need to run
glossa-lab on the tristen-desktop host. especially since this keeps
causing issues. … make sure we have installer and tray icon and that
it works correctly from the host. and then clean up what is not
needed in muse."
**Predecessor**: Spec 079 (supervised backend + tray on the Muse VM).
The VM backend's deaths were kernel OOM kills driven by the host
runtime daemon's memory growth — a platform property of the VM, not
of the application. The application therefore moves to the owner's
desktop, which is its natural host (tray-first design, H25 wrappers,
owner's interactive session).

## Audit findings (before the build)

1. **Three Windows launch paths still use development semantics.**
   `shell.cmd run` starts `glossa_lab.main:app` with `--reload` on
   `0.0.0.0`; the tray's `_start_backend` starts `main:app` on
   `0.0.0.0`; `scripts/run-backend-svc.cmd` starts `main:app`
   (loopback, but no factory). Production is
   `glossa_lab.main:create_app --factory` on `127.0.0.1:8001`
   (the Spec 079 Linux unit semantics).
2. **`setup-os.cmd stop` kills every `pythonw.exe` on the machine**
   (`taskkill /F /IM pythonw.exe`) — it would terminate unrelated
   GUI Python processes belonging to other programs.
3. **Two competing autostart mechanisms.** `setup-os.cmd install`
   registers the `GlossaLab` scheduled task (wscript + VBS, H25);
   `services/windows/install.cmd` independently creates a Startup
   shortcut pointing at `shell.cmd tray`, which violates H25 and
   can double-launch the tray.
4. **No deterministic data path on Windows.** Nothing in the
   installed launch chain sets `GLOSSA_MODE`, so `Settings.data_dir`
   resolves to `./data` relative to whatever cwd the launcher
   happens to have. Installed mode exists (`config.py`:
   `%LOCALAPPDATA%\GlossaLab\data` on win32) but is never selected.
5. **The tray does not supervise on Windows.** It starts the backend
   once at tray launch (`_ensure_backend_running`) and never again;
   a backend that dies while the tray lives stays dead until a human
   uses the menu. (On Linux, systemd supervises; on Windows the tray
   is the supervisor of record and must do this job.)
6. **Icon presence is checked, icon identity is not.**
   `setup-os.cmd install` checks the ICO exists but never verifies
   it is the packaged Glossa Lab asset (Spec 079 recorded SHA-256
   pins for ICO/PNG).

## User Scenarios & Testing

### User Story 1 — Glossa Lab runs on the desktop (Priority: P1)

The owner logs on to TRISTEN-DESKTOP; the tray appears with the
Glossa Lab icon; the backend is running on 127.0.0.1:8001 with the
migrated production data; if the backend process dies, the tray
restarts it (bounded), with no visible console window at any point.

**Acceptance Scenarios**:

1. **Given** a completed install, **When** the backend process is
   killed, **Then** the tray restarts it within the poll cycle
   budget and the identity check passes against the new PID.
2. **Given** the tray is running, **When** the owner chooses
   "Stop Service", **Then** the backend stops and stays stopped
   (supervision never overrides a deliberate stop).
3. **Given** a corrupted or missing tray icon asset, **When** the
   installer runs, **Then** it fails loudly and registers nothing.

### User Story 2 — One installer, one autostart (Priority: P1)

`setup-os.cmd install` is the only registration path; the legacy
Startup-shortcut installer delegates to it; re-running install
changes nothing (idempotent).

### User Story 3 — The data survived the move (Priority: P1)

The desktop backend serves the migrated production database:
SHA-256 of the snapshot matches on both machines and
`PRAGMA integrity_check` passes before first start.

### User Story 4 — Muse can still reach it (Priority: P2)

The VM-side MCP client reaches the desktop backend over the
tailnet (Tailscale Serve, loopback bind on the desktop) and
`get_status` answers from the desktop instance. The backend is
never bound to a public interface.

## Requirements

- **FR-001**: Every Windows backend launch path (`shell.cmd run`,
  tray `_start_backend`, `scripts/run-backend-svc.cmd`) MUST use
  `glossa_lab.main:create_app --factory`, host `127.0.0.1`, port
  8001 — no `--reload`, no `0.0.0.0`, no `main:app`.
- **FR-002**: The installed launch chain (tray VBS launcher,
  backend service wrapper, tray-spawned backend environment) MUST
  set `GLOSSA_MODE=installed`, so the data directory is
  `%LOCALAPPDATA%\GlossaLab\data` independent of caller cwd.
- **FR-003**: `setup-os.cmd stop` MUST terminate only Glossa Lab
  processes: graceful shutdown endpoint first, tray via
  `scripts\stop-tray.vbs`, backend only via PIDs on port 8001 whose
  command line matches this repo's uvicorn invocation. A
  machine-wide `taskkill /IM pythonw.exe` (or `python.exe`) MUST
  NOT appear in the stop path.
- **FR-004**: There MUST be exactly one Windows autostart
  mechanism: the `GlossaLab` scheduled task registered by
  `setup-os.cmd install` (action `wscript.exe` + `launch-tray.vbs`,
  per H25). `services/windows/install.cmd` MUST delegate to it and
  MUST NOT create a Startup shortcut; uninstall MUST remove the
  task and any legacy shortcut.
- **FR-005**: `setup-os.cmd install` MUST verify the SHA-256 of
  `tray\glossa_tray\assets\glossa-lab.ico`
  (`315940742d75720388264dcdf03178c58f878ea0701d03eeba95688d935ff520`)
  and `glossa-lab.png`
  (`bb41bf09d4177cee0c96b29ebe480f86a9e7115946f9e4ad132d2367a7adb077`)
  and fail loudly on missing or mismatched assets.
- **FR-006**: The tray MUST supervise the backend on Windows:
  when the health poll finds the backend down and the owner has
  not deliberately stopped it, the tray restarts it, capped at
  3 restarts per rolling hour; past the cap it reports the stopped
  state instead of looping (H11: every wait bounded).
- **FR-007**: A desktop verify script MUST emit the markers
  `GLOSSA_HOST_HEALTH`, `GLOSSA_HOST_IDENTITY`,
  `GLOSSA_TRAY_PROCESS`, `GLOSSA_ICON_HASH`, `GLOSSA_TASK_STATE`,
  `GLOSSA_RESTART_TEST`, where identity means the bounded Spec 079
  check (`/docs` 200 + health status/version + OpenAPI title
  "Glossa Lab" with matching version) — never liveness alone.
- **FR-008**: The desktop backend MUST bind loopback only. Remote
  access MUST be exclusively via Tailscale Serve on the owner's
  tailnet; no public bind, funnel, or third-party tunnel.
- **FR-009**: The production database MUST move as a
  SQLite-consistent snapshot (source backend stopped; SQLite
  backup API), SHA-256 recorded at the source, transferred only
  through the desktop-runner fleet mechanism, and re-verified
  (SHA-256 + `PRAGMA integrity_check`) on the desktop before the
  backend first starts against it.
- **FR-010**: All loops and waits added or touched by this change
  MUST be bounded with an explicit deadline or attempt cap and a
  diagnostic on timeout (H11). Windows multi-step automation MUST
  live in `.cmd` files (H12); tray start/stop MUST use the VBS
  wrappers (H25).

## Assumptions / epistemic boundaries (H13)

- The Actions runner's Windows session may not be the owner's
  interactive session; anything that must live in the owner's
  session (tray icon, logon task) is verified from the task/process
  state the runner can see, and any owner-session-only remainder is
  reported as such, never faked.
- The snapshot source of record is the production data directory
  identified by the migration inventory (Phase C of the migration
  record), named there with hashes; this spec governs how it
  moves, not which directory that is.
- macOS behaviour is unchanged. Linux supervision stays with
  systemd (Spec 079); this spec changes the Windows paths and the
  tray's Windows backend start/supervision only.
- The restart cap mirrors the fleet pattern (3 per hour, then
  owner attention) used by Spec 079 and Syncyard spec 007.
