# Test Specification

Test cases for Glossa Lab, linked to requirements in `docs/REQUIREMENTS.md`.

**Naming convention:** `TEST-<COMPONENT>-<NUMBER>`

**Test types:**
- `smoke` — basic functionality, run on every change
- `unit` — isolated component behavior
- `integration` — cross-component behavior
- `platform` — OS-specific behavior
- `boundary` — verifies component boundaries are respected

---

## Backend

### TEST-BE-001 — Backend starts in foreground mode

**Requirement:** REQ-BE-001
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- Python virtual environment exists with dependencies installed
- No other instance running on port 8000

**Steps:**
1. Run backend entrypoint in foreground mode
2. Wait up to 10 seconds for startup
3. Send GET to `http://localhost:8000/api/v1/health`
4. Verify HTTP 200 response with valid JSON

**Expected result:** Backend starts, health endpoint responds within 10 seconds
**Pass criteria:** Health endpoint returns HTTP 200 with `status: "healthy"`
**Fail criteria:** Startup exceeds 10 seconds, health endpoint unreachable, or invalid response

### TEST-BE-002 — Backend starts in background/service mode

**Requirement:** REQ-BE-002
**Type:** integration
**Platform:** all
**Automated:** planned

**Preconditions:**
- Python virtual environment exists with dependencies installed

**Steps:**
1. Start backend in background mode
2. Verify process is running and detached from terminal
3. Send GET to health endpoint
4. Verify response matches foreground mode behavior

**Expected result:** Backend runs in background, health endpoint responds identically
**Pass criteria:** Process running, health response valid
**Fail criteria:** Process not detached, health endpoint differs from foreground

### TEST-BE-003 — Backend clean shutdown

**Requirement:** REQ-BE-003
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend is running

**Steps:**
1. Send SIGTERM (POSIX) or CTRL_C_EVENT (Windows) to backend process
2. Wait up to 60 seconds for process to exit
3. Verify exit code is 0
4. Verify log file contains shutdown messages
5. Verify no orphaned database locks

**Expected result:** Backend shuts down cleanly within timeout
**Pass criteria:** Exit code 0, shutdown logged, no locks
**Fail criteria:** Timeout exceeded, non-zero exit, orphaned resources

### TEST-BE-004 — Backend database initialization

**Requirement:** REQ-BE-004
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- No existing database file at the configured path

**Steps:**
1. Delete database file if it exists
2. Start backend
3. Verify database file was created
4. Verify schema tables exist
5. Stop backend

**Expected result:** Database created automatically on first start
**Pass criteria:** Database file exists with expected schema
**Fail criteria:** Database not created, or backend crashes on missing database

---

## API

### TEST-API-001 — Health endpoint returns valid status

**Requirement:** REQ-API-001
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend is running

**Steps:**
1. Send GET to `/api/v1/health`
2. Verify HTTP 200 status code
3. Verify response is valid JSON
4. Verify response contains `status`, `version`, `uptime_seconds`
5. Verify `status` is one of: `healthy`, `degraded`, `down`
6. Verify `uptime_seconds` is a non-negative number
7. Verify response arrives within 1 second

**Expected result:** Valid health JSON within 1 second
**Pass criteria:** All fields present, valid values, response time < 1s
**Fail criteria:** Missing fields, invalid values, or timeout

### TEST-API-002 — Status endpoint returns system status

**Requirement:** REQ-API-002
**Type:** unit
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend is running

**Steps:**
1. Send GET to `/api/v1/status`
2. Verify HTTP 200 status code
3. Verify response contains job count and pipeline state information

**Expected result:** Detailed status JSON
**Pass criteria:** Response contains expected status fields
**Fail criteria:** Missing fields or HTTP error

### TEST-API-003 — API versioning prefix

**Requirement:** REQ-API-003
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend is running

**Steps:**
1. Send GET to `/api/v1/health` — verify 200
2. Send GET to `/health` (no version prefix) — verify 404
3. Send GET to `/api/health` (no version number) — verify 404

**Expected result:** Only versioned routes are accessible
**Pass criteria:** Prefixed route returns 200, non-prefixed return 404
**Fail criteria:** Non-prefixed routes return non-404

### TEST-API-004 — CORS headers in development mode

**Requirement:** REQ-API-004
**Type:** unit
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend is running in development mode

