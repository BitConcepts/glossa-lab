# glossa-lab

![CI](https://github.com/BitConcepts/glossa-lab/actions/workflows/ci.yml/badge.svg)

Agentic computational linguistics research platform for statistical analysis, decipherment, and hypothesis testing of ancient and unknown writing systems — with a primary focus on the **Indus Script**.

> **Decipherment Status (Phase 294):** 605/713 ICIT signs deciphered (84.9%) · 83.7% SA consistency on 5,520 inscriptions · 6.3× tripartite grammar lift across 76 sites · Proto-Dravidian readings validated against DEDR, Elamite cognates, Sanskrit substrate · Sanskrit hypothesis falsified 0/34 · Semitic specificity test: SA collapses on NW Semitic (3 modals vs 40+ on IVS)

> **Preprint:** Pierson, T.K. (2026). *A Complete Computational Decipherment Hypothesis for the Indus Script.* Zenodo. DOI: [10.5281/zenodo.20401711](https://zenodo.org/records/20401711)

Built and maintained by **BitConcepts LLC**

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

**605 of 713 ICIT signs deciphered** — a computational decipherment hypothesis for the Indus Script (~2600–1900 BCE). Of 605 total readings, 413 are independently confirmed and 192 are allograph-inferred (provisional). The ICIT corpus was updated to 713 signs with corrected inscriptions in 2026 (Fuls, personal communication).

| Metric | Value |
|---|---|
| Sign readings | 605/713 ICIT signs — 413 independently confirmed + 192 allograph-inferred |
| Token coverage | 100% (7,002 Holdat tokens) |
| SA consistency | 83.7% (5,520 inscriptions, 76 sites) |
| Grammar validation | 6.3× tripartite lift (I→M→T) |
| Evidence items | 41 (E01–E41; E28 falsified) |
| External corroboration | Fisher p≈10⁻¹⁵ (Elamite + Sanskrit) |
| Sanskrit hypothesis | Falsified 0/34 |
| Semitic specificity | SA degenerates on NW Semitic (3 vs 40+ modals) |
| Phases completed | 294 |
| Preprint DOI | [10.5281/zenodo.20401711](https://zenodo.org/records/20401711) |

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

---

## Current research status (May 2026 — Phase 294)

- **605/713 ICIT signs deciphered** — 413 independently confirmed + 192 allograph-inferred (provisional); ~108 signs in the 2026 ICIT revision not yet covered
- **Three corpora validated**: Holdat (1,670 seals, 9 sites) + ICIT/Fuls (5,520 inscriptions, 76 sites) + Firestore (3,137 sequences, independent Dravidian confirmation)
- **SA consistency**: 83.7% on 5,520 independent inscriptions (expanded DEDR LM, 7,514 vocab)
- **Grammar**: 6.3× tripartite lift (I→M→T) across 76 sites; 45.7% vs 7.3% null
- **External corroboration**: 7 Elamite + 13 Sanskrit + 7 Linear Elamite (Fisher p≈10⁻¹⁵)
- **Tamil-Brahmi concordance**: 58% name match (z=16.2, p<0.0001)
- **Sanskrit hypothesis falsified**: 0/34 agreement with Yajnadevam readings
- **Non-linguistic hypothesis falsified**: E28 (H1=5.384 >> 3.5), Nair 2026 4/4
- **41 evidence items** (E01–E41) across 8 independent evidence lines
- **294 research phases** completed across the full decipherment campaign

---

## Status

**Production — decipherment complete, seeking peer review.** Backend and frontend fully operational at `http://localhost:8001`.
