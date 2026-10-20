# Spec 035 — Freeze Record (PRED-2026-010: scoring the clean-withholding successor)

> ## FROZEN at the Spec 035 freeze merge (2026-10-20)
>
> Basis: the owner's freeze-and-execute order of
> 2026-10-20, verbatim **"go with your
> recommendation"** (`adjudication.md` §4),
> adopting the recommendation put to the owner the
> same day: freeze this contract and execute it,
> buying the formal step-0 record. The governed
> claim register passed the AEE lifecycle hooks at
> after_specify, after_plan, and after_tasks after
> four recorded recovery rounds at after_specify
> (30, then 9, then 8, then 0 failure modes;
> `aee/recovery-specify.md`) — the freeze digest
> recorded in `freeze.json` (framework026 digest,
> built by `build_freeze.py` from the DEFINITION
> and SOURCES it carries) covers the recovered
> register (0.8-draft), never the pre-recovery
> draft.

## 1. Basis

The contract implemented is the PRED-2026-010
registration of 2026-10-13
(`docs/PREDICTION_REGISTER.md`), with its trained
set derived at registration and frozen by hash
(`reports/pred010_derivation_record.json`). The
prediction's OSF preregistration (wjebq, DOI
10.17605/OSF.IO/WJEBQ) was verified accepted and
public at the draft (`osf-registration.md`) and
is re-verified at execution step 0.

The §0.4 coverage observation is part of this
basis: under the fixed crosswalk reading, P000
carries no best-match counterpart, so execution
is expected to close at step 0.4 as CANNOT BE RUN
AS WRITTEN, unscored. The freeze decision was
taken knowing that, on the owner's order.

The freeze also decides the two open design
decisions (`adjudication.md` §4): **DD-035-2
stands as drafted** (a mappable trained sign
with zero Harappa occurrences counts as not
meeting the bar), and **DD-035-4 is decided
YES**: this frozen spec files its own OSF
contract registration (the Spec 032–034
pattern), recorded in `osf-spec-registration.md`
and completed by append once its approval
verifies.

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
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

## 3. What the freeze fixes

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

## 4. What execution must satisfy (Phase-399)

- This freeze PR merged with house gates green
  (foundation check 0 failures, full backend
  suite, branding sweep, CI from run conclusions).
- The AEE hook pass over the register at
  after_specify / after_plan / after_tasks,
  gate **pass** — satisfied at this freeze act
  and recorded (`aee/freeze-aee-note.md`,
  `aee/recovery-specify.md`).
- The owner's execution order — given in the
  same act as the freeze order (above).
- Step 0 (spec §3) re-verifying, in order: the
  OSF registration (wjebq), the four input pins,
  the training pool and trained set, and the
  crosswalk coverage — with the step-0 record
  written and hashed before any scoring. The
  spec-level OSF registration filed under
  DD-035-4 is recorded by append in
  `osf-spec-registration.md`; step 0's
  registration check is wjebq, as frozen in
  spec §3.

## 5. What this freeze does not do

It scores nothing, opens no withheld content, and
computes no Harappa count or start rate.
Execution is Phase-399, under the execution
order recorded above. It does not touch any
other frozen record (Specs 026–034), the
PRED-2026-006 record, or any other prediction's
state.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
