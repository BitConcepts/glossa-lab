# Spec 028 — Harappa Robustness: Is the Repertoire Site Effect Independent of Its Largest Site?

> ## FROZEN UNDER DELEGATED ADJUDICATION — 2026-10-11
>
> Owner order (Tristen Pierson, 2026-10-11, verbatim): "Also
> do the Harappa robustness design follow up and execute it
> based on what you think the best way forward is." The
> adjudication record is `adjudication.md`: the design
> judgment is delegated to the program, execution is
> authorised on the frozen design, and there is no separate
> owner adjudication round for this spec. The freeze record
> is `freeze.md`; the machine freeze record is `freeze.json`.

## 1. Why this spec exists

Spec 027 Stage 1 (Phase-392) froze and executed the Q2
repertoire gate: under M77, after rarefaction to a common
cell size and stratification by object type, does site
explain more recorded sign-repertoire variation than
expected under permuted site labels, at the declared
practical margin (adjusted PERMANOVA R² = 0.01)?

Phase-392's verdict was **INCONCLUSIVE**, by its freeze's own
named case. The full-population result was unanimous:
median adjusted R² 0.01677, percentile interval
[0.01032, 0.02397] entirely above the margin, rejection
share 1.000, and both discriminating controls PASS. But the
SUPPORTED rule also required every leave-one-site-out (LOSO)
median to clear the margin, and dropping Harappa took the
median to **0.00928** — below 0.01 — while every other drop
held (0.01677–0.01863). The CONTRADICTED rule did not fire.
Phase-392's outcome record states the open question exactly:
detection is not in doubt at that design; what is not
established is the *practical, site-general* claim, because
margin-clearing is partially load-bearing on the corpus's
dominant site (Harappa: 1,437 of 3,030 analysis records,
47.4%).

This spec is the designed follow-up to that open question.
It does not rerun Phase-392 and it does not revise it. It
asks, under new frozen designs registered before execution:

- **Arm A:** does the bounded claim survive when Harappa is
  not in the population at all?
- **Arm B:** does the site effect survive when no site is
  allowed to count more than any other — i.e. is it an
  inscription-count artefact of the large corpora?
- **Arm C (exploratory):** within Harappa, what carries its
  contribution — which object types, which composition
  components?

## 2. Scope

### 2.1 In scope

- Two confirmatory arms (A: primary; B: secondary) under one
  freeze, one seed, and the program verdict taxonomy, plus
  one exploratory descriptive arm (C) that mints no verdict.
- The identical corpus substrate, corpus rules, sign list,
  and population definitions as the Phase-392 freeze
  (Spec 027 `stage1-freeze.md`), reproduced and asserted
  before any outcome is computed.
- A margins-only audit and a synthetic-only calibration as
  freeze inputs; an OSF registration of the frozen contract
  before execution; one execution (Phase-393); per-arm
  verdicts; a side-by-side statement with Phase-392; ledger
  entries.

### 2.2 Out of scope

- Any change to Phase-392's record, verdict, or frozen
  quantities. Any changed reading is a historical assessment
  under this spec, appended, never an edit to Spec 027.
- Any downstream repertoire-geography work. An Arm A or
  Arm B SUPPORTED verdict does not authorise it; Spec 027's
  closure rules are unaffected by this spec.
