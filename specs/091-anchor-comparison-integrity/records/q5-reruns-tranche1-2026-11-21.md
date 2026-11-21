# Spec 091 — Q5 item 3 dependency-aware reruns, Tranche 1: the two fallen premises (M342, M176)

**Date:** 2026-11-21 · **Spec:** 091-anchor-comparison-integrity · **Workstream:** Co-scientist audit Q5 item 3 (dependency-aware reruns), Round 2 tranche 1 · **Venue:** tower-compute (fresh clone `~/glossa-work/r2-reruns-bbdd9d30`) · **Runner:** `backend/scripts/spec091_q5_reruns.py` · **Machine record:** `records/q5-reruns-2026-11-21.json`

## Scope

M342 (ay/ā) and M176 (an/aṇ) are the two fallen premises: both stand at class **U** (insufficient evidence) after the corrected T303 site-statistics arm, yet downstream readings' filed arguments cite them as 'HIGH' anchors. This tranche reruns their own corrected results before any downstream deletion is recorded: reconstruct the occurrence denominator and terminal count from the corpus records in the repo, under the filed position/orientation definitions and seal deduplication, and reproduce the filed test.

**Definitions of record (from the T303 runner, `backend/scripts/spec091_stage3_site_stats.py`):** seals grouped by `cisi_number` (the deduplication key); a seal's site taken from its first row; position binning: position 0 of a multi-sign inscription is initial, the last position is terminal, everything else, including a single-sign inscription, is medial; a site's row enters the test table iff the sign's total at that site is at least 3. **Checker:** the repo's corrected `glossa_lab.site_stats_v2.chi_square_independence` (Pearson chi-square, no Yates correction; module site-stats-v2.0.0), the same checker that produced the filed result.

**Input limitation, stated on the record:** the raw Holdat corpus CSV (`corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`, SHA-256 `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e` as pinned by the T303 run) is gitignored working data and is **not held in this clone**; a from-raw recount was therefore not executable in this round. The reconstruction below is from the corpus-derived record the repo does hold: the full site-by-position tables filed in `records/t303-reclassification-acts.json` (run `study-20261118T151605Z-4c5c8b`), whose `all_site_counts` carry every site's counts, including sites excluded from the test table. No substitute data was used.

## Results

| Sign | Corpus n (reconstructed) | Terminal count | Terminal rate | Filed rate | Recomputed χ² | Filed χ² | df | Recomputed p | Filed p | Reproduces |
|---|---|---|---|---|---|---|---|---|---|---|
| M342 (ay/ā) | 584 | 70 | 70/584 = 12.0% | 12.0% | 25.2468 | 25.2468 | 16 | 0.0656 | 0.0656 | **YES** |
| M176 (an/aṇ) | 356 | 68 | 68/356 = 19.1% | 19.1% | 22.8589 | 22.8589 | 14 | 0.0626 | 0.0626 | **YES** |

Notes:

- M342: the test table's grand total is itself 584 (all 9 sites meet the inclusion threshold; no excluded sites), and the terminal column sums to 70 exactly.
- M176: the test table's grand total is 354, not 356. The difference is Rakhigarhi (0 initial, 2 medial, 0 terminal), excluded from the table under the at-least-3 rule and carried in `all_site_counts`; adding it back reconstructs the filed corpus n of 356. The terminal count is 68 either way.
- Both outcomes remain **difference not detected** (p ≥ 0.05). Under the corrected doctrine recorded at T303, a non-significant difference test is not evidence of site-invariance and re-earns no support: the rerun confirms the filed corrected result, and both signs remain class **U**. The sparse-table warning filed at T303 (smallest expected counts 0.33 and 0.25) applies to the recomputed values identically, because the tables are identical.

## Payload verdicts

- Runner exit code: **0** (overall; see the machine record).
- `PAYLOAD VERDICT T1 M342: chi2=25.2468 df=16 p=0.0656 n=584 terminal=70 rate=0.1199 reproduces=True`
- `PAYLOAD VERDICT T1 M176: chi2=22.8589 df=14 p=0.0626 n=356 terminal=68 rate=0.1910 reproduces=True`

## What this record does not do

It changes no standing, no ledger entry, and no register value. It reports a test outcome only: the filed corrected results for the two fallen premises reproduce from the filed corpus tables, so the downstream deletions in tranches 2 and 3 proceed on verified premises.
