# Rerun Contract — Phase-384 (C1 margin completion: Phase-137 F2/F3)

**Correction type:** C1 — the F2/F3 verdicts rested on
permutation p-values with point Cramer's V only; no interval and
no practical margin were adjudicated. **Register rows:**
PHASE-137 (SPEC-024 in part). **Frozen:** at the S3 merge.
Freeze record: `phase384-freeze.json`.

## Inputs

- `reports/phase137_results.json` — contains the full recorded
  profile tables (site x sign-column counts) for F2 (Holdat) and
  F3 (ICIT-lineage). No layer rebuild: the tables ARE the
  recorded computation's sufficient statistics.

## Computation (exactly this)

1. Verify: recompute chi-square and Cramer's V from each
   recorded table; assert equality with the recorded values
   (F2 chi2 745.9530278664314, V 0.11539837515155221; F3 chi2
   4966.362228365138, V 0.2190) within 1e-6 relative.
2. Parametric bootstrap for V: per site row, multinomial
   resample of the row total over the row's recorded column
   proportions; B = 9,999, seed 20261011; percentile 95% CI
   for V per family member.

## Margin + verdict rules (declared in advance)

- Practical margin (convention, declared here before the run):
  **V = 0.10** (small-effect floor). 
- F3 (original SUPPORTED): the support stands as SUPPORTED
  (bounded, lineage-labeled) iff the CI lower bound > 0.10;
  if the CI crosses 0.10, the framework status becomes
  INCONCLUSIVE at the declared margin (the permutation result
  is unchanged and is reported alongside).
- F2 (original NOT SUPPORTED): if the CI upper bound < 0.10,
  the bounded claim of a practically-sized site-repertoire
  differentiation on the Holdat layer is CONTRADICTED at the
  declared margin; if the CI crosses 0.10, INCONCLUSIVE.
- Uncontrolled period/preservation/excavation confounders of
  F3 remain exactly as confessed in the original record; this
  rerun changes nothing about them (Phase-140 handled
  preservation for the F3 population under Spec 025).

## Comparison reported

Recorded chi2/V/p vs table-verified chi2/V vs bootstrap CI vs
margin adjudication per member.
