# Spec 076 — Freeze record

**FROZEN — 2026-10-26.** This directory is the
frozen contract for Spec 076: `spec.md` (the M12
design carried into frozen form, with the
freeze-fixed completions at its §0), `claims.json`
(the claims register, drafted directly in the
recovered 0.7 form, 10 claims F076-C01…F076-C10),
`adjudication.md` (the drafting record, with the
freeze rulings DD-076-1…DD-076-7), this record,
the AEE hook artifacts under `aee/`, and the
strengthened-gate records under `gate-records/`.

The freeze is executed under the owner's order of
2026-10-26 ("Freeze and run the M12 pilot",
06:51 EDT). **Phase allocated: Phase 442**
(DD-076-1). This freeze is a **required-C4
freeze** (DD-076-7): the C4 records check is a
required branch-protection check since the act of
2026-10-25 that followed the Spec 075 shadow
freeze, and the gate records below must pass it
in CI on the freeze PR. **No OSF registration is
filed at this freeze** (DD-076-5): the M12
design's filing provisions name none, so the repo
freeze record governs and the absence is recorded
here rather than improvised around. Execution —
the §8 pilot — is a separate act under the same
owner order: it begins when this freeze record is
complete (this PR merged on genuine CI including
the required C4 check), runs once as frozen
(FF-5), and is recorded in `pilot-record.md` in
this directory.

## 1. What was frozen

- **The question** (spec §1): what the attested
  corpus, treated as a constraint system, demands
  of any completion — bounded possibility sets,
  forced exclusions, forced co-variations for the
  signs we do not have — derived by exact census
  deduction, never by scoring a reading.
- **The honesty architecture** (spec §3):
  necessities conditional on a stated assumption
  set (A-FRAME / A-DIR / A-FACE / A-KEY, filed as
  claims F076-C04…C07); three tiers (C census /
  S structural / T tendencies) never blended; the
  nine-type positional vocabulary of §3.4, under
  which the register records set membership, never
  identity.
- **The pilot** (spec §8): step 0 reproduction
  gate (any mismatch closes CANNOT BE RUN AS
  WRITTEN); step 1 derivation against the pre-named
  headline numbers (677 / 178 / 13); step 2 the
  marginals-preserving shuffle null (B = 999, seed
  20261026; label permutation named invalid in
  advance) at the frozen bars — the U2 finals
  residual 178 below the null's 5th percentile, the
  solo-only count 13 above its 95th; step 3 the
  blind positive control over the 94 strict signs
  under coding rules CR-1…CR-7, closing ASSUMPTION
  SET DOES NOT HOLD above 5 exclusions.
- **The completions the design left to the
  freeze** (spec §0, DD-076-3): FF-1 the seed;
  FF-2 the coding rules; FF-3 the resolution-value
  operationalisation; FF-4 the A-KEY clarification
  (the 13 duplicated Mahadevan ids live on the
  registry's cross-scheme join surface; the pilot
  frame performs no such join, so no frame row is
  excluded and attested members are flagged);
  FF-5 the pilot execution order. No bar, frame,
  null, or closure word of the design was moved
  (adjudication §4).

## 2. The inputs (spec §5, §7)

The corpus export (`glossa-corpus/indus/exports/indus_research.jsonl`,
SHA-256 08fc96c8…; 2,906 indusscript-m77 records;
frame census 11,507 tokens, 5,883 strict tokens,
slot totals 2,655 / 2,655 / 225 / 5,972, finals
partition 1,707 / 250 / 520 / 178); the anchors
file (`backend/reports/INDUS_FINAL_ANCHORS.json`,
SHA-256 df0cf620…; 287 entries, 94 strict, 44
pending); Registry v2
(`data/crosswalks/canonical_sign_registry_v2.csv`,
SHA-256 42ab09fb…, 1,013 rows) for the A-KEY
accounting. All three files are in git; none is
restricted.

## 3. Verification at the freeze

Every pin above was recomputed first-hand by the
freeze worker from the files as fetched from repo
main and agrees. The §7 census was re-derived
from those files and reproduces every pre-named
figure exactly — the third independent route to
the same numbers (Spec 033's pipeline census; the
design draft's recomputation; this freeze's). No
pilot quantity was computed at drafting or at the
freeze: the only computations performed are the
census reproductions the design itself prints in
§7 and the gate's C2 recomputation of the same
figures. The §8 null was not run, in any form,
before the freeze.

## 4. AEE gate

