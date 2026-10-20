# Spec 036 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-20
>
> This spec has one adjudication input, recorded
> here so the draft's basis is inspectable:
>
> 1. **The owner's draft order of 2026-10-20**:
>    draft the PRED-2026-011 scoring spec (Spec
>    036), as a draft only. That order is the
>    adjudicating act for this **draft**. It
>    commissions the design only: the freeze of
>    this contract and any execution are separate
>    owner decisions, not commissioned by it, and
>    this draft performs neither. The
>    PRED-2026-011 entry's own scoring gate states
>    the same: registration alone is not a scoring
>    order; scoring requires its own future spec
>    and a separate owner order. This draft is
>    that spec's design act, and it stops there.

## 1. The adopted basis (operative substance)

The registered test, carried into `spec.md`
without deviation:

- **Prediction.** Signs assigned to the INITIAL
  class in training on CISI Mohenjo-daro
  inscriptions ONLY, after the disclosed
  mappability screen, will appear preferentially
  in initial position in Harappa-specific
  Yajnadevam data as well (PRED-2026-011, the
  successor to PRED-2026-010, closed unscored by
  Spec 035 / Phase-399 at step 0.4, and through
  it to PRED-2026-006, closed unscored by Spec
  032 / Phase-396 at step 0.2).
- **Trained set.** P217, P324 (2 signs), derived
  at registration from the CISI Mohenjo-daro
  pool only (179 inscriptions, 28 classifiable
  signs; unscreened INITIAL set P000, P217,
  P324) by the recorded classification logic
  carried verbatim, then screened under the
  registered rule.
- **Screen.** An INITIAL sign is eligible only
  if at least one row in the frozen public
  crosswalk names it as `best_parpola_match`;
  `top3_parpola` appearances do not establish a
  counterpart. P217 is eligible through Y0520;
  P324 through Y0740; P000 is excluded (no
  best-match row), for the mapping reason only.
