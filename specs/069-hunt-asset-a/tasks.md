# Spec 069 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-22
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's readiness
> decisions of 2026-10-22, decision 3,
> commissioning this draft first in the
> dependency order Spec 069 → Spec 070 →
> Spec 071; the readiness assessment of the
> same date; and Spec 045's frozen record).
> The freeze, the registration, and the
> execution of Spec 069 are separate later
> owner acts.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the Asset A build), H13 (epistemic
      boundaries stated in spec §6), H15/H23
      (execution shape is graph-first, spec
      §8), H16 (data from the registered
      sources of record: the held published
      sources named at gate A1, the pinned
      crosswalk, the D-18 delivery on
      record), H24 (no private correspondence
      in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F069-C01…C12) drafted in
      the Spec 042–054 register shape, at
      `0.5-draft`, with `observed_at` carried
      on evidence items from this draft
      (DD-069-4) and the acceptance tests for
      each claim derived twice independently,
      disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state
      reported from the run's own conclusions.
- [ ] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the
      freeze act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register;
      the gate is the substantive form of
      DD-038-10: zero correctness failure
      modes and no claim below the 0.70
      threshold at each hook. Deliberate
      ordering (the Spec 035/038 record): any
      recovery round changes claim text, and
      the freeze digest is computed over the
      recovered register exactly once, at
      freeze.
- [ ] **L5 — Freeze-decision items.** The
      freeze decides OPEN-069-1 (asset
      location in this spec's directory),
      OPEN-069-2 (the D-18 state as a
      terminal empty feed), OPEN-069-3
      (jurisdiction coding in the build
      record or not), OPEN-069-4
      (second-enterer spot check),
      OPEN-069-5 (OSF registration), and
      OPEN-069-6 (phase number), and
      confirms or openly overturns
      DD-069-1…DD-069-5.
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` computed over the
      recovered register and finalised texts,
      every spec §4 pin re-asserted against
      the merged record, the execution phase
      number allocated (OPEN-069-6), and the
      OSF contract registration filed if L5
      confirms OPEN-069-5's proposal.
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Source availability and D-18
      state** (spec §3, gates A1–A2): the
      CISI volumes and Parpola's
      identifications in hand and named by
      edition in the build record (ASSET
      FAILED on failure); the D-18 input
      resolved on the record (sequencing
      stop on failure — the build does not
      start).
- [ ] **E3 — Blind entry** (spec §2, quoted
      §§2.3–2.5): rows entered from the
      sources only, blind to positional
      results; dispute coding completed; the
      entry log preserved.
- [ ] **E4 — Coverage and citation gates**
      (gates A3–A4): every sign of the full
      pinned-crosswalk universe carries a
      row; every non-`unidentified` row
      carries at least one §2.3 citation
      with a verbatim label (ASSET FAILED on
      failure).
- [ ] **E5 — Blind-entry attestation and
      freeze** (gates A5–A6): the build
      record attests the §2.4 order and
      blindness; `asset-a-freeze.json`
      recorded with the §2.7 contents and
      its digest recomputing from the
      canonical CSV — **before any join**.
- [ ] **E6 — Publication and outcome:** the
      classification and its digest published
      as this spec's first product (the
      asserted input of Specs 070 and 071);
      the §7 outcome record — report under
      the headline rules, the appended
      outcome in this directory, and the
      LEDGER entry; anchors asserted
      byte-identical before and after;
      foundation check reported as measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
