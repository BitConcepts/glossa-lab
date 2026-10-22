# Spec 062 — Spec 028 Arm A: the Precision Computation, Calibration Repair (Successor to Spec 061)

> ## FROZEN — 2026-10-21
>
> Frozen under the owner's approval of
> 2026-10-21 (amendment package Item 3: take
> Spec 062 through freeze and OSF filing).
> Drafted the same day under the owner's
> amendment-queue commission (item 3: Spec
> 061 calibration repair), including
> drafting-stage computation on synthetic /
> planted data (it scores nothing). The
> freeze decisions DD-062-7 to DD-062-12 are
> recorded in `adjudication.md` §8;
> DD-062-1 to DD-062-6 stand as drafted.
> **The repair ruling (DD-062-9):**
> construction R-1 — per-inscription
> Dirichlet drawing around the imposed
> composition, fixed-uniform coupling,
> κ_i = n_legible(i) − 1 — is adopted
> exactly as drafted; the verbatim redraw
> R-2 is not adopted and its tolerance
> amendment is not taken (R-2 stays on the
> record in `adjudication.md` §3 as a
> non-adopted alternative; R-3 and R-4 stand
> rejected on measurement). The calibration
> seed is fixed at the drafted value
> 20261021 (DD-062-7). This spec files its
> own OSF contract registration at the
> freeze under campaign decision E-1
> (DD-062-10). Execution runs as
> **Phase-424**, allocated at this freeze
> (DD-062-8) — Phase-423 was Spec 061's, and
> no repo record allocated Phase-424 before
> this act. Nothing in this contract has
> been computed on the recorded population:
> no trial has run, no world has been built
> under this contract, and gate 0.5-R has
> not run — it is an execution-time check.
> Execution awaits this freeze merging, the
> OSF registration's approval act, and a
> separate execution order.
>
> **What this spec is.** Spec 061 (Phase-423)
> executed on 2026-10-21 and closed **CANNOT
> BE RUN AS WRITTEN** at its gate 0.5: the
> frozen effect-imposition construction
> (candidate (b), DD-061-13) calibrates the
> boost factor b against the frozen estimator
> applied to the constructed population *in
> expectation*, and that function is a step
> function — A(1) = −0.0025188916876574316
> exactly and A(1.5) = A(2) = A(3) = 1.0
> exactly on the recomputed record — so no
> b in [1, 3] achieves |A(b) − θ| ≤ 1e-6 for
> either scenario. Spec 061's record is
> closed and is **never patched** (§11).
> This spec is its successor: it carries
> Spec 061's precision question, scenarios,
> search frame, gates 0.1–0.4, trial
> construction, resolution and target rules,
> and outcome wordings **verbatim in
> substance** (§§1–5, §4.7 table), and it
> replaces **only** the calibration
> definition (§4.7 step 3) and its gate
> (gate 0.5-R, §3). The defect and the repair
> are recorded in `adjudication.md`
> (DEF-062-1, DD-062-1…DD-062-6).
>
> **Scope fence (campaign decision E-3,
> carried unchanged).** Arm A2 — the decisive
> rerun of the frozen Arm A test — is **not**
> a member of this spec, is **not** designed,
> authorised, or executed by it, and stays
> unarmed. Spec 061's operative target T* is
> **undefined on Spec 061's record and stays
> undefined**; nothing in this draft quotes a
> target from that record. If this successor
> is ever frozen, executed, and returns
> targets, its own operative target is
> defined by the carried rule (DD-061-5,
> §4.5); whether that arms A2 is the owner's
> decision at the mini planning gate a fired
> trigger queues under E-3 — never this
> draft's act.

**Design source:** D-27, arm A1, as in
Spec 061 (experiment-design packet at PR
#195, `docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
§D-27), together with Spec 061's frozen
record (`specs/061-arm-a-precision/spec.md`
§4.7 + §5, `adjudication.md` DD-061-9…
DD-061-15, `outcome.md` — the execution of
record, Phase-423) and Spec 028's frozen
record (`specs/028-harappa-robustness/`,
Phase-393), in particular its generated-worlds
positive control (`calibration.json`: Arm A
positive control at boost 3.0, median
adjusted R² 0.023963353007570576 over
regenerated worlds).

