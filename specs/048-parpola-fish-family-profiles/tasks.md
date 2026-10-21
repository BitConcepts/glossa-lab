# Spec 048 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the campaign plan approved
> AS WRITTEN on 2026-10-21, the portfolio triage
> of the same date, and the Roif verification).
> The freeze and the execution of Spec 048 are
> separate later owner acts. This spec is under
> the campaign's Roif gate: its records are
> internal and its results are not published or
> surfaced under the campaign (claim F048-C14).

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      design D-04's sign-by-sign family test
      plus the Asset F consumption the campaign
      assigns this spec — no asset build, no
      coastal test, no language comparison),
      H13 (epistemic boundaries stated in spec
      §7), H15/H23 (execution shape is
      graph-first, spec §11), H16 (data from
      the registered sources of record: Asset F
      as frozen by Spec 044, the gate-0.3 pinned
      strict corpus, the gate-0.4 pinned Holdat
      layer, the Phase-43 record), H24 (no
      private correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F048-C01…C15) drafted in
      the Spec 032–044 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-048-8), and each
      claim's acceptance test derived twice
      with disagreements resolved in
      `adjudication.md` §3. No Asset F digest
      appears in the register: the pin is taken
      at the freeze (OPEN-048-1). The AEE
      lifecycle hooks have **not** run on this
      register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR (campaign Wave 1) and left
      unmerged for the freeze wave, CI state
      reported from the run's own conclusions.
      Builders before dependents: Spec 044
      freezes, and its step 0 produces Asset F,
      before this spec can freeze.
- [ ] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the freeze
      act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register; the
      gate is **pass**, and a stricter outcome
      blocks the freeze until its named
      recovery is complete and recorded.
      Deliberate ordering (the Spec 035/038/042
      record): any recovery round changes
      claim text, and the freeze digest is
      computed over the recovered register
      exactly once, at freeze. Freeze mechanics
      are re-checked against the adopted
      1.5.x engine at the freeze, per the
      campaign plan, not assumed from
      pre-adoption habit.
- [ ] **L5 — Freeze-decision items.** The
      freeze decides OPEN-048-1 (the Asset F
      digest pin, taken from Spec 044's step-0
      record — the freeze cannot complete
      without it), OPEN-048-2 (the operational
      meaning of "strict"), OPEN-048-3 (the
      20% PASS bar, confirmed against the T2.4
      record), OPEN-048-4 (the second-arm
      closure form, DD-048-4), OPEN-048-5
      (control-set matching and comparison
      rules, DD-048-7), OPEN-048-6 (OSF
      registration, under campaign E-1),
      OPEN-048-7 (unmapped members, DD-048-5),
      and OPEN-048-8 (phase number), and
      confirms or openly overturns DD-048-2.
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §2 pin re-asserted against
      the merged record, Asset F's digest
      stated from Spec 044's step-0 record,
      and the execution phase number allocated
      (DD-048-6).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.2): Asset F exhibited, its digest
      recomputed under the exclusion rule and
      asserted against the freeze pin (failure
      closes ASSET F DIGEST MISMATCH; absence
      closes ASSET F NOT AVAILABLE); membership
      join through the Mahadevan locators, with
      UNMAPPED members listed and the
      cross-check against the claim record's
      trio and the Phase-43 six reported, every
      divergence named.
- [ ] **E3 — Step 0, part 2** (gates 0.3–0.6):
      strict corpus identified, exported, and
      pinned, with the T2.4 reference points
      reproduced (failure closes STRICT CORPUS
      NOT PINNABLE); Holdat layer pinned and
      the per-sign crosswalk stated, conflicts
      named (failure closes SECOND ARM NOT
      RUNNABLE); occurrence census published (a
      TOO THIN closure ends the execution here,
      with the census as its finding); control
      set frozen in the step-0 record.
- [ ] **E4 — Primary arm** (spec §5):
      per-member T2.4 ending-follower rates on
      the pinned strict corpus; every member's
      full figures reported, TOO THIN and
      UNMAPPED members included by disposition.
- [ ] **E5 — Second arm, sensitivity, and
      controls** (spec §5): the Holdat repeat
      with conflict pairs reported separately;
      the 72/64/70 sensitivity; the control
      set through the identical measure, its
      comparison stated beside the family's.
- [ ] **E6 — Outcome:** the §9 record —
      results JSON and report under the
      headline rules (Asset F digest and join
      record, both corpus labels and digests,
      per-member tables for both arms, control
      figures, the sensitivity, §6's pre-written
      headline wording, the Roif-hold sentence),
      the appended outcome in this directory,
      the dated append to the claim
      `parpola_2010_dravidian_solution_manual_002`'s
      record (family verdict or closure — the
      claim's existing text untouched), and the
      LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.
      All records internal under the Roif gate.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
