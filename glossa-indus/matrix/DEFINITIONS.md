# Matrix definitions — `matrix-defs v1`

Spec 086 (winning-combination adoption), Point 2, task T201.
This document is the contract the matrix generator runs under:
the column classes, the derivation rules, and the evidence
registers are registered here, versioned, and are the only
ones the generator may use. A machine copy of every table in
this document lives in the generator
(`backend/glossa_lab/matrix_generate.py`); the Stage 3 gate
will carry its own registered copies, and a deliberate change
to any definition is made in both copies in the same motion.
Acceptance for this document is human-as-oracle: a reviewer
reads the definitions as the contract they are. *This does
not establish the definitions are the right semantics — it
establishes they are written down, versioned, and the only
ones the generator may use.*

**The honesty split, stated once.** "The matrix is
generated, never made" holds for the data. The definitions
in this document are human-registered — the same split the
reference implementation (the Breaking-Point Atlas) carries
in its own generator, named there and adopted here rather
than papered over. Every cell in the matrix arises from
exactly one rule below, applied to stored records; where the
record carries nothing, the matrix shows nothing and the
coverage block counts the gap. No relation is invented, and
no free text is matched into a relation — the
`CrossHypothesisMatrix` practice of regex-matching sign
names out of claim text is retired as a relation source
(Spec 085 FR-085-03).

## 1. Inputs — the evidence registers

The generator reads **only** the following, and nothing
else:

| Register | Identity | How it is reached |
|---|---|---|
| The ledger | `glossa-indus/ledger/claims.jsonl` (`ledger-schema v1`) | Directly. The sole entry point: every row, and every pointer the generator follows, comes from a ledger entry. |
| Source records of record | The files named in ledger entries' `sources[]` (the extracted-claims store files; the spec bundles `specs/*/claims.json` and `specs/*/aee-claims.json`) | Only through an entry's own `sources[]` pointers, and only after the file's canonical hash (the shared helper `glossa_lab.ledger_intake.sha256_file`: UTF-8, CRLF→LF) verifies equal to the `sha256` the entry records. A mismatch refuses generation, loudly, naming the file — the record the ledger mirrors is not the record on disk, and that is a defect to repair at the source, never to generate around. |
| Canonical anchors | `backend/reports/INDUS_FINAL_ANCHORS.json` | Named here. The anchor register: 287 records keyed by sign id (`M<n>`, Mahadevan frame; one `H<n>` key), each carrying a recorded `reading` (assignment). |
| Research-check sidecars | The files named in annotation entries' `sidecar` pointers (`glossa-indus/claims/research_checks/*.research_check.json`) | Only through annotation entries; hash-verified the same way. The Spec 025 contract stands: sidecars are advisory and never modify a claim. |
| Corpus snapshot | `glossa-corpus/indus/exports/indus_research.jsonl` (corpus V1, per `glossa-indus/CORPUS_VERSIONS.md`), read through its registered loader `glossa_lab.data.indus_corpus_v2.load_corpus()` | Named here; feeds the sign×sign block only (§9). Its canonical hash is stamped into the block's provenance. If the loader's active tier is not the real corpus (the loader has fallbacks), generation refuses — a block computed over a fallback or synthetic corpus is not the pipeline output for this snapshot. |

Why source records are read at all: the ledger mirrors each
claim's identifiers and provenance, but the *direction* of a
bundle evidence item and the *outcome* of a study are stored
in the claim's record of record, not in the ledger entry's
own fields. The ledger remains the sole entry point in the
sense that matters (C086-1): no cell exists that does not
trace to a ledger entry, and no content enters from a file
that no ledger entry names and hash-pins. The alternative —
a matrix built only from the ledger's flattened identifier
lists — could not distinguish a supporting document from a
dependency, and would have had to guess. This design refuses
to guess and says where each fact came from.

## 2. Rows

One row per ledger **claim** entry (840 in the Stage 1
build), in ledger order, identified by the entry's canonical
id. Annotation and reclassification entries are not rows.
A row displays the entry's `status` and `stage` **as the
ledger holds them** — the matrix displays the ledger's
values or nothing (spec.md Point 6); it holds no status of
its own.

## 3. Column classes

The evidence universe, in five registered classes. A column
exists only because a register names it.

