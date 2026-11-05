# Spec 093 — Tasks

Acceptance modes per the Autonomous Execution Doctrine.
Each task's *this does not establish* line survives into
its stage record. T001 and T002 are drafting tasks, done
with this package; every later task waits on the owner's
block ratification (Stage 0, T003).

## Drafting (done with this package)

- [x] **T001 — Drafting.** This package (spec.md,
  claims.md, aee-claims.json, plan.md, tasks.md, the
  grounding record) drafted under the owner's commission
  of 2026-11-05 and opened as a draft PR. Acceptance:
  **test** (the draft PR exists and its files are the
  package). *This does not establish:* that the package's
  design is sound — only that it was drafted, grounded,
  and filed for ratification.
- [x] **T002 — AEE validation of the draft bundle.** The
  bundle was validated under the pinned AEE at drafting
  (`aee validate`); the invocation and verbatim reading
  are in `records/t002-note.md`. Acceptance: **test**.
  *This does not establish:* that the claims are true, or
  that an adoption-time `aee assess` will read as this
  draft's validation did — validation is a form check,
  and the adoption assessment is Stage 0's own act.

## Stage 0 — Ratification and adoption

- [ ] **T003 — Ratification record and intake.** The
  owner's block act is recorded beside the package; the
  claims bundle is regenerated from claims.md by script,
  assessed under the pinned AEE (outcome recorded
  verbatim), and appended through the sanctioned intake;
  the spec directory receives its program-map assignment
  in the same landing; the gate runs before and after.
  Acceptance: **gate**. *This does not establish:* that
  the design is sound — only that it was ratified,
  recorded, and entered by the sanctioned path.

## Stage 1 — Inventory, normalization, join

- [ ] **T101 — Census completion.** The grounding
  inventory is re-run against the repo at adoption state
  and amended for any source or field it missed (C093-2);
  the disjointness counts of C093-3 are re-counted on the
  pinned snapshot and stated in the stage record.
  Acceptance: **test** (every count recomputable from the
  pinned files). *This does not establish:* that the
  census's sources are all the culture-side data in the
  world — only completeness against the named sources.
- [ ] **T102 — Material normalization register.** The
  material-class vocabulary and its mapping rules are
  filed; every distinct raw value in the pinned snapshot
  is dispositioned by rule (class, composite split,
  uncertainty handling, non-material exclusion), with the
  disposition counts stated. Acceptance: **test** (the
  register covers every distinct value; a raw value
  outside the register fails the check). *This does not
  establish:* that the classes are the right grain — only
  that the mapping is total, ruled, and frozen for the
  stages that consume it.
- [ ] **T103 — Join design, freeze, and precision audit.**
  The museum↔text join procedure is frozen; the
  hand-checked sample is drawn and checked; measured
  precision and the error census are recorded against the
  freeze's floor. Acceptance: **test** (sample,
  precision, and errors recomputable from the audit
  record). *This does not establish:* that the join is
  correct pair by pair — precision on the sample is the
  claim, and a join below its floor stops the material
  arm honestly (C093-8).

## Stage 2 — Channel independence

- [ ] **T201 — Channel definition.** The material-context
  projection is defined against G1 §2.1's state: the
  per-object tuple under Stage 1's vocabularies, the
  named population, and the bookkeeping feature set the
  prediction test may use, each stated so a second worker
  can implement from the definition alone. Acceptance:
  **human-as-oracle**. *This does not establish:* that
  the channel is independent — that is T202's question,
  and this task only makes it askable.
- [ ] **T202 — Freeze, administration, and standing.**
  The freeze is committed (fields, features, bars,
  controls, floors); the per-field prediction
  administration runs as Spec 089 runs; an independent
  auditor recomputes; C093-1's standing is recorded in
  §5's vocabulary with the per-field table. Acceptance:
  **human-as-oracle** (reviewer against freeze, runs,
  bar). *This does not establish:* that the surviving
  fields say anything about any reading — independence
  is about projections, and §5's vocabulary is the whole
  of what this task may conclude.

## Stage 3 — Comparanda register

- [ ] **T301 — Register v1.** Entries seeded per D-093-7
  are committed, each carrying comparanda set,
  transmission mechanism with source, fixed window, and
  compared practice; the four-element check runs over the
  register. Acceptance: **gate**. *This does not
  establish:* that the seeded comparisons are the right
  ones — only that each was fixed, with its mechanism,
  before anything was computed under it.

## Stage 4 — First computed passes

- [ ] **T401 — Site pass.** Freeze, runs, controls,
  held-out arm as the counts allow, audit, outcome —
  per plan.md Stage 4(a). Acceptance: **test** (bar
  adjudged mechanically on audited runs). *This does not
  establish:* why any accepted regularity holds — the
  pass states a joint-distribution fact at channel
  strength (C093-7), and no cause, function, or reading
  may be read into it.
- [ ] **T402 — Material pass (join-gated).** As T401,
  over the Stage 1 join's population, only if the join
  cleared its floor; otherwise the CANNOT BE
  ADMINISTERED record with the forcing counts is this
  task's deliverable. Acceptance: **test**. *This does
  not establish:* anything about material practice in
  the world if it stops — a stop is a finding about the
  record system, stated at its counts.
- [ ] **T403 — Contact-context administration.** The 14
  excavated seals and the Meluhha record administered
  as an evidence class under their Stage 3 entries'
  frozen expectations; the outcome states what the find
  contexts license and what they do not. Acceptance:
  **human-as-oracle**. *This does not establish:* a
  population claim of any kind — n=14 is an evidence
  class, and this task's record says so on its face.

## Stage 5 — Machinery extension

- [ ] **T501 — Matrix rows and map layer, generated.**
  The generators emit the material-context domain's
  matrix rows and the program map's material-context
  layer from the ledger family; no generated file is
  hand-edited. Acceptance: **gate** (regeneration
  reproduces the surfaces byte-for-byte from the
  ledger). *This does not establish:* that the layer's
  claims are true — only that the surface is the ledger,
  generated, citing ids.
- [ ] **T502 — Gate extension.** The ledger gate gains
  the culture-layer checks (citation existence, one-way
  flow, register-section counting support for Stage 6),
  with a seeded-violation proof that a bad citation
  fails. Acceptance: **test** (seeded violation fails;
  clean tree passes in both modes at the extended
  profile). *This does not establish:* that earlier
  layers' checks changed — the standing profile's
  existing counts are untouched, and the extension is
  additive.

## Stage 6 — Gap register and closeout

- [ ] **T601 — GR-093 entries and the completeness
  extension.** The culture-side entries (at least the
  five the plan names) are appended under the register's
  new section, each with its four elements (C093-12);
  the register's mechanical completeness checks are
  extended in the same landing to count the section.
  Acceptance: **gate**. *This does not establish:* that
  these are all the culture-side gaps there are — only
  that every entry carried is closable honestly.
- [ ] **T602 — Outcome record and VEXA report.** The
  closeout record states per stage what was
  administered, accepted, or stopped (with counts) and
  C093-1's standing as it finally stands; the outcome
  is reported to the VEXA chat in the record's own
  words, the send recorded. Acceptance: **test** (the
  recorded send matches the outcome record). *This does
  not establish:* the final word on the channel — later
  joins, later data, and the reader stand after it.
