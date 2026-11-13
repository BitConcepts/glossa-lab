# Spec 094 — Tasks

## Adoption (precondition for every stage)

- [x] **T001 — Package lands.** spec.md, claims.md, aee-claims.json,
  plan.md, tasks.md, records/ (commission-and-grounding record,
  ratification record, adoption AEE assessment) committed as
  `specs/094-research-loop-acceptance-hardening/` on
  `spec/094-adoption`. Claims: package-level. Acceptance: **test**
  (the package verification of record: aee-claims.json parses;
  claims.md and aee-claims.json carry the same 13 claim ids in the
  same order; every claim has a falsifier and a DNE line; the
  grounding record's mechanism statements are reproducible from the
  repo at the package's base commit and from the test record).
  *This does not establish:* that the package is approved — only
  that it is complete and internally consistent.
- [x] **T002 — AEE verification of the claims.** The C094 bundle run
  through the pinned assessor (aee 1.5.3, CI-faithful venv):
  `aee validate` (valid: 13 claim(s), exit 0) and `aee assess
  --no-ledger`, outcome **iterate** recorded in
  `records/adoption-aee-assessment.json` and quoted in the
  ratification record. No draft-time (T002-analogue) assessment
  exists for this package — the package was drafted in the goal
  workspace without an assessor run, and the adoption assessment is
  the first of record; nothing is back-filed. Acceptance: **test**
  (the assessor ran and its outcome is recorded verbatim).
  *This does not establish:* claim quality — a draft-stage outcome
  is the expected reading for a bundle on one asserted source; the
  owner's approval is the human act (T003).
- [x] **T003 — Owner block approval.** The owner ratifies the
  package as a block: spec, 13 claims, plan, and decisions
  D-094-1..6 as recommended (option tap plus typed confirmation,
  Glossa-Lab chat, 2026-11-13) — including the D-094-5 object
  adjustment carried by the parent addendum. Acceptance:
  **human-as-oracle** (the owner).
  *This does not establish:* approval of any later stage's output —
  each lands on its own evidence.
- [ ] **T004 — Claims-ledger intake + program-map assignment
  (separate gated act; NOT part of the adoption PR).** (a) Assign
  `094-research-loop-acceptance-hardening` in
  `glossa-indus/map/program-map-taxonomy.json` (domain/subdomain
  recorded in the act's record; the gate's V10 leg names an
  unassigned spec directory until this lands — that reading on
  this PR's CI is expected and is this task's, not a defect in the
  spec files); (b) append the C094 bundle through
  `tools/ledger/import_bundle.py --spec
  specs/094-research-loop-acceptance-hardening --date 2026-11-13`
  — the only sanctioned path, never a hand-edit; (c) refresh the
  settling chain and regenerate the generated layers over the
  grown ledger, republishing through the gated path; (d) re-pin
  the census literals in the pin-bearing tests from the
  regenerated artifacts' actuals, weakening nothing; (e) record
  the gate's summaries on the final tree. Claims: package-level.
  Acceptance: **test** (gate summaries + reconciliation test in
  the act's record).
  *This does not establish:* any C094 claim — the build stages
  discharge them.

## Stage 0 — Grounding completion (no code)

- [ ] **T010 — Live store inventory.** Read-only census of the
  three anchor-path stores on the live backend: staging entries by
  state; archive entries by status with the pre-gate
  approved/verified count named; anchors census. The record cites
  counts and states only and writes nothing live. Claims:
  C094-12 (inventory clause). Acceptance: **gate** (the record's
  counts are read from the stores at a named time).
  *This does not establish:* anything about the inventoried
  entries' soundness — they are counted, not examined.
- [ ] **T011 — Probe verdict carried; re-run staged.** The
  storage-edit probe's observed verdict (parent addendum,
  2026-11-13) is entered in the stage record as C094-10's
  grounding, and the probe's re-run against the built shape is
  registered as Stage 4's exit evidence (D-094-5 as adjusted).
  Claims: package-level. Acceptance: **gate**.
  *This does not establish:* that the anchor path shares the claim
  ledger's post-hoc net — the addendum's finding is that it has
  none, which is the exposure Stage 4 closes.

## Stage 1 — Record schema and the approval gate (C094-1..3)

- [ ] **T101 — Candidate record fields.** Falsifier, approver, and
  evidence fields become first-class fields of the candidate
  record, carried by the staging write; records lacking them are
  unapprovable until they carry them. Claims: C094-3.
  Acceptance: **test** (schema + staging-write coverage; a gate
  decision taken from request-only data is refused by
  construction).
  *This does not establish:* that any existing candidate gains the
  fields — pre-gate records stay as they are (C094-12).
- [ ] **T102 — Approve-route enforcement.** `staging_action`'s
  approve route requires a non-empty record falsifier and an
  approver validating as a named human under the `claim_stage`
  actor rules, against the D-094-1 named-humans list; automated
  identities are refused for approve, verify, and promote.
  Claims: C094-1, C094-2. Acceptance: **test** (probe (a) refuses
  in its original and automated-actor variants; a conforming
  approval carries all three record fields).
  *This does not establish:* falsifier quality — presence and
  attribution only (C094-1's own cap).

## Stage 2 — The promotion evidence standard (C094-4..5)

- [ ] **T201 — Evidence pinning.** Pin-by-SHA-256 at pin time,
  recorded on the candidate record; promotion verifies bytes
  against the pin and refuses on absence, mismatch, or a pin
  created by the promote request itself. Claims: C094-4.
  Acceptance: **test** (probe (b) variants: existing-file ref and
  request-created pin refuse; a pinned artifact promotes).
  *This does not establish:* relevance — that is T202's bar.
- [ ] **T202 — Registered evidence classes.** The admissible-class
  list lands as a registered artifact; the candidate's recorded
  class must be on it; loop or anchor-path output about the
  candidate is not a class and cannot be registered as one by
  configuration. Claims: C094-5. Acceptance: **test**
  (self-referential class refuses; an unregistered class refuses;
  a registered-class pinned artifact promotes on the record).
  *This does not establish:* the truth of any class member.

## Stage 3 — Verification redefined (C094-6..9)

- [ ] **T301 — Flat-delta flip removed.** The `sa_delta = 0.1`
  construction and the approved → verified flip leave
  `_run_anchor_lifecycle`; its other duties are unchanged.
  Claims: C094-7. Acceptance: **test** (a lifecycle run over
  approved candidates under a clean foundation check flips
  nothing).
  *This does not establish:* that archiving or expiry behaviour
  changed — they did not, except where they carried the flip.
- [ ] **T302 — Per-candidate verification + the MEDIUM binding.**
  Verification becomes a recorded per-candidate evaluation
  (method fixed in the stage's design note before the route is
  built), effected by a named human; promotion confers MEDIUM
  only on candidates so verified, LOW at most otherwise.
  Claims: C094-6, C094-8. Acceptance: **test** (verified promotes
  at MEDIUM; unverified caps at LOW, whatever its score).
  *This does not establish:* the evaluation method's soundness —
  the claim binds granularity and record.
- [ ] **T303 — Fabricated fallback delta removed.** `get_staging`
  stops substituting `round(score * 0.12, 3)`; surfaces present
  the delta as absent where no SA comparison has run. The current
  behaviour is first demonstrated from the code on the stage
  record (the claim rests on a drafting observation). Claims:
  C094-9. Acceptance: **test** (no response carries an `sa_delta`
  for a candidate with no recorded comparison).
  *This does not establish:* anything about real deltas where a
  comparison did run.

## Stage 4 — Lifecycle routing and atomic stores (C094-10..11)

- [ ] **T401 — Gated transition service.** All anchor-path status
  transitions route through a single service carrying
  `transition_stage`'s guarantees (one-step moves, actor
  validation with the automated ceiling, evidence trail); the
  stage-vocabulary mapping is answered on the stage record;
  direct `review_status` writes outside the service are removed.
  Claims: C094-10. Acceptance: **test + gate** (code census: no
  direct writes remain; a transition attempted outside the
  service does not exist to attempt).
  *This does not establish:* storage enforcement beyond this path
  — the closure is path-scoped (C094-10's own cap).
- [ ] **T402 — Atomic stores.** The three anchor-path stores move
  to `atomic_io.atomic_write_text` (or Spec 092 Stage 2's
  verified-write successor, if landed by build time); every write
  site from the drafting census is re-proven absent. Claims:
  C094-11. Acceptance: **test** (write-site census; a simulated
  write failure leaves each store byte-identical under a named
  error).
  *This does not establish:* read-back hash verification beyond
  the atomic path's own guarantees.
- [ ] **T403 — Storage-edit probe re-run.** The probe of record
  re-runs against the built shape; its outcome is filed with the
  stage record and handled per C094-10 as designed in Stage 0.
  Claims: package-level (D-094-5's exit gate). Acceptance:
  **gate**.
  *This does not establish:* the Stage 5 closeout — the full
  battery is Stage 5's act.

## Stage 5 — Closeout (C094-12..13)

- [ ] **T501 — Full battery + register amendment + boundary
  verification.** The full policy probe battery re-runs end to
  end on a scratch instance against the built system; the
  GR-088-05 register entry is amended with the path-scoped
  closure (amend, never delete); C094-12's no-diff boundary is
  verified against the adoption-day anchor and ledger state.
  Claims: C094-12. Acceptance: **gate**.
  *This does not establish:* closure of GR-088-05 beyond the
  anchor path.
- [ ] **T502 — Closeout record; C094-13 lifted by name.** The
  closeout record discharges C094-1..13 per claim on their
  evidence, or carries each undischarged claim as a named
  failure; on full discharge it lifts the loop-off protection by
  name. Claims: C094-13. Acceptance: **gate** (the record itself,
  parent-gated like every stage).
  *This does not establish:* approval of any later loop run's
  output — later runs are ordinary operations under the landed
  gates, judged on their own records.
