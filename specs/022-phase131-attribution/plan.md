# Plan — Spec 022 / Phase-131 Source-of-Disagreement Attribution

Owner-authorized 2026-10-09 (STEP 1 of the Glossa-Lab
program): spec, implementation, run, PR, and
merge-when-green in one authorization. The product is
a mechanism attribution of Phase-125's observed
disagreement — never a re-scoring: the Phase-125
verdict (FAIL — DISAGREEMENT) is FINAL, spec 020's NO
stands, and both are stated unchanged in the first
lines of the Phase-131 report.

## Approach

1. **Freeze first.** Spec 022 is committed alone
   before any attribution statistic exists. The only
   numbers in it are Phase-125/127 facts of record and
   Appendix A join-feasibility counts (join stages and
   eligibility — no alignment classification, no
   matched profile, no Arm B/C/D statistic).
2. **The join is the honest part.** Spec 019 §2.1 /
   spec 015 §1 already established that Holdat has no
   CISI object ID: Arm A reports every join stage with
   counts (S1 apparent namesakes rejected as
   non-identity, S2/S3 zero as found) and establishes
   identity only by content in shared M-space — the
   Phase-116 matcher route, with a frozen similarity
   threshold, mutual-best rule, and orientation-
   ambiguity exclusion. A small matched set is a
   finding (spec A6), not a defect.
3. **Fixed set, same machinery.** Arms B and C operate
   on exactly the 16 Phase-125 PRIMARY judgeable pairs
   and reuse `phase113_battery` / `phase125_cross_compilation`
   / `phase127_diagnostic` profile/TV machinery
   unchanged. New code is only: the matcher, the
   alignment/classifier, reversal contexts, stratum
   evaluation, the length-reweighting estimator, and
   the synthesis shares.
4. **Every arm carries its falsifier.** Arm B's
   support criterion is frozen against the Phase-127
   matched-size noise band's upper bound (0.131316)
   before any reversed statistic exists. Arm A's
   estimability gates (`MIN_MATCHED` 10) and Arm C's
   (`MIN_STRATUM_PAIRS` 4) are frozen likewise; cells
   that fail them are reported NOT ESTIMABLE with
   counts, never estimated silently.
5. **Synthesis without force.** Arm D credits each
   mechanism only by its own arm's registered
   estimator, marks unestimable rows NOT ESTIMABLE,
   states the residual unexplained share plainly, and
   never rescales shares to sum to 100% — overlaps
   between the median-TV-scale arms are stated, not
   resolved.
6. **Determinism.** No stochastic procedure exists in
   this phase; the alignment tie-break (diagonal >
   deletion > insertion) is frozen so two runs are
   byte-identical in statistics.
7. **H23 order.** Script → graph module → registration
   → assertion in `ATOMIC_NODES` → only then the run.

## Verification

- Unit tests (`backend/tests/test_phase131_attribution.py`)
  per spec §8.5: toy hand-computed controls for the
  matcher tiers, every alignment class, both
  estimability gates, Arm B reversal behaviour, Arm C
  strata/reweighting, and the synthesis rules;
  determinism; real-input pins (16 judgeable pairs;
  observed median TV 0.636931; noise band
  [0.046665, 0.131316]).
- Run reproduces the frozen input totals through its
  own code path and asserts the anchors hash before
  and after; a mismatch is a build defect, not a new
  measurement.
- Full backend suite + foundation check (H21) + ruff.
- Ledgers in both files (H1), AI disclosure; one PR;
  merge only when complete and all 7 CI checks green.
