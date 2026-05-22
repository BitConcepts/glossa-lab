# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Indus Script research — network centrality analysis (Phases 172–178)
- **Phase 172**: Full H+M×H+M directed bigram graph (161 nodes, 414 edges, Holdat LLC CSV)
  with betweenness centrality (BC) stratification; 20 grammar candidates (BC > 0),
  141 name-syllable candidates (BC = 0)
- **Phase 173**: BC check on 18 irresolvable MEDIAL signs — all 18 confirmed BC = 0
  (personal-name syllable signature)
- **Phase 174**: Betweenness-filtered Meluhhan name matching — 3 names at 100% phonological
  coverage (Nanna-a, Anana, Ama-e-a); 14 phoneme gaps identified for ICIT targeting
- **Phase 175**: Site-stratified grammar/name proportion proxy — grammar ratio ~72% at all
  5 sites (Pearson r = −0.685, NOT_SUPPORTED); Rakhigarhi absent from 5-site subset
- **Phase 176**: M059 bridge-role analysis — MIXED_BRIDGE (I=19%, M=47%, T=34%), rank 18;
  not a pure INITIAL hub as previously classified from Firestore corpus
- **Phase 177**: Full T/I/M positional rates + BC-to-slot mapping for all 161 H+M signs;
  M267 confirmed rank 3 MEDIAL bridge (81% MEDIAL, BC = 0.051); M342 rank 1 structural hub
  (BC = 0.055); M099 rank 10 confirmed bridge (77% MEDIAL)
- **Phase 178**: ICIT-priority phoneme targeting — 14 true gaps, 2 LOW upgrade candidates
  (M386, M143 for /man/)
- **Preprint §3.32**: New section *Betweenness Centrality Stratification (Phases 172–177)*
  added to `glossa-corpus/indus/preprint_v1.tex`; PDF recompiled and published
- §1.3 item 19 and updated Acknowledgments (Roif directed-graph methodology credit)

### Fixed

#### Indus Script — corpus loader correctness
- **Root cause resolved**: `load_holdat()` in Phases 172–178 scripts was calling
  `indus_corpus_v3.load_corpus()` (RMRL Firestore dump, 3,137 sideline sequences)
  instead of the Holdat LLC CSV (1,670 unified per-seal sequences). The Firestore corpus
  splits inscriptions by sideline, causing M267 to appear 81% INITIAL (starts the second
  sideline of compound inscriptions) rather than the correct 81% MEDIAL.
- Both `phase172_174_betweenness_stratification.py` and `phase175_178_network_deep.py`
  now load directly from `indus_corpus 2.csv` via the `position` column for correct
  sign ordering within each unified seal sequence.
- **Phase 175 site distribution** corrected: `load_site_distribution()` previously read
  `holdatllc_core_symbol_site_distribution.csv` which covers only M100-M416 (sparse subset)
  and excludes all 20 grammar candidates. Now reads the Holdat LLC CSV `site` column
  directly, giving correct token counts for all 161 H+M signs.
- Phase 177 `dominant_slot()` extended with `_P177_FUNCTIONAL_OVERRIDES` for confirmed
  grammar signs whose absolute corpus position is ambiguous in unified sequences (e.g.
  terminal markers that precede other suffixes in the same inscription).

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