- **Criterion.** At least 70% of the trained
  signs show a Harappa start rate of at least
  0.40 — with 2 signs, only 2 of 2 passes (the
  register's small-set caveat). A sign's start
  rate is the share of its Harappa occurrences,
  counted through its best-match counterpart
  glyphs, in which it is the first sign of a
  sequence.
- **Zero-occurrence rule (registered, not a
  design decision).** A mappable sign with zero
  Harappa occurrences does not meet the bar and
  remains in the denominator (DD-036-2).
- **Unmappable rule.** Any trained sign with no
  crosswalk counterpart is 50% of the set, above
  the registered 20% cap: the scoring closes as
  CANNOT BE RUN AS WRITTEN before the withheld
  file is opened.
- **Disclosure.** The cleanliness claimed is
  verified training-pool exclusion, not analyst
  blindness; the Harappa pool was inspected in
  aggregate during the Spec 032 closure audit.
  No Harappa start rate has ever been computed
  for P217 or P324.

## 2. Verification record at draft

Every registered fact this design rests on was
verified first-hand at drafting, 2026-10-20,
against the record on `main` (head `5e7f3cdb`,
the PRED-2026-011 registration-completion
merge):

- **Register entry** — read in
  `docs/PREDICTION_REGISTER.md` §3 (the
  PRED-2026-011 entry) and the two §6 notes of
  2026-10-20 (registration; OSF approval):
  prediction, trained set, screen rule and
  outcome, pins, criterion, zero-occurrence
  rule, unmappable closure, small-set caveat,
  disclosure, scoring gate, OSF pointer. All as
  designed here.
- **Registration package** — read in
  `docs/research/pred-2026-011-registration/`
  (README, OSF payload as filed, derivation
  record): pool 179 rows, all Mohenjo-daro, zero
  Yajnadevam rows; 28 classifiable signs
  (INITIAL 3 / MEDIAL 19 / MIXED 3 / TERMINAL
  3) with the full class map; unscreened INITIAL
  set [P000, P217, P324]; screen outcome
  (retained [P217, P324]; P000 excluded, no
  best-match row, `top3_parpola` appearances on
  Y0527, Y0740, Y0820, Y0892 only); criterion
  arithmetic (denominator 2, minimum passing
  signs 2, possible shares 0, 0.5, 1); the
  recorded classification script pin
  (`37e7bb53…`); the derivation script
  `backend/scripts/pred011_register_derivation.py`.
- **File pins** — recomputed by streaming hash
  from the bytes on `main` at this draft, all
  equal to the registered pins:
  `data/normalized/corpus_master.csv`
  `b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e`;
  `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`
  `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`;
  `backend/glossa_lab/data/yajnadevam_inscriptions.csv`
  `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`.
  The withheld file was hashed, not opened — the
  same byte operation the registration performed.
- **Crosswalk coverage at draft** — read from
  the pinned crosswalk itself (a public mapping
  file; no withheld content touched): P217 is
  named `best_parpola_match` on exactly one row
  (glyph Y0520, confidence 1.0, confirmed); P324
  on exactly one row (glyph Y0740, confidence
  0.9867, confirmed — that row's `top3_parpola`
  also names P000, the conflict flag the Spec
  035 record noted); P000 is named on no row.
  On the frozen reading, check 0.4 is therefore
  expected to **pass** at execution and the
  scoring to run — recorded in `spec.md` §0.4
  as an expectation only. The formal
  determination remains a step-0 act; this draft
  executes no step 0 and determines nothing.
- **Withheld census** — 5,679 inscriptions, 77
  sites, 2,717 Harappa, as recorded at the Spec
  032 freeze for the byte-identical file and
  restated in the PRED-2026-011 OSF payload; the
  pin above ties that census to these bytes.
- **OSF registration** — API-verified at this
  draft: accepted, public, DOI
  10.17605/OSF.IO/T6WHQ (`osf-registration.md`).
- **Not verified at draft, by design** — the
  filtered-pool manifest pin (`ab3b4c8a…`) is a
  derived value: it stands in the derivation
  record as read, and its re-derivation is
  step-0 check 0.3 at execution (spec §3). No
  Harappa count, occurrence count, or start rate
  was computed at this draft, and none exists
  anywhere in the record for P217 or P324.

## 3. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), knowing §0.4's
   expectation: step 0 is expected to pass in
   full, and execution (Phase-400) would then
   reach the first scoring of the H3 line — a
   CONFIRMED or NOT CONFIRMED verdict on the
   exact two-sign criterion — unless an earlier
   check (0.1–0.3) closes the study first. The
   opposite of the Spec 035 decision, where the
   freeze bought a formal closure record. Or
   decline, leaving PRED-2026-011 PENDING.
2. **DD-036-4 (proposal): whether the frozen
   spec files its own OSF contract registration**
   (the Spec 032–034 pattern), in addition to
   the prediction's preregistration (t6whq).
   **Recommendation: yes — follow the DD-035-4
   precedent**, which Spec 035's freeze decided
   the same way on the same structure (a
   prediction that arrived already registered).
   If filed, its record is kept in this
   directory and completed by append once the
   approval verifies, and execution step 0
   re-verifies both registrations.
3. The draft-fixed readings stand unless the
   freeze overturns them openly: the fixed
   step-0 order, fail-closed (DD-036-1); the
   per-sign table as descriptive only
   (DD-036-3); the counterpart reading
   (DD-036-5). The zero-occurrence rule is not
   among them: it is registered text (DD-036-2),
   and changing it would be a criterion change,
   not a design decision.

## 4. Freeze adjudication — 2026-10-20

4. **The owner's do-all order of 2026-10-20**:
   "do all of spec 036 now" — ordering the full
   Spec 036 arc (freeze, the spec-level OSF
   contract registration, and Phase-400
   execution) in one act. This order decides
   §3's questions:

   1. The contract is **FROZEN** as recovered at
      the freeze act (register 0.9-draft; the AEE
      lifecycle gate below), and Phase-400
      execution is ordered in the same act.
   2. **DD-036-2 is registered text carried, not
      a design decision**: the zero-occurrence
      reading (a mappable sign absent at Harappa
      counts as not meeting the bar) is the
      PRED-2026-011 registration's own text,
      restated here for the record; it is not
      opened, adopted, or overturned by this
      freeze.
   3. The draft-fixed readings **stand**:
      DD-036-1 (the fixed step-0 order,
      fail-closed), DD-036-3 (the per-sign table
      as descriptive only), DD-036-5 (the
      counterpart reading).
   4. **DD-036-4 is decided YES**: the frozen
      spec files its own OSF contract
      registration (the Spec 032–034 pattern), in
      addition to the prediction's
      preregistration (t6whq). Its record is
      filed in `osf-spec-registration.md` and
      completed by append once the approval
      verifies.

**The freeze gate (AEE lifecycle hooks).** The
hooks ran at this freeze act over the register
(after_specify / after_plan / after_tasks; gate
**pass**; `aee/freeze-aee-note.md`,
`aee/recovery-specify.md`). after_specify took
five rounds — 10, then 3, then 1, then 1 failure
modes, then 0 — of atomic rewrites, boundary
trims, pairwise confirmations, and one pair
separated by truthful phrasing; propositions,
falsifiers, and verdict rules were unchanged
throughout. after_plan and after_tasks passed
on the recovered register (0.9-draft) at the
first pass. No claim stood below the 0.70
threshold in any round. The freeze digest
recorded in `freeze.json` is computed over the
recovered register and the finalised freeze
texts, once.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
