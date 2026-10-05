# Spec 003 — MCP update, requirements/test traceability, Indus continuation

**Status:** Implemented on `feat/mcp-gaps-indus-continuation` (2026-10-05).
**Context:** Follow-on to the spec-kit + AEE migration (PR #54). Three work
stages: (A) bring the MCP server up to date with the post-migration API
surface, (B) close requirements/test gaps found by a traceability pass over
specs 001–002, (C) resume the Indus decipherment program at its recorded
next actions (Phase-102/103 follow-ups in `glossa-indus/LEDGER.md`).

## Stage A — MCP update

- Route-drift audit against the live FastAPI route table (311 routes via
  OpenAPI): all 27 pre-existing tools resolve; no functional drift (the
  experiment-graphs item routes name their path parameter `{exp_id}`,
  which does not affect calls).
- Six new tools (33 total): `list_indus_claims`, `get_indus_claim`,
  `get_indus_claim_aee_scores`, `list_indus_library`,
  `list_indus_hypotheses` (Indus evidence surface), and
  `get_foundation_status` (foundation auto-check state).
- `trigger_discovery_fetch` documentation aligned with the migration:
  `gdelt_ngrams` is the default GDELT source; the DOC API fetcher is
  paused/opt-in.

## Stage B — Traceability matrix (specs 001–002 → implementation → test)

| # | Requirement (source) | Implementation | Test evidence | Status |
|---|---|---|---|---|
| R1 | REST API + job engine (001) | `glossa_lab/main.py`, `api/jobs.py` | `test_jobs.py`, `test_status.py`, `test_health.py` | Covered |
| R2 | Discovery engine, multi-source (001) | `glossa_lab/discovery/` | `test_discovery_api.py`, `test_discovery_cli.py` | Covered |
| R3 | GDELT via Web Ngrams, DOC API opt-in (002-i) | `discovery/fetchers/gdelt_ngrams.py`, registry gating in `fetchers/__init__.py` | `test_gdelt_ngrams.py` (11) | Covered |
| R4 | Evidence Graph: library, claims, hypotheses (001) | `api/indus_evidence.py` | `test_indus_evidence_api.py` (25), `test_evidence_atomic_nodes.py` | Covered |
| R5 | Claim scoring on the AEE library (001, constitution §IV) | `glossa_lab/aee_core.py`, `GET /indus-evidence/claims/aee-scores`, `?aee=true` | `test_aee_core.py` (18) | Covered |
| R6 | Foundation check gate (001, constitution §III, H21) | `api/foundation_check.py`, `scripts/foundation_check.py` | API covered via research-loop/foundation tests; **script had no test and a hardcoded Windows path** | **Gap fixed here** (dynamic root resolution + `test_foundation_check_script.py`) |
| R7 | MCP server for agent integration (001) | `backend/glossa_mcp/server.py` | **Zero tests; `mcp` package in no dependency manifest** | **Gap fixed here** (`test_glossa_mcp.py` incl. route drift guard; `mcp` extra in `pyproject.toml`; 27 → 33 tools, baseline figure in 001 superseded) |
| R8 | Experiment Builder graph nodes (001, H15/H23) | `experiment_graph*.py` | `test_experiment_graph.py`, `test_atomic_nodes.py`, `test_graph_experiments.py` | Covered |
| R9 | Fully-cited daily briefing (002-ii) | — | — | Future work per spec 002 (T006); not a gap |
| R10 | Manuscript-method vision passes (002-iii) | — | — | Design notes per spec 002 (T007); not a gap |
| R11 | Frontend panels (001) | `frontend/` | Playwright suite in CI (not part of the backend pytest suite) | Covered by CI |
| R12 | Governance rules encoded (001) | `docs/governance/` | `test_governance_lint.py` | Covered |

Additional gaps found and disposition:

- `backend/scripts/foundation_check.py` also depended on the gitignored
  `corpora/` downloads; with the Holdat corpus fetched from its cited
  public source (CITATIONS.md A.13) the script now runs anywhere:
  **39 passed, 0 failed, 9 warnings** (2026-10-05 run; warnings are the
  script's pre-existing documented caveats).
- Spec 001's "27 tools" MCP figure is superseded by Stage A (33 tools);
  001 is an as-built baseline and is left as the historical record.

## Stage C — Indus program continuation

Recorded in `glossa-indus/LEDGER.md` (Phase-104 claims evaluation,
Phase-105 name-sign adjudication, Phase-102 OCR follow-up status):

- **Phase-104:** evaluate the 21 `untested` extracted claims against
  in-repo evidence, using each claim's own `falsification_condition` as
  the test and AEE scores (`aee_core`) as supporting signal. Status
  changes only where in-repo evidence clearly warrants them under the
  claims' existing status conventions; every change cites its evidence.
- **Phase-105:** positional/formula adjudication of the Phase-103
  personal-name candidates M362, M398, M375, M024 against the Holdat
  corpus, in the style of the Phase-101 M293 adjudication. The unrun
  draft `phase105_name_signs.py` asserted pre-written readings and
  promotions; it is replaced by a data-driven adjudication — no anchor
  promotion unless the program's thresholds are met by computed evidence.
- **Phase-102 follow-up (Mistral OCR of im77intro.pdf):** attempted only
  if the Mistral tooling/credentials are configured in the environment;
  otherwise recorded as blocked — no fabricated extraction.
- `docs/PREDICTION_REGISTER.md` PRED-2026-001..003 remain PENDING
  (external ICIT data); untouched.

## Epistemic boundaries (H13)

- Stage C evaluates claims only against evidence already in the repo;
  an AEE score is a consistency signal, not independent corroboration,
  and is never the sole basis for a status change.
- A null result (no claim moves, no candidate promoted) is a valid
  outcome and is reported as such.
- Assumptions: the Holdat corpus CSV (Miller 2025, CITATIONS.md A.13) is
  the same corpus the prior phases used; anchor conventions follow
  `backend/reports/INDUS_FINAL_ANCHORS.json` and prior phase reports.
