# Spec 036 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Adjudication input is recorded in
> `adjudication.md` (the owner's draft order of
> 2026-10-20, drafting only). The freeze and the
> execution tasks for Phase-400 remain gated on
> the owner's separate decisions; execution is
> additionally gated on step 0 of the spec, in
> the frozen order.

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
      (F036-C01…C15) drafted in the Spec
      032/033/034/035 register shape. Draft-stage
      self-check: the dependency-integrity checks
      and the cited-record facts are pinned by
      `backend/tests/test_spec036_freeze.py`; the
      AEE lifecycle hooks have **not** run on this
      register (L3).
- [x] **L3 — AEE lifecycle hooks (FREEZE GATE).** at the freeze act,
      run `run_aee.py assess` after_specify,
      after_plan, and after_tasks over the claim
      register; the gate is **pass**, and a
      stricter outcome blocks the freeze until its
      named recovery is complete and recorded.
      Deliberate ordering (the Spec 035 record):
      any recovery round changes claim text, and
      the freeze digest is computed over the
      recovered register exactly once, at freeze.
- [x] **L4 — Design PR.** This draft, opened as a
      DRAFT PR and left unmerged for the owner's
      freeze decision, CI green from run
      conclusions.
- [x] **L5 — Freeze.** On the owner's freeze
      order: hooks pass (L3), `freeze.md`
      finalised, `freeze.json` recomputed over
      the recovered register and the finalised
      freeze texts; freeze tests pin the digest
      replay, the definition constants, the
      register integrity, and the cited records
      (derivation record, register entry,
      crosswalk expectation). DD-036-4 decided at
      the freeze (proposal: file the spec's own
      OSF contract registration, following the
      DD-035-4 precedent).
- [ ] **L6 — Freeze PR merged**, house gates green
      (foundation 0 failures, full suite, branding
      sweep).
- [x] **L7 — Registration state.** The
      prediction's OSF preregistration (t6whq,
      DOI 10.17605/OSF.IO/T6WHQ) verified accepted
      and public by API at draft
      (`osf-registration.md`). A spec-level
      registration, if the freeze files one
      (DD-036-4), is recorded by append once its
      approval verifies.

## Execution (Phase-400) — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0** (spec §3), in the frozen
      order: 0.1 registration re-verification;
      0.2 input integrity; 0.3 training-pool and
      screen re-verification (filter, census,
      manifest hash, verbatim classification
      reproducing the unscreened set {P000, P217,
      P324} and the screen outcome {P217, P324}
      exactly); 0.4 crosswalk coverage under the
      fixed reading (DD-036-5). Any failure closes
      the study as recorded in §3, unscored; the
      step-0 record is written and hashed before
      any scoring. On the draft-stage expectation,
      all four checks pass (both trained signs
      carry confirmed best-match counterparts) and
      scoring is reached.
- [ ] **E3 — Scoring** (spec §5): the registered
      computation only; the per-sign table
      produced with it. (Reached only if step 0
      passes in full.)
- [ ] **E4 — Outcome:** the verdict under spec §6
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
