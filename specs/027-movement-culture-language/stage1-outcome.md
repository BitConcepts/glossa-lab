# Spec 027 — Stage 1 Outcome Record (Phase-392, Q2 gate)

Executed 2026-10-11 under `stage1-freeze.md` as amended
(freeze digest `30861f04e5968ed5c488c01dbc74891c7977cd256bc7
cf9ed075c1513d145762`, merged PR #154 `4684408f`), after the
OSF registration of the frozen contract
(https://osf.io/pnqrx/, filed 2026-10-11T14:02:01Z — see
`stage1/osf-registration.md`). H23 order observed: script →
graph module → registration verified → run.

## Verdict: INCONCLUSIVE

Bounded claim (freeze §1): in the named corpus, under M77,
after rarefaction to a common cell size and stratification
by object type, site explains more recorded sign-repertoire
variation than expected under permuted site labels, at the
declared practical margin (adjusted R² = 0.01).

**Primary (199 rarefaction draws, 499 permutations within
type strata per draw, seed 20261011):**

- Median adjusted PERMANOVA R² **0.01677**; 95% percentile
  interval **[0.01032, 0.02397]** — entirely above the
  margin.
- Share of draws rejecting at α = 0.05: **1.000** (median
  p = 0.002).
- Median raw R² 0.02934 (transparency; rules use adjusted).
- Cells included 8 (392 inscriptions per draw); excluded
  cells as frozen: Dholavira TAB 15, Lothal TAB 2,
  Chanhu-daro TAB 2, Kalibangan TAB 3.

**Controls (identical pipeline; failure would have made
the run INVALID):**

- Negative (pooled composition): median adjusted R²
  0.00020, rejection share 0.005 — **PASS**.
- Positive (deterministic planted effect): median adjusted
  R² 0.02121, interval [0.01580, 0.02760], rejection share
  1.000 — **PASS**. The instrument discriminates at the
  design's operating point; the observed primary effect
  (0.01677) sits between the negative control (~0) and the
  planted ~2×-margin control (0.02121).

**Jackknife (leave-one-site-out, median adjusted R²):**
drop Harappa **0.00928**; drop Mohenjo-daro 0.01806; drop
Dholavira 0.01863; drop Lothal 0.01687; drop Chanhu-daro
0.01677; drop Kalibangan 0.01708.

**Why INCONCLUSIVE (freeze §6, applied mechanically):**
the SUPPORTED rule requires every LOSO median above the
margin; dropping Harappa takes the median adjusted R² to
0.00928, below 0.01 — Harappa is partially load-bearing
for clearing the practical margin (not for detection: the
full-population interval clears the margin and every draw
rejects). The CONTRADICTED rule does not fire (rejection
is unanimous and the interval is above the margin). The
frozen taxonomy therefore returns INCONCLUSIVE — the
freeze's own named case: a jackknife range crossing the
margin while the primary interval does not.

**Labelled sensitivity (no verdict):** S-complete
(completeness-'N' excluded; 2,564 records, 6 cells):
median adjusted R² 0.01793, interval [0.01139, 0.02868],
rejection share 1.000 — consistent with the primary.

## What this does and does not mean

- Detection is not in doubt at this design: site labels
  carry repertoire information far beyond permutation in
  every rarefaction draw, and the controls show the
  instrument would have said so falsely ~0.5% of the time
  and would have caught a planted effect of this size.
- What is not established at the frozen standard is the
  *practical, site-general* claim: the margin-clearing
  effect size depends on the corpus's dominant site. The
  bounded claim is neither SUPPORTED nor CONTRADICTED.
- This result does not revise Phase-137's F3 SUPPORTED
  verdict: that test ran on a different layer (ICIT-native
  horus84) under a different frozen design (no rarefaction
  to a common cell size, no adjusted-margin rule, no
  jackknife clause) and was margin-adjudicated in Spec 026
  on that basis. The two results are recorded side by side;
  neither mechanically revises the other. No anchor is
  touched by this stage (anchors are sign readings; this
  stage computed none).
- The negative closure (spec §7.2) does **not** fire: it is
  bound to CONTRADICTED. Equally, INCONCLUSIVE authorises
  no downstream repertoire-geography work: Stage 2 remains
  unexecuted, Q6 stands NOT-YET-TESTABLE from Stage 0, and
  any further Stage 1 design (e.g. a site-balanced
  estimand) would require a new owner decision, a new
  freeze, and a new registration.

## Deviation recorded

The first Phase-392 launch stopped as INVALID on the
script's own population guard: a defective comparison
(sorted site list vs the unsorted frozen constant) reported
a population mismatch. The stopped run's own recorded flow
was then diffed against the frozen audit and reproduced it
**exactly** (every flow count, the cell table, 3,030
analysis records, 125 columns) — the population was never
in question; the guard was. The comparison was corrected
(one line), the event pair is committed in this branch's
history, and the corrected run reproduced the population
(`population_reproduced: true`) before computing outcomes.
No frozen rule, count, threshold, or design quantity was
changed. The stopped run's outputs are preserved in the
program scratch record.

## Products

`reports/phase392_results.json`, `reports/phase392_report.md`
(generated by the run), this record, ledger entries.
Anchors byte-identical; PRED untouched; no external deposit
in this stage beyond the pre-execution OSF registration.

AI disclosure: executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per
constitution sec.VI.
