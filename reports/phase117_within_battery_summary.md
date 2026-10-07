# Phase-117 — Within-Compilation Validation Battery for the 44 SA-Lineage Anchors

**Spec:** specs/016-phase117-within-compilation-validation (frozen before any results) · **Date:** 2026-10-07 · **GPU device:** cpu (torch absent)

Phase-116 (spec 015) returned R-NONE — no conjunctive cross-corpus positional gate on the Holdat/ICIT pair — and licensed validation within a single compilation. This battery is entirely Holdat-internal: W1 split-half positional cross-fit (spec-011 T2a thresholds unretuned), W3 junction coherence against a seeded donor-permutation null, W4 site-stratum stability. W2 (spec-011 T3) was dropped as a decision-bearing instrument at design (spec section 4.2); its statistics are recorded descriptively in the W3 records. A VALIDATED outcome earns the status `validated_within_compilation` (spec section 9): internal coherence within Holdat only — NOT independent validation, and not the `validated_non_sa` status of specs 011/014.

## Verdict

**BATTERY REJECTED at calibration.** The frozen gates of spec 016 section 6 were not both met, so FLAGGED44 was never run and the anchors file was not modified. The battery may not be re-tuned under this spec.

## Calibration (executed before the 44; reported whatever it showed)

| Set | n | VALIDATED | DEMOTE | UNRESOLVED | Gate |
|---|---|---|---|---|---|
| STRICT94 (positive, leave-one-out) | 94 | 2 | 19 | 73 | >= 47 required: **FAIL** |
| KUR113 (negative control) | 113 | 0 | 0 | 113 | <= 5 required: **PASS** |

phi (10th percentile of STRICT94 leave-one-out W3 self-scores, n = 81): **-7.461366**.

Per-instrument states (calibration):

| Set | Instrument | PASS | FAIL | INDETERMINATE |
|---|---|---|---|---|
| STRICT94 | W1 | 63 | 5 | 26 |
| STRICT94 | W3 | 3 | 9 | 82 |
| STRICT94 | W4 | 44 | 10 | 40 |
| KUR113 | W1 | 0 | 0 | 113 |
| KUR113 | W3 | 0 | 0 | 113 |
| KUR113 | W4 | 0 | 0 | 113 |

## Sets and corpora (recomputed; assertions in spec section 2-3)

- FLAGGED44: 44 anchors (24 SA_DERIVED + 20 SA_CONFIRMED_ONLY; 43 HIGH + M293 MEDIUM).
- STRICT94: 94 anchors (90 HIGH + 4 MEDIUM); Holdat token coverage 0.7368 (5,159 / 7,002).
- KUR113: 113 premise-superseded anchors, all reading `kur`.
- Holdat (sole corpus): 1670 inscriptions / 7002 tokens; frozen partition (seed 117) asserted at A = 3531 / B = 3471 tokens. No ICIT layer was loaded or consulted (Phase-116 constraint).

## Limitations (registered in spec section 10)

Single-compilation ceiling: every instrument measures coherence inside one modern compilation; systematic error in Holdat or in STRICT94's readings is invisible to this battery by construction. W3 concentration: 27/44 flagged anchors are judgeable by W3 alone. W1 fully judges 13/44. The negative gate is asymmetric (KUR113 is largely unjudgeable: W1 cannot PASS below 8 tokens and W4 cannot PASS below two 4-token sites, so the kur cohort structurally cannot validate; the gate verifies non-validation of the judgeable minority and the binding gate is the positive one). A FAIL demotes to CANDIDATE; it does not declare the reading false.

## Deviations

None in the battery's frozen definitions, thresholds, floors, bands, partition, seeds, or decision rule. Implementation conventions fixed where the spec is silent, recorded here per spec section 12: phi's percentile is the linear-interpolation (type-7) 10th percentile; W3's donor stream is one random.Random(117) consumed in sorted-sign order (STRICT94 LOO, KUR113, FLAGGED44); W2's descriptive support/context counts are computed against the evaluation core (leave-one-out core during STRICT94 calibration).

## Verification

Recorded in the phase ledger entries and the PR body (full backend suite; foundation check per H21; ruff).

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.
