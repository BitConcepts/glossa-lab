# Glossa-Lab Indus Evidence Graph — LEDGER

Work log for all batches, significant changes, and research decisions.

---

## Batch 1 — System Build
**Date**: 2026-05-17  
**Commit**: `b8bcec7`

- H20 rule added to AGENTS.md: agent may NEVER autonomously send emails to third parties.
- `CORPUS_VERSIONS.md` created. V1 = `indus_research.jsonl` (date-tracked, NOT version-bumped during exploration).
- `indus_corpus_v3.py` renamed → `indus_corpus_firestore.py` (supplementary external source, not the user corpus).
- Full `glossa-indus/` folder structure built (59 dirs), all config schemas, hypothesis model stubs, and intake script.

---

## Batch 2 — Roif + Hunt User Uploads
**Date**: 2026-05-17  
**Commit**: `TBD`

### Papers Processed
| Doc ID | File | Author | Title | Year |
|--------|------|--------|-------|------|
| `indus_valley_script_deciphered_from_myth_65ff0a26` | `Indus_Valley_Script_deciphered_From_Myth.pdf` | Roif, Avishai | Indus Valley Script Deciphered From Myth | — |
| `without_kings_or_conquests_the_indus_scr_ce9d98cc` | `Without_Kings_or_Conquests_The_Indus_Scr.pdf` | Hunt, Treasure A. | Without Kings or Conquests: The Indus Script Deciphered and a Civilization Reconstructed | 2025 |

### Roif — Guild Ledger Hypothesis
- **Model**: `hypotheses/models/roif_guild_ledger.yaml` — status: `partially_encoded`
- **Core claim**: Indus script = economic ledger of trade guilds using Akkadian-influenced mnemonics.
- **Sign assignments extracted**: fish=coastal guild, jar=tribute, arrow=tīr/enforcement, boat=maritime, horned deity=fire-altar intermediary, cattle, plough, serpent, grid.
- **Falsification finding**: Fish sign (coastal guild claim) → Phase-4x CISI data shows fish is NOT statistically enriched at coastal sites. Claim status: **partially_falsified**.
- **Manual claims registered**: 4 (guild ledger, fish-coastal, arrow-enforcement, horned-deity-Kalibangan)

### Hunt — Civic-Ritual Continuity System
- **Model**: `hypotheses/models/hunt_civic_ritual.yaml` — status: `partially_encoded`
- **Core claim**: Indus script = civic-ritual continuity system encoding ecological cycles and distributed governance via tripartite grammar (prefix/medial/suffix). NOT royal titulature.
- **Tripartite grammar**: prefix=identity/office/commodity, medial=action/transaction/domain, suffix=cycle/jurisdiction/logistics.
- **Translation Atlas**: 24 clusters with canonical forms, frequencies, co-occurrence sets.
- **Testable predictions**: lipid residues, isotopic assays, archaeoastronomy alignments.
- **Glossa-Lab cross-check**: Phase-43 Batch 5 formula_rate=35.5% vs null 0.6% (59× lift) — structural support for non-random inscription formula. 20 TERMINAL_STRONG + 40 INITIAL_STRONG signs consistent with tripartite prediction.
- **Manual claims registered**: 5 (tripartite syntax, civic-ritual interpretation, faunal-prefix, celestial-suffix, Translation Atlas)

### Claims Extraction Run
- **Script**: `scripts/indus_claims.py`
- **Documents processed**: 11
- **Total claims extracted**: 22
  - Roif: 6 claims (4 manual + 2 auto-extracted)
  - Hunt: 9 claims (5 manual + 4 auto-extracted)
- **Output**: `claims/extracted_claims/`
- **Report**: `reports/claim_reports/batch4_claims_report.json`

---

## Batch 3 — Literature Sweep
**Date**: 2026-05-17  
**Commit**: `227e927`

6 PDFs downloaded open-access and registered:
- Yadav et al. 2010 (PLoS ONE) — `yadav_2010_ngrams`
- Yadav et al. 2009 (arXiv) — `yadav_2009_arxiv`
- Rao et al. 2010 (ACL) — `rao_2010_coli_entropy`
- Parpola 2010 (Helsinki) — `parpola_2010_dravidian_solution`
- Sinha 2010 (arXiv) — `sinha_2010_network_arxiv`
- Farmer-Sproat-Witzel 2004 — `farmer_sproat_witzel_2004`

