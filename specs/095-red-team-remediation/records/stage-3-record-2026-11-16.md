# Stage 3 Record — Evidence Machinery (2026-11-16)

Spec 095 (red-team remediation), Stage 3: T301–T304. Branch
spec/095-s3-evidence-machinery, base 0b6ec665 (Spec 095 Stage 2
merge). Claims discharged: C095-7, C095-8, C095-9, C095-10 (per
claim, below). All four tasks are ticked in tasks.md; T303's tick
carries the judgment stated in its section.

## T301 — The contamination gate class (C095-7)

The six shapes are enumerated verbatim in C095-7; no shape or
instance had to be invented, and none was. The shapes: (S1) a
source-derived value labelled independent; (S2) a self-labelling
derivative presented as source data; (S3) a translation or
reading column presented as corpus data; (S4) a derived result
presented as independent confirmation; (S5) the same data under
two source identities; (S6) a summary or delivery presented as
the underlying record.

Implementation: backend/glossa_lab/ledger_contamination.py — a
gate class over intake presentations, run through the gate
tooling as `tools/ledger/check_ledger_gate.py --contamination`.
Design choice, stated: the class reports under its own summary
and is not folded into the V1–V11 check counts, because the
standing profile (--all 29/0/1, --regen 32/0/0) is a cross-stage
record that must not move; the class's own block reads
"contamination class (Spec 095 T301, C095-7): N presentations
scanned, M flag(s)" and closes CONTAMINATION: PASS / FLAGS
RAISED, with its own exit code. The detectors key on the
mislabelling, never on derivation alone: a derivative cited as a
derivative is ordinary work and is not flagged (negative fixture
neg-2 exists to prove it).

The six historical instances, re-detected from their records in
the acceptance fixtures (records/t301-fixtures-2026-11-16.json,
each fixture carrying its record citation):

- S1 — GR-088-01: the advertised "independent Parpola validation"
  computed from the Phase-96 crosswalk, whose values derive from
  the program's own construction (baseline sections 1.5, 4.4;
  0 of 184 eligible as independent). The fixture trips S1 (and
  S2, as the historical episode in fact did).
- S2 — GR-088-01: the Phase-96 mechanism itself (baseline
  section 4.3): program code wrote the project's anchor reading
  into the crosswalk reading field under a "Parpola 1994" source
  label — 116 entries (scan B-01).
- S3 — GR-088-16 family: the cross-compilation positional line
  (Phase-125 and its attribution successors 034/058), in which
  one side's profiles were computed over the mayig/CISI sign
  sequence transcription — a reading column in Parpola sign IDs —
  presented as corpus data of the same kind as the Holdat side;
  the attribution line localises the disagreement to the
  transcription layer (spec 058 is the transcription-disagreement
  mechanism study).
- S4 — GR-088-01: every "Parpola agrees" relation in the lineage
  is circular (scan B-01) — a derived agreement presented as
  independent confirmation; baseline section 5.3's distinction
  between original evidence and repetition on the same
  observations is the same episode's other face.
- S5 — GR-088-29: two production datasets (the VM-era dataset
  and desktop snapshot 1, 2026-10-28) held the same accumulated
  work product under two identities until the owner ruling of
  2026-11-05 made snapshot 1 canonical where they differ (scan
  C-09).
- S6 — GR-088-11: the claim-to-sign linkage exists only in the
  generated matrix layer (scan C-05: exactly one claim of 876
  carries sign_refs that resolve; the claims' own records carry
  none), so reading the linkage from the matrix is reading a
  generated summary in place of the underlying record. The same
  shape is corroborated inside the GR-088-29 ruling, which
  separates what VM production served (a delivery, snapshot 2)
  from the canonical record (snapshot 1).

Fixture outcomes (backend/tests/test_spec095_contamination_gate.py,
8 tests): all six historical fixtures are flagged with their
shape of record; six planted fixtures (one per shape, per the
RT-14 acceptance line) trip exactly their shape; three negative
fixtures (a genuinely independent source; a derivative cited as
a derivative; the same file under one identity twice) are not
flagged; a real ledger entry mutated to carry one pin under a
second identity is flagged S5, proving the class has teeth on
ledger-shaped data. On the current ledger the class passes:
1,025 presentations scanned, 0 flags (the live scan builds the
minimal presentation each entry itself carries, and runs the S5
pin check ledger-wide; verified independently that no content
pin is carried under two distinct paths anywhere in the ledger).

