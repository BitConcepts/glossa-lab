# Reconciliation — P1 extracted claims (Spec 086 Stage 1, T104)

Migration run: `migration-2026-11-01-stage1`, 2026-11-01. Source store:
`glossa-indus/claims/extracted_claims/` (10 files,
read-only). Grouping: proposition fingerprint under
`spec029-phase-i-v1` (D-B); the canonical record of each group
is the one the store itself leaves unmerged (no `merged_into`),
and every merged record's `merged_into` was verified to name
its group's canonical.

## Headline counts

| Measure | Count |
|---|---|
| Source records in | 31 |
| Canonical ledger entries out | 23 |
| Merged evidence instances (preserved as sources, D-B) | 8 |
| Fingerprint groups with >1 source record | 5 |

## Merged evidence instances

Each instance's own status/stage remains in its source record
(below, for the record); under D-B the proposition's canonical
entry carries the canonical record's status/stage, verified
byte-equal against that record by this report's check.

| Instance claim id | Canonical entry | Instance status (source) | Instance stage (source) |
|---|---|---|---|
| fuls2023_catalog_of_indussigns_searchins_1dbdecdb_statisti_0001 | ancient_writing_and_modern_technologies_51831ac9_statisti_0004 | untested | created |
| positional_analysis_of_indus_signs_a2bedc93_statisti_0001 | ancient_writing_and_modern_technologies_51831ac9_statisti_0004 | untested | created |
| the_archaeology_and_epigraphy_of_indus_w_27f45a68_statisti_0003 | ancient_writing_and_modern_technologies_51831ac9_statisti_0004 | untested | created |
| without_kings_or_conquests_the_indus_scr_ce9d98cc_statisti_0002 | ancient_writing_and_modern_technologies_51831ac9_statisti_0004 | untested | created |
| yadav_2010_ngrams_manual_002 | yadav_2009_arxiv_manual_002 | strongly_supported | checked |
| without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0004 | indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002 | untested | created |
| without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0003 | indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001 | untested | created |
| yadav_2010_ngrams_manual_001 | yadav_2009_arxiv_manual_001 | strongly_supported | checked |

## Fingerprint groups with >1 source record

- `a4874349e0cc…` canonical `ancient_writing_and_modern_technologies_51831ac9_statisti_0004` with 5 source records: `ancient_writing_and_modern_technologies_51831ac9_statisti_0004`, `fuls2023_catalog_of_indussigns_searchins_1dbdecdb_statisti_0001`, `positional_analysis_of_indus_signs_a2bedc93_statisti_0001`, `the_archaeology_and_epigraphy_of_indus_w_27f45a68_statisti_0003`, `without_kings_or_conquests_the_indus_scr_ce9d98cc_statisti_0002`
- `c5d0f0575c83…` canonical `yadav_2009_arxiv_manual_002` with 2 source records: `yadav_2009_arxiv_manual_002`, `yadav_2010_ngrams_manual_002`
- `d7e4efd6b774…` canonical `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002` with 2 source records: `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002`, `without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0004`
- `defa7480501b…` canonical `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001` with 2 source records: `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001`, `without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0003`
- `fdd32acf462b…` canonical `yadav_2009_arxiv_manual_001` with 2 source records: `yadav_2009_arxiv_manual_001`, `yadav_2010_ngrams_manual_001`

## Coverage (canonical entries)

- Falsifier: 14 of 23 entries carry
  one. Source records carrying a falsification condition
  (the store's field is `falsification_condition`):
  15 of
  31. The remaining gap is recorded as
  `falsifier: null`, never filled (D-086-Q6). Note for the
  record: the Spec 086 package's premise "0 of 31 carry a
  falsifier field" referred to a field literally named
  `falsifier`; the store carries the same content under
  `falsification_condition` on the records counted here, and
  the migration carries it where present.
- Does-not-establish (`not_understood`): 23 of
  23 entries.
- Explanation records (OD-2, named human author): 23
  of 23 entries.
- AEE state: 0 of 23 entries — the source records
  carry no scores; `aee_state` is null, shown as null.
- Confidence (harmonization adoption #3 item 6, binding —
  narrative confidence is not a number): every source record
  carries `confidence_in_source` as a NUMBER (float; 31 of 31
  records, all numeric — a full-store census found no
  qualitative confidence value in this population). Each
  canonical entry carries its canonical record's value
  verbatim in `confidence_in_source`; the 8 merged instances'
  values were checked against their canonicals' (differences:
  0). `confidence_text` is null on every entry: no narrative
  confidence exists in the source, and none was manufactured.
  Intake rule, enforced by the shared builder: a qualitative
  confidence string is carried verbatim into
  `confidence_text` and never normalized into a number.
- Unresolved sign mentions: 6 source records
  carry free-text `signs_involved` with no identifier-bearing
  field; they are NOT resolved into `sign_refs` (identifier
  fields only). Records: `indus_valley_script_deciphered_from_myth_65ff0a26_manual_002`, `indus_valley_script_deciphered_from_myth_65ff0a26_manual_003`, `indus_valley_script_deciphered_from_myth_65ff0a26_manual_004`, `parpola_2010_dravidian_solution_manual_002`, `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`, `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`.

## Mirror check

Every canonical entry's `status` and `stage` were compared
byte-equal against its source-of-record claim record after
the build; the migration test
(`test_spec086_ledger_migration.py`) re-runs this comparison
in CI. Status or stage differences: none (any difference
would be listed here and would stop the stage).
