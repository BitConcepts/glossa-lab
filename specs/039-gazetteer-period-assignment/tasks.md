# Spec 039 — Tasks

> ## PLAN — FROZEN 2026-10-20
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's decisions of
> 2026-10-20: the act authorised and bundled with
> D-25; evidence standard Option 1 — both DECIDED;
> and the owner's sequencing instruction). The
> freeze was taken at the bundle step in
> `plan.md` §2; the execution tasks run as
> Phase-403 under the frozen contract.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and
      claim register checked against constitution
      §§I–VIII and governance H2 (spec before
      code), H6 (no scope beyond the authorised
      act), H13 (epistemic boundaries stated in
      spec §§1 and 11), H15/H23 (execution shape
      is graph-first, spec §7), H21 (foundation
      check named at execution). The governing
      facts were verified against Spec 027
      §§5–6, the gazetteer bytes on `main`, Spec
      031's frozen rule and outcome, Spec 030's
      adjudication, the Phase-394/395 records,
      and the Zenodo deposit at draft time
      (`adjudication.md` §3).
- [x] **L2 — Claims-first register.** `claims.json`
      (F039-C01…C15) drafted in the Spec
      032/033/034/035/036 register shape.
      Draft-stage self-check: the
      dependency-integrity checks and the
      cited-record facts are pinned by
      `backend/tests/test_spec039_freeze.py`; the
      AEE lifecycle hooks have **not** run on this
      register (L3).
- [x] **L3 — AEE lifecycle hooks (FREEZE GATE).**
      Run at the freeze act, 2026-10-20, under aee
      1.5.0: after_specify cleared in three
      adjudicated rounds (register recovered to
      0.7-draft); after_plan and after_tasks clean
      at first pass. At every hook: zero
      correctness failure modes and no claim below
      the 0.70 threshold; the residual records are
      the 15 FR-2.3 draft-cap records (the
      DD-039-8 gate reading). Recorded in
      `aee/freeze-aee-note.md`. Deliberate ordering
      (the Spec 035 record): any recovery round
      changes claim text, and the freeze digest is
      computed over the recovered register exactly
      once, at freeze.
- [x] **L4 — Design PR.** This draft, opened as a
      DRAFT PR and left unmerged for the freeze
      decision in the bundle sequence, CI state
      reported honestly.
- [x] **L5 — Freeze.** Executed 2026-10-20 at
      the bundle step under the owner's standing
      pipeline authorisation: hooks pass (L3),
      `freeze.md` finalised, `freeze.json`
      recomputed over the recovered register and
      the finalised freeze texts; freeze tests pin
      the digest replay, the definition constants,
      the register integrity, the freeze-hook
      artifacts, and the cited records (gazetteer
      census, the F031-C10 rule, the Phase-395
      floors and link mass). DD-039-1…DD-039-6
      decided at the freeze as recommended;
      DD-039-7 fixed the execution phase as
      Phase-403; DD-039-8 recorded the gate
      reading; the spec's own OSF contract
      registration is filed under DD-039-6.
- [x] **L6 — Freeze PR merged**, house gates green
      (foundation 0 failures, full suite, branding
      sweep).

## Execution — gated on the freeze and the bundle sequence

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [x] **E2 — Input integrity:** the gazetteer
      file hashes to the spec §2 pin; any drift
      stops the execution before evidence work.
- [x] **E3 — Evidence assembly:** per site, the
      admissible published determinations with
      locators, under the frozen source hierarchy
      (DD-039-2) and the DD-039-3 published-venue
      rule; restricted sources recorded as
      citations only.
- [x] **E4 — Mapping and assignment:** the frozen
      mapping table applied per site; contested
      flags set under spec §5; blanks recorded
      with reason codes; outputs A and B written
      and hashed.
- [x] **E5 — Margins verification step** (spec
      §8): the Phase-395 period-eligibility gate
      recomputed over the assigned gazetteer,
      reported both ways over contested
      assignments; the standing link-mass floor
      stated in writing; no Q7 machinery beyond
      the gate runs.
- [x] **E6 — Dataset new version:** the Stage 0
      Zenodo record's new version deposited
      through the release gate and recorded by
      DOI; the existing version untouched.
- [x] **E7 — Outcome:** the outcome record in
      this spec's directory completed by append,
      the root LEDGER entry, and the foundation
      check (H21); nothing written into any
      frozen record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
