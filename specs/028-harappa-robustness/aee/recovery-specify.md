# AEE recovery record — specify stage (Spec 028)

Governing rule (Spec 026): an AEE outcome stricter than
`warn` blocks closure until the recovery work named by the
assessment is completed and recorded. The assessment is a
governance signal, not a probability that a historical
claim is true.

## Rounds

- **Round 1** (`20261011T154348Z`): outcome
  `gather_evidence`; 15 claims assessed, 26 failure modes,
  0 claims below the 0.70 threshold. Failure classes:
  irreducibility challenges on compound claim texts,
  negation-conflict challenges on paired claims, and one
  authority challenge (high) on the compliance claim.
- **Recovery 1:** claim texts rewritten as single
  propositions (enumerations moved into boundaries and
  metadata, boundaries and verdict rules unchanged);
  pairwise boundary confirmations added for every flagged
  pair, stating the distinct boundary each member governs;
  the compliance claim gained the owner directive and the
  PRED register as evidence. Register integrity re-verified
  (no cycles, no missing dependencies, no forbidden
  inheritance).
- **Round 2** (`20261011T154435Z`): outcome
  `gather_evidence`; 15 claims, 9 failure modes, 0 below
  threshold.
- **Recovery 2:** the compound compliance claim was split
  into two atomic claims (anchors; PRED register — the
  register grew 15 → 16); remaining negation asymmetries
  were reworded into positive single propositions
  ("postdates the freeze merge", "leaves Phase-392's
  record exactly as published", "clearing the practical
  margin", "exploratory only"); the owner directive's
  evidence was marked primary-authority for the compliance
  claims. Integrity re-verified.
- **Round 3 / final** (`20261011T154501Z`): outcome
  **pass**; 16 claims assessed, 0 failure modes, 0 claims
  below the 0.70 threshold; AEE exit code 0. The final
  artifacts are also copied as `assess-specify.json` and
  `evaluator-specify.json`.
- **Plan and tasks phases** (`20261011T154507Z`): both
  **pass** on the same register (16 claims, 0 failure
  modes, 0 below threshold); artifacts saved in this
  directory.

## Evaluator residual

`speckit.evaluator.run` has no registered evaluators in
this repository (no `evaluators.yml`). Its standalone
honest result is therefore a pass noting that none are
configured. The operative evaluator-contract results saved
here are the results produced by AEE assess through its
evaluator adapter. That residual is recorded, not papered
over.
