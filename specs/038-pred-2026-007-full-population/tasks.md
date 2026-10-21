# Spec 038 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Adjudication input is recorded in
> `adjudication.md` (the owner's draft order of
> 2026-10-20, drafting only; the freeze
> coordinator's three Stage-0 flags, disposed
> of in §3 of that record). The freeze and the
> execution tasks for Phase-401 (provisional)
> remain gated on the owner's separate
> decisions; execution is additionally gated on
> step 0 of the spec, in the frozen order.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan,
      and claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the registered test), H13 (epistemic
      boundaries stated in spec §§8–9),
      H15/H23 (execution shape is graph-first,
      spec §10), H21 (foundation check named at
      execution). The registered facts and the
      cited sources were verified by form and
      hash against the record on `main`
      (`adjudication.md` §2); no source was read
      for ITM membership.
- [x] **L2 — Claims-first register.**
      `claims.json` (F038-C01…C14) drafted in
      the Spec 032–036 register shape.
      Draft-stage self-check: the
      dependency-integrity checks and the
      cited-record facts are pinned by
      `backend/tests/test_spec038_freeze.py`;
      the AEE lifecycle hooks have **not** run
      on this register (L3).
- [x] **L3 — Coordinator flags disposed.** The
      three Stage-0 design-integrity flags
      (denominator arithmetic; cluster-class
      rule provenance; code-table provenance)
      are disposed of explicitly in
      `adjudication.md` §3 and carried into the
      spec (DD-038-1, DD-038-9, DD-038-5).
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE —
      not run on this draft).** At the freeze
      act, run `run_aee.py assess` after_specify,
      after_plan, and after_tasks over the claim
      register **under aee 1.5.0** (DD-038-7);
      the gate is **pass**, and a stricter
      outcome blocks the freeze until its named
      recovery is complete and recorded.
      Deliberate ordering (the Spec 035/036
      record): any recovery round changes claim
      text, and the freeze digest is computed
      over the recovered register exactly once,
      at freeze.
- [x] **L5 — Design PR.** This draft, opened as
      a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state reported
      from run conclusions.
- [x] **L6 — Freeze.** On the owner's freeze
      order: hooks pass (L4), `freeze.md`
      finalised, `freeze.json` recomputed over
      the recovered register and the finalised
      freeze texts; freeze tests pin the digest
      replay, the definition constants, the
      register integrity, and the cited records.
      DD-038-6 decided at the freeze (proposal:
      file the spec's own OSF contract
      registration). Phase number confirmed
      (DD-038-8).
- [ ] **L7 — Freeze PR merged**, house gates
      green (foundation 0 failures, full suite,
      branding sweep).

## Execution (Phase-401, provisional) — gated on the freeze and a separate execution order

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [x] **E2 — Step 0** (spec §3), in the frozen
      order: 0.1 sources and provenance (primary
      and cross-check verified and hashed; the
      conflict rule in force; the reconciliation
      note drafted for append); 0.2 enumeration
      (mechanical read of the primary's
      `icit_function` field over all its
      per-sign records; record-count
      reconciliation; cross-check run;
      discrepancies recorded) — the enumeration
      written and hashed before any Phase 5
      lookup; 0.3 Phase 5 output verification
      (recorded output present in
      sign-assignable form; the three named
      assignments reproduced). Any failure
      closes the study as recorded in §3,
      unscored — except the census branch (§6),
      which completes.
- [ ] **E3 — Scoring** (spec §5): NOT REACHED — the study closed at step 0.2 (see outcome.md). The registered
      computation only, under the cluster-class
      operationalisation (DD-038-9) and the
      coverage rule (§6); the per-sign table
      produced with it. (Reached only if step 0
      passes in full.)
- [x] **E4 — Outcome:** the verdict under spec
      §6, the census completion, the
      partial-scope record, or the closure,
      reported as itself; the register appends
      (spec §7, including the provenance
      reconciliation note), the outcome record
      in this spec's directory, the root LEDGER
      entry, and the foundation check (H21);
      nothing written into any frozen record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
