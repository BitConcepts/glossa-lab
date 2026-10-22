# Spec 062 — Tasks

> ## PLAN — FROZEN 2026-10-21 (successor to Spec 061)
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's
> amendment-queue commission of 2026-10-21,
> item 3; Spec 061's frozen record and
> Phase-423 outcome; Spec 028's frozen
> record). **The freeze, the OSF filing, and
> the execution of Spec 062 are separate
> later acts, each OWNER-APPROVAL; none is
> authorised by this draft. The freeze and
> the OSF filing were taken on 2026-10-21
> under the owner's approval (amendment
> package Item 3; L4/L5/E1 below); execution
> remains a separate later act. Arm A2 has no
> task in this plan** (E-3, spec header):
> it is contingent, trigger-armed, and
> unarmed on any record; Spec 061's T*
> stays undefined on Spec 061's record.

## Drafting (this draft)

- [x] **D1 — Failure verified against the
      frozen record.** Spec 061's §4.7 +
      §5, DD-061-9…DD-061-15, and the
      Phase-423 outcome read in full; the
      step function recomputed from the
      record's own values (A(1) =
      −0.0025188916876574316; A(1.5) = A(2) =
      A(3) = 1.0 exactly); gates 0.1–0.4 and
      gate 0.3's digit-for-digit reproduction
      confirmed as passed and intact.
- [x] **D2 — Candidate repairs derived and
      measured on planted data.** Four
      candidates derived on the record
      (adjudication §3); the lead candidate
      (R-1, per-inscription Dirichlet drawing,
      §4.7-R) implemented in a scratch script
      on synthetic/planted data mirroring the
      recorded Arm A margins, and shown to
      bracket both frozen θ values, increase
      strictly on the scan grid, and bisect
      to |A_R(b*) − θ| ≤ 1e-6 for both
      scenarios (numbers in adjudication §3).
      The demonstration scores nothing: no
      real corpus quantity was computed.
- [x] **D3 — This draft.** `spec.md`,
      `claims.json` (register 0.5-draft,
      F062-C01…C15), `adjudication.md`,
      `tasks.md`, opened as a DRAFT PR and
      left unmerged for the freeze decision.
      Spec 061's directory is untouched.

## Lifecycle (freeze gate — NOT run by this draft)

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance
      H2, H6 (no scope beyond the D-27 arm A1
      precision computation with the repaired
      calibration — arm A2 excluded, E-3),
      H13 (epistemic boundaries stated in
      spec §7), H15/H23 (execution shape is
      graph-first, spec §10), H16 (data from
      the registered sources of record: the
      pinned Phase-393 results, layer,
      machinery, margins audit, and Spec
      028/061 records), H24 (no private
      correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F062-C01…C15) drafted in
      the Spec 032–042 register shape, with
      `observed_at` carried on evidence items
      from this draft. The AEE lifecycle hooks
      have **not** run on this register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as DRAFT PR #307 and left unmerged for
      the freeze decision; CI state, when
      reported, is reported from the run's
      own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE
      GATE).** DONE 2026-10-21 at the freeze
      act: `aee assess` (lenient load) run
      after_specify, after_plan, and
      after_tasks over the claim register,
      recovered to 0.6-draft first (round 1
      over 0.5-draft: 22 failure modes — 15
      FR-2.3 draft-cap records and 7
      irreducibility challenges; the
      challenged heads restated singly, the
      freeze rulings carried into
      boundaries). Final round at every hook:
      15 draft-cap records only, zero
      correctness failure modes, minimum
      propagated score 0.72, no claim below
      the 0.70 threshold — **pass** on the
      DD-062-12 reading (the DD-038-10
      reading). Record in
      `aee/freeze-aee-note.md`.
- [x] **L5 — Freeze-decision items.** DONE
      2026-10-21 (`adjudication.md` §8):
      OP-062-1 decided DD-062-7 (calibration
      seed 20261021, as drafted); OP-062-2
      decided DD-062-8 (Phase-424 allocated,
      verified unallocated); OP-062-4
      decided DD-062-9 (construction R-1
      adopted as drafted; R-2 not adopted,
      its tolerance amendment not taken;
      R-3/R-4 rejections stand); OP-062-3
      decided DD-062-10 (OSF registration
      filed at the freeze, E-1); OP-062-5
      decided DD-062-11 (freeze and filing
      taken; execution not authorised).
      DD-062-1…DD-062-6 stand as drafted,
      none overturned.

## Execution (NOT authorised by this draft; every step OWNER-APPROVAL)

- [x] **E1 — Freeze + OSF.** DONE
      2026-10-21: this contract is frozen
      (digest computed over the recovered
      register 0.6-draft exactly once, at
      freeze; `freeze.md` / `freeze.json`),
      and this spec's own OSF contract
      registration is filed under campaign
      decision E-1 (DD-062-10; filing record
      `osf-spec-registration.md`). The
      registration stands pending approval;
      execution (E2–E5) awaits its approval
      act and a separate execution order
      (DD-062-11).
- [ ] **E2 — Graph-first build** (H15/H23) —
      script, graph node, registration,
      verification. **OWNER-APPROVAL** (as
      part of the execution order).
- [ ] **E3 — Step 0** (spec §3) — composite
      pin, population reproduction,
      recorded-distribution reproduction
      (gate 0.3, exact), search-frame
      assertion, gate 0.5-R calibration
      verification. **OWNER-APPROVAL** (the
      execution order).
- [ ] **E4 — Computation** (spec §4) — both
      scenarios, ascending grid m = 1…25,
      full grid table recorded.
      **OWNER-APPROVAL** (the execution
      order).
- [ ] **E5 — Outcome** (spec §6) — appended
      records only; anchors asserted
      byte-identical; foundation check
      reported as measured. No Arm A2 step
      exists in this plan.