## T302 — The standards stated once (C095-8)

Location, chosen and stated: glossa-indus/STANDARDS.md — the
Standards of Record, at the top level of the program tree beside
CORPUS_IDENTITY_STANDARD.md, the program's existing home for
documents of record that govern the whole evidence graph. (The
register's note said "in the study-spec template's terms, via
the Spec 090/093 pattern": the template carries no equivalence
or reporting vocabulary to inherit — verified by reading it —
so the standards are stated in the program's own terms, in one
place, and later studies cite them as "Standards of Record,
Part I/II".)

Part I (equivalence): equivalence only against a preregistered
margin, by an equivalence test (TOST or a stated interval rule);
never from a non-significant difference. Part II (statistical
reporting): a result is reportable only with effect size,
uncertainty interval, multiplicity handling, and achieved power
or precision basis; never a p-value alone. Both parts ground
themselves in the frozen record and note divergences in the
open: the program's frozen studies state numeric verdict bounds
in advance (Phase-125's section-6 pattern) but no frozen study
runs an equivalence test; the Phase-127 diagnostic is the
reporting standard's model (effect sizes, inscription-bootstrap
intervals, pre-registered arms, a power grid), against which the
Phase-48 pass tallies and the lone p-values formatted into
pipeline node outputs (Spec 095 Stage 2 census) are named as the
divergent older practice. Past results are not retroactively
held to the standard (C095-8, does-not-establish).

## T303 — The identifiability protocol, first application (C095-9)

The protocol is stated at STANDARDS.md Part III, built on the
program's own WP8 machinery (control families C1–C6, fairness
conditions, and the section 3.6 observational-equivalence rule,
carried verbatim in substance). The NOT IDENTIFIABLE amendment
is recorded in Part III as a dated amendment section — the
program's outcome vocabulary gains the verdict there, as
C095-9's text requires ("by a recorded amendment").

The full application — rival constructions per sign, per-sign
outcomes, the six standings re-stated, and the filed-not-applied
reasoning — is filed at
records/t303-identifiability-application-2026-11-16.md. Summary
of outcomes: all six readings are NOT IDENTIFIABLE under the
protocol, each for its own stated reasons; no outcome was
forced — the two partial discriminations the record contains
are recorded with their signs (M047: the meaning 'fish' carries
a discriminating observation of record, the value mīn does not;
M202: the sibilant class is discriminated by the Shu-ilishu slot
evidence, the value 'can' is not). The shared structural facts
are the audit's own: no strict anchor record states a falsifier
or a distinguishing observation (GR-088-12), the Phase-48
positional test never consumes the reading, the DEDR test is a
prefix-match plausibility count, and the Phase-276 comparanda
are similarity judgements (the same kun/kona pair is recorded
for both M044 and M124). NOT IDENTIFIABLE does not disprove any
reading, and the WP5 support-lineage dispositions are unchanged;
Part III rule 5 states the two-vocabulary rule, and claim
C091-6 (a count of support-lineage dispositions) is not
falsified by these outcomes.

Ledger application: FILED, NOT APPLIED, for a demonstrated
mechanical reason (full reasoning in the application record):
the ledger's reclassification act refuses, in the intake
validator, any supersedes naming no ledger entry, and no ledger
entry embodies any of the six standings (anchor readings are not
ledger claims; the ledger's three sign_refs in total resolve to
none of the six). The standings' other homes are a frozen audit
(not editable) and the canonical anchor table (gate-checked
data; an edit is a data change that would move the V6 strict
set and the 287 census, against Spec 094's byte-identical
boundary of record). Minting six new claims as targets would
create claims, not re-state standings. The ledger is untouched;
the claim census is unchanged (1,025 lines, 994 claims); the
gate holds. Tick judgment, stated honestly per the stage brief:
T303 is ticked because the task's work — protocol stated, first
application performed, amendment recorded, standings re-stated
under the outcome — is complete and filed; the one sub-part not
performed is the ledger mutation, which the machinery cannot
carry, and the application record names a remainder for the
Stage 5 closeout (a vehicle that can carry anchor standings as
acts does not yet exist).

## T304 — Reading direction as data (C095-10)

