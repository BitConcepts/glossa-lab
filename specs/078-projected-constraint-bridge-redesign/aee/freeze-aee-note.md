# Spec 078 — AEE hook artifacts at the freeze (honest record; the Spec 075 form)

The spec-kit AEE hooks ran against this spec's
claim register (`claims.json`, 10 claims
F078-C01…F078-C10, register_version 0.7-draft —
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

- `aee-after_specify-20261026T144557Z.json` +
  `evaluator-aee-after_specify-20261026T144557Z.json`
- `aee-after_plan-20261026T144557Z.json` +
  `evaluator-aee-after_plan-20261026T144557Z.json`
- `aee-after_tasks-20261026T144557Z.json` +
  `evaluator-aee-after_tasks-20261026T144557Z.json`

**What the hooks returned (identical at all three
phases, recorded as it happened).** The assess
summary at each phase is "Assessed 10 claim(s);
found 19 failure mode(s); 0 claim(s) below the
0.70 confidence threshold." The 19 findings in each
evaluator artifact are:

- **10 draft caps** — one per claim
  (`AEE-F078-Cnn-DRAFT-CAP`): the FR-2.3 draft cap,
  the standing behaviour for claims in `draft`
  status; the cap is a status cap, not a defect
  found in any claim, and **zero claims sit below
  the 0.70 threshold** (propagated confidences:
  C01 0.9445, C02 0.9445, C03 0.8695, C04 0.8695,
  C05 0.7950, C06 0.9445, C07 0.9445, C08 0.9445,
  C09 0.7200, C10 0.7950; minimum 0.7200).
- **9 irreducibility challenges**
  (`-IRREDUCIBILITY-CHALLENGE`, severity medium,
  kind `coverage_gap`, "Claim may contain multiple
  independently falsifiable propositions") on
  F078-C01, C02, C03, C04, C06, C07, C08, C09, C10.
  (F078-C05, A-DIR, drew no challenge: it is a
  single convention stated in one sentence.)
- **No counterexample challenge** — where Spec 076
  drew one (on its F076-C09), this register drew
  none; the difference is recorded, not explained
  away.

**How the challenges are answered — from the
spec's own structure, as at Specs 075/076.** They
are recorded here, not smoothed over:

- The irreducibility challenges name compound
  *requirement* and *assumption* claims. Each
  challenged claim carries its falsification tests
  on its face, and its sub-parts are not
  free-floating: C01's soundness is judged by one
  named recomputation (the successor pilot's step
  0, with the C2 record as the freeze-time
  instance); C02's by the pilot's §7.4 verdict
  bands, each band a separate named death; C03's
  by inspection of the filed register and coding
  file against the triple form; C04/C05/C07 are
  the design's §4.3 inheritance itself — the
  assumption set inherited as separately filed,
  separately falsifiable claims precisely so that
  one can fall without the others; C06
  (A-FACE-2) carries *two* falsification tests
  because the design gives it two named deaths
  (the residue case and the pattern-mode failure)
  — the pair is the claim's content, not two
  claims sharing a coat; C08's by the pilot's
  step-3′ counts against four separately stated
  failure conditions; C09/C10's by inspection of
  every output against their boundaries. The
  decomposition the challenge asks for exists; it
  lives in the spec's gate and claim structure
  rather than in a multiplied claim count, and
  splitting the register to silence a heuristic
  would not change any gate.

The nine challenges are advisory `*-CHALLENGE`
records (category `coverage_gap`). No finding of
any other kind appears in any of the six artifacts
— no contradiction, no independence or ambiguity
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
