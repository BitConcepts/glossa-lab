# Spec 068 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-22
>
> Adjudication inputs are recorded in
> `adjudication.md` (the Shakti readiness
> assessment §§1.5–1.6; the owner's 2026-10-22
> readiness decisions, decision 2, with
> decision 2c; and Spec 053's frozen record
> including DD-053-11). The freeze, the
> execution, and the OSF registration of
> Spec 068 are separate later owner acts.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      Spec 053's question as carried by
      Amendment S-053: the control-systems
      comparison on the Shakti restricted
      corpus, the amendment's grade sensitivity,
      and the carried subsampling sensitivity;
      arm B excluded, spec §13), H13
      (epistemic boundaries stated in spec
      §8), H15/H23 (execution shape is
      graph-first, spec §12), H16 (data from
      the registered sources of record: the
      intake record's pinned corpus and
      row-grades files, the pinned anchors and
      crosswalk files, published control counts
      entered as cited data at gate 0.6 — no
      count typed into a script), H24 (no
      private correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F068-C01…C14) drafted in
      the Spec 042–048 / Spec 054 draft register
      shape, at `0.5-draft`, with `observed_at`
      carried on evidence items from this draft
      (DD-068-6) and the acceptance tests for
      each claim derived twice independently,
      disagreements resolved in
      `adjudication.md` §3. The open freeze item
      OPEN-068-1 is registered as claim
      F068-C02 and carried as a dependency by
      the claims whose verdicts turn on the fit
      population. The AEE lifecycle hooks have
      **not** run on this register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a PR on branch
      `spec-068-yadav-zipf-controls-successor-draft`
      and left **open and unmerged** for the
      owner's freeze decision, CI state reported
      from the run's own conclusions.
- [ ] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the
      freeze act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register; the
      gate is **pass**, on the DD-038-10
      posture for draft registers adopted for
      Spec 053 in DD-053-19. Deliberate
      ordering: any recovery round changes
      claim text, and the freeze digest is
      computed over the recovered register
      exactly once, at freeze. Freeze mechanics
      are re-checked against the adopted aee
      engine at the freeze rather than assumed
      from pre-adoption habit.
- [ ] **L5 — Freeze-decision items.** The
      freeze decides OPEN-068-1 (the
      strict-sign-set limb: A retained and
      keyed to ICIT space by the step-0 mapping
      act, with the mapping's basis source
      named in the freeze record; or B dropped,
      the population stated as the full ICIT
      sign inventory of the restricted corpus —
      the choice recorded in spec §2.2's terms,
      no proceeding with the choice unstated),
      OPEN-068-2 (the intake record standing on
      the merged record, with both SHA-256 pins
      exactly as spec §2.1 states them, and
      every other spec §3 pin re-asserted),
      OPEN-068-3 (the contract as drafted, with
      DD-068-1…DD-068-6 confirmed or openly
      overturned), OPEN-068-4 (the AEE hooks on
      the DD-038-10 / DD-053-19 reading),
      OPEN-068-5 (the control-table posture of
      DD-053-13, or a named system openly
      replaced before any counting),
      OPEN-068-6 (the new OSF contract
      registration for Spec 068), and
      OPEN-068-7 (the execution phase number).
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §3 pin re-asserted against
      the merged record, the intake record
      asserted as OPEN-068-2 requires, the
      population limb recorded in the freeze
      record, the execution phase number
      allocated (OPEN-068-7), and the OSF
      contract registration filed as a new
      registration for this spec if L5 confirms
      OPEN-068-6 (its approval act remains a
      separate owner act).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §4 gates
      0.1–0.2): input integrity against the
      freeze pins, with the intake record
      asserted as standing; estimator self-test
      on the planted-parameter synthetic
      distribution (failure stops the run as
      INVALID before any corpus is touched).
- [ ] **E3 — Step 0, part 2** (gates 0.3–0.5):
      Shakti intake gates asserted against the
      intake record — S1, both SHA-256 pins
      recompute; S2, the audit census
      reproduces (failure at either closes as
      SHAKTI INTAKE NOT REPRODUCED); this
      successor's own restricted-corpus census
      measured and stated, governing over the
      draft's derived figures; the population
      act under the freeze's recorded limb —
      under limb A, the strict set's mapping
      to ICIT space stated per sign and the
      mapping table pinned (failure closes as
      STRICT MAPPING NOT PINNABLE); under
      limb B, the population stated as the
      full ICIT sign inventory of the
      restricted corpus.
- [ ] **E4 — Step 0, part 3** (gates 0.6–0.7):
      control set entered whole as cited data
      and frozen — N1, N2, N3's process, P1 —
      before any fit exists (failure closes
      CONTROL SET FREEZE FAILED); census floors
      applied, measured on the restricted set
      (a TOO THIN closure ends the execution
      here, with the census as its finding).
- [ ] **E5 — Primary fits** (spec §5): every
      system under the one estimator frozen by
      Spec 053; the §5.3 comparison rule and
      the §5.4 positive-control condition
      applied mechanically on the primary fit;
      every system's full quantities and gaps
      reported, NEAR MISS controls named, N3's
      replicate distribution and as-well share
      stated.
- [ ] **E6 — Sensitivities** (spec §6): the
      grade sensitivity fit (documented +
      corroborated, under the same limb) in
      full beside the primary, both orderings
      exhibited, a differing ordering reported
      as grade-sensitivity per P-F1 S4 with the
      §6.1 sentence carried in the headline
      block; the subsampling tables for both
      populations; the conditional
      full-inventory fit (limb A only) with no
      Phase-43 juxtaposition. Rows graded
      undocumented-uncorroborated enter no
      fit, count, statistic, or argument.
- [ ] **E7 — Outcome:** the §10 record —
      results JSON and report under the
      headline rules (the P-F1 S3 lineage
      statement verbatim first in the headline
      block, the corpus label and intake
      assertions, the full step-0 record, the
      per-system tables for the primary and
      the sensitivity populations, the
      positive-control placement, the headline
      word in §7's pre-written wording, and
      the fence sentence), the appended outcome
      in this directory, the dated
      strength-label append to
      `yadav_2009_arxiv_manual_001`'s record
      (no append on a step-0 closure), and the
      LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