**Steps:**
1. Send OPTIONS preflight request to `/api/v1/health` with Origin: `http://localhost:5173`
2. Verify `Access-Control-Allow-Origin` header is present
3. Verify the origin is allowed

**Expected result:** CORS headers present for localhost origins
**Pass criteria:** CORS headers allow localhost
**Fail criteria:** Missing or restrictive CORS headers

---

## Configuration

### TEST-CFG-001 — Backend starts with missing config file

**Requirement:** REQ-CFG-001
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- No config file exists at the expected path

**Steps:**
1. Ensure no config file at `./config/glossa.toml`
2. Start backend
3. Verify backend starts successfully with defaults
4. Verify health endpoint responds

**Expected result:** Backend starts with safe defaults, no crash
**Pass criteria:** Backend healthy without config file
**Fail criteria:** Crash or error on missing config

### TEST-CFG-002 — Environment variable overrides

**Requirement:** REQ-CFG-002
**Type:** unit
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend is not running

**Steps:**
1. Set `GLOSSA_LOG_LEVEL=WARNING`
2. Start backend
3. Verify log level is WARNING (not default INFO/DEBUG)
4. Stop backend

**Expected result:** Environment variable overrides config
**Pass criteria:** Config reflects environment variable value
**Fail criteria:** Config ignores environment variable

### TEST-CFG-003 — Platform-specific config paths

**Requirement:** REQ-CFG-003
**Type:** platform
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend in installed mode (not dev mode)

**Steps:**
1. On Windows: verify config loaded from `%APPDATA%\GlossaLab\config.toml`
2. On Linux: verify config loaded from `$XDG_CONFIG_HOME/glossa-lab/config.toml`
3. On macOS: verify config loaded from `~/Library/Application Support/GlossaLab/config.toml`
4. In dev mode: verify config loaded from `./config/glossa.toml`

**Expected result:** Correct path used per platform and mode
**Pass criteria:** Config loaded from documented path
**Fail criteria:** Wrong path or fallback without documentation

---

## Logging

### TEST-LOG-001 — Structured JSON log output

**Requirement:** REQ-LOG-001
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend is running

**Steps:**
1. Trigger a request to generate a log entry
2. Read log file
3. Verify each line is valid JSON
4. Verify each entry contains: timestamp, level, module, message

**Expected result:** Structured JSON logs with all required fields
**Pass criteria:** All log lines are valid JSON with required fields
**Fail criteria:** Non-JSON output or missing fields

### TEST-LOG-002 — Platform-specific log paths

**Requirement:** REQ-LOG-002
**Type:** platform
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend in installed mode

**Steps:**
1. Start backend in installed mode
2. Verify log file created at platform-appropriate path
3. In dev mode: verify log at `./logs/glossa.log`

**Expected result:** Logs written to correct platform path
**Pass criteria:** Log file exists at documented path
**Fail criteria:** Log file at wrong path or missing

### TEST-LOG-003 — No secrets in logs

**Requirement:** REQ-LOG-003
**Type:** unit
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend configured with a test secret via environment variable

**Steps:**
1. Set a test secret environment variable
2. Start backend
3. Trigger operations that use the secret
4. Search all log output for the secret value
5. Verify the secret does not appear

**Expected result:** Secret value absent from all log output
**Pass criteria:** grep for secret value returns zero matches
**Fail criteria:** Secret value found anywhere in logs

---

## Security

### TEST-SEC-001 — Localhost binding

**Requirement:** REQ-SEC-001
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend is running with default config

**Steps:**
1. Verify backend is listening on 127.0.0.1:8000
2. Verify backend is NOT listening on 0.0.0.0:8000
3. From a different machine on the same network, verify connection refused

**Expected result:** Backend only accessible from localhost
**Pass criteria:** 127.0.0.1 responds, external connections refused
**Fail criteria:** Backend accessible from external addresses

### TEST-SEC-002 — No secrets in API responses

**Requirement:** REQ-SEC-002
**Type:** unit
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend running with configured secrets

**Steps:**
1. GET `/api/v1/config`
2. Verify response does not contain any secret values
3. GET `/api/v1/health`
4. Verify response does not contain any secret values

**Expected result:** No secrets in any API response
**Pass criteria:** No secret values in response bodies
**Fail criteria:** Any secret value present in response

