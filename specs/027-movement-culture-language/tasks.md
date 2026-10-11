# Spec 027 — Tasks

> ## FROZEN — OWNER-ADJUDICATED 2026-10-11
>
> Adjudication is recorded in `adjudication.md` (T0 complete).
> Every Stage 0, Stage 1, and Stage 2 execution task remains
> gated on its own stage freeze. No task in this file is an
> execution authorization by itself.

## Draft lifecycle

- [x] **L1 — Constitution check.** Spec, plan, and claim
      register checked against constitution §§I–VIII and
      governance H2, H6, H13, and H15/H23. Recorded in spec §14
      and plan §4.
- [x] **L2 — Specify.** `spec.md` and structured `claims.json`
      (33 governed claims) authored; register integrity verified
      with Spec 026 `framework026.check_dependency_integrity`:
      no cycles, no missing dependencies, no forbidden
      inheritance.
- [x] **L3 — Clarify.** All unresolved owner choices are
      carried explicitly as spec §13 Asks 1–5; no answer is
      implied by the draft's recommendations.
- [x] **L4 — AEE after specify.** Rounds and recovery recorded
      in `aee/recovery-specify.md`; final outcome **pass**
      (33 claims, 0 failure modes, 0 below the 0.70 threshold).
- [x] **L5 — Plan.** `plan.md` authored with the post-
      adjudication stage sequence, constitution check, risks,
      and non-actions.
- [x] **L6 — AEE after plan.** Outcome **pass** (33 claims, 0
      failure modes, 0 below threshold); artifacts saved under
      `aee/`.
- [x] **L7 — Requirements checklist.** `checklists/
      requirements.md` authored and traced to FR-027-1…15.
- [x] **L8 — AEE after tasks.** Outcome **pass** (33 claims,
      0 failure modes, 0 below threshold); evaluator-contract
      result saved under `aee/`; composed strict outcome
      **pass**.
- [x] **L9 — Analyze.** Completed and recorded in
      `working/analyze.md`: every FR has a task path, every
      blocked question has a blocker and unblocking condition,
      and no execution task lacks its adjudication/freeze gate.
- [x] **L10 — Draft PR and ledgers.** Draft PR #147 opened
      and left unmerged; draft-opened entries appended to both
      program ledgers. No freeze, execution, external send, or
      publication.

## Owner adjudication gate

