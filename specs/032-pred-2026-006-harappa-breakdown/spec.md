# Spec 032 — PRED-2026-006: The Harappa Breakdown, Computed Exactly as Registered

> ## DESIGN — FOR FREEZE — 2026-10-13
>
> This spec freezes design **D-30** of the experiment-design
> portfolio of 2026-10-13 (`docs/research/
> experiment-designs-2026-10-13/`, draft PR #195),
> commissioned by the owner's order of 2026-10-13
> ("Design experiments for all of the 35 that remain in
> question or inconclusive") and adjudicated for freeze by
> the owner's order of 2026-10-13 06:39 EDT ("Freeze
> D-30, D-03, and D-20 for execution"). The adjudication
> is recorded in `adjudication.md`. Execution
> (**Phase-396**) runs only after this freeze merges and
> the OSF registration of this frozen contract verifies
> public; no execution is performed by this spec.

## 1. Purpose

PRED-2026-006 has stood in the prediction register since
2026-04-22 with the outcome **PARTIALLY CONFIRMED**. The
number under that outcome — 72.7% stability for the
INITIAL class — is a global figure across sites, measured
by `scripts/global_class_stability.py`. The registered
test itself is narrower and has never been run: the
register's own entry says "Harappa-specific breakdown
pending". This spec freezes the registered test, exactly
as registered, so the prediction can be scored on its own
criterion for the first time. It designs nothing new: the
criterion, the withheld data, and the verdict language
are the register's. Where the registered test cannot be
run as written, this spec's step 0 (§3) closes the study
and says so; it does not substitute a friendlier test.

## 2. The registered test

From `docs/PREDICTION_REGISTER.md`, PRED-2026-006
(H3: Cross-Site Class Preservation), registered
2026-04-22, quoted in substance:

- **Prediction.** Signs assigned to the INITIAL class in
  CISI Mohenjo-daro will appear preferentially in initial
  position in Harappa-specific Yajnadevam data as well.
- **Withheld data.** Harappa-site Yajnadevam sequences
  (held separate from the full-corpus analysis).
- **Success criterion.** At least 70% of the CISI-trained
  INITIAL signs show a start rate of at least 0.40 at
  the Harappa site.
- **Recorded state.** Tested: PARTIALLY — the global
  figure of 72.7% for the INITIAL class; Harappa-specific
  breakdown pending. Outcome: PARTIALLY CONFIRMED.

The register's §6 note of 2026-10-12 records that
PRED-2026-006 remains PARTIALLY CONFIRMED and is not
affected by the retirement of PRED-2026-004/005/008/009.
This freeze does not edit the register. The outcome,
whatever it is, is appended to the register at execution
as a dated entry (§7).

## 3. Step 0 — provenance checks (the design fails closed here)

Three things are verified from the record before any
counting. Each has a stated failure outcome, and each
failure closes the study as itself — never as a verdict.

### 3.1 The trained INITIAL set

The exact set of signs the CISI Mohenjo-daro training
produced — the lineage of the recorded
`global_class_stability.py` check (`scripts/
global_class_stability.py`; `outputs/analysis/
global_class_stability.json`; `reports/
global_class_stability_report.md`) — is reconstructed
from the program's records and frozen as a list. If the
exact trained set cannot be reproduced from the record,
the study closes as **CANNOT BE RUN AS WRITTEN**: a
similar set built fresh would be a different prediction,
and registering it would require a new PRED number
under the register's own rules. No set is improvised.

### 3.2 The withholding was real for this purpose

The Yajnadevam corpus has been loaded by the program
before (Phases 281–293 used it for unrelated decipherment
work). That exposure is recorded openly at execution.
The narrower fact the registration depends on is verified:
the INITIAL class assignments came from CISI
Mohenjo-daro, and the Harappa Yajnadevam sequences
played no part in training them. If that cannot be
verified, the closure is again **CANNOT BE RUN AS
WRITTEN**, with the reason.

### 3.3 Sign identity

Yajnadevam's sign codes are Mahadevan-style codes; the
trained INITIAL signs are CISI/Mahadevan signs. The
mapping between them uses the program's existing
crosswalk files under `data/crosswalks/` (the
Yajnadevam-to-Parpola crosswalks and their recorded
statistics), fixed before counting. Any trained INITIAL
sign with no crosswalk counterpart is counted and
reported as **UNMAPPABLE**; if unmappable signs exceed
20% of the trained set, the verdict is reported with
that coverage stated in its first sentence.

## 4. Data

The withheld set, verified in hand at this freeze:
`backend/glossa_lab/data/yajnadevam_inscriptions.csv` —
**5,679 inscriptions, 77 sites, of which 2,717 are
Harappa** (census counted for the portfolio design on
2026-10-13 and re-counted at this freeze; the frozen
freeze tests pin the census). Each row carries its site,
sign sequence, and CISI object reference. Rights
posture: the file is Yajnadevam's publicly released lipi
dataset, already held and used by the program; derived
statistics are publishable, and this study publishes
statistics, not the dataset.

## 5. Method

Exactly the registered computation, nothing added. For
each sign in the frozen trained INITIAL set, its start
rate at Harappa is the share of its Harappa occurrences
(in the withheld sequences, through the frozen
crosswalk) in which it stands in initial position. Count
the signs with a start rate at or above 0.40. Divide by
the number of trained INITIAL signs, with the
unmappable handling of §3.3 stated in the output.
Compare to 70%.

One descriptive addition is pre-registered here so it
cannot be mistaken for a criterion: the per-sign table
(every trained sign, its Harappa count, its start rate)
is published with the outcome, so the small-denominator
risk — whether the withheld material is large enough for
the rule to be meaningful sign by sign — is visible to
any reader. The table is descriptive only; it carries
no criterion and moves no verdict.

## 6. Criteria and verdict mapping

These are the register's criteria, not this spec's:

- **CONFIRMED** — the share of §5 is at least 70%.
- **NOT CONFIRMED** — the share is below 70%.

There is no inconclusive band in the registered
criterion, and this spec does not invent one. The only
soft landings are the step-0 closures (**CANNOT BE RUN
AS WRITTEN**; the **UNMAPPABLE** coverage statement),
each reported as itself, not dressed as a verdict.

## 7. Register handling at execution

Scoring follows the register's own discipline: the
outcome, whatever it is, is appended to
`docs/PREDICTION_REGISTER.md` as a dated entry under
the owner's execution order. The register's existing
text is never edited. This freeze changes no register
text, no other prediction's state, and no Spec
026–031 record.

## 8. Controls and named confounders

- **Within-lineage caution, stated in the verdict
  wording.** The Yajnadevam compilation's object base
  is itself published-corpus material, so the
  independence this test has is the *site-withholding*
  the registration specified — Harappa held out of
  training — not independence of scholarly lineage.
  The verdict claims the first and not the second.
- **Crosswalk conflicts.** Conflict-pair signs are
  flagged in the per-sign table.
- **Sequence-length composition.** Composition at
  Harappa differs from Mohenjo-daro's; the registered
  criterion does not adjust for it, so neither does
  this design — the composition is described alongside
  the outcome.

## 9. What this design would move, and what it would not establish

**What it would move.** The prediction from IN QUESTION
(the portfolio's classification) to scored — the first
time since April 2026 that its register entry would rest
on its own test. Either outcome is valuable: confirmation
retires a six-month caveat; non-confirmation corrects a
"PARTIALLY CONFIRMED" that the evidence never carried.

**What it would NOT establish.** Anything beyond the
registered statement: that opening signs are stable at
Harappa in this dataset. Not why, not what the signs
mean, and not stability at any other site.

## 10. Execution shape (Phase-396 — NOT run by this spec)

1. **Graph-first build** (H15/H23): experiment script,
   graph module, registration, registration
   verification, then run.
2. **Step 0** (§3): trained-set reconstruction and
   freeze; withholding verification; crosswalk fixing.
   A step-0 failure closes the study as recorded in §3
   and the closure is the outcome.
3. **Scoring** (§5): the registered computation only;
   the per-sign table produced with it.
4. **Outcome:** the verdict under §6, appended to the
   PRED register as a dated entry (§7), and recorded
   in this spec's directory and the root LEDGER;
   nothing written into any frozen record.

## 11. What this spec does not do

- It does not execute anything. Execution (Phase-396)
  follows the verified OSF approval of this frozen
  contract under the owner's order of 2026-10-13.
- It does not score, re-open, or alter PRED-2026-007
  (design D-31, a separate freeze) or any other
  prediction.
- It does not edit the PRED register, the global
  stability record, or any frozen Spec 026–031 record.
- It introduces no new criterion, band, adjustment, or
  substitute test (§§5–6).

## 12. Governed claims (summary)

The governed register is `claims.json` (F032-C01…C12):

- **C01** — a verdict under this spec states whether the
  registered criterion is met, and nothing beyond that
  statement.
- **C02** — the success criterion is the registered one:
  at least 70% of the frozen trained INITIAL signs with
  a Harappa start rate of at least 0.40.
- **C03** — the trained INITIAL set is reconstructed
  from the recorded training lineage and frozen before
  any counting.
- **C04** — failure to reproduce the exact trained set
  closes the study as CANNOT BE RUN AS WRITTEN.
- **C05** — the INITIAL assignments derive from CISI
  Mohenjo-daro; the Harappa Yajnadevam sequences played
  no part in training them.
- **C06** — sign identity is carried by the existing
  crosswalk files under `data/crosswalks/`, fixed
  before counting.
- **C07** — unmappable trained signs are counted and
  reported; coverage above 20% is stated in the
  verdict's first sentence.
- **C08** — the score is the share of frozen trained
  INITIAL signs whose Harappa start rate is at least
  0.40, computed on the withheld Harappa sequences only.
- **C09** — the per-sign table is published with the
  outcome as a descriptive record.
- **C10** — the verdict wording claims only the
  site-withholding independence the registration
  specified.
- **C11** — the outcome is appended to the PRED register
  as a dated entry; the register's existing text stays
  byte-identical.
- **C12** — step-0 closures are reported as themselves,
  never as verdicts.

## 13. Design decisions

The portfolio design D-30 is carried into this freeze
without deviation. Its own decisions, recorded here as
the design states them:

- **DD-30-1 — Step 0 fails closed.** Each provenance
  check has a stated failure outcome (§3); no check is
  waived, sampled, or repaired by substitution.
- **DD-30-2 — The per-sign table is descriptive.** It is
  pre-registered as a descriptive addition (§5) so it
  cannot be mistaken for a criterion.
- **DD-30-3 — Coverage in the first sentence.** The
  unmappable-coverage statement, when it applies, leads
  the verdict (§3.3), so a thin mapping cannot hide
  behind a headline share.

At freeze time one design-internal point is fixed, as
the design itself prescribes ("fixed before counting"):
the crosswalk fixing and the trained-set freeze happen
inside step 0 at execution, from the files named in
§§3–4, and the step-0 record is written and hashed
before any counting begins.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
