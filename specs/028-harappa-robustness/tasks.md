# Spec 028 — Tasks

> ## FROZEN UNDER DELEGATED ADJUDICATION — 2026-10-11
>
> Adjudication is recorded in `adjudication.md` (owner's
> delegated-design order, verbatim). Execution tasks remain
> gated on the freeze merge and the OSF registration, in
> that order (spec §3.1). No task in this file is an
> execution authorization by itself.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and claim
      register checked against constitution §§I–VIII and
      governance H2, H6, H13, H15/H23. Recorded in spec §10
      and plan §4.
- [x] **L2 — Specify.** `spec.md` and structured
      `claims.json` (16 governed claims) authored; register
      integrity verified with Spec 026
      `framework026.check_dependency_integrity`: no cycles,
      no missing dependencies, no forbidden inheritance.
- [x] **L3 — Adjudication record.** The owner's delegated
      order and the program's design decisions recorded in
      `adjudication.md`.
- [x] **L4 — Margins-only audit.** `build_margins_audit.py`
      → `margins-audit.json`: Phase-392 frozen counts
      reproduced exactly (eligible 3,144; analysis 3,030;
      Arm A 1,593; 125 columns); both arms ESTIMABLE on
      margins; no outcome field.
- [x] **L5 — Synthetic calibration.** `build_calibration.py`
      through `pipeline393.py` → `calibration.json`. The
      first calibration attempts exposed a defect in the
      Phase-392 control construction: with one synthetic
      population rarefied 199 times, Arm A's negative
      control rejection share was a generation-seed lottery
      (0.171/0.156 in the calibration attempts; 0.015/0.000
      under a second seed in the confirming diagnostic).
      Controls were rebuilt to regenerate the synthetic
      population per draw (shares returned to nominal:
      0.050/0.035/0.070 in the diagnostic), and the
      permutation strata were refined to type class ×
      legible-length value; final calibration PASSes both
      arms' controls. Recorded as freeze Amendment 1.
- [x] **L6 — Plan, checklist, tasks.** `plan.md`,
      `checklists/requirements.md`, this file.
- [x] **L7 — AEE hooks.** AEE assess + evaluator-contract
      outputs after specify, plan, and tasks saved under
      `aee/`; outcomes recorded in `aee/` notes.
- [x] **L8 — Freeze.** `freeze.md` + `freeze.json`
      (framework026 digest via `build_freeze.py`) + freeze
      tests (`backend/tests/test_phase393_freeze.py`).
- [ ] **L9 — Freeze PR.** Opened, CI verified from the
      run's own conclusion and job logs, merged. Ledger
      entries appended in both program ledgers.

## Registration gate

- [ ] **R1 — OSF registration.** The frozen contract
      registered on OSF (public, no embargo) after the
      freeze merge and before any execution; URL and filing
      timestamp recorded in `osf-registration.md` and both
      ledgers (separate PR).

## Execution — Phase-393 (after L9 + R1)

- [ ] **E1 — Script.** `backend/scripts/phase393_harappa_
      robustness.py`: asserts input hashes, reproduces the
      frozen populations (mismatch → INVALID, stops),
      runs Arms A/B/C exactly as frozen, writes
      `reports/phase393_results.json` +
      `reports/phase393_report.md`. The pipeline section is
      a verbatim copy of `pipeline393.py`'s; a test asserts
      the identity.
- [ ] **E2 — Graph module.** `backend/glossa_lab/
      experiment_graph_phase393.py` with the Phase-393
      AtomicNodeDef (H15).
- [ ] **E3 — Registration.** Node registered in
      `experiment_graph.py` via try/except import block;
      registration verified by import assertion (H23
      steps 1–4 complete before any run).
- [ ] **E4 — Run.** Execute once under the freeze; no
      frozen rule, constant, or threshold changed.
- [ ] **E5 — Outcome record.** Per-arm verdicts under
      spec §5.5 applied mechanically; decisive numbers
      recomputed from the results JSON; side-by-side
      statement with Phase-392; `historical-assessment-
      phase392.md` if a verdict changes Phase-392's
      reading; deviations recorded. Ledger entries in both
      program ledgers.

## Closeout

- [ ] **X1 — Verification on merged main.** Full backend
      suite and foundation check (0 failures); anchors
      byte-identical (sha256); PRED register untouched.
- [ ] **X2 — Boundaries.** No external send or deposit
      beyond the R1 registration; no Spec 027 artifact
      modified; no pooled cross-arm headline anywhere.