**Claim under test:** `STUDY-SPEC-028/ARM-A`
— unchanged from Spec 061. Spec 028's
Harappa-excluded arm, standing
**INCONCLUSIVE**: median adjusted R² 0.00878,
interval [0.00463, 0.01297] straddling the
0.01 margin. This spec does not re-run
Arm A. It computes, from Phase-393's
recorded resampling distribution, **how much
added non-Harappa material Arm A would need
for its interval to resolve at the 0.01
margin** — a precision computation on a
recorded distribution, whose product is an
intake target.

**AI disclosure:** this draft is produced by
an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per
constitution §VI.

---

## 1. The claim and the record it stands on

The record is Spec 061's §1 record,
unchanged, plus Spec 061's own outcome:

- Arm A population: **1,593 records at 5
  sites** (Mohenjo-daro 1,302; Dholavira 111;
  Lothal 74; Chanhu-daro 54; Kalibangan 52),
  294 inscriptions per draw under the frozen
  cell rarefaction (6 included cells),
  R = 199 draws, B = 499 permutations per
  draw, seed 20261012.
- Median adjusted R² **0.00878393455594817**,
  percentile interval
  **[0.004626892186724407, 0.01297407559730989]**,
  median raw R² 0.022315894493750963, share of
  draws rejecting **0.6231155778894473**,
  median p 0.034.
- Verdict: **INCONCLUSIVE** — the interval
  straddles the margin.
- Spec 061 execution (Phase-423, 2026-10-21):
  gates 0.1–0.4 **PASSED**, gate 0.3 with the
  recorded summary above reproduced
  digit-for-digit; gate 0.5 **FAILED** on the
  step function stated in the header, and the
  spec closed **CANNOT BE RUN AS WRITTEN**.
  No trial ran, no world was built under
  that contract, and no target quantity was
  computed. Its outcome record itself names
  the mechanism and the repair direction:
  the recorded Spec 028 positive control at
  boost 3.0 is a median over *generated*
  worlds — per-inscription drawing creates
  the within-site variation the
  in-expectation construction averages away —
  and "a calibration defined over generated
  worlds … is a different definition, and
  adopting one is an amendment act under a
  new planning gate." This spec is that act,
  in successor form.

### 1.1 The question, in plain words

(Carried verbatim from Spec 061 §1.1.)

Rather than shrug at that straddle, measure
the gap: how much more non-Harappa material,
of the same kind, would it take for the
interval to resolve at the 0.01 margin? The
answer is a number the program can act on —
the intake target that would make Arm A
decidable — stated before anyone goes
looking for data. **The computation measures
the program's own resolution. It establishes
nothing about the ancient world** (design
D-27, stated verbatim in substance; claim
F062-C01).

### 1.2 The hypothesis and its falsifier

(Carried verbatim from Spec 061 §1.2.)

**Hypothesis.** A finite intake target
exists: on a bounded search frame fixed at
the freeze, the computation returns a
smallest added-inscription total that
resolves Arm A at the 0.01 margin under at
least one of the two stated scenarios (§4.2).

**Falsifier** (campaign wording, governing):
**the computation returns no intake target
that resolves Arm A at the 0.01 margin under
either stated scenario.** That outcome is
pre-written in §5 as **NO TARGET UNDER
EITHER SCENARIO**, with the same prominence
as any target returned. "No target" is
always scoped to the frozen search frame
(§4.5): it means no grid point inside the
frame qualified, never that no amount of
data could resolve Arm A in principle.

## 2. Inputs (pinned — identical to Spec 061 §2)

This spec's step-0 pin is the same composite
pin as Spec 061's (DD-061-1, confirmed
DD-061-8). No pin changes: the repair touches
no input, no machinery file, and no recorded
summary.

| Input | Pin / state |
|---|---|
| Phase-393 results (`reports/phase393_results.json`) | SHA-256 `0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607` |
| Corpus layer of record (`backend/glossa_lab/data/yajnadevam_inscriptions.csv`) | SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` |
| Phase-393 machinery (`specs/028-harappa-robustness/pipeline393.py`) | SHA-256 `6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e` |
| Spec 028 margins audit (`specs/028-harappa-robustness/margins-audit.json`) | SHA-256 `15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d` |
| Spec 028 freeze record (`specs/028-harappa-robustness/freeze.json`) | SHA-256 `376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc` |
| Spec 028 calibration record (`specs/028-harappa-robustness/calibration.json`) — the generated-worlds positive control this repair's calibration is modelled on | SHA-256 `4198747b42121fea817db2e5ad82da10cca6118fef39bb14dc13cdf56ac204ff` (as read at Spec 061's freeze, DD-061-8 §9.1) |
| Spec 061 frozen record (`specs/061-arm-a-precision/spec.md`, `adjudication.md`, `claims.json`, `freeze.json`) and its outcome record (`outcome.md`, Phase-423) | Read in full at this draft; the predecessor contract and the failure of record |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`. This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

