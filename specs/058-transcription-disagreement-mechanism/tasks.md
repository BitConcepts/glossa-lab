# Spec 058 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the runnable-experiments
> campaign plan approved by the owner AS
> WRITTEN on 2026-10-21 — D-21 arm A is
> campaign member 15 — and the portfolio
> triage of the same date, drafting only).
> The freeze and the execution of Spec 058
> are separate later owner acts. Arm B is
> blocked and out of scope throughout; no
> task in this file touches it.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-21 arm A mechanism re-analysis of
      the recorded Phase-132 passes; arm B
      excluded, no AI substitution designed),
      H13 (epistemic boundaries stated in spec
      §8), H15/H23 (execution shape is
      graph-first, spec §11), H16 (data from
      the registered sources of record: the
      §2.1 committed pins and the Phase-132
      store record set produced under gate
      0.2 — no values typed into a script, no
      substitute source), H24 (no private
      correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F058-C01…C16) drafted in
      the Spec 032–042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-058-13). Acceptance
      tests derived twice independently per
      claim; disagreements and resolutions
      recorded in `adjudication.md` §5. The
      AEE lifecycle hooks have **not** run on
      this register (L4).
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
      exactly once, at freeze. Freeze
      mechanics are re-checked against the
      adopted 1.5.x engine at the freeze
      rather than assumed from pre-adoption
      habit (campaign plan, Wave 2).
- [ ] **L5 — Freeze-decision items.** The
      freeze decides DD-058-10 (OSF
      registration), DD-058-11 (execution
      venue / store preservation for gate
      0.2), and DD-058-12 (margins/census
      audit), and confirms or openly overturns
      DD-058-3, DD-058-6, DD-058-8, and
      DD-058-9.
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §2 pin re-asserted against
      the merged record, and the execution
      phase number allocated (DD-058-5).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
      The script imports the pinned Phase-132
      metrics module for the store loader,
      the P-space derivation, the alignment,
      and the reproduction computation; it
      does not reimplement them.
- [ ] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.3): committed-record integrity
      against the freeze pins; pilot-pass
      record-set production, inventory, and
      per-file SHA-256 manifest (a production
      shortfall closes the execution here as
      PILOT-PASS RECORDS NOT PRODUCIBLE, with
      the inventory shortfall as its finding);
      frame identity against the committed
      frame. Any other failure stops the run
      as INVALID.
- [ ] **E3 — Step 0, part 2** (gates 0.4–0.6):
      exact reproduction of the committed
      Phase-132 metrics from the produced set;
      adjudication-taxonomy cross-check
      (93 / 45 / 11 / 10 / 2 / 1; total 162);
      mismatched-population census published
      (40 objects on the committed record).
      Any mismatch stops the run as INVALID
      before any event is tabulated.
- [ ] **E4 — Tabulations** (spec §4): frozen
      alignments over the mismatched objects;
      mismatch events typed and counted; T1
      (by sign, with frequency shares and the
      design's CONCENTRATED / UNIFORM /
      BETWEEN states), T2 (by object type),
      T3 (by divergence type); the
      first-divergence table; the §4.4
      UNK-excluded descriptive secondary; the
      M-space sensitivity.
- [ ] **E5 — Outcome:** the §6 record —
      results JSON and report under the
      reporting rules (gate record and
      manifest, census, T1–T3 primary and
      secondary, first-divergence table,
      per-locus verdicts with their deciding
      numbers, the headline word and its
      pre-written paragraph, the fence
      sentence), the appended outcome in this
      directory, the mechanism-account append
      to `STUDY-SPEC-023/PHASE-132+383`'s
      record, and the LEDGER entry; anchors
      asserted byte-identical before and
      after; foundation check reported as
      measured. No outcome re-opens arm B:
      the human-coder arm proceeds, if ever,
      only under the owner's lifted hold and
      its own planning gate (campaign plan
      Part 6 item 4).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
