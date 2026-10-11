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
