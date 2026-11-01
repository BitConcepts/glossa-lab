# Spec 086 — Stage 2 record: the matrix generator (T201–T203)

Date: 2026-11-01. Branch: `feat/086-matrix-generator` (off
main `bf7e4f83`, the Stage 1 merge). This record is the
Stage 2 closeout required by T203: the generator output and
coverage block are filed verbatim below, with the claim
assessments for the Stage 2-scope claims. Standing position,
unchanged by anything in this stage: **the Indus script is
not deciphered**; the matrix is the ledger in matrix form,
and no cell in it is a decipherment result.

## What was built

- `glossa-indus/matrix/DEFINITIONS.md` — `matrix-defs v1`
  (T201): the registered column classes, derivation rules
  R1–R6, the R3 outcome table, and the named evidence
  registers, with machine copies registered in the
  generator.
- `backend/glossa_lab/matrix_generate.py`, invoked as
  `tools/ledger/generate_matrix.py` (T202): a pure builder
  (`build_matrix`) plus a thin write wrapper
  (`write_matrix`), per harmonization adoption 3 item 5.
  It reads only the ledger and the registers DEFINITIONS.md
  §1 names, and writes `glossa-indus/matrix/matrix.json` and
  `matrix.md`.
- The measurement entry kind, implemented additively in
  `glossa-indus/ledger/ledger-schema.json`,
  `backend/glossa_lab/ledger_intake.py`, and
  `glossa-indus/ledger/SCHEMA.md` (disposition below).
- `backend/tests/test_spec086_matrix.py` — 20 tests.

## DEFINITIONS.md — the key semantic choices (owner's oracle read)

T201's acceptance is human-as-oracle. The choices that
carry semantic weight, stated plainly:

1. **Registers are reached only through the ledger.** The
   generator reads a source record only via an entry's
   `sources[]` pointer, and only after the file's canonical
   hash verifies against the hash the entry records. A
   mismatch refuses generation. (The stored direction and
   outcome data the rules need lives in those source
   records, not in ledger fields; deriving it from anywhere
   else would be guessing.)
2. **The R3 outcome table is asymmetric by design.** Only
   three recorded outcome strings bear on a claim —
   `NOT SUPPORTED`, `INCONSISTENT`, `NOT NUMERAL-LIKE` —
   and all three map to `opposes`. **No study outcome maps
   to `supports` in v1**: the studies in this corpus test
   claims; a test that does not refute is recorded
   non-bearing, never as support. Everything else
   (`INCONCLUSIVE`, `IDENTIFICATION FAILED`, `RECOVERED`,
   administrability outcomes) is non-bearing and is listed
   in the coverage block with its reason.
3. **The latest-dated outcome block governs.** Where a
   study appended more than one outcome for one claim, the
   cell follows the latest; every block is cited, and the
   superseded blocks are listed in coverage. (This is the
   Spec 054 / Yadav construction: the 2026-10-24
   `STRICT CORPUS NOT PINNABLE` append mints nothing; the
   2026-10-25 `NOT SUPPORTED` re-execution mints the
   `opposes` cell, citing both.)
4. **A claim's own document is provenance, not a cell**,
   and **`depends_on`-type references carried in
   `evidence_refs` are not cells in v1** (they are
   claim×claim, not claim×evidence). The 790 such pairs are
   counted and listed in the matrix's coverage data, not
   dropped silently.
5. **The research-check verdict table (R5) is registered
   empty in v1.** All 31 annotation sidecars carry
   `verdict: null`, and under Spec 025 a research check is
   advisory and never adjudicates. Result: 31 research-check
   columns exist and all 31 are unused, stated in coverage
   rather than hidden.
6. **Anchors (R4) yield zero cells today, on the record.**
   The ledger's only `sign_refs` (`mahadevan:72/64/70`)
   name anchors that are absent from the canonical anchors
   register, so no anchor record with a recorded reading
   exists for them; the three refs are listed as unresolved
   in coverage. No anchor relation was manufactured.
7. **The sign×sign block is the existing pipeline's output
   as emitted** — same corpus snapshot (the registered V1
   export, canonical hash in the artifact), same call-site
   parameters as `analyze_script.py` §6. The pipeline
   reports 1,631 edges and emits the top 200 edge records;
   both numbers are carried, labeled. Sign ids are the
   corpus loader's integer ids rendered `sign-int:<n>`,
   not relabeled with a frame name the loader does not
   guarantee.
