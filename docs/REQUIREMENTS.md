# Glossa Lab — Functional Requirements

> Last updated: 2026-05-17
> Keep this in sync with every feature change.

---

## R1 — Study Builder

### R1.1 Layout
- SB-L1: Study Builder fills the full content area with no vertical scrollbars.
- SB-L2: Canvas must not be obscured by the bottom IDE panel (use `marginBottom: effectivePanelH`).
- SB-L3: Toolbar must be a single row with no wrapping.

### R1.2 Theme
- SB-T1: Light mode: panels use `#f8fafc` bg, `#1e293b` text.
- SB-T2: Light mode: canvas uses `#f1f5f9` background (not dark `#0a0f1e`).
- SB-T3: Nodes use white bg in light mode, `#111827` in dark mode.

### R1.3 Node types (8 total)
- SB-N1: `experiment`, `pipeline`, `corpus`, `rag_query`, `ai_analysis`, `note`, `report`, `hypothesis`.
- SB-N2: Every node has a left target handle and right source handle.
- SB-N3: Every node has a header `x` delete button.
- SB-N4: Run-status dot appears on nodes during study execution.

### R1.4 Edges
- SB-E1: Edges are reconnectable by dragging an endpoint to a different handle.
- SB-E2: Dropping an endpoint without a target deletes the edge.
- SB-E3: Delete/Backspace deletes selected edges.
- SB-E4: Right-click edge shows Delete + Reverse direction menu.

### R1.5 Context menus
- SB-C1: Right-click on canvas shows add-node submenu for all 8 node types. Browser default context menu suppressed.
- SB-C2: Right-click on node shows Duplicate / Rename / Disconnect all / Delete.
- SB-C3: Menu items must execute on click (close handler must not race the click).

### R1.6 Grid / canvas
- SB-G1: 15px snap to grid.
- SB-G2: Dot grid visible in canvas background.
- SB-G3: Animated edges (purple) during run.

### R1.7 Study management
- SB-S1: Node count shown per study in the list.
- SB-S2: One-click duplicate.
- SB-S3: Export to `<name>.glossa-study.json` via toolbar.
- SB-S4: Import from JSON file via toolbar.
- SB-S5: Left panel is drag-resizable.
- SB-S6: Left panel is collapsible.
- SB-S7: Left panel dockable left or right.

### R1.8 Execution model
- SB-X1: `experiment` → sync in-process via `ExperimentBase.run()`.
- SB-X2: `pipeline` → submit Job + poll (120s timeout).
- SB-X3: `corpus` → passes `corpus_id` downstream.
- SB-X4: `rag_query` → TF-IDF search, passes retrieved chunks downstream.
- SB-X5: `ai_analysis` → sends upstream context to Glossa AI.
- SB-X6: `note`/`report`/`hypothesis` → annotation only, status `annotation`.

---

## R2 — Experiment Builder

### R2.1 Layout
- EB-L1: Fills full content area, no vertical scrollbars.
- EB-L2: Single-row toolbar.

### R2.2 Theme
- EB-T1: Light mode canvas `#f1f5f9`, nodes white. Dark mode canvas `#080d18`, nodes `#111827`.

### R2.3 Typed port system
- EB-P1: Every atomic node declares named input/output ports with explicit types.
- EB-P2: Types: `sequences`(green), `freq_map`(blue), `profiles`(purple), `clusters`(amber), `number`(red), `text`(teal), `json`(indigo), `any`(gray).
- EB-P3: Port colour consistent across handles, palette badges, and edges.
- EB-P4: Incompatible connections show amber edge + "⚠ type mismatch" label.

### R2.4 Palette completeness
- EB-A1: 11 built-in atomic nodes in palette (Sources, Transforms, Analysis, Outputs categories).
- EB-A2: ALL registered ExperimentBase subclasses appear in palette under "Experiments".
- EB-A3: Dragging a registered experiment creates an `ExperimentWrapper` node; no experiments are hardcoded.

### R2.5 Context menus
- EB-C1: Right-click canvas shows add-node menu by category.
- EB-C2: Right-click node shows Duplicate / Disconnect all / Delete.

