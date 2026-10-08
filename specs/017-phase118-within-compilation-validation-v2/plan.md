# Plan — Spec 017 / Phase-118 Within-Compilation Validation Battery v2 (W1-primary, cross-fit W3)

Successor to spec 016 (Phase-117), whose battery was rejected
at calibration. The owner's commission (2026-10-07) covers
design **and** execution in one authorization; the spec is
still frozen alone, before any Phase-118 statistic exists,
and execution follows the frozen order of spec §11.

## Approach

1. **Diagnosis before design.** Phase-117's results JSON
   localizes the rejection: W1 sound (63/94 PASS on the
   core), W3 the binding constraint (3/94 PASS) via two
   recorded defects — the leave-one-out-minus-self reference
   (φ = −7.461366) and the p ≤ 0.05 donor leg attained by
   3/81 judged core signs (median core p 0.627) — and a
   negative gate that passed vacuously (KUR113 INDETERMINATE
   on every instrument; the 24 judged kur signs met W3's
   FAIL conjunction 0 times). Every redesign decision in
   spec 017 cites one of these numbers; nothing is changed
   without a recorded basis, and nothing with a recorded
   basis is silently kept (fate table, spec Context).
2. **Feasibility before freeze.** Design-stage counts only:
   per-direction junction availability at floors 2/3/4
   (the floor choice decides whether a negative control
   exists at all: JKUR = 29 / 4 / 1), judgeable-set sizes
   (J94 = 67 at floor 2), the flagged cohort's validation
   cap (11/44), and the three by-construction UNRESOLVED
   signs re-verified under the new definitions (M235/M254/
   M402 remain judgeable by no instrument).
3. **Instruments.** W1 primary, carried verbatim (same
   partition — seed 117, totals asserted — same thresholds).
   W3 rebuilt cross-fit: model and φ from the opposite half,
   donor null retained per direction with median-donor
   bands (PASS: score ≥ φ_d ∧ p_d ≤ 0.50; FAIL its mirror),
   W1's combination rule. W4 verbatim, narrowed to
   FAIL-guard. W2 remains dropped.
4. **Gates with teeth.** Positive gate over the judgeable
   core (share of J94, with a frozen minimum |J94| ≥ 50 —
   design count 67, asserted at run time). Negative gate
   over JKUR requiring zero validations **and** an actively
   failed share ≥ 0.25 — universal indeterminacy now
   *fails* the gate by construction, repairing spec 016's
   recorded defect.
5. **Decision structure.** W1-primary conjunction (W1 PASS
   ∧ rebuilt-W3 PASS ∧ no FAIL), statuses exactly as spec
   016 §9 (`validated_within_compilation` /
   `failed_within_compilation_validation` / stays
   `pending_non_sa_validation`); §9's anti-circularity text
   carried over verbatim in substance.

## Determinism

Counting, the frozen seed-117 partition shuffle, and one
seeded donor stream (`random.Random(118)`, spec §3) consumed
in a frozen order. An execution must reproduce its reports
byte-identically except timestamps, and must assert the
partition totals (A = 3,531 / B = 3,471) and the judgeability
counts (J94 = 67, JKUR = 29) before calibrating.

## Stacking

This phase's code reuses Phase-117's machinery
(`phase113_battery` contexts/profiles; `phase117_battery`'s
partition, W1, W4, junction primitives), which lives on PR
#75's unmerged branch. The worktree and PR are therefore
stacked on `phase/117-within-compilation-battery`; the PR
retargets to main when #75 merges.

## Out of scope

Any use of either ICIT layer (Phase-116 R-NONE), any anchor
promotion, any change to spec 016's frozen record, any
external communication, and any merge without the owner's
explicit say-so.
