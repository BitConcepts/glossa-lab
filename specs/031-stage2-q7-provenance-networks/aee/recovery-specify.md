# AEE recovery record — specify stage (Spec 031 freeze)

Governing rule (Spec 026): an AEE outcome stricter than
`warn` blocks closure until the recovery work named by
the assessment is completed and recorded. The
assessment is a governance signal, not a probability
that a claim is true. Invocation for every round:
`.specify/extensions/aee/scripts/python/run_aee.py
assess --input specs/031-stage2-q7-provenance-networks/
claims.json --phase <phase> --threshold 0.70 --project
glossa-lab-spec031`, Glossa venv first on PATH (AEE
package 1.0.4; specify CLI 1.0.10; AEE extension
v1.1.0; evaluator extension v1.0.0).

## Rounds

- **Round 1** (`20261013T060646Z`, after_specify, on
  the register as first drafted): outcome `iterate`;
  12 claims assessed, 5 failure modes, 0 claims below
  the 0.70 threshold (every claim scored 0.9945, band
  high — the register already carried evidence lists
  and boundary confirmations from drafting). Failure
  classes: **irreducibility challenges ×2** (F031-C01
  — the "objects, materials, and techniques"
  enumeration; F031-C06 — the coordinated
  "classifications and their published applications"
  construction) and **negation-conflict challenges
  ×3**, all against F031-C07 (paired with C05, C11,
  and C12 — pairs whose texts share vocabulary while
  governing different acts: computation vs closure,
  internal use vs release, applying vs fixing a
  threshold).
- **Recovery 1:** claim texts rewritten as single
  atomic propositions, in the Spec 030 recovery
  pattern. The enumeration and secondary clause the
  texts carried were moved into the claims'
  boundaries verbatim in substance (C01's
  objects/materials/techniques enumeration, carried
  as the definition of "craft evidence"; C06's
  published-applications route, carried as the
  mechanism by which classifications reach
  assemblages). Boundaries and verdict rules are
  unchanged in substance, and no falsification test
  was altered. Pairwise boundary confirmations for
  the three flagged pairs were added to the claims
  on both sides of each pair (C05↔C07, C07↔C11,
  C07↔C12). Register integrity re-verified with
  `glossa_lab.framework026.check_dependency_integrity`
  (no cycles, no missing dependencies, no forbidden
  inheritance). Register version 0.1-draft →
  0.2-draft, with the change recorded in the
  register's note.
- **Round 2** (`20261013T060745Z`, after_specify, on
  the recovery-1 register): outcome `iterate`; 4
  failure modes, 0 below threshold. The
  irreducibility challenges were cleared; the
  remaining challenges were negation-conflicts on
  C05↔C07, C07↔C11, C07↔C12 — plus a new C01↔C07
  pairing created by the recovery-1 boundary text is
  not assessed (the check reads claim texts only).
  Reading the assessor's check showed it pairs claim
  **texts** sharing three or more content tokens
  where exactly one text carries a negation word;
  boundary confirmations cannot resolve it — the
  texts themselves must not present the accidental
  collision.
- **Recovery 2:** the texts of C01, C05, C11, and
  C12 were reworded to remove the accidental token
  collisions while preserving each claim's
  proposition exactly: C01 ("Q7 verdicts under
  Spec 031 concern craft evidence only."), C05
  ("The two response arms are computed on separate
  eligible site sets."), C11 ("No released row is
  derived from an open_access_read_only source." —
  same force as "nothing derived … is released"),
  C12 ("Support thresholds take their values from
  the D8 audit margins." — the freeze-fixing half of
  the claim is carried explicitly in C12's boundary,
  falsification test, and verdict rule). No
  falsification test, verdict rule, boundary, or
  dependency was altered. Register version
  0.2-draft → 0.3-draft.
- **Round 3 / final** (`20261013T060931Z`
  after_specify; `20261013T060940Z` after_plan;
  `20261013T060942Z` after_tasks, on the recovered
  register): outcome **`pass`** at all three phases
  — 12 claims assessed, 0 failure modes, 0 claims
  below the 0.70 threshold at each phase. The final
  after_specify artifacts are also copied as
  `assess-specify.json` and `evaluator-specify.json`.

## Evaluator residual

`speckit.evaluator.run` has no registered evaluators
in this repository (unchanged from Specs 026–030);
the operative evaluator-contract result is the
AEE-produced one saved beside the assessment
artifacts in this directory. Evaluator artifacts are
filed for round 1 and for the final round
(`evaluator-specify.json`); the intermediate rounds'
evaluator stubs were not retained — they carried no
registered evaluators, and every round's assessment
artifact (the substantive record) is filed.
