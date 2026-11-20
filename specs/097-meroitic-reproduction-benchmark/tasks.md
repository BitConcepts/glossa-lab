# Spec 097 — Tasks

## Stage 0 — Adoption and registration

- [x] **T001 — Package lands and the program is registered.**
  spec.md, claims.md, aee-claims.json, plan.md, tasks.md and
  records/ committed as `specs/097-meroitic-reproduction-benchmark/`;
  the six claims intaken into the ledger under C097-1..C097-6; the
  taxonomy entry added (D-097-2); the program-map artifacts
  regenerated; the census pins the intake moves updated in the
  same pull request. Acceptance: **test** (aee-claims.json parses;
  claims.md and aee-claims.json carry the same six claim ids in the
  same order; every claim has a falsifier and a does-not-establish
  line; the ledger gate and the program-map conformance checks pass
  on the landed tree). *This does not establish:* that the package
  is approved — only that it is complete, consistent, and
  registered.
- [x] **T002 — AEE verification of the claims.** The C097 bundle
  run through the pinned assessor: `aee validate` and `aee assess
  --no-ledger`, the outcome recorded verbatim in
  `records/adoption-aee-assessment.json`. Acceptance: **test**
  (the assessor ran and its outcome is recorded). *This does not
  establish:* claim quality — a draft-stage outcome is the expected
  reading for a bundle on asserted sources.
- [x] **T003 — Owner commission recorded.** The owner's
  2026-11-20 commission of the benchmark and the direction that it
  stand as its own program are the adoption act of record, filed
  in `records/adoption-and-registration-2026-11-20.md`.
  Acceptance: **record** (the record names the direction, its
  date, and what it superseded: the Spec 095 placement, not the
  scoping's substance).
- [x] **T004 — Platform registration.** The program's project
  created in the live backend through the Projects API and read
  back; the registered work (this package, its ledger claims)
  surfaces through the platform's own record machinery (the
  spec-study register and the ledger-driven surfaces) on the
  package's landing; what the project model cannot carry is
  recorded, not improvised. Acceptance: **test** (the project
  read-back matches the created record; the Indus project remains
  the active project, undisturbed). Recorded in
  `records/adoption-and-registration-2026-11-20.md`.

## Stage 1 — Step 0

- [x] **T101 — Corpus identity record and execution freeze.**
  The paper's corpus repository pinned by exact commit; license
  recorded; the C095-3-style identity record and the execution
  freeze (counting bases, reconciliation rules, Leg C arms, seeds,
  settings grid, independence reading log) filed under `records/`
  before any computation. Claims: C097-1. Acceptance: **test**
  (the pin resolves to the recorded commit and tree; the freeze
  predates every computation).

## Stage 2 — The legs

- [x] **T201 — Leg A, the census.** The ten published counts and
  the seven Table 2 dictionary sizes, each reproduced exactly
  under a frozen basis or diverged with its cause traced.
  Claims: C097-2. Acceptance: **test** (the per-count table is
  complete; every divergence names its cause).
- [x] **T202 — Leg B, sign statistics.** The attested sign set
  against the fixture's 19 under the frozen reconciliation; the
  frequency-rank Spearman comparison at the fixed 0.90 bar; the
  positional distributions computed and archived. Claims: C097-3.
  Acceptance: **test** (the archived distributions exist and the
  comparison's basis is stated).
- [x] **T203 — Leg C, alignment.** The program's own
  implementation of the paper's stated method over the frozen
  settings grid and arms; precision at 10 per dictionary and
  setting; the complete run index, failures included. Claims:
  C097-4. Acceptance: **test** (the run index covers the grid with
  no gaps; no seeded dictionary is scored as unseen).

## Stage 3 — Outcome and closeout

- [x] **T301 — Benchmark outcome record.** Per-leg verdicts
  exactly as the fixed criteria read; reproduced numbers beside
  the published targets; the falsifier applied as written; the
  licensing posture restated; this spec's claims adjudicated on
  the outcome. Claims: C097-5, C097-6. Acceptance: **record**
  (the verdict follows from the record's own per-count and
  per-leg tables under the stated rule).
- [x] **T302 — Closeout.** Tasks ticked to the record; remainders
  named (none expected beyond what the outcome record itself
  carries); the program's standing stated in one paragraph.
  Acceptance: **record**.

## Stage 4 — The decipherment campaign (added 2026-11-20)

- [x] **T401 — Campaign design and preregistration.** The
  design record (corpus plan, anchor inventory shape, the
  affiliation rivals with falsifiers, the identifiability
  protocol and blind held-out test, the expert-verification
  design) filed and the campaign claims intaken BEFORE any
  campaign execution. Claims: C097-7..C097-11. Acceptance:
  **record** (the design is on file and the claims are in the
  ledger before Stage 4.1 work begins).
- [x] **T402 — Corpus completion.** The canonical corpus build
  with per-text provenance; every openly licensed source
  acquired or gap-named; counts reconciled against the REM
  totals. Claims: C097-7. Acceptance: **record + test** (the
  completion record's held/acquired/gap account is complete
  against its own search account).
- [x] **T403 — Anchor inventory freeze v1.** Every anchor with
  form, proposed reading, evidence class, source, and licensed
  use; the development / held-out split hash-pinned in the
  freeze. Claims: C097-8. Acceptance: **record**.
- [ ] **T404 — Affiliation adjudication.** R1/R2/R3 tested as
  registered; verdict record with the tests' outputs. Claims:
  C097-9. Acceptance: **test**.
- [ ] **T405 — Candidate readings and blind scoring.**
  Generation from licensed routes only; identifiability
  screening; frozen readings scored once on the sealed
  held-out set. Claims: C097-10. Acceptance: **test**.
- [ ] **T406 — Expert-verification package.** The design of
  Stage 4.5 prepared for the owner's approval; no outreach.
  Claims: C097-11. Acceptance: **record**.
