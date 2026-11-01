# Ledger schema — `ledger-schema v1`

Spec 086 (winning-combination adoption), Point 1. The ledger is
`claims.jsonl` in this directory: one JSON object per line,
append-only. Git is the ledger's WORM layer — a correction is a
new line (a reclassification entry), never an edit to an old
line. The machine schema pinned beside this document is
`ledger-schema.json` (its `$id` is the version string
`ledger-schema v1`); the Stage 1 validator
(`tools/ledger/validate_ledger.py`, module
`backend/glossa_lab/ledger_intake.py`) enforces it, extending
the pinned-schema + CI validator pattern of Spec 029 decision
D-A (whose literal subject was the anchors file) to the ledger
— an extension, labeled as such in the spec (Point 7).

**Ledger type (declared).** This ledger is a **claim ledger**
under the framework ruling of 2026-11-01 (duplicate
propositions are layer-scoped; canonical winning-combination
pattern note, commit `3bcd1fd`): one entry per proposition,
and a duplicate proposition is **refused at intake** per D-B
— never counted-and-kept. Glossa operates no
assertion/evidence ledger in v1: research-check sidecars
enter as annotation entries in this ledger, and evidence
instances are `sources[]` records of a claim entry,
preserved per D-B.

## Entry kinds

Every entry carries `id`, `kind`, `date` (the entry's
intake/migration date). Three kinds exist in v1:

### `claim`

A canonical claim entry — one per proposition (D-B). Fields:

| Field | Meaning |
|---|---|
| `population` | `extracted` (P1 literature claims), `bundle` (P2 spec governance bundles), or `discovery` (human-promoted candidates) |
| `statement` | The atomic proposition text, verbatim from the representative source record |
| `proposition_fingerprint` | SHA-256 over the normalized statement under the frozen `spec029-phase-i-v1` rules, recomputed at intake, never copied on trust |
| `sources` | Every source record of this proposition: `{path, sha256, role, spec, claim_id, document_id}`. `role` is `source_of_record` (the representative record's own file: for P1 its extracted-claims file; for P2 the representative pair's `claims.json` where it exists, else its `aee-claims.json`), `bundle_aee` (the representative pair's other serialization), `evidence_instance` (any further record of the same proposition, preserved per D-B), or `promotion` (a discovery item promoted by a named human) |
| `as_of` | The source record's own as-of where it carries one (P1 `stage_as_of`); else `null` |
| `status` | The status **as held in the source of record**, mirrored, never re-adjudicated by intake. Discovery candidates carry `candidate` |
| `stage` / `stage_source` | The Spec 029 stage where computed, with its provenance (D-E: a cache with provenance, never an assertion); `null` where not computed |
| `aee_state` | `{direct, propagated, band}` where the record carries AEE scoring; `null` where not scored — a null is shown as null |
| `confidence_in_source` | The source record's own confidence when it is a NUMBER, carried verbatim; else `null` |
| `confidence_text` | The source record's confidence when it is QUALITATIVE text, carried VERBATIM; else `null`. Narrative confidence is not a number (harmonization adoption #3 item 6, binding): a text confidence is never normalized into `confidence_in_source`, and a numeric confidence is never rendered as text. Both null = the source carries no confidence |
| `falsifier` | The falsification test text(s) from the entry's source records (ordered union over the proposition's records, each string traceable to a named source), or `null` where no source record carries one. The null is a counted gap, never filled by invention (D-086-Q6) |
| `does_not_establish` | The representative record's own line (P1 `not_understood`; P2 `boundary`); `null` where it carries none |
| `evidence_refs` | Identifiers the source record names: evidence-instance claim ids, source document ids, evidence `ref`s, `depends_on` ids. Identifiers only — free-text fields (e.g. P1 `contradicting_evidence` strings) are not identifiers and are not carried here |
| `sign_refs` | Frame-qualified sign identifiers from identifier-bearing fields only (P1 `sign_ids`, rendered `system:value`). Free-text sign mentions are never resolved into refs; they are counted as unresolved in the migration reconciliation |
| `author` / `author_kind` / `explanation_record` | Present only where the entry carries explanation content (OD-2): a named human author whose adoption act exists in a durable record. Mechanically imported entries without one carry `null` and stand at their computed stage |
| `migration` | `{run_id, migrated_at}` for entries created by a D-E migration run; `null` for entries intaken after Stage 1 |

**Prospective rule (D-086-Q6):** a claim entry with
`migration: null` (i.e. any new intake after Stage 1) must
carry a non-null `falsifier`. Migrated entries may carry
`falsifier: null`; the validator publishes the coverage count
on every run.

