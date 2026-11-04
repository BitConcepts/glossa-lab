# T002 — AEE verification of the C088 bundle (2026-11-04)

The bundle was assessed with the same assessor, the same way, as Spec
087's T002: the pinned AEE in the CI-faithful venv (`glossa-ci`, aee
1.5.3), run from the package directory.

Commands (verbatim):

```
~/workspace/venvs/glossa-ci/bin/aee validate aee-claims.json
~/workspace/venvs/glossa-ci/bin/aee assess --no-ledger --input aee-claims.json --output records/t002-aee-assessment.json
```

Validate printed `valid: 19 claim(s) in aee-claims.json` and exited 0.
Assess exited 1 (its outcome is not `pass`; the Spec 087 T002 assessment
exited the same way) and wrote `records/t002-aee-assessment.json`.

Verbatim outcome of record:

- **Outcome: iterate**
- Summary: "Assessed 19 claim(s); found 80 failure mode(s); 19 claim(s)
  below the 0.70 confidence threshold. Shared evidence: 1 supporting
  source(s) shared across 19 of 19 claim(s); the same evidence set
  supports multiple claims (FR-2.8, reporting only, no outcome effect in
  this phase). Draft cap: 19 draft claim(s) capped at
  gather_evidence/iterate (FR-2.3). Stage cap: 19 claim(s) below stage
  'explained'; the outcome cannot be 'pass' (Spec 004 R1.4). Not
  understood: 38 residual unknown(s) are recorded on this assessment
  (Spec 004 R5.2). Lane 1 (machine verification): outcome iterate; 0
  claim(s) at or above the 0.70 threshold, 19 below. Lane 2 (human
  acceptance): stages by effective stage: created 19. Lane-2 lag: 19
  claim(s) below explained."

Reading (the Spec 086/087 discipline): `iterate` is the expected outcome
for a draft bundle whose evidence is a single asserted package source —
the draft cap and stage cap bind by construction. T002's acceptance
criterion is that the claims were actually run through the assessor and
the outcome recorded, which is what happened; the owner's block approval
of the package (T003) is the human act that carries the claims forward.
