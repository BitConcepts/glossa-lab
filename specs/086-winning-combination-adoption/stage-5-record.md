# Spec 086 — Stage 5 record (layered map)

Stage 5 builds the layered map last, per the approved build order: ledger
(Stage 1) → matrix (Stage 2) → gate (Stage 3) → settling (Stage 4) → map
(Stage 5). This record carries one section per task as the stage executes.

## T501 — Wireframes first (gate): package produced, awaiting owner approval

**State: the package is produced and presented for the owner's approval by
name. T501's acceptance is the owner's approval act on the actual screens,
which has not happened — the T501 checkbox in tasks.md is therefore left
UNTICKED. Ticking it would claim the gate had passed; the gate is the
owner's act, not the worker's.**

### The package

In-repo at `records/stage-5-wireframes/`; mirrored for the owner's direct
reading at the goal workspace,
`files/2026-11-01-spec086-stage5-wireframes/` (21 files, byte-identical
copies).

- `README.md` — status (DRAFT for approval), contents, the decisions in
  short, the provenance of every number on the screens, and what approval
  unblocks (T502–T504) and does not.
- `decisions.md` — the eight open questions (Q1–Q8), each with the worker's
  recommendation, plus the items decided upstream and recorded as not open.
- `conformance.md` — Point 5(a)–(e) clause by clause; the Stage 5 claim
  legs as designed (C086-16 displayed-score leg, C086-17, C086-18,
  C086-19); what T502/T503/T504 build and verify against the screens; the
  superseded Spec 085 elements.
- `wireframes/` — the shared stylesheet (the 081/085 package stylesheet,
  unchanged), `render-shots.py`, five screens, and `shots/` with all 10
  renders (desktop 1440 + mobile 390 per screen, produced in this
  environment with the Playwright venv; the desktop renders of the system
  view and the matrix view were inspected visually — layout, numbers, and
  annotation blocks render as designed).

### The five screens

1. **01-system-view** (L1) — conforms Spec 085's graph explorer: the header
   strip (claims by status; validated-anchor share 94 of 287, 0.3275;
   nearest dated items), the as-of stamp line with its STALE behavior, the
   standing-position banner (C086-20), the sign inventory by frame, matrix
   coverage (1,363 cells; the 7 opposes cells named; the 14 empty rows
   counted with three named; both unused column classes stated), the claim
   population by stage and population with the falsifier-gap census line
   (831/840; the 9 gaps all in the extracted population), the unresolved
   sign mentions (14, verbatim, on 5 claims) and the 3 sign references with
   no matrix anchor record, and the imported sign×sign block with both of
   its numbers (pipeline 1,631 edges; 200 edge records over 80 nodes).
   **The node-link canvas is removed** (decision Q1): the gated chain
   verifies no claim-graph edge set — the 790 claim×claim dependency pairs
   are coverage data, not cells (count verified directly against
   matrix.json for this package).
2. **02-claim-view** (L2, new) — specimen
   parpola_2010_dravidian_solution_manual_002, the one claim exercising
   four designed states at once: falsifier present but 0 evaluable; the
   ledger's "this does not establish" line verbatim; the displayed-score
   block in its honest empty state (aee_state null on 840 of 840) with the
   ScoringEngine-only label (C086-16's leg); settling bearing under both
   stored runs (touched via mahadevan:70 by the incumbent, via 72/64/70 by
   the challenger; tallies 0/0/0 under both; not divergent); and its matrix
   row rendered as the explicit empty state (1 of the 14), with
   yadav_2009_arxiv_manual_002's populated 2-cell row as the contrast
   inset (documents supports via yadav_2010_ngrams; studies opposes via
   Spec 054, both outcome appends cited, the 2026-10-25 append governing).
3. **03-evidence-view** (L3, new) — the column side for the same claim: the
   column-class summary (documents 316 / studies 10 / anchors 287 /
   research checks 31 / corpus texts 0 columns; 0 cells from every class
   for this claim); the source-of-record document as provenance, not a
   cell (sha256 3851a68c…); the advisory research-check annotation with its
   null verdict stated; and the anchor register records behind the claim's
   sign_refs (M064 va, HIGH, sa_in_provenance_chain, not strict; M070 vēl,
   HIGH, strict_sa_independent, strict; M072 mā, HIGH,
   pending_non_sa_validation — 1 of the 44 pending), confidence carried
   verbatim, with the registered matrix-defs vs glossa-settle-1 divergence
   named in a callout on the screen (decision Q8).
4. **04-matrix-view** — conforms Spec 085's matrix view: claims×evidence as
   the primary form (840 rows × 644 columns, 1,363 cells), relations shown
   as words (supports 1,356 / opposes 7 / constrains 0), the sign×sign
   block as a secondary form, claim×sign as a sign row-filter (decision
   Q5), the two unused column classes rendered as greyed class columns,
   empty rows hatched and explained, and a selected-cell panel carrying the
   cell's citations and its deriving rule (the yadav × 054 opposes cell,
   rule R3, both appends cited).
