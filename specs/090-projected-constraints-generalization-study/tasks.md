# Spec 090 — Tasks

Acceptance modes per the Autonomous Execution Doctrine: **test** (a named
automated check decides), **gate** (the Spec 086 gate / CI decides),
**human-as-oracle** (a named human reads a named artifact and rules).
Every task carries the *This does not establish* line that must survive
into its stage report.

## Stage 0 — Package adoption

- [x] **T001 — Package lands.** spec.md, claims.md, aee-claims.json,
  plan.md, tasks.md, records/ (commission-and-grounding record, the two
  source documents byte-identical to AXIOVEX/vexa commit 88839493, T002
  assessment + note) committed as
  `specs/090-projected-constraints-generalization-study/` on
  `feat/090-spec-package`. Claims: package-level. Acceptance: **test**
  (the package verification of record: aee-claims.json parses; claims.md
  and aee-claims.json carry the same 16 claim ids; every claim has a
  falsifier and a DNE line; the source documents in records/ hash to
  the pinned values a66ffe4f… / 281f3543…; the grounding record's
  census numbers are reproducible from the repo at the package's base
  commit).
  *This does not establish:* that the package is approved — only that
  it is complete and internally consistent.
- [x] **T002 — AEE verification of the claims.** The C090 bundle run
  through the pinned assessor (aee 1.5.3, CI-faithful venv), exactly as
  Spec 088's and Spec 089's T002: `aee validate` → `valid: 16
  claim(s)`; `aee assess --no-ledger` → **outcome: iterate** (71
  failure modes; draft cap and stage cap binding by construction).
  Assessment of record: `records/t002-aee-assessment.json`; commands
  and verbatim outcome: `records/t002-note.md`. Acceptance: **test**
  (the assessor ran and its outcome is recorded verbatim).
  *This does not establish:* claim quality — `iterate` is the expected
  reading for a draft bundle on one asserted source; the owner's
  approval is the human act (T003).
- [x] **T003 — Owner block approval.** The owner ratifies the package
  as a block: spec, 16 claims, plan, and decisions D-090-1..4.
  Acceptance: **human-as-oracle** (the owner).
  *This does not establish:* approval of any later stage's output —
  the G1 document, the derivation, and the outcome each land on their
  own evidence.
- [x] **T004 — Adoption intake + generated-layer regeneration.** After
  T003: (a) record the pre-append gate run (gate CLI on the
  un-appended tree, ALL PASS); (b) append the C090 bundle through
  `tools/ledger/import_bundle.py --spec
  specs/090-projected-constraints-generalization-study --date
  <adoption date>` — the only sanctioned path, never a hand-edit;
  (c) regenerate the generated layers over the grown ledger, republish
  through `tools/ledger/gated_publish.py`, and run the settling-chain
  refresh the pin move forces (canonicals verified 6/6 over the new
  build before the pin refresh). Claims: C090-13. Acceptance: **gate**
  (the ledger-gate job green incl. the bundle-reconciliation test; the
  ledger diff is exactly the append).
  *This does not establish:* anything about the appended claims' truth
  — only that the ledger grew by the sanctioned path and the generated
  layers match it.

## Stage 1 — The G1 document (PR: feat/090-s1-g1-document)

