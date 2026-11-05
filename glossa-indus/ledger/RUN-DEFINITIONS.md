# Run definitions — `run-defs v1`

Spec 089 (run-scoped results), Stage 1, task T101. This
document is the contract the run machinery runs under: the
surfaces, the run-id format and minting rule, the run-record
header, the comparability key (**run-key v1**), the
determinism classes, the junction disposition vocabulary,
and the run-index act format are registered here, versioned,
and are the only ones the machinery may use. A machine copy
of every registered table in this document lives in the
library (`backend/glossa_lab/run_records.py`); the Stage 5
gate class (V11) will carry its own registered copies, and a
deliberate change to any definition is made in every copy in
the same motion, as a new version of these definitions.
Acceptance for this document is human-as-oracle: the owner
settled the judgment rows at the package ratification
(T003, decisions D-089-1..6, including the comparability
judgment row D-089-4). *This does not establish the
definitions are the right semantics — it establishes they
are written down, versioned, ratified, and the only ones
the machinery may use.*

**The honesty split, stated once.** The definitions in this
document are human-registered; the records produced under
them are machine-written at execution time and never edited
afterwards. Relations a record cannot carry about itself
(supersession, quarantine, adjudication) live in the run
index (§7), never as flags edited onto a record (D-089-3,
C089-2).

## 1. Surfaces — the closed list, and the result-bearing test

An execution is **result-bearing** iff its output is written
to a store of record or cited in a record of record. Only
result-bearing executions mint run ids and write run
records; exploratory commands remain exploratory and mint
nothing. The named surfaces are a closed list:

| Surface token | Executions | Store of record |
|---|---|---|
| `settling` | Settling runs (`glossa_lab.settling` via `tools/ledger/run_settling.py`): scenario evaluations, dual-run comparisons, set materializations | `glossa-indus/ledger/runs/` |
| `experiment` | Backend experiment jobs, at citation time: the job executes in the live backend under its own execution-minted job id (uuid); the run record on this surface is the repo-side citation record that binds the job id and its recorded inputs (C089-8) | The citing spec's `records/` (Stage 4 writer) |
| `study` | Study re-executions: a frozen study's recomputation or re-run under its freeze record | The study's spec `records/` |
| `suite` | Suite runs cited as evidence: CI runs (bound by the CI citation form, §7.3) and local evidence runs (bound by a lightweight run record, Stage 4) | The citing stage's records |

A surface not on this list has no registered determinism
class (§5) and its runs cannot be cited as evidence until a
run-defs amendment registers it (C089-19).

## 2. Run identity (D-089-1)

A run id has the form

```
<surface>-<yyyymmddThhmmssZ>-<6 lowercase hex>
```

e.g. `settling-20261104T073900Z-a1b2c3`. The timestamp is
the execution's start, UTC, at one-second resolution. The
trailing component is six lowercase hexadecimal characters
drawn from a cryptographic random source at minting time.

- **Minting point.** The id is minted by the executing tool
  at execution start, before any results exist — so an
  execution that crashes, refuses, or produces nothing still
  has an id and a run record stating the absence (§3).
