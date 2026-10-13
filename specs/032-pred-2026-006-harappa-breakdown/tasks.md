# Spec 032 — Tasks

> ## PLAN — FOR FREEZE — 2026-10-13
>
> Adjudication input is recorded in `adjudication.md`
> (the design commission of 2026-10-13 and the owner's
> freeze order of 2026-10-13 06:39 EDT). Execution
> tasks for Phase-396 are listed for shape only and
> remain gated on the OSF registration of this frozen
> contract verifying public.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and
      claim register checked against constitution
      §§I–VIII and governance H2, H6, H13, H15/H23,
      H26; the register's own rules carried into the
      spec verbatim in substance.
- [x] **L2 — Claims-first register.** `claims.json`
      (F032-C01…C12) drafted in the Spec 028/030/031
      register shape; framework026 dependency
      integrity verified clean (no cycles, no missing
      dependencies, no forbidden inheritance).
- [x] **L3 — AEE hooks.** AEE assess +
      evaluator-contract pass at after_specify,
      after_plan, and after_tasks over the register;
      artifacts saved under `aee/`. The gate is
      **pass**; a stricter outcome blocks the freeze
      until its named recovery is complete and
      recorded.
- [x] **L4 — Design PR merged** (spec, claims,
      adjudication, plan, tasks, AEE artifacts,
      LEDGER entry), CI green from run conclusions.
- [x] **L5 — Freeze.** `freeze.md` + `freeze.json`
      via `build_freeze.py`; freeze tests pin the
      digest replay, the definition constants, the
      register integrity, the withheld-data census,
      and the register text.
- [ ] **L6 — Freeze PR merged**, house gates green
      (foundation 0 failures, full suite, branding
      sweep).
- [ ] **L7 — OSF registration filed** for the frozen
      contract; the registration-record PR is left
      open with the pending state and completed by
      append once the approval verifies public with a
      minted DOI.

## Execution (Phase-396) — gated on the verified registration

- [ ] **E1 — Graph-first build** (H15/H23): script,
      graph module, registration, registration
      verification, then run.
- [ ] **E2 — Step 0:** trained-set reconstruction and
      freeze; withholding verification; crosswalk
      fixing; the step-0 record written and hashed
      before any counting. A step-0 failure closes
      the study under spec §3 and the closure is the
      outcome.
- [ ] **E3 — Scoring:** the registered computation
      only (spec §5); the per-sign table produced
      with it.
- [ ] **E4 — Outcome:** the verdict under spec §6,
      appended to the PRED register as a dated entry
      (spec §7), recorded in this spec's directory
      and the root LEDGER; nothing written into any
      frozen record.
