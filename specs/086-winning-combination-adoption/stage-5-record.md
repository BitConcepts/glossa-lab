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

## T502 — Map builder: the approval act, then the build

**The approval act (recorded first, as the act that opens this task).**
On 2026-11-02, in the Glossa-Lab chat, the owner approved the T501
wireframes package **as a block, Q1–Q8 as recommended**. That act is
T501's acceptance (its gate was the owner's approval on the actual
screens), and the T501 checkbox in tasks.md is ticked complete on
this act. The wireframes are the requirements for T502–T504: any
place the build cannot honor them as drawn stops the step and is
reported; it is never absorbed silently.


### T502 — built (2026-11-02)

- **Definitions registered first**: `glossa-indus/map/DEFINITIONS.md`
  carries map-defs v1 (inputs, artifact form, the Q3 header
  contract, the edge-citation rule, the Q4 nearest-items rule, the
  census rule, the amendment discipline). The builder
  (`backend/glossa_lab/map_generate.py`, pure builder + thin write
  wrapper, the matrix pattern) and the gate's registered copies
  implement it; the agreement test pins the copies to each other.
- **The builder** reads the ledger and the gate-verified layers
  only: it refuses, naming the mismatch, when the published
  matrix's as-of stamp names another ledger build, and when a
  stored run record is pinned to another build. It never reads
  hand-authored data. CLI: `tools/ledger/generate_map.py`
  (`--check`, `--gated`). Publication is through
  `gated_publish.publish_map` (candidate → gate → replace only
  on ALL PASS).
- **The artifact** (`glossa-indus/map/map-data.json`, 4,482,667
  bytes, sha256 415425d7a6b9f60057d3ad744069a0a8177cb9c4a6e6b614ac3e3cfb679395dd):
  1,484 elements (840 claims + 644 columns), 1,363 edges (one per
  matrix cell), the header exactly as Q3 approved it (claims by
  status; validated-anchor share 94 of 287 = 0.3275; nearest
  dated items per Q4 — 2026-10-25 study 054, 2026-10-24 study
  052 ×4, 2026-10-24 study 074; the 44 pending as a count with
  its reason), the three levels' data with every element citing
  its ledger ids, the matrix view data (incl. the Q5 sign
  row-filter form and the sign×sign block), the settling section
  opening on the stored T405 comparison (Q7), the displayed-score
  slot in its honest empty state (Q6 — `{state: "empty"}` on all
  840 claims; no score computed anywhere), the falsifier census
  (831 of 840; the 9 gaps named), the mahadevan:64/70/72
  divergence data (Q8), S-R3 labeled UNMEASURED, empty states
  for the 14 cell-less claims and the unresolved mentions.
- **The edge-citation rule** (registered in map-defs §5, found
  necessary by this build): an edge carries the cell's citations
  that individually carry the relation. Exactly one live cell is
  affected — yadav × study 054, whose cell cites both the
  superseded 2026-10-24 outcome append and the governing
  2026-10-25 append; the edge carries the governing pointer
  only, the cell keeps both, labeled. See the C086-21 pattern
  note at the end of this record.
- **The gate's map legs are live**: V2's map-header leg, V4 over
  the map's edges (with the edge census), V5's full map
  recomputation by the gate's own route under its registered
  map-defs v1 copies (in addition to the Stage 3 trace leg),
  V6's map-header leg, V7's lossless regeneration over the map
  artifact, and V9's writer census naming the map writer. The
  census rule is in force: on the clean tree the map classes
  report their live counts, and the two zero-instance
  sub-populations (corpus_texts elements, constrains edges) are
  reported UNPROVEN on the live population in the gate output
  itself, with their teeth on fixtures in the battery.
