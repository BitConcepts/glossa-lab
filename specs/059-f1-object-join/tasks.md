# Spec 059 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the approved
> runnable-experiments campaign of
> 2026-10-21, member 16 of 20; the portfolio
> triage of the same date, finding D-22 RIPE;
> design D-22 governing substance). The freeze
> and the execution of Spec 059 are separate
> later acts under the campaign's Waves 2
> and 3.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-22 object-ID-join replication of
      F1), H13 (epistemic boundaries stated in
      spec §7, including the string-identity
      boundary of §7.1), H15/H23 (execution
      shape is graph-first, spec §10), H16
      (data from the registered sources of
      record: the pinned lineage layer, the
      CISI catalogue layer, the Phase-130
      schema, and the pinned Spec 024 records),
      H24 (no private correspondence in the
      repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F059-C01…C15) drafted in
      the Spec 032–042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-059-5). Acceptance
      tests derived twice independently per
      claim; disagreements and resolutions
      recorded in `adjudication.md` §3. The
      AEE lifecycle hooks have **not** run on
      this register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR on branch
      `spec-059-f1-object-join-draft` and left
      unmerged for the freeze decision, CI
      state reported from the run's own
      conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the
      freeze act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register; the
      gate is **pass**, and a stricter outcome
      blocks the freeze until its named
      recovery is complete and recorded.
      Freeze mechanics are re-checked against
      the adopted 1.5.x engine at the freeze,
      per the campaign plan — not assumed
      from pre-adoption habit.
- [x] **L5 — Freeze-decision items.** The
      freeze rules on OF-059-1 (the gate bar's
      reading: 61.0% operative at draft),
      OF-059-2 (the correction family),
      OF-059-3 (the object-ID source and the
      Phase-130 schema pin), OF-059-4 (OSF
      registration), and OF-059-5 (join
      audit), and confirms or openly
      overturns DD-059-3 and DD-059-4.
- [x] **L6 — Freeze.** On the campaign's
      freeze act for this member, with L4
      passed and L5 decided: hooks recorded,
      `freeze.md` finalised, `freeze.json`
      recomputed over the recovered register
      and finalised texts, every spec §2 pin
      re-asserted against the merged record
      (local-store pins recomputed, not
      carried), the object-ID mapping source
      named and pinned (OF-059-3), and the
      execution phase number allocated
      (DD-059-6).
      **Done at the freeze act of 2026-10-21:**
      hooks PASS over the recovered register
      (0.8-draft) under aee 1.5.3 — zero
      correctness failure modes, no claim below
      0.70 (minimum 0.72), draft-cap records
      only (DD-059-14 gate reading); every §2
      pin re-asserted two-route at `main`
      `a3509525`; OF-059-1 resolved as
      DD-059-7 (gate bar adopted: 61.0%,
      ≥ 3,465 rows), OF-059-2 as DD-059-8
      (single-test family confirmed), OF-059-3
      as DD-059-9 (object-identifier sources
      named and pinned), OF-059-4 as
      DD-059-10 (OSF under E-1), OF-059-5 as
      DD-059-11 (gate census suffices as the
      join audit); DD-059-3 confirmed
      (DD-059-12); Phase-421 allocated
      (DD-059-13); OSF contract registration
      filed under E-1 (filing record in
      `osf-spec-registration.md`).
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and the campaign's execution pass

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
      Executed 2026-10-21 as Phase-421: script
      `backend/scripts/phase421_f1_object_join.py`,
      node `IndusPhase421F1ObjectJoin`,
      registration verified by import before
      the run.
- [x] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.2): input integrity against the
      freeze pins; original concordance join
      reproduced exactly (5,679 / 2,895 / 2 /
      2,782). Any failure stops the run as
      INVALID before any new join is built.
      Executed 2026-10-21: gate 0.1 PASS
      (every §2 and DD-059-9 pin, two routes);
      gate 0.2 PASS (recorded census
      reproduced exactly).
- [x] **E3 — Step 0, part 2** (gates 0.3–0.4):
      the object-ID join built through the
      Phase-130 schema (object identifiers
      only; string identity never a key —
      F059-C06), validated, and censused by
      resolution class; the gate comparison
      against the freeze-ruled bar. A gate
      failure ends the execution here: the
      census and the §3.5 closure wording are
      its complete record, unscored.
      Executed 2026-10-21: gate 0.3 PASS
      (dataset built by the pinned route-(b)
      construction, 5,018 records; Phase-130
      validation verdict pass, 0 errors,
      0 warnings; census 2,899 joined /
      2,780 unjoined / 0 ambiguous, 2,479
      distinct objects); **gate 0.4 FAILED —
      2,899 joined rows (51.05%) against the
      DD-059-7 bar of ≥ 3,465 rows (61.0%),
      shortfall 566 rows; the execution
      closed CLOSED AT STEP 0 — JOIN GATE
      NOT MET**, with the census and the
      §3.5 wording as its complete record.
- [ ] **E4 — Primary** (spec §4, gate-passed
      only): the frozen Phase-136 flow on the
      enlarged set — eligibility and
      estimability applied mechanically (a
      failure is NOT ESTIMABLE, counts shown,
      no p-value), the CMH test under the
      frozen parameters, the LOSO rerun
      (descriptive), and both covariate
      comparisons (joined vs unjoined;
      original joined set vs added rows).
      **NOT REACHED** — gate 0.4 failed at
      E3; no F1 quantity was computed.
- [x] **E5 — Outcome:** the §5 record in the
      pre-written wording for the outcome
      class that fired — results JSON and
      report under the headline rules (lineage
      label, gate census, flow, quantities,
      verdict word, LOSO table, covariate
      comparisons, the scope sentence), the
      appended outcome in this directory, the
      dated replication append to
      `STUDY-SPEC-024/F1`'s record (including
      the "on the joined subset" re-statement
      where §5 provides for it), and the
      LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.
      Delivered 2026-10-21 in the closure form
      the gate outcome prescribes
      (`outcome.md` in this directory — the
      dated replication append to the claim's
      record; §5 provides no "on the joined
      subset" re-statement for a gate closure
      and the §3.5 wording states the scope is
      unchanged; no §4 quantities, LOSO table,
      or covariate comparisons exist to
      report), with
      `reports/phase421_results.json`,
      `reports/phase421_join_census.json`,
      and `reports/phase421_report.md`;
      anchors asserted byte-identical before
      and after; foundation check reported
      as measured at the merge (landing
      append to `outcome.md`).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