- **Ids name executions, never content.** An id is never
  derived from the run's inputs, results, or any hash of
  them. Two executions with identical inputs and identical
  results carry different ids. (The settling store's retired
  content-addressed filename — a hash of {candidate, scope,
  pins, scenario} under which a same-basis rerun replaced
  its own record — is the defect this rule removes; its
  retirement on the write path is Stage 2's act.)
- **Uniqueness.** The minter never issues the same id
  twice: within a minting process it remembers the ids it
  has issued and redraws on collision. A store write that
  would collide with an existing record path or index entry
  refuses (Stage 2 registers the refusal on the settling
  write path); an id collision is a named refusal, never an
  overwrite.
- **Never caller-assigned after the fact.** A citing record
  names the id the executing tool minted; it never assigns
  one. Pre-spec records are the one exception in form only:
  they receive *legacy* ids in the index, derived under §7.2,
  and are labeled as such wherever cited (C089-17).

## 3. The run record

A run record is a JSON object. It carries a **header**
under the key `run`, the surface's own fields, and exactly
one outcome: a `result` block, or an **absence block**
under the key `absence`. A run record, once written, is
never edited or deleted by a later run (C089-2).

### 3.1 Header fields

| Field | Content |
|---|---|
| `run_id` | The execution-minted id (§2), or a legacy id (§7.2) in index entries only — never inside a pre-spec record, whose bytes are untouched |
| `surface` | One of the §1 surface tokens |
| `tool` | The executing tool's name (e.g. `run_settling.py run`) |
| `tool_version` | The executing tool's version as the tool reports it |
| `started` | Execution start stamp, ISO 8601 UTC (`...Z`) |
| `finished` | Execution finish stamp, ISO 8601 UTC; present unless the execution is still running at record time — a finished record always carries it |
| `key` | The comparability key (§4), complete for the surface |
| `determinism_class` | The surface's registered class (§5); for the `experiment` surface, the per-graph registered class (§5) |

A run record is a record of an *event*, so its stamps are
wall-clock execution stamps. This is a deliberate exception
in form, not in spirit: the Spec 086 input-derived-stamp
discipline governs generated artifacts (whose content is a
function of their inputs) and is untouched; an execution is
not a function of its inputs, and its stamps say when it
happened.

### 3.2 The absence block

A no-result execution's record carries, instead of a
`result` block:

```json
"absence": {"kind": "empty" | "refused" | "crashed", "detail": "<what happened>"}
```

The kinds are a closed list: `empty` (the execution ran and
produced no results), `refused` (the execution declined —
a precondition, validation, or gate refusal), `crashed`
(the execution failed mid-run). An absence block with a
kind outside this list is not a run record. The one-side-
empty case the junction rule polices (C089-11) is stated in
this form, never as a missing record.

## 4. run-key v1 — the comparability key (D-089-4)

Every run record carries its full key under `key`:

| Component | Content | Constitutive |
|---|---|---|
| `surface` | The §1 surface token | **yes** |
| `command` | The command/tool invocation that executed (e.g. the CLI subcommand and its scenario argument) | **yes** |
| `tool_version` | The executing tool's version | **yes** (with `command`: the command/tool component) |
| `input_pins` | The per-surface pin list (§4.1) | **yes** |
| `seed` | The execution's seed, or the registered no-seed marker (§4.2) | **yes** |
| `code_version` | The git SHA of the tree executed (for backend jobs: the deployed build identity) | no — recorded and diffed |
| `environment_class` | Venue/runtime class token, e.g. `ci/linux`, `vm/linux`, `desktop/windows` | no — recorded and diffed |

Two runs are **comparable** (the owner's "similar") exactly
when their keys agree on every constitutive component
(C089-9). Agreement is decided by the key, never by names:
the same scenario name does not make two runs comparable,
and different names do not make them incomparable
(C089-10). Where two keys differ on a constitutive
component, the pair is reported as **different experiments,
with the differing component named** — never as a
divergence, and never pooled. A code-version or
environment-class difference does not break comparability;
it is what a junction explains *with* (D-089-4's judgment
row: under the alternative, a rerun after a code fix could
never trigger a junction, exempting exactly the divergences
the rule exists to catch).

### 4.1 Input pins, per surface

- **settling**: the run record's existing `pins` block,
  verbatim (ledger SHA-256 + lines; anchors-register raw
  SHA-256 + record/strict counts; phase108-register
  SHA-256; corpus-snapshot SHA-256).
- **experiment**: the job's recorded inputs — graph id +
  registered graph version, parameters, and the job's data
  pins where the graph reads data.
- **study**: the freeze record's pin set — the study's spec
  id and the frozen artifacts' hashes the re-execution ran
  against.
- **suite**: the invocation's selection (the test paths /
  node ids named on the command line). The tree state the
  run measured (tree SHA + dirty flag) is carried in the
  light record beside the header (Stage 4), not in the key;
  the tree SHA is the key's `code_version`.

### 4.2 Seed

A surface with a seed records the seed value. A surface
with no seed records the registered no-seed marker, the
string `"no-seed"`. The component is never omitted: an
absent seed component is a malformed key, not an unseeded
run.

## 5. Determinism classes (C089-19)

Each named surface's class is registered here. A
**deterministic** surface's comparable runs must agree
byte-for-byte in their result blocks; any difference is a
junction by definition. A **named-nondeterministic**
surface's divergence is expected to occur, and the
junction's job is to show the divergence is inside the
registered nondeterminism's shape — or quarantine the pair.

| Surface | Class | Registered nondeterminism shapes |
|---|---|---|
| `settling` | deterministic | — |
| `study` | deterministic (under the freeze record's fixed pins; the freeze-gate C2 recomputation precedent) | — |
| Generated-layer builders (matrix / map / program-map generation) | deterministic under fixed inputs; bound by the generated layers' stamp discipline, not by run records, in v1 | — |
| `suite` | named-nondeterministic | Shape #1 (below) |
| `experiment` | per-graph registration; default named-nondeterministic for LM-bearing graphs; deterministic only by a per-graph registration act recorded with the graph | per-graph |

**Suite shape #1 — the tray teardown flake.** A divergence
between two suite runs is inside this shape iff it is
confined to teardown ERROR entries of the sqlite
closed-database family on tray test ids (first registered
instance: `test_tray_token_auth.py::
test_copy_api_token_without_tkinter_is_named`), with the
runs' pass and fail counts otherwise equal. Any divergence
outside that confinement — a different test, a changed
count, a failure rather than a teardown error — is not
this shape.

## 6. Junction dispositions (vocabulary)

A junction report (Stage 3) ends in exactly one
disposition from this registered vocabulary:

- `explained-by-named-difference` — a named key or
  environment difference, with evidence connecting it to
  the divergence.
- `not-comparable` — a constitutive key component differs;
  the pair is reclassified as different experiments
  (C089-10).
- `identical-after-all` — the reported difference was in a
  presentation of the records, not in the records; the
  report names the presentation artifact.
- `unexplained` — none of the above on the evidence; both
  runs are quarantined (C089-13) pending adjudication.

**The mechanical explained case, registered narrowly.** A
divergence wholly inside a registered nondeterminism shape
for the pair's surface (§5) is
`explained-by-named-difference` by the junction tool
itself, citing the shape and the divergent lines. Every
other explanation is an adjudication act recorded in the
index (§7) — the tool does not originate explanations
beyond the registered shape case (D-089-2).

## 7. The run index (D-089-3, D-089-5)

### 7.1 Form and acts

One index per run store: `run-index.jsonl` in the store's
directory, one JSON act per line, append-only. Relations
change by appended acts, never by editing a record or a
prior act. The acts:

| Act | Fields | Meaning |
|---|---|---|
| `entry` | `run_id`, `record` (store-relative path), `key`, `legacy` (bool); legacy entries add `label` + `key_partial` + `missing` (§7.2) | A run record stands in the store under this id |
| `supersedes` | `run_id` (the new run), `supersedes` (the old run's id), `ref` (the act that ordered the supersession — a stage record, PR, or refresh record) | The new run supersedes the old; the old record remains in the store, addressable under its own id |
| `quarantine` | `junction_id`, `run_ids` | The named junction's disposition is unexplained; the named runs are quarantined |
| `adjudication` | `junction_id`, `ruling`, `actor`, `resulting_state` (`quarantine-lifted` \| `quarantine-confirmed`) | A named actor's ruling on a junction; lifts or confirms its runs' quarantine |

Junction ids are minted like run ids:
`junction-<yyyymmddThhmmssZ>-<6 lowercase hex>` (the
junction tool, Stage 3, is the minter).

**Fold rules.** Folding the acts in file order yields the
store's current state: its entries, its supersession
chains, its open quarantines. A fold refuses, loudly:

- an act naming a run id with no prior `entry` act
  (`supersedes`, `quarantine`), or an adjudication naming
  a junction id no prior `quarantine` act introduced;
- a second `entry` act for one run id (an id is one
  execution);
- a second `supersedes` act over one old id (a record's
  successor is single; chains are linear);
- a malformed act (an unknown act kind, a missing required
  field, an out-of-vocabulary `resulting_state`).

Appending an act validates it against the folded state
first: a refused act is never written, and the index file
is byte-unchanged by the refusal.

### 7.2 Legacy entries (D-089-5)

Pre-spec run records are covered **index-only**: their
bytes are never rewritten, and no id is inserted into them.
Each receives an `entry` act under a **legacy id** derived
from its store path:

```
legacy:<store-relative path, final suffix removed>
```

e.g. the record at `t405-incumbent-over-full-frame--
d9f73e4c4e4e.json` in the settling store stands under
`legacy:t405-incumbent-over-full-frame--d9f73e4c4e4e`.
The derivation is a pure function of the path: stable
across calls, and distinct paths derive distinct ids (a
store whose records collide under the derivation is a
store defect, reported, not worked around).

A legacy entry carries the key components recoverable from
the record itself — for settling records: `surface`
(`settling`), `semantics`, `candidate`, and `input_pins`
(the record's `pins` block verbatim) — plus `legacy: true`,
`key_partial: true`, the list of registered components
that do not exist to recover (`missing`: command,
tool_version, code_version, seed, environment_class, and
the execution stamps), and the label, verbatim:

```
legacy — key partial
```

A legacy run's results may be cited only under that label
(C089-17). The label says the binding is partial,
permanently; it does not say the results are suspect.

### 7.3 The CI citation form

A CI suite run is cited as the quadruple **{GitHub run id,
head SHA, job name, per-job conclusion}** — the
delivery-checker discipline, generalized from merge gates
to any evidence citation (D-089-6). A citation that names
fewer than the four does not bind the run.

## 8. The boundary with the fabricated-delivery protocol

That protocol (owner order, 2026-11-04) governs *presented*
results; these definitions govern *recorded executions*.
A fabricated delivery is not a run, creates no run record,
and enters no junction; a run record certifies what an
execution recorded, never that a presentation of it was
honest. Where a presented result and a run record disagree,
the record governs and the disagreement is a presentation
defect under that protocol, not a junction under these
definitions (C089-20). Junction machinery never ingests
deliveries.

## 9. Amendment

These definitions change only as a new version
(`run-defs v2`, …), propagated to every registered copy —
this document, the library's machine copy, and (from
Stage 5) the gate's V11 copies — in the same motion. The
comparability judgment row (§4) is the owner's, settled at
T003; changing it is an owner act, not an amendment a stage
may make. The library's write entry points are named here
as owed to the gate's writer census when V11 lands
(Stage 5's registration act); they write run stores and
indexes only, never a gated generated artifact.
