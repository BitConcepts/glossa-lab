# Spec 096 — Tasks

## Stage 0 — Adoption and registration

- [ ] **T001 — Package lands and the program is registered.**
  spec.md, claims.md, aee-claims.json, plan.md, tasks.md and
  records/ committed as `specs/096-meroitic-reproduction-benchmark/`;
  the six claims intaken into the ledger under C096-1..C096-6; the
  taxonomy entry added (D-096-2); the program-map artifacts
  regenerated; the census pins the intake moves updated in the
  same pull request. Acceptance: **test** (aee-claims.json parses;
  claims.md and aee-claims.json carry the same six claim ids in the
  same order; every claim has a falsifier and a does-not-establish
  line; the ledger gate and the program-map conformance checks pass
  on the landed tree). *This does not establish:* that the package
  is approved — only that it is complete, consistent, and
  registered.
- [ ] **T002 — AEE verification of the claims.** The C096 bundle
  run through the pinned assessor: `aee validate` and `aee assess
  --no-ledger`, the outcome recorded verbatim in
  `records/adoption-aee-assessment.json`. Acceptance: **test**
  (the assessor ran and its outcome is recorded). *This does not
  establish:* claim quality — a draft-stage outcome is the expected
  reading for a bundle on asserted sources.
- [ ] **T003 — Owner commission recorded.** The owner's
  2026-11-20 commission of the benchmark and the direction that it
  stand as its own program are the adoption act of record, filed
  in `records/adoption-and-registration-2026-11-20.md`.
  Acceptance: **record** (the record names the direction, its
  date, and what it superseded: the Spec 095 placement, not the
  scoping's substance).

## Stage 1 — Step 0

- [ ] **T101 — Corpus identity record and execution freeze.**
  The paper's corpus repository pinned by exact commit; license
  recorded; the C095-3-style identity record and the execution
  freeze (counting bases, reconciliation rules, Leg C arms, seeds,
  settings grid, independence reading log) filed under `records/`
  before any computation. Claims: C096-1. Acceptance: **test**
  (the pin resolves to the recorded commit and tree; the freeze
  predates every computation).

## Stage 2 — The legs

- [ ] **T201 — Leg A, the census.** The ten published counts and
  the seven Table 2 dictionary sizes, each reproduced exactly
  under a frozen basis or diverged with its cause traced.
  Claims: C096-2. Acceptance: **test** (the per-count table is
  complete; every divergence names its cause).
- [ ] **T202 — Leg B, sign statistics.** The attested sign set
  against the fixture's 19 under the frozen reconciliation; the
  frequency-rank Spearman comparison at the fixed 0.90 bar; the
  positional distributions computed and archived. Claims: C096-3.
  Acceptance: **test** (the archived distributions exist and the
  comparison's basis is stated).
- [ ] **T203 — Leg C, alignment.** The program's own
  implementation of the paper's stated method over the frozen
  settings grid and arms; precision at 10 per dictionary and
  setting; the complete run index, failures included. Claims:
  C096-4. Acceptance: **test** (the run index covers the grid with
  no gaps; no seeded dictionary is scored as unseen).

## Stage 3 — Outcome and closeout

- [ ] **T301 — Benchmark outcome record.** Per-leg verdicts
  exactly as the fixed criteria read; reproduced numbers beside
  the published targets; the falsifier applied as written; the
  licensing posture restated; this spec's claims adjudicated on
  the outcome. Claims: C096-5, C096-6. Acceptance: **record**
  (the verdict follows from the record's own per-count and
  per-leg tables under the stated rule).
- [ ] **T302 — Closeout.** Tasks ticked to the record; remainders
  named (none expected beyond what the outcome record itself
  carries); the program's standing stated in one paragraph.
  Acceptance: **record**.
