# Spec 051 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the campaign plan approved
> as written 2026-10-21, the portfolio triage
> of the same date, and the Roif preprint
> verification of the same date — drafting
> only). The freeze and the execution of
> Spec 051 are separate later owner acts.
> This spec's freeze follows Spec 047's freeze
> in dependency order. All execution products
> are held under the Roif gate (spec §9).

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-10 arrow-sign distribution test of
      claim `manual_003`, consuming Asset B as
      frozen), H13 (epistemic boundaries stated
      in spec §10), H15/H23 (execution shape is
      graph-first, spec §13), H16 (data from
      the registered sources of record: the
      pinned claim and Phase-104 records, the
      pinned roles file, the pinned gazetteer
      spine, Asset B as frozen by Spec 047, and
      the counting layer exported and pinned at
      step 0 — never values typed into a
      script), H24 (no private correspondence
      in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F051-C01…C20) drafted in
      the Spec 032–047 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-051-7). Acceptance
      tests were derived twice, independently,
      per claim; the five disagreements and
      their resolutions are recorded in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state
      reported from the run's own conclusions.
- [ ] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the freeze
      act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register, under
      the program's current aee pin (engine
      1.5.x, re-checked at the freeze rather
      than assumed); the gate is **pass**, and
      a stricter outcome blocks the freeze until
      its named recovery is complete and
      recorded. Deliberate ordering (the Spec
      035/038 record): any recovery round
      changes claim text, and the freeze digest
      is computed over the recovered register
      exactly once, at freeze.
- [ ] **L5 — Freeze-decision items.** The
      freeze decides the OPEN items of
      `adjudication.md` §5 (OSF registration
      under E-1 with its R-7 reading confirmed;
      permutation and class-addition seeds; the
      thin-asset reading DD-051-5, confirmed
      consistently with Spec 047's freeze; the
      Fisher exact test's status; the second
      corpus layer's role; the contract-drift
      check against Spec 047's frozen §4; the
      counting-layer export form), and confirms
      or openly overturns DD-051-1, DD-051-2,
      DD-051-3, and DD-051-8.
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided, and
      Spec 047 already frozen: hooks recorded,
      `freeze.md` finalised, `freeze.json`
      computed over the recovered register and
      finalised texts, every spec §2 pin
      re-asserted against the merged record,
      **Asset B's digest taken as this spec's
      pin from Spec 047's freeze record and
      step-1 outcome record**, and the execution
      phase number allocated (DD-051-6).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.3): input integrity against the
      freeze pins; Asset B digest assertion
      (a mismatch closes the run as INVALID, an
      unfrozen or unsound asset as NOT-RUN, per
      the §6 wordings); Asset B form check and
      testable-set derivation. Any failure stops
      the run before a class is read for a test.
- [ ] **E3 — Step 0, part 2** (gates 0.4–0.5):
      counting layer identified, exported in
      full, and pinned by digest; M391 census
      reproduced exactly (75 / 52 / 16 / 14 / 11 /
      10 / 10 / 3 / 2, total 193) with per-site
      totals and mean lengths derived; join
      census accounting for every record exactly
      once, non-spine sites named with their
      M391 counts. Any failure stops the run as
      INVALID before any share exists.
- [ ] **E4 — Step 0, part 3** (gate 0.6):
      test-population census (counts only) and
      the floors — at least 3 testable
      gateway/border sites carrying M391, both
      sides of the comparison non-empty. A floor
      failure ends the execution as INCONCLUSIVE
      with the classification as the finding.
- [ ] **E5 — Primary and rival score** (spec
      §§5.2–5.4): per-site shares, R, the
      9,999-shuffle permutation test at the
      freeze-recorded seed, the Fisher exact
      test reported beside it, R_city, both
      regression fits with the class-addition
      outcome (ADDS / SIZE-ONLY / NEITHER) and
      the text-length description; verdict by
      the frozen partition; §5.5 sensitivities
      reported beside the primary.
- [ ] **E6 — Outcome:** the §8 record —
      results JSON and report under the
      headline rules (corpus label, Asset B
      digest and status counts, join census,
      per-site and per-class quantities, the
      rival score, the fence sentence), the §6
      pre-written wording for the outcome
      reached, the appended outcome in this
      directory, the dated append to the claim
      `indus_valley_script_deciphered_from_myth_65ff0a26_manual_003`'s
      record, and the LEDGER entry; anchors
      asserted byte-identical before and after;
      foundation check reported as measured.
      All products held under the Roif gate:
      campaign reporting names this member only
      as "executed — held under the Roif gate".

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
