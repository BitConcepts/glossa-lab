# Spec 035 — PRED-2026-010: Scoring the Clean-Withholding Successor, Exactly as Registered

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-20
>
> Drafted under the owner's order of 2026-10-20
> ("Let's do your recommendation" — the recommendation
> named the CISI 3.1 intake and the drafting of this
> scoring spec), recorded in `adjudication.md`. This
> spec designs the scoring of PRED-2026-010 exactly as
> registered. It executes nothing: execution is
> **Phase-399**, under the owner's separate freeze and
> execution orders, and only after the freeze of this
> contract merges. Unlike Specs 032–034, the
> registration this design rests on already exists —
> the prediction's own OSF preregistration
> (https://osf.io/wjebq/) — and it was verified by API
> at this draft (`osf-registration.md`). Nothing in
> this draft opens the withheld file for content.

## 1. Purpose

PRED-2026-010 has stood in the prediction register
since 2026-10-13 with Tested **PENDING** and Outcome
**PENDING**. It is the clean-withholding successor to
PRED-2026-006, which Spec 032 / Phase-396 closed at
step 0 as CANNOT BE RUN AS WRITTEN (unscored) because
its trained set had been derived from the combined
corpus — the withheld Harappa data sat inside the
training pool. PRED-2026-010 removed that defect at
registration: its trained set was derived from the
CISI Mohenjo-daro pool only and frozen by hash before
any scoring.

This spec freezes nothing yet. It carries the
registered test into a freezable contract, exactly
as registered — the criterion, the trained set, the
data, the unmappable rule, and the verdict language
are the register's. Where the registered test cannot
be run as written, this spec's step 0 (§3) closes
the study unscored and says so; it does not
substitute a friendlier test.

## 2. The registered test

From `docs/PREDICTION_REGISTER.md`, PRED-2026-010
(H3 successor: Cross-Site Class Preservation — clean
withholding), registered 2026-10-13, quoted in
substance with its pins:

- **Prediction.** Signs assigned to the INITIAL
  class in training on CISI Mohenjo-daro
  inscriptions ONLY will appear preferentially in
  initial position in Harappa-specific Yajnadevam
  data as well.
- **Trained INITIAL set (derived at registration,
  frozen).** P000, P217, P324 — 3 signs. Derived by
  the recorded `global_class_stability`
  classification logic carried verbatim (as in the
  frozen Phase-396 build
  `backend/scripts/phase396_pred006_step0.py`) over
  the CISI Mohenjo-daro pool only: 179 inscriptions,
  28 classifiable signs (INITIAL 3, MEDIAL 19,
  MIXED 3, TERMINAL 3). Derivation:
  `backend/scripts/pred010_register_derivation.py`;
  record: `reports/pred010_derivation_record.json`.
- **Training pool (fixed by hash).**
  `data/normalized/corpus_master.csv`, SHA-256
  `b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e`,
  filtered to source "Corpus of Indus Seals and
  Inscriptions (mayig digitization)" — all 179 rows
  Mohenjo-daro, zero Yajnadevam rows; filtered-pool
  manifest SHA-256
  `ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a`.
- **Withheld data (fixed by hash).** Harappa-site
  Yajnadevam sequences in
  `backend/glossa_lab/data/yajnadevam_inscriptions.csv`,
  SHA-256
  `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`,
  held separate; byte-hashed only at registration,
  not opened for content.
- **Crosswalk (fixed by reference).**
  `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`,
  SHA-256
  `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`.
  At scoring, a trained sign with no crosswalk
  counterpart is UNMAPPABLE (denominator only); if
  unmappable signs exceed 20% of the trained set —
  with 3 signs, any single unmappable sign is 33% —
  the scoring closes as CANNOT BE RUN AS WRITTEN.
- **Success criterion.** ≥ 70% of the trained
  INITIAL signs above show start_rate ≥ 0.40 at
  Harappa site (bars identical to PRED-2026-006).
- **Small-set caveat (the register's own words, in
  substance).** The clean pool yields 3 trained
  signs, so the share can only be 0, 1/3, 2/3, or
  1, and the 70% bar passes only at 3 of 3; each
  sign carries a third of the verdict. The set is
  registered exactly as derived — the pool was not
  widened to enlarge it, because widening is what
  voided 006.
- **Method constraint.** Positional classification
  only; no semantic anchoring (SA-free).
- **Disclosure (carried verbatim in substance; see
  §8).** The Yajnadevam Harappa pool was previously
  inspected in aggregate during the Spec 032
  closure audit, and those counts are published in
  its record. No Harappa start rate has ever been
  computed for any sign. The cleanliness claimed is
  verified training-pool exclusion — the trained
  set provably never saw the pool — not analyst
  blindness.
- **OSF registration.** https://osf.io/wjebq/,
  DOI 10.17605/OSF.IO/WJEBQ, filed 2026-10-13 from
  the Predictions & Registrations node `nrb9u`;
  verified accepted and public at this draft
  (`osf-registration.md`).

This draft does not edit the register. The outcome,
whatever it is, is appended to the register at
execution as a dated entry (§7).

## 3. Step 0 — verification before any Harappa content is touched

Four checks, in this order. Each has a stated
failure outcome, and each failure closes the study
as itself — never as a verdict. The order is part
of the design: the withheld file's *content* is
opened only after every check has passed (its
SHA-256 in check 0.2 is a byte operation, not
content access).

### 0.1 The registration still stands

The OSF registration (wjebq) is re-verified by API
at execution: `reviews_state` accepted, `public`
true, `pending_registration_approval` false,
`withdrawn` false, `embargoed` false, and the DOI
identifier equal to 10.17605/OSF.IO/WJEBQ. This
check was discharged at this draft (2026-10-20;
`osf-registration.md`) and is re-run at execution,
because a registration's state can change. If the
registration no longer stands as recorded,
execution does not proceed and the study stops
here, reported as itself.

### 0.2 Input integrity

The SHA-256 of each pinned file is recomputed and
must equal the registered hash: the training pool
(`b19cfe95…`), the crosswalk (`e44b8b55…`), and the
withheld file (`c02e3d7b…`). (All three were
verified against the bytes on `main` at this draft;
see `adjudication.md` §2.) Any mismatch closes the
study as **CANNOT BE RUN AS WRITTEN**: the inputs
no longer are the registered inputs, and scoring
different bytes would score a different prediction.

### 0.3 The training-pool exclusion, re-verified

The Spec 032 lesson, applied to this successor:
the withholding is re-proven, not assumed. From
`data/normalized/corpus_master.csv`, apply the
registered filter (source "Corpus of Indus Seals
and Inscriptions (mayig digitization)") and assert
the filtered pool is exactly the registered pool:
179 rows, every row Mohenjo-daro, zero Yajnadevam
rows, and the recomputed filtered-pool manifest
hash equal to `ab3b4c8a…`. Then rerun the recorded
`global_class_stability` classification logic
verbatim — imported unchanged from the frozen
Phase-396 build, exactly as the registration
derivation ran it — over the filtered pool only,
and assert the result equals the derivation record
(`reports/pred010_derivation_record.json`): 28
classifiable signs with class counts INITIAL 3,
MEDIAL 19, MIXED 3, TERMINAL 3, and the trained
INITIAL set exactly {P000, P217, P324}. Any
mismatch closes the study as **CANNOT BE RUN AS
WRITTEN**, unscored: a different trained set is a
different prediction, and registering it would
require a new PRED number under the register's own
rules. No set is improvised, and the pool is never
widened.

### 0.4 Crosswalk coverage — the unmappable cap

For each trained sign, determine its counterpart
in the frozen crosswalk. A trained sign with no
counterpart is UNMAPPABLE. With 3 trained signs,
one unmappable sign is 33% of the set — above the
registered 20% cap — so **any** unmappable trained
sign closes the scoring as **CANNOT BE RUN AS
WRITTEN**, unscored, before the withheld file is
opened. This check reads only the crosswalk and
the trained set.

"Counterpart" carries the programme's established
reading, fixed here so step 0 has no discretion
(DD-035-5): the frozen Phase-396 build's
`fix_crosswalk` reading, under which a trained
sign's counterparts are the Yajnadevam glyphs
whose row in the crosswalk names the sign as its
`best_parpola_match`; appearances in a row's
`top3_parpola` alternatives never create a
counterpart — they set the conflict flag (§5, §8).

**Draft-stage observation, recorded for the freeze
decision.** That reading was applied to the pinned
crosswalk at this draft (a read of a hash-pinned
mapping file; no withheld content was touched).
Under it: P217 has a best-match counterpart
(glyph Y0520, confidence 1.0, confirmed) and P324
has one (glyph Y0740, confidence 0.9867,
confirmed); **P000 has none** — it appears only
as a top-3 alternative (on the rows for Y0527,
Y0740, Y0820, and Y0892), never as a best match.
If the step-0 determination under the frozen
contract applies the same reading to the same
pinned bytes, check 0.4 closes this study as
**CANNOT BE RUN AS WRITTEN**, unscored, and that
closure is the outcome. The formal determination
remains a step-0 act; this draft executes no step
0 and closes nothing. The observation is recorded
here, and in `adjudication.md`, so the freeze
decision is made with open eyes.

### The step-0 record

The outcome of every check — the recomputed
hashes, the pool census, the reproduced class
census and trained set, the crosswalk coverage —
is written as a step-0 record and hashed before
any scoring begins (the Spec 032 pattern). If a
check closes the study, that record is the
outcome, and it is reported as a closure, not a
verdict (§6).

## 4. Data

The withheld set, as recorded at the Spec 032
freeze for the byte-identical file (the hash in
§2/§0.2 ties that census to these bytes):
`backend/glossa_lab/data/yajnadevam_inscriptions.csv`
— 5,679 inscriptions, 77 sites, of which 2,717 are
Harappa. Each row carries its site, sign sequence,
and CISI object reference. The scoring pool is the
Harappa-site rows of that file, reached only after
step 0 passes. Rights posture: the file is
Yajnadevam's publicly released lipi dataset,
already held and used by the programme; derived
statistics are publishable, and this study
publishes statistics, not the dataset.

The training side is closed: the pool of §2, the
derivation record, and nothing else. No training
data is added, refreshed, or re-derived under this
spec beyond the step-0 reproduction of §0.3, which
must match the record exactly or close the study.

## 5. Method

Exactly the registered computation, nothing added
(the Spec 032 §5 computation, restated for this
trained set). For each sign in the frozen trained
INITIAL set, mapped through the frozen crosswalk
to its Yajnadevam counterpart glyphs (§0.4: the
glyphs whose best match is the sign), its start
rate at Harappa is the share of its Harappa
occurrences (in the withheld sequences, counted
over those glyphs) in which it stands in initial
position — initial position being the first sign
of a sequence, so a one-sign sequence's sign
stands initial. Count the signs with a start rate
at or above 0.40. Divide by the number of trained
INITIAL signs (3). Compare to 70%.

One edge is fixed here, at draft, so it cannot be
decided after the fact (DD-035-2): a mappable
trained sign with **zero** Harappa occurrences has
no start rate and therefore does not show a start
rate at or above 0.40; it counts as not meeting the
bar. The registered criterion has no
not-estimable band, and this spec does not invent
one (§6).

One descriptive addition is pre-registered here so
it cannot be mistaken for a criterion: the
per-sign table (every trained sign, its crosswalk
counterpart, its Harappa occurrence count, its
initial-position count, its start rate, and a
conflict-pair flag where the crosswalk records
one) is published with the outcome, so the
small-denominator structure of a 3-sign test is
visible to any reader. The table is descriptive
only; it carries no criterion and moves no verdict.

## 6. Criteria and verdict mapping

These are the register's criteria, not this spec's:

- **CONFIRMED** — the share of §5 is at least 70%.
  With 3 trained signs, this is exactly 3 of 3.
- **NOT CONFIRMED** — the share is below 70%:
  0, 1/3, or 2/3.

There is no inconclusive band in the registered
criterion, and this spec does not invent one. The
only soft landings are the step-0 closures
(**CANNOT BE RUN AS WRITTEN**; a registration stop
under §0.1), each reported as itself, not dressed
as a verdict. A step-0 closure is not a
refutation: PRED-2026-010 would remain unscored,
and the register's §4 (Failed Predictions) gains
no entry from a closure.

## 7. Register handling at execution

Scoring follows the register's own discipline: the
outcome, whatever it is, is appended to
`docs/PREDICTION_REGISTER.md` as a dated entry
under §6 (insertions only), under the owner's
execution order; the §3 entry's Tested/Outcome
fields for PRED-2026-010 move from PENDING in the
same append, and the Phase D register-hash pin is
advanced by name for that authorised change — the
two 2026-10-13 precedents (the PRED-2026-006
closure entry; the PRED-2026-010 registration)
record exactly this handling. PRED-2026-006's
entries stay byte-identical and it remains
unscored. This draft changes no register text, no
other prediction's state, and no Spec 026–034
record.

## 8. Controls and named confounders

- **Within-lineage caution, stated in the verdict
  wording.** The Yajnadevam compilation's object
  base is itself published-corpus material, so the
  independence this test has is the
  *site-withholding* the registration specified —
  Harappa held out of training — not independence
  of scholarly lineage. The verdict claims the
  first and not the second.
- **The disclosure travels with every outcome
  statement.** The Harappa pool was inspected in
  aggregate during the Spec 032 closure audit (970
  Harappa inscriptions inside the old combined
  training corpus, carrying 1,013 occurrences of
  11 of 006's 12 trained signs). No outcome
  statement under this spec may claim blind
  withholding; the cleanliness claimed is verified
  training-pool exclusion (§0.3), exactly as
  registered.
- **Small-set fragility.** Three signs; each
  carries a third of the verdict. Every outcome
  statement carries the register's small-set
  caveat in its first paragraph — the 3-of-3 pass
  structure is a property of the clean pool,
  stated before any scoring, not a defect
  discovered after one.
- **Crosswalk conflicts.** Conflict-pair signs are
  flagged in the per-sign table (§5); the
  crosswalk is used as the registered mapping,
  fixed before counting.
- **Sequence-length composition.** Composition at
  Harappa differs from Mohenjo-daro's; the
  registered criterion does not adjust for it, so
  neither does this design — the composition is
  described alongside the outcome.
- **The neighbouring figure is not this test.**
  The old global figure (72.7% INITIAL stability
  across all sites on the pooled corpus) is a
  different quantity, computed on the pool that
  voided 006. No outcome statement may present it
  as evidence for or against this prediction.

## 9. What this design would move, and what it would not establish

**What it would move.** PRED-2026-010 from PENDING
to scored — the first time the H3 cross-site class
preservation hypothesis is scored on a withholding
that was clean by construction. Either outcome is
valuable: confirmation is the first registered
prediction this programme confirms on its own
criterion; non-confirmation retires the INITIAL
class's cross-site claim on evidence rather than
on suspicion. On the draft-stage coverage
observation (§0.4), the likelier movement is
different, and it is stated plainly: execution
would close the study at step 0.4, moving
PRED-2026-010 from PENDING to CLOSED AT STEP 0 —
unscored, not refuted — the second prediction in
the H3 line to end that way, this time on
crosswalk coverage rather than training
contamination. A closure reached under a frozen
contract is a finding with a record; it is not a
scoring, and §6 forbids reporting it as one.

**What it would NOT establish.** Anything beyond
the registered statement: that these 3 signs,
trained at Mohenjo-daro, open texts at Harappa in
this dataset at the registered rates. Not why, not
what the signs mean, not stability at any other
site, and not anything about PRED-2026-006, whose
closure stands as recorded.

## 10. Execution shape (Phase-399 — NOT run by this spec)

1. **Graph-first build** (H15/H23): experiment
   script, graph module, registration in the
   experiment graph, then run.
2. **Step 0** (§3): registration re-verification,
   input integrity, training-pool re-verification,
   crosswalk coverage — in that order, fail-closed,
   with the step-0 record written and hashed before
   any scoring. A step-0 failure closes the study
   as recorded in §3 and the closure is the outcome.
3. **Scoring** (§5): the registered computation
   only; the per-sign table produced with it.
4. **Outcome:** the verdict under §6, appended to
   the PRED register as a dated entry (§7), and
   recorded in this spec's directory and the root
   LEDGER; the foundation check (H21) is run after
   the claim consequence lands; nothing is written
   into any frozen record.

## 11. What this spec does not do

- It does not execute anything. Execution
  (Phase-399) follows the owner's freeze order for
  this contract and a separate execution order.
- It does not open the withheld file for content,
  compute any Harappa count, or compute any start
  rate. At this draft the withheld file was not
  touched at all; its registered hash was verified
  against the bytes on `main` by a streaming hash,
  the same byte operation the registration itself
  performed.
- It does not widen the trained set, adjust the
  bars, add a band, or substitute a different
  test (§§5–6).
- It does not score, re-open, or alter
  PRED-2026-006 (closed, unscored) or any other
  prediction.
- It does not edit the PRED register, the
  derivation record, or any frozen Spec 026–034
  record.
- It files no new OSF registration at draft. The
  prediction's preregistration (wjebq) is the
  registered contract this design implements;
  whether the frozen spec also files its own OSF
  contract registration (the Spec 032–034 pattern)
  is a freeze-time decision, recorded as DD-035-4.

## 12. Governed claims (summary)

The governed register is `claims.json`
(F035-C01…C15):

- **C01** — a verdict under this spec states
  whether the registered criterion for
  PRED-2026-010 is met, and nothing beyond that
  statement.
- **C02** — the success criterion is the
  registered one: at least 70% of the trained
  INITIAL signs with a Harappa start rate of at
  least 0.40 — with 3 signs, only 3 of 3 passes.
- **C03** — the trained INITIAL set is the
  registration's: P000, P217, P324, derived from
  CISI Mohenjo-daro only and fixed by the pinned
  derivation record.
- **C04** — step 0 re-derives the pool and the
  classification and must reproduce the trained
  set exactly before any withheld content is
  opened; failure closes the study as CANNOT BE
  RUN AS WRITTEN, unscored.
- **C05** — every input is pinned by its
  registered SHA-256 (pool file, filtered-pool
  manifest, crosswalk, withheld file); a mismatch
  closes the study as CANNOT BE RUN AS WRITTEN.
- **C06** — the OSF registration (wjebq) stands
  accepted and public; it is verified before
  execution design is finalised and re-verified
  at execution.
- **C07** — the cleanliness claimed is verified
  training-pool exclusion, not analyst blindness;
  the aggregate-inspection disclosure travels
  with every outcome statement.
- **C08** — sign identity is carried by the
  frozen crosswalk only, fixed before counting.
- **C09** — any unmappable trained sign is 33%
  of the set, above the registered 20% cap, and
  closes the scoring as CANNOT BE RUN AS WRITTEN
  before the withheld file is opened.
- **C10** — the score is the share of trained
  signs whose Harappa start rate is at least
  0.40, computed on the withheld Harappa sequences
  only, a start rate being the share of a sign's
  occurrences in which it stands initial.
- **C11** — a mappable trained sign with zero
  Harappa occurrences does not meet the bar.
- **C12** — the per-sign table is published with
  the outcome as a descriptive record; it carries
  no criterion.
- **C13** — the verdict wording claims only the
  site-withholding independence the registration
  specified, and carries the small-set caveat.
- **C14** — the outcome is appended to the PRED
  register as a dated entry; PRED-2026-006's
  entries stay byte-identical and it remains
  unscored.
- **C15** — step-0 closures are reported as
  themselves, never as verdicts; a closure is not
  a refutation.

## 13. Design decisions

- **DD-035-1 — Step 0 fails closed, in a fixed
  order.** Each verification has a stated failure
  outcome (§3); no check is waived, sampled, or
  repaired by substitution, and the withheld
  file's content is opened only after all four
  pass. The order — registration, input integrity,
  training-pool re-verification, crosswalk
  coverage — puts the Spec 032 lesson (re-prove
  the withholding) before any contact with the
  withheld content.
- **DD-035-2 — The zero-occurrence edge is fixed
  at draft.** A mappable trained sign absent at
  Harappa counts as not meeting the bar (§5). The
  alternative — closing as not-estimable — was
  rejected: the registered criterion has no such
  band, and inventing one after seeing the counts
  would be a criterion change. Recorded here so
  the freeze decision can overturn it openly if
  the owner prefers the closure reading.
- **DD-035-3 — The per-sign table is
  descriptive.** Pre-registered as a descriptive
  addition (§5) so it cannot be mistaken for a
  criterion — with 3 signs, the table *is* the
  result's context, and it moves no verdict.
- **DD-035-4 — No separate spec registration at
  draft.** Specs 032–034 each filed their own OSF
  contract registration after freezing. This
  prediction arrived already registered (wjebq,
  filed at prediction registration from node
  `nrb9u`). This draft files nothing new; the
  freeze act decides whether the frozen spec
  follows the 032–034 pattern with its own filing.
  Either way, execution step 0 re-verifies wjebq
  (§0.1), and if a spec registration is filed, it
  is verified the same way before any run.
- **DD-035-5 — The counterpart reading is fixed
  in the design.** "Counterpart" in check 0.4
  means the frozen Phase-396 build's reading
  (best-match rows carry identity; top-3
  alternatives set conflict flags only) — named in
  §0.4, not left to execution. The alternative —
  letting step 0 choose a reading — was rejected:
  a reading chosen at execution, with its
  consequence visible, is a criterion decision
  taken after the fact. Fixing the reading is
  also what makes the §0.4 observation meaningful:
  the freeze decision is taken knowing what the
  established reading yields on the pinned
  crosswalk.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
