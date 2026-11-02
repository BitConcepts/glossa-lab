# Map definitions — `map-defs v1`

Spec 086 (winning-combination adoption), Point 5, task T502.
This document is the contract the map builder runs under: the
map artifact's sections, the header contract, the edge form,
and the evidence assembly are registered here, versioned, and
are the only ones the builder may use. A machine copy of every
rule in this document lives in the builder
(`backend/glossa_lab/map_generate.py`); the verification gate
(`backend/glossa_lab/ledger_gate.py`) carries its own
registered copies and recomputes the artifact by its own
route (gate check V5). A deliberate change to any definition
is made in all copies in the same motion (§11).
Acceptance for this document is human-as-oracle: a reviewer
reads the definitions as the contract they are. *This does
not establish the definitions are the right presentation —
it establishes they are written down, versioned, and the
only ones the builder may use.*

**The honesty split, stated once.** "The map is generated,
never made" holds for the data. The definitions in this
document are human-registered — the same split the matrix
carries (`glossa-indus/matrix/DEFINITIONS.md`). Every value
in the map artifact is either copied verbatim from a named
source record or computed by a rule below from such records.
Where the record carries nothing, the map carries an explicit
empty state and counts the gap. The map holds no status,
stage, or score of its own: it displays the ledger's values
or nothing (spec.md Point 6, D-E). The map renders the
program's epistemic state; the standing position — the Indus
script is not deciphered — is untouched by anything here
(C086-20).

## 1. Inputs — the verified layers and records

The builder reads only:

- the **ledger** (`glossa-indus/ledger/claims.jsonl`), the
  sole entry point of the whole chain;
- the **gated matrix artifact** (`glossa-indus/matrix/
  matrix.json`), read as published — the map derives from
  the matrix the gate verifies, never from a private
  recomputation the gate has not seen;
- the **source records the ledger entries name** in
  `sources[]` and annotation sidecars, read only after
  their canonical hash verifies against the hash the entry
  records (the chain's standing rule; a mismatch refuses
  generation);
- the **canonical anchors register**
  (`backend/reports/INDUS_FINAL_ANCHORS.json`) and the
  **Phase-108 provenance register**
  (`reports/phase108_provenance_register.json`), for the
  strict-set recomputation of §3 and the sign records of §7;
- the **settling records of record**: the assignment sets
  (`glossa-indus/ledger/assignment-sets.json`), the stored
  run records (`glossa-indus/ledger/runs/*.json`), the
  filed dual-run comparison record
  (`specs/086-winning-combination-adoption/records/
  stage-4-dual-run-comparison.json`), and the registered
  canonicals (`glossa-indus/ledger/settling-canonical.json`).

No other input exists. In particular the builder reads no
application database and no app entity (approved decision
D-086-Q1: reports and other app entities are not map
elements).

## 2. Artifact form

One artifact: `glossa-indus/map/map-data.json`, serialized
as `json.dumps(..., ensure_ascii=False, indent=1)` plus a
trailing newline, UTF-8, LF endings — the matrix artifact's
serialization, so delete-and-regenerate over unchanged
inputs is byte-identical. Top-level sections, in order:
`artifact`, `generated_from`, `generated_by`, `header`,
`elements`, `edges`, `loads`, `matrix`, `system`, `claims`,
`settling`. Each section below names its rule.

## 3. The header (Point 5(b); decisions Q3, Q4)

The header carries exactly the spec's three items, computed,
never typed:

- **`claims_by_status`** — the count of ledger claim entries
  by their `status` field, as a `{status: count}` object.
  (Gate V2's map leg compares this object against the
  ledger.) The header also carries `claims_total`.
- **Validated-anchor share** — the strict share: the strict
  set recomputed from the canonical anchors register under
  the rule the register itself records (rule id
  `strict_sa_independent_hm`: confidence in {HIGH, MEDIUM}
  AND the Phase-108 register category not in the SA-lineage
  set AND the register's `sa_in_chain` false), over all
  register records. Carried under both names the gate's V6
  map leg reads — `validated_anchor_share` and
  `strict_anchor_share` — as the full-precision quotient,
  with `anchors_strict` and `anchors_total` beside it.
- **Nearest dated items** (Q4) — the genuinely dated things
  near the present are the study-outcome blocks stored in
  the claims' own source records. The rule: take every
  (claim, study) pair's **governing** outcome block (the
  latest-dated block for that pair under the matrix-defs
  total order; ties break by pointer) whose recorded outcome
  **bears** a relation under the matrix outcome table;
  group those blocks by (date, study, outcome); order the
  groups by date descending, then study ascending; the
  header carries the **first three groups**, each as
  `{date, study, outcome, relation, claims}` with the
  bearing claims named. Beside the groups, **`pending_validations`** —
  the count of register records whose `validation_status`
  is `pending_non_sa_validation`, with the reason stated:
  the register records no review dates for them, so they
  appear as a count, not as dated items (Q4).
- **`as_of`** — the stamp of §9.

The falsifier-gap census is **not** a header item (Q3): it
lives on the system view (§6), and the gate prints it on
every run.

