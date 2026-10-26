# Spec 077 — AEE hook artifacts at the freeze (honest record; the Spec 075/076 form)

The spec-kit AEE hooks ran against this spec's
claim register (`claims.json`, 10 claims
F077-C01…F077-C10, register_version 0.7-draft —
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

- `aee-after_specify-20261026T142310Z.json` +
  `evaluator-aee-after_specify-20261026T142310Z.json`
- `aee-after_plan-20261026T142310Z.json` +
  `evaluator-aee-after_plan-20261026T142310Z.json`
- `aee-after_tasks-20261026T142310Z.json` +
  `evaluator-aee-after_tasks-20261026T142310Z.json`

**What the hooks returned (identical at all three
phases, recorded as it happened).** The assess
summary at each phase is "Assessed 10 claim(s);
found 21 failure mode(s); 0 claim(s) below the
0.70 confidence threshold." The 21 findings in each
artifact are: the 10 FR-2.3 draft caps (one per
claim — every claim is draft at a freeze, and the
cap lifts only on ratification, which is the
execution's business, not the freeze's); 10
irreducibility challenges (one per claim); and 1
negation-conflict challenge (F077-C01 against
F077-C03). No claim falls below the 0.70 threshold
(the minimum propagated confidence is 0.7200,
F077-C09). There are no findings of independence
or ambiguity kind, and no evidence-resolution
failures.

**How the challenges are answered (DD-077-3; the
register was not reworded to silence them).**

- *Irreducibility (all 10 claims).* Each claim is a
  single proposition with its machinery carried in
  the spec's own sections: C01 is one share against
  one bar (its administration — FF-3/FF-4/FF-5 — is
  spec text, not further claims); C02 is one
  two-condition rule; C03–C10 are each a single
  gate, reproduction, map, administration,
  sensitivity, deliverable, or input condition. The
  register's structure is the decomposition the
  challenge asks for: the verdict-bearing claims
  are two, and everything else is filed as its own
  claim precisely so it can fail on its own.
- *Negation conflict (F077-C01 vs F077-C03).* The
  two claims do not contradict; they are a claim
  and its gate. C01 asserts the witnessing share
  under the frozen match rules over the pinned
  inputs; C03 asserts that the execution runs only
  if those pins verify first-hand, and closes the
  execution if any fails. C01's truth is therefore
  conditional on C03's gate in exactly the way the
  spec states (§4.1 step 0 precedes counting; a
  step-0 failure files no C01 verdict at all, in
  either direction). A gate that can stop a claim
  from being tested is not a negation of the claim.

**What this note does not establish:** that the
register is right. The evaluator's challenges are
answered from the spec's structure; the claims
themselves stand or fall at the execution, under
their own falsifiers.
