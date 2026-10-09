# Tasks — Spec 022 / Phase-131 Source-of-Disagreement Attribution

## Phase (owner-authorized 2026-10-09)

- [x] T1 Spec 022 (spec/plan/tasks) committed alone — pre-registration freeze: non-goals (§0: attribution diagnostics ONLY; Phase-125 FAIL FINAL; spec 020 NO stands), join discipline (A3: no CISI-ID join on Holdat keys), arms A–D with operational definitions, support/estimability criteria (noise-band bound 0.131316; MIN_MATCHED 10; MIN_STRATUM_PAIRS 4), synthesis estimators + overlap rule, claim scope.
- [x] T2 Core module `backend/glossa_lab/phase131_attribution.py` (spec §§3–6 machinery, reusing Phase-113/125/127 profile/TV code).
- [x] T3 Orchestration `backend/glossa_lab/phase131_run.py` + runner `backend/scripts/phase131_attribution.py` (frozen inputs via their loaders; corpus totals + anchors hash asserted; judgeable set read from the Phase-125 results of record; noise band read from the Phase-127 results of record).
- [x] T4 Unit tests `backend/tests/test_phase131_attribution.py`, incl. toy hand-computed controls per arm, estimability gates, determinism, and real-input pins (16 judgeable pairs; observed median TV 0.636931; noise band [0.046665, 0.131316]).
- [x] T5 H23 gate: graph module `backend/glossa_lab/experiment_graph_phase131_attribution.py` (node `IndusPhase131Attribution`) + registration in `experiment_graph.py`, asserted in `ATOMIC_NODES`, before any run.
- [x] T6 Run → `reports/phase131_attribution_results.json` + `reports/phase131_attribution.md`; first lines state attribution-diagnostics-only and that the Phase-125 FAIL and spec 020's NO stand untouched; anchors hash re-asserted unchanged.
- [x] T7 Full backend suite + foundation check (H21); ruff clean.
- [x] T8 Ledger entries (both files; AI disclosure) and one PR; merge only when complete + all 7 CI checks green (standing auto-merge rule); post-merge verification on the merged state (suite counts, anchors hash).

## Explicitly not tasks of this phase

- Re-scoring Phase-125, issuing any verdict, or phrasing any finding as softening the Phase-125 FAIL or spec 020's NO.
- Any anchor, claim, PRED, or status change.
- Any CISI-ID / artifact-key join between Holdat and mayig (spec 019 §2.1 prohibition stands; Arm A S1–S3 are counted and rejected / reported as found, never used).
- Pooling inscriptions across compilations for any statistic.
- Loosening the matcher (threshold, eligibility, mutual-best) or any estimability gate after the freeze to enlarge the matched set.
- Period stratification (no period metadata exists on either side — NOT ESTIMABLE by construction, spec §5.1).