- [x] **T0 — Owner answers spec §13 Asks 1–5.** Answered
      2026-10-11 ("Approve Spec 027 with the recommended
      answers and freeze it"); binding record in
      `adjudication.md`:
  1. stage order and Stage 0 scope → **0A** (gazetteer +
     chronology spine in one Stage 0);
  2. Q2 governing sign list → **M77** (Parpola/CISI only as a
     labelled crosswalk sensitivity);
  3. Q2 corpus inclusion rules → **approved as drafted**;
  4. gazetteer licensing/publication posture → **CC BY 4.0
     through the release gate**, lawfully reusable rows only;
  5. Stage 1 timing → **executes on the adjudicated design**
     once its own freeze is committed and merged.

## Stage 0 — Gazetteer and chronology spine (after T0 + Stage 0 freeze)

- [x] **S0-1 — Stage 0 freeze.** Name source versions, licence
      evidence, schemas, clustering rule, calibration version,
      chronology-scenario treatment, phase number, graph nodes,
      hashes, and tests. Freeze is committed and merged before
      any Stage 0 build task runs.
- [x] **S0-2 — Source and licence audit.** Assign every
      candidate source a spec §5.1 licence state; catalogue
      non-reusable sources without copying them.
- [x] **S0-3 — Gazetteer schema and validators.** Implement
      the §6.2 contract and fail-loud checks for source,
      locator, period scheme, licence, coordinate state, and
      origin group.
- [x] **S0-4 — Gazetteer build.** Produce source-asserted rows,
      duplicate/conflict reports, and coverage/survey-bias
      reports. Restricted coordinates remain restricted.
- [x] **S0-5 — Chronology schema and validators.** Implement
      the §6.4 contract; reject aggregate period assertions as
      timing rows; require material and context-association
      fields.
- [x] **S0-6 — Chronology build.** Trace every date to its
      underlying record and publication; preserve competing
      scenarios, including the CONTESTED Mutin et al. revision.
- [x] **S0-7 — Stage 0 closeout.** Descriptive fitness-for-
      question report for Q1–Q9, claim integrity check, H21
      foundation check if triggered, ledger entries, and the
      owner's Ask 4 publication disposition handled separately
      through the release gate if selected.

## Stage 1 — Q2 repertoire gate (after Stage 0 + Stage 1 freeze; Ask 5 controls the go)

- [x] **S1-1 — Margins-only corpus audit.** Population flow,
      sign-list coverage, completeness grid, permutable-cell
      projections, and dominant-site shares. No repertoire
      outcome is computed.
- [x] **S1-2 — Stage 1 freeze.** Insert the adjudicated sign
      list and corpus rules; freeze estimand, practical margin,
      interval rule, rarefaction, permutation strata, jackknife,
      controls, seeds, hashes, and verdict rules.
- [x] **S1-3 — H15/H23 gate.** Future phase script, graph
      module, registration, and registration verification in
      order before any run.
- [x] **S1-4 — Execution.** Run the frozen design once;
      report effect and interval, permutation result,
      single-object-type results where supported, jackknife,
      sensitivities, and every model variant tried.
- [ ] **S1-5 — Closure branch.** Apply spec §7.6 exactly:
      SUPPORTED requires a new proposal for downstream work;
      CONTRADICTED triggers negative closure; INCONCLUSIVE
      permits no downstream estimand work; INVALID preserves
      the instrument record and requires a new version/freeze
      for any corrected attempt.

## Stage 2A — Q7 (conditional; own freeze)

- [ ] **S2A-1 — Provenance and licence audit.** Build the D8
      link register with provenance method and licence state
      per link.
- [ ] **S2A-2 — Q7 freeze.** Site-pair matrices, controls,
      period eligibility, statistic, margin, jackknife, and
      negative controls.
- [ ] **S2A-3 — Execution and bounded report.** Ceramic and
      craft-technique outcomes separately; no people or
      language conclusion.

## Stage 2B — Q6 (conditional; own freeze)

- [ ] **S2B-1 — Timing-support assessment.** Evidence the
      spec §8.2 support conditions from Stage 0 metadata
      without inspecting timing outcomes. If unsupported,
      record NOT-YET-TESTABLE and stop.
- [ ] **S2B-2 — Q6 freeze.** Trait list, completeness grid,
      timing model, chronology scenario, rival patterns, and
      decision thresholds.
- [ ] **S2B-3 — Execution and bounded report.** Simultaneous,
      wave-like, and polycentric rivals reported under the
      frozen rule; no migration or administration claim beyond
      the bounded timing result.

## Registered-but-blocked questions (no execution tasks)

- [ ] **B1 — Q1 mobility arm.** Status NOT-YET-TESTABLE.
      Reassess only on evidence that a lawful site-period
      mobility dataset covers the frozen minimum independent
      inscription-bearing sites with baselines and period
      linkage.
- [ ] **B2 — Q3 Cemetery H / early PGW.** Status
      NOT-YET-TESTABLE. Reassess only on new paired primary
      isotope/aDNA data with same-catchment baselines.
- [ ] **B3 — Q4 Late Harappan transect.** Status
      REGISTERED-BLOCKED. Reassess on the full linked dataset,
      or design the declared fallback separately with its
      weaker verdict ceiling.
- [ ] **B4 — Q5 Mehrgarh replication.** Status
      NOT-YET-TESTABLE by this program. Reassess on independent
      sealed-context short-lived/enamel replication or
      refutation.
- [ ] **B5 — Q8 substrate stratigraphy.** Status
      NOT-YET-TESTABLE. Reassess only when at least two
      qualified human etymologists can code independently and
      blind under a frozen agreement rule. AI substitution is
      prohibited.
- [ ] **B6 — Q9 Brahui discriminator.** Status MAY BE
      NOT-YET-TESTABLE, declared in advance. Reassess only on a
      pre-registered linguistic observation with materially
      different expectations under the relic and later-arrival
      models.

## Closeout boundaries

- [ ] **X1 — No publication in the draft program.** Any later
      publication follows the owner's Ask 4 answer and the
      program release gate in a separate record.
      *Closeout note (2026-10-11): complied with — the Stage 0
      package was prepared and gate-verified in-repo only; no
      deposit or publication was made in this program. The two
      OSF registrations (design osf.io/a2xvc; Stage 1 contract
      osf.io/pnqrx) are program records under owner direction,
      not result publications. X1 remains a standing boundary
      for any future publication.*
- [x] **X2 — No anchor or PRED contact.** Verify at every
      stage closeout that anchors are byte-identical and no
      PRED-2026 scoring occurred.
      *Verified at program closeout (2026-10-11): anchors
      sha256 eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86
      ebb1fa3b602cfaed (byte-identical); zero program commits
      touched docs/PREDICTION_REGISTER.md; no PRED scoring ran.*
