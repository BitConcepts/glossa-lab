# Spec 086 — Winning-Combination Adoption: Ledger, Generated Matrix, Executable Settling, Layered Map

**Status:** APPROVED AS A BLOCK by the owner on 2026-11-01
(06:40 EST, option tap + message in the Glossa-Lab chat:
"Approve the Spec 086 package as a block"). The §8 decision
items stand as the package recommends (draft defaults adopted
as written). This document is the approved package text,
adopted into the repo under Stage 0 (tasks.md T001); the
approval act is also recorded in plan.md and LEDGER.md.

**Recorded addition (2026-11-01, record-only, no design
change):** Amendment 1 to the canonical winning-combination
pattern was ratified by the owner on 2026-11-01 (relayed from
the RCPH chat): the named failure mode "a citation can exist,
be relevant, and still not carry the relation," with five
binding corollaries (builder comments are not verification; an
artifact's citation list is itself a claim under ledger
discipline; the gate must include a citation-to-relation tie
check class; a gate is never loosened for a failing citation —
the repair goes in the downstream layer; a red gate leaves the
previously published artifact byte-untouched). This package
already carries that substance as approved — C086-9
(relation-carrying citations), the Stage 3 V4 check class,
C086-11 (gated publication), all adopted from the Atlas
pattern note before the amendment was ratified. Adoption is
confirmatory: no plan change, no claim text altered, and no
conflict with any ratified local decision.

**Recorded adoption 2 (2026-11-01, harmonization).** The
pattern note "Canonicalize before you hash" (from the
Spec-Kit AEE chat, delivered 2026-11-01) is ADOPTED with the
following scoping, recorded so no later stage misreads it:
(1) Checkout pinning is already in force in this repo
(`.gitattributes`: `* text=auto eol=lf` plus per-extension LF
rules; CRLF reserved for `.bat`/`.cmd`/`.ps1`) — conformance
recorded, no action. (2) Canonical-form hashing is adopted
for this spec's generated layers: every hash the ledger
tooling records over a source file is computed by one shared
canonical-hash helper (CRLF→LF normalized, UTF-8) in
`backend/glossa_lab/ledger_intake.py`, and generated
artifacts are written with pinned LF newlines. (3) The
existing freeze regime's raw-byte pins (framework026
`verify_freeze`) are NOT migrated and are not to be touched:
they are historical records that verify today on both
platforms under the attributes regime. (4) The note's
corollary — a read-only gate must be write-free, caches
included — is recorded as a Stage 3 design requirement (see
stage-1-record.md): the Stage 3 gate runs with interpreter
bytecode writing disabled and proves write-freedom by
hashing the published tree before/after a red run (tying to
Amendment 1's corollary 5). Implementation belongs to
Stage 3; no claim text or stage design is altered by this
adoption.

**Recorded adoption 3 (2026-11-01, harmonization).** Six
findings from the MPCodec chat's completed adoption (their
spec 031, landed; pattern note 2026-11-01 in the
AXIOVEX/mpcodec repo) are adopted with these dispositions:

1. **Measurements as first-class entries — ADOPTED FOR
   STAGE 2.** Assessed against ledger-schema v1: the schema
   discriminates entries by `kind` with per-kind shapes, so a
   `measurement` kind (value, unit, direction, condition
   class, artifact sha256) can be added as a new kind branch
   WITHOUT altering the pinned claim-entry shape. Stage 2's
   matrix generator will mint measurement entries from source
   artifacts; Stage 1's migration does not extract them and
   this stage does not change the pinned schema.
2. **V4 gains a numeric arm — binding design input for
   Stage 3.** Where a cited evidence entry carries a
   measurement and the claim carries a machine-readable
   bound, the gate refuses a `supports` citation whose value
   violates the bound (and vice versa).
3. **Layers named in advance — binding design input for
   Stage 4.** The semantics registration must name the layers
   distinction: computed settling outputs and ledger
   verdicts/digestions are different layers; neither
   overrides the other in the record (MPCodec's flagship
   claim stands computed CONTESTED alongside an owner
   disposition of supported, without contradiction).
4. **Counter-decomposition before "not checkable" — binding
   design input for Stage 4.** Before any quantity is
   recorded as not checkable, its source artifact is searched
   for a counter decomposition; honestly UNMEASURED
   quantities are shown as such at the settle layer and on
   the map.
5. **A gate must never mutate the tree it checks — BINDING
   DESIGN RULE for Stages 2–3**, recorded alongside the
   canonical-hash and gate-write-freedom requirements:
   generators expose a PURE builder (output computed in
   memory) plus a thin write wrapper used only by the
   generate command; gates and regen checks call only the
   pure builder and compare against committed bytes.
   (MPCodec's first map check called the generator's write
   path and rewrote the artifact under test.)
6. **Narrative confidence is not a number — BINDING NOW,
   applied in this stage.** Free-text/qualitative confidence
   in source records migrates VERBATIM into a dedicated
   `confidence_text` field and is never normalized into a
   numeric value. Audit of this stage's migration (full
   census, recorded in stage-1-record.md and in the
   reconciliation reports): the only confidence in the
   migrated populations is P1's `confidence_in_source`, a
   NUMBER on all 31 records, carried verbatim into the
   entries' `confidence_in_source` (merged instances' values
   agree with their canonicals', 0 differences); the P2
   bundles carry no confidence field at any depth in 1,624
   records; no qualitative confidence exists in any migrated
   population, so `confidence_text` is null on every migrated
   entry. The intake builder routes any future qualitative
   value to `confidence_text` verbatim (teeth-tested). The
   qualitative confidences the finding names (anchor pairs'
   `confidence: "low"`) live outside this repo tree and are
   not a Stage 1 population; recorded Stage 4 intake
   constraint: they may enter only through `confidence_text`.

No conflict with any ratified local decision was found in
these six; AEE's numeric confidence (where a source carries
one) is untouched — it stays numeric, in its own field.

