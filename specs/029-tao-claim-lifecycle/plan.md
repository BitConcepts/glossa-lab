# Spec 029 — Plan

> ## PLAN — DRAFT, NOT FROZEN — 2026-10-12
>
> Written against the adjudicated spec: `spec.md` (claims
> F029-C01…C10, requirements FR-029-01…12), the owner's
> block ratification of OD-1…OD-6 in `adjudication.md`
> (2026-10-12, verbatim: "ratify all of these as a block
> and do it"), and the retroactive audit in `audit.md`
> with its `reclassification-ledger.json` (345 entries).
> This plan disposes of each §8 decision by citing that
> record, per spec §6(d) — never by default. The freeze,
> and every merge in the implementation sequence, remain
> owner-gated.
>
> **Scope update (2026-10-12):** the audit's §9 items
> **D-A, D-B, D-D, and D-E entered scope** via the
> owner's ratification the same day ("do all this").
> They are planned as Workstreams 5–7 and the Workstream
> 2 revision below. **D-C (README errata) did not enter
> this plan**: it is executed separately as an immediate
> errata PR and appears nowhere in `tasks.md`.

**Governing documents:** `spec.md`, `claims.json`,
`adjudication.md`, `assessment.md`, and `audit.md` in
this directory; Spec 026's framework artifacts (evidence
counted by origin group); Spec 028's lifecycle records
(house format precedent); the Glossa constitution; and
governance rules H2, H6, H13, H15/H23, and H21.

**Tooling record:** specify CLI 1.0.10 (setup and
extension management only — see §8); AEE extension
v1.1.0; evaluator extension v1.0.0; AEE package 1.0.4
from the Glossa venv on PATH for any AEE invocation
(the spec-kit venv carries 1.0.2; every invocation
states and pins its PATH, per the Spec 028 precedent).

## 0. The stage invariant (D-E, engraved)

**A stage is always recomputable from the record's
evidence. The stored stage is a cache with provenance,
never an assertion.** Every stored stage therefore
carries `stage_source` (the computation or record it
derives from: the reclassification ledger entry, the
bundle-minimum computation, or a transition-service
history entry) and `stage_as_of` (when that derivation
was made). A stored stage lacking either field, or one
that disagrees with its recomputation, is a defect —
Phase G checks for exactly this in CI. This invariant
governs Workstreams 1, 2, 5, and 6 and every phase that
touches a stage.

## 1. Lifecycle sequence (this spec)

1. **Constitution check** — §5 below; performed at spec
   drafting and re-performed for this plan.
2. **Specify** — done: `spec.md` + `claims.json`
   (10 governed claims), claims-first, hand-authored in
   house format (deviation recorded in spec §9).
3. **Adjudication** — done: OD-1…OD-6 ratified as a
   block, `adjudication.md` (2026-10-12).
4. **Retroactive audit** — done: `audit.md` +
   `reclassification-ledger.json` (345 entries: 336
   staged claim items + 9 grouped/surface records),
   merged with the freeze of the spec on main
   (`03802571`).
5. **Scope ratification** — done: audit §9 items D-A,
   D-B, D-D, D-E ratified 2026-10-12 (banner above);
   D-C separated as an immediate errata PR.
6. **Plan + tasks** — this document and `tasks.md`.
7. **AEE hooks** — AEE assess plus evaluator-contract
   pass over spec, plan, and tasks, per the house flow;
   outcomes recorded under `aee/`. A `fail` outcome
   blocks the freeze until its recovery record is
   complete (Spec 028 precedent).
8. **Freeze** — `freeze.md` + `freeze.json` (framework026
   digest) + freeze tests in `backend/tests/`, freezing
   this plan's design decisions (§2), the migration
   contract (§2.2), and the display dispositions (§2.3).
   The freeze PR merges only on the owner's order, with
   CI verified from the run's own conclusion and job
   logs.
9. **Implementation** — Phases A–J (§3), each its own
   PR, each merge owner-gated, CI green verified from
   run conclusions before any merge. No phase begins
   before the freeze merge.
10. **Closeout** — full backend suite and foundation
    check on merged main (H21); ledger-vs-live
    reconciliation re-run and matched; the anchors'
    pre-existing fields verified unchanged (additive
    keys excluded, §2.2); PRED register untouched
    verified; closeout record in this directory;
    entries in both program ledgers.

## 2. Design summary

