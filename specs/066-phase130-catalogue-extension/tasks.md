# Spec 066 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication input is recorded in
> `adjudication.md` (the owner's approval of
> 2026-10-21; the freeze decisions in §4). The
> execution tasks for Phase-428 run under the
> frozen contract; execution is additionally
> gated on step 0 of the spec, in the frozen
> order, and begins only after the freeze PR
> merges on genuine CI green.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan,
      and claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the approved Item 7 act), H13 (epistemic
      boundaries stated in spec §§1, 8, 9),
      H15/H23 (execution shape is graph-first,
      spec §7), H16 (data from the registered
      sources of record: the gated portion, the
      pinned layers, the committed census), H24
      (no private correspondence in the repo; the
      restricted material itself never enters
      it). The gate terms, the pins, and the
      candidate-set counts were verified at
      draft time (`adjudication.md` §2).
- [x] **L2 — Claims-first register.**
      `claims.json` (F066-C01…C15) drafted in the
      Spec 032/033/034/035/036/037 register
      shape. Draft-stage self-check: the
      dependency-integrity checks and the
      cited-record facts are pinned by
      `backend/tests/test_spec066_freeze.py`; the
      AEE lifecycle hooks run at L3.
- [x] **L3 — AEE lifecycle hooks (FREEZE
      GATE).** Run at the freeze act, 2026-10-21,
      under aee 1.5.3: after_specify cleared in
      two adjudicated rounds (register recovered
      to 0.6-draft); after_plan and after_tasks
      clean at first pass. At every hook: zero
      correctness failure modes and no claim
      below the 0.70 threshold (minimum
      propagated 0.72); the residual records are
      the 15 FR-2.3 draft-cap records (the
      DD-066-10 gate reading). Recorded in
      `aee/freeze-aee-note.md`. The gate is the DD-066-10
      reading: zero correctness failure modes and
      no claim below the 0.70 threshold at every
      hook; the FR-2.3 draft-cap records are
      structural. Deliberate ordering (the Spec
      035 record): any recovery round changes
      claim text, and the freeze digest is
      computed over the recovered register
      exactly once, at freeze.
- [x] **L4 — Freeze.** `freeze.md` finalised;
      `freeze.json` computed over the recovered
      register and the finalised freeze texts by
      `build_freeze.py`; freeze tests pin the
      digest replay, the definition constants,
      the register integrity, the freeze-hook
      artifacts, and the cited records (gate and
      census constants, the committed pins, the
      Spec 059 closure figures). DD-066-4
      confirmed (halt threshold and denominator),
      DD-066-5 (stratum and seed), DD-066-8 (no
      OSF registration), DD-066-9 (phase
      allocation Phase-428), and DD-066-10 (the
      gate reading) decided at the freeze
      (`adjudication.md` §4).
- [ ] **L5 — Freeze PR merged**, house gates
      green from the run's own conclusions
      (7 of 7 jobs). *(This task closes with the
      merge; the merge commit and CI run are
      recorded here by append in the execution
      landing, the house form.)* No anchor or register
      consequence exists under this spec, so no
      foundation gate applies — stated openly in
      spec §7.
- [ ] **L6 — Gate state.** The Phase-130 gate
      is on record before any processing
      (restricted store PROVENANCE entry 22,
      recorded at intake 2026-10-20) and the
      portion PDF hash was re-verified at this
      draft (`adjudication.md` §2). No OSF
      registration is filed for this act
      (DD-066-8).

## Execution (Phase-428) — under the frozen contract and the owner's approval of 2026-10-21

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run. The
      build's row-level working files are
      written only in the restricted local store.
- [ ] **E2 — Step 0** (spec §7), in the frozen
      order: 0.1 gate record on record, naming
      this material restricted, quoted in the
      outcome; 0.2 every pin recomputed (two
      routes where committed); 0.3 candidate
      sets re-derived to the spec §3 counts;
      0.4 repo cleanliness (no portion-derived
      row-level file in tree or index). Any
      failure stops the execution as itself,
      before any candidate is graded.
- [ ] **E3 — Grading** (spec §5.3): candidate
      generation (the 2,101, in the two §3
      sets); ladder grading of the full census;
      low-confidence hand-verification against
      the page renders; the hand-check stratum
      (seed 20261021, DD-066-5) and its cause
      attribution; the medium-coverage
      determination; the §6 aggregates.
- [ ] **E4 — Halt evaluation** (spec §5.5):
      conflict share of all graded candidates
      against 20%; the true-non-identity
      tripwire. On halt: no extension index is
      committed, no merged layer is pinned, and
      the outcome is INTAKE COMPLETE —
      CATALOGUE EXTENSION HALTED.
- [ ] **E5 — Build and pinning** (spec §§5.2,
      5.6), on pass only: the merged catalogue
      layer v2 in the local store (collisions
      recorded; the existing object stands); the
      Phase-130 validator over the extension
      dataset form (license_basis = the entry-22
      gate, quoted); the extension index
      committed under `data/intake/`.
- [ ] **E6 — Outcome:** the aggregates, the
      halt verdict with its arithmetic, the
      §5.7 projection (labelled), and the pins
      recorded in this spec's `outcome.md`, the
      root LEDGER, and the phase machine record;
      the local products named by filename and
      row count only; repo cleanliness
      re-checked before the outcome commit;
      foundation read-back after the outcome
      lands; nothing written into any frozen
      record, the PRED register, or the anchors.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
