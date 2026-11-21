# Spec 098 — Test-Case Execution Record (2026-11-21)

Executed on **tower-compute** in the fresh clone
`~/glossa-work/ident65-w4-2026-11-21`, on synthetic fixtures
only. No real inscription, no held-out material, and no
scoring-path code for the study itself was run; this record
covers the package's test cases and bundle checks, and is not
study execution (D-098-2).

## TC-098-01 and TC-098-02 — payload verdict

Command:

```
python3 -m unittest discover -s specs/098-identifiability-over-the-65/tests -v
```

Payload verdict (the test process's own record): **10 tests
ran, all ok; process exit code 0.** TC-098-01 contributes 3
tests (split determinism against the frozen rule recomputed
independently in the test; seal recompute and tamper
detection; development-export exclusion and the
`SealViolation` refusal). TC-098-02 contributes 7 tests
(planted discriminable sign passing on both arms under their
different outcome names; planted equivalent sign NOT
IDENTIFIABLE; margin below the null percentile NOT
IDENTIFIABLE; low-count precedence to UNDECIDABLE AT THIS
POWER; no-sheet NOT IDENTIFIABLE by construction; the
flexibility penalty moving a variant case across the bar).

## Bundle consistency check — payload verdict

`aee-claims.json` parses; its claim ids are C098-1..C098-8 in
order, identical to claims.md's claim ids in order; every
claim in both files carries a falsifier and a
does-not-establish line. The pinned AEE assessor
(`~/glossa-work/venvs/glossa-ci/bin/aee`) reports:

- `aee validate`: **valid: 8 claim(s)**, exit 0.
- `aee assess --no-ledger`: outcome **iterate**, exit 1 —
  the expected draft-stage reading for a bundle on asserted
  sources (the same outcome Spec 097's bundle received at
  adoption); the full assessment is filed at
  `records/adoption-aee-assessment.json`.

## What this does not establish

Fixture passage proves the frozen seal, split, and decision
rules behave as written on planted cases. It does not prove
the study's machinery discriminates any real reading; that is
exactly what Stages 1–4 exist to test, and the study-premise
falsifier (spec.md §4) is written against that possibility.
