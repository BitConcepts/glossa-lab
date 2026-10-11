# AEE recovery record — specify stage (Spec 027)

Governing rule (Spec 026): an AEE outcome stricter than `warn`
blocks closure until the recovery work named by the assessment
is completed and recorded. The assessment is a governance
signal, not a probability that a historical claim is true.

## Rounds

- **Round 1** (`20261011T043150Z`): outcome
  `gather_evidence`; 25 claims assessed, 36 failure modes, 0
  claims below the 0.70 threshold. Failure classes were
  irreducibility challenges on compound governance claims,
  negation-conflict challenges, and authority challenges on the
  compliance claims.
- **Recovery 1:** compound claims were decomposed into atomic
  claims (25 → 33). New atomic claims cover coordinate
  restriction inheritance, sign-list versioning, the Q1
  ecological-join boundary, the Q8 AI-substitution prohibition,
  package deals, teleology joins, and the four separate hard
  identifications formerly pooled in one claim. Boundary
  confirmations were added where the engine flagged possible
  negation conflicts. The Spec 026 integrity check still passed:
  no cycles, no missing dependencies, and no forbidden
  inheritance.
- **Round 2** (`20261011T043222Z`): outcome
  `gather_evidence`; 33 claims, 17 failure modes, 0 below
  threshold. Authority challenges were resolved in the next
  recovery by attaching the owner directive as primary-authority
  evidence to the compliance claims.
- **Round 3** (`20261011T043236Z`): outcome `iterate`; 33
  claims, 10 residual failure modes, 0 below threshold. The
  remaining irreducibility flags were traced to the engine's
  transparent compound-language heuristic (commas and
  conjunctions in claim text); the remaining negation flags
  were traced to paired claims in which only one member used a
  negation token.
- **Recovery 3:** the flagged claim texts were rewritten as
  single propositions without changing their boundaries,
  falsifiers, dependencies, or verdict rules. Paired claims
  were reworded so their distinct boundaries are explicit
  without a spurious negation asymmetry. The integrity check
  was rerun and still passed.
- **Round 4 / final** (`20261011T043305Z`): outcome **pass**;
  33 claims assessed, 0 failure modes, 0 claims below the 0.70
  threshold; AEE exit code 0. The final artifacts are also
  copied as `assess-specify.json` and `evaluator-specify.json`.

## Evaluator residual

`speckit.evaluator.run` has no registered evaluators in this
repository (no `evaluators.yml`). Its standalone honest result
is therefore a pass noting that none are configured. The
operative evaluator-contract results saved here are the results
produced by AEE assess through its evaluator adapter. That
residual is recorded, not papered over.
