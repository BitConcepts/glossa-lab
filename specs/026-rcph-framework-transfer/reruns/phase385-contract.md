# Rerun Contract — Phase-385 (C1 margin completion: Phase-140 G1)

**Correction type:** C1 — G1 SUPPORTED under control rested on
the controlled permutation p-value (0/9,999) with point V
0.2190; no interval for the controlled effect was reported.
**Register rows:** PHASE-140 (SPEC-025 in part). **Frozen:** at
the S3 merge. Freeze record: `phase385-freeze.json`.

## Inputs

- The horus84 layer file at its pinned path (sha256
  c368f290... asserted at runtime, as Phase-140 does).
- `data/evidence_integration/phase139_harmonized_covariates.json`
  (preservation per inscription).
- `reports/phase137_results.json` F3 profile table (the sign
  columns incl. OTHER) and `reports/phase140_results.json`
  (recorded G1 quantities for verification).
- Population rebuilt with the Phase-140 module's own machinery
  (imported, not reimplemented).

## Computation (exactly this)

1. Verify: rebuilt population == 5,410 inscriptions / 7 sites /
   5,404 permutable; observed chi2 == 4966.362228365138
   (tolerance 1e-6 relative). Any mismatch stops the rerun and
   is reported as a finding.
2. Stratified bootstrap for V: resample inscriptions WITHIN
   composition x preservation strata (the frozen G1 strata,
   UNRECORDED retained as a level) with replacement; per
   replicate rebuild the site x sign-column table and compute
   Cramer's V; B = 1,999, seed 20261011; percentile 95% CI.
3. Exploratory companions (labeled EXPLORATORY everywhere):
   the same stratified bootstrap within composition x
   chron_band strata and composition x depth_band strata
   (the Phase-140 sensitivity designs), CIs only.

## Margin + verdict rules (declared in advance)

- Margin: **V = 0.10** (same declared convention as Phase-384).
- G1 (original SUPPORTED under control): stands as SUPPORTED
  (bounded; chronology NOT controlled — the rider is verbatim
  in this rerun's report) iff the stratified CI lower bound
  > 0.10; a CI crossing 0.10 makes the framework status
  INCONCLUSIVE at the declared margin. The permutation result
  is not recomputed and not altered; it is reported alongside.

## Comparison reported

Recorded G1 quantities vs verified quantities vs stratified CI
vs margin adjudication; sensitivity CIs labeled EXPLORATORY.
