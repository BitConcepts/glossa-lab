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

---

## 2026-10-05 — MCP update (Stage A of feat/mcp-gaps-indus-continuation)

- **Route-drift audit:** enumerated the live FastAPI route table from the
  running app (311 method/path routes via the OpenAPI schema) and checked
  every route called by the 27 existing MCP tools. Result: **no functional
  drift** — every method/path resolves. Sole mismatch is cosmetic: the
  experiment-graphs item routes name their path parameter `{exp_id}`
  (MCP interpolates a concrete ID, so calls are unaffected).
- **New MCP tools (+6 → 33 total)** in `backend/glossa_mcp/server.py`,
  following the existing `_get`/`_fmt`/`_err` conventions:
  `list_indus_claims` (filters + opt-in `aee=true` AEE score attachment),
  `get_indus_claim` (resolved via the claims list endpoint — the evidence
  API has no per-claim route), `get_indus_claim_aee_scores`
  (GET /api/v1/indus-evidence/claims/aee-scores), `list_indus_library`,
  `list_indus_hypotheses`, and `get_foundation_status`
  (GET /api/v1/foundation/status — last-check state the existing
  `run_foundation_check` tool did not expose).
- **GDELT consistency:** `trigger_discovery_fetch` docstring now states
  GDELT is served by the `gdelt_ngrams` fetcher by default and the DOC
  API fetcher is paused/opt-in, matching post-migration discovery
  defaults. Tool inventory docs updated (README.md, backend/README.md,
  AGENTS.md: 27 → 33 tools).
- **Requirements gap found & fixed here:** the `mcp` package was declared
  in no dependency manifest — the MCP server could not be imported from a
  clean install of the declared deps. Added an `mcp` optional-dependency
  group (`mcp>=1,<2`, `httpx`) to `backend/pyproject.toml`.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

---

## 2026-10-05 — Requirements & test gaps (Stage B of feat/mcp-gaps-indus-continuation)

- **Traceability:** specs/003-mcp-and-test-gaps/ (spec/plan/tasks) carries
  the requirement → implementation → test matrix over specs 001–002
  (R1–R12). Two genuine gaps found and fixed; spec 002 T006/T007 are
  future-scoped by their own spec and were left alone.
- **Gap 1 — MCP had zero tests:** added `backend/tests/test_glossa_mcp.py`
  (24 tests): httpx MockTransport happy-path request formation/response
  formatting for every tool family, error-path helper coverage, a
  33-tool inventory assertion, and a drift guard that extracts every
  route called in the MCP source and asserts it exists in the live
  FastAPI route table.
- **Gap 2 — foundation_check.py unrunnable off Windows:** the hardcoded
  `C:\Users\trist\...` repo path is replaced by `resolve_repo_root()`
  (`GLOSSA_REPO_ROOT` env override, else script-location-derived —
  identical target on the Windows dev box). Added
  `backend/tests/test_foundation_check_script.py` (5 tests).
- **Foundation check real run (this environment):** with the Holdat
  corpus fetched from its cited public source (CITATIONS.md A.13) into
  the gitignored `corpora/` layout, the script now runs end-to-end:
  **39 checks passed, 0 failed, 9 warnings** (verdict READY WITH
  CAVEATS; warnings are the script's pre-existing documented caveats:
  site coverage, P/M numbering crosswalk, superseded TB corpus,
  phase52 result absent, torch absent). Report regenerated at
  `reports/foundation_check_report.json`.
- **Full backend suite:** 562 passed, 9 skipped, 0 failed (baseline
  533 + 24 MCP + 5 foundation-script tests). Ruff clean on changed files.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

---

## 2026-10-05 — Indus program continuation (Stage C of feat/mcp-gaps-indus-continuation)

- **Phase-104 (claims evaluation):** all 21 untested extracted claims
  evaluated against in-repo evidence under pre-stated rules
  (`backend/scripts/phase104_claims_evaluation.py`, graph node
  `IndusClaimsEval`). 5 claims moved to `contradicted` — duplicate
  extractions of the already-adjudicated Farmer/Sproat/Witzel
  proposition, verdict + cited evidence carried over with cross-reference.
  16 stay untested, each with a recorded reason (site-typology data,
  sign-class set, or atlas definitions absent from the repo; unstated
  sign numbering; or extraction fragments with no falsification
  condition). Detail: `glossa-indus/LEDGER.md`,
  `glossa-indus/reports/phase104_claims_evaluation.json`.
- **Phase-105 (name-sign adjudication):** the unrun draft
  `phase105_name_signs.py` (pre-written readings/promotions) was replaced
  with a Phase-101-style positional/formula adjudication over the Holdat
  corpus. Verdicts: M375 CORROBORATED; M362 and M398 INCONCLUSIVE
  (3 tokens each — underpowered); **M024 CHALLENGED** as a medial
  name-component (100% INITIAL profile; Holdat roles: CLASSIFIER_PREFIX)
  and flagged for future adjudication. No anchor promoted, demoted, or
  modified. Report: `reports/phase105_name_signs.json`.
- **Phase-102 follow-up (Mistral OCR): BLOCKED** — no Mistral key
  configured, `pypdfium2` absent, and `im77intro.pdf` not in this
  checkout. Recorded, not fabricated.
- **Foundation check (H21):** re-run after Stage C — 39 passed,
  0 failed, 9 warnings.
- PRED-2026-001..003 remain PENDING (external ICIT data); untouched.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

### [2026-10-05] Entry — Spec 003 follow-up fix: mcp in dev extra (CI)

**Type:** bugfix (test infrastructure)
**Summary:**

- PR #55's backend CI job failed at collection: `tests/test_glossa_mcp.py`
  raised `ModuleNotFoundError: No module named 'mcp'` because CI installs
  only `pip install -e ".[dev]"` and Stage A had declared `mcp` solely in
  its own optional-dependency group. Local runs passed because the venv
  had the mcp extra installed — a local/CI environment divergence.
- Fix: added `mcp>=1,<2` to the `dev` extra in `backend/pyproject.toml`
  (with an explanatory comment). The standalone `mcp` extra remains for
  runtime installs of the server itself. No other files changed.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

### [2026-10-05] Entry — MCP robustness: ignore ambient proxy env + README count

**Type:** bugfix (MCP server) / docs
**Summary:**

- First live use of the MCP server from the Muse VM failed on every
  tool call: `InvalidURL — Invalid port: ':1]'`. Root cause: the MCP
  server's httpx client trusted ambient proxy env; this VM's NO_PROXY
  list contains bracketed IPv6 entries that corrupt httpx URL parsing.
  The server only ever talks to the local backend, so `_get()` now
  passes `trust_env=False`. Covered by a new test
  (`test_http_client_ignores_ambient_proxy_env`; MCP suite now 25).
- README's key-files table still said "27 tools" for the MCP server;
  corrected to 33 (the count everywhere else was already right).
- A `glossa-lab-mcp` skill (SKILL.md + stdio client wrapper) now lives
  in Tristen's Muse workspace skills, wrapping all 33 tools; the
  backend + MCP were started locally and exercised live (status,
  foundation status, AEE claim scores, discovery stats, hypotheses).

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

### [2026-10-05] Entry — MCP proxy fix completed: all client constructions

**Type:** bugfix (MCP server) — completes the PR #56 fix
**Summary:**

- PR #56 fixed only `_get()`. Five direct `httpx.Client(...)`
  constructions remained and still trusted ambient proxy env, so
  `run_experiment`, `run_foundation_check`, the research-loop fire
  path, `get_dashboard_highlights`, and `get_report` would still have
  failed with the InvalidURL proxy error on affected machines.
- Refactor: single `_client(timeout)` helper (trust_env=False);
  `_get()` and all five call sites now go through it. New AST
  regression test asserts every `httpx.Client` call in server.py
  passes trust_env=False, so the pattern cannot silently return.
  MCP suite: 26 tests, all passing.
- Verified live with the RAW environment (no client-side env
  sanitization): get_status, get_dashboard_highlights, list_reports,
  get_report (JSON report), and run_foundation_check all succeed
  through the MCP against the running backend.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

### [2026-10-05] Entry — Foundation status tracker records research-API runs

**Type:** bugfix (backend API wiring)
**Summary:**

- The foundation status tracker (`api/foundation.py`) only recorded
  runs from its own `_run_check()` (POST /foundation/check + the
  15-minute auto-check). The research API check
  (GET /api/v1/research/foundation-check — the endpoint the MCP
  `run_foundation_check` tool calls) recorded nothing, so
  GET /foundation/status stayed null after MCP-triggered runs.
- Fix: `foundation.record_result(result, source=...)` now exists as
  the shared recording path; the research handler records its summary
  (n_pass→n_ok, overall_status→verdict) with source="research_api"
  after every run (best-effort — a recording failure cannot break the
  check response). The status payload gains a `source` field;
  tracker-path runs are tagged source="foundation_api".
- Tests: `tests/test_foundation_status_wiring.py` (2) pins the
  mapping + verdict recording via the shared TestClient.
- Live verification (MCP): run_foundation_check → 17 pass / 0 fail /
  0 warn (the API-native check set), then get_foundation_status
  showed last_checked_at set, verdict PASS, n_ok 17,
  source "research_api". Previously it showed all nulls.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## [2026-10-05] Entry — Spec 004: Indus Executable Package (WS1–WS4)

Branch `feat/indus-executable-package` (PR opened, not merged).

