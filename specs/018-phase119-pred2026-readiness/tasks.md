# Tasks — Spec 018 / Phase-119 PRED-2026 Readiness Harness

## Build phase (owner-authorized 2026-10-07)

- [x] T1 Spec 018 (spec/plan/tasks) committed alone — pre-registration freeze: registered criteria quoted verbatim, frozen sign sets + canonical map, evaluability matrix, dedup protocol, scoring rules, dry-run rule; Appendix A design-stage measurements included.
- [x] T2 Core module `backend/glossa_lab/pred_harness.py` (§3 maps/classes, §5 dedup, §7 adapters, §6 gating/scoring, §8 dry-run gate).
- [x] T3 Synthetic fixtures `backend/tests/fixtures/pred_harness/` (one per adapter class + toy converted layer) and unit tests `backend/tests/test_phase119_pred_harness.py`, incl. toy prediction end-to-end (CONFIRMED and REFUTED paths), gate refusal, verdict lock, dry-run label/no-criterion-statistic.
- [x] T4 H23 gate: graph module `backend/glossa_lab/experiment_graph_phase119.py` (node `IndusPhase119PredHarness`) + registration in `experiment_graph.py`, asserted in `ATOMIC_NODES`, before any run.
- [x] T5 Phase script `backend/scripts/phase119_pred_harness.py`; dry run on the expanded ICIT layer → `reports/phase119_pred_harness_results.json` + `reports/phase119_acquisition_log.json`; dry-run numbers reproduce Appendix A.1/A.2; summary `reports/phase119_pred_harness_summary.md`.
- [x] T6 Full backend suite + foundation check (H21); ruff clean.
- [x] T7 Ledger entries (both files; AI disclosure) and one PR. No merge without the owner's explicit say-so.

## Explicitly not tasks of this phase

- Evaluating PRED-2026-001–003 (no qualifying dataset exists; spec §10).
- Updating `docs/PREDICTION_REGISTER.md` Tested/Outcome fields (that belongs to a future authorized evaluation act).
- Acquiring any dataset or contacting any source (H14).
