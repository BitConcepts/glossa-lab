# Spec 077 — Freeze record

**FROZEN — 2026-10-26.** This directory is the
frozen contract for Spec 077: `spec.md` (the M7
design carried into frozen form, with the
freeze-fixed completions at its §0), `claims.json`
(the claims register, drafted directly in the
recovered 0.7 form, 10 claims F077-C01…F077-C10),
`adjudication.md` (the drafting record, with the
freeze rulings DD-077-1…DD-077-9), this record,
the AEE hook artifacts under `aee/`, and the
strengthened-gate records under `gate-records/`.

The freeze is executed under the owner's order of
2026-10-26 ("do all now" — M7 freeze-and-execute
from the what's-next board). **Phase allocated:
Phase 443** (DD-077-1). This freeze is a
**required-C4 freeze** (DD-077-9): the C4 records
check is a required branch-protection check since
2026-10-25, and the gate records below must pass
it in CI on the freeze PR. **No OSF registration
is filed at this freeze** (DD-077-5): the M7
design's filing provisions name none, so the repo
freeze record governs and the absence is recorded
here rather than improvised around. Execution is
a separate act under the same owner order: it
begins when this freeze record is complete (this
PR merged on genuine CI including the required C4
check), runs once as frozen, and is recorded in
`step0-record.md` and `outcome.md` in this
directory, with the machine record at
`reports/phase443_results.json`.

## 1. What was frozen

- **The question** (spec §1): whether the
  program's signary — the 557-sign population
  frame behind Rung 1 — is witnessed by sign lists
  that did not come from the program (Mahadevan
  1977; Wells 1998), mapped against Registry v2,
  with a named attack on token 999, the one
  population sign with no published identity.
- **The claims** (spec §2): F077-C01, at least
  90% of the 557 witnessed — the bar in counts is
  at least 502 of 557, and the falsifier applies
  to the ancestry-adjusted share when it is lower;
  F077-C02, token 999's identity settled by the
  two-condition rule or standing NO PUBLISHED
  IDENTITY. Eight further claims carry the step-0
  pin verification, the population reproduction,
  the ancestry map, the 13-id resolution, the two
  sensitivities, the gap-list deliverable, and the
  Table I input condition.
- **The completions the design left to the
  freeze** (spec §0): FF-1 numbering; FF-2 the
  witness set (the counted Wells witness is the
  extracted 1998 list; Wells 2006 is held in plate
  form only and is not counted; the Wells/ICIT
  2015 surface is not a witness, being the
  population's own keying frame); FF-3 the match
  rules operationalized; FF-4 the 13 duplicated
  Mahadevan ids resolved per (sign, id) on the
  record before counting, unresolved counting as
  not witnessed; FF-5 the ancestry adjustment in
  its root-list reading, both shares reported;
  FF-6 token 999's reference behavior (2
  occurrences, 0 text-final, rate 0.0) and the
  absolute-count administration of C02 (witness
  total exactly 2; final count 0 at that total);
  FF-7 Table I pinned by its acceptance form, the
  landed file's hash recorded at step 0; FF-8
  sensitivity S2's administration (its exclusion
  set is empty under the frozen witness
  definitions, stated openly with the per-witness
  breakdown reported in full). No bar, threshold,
  or closure word of the design was moved.

## 2. The inputs (spec §3)

