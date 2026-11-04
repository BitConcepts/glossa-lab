# Program-map definitions — `program-map-defs v1`

Spec 088 (full-picture program map + gap register), task T101.
This document is the contract the program-map builder runs
under: the inputs, the derivation table, the roll-up
precedence, the find kinds, and the stamp are registered
here, versioned, and are the only ones the builder may use.
A machine copy of every table in this document lives in the
builder (`backend/glossa_lab/program_map_generate.py`); the
Stage 3 gate (V10) will carry its own registered copies, and
a deliberate change to any definition is made in every copy
in the same motion. Acceptance for this document is
human-as-oracle: the owner settled the judgment rows at the
package ratification (T003, D-088-3); the stage reviewer
rules that this document says exactly what T003 approved.
*This does not establish the definitions are the right
semantics — it establishes they are written down, versioned,
and the only ones the builder may use.*

**The honesty split, stated once.** "The map is generated,
never made" holds for the data. The definitions in this
document are human-registered — the same split the matrix
definitions (Spec 086) carry, named there and adopted here.
Every node in the program map arises from exactly one rule
below, applied to the registered inputs; where the record
carries nothing, the map shows the absence and the coverage
block counts it. No standing is read from prose, ever (C2):
a standing that exists only in a spec's narrative, a stage
record, or a report is not an input, and its shortfall is a
find for the gap register (C088-17).

## 1. Inputs — the closed list

The builder reads **only** the following, and nothing else:

