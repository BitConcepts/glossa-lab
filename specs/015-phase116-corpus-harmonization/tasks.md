# Tasks — Spec 015 / Phase-116 Corpus-Harmonization Study

- [ ] T1 Spec 015 (spec/plan/tasks) committed alone — pre-registration.
- [ ] T2 Keyed-layer builder (`backend/scripts/phase116_build_keyed_layer.py`); build run; §2 assertions (kept subset == Phase-115 v2 layer: 4,531 / 13,492 / 2,388).
- [ ] T3 Analysis module (`backend/glossa_lab/phase116_harmonization.py`): keyed loaders, profiles (phase113 conventions), matcher tiers A/B/C, §5 arms, verdict rules, §6 recommendation assembly.
- [ ] T4 Run module (`backend/glossa_lab/phase116_run.py`) + runner script (`backend/scripts/phase116_harmonization_study.py`): §3 baseline assertions gate all arms.
- [ ] T5 H23 gate: graph module `experiment_graph_phase116.py` (node `IndusPhase116Harmonization`) + registration in `experiment_graph.py`, before any run.
- [ ] T6 Unit tests (`backend/tests/test_phase116_harmonization.py`): matcher toy cases (direct/reversed/ambiguous/containment/non-match), profile conventions, verdict-rule boundaries, ATOMIC_NODES registration assertion.
- [ ] T7 Execute the run; write `reports/phase116_harmonization_results.json` + `reports/phase116_harmonization_summary.md` (per-hypothesis verdicts with numbers; §6 recommendation verbatim-assembled; assumptions list).
- [ ] T8 Full backend suite + foundation check (H21); ruff clean.
- [ ] T9 Ledger entries (root `LEDGER.md`, `glossa-indus/LEDGER.md`; AI disclosure).
- [ ] T10 One PR (no merge — owner's explicit say-so required).