### R2.6 Import/export (consistent with Study Builder)
- EB-E1: `↑ Import` button in toolbar imports `.glossa-exp.json`.
- EB-E2: `↓ Export` button downloads current experiment as JSON.

### R2.7 Save and run
- EB-R1: Save persists to `backend/glossa_lab/experiments/graphs/<id>.json`.
- EB-R2: Run Preview executes graph and displays result.
- EB-R3: Saved graph experiments appear in Study Builder palette as `🔀`.

---

## R3 — RAG

- RAG-I1: Index auto-builds on server startup (background task).
- RAG-I2: Index covers reports, notebooks, hypotheses, experiment descriptions.
- RAG-I3: Rebuild via `POST /api/v1/rag/index`.
- RAG-Q1: `POST /api/v1/rag/query` returns top-k chunks with `text`, `source`, `source_type`, `score`.
- RAG-AI1: Research + Study AI context modes prepend retrieved chunks to the LLM system prompt.
- RAG-G1: `rag_query` study node executes RAG search during `Run Study`.

---

## R4 — Node Registry

- NR-1: `GET /api/v1/node-registry/{type}/{ref_id}` returns JSON Schema for the node's params.
- NR-2: Supports all 8 Study Builder node types and all registered experiment/pipeline IDs.
- NR-3: Inspector uses the schema to render typed form fields.

---

## R5 — Navigation

- NAV-1: Workflow section order: Corpora → Experiments → Exp. Builder → Pipelines → Study Builder → Reports → Studies.
- NAV-2: Main column is `height: 100vh; overflow: hidden`.
- NAV-3: Canvas views get zero padding, no maxWidth, correct marginBottom.

---

## R6 — Context Menu (general)

