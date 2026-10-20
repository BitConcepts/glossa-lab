# Spec 035 — Draft Freeze Record (PRED-2026-010: scoring the clean-withholding successor)

> ## DRAFT — NOT FROZEN — 2026-10-20
>
> This document proposes the freeze. The freeze
> takes effect only under the owner's freeze order
> and the freeze PR's merge; until then Spec 035 is
> a design draft, its digest below is a **draft
> digest** over the draft texts, and nothing in it
> authorises any run. If the freeze act changes any
> covered text — the AEE recovery rounds are the
> expected cause — the digest is recomputed in the
> freeze PR and this document is finalised there,
> by append where the house pattern requires it.

## 1. Basis

The owner's draft order of 2026-10-20 (drafting
only), recorded in `adjudication.md`. The contract
implemented is the PRED-2026-010 registration of
2026-10-13 (`docs/PREDICTION_REGISTER.md`), with
its trained set derived at registration and frozen
by hash (`reports/pred010_derivation_record.json`).
The prediction's OSF preregistration (wjebq, DOI
10.17605/OSF.IO/WJEBQ) was verified accepted and
public at this draft (`osf-registration.md`).

The draft-stage coverage observation (spec §0.4)
is part of this basis: under the fixed crosswalk
reading, P000 carries no best-match counterpart,
so execution is expected to close at step 0.4 as
CANNOT BE RUN AS WRITTEN, unscored. The freeze
decision is taken knowing that.

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Its
**draft digest** is recorded in `freeze.json`
itself and reported with the draft PR. Covered
sources (nothing else decides the question):

- `specs/035-pred-2026-010-scoring/freeze.md` (this
  document)
- `specs/035-pred-2026-010-scoring/spec.md`
- `specs/035-pred-2026-010-scoring/claims.json`
- `specs/035-pred-2026-010-scoring/adjudication.md`
- `specs/035-pred-2026-010-scoring/osf-registration.md`
- `specs/035-pred-2026-010-scoring/aee/freeze-aee-note.md`
- `specs/035-pred-2026-010-scoring/build_freeze.py`
- `backend/tests/test_spec035_freeze.py`

`plan.md` and `tasks.md` are lifecycle bookkeeping
and are not digest-covered (the house rule since
Spec 026: plans change as work proceeds).

## 3. What the freeze would fix

- **The criterion** (spec §6 / F035-C02): at least
  70% of the trained INITIAL signs at Harappa
  start rate at least 0.40; with 3 signs, only
  3 of 3 passes. CONFIRMED / NOT CONFIRMED are the
  only verdicts; no band is added.
- **Step 0, fail-closed, in a fixed order** (spec
  §3 / DD-035-1): registration re-verification;
  input integrity against the four registered
  pins; training-pool re-verification reproducing
  {P000, P217, P324} exactly; crosswalk coverage
  under the fixed reading (DD-035-5). The
  withheld file's content is opened only after
  all four pass.
- **The closures** (F035-C09, F035-C15): any
  unmappable trained sign (33% > the registered
  20% cap) closes the scoring as CANNOT BE RUN AS
  WRITTEN before the withheld file is opened; a
  closure is reported as itself, never as a
  verdict, and is not a refutation.
- **The computation** (spec §5 / F035-C10), the
  zero-occurrence rule (F035-C11 / DD-035-2), the
  descriptive per-sign table (F035-C12), the
  verdict wording and its disclosure
  (F035-C07, F035-C13), and the register handling
  (F035-C14).

## 4. What execution must satisfy before anything runs

- The owner's freeze order, and the freeze PR
  merged with house gates green (foundation check
  0 failures, full backend suite, branding sweep,
  CI from run conclusions).
- The AEE hook pass over the register at
  after_specify / after_plan / after_tasks,
  gate **pass**, recovery rounds recorded
  (`aee/freeze-aee-note.md`).
- A separate owner execution order for
  Phase-399.
- Step 0 (spec §3) re-verifying, in order: the
  OSF registration (wjebq — and any spec-level
  registration the freeze files under DD-035-4),
  the four input pins, the training pool and
  trained set, and the crosswalk coverage — with
  the step-0 record written and hashed before any
  scoring.

## 5. What this draft does not do

It does not freeze anything, execute anything,
open the withheld file for content, compute any
Harappa count or start rate, file any OSF
registration, or edit the PRED register, the
derivation record, or any frozen record. It
leaves the freeze — and, after it, the execution
— to the owner's separate orders.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
