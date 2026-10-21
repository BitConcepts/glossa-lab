# Spec 044 — Tasks

> ## PLAN — FROZEN 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the campaign plan approved
> AS WRITTEN on 2026-10-21, the portfolio triage
> of the same date, and the Roif verification).
> The freeze act of 2026-10-21 (campaign Wave 2,
> delegated under the approved plan) completed
> L4–L6 below; the freeze decisions are
> `adjudication.md` §7 and the digest record is
> `freeze.md` / `freeze.json`. Execution
> (Phase-404) is a separate later owner act.
> This spec is under the campaign's Roif gate:
> its records are internal and its results are
> not published or surfaced under the campaign
> (claim F044-C14).

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      design D-02's sign-by-sign residue plus
      the Asset F build the campaign assigns
      this spec), H13 (epistemic boundaries
      stated in spec §7), H15/H23 (execution
      shape is graph-first, spec §11), H16
      (data from the registered sources of
      record: the gate-0.1 pinned layer, the
      pinned gazetteer, Parpola's published
      list as cited data), H24 (no private
      correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F044-C01…C15) drafted in
      the Spec 032–042 register shape, with
      `observed_at` carried on evidence items
      from this draft (DD-044-8), and each
      claim's acceptance test derived twice
      with disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR (campaign Wave 1) and left
      unmerged for the freeze wave, CI state
      reported from the run's own conclusions.
      Asset builders freeze before dependents:
      this spec's freeze precedes Spec 048's
      (D-04), which pins Asset F's digest.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE
      — run at the freeze, 2026-10-21).** At the freeze
      act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register; the
      gate is **pass**, and a stricter outcome
      blocks the freeze until its named
      recovery is complete and recorded.
      Deliberate ordering (the Spec 035/038/042
      record): any recovery round changes
      claim text, and the freeze digest is
      computed over the recovered register
      exactly once, at freeze. Freeze mechanics
      are re-checked against the adopted
      1.5.x engine at the freeze, per the
      campaign plan, not assumed from
      pre-adoption habit.
- [x] **L5 — Freeze-decision items (decided
      2026-10-21, `adjudication.md` §7).** The
      freeze decides OPEN-044-1 (layer of
      record), OPEN-044-2 (Asset F source and
      DD-044-5), OPEN-044-3 (coastal list scope
      and DD-044-7), OPEN-044-4 (test form:
      DD-044-2, DD-044-4), OPEN-044-5 (OSF
      registration, under campaign E-1), and
      OPEN-044-6 (phase number), and confirms
      or openly overturns DD-044-1.
- [x] **L6 — Freeze.** On the owner's freeze
      order (campaign Wave 2 delegation), with
      L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` recomputed over the
      recovered register and finalised texts,
      every spec §2 pin re-asserted against
      the merged record, and the execution
      phase number allocated (DD-044-6).
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, part 1** (spec §3 gates
      0.1–0.2): corpus layer identified,
      exported, and pinned, with the original
      population description reproduced
      (failure closes LAYER NOT PINNABLE);
      Asset F built from Parpola's published
      list under the §4 contract, frozen, and
      its digest recorded, with the
      cross-check against the claim-record
      lists reported (failure closes ASSET F
      FREEZE FAILED).
- [ ] **E3 — Step 0, part 2** (gates 0.3–0.5):
      coastal list frozen with per-site bases
      and contested sites named (failure closes
      COASTAL LIST FAILED); occurrence census
      published (a TOO THIN closure ends the
      execution here, with the census as its
      finding); corpus-wide coastal baseline
      stated before any per-sign test.
- [ ] **E4 — Primary** (spec §5): per-member
      exact tests with the Bonferroni
      family-wise correction; every member's
      full counts reported, TOO THIN members
      included.
- [ ] **E5 — Sensitivities** (spec §5):
      inscription-level measure,
      site-size-matched, and
      contested-sites-removed, reported
      alongside the primary without changing
      its verdict.
- [ ] **E6 — Outcome:** the §9 record —
      results JSON and report under the
      headline rules (corpus label and digest,
      Asset F digest, frozen coastal list,
      per-member tables, §6's pre-written
      headline wording, the Roif-hold
      sentence), Asset F's canonical file
      preserved in this directory, the appended
      outcome in this directory, the dated
      residue append to the claim
      `indus_valley_script_deciphered_from_myth_65ff0a26_manual_002`'s
      record (member note or residue closure —
      the family verdict's text untouched), and
      the LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.
      All records internal under the Roif gate.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