### 2.1 Workstream 1 — Data model and AEE wiring
(FR-029-01…07, FR-029-11, FR-029-12; claims C01–C05,
C08, C09)

- **Stage axis (FR-029-01).** The extracted-claims
  record shape and the anchor record shape each gain an
  additive lifecycle representation: `stage` (one of
  created, checked, explained, accepted, digested —
  OD-4: Tao's names verbatim, in data and displays),
  `stage_source` and `stage_as_of` (§0), and
  `stage_history`, an append-only list of
  {from_stage, to_stage, actor, timestamp,
  evidence_refs, reason}. Existing fields keep their
  meanings; the stage is a new axis, never a rename of
  `claim_status` or of confidence (spec §6(b)).
  `aee_core.claim_from_glossa` maps the stage axis as a
  distinct object — it is not folded into AEE
  `ClaimStatus` and does not alter score propagation.
  `GET /claims`, `GET /claims/aee-scores`, and the
  anchor surfaces serialize stage and lane-1 score as
  distinct objects.
- **Transition enforcement (FR-029-02; C02).** A single
  transition service is the only writer of stage
  changes. Legal moves: one step forward along
  created → checked → explained → accepted → digested,
  or backward to any earlier stage with a recorded
  reason (demotion is a normal, publishable event).
  Automated actors (extraction, scoring, the research
  loop, batch jobs) are allowlisted to `created` and
  `checked` transitions only; any automated attempt
  above `checked` fails closed. Transitions above
  `checked` additionally validate, fail-closed: a named-
  human actor (a process name never validates), and the
  gate records required by FR-029-06/07. Every
  transition the service writes updates `stage`,
  `stage_source` (the history entry), and `stage_as_of`
  together.
- **Risk flag (FR-029-03; P3).** `verified_unexplained`
  is a computed, queryable API field: true when the
  claim's lane-1 state includes a SUPPORTED-class
  verdict or a high score band while its stage is below
  `explained`. The audit's 105 flagged items are the
  regression fixture (§2.2).
- **Bundles (FR-029-04; C03).** A decipherment claim is
  a parent record plus sub-claim records of kinds
  `reading_soundness`, `scholarship_accounting`,
  `attribution`, and `explanation_intelligibility`,
  each with its own evidence list, falsification
  condition, stage, and trail. Once a bundle exists,
  the parent's stage is computed — minimum of sub-claim
  stages, then the attribution cap — and the stored
  parent stage is that computation's cache
  (`stage_source` = the bundle-minimum computation).
  Bundle machinery is built in this workstream;
  decomposition of individual anchors into bundles
  proceeds as sub-claim records are authored (an
  ongoing lane-2 work queue, not a migration
  deliverable — see §2.2 for how migrated stages and
  later decomposition interact).
- **Attribution sub-claim (FR-029-05; C05; OD-3).** The
  template requires: (i) prior readings accounted for,
  each with a resolvable citation; (ii) the
  completeness basis — a search record (corpora and
  literature searched, date, searcher); (iii) a contest
  state in {uncontested, contested} plus, when
  contested, a contest record (who contests, on what
  evidence, when). **Contested** means an active,
  evidenced dispute: while contested, the contest
  renders wherever the parent renders, and the parent's
  stage is capped at `checked` (OD-3). **Unexamined**
  attribution carries no special cap; the bundle
  minimum rule applies.
- **Explanation record (FR-029-06; C04; OD-2).** Fields:
  named human author; artifact URI; stored content
  hash of the account; the venue where challenges are
  filed and answered; an AI-assistance disclosure field
  (constitution §VI). The `accepted` transition
  requires a valid explanation record (for bundles: for
  the parent's `explanation_intelligibility` sub-claim
  at minimum). Authorship validation rejects any
  non-human or process actor: per OD-2 an AI system may
  draft an account but may **never** be the named
  human; internal and external human authors carry the
  same weight at this gate.
- **Digestion record (FR-029-07; C04; OD-2, OD-5).** The
  `digested` transition requires a digestion record in
  exactly one of the three OD-5 classes, each with
  resolvable references: (i) independent scholarly
  **reuse** in work not authored by the program;
  (ii) a published substantive **challenge** answered in
  a durable record (the exchange is the record);
  (iii) an independent **citation engaging the
  mechanism**, judged by a named reviewer at intake
  with the rationale stored on the record. Every class
  requires engagement by at least one scholar
  independent of the program (not an author of the
  claim, not program staff) — an independence field is
  validated fail-closed. **Adverse digestion:** an
  unanswered refutation is recorded as a digestion
  record of adverse kind; it flags the claim contested
  and pulls the parent back under the bundle rule via a
  recorded demotion transition.
- **Priority register (FR-029-11; C08; OD-6).** An
  intake path (API + record store) registers an
  external scholar's reading on record completeness
  alone — no score, stage, or verdict is required or
  implied — and the entry's credit display is invariant
  under later program assessment. Per OD-6 the
  registration is **public at intake**: claimant name,
  server timestamp, and a SHA-256 hash of the reading
  are published immediately; the reading's content is
  stored sealed and is revealed only when the claimant
  publishes or at a claimant-chosen reveal date
  (default 24 months from registration, extendable
  once — the extension is itself a dated record).
- **Trails (FR-029-12; C09).** Every verdict record and
  every stage-transition record serializes: evidence
  references with origin groups, the falsifier state at
  decision time, the actor (named human or named
  process), and the timestamp. A per-claim trail view
  is exposed from the claims API. Completeness is
  enforced by the claims test suite in CI (Workstream
  4), not by review memory.

### 2.2 Workstream 2 — OD-1 re-staging, executed EARLY
(OD-1; D-E; audit ledger as the single source of truth)

Per D-E this migration is an **early gated phase** —
immediately after the stage-axis core (Phase A) — not
the last step of the implementation. It is mechanical:
it exercises judgment nowhere, because the audit ledger
is its single source of truth.

- **Form.** A one-time, dated migration (a script under
  `backend/scripts/` plus its run record), executed
  once under the freeze. Its input is the frozen
  `reclassification-ledger.json` (345 entries); its
  output is, per record: `stage`, `stage_source`
  (naming the ledger and the entry), `stage_as_of`
  (the migration date), and an initial `stage_history`
  entry naming the migration, the date, and the ledger
  entry as its evidence ref. It is a reclassification
  event, not an edit: every pre-existing field is
  untouched.
- **Coverage.** The 336 staged items: 287 anchors
  (193 created / 94 checked), 31 extracted claims
  (21 created / 10 checked), 5 live PRED-2026 items
  (3 created / 2 checked), 3 hypothesis-model records
  (created), and 10 study-headline entries (checked).
  The ledger's 9 grouped/surface records are not record
  writes; they are dispositions consumed by Workstream
  3. Stage = highest stage whose evidence exists in
  the record (OD-1), which is exactly the rule the
  audit applied — the migration replays the ledger, it
  does not re-judge.
- **Recompute proof.** The migration's reconciliation
  (see Verification) *is* the §0 invariant demonstrated
  for the ledger-stamped population: stages recomputed
  from the live stores, via the audit's rule, equal the
  stored caches and their `stage_source` provenance.
- **Additive-only guarantee.** For the anchors file the
  migration asserts, in its run record, a canonical
  comparison of every pre-existing field before and
  after (byte-identical excluding the additive stage
  keys) plus before/after SHA-256 of the file. The
  file's hash changes by design under OD-1; what must
  not change is any pre-existing content.
- **Risk flags.** The migration also writes the initial
  `verified_unexplained` state for the audit's 105
  flagged items (the strict 94 anchors, the 8
  supported-class claim records, and the SUPPORTED
  study headlines F1, F3, G1), as computed by the
  FR-029-03 rule.
- **Interaction with bundles.** Migrated stages stand —
  as ledger-sourced caches — until a bundle is authored
  for the record; from the first bundle transition
  onward the computed-minimum rule (FR-029-04) governs,
  `stage_source` changes to the computation, and any
  resulting demotion is recorded as a normal dated
  transition with the decomposition as its reason.
- **Safety.** Dry-run mode first, emitting a
  reconciliation report; the live run proceeds only on
  a clean dry run. The migration is idempotent: a
  second run is a no-op and says so. A pre-migration
  snapshot of every touched store is taken and named
  in the run record.
- **Verification (the migration's acceptance test).**
  (a) Foundation check: 0 failures (H21; baseline
  40 OK / 0 fail / 8 warn); (b) full backend suite
  green; (c) ledger-vs-live reconciliation: per-class,
  per-stage counts recomputed from the live stores
  equal the ledger's §3 table exactly (220 created /
  116 checked / 0 explained / 0 accepted / 0 digested),
  and the 105 `verified_unexplained` flags reconcile;
  (d) the additive-only assertion in the run record;
  (e) every stamped record carries `stage_source` and
  `stage_as_of`.

### 2.3 Workstream 3 — Display fixes (FR-029-08…10;
C06, C07; audit §5 P5/P6)

