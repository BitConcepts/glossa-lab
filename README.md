# glossa-lab

[![CI](https://github.com/BitConcepts/glossa-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/glossa-lab/actions/workflows/ci.yml)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20379070-blue)](https://doi.org/10.5281/zenodo.20379070)
[![paper](https://img.shields.io/badge/paper-Academia.edu-blue)](https://www.academia.edu)
[![code](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![version](https://img.shields.io/badge/version-1.0.0-orange)](CHANGELOG.md)

**Author:** Tristen Pierson, BitConcepts Research \
**ORCID:** [0009-0003-7269-956X](https://orcid.org/0009-0003-7269-956X)

Agentic computational linguistics research platform for statistical analysis, decipherment, and hypothesis testing of ancient and unknown writing systems — with a primary focus on the **Indus Script**.

> **Decipherment Status (re-based 2026-10-06 — see note below):** **94 strict SA-independent H+M readings** (90 HIGH + 4 MEDIUM) covering **73.68%** of Holdat IVS tokens (5,159/7,002) · Dravidian phonotactic violations: WITHDRAWN — the checker was defective (it discarded the very sounds it was meant to test for), so its zero count is not evidence; no corrected count has been run · grammar site-invariance: NOT established — the counts behind the old figure came from a statistical routine that has since been found defective, and no difference detected would not by itself prove equivalence · 44 further anchors (43 HIGH + 1 MEDIUM) flagged `pending_non_sa_validation` (SA-lineage provenance; excluded from the strict set) · Fish-sign isolation test: 0/113 isolated in the corpus and 0/27 isolated in the Gulf catalog (separate populations, reported separately — never pooled) · M267 reclassified as genitive particle · 3-slot positional grammar z=10.3 (0/2000 permutations) · Independent structural study: Nair 2026 (arXiv:2604.17828) — structural work on a different corpus; not a replication of these readings or this grammar

> **Preprint (v9):** Pierson, T.K. (2026). *A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar.* Zenodo. DOI: [10.5281/zenodo.23668053](https://doi.org/10.5281/zenodo.23668053)
>
> **Superseded:** Preprint v8 (Zenodo DOI: [10.5281/zenodo.23604590](https://doi.org/10.5281/zenodo.23604590), deposited 2026-10-23) is retained as history; v9 (deposited 2026-10-26) is the deposit of record. Concept DOI: [10.5281/zenodo.20379070](https://doi.org/10.5281/zenodo.20379070) (unchanged).

> **Re-based after Phase-107/108 (Phase-109, 2026-10-06).** The v4 preprint's headline set (161 H+M anchors / 90.96% coverage / 59% Parpola agreement) has been **retired** as this programme's headline basis. Phase-107 falsified the project's simulated-annealing (SA) machinery as evidence for sign values (held-out anchor agreement 0.000; Sanskrit and scrambled controls statistically indistinguishable from Dravidian). Phase-108 classified all 287 anchors by provenance: 44 HIGH anchors were SA-derived or SA-confirmed-only, and a 116-anchor cohort traced to research-loop heuristic tables promoted without validation. Phase-109 re-reviewed that cohort under pre-registered rules (112 prior sourced readings restored, 1 kept on Parpola crosswalk support, 3 demoted), flagged the 44 SA-lineage anchors `pending_non_sa_validation`, and individually re-reviewed M293, M362, and M398 (each HIGH → MEDIUM). Headline numbers are now the **strict SA-independent set** — anchors whose provenance chain contains no SA — recomputed fresh on the post-review anchor table (`reports/phase109_rebase.json`). The citation of record is now preprint v8 (Zenodo DOI 10.5281/zenodo.23604590, deposited 2026-10-23), which carries the re-based strict set; v4 is superseded. (Updated 2026-10-26: the deposit of record is now preprint v9, Zenodo DOI 10.5281/zenodo.23668053; the v8 statement in this note stands as the history of the 2026-10-23 deposit.) (Correction 2026-10-25, programme red team: the banner above previously named v4 as citation of record and linked a DOI that resolves to the v3.0.0 record.) Artifacts: `reports/phase107_*`, `reports/phase108_*`, `reports/phase109_*`.

> **Errata (2026-10-12).** Two figures in this README misstated the canonical anchor table (`backend/reports/INDUS_FINAL_ANCHORS.json`) and are corrected in place. (1) The full post-review anchor table holds **166 HIGH + 5 MEDIUM + 3 LOW + 113 CANDIDATE** entries (the Indus Script Decipherment section previously stated 112 LOW + 4 CANDIDATE). (2) The anchors flagged `pending_non_sa_validation` number 44, of which **43 HIGH + 1 MEDIUM** (the status banner, the metrics table, and the research-status list previously stated 44 HIGH). The one MEDIUM anchor is M293, re-reviewed HIGH → MEDIUM in Phase-109, after the Phase-108 classification that flagged the set. Corrected immediately as errata under Spec 029 decision D-C (`specs/029-tao-claim-lifecycle/audit.md` §9): factual misstatements of the canonical record, distinct from interpretive re-staging.

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

**94 strict SA-independent H+M candidate readings** (90 HIGH + 4 MEDIUM) covering 73.68% of the Holdat IVS corpus — a falsifiable computational decipherment hypothesis for the Indus Script (~2600–1900 BCE). Re-based 2026-10-06 (Phase-109; see the note at the top of this README): the full post-review anchor table holds 287 entries (166 HIGH + 5 MEDIUM + 3 LOW + 113 CANDIDATE).

| Metric | Value |
|---|---|
| Strict SA-independent H+M readings | 94 (90 HIGH + 4 MEDIUM) |
| Token coverage (strict set) | 73.68% (5,159/7,002 Holdat tokens) |
| Full H+M set (post-review) | 171 readings; 92.19% token coverage (6,455/7,002) |
| SA-lineage anchors pending validation | 44 flagged `pending_non_sa_validation` (43 HIGH + 1 MEDIUM; excluded from the strict set) |
| Phonotactic violations (strict set) | WITHDRAWN — the Phase-58 checker discarded the prohibited initial sounds before testing, so its zero is not a measurement; no corrected count has been run |
| Grammar site-invariance | NOT established — the Phase-69 routine behind the old 65/65 and 90/90 counts returned preset p-values in place of computed ones; no corrected test has been run, and no difference detected would not by itself prove equivalence |
| Parpola crosswalk comparison | WITHDRAWN as validation — the old 81/81 figure compared this project's readings against a crosswalk field that was populated from those same readings when the file was expanded (Phase-96), so agreement on those entries compares the project with itself; the number of genuinely independent comparisons has not been established. (The retired 59% figure remains not comparable, for the reasons already recorded.) |
| Positional grammar | z=10.3; 0/2000 permutations exceeded observed |
| Fish-sign isolation | 0/113 isolated (corpus); 0/27 isolated (Gulf catalog) — separate populations, reported separately |
| Independent structural study | Nair 2026 (arXiv:2604.17828), on the ICIT corpus — independent structural work on a different corpus; it does not test these readings or this grammar and is not a replication of them |
| Preprint DOI | [10.5281/zenodo.23668053](https://doi.org/10.5281/zenodo.23668053) (v9, deposit of record, deposited 2026-10-26). Superseded: v8 [10.5281/zenodo.23604590](https://doi.org/10.5281/zenodo.23604590) (2026-10-23); v4 [10.5281/zenodo.20414696](https://doi.org/10.5281/zenodo.20414696) |

> **Historical note (retired 161-anchor set — not current metrics).** Two Phase-170 figures computed on the retired 161-anchor set were previously listed in this table and are retained here as history only: seal coverage 69.8% (1,165/1,670 seals fully covered) and grammar accuracy 93.2% sign-level. They describe the retired set, not the current strict set.

### Key files

```
backend/reports/
├── INDUS_FINAL_ANCHORS.json                        ← anchor table with all readings
glossa-corpus/indus/
├── pierson_2026_indus_decipherment.tex              ← preprint source (LaTeX)
└── pierson_2026_indus_decipherment_preprint_v9.pdf  ← preprint PDF (CC BY 4.0)
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
│  ├─ glossa_mcp/       ← MCP server (Warp/Oz agent integration, 33 tools)
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

Glossa Lab ships a [FastMCP](https://github.com/jlowin/fastmcp) server that exposes 33 backend operations as MCP tools, allowing Warp's Oz agent to query and control the system directly — no manual API calls required.

### What it covers

| Category | Tools |
|---|---|
| Status | `get_status`, `get_system_metrics` |
| Jobs | `list_jobs`, `get_job`, `create_job`, `cancel_job`, `get_job_results` |
| Experiments | `list_experiments`, `get_experiment`, `run_experiment` |
| Research loop | `start_research_loop`, `get_research_loop_status`, `stop_research_loop`, `get_research_loop_results`, `get_anchor_staging` |
| Foundation check | `run_foundation_check`, `get_foundation_status` |
| Indus evidence | `list_indus_claims`, `get_indus_claim`, `get_indus_claim_aee_scores`, `list_indus_library`, `list_indus_hypotheses` |
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

### Provenance & source registry

The programme's provenance registry is indexed publicly on the Open Science Framework: [osf.io/ybd65](https://osf.io/ybd65/) — components for literature (`zbh86`), corpora (`dfrhz`), and programme outputs (`vwa7s`). The OSF project is the public index; this repository (with `CITATIONS.md`) remains canonical.

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
| `backend/glossa_mcp/server.py` | MCP server — 33 tools for Warp/Oz agent integration |

---

## Current research status (October 2026 — post Phase-109 re-base; preprint v9 of record)

- **94 strict SA-independent H+M readings** — 90 HIGH + 4 MEDIUM confidence; **73.68% token coverage** of the 7,002-token Holdat corpus
- **44 anchors flagged** `pending_non_sa_validation` (43 HIGH + 1 MEDIUM; SA-derived or SA-confirmed-only provenance, Phase-108 audit)
- **Staging cohort re-reviewed** (Phase-109): 116 research-loop-promoted anchors — 112 prior sourced readings restored, 1 kept on Parpola crosswalk support (that support has since been withdrawn by the 2026-10-26 repair audit — the crosswalk comparison is not independent evidence; the entry requires revalidation), 3 demoted; M293, M362, M398 individually re-reviewed (HIGH → MEDIUM each)
- **SA falsified as evidence for sign values** (Phase-107): held-out agreement 0.000, controls non-discriminating; governance rule **H26** — no SA-sufficient promotion gates
- **Fish-sign isolation test**: 0/113 isolated in the corpus and 0/27 isolated in the Gulf catalog (separate populations, reported separately — never pooled)
- **M267 reclassified**: genitive particle (iN/in), not fish sign
- **Three-slot grammar** (CLASSIFIER–TITLE–SUFFIX): z=10.3, 0/2000 permutations
- **Independent structural study**: Nair 2026 (arXiv:2604.17828) — structural work on a different corpus (ICIT); it does not test these readings or this grammar and is not a replication of them
- **Preprint v9** is the citation of record (Zenodo DOI 10.5281/zenodo.23668053, deposited 2026-10-26), superseding v8

---

## Status

**Preprint v9 published (Zenodo DOI: 10.5281/zenodo.23668053; v8, DOI 10.5281/zenodo.23604590, superseded). Not peer-reviewed.** Backend and frontend operational at `http://localhost:8001`.
