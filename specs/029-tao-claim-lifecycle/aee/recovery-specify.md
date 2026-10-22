# AEE recovery record — Spec 029 lifecycle task L3 (2026-10-12)

Governing rule (Spec 026): an AEE outcome stricter than
`warn` blocks closure until the recovery work named by
the assessment is completed and recorded. The assessment
is a governance signal, not a probability that a claim
is true.

## Rounds

- **Round 1** (`20261012T133440Z` specify /
  `20261012T133515Z` plan / `20261012T133518Z` tasks):
  outcome `iterate` at all three phases; 10 claims
  assessed, 32 failure modes, 10 claims below the 0.70
  threshold, AEE exit code 1. Failure classes:
  irreducibility challenges on all 10 compound claim
  texts and negation-conflict challenges on 22 claim
  pairs. Root cause, checked against the Spec 028
  register: the Spec 029 register carried no `evidence`
  field on any claim (0/10) and no `boundary_confirmation`
  metadata on any claim (0/10), so every claim sat at
  the no-evidence confidence floor (0.25). Full record:
  `aee/l3-outcome.md`.
- **Recovery 1** (owner-authorized 2026-10-12,
  "Authorize the L3 recovery PR and resume
  implementation"):
  1. An `evidence` list was added to every claim, in
     the Spec 028 register shape — observed-kind,
     artifact/primary-quality references into this
     spec's own record set (spec.md sections,
     assessment.md findings, audit.md sections,
     adjudication.md), each ref resolving to a real
     section that supports the claim it is attached to.
  2. Pairwise `boundary_confirmation` metadata was
     added for every flagged pair, stating the distinct
     boundary each member governs.
  3. Compound claim texts were rewritten as single
     positive propositions. Enumerations and the
     prohibitory apparatus remain carried by each
     claim's boundary, verdict rule, falsification
     tests, and metadata — unchanged except where a
     split moved them (below).
  4. Three claims were honestly split, following the
     Spec 028 precedent (its compliance claim split
     grew that register 15 → 16):
     - `F029-C11` (parent-stage minimum rule) split
       from `F029-C03` (bundle composition). C03's
       second falsification test, its minimum-rule
       verdict text, and the `ASM-PARENT-AVERAGES-CHILDREN`
       forbidden assumption moved to C11. C03 records
       its four sub-claim kinds in metadata.
     - `F029-C12` (digested gate) split from
       `F029-C04` (accepted gate). C04's second
       falsification test and the `ASM-TIME-IS-DIGESTION`
       forbidden assumption moved to C12.
     - `F029-C13` (remaining-unknowns display rule)
       split from `F029-C06` (score placement). C06's
       second falsification test moved to C13.
     `F029-C05` gained a dependency on `F029-C11`
     because its cap rule invokes the minimum rule.
     No claim's boundary was changed; no verdict rule
     changed in substance — split rules moved verbatim
     to the successor claim named above.
  5. Register integrity re-verified with
     `glossa_lab.framework026.check_dependency_integrity`:
     no cycles, no missing dependencies, no forbidden
     inheritance (`ok: true`).
- **Round 2 / final** (`20261012T134637Z` specify /
  `20261012T134651Z` plan / `20261012T134652Z` tasks):
  outcome **pass** at all three phases; 13 claims
  assessed, 0 failure modes, 0 claims below the 0.70
  threshold; AEE exit code 0. The final artifacts are
  saved in this directory; the after_specify pair is
  also copied as `assess-specify.json` and
  `evaluator-specify.json` (house convention).

## Tooling (identical for all runs)

`run_aee.py assess --input
specs/029-tao-claim-lifecycle/claims.json --phase
<phase> --threshold 0.70 --project glossa-lab-spec029`,
run non-interactively from the repo root with the
Glossa venv first on PATH, so the `aee` executable
resolved to AEE package **1.0.4** (spec-kit venv's
1.0.2 not used). specify CLI 1.0.10; AEE extension
v1.1.0; evaluator extension v1.0.0.

## Evaluator residual

`speckit.evaluator.run` has no registered evaluators in
this repository (no `evaluators.yml`). The operative
evaluator-contract results saved here are the results
produced by AEE assess through its evaluator adapter.
That residual is recorded, not papered over.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## Addendum — freeze-time uniformity fix (2026-10-12)

After the recovery PR merged (PR #167), the freeze
tests required `boundary_confirmation` on *every*
claim; the three split claims (F029-C11/C12/C13) had
carried their pair confirmations only on their parent
claims. Each split claim gained its own confirmation
stating its boundary against its parent claim. The
metadata field is inert to the assessor (it appears
nowhere in the AEE package), and the pass was
re-confirmed on the final register bytes at all three
phases (`20261012T140048Z` / `20261012T140049Z` /
`20261012T140051Z`): outcome **pass**, 13 claims,
0 failure modes, 0 below threshold. Those artifacts
are saved alongside the recovery-round artifacts in
this directory.
