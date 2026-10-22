# Paper Search MCP — connector & usage doc (Glossa Lab)

The Glossa Lab side of the shared scholarly paper-search MCP
(openags/paper-search-mcp), adopted 2026-10-22 by owner order for
three jobs: **checking research** (is a claim, derivation, or citation
real and as described?), **challenging proposed research** (what is
the strongest prior or rival work it must survive?), and **finding
prior material** before novelty is claimed. Implemented by
`specs/025-paper-search-research-check/`; the binding audit protocol
below is carried over unchanged from the RCPH connector
(`custom.paper-search` in the projected-constraints workspace).

## Server and install (shared — do not duplicate)

- **paper-search-mcp** by openags —
  https://github.com/openags/paper-search-mcp (MIT). One stdio server
  covering arXiv + Crossref + Semantic Scholar + OpenAlex + CORE +
  BASE + Europe PMC + PubMed + more, with open-access full-text
  retrieval; no key required for core function.
- The server runs from the dedicated pinned venv
  `~/workspace/venvs/paper-search-mcp`. **The `mcp` SDK pin must stay
  on the 1.x line** — the server uses the 1.x FastMCP; an `mcp>=2`
  resolution breaks it. The pinned set and rebuild recipe are
  maintained with the RCPH-side skill
  (`~/workspace/custom-skills/local-paper-search-mcp/`).
- Glossa does **not** re-install or vendor the server. Glossa's part
  is the client + stage below.

## Glossa-side tooling

- **Client:** `backend/glossa_lab/paper_search.py`, run under the
  backend venv (which already depends on `mcp>=1,<2`). It spawns the
  server via the paper-search venv interpreter and exposes
  `list_tools()` / `call_tool()` plus typed helpers (`search_papers`,
  `search_source`, `resolve_doi`, `read_full_text`). Config:
  `GLOSSA_PAPER_SEARCH_PYTHON` (server interpreter override),
  `GLOSSA_PAPER_SEARCH_TIMEOUT` (default per-call timeout, 300 s).
  CLI: `python -m glossa_lab.paper_search tools|call ...` from
  `backend/`.
- **Stage:** `backend/glossa_lab/research_check.py` — the
  RESEARCH-CHECK stage. It runs **before** AEE scoring/adjudication,
  attaches an advisory sidecar record to a claim dossier
  (`glossa-indus/claims/research_checks/<doc>__<claim>.research_check.json`),
  and never modifies the claim file, a score, or a status. Its
  record's `verdict` is always `null`: the stage audits prior
  material and citations; it does not adjudicate decipherments.
  CLI: `python -m glossa_lab.research_check --claim-file <dossier>
  [--claim-id ID] [--alt-phrasing "..."] [--doi DOI] [--out DIR]
  [--no-full-text]`.
- Optional upstream keys (Semantic Scholar / OpenAlex / CORE /
  Unpaywall email) travel only as `PAPER_SEARCH_MCP_*` environment
  variables at call time — never written into files, argv, or logs.

## Workhorse tools (via the client)

- `search_papers` — federated search (`query`, `sources`,
  `max_results`); returns deduplicated `papers` plus per-source
  `errors` — prefer it when failures must be visible. Note:
  `max_results` behaves like a global cap on the merged list; for
  per-source depth also call the per-source tools.
- Per-source: `search_arxiv`, `search_semantic`, `search_openalex`,
  `search_crossref`, `search_core`, `search_base`,
  `search_europepmc`, … (`query`, `max_results`). Some per-source
  tools return double-encoded JSON strings; the Glossa client
  normalizes that.
- `get_crossref_paper_by_doi` — canonical metadata by DOI.
- Full text (open access only): `read_arxiv_paper` (`paper_id`,
  `save_path`) and `download_with_fallback` (OA chain). **`use_scihub`
  is hard-off** — the client refuses it in code.

## Audit protocol (binding for audits that use this server)

1. **Per-claim concept queries.** For each claim under audit, run at
   least **two different concept phrasings** (the claim's own words,
   and a stranger's words for the same idea — include the mechanism,
   the quantity estimated, and the setting) across at least **two
   independent sources**, one of which is a semantic/relevance index
   (Semantic Scholar or OpenAlex) when reachable, plus arXiv and
   Crossref. Keyword indexes (arXiv especially) are brittle: a null
   from one phrasing is not a null.
