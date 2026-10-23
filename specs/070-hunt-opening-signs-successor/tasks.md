# Spec 070 — Tasks

> ## PLAN — FOR FREEZE DECISION — 2026-10-22
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's readiness
> decisions of 2026-10-22, decision 3,
> commissioning this draft second in the
> dependency order Spec 069 → Spec 070 →
> Spec 071; the readiness assessment of the
> same date; Spec 049's draft at PR #250;
> and the recovered Phase-43 battery
> record). The freeze, the registration,
> and the execution of Spec 070 are
> separate later owner acts. **This spec
> cannot freeze before Asset A exists as a
> frozen product of Spec 069.**

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the re-scoped D-06 test), H13
      (epistemic boundaries stated in spec
      §8, the honesty fence in the banner and
      §6), H15/H23 (execution shape is
      graph-first, spec §10), H16 (data from
      the registered sources of record: the
      frozen Asset A of Spec 069, the Shakti
      corpus cited only through its intake
      record, the pinned crosswalk), H24 (no
      private correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F070-C01…C13) drafted in
      the Spec 042–054 register shape, at
      `0.5-draft`, with `observed_at` carried
      on evidence items from this draft
      (DD-070-5) and the acceptance tests for
      each claim derived twice independently,
      disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Design PR.** This draft, opened
      as a DRAFT PR and left unmerged for the
      owner's freeze decision, CI state
      reported from the run's own conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE GATE
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
- [x] **L5 — Freeze-decision items.** The
      freeze decides OPEN-070-1 (the intake
      record landed in final form),
      OPEN-070-2 (Asset A's digest quoted
      from Spec 069's executed record —
      requires Spec 069 executed first),
      OPEN-070-3 (the Wells-space keying
      rule), OPEN-070-4 (the counting rule
      for U), OPEN-070-5 (the unkeyable-sign
      disposition), OPEN-070-6 (OSF), and
      OPEN-070-7 (phase number), and confirms
      or openly overturns DD-070-1…DD-070-6.
- [x] **L6 — Freeze.** On the owner's freeze
      order, with L4 passed and L5 decided:
      hooks recorded, `freeze.md` finalised,
      `freeze.json` computed over the
      recovered register and finalised texts,
      every spec §3 pin re-asserted against
      the merged record, the execution phase
      number allocated (OPEN-070-7), and the
      OSF contract registration filed if L5
      confirms OPEN-070-6's proposal.
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, assertions** (spec §5
      gates 0.1–0.3): Asset A dependency
      state and digest assertion (NOT-RUN /
      ASSET NOT FROZEN / ASSET PIN MISMATCH
      on failure); Shakti intake S1/S2
      against the intake record (SHAKTI
      INTAKE NOT REPRODUCED on failure);
      input integrity (INVALID on failure).
- [ ] **E3 — Step 0, population** (gates
      0.4–0.6): the §2 battery run over the
      documented-lineage primary; O
      enumerated in full in Wells space and
      **published as the first product,
      before any join or test**; every sign
      keyed to exactly one Asset A row, an
      unkeyable sign named with its
      freeze-stated disposition (POPULATION
      NOT KEYED where the freeze so
      directs); U census, unicorn naming,
      coverage, and freeze-order proof
      (INVALID on failure).
- [ ] **E4 — Primaries** (spec §4): the
      primary arm, the reversed arm, and the
      three sensitivities (contested
      included; unicorn removed; corroborated
      population under P-F1 S4), with the
      headline decided by §4.3's precedence.
- [ ] **E5 — Outcome:** the §6 record —
      results JSON and report under the
      headline rules (the honesty fence and
      the P-F1 S3 lineage statement in the
      headline block, the Asset A digest, the
      full counts of both arms, R1/R2 and
      their p values, all sensitivities, and
      the headline word in §4.6's pre-written
      wording), the appended outcome in this
      directory, the dated animal-half append
      to the claim's record, and the LEDGER
      entry; anchors asserted byte-identical
      before and after; foundation check
      reported as measured.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
