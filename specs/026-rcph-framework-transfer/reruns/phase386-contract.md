# Rerun Contract — Phase-386 (deterministic replay spot set)

**Type:** REPRODUCE-ONLY verification for the verdict-bearing
deterministic chain. **Register rows:** PHASE-116, PHASE-125,
PHASE-127, PHASE-131 (and the spec rows that mirror them:
SPEC-015, SPEC-019, SPEC-021, SPEC-022). **Frozen:** at the S3
merge. Freeze record: `phase386-freeze.json`.

## Computation (exactly this)

Mechanics (amended before freeze, 2026-10-10): each original
script is re-executed in a DISPOSABLE worktree of the frozen
tree, so its outputs land in the copy and the committed
originals in the real tree are never overwritten. The Phase-386
comparator (`backend/scripts/phase386_replay_audit.py`) then
compares the replayed results files against the committed ones,
quantity by quantity. An item whose script cannot be
re-executed in the disposable tree (missing local store,
environment drift) is recorded NOT REPRODUCIBLE with the
evidenced reason — never silently skipped and never
substituted with a different computation.

For each item, the comparison covers the headline quantities:

- PHASE-116: median W1 0.4519, Spearman rho -0.0826 (recompute
  from the recorded harmonization inputs via the phase116
  script path).
- PHASE-125: median TV 0.636931, null p = 0.824 (recompute via
  backend/scripts/phase125_cross_compilation.py machinery on
  the recorded inputs).
- PHASE-127: null median TV 0.0826, bootstrap CI 0.549-0.722,
  0/999 replicates >= observed (recompute via the phase127
  diagnostic machinery; seed as recorded).
- PHASE-131: attributed share 6.1% / residual 93.9% (recompute
  via the phase131 script path on recorded inputs).

Tolerances declared per item in the script: exact for counts
and shares derived from counts (1e-9), 1e-3 absolute for the
printed rounded statistics above, with full-precision values
compared at 1e-6 relative where the results JSON carries them.

## Outcome rules

Per item: REPRODUCED (all compared quantities within
tolerance), DRIFT (a quantity differs — reported with both
values and the investigated cause), or NOT REPRODUCIBLE
(the recorded computation cannot be re-executed from the
repository as it stands — reason evidenced). No outcome of
this phase changes any original verdict by itself; DRIFT /
NOT REPRODUCIBLE outcomes feed the historical assessments.

## Comparison reported

Per item: recorded values vs replayed values vs outcome.
