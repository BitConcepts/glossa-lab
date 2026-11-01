# Claims — Spec 086 (C086-1 … C086-21)

Every claim carries at least one falsifier executable against the
built system. The build phase normalizes this list into the spec
bundle's `aee-claims.json` in the repo's established format and
validates it under the pinned AEE (1.5.3) before any build task
starts (tasks.md T002). Claims C086-9, C086-11, and C086-12/C086-13
carry the mechanics adopted from the Breaking-Point Atlas pattern
note `PATTERN-NOTE-2026-11-01-gate-and-settle` under the
harmonization rule (see README.md).

---

**C086-1 — The ledger is the sole entry point downstream.**
Every element of the generated matrix and the map traces to a
ledger entry id, and no matrix cell or map element exists whose
content came from anywhere else.
*Falsifier:* a matrix cell or map element with no ledger id path,
or whose content matches a non-ledger source (a sidecar file, a
database row, a bundle) that no ledger entry mirrors.

**C086-2 — Intake is schema-pinned and validated.**
Every line of `glossa-indus/ledger/claims.jsonl` validates against
the pinned ledger schema (`ledger-schema v1`), and the Stage 1
validator, run in CI, rejects a malformed, extra-field, or
missing-field entry.
*Falsifier:* a ledger line that fails schema validation while the
validator passes it; or a seeded malformed entry the validator
accepts in the Stage 1 teeth test.

**C086-3 — D-B dedupe is enforced at intake, not by memory.**
Every canonical entry's `proposition_fingerprint` recomputes to
its stored value under the frozen rules (`spec029-phase-i-v1`),
no two canonical entries share a fingerprint, and an intake
attempt whose fingerprint collides with an existing proposition
is refused, naming both records, writing nothing.
*Falsifier:* two canonical entries with one fingerprint; an entry
whose stored fingerprint differs from recomputation; or a seeded
duplicate intake that is written.

**C086-4 — Corrections are append-only reclassifications.**
A superseded claim is marked by an appended reclassification entry
with a `supersedes` pointer; no existing ledger line is ever
edited in place.
*Falsifier:* git history showing a modified (rather than appended)
ledger line for an existing id, outside a D-E migration record
that itself reconciles.

**C086-5 — No field is fabricated at migration or intake.**
A migrated or intaken entry carries a `falsifier` or a
`does_not_establish` line only where its source record carries one
or a named human-authored record supplies one; where neither
exists the field is null, and every gate run publishes the
falsifier-coverage count of the ledger.
*Falsifier:* an entry whose falsifier or does-not-establish text
appears in no source record and no human-authored record; or a
gate run that omits the coverage count.

**C086-6 — OD-2 authorship is preserved.**
No ledger entry carries explanation content
(`explanation_record`, or a `does_not_establish` line sourced from
one) unless it names a human author whose adoption act exists in a
durable record; the intake validator rejects explanation content
without one.
*Falsifier:* an entry with explanation content whose named author
has no adoption record, or whose author is not a named human; or a
seeded authorless explanation the validator accepts.

**C086-7 — The matrix is generated, never made.**
`glossa-indus/matrix/matrix.json` and `matrix.md` are produced
solely by the registered generator from the ledger; deleting them
and regenerating from an unchanged ledger reproduces them
byte-for-byte.
*Falsifier:* a regeneration diff over an unchanged ledger; or
matrix content present that the generator, run on the same
ledger, does not produce.

**C086-8 — Every matrix cell is traceable to its derivation.**
Every non-empty cell names its relation, its citation ids, and
the registered derivation rule (matrix-defs version) that
produced it, and inspecting the cited ledger entries exhibits
that rule's stored relation.
*Falsifier:* a sampled non-empty cell with no rule id, or whose
cited entries do not carry the stored relation its rule requires.

