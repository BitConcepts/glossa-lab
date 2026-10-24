# Spec 074 — Tasks

> ## PLAN — FOR FREEZE — 2026-10-24
>
> Adjudication inputs are recorded in
> `adjudication.md` (the owner's order of
> 2026-10-24; Spec 070's frozen contract and
> executed closure; Spec 073's executed
> record; the Shakti intake record of
> 2026-10-22). The freeze and the OSF filing
> are commissioned with this draft; the
> execution is a separate later act.
> **This spec cannot freeze against a
> surface that is not frozen: Registry v2
> and Asset A v2 exist as frozen products
> of Spec 073 on the merged record, and
> gate 0.1 asserts their digests.**

## Lifecycle

- [x] **L1 — Constitution check.** Spec and
      claim register checked against
      constitution §§I–VIII and governance H2
      (spec before code), H6 (no scope beyond
      the re-asked D-06 test on the repaired
      surface), H13 (epistemic boundaries
      stated in spec §8, the honesty fence in
      the banner and §6), H15/H23 (execution
      shape is graph-first, spec §10), H16
      (data from the registered sources of
      record: the frozen Registry v2 and
      Asset A v2 of Spec 073, the Shakti
      corpus cited only through its intake
      record, the pinned crosswalk, Spec
      070's pinned machine record), H24 (no
      private correspondence in the repo).
- [x] **L2 — Claims-first register.**
      `claims.json` (F074-C01…C13) drafted in
      the Spec 042–070 register shape, at
      `0.5-draft`, with `observed_at` carried
      on evidence items from this draft
      (DD-074-5) and the acceptance tests for
      each claim derived twice independently,
      disagreements resolved in
      `adjudication.md` §3. The AEE lifecycle
      hooks have **not** run on this register
      (L4).
- [x] **L3 — Draft + freeze PR.** This
      draft, opened as a PR with the freeze
      products (L4–L6) under the owner's
      combined order of 2026-10-24, CI state
      reported from the run's own
      conclusions.
- [x] **L4 — AEE lifecycle hooks (FREEZE
      GATE — run at the freeze act).** Run
      `run_aee.py assess` after_specify,
      after_plan, and after_tasks over the
      claim register; the gate is the
      substantive form of DD-038-10 (DD-074-6):
      zero correctness failure modes and no
      claim below the 0.70 threshold at each
      hook. Deliberate ordering (the Spec
      035/038 record): any recovery round
      changes claim text, and the freeze
      digest is computed over the recovered
      register exactly once, at freeze.
      *(Done at the freeze act of 2026-10-24:
      `aee assess` (lenient load, aee 1.5.3)
      over the register recovered 0.5-draft →
      0.7-draft in two rounds; the final round
      at all three hooks carries 13 failure
      modes each, every one an FR-2.3
      draft-cap record, zero correctness
      modes, minimum propagated 0.795 — the
      gate passes on the DD-038-10 reading.
      Record: `aee/freeze-aee-note.md`.)*
- [x] **L5 — Freeze-decision items.** The
      freeze decides OPEN-074-1 (the v2
      digests copied from Spec 073's executed
      record), OPEN-074-2 (the two-leg keying
      route), OPEN-074-3 (the reproduction
      assertion and its closure class),
      OPEN-074-4 (the unkeyable-sign
      disposition), OPEN-074-5 (OSF), and
      OPEN-074-6 (phase number), and confirms
      or openly overturns DD-074-1…DD-074-6.
      *(Ruled at the freeze act of 2026-10-24
      as DD-074-7 to DD-074-13, adjudication
      §8; DD-074-1…DD-074-6 stand as drafted.)*
- [x] **L6 — Freeze.** With L4 passed and L5
      decided: hooks recorded, `freeze.md`
      finalised, `freeze.json` computed over
      the recovered register and finalised
      texts, every spec §3 pin re-asserted
      against the merged record, the
      execution phase number allocated
      (OPEN-074-6), and the OSF contract
      registration filed (OPEN-074-5).
      *(Freeze digest
      `5416a0d331e76fcec720746849969f2e86e9d79f2cc0fa583e1050662ffba36c`;
      phase allocated Phase 440 (DD-074-12);
      able-to-fail proof run as freeze.md §7
      records; OSF filing recorded in
      `osf-spec-registration.md`.)*
- [ ] **L7 — Freeze PR merged**, house gates
      green (full suite, branding sweep,
      foundation check reported as measured).

## Execution — gated on the freeze and a separate execution order

- [ ] **E1 — Graph-first build** (H15/H23):
      script, graph module, registration,
      registration verification, then run.
- [ ] **E2 — Step 0, assertions** (spec §5
      gates 0.1–0.3): repaired-surface
      dependency state and digest assertion
      (NOT-RUN / ASSET NOT FROZEN / ASSET PIN
      MISMATCH on failure); Shakti intake
      S1/S2 against the intake record (SHAKTI
      INTAKE NOT REPRODUCED on failure);
      input integrity (INVALID on failure).
- [ ] **E3 — Step 0, population** (gates
      0.4–0.6): the §2 battery run over the
      documented-lineage primary; O
      enumerated in full in Wells space and
      **published as the first product,
      before any join or test**; the
      enumeration asserted against Spec 070's
      recorded 31 (POPULATION NOT REPRODUCED
      on a difference); every sign keyed to
      exactly one Asset A v2 row under the
      two-leg route, an unkeyable sign named
      with its freeze-stated disposition
      (POPULATION NOT KEYED where the freeze
      so directs); U census, unicorn naming,
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
      headline block, the Asset A v2 digest,
      the gate 0.4 reproduction record, the
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

*AI disclosure: drafted by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