- CTX-1: All context menus render via a floating `<div>` at `z-index: 99999` so they appear above React Flow nodes.
- CTX-2: Browser default context menu must be suppressed via `preventDefault()` in all right-click handlers.
- CTX-3: The close handler listens for `mousedown` on elements outside the menu (using `setTimeout(0)` to avoid catching the opening click).
- CTX-4: The pane right-click is attached via `onContextMenu` directly on the React Flow wrapper `<div>` (more reliable than React Flow's `onPaneContextMenu` prop).

---

## R7 — AI Chat

- CHAT-1: Floating chat window is `position: fixed`.
- CHAT-2: Context modes: Global, Corpus, Experiment, Study, Research.
- CHAT-3: Research + Study modes inject RAG chunks.
- CHAT-4: Slash commands: `/compress`, `/clear`, `/export md`, `/export pdf`, `/help`.
- CHAT-5: Major action cards require explicit user approval.

---

## R8 — Experiment Execution (Studies)

- EXEC-1: Upstream results propagated to downstream nodes via `upstream_results` kwarg.
- EXEC-2: Topological sort (Kahn's) determines execution order.
- EXEC-3: CLI-only experiments marked `skipped` with message.
- EXEC-4: Graph experiments (from Experiment Builder) are discoverable and runnable in studies.

---

## R15 — Database Reliability

> Last updated: 2026-05-17

- DB-WAL-1: The SQLite database connection MUST enable WAL (Write-Ahead Logging) journal mode immediately after opening: `PRAGMA journal_mode=WAL`.
- DB-WAL-2: The connection MUST set `PRAGMA busy_timeout=5000` to retry for up to 5 seconds before raising `OperationalError` on lock contention.
- DB-WAL-3: The connection SHOULD set `PRAGMA synchronous=NORMAL` for performance while retaining crash safety.
- DB-WAL-4: These PRAGMAs MUST be applied in `Database.connect()` before `_apply_schema()` so they take effect for all subsequent operations including seeding and migrations.
- DB-WAL-5: The application MUST NOT raise `sqlite3.OperationalError: database is locked` during the standard test suite when background tasks (discovery, model intelligence, provider probes) are running concurrently.

---

## Test Coverage Targets

| Area | Min Coverage |
|------|--------------|
| `experiment_graph.py` — atomic node functions | 80% |
| `experiment_graph.py` — `execute_graph()` | 90% |
| `rag.py` — `build_index()` + `query()` | 75% |
| `api/studies.py` — `run_study()` | 70% |
| Frontend component tests (React Testing Library) | Key interactions per builder |

---

## R9 — User-Definable Language Models (H16 Phase 1)

- LM-1: CorpusLM atomic node builds a LanguageModel from any corpus stored in the database.
- LM-2: CorpusLM accepts corpus_id and min_freq params; returns lm, n_signs, n_tokens, h1.
- LM-3: CorpusLM returns a descriptive error (not a crash) when corpus_id is missing or not found.
- LM-4: Any corpus uploaded via the Corpora tab is immediately usable as an LM source.
- LM-5: BuiltinLM is retained for backward compatibility but CorpusLM is the preferred path.

---

## R10 — User-Definable Report Templates (H16 Phase 2)

- RT-1: report_templates table stores user-defined templates (name, description, category, sections).
- RT-2: sections is a JSON array of SectionDef objects (title, data_source, data_key, chart_type, include_table).
- RT-3: GET /report-templates returns all templates; POST creates; PUT updates; DELETE removes.
- RT-4: ReportGenerator atomic node generates a structured report from a template_id + upstream data.
- RT-5: All hardcoded Python template definitions in reports.py are migrated to DB in future phase.
- RT-6: Reports & Data view splits into 📋 Reports tab (PDF/MD) and 📂 Data tab (JSON/CSV/artifacts).

---

## R11 — World Language Corpus Catalogue (H16 Phase 3)

- CC-1: corpus_catalogue table stores at least 30 world language entries on startup (idempotent seeder).
- CC-2: Entries cover undeciphered scripts, deciphered ancient scripts, and modern typological comparators.
- CC-3: GET /corpus-catalogue returns entries with already_imported flag enriched from user's corpus DB.
- CC-4: GET /corpus-catalogue supports ?undeciphered=true/false and ?script_type= filters.
- CC-5: POST /corpus-catalogue/{id}/import imports a bundled local_module entry in one click.
- CC-6: Entries without local_module return HTTP 501 with a message to upload manually.
- CC-7: Import is idempotent — re-importing an existing corpus returns already_exists reason, not an error.

---

## R12 — Anchor Set Library (H16 Phase 4)

- AS-1: anchor_sets table stores user-defined anchor pairs (cipher, target, confidence, note).
- AS-2: GET /anchor-sets returns all sets; optional ?corpus_id= filter for per-corpus sets.
- AS-3: POST creates; PUT updates; DELETE removes.
- AS-4: AnchorSetLoader atomic node loads anchor pairs from DB by anchor_set_id.
- AS-5: AnchorSetLoader returns {anchors: {cipher: target}, n_anchors, pairs} compatible with SADecipher.

---

## R13 — Governance Enforcement (H16 Phase 5)

- GOV-1: New experiment Python files must not define ExperimentBase subclasses (H15/H16).
- GOV-2: New experiment Python files must not contain hardcoded anchor dicts.
- GOV-3: New script Python files must not contain hardcoded study-specific report titles.
- GOV-4: Governance lint runs as part of the standard test suite (shell.cmd test).
- GOV-5: Legacy files in an explicit whitelist are exempted; the whitelist shrinks with migration.

---

## R14 — Evidence Graph API

> Last updated: 2026-05-17

### R14.1 Library endpoints
- EG-L1: `GET /api/v1/indus-evidence/library` returns `{documents, total, limit, offset}` with document metadata and claim counts.
- EG-L2: Supports `?q=`, `?status=`, `?limit=`, `?offset=` query params.
- EG-L3: `POST /api/v1/indus-evidence/upload` accepts multipart PDF; queues intake pipeline in background. Non-PDF returns 400.
- EG-L4: `POST /api/v1/indus-evidence/import-url` accepts `{url}` JSON; downloads PDF and queues intake. Empty url returns 400.
- EG-L5: `POST /api/v1/indus-evidence/intake/run` triggers full intake + claims extraction pipeline in background; returns `{status: 'queued'}`.

### R14.2 Claims endpoints
- EG-C1: `GET /api/v1/indus-evidence/claims` returns `{claims, total, limit, offset}`.
- EG-C2: Supports `?claim_type=`, `?claim_status=`, `?doc_id=`, `?sign=`, `?q=`, `?limit=`, `?offset=`.
- EG-C3: Each claim record includes `claim_id`, `source_document_id`, `claim_type`, `normalized_claim`, `claim_status`.

### R14.3 Hypotheses endpoint
- EG-H1: `GET /api/v1/indus-evidence/hypotheses` returns `{models}` list of hypothesis model summaries.
- EG-H2: Each model summary includes `model_id`, `model_name`, `status`, `n_claims`, `n_tests`, `file`.

### R14.4 Sweep config
- EG-S1: `GET /api/v1/indus-evidence/sweep/config` reads and returns `glossa-indus/config/sweep.yaml`. Returns 404 if file not found.
- EG-S2: `PUT /api/v1/indus-evidence/sweep/config` saves updated config to `sweep.yaml`. Returns `{status: 'saved'}`.
- EG-S3: `POST /api/v1/indus-evidence/sweep/run` builds a TopicProfile from sweep.yaml and runs enabled discovery fetchers in a background task. Returns `{status: 'running'}`.
- EG-S4: `GET /api/v1/indus-evidence/sweep/candidates` returns latest sweep candidates from log file. Returns empty list if no sweep has run.
- EG-S5: `POST /api/v1/indus-evidence/sweep/intake` accepts candidate metadata; downloads PDF if URL is direct PDF; logs to `pending_imports.jsonl` otherwise.

### R14.5 Sweep configuration schema (sweep.yaml)
- EG-SC1: `schema_version` field specifies config format version.
- EG-SC2: `sweep.keywords` has three tiers: `primary`, `secondary`, `expansions`.
- EG-SC3: `sweep.sources` is a dict keyed by source name; each has `enabled` boolean and `max_results` integer.
- EG-SC4: `sweep.exclusions` is a list of phrase strings to filter from results.
- EG-SC5: `sweep.filters.min_year`, `sweep.filters.languages`, `sweep.filters.require_open_access` filter the candidate list.
- EG-SC6: `sweep.output.auto_intake` and `sweep.output.max_candidates` control auto-processing behaviour.
- EG-SC7: The sweep.yaml schema is generic — any project can provide its own config file with the same structure.

### R14.6 Evidence Graph atomic nodes
- EG-N1: Seven atomic nodes registered in `ATOMIC_NODES` under category `Evidence Graph`.
- EG-N2: `IndusLiteratureLoader` loads papers from `glossa-indus/literature/documents/`.
- EG-N3: `IndusClaimsLoader` loads extracted claims with type/status/sign filters.
- EG-N4: `CrossHypothesisMatrix` groups claims by sign or type and computes agree/conflict verdicts.
- EG-N5: `HiddenHypothesisGen` derives compound cross-paper hypotheses requiring ≥2 source papers.
- EG-N6: `IndusClaimTester` tests positional claims against corpus sequences.
- EG-N7: `IndusNullModelTest` runs shuffle null model for sign-position enrichment.
- EG-N8: `IndusIntakeRunner` triggers intake + claims pipeline on pending uploads.
- EG-N9: New port types `claims` (#b45309) and `papers` (#0891b2) are registered in PORT_COLORS.

### R14.7 Frontend Evidence Graph workspace
- EG-UI1: Evidence Graph nav item visible in Research sidebar section.
- EG-UI2: Library tab: stat row, drag-drop dropzone, URL import, Re-run intake, search, paper list, hypothesis models.
- EG-UI3: Claims tab: filterable by type, status, sign; expandable claim cards.
- EG-UI4: Sweep tab: config editor (name, keywords, exclusions, enabled sources), Save Config, Run Sweep, candidates list with Import action.
- EG-UI5: Discovery view shows `🗂 → Evidence` action on Indus/Harappan classified items.

---

## R16 — CI/CD Pipeline

> Last updated: 2026-05-17

- CICD-1: A GitHub Actions workflow (``.github/workflows/ci.yml``) MUST run on every push and pull request to `main`.
- CICD-2: The pipeline MUST have three jobs: `backend-tests`, `playwright-tests`, and `lint`.
- CICD-3: `backend-tests` MUST run `pytest` on the full `backend/tests/` suite with zero failures as the pass criterion.
- CICD-4: `playwright-tests` MUST run `npx playwright test` against a running backend instance; all 39 Evidence Graph tests and all navigation tests MUST pass.
- CICD-5: `lint` MUST run `ruff check` on the backend codebase with zero errors as the pass criterion.
- CICD-6: All three jobs MUST complete without error before a PR may be merged.

---

## Test Coverage Targets (updated May 2026)

| Area | Tests | Min Coverage |
|------|-------|--------------|
| `experiment_graph.py` — atomic node functions | ✅ 44+ tests | 80% |
| `experiment_graph.py` — `execute_graph()` | ✅ 10+ tests | 90% |
| `database.py` — report_templates / anchor_sets / corpus_catalogue CRUD | ✅ | 90% |
| `api/report_templates.py` | ✅ | 90% |
| `api/anchor_sets.py` | ✅ | 90% |
| `api/corpus_catalogue.py` | ✅ | 80% |
| `api/indus_evidence.py` — all 11 endpoints | ✅ 20 tests | 100% |
| `experiment_graph_indus_evidence.py` — 7 nodes | ✅ 44 tests | 100% |
| Playwright — navigation | ✅ 28 tests | All nav items |
| Playwright — evidence graph | ✅ 39 tests | All 3 tabs, all features |
| Playwright — backend integration (Evidence Graph API) | ✅ 14 tests | All endpoints |
| CI/CD — GitHub Actions | ✅ 3-job workflow | push + PR |

---

## R17 — Experiment Registration Gate (H23 — MANDATORY)

> Last updated: 2026-05-17
> Enforces the 5-step gate from AGENTS.md H23. These requirements apply to every
> new research phase script added to `backend/scripts/phase*.py`.

### R17.1 — Script requirements
- EXP-S1: Every `backend/scripts/phase*.py` MUST import `torch`, detect `torch.cuda.is_available()`, and expose GPU device in its JSON output.
- EXP-S2: Every script MUST write a JSON report to `reports/` with a `_citation` key and `gpu_device` field.
- EXP-S3: Scripts that run SA MUST use `BigramScorer` from `glossa_lab.pipelines.decipher`.

### R17.2 — Graph node module requirements
- EXP-G1: Every new phase group MUST have a corresponding `backend/glossa_lab/experiment_graph_phaseNN_MM.py` module created BEFORE the scripts are run.
- EXP-G2: The module MUST use a lazy `from glossa_lab.experiment_graph import AtomicNodeDef` inside the `_node_defs()` factory function to avoid circular imports.
- EXP-G3: Every node MUST declare `gpu_device` as a text output port.
- EXP-G4: All nodes MUST use category `"Indus Decipherment"` or an approved sub-category.
- EXP-G5: The `_run_phase_script()` helper MUST use `subprocess.run` with a 900s timeout.

### R17.3 — Registration in experiment_graph.py
- EXP-R1: The `_phaseNN_MM_node_defs()` factory MUST be imported in `experiment_graph.py` via a try/except block matching the existing Phase-14/15/20 pattern.
- EXP-R2: Registration MUST be verified by running `python -c "from glossa_lab.experiment_graph_phaseNN_MM import _phaseNN_MM_node_defs; print(len(_phaseNN_MM_node_defs()), 'nodes')"` and confirming N > 0 nodes printed with no error.
- EXP-R3: The ATOMIC_NODES dict MUST contain the new node IDs after module load.

### R17.4 — Phase execution order
- EXP-O1: The 5-step gate order is MANDATORY: (1) write script, (2) create graph module, (3) register in experiment_graph.py, (4) verify registration, (5) run script.
- EXP-O2: Running a phase script before completing Steps 2-4 is a violation of R17 and H23.
- EXP-O3: The Foundation Check (`foundation_check.py`) MUST be run after every phase that modifies INDUS_FINAL_ANCHORS.json or adds new phase result files.

### R17.5 — Indus Decipherment pipeline phases (Phase-44–61)
- EXP-P1: All Phase-44 through Phase-61 research scripts have been registered as `AtomicNodeDef` nodes in the `Indus Decipherment` category.
- EXP-P2: Phase-48-55 nodes registered in `experiment_graph_phase48_55.py` (8 nodes).
- EXP-P3: Phase-56-61 nodes MUST be registered in `experiment_graph_phase56_61.py` (6 nodes) before those scripts run.
- EXP-P4: The syllabic LM (`dravidian_syllabic_lm.json`) MUST exist before Phase-52/57 SA nodes are invoked.

---

## R18 — GPU Enforcement (H20)

> Last updated: 2026-05-17

- GPU-1: All Indus Decipherment atomic nodes MUST call `_get_device()` returning `"cuda"` or `"cpu"`.
- GPU-2: All SA-based phase scripts MUST use `BigramScorer` from `glossa_lab.pipelines.decipher` which auto-selects CUDA.
- GPU-3: The `gpu_device` field MUST appear in every JSON report written by a phase script.
- GPU-4: Foundation Check `CHECK NEW-G` MUST pass (`GPU CUDA available: <device name>`).
- GPU-5: CPU-only fallback is acceptable but MUST print a warning; silent CPU fallback is forbidden.

---

## R19 — Foundation Check (H21)

> Last updated: 2026-05-17

- FC-1: `backend/scripts/foundation_check.py` MUST be run and pass (0 failures) after any phase that:
  - Modifies `backend/reports/INDUS_FINAL_ANCHORS.json`
  - Updates any `dravidian_*.json` language model
  - Adds new `phase*.json` result files to `reports/`
  - Promotes anchor confidence (MEDIUM→HIGH or LOW→MEDIUM)
- FC-2: The Foundation Check MUST include a CHECK for every new phase's key metric (z-score, concordance, coverage %).
- FC-3: Checks NEW-A through NEW-G (Phase-44 through Phase-52 results) MUST all pass.
- FC-4: Foundation Check MUST show `RESULT: N checks passed, 0 failed` before any commit involving phase results.
- FC-5: The check for HIGH anchor count MUST use `>= 7` not `== 7` to accommodate Phase-48 promotions.

---

## REQ-BE — Backend Process

- REQ-BE-001: The backend MUST start successfully in foreground mode and respond to `GET /api/v1/health` within 10 seconds.
- REQ-BE-002: The backend MUST support background/service mode, running detached from the terminal with identical health behaviour.
- REQ-BE-003: The backend MUST shut down cleanly (exit code 0) on SIGTERM / CTRL_C_EVENT within 60 seconds, releasing all database locks.
- REQ-BE-004: The backend MUST create the SQLite database file and apply the full schema automatically on first start if no database exists.

---

## REQ-API — HTTP API

- REQ-API-001: `GET /api/v1/health` MUST return HTTP 200 with valid JSON containing `status`, `version`, and `uptime_seconds` within 1 second.
- REQ-API-002: `GET /api/v1/status` MUST return HTTP 200 with system status fields including job count and pipeline state.
- REQ-API-003: All API routes MUST use the `/api/v1/` prefix; unprefixed routes MUST return 404.
- REQ-API-004: CORS headers MUST allow `http://localhost:5173` (and other configured localhost origins) when the backend runs in development mode.

---

## REQ-CFG — Configuration

- REQ-CFG-001: The backend MUST start with safe defaults when no config file exists; it MUST NOT crash on a missing config file.
- REQ-CFG-002: Environment variables (e.g. `GLOSSA_LOG_LEVEL`) MUST override file-based configuration values.
- REQ-CFG-003: Configuration file paths MUST be platform-specific: `%APPDATA%\GlossaLab\config.toml` on Windows, `$XDG_CONFIG_HOME/glossa-lab/config.toml` on Linux, `~/Library/Application Support/GlossaLab/config.toml` on macOS; dev mode always uses `./config/glossa.toml`.

---

## REQ-LOG — Logging

- REQ-LOG-001: Log output MUST be structured JSON with each line containing `timestamp`, `level`, `module`, and `message`.
- REQ-LOG-002: Log files MUST be written to the platform-appropriate path; dev mode writes to `./logs/glossa.log`.
- REQ-LOG-003: Secret values (API keys, passwords) MUST NOT appear in any log output.

---

## REQ-SEC — Security

- REQ-SEC-001: The backend HTTP server MUST bind to `127.0.0.1` (localhost only) by default and MUST NOT be accessible from external network addresses without explicit configuration.
- REQ-SEC-002: API responses MUST NOT include secret values (API keys, credentials, tokens) in any field.

---

## REQ-FE — Frontend

- REQ-FE-001: The frontend MUST communicate with backend exclusively through the versioned API (`/api/v1/`); no business logic may execute outside API calls.
- REQ-FE-002: The frontend MUST display the correct backend health status (`healthy` / `down`) reflecting the current backend state.
- REQ-FE-003: The frontend dev server (`npm run dev`) MUST start on port 5173 and serve a renderable page.

---

## REQ-TRAY — System Tray

- REQ-TRAY-001: The system tray application MUST reflect backend status (running/stopped) and update when the backend state changes.
- REQ-TRAY-002: The tray application MUST NOT contain backend logic; all interaction with the backend MUST go through HTTP or CLI invocation; no database access, pipeline logic, or job execution is permitted in the tray code.

---

## REQ-SVC — Service and Startup

- REQ-SVC-001: On Windows, the tray application MUST support registration as a startup item so that it launches automatically at login.
- REQ-SVC-002: On Linux, the backend MUST be controllable via a systemd user service unit (`systemctl --user start/stop/status glossa-lab`).
- REQ-SVC-003: On macOS, the backend MUST be controllable via a LaunchAgent plist (`launchctl load/unload`).

---

## REQ-XP — Cross-Platform

- REQ-XP-001: The backend MUST start and respond to the health endpoint identically on Windows, Linux, and macOS.
- REQ-XP-002: The setup scripts (`scripts/setup.cmd` / `scripts/setup.sh`) MUST create the virtual environment and install dependencies in a single invocation; running them a second time MUST be idempotent.
- REQ-XP-003: All backend dependencies MUST resolve from within the virtual environment; no globally-installed Python packages may be required.

---

## REQ-INT — Integration and Boundary

- REQ-INT-001: The frontend MUST NOT contain process management code (spawn, exec, kill); all service lifecycle operations are the tray's responsibility.
- REQ-INT-002: The `version` field returned by `GET /api/v1/health` MUST exactly match the version string declared in `backend/pyproject.toml`.

---

## REQ-PIPE — Analysis Pipelines

- REQ-PIPE-001: The block entropy pipeline MUST return a `block_entropies` array with entries for N=1..6, each having `raw_nats` and `normalized` fields within a valid numeric range.
- REQ-PIPE-002: The character frequency pipeline MUST return `total_symbols`, `unique_symbols`, `frequencies`, and `zipf_exponent`; frequencies MUST sum to `total_symbols`.
- REQ-PIPE-003: The pipeline engine MUST transition submitted jobs to `completed` status and make results retrievable via `GET /api/v1/jobs/{id}/results`.

---

## REQ-KDL — Kandles Phonetic-Visual Analysis

> Patent: 

- REQ-KDL-001: The Kandles phonetic mapping MUST assign each English word to the correct consonant group (1–7) and vowel-initial group (0) based on its initial phoneme.
- REQ-KDL-002: Kandles color-coded text output MUST include the correct color name and hex code for each word.
- REQ-KDL-003: Kandles grid generation MUST produce a 6×6 grid from a 36-word input with correct color assignments and group numbers per cell.
- REQ-KDL-004: Cross-language Kandles comparison MUST compute a similarity metric in [0, 1] between grids generated from texts in different languages.

---

## REQ-HTD — Hierarchical Text Decomposition

> Patent: 

- REQ-HTD-001: Text decomposition MUST split a multi-section text into independently addressable slices each with a unique ID; individual slices MUST be retrievable by that ID.
- REQ-HTD-002: Slice filtering MUST support single-cluster, multi-cluster AND, and multi-cluster OR predicates and return the correct subset in each case.

---

## REQ-SEM — Semantic Cluster Tagging

> Patent: 

- REQ-SEM-001: The default semantic taxonomy MUST include at least: Culture, Nations, Nature, Religion, People, Spiritual.
- REQ-SEM-002: Manual tags applied to a text segment MUST be persisted and returned correctly when the segment is retrieved.