---

## Frontend

### TEST-FE-001 — Frontend connects to backend API

**Requirement:** REQ-FE-001
**Type:** integration
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend running, frontend dev server running

**Steps:**
1. Load frontend in browser
2. Verify frontend fetches from `/api/v1/health`
3. Verify no application logic executes outside API calls

**Expected result:** Frontend communicates exclusively via API
**Pass criteria:** API calls observed, no local computation of backend logic
**Fail criteria:** Frontend contains business logic or bypasses API

### TEST-FE-002 — Frontend displays health status

**Requirement:** REQ-FE-002
**Type:** integration
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend running, frontend loaded

**Steps:**
1. Verify frontend displays "healthy" when backend is up
2. Stop backend
3. Verify frontend displays "down" or connection error state

**Expected result:** Health status reflected in UI
**Pass criteria:** UI shows correct status for both states
**Fail criteria:** UI does not reflect backend state

### TEST-FE-003 — Frontend dev server starts

**Requirement:** REQ-FE-003
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- npm dependencies installed

**Steps:**
1. Run `npm run dev` in frontend directory
2. Verify dev server starts on expected port (5173)
3. Load page in browser
4. Verify page renders

**Expected result:** Dev server starts and serves the application
**Pass criteria:** Page loads successfully
**Fail criteria:** Dev server fails to start or page does not render

---

## Tray

### TEST-TRAY-001 — Tray displays backend status

**Requirement:** REQ-TRAY-001
**Type:** integration
**Platform:** windows, macos
**Automated:** no (manual, requires desktop environment)

**Preconditions:**
- Tray application running, backend running

**Steps:**
1. Verify tray shows "running" or healthy icon
2. Stop backend
3. Verify tray shows "stopped" or error icon

**Expected result:** Tray reflects backend status
**Pass criteria:** Status matches backend state
**Fail criteria:** Status does not update or is incorrect

### TEST-TRAY-002 — Tray does not contain backend logic

**Requirement:** REQ-TRAY-002
**Type:** boundary
**Platform:** all
**Automated:** planned

**Preconditions:**
- Tray codebase available for inspection

**Steps:**
1. Static analysis: verify no imports from backend package
2. Verify all backend interaction goes through HTTP or CLI
3. Verify no database access, no pipeline logic, no job execution

**Expected result:** Tray is a pure control surface
**Pass criteria:** No backend logic in tray code
**Fail criteria:** Any backend logic found in tray

---

## Service/Startup

### TEST-SVC-001 — Windows startup registration

**Requirement:** REQ-SVC-001
**Type:** platform
**Platform:** windows
**Automated:** no (requires Windows desktop)

**Preconditions:**
- Tray installed on Windows

**Steps:**
1. Register tray for startup
2. Log out and log in
3. Verify tray is running after login

**Expected result:** Tray starts automatically on login
**Pass criteria:** Tray process present after login
**Fail criteria:** Tray not started

### TEST-SVC-002 — Linux systemd service

**Requirement:** REQ-SVC-002
**Type:** platform
**Platform:** linux
**Automated:** planned

**Preconditions:**
- systemd user service unit installed

**Steps:**
1. `systemctl --user start glossa-lab`
2. Verify service is active: `systemctl --user is-active glossa-lab`
3. Verify health endpoint responds
4. `systemctl --user stop glossa-lab`
5. Verify service stopped cleanly

**Expected result:** Backend manageable via systemd
**Pass criteria:** Start/stop/status all work correctly
**Fail criteria:** Service fails to start or stop

### TEST-SVC-003 — macOS LaunchAgent

**Requirement:** REQ-SVC-003
**Type:** platform
**Platform:** macos
**Automated:** no (requires macOS)

**Preconditions:**
- LaunchAgent plist installed

**Steps:**
1. `launchctl load ~/Library/LaunchAgents/com.glossalab.backend.plist`
2. Verify backend is running
3. Verify health endpoint responds
4. `launchctl unload ~/Library/LaunchAgents/com.glossalab.backend.plist`
5. Verify backend stopped

**Expected result:** Backend manageable via LaunchAgent
**Pass criteria:** Load/unload/status all work correctly
**Fail criteria:** Agent fails to load or backend doesn't start

---

## Cross-Platform

### TEST-XP-001 — Backend runs on all platforms

