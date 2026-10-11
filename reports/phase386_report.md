# Phase-386 — Deterministic Replay Audit (Spec 026)

**Register rows:** PHASE-116, PHASE-125, PHASE-127, PHASE-131
(REPRODUCE-ONLY). **Contract:** `specs/026-rcph-framework-
transfer/reruns/phase386-contract.md`, freeze digest
`38258f64cae2330d…` (verified on the execution tree).
**Mechanics:** each original script was re-executed in a
disposable worktree of the frozen tree (so replayed outputs
never touched the committed originals); the comparator
(`phase386_replay_audit.py`) compared headline quantities
against the committed results files. **Results:**
`reports/phase386_results.json`.

| Item | Quantities compared | Outcome |
|---|---|---|
| Phase-116 | median W1 0.4519 (replayed full-precision match), Spearman mean r −0.0826 | **REPRODUCED** |
| Phase-125 | median TV 0.636931; judgeable signs 16; null count 823 / 999 (p = 0.824); verdict FAIL / DISAGREEMENT re-emitted | **REPRODUCED** |
| Phase-127 | Phase-125 median TV of record; matched-size null CI [0.046665, 0.131316]; share of replicates ≥ observed 0.0; bootstrap median-TV CI [0.548638, 0.722042] | **REPRODUCED** |
| Phase-131 | credited share 0.061321; residual unexplained 0.938679 | **REPRODUCED** |

Same/different: **identical** — the verdict-bearing
deterministic chain of Specs 015/019/021/022 replays exactly
from the repository as it stands, including the stochastic
components under their recorded seeds. No verdict changes;
the REPRODUCE-ONLY classifications are discharged. Anchors
unchanged in every replay (each script's own anchors_unchanged
assertion true). Foundation check after the run: 40 passed,
0 failed.
