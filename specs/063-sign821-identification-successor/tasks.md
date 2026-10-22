# Spec 063 — Tasks

> ## PLAN — FROZEN 2026-10-21 (successor to Spec 056)
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's approval of
> 2026-10-21, amendment package Item 5; the
> authoritative draft, Amendment Queue
> Item 5, §§6.1, 7 and 8; Spec 056's frozen
> and executed record). **The freeze and the
> OSF filing were taken on 2026-10-21 under
> the owner's Item 5 approval (L4/L5/E1
> below); execution remains a separate
> later act, not authorised by the freeze.**

## Drafting (this draft)

- [x] **D1 — Predecessor record read in
      full.** Spec 056's `spec.md`,
      `claims.json`, `adjudication.md`,
      `tasks.md`, `freeze.json`,
      `osf-spec-registration.md`, and
      `outcome.md` with its extraction
      record: K-1's checklists (R-1, R-2,
      R-4, R-5 passed; R-3 failed), the R-3
      record, and the named unblocking act.
- [x] **D2 — Pins and facts re-verified two
      routes.** Every spec §2 pin re-derived
      by git-blob and contents-API raw at
      `main` `e03f7832…`, the routes agreeing
      byte-for-byte; registry and witness
      facts re-derived by parse; held-text
      locators re-derived; the thesis PDF's
      digest asserted on the local file.
- [x] **D3 — Preservation act.** The
      reference record of the amendment
      draft's §6.1 written as
      `drawn-form-reference-821.json` in this
      directory; its SHA-256 computed at
      commitment (`695dd35d…`) and pinned in
      spec §2 and the freeze. No images.
- [x] **D4 — This draft.** `spec.md`,
      `claims.json` (register 0.5-draft,
      F063-C01…C15), `adjudication.md`,
      `tasks.md`. Spec 056's directory is
      untouched.

## Lifecycle (freeze gate)

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance
      H2 (spec before code), H6 (no scope
      beyond the identification of sign 821
      for candidate K-1 — sign 297's
      successor is a separate spec), H13
      (epistemic boundaries stated in spec
      §10), H15/H23 (execution shape is
      graph-first, spec §13), H16 (data from
      the registered sources of record: the
      pinned held source document, registry,
      witness, Spec 056's records, the
      preserved reference, and the pinned
      local thesis file), H24 (no private
      correspondence in the repo), H26 (no
      semantic-anchoring machinery is used
      as a gate for anything in this spec —
      the identification is drawn-form
      matching against a recorded reference,
      with traps asserted).
- [x] **L2 — Claims-first register.**
      `claims.json` (F063-C01…C15) drafted in
      the Spec 056/062 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-063-8). Acceptance
      tests were derived twice independently;
      disagreements and resolutions are
      recorded in `adjudication.md` §5. The
      AEE lifecycle hooks have **not** run on
      this register at drafting (L4).
- [x] **L3 — Freeze PR.** This spec, opened
      as a PR for the freeze decision; CI
      state, when reported, is reported from
      the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE
      GATE).** DONE 2026-10-21 at the freeze
      act: `aee assess` (lenient load, aee
      1.5.3) run after_specify, after_plan,
      and after_tasks over the claim
      register, recovered to 0.6-draft first
      (the recovery record is in
      `aee/freeze-aee-note.md` and the
      register's own note). Final round at
      every hook: FR-2.3 draft-cap records
      only, zero correctness failure modes,
      no claim below the 0.70 threshold —
      **pass** on the DD-063-15 reading (the
      DD-038-10 reading).
- [x] **L5 — Freeze-decision items.** DONE
      2026-10-21 (`adjudication.md` §7):
      OP-063-1 decided DD-063-10 (Phase-425
      allocated, verified unallocated);
      OP-063-3 decided DD-063-11 (route 3,
      composition, adopted with its
      justification); OP-063-4 decided
      DD-063-12 (step-0 class names
      confirmed, including the thesis-file
      assertion before any plate read);
      OP-063-2 decided DD-063-9 (OSF
      registration filed at the freeze,
      E-1); OP-063-5 decided DD-063-13
      (freeze and filing taken; execution
      not authorised). DD-063-1…DD-063-8
      stand as drafted, none overturned.

## Execution (NOT authorised by this freeze; every step OWNER-APPROVAL)

- [x] **E1 — Freeze + OSF.** DONE
      2026-10-21: this contract is frozen
      (digest computed over the recovered
      register 0.6-draft exactly once, at
      freeze; `freeze.md` / `freeze.json`),
      and this spec's own OSF contract
      registration is filed under campaign
      decision E-1 (DD-063-9; filing record
      `osf-spec-registration.md`). The
      registration stands pending approval;
      execution (E2–E5) awaits its approval
      act and a separate execution order
      (DD-063-13).
- [ ] **E2 — Graph-first build** (H15/H23):
      script, graph node, registration,
      registration verification, for
      Phase-425. **OWNER-APPROVAL** (as part
      of the execution order).
- [ ] **E3 — Step 0** (spec §3): input
      integrity; thesis file asserted to its
      frozen digest on the local file before
      any plate is read; reference
      producible at its pinned digest with
      the plate page produced from the
      pinned file. Any failure closes the
      run as CLOSED AT STEP 0 in its named
      class. **OWNER-APPROVAL** (the
      execution order).
- [ ] **E4 — Identification protocol**
      (spec §5): step D (two independent
      descriptor derivations, reconciliation,
      comparison with the preserved
      descriptor), step C (continuity on the
      anchors' agreement), step M (the match
      by exactly one frozen route, traps
      asserted). **OWNER-APPROVAL** (the
      execution order).
- [ ] **E5 — Outcome** (spec §§6–8): the
      outcome record under the pre-written
      wording; on RECOVERED the appended
      restatement (created, untested,
      designed-never-run test note), on
      IDENTIFICATION FAILED the appended
      closure entry; the LEDGER entry;
      anchors asserted byte-identical;
      foundation check reported as measured.
      No prior record is edited or deleted
      at any point.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
