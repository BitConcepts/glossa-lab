# Spec 041 — Tasks

> ## PLAN — FROZEN 2026-10-22
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's commissioning
> order of 2026-10-21, drafting only; the
> freeze decisions at §6, taken 2026-10-22
> under the owner's instruction to resolve the
> program's open pull requests). The execution
> remains a separate owner gate: it has not
> been ordered and has not started. Execution
> tasks run as Phase-435 under the frozen
> contract.

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the mapping act Spec 040's closure
      names), H13 (epistemic boundaries stated
      in spec §11), H15/H23 (execution shape is
      graph-first, spec §13), H16 (data from
      the registered sources of record: the
      pinned layer, the pinned Phase-139
      covariates and records, published
      stratigraphic sources under spec §3),
      H24 (no private correspondence in the
      repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F041-C01…C15) drafted in
      the Spec 032–040 register shape.
      Draft-stage verification: dependency
      integrity over the register and the
      cited-record facts are recorded in
      `adjudication.md` §2; the AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state
      reported from the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE).**
      Run at the freeze act of 2026-10-22 under
      aee 1.5.0 (the `aee assess` invocation the
      repo's `run_aee.py` harness wraps; lenient
      load, evidence verification off, no
      ledger): after_specify, after_plan, and
      after_tasks over the claim register,
      recovered through four rounds to
      0.8-draft. **PASS** under the DD-041-15
      gate reading (adopting DD-038-10): 15
      failure modes at every hook, all FR-2.3
      draft-cap records; zero correctness
      failure modes; no claim below the 0.70
      threshold (minimum propagated 0.72).
      Record: `aee/freeze-aee-note.md` and the
      register's own note.
- [x] **L5 — Freeze-stage verification
      (FREEZE GATE).** Spec §4's pins re-verified
      at the merged record by two independent
      routes: the anchors file at the refreshed
      pin `df0cf620…` (570,344 bytes; Spec 040's
      carried value superseded, used nowhere);
      the Phase-139 covariates at `a0f0d05a…`
      (2,665,622 bytes). The layer file is not
      producible on the freeze machine (the
      loader's default-path copy is absent);
      its pin `c368f290…` stands on the records
      of record, stated openly in `freeze.md`
      §2 and `adjudication.md` §6 — no pin was
      refreshed. DD-041-10, DD-041-11, and
      DD-041-12 decided; DD-041-13's
      reservations recorded (adjudication §6).
- [x] **L6 — Freeze.** Executed 2026-10-22:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` computed over the recovered
      register (0.8-draft) and finalised texts
      exactly once, execution phase **Phase-435**
      allocated (DD-041-14), and the artifact
      paths (§5.6) named into the freeze record.
- [x] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep —
      completed at the merge of the freeze PR;
      CI verified from the settled run's own
      job conclusions on the merged head.
      Foundation check NOT RUN at this freeze:
      the check needs the gitignored corpora
      tree, which is absent from this machine —
      the Spec 056 precedent; it establishes no
      foundation failure and is owed at the
      execution venue, whose step 0 asserts the
      layer pin fail-closed in any case).

## Execution — gated on the freeze and a separate execution order

- [x] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [x] **E2 — Step 0 (spec §6):** gates
      G0.1–G0.6 in order, fail-closed — layer
      identity; population reproduction (the
      seven sites, 5,410 rows); the value-level
      label census with headline counts
      reproducing the recorded tables, and the
      covariates copy asserted against the
      layer; anchors at the refreshed pin;
      source admissibility classified before
      extraction; the no-computation fence
      observed. Any failure closes the act at
      step 0 with no artifact.
- [x] **E3 — Extraction (spec §7.1):** per
      attested cell, the site publication's
      own determination sought and recorded
      (citation, locator, mapping rule,
      verification mode) under the §3 standard
      and the freeze's DD-041-11 scope.
- [x] **E4 — Classification (spec §§7.2–7.3):**
      contested cells retained with both
      determinations and binding value
      UNASSIGNED; unassigned cells given
      exactly one enumerated reason; no
      precedence applied; no class skipped.
- [x] **E5 — Dual verification (spec §7.4):**
      every MAPPED or CONTESTED cell
      re-verified at its locator by a second
      pass; reclassifications recorded, never
      edited into agreement.
- [x] **E6 — Completeness + artifact
      (spec §5.5):** the artifact's cell set
      asserted equal to the step-0 census
      triple set, exactly once each; the
      artifact and its meta written (§5.6)
      and pinned by SHA-256.
- [x] **E7 — Coverage report (spec §8):**
      cell counts by site × field × status;
      placement counts under derivations
      A1 / A2 / B / C with unplaced rows split
      by cause and the 57.6% ceiling stated;
      the secondary full-layer attestation
      census; the dual-verification record.
- [x] **E8 — Outcome:** the §9 record in this
      directory (artifact pin, gate and
      construction record, claim consequences),
      the LEDGER entry, anchors asserted
      byte-identical before and after,
      foundation check reported as measured.
      No G1 quantity is computed at any step
      (spec §10).

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