**C086-9 — Citations carry their relations (adopted, Atlas note
2026-11-01).**
For every citation on every non-empty matrix cell and every map
edge, at least one registered tie mechanically holds (spec.md
Point 4: T1 source membership, T2 dated test with matching
outcome direction, T3 registered anchor, T4 registered
instrument). Existence, shared documents, shared signs without a
T3 anchor record, and topical relevance are not ties.
*Falsifier:* a seeded Atlas-style miscarriage — a citation that
exists and is relevant but satisfies no tie rule (e.g., citing
Spec 054's UNEXECUTED closure as support for the Yadav claim) —
that the gate passes; or any production cell/edge citation the
gate's V4 check cannot tie.

**C086-10 — The verification gate guards the chain in CI.**
A CI job beside C4 (`ledger-gate`) recomputes the matrix and the
map from the ledger on every PR and push, running check classes
V1–V9 (spec.md Point 4), and a divergence in any class fails the
job.
*Falsifier:* a seeded divergence in any one class (a flipped
ledger status not reflected in the matrix; a count mismatch; a
hand-edited generated artifact) that merges with the job green.

**C086-11 — Publication is gated (adopted, Atlas note
2026-11-01).**
Generated artifacts are published only through candidate → gate →
replace: the builder writes a candidate, the gate runs against
the candidate, and the published file is replaced only on ALL
PASS; on a red gate the previously published artifact is
byte-untouched and the build fails.
*Falsifier:* a negative-control run (seeded divergence) after
which the published artifact differs by even one byte from its
pre-run hash, or after which the build reports success.

**C086-12 — Lossless regeneration is a checked mode (adopted,
Atlas note 2026-11-01).**
The gate's `--regen` mode hashes the matrix and map artifacts,
regenerates both from the ledger, and byte-compares; any diff is
classified in the run record as exactly the intended change
(named) or a downstream defect (fixed by regeneration, never by
editing the artifact).
*Falsifier:* a `--regen` run whose byte diff goes unreported, or
a downstream defect closed by hand-editing a generated artifact
anywhere in the repo's history after this spec lands.

**C086-13 — Settling is derive-before-build (adopted, Atlas note
2026-11-01).**
The settling semantics (`glossa-settle-1`) and the hand-derived
canonical scenarios (with prose derivations) are registered in
git **before** the settling engine module exists, and the
engine's test requires exact reproduction of every canonical —
counts, enumerations, and tallies equal.
*Falsifier:* commit order showing the engine predating the
semantics/canonical registration; or a canonical scenario whose
engine output differs from the registered expectation in any
field, with the test green.

**C086-14 — Settling is mechanical, labeled, and read-only
against the ledger.**
Every reported settling result comes from a stored run record
(inputs incl. ledger build hash, rule version, per-rule outcomes,
enumerations, coverage); every output surface carries the
computation label (spec.md Point 3); and the settling package has
no write path to the ledger (no intake/write module import —
gate check V9).
*Falsifier:* a reported settling number with no run record; an
output surface missing the label; or a settling module importing
a ledger write path, found by the V9 audit or by inspection.

**C086-15 — Interchangeability discipline for dual readings.**
A dual-reading comparison records the same ledger build hash and
the same corpus snapshot hash for both runs, and emits a
per-claim divergence list (both bearing tallies shown per claim),
naming any pre-registered expectation for a touched claim and
reporting agreement or divergence against it.
*Falsifier:* a comparison report whose two run records carry
different input hashes; a comparison that narrates divergence
without the per-claim list; or a touched claim with a
pre-registered expectation the report neither names nor scores
against.

**C086-16 — Settling moves nothing.**
A settling run creates only run records: no ledger entry, claim
status, stage, score, anchor assignment, or store-of-record
content changes as a result of a run; displayed scores are
`aee/scoring.py` outputs over the ledger's relation set, never a
parallel computation.
*Falsifier:* a store diff attributable to a settling run; or a
displayed score differing from an independent ScoringEngine
execution over the same relation set.

**C086-17 — The map renders the generated data exactly.**
For any view and filter selection, the map's rendered counts and
elements equal the gated map artifact's contents for the same
selection, and its header state (claims by status,
validated-anchor share, nearest dated items) equals the gate's
recomputed values for the ledger build the artifact names.
*Falsifier:* a rendered count, element, or header value differing
from the artifact/gate values for the same selection and build,
found by Playwright + artifact comparison (Spec 081/083
verification precedent).

**C086-18 — Generated artifacts carry as-of stamps (D-D
generalized).**
Every generated artifact (matrix, map data, settling run records,
any report citing claims) carries its generation time, the ledger
content hash it was computed from, and the definition/rule
versions in force; a surface showing an artifact whose stamp hash
does not match the current ledger marks it stale.
*Falsifier:* a generated artifact with no stamp, or a stale
artifact displayed without its stale marking.

**C086-19 — The chain never widens visibility (Spec 083).**
A workspace-scoped map response contains no element whose source
record is out of scope for the requester, and no relation
incident to an absent element. (Scope is whatever the source
record's scoping is under Spec 083, as in C085-13.)
*Falsifier:* an out-of-scope record's element present in a scoped
response, or a relation pointing at an element the response
omits.

**C086-20 — Scoping: this adoption changes no verdict.**
This adoption changes no decipherment verdict, no claim's status
or stage, no score, and the program's standing position; the
migration reconciliation (per-population, before/after per claim
id) is the evidence, and the Indus script remains not deciphered.
*Falsifier:* a claim whose status, stage, or verdict differs
between its source of record before migration and its ledger
mirror after, other than by a pre-existing adjudication act the
reconciliation names.

**C086-21 — Harmonization is exercised, not just cited.**
Improvements found during this build (at minimum the two named
in spec.md Point 7) are written as short pattern notes and
delivered to the RCPH and Breaking-Point Atlas chats; incoming
pattern notes are adopted with a recorded adoption act or
surfaced to the owner as conflicts — never silently absorbed or
silently dropped.
*Falsifier:* a stage closeout recording a pattern improvement
with no delivered note in the delivery record; or an incoming
note (beginning with `PATTERN-NOTE-2026-11-01-gate-and-settle`,
whose adoption README.md records) with no adoption record in
this spec's repo record.
