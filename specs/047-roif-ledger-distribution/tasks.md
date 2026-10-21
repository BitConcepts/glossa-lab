# Spec 047 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the campaign plan approved
> as written 2026-10-21, the portfolio triage
> of the same date, and the Roif preprint
> verification of the same date — drafting
> only). The freeze and the execution of
> Spec 047 are separate later owner acts.
> All execution products are held under the
> Roif gate (spec §10).

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
      `adjudication.md` §5 (second corpus layer;
      permutation seed; D-10 against a thin
      Asset B; spine-only population; the
      all-UNMAPPED ledger case; OSF registration
      under E-1 with its R-7 reading confirmed;
      classification audit), and confirms or
      openly overturns DD-047-1 and DD-047-2.
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` computed over the recovered
      register and finalised texts, every spec
      §2 pin re-asserted against the merged
      record, and the execution phase number
      allocated (DD-047-6).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

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
