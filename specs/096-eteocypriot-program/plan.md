# Spec 096 — plan

Stage 0 is complete at adoption (owner's direction, 2026-11-20).
The execution stages run in order under D-096-3, each landed as
its own PR on genuine per-job CI green. Nothing in this plan
starts a stage by itself, and no stage's landing is claimed from
a wrapper's completion state: every verdict is the payload's
own (run records, per-job CI results).

## Stage 0 — Program setup (COMPLETE 2026-11-20)

The package (spec.md, claims.md, aee-claims.json with
C096-1..C096-4, plan.md, tasks.md), the AEE assessment of the
package, the program-map assignment in
`glossa-indus/map/program-map-taxonomy.json` (D-096-4), the
claims-ledger intake through the sanctioned importer inside
the adoption PR (D-096-2), the generated-layer refresh the
intake requires, and the adoption record citing the numbers.

Discharge: no claim is discharged at adoption; intake sets no
standing (spec §6).

## Stage 1 — Corpus assembly and freeze

The corpus-availability survey of the preregistration draft
§3.1, resolved item by item or carried as named gaps; intake
of what is held under a C095-3 identity record
(`corpus/corpus.json` with per-inscription SHA-256 pins); the
frozen census; the split by inscription; the signary frame;
the frozen E1 procedure (derivation rules, match score, the
A1/A2 pairings, the ground truth of record); and the
registered floors instantiated against the census — a floor
that cannot be met closing its experiment as TOO THIN at
freeze. The step-0 closure check (draft §3.1) is recorded.
The freeze is committed before any analysis runs.

Discharge: the freeze record is Stage 1's deliverable; it
fixes everything Stage 2 is allowed to do.

## Stage 2 — Registered analysis

The E1 driver (stdlib-only, deterministic) loads the frozen
corpus, verifies its hash against the freeze pin (fail-closed),
and runs the frozen procedure on the administrable legs under
both assumptions; its run record is filed verbatim. E2 runs
only if its precondition (E1 success) and its census floor
both stand; E3 engages only for E2 survivors. Verdicts are
read from the run record, never from a summary of it.

## Stage 3 — Outcome and adjudication package

The outcome record states each claim's verdict with its
precision basis (C096-4): SUPPORTED at a stated strength, NOT
SUPPORTED, NOT IDENTIFIABLE, TOO THIN, or step-0 CLOSED, per
experiment and per claim, with the sensitivities (S1 readings,
S2 Golgoi, S3 per-assumption reporting) dispositioned. Ledger
standing changes, if any are warranted, are prepared as an
adjudication package for the named human approver; the expert
adjudication package (proposal §6 item 4) is prepared if the
outcome carries anything to adjudicate. Contacting any
specialist is a separate owner act (D-096-5) and is not part
of any stage.
