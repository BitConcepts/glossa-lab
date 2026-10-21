# Spec 036 — PRED-2026-011: Scoring the Screened Clean-Withholding Successor, Exactly as Registered

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-20
>
> Drafted under the owner's draft order of
> 2026-10-20 (draft the PRED-2026-011 scoring
> spec), recorded in `adjudication.md`. This
> spec designs the scoring of PRED-2026-011
> exactly as registered. It executes nothing:
> execution is **Phase-400**, under the owner's
> separate freeze and execution orders, and only
> after the freeze of this contract merges. As
> with Spec 035, the registration this design
> rests on already exists — the prediction's own
> OSF preregistration (https://osf.io/t6whq/) —
> and it was verified by API at this draft
> (`osf-registration.md`). Nothing in this draft
> opens the withheld file for content.

## 1. Purpose

PRED-2026-011 has stood in the prediction
register since 2026-10-20 with Tested **PENDING**
and Outcome **PENDING**. It is the successor to
PRED-2026-010, which Spec 035 / Phase-399 closed
at step 0 as CANNOT BE RUN AS WRITTEN (unscored)
because one of its three trained signs, P000,
has no counterpart in the frozen crosswalk — one
unmappable sign of three is 33%, above the
registered 20% cap. PRED-2026-010 was itself the
clean-withholding successor to PRED-2026-006,
which Spec 032 / Phase-396 closed at step 0
(unscored) because its trained set had been
derived from the combined corpus.

PRED-2026-011 removed both predecessor defects
at registration: the withholding is clean by
construction (the CISI Mohenjo-daro pool only,
as in PRED-2026-010), and the trained set was
screened for mappability before registration,
using only the public, hash-pinned crosswalk —
the one design change, disclosed in the entry
itself. This spec freezes nothing yet. It
carries the registered test into a freezable
contract, exactly as registered — the
criterion, the trained set, the screen, the
data, the unmappable rule, and the verdict
language are the register's. Where the
registered test cannot be run as written, this
spec's step 0 (§3) closes the study unscored
and says so; it does not substitute a
friendlier test.

## 2. The registered test

From `docs/PREDICTION_REGISTER.md`,
PRED-2026-011 (H3 successor: Cross-Site Class
Preservation — clean withholding, disclosed
mappability screen), registered 2026-10-20,
quoted in substance with its pins:

- **Prediction.** Signs assigned to the INITIAL
  class in training on CISI Mohenjo-daro
  inscriptions ONLY, after the disclosed
  mappability screen below, will appear
  preferentially in initial position in
  Harappa-specific Yajnadevam data as well.
- **Trained INITIAL set (derived at
  registration, frozen).** P217, P324 — 2 signs.
  The unscreened classification reproduced
  PRED-2026-010 exactly: 179 CISI Mohenjo-daro
  inscriptions, 28 classifiable signs (INITIAL
  3, MEDIAL 19, MIXED 3, TERMINAL 3), unscreened
  INITIAL set P000, P217, P324, derived by the
  recorded `global_class_stability`
  classification logic carried verbatim (as in
  the frozen Phase-396 build
  `backend/scripts/phase396_pred006_step0.py`).
  Derivation:
  `backend/scripts/pred011_register_derivation.py`;
  record:
  `docs/research/pred-2026-011-registration/derivation-record.json`.
- **Mappability screen (the one disclosed
  design change).** Before registration, an
  INITIAL sign is eligible only if at least one
  row in the frozen public crosswalk names it
  as `best_parpola_match`. Appearances in
  `top3_parpola` do not establish a counterpart.
  P217 is eligible through Y0520 (confidence
  1.0, confirmed); P324 is eligible through
  Y0740 (confidence 0.9867, confirmed); P000 is
  excluded because it has no best-match row and
  appears only in `top3_parpola` on Y0527,
  Y0740, Y0820, and Y0892. The screen used only
  the public crosswalk; no Harappa inscription
  rows, sequences, occurrence counts, or start
  rates informed the design. P000 was not
  excluded because of any observed Harappa
  behaviour; no Harappa behaviour for P000 was
  examined.
- **Training pool (fixed by hash).**
  `data/normalized/corpus_master.csv`, SHA-256
  `b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e`,
  filtered to source "Corpus of Indus Seals and
  Inscriptions (mayig digitization)" — all 179
  rows Mohenjo-daro, zero Yajnadevam rows;
  filtered-pool manifest SHA-256
  `ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a`.
- **Withheld data (fixed by hash).**
  Harappa-site Yajnadevam sequences in
  `backend/glossa_lab/data/yajnadevam_inscriptions.csv`,
  SHA-256
  `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`,
  held separate; byte-hashed only at
  registration, not opened for content.
- **Crosswalk (fixed by reference).**
  `data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`,
  SHA-256
  `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2`.
  At scoring, sign identity is carried only by
  rows whose `best_parpola_match` is the
  trained sign. A trained sign with no
  counterpart is UNMAPPABLE; if unmappable
  signs exceed 20% of the trained set — with 2
  signs, any single unmappable sign is 50% —
  the scoring closes as CANNOT BE RUN AS
  WRITTEN.
- **Success criterion.** ≥ 70% of the trained
  INITIAL signs above show start_rate ≥ 0.40 at
  Harappa site (bars identical in form to
  PRED-2026-006 and PRED-2026-010). A sign's
  start rate is the share of its Harappa
  occurrences, counted through its best-match
  counterpart glyphs, in which it is the first
  sign of a sequence. A mappable sign with zero
  Harappa occurrences does not meet the bar and
  remains in the denominator.
- **Small-set caveat (the register's own words,
  in substance).** This is a two-sign test,
  weaker than PRED-2026-010's already small
  three-sign test. The possible shares are only
  0, 1/2, and 1, so the 70% bar passes only at
  2 of 2; each sign carries half the verdict. A
  pass would establish only that P217 and P324
  both met the bar in this pinned dataset. It
  would not validate the INITIAL class as a
  whole, estimate a general cross-site
  preservation rate, say anything about P000's
  positional behaviour, or establish a
  decipherment or sign meaning. A failure would
  likewise be a failure of this exact two-sign
  criterion, not a refutation of cross-site
  preservation for the wider INITIAL class.
- **Method constraint.** Positional
  classification only; no semantic anchoring
  (SA-free).
- **Disclosure (carried verbatim in substance;
  see §8).** The Yajnadevam Harappa pool was
  previously inspected in aggregate during the
  Spec 032 closure audit, and those counts are
  published in its record. No Harappa start
  rate has ever been computed for P217 or P324.
  The cleanliness claimed is verified
  training-pool exclusion — the trained set
  provably never saw the pool — not analyst
  blindness.
- **OSF registration.** https://osf.io/t6whq/,
  DOI 10.17605/OSF.IO/T6WHQ, filed 2026-10-20
  from the Predictions & Registrations node
  `nrb9u`; verified accepted and public at this
  draft (`osf-registration.md`).

This draft does not edit the register. The
outcome, whatever it is, is appended to the
register at execution as a dated entry (§7).

## 3. Step 0 — verification before any Harappa content is touched

Four checks, in this order. Each has a stated
failure outcome, and each failure closes the
study as itself — never as a verdict. The order
is part of the design: the withheld file's
*content* is opened only after every check has
passed (its SHA-256 in check 0.2 is a byte
operation, not content access).

### 0.1 The registration still stands

The OSF registration (t6whq) is re-verified by
API at execution: `reviews_state` accepted,
`public` true, `pending_registration_approval`
false, `withdrawn` false, `embargoed` false,
and the DOI identifier equal to
10.17605/OSF.IO/T6WHQ. This check was discharged
at this draft (2026-10-20;
`osf-registration.md`) and is re-run at
execution, because a registration's state can
change. If the registration no longer stands as
recorded, execution does not proceed and the
study stops here, reported as itself.

### 0.2 Input integrity

The SHA-256 of each pinned file is recomputed
and must equal the registered hash: the
training pool (`b19cfe95…`), the crosswalk
(`e44b8b55…`), and the withheld file
(`c02e3d7b…`). (All three were verified against
the bytes on `main` at this draft; see
`adjudication.md` §2.) Any mismatch closes the
study as **CANNOT BE RUN AS WRITTEN**: the
inputs no longer are the registered inputs, and
scoring different bytes would score a
different prediction.

### 0.3 The training-pool exclusion and the disclosed screen, re-verified

The Spec 032 lesson, applied to this successor:
the withholding is re-proven, not assumed — and
for this prediction the screen is part of what
is re-proven. From
`data/normalized/corpus_master.csv`, apply the
registered filter (source "Corpus of Indus
Seals and Inscriptions (mayig digitization)")
and assert the filtered pool is exactly the
registered pool: 179 rows, every row
Mohenjo-daro, zero Yajnadevam rows, and the
recomputed filtered-pool manifest hash equal to
`ab3b4c8a…`. Then rerun the recorded
`global_class_stability` classification logic
verbatim — imported unchanged from the frozen
Phase-396 build, exactly as the registration
derivation ran it — over the filtered pool only,
and assert the result equals the derivation
record
(`docs/research/pred-2026-011-registration/derivation-record.json`):
28 classifiable signs with class counts INITIAL
3, MEDIAL 19, MIXED 3, TERMINAL 3, and the
unscreened INITIAL set exactly {P000, P217,
P324}. Then apply the registered mappability
screen to that unscreened set against the
pinned crosswalk — eligible only if at least
one crosswalk row names the sign as
`best_parpola_match`; `top3_parpola` appearances
never establish eligibility — and assert the
screened set is exactly {P217, P324}, with
P000's exclusion reproduced as a screen outcome
(no best-match row; `top3_parpola` appearances
only, on Y0527, Y0740, Y0820, Y0892). Any
mismatch closes the study as **CANNOT BE RUN AS
WRITTEN**, unscored: a different trained set is
a different prediction, and registering it would
require a new PRED number under the register's
own rules. No set is improvised, the screen is
not re-run under a different reading, and the
pool is never widened.

### 0.4 Crosswalk coverage — the unmappable cap

For each trained sign, determine its counterpart
in the frozen crosswalk. A trained sign with no
counterpart is UNMAPPABLE. With 2 trained signs,
one unmappable sign is 50% of the set — above
the registered 20% cap — so **any** unmappable
trained sign closes the scoring as **CANNOT BE
RUN AS WRITTEN**, unscored, before the withheld
file is opened. This check reads only the
crosswalk and the trained set.

"Counterpart" carries the programme's
established reading, fixed here so step 0 has no
discretion (DD-036-5, carrying DD-035-5): the
frozen Phase-396 build's `fix_crosswalk`
reading, under which a trained sign's
counterparts are the Yajnadevam glyphs whose row
in the crosswalk names the sign as its
`best_parpola_match`; appearances in a row's
`top3_parpola` alternatives never create a
counterpart — they set the conflict flag (§5,
§8).

**Draft-stage expectation, recorded for the
freeze decision — an expectation, not a
determination.** That reading was applied to the
pinned crosswalk at this draft (a read of a
hash-pinned mapping file; no withheld content
was touched). Under it, both trained signs
carry confirmed best-match counterparts: P217 →
Y0520 (confidence 1.0, confirmed, the sole
best-match row naming P217) and P324 → Y0740
(confidence 0.9867, confirmed, the sole
best-match row naming P324). Check 0.4 is
therefore designed to **pass**, and — the
earlier checks passing — execution would
proceed to the first scoring of the H3 line
(§5). The check still runs fail-closed at
execution exactly as written: the formal
determination remains a step-0 act, and this
draft executes no step 0 and determines
nothing. The expectation is recorded here, and
in `adjudication.md`, so the freeze decision is
made with open eyes — in the opposite direction
from Spec 035's: there the freeze bought a
formal closure record; here it buys a scored
verdict, CONFIRMED or NOT CONFIRMED, unless an
earlier check closes the study first.

### The step-0 record

The outcome of every check — the recomputed
hashes, the pool census, the reproduced class
census and unscreened set, the reproduced
screen outcome, the crosswalk coverage — is
written as a step-0 record and hashed before
any scoring begins (the Spec 032 pattern). If a
check closes the study, that record is the
outcome, and it is reported as a closure, not a
verdict (§6).

## 4. Data

The withheld set, as recorded at the Spec 032
freeze for the byte-identical file (the hash in
§2/§0.2 ties that census to these bytes) and
restated in the PRED-2026-011 registration:
`backend/glossa_lab/data/yajnadevam_inscriptions.csv`
— 5,679 inscriptions, 77 sites, of which 2,717
are Harappa. Each row carries its site, sign
sequence, and CISI object reference. The scoring
pool is the Harappa-site rows of that file,
reached only after step 0 passes. Rights
posture: the file is Yajnadevam's publicly
released lipi dataset, already held and used by
the programme; derived statistics are
publishable, and this study publishes statistics,
not the dataset.

The training side is closed: the pool of §2, the
derivation record, and nothing else. No training
data is added, refreshed, or re-derived under
this spec beyond the step-0 reproduction of
§0.3, which must match the record exactly or
close the study. The screen is likewise closed:
it is reproduced at §0.3 under its registered
rule, never re-designed.

## 5. Method

Exactly the registered computation, nothing
added (the Spec 032 §5 computation, restated
for this trained set and stated in the
registration's analysis plan). For each sign in
the frozen trained INITIAL set, mapped through
the frozen crosswalk to its Yajnadevam
counterpart glyphs (§0.4: the glyphs whose best
match is the sign), its start rate at Harappa
is the share of its Harappa occurrences (in the
withheld sequences, counted over those glyphs)
in which it stands in initial position — initial
position being the first sign of a sequence, so
a one-sign sequence's sign stands initial. Count
the signs with a start rate at or above 0.40.
Divide by the number of trained INITIAL signs
(2). Compare to 70%.

One edge is already fixed by the registration
itself, so it cannot be decided after the fact
(DD-036-2): a mappable trained sign with
**zero** Harappa occurrences has no start rate
and therefore does not show a start rate at or
above 0.40; it counts as not meeting the bar
and remains in the denominator. The registered
criterion has no not-estimable band, and this
spec does not invent one (§6).

One descriptive addition is pre-registered here
so it cannot be mistaken for a criterion: the
per-sign table (every trained sign, its crosswalk
counterpart, its Harappa occurrence count, its
initial-position count, its start rate, and a
conflict-pair flag where the crosswalk records
one) is published with the outcome, so the
small-denominator structure of a 2-sign test is
visible to any reader. The table is descriptive
only; it carries no criterion and moves no
verdict.

## 6. Criteria and verdict mapping

These are the register's criteria, not this
spec's:

- **CONFIRMED** — the share of §5 is at least
  70%. With 2 trained signs, this is exactly 2
  of 2.
- **NOT CONFIRMED** — the share is below 70%:
  0 or 1/2.

There is no inconclusive band in the registered
criterion, and this spec does not invent one.
The only soft landings are the step-0 closures
(**CANNOT BE RUN AS WRITTEN**; a registration
stop under §0.1), each reported as itself, not
dressed as a verdict. A step-0 closure is not a
refutation: PRED-2026-011 would remain unscored,
and the register's §4 (Failed Predictions) gains
no entry from a closure.

## 7. Register handling at execution

Scoring follows the register's own discipline:
the outcome, whatever it is, is appended to
`docs/PREDICTION_REGISTER.md` as a dated entry
under §6 (insertions only), under the owner's
execution order, and the Phase D register-hash
pin is advanced by name for that authorised
change. If the outcome is a verdict, the §3
entry's Tested/Outcome fields for
PRED-2026-011 move from PENDING in the same
append. If the outcome is a step-0 closure, the
§3 Outcome stays **PENDING** — the Spec 035
precedent for PRED-2026-010 (F035-C15): a
closure is not a verdict, and the register does
not record it as one. PRED-2026-006's and
PRED-2026-010's entries stay byte-identical and
both remain unscored. This draft changes no
register text, no other prediction's state, and
no Spec 026–035 record.

## 8. Controls and named confounders

- **Within-lineage caution, stated in the
  verdict wording.** The Yajnadevam
  compilation's object base is itself
  published-corpus material, so the independence
  this test has is the *site-withholding* the
  registration specified — Harappa held out of
  training — not independence of scholarly
  lineage. The verdict claims the first and not
  the second.
- **The disclosure travels with every outcome
  statement.** The Harappa pool was inspected in
  aggregate during the Spec 032 closure audit
  (970 Harappa inscriptions inside the old
  combined training corpus, carrying 1,013
  occurrences of 11 of 006's 12 trained signs).
  No outcome statement under this spec may claim
  blind withholding; the cleanliness claimed is
  verified training-pool exclusion (§0.3),
  exactly as registered. No Harappa start rate
  has ever been computed for P217 or P324.
- **Small-set fragility.** Two signs; each
  carries half the verdict. Every outcome
  statement carries the register's small-set
  caveat in its first paragraph — the 2-of-2
  pass structure is a property of the clean pool
  and the disclosed screen, stated before any
  scoring, not a defect discovered after one.
- **The screen is an eligibility rule, not a
  result.** P000's exclusion was decided at
  registration on the public crosswalk alone.
  No outcome statement may present the screen as
  evidence about P000's positional behaviour,
  and no outcome for this prediction says
  anything about P000 at all.
- **Crosswalk conflicts.** Conflict-pair signs
  are flagged in the per-sign table (§5) — the
  Y0740 row's `top3_parpola` also names P000,
  which sets that flag for P324's counterpart;
  the crosswalk is used as the registered
  mapping, fixed before counting.
- **Sequence-length composition.** Composition
  at Harappa differs from Mohenjo-daro's; the
  registered criterion does not adjust for it,
  so neither does this design — the composition
  is described alongside the outcome.
- **The neighbouring figures are not this
  test.** The old global figure (72.7% INITIAL
  stability across all sites on the pooled
  corpus) is a different quantity, computed on
  the pool that voided 006; PRED-2026-010's
  step-0 closure is a record about a different
  trained set. No outcome statement may present
  either as evidence for or against this
  prediction.

## 9. What this design would move, and what it would not establish

**What it would move.** PRED-2026-011 from
PENDING to scored — the first time the H3
cross-site class preservation hypothesis is
scored at all: the first test in the line whose
withholding was clean by construction *and*
whose trained signs all carried crosswalk
counterparts under a mapping fixed before
counting. Either outcome is valuable, and both
are narrow by registration: confirmation would
be the first registered prediction this
programme confirms on its own criterion, and it
would establish only that P217 and P324 both
met the bar in this pinned dataset;
non-confirmation retires the exact two-sign
criterion on evidence rather than on suspicion.
On the draft-stage expectation (§0.4), step 0
passes in full and the scoring runs; if an
earlier check instead closes the study, the
movement is from PENDING to CLOSED AT STEP 0 —
unscored, not refuted — and §6 forbids reporting
it as a scoring.

**What it would NOT establish.** Anything beyond
the registered statement: that these 2 signs,
trained at Mohenjo-daro, open texts at Harappa
in this dataset at the registered rates. Not
why, not what the signs mean, not stability at
any other site, not the INITIAL class as a
whole, not anything about P000, and not anything
about PRED-2026-006 or PRED-2026-010, whose
closures stand as recorded.

## 10. Execution shape (Phase-400 — NOT run by this spec)

1. **Graph-first build** (H15/H23): experiment
   script, graph module, registration in the
   experiment graph, then run.
2. **Step 0** (§3): registration re-verification,
   input integrity, training-pool and screen
   re-verification, crosswalk coverage — in that
   order, fail-closed, with the step-0 record
   written and hashed before any scoring. A
   step-0 failure closes the study as recorded
   in §3 and the closure is the outcome.
3. **Scoring** (§5): the registered computation
   only; the per-sign table produced with it.
4. **Outcome:** the verdict under §6 or the
   closure under §3, appended to the PRED
   register as a dated entry (§7), and recorded
   in this spec's directory and the root LEDGER;
   the foundation check (H21) is run after the
   claim consequence lands; nothing is written
   into any frozen record.

## 11. What this spec does not do

- It does not execute anything. Execution
  (Phase-400) follows the owner's freeze order
  for this contract and a separate execution
  order.
- It does not open the withheld file for
  content, compute any Harappa count, or compute
  any start rate. At this draft the withheld
  file was not touched for content; its
  registered hash was verified against the bytes
  on `main` by a streaming hash, the same byte
  operation the registration itself performed.
- It does not widen the trained set, re-run the
  screen under a different reading, adjust the
  bars, add a band, or substitute a different
  test (§§5–6).
- It does not score, re-open, or alter
  PRED-2026-006 or PRED-2026-010 (both closed,
  unscored) or any other prediction.
- It does not edit the PRED register, the
  derivation record, or any frozen Spec 026–035
  record.
- It files no new OSF registration at draft.
  The prediction's preregistration (t6whq) is
  the registered contract this design implements;
  whether the frozen spec also files its own OSF
  contract registration (the Spec 032–034 pattern,
  and the Spec 035 freeze's decision) is a
  freeze-time decision, recorded as DD-036-4.

## 12. Governed claims (summary)

The governed register is `claims.json`
(F036-C01…C15):

- **C01** — a verdict under this spec states
  whether the registered criterion for
  PRED-2026-011 is met, and nothing beyond that
  statement.
- **C02** — the success criterion is the
  registered one: at least 70% of the trained
  INITIAL signs with a Harappa start rate of at
  least 0.40 — with 2 signs, only 2 of 2 passes.
- **C03** — the trained INITIAL set is the
  registration's screened set: P217, P324,
  derived from CISI Mohenjo-daro only and
  screened under the registered rule, fixed by
  the pinned derivation record.
- **C04** — step 0 re-derives the pool, the
  classification, and the screen, and must
  reproduce the screened trained set exactly —
  P000's exclusion reproduced as a screen
  outcome — before any withheld content is
  opened; failure closes the study as CANNOT BE
  RUN AS WRITTEN, unscored.
- **C05** — every input is pinned by its
  registered SHA-256 (pool file, filtered-pool
  manifest, crosswalk, withheld file); a mismatch
  closes the study as CANNOT BE RUN AS WRITTEN.
- **C06** — the OSF registration (t6whq) stands
  accepted and public; it is verified before
  execution design is finalised and re-verified
  at execution.
- **C07** — the cleanliness claimed is verified
  training-pool exclusion, not analyst blindness;
  the aggregate-inspection disclosure travels
  with every outcome statement.
- **C08** — sign identity is carried by the
  frozen crosswalk only, fixed before counting.
- **C09** — any unmappable trained sign is 50%
  of the set, above the registered 20% cap, and
  closes the scoring as CANNOT BE RUN AS WRITTEN
  before the withheld file is opened.
- **C10** — the score is the share of trained
  signs whose Harappa start rate is at least
  0.40, computed on the withheld Harappa sequences
  only, a start rate being the share of a sign's
  occurrences, counted through its counterpart
  glyphs, in which it stands initial.
- **C11** — a mappable trained sign with zero
  Harappa occurrences does not meet the bar.
- **C12** — the per-sign table is published with
  the outcome as a descriptive record; it carries
  no criterion.
- **C13** — the verdict wording claims only the
  site-withholding independence the registration
  specified, carries the small-set caveat, and
  says nothing about P000.
- **C14** — the outcome is appended to the PRED
  register as a dated entry; PRED-2026-006's and
  PRED-2026-010's entries stay byte-identical and
  both remain unscored.
- **C15** — step-0 closures are reported as
  themselves, never as verdicts; a closure is not
  a refutation.

## 13. Design decisions

- **DD-036-1 — Step 0 fails closed, in a fixed
  order.** Each verification has a stated failure
  outcome (§3); no check is waived, sampled, or
  repaired by substitution, and the withheld
  file's content is opened only after all four
  pass. The order — registration, input integrity,
  training-pool and screen re-verification,
  crosswalk coverage — puts the Spec 032 lesson
  (re-prove the withholding) before any contact
  with the withheld content.
- **DD-036-2 — The zero-occurrence edge is
  registered, not decided here.** Unlike Spec
  035, where the corresponding edge (DD-035-2)
  had to be fixed at draft, PRED-2026-011's
  entry states the rule itself: a mappable sign
  with zero Harappa occurrences does not meet
  the bar and remains in the denominator (§5).
  This spec carries it; it does not re-open it.
  Recorded so the freeze decision does not
  mistake a registered rule for an open point.
- **DD-036-3 — The per-sign table is
  descriptive.** Pre-registered as a descriptive
  addition (§5) so it cannot be mistaken for a
  criterion — with 2 signs, the table *is* the
  result's context, and it moves no verdict.
- **DD-036-4 — OPEN PROPOSAL: a spec-level OSF
  registration, decided at freeze.** Specs
  032–034 each filed their own OSF contract
  registration after freezing, and Spec 035's
  freeze decided the same (DD-035-4, decided
  YES). This prediction arrived already
  registered (t6whq, filed at prediction
  registration from node `nrb9u`). This draft
  files nothing new. **Proposal to the freeze
  decision: follow the DD-035-4 precedent and
  file the frozen spec's own OSF contract
  registration in addition to t6whq.** Either
  way, execution step 0 re-verifies t6whq
  (§0.1), and if a spec registration is filed,
  it is verified the same way before any run.
  The full proposal set for the freeze decision
  is recorded in `adjudication.md` §3.
- **DD-036-5 — The counterpart reading is fixed
  in the design.** "Counterpart" in check 0.4
  and in the §0.3 screen reproduction means the
  frozen Phase-396 build's reading (best-match
  rows carry identity; top-3 alternatives set
  conflict flags only) — named in §0.4, not left
  to execution, carrying DD-035-5. The
  alternative — letting step 0 choose a reading —
  was rejected for the reason recorded there: a
  reading chosen at execution, with its outcome
  visible, is not the registered test.
- **DD-036-6 — Freeze mechanics are the house
  pattern.** The freeze digest is the
  framework026 `build_freeze` digest, computed
  over the claim register and the finalised
  freeze texts exactly once, at the freeze act,
  after the AEE lifecycle hooks pass over the
  register (the hooks are a freeze gate; they
  have not run on this draft — `plan.md`,
  `aee/freeze-aee-note.md`). The digest in
  `freeze.json` at this draft is a draft digest
  over this draft contract and decides nothing.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