Carrier, chosen and stated: the Stage 1 corpus identity
registry (backend/glossa_lab/data/corpus_identity.py) — every
identity now carries an `orientation_basis` field — and its
standard document (glossa-indus/CORPUS_IDENTITY_STANDARD.md,
new section 5, added under the standard's own section-4 recorded
-act rule). The registry was chosen because it is the identity
of record a loader and a reader already consult. As registered,
none of the eight corpora records a reading-direction basis;
each entry states that and names the standing assumption
(stored order as reading order) as an assumption, not a fact.

Re-issues filed at records/t304-positional-reissue-2026-11-16.md,
scoped to the positional results this stage touches:

- R1, Phase-125 cross-compilation comparison (all three arms):
  recomputed from the recorded per-pair profiles in both
  orientations; the as-recorded orientation reproduces every
  filed statistic to six decimals; under joint reversal,
  per-pair TV is identical (max |delta| 0.0), median TV and W1
  unchanged, Spearman initial/terminal exchange, modal
  agreement unchanged — the FAIL/DISAGREEMENT verdict is
  orientation-invariant because one assumption is applied to
  both sides; only end-naming readings flip.
- R2, Phase-127 diagnostic arms (a)/(b): orientation invariance
  derived by the same reflection argument; stated as a
  derivation (per-replicate draws are not filed; no recomputation
  claimed).
- U1, the six anchors' Phase-48 positional-test outcomes:
  undefined-reversal statement — the profiles the test consumed
  were computed at runtime from the Holdat layer, which is not
  in the tree, and the filed record carries outcomes without
  profiles; no reversed variant can be computed from the record
  as filed.
- U2, token frequency counts: reversal not defined for a count.
- U3, position-independent anchor flags: reversal not defined
  for a flag defined without orientation.

Acceptance: backend/tests/test_spec095_orientation_registry.py
(2 tests) — every registered identity carries an orientation
basis, and the standard states the requirement.

## Verification (local; no CI claim)

- New tests: test_spec095_contamination_gate.py 8 passed;
  test_spec095_orientation_registry.py 2 passed. Stage 1/2
  regression batch (corpus battery, validator pinning, synthetic
  containment): 39 passed, 2 skipped.
- Ledger gate, run sequentially on the quiet final tree:
  --all → summary: 29 PASS / 0 FAIL / 1 NOT-RUN; RESULT: PASS.
  --regen → summary: 32 PASS / 0 FAIL / 0 NOT-RUN; RESULT: PASS.
  Contamination class → 1,025 presentations scanned, 0 flag(s);
  CONTAMINATION: PASS. In-tree regenerations restored after each
  mode (generated layers only).
- Full backend suite, CI invocation (GPU files ignored;
  phase392 deterministic test deselected by plain nodeid from
  backend/; two-part split at test_spec086_ledger_gate.py, union
  stated): part 1 (test_spec086_ledger_gate.py alone) 67 passed
  in 943.68s; part 2 (the remainder) 2,875 passed / 66 skipped /
  1 deselected in 644.79s, with 1 one-off ERROR —
  test_workspace_scope_check.py::test_run_check_verdict_and_missing_db,
  the recorded known one-off fixture error (first sighted
  2026-11-12 in PR #561's CI; sqlite "no such table" at fixture
  setup), which passes on isolated rerun (1 passed in 0.10s).
  Union: 2,942 passed / 66 skipped / 1 deselected / 0 failed.
  The box's ClamAV on-access scanning (fanotify) throttled both
  parts throughout — the pytest process waited in
  fanotify_get_response for long stretches — so the wall times
  are the box's, not the suite's; no test outcome is attributed
  to it beyond the one-off error's rerun proof.
- Ruff (repo config, from backend/): clean on all changed files.

## Deviations

1. T303's ledger application is filed-not-applied (reasoned
   above and in the application record) — the brief's own
   fallback, exercised with its reason demonstrated from the
   validator's code, not asserted.
2. One self-inflicted revert, repaired: the post-gate restore
   after --all used a whole-tree checkout of glossa-indus/ and
   reverted this stage's section 5 of CORPUS_IDENTITY_STANDARD.md
   along with the gate's regenerations. The section was
   re-appended from its source and verified present (section 5
   at line 80) before the suite ran; later restores in this
   stage touched generated layers only.
3. The contamination class is a sibling report block rather than
   new V-legs inside run_gate: adding legs inside the counted
   summary would move the standing profile the brief forbids
   moving. The class is run by the same tooling, at intake, with
   its own summary and exit code.
