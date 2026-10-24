# Spec 052 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the runnable-experiments
> campaign plan approved by the owner as
> written on 2026-10-21 — member 1, decision
> E-3 binding this spec to arm A only — the
> portfolio triage of the same date, and
> design D-01). The freeze and the execution
> of Spec 052 are separate later acts.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      design D-01 arm A: the Soviet-compilation
      consistency check; arm B excluded per
      campaign E-3), H13 (epistemic boundaries
      stated in spec §7), H15/H23 (execution
      shape is graph-first, spec §10), H16
      (data from the registered sources of
      record: the pinned Phase-121 dataset,
      the pinned Phase-43 results record, and
      crosswalk v1), H24 (no private
      correspondence in the repo), H26 (no
      semantic-anchoring machinery anywhere in
      this design).
- [x] **L2 — Claims-first register.**
      `claims.json` (F052-C01…C15) drafted in
      the Spec 032–042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-052-7). Acceptance
      tests derived twice independently per
      claim; disagreements and resolutions
      recorded in `adjudication.md` §3. The
      AEE lifecycle hooks have **not** run on
      this register (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      freeze decision, CI state reported from
      the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the
      freeze act, run `run_aee.py assess`
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
      freeze decides the OPEN items of
      `adjudication.md` §5: the gate-0.5
      battery definition (every element
      derived from the Phase-43 record and
      cited, or the spec does not freeze);
      the record-to-battery-input mapping
      (including Marshall → Mahadevan passage,
      the K1965-T4 entry form, the opening
      formula's identity, and the TOO THIN
      count's derivation); DD-052-3 (PARTIAL)
      and DD-052-5 (BATTERY NOT PINNABLE)
      confirmed or openly replaced; the OSF
      filing executed under campaign E-1; and
      the battery-reproduction question
      (adjudication §5, item 6).
- [x] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts
      (including the frozen battery definition
      and mapping), every spec §2 pin
      re-asserted against the merged record,
      and the execution phase number allocated
      (DD-052-6).
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

**Freeze note — 2026-10-23.** E1–E5 below were
drafted for the unamended (Soviet) design and are
retained as its record. The amended run's execution
is not tasked here: it awaits a separate owner
order, and its tasking will be written against the
frozen amendment (NB-1, gates A–D) when that order
comes. No item below is an instruction to execute
the amended run.

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run. The
      script implements the frozen battery
      definition and mapping of L5/L6, and no
      other rules.
- [ ] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.3): Soviet-records and battery pins
      against the freeze values; record counts
      and provenance reproduced; printed
      anomalies asserted as printed. Any
      failure stops the run as INVALID before
      any census.
- [ ] **E3 — Step 0, part 2** (gates 0.4–0.6):
      battery definition verified complete
      against gate 0.5's list (an incomplete
      definition closes the run as BATTERY NOT
      PINNABLE); dataset-form census published
      (total, per-sign positional, and mapped
      counts); TOO THIN gate applied from the
      census (a TOO THIN closure ends the
      execution here, with the census as its
      finding).
- [ ] **E4 — Primary** (spec §4): the frozen
      battery on the mapped Soviet inputs;
      per-sign final- and initial-position
      rates with exact counts; the opening
      formula against its frozen chance
      baseline (a baseline that cannot be
      computed as frozen closes the run as NOT
      ADJUDICATED); crosswalk-conflict pairs
      reported separately.
- [ ] **E5 — Outcome:** the §6 record —
      results JSON and report under the
      headline rules (dataset label, census,
      per-sign quantities, conflict-pair
      report, the outcome word or stop class),
      the appended outcome in this directory,
      the dated appends to the parent claim's
      record and to each of the three
      fragments' records in the same words
      (spec §4.2), and the LEDGER entry;
      anchors asserted byte-identical before
      and after; foundation check reported as
      measured. No arm B task exists in this
      list, and none may be added by an
      execution act (campaign E-3).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## Amendment — 2026-10-23 (owner mini-gate)

Drafted under Item 2 of the owner-approved
waiting-decisions package of 2026-10-23. The
amendment returns to the owner as a mini-gate;
it does not freeze this spec.

- [x] **A1 — Settled rulings recorded.**
      `adjudication.md` §9: ruling (a) — no
      battery element, the chance baseline
      included, invented or borrowed under the
      Phase-43 name; the amendment route adopted
      (§8.5 route (2)); the recovery route stays
      open. Ruling (b) — the Soviet mapping
      impossible on the current record; arm A as
      designed closed; the Soviet tables retired
      from the member.
- [x] **A2 — Amendment drafted.**
      `amendment.md`: battery NB-1 specified in
      full (elements NB-1.1–NB-1.9, every
      constant with its derivation or its
      labelled basis); the re-scoped data (the
      Shakti corpus layer; Spec 068's primary
      population; restricted venue; pins at
      freeze); amended step-0 gates A–D;
      outcome semantics re-pointed. Claims
      F052-C16…C19 appended to the register at
      0.5-draft.
- [x] **A3 — Owner mini-gate.** The owner
      approves, amends, or declines the
      amendment (amendment.md §7 lists the three
      decisions). On approval: L4 runs over the
      recovered register; L5 is decided **as
      amended** — its battery-derivation and
      Soviet-mapping items are closed by
      adjudication §9, not by the freeze — and
      the freeze path (L5 remainder, L6, L7)
      resumes. Nothing in the amendment
      executes before a separate execution
      order, and no task is added to the
      Execution list by this amendment.
