# Implementation Plan: Desktop Host Migration

**Spec**: [spec.md](./spec.md) · **Branch**: `spec/080-desktop-host-migration`

## Approach

Fix the Windows paths in place; do not add a parallel stack.

- **Launch semantics**: point `shell.cmd run`, the tray's Windows
  `_start_backend`, and `scripts/run-backend-svc.cmd` at the
  production entry (`create_app --factory`, `127.0.0.1:8001`).
- **Installed mode**: set `GLOSSA_MODE=installed` in
  `scripts/launch-tray.vbs` (PROCESS environment, inherited by the
  tray and the backend it spawns), in `scripts/run-backend-svc.cmd`,
  and explicitly in the tray's backend child environment, so the
  data path is `%LOCALAPPDATA%\GlossaLab\data` no matter who calls.
- **Targeted stop**: rewrite `setup-os.cmd`'s stop path — shutdown
  endpoint, bounded wait, tray via `scripts\stop-tray.vbs`, then
  port-8001 PIDs filtered by uvicorn/glossa command line. The
  machine-wide `taskkill /IM pythonw.exe` goes away.
- **One installer**: `setup-os.cmd install` stays canonical and
  gains icon SHA-256 verification (ICO + PNG pins from Spec 079).
  `services/windows/install.cmd` becomes a delegating shim;
  `uninstall.cmd` delegates and also removes any legacy shortcut.
- **Tray supervision (Windows)**: the existing 3-second health
  poller gains a bounded auto-restart: on a down reading, if the
  owner did not deliberately stop the backend and fewer than 3
  restarts happened in the trailing hour, start it; otherwise
  leave it down and say so in the status line. A user stop sets a
  flag that only an explicit start clears.
- **Install/verify pair**: `scripts/install-desktop-host.cmd`
  (deps if needed → `setup-os.cmd install` → `setup-os.cmd start`
  → verify) and `scripts/verify-desktop-host.cmd` wrapping
  `scripts/verify_desktop_host.py`, which reuses the Spec 079
  identity check (`services/linux/healthcheck.py` — pure stdlib,
  platform-neutral) and emits the FR-007 markers, including a
  kill-and-watch restart test with a bounded deadline.
- **Migration run** (outside the PR, recorded in the goal record):
  inventory → deploy merged main to the desktop install path →
  install in the owner's user context → quiesce VM backend →
  SQLite backup snapshot → transfer via runner `grab`/job
  mechanisms only → hash + integrity verify on the desktop →
  Tailscale Serve route proof (health + MCP `get_status` from the
  VM) → cutover (VM unit stop+disable) → VM cleanup per the safe
  cleanup skill.

## Verification

- `backend/tests/test_desktop_host_migration.py`: static contract
  tests over the Windows launch/install files (banned tokens
  absent, required tokens present, hash pins present, no global
  pythonw kill, delegator shape) + unit tests for the verify
  script's pure helpers (icon hash comparison, marker emission).
- Existing suites stay green: backend tests, shell-scripts CI job
  (windows-latest), freeze gate — 8/8 incl. C4 before merge.
- Live: the FR-007 markers from the desktop install, the restart
  test's old→new PID pair, the access-route proof, and the
  before/after VM resource numbers, all in the migration record.
