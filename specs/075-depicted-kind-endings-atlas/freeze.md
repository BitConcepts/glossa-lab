# Spec 075 — Freeze record

**FROZEN — 2026-10-25.** This directory is the
frozen contract for Spec 075: `spec.md` (the
design), `claims.json` (the claims register,
drafted directly in the recovered 0.7 form, 13
claims F075-C01…F075-C13), `adjudication.md` (the
drafting record, with the freeze rulings at §8),
this record, the AEE hook artifacts under `aee/`,
and the strengthened-gate records under
`gate-records/`.

The freeze is executed under the owner's order of
2026-10-25 ("do the atlas freeze", 11:59 EDT).
**Phase allocated: Phase 441** (DD-075-2). This
freeze is the designated **C4 shadow freeze**
(DD-075-7; gate build decision of 2026-10-25):
the strengthened gate runs in full and is
reported in §5; the C4 CI job runs on the freeze
PR and must pass on the complete record set, but
it is not yet a required branch-protection check
— that begins with the freeze after this one. An
OSF registration is filed for this freeze at the
freeze act; its record is
`osf-spec-registration.md` in this directory
(registration id and DOI only). Execution is a
separate act: under the owner's order of
2026-10-25 (12:03 EDT) it begins when this freeze
record is complete — this PR merged on genuine
CI including the C4 job, the OSF registration
approved and verified — under the frozen step-0
gates, fail-closed. It has not run at the freeze.

## 1. What was frozen

- **The question** (spec §1.1): for each kind of
  thing the published sign identifications
  depict, do that kind's signs gather at the
  ends of inscriptions — asked per kind, in
  this spec's own claim family. It is not Spec
  071's retired question and not Hunt's claims
  in any form; Spec 071's claim stands
  UNTESTED under its 2026-10-25 retirement,
  untouched by this freeze.
- **The classes** (spec §4): Asset A v2's
  depicted kinds over Registry v2 — other,
  human, animal, object_goods tested; the
  celestial class pre-registered EMPTY (0
  signs), reported first and never tested;
  unidentified signs in no class and no
  comparison class (design R8); token 999 the
  named exclusion.
- **The test** (spec §5): per kind, the pooled
  final-position rate against the
  frequency-matched comparison class (the other
  identified kinds), Fisher's exact (two-sided)
  at 5%, with per-sign tables published in
  full; verdict bands frozen (SUPPORTED ≥ 1.5
  + significance + the half-of-occurrences
  condition; NOT SUPPORTED ≤ 1.0, the
  falsifier's word stated in advance;
  INCONCLUSIVE between; TOO THIN below the
  floors of 20 signs / 30 occurrences). Four
  verdicts; no pooled verdict exists.
- **The gates** (spec §6): step 0, gates
  0.1–0.6, fail-closed, the census published
  before any rate — with the pre-verification
  flag stated in the spec: gate 0.4's
  population reproduction is a replay/drift
  gate over quantities verified at this
  freeze; no census and no final-position
  quantity was computed before an execution.

## 2. The inputs (spec §3)

Asset A v2 (SHA-256 681e017d…, 552 rows; kinds
other 246 / unidentified 211 / human 43 /
animal 30 / object_goods 22 / sky_cycle 0;
dispute_status none 548 / borderline 4 /
contested 0) and Registry v2 (SHA-256
42ab09fb…, 1,013 rows), as frozen by Spec
073's executed record; the Shakti corpus
(SHA-256 345241b1…, 5,704 rows) and its
row-grades file (SHA-256 02394241…; grades
3,212 / 2,087 / 405) under the 2026-10-22
intake record, restricted-local and never in
git; Registry v1 (8a0b2a82…, 803 rows), the
sign crosswalk of record
(`data/crosswalks/sign_crosswalk_master.csv`,
4ace1a61…, 205 rows), and the anchors file
(df0cf620…) as gate-0.3 integrity pins.

## 3. Verification at the freeze

Every pin above was recomputed first-hand by
the drafting worker from the files on the
freeze base (main 379a9fc3) and agrees
(adjudication §2). The primary population,
enumerated under spec §3's construction,
reproduces **3,045 analyzable rows / 557
distinct signs / 550 in sequences of length
≥ 2** exactly; the corroborated population
reproduces 5,131 analyzable rows; token 999
stands in 2 primary rows with 2 occurrences.
The keying surface fact the two-leg route
rests on is unchanged from Spec 074's record:
the combined Wells map over Registry v2
carries 708 distinct ids with zero resolving
to more than one sign (recomputed in the
freeze tests). No class census on the
population and no final-position quantity was
computed at drafting or at the freeze.

## 4. AEE gate

The hooks ran before the digest was computed,
with the pinned evaluator (aee 1.5.3) in the
freeze configuration, at all three hooks
(after_specify, after_plan, after_tasks). Each
artifact carries **22 findings: the 13 FR-2.3
draft caps (one per claim), 7 irreducibility
challenges (F075-C06, C07, C08, C09, C10, C12,
C13) and 2 counterexample challenges (F075-C09,
C12); zero findings of contradiction,
independence, ambiguity, or
evidence-resolution kind; no claim below the
0.70 threshold (minimum propagated confidence
0.8695)**. The challenges are a recorded
difference from Spec 074's register (draft
caps only); they are answered in
`aee/freeze-aee-note.md` from the spec's own
gate structure and ruled at DD-075-6 — the
register was not reworded to silence them.

## 5. The strengthened gate (shadow run)