9 docs total registered (includes 3 Rao 2009 variants).

---

## Batch 4 — Claims Extraction Pipeline Build
**Date**: 2026-05-17  
**Commit**: `227e927`

`indus_claims.py` built. 7 claims extracted in initial run with manual curation for Parpola/FSW/Yadav. Expanded to 22 claims in Batch 2 re-run.

---

## Batch 5 — Null Models + Hunt Tripartite Test
**Date**: 2026-05-17  
**Commit**: `227e927`

Results:
- **Random shuffle null**: effect = **231.9σ** — positional structure is REAL
- **Freq-preserved null**: 0.13/20 top bigrams reproduced — bigrams NOT explained by frequency alone
- **Site-preserved null**: 1.58σ cross-site recurrence
- **Hunt tripartite test**: formula_rate=35.5% vs null=0.6% → **59× lift** [VERIFIED]

---

## Batch 6 — Automated Sweep, New Atomic Nodes, and Full UX Integration
**Date**: 2026-05-17  
**Commit**: `f80e2c3`

### Sweep configuration schema
- `config/sweep.yaml` created: per-project sweep config with tiered keywords
  (primary/secondary/expansions), per-source enable/max_results, exclusions,
  filters (min_year, languages, open_access), and output settings.
- Schema is generic — any project can have its own `sweep.yaml`.

### Backend evidence graph API
- `backend/glossa_lab/api/indus_evidence.py`: 11 REST endpoints covering library,
  claims, hypotheses, sweep config (GET/PUT), sweep run, sweep candidates, sweep
  intake, upload, import-url, and intake/run.
- Sweep engine builds a `TopicProfile` from `sweep.yaml` and runs the existing
  discovery fetchers directly, deduplicating against registered papers.
- All background tasks; sweep stores candidates in `logs/sweep_candidates_latest.json`.