**Requirement:** REQ-XP-001
**Type:** platform
**Platform:** all
**Automated:** planned (CI matrix)

**Preconditions:**
- Clean clone on each platform

**Steps:**
1. Run setup script for the platform
2. Run backend
3. Verify health endpoint responds
4. Verify no platform-specific code in backend core

**Expected result:** Backend works identically on Windows, Linux, macOS
**Pass criteria:** Health endpoint responds on all three platforms
**Fail criteria:** Failure on any platform

### TEST-XP-002 — Bootstrap scripts work

**Requirement:** REQ-XP-002
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- Clean clone, no virtual environment

**Steps:**
1. Run `scripts/setup.cmd` (Windows) or `scripts/setup.sh` (POSIX)
2. Verify virtual environment created
3. Verify dependencies installed
4. Run setup script again (idempotency check)
5. Verify no errors on second run

**Expected result:** Environment set up correctly, idempotent
**Pass criteria:** venv exists, deps installed, second run succeeds
**Fail criteria:** Setup fails or second run errors

### TEST-XP-003 — Environment isolation

**Requirement:** REQ-XP-003
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- Clean clone, no global Python packages related to glossa-lab

**Steps:**
1. Run setup script
2. Verify all imports resolve from virtual environment only
3. Verify no global packages are required
4. Delete venv, re-run setup, verify reproducible

**Expected result:** Fully isolated, reproducible environment
**Pass criteria:** All deps in venv, reproducible from scratch
**Fail criteria:** Global dependency required

---

## Integration/Boundary

### TEST-INT-001 — Frontend does not manage services

**Requirement:** REQ-INT-001
**Type:** boundary
**Platform:** all
**Automated:** planned

**Preconditions:**
- Frontend codebase available for inspection

**Steps:**
1. Static analysis: verify no process management code (spawn, exec, kill)
2. Verify no service lifecycle API calls from frontend
3. Verify no direct subprocess invocation

**Expected result:** Frontend is purely a UI layer
**Pass criteria:** No service management code in frontend
**Fail criteria:** Any process management logic found

### TEST-INT-002 — Version consistency

**Requirement:** REQ-INT-002
**Type:** smoke
**Platform:** all
**Automated:** planned

**Preconditions:**
- Backend running

**Steps:**
1. Read version from `backend/pyproject.toml`
2. GET `/api/v1/health`
3. Compare `version` field in response to pyproject.toml version

**Expected result:** Versions match exactly
**Pass criteria:** Versions are identical strings
**Fail criteria:** Version mismatch

---

## Analysis Pipelines

### TEST-PIPE-001 — Block entropy pipeline produces valid output

**Requirement:** REQ-PIPE-001
**Type:** smoke
**Platform:** all
**Automated:** yes (test_study_synthetic.py, test_study_rao2009.py)

**Steps:**
1. Submit a text corpus to the block_entropy pipeline
2. Verify result contains block_entropies array with N=1..6
3. Verify each entry has raw_nats and normalized fields
4. Verify normalized values are in plausible range [0, max_n]

**Expected result:** Valid block entropy results
**Pass criteria:** All fields present, values in range
**Fail criteria:** Missing fields or out-of-range values

### TEST-PIPE-002 — Character frequency pipeline produces valid output

**Requirement:** REQ-PIPE-002
**Type:** smoke
**Platform:** all
**Automated:** planned

**Steps:**
1. Submit a text corpus to the char_freq pipeline
2. Verify result contains total_symbols, unique_symbols, frequencies, zipf_exponent
3. Verify frequencies sum to total_symbols

**Expected result:** Valid frequency results
**Pass criteria:** All fields present, frequencies consistent
**Fail criteria:** Missing fields or inconsistent counts

### TEST-PIPE-003 — Pipeline engine processes jobs

**Requirement:** REQ-PIPE-003
**Type:** smoke
**Platform:** all
**Automated:** yes (test_jobs.py)

**Steps:**
1. Create a job with pipeline="block_entropy" and valid text_id
2. Wait for engine to process
3. Verify job status transitions to completed
4. Verify results are retrievable via GET /api/v1/jobs/{id}/results

**Expected result:** Job processed, results stored
**Pass criteria:** Job completed, results accessible
**Fail criteria:** Job stuck in pending/running, or no results

---

## Kandles Phonetic-Visual Analysis

