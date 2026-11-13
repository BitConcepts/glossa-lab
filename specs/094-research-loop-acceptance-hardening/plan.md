# Spec 094 — implementation plan

Stages run in the order D-094-4 fixes: Stage 0 (grounding
completion) immediately, in parallel with Spec 092 S1 which it does
not disturb; the build stages (1–4) after Spec 092 S1 and before
Spec 091 Stage 1, whose locator pass is the candidate flow these
gates exist to receive; Stage 5 (closeout) ends the spec. The
adoption (ratification + this package's landing) precedes all
stages; the claims-ledger intake is a separate gated act, not part
of the adoption PR and not a stage. Dependencies between stages
are stated per stage. The probe battery of 2026-11-13 is the
acceptance instrument throughout: at each stage's exit the policy
probes in that stage's scope must refuse, and each stage record
names the claims it discharges and the probe or census that
discharged them.

## Adoption (precondition for every stage)

The package lands as the adoption PR (`spec/094-adoption`); the
claims are assessed under the pinned AEE at adoption
(`records/adoption-aee-assessment.json`). On the owner's block
approval — spec, 13 claims, this plan, and decisions D-094-1..6 as
recommended — the adoption PR records the ratification and appends
the root LEDGER.md entry. The claims-ledger intake (program-map
assignment, `tools/ledger/import_bundle.py` append, generated-layer
regeneration, gated republication) executes as its own gated act
after this landing, on the Spec 092 T004 pattern; it is recorded
in its own record when it runs, and nothing in the stages below
waits on it except where a stage record cites the grown census.
Claims: package-level (no C094 claim discharges here; C094-12's
boundary census starts from the adoption tree).

## Stage 0 — Grounding completion (no code)

**Objective.** Every number and verdict the later stages cite
exists in this stage's record.

**Work.**
- **Live store inventory.** Read-only census of the three
  anchor-path stores on the live backend: staging entries by
  state (read as 0 items on 2026-11-13); archive entries by
  status, with the pre-gate `approved`/`verified` count named —
  the count C094-12's no-grandfathering rule and D-094-6's
  re-evidencing cost turn on; the anchors file census (287 at
  drafting). Counts and states only; no record content is
  re-adjudicated, and no live store is written.
- **Probe verdict of record.** The claim-record storage-edit
  probe is already observed (parent addendum, 2026-11-13: a bare
  `created` → `digested` edit is detected by cross-store
  consistency only — 10 FAIL in full mode, 13 FAIL in --regen
  mode, every failure a divergence check, no lifecycle
  validation). Stage 0 carries that verdict into its record as
  the grounding C094-10's design answers, and stages the probe's
  re-run against the built shape as Stage 4's exit evidence
  (D-094-5 as adjusted).

**Acceptance.** **Gate** — the record itself: inventory counts
and the probe verdict stated from reads, not inference. Claims
discharged: none (Stage 0 grounds C094-12's inventory clause and
D-094-5's gate; the claims discharge at their build stages).

## Stage 1 — Record schema and the approval gate (C094-1..3)

**Objective.** Approval stops being a bare status flip: it
becomes a gated act whose inputs live on the candidate record
and whose actor is a named human.

**Design.**
- **Record fields.** Candidate records gain `falsifier`,
  `approver`, and evidence fields as first-class fields
  (C094-3), written at staging/adjudication time — never
  supplied in the request that asks for the transition. The
  pipeline's staging write is the natural carrier; legacy
  records lacking the fields are simply unapprovable until
  they carry them (the C094-12 posture applied at record
  level).
- **Actor validation.** The approve route validates the
  approver against the `claim_stage` actor rules, reused not
  redefined: named humans on the D-094-1 list validate;
  automated identities (allowlist or process-token) are
  refused for approve, verify, and promote alike (C094-2). The
  named-humans list lives where the actor rules already read
  their allowlist from, or beside it — not a new registry.
- **Route enforcement.** `staging_action`'s approve route
  refuses when the record's falsifier is empty or the approver
  does not validate, in the endpoint's established refusal
  shape; the refusal changes nothing and writes nothing.

**Acceptance.** **Test** — probe (a) refuses in its original
variant (no falsifier on the record) and its automated-actor
variant; approvals on the built system carry all three record
fields. Claims discharged: C094-1, C094-2, C094-3.

## Stage 2 — The promotion evidence standard (C094-4..5)

**Objective.** Promotion evidence stops being a path that
exists and becomes a pinned artifact of a registered class.

**Design.**
- **Pinning.** An evidence artifact is pinned by SHA-256 at pin
  time, the pin recorded on the candidate record;
  `promote_to_anchors` verifies the artifact's bytes against
  the pin at promotion time and refuses on absence or mismatch
  (C094-4). A pin created by the promote request itself is a
  refusal, per C094-3.
- **Registered classes.** A named list of admissible evidence
  classes (external corpus record, published concordance entry,
  independent-expert record, adjudicated claim dossier — the
  list as ratified, amendable only by a recorded act). The
  candidate's recorded class must be on the list; loop or
  anchor-path output about the candidate itself is not a class
  and cannot be registered as one by configuration (C094-5).
- **Entry note.** The bug lane's corpus-membership precondition
  (defect 3) and request-ref refusal (defect 2's bug-shaped
  half) are assumed landed or land with this stage; the stage
  record names which.

**Acceptance.** **Test** — probe (b) refuses in all three
variants (no ref; existing-file ref; self-referential class),
and a promotion on a properly pinned, classed artifact succeeds
on the record. Claims discharged: C094-4, C094-5.

## Stage 3 — Verification redefined (C094-6..9)

**Objective.** "Verified" names a per-candidate act again, and
nothing else confers it.

**Design.**
- **Removal, not tuning.** The `sa_delta = 0.1` construction
  and the approved → verified flip leave `_run_anchor_lifecycle`
  (C094-7); the lifecycle's other duties (expiry of stale
  rejections, archiving) are untouched except where they
  carried the flip.
- **Per-candidate verification.** A verification is a recorded
  evaluation of one candidate, citing the per-candidate evidence
  it rests on, effected by a named human under the Stage 1 actor
  rules (C094-6). The evaluation method is fixed in this stage's
  design note, on its record, before the route is built.
- **The MEDIUM binding.** Promotion confers MEDIUM only on
  candidates verified under C094-6; approved-but-unverified
  promotes at LOW at most (C094-8). HIGH is untouched —
  promotion has never conferred it.
- **The staging surface.** `get_staging`'s fabricated fallback
  delta (`round(score * 0.12, 3)`) is removed; where no SA
  comparison has run, the surface presents the delta as absent
  (C094-9). Stage 3 demonstrates the current behaviour from the
  code before changing it — the claim rests on a drafting
  observation, not on the tested battery.

**Acceptance.** **Test** — a lifecycle run over approved
candidates under a clean foundation check flips nothing; a
per-candidate verification on the record promotes at MEDIUM
while an unverified one caps at LOW; no surface response carries
an `sa_delta` for a candidate with no recorded comparison.
Claims discharged: C094-6, C094-7, C094-8, C094-9.

## Stage 4 — Lifecycle routing and atomic stores (C094-10..11)

**Objective.** The anchor path's transitions pass the same
fail-closed gate the claim path uses, and its stores stop being
one truncating write away from zero.

**Design.**
- **The transition service.** All anchor-path status
  transitions (staged, approved, verified, promoted, rejected,
  archived, expired) route through a single gated transition
  service carrying `transition_stage`'s guarantees: one-step
  moves, actor validation with the automated ceiling, an
  evidence trail. The stage-vocabulary mapping for anchor-path
  statuses is a design question this stage answers on its
  record rather than prejudging — the claims bind the
  guarantees, not the vocabulary. Direct `review_status` writes
  outside the service are removed, and the removal is proven by
  census, not by reading the diff.
- **Atomic stores.** The three stores move to
  `atomic_io.atomic_write_text` — or to the verified-write
  successor if Spec 092 Stage 2 has landed it by build time
  (C094-11 adopts the stronger contract only if it exists).
  Every write site in the anchor path is enumerated from the
  drafting census (eight-plus truncating sites in
  `api/research_loop.py`) and re-proven absent by the exit
  census.
- **The probe re-run.** The claim-record storage-edit probe
  re-runs against the built shape (D-094-5's exit gate); its
  outcome is handled per C094-10 as designed in Stage 0 if the
  original verdict showed routing alone cannot hold the line.

**Acceptance.** **Test + gate** — a code census shows no direct
`review_status` writes and no direct truncating writes to the
three stores outside the service and the atomic path; a
simulated write failure leaves each store byte-identical under
a named error; the storage-edit probe's re-run outcome is on
the record. Claims discharged: C094-10, C094-11.

## Stage 5 — Closeout (C094-12..13)

**Objective.** The spec ends on a full re-run of the instrument
that opened it, or it ends as a failure record.

**Work.**
- The full policy probe battery re-runs end to end on a scratch
  instance against the built system (probes (a) and (b) in all
  variants, the lifecycle flip test, the storage-edit re-run
  already filed at Stage 4).
- The GR-088-05 register entry is amended with the path-scoped
  closure — amend, never delete, per the register's own
  discipline — recording that the lifecycle is now routed and
  storage-backed for the anchor path and remains as it was
  elsewhere.
- C094-12's no-diff boundary is verified against the
  adoption-day anchor and ledger state: no pre-existing anchor
  entry or claim record changed by any diff under this spec;
  the pre-gate stock's inventory (Stage 0) is restated with its
  promotability suspension in force until re-evidenced.
- C094-13's protection is lifted by name in the closeout
  record: the loop may run against the live stores under the
  landed gates, as ordinary operations.

**Acceptance.** **Gate** — every claim C094-1..13 discharged or
carried as a named failure. A stage that ends with an
undischarged claim ends as a failure record, not a closeout.

## Design rules carried through every stage

- **The tested path is the production path.** Gates are proven
  against the built system's real endpoints on a scratch
  instance, never against test doubles alone — the 2026-11-11
  lesson (doubles that do not enforce what production enforces
  hide exactly the defects this spec closes).
- **No bar is re-barred inside its own stage.** A probe that
  still passes is a stage failure, reported as one — never
  reclassified as a finding to note.
- **Gate inputs live on records.** Any stage that finds itself
  reading a deciding input from a request stops and reports;
  that shape is defect 2, and it does not re-enter by the back
  door.
- **The loop stays off.** No stage runs the research loop
  against the live stores; scratch-instance executions for
  stage evidence are the only loop runs, and their stores are
  disposable by construction.