- Stage 2 of Spec 027 (Q7/Q6), the Parpola/CISI sensitivity
  (recorded NOT ESTIMABLE at the frozen crosswalk rule in
  Spec 027's Stage 1 freeze; not revisited here), pottery
  graffiti (never pooled; excluded from every population,
  as frozen), anchors, and PRED-2026 scoring.
- Any claim about dialects, languages, ethnic groups,
  political units, or workshops as peoples. Every claim in
  this spec is about *recorded repertoires in this corpus*.

## 3. Governing framework

### 3.1 Lifecycle

Specify → plan → tasks → margins audit → synthetic
calibration → freeze (this spec's `freeze.md`/`freeze.json`)
→ freeze PR merged on verified CI → OSF registration of the
frozen contract → H23 execution gate (script → graph module
→ registration → registration verification → run) → outcome
record → closeout verification. A changed gate is a new
version and a new freeze; a freeze is never regenerated over
a run.

### 3.2 Claim register

`claims.json` in this directory is the structured register
(IDs `F028-C…`). Every governed claim carries a stable ID,
one bounded proposition, an epistemic layer (`O`, `I`, `M`,
or `Interp.`), a boundary, assumptions and `depends_on`
links, `forbidden_assumptions` and a strongest rival in its
metadata, at least one falsification test, evidence records
with origin groups, and a verdict rule. The register must
pass the Spec 026 machinery
(`backend/glossa_lab/framework026.py`): no dependency
cycles, no missing dependencies, no forbidden-assumption
inheritance. Renamed-equivalent assumptions remain a human
review obligation; the mechanical check is exact-match after
whitespace normalisation.

### 3.3 Verdict taxonomy

Framework verdicts are exactly:

- **INVALID** — the run or instrument cannot discriminate
  the bounded claim (including a non-discriminating
  control, or a population that does not reproduce);
- **INCONCLUSIVE** — a valid design ran, but the evidence,
  interval, jackknife, or practical margin does not
  adjudicate the bounded claim;
- **CONTRADICTED** — a valid, discriminating test defeats
  the bounded claim under its frozen rule;
- **SUPPORTED** — a valid, discriminating test supports the
  bounded claim under its frozen rule and declared margin.

`NOT-YET-TESTABLE` and `NOT ESTIMABLE` are registration
statuses, not verdicts. Verdicts in this spec are **per
arm**: each arm's bounded claim receives its own verdict
under its own frozen rule. There is no Spec 028 headline
verdict and no pooled cross-arm verdict (§5.4).

### 3.4 Evidence origin groups

Evidence is counted by origin group, never by database
mirror or republication. The inscription layers used here
are ICIT-lineage and remain **one** origin group, as
established by Specs 024–026; the Spec 027 Stage 1 corpus
(the M77-keyed layer and the horus84 metadata join) is the
same origin group, not corroboration of itself. Phase-392's
published numbers are program records (governance evidence
for design), not independent empirical corroboration of any
Arm A/B result. Generated assertions, including this spec's
prose, are neutral governance evidence only.

## 4. Corpus (inherited, not re-decided)

The substrate, rules, and populations are those frozen in
Spec 027's `stage1-freeze.md` §§2–3, under the owner's
Spec 027 adjudication (M77 governs; Ask 3 rules as drafted):

- **Substrate:** `icit_converted_v2_keyed.json` (sha256
  `bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8`),
  the program's M77-keyed layer and named deduplication
  artifact; metadata join on `id` to horus84
  `inscriptions.csv` (sha256
  `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`)
  for completeness fields. Local store:
  `corpora/downloads/spec028_harappa/` (gitignored).
- **Token rules:** `sign_list_version` = M77 on every
  record; composition tokens = `direct` + `chain` mapped
  M-signs + `unmapped` pooled into the single UNMAPPED
  column; `placeholder` positions are not signs (damage
  flag only).
- **Eligibility:** legible-token count (direct + chain +
  unmapped) ≥ 2; provenanced records only (site present,
  not `Unknown`); object classes SEAL + TAB; pottery
  graffiti (`POT:T:g`) excluded from every population.
- **Sign columns:** the frozen 125 — M-signs with ≥ 10
  mapped tokens in the eligible population (123) +
  UNMAPPED + OTHER.
- **Populations (frozen margins, from `margins-audit.json`;
  execution must reproduce exactly):** eligible 3,144;
  analysis population (sites with ≥ 20 eligible
  inscriptions) 3,030 records at 6 sites — Harappa 1,437
  (SEAL 361 / TAB 1,076), Mohenjo-daro 1,302 (1,138 / 164),
  Dholavira 111 (96 / 15), Lothal 74 (72 / 2), Chanhu-daro
  54 (52 / 2), Kalibangan 52 (49 / 3). **Arm A population:**
  the analysis population minus Harappa — 1,593 records at
  5 sites. **Arm B population:** the full analysis
  population. **Arm C population:** Harappa's 1,437 analysis
  records.
- **No-peeking fence:** the margins audit computes no
  site-by-sign association, divergence, or permutation
  statistic; a test pins the absence of outcome fields.
  Phase-392's published LOSO medians are cited in §1 as
  motivation only; no new arm outcome was inspected before
  this freeze. (Arm A's median will be near Phase-392's
  published drop-Harappa LOSO value by construction — the
  machinery and population coincide — but Arm A's verdict
  turns on quantities Phase-392 never computed for this
  population: its rejection share, its own LOSO clause over
  five sites, and its controls on this population's shape,
  under a fresh seed.)

## 5. Design

### 5.0 Shared machinery and constants

Both confirmatory arms use the Phase-392 machinery as
amended by its Amendment 1: per-inscription M77 composition
(proportions over the frozen 125 columns), Bray–Curtis
distance, PERMANOVA with the standard adjusted R²
(null expectation ≈ 0), permutation of site labels **within
permutation strata** (B = 499 per draw, p = (1 + #{F_perm ≥
F_obs}) / (1 + B)), R = 199 draws, α = 0.05, practical
margin adjusted R² = **0.01**, seed **20261012** (fresh,
pre-declared here; one seed for all arms, controls,
jackknives, and sensitivities, so no later choice exists).
The permutation strata are **type class × legible-length
value** (the exact legible-token count) — a refinement of
Phase-392's type-only strata, recorded as Amendment 1 in
`freeze.md` with its calibration evidence (see also §6).
Two pre-freeze calibration findings forced Amendment 1:
first, the Phase-392 control construction (one synthetic
population rarefied 199 times) makes the negative control's
rejection share a lottery over the generation seed —
0.171/0.156 in this spec's first calibration attempts and
0.015/0.000 under a second seed — because one generated
population's small-cell noise recurs in every draw; the
Spec 028 controls therefore **regenerate the synthetic
population per draw**, which returned the shares to nominal
(0.050/0.035/0.070 across diagnostic variants). Second,
legible length is site-correlated within type class
(margins: mean 3.88–4.96 across included cells) and
sampling dispersion follows length, so the strata carry
the exact length value to keep labels exchangeable within
strata. Strata govern only which permutations are legal;
every effect-size quantity is computed exactly as in
Phase-392.
Per-draw summaries: median adjusted R², percentile interval
[2.5%, 97.5%], share of draws rejecting, median raw R² for
transparency (rules use the adjusted scale only).

**Discriminating controls (per arm; failure = that arm
INVALID):** each arm runs the identical arm pipeline on
synthetic populations templated on the arm's analysis
entries (same slots, same per-inscription legible lengths),
with the synthetic population **regenerated per draw**
(Amendment 1 — each draw is an independent null or planted
world):

- *Negative control:* tokens drawn from the arm's pooled
  composition (Arm A: pooled over the Arm A eligible
  population; Arm B: pooled over the full eligible
  population — pooled compositions are margins). PASS iff
  median adjusted R² < 0.01 AND the share of draws
  rejecting is ≤ 0.10 (the binomial tolerance the
  regenerated construction requires; freeze Amendment 1
  part 3).
- *Positive control:* each site's composition = the arm's
  pooled composition perturbed toward a site-specific set
  of 10 signs (probability × 3, renormalised). Sets are
  **deterministic**: disjoint blocks of 10 from the 60 most
  frequent mapped sign columns under the arm's pooled
  ranking, assigned in the arm's frozen site order (Arm A:
  Mohenjo-daro, Dholavira, Lothal, Chanhu-daro, Kalibangan;
  Arm B: Harappa, Mohenjo-daro, Dholavira, Lothal,
  Chanhu-daro, Kalibangan); the sets are recorded in
  `margins-audit.json`. PASS iff ≥ 95% of draws reject AND
  the adjusted R² interval lies entirely above 0.01.