**Hash recipe (canonical, pinned).** Every `sha256` recorded
in this ledger over a source file is the SHA-256 of the
file's **canonical form** — UTF-8 decoded, CRLF normalized
to LF — computed by the one shared helper
(`glossa_lab.ledger_intake.sha256_file`), never of the raw
bytes (harmonization adoption 2026-11-01, "Canonicalize
before you hash"). This ledger file itself is written with
pinned LF newlines. The existing freeze regime's raw-byte
pins (framework026 `verify_freeze`) are a separate historical
regime, untouched by this adoption.

### `reclassification`

An append-only correction: `supersedes` names the entry it
reclassifies, `reason` states the act, and the entry carries
the fields it moves (e.g. `status`, `stage`). The superseded
line is never edited.

### `annotation`

A research-check annotation (intake route 3). The Spec 025
contract stands: the sidecar stays advisory and never modifies
a claim. Fields: `target_claim_id` (the claim id the sidecar
bears on, verbatim from the sidecar), `canonical_claim_id`
(the ledger's canonical entry for that claim, resolved through
the store's `merged_into` pointers; equal to
`target_claim_id` when already canonical), `sidecar`
(`{path, sha256}` of the sidecar file), and `bearing` — the
bearing the sidecar's own record states: `advisory: true`,
its `stage`, `verdict`, `checked_at`, `protocol`,
`sources_requested`, `neighbors_surfaced` (count of its
`neighbors`), and `gaps` (count of its `gaps`). An annotation
changes no status, stage, or score.

## Amendment — 2026-11-01 (Spec 086 Stage 2): the `measurement` kind

Adoption 3, item 1 (MPCodec's findings, adopted 2026-11-01)
assessed at Stage 1 that a `measurement` kind fits this
schema as an addition without altering the pinned
claim-entry shape, and assigned its implementation to
Stage 2. It is implemented here, additively:

- the `kind` enum gains `measurement` (the three existing
  values and every existing kind's required shape are
  byte-unchanged);
- a fourth per-kind branch requires, for `measurement`
  entries: `subject` (what is measured — an entry id, a
  sign pair, a named population), `statistic` (the named
  statistic), `value` (a number), `unit`, `direction`,
  `condition_class` (the conditions the value holds
  under), and `artifact` (`{path, sha256}` — the artifact
  the value was read from);
- the validator gains the kind's provenance check: the
  recorded `artifact.sha256` must verify against the
  artifact on disk under the canonical-hash recipe above
  (a measurement traces to its artifact or it does not
  enter — the C086-5 discipline, applied to this kind).

**Versioning reading, recorded because the schema pins no
explicit rule for kind additions.** The ambiguity: adding a
kind changes what the schema accepts, which could be read
as requiring a new version string. The conservative
reading taken here: the pinned substance of `ledger-schema
v1` is the per-kind entry shapes, above all the claim
shape; an *additive* kind branch alters no existing shape,
and the Stage 1 assessment framed the addition as within
v1's kind-discrimination design — so the `$id` stays
`ledger-schema v1`. A future change that alters an
existing kind's shape, or removes a kind, would require a
new version. If the owner rules otherwise, the correction
is a version bump recorded the same way.

**No measurement entries exist yet.** Stage 2 mints none:
minting is an intake act with its own reconciliation, the
matrix generator never writes the ledger (spec 086 Point
6, one-way flow), and no pre-existing measured source
artifact is in Stage 2's migration scope. The measured
evidence that arises in Stage 2's registers (the sign×sign
block's weights and frequencies) is carried in the matrix
artifact with full provenance (`glossa-indus/matrix/
DEFINITIONS.md` §11). The kind stands ready for the intake
that mints from a named source.

## Invariants the validator enforces

1. Every line validates against `ledger-schema.json`.
2. Every claim entry's fingerprint recomputes to its stored
   value under `spec029-phase-i-v1`; no two claim entries
   share a fingerprint (D-B).
3. Every falsifier string and every `does_not_establish` line
   traces to a source record named in the entry's `sources`
   (C086-5).
4. Explanation content appears only with a named human author
   (C086-6, OD-2).
5. New (non-migration) claim entries carry a falsifier.
6. Annotation targets and reclassification `supersedes`
   pointers resolve to ledger entries.
7. Every run publishes the falsifier-coverage count.
8. A `measurement` entry's recorded artifact hash verifies
   against the artifact on disk (Stage 2 amendment, above).
