# glossa-lab

[![CI](https://github.com/BitConcepts/glossa-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/glossa-lab/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20414696.svg)](https://doi.org/10.5281/zenodo.20414696)
[![paper](https://img.shields.io/badge/paper-Academia.edu-blue)](https://www.academia.edu)
[![code](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![version](https://img.shields.io/badge/version-1.0.0-orange)](CHANGELOG.md)

**Author:** Tristen Pierson, BitConcepts Research \
**ORCID:** [0009-0003-7269-956X](https://orcid.org/0009-0003-7269-956X)

Agentic computational linguistics research platform for statistical analysis, decipherment, and hypothesis testing of ancient and unknown writing systems — with a primary focus on the **Indus Script**.

> **Decipherment Status (Audited):** 185 corpus-attested Proto-Dravidian readings covering 92.8% of Holdat IVS tokens · 80% agreement with Parpola (1994) on 20 tested signs · Dravidian signal confirmed on two independent corpora (Holdat 57.8%, M77 70.5%) · Reading entropy H₂ = 4.11 bits (linguistic range) · 97.7% inscription uniqueness · Sanskrit hypothesis falsified 0/34

> **Preprint (v3):** Pierson, T.K. (2026). *A Computational Decipherment Hypothesis for the Indus Script: 185 Proto-Dravidian Readings Validated Across Two Independent Corpora.* Zenodo. DOI: [10.5281/zenodo.20414696](https://doi.org/10.5281/zenodo.20414696)

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

**185 corpus-attested Proto-Dravidian readings** covering 92.8% of the Holdat IVS corpus — a computational decipherment hypothesis for the Indus Script (~2600–1900 BCE). Validated through 6 independent tests on audited data.

| Metric | Value |
|---|---|
| Corpus-attested readings | 185 signs (167 distinct readings) |
| Token coverage (HIGH only) | 92.8% (6,501/7,002 Holdat tokens) |
| Parpola agreement | 80% (15/20 exact matches, strict comparison) |
| Language discrimination | Dravidian 57.8% vs Uniform 0.0% (anchored bigram) |
| Corpus independence | M77 Dravidian hit rate: 70.5% |
| Reading entropy | H₂ = 4.11 bits (linguistic range: 2–4.5) |
| Inscription uniqueness | 97.7% (1,631/1,670 unique sequences) |
| Phonological coverage | 76% (19/25 Proto-Dravidian initials attested) |
| Sanskrit hypothesis | Falsified 0/34 |
| Total anchor signs | 605 (400 HIGH + 205 LOW unread) |
| Preprint DOI | [10.5281/zenodo.20414696](https://doi.org/10.5281/zenodo.20414696) |

> **Note:** All numbers are from `RELEASE_VALIDATION.json`, a cold re-run on audited data. See `outputs/AUDIT_CORRECTIONS.json` for full audit trail including bugs found and claims retracted.

### Key files

```
backend/reports/
├── INDUS_FINAL_ANCHORS.json          ← 605-sign anchor table with all readings
├── INDUS_DECIPHERMENT_REPORT.pdf     ← PDF report
outputs/
├── indus_decipherment_report_final.json  ← comprehensive report (JSON)
├── phase219_arxiv_updated.json       ← arXiv preprint text + data
research/indus/
├── pierson_2026_indus_preprint.pdf
└── phase_reports/
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

## Current research status (May 2026 — Audited)

- **185 corpus-attested readings** covering 92.8% of Holdat IVS tokens (7,002 tokens, 1,670 seals)
- **80% Parpola agreement** (15/20 signs match Parpola 1994/2010 proposals)
- **Corpus-independent signal**: Dravidian 57.8% (Holdat) and 70.5% (Mahadevan 1977)
- **Reading-level entropy**: H₂ = 4.11 bits (linguistic range)
- **97.7% inscription uniqueness** — supports registration-code / guild-identity model
- **76% Proto-Dravidian phonological inventory** attested (19/25 initials; 4/6 missing are expected rare)
- **Sanskrit hypothesis falsified**: 0/34 agreement with Yajnadevam readings
- **400 HIGH + 205 LOW** anchor signs (LOW signs unread, awaiting individual evidence)
- **3 bugs found and fixed** during audit (mass-assignment pipelines); **3 claims retracted** (see `outputs/AUDIT_CORRECTIONS.json`)

---

## Status

**Seeking peer review.** Release validation complete (`outputs/RELEASE_VALIDATION.json`). Backend and frontend operational at `http://localhost:8001`.
