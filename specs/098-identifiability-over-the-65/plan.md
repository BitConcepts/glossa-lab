# Spec 098 — Plan

## Stage 0 — Adoption, freeze, registration (T001–T004)

The package (spec.md, claims.md, aee-claims.json, plan.md,
tasks.md, test-cases.md, tools/, tests/, records/) lands by
pull request against the next free spec number (D-098-1),
with the design frozen in
`records/freeze-v1-2026-11-21.md` and the population frozen in
`records/population-annex-2026-11-21.md`. The two test cases
are executed on tower-compute at adoption and their payload
verdicts recorded. The claims bundle (`aee-claims.json`,
C098-1..C098-8) is intaken into the canonical ledger through
the bundle-import route, the taxonomy entry is added, the
settling chain is refreshed in the standing order, the
generated layers are regenerated, and every census pin the
intake moves is updated in the same pull request (D-098-3),
as Specs 096/097 performed the same registration.

Gate: the pull request merges only on genuine per-job CI
green (all ten jobs read per job; a wrapper's success is not
the payload's).

## Stage 1 — Step 0: provenance audit, gap resolution, seal

On tower-compute, in a fresh clone: (1) the provenance audit
of freeze §7 gap 1 — every sequence-bearing source in the
corpus of record checked against the candidate-generation
inputs of record, the genuine-holdout subset established or
its absence recorded; (2) the M044/M374 resolution of gap 2
under the frozen crosswalk, or their UNDECIDABLE default
recorded; (3) the per-sign power grid (Standards Part II
precision basis) computed on development-side counts only;
(4) the execution freeze annex fixing the context model's
estimator details the design leaves open; (5) the seal struck
— held-out cluster list generated, count and SHA-256
committed, list to custody. Claims: C098-1, C098-6.

Gate: the seal record is committed before any scoring-path
code runs; the seal hash recomputes from the design's rule.

## Stage 2 — Rivals and prediction sheets (development only)

Rival construction for all 71 signs under WP8 fairness, and
one prediction sheet per sign, reviewed for value-relevance
before unsealing; sheets that fail review, and signs with no
acceptable sheet, are recorded NOT IDENTIFIABLE by
construction without touching held-out data. Claims: C098-3,
C098-4.

Gate: every sheet and rival is committed before the seal is
opened; the commit order is itself the evidence.

## Stage 3 — The single scoring run

The held-out list is released once, recorded; the frozen
scoring path computes per-sign margins, penalties, and the
permutation null; the run index is complete, failures
included; raw outputs are archived before any verdict is
written. Claims: C098-5, C098-8.

Gate: each per-sign outcome follows mechanically from its
recorded margins under the frozen rules (the `decide` rule of
`tools/seal_and_score.py` is the reference implementation).

## Stage 4 — Outcome and closeout

The outcome record: per-sign outcomes in the frozen
vocabulary, per arm; family counts; the study-premise
falsifier applied as written (spec §4); the contamination
ceiling restated on the face of the record; this spec's
claims adjudicated on the outcome. No standing changes
(C098-7) — any standing act on these outcomes is a separate
program act. Closeout ticks the tasks and names remainders.

## Shared-file discipline

The shared files this package touches in its adoption pull
request are exactly the registration set of D-098-3 (ledger,
settling chain, taxonomy, generated layers, census pins),
re-applied on the latest origin/main at landing time. A
conflict in that set that cannot be resolved without
dropping another package's entries holds the pull request
and is reported, never resolved by deletion.