8. **The as-of stamp carries no wall clock.** It records
   the ledger's canonical hash, line count, and latest
   entry date, plus `ledger-schema v1` and
   `matrix-defs v1`. A wall-clock generation time would
   make C086-7's byte-identity impossible; the stamp's
   date is the ledger's (see the C086-18 assessment).

## Generator output — verbatim (including the coverage block)

```text
Matrix generation — glossa-indus/matrix/ (matrix-defs v1; ledger-schema v1)
generated from: glossa-indus/ledger/claims.jsonl
ledger sha256: c4e2326ec8757bb700dac0142dd0adf17d7464b4d929f5b103868c9228f13ccf
ledger lines: 871; ledger date: 2026-11-01
rows: 840 claims (826 with at least one cell; 14 empty)
columns: studies 10, documents 316, research_checks 31, anchors 287, corpus_texts 0
cells: 1363 (supports 1356, opposes 7, constrains 0)
cells by class: studies 7, documents 1356, research_checks 0, anchors 0, corpus_texts 0
falsifier coverage: 831 of 840 claim entries carry a falsifier
falsifier coverage by population: bundle 817/817, extracted 14/23
Coverage
empty rows: 14
  ancient_writing_and_modern_technologies_51831ac9_sign_val_0002, ancient_writing_and_modern_technologies_51831ac9_sign_val_0003, indus_valley_script_deciphered_from_myth_65ff0a26_manual_001, indus_valley_script_deciphered_from_myth_65ff0a26_manual_002, indus_valley_script_deciphered_from_myth_65ff0a26_manual_003, indus_valley_script_deciphered_from_myth_65ff0a26_manual_004, parpola_2010_dravidian_solution_manual_001, parpola_2010_dravidian_solution_manual_002, the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001, the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002, without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001, without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_002, without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004, without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_005
unused columns (studies): 6 of 10
  046, 047, 051, 056, 063, 064
unused columns (documents): 0 of 316
unused columns (research_checks): 31 of 31
  glossa-indus/claims/research_checks/ancient_writing_and_modern_technologies_51831ac9__ancient_writing_and_modern_technologies_51831ac9_sign_val_0001.research_check.json, glossa-indus/claims/research_checks/ancient_writing_and_modern_technologies_51831ac9__ancient_writing_and_modern_technologies_51831ac9_sign_val_0002.research_check.json, glossa-indus/claims/research_checks/ancient_writing_and_modern_technologies_51831ac9__ancient_writing_and_modern_technologies_51831ac9_sign_val_0003.research_check.json, glossa-indus/claims/research_checks/ancient_writing_and_modern_technologies_51831ac9__ancient_writing_and_modern_technologies_51831ac9_statisti_0004.research_check.json, glossa-indus/claims/research_checks/farmer_sproat_witzel_2004__farmer_sproat_witzel_2004_manual_001.research_check.json, glossa-indus/claims/research_checks/fuls2023_catalog_of_indussigns_searchins_1dbdecdb__fuls2023_catalog_of_indussigns_searchins_1dbdecdb_statisti_0001.research_check.json, glossa-indus/claims/research_checks/indus_valley_script_deciphered_from_myth_65ff0a26__indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001.research_check.json, glossa-indus/claims/research_checks/indus_valley_script_deciphered_from_myth_65ff0a26__indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002.research_check.json, glossa-indus/claims/research_checks/indus_valley_script_deciphered_from_myth_65ff0a26__indus_valley_script_deciphered_from_myth_65ff0a26_manual_001.research_check.json, glossa-indus/claims/research_checks/indus_valley_script_deciphered_from_myth_65ff0a26__indus_valley_script_deciphered_from_myth_65ff0a26_manual_002.research_check.json, glossa-indus/claims/research_checks/indus_valley_script_deciphered_from_myth_65ff0a26__indus_valley_script_deciphered_from_myth_65ff0a26_manual_003.research_check.json, glossa-indus/claims/research_checks/indus_valley_script_deciphered_from_myth_65ff0a26__indus_valley_script_deciphered_from_myth_65ff0a26_manual_004.research_check.json, glossa-indus/claims/research_checks/parpola_2010_dravidian_solution__parpola_2010_dravidian_solution_manual_001.research_check.json, glossa-indus/claims/research_checks/parpola_2010_dravidian_solution__parpola_2010_dravidian_solution_manual_002.research_check.json, glossa-indus/claims/research_checks/positional_analysis_of_indus_signs_a2bedc93__positional_analysis_of_indus_signs_a2bedc93_statisti_0001.research_check.json, glossa-indus/claims/research_checks/the_archaeology_and_epigraphy_of_indus_w_27f45a68__the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001.research_check.json, glossa-indus/claims/research_checks/the_archaeology_and_epigraphy_of_indus_w_27f45a68__the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002.research_check.json, glossa-indus/claims/research_checks/the_archaeology_and_epigraphy_of_indus_w_27f45a68__the_archaeology_and_epigraphy_of_indus_w_27f45a68_statisti_0003.research_check.json, glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0003.research_check.json, glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_critique_0004.research_check.json, glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001.research_check.json, glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001.research_check.json, glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_002.research_check.json, glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003.research_check.json, glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004.research_check.json, glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_005.research_check.json, glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_statisti_0002.research_check.json, glossa-indus/claims/research_checks/yadav_2009_arxiv__yadav_2009_arxiv_manual_001.research_check.json, glossa-indus/claims/research_checks/yadav_2009_arxiv__yadav_2009_arxiv_manual_002.research_check.json, glossa-indus/claims/research_checks/yadav_2010_ngrams__yadav_2010_ngrams_manual_001.research_check.json, glossa-indus/claims/research_checks/yadav_2010_ngrams__yadav_2010_ngrams_manual_002.research_check.json
unused columns (anchors): 287 of 287
  H003, M001, M002, M003, M004, M005, M006, M007, M008, M009, M010, M011, M012, M013, M014, M015, M016, M017, M018, M019, M020, M021, M022, M023, M024, M025, M026, M027, M028, M029, M030, M031, M032, M033, M034, M035, M036, M037, M038, M039, M040, M041, M042, M043, M044, M045, M046, M047, M048, M049, M050, M051, M052, M053, M054, M055, M056, M057, M058, M059, M060, M061, M062, M063, M064, M065, M066, M067, M068, M069, M070, M071, M072, M073, M074, M075, M076, M077, M078, M079, M080, M081, M082, M087, M089, M099, M100, M101, M102, M103, M104, M105, M106, M107, M108, M109, M111, M112, M115, M116, M117, M118, M120, M123, M124, M125, M126, M127, M128, M129, M130, M131, M133, M134, M135, M136, M137, M138, M140, M143, M145, M146, M147, M149, M151, M153, M155, M156, M157, M158, M162, M163, M164, M165, M168, M169, M170, M175, M176, M177, M178, M181, M183, M185, M186, M190, M192, M193, M194, M195, M197, M198, M200, M201, M202, M203, M207, M208, M209, M210, M211, M213, M214, M217, M218, M219, M220, M221, M222, M223, M224, M226, M227, M230, M231, M233, M235, M237, M239, M240, M242, M243, M245, M247, M249, M250, M251, M252, M254, M255, M256, M258, M259, M260, M261, M262, M264, M267, M270, M272, M274, M277, M278, M280, M281, M286, M287, M293, M295, M297, M298, M301, M303, M304, M305, M307, M309, M310, M311, M312, M314, M316, M318, M320, M321, M322, M323, M324, M327, M328, M329, M330, M332, M334, M336, M339, M340, M341, M342, M345, M346, M347, M350, M351, M354, M355, M356, M357, M359, M360, M362, M363, M364, M365, M367, M369, M370, M374, M375, M378, M379, M380, M381, M382, M383, M386, M387, M388, M389, M390, M391, M392, M394, M396, M397, M398, M400, M401, M402, M405, M406, M407, M408, M412, M413, M415, M416
unused columns (corpus_texts): 0 of 0
unresolved sign mentions: 14
  indus_valley_script_deciphered_from_myth_65ff0a26_manual_002: fish sign family (glossa-indus/claims/extracted_claims/indus_valley_script_deciphered_from_myth_65ff0a26.json)
  indus_valley_script_deciphered_from_myth_65ff0a26_manual_003: arrow sign (glossa-indus/claims/extracted_claims/indus_valley_script_deciphered_from_myth_65ff0a26.json)
  indus_valley_script_deciphered_from_myth_65ff0a26_manual_004: horned deity sign (glossa-indus/claims/extracted_claims/indus_valley_script_deciphered_from_myth_65ff0a26.json)
  parpola_2010_dravidian_solution_manual_002: fish sign family (glossa-indus/claims/extracted_claims/parpola_2010_dravidian_solution.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003: buffalo (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003: elephant (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003: fish (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003: rhinoceros (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003: tiger (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003: unicorn (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004: crescent (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004: seven-petaled (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004: star (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
  without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004: sun (glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json)
sign refs without an anchor record: 3
  parpola_2010_dravidian_solution_manual_002: mahadevan:64 — no anchor record under this key
  parpola_2010_dravidian_solution_manual_002: mahadevan:70 — no anchor record under this key
  parpola_2010_dravidian_solution_manual_002: mahadevan:72 — no anchor record under this key
study outcome blocks not bearing: 7
  indus_valley_script_deciphered_from_myth_65ff0a26_manual_001 x study 047: INCONCLUSIVE (classification gate, spec section 6.3) (2026-10-21) — governing outcome is non-bearing [glossa-indus/claims/extracted_claims/indus_valley_script_deciphered_from_myth_65ff0a26.json:indus_valley_script_deciphered_from_myth_65ff0a26_manual_001#spec047_step2]
  indus_valley_script_deciphered_from_myth_65ff0a26_manual_003 x study 051: INCONCLUSIVE — THE CLASSIFICATION IS THE FINDING (2026-10-21) — governing outcome is non-bearing [glossa-indus/claims/extracted_claims/indus_valley_script_deciphered_from_myth_65ff0a26.json:indus_valley_script_deciphered_from_myth_65ff0a26_manual_003#spec051_execution]
  the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001 x study 056: IDENTIFICATION FAILED (2026-10-21) — governing outcome is non-bearing [glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json:the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001#spec056_closure]
  the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001 x study 063: RECOVERED (2026-10-22) — governing outcome is non-bearing [glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json:the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001#spec063_restatement]
  the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002 x study 046: IDENTIFICATION FAILED (sign unmatched) (2026-10-21) — governing outcome is non-bearing [glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json:the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002#first_check]
  the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002 x study 064: IDENTIFICATION FAILED (continuity/discrimination not sustained) (2026-10-22) — governing outcome is non-bearing [glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json:the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002#spec064_check]
  yadav_2009_arxiv_manual_002 x study 054: STRICT CORPUS NOT PINNABLE (2026-10-24) — superseded by a later outcome block from the same study [glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json:yadav_2009_arxiv_manual_002#spec054_outcome_append_2026_10_24]
dependency pairs carried in evidence_refs (not matrix cells under matrix-defs v1): 790
Sign×sign block (imported from the existing pipeline)
pipeline: glossa_lab.pipelines.cooccurrence.build_cooccurrence_network {'window': 2, 'min_freq': 3, 'min_edge_weight': 2}
corpus: glossa-corpus/indus/exports/indus_research.jsonl sha256 08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e
sequences: 2784; sign tokens: 11705
nodes: 80; edges: 1631 reported by the pipeline (200 edge records emitted); communities: 1
RESULT: GENERATED
```

