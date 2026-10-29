# Tasks: Desktop Host Migration

- [x] T001 Audit Windows launch/install/stop paths + Spec 079 record (done pre-spec; findings in spec.md)
- [x] T002 Spec 080: spec.md / plan.md / tasks.md / aee-claims.json with falsifiers before code
- [x] T003 `shell.cmd run`: production factory entry, loopback, no reload
- [x] T004 `scripts/run-backend-svc.cmd`: factory entry + `GLOSSA_MODE=installed`
- [x] T005 Tray: factory/loopback backend start, `GLOSSA_MODE=installed` in child env, bounded supervision restart (cap 3/hour, user-stop respected), bounded stop wait
- [x] T006 `scripts/launch-tray.vbs`: set `GLOSSA_MODE=installed` for the tray process tree
- [x] T007 `setup-os.cmd`: icon SHA-256 verification at install (fail loudly); targeted stop (no global pythonw kill)
- [x] T008 `services/windows/install.cmd` delegates to `setup-os.cmd install`; `uninstall.cmd` delegates + removes legacy shortcut; README rewritten to the canonical path
- [x] T009 Install/verify pair: `scripts/install-desktop-host.cmd`, `scripts/verify-desktop-host.cmd`, `scripts/verify_desktop_host.py` (FR-007 markers, bounded)
- [x] T010 Tests: `backend/tests/test_desktop_host_migration.py` (static contracts + verify helpers); full local suite + ruff on changed Python — done. Final evidence: targeted Spec 080 + supervision tests 11 passed / 1 skipped; ruff (repo config) clean on changed files and the whole backend tree; full suite in CI-parity conditions (fresh venv, `pip install -e .[dev]` from PyPI exactly as CI does, aee = applied-epistemic-engineering 1.5.3) = 1951 passed, 14 skipped, 1 failed in 652 s. The one failure is `test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`, which by design SKIPS in CI (its CISI builder inputs are local-only); on this VM the local store exists so it runs and fails inside the builder on local-store state — pre-existing and unrelated to this change (no changed file is involved). Two environment findings from the runs: (1) the worktree initially inherited the supervision clone's sparse-checkout profile, which hid specs/029 fixtures and failed collection; sparse checkout was disabled for this worktree only and the tree materialized in full; (2) the shared VM venv (`~/workspace/venvs/glossa-lab`) carries a stale hand-copied aee 1.0.4 while pyproject requires applied-epistemic-engineering >=1.5.0,<1.6 — with that venv the suite fails 52 aee tests for version reasons alone, so local suite evidence must use a CI-parity venv
- [x] T011 Docs: CHANGELOG, LEDGER entry, services/windows README, tray README (Windows supervision + installed data path)
- [ ] T012 PR + CI green (8/8 incl. C4) + merge
- [ ] T013 Desktop deploy + install + verify markers (migration record)
- [ ] T014 Data snapshot (source stopped, SQLite backup) → fleet-only transfer → desktop hash + integrity verify
- [ ] T015 Access route: Tailscale Serve proof — health + MCP get_status from the VM against the desktop instance
- [ ] T016 Cutover: VM unit stop + disable; MCP repointed; post-cutover smoke test
- [ ] T017 VM cleanup per safe-workspace-cleanup (inventory → prove → salvage → remove), before/after RAM + disk in the migration record
- [ ] T018 Amendment 1 fix: icon verification via .NET SHA-256 helper (case-insensitive, discriminated failures); autostart amended to the HKCU Run value (read-back verified), scheduled-task path + register_task.ps1 removed, tray + verify script read the Run value (marker GLOSSA_AUTOSTART_STATE); PR + CI green (8/8 incl. C4) + merge, then desktop install re-run green
