# Spec 057 — Tasks

> ## PLAN — FROZEN 2026-10-21 (execution Phase-419)
>
> Adjudication inputs are recorded in
> `adjudication.md` (the runnable-experiments
> campaign plan approved by the owner as
> written on 2026-10-21 — member 14 — and the
> portfolio triage of the same date, drafting
> only). The freeze and the execution of
> Spec 057 are separate later acts.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-19 re-extraction of the five
      passages), H13 (epistemic boundaries
      stated in spec §9), H15/H23 (execution
      shape is graph-first, spec §12), H16
      (data from the registered sources of
      record: the five pinned held texts and
      source documents of spec §2), H24 (no
      private correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F057-C01…C15) drafted in
      the Spec 032–046 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-057-9). The AEE
      lifecycle hooks have **not** run on this
      register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state
      reported from the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE
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
- [x] **L5 — Freeze-decision items.** The
      freeze decides OPEN-1 (the HEADING NOT
      PRESENT sub-state, DD-057-3), OPEN-2
      (the S-3 delimitation), and OPEN-3
      (recovered-claim intake inside the
      execution, DD-057-6), files the OSF
      contract registration under the
      campaign's E-1 policy (OPEN-4), and
      confirms or openly overturns DD-057-5
      and DD-057-7.
- [x] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §2 pin re-asserted against
      the merged record, and the execution
      phase number allocated (DD-057-8).
      **Done at the freeze act of 2026-10-21:**
      hooks PASS over the recovered register
      (0.8-draft) under aee 1.5.3 — zero
      correctness failure modes, no claim below
      0.70 (minimum 0.72), draft-cap records
      only (DD-057-17 gate reading); every §2
      pin re-asserted two-route at `main`
      `770155de`; OPEN-1 to OPEN-3 resolved as
      DD-057-10 to DD-057-12 in
      `adjudication.md` §7, DD-057-5 and
      DD-057-7 confirmed (DD-057-14,
      DD-057-15); Phase-419 allocated
      (DD-057-16); OSF contract registration
      filed under E-1 (DD-057-13; filing record
      in `osf-spec-registration.md`).
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [x] **E2 — Step 0** (spec §3): input
      integrity against the freeze pins;
      source-set integrity against the
      recorded merge; gate verdicts recorded
      before any passage is read. A failure
      closes the run at step 0 in the class
      named, with no source accounted.
- [x] **E3 — Location** (spec §§4–5): for
      each source in §2.1 order, the stated
      search where the pinned cleaned text is
      absent; heading location under the
      heading-form rule; delimitation; the
      verbatim passage artifact with its
      SHA-256 and locator on the source's row.
- [x] **E4 — Accounting** (spec §6): exactly
      one outcome per source — CLAIM
      RECOVERED (recovered claim through
      normal intake at the created stage, per
      OPEN-3), PASSAGE EMPTY (passage quoted
      as evidence), or SOURCE UNLOCATED
      (sub-state, full search log, named
      unblocking act). Five rows, no fewer.
- [x] **E5 — Outcome:** the §8 record —
      accounting table, passage artifacts,
      intake records, the §7 headline class
      with its counts shown, the §7.2
      disposition note appended to the
      heading record, and the LEDGER entry;
      anchors asserted byte-identical before
      and after; foundation check reported as
      measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
