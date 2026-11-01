# Plan — Spec 086 Winning-Combination Adoption (Stages 0–1)

**Date**: 2026-11-01
**Branch**: `spec/086-stage0-1-ledger-intake`
**Proposal basis**: the owner's adoption order of 2026-11-01
(relayed from the RCPH chat) and his block approval of the
Spec 086 package the same day (06:40 EST, Glossa-Lab chat:
"Approve the Spec 086 package as a block"). In this repo's
governance terms the approved package is the proposal (H2);
its §8 decision items stand as recommended, and its §9
non-goals carry the epistemic boundaries (H13): no verdict,
status, stage, or score changes; migration reads — never
edits — the existing stores and every frozen tree.

## Stage 0 — adoption record

1. **Package adopted into the repo** (T001):
   `spec.md`, `claims.md`, `tasks.md` are the approved package
   texts (goal workspace
   `files/2026-11-01-spec086-package/`), with the approval act
   recorded at the head of `spec.md`.
2. **Claims normalized** (T002): `aee-claims.json` carries
   C086-1…21, statement and falsifier text normalized from
   `claims.md` without substantive change. Pinned AEE 1.5.3
   verification, run 2026-11-01:
   - `aee validate` → `valid: 21 claim(s) in specs/086-winning-combination-adoption/aee-claims.json`
   - `aee assess --no-ledger` → outcome `iterate`; summary:
     "Assessed 21 claim(s); found 91 failure mode(s); 21
     claim(s) below the 0.70 confidence threshold." (Draft
     claims with a single shared asserted evidence source —
     the expected well-formedness result; full output in
     `records/t002-aee-assessment.json`.)
3. **Amendment 1 to the canonical pattern** (ratified by the
   owner 2026-11-01, relayed from the RCPH chat) is recorded
   at the head of `spec.md`: the named failure mode "a
   citation can exist, be relevant, and still not carry the
   relation" and its five corollaries are already carried by
   this package as approved (C086-9, Stage 3 check V4,
   C086-11). Adoption confirmatory; no plan change; no
   conflict with a ratified local decision.
4. **LEDGER.md entry** (T003) records the adoption, including
   the harmonization adoption record for
   `PATTERN-NOTE-2026-11-01-gate-and-settle`.
5. **Harmonization adoption 2** (2026-11-01):
   "Canonicalize before you hash" (Spec-Kit AEE chat) adopted
   with the scoping recorded at the head of `spec.md` —
   checkout pinning already in force (`.gitattributes`,
   verified); canonical-form hashing for this spec's
   generated layers via the one shared helper in
   `ledger_intake.py` (Stage 1's recorded source hashes were
   switched to it before this PR pushed); the freeze
   regime's raw-byte pins expressly NOT migrated; the
   gate-write-freedom corollary recorded as a Stage 3 design
   requirement in `stage-1-record.md`.
6. **Harmonization adoption 3** (2026-11-01): six findings
   from the MPCodec adoption (their spec 031), recorded at
   the head of `spec.md` with dispositions — measurements as
   first-class entries adopted for Stage 2 (fits
   ledger-schema v1 as an added kind, claim shape untouched);
   V4 numeric arm and gate-never-mutates (pure builder + thin
   write wrapper) as binding inputs for Stages 2–3; layers
   distinction and counter-decomposition-before-not-checkable
   as binding inputs for Stage 4; and item 6 (narrative
   confidence is not a number) BINDING NOW — applied in
   Stage 1 via the `confidence_in_source`/`confidence_text`
   field pair, with the full-population audit in
   `stage-1-record.md` and the reconciliation reports.

## Stage 1 — ledger intake validator

1. **Ledger home + pinned schema** (T101):
   `glossa-indus/ledger/` with `SCHEMA.md`,
   `ledger-schema.json` (`ledger-schema v1`), and
   `claims.jsonl` built by the migration (step 3).
2. **Validator + intake module** (T102):
   `backend/glossa_lab/ledger_intake.py` +
   `tools/ledger/validate_ledger.py` — schema validation,
   D-B fingerprint recomputation and duplicate refusal under
   the frozen `spec029-phase-i-v1` rules, field-provenance
   checks (C086-5, C086-6), falsifier required for new claim
   entries (prospective rule, decision D-086-Q6), append via
   temp + fsync + atomic rename + read-back hash.
3. **Intake routes** (T103): extraction intake (extracted-claim
   record → ledger append as the route's final step), bundle
   import tool (`tools/ledger/import_bundle.py`, for
   freeze/adjudication events), research-check annotation
   intake (sidecars stay advisory; annotation entries only),
   discovery promotion (named human act; candidate entries).
4. **Migrations** (T104), one gated run per population, via
   `tools/ledger/migrate_ledger.py`: P1 extracted claims
   (31 source records), P3 research-check annotations (31),
   P2 spec bundles (census re-derived on this checkout:
   52 `claims.json` files / 777 records + 57 `aee-claims.json`
   files / 826 records = 1,603 pre-existing source records,
   plus this spec's own Stage 0 bundle, 21 claims, migrated
   with the rest for 1,624 total). D-B grouping:
   one canonical entry per proposition fingerprint; every
   other source record of the proposition is preserved as a
   source (evidence instance) of the canonical entry and is
   listed in the reconciliation report. Reconciliation reports
   and the validator's output over the built ledger are filed
   verbatim in `stage-1-record.md` + `records/`.
5. **Tests**: `backend/tests/test_spec086_ledger_intake.py`
   (validator teeth + the four routes) and
   `backend/tests/test_spec086_ledger_migration.py`
   (reconciliation invariants over the built ledger), in the
   Backend tests CI job.

## Verification

- New tests + the Spec 029 Phase I fingerprint family + Spec
  084 conformance pass locally in the CI-faithful venv before
  push; a full backend suite run without `-x` enumerates zero
  failures.
- The migration is read-only against every source store: the
  PR diff contains no modification to any existing claim file,
  bundle, sidecar, or frozen record.
- Census delta vs the package: the package's audit counted
  56 `aee-claims.json` files / 1,592 P2 records from a Spec
  083 worktree; this fresh main checkout carries 57 files /
  1,603 pre-existing records (Spec 084's bundle is the
  additional file), and the migration census of 1,624 adds
  this spec's own 21-claim bundle. The Stage 1
  reconciliation reports are authoritative. One package
  premise is corrected by the build: P1's falsifier gap is
  real but smaller than stated — the store carries the
  content as `falsification_condition` on 15 of 31 records
  (14 of 23 canonical entries); the null gap is 9 entries.