Pre-freeze calibration on synthetic data only
(`calibration.json`, produced by `build_calibration.py`
through `pipeline393.py`, the module whose pipeline section
the execution script copies verbatim) must show both
controls PASS for both arms before this freeze is merged;
the calibration results are quoted in `freeze.md`.

**Population reproduction is a precondition:** if the
executed populations differ from §4's frozen margins in any
count, the run is INVALID (population not reproduced) and
stops before any outcome.

### 5.1 Arm A — Harappa-excluded (CONFIRMATORY, primary)

- **Bounded claim:** site-linked repertoire structure
  at/above the practical margin exists among the
  non-Harappa sites — i.e. in the named corpus, under M77,
  after rarefaction and type stratification, site explains
  more recorded sign-repertoire variation than expected
  under permuted site labels, at adjusted R² margin 0.01,
  in the population that excludes Harappa.
- **Population:** Arm A population (1,593 records, 5 sites).
- **Draw:** the Phase-392 cell rarefaction, unchanged:
  within each site × type-class cell, sample without
  replacement to n_cell = **49**; cells below 49 are
  excluded from the rarefied population and reported.
  Included cells (6): Mohenjo-daro SEAL/TAB, Dholavira
  SEAL, Lothal SEAL, Chanhu-daro SEAL, Kalibangan SEAL →
  294 inscriptions per draw. Excluded: Dholavira TAB 15,
  Lothal TAB 2, Chanhu-daro TAB 2, Kalibangan TAB 3.
