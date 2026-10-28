# Tasks: Supervised Backend + Tray Installation

- [x] T001 Audit Syncyard spec 007 + tray supervisor; extract the pattern
- [x] T002 Audit glossa-lab startup end to end (tray, backend, installers, VM recipe)
- [x] T003 Identify the correct icon (frontend brand tile; encode as SVG/PNG/ICO assets)
- [x] T004 Rewrite Linux backend unit (production entry point, restart cap, OnFailure alert)
- [x] T005 Rewrite Linux installer: backend + tray + icon, idempotent, user/system modes, legacy-unit retirement
- [x] T006 Identity healthcheck (bounded) + OWNER_NEEDED alert script
- [x] T007 Tray: brand icon + status badge; Linux autostart via the installer; unit-name alignment
- [x] T008 Fix `shell.sh run` (production entry point, port 8001) and `shell.sh tray` (PYTHONPATH)
- [x] T009 Windows: icon location in the Startup shortcut installer; install fails loudly if the icon/venv is missing
- [x] T010 Tests: icon assets, healthcheck identity, installer render, tray icon pixels
- [x] T011 Docs: services/linux README, tray README, CHANGELOG, this spec
- [x] T012 Scratch end-to-end verification (install → start → health → restart-on-kill → tray icon)
- [ ] T013 PR + CI green (8/8 incl. C4) + merge
- [ ] T014 Live VM cutover to the system unit; verify; stand the cron watchdog's restart duty down
