# T002 — AEE verification of the C091 bundle (2026-11-05)

The bundle was assessed with the same assessor, the same way, as Spec
088/089's T002: the pinned AEE in the CI-faithful venv (`glossa-ci`, aee
1.5.3), run from the package directory.

Commands (verbatim):

```
~/workspace/venvs/glossa-ci/bin/aee validate aee-claims.json
~/workspace/venvs/glossa-ci/bin/aee assess --no-ledger --input aee-claims.json --output records/t002-aee-assessment.json
```

Validate printed `valid: 15 claim(s) in aee-claims.json` and exited 0.
Assess exited 1 (its outcome is not `pass`; the Spec 088/089 T002
assessments exited the same way) and wrote
`records/t002-aee-assessment.json`.

Bundle generation: `aee-claims.json` was generated from `claims.md` by
script (the claim statement as `text`, the falsifier as the single
falsification test, one asserted package evidence entry per claim — the
Spec 088/089 normalization, with the "does not establish" lines carried
in claims.md as the normative text). Set identity for this bundle
verified mechanically at drafting: the 15 ids in `aee-claims.json`
equal the 15 ids in `claims.md`, in order; every claim carries exactly
one falsifier.

Verbatim outcome of record:

- **Outcome: iterate**
- Summary: "Assessed 15 claim(s); found 66 failure mode(s); 15 claim(s)
  below the 0.70 confidence threshold. Shared evidence: 1 supporting
  source(s) shared across 15 of 15 claim(s); the same evidence set
  supports multiple claims (FR-2.8, reporting only, no outcome effect
  in this phase). Draft cap: 15 draft claim(s) capped at
  gather_evidence/iterate (FR-2.3). Stage cap: 15 claim(s) below stage
  'explained'; the outcome cannot be 'pass' (Spec 004 R1.4). Not
  understood: 30 residual unknown(s) are recorded on this assessment
  (Spec 004 R5.2). Lane 1 (machine verification): outcome iterate; 0
  claim(s) at or above the 0.70 threshold, 15 below. Lane 2 (human
  acceptance): stages by effective stage: created 15. Lane-2 lag: 15
  claim(s) below explained."

`iterate` is the expected outcome for a draft bundle on a single
asserted source; the owner's approval (T003) is the human act.
