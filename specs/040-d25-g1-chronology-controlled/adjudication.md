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

## 5. Freeze-plan approval and the freeze act — 2026-10-24

§3 asked the freeze to decide five things. The
freeze-plan package
(`2026-10-24-spec-040-freeze-plan.md`, prepared
2026-10-24 on the owner's order from the merged
record at `58bb6ac7`) put those decisions, the
dependency judgment, and the derivation choice
to the owner as one package. **On 2026-10-24 at
10:54 EDT the owner approved the plan as
specified ("Approve as specified").** This
section records that approval and the decisions
it carries. It is the freeze record's
adjudication half; `freeze.md` is its other
half.

### 5.1 The dependency judgment (plan R1)

The §1 gate is judged **satisfied by
successor-artifact substitution, openly
recorded**:

- **Spec 039's own artifact did not satisfy
  §1.** That 2026-10-20 finding stands
  unchanged: Spec 039 executed (freeze digest
  `ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742`;
  PRs #226/#234/#235), and its artifact,
  `data/movement/gazetteer_rows_assigned.jsonl`
  (SHA-256
  `64f288d35c492d8babacb4efb9c7446573a62168095db44f7469cd7904fcabb4`,
  recomputed at this freeze), assigns periods
  per site as label sets with no site ×
  local-label mapping key, and carries no rows
  for three of the seven G1 sites — §1
  conditions 2 and 4 failed, and Spec 040
  closed NOT-YET-TESTABLE at the dependency
  gate.
- **Spec 041's artifact satisfies the §1
  interface in substance and is accepted as
  the successor dependency artifact** — the
  separately governed act Spec 040's own
  closure contemplated. Spec 041 froze on
  2026-10-22 (freeze digest
  `fe6188864d5ff497fed5e3e89456d0499987c2cbc8ada5997920e864360dfdc7`)
  and executed as Phase-435. Its artifact,
  `data/evidence_integration/site_period_mapping.jsonl`
  (SHA-256
  `1e5b54c9193fb52092c34e1c959ec64a48b83cacbb8e5705f629635183c12b67`;
  meta record SHA-256
  `bda1017dd88da0b14efaa3ffc5ff280b09818349bda4de1ed20f8c60d42864a9`;
  step-0 census SHA-256
  `b57fb6b1a0aa1e491ba38bf18978eec58c355f3bf833f58298c7516aabeca6be`
  — all three recomputed at this freeze), is
  keyed by site × field × local label and
  carries, for each of its 24 MAPPED cells,
  exactly one published determination verified
  `OWN_TEXT` with citation, locator, mapping
  rule, verification mode and `contested:
  false`; its 54 UNASSIGNED cells each carry
  exactly one enumerated reason
  (NO_PUBLISHED_DETERMINATION 35,
  DETERMINATION_UNVERIFIED 10,
  SPANS_COARSE_BOUNDARY 4, LABEL_UNCERTAIN_IN_LAYER 3,
  NOT_IN_PUBLISHED_SCHEME 2); no cell is
  CONTESTED. The substitution is stated here
  and in `freeze.md`, never smoothed over: the
  accepted artifact is Spec 041's product, not
  Spec 039's.

### 5.2 §1 verification at the freeze (plan R2)

Verified mechanically at this act, before the
digest was computed: the artifact recomputes
to its pin; all 78 cells validate against the
frozen schema; the cell census built from the
pinned Phase-139 covariates
(`a0f0d05a…`) equals the artifact's 78
(site, field, local label) triples exactly,
with every cell's `attested_rows` equal; the
population margins reproduce exactly (period
labels 2,266; phase labels 2,638; both 1,788;
any label 3,116; neither 2,294); and the
§4.1 three-record join under derivation A1
yields exactly one assignment row for each of
the 5,410 population inscription IDs — no
missing ID, duplicate, extra row, or site
mismatch. Anchors stand at
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
(recomputed at this freeze).

### 5.3 The derivation (plan R3)

**Derivation A1 governs** as the sole primary
row derivation: a row is placed when at least
one of its recorded labels is MAPPED and every
MAPPED label agrees on one coarse period; an
UNASSIGNED label does not veto; disagreement
between MAPPED labels, no recorded label, or
all labels UNASSIGNED leaves the row
UNASSIGNED in the primary. No field precedence
applies. A2, B and C are not chosen and are not
silently substituted at execution. Reproduced
at this freeze from the pinned inputs under
A1: **1,457 placed** (EARLY 32, MATURE 1,386,
LATE 39); 3,953 unplaced (2,294 no informative
label, 1,658 all labels UNASSIGNED, 1
disagreement — the Kalibangan row, period 1
EARLY against phase "Late" MATURE, left
unplaced and visible). Placed by site:
Dholavira 133, Harappa 1,021, Kalibangan 157,
Lothal 108, Nausharo 38, Mohenjo-daro 0,
Chanhu-daro 0.

### 5.4 The remaining decisions (plan R4)

- **DD-040-1 — ADOPTED.** The governing basic
  bootstrap interval against the V = 0.10
  margin assigns any eventual §6 outcome; the
  permutation p is computed and reported but
  cannot rescue an interval that fails the
  margin; no p-value threshold is a second
  gate.
- **DD-040-5 — CONFIRMED.** The thinness
  closure's word is **NOT-YET-TESTABLE**, not
  D-25's "INCONCLUSIVE-BY-DESIGN."
- **DD-040-6 — RETAINED.** The third §5
  margins arm (at least 1,000 permutable
  inscriptions) stays in the frozen gate. All
  three §5 margins arms are retained.
- **DD-040-9 — FILED.** The frozen spec files
  its own OSF registration, following the
  standing freeze → OSF sequence (record:
  `osf-spec-registration.md`, completed by
  append after filing).
- **DD-040-10 — ALLOCATED.** The highest
  phase on the merged record at this act is
  Phase-438 (Spec 054); the execution phase
  allocated mechanically is **Phase-439**.
- **§8.1 — NOT APPLICABLE.** The accepted
  artifact contains zero CONTESTED cells, so
  there are no contested mappings to include
  and no sensitivity label to consume; the
  contested-included sensitivity is recorded
  NOT APPLICABLE for this freeze. Candidate
  disagreement strands preserved inside Spec
  041's determination sets are not
  reclassified as contested cells.

### 5.5 The known margins consequence — stated, not hidden

On Spec 041's published counts, reproduced at
§5.3 above, Spec 040 §5's margins gate already
fails under **every** derivation: EARLY
retains assigned inscriptions from 1 distinct
site (Harappa) and LATE from 2 (Dholavira,
Lothal), against the 5-site arm; and the
unassigned share exceeds the 40% arm under
every derivation (A1/C 73.1%, B 74.8%,
A2 85.6%) — Mohenjo-daro places 0 of its
1,923 population rows under every derivation.
This freeze is therefore a
dependency-settlement and closure act: it
settles the dependency and the derivation and
locks the contract. If execution is later
ordered and §5 is retained unchanged, the
expected outcome is **NOT-YET-TESTABLE at the
margins gate**, not a chronology-controlled
verdict on G1. No part of this act loosens §5
to make the test run.

### 5.6 What the approval does not authorise

No execution of Spec 040 in any part — no
margins run, regression, primary, sensitivity,
or outcome (plan R7). Execution begins only on
a later owner order naming Spec 040 and
Phase-439. No anchor, reading, or PRED-2026
state is touched by this act.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
