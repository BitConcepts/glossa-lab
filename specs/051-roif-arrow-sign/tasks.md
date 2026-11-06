# Spec 051 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the campaign plan approved
> as written 2026-10-21, the portfolio triage
> of the same date, and the Roif preprint
> verification of the same date — drafting
> inputs; the freeze decisions are §7 of the
> same record). Frozen at the freeze act of
> 2026-10-21 in the campaign's Wave 2 freeze
> wave; execution runs as Phase-409 under the
> frozen contract, gated as L7 and the
> execution list below record. This spec's
> freeze follows Spec 047's freeze in
> dependency order. All execution products
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
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE).**
      Run at the freeze act, 2026-10-21, under
      aee 1.5.0 (the `glossa-aee150` venv):
      after_specify cleared in two adjudicated
      rounds over the recovered register (a
      loadability recovery 0.5-draft → 0.6-draft,
      then 75 failure modes over 0.6-draft
      recovered to 0.7-draft); after_plan and
      after_tasks clean at first pass. At every
      hook: zero correctness failure modes and
      no claim below the 0.70 threshold
      (minimum propagated 0.72); the residual
      records are the 20 FR-2.3 draft-cap
      records (the DD-051-16 gate reading).
      Recorded in `aee/freeze-aee-note.md`.
- [x] **L5 — Freeze-decision items.** Decided
      on the record in `adjudication.md` §7:
      DD-051-9 (OSF registration under E-1, R-7
      reading confirmed), DD-051-10 (seed
      20261021 for both permutation tests),
      DD-051-11 (Fisher exact test reported, not
      verdict-bearing), DD-051-12 (second corpus
      layer unused), DD-051-13 (counting-layer
      identify/export/pin posture confirmed),
      DD-051-14 (Asset B pin timing: contract
      anchor plus step-1 outcome record as the
      fixed pin source; gate 0.2 asserts at
      execution), and the contract-drift check
      against Spec 047's frozen §4 (no drift).
      DD-051-1, DD-051-2, DD-051-3, DD-051-5, and
      DD-051-8 are CONFIRMED as drafted;
      DD-051-5's consistency with Spec 047's
      DD-047-11 is recorded in §7.
- [x] **L6 — Freeze.** Executed 2026-10-21:
      hooks recorded (L4), `freeze.md` finalised,
      `freeze.json` computed exactly once over
      the recovered register (0.7-draft) and the
      finalised freeze texts, every spec §2 pin
      re-asserted against the merged record by
      two independent routes (contents-API raw
      and git-blob at `main` `0cf9cd2f`; both
      routes agree on every file — `freeze.md`
      §2), the freeze tests proven able to fail
      (mutation → red → restore → green;
      `freeze.md` §6), **Asset B anchored on
      Spec 047's freeze digest with its pin
      source fixed as Spec 047's step-1 outcome
      record** (DD-051-14; no byte-digest exists
      at this freeze), and the execution phase
      allocated as Phase-409 (DD-051-15).
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).
      This PR is the item's vehicle; its merge
      on green CI completes it. Execution below
      stays gated on the OSF registration's
      approval act (the parent's approval
      click; DD-051-9) and a separate execution
      order.

## Execution — gated on the freeze and a separate execution order

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [x] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.3): input integrity against the
      freeze pins; Asset B digest assertion
      against the digest recorded in Spec 047's
      step-1 outcome record (the pin source
      fixed at the freeze, DD-051-14; a mismatch
      closes the run as INVALID, an unfrozen or
      unsound asset as NOT-RUN, per the §6
      wordings); Asset B form check and
      testable-set derivation. Any failure stops
      the run before a class is read for a test.
- [x] **E3 — Step 0, part 2** (gates 0.4–0.5):
      counting layer identified, exported in
      full, and pinned by digest; M391 census
      reproduced exactly (75 / 52 / 16 / 14 / 11 /
      10 / 10 / 3 / 2, total 193) with per-site
      totals and mean lengths derived; join
      census accounting for every record exactly
      once, non-spine sites named with their
      M391 counts. Any failure stops the run as
      INVALID before any share exists.
- [x] **E4 — Step 0, part 3** (gate 0.6):
      test-population census (counts only) and
      the floors — at least 3 testable
      gateway/border sites carrying M391, both
      sides of the comparison non-empty. A floor
      failure ends the execution as INCONCLUSIVE
      with the classification as the finding.
- [ ] **E5 — Primary and rival score** (spec
      §§5.2–5.4): per-site shares, R, the
      9,999-shuffle permutation test at the
      freeze-recorded seed 20261021, the Fisher
      exact test reported beside it (not
      verdict-bearing, DD-051-11), R_city, both
      regression fits with the class-addition
      outcome (ADDS / SIZE-ONLY / NEITHER) and
      the text-length description; verdict by
      the frozen partition; §5.5 sensitivities
      reported beside the primary.
- [x] **E6 — Outcome:** the §8 record —
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