Ordered by public visibility (OD-1), in two steps:

- **Step 1 — Withdrawals (no dependency on the
  migration; may ship first).**
  - `DeciphermentPanel`: the "**{totalAnchors} signs
    deciphered**" headline and the confidence-led
    layout are withdrawn (audit §5-P5.1). The
    replacement summary leads with the program's
    standing position and the lifecycle stage summary
    under lane-2 labels, with the OD-4 one-line legend;
    no summary position carries a score, band, mean, or
    count as a standing claim (FR-029-08).
  - Dashboard API (`backend/glossa_lab/api/
    dashboard.py`): `sa_aggregate` and
    `fully_decoded_pct` / `n_fully_decoded` are removed
    from the served payload, and the panel stops
    consuming them (audit §5-P5.2). The underlying data
    files are untouched — history is preserved in the
    record, withdrawn from the surface.
  - `GET /claims/aee-scores`: `mean_propagated_score`
    is withdrawn from the summary position
    (audit §5-P5.3). If a program-level lane-1
    diagnostic is retained anywhere, it appears only
    inside a block labelled as checking-stage (lane-1)
    diagnostics, with the checking method and falsifier
    context — never as a headline figure.
  - Score bands render only inside lane-1 checking
    presentations, alongside the score and method —
    never beside a claim status where band and status
    can contradict (audit §5-P5.4).
