# Spec 026 — Plan

**Governing documents:** spec.md (this spec), transfer-map.md,
classification-criteria.md. **Tooling record:** working/tooling.md
(spec-kit 1.0.10; AEE ext v1.1.0; evaluator v1.0.0; aee pkg 1.0.4
in the Glossa venv — pinned on PATH for every AEE invocation).

## Stage sequence (each stage its own PR, merged on verified-green CI)

1. **S1 — Lifecycle + machinery.** This spec through the full
   spec-kit lifecycle (constitution check → specify → clarify →
   plan → checklist → tasks → analyze → implement → converge).
   AEE assess at specify/plan/tasks/implement + evaluator results
   saved under `aee/`; the specify-stage assess on prose returned
   0 claims (vacuous pass — recorded as a finding, recovery =
   assess runs against the structured claim register
   `claims.json`, FR-026-2). Machinery: `backend/glossa_lab/
   framework026.py` (claim-register integrity: cycle detection
   via aee_core ClaimGraph + NEW forbidden-assumption
   inheritance check; canonical freeze record + verifier) with
   tests in `backend/tests/test_framework026.py`. Transfer map +
   classification criteria included; criteria are the freeze
   point of this PR.
2. **S2 — Impact register.** Generator script
   (`backend/scripts/spec026_register_build.py`) reads
   `working/inventory.json` + the authored classification table
   (`register-classifications.json`, one entry per inventory
   item, each with rationale) and emits
   `impact-register.json` + `.csv` + `.md`. Register merged
   before any rerun begins.
3. **S3 — Rerun freezes.** For each RERUN-REQUIRED item: a rerun
   contract under `reruns/` (correction type, exact computation,
   margin, seeds, data hashes, comparison format) + the H23
   artifacts in order (phase script, graph module, registration).
   Freeze commit precedes any rerun execution.
4. **S4 — Rerun executions.** One PR per rerun phase: script run
   (timeouts, H9), results JSON, report with original-vs-rerun
   comparison, graph-node verification, foundation check.
5. **S5 — Historical assessments + closeout.** Assessments file
   (MD + JSON) for every status-changed item; ledgers appended;
   full suite + foundation on merged main; AEE `gaps` after
   verify; converge decision recorded in tasks.md.

## Constitution check

- §I provenance: reruns read only recorded, cited data files;
  hashes pinned in freeze records.
- §II ledger: every stage appends to LEDGER.md (+ glossa-indus
  cross-reference where the pattern applies).
- §III foundation gate: run after every phase-result change;
  anchors never modified by this spec.
- §IV falsifiable claims: spec §9 boundaries; AEE via aee_core
  (same engine) + extension assess on the structured register.
- §V public/private: no correspondence material; all artifacts
  are methodology/records.
- §VI AI disclosure: in spec, ledgers, and reports.
- §VII SDD: this lifecycle; graph-first for all rerun phases.
- §VIII verification: tests + ruff on changed Python; CI from
  run conclusions + job logs (never the PR-page rollup).

## Risks

- Register scope (116 items) invites classification drift —
  countered by criteria-first freeze + per-row rationale +
  generator-enforced completeness (every inventory item exactly
  one register row, asserted in tests).
- Rerun scripts for old phases may depend on data layouts that
  moved — each rerun contract names its exact input files +
  hashes; an input that cannot be hash-matched converts the
  rerun to an evidenced hard-stop, not a silent substitution.
- The aee version split (1.0.4 vs 1.0.2 across venvs) could make
  assessment results environment-dependent — PATH pinned +
  version recorded in each artifact.