| Input | Identity | How it is reached |
|---|---|---|
| The ledger | `glossa-indus/ledger/claims.jsonl` (`ledger-schema v1`) | Directly. Its canonical SHA-256 (the shared helper `glossa_lab.ledger_intake.sha256_file`: UTF-8, CRLF→LF) is computed at build time and carried in the stamp. |
| The taxonomy | `glossa-indus/map/program-map-taxonomy.json` (`program-map-taxonomy v1`) | Directly. Curated grouping only (§8); it carries no standings, by format (§8's forbidden keys). |
| The spec tree | The directory names under `specs/` | Names only. No spec file's contents are read for any purpose (C2). |

Any other file — a stage record, a report, a bundle file —
is not an input, and a build that needs one has left the
definitions. Amendments to this list are new definitions
versions (§12).

## 2. Nodes

One node per ledger **claim** entry, identified by the
entry's canonical id; one node per spec directory,
identified by the directory name (D-088-1). Annotation
entries are not nodes and never affect standings.
Reclassification entries are not nodes; they resolve into
their target claim's governing entry (§3).

## 3. Governing entries — reclassification chains

A claim's **governing entry** is its claim entry with every
reclassification that supersedes it applied in ledger
order: for each field a reclassification carries (`status`,
`stage`), the later entry's value governs. A reclassification
whose `supersedes` does not resolve to a claim entry fails
the build, naming the entry. The ledger today contains zero
reclassification entries, so this rule is registered ahead
of need — the same posture matrix-defs took toward its
empty registers.

## 4. Claim derivation

### 4.1 Membership — the claim's home

A **bundle** claim's home study is the spec directory named
by its **source-of-record** source (the `sources[]` entry
with `role` = `source_of_record`): exactly one such source
exists per bundle claim, and on the current ledger its
`spec` coincides with the first `sources[]` entry carrying
a `spec` for all 853 bundle claims. Sources in other roles
(`bundle_aee`, `evidence_instance`, `promotion`) do **not**
confer membership: 44 bundle claims name further spec
directories in non-representative sources (citations of the
proposition by other studies), and counting those as
membership would let a citing study's class move with a
claim it did not produce. The builder enumerates those 44
in the coverage block (§9) so the default is visible, not
silent. A bundle claim whose source-of-record source names
no spec, or a spec that is not a directory in the tree,
fails the build naming the claim — its citation does not
resolve (C088-6).

An **extracted** claim belongs to no study. Its home is the
source document named by its source-of-record source's
`document_id`, and its grouping is the taxonomy's
extracted-document assignment for that document (§8). A
missing or unassigned document fails the build naming the
claim.

A claim of any other population (e.g. `discovery`) has **no
registered assignment route in v1** and fails the build
naming the claim, until a definitions amendment registers
one. Failing is the design: an unassigned population must
not be silently grouped.

### 4.2 The derivation table (D-088-3, ratified at T003)

Applied to the governing entry's `status`:

| Ledger status | Class | Ground |
|---|---|---|
| `strongly_supported` | `positive` | The record's strongest support standing. |
| `contradicted` | `negative` | The record states the claim is contradicted. |
| `unsupported` | `negative` | The record states the claim is not supported. |
| `partially_falsified` | `negative` | A falsification that landed in part is a negative standing, not a mixed one — v1 has no mixed class. |
| `superseded` | `closed_other` | The claim was replaced by a later act; its standing is closed, not negative. |
| `draft` | `open` | A governance bundle's registered-but-unjudged state. |
| `untested` | `open` | Extracted and not yet taken up by a test. |
| `partially_supported` | `open` | **Registered judgment row**: partial support is not a program judgement of support, and v1 has no "mixed" class. The verbatim status is shown in the standing text (§4.3), so nothing is hidden. |

Any status outside this table fails the build, naming the
entry — the table is total over the observed vocabulary
because the build refuses the unobserved, not because it
guesses at it.

### 4.3 Standing text

A claim node's standing text is a mechanical template over
the governing entry's verbatim fields:

```
Ledger standing: status <status> · stage <stage|none> · falsifier <present|absent>
```

`stage` is the entry's `stage` verbatim, or `none` when the
entry carries none. `falsifier` is `present` when the entry
carries a non-empty falsifier, else `absent`. `aee_state`
plays no part in derivation: it is null for the whole
ledger today, and the defs register no rule that reads it.

## 5. Study roll-up

A study's member classes are the classes of its member
claims (§4.1). The class is the first matching rule:

1. **No members → `unjudged`.** No derivation exists; the
   node shows no standing beyond the fact (C088-5).
2. **Any positive and any negative → judgment call.** The
   displayed class is `open`; the case is emitted as a
   judgment-call find (§6) with its positive/negative member
   counts, and listed in the coverage block. The precedence
   does not resolve mixed evidence into a verdict.
3. **All members `closed_other` → `closed_other`.**
4. **Any negative → `negative`.**
5. **Any positive → `positive`.**
6. **Otherwise → `open`.**

A restricted study (§7) is not rolled up at all.

## 6. Find kinds

The builder emits a machine find list
(`program-map-finds.json`) beside the map. Exactly four
kinds exist in v1:

| Kind | Emitted |
|---|---|
| `bundle_less_study` | Once per unjudged study (§5 rule 1), subject = the spec directory. |
| `judgment_call` | Once per judgment-call study (§5 rule 2), subject = the spec directory, with positive/negative/total member counts. |
| `extracted_null_falsifier` | Once per extracted claim carrying no falsifier, subject = the claim id, with its source document. The 9 of record are enumerated here, by construction. |
| `restricted_node` | Once per restricted study (§7), subject = the spec directory. |

Finds are sorted by (kind, subject). The scans (S5) and the
register (S6) consume this list; nothing else emits finds.

## 7. Restricted studies

A spec directory in the taxonomy's `restricted` list
renders **name-only** in every generated artifact
(C088-19): its study node carries its directory name, its
taxonomy grouping, the restricted flag, and the registered
name-only form below — no class, no standing beyond the
form, and no member counts (member data is derived data,
and the restriction admits none). Its claims still receive
their own claim nodes: the restriction binds the study's
presentation, not the ledger.

| Spec directory | Registered name-only form |
|---|---|
| `072-fish-family-profiles-redesign` | `executed — held under the Roif gate` |

A restricted directory with no registered form in this
table fails the build. Adding a form is a definitions
amendment (§12); adding a directory to the taxonomy's list
is a taxonomy amendment (§8) — both are acts, recorded.

## 8. The taxonomy

`program-map-taxonomy v1` is a curated file: declared
domains, declared subdomains per domain, one assignment
per study directory, one assignment per extracted source
document, and the restricted list. It is grouping only.
**The format carries no standings**: the builder refuses a
taxonomy in which any key named `standing`, `status`,
`class`, `standing_text`, `verdict`, `score`, or `curated`
appears anywhere, at any depth (C088-17) — the absence of
RCPH's curated-standing mechanism is enforced by the
format check, not by convention.

Coverage over the taxonomy is exact and bidirectional:
every spec directory in the tree is assigned exactly once;
an assignment naming no directory, a duplicate assignment,
an undeclared domain, or a subdomain not declared under
its domain each fail the build. Every extracted source
document in the ledger is assigned exactly once, and an
assignment naming a document the ledger does not carry
fails the build. Changing any assignment is a new taxonomy
version, recorded in the stage record in the same motion
(C088-9).

## 9. Coverage block

Every build emits the coverage block, in `program-map.json`:

- claim nodes: total; by population; by class;
- study nodes: total; by class (restricted studies counted
  separately, never under a class); the unjudged study list;
  the judgment-call list;
- per-domain node counts, and per-class counts within each
  domain — per domain only; no output computes a
  cross-domain aggregate progress figure (C088-14);
- falsifier coverage recomputed from the ledger: claims
  carrying a falsifier, of all claim entries, and the
  null-falsifier extracted claim ids;
- the multi-spec claim list (§4.1): bundle claims whose
  `sources[]` name more than one distinct spec directory,
  counted and listed by id, so the membership default's
  population is visible in every build.

## 10. As-of stamp

Every generated artifact carries: the ledger's canonical
SHA-256, the ledger line count, the ledger's own latest
entry date, and the versions in force (`ledger-schema v1`,
`program-map-defs v1`, `program-map-taxonomy v1`). There is
no wall-clock generation time: delete-and-regenerate
byte-identity (C088-13) is the acceptance property, which a
clock stamp would make impossible, and the stamp's purpose
is to name the data the artifact was computed from — the
ledger hash is that name. An artifact whose stamp hash does
not match the current ledger is stale; the gate (S3, V10)
is where that is enforced.

## 11. Class vocabulary

Claim classes: `positive`, `negative`, `open`,
`closed_other`. Study classes: those four plus `unjudged`.
**`in_flight` is registered with no derivation rule in v1**
(D-088-4, C088-18): no record of record in the repository
carries study run-state — job state lives in the live
backend, outside the builder's inputs — and deriving it
from prose is C2-forbidden. A build that emits an
`in_flight` node fails. Running work is visible through
the scans and the register, not the map, until a registered
run-state source exists.

## 12. Amendment discipline

A change to any table or rule in this document is a new
definitions version (`program-map-defs v2`, …), made in
this document and in the builder's machine copy in the same
motion, and recorded in the spec's stage record. Artifacts
generated under an older version are stale by their stamp
(§10) until regenerated. The Stage 3 gate's registered
copies join this discipline when they land.
