# Tasks — Spec 016 / Phase-117 Within-Compilation Validation Battery

## Design phase (this PR; owner-authorized 2026-10-07)

- [x] T1 Spec 016 (spec/plan/tasks) committed alone — design pre-registration. Instruments (W1, W2 keep/drop, W3, W4), sparsity rules, calibration gates, decision rule, and the §9 claim scope frozen in that commit.
- [x] T2 Appendix A finalized in the following commit: design-stage feasibility tables (partition totals, per-instrument judgeability for FLAGGED44 / STRICT94 / KUR113, W2 keep/drop numbers, per-anchor attestation table for the 44). Instrument statistics only — no sign scored.
- [x] T3 Ledger entries (root `LEDGER.md`, `glossa-indus/LEDGER.md`; design only; AI disclosure).
- [x] T4 One PR, titled as a DESIGN PR (branched from main `83d03672` pre-history-rewrite; mechanical rebase onto rewritten main noted in the PR body). No merge without the owner's explicit say-so.

## Execution phase (GATED — requires the owner's separate, explicit approval after the design PR; spec §11)

- [x] T5 Implementation: `backend/glossa_lab/phase117_battery.py` (partition, W1, W3, W4, decision rule), `backend/glossa_lab/phase117_run.py`, runner `backend/scripts/phase117_within_battery.py`; unit tests `backend/tests/test_phase117_battery.py` incl. toy end-to-end controls. (Execution authorized by the owner 2026-10-07.)
- [x] T6 H23 gate: graph module `backend/glossa_lab/experiment_graph_phase117.py` (node `IndusPhase117WithinCompilationValidation`) + registration in `experiment_graph.py`, asserted in `ATOMIC_NODES`, before any run. Partition totals (A 3,531 / B 3,471) asserted.
- [x] T7 Calibration (spec §6): φ from STRICT94 LOO self-scores; STRICT94 LOO and KUR113 evaluated; gates checked. **BATTERY REJECTED: STRICT94 VALIDATED 2/94 (gate ≥ 47 FAIL); KUR113 VALIDATED 0/113 (gate ≤ 5 PASS).** Reports + ledgers written; stopped per §6.
- [ ] T8 Main run on FLAGGED44 — **not executed**: the §6 stop rule fired at T7 (battery rejected at calibration); FLAGGED44 was never run and the anchors file was not modified. No change register exists.
- [ ] T9 Full backend suite + foundation check (H21); ruff clean.
- [ ] T10 Ledger entries (both files; AI disclosure) and one PR. No merge without the owner's explicit say-so.
