# Plan — Spec 011 / Phase-113

1. **Spec first (pre-registration).** Spec 011 written and
   committed ALONE, before any battery implementation is run
   against any anchor and before any calibration or validation
   statistic exists. Git order is the pre-registration proof.
2. **Machinery (pure, deterministic).** `phase113_battery.py`:
   corpus loaders (Holdat via the existing `load_holdat_corpus`
   loader machinery; ICIT converted layer from the gitignored
   downloads area, main-checkout fallback path), positional
   profiles (Phase-69 I/M/T convention), deterministic
   syllabifier for the §3 canon, T1/T2/T3 evaluators, the §5
   decision rule. No SA artifact is imported or read; the
   syllabic LM is not used.
3. **Unit tests.** `test_phase113_battery.py`: syllabifier canon
   cases (legal + cluster failures), profile/modal/TV arithmetic
   on toy corpora, decision-rule truth table, set recomputation
   assertions (44 / 94 / 113), and a toy end-to-end: a synthetic
   anchor planted with core-consistent behavior validates; a
   synthetic isolated anchor does not.
4. **H23 gate.** Graph module `experiment_graph_phase113.py`
   (node `IndusPhase113NonSaValidation`, loads the results
   report), registration in `experiment_graph.py`, assertion of
   the node ID in `ATOMIC_NODES` — all before the runner executes.
5. **Calibration.** Runner executes §4: battery over STRICT94
   (leave-one-out) and KUR113. Gates: strict VALIDATED ≥ 57/94;
   kur VALIDATED ≤ 5/113. Failure → battery rejected; reports +
   ledgers written; phase stops with the anchors file untouched.
6. **Main run (only if calibration passes).** Battery over
   FLAGGED44; §5 applied mechanically; anchors file updated;
   change register written (one record per flagged anchor,
   including UNRESOLVED non-actions).
7. **Verification.** Full backend suite (baseline 643 passed /
   11 skipped) and `foundation_check.py` (H21; baseline
   40 / 0 / 8) in the worktree venv; ruff over all new/changed
   Python before push.
8. **Record + PR.** Results JSON + summary MD (calibration
   outcomes first, whatever they show; per-test tallies; final
   tier counts; new strict-core size and Holdat coverage);
   ledger entries in both ledgers with AI disclosure; one PR
   from `phase/nonsa44-validation`. No merge — the owner merges
   science PRs on explicit say-so.
