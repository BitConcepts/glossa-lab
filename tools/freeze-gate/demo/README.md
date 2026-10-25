# C4 demonstration fixtures

Each directory under `fixtures/` is a make-believe freeze: a
`freeze.json` marker plus a `gate-records/` set that is complete
(`complete/`), missing one record (`missing-c1/`, `missing-c2/`,
`missing-c3/`), or carrying a blocking content failure
(`unresolved-c2/` — an unresolved mismatch on a gate-turning
quantity; `unverified-c3/` — an unverified verdict-bearing
claim). The machinery tests in `../tests/` check the C4 checker
against all six. The checker's able-to-fail demonstration on live
CI copies one fixture at a time into a scratch `specs/`
directory (the C4 job's PR-scope watches `specs/`, as it will
for real freezes) in a test PR that is then closed unmerged;
the results are filed with the build's records. The fixtures
are not real freezes and carry no claim about anything.
