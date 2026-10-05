# LEDGER

Append-only record of all meaningful work in Glossa Lab.

---

## Archived (35 entries)

*Archived on 2026-06-07*

- ## Archived (25 entries, 2026-05-29) — —
- ## [2026-05-26] Entry — Competing LM Convergence Test + Dravidianist Outreach Sent — —
- ## [2026-05-26] Entry — Phase 295: Infrastructure Sprint + Bulk Mine 5000 — —
- ## [2026-05-29] Entry — Research Loop Phases 5-7: Experiment Builder + Insight Selection + DB Persistence — —
- ## [2026-05-29] Entry — Governance Migration + Phase Advancement Sprint — —
- ## [2026-05-29] Entry — Full Phase Advancement + SA Experiment Diagnosis + Research Loop Verification — —
- ## [2026-05-29] Entry — Session Close — —
- ## [2026-05-29] Entry — UI Feature Sprint: Pause/Resume, Auto-Queue, Arrange Fix, ETA Fix — —

## [2026-06-07] Entry — Data Integrity Fixes + Kalyanaraman Integration + Phase Advancement + Dynamic Phases

Objective:
  Fix foundation check data integrity bugs, integrate Kalyanaraman rebus
  papers as second-source validation, fix phase advancement system, add
  dynamic phase generation.

What was done:

  1. ANCHOR TOTAL BUG FIX:
     - fa["total"] was set to H+M count only by 3 writer paths (promotion,
       auto-fix, cleanup script) but foundation check expected len(anchors)
     - Fixed in: api/research_loop.py, api/foundation_check.py, scripts/_fix_anchors.py
     - Repaired INDUS_FINAL_ANCHORS.json total: 260 → 286
     - Foundation check: 40 pass, 0 fail, 8 warn

  2. STALE DASHBOARD FIX:
     - "Next steps" showed stale fix_foundation proposal after FC was fixed
     - ResearchLoopPanel now filters out fix_foundation proposals when
       live FC shows 0 failures

  3. KALYANARAMAN REBUS INTEGRATION:
     - Built rebus lexicon from 52 PDFs: 24 rebus pairs, 200 Dravidian terms,
       144 sign references, 31 craft vocabulary items
     - Created KalyanCrossValidation atomic node + graph experiment
     - First run: 105 overlapping signs, 113 new candidates, complementarity=1.0
     - Auto-queued on every anchor promotion (alongside SA experiments)
     - Data file: backend/glossa_lab/data/kalyanaraman_rebus.json

  4. CGSA EXPERIMENT FIX:
     - ClusterMapper node referenced undefined `_log` instead of `logger`
     - One-line fix in experiment_graph.py

  5. SA MULTI-LANGUAGE BUILD FIX:
     - "nw semitic" split into ["nw", "semitic"] by whitespace regex
     - Added pre-normalization for multi-word language names before splitting

  6. PHASE ADVANCEMENT FIX:
     - Phase 5 was terminal — "Complete Phase" cleared state but coverage
       kept returning Phase 5. No Phase 6 existed.
     - Added completed_through_phase tracking in phase_state.json
     - Added Phase 6 (Peer Review) and Phase 7 (Publication)
     - _get_phase_for_coverage now skips completed phases
     - Verified: Phase 5 → 6 transition works via API

  7. DYNAMIC PHASE GENERATOR:
     - New module: pipelines/phase_generator.py
     - Auto-generates phase goals from available experiments + project state
     - Persists to outputs/phase_goals.json (editable)
     - API: GET /phase/goals, POST /phase/goals, POST /phase/generate
     - config.py loads dynamic goals when available, falls back to defaults

  8. STAGING REVIEW:
     - 14 staged candidates rejected (all from blocker_sign_context,
       recommended=false, statistically_sufficient=false, SA delta 4.9-5.0%)

Files changed:
  backend/glossa_lab/api/research_loop.py (promotion total fix + Kalyanaraman auto-queue)
  backend/glossa_lab/api/foundation_check.py (auto-fix total calculation)
  backend/glossa_lab/api/experiments.py (multi-word language normalization)
  backend/glossa_lab/api/phase.py (goals CRUD + generate endpoints)
  backend/glossa_lab/config.py (Phase 6+7, dynamic goal loading)
  backend/glossa_lab/experiment_graph.py (ClusterMapper _log fix, Kalyanaraman node registration)
  backend/glossa_lab/experiment_graph_kalyanaraman.py (NEW — cross-validation node)
  backend/glossa_lab/pipelines/phase_advancer.py (completed_through_phase tracking)
  backend/glossa_lab/pipelines/phase_generator.py (NEW — dynamic phase generation)
  backend/glossa_lab/data/kalyanaraman_rebus.json (NEW — rebus lexicon)
  backend/glossa_lab/experiments/graphs/indus_kalyanaraman_crossval.json (NEW)
  backend/scripts/_fix_anchors.py (total = len(anchors))
  backend/scripts/_build_kalyanaraman_lexicon.py (NEW — lexicon builder)
  backend/reports/INDUS_FINAL_ANCHORS.json (total repaired)
  frontend/src/components/ResearchLoopPanel.tsx (stale proposal filter)

