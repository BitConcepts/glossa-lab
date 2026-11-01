# Spec 026 — CORE as a keyed source for the RESEARCH-CHECK stage

**Status:** Implemented 2026-10-22 on branch
`spec/026-core-research-source` (owner's mirror directive, same day:
APIs added for the RCPH program are mirrored for Glossa Lab).
**Context:** Spec 025 adopted the shared paper-search-mcp server and
built the RESEARCH-CHECK stage on it. That server's CORE source has
been dark in practice: keyless CORE calls from this network return
empty (measured 2026-10-22 and recorded in
`docs/paper-search-mcp.md`), and the server's CORE key slot is an
environment variable this project does not carry. Meanwhile the RCPH
workspace connected CORE properly — the free key registered as the
`custom.core` connection, reached through the Secure Vault surrogate
route, and verified live the same day. CORE is the largest
open-access full-text collection the protocol draws on (CORE's own
service page: 452M+ searchable records, 57M+ full texts), and the
audit protocol's nearest-neighbor rule turns on full text, not
abstracts. This spec mirrors that capability into Glossa's
research-check tooling. Tooling only: it audits nothing, and it
changes no claim, score, or status.

## What is adopted

**CORE (core.ac.uk) via the registered `custom.core` connection** —
the same route the RCPH connector
(`~/workspace/custom-connectors/custom.core/CONNECTOR.md`) proved:
an Authorization bearer surrogate from
`dynamic_credentials.py` (`/opt/muse/skills/custom-connector-setup/bin`),
swapped for the real key by the runtime only on egress to
`api.core.ac.uk`. Glossa's code never reads, prints, or stores the
key value; no `PAPER_SEARCH_MCP_CORE_API_KEY` is introduced anywhere.

## Design

1. **Client — `backend/glossa_lab/core_search.py`.** A small REST
   client in Glossa's tree (stdlib `urllib`, in the shape of the
   RCPH connector helper, which is also where its behavior contract
   comes from):
   - `search_works(query, limit)` against the canonical path
     `/v3/search/works/` — **with the trailing slash**: the slashless
     form answers 301 to the same host, and authenticated requests
     here refuse redirects by design, so the slash is part of the
     contract, not a style choice.
   - `get_work(core_id)` against `/v3/works/<id>`.
   - `normalize_work()` maps a CORE work record onto the paper shape
     the RESEARCH-CHECK stage already consumes (title, authors,
     year, doi, url, abstract) plus `has_full_text` and — in memory
     only — the `full_text` itself when CORE holds it.
   - **Pace guard:** a module-level minimum interval between network
     calls mirroring the connector's registered tier (about 5 single
     requests per 10 s → 2.1 s spacing with margin).
   - **429 is a hard stop:** the client raises `CoreRateLimitError`
     and never retries. Other HTTP failures raise `CoreError` with a
     clean message (house style: error surfaces, never silent
     empties). Every call carries an explicit timeout (H9/H11).
   - CLI: `python -m glossa_lab.core_search search '<query>' [limit]`
     / `get <core-id>` from `backend/`, SlimJSON to stdout.

   Why a client module rather than the MCP server's `search_core`:
   the server's CORE source reads its key from an environment
   variable, which the vault-surrogate route deliberately does not
   provide. The direct client is the only route that uses the
   registered connection, and it leaves the server's tool surface —
   and the 33-tool `glossa_mcp` surface — untouched, exactly as in
   spec 025's placement decision.

2. **Stage integration — `backend/glossa_lab/research_check.py`.**
   CORE becomes an additional per-phrasing source alongside the
   stage's existing roster (federated `search_papers` + per-source
   arXiv + Crossref, whose behavior is unchanged):
   - For each claim phrasing, one CORE search via the new client;
     its hits are normalized into the neighbor pool under source
     `"core"` and take part in the same dedupe, vocabulary-overlap
     ranking, and record shaping as every other source.
   - A CORE neighbor that carries full text **is its own read
     source**: when such a neighbor clears the stage's existing
     relevance gate, the read is recorded in
     `neighbors_read_full_text` (with `source: "core"` and the word
     count) without consuming an arXiv read slot and without writing
     the text itself into the sidecar.
   - A 429 from CORE stops CORE for the rest of the run (the
     connector's stop rule): the failure is recorded in
     `source_errors`, a gap entry states that remaining phrasings
     were not searched on CORE, and the run continues on the other
     sources. Other CORE errors are recorded per phrasing.
   - The client is injectable (`core_client=`), mirroring the
     existing `client=` test seam. CLI gains `--no-core` (default:
     CORE on).
   - **Advisory invariant unchanged:** sidecar format is the same
     record shape; `verdict` is still `null` by construction; claim
     files are never modified.

3. **Docs.** A CORE section in `docs/paper-search-mcp.md`
   (route, trailing-slash rule, pacing, 429 stop, the protocol
   standing that CORE is now a *reached* source, and the updated
   CORE line in the limits list), a pointer line in `AGENTS.md`,
   and this spec's entry in `LEDGER.md` (H1/H7/H8).

4. **Tests — `backend/tests/test_core_search.py`.** Offline: client
   request shape (slashed path, bearer surrogate applied, host
   guard), pace constant and pacing behavior with a fake clock,
   429 → `CoreRateLimitError` with no second attempt, CORE work
   normalization, and the stage's CORE source against stub clients
   (pool merge + ranking shape, CORE full-text read recorded,
   429 stops CORE for the run, advisory invariant). Live behaviour
   is proven by the smoke record, not the suite.

## Smoke record

`specs/026-core-research-source/smoke/` — run 2026-10-22 from the
Glossa tree: (i) two protocol phrasings of an Indus-relevant concept
query through the new client, with per-hit full-text availability
noted; (ii) one scoped end-to-end RESEARCH-CHECK run on a single
claim (Yadav 2010 n-grams dossier) with CORE among its sources, the
sidecar written to the usual place
(`glossa-indus/claims/research_checks/`). No backend process is
restarted or disturbed by any of this work.

## Epistemic boundaries (H13)

- CORE output is a *lead*, never evidence — the same boundary as
  spec 025. A CORE full text becomes an audit finding only through
  the audit protocol (nearest-neighbor full-text reading and
  independent metadata verification), which is the follow-on audit's
  work, not this spec's.
- CORE aggregates repository deposits of uneven quality: hits can
  include duplicates, mis-dated records, and non-peer-reviewed
  material. The stage records what CORE returned; ranking by
  claim-vocabulary overlap is a surfacing heuristic, not a judgment
  of a hit's quality.
- A CORE 429 or error is recorded as a source failure in the
  sidecar, never as an empty literature — the protocol's standing
  rule, applied to the new source unchanged.
- Assumptions: the `custom.core` connection stays registered with
  its current placement (bearer header, host `api.core.ac.uk`);
  the registered pace (~5 single requests per 10 s) remains the
  tier. If the connection is rotated, only the vault entry changes —
  no code in this spec holds the key.
- Working-tree caveat: this checkout carries pre-existing
  uncommitted modifications from other work (extracted-claims
  dossiers, claim reports, outputs). They are preserved untouched;
  this spec commits only its own files, by explicit path. None of
  the files this spec modifies carried uncommitted changes at
  branch time (verified by `git status`).