- **Step 2 — Lane-separated rendering (after the
  migration populates stage data).**
  - `IndusEvidenceView` and the claim/anchor surfaces
    render two distinct regions: a lane-2 region
    carrying the stage in Tao's verbatim names with the
    legend, and a lane-1 region carrying verdicts,
    scores, and extraction statuses in checking
    vocabulary only. Lane-1 badges lose stage colours
    and acceptance language; stage colours, if used,
    belong to the lane-2 region alone (FR-029-10).
  - Contested attribution renders on the parent
    wherever the parent renders (FR-029-05).
  - Every verdict display renders the verdict's
    `not_understood` statement with the verdict
    (FR-029-09). Verdict records lacking the field
    render as incomplete — visibly, not silently.
    Authoring `not_understood` text for existing
    verdict records is lane-2 human work queued by this
    step; the field ships required-for-new-records
    from Workstream 1.

### 2.4 Workstream 4 — CI and trail completeness
(FR-029-12; C09; supports C02, C05, C06; §0)

- **Trail completeness tests.** The claims test suite
  fails CI on any new verdict or stage-transition
  record missing evidence refs, origin groups,
  falsifier state, actor, or timestamp.
- **Stage-cache integrity tests (§0).** CI recomputes
  stages from record evidence for a sampled population
  (and for the full migrated population on demand) and
  fails on any stored stage that disagrees with its
  recomputation or lacks `stage_source` / `stage_as_of`.
- **Transition-rule tests with discriminating
  controls.** Each gate is paired with a control that
  must fail: an automated actor attempting an
  `explained` transition; a named-human transition
  above `checked` with no explanation record; an
  `accepted`→`digested` move whose digestion record
  lacks program-independent engagement; a bundle whose
  attribution is contested rendering above `checked`.
  A gate that cannot differentially fail marks the run
  INVALID, per the program's Spec 026 discipline.
- **Parent-stage computation tests.** Minimum-of-
  sub-claims, the OD-3 cap, and adverse-digestion
  pullback, each on synthetic fixtures.
- **Display regression guards.** Automated checks that
  the withdrawn strings and fields stay withdrawn
  ("signs deciphered" headline pattern absent from the
  frontend; `mean_propagated_score` absent from the
  scores endpoint's summary; `sa_aggregate` /
  `fully_decoded_pct` absent from the dashboard
  payload), and that lane labels and the stage legend
  are present on the claim surfaces.

### 2.5 Workstream 5 — Anchor annotation and schema (D-A)

Additive annotation of the canonical anchors file, and
a declared schema so its shape stops drifting (the
audit found **56 distinct field shapes** across the
287 records):