### TEST-KDL-001 — Kandles phonetic mapping is correct

**Requirement:** REQ-KDL-001
**Type:** unit
**Platform:** all
**Automated:** planned
**Patent:** US 2024/0248922 A1

**Steps:**
1. Map the word "cat" → expect group 1 (K/G/J/Ch), color Yellow
2. Map the word "moon" → expect group 2 (M/N), color Grey
3. Map the word "tree" → expect group 3 (T/D/Th), color Red
4. Map the word "river" → expect group 4 (R/L), color Blue
5. Map the word "water" → expect group 5 (Y/W/H/Kh), color Green
6. Map the word "fire" → expect group 6 (P/B/F/V), color Purple
7. Map the word "sun" → expect group 7 (S/Z/Sh), color Brown
8. Map the word "apple" → expect group 0 (vowel-initial)

**Expected result:** Each word maps to the correct Kandles group
**Pass criteria:** All 8 mappings correct
**Fail criteria:** Any mapping incorrect

### TEST-KDL-002 — Kandles color-coded text output

**Requirement:** REQ-KDL-002
**Type:** unit
**Platform:** all
**Automated:** planned
**Patent:** US 2024/0248922 A1

**Steps:**
1. Input: "The cat sat on the mat"
2. Generate Kandles color-coded output
3. Verify "The" → Red (T group), "cat" → Yellow (K group), "sat" → Brown (S group), etc.
4. Verify output includes both color name and hex code

**Expected result:** Each word correctly color-coded
**Pass criteria:** All words have correct color assignments
**Fail criteria:** Any word miscolored

### TEST-KDL-003 — Kandles grid generation

**Requirement:** REQ-KDL-003
**Type:** unit
**Platform:** all
**Automated:** planned
**Patent:** US 2024/0248922 A1

**Steps:**
1. Input: a text of 36 words
2. Generate Kandles grid
3. Verify grid is 6x6 (equal rows and columns)
4. Verify each cell has color, number (1-7), and original word
5. Verify grid matches expected Kandles mapping for each word

**Expected result:** Valid Kandles grid with correct dimensions and coloring
**Pass criteria:** Grid dimensions correct, all cells properly mapped
**Fail criteria:** Wrong dimensions or incorrect color assignments

### TEST-KDL-004 — Cross-language Kandles comparison

**Requirement:** REQ-KDL-004
**Type:** integration
**Platform:** all
**Automated:** planned
**Patent:** US 2024/0248922 A1

**Steps:**
1. Generate Kandles grid for an English text
2. Generate Kandles grid for a transliterated Tamil text
3. Compute similarity metric between the two grids
4. Verify similarity metric is a number in [0, 1]

**Expected result:** Valid cross-language comparison with similarity score
**Pass criteria:** Similarity metric computed, in valid range
**Fail criteria:** Comparison fails or metric out of range

---

## Hierarchical Text Decomposition

### TEST-HTD-001 — Text decomposition into stories and slices

**Requirement:** REQ-HTD-001
**Type:** unit
**Platform:** all
**Automated:** planned
**Patent:** US 2024/0248922 A1

**Steps:**
1. Upload a multi-section text
2. Decompose into stories and slices
3. Verify each slice is independently addressable (has unique ID)
4. Verify slices can be retrieved individually

**Expected result:** Text decomposed into navigable hierarchy
**Pass criteria:** All slices addressable and retrievable
**Fail criteria:** Slices not independently accessible

### TEST-HTD-002 — Slice filtering by clusters and tags

**Requirement:** REQ-HTD-002
**Type:** unit
**Platform:** all
**Automated:** planned
**Patent:** US 2024/0248922 A1

**Steps:**
1. Create slices with different cluster tags
2. Filter by a single cluster → verify correct subset returned
3. Filter by multiple clusters (AND) → verify intersection
4. Filter by multiple clusters (OR) → verify union

**Expected result:** Filtering returns correct subsets
**Pass criteria:** All filter operations return expected slices
**Fail criteria:** Incorrect filtering results

---

## Semantic Cluster Tagging

### TEST-SEM-001 — Default semantic taxonomy exists

**Requirement:** REQ-SEM-001
**Type:** smoke
**Platform:** all
**Automated:** planned
**Patent:** US 2024/0248922 A1