The hooks ran before the digest was computed,
with the pinned evaluator (aee 1.5.3) in the
freeze configuration, at all three hooks
(after_specify, after_plan, after_tasks). Each
artifact carries **19 findings: the 10 FR-2.3
draft caps (one per claim), 8 irreducibility
challenges (F076-C01, C03, C04, C06, C07, C08,
C09, C10) and 1 counterexample challenge
(F076-C09); zero findings of contradiction,
independence, ambiguity, or evidence-resolution
kind; no claim below the 0.70 threshold (minimum
propagated confidence 0.7200)**. The challenges
are answered in `aee/freeze-aee-note.md` from the
spec's own structure — the assumption set is
itself the decomposition, filed as four separate
claims (C04…C07), and C09's universality is its
content — and ruled at DD-076-3; the register was
not reworded to silence them.

## 5. The strengthened gate (full run, required C4)

- **C1 — kill-test battery** (evaluator aee 1.5.3,
  the pinned version; run 2026-10-26 for this
  freeze; record `gate-records/c1-battery-result.json`).
  The evaluator flags **none** of the four cases —
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
  all 11 gate-turning quantities and — beyond the
  scaffold's sampled 3 — every one of the 5
  remaining quantities: **16 of 16 agree**,
  including the three input digests, the 11,507 /
  5,883 token censuses, the slot totals, the
  finals partition summing to 2,655, the 677
  exclusions with their size distribution, the
  solo-only set of 13, and the 24 absent signs.
- **C3 — evidence sample, verification on**
  (record `gate-records/c3-evidence-sample.json`,
  outcome PASS). Sample: the 3 verdict-bearing
  claims (F076-C01, C02, C08) plus the scaffold's
  sample of the remainder (F076-C03, C04) — 5 of
  10. The verifier read every cited text against
  its claim: **all 5 sampled claims verified; no
  verdict-bearing claim unverified**.
- **C4 — mechanical check.** The gate-records set
  above is what the C4 CI job reads; it passed on
  this directory before the PR was assembled
  (checker run at the freeze act) and must pass
  in CI on the freeze PR, where it is a required
  branch-protection check.
- **C5 — gate statistics** (regenerated at this
  freeze; `docs/freeze-gate/gate-statistics.md`
  in the freeze PR): freezes carrying gate
  records so far: **2** (075, this one); freezes
  blocked by C2: **0**; blocked by C3: **0**; C2
  mismatches recorded: **0**; C3 unverified
  sampled claims: **0**.

## 6. The S4 note (recorded at this freeze, per the 2026-10-26 scan)

The indirect-methods scan adopted S4 as a
governing-rule extension: because a deterministic
generator of seal-like inscriptions for a fictional
non-language passes published statistical language
diagnostics, permutation nulls are necessary but
not sufficient for score-based methods. This
pilot is not a score-based language diagnostic:
its two statistics are census-concentration
measures (where the unread signs' final slots and
the solo-only signs sit, counted exactly) tested
against a marginals-preserving shuffle, and its
calibration is an independent blind positive
control over the strict core — not a comparison
against a language-likeness score. S4 therefore
adds no generator arm to this pilot; the boundary
is recorded in spec §14 so that any future use of
the register that leans on a statistic of
language-likeness takes S4 with it at that time.

## 7. Freeze digest

The freeze digest is computed by `build_freeze.py`
(framework026) over seven sources — this record,
`spec.md`, `claims.json`, `adjudication.md`,
`aee/freeze-aee-note.md`, `build_freeze.py`, and
`backend/tests/test_spec076_freeze.py` — and is
recorded in `freeze.json` in this directory and
quoted in the freeze pull request. It was computed
after the AEE gate and the gate records were
filed, over the final texts. The freeze tests
(`backend/tests/test_spec076_freeze.py`) replay
the digest, assert the definition's constants,
the register's integrity, the hook artifacts'
pass shape, and the input pins of §2 by
recomputation.

## 8. Able-to-fail proof

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

## 9. What this freeze establishes / does not establish

This freeze establishes that the
projected-constraint question is well-posed
against its pinned frame: its census reproduces
by three independent routes, its assumption set
is filed as claims with falsifiers, its bars were
committed by the design before any run and are
frozen here unmoved, its null is the valid one
(the invalid one named in advance), and its
calibration control can fail. It does not
establish that the pilot passes, that any register
entry holds, or anything about what any sign
means: **no register exists yet**, no null has
been run, and no claimed type has been coded. It
moves no anchor, reading, PRED-2026 state,
verdict, status, or frozen text anywhere in the
programme, touches neither M4's gate nor M7's
attack, and leaves the standing position
unchanged: the script is not deciphered.
