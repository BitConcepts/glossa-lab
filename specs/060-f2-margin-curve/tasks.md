# Spec 060 — Tasks

> ## PLAN — FROZEN 2026-10-21 (execution Phase-422)
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner-approved
> runnable-experiments campaign of
> 2026-10-21, member 17; the portfolio triage
> of the same date; design D-23 with the
> D-20 correction of adjudication §2). The
> freeze and the execution of Spec 060 are
> separate later acts.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-23 margin curve and
      shared-population test of F2's residue),
      H13 (epistemic boundaries stated in spec
      §9), H15/H23 (execution shape is
      graph-first, spec §12), H16 (data from
      the registered sources of record: the
      two layers at their Phase-137-recorded
      pins, the Phase-137 machinery, the
      Phase-384 v2 estimator), H24 (no private
      correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F060-C01…C15) drafted in
      the Spec 032–042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-060-9) and the
      acceptance tests derived twice
      independently, disagreements resolved in
      `adjudication.md` §4.
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
      exactly once, at freeze. Freeze mechanics
      are re-checked against the adopted
      1.5.x engine at the freeze, per the
      campaign plan.
- [x] **L5 — Freeze-decision items.** The
      freeze decides DD-060-6 (OSF
      registration), DD-060-7 (synthetic
      calibration), and DD-060-8 (execution
      venue / held-layer copies), and confirms
      or openly overturns DD-060-2, DD-060-3,
      and DD-060-4. **Decided at the freeze act of
      2026-10-21** as DD-060-10 to DD-060-17 in
      `adjudication.md` §8: OSF registration filed
      under E-1 (DD-060-10); DD-060-2, DD-060-3, and
      DD-060-4 all CONFIRMED (DD-060-11, DD-060-12,
      DD-060-13 — the SEAL reading and the period
      stated-unavailability wording stand, with no
      imported period assignment); no fresh synthetic
      calibration beyond gate 0.3 (DD-060-14); the
      venue is the owner's machines at the loaders'
      default paths, both held copies verified at
      the freeze to hash exactly to the §3 pins
      (DD-060-15).
- [x] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §3 pin re-asserted against
      the merged record (the two layer pins
      against the held files at the named
      venue), and the execution phase number
      allocated (DD-060-5).
      **Done at the freeze act of 2026-10-21:**
      hooks PASS over the recovered register
      (0.7-draft) under aee 1.5.3 — zero
      correctness failure modes, no claim below
      0.70 (minimum 0.795), draft-cap records
      only (DD-060-17 gate reading); every §3
      pin re-asserted two-route in the
      foreground at `main` `a3509525`, all
      matching the draft pins, the estimator
      and contract hashes also matching the
      Phase-384 freeze-v2 sources record; both
      held-layer copies verified at the
      loaders' default paths to hash exactly
      to their recorded pins; OPEN-060-1 to
      OPEN-060-6 resolved as DD-060-10 to
      DD-060-16 in `adjudication.md` §8;
      Phase-422 allocated (DD-060-16); OSF
      contract registration filed under E-1
      (DD-060-10; filing record in
      `osf-spec-registration.md`). The freeze
      computed nothing — no census, no curve
      cell, no shared-population quantity.
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

Campaign order (plan Part 4, Wave 3):
**Spec 060 executes in group 2, the
independent executions.** It consumes no
shared asset and no member's output, and no
member consumes its output inside the pass.

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §4 gates
      0.1–0.3): input integrity against the
      freeze pins (both held layers included);
      both layers' population reproduction
      against the recorded tables, counts, χ²,
      and V; estimator regression against both
      recorded governing intervals. Any failure
      stops the run as INVALID before any arm
      quantity.
- [ ] **E3 — Step 0, part 2** (gate 0.4):
      shared-population census published
      (site intersection re-derived, per-layer
      and per-site counts). A THIN result
      closes arm 2 here, with the census as
      its finding; arm 1 proceeds (DD-060-2).
- [ ] **E4 — Arm 1** (spec §5.1): the margin
      curve on the full Holdat population —
      governing interval recomputed under the
      Phase-384 v2 estimator, the five grid
      cells worded by claim F060-C08's rule,
      labelled sensitivity in every product.
- [ ] **E5 — Arm 2** (spec §5.2, if its gate
      passed): per-layer governing intervals
      on the shared population under identical
      code, signs never pooled or mapped
      (F060-C14); period mix described per
      layer or its unavailability stated
      (F060-C13); the outcome word under
      F060-C12, in the §6 wording that matches
      it — for COMPOSITION DOES NOT, the
      corrected hand-off wording of §6.3.
- [ ] **E6 — Outcome:** the §8 record —
      results JSON and report under the
      headline rules (both corpus labels, the
      gate record, the full curve, the census,
      both interval pairs, the no-verdict-moves
      sentence), the appended outcome in this
      directory, the dated append to
      `STUDY-SPEC-024/F2-HOLDAT`'s record, and
      the LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