- **Teeth** (backend/tests/test_spec086_ledger_gate.py, Stage 5
  section; the whole battery is 47 tests, all passing): the
  registered-copies agreement test; a clean-tree census test;
  V2 header count flip → FAIL; V5 claims-section divergence
  named (the specimen claim's does_not_establish); V5
  settling-section divergence named (a run's assigned_count);
  V5 partial candidate (settling section deleted) → FAIL naming
  the section; V6 header share flip → FAIL; V4 edge citing the
  superseded append → FAIL naming the pointer; V7 hand-edited
  map → FAIL classified downstream-defect, and PASS classified
  intended-change-named when the change is named; gated
  publication of the map plus its negative control (a flipped
  candidate is refused and the published artifact stays
  byte-untouched). Builder/API/scoping tests live in
  backend/tests/test_spec086_map.py (14 tests).
- **Clean-tree end state**: full gate 20 PASS / 0 FAIL / 1
  NOT-RUN (V7, which runs under --regen by the standing design);
  regen gate 23 PASS / 0 FAIL / 0 NOT-RUN. No map class remains
  NOT-RUN. The verbatim outputs follow.

#### Gate output — full (`check_ledger_gate.py --all`), verbatim

```
Ledger gate — glossa-indus chain (Spec 086, Point 4)
mode: full
root: /home/hatch/workspace/glossa-run/spec086-stage5-build
ledger: glossa-indus/ledger/claims.jsonl — 871 lines, canonical sha256 c4e2326ec8757bb700dac0142dd0adf17d7464b4d929f5b103868c9228f13ccf
definitions: matrix-defs v1 (the gate's registered copies); ledger schema: ledger-schema v1
map definitions: map-defs v1 (the gate's registered copies)
settling semantics: glossa-settle-1 (the gate's registered copies); canonicals: glossa-indus/ledger/settling-canonical.json
falsifier coverage: 831 of 840 claim entries carry a falsifier (published on every gate run, C086-5) — by population: bundle 817/817, extracted 14/23
checks:
PASS V1 ledger validity — pinned schema, fingerprints (spec029-phase-i-v1), D-B uniqueness, field provenance, pointers (Stage 1 validator)
  871 lines validate against ledger-schema v1; every fingerprint recomputes; no duplicates
PASS V1 recorded source hashes — every sources[] and sidecar hash verifies (canonical hash)
  1686 recorded hashes verified against the files on disk via ledger_intake.sha256_file
PASS V2 count equivalence — claims by status: ledger == matrix
  840 claims; counts equal
PASS V2 count equivalence — claims by stage: ledger == matrix
  840 claims; counts equal
PASS V2 count equivalence — claims by population: ledger == matrix
  840 claims; counts equal
PASS V2 count equivalence — falsifier coverage block: ledger == matrix
  matrix carries {'covered': 831, 'total': 840, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 817, 'total': 817}}}; recomputed {'covered': 831, 'total': 840, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 817, 'total': 817}}}
PASS V2 count equivalence — claims by status: ledger == map header
  map header carries {'contradicted': 4, 'draft': 816, 'partially_falsified': 1, 'partially_supported': 3, 'strongly_supported': 2, 'superseded': 1, 'unsupported': 1, 'untested': 12}
  census: 840 claims counted across 8 statuses in the map header
PASS V3 matrix recomputation — cells cell-for-cell (relation, citation ids, derivation rule id)
  1363 cells recomputed from the ledger by the gate's own route; every cell equal
PASS V3 matrix recomputation — rows, columns, coverage, as-of stamp, sign×sign block
  rows, columns, coverage, the as-of stamp and the sign×sign block all equal the gate's recomputation
PASS V4 relation-carrying citations — every citation ties under T1–T4 (incl. the numeric arm)
  1363 matrix cells and 1363 map edges checked; 4090 citations required to carry their relation under T1–T4
  numeric arm: 0 citations in the live population carry a measurement with a machine-readable bound (the arm is exercised on fixtures in the teeth battery)
  map edge census: supports 1356, opposes 7, constrains 0
  UNPROVEN on the live population: constrains map edges — 0 live instances (the class is empty in the artifact and says so; its teeth are fixtures in the battery)
PASS V5 map recomputation — elements trace, embedded fields equal, loads block deep-equals the matrix's
  1484 elements trace to ledger ids; loads block equal
PASS V5 map recomputation — full artifact, the gate's own route (map-defs v1 copies)
  every section of the map artifact equals the gate's recomputation from the ledger (header, elements, edges, loads, matrix, system, claims, settling)
  census: 840 claim elements; column elements by class: studies 10, documents 316, research_checks 31, anchors 287, corpus_texts 0
  census: 1363 map edges by relation: supports 1356, opposes 7, constrains 0; 840 per-claim records; 2 stored settling runs recomputed
  UNPROVEN on the live population: corpus_texts elements — 0 live instances (the class exists in the definitions and carries no columns in v1; its teeth are fixtures in the battery)
  UNPROVEN on the live population: constrains edges — 0 live instances (the relation class is empty in the generated matrix and the artifact says so; its teeth are fixtures in the battery)
PASS V6 anchor shares — strict set recomputes under the recorded D-A rule (strict_sa_independent_hm)
  strict anchors: 94 of 287; strict share 0.3275; validated-anchor share (the strict share, spec.md Point 5) 0.3275; rule version as recorded: Phase-109 follow-through (spec 007, 2026-10-06) applying the Phase-108 strict definition
PASS V6 anchor shares — map header leg
  map header shares equal the recomputation
  census: the share is computed over 287 register records, 94 of them strict
NOT-RUN V7 lossless regeneration
  runs under --regen (the push CI job runs it)
PASS V8 settling canonicals — scenarios reproduce under the gate's own glossa-settle-1 route
  5 registered canonical scenarios reproduced exactly under the gate's own glossa-settle-1 route (S-R4 result blocks, field-for-field), over provenance pins that verify against this tree
PASS V8 settling canonicals — the registered comparison reproduces
  comparison incumbent-vs-full-register-over-subset reproduced exactly (claims compared, per-claim divergences, coverage deltas, signs assigned by one only, expectations named); the expectations note is checked on its mechanically derivable part — the absence clause matches verbatim; the registered note's remainder is brief-specific prose (FINDING-S4-1, stage record)
PASS V8 scenario/verdict separation — the settling layer carries no reachable ledger write path
  1 settling/scenario module(s) scanned; none imports or reaches a ledger write path (append_entry, write_ledger, write_matrix) — the settling layer's outputs are computed records, never ledger verdicts
PASS V9 no write path — gate import hygiene
  the gate modules import no write entry point (append_entry, write_ledger, write_matrix) and contain no write call
PASS V9 no write path — settling/scenario import audit
  1 settling/scenario module(s) audited; none imports a ledger write path
PASS V9 no write path — matrix/map writer census
  writers of the gated artifacts: ['backend/glossa_lab/gated_publish.py', 'backend/glossa_lab/map_generate.py', 'backend/glossa_lab/matrix_generate.py']
  readers (no write call): 4 module(s)
  census scope: backend/glossa_lab, backend/scripts, tools (test code writes fixtures under tmp dirs by design and is not a publication path)
summary: 20 PASS / 0 FAIL / 1 NOT-RUN
RESULT: PASS
```

#### Gate output — regen (`check_ledger_gate.py --regen`), verbatim

```
Ledger gate — glossa-indus chain (Spec 086, Point 4)
mode: full + regen
root: /home/hatch/workspace/glossa-run/spec086-stage5-build
ledger: glossa-indus/ledger/claims.jsonl — 871 lines, canonical sha256 c4e2326ec8757bb700dac0142dd0adf17d7464b4d929f5b103868c9228f13ccf
definitions: matrix-defs v1 (the gate's registered copies); ledger schema: ledger-schema v1
map definitions: map-defs v1 (the gate's registered copies)
settling semantics: glossa-settle-1 (the gate's registered copies); canonicals: glossa-indus/ledger/settling-canonical.json
falsifier coverage: 831 of 840 claim entries carry a falsifier (published on every gate run, C086-5) — by population: bundle 817/817, extracted 14/23
checks:
PASS V1 ledger validity — pinned schema, fingerprints (spec029-phase-i-v1), D-B uniqueness, field provenance, pointers (Stage 1 validator)
  871 lines validate against ledger-schema v1; every fingerprint recomputes; no duplicates
PASS V1 recorded source hashes — every sources[] and sidecar hash verifies (canonical hash)
  1686 recorded hashes verified against the files on disk via ledger_intake.sha256_file
PASS V2 count equivalence — claims by status: ledger == matrix
  840 claims; counts equal
PASS V2 count equivalence — claims by stage: ledger == matrix
  840 claims; counts equal
PASS V2 count equivalence — claims by population: ledger == matrix
  840 claims; counts equal
PASS V2 count equivalence — falsifier coverage block: ledger == matrix
  matrix carries {'covered': 831, 'total': 840, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 817, 'total': 817}}}; recomputed {'covered': 831, 'total': 840, 'by_population': {'extracted': {'covered': 14, 'total': 23}, 'bundle': {'covered': 817, 'total': 817}}}
PASS V2 count equivalence — claims by status: ledger == map header
  map header carries {'contradicted': 4, 'draft': 816, 'partially_falsified': 1, 'partially_supported': 3, 'strongly_supported': 2, 'superseded': 1, 'unsupported': 1, 'untested': 12}
  census: 840 claims counted across 8 statuses in the map header
PASS V3 matrix recomputation — cells cell-for-cell (relation, citation ids, derivation rule id)
  1363 cells recomputed from the ledger by the gate's own route; every cell equal
PASS V3 matrix recomputation — rows, columns, coverage, as-of stamp, sign×sign block
  rows, columns, coverage, the as-of stamp and the sign×sign block all equal the gate's recomputation
PASS V4 relation-carrying citations — every citation ties under T1–T4 (incl. the numeric arm)
  1363 matrix cells and 1363 map edges checked; 4090 citations required to carry their relation under T1–T4
  numeric arm: 0 citations in the live population carry a measurement with a machine-readable bound (the arm is exercised on fixtures in the teeth battery)
  map edge census: supports 1356, opposes 7, constrains 0
  UNPROVEN on the live population: constrains map edges — 0 live instances (the class is empty in the artifact and says so; its teeth are fixtures in the battery)
PASS V5 map recomputation — elements trace, embedded fields equal, loads block deep-equals the matrix's
  1484 elements trace to ledger ids; loads block equal
PASS V5 map recomputation — full artifact, the gate's own route (map-defs v1 copies)
  every section of the map artifact equals the gate's recomputation from the ledger (header, elements, edges, loads, matrix, system, claims, settling)
  census: 840 claim elements; column elements by class: studies 10, documents 316, research_checks 31, anchors 287, corpus_texts 0
  census: 1363 map edges by relation: supports 1356, opposes 7, constrains 0; 840 per-claim records; 2 stored settling runs recomputed
  UNPROVEN on the live population: corpus_texts elements — 0 live instances (the class exists in the definitions and carries no columns in v1; its teeth are fixtures in the battery)
  UNPROVEN on the live population: constrains edges — 0 live instances (the relation class is empty in the generated matrix and the artifact says so; its teeth are fixtures in the battery)
PASS V6 anchor shares — strict set recomputes under the recorded D-A rule (strict_sa_independent_hm)
  strict anchors: 94 of 287; strict share 0.3275; validated-anchor share (the strict share, spec.md Point 5) 0.3275; rule version as recorded: Phase-109 follow-through (spec 007, 2026-10-06) applying the Phase-108 strict definition
PASS V6 anchor shares — map header leg
  map header shares equal the recomputation
  census: the share is computed over 287 register records, 94 of them strict
PASS V7 lossless regeneration — matrix.json
  byte-identical after regeneration (sha256 b3cdbf49e6305ae771468f26858678db568d1b58cb0b200e55b92810adb29849)
PASS V7 lossless regeneration — matrix.md
  byte-identical after regeneration (sha256 7c963ff55c38d4dc9a52d240dacb03da0f2eebfaff5411cc398144727140b255)
PASS V7 lossless regeneration — map data
  byte-identical after regeneration (sha256 415425d7a6b9f60057d3ad744069a0a8177cb9c4a6e6b614ac3e3cfb679395dd)
PASS V8 settling canonicals — scenarios reproduce under the gate's own glossa-settle-1 route
  5 registered canonical scenarios reproduced exactly under the gate's own glossa-settle-1 route (S-R4 result blocks, field-for-field), over provenance pins that verify against this tree
PASS V8 settling canonicals — the registered comparison reproduces
  comparison incumbent-vs-full-register-over-subset reproduced exactly (claims compared, per-claim divergences, coverage deltas, signs assigned by one only, expectations named); the expectations note is checked on its mechanically derivable part — the absence clause matches verbatim; the registered note's remainder is brief-specific prose (FINDING-S4-1, stage record)
PASS V8 scenario/verdict separation — the settling layer carries no reachable ledger write path
  1 settling/scenario module(s) scanned; none imports or reaches a ledger write path (append_entry, write_ledger, write_matrix) — the settling layer's outputs are computed records, never ledger verdicts
PASS V9 no write path — gate import hygiene
  the gate modules import no write entry point (append_entry, write_ledger, write_matrix) and contain no write call
PASS V9 no write path — settling/scenario import audit
  1 settling/scenario module(s) audited; none imports a ledger write path
PASS V9 no write path — matrix/map writer census
  writers of the gated artifacts: ['backend/glossa_lab/gated_publish.py', 'backend/glossa_lab/map_generate.py', 'backend/glossa_lab/matrix_generate.py']
  readers (no write call): 4 module(s)
  census scope: backend/glossa_lab, backend/scripts, tools (test code writes fixtures under tmp dirs by design and is not a publication path)
summary: 23 PASS / 0 FAIL / 0 NOT-RUN
RESULT: PASS
```

### T503 — the surface (2026-11-02)

- **API**: `backend/glossa_lab/api/indus_map.py`, mounted at
  `/api/v1/indus-map`, serves the published artifact's sections
  exactly as published (header/system/matrix/settling/claim/
  evidence). The only value computed at serve time is the stale
  flag (C086-18): the artifact's as-of ledger hash against the
  ledger's current hash. Responses carry the map's sha256.
- **Scoping (C086-19)**: `cloud_scope` resolves the indus-map
  resource to the primary workspace (indus-script), like
  indus-evidence. The battery's oracle: an actor whose roles
  name another workspace receives the scoped 404
  (`{"detail": "Not found"}`) on every map route, with no map
  element in the body; a member reads the map. Desktop/token
  mode serves behind the existing API-token middleware.
- **Surface**: a new "System graph" tab (Program group, after
  Experiments, with the wireframe's "new" chip) rendering
  `frontend/src/components/SystemGraphView.tsx` — the five
  screens from the served artifact, no client-side
  recomputation of any gated value, no graph canvas (Q1). The
  header strip and stamp line ride every screen; the STALE
  marking renders when the stamp's ledger hash stops matching.
- **Guards**: the Spec 029 guard testids live on the program
  home and were not touched; the surface's own testids are new
  and distinct (indus-map-header, indus-map-stamp,
  indus-map-standing-position). **No existing frontend test was
  changed.** One new e2e file
  (`frontend/e2e/system-graph.spec.ts`, 3 tests); the
  navigation, program-home and Spec 029 guard suites (42 tests)
  pass unchanged.
- One judgment recorded: the signary sizes in the system view's
  callout (557 / 527 / 584) are the approved wireframes' surface
  copy; no machine-readable source exists in the gated chain,
  so they are not artifact data (see D5 in the T504 comparison).

### T504 — verification (2026-11-02)

Playwright renders of all five screens at desktop (1440) and
mobile (390), compared screen by screen against the approved
wireframe renders. The full comparison — served-identity
check (the stamp line "map data · ledger c4e2326e… · fresh",
a marker only the new build carries, asserted before any
shot), per-screen results, five named differences (D1–D5, data
governing in every case), and the defects found and fixed
in-PR — is filed at
`records/stage-5-build/comparison.md`, with the shots in
`records/stage-5-build/shots/` and the capture script beside
them. Headline: all five screens match the approved wireframes
in structure and data; D1 is the one numeric difference (the
header's validated share renders the artifact's 94/287 =
32.8%; the wireframe's strip printed 32.9%, the 286-frame
share — the artifact governs under C086-17).

### T505 — closeout: the Spec 085 audit re-scored (2026-11-02)

The audit (goal workspace
`hidden_files/graph-matrix-audit-2026-11-01.md`, Spec 085)
scored the owner's sentence in four parts and listed six gaps.
Re-scored against the built chain (ledger → matrix → gate →
settling → map → surface), none inflated:

**The four parts.** (a) System as graph nodes: NO → **PARTIAL**
— one generated, gate-verified graph (1,484 elements, 1,363
edges) now spans claims and evidence (documents, studies,
anchors, research checks) with signs joined by identifier; it
is a view over the ledger by design, not a graph store, and
reports/experiments/discovery items are not nodes in it.
(b) Matrix form: PARTIAL → **YES for claims×evidence** — a
claim×evidence matrix is generated, persisted, gate-verified
cell-for-cell, served, and rendered; claim×sign exists only
as the Q5 row-filter (1 claim carries sign_refs).
(c) Digestion surface: PARTIAL → **YES for the map and
matrix** — the System graph surface renders them as the
program's primary map. (d) Projected-constraint engine:
NO → **PARTIAL** — a mechanical constraint-settling engine
(glossa-settle-1) runs in the product over ledgered relations
with computed coverage, conflicts and forced consequences,
gate-verified; it is not the Spec 076/078 projected-constraint
corpus model, which remains two closed studies, and its
positional-class rule (S-R3) remains UNMEASURED.

**The six gaps.**
1. *One entity graph* — **partially closed.** A single
   generated graph over the epistemic core exists and is the
   primary surface, every element citing ledger ids; not a
   graph store, and not spanning reports/experiments/discovery.
2. *Edges for the live claim population* — **partially
   closed.** 1,363 typed claim→evidence edges now exist for
   all 840 claims, gate-verified; claim→claim dependency pairs
   (790) are carried as coverage data, expressly not edges
   (Q1), and extracted claims still carry no depends_on /
   conflicts_with fields for the AEE graph.
3. *A matrix layer* — **closed.** The claims×evidence matrix
   is generated from the ledger, persisted, served through the
   API, and recomputed cell-for-cell by the gate on every run;
   the sign×sign block rides the same artifact.
4. *A graph/matrix surface in the SPA* — **closed as
   approved.** The surface exists (five screens). The audit's
   literal forms (a node-link canvas, heatmaps) were put to
   the owner as Q1 and declined: relations render as words in
   tables. On the audit's literal terms this is partial; on
   the program's ratified terms it is closed.
5. *An actual projected-constraint engine in the product* —
   **partially closed.** The settling layer is a real
   in-product engine of the kind the Winning Combination
   specifies (assignments settled mechanically over the
   matrix, dual readings under interchangeability, the gate
   recomputing every result). The Spec 076/078 engine as such
   was not built; the phase-14 stub is untouched; S-R3 is
   UNMEASURED for want of a positional-class table.
6. *Join the two graph worlds* — **partially closed.** Claims
   and signs share identifiers where the ledger carries them:
   sign_refs resolve through the register under the settling
   key, and the map names the matrix key's non-resolution
   instead of hiding it (Q8). The joined population is one
   claim of 840; claim text is not identifier-linked.

### Claim assessments — Stage 5 legs

- **C086-15 (map leg) — established.** The map carries the two
  stored runs over identical pins (ledger c4e2326e…, corpus
  08fc96c8…, anchors df0cf620…), the per-claim divergence list
  (1 compared, 0 divergent), and the expectations absence
  statement generated by the comparison itself; the gate
  re-settles both runs and recomputes the comparison on every
  run (V5 full leg, V8), so a pin or result divergence fails
  the gate by name.
- **C086-16 — established, including the displayed-score
  leg.** Settling writes only run records (the panel's
  computed-layer callout states it; V8's separation arm and V9
  prove no write path); the displayed-score slot carries
  `{state: "empty"}` on all 840 claims — aee_state is null on
  the whole population — rendered under the one permitted
  label and never as a number.
- **C086-17 — established.** The surface renders the published
  artifact as served; the gate recomputes the artifact
  section-for-section (V5), so what the surface can serve is
  what the ledger generates. T504's comparison found one
  wireframe number the artifact contradicts (D1) and the
  surface follows the artifact.
- **C086-18 — established.** Every response carries the as-of
  stamp (source hashes and versions, no wall clock); the
  surface marks the map STALE when the stamp's ledger hash
  stops matching the ledger's current hash (the flag is
  computed at serve time and unit-tested in its fresh state;
  the stale state's rendering is the same code path with the
  flag true).
- **C086-19 — established.** The indus-map resource resolves
  to the primary workspace; the scoping oracle in the battery
  shows an out-of-scope actor receiving the scoped 404 on
  every route with no map element in the body, and in-scope
  responses contain only the primary workspace's artifact.
- **C086-20 — established for Stage 5.** No claim's status,
  stage, or standing-position text was changed by this stage:
  the ledger is byte-identical to Stage 4's (sha256
  c4e2326e…), and the standing position leads the surface as
  a callout, unmodified.
- **C086-21 — exercised; one refinement written up for
  delivery.** This stage produced one transferable refinement,
  stated here as the pattern note so the owning chat can
  deliver it to the RCPH and Atlas chats: **when a cell cites
  both a superseded record and its governing successor, an
  edge derived from the cell carries only the citations that
  individually carry the relation (the governing record); the
  superseded citation stays on the cell, labeled.** This is
  Amendment 1 applied at the edge layer: a citation list is a
  claim, and an edge that carried the superseded pointer would
  assert a relation that record no longer carries. The census
  discipline was also exercised on a third artifact class
  (zero-instance sub-populations reported UNPROVEN in the gate
  output, not silently passed). No incoming pattern note was
  pending against this stage; nothing in this build conflicts
  with a ratified local decision.

**Seat and scope.** Records, the map chain, and the surface:
no ledger line changed, no verdict moved, main untouched. The
worker does not merge; the branch and clone are kept for the
gate-and-merge cycle. **Stage 5 completes Spec 086** when this
PR merges (see the root LEDGER.md entry).

**AI disclosure:** executed by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per constitution sec. VI.
