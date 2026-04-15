# Glossa Lab — Functional Requirements

> Last updated: 2026-04-08
> Covers the April 2026 development cycle.  Keep this in sync with every feature change.

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

## Test Coverage Targets

| Area | Min Coverage |
|------|-------------|
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

## Test Coverage Targets (updated)

| Area | Min Coverage |
|------|-------------|
| `experiment_graph.py` — atomic node functions | 80% |
| `experiment_graph.py` — `execute_graph()` | 90% |
| `database.py` — report_templates / anchor_sets / corpus_catalogue CRUD | 90% |
| `api/report_templates.py` | 90% |
| `api/anchor_sets.py` | 90% |
| `api/corpus_catalogue.py` | 80% |
| Playwright — corpora, reports, experiment builder | Core interactions per view |