## 3. Step 0 — gates before any precision quantity (fail-closed)

Gates 0.1–0.4 are Spec 061's gates, carried
verbatim. Gate 0.5 is replaced by gate
0.5-R, which verifies the repaired
calibration of §4.7-R. A failure stops the
execution in the class named; nothing is
repaired at run time.

- **0.1 Composite pin integrity.** Every §2
  input hashes to its freeze-record value,
  including the resampling-distribution pin's
  summary component
  (`phase393_results.json`). A mismatch stops
  the run as **INVALID**.
- **0.2 Population reproduction.** The frozen
  population flow, re-run on the pinned layer,
  reproduces the recorded Arm A population
  exactly: 1,593 records at the 5 named sites
  with the recorded site totals and cell
  counts, 6 included cells, 294 inscriptions
  per draw. A mismatch stops the run as
  **INVALID**.
- **0.3 Recorded-distribution reproduction.**
  The frozen Arm A primary, re-run under the
  recorded machinery and seed (20261012;
  R = 199; B = 499), reproduces the recorded
  summary exactly: median adjusted R²
  0.00878393455594817, interval
  [0.004626892186724407, 0.01297407559730989],
  rejection share 0.6231155778894473. Any
  mismatch stops the run as **INVALID**.
  *Why this gate is preserved by the repair,
  mechanically:* gate 0.3 is a function of
  exactly four things — the §2 pins, the
  frozen `pipeline393` machinery, the recorded
  seed 20261012, and the recorded R/B — and
  §4.7-R changes none of them. The repaired
  calibration (§4.7-R steps 1–5) is downstream
  of gate 0.3, consumes none of gate 0.3's
  inputs, and shares no RNG stream with it
  (the calibration Generator of §4.7-R step 2
  is a separate Generator object, created and
  exhausted before any trial Generator
  exists; gate 0.3's reproduction uses the
  recorded run's own seed discipline, exactly
  as in Spec 061). The amendment is fenced
  the same way Spec 061 fenced its own
  calibration: if gate 0.3 fails under this
  successor, this spec closes fail-closed
  exactly as Spec 061 would have.
- **0.4 Search frame present.** The freeze
  record states, in full: the multiplier grid,
  the search ceiling, the per-grid-point trial
  count, the draws and permutations per trial,
  the simulation seed, and the
  effect-imposition construction (§4.7-R).
  Any element absent stops the run as
  **CANNOT BE RUN AS WRITTEN** before any
  trial.
