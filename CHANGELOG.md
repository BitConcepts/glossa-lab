# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-21

### Added

#### Platform
- FastAPI backend service with SQLite database (providers, experiments, studies, discovery)
- React / TypeScript / Vite frontend (pre-built artefact committed — no Node.js required on the server)
- Windows system tray application (`tray/`) with auto-start via HKCU Run entry
- Linux systemd and macOS LaunchAgent service definitions
- Shell wrappers `shell.sh` / `shell.cmd` for unified cross-platform tool invocation
- OS integration scripts `setup-os.sh` / `setup-os.cmd` for service lifecycle management
- CI pipeline: pytest (Ubuntu), Playwright (Ubuntu), shell-script functional tests (Ubuntu + macOS + Windows)

#### Backend pipelines
- 17 registered analysis pipelines: block entropy, character frequency, co-occurrence network,
  substitution-cipher decipherment, distributional decipherment, hypothesis engine, Kandles
  phonetic fingerprint, logosyllabic (Ventris-style) analysis, numeral detection, NWSP
  (Fuls method), paradigm detection, positional analysis, sign clustering, sign function
  estimator, sign polyvalence, structural fingerprint, word-structure typology
- Graph-based Experiment Builder with atomic nodes and JSON experiment specs
- Study Builder: multi-experiment DAG workflows
- Evidence Graph: literature library, PDF/URL ingestion, claim extraction, sweep pipeline,
  cross-hypothesis falsification matrix

#### AI and model intelligence
- Unified AI Provider Registry (OpenAI, Anthropic, Google, Mistral, Ollama, vLLM / custom)
- Model intelligence sync from HuggingFace Open LLM Leaderboard (nightly, with static fallback)
- Per-bucket model assignment (Reasoning / Conversational / Long-form / Global) with
  draft/apply workflow and auto-configure
- Discovery engine with 10+ fetchers (arXiv, EuropePMC, CrossRef, PubMed, DOAJ, SemanticScholar…)

#### Indus Script research outputs (`research/indus/`) — CC BY 4.0
- Preprint: *A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script:
  161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar* (Pierson 2026)
- Anchor table: 397 Mahadevan M-number signs with candidate readings, confidence levels,
  DEDR citations, and evidence basis (CSV + JSON)
- Mahadevan-Parpola M↔P crosswalk (45 entries)
- 35 computational phase reports (Phases 127–170)
- Supplemental datasets:
  - `fish_sign_compound_context.csv` — per-seal compound-context listing for M047 + M001
  - `iconographic_formula_pairs.csv` — 63 enriched INITIAL-sign × seal-icon chi-square pairs
  - `formula_bigram_table.csv` — top-30 H+M bigrams with PMI (backbone formula M342·M176)
  - `polysemy_divergence_summary.csv` — Phase-150 permutation null test (21 signs, 1000 shuffles)
- `DATA_LICENSES.md` — full data attribution and license compliance record for all upstream sources

#### Repository hygiene
- MIT license for source code; CC BY 4.0 for research outputs
- `CITATION.cff` (CFF 1.2.0) for academic software citation
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`
- Branch protection on `main` (PRs required; no direct push)
- `develop` → `main` GitFlow workflow

### Fixed
- Removed Layer1Labs proprietary license from git history; replaced with MIT throughout
- Removed patent PDFs and internal `.specsmith/` governance state from git history
  (`git filter-repo` rewrote 587 commits)
- `shell.cmd`: removed hardcoded personal machine Python paths; now uses portable `py` launcher
- `ag2_agent.py`: undefined `list_discovered_experiments` → correct `list_graph_experiments`
- `ag2_agent.py`: unused import `time`, long lines, unused variable

### Security
- `data/.keys.json` (API credentials) confirmed never tracked; added to `.gitignore`
- All SpecSmith internal governance state (`model-rate-limits.json`, governance YAMLs, etc.)
  removed from git history and gitignored
- Merkur patent PDFs (`US20240248922A1.pdf`) removed from git history

---

## How to report issues

Please use the [GitHub Issues](https://github.com/BitConcepts/glossa-lab/issues) tracker.
When filing a bug report, include:
- Your OS and Python version (`python --version`)
- Steps to reproduce
- Expected vs actual behaviour
- Any relevant log output from `logs/backend.log`

For research questions about the Indus Script decipherment methodology, open a Discussion
rather than an Issue.

[Unreleased]: https://github.com/BitConcepts/glossa-lab/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/BitConcepts/glossa-lab/releases/tag/v0.1.0
