# Fix WS2 — Unpaywall configuration proof (2026-10-22)

Commission: configure an Unpaywall email for the paper-search connector
per `~/workspace/custom-connectors/custom.paper-search/CONNECTOR.md` and
prove the fix by re-running one of the audit session's failed
Crossref-DOI full-text downloads, identity-checking whatever comes back.

## What the connector doc prescribes

Unpaywall is disabled until `PAPER_SEARCH_MCP_UNPAYWALL_EMAIL` is set.
The doc's mechanism is explicit: the address is an API courtesy field,
set from the caller's environment at call time — *"no address is baked
into these files"* and keys/addresses travel only as
`PAPER_SEARCH_MCP_*` environment variables, never written into files,
argv, or logs. There is therefore no config file to edit; "configure"
means running the connector with the variable set. The program contact
email `tpierson@bitconcepts.tech` (the preprint's contact address in
`docs/research/PREPRINT_VERSIONING.md`) was used, set transiently in the
environment only.

Tool pattern (from the doc):
`PS = ~/workspace/venvs/paper-search-mcp/bin/python ~/workspace/custom-skills/local-paper-search-mcp/bin/paper_search_mcp.py`

## Proof runs — DOI 10.1371/journal.pone.0009506 (Yadav et al. 2010, PLoS ONE)

This is the DOI whose audit-session download returned an unrelated
cotton-transcriptome PDF (audit method note; `raw/W1_dl_yadav2010.json`).

1. **`search_unpaywall`** (with the email set): exit 0. Unpaywall
   reports the work open access (`is_oa: true`, journal_is_oa: true,
   oa_status: gold) with three OA locations, including the PubMed
   Central PDF (`https://pmc.ncbi.nlm.nih.gov/articles/PMC2841631/pdf/pone.0009506.pdf`).
   **The Unpaywall leg works with the email configured.**

2. **`download_with_fallback` via source `crossref`** (with the email
   set): **still defective, twice over.** The server's own post-download
   stat stage crashed (`TypeError: stat: path should be string… not
   NoneType` — the server stat'd a `None` mtime; a server-side tooling
   bug), and the PDF it had in fact downloaded was the **wrong paper**:
   Rawat et al. 2023, a nanomaterials article (Cellulose 30:3945–3966,
   DOI 10.1007/s10570-023-05065-4), 4,802,816 bytes, SHA-256
   `c111a9d5…` — identity-checked against the Crossref record for the
   requested DOI and rejected. This is the second distinct wrong
   artifact this route has served for this DOI (the audit session got a
   cotton-transcriptome paper). One attempt only; no retry loop.

3. **`download_with_fallback` via source `europepmc`, paper_id
   `PMID:20333254`** (same DOI; the route that recovered the paper in
   the audit session): exit 0 in ~15 s; returned
   `europepmc_PMID20333254_Statistical_analysis_of_the_Indus_script_using_n-g.pdf`,
   2,209,513 bytes, SHA-256
   `b3e79817db04dfd86897604ba7776cf0c5c1200341f30fc3dd91722e07e76eb6`.
   **Identity check (first-hand, coordinator):** the first page reads
   "Statistical Analysis of the Indus Script Using n-Grams — Nisha
   Yadav, Hrishikesh Joglekar, Rajesh P. N. Rao, Mayank N. Vahia,
   Ronojoy Adhikari, Iravatham Mahadevan", with the citation line
   "Yadav N, et al. (2010) … PLoS ONE 5(3): e9506.
   doi:10.1371/journal.pone.0009506" printed on the page. **This is the
   correct paper.** The extracted first page is filed as
   `raw/fix_ws2_yadav2010_first_page.txt` (PDFs are not committed, per
   the repo's PDF policy).

## Verdict

- **Configured and proven:** the Unpaywall email (env mechanism, per the
  connector doc) — `search_unpaywall` returns full OA location data,
  and an end-to-end full-text download of the audit session's failed DOI
  succeeds **via the Europe PMC route** and passes identity check.
- **Still defective (recorded, not papered over):** the `crossref`
  source route of `download_with_fallback` serves wrong artifacts for
  this DOI and the server's stat stage then crashes. Until that is
  fixed upstream, the standing discipline is: prefer the
  europepmc/pmc routes with explicit paper ids, and **identity-check
  every downloaded artifact against its Crossref record before reading
  it** — a "successful" download is not evidence of identity (the same
  lesson the audit recorded, and the program's served-artifact identity
  rule).
