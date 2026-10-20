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
- [ ] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the freeze
      act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register; the
      gate is **pass**, and a stricter outcome
      blocks the freeze until its named
      recovery is complete and recorded.
      Deliberate ordering (the Spec 035
      record): any recovery round changes
      claim text, and the freeze digest is
      computed over the recovered register
      exactly once, at freeze.
- [ ] **L5 — Dependency gate (FREEZE GATE).**
      Verify spec §1 against the merged record:
      Spec 039 executed, its freeze digest and
      outcome named; the assignment artifact
      pinned by SHA-256 and satisfying the §4
      interface (site-period resolution,
      citations, contested flags,
      published determinations only). Failure
      is recorded as NOT-YET-TESTABLE at the
      dependency gate; no freeze proceeds.
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 and L5 passed: hooks
      recorded, `freeze.md` finalised (Spec 039
      artifact named in), `freeze.json`
      recomputed over the recovered register
      and finalised texts, the execution phase
      number allocated (DD-040-10), and
      DD-040-1, DD-040-5, DD-040-6, DD-040-9
      decided.
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check after any anchor- or
      phase-bearing change — none exists at
      draft; the freeze allocates a phase
      number and its record states the measured
      foundation state).

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

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