**Steps:**
1. Query the system for available semantic clusters
2. Verify at least Culture, Nations, Nature, Religion, People, Spiritual are present

**Expected result:** Default taxonomy available
**Pass criteria:** All 6 default clusters present
**Fail criteria:** Any default cluster missing

### TEST-SEM-002 — Manual tagging

**Requirement:** REQ-SEM-002
**Type:** unit
**Platform:** all
**Automated:** planned
**Patent:** US 2024/0248922 A1

**Steps:**
1. Upload a text segment
2. Apply a manual tag "test-label"
3. Retrieve the segment
4. Verify the tag is present

**Expected result:** Manual tag persisted and retrievable
**Pass criteria:** Tag stored and returned correctly
**Fail criteria:** Tag lost or incorrect

---

## Database Reliability (R15)

> All tests automated in `backend/tests/test_database.py`.

### TEST-DB-WAL-001 — WAL journal mode is active after connect
**Requirement:** R15 DB-WAL-1
**Type:** smoke · **Automated:** yes (covered by test_database.py connection tests)
**Pass criteria:** `PRAGMA journal_mode` returns `wal` after `Database.connect()` is called.

### TEST-DB-WAL-002 — busy_timeout is set to 5000ms
**Requirement:** R15 DB-WAL-2
**Type:** unit · **Automated:** yes
**Pass criteria:** `PRAGMA busy_timeout` returns a value ≥ 5000 after connect.

### TEST-DB-WAL-003 — No database-is-locked errors under concurrent background tasks
**Requirement:** R15 DB-WAL-5
**Type:** integration · **Automated:** yes (full test suite: 445 pass, 0 fail with background tasks active)
**Pass criteria:** The session-scoped TestClient test suite completes with 0 `OperationalError: database is locked` failures even when the backend lifespan starts discovery scheduler, model intelligence sync, and provider probe background tasks.

### TEST-DB-WAL-004 — synchronous=NORMAL is set
**Requirement:** R15 DB-WAL-3
**Type:** unit · **Automated:** yes
**Pass criteria:** `PRAGMA synchronous` returns `1` (NORMAL) or `2` (FULL) — not 0 (OFF).

---

## Evidence Graph API (R14)

> All tests in this section are **automated** (`backend/tests/test_indus_evidence_api.py`).
> Run: `pytest tests/test_indus_evidence_api.py -v`

### TEST-IEA-001 — Library endpoint shape
**Requirement:** R14.1 EG-L1
**Type:** smoke · **Automated:** yes
**Pass criteria:** `GET /api/v1/indus-evidence/library` returns 200 with `{documents, total, limit, offset}`

### TEST-IEA-002 — Library total non-negative
**Requirement:** R14.1 EG-L1
**Type:** unit · **Automated:** yes
**Pass criteria:** `total` is always an integer >= 0

### TEST-IEA-003 — Library query filter
**Requirement:** R14.1 EG-L2
**Type:** unit · **Automated:** yes
**Pass criteria:** Bogus `?q=` returns empty list with total=0

### TEST-IEA-004 — Library limit param
**Requirement:** R14.1 EG-L2
**Type:** unit · **Automated:** yes
**Pass criteria:** `?limit=1` returns at most 1 document

### TEST-IEA-005 — Claims endpoint shape
**Requirement:** R14.2 EG-C1
**Type:** smoke · **Automated:** yes
**Pass criteria:** Returns `{claims, total, limit, offset}` with list values

### TEST-IEA-006 — Claims total non-negative
**Requirement:** R14.2 EG-C1
**Type:** unit · **Automated:** yes

### TEST-IEA-007 — Claims type filter
**Requirement:** R14.2 EG-C2
**Type:** unit · **Automated:** yes
**Pass criteria:** Bogus type returns empty claims

### TEST-IEA-008 — Claims status filter
**Requirement:** R14.2 EG-C2
**Type:** unit · **Automated:** yes

### TEST-IEA-009 — Hypotheses endpoint shape
**Requirement:** R14.3 EG-H1
**Type:** smoke · **Automated:** yes
**Pass criteria:** Returns `{models: [...]}`

### TEST-IEA-010 — Hypotheses model keys
**Requirement:** R14.3 EG-H2
**Type:** unit · **Automated:** yes
**Pass criteria:** Each model has `model_id`, `model_name`, `status`, `n_claims`, `n_tests`, `file`

