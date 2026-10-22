# Spec 068 — Tasks

> ## PLAN — FROZEN 2026-10-22
>
> Adjudication inputs are recorded in
> `adjudication.md` (the Shakti readiness
> assessment §§1.5–1.6; the owner's 2026-10-22
> readiness decisions, decision 2, with
> decision 2c; and Spec 053's frozen record
> including DD-053-11). The freeze act of
> 2026-10-22 (the owner's freeze rulings;
> `freeze.md`; DD-068-7 to DD-068-13) froze the
> contract, filed the OSF registration, and
> allocated Phase-430; execution runs under
> the owner's execution order of 2026-10-22.

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
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE).**
      Run at the freeze act, 2026-10-22, under
      aee 1.5.3: after_specify, after_plan, and
      after_tasks over the register, on the
      DD-038-10 posture adopted as DD-068-10.
      The freeze's rulings were carried into the
      register first; two recovery rounds the
      hooks forced (0.5-draft → 0.6-draft
      loadability; → 0.7-draft head
      restatements; → 0.8-draft final
      tightening) were completed before the
      digest. Final round: 14 FR-2.3 draft-cap
      records only at every hook, zero
      correctness failure modes, minimum
      propagated 0.795 — **pass**
      (`aee/freeze-aee-note.md`).
- [x] **L5 — Freeze-decision items.** Decided
      at the freeze act, 2026-10-22
      (`adjudication.md` §7): OPEN-068-1 ruled
      **LIMB B** (DD-068-7 — the strict-sign-set
      restriction dropped, openly; the
      population stated as the full ICIT sign
      inventory of the restricted corpus; limb A
      considered and not taken), OPEN-068-2
      (DD-068-8 — the intake record asserted on
      the merged record with both pins exact;
      every other spec §3 pin re-asserted; the
      claim file re-pinned at its current hash
      on an open discrepancy record),
      OPEN-068-3 (DD-068-9 — DD-068-1…DD-068-6
      confirmed as drafted), OPEN-068-4
      (DD-068-10 — the DD-038-10 gate reading),
      OPEN-068-5 (DD-068-11 — the four control
      systems stand as named), OPEN-068-6
      (DD-068-12 — the new OSF contract
      registration filed at the freeze), and
      OPEN-068-7 (DD-068-13 — Phase-430).
- [x] **L6 — Freeze.** Done 2026-10-22:
      `freeze.md` finalised; `freeze.json`
      computed over the recovered register
      (0.8-draft) and the finalised texts
      exactly once; the OSF contract
      registration filed as a new registration
      for this spec (DD-068-12; filing record in
      `osf-spec-registration.md`, completed by
      append after filing; its approval act
      remains a separate owner act).
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