| Class | Column id | Universe (what makes a column exist) |
|---|---|---|
| `studies` | The spec number exactly as recorded in a stored outcome record (e.g. `054`) | Every spec that has at least one stored outcome record (§6) on some claim's record of record. |
| `documents` | A literature document id (e.g. `fuls2023_catalog_of_indussigns_searchins_1dbdecdb`) or a bundle evidence item's `ref` exactly as stored (e.g. `specs/026-rcph-framework-transfer/spec.md#8`) | Every document named by a stored evidence instance, and every `ref` carried by a stored evidence item of some claim's record of record. |
| `research_checks` | The sidecar file path, as named in the annotation entry | Every sidecar named by a ledger annotation entry. |
| `anchors` | The anchor register's key exactly as stored (e.g. `M342`) | Every record in the canonical anchors register. |
| `corpus_texts` | An inscription id from the corpus snapshot | **No columns in v1.** No stored relation in the ledger or its registers names a corpus text as bearing on a claim, so no rule below produces a corpus-text cell. The class is registered so the emptiness is stated, not omitted; a future rule has a registered home here. |

## 4. Relations

A cell carries exactly one of three relations:

- **supports** — the column's stored record affirms the
  row claim: a stored evidence item whose direction is
  `supports`, an evidence instance standing behind the
  claim, or a study outcome in the bearing table (§6)
  mapped to `supports`.
- **opposes** — the column's stored record tells against
  the row claim: a stored evidence item whose direction is
  `opposes`, or a study outcome in the bearing table mapped
  to `opposes`.
- **constrains** — the column bounds the row claim's
  reading space without affirming or denying it: an anchor
  record whose assigned reading fixes a sign the claim
  names, or a registered settling instrument whose subject
  set includes the claim.

An empty cell is the absence of a derivable relation,
shown as absence — never filled by judgment.

## 5. Derivation rules

Each rule names its stored inputs, its mechanics, and its
citation form. Every cell records: the relation, the rule
id, this definitions version, and its citations — the
ledger entry id first, then the pointer to the exact stored
item the relation was read from, so an inspector can
exhibit the stored relation from the cited records
(C086-8).

### R1 — Evidence instance (documents, supports)

