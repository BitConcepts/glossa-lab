# Plan 003 — MCP update, requirements/test traceability, Indus continuation

## Stage A (MCP)

- Enumerate the live route table from the app's OpenAPI schema; diff
  every MCP-called method/path against it (path-parameter names
  normalised — only URL structure is load-bearing).
- Add Indus evidence tools on the existing `_get`/`_fmt`/`_err`
  conventions, only for routes that exist; `get_indus_claim` resolves
  via the list endpoint because no per-claim route exists.
- Add `get_foundation_status` for the `/api/v1/foundation/status` state
  the existing `run_foundation_check` tool did not expose.
- Declare the `mcp` extra in `backend/pyproject.toml` (found undeclared
  during the audit) so the server is installable from the manifest.
- Update tool inventories in README.md, backend/README.md, AGENTS.md.

## Stage B (gaps)

- Traceability pass over specs 001–002 → matrix in spec.md (R1–R12).
- `backend/tests/test_glossa_mcp.py`: httpx MockTransport; happy-path
  request formation/response formatting per tool family, error-path
  helper coverage, tool-inventory assertion, and a drift-guard test
  that extracts every route called in `glossa_mcp/server.py` source and
  asserts it exists in the live app's OpenAPI route table.
- `foundation_check.py`: replace the hardcoded Windows repo path with
  `resolve_repo_root()` (env override `GLOSSA_REPO_ROOT`, else
  script-location-derived). Run it (Holdat corpus fetched from its
  CITATIONS.md A.13 public source into the gitignored `corpora/` layout)
  and record the real result.
- `backend/tests/test_foundation_check_script.py`: resolver unit tests
  (ast-extracted, no check body executed) + subprocess integration test
  (skips when the corpus is absent).
- Full backend suite run; ruff on changed files.

## Stage C (Indus)

- Phase-104 claims evaluation: script
  `backend/scripts/phase104_claims_evaluation.py` + graph module
  `backend/glossa_lab/experiment_graph_phase104_claims.py` (H15/H23:
  graph-first, registered in `experiment_graph.py`, registration
  verified before the script runs). Reads extracted claims, their
  in-repo evidence fields, AEE scores, and anchor/corpus cross-checks;
  writes `glossa-indus/reports/phase104_claims_evaluation.json`;
  claim status changes applied to the claim JSONs only where the
  computed evidence meets the stated rule, each change cited.
- Phase-105 name adjudication: rewrite the unrun draft
  `backend/scripts/phase105_name_signs.py` as a positional/formula
  adjudication (Phase-101 style) over the Holdat corpus; the existing
  `IndusNameSigns` graph node already targets this script. Verdicts to
  `reports/phase105_name_signs.json`; anchors file touched only on a
  threshold-meeting promotion, followed by a foundation-check run (H21).
- OCR: probe for Mistral credentials + `pypdfium2`; run the registered
  Phase-104-OCR node script only if both are present, else record
  blocked in the ledger.
- Ledger: Phase-104/105 entries in `glossa-indus/LEDGER.md`, summary in
  root `LEDGER.md`, both with AI disclosure (constitution §VI).
