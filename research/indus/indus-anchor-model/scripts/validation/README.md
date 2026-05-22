# Validation Scripts

One-button reproducibility checks for the publicly released data
accompanying Pierson (2026).

## Quick start

```bash
# From this directory:
python run_all_public_checks.py

# Or with explicit paths:
python run_all_public_checks.py \
    --data-dir ../../data/public/ \
    --output-dir ../../outputs/
```

**Requirements:** Python 3.10+ (stdlib only — no third-party packages needed).

## What it does

`run_all_public_checks.py` executes five checks against the publicly
released CSVs.  No Holdat LLC corpus, ICIT crosswalk, or restricted data is
required.

| # | Check | What it verifies |
|---|-------|-----------------|
| 1 | `anchor_table_integrity` | 397 signs present, 161 at HIGH+MEDIUM confidence, unique IDs |
| 2 | `fish_sign_compound_only` | All fish-sign occurrences are compound (zero isolated) |
| 3 | `formula_bigram_backbone` | M342·M176 is the top bigram by raw count |
| 4 | `positional_profile_sanity` | M267 is >70 % non-initial; M342 is in the terminal cluster |
| 5 | `coverage_arithmetic` | H+M anchor count = 161; token coverage consistent with 88–93 % |

## Expected output

### Console

```
  [✓] anchor_table_integrity: PASS — 397 signs total, 161 HIGH+MEDIUM …
  [✓] fish_sign_compound_only: PASS — All 27 fish-sign occurrences are compound …
  [✓] formula_bigram_backbone: PASS — Top bigram is M342·M176 (count=122) …
  [✓] positional_profile_sanity: PASS — M267 confirmed non-initial …
  [✓] coverage_arithmetic: PASS — Top-30 H+M bigram tokens: …

RESULT: OK — all checks passed or skipped.
```

### Files

- `outputs/logs/public_validation_report.txt` — human-readable report
- `outputs/tables/public_validation_summary.csv` — machine-readable summary

The CSV has columns: `check_name`, `status`, `reproducibility_tag`, `detail`.

## Reproducibility tags

Each check is tagged with one of:

- **REPRODUCED_FROM_PUBLIC_DATA** — check passed using only released files
- **NOT_REPRODUCIBLE_FROM_RELEASED_DATA** — check failed
- **REQUIRES_RESTRICTED_CORPUS** — check skipped (data file not found)

## Exit codes

- `0` — all checks PASS or SKIP
- `1` — one or more checks FAIL
- `2` — fatal error (bad arguments, missing Python, etc.)

## Data directory layout

The `--data-dir` should contain (or have in a `supplemental/` subdirectory):

```
data/public/
├── anchor_table.csv
├── supplemental/
│   ├── fish_sign_compound_context.csv
│   ├── formula_bigram_table.csv
│   └── README.md
```

## Claim tiers

These checks span the model's three claim tiers:

- **Tier 1 (structural):** Checks 1, 3, 5 — sign inventory, bigram backbone, coverage
- **Tier 2 (candidate anchors):** Checks 2, 4 — fish-sign constraint, positional profiles
- **Tier 3 (speculative):** Not tested here — requires corpus-level reproduction