- [x] **T101 — The G1 draft.** `records/g1-document.md`: Appendix B
  items 1–3 in the skeleton's terms — the record system defined over
  its actual classes (corpus records, anchor records, ledger claim
  lines), each with its provenance rule, its population re-counted at
  the tree state read, and its exception classes accounted (the
  anchors register's `no_validation_record` entries named); the
  projection rule stated as a decidable mapping from a defined
  candidate state to the records it would produce; the
  cannot-distinguish account, every indistinguishability tied to its
  grounding record or count; the absolute disposition by audit
  (candidates enumerated and disposed of; one named absolute, the
  none-needed proof, or the two-absolutes finding). No outcome
  language anywhere in the document. Claims: C090-1..7, C090-12.
  Acceptance: **human-as-oracle** (the stage reviewer against Appendix
  B items 1–3 and C090-7's separation, line by line).
  *This does not establish:* that the definitions are right — only
  that they are stated, completely, in the skeleton's terms, before
  results; their trial is T102's attack and S2's use of them.
  *Completed (draft) 2026-11-04:* `records/g1-document.md` v1
  (31,376 bytes, SHA-256
  974d5043ab463d0e6a33912b6e1136bcac288cd679827edade3c81d7af858d5b),
  drafted from the records at a7db3cfb; drafting record:
  `records/stage-s1-record.md`. T102 (adversarial pass) and T103
  (revision + freeze) remain open — the document is a draft until
  T103 freezes it.
- [x] **T102 — The adversarial pass.** A worker other than the
  drafter attacks the draft on the record, on the four named
  questions: (i) second absolute — any quantity functioning as
  taken-as-given while disposed of as relative or derived, and any
  practice absolute the audit omits; (ii) rule or metaphor — at least
  one concrete pair of candidate states posed and the equivalence
  question put to the stated rule; (iii) grounded
  indistinguishability — every asserted indistinguishability opened
  against its cited record, and a search for a distinguished pair the
  draft calls indistinguishable; (iv) protocol separation — any
  sentence that concludes. Each attack is marked sustained or not, on
  evidence, in the pass record. Claims: C090-3, C090-4, C090-5,
  C090-6, C090-7. Acceptance: **human-as-oracle** (the stage reviewer
  confirms each named question was actually attacked, not gestured
  at).
  *This does not establish:* that an unsustained attack means the
  draft is sound — only that these four attacks, worked on evidence,
  did not land; the independent reader's judgment stands after this
  study regardless.
  *Completed 2026-11-04:* `records/stage-s1-adversarial-record.md`
  — the four attacks executed on evidence against the draft at
  f43447bb (v1 hash recomputed and matched): (i) second absolute
  NOT SUSTAINED (the none-needed disposition survives; clarity
  residue F7); (ii) rule or metaphor SUSTAINED IN PART — π is a
  decidable rule, executed on the draft's illustrations and two
  attacker cases, with defects F1 (high), F2 (high), F3 (medium);
  (iii) grounded indistinguishability NOT SUSTAINED (every item
  α–ε re-counted; note F9); (iv) separation NOT SUSTAINED,
  citation precision SUSTAINED in part (F4 medium; F5, F6 low;
  F8 clarity). Nine findings F1–F9 carried to T103.
- [x] **T103 — Revision and freeze, or the NOT YET exit.** Sustained
  attacks answered by revision, each answer recorded (attack →
  disposition → text changed); the revised document frozen, its
  SHA-256 quoted in the stage record — the G1 outcome is STATED. If a
  sustained attack cannot be answered by revision (the projection
  will not state as a rule; the audit will not close), no text is
  forced: the stage record declares G1 NOT YET with the missing
  element named, and the study proceeds to Stage 3. A sustained split
  on the absolute disposition goes to the owner as oracle (D-090-2)
  before the freeze. Claims: C090-1, C090-5, C090-6. Acceptance:
  **human-as-oracle** (the stage reviewer; the owner where the
  D-090-2 split rule fires).
  *This does not establish:* that a frozen G1 document is the final
  G1 answer — amendments remain possible as recorded acts, and the
  reader's verdict is not this study's to give.
  *Completed 2026-11-04:* G1 outcome **STATED** — the document
  revised under findings F1–F8 (F9's clarifying clause added) and
  frozen as **v1.1** (34,226 bytes, SHA-256
  4f2018f40c9ccaf0811cd7661b0c9e1ebd840c7e014d954f778c42edef27efc2);
  freeze act: `records/stage-s1-freeze-record.md`. The NOT YET
  exit was not taken (every sustained attack was answerable by
  revision), and the D-090-2 owner-oracle rule did not fire (no
  sustained split on the absolute disposition: NONE-NEEDED
  stands). Stage 2 derives against v1.1 at the hash above.

## Stage 2 — The G2 derivation (PR: feat/090-s2-g2-derivation)

- [x] **T201 — Candidate derivation(s).** Runs only on a frozen G1
  document. For each candidate: the statement in D4's form (over the
  G1 projection's equivalence classes); the derivation chain, step by
  step from D1–D3 and the G1 document's definitions only; the
  falsifier in D4's form (a named record kind with named properties
  that the framework declares impossible); and the bite statement
  (what the condition excludes, or the plain note that it is true and
  trivial). All candidates, completed or broken, are in the
  derivation record. Claims: C090-8, C090-9, C090-10. Acceptance:
  **test** (the derivation record's mechanical completeness: every
  candidate carries statement, chain, falsifier, bite statement; every
  chain step cites its premise).
  *This does not establish:* that any chain is sound — soundness is
  T202's audit, and a complete-looking chain is exactly what an audit
  exists to test.
  *Completed (derivation) 2026-11-04:* `records/g2-derivation.md`,
  derived against the frozen G1 document v1.1 (SHA-256 4f2018f4…,
  recomputed and matched before deriving). Four candidates worked:
  Candidate 1 (the non-certification condition) and Candidate 2
  (the recorded-profile condition) carry complete chains, each with
  its D4-form statement, step-by-step chain with premises cited,
  counted form, D4 falsifier, bite statement, and a
  derivation-provenance self-audit with its labeled boundaries;
  Candidate 3 (register-certification over the unvalidated
  readings) and Candidate 4 (standalone corpus regularities) are
  recorded NOT DERIVED, each with its obstruction named (the bridge
  premise G1 does not supply; the fitted-form refusal of C090-9).
  Mechanical completeness per this task's acceptance holds on the
  record's face. T202 — the audit by a worker other than the
  deriver, which declares the G2 outcome — remains open.
- [x] **T202 — The derivation audit and the G2 outcome.** A worker
  other than the deriver re-walks every step of every candidate:
  premises traced to the G1 document or D1–D3 (a physics premise
  anywhere fails the candidate under D-090-3, with the step named);
  the falsifier tested for form (a record the system admits,
  recognizable if observed); class-level form confirmed (no
  corpus-fitted regularity wearing the label). The stage outcome is
  declared on the audit: DERIVED (at least one candidate completes)
  or NOT YET (the obstruction record names, per candidate, where the
  chain broke and what would have to change). Broken candidates are
  not repaired inside the audit; a repair is a new attempt recorded
  as such and audited in turn. Claims: C090-8..11. Acceptance:
  **human-as-oracle** (the stage reviewer against the audit record).
  *This does not establish:* that a DERIVED outcome makes the
  condition important — the audit settles soundness and form; the
  outcome record (T301) states the bite plainly, including if it is
  small.
  *Status 2026-11-04:* the audit's input has landed — the
  derivation record of T201 (`records/g2-derivation.md`, on branch
  `feat/090-s2-g2-derivation`), carrying two completed chains (each
  with a derivation-provenance self-audit and labeled boundaries
  for the audit to press) and two candidates recorded not derived
  with their obstructions named. The audit itself, and the DERIVED
  / NOT YET declaration on it, remain open: they are a worker
  other than the deriver's act, per this task's text and the
  plan's separation rule.
  *Completed 2026-11-04:* `records/stage-s2-audit-record.md`
  — the audit executed by a worker other than the deriver
  against the frozen G1 document v1.1 (hash recomputed and
  matched before auditing). Five attacks, each driven to a
  verdict: premise tracing NOT SUSTAINED (every premise of
  both chains traces to D1–D3 or the frozen G1; no physics
  premise anywhere); Candidate 1's strength NOT SUSTAINED
  (the variation holds for an arbitrary state in all three
  dimensions; the Class II counted form recounted
  independently, 0 of 3; the falsifier admissible,
  recognizable, and observable in D4's form);
  Candidate 2's bite NOT SUSTAINED as a refutation of
  derivedness, with its strength finding confirmed (the
  recorded profiles recomputed first-hand: M77 1,669 /
  5,361 / 64, max 541, one hapax; ICIT 4,410 / 14,213 /
  713, max 527; CISI 179 sides, 1,003 tokens, 182 codes);
  the refusals NOT SUSTAINED (Candidate 3's bridge premise
  verified absent; Candidate 4 verified as Candidate 2's
  corollaries); form NOT SUSTAINED. **G2 outcome declared:
  DERIVED** — Candidate 1 (the non-certification
  condition) and Candidate 2 (the recorded-profile
  condition, declared at consistency strength, its
  excluding power being consistency's under the frozen
  projection) survive with their D4 falsifiers stated;
  Candidates 3 and 4 stand NOT DERIVED with their
  obstructions verified. No candidate was repaired inside
  the audit.

## Stage 3 — Outcome record + report (PR: feat/090-s3-outcome)

- [x] **T301 — The outcome record.** Per-claim dispositions for
  C090-1..16 (discharged / carried, with the evidence pointer for
  each); the per-stage outcomes in spec.md's vocabulary (G1: STATED
  or NOT YET with the missing element; G2: DERIVED or NOT YET with
  the obstruction); the study-level outcome (INSTANTIATES-path /
  ANALOGY with the metaphorical element named / NOT YET with the
  missing work stated); the G3–G5 sequencing note (commissioned in
  principle, not started; what this outcome implies for them, as
  assessment); and the explicit statements that no claim's
  status/stage/score moved, that no convergence step was taken or
  implied, and that the formal verdict over the full G1–G5 bar
  belongs to the independent reader under the judging protocol, not
  to this study. Claims: C090-12..16. Acceptance: **human-as-oracle**
  (the stage reviewer against the stage records).
  *This does not establish:* the verdict on the domain — it
  establishes what this study produced and what it did not, which is
  the input the reader's verdict and the registry entry are made
  from.
  *Completed 2026-11-04:* `records/study-outcome-2026-11-04.md`
  — G1: **STATED** (the G1 document frozen at v1.1, SHA-256
  4f2018f4…; the absolute audit's NONE-NEEDED disposition sustained
  under the T102 adversarial pass, its sustained defects F1–F9 all
  answered by revision at the freeze); G2: **DERIVED** (declared on
  the T202 audit: Condition 1, the non-certification condition, at
  full strength; Condition 2, the recorded-profile condition, at
  consistency strength; Candidates 3 and 4 NOT DERIVED with their
  obstructions verified); study-level outcome:
  **INSTANTIATES-path** in spec.md's defined vocabulary — the
  formal INSTANTIATES verdict over the full G1–G5 bar is the
  independent reader's and is not issued here. Per-claim
  dispositions for C090-1..16 are recorded in the outcome record at
  the strength each stage's evidence supports; no claim's
  status/stage/score moved (the study's only ledger change remains
  the Stage 0 intake append), and no convergence step was taken or
  implied.
- [x] **T302 — The report to the VEXA chat.** The outcome (or, if a
  stage could not run, the blocker) delivered to the VEXA chat for
  the improvement registry: the per-stage outcomes, the study-level
  outcome in the skeleton's vocabulary — ANALOGY or NOT YET stated
  in those words when they are the outcome — and the evidence
  pointers. The send is recorded in the outcome record (date,
  destination, text or its hash). Claims: C090-16. Acceptance:
  **test** (the recorded send matches the outcome record's outcomes;
  no outcome word differs between the two).
  *This does not establish:* that the registry entry closes the
  generalization question — it records this study's outcome; the
  follow-on stages and the reader's verdict stand after it.
  *Completed (report text) 2026-11-04:* the report text is
  committed at `records/vexa-report-2026-11-04.md` (SHA-256
  bd432314b46f833026342f8163e431f8188fb453bd1b78c80d2d09cc682860c1)
  and is recorded in the outcome record with its destination (the
  VEXA chat) and hash; its outcome words match the outcome
  record's exactly (G1 STATED; G2 DERIVED; study level
  INSTANTIATES-path, with the formal verdict expressly reserved to
  the independent reader). Delivery to the VEXA chat is the parent
  seat's act on this PR's merge, per the commission's routing; the
  claim C090-16 stands open on exactly that delivery leg until the
  send lands, and the outcome record says so.
