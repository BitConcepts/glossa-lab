# Implementation Plan: Supervised Backend + Tray Installation

**Spec**: [spec.md](./spec.md) · **Branch**: `fix/backend-tray-supervision`

## Approach

Follow the Syncyard spec 007 supervision shape, adapted to where
each Glossa component actually lives:

- **Backend (VM + Linux installs)** → systemd unit
  `glossa-lab-backend`: hidden by construction (a service has no
  console), `Restart=on-failure`, start limit 3/hour, `OnFailure`
  alert unit records `OWNER_NEEDED`; user manager by default,
  system manager where no user manager exists (the Muse VM runs
  as root with no user runtime directory).
- **Tray (desktop sessions)** → per-user autostart (Linux
  `.desktop`, Windows scheduled task via VBS wrappers as today),
  icon = packaged brand asset with a status badge (Syncyard tray
  treatment).
- **One installer** (`services/linux/install.sh`, driven by
  `setup-os.sh install`) renders units/support files, installs tray
  + icon, retires the legacy unit, enables/starts, then verifies
  identity with `healthcheck.py` (bounded).
- **Cutover**: PR lands first; then the VM backend is switched from
  the nohup + cron-watchdog recipe to the system unit, verified
  (HTTP 200 + identity + kill/restart), and only then is the
  watchdog's restart duty stood down in its cron file.

## Verification

- `backend/tests/test_supervision_installer.py`: icon asset
  format/content, healthcheck accept/reject, installer render-only
  output, tray icon pixels.
- Scratch end-to-end: render-only install into a scratch HOME;
  tray under Xvfb with the packaged icon; backend under the
  unit file in the scratch tree via a user-mode systemd where
  available, otherwise uvicorn run of the exact ExecStart line.
- CI: full repo suite (incl. C4 governance) green before merge.
- Live: post-cutover `systemctl status`, healthcheck output, and a
  kill → supervised-restart check recorded in the goal record.
