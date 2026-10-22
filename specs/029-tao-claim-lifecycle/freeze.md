# Spec 029 — Freeze Record (Tao Claim Lifecycle)

> ## FROZEN at the Spec 029 freeze merge (2026-10-12)
>
> Basis: Spec 029 as adjudicated by the owner
> (`adjudication.md` — OD-1…OD-6 ratified as a block
> 2026-10-12, plus the same-day addendum ratifying the
> audit's §9 items D-A, D-B, D-D, D-E into scope; D-C
> excluded and executed separately). The governed claim
> register enters this freeze as recovered under the
> owner-authorized L3 recovery (PR #167; record:
> `aee/recovery-specify.md`) — the freeze digest below
> covers the recovered register, never the pre-recovery
> one. The machine freeze record is `freeze.json`
> (framework026 digest, built by `build_freeze.py`).

## 1. What is frozen

- **The design.** `spec.md` (FR-029-01…12) as
  adjudicated: the five-stage lifecycle
  (created / checked / explained / accepted / digested,
  OD-4 verbatim names), the automation cap at `checked`,
  bundle decomposition with the attribution sub-claim
  and the OD-3 contested cap, the OD-2 explanation
  gate and OD-5 digestion threshold, lane-separated
  display with the mandatory remaining-unknowns
  statement, the OD-6 priority register, and per-record
  evidence trails.
- **The governed claim register.** `claims.json`,
  register_version `draft-2`: 13 claims
  (F029-C01…C13), recovered at L3 — the AEE hook pass
  over this register returns **pass** at after_specify,
  after_plan, and after_tasks (13 claims, 0 failure
  modes, 0 below the 0.70 threshold; `aee/` artifacts).
- **The re-staging source of truth.**
  `reclassification-ledger.json` (345 entries), whose
  §3 counts the Phase D migration must reproduce
  exactly and which freeze tests pin:
  anchors 193 created / 94 checked; extracted claims
  21 / 10; PRED-2026 live 3 / 2; hypothesis models
  3 created; study headlines 10 checked — totals
  **220 created / 116 checked / 0 explained /
  0 accepted / 0 digested**, with **105**
  `verified_unexplained` flags.
- **The work order.** `plan.md` and `tasks.md` as
  merged (PR #165) with the L3 recovery outcome
  appended. Implementation phases A–J, E1, E2, G run
  in the tasks.md order, each under its phase gate.

## 2. Bookkeeping rule for the frozen bytes

`plan.md` and `tasks.md` are digest-covered as frozen.
Phase completion during implementation is recorded in
phase records in this directory and in the program
ledgers (root `LEDGER.md`), **not** by editing the
frozen files. Checkbox ticks for F1/F2 and phases
A–X are applied in a single closeout pass (task X2),
which is recorded as a freeze amendment in the
closeout record; the freeze itself is never
regenerated (Spec 026 §4.7). The design sources
(spec.md, claims.json, adjudication.md, assessment.md,
audit.md, reclassification-ledger.json) are not
bookkeeping: any change to them after this freeze is
a design change requiring a new owner adjudication.

## 3. Tooling pins

- AEE package **1.0.4** (Glossa venv, PATH-pinned for
  every AEE run); AEE extension v1.1.0; evaluator
  extension v1.0.0; specify CLI 1.0.10; Python 3.12.3.
- Freeze machinery: `glossa_lab.framework026`
  (`build_freeze` / `verify_freeze` /
  `check_dependency_integrity`).

## 4. What this freeze does not do

It changes no live record, display, or score. The
OD-1 re-staging of existing records happens only in
Phase D, mechanically, from the frozen ledger. The
audit's historical-limitation labels (audit.md §7)
stand as published and are not amended by this
freeze.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
