# Spec 042 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's order of
> 2026-10-21 and the portfolio triage of the
> same date, drafting only). The freeze was
> executed 2026-10-21 under the campaign
> plan approved as written (authorisation
> E-1); the execution of Spec 042 remains a
> separate later owner act.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-28 object-type split of Arm B),
      H13 (epistemic boundaries stated in spec
      §7), H15/H23 (execution shape is
      graph-first, spec §10), H16 (data from
      the registered sources of record: the
      pinned Phase-393 layer, machinery,
      margins audit, and results), H24 (no
      private correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F042-C01…C15) drafted in
      the Spec 032–040 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-042-4). The AEE
      lifecycle hooks have **not** run on this
      register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state
      reported from the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE).** Ran at the freeze act of 2026-10-21 under aee 1.5.0; passed on the DD-042-9 reading (zero correctness failure modes, minimum propagated 0.72, draft-cap records only). Record: `aee/freeze-aee-note.md`. The original gate text follows. At the freeze
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
- [x] **L5 — Freeze-decision items.** Decided at the freeze act of 2026-10-21 (`adjudication.md` §6): DD-042-6 adopted (OSF registration filed at the freeze), DD-042-7 declined (no fresh synthetic calibration; gate 0.5 stands as the machinery check), DD-042-8 confirmed (the census is the margins instrument), DD-042-2 and DD-042-3 confirmed. The original item follows. The
      freeze decides DD-042-6 (OSF
      registration), DD-042-7 (synthetic
      calibration), and DD-042-8 (margins
      audit), and confirms or openly overturns
      DD-042-2 and DD-042-3.
- [x] **L6 — Freeze.** Executed 2026-10-21: hooks recorded, `freeze.md` finalised, `freeze.json` computed exactly once over the recovered register (0.7-draft) and the finalised texts, every spec §2 pin re-asserted by two routes, execution phase allocated as Phase-407. The original item follows. On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §2 pin re-asserted against
      the merged record, and the execution
      phase number allocated (DD-042-5).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.3): input integrity against the
      freeze pins; population reproduction
      against the recorded flow counts;
      partition census published. Any failure
      stops the run as INVALID before margins.
- [ ] **E3 — Step 0, part 2** (gates 0.4–0.5):
      stratum floors from the census (a THIN
      closure ends the execution here, with
      the census as its finding); pooled Arm B
      regression reproduced exactly. Any
      mismatch stops the run as INVALID.
- [ ] **E4 — Primaries** (spec §4): seal
      stratum and tablet stratum, each with
      its controls and full site jackknife,
      drop-Harappa named in both. A stratum
      whose controls fail is NOT ADJUDICATED
      and the headline follows spec §9.
- [ ] **E5 — Outcome:** the §6 record —
      results JSON and report under the
      headline rules (corpus label, census,
      per-stratum quantities and verdicts,
      the pattern word with direction, the
      fence sentence), the appended outcome in
      this directory, the stratum-resolved
      append to `STUDY-SPEC-028/ARM-B`'s
      record, and the LEDGER entry; anchors
      asserted byte-identical before and
      after; foundation check reported as
      measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
