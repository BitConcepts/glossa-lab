# WP1 — Dependency map (human-readable companion)

The machine-readable inventory is `dependency-map.json` in this same
folder (18 records, 17 claims, 50 edges). This document explains the
four required traces in plain language. Hashes are SHA-256, computed
2026-10-26 over the byte-verified staged copies. Code revision for
every chain: repo HEAD `d80dcb7c` (main); the defect-site files are
unchanged since the audited snapshot `cc9ffeb4…` — the 11-commit,
50-file compare touches none of them.

**A note that applies to every chain:** assignment coverage is not
accuracy. The coverage figures count corpus tokens whose sign carries
a candidate reading. They say nothing about whether any reading is
correct, and nothing in this map upgrades them.

## The four traces

### Trace 1 — The 94 strict set and how it was derived

**Phase-48 promotions → Phase-108 provenance → retained tiers → 94 subset**

1. **Phase-48 promotions** (`C-PHASE48-PROMOTIONS`).
   `outputs/phase48_medium_validation.json` records 30 candidates
   tested and 30 promoted. Its three tests each contain a
   pass-by-default path — a too-short reading passes the dictionary
   test; a reading whose character is missing from the language model
   passes the bigram test; a sign with no checkable neighbors passes
   too; a role with no expectation passes the positional test. The
   positional test never uses the proposed reading's sound, and the
   dictionary test checks that a word exists, not that the sign maps
   to it.
2. **Phase-108 provenance** (`C-PROV108-CLASSIFICATION`). Spec 006's
   pre-registered taxonomy classified all 287 anchors from in-repo
   trails: GRAMMAR 163, DEDR 33, SA_DERIVED 24, SA_CONFIRMED_ONLY 20,
   LITERATURE 17, MIXED 15, ICONOGRAPHIC 12, CROSSWALK_CORPUS 3,
   FORMULA 0, UNTRACEABLE 0. Spec 006 itself states the limit:
   "SA-independent" means the recorded chain never passed through the
   SA lineage — it does not mean validated.
3. **Retained tiers** (`C-RETAINED-TIERS`). Phase-109 re-reviewed the
   116-anchor staging cohort (change register:
   `reports/phase109_change_register.json`); 44 anchors (43 HIGH +
   1 MEDIUM) carry the flag `pending_non_sa_validation` and are
   excluded from the strict set.
4. **The 94 subset** (`C-94SET`, `C-COVERAGE-94`, `C-COVERAGE-FULL`).
   `reports/phase109_rebase.json` recomputes headline quantities on
   the post-review table: strict set 94 signs (90 HIGH + 4 MEDIUM),
   token coverage 73.68% (5,159/7,002); full H+M set 171 readings,
   coverage 92.19% (6,455/7,002). Both coverage figures are assignment
   coverage (see the note above).

### Trace 2 — Headline metrics through the defective routines

**Phase-58 and Phase-69 → `provenance_audit.py` → Phase-109 rebase → headline metrics**

`backend/glossa_lab/pipelines/provenance_audit.py` is the shared
library. Its `phonotactic_check` imports Phase-58's machinery;
its `site_invariance` imports Phase-69's; the Phase-109 rebase script
imports the library and publishes the results as the headline
quantities in `reports/phase109_rebase.json`, which the README then
displays.

- **Phonotactics** (`C-PHONO-0`). Phase-58's checker deletes the
  prohibited initial characters from each reading before testing,
  returns "valid" for input it cannot check, and tests only the
  first reading segment in initial position. Results: 0 violations
  on every set it has ever been run on (strict 94, full H+M 171,
  and the pre-review sets in the Phase-108 recomputation) — the
  output the defective construction guarantees.
- **Site invariance** (`C-SITEINV-6565`). Phase-69's chi-square
  routine returns preset p-values (0.0 / 1.0 by statistic size, 0.5
  on any exception) instead of computing them. The rebase records
  strict 65 tested / 65 invariant / 29 insufficient data, and full
  H+M 90 / 90 / 81. The README displays only the tested denominators,
  and only as "invariance" — two separate problems: the p-values are
  not computed, and no-difference-detected would not establish
  equivalence even with correct p-values.

### Trace 3 — The crosswalk and the decisions resting on it

**Phase-96 crosswalk construction → Parpola agreement → KEEP/RESTORE decisions**

1. **Construction** (`crosswalk_v2` record). Phase-96 built entries
   of `backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json`
   (v2.1, 184 entries) by copying each anchor's own reading into the
   entry's `reading` field. The file's own statistics record 67
   entries as identity-inference-only and 113 as attested by an
   independent in-repo source — attestation of a sign pairing, which
   is not the same as an independently sourced reading.
2. **Agreement** (`C-PARPOLA-81`). `provenance_audit.parpola_agreement`
   compares each anchor reading against that same `reading` field
   (normalized first-segment equality, the Spec 006 registered
   method). On the strict set: 81 compared, 81 agree. The rebase
   artifact itself carries the caveat that the rate is "partially
   tautological"; on the Phase-96-built entries it is a comparison
   of the project with itself.
3. **Decisions** (`C-KEEP-RESTORE-109`). Phase-109's cohort review
   restored 112 prior sourced readings, demoted 3, and kept 1 on
   Parpola crosswalk support. That one decision's crosswalk leg is
   flagged `requires_revalidation` in the overlay; the decision is
   not reversed by this repair, and its other evidence was not
   re-examined here.

