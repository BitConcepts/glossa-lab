# Spec 055 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the runnable-experiments
> campaign plan approved AS WRITTEN on
> 2026-10-21 — D-15 is campaign member 11 —
> the portfolio triage of the same date, and
> design D-15; drafting only). The freeze
> and the execution of Spec 055 are separate
> later acts under the campaign. Design D-16
> is not a task of this spec in any phase
> (campaign decision E-7).

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-15 identification and
      numeral-behaviour test for this one
      fragment; D-16 expressly out of scope
      under E-7), H13 (epistemic boundaries
      stated in spec §9), H15/H23 (execution
      shape is graph-first, spec §12), H16
      (data from the registered sources of
      record: the held source document, the
      pinned crosswalk registry, the strict
      corpus as pinned at gate 0.4), H24 (no
      private correspondence in the repo),
      H26 (no semantic-anchoring machinery is
      used as a gate for anything in this
      spec — the test is a source recovery
      and a distributional comparison).
- [x] **L2 — Claims-first register.**
      `claims.json` (F055-C01…C15) drafted in
      the Spec 042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-055-8). Acceptance
      tests were derived twice independently;
      disagreements and resolutions are
      recorded in `adjudication.md` §5. The
      AEE lifecycle hooks ran at the freeze
      act (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      freeze decision, CI state reported from
      the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE).**
      Run at the freeze act, 2026-10-21, under
      aee 1.5.0 (the `glossa-aee150` venv):
      after_specify cleared in adjudicated
      rounds over the recovered register (a
      loadability recovery 0.5-draft → 0.6-draft,
      then 53 failure modes over 0.6-draft
      recovered to 0.7-draft, with a final
      restatement of F055-C13's head clearing
      the last correctness records);
      after_plan and after_tasks clean at first
      pass on the final register. At every
      hook: zero correctness failure modes and
      no claim below the 0.70 threshold
      (minimum propagated 0.72); the residual
      records are the 15 FR-2.3 draft-cap
      records (the DD-055-18 gate reading).
      Recorded in `aee/freeze-aee-note.md`.
- [x] **L5 — Freeze-decision items.** Decided
      on the record in `adjudication.md` §7:
      DD-055-9 (OSF registration under E-1),
      DD-055-10 (OPEN-1: the §6 recovery-record
      form confirmed — `source-table-recovery.json`,
      schema `glossa.source-table-recovery/1`,
      on every terminal outcome), DD-055-11
      (OPEN-2: control-set rule and directional
      median clause confirmed), DD-055-12
      (OPEN-3: occurrence floor confirmed at
      5), DD-055-13 (OPEN-4: corpus pinning
      posture confirmed — pinned at gate 0.4,
      no freeze-time pin, with the reason),
      DD-055-14 (OPEN-5: hedged numeral-set
      members excluded, listed separately),
      DD-055-15 (OPEN-6: positional entropy
      confirmed as drafted), DD-055-16
      (OPEN-7: dry-run on a non-target sign
      required), DD-055-17 (Phase-414),
      DD-055-18 (DD-038-10 gate reading).
      DD-055-1 to DD-055-8 are CONFIRMED as
      drafted. The freeze does not adjudicate
      sign 700: it is located by locator only
      in the recovery form (F055-C09), and the
      registry trap (the `W900` cell on the
      P154 row; matching by drawn form only,
      F055-C07) is carried as drafted.
- [x] **L6 — Freeze.** Executed 2026-10-21:
      hooks recorded (L4), `freeze.md`
      finalised, `freeze.json` computed
      exactly once over the recovered register
      (0.7-draft) and the finalised freeze
      texts, every spec §2 pin re-asserted
      against the merged record by two
      independent routes (contents-API raw
      and git-blob at `main` `3af269f6`; both
      routes agree on every file —
      `adjudication.md` §8), the freeze tests
      proven able to fail (mutation → red →
      restore → green; `freeze.md` §6), the
      spec's OSF contract registration filed
      under E-1 (DD-055-9), and the execution
      phase allocated as Phase-414
      (DD-055-17).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and the campaign's execution pass

Campaign order (plan Part 4, Wave 3):
**Spec 055 executes in group 2, the
independent executions.** Its recovery record
is a record of this spec; no campaign member
consumes it, and D-16 takes nothing from this
execution except through its own future
planning gate.

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0** (spec §3 gates
      0.1–0.3): input integrity against the
      freeze pins; source document produced
      from the held copy with the §1 material
      located verbatim; recovery-before-verdict
      ordering asserted. Any failure closes
      the run as CLOSED AT STEP 0 in the named
      class, produces `source-table-recovery.json`
      in its closure form, and ends the
      execution here.
- [ ] **E3 — Step 1, the recovery** (spec
      §§4, 6): the source's sign list named
      from the document's own text, naming
      statements quoted with locators; the
      full sign-900 material recovered
      verbatim; the drawn sign matched by
      drawn form to a crosswalk-registry entry
      or to the named list's entry for 900,
      citation attached. Number- and
      string-matching are forbidden
      (F055-C07). The recovered document's
      sign-700 statements are located for the
      record's locator block and adjudicated
      in no way (F055-C09). A failure closes
      the run as IDENTIFICATION FAILED in the
      named sub-class, with the closure-form
      recovery record.
- [ ] **E4 — Step 2 gate and pre-counting
      record** (spec §3 gate 0.4; §5.1): the
      strict-corpus layer identified,
      exported, and pinned by digest; the
      identified sign's occurrence census in
      it (absent or below the floor closes as
      IDENTIFIED — TOO FEW OCCURRENCES TO
      TEST, count named); the known-numeral
      set fixed from published identifications
      (target excluded) and the control set
      selected by the frozen rule — all before
      any §5.2 measure exists.
- [ ] **E5 — Step 2, the behaviour test**
      (spec §5): the three measures computed
      identically for the target, every
      numeral-set member, and every control
      sign; the outcome assigned by the §5.3
      mapping alone. The source document's
      own argument for six is not consulted
      as evidence at this stage (F055-C15).
- [ ] **E6 — Outcome** (spec §8): the §5.4
      wording for the outcome reached;
      `source-table-recovery.json` as produced
      (on every terminal outcome); the results
      JSON where step 2 ran; the outcome append
      in this directory carrying the §8
      reporting obligations, including the
      chain sentence on D-16 and E-7; the
      appended entry on the claim
      `ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`'s
      record; the LEDGER entry; anchors
      asserted byte-identical before and
      after; foundation check reported as
      measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