## Byte-identity proof (C086-7 acceptance)

Generated artifacts (canonical SHA-256, the ledger tooling's
shared helper):

- `matrix.json`: `b3cdbf49e6305ae771468f26858678db568d1b58cb0b200e55b92810adb29849` (746,668 bytes)
- `matrix.md`: `7c963ff55c38d4dc9a52d240dacb03da0f2eebfaff5411cc398144727140b255` (38,488 bytes)

Both files were then deleted and regenerated from the
unchanged ledger: `cmp` reports the regenerated files
byte-identical to the first generation, the generator's
printed output identical across runs, and
`generate_matrix.py --check` reports `CHECK: MATCH`.
The committed artifacts equal a fresh pure build, pinned
in CI by `test_committed_matrix_is_byte_identical_to_fresh_build`.

## Sampled cells, traced to their stored records

Four cells were traced by hand, independently of the
generator, to the records they cite (the test file
additionally re-derives sampled R1/R2/R3 cells
mechanically):

1. **R3, the Spec 054 teeth case** —
   `yadav_2009_arxiv_manual_002` × study `054` = `opposes`.
   The stored record carries both appends:
   `spec054_outcome_append_2026_10_24` (outcome
   `STRICT CORPUS NOT PINNABLE`) and
   `spec054_outcome_append_2026_10_25` (outcome
   `NOT SUPPORTED`, the re-execution). The cell cites the
   ledger entry and both appends; the 2026-10-24 block
   appears in coverage under "superseded by a later
   outcome block from the same study". The ledger entry's
   own status (`strongly_supported`, stage `explained`)
   is untouched — the study outcome is a cell, not a
   verdict change.