Registry v2 (`data/crosswalks/canonical_sign_registry_v2.csv`,
SHA-256 42ab09fb…; 1,013 rows = 396 parpola_1982
+ 407 yajnadevam_glyphid + 210 icit_wells); Spec
075's machine record (`reports/phase441_results.json`,
SHA-256 f55ae911…; census 3,045 / 557 / 550;
token 999 at 2 primary rows / 2 occurrences); the
M77 sign list, dataset v3
(`glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list.csv`,
SHA-256 9c619bfe…; 417 rows, 179 dagger-flagged /
238 not / 0 uncertain — the printed §11.4 total
exactly), extracted from the held volume (SHA-256
ef68fe8d…e110) under the trigger-census
instrument's single pass; the Wells 1998 sign list
(`glossa-corpus/indus/sources/wells-1998/wells1998_sign_list.csv`,
SHA-256 22bde128…; 588 rows, 587 printed entries
+ sign 407 NOT PRINTED), from the held thesis
(SHA-256 5720dc01…), with its Figure 3.6
cross-references (SHA-256 b0ef40da…; 55 pairings
over 17 distinct Mahadevan targets); the C-7
canonical M77 raw text (`data/mahadevan_m77_raw.txt`,
SHA-256 11441e38…); Table I pinned by acceptance
form (FF-7). The witness datasets and the thesis
live in the canonical store and the restricted
local holdings; they are cited by hash and never
enter git. The restricted-local derivation inputs
for the population reproduction (corpus
345241b1…; row grades 02394241…) are likewise
cited by hash only.

## 3. Verification at the freeze

Every pin above was recomputed first-hand by the
freeze worker from the files as fetched from repo
main or as held in the canonical store, and
agrees. The population census and token 999's
reference behavior were re-derived under Spec
075's frozen construction from its hash-verified
restricted-local inputs and reproduce the frozen
figures exactly (3,045 analyzable rows / 557
distinct signs / 550 in sequences of length ≥ 2;
999 at 2 occurrences, 0 text-final — both of its
sequences read 034-999-034). The witness tables'
actual columns were read, not their descriptions
(the draft amendment's binding rule). No witness
counting was performed at drafting or at the
freeze: the only computations are the step-0
reproductions the frozen spec itself names and
the gate's C2 recomputation of the same pinned
quantities. The counting, the gap list, and the
999 attack run once, after this freeze merges,
under §8 of the spec.

## 4. AEE gate

The hooks ran before the digest was computed,
with the pinned evaluator (aee 1.5.3) in the
freeze configuration, at all three hooks
(after_specify, after_plan, after_tasks). Each
artifact carries **21 findings: the 10 FR-2.3
draft caps (one per claim), 10 irreducibility
challenges (one per claim), and 1
negation-conflict challenge (F077-C01 against
F077-C03); zero findings of independence,
ambiguity, or evidence-resolution kind; no claim
below the 0.70 threshold (minimum propagated
confidence 0.7200)**. The challenges are answered
in `aee/freeze-aee-note.md` from the spec's own
structure — the register's two verdict-bearing
claims carry the design's claims and every other
condition is filed as its own claim so it can
fail on its own; C01 and C03 are a claim and its
gate, not a contradiction — and ruled at
DD-077-3; the register was not reworded to
silence them.

## 5. The strengthened gate (full run, required C4)

- **C1 — kill-test battery** (evaluator aee
  1.5.3, the pinned version; run 2026-10-26 for
  this freeze; record
  `gate-records/c1-battery-result.json`). The
  evaluator flags **none** of the four cases —
  the same determinations as the canonical battery
  output on main, against which the C4 check
  matches this record. The blind spots, named in
  plain words as filed:
  - Case (i), the real Spec 026-era design
    (non-discriminating instrument): "The
    evaluator cannot be run against this case in
    its current form, so the gate has no reading
    on this defect class at all. Reason recorded:
    Error: input bundle contains zero claims: an
    empty bundle is an input error, never a pass
    (Spec 003 FR-1.1)" — the evaluator extracts
    zero claims from the prose design and cannot
    run.
  - Case (ii), planted unfalsifiable headline
    claim: "The evaluator does not detect a
    falsifier that is present in form and empty in
    substance: the planted headline claim FB2-C01
    passes with no correctness finding naming its
    untestable test."
  - Case (iii), planted wrong pin (52 against a
    source summing to 47): "The evaluator does not
    recompute pinned quantities against their
    cited sources: a total of 52 pinned against a
    source summing to 47 passes without a
    correctness finding. C2 (independent
    recomputation) is the component that carries
    this class."
  - Case (iv), planted unsupported citations:
    "The evaluator verifies that citations
    resolve, not that they support: claims stating
    the opposite of their cited records pass in
    both the freeze configuration and with evidence
    verification on. C3's verification step — a
    verifier reading the cited text against the
    claim — is the component that carries this
    class."
- **C2 — independent spot-check** (record
  `gate-records/c2-spotcheck.json`, outcome PASS).
  A worker who did not draft the spec recomputed,
  from the spec text and the pinned inputs only,
  all 14 gate-turning quantities and the
  scaffold's sampled 3 of the remaining 10:
  **17 of 17 sampled quantities agree**,
  including the registry and machine-record
  digests, the population census (3,045 / 557 /
  550), token 999's occurrences and finals (2 /
  0), the 502-of-557 bar, both witness dataset
  digests, the 13 duplicated ids recomputed from
  the registry, the Figure 3.6 expansion (55
  pairings over 17 targets), and the Table I
  printed totals row as recorded in the
  extraction workpapers.
