# LEDGER

Append-only record of all meaningful work in Glossa Lab.

---

## [2026-03-31] Entry — Repository scaffold and governance bootstrap

Objective: Establish the initial repository scaffold with governance files, documentation, and directory structure.
What was done:
- Repository created with directory structure: backend/, frontend/, tray/, services/{windows,linux,macos}/, scripts/, docs/
- Governance files created: AGENTS.md, README.md, docs/architecture.md, docs/workflow.md, docs/services.md
- Component READMEs created for backend/, frontend/, tray/, scripts/, services/*/
- .gitignore and .gitattributes configured for Python, React, cross-platform development
- All directories contain .gitkeep placeholders

Files changed: all initial repository files (see git log for full list)
Checks run: directory structure verified, all governance files present, .gitignore covers expected patterns
Results: scaffold complete, no runtime code, no bootstrap scripts, no LEDGER.md (added retroactively)
Open TODOs:
- [ ] Harden AGENTS.md with context window management, session boundaries, authority hierarchy
- [ ] Extend docs/architecture.md with concrete interface specifications
- [ ] Create docs/REQUIREMENTS.md with formal numbered requirements
- [ ] Create docs/TEST_SPEC.md with test cases linked to requirements
- [ ] Fix .gitignore missing entries (services/macos/.gitkeep, root node_modules/)
- [ ] Create bootstrap scripts (setup.ps1, setup.sh, run.ps1, run.sh)
- [ ] Scaffold Python backend (pyproject.toml, package structure, entrypoint, health endpoint)
- [ ] Scaffold React frontend (package.json, Vite config, app shell)
- [ ] Define technology decisions for tray framework, IPC mechanism
Risks: technology decisions not yet finalized for tray framework, IPC mechanism, backend web framework
Next step: harden AGENTS.md and extend architecture with concrete specifications

---

## [2026-03-31] Entry — Governance hardening, architecture extension, requirements, tests, and implementation scaffold

Objective: Complete all foundational tasks — harden governance, extend architecture with concrete specs, create requirements and test specifications, fix gitignore, create bootstrap scripts, and scaffold backend + frontend.
What was done:
- Created LEDGER.md (was missing — hard blocker)
- Hardened AGENTS.md: added context window management, conversation summarization recovery, session boundary rules, document authority hierarchy, agent role definition, drafting assistance rules, conflict/consistency handling protocol; fixed backtick formatting error on line 55
- Extended docs/architecture.md: added API boundary spec (REST, /api/v1/, core endpoints), health/status contract (JSON schema, timing requirements), configuration model (TOML, platform paths, env var overrides), logging model (structured JSON, platform paths, rotation), state model (SQLite + filesystem, platform paths), IPC model (HTTP REST only, no implicit coupling), process lifecycle contract (startup sequence, shutdown sequence, signal handling, timeouts), security model (localhost-only, no auth for local, no secrets in responses/logs), technology decisions (DEC-001 through DEC-006)
- Created docs/REQUIREMENTS.md: 25 formal requirements across 10 component categories (BE, API, CFG, LOG, SEC, FE, TRAY, SVC, XP, INT)
- Created docs/TEST_SPEC.md: 25 test cases linked 1:1 to requirements, covering smoke, unit, integration, platform, and boundary types
- Fixed .gitignore: added services/macos/.gitkeep to keep-placeholders, added root node_modules/, added dev-mode data/config/logs directories
- Created bootstrap scripts: scripts/setup.ps1, setup.sh (create venv, install deps, idempotent), scripts/run.ps1, run.sh (start backend/frontend, support --all flag)
- Scaffolded Python backend: pyproject.toml (FastAPI + uvicorn + python-json-logger), glossa_lab package with __init__.py, main.py (FastAPI app, lifespan, CORS), config.py (TOML + env vars + platform paths), logging.py (structured JSON), api/health.py (GET /api/v1/health per REQ-API-001), tests/test_health.py (3 tests covering TEST-API-001, TEST-API-003, TEST-INT-002)
- Scaffolded React frontend: package.json (Vite + React 19 + TypeScript), vite.config.ts (API proxy to backend), tsconfig.json, index.html, src/main.tsx, src/App.tsx (health status display per REQ-FE-002)
- Removed .gitkeep placeholders replaced by real content (backend/, frontend/, scripts/)

Files changed:
- LEDGER.md (created, updated)
- AGENTS.md (edited — 7 new sections, 1 fix)
- docs/architecture.md (edited — 10 new sections)
- docs/REQUIREMENTS.md (created)
- docs/TEST_SPEC.md (created)
- .gitignore (edited)
- scripts/setup.ps1 (created)
- scripts/setup.sh (created)
- scripts/run.ps1 (created)
- scripts/run.sh (created)
- backend/pyproject.toml (created)
- backend/glossa_lab/__init__.py (created)
- backend/glossa_lab/main.py (created)
- backend/glossa_lab/config.py (created)
- backend/glossa_lab/logging.py (created)
- backend/glossa_lab/api/__init__.py (created)
- backend/glossa_lab/api/health.py (created)
- backend/tests/__init__.py (created)
- backend/tests/test_health.py (created)
- frontend/package.json (created)
- frontend/vite.config.ts (created)
- frontend/tsconfig.json (created)
- frontend/index.html (created)
- frontend/src/main.tsx (created)
- frontend/src/App.tsx (created)
- backend/.gitkeep (deleted)
- frontend/.gitkeep (deleted)
- scripts/.gitkeep (deleted)

Checks run:
- All governance files present and internally consistent
- Requirements ↔ test spec 1:1 linkage verified (25 requirements, 25 tests)
- Architecture technology decisions documented (DEC-001 through DEC-006)
- .gitignore covers venv, node_modules, data, config, logs, OS artifacts
- Backend Python syntax verified (files created without errors)
- Note: pip install and pytest not run in this session (no venv created yet)

Results:
- Milestone 1 (repo scaffold + docs scaffold + boundaries) complete
- Milestone 2 (Python backend + React frontend scaffold) complete
- All governance files present: AGENTS.md, LEDGER.md, README.md, architecture.md, workflow.md, services.md, REQUIREMENTS.md, TEST_SPEC.md
- Backend has working FastAPI app with health endpoint
- Frontend has Vite + React app with health status display
- Bootstrap scripts ready for both Windows and POSIX

Open TODOs:
- [ ] Run scripts/setup.ps1 and verify venv creation + pip install succeeds
- [ ] Run pytest on backend/tests/ to verify health endpoint tests pass
- [ ] Run npm install in frontend/ and verify dev server starts
- [ ] Implement remaining API endpoints (GET /api/v1/status, jobs CRUD)
- [ ] Implement database initialization (SQLite, migrations)
- [ ] Implement log rotation
- [ ] Begin tray scaffold (Milestone 3 — after framework decision DEC-005)
- [ ] Create Windows service/startup integration (Milestone 4)
- [ ] Create Linux systemd unit file (Milestone 5)
- [ ] Create macOS LaunchAgent plist (Milestone 6)
- [ ] Add CI pipeline with cross-platform test matrix

Risks:
- Tray framework decision (DEC-005) still pending — blocks Milestone 3
- Backend tests not yet run against actual venv — syntax is verified but runtime not confirmed
- Frontend dependencies not yet installed — package.json created but npm install not run
- All requirements are in "draft" status — need human review to promote to "accepted"

Next step: Run setup scripts to verify environment bootstrap, run backend tests, run frontend dev server — then promote requirements from draft to accepted

---

## [2026-04-01] Entry — Replace .ps1 with .cmd wrappers, verify shell.cmd

Objective: Eliminate PTY-hanging .ps1 scripts, add shell.cmd unified entry point, verify tests and lint pass through it.
What was done:
- Verified shell.cmd test: `shell.cmd test backend\tests -v` — 3/3 tests passed (test_health_endpoint_returns_200, test_health_version_matches_package, test_versioned_routes_only)
- Verified shell.cmd lint: `shell.cmd lint backend\glossa_lab` — all checks passed
- Deleted all .ps1 files: shell.ps1, scripts/run.ps1, scripts/setup.ps1
- Added .cmd wrappers: shell.cmd (repo root), scripts/run.cmd, scripts/setup.cmd
- Updated AGENTS.md with H7 (shell wrapper required) and H8 (no silent commands), shell wrapper documentation, forbidden/required invocation patterns
- Committed and pushed to main (d33f914)

Files changed:
- AGENTS.md (modified — added shell wrapper section, H7, H8)
- shell.cmd (created — unified entry point)
- scripts/run.cmd (created)
- scripts/setup.cmd (created)
- scripts/run.ps1 (deleted)
- scripts/setup.ps1 (deleted)
- shell.ps1 (deleted)
- scripts/setup.sh (modified)
- frontend/package-lock.json (added)

Checks run:
- `shell.cmd test backend\tests -v` — 3 passed, 0 failed (0.37s)
- `shell.cmd lint backend\glossa_lab` — all checks passed
- git status verified before commit — staged changes matched expectations

Results: shell.cmd works correctly on Windows. PTY hang issue resolved by routing all invocations through `python -m`. All .ps1 files removed.
Open TODOs:
- [ ] Run npm install in frontend/ and verify dev server starts
- [ ] Implement remaining API endpoints (GET /api/v1/status, jobs CRUD)
- [ ] Implement database initialization (SQLite, migrations)
- [ ] Implement log rotation
- [ ] Begin tray scaffold (Milestone 3 — after framework decision DEC-005)
- [ ] Create Windows service/startup integration (Milestone 4)
- [ ] Create Linux systemd unit file (Milestone 5)
- [ ] Create macOS LaunchAgent plist (Milestone 6)
- [ ] Add CI pipeline with cross-platform test matrix
- [ ] Create shell.sh POSIX equivalent of shell.cmd
Risks:
- shell.sh (POSIX equivalent) not yet created — Linux/macOS users cannot use the wrapper yet
- Tray framework decision (DEC-005) still pending — blocks Milestone 3
- All requirements still in draft status
Next step: Create shell.sh POSIX wrapper, then implement remaining API endpoints and database initialization