2. **R1** — `ancient_writing_and_modern_technologies_51831ac9_statisti_0004`
   × document `fuls2023_catalog_of_indussigns_searchins_1dbdecdb`
   = `supports`. The stored record's evidence instance
   names that `source_document_id`, and the instance id is
   carried in the ledger entry's `evidence_refs`.
3. **R2** — `026-rcph-framework-transfer/F026-C01A` ×
   `specs/026-rcph-framework-transfer/spec.md#8` =
   `supports`. The bundle source-of-record's evidence item
   for that ref stores `direction: "supports"` verbatim.
4. **R3, Spec 052** — `farmer_sproat_witzel_2004_manual_001`
   × study `052` = `opposes`. The stored record carries
   the Spec 052 append of 2026-10-24 with outcome
   `INCONSISTENT`, which the outcome table maps to
   `opposes`.

Totals the traces sit in: 1,363 cells over 840 rows (826
rows with at least one cell, 14 empty); by relation
1,356 `supports` / 7 `opposes` / 0 `constrains`; by class
1,356 document cells and 7 study cells; research-check,
anchor, and corpus-text cells are zero for the registered
reasons above. Falsifier coverage: 831 of 840 claims
(bundle 817/817, extracted 14/23). Unresolved sign
mentions: 14 free-text mentions over 6 records, listed in
coverage.

