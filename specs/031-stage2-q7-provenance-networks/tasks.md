# Spec 031 — Tasks

> ## PLAN — FOR FREEZE — 2026-10-13
>
> Adjudication input is recorded in `adjudication.md`
> (the 2026-10-12 adopted asks 1B/2B/3A/4A/5A/6A plus
> the owner's 2026-10-13 design-and-freeze order).
> Execution tasks for Phase-395 are listed for shape
> only and remain gated on a separate owner order
> after the freeze merges and the OSF registration
> verifies public.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and
      claim register checked against constitution
      §§I–VIII and governance H2, H6, H13, H15/H23;
      Spec 027 §10 hard limits carried into spec §8
      verbatim in substance.
- [x] **L2 — Claims-first register.** `claims.json`
      (F031-C01…C12) drafted in the Spec 028/030
      register shape; framework026 dependency
      integrity verified clean (no cycles, no missing
      dependencies, no forbidden inheritance).
- [ ] **L3 — AEE hooks.** AEE assess +
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
      register integrity, and the D8 margins.
- [x] **L6 — Freeze PR merged**, house gates green
      (foundation 0 failures, full suite, branding
      sweep).
- [ ] **L7 — OSF registration filed** for the frozen
      contract (adopted 6A); registration record
      follows once the approval verifies public with
      a minted DOI.

## Execution (Phase-395) — NOT ORDERED

- [x] **E1 — Graph-first build** (FR-027-13): script,
      graph module, registration, registration
      verification, then run.
- [x] **E2 — Digitisation design step:** per-source
      posture assignments; D8 residual (ii)
      appendix re-verification; method split of the
      other-site determinations.
- [x] **E3 — Margins step:** eligibility and
      viability per arm; population record written
      and hashed before any response is computed;
      arm closures under spec §§4.2/4.3 recorded.
- [x] **E4 — Outcome step:** controls, primary
      tests, labelled sensitivity, jackknife,
      verdicts per spec §5.2; outcome recorded in
      this spec and cross-recorded under Spec 027;
      nothing written into Stage 1 or Spec 028
      records.