- **C1 — kill-test battery** (evaluator aee
  1.5.3, the pinned version; run 2026-10-25 for
  this freeze; record
  `gate-records/c1-battery-result.json`). The
  evaluator flags **none** of the four cases.
  The blind spots, named in plain words as
  filed:
  - Case (i), the real Spec 026-era design
    (non-discriminating instrument): "The
    evaluator cannot be run against this case
    in its current form, so the gate has no
    reading on this defect class at all.
    Reason recorded: Error: input bundle
    contains zero claims: an empty bundle is
    an input error, never a pass (Spec 003
    FR-1.1)" — the evaluator extracts zero
    claims from the prose design and cannot
    run.
  - Case (ii), planted unfalsifiable headline
    claim: "The evaluator does not detect a
    falsifier that is present in form and
    empty in substance: the planted headline
    claim FB2-C01 passes with no correctness
    finding naming its untestable test."
  - Case (iii), planted wrong pin (52 against
    a source summing to 47): "The evaluator
    does not recompute pinned quantities
    against their cited sources: a total of
    52 pinned against a source summing to 47
    passes without a correctness finding. C2
    (independent recomputation) is the
    component that carries this class."
  - Case (iv), planted unsupported citations:
    "The evaluator verifies that citations
    resolve, not that they support: claims
    stating the opposite of their cited
    records pass in both the freeze
    configuration and with evidence
    verification on. C3's verification step —
    a verifier reading the cited text against
    the claim — is the component that carries
    this class."
- **C2 — independent spot-check** (record
  `gate-records/c2-spotcheck.json`, outcome
  PASS). A worker who did not draft the spec
  recomputed, from the spec text and the
  pinned inputs only, all 17 gate-turning
  quantities and — beyond the scaffold's
  sampled 3 — every one of the 8 remaining
  quantities: **25 of 25 agree**, including
  the Asset A v2 and Registry v2 digests and
  census, the corpus and grades digests and
  counts, the population 3,045 / 557 / 550,
  the corroborated 5,131, the floor basis 22,
  and token 999's 2 rows / 2 occurrences. One
  path correction is recorded in the record
  and at adjudication §6: the recomputer was
  tasked with a non-existent filename
  (`final_crosswalk.csv`); the spec's §3
  names the crosswalk of record correctly
  (`sign_crosswalk_master.csv`), whose digest
  and rows agree with the pin.
- **C3 — evidence sample, verification on**
  (record `gate-records/c3-evidence-sample.json`,
  outcome PASS). Sample: the 5 verdict-bearing
  claims (F075-C03, C06, C07, C08, C11) plus
  the scaffold's sample of the remainder
  (F075-C05, C12) — 7 of 13. The verifier read
  every cited text against its claim: all 22
  individual references resolve and support
  their claims; **all 7 sampled claims
  verified; no verdict-bearing claim
  unverified**. The engine's own verification
  run (aee assess --verify-evidence, lenient;
  27 evidence items checked) is recorded in
  the record's notes: its MISSING-REF findings
  are its single-path reading of multi-path
  and out-of-repo (goal-record) references,
  and its QUALITY-MISMATCH findings a
  labelling difference on decision-record
  references — battery case (iv)'s blind spot,
  carried by the verifier's reading, as
  designed.
- **C4 — mechanical check.** The gate-records
  set above is what the C4 CI job reads; it
  passed on this directory before the PR was
  assembled (checker run at the freeze act)
  and must pass in CI on the freeze PR. In
  this shadow freeze the job is not a
  required branch-protection check.
- **C5 — gate statistics** (regenerated at
  this freeze; `docs/freeze-gate/gate-statistics.md`
  in the freeze PR): freezes carrying gate
  records so far: **1** (this one, shadow);
  freezes blocked by C2: **0**; blocked by C3:
  **0**; C2 mismatches recorded: **0**; C3
  unverified sampled claims: **0**. The
  register-discipline gate's scale, for
  contrast: 47 freezes carry an AEE freeze
  note on main, the legacy gate's findings
  draft-cap hygiene records throughout.

## 6. Freeze digest

The freeze digest is computed by
`build_freeze.py` (framework026) over seven
sources — this record, `spec.md`, `claims.json`,
`adjudication.md`, `aee/freeze-aee-note.md`,
`build_freeze.py`, and
`backend/tests/test_spec075_freeze.py` — and is
recorded in `freeze.json` in this directory and
quoted in the freeze pull request. It was
computed after the AEE gate and the gate
records were filed, over the final texts. The
freeze tests (`backend/tests/test_spec075_freeze.py`)
replay the digest, assert the definition's
constants, the register's integrity, the hook
artifacts' pass shape, and the input pins of
§2 by recomputation.

## 7. Able-to-fail proof

With the assembled freeze in place, the
register's `register_version` was mutated in
exactly one place (0.7-draft → 0.7-draft-MUTATED)
and the freeze tests were run: they failed (the
replay and the register integrity assertions).
The register was then restored byte-identical —
its SHA-256 re-verified against the frozen
value — and the tests passed. The freeze is
therefore falsifiable by its own tests: a
silent change to a frozen source breaks the
replay rather than passing unnoticed.

## 8. What this freeze establishes / does not establish

This freeze establishes that the depicted-kind
endings question is well-posed against the
repaired surface: its population reproduces,
its inputs are pinned and independently
recomputed, its kinds are the published
identifications at measured sizes, its
celestial arm is honestly empty, its falsifier
is stated per kind in advance, and its verdict
words are frozen — and it files the
strengthened gate's first full run as the
designated shadow freeze. It does not
establish anything about any kind's ending
behaviour: **no verdict exists**, no census
past the step-0 population facts has been
taken, and no final-position quantity has been
computed. It does not touch Spec 071's
retirement or its reopening trigger, and it
moves no anchor, reading, PRED-2026 state,
verdict, status, or frozen text anywhere in
the programme. Execution runs only under the
owner's order recorded in the header, against
this frozen record, through the frozen gates.
