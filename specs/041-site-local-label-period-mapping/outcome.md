# Spec 041 — Outcome record (Phase-435 execution)

## Headline (Spec 040 §10 form)

**Outcome word: EXECUTED.** This act built the
site-period mapping for the **ICIT-lineage layer
(horus84)**: of the 78 local chronological labels
attested on the 5,410 population inscriptions, 24
cells are assigned a coarse period on a published
determination verified to the §3 bar (30.8%; 4 EARLY,
18 MATURE, 2 LATE) and 54 are unassigned with an
enumerated reason (69.2%); the contested-excluded
count is 0 — no cell drew two admissible
determinations assigning different coarse periods.
Spec 039's artifact stands byte-identical and
untouched by this act. No G1 quantity is quoted
anywhere in this act's products, so the standing
rider is not engaged.

**What the artifact is for:** it is the §5 mapping
input — a cell per (site, field, local label) with
its coarse period or its recorded reason for having
none, each grounded cell carrying its published
determination's citation, locator, rule and
verification mode — prepared so that a future
Spec 040 freeze can judge, against Spec 040 §1,
whether this mapping satisfies the chronology-
control dependency. **What it is not for:** it is
not a dating of any inscription or object (an
inscription with no recorded label, or an
unassigned one, is unplaced, and that state is not
a defect to be repaired); it does not adopt any
row-level derivation (the §8 counts are reported,
none preferred); it does not satisfy Spec 040's
gate by existing, amend Spec 040's NOT-YET-TESTABLE
closure, or touch any anchor, reading, or
PRED-2026 state.

## Artifact pin

- Artifact: `data/evidence_integration/site_period_mapping.jsonl`
- Artifact SHA-256: `1e5b54c9193fb52092c34e1c959ec64a48b83cacbb8e5705f629635183c12b67`
- Meta: `data/evidence_integration/site_period_mapping_meta.json`,
  SHA-256 `bda1017dd88da0b14efaa3ffc5ff280b09818349bda4de1ed20f8c60d42864a9`
- Census: `specs/041-site-local-label-period-mapping/step0-census.json`,
  SHA-256 `b57fb6b1a0aa1e491ba38bf18978eec58c355f3bf833f58298c7516aabeca6be`
- Results: `reports/phase435_results.json`;
  step-0 machine record: `reports/phase435_step0.json`

## Gate record (step 0, spec §6)

**STEP 0 PASSED — all six gates, fail-closed, in
order** (full record: `step0-record.md`). G0.1 the
layer asserted at the frozen pin
(`c368f290…`, 5,679 × 38) — the venue's sweep copy
being absent, the file was re-acquired from its
pinned source repository and hash-asserted before
any use; G0.2 the population reproduced exactly
(seven sites, 5,410 rows); G0.3 the census
reproduced the recorded margins exactly (2,266 /
2,638 / 1,788 / 3,116 / 2,294) with the Phase-139
covariates agreeing on all 5,410 population rows
under the Phase-139 loader's recorded value
convention (7 whitespace-variant rows disclosed in
the step-0 record); G0.4 anchors at `df0cf620…`
before and after (unchanged); G0.5 source
classification committed before extraction (applied
record in the coverage report); G0.6 no quantity
computed at step 0.

## Construction record (E1–E8)

- **E1 graph-first:** runner
  `backend/scripts/phase435_site_period_mapping.py`;
  graph node `IndusPhase435SitePeriodMapping`
  (`backend/glossa_lab/experiment_graph_phase435.py`)
  registered in `experiment_graph.py` and verified
  registered in the assembled tree before the run
  record was finalized.
- **E2 step 0:** above; census committed as the
  §5.5 denominator (78 cells).
- **E3 extraction:** per-cell published
  determinations sought under §3 (four parallel
  evidence passes by site group; verbatim quotes
  with locators; conflicts flagged, none reconciled
  at this stage); adjudicated single-handedly by
  the executing agent into `determinations.json`.
- **E4 classification:** 24 MAPPED / 54 UNASSIGNED
  / 0 CONTESTED; every unassigned cell carries
  exactly one §5.4 reason; no precedence applied;
  no §7.3 class skipped.
- **E5 dual verification:** independent second pass
  over all 28 draft MAPPED cells — 23 confirmed,
  1 confirmed with caveat, **4 reclassified**
  (Harappa phases A, C, A-C, B/C → UNASSIGNED /
  DETERMINATION_UNVERIFIED), 2 determinations
  strengthened at better locators in the same
  publications, 2 re-probes closed as recorded
  (`verification-record.json`).
- **E6 completeness:** the artifact's cell set is
  asserted equal to the census triple set by the
  runner and re-asserted by
  `backend/tests/test_spec041_execution.py`; the
  artifact is pinned above.