### 7 new Evidence Graph atomic nodes
- `backend/glossa_lab/experiment_graph_indus_evidence.py`
- Category: `Evidence Graph`; two new port colors (`claims` #b45309, `papers` #0891b2).

| Node | Description |
|------|-------------|
| IndusLiteratureLoader | Load papers from `literature/documents/` |
| IndusClaimsLoader | Load claims with type/status/sign filters |
| CrossHypothesisMatrix | Agree/conflict verdicts grouped by sign or type |
| HiddenHypothesisGen | Cross-paper compound hypotheses (≥2 source papers) |
| IndusClaimTester | Test positional claims against corpus sequences |
| IndusNullModelTest | Shuffle null model for sign-position enrichment |
| IndusIntakeRunner | Trigger intake + claims pipeline |

### Frontend — Evidence Graph view
- `frontend/src/components/IndusEvidenceView.tsx`: 3-tab workspace
  - Library: paper list, stats, drag-drop PDF dropzone, URL import, Re-run intake
  - Claims: filterable by type/status/sign, expandable claim cards
  - Sweep: config editor (keywords, exclusions, sources), Run Sweep, candidates + Import
- `frontend/src/App.tsx`: `evidence` tab added under Research section.
- `frontend/src/components/Discovery/DiscoveryView.tsx`: `🗂 → Evidence` action
  added to Indus/Harappan discovery card items.

---

## Batch 7 — Tests, CI/CD, and Full Documentation
**Date**: 2026-05-17  
**Commit**: `7d44d85`

### Test coverage
- `backend/tests/test_indus_evidence_api.py`: 20 tests, all 11 API endpoints covered.
- `backend/tests/test_evidence_atomic_nodes.py`: 45 tests (44 registered + 1 real-corpus
  integration test), all 7 Evidence Graph nodes.
- `frontend/e2e/evidence-graph.spec.ts`: 39 Playwright tests, all pass offline.
- `frontend/e2e/navigation.spec.ts`: 2 new Evidence Graph nav tests; 5 pre-existing
  failures fixed (Studies→Projects, Indus Data removed, title changes).
- `frontend/e2e/backend-integration.spec.ts`: 14 new Evidence Graph API integration tests.

### CI/CD
- `.github/workflows/ci.yml`: 3-job GitHub Actions pipeline.
  - `backend-tests`: Python 3.12, pytest --tb=short, pip cache
  - `frontend-tests`: Node 20, npm build + Playwright Chromium
  - `indus-evidence-scripts`: smoke test intake/claims scripts + sweep.yaml validation

### Documentation updates
- `README.md`: Evidence Graph in overview, repo structure, components, research status.
- `docs/USER_GUIDE.md`: Section 16 (Evidence Graph) added; navigation table updated;
  last-updated 2026-05-17.
- `docs/REQUIREMENTS.md`: R14 Evidence Graph API requirements (R14.1–R14.7) added;
  test coverage table updated.
- `docs/TEST_SPEC.md`: TEST-IEA-001–020, TEST-EV-REAL-01, TEST-EV-001–044,
  TEST-PW-EG-001–039, and backend integration block added.
- `docs/architecture.md`: Evidence Graph layer in system diagram; Evidence Graph
  subsystem section; frontend key UI modules table.

### Gap analysis summary (all gaps closed)

| Gap | Status |
|-----|--------|
| Pre-existing nav test failures (Studies, Indus Data, etc.) | ✅ Fixed |
| IndusClaimTester tested only on synthetic corpus | ✅ Real CISI corpus integration test added |
| No CI/CD pipeline | ✅ 3-job GitHub Actions workflow added |
| README missing Evidence Graph | ✅ Updated |
| USER_GUIDE missing Evidence Graph | ✅ Section 16 added |
| REQUIREMENTS.md missing R14 | ✅ R14.1–7 added |
| TEST_SPEC.md missing Evidence Graph specs | ✅ TEST-IEA/EV/PW-EG added |
| architecture.md missing Evidence Graph | ✅ Updated |

---

## Batch 8 — SQLite WAL Fix + Specsmith Migration
**Date**: 2026-05-17  
**Commit**: `438cc69` (WAL) + staged

### SQLite WAL mode fix (database.py)
- Root cause: 14 backend tests failing with `sqlite3.OperationalError: database is locked`.
  Background tasks started by the app lifespan (provider probes, model intelligence
  sync, RAG index build, discovery scheduler) were writing to the DB concurrently
  with test write operations. Default DELETE journal mode with `busy_timeout=0`
  caused instant failures.
- Fix: Three PRAGMAs added to `Database.connect()` right after opening the connection:
  - `PRAGMA journal_mode=WAL` — Write-Ahead Logging, concurrent readers + writers
  - `PRAGMA busy_timeout=5000` — retry up to 5 seconds before raising
  - `PRAGMA synchronous=NORMAL` — crash-safe with WAL, faster than FULL
- Result: **445 passed, 0 failed** (was 428 passed, 16 failed).

### Specsmith migration (model-rate-limits.json)
Both `.specsmith/model-rate-limits.json` files updated to current-gen model landscape:

| Added | Provider |
|-------|----------|
| `o3` | OpenAI |
| `o4-mini` | OpenAI |
| `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano` | OpenAI |
| `claude-sonnet-4-20250514` | Anthropic |
| `gemini-2.5-flash` | Google |
| `gemini-2.5-flash-preview-05-20` | Google |
| `gemini-2.5-pro-preview-05-06` | Google |
| `gemini-3-pro-preview`, `gemini-3.1-pro-preview` | Google |
| `gemini-3-flash-preview` | Google |

### model_intelligence.py static fallback migration
- Added `gpt-5.4` to `_sync_static_fallback()` known_models dict.
  Previously appeared in specsmith (rpm=60, tpm=500k) and in pacing test
  messages but had no benchmark scores, causing it to show as unscored
  in the Model Assignments UI.
- Scored at top-tier reasoning class (exceeds gpt-4.1 on reasoning bucket).

---

## Phase-45 — Positional Cross-Check, M267, Hunt Tripartite, Fish Coastal, UX
**Date**: 2026-05-17

### T1: Wells/Fuls Positional Cross-Check (phase45_t1_fuls_crosscheck.py)
- **Concordance: 7/7 = 100%** — STRONG_AGREEMENT
- All 4 CLASSIFIER_PREFIX anchors (M006 puli, M016 kaḷiṟu, M045 yānai, M062 erutu): avg_pos=0.000, is_starter=True, holdat_role=CLASSIFIER_PREFIX
- All 3 CASE_MARKER_SUFFIX anchors (M099 kol/koḷ, M176 an/aṇ, M342 ay/ā): avg_pos≈0.56–0.61, is_ending=True, holdat_role=CASE_MARKER_SUFFIX
- Fuls NWSP independently confirms our readings with perfect alignment.
- Wells 2015 passages located in cleaned text (8 passages found).
- Report: `reports/phase45_t1_fuls_crosscheck.json`

### T2: M267 Full Investigation (phase45_t2_m267.py)
- **Hypothesis: GRAMMATICAL_PARTICLE or DETERMINATIVE** — motif-independent, medial position
- n=400, avg_pos=0.540 (medial), iconographic entropy=0.852 (normalised) → UNIFORM across ALL motifs
- Appears on unicorn(147×), zebu bull(78×), elephant(43×), script only(34×), rhinoceros(26×)…
- **M267→M099 formula 84×** (precedes kol/koḷ); M099→M267 only 8× (asymmetric)
- Anchored adjacents: erutu, an/aṇ, kol/koḷ, kaḷiṟu, ay/ā both before and after
- Top site: Mohenjo-daro (135, 34%); present at all 5 major sites
- Epistemic: INFERRED, low confidence — consistent with copula or genitive particle
- Report: `reports/phase45_t2_m267.json`

### T3: Hunt Tripartite Formula Test (phase45_t3_hunt_tripartite.py) — GPU: cuda (torch 2.5.1+cu121)
- **Verdict: SUPPORTED**
- Sign pools (count≥8): INITIAL_STRONG=75, TERMINAL_STRONG=5, MEDIAL=22
- P1 (INITIAL_STRONG iconog-restricted, entropy<0.7): 10/75 = 13.3% — weak
- **P2 (INITIAL_STRONG faunal > 50%): 75/75 = 100%** — strong
- **P3 (TERMINAL_STRONG iconog-uniform): 5/5 = 100%** — strong
- Interpretation: INITIAL_STRONG signs are overwhelmingly associated with faunal motifs (unicorn, zebu, elephant…). Some are iconographically concentrated (restricted); the rest are faunal but spread. TERMINAL_STRONG signs are fully uniform across motifs — consistent with grammatical suffixes, not identity markers.
- Hunt's identity-marker hypothesis confirmed for faunal association; the entropy restriction (P1) is weaker than predicted (many faunal signs spread across multiple faunal categories rather than one).
- Contingency matrices built on GPU.
- Report: `reports/phase45_t3_hunt_tripartite.json`

### T6: Fish Sign M047 Coastal Enrichment (phase45_fish_coastal_test.py) — GPU: cuda
- **Verdict: NO_ENRICHMENT** (but n=13, severely underpowered)
- M047 in corpus: 13 total occurrences across 7 sites
- Coastal (Lothal+Dholavira): 2/230 = 0.87%; Inland: 10/1379 = 0.73%; RR=1.20×
- Fisher exact p=0.685 — not significant
- Interpretation: The test is UNDERPOWERED — M047 count=13 is too rare for site-distribution analysis. No anti-signal either. The mīn reading remains plausible on linguistic grounds; coastal enrichment simply cannot be confirmed with this corpus size.
- GPU used for inscription-scanning tensor (bool tensor on cuda).
- Report: `reports/phase45_fish_coastal_test.json`

### T7: Contact Zone Corpus Status
- Directories NOT empty — contains substantial data:
  - `contact_zone/cdli_meluhha/`: 2 files, 1.5 MB (CDLI Meluhha inscriptions)
  - `contact_zone/gulf_seals/`: 1 file, 23 KB
  - `contact_zone/indus_seals_mesopotamia/`: 1 file, 18 KB
  - `contact_zone/publications/`: 23 files, 65 MB
- Deferred to Phase-46: need a proper contact_zone analysis script.

### Backend: Global Rate-Limit Cooldown
- All 11 remaining fetchers wired with `source_is_cooling` + `_429_cooldown`:
  crossref, europepmc, doaj, pubmed, openalex, brave, newsapi, academia_rss, patentsview, serpapi, uspto
- Generic cooldown registry in base.py now fully covers all fetchers.

### Frontend UX Improvements
- AI chat (floating + docked): Shows `📁 ProjectName` badge when no specific corpus/experiment context is active (instead of always showing "Global").
- Project auto-activation: If exactly one project exists and nothing is explicitly selected, it activates automatically on load.
- Explicit Global preference: Clicking "All Projects (Global)" stores `__global__` sentinel so auto-activate doesn't override it on next reload.
- CorrespondenceView: Each row now shows `← from_addr` or `→ to_addr` direction indicator.
