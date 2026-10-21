# Spec 061 — Spec 028 Arm A: the Precision Computation (Arm A1 of Design D-27)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-21
>
> Drafted under the runnable-experiments campaign
> plan approved by the owner AS WRITTEN on
> 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`),
> Part 2, member 18: design D-27, **arm A1 only**.
> The portfolio triage of 2026-10-21 found D-27
> **RIPE (arm A1)**. Drafting is the act this
> campaign approval covers; **the freeze and the
> execution of Spec 061 are separate later acts.**
> No AEE lifecycle hooks have run on this draft;
> they are a freeze gate. Nothing in this draft
> has been computed, frozen, registered, or filed.
>
> **Scope fence (campaign decision E-3).** Arm A2 —
> the decisive rerun of the frozen Arm A test — is
> **not** a member of this pass and is **not**
> designed, authorised, or executed by this spec.
> Its contingent status and its trigger's exact
> definition are recorded in `adjudication.md`
> §6 and in claim F061-C14. A fired trigger queues
> a mini planning gate; it does not join this pass.
>
> The execution phase number is **unassigned** at
> this draft. Phase-400 is Spec 036's, Phase-401
> Spec 038's, Phase-402 Spec 037's, and Phase-403
> Spec 039's; Spec 040 allocated none. Spec 061
> allocates its phase number at the freeze act,
> from the merged record as it then stands
> (DD-061-7).

**Design source:** D-27, arm A1, in the
experiment-design packet at PR #195
(`docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
§D-27, read in full at this draft). The design
governs the substance of this spec, including
the two stated scenarios and the 0.01 margin.

**Claim under test:** `STUDY-SPEC-028/ARM-A` —
Spec 028's Harappa-excluded arm, standing
**INCONCLUSIVE**: median adjusted R² 0.00878,
interval [0.00463, 0.01297] straddling the 0.01
margin. This spec does not re-run Arm A. It
computes, from Phase-393's recorded resampling
distribution, **how much added non-Harappa
material Arm A would need for its interval to
resolve at the 0.01 margin** — a precision
computation on a recorded distribution, whose
product is an intake target.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

Spec 028 (Phase-393) ran Arm A with Harappa
removed entirely, to ask whether site-linked
repertoire structure at or above the program's
practical margin (adjusted R² 0.01) exists among
the non-Harappa sites. Its recorded primary
(`reports/phase393_results.json`, SHA-256
`0a1657a8…`, recomputed at this draft):

- Arm A population: **1,593 records at 5 sites**
  (Mohenjo-daro 1,302; Dholavira 111; Lothal 74;
  Chanhu-daro 54; Kalibangan 52), 294
  inscriptions per draw under the frozen cell
  rarefaction (6 included cells), R = 199 draws,
  B = 499 permutations per draw, seed 20261012.
- Median adjusted R² **0.00878393455594817**,
  percentile interval
  **[0.004626892186724407, 0.01297407559730989]**,
  median raw R² 0.022315894493750963, share of
  draws rejecting **0.6231155778894473**, median
  p 0.034.
- Every leave-one-site-out median also below the
  margin (Mohenjo-daro 0.00656; Dholavira
  0.00948; Lothal 0.00884; Chanhu-daro 0.00761;
  Kalibangan 0.00859). Controls passed.
- Verdict: **INCONCLUSIVE** — the interval
  straddles the margin, so the current data
  cannot tell a real-but-small effect from none
  at the agreed size.

### 1.1 The question, in plain words

Rather than shrug at that straddle, measure the
gap: how much more non-Harappa material, of the
same kind, would it take for the interval to
resolve at the 0.01 margin? The answer is a
number the program can act on — the intake
target that would make Arm A decidable — stated
before anyone goes looking for data. **The
computation measures the program's own
resolution. It establishes nothing about the
ancient world** (design D-27, stated verbatim
in substance; claim F061-C01).

### 1.2 The hypothesis and its falsifier

**Hypothesis.** A finite intake target exists:
on a bounded search frame fixed at the freeze,
the computation returns a smallest added-
inscription total that resolves Arm A at the
0.01 margin under at least one of the two
stated scenarios (§4.2).

**Falsifier** (campaign wording, governing):
**the computation returns no intake target
that resolves Arm A at the 0.01 margin under
either stated scenario.** That outcome is
pre-written in §5 as **NO TARGET UNDER EITHER
SCENARIO**, with the same prominence as any
target returned. "No target" is always scoped
to the frozen search frame (§4.5): it means no
grid point inside the frame qualified, never
that no amount of data could resolve Arm A in
principle.

