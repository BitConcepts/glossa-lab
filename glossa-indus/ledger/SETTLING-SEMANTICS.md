# Settling semantics — `glossa-settle-1`

Spec 086 (winning-combination adoption), Point 3, task
T401. This document **registers** the settling semantics
before any settling code exists (derive-before-build,
C086-13, adopting the Atlas pattern note
`PATTERN-NOTE-2026-11-01-gate-and-settle`): the semantics
are written here first, the canonical outputs are derived
by hand in `settling-canonical.json` beside this document,
the engine is written last (T403), and its test must
reproduce every canonical exactly (T404). Acceptance for
this document is human-as-oracle — the owner or a named
reviewer reads the semantics as the contract they are.
*This does not establish the rules are the right rules —
each carries its grounding so a reviewer can disagree in
the open.* (tasks.md T401, carried verbatim.)

**Standing position.** The Indus script is not
deciphered. Nothing computed under these semantics is a
decipherment claim, a reading, or evidence about the
script. Every settling output, in every surface, carries
the label:

> Computation over ledgered relations under
> glossa-settle-1 semantics. Establishes what the ledger
> implies under these rules, not what the script says.

**The Atlas's constants are not lifted.** The Atlas's
settle-1 constants — window breaks at 3+ broken feeders,
or 2+ with the amplifier as the third leg — are
Atlas-specific, grounded in that study's ledgered claims,
and are expressly **not** adopted here (the Atlas note's
own limit, carried in spec.md Point 3). No numeric
threshold from the Atlas's semantics appears in this
document. glossa-settle-1's rules are derived from
Glossa's own record: the anchor tiers and the strict-set
rule of Spec 029 decision D-A (ratified 2026-10-12), and
the Spec 073/074 precedent, as spec.md Point 3 states it,
of testing on a frozen classification surface — settling
reads a hash-pinned register state, never a moving one.

**The layers distinction (harmonization adoption 3,
item 3 — binding design input for this stage).**
Computed settling outputs and ledger verdicts/digestions
are **different layers**; neither overrides the other in
the record. A settling output is not a claim, never
enters the ledger, and moves no status, stage, score, or
weight (C086-16); anything a run appears to discover
re-enters only through Point 1 intake. Mechanically, the
settling package has no write path to the ledger (gate
check V9 audits the imports). A run's outputs live
downstream of the ledger, gated like the matrix.

## 1. Inputs — the registers a run reads

A settling run reads exactly the following, each pinned
by hash in the run record's header:

| Register | Identity | Pin |
|---|---|---|
| The ledger | `glossa-indus/ledger/claims.jsonl` (`ledger-schema v1`) | canonical content hash (the shared helper `glossa_lab.ledger_intake.sha256_file`) + line count — the **ledger build**. At this registration: 871 lines, `c4e2326ec8757bb700dac0142dd0adf17d7464b4d929f5b103868c9228f13ccf`. |
| Canonical anchors | `backend/reports/INDUS_FINAL_ANCHORS.json` | raw-byte SHA-256 + counts. At this registration: 570,344 bytes, `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`; 287 records (286 under the `M` prefix, 1 under `H`); strict set 94 (HIGH 90, MEDIUM 4). |
| Phase-108 provenance register | `reports/phase108_provenance_register.json` | read by the strict-set rule (below); the gate recomputes the strict set from it (check V6). |
| Records of record | the files named in ledger entries' `sources[]` | reached only through an entry's own pointers, only after the canonical hash verifies (the Stage 2 route) — S-R2's outcome blocks live there. |

The strict set is **recomputed**, never trusted from the
stored flags: an anchor is strict iff its `confidence`
is in {HIGH, MEDIUM} **and** its Phase-108 register
category is not in {SA_DERIVED, SA_CONFIRMED_ONLY} **and**
its register record's `sa_in_chain` is false — rule id
`strict_sa_independent_hm`, version as recorded in the
anchors file itself: "Phase-109 follow-through (spec
007, 2026-10-06) applying the Phase-108 strict
definition". The stored `strict_set` flag is a cache of
this join (D-A); the Stage 3 gate verified recomputed ==
stored over all 287 records (V6, 94 of 287, share
0.3275). A run whose recomputation disagrees with the
stored flags refuses — the register is not in the state
its record claims.

## 2. Signs, frames, and identity

- A **sign** is a pair (frame, number). Its
  frame-qualified string form is `frame:number` with the
  number in unpadded decimal — the form the ledger's
  `sign_refs` store (e.g. `mahadevan:72`).