### TEST-IEA-011 — Sweep config GET shape
**Requirement:** R14.4 EG-S1
**Type:** smoke · **Automated:** yes
**Pass criteria:** Returns `{schema_version, sweep: {name, keywords, exclusions, sources}}`

### TEST-IEA-012 — Sweep config PUT round-trip
**Requirement:** R14.4 EG-S2
**Type:** integration · **Automated:** yes
**Pass criteria:** PUT saves, GET reflects the change

### TEST-IEA-013 — Sweep run returns ack
**Requirement:** R14.4 EG-S3
**Type:** smoke · **Automated:** yes
**Pass criteria:** POST returns `{status: 'running', message: ...}`

### TEST-IEA-014 — Sweep candidates shape
**Requirement:** R14.4 EG-S4
**Type:** unit · **Automated:** yes
**Pass criteria:** Returns `{candidates: [...]}` even when empty

### TEST-IEA-015 — Sweep intake missing url
**Requirement:** R14.4 EG-S5
**Type:** boundary · **Automated:** yes
**Pass criteria:** Empty body returns 400 or 422

### TEST-IEA-016 — Sweep intake non-PDF url
**Requirement:** R14.4 EG-S5
**Type:** unit · **Automated:** yes
**Pass criteria:** Non-PDF URL returns `{status: 'pending_manual'}`

### TEST-IEA-017 — Import URL empty body
**Requirement:** R14.1 EG-L4
**Type:** boundary · **Automated:** yes
**Pass criteria:** Empty url returns 400

### TEST-IEA-018 — Intake run returns queued
**Requirement:** R14.1 EG-L5
**Type:** smoke · **Automated:** yes
**Pass criteria:** Returns `{status: 'queued'}`

### TEST-IEA-019 — Upload non-PDF returns 400
**Requirement:** R14.1 EG-L3
**Type:** boundary · **Automated:** yes
**Pass criteria:** `.txt` file returns 400 with detail containing 'PDF'

### TEST-IEA-020 — Library offset pagination
**Requirement:** R14.1 EG-L2
**Type:** unit · **Automated:** yes
**Pass criteria:** Out-of-bounds offset returns empty list, not error

---

## Evidence Graph Atomic Nodes (R14.6)

> All tests automated in `backend/tests/test_evidence_atomic_nodes.py`.
> Run: `pytest tests/test_evidence_atomic_nodes.py -v`

### TEST-EV-REAL-01 — ClaimTester against real CISI corpus
**Requirement:** R14.6 EG-N6
**Type:** integration · **Automated:** yes
**Pass criteria:** IndusClaimTester runs on real `indus_cisi` sequences; n_tested >= 1; all result keys present

### TEST-EV-038 through TEST-EV-044 — Node registration checks
**Requirement:** R14.6 EG-N1, EG-N9
**Type:** smoke · **Automated:** yes
**Covers:** All 7 nodes registered, category='Evidence Graph', descriptions non-empty, port types valid, `claims`+`papers` colors defined, params_schema valid

### TEST-EV-001 through TEST-EV-006 — IndusLiteratureLoader
**Requirement:** R14.6 EG-N2
**Type:** unit · **Automated:** yes
**Covers:** returns papers list, total matches, max_papers respected, query filter, paper keys, text output

### TEST-EV-007 through TEST-EV-013 — IndusClaimsLoader
**Requirement:** R14.6 EG-N3
**Type:** unit · **Automated:** yes
**Covers:** returns claims, total matches, type/status filters, upstream papers filter, max_claims, type_counts shape

### TEST-EV-014 through TEST-EV-019 — CrossHypothesisMatrix
**Requirement:** R14.6 EG-N4
**Type:** unit · **Automated:** yes
**Covers:** requires claims, returns matrix, conflict detection for fish sign, n_conflicts bounds, group_by types, json output

### TEST-EV-020 through TEST-EV-025 — HiddenHypothesisGen
**Requirement:** R14.6 EG-N5
**Type:** unit · **Automated:** yes
**Covers:** requires claims, returns hypotheses, cross-paper >=2 sources, hypothesis keys, testability values, total matches

### TEST-EV-026 through TEST-EV-030 — IndusClaimTester
**Requirement:** R14.6 EG-N6
**Type:** unit · **Automated:** yes
**Covers:** requires sequences, requires claims, returns test_results, result keys, verdict values

