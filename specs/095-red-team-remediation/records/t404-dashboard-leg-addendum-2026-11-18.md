# T404 — Dashboard-leg addendum (2026-11-18)

**Status of this document.** An addendum to the T404 audit package
(`t404-thresholds-2026-11-17.md`, `t404-scoring-corrections.json`,
`t404-run-2026-11-17.json`, Stage 4 record). The original run record
is unedited. The Stage 4 run deferred the dashboard-dependent legs
because the dashboard did not exist; the T403 build (owner-approved
wireframes, 2026-11-18) created it, and this addendum re-runs those
legs against the built dashboard under the audit's own protocol,
thresholds fixed in advance in the thresholds file and the scoring
corrections. Nothing in this addendum remediates the Stage 4 run's
five functional defects (project import 422, job pause/resume 409,
report generate 503, no rollback/restore, color-contrast); that
scope is a separate owner decision, still pending.

**Instance.** An audit instance of the built tree (branch
`feat/095-t403-dashboard-build`), copied from the build clone with
its stores as found, served on a spare port with API auth off, per
the Stage 4 instance definition. The instance's extracted-claims
store was restored to the ledger-mirrored bytes before the run
(the copy had inherited a suite-regenerated state; the settling
engine's source verification refused against it, correctly, until
restored — the refusal is the machinery working, and the scored run
below ran on the restored tree). Driver and raw results:
`records/t403-screenshots/t404-dashboard-leg-results.json`, step
screenshots `records/t403-screenshots/t404-p*.png`, surface
screenshots in the same directory (desktop + mobile, filed with
the T403 build record).

## The eight-step protocol (threshold P1: at least 6 of 8 completable end-to-end)

All eight steps completed end-to-end. **8/8 — P1 MET.**

- **P1 — home.** Census of record on the face (994 claims);
  strongest readings carry NOT IDENTIFIABLE; does-not-claim panel
  present.
- **P2 — program status.** Blocked items render with their
  blockers; GR-088-01 named.
- **P3 — inscription explorer.** Filter by sign 145; open
  GLI-IND-0000206; four labelled layers (observation,
  transcription, hypothesis, claim); selecting a sign position
  shows only that sign's statements.
- **P4 — hypothesis comparison.** No translation held, stated;
  the nonlinguistic position present; 12 NOT IDENTIFIABLE markers
  across the surface.
- **P5 — evidence inspection.** Falsifier-absent filter returns
  exactly 9 claims; the first (`ancient_writing_and_modern_
  technologies_51831ac9_sign_val_0001`) opens with its detail and
  lineage. (First driver attempt failed here: the claim detail
  card's test identifier was being dropped by the shared Card
  component, so the step could not verify the detail it had in
  fact opened. The build defect was fixed, the e2e spec gained
  the missing detail assertions, and the scored run above is the
  re-run on the fixed build.)
- **P6 — contribution.** Candidate submitted through the form:
  "T404 dashboard-leg candidate: sign M044 carries the value ku in
  syllabic slots.", with its falsifier and the evidence reference
  M044. Accepted as candidate `RDC-20261118171355-001` at stage
  "staged". Per the scoring corrections, the pass evidence is the
  store, not the screen: the candidate id and the exact candidate
  text were verified present in the audit instance's staging store
  (`outputs/anchor_staging.json`) after the run, exactly once.
- **P7 — experiment reproduction.** Legacy runs are marked not
  reproducible with the missing pieces named. The T405 run of
  record re-ran on scratch from the surface: corpus identity
  verified, record written to scratch only, quantities compared
  run against run — assigned_count recorded 94, re-run 94;
  assigned_share identical.
- **P8 — audit-trail export.** The claim opened in P5 exported
  from its detail: downloaded file `claim-audit-trail-ancient_
  writing_and_modern_technologies_51831ac9_sign_val_0001.json`
  (16,718 bytes; filed with the results). Verified after download:
  the file carries the ledger row for the claim (`ledger_row`
  present; claim id and statement match the record).

## Accessibility pass (axe-core 4.10.2, the seven dashboard surfaces)

- **A1 — zero violations of severity "critical": NOT MET.**
  Critical findings, all on the new dashboard surfaces:
  `label` (form elements without an accessible label) —
  inscription explorer 2 nodes, researcher contribution 4 nodes;
  `select-name` (select elements without an accessible name) —
  inscription explorer 2 nodes, evidence inspection 3 nodes.
  Home, program status, hypothesis comparison, and experiment
  reproduction have no critical findings. The wireframe kit's
  labelled controls carry their labels as adjacent text; the
  explorer's and contribution form's icon-and-placeholder controls
  and the filter selects do not expose an accessible name. This is
  a defect of the built surfaces, filed here as measured; its
  remediation is not part of the build commission and joins the
  remediation-scope question already before the owner.
- **A2 — at most 3 serious violations, each named, and the home
  surface's primary navigation traversable by keyboard alone:
  MET.** Serious classes (2, within the bound): `color-contrast`
  — home 8 nodes, program status 4, inscription explorer 4,
  hypothesis comparison 4, evidence inspection 4, researcher
  contribution 4, experiment reproduction 0 (this is the Stage 4
  run's standing contrast finding, present on the new surfaces in
  the same class); `scrollable-region-focusable` — hypothesis
  comparison 1 node. Keyboard: on the home surface the section
  navigation is the first focus order — the six section tabs are
  the first six Tab stops, followed by the six feature-card open
  buttons; the primary navigation is traversable by keyboard
  alone. (The axe home pass and the keyboard traversal were
  measured in a supplementary pass on the same instance and build:
  the app's section state persists across a same-hash navigation,
  so the main driver's return-to-home step could not reset it;
  the supplementary pass navigated by the section tab itself.)
- Moderate findings, not scored: `heading-order` (1 node, all
  seven surfaces) and `region` (5 nodes, all seven surfaces) —
  the app shell's landmark structure, shared with every existing
  surface.

## What this addendum does and does not settle

The dashboard leg of T404 is now run and filed: P1 met (8/8), A1
not met (criticals named above), A2 met. T404 as a whole remains
open: its authenticated legs still wait on the owner's sessions,
and C095-13 is not discharged — the A1 criticals and the Stage 4
run's five functional defects both stand for the owner's
remediation-scope decision, which also gates Spec 095's T503
closeout. The original package verdict (FAIL against its
thresholds) is unchanged by this addendum; the dashboard leg's own
scores are as stated here.