**Requirements source:** the owner's adoption order of 2026-11-01,
relayed from the RCPH chat: "adapt Glossa-Lab to the winning
combination," with the build order fixed (ledger intake validator →
matrix generator → verification gate → executable settling → map last)
and stage reports carrying the gate's output, not a summary of it. The
canonical pattern statement is
`~/workspace/projected-constraints-program/analyses/proposal-engine/winning-combination-pattern-2026-11-01.md`
(the framework's home; quoted below). The gap analysis is the Spec 085
audit of 2026-11-01 (`hidden_files/graph-matrix-audit-2026-11-01.md`),
cited throughout as "the audit."

**Conventions of this document.** For each of the pattern's seven
points: (a) the requirement, in the pattern note's or the ratified
decision's own wording where it is definitional; (b) Glossa's current
state, from the audit plus verification against the repo on 2026-11-01;
(c) the adoption design, naming exact artifacts. Where the owner's
relayed gloss of a ratified decision differs from the decision's
literal subject, the decision's text governs and the difference is
named (see §8 and README.md).

---

## 0. The pattern, as stated by its home

The canonical note states the pattern in six points (governance 1–4
from the Breaking-Point Atlas, execution and proof 5–6 from the RCPH
graph node matrix). The owner's adoption order states seven, splitting
the governance point and adding the harmonization rule as point 7.
This spec follows the order's seven-point structure; the note's text
is the substance.

> **From the Breaking-Point Atlas — governance.**
> 1. An **epistemic ledger** accompanies the work, always: every
>    material claim with its statement, source, date, status,
>    confidence, falsifier, and a "this does not establish" line.
>    Corrections are append-only reclassifications; superseded claims
>    are marked, never edited away. The ledger is the sole entry
>    point — nothing enters any other layer except through it.
> 2. The **matrix is generated from the ledger** by script. If it is
>    not in the ledger, it is not in the matrix.
> 3. A **layered map is the primary surface** (system → component →
>    evidence), rendering exactly the generated data, with the
>    headline state carried in its header and every element traceable
>    to ledger ids.
> 4. **Truth flows one way**: ledger → matrix → map. Downstream layers
>    are never hand-edited; a disagreement is a defect in the
>    downstream layer.
>
> **From the RCPH graph node matrix — execution and proof.**
> 5. The **matrix runs**: the representation is executable in the
>    project's engine (settle, propagate, project), so a system's
>    implications are computed, not narrated.
> 6. **Every arrow is machine-checked**: a verification test
>    recomputes each downstream layer from its source and *gates the
>    build* — on failure, nothing ships. Codec and regeneration checks
>    are lossless; drift is a defect. Where two readings of one system
>    exist, their agreement is proven against pre-registered
>    expectations, not asserted.

> **Harmonization (Tristen's standing rule, 2026-11-01).** "The
> concept and discipline are always accompanied by the epistemic
> ledger, in every project using the framework, and all framework
> projects are kept harmonized. When any framework chat finds an
> improvement to this pattern — a stronger gate, a better intake rule,
> a named failure mode, a refinement worth adopting — it writes the
> improvement as a short pattern note and **delivers it to every other
> framework chat** for adoption. A receiving chat adopts it unless it
> conflicts with a ratified local decision, in which case it surfaces
> the conflict to Tristen rather than diverging silently."

Reference shapes (Atlas, verified 2026-11-01): the ledger is
`ledger/claims.jsonl`, one JSON object per line with fields `id`,
`statement`, `source`, `source_date`, `status`, `confidence`,
`falsifier`, `does_not_establish`, `part`, `load_tags`; the matrix is
produced by `matrix/generate_matrix.py` and never hand-edited; the
gate is `verify_equivalence.py` (checks M1/M2/M3 over the matrix,
G1–G5 over the map, and a `--regen` mode requiring byte-identical
regeneration), and the map builder gates publication on it ("a red
gate means the candidate never replaces map/graph.json").

**The ratified decisions the order cites (D-A, D-B, D-D, D-E)** are
Glossa's own: Spec 029, ratified as a block by the owner on 2026-10-12
(owner's words: "do all this"), recorded in
`specs/029-tao-claim-lifecycle/adjudication.md`, addendum "D-A through
D-E ratified as a block (2026-10-12)". Their verbatim substance is
quoted at the points where this spec uses them. One caution the owner
should see plainly: the relay's shorthand ("D-A pinned-schema
validator") names the *pattern* each decision established, not always
its literal subject — D-A's subject is the anchor file. This spec
adopts the decisions as written and labels every generalization as an
extension, offered back to the framework under Point 7.

---

## 1. Point 1 — One ledger, sole entry point

### (a) Requirement

Every decipherment claim lives in a single claims ledger carrying: the
statement (atomic, one proposition per claim), its evidence and
sources, its status, its AEE state where scored, a falsifier, and a
"this does not establish" line. Corrections are append-only
reclassifications; a superseded claim is marked, never edited away.
Nothing enters any downstream layer except through the ledger. The
proposition-fingerprint dedupe (D-B) is enforced at intake by the
validator, not by memory.

D-B, verbatim (Spec 029 adjudication addendum, 2026-10-12):

> **D-B — Duplicate extracted claims: deduplicate by proposition —
> merge, never delete; guard the intake.** One canonical claim per
> proposition; every source document that stated it is preserved as
> an evidence instance of that claim, with evidence counted **once
> per origin group** (Spec 026's evidence-counting rule applied to
> the store). Stage and score attach to the proposition, not to an
> instance. A proposition fingerprint (normalised-text hash) is
> checked at extraction intake, so a future wholesale re-extraction
> collides loudly instead of silently regenerating a doubled set.

The fingerprint's frozen definition (implemented in
`backend/glossa_lab/proposition_fingerprint.py`, Spec 029 Phase I):
SHA-256 over the normalized claim text — Unicode NFKC, case-folded,
every non-letter/digit character replaced by a single space, rejoined
— rules version `spec029-phase-i-v1`. The module header records the
standing rule: "changing them changes every fingerprint; any change
is a new phase, not an audit edit." This spec does not change them.

D-A's schema discipline, verbatim (same addendum) — the anchors file
gains "a declared schema … enforced by a CI validator — the file has
accreted 56 distinct field shapes, and without a schema gate the
annotation decays back into drift." The owner's relay generalizes
this as "the pinned-schema validator pattern (D-A)"; Point 1's design
extends that pattern to the ledger schema and says so.

### (b) Current state (audit + verification)

There is no single ledger. Decipherment claims live in three
populations, in two formats, under three governance regimes
(verified 2026-11-01 against the repo):

- **P1 — Extracted literature claims:**
  `glossa-indus/claims/extracted_claims/*.json` — 31 claims in 10
  files. Every record already carries `proposition_fingerprint`,
  `stage`, `stage_source`, `stage_as_of`, `stage_history`,
  `claim_status`; 23 of 31 carry `explanation_record` and
  `not_understood`; stored relations are sparse (`evidence_instances`
  on 5, `contradicting_evidence` on 4, `merged_into` on 8,
  `source_document_id` on all 31, `sign_ids` on 1, `signs_involved`
  free text on 6). **No record carries a falsifier field** —
  `testability` is adjacent to, and is not, a falsifier.
- **P2 — Spec governance bundles:** `specs/*/claims.json` (52 files)
  and `specs/*/aee-claims.json` (56 files) — 1,592 claim records
  across both globs (the audit's census): 1,126 carry non-empty
  `depends_on`, 0 carry `conflicts_with`. These are the
  freeze-gate-governed claims (C4), each with falsifiers and AEE
  adjudication states, living per-spec. Whether the two formats
  double-count any (spec, claim) pair is a migration reconciliation
  question, not assumed either way.
- **P3 — Research-check sidecars:**
  `glossa-indus/claims/research_checks/*.research_check.json` — 31
  files, each keyed by `claim_id` + `document_id`, `stage:
  "research_check"`, `advisory: true`, `verdict: null`, produced by
  the Spec 025 stage (`backend/glossa_lab/research_check.py`), whose
  ratified contract (repo `AGENTS.md`) is that it "never modifies a
  claim, score, or status, and never adjudicates a decipherment."

Adjacent stores the matrix will need as its evidence universe (not
claim populations): the canonical anchors file
`backend/reports/INDUS_FINAL_ANCHORS.json` (287 entries; tiers HIGH
166 / MEDIUM 5 / LOW 3 / CANDIDATE 113 as recomputed in D-A's text;
94 strict; each record D-A-annotated with `validation_status` and
`strict_set`); the `anchor_sets` database table (operator-built sets
whose `pairs` payloads, sampled live 2026-11-01, are generic
`{"cipher","target","confidence","note"}` strings, **not**
frame-qualified sign ids); hypotheses (database table +
`glossa-indus/hypotheses/models/`); corpus texts; and
`discovery_items` (database table; a fetch pipeline's candidates).

The live database carries **no claims table** (verified against
`backend/glossa_lab/database.py`'s table list) — per the Spec 080
custody finding, the claims of record live in the repo checkout. The
on-disk graph stores (`glossa-indus/claims/support_graph/`,
`contradictions/`, `claim_clusters/`, `normalized_claims/`) are empty
(`.gitkeep` only, verified).

What already conforms: D-B is implemented and enforced at extraction
intake today (`proposition_fingerprint.py` raises
`DuplicatePropositionError`); the Spec 029 lifecycle gives claims a
stage vocabulary (created, checked, explained, accepted, digested)
whose stored value is, per D-E, "a cache with provenance, never an
assertion"; AEE scoring state exists per claim where scored (pinned
AEE 1.5.3).

### (c) Adoption design — the ledger

**Home and format (decision item D-086-Q5).**
`glossa-indus/ledger/` in the repo, Atlas-shaped:

- `glossa-indus/ledger/claims.jsonl` — the ledger. One JSON object
  per line, append-only. Git is the ledger's WORM layer: a correction
  is a new line (a reclassification entry), never an edit to an old
  line.
- `glossa-indus/ledger/SCHEMA.md` + a machine schema
  (`glossa-indus/ledger/ledger-schema.json`) — the pinned schema,
  versioned (`ledger-schema v1`); the Stage 1 validator enforces it
  in CI exactly as D-A's validator enforces the anchors schema.
- `glossa-indus/ledger/reclassifications.jsonl` is **not** a separate
  file: reclassifications are ledger lines with `kind:
  "reclassification"` and a `supersedes` pointer, so the ledger is
  one artifact with one intake (Spec 029's
  `reclassification-ledger.json` is the local precedent for the
  content; the form here keeps one file).

**Entry schema (v1).** Each entry carries: `id` (the canonical claim
id — for P1, the existing `claim_id`; for P2, `spec-id/claim-id`);
`kind` (`claim` | `reclassification`); `statement` (the atomic
proposition text — P1 `normalized_claim`; P2 the bundle's statement);
`proposition_fingerprint` (D-B, rules version
`spec029-phase-i-v1`, recomputed at intake, never copied on trust);
`population` (`extracted` | `bundle`); `sources` (P1:
`source_document_id` + evidence instances; P2: spec id + bundle path
+ bundle hash at import); `date` (the entry's intake/migration date)
and `as_of` (the source record's own as-of where it carries one);
`status` (the status **as held in the source of record** — P1
`claim_status`; P2 the bundle's adjudication state — mirrored, never
re-adjudicated by intake); `stage` (Spec 029 stage where computed,
with `stage_source` provenance per D-E; absent where not computed);
`aee_state` (`{direct, propagated, band}` where scored under the
pinned AEE; `null` where not scored — a null is shown as null);
`falsifier` (from the source record where it carries one; `null`
with the gap counted where it does not — see the falsifier-gap rule
below); `does_not_establish` (P1: the record's `not_understood` where
present; P2: the bundle's equivalent line where present; else
`null`, counted); `evidence_refs` (ids of anchors, texts, documents,
research checks, and studies the entry's source record names);
`sign_refs` (frame-qualified sign identifiers from
identifier-bearing fields only — Spec 085 FR-085-03 carries in
unchanged); `author` / `author_kind` where the entry carries
explanation content (see OD-2 under Point 6); `migration` (for
migrated entries: source path + source content hash + migration run
id).

**The falsifier gap, stated plainly.** The pattern requires a
falsifier per claim. P2 carries falsifiers. P1 does not (0 of 31
carry a falsifier field), and roughly a quarter of P1 lacks even
`not_understood`. This spec does **not** invent falsifiers for
existing claims — a falsifier written by the migration would be a
claim about the claim, authored by no one (OD-2's failure mode).
Instead: (i) migrated entries record `falsifier: null`; (ii) every
matrix build and gate run publishes the falsifier-coverage count;
(iii) the intake validator requires a falsifier for every **new**
claim entry from Stage 1 onward; (iv) backfilling an existing
claim's falsifier is a human-authored reclassification entry under
the normal adjudication discipline (decision item D-086-Q6).

**Intake paths (the only ways in).** All intake passes through one
validator CLI (`tools/ledger/validate_ledger.py` + the intake module
`backend/glossa_lab/ledger_intake.py`), which performs, in order:
schema validation against the pinned schema; proposition-fingerprint
recomputation and duplicate refusal (D-B — a collision names both
records and writes nothing, per the existing
`DuplicatePropositionError` contract); field-provenance checks (a
`falsifier`, `does_not_establish`, or explanation field must trace
to a source record or a named human-authored record); and the append
itself, through the repo's verified-write path with read-back hash.
The four intake routes:

1. **Extraction intake (P1, going forward).** The existing extraction
pipeline's writer gains a ledger append through the validator as
   its final step. A claim that fails validation does not enter, and
   the failure is loud (the D-B contract's shape).
2. **Bundle intake (P2, at freeze/adjudication events).** A
   mechanical import tool runs when a spec's claims bundle is frozen
   or its adjudication lands: it reads the bundle, emits one ledger
   entry per claim (status mirrored from the bundle's adjudication
   state), and records the bundle's path + content hash on every
   entry. The bundle remains the spec's governance artifact and a
   C4 freeze input; the ledger entry is its downstream mirror, and
   the mirror is regenerated — never edited — when the bundle's
   state moves by an adjudication act.
3. **Research-check intake (P3, annotation route).** The Spec 025
   contract stands untouched: the research-check stage stays
   advisory and never modifies a claim. What enters the ledger is a
   distinct, validated **annotation entry** — a ledger line with
   `kind: "annotation"`, the sidecar's id and content hash, the
   claim id it bears on, and the bearing the sidecar's own record
   states (sources found / not found, per its protocol). The
   annotation changes no status, stage, or score; it makes the
   check's existence and result addressable by the matrix (Point 2)
   under the relation rules of Point 4. A claim's status moves only
   through adjudication, as today.
4. **Discovery promotion (human act).** `discovery_items` never
   auto-enter. A named human promotes an item to a candidate ledger
   entry (`status: "candidate"`, falsifier required at promotion)
   through the validator; candidates are visible in the matrix as
   candidates and carry no weight in settling until adjudicated.

**Migration under D-E.** D-E, verbatim (same addendum):

> **D-E — Where the stages live: the audit ledger is the source of
> truth until the plan's re-staging migration.** … The governing
> invariant: **a stage is always recomputable from the record's
> evidence — the stored value is a cache with provenance, never an
> assertion.**

Applied here: each population migrates by a one-time mechanical
script, run per population as its own gated task, emitting a
**reconciliation report**: entries in == source records out, per
claim id; proposition-fingerprint collisions listed (expected: the
P2 double-format question is answered by this report, not assumed);
every mirrored status/stage byte-equal to its source; falsifier and
does-not-establish coverage counted. Until a population's migration
has run and reconciled, that population's current home remains its
source of truth and the matrix does not read it. After migration,
the ledger is the entry point for everything downstream; the old
homes remain as upstream sources of record for their own governance
(bundles for C4, extracted files as the extraction store) and are
never edited by any downstream layer. Migration is **read-only
against every frozen tree**: if a migration step appears to require
editing a frozen record (Spec 029's freeze, any spec's freeze.json),
it stops and reports — it does not proceed under any amendment
improvised inside this spec.

---

## 2. Point 2 — The matrix is generated, never made

### (a) Requirement

> "The **matrix is generated from the ledger** by script. If it is
> not in the ledger, it is not in the matrix." Research-check
> sidecars feed the ledger through intake only; they never write to
> the matrix or the map directly.

### (b) Current state

No claims×evidence matrix exists (audit verdict (b), PARTIAL): the
sign×sign co-occurrence adjacency lives inside analysis code; the
`CrossHypothesisMatrix` experiment node emits an on-demand roll-up
by regex-matching sign names out of claim text — a practice this
adoption retires as a relation source (Spec 085 FR-085-03). No
matrix is persisted or served.

### (c) Adoption design

**Artifacts.** `glossa-indus/matrix/` holding the generated outputs
(`matrix.json`, `matrix.md`, in the Atlas's shapes), produced by one
generator (`backend/glossa_lab/matrix_generate.py`, invoked as
`tools/ledger/generate_matrix.py`) reading **only** the ledger plus
the evidence registers the ledger entries reference.

**Shape.** Rows: ledger claim entries (canonical ids). Columns: the
evidence universe, in registered column classes — anchor records
(canonical anchors file ids), corpus texts, evidence documents
(literature), research checks (by sidecar id, via annotation
entries), and studies (by spec id). Cell value: one of **supports /
opposes / constrains**, plus the citation ids and the derivation
rule id that produced the cell. An empty cell is the absence of a
derivable relation, shown as absence — never filled by judgment.

**Derivation rules (registered definitions).** Each cell arises from
exactly one registered rule, e.g.: supports ← a claim's stored
`evidence_instances` naming the document, or a `tested_by` record
whose study outcome supports the claim; opposes ← stored
`contradicting_evidence`, or a `tested_by` outcome that refutes it;
constrains ← an anchor record whose frame-qualified sign intersects
the claim's `sign_refs` with a recorded assignment (the assignment
bounds the claim's reading space), or a registered settling
instrument whose subject set includes the claim. The rule set lives
in `glossa-indus/matrix/DEFINITIONS.md` with a machine copy inside
both the generator and the gate (the Atlas's registered-copies
pattern: the gate's independence comes from recomputing by a second
route; a deliberate rule change is made in both copies in the same
motion and the gate flags artifacts built under the old rules until
regenerated). Definitions are versioned (`matrix-defs v1`).

**Honesty note on "never made."** The Atlas's own generator carries
hand-registered definition tables (load map, tag overrides,
instrument set) — verified in its source. "Generated, never made"
holds for the data; the *definitions* are human-registered,
versioned, and auditable. Glossa adopts the same split and names it,
rather than claiming a purity the reference implementation does not
have.

**Coverage is part of the artifact.** Every generation emits the
coverage block the gate later checks: rows with no non-empty cell,
columns never borne on, falsifier coverage of the ledger, and
unresolved sign mentions (free-text `signs_involved` that no
identifier resolves — the curation work list, carried from Spec
085). The sign×sign co-occurrence block is imported from the
existing pipeline output for the same corpus snapshot, not
recomputed by new code (Spec 085 FR-085-04 carries in).

---

## 3. Point 3 — The matrix runs: mechanical settling, interchangeability

### (a) Requirement

> "The **matrix runs**: the representation is executable in the
> project's engine (settle, propagate, project), so a system's
> implications are computed, not narrated." — and the owner's order:
> sign-value assignments are treated as a constraint system over the
> matrix and settled mechanically — checked against every anchor
> context touched, coverage and conflicts computed and enumerated;
> dual readings follow the interchangeability discipline (same
> inputs, both readings, divergences listed claim by claim); a result
> not recomputable from the ledger by script is not reported as a
> result. Pattern point 6 adds: where two readings exist, "their
> agreement is proven against pre-registered expectations, not
> asserted."

**Adopted refinement (harmonization, 2026-11-01):** the Atlas
pattern note `PATTERN-NOTE-2026-11-01-gate-and-settle` (see
README.md for the adoption record and first-hand verification)
requires the settle layer to be **barred by hand before it is
built**: semantics registered in writing first, canonical outputs
derived by hand in prose, the engine written last, its tests
requiring exact reproduction of the hand-derived canonicals;
outputs labeled computations over ledgered relations; and **no
write path** from the settling layer to the ledger. This spec
adopts that discipline in full for Stage 4.

### (b) Current state

There is no settling engine (audit verdict (d), NO): the one
in-product node named for constraint projection is a stub returning
"Constraint projection engine not available" (`experiment_graph_
phase14.py`, "engine removed"); Specs 076/078 are closed one-off
studies whose verdicts stand (076: assumption set does not hold;
078: cannot be administered) and whose designs this spec does not
resurrect. What runs today is AEE scoring with weakest-link
propagation — over the spec-bundle population's `depends_on` edges
in governance, and over an effectively edgeless graph in the live
app (the audit's identity-propagation finding). Spec 085 §7 defined
four constraint kinds and the subsumption rule (the engine extends
`aee/scoring.py`; it never forks it); both carry into this point's
design.

### (c) Adoption design — derive-before-build settling

**Step 1 — semantics registered first (no engine code in the same
act).** `glossa-indus/ledger/SETTLING-SEMANTICS.md`, version
`glossa-settle-1`, registered before any settling code exists. Its
rules are derived from **Glossa's own ledger** — anchor tiers and
validation states under D-A, the Spec 073/074 precedent of testing
on a frozen classification surface, the matrix's registered
relations. **The Atlas's settle-1 constants (its window breaks at
3+ broken feeders, or 2+ with the amplifier as third leg) are
Atlas-specific, grounded in that study's ledgered claims, and are
explicitly NOT lifted** (the note's own limit, adopted verbatim in
substance). The v1 rule set:

- **S-R1, anchor-context check.** An assignment entry is a
  (frame, sign id) → value mapping. Its anchor contexts are every
  canonical anchor record for that sign in that frame. Where a
  strict anchor (D-A `strict_set`, recomputed under the recorded
  rule version) assigns a different value, the entry is in conflict;
  every conflict is enumerated as (entry, anchor id, both values).
- **S-R2, matrix-bearing check.** For each assigned sign, every
  ledger claim whose `sign_refs` include it is checked: a claim
  whose recorded outcome or falsifier bears against the assigned
  value's reading family is enumerated as opposing; a supporting
  outcome as supporting; a claim whose falsifier would be triggered
  by the assignment is enumerated as constraining. Unexecuted or
  null-outcome tests bear neither way (Point 4's T2 rule, applied
  here at run time).
- **S-R3, internal consistency.** Two signs in the same registered
  positional class (from `canonical_signs` positional attributes)
  assigned the same value violate the distinctness rule where the
  semantics register it; violations enumerated pairwise.
- **S-R4, coverage.** Computed, never narrated: assigned share of
  the frame's sign inventory; strict-anchor agreement share over
  contexts touched; claims touched (matrix rows intersecting
  assigned signs) with their bearing tallies.
- **Forced consequences (narrow, finite).** A value is reported as
  forced only where every assignment set consistent with S-R1/S-R3
  assigns it — computed over those finite kinds only. Score ceilings
  under dependency remain AEE's propagated scores (subsumption,
  below); the settling layer reports them, it does not recompute a
  rival number.

**Step 2 — canonical outputs derived by hand.** Before the engine
is written, at least four canonical scenarios are derived in prose
from the ledger and matrix, and registered in
`glossa-indus/ledger/settling-canonical.json` in the Atlas's shape
(clamps/inputs, prose `derivation`, `expected`): the null assignment
(coverage zero, no conflicts, no witnesses); the incumbent set
(Step 3) over a named sign subset with hand-counted coverage and
conflicts; the full-register set over the same subset; and one
seeded-conflict assignment whose conflict enumeration is derived by
hand. The prose derivations are the review surface — the Atlas
note's named limit (derivations and engine share an author) is met
here by making the derivations part of the Stage 4 approval record
the owner reads.

**Step 3 — the engine, last.** `backend/glossa_lab/settling.py`
evaluates an assignment-set record over one ledger build (build id
= ledger content hash) and writes a **run record** (inputs, rule
version, per-rule outcomes, enumerations, coverage) to the run
store. Its test (`backend/tests/test_settling_canonical.py`)
requires **exact reproduction** of every registered canonical —
levels of agreement included: counts, enumerations, and tallies
equal, not approximately. A mismatch means the engine or the
registered derivation is wrong; the fix is made in the open, never
by quietly editing the expectations (the Atlas test's stated bar,
adopted).

**Assignment sets of record.** An assignment set is a stored record
under the ledger's perimeter (not a ledger claim; it enters through
the same validator as a registered instrument, with author and
provenance). V1 registers two from stored data alone: the
**incumbent** — the strict anchor set (94) read as assignments —
and the **full-register** set (all 287 canonical anchors). A
literature challenger (a published alternative reading's
assignments) enters only as its own intake record with sources;
none is fabricated for v1.

**Interchangeability protocol.** A dual run executes the same
engine, same ledger build hash, same corpus snapshot hash, over two
assignment sets; both run records are stored; the comparison output
is a **per-claim divergence list**: every ledger claim whose matrix
bearing (supporting/opposing/constraining tallies under S-R2)
differs between the runs, with both tallies shown, plus the
coverage/conflict deltas. Where a pre-registered expectation exists
in the program's record for a touched claim (a frozen study's
outcome record, e.g. Spec 074's), the comparison names it and
reports agreement or divergence against it — proven against the
expectation, not asserted (pattern point 6).

**Labels and the write bar.** Every settling output, in every
surface, carries the label: "Computation over ledgered relations
under glossa-settle-1 semantics. Establishes what the ledger
implies under these rules, not what the script says." Settling
outputs are not claims, never enter the ledger, and move no status,
stage, score, or weight; anything a run appears to discover
re-enters only through Point 1 intake. Mechanically: the settling
package has **no write path to the ledger** — it imports no intake
or write module, and the Point 4 gate audits that (check V9).

**Subsumption (carried from Spec 085 §7, unchanged).** The engine's
propagation core is `aee/scoring.py` over a ClaimGraph whose edge
source is the ledger/matrix relation set; where a settling rule
and AEE semantics disagree about a claim, AEE's number stands as
the score and the disagreement is reported as a witness. The four
Spec 085 constraint kinds (score-floor, anchor consistency, support
floor, contradiction tension) are retained as the projection
vocabulary the settling rules extend; Spec 085's claims C085-8…12
map onto C086-13…16 below.

---

## 4. Point 4 — A verification gate guards every publication

### (a) Requirement

> "**Every arrow is machine-checked**: a verification test
> recomputes each downstream layer from its source and *gates the
> build* — on failure, nothing ships. Codec and regeneration checks
> are lossless; drift is a defect."

**Adopted refinement (harmonization, 2026-11-01):**
`PATTERN-NOTE-2026-11-01-gate-and-settle` adds three mechanics,
adopted here in full: **(i) relation-carrying citations** as the
gate's decisive check class; **(ii) gated publication** —
candidate artifact → gate → replace the published artifact only on
a pass, a red gate leaving the previous artifact byte-untouched;
**(iii) lossless regeneration as a checked mode** — byte-compare
after regeneration; any diff is either exactly the intended change
or a downstream defect, and is never closed by hand-editing the
artifact.

The note names the failure mode this point exists to catch, and
this spec adopts the naming verbatim:

> **A citation can exist, be relevant, and still not carry the
> relation.** … Corollary for all framework projects: builder
> comments are not verification, and an edge's citation list is a
> claim, subject to the same discipline as any other claim.

(The Atlas instance: its gate's first run passed 202 checks and
failed exactly one — an edge citing a falsifier that belonged to a
different load; every existence and count check had passed. The
repair went in the downstream layer; the gate was not loosened.
Verified first-hand 2026-11-01: gate 204 PASS / 0 FAIL; a flipped
ledger status in a scratch copy turns it red, 6 FAIL.)

### (b) Current state

Glossa has a correctness-bearing CI gate of the same family: the
**C4 freeze-gate** job (`.github/workflows/ci.yml`, job
`freeze-gate`, "Freeze gate records check (C4)") runs
`tools/freeze-gate/check_freeze_gate.py --pr-scope` on PRs and
`--all` on pushes, under the pinned evaluator (AEE 1.5.3,
`tools/freeze-gate/evaluator-version.txt`); and the Spec 082
delivery checker (`tools/delivery-check/check_delivery.py`) proves
delivered artifacts against run records. What does not exist: any
gate over a ledger → matrix → map chain, because the chain does not
exist yet; and no Glossa gate today checks that a citation *carries*
its relation (Spec 084's conformance tests diff served text against
fixtures — an existence/fidelity check of a different kind).

### (c) Adoption design — the ledger gate

**Placement.** A new CI job in `.github/workflows/ci.yml` beside
C4: job `ledger-gate`, "Ledger/matrix/map equivalence gate",
running `tools/ledger/check_ledger_gate.py` — `--pr-scope` on PRs
(gate over the artifacts the change touches), full mode on pushes
to main, and a `--regen` mode mirroring the Atlas's. The C4 job is
untouched; the two gates are siblings, and a red in either blocks
merge under the standing CI rule.

**Check classes** (each check prints PASS/FAIL with its evidence;
the stage reports carry this output verbatim):

- **V1 — Ledger validity.** Every ledger line validates against
  the pinned ledger schema; every entry's proposition fingerprint
  recomputes under `spec029-phase-i-v1`; no two canonical entries
  share a fingerprint (D-B); every reclassification points at an
  existing entry; migration entries' source hashes match their
  source files.
- **V2 — Count equivalence.** Claims by status, by stage, and by
  population recomputed from the ledger == the matrix's header
  counts == the map's header counts.
- **V3 — Matrix recomputation.** The matrix is recomputed from the
  ledger by an independent route (registered definition copies)
  and compared cell-for-cell: relation, citation ids, derivation
  rule id.
- **V4 — Relation-carrying citations (the decisive class).** For
  every citation on every non-empty matrix cell and every map
  edge, at least one registered tie must mechanically hold
  between the cited record and the relation asserted:
  - **T1, source membership:** the cited record is the claim
    itself, or is named in the claim's stored relation field for
    that relation (`evidence_instances` for supports;
    `contradicting_evidence` for opposes; the bundle's evidence /
    `depends_on` records for governance claims).
  - **T2, dated test:** the cited record is a study that tested
    the claim (the claim's stored per-spec outcome records name
    it) **and** its recorded outcome direction matches the
    relation — a supporting outcome for supports, a refuting
    outcome for opposes. An unexecuted or null outcome carries
    neither relation (standing example: Spec 054's UNEXECUTED
    closure may not be cited as support or opposition for the
    Yadav claim).
  - **T3, registered anchor:** the cited record is a canonical
    anchor whose frame-qualified sign intersects the claim's
    `sign_refs`, and whose tier/validation state is as cited (a
    citation claiming a strict anchor must recompute as strict
    under the D-A rule version recorded in the anchors file).
  - **T4, registered instrument:** the cited record is a
    registered constraint or assignment record whose subject set
    includes the claim or its signs.
  Existence, shared documents, shared signs without a T3 anchor
  record, and topical relevance are **not** ties. A citation with
  no tie fails the gate, naming the cell, the citation, and the
  relation it failed to carry.
- **V5 — Map recomputation.** Every map element traces to ledger
  ids; embedded claim fields equal the ledger's; the map's loads
  block deep-equals the matrix's; per-element relation citations
  pass V4.
- **V6 — Anchor shares.** The validated-anchor share and the
  strict share in the map header recompute from the canonical
  anchors file under its recorded D-A rule version.
- **V7 — Lossless regeneration (checked mode).** `--regen`:
  hash matrix + map artifacts, regenerate both from the ledger,
  byte-compare. A diff is either exactly the intended change
  (named in the change that carries it) or a downstream defect,
  fixed by regeneration — never by editing the artifact.
- **V8 — Settling canonicals (Stage 4 onward).** The registered
  hand-derived canonical scenarios reproduce exactly under the
  engine (Point 3, Step 2's bar), run as part of the gate job.
- **V9 — No write path.** The settling/scenario packages import
  no ledger intake or write module; the generator and gate are
  the only writers of matrix/map artifacts, and they write only
  through the gated-publication path.

**Gated publication.** Every generated artifact (matrix files,
map data) is produced as a **candidate**: the builder writes a
candidate file, the gate runs against the candidate
(`check_ledger_gate.py --candidate <path>`), and the published
file is replaced only on ALL PASS — in CI, the merge consumes
only gated artifacts; locally and in the app bundle, the same
candidate → gate → replace mechanics apply (the Atlas's
`build_graph.py` publish block is the reference shape, verified
2026-11-01). A red gate leaves the previously published artifact
byte-untouched and fails the build. The gate's teeth are proven
by negative control in Stage 3's acceptance: a scratch tree with
a seeded divergence (a flipped status; a P4-027-style miscarried
citation) must turn the gate red, name the diverged checks, and
leave the published artifact unchanged.

---

## 5. Point 5 — A layered map is the primary surface

### (a) Requirement

> "A **layered map is the primary surface** (system → component →
> evidence), rendering exactly the generated data, with the
> headline state carried in its header and every element traceable
> to ledger ids." The owner's order adds: header carries claims by
> status, validated-anchor share, and the nearest dated items; the
> map renders the generated data exactly and nothing else.

### (b) Current state

The app's 17 Spec 081 screens digest claims, studies, signs, and
pipelines one kind at a time; no screen renders the system's graph
or any matrix (audit verdict (c), PARTIAL). Spec 085 drafted the
System graph screen (three wireframes, owner approval pending) as
a graph/matrix/projection surface over a *derived entity graph*.
Under this adoption the surface's data source changes — ledger →
matrix → generated map data, gated — and its design is conformed,
not restarted (README.md lists the deltas).

### (c) Adoption design

**Artifact.** The map's data layer is a generated artifact,
`glossa-indus/map/map-data.json`, produced from the matrix by the
map builder and published only through Point 4's gated
publication. The in-app surface renders that artifact and live
API responses derived from the same gated data — nothing else.
Every visual element carries the ledger ids behind it (claim ids
on claim elements; anchor/document/check ids on evidence
elements), inspectable in the surface.

**Views (system → claim → evidence).**

- **System view** — the decipherment model as a whole: sign
  inventory by frame with assignment state (the incumbent settling
  run's coverage), where the load sits (conflict and
  zero-coverage hotspots from the matrix coverage block), the
  claim population by status and stage.
- **Claim view** — one claim: statement, status, stage, AEE state,
  falsifier, "this does not establish" line, its matrix row
  rendered (what bears on it, and how), its settling bearing under
  the incumbent and any challenger run.
- **Evidence view** — the anchors, texts, documents, and research
  checks behind a claim: the matrix column side, each element
  traceable to its register record.

**Header (headline state, all recomputed and gate-checked):**
claims by status; validated-anchor share (strict share, V6);
nearest dated items — defined mechanically as the dated ledger
items nearest today (pending validations, dated study outcomes,
held items carrying review dates), taken from ledger date fields,
never hand-typed (D-D, Point 6).

**Wireframes.** Stage 5 begins from Spec 085's three approved-
pending screens (01 explorer, 02 matrix, 03 projection panel)
with the deltas listed in tasks.md (header strip; ledger-id
citations; matrix view's primary form becomes claims×evidence
with claim×sign as a column-class filter; projection panel
becomes the settling panel with the incumbent/challenger
divergence view). The conformed wireframes go to the owner for
approval **by name** before any surface code is built (Spec
081/083 precedent; the owner's standing wireframe rule). Nothing
in this spec pre-approves pixels.

---

## 6. Point 6 — Governance: truth flows one way

### (a) Requirement

> "**Truth flows one way**: ledger → matrix → map. Downstream
> layers are never hand-edited; a disagreement is a defect in the
> downstream layer." Generated reports carry as-of stamps (D-D,
> generalized); verdicts move only by mechanical, recomputable
> migration (D-E).

D-D, verbatim (Spec 029 addendum):

> **D-D — Foundation report annotations: as-of label now;
> generated annotations as the structural fix.** … Structural: the
> report's claim annotations are **computed from the canonical
> data at report time**, stamped with the anchor file's hash,
> never hand-typed; and the foundation status endpoint is repaired
> to serve the on-disk report or fail loudly.

D-E's invariant, verbatim: "**a stage is always recomputable from
the record's evidence — the stored value is a cache with
provenance, never an assertion.**"

### (b) Current state

The disciplines exist in pieces: append-only reclassification is
Spec 029's house rule (its reclassification ledger; today's PR
#477 amendment executed exactly this pattern on the lane-2
adoption record); freeze records pin governed artifacts with the
C4 gate over them; Spec 084 fixtures hold approved public texts
with conformance tests in CI; D-D's structural half is implemented
for the foundation report. What is missing is the single declared
chain for the decipherment record as a whole — which is this
spec.

### (c) Adoption design

- **One-way flow, mechanically held.** The ledger is the only
  input to the generator; the matrix is the only input to the map
  builder; the gate (Point 4) is the enforcement. A disagreement
  discovered in any downstream layer is filed as a defect in that
  layer and closed by regeneration or by a ledger correction
  through intake — never by editing the downstream artifact.
- **As-of stamps (D-D generalized).** Every generated artifact
  (matrix, map data, settling run records, and any report that
  cites claims) carries: generation time, the ledger content
  hash it was computed from, and the definition/rule versions in
  force (ledger schema, matrix-defs, glossa-settle-1 where
  applicable). A stamp whose hash does not match the ledger at
  read time marks the artifact stale in every surface that shows
  it — the D-D failure mode (stale figures riding unflagged) is
  the named target.
- **Verdict movement only by migration (D-E).** A claim's status
  or stage changes in the ledger only via (i) an adjudication act
  in its source of record, mirrored by bundle/extraction intake,
  or (ii) a reclassification entry appended through intake with
  its evidence and provenance. No layer below the ledger holds a
  status of its own; the matrix and map display the ledger's
  values or nothing.
- **Authorship (OD-2) is preserved, not flattened.** OD-2
  (Spec 029): the explanation gate accepts "a named, accountable
  human author"; an explanation counts only when such a human
  authors it in a durable record (the 2026-10-13 lane-2 adoption
  and its 2026-11-01 amendment are the operating precedent).
  Mechanically imported ledger entries carry machine provenance
  and **no** explanation authorship: intake rejects any entry
  carrying explanation content without a named human author and
  its adoption record, and entries without one simply stand at
  their computed stage — the matrix and map show the gap rather
  than papering over it.
- **Spec 084 boundary.** Public texts stay under Spec 084's
  fixture regime. The Stage 5 map is an in-app operator surface;
  if a public map is ever wanted, its texts enter through Spec
  084's approval path first (its T011 slot), and the tracker's
  standing texts keep flowing through the Spec 084 publish path
  (C084-9), not through this spec's map builder.

---

## 7. Point 7 — Harmonization

### (a) Requirement

The standing rule as quoted in §0: the concept and discipline are
always accompanied by the epistemic ledger in every project using
the framework; framework projects stay harmonized (current users:
RCPH / projected-constraints, the framework's home; the
Breaking-Point Atlas, Axiovex Systems chat; Glossa-Lab, this
chat). Improvements are written up as short pattern notes and
delivered to the other framework chats; a receiving chat adopts
unless the improvement conflicts with a ratified local decision,
in which case it surfaces the conflict to the owner rather than
diverging silently.

### (b) Current state

This adoption is itself the rule's first exercise in this chat:
the owner's order arrived from the RCPH chat with the canonical
note; the Atlas's gate-and-settle note arrived the same day and
is incorporated at Points 3–4 (adoption record in README.md,
with first-hand verification of its proof claims).

### (c) Adoption design

- **Incoming notes** are read against this spec and the ratified
  local decisions before adoption; adoptions and any conflicts
  are recorded in this spec's repo record (and surfaced to the
  owner where the rule requires), never silently absorbed or
  silently dropped.
- **Outgoing notes.** Two candidate improvements are already
  visible and are assigned as stage deliverables, not afterthoughts:
  (i) the generalization of D-A's pinned-schema + CI validator
  from the anchors file to a program's ledger schema (Stage 1
  closeout writes it up); (ii) the falsifier-gap census — a
  coverage count for a pattern-required field the legacy
  population lacks, published by the gate instead of filled by
  invention (Stage 3 closeout writes it up). Each is delivered to
  the RCPH and Atlas chats as a short pattern note when produced.
- **The D-A gloss divergence is handled in the open.** The
  adoption order's shorthand ("D-A pinned-schema validator")
  generalizes the decision's literal subject (the anchors file).
  This spec follows the decision as written and labels the
  generalization an extension (Point 1). If the framework prefers
  the generalized naming, that is an amendment to the canonical
  note, proposed through the rule's own path — not a silent local
  redefinition (README.md, conflicts).

---

## 8. Decision items for the owner

The package is approvable as a block; these items carry draft
defaults the owner may amend in the approval act.

- **D-086-Q1 — Reports in the map** (Spec 085 Q1, restated). The
  app serves ~1,230 reports. Under the pattern, reports are not
  ledger entries and not matrix rows. Draft default: reports
  appear in the evidence view only where a ledger entry cites
  them (as evidence elements with their ids), never as first-class
  nodes. *085's draft took nodes; the pattern's ledger discipline
  is the reason this draft reverses it — the owner's ruling
  governs.*
- **D-086-Q2 — Settling/constraint authorship** (Spec 085 Q3,
  restated). Draft default: assignment sets and constraint records
  are authored as stored records outside the UI, under the
  program's approval discipline; the surface runs and reads. In-app
  authoring would be a further spec section.
- **D-086-Q3 — Cloud scoping timing** (Spec 085 Q4, restated).
  Draft default: the ledger, matrix, and gate are repo-side
  canonical artifacts under the operator perimeter; the in-app map
  ships desktop-first, inheriting Spec 083 scoping per record
  (non-widening, C086-19), and the cloud map waits for the Spec 083
  linkage closures named as its pre-launch gate. The claims are
  written so either order satisfies them.
- **D-086-Q4 — Stage 4 demonstration pair.** Draft default: the
  first dual run is incumbent (strict-94) vs full-register (287) —
  two real, stored, distinct assignment states — rather than
  waiting for a literature challenger to be intaken.
- **D-086-Q5 — Ledger home and format** (cited at Point 1).
  Draft default: `glossa-indus/ledger/claims.jsonl`, Atlas-shaped
  JSONL, schema pinned at `ledger-schema v1`.
- **D-086-Q6 — Falsifier-gap policy** (cited at Point 1). Draft
  default: prospective requirement at intake; existing gap counted
  and published by every gate run; backfill only by human-authored
  reclassification under adjudication discipline.

**Answered in drafting (not a decision item):** Spec 085 Q2
(anchor-pair payload shape). Sampled live 2026-11-01, the
`anchor_sets.pairs` payloads are generic cipher/target strings,
not frame-qualified sign ids; Spec 085's fallback is therefore the
operative path — user-built anchor sets are not settling contexts
in v1; the canonical anchors file is. Recorded here so the
question does not ride forward as open when it is not.

## 9. Non-goals

- No decipherment verdict, claim status, stage, or score changes;
  the standing position is untouched (C086-20). The script remains
  not deciphered; nothing in this spec is evidence about the
  script.
- No new scorer; no change to AEE scoring semantics (pinned
  1.5.3); no resurrection of Spec 076's assumption set or Spec
  078's design.
- No schema change to any store of record in v1; the ledger is a
  new artifact, and migration reads — never edits — the existing
  stores and every frozen tree.
- No invented relations and no invented falsifiers: where the
  record carries nothing, the layers show nothing and count the
  gap.
- Spec 072 is not inspected, summarized, or circulated by any
  part of this work; it enters the ledger, if at all, name-only
  under its existing restriction.
