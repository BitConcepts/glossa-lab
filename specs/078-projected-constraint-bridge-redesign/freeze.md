# Spec 078 — Freeze record

**FROZEN — 2026-10-26.** This directory is the
frozen contract for Spec 078: `spec.md` (the M13
design carried into frozen form, with the
freeze-fixed completions at its §0 and the S4 note
at its §13), `claims.json` (the claims register,
drafted directly in the recovered 0.7 form, 10
claims F078-C01…F078-C10), `adjudication.md` (the
drafting record, with the freeze-prep review and
the freeze rulings DD-078-1…DD-078-7), this record,
the AEE hook artifacts under `aee/`, and the
strengthened-gate records under `gate-records/`.

The freeze is executed under the owner's order of
2026-10-26 ("review, freeze, and run the M13
pilot"). **Phase allocated: Phase 444**
(DD-078-1). This freeze is a **required-C4
freeze** (DD-078-7): the C4 records check is a
required branch-protection check since the act of
2026-10-25 that followed the Spec 075 shadow
freeze, and the gate records below must pass it
in CI on the freeze PR. **An OSF registration IS
filed at this freeze** (DD-078-5), under the
owner's express order for M13 — in contrast to
Spec 076, where the design named none and none was
filed; the coordinator performs the filing after
merge via the proven ORCID/token-link route, and
the registration identifier is recorded with the
pilot record. Execution — the §7 pilot — is a
separate act under the same owner order: it begins
when this freeze record is complete (this PR
merged on genuine CI including the required C4
check), runs once as frozen (FF-078-5), and is
recorded in `pilot-record.md` in this directory.

## 1. What was frozen

- **The question** (spec §1): whether the
  redesigned bridge — the two-axis pair-form
  vocabulary (§3), coding rules NC-1…NC-8 (§5),
  and A-FACE-2 (§4) — carries the strict core's
  basis language into checkable claims without
  manufacturing contradictions, on the foundation
  Spec 076 established and against the failure it
  measured (36 exclusions under the one-axis
  bridge).
- **The inheritance** (spec §7.1–7.2): the census
  derivation and the step-2 shuffle finding of
  Spec 076 stand as foundation (claim F078-C01),
  conditional on the successor pilot's step-0
  re-verification; step 2 is not re-run.
- **The pilot** (spec §7): step 0 reproduction
  gate (any mismatch closes CANNOT BE RUN AS
  WRITTEN and voids the inherited standing); step
  3′ the blind positive control over the 94 strict
  signs under NC-1…NC-8 and the FF-078-3 blindness
  protocol, on the counted population of 86
  (FF-078-2), at the frozen bar — total failures
  ≤ 3, neither line > 2, no pattern (FF-078-4),
  administrability ≥ 25 of 86 — with the §7.4
  closure words (BRIDGE DOES NOT HOLD; CANNOT BE
  ADMINISTERED — THE CORE MAKES TOO FEW CHECKABLE
  CLAIMS).
- **The completions the design left to the
  freeze** (spec §0, DD-078-3): FF-078-1 the
  numbering (Spec 078, Phase 444); FF-078-2 the
  counted population defined mechanically;
  FF-078-3 the blindness protocol in full;
  FF-078-4 the pattern clause operationalised
  (no change to the bar); FF-078-5 the pilot
  execution order. No bar, frame, null, or closure
  word of the design was moved (adjudication §4),
  and the freeze-prep review required no amendment
  to the design (adjudication §2).

## 2. The inputs (spec §7.1)

The corpus export (`glossa-corpus/indus/exports/indus_research.jsonl`,
SHA-256 08fc96c8…; 2,906 indusscript-m77 records;
frame census 11,507 tokens, 5,883 strict tokens,
slot totals 2,655 / 2,655 / 225 / 5,972, finals
partition 1,707 / 250 / 520 / 178; slot base rates
0.2307 / 0.2307 / 0.5190 / 0.0196); the anchors
file (`backend/reports/INDUS_FINAL_ANCHORS.json`,
SHA-256 df0cf620…; 287 entries, 94 strict, 44
pending); Registry v2
(`data/crosswalks/canonical_sign_registry_v2.csv`,
SHA-256 42ab09fb…, 1,013 rows) for the A-KEY
accounting. All three files are in git; none is
restricted. The parent record is the Spec 076
pilot record (2026-10-26; freeze digest
83259ed3…), preserved in the programme goal record.

## 3. Verification at the freeze

Every pin above was recomputed first-hand by the
freeze worker from the files as fetched from repo
main and agrees. The inherited census was
re-derived from those files and reproduces every
pre-named figure exactly — a further independent
route to the same numbers (Spec 033's pipeline
census; the M12 design's recomputation; the Spec
076 freeze's; the 076 pilot's steps 0–1; this
freeze's). The counted population under FF-078-2
was derived from the same census: 94 strict − 5
frame-absent (039, 044, 046, 362, 374) = 89
frame-attested − 3 worked examples (M002, M342,
M347) = **86**. No pilot quantity was computed at
drafting or at the freeze: no basis beyond the
design's three published worked examples was coded
under NC-1…NC-8, the §7.3 coherence check was not
run on any counted sign, and the bar was not
checked against any coding (adjudication §4).

## 4. AEE gate

The hooks ran before the digest was computed,
with the pinned evaluator (aee 1.5.3) in the
freeze configuration, at all three hooks
(after_specify, after_plan, after_tasks). Each
artifact carries **19 findings: the 10 FR-2.3
draft caps (one per claim) and 9 irreducibility
challenges (F078-C01, C02, C03, C04, C06, C07,
C08, C09, C10); zero findings of contradiction,
independence, ambiguity, or evidence-resolution
kind; no claim below the 0.70 threshold (minimum
propagated confidence 0.7200)**. The challenges
are answered in `aee/freeze-aee-note.md` from the
spec's own structure — the inherited assumption
set is itself the decomposition, filed as
separate claims (C04/C05/C07), and A-FACE-2's two
falsification tests are its two named deaths —
and ruled at DD-078-4; the register was not
reworded to silence them.

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
  A fresh recomputation from the spec text and the
  pinned inputs only — written for this freeze and
  importing none of the spec's derivation code —
  recomputed all 13 gate-turning quantities and
  all 3 remaining quantities: **16 of 16 agree**,
  including the three input digests, the 11,507 /
  5,883 token censuses, the slot totals, the
  finals partition summing to 2,655, the slot base
  rates to 4 decimal places, the counted
  population (94 − 5 − 3 = 86, the frame-absent
  five named), the 677 exclusions with their size
  distribution, the solo-only set of 13, and the
  §6 worked-example rows with their anchor shares
  (M342 0.6876; M347 0.8218).
- **C3 — evidence sample, verification on**
  (record `gate-records/c3-evidence-sample.json`,
  outcome PASS). Sample: the 3 verdict-bearing
  claims (F078-C01, C02, C08) plus a sample of the
  remainder (F078-C03, C06) — 5 of 10. The
  verifier read every cited text against its
  claim: **all 5 sampled claims verified; no
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
  records so far: **3** (075, 076, this one);
  freezes
  blocked by C2: **0**; blocked by C3: **0**; C2
  mismatches recorded: **0**; C3 unverified
  sampled claims: **0**.

## 6. The S4 note (spec §13; queued at the rerun audit of 2026-10-26, F4)

In short: S4 — the rule that score-based methods
must face a calibrated structured generator,
because a deterministic generator of seal-like
inscriptions for a fictional non-language passes
published statistical language diagnostics — does
not add a generator arm to this pilot. M13's
verdicts rest on deduction (mechanical
contradiction of stated universal claims by
attested occurrences) and on a blind
human-language coding control, not on scores or
language-likeness diagnostics, which are the class
S4 governs. The pilot's one statistic, anchor
share against the slot base rate, is a calibration
device that files nothing and may never enter a
register entry (spec §8.3), so no filed claim ever
rests on a statistic a structured generator could
spoof. The inherited step-2 shuffle result already
carries Spec 076's own S4 boundary note and is not
re-run or extended here. The structured-fake risk
that does apply to a coding control — basis
language that looks claim-shaped but is not — is
what NC-7's weaker-strength coding, the summary
line, and A-FACE-2's residue falsifier exist to
catch, with the pattern clause as the tripwire.
The boundary is recorded in spec §13 so that any
future score-based use of the register takes S4
with it at that time.

## 7. Freeze digest

The freeze digest is computed by `build_freeze.py`
(framework026) over seven sources — this record,
`spec.md`, `claims.json`, `adjudication.md`,
`aee/freeze-aee-note.md`, `build_freeze.py`, and
`backend/tests/test_spec078_freeze.py` — and is
recorded in `freeze.json` in this directory and
quoted in the freeze pull request. It was computed
after the AEE gate and the gate records were
filed, over the final texts. The freeze tests
(`backend/tests/test_spec078_freeze.py`) replay
the digest, assert the definition's constants,
the register's integrity, the hook artifacts'
pass shape, and the input pins of §2 by
recomputation, including the FF-078-2 counted
population.

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

This freeze establishes that the bridge redesign
is well-posed against its inherited foundation:
its census reproduces by a further independent
route, its predecessor's failure is localised and
named part by part, its successor assumption is
filed as a claim with two named deaths, its bars
were committed by the design before any run and
are frozen here unmoved, its coding rules can
fail, and its one statistic is fenced out of the
register in advance. It does not establish that
the pilot passes, that the bridge holds, that
A-FACE-2 is true, or anything about what any sign
means: **no register exists unless the pilot
passes**, no coding under NC-1…NC-8 has been run
for the count, and no claim has been judged
against the census. It moves no anchor, reading,
PRED-2026 state, verdict, status, or frozen text
anywhere in the programme, touches neither M4's
gate nor M7's attack, and leaves the standing
position unchanged: the script is not deciphered.
