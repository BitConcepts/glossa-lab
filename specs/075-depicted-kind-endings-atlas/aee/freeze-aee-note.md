# Spec 075 — AEE hook artifacts at the freeze (honest record; the Spec 074 form, with one recorded difference)

The spec-kit AEE hooks ran against this spec's
claim register (`claims.json`, 13 claims
F075-C01…F075-C13, register_version 0.7-draft —
the recovered register form, §3 of the
adjudication) with the pinned evaluator
(aee 1.5.3, `tools/freeze-gate/evaluator-version.txt`)
in the freeze configuration:

```
aee assess --input claims.json --lenient --no-ledger --phase <hook>
```

for the three hooks `after_specify`,
`after_plan`, `after_tasks`, writing the result
JSON and the evaluator JSON into this directory:

- `aee-after_specify-20261025T161923Z.json` +
  `evaluator-aee-after_specify-20261025T161923Z.json`
- `aee-after_plan-20261025T161923Z.json` +
  `evaluator-aee-after_plan-20261025T161923Z.json`
- `aee-after_tasks-20261025T161923Z.json` +
  `evaluator-aee-after_tasks-20261025T161923Z.json`

**What the hooks returned (identical at all three
phases, recorded as it happened).** The assess
process exits non-zero (as it does for every
draft register — Spec 074's record is the same),
with the summary "Assessed 13 claim(s); found 22
failure mode(s); 0 claim(s) below the 0.70
confidence threshold." The 22 findings in each
evaluator artifact are:

- **13 draft caps** — one per claim
  (`AEE-F075-Cnn-DRAFT-CAP`): the FR-2.3 draft
  cap, the standing behaviour for claims in
  `draft` status; the cap (0.70) is a status
  cap, not a defect found in any claim, and
  every claim's propagated confidence sits at
  the cap with **zero claims below 0.70**.
- **7 irreducibility challenges**
  (`-IRREDUCIBILITY-CHALLENGE`, severity medium,
  kind `coverage_gap`, "Claim may contain
  multiple independently falsifiable
  propositions") on F075-C06, C07, C08, C09,
  C10, C12, C13.
- **2 counterexample challenges**
  (`-COUNTEREXAMPLE-CHALLENGE`) on F075-C09 and
  F075-C12.

**The recorded difference from Spec 074.** Spec
074's register drew only the 13 draft caps under
the same pinned evaluator and configuration.
This register additionally drew the 9 challenges
above. They are recorded here, not smoothed
over, and the freeze proceeds on this record for
the reasons stated next — the challenges are
advisory coverage-gap findings about claim
*shape*, and each is answered by the spec's own
structure:

- The irreducibility challenges name compound
  *requirement* claims. Each challenged claim
  carries exactly one falsification test, and
  its sub-parts are not free-floating: they are
  the spec's separately gated steps — gate 0.4's
  population reproduction and keying (C06, C08),
  gate 0.5's census and floors (C07), §4.4's
  census-only rule (C10), §1.4's arm discipline
  (C09), the append-only diff rule (C12), and
  §9's travelling cautions (C13) — each of which
  closes or falsifies **individually** at an
  execution. The decomposition the challenge
  asks for exists; it lives in the spec's gate
  structure rather than in a multiplied claim
  count, and splitting the register to silence a
  heuristic would not change any gate.
- The counterexample challenges name the two
  universal programme rules (C09: the celestial
  arm is *never* tested; C12: frozen records are
  *never* edited). A universal rule is falsified
  by a single counterexample, and each claim's
  stated falsification test is exactly that
  counterexample's form ("a celestial rate … in
  any product falsifies this claim"; "an edited
  line in a frozen record … falsifies this
  claim"). The universality is the rule's
  content, not a drafting accident.

The nine challenges are advisory `*-CHALLENGE`
records (in the assess artifacts they carry the
categories `coverage_gap` for the irreducibility
seven and `assumption_unvalidated` for the
counterexample two). No finding of any other
kind appears in any of the six artifacts — no
contradiction, no independence or ambiguity
finding, no pin or citation failure in the hook
configuration — and no claim scores below the
0.70 threshold (minimum propagated confidence
0.8695 in each artifact).

**What these artifacts are.** The register these
hooks certify is the register this freeze
freezes; the freeze test replays the six
artifacts' shape in CI. The hooks' non-zero exit
is the standing draft-state behaviour recorded
by every frozen spec in this line (071, 073,
074); it is not waived, hidden, or re-described
as a pass — the freeze is the act that freezes a
draft register under the cap, and the cap is
named in the register's own note.
