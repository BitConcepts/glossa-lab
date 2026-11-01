# Harmonization record — 2026-11-01 (Spec 086, Stage 3 filing)

Dated entries recorded under the harmonization rule
(winning-combination pattern, point 7) during Stage 3.
Records only; no build impact except where a disposition
says so.

## 2026-11-01 — The Atlas adopted Glossa's T105 pattern note

The Breaking-Point Atlas adopted the Stage 1 pattern note
("Pin the ledger's schema and gate it in CI",
`records/pattern-note-ledger-schema-validator.md`) the
same day it was delivered:

- a pinned ledger schema (`schema v1`) landed beside
  their ledger, derived from a census of its 541 entries;
- a SCHEMA check class in their `verify_equivalence.py`
  recomputes proposition fingerprints under their frozen
  rules and enforces one-entry-per-proposition dedupe;
- falsifier coverage — 541/541 — is published on every
  gate run, the falsifier-gap census discipline of the
  companion note in this directory;
- their gate moved 204/205 → 206/207 PASS with **no check
  loosened**; the canonical scenarios reproduce 6/6; four
  seeded failure controls are caught; a jsonschema
  cross-check of the class disagreed on 0 entries; 39
  legacy lines carrying raw UTF-8 bytes were recorded,
  not repaired.

Their record:
`~/workspace/breaking-point-atlas/scenarios/PATTERN-NOTE-ADOPTION-2026-11-01-da-schema-validator.md`.

## 2026-11-01 — Amendment 3 ratified: the T105 note enters the canonical pattern

Tristen ratified the T105 pattern note on 2026-11-01 as
**Amendment 3** to the canonical winning-combination
pattern note — "Pin the ledger's schema and gate it in
CI" — canonical note commit `4e1ff09`, with Glossa's
Stage 1 evidence cited in the amendment's record (relayed
from the RCPH chat, the framework's home). The naming
question Stage 1's filing left open — whether D-A's
pinned-schema + CI validator pattern generalizes under
that name — is therefore **decided**: the generalized
naming is canonical. Spec 086's own documents continue to
label the move an extension of D-A as ratified (the
decision's literal subject was the anchors file); the
amendment adopts the generalization at framework level,
which is the naming authority.

## 2026-11-01 — RCPH recorded its own adoption

RCPH (projected-constraints, the framework's home)
recorded its adoption of the same note the same day, with
its starting position stated plainly: its program ledger
holds 44 entries in 3 field shapes, carries no falsifier
field, has no pinned schema, and its CI validates parse
only. A schema + validator build is queued there. The
three framework projects now stand at three recorded
points on the same discipline — Glossa built, Atlas
adopted same-day, RCPH recorded with its gap published —
which is the harmonization rule working as designed: the
gap is in the record, not papered over.

## 2026-11-01 — Amendment 2 ratified: canonicalize before you hash

Amendment 2 to the canonical pattern note
(canonicalize-before-you-hash, proposed by Spec-Kit AEE)
was ratified by Tristen on 2026-11-01 and recorded in the
canonical note, commit `d1de85d`. (Amendment numbering
follows proposal order: Amendment 2 sits between
Amendment 1 — relation-carrying citations — and
Amendment 3 above.)

**Glossa's conformance, as adopted 2026-11-01 and
unchanged by the ratification:**

- the shared canonical helper
  (`glossa_lab.ledger_intake.sha256_file`: UTF-8 decode,
  CRLF→LF, then SHA-256) has been the only hash the
  ledger records since Stage 1, and Stage 3's V1
  recorded-source-hash arm verifies all 1,686 recorded
  hashes under it on every gate run;
- generated artifacts are written with pinned LF bytes
  and verified by byte-comparison (Stage 2) and by the
  gate's V7 regeneration check (Stage 3);
- the repo root `.gitattributes` already carried `eol=lf`
  before the amendment;
- the amendment's write-freedom corollary — the checker
  must not mutate what it checks (bytecode writing
  disabled; proven by hashing the published tree before
  and after a red run) — is implemented by this stage's
  gate and its tests: the CLI sets
  `sys.dont_write_bytecode` before importing the backend,
  the CI job sets `PYTHONDONTWRITEBYTECODE`, and the
  write-freedom proof is filed at
  `records/stage-3-negative-control.txt`.

**Standing scoping:** the framework026 freeze regime's
raw-byte pins are **not** migrated to the canonical
recipe. They are a different historical regime whose pins
verify on both platforms under the attributes regime —
recorded at adoption, and no conflict with the ratified
amendment arises: the amendment governs the ledger and
its generated layers.

## 2026-11-01 — Framework ruling: duplicate propositions are layer-scoped

A framework ruling landed 2026-11-01 from the RCPH chat,
recorded in the canonical pattern note, commit `3bcd1fd`:
**duplicate propositions are layer-scoped.** In a *claim*
ledger (one entry per proposition), duplicates are
**refused at intake** per D-B as written. In an
*assertion/evidence* ledger, duplicates are **counted**
in the published census, grouped by recomputed
fingerprint — never refused and never silently kept. A
project **declares its ledger type in its schema
document**. Neither branch permits a duplicate to pass
uncounted.

**Glossa's dispositions (each verified at recording):**

1. Our ledger is a claim ledger. D-B refusal is already
   the Stage 1 validator's behavior — a duplicate
   fingerprint is an intake/validation error naming both
   records, and the refusal is teeth-tested in
   `backend/tests/test_spec086_ledger_intake.py`. Branch
   (1) therefore leaves Glossa's discipline **unchanged**.
2. `glossa-indus/ledger/SCHEMA.md` already declared the
   substance ("A canonical claim entry — one per
   proposition (D-B)") but not in the ruling's explicit
   declared-type form. This stage adds the explicit
   declaration at the head of SCHEMA.md: *this ledger is a
   claim ledger under the 2026-11-01 layer-scoped ruling;
   duplicates are refused at intake per D-B.* SCHEMA.md
   is the human document, not the pinned
   `ledger-schema.json`; it was verified before editing
   that no hash pin and no test covers SCHEMA.md's bytes
   (its only references elsewhere are prose, in spec.md
   and the stage records).
3. Glossa operates **no assertion/evidence ledger** in
   v1, so branch (2) has no Glossa surface: research-check
   sidecars enter as annotation entries in the claim
   ledger, and evidence instances are `sources[]` records
   of a claim entry, preserved per D-B.
