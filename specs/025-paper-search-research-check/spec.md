# Spec 025 — Paper-search MCP client + RESEARCH-CHECK stage

**Status:** Implemented 2026-10-22 on `main` (owner's direct order,
same day the server was adopted for the RCPH workspace).
**Context:** The owner ordered a solid MCP server for three jobs —
checking research, challenging proposed research, and finding prior
material — implemented in both the RCPH workspace and Glossa Lab, with
each project's own material then audited under a fixed protocol. This
spec is the Glossa Lab implementation. The audit of Glossa's own
material is separate follow-on work, run by the Glossa Lab chat under
the protocol in `docs/paper-search-mcp.md`; this spec is tooling only
and audits nothing.

## What was adopted

**paper-search-mcp** by openags (MIT) — the multi-source scholarly
search/retrieval MCP server already installed for RCPH: arXiv,
Crossref, Semantic Scholar, OpenAlex, CORE, BASE, Europe PMC, PubMed
and more, with open-access full-text retrieval and no key required for
core function. The install is **shared, not duplicated**: the server
runs from the dedicated venv `~/workspace/venvs/paper-search-mcp`
(pinned dependency set; the `mcp` SDK must stay on the 1.x line — the
server uses its FastMCP). Glossa adds a client and a stage; it does
not vendor or re-install the server.

## Design

1. **Client — `backend/glossa_lab/paper_search.py`.** A stdio MCP
   client in Glossa's own tree, run under Glossa's backend venv (which
   already depends on `mcp>=1,<2`). It spawns the server with the
   paper-search venv's interpreter
   (`~/workspace/venvs/paper-search-mcp/bin/python -m
   paper_search_mcp.server`; override via `GLOSSA_PAPER_SEARCH_PYTHON`)
   and exposes `list_tools()` / `call_tool()` plus typed helpers
   (`search_papers`, `search_source`, `resolve_doi`, `read_full_text`).
   It follows the house patterns of `backend/glossa_mcp/server.py`:
   clean JSON-style error dicts instead of crashes, explicit timeouts
   on every call, ambient-proxy passthrough with the NO_PROXY
   sanitization both existing clients apply. `PAPER_SEARCH_MCP_*`
   environment variables (optional free API keys) pass through from
   the caller's environment and are never written to files.
   **Sci-Hub is hard-off:** `read_full_text` refuses any call that
   would set `use_scihub`, in code, not just by convention.

   Why a client module rather than new tools on `glossa_mcp`:
   `glossa_mcp` is the control surface for the running backend (its
   33 tools map to backend routes and are drift-guarded against
   them). Paper search is an *outward-facing* client of an external
   server; it has no backend route and needs no running backend. It
   therefore lives beside the research loop, not inside the control
   server, and the 33-tool surface is unchanged.

2. **Stage — `backend/glossa_lab/research_check.py`.** A
   RESEARCH-CHECK / prior-art audit stage for claim dossiers
   (`glossa-indus/claims/extracted_claims/*.json`), designed to run
   **before** AEE scoring / adjudication of a claim, per the standing
   design direction (an audit stage attached to dossiers ahead of
   scoring). For one claim it executes the audit protocol's search
   discipline: at least two concept phrasings (the claim's own words
   plus caller-supplied or mechanically keyword-reduced phrasing,
   marked as to origin) across at least two independent sources;
   DOI resolution for any citations supplied; nearest-neighbor
   surfacing from the merged results, with full-text reads of
   reachable open-access neighbors. It writes a sidecar record to
   `glossa-indus/claims/research_checks/` (the claim file itself is
   never modified) and is runnable standalone:
   `python -m glossa_lab.research_check --claim-file <dossier>
   [--claim-id ID] [--alt-phrasing "..."] [--doi DOI]`.

   **Advisory invariant:** the record's `verdict` field is always
   `null`. The stage audits prior material and citations; it never
   scores a claim, never changes a claim status, and never
   adjudicates a decipherment. Scoring stays with `aee_core`;
   adjudication stays with the program's recorded gates.

3. **Doc — `docs/paper-search-mcp.md`.** The connector/usage doc,
   mirroring the RCPH one (`custom.paper-search`): tool inventory,
   call patterns, the binding audit-usage protocol (unchanged),
   measured source status and limits, operating rules.

4. **Tests — `backend/tests/test_paper_search.py`.** Offline unit
   tests: client configuration and the Sci-Hub refusal; the stage's
   plan construction (≥2 phrasings × ≥2 sources) and record shaping
   against a stubbed client, including the advisory invariant. No live
   network in the test suite; live behaviour is proven by the smoke
   record below.

## Smoke record

`specs/025-paper-search-research-check/smoke/` — run 2026-10-22 from
the Glossa tree via the stage's own client: (i) tool list; (ii) a
domain concept query on Indus decipherment prior work (plus the
protocol's second phrasing); (iii) DOI resolution
(10.1126/science.1170391, Rao et al. 2009). Raw outputs filed there;
summary in `plan.md`.

## Epistemic boundaries (H13)

- Search output is a *lead*, never evidence: nothing this tooling
  returns enters a claim dossier, score, or publication as evidence
  by itself. The audit protocol (full-text nearest neighbors,
  independent metadata verification) is what turns a lead into an
  audit finding, and that audit is the follow-on work, not this spec.
- The stage's records state what was searched, what failed, and what
  was read in full. An unreachable neighbor is recorded as an open
  gap, never as "no prior art".
- Assumptions: the shared paper-search venv remains the pinned
  install maintained from the RCPH side; Glossa's backend venv keeps
  `mcp>=1,<2`. No backend process is restarted by this work; the
  stage is inert until invoked.
- Adversarial consideration: upstream scholarly APIs rate-limit the
  shared egress IP (measured 2026-10-22: Semantic Scholar, OpenAlex,
  CORE unreachable anonymously). The stage records per-source errors
  in its record rather than treating an empty source as an empty
  literature.
