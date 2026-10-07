# Tasks — Spec 016 / Phase-117 Within-Compilation Validation Battery

## Design phase (this PR; owner-authorized 2026-10-07)

- [x] T1 Spec 016 (spec/plan/tasks) committed alone — design pre-registration. Instruments (W1, W2 keep/drop, W3, W4), sparsity rules, calibration gates, decision rule, and the §9 claim scope frozen in that commit.
- [x] T2 Appendix A finalized in the following commit: design-stage feasibility tables (partition totals, per-instrument judgeability for FLAGGED44 / STRICT94 / KUR113, W2 keep/drop numbers, per-anchor attestation table for the 44). Instrument statistics only — no sign scored.
- [x] T3 Ledger entries (root `LEDGER.md`, `glossa-indus/LEDGER.md`; design only; AI disclosure).
- [x] T4 One PR, titled as a DESIGN PR (branched from main `83d03672` pre-history-rewrite; mechanical rebase onto rewritten main noted in the PR body). No merge without the owner's explicit say-so.

## Execution phase (GATED — requires the owner's separate, explicit approval after the design PR; spec §11)

- [ ] T5 Implementation: `backend/glossa_lab/phase117_battery.py` (partition, W1, W3, W4, decision rule), `backend/glossa_lab/phase117_run.py`, runner `backend/scripts/phase117_within_battery.py`; unit tests `backend/tests/test_phase117_battery.py` incl. toy end-to-end controls.
- [ ] T6 H23 gate: graph module `backend/glossa_lab/experiment_graph_phase117.py` (node `IndusPhase117WithinCompilationValidation`) + registration in `experiment_graph.py`, asserted in `ATOMIC_NODES`, before any run. Partition totals (A 3,531 / B 3,471) asserted.
- [ ] T7 Calibration (spec §6): φ from STRICT94 LOO self-scores; STRICT94 LOO and KUR113 evaluated; gates checked. If rejected: reports + ledgers, stop.
- [ ] T8 Main run on FLAGGED44 (only if both gates pass); apply the §8 decision rule; write `reports/phase117_within_battery_results.json`, `reports/phase117_within_battery_change_register.json`, `reports/phase117_within_battery_summary.md`; anchors-file changes per §8 only.
- [ ] T9 Full backend suite + foundation check (H21); ruff clean.
- [ ] T10 Ledger entries (both files; AI disclosure) and one PR. No merge without the owner's explicit say-so.
