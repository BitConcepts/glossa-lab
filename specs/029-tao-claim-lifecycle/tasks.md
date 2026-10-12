# Spec 029 — Tasks

> ## PLAN — DRAFT, NOT FROZEN — 2026-10-12
>
> Adjudication is recorded in `adjudication.md` (OD-1…
> OD-6 ratified as a block, 2026-10-12). Audit §9 items
> D-A, D-B, D-D, D-E entered scope by the owner's
> ratification the same day and are planned below;
> **D-C is excluded** — it is executed separately as an
> immediate errata PR. Implementation tasks remain
> gated on the freeze merge (§Freeze gate below) and
> each phase merge is owner-gated. No task in this
> file is an execution authorisation by itself.

## Lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and claim
      register checked against constitution §§I–VIII
      and governance H2, H6, H13, H15/H23. Recorded in
      plan §5.
- [x] **L2 — Plan + tasks.** `plan.md` and this file,
      hand-authored in Spec 028 house format, including
      the 2026-10-12 scope ratification (D-A, D-B, D-D,
      D-E in; D-C out). The tooling deviation is
      recorded in plan §8.
- [ ] **L3 — AEE hooks.** AEE assess + evaluator-contract
      pass over spec, plan, and tasks; outputs saved
      under `aee/` with outcomes recorded. A `fail`
      outcome blocks the freeze until its recovery
      record is complete. If the hook pass cannot run
      non-interactively, that outcome is recorded here
      rather than skipped silently (plan §8).

## Freeze gate

- [ ] **F1 — Freeze artifacts.** `freeze.md` +
      `freeze.json` (framework026 digest via the house
      freeze builder, over spec.md, claims.json,
      adjudication.md, assessment.md, audit.md,
      reclassification-ledger.json, plan.md, tasks.md)
      + freeze tests in `backend/tests/` asserting the
      digest and the ledger's §3 counts.
- [ ] **F2 — Freeze PR.** Opened as a draft; CI verified
      from the run's own conclusion and job logs;
      branding sweep clean; merged only on the owner's
      order. Ledger entries appended in both program
      ledgers.

## Phase A — Stage axis and transition core
(FR-029-01…03; claims C01, C02; plan §0; after F2)

- [ ] **A1 — Record shapes.** Additive `stage`,
      `stage_source`, `stage_as_of`, and append-only
      `stage_history` (from/to stage, actor, timestamp,
      evidence refs, reason) on the extracted-claims and
      anchor record shapes; no existing field changes
      meaning.
- [ ] **A2 — AEE mapping.** `aee_core.claim_from_glossa`
      maps the stage axis as a distinct object, never
      folded into `ClaimStatus` or confidence; a
      regression test proves score propagation is
      byte-identical to pre-change behaviour on the
      current claim set.
- [ ] **A3 — Transition service.** The single writer of
      stage changes: one-step-forward legality, backward
      moves only with a recorded reason, automated actors
      allowlisted to `created`/`checked` and fail-closed
      above `checked`, named-human actor required above
      `checked` (a process name never validates). Every
      write updates `stage`, `stage_source`, and
      `stage_as_of` together.
- [ ] **A4 — Endpoint serialization.** `GET /claims`,
      `GET /claims/aee-scores`, and the anchor surfaces
      serialize stage (with provenance and history
      summary) and lane-1 score as distinct objects.
- [ ] **A5 — Risk flag.** `verified_unexplained`
      computed per FR-029-03 and exposed in API output;
      tests cover the audit's flagged shapes (SUPPORTED-
      class or high band below `explained`).
- [ ] **A6 — Phase gate.** Foundation check 0 failures
      + full backend suite green; branding sweep; PR
      with CI verified from run conclusions; owner-gated
      merge.

## Phase D — OD-1 re-staging migration (EARLY, per D-E)
(OD-1; plan §0, §2.2; audit ledger as the single source
of truth; after A6)

- [ ] **D1 — Consumer inventory.** Every consumer of
      the anchors file hash and of the claim stores is
      inventoried and named in the phase record before
      any run.
- [ ] **D2 — Migration script.** Consumes the frozen
      `reclassification-ledger.json` only; stamps
      `stage`, `stage_source` (ledger + entry),
      `stage_as_of`, and an initial `stage_history`
      entry per record; dry-run mode emitting a
      reconciliation report; idempotent (second run is
      a no-op and says so); pre-run snapshot of every
      touched store, named in the run record;
      additive-only assertion (canonical comparison of
      pre-existing fields, before/after SHA-256).
- [ ] **D3 — Dry run.** Reconciliation matches the
      ledger §3 table exactly: per class — anchors
      193 created / 94 checked; extracted claims
      21 / 10; PRED-2026 live 3 / 2; hypothesis models
      3 created; study headlines 10 checked — totals
      220 created / 116 checked / 0 / 0 / 0, and the
      105 `verified_unexplained` flags reconcile. A
      mismatch stops the phase; it is not smoothed.
- [ ] **D4 — Live run.** One dated reclassification
      event: stages and provenance stamped on the live
      records; the anchors file's additive change lands
      in this phase's PR; backend stores updated by the
      run; run record written to this directory.