Checks run:
  - Foundation check: 40 pass, 0 fail, 8 warn
  - Kalyanaraman cross-validation: COMPLEMENTARY (144 signs, 113 new candidates)
  - Phase advancement: Phase 5 → 6 verified via API
  - npm run build: clean, 0 TS errors
  - Backend health: healthy
  - specsmith audit: 29 pass, 2 issues (ledger TODOs + scaffold type)

Open TODOs:
  - [ ] Contact Suresh Kolichala via Academia.edu with review packet
  - [ ] Wait for Dravidianist responses (Renganathan, Murugaiyan, Kobayashi)
  - [ ] Check SSRN status (submission ID 6827038)

Next step:
  Run Phase 6 (Peer Review) experiments from the Phase Advancer UI.


## 2026-06-07T14:07 — specsmith migration: 0.11.7 → 0.13.0
- **Author**: specsmith
- **Type**: migration
- **Status**: complete
- **Chain hash**: `8fdaa4a6a232e910...`

## [2026-10-05] Entry — Spec-kit + AEE migration (Stage 1): specsmith retired

Objective:
  Replace specsmith as the active governance/SDD tooling with spec-kit +
  the AEE and evaluator extensions, following the adoption pattern already
  used for the Axiovex website and Rockeagle projects. Recorded as
  specs/001-glossa-lab-baseline/ (as-built baseline).

What was done:
  1. `specify init` (spec-kit 1.0.10, copilot integration, sh scripts)
     into the existing repo; extensions `aee` and `evaluator` installed
     from the local spec-kit-aee / spec-kit-evaluator clones with --dev
     and vendored as real files under .specify/extensions/ (nested .git
     directories and dev venvs stripped — no gitlinks).
  2. Constitution ratified at .specify/memory/constitution.md, codifying
     the project's existing governance: CITATIONS.md provenance,
     append-only ledger, foundation-check gate, falsifiable-claims
     discipline, public/private correspondence boundary (H24), AI
     disclosure, no secrets in tracked files.
  3. specsmith removed as ACTIVE tooling: .agents/skills/specsmith{,-audit,-save}/,
     scaffold.yml, and the tracked runtime state
     backend/.specsmith/model-rate-limits.json deleted. Historical
     mentions in this ledger, CHANGELOG.md, and docs/ledger-archive.md
     are append-only history and were NOT rewritten.
  4. Runtime rate-limit persistence moved from .specsmith/rate_limits.json
     to .glossa-state/rate_limits.json at repo root (same walk-up logic)
     in backend/glossa_lab/discovery/fetchers/base.py and
     backend/glossa_lab/model_intelligence.py; .gitignore now ignores
     .glossa-state/ instead of .specsmith/.
  5. AGENTS.md updated: governance configuration lives in .specify/ +
     specs/; session workflow is git + spec-kit flow. LIFECYCLE.md phase
     tracking moved off scaffold.yml.

AI disclosure: this migration was executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per constitution §VI.

### [2026-10-05] Entry — Spec-kit + AEE migration (Stage 2: AEE library core)

**Type:** architecture / epistemic infrastructure
**Summary:** The core tool now runs claim scoring on the underlying
epistemic engineering library, `applied-epistemic-engineering` (the
`aee` package, >=1.0.4,<2, added to `backend/pyproject.toml`).

- New `backend/glossa_lab/aee_core.py`: adapter mapping Glossa's
  extracted-claims JSON (`glossa-indus/claims/extracted_claims/*.json`)
  onto AEE `Claim`/`Evidence`/`ClaimGraph`, scored by AEE's
  `ScoringEngine`. `falsification_condition` maps natively onto
  `Claim.falsification_tests`; Glossa `claim_status` maps onto
  `ClaimStatus` (Glossa `untested` → AEE DRAFT, original preserved in
  `Claim.metadata`); fields AEE has no concept for (claim-type taxonomy,
  `testability`, quote fragments, sign lists, `confidence_in_source`)
  are preserved via `Claim.metadata` / `Claim.source_ref`. Glossa's
  assessed status enters scoring through attached evidence strength —
  the `ScoringEngine` takes no status input — documented in the module
  docstring.
