# Tasks — Spec 019 / Phase-125 Cross-Compilation Positional Comparison

## Phase (owner-authorized 2026-10-08)

- [x] T1 Spec 019 (spec/plan/tasks) committed alone — pre-registration freeze: question, frozen inputs + hashes, object-join discipline (§2.1), arms (§3), floor (§4), statistics + shuffle null (§5), verdict rules / falsifier (§6), claim scope (§7); Appendix A design-stage counts.
- [x] T2 Core module `backend/glossa_lab/phase125_cross_compilation.py` (§3 arms, §4 profiles, §5 statistics + null, §6 verdict rule).
- [x] T3 Orchestration `backend/glossa_lab/phase125_run.py` + runner `backend/scripts/phase125_cross_compilation.py` (frozen inputs via their loaders; corpus totals + anchors hash asserted).
- [x] T4 Unit tests `backend/tests/test_phase125_cross_compilation.py`, incl. real-input arm/judgeability counts, toy machinery checks, toy shuffle-null controls, and toy end-to-end PASS / FAIL / NULL-STARVED verdict controls.
- [x] T5 H23 gate: graph module `backend/glossa_lab/experiment_graph_phase125.py` (node `IndusPhase125CrossCompilationPositional`) + registration in `experiment_graph.py`, asserted in `ATOMIC_NODES`, before any run.
- [x] T6 Run → `reports/phase125_cross_compilation_results.json` + `reports/phase125_cross_compilation_summary.md`; verdict as found; anchors hash re-asserted unchanged.
- [x] T7 Full backend suite + foundation check (H21); ruff clean.
- [x] T8 Ledger entries (both files; AI disclosure) and one PR; merge only when complete + CI green (standing auto-merge rule); post-merge verification on main (suite counts, anchors hash).

## Explicitly not tasks of this phase

- Any anchor, claim, or status change; any PRED verdict.
- Any object-level join between Holdat and mayig (spec §2.1: no legitimate CISI object-ID join exists).
- Pooling inscriptions across compilations for any statistic.
- Mechanism attribution if the verdict is FAIL (a successor diagnostic spec, Phase-116 pattern, would own that question).