## 4. Elements and loads (the gate's trace surface)

- **`elements`** — one element per ledger claim
  (`{kind: "claim", id, statement, status, stage,
  population}`, the four embedded fields copied verbatim
  from the ledger entry) and one per matrix column
  (`{kind: <column class>, id}`), claims first in ledger
  order, then columns in the matrix's column order. Every
  element traces to a ledger id (Point 5(a)).
- **`loads`** — for every matrix row, the count of its
  cells by relation: `{row id: {supports, opposes,
  constrains}}`, zero-filled. (Gate V5 deep-compares this
  block against the matrix's rows and cells.)

## 5. Edges — one per matrix cell, citations that carry

- **`edges`** — exactly one edge per matrix cell:
  `{from: <column id>, to: <row (claim) id>, rel:
  <relation>, rule: <derivation rule>, column_class:
  <class>, citations: [...]}`. The edge set is the matrix's
  cell set in edge form; there are no other edges. The 790
  claim×claim dependency pairs are coverage data (§6's
  matrix section carries them inside the coverage block);
  they are **not** edges and never render as relations.
  No claim×sign edge exists (there are no claim×sign cells).
- **The edge-citation rule.** An edge asserts its relation;
  under Amendment 1 (a citation can exist, be relevant, and
  still not carry the relation) an edge's citations are
  exactly the cell's citations **that individually carry
  the relation** under the gate's tie rules T1–T4:
  - R1/R2 cells: the cell's citations, unchanged.
  - R3 cells: the claim id and the **governing** block's
    pointer only. A superseded block is cited by the cell
    (the full trail stays in the embedded cell, §6, labeled
    by its date) but it does not carry the relation — the
    governing block does — so it is not an edge citation.
    On the current population exactly one cell's edge
    citation set is a proper subset of its cell's: the
    yadav_2009_arxiv_manual_002 × 054 cell.
  Gate V4 checks every edge citation against the tie rules;
  an edge citation that does not tie fails the gate.

## 6. The matrix section and the system view

- **`matrix`** — the gated matrix artifact's `rows`,
  `columns`, `cells`, `coverage`, and `sign_sign_block`,
  carried verbatim. The map republishes the gated matrix's
  contents inside its own gated artifact so the surface
  reads one artifact; the gate's V5 route recomputes each
  of these from the ledger by its own route and compares.
- **`system`** — the system view's data, all computed:
  - `sign_inventory`: the settled frame (the frame the
    assignment sets of record name), the register records
    in frame scope (register total minus the sets'
    `out_of_frame_records`, which are named, not dropped),
    and per set of record: assignment count and its share
    of the frame scope.
  - `matrix_coverage`: cells total, cells by relation and
    by class, rows total / with cells / the empty rows
    named, columns by class, the unused columns by class,
    the conflict hotspots (every opposes cell: row, column,
    study), the study columns carrying only non-bearing
    governing outcomes, and the dependency-pairs count
    labeled as coverage data, not cells.
  - `claim_population`: counts by status, by stage, by
    population; the count of claims with **no stage
    recorded**, as a bare count only (Spec 072's contents
    are never an element of this surface).
  - `falsifier_census`: covered / total, by population,
    and the gap claim ids named.
  - `aee_state_census`: how many claims carry an AEE state
    (today: none of 840) — the population fact behind the
    claim view's displayed-score empty state (§7).
  - `unresolved`: the prose sign mentions verbatim
    (`{record, source, mention}` — a work list; no edge,
    cell, or link is made from words) and the sign
    references with no anchor record under the matrix's
    key (`{row, sign_ref, reason}`), both from the matrix
    coverage block.
  - `sign_sign_block_summary`: the block's node count,
    reported edge count, emitted edge count, community
    count, and corpus hash — both edge numbers carried,
    labeled (the block itself is in the `matrix` section).

## 7. The claims section (claim view + evidence view)

One record per ledger claim, keyed by claim id:

- verbatim ledger fields: `statement`, `status`, `stage`,
  `population`, `author`, `author_kind`, `as_of` (the
  claim's own as-of), `date` (the ledger line's date),
  `falsifier` (the list, or null), `does_not_establish`
  (verbatim, or null — a null is an absence the surface
  renders as a counted gap, never a blank), `aee_state`,
  `sign_refs`, `sources` (verbatim).
- `falsifier_counts`: `present` — the count under
  glossa-settle-1's counting rule (a list counts its
  non-empty strings; a string counts one; null counts
  zero). `evaluable` — counted by the settling layer, and
  carried **only where a stored run record counts it for
  this claim** (the claim appears in a run's
  `claims_touched`); otherwise null, and the surface
  states that no stored run counts an evaluable falsifier
  for the claim. The number is never estimated.
- `displayed_score`: the C086-16 slot's data —
  `{state: "recorded", aee_state: <value>}` when the
  ledger carries an AEE state for the claim, else
  `{state: "empty"}`. The map never computes a score; the
  only label a displayed score may carry is the
  ScoringEngine label the claim registers (C086-16).
