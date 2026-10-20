# Spec 040 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-20
>
> This spec has two adjudication inputs, recorded
> here so the draft's basis is inspectable:
>
> 1. **The owner's bundle decision of
>    2026-10-20**: the gazetteer
>    period-assignment act and D-25 are
>    authorised as a bundle, sequenced by the
>    agent at the right time — the act first,
>    D-25 after it. The act is being drafted as
>    Spec 039; this spec is D-25's draft.
> 2. **The owner's evidence-standard decision
>    of 2026-10-20**: the gazetteer act uses
>    **published period determinations only**
>    (Option 1 of the decision memo of the same
>    date). Program-derived dates-to-period
>    assignments are excluded.
>
> These inputs commission this **draft** and
> fix its dependency and evidence standard.
> They are not a freeze order and not an
> execution order for Spec 040: both remain
> separate owner decisions, and the freeze is
> additionally barred by the dependency gate
> (spec §1) until Spec 039 has executed.

## 1. The adopted basis (operative substance)

- **The design.** D-25 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
  §D-25): the chronology-controlled rerun of
  Spec 025's G1, period added as one
  stratification to the Phase-140 controlled
  permutation test, same statistic, same 9,999
  shuffles, same effect estimator as the
  Phase-385 rerun, judged against the family's
  0.10 margin.
- **The claim.** `STUDY-SPEC-025/G1`:
  SUPPORTED under composition and preservation
  control (Phase-140: χ² 4966.362228365138,
  0 of 9,999 permutations ≥ observed,
  p = 0.0001, V = 0.2190), margin-completed by
  Phase-385 (governing basic CI
  [0.1838, 0.2102] above the V = 0.10 floor),
  carrying the rider in every statement:
  **chronology is not controlled**.
- **The population.** The Phase-137 F3
  population on the ICIT-lineage layer
  (horus84, SHA-256 `c368f290…`): 5,410
  inscriptions at 7 eligible sites; profile
  configuration as frozen for Phase-140.
- **The spine.** The 205-row extended
  chronology spine of Spec 030 / Phase-394
  (`data/movement/chronology_rows_phase394.jsonl`,
  SHA-256 `9dc2fba5…`): traced dated-context
  assertions by site. Spec 030's re-test on it
  closed Q6 NOT-YET-TESTABLE (C1 1 FAIL,
  C2 6 FAIL, C3 0.0 FAIL, C4 median σ 70 PASS).
  The spine supports and cross-checks
  site-period assertions; it does not label
  inscriptions.
- **The dependency.** Spec 039 (the gazetteer
  act) executes first and produces the frozen
  period-assignment artifact at site-period
  resolution, under published determinations
  only. Until it has executed, Spec 040's
  freeze is barred (spec §1).

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-20:

- **Design D-25** — read in full on the PR #195
  branch: the question, hypothesis, falsifier,
  data, method, criteria fixed in advance
  (including the too-thin closure: fewer than
  3 period strata retaining at least 5 sites
  each, or more than 40% of rows unassignable),
  the contested-row posture (excluded from
  stratum assignment in the primary, included
  in a stated sensitivity), the
  leave-one-site-out and named drop-Harappa
  sensitivities, and the limits (no mechanism,
  no movement).
- **Spec 025 record** — read on `main` (head
  `5e7f3cdb`): spec.md (G1's design, the §3
  covariate evidence — period informative on
  41.9% of the F3 population, structural
  missingness by site, site-local period
  vocabularies), phase139-freeze.md and
  phase140-freeze.md (final strata =
  composition × preservation; chronology
  routed to the EXPLORATORY S-chron panel;
  the mandatory rider; the composition-only
  regression requirement).
- **Phase-140 results** — read on `main`:
  population 5,410 / 7 sites; observed χ²
  4966.362228365138; 0 of 9,999; p = 0.0001;
  V = 0.2190084751289231; covariates file
  SHA-256 `a0f0d05a…` (recomputed at this
  draft from `main`: equal).
- **Phase-385 record** — read on `main`:
  report, v2 contract, and results. The v1
  percentile interval [0.2282, 0.2537] excluded
  the point estimate and was superseded; v2's
  governing basic interval is
  [0.1837750116366994, 0.2102434435947284],
  B = 4,999, seed 20261012, margin V = 0.10,
  computed by stratified bootstrap within the
  frozen G1 strata. The recorded S-chron
  exploratory basic interval is
  [0.18480004041254045, 0.20984224851507333].
- **Spec 030 record** — read on `main`: the
  spine extension to 205 rows, the §4 re-test
  values, the contested two-computation
  posture, and the express reservation of
  Ask 2 (whether the contested-excluded
  computation binds a future Q6 freeze) — a
  reservation this spec does not touch: it
  governs Q6 timing scenarios, not G1 period
  strata; Spec 040's own contested posture is
  fixed by D-25 and stated in spec §4.4.
- **Spec 027 §6.2** — read on `main`: the
  gazetteer unit (one source assertion about a
  site), the `program_period_assignment` field
  (nullable; mapping rule and reviewer recorded
  when present), and §6.5's rule that competing
  assertions are preserved, never deleted.