*Stored input:* an extracted claim's record of record
carries `evidence_instances`: other extracted claims
standing as evidence for it, each naming its own
`source_document_id`.
*Mechanics:* for each instance, one cell
(claim × the instance's document) with relation
`supports`. Citations: the ledger entry id; the instance's
claim id.
*Note:* the claim's **own** document is provenance
(extraction origin), not evidence, and produces no cell
under any rule.

### R2 — Bundle evidence direction (documents, per stored direction)

*Stored input:* a bundle claim's record of record carries
`evidence`: items with `ref` and `direction`.
*Mechanics:* for each item, one cell (claim × the item's
`ref`) whose relation is the item's stored `direction`
mapped through the direction table: `supports` →
`supports`, `opposes` → `opposes`, `constrains` →
`constrains`. Multiple items naming the same `ref` merge
into one cell, citations accumulating. If two items for
the same (claim, `ref`) carry **conflicting** directions,
generation refuses, naming the claim and the ref — a
contradiction in the record is repaired at the source,
never averaged by the generator. Citations: the ledger
entry id; the item's `ref`.
*Population note:* in the Stage 1 build every stored
direction is `supports` (2,736 items). The other two
directions are registered because the rule reads the stored
field, not today's census.

### R3 — Study outcome (studies, per the outcome table)

*Stored input:* a claim's records of record carry stored
outcome blocks: dated dictionary fields naming a `spec`
and an `outcome` (execution-outcome appends, first-check
and closure records — e.g. `spec074_outcome_append_2026_10_24`,
`first_check`).
*Mechanics:* outcome blocks are grouped by (claim, spec).
The **latest dated** block governs the study's current
bearing on the claim (a study's later act supersedes its
earlier outcome — a re-execution replaces the outcome it
re-ran); a block without a date sorts before dated blocks,
and ties break by field name, so the order is total and
mechanical. If the governing block's outcome is in the
bearing table (§6), one cell (claim × spec) arises with
the table's relation, citing **all** of the study's blocks
for that claim. If it is not in the table, no cell arises,
and every block is listed in the coverage block with its
reason (non-bearing outcome, or superseded by a later
block). Citations: the ledger entry id; one pointer per
block (`<source path>:<claim id>#<field name>`).
*What this rule refuses:* an outcome that a study did not
reach a verdict with — inconclusive, unexecuted,
not-pinnable, identification-failed — is not a bearing on
the claim's truth, in either direction. Citing Spec 054's
2026-10-24 `STRICT CORPUS NOT PINNABLE` closure as support
for the Yadav claim is the named Atlas failure mode; under
this rule that block produces no cell at all, and the
study's cell for that claim comes from its governing
2026-10-25 block (`NOT SUPPORTED` → `opposes`).

### R4 — Anchor assignment (anchors, constrains)

*Stored input:* a claim entry's `sign_refs` (frame-qualified
sign identifiers from identifier-bearing fields only — the
ledger's own discipline) and the anchors register.
*Mechanics:* for each sign ref `mahadevan:<n>`, the anchor
keyed `M<n>`, if the register holds it **and** the anchor
carries a recorded `reading`, yields one cell
(claim × anchor) with relation `constrains`: the recorded
assignment bounds the claim's reading space. Sign refs
whose frame is not `mahadevan`, or that name no anchor
record, produce no cell and are listed in the coverage
block. Citations: the ledger entry id; the anchor id.
*Population note:* in the Stage 1 build exactly one claim
carries `sign_refs` (`parpola_2010_dravidian_solution_manual_002`,
naming mahadevan:72, 64, 70), and the register holds no
anchor under any of those keys — so R4 yields **zero**
cells today and all 287 anchor columns stand unused. That
is the record's true state, shown, not a defect of the
rule.

### R5 — Research-check verdict (research checks; no cells in v1)

*Stored input:* annotation entries and their sidecars,
which carry a `verdict` field under the Spec 025 protocol.
*Mechanics:* a cell would arise only if a sidecar's
`verdict` were a string present in a registered verdict
table mapping it to a relation. **The v1 verdict table is
empty**: no verdict vocabulary has been registered, because
the sidecar population states no verdicts — all 31
bearings in the Stage 1 build carry `verdict: null`, and a
research check is advisory by contract (it never modifies a
claim). Registering a mapping for a vocabulary that does
not exist in the record would invent relations. The 31
research-check columns therefore stand unused in v1, and
the coverage block says so. A future definitions version
may register a verdict vocabulary when the sidecars carry
one.

### R6 — Settling instrument (constrains; register empty in v1)

*Stored input:* a registered settling instrument
(Stage 4's `glossa-settle-1` records) whose subject set
includes the claim.
*Mechanics:* one cell (claim × instrument) with relation
`constrains`. **The instrument register is empty in v1** —
no settling semantics exist until Stage 4 — so R6 yields
no cells and no columns. It is registered now so the
rule's home exists before the engine does
(derive-before-build, C086-13).

## 6. The outcome table (for R3)

A study outcome bears on a claim only if its recorded
outcome string is an exact entry in this table. Every
other outcome string — listed or not — is non-bearing.
The table is deliberately small: it registers the verdict
strings the record actually carries, and a new string
enters the table only by a definitions amendment, never by
the generator's inference.

| Recorded outcome | Relation | Ground |
|---|---|---|
| `NOT SUPPORTED` | `opposes` | The study's frozen test ran and its outcome is that the claim is not supported (Specs 054, 074). |
| `INCONSISTENT` | `opposes` | The study's recorded verdict on the claim's thesis (Spec 052's battery, appended to the claims it tested). |
| `NOT NUMERAL-LIKE` | `opposes` | The study's numeral-behaviour test outcome on the claim's proposed value (Spec 055's first check). |

Outcomes observed in the record that are **non-bearing**,
named so the disposition is auditable (not an exhaustive
list — unlisted strings are non-bearing by the rule
above): `INCONCLUSIVE …` (a test that ran and could not
decide), `IDENTIFICATION FAILED …` and `RECOVERED`
(whether the claim can be administered or carried in the
program's form — a standing act, not a verdict on the
proposition), `STRICT CORPUS NOT PINNABLE` (the test did
not execute). No outcome in the record maps to `supports`
in v1: the studies columns' only cells are the three
`opposes` rows above. Support enters this matrix through
documents (R1, R2), not through study verdicts — that is
what the stored record carries.

## 7. Coverage — part of the artifact

Every generation emits the coverage block, in the artifact
(`matrix.json`), in the generator's printed output, and
rendered in `matrix.md`:

- rows with no non-empty cell (count, and their ids);
- columns never borne on, per class (count, and their ids);
- falsifier coverage of the ledger (claims carrying a
  falsifier, of all claim entries, and per population —
  recomputed from the ledger at generation time);
- unresolved sign mentions: the free-text `signs_involved`
  mentions on extracted claims' records, which no
  identifier resolves — the curation work list, carried
  from Spec 085 — listed with the record that carries them;
- sign refs that resolve to a frame but to no anchor
  record (the R4 residue);
- study outcome blocks that produced no cell, each with
  its reason (non-bearing outcome, or superseded by a later
  block from the same study);
- claim-to-claim dependency pairs carried in ledger
  `evidence_refs` that resolve to other ledger entries:
  counted and listed by pair. Under matrix-defs v1 these
  are **not** matrix cells (the matrix is claims×evidence;
  a dependency's target is a claim, not an evidence item) —
  they are recorded here so the relation is visible in the
  artifact, not silently dropped.

## 8. The sign×sign block

`matrix.json` carries one further block, imported — not
recomputed by new code — from the existing co-occurrence
pipeline (`glossa_lab.pipelines.cooccurrence.build_cooccurrence_network`,
the pipeline `analyze_script.py` §6 runs), executed over
the corpus snapshot register (§1) with that call site's
parameters: `window=2, min_freq=3, min_edge_weight=2`
(remaining parameters at the pipeline's defaults, including
its top-80 node selection and top-200 edge emission — the
block is the pipeline's output as emitted, truncation
included, and its provenance block says so).

Sign ids in the block are the corpus loader's integer sign
ids, rendered `sign-int:<n>`. They are **not** relabeled
with a frame name: the loader documents that it converts
source ids to Mahadevan integers where its crosswalk maps
and otherwise preserves source-frame integers, so a single
frame label would assert a mapping the loader does not
guarantee. The block's provenance records the corpus path,
its canonical hash, the loader tier, the pipeline module,
and the parameters — the snapshot is pinned by hash, which
is what "the same corpus snapshot" means mechanically.

## 9. As-of stamp

Every generated artifact carries: the ledger's canonical
content hash, the ledger line count, the ledger's own
latest entry date, and the definition versions in force
(`ledger-schema v1`, `matrix-defs v1`). There is no
wall-clock generation time: the acceptance test for this
stage is delete-and-regenerate **byte-identity** (C086-7),
which a clock stamp would make impossible, and the stamp's
purpose under D-D is to name the data the artifact was
computed from — the ledger hash is that name. An artifact
whose stamp hash does not match the current ledger is
stale, and Stage 3's gate is where that is enforced.

## 10. Registered non-relations

Named here so the absences are decisions, not oversights:

- **`depends_on`** (bundle records): a claim-to-claim
  relation; not a matrix cell in v1 (see §7, last item).
- **A claim's own source document**: provenance, not
  evidence (R1 note).
- **Disposition and lifecycle blocks** on extracted records
  (dated blocks naming a `spec` but carrying no `outcome` —
  e.g. Spec 057's and 065's dispositions): lifecycle acts,
  already mirrored in the ledger's `status`/`stage`; not
  test outcomes, and R3 does not read them.
- **`glossa_lab_evidence`** (extracted records): free-text
  program-evidence notes with bracketed verdict words
  embedded in prose. Turning them into relations would
  require parsing prose — the retired practice. Not read.
- **`contradicting_evidence`** (extracted records):
  free-text strings naming literature and phases in prose,
  not identifiers (the ledger's SCHEMA.md records the same
  disposition). Not read; the claims carrying it are the
  curation backlog for a future identifier-bearing intake.
- **Explanation content** (`explanation_record`, lane-2
  texts): authorship-bearing prose under OD-2; carries no
  matrix relation.

## 11. Measurements (adoption 3, item 1 — disposition)

Measured evidence does arise in this stage's registers —
the sign×sign block's edge weights and node frequencies
are measurements (values with units and condition
classes), and they are carried **in the matrix artifact**
with full provenance (§8). The ledger's `measurement`
entry kind is implemented additively in Stage 2 (schema
branch + validator support; see the dated amendment in
`glossa-indus/ledger/SCHEMA.md`), so a measurement can
enter the ledger through intake with its value, unit,
direction, condition class, and artifact hash. **No
measurement entries are minted into the ledger by this
stage**: the generator never writes the ledger (truth
flows one way, spec.md Point 6), minting is an intake act,
and no pre-existing measured source artifact is in this
stage's migration scope. The block's statistics stand in
the artifact, pinned to the corpus hash, until an intake
act — a future migration with its own reconciliation —
mints entries from a named source.

## 12. Amendment discipline

A change to any table in this document is a new
definitions version (`matrix-defs v2`, …), made in this
document and in the generator's machine copy in the same
motion, and recorded in the spec's stage record. Artifacts
generated under an older version are stale by their stamp
(§9) until regenerated. The Stage 3 gate's registered
copies join this discipline when they land.
