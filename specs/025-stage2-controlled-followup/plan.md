# Spec 025 — Plan

> ## FROZEN — OWNER-ADJUDICATED 2026-10-10 (spec.md §11)
>
> Adjudication is recorded in spec.md §11 (all six asks
> answered with the recommended answers). Phase-139 executes
> under this freeze; Phase-140 is gated on the Phase-139
> freeze record (step 5 below); Phase-141 proceeds per
> spec.md §5 under the same freeze record.

## Phase-139 — Covariate audit + harmonization (no outcome data)

1. Recompute the spec §3 covariate tables from the layer file as
   acquired (hash-asserted); confirm or correct every fill rate
   in the execution environment.
2. Build the covariate-eligibility audit against the §4.2 gate:
   per covariate — recorded coverage on the F3 population, per-
   site recorded counts, permutable-N projections under each
   candidate strata crossing (margins only).
3. If §11 Q2(a): construct `chron_band` mapping table from
   published site stratigraphies — per-cell citations, versioned
   artifact, Class C grading recorded. Construct `depth_band`
   per §4.2 step 2 if Q3(a).
4. Deliverable: Phase-139 audit report ending in a freeze
   recommendation — which covariates the freeze names, under
   which fallback (§4.3) — or a NOT ESTIMABLE record for G1.
5. **Freeze gate:** a freeze record naming the final strata,
   seed, thresholds, and fallback is committed and merged
   before any Phase-140 code runs.

## Phase-140 — G1 controlled F3 re-test

1. Graph module + node registered and verified (H15/H23);
   unit tests for strata construction, permutation-within-
   strata, and the statistic against the Phase-137 pure helpers
   (the uncontrolled configuration must reproduce the Phase-137
   observed statistic on the same population — a built-in
   regression check on comparability).
2. Anchors + layer hash asserted; run B = 9,999 permutations
   under the frozen strata.
3. Deliverables: results JSON (flow, strata table, permutable N,
   observed vs null distribution, V, per-site TV distances,
   covariate coverage statement), phase report under the
   mandatory lineage headline.

## Phase-141 — F1 leave-one-site-out sensitivity

1. Reuse the Phase-136 machinery and frozen definitions
   unchanged; add only the stratum-drop parameter, with unit
   tests (the no-drop configuration must reproduce the
   Phase-136 result exactly).
2. Run L-MD, L-HA, L-KA; apply the Phase-136 §5 estimability
   rule per subset.
3. Deliverables: results JSON + phase report stating the §5
   robustness-criterion outcome and naming any load-bearing
   site.

## Combined close-out

1. BH correction across the executing family members (§6, per
   §11 Q4) applied once; combined Spec 025 report assigning
   G1's verdict word and the F1 stability statement.
2. Foundation check 0 failures; anchors re-asserted.
3. Publication per §11 Q6 (release gate if publishing).
4. Program ledgers updated; Spec 024 records are not edited —
   Spec 025 results cite and sit alongside them.