### TEST-EV-031 through TEST-EV-034 — IndusNullModelTest
**Requirement:** R14.6 EG-N7
**Type:** unit · **Automated:** yes
**Covers:** requires sequences, requires target_sign, returns z_score/p_approx/verdict, verdict in valid set

### TEST-EV-035 through TEST-EV-037 — IndusIntakeRunner
**Requirement:** R14.6 EG-N8
**Type:** smoke · **Automated:** yes
**Covers:** returns pipeline_results, result shape, text output

---

## Evidence Graph Playwright Tests (R14.7)

> All tests automated in `frontend/e2e/evidence-graph.spec.ts`.
> Run (offline): `npx playwright test e2e/evidence-graph.spec.ts`

### TEST-PW-EG-001 through TEST-PW-EG-003 — Navigation
**Requirement:** R14.7 EG-UI1
**Type:** smoke · **Automated:** yes
**Covers:** nav item visible, clicking renders view header, subtitle text

### TEST-PW-EG-004 through TEST-PW-EG-010 — Tab bar
**Requirement:** R14.7 EG-UI2/3/4
**Type:** unit · **Automated:** yes
**Covers:** Library/Claims/Sweep buttons visible, Library default, Claims tab switches, Sweep tab switches, Library restores

### TEST-PW-EG-011 through TEST-PW-EG-020 — Library tab
**Requirement:** R14.7 EG-UI2
**Type:** integration · **Automated:** yes
**Covers:** stats row, dropzone text, secondary text, URL field, Import button, Re-run button, search field, search updates, button disabled state, paper list state

### TEST-PW-EG-021 through TEST-PW-EG-026 — Claims tab
**Requirement:** R14.7 EG-UI3
**Type:** integration · **Automated:** yes
**Covers:** total counter, search input, type dropdown, sign filter, filter typing, expand on click

### TEST-PW-EG-027 through TEST-PW-EG-035 — Sweep tab
**Requirement:** R14.7 EG-UI4
**Type:** integration · **Automated:** yes
**Covers:** Config heading, Save Config, Run Sweep, Sweep Name, Primary Keywords, Exclusions, Candidates heading, Refresh button, empty state

### TEST-PW-EG-036 through TEST-PW-EG-039 — Backend integration
**Requirement:** R14.7 all
**Type:** integration · **Automated:** yes (requires backend)
**Covers:** paper count, hypothesis models stat, claims count, sweep config name

---

## CI/CD Pipeline (R16)

> All tests in this section verify the GitHub Actions workflow in `.github/workflows/ci.yml`.

### TEST-CI-001 — Backend tests job passes
**Requirement:** R16 CICD-3
**Type:** integration · **Automated:** yes (GitHub Actions `backend-tests` job)
**Pass criteria:** `pytest backend/tests/` exits 0 with 0 failures on every push to `main`.

### TEST-CI-002 — Playwright tests job passes
**Requirement:** R16 CICD-4
**Type:** integration · **Automated:** yes (GitHub Actions `playwright-tests` job)
**Pass criteria:** `npx playwright test` exits 0; all 39 Evidence Graph tests and all navigation tests pass against a live backend.

### TEST-CI-003 — Lint job passes
**Requirement:** R16 CICD-5
**Type:** smoke · **Automated:** yes (GitHub Actions `lint` job)
**Pass criteria:** `ruff check` exits 0 with zero lint errors on the backend codebase.

### TEST-CI-004 — All three jobs required before merge
**Requirement:** R16 CICD-6
**Type:** boundary · **Automated:** yes (branch protection rule)
**Pass criteria:** PRs targeting `main` cannot be merged unless `backend-tests`, `playwright-tests`, and `lint` all pass.

---

## Evidence Graph Backend Integration Tests (R14)

> Tests in `frontend/e2e/backend-integration.spec.ts` → Evidence Graph API describe block.
> Run: `npx playwright test --config=playwright.backend.config.ts`

**Covers (14 tests):** library shape, total>=11, limit param, claims list total>=22, claims type filter, claims bogus type, hypotheses list >=2, hypotheses shape, sweep config shape, candidates shape, intake run queued, sweep run running, upload non-PDF 400, import-url 400, sweep intake pending_manual
