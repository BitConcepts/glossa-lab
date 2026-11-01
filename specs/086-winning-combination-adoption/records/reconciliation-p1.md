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

---

## Addendum — 2026-11-01: provenance re-trace after PR #477 (post-migration source change)

**What changed upstream.** This migration was first executed
against main `84777bca`. PR #477 (merged to main as `665414b4`,
then merged into this branch) carried the owner's 2026-11-01
lane-2 adoption act: under red-team finding RT-21, the
`not_understood` field of two source-of-record claim records
was refreshed in place in the extraction store, each with its
own dated append block on the record —

- `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
  (`glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json`;
  append block `spec074_not_understood_refresh_2026_10_25`),
- `yadav_2009_arxiv_manual_002`
  (`glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json`;
  append block `spec054_not_understood_refresh_2026_10_25`).

No other ledger source file was touched by that merge
(verified by diff: exactly these two files under
`glossa-indus/` and `specs/` bundle paths).

**How it surfaced.** CI run `41327195581` on this branch
failed `test_spec086_ledger_migration.py::test_ledger_validates_clean`
with exactly two errors, both of the form
"provenance: does_not_establish traces to no representative
source record" — ledger lines 19 and 23, the two entries
above. The validator compares each entry's
`does_not_establish` (mirrored at migration from the source
record's `not_understood`) against the `not_understood` /
`boundary` texts of the records named in the entry's
`sources` with role `source_of_record` / `bundle_aee`; the
two entries still carried the pre-refresh texts. Every
headline count in CI matched this report exactly (871 lines;
840 claims; falsifier 831/840; does-not-establish 755/840).

**The correction, and its authority.** The two claims'
`status`, `stage`, and `falsifier` are unchanged by the
upstream act (each refresh append states so, and both were
verified byte-equal against the current records:
`partially_supported` / `explained` and
`strongly_supported` / `explained`, falsification conditions
untouched). Only the mirrored `does_not_establish` texts and
the two files' source hashes had gone stale. The correction
re-executes this same D-E migration run
(`migration-2026-11-01-stage1`, same date) with the stage's
own tool against the current sources, before this stage's PR
has merged — the state has never been published. This is the
form C086-4's falsifier expressly excepts from the
append-only rule ("a D-E migration record that itself
reconciles"), and it follows this record's own precedent:
the first build's ledger hash was superseded in-stage by the
canonical-hash rebuild and recorded in `stage-1-record.md`.
An appended reclassification entry was not used: a
reclassification marks a superseded claim state (SCHEMA.md),
but a migration entry must mirror its source of record
(spec Point 6 (c)(i): a source-of-record act is "mirrored by
bundle/extraction intake"), and the intake validator checks
every migration line against its named sources — a stale
migration line cannot be cured by an appended line, only by
the migration record reconciling against the moved sources.

**Second finding, disclosed.** The re-execution also
re-traced the recorded source hash of 21 further P1 entries
(lines 1–18 and 20–22). Their recorded hashes matched no
committed state of their source files: the files are
byte-identical at the migration base `84777bca` and at HEAD,
and they hash to the values the re-execution now records.
The first execution evidently ran against the extraction
store's suite-regenerated transient bytes (the backend suite
regenerates this store in-tree); the store was later restored
to its committed state without re-running the migration, and
no Stage 1 check compares recorded source hashes, so the
drift was invisible until this diff. Only `sources[].sha256`
changed on those 21 entries — no statement, status, stage,
falsifier, or does-not-establish field moved. Entries:
`ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`,
`…_sign_val_0002`, `…_sign_val_0003`, `…_statisti_0004`,
`farmer_sproat_witzel_2004_manual_001`,
`indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001`,
`…_critique_0002`, `…_manual_001`, `…_manual_002`,
`…_manual_003`, `…_manual_004`,
`parpola_2010_dravidian_solution_manual_001`, `…_manual_002`,
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001`,
`…_sign_val_0002`,
`without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001`,
`…_manual_001`, `…_manual_002`, `…_manual_004`, `…_manual_005`,
`yadav_2009_arxiv_manual_001`.

**Reconciliation after the correction.** Unchanged, exactly:
31 P1 source records in → 23 canonical entries out (8 merged
evidence instances preserved as sources); ledger totals 871
lines = 840 claim entries (bundle 817, extracted 23) + 31
annotation entries; falsifier coverage 831 of 840 (extracted
14 of 23); does-not-establish coverage 755 of 840. The
validator over the corrected ledger reports PASS with these
counts (output re-filed at `records/stage-1-validator-output.txt`,
byte-identical text to the pre-correction filing, as the
counts did not move). Ledger SHA-256: `c4e2326e…`
(supersedes `30eb6235…`, the pre-correction build, never
published).