- `matrix_row`: the claim's cells verbatim (the full
  citation trail, superseded blocks included and labeled
  by the record), and `empty: true` when it has none.
- `settling_bearing`: null when no stored run touches the
  claim; otherwise, per stored run: the candidate, the
  signs it touches the claim via, and the tallies — plus
  the comparison's `divergent` verdict for the claim.
  Tallies are computed outputs of the settling layer, a
  different layer from the ledger fields above.
- `annotations`: the ledger annotation entries targeting
  this claim, verbatim (`id`, `sidecar`, `bearing`) —
  research checks are advisory; their verdict field is
  carried as recorded (null on the whole population).
- `evidence` (the evidence view's data):
  - `column_summary`: per column class, the class's
    column count in the matrix and this claim's cell
    count in that class.
  - `source_document`: the claim's `source_of_record`
    source entry, verbatim. A claim's own document is its
    provenance, never a cell (matrix-defs v1).
  - `sign_records`: one per `sign_refs` entry:
    `{sign_ref, matrix_key, matrix_record: null,
    settle_key, settle_record}` — the two registered key
    constructions side by side. The matrix's R4 key is
    `M` + the sign_ref's number **as written** (no
    zero-padding); the settling layer's key (glossa-
    settle-1 §2) is the frame prefix + the number
    **zero-padded to three digits**. Where the two
    constructions resolve differently, `divergence: true`
    and the surface names it on the screen (decision Q8).
    `settle_record` carries the register record's
    `reading`, `confidence` (**verbatim**, never
    converted to a number), and `validation_status`, plus
    `strict` from the §3 strict-set recomputation — or
    null when no record exists under the settle key.

## 8. The settling section

- `label` — the run records' own label, verbatim:
  "Computation over ledgered relations under
  glossa-settle-1 semantics. Establishes what the ledger
  implies under these rules, not what the script says."
- `semantics` — `glossa-settle-1`.
- `assignment_sets` — per set of record: id, frame,
  assignment count, provenance source; the register pin
  (path, raw sha256, records, strict); the out-of-frame
  records named.
- `runs` — one per stored run record, ordered with the
  incumbent first and the rest by record id (the order the
  panel presents):
  the record id (the file's stem), scenario, candidate,
  the record's `pins` verbatim, and from its `result`:
  `scope_signs`, `assigned_count`, `assigned_share`,
  `contexts_touched`, `strict_contexts`, `consistent`,
  `non_strict_contexts`, the conflicts **list** verbatim,
  `strict_agreement_share`, `claims_touched` verbatim,
  `forced` verbatim, and `s_r3` verbatim. The panel opens
  on the stored T405 pair (decision Q7): the first two
  run records of the store.
- `comparison` — the filed comparison record: its path,
  its sha256, and its `result` verbatim (claims compared
  with both tallies and the divergent flag, per-claim
  divergences, coverage deltas, signs assigned by one
  only, pre-registered expectations and the record's own
  absence statement).
- `canonicals` — the registered canonical scenarios: per
  scenario, `id`, `title`, and the `expected` result
  block verbatim, with the canonical file's path and
  sha256. (Gate V8 re-derives these on every run; the map
  carries them as the panel's oracle display.)
- `reach` — the rules' stated reach: claims carrying
  sign_refs (counted from the ledger), claims no run can
  touch (total minus that count), and the S-R3 statement:
  the positional-class rule's status as the run records
  carry it (`s_r3.class_table` null = no positional-class
  table exists in the record; the rule is registered but
  inert and reports a determinate zero — labeled
  **UNMEASURED** on the surface, never estimated).

## 9. As-of stamp (D-D, generalized)

The header's `as_of` carries: the ledger's canonical
content hash, line count, and latest entry date; the
definition versions in force (`ledger-schema v1`,
`matrix-defs v1`, `map-defs v1`, `glossa-settle-1`); and
the content hashes of the gated inputs the map was
computed from (the matrix artifact, the anchors register
raw-bytes hash, the assignment sets, the comparison
record, the canonicals). There is **no wall-clock
generation time**: delete-and-regenerate byte-identity is
the acceptance shape (the matrix's §9 rule), and the
stamp's purpose is to name the data the artifact was
computed from. A surface showing a map whose stamp hash
does not match the current ledger marks it **STALE**
(C086-18).

## 10. The census rule (gate output)

Every map check class in the gate (V2 map-header leg, V4
over map edges, V5 map recomputation, V6 map-header leg,
V7 map regeneration) states in its evidence the **live
instance count** behind it. A class — or a named
sub-population, such as constrains edges or corpus-text
elements — with **zero** live instances is reported in the
gate output as **UNPROVEN on the live population**, never
silently counted as passing; its teeth live in the test
battery on fixtures. On the current population the empty
sub-populations are named in the stage record's census.

## 11. Amendment discipline

A change to any rule in this document is a new definitions
version (`map-defs v2`, …), made in this document, in the
builder's machine copy, and in the gate's registered copies
in the same motion, and recorded in the spec's stage
record. Artifacts generated under an older version are
stale by their stamp (§9) until regenerated and
re-published through the gate.