## Claim assessments (Stage 2 scope)

- **C086-7 (the matrix is generated, never made)** —
  established for the matrix. Delete-and-regenerate over
  the unchanged ledger reproduces both artifacts
  byte-for-byte (proof above); the committed artifacts
  equal a fresh pure build under test. The claim's map
  leg belongs to Stage 5.
- **C086-8 (every cell traceable to its derivation)** —
  established structurally. Every one of the 1,363 cells
  carries a relation, a registered rule id, and non-empty
  citations whose first element is the cell's ledger row;
  sampled cells re-derive from the stored records they
  cite (tests + the four hand traces above). This does
  not establish the underlying relations are true — only
  that each is exhibited by the record it cites.
- **C086-9 (citations carry their relations)** — the
  production side holds by construction: a cell's
  citations are exactly its derivation's tie (T1 source
  membership for R1/R2, T2 dated test with matching
  outcome direction for R3, T3 registered anchor for R4),
  and the claim's named miscarriage — citing Spec 054's
  unexecuted closure as support for the Yadav claim —
  cannot be minted: the Yadav × 054 cell is `opposes`,
  citing the executed re-execution. The falsifier's
  gate-side leg (a seeded miscarriage the gate passes)
  belongs to Stage 3's V4 check class.
- **C086-1 (the ledger is the sole entry point)** — the
  matrix leg holds: every cell traces to a ledger entry
  id, and the generator's only inputs are the ledger, the
  source records the entries mirror (hash-verified), the
  annotation sidecars the entries name, and the two
  reference registers DEFINITIONS.md names. The map leg
  belongs to Stage 5.
- **C086-18 (as-of stamps)** — the matrix leg holds with
  one deliberate reading, flagged for the owner: the
  stamp carries the ledger content hash and both version
  stamps as the claim requires, and its date element is
  the ledger's latest entry date rather than a wall-clock
  generation time, because a wall clock would falsify
  C086-7 on every regeneration. Stale-marking on
  downstream surfaces is Stage 3/5 scope.

## Measurement-kind disposition (adoption 3, item 1)