## 2. Inputs (pinned at this draft; re-asserted at the freeze)

This spec's subject is a recorded distribution,
so its step-0 pin is **composite** (DD-061-1,
and see the defect recorded in §2.1):

| Input | Pin / state |
|---|---|
| Phase-393 results (`reports/phase393_results.json`) — the recorded resampling distribution's summary of record: Arm A median, interval, rejection share, draw and permutation counts | SHA-256 `0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607` (recomputed at this draft from `main` at `83b6a563402b02809ab1143848e4dd2c0cfd9de3`) |
| Corpus layer of record (`backend/glossa_lab/data/yajnadevam_inscriptions.csv`) — the layer the recorded site samples are drawn from | SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` (recomputed at this draft) |
| Phase-393 machinery (`specs/028-harappa-robustness/pipeline393.py`) | SHA-256 `6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e` (recomputed at this draft) |
| Spec 028 margins audit (`specs/028-harappa-robustness/margins-audit.json`) — Arm A site totals, cells, included/excluded cells | SHA-256 `15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d` (recomputed at this draft) |
| Spec 028 freeze record (`specs/028-harappa-robustness/freeze.json`) | SHA-256 `376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc` (recomputed at this draft) |
| Spec 028 design (`specs/028-harappa-robustness/spec.md`) — the frozen Arm A machinery, seed, verdict family, and OSF registration (osf.io/7m35w) this computation is about | Read in full at this draft |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

### 2.1 Defect recorded at draft (DEF-061-1)

The design and the triage speak of "Phase-393's
recorded resampling distribution." **No
per-draw distribution is on record in the
repository.** `phase393_results.json` records
only the distribution's summaries (median,
percentile interval, rejection share, median p)
for each arm and cell; the per-draw adjusted-R²
values the pipeline computes in memory
(`pipeline393.py`: `adj_draws`) were not
written to any file. The distribution is
therefore pinned **as a composite**: its
recorded summary (the results file) **plus**
the exact inputs and machinery that produced
it (corpus layer, pipeline, margins audit,
freeze record, seed 20261012, R = 199,
B = 499), and step 0 (§3, gate 0.3) requires
the recorded summary to be **reproduced
exactly** by re-running the frozen Arm A
primary before any precision quantity is
computed. If that reproduction fails, this
spec closes fail-closed; it does not proceed
on a distribution it cannot re-derive. The
freeze may instead direct a different pin —
openly, in the freeze record — but it may not
leave the phrase "the recorded distribution"
pointing at a file that does not contain one.

## 3. Step 0 — gates before any precision quantity (fail-closed)

Execution runs these checks in order, before
any resampling-at-scale, interval, or target
quantity is computed. A failure stops the
execution in the class named; nothing is
repaired at run time.

- **0.1 Composite pin integrity.** Every §2
  input hashes to its freeze-record value,
  including the resampling-distribution pin's
  summary component (`phase393_results.json`).
  A mismatch stops the run as **INVALID**.
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
  mismatch stops the run as **INVALID** — the
  precision computation does not proceed on a
  distribution that does not reproduce its own
  record (this is the fail-closed consequence
  of DEF-061-1).
- **0.4 Search frame present.** The freeze
  record states, in full: the multiplier grid,
  the search ceiling, the per-grid-point trial
  count, the draws and permutations per trial,
  the simulation seed, and the
  effect-imposition construction (§4.3,
  OP-061-1…OP-061-5 in `adjudication.md`). Any
  element absent stops the run as **CANNOT BE
  RUN AS WRITTEN** before any trial: those
  values change the target, so supplying them
  at run time would be exactly the assumption
  the doctrine makes a tripwire, not
  discretion.

## 4. The precision computation

Computation-first: this spec's whole product
is the output of the rule stated here, applied
to the distribution pinned at §3. No other
quantity is computed, and no verdict about
Arm A's bounded claim is taken.

### 4.1 Base quantities (all from the record)

- Margin: adjusted R² **0.01** (the frozen
  family's single margin; not re-derived).
- Arm A site totals of record: Mohenjo-daro
  1,302; Dholavira 111; Lothal 74;
  Chanhu-daro 54; Kalibangan 52 — total 1,593.
- Recorded point estimate:
  θ̂ = 0.00878393455594817.

### 4.2 The two stated scenarios (design-fixed)

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

### 4.3 Trial construction (the design's method, stated mechanically)

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
   effect the scenario's θ (OP-061-5; the
   draft names the candidate constructions in
   `adjudication.md` and does not choose
   between them, because the choice changes
   the target);
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
program holds (claim F061-C13).

### 4.4 The resolution rule (mechanical)

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

### 4.5 The target rule (mechanical)

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
  totals** of §4.1 (the design's "multiples of
  their current sizes"; DD-061-3), with the
  integer rounding the freeze fixes
  (OP-061-1) and the per-site integers as
  computed, summing exactly to the total;
- the qualifying share at that point, and the
  full grid table (every grid point's share,
  both scenarios) so that non-monotonic
  behaviour — a qualifying point followed by a
  non-qualifying one — is visible in the
  record rather than smoothed away. The target
  is the smallest qualifying total whether or
  not the shares are monotone; the table, not
  an assumption, is what shows the pattern.

If no grid point inside the frozen ceiling
qualifies for a scenario, that scenario
returns **NO TARGET (within the frozen search
frame)**. The two scenarios' results combine
into exactly one headline under §5.

### 4.6 What is not computed

No LOSO variant of the target, no per-site
target optimisation (reallocating additions
to the smallest sites is a different design
and is not smuggled in as a sensitivity), no
S-complete variant, no Arm B quantity, and no
re-adjudication of Arm A. The pooled and LOSO
record stands exactly as Phase-393 left it.

## 5. Outcomes (the full set, wordings pre-written)

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

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run:

- BOTH: "From Phase-393's recorded resampling
  distribution, the precision computation
  returns an intake target for Spec 028 Arm A
  under both stated scenarios. If the true
  effect is at the current point estimate
  (0.00878, below the margin), [T₁] added
  non-Harappa inscriptions (multiple [m₁];
  per-site [distribution₁]) make the interval
  resolve downward at the 0.01 margin in at
  least 80% of trials. If the true effect is
  0.015, [T₂] added inscriptions (multiple
  [m₂]; per-site [distribution₂]) make it
  resolve upward. The intake target that
  resolves Arm A under either scenario is the
  larger, [max(T₁,T₂)] (DD-061-5). This is a
  measurement of the test's resolution on
  recorded data. It is not evidence about the
  ancient world, and it does not change Arm
  A's INCONCLUSIVE verdict."
- SCENARIO 1 ONLY: "…returns an intake target
  under Scenario 1 only: [T₁] added
  non-Harappa inscriptions (multiple [m₁];
  per-site [distribution₁]) resolve Arm A
  downward at the 0.01 margin if the true
  effect is at the current point estimate
  (0.00878). Under Scenario 2 (true effect
  0.015), no grid point inside the frozen
  search frame ([ceiling]) qualified, so no
  upward target is returned. [Resolution /
  ancient-world sentences as in BOTH.]"
- SCENARIO 2 ONLY: the mirror form, with
  Scenario 2's target stated and Scenario 1's
  no-target stated with the frame named.
- NEITHER (the falsifier's outcome): "From
  Phase-393's recorded resampling distribution,
  the precision computation returns **no
  intake target that resolves Arm A at the
  0.01 margin under either stated scenario**,
  within the frozen search frame (grid
  [grid]; ceiling [ceiling]; [trials] trials
  per point). The grid table is published
  with this record so the near misses are
  visible. Spec 028 Arm A stands INCONCLUSIVE
  with no computed intake target; the
  contingent rerun (Arm A2) has no target to
  arm on, and its trigger (§6 of the
  adjudication) does not fire on this
  record."
- INVALID (gate 0.1, 0.2, or 0.3): "The
  precision computation did not run: [gate]
  failed ([observed values]). No target
  quantity was computed. Spec 028 Arm A
  stands exactly as recorded."
- CANNOT BE RUN AS WRITTEN (gate 0.4): "The
  precision computation did not run: the
  freeze record does not state [missing
  search-frame element(s)], and those values
  may not be supplied at run time. No target
  quantity was computed."

## 6. Reporting obligations

Every product of an execution carries, in its
headline paragraph or first table:

1. the statement that the computation is a
   **simulation over recorded data** —
   Phase-393's recorded resampling
   distribution and the recorded site samples
   — and that its added inscriptions are
   resamples, not held data;
2. both scenario values (θ₁ = 0.00878 as
   recorded; θ₂ = 0.015) and the 0.01 margin;
3. the full grid table of §4.5 (every grid
   point, both scenarios, the resolution
   shares), the frozen search frame in full
   (grid, ceiling, trials, draws, seed,
   effect-imposition construction), and, for
   each returned target, its total, multiple,
   and per-site integer distribution;
4. the headline word of §5 and, where a target
   is returned, the DD-061-5 operative target
   with its scenario condition named;
5. the fence sentence: "This computation
   measures the resolution of a recorded test.
   It establishes nothing about the ancient
   world."

Deliverables at execution: a results JSON
(the §2 pins as asserted, the gate verdicts,
the full grid table, per-scenario targets or
no-target records, the trial intervals or
their recorded summaries under the frozen
frame), a report under these headline rules,
the experiment-graph node (H15/H23, registered
and verified before the run), the outcome
append in this directory, and the LEDGER entry
(H1). Foundation check (H21) after the
execution phase: 0 failures, or the outcome
record says why not. Anchors asserted
byte-identical before and after.

## 7. Epistemic limits (binding on all outputs)

1. **No ancient-world conclusion.** The design
   is explicit and this spec repeats it as a
   fence: A1 measures the program's own
   resolution. No output may present a target
   as evidence for or against site-linked
   repertoire structure, movement of people,
   or any sign meaning.
2. **The frozen verdict stands.** Spec 028
   Arm A's INCONCLUSIVE verdict is not edited,
   superseded, or re-adjudicated by anything
   this spec computes. A returned target
   appends to the claim `STUDY-SPEC-028/ARM-A`
   as a dated precision record beside it.
3. **A target is not a promise.** A target
   says: *if* real new data of the same kind
   arrives in that amount, *and* the true
   effect is the scenario's θ, the interval
   resolves in at least 80% of trials like
   these. Real data may differ in kind,
   composition, and provenance from resampled
   recorded data; the rerun's actual verdict
   belongs to the rerun alone (Arm A2, not in
   this pass).
4. **"No target" is frame-scoped.** It is a
   statement about the frozen grid and
   ceiling, never about all possible data.
5. Negative, no-target, invalid, and
   cannot-be-run outcomes publish with the
   same prominence as a returned target.

## 8. Risks and honest weaknesses

- **The recorded distribution is a summary,
  not a file of draws** (DEF-061-1). Gate 0.3's
  exact-reproduction standard is this draft's
  answer; if the frozen machinery cannot
  reproduce its own summary on the pinned
  inputs, this computation honestly does not
  run.
- **Resampled data is tidier than real data.**
  Additions simulated from the recorded sites
  inherit those sites' compositions and the
  surviving record's biases. A target computed
  this way is a planning number under stated
  scenarios, not a guarantee about future
  intake — §7.3 binds every output to say so.
- **The small sites dominate the arithmetic.**
  Four of the five Arm A sites carry 291 of
  the 1,593 records between them; proportional
  scaling (DD-061-3) directs most simulated
  additions to Mohenjo-daro because that is
  what "multiples of current sizes" means.
  Whether a smallest-sites-first allocation
  would be a better intake policy is a real
  question — for a different design, recorded
  here so it is not mistaken for this one's
  answer.
- **Five sites is few, and the interval is
  wide for structural reasons** (interval
  width 0.00835 on the recorded primary). The
  computation may honestly return no target
  inside any reasonable ceiling; §5 pre-writes
  that outcome so it cannot be softened.

## 9. Stop conditions and outcome classes

Execution ends in exactly one of:

- **TARGET UNDER BOTH SCENARIOS**,
  **TARGET UNDER SCENARIO 1 ONLY**, or
  **TARGET UNDER SCENARIO 2 ONLY** — per §4–§5,
  after all gates pass.
- **NO TARGET UNDER EITHER SCENARIO** — the
  falsifier's outcome, after all gates pass.
- **INVALID** — a §2 pin mismatches (0.1); the
  population does not reproduce (0.2); or the
  recorded distribution does not reproduce
  (0.3).
- **CANNOT BE RUN AS WRITTEN** — the frozen
  search frame is incomplete (0.4).

## 10. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — composite pin, population
   reproduction, recorded-distribution
   reproduction, search-frame assertion.
3. **Computation** (§4) — both scenarios,
   ascending grid, full grid table recorded.
4. **Outcome** (§6) — appended records only;
   anchors asserted byte-identical;
   foundation check reported as measured.
   No Arm A2 step exists in this shape.

## 11. What this spec is not

Not a rerun of Arm A (that is Arm A2,
contingent and outside this pass), not a new
corpus, not a verdict on `STUDY-SPEC-028/ARM-A`,
not an intake act, and not an authorisation to
execute. It is a precision computation on a
recorded distribution, designed so that its
honest outcomes — including returning no
target at all — are written down before any
trial is run.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
