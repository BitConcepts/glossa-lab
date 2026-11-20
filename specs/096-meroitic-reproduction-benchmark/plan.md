# Spec 096 — Plan

## Stage 0 — Adoption and registration (T001–T003)

The package (spec.md, claims.md, aee-claims.json, plan.md,
tasks.md, records/) lands by pull request against the next free
spec number (D-096-1), the claims are intaken into the ledger
under this spec's own claim ids (C096-1..C096-6) through the
ledger bundle-import route, the program is registered in the
program-map taxonomy (D-096-2), the generated program-map
artifacts are regenerated, and every census pin the intake moves
is updated in the same pull request with the move recorded. The
claims bundle is verified under the pinned AEE at adoption and
the outcome recorded verbatim. The owner's commission and the
program-placement direction of 2026-11-20 are the adoption act,
recorded in `records/adoption-and-registration-2026-11-20.md`.

Gate: the pull request merges only on genuine per-job CI green
(all ten jobs read per job; a wrapper's success is not the
payload's), with the ledger/matrix/map gate among them.

## Stage 1 — Step 0 (T101)

Locate the paper's corpus repository; pin it by exact commit;
record its license (or its absence, with the D-096-3 posture);
file the C095-3-style identity record and the execution freeze
(counting bases, reconciliation rules, Leg C arms, seeds,
settings grid) under `records/`, before any computation. Every
reading of the authors' code is logged in the identity record
(mapping scheme only, per the independence rule).

Gate: the identity record's pin resolves; the freeze predates
every computation it governs.

## Stage 2 — The legs (T201–T203)

Leg A: the census, count by count, under the frozen bases. Leg B:
the sign set, the frequency-rank comparison, and the positional
distributions, archived as data alongside the record. Leg C: the
program's own implementation of the paper's stated alignment
method (embedding training where the freeze's arms require it,
VecMap-style alignment, CSLS retrieval, precision at 10), run
over the frozen settings grid with a complete run index. All
execution runs on the program's execution hosts, never in a
coordination environment; worker clones are fresh, and the origin
checkout's serving tree is never a work tree.

Gate: each leg's raw outputs are archived before its verdict is
written.

## Stage 3 — Outcome and closeout (T301–T302)

The benchmark outcome record under `records/`: per-leg verdicts
exactly as the fixed criteria read, the reproduced numbers beside
the published targets, the falsifier applied as written (C096-5),
the licensing posture restated so no verdict travels without it,
and the claims of this spec adjudicated on the outcome. The
closeout ticks the tasks, states what remains (nothing, or the
named remainder), and the package's landing discipline is the
same as Stage 0's: pull request, per-job CI green, branch and
worker clone removed in the same motion as the merge.

## Shared-file discipline

A second program package (the Eteocypriot pilot) is landing in
parallel and touches the same shared files (the claims ledger,
the program-map taxonomy and its generated artifacts, the census
pins). Before any pull request that touches a shared file merges,
the branch is brought onto the latest origin/main and the
registration steps are re-applied cleanly on top of whatever has
landed; nothing is force-pushed; a conflict that cannot be
resolved without dropping the other program's entries holds the
pull request and is reported, never resolved by deletion.