- The canonical anchors register keys its records by
  sign id: for the mahadevan frame, `M` followed by the
  number **zero-padded to three digits** (`M064`,
  `M099`, `M342`). Every one of the 287 keys matches
  `^[A-Z]\d{3}$` (verified at this registration), and the
  file is governed by the D-A declared schema
  (`specs/029-tao-claim-lifecycle/anchors-schema.json`).
- **Identity is by (frame, number).** `mahadevan:64`,
  `mahadevan:064`, and the register key `M064` denote
  the same sign. A frame-qualified ref resolves to the
  register key by this rule, or it does not resolve.
- **Frames in v1.** glossa-settle-1 settles the
  **mahadevan** frame only. A frame's **inventory** is
  the set of the register's keys under the frame's
  prefix: inventory(mahadevan) = 286 signs. The register
  holds one further key, `H003` (reading `an`, LOW, not
  strict), under a frame the anchors file does not name;
  it is out of scope in v1 — counted here, not dropped.
  Its frame's name is **UNMEASURED** (§10): not recorded
  in the register.
- **Named divergence, recorded not repaired.** This
  identity rule differs in mechanics from two earlier
  registered texts, and the difference is stated so no
  layer misreads another: matrix-defs v1 rule R4
  constructs the key literally as `M<n>` (unpadded), so
  `mahadevan:64` names no key under R4 and R4 yields
  zero cells — Stage 2's recorded state of the matrix
  layer, which stands until matrix-defs is amended
  through its own discipline. The Stage 3 gate's V4 R4
  tie converts a key to `mahadevan:064` (padding kept),
  which likewise does not equal the ledger's stored
  `mahadevan:64`. The settling layer resolves by number,
  on the ground above (the register's uniform key
  convention under its declared schema). Under
  glossa-settle-1, `mahadevan:64`, `mahadevan:70`, and
  `mahadevan:72` **do** resolve — to M064, M070, M072,
  all HIGH, with readings `va`, `vēl`, `mā`. Amending
  the matrix layer's mechanics is a matrix-defs
  amendment, outside this registration's scope; the
  divergence is flagged in the Stage 4 record for the
  owner's oracle read.

## 3. Candidates — assignment sets as data

- An **assignment** is one (frame, sign) → value pair,
  written `{sign: "mahadevan:70", value: "vēl"}`. A
  **candidate** (assignment set) is a stored record —
  data, not code:

  ```json
  {
    "id": "<candidate id>",
    "provenance": {"author": "…", "source": "…", "date": "…"},
    "frame": "mahadevan",
    "assignments": [{"sign": "mahadevan:70", "value": "vēl"}]
  }
  ```

- A candidate that assigns one sign twice is malformed;
  a run over it refuses. A candidate's assignments may
  name signs outside a run's scope and outside the
  register; §6 defines what a run does with each case.
- **Values compare as exact strings** (Unicode code
  points as stored; no case folding, no diacritic or
  length normalization): `vēl` ≠ `vel`. A reading is
  the string the register stores, or it is a different
  value.
