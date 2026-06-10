# glossa-lab

[![CI](https://github.com/BitConcepts/glossa-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/glossa-lab/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20414696.svg)](https://doi.org/10.5281/zenodo.20414696)
[![paper](https://img.shields.io/badge/paper-Academia.edu-blue)](https://www.academia.edu)
[![code](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![version](https://img.shields.io/badge/version-1.0.0-orange)](CHANGELOG.md)

**Author:** Tristen Pierson, BitConcepts Research \
**ORCID:** [0009-0003-7269-956X](https://orcid.org/0009-0003-7269-956X)

Agentic computational linguistics research platform for statistical analysis, decipherment, and hypothesis testing of ancient and unknown writing systems — with a primary focus on the **Indus Script**.

> **Decipherment Status (v4 preprint):** 161 H+M candidate readings (75 HIGH + 86 MEDIUM) covering 90.96% of Holdat IVS tokens · 59% agreement with Parpola (1994) · Fish-sign isolation test: 0/140 isolated across all 9 sites and Gulf catalog · M267 reclassified as genitive particle · 3-slot positional grammar z=10.3 (0/2000 permutations) · Independent replication: Nair 2026 (arXiv:2604.17828)

> **Preprint (v4):** Pierson, T.K. (2026). *A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar.* Zenodo. DOI: [10.5281/zenodo.20414696](https://doi.org/10.5281/zenodo.20414696)

Built and maintained by **[BitConcepts LLC](https://bitconcepts.tech)**

---

## Overview

Glossa Lab is a production research tool combining a Python backend, React frontend, and Windows/Linux/macOS service support. It provides an end-to-end environment for:

- **Corpus management** — upload, register, inspect, and sanitise sign-sequence corpora
- **Statistical analysis** — entropy, Zipf, positional profiles (T/I/M), writing-system classification
- **Decipherment experiments** — SA-based sign-to-phoneme hypothesis generation, benchmarks vs known scripts
- **Experiment Builder** — composable graph experiments using atomic nodes (no coding required); new **Evidence Graph** category with 7 nodes for comparative literature analysis
- **Study Builder** — multi-experiment research workflows as visual graphs
- **Glossa AI** — embedded research assistant that runs analyses, proposes hypotheses, and navigates the tool
- **Discovery engine** — continuous literature discovery across arXiv, EuropePMC, CrossRef, DOAJ and more
- **Evidence Graph** — per-project literature library, automated paper sweep (configurable via `sweep.yaml`), claim extraction, cross-hypothesis falsification matrix, and hidden hypothesis generation
- **AI Provider Registry** — unified management of cloud (OpenAI, Anthropic, Mistral, Google…), local (Ollama), and self-hosted (vLLM) AI backends with model scoring and smart assignment
- **Reports & Data** — PDF, Markdown, JSON, CSV export of all results

---

## System architecture

```text
[ Tray ] ─────┐
              │
[ Frontend ] ─┼──→ [ Backend Service (FastAPI) ] ──→ [ Pipelines / Jobs / Models ]
              │              │
[ CLI / Dev ] ┘         [ SQLite DB ]
                              │
                    [ Provider Registry ] ──→ [ Cloud / Ollama / vLLM ]
```

### Key principles

- The backend is the **source of truth**
- The tray and frontend are **interfaces**, not runtime owners
- All communication occurs through **explicit REST APIs**
- Service lifecycle is **deterministic and observable** — every background process logs START/COMPLETE

---

## Components

### Backend (Python / FastAPI)

- REST API + background job engine
- SQLite database (providers, model scores, discovery items, experiments, studies)
- AI provider registry with test/probe on startup and on-demand
- HuggingFace Open LLM Leaderboard sync (nightly) + static fallback scores
- Discovery engine with 10+ fetchers (arXiv, EuropePMC, CrossRef, PubMed, DOAJ…)
- RAG index for research context injection
- Ollama auto-detection and lifecycle management

### Frontend (React / TypeScript / Vite)

Built artefact (`frontend/dist/`) is committed to the repo so the server only needs `git pull` — no Node.js required on the deployment target.

Key panels:
- **Provider Registry** — add/test/manage AI providers; badges: 🦙 Ollama · ☁️ Cloud · ⚡ vLLM/Custom · 🤗 HuggingFace
- **Model Assignments** — assign primary/fallback models per bucket (Reasoning / Conversational / Long-form / Global) with draft/apply workflow, scores, filter, and swap
- **Experiment Builder** — visual DAG editor with `Evidence Graph` palette category (7 nodes)
- **Study Builder** — multi-experiment research workflows (accessible via Projects)
- **Discovery View** — literature feed with `→ Evidence` import action for Indus/Harappan items
- **Evidence Graph** — three-tab workspace: Library (PDF upload, URL import), Claims (filterable), Sweep (configurable sweep + candidate import)
- **Foundation Check** — research integrity dashboard (17 checks; must be PASS before external communication)
- **Bottom Panel** — structured Logs (JSON → human-readable), Jobs, Terminal

### Tray (Windows/macOS)

Local control surface. Start/stop/restart backend, open UI, quick status.

---

## Indus Script Decipherment

**161 H+M candidate readings** (75 HIGH + 86 MEDIUM) covering 90.96% of the Holdat IVS corpus — a falsifiable computational decipherment hypothesis for the Indus Script (~2600–1900 BCE).

| Metric | Value |
|---|---|
| H+M candidate readings | 161 (75 HIGH + 86 MEDIUM) |
| Token coverage (H+M) | 90.96% (6,363/7,002 Holdat tokens) |
| Seal coverage | 69.8% (1,165/1,670 seals fully covered by H+M) |
| Parpola agreement | 59% (44/75 HIGH readings in Parpola 1994) |
| Positional grammar | z=10.3; 0/2000 permutations exceeded observed |
| Fish-sign isolation | 0/140 isolated (0/113 corpus + 0/27 Gulf) |
| External replication | Nair 2026 (arXiv:2604.17828) on ICIT corpus |
| Grammar accuracy | 93.2% sign-level at 161 H+M (Phase-170) |
| Preprint DOI | [10.5281/zenodo.20414696](https://doi.org/10.5281/zenodo.20414696) |

### Key files

```
backend/reports/
├── INDUS_FINAL_ANCHORS.json                        ← anchor table with all readings
glossa-corpus/indus/
├── pierson_2026_indus_decipherment.tex              ← preprint source (LaTeX)
└── pierson_2026_indus_decipherment_preprint_v4.pdf  ← preprint PDF (CC BY 4.0)
research/indus/
└── phase_reports/                                   ← all phase analysis reports
```

---

## Repository structure

```text
glossa-lab/
├─ LICENSE              ← MIT (source code)
├─ AGENTS.md            ← agent operating rules (read first, every session)
├─ LEDGER.md            ← session ledger (sole continuity authority)
├─ README.md
├─ CITATIONS.md         ← citation registry for all research data
├─ setup-os.cmd / setup-os.sh  ← start/stop/restart
├─ shell.cmd / shell.sh        ← tool wrapper (pytest, ruff, python)
├─ .github/
│  └─ workflows/ci.yml  ← GitHub Actions CI
├─ backend/             ← Python FastAPI application
│  ├─ glossa_lab/       ← app modules (api/, experiments/, discovery/, ...)
│  ├─ glossa_mcp/       ← MCP server (Warp/Oz agent integration, 27 tools)
│  ├─ scripts/          ← all research and utility scripts
│  └─ tests/
├─ frontend/            ← React / TypeScript / Vite
│  ├─ src/
│  └─ dist/             ← built artefact (committed for server deploy)
├─ tray/                ← system tray app
├─ services/            ← systemd / launchd / Windows service definitions
├─ docs/
│  ├─ images/           ← diagrams and sign images
│  ├─ governance/       ← governance docs
│  ├─ research/         ← decipherment research docs
│  ├─ USER_GUIDE.md
│  ├─ architecture.md
│  └─ REQUIREMENTS.md
├─ data/                ← canonical corpus and reference data
│  ├─ crosswalks/       ← sign crosswalk CSVs (M-number ↔ Parpola, ICIT/Fuls)
│  ├─ raw/              ← raw source corpora
│  ├─ normalized/       ← cleaned / extracted corpus files
│  └─ import/           ← staged import artifacts
├─ outputs/             ← generated computational artifacts
│  └─ analysis/         ← summary JSON analysis files
├─ reports/             ← human-readable research reports (PDF, Markdown)
├─ research/            ← public preprint outputs
│  └─ indus/            ← preprint PDF, anchor table, phase reports (CC BY 4.0)
├─ scripts/             ← project-wide utility scripts
├─ glossa-corpus/       ← internal corpus store
├─ glossa-indus/        ← Evidence Graph data store
│  ├─ config/sweep.yaml
│  ├─ literature/ · claims/ · hypotheses/ · raw/
│  └─ scripts/
└─ corpora/             ← external corpus downloads (gitignored, ~3 GB)
```

---

## Quick start

### Windows

```powershell
# First-time install (registers autostart, installs deps)
setup-os.cmd install

# Start backend + tray
setup-os.cmd start

# Verify
curl.exe -sf http://localhost:8001/api/v1/health
```

### Linux (systemd)

```bash
cd backend && python3 -m venv venv && venv/bin/pip install -e .
sudo systemctl start glossa-lab
curl -sf http://localhost:8001/api/v1/health
```

Open `http://localhost:8001` in your browser.

---

## Development workflow

All non-trivial work follows the proposal-first cycle in `AGENTS.md`. **Frontend changes require a rebuild before they are visible:**

```powershell
cd frontend && npm run build
# Verify served bundle:
curl.exe -sf http://localhost:8001/ | Select-String 'index-[A-Za-z0-9]+\.js'
```

---

## MCP server (Warp / Oz)

Glossa Lab ships a [FastMCP](https://github.com/jlowin/fastmcp) server that exposes 27 backend operations as MCP tools, allowing Warp's Oz agent to query and control the system directly — no manual API calls required.

### What it covers

| Category | Tools |
|---|---|
| Status | `get_status`, `get_system_metrics` |
| Jobs | `list_jobs`, `get_job`, `create_job`, `cancel_job`, `get_job_results` |
| Experiments | `list_experiments`, `get_experiment`, `run_experiment` |
| Research loop | `start_research_loop`, `get_research_loop_status`, `stop_research_loop`, `get_research_loop_results`, `get_anchor_staging` |
| Foundation check | `run_foundation_check` |
| Discovery | `list_discovery_items`, `get_discovery_stats`, `trigger_discovery_fetch`, `update_discovery_item_status` |
| Dashboard | `get_latest_insight`, `get_dashboard_highlights` |
| Anchor sets | `list_anchor_sets`, `get_anchor_set`, `create_anchor_set` |
| Reports | `list_reports`, `get_report` |

### Setup

1. **Start the backend** (`setup-os.cmd start` or `uvicorn glossa_lab.main:create_app --factory --port 8001`).
2. In Warp, open **Settings → Agents → MCP Servers** and add a new server with:

```json
{
  "glossa-lab": {
    "command": "C:/Users/trist/Development/BitConcepts/glossa-lab/backend/venv/Scripts/python.exe",
    "args": ["C:/Users/trist/Development/BitConcepts/glossa-lab/backend/glossa_mcp/server.py"]
  }
}
```

Adjust the path to match your install location. The server defaults to `http://127.0.0.1:8001`; override with the `GLOSSA_BASE_URL` environment variable if needed.

### Source

```
backend/glossa_mcp/
├── __init__.py
└── server.py   ← FastMCP server (edit here to add tools)
```

---

## Project discipline

This project follows strict research governance enforced by both convention and tooling:

- **Append-only ledger** — Every session's work is recorded in `LEDGER.md`. No ledger entry = work not done.
- **Data provenance** — Every data file must have a citation traceable to `CITATIONS.md`. No uncited data in the pipeline.
- **Graph-first experiments** — All research phases are registered as navigable experiment graph nodes (see `backend/glossa_lab/experiment_graph*.py`). No ad-hoc scripts without graph registration.
- **Foundation checks** — `backend/scripts/foundation_check.py` must pass before any external communication or publication. This guards against regressions in anchor data, grammar metrics, and sign accounting.
- **Public/private boundary** — Private correspondence lives in `.correspondence/` (gitignored). No third-party emails or private contact details in tracked files.
- **AI disclosure** — All AI-assisted work is disclosed in publications and the ledger. Statistical tests are designed and interpreted by the author; AI tooling is used for scripting, data management, and literature search.

Full governance rules: [`docs/governance/`](docs/governance/)

---

## Documentation

| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent operating rules — read first every session |
| `LEDGER.md` | Append-only session ledger — the sole continuity authority |
| `CITATIONS.md` | Research data citation registry |
| `docs/governance/` | Hard rules, session protocol, roles, verification |
| `docs/USER_GUIDE.md` | Full user guide (all panels) |
| `docs/architecture.md` | System architecture |
| `docs/REQUIREMENTS.md` | Formal requirements (R1–R16) |
| `docs/TESTS.md` | Test specification |
| `docs/research/` | Decipherment research documents |
| **`research/indus/`** | **Public outputs — preprint PDF, anchor table, phase reports (CC BY 4.0)** |
| `backend/glossa_mcp/server.py` | MCP server — 27 tools for Warp/Oz agent integration |

---

## Current research status (June 2026 — Preprint v4)

- **161 H+M candidate readings** — 75 HIGH + 86 MEDIUM confidence (4 PROVISIONAL_MEDIUM flagged)
- **90.96% token coverage** of the 7,002-token Holdat corpus; 69.8% of seals fully covered
- **59% Parpola agreement**: 44/75 HIGH readings appear in Parpola (1994)
- **Fish-sign isolation test**: 0/140 isolated across all 9 sites and Gulf deposit catalog
- **M267 reclassified**: genitive particle (iN/in), not fish sign
- **Three-slot grammar** (CLASSIFIER–TITLE–SUFFIX): z=10.3, 93.2% sign-level accuracy
- **External replication**: Nair 2026 (arXiv:2604.17828) confirms non-random structure on ICIT corpus
- **4 provisional sibilant readings** (M330, M165, M202, M198) added in Phase-163/166
- **Preprint v4** available at `glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v4.pdf`

---

## Status

**Preprint v4 published (Zenodo DOI: 10.5281/zenodo.20414696). Seeking peer review.** Backend and frontend operational at `http://localhost:8001`.
