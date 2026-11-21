# Spec 098 — Test Cases

Both test cases are implemented in `tests/test_seal_and_score.py`
against the reference implementation of the frozen mechanisms in
`tools/seal_and_score.py`, run on synthetic fixtures only (no real
inscription, no held-out material). Execution at adoption is
recorded, with payload verdicts, in
`records/tc-execution-2026-11-21.md`.

## TC-098-01 — Seal and split integrity

*Exercises:* C098-1 (nothing scored before freeze and seal),
C098-2 (frozen population mechanics).
*Fixture:* 200 synthetic cluster ids (`FIX-0000`..`FIX-0199`).
*Assertions:*
1. The split is deterministic and order-independent, and every
   cluster's assignment agrees with the frozen rule recomputed
   independently in the test (`SHA-256("098-split-v1:" + id)
   mod 5 == 0`); development and held-out sides are disjoint and
   exhaustive; the held-out share lands in the band the 20
   percent rule implies.
2. The seal hash recomputes from the held-out list, and fails
   verification on a list with one id replaced or one id added.
3. The development export contains zero held-out cluster ids,
   and the scoring path's guard raises `SealViolation` when a
   development input contains a held-out id.
*Pass condition:* all assertions hold; the test process exits 0.

## TC-098-02 — Decision-rule behaviour on planted cases

*Exercises:* C098-4 (value-relevance gate), C098-5 (decision
rules as frozen), C098-6 (contamination ceiling on outcome
names).
*Fixture:* planted per-sign scoring inputs (held-out token
counts, candidate and best-rival log-likelihoods, permutation-
null 99th percentiles) fed to the frozen `decide` rule.
*Assertions:*
1. A discriminable sign (margin 18 nats, above the null's 99th
   percentile, 12 held-out tokens, accepted sheet) returns
   DISCRIMINATED ON PSEUDO-HELD-OUT on the in-corpus arm and
   IDENTIFIABLE ON HELD-OUT on the genuine arm — the ceiling is
   in the outcome name, not in a footnote.
2. An observationally equivalent sign (margin 0.5 nats) returns
   NOT IDENTIFIABLE.
3. A margin above the 10-nat bar but below the null's 99th
   percentile returns NOT IDENTIFIABLE.
4. A sign with 3 held-out tokens returns UNDECIDABLE AT THIS
   POWER even with an overwhelming margin (precedence of the
   power rule).
5. A sign with no accepted prediction sheet returns NOT
   IDENTIFIABLE by construction, whatever its margin.
6. The flexibility penalty moves a variant-carrying case across
   the bar: raw margin 17 nats passes; charged with six free
   choices at the frozen 2 nats each, the penalized margin of
   5 nats returns NOT IDENTIFIABLE.
*Pass condition:* all assertions hold; the test process exits 0.
