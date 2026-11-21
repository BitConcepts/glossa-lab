# Spec 098 — Adoption and Registration Record (2026-11-21)

**Adoption act.** The owner's directive of 2026-11-21: execute
all recommendations of the independent Co-scientist audit of
the 94 strict-core Indus readings (findings filed 2026-11-21)
by Sunday 2026-11-22 10:00 AM ET. This package is the audit's
Q5 item 2: a locked, genuinely out-of-sample predictive
comparison with serious alternatives, rerunning
identifiability for the six E readings against stronger
alternatives and extending the identifiability test to the
65 I readings.

**Number.** D-098-1: at the check of 2026-11-21, the highest
landed spec package on origin/main was 097
(`specs/097-meroitic-reproduction-benchmark`), no 098
directory existed, and no branch or open pull request carried
098. This package takes 098.

**What is registered where.**

- The spec package itself (this directory) is the study's
  registration of record: specification, eight AEE claims
  with falsifiers (claims.md; bundle form in
  aee-claims.json), plan, tasks, two implemented test cases,
  the freeze record, and the population annex.
- **Ledger intake: deferred, with the reason on the record
  (D-098-3).** Parallel audit-response packages are landing
  in the same window and touch the same shared files (the
  claims ledger and the census pins it moves). Under the
  program's shared-file discipline, the intake of the
  C098-1..C098-8 bundle through
  `tools/ledger/import_bundle.py` is serialized through the
  coordinator and re-applied on the latest main; it is not
  performed inside this package's pull request, and no shared
  file is touched here. The bundle is complete, parses, and
  matches claims.md claim for claim; the intake is task T004,
  open, with this deferral as its blocker of record.
- No program-map, taxonomy, census, ledger, anchor, or
  standing record is changed by this package.

**Freeze and run state.** The design is frozen
(`records/freeze-v1-2026-11-21.md`). The study is **not run**
in this round (D-098-2): the freeze names two gaps that Stage
1 must resolve on the record before the seal can be honestly
struck — the provenance audit for a genuine-holdout subset
(the candidates were derived on the full historical corpus,
so the in-corpus arm is capped at DISCRIMINATED ON
PSEUDO-HELD-OUT), and the M044/M374 grapheme gap. The test
cases TC-098-01/02 were executed at adoption on synthetic
fixtures only; their payload verdicts are in
`records/tc-execution-2026-11-21.md`. Fixture execution is
not study execution, and this record does not present it as
such.

**Venue.** All work for this package, including the fixture
test execution, ran on tower-compute in a fresh clone under
`~/glossa-work/`. Nothing ran in the coordination VM or on
the mini-server.
