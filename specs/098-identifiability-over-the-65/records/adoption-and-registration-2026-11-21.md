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
- **Ledger intake and full registration: performed in this
  landing** (D-098-3), in the Spec 096/097 pattern. Claims
  C098-1..C098-8 were appended to the canonical ledger through
  tools/ledger/import_bundle.py (route 2), dated 2026-11-21:
  8 appended, 0 already canonical; the ledger grows from
  1,040 lines / 1,009 claims to 1,048 lines / 1,017 claims.
  The program-map taxonomy gains one study entry,
  098-identifiability-over-the-65, domain Anchors & readings,
  subdomain Validation batteries for the SA-lineage anchors,
  Phases 111-119. The settling chain was refreshed in the
  standing order: verify-canonicals 6/6 PASS over the grown
  build before any pin moved; both T405 scenarios re-executed
  (runs settling-20261121T110155Z-e5597c and
  settling-20261121T110155Z-f28db5) with result blocks
  byte-equal to the superseded generations; the Stage 4
  dual-run comparison re-filed from the new pair; assignment
  sets re-materialized unchanged (run
  settling-20261121T110209Z-bb2f40; incumbent 94,
  full-register 286, H003 out of frame); the canonical pin
  refreshed with the re-derivation recorded as
  re_derivations[14]; the superseded generation
  (settling-20261120T213231Z-7d96a8,
  settling-20261120T213235Z-f9e682,
  settling-20261120T213249Z-5a3a46) departed the store with
  its departure accounting appended through
  run_records.append_act. The generated layers were
  regenerated in dependency order (matrix, program map,
  map-data), and every census pin the intake moves was
  updated in the same pull request from the regenerated
  artifacts actuals. An earlier draft of this package
  deferred the intake to a coordinator serialization; the
  program conformance machinery requires the registration in
  the landing pull request itself, and the deferral was
  withdrawn before landing — the record states this so the
  change of plan is not silent.
- No anchor or standing record is changed by this package;
  the ledger, taxonomy, census, and generated-layer changes
  above are the registration, and nothing else.

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
