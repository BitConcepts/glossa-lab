# Spec 061 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign plan,
>    approved by the owner AS WRITTEN on
>    2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`).
>    Spec 061 is Part 2, **member 18**: design
>    D-27, arm A1. Campaign decisions that bind
>    this draft: **E-3** (trigger-armed arms do
>    not auto-join — arm A2 is not a member of
>    this pass; §6 below), **E-5** (a step-0
>    failure closes this experiment, never the
>    pass), and Part 7's tripwire that any
>    assumption which would change a test's
>    outcome is never discretion (the ground
>    for gate 0.4 and §5's OPEN items).
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-27 found **RIPE (arm A1)** — the
>    precision computation runs today on
>    Phase-393's recorded resampling
>    distribution and produces a concrete
>    intake target under two stated scenarios;
>    arm A2 stays trigger-armed.
> 3. **Design D-27, arm A1** (PR #195 packet,
>    `04-study-headlines.md` §D-27), read in
>    full at this draft. The design governs
>    substance: the method (resampling the
>    recorded site samples with replacement at
>    multiples of their current sizes), the
>    criterion (the resampled interval excludes
>    the 0.01 margin in at least 80% of trials),
>    both scenario values (0.00878 and 0.015),
>    the product (smallest total added count
>    and its per-site distribution), and the
>    limit (A1 establishes nothing about the
>    ancient world).
>
> These inputs commission this **draft**. They
> are not a freeze order and not an execution
> order for Spec 061: both remain separate
> later acts under the campaign's waves.

## 1. The adopted basis (operative substance)

- **The member.** D-27 arm A1 only — "Spec 028
  Arm A — the precision design (residue),"
  campaign member 18. Arm A2 is excluded by
  the tasking and by E-3 (§6).
- **The claim.** `STUDY-SPEC-028/ARM-A`:
  INCONCLUSIVE — median adjusted R²
  0.00878393455594817, interval
  [0.004626892186724407, 0.01297407559730989]
  straddling the 0.01 margin, rejection share
  0.6231155778894473, every LOSO median below
  the margin, controls passing.
- **The falsifier** (campaign wording,
  governing): the computation returns no
  intake target that resolves Arm A at the
  0.01 margin under either stated scenario.
  Pre-written as the NO TARGET headline in
  spec §5.
- **The computation.** A simulation over
  recorded data, not a test of the ancient
  world: scale the recorded Arm A site samples
  by multiples, impose each scenario's θ in
  turn, and find the smallest added total at
  which the interval excludes the margin in
  ≥ 80% of trials (spec §4).

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
against `main` at
`83b6a563402b02809ab1143848e4dd2c0cfd9de3`,
**via the GitHub API only** (this draft never
touched a local checkout of the repository):

- **Design D-27** — read in full: question,
  Arm A1 method and criteria (multiples,
  80% of trials, both scenarios, smallest
  total + per-site distribution), Arm A2's
  blocked status and trigger, and the
  "nothing about the ancient world" limit.
- **Campaign plan** — Parts 1–4 read: member
  18's row and falsifier, the contingent-
  members paragraph (A2's trigger is new data
  reaching the target A1 computes, through
  Phase-130 intake), E-3, E-5, and the Part 7
  outcome-changing-assumption tripwire.
- **Phase-393 Arm A record** — read from
  `reports/phase393_results.json`: primary
  quantities as in §1, site records 1,593,
  inscriptions per draw 294, provenance seed
  20261012, draws 199, permutations per draw
  499, freeze digest of the Phase-393 run
  `619ab0c3…`.
- **Spec 028's frozen Arm A design** — read in
  `specs/028-harappa-robustness/spec.md`:
  population (analysis 3,030 minus Harappa's
  1,437 = 1,593 at 5 sites), draw (cell
  rarefaction to 49; included cells
  Mohenjo-daro SEAL/TAB, Dholavira SEAL,
  Lothal SEAL, Chanhu-daro SEAL, Kalibangan
  SEAL; excluded TAB cells 15/2/2/3), verdict
  family, margin 0.01, seed, and the OSF
  registration of the frozen contract
  (osf.io/7m35w) that arm A2 would rerun.
- **Margins audit** — read: Arm A site totals
  and cells as in spec §4.1.
- **Input pins** — recomputed at this draft
  and stated in spec §2: results
  `0a1657a8…`, corpus layer `c02e3d7b…`,
  pipeline393.py `6c2ff91c…`, margins audit
  `15ae0281…`, Spec 028 freeze.json
  `376cd8e7…`, anchors `df0cf620…` (matching
  Spec 042's draft pin, re-verified here, not
  inherited on trust).
- **Not done at draft, by design** — no trial
  was run, no interval at scale was computed,
  no target was estimated or peeked at, no
  code was written or run, the AEE hooks have
  not run, and nothing was filed with OSF.

## 3. Defects found at draft

- **DEF-061-1 — The "recorded resampling
  distribution" is not a file.** Neither the
  design's phrase nor the triage's ("computing,
  from Phase-393's recorded resampling
  distribution…") matches the repository:
  `phase393_results.json` contains summaries
  only; the per-draw `adj_draws` the pipeline
  computes were never persisted. **Disposition
  at draft:** the pin is made composite and
  gate 0.3 requires exact reproduction of the
  recorded summary from the pinned inputs
  before anything is scaled (DD-061-1,
  claims F061-C06/C07, spec §§2.1, 3). If the
  freeze prefers a different remedy (e.g.
  directing a per-draw regeneration record to
  be created and pinned as its own act), it
  records that openly; what it may not do is
  freeze the phrase unexamined. This defect
  is in the design's input description, not
  in Phase-393's execution, whose summaries
  were always its stated product.
- **DEF-061-2 — The design fixes no search
  frame.** Grid, ceiling, trials per point,
  simulation seed, and the construction that
  imposes a scenario θ on resampled recorded
  samples are all unspecified in D-27, and
  each changes the returned target — under
  the campaign's Part 7 rule, none may be
  supplied by the executor. **Disposition:**
  recorded as OPEN items OP-061-1…OP-061-5
  (§5) that the freeze must decide; gate 0.4
  closes the run as CANNOT BE RUN AS WRITTEN
  if any is still missing at execution. The
  draft does not treat this as a drafting
  failure: the design's computation rule
  (§4.4–§4.5) is stated mechanically and
  completely conditional on the frame, and
  inventing frame values at draft would have
  been exactly the improvisation the
  campaign forbids.

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-061-1 — The distribution pin is
  composite, with exact reproduction as its
  gate.** Summary file + corpus + pipeline +
  margins audit + Spec 028 freeze record are
  all pinned (spec §2), and gate 0.3 requires
  the frozen primary to reproduce the recorded
  summary exactly. Ground: DEF-061-1.
- **DD-061-2 — Resolution means strict
  exclusion.** A trial resolves iff its
  interval's bound is strictly beyond 0.01 in
  the scenario's direction; a touching bound
  does not resolve. The design's word is
  "exclude"; the frozen family's "entirely at
  or below" wording (a CONTRADICTED clause,
  written for a different question) is not
  imported. Claim F061-C10.
- **DD-061-3 — Per-site distribution is
  proportional to recorded site totals.** The
  design scales "at multiples of their
  current sizes" and asks for the target's
  "per-site distribution"; the distribution
  of a multiple-scaled total is the recorded
  totals' proportions. Equal-per-site and
  smallest-sites-first allocations are
  different designs. Claim F061-C11.
- **DD-061-4 — Scenario 1 computes at the
  recorded full-precision estimate.**
  θ₁ = 0.00878393455594817; the design's
  0.00878 is that value as stated in prose.
  Claim F061-C09.
- **DD-061-5 — The operative (trigger) target
  is the larger returned target; a single
  returned target is operative with its
  scenario condition.** Ground: the trigger
  A2 arms on is "the target A1 computes"
  (campaign, contingent members); where A1
  computes two, the one that resolves Arm A
  under either scenario is the larger. Where
  neither is returned, no operative target
  exists and the trigger cannot fire on this
  record. Claim F061-C14; §6 below.
- **DD-061-6 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today (the
  Spec 038/042 convention).
- **DD-061-7 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.

## 5. OPEN for the freeze (each blocks the freeze until decided and recorded)

- **OP-061-1 — The multiplier grid and
  integer rounding.** Which multiples are
  searched (range and step), and how a
  multiple's per-site shares are rounded to
  integers summing exactly to the total.
  Changes the target directly.
- **OP-061-2 — The search ceiling.** The
  largest multiple (or largest total) the
  computation may examine. Without a ceiling,
  "no target" — the falsifier's outcome — is
  not decidable; with one, it is always
  frame-scoped (spec §7.4).
- **OP-061-3 — Trials per grid point, and
  draws/permutations per trial.** Proposal
  recorded, not decided: trials sufficient
  that the 80% share's own sampling error is
  reported beside it, with draws/permutations
  inherited from the frozen design (199/499)
  unless the freeze directs otherwise.
- **OP-061-4 — The simulation seed.** A fresh
  seed fixed in the freeze record (the
  Phase-393 seed 20261012 belongs to the
  recorded run and to gate 0.3's reproduction;
  reusing it for the scaling simulation would
  entangle the two).
- **OP-061-5 — The effect-imposition
  construction.** How a resampled world is
  made to have true effect exactly θ₁ or θ₂.
  Candidate constructions the freeze chooses
  among (the draft takes no position, because
  the choice changes the target): (a) shift
  the recorded per-site compositions along
  the recorded site-difference direction,
  rescaled until the constructed world's
  adjusted-R² effect equals θ, verified by
  the frozen estimator on the constructed
  population; (b) generate each site's
  composition as the pooled composition
  perturbed toward site-specific components
  in the frozen positive-control manner,
  calibrated until the effect equals θ;
  (c) an analytic width-scaling computation
  with no imposed world — recorded here
  because a freeze might argue the design's
  "interval width scales" sentence means it,
  and rejected at draft as the primary
  reading because the design's operative
  criterion is stated over *trials* of a
  resampled interval, which (c) does not
  produce.
- **OP-061-6 — Whether the frozen spec files
  its own OSF registration.** Proposal: yes,
  under campaign decision E-1 (every
  specification in the pass registers its own
  OSF contract at its freeze). Arm A2 needs
  none — its test is already registered
  (osf.io/7m35w) — but A1's contract is new.
  Nothing is filed at draft.
- **OP-061-7 — Whether execution requires a
  fresh synthetic calibration** of the
  scaling simulation (e.g. recovering a planted
  θ at the recorded scale, m = 1, before any
  larger multiple is examined). The draft's
  gate 0.3 already forces exact reproduction
  at the recorded scale; whether that suffices
  for the imposed worlds of OP-061-5 is the
  freeze's decision.

The freeze also confirms or openly overturns
DD-061-2, DD-061-3, and DD-061-5.

## 6. The contingent member: arm A2 (not in this pass — E-3)

**Status.** Arm A2 — the decisive rerun of
the already-frozen, already-registered Arm A
test (OSF osf.io/7m35w; no new design needed)
— is **not** a member of the runnable-
experiments campaign, is not part of Spec
061, and is not designed, authorised, or
executed here. Spec 061 contains no A2 task,
no A2 gate, and no A2 execution step, by
design.

**Trigger definition (exact, as this draft
records it).** A2's trigger fires when **new
multi-site inscription data, verified through
Phase-130 intake, brings the cumulative added
non-Harappa inscription count to at least the
operative target T\***, where:

- T\* is the target Spec 061's computation
  returns, under DD-061-5: the larger of the
  two scenario targets if both are returned;
  the single returned target (with its
  scenario condition recorded beside it) if
  only one is returned; **undefined — the
  trigger cannot fire on Spec 061's record —
  if NO TARGET is returned**;
- "added" is counted against the recorded
  Arm A base of this computation (1,593
  records at the five Arm A sites; per-site
  conformance against the target's returned
  per-site distribution is judged at the
  mini planning gate the trigger queues, not
  assumed from the total alone);
- only genuinely new data counts — never
  Spec 061's simulated resamples (claim
  F061-C13) — with lineage stated for the
  intake as a whole and material outside the
  ICIT lineage preferred, as design D-27
  states for A2 (the same missing input as
  D-24). The weekly data watch already tests
  for this event class.

**Consequence of a fired trigger (E-3).** The
arm does **not** join this pass and does not
execute. It queues for its own mini planning
gate, at which the owner decides afresh. If
Spec 061 returns no target, A2 remains armed
only in the design's general sense (new data
would still be welcome to the program) but
has no computed target to arm on, and no
later act may quote one from this record.

## 7. Acceptance tests derived twice, independently — disagreements and resolutions

Per the campaign doctrine, each claim's
acceptance test was derived twice: once from
the claim text as written (**derivation A**),
and once independently from the underlying
requirement alone — the design sentence, the
campaign row, or the frozen record the claim
rests on (**derivation B**) — without
consulting A's wording. Where the two
derivations agreed, the claim's
`falsification_tests` carry the agreed test.
Disagreements, and their resolutions:

| Claim | Disagreement between the derivations | Resolution in this draft |
|---|---|---|
| F061-C06/C07 | A pinned the results file alone (it is the named input); B required the machinery and inputs too, because a summary cannot be resampled. | B adopted — composite pin + reproduction gate (DD-061-1). This disagreement is what surfaced DEF-061-1. |
| F061-C10 | A imported the frozen family's "interval entirely at or below 0.01" as the downward-resolution test; B used the design's word "exclude," which a touching bound fails. | B adopted — strict exclusion (DD-061-2); the family's wording governs verdicts on real runs, not this design's resolution criterion. Freeze may overturn openly (§5). |
| F061-C11 | A allocated the added total equally across the five sites (a target is "per site"); B allocated in proportion to current sizes ("multiples of their current sizes"). | B adopted (DD-061-3); the equal-allocation reading is recorded as a refused alternative in the claim. |
| F061-C09 | A computed Scenario 1 at the design's printed 0.00878; B at the record's full-precision 0.00878393455594817. | B adopted (DD-061-4): the record governs its own point estimate; the printed value is its rounding. |
| F061-C14 | A defined the trigger on "the target" as if A1 returned exactly one; B noted A1 can return zero, one, or two targets and the trigger is undefined in two of those cases. | B adopted — DD-061-5 defines T\* for all three cases, including cannot-fire. |
| F061-C03/C12 | A treated the search frame (grid, ceiling, trials, seed, construction) as drafting detail the spec should simply state; B derived from the campaign's Part 7 tripwire that unstated frame values are outcome-changing assumptions no one in the pass may supply. | B adopted — the frame is OPEN for the freeze (OP-061-1…OP-061-5) with gate 0.4 fail-closed. **This is the draft's largest open item**; the computation rule itself (F061-C10/C11) is fully stated conditional on the frame. |
| F061-C03 (OP-061-5) | On the effect-imposition construction the two derivations did not merely disagree — they produced different mechanisms (composition-shifting vs planted-perturbation), and a third reading (analytic width-scaling) besides. No resolution was reachable from the design text alone. | **Unresolved at draft, by record.** Candidate constructions are named in OP-061-5 with the draft's reasoning on (c); the freeze chooses. The draft does not pick one silently, because the choice changes the target. |

All other claims (C01, C02, C04, C05, C08,
C13, C15): the two derivations agreed on the
operative check (inspection against the
stated boundary, an exact gate, or mechanical
recomputation from the published record), and
no disagreement is recorded because none
arose.

## 8. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   §2 pin re-asserted against the merged
   record — or decline, leaving
   `STUDY-SPEC-028/ARM-A` INCONCLUSIVE with
   no computed intake target and A2 unarmed
   on any number.
2. Decide OP-061-1…OP-061-5 (the search
   frame and the effect-imposition
   construction) and OP-061-6 (OSF) and
   OP-061-7 (calibration), and confirm or
   openly overturn DD-061-2, DD-061-3, and
   DD-061-5.
3. Note DEF-061-1 and the composite-pin
   remedy in DD-061-1, or direct a different
   remedy in the freeze record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