- **Explicit `validation_status` on every anchor.** No
  absent fields: where an anchor already carries a
  value it is preserved verbatim; where the field is
  absent, the value the record's own provenance
  establishes is made explicit. No anchor's tier,
  reading, basis, or existing value changes (D-A is
  annotation, never re-tiering).
- **Computed `strict_set` flag on every anchor.** The
  flag is computed by the existing strict-set rule
  (the Phase-108 provenance register + the Phase-109
  rule — the same join the audit used to reproduce
  **94** exactly), and the rule's identifier and
  version are recorded with the flag (file-level
  metadata naming the rule and its version), so the
  flag is recomputable and strict membership becomes
  inspectable from the canonical file alone (audit
  §5-P8 defect 1). The annotation run reconciles:
  strict count = 94, and flagged composition matches
  the audit (90 HIGH + 4 MEDIUM).
- **Declared schema + CI validator.** A schema file
  declares the anchors file's shape (required core
  fields, the additive fields of this spec —
  stage/`stage_source`/`stage_as_of`/history,
  `validation_status`, `strict_set` — and which fields
  are optional). The annotation pass normalises the 56
  observed shapes additively into the declared shape;
  a CI validator then fails on any record whose shape
  is undeclared. The schema is the contract future
  writers code against.

### 2.6 Workstream 6 — Claim-store deduplication (D-B)

Merge, never delete — the unit of repair is the
2026-10-09 extraction batch the audit identified
(§5-P2: two propositions double-recorded from
different source documents):

- **Proposition inventory.** A fingerprint scan (below)
  over the claims store fixes the exact duplicate set
  at the phase's start; the audit's two known
  propositions are the expected minimum, and any
  further collisions are reported in the phase record,
  not silently absorbed.
- **Merge.** One canonical claim per proposition. The
  canonical record is the one with the fuller trail;
  every other record of the proposition is preserved
  as an **evidence instance** attached to the canonical
  claim — nothing is deleted. Stage and stage history
  (stamped by Phase D before this phase runs) are
  preserved: the canonical record keeps its stage, and
  each evidence instance retains its own stamped stage
  and history as part of its preserved record.
- **Origin-group counting.** A merged proposition's
  evidence counts its origin group **once**: the
  duplicate extraction no longer double-counts one
  source's evidence in the AEE wiring. Any resulting
  lane-1 score movement is recomputed, reported with
  its cause in the phase record (the in-depth numbers
  rule), and never smoothed.
- **Fingerprint at intake.** Extraction intake computes
  a **proposition fingerprint** — a hash over the
  normalised claim text (normalisation rules defined
  and frozen in the phase: case-folding, whitespace
  and punctuation normalisation, as a minimum) — and a
  collision with an existing fingerprint **fails
  loudly**: intake stops with an error naming both
  records, rather than silently creating a duplicate
  or silently merging.

### 2.7 Workstream 7 — Foundation annotations (D-D)

The audit (§5-P8 defect 3) found Phase-48-era prose
riding unflagged inside a live foundation report, and
the status endpoint serving silent nulls while a valid
report sat on disk. Two steps:

- **Interim as-of labelling (ships early).** The
  current report's embedded `solid_claims` /
  `caveated_claims` annotations are stamped with a
  dated as-of label stating the anchor table they
  describe. The stale prose is labelled, not silently
  refreshed and not silently left.
- **Structural fix.** Annotations are **computed from
  canonical data at report-generation time** (the
  current anchors file and claim stores), and the
  generated report is stamped with the **SHA-256 of
  the anchors file** it was computed against — stale
  prose becomes impossible by construction, because
  the annotations regenerate with the report. The
  foundation status endpoint **serves the on-disk
  report or fails loudly**: a missing or unreadable
  report produces an explicit error response, never
  the silent nulls (`last_checked_at: null`,
  `verdict: null`, zero counts) the audit observed.

## 3. Sequencing and dependencies

