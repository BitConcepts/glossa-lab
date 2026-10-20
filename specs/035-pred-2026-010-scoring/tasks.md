# Spec 035 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Adjudication input is recorded in
> `adjudication.md` (the owner's draft order of
> 2026-10-20, drafting only). The freeze and the
> execution tasks for Phase-399 remain gated on
> the owner's separate decisions; execution is
> additionally gated on step 0 of the spec, in the
> frozen order.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and
      claim register checked against constitution
      §§I–VIII and governance H2 (spec before
      code), H6 (no scope beyond the registered
      test), H13 (epistemic boundaries stated in
      spec §§8–9), H15/H23 (execution shape is
      graph-first, spec §10), H21 (foundation
      check named at execution). The registered
      facts were verified against the register,
      the derivation record, the pinned bytes on
      `main`, and the OSF API at draft time
      (`adjudication.md` §2).
- [x] **L2 — Claims-first register.** `claims.json`
      (F035-C01…C15) drafted in the Spec
      032/033/034 register shape. Draft-stage
      self-check: the dependency-integrity checks
      (no cycles, no missing dependencies, no
      forbidden inheritance) replicated over the
      register JSON and clean; the freeze runs the
      framework026 machinery itself (L5).
- [x] **L3 — AEE hooks.** AEE assess +
      evaluator-contract pass at after_specify,
      after_plan, and after_tasks over the
      register. **Not run at draft** (recorded in
      `aee/freeze-aee-note.md`); a freeze gate —
      the gate is **pass**, and a stricter outcome
      blocks the freeze until its named recovery
      is complete and recorded. Run at the freeze
      act, 2026-10-20: **pass** at all three hooks
      over register 0.8-draft after four recorded
      recovery rounds at after_specify
      (`aee/recovery-specify.md`).
- [x] **L4 — Design PR.** This draft, opened as a
      DRAFT PR (#218) and left unmerged for the
      owner's freeze decision, CI green from run
      conclusions.
- [x] **L5 — Freeze.** On the owner's freeze
      order (2026-10-20, "go with your
      recommendation"): hooks pass (L3),
      `freeze.md` finalised, `freeze.json`
      recomputed over the recovered register and
      the finalised freeze texts; freeze tests pin
      the digest replay, the definition constants,
      the register integrity, and the cited records
      (derivation record, register entry, crosswalk
      observation). DD-035-2 stands as drafted;
      DD-035-4 decided YES (the spec files its own
      OSF contract registration).
- [x] **L6 — Freeze PR merged**, house gates green
      (foundation 0 failures, full suite, branding
      sweep). PR #218 merged `b481a866`, CI 7/7 green
      from run conclusions.
- [x] **L7 — Registration state.** The
      prediction's OSF preregistration (wjebq,
      DOI 10.17605/OSF.IO/WJEBQ) verified accepted
      and public by API at draft
      (`osf-registration.md`). A spec-level
      registration, if the freeze files one
      (DD-035-4), is recorded by append once its
      approval verifies.

## Execution (Phase-399) — gated on the freeze and a separate execution order

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [x] **E2 — Step 0** (spec §3), in the frozen
      order: 0.1 registration re-verification;
      0.2 input integrity; 0.3 training-pool
      re-verification (filter, census, manifest
      hash, verbatim classification reproducing
      {P000, P217, P324} exactly); 0.4 crosswalk
      coverage under the fixed reading (DD-035-5).
      Any failure closes the study as recorded in
      §3, unscored; the step-0 record is written
      and hashed before any scoring. On the
      draft-stage observation, 0.4 is expected to
      close the study (P000 unmappable, 33% > 20%).
- [ ] **E3 — Scoring** (spec §5): **NOT REACHED** —
      step 0 closed the study at check 0.4
      (`outcome.md`); the registered
      computation only; the per-sign table
      produced with it. (Reached only if step 0
      passes in full.)
- [x] **E4 — Outcome:** the verdict under spec §6
      or the closure under §3, reported as itself;
      the register append (spec §7), the outcome
      record in this spec's directory, the root
      LEDGER entry, and the foundation check
      (H21); nothing written into any frozen
      record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
