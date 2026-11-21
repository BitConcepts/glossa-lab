# Spec 098 — Tasks

## Stage 0 — Adoption, freeze, and registration

- [x] **T001 — Package lands, design frozen.** spec.md,
  claims.md, aee-claims.json, plan.md, tasks.md,
  test-cases.md, tools/, tests/ and records/ committed as
  `specs/098-identifiability-over-the-65/`; the design frozen
  in `records/freeze-v1-2026-11-21.md`; the population frozen
  in `records/population-annex-2026-11-21.md` (65 I + 6 E =
  71 signs, values exactly as recorded). Acceptance: **test**
  (aee-claims.json parses; claims.md and aee-claims.json carry
  the same eight claim ids in the same order; every claim has
  a falsifier and a does-not-establish line). *This does not
  establish:* that the study has run — Stage 0 freezes it.
- [x] **T002 — Test cases executed.** TC-098-01 (seal and
  split integrity) and TC-098-02 (decision rules on planted
  cases) run on tower-compute against
  `tools/seal_and_score.py`; payload verdicts (the test
  processes' own exit codes and outputs) recorded in
  `records/tc-execution-2026-11-21.md`. Acceptance: **test**.
- [x] **T003 — Owner directive recorded.** The owner's
  2026-11-21 directive to execute all Co-scientist audit
  recommendations, and this package's assignment to Q5
  item 2, are the adoption act of record, filed in
  `records/adoption-and-registration-2026-11-21.md`.
  Acceptance: **record**.
- [ ] **T004 — Ledger intake (deferred, D-098-3).** The
  C098-1..C098-8 bundle (`aee-claims.json`) intaken into the
  canonical ledger through the bundle-import route by the
  coordinator, re-applied on the latest main alongside the
  other audit-response packages; census pins the intake moves
  updated in the same act. Acceptance: **test** (the ledger
  gate passes on the landed tree after intake). Blocked in
  this round by the shared-file serialization of D-098-3,
  not by the bundle, which is complete and filed here.

## Stage 1 — Step 0 (before anything is scored)

- [ ] **T101 — Provenance audit and genuine-holdout subset.**
  Every sequence-bearing source in the corpus of record
  checked against the candidate-generation inputs of record;
  the genuine-holdout subset established with its documentary
  basis, or its absence recorded. Claims: C098-6.
  Acceptance: **record**.
- [ ] **T102 — M044/M374 gap resolution.** Their sequences
  resolved from the diplomatic text codes under the frozen
  crosswalk, or both signs recorded as defaulting to
  UNDECIDABLE AT THIS POWER. Claims: C098-2. Acceptance:
  **record + test** (resolved sequences verify against the
  crosswalk of record).
- [ ] **T103 — Power grid and execution freeze annex.** The
  per-sign power grid on development-side counts only
  (minimum detectable margin per sign at its expected
  held-out count); the context-model estimator details fixed
  in an execution freeze annex committed before the seal.
  Claims: C098-5. Acceptance: **record**.
- [ ] **T104 — The seal.** Held-out cluster list generated
  under the frozen rule on tower-compute; seal record (count
  and SHA-256 only) committed; list held in custody outside
  the repository. Claims: C098-1. Acceptance: **test** (the
  seal hash recomputes; the seal record predates every
  scoring artifact).

## Stage 2 — Rivals and prediction sheets (development only)

- [ ] **T201 — Rival construction.** R-A..R-E for all 71
  signs, plus the Arm E cross-sign and comparandum rivals,
  constructed on development data only under WP8 fairness;
  tuning budgets recorded per sign. Claims: C098-3.
  Acceptance: **record + test** (no rival input contains a
  held-out cluster id — the TC-098-01 guard run over the
  actual development export).
- [ ] **T202 — Prediction sheets.** One sheet per sign,
  reviewed for value-relevance before unsealing; rejected
  sheets and sheetless signs recorded NOT IDENTIFIABLE by
  construction. Claims: C098-4. Acceptance: **record** (the
  sheets are committed before the seal's release entry).

## Stage 3 — Scoring (the seal opened once)

- [ ] **T301 — The scoring run.** The held-out list released
  once and the release recorded; per-sign margins, penalties,
  and the frozen permutation null computed; the complete run
  index archived with raw outputs before verdicts.
  Claims: C098-5, C098-8. Acceptance: **test** (every outcome
  follows from its recorded margins under the reference
  `decide` rule; the seal verifies at scoring time).

## Stage 4 — Outcome and closeout

- [ ] **T401 — Outcome record.** Per-sign outcomes per arm
  in the frozen vocabulary; family counts; the premise
  falsifier applied as written; the contamination ceiling
  restated; this spec's claims adjudicated on the outcome.
  Claims: C098-5, C098-6, C098-7. Acceptance: **record**.
- [ ] **T402 — Closeout.** Tasks ticked to the record;
  remainders named (any standing act on the outcomes is a
  separate program act, not a remainder of this study).
  Acceptance: **record**.
