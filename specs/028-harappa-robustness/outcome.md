# Spec 028 — Phase-393 Outcome Record

Executed 2026-10-11 under the merged freeze (PR #158,
digest `619ab0c3…`) and the OSF registration of the frozen
contract (https://osf.io/7m35w/, filed
2026-10-11T16:13:11Z, before execution). Single clean run:
540.6 s, seed 20261012; population guard reproduced the
frozen margins exactly (zero mismatches); input hashes
asserted. Results: `reports/phase393_results.json`,
`reports/phase393_report.md`. All decisive numbers below
were recomputed from the results JSON.

## Verdicts (frozen rules, applied mechanically)

### Arm A — INCONCLUSIVE (primary)

Bounded claim: "site-linked repertoire structure at/above
the practical margin exists among the non-Harappa sites."

- Median adjusted R² **0.00878** — below the 0.01 margin;
  interval **[0.00463, 0.01297]** straddles the margin.
- Rejection share **0.623** (median p 0.034); median raw
  R² 0.02232.
- LOSO medians all below the margin: Mohenjo-daro drop
  0.00656; Dholavira 0.00948; Lothal 0.00884; Chanhu-daro
  0.00761; Kalibangan 0.00859.
- Controls PASS (negative 0.00046, share 0.040; positive
  0.02396 [0.0156, 0.0336], share 1.000).
- S-complete sensitivity (labelled, no verdict): 0.00647
  [0.00224, 0.01089], share 0.241.
- Rule application: SUPPORTED fails on every clause
  (share, interval, jackknife). CONTRADICTED does not
  fire: the interval is not entirely at/below the margin
  and the rejection share is far above 0.05. INCONCLUSIVE.

### Arm B — INCONCLUSIVE (secondary)

Bounded claim: "the site effect is not an
inscription-count artifact of the large corpora."

- Median adjusted R² **0.02237** — ABOVE Phase-392's
  full-population 0.01677; interval **[0.01222, 0.03333]**
  entirely above the margin; rejection share **0.955**;
  median p 0.004.
- LOSO: drop-Harappa median **0.00661** [0.00159, 0.01153]
  — below the margin. Every other drop stays at/above
  0.0226 (Mohenjo-daro 0.02376; Dholavira 0.02436; Lothal
  0.02475; Chanhu-daro 0.02256; Kalibangan 0.02454).
- Controls PASS (negative 0.00204, share 0.055; positive
  0.01670 [0.0105, 0.0240], share 1.000). Quota
  allocations reproduced the freeze's deterministic table
  exactly.
- Rule application: the SUPPORTED rule's jackknife clause
  fails on the Harappa drop alone, so the verdict is
  INCONCLUSIVE — the same failure mode as Phase-392.
  CONTRADICTED does not fire. Recorded plainly: the
  equal-weight point estimate is HIGHER than the
  count-weighted one, which is the direction the bounded
  claim asserts; the frozen verdict is nevertheless
  INCONCLUSIVE because the claim's own rule requires
  jackknife stability, and the effect does not survive
  Harappa's removal under either weighting.

### Arm C — exploratory (no verdict, as frozen)

- Harappa centroid vs pooled others: Bray–Curtis
  **0.3410**. Within TAB only: **0.4953**; within SEAL
  only: **0.1114**. Harappa's own SEAL-vs-TAB centroid
  distance: **0.4501**. Harappa's distinctiveness is
  carried overwhelmingly by its tablets, not its seals.
- Largest per-column contributions to Harappa vs pooled
  others: M328 **0.0734** (≈21.5% of the distance), M089
  0.0275, M095 0.0216, M087 0.0172, M176 0.0162, M122
  0.0145, UNMAPPED 0.0132, M086 0.0128. One column
  (M328) carries about a fifth of Harappa's total
  compositional distance from the other sites.

## What the two arms jointly establish

The question Phase-392 left open is answered in the
descriptive record, under two different estimands:

1. Without Harappa, the site effect among the remaining
   five sites sits BELOW the practical margin (Arm A
   point estimate 0.00878; S-complete 0.00647). The
   margin-clearing structure Phase-392 detected does not
   exist independently of Harappa at the frozen standard.
2. Equal site weighting does not shrink the effect — it
   grows (Arm B 0.02237 vs Phase-392's 0.01677) — so the
   effect is not produced by the large corpora's
   inscription counts. But it remains Harappa-dependent:
   the drop-Harappa LOSO collapses below the margin under
   both weightings (Phase-392: 0.00928; Arm B: 0.00661).

Neither arm's verdict is SUPPORTED, and neither is
CONTRADICTED: in both arms the effect is real enough to
detect frequently and to straddle or clear the margin in
the full configuration, and in both it fails the frozen
jackknife clause on exactly one site. The joint reading
is stated in `historical-assessment-phase392.md`;
Phase-392's record itself is not modified.

## Controls note

The executed controls reproduce the pre-freeze
calibration's control summaries EXACTLY (all four medians,
intervals, and shares identical to `calibration.json`) —
the executed control construction is numerically the
calibrated one, as the freeze required (shared pipeline,
fresh per-arm RNG at the frozen seed).

## Deviations (execution)

1. Two aborted launches preceded the clean run, both in
   the execution script's non-frozen glue, neither
   producing any outcome or results file: (a) the first
   launch called a nonexistent loader name on the frozen
   margins-audit module (AttributeError at startup);
   (b) the second launch hit a NameError because the
   script's verbatim pipeline slice initially began two
   lines late, omitting the ALPHA/MARGIN_R2 constants.
   Both were fixed in the script's own sections only; the
   frozen pipeline section is verbatim in the executed
   script (test-pinned), and the inputs, seed, and frozen
   design were untouched. The clean run above is the
   single executed run.
2. No other deviations. The frozen pipeline, verdict
   rules, quota construction, control construction, and
   Arm C item list were executed as frozen.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.
