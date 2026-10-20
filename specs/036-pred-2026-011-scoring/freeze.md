# Spec 036 — Freeze Record (PRED-2026-011: scoring the screened clean-withholding successor)

> ## FROZEN at the Spec 036 freeze merge (2026-10-20)
>
> Basis: the owner's do-all order of 2026-10-20,
> verbatim **"do all of spec 036 now"**
> (`adjudication.md` §4), which orders the full
> Spec 036 arc — freeze, the spec-level OSF
> contract registration, and Phase-400 execution —
> in one act. The governed claim register passed
> the AEE lifecycle hooks at after_specify,
> after_plan, and after_tasks after five recorded
> rounds at after_specify (10, then 3, then 1,
> then 1, then 0 failure modes;
> `aee/recovery-specify.md`) — the freeze digest
> recorded in `freeze.json` (framework026 digest,
> built by `build_freeze.py` from the DEFINITION
> and SOURCES it carries) covers the recovered
> register (0.9-draft), never the pre-recovery
> draft.

## 1. Basis

The contract implemented is the PRED-2026-011
registration of 2026-10-20
(`docs/PREDICTION_REGISTER.md`), with its trained
set derived at registration under the disclosed
mappability screen and fixed by reference from
the derivation record
(`docs/research/pred-2026-011-registration/derivation-record.json`).
The prediction's OSF preregistration (t6whq, DOI
10.17605/OSF.IO/T6WHQ) was verified accepted and
public at the draft (`osf-registration.md`) and
is re-verified at execution step 0.

The §0.4 coverage observation is part of this
basis: under the fixed crosswalk reading, both
trained signs carry confirmed best-match
counterparts (P217 → Y0520; P324 → Y0740), so
execution is expected to pass step 0 in full
and the scoring to run — the opposite of the
Spec 035 expectation, where the freeze was
taken knowing execution would close at step
0.4. The freeze decision was taken knowing
that, on the owner's order. The scoring outcome
itself is not known: no Harappa count or start
rate has been taken for either sign.

The freeze also decides the open design
questions (`adjudication.md` §4): **DD-036-2 is
registered text carried, not a design decision**
(a mappable trained sign with zero Harappa
occurrences counts as not meeting the bar), the
draft-fixed readings **stand** (DD-036-1,
DD-036-3, DD-036-5), and **DD-036-4 is decided
YES**: this frozen spec files its own OSF
contract registration (the Spec 032–034
pattern), recorded in `osf-spec-registration.md`
and completed by append once its approval
verifies.

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`,
computed by `build_freeze.py` in this
directory). Covered sources (nothing else
decides the question):

- `specs/036-pred-2026-011-scoring/freeze.md` (this
  document)
- `specs/036-pred-2026-011-scoring/spec.md`
- `specs/036-pred-2026-011-scoring/claims.json`
- `specs/036-pred-2026-011-scoring/adjudication.md`
- `specs/036-pred-2026-011-scoring/osf-registration.md`
- `specs/036-pred-2026-011-scoring/aee/freeze-aee-note.md`
- `specs/036-pred-2026-011-scoring/build_freeze.py`
- `backend/tests/test_spec036_freeze.py`

`plan.md` and `tasks.md` are lifecycle bookkeeping
and are not digest-covered (the house rule since
Spec 026: plans change as work proceeds).

## 3. What the freeze fixes

- **The criterion** (spec §6 / F036-C02): at least
  70% of the trained INITIAL signs at Harappa
  start rate at least 0.40; with 2 signs, only
  2 of 2 passes. CONFIRMED / NOT CONFIRMED are the
  only verdicts; no band is added.
- **Step 0, fail-closed, in a fixed order** (spec
  §3 / DD-036-1): registration re-verification;
  input integrity against the four registered
  pins; training-pool re-verification reproducing
  the unscreened classification exactly and the
  registered screen returning {P217, P324};
  crosswalk coverage under the fixed reading
  (DD-036-5). The withheld file's content is
  opened only after all four pass.
- **The closures** (F036-C09, F036-C15): any
  unmappable trained sign (50% > the registered
  20% cap) closes the scoring as CANNOT BE RUN AS
  WRITTEN before the withheld file is opened; a
  closure is reported as itself, never as a
  verdict, and is not a refutation.
- **The computation** (spec §5 / F036-C10), the
  zero-occurrence rule (F036-C11 / DD-036-2, the
  registered text carried), the descriptive
  per-sign table (F036-C12), the verdict wording
  and its disclosure (F036-C07, F036-C13), and the
  register handling (F036-C14).

## 4. What execution must satisfy (Phase-400)

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
  OSF registration (t6whq), the four input pins,
  the training pool, the classification, and the
  screen, and the crosswalk coverage — with the
  step-0 record written and hashed before any
  scoring. The spec-level OSF registration filed
  under DD-036-4 is recorded by append in
  `osf-spec-registration.md`; step 0's
  registration check is t6whq, as frozen in
  spec §3.

## 5. What this freeze does not do

It scores nothing, opens no withheld content, and
computes no Harappa count or start rate.
Execution is Phase-400, under the execution
order recorded above. It does not touch any
other frozen record (Specs 026–035), the
PRED-2026-006 or PRED-2026-010 records, or any
other prediction's state.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
