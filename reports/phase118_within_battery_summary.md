# Phase-118 — Within-Compilation Validation Battery v2 for the 44 SA-Lineage Anchors

**Spec:** specs/017-phase118-within-compilation-validation-v2 (frozen before any results) · **Date:** 2026-10-07 · **GPU device:** cpu (torch absent)

Successor to Phase-117 (spec 016), whose battery was rejected at calibration: its W3 (leave-one-out-minus-self junction reference; PASS band p <= 0.05 attained by 3/81 judged core signs) made its own PASS nearly unattainable, and its KUR113 gate passed vacuously on universal indeterminacy. This battery is the commissioned W1-primary redesign, entirely Holdat-internal: W1 split-half positional cross-fit (spec-011 T2a thresholds unretuned) as the primary instrument; W3 junction coherence rebuilt cross-fit (model and phi from the opposite partition half; donor-permutation null retained per direction; median-donor bands); W4 site-stratum stability as a FAIL-guard only. W2 remains dropped as decision-bearing (spec 016 section 4.2). A VALIDATED outcome earns the status `validated_within_compilation` (spec 017 section 9, carrying spec 016 section 9): internal coherence within Holdat only — NOT independent validation, and not the `validated_non_sa` status of specs 011/014.

## Verdict

**BATTERY REJECTED at calibration.** The frozen gates of spec 017 section 6 were not both met, so FLAGGED44 was never run and the anchors file was not modified. The battery may not be re-tuned under this spec.

## Calibration (executed before the 44; reported whatever it showed)

phi per direction (10th percentile, type-7, of STRICT94 cross-fit self-scores): modelA→scoreB = **-7.192755** (n = 83); modelB→scoreA = **-7.088781** (n = 89).

| Gate | Denominator | Result | Requirement | Verdict |
|---|---|---|---|---|
| Positive (STRICT94) | J94 = 67 judgeable of 94 (tally over all 94: 14 V / 21 D / 59 U) | VALIDATED 14 / 67 = 0.2090 | share >= 0.5 and n >= 50 | **FAIL** |
| Negative (KUR113) | JKUR = 29 judgeable of 113 (tally over all 113: 0 V / 0 D / 113 U) | VALIDATED 0, DEMOTE 0 / 29 = 0.0000, UNRESOLVED 29 | VALIDATED = 0 and DEMOTE share >= 0.25 and n >= 8 | **FAIL** |

Negative-gate diagnostic: in **0 of 58** JKUR direction records is the sign's cross-fit score below its direction's phi, while every judgeable direction's donor p-value is >= 0.50 (minimum 0.579) — the relative (donor) leg separates the known-bad `kur` readings from the core's fabric, but the absolute leg never fires, because the phoneme pair of `kur` occupies high-probability junction cells. The conjunctive FAIL band therefore produces no kur demotion and the negative gate fails on its discrimination clause — it does not pass vacuously. This is the coarse-fabric limit registered in spec section 10, now measured under the cross-fit construction as well.

Per-instrument states (calibration):

| Set | Instrument | PASS | FAIL | INDETERMINATE |
|---|---|---|---|---|
| STRICT94 | W1 | 63 | 5 | 26 |
| STRICT94 | W3 | 22 | 11 | 61 |
| STRICT94 | W4 | 44 | 10 | 40 |
| KUR113 | W1 | 0 | 0 | 113 |
| KUR113 | W3 | 0 | 0 | 113 |
| KUR113 | W4 | 0 | 0 | 113 |

## Sets and corpora (recomputed; assertions in spec sections 2-3)

- FLAGGED44: 44 anchors (24 SA_DERIVED + 20 SA_CONFIRMED_ONLY; 43 HIGH + M293 MEDIUM).
- STRICT94: 94 anchors (90 HIGH + 4 MEDIUM); Holdat token coverage 0.7368 (5,159 / 7,002). Judgeable core J94 = 67 (asserted).
- KUR113: 113 premise-superseded anchors, all reading `kur`. Judgeable JKUR = 29 (asserted; W3-scorable only — the cohort is structurally W1-unscorable and W4-unjudgeable).
- Holdat (sole corpus): 1670 inscriptions / 7002 tokens; frozen partition (seed 117, carried from spec 016) asserted at A = 3531 / B = 3471 tokens. No ICIT layer was loaded or consulted (Phase-116 constraint).

## Limitations (registered in spec section 10)

Single-compilation ceiling: every instrument measures coherence inside one modern compilation; systematic error in Holdat or in STRICT94's readings is invisible to this battery by construction. Cross-fit halves the evidence twice over (W1 and rebuilt W3 both derive and score on disjoint halves); per-direction W3 scores may average as few as 2 junction observations (the floor at which the negative control remains testable). The negative gate rests on W3 alone over 29 judgeable kur signs. The section-8 conjunction is reachable by at most 11/44 flagged anchors; M235, M254, M402 are judgeable by no instrument and UNRESOLVED by construction. A FAIL demotes to CANDIDATE; it does not declare the reading false.

## Deviations

None in the battery's frozen definitions, thresholds, floors, bands, partition, seeds, or decision rule. Conventions fixed in the frozen spec text itself (not post-hoc): phi's percentile is the linear-interpolation (type-7) 10th percentile per direction; the donor stream is one random.Random(118) consumed in sorted-sign order (STRICT94 LOO, KUR113, FLAGGED44), per sign in direction order modelA_scoreB then modelB_scoreA, with guard-rejected directions consuming no draws; W2's descriptive support/context counts are computed against the evaluation core (leave-one-out core during STRICT94 calibration).

## Verification

Recorded in the phase ledger entries and the PR body (full backend suite; foundation check per H21; ruff).

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.
