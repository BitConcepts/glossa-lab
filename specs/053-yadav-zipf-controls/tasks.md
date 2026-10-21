# Spec 053 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the campaign plan approved
> AS WRITTEN on 2026-10-21, member 6, design
> D-07 arm A only; the portfolio triage of the
> same date; decision E-3 for arm B). The
> freeze and the execution of Spec 053 are
> separate later acts under the campaign's
> Waves 2 and 3.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      design D-07 arm A: the control-systems
      comparison, its two design-fixed
      sensitivity families, and the
      full-inventory bridge sensitivity; arm B
      excluded per campaign E-3), H13
      (epistemic boundaries stated in spec
      §7), H15/H23 (execution shape is
      graph-first, spec §11), H16 (data from
      the registered sources of record: the
      gate-0.3 pinned corpus layer, the pinned
      anchors and crosswalk files, published
      control counts entered as cited data at
      gate 0.4 — no count typed into a script),
      H24 (no private correspondence in the
      repo), H26 (no semantic-anchoring
      machinery anywhere in this design).
- [x] **L2 — Claims-first register.**
      `claims.json` (F053-C01…C15) drafted in
      the Spec 032–048 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-053-10), and each
      claim's acceptance test derived twice
      with disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR (campaign Wave 1) and left
      unmerged for the freeze wave, CI state
      reported from the run's own conclusions.
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
      freeze decides OPEN-053-1 (strict corpus
      pin and population), OPEN-053-2
      (estimator), OPEN-053-3 (control
      sources), OPEN-053-4 (census floors),
      OPEN-053-5 (comparison rule ε),
      OPEN-053-6 (synthetic process),
      OPEN-053-7 (OSF registration, under
      campaign E-1), and OPEN-053-8 (phase
      number), and confirms or openly overturns
      DD-053-2, DD-053-4, DD-053-5, and
      DD-053-6.
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §2 pin re-asserted against
      the merged record, and the execution
      phase number allocated (DD-053-8).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.2): input integrity against the
      freeze pins; estimator self-test on the
      planted-parameter synthetic distribution
      (failure stops the run as INVALID before
      any corpus is touched).
- [ ] **E3 — Step 0, part 2** (gates 0.3–0.4):
      strict corpus identified, exported, and
      pinned, with its lineage shown (failure
      closes STRICT CORPUS NOT PINNABLE);
      control set entered whole as cited data
      and frozen — N1, N2, N3's process, P1 —
      before any fit exists (failure closes
      CONTROL SET FREEZE FAILED).
- [ ] **E4 — Step 0, part 3** (gate 0.5):
      strict census published (types present,
      strict tokens, inscriptions) and floors
      applied (a TOO THIN closure ends the
      execution here, with the census as its
      finding); control tables' V and N stated
      for the record.
- [ ] **E5 — Primary fits** (spec §4): every
      system under the one estimator; the
      §4.3 comparison rule and the §4.4
      positive-control condition applied
      mechanically; every system's full
      quantities and gaps reported, NEAR MISS
      controls named, N3's replicate
      distribution and as-well share stated.
- [ ] **E6 — Sensitivities** (spec §5):
      S1 inscription-level subsampling
      (halves, quarters, 99 replicates each),
      S2 crosswalk split/merge variants
      (partial variants labelled, unexpanded
      types named), S3 full-inventory fit
      reported beside the recorded exponent —
      none changing the headline.
- [ ] **E7 — Outcome:** the §9 record —
      results JSON and report under the
      headline rules (corpus label and digest,
      frozen control tables with citations,
      per-system quantities, the
      positive-control condition stated before
      the headline word, the §6 pre-written
      wording, the fence sentence), the
      appended outcome in this directory, the
      dated strength-label append to
      `yadav_2009_arxiv_manual_001`'s record,
      and the LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
