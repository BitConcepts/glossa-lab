# Spec 040 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's bundle and
> evidence-standard decisions of 2026-10-20,
> drafting only). The freeze is barred until
> Spec 039 has executed (spec §1); execution
> remains gated on the freeze and a separate
> execution order.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan,
      and claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-25 rerun of G1), H13 (epistemic
      boundaries stated in spec §11), H15/H23
      (execution shape is graph-first, spec
      §13), H16 (data from the registered
      sources of record: the pinned layer, the
      Phase-139 covariates, the pinned spine,
      and — at the freeze — the pinned Spec 039
      assignment artifact), H24 (no private
      correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F040-C01…C15) drafted in
      the Spec 032–037 register shape.
      Draft-stage self-check: dependency
      integrity and the cited-record facts are
      pinned by
      `backend/tests/test_spec040_freeze.py`;
      the AEE lifecycle hooks have **not** run
      on this register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state
      reported from the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE).**
      Run at the freeze act of 2026-10-24 (see
      the freeze-act record appended below):
      `aee assess` after_specify, after_plan,
      and after_tasks over the claim register,
      recovered in two rounds (0.5-draft →
      0.7-draft); the gate **passed** on the
      DD-038-10 reading (15 FR-2.3 draft-cap
      records only; zero correctness modes;
      minimum propagated confidence 0.8445).
      Record: `aee/freeze-aee-note.md`.
- [x] **L5 — Dependency gate (FREEZE GATE).**
      Verified at the freeze act of 2026-10-24:
      §1 judged satisfied by the openly recorded
      successor-artifact substitution of Spec
      041's artifact (Spec 039 executed and
      named; its own artifact did not satisfy
      §1; Spec 041's artifact pinned at
      `1e5b54c9…` and mechanically verified —
      `adjudication.md` §5, `freeze.md` §3).
- [x] **L6 — Freeze.** Executed 2026-10-24 on
      the owner's approval of the freeze plan
      as specified: hooks recorded, `freeze.md`
      finalised (both artifacts named in),
      `freeze.json` recomputed exactly once
      over the recovered register and finalised
      texts, the execution phase number
      allocated as **Phase-439** (DD-040-10),
      and DD-040-1 adopted, DD-040-5 confirmed,
      DD-040-6 retained, DD-040-9 filed.
- [x] **L7 — Freeze PR and OSF record.** The
      freeze PR carries this record; its merge
      on genuine CI green (read from the run's
      own job conclusions) and the OSF filing
      under DD-040-9 complete the act — the
      filing is recorded in
      `osf-spec-registration.md`, completed by
      append after filing. Execution (E1–E7)
      remains gated on a separate owner order.

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Dependency re-verification and
      input integrity:** the Spec 039 artifact
      and every §3 pin hash to their freeze
      values; the §4.1 join covers the 5,410-row
      population exactly (one assignment row
      per inscription id; no duplicates; site
      agreement asserted). Any failure stops
      the run as INVALID before margins.
- [ ] **E3 — Margins gate** (spec §5): margins
      only — assigned/unassigned by site and
      period, sites per period, contested-
      excluded count, permutable N. Failure
      closes the execution NOT-YET-TESTABLE;
      no outcome quantity is computed.
- [ ] **E4 — Comparability regression**
      (spec §7): the composition-only and
      composition × preservation configurations
      reproduce Phase-137/Phase-140 exactly.
      Any mismatch stops the run as INVALID.
- [ ] **E5 — Primary** (spec §6): the
      period-stratified permutation (B = 9,999,
      seed 20261009) and the stratified basic
      bootstrap interval (B = 4,999, seed
      20261012, basic interval governing);
      outcome assigned by §6.4 alone.
- [ ] **E6 — Sensitivities** (spec §8):
      contested-included; leave-one-site-out
      over every analysis site; drop-Harappa
      named in the headline sensitivity
      paragraph (or NOT APPLICABLE, recorded);
      recorded companions reported as recorded.