- API (additive only, existing shapes unchanged):
  `GET /api/v1/indus-evidence/claims/aee-scores` returns the full AEE
  assessment; `GET /claims?aee=true` attaches a per-claim `aee_score`.
  Verified live: 31 claims, mean propagated score 0.485.
- Tests: `backend/tests/test_aee_core.py` — 18 passed (mapping,
  falsification preservation, evidence attachment, scoring sanity,
  round-trip on the real Parpola 2010 fixture and the full claims dir);
  `test_indus_evidence_api.py` still 25 passed.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

### [2026-10-05] Entry — Spec-kit + AEE migration (Stage 3: GDELT ngrams)

**Type:** discovery infrastructure / external guidance adoption
**Summary:** Implemented GDELT's published migration guidance
(Kalev Leetaru, GDELT Project; public posts only — no correspondence
reproduced, per constitution §V):

- New default GDELT source `backend/glossa_lab/discovery/fetchers/gdelt_ngrams.py`
  (source id `gdelt_ngrams`): consumes the temporary Web Ngrams dataset
  (per-minute `<ts>.ngrams.txt.gz` + `<ts>.toc.json.gz`), requests the
  file from ~5 minutes ago, walks back over 15-minute heartbeat marks
  (bounded, 24 marks ≈ 6 h), matches topic keywords against quadgrams
  (with tri/bi/unigram reduction; >4-word keywords via constituent
  windows), applies topic exclusions, cross-references DOCIDs through
  the TOC into discovery `RawItem`s, and persists a watermark in
  `.glossa-state/gdelt_ngrams.json`.
- The DOC-API fetcher (`gdelt.py`) is retained but opt-in only
  (explicit source request or topic override), docstring-noted as
  paused per GDELT's request during the Spanner migration.
- Tests: `backend/tests/test_gdelt_ngrams.py` — 11 passed, synthetic
  fixtures, no network. A live smoke test against the real dataset is
  reported in the migration PR.
- `specs/002-gdelt-ngrams-and-frontier-methods/` documents the switch
  plus two recorded-but-not-implemented learnings: a future fully-cited
  daily briefing over the discovery corpus ("Today's Trends" pattern),
  and manuscript-method design notes for future seal/tablet vision
  work (physical metadata up front; discrete focused passes).

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

### [2026-10-05] Entry — Spec-kit + AEE migration (Stage 4: verification)

**Type:** verification / release bookkeeping
**Summary:**

- Synced with origin/main after the Dependabot merges (#50–#53:
  checkout/setup-node/setup-python v7, Pillow bump in
  `tray/requirements.txt`) — clean merge, no conflicts; the AEE
  dependency addition and the Dependabot changes coexist.
- Tracked-file sweep for the retired tooling: remaining mentions are
  only the constitution/AGENTS/LIFECYCLE retirement notes, this ledger,
  the CHANGELOG, `docs/ledger-archive.md`, and the migration spec's own
  task text — i.e. historical records and removal documentation only.
- Tests (venv with backend deps + dev extras + AEE 1.0.4): full backend
  suite 533 passed, 9 skipped, 0 failed (508 + 9 skipped across 45 test
  files, plus `test_indus_evidence_api.py` 25 passed run separately).
  New tests: `test_aee_core.py` 18, `test_gdelt_ngrams.py` 11. Ruff
  clean on all changed Python files.
- Foundation check: `backend/scripts/foundation_check.py` cannot run
  off the Windows dev box (it hardcodes a `C:\Users\trist\...` repo
  path — pre-existing, untouched by this migration); it fails at its
  first corpus read here. The live foundation-check API module is
  covered by the passing suite.
- Live GDELT ngrams smoke test: endpoint and naming verified against
  the dataset's documented example pair (2026-06-30 20:16 UTC —
  1,063,647 quadgrams, 1,977 TOC entries; end-to-end matching on real
  data works, e.g. the blog's own "disease" example search → 16 items;
  "Indus script" matched 0 items in that single minute). However, NO
  current files were found: every probed mark for 2026-10-05 (25-mark
  walk-back) and spot marks over the preceding weeks returned 404, so
  the dataset appears not to be publishing new files at test time.
  The fetcher handles this correctly (bounded walk, no items, no
  watermark advance) and will pick files up when publication resumes.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.
