# Spec 034 — Tasks

> ## PLAN — FOR FREEZE — 2026-10-13
>
> Adjudication input is recorded in `adjudication.md`
> (the design commission of 2026-10-13 and the owner's
> freeze order of 2026-10-13 06:39 EDT). Execution
> tasks for Phase-398 are listed for shape only and
> remain gated on the OSF registration of this frozen
> contract verifying public.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and
      claim register checked against constitution
      §§I–VIII and governance H2, H6, H13, H15/H23,
      H21; the design's fixed gate and lines verified
      against the Phase-125/127/131 and Phase-124
      records at design time.
- [x] **L2 — Claims-first register.** `claims.json`
      (F034-C01…C14) drafted in the Spec 028/030/031
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
      register integrity, and the cited Phase
      records.
- [ ] **L6 — Freeze PR merged**, house gates green
      (foundation 0 failures, full suite, branding
      sweep).
- [ ] **L7 — OSF registration filed** for the frozen
      contract; the registration-record PR is left
      open with the pending state and completed by
      append once the approval verifies public with a
      minted DOI.

## Execution (Phase-398) — gated on the verified registration

- [ ] **E1 — Graph-first build** (H15/H23): script,
      graph module, registration, registration
      verification, then run.
- [ ] **E2 — Step 0 bridge:** the three routes as
      cited data; the bridge census published; the
      gate applied. Below the gate, close as TOO
      THIN TO ATTRIBUTE and stop.
- [ ] **E3 — Step 1 measurement:** Phase-125's
      distance and floors on the matched subset;
      the Phase-131-category decomposition.
- [ ] **E4 — Outcome:** the attribution under spec
      §6 with the §7 selection-bias report in the
      verdict statement, recorded in this spec's
      directory and the root LEDGER; nothing written
      into the settled records.
