# Plan — Spec 016 / Phase-117 Within-Compilation Validation Battery (DESIGN ONLY)

Design phase only. This plan produces the frozen spec and its
feasibility appendix; it implements nothing and runs nothing.
Execution follows the Phase-113/115 pattern (frozen spec →
implementation → H23 graph registration → calibration → main
run → reports → suite/foundation → ledgers → PR) **only after
the owner's separate execution approval** (spec §11).

## Approach (design phase)

1. **Record synthesis.** Specs 011/014 and the Phase-116
   harmonization record fix the design space: the cross-corpus
   gate is forbidden (R-NONE); T2a was sound; T2b's failures
   were inventory-membership artifacts; T3's support axis is a
   frequency proxy and its legality axis has base rate 1.000.
   Each spec-011 component's fate is recorded in the spec's
   context table — nothing silently kept, nothing silently
   dropped.
2. **Feasibility before freeze.** Design-stage statistics from
   Holdat counts only (no instrument scores any sign): set
   sizes and attestation distributions; the frozen partition's
   per-half judgeability; T3-design support/context
   availability (the W2 keep/drop basis); junction-context
   availability (W3 floor); site-stratum availability (W4
   floors). Frozen choices cite these numbers; the full tables
   are the spec's Appendix A, finalized in the commit after
   the freeze.
3. **Instruments.** W1 split-half positional cross-fit (T2a's
   thresholds carried over unretuned; derivation and scoring
   on disjoint halves). W2 dropped with numbers. W3 junction
   model over STRICT94 readings with an absolute floor defined
   as a frozen quantile of core self-scores and a seeded
   donor-permutation null over frequency-band readings. W4
   site-stratum stability with an attestation-asymmetric FAIL
   (modal flip requires ≥ 8 tokens in each disagreeing
   stratum).
4. **Decision structure.** Calibration gates in the
   011/014 pattern (STRICT94 LOO ≥ 47/94; KUR113 ≤ 5/113),
   then a mechanically applicable rule whose VALIDATED
   conjunction (W3 PASS + one positional PASS + no FAIL)
   is shaped by the Appendix A judgeability split, with
   every instrument holding veto power via DEMOTE.
5. **Claim discipline.** §9 coins `validated_within_compilation`,
   forbids its shortening or conflation with `validated_non_sa`,
   fixes the exact claim a pass supports, preserves the
   SA-lineage provenance record under all outcomes, and makes
   every outcome explicitly provisional against genuinely
   independent corpora.

## Determinism

The battery as designed is counting, seeded shuffling, and
seeded donor draws (all streams seeded 117, §3); an execution
must reproduce its reports byte-identically except timestamps,
and must assert the frozen partition totals (A = 3,531 /
B = 3,471 tokens) before calibrating.

## Out of scope for the design phase

Implementation, calibration, any run against any anchor, any
anchors-file change, any use of either ICIT layer, and any
external communication.
