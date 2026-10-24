# Spec 054 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the campaign plan
> approved AS WRITTEN on 2026-10-21, member 7;
> the portfolio triage of the same date,
> drafting only; and Spec 045's DD-045-4
> touchpoint). The freeze and the execution
> of Spec 054 are separate later owner acts.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-08 falsifier-and-rerun act), H13
      (epistemic boundaries stated in spec
      §7), H15/H23 (execution shape is
      graph-first, spec §11), H16 (data from
      the registered sources of record: the
      pinned Phase-43 files, the database-held
      V3 corpus pinned at gate 0.3, the Holdat
      layer pinned at gate 0.4, the pinned
      crosswalk), H24 (no private
      correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F054-C01…C15) drafted in
      the Spec 042–048 register shape, at
      `0.5-draft`, with `observed_at` carried
      on evidence items from this draft
      (DD-054-8) and the acceptance tests for
      each claim derived twice independently,
      disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state
      reported from the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE
      — run at the amended freeze, 2026-10-23).** At the
      freeze act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register;
      the gate is **pass**, and a stricter
      outcome blocks the freeze until its
      named recovery is complete and
      recorded. Deliberate ordering (the
      Spec 035/038 record): any recovery
      round changes claim text, and the
      freeze digest is computed over the
      recovered register exactly once, at
      freeze. Freeze mechanics are
      re-checked against the adopted aee
      1.5.x engine at the freeze rather than
      assumed from pre-adoption habit
      (campaign Part 4, Wave 2).
- [x] **L5 — Freeze-decision items.** The
      freeze decides OPEN-054-1 (the battery's
      threshold rule, stated from the record),
      OPEN-054-2 ("strict", operationally),
      OPEN-054-3 (the occurrence floor's value
      and DD-054-5's confirmation),
      OPEN-054-4 (the crosswalk of record and
      DD-054-4), OPEN-054-5 (the shuffle
      null's construction and seed),
      OPEN-054-6 (the Spec 045 reconciliation
      touchpoint, spec §5.2), and OPEN-054-7
      (DD-054-2's precedence rule), and
      confirms or openly overturns
      DD-054-1…DD-054-6.
- [x] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §2 pin re-asserted against
      the merged record, the execution phase
      number allocated (OPEN-054-9),
      the OSF contract registration filed
      under campaign decision E-1 if L5
      confirms OPEN-054-8's proposal, and —
      as part of this same act, not of any
      execution — **the §4 falsifier append
      made to the record of
      `yadav_2009_arxiv_manual_002`, verbatim**
      (claim F054-C04).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.2): input integrity against the
      freeze pins; the original 40/20 sets
      exhibited sign by sign from a pinned
      source. A failure stops the run as
      INVALID (0.1) or ORIGINAL SETS NOT
      EXHIBITABLE (0.2) before any quantity.
- [ ] **E3 — Step 0, part 2** (gates
      0.3–0.5): strict corpus identified,
      exported, pinned, and the battery
      reproduced against the recorded
      reference points (STRICT CORPUS NOT
      PINNABLE / BATTERY NOT REPRODUCED on
      failure); Holdat layer pinned, per-sign
      crosswalk and both segmentation
      statements recorded (SECOND ARM NOT
      RUNNABLE on failure); census under the
      frozen floor (a THIN closure ends the
      execution here, with the census as its
      finding).
- [ ] **E4 — Arms and overlap** (spec §5):
      arm 1 on the pinned strict corpus; arm
      2 on the Holdat layer through the
      crosswalk, conflict pairs reported
      separately; reappearance per set per
      arm; the pooled and per-class overlap
      against the frozen 999-shuffle null;
      the §5.1 sensitivity beside the primary.
- [ ] **E5 — Outcome:** the §9 record —
      results JSON and report under the
      headline rules (the falsifier verbatim
      with its append date, the full step-0
      record, per-arm per-sign tables, the
      reappearance counts, the overlap and
      null record, the sensitivity, and the
      headline word in §6's pre-written
      wording), the appended outcome in this
      directory, the dated outcome append to
      `yadav_2009_arxiv_manual_002`'s record,
      and the LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## Amendment — 2026-10-23 (owner mini-gate)

Drafted under Item 3 of the owner-approved
waiting-decisions package of 2026-10-23. The
amendment returns to the owner as a mini-gate;
it does not freeze this spec and it appends
nothing to any claim record.

- [x] **A1 — Settled rulings recorded.**
      `adjudication.md` §8: the §7.5(2)
      falsifier design adopted (new battery
      NB-1 producing its own sets in both
      arms; the three conditions re-aimed —
      per-class reappearance < ½, pooled
      overlap vs the 999-shuffle null's 95th
      percentile, DD-054-2 precedence,
      DD-054-5 denominator discipline;
      verdict wordings rewritten, no
      RE-EARNED); the §7.5(3) generator act
      decided with it.
- [x] **A2 — Amendment drafted.**
      `amendment.md`: the amended statement;
      battery NB-1 specified in full; the
      decision procedure (sets, reappearance,
      overlap null with its construction
      stated — answering OPEN-054-5 —
      precedence, denominators); amended
      step-0 gates (BATTERY NOT REPRODUCED
      replaced by determinism; ORIGINAL SETS
      NOT EXHIBITABLE retired as a closure,
      its fact retained); the exact falsifier
      text for the amended freeze; rewritten
      verdict wordings. Claims F054-C16…C19
      appended to the register at 0.5-draft.
- [x] **A3 — Generator fix prepared.**
      Separate commit in this PR:
      `glossa-indus/scripts/indus_claims.py`
      carry-over gains `falsification_condition`
      (dated comment in the block's style).
      Proven both ways in a scratch tree
      (amendment.md §7): unmodified generator
      drops an appended condition on
      regeneration; fixed generator preserves
      it verbatim, with no other change beyond
      baseline timestamps.
- [x] **A4 — Owner mini-gate.** The owner
      approves, amends, or declines the
      amendment (amendment.md §11 lists the
      decisions). On approval: L4 runs over
      the recovered register; L5 is decided
      **as amended** — including the falsifier
      append (amendment.md §8 text) performed
      as a freeze act and the claim-record
      hash registered **after** the append —
      and the freeze path resumes. The
      generator commit lands with this PR on
      approval of the amendment; on decline it
      is withdrawn with the draft.
