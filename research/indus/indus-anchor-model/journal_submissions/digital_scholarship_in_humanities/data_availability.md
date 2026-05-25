# Data Availability Statement
## For Digital Scholarship in the Humanities submission

---

## Publicly available data and code

All analysis scripts, public data tables, and documentation are available in the GitHub repository:

**https://github.com/BitConcepts/glossa-lab**

Specifically at: `research/indus/indus-anchor-model/`

The following files are released under CC BY 4.0 (data tables) and MIT License (code):

| File | Description |
|---|---|
| `data/public/anchor_table_397.csv` | All 397 Mahadevan M-number signs with candidate readings and confidence tiers |
| `data/public/fish_sign_contexts.csv` | Per-seal compound-context listing for M047 and M001 |
| `data/public/formula_bigrams.csv` | Top-30 directed H+M×H+M bigrams with counts and PMI |
| `data/public/iconographic_formula_pairs.csv` | 63 enriched INITIAL-sign × seal-icon chi-square pairs |
| `data/public/polysemy_divergence_summary.csv` | Phase-150 permutation null test results (21 signs, 1,000 shuffles) |
| `scripts/validation/run_all_public_checks.py` | One-button public reproducibility checker (stdlib only) |
| `scripts/network_analysis/run_betweenness.py` | Betweenness centrality analysis |
| `scripts/fish_sign_test/run_fish_sign_test.py` | Fish-sign isolation test |

A Zenodo archive with a permanent DOI will be created before final publication.

---

## Restricted data

The **Holdat LLC Indus Corpus v3** (Miller 2025) is the primary corpus used in this study. It is not redistributed in this repository due to licensing. The following corpus-level statistics from the preprint were derived from this corpus and cannot be reproduced without authorized access:

- Token coverage percentages (90.96% H+M, 9.34% LOW)
- Per-sign positional rates (I/M/T fractions)
- Permutation null test (z = 10.3, 0/2000)
- Bootstrap confidence intervals for site-level KL divergences

Scripts are provided so that all analyses can be rerun by researchers with authorized access to Holdat or by using a compatible public corpus (e.g. ICIT) after sign-code crosswalking. The `data/restricted/README_restricted_data.md` file specifies exactly which outputs require restricted access.

---

## Public verification

Structural claims not dependent on the restricted corpus can be independently verified using only the public tables above. Run:

```bash
python scripts/validation/run_all_public_checks.py
```

This produces a pass/fail report for five reproducibility checks using only files in `data/public/`. Expected result: 5/5 PASS.

---

## ICIT cross-corpus validation

The ICIT corpus (~5,318 inscriptions, Fuls 2014) is identified as the target for independent cross-corpus validation. A full validation plan is provided in `docs/icit_validation_plan.md`. No ICIT data are included in this repository; the validation plan specifies the required Mahadevan-to-ICIT crosswalk and the eight tests to be rerun.
