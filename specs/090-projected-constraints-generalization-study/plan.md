# Spec 090 — study plan

**Date**: 2026-11-04. **Package branch**: `feat/090-spec-package` (this
package; repo home on adoption:
`specs/090-projected-constraints-generalization-study/`).
**Commission basis**: the owner's direct order of 2026-11-04 ("do both
in order," item 1), delivered via the VEXA chat
(`records/commission-and-grounding-2026-11-04.md`): Glossa attempts G1
and G2 of the generalization bar as a registered study. This is a
study, not a build: its stages produce documents, a derivation (or its
obstruction record), and an outcome record — no machinery, no gate
class, no code.

Study order:

**adoption → the G1 document (draft → adversarial pass → freeze) →
the G2 derivation → outcome record + report to the VEXA chat.**

The order is forced by the subject: G2 derives from the projection G1
states, so no derivation step may begin before the G1 document is
frozen; and the G1 document is written *before results* by G1's own
definition, so it may not be revised in light of the derivation's
fortunes — revisions after the freeze are amendment acts (D-090-1),
and a revision the derivation forces is itself a finding the outcome
record reports.

## Stage 0 — package adoption (precondition for every study stage)

- The package (spec.md, claims.md, aee-claims.json, plan.md, tasks.md,
  records/) lands in the repo as
  `specs/090-projected-constraints-generalization-study/` on the
  package branch, PR'd and merged on the owner's block approval.
- **T002 (done at drafting, re-verified at adoption)** — the C090
  bundle was run through the pinned assessor in the CI-faithful venv,
  the same invocation as Spec 088's and Spec 089's T002:

  ```
  ~/workspace/venvs/glossa-ci/bin/aee validate aee-claims.json
  → valid: 16 claim(s) in aee-claims.json   (exit 0)
  ~/workspace/venvs/glossa-ci/bin/aee assess --no-ledger \
      --input aee-claims.json --output records/t002-aee-assessment.json
  → exit 1; outcome: iterate
  ```

  Verbatim summary of record: "Assessed 16 claim(s); found 71 failure
  mode(s); 16 claim(s) below the 0.70 confidence threshold. Shared
  evidence: 1 supporting source(s) shared across 16 of 16 claim(s)…
  Draft cap: 16 draft claim(s) capped at gather_evidence/iterate
  (FR-2.3). Stage cap: 16 claim(s) below stage 'explained'; the outcome
  cannot be 'pass' (Spec 004 R1.4)…" (full text: `records/t002-note.md`;
  the assessment itself: `records/t002-aee-assessment.json`). `iterate`
  is the expected outcome for a draft bundle on a single asserted
  source; the owner's approval (T003) is the human act. The bundle was
  generated from claims.md by script; the generator reproduces Spec
  088's and Spec 089's committed bundles byte-identically from their
  claims.md files, and this bundle's set identity (16 ids, in order,
  one falsifier each) was verified mechanically (t002-note.md).
- **Pre-append gate check (the freeze discipline)**: before the intake
  append, the adoption PR runs the gate CLI on the un-appended tree
  and records ALL PASS, so any post-append failure is attributable to
  the append and not to drift (the Spec 088/089 adoption shape).
- **T003 — owner block approval** of spec + 16 claims + this plan +
  decisions D-090-1..4. No study task starts before it. This is the
  ratification act for the study — distinct from the commission,
  which authorized the package to be drafted.
- **T004 — adoption intake**: the claims enter the ledger through
  `tools/ledger/import_bundle.py --spec
  specs/090-projected-constraints-generalization-study --date
  <adoption date>` — never a hand-edit of claims.jsonl — followed, in
  the same motion, by regeneration of the generated layers over the
  grown ledger and the settling-chain refresh the pin move forces
  (canonicals verified 6/6 over the new build before the pin refresh),
  exactly the Spec 087/088/089 adoption shape. Claim C090-13 bounds
  the whole study's ledger diff to this append.

## Dependencies

- The skeleton and scoping note, of record in this package's
  `records/` (AXIOVEX/vexa commit 88839493, hashes verified at
  drafting). The study reasons from these copies; if the VEXA chat
  revises the skeleton mid-study, the revision is a new source
  version and the study records which version it answered.
