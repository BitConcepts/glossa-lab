# Contact-Zone Outputs — Provenance Note (2026-10-25, programme red team, finding C-8)

The contact-zone outputs in this directory were computed from
source datasets that were **lost** (holdings reconciliation
2026-10-25, items #28–30) and **rebuilt the same day** (PRs
#397/#398; tracked at
`glossa-corpus/indus/sources/contact-zone-rebuilt-2026-10-25/`
with their provenance record). Read them with that history:

- `contact_zone_results.json` is a 52-byte error stub
  (`{"error": "Experiment 'contact_zone' not found"}`), not a
  result. It is left in place as the record of that state and
  must not be cited as a finding.
- `phase46_t1_contact_zone.json`, `phase60_contact_deep.json`
  and `phase60b_contact_investigation.json` are surviving
  derived outputs whose original inputs no longer exist at
  their referenced paths. The phase46 fingerprint (1,462
  tablets; keyword/period/provenience distributions) is the
  reconciliation target the rebuilt meluhha file matches
  exactly; the phase60 outputs have no equivalent verification.
- The rebuilt files are **new files with new provenance — not
  the lost originals**, and per-field provenance differs by
  file (verbatim / re-derived / reconstructed; see the rebuild
  provenance record, including its disclosure that the seals
  file's per-seal type/period pairings are reconstructions
  fitted to the lost aggregates). The rebuilt Laursen file is a
  5-of-121-row fragment; its top-level
  `n_inscribed_with_indus_text` = 23 is the lost parse's
  figure, not a count over its 5 rows.
- The loader (`backend/glossa_lab/data/mesopotamian_contact.py`)
  reads from `corpora/downloads/contact_zone/…` (gitignored)
  and returns empty results silently when files are missing.
  The tracked rebuilt copies must be copied to those paths
  before the loader sees them; an empty result from this
  module is not evidence of an empty dataset.

*This note establishes the provenance status of this outputs
tree as of 2026-10-25. It does not establish that any output
here is numerically wrong.*
