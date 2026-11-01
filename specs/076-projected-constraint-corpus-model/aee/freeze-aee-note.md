# Spec 076 — AEE hook artifacts at the freeze (honest record; the Spec 075 form)

The spec-kit AEE hooks ran against this spec's
claim register (`claims.json`, 10 claims
F076-C01…F076-C10, register_version 0.7-draft —
the recovered register form) with the pinned
evaluator (aee 1.5.3,
`tools/freeze-gate/evaluator-version.txt`) in the
freeze configuration:

```
aee assess --input claims.json --lenient --no-ledger --phase <hook>
```

for the three hooks `after_specify`, `after_plan`,
`after_tasks`, writing the result JSON and the
evaluator JSON into this directory:

- `aee-after_specify-20261026T111349Z.json` +
  `evaluator-aee-after_specify-20261026T111349Z.json`
- `aee-after_plan-20261026T111349Z.json` +
  `evaluator-aee-after_plan-20261026T111349Z.json`
- `aee-after_tasks-20261026T111349Z.json` +
  `evaluator-aee-after_tasks-20261026T111349Z.json`

**What the hooks returned (identical at all three
phases, recorded as it happened).** The assess
summary at each phase is "Assessed 10 claim(s);
found 19 failure mode(s); 0 claim(s) below the
0.70 confidence threshold." The 19 findings in each
evaluator artifact are:

- **10 draft caps** — one per claim
  (`AEE-F076-Cnn-DRAFT-CAP`): the FR-2.3 draft cap,
  the standing behaviour for claims in `draft`
  status; the cap is a status cap, not a defect
  found in any claim, and **zero claims sit below
  the 0.70 threshold** (propagated confidences:
  C01 0.9445, C02 0.9445, C03 0.8695, C04 0.8695,
  C05 0.7950, C06 0.7200, C07 0.9445, C08 0.9445,
  C09 0.7200, C10 0.7950; minimum 0.7200).
- **8 irreducibility challenges**
  (`-IRREDUCIBILITY-CHALLENGE`, severity medium,
  kind `coverage_gap`, "Claim may contain multiple
  independently falsifiable propositions") on
  F076-C01, C03, C04, C06, C07, C08, C09, C10.
- **1 counterexample challenge**
  (`AEE-F076-C09-COUNTEREXAMPLE-CHALLENGE`,
  severity high, kind `assumption_unvalidated`).

**How the challenges are answered — from the
spec's own structure, as at Spec 075.** They are
recorded here, not smoothed over:

- The irreducibility challenges name compound
  *requirement* and *assumption* claims. Each
  challenged claim carries exactly one
  falsification test, and its sub-parts are not
  free-floating: C01's soundness is judged by two
  named recomputations (the C2 record and pilot
  step 0); C03's by inspection of the filed
  register against the vocabulary; C04–C07 are
  the design's §3.1 decomposition itself — the
  assumption set split into four separately filed,
  separately falsifiable claims precisely so that
  one can fall without the others; C08's by the
  pilot's step-3 count; C09/C10's by inspection of
  every output against their boundaries. The
  decomposition the challenge asks for exists; it
  lives in the spec's gate and claim structure
  rather than in a multiplied claim count, and
  splitting the register to silence a heuristic
  would not change any gate.
- The counterexample challenge names C09, a
  universal programme rule (the register *never*
  identifies; the ranking *never* scores). A
  universal rule is falsified by a single
  counterexample, and C09's stated falsification
  test is exactly that counterexample's form ("an
  output of this spec stating a set identity … 
  falsifies this claim"). The universality is the
  rule's content, not a drafting accident.

The nine challenges are advisory `*-CHALLENGE`
records (categories `coverage_gap` for the
irreducibility eight, `assumption_unvalidated`
for the counterexample one). No finding of any
other kind appears in any of the six artifacts —
no contradiction, no independence or ambiguity
finding, no pin or citation failure in the hook
configuration — and no claim scores below the
0.70 threshold.

**What these artifacts are.** The register these
hooks certify is the register this freeze freezes;
the freeze test replays the six artifacts' shape
in CI. The hooks' outcome (`iterate`) is the
standing draft-state behaviour recorded by every
frozen spec in this line; it is not waived,
hidden, or re-described as a pass — the freeze is
the act that freezes a draft register under the
cap, and the cap is named in the register's own
note.
