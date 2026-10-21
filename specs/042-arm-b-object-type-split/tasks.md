# Spec 042 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's order of
> 2026-10-21 and the portfolio triage of the
> same date, drafting only). The freeze and
> the execution of Spec 042 are separate
> later owner acts.

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
- [ ] **L4 — AEE lifecycle hooks (FREEZE GATE
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
- [ ] **L5 — Freeze-decision items.** The
      freeze decides DD-042-6 (OSF
      registration), DD-042-7 (synthetic
      calibration), and DD-042-8 (margins
      audit), and confirms or openly overturns
      DD-042-2 and DD-042-3.
- [ ] **L6 — Freeze.** On the owner's freeze
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
