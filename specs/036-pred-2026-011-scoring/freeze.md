# Spec 036 — Freeze Record (PRED-2026-011: scoring the screened clean-withholding successor)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-20
>
> This record is finalised at the freeze act.
> The digest in `freeze.json` at this draft is a
> **draft digest**, computed by `build_freeze.py`
> over this draft contract (register 0.5-draft)
> under the owner's draft order of 2026-10-20
> (`adjudication.md`). At the freeze act — on the
> owner's freeze order — the AEE lifecycle hooks
> run over the register first, and the digest is
> recomputed **exactly once** over the recovered
> register and the finalised freeze texts (the
> Spec 035 ordering). The draft digest decides
> nothing and is not the freeze digest.

## 1. Basis

The contract implemented is the PRED-2026-011
registration of 2026-10-20
(`docs/PREDICTION_REGISTER.md`), with its trained
set derived at registration, screened under the
registered rule, and frozen by hash
(`docs/research/pred-2026-011-registration/derivation-record.json`).
The prediction's OSF preregistration (t6whq, DOI
10.17605/OSF.IO/T6WHQ) was verified accepted and
public at the draft (`osf-registration.md`) and
is re-verified at execution step 0.

The §0.4 coverage expectation is part of this
basis: under the fixed crosswalk reading, both
trained signs carry confirmed best-match
counterparts (P217 → Y0520, confidence 1.0;
P324 → Y0740, confidence 0.9867), so step 0 is
expected to pass in full and execution to reach
the scoring — the first scored verdict of the H3
line, CONFIRMED or NOT CONFIRMED on the exact
two-sign criterion, unless an earlier check
closes the study. The expectation is a
draft-stage observation over the public
crosswalk, not a step-0 determination; the
freeze decision is taken knowing it either way.

The freeze also decides the open design proposal
(`adjudication.md` §3): **DD-036-4** — whether
this frozen spec files its own OSF contract
registration (the Spec 032–034 pattern; the
proposal is to follow Spec 035's DD-035-4
decision, YES). The zero-occurrence rule is not
an open decision: it is registered text
(DD-036-2).

## 2. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/036-pred-2026-011-scoring/freeze.md` (this
  document)
- `specs/036-pred-2026-011-scoring/spec.md`
- `specs/036-pred-2026-011-scoring/claims.json`
- `specs/036-pred-2026-011-scoring/adjudication.md`
- `specs/036-pred-2026-011-scoring/osf-registration.md`
- `specs/036-pred-2026-011-scoring/aee/freeze-aee-note.md`
- `specs/036-pred-2026-011-scoring/build_freeze.py`
- `backend/tests/test_spec036_freeze.py`

`plan.md`, `tasks.md`, and `outcome.md` are
lifecycle bookkeeping and are not digest-covered
(the house rule since Spec 026: plans change as
work proceeds).

## 3. What the freeze would fix

- **The criterion** (spec §6 / F036-C02): at
  least 70% of the trained INITIAL signs at
  Harappa start rate at least 0.40; with 2 signs,
  only 2 of 2 passes. CONFIRMED / NOT CONFIRMED
  are the only verdicts; no band is added.
- **Step 0, fail-closed, in a fixed order** (spec
  §3): registration re-verification; input
  integrity; training-pool and screen
  re-verification; crosswalk coverage. The
  withheld file's content is opened only after
  all four pass.
- **The trained set and the screen** (spec §2 /
  F036-C03): {P217, P324}, derived from the CISI
  Mohenjo-daro pool only and screened under the
  registered rule; P000's exclusion is a screen
  outcome, reproduced at step 0, never revisited.
- **The counterpart reading** (DD-036-5): the
  frozen Phase-396 build's reading — best-match
  rows carry identity; top-3 alternatives set
  conflict flags only.
- **Register handling at execution** (spec §7):
  dated append; on a verdict the §3 Tested/Outcome
  fields move in the same append, on a closure
  they stay PENDING; PRED-2026-006 and
  PRED-2026-010 stay byte-identical and unscored.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
