# Spec 047 — Tasks

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
> wave; execution runs as Phase-406 under the
> frozen contract, gated as L7 and the
> execution list below record. All execution
> products are held under the Roif gate
> (spec §10).

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the D-09 distribution test of the ledger
      thesis and the Asset B build it requires),
      H13 (epistemic boundaries stated in spec
      §11), H15/H23 (execution shape is
      graph-first, spec §14), H16 (data from
      the registered sources of record: the
      pinned gazetteer spine, the pinned primary
      layer, the pinned crosswalk, and published
      sources entered as cited data), H24 (no
      private correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F047-C01…C19) drafted in
      the Spec 032–042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-047-7). Acceptance
      tests were derived twice, independently,
      per claim; the four disagreements and
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
      aee 1.5.0 (the `glossa-aee150` venv; the
      `glossa-aee153` venv stands empty on this
      machine, recorded in
      `aee/freeze-aee-note.md`): after_specify
      cleared in two adjudicated rounds over the
      recovered register (a loadability recovery
      0.5-draft → 0.6-draft, then 67 failure
      modes over 0.6-draft recovered to
      0.7-draft); after_plan and after_tasks
      clean at first pass. At every hook: zero
      correctness failure modes and no claim
      below the 0.70 threshold (minimum
      propagated 0.72); the residual records are
      the 19 FR-2.3 draft-cap records (the
      DD-047-16 gate reading). Recorded in
      `aee/freeze-aee-note.md`.
- [x] **L5 — Freeze-decision items.** Decided
      on the record in `adjudication.md` §7:
      DD-047-8 (OSF registration under E-1, R-7
      reading confirmed), DD-047-9 (second
      corpus layer unused), DD-047-10 (seed
      20261021), DD-047-11 (D-10 proceeds under
      its own gates against a thin Asset B),
      DD-047-12 (spine-only population
      confirmed), DD-047-13 (all-UNMAPPED case
      proceeds on measure (a) alone), DD-047-14
      (§4.3 verification pass suffices).
      DD-047-1 and DD-047-2 are CONFIRMED as
      drafted.
- [x] **L6 — Freeze.** Executed 2026-10-21:
      hooks recorded (L4), `freeze.md`
      finalised, `freeze.json` computed exactly
      once over the recovered register (0.7-draft)
      and the finalised freeze texts, every spec
      §2 pin re-asserted against the merged
      record by two independent routes
      (contents-API raw and git-blob at `main`
      `83b6a563`; both routes agree on every
      file — `freeze.md` §2), the freeze tests
      proven able to fail (mutation → red →
      restore → green; `freeze.md` §6), and the
      execution phase allocated as Phase-406
      (DD-047-15).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).
      This PR is the item's vehicle; its merge
      on green CI completes it. Execution below
      stays gated on the OSF registration's
      approval act (the parent's approval
      click; DD-047-8) and a separate execution
      order.

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0** (spec §3): input
      integrity against the freeze pins; spine
      reproduction (36 rows, 30 clusters); join
      census accounting for every primary-layer
      record exactly once. Any failure stops
      the run as INVALID before any
      classification entry exists.
- [ ] **E3 — Step 1a, Asset B build** (spec
      §4): cited-data entry on the gazetteer
      spine under the two-source agreement
      rule; §4.3 verification pass; build gates
      B1–B4; freeze of the asset file with its
      SHA-256 digest, row count, and status
      counts recorded in the step-1 record. A
      build-gate failure closes the spec at
      step 1 and marks D-10 not-run by
      dependency closure.
- [ ] **E4 — Step 1b, ledger-sign list**
      (spec §5): extraction from the two
      Academia.edu postings of record only,
      crosswalk mapping, UNMAPPED entries
      recorded, list frozen in the same step-1
      act under its own digest; extraction
      census published.
- [ ] **E5 — Step 2, classification gate**
      (spec §6.3): testable count and both
      sides non-empty, checked against the
      frozen asset before any distribution
      quantity exists. A fired gate ends the
      execution as INCONCLUSIVE with the
      classification as the finding.
- [ ] **E6 — Step 2, primary and sensitivities**
      (spec §§6.2, 6.4): inscription-share
      ratio, 9,999-shuffle permutation test at
      the freeze-recorded seed, ledger-sign
      ratio with per-sign counts; each-source-
      alone and five-largest recomputations
      reported beside the primary, never
      verdict-changing.
- [ ] **E7 — Outcome:** the §9 record —
      results JSON and report under the
      headline rules (corpus label, Asset B
      digest and status counts, join census,
      primary quantities, the component fence),
      the §7 pre-written wording for the
      outcome reached, the appended outcome in
      this directory, the dated component-scoped
      append to the claim
      `indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`'s
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
