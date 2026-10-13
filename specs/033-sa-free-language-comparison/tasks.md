# Spec 033 — Tasks

> ## PLAN — FOR FREEZE — 2026-10-13
>
> Adjudication input is recorded in `adjudication.md`
> (the design commission of 2026-10-13 and the owner's
> freeze order of 2026-10-13 06:39 EDT). Execution
> tasks for Phase-397 are listed for shape only and
> remain gated on the OSF registration of this frozen
> contract verifying public.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and
      claim register checked against constitution
      §§I–VIII and governance H2, H6, H13, H15/H23,
      H26; the design's SA-free construction (H26)
      verified against every pipeline element.
- [x] **L2 — Claims-first register.** `claims.json`
      (F033-C01…C15) drafted in the Spec 028/030/031
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
      register integrity, the strict-set census, and
      the recorded original margins.
- [ ] **L6 — Freeze PR merged**, house gates green
      (foundation 0 failures, full suite, branding
      sweep).
- [ ] **L7 — OSF registration filed** for the frozen
      contract; the registration-record PR is left
      open with the pending state and completed by
      append once the approval verifies public with a
      minted DOI.

## Execution (Phase-397) — gated on the verified registration

- [ ] **E1 — Graph-first build** (H15/H23): script,
      graph module, registration, registration
      verification, then run.
- [ ] **E2 — Anchor freeze:** both pre-registered
      anchor lists written as cited data (family,
      sign, published value, source) and hashed
      before any scoring.
- [ ] **E3 — Scoring:** the frozen pipeline (spec §5)
      over the families, both controls, the
      robustness arm, and the Harappa-removed
      sensitivity.
- [ ] **E4 — Outcome:** the verdict under spec §6,
      recorded in this spec's directory and the root
      LEDGER, with the claim-status consequence
      appended as a dated entry to the claim's
      record; nothing written into any frozen record.
