# glossa-lab

![CI](https://github.com/layer1labs/glossa-lab/actions/workflows/ci.yml/badge.svg)

Agentic computational linguistics research platform for statistical analysis, decipherment, and hypothesis testing of ancient and unknown writing systems — with a primary focus on the **Indus Script** (Mahadevan corpus, Holdat LLC dataset) using methods developed by Dr. Andreas Fuls (TU Berlin / ICIT).

Built and maintained by **Layer1Labs Silicon, Inc.**

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

### Agent-Stack (layer1labs server — separate repo)

Three vLLM services on NVIDIA RTX PRO 5000 Blackwell (48 GB GDDR7):
- **l1-nexus** (port 8000) — `cpatonn/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit` — primary coding/agentic
- **l1-glossa** (port 8001) — `Qwen/Qwen3-14B` — research/long-context reasoning
- **l1-embed** (port 8002) — `BAAI/bge-m3` — embeddings (RAG)

Access via Tailscale (`100.118.107.3`). Repo: `layer1labs/agent-stack`.

---

## Repository structure

```text
glossa-lab/
├─ AGENTS.md            ← agent operating rules (read first, every session)
├─ LEDGER.md            ← session ledger (sole continuity authority)
├─ README.md
├─ CITATIONS.md         ← citation registry for all research data
├─ setup-os.cmd         ← canonical start/stop/restart (Windows)
├─ shell.cmd            ← tool wrapper (pytest, ruff, python — Windows)
├─ shell.sh             ← tool wrapper (Linux/macOS)
├─ .github/
│  └─ workflows/ci.yml  ← GitHub Actions CI (pytest + Playwright + evidence scripts)
├─ backend/
│  ├─ glossa_lab/       ← FastAPI app + all Python modules
│  │  ├─ api/           ← REST route modules
│  │  │  └─ indus_evidence.py ← Evidence Graph API (library, claims, sweep)
│  │  ├─ experiments/   ← ExperimentBase subclasses + graph JSONs
│  │  ├─ experiment_graph_indus_evidence.py ← 7 Evidence Graph atomic nodes
│  │  ├─ discovery/     ← literature discovery engine + fetchers
│  │  ├─ data/          ← corpora, anchor sets, LM files (cited per H18)
│  │  └─ model_intelligence.py ← HF leaderboard sync + scoring
│  ├─ reports/          ← experiment results, phase syntheses
│  └─ scripts/          ← utility and research scripts
├─ frontend/
│  ├─ src/              ← React source
│  │  └─ components/IndusEvidenceView.tsx ← Evidence Graph three-tab workspace
│  └─ dist/             ← built artefact (committed for server deploy)
├─ glossa-indus/        ← Indus Evidence Graph data store
│  ├─ config/sweep.yaml ← per-project sweep configuration (editable)
│  ├─ literature/       ← registered papers (JSON metadata)
│  ├─ claims/           ← extracted claims per document
│  ├─ hypotheses/       ← hypothesis model YAMLs
│  ├─ raw/user_uploads/ ← user-uploaded PDFs
│  └─ scripts/          ← intake + claims extraction pipeline
├─ tray/                ← system tray app
├─ docs/
│  ├─ USER_GUIDE.md
│  ├─ user-manual.md
│  ├─ architecture.md
│  └─ research/         ← decipherment research docs
├─ services/            ← systemd/launchd/Windows service definitions
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

## Research governance

- **H18** — Every data file must have `_citation` traceable to `CITATIONS.md`
- **H19** — Foundation check must PASS before external communication
- Current: **17 PASS / 0 FAIL / 0 WARN** (`GET /api/v1/research/foundation-check`)

---

## Documentation

| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent rules, start/stop commands, hard rules |
| `LEDGER.md` | Session ledger — sole continuity authority |
| `CITATIONS.md` | Research data citation registry |
| `docs/USER_GUIDE.md` | Full user guide (all panels) including Evidence Graph |
| `docs/architecture.md` | System architecture including Evidence Graph layer |
| `docs/REQUIREMENTS.md` | Formal requirements (R1–R14, incl. R13 Evidence Graph) |
| `docs/TEST_SPEC.md` | Test specification (TEST-IEA, TEST-EV, TEST-PW-EG) |
| `docs/research/` | Decipherment research documents |
| `docs/guides/` | How-to guides (experiments, pipelines, studies) |
| `glossa-indus/LEDGER.md` | Evidence Graph batch work log |

---

## Current research status (May 2026)

- **333/390 signs assigned** — 85.4% coverage, 17 HIGH-confidence anchors
- **99.2% token coverage** on Holdat corpus (1,670 seals / 7,002 tokens)
- **Phase-29d**: Enmenanak confirmed top candidate (score 7.0, p<0.001)
- **Phase-31 T3**: Indus Script and Tamil-Brahmi both in syllabic Zipf regime (δ=0.177)
- **Phase-43 (May 2026)**: 231.9σ positional structure confirmed; Hunt tripartite formula 59× lift
- **Evidence Graph (May 2026)**: 11 papers registered, 22 claims extracted across Parpola/FSW/Yadav/Roif/Hunt
- **TB correlation**: 0.907 (post M267 correction)

---

## Status

**Production — active research.** Backend and frontend fully operational at `http://localhost:8001`.
