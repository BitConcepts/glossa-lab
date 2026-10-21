# Spec 061 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the campaign plan
> approved AS WRITTEN on 2026-10-21, member
> 18, arm A1 only; the triage of the same
> date; design D-27). The freeze and the
> execution of Spec 061 are separate later
> acts. **Arm A2 has no task in this plan**
> (adjudication §6): it is contingent,
> trigger-armed, and outside this pass under
> campaign decision E-3.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-27 arm A1 precision computation —
      arm A2 excluded, E-3), H13 (epistemic
      boundaries stated in spec §7), H15/H23
      (execution shape is graph-first, spec
      §10), H16 (data from the registered
      sources of record: the pinned Phase-393
      results, layer, machinery, and margins
      audit), H24 (no private correspondence
      in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F061-C01…C15) drafted in
      the Spec 032–042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-061-6). The AEE
      lifecycle hooks have **not** run on this
      register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      freeze decision, CI state reported from
      the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the freeze
      act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register; the
      gate is **pass**, and a stricter outcome
      blocks the freeze until its named
      recovery is complete and recorded.
      Deliberate ordering (the Spec 035/038
      record): any recovery round changes
      claim text, and the freeze digest is
      computed over the recovered register
      exactly once, at freeze.
- [x] **L5 — Freeze-decision items.** The
      freeze decides OP-061-1…OP-061-5 (the
      search frame: grid and rounding, ceiling,
      trials and draws, simulation seed, and
      the effect-imposition construction),
      OP-061-6 (OSF registration, per campaign
      E-1), and OP-061-7 (synthetic
      calibration), and confirms or openly
      overturns DD-061-2, DD-061-3, and
      DD-061-5.
- [x] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §2 pin re-asserted against
      the merged record, the complete search
      frame written into the freeze record
      (gate 0.4 reads it from there), and the
      execution phase number allocated
      (DD-061-7).
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
      DONE 2026-10-21 (Phase-423):
      `backend/scripts/phase423_arm_a_precision.py`,
      graph module
      `backend/glossa_lab/experiment_graph_phase423.py`
      (node `IndusPhase423ArmAPrecision`),
      registration verified by import before
      the run.
- [x] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.2): composite resampling-
      distribution pin asserted against the
      freeze pins; Arm A population reproduced
      exactly (1,593 records, five site
      totals, 6 included cells, 294 per draw).
      Any failure stops the run as INVALID
      before any trial. DONE 2026-10-21:
      gates 0.1 and 0.2 PASS (outcome.md §2).
- [x] **E3 — Step 0, part 2** (gates 0.3–0.4):
      recorded-distribution reproduction
      (frozen Arm A primary re-run at seed
      20261012 reproduces the recorded median,
      interval, and rejection share exactly —
      a mismatch stops the run as INVALID);
      search frame read from the freeze record
      and asserted complete (any missing
      element closes the run as CANNOT BE RUN
      AS WRITTEN). DONE 2026-10-21: gates 0.3
      (exact reproduction, digit-for-digit)
      and 0.4 PASS; the freeze-added gate 0.5
      (construction calibration) then FAILED
      and closed the execution as CANNOT BE
      RUN AS WRITTEN — A(b) recomputes to the
      step function −0.0025188916876574316 at
      b = 1 and 1.0 at every b > 1, so no boost
      in [1, 3] achieves |A(b) − θ| ≤ 1e-6
      (outcome.md §2). E4 and E5 are closed in
      substance by that record: the computation
      cannot run under this frozen contract.
- [ ] **E4 — Computation** (spec §4): both
      scenarios independently, grid points in
      ascending total order, each trial a
      labelled simulation over recorded data
      under the frozen effect-imposition
      construction; resolution and
      qualification applied mechanically
      (F061-C10); full grid table recorded,
      including non-monotone patterns as
      observed.
- [x] **E5 — Outcome:** the §6 record —
      DONE 2026-10-21 in its closure form:
      `outcome.md` in this directory, the
      results JSON and Phase-423 report under
      `reports/`, and the root LEDGER entry;
      the record is the CANNOT BE RUN AS
      WRITTEN closure at gate 0.5, so the §6
      items that presuppose a computed grid
      (the grid table, per-target totals, the
      dated precision append to
      `STUDY-SPEC-028/ARM-A` with an operative
      T*) do not exist — no target was
      computed, T* is undefined on this
      record, and nothing is appended to the
      claim's record as a precision result.
      The §6 record as executed:
      results JSON and report under the
      headline rules (simulation label, both
      scenario values, the full grid table
      and search frame, per-target totals /
      multiples / per-site distributions or
      the no-target record, the §5 headline
      word with its pre-written wording, the
      fence sentence), the appended outcome in
      this directory, the dated precision
      append to `STUDY-SPEC-028/ARM-A`'s
      record (including, if a target is
      returned, the operative trigger target
      T\* under DD-061-5, recorded for the
      weekly data watch — recording it arms
      nothing by itself, per E-3), and the
      LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
