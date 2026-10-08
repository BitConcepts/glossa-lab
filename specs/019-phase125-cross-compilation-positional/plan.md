# Plan — Spec 019 / Phase-125 Cross-Compilation Positional Comparison

Owner-authorized 2026-10-08 (STEP 1 of the Glossa-Lab
program): spec, implementation, run, PR, and merge-when-green
in one authorization. The product is one verdict, reported
as found: do the mayig/CISI and Holdat compilations tell the
same positional story about crosswalk-joined signs, when
each story is computed strictly inside its own compilation?

## Approach

1. **Register first.** Spec 019 is committed alone before
   any comparison statistic exists. The only pre-freeze
   numbers are Appendix A counts (attestation, pair counts,
   judgeability, and the §2.1 contiguity verification) —
   the program's established pre-freeze measurement
   precedent. No profile is compared in Appendix A.
2. **Reuse, don't reinvent.** Positional counts, profiles,
   TV, and modal class come from `phase113_battery`
   unchanged; the mayig layer and crosswalk come through
   their Phase-122 loaders unchanged; the Holdat side uses
   the specs-015/017 loader replication unchanged. New
   code is only: arm construction, Spearman, W1, the
   pairing-shuffle null, the verdict rule, orchestration.
3. **The guards are code, not vigilance.** Within-
   compilation-only computation (no pooled corpus object
   exists in the module), crosswalk-only joining,
   confidence/uniqueness gating per arm, the floor as a
   counted exclusion, and the §2.1 prohibition on the
   padded-number object join are each pinned by a unit
   test.
4. **The null is part of the verdict.** PASS requires
   beating the pairing-shuffle null (B = 999, seed
   125125) as well as the distance and correlation
   gates — a PASS that a random re-pairing could
   produce is not a PASS (blind-affiliation lesson).
5. **H23 order.** Script → graph module → registration →
   assertion in `ATOMIC_NODES` → only then the run.
6. **Verdict as found.** PASS / FAIL / NULL-STARVED /
   NULL-INCONCLUSIVE are all legitimate. No anchor is
   touched; the anchors hash is asserted before and
   after; sensitivity arms are reported separately and
   never pooled into the primary verdict.

## Verification

- Unit tests (`backend/tests/test_phase125_cross_compilation.py`)
  per spec §8.5, including toy end-to-end controls for
  PASS, FAIL, and NULL-STARVED through the real §6 rule.
- Run reproduces Appendix A arm/judgeability counts
  (286 primary pairs, 16 judgeable at floor 8; arm B
  762 / 28) through its own code path; a mismatch is a
  build defect, not a new measurement.
- Full backend suite + foundation check (H21) + ruff.
- Ledgers in both files (H1), AI disclosure; one PR;
  merge only when complete and CI green.
