# Plan — Spec 021 / Phase-127 Cross-Compilation Disagreement Diagnostic

Owner-authorized 2026-10-08 (WORKSTREAM 1 of the
Glossa-Lab program): spec, implementation, run, PR, and
merge-when-green in one authorization. The product is a
decomposition of Phase-125's observed disagreement —
never a re-scoring: the Phase-125 verdict (FAIL —
DISAGREEMENT) is FINAL and is stated unchanged in the
first lines of the Phase-127 report's abstract.

## Approach

1. **Freeze first.** Spec 021 is committed alone before
   any diagnostic statistic exists. The only numbers in
   it are Phase-125 / Phase-122 facts of record and §7
   metadata-support counts (stratum sizes from metadata
   columns; no profile is compared at design stage).
2. **Fixed set, same machinery.** All arms operate on
   exactly the 16 Phase-125 PRIMARY judgeable pairs,
   read from the Phase-125 results of record, and reuse
   `phase113_battery` / `phase125_cross_compilation`
   profile/TV machinery unchanged. New code is only:
   resampling, neighbourhood decomposition, stratified
   profile evaluation, and the power grid.
3. **Noise priced three ways, never averaged.**
   Token-level split-half (§3) and matched-size (§4)
   nulls are cheap and registered with their clustering
   limitation (A3); the inscription-level bootstrap (§5)
   is the cluster-respecting, governing uncertainty
   statement. Each is reported on its own terms.
4. **Ambiguity handled honestly.** The primary arm
   excludes ambiguity by construction (§6 states this
   as a fact, not a finding); the decomposition arm
   prices the counterfactual — the same signs under
   their ambiguous mappings — with a single
   pre-registered descriptive estimator.
5. **Composition only where metadata exists.** Site
   and iconography strata exist on both sides (§7
   support facts); controls restrict Holdat only,
   because mayig is already entirely within each
   stratum. Everything the metadata does not support
   (unicorn variants, finer provenience, length) is
   stated as a gap in the report, not improvised.
6. **H23 order.** Script → graph module → registration
   → assertion in `ATOMIC_NODES` → only then the run.
7. **Determinism.** Fixed seeds and replicate counts
   per arm (spec §2); the run is reproducible byte-for-
   byte in its statistics.

## Verification

- Unit tests (`backend/tests/test_phase127_diagnostic.py`)
  per spec §10.5: toy hand-computed controls for every
  arm, determinism under the frozen seeds, and real-input
  pins (judgeable set == Phase-125's 16; observed median
  TV of record == 0.636931).
- Run reproduces the Phase-125 inputs' frozen totals
  through its own code path and asserts the anchors hash
  before and after; a mismatch is a build defect, not a
  new measurement.
- Full backend suite + foundation check (H21) + ruff.
- Ledgers in both files (H1), AI disclosure; one PR;
  merge only when complete and CI green.