- **C3 — evidence sample, verification on**
  (record `gate-records/c3-evidence-sample.json`,
  outcome PASS). Sample: the 2 verdict-bearing
  claims (F077-C01, F077-C02) plus the scaffold's
  sample of the remainder (F077-C04, F077-C09) —
  4 of 10. The verifier read every cited text
  against its claim: **all 4 sampled claims
  verified; no verdict-bearing claim
  unverified**.
- **C4 — mechanical check.** The gate-records set
  above is what the C4 CI job reads; it passed on
  this directory before the PR was assembled
  (checker run at the freeze act) and must pass
  in CI on the freeze PR, where it is a required
  branch-protection check.
- **C5 — gate statistics** (regenerated at this
  freeze; `docs/freeze-gate/gate-statistics.md`
  in the freeze PR): freezes carrying gate
  records so far: **3** (075, 076, this one);
  freezes blocked by C2: **0**; blocked by C3:
  **0**; C2 mismatches recorded: **0**; C3
  unverified sampled claims: **0**.

## 6. Freeze digest

The freeze digest is computed by `build_freeze.py`
(framework026) over seven sources — this record,
`spec.md`, `claims.json`, `adjudication.md`,
`aee/freeze-aee-note.md`, `build_freeze.py`, and
`backend/tests/test_spec077_freeze.py` — and is
recorded in `freeze.json` in this directory and
quoted in the freeze pull request. It was computed
after the AEE gate and the gate records were
filed, over the final texts. The freeze tests
(`backend/tests/test_spec077_freeze.py`) replay
the digest, assert the definition's constants,
the register's integrity, the hook artifacts'
pass shape, and the input pins of §2 by
recomputation — including the 13 duplicated
Mahadevan ids recomputed from the pinned registry
and Spec 075's census as printed in its machine
record.

## 7. Able-to-fail proof

With the assembled freeze in place, the register's
`register_version` was mutated in exactly one
place (0.7-draft → 0.7-draft-MUTATED) in a scratch
copy of the tree and the freeze tests were run:
they failed (the replay and the register
integrity assertions). The register was then
restored byte-identical — its SHA-256 re-verified
against the frozen value — and the tests passed.
The freeze is therefore falsifiable by its own
tests: a silent change to a frozen source breaks
the replay rather than passing unnoticed.

## 8. What this freeze establishes / does not establish

This freeze establishes that the M7 question is
well-posed against its pinned inputs: the witness
lists exist as checksum-exact extractions, the
population frame and token 999's reference
behavior reproduce exactly under the prior spec's
frozen construction, the match rules and the
ancestry adjustment are fixed in advance in their
conservative readings, and the one input that had
not landed (Table I) is pinned by an exact
acceptance form with a step-0 closure instead of
a substitute. It does not establish any part of
the answer: no witnessing share has been counted,
no gap list exists yet, and token 999 stands
exactly where Spec 073 left it — NO PUBLISHED
IDENTITY — until the execution runs. Nothing in
this freeze is a claim about what any sign means,
and the script is not deciphered.
