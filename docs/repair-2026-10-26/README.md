# External-audit repair — 2026-10-26

This directory and the accompanying code changes implement the repair
brief commissioned after the external audit of this program's evidence
chain (audited snapshot `cc9ffeb4`; baseline for this patch: main
`d80dcb7c`). The brief's rule throughout: historical records, frozen
specifications, registrations, and verdicts are preserved byte-for-byte;
corrections land as new versioned code, overlays, errata, and corrected
current prose — never as edits to history.

## Change summary

**New versioned code (old code untouched, still in tree for the record):**

- `backend/glossa_lab/phonotactics_v2.py` — phonological checker that
  preserves transliteration contrasts (the Phase-58 checker deleted the
  retroflexes it was meant to test for, and returned PASS for
  uncheckable input). Unrecognized input is now UNCHECKABLE, slash
  alternatives are judged individually, and every result is labeled
  initials-only. `backend/tests/test_repair_phonotactics_v2.py`.
- `backend/glossa_lab/site_stats_v2.py` — chi-square with validated
  integer counts and a standard-library incomplete-gamma p-value (the
  Phase-69 routine could only ever emit p ∈ {0.0, 0.5, 1.0}). No
  "invariance" verdict: difference detection only; equivalence requires
  a prespecified margin and is otherwise NOT_ASSESSED.
  `backend/tests/test_repair_site_stats_v2.py`.
- `backend/glossa_lab/crosswalk_provenance.py` +
  `backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_provenance.json`
  — provenance classification of all 184 crosswalk entries. Result:
  **0 comparisons are eligible as independent validation** (116 entries
  carry the project's own readings copied under a "Parpola 1994" source
  label). The original crosswalk file is unmodified.
  `backend/tests/test_repair_crosswalk_provenance.py`.
- `backend/glossa_lab/corpus_frames.py` — gap-aware inscription frames
  alongside the historical compressed frame; "initial" must name its
  boundary semantics; repeated-identifier cross-scheme joins block
  instead of silently taking the first match.
  `backend/tests/test_repair_corpus_frames.py`.
- `backend/glossa_lab/replay076.py` — safe replay wrapper for the
  frozen Spec 076 pilot: hash gate before computation, honest
  hash-provenance labels, new-output-directory rule, census checks.
  Demonstrated: byte-identical reproduction of the archived
  pilot-results.json with the frozen tree provably unchanged.
  `backend/tests/test_repair_replay076.py`; manifest example in this
  directory.
- `backend/scripts/repair_anchor_audit.py` — generator for the anchor
  support audit in this directory (`anchor-support-audit.json`): all 94
  strict-core entries and the 30 Phase-48 promotions with sourced
  per-sign dispositions. No promotion survives as supported; three
  promotions rest wholly on pass-by-default credits.
- `backend/scripts/repair_dry_run_invalidation.py` — the WP1
  containment proof over `dependency-map.json`.

**Corrected current prose:** the root `README.md` (banner, metrics
table, research-status section, citation of record → preprint v9, DOI
10.5281/zenodo.23668053). Withdrawn quantities are withdrawn, not
replaced with new numbers: no corrected phonotactic count has been run,
and no site-invariance equivalence has been established.

**Documents in this directory:** `baseline-and-dispositions.md`
(finding-by-finding), `dependency-map.md` / `.json`,
`claim-status-overlay.json`, `anchor-support-audit.json`,
`spec076-replay-manifest.example.json`, `wp7-prospective-redesign.md`,
`wp8-exposure-and-controls.md`, `wp9-study-preparations.md`.

## What this patch does not do

It does not revalidate any reading. Dependent corpus claims remain
unvalidated until a corrected analysis is run under a linguist-reviewed
rule set; three anchor entries await expert adjudication; the
contact-zone sequence study remains gated on the CISI Volume 3
transcription; the numeral validation pilot is closed as unavailable
for lack of independent constraints. Software correctness, historical
reproducibility, and scientific validity are separate questions, and a
passing test suite answers only the first.