| Phase | Content | Depends on |
|---|---|---|
| L | Lifecycle: constitution check, plan/tasks, AEE hooks | adjudication + audit + scope ratification (done) |
| F | Freeze of this plan's design + freeze tests | L; owner-gated merge |
| A | WS1 core: stage axis (+ `stage_source`/`stage_as_of`), history, AEE mapping, endpoint serialization, transition service, risk flag (FR-029-01…03) | F |
| D | WS2: OD-1 re-staging migration, EARLY per D-E — ledger replay, stamping, reconciliation | A |
| H | WS5: anchor annotation (explicit `validation_status`, computed `strict_set`) + declared schema + CI validator (D-A) | A, D (same file; runs after the migration's write) |
| I | WS6: claim-store deduplication + intake fingerprint (D-B) | D (stages stamped first; merges preserve them) |
| B | WS1 gates: bundles, attribution template, explanation + digestion records (FR-029-04…07) | A |
| C | WS1 registers: priority register, trail view (FR-029-11, 12) | A |
| J | WS7: foundation annotations — interim as-of label, then computed annotations + hash stamp + loud endpoint (D-D) | step 1: F; step 2: A |
| E1 | WS3 step 1: withdrawals (panel headline, dashboard fields, mean score, band placement) | F (independent of A–D; ships early on OD-1 visibility priority) |
| E2 | WS3 step 2: lane-separated rendering, contest display, `not_understood` rendering | D (stage data live) |
| G | WS4: CI completeness, stage-cache integrity, transition/display guards wired as gates | A–J, E (tests land with their phases; G wires the full gate set and proves the discriminating controls) |
| X | Closeout: suite + foundation on main, reconciliation re-run, ledgers, closeout record | all |

Each implementation phase is its own PR. Within every
phase, the gate order is: code → tests (including the
phase's discriminating controls) → foundation check +
full suite locally → branding sweep → PR → CI verified
from the run's own conclusion and job logs → owner-
gated merge. A phase that changes claim or anchor
records (D, H, I above all) additionally re-runs its
reconciliation before its PR is opened.

## 4. Principal risks and mitigations

| Risk | Mitigation in design |
|---|---|
| Migrated stage vs bundle minimum rule conflict (a migrated `checked` anchor later decomposes to sub-claims whose minimum is `created`) | §0 + §2.2: the migrated stage is a ledger-sourced cache; the computed rule governs from the first bundle transition, `stage_source` changes to the computation, and any demotion is a recorded, publishable event — the standard working as intended, not an inconsistency |
| Stored stage drifts from the evidence over time (the cache becomes an assertion by neglect) | The §0 invariant is enforced, not aspirational: `stage_source`/`stage_as_of` on every stage, and Phase G's CI recompute checks fail on disagreement |
| Anchors file hash changes break downstream byte-identity checks | OD-1 authorises the additive change; the migration records before/after hashes and a field-level canonical comparison; closeout re-verifies pre-existing fields, and every consumer of the old hash is inventoried in Phase D before the run. Phases D and H are sequenced so the file has one writer at a time |
| D-A normalisation mistaken for re-tiering | The phase's additive-only assertion covers tiers explicitly: annotation adds `validation_status`/`strict_set` and stage keys only; any tier, reading, or basis delta fails the phase |
| D-B merge changes lane-1 scores and is read as quiet re-scoring | Scores move only by removing a double-count the owner ordered removed; the movement is recomputed and reported with its cause in the phase record; verdicts and stages are untouched by the merge |
| `digested` gate gamed by program-adjacent "independent" engagement | Independence is a validated field (not an author of the claim, not program staff), fail-closed; class (iii) requires a named intake reviewer's stored rationale |
| Priority register becomes a de facto verdict surface | Registration issues on completeness alone; the credit display is invariant under later assessment (FR-029-11); no score/stage field exists on a register entry |
| Withdrawal step (E1) read as hiding results | Withdrawn figures remain in the frozen record and in git history with the audit's reasoning cited on the replacement surface; nothing is deleted from any record store |
| Extracted-claims store is regenerated wholesale by extraction batches (audit §2: the 31 claims are one 2026-10-09 batch) | Stage and history live on the claim record keyed by claim identity; the extraction path is an automated actor capped at `checked`; the D-B fingerprint makes a wholesale regeneration collide loudly on known propositions; a regeneration that would drop stage history fails the trail-completeness gate |
| Foundation endpoint's loud failure breaks a dashboard consumer | Loud is the requirement (D-D): consumers get an explicit error to handle, instead of nulls they currently render as a false "no data" state; the interim label ships first so the report's status is honest before the endpoint changes |

## 5. Constitution check

- **§I Provenance:** no new external data enters; the
  migration's only input is the frozen audit ledger,
  hash-asserted at freeze. D-A's `strict_set` flag
  derives from the Phase-108 register + Phase-109 rule,
  the program's own canonical artifacts.
- **§II Ledger:** every step is an append-only event in
  both program ledgers (`LEDGER.md`, `glossa-indus/
  LEDGER.md`); stage history itself is append-only;
  D-B merges preserve every record (nothing deleted).
- **§III Foundation gate:** the foundation check runs
  at the freeze, inside Phase D's verification, and at
  closeout (H21) — 0 failures required each time.
- **§IV Falsifiable claims:** `claims.json` governs;
  every requirement traces to F029-C01…C10; the
  transition gates carry discriminating controls
  (§2.4).
- **§V Public/private:** the priority register stores a
  claimant's contact for correspondence only; per H24
  no personal information or private correspondence
  enters the repo — register records live in the
  backend store, and any spec-side example is synthetic.
- **§VI AI disclosure:** present in spec, adjudication,
  audit, this plan, and tasks; explanation records
  carry their own AI-assistance disclosure field
  (FR-029-06).
- **§VII SDD:** sequential spec number; spec →
  adjudication → plan → tasks → freeze → execution;
  AEE hooks at each step (step 7 of §1).
- **§VIII Verification:** claims-register integrity,
  freeze-digest replay, migration reconciliation,
  schema validation, CI on every PR verified from run
  conclusions. No version string is introduced outside
  observed tool versions in the tooling record (the
  strict-set rule version recorded under D-A is the
  rule's own identifier, read from its source, not
  invented).

## 6. How this plan meets spec §6

- **(a) FR-029-01…12 without weakening any claim:**
  §2 maps every requirement to a workstream; the claim
  mapping is restated per phase in `tasks.md`.
- **(b) Additive migration:** §2.1 stage axis, §2.2
  additive-only guarantee, §2.5 additive annotation;
  existing fields keep their meanings throughout.
- **(c) Own freeze, discriminating controls,
  foundation check:** §1 steps 8–10, §2.4, §5 §III.
- **(d) §8 decisions disposed by citation:** OD-1 →
  §2.2 and Phase D; OD-2 → §2.1 explanation/digestion
  records and Phase B; OD-3 → §2.1 attribution cap and
  Phase B; OD-4 → §2.1 stage axis and Phase E2 legend;
  OD-5 → §2.1 digestion classes and Phase B; OD-6 →
  §2.1 priority register and Phase C. The §9 items
  dispose by the owner's 2026-10-12 scope ratification:
  D-A → §2.5 and Phase H; D-B → §2.6 and Phase I;
  D-D → §2.7 and Phase J; D-E → §0 and §2.2 (migration
  early, ledger as source of truth, cache invariant).
  Each cites `adjudication.md` (2026-10-12 block
  ratification) or the scope-ratification record in
  this plan's banner — never a default.

## 7. What this plan never does

Execute D-C (README errata — a separate immediate
errata PR owns it, not this spec); change any anchor
tier, reading, or basis (D-A annotates additively
only); delete any claim record (D-B merges only);
change any verdict as a lane-1 record; score
PRED-2026; modify the AEE library itself (this spec
governs the Glossa adapter, endpoints, records, and
surfaces only); re-stage any record outside the Phase
D migration or the transition service; treat a stored
stage as an assertion (§0); deposit or send anything
externally; or treat any task in `tasks.md` as an
execution authorisation by itself — the freeze merge
and each phase merge remain the owner's.

## 8. Tooling note (deviation recorded)

The specify CLI (1.0.10) provides project setup and
extension management only; it has no non-interactive
plan/tasks generation command, and the agent flow was
not available in the session that drafted this plan —
the same deviation recorded in spec §9 for the specify
step. This plan and `tasks.md` are therefore
hand-authored in the exact house format of Spec 028's
plan and tasks. The AEE + evaluator extension hooks
(after_plan / after_tasks) are carried as lifecycle
task L3 in `tasks.md`: if the hook pass runs, its
outputs are saved under `aee/`; if it cannot run
non-interactively, that outcome is recorded there
rather than silently skipped, and a `fail` outcome
blocks the freeze until its recovery record is
complete.

---

*AI disclosure: drafted by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI. The decisions this plan implements
are the owner's, recorded in `adjudication.md` and in
the 2026-10-12 scope ratification (D-A, D-B, D-D, D-E)
noted in the banner.*
