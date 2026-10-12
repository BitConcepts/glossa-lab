# Phase-394 — Spec 030 chronology-spine extension + Q6 re-test

Extension of the Phase-391 spine under the Spec 030 freeze (OSF https://osf.io/bge3k/). The Stage 0 products are inputs, unmodified; the re-test is the stage0-freeze.md section 4 assessment verbatim, margins only (F030-C05).

## Routes (frozen order R5 -> R1 -> R2 -> R4 -> R3)

- R5: ran=True; new rows 0; citations attached 0; corrections 0.
  Interim (as frozen): c1_regions_with_2plus_sites=1 (FAIL); c2_window_sites_direct_or_associated=5 (FAIL); c3_window_short_lived_share=0.0 (FAIL); c4_window_median_std_bp=70 (PASS) — status NOT-YET-TESTABLE
- R1: ran=True; new rows 0; citations attached 10; corrections 10.
  Interim (as frozen): c1_regions_with_2plus_sites=1 (FAIL); c2_window_sites_direct_or_associated=5 (FAIL); c3_window_short_lived_share=0.0 (FAIL); c4_window_median_std_bp=70 (PASS) — status NOT-YET-TESTABLE
- R2: ran=True; new rows 49; citations attached 124; corrections 0.
  Interim (as frozen): c1_regions_with_2plus_sites=1 (FAIL); c2_window_sites_direct_or_associated=5 (FAIL); c3_window_short_lived_share=0.0 (FAIL); c4_window_median_std_bp=70 (PASS) — status NOT-YET-TESTABLE
- R4: ran=True; new rows 0; citations attached 0; corrections 0.
  Interim (as frozen): c1_regions_with_2plus_sites=1 (FAIL); c2_window_sites_direct_or_associated=5 (FAIL); c3_window_short_lived_share=0.0 (FAIL); c4_window_median_std_bp=70 (PASS) — status NOT-YET-TESTABLE
- R3: ran=True; new rows 21; citations attached 0; corrections 0.
  Interim (as frozen): c1_regions_with_2plus_sites=1 (FAIL); c2_window_sites_direct_or_associated=6 (FAIL); c3_window_short_lived_share=0.0 (FAIL); c4_window_median_std_bp=70 (PASS) — status NOT-YET-TESTABLE

## Dedupe (rule 2)

- Measurements merged: 42; rows removed: 42; age conflicts not merged: 0; site-assertion conflicts: 6.

## Q6 re-test (extended spine)

### as_frozen — status: NOT-YET-TESTABLE
- c1_regions_with_2plus_sites: value 1 vs threshold 3 — FAIL
- c2_window_sites_direct_or_associated: value 6 vs threshold 10 — FAIL
- c3_window_short_lived_share: value 0.0 vs threshold 0.5 — FAIL
- c4_window_median_std_bp: value 70 vs threshold 80 — PASS
- Window direct/associated rows: 37

### excluding_contested — status: NOT-YET-TESTABLE
- c1_regions_with_2plus_sites: value 1 vs threshold 3 — FAIL
- c2_window_sites_direct_or_associated: value 6 vs threshold 10 — FAIL
- c3_window_short_lived_share: value 0.0 vs threshold 0.5 — FAIL
- c4_window_median_std_bp: value 70 vs threshold 80 — PASS
- Window direct/associated rows: 37

Ask 2 (whether the CONTESTED sensitivity binds a future Q6 freeze) is not decided by this build; both computations are reported above (integrity rule 5). A SUPPORTED-FOR-FREEZE-DESIGN outcome binds only that a Q6 freeze may be designed under Spec 027 section 8.2.