Measured evidence does arise in Stage 2's registers —
the co-occurrence block is values with provenance — so
the kind was implemented, additively: `ledger-schema.json`
gains `measurement` in the `kind` enum with a required-
fields branch (`subject`, `statistic`, `value`, `unit`,
`direction`, `condition_class`, and `artifact` as
`{path, sha256}`), and the validator verifies a
measurement entry's artifact hash against the file on
disk. **No measurement entries were minted**: the
generator never writes the ledger (Point 6's one-way
flow), minting is an intake act, and no pre-existing
measured source exists in Stage 2's migration scope.
The measured values themselves are carried in the matrix
artifact with full pipeline provenance instead.

Versioning: the schema pins no rule for adding an entry
kind; the ambiguity is recorded in SCHEMA.md's amendment
section. The conservative reading was taken — `$id` stays
`ledger-schema v1`, because the addition alters no
existing kind's shape (the Stage 1 assessment's own
framing of MPCodec finding 1); a shape-altering change
would require a new version. The 871 existing entries are
untouched and the ledger still validates.

## Verification

- Spec 086 family on the clean tree
  (`test_spec086_matrix.py`, `test_spec086_ledger_intake.py`,
  `test_spec086_ledger_migration.py`): **41 passed** (20 of
  them this stage's new matrix tests).
- Spec 029 family plus
  `test_policy_sync_conformance.py`: **255 passed,
  1 skipped**.
- Freeze family (`-k freeze`): **263 passed, 1 skipped**.
- Full backend suite: 2,232 tests collected (the two GPU
  files ignored, as CI ignores them). Two whole-suite
  attempts aborted on pytest INTERNALERRORs from the
  substrate (incident 2 below), so the enumeration was
  completed in eight sequential chunks over the same file
  list: **2,198 passed, 21 skipped, 14 failed**. The 14:
  - 12 were this stage's real-tree matrix tests, failing
    in the chunk sequence because
    `tests/test_indus_evidence_api.py` (pre-existing, on
    main; it runs in an earlier chunk) rewrites the
    extracted-claims source files in-tree, after which the
    generator refuses to build over records that no longer
    match the ledger — the refusal working as designed,
    surfaced as a test failure only because the tests
    assumed a pristine tree. Disposition, in the test
    module: when that precondition is destroyed the
    real-tree tests skip with the cause named (the
    assertions are unchanged wherever the precondition
    holds), and a fixture-tree test exercises the builder
    end to end in every run. Verified both ways:
    standalone, 20 passed; in one process after the
    evidence-API test, 12 skipped and 0 failed.
  - `test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`
    — the pre-established environmental failure from
    Stage 1: the external download it needs
    (`research_notes/indus-data-deep-sweep-20261008/.../inscriptions.csv`)
    is absent on this VM. Named as such, not fixed.
  - `test_auth_consumers.py::test_auth_proof_kit_end_to_end`
    — "the test backend did not answer health within
    30 s", a load timeout on this session's substrate.
    It passes in ~6 s on pristine main (`bf7e4f83`) and
    on this branch alike in quiet windows (5.77 s and
    6.23 s when re-run standalone for this record).
- After every run, the files the suite regenerates
  in-tree were restored to HEAD, and the matrix was
  re-verified against the restored tree
  (`generate_matrix.py --check`: `CHECK: MATCH`).

Disclosed incidents from this session, per the standing
rules: (1) the first write of `matrix_generate.py` was
truncated at 15,830 bytes by the intermittent write-denial
wave; the module was rewritten in verified chunks and
compiles at 34,778 bytes. (2) Two whole-suite runs aborted
on pytest INTERNALERRORs whose tracebacks cite module
versions not present in this tree (a 274-line
`indus_corpus_v2` with an extraction import; the tree's
file is 263 lines and hash-verified against HEAD) — a
substrate fault, not a suite result; the enumeration above
was completed in eight sequential chunks instead.
(3) The test suite regenerates timestamps in the
extracted-claims source files when it runs; those files
were restored to HEAD afterward, and the matrix was
re-verified against the restored tree (`--check`: MATCH).

## What this stage does not establish

From tasks.md, verbatim:

- T201: *This does not establish the definitions are the
  right semantics — it establishes they are written down,
  versioned, and the only ones the generator may use.*
- T202: *This does not establish that the underlying
  relations are true — only that the matrix is the
  ledger, in matrix form.*
- T203: *This does not establish the matrix is verified —
  Stage 3 exists because generation alone proves nothing
  about itself.*

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