- **Jackknife:** LOSO over the 5 Arm A sites, recomputed
  identically (no permutation); the clause is part of the
  verdict rule.
- **Sensitivity (labelled, no verdict):** S-complete —
  exclude records whose joined `complete` field is `N`
  (1,303 records; included cells re-derived under the same
  ≥ 49 rule — 4 cells per the margins audit); recompute
  median adjusted R² and rejection share.

### 5.2 Arm B — site-equal-weight (CONFIRMATORY, secondary)

- **Bounded claim:** the site effect is not an
  inscription-count artefact of the large corpora — i.e.
  in the named corpus, under M77 and type stratification,
  site explains more recorded sign-repertoire variation
  than expected under permuted site labels, at adjusted
  R² margin 0.01, when every site contributes equally to
  every draw regardless of its inscription count.
- **Population:** the full analysis population (3,030
  records, 6 sites).
- **Draw (site-equal quota):** each site contributes
  exactly **Q = 52** inscriptions per draw (312 per draw) —
  Q is the smallest analysis-site total (Kalibangan, 52),
  so every site can fill its quota from its own records.
  Within a site, the quota is split across type classes in
  proportion to the site's own type-class counts by the
  frozen allocation rule: largest-remainder proportional
  allocation, ties broken by type-class name ascending, a
  stratum capped at its own count with any capped remainder
  reassigned by continuing the same order. Sampling within
  each site × type-class allocation is without replacement.
  The per-site allocations are deterministic functions of
  the frozen margins and are recorded in the execution
  output. (Kalibangan's quota equals its full record count;
  its contribution is its whole recorded repertoire in
  every draw. That is the estimand working as designed, and
  it is stated here so it cannot be mistaken for an error.)
- **Jackknife:** LOSO over the 6 sites with Q held at 52
  (the quota is a design constant, not re-derived per
  drop); recomputed identically (no permutation).
- **No S-complete sensitivity for Arm B:** the frozen
  design carries the sensitivity on Arm A only; Arm B's
  bounded claim is about count weighting, and adding a
  second sensitivity to the secondary arm would multiply
  labelled non-verdicts without adjudicating anything the
  freeze names. Recorded as a design decision, not an
  omission.

### 5.3 Arm C — Harappa decomposition (EXPLORATORY, no verdict)

Descriptive only; no p-values, no margin comparisons, no
verdict language. Computed on the Arm C population and the
analysis population's mean compositions (no rarefaction):

1. The 6 × 6 matrix of Bray–Curtis distances between site
   mean compositions.
2. Harappa vs the pooled other-five-sites mean composition:
   total Bray–Curtis distance and its per-column
   decomposition (|p_i − q_i| / 2 per column, ranked; the
   top 25 columns recorded with their shares of the total).