- [ ] **E7 — Outcome:** the §10 record —
      results JSON and report under the
      headline rules, the appended outcome in
      this directory, the G1 consequence append
      (or the NOT-YET-TESTABLE / INVALID record),
      the LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.

---

## Freeze-act record - appended 2026-10-20

The freeze act was reached on 2026-10-20 under
the owner's pipeline order (freeze order
038 -> 037 -> 039 -> 040) and closed at the
dependency gate:

- **L4 - NOT RUN.** The section 1 gate stands
  in front of the hooks (see
  `aee/freeze-aee-note.md`); the gate failed,
  so no hook pass was run over the register.
- **L5 - FAILED, recorded.** Spec 039 has
  executed (freeze digest `ec53a841...`;
  PRs #226/#234/#235 merged) and its artifact
  recomputes to the expected SHA-256
  (`64f288d3...`), but the artifact does not
  satisfy the section 4 interface: assignments
  are per site as label sets (finding aids),
  with no site x local-label mapping key, and
  three of the seven G1 sites have no artifact
  rows. Spec section 1 conditions 2 and 4
  fail. The recorded state is
  **NOT-YET-TESTABLE - dependency gate**; the
  full verification is the dependency-gate
  record appended to `outcome.md`.
- **L6 / L7 - NOT REACHED.** No freeze: no
  digest computed, DD-040-1/5/6/9 undecided,
  no phase number allocated (DD-040-10 open),
  no OSF registration filed.
- **E1-E7 - NOT REACHED.** No execution was
  ordered or run; no label joined, no margin
  computed, no quantity calculated.

---

## Freeze-act record - appended 2026-10-24

The freeze was reached again on 2026-10-24
under the owner's approval of the freeze plan
as specified (2026-10-24, 10:54 EDT, "Approve
as specified"; the plan is
`2026-10-24-spec-040-freeze-plan.md` in the
program goal's files; the adjudication record
is `adjudication.md` §5):

- **L5 - PASSED, by substitution.** Spec 039
  stands executed (digest `ec53a841...`) with
  its artifact at `64f288d3...` — and its
  §1 failure stands. Spec 041's artifact
  (`1e5b54c9...`, freeze digest `fe618886...`,
  Phase-435) is accepted as the successor
  dependency artifact the 2026-10-20 closure
  contemplated, and was mechanically verified
  at the act: pin recomputed; 78 cells
  schema-valid; the covariate census equal to
  the artifact's triples; the A1 join covering
  the 5,410 population IDs exactly once and
  reproducing the published A1 counts (1,457
  placed; 32 / 1,386 / 39).
- **L4 - PASSED.** Hooks run over the register
  recovered in two rounds (0.5-draft ->
  0.7-draft): 15 failure modes, all FR-2.3
  draft-cap; zero correctness modes; minimum
  propagated confidence 0.8445 (`aee/`).
- **L6 - DONE.** Derivation A1 adopted as the
  primary; DD-040-1 adopted; DD-040-5
  confirmed (NOT-YET-TESTABLE); DD-040-6
  retained; DD-040-9 filed; DD-040-10
  allocated **Phase-439**; section 8.1 recorded
  NOT APPLICABLE (zero CONTESTED cells). The
  stale anchors pin was refreshed
  (`eccea6d5...` -> `df0cf620...`). The freeze
  digest was computed exactly once over the
  recovered register and the finalised texts.
  The freeze record states the known margins
  consequence in the open: on the pinned
  counts the section 5 gate already fails under
  every derivation, and a later execution is
  expected to close NOT-YET-TESTABLE at the
  margins gate.
- **L7 - CARRIED BY THE FREEZE PR.** Its merge
  on genuine CI green, read from the run's own
  job conclusions, and the OSF registration
  filed under DD-040-9 (record:
  `osf-spec-registration.md`, completed by
  append after filing) complete the act.
- **E1-E7 - NOT REACHED.** No execution was
  ordered; nothing was joined for outcome
  purposes, no margin was run, and no outcome
  quantity exists.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
