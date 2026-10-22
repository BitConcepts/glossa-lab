# Spec 036 — Plan

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Written against the governing record: the
> PRED-2026-011 registration in
> `docs/PREDICTION_REGISTER.md` (2026-10-20), its
> registration package
> (`docs/research/pred-2026-011-registration/`),
> and the Spec 032 / Phase-396 and Spec 035 /
> Phase-399 record sets that produced the
> successor. The owner's draft order of
> 2026-10-20 commissions this draft; the freeze
> and the execution (Phase-400) are separate
> owner decisions, and no task in `tasks.md` is
> itself an execution.

**Governing documents:** `spec.md`, `claims.json`,
and `adjudication.md` in this directory; the
PRED-2026-011 entry and the 2026-10-20 §6 notes in
`docs/PREDICTION_REGISTER.md`;
`docs/research/pred-2026-011-registration/derivation-record.json`;
`backend/scripts/pred011_register_derivation.py`;
`backend/scripts/phase396_pred006_step0.py` (the
frozen build carrying the classification logic and
the crosswalk reading verbatim);
`specs/035-pred-2026-010-scoring/` (spec, freeze,
outcome — the immediate precedent);
`specs/032-pred-2026-006-harappa-breakdown/`;
Spec 033/034 freeze records (house freeze
precedent); the Glossa constitution; governance
H1, H2, H6, H13, H15/H23, H21.

**Tooling record:** specify CLI 1.0.10 (setup and
extension management only); AEE extension v1.1.0;
evaluator extension v1.0.0; AEE package from the
Glossa venv first on PATH for every AEE invocation
(pinned `>=1.0.4,<1.5` per PR #181 — the 1.5.0
drift is a recorded, still-open owner decision
and is not touched by this draft).

## 1. Sequence

1. **Design PR** (this draft) — `spec.md`,
   `claims.json`, `adjudication.md`, `plan.md`,
   `tasks.md`, `osf-registration.md` (the
   verification record for the prediction's
   existing preregistration), `build_freeze.py` +
   `freeze.json` (the draft digest),
   `outcome.md` (the pre-written execution append
   skeleton — a skeleton only, nothing executed),
   the freeze test
   (`backend/tests/test_spec036_freeze.py`), the
   AEE note under `aee/`, and the LEDGER entry.
   Claims first. **AEE hooks have not run on this
   draft** (recorded in `aee/freeze-aee-note.md`):
   the hook pass (after_specify / after_plan /
   after_tasks) is a freeze gate, below — a
   deliberate ordering, not an omission, since
   any recovery round changes claim text and the
   digest must be computed over the recovered
   register exactly once, at freeze.
2. **Freeze PR** — on the owner's freeze order:
   AEE hook pass over the register (gate:
   **pass**, with any recovery rounds recorded in
   `aee/`), `freeze.md` finalised, `freeze.json`
   recomputed over the recovered register and the
   finalised freeze texts, and DD-036-4 decided
   (the proposal: file the frozen spec's own OSF
   contract registration, following the DD-035-4
   precedent). The freeze PR merges on green
   house gates; it executes nothing.
3. **Execution (Phase-400)** — on the owner's
   separate execution order: graph-first build
   (H15/H23); step 0 in the frozen order
   (registration re-verification; input integrity;
   training-pool and screen re-verification;
   crosswalk coverage), fail-closed, the step-0
   record written and hashed before any scoring;
   then the registered scoring and the per-sign
   table; the outcome (verdict or closure)
   appended to the PRED register and recorded in
   this directory, `outcome.md`, and the root
   LEDGER; the foundation check (H21) after the
   claim consequence lands. On the draft-stage
   expectation (spec §0.4), step 0 passes in full
   and the scoring runs; the expectation decides
   nothing.

## 2. What this plan never does

- It executes nothing at draft or at freeze; the
  execution is Phase-400, separately ordered.
- It opens no withheld content at any stage of
  the design; the withheld file's first content
  access is the execution's scoring step, after
  step 0 passes in full.
- It changes no register text, no derivation
  record, and no frozen Spec 026–035 record; the
  register consequence of any outcome lands only
  at execution, as a dated append (spec §7).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
