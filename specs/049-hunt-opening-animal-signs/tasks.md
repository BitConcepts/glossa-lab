# Spec 049 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the runnable-experiments
> campaign approved by the owner as written
> on 2026-10-21, and the portfolio triage of
> the same date, drafting only). The freeze
> and the execution of Spec 049 are separate
> later acts under the campaign's Waves 2
> and 3. This spec's freeze is additionally
> sequenced after Spec 045's Asset A freeze
> (adjudication §6, item 6).

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      design D-06: the animal half of the
      opening signs, consuming Asset A as
      frozen), H13 (epistemic boundaries
      stated in spec §8), H15/H23 (execution
      shape is graph-first, spec §10), H16
      (data from the registered sources of
      record: the pinned positional and
      Phase-43 records, the pinned corpus
      layer and crosswalk, and Asset A as
      frozen under Spec 045 — never re-derived
      here), H24 (no private correspondence in
      the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F049-C01…C16) drafted in
      the Spec 042/045 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-049-7), and each
      claim's acceptance test derived twice
      with disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR on branch
      `spec-049-hunt-opening-animal-signs-draft`
      and left unmerged for the freeze
      decision, CI state reported from the
      run's own conclusions.
- [ ] **L4 — AEE lifecycle hooks (FREEZE
      GATE — not run on this draft).** At the
      freeze act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register,
      read under the campaign's standing
      reading for draft-lifecycle registers;
      a correctness failure blocks the freeze
      until its named recovery is complete
      and recorded. Any recovery round
      changes claim text, and the freeze
      digest is computed over the recovered
      register exactly once, at freeze.
- [ ] **L5 — Freeze-decision items.** The
      freeze decides `adjudication.md` §6:
      the population reproduction and keying
      rules, the count corpus and counting
      rule, the exact test's form, DD-049-2
      and DD-049-3, the unicorn naming
      procedure, the freeze sequencing, and
      the OSF filing (campaign E-1).
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided,
      and **after Spec 045's Asset A freeze
      record exists**: hooks recorded,
      `freeze.md` finalised, `freeze.json`
      recomputed over the recovered register
      and finalised texts, every spec §3 pin
      re-asserted against the merged record,
      **Asset A's SHA-256 quoted verbatim from
      Spec 045's `asset-a-freeze.json` into
      this spec's freeze record**, and the
      execution phase number allocated
      (DD-049-8).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as
      measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §5 gates
      0.1–0.3): dependency state (Asset A
      frozen under Spec 045, or the execution
      closes NOT-RUN); the Asset A digest
      assertion against the freeze record's
      verbatim quote (a mismatch closes
      ASSET PIN MISMATCH before any join);
      input integrity against the freeze
      pins. Any failure stops the run in its
      named class before any population work.
- [ ] **E3 — Step 0, part 2** (gates
      0.4–0.5): population enumeration and
      keying under the frozen rules, the
      enumerated list published (a count
      other than 40, or an unkeyable sign,
      closes POPULATION NOT REPRODUCED);
      comparison census with per-sign counts,
      Asset A coverage shown for both sets,
      and the unicorn sign(s) named from the
      frozen asset's labels. A coverage
      failure stops the run as INVALID.
- [ ] **E4 — Primaries** (spec §4): the
      primary arm and the pre-registered
      reversed arm, each with full published
      tables, followed by sensitivities S-A
      (contested included under CISI labels)
      and S-B (unicorn removed, or its
      not-applicable statement).
- [ ] **E5 — Outcome:** the §6 record —
      results JSON and report under the
      headline rules (claim identifier, Asset
      A digest and per-kind counts, both
      arms' full counts, ratios and p values,
      both sensitivities, the verdict word or
      closure class, the fence sentence), the
      appended outcome in this directory, the
      dated animal-half append to the claim's
      record, and the LEDGER entry; anchors
      asserted byte-identical before and
      after; foundation check reported as
      measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