- **E7 coverage report:** `coverage-report.md`
  (cell counts, §8 counts under A1/A2/B/C with the
  ceiling, secondary census, verification record).
- **E8 outcome:** this record; LEDGER entry added;
  anchors asserted byte-identical before and after
  (G0.4, `anchors_unchanged: true` in the results).
- **Foundation check (as measured at the record
  merge):** run against the live backend at the
  landing — **17 pass / 0 fail / 0 warnings,
  overall PASS** (integrity_ok: true). The check
  reads the venue's local corpus state, which this
  act does not touch; it is reported as measured,
  not as evidence about the mapping.

## Claim consequences (per claim)

- **F041-C01** (the scholarly product is the
  mapping artifact) — **Satisfied**: the artifact
  exists at the pinned path and hash above.
- **F041-C02** (key = the layer's triple) —
  **Satisfied**: cells are keyed (site, field,
  local_label) verbatim from the layer, including
  queried and span labels as recorded.
- **F041-C03** (every population-attested cell
  exactly once) — **Satisfied**: mechanical
  equality against the step-0 census, asserted by
  the runner and the test.
- **F041-C04** (one coarse value per cell from the
  four-code vocabulary) — **Satisfied**: schema
  asserted; UNASSIGNED is the binding value for
  unassigned and (none arose) contested cells.
- **F041-C05** (a MAPPED cell rests on a
  determination verified to the DD-039-3 bar) —
  **Satisfied**: all 24 MAPPED cells carry exactly
  one OWN_TEXT determination at a stated locator
  in an admissible venue; the four draft cells
  that failed the bar at re-reading were
  reclassified rather than carried.
- **F041-C06** (no cell rests on program-derived
  inference) — **Satisfied**: no cell's value
  derives from the layer's data, the covariates,
  the register, or a date; dates were never used
  to assign a period.
- **F041-C07** (disagreement between admissible
  determinations → CONTESTED) — **Stands, not
  triggered**: no cell drew two admissible
  verified determinations assigning different
  coarse periods; all candidate disagreements
  involved an inadmissible or unverified strand
  and are preserved as determination sets.
- **F041-C08** (no admissible determination →
  UNASSIGNED) — **Satisfied**: 54 cells, each with
  exactly one enumerated §5.4 reason and its
  evidence note.
- **F041-C09** (step 0 reproduces the census from
  the pinned layer before construction) —
  **Satisfied**: gate record above and in
  `step0-record.md`.
- **F041-C10** (key space covers all seven
  population sites on the same terms) —
  **Satisfied**: all seven sites censused on the
  same rule; Chanhu-daro attests no informative
  label and so has no cells — a census fact, not
  an omission.
- **F041-C11** (every grounded cell independently
  re-verified at its locator before pinning) —
  **Satisfied**: E5 record; reclassifications
  applied and published, never edited into
  agreement.
- **F041-C12** (coverage report publishes the
  placement counts under each candidate
  derivation) — **Satisfied**: A1 1,457 · A2 780 ·
  B 1,366 · C 1,457 placed, with causes and the
  ceiling; no derivation adopted.
- **F041-C13** (the pinned artifact satisfies the
  form of Spec 040 §1 conditions 2–4 for a future
  freeze to judge) — **Prepared, not judged**:
  the artifact is in the §5.6 form, pinned, with
  contested cells' sensitivity basis preserved as
  determination sets (DD-041-10: no sensitivity
  label frozen for any cell; `sensitivity_label`
  is null throughout). Whether it satisfies the
  conditions is the future freeze's judgment, not
  this act's.
- **F041-C14** (this act amends no frozen record)
  — **Satisfied**: Spec 040's closure, Spec 039's
  artifact, and all frozen records stand as they
  were; the one departure from a frozen *text* is
  the §5.4 illustrative example for Nausharo 4,
  where the published evidence governed the cell
  and the departure is recorded in the cell's note
  and the coverage report — an execution finding,
  not an amendment of the frozen record.
- **F041-C15** (every output carries the
  ICIT-lineage (horus84) label) — **Satisfied**:
  the label appears in the artifact meta, the
  results, this record's headline, the coverage
  report's headline, and the LEDGER entry.

## What this does not establish

Completing this act does not establish that any
inscription belongs to any period (the mapping
assigns recorded labels, on publications'
authority, and 69.2% of labels could not be
assigned at the bar the spec set); it does not
make Spec 040's G1 testable (a future freeze must
judge the dependency and would still need its
own execution order); it computes no G1 quantity;
and its placement counts are bounded by the
57.6% ceiling — at most 3,116 of 5,410 population
rows carry any label, and the largest single
derivation places 1,457 rows (26.9%).
