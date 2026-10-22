# Spec 027 — Tooling Verification

Verified in the fresh worktree
`~/workspace/glossa-lab-spec027` on 2026-10-11. The local
checkout at `~/workspace/glossa-lab` was not used.

| Item | Version / fact | Evidence |
|---|---|---|
| `specify` CLI | 1.0.10 | `~/workspace/venvs/spec-kit/bin/specify --version` |
| AEE extension | v1.1.0, enabled | `specify extension list` |
| Evaluator extension | v1.0.0, enabled | `specify extension list` |
| AEE package on the pinned lifecycle PATH | 1.0.4 | Glossa venv `aee --version` |
| AEE package in the spec-kit venv | 1.0.2 | Spec-kit venv `aee --version` |

## Invocation rule

All AEE lifecycle invocations for Spec 027 run
`.specify/extensions/aee/scripts/python/run_aee.py assess`
against `specs/027-movement-culture-language/claims.json` with
the Glossa venv first on `PATH`, threshold 0.70, and project
`glossa-lab-spec027`. The version used is therefore 1.0.4 for
every saved run in this draft. A run made with the ambient PATH
is not comparable and must not be saved as a lifecycle output.

## Known residuals

- The evaluator extension has **no registered evaluators** in
  this repository (no `evaluators.yml`). The operative
  evaluator-contract outputs are produced by AEE assess through
  its evaluator adapter. A standalone evaluator run would
  honestly report that none are configured.
- The AEE package version split across venvs (1.0.4 versus
  1.0.2) is a real reproducibility hazard. It is controlled
  here by PATH pinning and this record; it is not eliminated.
- Extension hooks are marked optional in `.specify/
  extensions.yml`; Spec 027 treats them as mandatory for its
  own lifecycle, following Spec 026.
