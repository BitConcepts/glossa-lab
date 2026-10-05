# 001 — Glossa Lab Baseline (as-built)

**Status:** Baseline specification of the platform as it exists at adoption
of the spec-kit + AEE flow (2026-10-05). This spec describes shipped,
observable behaviour only; it invents no new features or claims.

**Assumptions (H13 epistemic boundaries):**
- The README, `docs/REQUIREMENTS.md`, `docs/architecture.md`, and the v4
  preprint are the authoritative descriptions of the as-built system.
- Research metrics below are the project's own published figures from the
  v4 preprint; this baseline records them, it does not re-verify them.

## What Glossa Lab is

An agentic computational linguistics research platform for statistical
analysis, decipherment, and hypothesis testing of ancient and unknown
writing systems, with a primary focus on the Indus Script. Built and
maintained by BitConcepts LLC. Open source (MIT for code, CC BY 4.0 for
research outputs in `research/indus/`).

## As-built components

### Backend (Python / FastAPI, `backend/glossa_lab/`)
- REST API + background job engine; SQLite database (providers, model
  scores, discovery items, experiments, studies).
- AI Provider Registry: cloud (OpenAI, Anthropic, Mistral, Google, …),
  local (Ollama), and self-hosted (vLLM) backends, with model scoring
  and per-bucket assignment.
- Discovery engine: literature/news discovery across arXiv, EuropePMC,
  CrossRef, DOAJ, PubMed, OpenAlex, Semantic Scholar, GDELT, and more
  (see `specs/002-gdelt-ngrams-and-frontier-methods/` for the GDELT
  source migration).
- Evidence Graph: per-project literature library, automated paper sweep,
  claim extraction, cross-hypothesis falsification matrix, hidden
  hypothesis generation.
- Experiment Builder (composable graph experiments from atomic nodes) and
  Study Builder (multi-experiment workflows as visual graphs).
- Glossa AI: embedded research assistant.
- Foundation Check: research-integrity dashboard (must PASS before
  external communication — constitution §III).
- MCP server (`backend/glossa_mcp/`, FastMCP, 27 tools) for agent
  integration.
- Reports export: PDF, Markdown, JSON, CSV.

### Frontend (React / TypeScript / Vite, `frontend/`)
- Panels for Provider Registry, Model Assignments, Experiment Builder,
  Study Builder, Discovery, Evidence Graph, Foundation Check, and a
  structured bottom panel (Logs / Jobs / Terminal).
- The built artefact (`frontend/dist/`) is committed so deployment
  targets need no Node.js.

### Tray / services
- System tray app (Windows/macOS) and systemd / launchd / Windows
  service definitions for lifecycle management. The backend is the
  source of truth; tray and frontend are interfaces, not runtime owners.

## Indus Script decipherment status (as published, preprint v4)

- 161 H+M candidate proto-Dravidian readings (75 HIGH + 86 MEDIUM)
  covering 90.96% of Holdat IVS tokens; 69.8% of seals fully covered.
- 59% agreement of HIGH readings with Parpola (1994).
- Three-slot positional grammar: z = 10.3 (0/2000 permutations).
- Fish-sign isolation test: 0/140 isolated.
- Independent replication: Nair 2026 (arXiv:2604.17828).
- Preprint v4: Pierson, T.K. (2026), *A Falsifiable Computational
  Decipherment Hypothesis for the Indus Valley Script*, Zenodo,
  DOI 10.5281/zenodo.20414696. Status: seeking peer review.

## Governance baseline

- Constitution: `.specify/memory/constitution.md`.
- Hard rules: `docs/governance/rules.md`; lifecycle:
  `docs/governance/LIFECYCLE.md`.
- Continuity: append-only `LEDGER.md`; citations: `CITATIONS.md`.
- Core claim scoring runs on the Applied Epistemic Engineering library
  via `backend/glossa_lab/aee_core.py` (see plan.md).