- [ ] **D5 — Post-run verification.** Foundation check
      0 failures (H21); full backend suite green;
      ledger-vs-live reconciliation re-run from the
      live stores and matched; every stamped record
      carries `stage_source` and `stage_as_of`; the
      additive-only assertion holds in the run record.
- [ ] **D6 — Phase gate.** As A6, with D5's evidence
      attached to the PR.

## Phase H — Anchor annotation and schema (D-A)
(plan §2.5; after A6 + D6 — same file, one writer at a
time)

- [ ] **H1 — `validation_status` made total.** Every
      anchor carries an explicit `validation_status`:
      existing values preserved verbatim; absent fields
      made explicit from the record's own provenance.
      Additive only — no tier, reading, basis, or
      existing value changes; the additive-only
      assertion (canonical comparison) proves it.
- [ ] **H2 — Computed `strict_set` flag.** Every anchor
      gains the flag, computed by the Phase-108 register
      + Phase-109 rule join; the rule's identifier and
      version are recorded in the file metadata.
      Reconciliation: strict count = 94 (90 HIGH +
      4 MEDIUM), matching the audit exactly.
- [ ] **H3 — Declared schema.** A schema file declares
      the anchors file's shape (required core fields,
      this spec's additive fields, optional fields);
      the annotation pass normalises the 56 observed
      field shapes additively into the declared shape.
- [ ] **H4 — CI validator.** CI fails on any anchors
      record whose shape is undeclared under H3's
      schema.
- [ ] **H5 — Phase gate.** As A6, with H1/H2
      reconciliation evidence attached.

## Phase I — Claim-store deduplication (D-B)
(plan §2.6; merge, never delete; unit of repair = the
2026-10-09 extraction batch; after D6)

- [ ] **I1 — Fingerprint + inventory.** The proposition
      fingerprint is defined and frozen (hash over
      normalised claim text; normalisation rules
      recorded). A scan of the claims store fixes the
      exact duplicate set in the phase record; the
      audit's two known double-recorded propositions
      are the expected minimum — further collisions are
      reported, not silently absorbed.
- [ ] **I2 — Merge.** One canonical claim per
      proposition (the fuller trail wins); every other
      record of the proposition is preserved as an
      evidence instance attached to the canonical
      claim. Nothing is deleted. Stamped stages and
      stage histories (Phase D) are preserved on the
      canonical record and on each evidence instance.
- [ ] **I3 — Origin-group counting.** A merged
      proposition's evidence counts its origin group
      once in the AEE wiring. Resulting lane-1 score
      movement is recomputed and reported in the phase
      record with its cause; verdicts and stages are
      untouched by the merge.
- [ ] **I4 — Intake gate.** Extraction intake computes
      the fingerprint for every new claim; a collision
      with an existing fingerprint fails loudly — intake
      stops with an error naming both records. Tested
      with a planted duplicate.
- [ ] **I5 — Phase gate.** As A6.

## Phase B — Bundles, attribution, explanation, digestion
(FR-029-04…07; claims C03, C04, C05; OD-2, OD-3, OD-5;
after A6)

- [ ] **B1 — Bundle representation.** Parent record +
      sub-claim records (`reading_soundness`,
      `scholarship_accounting`, `attribution`,
      `explanation_intelligibility`), each with evidence
      list, falsification condition, stage, and trail;
      parent stage computed as the minimum of sub-claim
      stages and stored as that computation's cache
      (`stage_source` = the computation) — unit-tested,
      never directly assignable.
- [ ] **B2 — Attribution template.** Required fields:
      prior readings with resolvable citations;
      completeness basis (search record: corpora and
      literature searched, date, searcher); contest
      state + contest record. OD-3 enforced: contested
      caps the parent at `checked`; unexamined carries
      no cap. Both cases tested.
- [ ] **B3 — Explanation record.** Named human author,
      artifact URI + stored content hash, challenge
      venue, AI-assistance disclosure field. Validation
      rejects process/AI actors as the named human
      (OD-2); the `accepted` transition fails closed
      without a valid record.
