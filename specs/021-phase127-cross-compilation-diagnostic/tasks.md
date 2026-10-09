# Tasks — Spec 021 / Phase-127 Cross-Compilation Disagreement Diagnostic

## Phase (owner-authorized 2026-10-08)

- [ ] T1 Spec 021 (spec/plan/tasks) committed alone — pre-registration freeze: non-goals (§0: no re-scoring, Phase-125 verdict FINAL), fixed judgeable set, arms (a)–(f) with estimators, seeds + replicate counts, composition metadata bounds + gaps, power method, claim scope.
- [ ] T2 Core module `backend/glossa_lab/phase127_diagnostic.py` (spec §§3–8 machinery, reusing Phase-113/125 profile/TV code).
- [ ] T3 Orchestration `backend/glossa_lab/phase127_run.py` + runner `backend/scripts/phase127_cross_compilation_diagnostic.py` (frozen inputs via their loaders; corpus totals + anchors hash asserted; judgeable set read from the Phase-125 results of record).
- [ ] T4 Unit tests `backend/tests/test_phase127_diagnostic.py`, incl. toy hand-computed controls per arm, determinism, and real-input pins (16 judgeable pairs; observed median TV 0.636931).
- [ ] T5 H23 gate: graph module `backend/glossa_lab/experiment_graph_phase127.py` (node `IndusPhase127CrossCompilationDiagnostic`) + registration in `experiment_graph.py`, asserted in `ATOMIC_NODES`, before any run.
- [ ] T6 Run → `reports/phase127_cross_compilation_diagnostic_results.json` + `reports/phase127_cross_compilation_diagnostic.md`; abstract states the Phase-125 verdict unchanged first; anchors hash re-asserted unchanged.
- [ ] T7 Full backend suite + foundation check (H21); ruff clean.
- [ ] T8 Ledger entries (both files; AI disclosure) and one PR; merge only when complete + CI green (standing auto-merge rule); post-merge verification on main (suite counts, anchors hash).

## Explicitly not tasks of this phase

- Re-scoring Phase-125, issuing any verdict, or phrasing any finding as softening the Phase-125 FAIL.
- Any anchor, claim, PRED, or status change.
- Any object-level join between Holdat and mayig (spec 019 §2.1 prohibition stands).
- Pooling inscriptions across compilations for any statistic.
- Composition controls on strata the metadata does not support (spec 021 §7 gaps).
- Attributing the residual disagreement to a side or mechanism (out of scope, spec 021 §9).