### Trace 4 — Displayed summaries back to the release artifacts

**README and UI metrics → paper source, PDF, version manifest, deposited record**

- The README is the only display surface among the staged files. Its
  banner (line 14), metrics table, and status section carry the
  summaries inventoried per claim in the JSON map.
- The paper source is named in the staged `AGENTS.md`:
  `glossa-corpus/indus/pierson_2026_indus_decipherment.tex`, with the
  v8 PDF `pierson_2026_indus_decipherment_preprint_v8.pdf` (that file
  records the v8 PDF's SHA-256 as `6d5b1e7f…`). Neither the source
  nor any PDF was among the staged files for this task.
- The deposit of record moved post-snapshot: v9, Zenodo record
  23668053, version DOI 10.5281/zenodo.23668053, concept DOI
  10.5281/zenodo.20379070 (goal-side v9 deposit record, 2026-10-26).
  That record documents the deposited PDF
  (`pierson_2026_indus_decipherment_preprint_v9.pdf`, 206,529 bytes,
  SHA-256 `d3cea9c3…`). **The deposited PDF was not fetched in this
  task and was not compared against that documented hash; the
  comparison is UNVERIFIED here.**
- The website tracker was already promoted to v9 by the deposit
  work (per the same record); the README is the surface that lagged.
  UI metric widgets beyond the README were not staged and are
  recorded in the map as not staged — not as verified.

## Records and hashes

| Record | Repo path | SHA-256 (staged copy) | Run environment as recorded |
|---|---|---|---|
| Anchor table | `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | — (data artifact) |
| Phase-48 validation output | `outputs/phase48_medium_validation.json` | `96540ece728513886fbbe957d68e9eb25b10a824c1960e0cb9f25c5eabddad14` | `gpu_device: cuda` |
| Phase-108 anchor trails | `reports/phase108_anchor_trails.json` | `c49334003e8c83dcab1a5707de278510f0dae35d729888c35c891f2ed7b5532a` | cpu (torch absent) |
| Phase-108 provenance register | `reports/phase108_provenance_register.json` | `2b04fed49d50a2958776c80e74a64fffd024b827c7da182077a405ace23f6a25` | cpu (torch absent) |
| Phase-108 subset recomputation | `reports/phase108_subset_recomputation.json` | `c10a276104b23afc7127f8a20021d09a18ffb23ed15c78f4cc76e95c3b723f0f` | cpu (torch absent) |
| Phase-108 impact map | `reports/phase108_impact_map.json` | `0bc9d9e5beeffa740382c09633819d202354c527649f004822c6657148059076` | cpu (torch absent) |
| Phase-109 rebase | `reports/phase109_rebase.json` | `b724c8708652e02c3904f4c4a4a8cc828442edc80dd11458b4c728a6e1828123` | cpu (torch absent); date 2026-10-06 |
| Phase-109 change register | `reports/phase109_change_register.json` | `beb12d6539770be844cb3e9a88f23fa9c268a625bf6c17e49381b7911527f7fd` | not recorded beyond phase/spec/date (unknown) |
| Crosswalk v2.1 | `backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json` | `3c54ed09b869a5046eb7e25d9e77accf25e552f17aadef95a4757a668739a7cb` | construction environment not recorded (unknown) |
| CISI corpus data | `data/indus_cisi_corpus.json` | `f9633c7045ad0a74fc0dff66164e24117b3f9de1850e0257d16f1b8505e314c1` | — (data artifact) |
| Spec 006 | `specs/006-anchor-provenance-audit/spec.md` | `2bdf4bbf63216fc47f481016881ec8ae130c7429fc605e44c36c7210c2232898` | — (specification) |
| README (staged, HEAD) | `README.md` | `9685b256d43efa7260f4a052839c10bfb45e8561a0bdd9baeece89611f688825` | — (display surface) |

Code inspection copies (hashed from `~/workspace/glossa-run/repair-2026-10-26/inspect/`):
Phase-58 `5df152d3…`, Phase-69 `95d4e462…`, Phase-96 `af4c90a6…`,
Phase-48 `e7fa7c17…`, `provenance_audit.py` `2fcc5ceb…`,
Phase-109 rebase script `b6fbf468…`, Phase-109 follow-through
`571ef648…`. Full hashes are in `dependency-map.json`.

## Claims in the map

C-PHASE48-PROMOTIONS · C-PROV108-CLASSIFICATION · C-RETAINED-TIERS ·
C-94SET · C-COVERAGE-94 · C-COVERAGE-FULL · C-PHONO-0 ·
C-SITEINV-6565 · C-PARPOLA-81 · C-KEEP-RESTORE-109 ·
C-FISH-ISOLATION · C-GRAMMAR-Z · C-SEAL-COVERAGE-RETIRED ·
C-GRAMMAR-ACCURACY-RETIRED · C-NAIR-REPLICATION · C-RELEASE-CHAIN ·
C-PROGRESS-PCT.

Each JSON claim entry carries its evidence records, source passages
(trail and code citations), artifacts, input hashes, code revisions,
run environment, and displayed summaries. Two claims are deliberately
carried as *preserved descriptive results* (C-GRAMMAR-Z: the
positional-grammar statistic and the M267 reclassification) — no
staged dependency routes them through the WP2–WP4 defect sites, and
WP1 item 6 preserves unrelated results unless their own dependencies
are affected.
