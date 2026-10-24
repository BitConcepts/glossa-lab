# Spec 045 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the runnable-experiments
> campaign approved by the owner as written
> on 2026-10-21, and the portfolio triage of
> the same date, drafting only). The freeze
> was completed on 2026-10-21 (adjudication
> §7, DD-045-9 to DD-045-21); the execution of
> Spec 045 remains a separate later act under
> the campaign's Waves 2 and 3.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      design D-05 and the Asset A build it
      owns), H13 (epistemic boundaries stated
      in spec §8), H15/H23 (execution shape
      is graph-first, spec §11), H16 (data
      from the registered sources of record:
      the pinned positional record, corpus
      layer, and crosswalk; Asset A labels
      from held published sources only), H24
      (no private correspondence in the
      repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F045-C01…C17) drafted in
      the Spec 042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-045-7), and each
      claim's acceptance test derived twice
      with disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR on branch
      `spec-045-hunt-depicted-kinds-draft` and
      left unmerged for the freeze decision,
      CI state reported from the run's own
      conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE
      GATE).** Run at the freeze act of
      2026-10-21 over the recovered register
      0.7-draft under aee 1.5.0: PASS on the
      DD-045-9 reading (zero correctness
      failure modes at every hook, no claim
      below the 0.70 threshold, draft-cap
      records only; `aee/freeze-aee-note.md`).
      Original gate text: at the freeze act,
      run `run_aee.py assess` after_specify,
      after_plan, and after_tasks over the
      claim register, read under the campaign's
      standing reading for draft-lifecycle
      registers; a correctness failure blocks
      the freeze until its named recovery is
      complete and recorded. Any recovery round
      changes claim text, and the freeze
      digest is computed over the recovered
      register exactly once, at freeze.
- [x] **L5 — Freeze-decision items.** Decided
      at the freeze act of 2026-10-21 in
      `adjudication.md` §7: the fit margin's
      value and fit form (DD-045-11), the
      §5.2 comparison rule's form
      (DD-045-12), the pooling threshold
      (DD-045-13), the jurisdiction-coding
      question (DD-045-14), DD-045-2/DD-045-3
      confirmed (DD-045-15), the
      second-enterer spot-check question
      (DD-045-16), the mandated repairs R1–R3
      (DD-045-17/18/19), the OSF filing
      (campaign E-1; DD-045-20), and the
      §5.2(a) reconciliation against D-08 —
      completed as a disambiguation, Spec 054
      standing as a draft with no frozen text
      (DD-045-19).
- [x] **L6 — Freeze.** Completed 2026-10-21
      under the campaign plan approved AS
      WRITTEN, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` computed over the
      recovered register and finalised texts,
      every spec §4 pin re-asserted against
      the merged record by two routes, and
      the execution phase number allocated as
      **Phase-411** (DD-045-10, resolving
      DD-045-8). Freeze order inside the
      campaign: Spec 045 freezes **before** the
      specs for D-06 and D-13, whose freezes pin
      Asset A's digest from this spec's
      execution record.
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as
      measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Asset A entry (blind).** From
      the held CISI volumes and Parpola's
      published identifications only, per
      spec §§2.3–2.4: rows entered, verbatim
      labels and citations recorded, entry
      log preserved. No positional output is
      opened during entry.
- [ ] **E2 — Dispute coding and D-18
      input.** Disputes coded per §2.5;
      the D-18 concordance table (Spec 046)
      incorporated per §2.6, or D-18's
      closure record attached (gate A2).
- [ ] **E3 — Asset A freeze.** Gates
      A1–A6 (spec §3) run in order; the
      canonical CSV and `asset-a-freeze.json`
      recorded with the digest, per-kind
      counts, input pins, and build-order
      attestation. Any gate failure closes
      the execution as ASSET FAILED and
      fires the campaign cluster rule for
      D-06 and D-13. **No join precedes this
      task.**
- [x] **E4 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
      Executed 2026-10-21 as Phase-411
      (step 0 first, under the campaign's
      Group 1 execution order): script
      `backend/scripts/phase411_hunt_depicted_step0.py`,
      node `IndusPhase411HuntDepictedStep0`,
      registration verified by import before
      the run.
- [x] **E5 — Step 0** (spec §6 gates
      0.1–0.4): input integrity; positional
      reproduction (805/2,267 and the
      40/61/20 classes); population census
      with Asset A coverage; freeze-order
      proof. Any failure stops the run as
      INVALID before any model quantity.
      Executed 2026-10-21: gate 0.1 PASS;
      **gate 0.2 FAILED — the execution
      closed INVALID** (pinned corpus
      3,463 inscriptions of length >= 3
      against the recorded 2,267; the
      40/61/20 classes exhibited by no
      record of record; the Firestore V3
      corpus the quantities belong to
      absent from the tree); gates 0.3 and
      0.4 NOT REACHED. E1–E3 (the Asset A
      build) never ran and E6 cannot run
      under this frozen contract; the
      record is `outcome.md` in this
      directory.
- [ ] **E6 — Primaries** (spec §5): models
      P and PH on the frozen split; the
      closing head-on comparison, per-sign
      scores published; the §5.3 sensitivity.
      A control failure records NOT
      ADJUDICATED with the control named.
- [x] **E7 — Outcome:** the §9 record —
      delivered 2026-10-21 in the closure
      form the INVALID outcome prescribes
      (`outcome.md`; no §5 quantities exist
      to report) —
      results JSON and report under the
      headline rules (claim identifier, Asset
      A digest and per-kind counts, both
      model fits and the frozen margin, both
      closing scores, the verdict word or
      closure class, the §8 limit in plain
      words), the appended outcome in this
      directory, and the LEDGER entry;
      anchors asserted byte-identical before
      and after; foundation check reported
      as measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
