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

## [2026-10-08] Entry — Phase-120: Bhaskar (2024) descriptive triage of the 44 pending anchors

First phase of the new-material program (Phase A). Commissioned as a
triage of the 44 anchors flagged `pending_non_sa_validation` against
the supplementary material of Bhaskar (2024), "Markers and agencies
of anisotropy in the Indus sign system" (Indian J. Hist. Sci.,
doi:10.1007/s43539-023-00102-3; ESM1-ESM13, acquired in the
2026-10-08 Indus data deep-sweep).

SCOPE FINDING (the phase's main result): the ESMs are NOT a
per-sign cross-compilation disagreement table. They are anisotropy
(sign-order/transposition) datasets — ESM1 the 33-object F3
catalogue, ESM2 F3 simulations vs M77/ICIT with D-type results and
the error label E1, ESM3-ESM12 sign-behaviour studies (99, 267/267a,
doubles, 97/98/123 markers, 244 family, fish family), ESM13 an
animal-behaviour catalogue (2,383 CISI rows). Bhaskar's stated
method (article p. 2) notes M77/ICIT/CISI disagreements only "in
each case", at case level. No per-sign M77/ICIT/CISI readings grid
exists in the material, and none was fabricated.

Built instead, honestly: (1) a curated register of every
cross-source disagreement Bhaskar documents — 16 dispute cases
(267/267a conflation BH-D01; ICIT conflations of 97/98 and 99/100;
the 244 normalisation split; two labelled E1s + the prose E1 of
ESM7 case 7; the M77 misprint of 257 as 197; the 162
classification dispute; the 402 coverage gap) + 4 form-reanalysis
notes — as `reports/phase120_bhaskar_disagreements.{csv,json}`;
(2) a mention index over the list-structured ESMs (behavioural
attestation only); (3) the triage of the 44 in
`reports/phase120_bhaskar_triage_44.{md,json}` via
`backend/glossa_lab/phase120_bhaskar.py` (H23 node
IndusPhase120BhaskarTriage registered before any run; runner
`backend/scripts/phase120_bhaskar_triage.py`).

Classification (strict rule: CONTESTED only when a documented case
names the sign's identity/form class; ALL-AGREE never inferred
from silent use, because the source contains no per-sign
concordance statements): ALL-AGREE 0 / CONTESTED 1 / NOT-COVERED
43 (16 mentioned behaviourally, 27 not mentioned). The one
CONTESTED anchor is M402 (BH-D10): the left-waving frontal flag on
K-39 has no variant in M77, ICIT, or the font package, and the
only other instance (7065) is doubted by Bhaskar to be 402 at
all — an object-vs-inventories gap, not a source-vs-source split.
Near-misses recorded in the report: M072 and M345 fall under
Bhaskar's own form-reanalyses (BH-R01/R02), a different claim
kind, and stay NOT-COVERED. Sanity check: 14/14 hand-read ESM
items agree with the parse (error modes documented in the
report: PUA glyph font — numbers/prose only; label-pattern
extraction finds 2 of 3 E1s, the third is prose).

NON-CLAIMS: descriptive only; no anchor status changed (anchors
file SHA-256 identical before/after; 287 anchors, 166/5/3/113);
nothing validated; no PRED content. Verification: 17 new tests;
full backend suite 808 passed / 13 skipped / 0 failed;
foundation check 40 / 0 / 8; ruff clean. PR opened against main;
not merged (owner merges).

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.
## Phase-121 — Soviet Positional Dataset (descriptive only)

Built 2026-10-08 under the owner's direction (Glossa-Lab
new-material program, Phase B). Extracted the printed tables of
the Soviet reports into a machine-readable descriptive dataset
(`data/soviet_positional/`, 7 tables, 109 records, every record
tracing to source + printed page + table id): Kondratov 1965
Tables 1-4 (new-sign emergence, 56 rows; sign frequency classes,
315 Proto-Indian signs in aggregate; polygrams; stable
initials x stable finals per-sign matrix) from Zide & Zvelebil
1976, and Volchok's three calendrical tables from Proto-Indica
1973. Findings recorded honestly: the 1968 Knorozov Formal
Analysis contains NO frequency/positional tables (prose + glyph
illustrations, searched in full), and Proto-Indica 1973 contains
no sign-frequency tables at all; Gurov's Table 1 (pp.56-57)
defeated extraction (diacriticised transliteration; no values
guessed). Method: 300-DPI renders, fresh RapidOCR from the
existing ocr venv, publisher text layer, and visual reads
triangulated. Hand verification: 36 sampled cells re-read from
the rendered pages, 36/36 match print. Printed anomalies
preserved as printed, never repaired (K1965-T4 printed grand
total 171 vs cell sum 160; K1965-T3 total mismatches). Memo:
`reports/phase121_soviet_positional_dataset.md`. NON-CLAIMS:
descriptive dataset only; no prediction scored, no anchor
validated; whether the Soviet positional data can formally
bear on PRED-2026-001/002 is an open question for a future
spec adjudication. Suite and foundation results recorded in
the Phase-121 PR.

**AI disclosure:** design and execution recorded by an AI
agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.
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
## 2026-10-08 — Phase-123: Wells segmentation witness memo (Phase D)

Witness statement (not an adjudication) recording how Bryan K. Wells's
grapheme segmentation (MA thesis, Calgary, 1998; PhD thesis, Harvard,
2006) treats each of the 157 anchor signs (113 CANDIDATE + 44
`pending_non_sa_validation`). Sources: MA thesis (587 signs / 802
varieties / 63 Sets, thesis p. 48; Fig. 3.6 concordance, p. 77) and PhD
thesis (676 signs, pp. 67-68; Fig. 3.2 plates, pp. 90-92; Appendix I
per-sign sheets), the held canonical registry (mayig Wells-2015
cross-match), and Phase-123 hand glyph-matching against the PhD plates.
Coverage: treatment determinable for 134/157 — SAME 87, SPLIT 40,
MERGE 5, NOT-COVERED 2, INDETERMINATE 23 (incl. M033/M126, whose only
correspondence runs through the unmerged Phase-122 chain, PR #81, and
which are therefore recorded indeterminate with the lead noted).
Hand verification: 20 rows checked against the thesis plates —
17 glyph-consistent (M389 consistent by glyph but carries a recorded
registry conflict over W805), 2 partial (M149, M401), 1 discrepancy
(M293, registry W920 vs the looped plate glyph; Wells's own 920/921
discussion, PhD pp. 70-71, does not settle it from the plate). The
attestation co-occurrence method (MA Appendix 1 vs ICIT artifact sets)
was attempted and rejected (best Jaccard 0.22) — recorded in the memo
so it is not repeated on the same inputs. No anchor tier, value, or
status was changed; no adoption of Wells's segmentation is recommended
or implied. Artifacts: `reports/phase123_wells_segmentation_witness.md`,
`data/crosswalks/wells_segmentation_witness_v1.{csv,json}`,
`backend/scripts/phase123_build_wells_witness.py`,
`backend/tests/test_phase123_wells_witness.py` (6 passed). Full backend
suite: 798 passed / 12 skipped / 0 failed (corpora/downloads symlinked
from the main checkout, as in prior phases); foundation check
40 passed / 0 failed / 8 warnings (baseline unchanged); ruff clean.
Test side effects (glossa-indus/ claims + reports, outputs/) reverted
before commit.

**AI disclosure:** research and execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## [2026-10-08] Entry — Phase-124: CISI Image Layer (enabling asset) — BUILT

Built the image layer over the CISI Vol. 1 (= MASI 86) and Vol. 2
research scans (in-copyright research copies; 431 + 486 pages,
image-only PDFs). The bundled djvu.txt OCR was assessed and found
inadequate for page-anchored work (single continuous stream, zero
page breaks, heavy garbling; corroborates only 344/1,475 (Vol. 1)
and 794/2,019 (Vol. 2) of the distinct IDs parsed by fresh OCR), so
all plate rows rest on fresh per-page RapidOCR (140 dpi renders,
checkpointed) with the djvu ID sequence used only as an existence
corroboration in each row's extraction basis.

Catalogue table (LOCAL STORE ONLY): 7,705 rows (Vol. 1: 3,320;
Vol. 2: 4,385), one per photographed side, keyed by CISI object ID
with 22 fields (caption raw + OCR score, PDF page, printed page,
site, object type, motif chapter, scale %, volume-level collection
scope, photo box, extraction basis, confidence, notes). Per-object
museum/material/dimensions are NOT printed on CISI plates and are
recorded as "not printed per object in CISI plates" with the fields
empty — not filled from outside sources. 3,156 non-plate
caption-like lines (sign-index entries) were dropped by the
plate-page/photo rule and counted. Low-confidence rows: 981, kept
and flagged, never silently corrected. Hand verification on four
pages read visually before extraction (Vol. 1 printed 10/30/55,
Vol. 2 printed 31; 36 rows): CISI ID 36/36 (2 via flagged I/l→1
normalisation), side 35/36 (M-69 a lost its side glyph), header
fields 16/16, photo association 36/36 with one degenerate merged
box (M-667 a, Vol. 2). Field accuracy on the sample: 87/88.

Sign-crop pipeline (committed code): caption-anchored photo
location (page-adaptive dark threshold; grid texture segmentation
as fallback) + inscription-band contrast-projection segmentation.
Worked sample on four plate pages (32 photos): 82 crops written,
1 photo skipped (degenerate box); visual classification of every
crop: 38 good / 29 partial / 15 bad — the honest single-pass yield
of the heuristic (46 % good). The 38-crop verified sample is
described (IDs, pages, coordinates) in
reports/phase124_cisi_local_store_manifest.json.

STORAGE GOVERNANCE: scans are in-copyright research copies; the
catalogue CSVs, crops, OCR checkpoints and renders live ONLY in
the gitignored local store
corpora/downloads/cisi_image_layer/ (verified with
git check-ignore -v from the main checkout: .gitignore:176
corpora/ rule; git status checked before commit — no image or
derived table staged). The PR contains only code, drivers, tests,
the memo, the describing manifest and these ledger entries.
NON-CLAIMS: enabling asset only; no sign identifications asserted;
no comparison study run; no anchor/tier/corpus statistic changed.
Verification: 24 new unit tests; full backend suite 816 passed / 12 skipped / 0 failed; foundation check 40 passed / 0 failed / 8 warnings; ruff
clean.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## [2026-10-08] Entry — Phase-125 (Spec 019): Cross-Compilation Positional Comparison — FAIL (agreement refuted)

Spec 019 (`specs/019-phase125-cross-compilation-positional/`,
freeze commit 8da500c0, committed alone before any comparison
statistic) pre-registered the question: do per-sign positional
profiles (initial/medial/terminal rates) computed WITHIN the
mayig/CISI compilation agree with the same profiles computed
WITHIN the Holdat compilation, for the same signs joined via
the Phase-122 crosswalk? Profiles were computed strictly
inside each compilation (inscriptions never pooled); the sole
join is crosswalk v1. PRIMARY arm: high-confidence pairs that
are unambiguous within the high set — 286 pairs of 372 high
(762 total). Floor 8 tokens per sign per compilation, counted
exclusions only: PRIMARY judgeable 16/286; sensitivity arm A
(medium-included) coincides pair-for-pair with PRIMARY because
crosswalk v1 contains zero medium pairs (registered design
fact, not an independent check); sensitivity arm B (all 762
pairs, pair-by-pair) judgeable 28.

Object-join discipline: NO object join was performed. Holdat's
cisi_number is internal sequential numbering (contiguous
1..N per site prefix, re-verified at freeze), not a CISI object
ID; the zero-padded coincidence with mayig CISI IDs is not an
identity join and was not used (spec §2.1). The comparison is
sign-level over full within-compilation profiles.

VERDICT (PRIMARY arm, frozen §6 rule, as found): **FAIL —
DISAGREEMENT.** Median TV 0.636931 (FAIL bound >= 0.50; PASS
bound <= 0.35); median W1 0.658181; Spearman rho initial
-0.424758, terminal +0.316034, medial -0.476874 (PASS bound
>= 0.50 on both gated rates); modal-class agreement 3/16 =
0.1875; pairing-shuffle null (B = 999, seed 125125) p_null
0.824 (823/999 shuffled re-pairings had median TV <= the
observed) — the falsifier pattern in full: far apart AND the
crosswalk pairing carries no positional agreement beyond
shuffled pairings. Arm B shows the same pattern (median TV
0.636931 over 28 judgeable pairs, p_null 0.737). Claim scope
per spec §7: this refutes crosswalk-joined positional
agreement between these two compilations on the judgeable
primary pairs; it does not identify which side produces the
disagreement, says nothing about individual signs/readings,
and leaves Phase-116 R-NONE (Holdat vs ICIT lineage, a
different pair and join) untouched. Verification: 12 new
unit tests (toy PASS / FAIL / NULL-STARVED controls through
the real §6 rule); full backend suite 866 passed / 13
skipped / 0 failed; foundation check 40 / 0 / 8; ruff clean.
Anchors file byte-identical (sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed,
asserted in code before/after). No anchor, claim, or PRED
status changed. Artifacts:
`reports/phase125_cross_compilation_results.json`,
`reports/phase125_cross_compilation_summary.md`.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## [2026-10-08] Entry — Spec 020: Soviet Positional Dataset Adjudication for PRED-2026-001/002 — Verdict NO (non-qualifying)

Spec 020 (`specs/020-soviet-pred-adjudication/`, STEP 2 of the
owner-ordered Glossa-Lab program, from main `3fd5ad30`)
adjudicated whether the Phase-121 Soviet positional dataset
(Kondratov 1965 tables, extracted from Zide & Zvelebil 1976;
`data/soviet_positional/`) qualifies as an evaluation source
for PRED-2026-001/002. The paper states its criteria BEFORE
application (spec §2), each derived mechanically from the
registered texts (register §2; spec 018 §§3–7): C1
source-class membership / frozen matrix qualification, C2
identity with the withheld data or a qualifying substitute,
C3 computability of the registered per-sign end/start
rates, C4 applicability of the frozen §5 dedup protocol, C5
canonical P-space mapping / harness ingestibility, C6
independence from the CGSA derivation inputs.

Application (spec §4), on the established facts (published
aggregate tables; zero inscription-level records; the only
per-sign table, K1965-T4, a restricted stable-initial-pair ×
stable-final co-occurrence matrix in Marshall numbers, with
no occurrence denominators; no Marshall↔M/P map in the
frozen §3 map or on main): C1 FAIL (fits none of the six
§4 classes; inventing a class would amend the frozen
matrix), C2 FAIL (not the full ICIT database, and no
qualifying substitute), C3 FAIL (0/14 TERMINAL end_rates and
0/12 INITIAL start_rates computable as §6.2 defines them),
C4 FAIL (no token sequences; Stages A–C inapplicable in
principle), C5 FAIL (Marshall numbering unmappable under
the frozen map; no §7 adapter ingests aggregate tables), C6
PASS (narrow: its content was not a derivation input; the
icit_full caveat C1 does not apply).

VERDICT: **NO.** Scoring did NOT run — the Phase-119
harness was not invoked in evaluation mode, and no dry run
was performed. PRED-2026-001 and PRED-2026-002 remain
PENDING; an append-only adjudication note recording the
verdict and its reasons was added to
`docs/PREDICTION_REGISTER.md` §6 (registered entries
unmodified). No code changed. No anchor, claim, registry,
or language-model file changed; anchors file byte-identical
(sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed,
asserted before/after). Verification: full backend suite
867 passed / 12 skipped / 0 failed (baseline 867/12/0);
foundation check 40 passed / 0 failed / 8 warnings;
branding sweep over changed files clean.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## 2026-10-08 — Phase-126 (ledger sequence): Wells-Split Descriptive Analysis of the 113 CANDIDATE Anchors — DESIGN INPUT

Descriptive analysis only (owner-ordered program step 3,
2026-10-08). For each of the 113 anchors whose `confidence`
field is `CANDIDATE` in `backend/reports/INDUS_FINAL_ANCHORS.json`,
the Phase-123 Wells segmentation witness treatment
(`data/crosswalks/wells_segmentation_witness_v1.{csv,json}`;
semantics per `reports/phase123_wells_segmentation_witness.md`)
was recorded in this phase's vocabulary — SPLIT → split,
MERGE → merge, SAME → unit-same, NOT-COVERED → not-covered,
INDETERMINATE → indeterminate — with the split components
(the witness table's `wells_graphemes`) recorded per sign,
and cross-tabulated (counts only) against the evidence
features actually present in the anchors file for these
signs, named by exact field: the attestation count and
positional profile parsed from `basis` (all 113 record
I=0.000 / T=0.000 / M=1.000, medial-only; freq 1–4),
`source` (Phase-111 for all 113), `validation_status`
(`premise_superseded` for all 113), `_phase132_note`
presence (70 present / 43 absent), `phase109_annotation`
presence (109 / 4), and the Phase-252 cohort fields
`dedr` / `dedr_source` / `phase_upgraded` / `upgrade_basis`
(4 signs: M157, M256, M307, M400 — all unit-same).

Headline counts (of 113): **split 27 · merge 4 · unit-same 62 ·
not-covered 1 · indeterminate 19** — identical to the
Phase-123 memo's CANDIDATE breakdown, re-derived here from
the two committed inputs. Treatment determinable for 93/113.
Split sizes: 20 signs into 2 graphemes, 6 into 3, 1 (M120)
into 5 (025–029). Split components overlap across CANDIDATEs:
11 Wells graphemes appear in the split sets of two CANDIDATE
signs each (10 distinct signs involved), so the split sets
are not disjoint. Merge: M115 and M116 share W019, M245 →
W615, M389 → W805 (the glyph-route row carrying the recorded
Phase-123 conflict). Not-covered: M312 only; zero CANDIDATEs
are absent from the witness table (the builder records any
absent sign as not-covered by construction — counted and
listed, never dropped). Indeterminate: 19, each with the
witness's reason carried into the memo (M126 carries the
chain-only lead, stated conditionally as Phase-123 recorded
it). Cross-tab highlights: by `basis` freq — freq 1: split 1 /
unit-same 11; freq 2: split 8 / unit-same 14; freq 3: split
11 / unit-same 17; freq 4: split 7 / unit-same 20 /
not-covered 1; the four Phase-252-cohort signs are all
unit-same; witness `correspondence_method` for the 113:
REGISTRY 87, GLYPH 6, GLYPH-SEARCH-NEGATIVE 1, none recorded
19 (the indeterminate rows); Phase-123 hand-verification
covers 8 of the 113 (7 verified, all unit-same; 1
verified_with_conflict, M389, merge).

Output is a DESIGN-INPUT memo addressed to future battery
design (`reports/phase126_wells_split_candidates.md` +
`reports/phase126_wells_split_candidates_results.json`):
which CANDIDATEs are compound-suspects under Wells, which
are unit-confirmed, and where the witness is silent, stated
as facts a future spec may use. No adjudication of any
sign's status is phrased, no promotion or demotion is
proposed, and no anchor was changed: the anchors file is
byte-identical before and after (sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed,
asserted in code). The 44 `pending_non_sa_validation`
anchors were verified disjoint from the 113 and not touched.
Code: `backend/glossa_lab/phase126_wells_split.py` (pure
machinery), `backend/glossa_lab/phase126_run.py`
(orchestration + memo), `backend/scripts/phase126_wells_split_candidates.py`
(entry point), experiment-graph node
`IndusPhase126WellsSplitCandidates`
(`backend/glossa_lab/experiment_graph_phase126_wells.py`;
distinct from the legacy Phase-126 ICIT node family).
Deterministic builder: two runs byte-identical (md5-verified).
Verification: 16 new tests passed in isolation; full backend
suite 883 passed / 12 skipped / 0 failed (baseline 867/12/0
plus this phase's 16); foundation check 40 passed / 0 failed
/ 8 warnings (baseline unchanged); ruff clean on all
new/changed files; branding sweep over changed files clean.
Test side effects (glossa-indus/ claims + reports, outputs/,
foundation report) reverted before commit, per precedent.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## [2026-10-08] Entry — History purge #2 (revised scope): 1,935 historical-only restricted-derived paths removed

Owner decision (Tristen Pierson, 2026-10-08): recommendation (ii)+(iii) approved, following the hard stop of the full-scope purge #2 attempt at its verification gate (nothing was pushed in that attempt).

**Step A — owner re-adjudication (human adjudicator).** The contested E-CISI classification in the 2026-10-08 history adjudication is resolved: files derived from the MIT-licensed mayig digitization (mayig/indus-valley-script-corpus) — including the mayig corpus layer, crosswalk v1, the sign registries, and the Wells witness dataset as the program's own generated data files — are ruled OWN-WORK (the MIT license travels with the digitization; sign-numbering/segmentation facts are data). They are NOT purge-eligible and remain in the tree and history. The conservative E-CISI rule remains the recorded basis for everything not covered by this ruling. Recorded as a dated addendum to the adjudication record (local: `~/workspace/glossa-run/history-adjudication-20261008.md`).

**Step B — scope.** Exactly the 1,935 historical-only RESTRICTED-DERIVED paths of adjudication Appendix A (paths NOT present at HEAD; mechanically re-verified: Appendix A 2,766 = 831 at HEAD excluded + 1,935 in scope; scope list local: `purge2-revised-scope-20261008.txt`). No HEAD-resident file was touched; the HEAD tree is byte-identical before/after (tree `6bb5dd60e8dcdde6f93d39f195fbfd4a8071b002` both sides).

**Step C — rewrite + gates.** git-filter-repo over all 21 branches + 3 tags. Gates, all passed BEFORE pushing: (a) 0 objects for every purged path across all refs in a fresh bare clone; (b) backend suite 883 passed / 12 skipped / 0 failed and foundation check 40 passed / 0 failed / 8 warnings on the rewritten tree (baseline-identical); (c) `backend/reports/INDUS_FINAL_ANCHORS.json` sha256 unchanged (`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`); (d) HEAD tree byte-identical (see Step B). Protection: captured fresh, `allow_force_pushes` flipped on for the push only, restored verbatim — closing GET identical to the pre-purge capture.

**Result.** Old main `9ef78ca65d98449d2d781c5270cb478fa321ba2b` is historical-only. New main: `7c959a81a1450c916d57364e4cb534f9e4de2acf`. All pre-2026-10-08-purge-#2 SHAs are historical-only. Pre-purge backup retained locally only (`~/workspace/glossa-run/glossa-lab-backup-20261008-prepurge2.git`, main 9ef78ca6; not deleted — deletion needs its own future owner order). GitHub Support garbage-collection ticket for purge #2: filing prepared (text local: `purge2-gc-ticket-20261008.md`, pattern of ticket #4834257); the ticket number will be recorded in a follow-up entry once filed.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## 2026-10-08 — Phase-127 (Spec 021): Cross-Compilation Disagreement Diagnostic — Phase-125's disagreement is not sampling noise, ambiguity, or controlled composition

Diagnostic only (owner-ordered program workstream 1,
2026-10-08). Spec 021 was frozen in its own commit
(83252e45) before any diagnostic statistic existed. This
phase does NOT re-score Phase-125 and issues no verdict:
the Phase-125 verdict — **FAIL — DISAGREEMENT** (PRIMARY
arm: 16 judgeable pairs of 286; median TV 0.636931;
Spearman ρ initial −0.424758 / terminal 0.316034;
pairing-shuffle null p = 0.824) — is FINAL and unchanged.
All arms operate on exactly those 16 judgeable pairs,
read from the Phase-125 results of record, with the
Phase-113/125 profile/TV machinery reused unchanged;
inscriptions never pooled; no object-level join.

Headline decomposition (deterministic; two runs
byte-identical in statistics):
(a) Holdat split-half noise floor: raw median TV 0.059538
across the 16 signs; full-size estimate (÷√2, registered
multinomial scaling) **0.042100**.
(b) Matched-size subsampling (Holdat at mayig's token
counts, B = 999): expected median TV under pure
Holdat-internal sampling **0.082613** (95% interval
0.046665–0.131316); share of replicates reaching the
observed 0.636931: **0.000000**.
(c) Inscription bootstrap of both compilations
(B = 999): median TV 0.643877, 95% CI
**0.548638–0.722042** — the entire interval sits above
the frozen Phase-125 FAIL bound 0.50. Per-pair CIs in
the results JSON.
(d) Crosswalk decomposition: primary TVs contain zero
ambiguity by construction (spec 019 §3). Counterfactual
estimator (spec 021 §6): median ambiguity share 0.666667;
median attributable TV 0.000000, median attributable
share −0.185664 over the 7 pairs with a judgeable
neighbourhood comparison (9 pairs have none) — where
defined, the ambiguous alternatives disagree as much as
or more than the primary pairs, so ambiguity accounts
for none of the observed disagreement under this
estimator.
(e) Composition controls (Holdat-side restrictions;
mayig is entirely Mohenjo-daro unicorn seals): site =
Mohenjo-daro → median TV 0.599138 (13 judgeable);
iconography = unicorn → 0.650510 (13); both → 0.602896
(11). Zero stratum-inconsistent inscriptions. Gaps
stated in the report (unicorn variants I–V, finer
provenience, length composition — not controllable
from the mayig metadata, not improvised).
(f) Power: under the registered criterion (95th
percentile of sampling-noise median TV ≤ the frozen
PASS bound 0.35), **8 tokens per sign** suffice — the
grid's first point qualifies on both the median-gate
and per-sign criteria — so the frozen gates are
informative at the observed effect scale; the observed
median is ~4× the noise 95th percentile even at the
floor size.

Residual reading (spec 021 §9 vocabulary): at the
observed sizes, the disagreement is not accounted for
by sampling noise, crosswalk ambiguity, or the
controlled composition strata. No side or mechanism is
attributed; no anchor, PRED, or status changed; the
anchors file is byte-identical before and after (sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed,
asserted in code). One filename deviation, recorded in
the report per spec §11: the graph module is
`experiment_graph_phase127_diagnostic.py` (the plain
name is a legacy node family; Phase-126 Wells
precedent); the node id is as specified. One toy test
premise was corrected during development (independent
resamples of a varied corpus are not a zero-TV control;
replaced with a degenerate identical-inscription
control) — machinery unchanged.
Code: `backend/glossa_lab/phase127_diagnostic.py`,
`backend/glossa_lab/phase127_run.py`,
`backend/scripts/phase127_cross_compilation_diagnostic.py`,
graph node `IndusPhase127CrossCompilationDiagnostic`.
Artifacts: `reports/phase127_cross_compilation_diagnostic.md`
+ `_results.json`.
Verification: 18 new tests passed in isolation (stable
across PYTHONHASHSEED 0/1/42); full backend suite
901 passed / 12 skipped / 0 failed (main baseline
883/12/0 plus this phase's 18); foundation check
40 passed / 0 failed / 8 warnings (baseline unchanged);
ruff clean on all new/changed files. Test side effects
(glossa-indus/ claims, outputs/) reverted before
commit, per precedent.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-08 — Phase-128: Integrated Evidence Dossiers for the 44 Pending Anchors — every Phase-120–127 record, joined per sign, gaps recorded not filled

Descriptive only (owner-ordered program workstream 2,
2026-10-08). For exactly the 44
`pending_non_sa_validation` anchors in
`backend/reports/INDUS_FINAL_ANCHORS.json` (sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed,
read-only, asserted unchanged before/after), one dossier per
anchor joining on M-number: the anchor record; Phase-120
Bhaskar triage classification/subflag/detail/case ids;
Phase-123 Wells witness treatment, graphemes, correspondence
method and hand-verification, with the Phase-126 class
vocabulary applied as a labelled label-normalisation
(Phase-126's own analysis set was the 113 CANDIDATE anchors —
no Phase-126 record exists for a pending sign); every
Phase-122 crosswalk v1 row asserted for the sign (Parpola
ids, relation, confidence, conflict flags); the Phase-125
PRIMARY-arm record and judgeability; Phase-127 per-pair
diagnostic values where they exist; and a uniform spec-020
limitation field (Soviet dataset adjudicated non-qualifying —
NOT-EVALUABLE-VIA-SOVIET-DATASET — on every dossier, recorded
as a limitation, not per-sign evidence). Every block carries
a provenance pointer to its source file and row key; missing
join keys are recorded NOT-COVERED, never inferred
(crosswalk: M281 has no row; Phase-125 PRIMARY: 8 of 44
signs have no record).

Join integrity: 44 in = 44 out (asserted in code and tests).
Coverage pins: Bhaskar CONTESTED is exactly {M402} (43
NOT-COVERED); Phase-125 judgeable among the 44 is exactly
{M072} (pair P058-M072, bootstrap CI median 1.0); Wells
pending breakdown SAME 25 / SPLIT 13 / MERGE 1 /
NOT-COVERED 1 / INDETERMINATE 4 (matches the Phase-123
memo). Phase-127 global diagnostic values (matched-size
expected median TV 0.082613, 0.000000 of 999 replicates
reaching the observed 0.636931; bootstrap median-TV CI
0.548638–0.722042) are recorded once in the JSON document;
the Phase-125 FAIL — DISAGREEMENT verdict is final and
unchanged.

Triage buckets (deterministic rules stated in the report
BEFORE membership; buckets 1–4 are independent predicates
and may overlap; evidence-thin is the defined residual):
evidence-complete 1 (M072 — wells_determinate ∧ crosswalk
present ∧ Phase-125 record ∧ Phase-127 pair);
segmentation-contested 15 (Wells SPLIT/MERGE or a recorded
verification discrepancy); crosswalk-contested 25 (any
crosswalk row conflict); not-covered 3 (M033, M058, M281 —
Bhaskar NOT-COVERED ∧ Wells NOT-COVERED/INDETERMINATE ∧ no
Phase-125/127 record); evidence-thin 10 (residual). The
report states plainly what the dossier cannot do: Bhaskar
covers 1/44; the Phase-125 judgeable subset is 16 of 286
pairs (1 of the 44 anchors); spec 020 closed the Soviet
route. No status recommendation, no adjudication, no PRED
content; no anchor changed.

Code: `backend/glossa_lab/phase128_dossiers.py`,
`backend/glossa_lab/phase128_run.py`,
`backend/scripts/phase128_evidence_dossiers.py`.
Artifacts: `reports/phase128_evidence_dossiers_44.json` +
`.csv` (flat rendering) + `.md` (synthesis). Builder
deterministic (two runs, PYTHONHASHSEED 0/42, byte-identical
outputs). Verification: 16 new tests passed; full backend
suite 916 passed / 13 skipped / 0 failed locally (913-test
baseline total preserved: 900/13 no-Holdat baseline + 16
new; see the Phase-127 count correction entry below);
foundation check 40 passed / 0 failed / 8 warnings
(baseline unchanged); ruff clean on all new files. Test
side effects (glossa-indus/ claims, outputs/) reverted
before commit, per precedent.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-08 — CORRECTION (append-only): Phase-127 suite count reconciled — 901/12 recorded vs 900/13 verified local re-run; total 913 in both; CI green

Correction to the Phase-127 entry above (appended, not
edited): its recorded suite count of 901 passed / 12 skipped
reflects a run with the gitignored Holdat CSV copy present;
the verified local re-run without that copy was 900 passed /
13 skipped / 0 failed, because the Holdat-dependent
foundation-script test skips when the gitignored Holdat CSV
copy is absent. Total is 913 in both counts; CI was green.
No other Phase-127 figure is affected.

## 2026-10-08 — Release-integrity audit (Zenodo v4.2.0) + release hash gate (owner-ordered program WS3)

Audit (`reports/release_integrity_audit_v420.md`): verdict
(i) STAGING ERROR. From the Zenodo records themselves
(API via the custom.zenodo route): v4.2.0 = record 23223655,
DOI 10.5281/zenodo.23223655, created 2026-10-07T22:12:48Z
(publication_date 2026-10-07 — correcting the program
record's 2026-10-08); its deposited
`INDUS_FINAL_ANCHORS.json` is 391,969 bytes, record MD5
b6eb0823…, downloaded sha256 841e9067…. v4.3.0 (record
23250395, created 2026-10-08T23:25:25Z) deposits
eccea6d5…, byte-identical to the repo file. Git history:
70 distinct content versions of the anchors file on
mainline in BOTH the current history and the pre-purge
backup mirror (identical sets); 841e9067… matches 0/70 in
either, and no blob of size 391,969 exists in either
object store. The deposited file's parsed JSON is exactly
commit bbecc1cd (2026-05-27, "AUDIT: Revert Phase 312 kol
mass-assignment"; backup twin f302fa68; sha256 569e51a7…,
605 anchors, 400 HIGH / 205 LOW); its only byte
difference from that commit is CRLF line endings (6,054
CRLF, 0 bare LF; LF-normalised sha256 = 569e51a7… exactly)
— a stale Windows working-tree copy, not a git blob. That
content left the repo 2026-06-05; eccea6d5… was
established 2026-10-06 11:46 UTC by Phase-110 Part B
(0ce70794), over a day before the deposit. Verdict (ii)
is falsified (no post-deposit — indeed no post-2026-10-06
— changing commit); no deposit was edited and no new
release was made.

Gate: `backend/scripts/release_gate.py` (offline,
stdlib-only) — manifest (JSON/YAML) maps each deposit
filename to a repo source or an explicit external-source
note; hashes staged + source on raw bytes, prints a
per-file MATCH/MISMATCH/MISSING/EXTERNAL table, exits
non-zero on any mismatch/missing (2 on malformed
manifest). `docs/RELEASE_CHECKLIST.md` makes the gate a
mandatory blocking step, incl. recording the gate output
into the release record per RELEASE_VALIDATION practice
and post-deposit provider-checksum confirmation. Tests:
7 new in `backend/tests/test_release_gate.py` (matching
set passes; one-byte mutation fails; missing source
fails; missing staged fails; external-source entry as
specified; malformed manifest exit 2; CRLF drift fails).
Verification: full backend suite in a fresh worktree
908 collected at origin/main baseline → 915 with this
work; run 910 passed / 6 skipped / 0 failed (skip/pass
split differs from the main-checkout baseline because
the gitignored corpora are absent, as in CI); foundation
check 40 passed / 0 failed / 8 warnings (baseline
unchanged, run with the Holdat copy linked in); ruff
clean on new files. Anchors file byte-identical
before/after (sha256 eccea6d5…, asserted).

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-08 — Phase-129: CISI Cropper v2 — benchmarked win on the frozen Phase-124 sample, gated expansion run (enabling asset)

Owner-ordered program workstream 4, 2026-10-08. Protocol frozen
BEFORE any tuning at commit 8a85c55f
(reports/phase129_cisi_cropper_v2_protocol.md): the benchmark is
Phase-124's 82-crop worked sample identically (same 200-dpi
renders, same photo boxes from the local store's
crops/verification.csv — 34 distinct photo boxes spanning the 32
ID+side groups Phase-124 counted), graded under the Phase-124
rubric verbatim, v1's grades frozen at 38 good / 29 partial /
15 bad (never re-graded); "v2 beats v1" := good > 38 AND bad <= 15
AND 41 <= total <= 123. v2 (backend/glossa_lab/cisi_cropper_v2.py)
keeps v1's column-std core signal and adds illumination
normalisation, sharper projection smoothing (2.0% vs 4.5%),
valley-capped hysteresis edges, valley splitting, a stroke-content
rejection gate and fitted crop heights — deterministic, CPU,
numpy+Pillow only. Two correctness defects were found and fixed
before grading, each pinned by a test (box-blur cumsum slicing;
y-fit capture by photo border rows).

Result: v1 boxes reproduced exactly by the untouched v1 segmenter
(harness assertion); v2 graded **50 good / 42 partial / 15 bad of
107** under the same rubric (manual pass; 15 ambiguous crops
re-examined at full resolution in photo context, changes in both
directions). All three frozen clauses met — v2 beats v1, as a
recall win at constant bad count and constant good rate, not a
precision claim. Correspondence (x-overlap >= 50%): of v1's goods
27 stayed good, 8 -> partial, 3 dropped; 9 partial -> good;
2 bad -> good; per-crop regression list in
reports/phase129_cisi_cropper_v2.md. Per-crop v2 grades live ONLY
in the local store (crops_v2/verification_v2.csv).

Expansion (gate opened by the win): v2 over the full Phase-124
catalogue (side A/a, non-degenerate box, benchmark photos
excluded): 5,247 photos -> **14,166 crops** (Vol. 1 6,438 /
Vol. 2 7,728), 3,287 distinct CISI IDs, local store only
(crops_v2_expansion/); manifest == disk exactly (14,166 unique
filenames). A first expansion attempt was discarded (exclusion
matched only 4/34 benchmark photos — round() vs the v1 driver's
int() truncation — and 7 filename collisions from
re-photographed exemplars); harness fixed + uniqueness asserted.
Seed-129 spot-check of 30 expansion crops (context only):
8 good / 10 partial / 12 bad — the pool covers all object types
at 140 dpi, not only seal plates.

Verification: 12 new tests passed; full backend suite 923 passed
/ 13 skipped / 0 failed; foundation check 40 passed / 0 failed /
8 warnings (baseline unchanged, corpora symlinked from the main
checkout); ruff clean; anchors file byte-identical (sha256
eccea6d5…, asserted before/after). No image, crop, render or
per-crop grade in git (git check-ignore + git status verified).
Reports: reports/phase129_cisi_cropper_v2.md +
reports/phase129_cisi_local_store_manifest.json (counts/schema
only).

**AI disclosure:** execution recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## [2026-10-08] Entry — Phase-130 (Spec 021): Independent-Data Intake Pack

Owner-ordered program Workstream 5 of 5 (2026-10-08), on
`phase/130-intake-pack` from main `9f0ec4da` (after PR #92).
The intake-side companion to spec 018 (Phase-119): the
machinery that receives a genuinely independent inscription
dataset when one lands. **No real external data was
ingested, no one was contacted, nothing was sent**; the only
end-to-end exercise is a synthetic fixture (invented signs
P901–P905, invented sites).

Deliverables. (1) Intake schema v1
(`data/intake/intake_dataset_schema_v1.json`, JSON Schema
draft 2020-12): per-inscription source-assigned ID, site,
object type, context/period, token-list sign sequence,
declared sign list, per-inscription provenance; dataset-level
source, compiler, license/terms basis, acquisition date,
upstream lineage declaration. REQUIRED = exactly the fields
spec 018's evaluability (§4/§6.1) and dedup (§5) consume; the
rest is optional-but-declared. The enforcing validator is
stdlib-only Python (repo precedent: core modules stdlib-only,
pydantic confined to the API layer, `jsonschema` not a
dependency); tests assert schema file and validator agree.
(2) Validator (`backend/glossa_lab/intake.py`): structured
pass / pass-with-warnings / reject verdicts with named reason
codes, including duplicate-ID detection and sign-list
declaration. The license gate is hard: a dataset with no
declared lawful basis (missing/empty `license_basis`) is a
REJECT (`LICENSE_BASIS_MISSING`), never a warning.
(3) Dedup lifted verbatim from `pred_harness` into the shared
module `backend/glossa_lab/dedup.py`; the harness imports and
re-exports it (identity asserted in tests) — no behaviour
change: Phase-119's tests pass unmodified in outcome, and the
Appendix A.6 measured numbers reproduce through the module on
the harness's fixtures and on the converted layer itself
(4,531 in; stages 1,468 / 370 / 247; kept 2,446; cumulative
removal 46.02%, the P-space figure of App. A.6). Note: the
tasking memo's alternate dedup stage names matched no repo
protocol; the frozen spec 018 §5 stages (A exact / B
sentinel-normalized / C near-duplicate) are what was lifted —
recorded in spec 021 §B2. (4) Crosswalk adapter requirements
(`docs/INTAKE_CROSSWALK_REQUIREMENTS.md`, requirements only,
no crosswalk built): evidence types, confidence-rubric
inputs and conflict handling after the Phase-122 v1 model.
(5) Intake runbook (`docs/INTAKE_RUNBOOK.md`): provenance →
license gate → schema validation → dedup → evaluability-class
assignment (spec 018 §4) → harness dry-run, headed by the
structural rule: intake output can only ever reach the
harness's dry-run path (the intake module imports `dry_run`
and binds no scoring name — asserted in tests); evaluation
requires its own future spec + owner authorization.

Fixture exercise (15 new tests): the synthetic dataset walks
every runbook stage; its deliberate duplicate cluster is
caught one per stage (7 in → 4 kept); the license-missing
variant fixture is rejected at the license gate with no dedup
or dry-run stage reached; a non-Parpola declared sign list
stops at the dry-run stage with the §7-adapter skip reason.

Reports: `reports/phase130_intake_pack_results.json`;
graph node `IndusPhase130IntakePack`
(`backend/glossa_lab/experiment_graph_phase130_intake.py`,
registered by try/except import; distinct from the legacy
Phase-130 decode-blocker node). Verification: 15 new tests
passed; full backend suite 938 passed / 13 skipped / 0 failed
(baseline 923/13/0 plus this phase's 15; corpora symlinked
from the main checkout per Phase-129 precedent); foundation
check 40 passed / 0 failed / 8 warnings (baseline unchanged);
ruff clean on all new/changed files; anchors file
byte-identical (sha256 eccea6d5…, asserted before/after).
Test side effects (glossa-indus/ claims + reports, outputs/)
reverted before commit, per precedent.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## 2026-10-09 — CORRECTION (append-only): Phase-130 suite skipped count corrected — 13 → 5; 938 passed / 0 failed unchanged

Correction to the Phase-130 (Spec 021) entry above (appended,
not edited; part of the 2026-10-08 follow-on program
closeout): its recorded suite line "938 passed / 13 skipped /
0 failed" is corrected — the skipped count is corrected from
13 to 5. The verified re-run settles the suite at 938 passed
/ 5 skipped / 0 failed (943 collected in that worktree
environment). Passed (938) and failed (0) were correct; only
the skipped count was wrong. Skip counts vary by worktree
environment (gitignored corpora presence). CI was 7/7 green.
No other Phase-130 figure is affected.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## 2026-10-09 — Phase-131 (Spec 022): Source-of-Disagreement Attribution — direction and composition explain almost none of it; the matched-object route is nearly empty and the residual stands at 0.938679 unexplained

Attribution diagnostics ONLY (owner-ordered Glossa-Lab
program STEP 1, 2026-10-09). Spec 022 was frozen in its
own commit (b2ff5759, on phase/131-attribution from
origin/main 7c062ddf) before any Phase-131 attribution
statistic existed; the only pre-freeze numbers are
Phase-125/127 facts of record and Appendix A
join-feasibility counts. This phase does NOT re-score
Phase-125 and issues no verdict: the Phase-125 verdict
— FAIL — DISAGREEMENT (16 judgeable pairs; median TV
0.636931) — is FINAL and unchanged, and spec 020's NO
stands untouched. No anchor, PRED, or status changed;
anchors sha256 eccea6d5… asserted unchanged before and
after. Work was done in a dedicated worktree; the main
checkout's stale working tree was never touched.

Arm A (matched-object alignment): every join stage
counted as found. S1 CISI-ID: 179 apparent zero-padded
namesakes / 0 validated — rejected as non-identity
(Holdat cisi_number is internal sequential numbering,
spec 019 §2.1); no S1 join performed. S2 catalogue
cross-references: 0. S3 shared artifact keys: 0. S4
content matcher (Phase-116 route; primary crosswalk
map, 286 pairs): 32/179 mayig inscriptions eligible
(all tokens primary-mapped; token-weighted coverage
0.725823); Tier EXACT / EXACT-REV matches: 0; matched
set = 4 pairs (NEAR 1, NEAR-REV 3; similarity
0.667–0.750; ambiguous-orientation excluded 0).
Pair classes over the 4: substitution 2,
insertion-deletion 2, identical / split / merge /
order-only 0. Difference blocks: substitution 2
(4 tokens), insertion-deletion 2 (2 tokens); all 4
pairs are the concrete examples (fewer than 3 per
class exist beyond those shown). Matched-object
median TV: NOT ESTIMABLE under the frozen gate
(matched 4 < MIN_MATCHED 10; 5 of 16 pairs have
defined matched TVs; unthresholded median over those
5 = 0.500000). The near-empty join is a finding: under
the only legitimate join, the two compilations' texts
essentially do not coincide.

Arm B (reading direction; diagnostics, not a
re-score): B1 mayig reversed median TV 0.582205;
B2 Holdat reversed median TV 0.582205 — the arms
coincide exactly, per pair, because TV is symmetric
under the INITIAL↔TERMINAL swap. Reduction vs
observed: 0.054726. Neither arm meets the frozen
support criterion (median TV ≤ 0.131316, the Phase-127
matched-size noise band's upper bound; band median
0.082613, interval [0.046665, 0.131316]). Direction
share credited: 0.000. The unreversed control
reproduced the Phase-125 median 0.636931 exactly
through this phase's code path (machinery check).

Arm C (stratification; floor 8 re-applied in-stratum;
estimable iff ≥ 4 judgeable pairs): site —
Mohenjo-daro ESTIMABLE (179 mayig / 606 Holdat
inscriptions, 13 judgeable, median TV 0.599138; same
value as Phase-127's site control through the new code
path); all 8 other Holdat sites NOT ESTIMABLE
(mayig-empty, counts reported). Object type — unicorn
III ESTIMABLE (5 judgeable, 0.663366), unicorn IV
ESTIMABLE (6, 0.628981); unicorn I/II/V NOT ESTIMABLE
(0/1/0 judgeable); all 8 non-unicorn Holdat
iconographies NOT ESTIMABLE (mayig-empty). Text
length — bin 6+ ESTIMABLE (9 judgeable, 0.512903);
bins 1 / 2-3 / 4-5 NOT ESTIMABLE (0/1/2 judgeable;
bin 1 has 0 Holdat inscriptions). Period: NOT
ESTIMABLE in every cell (no period metadata exists on
either side). Zero stratum-inconsistent inscriptions.
Composition adjustment (Holdat profiles reweighted to
the mayig length composition; 16/16 pairs included):
adjusted median TV 0.597874 → composition share
0.061321.

Arm D (synthesis; frozen estimators): segmentation
NOT ESTIMABLE, substitution NOT ESTIMABLE,
insertion-deletion NOT ESTIMABLE (all gated on the
4-pair matched set), order/direction 0.000 (ESTIMABLE,
no support), composition 0.061321 (ESTIMABLE),
matched-object residual NOT ESTIMABLE. Sum of credited
explained shares 0.061321; residual unexplained share
0.938679 — stated plainly: no registered estimator
accounts for the remaining disagreement. Shares not
forced to sum to 100%; overlaps stated, not rescaled.

Deviations: one clarification (NEAR ties for best
similarity disqualify a pairing — a tied best is not
the best) and one presentational note (Appendix A's
0.717 was a per-inscription mean coverage; the run
reports the token-weighted 0.725823), both recorded in
the report. Deterministic: two runs identical in
statistics. Verification: 32 new tests passed; full
backend suite 982 passed / 13 skipped / 0 failed
(baseline 950/13/0 plus this phase's 32); foundation
check 40 passed / 0 failed / 8 warnings (baseline
unchanged; corpora symlinked from the main checkout
temporarily); ruff clean on all new/changed files;
graph node IndusPhase131Attribution registered and
asserted in ATOMIC_NODES before the run (H23). Test
side effects (glossa-indus/ claims + reports, outputs/)
reverted before commit, per precedent.

**AI disclosure:** execution recorded by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

## 2026-10-09 — Zenodo v4.4.0 published (Phases 127–131, specs 021–022) + OSF registry update — owner-ordered program STEP 2

Publication: Zenodo **v4.4.0**, record **23261517**, DOI
**10.5281/zenodo.23261517** (concept DOI
10.5281/zenodo.20379070), published 2026-10-09. New version
created from the v4.3.0 record 23250395 via the API route
(custom.zenodo connector); the draft carried no `dates`
stub (checked: null), all 8 inherited files were deleted
and the 9-file curated set was uploaded fresh from the
gated staging directory, metadata set to version 4.4.0 /
publication_date 2026-10-09 with a description summarising
the 127–131 outcomes, negatives verbatim (Phase-131
residual unexplained 0.938679; direction NOT supported,
share 0.000; matched-object TV NOT ESTIMABLE).

Release sources (PR #96, merged 2eb7e82d; gate-record PR
#97, merged 8f396348; both 7/7 CI green before merge):
new program note
`glossa-corpus/indus/pierson_2026_indus_program_note_127_131.md`
(precedent location of the pierson_2026 notes) covering
Phases 127–131 + specs 021/022 with all outcomes verbatim;
the v4.3.0 program note 120_126 — deposited at v4.3.0 but
never committed — was committed with its exact deposited
bytes (sha256 2d61c136…, md5 ee339733…) so the gate has a
repo source for it; `outputs/RELEASE_VALIDATION.json`
restored the release_v4_3_0 entry exactly as deposited and
gained a release_v4_4_0 entry (Phase 127–131 outcomes;
suite re-verified at 257ed964: 970 passed / 5 skipped /
0 failed, CI configuration in the release worktree —
Phase-131 ledger record 982/13/0 stands as that phase's
own-environment count, and GitHub CI run 37915340386 on
the merge commit was green; foundation check re-verified
40 passed / 0 failed / 8 warnings).

Mandatory release gate (docs/RELEASE_CHECKLIST.md),
`backend/scripts/release_gate.py`, manifest 9 entries,
run against the final merged tree (source commit
**8f39634868f8bd09b4b69b2c4d3d820473dd95dd**; phase-results
source 257ed964dfcc8d4c7068e01308efd8532bdaa65b):
**PASS — 9/9 entries OK, 0 failed**, exit 0.
Per-file (staged sha256 == source sha256 for every MATCH):

| File | Status | sha256 |
|---|---|---|
| RELEASE_VALIDATION.json | MATCH | c78591f65770d86bf6b5e8c562d59bee7604b01a0c1b68e2f2e031bc8a87076b |
| INDUS_FINAL_ANCHORS.json | MATCH | eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed |
| pierson_2026_indus_program_note_127_131.md | MATCH | 326f88072ba2382cfd7c3ffe320e77fb9ce1357cbf9e9455f55793292ac864a5 |
| pierson_2026_indus_program_note_120_126.md | MATCH | 2d61c13647d84426d9a32c83aa2055c5eb8cd220de3254ac4db95b09e41bd4d6 |
| pierson_2026_indus_harmonization_note_116.md | MATCH | a7236ce058cbb36ac737f970f0e786f9ab6f24c92d1dbd0828725332433fcf92 |
| pierson_2026_indus_methods_note_111_112.md | MATCH | fdcd47704a8e023daaa81d560af79ed0af5b4115f54925600c02c71fa8dee830 |
| pierson_2026_indus_decipherment_addendum_v5.md | MATCH | b2818df804402e2e76bdcea53000b806eb7a36442ff6270e437da53e8fc7a8dc |
| AUDIT_CORRECTIONS.json | MATCH | 567ff7ada347c083b633d8b6709a8620832d3ffe9c1a6e67f07bcb31d9582a80 |
| pierson_2026_indus_preprint_v3.pdf | EXTERNAL | cfa25287b30958e024988a1bf280266d880b07d3feef2215e892315bdcd0162a |

The EXTERNAL entry is the built preprint v3 PDF, carried
forward byte-identical from v4.3.0 (its repo has the v4
PDF + stable .tex, not the v3 build). One carried-forward
note: AUDIT_CORRECTIONS.json is deposited as the repo's LF
bytes (md5 c0202c43…); the v4.3.0 deposit carried a CRLF
serialisation of the same content (md5 31de5453…) —
content identical after CRLF→LF normalisation (verified);
the checklist's clean-checkout rule governs. All other
carried files are md5-identical to the v4.3.0 deposit.

Post-deposit confirmation (checklist §4): the published
record 23261517 was re-pulled from the Zenodo API; its
9 files' record MD5s each equal the gated staged files'
MD5s — RELEASE_VALIDATION.json 144deea4f8c9dca1b07e64b2fc3eac41;
INDUS_FINAL_ANCHORS.json 00fde4dbf2ee6cbf96d020cba12ce043;
note 127_131 0350788f6912e8c72d463ecccb9ba9bb; note
120_126 ee3397333bd11eea155b983f6293fa89; harmonization
90d6b442fb8be605ccba2acbfcab67d6; methods
864369942b58dbac1c73f3ffa4a73845; addendum
48da2a8462eb5eb881057a18a3f2cbe1; AUDIT_CORRECTIONS
c0202c43dfc6ae3c83ca39e52f75e012; preprint v3 PDF
b552851dbf86a8edebeb9f84d982d878. 9/9 confirmed.

OSF: the provenance registry https://osf.io/ybd65/ was
updated with dated 2026-10-09 blocks (appended, not
restructured) on the parent node (ybd65) and the outputs
component (vwa7s, outcomes verbatim) and the corpora
component (dfrhz: no new corpus ingested; 14,166
Phase-129 crops local-only; Phase-130 intake pack,
synthetic fixture only), each verified by re-reading
after the update; the literature component (zbh86) was
left unchanged — Phases 127–131 used no new literature
sources. No anchor, PRED, or status changed by this
release; anchors sha256 eccea6d5… throughout.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-09 — Phase-132 (Spec 023): Keyed Transcription Layer, Stage P Pilot — the frozen stop-rule FIRED (exact-sequence agreement 0.20 < 0.80); build stops, no tranche proposed, no dataset publication

Spec 023 was frozen 2026-10-09 on the owner's instruction
of record (Tristen Pierson — "merge #99 and execute the
new plan"), answering all five §11 decision asks with
the proposed values as drafted; freeze + merge in PR #99.
The Stage P pilot build followed in PR #100 (merged at
main c789f7ad): deterministic 50-object frame over the
CISI Vol. 1–2 catalogue (Mohenjo-Daro 25 / Harappa 15 /
Lothal 6 / Kalibangan 4; Seals 34 / Tablets 11 /
unrecorded 5, counted from the frame records; mayig
overlap 10, all Mohenjo-Daro — the mayig layer resolved
176 MD / 3 site-uncaptured / 0 elsewhere, so the mayig
sub-quotas were corrected pre-transcription to MD 10 /
H 0 / LK 0, commit 33cb4c86; gold sample 10, seed
20261009; ambiguity log EMPTY, no exclusions; 10 key
disagreements logged and ruled from the plates, plate
reading governing). Two blinded passes plus a gold pass
and adjudication were executed by AI agents in
role-isolated blinded instances (each pass split across
5 batch instances); blindness held throughout.

Verdict, as found: the frozen pilot STOP-RULE FIRED —
exact-sequence inter-pass agreement (all 50 objects,
P space) = 0.20 (10/50), below the 0.80 floor. The
error arm did not fire (gold estimator 0.05 = 2/40;
frozen condition is > 0.05). Per spec §3.1 the build
STOPS: no tranche is proposed. Release gates (gold
scope) ALL FAIL — (i) exact-sequence 0.10 < 0.90,
(ii) per-token 0.4286 < 0.95, (iii) estimator 0.05 >
0.02 — so NO dataset publication occurs; the
owner-approved CC BY 4.0 route is not exercised and
the dataset JSON in data/keyed_transcription/ is the
in-repo build record only. A stopped pilot is a
result (spec §3.1).

Measurements (all computed from the on-disk records by
backend/scripts/phase132_metrics.py; reports/
phase132_pilot_metrics.json): exact-sequence agreement
P/M all-50 = 0.20/0.20, gold = 0.10/0.10; per-token
P/M all-50 = 0.4798 (95/198), gold = 0.4286 (18/42);
gold estimator P/M = 0.05 (2/40), with its frozen
limitation (errors identical across all three passes
are invisible). Tokens: pass_a 191, pass_b 190, gold
40, adjudicated final 189 (mean 3.78 / median 4 per
object; mayig reference ≈5.6). UNK shares: A 39.3%,
B 38.9%, gold 42.5%, adjudicated 40.7%;
crosswalk-unmapped adjudicated 8.5%; UNK+unmapped
adjudicated 49.2% — exceeding spec §7's 25%
NOT-EVALUABLE unmapped-share boundary as a property of
this layer; crosswalk-conflict tokens adjudicated 69.
Attestation (§7): P125 attested (1 token), P076 NOT
attested, P000 NOT attested. Intake validator
pass-with-warnings (0 errors, 21 warnings:
TOKEN_FORMAT_MISMATCH ×10, EMPTY_TOKEN_SEQUENCE ×6,
RECOMMENDED_FIELD_MISSING ×5); license gate pass (not
a release — the §5.6 gates failed); dedup 50 → 39 kept
(stage A −8, stage B −3). Evaluability by class
QUALIFIES for PRED-2026-001/002/003 (4 sites) — class
qualification only; no evaluation run or implied.

Deviations and findings, named plainly: (a) pass_b
batch 2 used the 200-DPI page renders (page_cache_200)
for several Vol. 2 objects after page-render access
failures, plus a self-made tighter re-crop for M-195 —
plate-only sources throughout, no external
transcription consulted; (b) two-sided-tablet B-face
ordering was flagged by passes and ruled at
adjudication (disagreement taxonomy: identity 93,
legibility 45, count 11, key 10, orientation 2,
order 1; total 162; only 5/50 objects had zero
disagreements); (c) PROCESS FINDING: several pass batch
self-reports' token tallies disagreed with the on-disk
records they wrote — every quantity in the pilot
report is computed from the on-disk records, never
from self-reports; (d) 6 objects have empty final
sequences as found (cisi:v1:M-566, cisi:v2:M-1542,
cisi:v2:H-886, cisi:v2:Pk-24, cisi:v1:K-21,
cisi:v1:K-88).

Effort (the pilot's explicit product): pass_a median
51.5 s/object (mean 66.68, total 3,334 s); pass_b
median 70 (mean 76.36, total 3,818); pass_gold median
110 (mean 97.9, total 979); adjudication median 30.5
(mean 38.9, total 1,945); all-in total 10,076 s ≈
201.5 s/object; 53.3 s per final token.

Stage T: this report makes NO Stage T recommendation.
The measured unit quantities are the inputs to the
owner's separate Stage T decision (spec §11 ask 2 /
tasks T9); spec §10(b) (commissioned external
transcription) is the alternative the spec names when
pilot gates fail, now askable with pilot numbers in
hand. Interpretation discipline (§8): the pilot
measured THIS pipeline — AI transcribers, these plate
renders, the Mahadevan-1977 drawings as the
identification reference — failing the frozen gates;
it does not measure expert human transcription, bears
on no anchor reading, and changes no PRED verdict.
Anchors sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed
asserted unchanged. Pilot report:
reports/phase132_pilot_report.md. Graph node
IndusPhase132PilotMetrics registered (additive module
backend/glossa_lab/experiment_graph_phase132.py + one
registry block, H23 pattern).

**AI disclosure:** all roles (pass_a, pass_b, pass_gold,
adjudicator) and this record were executed by AI agents
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-09 — Zenodo v4.5.0 published (Spec 023 + Phase-132 closeout) + OSF registry update — owner-ordered program ITEM 1

Publication: Zenodo **v4.5.0**, record **23266588**, DOI
**10.5281/zenodo.23266588** (concept DOI
10.5281/zenodo.20379070), published 2026-10-09. New version
created from the v4.4.0 record 23261517 via the API route
(custom.zenodo connector); the draft carried no `dates`
stub (checked: null), all 9 inherited files were deleted
and the 10-file curated set was uploaded fresh from the
gated staging directory, metadata set to version 4.5.0 /
publication_date 2026-10-09 with a description summarising
the Spec 023 / Phase-132 outcomes, negatives verbatim
(frozen stop-rule FIRED — exact-sequence agreement 0.20
vs the 0.80 floor; release gates all fail; pilot dataset
NOT published; program closeout to watch-and-respond).

Release sources (PR #102, merged 4ff4cca2; gate-record
PR #103, merged 573412cb; both 7/7 CI green before
merge): new program note
`glossa-corpus/indus/pierson_2026_indus_program_note_132_closeout.md`
(precedent location of the pierson_2026 notes) covering
Spec 023 + Phase-132 with all outcomes verbatim plus the
program closeout statement; `outputs/RELEASE_VALIDATION.json`
gained a release_v4_5_0 entry (Spec 023 / Phase-132
outcomes + program closeout; suite re-verified at
a6577d7f: 994 passed / 12 skipped / 0 failed, CI
configuration in the release worktree — GitHub CI run
37942349547 on the a6577d7f merge commit was green;
foundation check re-verified 40 passed / 0 failed /
8 warnings in the same worktree).

Mandatory release gate (docs/RELEASE_CHECKLIST.md),
`backend/scripts/release_gate.py`, manifest
release_manifest_450.json (10 entries), run against a
clean checkout of the final merged tree (source commit
**573412cbac0b75e09bfb52b171e0f07f17ae42cb**; release
sources 4ff4cca2; phase-results sources c789f7ad and
a6577d7f): **PASS — 10/10 entries OK, 0 failed**,
exit 0. Per-file (staged sha256 == source sha256 for
every MATCH):

| File | Status | sha256 |
|---|---|---|
| RELEASE_VALIDATION.json | MATCH | e67d14659406d6da67e4f300ca65a5c7aec5b36447710b7539123bfdf4d74536 |
| INDUS_FINAL_ANCHORS.json | MATCH | eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed |
| pierson_2026_indus_program_note_132_closeout.md | MATCH | d88f0a9b4526c31bce36223bdc91b55be81677ad683378db31da6fccd8eb8729 |
| pierson_2026_indus_program_note_127_131.md | MATCH | 326f88072ba2382cfd7c3ffe320e77fb9ce1357cbf9e9455f55793292ac864a5 |
| pierson_2026_indus_program_note_120_126.md | MATCH | 2d61c13647d84426d9a32c83aa2055c5eb8cd220de3254ac4db95b09e41bd4d6 |
| pierson_2026_indus_harmonization_note_116.md | MATCH | a7236ce058cbb36ac737f970f0e786f9ab6f24c92d1dbd0828725332433fcf92 |
| pierson_2026_indus_methods_note_111_112.md | MATCH | fdcd47704a8e023daaa81d560af79ed0af5b4115f54925600c02c71fa8dee830 |
| pierson_2026_indus_decipherment_addendum_v5.md | MATCH | b2818df804402e2e76bdcea53000b806eb7a36442ff6270e437da53e8fc7a8dc |
| AUDIT_CORRECTIONS.json | MATCH | 567ff7ada347c083b633d8b6709a8620832d3ffe9c1a6e67f07bcb31d9582a80 |
| pierson_2026_indus_preprint_v3.pdf | EXTERNAL | cfa25287b30958e024988a1bf280266d880b07d3feef2215e892315bdcd0162a |

The EXTERNAL entry is the built preprint v3 PDF, carried
forward byte-identical from v4.4.0 (record md5
b552851dbf86a8edebeb9f84d982d878; the repo holds the v4
PDF + stable .tex, not the v3 build).

Post-deposit confirmation (checklist §4): the published
record 23266588 was re-pulled from the Zenodo API; its
10 files' record MD5s each equal the gated staged
files' MD5s — RELEASE_VALIDATION.json
0dd6f48ba071252fc61dcb725cb9c2d8; INDUS_FINAL_ANCHORS.json
00fde4dbf2ee6cbf96d020cba12ce043; note 132_closeout
093ae180ac7a3c9cd44421ca69a8159f; note 127_131
0350788f6912e8c72d463ecccb9ba9bb; note 120_126
ee3397333bd11eea155b983f6293fa89; harmonization
90d6b442fb8be605ccba2acbfcab67d6; methods
864369942b58dbac1c73f3ffa4a73845; addendum v5
48da2a8462eb5eb881057a18a3f2cbe1; AUDIT_CORRECTIONS
c0202c43dfc6ae3c83ca39e52f75e012; preprint v3 PDF
b552851dbf86a8edebeb9f84d982d878. 10/10 confirmed.

OSF registry (osf.io/ybd65) updated the same day: dated
v4.5.0 blocks appended to the parent project and to
Components 1 (Outputs, vwa7s) and 2 (Corpora, dfrhz),
each verified by re-reading; Component 3 (Literature,
zbh86) unchanged — no new literature was used.

**AI disclosure:** this entry and the release execution
were performed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution §VI.

## 2026-10-09 — Indus program posture: WATCH-AND-RESPOND (owner decision)

Owner decision (Tristen Pierson, 2026-10-09): the
Indus program is set to **watch-and-respond** posture.
This entry records the closed lines, the named
triggers, the response path, and the standing state.

**(a) CLOSED LINES.**
(i) *Within-compilation validation batteries* — already
closed 2026-10-07 (see the closure entry of that date;
cross-referenced here, not re-closed): specs
011/014/016/017 (Phases 113/115/117/118) all rejected
at their calibration gates; no anchor ever received a
within-compilation validation; no further battery
redesign is authorized.
(ii) *Cross-compilation positional attribution* —
CLOSED. The Phase-125 verdict (FAIL — DISAGREEMENT)
stands final. Phase-127 showed the disagreement is not
a sampling artifact (matched-size null median TV
0.082613 vs observed 0.636931; 0 of 999 replicates
reached the observed median). Phase-131 (spec 022)
attributed only a composition share of 0.061321,
leaving a residual unexplained share of 0.938679, with
the segmentation, substitution, and
insertion-deletion shares NOT ESTIMABLE because the
legitimate matched-object join does not exist (4
matched pairs, 0 exact; Holdat's `cisi_number` is
internal sequential numbering, not a CISI key).
Reopening requires a legitimately keyed corpus layer,
which is external-data-dependent.
(iii) *Keyed transcription-layer build* — STOPPED AT
PILOT. Spec 023's Stage P pilot (Phase-132) fired its
frozen stop-rule (exact-sequence agreement 0.20 vs the
0.80 floor; error arm not fired) and all three release
gates failed, so no dataset was published. No Stage T
is proposed, scoped, or scheduled. A retry would
require a new owner decision **and** a materially
different transcription basis (e.g. human expert
transcription) — not a parameter change to the stopped
design.

**(b) POSTURE — WATCH-AND-RESPOND.** The program takes
no new internal study initiative. It responds to these
named triggers only:
(1) any reply to the 2026-10-08 letters — the RMRL
concordance request and the RMRL graffiti request
(both to R. Balakrishnan, Indus Research Centre,
RMRL), the Mitra/Dixit data request (Dixit et al.
2025 image-derived transcriptions), and the
Tiedekirja digital-CISI enquiry (Vols. 3.1/3.2/3.3);
(2) any hit from the weekly `indus-data-watch` —
Mahadevan Chair concordance, CISID release, Dixit
dataset deposit, CISI Vol. 3.4, Lothal 2025 seals,
Rakhigarhi report, Keeladi report, and any complete
digital CISI volume (3.1/3.2/3.3) appearing anywhere;
(3) GitHub Support ticket **#4838529** completion
(garbage collection after history purge #2) → verify
the pre-purge-#2 main commit `9ef78ca6` returns
HTTP 404 (404 = the commit is gone after garbage
collection) and record the closeout in these ledgers.
Response path for any data trigger: the Phase-130
intake pack (provenance capture → license gate →
dedup → spec-018 evaluability classification) →
report to the owner **before** any study is designed.
No study, battery, or PRED scoring runs without fresh
owner authorization.

**(c) STANDING STATE.** PRED-2026-001, PRED-2026-002,
and PRED-2026-003 remain **PENDING**, awaiting a
qualifying independent corpus under the frozen
spec-018 evaluability matrix. The 44 anchors remain
`pending_non_sa_validation`. The strict SA-free core
(94 readings, 73.68% corpus coverage) stands as a
hypothesis, not a validated decipherment.
Library-loan / document-delivery activity remains on
owner hold (2026-10-08). The pre-purge-#2 backup
mirror (`~/workspace/glossa-run/glossa-lab-backup-20261008-prepurge2.git`,
outside the repo) is retained pending its own owner
order. Standing watches verified live at this entry:
`glossa-backend-watchdog` (interval 20m, enabled) and
`indus-data-watch` (weekly, Wednesdays ~10:39 user
tz, enabled); their schedules are unchanged.

**AI disclosure:** this entry was recorded by an AI
agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-09 — Phase-133 (Spec 024): Evidence Integration, Stage 0 Inventory — coverage matrix, join-key audit, provenance grading; facts only, no associations computed

Spec 024 Stage 0 was frozen 2026-10-09 on the owner's
instruction of record (Tristen Pierson — "Execute the
plan"; PR #105, merge 467adbcf, freeze fecba9ec). The
Stage 0 build is Phase-133: a (layer × field) coverage
matrix over every machine-readable layer in hand, a
join-key audit with empirical collision counts,
field-provenance grading (O / C / I) of every field,
a mayig description-parseability measurement under a
stated rule, and a descriptive pass over the
non-machine-readable material. Everything was
recomputed by backend/scripts/
phase133_stage0_inventory.py from the local-store
files; nothing was copied from spec Appendix A —
Appendix A values are the claims the drift table
checks. Dataset: data/evidence_integration/
phase133_stage0_inventory.json (+ _meta.json with
input paths, sha256 per input, license basis per
layer). Report: reports/phase133_stage0_report.md.
Graph node IndusPhase133Stage0Inventory registered
(additive module + registry block, Phase-132 pattern).

Coverage, as found (243 matrix rows over 9 layers):
CISI catalogue 7,705 photo rows (Vol. 1: 3,320;
Vol. 2: 4,385), 22 fields, 3,494 distinct
volume-scoped objects (1,475 / 2,019); site filled
94.7% / 92.2%, object_type 95.1% / 96.3%,
motif_chapter 25.1% / 26.8% (2,005 rows; 909 of
3,494 distinct objects), material 0% and dimensions
0% on all 7,705 rows (not printed per object;
boundary 3; never back-filled). Object types (photo
rows): Seals 4,778, Tablets 2,180, Graffiti 417,
Objects 5. Holdat: 7,002 token rows, 19 fields,
1,670 distinct seal_id; site 100% and iconography
100% at token level (Class C; 9 values, unicorn
2,143 tokens / 514 inscriptions); prefix and vowel
empty on all rows; noun/verb constant 0. Holdat
semantic-roles table: 151 symbol rows, 15 fields.
mayig layer: 179 inscriptions / 179 objects, 1,003
tokens, 182 distinct signs; source corpus 179 files
/ 179 sides. horus84 (ICIT-lineage): 5,679 rows, 38
fields (see drift); site 100% raw over 77 values;
placeholders (-, --, None, ?, 0-in-mm-fields) encode
absence; row lengths vary 35–38 fields. Museum:
Met 28 curated objects (medium/dimensions on all
28), Cleveland 10 records in the acquired search
file (3 with type Seals), Penn 2 fetched records
(markdown capture, not machine-readable).

Join-key audit, as found: canonical key
cisi:v{volume}:{printed_id} re-derived; exactly one
printed ID (H-311) occurs in both volumes (unscoped
union 3,493). Within-volume duplicate photo_keys:
Vol. 1: 8, Vol. 2: 3 (printed IDs legitimately carry
multiple photo rows: 1,243 / 1,513 IDs with >1 row).
mayig cisi_object_id: 179/179 matched (all Vol. 1
only), 0 ambiguous, 0 unmatched — USABLE for these
values. horus84 cisi: rows matched 2,895 (Vol. 1
only 1,365; Vol. 2 only 1,530), ambiguous 2 (the
single distinct value H-311), unmatched 2,782
(including 662 '-' placeholder rows); distinct
values 4,074 (matched 2,476, ambiguous 1, unmatched
1,597) — NOT USABLE as a general join key. Holdat
cisi_number: PROHIBITED, never joined on; exact
coincidence with a printed ID 0 rows / 0 distinct
(zero-padded forms); after zero-stripping only,
1,355 of 1,670 distinct values coincide with some
printed ID and all 179 mayig IDs have a zero-padded
namesake — the Phase-131 fact stands (179 apparent,
0 validated). Holdat seal_id: intra-layer only,
1,670 distinct, 2–8 token rows per id. Museum
cross-reference census (rule: any string value
containing 'CISI' or 'Corpus of Indus'): 0 of 40
records (Met 0/28, Cleveland 0/10, Penn 0/2) — no
museum-to-CISI join counted or performed.

Provenance grading: 243 fields graded — O 207,
C 7, I 29, each with a one-line reason in the
dataset. The Class I exclusion list (29 fields,
named in the report): Holdat corpus letters,
letter_label_encoded, FormWithoutLemma,
MorphemeSeparated, morpheme boundary, noun, verb,
prefix, prefix_label_encoded, vowel, upos, xpos;
Holdat roles symbol, num_prefixes, num_suffixes,
num_shells, shell_density, is_starter, is_ending,
is_known_role, semantic_role; mayig tokens,
features; mayig source graphemes; horus84 class,
text, sanskrit, translation, notes. Catalogue
material/dimensions graded O and recorded 0%-filled
as printed, never inferred.

mayig parseability (rule declared before
application: case-insensitive substring match
against the §4.3-category + Holdat-iconography
motif-term list and a stated object-type-term list;
a parse is never ground truth): ≥1 motif term 179,
≥1 object-type term 179, both 179, neither 0; the
field contains only 5 distinct descriptions, all
"unicorn {I–V} seal", so the rate measures the
field's narrow vocabulary as acquired.

Anomalies recorded, not routed around: (1)
data/raw/other_sites/holdatllc_seal_catalog.csv is
not CSV and contains no seal catalogue — it is a
single-line Ollama /api/tags JSON listing three
local LLM models (qwen2.5-coder:7b-instruct,
qwen2.5:14b, mistral-nemo:12b); 0 seal records
recoverable. (2) Catalogue motif_chapter carries
spelling variants (unicorm/unicom/unicon/uricorn/
unico, tigerwithzebu) and Vol. 1 chapter headings
(SEALS, SEALSIMPRESSIONS) as values, as printed.
(3) horus84 placeholder conventions and variable
row lengths. (4) Museum directory holds 74 Met
object files (search candidates) vs the 28-ID
curated layer; Cleveland file holds 10 records vs
its "3 seals" summary.

Non-machine-readable pass (T4): Kodumanal volume
(152 pp.; Kodumanal report printed pp. 1–50;
sections incl. Trenches — 15 distinct KML-n labels
in OCR text — and a dedicated Graffiti Marks
section describing marks by ware and vessel
position; its printed graffiti tallies are
internally inconsistent — subtotals 75+70+70+10 =
225 under a stated 175, plus a separate "99
Graffiti marks collected" — quoted as printed prose
only, used as no counts). Kunal article (15 pp.,
J-STAGE 2012): stratigraphic prose/plates, no
tabular record structure; its embedded text layer
contains 0 alphanumeric characters (NUL glyphs), so
no machine-readable pass is possible as acquired;
no counts taken from it.

Appendix A drift: all headline Appendix A numbers
MATCH as re-measured except three DRIFT items —
(1) horus84 fields: Appendix A.4 (and §2.4) say 39;
the acquired header has 38 fields, and A.4's own
enumerated list names the same 38 — the "39" is a
miscount in the spec text; (2) Met "4 inscribed
seals" (A.5) is wording: 4 stamp-seal objects
(49.40.1–.4), only 49.40.3 titled with
"inscription"; (3) Cleveland "3 seals" (A.5) is
presentation: the acquired file is the full 10-record
search set. One NOT RECOMPUTED item: the Phase-124
98.9% sample field accuracy (Stage 0 takes no new
hand sample; the figure stands as a fact of record).

Arm-by-arm feasibility verdicts (§3.5, grounded
only in the audit; full text in the report): (a)
terminal-class × object-type SURVIVES IN REDUCED
FORM on the joined subsets only — mayig joins
179/179 but all joined objects are Seals (no
object-type variation); horus84 joins unambiguously
for 2,895 rows (2,752 with a filled catalogue
object_type: Seals 1,588, Tablets 1,088, Graffiti
69, Objects 7) under the mandatory ICIT lineage
label; Holdat joins 0 and carries no object-type
field. (b) motif × sequence: NO RECOMMENDATION
(per §3.5); the motif-bearing fields and the image
population exist at the proposed ~100-object scale
(motif_chapter 2,005 rows / 909 objects; Holdat
iconography complete but Class C; mayig parse
179/179 on a 5-description vocabulary), and test
(b) remains gated on Stage 1's separate go and
proceed gate. (c) site repertoire SURVIVES as a
coverage proposition — Holdat site over 1,670
inscriptions at 9 sites (Mohenjo-daro 606, Harappa
492, Lothal 124, Kalibangan 110, Dholavira 106,
Chanhu-daro 78, Surkotada 61, Banawali 60,
Rakhigarhi 33); horus84 site over 5,679 rows at 77
values; mayig has no site field (176/179 reach a
site via the catalogue join, all Mohenjo-Daro).
(d) graffiti comparative SURVIVES ONLY as the
comparative, descriptive §5.5 sketch — catalogue
Graffiti 417 photo rows over 395 distinct objects;
Kodumanal structure as above; the Tamil Nadu
graffiti corpus is NOT in hand (0 records), never
pooled (boundary 4), dating-gap caveat stands.

Stage 0 makes no Stage 1 recommendation beyond the
arm (b) existence facts. T6 (release-gated CC BY
4.0 publication of the inventory dataset) is
handled separately by the coordinator and was NOT
performed by this build; no publication, external
send, or outreach was made; no images or restricted
source files are in the change (text/code/JSON
only). No anchor, reading, or PRED changed:
anchors sha256 eccea6d5… asserted unchanged.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-09 — Zenodo v4.6.0 published (Spec 024 + Phase-133 Stage 0): inventory dataset CC BY 4.0 through the release gate; Phase-133 verification addendum

**Zenodo v4.6.0 published 2026-10-09** — DOI
10.5281/zenodo.23267995 (record 23267995); concept DOI
10.5281/zenodo.20379070 unchanged. The deposit (13
files) adds the Spec 024 / Phase-133 program note
(`pierson_2026_indus_program_note_133_stage0.md`) and
the Stage 0 inventory dataset
(`phase133_stage0_inventory.json` +
`phase133_stage0_inventory_meta.json`, CC BY 4.0 per
the owner's Decision Ask 4 adjudication — facts only,
no images) to the carried-forward v4.5.0 set.
Publication flow per docs/RELEASE_CHECKLIST.md:
program note + `RELEASE_VALIDATION.json`
`release_v4_6_0` entry via PR #108 (merge 8e9a90a7);
mandatory release gate run at 8e9a90a7 — **PASS
13/13** (12 MATCH + 1 EXTERNAL, the carried-forward
v3 preprint PDF byte-identical to the v4.5.0
record); gate recorded via PR #109 (merge 580bd8ae);
final gate run against the merged gate-record
commit 580bd8ae — **PASS 13/13**, exit 0 (final
staged `RELEASE_VALIDATION.json` sha256
a28703edc2e7d7bebcd2e7f3840a7e03fca5ac61fcba46df6068a3d07f91f229).
Post-deposit confirmation: **13/13** file checksums
on record 23267995 match the staged files. Suite and
foundation independently re-run at a289b19b in the
release worktree: **1005 passed / 5 skipped / 0
failed**; foundation **40 passed / 0 failed / 8
warnings**. OSF registry (osf.io/ybd65): dated
v4.6.0 blocks appended to the parent project, the
Program Outputs component (vwa7s), and the Corpora
component (dfrhz); the Literature component is
unchanged. Spec 024 task T6 marked DONE.

**Phase-133 verification addendum (coordinator,
2026-10-09).** The coordinator independently
recomputed the Stage 0 headline quantities from the
source files before publication; every figure
matched the merged inventory (PR #106) exactly under
the audit's stated matching rule, with one
clarification of record: the join-key audit matches
candidate values by **exact string**. Three horus84
`cisi` values carry trailing whitespace (`H-1734`
+TAB, `L-78` +space, `M-929` +space); the first
matches no printed ID under any rule, and the other
two are whitespace variants of valid printed IDs
that count as unmatched under the exact rule. A
whitespace-trimming recount differs by exactly
those 2 rows (matched 2,897 / unmatched 2,780 vs
the audit's 2,895 / 2,782). The report, dataset, and
program note (§3) stand as computed under the exact
rule; this note completes the record.

No anchor or PRED change — anchors sha256
eccea6d5… unchanged; PRED-2026-001/002/003 remain
PENDING. Spec 024 Stage 1 (motif pilot) is approved
in principle and still requires its separate
post-Stage-0 owner go; nothing in this release
authorizes it.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-09 — Phase-134 (Spec 024): Evidence Integration, Stage 1 Motif-Coding Pilot — exact agreement 0.84, Cohen's κ 0.7885; frozen §4.5 gates resolve to the MIDDLE BAND (proceed gate not met, stop rule not fired)

Owner go given 2026-10-09 ("Approve the Stage 1
motif-coding pilot"). Stage freeze recorded before
any sample image was viewed
(`specs/024-evidence-integration/stage1-freeze.md`,
commit `633e943e`), including a **premise correction
of record**: the shorthand population of 909
motif_chapter objects is degenerate (899/909 = 98.9%
unicorn chapters), so the frozen §4.2 population
governed — 3,245 catalogue objects with a parseable
photo box and object_type ∈ {Seals, Tablets,
Graffiti}. Frame of exactly 100 drawn by the frozen
rule (stratified site-group × type, largest-remainder
quotas with a 2-per-cell floor, sha256 seed
`phase134-20261009`; commit `e51d0637`); all 100
objects cropped from the local store (220 crops, 0
failures, 0 replacements; images never in git).

Two independent blinded passes coded all 100 objects
under the frozen 12-code taxonomy; a gold third pass
coded the 20-object subset; a separate adjudicator
ruled all 16 disagreements (pass A upheld 10, pass B
upheld 6, neither 0), the disagreement log preserved
in full in the dataset. All roles were executed by
AI agents in blinded role-isolated instances
(constitution §VI), disclosed in every artifact.
All quantities were computed by
`backend/scripts/phase134_metrics.py` from the
on-disk coding records — never from coder
self-reports.

**Results as found:** exact primary-motif agreement
**0.84** (84/100); Cohen's κ **0.7885** (chance
agreement Pe = 0.2436). Per-category agreement:
SCRIPT_ONLY 0.833 (30/36), UNICORN 0.793 (23/29),
GEOMETRIC 0.714 (5/7), ILLEGIBLE 0.667 (20/30);
small categories rest on 1–4 objects. **Confusion
structure:** 10 of 16 disagreements involve
ILLEGIBLE on one side (ILLEGIBLE×UNICORN 3,
ILLEGIBLE×SCRIPT_ONLY 5, ILLEGIBLE×ELEPHANT 1,
GEOMETRIC×ILLEGIBLE 1) — the disagreement mass sits
on the legibility boundary for worn objects, not on
animal identity among clearly visible depictions.
Gold-subset drift: A–B 0.80, A–G 0.85, B–G 0.75,
unanimous 0.70 — no pass is an outlier. Descriptive
concordance (freeze §6, never accuracy): of 31
unicorn-chapter objects in the frame, adjudicated
codes were UNICORN 22 / other 9. Adjudicated final
distribution: SCRIPT_ONLY 34, ILLEGIBLE 26, UNICORN
26, GEOMETRIC 6, COMPOSITE 2, GOAT_ANTELOPE 2,
ELEPHANT 1, TIGER 1, BUFFALO 1, RHINOCEROS 1.

**Gate verdict (frozen §4.5, applied exactly):**
proceed gate (agreement ≥ 0.85 AND κ ≥ 0.75) **NOT
MET** — agreement 0.84, one object short of the arm,
κ arm met; stop rule (agreement < 0.70 OR κ <
0.50) **NOT FIRED**. Verdict: **MIDDLE BAND**. The
motif arm is therefore **not** eligible for Stage
2(b) on this pilot alone; the pilot report
(`reports/phase134_pilot_report.md`) frames the
owner's decision without a recommendation dressed
as a verdict. No association statistic was computed.
Publication of the Stage 1 dataset beyond the repo
is not pre-authorized and is framed as an owner
decision alongside the verdict.

**Process finding (deviation D1 of the report):** a
coder completion handoff raced its own final two
record writes; a coordinator snapshot read 23/25 and
a blinded top-up was commissioned for the two
apparently-missing objects before the batch's own
records landed. The metrics script's fail-loud
duplicate check caught the collision at assembly;
resolved by rule (original batch records govern,
top-up records excluded from every quantity; the two
codings agree on both objects, so the data impact is
none). A second live instance of the Phase-132 §4(d)
finding, in the benign direction — and the reason
every quantity in this phase was computed from the
records, not from reports about the records.

No anchor or PRED change — anchors sha256
eccea6d5… unchanged; PRED-2026-001/002/003 remain
PENDING.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## [2026-10-22] Entry — Spec 025: Paper-Search MCP Client + RESEARCH-CHECK Stage

Objective:
  Implement the owner-ordered scholarly research-checking MCP
  (openags/paper-search-mcp) in Glossa Lab — tooling only; the audit
  of Glossa's own material is separate follow-on work assigned to
  the Glossa Lab chat.

What was done:

  1. SPEC: specs/025-paper-search-research-check/ (spec.md, plan.md,
     tasks.md) — proposal with H13 epistemic boundaries recorded
     before execution (H2).

  2. CLIENT: backend/glossa_lab/paper_search.py — stdio MCP client
     running under the backend venv (existing mcp>=1,<2 dependency),
     spawning the shared server from ~/workspace/venvs/paper-search-mcp
     (the pinned install maintained from the RCPH workspace; not
     duplicated). Sci-Hub is hard-off in code. Timeouts on every call
     (H9/H11); NO_PROXY sanitized as in the house clients.

  3. STAGE: backend/glossa_lab/research_check.py — RESEARCH-CHECK
     stage for claim dossiers, designed to run BEFORE AEE scoring /
     adjudication. Per claim: >=2 concept phrasings x >=2 sources,
     DOI resolution for supplied citations, nearest-neighbor
     surfacing with full-text reads of reachable OA neighbors.
     Records are advisory sidecars in glossa-indus/claims/
     research_checks/; verdict is always null; the claim file is
     never modified. Placement decision (client module beside the
     loop, not new glossa_mcp tools): glossa_mcp's 33 tools are
     route-drift-guarded backend controls; paper search has no
     backend route. Recorded in the spec.

  4. DOCS: docs/paper-search-mcp.md (connector/usage doc; the audit
     protocol carried over unchanged from the RCPH connector) and an
     AGENTS.md pointer section (H8).

  5. TESTS: backend/tests/test_paper_search.py — 10 offline tests
     (client config, Sci-Hub refusal, phrasing plan, record shaping
     against a stubbed client, advisory invariant). Run with the
     governance lint and MCP suites: 39 passed.

  6. SMOKE (live, raw outputs in the spec's smoke/): 57 tools via
     the Glossa client; federated + arXiv concept queries on Indus
     decipherment returned the real literature (Yadav et al. n-grams
     paper at the top); DOI 10.1126/science.1170391 resolved to the
     Rao et al. 2009 Science record; end-to-end stage run wrote the
     first sidecar (25 neighbors, 3 full-text reads, verdict null).
     MEASURED TRAP: the arXiv connector answers a no-match
     conjunction with a default high-profile list (ATLAS /
     gravitational-wave papers) instead of an empty result — the
     first stage run spent its read slots on those. The stage now
     ranks neighbors by claim-vocabulary overlap and gates reads on
     it; the rerun's reads were all on-topic. Recorded in
     docs/paper-search-mcp.md limits.
     Process note (H9): the first stage invocation was killed by a
     service restart mid-run (no record written; two downloaded
     PDFs remained under research_checks/full_text/, gitignored per
     the repo's PDF policy); retried detached and completed.

  7. COMMIT: this spec's files only, on branch
     spec/025-paper-search-research-check. The pre-existing
     uncommitted working-tree modifications (claims extraction,
     anchor staging, partial loop results) are not this session's
     work and were not staged. origin/main has advanced beyond this
     checkout (6215690d vs c4a3ef4c); push of this branch attempted
     as a new branch only — main was not touched.

**AI disclosure:** execution recorded by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per constitution SSVI.
## 2026-10-09 — Phase-135 (Spec 024): Evidence Integration, Stage 1 Re-Pilot — clarified codebook, fresh sample; exact agreement 0.78, Cohen's κ 0.7129; MIDDLE BAND for the second time; no Stage 2(b) design

Owner approval (Tristen Pierson, 2026-10-09): "Run
the combined path — clarify the boundary, re-pilot
fresh, freeze Stage 2(b) only if the gates pass,
publish the combined record." The clarification
(freeze record
`specs/024-evidence-integration/stage1-freeze-2.md`,
freeze commit `dee4e5c2`, committed before the frame
was drawn) defines only the legibility boundary:
five decision rules (B1–B5) for ILLEGIBLE /
SCRIPT_ONLY / GEOMETRIC and the classifiability
threshold, distilled from the 16 adjudicated
Phase-134 disagreements, which are quoted as worked
examples. The 12-code taxonomy, the precedence
rule, and every gate threshold are unchanged by
any amount.

Phase-135 re-pilot, executed under that freeze:
fresh 100-object stratified frame drawn from the
frozen §4.2 population (3,245) minus the 100
Phase-134 frame objects → 3,145 eligible; seed
`phase135-20261009`; **overlap with the Phase-134
frame = 0**, asserted at draw time and verified
independently. Two blinded passes + gold third
coding of 20 + adjudication of all 22
disagreements; coders saw the clarified codebook
only — its worked examples are the sole Phase-134
material issued to any coder. All roles
AI-executed with the §VI disclosure; all
quantities computed by script from the on-disk
records (verified complete: A 100, B 100, gold 20,
adjudication 22; fail-loud checks passed on the
first run). **Deviations: none.**

Results as found: exact agreement **0.78** (78/100),
Cohen's κ **0.7129** (Pe 0.2338). Frozen §4.5
gates: proceed gate NOT MET (both arms — agreement
0.78 < 0.85, κ 0.7129 < 0.75), stop rule NOT FIRED
→ **MIDDLE BAND, for the second time**. Per
freeze-2 §5, no Stage 2(b) design is drafted; the
owner's decision is framed in
`reports/phase135_pilot_report.md` §8 without a
recommendation dressed as a verdict.

Measured shifts against Phase-134 (descriptive;
the pilots differ in sample and codebook, so this
is not a controlled comparison): ILLEGIBLE usage
halved (marginals 14/12 vs 27/23), in the
clarification's intended direction, but
reproducibility did not follow it — ILLEGIBLE
per-category agreement fell 0.667 → 0.368, and
depiction-identity disagreements rose from 6/16 to
10/22. On a fresh sample under the clarified
codebook, this pipeline's measured reliability was
lower, not higher; the Phase-134 reading that the
disagreement was mostly one definitional boundary
is not supported by this run. Adjudicated
distribution (descriptive): SCRIPT_ONLY 38,
UNICORN 30, ILLEGIBLE 10, GEOMETRIC 8, ELEPHANT 4,
remainder ≤2; ZEBU and COMPOSITE 0. Gold-subset
drift: A–B 0.75, A–G 0.90, B–G 0.75, unanimous
0.75 — no outlier pass. Descriptive concordance
with unicorn-family motif chapters: 30 sampled,
26 adjudicated UNICORN (concordance, never
accuracy).

No association statistic was computed. No anchor
or PRED change — anchors sha256 eccea6d5…
unchanged; PRED-2026-001/002/003 remain PENDING.
Combined motif-arm publication follows as Zenodo
v4.7.0 per the same owner approval (both pilot
datasets, codes and logs only, no images).

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-09 — Zenodo v4.7.0 published (Spec 024 Stages 1–1b: Phase-134 + clarification + Phase-135): both motif pilot datasets CC BY 4.0 through the release gate

**Zenodo v4.7.0 published 2026-10-09** — DOI
10.5281/zenodo.23270096 (record 23270096); concept DOI
10.5281/zenodo.20379070 unchanged. The deposit (18
files) adds the Spec 024 Stages 1–1b program note
(`pierson_2026_indus_program_note_134_135_motif.md`)
and both motif-coding pilot datasets
(`phase134_pilot_dataset.json`,
`phase135_pilot_dataset.json`, each with its
provenance meta, CC BY 4.0 per the owner's
combined-path approval — codes, notes, and
disagreement logs only, no images) to the
carried-forward v4.6.0 set. Publication flow per
docs/RELEASE_CHECKLIST.md: program note +
`RELEASE_VALIDATION.json` `release_v4_7_0` entry via
PR #113 (merge e698cff2); mandatory release gate run
at e698cff2 — **PASS 18/18** (17 MATCH + 1 EXTERNAL,
the carried-forward v3 preprint PDF byte-identical to
the v4.6.0 record); gate recorded via PR #114 (merge
52580e43); final gate run against the merged
gate-record commit 52580e43 — **PASS 18/18**, exit 0
(final staged `RELEASE_VALIDATION.json` sha256
10c27e6b232438dd097f1dc61ed17b09b63b61c8464681d8c4fca8b2612ada36).
Post-deposit confirmation: **18/18** file checksums
on record 23270096 match the staged files. Suite and
foundation run at the Phase-135 merge 11e70c98 in
the release worktree: **1026 passed / 5 skipped / 0
failed**; foundation **40 passed / 0 failed / 8
warnings**. OSF registry (osf.io/ybd65): dated
v4.7.0 blocks appended to the parent project, the
Program Outputs component (vwa7s), and the Corpora
component (dfrhz); the Literature component is
unchanged. Spec 024 tasks T9b–T9e marked DONE.

The release closes the motif arm's combined path as
the numbers dictated: Phase-134 MIDDLE BAND (0.84 /
κ 0.7885), boundary clarified (stage1-freeze-2,
Rules B1–B5, gates unchanged), Phase-135 fresh-sample
re-pilot MIDDLE BAND again (0.78 / κ 0.7129), no
Stage 2(b) design drafted. The Stage 2(b) decision
now rests with the owner on the framed options in
`reports/phase135_pilot_report.md` §8; nothing in
this release authorizes it.

No anchor or PRED change — anchors sha256
eccea6d5… unchanged; PRED-2026-001/002/003 remain
PENDING.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-09 — Spec 024 motif arm CLOSED AS RUN (owner decision: paths (b) + (c) together)

Owner decision 2026-10-09: the Spec 024 motif arm
takes paths (b) AND (c) together. The arm is
**closed as run on the AI-coder basis**, effective
2026-10-09, resting on its published two-pilot
record — Phase-134 (exact agreement 0.84, Cohen's
κ 0.7885, MIDDLE BAND) and Phase-135 (clarified
codebook, fresh sample; exact agreement 0.78,
κ 0.7129, MIDDLE BAND for the second time) —
published as Zenodo v4.7.0, DOI
10.5281/zenodo.23270096. Neither pilot met the
frozen proceed gate; no Stage 2(b) design exists
or is authorized.

**Reopening condition (the preserved path (b)):**
the arm may be reopened ONLY under a new owner
decision AND a materially different measurement
basis — human expert coders — using the clarified
codebook (`stage1-freeze-2.md`), a fresh sample,
and the identical frozen gates (proceed ≥0.85 exact
agreement AND κ ≥0.75; stop <0.70 OR κ <0.50). A
third AI-basis pilot is expressly not a reopening
path. Stage 2 arms (a), (c), and (d) are
unaffected and stand in their Stage-0 forms;
their design freezes remain separate future owner
decisions. Closure record:
`specs/024-evidence-integration/motif-arm-closure.md`.

No anchor or PRED change — anchors sha256
eccea6d5… unchanged; PRED-2026-001/002/003 remain
PENDING.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## 2026-10-09 — Phase-137 (Spec 024): Evidence Integration, Stage 2(c) Site Repertoire Differentiation — F2 (Holdat) raw p = 0.7354; F3 (ICIT-lineage) raw p = 0.0001; verdicts deferred to the combined report's BH correction

Executed exactly as frozen in
`specs/024-evidence-integration/stage2c-freeze.md`
(merged PR #118 before any analysis code ran), under the
owner's Stage 2 instruction of record (Tristen Pierson,
2026-10-09 — "Do all next things"). Family members F2 and
F3 tested separately, never pooled: site × sign profile
tables (sign columns = layer-wide count ≥ 10 within the
analysis population, rarer → OTHER; placeholders excluded),
Pearson chi-square as a divergence statistic only,
inference by permutation of site labels at inscription
level within composition strata (B = 9,999, seed
20261009). Class I fields entered nothing in either
layer. H23 order followed (script → graph module
`IndusPhase137SiteRepertoire` → registration verified →
run). Results computed by script into
`reports/phase137_results.json`; report at
`reports/phase137_report.md`.

**F2 — Holdat compilation layer:** all 1,670 inscriptions,
all 9 sites eligible, length-class strata only (type
control degenerates — no type field in the layer, stated
in the freeze). Table 9 × 98 (OTHER = 911 tokens, 13.01%).
Observed χ² = 745.95 vs permutation median 770.32 / 95th
838.45; 7,353/9,999 permutations ≥ observed → **raw
p = 0.7354**. Cramér's V 0.1154. Sparsity disclosed per
freeze §3: 607/882 cells (68.8%) expected < 5, min
expected 0.214.

**F3 — ICIT-lineage layer (horus84):** 5,679 rows;
7 eligible sites, 5,410 inscriptions (70 site labels
excluded and named in the report, incl. Unknown);
type × length strata (16). Table 7 × 187 (OTHER = 1,387
profile tokens, 8.04% of 17,257). Observed χ² = 4,966.36
vs permutation median 2,667.87 / 95th 2,844.61; 0/9,999
permutations ≥ observed → **raw p = 0.0001** (the minimum
the frozen formula returns at B = 9,999). Cramér's V
0.2190. Sparsity: 887/1,309 cells (67.8%) expected < 5,
min expected 0.075. The uncontrolled-confounder
statement (freeze §6 B2: period, preservation, excavation
history not controlled) is stated in the report wherever
this positive result is stated.

**No verdict words here:** BH at q = 0.05 across the
family is applied once, in the combined Stage 2 report,
per the Stage 2(a) family declaration. Deviations from
the freeze: none (three recorded interpretations in the
report — inclusion token arm on parsed tokens, matching
the freeze's own audit counts with an identical eligible
set under either basis; the Holdat single-quote strip is
a measured no-op on the file in hand, which contains no
quotes; F3 length class on parsed tokens per the freeze's
wording). Verification: phase tests 22 passed (including
full recomputation reproducing the committed JSON
exactly); foundation check 40 passed, 0 failed. No anchor
or PRED change — anchors sha256 eccea6d5… unchanged.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.


## 2026-10-09 — Phase-136 (Spec 024): Evidence Integration, Stage 2(a) — Terminal-class × object type on the ICIT-lineage joined subset (F1): CMH 47.0047, raw p = 0.0001

Executed exactly as frozen in
`specs/024-evidence-integration/stage2a-freeze.md`
(PR #117; the freeze also carries the Stage 2
family declaration, tasks T10). PR #121, merge
`e7d17f6a`; CI 7/7. Flow as run, every design-audit
number reproduced: 5,679 ICIT-lineage rows → 2,895
joined (audited exact-string key; 2 ambiguous,
2,782 unmatched — 49.0% of the layer unjoinable or
ambiguous) → 2,752 typed → 2,676 in the
pre-declared {Seals, Tablets} restriction → 2,195
terminal-mapped → 2,062 in the 3 eligible strata
(Mohenjo-daro, Harappa, Kalibangan). Observed CMH
47.0047 (permutation median 0.455, 95th 3.991);
0/9,999 permutations ≥ observed → raw p = 0.0001.
MH common OR 2.384 (95% CI 1.847–3.077); crude OR
2.748 (control attenuates, does not remove).
TERMINAL shares: seals 28.1% vs tablets 12.5%
pooled eligible. Estimability: ESTIMABLE. Verdict
word assigned in the combined Stage 2 report after
the family BH correction (F1 q = 0.00015,
SUPPORTED). ICIT-lineage label in every headline;
the compilation-internal alternative explanation
is stated in the report. Not a PRED-2026
evaluation. No anchor change — anchors sha256
eccea6d5… unchanged. Results:
`reports/phase136_results.json`; report:
`reports/phase136_report.md`.

**AI disclosure:** execution recorded by an AI
agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

## 2026-10-09 — Phase-138 (Spec 024): Evidence Integration, Stage 2(d) — Graffiti descriptive protocol: 417 rows / 395 objects; motif_chapter 0/417; NO test computed

Executed exactly as frozen in
`specs/024-evidence-integration/stage2d-freeze.md`
(PR #119). PR #120, merge `4069bcb1`. Descriptive
only — no test, no p-value, not a family member.
Population as run: 417 catalogue Graffiti rows /
395 distinct objects (Vol. 1: 119/100; Vol. 2:
298/295). Objects by site: Harappa 262, Lothal 44,
Mohenjo-Daro 42, Kalibangan 26, no site 8.
Photo-rows-per-object mode 1 (374/395).
`motif_chapter` filled on 0 of 417 rows — the
editors' chapter organization assigns no depiction
chapter to any graffiti row. `caption_ocr_score`
median 0.943 (IQR 0.029). Kodumanal comparative
paragraph qualitative only, its printed tallies
quoted as prose with their internal inconsistency;
Tamil Nadu corpus NOT in hand (0 records);
≥1,000-year dating-gap caveat attached to every
comparative statement; no overlap statistic
computed (no machine-readable graffiti sign-form
repertoire exists in hand); no continuity claim.
Results: `reports/phase138_results.json`; report:
`reports/phase138_report.md`.

**Correction of record (same date):** PR #120
merged on a CI readout that did not match its
run's actual conclusion — the backend job had
failed on two pins in the phase's own test file
(a field-class string pin; a line-wrap pin; both
in test code, neither touching a descriptive
quantity). Caught by the executing worker's
verification against the run's API record and job
log; corrected in PR #123 (merge `1c2a5fd2`), CI
verified green from the run's own conclusion and
job log (1,044 passed / 14 skipped / 0 failed)
before merging. Foundation check 40 passed,
0 failed. No anchor change — anchors sha256
eccea6d5… unchanged.

**AI disclosure:** execution recorded by an AI
agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

## 2026-10-09 — Spec 024 Stage 2 COMBINED (Phases 136–138): declared-family BH correction applied once — F1 SUPPORTED, F2 NOT SUPPORTED, F3 SUPPORTED; arm (d) descriptive record complete

Owner instruction: "Do all next things"
(2026-10-09). Freezes PRs #117/#118/#119;
executions PRs #121 (Phase-136), #122 (Phase-137),
#120 + #123 (Phase-138). The combined report
(`reports/phase136_137_138_stage2_report.md`)
applies Benjamini–Hochberg at q = 0.05 across the
declared family's three raw p-values, once:
**F1** terminal × object type (ICIT-lineage):
p 0.0001 → q 0.00015, **SUPPORTED** (MH OR 2.384);
**F2** site repertoire (Holdat): p 0.7354 →
q 0.7354, **NOT SUPPORTED** (observed χ² 745.95
below its composition-controlled null median
770.32; per the §5.4 falsifier, site "dialects" on
this layer are recorded as an artifact of what each
site preserves, not a finding); **F3** site
repertoire (ICIT-lineage): p 0.0001 → q 0.00015,
**SUPPORTED** (χ² 4,966.36 vs null median
2,667.87; period/preservation/excavation-history
confounders uncontrolled and stated). Arm (d):
descriptive record complete (§5 entry above).
Arm (b) untouched — CLOSED (motif-arm closure
record). §8 governs: these are facts about use as
recorded in named layers; nothing here mints or
validates a reading, changes an anchor, or moves
PRED-2026 (001/002/003 PENDING). Publication of
the Stage 2 record as Zenodo v4.8.0 follows as
task T12 (entry on completion).

**AI disclosure:** execution recorded by an AI
agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

## 2026-10-09 — Zenodo v4.8.0 published (Spec 024 Stage 2: Phases 136–138): F1 SUPPORTED, F2 NOT SUPPORTED, F3 SUPPORTED through the release gate

**Zenodo v4.8.0 published 2026-10-09** — DOI
10.5281/zenodo.23273722 (record 23273722); concept DOI
10.5281/zenodo.20379070 unchanged. The deposit (22
files) adds the Spec 024 Stage 2 program note
(`pierson_2026_indus_program_note_136_137_138_stage2.md`)
and the three phase results files
(`phase136_results.json`, `phase137_results.json`,
`phase138_results.json`, CC BY 4.0) to the
carried-forward v4.7.0 set. Publication flow per
docs/RELEASE_CHECKLIST.md: program note +
`RELEASE_VALIDATION.json` `release_v4_8_0` entry via
PR #125 (merge b5c6c8e2); mandatory release gate run
at b5c6c8e2 — **PASS 22/22** (21 MATCH + 1 EXTERNAL,
the carried-forward v3 preprint PDF byte-identical to
the v4.7.0 record); gate recorded via PR #126 (merge
fe734ef0); final gate run against the merged
gate-record commit fe734ef0 — **PASS 22/22**, exit 0
(final staged `RELEASE_VALIDATION.json` sha256
7306f12f0d9c09d0320410b95d6a6d973993e7d5cefade39097e8d94caec8336).
Post-deposit confirmation: **22/22** file checksums
on record 23273722 match the staged files. Suite and
foundation run at the Stage 2 combined-report merge
949d627e in the release worktree: **1081 passed / 5
skipped / 0 failed**; foundation **40 passed / 0
failed / 8 warnings**. OSF registry (osf.io/ybd65):
dated v4.8.0 blocks appended to the parent project,
the Program Outputs component (vwa7s), and the
Corpora component (dfrhz); the Literature component
is unchanged. Spec 024 task T12 marked DONE.

Stage 2 outcomes, as found (one declared family,
Benjamini–Hochberg q = 0.05 applied once in the
combined report): **F1** terminal-class × object
type, within-site stratified (ICIT-lineage layer) —
CMH 47.0047, raw p = 0.0001, q = 0.00015, **SUPPORTED**
(Mantel–Haenszel common OR 2.384, 95% CI 1.847–3.077;
the layer is an ICIT-lineage derivative, not an
independent witness). **F2** site repertoire
differentiation (Holdat layer) — χ² 745.95, below its
permutation median 770.32, raw p = 0.7354,
q = 0.7354, **NOT SUPPORTED**. **F3** site repertoire
differentiation (ICIT-lineage layer) — χ² 4,966.36
against a permutation median of 2,667.87, raw
p = 0.0001, q = 0.00015, **SUPPORTED** (Cramér's V
0.2190; period, preservation, and excavation history
not controlled in that layer). Arm (d) (Phase-138)
was descriptive only: 417 catalogue graffiti rows
over 395 distinct objects, the editors'
depiction-chapter field filled on 0 of 417 rows; no
test was computed and no continuity claim is made.
The F2/F3 contrast is not itself a test: site
differentiation is not a layer-free fact.

No anchor or PRED change — anchors sha256
eccea6d5… unchanged; PRED-2026-001/002/003 remain
PENDING.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.


## 2026-10-10 — Phase-139 (Spec 025): Stage 2 controlled follow-up — covariate audit + harmonization (margins only); G1 ESTIMABLE, primary control = preservation

Executed exactly as frozen in Spec 025 (owner
adjudication 2026-10-10, spec.md sec.11; freeze merged
PR #129, main c3101cce). MARGINS ONLY: no association
statistic, no repertoire comparison, no G1 quantity
computed; sign tokens read only to reproduce the
Phase-137 F3 population (5,410 inscriptions, 7 eligible
sites — reproduced exactly) and its composition strata.
H23 order followed (script -> graph module
IndusPhase139CovariateAudit -> registration verified
-> run). Audit: backend/scripts/
phase139_covariate_audit.py; results:
reports/phase139_results.json; report:
reports/phase139_report.md; dataset + citation register:
data/evidence_integration/phase139_*.

Spec sec.3 reproduction: period/phase/both/preservation
counts reproduce EXACTLY (full layer 2,318/2,652/5,670;
F3 pop 2,266/2,638/1,788/5,404). Three printed draft
percentages carry documented deltas (union 57.7% =
rounded-percentage arithmetic, exact 57.6%; depth
48.1/49.9% under an unrecoverable draft parse rule —
bracketed [draft, audit 49.5/51.2%], classification
identical throughout; all-three 16.8 vs 16.9 knock-on).

Harmonization: chron_band (Q2(a), Class C) — 35 mapped
cells, 7 published citations (Kenoyer 2008/Meadow &
Kenoyer; Bisht; Marshall 1931; Mackay 1938; Lal &
Thapar; Rao 1979; Jarrige 1993); 0 period/phase band
conflicts; recorded 2,267 (41.9%) = the sec.3.3 bound
exactly (2,162 via period cells, 105 via Lothal phase
cells; Harappa Stratum I-VII 837 rows and Lothal Layer N
stay UNRECORDED — no citable correlation). depth_band
(Q3(a)): within-(site x unit) tertiles, documented
parse (VALUE 2,684 / SURFACE 50 / RANGE 10 / DOTDOT 9 /
UNITLESS 16 / COLON_FT_IN 1 / UNPARSED 1); 145
boundary-tie rows disclosed; recorded 2,765 (51.1%).
Preservation collapse: complete 3,046 / fragment 1,761
/ damaged 597 / UNRECORDED 6 — recorded 5,404 (99.9%).

Gate (sec.4.2 step 3, verbatim): chron_band FAILS arm
(i) -> SENSITIVITY; depth_band FAILS arm (i) ->
SENSITIVITY; preservation passes all three arms ->
PRIMARY CONTROL. Routing rule: exactly one passer, so
G1 is ESTIMABLE with primary strata = composition
(Phase-137 type class x length class) x preservation,
UNRECORDED retained as a stratum level; chronology
NOT controlled in the primary test and named as an
uncontrolled confounder in every G1 headline;
sensitivities S-chron / S-depth pre-declared
EXPLORATORY in the freeze record
(specs/025-stage2-controlled-followup/
phase139-freeze.md: final strata, seed 20261009, BH
q = 0.05 over G1 alone per Q4(b), sec.5 LOSO
criterion). Publication rides with the Spec 025
outcome record (Q6) — no release from Phase-139.
Anchors sha256 eccea6d5... unchanged; no PRED
movement.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution sec.VI.


## 2026-10-10 — Phase-140 (Spec 025): G1 — F3 site-repertoire re-test under preservation control (ICIT-lineage layer, horus84) — SUPPORTED under control; chronology NOT controlled

Executed exactly as frozen (phase140-freeze.md under
phase139-freeze.md; freeze records PR #131, merged
2ca98d05): Phase-137 F3 statistic family, population
reproduced by rule (5,410 inscriptions, 7 sites) and
asserted against the committed F3 record; covariates
joined from the Phase-139 harmonized dataset (5,410 /
5,410 rows, composition-stratum agreement asserted);
pre-run regression in the uncontrolled (composition-
only) configuration reproduced Phase-137 F3 EXACTLY
(chi2 4,966.362228365138; 0/9,999; median 2,667.87).

G1 (permutation within composition x preservation
strata, 53 strata, B = 9,999, seed 20261009):
permutable 5,404 / 5,410; observed chi2 4,966.36; null
median 2,684.74; p95 2,859.30; 0 of 9,999 permutations
>= observed; raw p = 0.0001. BH over G1 alone (Q4(b),
m = 1): adjusted 0.0001 <= 0.05 -> SUPPORTED under
control. Cramer's V (descriptive) 0.2190; sparsity
disclosed (887 / 1,309 cells expected < 5, 67.8%).
Headline rider (mandatory): ICIT-lineage layer
(horus84); preservation recorded coverage 99.9%;
chronology is NOT controlled in the primary test —
period/phase remain uncontrolled confounders.

Sensitivity panel (EXPLORATORY bounds only, never the
verdict): S-chron (composition x chron_band, 41.9%
recorded): permutable 5,342, null median 2,809.53,
0/9,999 >= observed, raw p 0.0001. S-depth
(composition x depth_band, 51.1% recorded):
permutable 5,406, null median 2,682.78, 0/9,999,
raw p 0.0001.

Deviation recorded in the phase report: first launch
aborted on the script's own layer-hash assertion (a
mis-split hash constant, one hex digit dropped) before
any computation; constant corrected to the verified
hash and relaunched; no design quantity affected.
Anchors sha256 eccea6d5... unchanged; no PRED
movement. Results: reports/phase140_results.json;
report: reports/phase140_report.md.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution sec.VI.


## 2026-10-10 — Phase-141 (Spec 025): F1 leave-one-site-out sensitivity (ICIT-lineage layer, horus84) — F1 STABLE, no load-bearing site

Executed exactly as frozen (phase141-freeze.md under
spec sec.5 / phase139-freeze.md sec.4; freeze records
PR #131, merged 2ca98d05): Phase-136 machinery
unchanged (its pure functions imported and reused)
plus the stratum-drop parameter only. No-drop
configuration reproduced the committed Phase-136
result EXACTLY (CMH 47.004657020769315; 0/9,999; raw
p 0.0001; MH OR 2.3839554105695653, CI 1.847-3.077).

Subsets (all ESTIMABLE under the Phase-136 sec.5 rule,
pooled expected >= 5 fraction 1.0 each): L-MD (drop
Mohenjo-daro): CMH 28.5198, 0/9,999, raw p 0.0001, MH
OR 2.706 (1.858-3.940). L-HA (drop Harappa): CMH
20.5927, 1/9,999, raw p 0.0002, MH OR 2.162
(1.541-3.033). L-KA (drop Kalibangan): CMH 47.1515,
0/9,999, raw p 0.0001, MH OR 2.400 (1.857-3.103).

Robustness criterion (sec.5, verbatim outcome): F1 is
STABLE under leave-one-site-out — every estimable
subset's MH common OR remains > 1 with its 95% CI
excluding 1, so no single site is load-bearing for
the F1 result. Raw p reported; no q-values (Q4(b));
no verdicts minted — a robustness statement about F1
only. Anchors sha256 eccea6d5... unchanged; no PRED
movement. Results: reports/phase141_results.json;
report: reports/phase141_report.md.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution sec.VI.


## 2026-10-10 — Spec 025 combined report (Phases 139-141) + foundation check

Combined report reports/phase139_140_141_spec025_
report.md (T13): the not-freezable-as-sketched finding
and Phase-139 gate outcomes (preservation PRIMARY
CONTROL 99.9%; chron_band SENSITIVITY 41.9%;
depth_band SENSITIVITY 51.1%); G1 SUPPORTED under
control (raw p 0.0001; BH over G1 alone, m = 1) with
the mandatory headline rider — ICIT-lineage layer
(horus84), preservation recorded coverage 99.9%,
chronology NOT controlled in the primary test;
EXPLORATORY bounds S-chron / S-depth both raw
p 0.0001; LOSO robustness statement verbatim (F1
STABLE, no load-bearing site). BH applied per Q4(b)
in the combined report (T13). Foundation check on
merged main fdfb0b39 (T14): 40 passed / 0 failed /
8 warnings; anchors re-asserted byte-identical
(eccea6d5...). Publication follows as Zenodo v4.9.0
per Q6 (T15).

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution sec.VI.


## 2026-10-10 — Zenodo v4.9.0 published (Spec 025: Phases 139–141): G1 SUPPORTED under control (chronology NOT controlled); F1 LOSO STABLE

**Zenodo v4.9.0 published 2026-10-10** — DOI
10.5281/zenodo.23288406 (record 23288406); concept DOI
10.5281/zenodo.20379070 unchanged. The deposit (26
files) adds the Spec 025 program note
(`pierson_2026_indus_program_note_139_140_141_spec025.md`)
and the three phase results files
(`phase139_results.json`, `phase140_results.json`,
`phase141_results.json`, CC BY 4.0) to the
carried-forward v4.8.0 set. Publication flow per
docs/RELEASE_CHECKLIST.md: program note +
`RELEASE_VALIDATION.json` `release_v4_9_0` entry via
PR #135 (merge 232f0d2f); mandatory release gate run
at 232f0d2f — **PASS 26/26** (25 MATCH + 1 EXTERNAL,
the carried-forward v3 preprint PDF byte-identical to
the v4.8.0 record); gate recorded via PR #136 (merge
a4514de1); final gate run against the merged
gate-record commit a4514de1 — **PASS 26/26**, exit 0
(final staged `RELEASE_VALIDATION.json` sha256
dfb95004d617ac0b47b48194b16166eb7185ff4b9ce6827b4be341166c53d03f).
Post-deposit confirmation: **26/26** file checksums
(MD5) on record 23288406 match the staged files.
Suite and foundation at the release commits: local
suite at merged main 5eec1542 in the release worktree
(canonical venv, corpora symlinked, CI configuration,
GPU files ignored) **1122 passed / 5 skipped / 0
failed** (CI at the same tree: 1109 passed / 18
skipped; the 13-test delta is exactly the local-store
tests that skip in CI); foundation **40 passed / 0
failed / 8 warnings**. OSF registry (osf.io/ybd65):
dated v4.9.0 blocks appended to the parent project,
the Program Outputs component (vwa7s), and the
Corpora component (dfrhz); the Literature component
is unchanged. Spec 025 task T15 marked DONE — Spec
025 is complete.

Spec 025 outcomes, as found: **Phase-139** — the
spec as sketched was NOT FREEZABLE (unit = locus
label, not an excavation unit; depth incommensurable;
context empty); gate: preservation PRIMARY CONTROL
(99.9%), chron_band SENSITIVITY (41.9%), depth_band
SENSITIVITY (51.1%); G1 ESTIMABLE. **Phase-140 (G1)**
— ICIT-lineage layer (horus84), permutation within
composition x preservation strata: chi2 4,966.36 vs
controlled null median 2,684.74; 0/9,999 >= observed;
raw p = 0.0001; BH over G1 alone (Q4(b), m = 1) ->
**SUPPORTED under control**; **chronology NOT
controlled** in the primary test (period/phase remain
uncontrolled confounders). EXPLORATORY bounds: S-chron
raw p 0.0001 (null median 2,809.53); S-depth raw
p 0.0001 (null median 2,682.78). **Phase-141 (LOSO)**
— L-MD OR 2.706 (1.858-3.940) p 0.0001; L-HA OR 2.162
(1.541-3.033) p 0.0002; L-KA OR 2.400 (1.857-3.103)
p 0.0001; **F1 STABLE under leave-one-site-out, no
single site load-bearing**; no q-values; no verdicts
minted. No anchor or PRED change — anchors sha256
eccea6d5... unchanged; PRED-2026-001/002/003 remain
PENDING.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution sec.VI.

## 2026-10-10 — Spec 026 S1: RCPH framework transfer — lifecycle, machinery, criteria freeze

Owner directive 2026-10-10: transfer the RCPH study framework
into Glossa, audit all prior Indus analyses against it, and
rerun everything the framework impacts. Spec 026
(specs/026-rcph-framework-transfer/) runs the full spec-kit
lifecycle with the AEE + evaluator extensions actually executed
and saved — Specs 024/025 left no saved assessment artifacts;
that gap is recorded as a finding in the spec.

S1 delivers: the 12-principle transfer map (headline: no
target-reading/language smuggling generalizes H26; origin-group
evidence accounting; discriminating controls with INVALID as
the consequence of a non-discriminating gate; verdict taxonomy
INVALID/INCONCLUSIVE/CONTRADICTED/SUPPORTED; canonical freeze
records; practical margins); the classification criteria,
FROZEN in this stage before any register exists; the governed
claim register (claims.json, 16 atomic claims); and the
machinery in backend/glossa_lab/framework026.py — dependency
integrity (cycles via aee_core ClaimGraph + the NEW
forbidden-assumption inheritance check the installed aee
package lacks) and canonical freeze build/verify, with 11 tests
incl. planted cycle, planted forbidden inheritance, and tamper
cases (all passing, ruff clean).

AEE record (aee/ in the spec dir): specify stage ran three
rounds — a vacuous 0-claim pass on prose (rejected as a gate
pass), gather_evidence on 8 compound claims (recovery:
decomposition into 16 atomic claims + second independent
evidence per claim), and a final gather_evidence with all 16
claims at 0.9945/high and 5 residual heuristic failure modes
whose named recovery actions were performed and recorded
(aee/recovery-specify.md). Plan and tasks stages: gather_evidence
(same profile); evaluator composed outcome under strict =
gather_evidence. Outcomes are recorded verbatim, not rounded up.

No anchors touched, no PRED scoring, no publication.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution sec.VI.

## 2026-10-10 — Spec 026 S2: Impact register frozen (116 items classified)

Under the criteria frozen at S1 (PR #138), every prior Indus
analysis is now classified in specs/026-rcph-framework-transfer/
impact-register.{json,csv,md} (generator:
backend/scripts/spec026_register_build.py; the build aborts on
any inventory/classification mismatch and --check is drift-free;
tests pin completeness and the exact rerun set).

Counts: RERUN-REQUIRED 8 — SPEC-023, SPEC-024, SPEC-025,
PHASE-132, PHASE-134, PHASE-135, PHASE-137, PHASE-140;
REPRODUCE-ONLY 12; REINTERPRET-ONLY 61 (incl. the INVALID blind-
affiliation runs 111/112/114, the calibration-rejected batteries
113/115/117/118, and the SA-era ledger-only cohort 52–104);
UNAFFECTED 27 (incl. Phase-107 as framework exemplar and
Phases 136/139/141, whose intervals/criteria were already on
record); NOT-RERUNNABLE 8 (Phases 92–95, 97–100 — no artifact
in any scoped location).

Reruns assigned: Phase-383 (C4 rescoring of the 132/134/135
coding pilots from on-disk records), Phase-384 (C1 margin
completion for Phase-137 F2/F3), Phase-385 (C1 margin completion
for Phase-140 G1), Phase-386 (deterministic replay spot set for
the REPRODUCE-ONLY verdict chain 116/125/127/131). The register
is a freeze point: reruns begin only after this stage merges.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution sec.VI.

## Spec 026 S3 — Rerun contracts + freezes + graph-first implementation

- Date: 2026-10-10. Stage S3 of Spec 026 (frozen plan). The
  S3 PR merges BEFORE any rerun executes.
- NUMBERING CORRECTION (Amendment 1 to the spec): the planned
  142–145 collide with the repository's existing global phase
  space (backend/reports runs to Phase-382; an
  experiment_graph_phase142_145.py module already exists).
  Reruns renumbered 383–386; the S2 register was corrected
  pre-merge (PR #139 amendment commit). Numbering only — no
  classification or criterion changed.
- Contracts (specs/026-rcph-framework-transfer/reruns/):
  phase383-contract.md (C4 rescoring of pilots 132/134/135 —
  rescoring only, origin-group audit, bootstrap CIs, gates =
  the pilots' own), phase384-contract.md (C1 for Phase-137
  F2/F3; margin V = 0.10 declared), phase385-contract.md (C1
  for Phase-140 G1; stratified bootstrap in the frozen strata;
  margin V = 0.10; chronology rider mandatory),
  phase386-contract.md (replay audit of 116/125/127/131 via
  disposable-worktree re-execution + comparator).
- Freeze records (framework026 canonical digests, verified
  in-tree at build): phase383 e94575c78f8e7a87…, phase384
  bf4356440ea035f3…, phase385 8af60b985d9994bc…, phase386
  38258f64cae2330d… (full records under reruns/).
- Graph-first (H15/H23): scripts written first, graph module
  experiment_graph_phase383_386.py second, registration in
  experiment_graph.py third, in-process registration check
  fourth (all four node IDs in ATOMIC_NODES) — all before any
  script execution beyond the contracts' own step-1
  verification, which reproduced the originals exactly
  (see tasks.md T12).

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI. No external correspondence sent.

## Spec 026 S3b — Phase-384/385 contract v2 (interval procedure corrected)

- Date: 2026-10-10. The Phase-384 v1 interval procedure
  (parametric bootstrap over table cells) FAILED its
  independence negative control: CI [0.1115, 0.1242] at true
  V = 0 (F2 margins), [0.0984, 0.1095] (F3 margins) — a
  non-discriminating procedure; its margin adjudication is
  INVALID under Spec 026 principle 5 (recorded in the
  Phase-384 report with v1 numbers preserved). Phase-385 v1
  used the correct resampling unit but a percentile-only
  interval that excluded its own point estimate
  ([0.2282, 0.2537] vs 0.2190).
- v2 contracts (reruns/phase384-contract-v2.md,
  phase385-contract-v2.md) + v2 scripts + new canonical
  freezes were frozen in this PR BEFORE any v2 execution.
  Corrections: inscription-level resampling (within site for
  384; within the frozen strata for 385) and the BASIC
  bootstrap interval as the governing interval. Margins and
  verdict rules unchanged (declared pre-run in v1).
- AI disclosure: Muse Spark via Muse, at the
  direction of Tristen Pierson, constitution sec.VI.
## Phase-383 (Spec 026 rerun) — C4 rescoring of pilots 132/134/135

- Date: 2026-10-10. Executed under the frozen Phase-383
  contract (digest e94575c78f8e7a87…, verified on the
  execution tree). Rescoring only; no re-coding.
- Every original headline value reproduces EXACTLY from the
  on-disk records (132: 0.20; 134: 0.84 / κ 0.7885; 135:
  0.78 / κ 0.7129; ILLEGIBLE per-category 0.667 / 0.368).
- New intervals (bootstrap over objects, B = 9,999): 132
  exact-seq CI [0.10, 0.32]; 134 agreement CI [0.77, 0.91],
  κ CI [0.689, 0.878]; 135 agreement CI [0.70, 0.86].
- Origin-group audit: all passes in all three pilots share
  ONE coder origin group (a single AI model family) —
  agreement is intra-origin consistency, not independent
  corroboration.
- Verdicts: 132 CONTRADICTED (stop-rule; CI far below the
  0.80 floor); 134 INCONCLUSIVE (middle band; the agreement
  CI reaches the 0.85 gate, so the "missed by one object"
  framing cannot be excluded on sampling grounds — and the
  CI spanning the gate is itself the finding); 135
  INCONCLUSIVE. Foundation check after the phase: 40/0.

## Phase-386 (Spec 026 rerun) — deterministic replay audit

- Date: 2026-10-10. Executed under the frozen Phase-386
  contract (digest 38258f64cae2330d…). Original scripts for
  Phases 116/125/127/131 re-executed in a disposable
  worktree; comparator outcome: ALL FOUR REPRODUCED on every
  compared headline quantity (116 median W1 + ρ; 125 median
  TV 0.636931, 16 judgeable, null 823/999; 127 null CI +
  bootstrap CI + share ≥ observed 0.0; 131 shares
  0.061321 / 0.938679). Anchors unchanged in every replay.
  Foundation check: 40/0.

## Phase-384 (Spec 026 rerun) — C1 margin completion for Phase-137 F2/F3

- Date: 2026-10-10. v1 (freeze bf4356440ea035f3…): χ²/V
  reproduced exactly from the recorded tables; its
  parametric cell-level bootstrap interval then FAILED the
  independence negative control (CI [0.1115, 0.1242] at true
  V = 0) — adjudication INVALID under principle 5, preserved
  in the report. v2 (contract + freeze 4e6c78bc917c96a3…
  frozen pre-execution in PR #142): inscription-level
  bootstrap within site, BASIC interval governing.
- F2 (Holdat, V 0.1154): basic CI [0.0589, 0.0778] — below
  the declared 0.10 floor → the bounded marginal claim is
  CONTRADICTED at the declared margin, converging with the
  original controlled-permutation NOT SUPPORTED (p = 0.7354).
- F3 (ICIT-lineage, V 0.2190): basic CI [0.1823, 0.2104] —
  SUPPORTED stands at the declared margin. Original
  confounder confessions unchanged.
- Foundation check after the phase: 40 passed / 0 failed.

## Phase-385 (Spec 026 rerun) — C1 margin completion for Phase-140 G1

- Date: 2026-10-10. v1 (freeze 8af60b985d9994bc…):
  population + χ² verified exactly; percentile-only interval
  [0.2282, 0.2537] excluded the point estimate (resampling
  bias) — superseded by v2 (freeze 9b20117a9ef1789d…, PR
  #142) with the BASIC interval governing, B = 4,999.
- G1 primary (composition × preservation strata): basic CI
  [0.1838, 0.2102] — entirely above the 0.10 floor →
  SUPPORTED under control STANDS at the declared margin.
  Chronology NOT controlled (rider). Exploratory S-chron /
  S-depth basic CIs [0.1848, 0.2098] / [0.1841, 0.2096].
- Foundation check after the phase: 40 passed / 0 failed.

## Spec 026 S5 — Closeout: historical assessments + verification

- Date: 2026-10-10/11. Historical assessments
  (specs/026-rcph-framework-transfer/historical-assessments
  .{md,json}; builder backend/scripts/
  spec026_assessments_build.py): all 116 register items
  assessed; **75 items carry a changed evidentiary status** —
  the 8 RERUN-REQUIRED rows (via Phases 383–386), the INVALID
  cohort (Phases 111–114 + Spec 017), the calibration-rejected
  cohort remapped to INCONCLUSIVE (115/117/118), the
  Phase-116/125/127 taxonomy mappings (bounded claims
  CONTRADICTED; diagnostics stand), the SA-era cohort
  (SPEC-004 + Phases 52–104: evidentiary status superseded
  under the H26 quarantine), and the NOT-RERUNNABLE cohort
  (Phases 92–95, 97–100: evidentiary ceiling — no claim-level
  weight). Original files and labels untouched throughout.
- AEE at implement stage: outcome gather_evidence (16
  claims, 0 below the 0.70 threshold, 5 residual heuristic
  failure modes) — recovery recorded in aee/
  recovery-implement.md; gaps register after verify: 0 open
  gaps (aee/gaps-implement.md).
- Program process notes (recorded for honesty): PR #139 was
  squash-merged minutes before its PR-head CI completed on a
  misread poll; the merged tree was subsequently verified
  green on BOTH the PR-head run (38107614340) and main's own
  run (38107756265), all jobs success, before any further
  merge. Separately, the v1 freeze records for Phases
  384/385 (and the shared graph-module coverage in all four
  v1 freezes) no longer verify against the current tree
  because the graph module changed for v2 — expected and by
  design: every freeze verified on its execution tree at run
  time, as recorded in the phase entries above.
- Full backend suite + foundation check on merged main and
  the anchors byte-identity check are recorded in the S5 PR
  and the program's final report. Anchors were not moved by
  any part of this program; no PRED scoring was performed;
  no publication was made (changed findings go to the owner
  first).

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI. No external correspondence sent.

## 2026-10-11 — Spec 027 DRAFT opened (movement, culture, and language)

- Draft PR #147 opened on branch
  `spec/027-movement-culture-language`; **left open,
  unmerged, and unfrozen**. This entry records a proposal,
  not an authorization.
- Spec 027 proposes Stage 0 (source-asserted settlement
  gazetteer + traced chronology spine, descriptive only),
  Stage 1 (Q2 repertoire gate with designed negative closure),
  conditional Stage 2 designs for Q7 and Q6, and a
  registered-but-blocked register for Q1, Q3, Q4, Q5, Q8, and
  Q9 with exact blockers and unblocking conditions.
- Governance: 33 claims in
  `specs/027-movement-culture-language/claims.json`; Spec 026
  integrity check passes. AEE outcomes after specify, plan,
  and tasks are all `pass`; composed strict evaluator outcome
  after tasks is `pass`. Tooling pinned per run (specify
  1.0.10; AEE extension v1.1.0; evaluator v1.0.0; AEE package
  1.0.4 from the Glossa venv).
- No stage was executed, no dataset was acquired or copied,
  no publication was made, no external party was contacted,
  no anchor changed, and no PRED-2026 scoring occurred.

AI disclosure: drafted by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-21 — Spec 060 EXECUTED (Phase-422): margin curve published (sensitivity); COMPOSITION DOES NOT on the shared population

Spec 060 was executed in full as Phase-422
under the frozen contract (freeze digest
8c04b1a8…; OSF registration 8ywxc approved
and public, DOI 10.17605/OSF.IO/8YWXC), in
Wave 3 Group 2 of the runnable-experiments
campaign, from origin/main at 3200b7b5.
Graph-first build (H15/H23): script
backend/scripts/phase422_f2_margin_curve.py,
graph node IndusPhase422F2MarginCurve,
registration verified by import before the
run. Gate 0.1 PASS: every spec §3 input
hashes to its stated value by two routes,
including both held layers at the Phase-137
loaders' default paths (Holdat 62d14d2b…;
ICIT c368f290…). Gate 0.2 PASS: both layers'
recorded profile tables reproduce exactly
(Holdat 1,670 inscriptions, 9 × 98, χ²
745.953, V 0.1154; ICIT 5,410, 7 × 187, χ²
4966.362, V 0.2190). Gate 0.3 PASS: the
Phase-384 v2 estimator, imported unchanged,
reproduces both recorded governing intervals
float-for-float (F2 basic [0.058939204306206666,
0.0777941604081594]; F3 basic [0.18229651053139323,
0.21036863506165235]). Gate 0.4 PASS: the
shared-population census (site intersection
re-derived: Chanhu-daro, Dholavira, Harappa,
Kalibangan, Lothal, Mohenjo-daro) retains
1,516 Holdat inscriptions and 2,139 ICIT
SEAL inscriptions, above the frozen floors.
Arm 1 (sensitivity display): the F2 margin
curve on the fixed grid — SUPPORTED AT 0.05,
STRADDLES 0.075, CONTRADICTED AT 0.10,
CONTRADICTED AT 0.125, CONTRADICTED AT 0.15 —
on governing interval [0.0589, 0.0778], point
V 0.1154; the recorded verdict at 0.10 stands
and no cell replaces it. Arm 2: on the shared
population (SEAL; DD-060-12), under identical
code with signs never pooled or mapped, the
Holdat governing interval [0.055251710457321024,
0.07607996659365032] (point V 0.1154) and the
ICIT governing interval [0.08368810617885544,
0.10835095759573735] (point V 0.1349) still
exclude each other — COMPOSITION DOES NOT,
recorded in the frozen §6.3 wording alongside
Spec 034's finished attribution (ATTRIBUTED
TO COMPOSITION on 169 matched objects, all
Mohenjo-daro seals): both statements stand,
neither edits the other, and no successor
study is designed or implied. Period mix:
PERIOD MIX NOT DESCRIBED FOR THIS LAYER -
FIELD NOT CARRIED for both layers (DD-060-13);
no period assignment was imported. No verdict
moves: F2 stands CONTRADICTED at 0.10 and F3
stands SUPPORTED at 0.10, exactly as recorded.
A second full run reproduced every quantity
identically. Anchors asserted byte-identical
before and after (df0cf620…). Foundation
check at the run: 40 passed / 0 failed /
8 warnings. Records:
specs/060-f2-margin-curve/outcome.md,
reports/phase422_results.json,
reports/phase422_report.md.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 027 FROZEN (owner adjudication of §13)

- Owner decision (Tristen Pierson, 2026-10-11 08:26 EDT,
  verbatim): "Approve Spec 027 with the recommended answers
  and freeze it." Binding record:
  `specs/027-movement-culture-language/adjudication.md`.
  Answers: Ask 1 → 0A (gazetteer + chronology spine in one
  Stage 0; order Stage 0 → Stage 1 gate → conditional
  Stage 2); Ask 2 → M77 governs Stage 1 (Parpola/CISI only as
  a separately labelled crosswalk-v1 sensitivity; Wells/ICIT
  not governing); Ask 3 → corpus inclusion rules approved as
  drafted; Ask 4 → CC BY 4.0 publication through the release
  gate for lawfully reusable rows only; Ask 5 → Stage 1
  executes on the adjudicated design once its own freeze is
  committed and merged.
- Stage phase numbers named at the freeze: Stage 0 =
  Phase-391, Stage 1 = Phase-392 (registered space ends at
  Phase-386; 387–390 are claimed by the docstring of the
  legacy unregistered phase382_390_actionable.py).
- AEE assess + evaluator-contract run for the freeze state:
  pass (33 claims, 0 failure modes, 0 below the 0.70
  threshold); outputs in
  `specs/027-movement-culture-language/aee/` with the phase
  mapping recorded in `freeze-aee-note.md`. claims.json is
  byte-identical to the draft-final register (sha256
  7d27d401…); Spec 026 integrity check passes (no cycles, no
  missing dependencies, no forbidden inheritance).
- No stage executed by this entry; no dataset acquired, no
  publication, no anchor change, no PRED-2026 scoring.

AI disclosure: recorded by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 027 Stage 0 EXECUTED (Phase-391: gazetteer + chronology spine)

- Freeze: `specs/027-movement-culture-language/stage0-freeze.md`
  + `stage0-freeze.json` (digest 4a9f6953… (final, after Amendments 1-3 recorded in the freeze); verify_freeze
  clean at merge). Three amendments recorded in the
  freeze (Mutin Table S2 regex anchoring; empty-material
  representation as `unknown`; release-CSV line endings) —
  the first two fired by the build's own assertions before
  any product was written, the third was caught at staging
  before commit; no frozen rule, count, or criterion
  changed.
- H15/H23 gate in order: script
  `backend/scripts/phase391_stage0_spine.py` → graph module
  `experiment_graph_phase391_392.py` → registration verified
  (`IndusPhase391Stage0Spine` in ATOMIC_NODES) → run.
- Gazetteer: 36 source-asserted rows (CISI Vol. 1 layer 11,
  Vol. 2 layer 4, XRONOS 21) over 30 program site clusters
  (5 multi-source). Licence states: verified_open 21 /
  open_access_read_only 15. Coordinate states:
  exact_published 21 / unknown 15. CISI non-site catalogue
  rows excluded: 526.
- Chronology spine: 177 traced rows (XRONOS 144 + Mutin et
  al. 2025 SI Table S2 33, scenario CONTESTED). Context
  grades: direct 33 / associated 36 / unassessed 108.
  Material classes: long-lived 105 / short-lived 57 /
  unknown 15. XRONOS's filtered export contains no
  Mohenjo-Daro, Harappa, Mehrgarh, Rakhigarhi, Dholavira,
  Kalibangan, or Lothal dates — recorded as a coverage
  statement in the report.
- Q6 timing-support assessment (criteria frozen in the Stage
  0 freeze before the build): **NOT-YET-TESTABLE** — regions
  with ≥2 window sites 1/3 required (FAIL); window
  direct/associated sites 5/10 (FAIL); window short-lived
  share 0.0/0.5 (FAIL); median window σ 70 BP ≤ 80 (PASS).
  No trait-timing outcome was inspected.
- Ask 4 release package prepared in
  `specs/027-movement-culture-language/stage0-release/`
  (verified_open rows only: gazetteer CSV 21 rows, chronology
  CSV 177 rows, source register verbatim, README, manifest).
  Release gate run in-repo: **PASS 4/4** (1 MATCH, 3 EXTERNAL
  with hashes recorded; output saved in the package).
  **No external deposit made** — the package is deposit-ready
  for a future owner order.
- Products: `data/movement/gazetteer_rows.jsonl`,
  `data/movement/chronology_rows.jsonl`,
  `data/movement/source_register.json`,
  `reports/phase391_results.json`,
  `reports/phase391_stage0_report.md`. Anchors
  byte-identical; no PRED scoring.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 027 Stage 1 FREEZE (Phase-392, Q2 gate)

- Freeze record: `specs/027-movement-culture-language/
  stage1-freeze.md` + `stage1-freeze.json` (framework026
  digest 9c937fbc5c0fb86b48478d66a6894a708b8e2fd36eb45c098740
  8ed01bc4a42a). Ask 5 authorises execution on this freeze's
  merge; no separate owner go.
- Margins-only audit first (Phase-139 pattern; no-peeking
  fence pinned by test): flow 5,679 → dedup-kept 4,531 →
  site-'Unknown' excluded 26 → SEAL/TAB 3,605 → legible >= 2
  → eligible 3,144 (52 sites). Analysis population: 6 sites
  >= 20 (Harappa 1,437; Mohenjo-daro 1,302; Dholavira 111;
  Lothal 74; Chanhu-daro 54; Kalibangan 52) = 3,030.
  Graffiti POT:T:g (473 kept) excluded from every Stage 1
  population. Join: 5,678/5,679 (one unjoined record flagged
  UNRECORDED metadata).
- Frozen design: per-inscription M77 composition (125
  columns: 123 signs >= 10 tokens + UNMAPPED + OTHER),
  Bray-Curtis PERMANOVA R^2 for site; rarefaction to cell
  n = 15 within site x type-class (10 cells, 150/draw);
  R = 199 draws; B = 499 permutations within type strata;
  seed 20261011; margin R^2 = 0.01 (declared convention);
  discriminating negative + positive controls (failure =
  INVALID); LOSO over the 6 sites; S-complete sensitivity
  (labelled, no verdict); period not a stratum (59.2%
  uninformative on this layer, Phase-139).
- Parpola/CISI sensitivity assessed on margins and recorded
  NOT ESTIMABLE at the frozen sign-by-sign unambiguity rule
  (17.57% unambiguous token coverage vs 99.94% any-pair);
  not run. M77 primary stands alone.
- Multi-line status is not recorded in the ICIT-lineage
  layer; eligibility is governed by the legible-token rule
  alone — recorded in the freeze as a stated boundary of the
  bounded claim.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 027 Stage 1 freeze AMENDMENT 1 (pre-merge, pre-outcome)

- Three changes to the Stage 1 freeze before its merge,
  forced by machinery smoke tests on SYNTHETIC data only (no
  real repertoire outcome computed): (1) estimand scale =
  adjusted PERMANOVA R^2 — the raw R^2 null expectation
  (g-1)/(n-1) sits above the 0.01 margin at any feasible
  cell size, which made the negative control unpassable and
  the margin comparison vacuous; (2) rarefaction cell size
  15 -> 49 (largest keeping all 6 sites, >= 8 cells; 392
  inscriptions/draw); (3) positive-control sign sets made
  deterministic (disjoint blocks of the 60 most frequent
  sign columns) after simulation showed seed-drawn sets made
  the planted effect luck-dependent (0.012-0.027).
- Calibration at the amended design (identical pipeline,
  synthetic populations): negative control PASS; positive
  control PASS (median adjusted R^2 0.0198, interval
  [0.0153, 0.0258], 100% draws rejecting). Amended freeze
  digest 30861f04... Full text: stage1-freeze.md Amendment 1.
- Process note: a VM replacement mid-program (2026-10-11
  ~13:12 EDT) wiped /tmp scratch (incl. one un-run smoke
  test's output) but no committed work; worktrees and stores
  under ~/workspace were intact. The backend was restarted
  by the watchdog per its standing job.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.
## 2026-10-11 — Zenodo v4.10.0 published (Spec 026: framework transfer, impact register, Phases 383–386): Phase-132 CONTRADICTED; F2 CONTRADICTED at the declared margin; F3 + G1 SUPPORTED stand; 75 historical assessments

**Zenodo v4.10.0 published 2026-10-11** — DOI
10.5281/zenodo.23298334 (record 23298334); concept DOI
10.5281/zenodo.20379070 unchanged. The deposit (59
files) adds the Spec 026 program note
(`pierson_2026_indus_program_note_383_386_spec026.md`)
and the Spec 026 record (transfer map, claim
register, classification criteria, impact register
md/json/csv + register classifications, Phase-383–386
rerun contracts and freezes, the four rerun reports
and results files, and the historical assessments
md/json, CC BY 4.0) to the carried-forward v4.9.0
set. Publication flow per docs/RELEASE_CHECKLIST.md:
program note + `RELEASE_VALIDATION.json`
`release_v4_10_0` entry via PR #149 (merge 2aa52c81);
mandatory release gate run at 2aa52c81 — **PASS
59/59** (58 MATCH + 1 EXTERNAL, the carried-forward
v3 preprint PDF byte-identical to the v4.9.0 record);
gate recorded via PR #150 (merge e42db25a); final
gate run against the merged gate-record commit
e42db25a — **PASS 59/59**, exit 0 (final staged
`RELEASE_VALIDATION.json` sha256
0055704016fb21ebd1c912fa77aac6dfc0081737021c178c7445d4705c9db9c7).
Post-deposit confirmation: **59/59** file checksums
(MD5) on record 23298334 match the staged files; the
DOI resolves. Suite and foundation at the release
commits: Spec 026 closeout verification on merged
main bf85ff31 — full backend suite **1,152 passed /
12 skipped / 0 failed** (the executing session's
terminal record; an early completion summary's
3,647-passed figure was a misread mid-run poll
fragment, corrected on the record the same day and
used nowhere in this release), foundation **40
passed / 0 failed**; main CI run 38110406069 on
bf85ff31 completed success; release PRs #149/#150 CI
verified from their runs' own conclusions (38139670443
and 38140305450, both completed success, 7/7 jobs).
OSF registry (osf.io/ybd65): dated v4.10.0 blocks
appended to the parent project, the Program Outputs
component (vwa7s), and the Corpora component (dfrhz);
the Literature component is unchanged.

Spec 026 outcomes, as found: **Framework transfer**
— 12 RCPH principles adopted with Indus adaptations
(transfer map; 16 governed claims); recorded
residuals: evaluator extension has no registered
evaluators in this repo; AEE package version split
across venvs (1.0.4 / 1.0.2), pinned per run.
**Impact register** — 116 items (Specs 001–025 +
Phases 52–141) under criteria frozen before
classification: RERUN-REQUIRED 8, REPRODUCE-ONLY 12,
REINTERPRET-ONLY 61, UNAFFECTED 27, NOT-RERUNNABLE 8
(Phases 92–95, 97–100, artifacts only in outputs/).
**Phase-383** — pilots 132/134/135 rescored from
on-disk records, all original values exact; 132
**CONTRADICTED** (exact-seq CI [0.10, 0.32] vs the
0.80 floor); 134/135 **INCONCLUSIVE** (CIs span their
gates); origin-group audit: ONE coder origin group
across all pilots — agreement is intra-origin
consistency, not independent corroboration.
**Phase-384** — margin V = 0.10 declared pre-run;
the rerun's v1 interval procedure **INVALID**
(self-caught: CI [0.1115, 0.1242] at true V = 0 on
its discriminating control; preserved, not used);
v2 BASIC intervals: F2 [0.0589, 0.0778] — bounded
claim **CONTRADICTED at the declared margin**,
converging with the original NOT SUPPORTED
(p = 0.7354); F3 [0.1823, 0.2104] — **SUPPORTED
stands** at the margin. **Phase-385** — G1 BASIC CI
[0.1838, 0.2102] — **SUPPORTED under control stands
at the declared margin**; **chronology NOT
controlled** in the primary test (standing rider).
**Phase-386** — Phases 116/125/127/131 replayed in a
disposable worktree: **all REPRODUCED exactly**; no
verdict changes. **Historical assessments** — 75 of
116 items carry a changed evidentiary status
(INVALID cohort 111–114 + Spec 017; 115/117/118 →
INCONCLUSIVE; SA-era cohort superseded under H26;
NOT-RERUNNABLE ceiling 92–95/97–100); original files
and labels never rewritten. No anchor or PRED
change — anchors sha256 eccea6d5... unchanged;
PRED-2026-001/002/003 remain PENDING.

**AI disclosure:** execution recorded by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution sec.VI.

## 2026-10-11 — Spec 027 Stage 1 freeze MERGED; OSF registration filed (Phase-392 contract)

- Stage 1 freeze merged as PR #154 (merge 4684408f) on CI
  run 38144799989 verified success from the run's own
  conclusion and job list. (PR #153, the original freeze PR,
  was closed as superseded: during a ~37-minute GitHub
  Actions trigger outage its post-amendment head never
  received a run — zero check-runs on the head via the API
  across two synchronize pushes, a close/reopen, and an
  empty commit. #154 carried the identical commits; the
  freeze merged on green CI only.)
- OSF follow-on executed (owner-directed 2026-10-11; the
  Spec 027 design registration osf.io/a2xvc recorded the
  same follow-on): the exact frozen Stage 1 contract
  registered on OSF BEFORE Stage 1 execution —
  https://osf.io/pnqrx/ (OSF Preregistration schema;
  filed 2026-10-11T14:02:01Z; public, no embargo; pending
  admin approval at filing, state 'initial'). Record:
  specs/027-movement-culture-language/stage1/
  osf-registration.md (incl. the source-node 410 and the
  draft-submit 404 API notes). Stage 1 execution proceeds
  only after this filing.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 027 Stage 1 EXECUTED (Phase-392): verdict INCONCLUSIVE

- Execution after the OSF filing (osf.io/pnqrx), under the
  merged Stage 1 freeze (digest 30861f04... see freeze
  entry; H23 order observed, registration verified at 471
  nodes). Population reproduced exactly before outcomes
  (eligible 3,144; analysis 3,030; 125 columns).
- Primary: median adjusted PERMANOVA R^2 0.01677, 95%
  interval [0.01032, 0.02397] (entirely above the frozen
  0.01 margin); share of 199 rarefaction draws rejecting
  1.000 (median p 0.002). Controls PASS (negative median
  adj R^2 0.00020, rejection share 0.005; positive median
  adj R^2 0.02121, interval [0.01580, 0.02760], rejection
  1.000) — the instrument discriminates at the design's
  operating point.
- Jackknife: dropping Harappa takes the median adjusted
  R^2 to 0.00928 (below margin); all other drops
  0.01677–0.01863. Under the frozen verdict rules the
  SUPPORTED rule therefore fails on its jackknife clause
  while the CONTRADICTED rule does not fire: **verdict
  INCONCLUSIVE** (the freeze's named case — jackknife range
  crosses the margin while the primary interval does not).
  Detection is unanimous; the margin-clearing effect is
  partially load-bearing on the corpus's dominant site.
- S-complete sensitivity (labelled, no verdict): median
  adj R^2 0.01793, interval [0.01139, 0.02868], rejecting
  1.000 — consistent with the primary.
- Consequences per the frozen rules: the section 7.2
  negative closure does NOT fire (bound to CONTRADICTED);
  INCONCLUSIVE authorises no downstream repertoire work.
  Stage 2 not executed (Q6 NOT-YET-TESTABLE from Stage 0;
  Q7 unfrozen). Phase-137 F3's SUPPORTED verdict is not
  revised (different layer, different frozen design; the
  two results stand side by side — see stage1-outcome.md).
  No anchor or PRED contact.
- Deviation recorded: the first launch stopped INVALID on
  a defective population-guard comparison (sorted vs
  unsorted site list); the stopped run's recorded flow was
  diffed against the frozen audit and reproduced it
  exactly — the guard, not the population, was wrong. One-
  line fix committed (1646de2f), relaunch reproduced the
  population and ran clean (155 s). Full record:
  specs/027-movement-culture-language/stage1-outcome.md.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 027 CLOSEOUT (Stages 0-1 program complete)

- Verification on merged main (a0c8566a, after PRs #147
  freeze / #151 Stage 0 / #154 Stage 1 freeze / #155 Stage
  1 execution): full backend suite **1,162 passed, 14
  skipped, 0 failed** (475.6 s, local run on the merged
  tree; each program PR additionally merged on CI verified
  from its run's own conclusion); foundation check **40
  passed, 0 failed, 8 warnings**; anchors
  INDUS_FINAL_ANCHORS.json byte-identical (sha256
  eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3
  b602cfaed); PRED register untouched (zero program commits
  on docs/PREDICTION_REGISTER.md).
- Program record: adjudication + freeze (PR #147, d9fa0806;
  design registered osf.io/a2xvc); Stage 0 Phase-391
  (PR #151): gazetteer 36 rows, chronology spine 177 rows,
  Q6 timing-support NOT-YET-TESTABLE, Ask 4 release package
  gate PASS 4/4 in-repo, no deposit; Stage 1 freeze
  (PR #154, digest 30861f04...) + OSF registration of the
  frozen contract (osf.io/pnqrx, filed before execution);
  Stage 1 Phase-392 (PR #155): verdict INCONCLUSIVE.
- Stage 2 was NOT executed (per program scope): Q6
  NOT-YET-TESTABLE on the Stage 0 spine assessment; Q7
  unfrozen and owner-gated. Any further Spec 027 work —
  a redesigned Stage 1 estimand, a Q7 freeze, a Q6 spine
  extension — requires a new owner decision.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Zenodo deposit: Spec 027 Stage 0 gazetteer + chronology spine (Phase-391), standalone dataset, CC BY 4.0

**Zenodo deposit published 2026-10-11** — DOI
10.5281/zenodo.23300361 (record 23300361; the new
record's own concept DOI 10.5281/zenodo.23300360). This
is a **standalone dataset record**, not a version of
the glossa-lab archive (concept DOI
10.5281/zenodo.20379070, cited as a related identifier,
relation isPartOf). Owner order 2026-10-11: "Deposit
the Stage 0 gazetteer package on Zenodo (CC BY 4.0)" —
executing the Spec 027 Ask 4 adjudicated posture
(owner, 2026-10-11): CC BY 4.0 via the release gate
for lawfully reusable rows only; restricted
coordinates never more precise than source state;
catalogue-only sources excluded.

Deposit (4 files, exactly the Phase-391 package at
`specs/027-movement-culture-language/stage0-release/`,
source commit 9a202fe95737c23aedd78edc9eb8df86be9a7a87):
`indus_gazetteer_stage0_ccby.csv` (21 verified_open
rows, XRONOS — the full Stage 0 gazetteer holds 36
source-asserted rows; the 15 open_access_read_only
CISI-derived rows are EXCLUDED from CC BY
redistribution; Possehl/Law/TwoRains/c14bazAAR are
catalogue-only and contribute no rows);
`indus_chronology_spine_stage0_ccby.csv` (all 177
traced rows: XRONOS 144 + Mutin et al. 2025 SI Table
S2 33, every Mutin row flagged scenario CONTESTED,
preserved as published — the Mehrgarh redating
scenario remains unreplicated and is NOT adopted);
`source_register.json` (verbatim from
`data/movement/source_register.json`);
`STAGE0_RELEASE_README.md` (package documentation).

Release gate (`backend/scripts/release_gate.py` per
docs/RELEASE_CHECKLIST.md): recorded at Phase-391 and
**re-run at 9a202fe9** in a fresh clean worktree before
deposit — **PASS 4/4** (1 MATCH + 3 EXTERNAL), exit 0,
hashes identical to the Phase-391 record. Staged
sha256: gazetteer 554609aada04…, spine b580d1903440…,
README d6b4ad7db765…, source_register 6e1a543fa785…
(MATCH against repo source). Post-deposit
confirmation: record 23300361 file checksums (MD5)
re-pulled from the Zenodo API — **4/4 match** the
gated staged files (gazetteer 80eea80316d790dcd4…,
spine ef6aef3a255248ee…, README d9a554a1e1dfbb60…,
source_register 7b5345a1aa9a5e50c11…); the DOI
resolves (HTTP 302 to the record). Validation entry:
`outputs/RELEASE_VALIDATION.json`
`spec027_stage0_gazetteer_deposit`. Related
identifiers on the record: glossa-lab concept DOI
(isPartOf), GitHub repo (isDerivedFrom), OSF Spec 027
registration osf.io/a2xvc (isDocumentedBy), Mutin et
al. 2025 DOI (isDerivedFrom), XRONOS (isDerivedFrom).

The deposit is descriptive infrastructure: it carries
no decipherment claim and no linguistic affiliation
for any site or period. No anchor file was deposited
or modified — anchors sha256 eccea6d5… unchanged;
PRED-2026-001/002/003 untouched, still PENDING; no
other deposit or send was made in this program.

**AI disclosure:** executed by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution sec.VI.
## 2026-10-11 — Spec 028 FREEZE (Phase-393, Harappa robustness)

- Owner order (verbatim): "Also do the Harappa robustness
  design follow up and execute it based on what you think
  the best way forward is." Design authority delegated to
  the program; recorded in
  specs/028-harappa-robustness/adjudication.md. No separate
  owner adjudication round for this spec.
- Design: Arm A (confirmatory, primary) — the Phase-392
  analysis population minus Harappa (1,593 records, 5 sites)
  through the identical Phase-392 machinery; Arm B
  (confirmatory, secondary) — site-equal-weight estimand on
  the full population (quota 52 per site per draw); Arm C
  (exploratory, descriptive only) — Harappa decomposition.
  Hierarchical reporting; no pooled headline. Verdicts are
  per arm under the Spec 026 taxonomy.
- Freeze inputs: margins-only audit reproducing the
  Phase-392 frozen counts exactly (eligible 3,144; analysis
  3,030; 125 columns; both arms ESTIMABLE on margins) and a
  synthetic-only calibration. Calibration forced Amendment
  1 (pre-merge, pre-outcome, synthetic evidence only):
  controls regenerate their synthetic population per draw
  (the inherited single-population construction made the
  negative control's rejection share a generation-seed
  lottery: 0.171/0.156 vs 0.015/0.000); permutation strata
  refined to type class x legible-length value; the negative
  control's PASS bound restated with its binomial tolerance
  (share <= 0.10). Final calibration: all four controls PASS
  (Arm A neg 0.00046/share 0.040, pos 0.02396/[0.0156,
  0.0336]; Arm B neg 0.00204/share 0.055, pos 0.01670/
  [0.0105, 0.0240]).
- Freeze record: specs/028-harappa-robustness/freeze.md;
  machine record freeze.json digest
  619ab0c30048b934a14f2f2e7583a1a2e93c25c0599488f97165c285c
  d38bb61. Claim register 16 claims, integrity check PASS;
  AEE assess PASS at after_specify (after two recovery
  rounds), after_plan, and after_tasks. Seed 20261012.
- Sequencing from here: freeze PR merges on verified CI ->
  OSF registration of the frozen contract -> Phase-393
  execution under H23. No anchor or PRED contact; Phase-392's
  record is never modified by this spec.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 028 OSF registration filed (Phase-393)

- Frozen Spec 028 contract registered on OSF BEFORE any
  execution, per the frozen sequencing:
  **https://osf.io/7m35w/** (filed 2026-10-11T16:13:11Z;
  OSF Preregistration schema; node 93bqh; 29 response
  fields from freeze.md as amended; public, no embargo;
  approval pending at filing — approvals are the agent's
  standing job in the parent loop, owner order
  2026-10-11). Record:
  specs/028-harappa-robustness/osf-registration.md.
- Freeze provenance: PR #158 merged c1fc0029; CI run
  38153881380 success verified from the run's own
  conclusion (7/7 jobs). Phase-393 execution follows
  under H23.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 028 EXECUTED (Phase-393): Arm A INCONCLUSIVE, Arm B INCONCLUSIVE

- Single clean run under the merged freeze + OSF
  registration (osf.io/7m35w): 540.6 s, seed 20261012;
  population guard reproduced the frozen margins exactly;
  executed controls reproduce the pre-freeze calibration's
  summaries numerically, exactly.
- **Arm A (primary) INCONCLUSIVE:** median adjusted R^2
  0.00878 (BELOW the 0.01 margin), interval [0.00463,
  0.01297], rejection share 0.623; all five LOSO medians
  below the margin (0.00656-0.00948); S-complete 0.00647;
  controls PASS. The non-Harappa sites do not clear the
  margin on their own; CONTRADICTED does not fire (the
  interval straddles the margin).
- **Arm B (secondary) INCONCLUSIVE:** median 0.02237
  (ABOVE Phase-392's 0.01677), interval [0.01222, 0.03333]
  entirely above the margin, share 0.955 — but the
  drop-Harappa LOSO median is 0.00661, failing the frozen
  jackknife clause exactly as in Phase-392; every other
  drop >= 0.0226. Controls PASS; quota allocations match
  the frozen table exactly.
- Joint reading (descriptive, no verdict upgraded):
  margin-clearing is Harappa-dependent under both
  weightings, and is NOT an inscription-count artifact
  (equal weighting raises the estimate). Arm C
  (exploratory): Harappa's distance from the other sites
  (BC 0.3410) is carried by its tablets (within-TAB
  0.4953 vs within-SEAL 0.1114); M328 alone contributes
  ~21.5% of the distance. Full record:
  specs/028-harappa-robustness/outcome.md; reading of
  Phase-392 updated only in
  specs/028-harappa-robustness/historical-assessment-
  phase392.md (Phase-392's record untouched).
- Deviations: two aborted launches in the execution
  script's non-frozen glue (wrong loader name; pipeline
  slice two lines short), both before any outcome; fixed
  in the script's own sections only; the clean run is the
  single executed run. Recorded in outcome.md.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 028 CLOSEOUT (program complete)

- Verification on merged main (909b239a, after PRs #158
  freeze / #159 OSF record / #160 execution): full backend
  suite **1,170 passed, 14 skipped, 0 failed** (504.3 s,
  local run on the merged tree; each program PR merged on
  CI verified from its run's own conclusions — runs
  38153881380, 38154592997, 38156384573, all success 7/7);
  foundation check **40 passed, 0 failed, 8 warnings**;
  anchors INDUS_FINAL_ANCHORS.json byte-identical (sha256
  eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3
  b602cfaed); PRED register untouched (zero program
  commits on docs/PREDICTION_REGISTER.md).
- Program record: delegated adjudication + freeze
  (PR #158, digest 619ab0c3...); OSF registration of the
  frozen contract (osf.io/7m35w, filed before execution);
  Phase-393 execution (PR #160): Arm A INCONCLUSIVE,
  Arm B INCONCLUSIVE, Arm C exploratory decomposition.
  Phase-392's record was never modified; its updated
  reading lives in the Spec 028 historical assessment.
- Follow-on boundary: any new test of the Harappa /
  tablet-specific structure Arm C describes requires a
  NEW spec, freeze, and registration. Nothing in Spec 028
  pre-registers or authorises it.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-11 — Spec 028 bookkeeping correction

- The L9/R1/E1-E5/X1-X2 task ticks in tasks.md were applied
  with title patterns that did not match the file's final
  task titles and silently missed in PRs #159/#160/#161;
  the work itself was completed and verified as recorded
  in the entries above. This entry's PR applies the ticks
  correctly. No record content changes.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — PRED-2026-004/005/008/009 retired (owner decision)

- Owner decision (Tristen Pierson, 2026-10-12): retire
  PRED-2026-004, PRED-2026-005, PRED-2026-008, and
  PRED-2026-009 in docs/PREDICTION_REGISTER.md.
- Recorded under the register's append-only discipline as
  a new dated §6 adjudication note; the §3 entries are
  unchanged. Each prediction: RETIRED — untested, never
  scored, NOT refuted. Cause: the registered success
  criterion is defined on, or depends on, the Phase 9
  simulated-annealing (SA) machinery that Phase-107
  falsified (held-out 0.000, 0/115), so each prediction
  is untestable as registered. PRED-2026-009 is the
  negative control for that same SA line and has no live
  test to control.
- Any successor must be registered as a NEW prediction
  number under an SA-free method; retired numbers are
  not reused.
- PRED-2026-001/002/003 remain PENDING; PRED-2026-006/007
  remain PARTIALLY CONFIRMED. No anchors, phases, code,
  or data changed — documentation only.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 drafted (claims-first): Tao claim lifecycle

- Owner directive (Tristen Pierson, 2026-10-12): realign
  Glossa-Lab's claim handling on Terence Tao's points —
  five claim stages (created, checked, explained,
  accepted, digested), decomposition of headline claims,
  digestion as first-class tracked work, attribution as a
  claim, anti-gradability, two lanes, provenance protecting
  priority, inspectable evidence trails.
- New draft spec `specs/029-tao-claim-lifecycle/`:
  `assessment.md` (gap assessment of the current claim
  machinery against the eight points, with file evidence —
  headline finding: no lifecycle, decomposition, digestion,
  or attribution machinery exists, and
  `frontend/src/components/DeciphermentPanel.tsx` renders a
  "signs deciphered" volume headline the standard forbids),
  `spec.md` (claims-first draft), and `claims.json`
  (register F029-C01…C10, all draft).
- Claims-first discipline: NO plan.md and NO tasks.md were
  written; nothing is frozen; six owner decisions are
  recorded open in spec §8 (OD-1…OD-6). Under claim
  F029-C10 the draft itself changes no claim, anchor,
  verdict, score, or display.
- Opened as a DRAFT PR for owner adjudication. Not merged.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 retroactive realignment audit (append-only reclassification)

- Owner directive (Tristen Pierson, 2026-10-12): the Tao
  realignment is retroactive — audit and re-run the
  discipline across ALL previously done work and prove
  the current claim set is disciplined under the eight
  points. Executed claims-first against the draft Spec
  029 (PR #164): NO code changed, NO live record edited.
- Deliverables appended in
  `specs/029-tao-claim-lifecycle/`: `audit.md` (the
  written audit) and `reclassification-ledger.json`
  (345 dated reclassification entries: 287 anchors, 31
  extracted claims, 3 hypothesis records, 5 live PRED
  items, 10 study-headline entries, 3 grouped instrument
  records, 6 presentation-surface flags).
- Inventory reconciled: 287 anchors reconcile across
  the canonical file, the Phase-108 register, and the
  foundation report; the strict set recomputed from the
  register + Phase-109 rule = 94 (90 HIGH + 4 MEDIUM),
  matching the published figure; extracted claims
  verified as exactly 31 (a single 2026-10-09
  re-extraction batch from 10 documents — the
  distribution differs from the Phase-104 record
  because the set was regenerated, with two propositions
  double-recorded).
- Honest stage distribution after the re-run: created
  220, checked 116, explained 0, accepted 0, digested 0.
  Nothing in the program carries a named-human
  explanation or digestion record; 105 entries are
  flagged verified-but-unexplained (strict 94 + 8
  supported-class claim records + F1/F3/G1 headlines).
- Worst nonconformances named with evidence in the
  audit: the DeciphermentPanel "signs deciphered"
  headline; the dashboard API still serving the
  falsified SA aggregate and a "fully decoded %"; 33
  HIGH anchors with SA in their provenance chain
  displayed indistinguishably from strict HIGH; 17 of
  31 extracted claims with no falsifier (including 2
  displayed strongly_supported); the exposed
  mean_propagated_score (0.484903).
- Unfixable published surfaces labelled HISTORICAL
  LIMITATION in the audit: the v4 preprint (DOI
  10.5281/zenodo.20414696; SSRN 6827038), Zenodo
  releases v4.1.0–v4.10.0, the frozen OSF PRED mirror
  (bg8yx), the phase-era report corpus, and the retired
  repo description (residual).
- Owner decisions recorded open in audit §9: evidence
  for OD-1 (two nonconforming displays are live
  machinery, not archived text) and OD-3 (attribution
  contest is material in the governed population), plus
  D-A (annotate the 33 chained HIGH) through D-E (where
  the stages live). Display fixes remain gated behind
  Spec 029 adjudication; PR #164 stays DRAFT, unmerged.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 owner adjudication: OD-1 through OD-6 ratified as a block

- Owner decision (Tristen Pierson, 2026-10-12, verbatim):
  "ratify all of these as a block and do it" — adopting
  the program's recommendations for `spec.md` §8 (OD-1
  through OD-6) exactly as presented. Recorded in
  `specs/029-tao-claim-lifecycle/adjudication.md`;
  `spec.md` §8 annotated DECIDED 2026-10-12 under each
  item with the original question text preserved.
- OD-1: immediate re-staging of all existing claims as
  one dated reclassification event; the retroactive
  audit's ledger is the re-staging record; stage =
  highest stage whose evidence exists in the record.
- OD-2: the explanation gate accepts a named, accountable
  human author (internal or external) with a durable
  public citable artifact; AI may draft, never be the
  named human; `digested` additionally requires engagement
  by at least one program-independent scholar.
- OD-3: contested attribution caps the parent at
  `checked`; contested (active, evidenced dispute) is
  distinguished from unexamined (no special cap; bundle
  minimum rule applies).
- OD-4: Tao's five stage names verbatim in data and on
  all displays; no synonym mapping.
- OD-5: a digestion record qualifies on any one of
  independent reuse, a published challenge answered in a
  durable record, or an independent mechanism-engaging
  citation judged by a named reviewer at intake; an
  unanswered refutation is adverse digestion (claim
  flagged contested, pulled back under the bundle rule).
- OD-6: the priority register is public at intake
  (claimant, timestamp, hash of the reading published);
  content sealed until the claimant publishes or a
  claimant-chosen date (default 24 months, extendable
  once).
- Scope: OD-1…OD-6 only; the audit §9 items D-A…D-E
  remain open. Governed claims stay `draft`; PR #164
  stays DRAFT, unmerged — the freeze merge is owner-gated
  and follows the audit's landing on the same branch.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 adjudication addendum: D-A through D-E ratified; README errata (D-C) executed

- Owner decision (Tristen Pierson, 2026-10-12, verbatim):
  "do all this" — ratifying D-A through D-E (audit §9)
  as a block, adopting the program's recommendations.
  Recorded as a dated addendum in
  `specs/029-tao-claim-lifecycle/adjudication.md`; the
  earlier scope note leaving D-A…D-E open is superseded.
- D-A: annotate the anchors in place, additively —
  total `validation_status` on every anchor, a computed
  `strict_set` flag with the rule version recorded, no
  tier demotion, and a declared anchors-file schema
  enforced by a CI validator.
- D-B: deduplicate extracted claims by proposition —
  merge, never delete; source documents preserved as
  evidence instances, counted once per origin group; a
  proposition-fingerprint guard at extraction intake.
- D-C: README factual errata corrected immediately, in
  this change, as errata (not re-staging). Against the
  canonical file (recomputed from the entries of
  `backend/reports/INDUS_FINAL_ANCHORS.json`: HIGH 166 /
  MEDIUM 5 / LOW 3 / CANDIDATE 113; pending set 44 =
  43 HIGH + 1 MEDIUM): (i) the tier split "112 LOW +
  4 CANDIDATE" corrected to 3 LOW + 113 CANDIDATE;
  (ii) "44 HIGH" for the `pending_non_sa_validation`
  set corrected to 43 HIGH + 1 MEDIUM in the status
  banner, the metrics table, and the research-status
  list; a dated errata note added to the README. The
  re-base note's past-tense Phase-108 narrative stands
  unaltered (the one MEDIUM pending anchor, M293, was
  HIGH at classification; Phase-109 demoted it).
- D-D: foundation report annotations get a dated as-of
  label as the interim step; structurally, annotations
  are generated from canonical data at report time
  (anchor-file hash stamped) and the foundation status
  endpoint is repaired to serve the on-disk report or
  fail loudly.
- D-E: the audit's reclassification ledger stays the
  source of truth for stages until the Spec 029 plan's
  early, gated re-staging migration stamps `stage` /
  `stage_source` / `stage_as_of` mechanically from it.
  Invariant: a stage is always recomputable from the
  record's evidence — the stored value is a cache with
  provenance, never an assertion.
- Plan scope: D-A, D-B, D-E, and D-D's structural half
  enter the Spec 029 plan; D-C is executed here and does
  not enter the plan.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 L3 recovery and freeze

- L3 recovery (owner-authorized 2026-10-12, "Authorize
  the L3 recovery PR and resume implementation"): the
  Spec 029 claim register was recovered in the Spec 028
  shape after the L3 hook pass returned a blocking
  `iterate` at all three phases (no `evidence` field
  and no `boundary_confirmation` metadata on any of
  the 10 claims; all at the 0.25 no-evidence floor).
  Evidence lists and pairwise boundary confirmations
  added; compound texts rewritten as single positive
  propositions; three recorded splits grew the
  register 10 → 13 claims (minimum rule F029-C11 from
  C03; digested gate F029-C12 from C04;
  remaining-unknowns rule F029-C13 from C06). Re-run:
  **pass** at after_specify / after_plan / after_tasks
  (13 claims, 0 failure modes, 0 below the 0.70
  threshold). Merged as PR #167 (main `e60b8408`).
  Record: `specs/029-tao-claim-lifecycle/aee/
  recovery-specify.md`; the blocking round's record
  stands at `aee/l3-outcome.md`.
- Freeze (F1): `specs/029-tao-claim-lifecycle/
  freeze.md` + `freeze.json` (framework026 digest
  `80d589fee7bfc0099f7df496e22d8570014817ee04bca37ca
  8d408d3841af59d`) over spec.md, the recovered
  claims.json, adjudication.md, assessment.md,
  audit.md, reclassification-ledger.json, plan.md,
  tasks.md, build_freeze.py, and the freeze tests
  (`backend/tests/test_spec029_freeze.py`, pinning the
  digest replay and the ledger's §3 counts: 345
  entries; 220 created / 116 checked / 0 / 0 / 0; 105
  `verified_unexplained` flags). Bookkeeping rule
  recorded in freeze.md §2: plan.md and tasks.md are
  frozen bytes; phase completion is recorded in phase
  records and this ledger, with checkbox ticks applied
  once at closeout (X2) as a freeze amendment.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase A: stage axis and transition core

- Phase A (tasks A1–A6; FR-029-01…03) implemented on
  branch `impl/029-phase-a-stage-core` from main
  `a38cf92e`: new module `backend/glossa_lab/
  claim_stage.py` carries the additive stage shape
  (`stage`, `stage_source`, `stage_as_of`, append-only
  `stage_history`) shared by extracted-claim and anchor
  records, with unstamped defaults — no live record was
  stamped or edited (stamping is Phase D's ledger
  replay). `aee_core.claim_from_glossa` maps the stage
  axis as a distinct object in Claim metadata, never
  folded into ClaimStatus or confidence; a regression
  test pins score propagation byte-identical to the
  pre-change scores captured at `a38cf92e` over the
  current 31-claim set (fixture in `backend/tests/
  fixtures/`). The transition service
  (`transition_stage`) is the single writer of stage
  changes: one-step-forward legality, reasoned
  demotion, automated actors allowlisted to
  created/checked and fail-closed above checked, a
  named-human actor required above checked (a process
  name never validates), and stage/source/as_of written
  together with the appended history entry.
  `GET /claims`, `GET /claims/aee-scores`, the signs
  (anchor) surface, and the dashboard decipherment
  summary serialize stage (with provenance and history
  summary) and lane-1 score as distinct objects.
  `verified_unexplained` is computed per FR-029-03 and
  exposed on those surfaces (filterable on
  `GET /claims`); on the current claim set it flags the
  audit's 8 supported-class records, plus the
  partially_falsified / band-high record under the
  rule's high-band disjunct. Gate evidence: foundation
  check 40 passed / 0 failed / 8 warnings (baseline
  identical, no new warnings); full backend suite
  2112 passed, 5 skipped, 0 failed; new Phase A tests
  in `backend/tests/test_spec029_phase_a.py`. CI on
  PR #169: the first run failed Backend tests on the
  anchor-surface test (signs-index entries from anchor
  sets carried no stage key in CI's seeded data; fixed
  by serializing the stage object for every entry
  source in `_build_sign_entry`); the run on the fixed
  head `3ef6d225` (run 38270045482) is all 7 checks
  success. Record:
  `specs/029-tao-claim-lifecycle/phase-a-record.md`.
  Honest limitations recorded there: FR-029-06/07 gate
  records above checked are Phase B machinery; anchor
  risk flags from the audit's strict rule are stamped
  by Phase D, not recomputed from confidence tiers.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase D: OD-1 re-staging migration executed

  The frozen reclassification ledger was applied to the
  live record stores as one dated reclassification
  event (OD-1): 336 records stamped additively with
  `stage`, `stage_source` (the ledger and the entry's
  item_id), `stage_as_of` 2026-10-12, one initial
  `stage_history` entry, and the ledger-stamped
  `verified_unexplained` flag state — 287 anchors in
  place (`backend/reports/INDUS_FINAL_ANCHORS.json`,
  SHA-256 eccea6d5… → 18e6f4b2…), 31 extracted claims
  in place, 3 hypothesis models in place, and 15
  document-class records (PRED live, study headlines)
  stamped in the dated machine-readable sidecar
  `specs/029-tao-claim-lifecycle/
  phase-d-stamped-records.json` (their source documents
  are unedited history). Migration is additive only —
  canonical before/after comparison per store proves
  no pre-existing field changed — idempotent, and
  fail-closed: the dry run reconciled against the
  ledger exactly before any write (220 created / 116
  checked / 0 explained / 0 accepted / 0 digested; 105
  verified_unexplained flags), and post-run
  verification from the live stores matches exactly.
  Consumers repaired in place with no stored value
  changed: hash-pinned phase runners/tests now use the
  canonical anchors digest (same pinned constant), the
  claim-extraction script preserves stage fields by
  claim identity across regenerations, and the
  verified_unexplained computation honours the
  ledger-stamped flag. Gate evidence: foundation check
  40 passed / 0 failed / 8 warnings (baseline
  identical); full backend suite green; PR/CI/merge
  evidence in `specs/029-tao-claim-lifecycle/
  phase-d-record.md` (D6). Records:
  `specs/029-tao-claim-lifecycle/phase-d-record.md`,
  `specs/029-tao-claim-lifecycle/
  phase-d-run-record.md`.
## 2026-10-12 — Spec 030 design draft (Q6 chronology-spine extension) + Spec 027 Stage 2/Q7 adjudication packet

Internal design work only, at the owner's direction
(2026-10-12: "Do all we can do today, no reaching out
yet"): nothing frozen, nothing executed, no external
contact. Two documents, one draft PR, prepared from
branch point `028d416c` (Spec 029 Phase A merge).

**Spec 030 — Q6 chronology-spine extension (design
draft).** New spec directory
`specs/030-q6-chronology-spine-extension/` (spec.md +
claims.json, F030-C01…C07, all draft; the register is
machine-validated: unique IDs, dependencies resolve,
acyclic, every claim carries a falsifier, evidence
list, and boundary confirmation). Q6 itself stays
owned by Spec 027 (F027-C16); Spec 030 owns only the
data extension. The design works from the frozen
Stage 0 criteria (stage0-freeze.md §4) and the Stage 0
values verified at row level against
`data/movement/chronology_rows.jsonl`: C1 = 1 region
of ≥3 (PK only; IN holds 44 rows / 10 sites, all
unassessed; TM holds 3 single-row sites; IR holds one
site in total; FI cannot qualify); C2 = 5 window d/a
sites of ≥10 (in-spine grade-up ceiling is 9, so new
window-dated sites are mathematically required);
C3 = 0.0 short-lived share of ≥0.5 — the binding
constraint, stated parametrically: with g long-lived
grade-ups, net new short-lived window d/a rows
s ≥ 31 + g, so long-lived grade-ups raise the
requirement row for row and tracing order is a design
decision (Ask 3); C4 passes at 70 BP and is a stop
condition, not a target. Five routes in stop-point
order (R5 XRONOS re-retrieval → R1 origin-record
tracing → R2 c14bazAAR database audit → R4 TwoRains
supplement audit → R3 targeted published-date
extraction, `open_access_read_only` under the
Phase-124 precedent); integrity rules extend Stage 0's
(trace-or-don't-build, lab-code dedupe, grading and
material classification on origin records only,
CONTESTED sensitivity reported per criterion, no
calibration computed); the re-test is the §4 assessment
verbatim, margins only, with SUPPORTED-FOR-FREEZE-
DESIGN or NOT-YET-TESTABLE as its only outcomes and a
negative extension closure recorded as a valid result
(F030-C07). Five asks for a future adjudication (§9),
including the coordinate-less-row rule and whether
the CONTESTED sensitivity binds.

**Spec 027 Stage 2 / Q7 adjudication packet.**
`specs/027-movement-culture-language/stage2-q7-adjudication-packet.md`
— a pre-decision packet in the house adjudication
format, not an adjudication. It names Q7's actual
gate (the D8 source/licence audit has never been run;
no lawful provenance link set exists), and puts six
asks with options and program recommendations: Ask 1
D8 audit sequenced Law (2011) → Kenoyer/Vidale →
Meluhha with stop rules (1B); Ask 2 two-tier provenance
links, instrumental primary / visual-only labelled
sensitivity (2B); Ask 3 each response arm on its own
eligible site set, never pooled (3A); Ask 4 Q7 does
NOT depend on the Spec 030 spine extension — period
eligibility is served by Stage 0 gazetteer labels (4A);
Ask 5 inherit the Spec 026/027 control and verdict
discipline wholesale, minimum-support fixed from
margins after the D8 audit (5A); Ask 6 Stage 1's
publication and OSF-registration posture mirrored
(6A). Dependencies table and explicit non-goals
included (no people/language conclusion, no Q1
upgrade, no digitisation before rights clearance, no
rights-holder contact under the packet).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 030 §9 + Spec 027 Q7 packet adjudicated (owner: "Freeze it")

Owner decision (Tristen Pierson, 2026-10-12, verbatim):
**"Freeze it"** — in response to the PR #170 science
packets. Under the program's established
block-ratification pattern (Spec 027's adjudication;
Spec 029's OD block and D-A…D-E block), the
instruction adopts the packets' stated
recommendations as a block and moves both to their
next step. Reading and answers are recorded in
`specs/030-q6-chronology-spine-extension/adjudication.md`
and `specs/027-movement-culture-language/stage2-q7-adjudication.md`;
Spec 030 `spec.md` §9 is annotated under each ask
with the original question text preserved. The Q7
packet file itself is unaltered; the Q7 adjudication
is a new file alongside it.

**Spec 030 §9:** Ask 1 → ADOPTED as proposed
(coordinate-less dated records admitted for
gazetteer-established sites, coordinate state
recorded as inherited-from-cluster; integrity
rule 7). Ask 2 → **NOT DECIDED, expressly not
covered**: the design states no recommendation
(F030-C04 is satisfied by the reporting whichever
way bindingness is later ruled), so no answer is
invented for it; both computations are reported
under rule 5 and bindingness is reserved to a
future Q6 freeze's adjudication. Ask 3 → ADOPTED
as proposed (short-lived-first tracing order, full
pool reported, no traced row excluded; C3
requirement stands parametrically at s ≥ 31 + g).
Ask 4 → ADOPTED (all five routes in the §4 order —
R5 → R1 → R2 → R4 → R3 — with margins-only interim
assessments and owner stop points) with the R3
posture CONFIRMED (open_access_read_only,
internal-spine-only, never released). Ask 5 →
ADOPTED (the build is Phase-394; OSF registration
of the frozen contract is a precondition of
execution — prescribed, not performed, by the
adjudication).

**Spec 027 Q7 packet:** all six recommendations
adopted as a block — 1B (D8 audit sequenced Law
(2011) → Kenoyer/Vidale → Meluhha, stop rule and a
reported outcome after each stage, desk audit of
published sources, no external contact), 2B
(two-tier provenance links: instrumental primary,
visual-only as a separately labelled sensitivity),
3A (each response arm on its own eligible site
set, never pooled), 4A (Q7 independent of the
Spec 030 extension; Stage 0 gazetteer period
labels serve eligibility), 5A (Spec 026/027 control
and verdict discipline inherited wholesale;
minimum-support rules fixed in the Q7 freeze from
margins only, after the D8 audit), 6A (Stage 1
publication posture mirrored; OSF registration of
the frozen Q7 contract prescribed before
execution, not performed by the adjudication).

**Consequences.** Q7 is **not frozen** by this
adjudication — by the packet's own logic its
freeze is designed from the D8 audit's margins.
The adjudication authorises, in order: (1) the D8
audit under 1B; (2) a Q7 freeze as a separate
later act; (3) execution only after that freeze
merges. The Spec 030 freeze follows in its own PR;
the Phase-394 build does **not** execute on this
record (adopted Ask 5's OSF-registration
precondition stands in front of it). No external
contact of any kind was made; no OSF or other
registration was created; no Spec 027/028/029
record was altered beyond the new Q7 adjudication
file.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 030 FROZEN (Q6 chronology-spine extension)

Spec 030 is frozen on its adjudication
(`specs/030-q6-chronology-spine-extension/adjudication.md`,
merged in PR #170): §9 Asks 1, 3, 4, 5 adopted as
proposed under the owner's instruction "Freeze it";
**Ask 2 expressly not covered** — the design states
no recommendation on whether the CONTESTED
sensitivity binds a future Q6 freeze, and the frozen
record carries that non-decision rather than an
invented answer (bindingness reserved to a future
Q6 freeze's adjudication under Spec 027 §8.2).

Freeze record: `freeze.md` / `freeze.json`
(framework026 digest
`3a61c63a26ffada3c21bf8b718610e6debe7f9c9ff58bf8ff736cbb7c3db00e9`,
built by `build_freeze.py`), covering the design,
the adjudication, and the governed claim register
(F030-C01…C07, register_version 0.2-draft). The
register enters the freeze as recovered at the
freeze AEE pass (`aee/recovery-specify.md`): round 1
returned `iterate` (11 failure modes — irreducibility
×7 on compound claim texts, negation-conflict ×4
against F030-C01); the recovery rewrote the claim
texts as single atomic propositions with the
enumerations and secondary clauses carried in
boundaries and metadata (boundaries and verdict
rules unchanged in substance) and added pairwise
boundary confirmations for the flagged pairs; round
2 returns **pass** at after_specify, after_plan, and
after_tasks (7 claims, 0 failure modes, 0 below the
0.70 threshold; framework026 register integrity
ok). Freeze tests pin the record's replay, the
adjudicated design constants (Phase-394; routes
R5 → R1 → R2 → R4 → R3; Ask 2's non-coverage carried
in the definition), the register's integrity, and
the Stage 0 gap values from
`reports/phase391_results.json` (Q6 NOT-YET-TESTABLE:
C1 = 1/3, C2 = 5/10, C3 = 0.0/0.5, C4 = 70/80 pass,
31 window d/a rows). Local gates: freeze tests 4/4;
full backend suite 1,174 passed / 14 skipped /
0 failed (baseline 1,170 + the 4 new freeze tests).

**The Phase-394 build does not execute on this
freeze.** Adopted Ask 5 makes OSF registration of
the frozen contract a precondition of execution,
mirroring Spec 027 Stage 1; the registration is
prescribed, not performed, here. Execution follows
registration under its own go. Q6 remains
registered-blocked under Spec 027 (F027-C16); this
freeze changes no Spec 027 record and loosens no
criterion.
## 2026-10-12 — Spec 027 Stage 2: D8 source/licence audit complete (Q7 gate condition met)

The D8 audit authorised by the Q7 adjudication
(`specs/027-movement-culture-language/stage2-q7-adjudication.md`,
adopted Ask 1B) is complete and recorded in
`specs/027-movement-culture-language/stage2-d8-audit.md`.
Sequenced as adopted, with a stop rule and a
reported outcome after each stage; a desk audit of
published sources and their terms only — no
external contact, no rights-holder approach,
nothing digitised.

**Stage 1 — Law (2011): NOT a rights failure.**
*Inter-Regional Interaction and Urbanism in the
Ancient Indus Valley* (RIHN Occasional Paper 11,
2011; Manohar edition in two parts incl. printed
appendices). More than 2,100 provenience
determinations for Harappa artifacts and almost 120
for other sites, methods recorded per material
study (INAA; Sr/S isotopes; Chapter 4
reference-based assignment). Chapters openly posted
on harappa.com; no open licence stated; **no bulk
machine-readable deposit located** — Spec 027 §4's
blocker note re-confirmed as of 2026-10-12.
Posture `open_access_read_only`: internal
digitisation for link construction under the
Phase-124 precedent, never released (Ask 6A).
Margins carried to the freeze: ~95% of
determinations are single-site (Harappa); under
Ask 2B only the instrumental subsets are the
primary tier.

**Stage 2 — Kenoyer/Vidale: NOT a rights failure.**
The bead-drilling technique classification
(Kenoyer & Vidale 1992 and its published extensions
and applications) is lawfully readable — anchor
texts openly posted as author PDFs, posture
`open_access_read_only` (publisher-only items
`catalogue_only`) — and traceable per published
application. No consolidated per-object dataset
exists; the bead/craft arm's data are assembled at
the Q7 freeze from published applications, method
and classification source recorded per cell
(Ask 3A), against per-arm minimum-support rules.

**Stage 3 — Meluhha compilations: closed as
catalogued context.** Possehl 1996 ("Meluhha", 76
cuneiform citations) names a source region, never
an Indus site; it contributes **no site-pair links
under any posture** (`catalogue_only`). Not a
rights failure — the component was never
link-bearing.

**Conclusion.** The §8.1 gate condition for Q7 is
met (Stage 0 complete + this audit). The Q7 freeze
may now be designed from the audit's margins under
Asks 2B/3A/5A with the OSF registration prescribed
by Ask 6A — **as a separate later act; this audit
designs and freezes nothing, and digitises
nothing**. Residuals recorded for the freeze: the
ceramic arm's site-report sources sit outside D8's
three components (posture assigned at freeze time);
appendix-level method-per-determination field
completeness is re-verified at digitisation design
time.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Owner confirmation of the freeze reading ("correct, do it")

Owner confirmation (Tristen Pierson, 2026-10-12
13:30 EDT, verbatim): **"correct, do it"** —
confirming the reading executed for both PR #170
packets: the packets are frozen with the
recommended options adopted as a block; execution
runs strictly as the adopted asks authorise; and
no OSF registration is made under that instruction.

Recorded alongside the original instruction
("Freeze it") in: the confirmation addendum
appended to
`specs/027-movement-culture-language/stage2-q7-adjudication.md`,
and `specs/030-q6-chronology-spine-extension/adjudication-confirmation.md`.
The Spec 030 adjudication file itself is not
edited: it is a digest-covered source of the
Spec 030 freeze (`freeze.json` digest
`3a61c63a26ffada3c21bf8b718610e6debe7f9c9ff58bf8ff736cbb7c3db00e9`),
and frozen bytes are never edited — the
confirmation is carried for that record by the
companion note and by this entry.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase H: D-A anchor annotation (total validation_status, computed strict_set, declared schema)

  D-A executed on the canonical anchors file
  (`backend/reports/INDUS_FINAL_ANCHORS.json`, SHA-256
  18e6f4b2… → df0cf620…): every one of the 287 anchors
  now carries an explicit `validation_status` —
  pre-existing values preserved verbatim (44
  `pending_non_sa_validation`, 113
  `premise_superseded`) and the 130 records that
  carried none annotated from their own provenance
  (94 `strict_sa_independent`, 33
  `sa_in_provenance_chain` — the audit's chained HIGH
  anchors, now distinguishable from strict HIGH anchors
  in the file itself — and 3 `no_validation_record`) —
  and a computed `strict_set` flag from the Phase-108
  register + Phase-109 `strict_sa_independent_hm`
  join, reconciling exactly to the canonical strict
  core (94 = 90 HIGH + 4 MEDIUM; membership verified
  against the frozen reclassification ledger's checked
  set), with the rule's identifier and version recorded
  in the file metadata. A declared schema
  (`specs/029-tao-claim-lifecycle/anchors-schema.json`)
  pins the file's shape, and a CI validator
  (`backend/tests/test_spec029_phase_h.py`, over
  `annotate_phase_h_anchors.validate_anchors_doc`)
  fails on any undeclared shape, any missing or
  out-of-vocabulary status, and any stored flag that
  disagrees with its recomputation. Annotation is
  additive only: stripping exactly the Phase H fields
  reproduces the Phase-D-stamped bytes canonically,
  and stripping Phase D + Phase H reproduces the
  pre-migration bytes. No tier, reading, basis, or
  existing value changed. The canonical-hash
  helpers/tests Phase D canonicalized were extended
  the same way (pinned constants unchanged). Gate
  evidence: foundation check 40 passed / 0 failed /
  8 warnings (baseline identical); full backend suite
  1227 passed / 6 skipped / 0 failed; PR/CI/merge
  evidence in `specs/029-tao-claim-lifecycle/
  phase-h-record.md` (H5).
## 2026-10-12 — Spec 030 frozen contract registered on OSF (Phase-394 precondition met)

The frozen Spec 030 contract (Q6 chronology-spine
extension; freeze digest
`3a61c63a26ffada3c21bf8b718610e6debe7f9c9ff58bf8ff736cbb7c3db00e9`,
freeze PR #172, merge `51aec850`) was registered on
OSF as prescribed by adopted Ask 5, before any
Phase-394 execution: **https://osf.io/bge3k/**,
DOI **10.17605/OSF.IO/BGE3K**, OSF Preregistration
schema, node `4s9u2`, filed 2026-10-12T17:57:38Z
with all 29 response fields carried from the frozen
record. The API approval route returned HTTP 409 as
the program record predicts; approval was effected
via the admin-notification email token link in the
signed-in browser (the standing approvals loop).
Post-approval state verified via the OSF API:
`reviews_state: accepted`, `public: true`, DOI
minted. Full record:
`specs/030-q6-chronology-spine-extension/osf-registration.md`.
Phase-394 execution follows under the owner's
authorisation of 2026-10-12 ("Register Spec 030 on
OSF and execute Phase-394"), under the frozen route
order and stop rules.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase I: D-B claim-store deduplication (proposition merge + intake fingerprint gate)

  D-B executed on the extracted-claims store
  (`glossa-indus/claims/extracted_claims/*.json`, the
  2026-10-09 batch: 31 records, 10 documents). The
  proposition fingerprint — SHA-256 over the normalised
  claim text (NFKC + case-fold; every non-alphanumeric
  character to a single space; whitespace collapsed),
  defined and frozen in
  `backend/glossa_lab/proposition_fingerprint.py`
  (rules version `spec029-phase-i-v1`) — finds **5
  duplicate groups, 31 records → 23 unique
  propositions**: the audit's two Yadav propositions
  (the Zipf-Mandelbrot frequency claim, both records
  at score 1.0 pre-merge, and the text-begin/end sign
  claim), the ledger-flagged positional-analysis
  proposition recorded five times, and two critique
  propositions (Farmer et al.'s "myth of a literate
  Harappan" and "collapse of the Indus-Script thesis")
  whose texts differ only in case, a mid-phrase
  newline, and a hyphen. Merge, never delete (tool:
  `specs/029-tao-claim-lifecycle/merge_phase_i_dedupe.py`):
  every record stays in its own file byte-preserved
  outside the additive Phase I keys; instances gain a
  `merged_into` pointer; canonicals (fuller trail wins,
  ties by scan order — in every group the record the
  frozen ledger did not flag `duplicate_record`) carry
  each instance's full record under
  `evidence_instances`. Phase D stage stamps are
  untouched on canonicals and instances alike (groups
  are stage-uniform: checked/checked, created/created);
  falsifiers were preserved where present and invented
  nowhere (the text-begin/end canonical honestly
  carries none — neither instance had one). Origin-group
  counting in the AEE wiring: instance records no longer
  enter the graph, so a merged proposition's evidence
  counts once. Score movement, reported with its cause:
  **no surviving claim's score changed** (all 23
  byte-identical to the Phase A pre-change fixture,
  which is preserved untouched; a post-merge successor
  fixture is added); the mean moved 0.484903 → 0.497641
  by composition only (the 8 surplus records — 1.0,
  0.85, 6 × 0.289375 — left the scored set). Intake
  gate: extraction intake
  (`glossa-indus/scripts/indus_claims.py`) computes the
  fingerprint for every new claim and stops loudly with
  an error naming both records on a collision with an
  existing proposition (known group members pass, so
  wholesale regeneration does not collide with itself;
  regeneration also carries the merge state by claim
  identity). Gate evidence in
  `specs/029-tao-claim-lifecycle/phase-i-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.
## 2026-10-12 — Spec 030 / Phase-394 executed: spine extended, Q6 re-test NOT-YET-TESTABLE (valid negative closure, F030-C07)

Phase-394 ran under the frozen Spec 030 contract (OSF
https://osf.io/bge3k/, DOI 10.17605/OSF.IO/BGE3K; record
PR #176 merge `9a30b4f8`; infrastructure PR #177 merge
`09589443`) through the frozen route order
R5 → R1 → R2 → R4 → R3, with a margins-only interim
assessment after each route. No §3.5 early stop triggered
(no interim reached SUPPORTED). The extended spine holds
205 rows: the 177 Stage 0 rows deduped under rule 2 to
135 measurements (42 duplicate sightings merged — the
Bannu series had been ingested once per source database;
0 age conflicts; 6 site-assertion conflicts recorded),
plus 49 new rows (R2) and 21 new rows (R3). Per route:
R5's fresh XRONOS export is byte-identical to the frozen
Stage 0 export (sha256
`8570bfd9b256ced2f9e840183ea52325b9a7079b79a2957c7db797f09c118655`)
— 0 new records, 0 corrections. R1 traced the Qasim Bagh
series to Betts et al. 2019 Table 4 (10 material
corrections, 10 citations, 0 grade corrections; OZT-624
reclassifies to long_lived on its origin string). R2's
c14bazAAR audit ingested p3k14c (CC0-1.0), NERD (CC BY
4.0) and RADON-B (CC BY 3.0) — 124 corroborating citations
and 49 new rows, all unassessed: every admitted RADON-B
record carries the same type/layer formula and no named
sample feature, the evidence class held non-grading in R1
(census in the results file); CalPal is catalogue_only
(no open licence verifiable). R4 located one data-bearing
supplement (Petrie et al. 2016 OSM: 28 Masudpur
determinations with named contexts, taxon materials and
the authors' own flags) but the rows are NOT ADMITTED —
neither Masudpur site is gazetteer-established and no
publication reached states coordinates for them, and
rule 7 admits coordinate-less rows only for
gazetteer-established sites; the full extraction is
preserved in the results file for a future act. R3
extracted 21 Harappa determinations (Dales & Kenoyer
1993, Table 40.1; internal-spine-only, never released),
10 graded associated on the report's own feature
evidence, making Harappa the sixth window site.

The frozen §4 re-test on the extended spine, verbatim:
C1 = 1 region (bar 3) FAIL; C2 = 6 sites (bar 10) FAIL;
C3 = 0.0 short-lived share, 0 of 37 window
direct/associated rows (bar 0.50) FAIL; C4 = median
sigma 70 BP (bar 80) PASS. **Q6 status: NOT-YET-TESTABLE**
— identical under the as-frozen computation and the
CONTESTED-excluded computation (no CONTESTED row sits in
the window pool); Ask 2's bindingness question is
expressly NOT decided (reserved, Spec 027 §8.2). C3 is
the binding constraint: every traced short-lived
determination the routes reached is below the window,
ungradeable on its published evidence, or behind the
Masudpur coordinate gap. No criterion was loosened and
no row was graded on anything but its origin record.
Full record:
`specs/030-q6-chronology-spine-extension/outcome.md`;
products `data/movement/*_phase394*` +
`reports/phase394_results.json`. Gates: foundation
check 40 passed / 0 failed / 8 warnings; full backend
suite 1,238 passed / 6 skipped / 0 failed.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Maintenance: AEE dependency pinned below 1.5 (pre-1.5 scoring semantics restored)

The external library `applied-epistemic-engineering`
(PyPI) released version 1.5.0 on
2026-10-12T20:09:42Z. Its FR-8.7 "substance over
presence" change replaced binary falsifiability
credit (1.0 when a falsification test exists) with
substance-scored credit: a test string without a
checkable condition now earns partial credit (0.5).

This repo declared the library unpinned
(`>=1.0.4,<2` in `backend/pyproject.toml`), so CI
resolved the newest 1.x release. The observed
failure: PR #180's CI run 38306744884 (created
2026-10-12T20:49:54Z, head `149ca1a7`) installed
aee 1.5.0 and failed exactly one test,
`tests/test_aee_core.py::test_score_dict_shape`
(`assert 0.5 == 1.0` — falsifiability 0.5, expected
1.0), on a synthetic in-test claim. The same test
fails on main alone (`93a84532`) under aee 1.5.0
and passes under 1.0.4 and under 1.4.0 (the version
CI resolved in main's last green run 38300926354,
2026-10-12T19:56:14Z). Main was therefore red in
waiting for every future CI run; the failure is
not a defect in PR #180 or in Spec 029 Phase I.

Change (this entry's PR, standalone): the
requirement in `backend/pyproject.toml` is pinned
to `applied-epistemic-engineering>=1.0.4,<1.5` —
the only file from which CI resolves this
dependency. No test, fixture, score, anchor, or
register file changes.

The pin restores the scoring semantics that
Specs 026–029 were frozen and gated under,
including Phase A's byte-pinned score fixture
(mean 0.484903 baseline) and the Spec 029 freeze.
Adopting aee 1.5.0 semantics is a separate future
decision, requiring re-baselined fixtures and a
fresh gate; it is expressly NOT taken here.

Gate evidence (local, CI-identical dependency
resolution in a scratch venv): the pinned
requirement resolved
`applied-epistemic-engineering 1.4.0` (< 1.5);
`tests/test_aee_core.py::test_score_dict_shape`
passed (1 passed); foundation check
(`backend/scripts/foundation_check.py`) 40 passed /
0 failed / 8 warnings; full backend suite
(`python -m pytest tests/ --tb=short -q
--ignore=tests/test_pipelines_gpu.py
--ignore=tests/test_install_gpu.py -x`, per
`.github/workflows/ci.yml`) 1238 passed / 6 skipped /
0 failed — identical totals to main's last green
run under aee 1.4.0.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase B: claim bundles, attribution cap, explanation + digestion gates

  The bundle machinery and the stage gates Phase A deferred
  (FR-029-04…07; tasks B1–B5), in one new module
  `backend/glossa_lab/claim_bundle.py` plus one additive
  guard in `claim_stage.py`. A decipherment claim is a
  bundle: a parent record plus sub-claim records of kinds
  `reading_soundness`, `scholarship_accounting`,
  `attribution`, `explanation_intelligibility` — each a
  first-class record with its own evidence list, its own
  falsification condition, and its own Phase A stage, moved
  only by the Phase A transition service. The parent stage
  is computed (minimum of sub-claim stages, then the caps;
  F029-C11) and stored as that computation's cache
  (`stage_source` =
  `bundle-minimum-computation:spec029-phase-b-v1`); it is
  never directly assignable — both the Phase A service and
  the Phase B gate layer refuse a bundle parent (additive
  guard: no Phase A record shape carries `sub_claims`, and
  the Phase A suite passes unmodified; score propagation
  remains byte-identical under the Phase A regression).
  Attribution is a sub-claim with a governed template
  (prior readings with resolvable citations; a completeness
  basis naming corpora and literature searched, date, and
  searcher; a contest state): contested — an active,
  evidenced dispute with no durable adjudication record
  resolving it — caps the parent at `checked` inside the
  computation itself (OD-3); unexamined carries no cap; a
  valid durable resolution lifts the cap, an unresolvable
  one fails closed. The explanation record gates
  `accepted` (FR-029-06): one named accountable human
  (AI systems may be recorded as drafter, never as the
  named human — AI and process names are rejected),
  resolvable artifact URI, stored SHA-256 content hash,
  challenge venue, AI-assistance disclosure. The digestion
  record gates `digested` (OD-5): any one of independent
  reuse, a published challenge answered in a durable
  record, or a mechanism-engaging citation with a named
  intake reviewer's stored rationale — each with
  resolvable references and a validated
  program-independence field (explicitly not a claim
  author, not program staff; missing fails closed).
  Adverse digestion: an unanswered refutation flags the
  claim contested, blocks any advance above `checked`,
  and pulls it back to at most `checked` by a recorded
  demotion (plain claim) or the computation's adverse cap
  (bundle parent). The gate layer
  (`gated_transition_stage`) validates on a trial copy and
  delegates the write to the Phase A service — a refused
  transition writes nothing. Every gate ships with
  discriminating controls (task B5): 60 new tests in
  `backend/tests/test_spec029_phase_b.py`, all synthetic
  fixtures; the first local run caught five real defects
  in the new module (an AI-name token gap, a
  resolution-validation gap), fixed in scope. No live
  claim or anchor was promoted, decomposed, or given a
  real gate record — machinery only, per the phase's hard
  limit. Gate evidence: foundation check 40 passed /
  0 failed / 8 warnings; full backend suite under the
  CI-parity venv (aee 1.4.0) 1316 passed / 6 skipped /
  0 failed — the 1256 baseline plus exactly this phase's
  60 tests. Record:
  `specs/029-tao-claim-lifecycle/phase-b-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase C: priority register (OD-6) + per-claim inspectable trails

Spec 029 Phase C (tasks C1–C3; FR-029-11, FR-029-12;
claims F029-C08, F029-C09; OD-6) landed as machinery in two
new modules plus additive endpoints on the existing claims
router. The priority register
(`backend/glossa_lab/priority_register.py`) files an
external scholar's reading at intake on record completeness
alone — claimant public identity, private claimant contact
(correspondence only, never serialized), reading, evidence —
with no score, stage, or verdict field existing on an entry.
The public record is exactly claimant + server timestamp
(claimant-asserted timestamps are ignored) + the SHA-256 of
the canonical claim content (canonicalization
`spec029-priority-canonical-v1`: JSON of
{reading, evidence}, sorted keys, fixed separators, UTF-8,
no normalisation — a one-byte difference changes the hash
and does not verify). Per plan §2.1 the content is stored
sealed, not hash-only: an HMAC-SHA256 sealed envelope
(stdlib only) under a key held in a separate 0600 file in
the gitignored runtime store (`.glossa-state/`), never in
the store file and never serialized; tampered envelopes
fail closed, and opened content is re-verified against the
published hash before reveal. Unseal triggers (OD-6):
claimant publication (presented content unseals only on an
exact hash match; a mismatch is refused and recorded as a
dated event) or the reveal date (claimant-chosen, or the
default 24 months from intake), extendable once only — a
second extension is refused and recorded. The register is
append-only (no edit/delete path in service or API;
corrections are new entries superseding), every transition
is a dated history event, the clock is injectable, and the
credit display (the public record) is invariant under
later program assessment — all tested in both directions.
The trail view (`backend/glossa_lab/claim_trail.py`,
`GET /claims/{claim_id}/trail`) assembles one serialized
trail per claim (anchors resolve by sign id too): stage +
stage history with the record's `stage_source` as a source
pointer on every stage event (D-E recomputability),
verdicts and transitions alike carrying evidence refs with
origin groups, falsifier state at decision time, actor and
timestamp (gaps stated, e.g. `actor_recorded: False`,
never invented), bundle decomposition + gate records
(Phase B), `validation_status`/`strict_set` (Phase H),
evidence instances counted once per origin group
(Phase I), and priority entries filed against the claim —
serialized through the register, so sealed content cannot
leak through the trail. 36 new tests in
`backend/tests/test_spec029_phase_c.py`, all synthetic
fixtures; NO real priority claim was filed by this phase
(hard limit — filing is claimant/owner action). Gate
evidence: foundation check 40 passed / 0 failed /
8 warnings; full backend suite under the CI-parity venv
(aee 1.4.0) 1352 passed / 6 skipped / 0 failed — the
1316 baseline plus exactly this phase's 36 tests. Record:
`specs/029-tao-claim-lifecycle/phase-c-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase J: foundation annotations (D-D)

Spec 029 Phase J (tasks J1–J4; plan §2.7; adjudication
D-D) repairs the foundation report's annotations and its
status endpoint, the surfaces the audit (§5-P8 defect 3)
found serving Phase-48-era figures ("37 HIGH + 36 MEDIUM…
75 LOW… 1 UNCERTAIN (M267)") beside a status endpoint
returning silent nulls while a healthy report sat on disk.
The annotations describing canonical data are now computed
from the canonical stores at report-generation time — new
module `backend/glossa_lab/foundation_annotations.py`,
used by `backend/scripts/foundation_check.py`: tier split
(166 HIGH + 5 MEDIUM + 3 LOW + 113 CANDIDATE of 287),
strict core (94 = 90 HIGH + 4 MEDIUM), pending count (44),
the validation_status distribution, M267's current state
(MEDIUM, strict — resolved, not UNCERTAIN), and the
extracted-claims total (31 in 10 files). The generated
report is stamped with the anchors file's SHA-256
(df0cf620… at this head, verified) plus a combined
claims-store digest, and every annotation carries the
dated as-of label naming that stamped table — the label
stands as the report's permanent provenance line.
Historical population figures that remain (Phases 48, 51,
56, 69, 71) are labelled in-detail with their as-of phase;
the stale figures themselves are purged, grep-provable.
The status endpoint serves the on-disk report (figures,
label, stamps) or fails loudly with an explicit 503 —
never silent nulls; a hash-stale report is served with an
explicit staleness flag. A regeneration test proves the
figures track the canonical file (mutation changes figures
+ stamp; unmutated regeneration reproduces them exactly).
What the foundation check checks is unchanged: 40 passed /
0 failed / 8 warnings, check lists byte-identical. Gate
evidence: full backend suite under the CI-parity venv
(aee 1.4.0) 1368 passed / 6 skipped / 0 failed — the
1352 baseline plus this phase's 16 tests. Record:
`specs/029-tao-claim-lifecycle/phase-j-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase E1: display withdrawals (anti-gradability)

Spec 029 Phase E1 (tasks E1.1–E1.5; FR-029-08; claim
F029-C06; audit §5-P5) performs the display withdrawals
only — no replacement rendering (that is Phase E2). The
DeciphermentPanel's "{totalAnchors} signs deciphered"
footer and headline tile, its "Deciphered signs — 100%"
bar, and its SA-confidence and seals-decoded tiles are
removed; the anchor count remains only as an index into
the anchor records under a neutral label. The dashboard
decipherment payload no longer serves `sa_aggregate`
(the Phase-107-falsified SA method's aggregate),
`fully_decoded_pct`, or `n_fully_decoded` — the serving
code, including the hardcoded Phase-218 fallback values,
is deleted, and the per-round progression field of the
same name goes with it; Phase A's `by_stage` /
`n_unstamped_stage` fields are untouched and verified
live. `mean_propagated_score` is withdrawn from the
`GET /claims/aee-scores` summary and retained nowhere;
per-claim scores remain in per-claim detail entries with
their falsifier and stage objects, and the Phase A/I
byte-identical per-claim regressions still pass. Band
placement (E1.4): no frontend surface renders an AEE
band beside a claim status — the band lives only inside
the per-claim lane-1 score object — and the panel's
non-archived summary badge (confidence level + weighted
percentage) and weighted-confidence bar are removed.
Before/after screenshots at desktop and mobile widths
and live served-payload checks are in
`specs/029-tao-claim-lifecycle/phase-e1-evidence/` and
`phase-e1-record.md`; other surfaces found serving
same-named values (historical experiment-graph node
schemas, historical phase scripts, SignsView counts)
are inventoried in the record as E2/G follow-ups, not
changed here. Record:
`specs/029-tao-claim-lifecycle/phase-e1-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase E2: lane-separated rendering

Spec 029 Phase E2 (tasks E2.1–E2.3 as frozen, plus E1.1's
deferred replacement rendering; FR-029-09, FR-029-10,
FR-029-05 display rule; claims F029-C06/C07; OD-4) builds
the honest replacement rendering after E1's withdrawals.
The DeciphermentPanel now leads with the program's standing
position — "The Indus script is not deciphered," the
repository description's standing line — and the lane-2
stage summary from the dashboard payload's `by_stage`
counts (created 193 · checked 94 · explained 0 · accepted 0
· digested 0), with the OD-4 legend: the five stage names
verbatim, each with its plain definition, including that
creation and checking alone never settle a claim. The
legend also renders on the IndusEvidenceView claims
surface. Every expanded claim renders two distinct labelled
regions: lane 2 (human-paced settlement — stage in the
verbatim name with its provenance and latest transition,
the `verified_unexplained` risk flag, and the contest
display) and lane 1 (machine-speed verification, checking
only — the extraction status in a single neutral chip, the
retained per-claim AEE score only inside this region with
its band and method context, the falsification condition,
and the not-understood statement). Lane-1 badges lost their
per-status colours; no lane-1 value renders in a lane-2
position or the reverse (asserted on the rendered DOM).
`GET /claims` additively serializes `not_understood` (the
record's own statement or `None`, with
`not_understood_recorded`) and `bundle` (the Phase B
serialization for bundle parents). A contested attribution
renders on the parent with the OD-3 cap visible (stage
capped at checked, the computation's caps shown, the
contest record shown). No live record is a bundle parent —
all 31 extracted claims serialize `bundle: null` and render
the honest no-bundle absence; the contested path is proven
on synthetic fixtures in the backend tests and the
Playwright spec. Every verdict display renders the record's
not-understood statement or, for unauthored records, the
absence as a visible gap ("not yet recorded — this record
is incomplete… no machine-generated text is substituted for
it"): all 31 live claims are unauthored, no text was
generated for any of them, and the authoring queue (the 8
verified_unexplained claims first) is written down in the
phase record as lane-2 human work. A verbatim-name guard
pins the five stage names and bans stage-label synonyms in
the touched sources; E1's withdrawals stay withdrawn.
Before/after screenshots at desktop and mobile widths and
live served-payload checks are in
`specs/029-tao-claim-lifecycle/phase-e2-evidence/` and
`phase-e2-record.md`. Record:
`specs/029-tao-claim-lifecycle/phase-e2-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-12 — Spec 029 Phase G: CI gates and trail completeness

Spec 029 Phase G (tasks G1–G5; FR-029-12; claim
F029-C09; plan §0, §2.4) turns the spec's invariants into
permanent CI gates so the discipline cannot silently
regress (new machinery:
`backend/glossa_lab/spec029_gates.py`; new tests:
`backend/tests/test_spec029_phase_g.py`, 26 tests, and
`frontend/e2e/spec029-phase-g.spec.ts`, 4 tests). G1 —
trail completeness over the real live stores: for all 344
live records (287 anchors, 31 extracted claims, 15
document-class records, 3 hypothesis models, 8 preserved
evidence instances) the Phase C trail is assembled and
every verdict and stage-transition event is checked for
evidence refs (resolvable, with origin groups), falsifier
state at decision time, actor, timestamp, and the
stage_source pointer on stamped events, with Phase B gate
records validated wherever a stage sits above `checked`.
The gaps that legitimately exist today were measured
before any gate was written and are carried as an explicit
recorded baseline, named per record and per field in the
test and the phase record: no anchor carries a per-anchor
falsifier (the frozen ledger's own flag), no extracted
claim's extraction-era verdict names an actor (17 also
lack a falsification condition), and the document-class
and hypothesis stamps carry no record-level evidence or
falsifier. A record with no baseline entry — any new
record — must have an empty gap profile, and a baseline
profile that grows fails. One real defect was found by
the gate and is recorded, not fixed (machinery Phase G
was not assigned): the Phase C trail builder iterates a
string-form `glossa_lab_evidence` character by character
on 9 live claims, serializing 122 whitespace-only
evidence pseudo-refs; it is tolerated under a named,
dated exception covering exactly those records, and the
follow-up fix is recorded in the phase record. G2 —
stage-cache recompute integrity (plan §0): every stored
stage in every live store is recomputed from its record's
evidence (frozen-ledger replay for the migrated
population — all 344 recompute equal today — the
bundle-minimum computation with the OD-3 cap for bundle
parents, the history tail for transition-service
records) and must equal the stored cache with
`stage_source`/`stage_as_of` present; an unrecomputable
provenance is a defect. Corruption controls fail both
directions (stage raised and lowered in scratch copies;
stripped provenance; a source naming a non-existent
ledger entry). G3 — the Phase B discriminating controls
and parent-stage computation tests are verified as a
named suite collected by the CI-identical invocation
(1,412 tests collected), and the meta-test is added:
each gate's negative-control set is non-empty and every
control actually fails its gate, with positive twins
passing — a non-differential gate is INVALID. G4 —
display guards, program-wide: the withdrawn fields
(`sa_aggregate`, `fully_decoded_pct`, `n_fully_decoded`,
`mean_propagated_score`) stay absent from the served
dashboard, scores-summary, claims, and trail payloads at
any depth (each guard proven to fail on a reintroduced
violation in a scratch payload); the "signs deciphered"
headline pattern appears nowhere in `frontend/src` or on
the rendered surfaces; stage synonyms never appear as
stage labels on the claim surfaces, whose vocabulary is
exactly the five verbatim stage names; lane labels and
the OD-4 legend are present; and every verdict display
serialization carries a `not_understood` slot (all 31
live claims still unauthored — the recorded absence, no
substituted text). SignsView's per-sign deciphered counts
(E1's inventory) are recorded in the phase record as the
standing follow-up, not a G4-named guard. Foundation
check 40 passed / 0 failed / 8 warnings; full backend
suite 1407 passed, 6 skipped (the 1381/6 merged baseline
plus exactly the 26 new tests), CI-parity venv at aee
1.4.0; the new Playwright spec passes locally (4, with
E2's 5 unchanged). No stage, record, verdict, score, or
display was changed by this phase. Record:
`specs/029-tao-claim-lifecycle/phase-g-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-13 — Spec 029 Phase X: closeout (spec complete)

Spec 029 (Tao claim lifecycle) is closed. All
implementation phases are merged: L3 recovery PR #167
(`e60b8408`), freeze PR #168 (`a38cf92e`), A #169
(`028d416c`), D #171 (`712f3b99`), H #175 (`f8da5eaf`),
I #180 (`92e8f392`), B #182 (`411386a6`), C #183
(`7f773d6b`), J #184 (`7528ddc5`), E1 #185 (`1533425b`),
E2 #186 (`587dec70`), G #187 (`3e14dce2`) plus its
record correction #188 (`db1c3832`). Maintenance PR
#181 (aee pin below 1.5, merged `170e6f1f`) is
acknowledged in the closeout record as an external
event during implementation, not a spec phase; the
Phase I worker runtime death and forensic recovery
are recorded there as a process note.

Final verification on merged main `db1c3832` (task
X1, CI-parity venv at aee 1.4.0): (a) stripping all
Spec 029 additive keys (Phase D stage stamps + Phase
H annotation) from `INDUS_FINAL_ANCHORS.json`
reproduces the pre-Spec-029 canonical file
byte-identically (SHA-256 `eccea6d5…`) — no
pre-existing anchor field changed in the whole spec;
(b) `docs/PREDICTION_REGISTER.md` is byte-identical
to the plan-freeze head `9202fd44` (its only
retirement entry, PR #163, predates implementation);
PRED-2026-001/002/003 still PENDING, unscored; (c)
ledger-vs-live reconciliation exact: 220 created /
116 checked / 0 explained / 0 accepted / 0 digested,
105 `verified_unexplained` flags, anchors
`strict_set` exactly 94 with the Phase H vocabulary
distribution 94/44/33/113/3, extracted claims 31
store records resolving to 23 canonical claims + 8
evidence instances with the Zipf proposition recorded
once; (d) framework026 `verify_freeze` returned []
on merged main and the freeze digest stands at
`80d589fe…` — never regenerated; (e) foundation
check 40 passed / 0 failed / 8 warnings and the full
backend suite 1407 passed / 6 skipped / 0 failed,
identical to Phase G's final totals.

Closeout records (task X2): the completion ticks
(F1/F2 + phases A–X, 53 checkboxes, checkbox-state
changes only — verified mechanically, no task text
changed, no task incomplete) were applied to
`tasks.md` once, as the recorded freeze amendment
`freeze.md` section 2 prescribes; because `tasks.md`
is a frozen source in this spec, the freeze test now
asserts exactly the amendment's two named drifts
(the ticks and its own acknowledgment) and fails on
any other. Audit items D-A, D-B, D-D, D-E are
disposed by this spec's phases; D-C was executed
separately (PR #166). Honest residuals stand as
recorded in the closeout record: the promotion
writer does not yet stamp Phase H fields at write
time (CI catches it); SignsView counts and the
historical SA-era node schemas stand inventoried,
not changed; aee 1.5.0 adoption remains a future
decision (14-test census: 5 score-semantics + 9
bundle-validation failures); the trail-builder
string-evidence defect and the G1 recorded baseline
stand as Phase G left them; `not_understood` remains
unauthored on all live claims (lane-2 human work);
and the committed foundation report's claims-store
digest is stale beside the live store (its anchors
hash matches; the Phase J as-of label flags exactly
this). Standing statement: no live claim stands
above `checked`; explained / accepted / digested
count 0 because those are lane-2 human outcomes the
machinery now gates but cannot manufacture. The
script is not deciphered. Record:
`specs/029-tao-claim-lifecycle/closeout-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-13 — Spec 031 design draft (Spec 027 Stage 2 / Q7 provenance networks)

Design work at the owner's direction (2026-10-13:
design and freeze Spec 027 Stage 2 / Q7 from the D8
margins; execution not ordered). New spec directory
`specs/031-stage2-q7-provenance-networks/` (spec.md +
claims.json F031-C01…C12 + adjudication.md + plan.md
+ tasks.md + aee/). Q7 the question stays owned by
Spec 027 (F027-C15); Spec 031 owns the Stage 2 design.

The design is built from the completed D8 audit's
margins under the adjudication adopted 2026-10-12
(1B/2B/3A/4A/5A/6A, recorded verbatim in the spec's
adjudication.md): two-tier links (Law 2011
instrumental determinations primary; Chapter 4
reference-based assignments a labelled sensitivity,
never pooled); Meluhha contributes no site-pair
links; each response arm on its own eligible site
set; period eligibility from Stage 0 gazetteer
labels only; Spec 026/027 control and verdict
discipline inherited wholesale (MRM/MRQAP partial
R² of the shared-source term, practical margin 0.02,
B = 9,999, R = 199 controls, site jackknife). The
support rules are fixed in the design from the
margins as design decisions DD-1…DD-8 under the 5A
mandate, each flagged with its reasoning: link
eligibility ≥ 3 primary determinations per site,
arm floors (ceramic ≥ 20 / bead ≥ 10 classified
items per site), arm viability ≥ 8 eligible sites
and ≥ 10 linked pairs, with the ceramic arm declared
conditionally estimable and closing NOT ESTIMABLE at
the execution margins step if its unaudited source
basis cannot evidence the site floor, and
sub-period variants declared untestable in advance.
The Harappa concentration (≈95% of Law's
determinations) and the drop-Harappa jackknife cell
are named in the design as the expected pressure
point; a Harappa-dependent effect cannot reach
SUPPORTED under the frozen rules.

AEE hook pass: round 1 iterate (5 failure modes) and
round 2 iterate (4), recovered honestly in the
Spec 030 pattern (atomic rewrites carrying
enumerations into boundaries; pairwise boundary
confirmations; text-level rewording of four claims
to remove accidental token collisions the assessor's
text-pairing check flags, propositions preserved);
final outcome **pass** at after_specify, after_plan,
and after_tasks (12 claims, 0 failure modes, 0 below
the 0.70 threshold). Record:
`specs/031-stage2-q7-provenance-networks/aee/recovery-specify.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-13 — Spec 031 frozen (Stage 2 / Q7 design freeze)

The Spec 031 design (design PR #191, merged `b00b3b1d`)
is frozen: `specs/031-stage2-q7-provenance-networks/
freeze.md` + `freeze.json`, framework026 digest
`f63167fc99c8d3c31f885b1014cad69fab3788fcf8e6212d018aa6948a2cdac6`
over freeze.md, spec.md, claims.json (register
0.3-draft, F031-C01…C12), adjudication.md, the AEE
recovery record and freeze note, build_freeze.py, and
the freeze test. Freeze tests pin the digest replay,
the definition constants (Phase-395; support rules
3 / 20 / 10 / 8 / 10; margin 0.02; B = 9,999; seed
20261013; the ceramic arm's NOT ESTIMABLE closure and
the not-ordered execution gate carried verbatim), the
register integrity, the D8 margins as the audit states
them, and the Stage 0 gazetteer counts at row level
(36 rows / 30 sites / 21 verified_open / 15
open_access_read_only). Foundation check 40 passed /
0 failed / 8 warnings. `plan.md` and `tasks.md` are
bookkeeping and are not digest-covered (the Spec
029/030 rule). Next per adopted 6A: OSF registration
of the frozen contract, then execution only on a
separate owner order. Nothing was executed under
this freeze: no link digitised, no similarity
computed, no verdict exists.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-13 — Spec 031 OSF registration filed (pending approval)

The frozen Spec 031 contract was registered on OSF
per adopted 6A, after the freeze merged (PR #192,
`95388bbc`) and before any execution: registration
**https://osf.io/jtwvc/** on node `rfhd4`, OSF
Preregistration schema, all 29 response fields filed
from the frozen record and read back exact; subjects
mirror the precedent registrations. State at filing:
`reviews_state: initial`,
`pending_registration_approval: true` — the single
recorded API approval attempt returned HTTP 409 (the
standing route's known behaviour), and the "Pending
Registration - Admin Notification" email arrived
(Gmail id `1a134000191cceec`, 2026-10-13T06:42:56Z).
The approval click is the parent chat's standing job;
the registration record
(`specs/031-stage2-q7-provenance-networks/osf-registration.md`)
is filed as a PR left open pending that click, and is
completed by append once the approval verifies with
its DOI. Execution (Phase-395) remains un-ordered.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-13 — Phase-104 carry-over correction (Spec 029 records)

The Phase-104 evaluation's RULE-DUP verdict carry-over
(contradicted, from farmer_sproat_witzel_2004_manual_001) was
written into the three canonical live records it prescribed —
indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001,
indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002,
without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001 —
which had stood untested at stage created since extraction.
Each record now carries the verdict and Phase-104's evidence
verbatim, an additive status_correction note preserving the
previous status, and a stage of checked written through the
transition service (the Phase D stamp stands as history[0];
the frozen reclassification ledger is untouched). Exactly the
three claims' AEE scores moved (the engine's contradiction
penalty now applies, as it always did on the canonical claim);
the Phase A pin moved to a successor fixture in the Phase I
pattern, and the Phase D / Phase I / Phase G pins were amended
to name this correction. The two Phase-104 records Phase I
merged as evidence instances (critique_0003 / critique_0004)
were not rewritten — named residual in the correction record
(specs/029-tao-claim-lifecycle/phase104-carryover-correction-record.md).
The first CI run caught the gap that had caused the original
loss — a wholesale store regeneration reverted claim_status to
the extraction default — so the extractor's carry-over now also
preserves a status_correction's outcome fields by claim
identity. Full suite 1,450 passed / 6 skipped / 0 failed
locally (CI re-run is the final evidence for the fixed tree);
foundation 40 / 0 / 8.
## 2026-10-13 — Spec 029 lane-2 drafts ADOPTED (owner authorship act, OD-2)

The 35 lane-2 drafts prepared earlier today (PR #190:
explanation drafts + `not_understood` drafts for 23 canonical
extracted claims, 10 study headline claims, and PRED-2026-006/007)
were shown to the owner in full, and the owner adopted all 35 as
authored by him, verbatim: "Adopt all 35 lane-2 drafts as authored
by me" (2026-10-13 06:12 EDT). The adoption completed the OD-2
authoring fields on every record in
`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`: author
Tristen Pierson (author_kind human); drafter unchanged (AI agent,
Muse Spark, via Muse); `artifact_uri` the adopted record itself
on main, per-claim fragment; `content_hash` the SHA-256 of each
record's explanation text; `challenge_venue` the repository issue
tracker; `ai_assistance_disclosure` restated to record the drafting
and the adoption. All 35 completed records validate under
`glossa_lab.claim_bundle.validate_explanation_record`. Adoption
itself changed no live record; ingestion into the live stores
(stage moves only through the transition service, only where its
rules allow) is the companion act of the same owner order, recorded
in `specs/029-tao-claim-lifecycle/lane2-adoption-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI. The explanation texts were AI-drafted and
human-adopted as recorded above; the drafting AI is not the
author of any explanation record.

## 2026-10-13 — Spec 029 lane-2 adoption INGESTED (20 claims explained; OD-2)

Companion act to the adoption recorded above (same owner order,
2026-10-13): the 35 adopted explanation records were ingested
into the live stores by
`specs/029-tao-claim-lifecycle/ingest_lane2_adoption.py`
(fail-closed; `--verify` re-asserts the ingested state against
the frozen ledger and the adopted record). `not_understood` and
the completed `explanation_record` now stand on all 35 records.
Stage changes went only through the Phase B gate layer
(transition service, the single writer): the 20 records at
`checked` advanced to `explained` (8 extracted claims, 10 study
headlines, PRED-2026-006/007); the 15 at `created` kept their
stage (explanation cannot precede checking) as authored-pending,
except the 3 Phase-104 fragment claims, whose texts were
ingested but whose stage and evaluation state this act did not
touch (the carry-over correction owns those). The
`verified_unexplained` stamp cleared on exactly the 9 records
whose flag was set and whose explanation took effect. Live state
after the act, over the 336-record stamped population: 220
created / 96 checked / 20 explained / 0 accepted / 0 digested;
96 stamped flags. Nothing reached `accepted` or `digested` —
those gates need the acceptance process and independent
scholarly engagement (OD-5), which do not exist yet. Append-only
held: every advanced record keeps its Phase D migration entry as
`stage_history[0]`, byte-identical; the frozen ledger, the PRED
register document, the anchors file, and Specs 027–031 records
are untouched; PRED-2026-001/002/003 untouched. Phase G gates
green (provenance partition now 324 ledger replays + the named
20 transition-service tails); full suite green with the AEE
score regression byte-identical; foundation check 40 ok / 0
fail / 8 warn on its own surface (this act touches none of its
inputs). Five test files' pre-adoption live-state assertions
were amended with dated, named notes (Phase A/D/E2/G/I) — the
superseded expectations are preserved in prose in each file.
Record: `specs/029-tao-claim-lifecycle/lane2-adoption-record.md`.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI. The ingested explanation texts were
AI-drafted and human-adopted (see the adoption entry above);
the drafting AI is not the author of any explanation record.

## 2026-10-13 — Spec 029 lane-2 adoption: regeneration carry-over fix (PR #197)

CI on the ingestion PR (run 38384800347) failed one backend test
(E2 live serialization): the intake pipeline's background
regeneration of the extracted-claims store (`indus_claims.py`,
triggered by the `/intake/run` endpoint test) stripped the
adopted `not_understood` / `explanation_record` fields, because
the regeneration carry-over list predated the lane-2 fields —
stage fields survived, authored fields did not. Fix: both fields
added to the carry-over list in `indus_claims.py` under the same
never-drop rule; the Phase D regeneration test now plants both
fields and asserts verbatim survival. The committed store was
never wrong; the defect was latent in any future regeneration.
Full account:
`specs/029-tao-claim-lifecycle/lane2-adoption-record.md`
(2026-10-13 addendum).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.
## 2026-10-13 — Spec 032 design draft (PRED-2026-006: the Harappa breakdown, design D-30)

Design D-30 of the experiment-design portfolio of 2026-10-13
(draft PR #195) is carried into `specs/032-pred-2026-006-harappa-breakdown/`
without deviation, under the owner's freeze order of 2026-10-13
06:39 EDT ("Freeze D-30, D-03, and D-20 for execution"; adjudication
in the spec's `adjudication.md`). The spec freezes PRED-2026-006's
registered test exactly as registered on 2026-04-22: at least 70% of
the CISI-trained INITIAL signs show a start rate of at least 0.40 at
Harappa, on the withheld Harappa-site Yajnadevam sequences
(`backend/glossa_lab/data/yajnadevam_inscriptions.csv` — 5,679
inscriptions, 77 sites, 2,717 Harappa; census counted at design
time and pinned by the freeze tests). Step 0 fails closed: the
trained INITIAL set is reconstructed from the recorded
`global_class_stability.py` lineage and frozen; the withholding is
verified as CISI Mohenjo-daro only; sign identity is carried by the
existing crosswalks under `data/crosswalks/`, fixed before counting.
A failed check closes the study as CANNOT BE RUN AS WRITTEN; unmappable
trained signs are counted and reported, with coverage above 20%
stated in the verdict's first sentence. The verdict mapping is the
register's own (CONFIRMED at a share of at least 70%; NOT CONFIRMED
below it; no inconclusive band exists and none is invented); the
per-sign table is pre-registered as a descriptive addition only.
Governed register: 12 claims (F032-C01…C12), recovered through three
AEE rounds (17, then 4, then 1 failure modes — atomic rewrites and
pairwise boundary confirmations; record in `aee/recovery-specify.md`)
to register_version 0.4-draft; AEE hook pass at after_specify,
after_plan, and after_tasks (0 failure modes). Execution is
Phase-396, gated on the OSF registration of the frozen contract
verifying public. The registered computation has never been run;
the PRED register is untouched by this design.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-13 — Phase-395 executed: Spec 031 / Q7 closes at the margins step

Execution of the frozen Spec 031 contract (Q7 provenanced-material
networks; freeze digest f63167fc; OSF registration
https://osf.io/jtwvc/, DOI 10.17605/OSF.IO/JTWVC, approved and
public before execution) under the owner's order of 2026-10-13.
Infrastructure PR #196 (merge b287e7d9): the Phase-395 build
(backend/scripts/phase395_q7_execution.py), the experiment graph
node IndusPhase395Q7Execution, and 11 machinery tests. The
digitisation design step inventoried Law (2011)'s posted chapters
(11 of 14 located; Chapters 4, 5, 9 absent from the posted set;
appendices print-only, so D8 residual (ii) is recorded as not
re-verifiable from the posted set), applied the frozen method
split (primary tier = INAA and Sr/S-isotope studies only), audited
nine ceramic classification reports for posture (2
open_access_read_only, 7 catalogue_only), and recorded the
bead/craft source position (no consolidated per-object dataset;
floor not countable). Link construction: 76 counted named-source
determinations; 6 link-eligible sites; 13 certain linked pairs
(2 further pairs uncertain on print-only appendix data, counted
as not linked); in the Stage 0 gazetteer universe, 2
link-eligible sites and 1 linked pair; Meluhha 0 links. Margins
step: of 30 gazetteer sites, 21 pass the coordinate screen and
ZERO pass the frozen period screen (period_label_as_published
empty on 33 of 36 rows, the only labels present being PN/Neo. on
three Central Asian sites; program_period_assignment empty on
all rows) — both arms therefore have 0 eligible sites. Bead/craft
arm closes NOT-YET-TESTABLE (spec section 4.3); ceramic arm
closes NOT ESTIMABLE (DD-7). The sensitivity tier was not
constructed, the DD-8 river network was not pinned, and no
response was computed in either arm; the section 5 machinery
exists and is fenced by synthetic-population tests. Population
record sha256
a0c98d56780051b46795621b644457e7674f7266321073e65a67ef51f83b54b8.
Outcome recorded at specs/031-stage2-q7-provenance-networks/
outcome.md with per-claim stage determinations (Spec 029
machinery; the frozen register is not edited), and cross-recorded
under Spec 027 (stage2-q7-outcome-cross-record.md, a new pointer
file only). Gates: foundation check 40 passed / 0 failed /
8 warnings; backend suite green in CI on PR #196 (1,409 passed /
20 skipped / 0 failed); branding sweep clean. The digitised link
data stays in the gitignored local store and is released nowhere
(F031-C11).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-13 — Spec 032 frozen (PRED-2026-006: the Harappa breakdown)

Spec 032 is frozen: design PR #199 (merge c00b87fa) and this freeze
record. The freeze digest (framework026, over the recovered register
0.4-draft, 12 claims F032-C01…C12) is recorded in
`specs/032-pred-2026-006-harappa-breakdown/freeze.json`; the freeze
tests pin the digest replay, the registered criterion (share at
least 70%; start-rate bar 0.40), the register integrity, the
withheld-data census (5,679 inscriptions; 77 sites; 2,717 Harappa),
and the PRED register entry byte-state (the freeze edited no
register text; PRED-2026-006 still stands PARTIALLY CONFIRMED on
the neighbouring global figure until execution appends the scored
outcome). Execution is Phase-396, gated on the OSF registration of
this frozen contract verifying public; the registered computation
has never been run.

## 2026-10-13 — Spec 033 design draft (the SA-free language comparison, design D-03)

Design D-03 of the experiment-design portfolio of 2026-10-13
(draft PR #195) is carried into `specs/033-sa-free-language-comparison/`
without deviation, under the owner's freeze order of 2026-10-13
06:39 EDT ("Freeze D-30, D-03, and D-20 for execution"; adjudication
in the spec's `adjudication.md`). The spec freezes the SA-free rerun
of the Dravidian-versus-rivals comparison behind
`parpola_2010_dravidian_solution_manual_001`, whose partial support
was computed with the semantic-anchoring machinery Phase-107
falsified (held-out 0.000, 0 of 115): no SA, no anchor promotion,
and no SA-derived quantity anywhere in the pipeline (H26). Data:
the strict sign set (94 readings, validation status
strict_sa_independent, in `backend/reports/INDUS_FINAL_ANCHORS.json`)
and the V3/Mahadevan-lineage corpus as held; anchor values from
published sources only. The estimator the design prescribes fixing
at freeze time is fixed in spec section 5 (counted conditional
model over phoneme-sequence and sign-identity units, add-one
smoothing, mean log probability per sign, identical for every family
and control). Criteria, with margins set from the recorded
originals (Phase-41: 1.0566 to 1; Phase-43: 0.484 log units per
sign) so the rerun can fail: SUPPORTED at a margin of at least 0.10
log units per sign over the best rival and above the 99th
percentile of the 999-assignment random distribution; NOT SUPPORTED
on a rival at or above Dravidian or Dravidian inside the random
range; INCONCLUSIVE on a sub-margin win or a Harappa-removed
sensitivity reversal. Governed register: 15 claims (F033-C01…C15),
recovered through three AEE rounds (9, then 5, then 1 failure
modes — atomic rewrites, boundary transfers, one genuine split:
the SUPPORTED percentile condition became F033-C15; record in
`aee/recovery-specify.md`) to register_version 0.4-draft; AEE hook
pass at after_specify, after_plan, and after_tasks (0 failure
modes). Execution is Phase-397, gated on the OSF registration of
the frozen contract verifying public. No score has been computed;
the claim's record is untouched by this design.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-13 — Spec 034 design draft (the matched-object attribution, design D-20)

Design D-20 of the experiment-design portfolio of 2026-10-13
(draft PR #195) is carried into
`specs/034-matched-object-attribution/` without deviation,
under the owner's freeze order of 2026-10-13 06:39 EDT
("Freeze D-30, D-03, and D-20 for execution"; adjudication
in the spec's `adjudication.md`). The spec attributes the
unexplained residue of a settled result: Phase-125 closed
FAIL — DISAGREEMENT between the CISI (Parpola) and ICIT
(Mahadevan) compilations (16 judgeable pairs of 286; median
TV distance 0.636931); Phase-127 showed sampling noise alone
produces 0.083; Phase-131 attributed 6.1%, leaving 93.9%
unexplained because the two digital layers shared zero
object keys (the Holdat cisi_number join was rejected as
non-identity and stays prohibited). Step 0 builds the
object bridge through the three lawful routes the program
holds — the 7,705-row CISI catalogue layer (Phases
120–124), the Phase-130 intake schema on the Mahadevan
side, and the 44 Phase-128 dossiers — behind a gate fixed
in advance: at least 150 matched objects with texts of
three or more signs in both compilations; below the gate
the study closes as TOO THIN TO ATTRIBUTE with the bridge
census published as the finding. Above the gate, per-sign
positional profiles are computed on the matched subset only
under Phase-125's own distance and count floors, and the
remaining disagreement is decomposed in Phase-131's own
categories (segmentation / substitution, checked against
the crosswalk's conflict pairs — the crosswalk is a record
of disagreement, never ground truth / composition
residue). Criteria: matched median at or below 0.20
ATTRIBUTED TO COMPOSITION; at or above 0.32 (half the
corpus-level distance) ATTRIBUTED TO TRANSCRIPTION;
between, a split attribution with the decomposition table
as the result. The selection-bias report (matched subset
mix against both full mixes) rides in every verdict
statement. The study never judges which compilation is
right, and the settled Phase-125 verdict is untouched.
Governed register: 14 claims (F034-C01…C14), recovered
through four AEE rounds (12, then 4, then 1, then 1 failure
modes — atomic rewrites, boundary transfers, definitional
verdict lines; record in `aee/recovery-specify.md`) to
register_version 0.5-draft; AEE hook pass at after_specify,
after_plan, and after_tasks (0 failure modes). Execution is
Phase-398, gated on the OSF registration of the frozen
contract verifying public. No object has been matched; no
distance has been computed.

## 2026-10-13 — Spec 033 frozen (the SA-free language comparison)

Spec 033 is frozen. The frozen contract (specs/033-sa-free-language-comparison/)
carries design D-03 without deviation: the SA-free rerun of the
Dravidian-versus-rivals comparison behind
`parpola_2010_dravidian_solution_manual_001`, on the strict sign
set (94 of 287 anchors) and the V3/Mahadevan-lineage corpus, with
no semantic anchoring, no anchor promotion, and no SA-derived
quantity anywhere in the pipeline (H26). The estimator the design
prescribed fixing at freeze time is fixed in spec section 5 and
recorded in adjudication.md section 2. Criteria: SUPPORTED at a
margin of at least 0.10 log units per sign over the best rival and
above the 99th percentile of the 999-assignment random
distribution; NOT SUPPORTED and INCONCLUSIVE rules as designed;
the Harappa-removed sensitivity can route only to INCONCLUSIVE.
Governed register: 15 claims (F033-C01…C15), register_version
0.4-draft, AEE pass at after_specify / after_plan / after_tasks
after three recorded recovery rounds. Freeze digest
(framework026): 412b4805063bbffb3915a834354cb428cc9b10958f614a1680b859005a43b66d.
Design merged as PR #203 (c1cad78e). Execution is Phase-397,
gated on the OSF registration of this frozen contract verifying
public. No score has been computed; no claim record, anchor, or
frozen record is altered by this freeze.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-13 — Spec 034 frozen (the matched-object attribution)

Spec 034 is frozen. The frozen contract
(specs/034-matched-object-attribution/) carries design D-20
without deviation: step 0 builds the object bridge between
the CISI and ICIT compilations through the three lawful
routes (the 7,705-row CISI catalogue layer; the Phase-130
intake schema; the 44 Phase-128 dossiers), with the Holdat
cisi_number join prohibited, behind the gate fixed in
advance — at least 150 matched objects with texts of three
or more signs in both compilations, below which the study
closes as TOO THIN TO ATTRIBUTE with the bridge census
published as the finding. Above the gate, the attribution
runs on the matched subset under Phase-125's own distance
and count floors, decomposed in Phase-131's categories,
with verdict lines at 0.20 (ATTRIBUTED TO COMPOSITION) and
0.32 (ATTRIBUTED TO TRANSCRIPTION) and a split attribution
between. Governed register: 14 claims (F034-C01…C14),
register_version 0.5-draft, AEE pass at after_specify /
after_plan / after_tasks after four recorded recovery
rounds. Freeze digest (framework026):
696fd1855c8cbc1fe767fdc26a1697deb1f0dc85253376efdd7064f102594c2a.
Design merged as PR #205 (805bd4ae). Execution is
Phase-398, gated on the OSF registration of this frozen
contract verifying public. No object has been matched; the
settled Phase-125 verdict and every other frozen record
stand untouched.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-13 — Phase-396 executed: Spec 032 / PRED-2026-006 closes at step 0

Execution of the frozen Spec 032 contract (PRED-2026-006: the
Harappa breakdown, computed exactly as registered; freeze
digest 34cd6230; OSF registration https://osf.io/3htn8/, DOI
10.17605/OSF.IO/3HTN8, approved and public before execution;
registration record completed by PR #204, merge d08b6e3e)
under the owner's order of 2026-10-13. Infrastructure PR #210:
the Phase-396 build (backend/scripts/phase396_pred006_step0.py),
the experiment graph node IndusPhase396Pred006Scoring, and 5
machinery tests. Step 0 ran in the frozen order, before any
counting. Check 3.1 PASSED: the classification recomputed from
the recorded training corpus reproduces the recorded
global_class_stability output exactly (105 classifiable signs,
no differences), and the trained INITIAL set froze at the
recorded 12 signs (P000, P001, P004, P013, P051, P098, P217,
P238, P265, P301, P310, P324). Check 3.2 FAILED, and the study
closed there: the recorded classification trained on the
combined corpus (data/normalized/corpus_master.csv; 2,722
inscriptions = 179 CISI, Mohenjo-daro only, + 2,543
Yajnadevam), and 970 of the Yajnadevam inscriptions inside
that training corpus are Harappa inscriptions carrying 1,013
occurrences of 11 of the 12 trained signs (P324 468, P098 254,
P217 91, P004 64, P310 60, P013 33, P001 16, P301 16, P238 5,
P051 4, P265 2, P000 0). The withholding the registration
specified was never real for this lineage, so under spec
section 3 / F032-C05 the outcome is CANNOT BE RUN AS WRITTEN
— a step-0 closure, not a verdict. Check 3.3 was not reached;
the registered scoring never ran; no Harappa start rate was
computed and no share exists. PRED-2026-006 remains unscored;
its register entry stands unchanged, annotated by an
append-only dated entry under register section 6 recording
this closure. Step-0 record sha256
26781336c8c34b006e62474448b17be4d895c1d7ea06d5c24418d49a38e7c4e7.
Outcome recorded at
specs/032-pred-2026-006-harappa-breakdown/outcome.md, with
per-claim determinations for F032-C01…C12 (the frozen register
is not edited). Gates: foundation check 40 passed / 0 failed /
8 warnings; branding sweep clean. The Spec 029 Phase D
register-hash pin (test_pred_register_document_untouched) was
advanced by name in the products PR to the post-append hash,
the append being the one authorised drift (Spec 032 spec
section 7); the Spec 029 freeze replay is unaffected.

## 2026-10-13 — Spec 033 EXECUTED (Phase-397): verdict NOT SUPPORTED

The SA-free rerun of the language comparison is complete, under
the frozen contract (digest
412b4805063bbffb3915a834354cb428cc9b10958f614a1680b859005a43b66d;
registered before execution at OSF osf.io/ephf7, DOI
10.17605/OSF.IO/EPHF7). On the strict sign set (94 signs; 1,722
scored sequences from the Mahadevan-lineage corpus as held),
mean log probability per sign: no-language baseline −2.6233,
Dravidian −2.8465, Munda −2.8616, Sanskrit −3.1184. The frozen
bars required Dravidian to beat the best rival by at least
0.10 and to stand above the 99th percentile of 999 random
assignments of the same published values; instead the best
rival is the baseline itself (margin −0.2232), and the
Dravidian score lies inside the random assignments' range
(percentile 91.2; 88 of 999 scored above it; random maximum
−2.7215). Verdict: NOT SUPPORTED (claim F033-C11 fired; the
F033-C15 percentile condition fails with it). Dravidian still
finishes ahead of Sanskrit head-to-head (+0.2719) — reported as
a fact, not the verdict rule. The Harappa-removed sensitivity
reproduces the same ordering; the robustness arm (second
anchor list per family) puts Dravidian last of the three
families and carries no verdict weight. Per the frozen status
rule, the Dravidian-solution claim's inherited partial support
(Phase-41/43 numbers, produced by the semantic-anchoring
method falsified in Phase-107) is replaced by a dated entry in
its record and its status reclassified to unsupported (the store token for a not-supported standing); the
old numbers stay in history, labelled as SA-produced. The
verdict settles only the bounded claim: not the rebus method,
not any single sign reading, not a decipherment in either
direction. Full record:
specs/033-sa-free-language-comparison/outcome.md and
reports/phase397_results.json.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-13 — Phase-398 executed: Spec 034 matched-object attribution — ATTRIBUTED TO COMPOSITION

Execution of the frozen Spec 034 contract (design D-20: why the
two compilations disagree; freeze digest 696fd185; OSF
registration https://osf.io/zd7uq/, DOI 10.17605/OSF.IO/ZD7UQ,
approved and public before execution; registration record
completed by PR #208, merge ca07abe8) under the owner's order of
2026-10-13. Infrastructure PR #213 (merge 32f303c4): the
Phase-398 build (backend/glossa_lab/phase398_matched_object.py),
the experiment graph node IndusPhase398MatchedObjectAttribution,
and 8 machinery tests fencing the join discipline. Step 0 built
the object bridge through the three frozen routes. Route (a),
the CISI catalogue layer (7,705 rows; 3,493 distinct objects),
attests all 179 mayig-layer objects. Route (b), the Mahadevan
side's published object references — the ICIT published corpus's
per-inscription CISI references, admitted as a Phase-130
intake-schema dataset (validation pass, 0 errors, 0 warnings;
5,018 inscriptions, 4,074 distinct objects) and joined on
provenance.object_id only — matched 179 objects: every mayig
object has exactly one ICIT inscription citing it. Holdat
cisi_number was never read and never used as a join key
(F034-C06; spec 019 section 2.1). Route (c), the 44 Phase-128
dossiers, intersects 61 of the gate objects (17 anchors). The
frozen gate — at least 150 matched objects with texts of three
or more signs in both compilations — is met at 169 (the 10
below-condition objects are listed in the outcome); a
kept-status sensitivity count gives 159, so the gate passes
under both counts, and no content deduplication was applied to
the bridge (identity rests on the published reference, not on
text uniqueness). Step 1 ran Phase-125's own measurement
(evaluate_arm: total variation, floor 8, the 286 PRIMARY pairs)
on the 169 matched objects only: 25 judgeable pairs (the
corpus-level run had 16), matched-object median TV 0.025694,
modal agreement 1.0, Spearman rho 0.898039 / 0.932164 /
0.850948, shuffle null p = 0.001. Under the frozen section 6
lines the outcome is ATTRIBUTED TO COMPOSITION (0.025694 <=
0.20); the falsifier (at or above 0.32) did not fire. In
Phase-131's persistence estimator the matched-object residual
is 0.040340 of the corpus-level 0.636931, against the 0.938679
share Phase-131 left unexplained without an object bridge.
Decomposition in Phase-131's categories over the 29
all-or-nothing-mappable objects: 22 identical, 1 order-only
(M-67, the same signs rotated by one position), 6 substitution;
difference-block token shares segmentation 0.0, substitution
0.909091, insertion/deletion 0.090909; the 10 substituted
positions checked against the crosswalk as a record of
disagreement — 0 conflict pairs, 0 crosswalk-attested, 10 with
no crosswalk row. The matched subset is all Mohenjo-daro seals
(the CISI vols 1–2 population the mayig layer transcribes), and
the verdict statement carries that description (F034-C12).
Nothing was written into the Phase-125/127/131 records, which
stand as issued (F034-C14); the anchors file was asserted
byte-identical before and after. Outcome recorded at
specs/034-matched-object-attribution/outcome.md, with
per-claim determinations for F034-C01…C14 (the frozen register
is not edited); full record at reports/phase398_results.json
and reports/phase398_matched_object_attribution.md. Gates:
foundation check and full suite in the products PR's CI;
branding sweep clean (run-time local suite side effects on
claims-store files were identified as test-harness writes and
discarded uncommitted; the run itself writes only its two
report files).
## 2026-10-13 — PRED-2026-010 registered: clean-withholding successor to PRED-2026-006

By owner order (Tristen Pierson, 2026-10-13), the successor
prediction called for by the Phase-396 closure was
registered the same day. PRED-2026-010 restates
PRED-2026-006's prediction and bars (at least 70% of the
trained INITIAL signs showing start_rate at least 0.40 at
Harappa) with the withholding made clean by construction:
the trained set was derived at registration by the recorded
global_class_stability logic (verbatim, imported from the
frozen Phase-396 build) over the CISI Mohenjo-daro pool
only — 179 inscriptions, 28 classifiable signs, INITIAL
set P000, P217, P324 (3 signs; registration derivation:
backend/scripts/pred010_register_derivation.py, record:
reports/pred010_derivation_record.json). The training
pool, filtered-pool manifest, withheld file, and crosswalk
are pinned by SHA-256 in the register entry; the
small-set caveat (the 70% bar passes only at 3 of 3) and
the disclosure (cleanliness = verified training-pool
exclusion, not analyst blindness; the Harappa pool was
inspected in aggregate during the Spec 032 audit) are
stated in the entry. Register handling: insertions only
(+20/-0 lines: the section 3 entry and a dated section 6
note); PRED-2026-006's entries are byte-identical and it
remains unscored. The Spec 029 Phase D register-hash pin
(test_pred_register_document_untouched) was advanced by
name a second time for this authorised append. OSF
Preregistration filed from the Predictions &
Registrations node (nrb9u): https://osf.io/wjebq/,
pending admin approval at filing (one API approval
attempt, HTTP 409, recorded; admin notification Gmail
1a1354c8d63d4ab9; record: docs/pred-2026-010-osf-registration.md).
No scoring ran; no Harappa start rate was computed for
any sign; the withheld file was byte-hashed only.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — Spec 035 design draft (PRED-2026-010: scoring the clean-withholding successor)

Spec 035 is drafted, not frozen: draft PR #218 carries
specs/035-pred-2026-010-scoring/ (spec, claims
F035-C01…C15, adjudication, plan, tasks, the OSF
verification record, the draft freeze record; draft
digest b68b102f193276a970791c8a293f567d7e4af86e893a5021ec3048b0d0fb5806).
It designs the scoring of PRED-2026-010 exactly as
registered: trained set P000, P217, P324 derived from
the CISI Mohenjo-daro pool only; criterion at least
70% of the trained signs at Harappa start rate at
least 0.40, which with 3 signs passes only at 3 of 3;
step 0 fail-closed in a fixed order (registration
re-verification; input pins; training-pool
re-verification; crosswalk coverage), the withheld
file's content opened only after all four pass. The
prediction's OSF preregistration (wjebq, DOI
10.17605/OSF.IO/WJEBQ) was API-verified accepted and
public at draft. Draft-stage coverage observation,
recorded in spec section 0.4 and adjudication.md:
under the frozen Phase-396 crosswalk reading, P000
has no best-match counterpart, so execution is
expected to close at step 0.4 as CANNOT BE RUN AS
WRITTEN, unscored; the formal determination remains
a step-0 act. AEE hooks have not run on the draft
register; they are a freeze gate. Nothing was
executed, no Harappa content was opened for content,
and the freeze and any execution (Phase-399) are the
owner's separate decisions.

## 2026-10-20 — PRED-2026-011 registered: clean-withholding successor to PRED-2026-010 with disclosed mappability screen

By owner order (Tristen Pierson, 2026-10-20), the successor
prediction prepared in the draft package merged the same
day (PR #219) was registered. PRED-2026-011 restates
PRED-2026-010's prediction and bars (at least 70% of the
trained INITIAL signs showing start_rate at least 0.40
at Harappa) with one disclosed design change, stated
before registration: the trained set is screened for
mappability against the frozen public crosswalk — an
INITIAL sign is eligible only if a crosswalk row names
it as best_parpola_match. The screen was applied to the
reproduced PRED-2026-010 derivation (179 CISI
Mohenjo-daro inscriptions, 28 classifiable signs,
unscreened INITIAL set P000, P217, P324; derivation:
backend/scripts/pred011_register_derivation.py, record:
docs/research/pred-2026-011-registration/derivation-record.json)
and yields the trained set P217, P324 (2 signs). P000
was excluded because it has no best-match counterpart
(it appears only in top3_parpola), not because of any
observed Harappa behaviour; no Harappa data informed
the design. The training pool, filtered-pool manifest,
withheld file, and crosswalk are pinned by SHA-256 in
the register entry; the small-set caveat (the 70% bar
passes only at 2 of 2; either outcome concerns only
the exact two-sign criterion) and the disclosure
(cleanliness = verified training-pool exclusion, not
analyst blindness; the Harappa pool was inspected in
aggregate during the Spec 032 audit) are stated in the
entry. Register handling: insertions only (the section
3 entry and a dated section 6 note); every existing
entry is byte-identical. The Spec 029 Phase D
register-hash pin (test_pred_register_document_untouched)
was advanced by name a third time for this authorised
append. OSF Preregistration filed the same day from the
Predictions & Registrations node (nrb9u) under the
same owner order; the verified URL and DOI are recorded
by append on approval (record:
docs/research/pred-2026-011-registration/README.md).
No scoring ran; no Harappa start rate was computed for
any sign; the withheld file was byte-hashed only.
Scoring requires its own future spec and owner order.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — Spec 035 freeze (PRED-2026-010 scoring contract frozen)

Spec 035 is FROZEN under the owner's freeze-and-execute order of 2026-10-20 ("go with your recommendation"; adjudication section 4): this PR merges the finalised freeze record (freeze digest d72a50e1943c1af55846dfb2db93e73b50e08a287c06925a331c0304096128c4). The claim register passed the AEE lifecycle hooks at the freeze act — after_specify after four recovery rounds (30, 9, 8, then 0 failure modes), after_plan and after_tasks at the first pass — over register 0.8-draft; the digest covers the recovered register, never the pre-recovery draft. DD-035-2 stands as drafted; DD-035-4 is decided: the frozen spec files its own OSF contract registration (its record lands in osf-spec-registration.md, completed by append on approval). Execution is Phase-399, ordered in the same act: step 0 in the frozen order, with the step-0.4 closure expected on the section 0.4 observation.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — Phase-399 outcome: PRED-2026-010 closed at step 0 (CANNOT BE RUN AS WRITTEN, unscored)

Phase-399 executed Spec 035 step 0 in the frozen order on 2026-10-20, under the owner's freeze-and-execute order. Checks 0.1–0.3 passed: the prediction's preregistration (wjebq) stood accepted and public; all registered input pins matched; and the CISI-Mohenjo-daro-only pool re-derived as registered (179 inscriptions, filtered-pool manifest hash matched), with the recorded classification reproducing the trained set {P000, P217, P324} exactly — the clean withholding verified. Check 0.4 closed the study: under the frozen crosswalk reading, P000 has no best-match counterpart (P217 → Y0520 at confidence 1.0; P324 → Y0740 at 0.9867), so one of three trained signs is unmappable — 33% against the registered 20% cap. Recorded outcome: CLOSED AT STEP 0 — CANNOT BE RUN AS WRITTEN, unscored, not a refutation; the withheld file was never opened and no Harappa count or start rate was computed. PRED-2026-010 remains unscored (register section 6 dated append; its section 3 Outcome stays PENDING per F035-C15; section 4 gains no entry); PRED-2026-006's record is untouched. Step-0 record: reports/phase399_results.json (step-0 record sha256 e231baf4cd0c664211089c6758296c10a035062b6566ac5200407872e4aeee1f). The spec-level OSF registration (qkj8d) was filed before execution under DD-035-4; its record completes by append on approval (PR #221).

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — PRED-2026-011 registration completed: OSF registration approved and public (t6whq)

The OSF Preregistration for PRED-2026-011, filed earlier
the same day from the Predictions & Registrations node
(nrb9u) under the owner's registration order, was
approved via the token link in OSF's
admin-notification email and verified approved and
public by API on 2026-10-20: registration t6whq,
https://osf.io/t6whq/, DOI 10.17605/OSF.IO/T6WHQ
(reviews_state accepted; public;
pending_registration_approval false; not withdrawn;
registered_from nrb9u; date_registered
2026-10-20T12:54:02Z). The verified URL and DOI are
recorded in the prediction register by a dated
section 6 append only; the registration package
README is flipped to REGISTERED with the same
identifiers, and the Spec 029 Phase D register-hash
pin was advanced by name a fifth time for this
authorised append. The registration's OSF emails
(draft-created notice and admin notification) were
archived after the API verification, per the
standing rule. PRED-2026-011 stands PENDING and
unscored; no scoring ran and no Harappa start rate
was computed. Scoring requires its own future spec
and owner order.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — Spec 039 design draft (gazetteer period assignment: the Spec 027 §6.2 act, published determinations only)

Spec 039 is drafted, not frozen: this draft PR carries
specs/039-gazetteer-period-assignment/ (spec, claims
F039-C01…C15, adjudication, plan, tasks, the draft
freeze record, and the pre-written outcome skeleton;
draft digest
52ca7dfc6ae0b7dc6ad22eb7f5f045ccf8f2e5d364108f0ec7c752e6a2e4f9dd).
It designs the Spec 027 §6.2 gazetteer
period-assignment act under the owner's decisions of
2026-10-20, recorded in its adjudication record as
DECIDED: (D1) the act is authorised, bundled with
the D-25 chronology test (one adjudication cycle;
this act executes first; D-25's own spec consumes
the assigned gazetteer as a hash-pinned input);
(D2) the evidence standard is Option 1 — published
period determinations only, every label traced to a
named publication with its locator, and no
program-derived assignments (Option 2 was not
adopted; no label is inferred from chronology-spine
dates). The act assigns program_period_assignment
per program site (36 rows, 30 sites; the field
stands null on all 36 rows on main, gazetteer
SHA-256
5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6),
carried onto every row for the site with its
mapping rule, reviewer, and per-determination
citations; disagreements are flagged contested and
carried verbatim — no majority vote (§6.3) — and
Spec 030 Ask 2 stays RESERVED, undecided by this
act. Outputs: a new assigned-gazetteer file (the
pre-act file is never edited), an assignment
report, and a new version of the Stage 0 Zenodo
record 23300361 (the existing deposit is never
edited). The act's verification step re-runs only
the period-eligibility gate of the Phase-395
margins step; the standing link mass (2
link-eligible sites, 1 linked pair, against floors
of 8 and 10) is unaffected and is stated wherever
the act's effect is described, and no study
verdict changes. Open for the freeze:
DD-039-1…DD-039-6 with recommendations (label set
Early/Mature/Late Harappan; four-tier citation
hierarchy; the TwoRains published-venue rule;
Masudpur establishment — recommended default not
in this act; the margins re-run as this act's
verification step; the spec's own OSF contract
registration). The AEE lifecycle hooks have not
run on this draft; they are the freeze gate.
Nothing was frozen, executed, or assigned by this
draft.
## 2026-10-20 - Spec 037 DRAFTED: CISI 3.1 concordance spine and HARP provenance annex (design only)

Under the owner's order of 2026-10-20 to move the
CISI follow-on uses forward, Spec 037 was drafted
as a DRAFT PR and left unmerged for the owner's
freeze decision. It designs the two candidate
uses the CISI 3.1 intake assessed (intake report
sections 7.5-7.6), over material held under the
Phase-130 gate (restricted store PROVENANCE entry
22: local use, extraction, and publishable derived
statistics permitted; redistribution of scans or
row data prohibited; nothing derived enters git).
Workstream A is the pilot test of the intake's 693
exact-string matches against corpus_master: all
693 graded as a census under a fixed ladder (site
mandatory; object type mandatory where graded, a
seal and a seal impression distinct classes; FC /
excavation / museum corroboration where records
exist on both sides; number-level ambiguity bars
VERIFIED) into VERIFIED / CONFLICT / UNRESOLVED,
with a seeded hand-check stratum attributing
conflicts to causes, a 20 percent conflict-share
halt rule on the spine build, and the spine itself
written only as a local table in the restricted
store. Workstream B is a descriptive annex of the
HARP rows' dig-year, lot, and period-code
structure, floor caveat attached; it does not
change the Spec 031 (Q7) record and feeds no
verdict. The fences are in the draft's first
section: a string match is not a same-object join;
the concordance is a finding aid, not evidence
about readings; no PRED-2026 entry can be scored
from this material (the tables carry no sign
transcriptions). Governed register F037-C01..C15;
draft digest
f5c489f17ad671470d6d18cd76b52defc09fa25280d3f90c326f290ee79ec140
over register 0.5-draft; AEE lifecycle hooks not
run (a freeze gate). Nothing was executed, no
join was computed, no candidate was graded, and
no portion row content was read for the design:
the draft rests on the intake's aggregates, the
gate record, and byte-level integrity checks.
Execution is Phase-401, gated on the owner's
separate freeze and execution orders.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — Phase-400 outcome: PRED-2026-011 CONFIRMED (2 of 2)

Phase-400 executed the frozen Spec 036 contract on
2026-10-20, under the owner's do-all order. Step 0
passed in full, in the frozen order: the prediction's
preregistration (t6whq) stood accepted and public; all
registered input pins matched; the CISI-Mohenjo-daro
pool re-derived as registered (179 inscriptions,
filtered-pool manifest hash matched), the recorded
classification reproduced exactly (28 classifiable
signs; unscreened INITIAL set {P000, P217, P324}), and
the registered mappability screen re-applied returned
{P217, P324} exactly, with P000's exclusion reproduced
as a screen outcome; and crosswalk coverage passed
(P217 → Y0520, confidence 1.0, confirmed; P324 →
Y0740, confidence 0.9867, confirmed, conflict-flagged;
no unmappable trained sign). The withheld file was
opened only behind the full pass, and the registered
computation ran once, in full, over its 2,717 Harappa
rows (2,621 tokenised sequences, 7,144 tokens): P217 —
119 Harappa occurrences, 104 initial, start rate
0.8739; P324 — 774 Harappa occurrences, 473 initial,
start rate 0.6111. Both signs meet the 0.40 bar: share
1.0 (2 of 2) against the registered 70% criterion —
**CONFIRMED**, on the exact two-sign criterion. The
verdict concerns only P217 and P324 in this pinned
dataset; it does not validate the INITIAL class as a
whole and says nothing about P000. PRED-2026-011's
section 3 Tested/Outcome fields move from PENDING to
the verdict in the same act (register section 6 dated
append; the Phase D register-hash pin advanced by
name a sixth time for that authorised change).
PRED-2026-006 and PRED-2026-010 remain unscored and
untouched. Step-0 record sha256
2bf0333b7d7fc437c9055299598ee83f0247acd08c7fa8b123044114e0c8e427;
scoring record sha256
101d54f5bd93d963402d73731962801294452c00f4fe4183e9135ba348ddb07f
(reports/phase400_results.json). The spec-level OSF
registration (gjen4) was filed before execution under
DD-036-4; its record (osf-spec-registration.md)
completes by append on approval.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — Maintenance: aee 1.5.0 adopted (pin >=1.5.0,<1.6)

Owner decision 2026-10-20: adopt aee 1.5.0. This change lands
only after Spec 036's freeze merged (PR #224, merge
`3419df564b70`), per the sequencing the owner set: no pin or
engine change on main while that freeze was in flight.

Change: `backend/pyproject.toml` now declares
`applied-epistemic-engineering>=1.5.0,<1.6` (was
`>=1.0.4,<1.5`, PR #181). Engine versions before/after: CI
resolved aee **1.4.0** under the old declaration; the adopted
line is the 1.5.x series (methodology 2.0). The upper bound
`<1.6` is justified two ways: the engine's own changelog
records 1.5.1–1.5.3 as documentation/metadata-only (verified
directly: the 1.5.0 and 1.5.3 wheels differ only in
`aee/_version.py`), and this PR's CI resolves the newest
1.5.x and is green, as is the suite under 1.5.0 exactly.

First-hand census (full backend suite under aee 1.5.0 on the
pre-adoption main, CI-identical invocation): **17 failed /
1368 passed / 7 skipped**, against CI green on the same tree
under the old pin. Every failure is class (a) — a test encoding
pre-1.5 behaviour the engine intentionally changed; no
class-(b) regression or ambiguity was found. Dispositions:

- **Score semantics (3).**
  `tests/test_aee_core.py::test_score_dict_shape`: FR-8.7
  substance-over-presence scoring gives the fixture's
  falsification string (no checkable condition) partial credit
  0.5, not 1.0; the expectation now asserts 0.5 and says why.
  `tests/test_spec029_phase_a.py::test_score_propagation_byte_identical_to_pre_change`
  and `tests/test_spec029_phase104_correction.py::test_score_movement_is_exactly_the_three_corrected_claims`:
  their byte-pinned score fixtures were re-baselined into
  successor fixtures
  (`spec029_post_merge_aee150_scores.json`,
  `spec029_post_phase104_correction_aee150_scores.json`;
  pre-1.5 fixtures preserved untouched, per this repo's
  supersession pattern). The full per-claim delta audit shows
  only documented methodology-2.0 changes: FR-8.7 boundary
  credit 1.0 -> 0.5 for the adapter's single-token
  `testability=...` boundaries (all 23 claims), FR-8.7
  falsifiability credit 1.0 -> 0.5 where a falsification
  string states no checkable condition (7 claims), FR-8.13
  unrounded components (evidence values identical to 1e-9)
  and the added `declared_state` / `propagation` score-dict
  keys, and FR-8.6/8.7 note texts. The Phase-104 movement
  assertion survives exactly: between the two regenerated
  fixtures, precisely the three corrected claims move, each
  by the contradiction penalty (before 0.139375 / band low;
  after 0.0 / band unknown; penalty 0.75).
- **Strict bundle validation (14).** aee 1.5.0's
  `Claim.from_dict` is strict by default: it refuses a
  scalar `boundary` (the model declares a list of strings)
  and requires the lifecycle `stage` field. Every frozen
  register (Specs 026, 029–036) predates both — `boundary`
  stored as a plain string, no `stage` field. The frozen
  register bytes are NOT modified, and the freeze test
  files cannot be edited either: each spec's freeze digest
  covers its own test file, so any edit breaks that spec's
  freeze-replay test (verified first-hand). The
  compatibility therefore lives in `backend/tests/conftest.py`:
  claim dicts carrying the legacy signature (a string
  `boundary` or no `stage` field) are loaded leniently
  (`strict=False` — the FR-1.3 compatibility path the
  engine's own error text names for historical bundles,
  reproducing the pre-1.5 loader semantics exactly); every
  other claim dict keeps strict loading. No production
  code loads registers through `Claim.from_dict`, so no
  runtime code changes.

Foundation check and the full backend suite are green on
this PR (CI 7/7, including the backend suite resolving the
newest 1.5.x under the new declaration).

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution
sec.VI.
Spec 038 draft (PRED-2026-007 full-population census and scoring, D-31)

Spec 038 is DRAFTED under the owner's draft order of
2026-10-20 (D-31 will be frozen for execution; this
step drafts only): the scoring contract for
PRED-2026-007 (H4: ICIT Function Alignment,
registered 2026-04-22), which stands PARTIALLY
CONFIRMED on a partial check of three named signs
(recorded 2 of 3, 67%, against the 70% bar), the
total ITM population never recorded. The design
(D-31, PR #195) first enumerates every ITM-coded
sign from the named primary source
(reports/indus_cgsa_cluster_analysis.json,
data.a[].icit_function; cross-check
data/crosswalks/canonical_sign_registry.csv;
conflict rule fixed before enumeration), then
scores the registered criterion (>= 70% of
ITM-coded signs TERMINAL or in TERMINAL clusters)
over the full population, reading only the recorded
CGSA Phase 5 output — no re-clustering; cluster
classes per the disclosed DD-038-9
operationalisation (the class recorded in
reports/cluster_characterization.md). The verdict
rule is mechanical and no outcome is pre-written
for any branch (DD-038-1: the register's recorded
67% is a pre-execution figure whose denominator
mixed in the LOG-coded P098, which the frame
excludes by rule). Claims F038-C01...C14; draft
digest
97b13bd1622664fe8dce7da4103b6f4206dabc9ff76b805addb5490b062b947b.
AEE hooks have not run on the draft register; they
are a freeze gate, run at the freeze act under aee
1.5.0 (DD-038-7). DD-038-6 is an open proposal for
the freeze decision (file the frozen spec's own OSF
contract registration). Nothing was executed,
nothing was frozen, and the ITM population was NOT
enumerated; the freeze and any execution
(Phase-401, provisional) are the owner's separate
decisions.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — Spec 038 FROZEN (D-31: PRED-2026-007 full-population census and scoring)

Spec 038 is FROZEN under the owner's
freeze-and-execute order of 2026-10-20 ("Freeze
D-31 for execution"), and Phase-401 execution
is ordered in the same act. The AEE lifecycle
gate ran under aee 1.5.0 (DD-038-7) — the first
freeze gate under the 1.5 engine — over the
recovered register 0.7-draft: three recorded
rounds at after_specify (24, then 20, then 14
failure modes, the last all FR-2.3 draft-cap
records; 0 correctness failure modes and 0
claims below the 0.70 threshold from round 2
on), after_plan and after_tasks clean at the
first pass each; the gate reading under aee
1.5.0 is recorded as DD-038-10. Freeze
decisions (adjudication.md section 6):
DD-038-6 YES (the frozen spec files its own
OSF contract registration); DD-038-8 decided —
Phase-401 is allocated to Spec 038 on the
merged record. The freeze digest is recorded
in specs/038-pred-2026-007-full-population/freeze.json
and computed over the recovered register and
the finalised freeze texts, once.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — Phase-401 (Spec 038) EXECUTED: PRED-2026-007 CLOSED AT STEP 0 — CANNOT BE RUN AS WRITTEN (unscored)

Phase-401 executed the frozen Spec 038 contract
under the owner's freeze-and-execute order.
Step 0.1 passed in full (register and all four
sources hashed to the freeze record; the
PRED-2026-007 entry standing as registered).
Step 0.2 closed the study: the enumeration of
the frozen primary (reports/
indus_cgsa_cluster_analysis.json,
data.a[].icit_function; 611 records, count
reconciled) returned zero ITM-coded signs, and
the held-record verification failed — P385's
record carries an empty icit_function value and
P378 has no record in the primary. In this file
the field is not a coded field: 579 of its 611
values are empty, 32 are free-text decipherment
glosses, and no record carries ITM or LOG.
Check 0.3 never ran; the Phase 5 output was
never read for assignments; no scoring figure
exists. PRED-2026-007 remains unscored; its
PARTIALLY CONFIRMED wording stands as the
pre-execution record; the register gained the
dated outcome entry and the DD-038-2 provenance
reconciliation note (the function codes descend
from Wells-derived catalog lines, not "mayig
features"). Record: specs/
038-pred-2026-007-full-population/outcome.md;
reports/phase401_results.json (step-0 record
sha256
4c026edc92cdcb0c1ba6821f5ebc8242b498bb9fc4cd158607d9b1ded24a784a).

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 — Spec 038 freeze-test amendment (owner-ordered)

On the freeze coordinator's recommendation, the
owner ordered the amendment on 2026-10-20,
verbatim: "Approve the freeze-test amendment".
The defect: the Spec 038 freeze fence
test_cited_records_carry_the_design_facts in
backend/tests/test_spec038_freeze.py asserted
the live whole-file SHA-256 of
docs/PREDICTION_REGISTER.md equals the
freeze-cited pin
4f8aeb54fd5853d73766ed9cf0222ef93cccfa8d9a8c399a4631221fbbb4c1c2,
while the frozen contract itself (spec section
7; DEFINITION register_handling) mandates dated
section-6 appends to that same register at
execution. PR #232 makes exactly those appends
(the Phase-401 outcome entry and the DD-038-2
provenance reconciliation note), advancing the
register's live hash to
f281bd674d7651e9c13351bad7cb321bd55000cd3f087a38276a4451fbbf7ef3,
so the fence failed by construction — the
single failure in an otherwise 1,400 passed /
20 skipped backend suite. The amendment narrows
that single assertion to the Spec 035 form
(the PRED-2026-007 entry's facts asserted on
the live register file; the freeze-time
whole-file hash remains asserted as a
DEFINITION constant and in the freeze record);
the other five cited files keep their live-hash
assertions; no other assertion changed and no
production code changed. freeze.json was
recomputed ONCE over the amended covered
sources with the repo's own builder
(specs/038-pred-2026-007-full-population/build_freeze.py,
framework026 build_freeze) in the freeze
environment (python 3.12.3, aee 1.5.0):
successor digest
11dfda0384fa966b14e4fc537a9be935e899c8318f079c3bff1e4f35c790930b.
The freeze-act digest
b54571d845a2be3429bc532fee4bb58c20723f77e2d40ffcd43b56e0caab6eef
stands as the digest of the freeze act in every
record that cites it (the OSF contract
registration bkqeh, outcome.md, the PRED
register entries, adjudication.md section 6)
and was edited nowhere. Record:
adjudication.md section 7; freeze.md addendum;
this entry. PRED-2026-007 remains unscored;
its PARTIALLY CONFIRMED wording stands.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.
## 2026-10-20 — Spec 037 FROZEN and Phase-402 EXECUTED: PILOT COMPLETE — SPINE HALTED

Spec 037 (CISI 3.1 concordance spine and HARP
provenance annex) was frozen and executed the same
day under the owner's standing pipeline
authorisation of 2026-10-20 (freeze order 038,
then 037, then 039, then 040). Freeze: the AEE
lifecycle gate ran under the adopted aee 1.5.0 —
after_specify cleared in three adjudicated rounds
(register recovered 0.5-draft to 0.7-draft; round 1:
37 failure modes; round 2: 27; round 3: the 15
FR-2.3 draft-cap records only, zero correctness
failure modes, no claim below the 0.70 threshold,
minimum propagated 0.72), after_plan and
after_tasks clean at first pass, the gate read
under DD-037-9 (adopting Spec 038's DD-038-10).
Freeze decisions DD-037-4 to DD-037-9 are recorded
in adjudication.md section 4 (halt threshold
confirmed at 20% of all candidates; hand-check
stratum 60; Workstream B inside Phase-402 gated on
step 0 only; the spec's own OSF registration —
filed as j6t9k, pending approval at this record;
phase allocation Phase-402). Freeze digest
122c2ea4858094d2c6514d05225dfaad1f5266cccffd764949736a78d81aa4db,
computed once over the frozen contract; PR #225
merged on a genuine 7/7 CI run (backend 1,479
passed / 20 skipped), merge commit e9b5026c.

Execution (Phase-402) ran graph-first (script,
graph node IndusPhase402Concordance, registration
committed before any run). Step 0 closed two runs
on defects in the execution's own checker — a gate
needle phrased from a paraphrase rather than
PROVENANCE entry 22's own words, then a census
assertion that counted raw strings (2,106) where
the intake's census counts resolved numbers (2,101
well-formed plus 5 garbled low-confidence tokens) —
each corrected openly and committed before the
re-run; no candidate was graded by either closed
run. The third run passed step 0 in full (gate on
record; portion PDF hash at the pin; local table
2,123 x 26 with its intake census and the
execution's own table hash 7179858d...; corpus_master
at its pin over the exact bytes consumed; repo
cleanliness PASS). The pilot regenerated the intake's
693 candidates exactly (289 / 102 / 302) and graded
the full census under the frozen ladder: VERIFIED
269 (38.82%), CONFLICT 341 (49.21%), UNRESOLVED 83
(11.98%). Conflicts: TYPE 339, NUMBER-AMBIGUOUS 2,
none on site; corroboration was UNGRADED for every
candidate (corpus_master carries no FC, excavation,
or museum values — graded bases: site 693, type
610, corroboration 0). An independent recount
re-graded all 693 with 0 mismatches. The seeded
hand-check stratum (seed 20261020; 30/15/15)
attributed all 15 sampled conflicts to genuine
compilation divergence (the portion's tablet
headings against the corpus's seal classing of the
same objects); the 30 sampled VERIFIED candidates
all spot-checked sound. HALT RULE FIRED: the
conflict share of 49.21% exceeds the frozen 20%
cap, so no spine file was written; the outcome is
PILOT COMPLETE — SPINE HALTED, as the contract
phrases it. Workstream B (inside the phase, gated
on step 0 only) reported the HARP annex as
descriptive aggregates: dig years 1986-2001 with
312 no-token rows; lot/record (registration) fill
754 of 1,094; period fill 656 of 1,094 as a FLOOR
(the scan's text layer loses split period tokens);
the full period-code inventory. The Spec 031 (Q7)
finding is unchanged. All row-level products
(grade table, build record, stratum attribution)
live only in the restricted portion folder; the
repo carries aggregates only. The PRED register
and the anchors are untouched; no prediction was
scored, advanced, or retired. Outcome record:
specs/037-cisi31-concordance-spine/outcome.md;
aggregate machine record: reports/phase402_results.json.
## 2026-10-20 — Spec 039 freeze (gazetteer period assignment: Phase-403 allocated)

Spec 039 is frozen under the owner's standing
pipeline authorisation of 2026-10-20, after Specs
038 and 037 in the freeze order. The AEE lifecycle
gate ran under aee 1.5.0: after_specify cleared in
three adjudicated rounds (20 failure modes over
register 0.5-draft; 17 over the 0.6 recovery text;
15 FR-2.3 draft-cap records only over 0.7-draft),
after_plan and after_tasks clean at first pass; at
every hook zero correctness failure modes and no
claim below the 0.70 threshold (minimum propagated
0.72). DD-039-1…DD-039-6 were decided as
recommended (coarse Early/Mature/Late Harappan
label set; four-tier citation hierarchy,
presentation only; the TwoRains published-venue
rule with doubtful venues not counting; Masudpur
not established — the act is confined to the
existing 30 sites; the margins re-run as this act's
verification step, confined to the period-eligibility
gate; the spec's own OSF contract registration
filed at the freeze). DD-039-7 allocates the
execution phase as Phase-403, and DD-039-8 adopts
the DD-038-10 / DD-037-9 AEE gate reading. The
scheme-aware mapping table is frozen in spec §4
before any assignment. The labels remain finding
aids, not dating evidence; the act changes no
verdict, and in-universe link mass stands at 2
link-eligible sites and 1 linked pair against
floors of 8 eligible sites and 10 linked pairs.
Spec 030 Ask 2 stays RESERVED. Nothing was
assigned by the freeze itself.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.
## 2026-10-20 — Spec 039 execution (Phase-403: gazetteer period assignments)

Spec 039 was executed as Phase-403 under the
frozen contract (freeze digest ec53a841…;
freeze PR #226 merged at 05f961fc). The pre-act
gazetteer verified against its frozen pin
(5ac76a30…; 36 rows, 30 sites, assignments null
×36) and was not modified. From published
determinations only, mapped through the frozen
table: **11 of 30 sites assigned** (17 of 36
rows), **1 contested** (banawali — the site
report maps to {Mature Harappan}, a 2014
journal review to {Early Harappan, Mature
Harappan}; both retained), **19 blank** (9
OUTSIDE_LABEL_SET, 8 NO_PUBLISHED_DETERMINATION,
2 UNMAPPED_SCHEME_VALUE). Output A:
data/movement/gazetteer_rows_assigned.jsonl
(sha256 64f288d3…), byte-identical to the
pre-act file outside the assignment field
(independent recount). The margins verification
step (DD-039-5) re-ran the F031-C10 eligibility
gate over Output A: 8 period-eligible sites
with contested counted, 7 with contested
excluded — and the step closes at the link-mass
floor: in-universe link mass is unchanged at 2
link-eligible sites and 1 linked pair against
floors of 8 eligible sites and 10 linked pairs.
Output C: a new version of Zenodo record
23300361 was deposited through the release gate
(PASS, 3/3) — record 23523454, DOI
10.5281/zenodo.23523454 — carrying the assigned
gazetteer for the 21 verified-open rows and the
assignment report; the existing version was not
edited. The OSF contract registration
(https://osf.io/w38ha/) stands FILED — PENDING
APPROVAL at this entry; its completion record
follows on verification. The labels are finding
aids, not dating evidence; no study outcome
changed: Q7 still fails its link-mass floors,
Q6 remains NOT-YET-TESTABLE, and Spec 030 Ask 2
stays RESERVED. Outcome record:
specs/039-gazetteer-period-assignment/outcome.md;
machine record: reports/phase403_results.json;
report: reports/phase403_gazetteer_assignment_report.md.

AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 - Spec 040 DRAFTED: D-25, the chronology-controlled rerun of G1 (design only)

Under the owner's bundle decision of 2026-10-20
(gazetteer period-assignment act first, then
D-25; evidence standard published period
determinations only), Spec 040 was drafted as a
DRAFT PR and left unmerged for the owner's
freeze decision. It designs design D-25 from
the PR #195 portfolio: the chronology-
controlled rerun of Spec 025's G1, the program's
strongest positive result (SUPPORTED under
composition and preservation control, Phase-385
governing basic CI [0.1838, 0.2102] above the
V = 0.10 floor), which still carries the rider
that chronology is not controlled. Period
enters as one added stratification
(composition x preservation x period) over the
Phase-137 population and columns; assignments
come only from Spec 039's frozen artifact at
site-period resolution (unique uncontested
published-determination mappings; contested
mappings excluded from the primary and included
in a labelled sensitivity); the governing
quantity is the Phase-385 v2 basic bootstrap
interval against the 0.10 margin, with the
outcome mapping written in advance (interval
entirely above: SUPPORTED - CHRONOLOGY
CONTROLLED, rider retired by append; straddling:
WEAKENED - RIDER CONFIRMED AS MATERIAL, G1
restated as a period-confounded association;
entirely at or below: CONTRADICTED AT THE
DECLARED MARGIN). The freeze is barred by a
fail-closed dependency gate until Spec 039 has
executed (its labels do not yet exist; D-25's
feasibility line had stated them as existing,
and the draft records that tension openly), and
an execution-stage margins gate (at least 5
sites in each coarse period, at most 40 percent
unassigned, at least 1,000 permutable) closes
the run NOT-YET-TESTABLE before any outcome
quantity exists. DD-040-1 records the decision
rule as re-derived from Spec 025's
permutation-p-only rule, for the freeze to
decide openly. Governed register F040-C01..C15;
draft digest
63ca1ac99ed106b7bb7cc3d0e324e7522617021ea353af2a6055d975d316ac85
over register 0.5-draft; AEE lifecycle hooks not
run (a freeze gate); the execution phase number
is unassigned at draft (Phase-401 is claimed by
the Spec 037 and Spec 038 drafts). Nothing was
executed: no label was joined, no margin
computed, the spine was not recomputed, and no
repertoire quantity was calculated.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-20 - Spec 040 CLOSED AT THE FREEZE GATE: NOT-YET-TESTABLE - dependency gate (D-25)

Spec 040's freeze act was reached under the
owner's pipeline order (freeze order
038 -> 037 -> 039 -> 040) and the dependency
gate of its section 1 was verified first-hand
against the executed Spec 039 record. Spec 039
has executed (freeze digest ec53a841...; freeze
PR #226 merged 05f961fc, record PR #234 merged
14d15411, completion PR #235 merged a61da697)
and its assignment artifact recomputes to the
expected SHA-256 (64f288d3...; 36 rows, 30
sites). The gate nevertheless fails, on
section 1 conditions 2 and 4. The executed
artifact assigns period labels per site -
label sets stating the periods a site's
published record spans (harappa: Early, Mature
and Late Harappan), carried identically onto
the site's rows (Spec 039 F039-C04/C06) - as
finding aids, not dating evidence (F039-C15).
It carries no mapping keyed by site x an
inscription's recorded local chronological
label, which is the only key Spec 040's
section 4 interface consumes, and local period
names appear only inside prose evidence
strings. Three of the seven G1 sites
(chanhu-daro, dholavira, nausharo) have no
artifact rows at all. Under DD-040-3 the
interface is not loosened to fit the product:
the recorded state is NOT-YET-TESTABLE -
dependency gate. No freeze followed: the AEE
lifecycle hooks were not run (the gate stands
in front of them), no freeze digest was
computed, DD-040-1/5/6/9 remain undecided (the
re-derived interval-at-margin rule is not
adopted), no execution phase number was
allocated (Phase-404 is not taken; DD-040-10
stays open), no OSF registration was filed,
and nothing was executed - no label joined, no
margin computed, no repertoire quantity
calculated. G1 stands exactly as Spec 025 and
Phase-385 left it: SUPPORTED under composition
and preservation control, governing basic CI
[0.1838, 0.2102] above the V = 0.10 floor, with
the rider that chronology is NOT controlled.
A secondary finding is recorded with the gate
record: the anchors pin carried in the Spec
040 draft (eccea6d5...) is superseded - the
anchors file recomputes to df0cf620... on
current main and at the draft's own base,
unchanged since 2026-10-12; a future freeze of
this contract must refresh that pin. Full
record: specs/040-d25-g1-chronology-controlled/
outcome.md (dependency-gate record, appended
2026-10-20).

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution sec.VI.
## 2026-10-21 — Spec 030 Ask 2 ruled BINDING (owner decision)

The one question Spec 030's 2026-10-12
adjudication expressly left open — Ask 2,
whether the CONTESTED-excluded computation must
bind a future Q6 freeze (the design stated no
recommendation; both computations were reported
under rule 5 with the as-frozen run as verdict
basis meanwhile) — is now decided. Owner
ruling (Tristen Pierson, 2026-10-21, program
chat): "Ask 2 is decided BINDING: a future Q6
freeze's timing-support assessment must meet
every frozen criterion with CONTESTED-scenario
rows excluded as well as with all rows included,
and a support claim that holds only with
contested rows included does not authorise a Q6
freeze." Recorded by dated append in
specs/030-q6-chronology-spine-extension/
adjudication.md; the 2026-10-12 record stands
untouched, as do the frozen spec, the freeze
record, and the Phase-394 records. Decision
memo: spec030-ask2-decision-memo-2026-10-21.md
(owner's research notes), which recommended
BINDING and verified the ruling changes no
standing outcome: Phase-394's two computations
were identical (C1 1 FAIL, C2 6 FAIL, C3 0.0
FAIL, C4 70 BP PASS under both), so Q6 remains
NOT-YET-TESTABLE. The both-ways reporting duty
(rule 5; F030-C04) is unchanged.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.
## 2026-10-21 — Spec 030 freeze-test amendment (owner-ordered)

The owner ordered the amendment on 2026-10-21,
verbatim: "Amend the freeze test (Spec 038
precedent)". The defect: the Spec 030 freeze
fence test_freeze_record_replays in
backend/tests/test_spec030_freeze.py replays the
freeze record with framework026 verify_freeze
over every covered source by whole-file SHA-256,
and specs/030-q6-chronology-spine-extension/
adjudication.md is a covered source — so the
dated append recording the owner's Ask 2 ruling
of 2026-10-21 (PR #241, the entry above) failed
the replay by construction: the single backend
failure (frozen source changed:
specs/030-q6-chronology-spine-extension/
adjudication.md) in an otherwise 1,366 passed /
20 skipped suite (run 39573949471; the run's
other six jobs green). No frozen byte was
altered; the frozen bytes remain an exact prefix
of the live file. The amendment narrows that
single assertion for adjudication.md to
prefix-integrity: the freeze-time bytes — 5,867
bytes, SHA-256
f962f910d81cb63f44abb4db0e1be2ee0fb9fca45f5242f23656113ddd609738
— are pinned in freeze.json (prefix_pins) and
asserted as a constant in the test, and must
remain an exact prefix of the live file; dated
appends after them are permitted. Every other
covered source keeps its live whole-file hash
assertion; no other assertion changed and no
production code changed. freeze.json was
recomputed ONCE over the amended state with the
repo's own builder
(specs/030-q6-chronology-spine-extension/
build_freeze.py, framework026) in the freeze
environment (python 3.12.3, aee 1.0.4),
faithfulness-proven first: the pre-amendment
builder over the original (pre-append,
pre-amendment) bytes reproduced the freeze-act
digest exactly. Successor digest
45ab6a1352f8e01ee7aebee88e3219a9af7d67908265172b0e321a302722c500.
The freeze-act digest
3a61c63a26ffada3c21bf8b718610e6debe7f9c9ff58bf8ff736cbb7c3db00e9
stands as the digest of the freeze act in every
record that cites it (the OSF contract
registration bge3k, osf-registration.md,
outcome.md) and was edited nowhere. Record:
adjudication.md freeze-test amendment section;
freeze.md addendum; this entry. The Ask 2
ruling stands as recorded above; Q6 remains
NOT-YET-TESTABLE.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.

## 2026-10-21 — Spec 047 step-1 execution (Phase-406: Asset B build and freeze)

Spec 047 was executed through step 1 as
Phase-406 under the frozen contract (freeze
digest 8501feab…; OSF registration b2a8w
approved and public). Step 0 gates all PASS:
input integrity (the eight §2 inputs hash
to their freeze pins, verified by two
independent routes), spine reproduction (36
rows, 30 clusters), and the join census
(5,679 records accounted for exactly once:
joined 5,106; non-spine 573 over 66 site
values; no site value 0). **Asset B froze**:
specs/047-roif-ledger-distribution/asset-b/
site-functions.jsonl, SHA-256 a1a9e484…,
30 rows — AGREED 3 (harappa administrative,
lothal port/trade, shahr i sokhta
mixed/unknown), DISAGREED 1 (surkotada),
SINGLE-SOURCE 10, NO-SOURCE 16; **testable
2**. The §4.3 verification pass demoted
khirsara and sheri khan tarakai to
SINGLE-SOURCE on independence grounds
before the freeze (recorded in full in the
outcome record). The ledger-sign list froze
in the same act: SHA-256 dfa48f50…, 8
entries from Roif's two postings of
record, 3 mapped (fish, jar, grid), 5
UNMAPPED; the DD-047-13 all-UNMAPPED case
does not fire. Step 2 was not run: no
distribution quantity exists, and the
claim stands UNTESTED. This concerns the
distribution component of Roif's ledger
thesis only; the guild-authority and
Akkadian-influence components were not
tested. Held under the Roif gate.
Outcome record:
specs/047-roif-ledger-distribution/outcome.md;
machine record: reports/phase406_results.json;
report: reports/phase406_step1_report.md.
## 2026-10-21 — Spec 046 (Phase-405) executed — IDENTIFICATION FAILED (sign unmatched)

Spec 046 ("Sign 297 Is the Horned Tiger": an
Identification Concordance, design D-18) was executed
as Phase-405 under its frozen contract (freeze-act
digest
80c3be31e5af5236f71cb2c1894b2946f9b8ad47b12bdeab9d03cd76468af405;
successor digest
e0d7add84b9d28ae5f6a6b392dca578b727ad4d99a117360a57d39f3b94b01c6
in freeze.json as merged), in Wave 3 group 1 of the
runnable-experiments campaign, before Asset A freezes.
The execution gate was satisfied before the run: OSF
registration dnts8 is approved + public.

Outcome, in the frozen wording: **IDENTIFICATION
FAILED (sign unmatched)** — "The fragment 'sign 297
is the horned tiger' cannot be carried to a
concordance: the drawn sign could not be matched from
Wells's published list. The record stays a stated gap.
No statement about the sign is made, and nothing is
fed to Asset A."

Step 0 passed in full: every spec section 2 input
pin recomputed by two independent routes and matched
(claim record bd0f7abd…, held Wells 2015 text
62acf855…, Phase-104 evaluation 2d0b83e8…, crosswalk
registry 8a0b2a82…, lane-2 drafts 3f645c9a…); the
source book produced from the held copy with the
printed-p. 97 passage located verbatim; all four
lists of record accounted for as HELD or CITABLE
(Wells HELD, CISI HELD, Parpola CITABLE, Mahadevan
CITABLE). Step 1 named the source's sign list from
the book's own apparatus — Wells's own list (Wells
2011), in Wells 2015 Chapter 2 / Figure 2.6 — and the
drawn-sign match then failed: the pinned registry
carries no entry for the drawn sign (its only W297
value sits inside the 17-value wells_ids cell on the
P205 "Prismed light rays" row, the trap the frozen
spec names in advance; P297 is the "Ladder motif", a
different sign; 0 of 803 registry descriptions name
a tiger); the Phase-123 Wells witness carries no
Wells grapheme 297; the drawn forms of Figure 2.6 did
not survive the held copy's text extraction (captions
only), so no inspectable drawn-sign reference exists
in the held record; and the Spec 004 WS2 record
(three candidate referents, none matching the
description in-repo) stands unrebutted. Matching by
number is forbidden (F046-C07) and was not used.

Step 2 was not reached: no list was scored, no
concurrence state was computed, and the hypothesis
is unjudged — neither supported nor falsified on
concurrence grounds. Delivery in the frozen closure
form: specs/046-horned-tiger-concordance/
concordance-297.json (schema glossa.concordance/1;
signs empty; closure block), SHA-256
772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf
(derived twice, identical; the run is deterministic
and reproducible byte-identically). Records:
reports/phase405_results.json,
reports/phase405_concordance_report.md,
specs/046-horned-tiger-concordance/outcome.md; graph
node IndusPhase405HornedTigerConcordance registered
and verified by import before the run; the claim's
record received its dated first-check append
(F046-C15; pre-existing content verified
byte-identical with the append removed; status and
stage unchanged). Anchors asserted byte-identical
before and after (df0cf620…). Asset A (Spec 045)
proceeds without this feed and records its absence;
the closure does not block the asset.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.

## 2026-10-21 — Spec 044 step 0 EXECUTED (Phase-404): Asset F built and frozen; execution closed TOO THIN at gate 0.4 (held under the Roif gate)

Spec 044 (design D-02, the fish-sign coastal
residue, sign by sign) executed its step 0 only,
under the runnable-experiments campaign approved
2026-10-21 (Wave 3, Group 1), as Phase-404. The
execution rule was satisfied: the frozen
contract's OSF registration 6p9et is approved
and public (freeze digest
6851f943d196fa389e48b67cb5161b90daa1180d8a3e1cf3f020fcf25691d9c8).
Graph-first build: backend/scripts/
phase404_fish_coastal_step0.py, graph node
IndusPhase404FishCoastalStep0 registered and
verified by import before the run. Gate 0.1
PASS: the CISI-based layer of record (the
Holdat corpus file, SHA-256
62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e)
re-asserted and the original family-level
test's population reproduced exactly (7,002
tokens; 1,670 inscriptions over 9 sites; M047
at 13 tokens in 13 inscriptions; Phase-45 T6
table 2 / 10 / 228 / 1,369, Fisher two-sided
p = 0.685), every figure verified by two
independent routes. Gate 0.2 PASS: Asset F,
the fish-family list, built solely from
Parpola's published list (1994, fig. 5.1,
pp. 70–78) via the pinned Mahadevan–Parpola
crosswalk and frozen at
specs/044-fish-sign-coastal-residue/
asset-f-fish-family.json — 7 members (M047,
M048, M050, M052, M060, M145, M147), digest
ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3
(SHA-256 of the canonical bytes, digest field
excluded; verified by two independent routes).
The DD-044-5 cross-check is on the record
(claim-record trio 72/64/70: no member in
Asset F; Phase-43 six: only 60) and added and
removed no member. Gate 0.3 PASS: the coastal
list frozen under the design's rule —
coastal/maritime Lothal and Dholavira (members
by name); Surkotada classed inland and listed
as contested. Gate 0.4 TOO THIN: the census
(margins only) is M047 13, M048 157, M050 17,
M052 22, M060 20, M145 3, M147 2 — one member
clears the 30-occurrence floor, fewer than the
two the frozen criterion needs, so the
execution closed as TOO THIN in the spec's
pre-written wording, with the full census as
its finding. Gate 0.5 was not reached; no
per-sign coastal test was computed and no
coastal split of any sign was counted. The
family-level verdict (partially falsified)
stands exactly as recorded, and the claim's
record was not edited. Anchors asserted
byte-identical before and after (df0cf620…).
Foundation check at the run: 40 passed /
0 failed / 8 warnings. Records:
specs/044-fish-sign-coastal-residue/outcome.md
(the step-0 outcome record and Spec 048's
pin source for Asset F's digest),
reports/phase404_results.json,
reports/phase404_step0_report.md. This entry
and those records are internal under the
campaign's Roif gate (R-7); they are not a
publication, and campaign reporting names
this member only as executed — held under
the Roif gate.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-21 — Spec 045 step 0 EXECUTED (Phase-411): INVALID at gate 0.2 (positional reproduction)

Spec 045 was executed at step 0 as Phase-411
under the frozen contract (freeze digest
5d8254dd…; OSF registration 4mt9k approved
and public), in Wave 3 Group 1 of the
runnable-experiments campaign, with step 0
running before the step-1 Asset A build as
the Group 1 executions of Specs 044 and 047
ran their step-0 gates first. Gate 0.1 PASS:
every spec §4 input recomputes to its freeze
pin, verified by two independent routes
(positional record 0e546962…, Phase-43 record
78a6c219…, corpus layer c02e3d7b…, crosswalk
4ace1a61… — 205 rows, 187 distinct sign keys,
anchors df0cf620…). **Gate 0.2 FAIL — the
execution closed INVALID in the frozen §5.5
wording.** The pinned corpus carries 3,463
inscriptions of length >= 3 against the
recorded 2,267; the 40/61/20 strong-sign
classes are exhibited by no record of record
(the Phase-43 record exhibits 10 of its 20
terminal-strong signs and no initial or
medial member list, and states no position
rule, count floor, threshold, or profiled-set
rule); and the corpus the recorded quantities
belong to — the Firestore V3 corpus (3,137
sequences), named by the Batch-5 record of
the same test — is absent from the tree (its
loader dump path does not exist on main).
No threshold was invented, no neighbouring
battery borrowed, and no corpus substituted:
the only tripartite code path in the tree is
Phase-45's iconography test, whose own rule
yields 75/22/5 on the Holdat roles, not the
recorded classes. Gates 0.3 and 0.4 were NOT
REACHED. Asset A was not built — gates A1–A6
never ran, no sign was classified, and **no
Asset A digest exists** for the D-06 / D-13
dependents to pin (stated plainly in the
outcome record for wave planning). The D-18
feed state was recorded, not consumed: Spec
046's concordance-297.json re-verified
(772db4df…, empty signs, IDENTIFICATION
FAILED closure form) — an empty feed, neither
consumed nor reconstructed. No model was
fitted, no closing score computed, and no
verdict recorded; the claim
without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001
stands IN QUESTION, partially supported for
position only, exactly as recorded. This
closure is about runnability, not about
Hunt's account or the grammar account, and
it quotes no other spec's closing measure
(DD-045-19). Anchors asserted byte-identical
before and after (df0cf620…). Records:
specs/045-hunt-depicted-kinds/outcome.md,
reports/phase411_results.json,
reports/phase411_step0_report.md.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-21 — Spec 057 EXECUTED (Phase-419): Class C — PARTIAL RECOVERY WITH UNLOCATED SOURCES (r=2, e=1, u=2)

Spec 057 was executed as Phase-419 under the
frozen contract (freeze digest 237b923a…;
OSF registration chq5e approved and public,
DOI 10.17605/OSF.IO/CHQ5E), in Wave 3 group 2
of the runnable-experiments campaign. Step 0
passed in full: gate 0.1 input integrity —
every §2 live pin recomputes to its freeze
value (five cleaned texts, five registry
files, Phase-104 2d0b83e8…, lane-2 drafts
3f645c9a…, anchors df0cf620…), verified in
the foreground by two independent routes;
the extracted-claims store was asserted by
entry facts under the freeze's Spec 038 form
(the S-4 claims file's live hash differs
from its freeze constant only by Spec 046's
first_check append to a different claim in
the same file; the …_statisti_0003 entry's
facts are unchanged — recorded on the
record, not passed over). Gate 0.2
source-set integrity: the canonical record
carries exactly the four recorded evidence
instances with fingerprint a4874349…. The
accounting, one outcome per source: S-1
SOURCE UNLOCATED, sub-state HEADING NOT
PRESENT IN HELD TEXT (its two occurrences
are a running sentence at line 102 and a
bibliography entry for S-3's paper at line
663; the full stated search ran, no document
copy exists in the repository, and the
unblocking act — re-acquisition of the
edition the extraction ran on — is named on
the row). S-2 PASSAGE EMPTY: the held
Search Inside excerpt of Fuls 2023 Chapter 3
(lines 536–615; chapter running heads at
lines 536 and 612) states the normalised
weighted position method, a worked histogram
example, and the stipulative INS/TMK
classification definitions of §3.3, and no
checkable finding — the judgement is stated
on the record with the byte-exact passage
artifact (25a0a558…) as its evidence. S-3
CLAIM RECOVERED: Fuls 2013's paper, its own
title as heading, findings-bearing body
lines 54–601 (artifact 88f29146…); its §7
Summary states the positional classification
finding (signs classifiable as Initial,
Early-Medial, Mid-Medial, Late-Medial,
Terminal, constant, or constant-but-not;
doubling/mirroring/hatching/marking can
change a sign's class; signs 382, 790, 832,
892 are good syllable candidates) on the
ICIT corpus as stated (3723 complete texts,
13556 signs, reduced 2474 texts / 9700
signs, mean length 4.01) — recovered as
fuls2013_positional_analysis_057_recovered_0001
at the created stage, unchecked, intake
record intake-S3.json. S-4 CLAIM RECOVERED:
Wells 2015 Appendix II, heading at line
3456, passage lines 3455–3822 (artifact
af28153c…); its Summary states the same
classification finding in the appendix's own
terms (classification list Initial through
Terminal; modified signs; the same four
syllable candidates; the same corpus
numbers as stated) — recovered as
wells2015_appendix_ii_positional_analysis_057_recovered_0001
at the created stage, unchecked, intake
record intake-S4.json. S-5 SOURCE UNLOCATED,
sub-state HEADING NOT PRESENT IN HELD TEXT
(its single occurrence at line 267 is
sentence-initial inside a running paragraph;
stated search and unblocking act as S-1).
Headline class C in the frozen §7.1 wording,
counts (2, 1, 2) shown beside it. Disposition
(§7.2, r ≥ 1): the heading record is
superseded by the two recovered claims,
by appended dated disposition note only —
no pre-existing field altered (removing the
append reproduces the pre-act file
byte-identically), status and stage
unchanged. Hypothesis F057-C14 borne out.
No claim was checked, no positional finding
is established by this act, and the passage
artifacts are internal records under
license_status "unclear". This act recovered
what five passages state. It checked none of
it. Anchors asserted byte-identical before
and after (df0cf620…). Records:
specs/057-five-sources-heading/outcome.md,
specs/057-five-sources-heading/passages/,
specs/057-five-sources-heading/intake-S3.json,
specs/057-five-sources-heading/intake-S4.json,
reports/phase419_results.json,
reports/phase419_five_sources_report.md.
## 2026-10-21 — Spec 058 EXECUTED (Phase-420): LOCALISED TO SIGNS

Spec 058 was executed as Phase-420 under the
frozen contract (freeze digest 8bdd4764…; OSF
registration 86dgh approved and public, DOI
10.17605/OSF.IO/86DGH), in Wave 3 Group 2 of the
runnable-experiments campaign — design D-21 arm A
only; arm B stays blocked and no AI substitution
for human coders was designed or run (F058-C06).
Step 0 passed in full, in frozen order: gate 0.1
every spec §2.1 input recomputes to its freeze
pin (verified in the foreground by two
independent routes — git blob and GitHub contents
API — at the run's base 3200b7b5); gate 0.2 the
Phase-132 pilot-pass record set produced at the
execution venue (the main-checkout machine's
gitignored store, read-only; the main checkout
was never modified) at the pilot report's §9
inventory — frame.json, 50 Pass A, 50 Pass B, 10
gold, 50 adjudication records, effort log 320
events — with a per-file SHA-256 manifest of the
162-file set recorded in the results JSON; gate
0.3 frame identity exact; gate 0.4 the pinned
phase132_metrics.py, imported unchanged,
reproduces the committed metrics file in full
(0.20 P and M; 0.4798; 0.4286; estimator 0.05;
totals 191/190/40/189; every per-object flag);
gate 0.5 taxonomy exact (identity 93, legibility
45, count 11, key 10, orientation 2, order 1;
total 162); gate 0.6 census 40 mismatched
objects. Tabulations over the frozen alignment:
E = 103 mismatch events (88 SUBSTITUTION, 15
INDEL); summed involvement 191. **LOCALISED TO
SIGNS (the frozen §5.2 wording): the 10
most-involved signs account for 54.5% (104/191)
of all mismatch involvement — UNK, P310, P144,
UNMAPPED:M817, P145, P245, P119, P184, P268,
P324 — with the mandatory UNK sentence carried:
UNK itself is the most-involved value (53/191,
27.7% of involvement), so the localisation is in
part a localisation to illegibility.** The
object-type locus did not fire: Seals carry
77.7% (80/103) of events but a 9.7-point
enrichment over their 68.0% frame share, below
the frozen 10-point margin (DD-058-8). The
segmentation locus did not fire: INDEL share
14.6% (the registered proxy, spec §8(4)).
First divergence falls at alignment position 1
in 21 of 40 objects, with UNK the most-involved
value there too (26). The descriptive
UNK-excluded secondary (no headline): E = 50,
top-10 share 41.5% (BETWEEN — the concentration
does not survive setting illegibility aside,
reported as found); the M-space sensitivity
agrees descriptively (top-10 53.9%). The claim
STUDY-SPEC-023/PHASE-132+383 stands CONTRADICTED
exactly as recorded; this entry and the outcome
record are its dated mechanism-account append —
the lane-2 drafts file is a frozen pin and was
not edited. Anchors asserted byte-identical
before and after (df0cf620…). Foundation check
at the run: 40 passed / 0 failed / 8 warnings.
Records:
specs/058-transcription-disagreement-mechanism/outcome.md,
reports/phase420_results.json (3d140333…),
reports/phase420_report.md (b8634d76…).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.
## 2026-10-21 — Spec 055 (Phase-414) executed — NOT NUMERAL-LIKE

Spec 055 ("Sign 900 Means Six": identify the sign, then
test it as a numeral; design D-15) was executed as
Phase-414 under its frozen contract (freeze digest
42ef82829ade894918b0bf946ac44354224d689202e2f7bf00eb747821bdedfc),
in Wave 3 group 2 of the runnable-experiments campaign.
The execution gate was satisfied before the run: OSF
registration tbyqg is approved + public.

Step 0 passed in full: every spec section 2 input pin
recomputed by two independent routes at the run's base
(3200b7b5) and matched (claim record e9819089…, held
cleaned text 1275b795…, literature record 92e19e6d…,
Phase-104 evaluation 2d0b83e8…, crosswalk registry
8a0b2a82…, lane-2 drafts 3f645c9a…, anchors df0cf620…);
the source produced from the held copy with the
sign-900 material located verbatim (Table 1's numeric
grid did not survive the held copy's extraction —
caption and prose recovered, nothing reconstructed);
the recovery record written before any verdict
wording.

Stage 1 — IDENTIFIED. The source's sign list is named
from the document's own text (four verbatim naming
statements, printed pp. 57, 59, 85, 88): the extended
Wells (2011, 2015) sign list of 702 distinct signs.
The drawn sign was matched by drawn form only: the
named list's sign 900 is the single-arc grapheme (the
verified Phase-123 Wells segmentation witness, row
M287, from Wells's PhD 2006 Figure 3.2 plates), and
exactly one registry row is a plain right parenthesis
with no added element — P154 ("Right parenthesis
(perhaps with a backward curve at the bottom)"),
whose Mahadevan crosswalk is M287. The registry's
W900 cell on that row is recorded as the frozen trap
(F055-C07) and was not used as the identification.
The recovery is preserved in the section 6 form:
specs/055-sign900-numeral/source-table-recovery.json
(schema glossa.source-table-recovery/1), SHA-256
439f1449b8d7707d1feb88ef34e2edf90d3d192ba5c6f30bfa29cdf34b48852d.
The sign-700 statements are located by locator only
(printed p. 70; pp. 72–74) and adjudicated in no way:
Design D-16 does not join this campaign even though
this recovery is the act that would unblock it; D-16
waits for its own planning gate (campaign decision
E-7).

Gate 0.4 passed: the strict-corpus layer (the
Mahadevan-lineage corpus as held — the indusscript-m77
records of the tracked primary corpus, the executed
Spec 033 precedent for this layer) was exported in
full and pinned (specs/055-sign900-numeral/
strict-corpus-export.jsonl, SHA-256
1e421af1b75f09f49c928ef7eaa86e4c9a382e059d4771f164256a069896e02c;
2,906 records, 11,507 tokens); the identified sign,
Mahadevan 287, stands at 79 occurrences, above the
frozen floor of 5.

Stage 2 outcome, in the frozen wording: "The sign
that Fuls's paper numbers 900, identified in Spec
055's recovery record as P154, does not behave as a
numeral sign behaves in the pinned strict corpus: on
3 of the three frozen measures it sits inside the
range of frequency-matched ordinary signs. The
numeral reading the fragment carries is contradicted
at the behaviour stage. The identification itself
stands as recovered; what fails is the behaviour the
reading predicts." The known-numeral set was fixed
before counting from the source's published
stroke-sign identification (29 Mahadevan identifiers;
the target excluded; Signs 415 and 70 hedged and
excluded under DD-055-14); the control set by the
frozen nearest-10 rule; a dry-run on Mahadevan 342
preceded the target (DD-055-16). Measures for the
target: short-text share 0.164557, numeral adjacency
share 0.455696, positional entropy 2.708415 bits —
numeral-side 1, control-side 3, NOT NUMERAL-LIKE by
the section 5.3 mapping alone. The claim hypothesis
(F055-C03) is falsified at the behaviour stage. No
outcome of this spec establishes the value six: the
source's own argument for six is preserved in the
recovery record as source material and was evidence
at no stage. Records: reports/phase414_results.json
(SHA-256 173a67a1d22651b1da03da0c40457e7234298fc6686dc22f3c2b6a25a2a5a6d5),
reports/phase414_sign900_report.md, graph node
IndusPhase414Sign900Numeral (registration verified by
import), the appended first_check entry on the
claim's record, and specs/055-sign900-numeral/
outcome.md. Anchors asserted byte-identical before
and after (df0cf620… at both points).

## 2026-10-21 — Spec 059 EXECUTED (Phase-421): CLOSED AT STEP 0 — JOIN GATE NOT MET

Spec 059 (design D-22, the seal/tablet
difference on a better join) was executed as
Phase-421 under the frozen contract (freeze
digest bba1caca…; OSF registration yfw7h
approved and public, DOI
10.17605/OSF.IO/YFW7H), in Wave 3 group 2 of
the runnable-experiments campaign. Graph-first
build: backend/scripts/phase421_f1_object_join.py,
graph node IndusPhase421F1ObjectJoin registered
and verified by import before the run. Gate 0.1
PASS: every spec section 2 pin and every
DD-059-9 object-identifier source pin
recomputes to its freeze-record value, verified
in the foreground by two independent routes
(committed pins: Phase-136 results 11a07413…,
Stage 2(a) freeze c65a4b9b…, Phase-136 builder
d5ceec46…, Phase-141 report d442f8d2…, combined
report 6a4f5d26…, registry 8a0b2a82…, Spec 034
outcome c0cc615d…, Spec 037 outcome 28e444f2…,
anchors df0cf620…, intake schema b94d03ad…,
Phase-398 builder 278f16b0…, intake validator
02b24e33…; local-store pins: horus84 layer
c368f290…, CISI vols 1–2 e0d698f9… /
e751244e…, ICIT converted keyed layer v2
bbfdbcd5…). Gate 0.2 PASS: the original
concordance join reproduced exactly (5,679
layer rows; 2,895 matched; 2 ambiguous; 2,782
unmatched). Gate 0.3 PASS: the object-ID join
dataset built by the pinned route-(b)
construction (5,018 records carrying
provenance.object_id) validated under the
pinned Phase-130 schema — verdict pass,
0 errors, 0 warnings — and censused against
the catalogue's 3,493 distinct objects:
**2,899 joined rows; 2,780 unjoined (661
carrying no identifier, 2,119 whose
identifier resolves to zero catalogue
objects); 0 ambiguous; 2,479 distinct
catalogue objects joined to.** The census was
derived twice (intake-dataset route and
lineage-direct route) with every row's joined
classification in agreement; five raw-value
discrepancies between the lineage layer and
its converted form are recorded per row in
the census and change no classification.
Gate 0.4 FAIL: 2,899 joined rows = 51.0477%
against the bar adopted at DD-059-7 (joined
share at least 61.0%, at least 3,465 of 5,679
rows) — a shortfall of 566 rows. The
object-ID join adds exactly 4 rows over the
original join (the two H-311 rows and the
trailing-space references L-78 and M-929) and
loses none. The execution therefore closed
**CLOSED AT STEP 0 — JOIN GATE NOT MET** in
the frozen section 3.5 wording, with the
census published as the finding. No F1
quantity was computed — no terminal mapping,
no CMH statistic, no p-value, no odds ratio —
and STUDY-SPEC-024/F1 stands exactly as
recorded: SUPPORTED on its original joined
subset, its "on the joined subset" scope
unchanged. The closure establishes nothing
about the claim; it is a measured property of
the available catalogue data. Anchors asserted
byte-identical before and after (df0cf620…).
Records: specs/059-f1-object-join/outcome.md,
reports/phase421_results.json (SHA-256
3948cd01…), reports/phase421_join_census.json
(95282931…), reports/phase421_report.md
(167584e1…); the script is deterministic
(byte-identical rerun).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.

## 2026-10-21 — Spec 043 (Phase-410) EXECUTED: PRED-2026-012 closed PROVENANCE — CANNOT BE RUN AS WRITTEN at step 0, check 0.3 (unscored)

Phase-410 executed the frozen Spec 043 contract
(freeze digest 8a8a334f…; OSF registration
vmcra approved and public) in Wave 3 Group 2
of the runnable-experiments campaign, under
the campaign approval's execution
authorization (adjudication.md §7.6), with
the step-0 provenance adjudication running
first, before any Phase 5 lookup, as the
frozen order requires. Check 0.1 PASS: all
seven frozen sources hashed to their pins,
re-derived by two independent routes. Check
0.2 PASS: the registry enumeration over 803
rows reproduced the draft census exactly
(791 uncoded, 12 coded; ITM = P056, P324,
P378, P385), the re-derivation of all 803
icit_function values from the pinned builder
rule agreed exactly (zero mismatches), the
held records verified (P098 carries no
code), and the cross-check read in full (611
records: 579 empty, 32 free-text glosses, no
ITM, no LOG) with every disagreement recorded
sign-by-sign, all of the expected kind.
**Check 0.3 — the provenance gate — FAIL on
all three limbs; the study closed
PROVENANCE — CANNOT BE RUN AS WRITTEN,
unscored.** The evidence set was produced in
full: D1 the pinned builder ("from ICIT docs
+ Fuls 2013"; W740 glossed "Initial Cluster
Terminal Marker"), D2 the pinned parser with
its test (function "(from Wells)" read off
the same catalog line as a positional class),
D3 Fuls 2013 "Positional Analysis of Indus
Signs" (held cleaned text, 9ed24098…,
two-route), and D4 Wells 2015 "The
Archaeology and Epigraphy of Indus Writing"
(held cleaned text, 62acf855…, two-route).
Class definition: positional — Wells
classifies signs "according to their
preferred text position" (Fuls 2013 §2), the
ICTM class is named "since they mark the end
of initial clusters" (§3.7), and Wells 2015
(ch. 3) defines it by the same cluster-final
role. Per-sign basis: every stated basis is
positional (W740 terminal distribution; W820,
W817, W861 initial distribution), and W231
(P056) has no stated basis at all — silence,
which the frozen standard (DD-043-10) fixes
as failure. Source agreement: Wells' published
ICTM class is exactly signs 060, 001, 002
(Wells 2015, ch. 3) — none a builder ITM key;
817/820/861 are published as initial signs,
820 also as a terminal marker, and W231 is
omitted where the table asserts ITM. The LOG
trace is recorded in the same form and gates
nothing (DD-043-12): sign 520 is "the other
common TM" in Wells 2015, not LOG, and no
per-sign LOG basis is stated for sign 700.
Check 0.4 never ran: the Phase 5 output was
byte-hashed at 0.1 and never opened, the
sanity anchor was never reproduced, and **no
Phase 5 assignment was looked up for any
sign**. No share, coverage figure, or verdict
exists. PRED-2026-012 remains unscored, its
§3 Outcome standing PENDING; PRED-2026-007's
PARTIALLY CONFIRMED stands untouched. The
closure is recorded in the register by dated
§6 append only (insertions-only
prefix-verified; the Phase D pin advanced by
name a ninth time), and it records what the
classification's assignments rest on — it is
not a verdict on the criterion and not a
refutation. Records:
specs/043-pred-2026-007-registry-frame/outcome.md,
reports/phase410_results.json (step-0 record
sha256 019c65991835505c7f8ecac11e3b62f5b01b1
fe825bed3c46eb23fdb2879c948),
reports/phase410_step0_report.md.

## 2026-10-21 — Spec 053 EXECUTED (Phase-413): STRICT CORPUS NOT PINNABLE at gate 0.3

Spec 053 was executed as Phase-413 under the
frozen contract (freeze digest fd2d5cb8…; OSF
registration s9yfe approved and public), in
Wave 3 Group 2 of the runnable-experiments
campaign (design D-07, arm A only; arm B
trigger-armed and not joined, campaign E-3),
under the graph-first build (script
backend/scripts/phase413_yadav_zipf_controls.py;
node IndusPhase413YadavZipfControls; registration
verified by import before the run). Gate 0.1
PASS: every spec §2 pin recomputes to its freeze
value, verified by two independent routes (claim
file 90476623…, anchors df0cf620… — 287 anchors,
94 strict_sa_independent — crosswalk 4ace1a61…,
Mahadevan–Parpola crosswalk 9ebd7723…, Phase-43
record 78a6c219…, re-read in the same pass: no
Zipf fit, exactly as DD-053-11 recorded; no
Phase-43 estimator was sought or substituted).
Gate 0.2 PASS: the §4.2 estimator the freeze
specified completely recovered the planted
parameters — fitted α 1.256 (error 0.056,
tolerance 0.10) and q 2.72 (error 0.72,
tolerance 1.0) from α 1.20 / q 2.0, V 200,
N 50,000, seed 20261021. **Gate 0.3 FAIL — the
execution closed STRICT CORPUS NOT PINNABLE in
the frozen §6 wording.** The V3 /
Mahadevan-lineage layer's only loader of record
reads the Firestore 'indusarrays' dump at
glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl,
which is absent from the tree (the sources/
subtree is untracked) and from the programme's
main checkout; the loader loads zero sequences,
so the layer cannot be exported or pinned. No
database copy exists in the execution tree, and
the main-checkout database (inspected read-only)
holds nine texts and no V3 Indus corpus. No
other layer in the tree is the corpus the
Phase-43 record names (Firestore source, 3,916
records / 3,137 sequences / 2,665 dockeys /
12,494 instances): the site-attributed layer
carries 5,679 records, the V1 export 15,508
mixed-source objects, the ICIT export 3,085
ICIT-encoded sequences, and the Holdat path is
absent and a different compilation besides. No
layer was substituted and no rule invented.
Gates 0.4 and 0.5 were NOT REACHED: no control
count was entered (no judgement on the control
set is recorded or implied), no census exists,
no system was fitted, the §4.4 condition was
never evaluated, and no sensitivity was
computed. The claim yadav_2009_arxiv_manual_001
stands exactly as recorded (strongly supported;
recorded exponent about 1.35); no strength
label was appended and its record was not
edited. Anchors asserted byte-identical before
and after (df0cf620…). Foundation check at the
run: 40 passed / 0 failed / 8 warnings. Records:
specs/053-yadav-zipf-controls/outcome.md,
reports/phase413_results.json,
reports/phase413_step0_report.md.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-21 — Spec 042 EXECUTED (Phase-407): THIN at gate 0.4 — the tablet stratum is too thin

Spec 042 (design D-28, the object-type split of
Spec 028's Arm B) executed in full under the
runnable-experiments campaign approved
2026-10-21 (Wave 3; campaign member 19), as
Phase-407. The execution gate was satisfied:
the frozen contract's OSF registration tmyzg
is approved and public (freeze digest
6be2988d7f4c290591d36f391ac84a772f18a9121e35ddd0e251956b5260f753).
Graph-first build: backend/scripts/
phase407_arm_b_object_type_split.py, graph node
IndusPhase407ArmBObjectTypeSplit registered and
verified by import before the run. Every spec
section 2 pin was re-derived in the foreground
by two independent routes (working-tree
sha256sum; git-blob hashlib at the base commit
3200b7b5) and agreed with the freeze record on
all six inputs. Gate 0.1 PASS: every section 2
input hashes to its freeze-record value.
Gate 0.2 PASS: the frozen population flow,
re-run on the Phase-393 machinery inputs
(supplied from the program's existing local
downloads and hash-verified, bbfdbcd5… /
c368f290…), reproduces the recorded counts
exactly (5,679 / 4,531 / 4,505 / 3,605 /
3,144 / 3,030), the recorded flow dict of both
the Phase-393 results and the Spec 028 margins
audit, the recorded Arm B analysis set, its
site x type cell table (identical to the
margins audit's, cell for cell), and the 125
sign columns. Gate 0.3 PASS: the partition
census — SEAL 1,768 + TAB 1,262 = 3,030, no
record of any other type (per site: Chanhu-daro
52/2, Dholavira 96/15, Harappa 361/1,076,
Kalibangan 49/3, Lothal 72/2, Mohenjo-daro
1,138/164). **Gate 0.4 fired THIN: the seal
stratum clears the floor at all 6 sites
(minimum Kalibangan, 49), but the tablet
stratum carries at least 20 inscriptions at
only 2 of the 6 sites and is recorded TOO
THIN with its counts; under DD-042-2 the
execution closed at that gate with headline
THIN, in the spec's pre-written section 4.3
wording.** Neither stratum was computed,
gate 0.5 (the pooled regression) was not
reached, and no verdict is recorded: the
section 1.2 hypothesis is unjudged, object
type is not exonerated, and Spec 028's Arm B
INCONCLUSIVE verdict stands exactly as
recorded, unedited. Per-stratum period and
preservation mixes are published with the
record (described, not controlled; Spec
037's 49% compilation-relativity caution
restated). Anchors asserted byte-identical
before and after (df0cf620…). Records:
specs/042-arm-b-object-type-split/outcome.md,
reports/phase407_results.json (SHA-256
6f0f5a4f37918d7acb2e899b916131d133d13fc6cecd3b2f4b03662d96919d72),
reports/phase407_report.md (SHA-256
67f0cc005508e52e304bff03c277834558abc06c25d299e587b2bb4898a6c37e)
— both digests verified by two independent
routes, and the script deterministic
(byte-identical on a second run).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-21 — Spec 056 (Phase-418) executed — IDENTIFICATION FAILED

Spec 056 (design D-17, the sign-821 fragment
recovery) was executed as Phase-418 under the
frozen contract (freeze digest 64c28ce1…;
OSF registration 3eygs approved and public,
DOI 10.17605/OSF.IO/3EYGS), in Wave 3 Group 2
of the runnable-experiments campaign.
Graph-first build: backend/scripts/
phase418_sign821_recovery.py, graph node
IndusPhase418Sign821Recovery registered and
verified by import before the run. Step 0
passed in full: every §2 pin recomputed by
two independent routes at base 3200b7b5 (held
text 62acf855…, Phase-104 evaluation
2d0b83e8…, lane-2 drafts 3f645c9a…, registry
8a0b2a82…, anchors df0cf620…); the claim
record asserted in the freeze's Spec 038 form
(constant bd0f7abd… in freeze.json plus the
fragment's facts on the live file — the live
file's only delta from the pinned bytes is
Spec 046's first_check append on the _0002
claim); the passage of record (Wells 2015,
"The Dholavira signboard, revisited", lines
2783–2871) produced from the held copy with
both anchor lines and the anchor sentence
located verbatim, and its slice recomputed to
the freeze-pinned digest (5,354 bytes,
51d6fb3a…). The DD-056-16 dry-run was worked
on the "Mohenjo-daro bangle pot" section
before the protocol touched the fragment.
Two independent extraction passes over the
pinned passage found the same candidate set
{K-1…K-4} and agreed on every checklist line
at reconciliation. The decisive candidate
K-1 — sign 821, in the Dholavira signboard
contexts, has a meaning of "city", either as
a determinative or as a word (printed p. 92),
with eyil the passage's preferred gloss among
DED 752 ūr, DED 808 eyil, DED 3568 nakar and
DED 4112 pāri — passes the argument
conditions R-1, R-2, R-4 and R-5 (its R-4
condition respects the passage's own ruling
that the non-attestation of eyil-ay/eyil-i is
not a nullification). The sign list is named
from the document itself: Wells's own list
(Wells 2011), in Wells 2015 Chapter 2 /
Figure 2.6. But the drawn sign is identified
by neither route R-3 allows: the pinned
registry carries no W821 value in any of its
803 rows (sole or multi-value), no registry
description names a city, and the Phase-123
Wells witness carries no grapheme 821; and
the source list's own entry stands in Figure
2.6, whose drawn forms did not survive the
held copy's text extraction (captions only),
so no entry can be quoted. The registry's
Yunmapped_0821 row is a Yajnadevam glyph
identifier — the frozen number-collision
trap — asserted as a trap and not used.
Under §6's mapping the run therefore closes
as IDENTIFICATION FAILED: the fragment is
neither recovered nor retired, and the
hypothesis is unjudged at the identification
condition — the passage does argue something
specific, so the retirement wording cannot
fire, and no claim enters the lifecycle. The
unblocking act is named on the record: the
preservation, as a committed and hashed
record, of an inspectable drawn-form
reference for Wells's sign 821. Records:
specs/056-sign821-recovery/outcome.md,
specs/056-sign821-recovery/extraction-record.md,
reports/phase418_results.json,
reports/phase418_recovery_report.md; the
claim's record received its dated closure
append (spec056_closure; removal reproduces
the pre-act file byte-identically; status and
stage unchanged). Anchors asserted
byte-identical before and after (df0cf620…).
This act is record repair: it establishes, at
most, what the source passage argues — never
whether the argument is right, and nothing
about sign 821 itself.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.

## 2026-10-21 — Spec 061 EXECUTED (Phase-423): CANNOT BE RUN AS WRITTEN at gate 0.5 (construction calibration)

Spec 061 was executed as Phase-423 under the
frozen contract (freeze digest 41b1785c…;
OSF registration fza8c approved and public,
DOI 10.17605/OSF.IO/FZA8C), in Wave 3
Group 2 of the runnable-experiments campaign
(member 18, design D-27 arm A1 only; Arm A2
is not in this pass, E-3). Graph-first build
(H15/H23): script
backend/scripts/phase423_arm_a_precision.py,
graph module
backend/glossa_lab/experiment_graph_phase423.py
(node IndusPhase423ArmAPrecision), registration
verified by import before the run. The run of
record executed on the owner's desktop
(TRISTEN-DESKTOP) in the freeze environment
(Python 3.12.3, NumPy 2.5.3), the executed
script byte-identical to the committed script.
Step 0, gates in frozen order: **0.1 PASS**
(every composite-pin component recomputes to
its freeze value: results 0a1657a8…, corpus
c02e3d7b…, pipeline 6c2ff91c…, margins
15ae0281…, Spec 028 freeze 376cd8e7…, anchors
df0cf620…). **0.2 PASS** (the frozen
population flow reproduces the recorded Arm A
population exactly: 1,593 records, the five
site totals, the audit's cell table, 6
included cells, 294 per draw). **0.3 PASS,
exact** (the frozen Arm A primary re-run at
seed 20261012 reproduces the recorded summary
digit-for-digit: median adjusted R²
0.00878393455594817, interval
[0.004626892186724407, 0.01297407559730989],
rejection share 0.6231155778894473). **0.4
PASS** (the freeze record states the full
§4.7 frame). **0.5 FAIL — the execution
closed CANNOT BE RUN AS WRITTEN.** The frozen
calibration's A(b) — the frozen estimator on
the constructed population in expectation —
recomputes to a step function: A(1) =
−0.0025188916876574316 (the frozen record's
own value, 1 − 1592/1588) and A(b) = 1.0
exactly at every b > 1 evaluated (1.5, 2.0,
3.0; between-site sum of squares equal to the
total at each). The mechanism: every
inscription at a site carries the same
expected proportion vector, so the
constructed population has zero within-site
variation and the estimator sees perfect site
separation at any boost above 1. No boost in
[1, 3] achieves |A(b) − θ| ≤ 1e-6 for either
scenario (θ₁ = 0.00878393455594817,
θ₂ = 0.015); Scenario 1's bisection did not
reach the tolerance within 100 iterations and
the gate closed the run there. Spec 028's
recorded positive control at boost 3.0
(median 0.023963353007570576) is a median over
generated worlds — a different quantity from
A(3), which recomputes to 1.0; the drawing of
inscriptions is what creates the within-site
variation the in-expectation construction
averages away. No trial ran, no world was
built, no target quantity was computed, and
no substitute construction was supplied at
run time. Spec 028 Arm A stands exactly as
recorded (INCONCLUSIVE); the operative
target T* (DD-061-5) is undefined on this
record, so Arm A2's trigger does not fire on
it and no target may be quoted from this
record. A successor calibration is a new act
under a new freeze or an amendment. Records:
specs/061-arm-a-precision/outcome.md,
reports/phase423_results.json (SHA-256
f7007009…), reports/phase423_report.md
(SHA-256 3669eb38…). Anchors byte-identical
before and after (df0cf620…).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.


## 2026-10-21 — Spec 047 step-2 EXECUTED (Phase-406): INCONCLUSIVE — classification gate (§6.3); held under the Roif gate

Spec 047's step 2 (the builder's own test,
design D-09) was executed as Phase-406 under
the frozen contract (freeze digest
8501feab…; OSF registration b2a8w approved
and public), in Wave 3 Group 3 of the
runnable-experiments campaign, against
Asset B as pinned in the step-1 outcome
record. Graph-first build (H15/H23): script
backend/scripts/phase406_roif_ledger_step2.py;
graph node IndusPhase406RoifLedgerStep2
added to backend/glossa_lab/
experiment_graph_phase406.py (the step-1 node
unchanged beside it), registration verified
by import before the run. Step 0 re-run
passed in full, in the frozen order: input
integrity (every §2 pin recomputed, by two
independent routes in the foreground and
again by the phase machinery), spine
reproduction (36 rows, 30 clusters), and
the join census accounting for all 5,679
primary-layer records exactly once (joined
5,106; non-spine 573 over 66 site values;
no site value 0) — identical to the step-1
census in every figure. Asset B was
re-asserted at its step-1 digest
(a1a9e484…; 30 rows; AGREED 3, DISAGREED 1,
SINGLE-SOURCE 10, NO-SOURCE 16; testable 2)
and the ledger-sign list at its digest
(dfa48f50…; 8 entered, 3 mapped, 5
UNMAPPED; the DD-047-13 all-UNMAPPED case
does not fire). **The §6.3 classification
gate fired on both of its clauses**: 2
testable sites (harappa — administrative;
lothal — port/trade) is below the frozen
floor of 12, and in the test population
(harappa 2,717 joined records; lothal 208;
NO-CORPUS-COVERAGE none) the pooled
ADMIN-TRADE-GATEWAY side carries both sites
while the domestic/ritual contrast side is
empty. The execution therefore closed
INCONCLUSIVE — the classification is the
finding, in the spec's pre-written §7
wording. No distribution quantity was
computed (no R, no permutation p-value, no
R_ledger, no per-sign counts); E6 (the
primaries and the each-source-alone /
five-largest recomputations) was not run,
and the §6.4 exclusions were republished in
full. The claim
indus_valley_script_deciphered_from_myth_65ff0a26_manual_001
received its dated, component-scoped
step-2 append (key spec047_step2; removal
reproduces the pre-act record file
byte-identically, verified at the act;
claim_status untested and stage created
unchanged) — the claim stands UNTESTED for
its distribution component, now with the
reason measured rather than asserted. The
standing step-1 disclosures were carried
unchanged and not relitigated (the §4.5
attestation disclosure; the §4.3
verification-pass demotions of khirsara and
sheri khan tarakai; the quoted-source basis
of the surkotada DISAGREED row). This
concerns the distribution component of
Roif's ledger thesis only; the
guild-authority and Akkadian-influence
components were not tested. Records:
specs/047-roif-ledger-distribution/outcome.md
(step-2 record appended; the step-1 text
unedited), reports/phase406_step2_results.json
(SHA-256 7d0a303f…), reports/
phase406_step2_report.md (SHA-256
87b6e0a0…) — the script deterministic, both
outputs byte-identical on a second run.
Anchors asserted byte-identical before and
after (df0cf620…). Held under the Roif
gate.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.

## 2026-10-21 — Spec 050 EXECUTED (Phase-416): CLOSED AT STEP 0 — ASSET NOT FROZEN (dependency closure)

Spec 050 was executed as Phase-416 under the
frozen contract (freeze digest fdcbae64…;
OSF registration uwdmy approved and public,
DOI 10.17605/OSF.IO/UWDMY), in Wave 3 Group 3
of the runnable-experiments campaign (member
10, design D-13; consumer of Asset A). Step 0
ran in the frozen order, fail-closed, and
closed at its first gate. **Gate 0.1 FAIL, in
its absent branch — CLOSED AT STEP 0 — ASSET
NOT FROZEN.** The gate reads Asset A's SHA-256
from the fixed pin source, Spec 045's
asset-a/asset-a-freeze.json (DD-050-11), and
asserts it before any join or counting; that
file does not exist, and neither does the
canonical depicted-kind-classification.csv, so
no Asset A digest exists to assert. The
absence was verified first-hand at the
execution base (main at 3e75d7b0…) by two
independent routes — the fresh clone's tree
(listing, existence tests, and the full
recursive ls-tree at the base commit) and the
GitHub API (contents API 404 for the asset-a
directory and the freeze file; the recursive
git-trees read at the same commit, 6,124
entries, not truncated, with no asset-a path
anywhere) — and the two routes agree. The
dependency's terminal record is Spec 045's:
executed as Phase-411, INVALID at its step-0
gate 0.2 (PR #268, merged c97c8d4c…; landing
record PR #269), its outcome record stating
plainly that Asset A was not built — build
gates A1–A6 never ran, no asset-a directory,
CSV, or freeze file exists, and no Asset A
digest exists for any dependent to pin. Gates
0.2–0.6 of Spec 050 were NOT REACHED. No join
was made, no sign was classified, no census
was taken, and no final-position quantity was
computed; no substitute asset, digest, or
stand-in file was created, and Asset A was
not reconstructed from any material. The
standing consequence: the D-13 comparison was
never run and its hypothesis is unjudged. The
claim
without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004
stands UNTESTED as recorded — this is a
dependency closure under the campaign's
cluster rule, not a verdict on the claim, and
position is not meaning. Anchors asserted
byte-identical before and after (df0cf620…).
Records: specs/050-hunt-sky-signs-endings/outcome.md.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.
## 2026-10-21 — Spec 051 EXECUTED (Phase-409): INCONCLUSIVE at gate 0.6 — the classification is the finding

Spec 051 was executed as Phase-409 under the
frozen contract (freeze digest 818cfa4e…;
OSF registration xnrph approved and public),
in Wave 3 Group 3 of the runnable-experiments
campaign (member 9, design D-10). Graph-first
build (H15/H23): script
backend/scripts/phase409_roif_arrow_sign.py,
graph module
backend/glossa_lab/experiment_graph_phase409.py
(node IndusPhase409RoifArrowSign), registration
verified by import before the run (497
registered nodes). Step 0, gates in frozen
order: **0.1 PASS** (every §2 hash pin
recomputes to its freeze value — Phase-104
evaluation 2d0b83e8…, Holdat roles 3f1c24ed…,
gazetteer 5ac76a30…, defect file fc05e552…,
Spec 047 frozen spec 1a18dac0…, anchors
df0cf620…; the claim file asserted in the
Spec 038 form, its manual_003 facts matching
on the live file). **0.2 PASS** (Asset B,
consumed from Spec 047's step 1, recomputes
to a1a9e484… — identical to the digest
recorded in Spec 047's step-1 outcome record,
the pin source fixed by DD-051-14; the digest's
presence in that record verified
mechanically). **0.3 PASS** (exactly 30 rows,
one per gazetteer cluster, the seven contract
fields, contract vocabularies; per-status
counts AGREED 3, DISAGREED 1, SINGLE-SOURCE
10, NO-SOURCE 16; testable set derived by
rule: 2 — harappa, administrative; lothal,
port/trade). **0.4 PASS** (the Holdat counting
layer of record identified from the
database-held downloads tree — the Holdat
corpus file the Phase-45/46/54 scripts of
record read — exported in full as held and
pinned at 62d14d2b…: 7,002 sign-token rows,
1,670 inscriptions over 9 sites; the
re-derived M391 census reproduces the §1
census exactly: 75 / 52 / 16 / 14 / 11 / 10 /
10 / 3 / 2, total 193). **0.5 PASS** (every
one of the 7,002 records accounted for
exactly once: joined 6,117 to a spine cluster
over 1,453 inscriptions; non-spine 885 over
217 inscriptions — Dholavira 439 records /
16 M391, Chanhu-daro 310 / 10, Rakhigarhi
136 / 2; no site value 0). **0.6 — THE
FLOORS FIRE; the execution closes as
INCONCLUSIVE — THE CLASSIFICATION IS THE
FINDING.** Testable gateway/border sites
carrying M391: 0, against the floor of 3;
the pooled side is non-empty (2 sites) and
the contrast side {domestic, ritual} is
empty in the test population. No share,
ratio, permutation, or regression quantity
was computed, and the §5 primary (task E5)
did not run. The claim
indus_valley_script_deciphered_from_myth_65ff0a26_manual_003
stands UNTESTED, now with the reason measured
rather than asserted; its record received its
dated append (spec051_execution; removal
reproduces the pre-act file byte-identically;
status and stage unchanged). Records:
specs/051-roif-arrow-sign/outcome.md,
reports/phase409_results.json (SHA-256
3f4bf2a5…), reports/phase409_report.md
(SHA-256 51a9d3a1…). Anchors byte-identical
before and after (df0cf620…). All products
are held under the Roif gate (spec §9).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.

## 2026-10-21 — Spec 048 EXECUTED (Phase-408): STRICT CORPUS NOT PINNABLE at gate 0.3 (held under the Roif gate)

Spec 048 was executed as Phase-408 under the
frozen contract (freeze digest 56beec70…; OSF
registration eqpab approved and public, DOI
10.17605/OSF.IO/EQPAB), in Wave 3 Group 3 of
the runnable-experiments campaign (design
D-04; consumer of Asset F), under the
graph-first build (script
backend/scripts/phase408_fish_family_step0.py;
node IndusPhase408FishFamilyStep0; registration
verified by import before the run, 497 nodes).
Integrity PASS: every §2 byte pin recomputes
to its freeze value by two independent routes
(Phase-43 record 78a6c219…, anchors
df0cf620… — 287 anchors, 94
strict_sa_independent, M072
pending_non_sa_validation — Mahadevan–Parpola
crosswalk 9ebd7723…, Spec 033 spec
eaea0e2e…); the claim file was asserted in
the Spec 038 form (manual_002's facts on the
live file; its freeze-time hash 3202aeca… a
definition constant — the live file's only
delta for manual_002 after the post-freeze
store regeneration is its extracted_at
timestamp). **Gate 0.1 PASS**: Asset F's
digest, recomputed over the canonical bytes
with the digest field excluded (Spec 044
§4.2), is
ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3
— identical to the digest recorded in Spec
044's step-0 outcome record (the pin source
fixed at the freeze, DD-048-9) and to the
file's own digest field; 7 members; the asset
was not rebuilt or substituted. **Gate 0.2
PASS**: every member joins via its
mahadevan_number locator through the pinned
crosswalk (M047, M048, M050, M052, M060,
M145, M147 — all MAPPED, none UNMAPPED, the
crosswalk's Parpola locator agreeing in
every case); the cross-check names every
divergence — of the claim record's trio
(72, 64, 70) none is an Asset F member, of
the Phase-43 six (267, 72, 65, 59, 60, 70)
only 60 is — and adds and removes no member.
**Gate 0.3 FAIL — the execution closed
STRICT CORPUS NOT PINNABLE in the frozen §6
wording.** The V3 / Mahadevan-lineage layer's
only loader of record reads the Firestore
'indusarrays' dump at
glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl,
which is absent from the tree (the tracked
rmrl directory holds only its bulletin and
provenance files); the loader, imported from
its file and run, loads zero records and zero
sequences, so the layer cannot be exported
whole or pinned, and the T2.4 reference
points (sign 72 — 181 occurrences, 25.9%,
supported; sign 267 — 356, 3.8%, not
supported) cannot be re-derived from a
pinned layer. No database copy exists in the
execution tree, and no other layer in the
tree is the corpus the Phase-43 record names
(Firestore source, 3,916 records / 3,137
sequences / 2,665 dockeys / 12,494
instances): the site-attributed layer carries
5,679 records, the V1 export 15,508
mixed-source objects, the ICIT export 3,085
ICIT-encoded sequences, and the Holdat path
is absent from the tracked tree and is the
second compilation besides. No layer was
substituted and no rule invented. Gates 0.4,
0.5, and 0.6 were NOT REACHED: no Holdat
judgement, no census (no TOO THIN judgement
is recorded or implied for any member), and
no control judgement exists. No
ending-follower rate was computed for any
sign in either arm, no sensitivity was
computed, and no family verdict is recorded:
the claim
parpola_2010_dravidian_solution_manual_002
stands exactly as recorded (IN QUESTION,
partially supported), its record unedited.
Anchors asserted byte-identical before and
after (df0cf620…). Foundation check at the
run: 40 passed / 0 failed / 8 warnings.
Records: specs/048-parpola-fish-family-profiles/outcome.md,
reports/phase408_results.json (SHA-256
c08e775c…), reports/phase408_step0_report.md
(SHA-256 9dca830c…) — both digests verified
by two independent routes, and the script
deterministic (byte-identical on a second
run). This entry and its records are
internal under the campaign's Roif gate
(R-7); not a publication.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.


## 2026-10-21 — Phase-43 battery deposit: producing script restored byte-for-byte as the record of record

Owner-approved amendment (Item 2 of the 2026-10-21 amendment queue): the
Phase-43 positional battery is pinned as a record of record. Deposited:
(1) backend/scripts/phase43_part2.py restored byte-for-byte from commit
3e0ab651fb3f38aed0385c73c66600819cc04f1c, SHA-256
6d5a079d47113937afd3340ab4b35781d1b7202644b180ba814d15f03f49699e — the
producing script of the Phase-43 results file; (2)
backend/scripts/phase43_all.py restored byte-for-byte from the same
commit, SHA-256
6a3bc7764ea32ddc4b578cad66881fdcb2b542ab03daa3f9a0ddcac6c30fb133 — the
sibling run whose T2.3 candidate-scan constants differ (top-50; floors
10 / 0.40 / 0.20) and which did not produce the deposited results; (3)
docs/phase43-battery-methods.md, stating the battery exactly as run
(V3 loader with min_length=2; position rule first=initial / last=terminal
/ else medial on sequences of length at least 2; count floor total at
least 5, 201 signs profiled; the six-step cascade TERMINAL_STRONG at
t_rate at least 0.60, INITIAL_STRONG at i_rate at least 0.55,
MEDIAL_STRONG at m_rate at least 0.65, TERMINAL_MODERATE at least 0.40,
INITIAL_MODERATE at least 0.40, else MIXED; the T2.3 opening-formula
counting rule; the T2.4 fish floors; the deposited corpus statistics
3,916 records / 2,665 dockeys / 3,137 sequences / 12,494 sign
instances), including the explicit statements that the battery contains
no chance-baseline step (none ever existed) and that the full member
lists for the 40/61 classes plus terminal ranks 11-20 were never written
to any file; (4) docs/phase43-battery-provenance.md, recording the
deletion (commit fac2f2c8f97f3982178b8f869b1542e1ffb4c389, 2026-05-17
cleanup), the recovery source (pre-purge mirror history), the results
file pin outputs/phase43_all.json SHA-256
78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4, and
the loader pin (backend/glossa_lab/data/indus_corpus_v3.py as on main —
loading logic byte-identical to the Phase-43 original; one cosmetic
__main__-block line differs). Restored files carry their original bytes;
no annotation was added inside them. This deposit does not establish
that the frozen classes can be reproduced today (the corpus dump is
missing; gates G3/G4 have never run), that the Phase-43 results are
correct, or that Specs 049 / 052 / 054 pass their other gates.

AI disclosure: executed by an AI agent (Muse, via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-21 — Spec 066 EXECUTED (Phase-428): INTAKE COMPLETE — CATALOGUE EXTENSION PINNED

The Phase-130 catalogue-extension intake (amendment package Item 7, owner-approved
2026-10-21) ran under the frozen contract: freeze digest
0b81d8421c8fe66b486b2c729bb7e978faa6327c74b8f1bff7984128a31aa355, freeze PR #314
merged at c6140cf199b158b25ee4cef6e3bcd9837eb000db on genuine CI green (run
39715444485, 7 of 7). The CISI 3.1 portion and its extraction are restricted
research material under PROVENANCE entry 22 of the restricted local store (the
gate is quoted verbatim in the spec's outcome.md §1); no scan, render, extraction
row, or extracted field beyond number + site section + published type class +
grade class entered git at any point, and repo cleanliness was checked before
any join work and again before the outcome commit. Step 0 asserted every pin
(portion PDF, extraction table, vols 1–2 catalogue CSVs, horus84
inscriptions.csv, the committed Phase-421 census/results, the Phase-130 schema,
the validator) and re-derived the candidate sets exactly: 2,101 distinct
well-formed portion numbers (1,341 referenced — 1,293 zero-resolution + 48
already-joined — and 760 unreferenced). Graded by the frozen ladder (corroboration
rung UNGRADED for every candidate, DD-066-7, because the in-hand layers carry no
FC/excavation/museum values): VERIFIED 2,089, CONFLICT 12 (NUMBER-AMBIGUOUS 11,
SITE 1), UNRESOLVED 0; referenced 1,331/10/0, unreferenced 758/2/0. The 2
low-confidence candidates were hand-verified against page renders and confirmed
as printed; the 183 medium-confidence candidates stand VERIFIED under the
stratum determination. The seeded stratum (seed 20261021; 30 VERIFIED, the whole
12-candidate CONFLICT class, the empty UNRESOLVED class) was hand-read on page
renders: 30 of 30 sampled VERIFIED sound; all 12 sampled CONFLICTs attributed
to extraction error (scan text-layer number misreads, photo-column spill into
data fields, OCR variants, empty key fields in duplicate plate listings); true
non-identity 0. HALT VERDICT: conflict share 12/2,101 = 0.57% against the 20%
cap, tripwire count 0 — NO HALT. The merged catalogue layer v2 was built and
held in the restricted local store only (SHA-256
cd0c2ba8823678be9f7573616528ae0b6be2fe579dc7e34c93add421c80886ad; 2,655,958
bytes; 9,741 rows; 5,529 distinct objects; 2,036 new objects; 53 collisions
where the existing object stands). The Phase-130 validator over the extension
dataset form (2,089 records, license_basis = the entry-22 gate) returned
pass-with-warnings, 0 errors. Committed: the extension index
data/intake/cisi31_extension_index.csv (2,101 rows, the four lawful columns),
reports/phase428_results.json, and specs/066-phase130-catalogue-extension/
outcome.md. The projected join — 2,899 + 1,777 = 4,676 rows (82.34%) against
the Spec 059 bar of 3,465 — is a projection only; no join has run. A VERIFIED
catalogue object is not a verified join; no F1 quantity exists from this act;
STUDY-SPEC-024/F1 stands as recorded SUPPORTED on its original joined subset
(MH OR 2.384 [1.847, 3.077], q=0.00015), and Spec 059's record stands unpatched.

AI disclosure: executed by an AI agent (Muse, via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-22 — Spec 064 EXECUTED (Phase-426): IDENTIFICATION FAILED — continuity/discrimination not sustained

Spec 064 ("Sign 297 Is the Horned Tiger": an Identification Concordance,
Successor to Spec 046) was executed as Phase-426 under its frozen contract
(freeze digest cfeb7baf71fad26e81ca80a08395c87a07d158974480923fd38eb2fed854c405),
under the separate execution order the freeze awaited (DD-064-17). The
execution gate was satisfied before the run: OSF registration s6hr9 is
approved + public (approved and API-verified 2026-10-22).

Outcome, in the frozen wording: **IDENTIFICATION FAILED
(continuity/discrimination not sustained)** — "The fragment 'sign 297 is
the horned tiger' cannot be carried to a concordance: the descriptor's
discrimination of 297 from its neighbours in the 289–308 run was not
sustained by both independent derivations. The record stays a stated gap.
No statement about the sign is made, and nothing is fed to Asset A.
Qualification (carried from the preserved reference, Spec 064 §1): the
identification of Wells's 297 rests on a drawn-form reference whose
continuity status is QUALIFIED — anchored at family level only; its
step C discrimination check is part of this run's record."

Step 0 passed in full: every spec section 2 pin recomputed and matched
(claim record 997fa336…, held Wells 2015 text 62acf855…, Phase-104
evaluation 2d0b83e8…, crosswalk registry 8a0b2a82…, Phase-123 witness
ecbc37a4…, lane-2 drafts 3f645c9a…, Spec 046 closure delivery 772db4df…
standing unedited, and the preserved drawn-form reference 33ee22ec…);
the source book produced from the held copy with the printed-p. 97
passage located verbatim; all four lists of record accounted for as HELD
or CITABLE (Wells HELD, CISI HELD, Parpola CITABLE, Mahadevan CITABLE);
and gate 0.4 passed — the local thesis file's digest asserted against
its pin (4b39330c…, 19,313,853 bytes) before any plate was read, and the
plate page (Wells 2006 thesis, Figure 3.2, thesis p. 90 / PDF p. 102)
produced from it. No image is committed anywhere in the run.

Step 1 named the source's sign list from the book's own apparatus —
Wells's own list (Wells 2011), in Wells 2015 Chapter 2 / Figure 2.6.
Step D derived the drawn-form descriptor twice, independently, from the
thesis plate (three strokes clear above a single sharp bend, four stroke
ends at the base, uppers slanting steeply down-left, lowers running down
to the right with a basal splay) and sustained the preserved reference:
agreement on its feature set, with two noted readings (the preserved
"four" is the count at the base; its "near-vertical" lowers slant about
30 degrees from vertical) judged not material. Step C — mandatory in
this successor — was then not sustained: neither derivation affirms that
the descriptor picks out plate 297 and no neighbour in the 289–308 run
(signs 299, 302 and 303 satisfy every stated feature of the descriptor;
the family anchor, registry row P205, is corroboration only and expressly
not an identification). The run closed under the pre-registered closure
before step M and before any scoring; step 2 was not reached, no list was
scored, and the hypothesis is unjudged on concurrence grounds. The
preserved reference's continuity status remains QUALIFIED, carried on
every product of the run.

Delivery in the frozen closure form:
specs/064-sign297-concordance-successor/concordance-297.json (schema
glossa.concordance/1; producer_spec 064; signs empty; closure block),
SHA-256 9e765576349d4d294a4fc04f0d6750be3718dfc60fa267ea16c04c6130db7488
(derived twice, identical; the run is deterministic and reproducible
byte-identically). Records: reports/phase426_results.json,
reports/phase426_concordance_report.md,
specs/064-sign297-concordance-successor/outcome.md; graph node
IndusPhase426Sign297ConcordanceSuccessor registered and verified by
import before the run; the claim's record received its dated
successor-check append (spec064_check, Phase-426, 2026-10-22) beside
Spec 046's unedited first_check entry, verified at the act (removal
reproduces the pre-act file byte-identically; status and stage
unchanged). Spec 046's frozen record, outcome, and closure delivery
stand unedited. Anchors asserted byte-identical before and after
(df0cf620…).

## 2026-10-22 — Spec 063 (Phase-425) executed — RECOVERED (route 2)

Spec 063 (the sign-821 identification successor
to Spec 056) was executed as Phase-425 under
the frozen contract (freeze digest dc24a10e…;
OSF registration kfet5 approved and public,
API-verified 2026-10-22), under the owner's
separate execution order (DD-063-13).
Graph-first build: backend/scripts/
phase425_sign821_identification.py, graph node
IndusPhase425Sign821Identification registered
and verified by import before the run. Step 0
passed in full: every §2 pin recomputed (held
text 62acf855…, registry 8a0b2a82…, witness
ecbc37a4…, Spec 056's freeze/outcome/extraction
records, Phase-104 evaluation 2d0b83e8…,
lane-2 drafts 3f645c9a…, anchors df0cf620…,
preserved reference 695dd35d…); the claim
record asserted in the Spec 038 form (constant
bd0f7abd… in freeze.json plus the fragment's
facts on the live file — entry present,
UNTESTED, created, its spec056_closure append
present); the local Wells 2006 thesis PDF
asserted to its frozen digest on the local
file BEFORE any plate was read (4b39330c…,
19,313,853 bytes); and the plate page (thesis
p. 92 / PDF p. 104, Figure 3.2) produced from
that pinned file (its embedded plate image
Im106.tiff, SHA-256 961ed7de…). Step D: two
independent derivations from the plate —
sequential plate read and neighbour-contrast
read, each without sight of the other or of
the drafted descriptor wording — agree feature
by feature: two identical vertical oval
outlines side by side, touching at the
vertical midline, each divided by three
straight diameters (one vertical, two
diagonal) into six sectors; their neighbour
discriminations agree on all five named
neighbours (818 a single 4-sector circle; 820
the single oval; 822 a single spoked oval
flanked by paired vertical strokes; 823 a
single denser-crossed oval; 791 two plain
ovals). No disagreement arose. The reconciled
descriptor agrees with the preserved record's
descriptor on every feature — the reference
is SUSTAINED, checked not inherited. Step C:
continuity passes on the anchors' agreement —
the Appendix II formation passage ("sign 820
doubles to form sign 821", held-text lines
3691–3704, verified verbatim), the P378
registry anchor (W820 / M391, "Wheel with 6
spokes with even angles"), and the plate
agreement at 820/821 all agree on the doubled
six-spoke-wheel form; the plate number alone
anchored nothing. Step M: route 1 (registry,
by drawn form) was attempted and FAILED — no
registry row carries the doubled form (its
only two "6 spokes" descriptions are P378, a
single wheel, and P379, a single flanked
wheel), with no fallback to P378, the base
sign; route 2 (the list's own entry, through
the preserved reference) SATISFIED the match;
route 3 (composition) was not used — exactly
one route identifies the sign. Traps asserted
by name: Yunmapped_0821 (a Yajnadevam glyph
identifier, empty wells_ids, frequency 10 —
asserted as a trap, never used), sign 861
(Figure 6.12 reading-confusion trap), P378 as
the target, and number-only matching in any
form (none used). Candidate K-1 — sign 821,
in the Dholavira signboard contexts, has a
meaning of "city", either as a determinative
or as a word (Wells 2015, printed p. 92) —
therefore passes R-1 through R-5 (R-1, R-2,
R-4, R-5 of record in Spec 056's executed
record on the pinned passage; R-3 run afresh
under §5) and the outcome is RECOVERED. The
claim enters the lifecycle at the created
stage, untested, as the appended
spec063_restatement entry on the fragment's
own record (proposition, verbatim quote and
locator, named sign list and identification,
R-4 condition, R-5 numbers and conditions, and
the designed-never-run test note; removal of
the append reproduces the pre-act file
byte-identically; the fragment's original
entry and its spec056_closure append stand
above it, unedited). No test was run. Spec
056's record is unedited; its IDENTIFICATION
FAILED stands as the record of the first run.
Records: specs/063-sign821-identification-successor/
outcome.md, specs/063-sign821-identification-successor/
identification-record.md,
reports/phase425_results.json (SHA-256
c7b246e9…), reports/phase425_identification_report.md
(SHA-256 67f753bf…). Anchors asserted
byte-identical before and after (df0cf620…).
Foundation check as measured: 40 passed / 0
failed / 8 warnings. This act is
identification on a preserved reference: it
establishes, at most, whether the drawn sign
candidate K-1 names is identified in the
program's claim form — never whether K-1's
suggested meaning is right, and nothing about
sign 821 itself beyond the identification.

## 2026-10-22 — Spec 067 EXECUTED (Phase-429): REPLICATED

Spec 059's question re-run against the Spec 066 merged catalogue layer v2, under
the frozen Spec 067 contract (freeze digest
73463ab949f65ecf620a9f4544b9a84fe18f72056a86c48ce9d5d0164f3d41db; freeze PR #318
merged at dcfa3af6; OSF registration qsthg approved and API-verified public
before the run). Step 0, in the frozen order: gate 0.1 PASS — every pin
recomputed, the merged layer v2 asserted on the local file first (SHA-256
cd0c2ba8823678be9f7573616528ae0b6be2fe579dc7e34c93add421c80886ad, 2,655,958
bytes, 9,741 rows, 5,529 distinct objects); gate 0.2 PASS — the original
concordance join reproduced exactly against the vols. 1–2 layer (5,679 / 2,895
/ 2 / 2,782), contributing no row; gate 0.3 PASS — the object-ID join through
the Phase-130 schema (5,018 records, validation pass) joined 4,676 of 5,679
rows (82.34%) against layer v2 (661 no identifier, 342 resolving to zero, 0
ambiguous; 3,763 distinct objects); gate 0.4 PASS — the mandatory type-fill
census before any F1 quantity: newly joined objects 1,777 rows / 1,284 distinct
objects, type filled 1,152 objects, unfilled 132; whole joined set type filled
3,511 of 3,763 distinct objects (317 rows unfilled), restricted to
{Seals, Tablets} 4,077 rows, census-form eligible strata Harappa, Kalibangan,
Mohenjo-daro; gate 0.5 PASS — 4,676 joined rows against the bar carried from
Spec 059 at DD-067-7 (≥ 3,465 rows, 61.0%), a margin of 1,211 rows, judged on
this execution's own census (Spec 066's projection is not cited as a result).
The frozen Phase-136 flow on the enlarged set, unchanged: 4,676 joined → 4,359
typed → 4,077 seals/tablets → 3,315 terminal-mapped → 3,181 in the eligible
strata (Harappa, Mohenjo-daro, Kalibangan — the original three); estimable
(pooled expected counts ≥ 5 in 4 of 4 cells). CMH chi-square 67.3998;
permutation raw p = 0.0001 (B = 9,999, seed 20261009); family-adjusted
q = 0.0001 (single-test family, DD-067-8); Mantel–Haenszel common odds ratio
2.452, 95% CI [1.965, 3.058] — entirely above 1.5, so the §5 verdict is
REPLICATED. Leave-one-site-out (descriptive): drop Harappa 2.214
[1.611, 3.042], drop Mohenjo-daro 2.723 [2.026, 3.659], drop Kalibangan 2.465
[1.974, 3.079] — every subset estimable, no site load-bearing. Both covariate
comparisons are in the machine record (the added rows are chiefly Harappa's,
shorter, and more fragmentary than the original joined set). The claim's
"on the joined subset" scope is re-stated by the outcome's appended record
only, as §5 provides for a REPLICATED outcome: the difference is now recorded
on the enlarged object-ID-joined subset, 4,676 of 5,679 rows (82.34%). Spec
024's frozen verdict and Spec 059's gate closure stand exactly as recorded,
unedited. Anchors asserted byte-identical before and after (df0cf620…).
Foundation check as measured on the execution tree: 40 passed / 0 failed /
8 warnings. The per-row join census against layer v2 stays restricted-local
(phase429_join_census.json, 5,679 rows, beside the merged layer in the
restricted local store), named by filename and count only; no row-level
merged-layer data entered git. Records: specs/067-f1-enlarged-join/outcome.md,
reports/phase429_results.json (SHA-256 f08d469b…), reports/phase429_report.md
(SHA-256 8cc2c154…); the script is deterministic (all outputs byte-identical
on a second run).

AI disclosure: executed by an AI agent (Muse, via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-22 — Spec 065 EXECUTED (Phase-427): Class B — S-5 RESOLVED, S-1 STILL BLOCKED

Spec 065 was executed as Phase-427 under the
frozen contract (freeze digest f50a6e9c…;
OSF registration 34s9u approved and public,
API-verified by the parent before the
execution order; owner's 2026-10-21 approval
of the amendment package as written, Item 6).
Step 0 passed in full, in frozen order: gate
0.1 input integrity — every §2 live pin
recomputes to its freeze value (the two held
cleaned texts, the two registry files, Spec
057's freeze record, outcome, spec, and
adjudication, and the anchors file), with the
extracted-claims store asserted by entry
facts under the Spec 038 form (fingerprint
a4874349…, the merged_into posture as Spec
057 left it, the rows' quote fragments —
S-1's lowercase "positional analysis", S-5's
sentence-case "Positional analysis"); gate
0.2 the acquired S-5 file asserted on the
local file (657,863 bytes, SHA-256
77f10f32…, MD5 36616e20… matching the Zenodo
record); gate 0.3 the S-1 intake
determination — the blocked arm, on evidence
re-read first-hand at step 0 (no intake-S1.json
in the spec directory; PROVENANCE.md carries
no S-1 provenance entry, entry 23 being
Hunt/S-5 and both S-1 sections stating no
file acquired and no provenance entry taken;
the S-1 downloads folder holds only
BLOCKED.md; the Oakland ILL portion-copy
request placed 2026-10-22 is pending, with
nothing delivered and nothing intake-pinned);
gate 0.4 order. The accounting, one outcome
per source: S-5 HEADING ABSENT FROM DOCUMENT
— the acquired file's own text layer,
extracted in full from the pinned bytes
(pdftotext -layout; 2,273 lines, 84,672 bytes;
artifact extraction-S5.txt, 74e42f8e…),
carries exactly one occurrence of "positional
analysis" (extraction line 340, PDF page 9),
sentence-initial inside a running paragraph
of §5.5 "Governance and Civic Authority"
("…waterworks. Positional analysis / shows a
clear tripartite administrative grammar:") —
a mention inside a running sentence, not in
heading form under the carried §5.1 rule; the
Spec 057 sub-state HEADING NOT PRESENT IN
HELD TEXT is converted to a document-level
finding on the acquired file's hash, and no
passage or claim arises. S-1 STILL UNLOCATED
— ACQUISITION BLOCKED (owner account act) —
no search was run for S-1 and nothing about
the chapter is found or implied; its evidence
is the blocker record, and the unblocking act
remains a handed-over, intake-pinned copy
before a later run. Headline class B in the
frozen §7.1 wording. Disposition (§7.2): the
heading record stands superseded-not-retired
exactly as Spec 057 left it, by appended
dated disposition_spec065 note only — no
pre-existing field altered, Spec 057's
disposition entry unedited, removal of the
append reproducing the pre-act file
byte-identically (verified at the act), status
and stage unchanged; retirement is not
available while S-1 remains unlocated.
Hypothesis F065-C14 is defeated over the one
document actually searched (S-5) and stands
unjudged as to S-1. No claim was recovered,
no claim was checked, and no positional
finding is established by this act. This act
searched two documents for a heading. It
checked nothing either passage states.
Anchors asserted byte-identical before and
after (df0cf620…). Foundation check at the
execution: 40 passed, 0 failed, 8 warnings.
Records: specs/065-s1-s5-heading-successor/
outcome.md, specs/065-s1-s5-heading-successor/
extraction-S5.txt, reports/phase427_results.json,
reports/phase427_s1_s5_report.md.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-22 — Spec 065 S-1 RECOVERY ACT (Phase-427): S-1 RESOLVED — HEADING ABSENT FROM DOCUMENT; combined accounting Class A; heading record RETIRED

The separately commissioned recovery act
named by the frozen contract (spec §4.2: an
intake record appended after the run arms a
later act) and by the execution record's S-1
row. The document was handed over by the
owner on 2026-10-22 — his own download from
the author's Academia.edu posting, delivered
by upload — and pinned at hand-over
(PROVENANCE.md entry 24, local research
store) and by the intake record appended to
the spec's directory (intake-S1.json):
Ancient_Writing_and_Modern_Technologies.pdf,
3,565,316 bytes, SHA-256 51831ac9… — one
value across the intake pin, the registry's
recorded checksum for S-1's source document,
and the spec §2.1 pin. The pinned file was
asserted by SHA-256 before any search, its
§2 record inputs re-asserted on the live
files, and its own text layer extracted in
full from the pinned bytes (pdftotext
-layout; 1,097 lines, 54,058 bytes; artifact
extraction-S1.txt, e5bc973d…; deterministic,
reproduced byte-identically on a second
run). Every occurrence of "positional
analysis" (case-insensitive) in that text
layer — exactly two, none pre-filtered, a
whitespace-flexible search confirming none
is split: extraction line 121, PDF page 4
(printed p. 60), a mention inside a running
sentence of SEGMENTATION METHODS ("…
paradigmatic cluster analysis, structural
analysis, or positional analysis of
signs"); and extraction line 925, PDF page
31 (printed p. 87), a bibliography entry in
LITERATURE for Fuls 2013's "Positional
Analysis of Indus Signs". Neither is in
heading form under the carried §5.1 rule
(running-sentence mentions and bibliography
entries never anchor a passage). S-1
therefore resolves HEADING ABSENT FROM
DOCUMENT, a document-level finding on the
searched file's hash, converting the Spec
057 sub-state HEADING NOT PRESENT IN HELD
TEXT; in substance it matches the held
text's posture (the same two occurrences in
the same two postures), now on the document
itself. No passage was delimited, no claim
recovered, none checked. On the completed
two-row accounting (S-5 HEADING ABSENT FROM
DOCUMENT at the execution; S-1 HEADING
ABSENT FROM DOCUMENT by this act), the
frozen §7 derivation gives headline class
A — BOTH SOURCES RESOLVED, in the §7.1
pre-written wording (outcome.md §9.3); the
execution's class B headline stands
unedited as that run's record. Disposition
(§7.2): both sources resolved and neither
row of the successor recovered a claim, so
the canonical heading record
ancient_writing_and_modern_technologies_51831ac9_statisti_0004
stands RETIRED — as an extraction artefact,
in the form Spec 057 §7.2's retirement limb
states for a complete accounting — by
appended dated disposition_spec065_recovery
note only; Spec 057's disposition and Spec
065's disposition_spec065 entries stand
unedited, no pre-existing field was
altered, and removing the append reproduces
the pre-act file byte-identically (pre-act
c994b18d…, post-act 861b1468…, verified at
the act); the record's status (untested)
and stage (created) are unchanged.
Hypothesis F065-C14 is now defeated over
both documents actually searched; it no
longer stands unjudged as to S-1. Anchors
asserted byte-identical before and after
(df0cf620…). Foundation check at the act:
40 passed, 0 failed, 8 warnings (the store's
combined hash stood at 07fb35c9… on the
act's base and moves by this act's append;
the committed report is regenerated with
this record). Records:
specs/065-s1-s5-heading-successor/outcome.md
§9, specs/065-s1-s5-heading-successor/intake-S1.json,
specs/065-s1-s5-heading-successor/extraction-S1.txt.

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.

## 2026-10-22 — Spec 025 MATERIAL AUDIT EXECUTED: paper-search check of all 31 extracted claims + preprint citations

Per the owner's 2026-10-22 order, executed on
branch spec/025-paper-search-research-check
(main merged in at a5a65f86) under the protocol
in docs/paper-search-mcp.md. RESEARCH-CHECK
stage sidecars now exist for all 31 claims in
glossa-indus/claims/extracted_claims/ (advisory,
verdict null by construction); all raw outputs,
worker findings, and the audit report are filed
in specs/025-paper-search-research-check/
audit-2026-10-22/. Headline outcomes: both
strongly_supported Yadav extractions verified
verbatim against the source papers' full texts
(the Zipf fit is on the EBUDS subset of M77;
beginner/ender priority runs to Kondratov 1976
and Mahadevan 1977); the Farmer-cluster
"contradicted" framing did not survive the
challenge pass as a settled refutation (Sproat
2014 and Rao et al. 2010 read in full text —
the literature position is contested and
unresolved); a three-part positional grammar is
published prior art (Wells 2015 ch. 3; Sinha et
al. 2010; Yadav 2009; Fuls's positional classes);
the fish = mīn rebus priority is Heras's, with
Parpola 2010 a synthesis; the Roif document is
a self-published manuscript with no venue or
identifier of its own. No claim status, anchor,
or score was changed by the audit; ten
correction proposals are filed gate-pending in
the audit directory. Open gaps include Kak
1988, Mahadevan 1977 full text, Kondratov 1976,
Korvink 2011, the Rao Science/PNAS full texts
via this connector, and the session-long
OpenAlex/Semantic Scholar 429 outages.

AI disclosure: executed by an AI agent (Muse,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.

## 2026-10-22 — Preprint v5: citation corrections from the Spec 025 material audit

glossa-corpus/indus/pierson_2026_indus_
decipherment.tex bumped v4 → v5 (citation
corrections only; docs/research/
PREPRINT_VERSIONING.md and AGENTS.md updated).
§8 entries corrected: Wells & Fuls 2015 (was
"Wells 2011"); Parpola, Parpola & Brunswig 1977,
JESHO 20(2), Simo Parpola first author (was
1975, 18(2)); Crawford 2001 as the monograph
(was an Archaeology International article);
Parpola 2010 as the CICT conference lecture,
Coimbatore (the World Archaeology 42(2)
attribution was not verified in any reachable
index — seven Crossref searches across two
workers). Rao et al. Science 2009 entry added;
the §1.2 entropy result now cites it instead of
the PNAS Markov paper; the §2.1 Zipf exponent
~1.7 no longer carries a Rao 2009 attribution
(no text read reports it; Yadav 2010's full-text
fit gives b = 2.59 on EBUDS/M77). Nair 2026
characterizations in §1.3/§3.10/Acknowledgments
corrected to his full text (independent scorecard
study; hedged intermediate result — not a
replication of this paper's tests); his three
quoted statistics verified exact. Evidence and
bounds per item: audit-2026-10-22/
corrections_log.md. The v5 PDF was NOT
regenerated (no xelatex in the audit
environment); the v4 PDF remains the compiled
artifact of record. Nothing submitted.
Adversarial pass required before submission.

AI disclosure: executed by an AI agent (Muse,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.

## 2026-10-22 — Spec 025 material audit: merge record (addendum)

PR #331 (branch spec/025-paper-search-
research-check) merged to main as 814a5dc2.
Commits: 5d436362 (audit records, stage
sidecars for all 31 claims, preprint v5,
ledger entries) and 0abf27f3 (AUDIT_REPORT.md,
W5 findings reconstruction by repair worker
W7, and a ruff F401 fix in
backend/glossa_lab/research_check.py — an
unused typing.Callable import that the
shell-wrappers CI job caught on all three
OSes; ruff check backend/ passes). CI on the
final head: all seven checks green (backend
pytest, frontend Playwright, evidence-graph
smoke, Indus public validation, shell
wrappers ×3). No anchors, phase data, claim
statuses, or scores were touched, so the H21
foundation check was not triggered. This
addendum and the report's merge line land
via a small follow-up PR.

AI disclosure: executed by an AI agent (Muse,
via Muse) at the direction of Tristen Pierson,
per constitution sec.VI.

## 2026-10-22 — Spec 025 material audit: fix commission, batch A (proposals P1–P8 notes and metadata; P5)

Owner order 2026-10-22: "fix all of these and make all the
corrections and get back on track." Executed against
correction_proposals.md in specs/025-paper-search-research-check/
audit-2026-10-22/. Dossier framing/priority/scope notes were
appended as dated audit_note_2026_10_22 entries on the affected
claims (P1 Farmer framing — contested and unresolved; P6 Parpola
priority — the fish rebus is Heras's, Parpola 2010 a synthesis;
P7 Yadav corpus-scope and priority; P8 Hunt/positional prior-art
and the Fuls source identification of the "Positional Analysis"
stubs). Literature-registry source fields were corrected in
place with the old values preserved in an appended
metadata_correction record (P2 fuls2023 detected_year 2008 →
2023; P3 the Roif document's detected_doi removed — it is a
self-published manuscript with no identifier of its own; P4 the
Fuls chapter's authorship, year, title, and the removed DOI,
which belongs to Fuls 2015). P5: the DECIPHERMENT_DOSSIER_v1.md
"Nair (2026) scorecard: 4/4 linguistic-consistent" line was
corrected in both places it appears to Nair's own framing
(4/4 against the heraldic baseline, 2/4 against the
administrative baseline; intermediate conclusion). No claim
status, stage, anchor, or score was changed anywhere, so H26
is satisfied by construction — the audit records are the cited
non-SA evidence — and the H21 foundation check was not
triggered; its posture is asserted in the fix addendum. P9/P10
and the preprint version follow in batch C; the tooling proof
and gap-closure evidence are batch B.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-22 — Spec 025 material audit: fix commission, batch B (tooling proof, gap-closure evidence, public-surface check)

Batch B files the fix commission's evidence records in
specs/025-paper-search-research-check/audit-2026-10-22/:
fix_execution_addendum_2026-10-22.md (per-proposal execution
record for batches A and B), raw/fix_ws2_unpaywall_proof.md
(the Unpaywall email configured per the connector doc's
environment mechanism; the audit session's failed Yadav DOI
re-run — proven end-to-end via the Europe PMC route with the
artifact identity-checked; the crossref download route's
wrong-artifact defect recorded as standing),
raw/fix_ws3_evidence_notes.md and raw/fix_ws3_handoff.md
(Rao Science and Rao PNAS full texts read — the PNAS paper
contains no Zipf content, upgrading audit correction #6 to
full-text confirmation; Wells 1998 thesis resolved at record
level; Kak 1988 examined, Zipf attribution unsupported at the
reached evidence level; the five in-text Mahadevan works
verified at published-bibliography level; Steinkeller narrowed
but still open), raw/fix_ws3_rao_pnas_crossref.json,
raw/fix_ws2_yadav2010_first_page.txt, and
public_surface_check_2026-10-22.md (neither research page
states any corrected item; one clarifying prior-art draft
filed for the owner's approval — nothing published).

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-22 — Spec 025 material audit: fix commission, batch C (P9, P10 flag, preprint v6 + adversarial pass)

Batch C completes the fix commission. P9: the preprint's §8
gains the five Mahadevan works the text already relied on
(1981, 1982, 1986, 1989, 2011), from records verified at
published-bibliography level on the batch-B evidence (the
2011 identification is inferred and is stated as such
wherever the entry is described); the §3.23/§3.24 paper
counts, which no verifiable source supports, are qualified
in the text as this program's own text-mining corpus counts.
P10: the §8 Steinkeller 1982 entry is unchanged and stands
flagged as unverified — new evidence positively indicates
the titled article is JAOS 108(2):197–202 (1988), the 1988
record was not substituted per the proposal's own rule, and
the JAOS 102(2) contents check remains the one named open
item. The preprint is bumped to v6 (source + regenerated
PDF: TinyTeX XeLaTeX, two clean passes, 18 pages, corrected
entries spot-checked in the rendered output; the v4 PDF is
superseded). The adversarial pass required before submission
was run on the v6 source by an independent engine and
adjudicated finding-by-finding
(audit-2026-10-22/adversarial_pass_2026-10-22.md): one
finding sustained in narrow form (the §2.1 Zipf exponent
~1.7 is the paper's own unreleased-corpus statistic without
a checkable derivation — flagged for the owner's submission
decision, not silently rewritten), three not sustained.
Nothing has been submitted or deposited; the package stops
at submission-ready (audit-2026-10-22/
submission_package_summary_2026-10-22.md). No claim status,
anchor, or score changed in any batch; H21 was not
triggered (no anchor, language-model, or phase-result files
touched) and the committed foundation report stands at
59 OK / 0 failed / 6 warnings.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-22 — Spec 025 material audit: fix repair (literature records restored to frozen pins; P2/P4/P8 corrections moved to dossier notes)

Repair landed with batch C (PR #336). Batch A's in-place
edits to three literature-registry records (the Fuls 2023
catalogue, the Fuls chapter, the Positional Analysis paper)
changed bytes that are freeze-pinned whole-file by the Spec
055 and Spec 057 freeze tests (SHA-256 92e19e6d…,
bb23e5e9…, 9b95174b…). PR #334's first backend failure was
this collision; it was misclassified at the time as a
cold-cache transient, and that classification is corrected
here and in audit-2026-10-22/fix_repair_2026-10-22.md (the
passing runs are consistent with the suite's in-job store
regeneration restoring the pinned bytes; the job runs with
--maxfail=1, so only the first failing test was ever shown).
The three records are restored byte-for-byte (hashes verified
equal to their pins), and the P2, P4, and P8 source
corrections are preserved as dated audit_correction_2026_
10_22 notes on the corresponding claims dossiers — the
proposals' own alternative limb for frozen fields. P3's
registry edit stands (that record is not whole-file pinned).
No frozen test was re-pinned; if the owner prefers the
registry records themselves corrected, the ruling needed is
to amend the Spec 055/057 pins to the corrected bytes.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-22 — Roif credit: preprint v7 (fish credit landed; §3.32 restoration draft held)

Owner-directed addenda to the spec-025 audit fix commission
(record: audit-2026-10-22/roif_credit_addendum_2026-10-22.md).
Preprint v6 carried zero mentions of Avishai Roif while §3.5
and §3.19 report tests of his published fish-sign model.
Preprint v7 corrects that: §8 gains Roif 2025a (Academia.edu,
12 June 2025, academia.edu/129921039) and Roif 2025b
(Academia.edu, 2 August 2025, academia.edu/143222807) — no
DOIs, stable URLs are the identifiers; §3.5 and §3.19 credit
the model to him in his terms (/mi/ (mīn) value/divine marker
and guild/title marker; the "coastal controller"
maritime-guild reading) with the division of labour stated
(his model and predictions; the program's measurements); §7
Acknowledgments names him as the model's source. PDF
regenerated (two clean XeLaTeX passes, 18 pages, SHA-256
b7a640ac…), Roif content verified in the rendered output.
Dossiers: the Roif literature record's detected_authors now
names him (dated credit note; record not freeze-pinned), and
all six Roif-dossier claims carry dated credit notes naming
him as the claims' author (P3 extended). §3.32 (betweenness)
was NOT restored: a marked restoration draft reconstructed
from the Phase 172–177 records is filed with the package,
HELD PENDING ROIF'S REPLY, carrying the agreed verbatim
attribution sentence. Nothing submitted, posted, or sent;
no claim status, anchor, or score changed; H21 not
triggered.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## [2026-10-22] Entry — Shakti readiness decisions recorded; P-F1 intake adopted; successor drafts commissioned

Objective:
  File the owner's seven Shakti-readiness decisions of 2026-10-22 in
  the program's records — the adopted P-F1 intake record for the
  ShaktiOSindia corpus, the prediction-register notes those decisions
  require, and this ledger entry — without changing any frozen
  record, register term, or campaign outcome. The decisions come from
  the owner's item-by-item walk through section 4 of the readiness
  memo (research_notes/shakti-readiness-proposals-2026-10-22.md) in
  the parent chat on 2026-10-22; the memo itself is unchanged and
  unedited.

What was done:

  1. DECISIONS RECORD: docs/decisions/2026-10-22-shakti-readiness-
     decisions.md — the seven decisions in substance: (1) P-F1
     adopted as written, gates S1–S4 the standing citation form for
     the Shakti corpus, senior to every successor; (2) Spec 053
     successor approved for drafting under Amendment S-053
     (documented-only primary, 3,212 rows; documented+corroborated
     sensitivity, 5,299 rows; strict-set choice reserved to the
     freeze; the result is a new baseline, neither confirming nor
     correcting Phase-43); (3) Hunt re-scope commissioned in
     dependency order; (4) fish-family re-design commissioned,
     ICIT-native, with the Roif gate carried; (5) Spec 018's frozen
     matrix confirmed governing PRED-2026-001/002/003, no class
     amendment to fit Shakti, all three remain PENDING unscored, no
     section 8 dry-run on Shakti; (6) PRED-2026-012 note only — its
     block is documentary, no documents hunt commissioned, remains
     PENDING unscored, Spec 043's closure stands; (7) D-24 trigger
     discipline — Shakti does not trip D-24 / D-01B / D-07B / D-27A2,
     all triggers remain armed.

  2. INTAKE RECORD: docs/decisions/2026-10-22-shakti-corpus-intake-
     record.md — the P-F1 intake record as adopted: corpus identity
     and pins (sanitized_corpus.json, SHA-256 345241b1…; upstream
     commit e48b3ec1; licence as stated by the deposit: corpus
     GPL-3.0, scripts MIT; held restricted-local, never in git), the
     row-grades file pin (shakti_row_grades_2026-10-22.csv, SHA-256
     02394241… — the provenance audit recorded the path but no hash;
     this hash was computed on the held file and is pinned for the
     first time by the intake record), the Yajnadevam lineage
     evidence pin (population-script.sql, SHA-256 a1bcc150…), the
     census (5,704 rows; 5,536 analyzable; grades 3,212 / 2,087 /
     405; 4,904 of 5,536 analyzable rows, 88.6%, carrying a CISI
     identifier; 18,065 true sign tokens; 713 distinct signs; 77
     sites), the four gates S1–S4 in adopted form, and the citation
     rule (a successor cites the corpus only through this record and
     asserts S1/S2 in its step-0 record).

  3. PRED NOTES: docs/PREDICTION_REGISTER.md, section 6 only, two
     dated notes appended, no other text touched — the Shakti
     corpus adjudicated NON-QUALIFYING for PRED-2026-001/002/003
     under Spec 018's frozen matrix, with the owner's confirmation
     recorded; and the PRED-2026-012 owner note (documentary block;
     no documents commission). No prediction's Tested or Outcome
     field moved.

  4. COMMISSIONED DRAFTS: Spec 068 (Spec 053 successor), Spec 069
     (Asset A build), Spec 070 (openings successor), Spec 071
     (sky-signs successor), Spec 072 (fish-family re-design) — to be
     prepared as freeze-ready drafts. Freezes are reserved to
     separate owner acts; nothing in this entry freezes, executes,
     or registers any of them.

  5. DATA WATCH: the D-24 trigger-discipline note was appended to
     ~/workspace/glossa-run/indus-data-watch-state.md on 2026-10-22,
     instructing the weekly data watch that Shakti does not unblock
     D-24 / D-01B / D-07B / D-27A2 and that all triggers remain
     armed.

AI disclosure: produced by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.

## 2026-10-22 — Spec 068 EXECUTED (Phase-430): COMPARISON UNINFORMATIVE

Spec 053's frozen control-systems comparison executed on the Shakti corpus as
its successor under Amendment S-053, under the frozen Spec 068 contract
(freeze digest ab890859c0ec313b4e2cdf89a9dddd885fae505e888c5f8c9ef2ba68c5f3c62d;
freeze PR #342 merged at 9bdb21d0; OSF registration 3pbwe filed 2026-10-22 and
standing pending approval at the run, recorded as it stands per freeze.md §7
and the owner's execution order of 2026-10-22). Step 0, in the frozen order,
all PASS: gate 0.1 — every §3 pin recomputed (the claim file at its DD-068-8
re-pinned hash ec31778a…, the intake record standing); gate 0.2 — the
estimator self-test by Phase-413's own functions (planted α 1.20 / q 2.0
recovered as 1.256 / 2.72); gates 0.3–0.4 — the Shakti pins recompute and the
audit census reproduces exactly (5,704 rows; 5,536 analyzable; grades 3,212 /
2,087 / 405; 18,065 tokens; 713 signs; 77 sites), with this successor's own
census governing (primary 3,045 analyzable / 11,805 tokens / 557 signs;
sensitivity 5,131 / 17,216 / 707); gate 0.5 — the population act under limb B
(DD-068-7: the full ICIT sign inventory of the restricted corpus; no mapping
act); gate 0.6 — the four controls entered whole as cited data before any fit
(N1 Mesopotamian numerical signs, 12 types / 1,981 tokens, from the published
SFU NatLang proto-cuneiform derivation; N2 heraldic charges, 57 types / 825
tokens, from the Dering Roll's 324 blazons under the frozen counting rules;
P1 Linear B, 89 types / 47,292 tokens, from the DAMOS transliterations; N3 the
Yule–Simon process, ρ = 0.10, seed 20261021, 99 replicates); gate 0.7 — floors
met (557 ≥ 50 types; 11,805 ≥ 2,000 tokens). Fits under Spec 053's one frozen
estimator (every system cross-checked exactly against Phase-413's
implementation of record): Indus primary α 2.004, q 19.9, NRMSE_log 0.1584;
N1 0.5335; N2 0.1839; N3 median 0.2405 (as-well share 0.00); P1 Linear B 0.9229.
No non-linguistic control fits as well as the Indus primary — the falsifier
does not fire, and no control is a NEAR MISS (the closest, heraldic charges at
gap +0.0255, sits above the frozen 0.02 band). But the positive-control
condition fails: Linear B, the set's one certain writing system, fits worse
than every non-linguistic control — worst of all five systems — so under the
frozen §5.5 mapping the headline is COMPARISON UNINFORMATIVE whatever the
falsifier does. The sensitivity fit (α 1.96, NRMSE_log 0.1544) carries the
same verdict-relevant ordering — not grade-sensitive — and the subsampling
tables are in the machine record. Per the §7 wording for this outcome, the
claim yadav_2009_arxiv_manual_001 stands exactly as recorded with no strength
label added; the Indus quantities are a new baseline on the Shakti corpus,
neither confirming nor correcting any Phase-43 quantity. Anchors asserted
byte-identical before and after (df0cf620…). Foundation check as measured on
the execution tree: 40 passed / 0 failed / 8 warnings. The restricted corpus
and row-grades files were read from the restricted local store only; no
corpus data entered git. Records: specs/068-yadav-zipf-controls-successor/
outcome.md, reports/phase430_results.json (SHA-256 ca83af8f…),
reports/phase430_report.md (SHA-256 e7597718…); the script is deterministic
(the control tables were re-issued with LF line endings before the
record was finalised, so the committed bytes are the cited bytes;
the final record then reproduced byte-identically on a second run).

AI disclosure: executed by an AI agent (Muse, via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.
## 2026-10-22 — Spec 069 EXECUTED (Phase-432): ASSET BUILT AND FROZEN

The Asset A build under Spec 045's frozen §§2–3 contract, quoted
verbatim in Spec 069 (Spec 069 freeze digest 657b930c…; freeze PR #338
merged at ba61d9cd; OSF registration r3xqb filed at the freeze,
pending the owner's approval act at the time of the run). Gates A1–A6
in order, all PASS, before any join: A1 the CISI volumes (vols. 1–2,
1991) and Parpola's published identifications in hand and named by
edition — the CISI sign list entered through the held mayig CISI
digitization, restored from the public upstream at commit ad2f1e2
after the programme's downloads copy was found missing during a
concurrent workspace sweep (spot values agree across the loss);
Parpola 2010 consulted in held form, its numbers not keyable to the
crosswalk's sign keys, so agreement is single_source throughout and
no row is contested — recorded openly in the build record. A2 the
D-18 input re-asserted as Spec 046's terminal empty feed
(concordance-297.json, SHA-256 772db4df…, signs empty, IDENTIFICATION
FAILED closure); the build proceeded without the feed and did not
reconstruct it. Blind double entry with reconciliation: 187 rows
over the full pinned-crosswalk universe (crosswalk SHA-256
4ace1a61…, 205 rows / 187 distinct sign keys) — animal 20, sky_cycle
0, object_goods 14, human 25, other 127, contested 0, unidentified 1
(M059: no governing identification in any held §2.3 source; sources
searched recorded). Four borderline rows (P073, P074, P217, P320).
Asset A SHA-256
952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b,
published as the spec's first product in
specs/069-hunt-asset-a/asset-a/ (canonical CSV, asset-a-freeze.json,
entry log entry-decisions.json); it is the asserted step-0 input of
Specs 070 and 071. The zero sky_cycle count is a fact about the held
published identifications of this universe, recorded as it landed.
Deterministic (second run byte-identical); anchors byte-identical
before and after (df0cf620…). Foundation check on the execution
tree: 40 passed / 0 failed / 8 warnings. Records:
specs/069-hunt-asset-a/outcome.md, build-record.md,
reports/phase432_results.json, reports/phase432_report.md.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.
## 2026-10-12 — Plain-language pass, phase 1 (owner directive)

At the owner's direction (2026-10-12: all papers, analyses, and
documents in plain language — easy for a general reader, still
scientifically accurate), a language-only pass was applied to the
program's living prose documents on branch
`plain-language-phase1`: docs/research/ DECIPHERMENT_DOSSIER_v1,
DECIPHERMENT_LIMITS, STRUCTURAL_MODEL, BASELINE_COMPARISON,
CORPUS_DEFINITION, SIGNAL_STATUS, SIGN_INVENTORY,
REPRODUCIBILITY_PROTOCOL, NORMALIZATION_RULES (explanatory prose
only — no rule statement changed), CORPUS_EXPANSION_LEADS, and
the unpublished v5 addendum draft
(glossa-corpus/indus/pierson_2026_indus_decipherment_addendum_v5.md).
Method: jargon replaced where a plain word carries the same
meaning; irreplaceable technical terms defined in plain words at
first use. No number, verdict, claim, or conclusion was changed.
Frozen material was not touched: the v3/v4 preprints and their
DOIs, the numbered program notes, ledgers and registers, claim
records, and run reports. Full inventory and classification:
~/workspace/your_files/2026-10-12-plain-language-inventory.md.

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution §VI.

## 2026-10-22 — Spec 072 EXECUTED (Phase-431) — held under the Roif gate

Spec 072 (Phase-431) was executed on 2026-10-22 under its frozen
contract (freeze digest
3925f365bdc452031bb7356f9b357c6d5068da4a835afcfd75b0e9ffa3a69e92; freeze
PR #341 merged at 862f56d8; OSF registration tc8ey). Under spec §7
limit 1 (the Roif gate), this study is named in programme reporting
only as: **executed — held under the Roif gate**, without result
content, until Roif 2025a + 2025b are cited and the owner clears the
specific publication act. Records:
specs/072-fish-family-profiles-redesign/outcome.md,
reports/phase431_report.md, reports/phase431_results.json — all held
in the same form.

**Redaction — 2026-10-25.** This entry formerly carried the study's
full result content. It was reduced to the permitted form above on
2026-10-25 under the owner's realignment decision
(docs/decisions/2026-10-25-realignment-decision.md; red-team finding
RT-26), by the same act that reduced the outcome record, the phase
report and machine record, the claim append, the experiment-graph
description, and the held insert file. Git history retains the
original text of this entry; no history purge has been authorised or
performed. A superseding entry recording the act stands at the end of
this ledger under 2026-10-25.

AI disclosure: executed by an AI agent (Muse, via Muse) at the direction of Tristen Pierson, per
constitution sec.VI.


## 2026-10-22 — Spec 070 EXECUTED (Phase-433): CLOSED AT STEP 0 — POPULATION NOT KEYED

The opening-signs successor on Shakti, under its frozen contract
(Spec 070 freeze digest 763108f8…; freeze PR #340 merged at 1213029d;
OSF registration nghs5 filed at the freeze, pending the owner's
approval act at the time of the run). Step-0 gates in order: 0.1
Asset A asserted PASS (Spec 069's executed record; canonical CSV
recomputes to 95231935…; per-kind counts match); 0.2 the Shakti
intake reproduced under P-F1 S1/S2 PASS (hashes recompute; census
5,704 rows, 5,536 analyzable, grades 3,212/2,087/405, 4,904
CISI-carrying, all recounted from the files); 0.3 input integrity
PASS. At 0.4 the section 2 battery over the 3,212 documented-lineage
rows classified 220 signs (TERMINAL_STRONG 42, MEDIAL_STRONG 81,
TERMINAL_MODERATE 37, INITIAL_STRONG 31, INITIAL_MODERATE 6, MIXED
23) and the opening-strong set — 31 signs — was enumerated in full
in Wells space and published (hash recorded before any join; no
join quantity exists in the record). Keying under the freeze-fixed
route (DD-070-9) resolved 26 of the 31; five could not be keyed —
ICIT 136, 298, 401, 617, 824: no parpola_1982 registry row carries
their Wells ids (verified independently: no registry row in any
numbering system carries W136/W298/W401/W617/W824; the numberings
are genuinely different lists — Parpola 136 carries Wells W048|W049).
Under the disposition the freeze fixed in advance (DD-070-11, the
conservative branch), the execution closed as POPULATION NOT KEYED:
no join performed, no test quantity computed, claim
without_kings…_manual_003 stands as recorded (IN QUESTION), no dated
append made (the appends belong to the verdict classes). The answer
to Spec 049's question in re-scoped form is therefore not settled
by this execution, in either direction; a successor must first
repair the keying surface by a new freeze decision. Deterministic
(second run byte-identical); anchors byte-identical before and
after; foundation check on the execution tree 40 passed / 0 failed
/ 8 warnings. Records: specs/070-hunt-opening-signs-successor/
outcome.md, reports/phase433_results.json,
reports/phase433_report.md.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-22 — Spec 071 EXECUTED (Phase-434): STOPPED AT STEP 0, GATE 0.3 — INVALID

The sky-signs successor on Shakti, under its frozen contract (Spec
071 freeze digest c06a7a86…; freeze PR #343 merged at 161bbe0d; OSF
registration b62p4 filed at the freeze, pending the owner's approval
act at the time of the run). Step-0 gates in order: 0.1 Asset A
asserted PASS against the freeze-fixed pin source (Spec 069's
asset-a-freeze.json; canonical CSV recomputes to 95231935…; counts
match); 0.2 the Shakti intake reproduced under P-F1 S1/S2 PASS
(census recounted from the files); 0.3 input integrity PASS, but
coverage FAIL, and the run stops as INVALID in the gate's own
terms: of the 557 distinct signs occurring in the primary
population (3,212 documented-lineage rows; totals only counted at
the gate, no positional quantity taken), 285 carry exactly one
Asset A row under the shared keying route (DD-071-10) and 272 carry
none — 134 Wells ids with no resolution in the pinned registry's
parpola_1982 Wells map, and 138 resolving to registry signs
outside Asset A's 187-row crosswalk universe; every uncovered sign
is listed in the machine record with its total and reason. The
gate's rationale is the design's: an absent row is never treated
as non-celestial by default, because that default would silently
define the comparison class. Gates 0.4/0.5 were not reached; no
final-position quantity was computed; no verdict is recorded; the
claim without_kings…_manual_004 stands UNTESTED as recorded and no
dated append is made (the appends belong to the verdict classes).
Recorded adjacently, as a fact of the frozen asset rather than a
second outcome: the celestial class is empty in Asset A (zero
sky_cycle rows), so a coverage repair alone would have met gate
0.4's TOO THIN floor (0 of 30 occurrences). Deterministic (second
run byte-identical); anchors byte-identical before and after;
foundation check on the execution tree 40 passed / 0 failed / 8
warnings. Records: specs/071-hunt-sky-signs-successor/outcome.md,
reports/phase434_results.json, reports/phase434_report.md.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-23 — Preprint v8: F2 Zipf qualification + Spec 068 integration; Spec 072 insert held

Preprint v8 (branch preprint-v8-f2-spec068; version note:
specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md)
resolves the spec-025 audit's F2 finding (the §2.1 Zipf exponent ~1.7
printed without a checkable derivation; adversarial pass 2026-10-22,
SUSTAINED in narrow form) by the qualify-in-place branch of its
recommendation — the add-the-derivation branch was not honestly
available, because the only derivation on record (−1.7046,
Sproat-benchmark script) belongs to a different corpus (7,138 texts /
24,502 tokens / 649 types) than §2.1's Holdat corpus. §2.1 now presents
the exponent as the program's own uncheckable corpus statistic, no
longer as evidence the script is a language, citing Yadav et al.
(2010) and its own stated limit; the Yadav entry is added to §8 after
Wells & Fuls (no other §8 entry touched; both Rao entries and both
Roif entries byte-identical). New §2.1.1 reports the Spec 068
(Phase-430; OSF 3pbwe) registered frequency-curve test on the Shakti
corpus (α = 2.004, error 0.1584 documented-lineage; α = 1.96, error
0.1544 documented + corroborated; Linear B, the one certain writing
system among the controls, fitted worst at 0.9229) with its
registered outcome wording: COMPARISON UNINFORMATIVE. §3.10 applies
the same qualification to Nair's Zipf slope. Everything else is
carried from v7 intact, including all Roif credit (§§3.5/3.19/§7/§8);
§3.32 remains absent and its restoration draft held. The Spec 072
(Phase-431) fish-family result is NOT integrated: its insert is filed
HELD at glossa-corpus/indus/pierson_2026_indus_decipherment_spec072_insert_HELD.md
(publication requires Roif 2025a/b citation AND owner clearance of
the specific act; claim F072-C14). PDF regenerated (TinyTeX XeLaTeX,
two clean passes, zero errors, 19 pages; SHA-256
0f70dece76d3cdd31fa2ccb5c9fdbc9c2953587a9895700b8cf4632cd81f6670),
all v8 changes verified in the rendered output (E1 wording, §2.1.1
figures and UNINFORMATIVE, Yadav entry, Roif entries, "End of
Preprint v8"; no betweenness, no §3.32). An independent red-team
pass on v8 is IN PROGRESS under the standing rule (no paper
publishes without TeX + a red-team pass); its record will be filed
in the audit directory when complete. Nothing submitted.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-23 — Preprint v8 red-team round 1: adjudicated and revised (R-01..R-45)

The independent red-team pass on preprint v8 ran as round 1 (attack:
independent engine, full text ×3 passes, 241 raw findings aggregated
to 125 items; adjudication against primary records: 44 sustained /
76 sustained in part / 3 not sustained / 2 moot). All adjudicated
replacement blocks R-01..R-45 were applied verbatim to
glossa-corpus/indus/pierson_2026_indus_decipherment.tex (revision
commit 8a9e80cf; §6 data-availability commit string pinned to that
commit by pin-only commit dba6d486). Corrected anchor arithmetic
(6,369 of 7,002; HIGH 70.34%); INCONCLUSIVE verdicts restored in
§§3.11/3.13; Phase-107 SA held-out failure disclosed in §2.4; 79.8%
aggregate and 6,869/47 mining counts withdrawn as evidence; §2.1.1
exponent non-comparability guard added. The Phase-109 re-based
anchor numbers were NOT substituted (owner's decision, per
adjudication §D item 2). Protected Roif/Rao text byte-intact; §3.32
still absent; no betweenness. PDF rebuilt with TinyTeX XeLaTeX, two
passes, exit 0, zero errors/warnings, 23 pages, SHA-256
1ef5eb721f4b9cdd7fc4f1afbe790793cd2c0ba74d48898c0331a0ae0309d2b0,
render-verified (pdftotext). Still open: Holdat corpus release; SA
re-base (owner); DEDR 135 (M176) / 4988 (M261) verification (repo
records conflict — audit tables blank, Phase-132 V08 asserts both);
red-team round 2 pending. Record:
specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md.
Nothing submitted, deposited, or published; PR #353 not merged.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-23 — Preprint v8 red-team round 2: adjudicated and revised (R2R-01..R2R-58)

Round 2 of the independent red-team pass on preprint v8 (attack:
independent engine, full text ×4 passes, 207 raw findings aggregated
to 58 items + positives; adjudication against primary records:
28 sustained / 29 sustained in part / 0 not sustained / 1 moot;
positives P1–P5 all confirmed). All adjudicated replacement blocks
R2R-01..R2R-58 were applied verbatim to
glossa-corpus/indus/pierson_2026_indus_decipherment.tex (57 blocks
with replacement text; R2R-06 moot) — revision commit 2d26b929; §6
data-availability commit string pinned to that commit by pin-only
commit d39f75f0. Corrected permutation parenthetical at all three
locations (0.0005); Phase-134 inputs unrounded (z = 10.344); all
four sibilants PROVISIONAL_MEDIUM everywhere; SA-affected count and
85.28% bound printed; Phase-107 "pre-registered" replaced by the
Spec 005 wording; Gulf echoes cured; Phase-133 figures corrected
(43.5%); 19 blockers named in §3.29; §8 gains Sproat (2014) and
Rao et al. (2010) (additions only). Protected Roif/Rao text
byte-intact; §3.32 still absent; no betweenness; Spec 072 insert
still HELD. PDF rebuilt with TinyTeX XeLaTeX, two passes, exit 0,
zero errors/warnings, 27 pages, SHA-256
8d0d676eee187de71ad268c6ff374b9d6d6e8a788582552f366e9dc59365ddd0,
render-verified (pdftotext); printed word count 14,370 measured on
the shipped PDF by the adjudicated command (pre-revision figure
10,837). Still open: Phase-132 V03 motif counts vs §3.4 printed
counts (deliberately out of R2R-26's scope; reserved for round 3);
§3.19 combined-figure cross-reference (no replacement prescribed;
flagged for round 3); Holdat release, SA re-base, DEDR verification
(owner decisions); red-team round 3 pending. Record:
specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md.
Nothing submitted, deposited, or published; PR #353 not merged.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-23 — Preprint v8 red-team round 3: adjudicated and revised (R3R-01..R3R-X3)

Round 3 of the independent red-team pass on preprint v8 (attack:
independent engine, GPT-5.5 via OpenAI API, full text ×4 passes,
116 raw findings aggregated to 53 items + 4 adjudicator-only
probes + 36 positives; adjudication against primary records:
12 sustained / 32 sustained in part / 9 moot of 53; probes
R3X-1/R3X-2/R3X-3 sustained, R3X-4 not sustained; positives 36/36
confirmed). All adjudicated replacement blocks R3R-01..R3R-X3
(47 blocks) were applied verbatim to
glossa-corpus/indus/pierson_2026_indus_decipherment.tex (MOOT and
not-sustained items have no replacement; R3R-23/42/46 disclosures
stand) — revision commit 196ea0a2; §6 commit string pinned to
that commit by pin-only commit 20463bd9. §3.4 prints the
Phase-132 V03 motif table (147/78/43…) beside χ² = 12.98; §3.8
prints the true top five (M060/M045/M016/M067/M039); §3.19 free
of the combined 0/140; §3.27 free of "Formal cross-validation"
and of the SUPPORTED verdict label; §4.4 SA item aligned to
§2.4; §3.3 prints the M342/M176/M261 HIGH basis. Protected
Roif/Rao text byte-intact; §3.32 still absent; no betweenness;
Spec 072 insert still HELD. PDF rebuilt with TinyTeX XeLaTeX,
two passes, exit 0, zero errors, 30 pages, SHA-256
ddf71f1db2f6655c651420a7c103e0492c9325e5a0fa36d8019173206dd1934d,
render-verified (pdftotext); printed word count 17,016 measured
on the shipped PDF by the adjudicated command (round-2 figure
14,370). Still open: the §D owner decisions (Holdat release,
calibration, SA/V07 re-base, rival comparisons, Zenodo archive)
and the §E record gaps; red-team round 4 pending. Record:
specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md.
Nothing submitted, deposited, or published; PR #353 not merged.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-23 — Preprint v8 red-team round 4: adjudicated and revised (R4R-01..R4R-21)

Round 4 of the independent red-team pass on preprint v8 (attack:
independent engine, GPT-5.5 via OpenAI API, full text ×4 passes,
85 raw findings aggregated to 38 items + 68 positives; adjudication
against primary records: 8 sustained / 9 sustained in part / 20 moot /
1 not sustained of 38; positives 68/68 confirmed; settlements
S1–S5). All adjudicated text-bearing replacement blocks
R4R-01..R4R-21 were applied verbatim to
glossa-corpus/indus/pierson_2026_indus_decipherment.tex (MOOT items
and R4-17 not sustained have no replacement; R4R-16 is a class (c)
record gap with no text; class (b) owner decisions not taken,
interim text only) — revision commit ba5b4bf9; §6 commit string
pinned to that commit by pin-only commit 0bf385b4. R4R-01
re-describes the fish-sign isolation result at all eight locations
at UNTESTABLE / no-single-sign-inscriptions strength (the corpus
contains no single-sign inscriptions at all, Phase-134 F9);
§3.16 sibilant count corrected (6 for the 157-set, 10 current);
§3.11 markers corrected to 35/161 (21.7%), 0/161 stands; §1.3 S12
wording aligned with §3.30; §2.2 gains the HIGH-rule limit
sentence. Protected Roif/Rao text byte-intact; §3.32 still absent;
no betweenness; Spec 072 insert still HELD. PDF rebuilt with
TinyTeX XeLaTeX, two passes, exit 0, zero errors, 31 pages,
SHA-256 ea924ec13f3e8a33fa7045bca386a5baed68bd94357800ceb339e6eedf38e942,
render-verified (pdftotext); printed word count 17,997 measured
on the shipped PDF by the adjudicated command (round-3 figure
17,016). Prescribed survivals flagged in the version note: 39/161
and 24.2% once each inside R4R-05's corrective sentence; three
block-standing "compound-only pattern" remainders. Loop NOT
closed at round 4 per adjudication §D. Still open: the §D owner
decisions and the §E record gaps (incl. R4-16's seven unrecorded
§8 identifications); red-team round 5 pending. Record:
specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md.
Nothing submitted, deposited, or published; PR #353 not merged.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-23 — Preprint v8 red-team round 5: adjudicated and revised (R5R-01..R5R-11)

Round 5 of the independent red-team pass on preprint v8 (attack:
independent engine, GPT-5.5 via OpenAI API, direct, full text ×4
passes, 94 raw findings aggregated to 38 items + 87 positives;
adjudication against primary records: 5 sustained / 6 sustained
in part / 25 moot / 2 not sustained of 38; positives 87/87
confirmed; settlements S6–S10). All adjudicated replacement
blocks R5R-01..R5R-11 were applied verbatim to
glossa-corpus/indus/pierson_2026_indus_decipherment.tex (formatting
conversion only; each target verified by exact match; MOOT and
NOT SUSTAINED items have no replacement; R5R-06's class (b)
corpus-release decision is the owner's and was not taken) —
revision commit 88a6bf46; §6 commit string pinned to that commit
by pin-only commit e585c767. Load-bearing cures: R5R-04 (§1.3 +
§6: the anchor table records a DEDR citation for 15 of its 161
rows in anchor_table.csv — 16 of 161 in ANCHOR_STATUS_AUDIT.csv,
per S8 — and the "with DEDR citations" claim is removed at both
locations); R5R-03 (§3.8, per S9: 63 pairs enriched at
single-cell contribution >1.0; exactly 14 at or above the
Bonferroni threshold χ²≈14.7 on that statistic, a conservative
comparison whose passes are valid for the full 2×2 statistic;
the Phase-149 "robust" definition corrected to C2's subtraction
estimate (~43 = 63 − 19.7); the 394 denominator's filters from
the Phase-143 script printed); R5R-01 (§6 pin explanation
corrected per S10); §5 Tier 2/Tier 3 defined (R5R-05); §5 lead
"reproducible" split (R5R-06); §4.5 Gulf scope aligned with
§3.19 (R5R-07); §3.28/§1.3 ICIT necessity claim replaced
(R5R-08); §2.3 semantic labels restated as interpretation
(R5R-09; §2.2's MEDIUM parenthetical left standing as a gloss
read with that cure); §2.2 ghost DEDR/Parpola criteria removed
(R5R-10); §2.3 z-score cross-reference corrected (R5R-02);
abstract subject restored (R5R-11). POST-PIN TRUTH CHECK
(flagged, not silently fixed): R5R-01's sentence as applied
names a92c53aa / ba5b4bf9 — true of the round-4 state the
adjudication examined, not of the final round-5 state (at the
named commit 88a6bf46 the §6 first sentence names ff9b9146, and
the shipped draft names 88a6bf46); the remainder of the
sentence is verified true (one differing sentence, only in the
commit string). Protected Roif/Rao text byte-intact (hash-verified
per passage against ff9b9146); §3.32 still absent; no
betweenness; Spec 072 insert still HELD. PDF rebuilt with
TinyTeX XeLaTeX, two passes, exit 0, zero errors, 32 pages,
SHA-256 969c45d8da58a110371fabdf48875641a466eb20daacec0a78b65efb3b2c7a1f,
render-verified (pdftotext); printed word count 18,591 measured
on the shipped PDF by the adjudicated command (round-4 figure
17,997). The "16 of 161" audit-file figure appears in the
adjudication and the version note, not in the PDF — no R5R
block prints it. Loop NOT closed at round 5 per adjudication
§D. Still open: the §D owner decisions, the §E record gaps
(incl. the new Phase-143 pair-list, DEDR-column-discrepancy and
Mitchell-search gaps), and the R5R-01 residual above; red-team
round 6 pending. Record:
specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md.
Nothing submitted, deposited, or published; PR #353 not merged.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-23 — Preprint v8 red-team round 6: adjudicated and revised (R6R-01..R6R-10)

Round 6 of the independent red-team pass on preprint v8 (attack:
independent engine, GPT-5.5 via OpenAI API, direct, four passes,
84 raw findings aggregated to 39 items + 74 positives, plus a
14-sentence §6 line-by-line audit; adjudication against primary
records: 5 sustained / 4 sustained in part / 28 moot / 2 not
sustained of 39; positives 74/74 confirmed; settlements
S11–S18). All adjudicated replacement blocks R6R-01..R6R-10 were
applied verbatim to
glossa-corpus/indus/pierson_2026_indus_decipherment.tex
(formatting conversion only; each target verified by exact
match; MOOT and NOT SUSTAINED items have no replacement;
R6R-06's owner-confirmation fallback not invoked — the
adjudicated text was applied) — revision commit b28cf2f5; §6
commit string pinned to that commit by pin-only commit
81a37e06. Load-bearing cures: R6R-01 (§6 pin replaced with the
purely procedural form naming no historical commit, per S11 —
post-pin clause-by-clause truth check passes in full: named
commit b28cf2f5 is the revision commit, its parent is dff001c7
which its §6 copy names, the revision→pin diff is one line and
one string only in both the .tex and the rendered text, and the
records commits change no paper text); R6R-02 (the three DEDR
counts distinguished at §1.3, §2.4 and §3.27, per S12 — no
number changes); R6R-03 (§6 anchor table described as its 397
rows, per S13); R6R-04 (§6 selected-rows sentence corrected,
per S14); R6R-05 + R6R-06 (§8 gains Jha & Rajaram (2000) only;
§3.28 aligned to Parpola, Parpola & Brunswig 1977, per S15);
R6R-07 (Appendix C Phase-44 ratio stated as 3.1334, a ratio of
two lifts 0.4965 / 0.1584, with the §2.4 limit, per S16);
R6R-08 (§3.23 span 1972–2018, 46 years); R6R-09 (Phase-134
cross-reference to §2.3 only); R6R-10 (§3.7 PMI denominator
5,332 printed; 2.43 recomputes, 2.432). Protected Roif/Rao text
byte-intact (§8 identical apart from the Jha addition); §3.32
still absent; no betweenness; Spec 072 insert still HELD. PDF
rebuilt with TinyTeX XeLaTeX, two passes, exit 0, zero errors,
32 pages, SHA-256
48dfb48ed0d860af64c8d74786b79638dc8cd6185c491c2df2f76efe57a3a69b,
render-verified (pdftotext); printed word count 19,011 measured
on the shipped PDF by the adjudicated command (round-5 figure
18,591). Loop NOT closed at round 6 per adjudication §D. Still
open: the §D owner decisions (incl. the R6R-06 confirmation if
a distinct 1975 Parpola source is identified), the §E record
gaps (incl. the DEDR-column discrepancy / per-sign DEDR
provenance and the title-level Phase-167 Parpola identity);
red-team round 7 pending. Record:
specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md.
Nothing submitted, deposited, or published; PR #353 not merged.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-23 — Preprint v8 red-team round 7: adjudicated and revised (R7R-01..R7R-04)

Round 7 of the independent red-team pass on preprint v8 (attack:
independent engine, GPT-5.5 via OpenAI API, direct, four passes,
93 raw findings aggregated to 40 items + 48 positives, plus a
16-item §6 line-by-line audit; adjudication against primary
records: 3 sustained / 1 sustained in part / 34 moot / 2 not
sustained of 40; positives 48/48 confirmed; settlements
S19–S22). All adjudicated replacement blocks R7R-01..R7R-04 were
applied verbatim to
glossa-corpus/indus/pierson_2026_indus_decipherment.tex
(formatting conversion only; each target verified by exact
match; MOOT and NOT SUSTAINED items have no replacement) —
revision commit 649e0e75; §6 commit string pinned to that commit
by pin-only commit 9133db8f. Cures: R7R-01 (§3.7, §3.12 and §3.28
cluster population stated as the population the Phase-148 record
groups — the 97 INITIAL-sign clusters partition all 1,670 seals
by first sign alone, not the 1,165 fully H+M-covered seals of
§3.6, per S19; no number changes); R7R-02 (§3.28 Phase-167 record
path made breakable at its slashes; verified on the rendered
page 23 — the full path and its closing parenthesis print inside
the text block, nothing clipped); R7R-03 (§2.1 "primary published
formal-seal assemblage" superlative replaced by the corpus's
printed scope, the share of the full published assemblage stated
as not measured); R7R-04 (§3.13 prints the Phase-150 permutation
seed, 42, fixed in its script). Settlements: S19 (population
label sustained, class (a)); S20 (§6 line-by-line audit NOT
SUSTAINED — all 16 clauses verified true against the completed
round-6 pin cycle; the R6R-01 procedural form's first full test,
passed; this round §6 was not touched except its pin string, and
the post-pin clause-by-clause check against the round-7 graph —
revision 649e0e75, its §6 copy naming its parent 36e8c7ad, pin
9133db8f one line / one string in both .tex and rendered text,
records commits changing no paper text — passes in full); S21
(Tier-2 sentence MOOT against its own definition and the body's
adverse results); S22 (§5 "favours" MOOT, seventh airing, prior
rulings upheld). Protected Roif/Rao/Jha & Rajaram text
byte-intact (§8, §3.5/§3.19 Roif credit, §7 acknowledgment
identical — the .tex diff touches only §2.1, §3.7, §3.12, §3.13,
§3.28, §6's pin string and the word-count line); §3.32 still
absent; no betweenness; Spec 072 insert still HELD. PDF rebuilt
with TinyTeX XeLaTeX, two passes, exit 0, zero errors, 32 pages,
SHA-256
5335cdaba21c88c7ae6b56a75e5ec0f1a4db109ad480e57c652568709920b035,
render-verified (pdftotext + rendered-page inspection of p. 23);
printed word count 19,193 measured on the shipped PDF by the
adjudicated command (round-6 figure 19,011). Loop NOT closed at
round 7 per adjudication §D. Still open: the §D owner decisions
(incl. the R6R-06 confirmation if a distinct 1975 Parpola source
is identified), the §E record gaps (incl. the per-cluster fully
H+M-covered breakdown no record reports, extended at §E.11);
red-team round 8 pending. Record:
specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md.
Nothing submitted, deposited, or published; PR #353 not merged.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.

## 2026-10-23 — Preprint v8 red-team loop CLOSED at round 8; closure records filed

Round 8 of the independent red-team pass on preprint v8 (attack:
independent engine, GPT-5.5 via OpenAI API, direct, four passes,
80 findings plus 44 positives, including a §6 line-by-line audit;
adjudication against primary records, commit c8cea1d6):
SUSTAINED 0 / SUSTAINED IN PART 0 / MOOT 38 / NOT SUSTAINED 2 of
40 aggregated items (R8-01..R8-40); positives 44/44 confirmed;
settlements S23 (§6 audit — all 16 clauses verified true against
the completed round-7 pin cycle) and S24 (title word
"Falsifiable"; owner decision R3-14 stands). §B of the round-8
adjudication is empty — no R8R replacement texts, no revision
act; the round-7-revised paper text stands unchanged. The loop
CLOSES at round 8 per the adjudication's §D closure statement:
the loop's test was the paper's text against its records, and a
full independent pass finds no statement the records contradict
and no claim worded beyond its printed disclosures. Closure is
not a claim the decipherment is correct; the §E record gaps
stand exactly as filed, and the owner decisions stand with
their interim cures in place. Final state: 32 pages, PDF
SHA-256
5335cdaba21c88c7ae6b56a75e5ec0f1a4db109ad480e57c652568709920b035,
word count 19,193 (pdftotext | wc -w, verified on the shipped
PDF), §6 pins revision commit 649e0e75. This entry, the
version note's "Red-team loop closure (2026-10-23)" section
(full round-by-round ledger, rounds 1–8), and the AGENTS.md
preprint "Current version" update are records only — no paper
text changed. Protected text byte-intact; §3.32 still absent;
Spec 072 insert still HELD. Standing gates: the owner's read of
this build; deposit executed separately by the owner. Nothing
submitted, deposited, or published.

AI disclosure: executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.
## 2026-10-23 — Spec 073 EXECUTED (Phase-436): REPAIRED WITH NAMED SHORTFALL

The keying-surface repair is built and measured. Registry v2
(data/crosswalks/canonical_sign_registry_v2.csv, SHA-256
42ab09fb...) carries all 803 v1 rows byte-identical and adds 210
icit_wells rows (sign ids W136-form), each cited to the published
ICIT sign list in Fuls 2023, *A Catalog of Indus Signs*, Ch. 2.3
(consulted from the held print PDF on the owner's desktop; the
change schedule is at specs/073-keying-surface-repair/registry-v2/).
No Wells-map completions were added: the Catalog's Parpola column
states Parpola (1994)'s own numbering, not the registry's, so it
grounds no completion (catalog-consult.json holds the evidence).
Asset A v2 (SHA-256 681e017d...) carries all 187 v1 rows
field-for-field and adds 365 rows entered blind under the Spec
045/069 discipline — the deterministic second pass was first
required to reproduce Spec 069's recorded pass-2 codings on all 187
carried labels exactly (0 misses). Coverage over the recorded
populations, counts only: Spec 070's 31-sign set now keys 31 of 31
(baseline 26 by resolution), Spec 071's 557-sign documented set now
keys 556 of 557 (baseline 285). The five named signs (ICIT 136, 298,
401, 617, 824) are each resolved and keyed; none carries a verbal
depiction in any ruled source, so each is coded unidentified —
keyed for joining, honestly unclassified. Named shortfall: token
999, a corpus placeholder occurring in the documented stratum but in
no published sign list — NO PUBLISHED IDENTITY, named on the
schedule, never dropped. The celestial class in Asset A v2 is 0
rows (carried 0, new 0), stated beside Spec 071's frozen TOO THIN
floor of 30. Closing re-assertion: Registry v1 (8a0b2a82...) and
Asset A v1 (95231935...) re-hashed at the close and byte-identical.
Neither predecessor study is re-run or amended; both Hunt claims
stand untouched; whether either Hunt question is re-frozen against
the repaired surface is a separate owner decision. Freeze digest
5419c4c4...; OSF registration https://osf.io/9kh4a/ (approval
pending at this entry's writing). Records:
specs/073-keying-surface-repair/outcome.md,
reports/phase436_results.json, reports/phase436_report.md.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.
## 2026-10-24 — Spec 041 EXECUTED (Phase-435): site-period mapping built for the ICIT-lineage layer (horus84)

The mapping the Spec 040 chronology-control dependency was waiting on now
exists as a pinned artifact. Step 0 passed all six frozen gates on the
hash-pinned layer (5,679 rows; census margins reproduced exactly: period
2,266 / phase 2,638 / both 1,788 / union 3,116 / neither 2,294; the
Phase-139 covariates agree on all 5,410 population rows; anchors
df0cf620... asserted byte-identical before and after). Of the 78 local
chronological labels attested on the population, 24 cells are MAPPED on a
published determination verified to the spec section 3 bar (4 EARLY, 18
MATURE, 2 LATE; artifact
data/evidence_integration/site_period_mapping.jsonl, SHA-256
1e5b54c9...) and 54 are UNASSIGNED with an enumerated reason (35 no
published determination, 10 determination unverified, 4 boundary spans,
3 labels uncertain in the layer, 2 not in the published scheme); 0 cells
are CONTESTED. Dual verification re-read every grounded cell at its
locator: 23 confirmed, 1 confirmed with a recorded caveat, and 4 Harappa
phase cells (A, C, A-C, B/C) reclassified to UNASSIGNED /
DETERMINATION_UNVERIFIED — never edited into agreement. Placement counts
are reported under all four candidate derivations, none adopted (A1
1,457 · A2 780 · B 1,366 · C 1,457 of 5,410 rows; at most 3,116 rows,
57.6%, carry any label at all; Mohenjo-daro places zero rows under every
derivation). One recorded departure from the freeze's illustrative text:
Nausharo Period IV is MAPPED MATURE on the excavator's own published
scheme (Jarrige et al. 2011, pp. 9, 30), which the freeze example had
followed an incomplete consultation in expecting to be absent. This act
computes no G1 quantity, amends no frozen record, and does not satisfy
Spec 040's gate by existing — that judgment belongs to a future
Spec 040 freeze. Freeze digest fe618886...; OSF registration
https://osf.io/w2vkn/ (approved 2026-10-23). Records:
specs/041-site-local-label-period-mapping/outcome.md,
specs/041-site-local-label-period-mapping/coverage-report.md,
reports/phase435_results.json.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-24 — Spec 052 EXECUTED (Phase-437): battery NB-1 on the Shakti layer (CISI-compilation lineage) — INCONSISTENT

The amended D-01 arm A the parent claim's contradicted verdict
carried as its open caveat is now executed. Step 0 passed all four
amended gates, in order, fail-closed: the corpus pin recomputed
exactly (corpus 345241b1...; row grades 02394241...; restricted-local,
read in place, never in git); the primary population reproduced the
freeze-recorded counts exactly (3,045 rows / 11,805 tokens / 557
signs; sensitivity 5,131 / 17,216 / 707); the battery run twice under
seed 43052 produced identical outputs; thinness cleared (2,068
sequences of length >= 3; 90 classifiable signs). Battery NB-1 as
frozen: condition F (dedicated final sets) HOLDS — 7 TERMINAL_STRONG
signs (034, 413, 501, 503, 692, 817, 820) against a permutation-null
chance level of 0 (999 within-sequence permutations; null
min/median/max 0/0/0) — and condition O (opening formula) HOLDS —
the opening bigram (400, 740) recurs 179 times over B = 2,942
(dominance 0.0608) against a chance level of 76 (null 64/68/84).
Both conditions hold, so under the amendment's re-pointed semantics
the outcome is INCONSISTENT: the Farmer pattern is absent in this
compilation and the "artefact of the Soviet dataset" caveat widens.
The sensitivity population, reported with the same prominence,
returned the same word: INCONSISTENT (9 TERMINAL_STRONG against a
chance level of 0; (400, 740) 235 times over B = 4,293 against a
chance level of 95) — the outcome is not grade-sensitive. One
census note, recorded openly in the step-0 record: the freeze
census's 112 sensitivity-classifiable signs counted total
occurrences; under NB-1 (length-1 sequences enter no count) sign
540 has N = 13 and the count is 111 — no gate turns on it, and the
primary count (90) agrees under both readings. The outcome was
appended in the same words to the parent claim's record and to all
three fragments' records (purely additive); the parent claim
farmer_sproat_witzel_2004_manual_001 stands contradicted exactly as
recorded — this outcome moves no verdict and is not a verdict on
the Farmer–Sproat–Witzel thesis. Anchors df0cf620... asserted
byte-identical before and after. Freeze digest 83658949...; OSF
registration https://osf.io/7cu23/ (approved 2026-10-24). Records:
specs/052-farmer-not-writing-soviet/outcome.md,
specs/052-farmer-not-writing-soviet/step0-record.md,
reports/phase437_results.json, reports/phase437_report.md.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-24 — Spec 054 EXECUTED (Phase-438): Yadav's opening/closing signs under battery NB-1 — STRICT CORPUS NOT PINNABLE at gate G2

The amended falsifier act is now executed. Step 0 ran in the
amendment §6 order, fail-closed: gate G1 (pin checks) PASS — every
freeze §2 pin recomputed (the claim store after the falsifier
append at 938174b0...; the Phase-43 record at 78a6c219...; the
positional companion at 0e546962...; crosswalk v1 JSON/CSV at
4e7559df.../3d0b9ef1...; the anchors at df0cf620...; the recovered
register at ea161e47...) and the freeze digest re-asserted
(d85f6ace...). Gate G2 (strict corpus identification and pin)
FAILED on observed values: the V3 loader's data file — the
Firestore 'indusarrays' dump the pinned Phase-43 record names as
its corpus's source (T1_1: 3,916 records / 2,665 dockeys / 3,137
sequences / 12,494 sign instances) — is absent at its path in the
execution tree, in the main checkout, and in every sibling tree
scanned (9 candidate paths), so the loader loads zero records and
zero sequences and the layer cannot be exported or pinned; no
database copy of the layer exists (the programme database's only
Indus text is the synthetic prototype); and every other layer held
was censused and is a different corpus or lineage (the
site-attributed yajnadevam layer at 5,679 records; the V1 research
export at 15,508 records; the mayig CISI layer at 179 / 1,003 /
182; the Holdat downloads layer at 1,670 / 7,002 / 390 — arm 2's
own layer; the Shakti layer at 5,704 rows), so none was
substituted. Gates G3 (thinness), G4 (second arm) and G5
(determinism) were NOT REACHED; no positional quantity was
computed in either arm, no strong set was produced, and the
amended statement stands untested. The outcome was appended as a
dated entry to the record of yadav_2009_arxiv_manual_002
(spec054_outcome_append_2026_10_24; the store moved 938174b0... ->
21009b4a... by exactly that entry; durability proven by
regeneration in a scratch tree — the entry and the falsifier both
survive verbatim). The claim stands exactly as recorded: strongly
supported, stage explained, with the falsifier appended at this
spec's freeze — this closure moves no status and is not a verdict
on Yadav et al. (2010)'s statement or on the amended one. The
same observed facts closed Spec 053 (Phase-413) at its gate 0.3
on 2026-10-21. Anchors df0cf620... asserted byte-identical before
and after. Freeze digest d85f6ace...; OSF registration
https://osf.io/8spvf/ (approved 2026-10-24). Records:
specs/054-yadav-opening-closing/outcome.md,
specs/054-yadav-opening-closing/step0-record.md,
reports/phase438_results.json, reports/phase438_report.md.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-24 — Spec 040 EXECUTED (Phase-439): D-25 G1 chronology-controlled rerun — NOT-YET-TESTABLE at the section 5 margins gate

The chronology-controlled rerun of G1 is now executed under the
frozen contract (freeze digest 16aeeb70...; OSF registration
https://osf.io/2rgtb/, approved 2026-10-24). Step 0 ran in order,
fail-closed, and PASSED all three gates: pin verification (every
freeze section 3 pin recomputed — the accepted Spec 041 artifact
at 1e5b54c9..., its meta and step-0 census, Spec 039's artifact at
64f288d3..., the Phase-139 covariates at a0f0d05a..., the spine at
9dc2fba5..., the anchors at df0cf620...; the freeze record
replays; the ICIT-lineage layer (horus84) asserted at c368f290...
before any use); population reproduction and the section 4.1 join
under derivation A1 (5,410 rows; covariates in agreement with the
layer on every row; the join yields exactly one assignment row
per inscription ID and reproduces the freeze counts exactly —
1,457 placed: EARLY 32, MATURE 1,386, LATE 39; 3,953 unplaced);
and determinism (the record computed twice, identical; two venue
runs byte-identical). The section 5 margins gate then FAILED on
arms 1 and 2 and passed arm 3: EARLY retains assigned
inscriptions from 1 distinct site (Harappa) and LATE from 2
(Dholavira, Lothal) against the 5-site arm (MATURE retains 5);
the unassigned share is 73.1% against the 40% arm; permutable
inscriptions under the primary strata number 1,205 against the
1,000 arm (DD-040-6 retained). The execution closes
NOT-YET-TESTABLE (DD-040-5): no profile table, no permutation,
and no interval was computed, and the section 7 regression, the
section 6 primary, and the section 8 sensitivities were not
reached. No consequence arises for G1: STUDY-SPEC-025/G1 stands
exactly as Spec 025 and Phase-385 left it — SUPPORTED under
composition and preservation control, governing basic interval
[0.1838, 0.2102] against V = 0.10, with the standing rider
(chronology is NOT controlled in the primary test). This closure
is the outcome the freeze record forecast on the pinned counts;
the margins here were recomputed from those inputs at this run.
Anchors df0cf620... asserted byte-identical before and after; no
PRED contact. Venue note: the run's fresh git worktree was
reaped by the VM write restriction mid-run; the run executed in
a minimal tree assembled from origin/main via the API with every
input hash-verified at gate 1, and the record was landed through
the git-data API. Records: specs/040-d25-g1-chronology-controlled/
outcome.md, specs/040-d25-g1-chronology-controlled/step0-record.md,
reports/phase439_results.json, reports/phase439_report.md.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-24 — Spec 074 EXECUTED (Phase-440): Hunt's opening signs on the repaired keying surface — NOT SUPPORTED

Spec 074 — Spec 070's successor on the keying surface Spec 073 repaired —
executed under the owner's order of 2026-10-24 ("Shouldn't we do all three
of these?"), after OSF registration cfe7z was approved and public (DOI
10.17605/OSF.IO/CFE7Z; freeze digest 5416a0d3..., freeze PR #368 merged
c561f293; OSF record PR #371). All six step-0 gates passed, fail-closed in
the frozen order. Gate 0.4's reproduction assertion held exactly: the
enumerated population's canonical publication hash (30092b6f...) equals
Spec 070's recorded hash; the 31 opening-strong signs, their per-sign
I/M/T counts, and the full battery census (220 signs at the floor) all
reproduce Spec 070's recorded measurement. Keying under the frozen
two-leg route (DD-074-8) resolved 31/31: 26 signs under leg 1
(parpola_1982 wells_ids over Registry v2) and the five signs Spec 070
could not key — 136, 298, 401, 617, 824 — under leg 2 (Registry v2's
icit_wells rows) to their own W-keyed Asset A v2 rows, each classified
unidentified in the frozen asset (SHA-256 681e017d...; 552 rows; animal
30, sky_cycle 0, object_goods 22, human 43, other 246, contested 0,
unidentified 211): counted, listed, excluded from the primary's numerator
and denominator. Keying is not classification. The frozen section 4 test
then scored: the disjoint 2x2 over classified members is [[2, 24],
[6, 58]] — of the 31 opening-strong signs, 2 are animal signs (226 and
241, both fish), a share of 0.0769 against 0.0889 over the table's
classified universe; enrichment ratio R1 = 0.8654; Fisher exact one-sided
p = 0.7345 (two-sided 1.0). The reversed arm agrees in direction (R2 =
0.0: none of the comparison inventory's six animal signs is
opening-strong; the two animal signs in the population occur 21 and 10
times, below the inventory's 30-occurrence floor). Sensitivities: S-A
equals the primary (zero contested rows in Asset A v2); S-B is not
applicable (no Asset A v2 verbatim label identifies a unicorn — stated,
not assumed); S-C on the documented + corroborated population (O = 35,
U = 89) returns the same word (R1 = 0.8929, p = 0.7140), so the result is
not grade-sensitive. Verdict under section 4.3 rule 1, on both grounds
independently (R1 at or below 1.0; p at or above 0.05): NOT SUPPORTED —
the section 1.2 falsifier fires, and the animal half of Hunt's claim
(without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003) is
recorded not supported in its re-scoped form; the claim stands partially
supported on its positional half alone, stage explained, falsification
condition unchanged, via the dated append
spec074_outcome_append_2026_10_24. This is the first verdict the claim's
animal half has had in either direction — Spec 070 closed before
scoring, and its POPULATION NOT KEYED closure stands unamended beside
this outcome. Honesty fence: the test measures the claim against a
positional framework measured on the graded ICIT corpus, never against
the Phase-43 framework; lineage statement (P-F1 S3): this corpus is an
ICIT-lineage corpus, and agreement between it and the program's earlier
ICIT-lineage layer is consistency within one tradition, not independent
corroboration. Fence sentence: this result is about depiction and
position in recorded data; it is not evidence that any sign marked
identity, a guild, or goods. Spec 037's 49% cross-compilation label
caution travels with the result. Anchors df0cf620... asserted
byte-identical before and after; the results record is byte-identical
across two runs (SHA-256 d539519d...). Records:
specs/074-hunt-opening-signs-repaired-surface/outcome.md,
specs/074-hunt-opening-signs-repaired-surface/step0-record.md,
reports/phase440_results.json, reports/phase440_report.md.

AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.


## 2026-10-25 — Realignment: Spec 072 records redacted to the Roif gate's permitted form

Under the owner's decision of 2026-10-25 (criterion directed by the
owner: the option best suited to the success of the programme;
docs/decisions/2026-10-25-realignment-decision.md), the full
realignment package arising from the 2026-10-24 red-team attack is
approved, and its Item 1.1 is decided as option (a), REDACT. The
2026-10-22 Spec 072 entry above is reduced to the Roif gate's
permitted form, as are specs/072-fish-family-profiles-redesign/
outcome.md, reports/phase431_report.md, reports/phase431_results.json,
the spec072_outcome_2026_10_22 append on claim
parpola_2010_dravidian_solution_manual_002,
backend/glossa_lab/experiment_graph_phase431.py's recorded outcome
sentence, and glossa-corpus/indus/
pierson_2026_indus_decipherment_spec072_insert_HELD.md. The act is
recorded in full — surfaces, reasoning, sweep, and the standing
residual that git history retains the original text (no history purge
authorised or performed) — in the decision record. No verdict, claim
status, stage, or score is changed by this act.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.


## 2026-10-25 — Spec 062 EXECUTED (Phase-424): NO TARGET UNDER EITHER SCENARIO

Spec 062 — Spec 061's successor carrying construction R-1's repaired
calibration — executed under the frozen Spec 062 contract (freeze digest
1800de53...; freeze PR #307 merged 9e4e8ead; OSF registration 4m27t
approved and public, DOI 10.17605/OSF.IO/4M27T). Step 0 passed every
gate at two venues with byte-identical calibration records, including
the repaired gate 0.5-R: A_R strictly increasing on the scan grid
(A_R(1) = 0.00022759124836990718, A_R(3) = 0.028821884413380183);
Scenario 1 b* = 1.8665771484375 (|error| 8.22e-07), Scenario 2 b* =
2.2470703125 (|error| 1.68e-08) — the R-1 repair calibrates on the real
recorded population, where Spec 061's frozen calibration could not
impose either scenario value at all. Gate 0.3 reproduced the recorded
Arm A summary exactly (median adjusted R2 0.00878393455594817, interval
[0.004626892186724407, 0.01297407559730989], rejection share
0.6231155778894473). The grid then ran on the owner's desktop as two
detached checkpointed processes (launched 2026-10-22T09:24:18Z; all 25
checkpoints per scenario; both processes exited cleanly) and was
assembled on the desktop on 2026-10-25, its step-0 re-run again
digit-for-digit. No grid point inside the frozen search frame (integer
multiples m = 1..25; ceiling m = 25, added total 38,232; 199 trials per
point; a point qualifies at a resolving share of at least 0.80)
qualified under either scenario. The highest resolving share anywhere
is at m = 1: 0.0804 under Scenario 1 (16/199) and 0.1759 under
Scenario 2 (35/199); the next highest is Scenario 2 at m = 4, 0.1005.
Verdict under section 5: NO TARGET UNDER EITHER SCENARIO — the
falsifier's outcome, scoped to the frozen search frame (no grid point
inside the frame qualified; never that no amount of data could resolve
Arm A in principle). No intake target exists under this spec, no
operative target exists, and Spec 061's T* remains undefined on Spec
061's record. Spec 028 Arm A stands INCONCLUSIVE exactly as recorded.
Arm A2 was never armed, joined, or touched, and with no target
returned its trigger does not fire on this record — nothing about Arm
A2 may be claimed from it. Anchors df0cf620... asserted byte-identical
before and after. Records: specs/062-arm-a-precision-calibration-repair/
outcome.md, reports/phase424_results.json, reports/phase424_report.md.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.


## 2026-10-25 — Spec 075 EXECUTED (Phase-441): per-kind verdicts — other INCONCLUSIVE; human, animal, object_goods NOT SUPPORTED

Spec 075 — the depicted-kind endings atlas, this programme's own claim
family F075 (not Spec 071's retired question, not Hunt's claims in any
form) — executed under the frozen Spec 075 contract (freeze digest
aa06726f...; freeze PR #389 merged fd9bd448 on genuine CI including the
C4 freeze-gate-records check, this freeze being the designated C4
shadow freeze; OSF registration jv74f approved and public, DOI
10.17605/OSF.IO/JV74F), on the owner's execution order of 2026-10-25
(12:03 EDT). The celestial arm was reported first, as pre-registered:
the celestial class as frozen in Asset A v2 contains zero signs; there
is no celestial rate; the empty class is Spec 071's closing finding,
restated where a reader of an endings atlas would look for it, and it
establishes nothing new about sky signs. Spec 071's retirement stands
untouched and its claim UNTESTED. All six step-0 gates passed in order:
the asset pins against Spec 073's executed record; the Shakti intake
under P-F1 S1/S2; input integrity (crosswalk, Registry v1, anchors);
the primary population reproduced exactly (3,045 analyzable
documented-lineage rows, 557 distinct signs, 550 in sequences of length
>= 2 — the spec's flagged replay/drift gate) and keyed in full under
the two-leg route of DD-075-5 (556 signs keyed, 423 by leg 1 and 133 by
leg 2, to 424 distinct Asset A v2 rows; token 999 the named exclusion,
2 rows / 2 occurrences, counted and never classed); the census
published before any rate (other 307 signs / 7,006 occurrences; human
53 / 978; animal 39 / 1,179; object_goods 24 / 2,159; unidentified 133
signs / 481 occurrences as context; corpus-wide final-position rate
0.2579), no kind TOO THIN; and the freeze-order proof from the external
records. The per-kind verdicts under section 5.2's frozen bands,
against each kind's frequency-matched comparison class: other
INCONCLUSIVE (rate 0.2900 vs 0.2686; ratio 1.0796; Fisher two-sided
p = 0.0295; the half-of-occurrences share 0.4970 also just under its
condition); human NOT SUPPORTED (0.2526 vs 0.3244; ratio 0.7785;
p = 6.93e-06); animal NOT SUPPORTED (0.2774 vs 0.3112; ratio 0.8912;
p = 0.0200); object_goods NOT SUPPORTED (0.1153 vs 0.2844; ratio
0.4055; p = 2.34e-67 — the atlas's strongest departure, in the
depleting direction). Three falsifier-word verdicts and one
inconclusive: the family hypothesis (F075-C03) stands in question, and
no pooled depicted-kinds verdict exists. The sensitivities agree in
every word: S1 (borderline removed: 255, 256, 520, 716, 717) returns
the same four words; S2 (contested included) equals the primary
exactly, Asset A v2 carrying zero contested rows; S3 (documented +
corroborated, 5,131 rows, 707 signs, none unkeyable) returns the same
four words — no verdict is grade-sensitive. Position is not meaning:
these are positional facts about the published identification layer on
this ICIT-lineage corpus, carrying Spec 037's 49% cross-compilation
caution. Two runs byte-identical (results SHA-256 f55ae911...).
Anchors df0cf620... asserted byte-identical before and after. Records:
specs/075-depicted-kind-endings-atlas/outcome.md and step0-record.md,
reports/phase441_results.json, reports/phase441_report.md; the
registration record (osf-spec-registration.md) landed ahead of the
execution (PR #392, merged 83cea50d).

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.
## 2026-10-28 — Spec 080 BUILD: Windows host migration package (desktop production home)

At the owner's direction (2026-10-28), Glossa Lab's production home
moves from the Muse VM — where the backend was repeatedly killed by
kernel OOM events outside the project's control (Spec 079 record) —
to the owner's Windows host, TRISTEN-DESKTOP. This entry records the
BUILD; the cutover outcome gets its own entry when it happens.

Built under specs/080-desktop-host-migration (claims C080-1..C080-9
with falsifiers): production launch semantics on every Windows
surface (`create_app --factory`, 127.0.0.1, no reload) in shell.cmd,
the tray start path, and scripts/run-backend-svc.cmd; one canonical
installer (setup-os.cmd; services/windows delegators; the
H25-violating Startup shortcut retired); a targeted stop path (the
previous stop killed every pythonw.exe on the machine); installer
verification of the tray icon assets against pinned SHA-256 hashes
(ICO 315940742d75720388264dcdf03178c58f878ea0701d03eeba95688d935ff520,
PNG bb41bf09d4177cee0c96b29ebe480f86a9e7115946f9e4ad132d2367a7adb077);
deterministic installed-mode data path (%LOCALAPPDATA%\GlossaLab\data
via GLOSSA_MODE=installed in the launch chain); tray supervision on
Windows (capped auto-restart, 3/hour, never overriding a user stop —
before this change the tray started the backend once and never
restarted it); and the host tooling scripts/install-desktop-host.cmd
+ scripts/verify-desktop-host.cmd (identity-grade verification
markers). An audit note for the record: shell.cmd's committed run
line carried a redacted host token (asterisks) where the bind
address belonged — the line is replaced wholesale by this spec.

Also recorded plainly: this ledger has no entries for Specs
076–079. That gap predates this change; it is flagged here rather
than silently backfilled.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## 2026-10-28 — G44-I Amendment 3 rerun: FAILED — KI-2 triggered; Step 0-G line closed; OD-1 ruled

The G44-I implantation instrument (frozen draft 2026-10-26, Amendments
1–3, PRs #422/#423 for the halt record and amendment package) was rerun
under Amendment 3 and executed on TRISTEN-DESKTOP through the Syncyard
gatekeeper (run 40736921121) on the hash-verified staged package:
script SHA-256 6de44f06329b1111479a54bea3780ad41734e4f0e5e3928772a9e7575c7ca0f9,
population pin SHA-256 f1d984c546c77bbd5459895e9ab31b877dd7a2af69a88ff4248049bf11e8811c;
seeds model 20298464, split 20292778, leg-2 20298297, leg-3 20291685.

Results: the §6 realization gate PASSED (implantation realized exactly,
recounted independently — the first gate pass in this line). Leg 1
PASSED (B = 0.6518 vs bar 0.60; 34/44 vs bar 33). Leg 1B FAILED
(realized margin +0.0017 vs the frozen +0.05 bar — the scorer beat the
frequency baseline, narrowly, instead of losing to it). Leg 2 PASSED.
Leg 3 PASSED (both arms; five calibration checks first).

Verdict under the draft's §§7–9: FAILED — KI-2 TRIGGERED. The gate
passed and leg 1B failed with OD-1 undecided before the run, so the
prediction-pair profile-scoring design stands convicted — wrong, not
under-tuned; no further instrument under this scorer design in any
validation family. Printed alongside the verdict, as §8 prescribes: the
narrowing facts (gate and legs 1/2/3 passed, leg 1 with room; the 1B
failure was a 0.0483 shortfall on a beat, not a loss) and the §8 doubt
(under exact realization the baseline starts the race holding the
planted pair for most signs, so the margin is decided by a minority of
signs plus split-sample noise). KI-3 did not trigger as defined — it
flags a validation, and this run did not validate; the margin half of
its conditions is met (+0.0017 ≤ 0.10) and the agreement half is
pending the counts. KI-1 stands at zero strikes: implantation is
vindicated, not convicted — implantation-by-relabeling is recorded as
a proven instrument, with Amendments 1–3 as its design record.

OD-1 (owner decision, 2026-10-28): leg 1B is demoted to a reported
diagnostic for any future draft, with the tripwire preserved — a
baseline win (negative margin) under exact realization remains
disqualifying in any future gate review. The decision is forward-only:
it does not amend this verdict and does not revive the convicted
scorer design.

§9 endgame executes: the Step 0-G instrument line CLOSES entirely (no
fifth design). M4 remains GATED — DRAFT ONLY, permanently under its
current gate. The 44 pending readings remain pending indefinitely,
carrying no weight — neither validated nor falsified; this run scored
none of them. The scorer's honest measure stands on the record: it
recovers planted truth above the frozen bar and cannot be
distinguished from the corpus's own frequency summary of itself.

§8 agreement counts (baseline full-pair / position-only /
neighbor-only, of 44): PENDING-APPEND. The run's results file is in
verified transit from the desktop; when it lands, the counts are
appended to the full run record (goal record
2026-10-28-g44i-rerun-record.md, with the red-team assessment at
2026-10-28-g44i-rerun-od1-redteam-assessment.md) as a dated appendix.
The append does not change the verdict.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-22] Entry — Spec 026: CORE as a Keyed Source for RESEARCH-CHECK

Objective:
  Mirror the RCPH workspace's CORE capability into Glossa Lab's
  research-check tooling (owner's mirror directive, 2026-10-22:
  APIs added for the RCPH program are mirrored for Glossa). CORE
  via the registered custom.core connection was connected and
  verified on the RCPH side the same day. Tooling only; no Glossa
  material is audited by this spec.

What was done:

  1. SPEC: specs/026-core-research-source/ (spec.md, plan.md,
     tasks.md) — proposal with H13 epistemic boundaries recorded
     before execution (H2). Route decision recorded in the plan:
     a direct client on the vault surrogate, not the MCP server's
     search_core (its key slot is an environment variable the vault
     route deliberately does not provide) and not keyless calls
     (measured empty under spec 025).

  2. CLIENT: backend/glossa_lab/core_search.py — CORE v3 client in
     the shape of the proven RCPH connector helper. The registered
     custom.core credential is attached as a runtime bearer
     surrogate (dynamic_credentials.add_surrogate_to_request); the
     key value is never read, printed, or stored by the code.
     Canonical search path /v3/search/works/ WITH trailing slash
     (the slashless form 301s; redirects are refused on
     authenticated requests). Pace guard 2.1 s minimum interval
     (registered tier ~5 single requests per 10 s). HTTP 429 raises
     CoreRateLimitError and is never retried; every call carries an
     explicit timeout (H9/H11). CLI: python -m glossa_lab.core_search
     search|get.

  3. STAGE: backend/glossa_lab/research_check.py — CORE joins the
     source roster as a per-phrasing keyed search (injectable
     core_client; --no-core to disable). Hits merge into the same
     neighbor pool and vocabulary-overlap ranking; a CORE hit
     carrying full text is its own read source (recorded in
     neighbors_read_full_text with source "core" and word count;
     the text itself never enters the sidecar). A 429 stops CORE
     for the rest of the run with a source_errors record and a gap
     entry; the run continues on the other sources. Existing
     sources' behavior unchanged; verdict still null by
     construction; claim files never modified.

  4. DOCS: docs/paper-search-mcp.md gained a CORE section (route,
     trailing-slash rule, pacing, 429 stop, protocol standing:
     CORE is now a reached source) and its limits-list CORE line
     was updated from "keyless returns empty"; AGENTS.md gained a
     pointer bullet in the research-check section (H8).

  5. TESTS: backend/tests/test_core_search.py — 11 offline tests
     (request shape with slashed path + bearer surrogate, host
     guard, redirect refusal, 429 hard stop with exactly one
     attempt, pace-guard arithmetic, work normalization, stage pool
     merge + CORE full-text read, stage 429 stop, --no-core). The
     spec-025 tests now inject a null CORE client so that suite
     stays offline. Run together — CORE + paper-search + governance
     lint + MCP suites: 51 passed.

  6. SMOKE (live, raw outputs in the spec's smoke/): two protocol
     phrasings of an Indus concept via the client — "Indus script
     decipherment" (673,990 hits; 1 of top 10 with full text) and
     "statistical analysis of Indus signs n-grams linguistic
     structure" (9 of top 10 with full text). CORE search is loose
     (polysemy: Indus river-basin geology, generic n-gram papers);
     the stage's vocabulary ranking is what makes it usable.
     Scoped end-to-end stage run on the Yadav 2010 n-grams claim
     (Zipf-Mandelbrot): CORE queried per phrasing, contributed 8 of
     23 neighbors, zero source errors; the 3 full-text reads went
     to on-topic arXiv neighbors — the two full-text-carrying CORE
     neighbors scored relevance 0.0 and were correctly not read
     (the CORE read path is covered by the offline tests). Sidecar
     written to the usual place; verdict null. No backend process
     was restarted or disturbed (the running uvicorn on :8001 was
     left alone).

  7. COMMIT: this spec's files only, on branch
     spec/026-core-research-source. The pre-existing uncommitted
     working-tree modifications (extracted-claims dossiers, claim
     reports, anchor staging, partial loop results) are not this
     session's work and were not staged; none of the files this
     spec modifies carried uncommitted changes at branch time.

**AI disclosure:** execution recorded by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per constitution SSVI.

## 2026-10-29 — Spec 080 Amendment 1: installer defects fixed; autostart mechanism amended

The Spec 080 desktop install job (gatekeeper
`glossa-host-install-2026-10-28-r1`, run 40802151979) completed
GitHub-green while its 27 markers proved the install had NOT
landed: INSTALL_EXIT 1 and no `GlossaLab` scheduled task. Two
defects, pinned in the source and on the host:

1. Icon verification: `setup-os.cmd install` hashed the tray
   icons with an inline `Get-FileHash` one-liner in a
   `powershell -NoProfile` child. In that context the cmdlet
   threw CommandNotFoundException and the batch check reported
   the hashing failure as a hash "mismatch", refusing an
   install whose assets match the pins exactly.
2. Autostart registration: `Register-ScheduledTask` returned
   HRESULT 0x80070005 in both the installer's elevation-wrapper
   path and the direct fallback, and the fallback script still
   printed "Task registered." after the failure.

Host diagnostic `glossa-host-diag-2026-10-28` (run 40807602846)
established the execution context (tristen-desktop\trist,
session 1, not elevated) and that per-user task registration
is denied in it with and without an explicit principal, while
schtasks.exe exits 0 creating nothing. On that evidence the
Desktop Access program directed, and this change records,
Amendment 1 to Spec 080: the canonical per-user autostart is
the HKCU Run value `GlossaLab` (wscript.exe + launch-tray.vbs),
written and read-back-verified by the installer; the
scheduled-task path and scripts\register_task.ps1 are removed
(no dual mechanism). Icon verification moves to
scripts\verify_icon_hashes.ps1 (.NET SHA-256, case-insensitive
comparison, exit 2/3/4 discriminating hashing failure /
missing asset / mismatch; the method is printed as
GLOSSA_ICON_HASH method=dotnet-sha256). The tray's autostart
detection and scripts\verify_desktop_host.py read the Run
value; FR-007's GLOSSA_TASK_STATE marker is renamed
GLOSSA_AUTOSTART_STATE. FR-005's bar — verify, fail loudly,
refuse on any failure — is unchanged. Spec record:
specs/080-desktop-host-migration/spec.md, Amendment 1;
contract tests C080-5 (updated) and C080-8 (new).

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-29] Entry - Spec 080 Amendment 2: Autostart Restored to Route-B Scheduled Task

Amendment 1's HKCU Run-key autostart is superseded. Host
diagnostic glossa-host-diag2-2026-10-28 (gatekeeper run
40816104983, 20 markers), from the same non-elevated job context
as diag1 (tristen-desktop\trist, session 1), registered a task
cleanly via the cmdlet route with a scoped principal: task file
present, CIM state Ready, principal trist / Interactive /
Limited, trigger MSFT_TaskLogonTrigger for
TRISTEN-DESKTOP\trist. The schtasks route still fails there.
Diag1's denials (run 40807602846) were therefore shape-caused
(unscoped trigger, no scoped principal, elevation wrapper),
not a venue-wide bar.

This change restores Spec 080's design of record:
scripts\register_task.ps1 returns in the route-B shape and is
invoked directly by setup-os.cmd install (no elevation); it
reads the task back, prints GLOSSA_TASK_STATE, and gates the
install on the Ready state. The HKCU Run route is removed (Run
deletes remain as legacy cleanup). The tray's autostart
detection and scripts\verify_desktop_host.py return to the
task (CIM read); FR-007's marker is GLOSSA_TASK_STATE again.
Amendment 1's icon-verification fix (.NET SHA-256 helper,
case-insensitive, discriminated failures) is unchanged.
Spec record: specs/080-desktop-host-migration/spec.md,
Amendment 2; contract test C080-8 (revised).

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-29] Entry - Spec 080: Verify Script Backend Identification Fix

scripts\verify_desktop_host.py identified the backend by the
PID listening on port 8001. On TRISTEN-DESKTOP that listener is
tailscaled.exe (session 0): Tailscale Serve holds the tailnet
:8001 and proxies to the app's loopback :8001. The restart leg
therefore tried to kill the Tailscale service process and
reported kill-failed (host run 40835699406), failing
GLOSSA_HOST_VERIFY while every app leg passed; a follow-up
app-stop proof (run 40840066177) confirmed the app's own stop
works and the "port still listening" reading was the proxy.
Fix: the backend is identified by command line
(glossa_lab + uvicorn - the targeted stop path's own test) as
a process SET; the restart leg kills that set and waits for a
healthy backend under a PID outside the set. The port listener
is never targeted for kill or identity.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-29] Entry - Spec 080 Amendment 3: Persistence (Task-Owned Start, Idempotent Start)

Diagnosis (host runs 40855200786 + 40861773854): the desktop
backend passed every verification leg, then vanished within
~35 minutes. The logon task had never run (console session
logged on since 2026-09-25; LastRunTime 11/30/1999); every
verified start was launched inside a gatekeeper job and died
with that job's teardown - tray and backend both at 0
processes, backend log ending after startup with no shutdown
lines. An earlier cycle also showed a double-start race
(address-in-use).

Amendment 3: register_task.ps1 gains the scheduler's
restart-on-failure (RestartCount 3, RestartInterval 1 min);
launch-tray.vbs now waits on the tray and propagates its exit
code, so the task stays Running for the tray's lifetime and
the scheduler restarts a crashed tray (a clean exit-0 quit is
not restarted). setup-os.cmd start is idempotent: the bounded
Spec 079 identity check runs first, and an already-healthy
backend makes the start a no-op success
(GLOSSA_START_STATE already-running). The durable start is
the task fired on demand (Start-ScheduledTask) - scheduler-
owned, so it outlives any job; the persistence proof must
span a job boundary (separate later probe job). Spec record:
specs/080-desktop-host-migration/spec.md, Amendment 3;
contract tests C080-8 (extended) and C080-9 (new).

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-29] Entry - Spec 080: Verify Process Identification Precision

Follow-up to the backend-identification fix: the command-line
match also matched the PowerShell process running the CIM
query itself (its -Command text carries the pattern), and
that transient PID failed the restart leg's kill step (host
run 40880047294; every other leg passed). Process
identification in scripts\verify_desktop_host.py now requires
the repo venv's python executable (ExecutablePath) in
addition to the command-line pattern, for both the backend
set and the tray set, via a shared helper.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-29] Entry - Spec 080 Amendment 3 Consolidation: Kill-Based Restart Leg Purged

Per Desktop Access direction after start-verify run
40880047294 (start fully green; the kill-based restart leg
failed a third time; three tray processes had accumulated):
(a) GLOSSA_RESTART_TEST in scripts\verify_desktop_host.py no
longer kills anything - it cycles the app through its own
controls (setup-os.cmd stop -> backend set gone + proxy
health not 200 -> setup-os.cmd start -> identity under a
fresh PID), the restart-verify2 method (proof of record:
run 40849993917). kill_pid/taskkill are gone from the suite.
(b) setup-os.cmd start's idempotency covers the tray too:
backend healthy + tray running = full no-op; tray missing =
launch only the tray. (c) timeout /t waits in setup-os.cmd
are replaced with ping waits - timeout.exe prints "Input
redirection is not supported" under redirected stdin,
dirtying successful job logs.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-29] Entry - Desktop UI-Log Audit Fix 1: Tray Supervision Honesty

Objective:
  Owner directive 2026-10-29 ("check ui logs too. I see lots of
  failures and fallthroughs. fix all."): audit the desktop host's
  UI/tray/backend logs, catalog every failure and fallthrough, fix
  root causes. This entry covers the tray (tray/glossa_tray/main.py).

Findings fixed (all in the tray):
  1. The status poller ENDED after ~24 h of polling
     (_MAX_POLL_ITERATIONS) with only a print - invisible under
     pythonw - leaving the tray showing a frozen status with
     supervision silently over. Polling now runs in bounded
     segments (H11: bound kept, expiry diagnosed) that renew
     themselves and record each renewal in the tray log; a crashed
     segment or a single failed poll is logged and polling
     continues.
  2. Auto-restart ignored in-flight starts: the 3-second poller
     restarted over a still-booting backend, spawning duplicates
     that raced for the port (Errno 10048 in logs/backend.log,
     2026-10-29) and burned the 3/hour restart cap on one slow
     start. Starts now record an in-flight flag + timestamp;
     auto-restart returns "starting" inside a 120 s grace window,
     and a start that never comes up is logged as failed before
     supervision resumes. Cap-reached is logged once, not per poll.
  3. The stop path's documented "then kill if still running" did
     not exist: the shutdown request's failure was swallowed and
     no kill was attempted. Stop now waits (bounded) for the
     backend to go away, then kills the listening PID (netstat)
     as the last resort, and logs the outcome either way.
  4. The tray had NO log of its own - every diagnostic was a
     print discarded by pythonw (audit confirmed no current-era
     tray log file exists on the host). logs/tray.log now records
     tray start, backend starts, auto-restarts, stop outcomes,
     config failures, autostart failures, and poller renewals,
     rotated under the same policy as the backend log (shared
     _rotate_log_file helper).
  5. Config load/save failures were silent (a corrupt config
     silently defaulted the port, making the tray poll the wrong
     port); autostart install results were discarded (a failed
     install retried invisibly on every launch); a backend spawn
     failure (e.g. missing venv pythonw) propagated out of main()
     and killed the tray before its icon appeared. All three are
     now logged, and a failed spawn leaves the tray alive showing
     the failure in its status.

Tests: backend/tests/test_tray_supervision.py - 11 behavior tests
(pystray/Pillow stubbed, headless): in-flight start never
duplicated, grace expiry resumes supervision, cap logged once,
user stop never overridden, poller renews after a segment failure,
segment survives a bad poll, tray log writes + rotates, config
failure logged, spawn failure contained, stop kill-fallback
exercised end to end.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-29] Entry - Desktop UI-Log Audit Fix 2: Windows Script Honesty

Objective:
  Owner directive 2026-10-29 ("check ui logs too. I see lots of
  failures and fallthroughs. fix all."): root-cause fixes for the
  Windows launch/install scripts and the host verifier.

Findings fixed:
  1. shell.cmd setup ran five fallible steps (pip upgrade, backend
     install, tray requirements, GPU installer, npm install +
     build) with no errorlevel checks and ended with "[OK]
     Dependencies updated." + exit 0 unconditionally - success
     reported on failure. Every step is now checked; a failure
     exits 1 naming the step. install-desktop-host.cmd already
     checked the result (a check that could never fire); now it
     can. setup-os.cmd's install path only re-checked that
     pythonw.exe existed after its shell.cmd setup call; it now
     aborts on a setup failure as well.
  2. scripts/start_services.cmd, start_services.ps1 and
     start_services_safe.ps1 were stale duplicate entry points:
     they launched uvicorn with the retired non-factory app object
     (glossa_lab.main:app), no GLOSSA_MODE (so the dev data
     directory, not the installed one), hard-coded port 8001, and
     printed success unconditionally (the .ps1 is on record as
     having shipped with a parser error; the _safe variant existed
     only to work around it). All three are now delegating shims
     to the canonical setup-os.cmd start, per the C080-4 shim
     precedent (a shim, never a second launch path).
  3. Retired two-task machinery deleted: scripts/register-tasks.ps1
     (registered the retired GlossaLabBackend + GlossaLabTray task
     pair; the single GlossaLab task via register_task.ps1 is the
     only registrar) and scripts/run-tray-svc.cmd (the retired
     task's wrapper; its timeout /t wait under redirected stdin is
     one historical source of "Input redirection is not
     supported" noise in logs/tray.log).
  4. scripts/exec.cmd's wait loop used timeout /t 1 - the last
     timeout.exe wait in the Windows scripts; now a ping wait.
     A contract test scans every Windows .cmd for operational
     timeout.exe waits. The pre-existing assertion for this in
     test_start_is_idempotent_on_verified_identity ended in
     "or True" and could never fail; it is a real check now.
  5. scripts/verify_desktop_host.py reported GLOSSA_TRAY_PROCESS
     but its overall verdict ignored it: a host with no tray
     (its user interface down) verified PASS. Tray presence is
     now part of the verdict, with --skip-tray-check recording
     an explicit skip in the marker, mirroring --skip-restart-test.

Tests: backend/tests/test_desktop_host_migration.py - the
repaired timeout assertion plus new contract tests for the
shims, the retired files' absence, shell.cmd failure
propagation, and the timeout.exe ban.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-29] Entry - Desktop UI-Log Audit Fix 3: Backend Fallthrough Honesty

Objective:
  Owner directive 2026-10-29 ("check ui logs too. I see lots of
  failures and fallthroughs. fix all."): root-cause fixes for the
  backend failures visible in the desktop host's live log.

Findings fixed:
  1. The discovery LLM client (backend/glossa_lab/discovery/
     llm.py) retried a failing provider on EVERY call with no
     memory: in the desktop backend log of 2026-10-29, one
     scheduler tick produced dozens of consecutive "provider
     mistral returned 429, falling through" lines (one per
     classified item), in a log carrying 1,378 WARNING lines. The
     client now carries the same circuit breaker as ai_utils.call_llm (the
     newer stack): 5 consecutive failures open the circuit for
     600 s (one WARNING at open, skips at DEBUG), success resets
     the count, expiry allows a retry. Fall-through order and the
     all-providers-failed LLMError are unchanged.
  2. _sync_static_fallback_async (model_intelligence.py) swallowed
     every per-model INSERT failure and the COMMIT failure with
     bare except/pass and returned "errors": 0 unconditionally -
     a partially written static fallback reported full success.
     Errors are now counted, the first is logged at WARNING with
     the counts, and the returned dict carries the real number.

Not code-fixed, by evidence: the dashboard insight cascade in
the same log (reasoning -> conversational -> short-prompt, then
"empty response after 3 attempts") is an HONEST degraded path -
the returned payload tells the user the provider may be
overloaded and names the remedy (model "empty-fallback"); its
root cause was the dead/rate-limited provider, addressed by
item 1's circuit discipline in the discovery stack and by the
pre-existing circuit in ai_utils.

Tests: backend/tests/test_discovery_llm_circuit.py - circuit
opens at the threshold and stops invoking the provider, a
healthy fallback keeps serving during cooldown, success resets
the failure count, cooldown expiry allows a retry.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec.VI.

## [2026-10-29] Entry — Leg B hardening: spec-study register API (the program record gets a surface)

- **Gap (Leg B reconciliation, delta D0):** every spec-kit study execution
  (Specs 001–081) had NO API surface — `/studies` serves canvas graphs,
  and no endpoint enumerated the `specs/` register, so no UI surface
  could show a study verdict or status.
- **Fix:** new read-only `GET /api/v1/spec-studies` and
  `GET /api/v1/spec-studies/{spec_id}` (`backend/glossa_lab/api/spec_studies.py`),
  serving one entry per `specs/NNN-slug/` directory: spec_id, slug,
  title (spec.md H1), has_outcome, and the outcome record's own headline
  verbatim-truncated (never paraphrased). Duplicate spec numbers
  (021/025/026) return `ambiguous: true` with all matches.
- **Restricted entry:** Spec 072's directory contents are never opened
  by this module; its entry is built from the directory name only
  (public naming) with `restricted: true`.
- **Tests:** `backend/tests/test_spec_studies.py` — 6 passed (register
  enumeration, 052 INCONSISTENT headline, duplicate ambiguity, 404,
  restricted-contents-never-read on a synthetic register, restricted
  entry shape on the real register). Ruff clean.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec. VI.

## [2026-10-29] Entry — Leg C hardening 4: [VERIFIED] marker requires a resolvable reference (C-04)

- **Finding (Leg C red team, measured with the real assessor, AEE
  1.5.3):** prefixing a claim's own `glossa_lab_evidence` text with
  the literal substring `[VERIFIED]` raised its propagated score
  from 0.164 to 0.725 (evidence and independence components at
  maximum) — `aee_core` conferred OBSERVED/TEST purely on the
  substring, with no artifact, hash, or provenance check.
- **Fix (`backend/glossa_lab/aee_core.py`):** `[VERIFIED]` confers
  `EvidenceKind.OBSERVED` only when the same record carries an
  evidence reference (`evidence_ref`, `glossa_lab_evidence_ref`, or
  `evidence_artifact`) whose artifact path exists relative to the
  repo root or `backend/` — the same resolution rule as the C-03
  promotion gate. An unreferenced or unresolvable marker is
  INFERRED, like any other self-authored text. Records whose
  `[VERIFIED]` text names no artifact will score lower than before;
  that is the intended correction, and re-crediting a claim means
  recording the artifact it was verified against.
- **Tests:** `backend/tests/test_aee_core.py` — unreferenced marker
  → INFERRED; resolvable reference (`LEDGER.md`) → OBSERVED;
  fabricated reference → INFERRED.

AI disclosure: executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec. VI.

Amendment to the Leg C hardening 4 entry (same PR): the C-04 rule
change moved exactly three live-store scores — every claim whose
record carries `[VERIFIED]` with no resolvable reference
(parpola_2010_dravidian_solution_manual_001,
yadav_2009_arxiv_manual_001, yadav_2009_arxiv_manual_002; evidence
component 1.0 → 0.706875, band high → medium each). Per the
established fixture-supersession precedent in
`backend/tests/test_spec029_phase104_correction.py` (aee 1.5.0
adoption, Spec 054), the post-correction score fixture was
regenerated from the live store, the test header records the
supersession and its cause, and the movement test now names the
Leg C set and asserts its cause mechanically (record carries
`[VERIFIED]`, `_verified_marker_is_referenced` is false, only the
evidence component fell). The post-merge baseline fixture is
unchanged.
