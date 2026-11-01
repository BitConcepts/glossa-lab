# Spec 026 — Plan

## Decision: which route to CORE, and why

Three routes were available:

- **(A) Direct client in Glossa's tree using the vault surrogate**
  (chosen): `glossa_lab/core_search.py` builds requests against
  `api.core.ac.uk` and lets `dynamic_credentials.add_surrogate_to_request`
  attach the registered `custom.core` credential as a bearer header.
  This is byte-for-byte the pattern the RCPH connector helper
  (`custom.core/bin/core_api.py`) already runs in production, so the
  behavior contract (trailing-slash search path, redirects refused,
  registered pace, 429 stop) is inherited from a proven route rather
  than re-derived.
- **(B) The MCP server's `search_core` tool**: reads its key from
  `PAPER_SEARCH_MCP_CORE_API_KEY` in the server process's
  environment. The vault route deliberately never materializes the
  key into files or process environments this project controls, and
  spec 025's rule is that `PAPER_SEARCH_MCP_*` values are only ever
  passed through from a caller's environment, never stored. There is
  no compliant way to feed (B) from the registered connection.
- **(C) Keyless CORE calls**: measured empty from this network
  (spec 025 limits record). Not a route.

(A) also keeps the change additive: the MCP tool surface, the
`glossa_mcp` 33-tool surface, and the stage's existing sources are
all untouched in behavior.

## Pieces

1. `backend/glossa_lab/core_search.py` — CORE v3 client: search
   (canonical slashed path), get-by-id, work normalization, pace
   guard (2.1 s minimum interval), `CoreError` /
   `CoreRateLimitError`, explicit timeouts, CLI.
2. `backend/glossa_lab/research_check.py` — per-phrasing CORE source
   in `run_research_check` (+ injectable `core_client`, `use_core`
   flag, `--no-core` CLI flag); CORE full-text neighbors recorded as
   read from source `"core"`; 429 stops CORE for the run with an
   error record + gap entry.
3. `backend/tests/test_core_search.py` — offline unit tests for the
   client and the stage integration.
4. `docs/paper-search-mcp.md` — new CORE section; limits list CORE
   line updated from "keyless returns empty" to the keyed route.
5. `AGENTS.md` — pointer line in the research-check section.
6. `LEDGER.md` — session entry (H1/H7).

## Placement in the research flow

Unchanged from spec 025: the stage runs before AEE
scoring/adjudication and writes advisory sidecars. CORE simply joins
the stage's source roster at invocation time. No loop code, API
route, running process, or claim file is modified, so nothing needs
a restart; the running backend (uvicorn on :8001) is not touched.

## Smoke summary (2026-10-22, raw outputs in `smoke/`)

- (i) Two protocol phrasings through the new client from the Glossa
  tree: "Indus script decipherment" (totalHits 673,990; 1 of the
  top 10 carrying full text — a Harappan–Brahmi paper, 3,737 words)
  and a stranger's phrasing, "statistical analysis of Indus signs
  n-grams linguistic structure" (9 of the top 10 carrying full
  text). CORE search is loose (polysemy: the Indus *river basin*,
  generic n-gram papers) — the stage's claim-vocabulary ranking is
  what makes it usable, exactly as with the arXiv trap in spec 025.
- (ii) Scoped end-to-end stage run on the Yadav 2010 n-grams claim
  ("Indus script sign frequencies follow a Zipf-Mandelbrot
  distribution"): CORE queried once per phrasing and contributed 8
  of 23 neighbors with zero source errors; the 3 full-text reads
  went to on-topic arXiv neighbors. The two CORE neighbors carrying
  full text scored relevance 0.0 against the claim and were
  correctly not read — the gate working as designed; the CORE read
  path itself is covered by the offline stage tests. Sidecar in the
  usual place (`glossa-indus/claims/research_checks/`), verdict
  null.
