# AEE recovery record — specify stage (Spec 030 freeze)

Governing rule (Spec 026): an AEE outcome stricter than
`warn` blocks closure until the recovery work named by
the assessment is completed and recorded. The
assessment is a governance signal, not a probability
that a claim is true. Invocation for every round:
`.specify/extensions/aee/scripts/python/run_aee.py
assess --input specs/030-q6-chronology-spine-extension/
claims.json --phase <phase> --threshold 0.70 --project
glossa-lab-spec030`, Glossa venv first on PATH (AEE
package 1.0.4; specify CLI 1.0.10; AEE extension
v1.1.0; evaluator extension v1.0.0).

## Rounds

- **Round 1** (`20261012T170809Z`, after_specify, on
  the register as merged in PR #170): outcome
  `iterate`; 7 claims assessed, 11 failure modes, 0
  claims below the 0.70 threshold (every claim scored
  0.9945, band high — the register already carried
  evidence lists and boundary confirmations from
  drafting). Failure classes: **irreducibility
  challenges ×7** (one per claim — compound claim
  texts carrying enumerations and second clauses) and
  **negation-conflict challenges ×4**, all against
  F030-C01 (paired with C03, C05, C06, C07 — pairs
  whose texts share vocabulary while differing in
  negation polarity).
- **Recovery 1:** claim texts rewritten as single
  atomic propositions, in the Spec 028 recovery
  pattern. The enumerations and secondary clauses the
  texts carried were moved into the claims'
  boundaries verbatim in substance (C01's frozen-set
  enumeration, C02's trace-field list and not-built
  clause, C03's lab-code identity rule, C05's three
  prohibitions, C06's release bar, C07's closure
  consequences); boundaries and verdict rules are
  unchanged in substance, and no falsification test
  was altered. Pairwise boundary confirmations for
  the four flagged pairs were added to
  F030-C01's `boundary_confirmation` with reciprocal
  sentences on C03, C05, C06, and C07. Register
  integrity re-verified with
  `glossa_lab.framework026.check_dependency_integrity`
  (no cycles, no missing dependencies, no forbidden
  inheritance). Register version 0.1-draft →
  0.2-draft, with the change recorded in the
  register's note.
- **Round 2 / final** (`20261012T171217Z` /
  `20261012T171218Z`): outcome **pass** at all three
  lifecycle phases (after_specify, after_plan,
  after_tasks) on the recovered register — 7 claims,
  0 failure modes, 0 claims below the 0.70 threshold;
  AEE exit code 0. Evaluator-contract results pass
  with the same summary. The final after_specify
  artifacts are also copied as `assess-specify.json`
  and `evaluator-specify.json`.

## Evaluator residual

`speckit.evaluator.run` has no registered evaluators
in this repository (unchanged from Specs 026–029);
the operative evaluator-contract result is the
AEE-produced one saved beside the assessment
artifacts in this directory.
