# AGENTS.md — Glossa Lab Codebase Reference

Read this file at the start of every session before making any changes.

---

## Session hygiene

At the end of every session, make sure all changes are committed and pushed:

`ash
git add -A && git commit -m "chore: session close" && git push
`

Kill any background processes started during the session (uvicorn, watchers, etc.)
before exiting.

---

## For AI Agents

All codebase governance rules are defined in docs/governance/ and apply to every
session. Read the following before any non-trivial action:

- docs/governance/rules.md — hard rules (no polling loops, no secrets in code, etc.)
- docs/governance/LIFECYCLE.md — feature lifecycle and phase management
- docs/governance/context-budget.md — token / cost budgeting

**Before any action that modifies production code or data:** verify the proposed
change against docs/governance/rules.md.

**Governance data** is gitignored and lives in local runtime directories (`.specsmith/`, `.chronomemory/`)
(local runtime only — never committed).

---

## Preprint — Current Version

**Title:** A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script:
161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar

**Author:** Tristen Kyle Pierson / BitConcepts LLC

**Current version:** v4 (June 2026)

**Source:** `glossa-corpus/indus/pierson_2026_indus_decipherment.tex`

**PDF:** `glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v4.pdf`

**DOI:** https://doi.org/10.5281/ZENODO.20414696 (Zenodo)

**SSRN:** Submission ID 6827038 (check status)

**Versioning rule:** The `.tex` filename is stable (`pierson_2026_indus_decipherment.tex`).
Bump the version number in the title block and footer, and rename the PDF to
`pierson_2026_indus_decipherment_preprint_vN.pdf` on each new version.
Full version history and step-by-step bump procedure: `docs/research/PREPRINT_VERSIONING.md`.

**Attribution:** Zero tolerance for uncited material. Any contribution from private
correspondence that has not been independently published must not appear without
explicit prior consent. See `ATTRIBUTION.md`.

---

## Supplementary Rule Files

The following project-specific rule files apply to all sessions:

- `docs/research/NORMALIZATION_RULES.md` — Indus sign normalization rules for
  corpus processing and sign-ID canonicalization.
- `docs/research/PREPRINT_VERSIONING.md` — Preprint version history and naming
  conventions.

---

## MCP server

A FastMCP server lives at `backend/glossa_mcp/server.py` and exposes 27 tools
for querying and controlling the backend without manual API calls:

- **Status/metrics** — `get_status`, `get_system_metrics`
- **Jobs** — `list_jobs`, `get_job`, `create_job`, `cancel_job`, `get_job_results`
- **Experiments** — `list_experiments`, `get_experiment`, `run_experiment`
- **Research loop** — `start_research_loop`, `get_research_loop_status`,
  `stop_research_loop`, `get_research_loop_results`, `get_anchor_staging`
- **Foundation check** — `run_foundation_check`
- **Discovery** — `list_discovery_items`, `get_discovery_stats`,
  `trigger_discovery_fetch`, `update_discovery_item_status`
- **Dashboard** — `get_latest_insight`, `get_dashboard_highlights`
- **Anchor sets** — `list_anchor_sets`, `get_anchor_set`, `create_anchor_set`
- **Reports** — `list_reports`, `get_report`

The server connects to the running backend at `GLOSSA_BASE_URL`
(default: `http://127.0.0.1:8001`). Tools return clean JSON error objects when
the backend is unreachable — they never crash the MCP process.
