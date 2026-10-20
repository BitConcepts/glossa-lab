# Spec 037 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Adjudication input is recorded in
> `adjudication.md` (the owner's draft order of
> 2026-10-20, drafting only). The freeze and the
> execution tasks for Phase-401 remain gated on
> the owner's separate decisions; execution is
> additionally gated on step 0 of the spec, in
> the frozen order.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and
      claim register checked against constitution
      §§I–VIII and governance H2 (spec before
      code), H6 (no scope beyond the two assessed
      candidate uses), H13 (epistemic boundaries
      stated in spec §§1, 5, 6), H15/H23 (execution
      shape is graph-first, spec §7), H16 (data
      from the registered source of record: the
      gated portion and the pinned corpus_master),
      H24 (no private correspondence in the repo;
      the restricted material itself never enters
      it). The intake census, the gate terms, and
      the in-repo pins were verified at draft time
      (`adjudication.md` §2).
- [x] **L2 — Claims-first register.** `claims.json`
      (F037-C01…C15) drafted in the Spec
      032/033/034/035/036 register shape.
      Draft-stage self-check: the dependency-
      integrity checks and the cited-record facts
      are pinned by
      `backend/tests/test_spec037_freeze.py`; the
      AEE lifecycle hooks have **not** run on this
      register (L3).
- [ ] **L3 — AEE lifecycle hooks (FREEZE GATE —
      not run on this draft).** At the freeze act,
      run `run_aee.py assess` after_specify,
      after_plan, and after_tasks over the claim
      register; the gate is **pass**, and a
      stricter outcome blocks the freeze until its
      named recovery is complete and recorded.
      Deliberate ordering (the Spec 035 record):
      any recovery round changes claim text, and
      the freeze digest is computed over the
      recovered register exactly once, at freeze.
- [x] **L4 — Design PR.** This draft, opened as a
      DRAFT PR and left unmerged for the owner's
      freeze decision, CI green from run
      conclusions.
- [ ] **L5 — Freeze.** On the owner's freeze
      order: hooks pass (L3), `freeze.md`
      finalised, `freeze.json` recomputed over the
      recovered register and the finalised freeze
      texts; freeze tests pin the digest replay,
      the definition constants, the register
      integrity, and the cited records (gate and
      census constants, corpus_master pin, the
      Spec 031 fence). DD-037-4 confirmed
      (halt threshold), DD-037-5, DD-037-6, and
      DD-037-7 decided at the freeze.
- [ ] **L6 — Freeze PR merged**, house gates green
      (full suite, branding sweep; no anchor or
      register consequence exists under this spec,
      so no foundation gate applies — stated
      openly in spec §7).
- [x] **L7 — Gate state.** The Phase-130 gate is
      on record before any processing (restricted
      store PROVENANCE entry 22, recorded at
      intake 2026-10-20) and the portion PDF hash
      was re-verified at this draft
      (`adjudication.md` §2). A spec-level OSF
      registration, if the freeze files one
      (DD-037-7), is recorded by append once its
      approval verifies.

## Execution (Phase-401) — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run. The
      build's row-level working files are written
      only in the restricted local store.
- [ ] **E2 — Step 0** (spec §7), in the frozen
      order: 0.1 gate record on record and naming
      this material restricted; 0.2 portion PDF
      SHA-256 equals the intake pin and the local
      table parse-validates at 2,123 × 26 with
      its intake census; 0.3 corpus_master pin;
      0.4 repo cleanliness (no portion-derived
      file in tree or index). Any failure stops
      the execution as itself, before any join is
      computed.
- [ ] **E3 — Pilot** (spec §4): candidate
      generation (the 693); ladder grading of the
      full census; the hand-check stratum (size
      and seed per the freeze's DD-037-5) and its
      cause attribution; the §4.4 aggregates.
- [ ] **E4 — Spine build** (spec §4.5): the local
      concordance table from VERIFIED joins only,
      written in the portion folder of the
      restricted store — unless the halt rule
      (§4.7) fires, in which case no spine file is
      written and the outcome is PILOT COMPLETE —
      SPINE HALTED.
- [ ] **E5 — Annex** (spec §5), if the freeze's
      DD-037-6 places it in this phase: dig-year,
      lot, and period-code aggregates from the
      pinned local table, floor caveat attached;
      local working files in the restricted store.
- [ ] **E6 — Outcome:** the aggregates and outcome
      classes recorded in this spec's `outcome.md`
      and the root LEDGER; the local products
      named by filename and row count only; repo
      cleanliness re-checked before the outcome
      commit; nothing written into any frozen
      record, the PRED register, or the anchors.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
