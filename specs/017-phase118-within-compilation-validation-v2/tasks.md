# Tasks — Spec 017 / Phase-118 Within-Compilation Validation Battery v2

Owner commission 2026-10-07 covers design + execution (spec §11).

- [ ] T1 Spec 017 (spec/plan/tasks) committed alone — design pre-registration: W1 primary verbatim, W3 rebuilt cross-fit (model + φ cross-half, donor null per direction, median-donor bands), W4 FAIL-guard, judgeability definitions (§2.1), gates with discrimination teeth (§6), W1-primary decision rule (§8), §9 carried over verbatim in substance.
- [ ] T2 Appendix A finalized in the following commit: per-anchor attestation tables for FLAGGED44 and the JKUR 29-sign list under the frozen definitions. Counts only — no sign scored.
- [ ] T3 Implementation: `backend/glossa_lab/phase118_battery.py` (W1/W4 carried, W3 cross-fit, decision rule), `backend/glossa_lab/phase118_run.py`, runner `backend/scripts/phase118_within_battery.py`; unit tests `backend/tests/test_phase118_battery.py` incl. toy end-to-end controls (coherent validates; incoherent demotes).
- [ ] T4 H23 gate: graph module `backend/glossa_lab/experiment_graph_phase118.py` (node `IndusPhase118WithinCompilationValidation`) + registration in `experiment_graph.py`, asserted in `ATOMIC_NODES`, before any run. Partition totals (A 3,531 / B 3,471) and judgeability counts (J94 67, JKUR 29) asserted.
- [ ] T5 Calibration (spec §6): φ_{A→B} / φ_{B→A} from STRICT94 cross-fit self-scores; STRICT94 and KUR113 evaluated; gates checked (positive over J94; negative over JKUR with discrimination tallies). Outcome recorded whatever it shows.
- [ ] T6 Main run on FLAGGED44 — only if both §6 gates pass; §8 applied mechanically; change register written; changed-entries == register-signs asserted. (If the gates fail: battery rejected, the 44 never run, anchors untouched, no change register — the 011/014/016 pattern.)
- [ ] T7 Full backend suite + foundation check (H21); ruff clean.
- [ ] T8 Ledger entries (`LEDGER.md`, `glossa-indus/LEDGER.md`; AI disclosure) and one stacked PR (base `phase/117-within-compilation-battery`). No merge without the owner's explicit say-so.