- The substrate stands: Spec 086 complete (ledger, gate V1–V9,
  matrix, maps), Spec 087 complete, Spec 088 complete (gate V10,
  program map, ratified register), Spec 089 adopted or in adoption —
  the study depends on their records, not on 089's build stages.
- The grounding census (`records/commission-and-grounding-2026-11-04.md`)
  is the study's counted starting state; S1 re-counts whatever it
  cites at the tree state it actually reads, and says which.
- No dependency on the desktop host, the live backend, or any
  external party: the study works from the repo's records.

## Stage 1 — The G1 document

**PR**: `feat/090-s1-g1-document` → one PR (the G1 document + the
adversarial-pass record + the drafting record; documents only).

**Contents**:

- **The draft** (`records/g1-document.md`, D-090-1): written from the
  records, containing exactly Appendix B items 1–3 and nothing else:
  1. *The record system (D1).* The record classes — corpus records,
     anchor records, ledger claim lines — each defined with its
     provenance rule and its counted population; the register's
     exception classes (the 3 `no_validation_record` anchors)
     accounted for in the definition, per C090-2.
  2. *The projection rule (D2).* The candidate state for the
     decipherment domain defined; the rule pi stated as a mapping
     from a candidate state to the records it would produce;
     projection-equivalence defined by the rule; and the
     **cannot-distinguish account**: the indistinguishabilities the
     records impose, each tied to its grounding record or count
     (frame-dependent signary; unattested and unanchored contexts;
     the 44 pending-validation readings; completions differing only
     outside the surviving records), per C090-3/C090-4.
  3. *The absolute disposition (D3).* The audit of C090-6: the
     candidate absolutes enumerated (the corpus frame; the anchor
     readings' external identifications; the surviving corpus's
     extent; any further candidate the drafting finds in practice),
     each disposed of as record-relative (variation exhibited),
     derived, the one named absolute — or the none-needed proof
     assembled from the dispositions; or the two-absolutes finding,
     if that is where the audit lands (D-090-2).
  The draft contains no outcome language anywhere (C090-7): a reader
  handed it learns what the records are and what they cannot say —
  never what the team concluded.
- **The adversarial pass** (a separate worker, not the drafter): the
  draft attacked on the record, on named questions —
  (i) *Second absolute*: does any quantity function in the draft as
  taken-as-given while the audit disposes of it as relative or
  derived? Are there absolutes in the program's practice the audit
  never lists?
  (ii) *Rule or metaphor*: is pi a decidable mapping, or does any
  equivalence question the draft raises require intuition the rule
  does not supply? The attacker must pose at least one concrete
  pair of candidate states and test the rule against it.
  (iii) *Grounded indistinguishability*: is every asserted
  indistinguishability tied to a record the attacker can open? Is
  any pair the draft calls indistinguishable actually distinguished
  by a record?
  (iv) *Protocol separation*: does the draft anywhere conclude?
  Each attack is sustained or not, on evidence, in the pass record.
- **Revision + freeze**: sustained attacks are answered by revision;
  the answers are recorded (attack → disposition → the text it
  changed). The frozen G1 document is hashed in the stage record.
  If an attack sustains that cannot be answered by revision — the
  projection will not state as a rule; the audit will not close —
  the stage does not force it: the G1 outcome is NOT YET with the
  missing element named, and the study proceeds to S3 (S2 cannot run
  without a stated projection; its outcome is then NOT YET on the
  same obstruction).

**Verification**: the stage reviewer checks the frozen document
against Appendix B items 1–3 line by line, re-counts every population
figure it cites from the records at the tree state read, and confirms
the hash in the stage record is the document's hash.

**Claims**: C090-1..7, C090-12 (the D6 account the draft's record-system
section touches).

## Stage 2 — The G2 derivation

**PR**: `feat/090-s2-g2-derivation` → one PR (the derivation record;
documents only). Runs only if S1 froze a G1 document.

**Contents**:

- **Candidate derivation(s)**: necessary conditions in D4's form,
  derived from the frozen G1 document — its definitions, its stated
  projection, its absolute disposition — plus D1–D3 and nothing else
  (D-090-3). Natural hunting ground, named as occasion only: what
  must hold of every completion of a corpus whose sign inventory is
  frame-relative; what the projection's equivalence classes force on
  any reading assignment over unanchored signs; what a record system
  with this provenance structure cannot certify about its own
  completions. A candidate suggested by the physics pattern is
  welcome; its chain must stand with the physics premise removed
  (C090-8).