- **Assignment sets of record** (definitions registered
  here; their materialization as stored records is
  T403's act, each with provenance):
  - **incumbent** — the strict set read as assignments:
    {(sign → its record's `reading`) : the sign's
    register record is strict}. Over the mahadevan
    frame at this registration: 94 assignments.
  - **full-register** — every register record of the
    frame read as assignments: {(sign → `reading`) :
    every record under the frame's prefix}. Over
    mahadevan: 286 assignments.
  - A literature challenger enters only as its own
    intake record with sources (spec.md Point 3);
    none is fabricated for v1.
- **Restriction.** A run evaluates a candidate
  **over a scope**: a named list of frame-qualified
  signs. The run's effective candidate is the
  candidate's assignments whose sign is in the scope;
  assignments outside the scope are enumerated in the
  run record as out-of-scope and enter no count.

## 4. Contexts — the extraction rule

Derived from Glossa's own anchor record as found in the
tree:

- For an assigned sign, its **anchor context** is the
  register record keyed by that sign, if one exists.
  The register is a mapping keyed by sign id, so at
  most one record per (frame, sign) can exist: a sign
  has **one context or none**. An assigned sign with no
  record is **uncontexted** and is enumerated as such.
  (If a future register state could carry two records
  for one sign, this rule cannot represent it — see the
  semantics' falsifier, §11(a).)
- A context carries exactly the fields the rules read:
  the record's `reading` (its recorded assignment), its
  `confidence` (§9), and its strictness under §1's
  recomputed rule.
- **Reconciliation with the pair-list shape.** No
  pair-set field exists in the canonical register: no
  field of any of the 287 records holds a list of
  cipher/target pairs (the records' field census is in
  the Stage 4 record). The pair-list shape —
  `{"cipher", "target", "confidence", "note"}` elements
  under a `pairs` field — exists in this codebase only
  in the live database's `anchor_sets` table
  (`backend/glossa_lab/database.py`, schema v8): the
  operator/user-built sets. Those sets are **not
  settling contexts in v1**: Spec 085 Q2, answered in
  Spec 086 §8, records that their payloads are generic
  cipher/target strings, not frame-qualified sign ids,
  and that the canonical anchors file is the operative
  context source; decision D-086-Q2 keeps assignment
  and constraint authorship outside the UI as stored
  records. If a future semantics version settles over
  such a set, a "pair" will be one element of its
  `pairs` list and a context the element a candidate's
  sign touches; glossa-settle-1 registers no rule over
  them.

## 5. The rules

### S-R1 — anchor-context check

For each assigned sign (in scope) with a context:

- context strict **and** assigned value ≠ the record's
  `reading` → **conflict**, enumerated as
  `{sign, anchor, assigned_value, anchor_reading}`;
- context strict **and** assigned value = `reading` →
  **consistent**;
- context not strict → a **non-strict context**:
  touched, enumerated with its record's reading and
  confidence, carrying no S-R1 verdict either way.

Every assigned sign is checked; there is no sampling.
An uncontexted assignment enters no S-R1 count and is
enumerated under §7's `uncontexted_assignments`.

### S-R2 — matrix-bearing check (v1 determinate form)

A ledger claim is **touched** by a run iff the claim's
`sign_refs` (identity by (frame, number), §2) intersect
the run's effective candidate's assigned signs. For each
touched claim, the run enumerates the claim, the
intersecting refs (`via_signs`, in the order the ledger
entry stores its `sign_refs`), and its **bearings**,
taken from registered machine-readable sources only:

- **(i) Study outcomes.** The claim's governing stored
  outcome blocks — the dated outcome blocks on its
  record of record, grouped by study, the latest dated
  governing, under the ordering matrix-defs v1 R3
  registers — mapped through the matrix-defs v1 outcome
  table (§6 of `glossa-indus/matrix/DEFINITIONS.md`):
  `NOT SUPPORTED` → opposing, `INCONSISTENT` → opposing,
  `NOT NUMERAL-LIKE` → opposing; **no recorded outcome
  maps to supports in the table**, and every other
  outcome — inconclusive, unexecuted, not-pinnable,
  identification-failed — bears neither way (the T2 rule
  of spec.md Point 4, applied at run time). Tallied once
  per (claim, study): `supporting`, `opposing`,
  `constraining` counts. No outcome in the table maps
  to `constraining`, so that tally is 0 under (i) in v1.
- **(ii) Falsifiers.** Counted as `falsifiers_present`
  (the number of falsifier strings on the ledger entry)
  and `falsifiers_evaluable`: **0 in v1**. Falsifiers in
  this record are prose corpus/statistical conditions;
  no registered rule evaluates one against an
  assignment. They are counted and named, never
  silently dropped (§10).

**Value-independence, stated plainly.** In v1 no stored
bearing is keyed to an assigned *value*, so a touched
claim's tallies depend on **which signs** are assigned,
never on the values assigned. A run record says so
wherever it reports tallies. This is the record's true
state, and it is the determinate form of spec.md's
S-R2 sketch that the current record supports; the
sketch's value-keyed reading-family test is registered
as a named gap (GAP-S2, §10), not implemented by judging
prose — parsing prose into relations is the practice
Spec 085 retired.

### S-R3 — internal consistency (registered; inert in v1)

- **Rule schema.** Where a **positional-class table**
  — a stored record, with provenance, mapping signs of
  a frame to class labels — is registered, two signs of
  one class assigned the same value violate the
  distinctness rule; violations are enumerated pairwise
  as `{sign_a, sign_b, class, value}`.
- **In v1 no class table is registered**, so the rule
  is inert: every run reports
  `s_r3: {class_table: null, violations: []}` — a
  determinate zero, not an omission. The class table is
  **UNMEASURED** (§10): the counter-decomposition
  search that established this is part of this
  registration. Registering a table is a semantics
  amendment with its own record; until then, no S-R3
  violation can exist and none can be reported.

### S-R4 — coverage (computed, never narrated)

A run record carries exactly these fields (the
canonicals' `expected` objects use exactly these names):

- `scope`: the scope's sign list, in scope order;
  `scope_signs`: its count.
- `assigned`: the effective candidate's assignments
  within scope, in scope order; `assigned_count`;
  `assigned_share` = `assigned_count / scope_signs`.
- `uncontexted_assignments`: assigned signs with no
  register record, enumerated `{sign, value}`.
- `contexts`: one entry per contexted assigned sign, in
  scope order: `{sign, anchor, assigned_value,
  anchor_reading, confidence, strict, result}` with
  `result` ∈ `consistent | conflict | non_strict`;
  `contexts_touched`, `strict_contexts`, `consistent`,
  `non_strict_contexts` counts.
- `conflicts`: the S-R1 conflict enumeration (§5).
- `strict_agreement_share` = `consistent /
  strict_contexts`; when `strict_contexts` = 0 the
  share is **null** (glossed "no strict contexts
  touched") — never 0 or 1 by convention.
- `contexted_share` = `contexts_touched /
  assigned_count`; when `assigned_count` = 0 the share
  is **null** (glossed "no assignments in scope").
- `claims_touched`: per §5 S-R2, in ledger order;
  `claims_touched_count`.
- `s_r3`: as registered above.
- `forced`: per §6, in scope order.
- Header: `semantics: "glossa-settle-1"`, the input
  pins of §1, the candidate id, the scope.

## 6. Forced consequences (narrow, finite)

Within a run (candidate C over scope S): for each sign
s ∈ S not assigned by C, if **every** assignment of
values to S's unassigned signs that is consistent with
S-R1 (and S-R3, inert in v1) gives s the same value,
(s, that value) is **forced**, and the run enumerates
it.

Under S-R1 the computation collapses, and the collapse
is stated rather than dressed up: a strict-anchored
sign admits exactly one consistent value — its record's
`reading`; every other sign admits at least two (its
record's reading, if any, and any other string, the
value space being open). So in v1:

> forced = {(s, reading(s)) : s ∈ S ∖ assigned(C),
> s strict}.

Corollary over the full frame: the unscoped forced set
of the mahadevan frame is the strict register itself —
94 (sign, reading) pairs. In v1 the forced computation
is therefore the strict register restated for the
scope's unassigned signs; it becomes informative only
when a registered rule couples signs (S-R3 with a class
table, or a successor rule). Reported as computed,
labeled as such, never narrated as a discovery.

Score ceilings under dependency remain AEE's propagated
scores (spec.md Point 3, subsumption): the settling
layer reports them where a surface displays them; it
does not recompute a rival number.

## 7. Scenarios and dual runs

- A **scenario** is a stored record `{id, candidate,
  scope}` — a **run input**, never a verdict input. A
  scenario asserts nothing; it names the candidate and
  the context scope a run evaluates. The registered
  canonical scenarios live in `settling-canonical.json`
  beside this document, each with its prose derivation
  and its expected run record.
- A **dual run** (interchangeability) executes the same
  engine, under the same semantics version, over two
  candidates, with **identical input pins**: the same
  ledger build hash and the same corpus snapshot hash
  (the snapshot the matrix pins:
  `glossa-corpus/indus/exports/indus_research.jsonl`,
  canonical hash recorded in the comparison — settling
  does not read the corpus in v1; the pin is carried so
  the comparison's inputs are fully named, per
  C086-15). Both run records are stored.
- The comparison output is a **per-claim divergence
  list**: every claim touched by either run whose
  S-R2 tallies differ between the runs, with both
  tallies shown; plus the coverage deltas (assigned,
  contexts, strict contexts, consistent, conflicts,
  forced counts), the signs assigned by one candidate
  only, and — for each touched claim — any
  **pre-registered expectation** the program's record
  carries for it (a frozen study's outcome record),
  named with agreement or divergence scored against it.
  Where no expectation exists for a touched claim, the
  comparison says so: a named absence, not an omission.
  Two readings are never blended into one verdict.

## 8. Confidence carriage

Every context line of a run record carries its anchor
record's `confidence` **verbatim** — the register's own
vocabulary (HIGH, MEDIUM, LOW, CANDIDATE) — and no
settling computation converts a confidence to a number,
a weight, or a threshold (harmonization adoption 3,
item 6: narrative confidence is not a number). Strictness
is computed from the §1 rule, in which confidence is one
input among three; it is never a confidence score. (The
`confidence: "low"` values the adoption record names
live on the database anchor sets' pairs — out of v1
scope under §4; if such a set is ever intaken, its
confidences enter only as verbatim text, the Stage 1
`confidence_text` discipline.)

## 9. What a run may never do

A run creates only a run record. It writes nothing to
the ledger, the matrix, or any store of record; it
imports no intake or write module (gate V9). Its record
carries the label of the head of this document and the
§5 header pins, so a reported settling number with no
run record behind it is not a result (C086-14).

## 10. UNMEASURED register and named gaps

Quantities this registration could not compute from the
record, named after the counter-decomposition search
(harmonization adoption 3, item 4: before a quantity is
recorded as not checkable, its source artifact is
searched for a counter decomposition):

1. **The S-R3 positional-class table — UNMEASURED.**
   Searched: the canonical anchors file (no
   positional-class field on any record; positional
   content exists only inside prose `basis` strings —
   parsing prose is the retired practice); the
   `canonical_signs` table schema
   (`backend/glossa_lab/database.py`) — continuous
   `start_rate` / `end_rate` / `internal_rate`, not
   classes, and a live-database artifact, not a repo
   record; `data/crosswalks/canonical_sign_registry_v2.csv`
   — Parpola-frame ids with the same continuous rates;
   `data/soviet_positional/` — Kondratov sign classes of
   a different numbering tradition, whose dataset
   header registers it `descriptive_only` with an
   explicit non-claims line; `glossa-indus/analysis/
   positional/hunt_tripartite_test.json` — a test
   output, not a class table. No registered class table
   over the mahadevan frame exists in the record.
2. **GAP-S2 — value-keyed claim bearing.** Spec.md's
   S-R2 sketch ("a claim whose recorded outcome or
   falsifier bears against the assigned value's reading
   family"; "a claim whose falsifier would be triggered
   by the assignment") is not mechanically determinate
   over the current record. Searched: the record of the
   ledger's only sign_refs-bearing claim
   (`parpola_2010_dravidian_solution_manual_002`,
   `glossa-indus/claims/extracted_claims/parpola_2010_dravidian_solution.json`)
   — its `proposed_value` is a single prose string for a
   sign *family* ("meen/min (fish; also star,
   lightning in Proto-Dravidian)"), not per-sign values;
   its falsifier is a prose corpus-statistical
   condition ("If fish signs do not show terminal-sign
   followers consistent with case suffixes"); its one
   outcome-shaped append names Spec 072, carries no
   outcome string, and stands with its result content
   removed under the Roif gate (Spec 086 §9: Spec 072
   enters records name-only — it is not read here).
   No per-sign proposed value in identifier-bearing
   form exists anywhere in the ledger (the whole
   ledger carries exactly three `sign_refs`, all on
   this claim). What closes the gap: per-sign proposed
   values intaken in identifier-bearing fields, after
   which a successor semantics version can register a
   value-keyed tie rule beside V4's T-rules. Until
   then, S-R2 v1's form (§5) is the whole rule.
3. **The H-prefix frame name — UNMEASURED.** The
   anchors file does not name the frame of its one
   `H`-prefixed key (§2). Nothing in v1 depends on it.

## 11. The falsifier of these semantics

glossa-settle-1 is the wrong semantics for Glossa's
record if any of the following is observed:

- **(a)** a register state in which one (frame, sign)
  carries two anchor records with different readings —
  §4's one-context-per-sign extraction cannot represent
  it, and a run over such a state must refuse rather
  than choose;
- **(b)** a stored outcome block whose bearing under
  the outcome table depends on which *value* a
  candidate assigns — §5's value-independence, and
  with it GAP-S2's closure state, would be falsified;
- **(c)** an anchor-record class the extraction rule
  cannot represent — e.g. a record carrying pair-sets
  spanning several inscriptions (none exists in the
  register today);
- **(d)** a claim intaken with per-sign proposed values
  in identifier-bearing form whose falsifier a
  registered rule evaluates differently than the same
  evaluation derived by hand — the GAP-S2 closure test.

## 12. Amendment discipline

A change to any rule in this document is a new
semantics version (`glossa-settle-2`, …), registered in
the open with its reason; canonicals are re-derived by
hand under the new version before the engine moves;
run records stamped with an older version stand as
computations under that version. Nothing in this
document is edited silently.

**Registered:** 2026-11-01, Spec 086 Stage 4 (T401),
before any settling code exists in the tree.
Version: `glossa-settle-1`.