2. **Nearest-neighbor rule.** From the merged results, identify the
   closest neighbors to the claim (same statistic/quantity, same
   setting, same mechanism — not just shared keywords). **Read the
   full text of every closest neighbor**, at least the sections where
   the neighbor defines its statistic and states its results.
   **Abstracts alone never establish novelty, and never establish its
   absence.** If a closest neighbor's full text cannot be reached
   through any OA route, the audit records that as an open gap — it
   does not record "no prior art".
3. **Challenge pass.** Separately from the novelty pass, run
   challenge-style queries aimed at *refuting or pre-empting* the
   claim: the rival statistic's name, the standard textbook quantity,
   the review articles in the area. Reviews are the fastest map of
   who did what first.
4. **Verify metadata independently.** Every load-bearing citation
   gets `get_crossref_paper_by_doi` (or the arXiv record) checked
   against the citing text: title, author list, venue, year, and
   that the cited equations/results are actually in the retrieved
   full text. A search snippet is never a citation.
5. **File the evidence.** Raw tool outputs (query strings, sources,
   timestamps, full JSON/text) go into the audit's own directory.
   Report which sources were queried, which failed, and which
   neighbors were read in full. An audit that cannot show its
   queries has not run.

## Limits and source status (measured 2026-10-22, this VM)

- **arXiv — works.** Search and full-text read verified live.
  Keyword search: term conjunction over title/abstract;
  phrasing-sensitive (protocol rule 1). **Measured trap
  (2026-10-22, spec 025 smoke): a conjunction that matches nothing
  can return a default high-profile list (ATLAS / gravitational-wave
  papers) instead of an empty result.** Treat arXiv hits sharing no
  vocabulary with the query as suspect, never as neighbors; the
  RESEARCH-CHECK stage ranks neighbors by claim-vocabulary overlap
  for exactly this reason.
- **Crossref — works.** Search and DOI resolution verified live.
  Metadata only; no full text.
- **Semantic Scholar — rate-limited anonymously.** Anonymous API
  returned 429 on repeated attempts (shared egress-IP pool). Remedy:
  free key via `PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY`. Optional.
- **OpenAlex — rate-limited anonymously.** Anonymous daily quota
  exhausted (HTTP 429) via the shared egress IP. Remedy: free key
  (`PAPER_SEARCH_MCP_OPENALEX_API_KEY`) and/or
  `PAPER_SEARCH_MCP_OPENALEX_EMAIL`. Optional.
- **CORE — keyless use returns empty** (hard unauthenticated
  rate-limiting). Remedy: free key (`PAPER_SEARCH_MCP_CORE_API_KEY`).
- **Unpaywall — disabled** until `PAPER_SEARCH_MCP_UNPAYWALL_EMAIL`
  is set (any valid contact email; API courtesy field).
- **BASE — expected empty** from here: its OAI-PMH endpoint requires
  institutional IP registration. Treat BASE as unsearched.
- **Google Scholar — unreliable by design** (bot detection); never
  the sole source for a negative result.
- Full text is **open-access only**. Paywalled neighbors are a
  recorded gap, routed — if the owner directs — to a separate
  discovery tier, never to this connector's Sci-Hub tool.
- Rate discipline: calls are serial; a 429 ends that source's use
  for the session — switch sources and note the gap; do not
  retry-loop.
- Full-text reads are slow (PDF download + parse, server logs are
  verbose): budget minutes per read and run long stage invocations
  detached with output to a file.

## Operating rules

1. Read this doc before an audit; take arguments from the tool list
   (`python -m glossa_lab.paper_search tools`) and the examples
   here, not from memory of other servers.
2. Everything this server returns is a *lead* until the audit
   protocol has been applied to it. Search output never goes into a
   dossier, score, paper, or registration as evidence by itself.
3. The RESEARCH-CHECK stage is advisory. Its records inform audits;
   they do not move claims, anchors, or scores. Corrections arising
   from an audit follow Glossa's own record rules (append-only
   corrections; frozen records are never silently rewritten).
4. Keep downloads and audit outputs in the audit's own directories,
   not loose in the tree.