- **WS1 / Phase-106**: Phase-52 syllabic SA re-run through the registered
  `IndusConstrainedSA` experiment-graph node (unmodified script, CPU,
  420.8 s). Artifacts restored: `reports/phase52_syllabic_sa.json`,
  `reports/phase52_full_decipherment_table.json`. z = 17.642 (reproduces
  the historical z = 16.01 claim's magnitude; its artifact was lost);
  per-sign agreement with confirmed anchors 113/275 = 41.09% (historical
  claim said 55% — reported as observed). Foundation CHECK NEW-F passes;
  the Phase-52 warning is gone.
- **WS2**: M↔P crosswalk v2.1, 179 → 184 entries, evidence-gated (each
  addition carries an `evidence` field); 220 unadmitted pairs held in a
  new candidates file (216 identity-inference-only, 4 conflicted);
  stats regenerated from entries (113/184 independently attested).
  Phase-104 RULE-NUM addressability reported (3 of 5 via the canonical
  registry's Wells column; no re-adjudication).
- **WS3**: `INDUS_FINAL_ANCHORS.json` bookkeeping regenerated from the
  287 entries (HIGH 166 / MEDIUM 109 / LOW 8 / CANDIDATE 4; H+M = 275);
  anchors mapping provably unchanged (canonical sha256
  fa16861c3b896266508cab805bc69b21a620db46b536f4cb8e5f4fed04f294f7
  before/after); canonical count definitions recorded in metadata,
  incl. "161 anchors" = Phase-170 grammar-retest H+M snapshot.
- **WS4**: all 78 queued discovery items triaged via the discovery API
  (saved 33 / reviewed 10 / dismissed 35; "new" queue empty). Mining
  unavailable — no LLM provider configured (endpoint refuses); recorded.
- Verification: backend suite 564 passed / 9 skipped / 0 failed;
  foundation check 40 passed / 0 failed / 8 warnings. Detail entries:
  `glossa-indus/LEDGER.md` (Phase-106 + WS2–WS4 sections).

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## [2026-10-05] Entry — Phase-107 / Spec 005: Phase-52 v2 — the Strengthened SA Does Not Generalise; Claims A–F Resolved as Pre-Registered

Branch `feat/phase52-v2` (PR opened, not merged — owner reviews
scientific results). Full per-step entries: `glossa-indus/LEDGER.md`
(Phase-107, Steps 1, 1-audit, 2, 3, 4×2, 5). The package executed the
pre-registered spec 005 protocol end-to-end; a mid-package runtime
restart killed the first coordinator and the package was completed by
a continuation session from committed checkpoints (Step 2's
phono/harmony folds resumed from checkpoint, not re-run).

- **Step 1 (validation):** 5-fold held-out anchor CV of the current
  Phase-52 objective: held-out agreement **0.000 ± 0.000** (0/115
  evaluable), secondary (never-pinned) 3/700 = 0.43%, fold z mean
  18.81. Blind controls: Sanskrit z 60.87 / held-out 0.000; scrambled
  z 16.48 / 0.000; Ge'ez z 6.33 / undefined. **Claims A and B
  falsified.** The historical 41.09% decomposes as pinned 113/116 vs
  never-pinned 0/159 (Addendum A).
- **Step 1 sanity audit (continuation):** all 8 checks pass — no
  leakage path; reachability denominators reconcile (unreachable
  gold 'ya' among pinnable; H003 has a gold but zero corpus
  occurrences, 115/116 evaluable); fold 0 at production config
  (5×10×30k) reproduces 0/24, z 19.232. The zero is not a harness
  artifact. (Audit run 1's spurious B1 FAIL was an audit-side
  denominator error; fixed, re-run, recorded.)
- **Step 2 (ablation):** phonotactic / vowel-harmony / positional
  terms each give held-out 0.000 (z 19.01 / 20.92 / 19.91) — all
  DROPPED by the keep rule; **Claim C falsified per term**; best
  objective remains LM-only.
- **Step 3 (delta + scale):** delta scorer numerically sound (mean
  best-score diff 0.297%) but **Claim D FAILS** on consensus
  agreement (31.2% < 95%): the objective's optimum is a plateau of
  near-equivalent mappings. Scaled run (10×10×100K): z 18.452;
  stability selection — **0 SA-supported, 0 probable, 275 unstable**.
- **Step 4 (corpus):** hunt record in
  `reports/phase107_acquisition_log.json` + CITATIONS §J. Ingested:
  ICIT/Lipi export via field-cady MIT mirror (5,679 insc; layer
  1,007 insc / 2,238 tok after dedupe). Not obtainable: RMRL
  Mahadevan concordance (no bulk export; contact route closed under
  H14), official ICIT, CISI/CISID, Wells standalone, Dixit dataset,
  TN graffiti DB (comparative-only by design), Zenodo lexicons.
  Not found: CDLI, OSF/Figshare, Dilmun/Gulf downloadable, Harappa.com
  datasets. A layer-build dedupe defect (flat-list indexing) was
  found in audit, fixed, rebuilt pre-commit (1 inscription affected;
  pooling re-dedupes independently). Pooled corpus 2,684 insc /
  9,264 tok: headline held-out still **0.000** (z ≈ 11.99). **Claim
  E: pooling does not help** (exact tie at zero; not "falsified"
  under the strict rule).
- **Step 5 (metrology):** **C1 FAIL, C2 NOT APPLICABLE, C3 FAIL**
  (block contiguity 0.3846 < 0.80). The pre-registered M086–M092
  stroke family is only 2/7 present in Holdat (M087/M089, both HIGH
  *syllabic* anchors in this programme); an unpadded-ID script defect
  was caught pre-commit and recorded.
- **Bottom line:** every strengthening lever in the plan was applied
  and measured; none moves held-out agreement off zero. The Phase-52
  SA objective fits (z ≈ 18–19) but does not determine per-sign
  values — the decipherment programme's anchor values are not
  corroborated by its own SA under held-out testing, and the
  Phase-107 decipherment table marks all 275 unpinned signs
  "unstable". No anchor readings or confidences were changed.
- **Verification:** backend suite **576 passed / 9 skipped / 0
  failed** (baseline 564/9; +10 new `test_sa_validation.py` tests,
  +2 net suite growth); foundation check **40 passed / 0 failed / 8
  warnings** (baseline-identical, H21 satisfied); ruff clean on all
  branch-changed Python files.
- **Out-of-scope note:** `backend/scripts/phase107_tb_name_check.py`
  and `outputs/phase107_tb_name_check.json` are LEGACY artifacts of
  an earlier era's Phase-107 labelling (spec 005 phase-numbering
  note); they are not part of spec 005's tasks and were left
  untouched.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

Phase-107 PR: https://github.com/BitConcepts/glossa-lab/pull/60 (opened 2026-10-05, NOT merged — owner review gate).

## [2026-10-06] Entry — Phase-108 / Spec 006: Anchor Provenance Audit — 210 of 287 Anchors Are Fully SA-Independent; the Rest Is Mapped

- **Question:** Phase-107 falsified simulated annealing as evidence for
  sign values but left all 287 anchors unchanged. What does each
  anchor's value and confidence actually rest on? Spec 006
  pre-registered the taxonomy and SA-dependence rules before any
  classification (commit 9d17a8d2). Full record:
  `glossa-indus/LEDGER.md` Phase-108 sections; register:
  `reports/phase108_provenance_register.json`; summary:
  `reports/phase108_provenance_summary.md`.
- **Headline:** GRAMMAR 163, DEDR 33, SA_DERIVED 24, SA_CONFIRMED_ONLY
  20, LITERATURE 17, MIXED 15, ICONOGRAPHIC 12, CROSSWALK_CORPUS 3,
  UNTRACEABLE 0. SA-dependent total 77; **SA-independent 210/287
  (73.2%)** — strict, including-untraceable, and
  excluding-untraceable-from-denominator all coincide because no trail
  proved untraceable. All 44 SA_DERIVED + SA_CONFIRMED_ONLY anchors are
  HIGH tier.
- **Dominant findings:** (1) 116 anchors (40%) are the research loop's
  staging cohort — readings from fixed heuristic tables ('min'
  bulk-assigned to ~40 signs), promoted via an endpoint named
  verify-sa that performs no SA test; caught by the Step-2 spot audit
  after pass 1 mislabeled them DEDR. (2) The Phase-116/216
  recalibration gates promoted on SA consistency as a sufficient
  disjunct — M293 'ta' (232 tokens) reached HIGH on the SA-only path.
  (3) Phase-293 promoted 12 DEDR-injected signs whose own records said
  "SA confirmation pending".
- **Recomputation (SA-independent H+M, 198/275):** coverage 77.96%
  (full 96.47%); phonotactic violations 0 on both sets; site
  invariance 100% on both sets (65/65 strict, 90/90 full) — the
  programme's strongest grammar claim survives; the README's 59%
  Parpola figure is a Phase-170-era quantity whose 44-sign source set
  is 45.5% SA-lineage and which does not reproduce on current sets.
- **Impact map:** 77 circular/component chains catalogued with
  citations; 0/31 extracted claims cite any sign ID; all 37 SA-citing
  foundation-check lines assessed post-107 (retire Phase-52/57/67
  evidential framings; Phase-56/47/58/69 stand). Recommendations
  authored for the owner, NOT executed (summary Step-5 section).
- **Verification:** backend suite **586 passed / 9 skipped / 0
  failed** (baseline 576/9 + 10 new tests); foundation check **40/0/8**
  (baseline-identical); ruff clean; anchors file sha256 identical to
  main — audit-only, no anchor changed.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

Phase-108 PR: https://github.com/BitConcepts/glossa-lab/pull/61 (opened 2026-10-06, NOT merged — owner review gate).

## [2026-10-06] Entry — Phase-109 / Spec 007: Phase-108 Follow-Through — Staging Cohort Re-Reviewed, SA-Lineage Flagged, Headlines Re-Based

- **Step 1 (staging cohort, 116):** (a) KEEP 1 (M222, Parpola
  crosswalk support); (b) RESTORE 112 — 109 `kur`/LOW Phase-111
  allograph priors + M042 `vaN`, M046 `kaL`, M108 `kaL` at HIGH
  (Phase-89 DEDR); (c) DEMOTE 3 (H003, M231, M252). Two hand-check
  corrections pre-registered in a spec addendum before apply
  (exact reading identity; SA-origin priors not restorable).
- **Step 2:** 44 SA-lineage HIGH anchors flagged
  `pending_non_sa_validation` + `provenance_class`; no value/tier
  changed.
- **Step 3:** M293 `ta`, M362 `aṇi`, M398 `kuṟi` each HIGH →
  MEDIUM on dossier evidence (Phase-101's own outcome; Phase-105
  INCONCLUSIVE never superseded).
- **Step 4:** `/staging/verify-sa` renamed `/staging/verify-archive`
  (deprecated alias retained); `/staging/promote` gated on a
  recorded non-SA evidence reference; SA auto-queue removed;
  governance **H26** (no SA-sufficient promotion gates);
  foundation-check SA framings retired as text only.
- **Step 5 (re-based headlines):** strict SA-independent set
  **94 H+M (90 HIGH + 4 MEDIUM), coverage 73.68%** (5,159/7,002),
  0 phonotactic violations, site invariance 65/65; full table
  287 (166/5/112/4), full H+M 171 at 92.19%. README re-based;
  anchors bookkeeping regenerated; preprint v5 addendum drafted
  in-repo only (NOT submitted; v4 untouched).
- **Change register:** 164 records; completeness verified
  mechanically — 162 anchor entries differ from main, all covered.
- **Verification:** backend suite **609 passed / 9 skipped / 0
  failed** (baseline 586/9 + 23 new tests); foundation check
  **40/0/8** after every step; ruff clean.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

Phase-109 PR: https://github.com/BitConcepts/glossa-lab/pull/62 (opened 2026-10-06, NOT merged — owner review gate for all scientific changes).

## [2026-10-06] Entry — Phase-110: M222/'kur' adjudication + OSF registry link (spec 008)

Branch `feat/phase110-m222-adjudication` (PR opened, not merged).

- **Adjudication of the Phase-109 flagged tension:** the 109
  `kur`/LOW restorations derive from Phase-111 allograph
  resolution, whose bases cite M222 read as `kur` — while M222
  stands at `min`/MEDIUM on crosswalk support. Dossier
  (`reports/phase110_m222_dossier.json`): Phase-111 copied the
  donor sign's reading verbatim; its recorded run matched 220/220
  rare signs to M222 at L1=0.000 because every rare-sign profile
  in the corpus is (0,0,1) — the match carried zero discriminating
  information (Phase-132 had already called the values "parking
  placeholders"). Verdict: contradiction REAL; the values are
  pure premise inheritance from a superseded premise.
- **Disposition (pre-registered rule + dated spec addendum):**
  Cohort A (109) annotated `premise_superseded` and demoted
  LOW → CANDIDATE; the 4 CANDIDATE Phase-111 `kur` entries
  (M157/M256/M307/M400) annotated with the same status (their
  Phase-252 legs support 'en'/'taṇ', not `kur` — Cohort C empty);
  M222 annotated, its `min`/MEDIUM NOT re-tried. Tiers now
  166/5/3/113; H+M unchanged (171). Change register: 115 records,
  diff-verified complete (114 entries).
- **OSF link:** README "Provenance & source registry" pointer +
  CITATIONS.md header note → https://osf.io/ybd65/ (literature
  zbh86, corpora dfrhz, outputs vwa7s); repo remains canonical.
- **Verification:** foundation check 40/0/8; backend suite
  609 passed / 9 skipped / 0 failed; ruff clean; H23 graph nodes
  `IndusPhase110M222Dossier` / `IndusPhase110M222Apply` registered
  before running. Detail: `glossa-indus/LEDGER.md` Phase-110 entry.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## [2026-10-06] Entry — Phase-111 / Spec 009: Blind Language-Affiliation Study — Pre-Registration Frozen

- **Design source:** deep-research report
  `~/workspace/research_notes/indus-blind-language-affiliation-study-d-20261007-0101/report.md`
  (sourced design: ranked feature set, matched-size panel, gate and
  verdict thresholds, blinding protocol, licensing survey).
  Owner approved execution of the full path 2026-10-06
  ("do all this now").
- **Pre-registration:** spec 009
  (`specs/009-phase111-blind-affiliation/`) is committed in its own
  commit BEFORE any pipeline output exists; the git order is the
  registration proof. Frozen in it: the 28-feature vector (design
  report ranks 2–9 as one joint vector; rank 10 dictionary-reading
  excluded — SA falsified by Phase-107), the panel (Linear B, Vedic +
  Classical Sanskrit, Old Tamil, Sumerian Ur III, Akkadian, Ge'ez,
  Turkish + Malay/Indonesian decoys; khipu + proto-cuneiform as
  attested non-linguistic; synthetics S1–S4; Indus as 3 anonymized
  replicates under Mahadevan and Wells sign lists), resampling
  (N = 11,000, 100 draws, target length distribution = Holdat
  empirical, mean 4.193), the VALIDATION GATE (linguistic balanced
  accuracy ≥ 0.85 with lower 95% CI > 0.70 AND family balanced
  accuracy ≥ 0.70 with permutation p < 0.001; failure = STOP,
  INCONCLUSIVE, no Indus classification), SUPPORT thresholds
  (posterior ≥ 0.90, BF ≥ 10 vs runner-up AND vs both synthetic
  generators, same winner both sign lists in ≥ 90% of draws),
  REFUTATION rule (BF < 3 or TOST ±0.05 = NO FAMILY
  DISCRIMINATION), BH q = 0.05, custodian/analyst separation.
- **Registered gaps at freeze time:** Elamite (no verified open
  corpus — not scraped around); attested SCA heraldry (license
  unverified — synthetic heraldic generator substitutes).
- **Licensing:** owner directive — publish nothing requiring
  permission we lack; raw downloads live only in the gitignored
  sources dir; only feature vectors, statistics, code, and logs
  are committed.
- **Status at this entry:** spec frozen; no panel built, no gate
  run, no result exists. Outcome entries follow as separate
  appends.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## [2026-10-06] Entry — Phase-111 / Spec 009: Outcome — Gate Passed Perfectly; Run Invalid at Control Validity (INVALID RUN)

- **Execution:** pipeline as committed at 92cad2ab (custodian /
  features / analyst / orchestrator + H23 graph nodes; 17 unit
  tests passing pre-run). Panel built from the frozen roster +
  Addendum A substitutions/gaps (UD treebanks for the K8/K9
  decoys; K6 Akkadian and N2 proto-cuneiform logged gaps, never
  scraped around; acquisition record:
  reports/phase111_acquisition_log.json). As built: 9 known
  corpora, 3 anonymized Indus replicates (R1 7,002 tokens /
  390 signs; R2 14,213 / 713; R3 pooled 21,215 / 1,103),
  4 synthetic controls. No corpus fell under the 5,000-token
  power rule.
- **Gate (§7): PASSED on both tests.** G1 linguistic balanced
  accuracy 1.000 (requirement ≥ 0.85), bootstrap 95% CI lower
  bound 1.000 (> 0.70), p = 0.00050. G2 family balanced
  accuracy 1.000 (≥ 0.70), permutation p = 0.000999 (< 0.001,
  1,000 permutations); per-family recall 1.000 for all seven
  families. BH-adjusted T1/T2 p = 0.0020 (q = 0.05).
- **Control validity (§8): FAILED — the run's binding outcome.**
  S3 (heraldic generator) and S4 (administrative generator)
  classified non-linguistic in 1.00 of draws, but S1 (within-text
  permutation of R1) and S2 (i.i.d. Zipf matched to R1 unigrams)
  classified non-linguistic in **0.00** of draws against the
  ≥ 0.95 requirement: both Indus-derived nulls sat in family
  space in every draw. Recorded mechanism: the gate's attested
  non-linguistic class rested on khipu alone (N2 gap), a
  vocabulary-10 outlier, so the validated boundary never had to
  reject structureless draws carrying a linguistic unigram
  profile. Per §8 this invalidates the run, not the hypotheses.
- **Verdict (V6 vocabulary, verbatim):** `INVALID RUN —
  CONTROL VALIDITY FAILED`. No §9 verdict rule fired; T3/T4
  exceedance values in the results file are audit-only and carry
  no verdict weight. No Indus affiliation claim — for or against
  any family, or for linguistic status itself — is made by this
  phase. Unblinding event: 2026-10-07T03:52:39.601141+00:00,
  code HEAD 92cad2ab (digests in the results file). No re-runs,
  no tuning, per §6/§11. Reports:
  reports/phase111_blind_affiliation_results.json +
  reports/phase111_blind_affiliation_summary.md.
- **Lesson recorded for any successor spec:** a gate whose
  non-linguistic class has one attested, extreme-outlier member
  cannot validate the boundary the verdict path needs; control
  validity caught it, which is the protocol working. A future
  panel needs a comparably difficult attested non-linguistic
  member or null classes inside the gate — by new spec, never
  by patching this run.
- **No anchors touched; no prior result altered.**

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## [2026-10-07] Entry — Phase-112 / Spec 010: Blind Language-Affiliation Study, Order-Carrying Features — Pre-Registration Frozen

- **Why this study exists:** Phase-111's gate passed perfectly,
  but its run was invalidated at control validity — S1
  (within-text permutation of R1) and S2 (i.i.d. unigram null)
  classified linguistic in 100% of draws, showing the 28-feature
  vector's power was carried by unigram statistics. Owner
  authorized the successor study 2026-10-07 ("yes do the
  successor now").
- **Pre-registration:** spec 010
  (`specs/010-phase112-blind-affiliation/`) committed in its own
  commit AFTER the design-stage tooling commits (73ebbfb1,
  f0e5a6c5) and BEFORE any Phase-112 panel build, gate
  evaluation, or Indus statistic exists; the git order is the
  registration proof. **The one design change:** the
  classification feature set contains ONLY permutation-sensitive
  (order-carrying) features, admitted by a pre-registered audit
  on the nine known corpora (median |Cohen's d| ≥ 0.8 under
  within-text permutation, same sign ≥ 8/9 corpora,
  non-degenerate ≥ 5/9; mechanical toy test as a first screen).
  Audit outcome: **16 of 23 candidates admitted** (entropy /
  conditional-entropy / Markov-perplexity / repetition /
  bigram-type / adjacency features; median |d| up to 60.0);
  dropped: the positional-concentration family
  (`init80_frac`, `term80_frac`, `term_init_ratio`, `hend_first`,
  `hend_last`), `rep_adj_2`, `fl_mi`. Full record:
  `reports/phase112_feature_audit.json`.
- **Inherited unchanged from spec 009:** panel (as assembled,
  incl. Addendum A substitutions and the registered gaps:
  Elamite, K6 Akkadian, N2 proto-cuneiform, attested SCA
  heraldry), resampling (N = 11,000; 100 draws; sensitivity
  5k/19.6k), unit rules, S1–S4 generators, LDA classifier,
  custodian/analyst blinding, gate thresholds (§7), verdict
  rules (§9, V6 vocabulary), BH q = 0.05. **New:** S5, a
  positional-bigram template generator (relative-position bins,
  β = 1.0 interpolation), added as a fifth control under §8
  (≥ 95% of draws non-linguistic-collapsed for EACH of S1–S5),
  with NO disclosed training instance and NO class in the final
  model — the undisclosed probe Phase-111's design lacked.
- **Staging note:** the Phase-111 downloads were lost with their
  worktree; the identical panel was re-obtained from the same
  openly licensed origins into the gitignored
  `sources/phase112/` and **verified loader-equivalent**: every
  corpus's loader statistics and chunk counts reproduce the
  committed Phase-111 build log exactly (all 12 loadable
  corpora MATCH). Record:
  `reports/phase112_acquisition_log.json`.
- **Status at this entry:** spec frozen; no panel built, no gate
  run, no result exists. Outcome entries follow as separate
  appends. No anchors touched.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## [2026-10-07] Entry — Phase-112 / Spec 010: Outcome — Gate Passed; INVALID RUN at Control Validity, at the New S5 Trap (INVALID RUN)

- **Execution:** pipeline as committed at 7e2626cf (custodian /
  features / analyst / orchestrator + H23 graph nodes, verified in
  ATOMIC_NODES pre-run; 18 unit tests passing). Panel rebuilt from
  the re-staged, loader-equivalence-verified sources (all 12
  loadable corpora MATCH the Phase-111 build log exactly). Two
  aborted build attempts preceded the completed run — a worker
  stall under extreme host contention and a VM reboot mid-build;
  neither produced any statistic (panel file is written only at
  build completion). The completed run used BLAS thread-count env
  pinning as a stall mitigation (environment only; no code, seed,
  or threshold changed). Full disclosure in the summary.
- **Gate (§7): PASSED on both tests.** G1 linguistic balanced
  accuracy 1.000 (CI lower bound 1.000, p = 0.00050); G2 family
  balanced accuracy 1.000 (permutation p = 0.000999); per-family
  recall 1.000 for all seven families. Order-carrying features
  alone separate the known corpora perfectly at Indus size.
- **Control validity (§8): FAILED at S5 — the run's binding
  outcome.** Shares classified non-linguistic (requirement
  ≥ 0.95 each): S1 permutation **1.00**, S2 i.i.d. Zipf **1.00**,
  S3 heraldic **1.00**, S4 administrative **1.00** — the traps
  that invalidated Phase-111 (S1/S2 at 0.00 there) are now
  rejected in every draw; the one design change did its work.
  But **S5 (positional-bigram template generator) scored 0.00**:
  a grammar-free process matching R1's lengths, its unigram
  profile (TV distance 0.0419), and its relative-position bigram
  statistics by construction sat in family space in 100% of
  draws. §8 is conjunctive; the run is invalid.
- **Verdict (V6 vocabulary, verbatim):** `INVALID RUN —
  CONTROL VALIDITY FAILED`. No §9 verdict rule fired; T3/T4
  exceedance values and the sensitivity descriptives in the
  results file are audit-only and carry no verdict weight. No
  Indus affiliation claim — for or against any family, or for
  linguistic status itself — is made by this phase. Unblinding
  event: 2026-10-07T16:02:08.334428+00:00, code HEAD 7e2626cf
  (digests in the results file). No re-runs, no tuning, per
  §6/§11. Reports:
  reports/phase112_blind_affiliation_results.json +
  reports/phase112_blind_affiliation_summary.md.
- **Lesson recorded for any successor spec:** order statistics
  up to relative-position bigrams are reproducible by a
  positional template process with no grammar; discrimination
  claims must be validated against positional-template nulls,
  not only against order destruction. Any successor needs its
  own pre-registered audit and traps for whatever longer-range
  structure it proposes to measure — by new spec, never by
  patching this run.
- **Suite / foundation:** backend suite 643 passed / 11 skipped
  / 0 failed (the +1 skip vs the Phase-111 baseline is
  Phase-111's own panel test skipping — its runtime state lived
  in the removed Phase-111 worktree); foundation check
  40 passed / 0 failed / 8 warnings.
- **No anchors touched; no prior result altered.**

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## [2026-10-07] Entry — Phase-113 / Spec 011: Non-SA Validation Battery for the 44 SA-Lineage Anchors — Pre-Registration Frozen

- **Spec:** `specs/011-phase113-nonsa44-validation/` (spec/plan/tasks),
  committed alone at `81049c98` before any battery code ran against
  any anchor. Owner authorization: Tristen Pierson, 2026-10-07
  (roadmap item 2).
- **Question:** do the 44 anchors Phase-109 flagged
  `pending_non_sa_validation` (24 SA_DERIVED + 20 SA_CONFIRMED_ONLY;
  43 HIGH + M293 MEDIUM) survive a validation battery that never
  touches an SA output (H26)?
- **Frozen battery:** T1 cross-corpus consistency (ICIT converted
  layer vs Holdat; attestation floor 3 tokens; modal-class agreement;
  profile TV ≤ 0.40); T2 positional-grammar fit vs the strict
  SA-independent core (profile TV ≤ 0.35 to the class centroid, modal
  share ≥ 0.45; reading–slot phonotactics incl. Phase-58 initial
  validity and a frozen syllable canon); T3 compositional
  co-occurrence (≥ 3 strict partners at co-occurrence ≥ 2; ≥ 4
  fully-core-readable contexts; ≥ 0.75 canon-legal compositions).
- **Frozen decision rule:** VALIDATED_NON_SA iff all three PASS
  (tier unchanged; this phase validates or demotes, never promotes);
  DEMOTE to CANDIDATE on any FAIL; UNRESOLVED otherwise (stays
  flagged).
- **Frozen calibration gates (run before the 44):** STRICT94
  leave-one-out VALIDATED ≥ 57/94; KUR113 (Phase-110
  premise-superseded cohort) VALIDATED ≤ 5/113. A failed gate
  rejects the battery: no re-tuning under this spec, FLAGGED44
  never run, anchors file untouched.
- **Machinery (H23/H15):** `phase113_battery.py` (pure counting;
  no SA artifact read; syllabic LM deliberately unused),
  `phase113_run.py`, runner `phase113_nonsa_battery.py`, graph
  node `IndusPhase113NonSaValidation` registered and asserted in
  ATOMIC_NODES before any run; 30 unit tests (canon, profiles,
  decision-rule truth table, toy end-to-end controls, set
  recomputation, registration).
## [2026-10-07] Entry — Phase-113 / Spec 012: Blind Language-Affiliation Study, Adversarial Protocol — Pre-Registration Frozen

- **Why this study exists:** Phase-111 fell to unigram mimicry
  (S1/S2), Phase-112 — with only order-carrying features — fell
  to S5, a grammar-free positional-bigram template (control
  share 0.00). The recorded lesson, twice confirmed: a fixed
  trap is beaten by the next subtler mimic. Owner authorized
  the adversarial successor 2026-10-07 (roadmap item 4).
- **Pre-registration:** spec 012
  (`specs/012-phase113-blind-affiliation/`) committed in its own
  commit AFTER the design-stage tooling commits (110c1fe9,
  dc57566b) and BEFORE any Phase-113 panel build, gate
  evaluation, adversarial round, or Indus statistic exists; the
  git order is the registration proof. **The design change:**
  fixed traps are replaced by an adversarial protocol — a
  feature ladder frozen in advance (L1 = spec-010's 16; L2 =
  L1 + admitted family B; L3 = L2 + admitted family C), three
  rounds (one per ladder step), each with the round classifier
  frozen while a deterministic, seeded, budgeted optimizer
  (200 evaluations/round) searches a parametric generator
  family G(θ) — positional/global bigram+trigram mixtures with
  burst and copy components — for corpora that match R1 on all
  previous rounds' feature families and maximize family
  assignment. A round holds only if the frozen classifier
  rejects the optimized generator in ≥ 95% of draws; a defeat
  ends the run INVALID at that round with the defeating
  generator reported in full. Final control validity is
  conjunctive over S1–S5 and A1–A3 under C_3; the §10 verdict
  fires only if every round holds.
- **Feature admission (design stage, known corpora only):**
  every new candidate had to pass BOTH the spec-010
  permutation-sensitivity audit (median |d| ≥ 0.8, same sign
  ≥ 8/9, non-degenerate ≥ 5/9) AND a new power audit at
  N = 7,002 (median pairwise between-class |Cohen's d| ≥ 0.5).
  Outcome: family B admitted 8 of 14 (`blockH5`, `blockH6`,
  `mi_lag2`, `mi_lag3`, `rep_adj_4`, `adj_clustering_lag2`,
  `restore_acc_tri`, `bigram_type_ratio_lag2`); family C
  admitted 6 of 6. The power audit admitted all 20 candidates;
  every exclusion was made by the permutation audit (six
  family-B candidates with inconsistent permutation-response
  sign). Ladder power at N = 7,002: family balanced accuracy
  1.000 at all three ladder steps. **The pre-registered
  INDETERMINATE AT THIS CORPUS SIZE outcome does NOT fire**
  (criteria: < 3 admitted new features — 14 admitted; or
  full-ladder family BA at 7,002 < 0.70 — it is 1.000), so the
  adversarial rounds proceed. Full record:
  `reports/phase113_feature_audit.json`.
- **Inherited unchanged from specs 009/010:** panel (as
  assembled, with its registered gaps), resampling
  (N = 11,000; 100 draws; sensitivity 5k/19.6k), unit rules,
  S1–S5 controls and their generator-training instances, LDA
  classifier, custodian/analyst blinding, gate thresholds,
  verdict rules and V6 vocabulary, BH q = 0.05, licensing
  discipline (publish nothing requiring permission we lack).
- **Staging note:** the Phase-112 panel staging was lost with
  its worktree; the identical panel was re-obtained from the
  same openly licensed origins into the gitignored
  `sources/phase113/` and **verified loader-equivalent**: all
  eleven loader-backed corpora reproduce the committed
  Phase-111 build log exactly (11/11 MATCH; Holdat and ICIT
  transferred with SHA-256 equality). Record:
  `reports/phase113_acquisition_log.json`.
- **Status at this entry:** spec frozen; no panel built, no
  gate run, no round run, no result exists. Outcome entries
  follow as separate appends. No anchors touched.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## [2026-10-07] Entry — Phase-113 / Spec 011: Outcome — Battery Rejected at the Calibration Gates (BATTERY REJECTED)

- **Calibration, executed exactly as frozen.** STRICT94
  (positive control, leave-one-out): VALIDATED **3** / DEMOTE 45 /
  UNRESOLVED 46 — the ≥ 57 gate **FAILED**. KUR113 (negative
  control): VALIDATED **0** / DEMOTE 16 / UNRESOLVED 97 — the
  ≤ 5 gate passed. Battery **rejected**; FLAGGED44 was never run;
  `INDUS_FINAL_ANCHORS.json` is byte-untouched by this phase; no
  anchor changed tier or status. Full record:
  `reports/phase113_nonsa44_results.json` +
  `reports/phase113_nonsa44_summary.md`.
- **Diagnosis (descriptive, from the calibration records; no
  re-tuning performed):** T2 is sound (profile fit passes 91/94;
  its 13 failures are all the class-initial-inventory sub-check).
  T3's legality component never fires (0/89 strict signs with
  contexts below the 0.75 legal bar); its binding constraint is
  partner support under leave-one-out. **T1 is the failing
  component and it fails on data:** 45/94 strict signs have zero
  tokens in the ICIT converted layer and 16 more sit below the
  attestation floor (61/94 NOT_ATTESTED); of the 33 attested,
  22 fail modal-class/profile agreement. The converted layer
  (1,007 inscriptions / 2,238 tokens of 5,679 source
  inscriptions, 69.3% token-map coverage) is too sparse and
  conversion-noisy to carry a conjunctive cross-corpus gate —
  the spec §8 caveat, now measured. The kur gate confirms the
  battery does not validate known-bad readings, but a battery
  that cannot validate the known-good core either is not a
  validation instrument.
- **Lesson recorded for any successor spec:** a cross-corpus
  test is only as strong as the converted layer beneath it;
  either rebuild T1 on a fuller ICIT extraction (the restricted
  4,410-inscription OCR corpus exists locally but is in ICIT
  numbering with probabilistic ordering) or scale attestation
  floors to measured layer coverage — by new spec, never by
  patching this run. The 44 anchors remain
  `pending_non_sa_validation`; their status is unchanged and
  the question stays open.
- **Suite / foundation:** recorded in the PR body (full backend
  suite; foundation check per H21 — anchors untouched, reports
  added).
## [2026-10-07] Entry — Phase-113 / Spec 012: Outcome — Gate Passed at Round 1; INVALID RUN at Round-1 Adversarial Control A1 (INVALID RUN)

- **Verdict (verbatim, frozen spec-012 §10 V6 vocabulary):
  INVALID RUN — CONTROL VALIDITY FAILED**, fired at round 1
  (spec §8.2). No affiliation verdict — for or against any
  family, or for linguistic status itself — is produced by this
  phase, and none may be quoted from it.
- **Design recap:** the adversarial successor to 111/112. A
  frozen feature ladder (L1 = spec-010's 16; L2 = L1 + family B;
  L3 = L2 + family C) with three rounds, one per ladder step;
  each round freezes its classifier, then a deterministic
  seeded optimizer (200 evaluations) searches the generator
  family G(θ) (positional/global bigram+trigram mixtures with
  burst and copy) for corpora matching R1 on all previous
  rounds' families and maximizing family assignment. A round
  holds only if the frozen classifier rejects the optimized
  corpus in ≥ 95% of 100 draws.
- **Power analysis (§4.4):** dual audit on the nine known
  corpora — family B admitted 8/14, family C 6/6 (the power
  audit at N = 7,002 admitted all 20 candidates; every
  exclusion was the permutation audit's). Ladder family
  balanced accuracy at N = 7,002: 1.000 at all three steps.
  **INDETERMINATE AT THIS CORPUS SIZE did not fire**; the
  rounds proceeded.
- **Gate (round 1, L1):** PASSED perfectly — G1 BA 1.000, CI
  lower bound 1.000, bootstrap p = 0.00050; G2 BA 1.000,
  permutation p = 0.000999; all 7 family recalls 1.000. Third
  consecutive perfect gate in this study line; the failure is
  again at control validity, not validation.
- **Round 1 (the defeat):** 183/200 optimizer candidates were
  feasible (unigram TV ≤ 0.05); the objective was bimodal —
  median 0.0, but 82 candidates scored ≥ 0.99 mean family
  posterior mass. Candidate 0 (the forced θ_S5 anchor, S5's
  exact construction) scored 0.99999995. Winner (eval 53):
  a trigram-dominated grammar-free mixture — w_G3 0.534,
  w_P3 0.280, w_G2 0.174, w_P1 0.011, w_P2 0.001; β_P2 3.0,
  β_P3 0.3, β_G2 1.0, β_G3 0.3; p_burst 0.048, p_copy 0.189;
  evaluation-corpus unigram TV to R1 0.0394. A_1 (13,202
  texts / 55,002 tokens, TV 0.0387): **control share under
  C_1 = 0.00** (0/100 draws non-linguistic-collapsed). The
  frozen §8.2 stop rule fired: rounds 2–3 not run, §8.4 final
  recheck not reached, T3–T5 not run.
- **Defeating generator:** reported in full in
  `reports/phase113_blind_affiliation_summary.md` per spec
  §8.3. Reading: Phase-112's S5 was one point of the defeating
  region; the region is broad — L1's order statistics
  (≤ relative-position bigrams) are producible by many
  bounded-order Markov/template mixtures matching the unigram
  profile. Whether the L2/L3 features resist is NOT measured
  by this run (the protocol forbids proceeding past a failed
  round); it is a question for a successor spec, never a
  patch of this run.
- **Blinding:** the key was never opened for classification
  (unblinding is null in the results file); the classify stage
  was invoked once as an integrity check and refused, as
  designed. Code HEAD for the run: 24cb33a0. Deviations from
  the frozen spec: none. One VM reboot occurred during the
  design stage (before any run; nothing lost but /tmp
  scratch); the run itself was uninterrupted and checkpointed.
- **Suite / foundation:** backend suite 667 passed / 12
  skipped / 0 failed (the +1 skip vs the 643/11 baseline is
  Phase-112's state-dependent panel test — the same mechanism
  recorded in Phase-112's accounting); foundation check
  40 passed / 0 failed / 8 warnings. Reports:
  reports/phase113_blind_affiliation_results.json +
  reports/phase113_blind_affiliation_summary.md.
- **No anchors touched; no prior result altered.**

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

---

## Phase-115 — Non-SA Validation Battery v2: Pre-Registration + Outcome (spec 014)

Successor to Phase-113 (spec 011, battery rejected at calibration),
authorized by Tristen Pierson 2026-10-07 ("continue fully") along
the successor paths Phase-113 recorded. Spec 014 frozen alone in
`fddd4dbf` before any battery-v2 code ran against any anchor.

- **Layer rebuilt (spec §2):** diagnosis decomposed the Phase-107
  loss — a leading-zero key mismatch (CSV `002` vs registry `2`)
  cost 4,014 tokens; the all-or-nothing inscription rule cost most
  of the rest. The v2 builder (key normalization; sentinel
  positions for placeholders/unmapped codes; partial inscriptions
  retained; Holdat wildcard + intra-layer exact dedupe) produces
  **4,531 inscriptions / 13,492 mapped tokens at 91.554%
  token-map coverage** (v1: 1,007 / 2,238 / 69.3%), byte-identical
  across rebuilds (sha256 f837a15a…). Corpus data stays gitignored;
  statistics only published.
- **Battery v2:** T1 rebuilt on the v2 layer with attestation
  floors scaled to each sign's measured opportunity
  (O = r·n_H, r = 1.926878; bands frozen in spec §4; FAIL requires
  ≥ 3 tokens). T2/T3, calibration gates, and the decision rule are
  spec 011 unchanged (machinery reused, not reimplemented).
- **Calibration outcome — BATTERY REJECTED (second frozen
  rejection).** STRICT94 (leave-one-out): VALIDATED **1** / DEMOTE
  57 / UNRESOLVED 36 — gate (≥ 57) FAILED. KUR113: VALIDATED **0**
  / DEMOTE 23 / UNRESOLVED 90 — gate (≤ 5) passed. FLAGGED44 was
  never run; `INDUS_FINAL_ANCHORS.json` is untouched (zero diff);
  all 44 remain `pending_non_sa_validation`; tier counts and the
  94-sign strict core / 73.68% coverage are unchanged.
- **Diagnosis (post-hoc, descriptive):** the failure mode inverted
  — v1 could not attest the core (61/94 NOT_ATTESTED); v2 attests
  it (51/94 judged) and finds systematic cross-corpus
  disagreement: 43 T1 FAILs, 40 on modal-class disagreement
  (median TV 0.79; largest cell Holdat-INITIAL → ICIT-MEDIAL, 18;
  direction-swap pairs only 8); 25/94 strict signs have zero
  tokens in the ICIT corpus at all. T2/T3 tallies identical to
  Phase-113. Recorded conclusion: a conjunctive cross-corpus gate
  on this pair of compilations is not a validation instrument;
  any further successor must first pre-register a
  corpus-harmonization study of *why* the profiles disagree —
  new spec + owner direction required.
- **Suite / foundation:** 697 passed / 11 skipped / 0 failed
  (673 baseline + 24 new); foundation 40 / 0 / 8; ruff clean.
  (Full-suite side-effect churn in test-generated outputs was
  reverted; not part of this phase.)
## [2026-10-07] Entry — Phase-116 / Spec 015: Corpus-Harmonization Study — Pre-Registration Frozen

- **Spec:** `specs/015-phase116-corpus-harmonization` (spec/plan/tasks),
  committed alone (`0b626308`) before any harmonization statistic
  existed. Owner authorization: Tristen Pierson, 2026-10-07 ("Launch
  the corpus-harmonization study"). Phase-114 (spec 012) is reserved
  and untouched.
- **Question (Phase-115's recorded successor):** Phase-115's T1 v2
  judged 51 strict signs and failed 43 — 40 on modal-position-class
  disagreement, median TV 0.789474. Why do Holdat's and the ICIT
  converted layer's positional profiles disagree? Five frozen
  hypothesis families with numeric verdict thresholds:
  H-COMPOSITION (paired matched-text core test: restrict both layers
  to the same texts via a frozen wildcard matcher), H-SEGMENTATION
  (S1 sentinel-strip re-judgment; S2 artifact-unit re-unitization),
  H-MAPPING (disagreement-mass concentration + chain-share contrast
  + top-10 crosswalk audit), H-DIRECTION (matcher orientation share;
  global-flip agreement), H-DEFINITION (continuous relative-position
  W1 / Spearman + 5-bin agreement). BH q = 0.05 across the one
  per-sign permutation family. Recommendation assembled mechanically
  from the verdicts (spec §6 templates).
- **Diagnostic only:** no anchor changes, no validation verdicts;
  the anchors file is never opened for writing under this spec.
- **Pre-freeze diagnostics (schema level):** the layers share no
  artifact key (Holdat `cisi_number` is Holdat-internal sequential;
  ICIT `cisi` is CISI numbering; intersection 0 raw and normalized),
  so identity is established by inscription content in M-sign space.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## [2026-10-07] Entry — Phase-116 / Spec 015: Outcome — Two Mechanisms Refuted, Three Unresolved at Frozen Power; Recommendation R-NONE

- **Baseline reproduced exactly (asserted before any arm ran):**
  T1 v2 over STRICT94 — judged 51 (8 PASS / 43 FAIL), 40
  modal-disagreement failures, median TV 0.789474, mean TV 0.657011,
  A_full 11/51. The keyed ICIT layer's kept subset reproduces the
  Phase-115 v2 layer byte-for-byte in sequence content/order
  (4,531 inscriptions / 13,492 mapped / 2,388 sentinels); conversion
  audit recomputed all 16,141 matcher-population tokens from their
  stored source codes with zero mismatches.
- **Matcher yield (itself a finding):** Tier A (direct, mutually
  unique) **13** pairs; Tier B (reversed) **17**; Tier C
  (containment) **1**; ambiguous-orientation 0. Before uniqueness:
  135 direct-compatible vs **240 reversed-compatible** pairs;
  14,456 containment candidates collapsed to 1 mutually-unique
  pair. The two compilations share almost no mutually-unique
  identical texts.
- **H-COMPOSITION — UNRESOLVED (power):** Tier A 13 < the frozen
  100-pair gate; only 3 judged signs qualify on the restriction
  (on those 3, restricted agreement is 1.0 / TV 0.0 — n=3 licenses
  nothing, and the frozen gate said so in advance).
- **H-SEGMENTATION — UNRESOLVED:** arm S1 **REFUTED** — stripping
  sentinel positions made T1 failures *worse* (43 → 45); the
  sentinel-geometry mechanism is dead (leading-sentinel rate
  12.84%; median demoted-initial share 0.1667, both too small and
  the wrong direction). Arm S2 UNRESOLVED (power): 4 qualifying
  signs; descriptively artifact-units TV 0.1042 vs row-units
  0.0917 — no repair signal.
- **H-MAPPING — REFUTED:** disagreement is diffuse, not
  crosswalk-concentrated (top-5 TV share 0.1492, top-10 0.2956 ≤
  the frozen 0.40 diffuseness bar; chain-heavy group only 3 signs
  vs 46 clean, descriptive Δ = 0.0598). The §5.3 audit table is in
  the results JSON.
- **H-DIRECTION — UNRESOLVED:** D1 underpowered (A+B = 30 < 50;
  reversed share 0.5667 suggestive but licenses no verdict). D2:
  a global flip improves modal agreement 0.2157 → 0.3137 (+0.098),
  inside the frozen unresolved band (0.05, 0.30) — orientation
  contributes at most modestly; it is not the primary mechanism.
- **H-DEFINITION — REFUTED (decisively):** median W1 = 0.4519
  (refutation bar 0.20), material-displacement share 0.6863 (bar
  0.50), 5-bin modal agreement 0.1373, and per-sign mean relative
  positions are essentially uncorrelated across the compilations
  (Spearman ρ = −0.0826). The disagreement is genuine positional
  displacement, not a binning artifact. Permutation context: 43 of
  51 judged signs disagree beyond token-level sampling noise
  (BH q = 0.05, full layers).
- **Harmonization recommendation (spec §6, mechanical): R-NONE** —
  no transformation is justified; cross-corpus positional
  validation on this pair of compilations is not viable under any
  convention alignment tested; a future battery must not use a
  conjunctive cross-corpus positional gate on this pair.
  MAY-NOT lines recorded for crosswalk error and binning artifact;
  composition/segmentation/direction remain unresolved — no
  assumption licensed either way. All 44 anchors remain
  `pending_non_sa_validation`.
- **Deviations / interpretations (disclosed):** Tier C implemented
  with strict length inequality (equal-length containment *is*
  compatibility, i.e. tiers A/B); a matched Holdat text with
  partners in both Tier A and Tier C takes its artifact group from
  the Tier A partner; the keyed builder retains per-token source
  codes (required by the §5.3 audit) beyond spec §2's listed
  fields. Suite/foundation runs used the main checkout's
  gitignored `corpora/downloads` via a temporary symlink in this
  worktree (git-invisible; removed after); unrelated generated-file
  churn from the suite/foundation runs was reverted and is not in
  the PR.
- **Suite / foundation:** full backend suite **687 passed / 11
  skipped / 0 failed** (main-checkout baseline at 5d8f5d58: 673 /
  11; +14 Phase-116 tests); foundation check **40 passed / 0
  failed / 8 warnings**; ruff clean. Anchors file untouched.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.
## [2026-10-07] Entry — Correction: Spec 012 Study Renumbered Phase-113 → Phase-114; §6 Sanity-Anchor Qualification Recorded

Append-only records correction to the two spec-012 entries above
(freeze and outcome, both 2026-10-07). The original entries stand
as written when made; nothing in them is altered. No re-run was
performed and no study outcome is affected.

- **Renumbering.** Spec 012's adversarial blind-affiliation study
  was designed and executed as "Phase-113" in parallel with spec
  011's non-SA validation study, which also carried Phase-113 and
  merged first (PR #69), retaining the number. Spec 012's study
  is renumbered **Phase-114**. Frozen artifact filenames
  (`reports/phase113_*` and the `phase113_*` code modules) are
  retained unchanged; "Phase-113" in those artifacts and in the
  entries above refers to this study. Dated renumbering notes
  were added at the top of
  `specs/012-phase113-blind-affiliation/spec.md` and of
  `reports/phase113_blind_affiliation_summary.md`.
- **§6 sanity-anchor qualification.** Spec 012 §6 requires
  positional-bigram TV between G(θ_S5) and the frozen S5
  generator < 0.10. Under the finest-grained reading of that
  statistic (frequency-weighted per-(b, b′, x)-context TV), two
  samples from the identical model at ~55k tokens already sit at
  0.246 (the sampling-noise floor); G(θ_S5)-vs-S5 measured 0.243
  — no systematic excess over the noise floor. The committed
  unit test therefore asserts TV < 0.30 AND TV ≤ noise floor +
  0.05, plus unigram TV to R1 < 0.10 (measured 0.038); under the
  coarser per-bin-pair successor-TV reading the value is 0.064,
  which does meet 0.10. The anchor's substance is confirmed
  three ways (S5's recorded unigram TV to R1 = 0.0419 reproduced
  exactly; no excess over the identical-model noise floor;
  candidate 0 behaved exactly as S5 in the run — objective
  0.99999995 under C_1, unigram TV 0.0383). No study outcome
  depends on the anchor's threshold: the INVALID-at-round-1
  verdict rests solely on the frozen rounds protocol (spec 012
  §§7–10). Recorded in full as the §12.1 addendum (2026-10-07)
  in the spec and as a dated footnote in the summary at the
  candidate-0 mention.

**AI disclosure:** records corrections recorded by an AI agent
(Muse Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## [2026-10-07] Entry — Merge Record: PR #71 Branch Merged origin/main (PR #70); Phase-Number Code Collisions Resolved

The Phase-114 (spec 012) branch merged origin/main at a6d97daf
(PR #70: spec 011 outcome, spec 013, spec 014 / Phase-115). The
parallel use of "Phase-113" by specs 011 and 012 had produced
same-name code modules; conflicts were resolved append-only /
union, with no frozen spec or report text altered and no result
changed:

- Both `LEDGER.md` files: all entries from both sides retained
  in full; the correction entry above closes each file.
- `backend/glossa_lab/phase113_run.py`: spec 011's battery
  orchestrator retains the name; spec 012's orchestrator moved
  to `phase114_run.py` (import sites updated; report and state
  artifact names remain `phase113_*` as frozen).
- `backend/glossa_lab/experiment_graph_phase113.py`: unioned —
  one module now registers spec 011's
  IndusPhase113NonSaValidation plus spec 012's
  IndusPhase113BlindRounds / IndusPhase113BlindClassify, each
  study's node behavior preserved.
- Recorded in spec 012 as the §12.2 addendum (2026-10-07).

**AI disclosure:** merge resolution recorded by an AI agent
(Muse Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## [2026-10-07] Entry — Phase-117 (spec 016): Within-Compilation Validation Battery — DESIGN ONLY (not executed)

Owner authorized the design 2026-10-07 (execution requires his
separate, explicit approval; this entry records a design, not
a study). Specs 011/014 batteries were rejected at calibration
on their cross-corpus test; Phase-116 (spec 015) returned
R-NONE — no conjunctive cross-corpus positional gate on the
Holdat/ICIT pair — and licensed exactly two routes: within a
single compilation, or await a genuinely independent corpus.
Spec 016 takes the first route. Frozen design: W1 split-half
positional cross-fit (spec-011 T2a thresholds unretuned;
frozen partition, 15 length×site strata, seed 117, halves
3,531 / 3,471 tokens); W2 (spec-011 T3) DROPPED as a
decision-bearing instrument on design-stage numbers (5/44
PASS-capable; composed-legality base rate 1.000, 523/523);
W3 junction model over STRICT94 readings with a frozen
quantile floor and a seeded donor-permutation null (B = 999,
frequency-band donors; judgeable 40/44); W4 site-stratum
stability with an attestation-asymmetric FAIL (judgeable
9/44). Calibration gates: STRICT94 LOO VALIDATED ≥ 47/94;
KUR113 VALIDATED ≤ 5/113 — failure rejects the battery and
the 44 are never run. Decision rule: VALIDATED ⟺ W3 PASS ∧
(W1 ∨ W4) PASS ∧ no FAIL; DEMOTE on any FAIL; else
UNRESOLVED (M235, M254, M402 are UNRESOLVED by construction
— judgeable by no instrument). The success status is the new
value `validated_within_compilation`, defined in spec §9
with an anti-circularity clause: it claims internal
coherence within Holdat only, never independence, never to
be conflated with `validated_non_sa`; SA-lineage provenance
is unaltered by any outcome; all outcomes are provisional
against genuinely independent corpora. Feasibility appendix
(A.1–A.5) computed from Holdat counts at design stage — no
sign was scored. No anchors changed; no code written; no
run performed. Branch `phase/within-compilation-battery-design`
from main 83d03672 (pre-history-rewrite; rebase is mechanical,
trees identical).

**AI disclosure:** design recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## [2026-10-07] Entry — Phase-117 (spec 016): Within-Compilation Validation Battery — EXECUTED, BATTERY REJECTED at calibration

Owner approved execution 2026-10-07 (after design PR #74
merged; main cea59cbe). Implementation (pipeline b5fd725a;
H23 graph registration e3529b55; outcome dd898a50): W1
split-half positional cross-fit, W3 junction coherence with
donor-permutation null, W4 site-stratum stability; W2
descriptive only per spec §4.2. The frozen partition was
reproduced and asserted before any instrument ran (halves
A = 3,531 / B = 3,471 tokens; Appendix A.5 spot counts exact:
M293 124/108, M011 10/5, M024 12/1, M177 5/0). phi (10th
percentile, linear interpolation, of the 81 STRICT94
leave-one-out W3 self-scores) = -7.461366. Determinism
verified: a second in-process execution reproduced the
results byte-identically except the run timestamp.

Calibration (spec §6), reported verbatim: STRICT94
leave-one-out — VALIDATED 2 / DEMOTE 19 / UNRESOLVED 73;
positive gate >= 47/94 FAILED. Per-instrument STRICT94
(PASS/FAIL/INDETERMINATE): W1 63/5/26; W3 3/9/82; W4
44/10/40. KUR113 — VALIDATED 0 / DEMOTE 0 / UNRESOLVED 113;
negative gate <= 5/113 PASSED (every instrument state
INDETERMINATE for the whole cohort — the asymmetry §6
registered). Verdict: BATTERY REJECTED at calibration.
FLAGGED44 was never run; the anchors file was not modified;
no change register exists; all 44 remain
`pending_non_sa_validation`; tier counts unchanged
(166 HIGH / 5 MEDIUM / 3 LOW / 113 CANDIDATE); strict core
94; Holdat H+M coverage 0.7368 unchanged.

Diagnosis (post-hoc, labeled as such): the §8 conjunction's
mandatory W3 PASS is the binding constraint — under
leave-one-out only 3/94 core signs meet W3's frozen PASS
band (p <= 0.05 and score >= phi) against the core-minus-self
junction model, although W1 cross-fit PASSes 63/94 and W4
44/94 of the core. No re-tuning under spec 016; a successor
battery requires a new spec, and the genuinely independent
corpus route remains the other Phase-116-licensed branch.
Verification: 24 new unit tests pass (incl. toy end-to-end
controls and the frozen partition assertion); full backend
suite 758 passed / 13 skipped / 0 failed; foundation check
40 / 0 / 8; ruff clean.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## [2026-10-07] Entry — Phase-119 (spec 018): PRED-2026 Readiness Harness — BUILT (dry run only; no prediction evaluated)

Owner directed 2026-10-07. Spec 018 frozen in its own commit
(d09e3e47) before any code: the registered PRED-2026-001–003
criteria quoted verbatim from docs/PREDICTION_REGISTER.md §2;
frozen sign sets (TERMINAL 14 / INITIAL 12 / MEDIAL 46 /
MIXED 33, corpus_freq ≥ 10 on the frozen sign inventory) and
canonical registry map (M→P / W→P with the freq-then-lowest-P
conflict rule; M002 ambiguous → UNK); evaluability matrix
classifying the ICIT lineage honestly per item
(icit_lineage_derivative and derivation_corpus qualify for
nothing; icit_full qualifies as the registered target under
verbatim caveat C1); dedup protocol (stage A exact, stage B
sentinel-normalized, stage C Levenshtein ≤ 1 on UNK-stripped
sequences of length ≥ 4 against kept anchors only); §6.1
gates (qualifying class, complete provenance,
unmapped+ambiguous ≤ 25% of tokens, verdict lock, ≥ 2 sites
for 003) enforced in code before any criterion statistic
exists; §8 dry-run rule with the in-artifact label "HARNESS
DRY RUN — NOT A PRED EVALUATION".

Built: backend/glossa_lab/pred_harness.py (adapters for
rmrl_concordance / image_transcription / future_concordance
+ dry-run-only converted_layer, provenance log per the
Phase-107/111 pattern), scripts/phase119_pred_harness.py,
graph node IndusPhase119PredHarness (H23: registered and
asserted in ATOMIC_NODES before any run), synthetic fixtures,
21 unit tests incl. a toy prediction evaluated end-to-end
through the real gating/scoring code in both verdict
directions and the real PRED-2026-003 scorer on toy
fixtures (0.80 CONFIRMED / 0.40 REFUTED).

Dry run (only run performed; population = Phase-115 expanded
ICIT converted layer, 4,531 inscriptions / 15,880 tokens,
class icit_lineage_derivative): dedup kept 2,446 (stage A
removed 1,468 = 32.40%; B incremental 370; C incremental 247;
cumulative 46.02%). Sign-set coverage: TERMINAL attested
12/14 (unattested P076, P125), INITIAL 11/12 (unattested
P000), MEDIAL 38/46; unmapped 47 tokens (9 unmapped + 38
ambiguous). PRED-003 classifiability coverage 2,544/4,531
(56.15%) pre-dedup, 1,045/2,446 (42.72%) post-dedup. No rate
against the 0.45 thresholds, no conformance fraction, and no
verdict was computed. One additive correction: spec Appendix
A.6 records that the appendix's prototype dedup figures were
measured on raw M-space sequences while §5 as frozen operates
on P-space sequences; the harness asserts the corrected
P-space values and reproduced every other Appendix A figure
exactly. Reports: reports/phase119_pred_harness_results.json
+ phase119_acquisition_log.json (three awaited sources as
GAPs) + phase119_pred_harness_summary.md. Anchors unchanged
(287; 166/5/3/113; strict core 94). Verification: 21 new
tests pass; full backend suite 779 passed / 13 skipped /
0 failed (main baseline 758/13); foundation check 40 / 0 / 8;
ruff clean.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.
## [2026-10-07] Entry — Phase-118 (spec 017): Within-Compilation Validation Battery v2 (W1-primary redesign) — DESIGNED + EXECUTED under one commission, BATTERY REJECTED at calibration

Spec 017 was commissioned by the owner 2026-10-07 ("Commission
spec 017 — W1-primary redesign") covering design and execution
in one authorization, after spec 016's battery was rejected at
Phase-117 calibration. Design frozen in its own commit
(8c0d93a3) before any Phase-118 statistic existed; Appendix A
finalized in the following commit (9d9d037e); branch stacked on
PR #75's branch `phase/117-within-compilation-battery`.

The redesign, from Phase-117's recorded diagnosis: W1
split-half positional cross-fit PRIMARY, carried verbatim
(frozen seed-117 partition; T2a thresholds unretuned); W3
junction coherence rebuilt cross-fit — junction model and
phi_d (10th percentile, type-7, of STRICT94 cross-fit
self-scores per direction) derived on the opposite partition
half, the leave-one-out-minus-self reference abolished,
donor-permutation null (B = 999) retained per direction with
median-donor bands (PASS_d: score >= phi_d and p_d <= 0.50;
FAIL_d the mirror), per-direction junction floor 2; W4
verbatim as FAIL-guard only; W2 remains dropped. Judgeability
frozen as count properties (J94 = 67, JKUR = 29, asserted at
run time and held). Gates with teeth: positive — VALIDATED
share over J94 >= 0.50 (|J94| >= 50); negative — over JKUR,
VALIDATED = 0 AND DEMOTE share >= 0.25, so universal
indeterminacy fails the gate instead of passing it (spec
016's recorded defect). Decision rule: VALIDATED iff W1 PASS
and W3 PASS and no FAIL; §9 carried over verbatim in
substance (validated_within_compilation; never independent
validation; provenance unaltered; no promotion, ever).

Execution: implementation + 12 unit tests (toy coherent
validates / incoherent demotes; H23 node
IndusPhase118WithinCompilationValidation registered before
any run). Frozen assertions held: partition A 3,531 / B 3,471;
J94 = 67; JKUR = 29. phi: modelA->scoreB -7.192755 (n = 83);
modelB->scoreA -7.088781 (n = 89). Calibration — STRICT94:
VALIDATED 14 / DEMOTE 21 / UNRESOLVED 59; per-instrument
(PASS/FAIL/INDETERMINATE): W1 63/5/26; W3 22/11/61; W4
44/10/40. Positive gate FAILED: VALIDATED over J94 =
14/67 = 0.2090 (required >= 0.50). KUR113: VALIDATED 0 /
DEMOTE 0 / UNRESOLVED 113; over JKUR: VALIDATED 0, DEMOTE
0/29 = 0.0000 (required >= 0.25), UNRESOLVED 29. Negative
gate FAILED on its discrimination clause. Verdict: BATTERY
REJECTED at calibration. FLAGGED44 was never run; the anchors
file was not modified; no change register exists; all 44
remain `pending_non_sa_validation`; tier counts unchanged
(166 HIGH / 5 MEDIUM / 3 LOW / 113 CANDIDATE); strict core 94;
Holdat H+M coverage 0.7368 unchanged.

Diagnosis (measured, not post-hoc speculation): the cross-fit
rebuild repaired W3's PASS leg on the core (PASS 3 -> 22) but
the both-directions conjunction still leaves most core signs
INDETERMINATE (61/94), and the negative control exposed the
deeper limit: in 0 of 58 JKUR direction records is the
cross-fit score below phi_d, while every judgeable p-value is
>= 0.579 (median 0.653) — the donor leg separates `kur` from
the core's fabric but the absolute leg never fires, because
the `kur` phoneme pair occupies high-probability junction
cells (the coarse-fabric limit registered in spec §10). The
negative gate failed rather than passing vacuously, which is
the behavior spec 017 §6 was designed to force. No re-tuning
under spec 017; a successor battery requires a new spec, and
the genuinely independent corpus route remains the other
Phase-116-licensed branch. Determinism verified: two
executions byte-identical except run_utc. Verification:
suite 770 passed / 13 skipped / 0 failed; foundation check
40 / 0 / 8; ruff clean.

**AI disclosure:** design and execution recorded by an AI
agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.

## 2026-10-07 — Validation-battery line CLOSED (owner decision)

Owner decision (Tristen Pierson, 2026-10-07): the anchor-validation battery line is closed. Four frozen batteries were rejected at calibration — Phase-113 (spec 011, cross-corpus v1: T1 starved on the partial ICIT layer, STRICT94 3/94), Phase-115 (spec 014, cross-corpus v2: with the expanded layer, Holdat/ICIT positional profiles genuinely disagree, STRICT94 1/94), Phase-117 (spec 016, within-compilation v1: mandatory W3 leave-one-out reference self-defeating, STRICT94 2/94), Phase-118 (spec 017, within-compilation v2 W1-primary: positive gate 14/67 judgeable; negative gate failed its discrimination clause — the coarse-fabric limit of spec 017 §10, measured under both constructions). No further battery redesigns are authorized; another redesign would be tuning toward a pass. The 44 flagged anchors remain `pending_non_sa_validation`. Their validation awaits genuinely independent data (RMRL / Dixit-Mitra / Mahadevan Chair concordance; PRED-2026 readiness proceeds under spec 018). AI-assisted record (Muse Spark, Muse), owner-directed.

## 2026-10-08 — Phase-122: Parpola↔Mahadevan Crosswalk v1 + mayig Corpus Integration

Crosswalk v1 built as data (CSV + JSON) in `data/crosswalks/
parpola_mahadevan_crosswalk_v1.{csv,json}`, loader
`backend/glossa_lab/data/parpola_mahadevan_crosswalk_v1.py`,
builder `backend/scripts/phase122_build_crosswalk_mayig.py`
(deterministic; re-runs byte-identical). Canonical basis: the
program's canonical registry `data/crosswalks/
canonical_sign_registry.csv` (sha256 unchanged,
8a0b2a82…bd420), named the map of record by spec 018 §A2; the
sparse `mahadevan_parpola_crosswalk_v2.json` — explicitly
REJECTED as canonical by spec 018 appendix A.4 — is used only
as a labelled source. 766 rows = 762 pairs + 4 unmapped-P rows
(P000, P225, P261, P358). P signs covered 412, M signs covered
412. Relations (no forced 1:1): 1:1 352, one-to-many 78,
many-to-one 66, many-to-many 266, unmapped 4. Confidence
(frozen rubric: high = canonical registry AND mayig features
agree; medium = exactly one of those; low = v2-only or
candidate-only): high 372, medium 0, low 390 — medium is empty
because the registry and mayig pair sets are identical
(372/372, two independent structured maps in pair-for-pair
agreement). Conflicts: 383 pairs across 209 P signs, kept on
both sides with sources and flagged — essentially all are the
documented crosswalk_v2 number-identity inversions (168 of
v2's 171 pairs contradict the registry+mayig consensus),
independently confirming spec 018 A.4. The candidates file's
4 pre-recorded unresolved conflicts are carried verbatim.

mayig corpus integrated as a first-class corpus layer
alongside the existing converted layers:
`data/corpus_layers/mayig_cisi_layer_v1.json` (+ `_meta.json`),
loader `backend/glossa_lab/data/mayig_layer.py`, following the
Phase-115/116 builder + build-metadata + per-inscription
provenance pattern. Source: mayig/indus-valley-script-corpus
commit ad2f1e218a34b8c33c57de0d6cb8d99272765bbb (2025-04-16),
MIT license verified from its LICENSE file (Copyright (c) 2024
Michael Carlson); because mayig is MIT the converted layer is
committed (unlike the ICIT layers, gitignored with statistics
only). 179 inscriptions / 179 CISI objects (all Mohenjo-daro),
1,003 sign tokens, 182 distinct P signs; every record keyed by
CISI object ID with side ID, description, source file, token
sequence in source order, and per-token feature vectors.

Coverage through crosswalk v1 (usable map = high+medium):
tokens clean 768 / ambiguous 202 / unmapped 33 of 1,003;
inscriptions clean 42 / partial 137 / none 0. Top failure
modes: P122 ambiguous (76 tokens), P086 ambiguous (35), P000
unmapped (19 — damage marker, correctly no M counterpart).
CISI Vols. 1–2 overlap by object ID: against the structured ID
lists obtainable now (Bhaskar et al. 2024 ESM13 catalogue CISI
IDs; Phase-116 keyed ICIT layer `cisi` field), all 179 mayig
objects are present in both (179/179, 100%); the CISI scan OCR
extraction bases catch only 12 (Vol. 1) and 8 (Vol. 2) — an
extraction artefact, documented in the report; the definitive
figure awaits Phase E's structured catalogue table.
Marshall numbering (Kondratov, Phase-121): no Marshall↔M/P
pairs extractable from sources on main; v1 asserts none.

Explicit non-claims: no positional comparison study was run
(future spec); no anchor-status implications; the crosswalk is
a working v1 with stated confidence, not an adjudication of
sign identity; anchors and tiers untouched. Report:
`reports/phase122_crosswalk_mayig.md` (+ `_results.json`).
Verification: 8 new tests in
`backend/tests/test_phase122_crosswalk_mayig.py`; full backend
suite 800 passed / 12 skipped / 0 failed (run in two parts:
790/12 excluding test_pipelines_gpu.py, plus 10/0 GPU-file);
foundation check 40 / 0 / 8; ruff clean on new files. Test
side-effect changes (glossa-indus/ claims, outputs/) reverted
before commit.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson,
per constitution §VI.
