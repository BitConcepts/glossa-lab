# Material Audit 2026-10-22 — plan (H2/H13)

**Commission:** Owner order 2026-10-22 (Glossa Lab chat): audit Glossa's
own material with the paper-search MCP under the binding protocol in
`docs/paper-search-mcp.md`. Tooling: spec 025 (branch
`spec/025-paper-search-research-check`, main merged in at `a5a65f86`).

## Scope

1. All 31 claims in `glossa-indus/claims/extracted_claims/*.json`
   (10 dossiers) get a RESEARCH-CHECK stage record
   (`glossa-indus/claims/research_checks/`). Deep treatment (challenge
   queries per protocol rule 3 + source-paper citation verification
   per rule 4) for the load-bearing set: every claim whose recorded
   status is not `untested` (13: 4 strongly_supported, 3
   partially_supported, 1 partially_falsified, 1 unsupported,
   4 contradicted) plus the tripartite-grammar and positional-analysis
   claims the preprint's headline assertions rest on.
2. Every citation in the preprint
   (`glossa-corpus/indus/pierson_2026_indus_decipherment.tex`,
   23 reference entries) verified against Crossref/arXiv metadata;
   load-bearing ones additionally checked for the cited result in the
   retrieved full text where an OA route exists.
3. Citations relied on by the anchor dossiers
   (`reports/phase128_evidence_dossiers_44.json`,
   `reports/phase109_dossier_*.json`, `reports/phase110_m222_dossier.json`)
   inventoried; load-bearing ones verified as in (2).
4. Challenge pass (protocol rule 3) for the preprint's three headline
   assertions: the 161 anchors; the three-slot positional grammar;
   the Dravidian reading family.

## Epistemic boundaries (H13)

- The RESEARCH-CHECK stage is advisory; its records' verdicts are null
  by construction. This audit changes no claim status, anchor, or
  score. Findings that imply a correction are filed as dated
  correction notes or correction PROPOSALS marked gate-pending where
  the program's own gates (H21/H26, AEE adjudication) must run.
- Abstract-level findings are labelled "at abstract level" in every
  report line and correction note that uses them (abstract-bound
  rule, AGENTS.md 2026-10-22). Only full-text reads support
  unqualified statements.
- Unreachable full texts are open gaps, never "no prior art".
- A 429 from any source ends that source for the session; the gap is
  recorded and another source is used. No retry loops.
- Sci-Hub is hard-off. No scholar is contacted (H14). No
  adjudication of any decipherment is performed.
- If corrections produce a new preprint version, it is flagged
  "adversarial pass required before submission" — nothing is
  submitted.

## Evidence filing

Raw outputs (queries, sources, timestamps, JSON) in this directory's
`raw/`; stage sidecars in `glossa-indus/claims/research_checks/`
(stage convention; downloaded PDFs there are gitignored per repo
policy). Final report: `AUDIT_REPORT.md` in this directory.
Ledger entries: audit opening + each correction batch (H1).
