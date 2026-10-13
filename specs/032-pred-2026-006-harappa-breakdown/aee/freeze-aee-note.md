# AEE record — Spec 032 freeze state (2026-10-13)

Run at the freeze, against the frozen claim register.

- **Invocation:** `.specify/extensions/aee/scripts/
  python/run_aee.py assess --input
  specs/032-pred-2026-006-harappa-breakdown/claims.json
  --phase <phase> --threshold 0.70 --project
  glossa-lab-spec032`, Glossa venv first on PATH
  (AEE package 1.0.4; specify CLI 1.0.10; AEE
  extension v1.1.0; evaluator extension v1.0.0).
- **Outcome:** AEE assess **pass** at all three
  lifecycle phases (after_specify after the three
  recovery rounds recorded in `recovery-specify.md`;
  after_plan; after_tasks) — 12 claims, 0 failure
  modes, 0 claims below the 0.70 threshold; exit
  code 0. Evaluator-contract results pass with the
  same summary.
- **Known residuals (unchanged from Specs 026–031):**
  the evaluator extension has no registered evaluators
  in this repository; the operative evaluator-contract
  result is the AEE-produced one. The AEE package
  version split across venvs (1.0.4 Glossa / 1.0.2
  spec-kit) is controlled by PATH pinning, not
  eliminated.