- **0.5-R Construction calibration
  (repaired; replaces Spec 061's gate 0.5).**
  Per scenario, the §4.7-R calibration is
  verified before any trial: (i) the bracket
  recomputes — A_R(1) < θ < A_R(3), where
  A_R is the drawn-population median of
  §4.7-R step 3; (ii) A_R is strictly
  increasing on the recorded scan grid
  b = 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75,
  3 (the nine scan values are recorded in the
  results JSON); (iii) the bisection achieves
  |A_R(b) − θ| ≤ 1e-6 within 100 iterations,
  with the achieved b and A_R(b) recorded.
  Any failure stops the run as **CANNOT BE
  RUN AS WRITTEN** — the construction cannot
  impose the scenario's θ, and no other
  construction may be supplied at run time.

## 4. The precision computation

Carried from Spec 061 §4 without change,
except §4.7, whose step 3 is replaced by
§4.7-R. No other quantity is computed, and
no verdict about Arm A's bounded claim is
taken.

### 4.1 Base quantities (all from the record)

- Margin: adjusted R² **0.01** (the frozen
  family's single margin; not re-derived).
- Arm A site totals of record: Mohenjo-daro
  1,302; Dholavira 111; Lothal 74;
  Chanhu-daro 54; Kalibangan 52 — total 1,593.
- Recorded point estimate:
  θ̂ = 0.00878393455594817.

### 4.2 The two stated scenarios (design-fixed; carried verbatim)

- **Scenario 1 — true effect at the current
  point estimate:** θ₁ = **0.00878** (the
  design's stated value; the computation uses
  the recorded full-precision θ̂ of §4.1 as
  θ₁'s value, DD-061-4). Being *below* the
  margin, Scenario 1 resolves **downward**:
  resolution means the interval excludes the
  margin from below — toward "no effect of
  the agreed size."
- **Scenario 2 — true effect at 0.015:**
  θ₂ = **0.015** exactly, as the design
  states. Being *above* the margin, Scenario
  2 resolves **upward**: the interval excludes
  the margin from above.

No third scenario, and no other value for
either scenario, may be computed under this
spec. A reader who wants another θ wants a
different spec.

### 4.3 Trial construction (carried verbatim)

At each grid point — a scale multiple *m* of
the current site sizes, on the freeze-fixed
grid (§3 gate 0.4) — and for each scenario
separately, the computation runs the
freeze-fixed number of independent trials.
Each trial:

1. builds a simulated Arm A world at scale
   *m* by **resampling the recorded site
   samples with replacement at *m* times
   their current sizes** — the design's
   method, labelled a simulation over recorded
   data in every output — under the
   freeze-fixed effect-imposition construction
   that makes the world's true adjusted-R²
   effect the scenario's θ (§4.7-R; the
   calibrated boost b* of §4.7-R step 3 is the
   only quantity the repair supplies here,
   exactly where DD-061-13's calibration
   supplied it);
2. runs the frozen Arm A machinery on that
   world (the §2 pipeline; the recorded draw
   design — cell rarefaction, R draws,
   B permutations per draw — at the scale the
   world provides), producing one adjusted-R²
   percentile interval [2.5%, 97.5%] over the
   trial's draws, exactly as Phase-393
   intervals are constructed;
3. records whether that interval **resolves**
   under §4.4.

Added inscriptions in a trial are simulated
resamples of recorded inscriptions. They are
not new data, they carry no new evidence, and
no output may describe them as data the
program holds (claim F062-C09).

### 4.4 The resolution rule (mechanical; carried verbatim)

A trial **resolves** iff its interval
**excludes** the 0.01 margin in its scenario's
direction, strictly (DD-061-2):

- Scenario 1: the interval's upper bound is
  **< 0.01**.
- Scenario 2: the interval's lower bound is
  **> 0.01**.

An interval whose bound equals 0.01 touches
the margin; it does not exclude it, and the
trial does not resolve.

A grid point **qualifies** for a scenario iff
at least **80%** of its trials resolve (the
design's fixed share).

### 4.5 The target rule (mechanical; carried verbatim)

For each scenario independently, grid points
are examined in ascending order of total
added inscriptions. The scenario's **target**
is the **smallest total added-inscription
count at a qualifying grid point**, reported
with:

- the multiple *m* at which it was found;
- its **per-site distribution**: added
  inscriptions allocated across the five Arm A
  sites **in proportion to their recorded site
  totals** of §4.1 (DD-061-3), exact in
  integers at integer multiples, summing
  exactly to the total;
- the qualifying share at that point, and the
  full grid table (every grid point's share,
  both scenarios).

If no grid point inside the frozen ceiling
qualifies for a scenario, that scenario
returns **NO TARGET (within the frozen search
frame)**. The two scenarios' results combine
into exactly one headline under §5. The
operative target rule of DD-061-5 is carried:
the operative target is the larger returned
target; a single returned target is operative
with its scenario condition recorded beside
it; if no target is returned, no operative
target exists under this spec either — and,
separately, Spec 061's T* remains undefined
on Spec 061's record regardless of anything
this spec returns (header; claim F062-C10).

### 4.6 What is not computed (carried verbatim)

No LOSO variant of the target, no per-site
target optimisation, no S-complete variant, no
Arm B quantity, and no re-adjudication of
Arm A. The pooled and LOSO record stands
exactly as Phase-393 left it.

### 4.7 The frozen search frame (carried verbatim from Spec 061 §4.7)

| Element | Frozen value (carried; re-asserted at this successor's freeze) |
|---|---|
| Multiplier grid | Integer multiples m = 1, 2, …, 25, step 1, examined in ascending order of total added inscriptions (added total at m is (m − 1) × 1,593) |
| Search ceiling | m = 25 (added total 38,232; world total 39,825) |
| Trials per grid point | 199 |
| Draws per trial | 199 (the pipeline's frozen DRAWS) |
| Permutations per draw | 499 (the pipeline's frozen PERMS) |
| Simulation seed | 20261021, with Spec 061's stream discipline (one NumPy Generator per scenario, seeded 20261021, consumed in ascending grid order; within a grid point, trials in order 1…199; within a trial, first the template slot resampling (sites in alphabetical order), then the frozen world generation, then the frozen pipeline run) |
| Effect-imposition construction | Candidate (b)'s imposed compositions (DD-061-13 steps 1–2 and trial world step 4), with the calibration of step 3 **replaced by §4.7-R** |
| Per-site distribution | Proportional to the recorded site totals (DD-061-3); at integer multiples the per-site added counts are exactly (m − 1) × (1,302, 111, 74, 54, 52) |

### 4.7-R The repaired calibration (replaces DD-061-13 step 3 only)

DD-061-13 steps 1, 2, and 4 stand verbatim:
(1) the pooled composition is computed
exactly as Spec 028's `build_calibration.py`
computes it; (2) the imposed composition per
site is the pooled composition with the
columns of the site's positive-control sign
set (10 signs per site, from the pinned
margins audit) multiplied by a boost factor
b ≥ 1 and renormalised to sum 1 — call it
p_s(b); (4) a trial world at grid point m is
built exactly as DD-061-13 step 4 states,
with the world's vectors generated by the
frozen `pipeline393.synthetic_entries` under
the imposed compositions p_s(b*). **Only
step 3 — how b is chosen — is replaced:**

3-R. *Calibration over drawn populations.*
   b is chosen per scenario so that A_R(b) = θ,
   where A_R is defined mechanically as
   follows. The calibration sits at the level
   of Spec 028's recorded positive control —
   per draw, one generated population over the
   full template, then the frozen cell
   rarefaction — because that is the quantity
   the record actually reports for candidate
   (b) (median adjusted R² 0.023963353007570576
   at boost 3.0), and because a calibration
   and the trial intervals it serves should
   be medians of the same draw-level
   estimator, not of two differently weighted
   ones (the population-versus-cell weighting
   difference Spec 061 §8 recorded is removed
   by this choice, and its removal is itself
   recorded in §8).
   1. *Fixed randomness (drawn once, before
      any b is evaluated).* The template is the
      recorded Arm A entries (the 1,593
      recorded entries with their site, type
      class, and legible length, in the pinned
      population flow's order). A dedicated
      NumPy Generator — the **calibration
      Generator**, seeded 20261021, a separate
      Generator object from both per-scenario
      trial Generators, created before them and
      used for nothing else — is consumed in
      exactly this order: (i) a uniform array
      U[d, i, k] for draws d = 1…199,
      inscriptions i in template order, and
      composition columns k in the pinned
      `composition_columns` order, each entry
      clipped to [1e-12, 1 − 1e-12] as a
      numerical guard; (ii) for each draw d in
      order, the rarefaction selections: for
      each included cell in the frozen
      `_cells_plan` order, `rng.choice(cell
      size, 49, replace=False)` exactly as the
      frozen `_draw_cells` performs it. The
      uniforms and the selections are then
      **fixed for both scenarios and every b**.
   2. *Per-inscription Dirichlet drawing
      around the imposed composition.* For a
      boost b and draw d, inscription i at
      site s carries the proportion row
      q_i(b) = G_i / Σ_k G_ik, where
      G_ik = GammaQuantile(U[d, i, k]; shape
      κ_i · p_s,k(b)), the gamma quantile
      function evaluated at the fixed uniform,
      and κ_i = n_legible(i) − 1. Three
      properties are definitional, not
      empirical: the row's mean over the
      drawing is exactly the imposed
      composition (E[q_i(b)] = p_s(b), the
      Dirichlet mean — the centre is exact,
      not an approximation); the row varies
      from inscription to inscription at the
      same scale as the frozen construction's
      own token drawing (a Dirichlet(κp) row
      has Var(q_k) = p_k(1 − p_k)/(κ + 1), and
      κ_i = n_legible(i) − 1 makes this
      p_k(1 − p_k)/n_legible(i), exactly the
      variance of a multinomial proportion
      over n_legible(i) tokens — κ_i is
      derived from the record's own drawing,
      not invented; the eligibility floor
      n_legible ≥ 2 gives κ_i ≥ 1); and every
      shape κ_i · p_s,k(b) is positive on the
      pinned composition columns (each column
      is present in the pooled composition,
      and the boost only multiplies).
      Per-inscription drawing is what restores
      the within-site variation the frozen
      construction averaged away: two
      inscriptions at a site carry different
      drawn rows, as they do in Spec 028's
      generated worlds. The draw's count
      vector is vec_i(b) = q_i(b) ·
      n_legible(i) (real-valued; §8 states
      this limit openly).
   3. *The calibration function.* For draw d
      and boost b, the draw statistic is the
      frozen estimator on the fixed rarefaction
      selection S_d applied to the drawn
      population of step 2 — the frozen
      `pipeline393` proportion normalisation,
      Bray–Curtis, PERMANOVA, and `adjusted_r2`
      over the selection's 294 inscriptions,
      permutations off (permutations do not
      enter adjusted R²; the frozen calibration
      of DD-061-13 was likewise permutations
      off). A_R(b) is the **median of the 199
      draw statistics** — the same summary, at
      the same level, as Spec 028's recorded
      positive control.
   4. *Why A_R can calibrate where A could
      not.* The uniforms and selections are
      fixed numbers. The gamma quantile
      function is continuous in its shape
      parameter on (0, ∞) for any fixed
      uniform in (0, 1); p_s(b) is continuous
      in b; the estimator is a ratio of
      polynomials in the proportion rows with
      positive denominators wherever any two
      selected rows differ. Each draw statistic
      is therefore a continuous function of b,
      and a median of finitely many continuous
      functions is continuous. A_R is a
      deterministic continuous function of b —
      not a step function (contrast the frozen
      A: §1), and not a Monte Carlo estimate
      re-drawn at each b (contrast candidate
      R-2 in `adjudication.md` §3, whose
      measured step sizes are recorded there).
      Whether A_R is *strictly increasing* and
      brackets θ is not assumed: gate 0.5-R
      verifies both, on the record, before any
      trial.
   5. *Bisection.* b is found by bisection on
      [1, 3], at most 100 iterations, stopping
      when |A_R(b) − θ| ≤ 1e-6; the achieved b
      and A_R(b) are recorded in the results
      JSON (gate 0.5-R verifies this before any
      trial). The tolerance and bracket are
      carried from DD-061-13 unchanged: 1e-6 is
      more than a thousand times smaller than
      Scenario 1's distance to the margin,
      0.01 − 0.00878393455594817 =
      0.00121606544405183, so calibration error
      cannot confuse the scenarios' geometry.

   The construction's stated limits are
   recorded in §8, including the one this
   repair introduces (calibration rows are
   drawn continuous proportions, where trial
   worlds carry drawn token counts — named
   openly, with the two constructions'
   agreement at boost 3.0 measured at draft
   level on planted data in `adjudication.md`
   §3).

Candidate (a) remains not adopted and
candidate (c) remains rejected, for
DD-061-13's stated reasons. The alternative
repairs considered at this draft — including
the verbatim redraw-per-b median that Spec
061's outcome record suggests — are derived
and disposed of in `adjudication.md` §3,
with draft-level measurements.

## 5. Outcomes (the full set, wordings pre-written; carried verbatim from Spec 061 §5)

The execution's headline is exactly one of
the first four; the §3 stop classes are
closures, not outcomes.

- **TARGET UNDER BOTH SCENARIOS** — both
  scenarios return a target.
- **TARGET UNDER SCENARIO 1 ONLY.**
- **TARGET UNDER SCENARIO 2 ONLY.**
- **NO TARGET UNDER EITHER SCENARIO** — the
  falsifier's outcome (§1.2).

### 5.1 Pre-written outcome wordings

Carried verbatim from Spec 061 §5.1 (the
BOTH, SCENARIO 1 ONLY, SCENARIO 2 ONLY, and
NEITHER forms, and the INVALID form for
gates 0.1–0.3), with two named substitutions
that change no substance: "Spec 061" reads
"Spec 062" where the wording names the
executing spec, and the CANNOT BE RUN AS
WRITTEN (gate 0.4) form gains the gate 0.5-R
form beside it:

- CANNOT BE RUN AS WRITTEN (gate 0.5-R):
  "The precision computation did not run:
  gate 0.5-R (construction calibration)
  failed ([observed values: A_R(1), A_R(3),
  the scan grid, the bisection record]). The
  repaired construction cannot impose the
  scenario's θ on the drawn-population
  calibration, and no other construction may
  be supplied at run time. No target quantity
  was computed. Spec 028 Arm A stands exactly
  as recorded."

## 6. Reporting obligations (carried from Spec 061 §6, with the calibration record updated)

Every product of an execution carries, in its
headline paragraph or first table:

1. the statement that the computation is a
   **simulation over recorded data** —
   Phase-393's recorded resampling distribution
   and the recorded site samples — and that its
   added inscriptions are resamples, not held
   data;
2. both scenario values (θ₁ = 0.00878 as
   recorded; θ₂ = 0.015) and the 0.01 margin;
3. the full grid table of §4.5 (every grid
   point, both scenarios, the resolution
   shares, each with its binomial standard
   deviation under DD-061-11), the frozen
   search frame in full, the per-scenario
   calibration record (the achieved boost b
   and A_R(b) of §4.7-R, **plus the gate 0.5-R
   bracket and scan-grid values**), and, for
   each returned target, its total, multiple,
   and per-site integer distribution;
4. the headline word of §5 and, where a target
   is returned, the operative target with its
   scenario condition named;
5. the fence sentence: "This computation
   measures the resolution of a recorded test.
   It establishes nothing about the ancient
   world."

Deliverables at execution: as in Spec 061 §6
(a results JSON, a report under these headline
rules, the experiment-graph node registered
and verified before the run, the outcome
append in this directory, and the LEDGER
entry). The execution phase number is **Phase-424**,
allocated at the freeze (DD-062-8; OP-062-2
decided there, verified against the root
LEDGER, the frozen specs' freeze records,
and the repository tree).
Foundation check (H21) after the execution
phase: 0 failures, or the outcome record says
why not. Anchors asserted byte-identical
before and after.

## 7. Epistemic limits (binding on all outputs; carried verbatim from Spec 061 §7)

1. **No ancient-world conclusion.** A1
   measures the program's own resolution. No
   output may present a target as evidence for
   or against site-linked repertoire structure,
   movement of people, or any sign meaning.
2. **The frozen verdict stands.** Spec 028
   Arm A's INCONCLUSIVE verdict is not edited,
   superseded, or re-adjudicated by anything
   this spec computes.
3. **A target is not a promise.** A target
   says: *if* real new data of the same kind
   arrives in that amount, *and* the true
   effect is the scenario's θ, the interval
   resolves in at least 80% of trials like
   these. Real data may differ in kind,
   composition, and provenance from resampled
   recorded data; the rerun's actual verdict
   belongs to the rerun alone (Arm A2, not in
   this spec).
4. **"No target" is frame-scoped.** It is a
   statement about the frozen grid and
   ceiling, never about all possible data.
5. Negative, no-target, invalid, and
   cannot-be-run outcomes publish with the
   same prominence as a returned target.

## 8. Risks and honest weaknesses

Spec 061 §8's risks are carried (the recorded
distribution is a summary, not a file of
draws — gate 0.3 remains the answer;
resampled data is tidier than real data; the
small sites dominate the proportional
arithmetic; five sites is few). Two are
restated in the repaired form, and one is new:

- **The calibration and the trials now sit at
  the same level (a recorded change from
  Spec 061, not a silent one).** Spec 061's
  calibration targeted the constructed
  population's expected adjusted R² under the
  full-population estimator, while its trials
  measured resolution under the equal-cell
  draw design; Spec 061 §8 recorded that
  weighting difference openly. The repaired
  calibration targets the median of the same
  draw-level estimator the trials summarise
  (generated population, frozen rarefaction,
  adjusted R² per draw, median over draws) at
  the recorded scale m = 1 — the level of
  Spec 028's recorded positive control. What
  remains different, inherently, is scale: the
  calibration fixes θ at the recorded scale,
  and the trials then measure resolution at
  scaled worlds built around the calibrated
  boost. That is the design's own structure
  (DD-061-15 (iii) computed the m = 1 point
  for the same reason), stated here so no
  reader mistakes the imposed θ for a
  scaled-world quantity.
- **Calibration rows are continuous
  proportions; trial rows are token counts
  (new, introduced by this repair, stated
  openly).** The calibration draws of §4.7-R
  give each inscription a Dirichlet proportion
  row centred exactly on its site's imposed
  composition, with variance matched to the
  frozen token drawing; the trial worlds of
  §4.3 are generated by the frozen
  `synthetic_entries`, whose rows are integer
  token counts drawn from the same imposed
  composition. The two row kinds have the
  same centre and the same per-column
  variance by construction, but they are not
  the same distribution (a continuous row is
  never a token count vector, and their
  higher moments differ). The draft measured
  the two constructions' agreement where the
  record gives a comparison — the median at
  boost 3.0 on planted data, against both the
  verbatim redraw construction and Spec 028's
  recorded value (`adjudication.md` §3). The
  freeze considered the verbatim
  redraw construction recorded there and did
  not adopt it (DD-062-9; OP-062-4 decided):
  R-1 as drafted is the frozen construction,
  and the tolerance change R-2 requires (its
  calibration function is a step function,
  and the frozen 1e-6 tolerance is not
  attainable on it in general; the measured
  step sizes are in `adjudication.md` §3) is
  not taken. What may not happen
  is a silent substitution at run time: gate
  0.5-R verifies the construction this spec
  freezes, whichever one the freeze adopts.
- **The calibration is now seed-dependent in
  a way the frozen one was not.** The frozen
  A(b) was deterministic and seed-free; A_R
  depends on the 199 drawn worlds, hence on
  the calibration Generator's seed. The draft
  carries the frozen seed value (20261021) on
  a separate Generator (§4.7-R step 3-R.1) so
  that no new constant enters silently; the
  freeze fixes that drafted value as the
  calibration seed and substitutes no fresh
  seed (DD-062-7; OP-062-1 decided). Either
  way the seed, the
  W = 199 world count, and the draw order are
  freeze-record values, and gate 0.5-R's
  recorded scan makes a badly drawn world set
  visible before any trial: a world set whose
  A_R does not bracket θ or does not increase
  closes the run instead of calibrating badly.

## 9. Stop conditions and outcome classes

Execution ends in exactly one of:

- **TARGET UNDER BOTH SCENARIOS**,
  **TARGET UNDER SCENARIO 1 ONLY**, or
  **TARGET UNDER SCENARIO 2 ONLY** — per
  §4–§5, after all gates pass.
- **NO TARGET UNDER EITHER SCENARIO** — the
  falsifier's outcome, after all gates pass.
- **INVALID** — a §2 pin mismatches (0.1); the
  population does not reproduce (0.2); or the
  recorded distribution does not reproduce
  (0.3).
- **CANNOT BE RUN AS WRITTEN** — the frozen
  search frame is incomplete (0.4), or the
  repaired construction cannot impose a
  scenario's θ under gate 0.5-R.

## 10. Execution shape (gated; NOT run by this draft; every step OWNER-APPROVAL)

1. **Freeze** of this spec — TAKEN
   2026-10-21 under the owner's approval
   (amendment package Item 3): OP-062-1…
   OP-062-4 decided in `adjudication.md` §8
   (DD-062-7…DD-062-10), the execution phase
   number Phase-424 allocated (DD-062-8),
   and the AEE freeze gate passed
   (`aee/freeze-aee-note.md`).
2. **OSF contract registration** for this
   spec at its freeze, under campaign decision
   E-1 as Spec 061 filed its own (DD-062-10).
   The filing record is
   `osf-spec-registration.md`, completed by
   append after the filing exists. Steps
   3–6 below remain gated on the
   registration's approval act and a
   separate execution order (DD-062-11).
3. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
   **OWNER-APPROVAL** (as part of the
   execution order).
4. **Step 0** (§3) — composite pin, population
   reproduction, recorded-distribution
   reproduction, search-frame assertion,
   gate 0.5-R calibration verification.
5. **Computation** (§4) — both scenarios,
   ascending grid, full grid table recorded.
6. **Outcome** (§6) — appended records only;
   anchors asserted byte-identical;
   foundation check reported as measured.
   No Arm A2 step exists in this shape.

## 11. What this spec is not

Not a patch to Spec 061 (its frozen record,
its outcome, and its undefined T* stand
exactly as executed; this spec supersedes it
only as a successor contract for a future
run), not a rerun of Arm A (that is Arm A2,
contingent and outside this spec), not a new
corpus, not a verdict on
`STUDY-SPEC-028/ARM-A`, not an intake act, and
not an authorisation to execute. It is a
precision computation on a recorded
distribution, designed so that its honest
outcomes — including returning no target at
all — are written down before any trial is
run.

**This does not establish** (draft-level
demonstration, `adjudication.md` §3): the
planted-data demonstration filed with this
draft establishes that the repaired
construction *can* calibrate — that A_R is
continuous and increasing on planted data and
that a b* meeting the frozen 1e-6 tolerance
exists there for both frozen θ values. It
establishes nothing about the real corpus,
nothing about whether A_R brackets θ on the
recorded population (that is gate 0.5-R's
execution-time check), and nothing about the
precision question's answer, which no
drafting-stage computation has touched.

---

*AI disclosure: drafted by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
