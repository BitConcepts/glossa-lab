# Positional Analysis Scripts

## Purpose

Computes per-sign positional profiles across the three-slot grammar model
(INITIAL, MEDIAL, TERMINAL) and validates the claim that sign positions
are non-random (Tier 1 structural claim).

## Planned scripts

- `run_positional_profiles.py` — For each sign in the anchor table, compute the
  fraction of occurrences in each positional slot. Output a CSV of
  `(sign, initial_frac, medial_frac, terminal_frac, dominant_slot, n)`.
- `run_slot_entropy.py` — Compute Shannon entropy of positional distributions
  to quantify how tightly each sign is constrained to its slot.

## Inputs

- **Holdat LLC Indus Corpus v3** (required) — per-seal sign sequences with
  positional annotations. Not included in the public release.
- `anchor_table.csv` — sign IDs and confidence tiers (included in `data/public/`).

## Outputs

- `outputs/tables/positional_profiles.csv`
- `outputs/tables/slot_entropy.csv`
- `outputs/figures/positional_heatmap.png` (optional, requires matplotlib)

## Reproducibility status

**REQUIRES_RESTRICTED_CORPUS** — Full positional profile computation requires
the Holdat LLC corpus. The released anchor table contains positional keywords
in the Basis field, but the raw per-seal data is not publicly available.

Partial validation is possible via `run_all_public_checks.py` (Check 4:
`positional_profile_sanity`), which confirms M267 non-initial and M342
terminal from the released metadata.

## Claim tier

**Tier 1 (structural)** — Positional grammar is a falsifiable structural
property of the corpus, independent of any specific phonetic reading.