- [ ] **B4 — Digestion record.** The three OD-5 classes
      (independent reuse; published challenge answered
      in a durable record; mechanism-engaging citation
      with a named intake reviewer's stored rationale),
      each with resolvable references and a validated
      program-independence field (not a claim author,
      not program staff). Adverse digestion (unanswered
      refutation) flags the claim contested and records
      the pullback demotion.
- [ ] **B5 — Discriminating controls.** Each gate paired
      with a must-fail control (plan §2.4): automated
      actor → `explained`; human transition without an
      explanation record; `digested` without independent
      engagement; contested bundle rendering above
      `checked`. A non-differential gate marks the run
      INVALID.
- [ ] **B6 — Phase gate.** As A6.

## Phase C — Priority register and trails
(FR-029-11, FR-029-12; claims C08, C09; OD-6; after A6)

- [ ] **C1 — Priority register.** Intake API + store:
      issuance on record completeness alone (no score,
      stage, or verdict field exists on an entry);
      public record = claimant + server timestamp +
      SHA-256 of the reading; content sealed until
      claimant publication or reveal date (default
      24 months, extendable once as a dated record);
      credit display invariant under later program
      assessment — tested.
- [ ] **C2 — Trail view.** Per-claim API trail:
      evidence refs with origin groups, falsifier state
      at decision time, actor, timestamp, for verdicts
      and stage transitions alike.
- [ ] **C3 — Phase gate.** As A6.

## Phase J — Foundation annotations (D-D)
(plan §2.7; step 1 after F2, step 2 after A6)

- [ ] **J1 — Interim as-of label.** The current
      foundation report's `solid_claims` /
      `caveated_claims` annotations are stamped with a
      dated as-of label naming the anchor table they
      describe. Labelled, not silently refreshed.
- [ ] **J2 — Computed annotations.** At report-
      generation time, annotations are computed from
      canonical data (current anchors file + claim
      stores); the generated report is stamped with the
      SHA-256 of the anchors file it was computed
      against. A regeneration test proves the figures
      track the canonical file.
- [ ] **J3 — Loud endpoint.** The foundation status
      endpoint serves the on-disk report; a missing or
      unreadable report produces an explicit error
      response — never silent nulls. Tested both ways
      (report present → served; report absent → loud
      error, no null payload).
- [ ] **J4 — Phase gate.** As A6.

## Phase E1 — Display withdrawals
(FR-029-08; claim C06; audit §5-P5; after F2 — no
dependency on A–D; ships early on OD-1's visibility
priority)

- [ ] **E1.1 — Panel headline.** The "{totalAnchors}
      signs deciphered" headline and the confidence-led
      layout are withdrawn from `DeciphermentPanel`;
      the replacement leads with the standing position
      and the lifecycle stage summary under lane-2
      labels, with the OD-4 one-line legend. Rendered
      output verified by screenshot at desktop and
      mobile widths before the phase is called done.
- [ ] **E1.2 — Dashboard payload.** `sa_aggregate`,
      `fully_decoded_pct`, and `n_fully_decoded` removed
      from the dashboard API payload and from the
      panel's consumption; underlying data files
      untouched.
- [ ] **E1.3 — Mean score.** `mean_propagated_score`
      withdrawn from the `GET /claims/aee-scores`
      summary position; any retained program-level
      diagnostic appears only inside a lane-1-labelled
      block with method and falsifier context.
- [ ] **E1.4 — Band placement.** Score bands render
      only inside lane-1 checking presentations,
      alongside score and method — never beside a claim
      status.
- [ ] **E1.5 — Phase gate.** As A6.

## Phase E2 — Lane-separated rendering
(FR-029-09, FR-029-10, FR-029-05 display rule; claims
C06, C07; OD-4; after D6)

- [ ] **E2.1 — Two regions.** `IndusEvidenceView` and
      the anchor surfaces render a lane-2 region (stage
      in Tao's verbatim names + legend) distinct from a
      lane-1 region (verdicts, scores, extraction
      statuses in checking vocabulary only). Lane-1
      badges lose stage colours and acceptance language.
      Screenshots at desktop and mobile widths verify
      the rendering.
- [ ] **E2.2 — Contest display.** A contested
      attribution renders on the parent wherever the
      parent renders.
- [ ] **E2.3 — Not-understood.** `not_understood`
      rendered with every verdict; records lacking the
      field render as incomplete, visibly. The authoring
      queue for existing verdict records is written down
      in the phase record as lane-2 human work (no
      machine-generated text is substituted for it).
- [ ] **E2.4 — Phase gate.** As A6.

## Phase G — CI gates and trail completeness
(FR-029-12; claim C09; plan §0, §2.4; after A–J, E)

- [ ] **G1 — Completeness gate.** CI fails on any new
      verdict or stage-transition record missing
      evidence refs, origin groups, falsifier state,
      actor, or timestamp.
- [ ] **G2 — Stage-cache integrity.** CI recomputes
      stages from record evidence (sampled population;
      full migrated population on demand) and fails on
      any stored stage that disagrees with its
      recomputation or lacks `stage_source` /
      `stage_as_of` (plan §0).
- [ ] **G3 — Gate suite.** The Phase B discriminating
      controls and the parent-stage computation tests
      (minimum rule, OD-3 cap, adverse-digestion
      pullback) run as a named CI suite.
- [ ] **G4 — Display guards.** Automated checks: the
      withdrawn strings/fields stay withdrawn (panel
      headline pattern, dashboard fields, scores-summary
      mean); lane labels and the stage legend are
      present on the claim surfaces; no stage name
      renders in a lane-1 position.
- [ ] **G5 — Phase gate.** As A6.

## Closeout

- [ ] **X1 — Verification on merged main.** Full
      backend suite and foundation check (0 failures);
      the anchors' pre-existing fields verified
      unchanged by canonical comparison (additive keys
      from Phases D and H excluded); PRED register
      untouched; final ledger-vs-live reconciliation
      attached.
- [ ] **X2 — Records.** Closeout record in this
      directory; entries in both program ledgers;
      deviations all recorded; D-A, D-B, D-D, D-E noted
      as disposed by this spec's phases; D-C noted as
      executed separately (outside this spec).