- **Gazetteer state** — the published Stage 0
  gazetteer (36 rows / 30 sites) carries an
  empty `program_period_assignment` on every
  row and a published period label on only 3
  rows (Central Asian "PN"/"Neo." entries):
  the dependency of spec §1 as found.
- **Design-source tension, recorded** — D-25's
  feasibility line states the gazetteer's
  period labels as an existing asset. They did
  not exist when the design was written and do
  not exist yet. The owner's bundle decision
  (Spec 039 first) is the act that makes them
  exist; this draft records the tension rather
  than harmonising it (spec §2.4).
- **Phase-number state** — Phase-400 is Spec
  036's; Phase-401 is claimed by the Spec 037
  draft (PR #225) and provisionally by the
  Spec 038 draft. Spec 040 allocates no phase
  number at draft (DD-040-10).
- **Not done at draft, by design** — no period
  label was read into the layer, no assignment
  join was built, no margins were computed,
  the spine was not recomputed, and no
  repertoire quantity was calculated. Every
  quantity in this spec beyond the cited
  records is a quantity the gated execution
  will produce, not one this draft has seen.

## 3. What the freeze decision is asked to decide

The freeze is barred until spec §1's
dependency gate is satisfied on the merged
record. When it is reached, the freeze decides:

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with the
   Spec 039 artifact's path, version, and
   SHA-256 named into the freeze record — or
   decline, leaving G1 with its rider as the
   program's final word.
2. **DD-040-1 (proposal): the decision rule is
   re-derived, not carried.** Spec 025 assigned
   G1's verdict from its permutation p alone
   (p ≤ 0.05, BH over G1 alone). D-25 and the
   Phase-385 margin completion supersede that
   for this rerun: the governing basic interval
   against the V = 0.10 margin assigns the
   outcome (§6.4); the permutation p is
   computed and reported but cannot rescue an
   interval that fails the margin, and no
   p-value threshold is a second gate. This is
   a change from Spec 025's stated rule,
   recorded here as a decision for the freeze,
   never applied silently.
3. **DD-040-5 (proposal): the thinness
   closure's word.** D-25 names its too-thin
   closure INCONCLUSIVE-BY-DESIGN. This spec
   governs the same closure as
   **NOT-YET-TESTABLE** (spec §5), the
   program's established word for a test the
   data cannot yet support (Specs 027/030), on
   the ground that no estimand is computed past
   the gate. The freeze confirms the word or
   restores the design's, openly.
4. **DD-040-6 (proposal): the third margins
   arm.** D-25 fixes two arms (≥ 5 sites in
   each period stratum; ≤ 40% unassigned).
   This draft adds a third: ≥ 1,000 permutable
   inscriptions under the combined strata,
   carried from Spec 025's covariate-gate floor
   (§4.2 step 3 of that spec), so a fragmented
   design whose strata are nearly all
   single-site cannot proceed on a technicality.
   The freeze confirms or strikes the arm
   before any margin is computed.
5. **DD-040-9 (proposal): whether the frozen
   spec files its own OSF registration** —
   proposal: yes, following the Spec 027/030
   study-design pattern, so the assignment
   interface, gates, and decision rules are
   timestamped outside the repo before
   execution. Nothing is filed at draft.

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

- **DD-040-2 — Period enters by
  stratification.** The design's method is
  explicit (shuffling inside groups matched
  for composition, preservation, and period);
  no covariate or matching-score form is
  offered.
- **DD-040-3 — The assignment interface is
  site-period resolution.** A mapping keyed by
  site × the inscription's recorded local
  chronological label, producing one coarse
  label or `UNASSIGNED`. Site-level labels
  alone cannot place inscriptions at sites
  occupied across periods, and the spine's
  dates never place an inscription (spec
  §4.3). If Spec 039's executed product cannot
  support this interface, §1's gate fails and
  the honest state is NOT-YET-TESTABLE — the
  interface is not loosened to fit the product.
- **DD-040-4 — Sign columns are fixed from
  the full base population.** Re-deriving them
  on the assigned subset would change the
  estimand with the assignment rate; the
  Phase-137/140 column set governs (spec §6.1).
- **DD-040-7 — The below-margin range is two
  outcomes, not one.** D-25's "straddles or
  falls below the margin" is resolved into
  WEAKENED (interval straddles 0.10) and
  CONTRADICTED AT THE DECLARED MARGIN
  (interval entirely at or below 0.10),
  because the claim consequences differ: a
  period-confounded association in the first
  case, a defeated chronology-controlled claim
  in the second (spec §6.4).
- **DD-040-8 — Contested sensitivity labels
  come only from Spec 039's freeze.** Where a
  contested mapping has no unique frozen
  sensitivity label, the sensitivity is NOT
  ESTIMABLE for it; execution chooses nothing
  (spec §4.4).
- **DD-040-10 — No execution phase number at
  draft.** Allocated at the freeze act, after
  the Spec 037 / Spec 038 claims on Phase-401
  are settled on the merged record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
