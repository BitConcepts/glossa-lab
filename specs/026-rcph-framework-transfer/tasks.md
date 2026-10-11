# Spec 026 — Tasks

## Stage S1 — Lifecycle + machinery

- [x] T1 — Tooling verification (Step A): versions + invocation
      mechanisms recorded in working/tooling.md. **Done
      2026-10-10:** specify 1.0.10; AEE ext v1.1.0; evaluator
      v1.0.0; aee pkg 1.0.4 (Glossa venv, PATH-pinned).
- [x] T2 — Transfer map (FR-026-1): transfer-map.md, 12
      principles + non-transfer section. **Done 2026-10-10.**
- [x] T3 — Claim register + integrity machinery (FR-026-2):
      claims.json (16 atomic claims after AEE-driven
      decomposition); backend/glossa_lab/framework026.py;
      backend/tests/test_framework026.py (11 tests incl. planted
      cycle + planted forbidden inheritance + tamper cases).
      **Done 2026-10-10: 11 passed, ruff clean.**
- [x] T4 — Freeze/replay machinery (FR-026-3): build_freeze /
      verify_freeze in framework026.py, covered by T3 tests.
      **Done 2026-10-10.**
- [x] T5 — Classification criteria frozen (FR-026-5, first
      half): classification-criteria.md in this PR; the register
      may only be built after this PR merges.
- [x] T6 — AEE assess at specify stage (FR-026-4): three rounds
      saved under aee/; round-1 prose assess = vacuous 0-claim
      pass (finding, not accepted); final outcome
      **gather_evidence** (16 claims, all 0.9945/high, 5 residual
      heuristic failure modes) with all named recovery actions
      performed and recorded in aee/recovery-specify.md. Closure
      proceeds on completed recovery, outcome recorded verbatim —
      not rounded up.
- [x] T7 — AEE assess at plan + tasks stages; artifacts saved
      under aee/. **Done 2026-10-10:** both stages outcome
      **gather_evidence** (16 claims, all 0.9945/high, same 5
      residual heuristic failure modes as specify round 3);
      evaluator composed outcome under the strict strategy =
      gather_evidence (aee/evaluator-composed-strict.json).
      `speckit.evaluator.run` itself has no registered evaluators
      in this repo (no evaluators.yml) — its honest standalone
      output is a pass noting none configured; the operative
      evaluator results are the AEE-produced contract results,
      recorded here rather than papered over.
- [x] T8 — Analyze + converge for S1: spec/plan/tasks/checklist
      cross-checked (analyze: FR-026-1…8 ↔ tasks T1–T16 ↔
      checklist CQ/CR/CF all trace; no orphan requirements);
      PR merged on CI verified from the run's own conclusion +
      job logs. **Done 2026-10-10:** PR #138 merged
      (569ef565) on CI run 38106746647 completed success,
      verified from the run record + job list (6/7 jobs success
      with Playwright last to conclude; an early watch exit was
      NOT trusted — the run record governed).

## Stage S2 — Impact register

- [x] T9 — register-classifications.json authored per frozen
      criteria (one entry per inventory item, rationale each).
      **Done 2026-10-10:** 116 entries; counts by class —
      RERUN-REQUIRED 8, REPRODUCE-ONLY 12, REINTERPRET-ONLY 61,
      UNAFFECTED 27, NOT-RERUNNABLE 8.
- [x] T10 — Register generator + emitted impact-register
      .json/.csv/.md; completeness asserted (rows = inventory
      items); PR merged before any rerun work begins.
      **Done 2026-10-10 (build side):** generator strict
      (duplicates/missing/extra/class-validity all abort);
      --check drift-free; tests in
      backend/tests/test_spec026_register.py pin completeness
      and the exact RERUN-REQUIRED set {SPEC-023, SPEC-024,
      SPEC-025, PHASE-132, PHASE-134, PHASE-135, PHASE-137,
      PHASE-140}.

## Stage S3 — Rerun freezes

- [ ] T11 — Rerun contract per RERUN-REQUIRED item under
      reruns/ (correction, computation, margin, seeds, input
      hashes, comparison format), frozen by merge.
- [ ] T12 — H23 steps 1–4 per rerun phase (script, graph
      module, registration, registration verified) inside the
      freeze PR — scripts written, not yet run.

## Stage S4 — Rerun executions

- [ ] T13 — Each rerun executed (H23 step 5) under its frozen
      contract; results + comparison report per rerun; one PR
      per phase; foundation check after each.

## Stage S5 — Assessments + closeout

- [ ] T14 — historical-assessments.md/.json for every
      status-changed item; originals untouched (diff-checked).
- [ ] T15 — AEE assess at implement stage + gaps after verify;
      artifacts under aee/.
- [ ] T16 — Full suite + foundation check on merged main;
      anchors byte-identical; both ledgers appended; converge
      decision recorded here. No publication.
