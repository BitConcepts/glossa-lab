# Permutation Test Scripts

## Purpose

Permutation-based null-hypothesis tests that assess whether the observed
structural patterns (positional constraints, bigram frequencies, polysemy
profiles) could have arisen by chance.

These tests support the Tier 1 structural claim that the Indus script
encodes a grammar-governed writing system.

## Planned scripts

- `run_polysemy_permutation.py` — Within-seal position shuffles (1,000
  iterations) testing whether observed collocate divergence between
  positional slots exceeds the null expectation. Reproduces the Phase 150
  result: observed polysemy rate (66.7 %) is *below* the null mean
  (80.7 %), confirming strong positional constraints.
- `run_bigram_shuffle.py` — Row-wise permutation test on the bigram table
  to verify that the M342·M176 backbone frequency is not a corpus artefact.
- `run_iconographic_enrichment_test.py` — Bonferroni-corrected chi-square
  permutation test for INITIAL-sign × seal-iconography enrichment.

## Inputs

- **Holdat LLC Indus Corpus v3** (required) — per-seal sign sequences for
  full permutation testing.
- `polysemy_divergence_summary.csv` — summary statistics from Phase 150
  (included in `data/public/supplemental/`).
- `formula_bigram_table.csv` — top-30 bigrams (included in `data/public/`).
- `iconographic_formula_pairs.csv` — enriched pairs (included in `data/public/`).

## Outputs

- `outputs/tables/polysemy_permutation_results.csv`
- `outputs/tables/bigram_shuffle_pvalues.csv`
- `outputs/tables/iconographic_enrichment_pvalues.csv`
- `outputs/figures/polysemy_null_distribution.png` (optional)

## Reproducibility status

**REQUIRES_RESTRICTED_CORPUS** — Full permutation testing requires the
Holdat LLC corpus for per-seal sequence data. The released summary
statistics in `polysemy_divergence_summary.csv` allow verification of the
reported figures but not independent recomputation.

## Claim tier

**Tier 1 (structural)** — These are purely statistical tests on corpus
structure, independent of any specific phonetic reading assignment.
