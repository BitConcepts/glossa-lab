# Spec 034 — Freeze Record (Matched-Object Attribution of the Phase-125 Residual)

> ## FROZEN at the Spec 034 freeze merge (2026-10-13)
>
> Basis: design **D-20** of the experiment-design
> portfolio of 2026-10-13 (draft PR #195), commissioned
> by the owner's order of 2026-10-13 ("Design
> experiments for all of the 35 that remain in question
> or inconclusive") and adjudicated for freeze by the
> owner's order of 2026-10-13 06:39 EDT, verbatim
> **"Freeze D-30, D-03, and D-20 for execution"**
> (`adjudication.md`). The governed claim register
> passed the AEE lifecycle hooks at after_specify,
> after_plan, and after_tasks after four recorded
> recovery rounds (12, then 4, then 1, then 1 failure
> modes; `aee/recovery-specify.md`) — the freeze digest
> recorded in `freeze.json` (framework026 digest, built
> by `build_freeze.py` from the DEFINITION and SOURCES
> it carries) covers the recovered register, never a
> pre-recovery draft.

## 1. What was decided, and on what basis

The settled Phase-125 result (FAIL — DISAGREEMENT
between the CISI and ICIT compilations) carries a
93.9% unexplained residue that Phase-131 could not
attribute for want of shared object keys. This freeze
adopts design D-20 without deviation: build the
object bridge through the three lawful routes, gate
the study at 150 matched objects, and — if the gate
passes — attribute the residue on the matched subset
under Phase-125's own measurement, in Phase-131's own
categories. Nothing was left to freeze-time fixing:
the distance, the floors, the categories, the gate,
and both verdict lines are the design's own numbers,
verified against the Phase-124/125/127/131 records
before the freeze (adjudication §2).

## 2. Frozen sources

`freeze.md`, `spec.md`, `claims.json`, and
`adjudication.md` in this directory;
`aee/recovery-specify.md` and `aee/freeze-aee-note.md`;
`build_freeze.py`; and `backend/tests/
test_spec034_freeze.py` — digest-covered as frozen.
`plan.md` and `tasks.md` are bookkeeping and are NOT
digest-covered (the Spec 029/030 rule).

## 3. What execution must satisfy (Phase-398)

- Step 0 builds the bridge through the CISI catalogue
  layer (7,705 rows), the Phase-130 intake route, and
  the 44 Phase-128 dossiers — cited pairs only;
  Holdat `cisi_number` is never a join key.
- The gate is 150 matched objects with texts of three
  or more signs in both compilations; below it the
  study closes as TOO THIN TO ATTRIBUTE with the
  bridge census published as the finding.
- Above the gate: Phase-125's distance and floors on
  the matched subset only; decomposition in
  Phase-131's categories; the crosswalk as a record
  of disagreement, never ground truth.
- Verdict lines on the matched median: at or below
  0.20 ATTRIBUTED TO COMPOSITION; at or above 0.32
  ATTRIBUTED TO TRANSCRIPTION; between, a split
  attribution with the decomposition table as the
  result. Every verdict statement carries the matched
  subset's description (selection-bias rule).
- The settled Phase-125/127/131 records are never
  edited; the outcome appends in this spec's
  directory and the root LEDGER.

## 4. What this freeze does NOT do

It matches no objects and computes no distance.
Execution is Phase-398, gated on the OSF registration
of this frozen contract verifying public. It does not
touch any other frozen record (Specs 026–033), any
claim record, or the settled Phase-125 verdict.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