3. Type decomposition: Harappa-vs-others Bray–Curtis within
   SEAL records only and within TAB records only (mean
   compositions); and the Harappa SEAL vs Harappa TAB mean
   composition distance.
4. Harappa's recorded token mass by type class (a margin,
   restated beside the decomposition).

Arm C answers "what carries Harappa's contribution"
descriptively. It cannot support, defeat, or soften any
verdict, and it is labelled EXPLORATORY in every output,
including the generated report.

### 5.4 Multiplicity and reporting

Hierarchical, frozen here: **Arm A is the primary claim.**
**Arm B is a separate bounded claim**, reported at its own
frozen rule and labelled SECONDARY wherever reported. No
pooled headline across arms is permitted: no combined
verdict, no combined effect size, no sentence of the form
"Spec 028 shows …" that merges the arms' verdicts. The
outcome record reports the arms side by side, each under
its own claim, plus the Phase-392 side-by-side (§7).

### 5.5 Verdict rules (per arm, applied mechanically)

For each confirmatory arm, with its own quantities:

- **INVALID** iff a control of that arm fails, or the
  population is not reproduced, or a frozen rule was
  changed after outcome inspection. No primary verdict is
  issued from that arm's numbers.
- **SUPPORTED** iff the arm's controls pass AND ≥ 95% of
  the arm's primary draws reject (p ≤ 0.05) AND the arm's
  adjusted R² percentile interval lies entirely above
  0.01 AND every LOSO median adjusted R² of that arm
  is > 0.01.
- **CONTRADICTED** iff the arm's controls pass AND
  (≥ 95% of the arm's primary draws fail to reject OR the
  arm's adjusted R² percentile interval lies entirely at
  or below 0.01).
- **INCONCLUSIVE** iff the arm's controls pass and neither
  rule fires (including a jackknife range crossing the
  margin while the primary interval does not — the
  Phase-392 case, named here in advance for both arms).

## 6. Freeze inputs

- `build_margins_audit.py` → `margins-audit.json`: population
  flow and per-arm margins; reproduces the Phase-392 frozen
  counts exactly (eligible 3,144; analysis 3,030; Arm A
  1,593; cells as in §4/§5.1; Arm B quota feasibility for
  every LOSO drop; Arm C counts). Arm A and Arm B are both
  ESTIMABLE on margins; had either failed its support rules,
  the freeze would have recorded NOT ESTIMABLE for that arm
  and proceeded with the estimable arm(s) only.
- `pipeline393.py` + `build_calibration.py` →
  `calibration.json`: synthetic-only calibration of both
  arms' controls under the final (amended) design — both
  controls PASS for both arms (quoted in `freeze.md`). The
  calibration sequence that forced Amendment 1 (three
  attempts and one diagnostic, all synthetic) is recorded
  in `freeze.md` in full; `calibration.json` holds the
  final configuration's results.
- `build_freeze.py` → `freeze.json`: the framework026
  canonical freeze record (digest over the definition, this
  spec, the freeze record, the adjudication, the audit, the
  calibration, the pipeline module, and the freeze tests).

## 7. Relation to Phase-392

The outcome record (`outcome.md`) carries a side-by-side
statement: Phase-392 INCONCLUSIVE (its numbers, unchanged)
beside each arm's verdict, each under its own frozen rule
and population. If an arm's verdict changes the *reading*
of Phase-392's result (for example, Arm A SUPPORTED would
show the site-general claim fails only in the
six-site-jackknife form Phase-392 froze, not in substance),
that reading is recorded in
`historical-assessment-phase392.md` as a historical
assessment — appended, dated, and explicitly not an edit to
Spec 027. Neither arm mechanically revises Phase-392's
verdict, and Phase-392's verdict does not pre-decide either
arm.

## 8. Execution shape

- Phase-393 script `backend/scripts/phase393_harappa_
  robustness.py` + graph module
  `backend/glossa_lab/experiment_graph_phase393.py`,
  registered in `experiment_graph.py` and verified, before
  the run (H15/H23, in that order).