5. **05-settling-panel** — conforms Spec 085's projection panel into the
   settling panel: the computed-layer banner carrying the run records' own
   label ("Establishes what the ledger implies under these rules, not what
   the script says"); registered run inputs (glossa-settle-1; assignment
   sets of record: incumbent 94, full-register 286; user-built anchor sets
   excluded in v1, stated); the two stored T405 run records with their
   scalars and shared pins; the divergence view (1 claim compared, 0
   divergent; coverage deltas; 192 signs assigned by the full register
   only; the pre-registered-expectations absence statement; the S-R2
   value-independence limit stated where the numbers appear); the five
   hand-derived canonicals as the engine's oracle; and the rules' reach
   stated next to the results (S-R3 UNMEASURED; 839 of 840 claims outside
   any run's reach in v1).

Every element on every screen carries a "Cites:" line naming the ledger,
matrix, register, or run-record ids behind it (Point 5(a)). Layer tags
(Ledger / Matrix / Computed · settling) appear on the elements so the
layers distinction is visible on the surface, not only documented.

### Facts the package rests on (computed from the merged tree at 2bac69cd)

- No System graph screen exists in the current frontend — the nav gains the
  entry as new; T503's "rebuilt" is against Spec 085's draft, not a shipped
  screen. Today's screens are untouched by this package.
- Ledger: 871 lines (840 claims + 31 annotations); status draft 816,
  untested 12, contradicted 4, partially_supported 3, strongly_supported 2,
  partially_falsified 1, unsupported 1, superseded 1; stage created 814,
  explained 8, checked 3, no stage recorded 15 (shown as a bare count only;
  Spec 072's contents are never an element of this surface); populations
  bundle 817 / extracted 23; falsifier 831 present / 9 missing (all
  extracted); aee_state null on 840 of 840.
- Matrix: 840 rows (826 with cells, 14 named empty), 644 columns, 1,363
  cells (supports 1,356, all document cells; opposes 7, all study cells;
  constrains 0); dependency pairs carried as coverage data: 790 (counted
  from matrix.json for this record).
- Anchors register: 287 records; strict 94 (HIGH 90 + MEDIUM 4 by the
  recorded D-A rule; tiers HIGH 166 / MEDIUM 5 / LOW 3 / CANDIDATE 113);
  44 pending_non_sa_validation.
- Settling: assignment sets incumbent 94 / full-register 286, out-of-frame
  record H003 named; T405 runs over the full frame — incumbent 94 contexts,
  94 strict-consistent, 0 conflicts; full-register 286 contexts, 94
  strict-consistent, 192 non-strict, 0 conflicts; per-claim divergences 0.

### A recorded interpretation (for the owner's approval read)

T501's text names claim×sign "a column-class filter." The wireframe
implements sign filtering over **rows** (claims are the rows; there are no
claim×sign columns in the generated matrix to filter), alongside the
column-class filters proper. The difference is named in decisions.md Q5
rather than silently conformed; approving the package approves the
implementation as wired.

### Claim legs assessed at T501 (Stage 5 legs only)

- **C086-16, displayed-score leg: DESIGNED, not established.** The claim
  view wires the score block with the ScoringEngine-only label and its
  honest empty state. The leg is established only when T503 builds the
  surface and T504 verifies the rendered block against the wireframe.
- **C086-17, design leg: satisfied as designed.** The wireframes render the
  gated population's real numbers and cite ids per element; the builder leg
  (artifact values equal the ledger's, gate V5) belongs to T502, and the
  rendered-equality leg to T504.
- **C086-18, design leg: satisfied as designed.** The stamp line and STALE
  marking are wired on every screen; the build legs belong to T502/T503.
- **C086-19: no T501 leg beyond design.** The wireframes keep the signed-in
  shell and the build-stamp chip; scoping is an API property T503 builds
  and its tests prove.

### Seat and scope

Records only: no builder code, no surface changes, no map artifacts, no
.py touched. The worker does not merge; the branch and clone are kept for
the approval cycle. Nothing in this package pre-authorizes T502–T505.

**AI disclosure:** executed by an AI agent (Muse, via Muse) at the
direction of Tristen Pierson, per constitution sec. VI.
