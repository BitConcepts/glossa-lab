# Site Divergence Scripts

## Purpose

Measures inter-site variation in sign usage to test whether the Indus
script exhibits geographic dialect effects or site-specific formulaic
traditions. Computes KL divergence and bootstrap confidence intervals
between site-level sign distributions.

This analysis supports both Tier 1 (structural: script is standardised
across sites) and Tier 2 (candidate anchors: anchor readings are
consistent across regions).

## Planned scripts

- `run_site_kl_divergence.py` — Compute pairwise KL divergence between
  sign frequency distributions at major sites (Mohenjo-daro, Harappa,
  Lothal, Kalibangan, Dholavira, etc.). Output a site × site divergence
  matrix and identify signs with the largest inter-site variance.
- `run_site_bootstrap.py` — Bootstrap resampling (10,000 iterations) to
  compute confidence intervals for site-level divergence measures.
  Tests whether observed cross-site consistency exceeds what would be
  expected from a geographically fragmented system.
- `run_gulf_seal_analysis.py` — Focused analysis of Gulf (Dilmun/Failaka)
  seals vs. Indus Valley seals. Tests whether Gulf seal formulas show
  adaptation to a foreign-trade context while preserving core grammar.

## Inputs

- **Holdat LLC Indus Corpus v3** (required) — per-seal sign sequences with
  site provenance metadata.
- `anchor_table.csv` — to identify which signs are H+M anchors.
- `fish_sign_compound_context.csv` — for site-level fish-sign distribution.

## Outputs

- `outputs/tables/site_kl_matrix.csv`
- `outputs/tables/site_bootstrap_ci.csv`
- `outputs/tables/gulf_seal_comparison.csv`
- `outputs/figures/site_divergence_heatmap.png` (optional)

## Reproducibility status

**REQUIRES_RESTRICTED_CORPUS** — Site-level analysis requires the full
Holdat LLC corpus with per-seal site provenance. The released
`fish_sign_compound_context.csv` includes site information for 27 seals,
which allows a limited cross-site comparison for fish signs only.

## Claim tier

- **Tier 1 (structural)** — Cross-site consistency of positional grammar
- **Tier 2 (candidate anchors)** — Geographic robustness of anchor readings