- The script asserts the input hashes, reproduces the
  frozen populations, runs Arm A, Arm B, and Arm C exactly
  as frozen, and writes `reports/phase393_results.json` and
  `reports/phase393_report.md`. A deadline guards the run.
- Outcome + side-by-side + historical assessment (if any)
  in this directory; append-only entries in both program
  ledgers (`LEDGER.md`, `glossa-indus/LEDGER.md`).
- Closeout: full backend suite and foundation check on
  merged main; anchors byte-identical; PRED register
  untouched (no scoring run exists under this spec).

## 9. Requirements

- **FR-028-1** The claim register passes the Spec 026
  integrity check (no cycles, missing dependencies, or
  forbidden inheritance).
- **FR-028-2** The margins audit contains no outcome field;
  a test pins the fence.
- **FR-028-3** Both arms' controls are calibrated on
  synthetic data before the freeze, through the same
  pipeline code the execution runs (verbatim-copy identity
  asserted by test).
- **FR-028-4** The freeze is a framework026 digest record;
  the freeze tests pin the audit margins, the design
  constants, and digest replay.
- **FR-028-5** The frozen contract is registered on OSF
  after the freeze merge and before execution; the
  registration URL is recorded in this directory and both
  ledgers.
- **FR-028-6** The H23 order is observed: script → graph
  module → registration → verification → run.
- **FR-028-7** The executed populations reproduce the
  frozen margins exactly, asserted in the run before any
  outcome; a mismatch stops the run as INVALID.
- **FR-028-8** Verdicts are per arm under §5.5, applied
  mechanically from the run outputs; decisive numbers are
  recomputed from the results JSON before being reported.
- **FR-028-9** Arm C is descriptive only: no p-values, no
  margin rule, no verdict; labelled EXPLORATORY in every
  output.
- **FR-028-10** No pooled cross-arm headline anywhere in
  the outcome record, the generated report, or the ledger
  entries.
- **FR-028-11** Phase-392's record is never modified by
  this spec; any changed reading is an appended historical
  assessment.
- **FR-028-12** Anchors remain byte-identical and no
  PRED-2026 scoring occurs; verified at closeout.
- **FR-028-13** No external send or deposit is made under
  this spec beyond the pre-execution OSF registration of
  the frozen contract.
- **FR-028-14** Every deviation from this spec or the
  freeze is recorded as it happens, in the outcome record,
  with its evidence.

## 10. Epistemic boundaries (H13)

**Assumptions declared:** site is the analytic unit (a
recorded provenance label in the layer, not a political or
ethnic entity); the M77-keyed layer is the corpus *as
recorded* — its dedup and conversion chain are inherited
from the Phase-115/116 build and the Spec 027 freeze;
composition proportions normalise inscription length by
construction; within a type-class stratum, site labels are
exchangeable under the null; the adjusted R² scale carries
the margin's meaning (a share of dispersion beyond null
expectation), as established by Phase-392 Amendment 1.

**Adversarial challenges named in advance:** (1) Harappa's
distinctiveness could be an excavation/publication-history
artefact — the design answers only the robustness question
named in §1; preservation and completeness confounds are
addressed only to the extent the S-complete sensitivity
(Arm A) speaks to completeness, and the outcome record must
say so. (2) Period is **not** controlled: the layer's period
field is 59.2% uninformative (Phase-139 audit, inherited
limitation, restated wherever a verdict headline appears).
(3) Multi-line status is not recorded in this layer;
eligibility ran on the frozen legible-token rule (inherited
boundary). (4) Arm B's equal quota discards most of the two
large sites' records by design; its estimand is the
equal-weight one named in §5.2 and no other.

**Belief artifacts relied on:** the Phase-392 frozen record
and outcome (program records); the Spec 027 adjudication's
inherited values (M77; Ask 3 rules); the Spec 026 verdict
taxonomy and margin convention. No P1 belief artifact below
MEDIUM confidence is relied on for any verdict.

AI disclosure: authored and executed by an AI agent
(Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.
