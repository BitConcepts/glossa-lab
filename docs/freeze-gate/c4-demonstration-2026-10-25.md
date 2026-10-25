# C4 able-to-fail demonstration — 2026-10-25

The C4 check (`tools/freeze-gate/check_freeze_gate.py`, CI job
"Freeze gate records check (C4)") was demonstrated able to fail
on live CI before any freeze depends on it, as the gate design's
acceptance test requires. Four test PRs each copied one fixture
from `tools/freeze-gate/demo/fixtures/` into a scratch
`specs/999-c4-demonstration/` directory — the path the job's
PR-scope watches, exactly as it will for a real freeze. All four
PRs were closed unmerged and their branches deleted, as
designed. Conclusions below are the C4 job's own, read from
each run; the Backend job passed on all four PRs, so each
failure is the gate's own, not collateral.

| Test PR | Fixture | C4 job conclusion | Run |
|---|---|---|---|
| #383 | missing-c1 (no battery result) | **FAILURE** | 40203200434 |
| #384 | missing-c2 (no spot-check record) | **FAILURE** | 40203206456 |
| #385 | missing-c3 (no evidence-sample record) | **FAILURE** | 40203213916 |
| #386 | complete (all three records, valid) | **SUCCESS** | 40203219363 |

The checker's own words, from the run logs:

- PR #384: `C4 FAIL: specs/999-c4-demonstration` —
  `C2: gate-records/c2-spotcheck.json is missing`
- PR #386: `C4 PASS: specs/999-c4-demonstration`

The machinery's content failures (an unresolved mismatch on a
gate-turning quantity; an unverified verdict-bearing claim; a
stale-evaluator battery result; an unflagged case naming no
blind spot) are covered by the unit tests in
`tools/freeze-gate/tests/` (12 passed at the build), which run
in the same CI job.

**Enforcement state, restated:** the C4 job is not a required
branch-protection check. The first strengthened freeze (the
endings atlas) is the designated shadow freeze; the check
becomes required with the freeze after it.

*AI disclosure: demonstration run by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
