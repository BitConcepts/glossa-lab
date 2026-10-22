# Spec 026 — Tasks

- [x] T1 Inspect the working route (custom.core CONNECTOR.md +
      helper), the spec-025 implementation, governance rules
      (H1/H2/H7/H8/H9/H11/H13), and `git status` (pre-existing
      uncommitted work preserved; no target file carries
      uncommitted changes).
- [x] T2 Branch `spec/026-core-research-source`; write this spec +
      plan (proposal before execution, H2/H13).
- [x] T3 Implement `backend/glossa_lab/core_search.py` (surrogate
      bearer auth, slashed search path, redirects refused, pace
      guard, 429 hard stop, timeouts, CLI).
- [x] T4 Integrate CORE into `backend/glossa_lab/research_check.py`
      (per-phrasing source, pool merge, CORE full-text reads,
      429-stops-CORE, `--no-core`; existing sources unchanged).
- [x] T5 Offline tests `backend/tests/test_core_search.py`; run
      them plus the spec-025 suite, governance lint, and MCP suite.
- [x] T6 Docs: CORE section in `docs/paper-search-mcp.md` (+ limits
      line), AGENTS.md pointer line (H8).
- [x] T7 Live smoke from the Glossa tree (two Indus concept
      phrasings via the client; one scoped end-to-end stage run with
      CORE among its sources) — raw outputs in `smoke/`.
- [x] T8 Ledger entry; commit this spec's files only, by explicit
      path; push the branch.