- **The derivation record**: for each candidate — the statement in
  D4's form (over equivalence classes, C090-9); the chain, step by
  step, each step citing the definition or stated rule it follows
  from; the falsifier in D4's form (the impossible record, named as
  a record kind with properties, C090-10); and whether the condition
  bites — what candidate decipherment or claim it would exclude, or
  the plain statement that it is true and trivial.
- **The derivation audit** (a separate worker or the stage reviewer,
  not the deriver): every step re-walked; every premise traced to
  the G1 document or D1–D3; the falsifier tested for form (is it a
  record the system admits? would its observation be recognizable?).
  A step that does not follow is named, and the candidate falls to
  the obstruction record rather than being repaired silently
  mid-audit — repairs are new derivation attempts, recorded as such.
- **Outcome**: DERIVED (at least one candidate's chain completes the
  audit) or NOT YET (the obstruction record names, per candidate,
  where the chain broke and what would have to change). Both are
  stage results; the stage is not permitted to end in neither.

**Verification**: the audit record is the verification; the stage
record quotes its outcome per candidate.

**Claims**: C090-8..11.

## Stage 3 — Outcome record + report

**PR**: `feat/090-s3-outcome` → one PR (the outcome record; the tasks
ticks; documents only), plus the report act itself, which is a chat
message, not a PR.

**Contents**:

- **The outcome record** (the closeout, T301): per-claim dispositions
  for C090-1..16 (discharged / carried, with the evidence pointer for
  each); the per-stage outcomes in spec.md's vocabulary (G1: STATED
  or NOT YET + the missing element; G2: DERIVED or NOT YET + the
  obstruction); the study-level outcome (INSTANTIATES-path / ANALOGY
  + the element named / NOT YET + the missing work); the G3–G5
  sequencing note (commissioned in principle by the same order, not
  started, with what this study's outcome implies for their order
  and difficulty — as assessment, not as a plan); and the explicit
  statements that no claim's status/stage/score moved, no convergence
  step was taken or implied, and the formal verdict over the full bar
  remains the independent reader's, not this study's.
- **The report to the VEXA chat** (T302): the outcome (or the
  blocker, if a stage could not run) delivered to the VEXA chat for
  the improvement registry, carrying the per-stage outcomes, the
  study-level outcome, and the evidence pointers. The send is
  recorded in the outcome record (date, destination, text or its
  hash). If the outcome is ANALOGY or NOT YET, the report says so in
  those words — the skeleton requires the outcomes recorded either
  way, and this study does not soften them in transit.

**Claims**: C090-12..16 (closeout side).

## Decision points needing the owner

- **T003 (Stage 0)** — block ratification of this package: spec, 16
  claims, this plan, decisions D-090-1..4. The commission authorized
  the study; ratification is the program's own act that starts it.
- **The absolute disposition, if split (S1)** — if the adversarial
  pass sustains an attack on the audit that the drafters cannot close
  (a genuine second-absolute candidate, or a candidate whose
  disposition reasonable readers split on), the question goes to the
  owner as oracle (D-090-2) with the attack record as the brief. The
  study does not resolve a sustained split by drafting majority.
- **Nothing else is the owner's by default**: stage outcomes
  (STATED/NOT YET, DERIVED/NOT YET) are the stages' own verdicts on
  their records, reported in the outcome record; publication of any
  study product (a paper, a tracker entry) is a separate owner act
  outside this spec.

## Design rules carried through every stage

- **Definitions before results, and the freeze is real**: the G1
  document is not revised in light of G2's fortunes except by a
  recorded amendment act, and such an amendment is reported as a
  finding (the definitions the derivation needed were not the
  definitions stated).
- **The protocol's separation is structural**: drafters, attackers,
  derivers, and auditors are separate workers; conclusions live only
  in derivation and outcome records; the G1 document never acquires
  any.
- **Numbers come from records**: every count quoted in any stage
  record is re-counted from the records at the tree state read, with
  the state named — never carried from this package's census without
  the re-count.
- **A clean negative is a result**: NOT YET with a named obstruction
  and ANALOGY with a named element are completions of this study, on
  the same footing as STATED/DERIVED. No stage softens an outcome to
  make the study read better; the improvement registry gets the
  outcome the records support.
