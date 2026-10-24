# Spec 025 — Plan

## Decision: which client shape, and why

Two shapes were available:

- **(A) Client module in Glossa's tree** (chosen): `glossa_lab/
  paper_search.py` runs under the backend venv (already carries
  `mcp>=1,<2` per `backend/pyproject.toml`) and spawns the shared
  server from `~/workspace/venvs/paper-search-mcp`. The research
  loop / claims flow imports it directly; a CLI in the stage module
  covers standalone use.
- **(B) Register the server in an MCP-client config**: Glossa has no
  MCP-*client* configuration surface in-tree (its MCP artifact is the
  `glossa_mcp` *server* for backend control; external agents bring
  their own client configs). There is nothing in-tree to register
  into, and adding tools to `glossa_mcp` would break its
  route-drift-guarded contract (every tool maps to a backend route).

(A) follows the repo's own layering: outward integrations live as
packages/modules under `glossa_lab/` (cf. `discovery/`), control
lives in `glossa_mcp/`.

## Pieces

1. `backend/glossa_lab/paper_search.py` — stdio client (async core,
   sync facade, explicit timeouts, NO_PROXY sanitization,
   `PAPER_SEARCH_MCP_*` passthrough, Sci-Hub hard-off in
   `read_full_text`).
2. `backend/glossa_lab/research_check.py` — the RESEARCH-CHECK
   stage: plan construction (≥2 phrasings × ≥2 sources), execution
   against the client, nearest-neighbor full-text reads where OA
   routes exist, sidecar record writer, CLI.
3. `backend/tests/test_paper_search.py` — offline unit tests.
4. `docs/paper-search-mcp.md` — connector/usage doc + audit protocol.
5. `AGENTS.md` — one short section pointing at the stage and doc
   (H8: architecture-affecting change updates docs in-cycle).
6. `LEDGER.md` — session entry (H1/H7).

## Placement in the research flow

The stage attaches to a claim dossier **before** AEE scoring /
adjudication and produces an advisory sidecar in
`glossa-indus/claims/research_checks/`. It is invoked explicitly
(CLI or import); no loop code, API route, or running process is
modified by this spec, so nothing needs a restart to be safe — the
stage simply becomes available to the loop's operators and to the
follow-on audit.

## Smoke summary (2026-10-22, raw outputs in `smoke/`)

- (i) `tools` — the server answered from the Glossa client with its
  full tool list.
- (ii) Concept queries on Indus decipherment prior work returned real
  results on the reachable sources (arXiv / Crossref federated run +
  per-source runs filed); per-source failures, where any, are in the
  filed JSON `errors` fields.
- (iii) `get_crossref_paper_by_doi` for 10.1126/science.1170391
  returned the Rao et al. 2009 *Science* record.
- (iv) End-to-end stage run on the Yadav 2009 dossier claim. First
  attempt surfaced a measured arXiv trap: a no-match conjunction
  returns a default high-profile list (ATLAS, gravitational-wave
  papers) instead of an empty result, and those junk hits consumed
  the full-text read slots. The stage now ranks neighbors by
  claim-vocabulary overlap and spends reads on the highest-overlap
  arXiv neighbors; rerun filed in `smoke/04_stage_run.txt` and as
  the first sidecar under `glossa-indus/claims/research_checks/`.
