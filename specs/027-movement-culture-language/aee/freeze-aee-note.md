# AEE record — Spec 027 freeze state (2026-10-11)

Run at the freeze, after the owner adjudication was recorded
in `adjudication.md`, against the frozen claim register.

- **Invocation:** `.specify/extensions/aee/scripts/python/run_aee.py
  assess --input specs/027-movement-culture-language/claims.json
  --phase after_tasks --threshold 0.70 --project glossa-lab-spec027`,
  Glossa venv first on PATH (AEE package 1.0.4; specify CLI
  1.0.10; AEE extension v1.1.0; evaluator extension v1.0.0 —
  pinned as in `working/tooling.md`).
- **Phase mapping (recorded, not hidden):** the evaluator
  adapter supports only `after_specify`, `after_plan`, and
  `after_tasks`. A first attempt with `--phase after_freeze`
  failed with `unsupported evaluator phase: after_freeze`
  (exit 2; a partial runtime assessment file remains in the
  gitignored `.specify/extensions/aee/assessments/` runtime
  directory and is not a lifecycle artifact). The freeze-state
  run therefore used `after_tasks` — the lifecycle position of
  the register being frozen — and its outputs are saved here
  as `aee-after_freeze-20261011T123623Z.json` and
  `evaluator-aee-after_freeze-20261011T123623Z.json`. The
  `phase` field inside both files reads `after_tasks`, which
  is the engine's label; this note is the mapping record.
- **Outcome:** AEE assess **pass** — 33 claims, 0 failure
  modes, 0 claims below the 0.70 threshold; exit code 0.
  Evaluator-contract result **pass** with the same summary.
- **Register identity:** `claims.json` at the freeze is
  byte-identical to the draft-final register (sha256
  `7d27d401125a6bc38e3c5380b82932760b2fd330678b71bb99385d91eece8db6`).
  Adjudication changed decisions, not claims.
- **Known residuals (unchanged from the draft):** the
  evaluator extension has no registered evaluators in this
  repository; the operative evaluator-contract result is the
  AEE-produced one. The AEE package version split across venvs
  (1.0.4 Glossa / 1.0.2 spec-kit) is controlled by PATH
  pinning, not eliminated.
