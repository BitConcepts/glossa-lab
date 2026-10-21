# Spec 048 — Tasks

> ## PLAN — FROZEN — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the campaign plan approved
> AS WRITTEN on 2026-10-21, the portfolio triage
> of the same date, and the Roif verification).
> The freeze was executed on 2026-10-21 under
> that approval (Wave 2 freeze wave):
> `adjudication.md` §7 records the freeze
> decisions DD-048-9 to DD-048-18, including
> the Asset F pin-timing ruling (DD-048-9).
> Execution of Spec 048 is a separate later
> owner act. This spec is under
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
      `adjudication.md` §3. No Asset F byte-digest
      appears in the register: under the freeze's
      pin-timing ruling (DD-048-9) the register
      quotes Spec 044's freeze digest as the
      contract anchor in F048-C06's boundary and
      fixes the step-0 outcome record as the pin
      source. The AEE lifecycle hooks ran at the
      freeze (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR (campaign Wave 1) and left
      unmerged for the freeze wave, CI state
      reported from the run's own conclusions.
      Builders before dependents: Spec 044's
      freeze precedes this freeze (the contract
      anchor, DD-048-9); its step 0, which
      produces Asset F, precedes this spec's
      execution.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE).**
      Run at the freeze act of 2026-10-21 under
      aee 1.5.0: the 0.5-draft register was
      refused at load (evidence enums); recovered
      through 0.6-draft to 0.7-draft as the
      register's note records; after_specify
      cleared in recorded recovery rounds,
      after_plan and after_tasks clean at first
      pass; at every hook zero correctness
      failure modes, no claim below 0.70
      (minimum propagated 0.72), draft-cap
      records only (gate reading DD-048-17;
      record in `aee/freeze-aee-note.md`).
- [x] **L5 — Freeze-decision items.** Decided
      at the freeze (`adjudication.md` §7):
      OPEN-048-1 by the coordinator's pin-timing
      ruling (DD-048-9 — Spec 044's freeze digest
      quoted as contract anchor; the pin source
      fixed as Spec 044's step-0 outcome record;
      gate 0.1 asserts the byte-digest at
      execution step 0), OPEN-048-2 confirmed
      as drafted (DD-048-10), OPEN-048-3 the
      20% bar confirmed (DD-048-11),
      OPEN-048-4 DD-048-4 confirmed
      (DD-048-12), OPEN-048-5 control rules
      fixed with DD-048-7 confirmed
      (DD-048-13), OPEN-048-6 OSF yes under E-1
      (DD-048-14), OPEN-048-7 DD-048-5
      confirmed (DD-048-15), OPEN-048-8
      Phase-408 allocated (DD-048-16);
      DD-048-2 confirmed.
- [x] **L6 — Freeze.** Executed 2026-10-21:
      hooks recorded (`aee/`), `freeze.md`
      finalised, `freeze.json` computed exactly
      once over the recovered register (0.7-draft)
      and the finalised texts, every spec §2 pin
      re-asserted against the merged record by
      two routes (`adjudication.md` §8), the
      Asset F contract anchor stated from Spec
      044's freeze (DD-048-9 — no byte-digest
      exists at this freeze), and the execution
      phase allocated as Phase-408 (DD-048-16).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).
      (Completed at the merge; recorded with the
      freeze PR.)

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.2): Asset F exhibited, its digest
      recomputed under the exclusion rule and
      asserted against the freeze pin (failure
      closes ASSET F DIGEST MISMATCH; absence
      closes ASSET F NOT AVAILABLE — the pin
      asserted is the digest recorded in Spec
      044's step-0 outcome record, the pin source
      fixed at the freeze (DD-048-9)); membership
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
