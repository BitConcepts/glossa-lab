# Spec 041 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-21
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's commissioning
> order of 2026-10-21, drafting only). The
> freeze and the execution are separate owner
> gates; nothing here has been frozen, filed,
> or run.

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
- [ ] **L4 — AEE lifecycle hooks (FREEZE GATE
      — not run on this draft).** At the
      freeze act, run `run_aee.py assess`
      after_specify, after_plan, and
      after_tasks over the claim register; the
      gate is **pass**, and a stricter outcome
      blocks the freeze until its named
      recovery is complete and recorded.
      Deliberate ordering (the Spec 035
      record): any recovery round changes
      claim text, and the freeze digest is
      computed over the recovered register
      exactly once, at freeze.
- [ ] **L5 — Freeze-stage verification
      (FREEZE GATE).** Re-verify spec §4's
      pins against the merged record and the
      executing environment: the layer file
      producible at SHA-256 `c368f290…`; the
      anchors file at the refreshed pin
      `df0cf620…` (Spec 040's carried value is
      superseded and must not be used); the
      Phase-139 covariates at `a0f0d05a…`.
      Decide DD-041-10, DD-041-11, DD-041-12;
      record DD-041-13's reservations.
      Failure of any pin is recorded and bars
      the freeze; no pin is refreshed silently.
- [ ] **L6 — Freeze.** On the owner's freeze
      order, with L4 and L5 passed: hooks
      recorded, `freeze.md` finalised,
      `freeze.json` computed over the recovered
      register and finalised texts, the
      execution phase number allocated
      (DD-041-14), and the artifact paths
      (§5.6) named into the freeze record.
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0 (spec §6):** gates
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
- [ ] **E3 — Extraction (spec §7.1):** per
      attested cell, the site publication's
      own determination sought and recorded
      (citation, locator, mapping rule,
      verification mode) under the §3 standard
      and the freeze's DD-041-11 scope.
- [ ] **E4 — Classification (spec §§7.2–7.3):**
      contested cells retained with both
      determinations and binding value
      UNASSIGNED; unassigned cells given
      exactly one enumerated reason; no
      precedence applied; no class skipped.
- [ ] **E5 — Dual verification (spec §7.4):**
      every MAPPED or CONTESTED cell
      re-verified at its locator by a second
      pass; reclassifications recorded, never
      edited into agreement.
- [ ] **E6 — Completeness + artifact
      (spec §5.5):** the artifact's cell set
      asserted equal to the step-0 census
      triple set, exactly once each; the
      artifact and its meta written (§5.6)
      and pinned by SHA-256.
- [ ] **E7 — Coverage report (spec §8):**
      cell counts by site × field × status;
      placement counts under derivations
      A1 / A2 / B / C with unplaced rows split
      by cause and the 57.6% ceiling stated;
      the secondary full-layer attestation
      census; the dual-verification record.
- [ ] **E8 — Outcome:** the §9 record in this
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
