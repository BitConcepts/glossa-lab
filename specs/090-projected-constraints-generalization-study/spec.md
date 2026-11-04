# Feature Specification: Spec 090 — Projected-Constraints Generalization Study (G1+G2 Attempt)

**Feature Branch**: `090-projected-constraints-generalization-study`
(build stages); this package lands on `feat/090-spec-package`
**Created**: 2026-11-04
**Status**: Draft package — awaiting the owner's block approval (Stage 0, T003)
**Input**: The owner's direct order of 2026-11-04 ("do both in order,"
item 1), delivered to this chat by the VEXA chat: the generalization
study is commissioned, with Glossa as the test bed, as a registered
study in this program under its own spec process. The skeleton and
the bar come from AXIOVEX/vexa (commit 88839493):
`docs/GENERALIZATION-SKELETON-2026-11-04.md` (definitions D1–D6, the
skeleton S1–S5, the judging protocol, Appendix B) and
`docs/GENERALIZATION-SCOPING-NOTE-2026-11-04.md` (the G1–G5 bar).
Byte-identical copies, with hashes, are in this package's `records/`
(see `records/commission-and-grounding-2026-11-04.md`).
**Evidence of record**: the grounding census in
`records/commission-and-grounding-2026-11-04.md`, counted and read
first-hand from the repo at origin/main `c643500b` on 2026-11-04: the
claims ledger (907 lines, 876 claim entries, falsifier on 867/876);
the anchor register (287 records, strict 94, 44 pending validation);
the corpus files (M77 flat file: 1,669 inscriptions / 5,361 tokens /
64 distinct signs, SHA-256 878fd223…; the ICIT frame's 713 distinct
codes); the signary's measured frame-dependence (Spec 077's frozen
557-sign population, 399/557 witnessed against a 502 bar); the
executable matrix standing (ledger → generated matrix, 876 × 644,
1,399 cells → generated maps; gate classes V1–V10, the gate never
writes; settling under glossa-settle-1); and Specs 076/078, the
program's adjacent projected-constraint work, both frozen 2026-10-26
and both closed negatively on their own terms.
**Predecessors**: Spec 086 (the Winning Combination adoption — the
ledger, the generated matrix and maps, the gate: the D6 element this
study finds standing), Spec 087 (registry discipline), Spec 088 (the
full-picture map and gap register; the adoption-intake discipline
this spec's C090-13 repeats), Spec 089 (run-scoped results — the
program's run hygiene over the same substrate). Framework peers: the
RCPH program, whose physics instantiation is the skeleton's
calibration case (the skeleton's Appendix A) and whose results are
*not* evidence for this domain.

## Purpose

Projected Constraints is, today, a physics framework. The owner's
question — the question the VEXA chat's scoping note formalized and
the skeleton document states — is whether there is a
domain-independent skeleton inside it, of which the physics is one
instantiation, and what would *prove* that rather than merely
suggest it. The bar the scoping note sets is G1–G5, all five, or the
verdict is analogy.

This study is the second-instantiation attempt for the decipherment
domain, scoped to the first two items of the bar:

- **G1** — the domain's records, projection rule, and (if any)
  primitive absolute defined in writing before any result, with the
  same rigor as the physics charter, including what the records
  provably cannot identify.
- **G2** — at least one necessary condition derived in the domain by
  the skeleton's machinery (not imported from physics), stated with
  its falsifier.

The decipherment domain is the honest test bed for this, per the
scoping note's own assessment: Glossa already runs the executable
matrix and the ledger discipline, its anchors are records with
sources and coverage, and it has *not* stated a projection rule, a
primitive absolute, or a necessary condition in the skeleton's
terms. G1 and G2 are open here. Close enough to attempt; distinct
enough (texts, not spacetime) that success would mean something.

This is a research study, not a build. It produces documents,
derivations, and records — the G1 document, the G2 derivation record
(or its obstruction record), and the outcome record — and no
machinery. Its success conditions are the skeleton's, not the
program's usual ones: a clean NOT YET, with the missing work named,
is a complete and publishable outcome of this study, recorded in the
VEXA improvement registry either way.

## The two study questions

- **Q1 (G1).** Can Glossa's record system, projection rule, and
  primitive absolute (or the proof that none is needed) be stated in
  the skeleton's terms — D1, D2, D3 — in a single document written
  before results, including an explicit account of what the records
  provably cannot distinguish? The document must satisfy the judging
  protocol: an independent reader receives only the skeleton, this
  document, and the domain's records, and the document therefore
  contains definitions and provenance rules only — no conclusions,
  no outcome language, nothing the reader would have to take on the
  domain team's word.
- **Q2 (G2).** Can at least one necessary condition be *derived* in
  the decipherment domain by the skeleton's machinery — proceeding
  from D1–D3 and the projection rule as stated in the G1 document,
  in D4's form (a statement holding of every state in every
  projection-equivalence class consistent with the records), carrying
  its falsifier (a record the framework declares impossible, whose
  observation would refute the derivation's application)? A condition
  fitted to the observed corpus, or imported from the physics
  instantiation by analogy, does not answer Q2.

## Scope — what this spec does

- **S0 — Adoption.** The package lands in the repo as
  `specs/090-projected-constraints-generalization-study/`; the C090
  bundle enters the ledger through the sanctioned intake; the
  generated layers regenerate over the grown ledger, exactly the
  Spec 087/088/089 adoption shape.
- **S1 — The G1 document.** One document, drafted from the records
  (Appendix B items 1–3): the record system's definition with
  provenance rules; the projection rule, including the
  cannot-distinguish account grounded in the program's actual
  underdetermination record; the primitive absolute named (with the
  at-most-one audit), or the none-needed proof. The draft then faces
  an internal adversarial review pass by a separate worker, attacking
  named questions: is a second absolute smuggled in? is the
  "projection" a rule or a metaphor? is every indistinguishability in
  the cannot-distinguish account tied to a record? The document is
  revised against the attack record and frozen as the study's G1
  deliverable.
- **S2 — The G2 derivation.** Candidate necessary conditions are
  derived from the G1 document's stated projection, with the
  derivation chain inspectable step by step, and each candidate's
  falsifier stated in D4's form. The derivation is attempted
  honestly: if no candidate's chain completes, the stage records
  NOT YET with the obstruction named (which premise fails, which
  step does not follow) — a failed derivation is a result, not a
  defect of the stage.
- **S3 — Outcome record + report.** A closeout record states the
  per-stage outcomes and the study-level outcome in the skeleton's
  vocabulary, with evidence pointers; the outcome (or the blocker)
  is reported to the VEXA chat for the improvement registry, as the
  commission requires. G3–G5 sequencing is noted as the follow-on
  the same commission holds in principle; this spec does not start
  them.

## Non-goals (explicit)

- **G3, G4, G5 are not attempted.** No separator is computed for G3
  credit; no gate instance is staged for G4 credit; no reproduction
  package is assembled for G5. Standing instances in the program's
  history (the gate's refusals, the matrix's reproducibility) may be
  cited as program history; they are not this study's evidence for
  G3–G5 (C090-15).
- **No machinery is built.** No code, no gate class, no registry.
  The study writes documents and records only.
- **No claim about the Indus script changes.** No existing claim's
  status, stage, or score moves as a consequence of any stage; the
  study's total ledger diff is its adoption intake append (C090-13).
  The program's standing position — the Indus script is not
  deciphered — is untouched, and nothing in this study is a
  decipherment claim or evidence for one.
- **No convergence step.** This study does not enter the program
  into VEXA convergence Stage 1, does not change the program's
  stack, and is not evidence in any convergence dashboard. It is a
  study *about* the skeleton, run beside the program's own work
  (C090-14).
- **Specs 076/078 are not reopened.** Their frozen records and
  negative verdicts stand. They are cited as the adjacent prior work
  they are — on their own terms — not re-run, not re-argued, and not
  presented as skeleton-instantiation attempts (they were not).
- **The physics is not evidence.** The RCPH instantiation is the
  skeleton's calibration case. No physics result (no F0 theorem, no
  separator constant, no identifiability result about causal sets)
  is a premise in any derivation under this spec (C090-8).

## The judging protocol, as binding on this study

The skeleton's protocol governs how the study's products are
written, because it governs how they will be read:

- The **G1 document** is written for a reader who holds only the
  skeleton, the G1 document, and the records. It therefore carries
  definitions, provenance rules, and cited record pointers — and no
  conclusions (C090-7). Anything the study concludes lives in the
  derivation record and the outcome record, which are separate
  artifacts the protocol's reader does not receive as part of G1.
- The study does **not** judge itself INSTANTIATES. The verdicts
  belong to the independent reader under the protocol. The study's
  outcome record states what was produced and what was not, in the
  vocabulary below; the formal verdict over G1–G5 as a whole cannot
  exist until G3–G5 are attempted, and this study says so.

## Outcome vocabulary

Per stage:

- **G1: STATED** (the G1 document stands frozen: record system,
  projection rule with its cannot-distinguish account, and the
  absolute disposition, each in the skeleton's terms) — or **NOT
  YET**, with the missing element named (e.g., the projection could
  be stated only as a metaphor; the absolute audit could not close).
- **G2: DERIVED** (at least one necessary condition whose derivation
  chain completes from the G1 document's definitions, with its D4
  falsifier stated) — or **NOT YET**, with the obstruction named.

Study level, in the skeleton's terms:

- **INSTANTIATES-path** — G1 STATED and G2 DERIVED, with G3–G5
  unattempted: the instantiation question stays open and the path
  to the full bar is unobstructed by anything this study found.
  (This is not the verdict INSTANTIATES, which requires all five.)
- **ANALOGY** — some S element holds only metaphorically in this
  domain, and the outcome record names which and why (e.g., the
  "projection" cannot be made a rule; two absolutes are required,
  which under D3 means the domain instantiates something else).
- **NOT YET** — a named element is unproven for a named reason that
  further work could close (an incomplete derivation, an unclosed
  audit), with the missing work stated.

ANALOGY and NOT YET are publishable outcomes, recorded either way,
per the skeleton. The study fails only if it closes without an
outcome record, or states its outcome in terms the skeleton does
not define.

## Decisions

- **D-090-1 — The G1 document is a single standalone artifact in the
  spec's records.** Options: (a) one document at
  `specs/090-projected-constraints-generalization-study/records/g1-document.md`,
  versioned only by recorded amendment acts, written to be handed to
  the protocol's reader as-is; (b) the G1 content distributed across
  stage records; (c) a published surface (tracker page, preprint).
  *Recommendation: (a).* The judging protocol needs a bounded
  artifact a reader can be handed; (b) makes the G1 act unfindable,
  and (c) is a publication act that belongs to the owner after the
  study, not to a stage. Amendments to the frozen G1 document are
  new versions with their acts recorded — the document the G2
  derivation cites is always identifiable by hash.
- **D-090-2 — The absolute question is decided by audit at S1, not
  pre-decided by this package.** The G1 stage must enumerate the
  candidate absolutes the program's practice actually uses (the
  candidate set in claim C090-6 is the starting list, not the
  answer) and dispose of each: record-relative, derived, or the one
  named absolute. Three outcomes are all legitimate: exactly one
  absolute named; a none-needed proof (every candidate shown
  record-relative or derived); or the finding that the domain
  requires two — which is recorded as a skeleton mismatch (under D3
  the domain then instantiates something else), feeding the
  study-level ANALOGY outcome, not a forced fit. *Recommendation:
  adopt the audit rule; the owner is the oracle if the S1
  adversarial pass sustains a split the drafters cannot close.*
- **D-090-3 — Derivation provenance: from the stated projection
  only.** A G2 candidate counts as derived only if every step of its
  chain follows from D1–D3 and the G1 document's stated projection
  rule and definitions. The physics instantiation may be named as
  the *occasion* for a candidate (the analogy that suggested it) but
  never as a premise; a chain that needs a physics premise is
  recorded as not derived, with the step named. *Recommendation:
  adopt.* Without this rule, G2 degenerates into analogy-hunting,
  which is exactly what the bar exists to exclude.
- **D-090-4 — The outcome is reported to the VEXA chat as a study
  deliverable, whatever it is.** The S3 report carries the per-stage
  outcomes, the study-level outcome in the skeleton's vocabulary,
  and the evidence pointers, for the improvement registry —
  including when the outcome is ANALOGY or NOT YET. *Recommendation:
  adopt* (the commission names the report; the skeleton requires
  the outcomes recorded either way).

## Requirements (summary; the claims in claims.md are the normative text)

- **FR-090-01 — The G1 document exists, single and standalone** (S1;
  C090-1). One document in the spec's records states the record
  system, the projection rule, and the absolute disposition, written
  before any G2 result exists.
- **FR-090-02 — The record-system definition covers the actual
  record classes, with provenance rules** (S1; C090-2). Corpus
  records, anchor records, and ledger claim lines are each defined
  as record classes with their provenance rule and their population
  counted from the records; records that break a stated rule (the
  register's no-validation-record entries) are accounted for by the
  definition, not passed over.
- **FR-090-03 — The projection rule is a rule** (S1; C090-3). It
  defines the candidate state and maps a state to the records it
  would produce, precisely enough that projection-equivalence of two
  named states is decidable under the stated rule.
- **FR-090-04 — The cannot-distinguish account is explicit and
  record-grounded** (S1; C090-4). Every asserted indistinguishability
  cites the record or count that grounds it (frame-dependent
  signary; corpus-attested signs with no anchor coverage; the 44
  pending-validation anchors; completions differing only outside
  the surviving records).
- **FR-090-05 — At most one primitive absolute, or none** (S1;
  C090-5). The G1 document names exactly one absolute with the audit
  showing every other absolute-looking input record-relative or
  derived from it, or proves none is needed. This package does not
  prejudge which outcome obtains.
- **FR-090-06 — The absolute disposition is reached by audit** (S1;
  C090-6). The candidate absolutes the program's practice uses are
  enumerated and each is disposed of on the record.
- **FR-090-07 — The G1 document carries definitions only** (S1;
  C090-7). No outcome claims, no G2 material, no instantiation
  verdicts — per the judging protocol.
- **FR-090-08 — The G2 derivation proceeds from the stated
  projection** (S2; C090-8). Every step follows from D1–D3 and the
  G1 document; no physics result is a premise.
- **FR-090-09 — The necessary condition is stated over equivalence
  classes** (S2; C090-9). D4's form: every state in every
  projection-equivalence class consistent with the records — not a
  regularity fitted to the observed corpus.
- **FR-090-10 — The necessary condition carries its D4 falsifier**
  (S2; C090-10). A named record, of a kind the record system admits,
  whose observation would refute the derivation's application.
- **FR-090-11 — A failed derivation is a NOT YET with its
  obstruction named** (S2; C090-11). No weaker statement is
  substituted and called derived; no gap is presented as a step.
- **FR-090-12 — The executable-matrix element is accounted as it
  stands** (S1, S3; C090-12). The study's account of D6/S5 cites the
  standing machinery exactly as it operates and credits this study
  with none of it.
- **FR-090-13 — The ledger does not move beyond the intake append**
  (all stages; C090-13). No claim's status, stage, or score changes;
  nothing about the script is claimed.
- **FR-090-14 — No convergence implication** (all stages; C090-14).
  The study is not a convergence step and enters the program into no
  stage.
- **FR-090-15 — G3–G5 remain unattempted by this spec** (all stages;
  C090-15). Program history may be cited as history, never as this
  study's G3/G4/G5 evidence.
- **FR-090-16 — The outcome is recorded and reported either way**
  (S3; C090-16). Per-stage outcomes and the study-level outcome in
  the skeleton's vocabulary, with evidence pointers, in the closeout
  record; the report to the VEXA chat is delivered as a study
  deliverable.

## Governance

Claims first (this package's `claims.md` / `aee-claims.json`,
C090-1..16), assessed under the pinned AEE before any study task
starts (Stage 0, T002 — the assessment is in
`records/t002-aee-assessment.json`, its invocation and verbatim
outcome in `records/t002-note.md`). The owner's block approval of
this package (T003) is the ratification act for the spec and for
decisions D-090-1..4. Verdicts and citations follow program
doctrine: numbers only from records read first-hand; assessments by
actually running the assessor. The study's judgment calls are named
where they sit: the absolute disposition (D-090-2) is the study's
central one, and the owner is its oracle if the S1 adversarial pass
leaves it split. The spec ends with its outcome record (T302); the
formal INSTANTIATES / ANALOGY / NOT YET verdict over the full G1–G5
bar belongs to the independent reader under the judging protocol
and cannot be issued by this study — its outcome record states what
stands, in the vocabulary above, and stops there.
