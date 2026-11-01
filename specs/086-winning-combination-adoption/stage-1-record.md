# Stage 1 record — Spec 086 ledger intake validator

**Date:** 2026-11-01. **Branch:** `spec/086-stage0-1-ledger-intake`.
**Scope:** tasks.md Stage 0 (T001–T003, in this same PR) and
Stage 1 (T101–T105). Build order per the owner's adoption
order: the validator and the ledger come first; the matrix
generator is Stage 2 and does not exist yet.

## What was built

- **Stage 0 (T001–T003):** the approved package adopted at
  `specs/086-winning-combination-adoption/` (spec.md with the
  2026-11-01 block-approval act and the Amendment 1
  confirmatory record at its head; claims.md verbatim;
  tasks.md; plan.md). Claims normalized into `aee-claims.json`
  (C086-1…21) and verified under the pinned AEE 1.5.3:
  `aee validate` → `valid: 21 claim(s)`; `aee assess
  --no-ledger` → outcome `iterate`, "Assessed 21 claim(s);
  found 91 failure mode(s); 21 claim(s) below the 0.70
  confidence threshold" (draft claims, one shared asserted
  evidence source — the expected well-formedness result; full
  output in `records/t002-aee-assessment.json`). LEDGER.md
  entry records the adoption, including the harmonization
  record for `PATTERN-NOTE-2026-11-01-gate-and-settle`.
- **Ledger home + pinned schema (T101):**
  `glossa-indus/ledger/` — `SCHEMA.md`,
  `ledger-schema.json` (`ledger-schema v1`), `claims.jsonl`.
- **Validator + intake (T102):**
  `backend/glossa_lab/ledger_intake.py` +
  `tools/ledger/validate_ledger.py` — pinned-schema
  validation; D-B fingerprint recomputation and duplicate
  refusal under the frozen `spec029-phase-i-v1` rules;
  field-provenance checks (C086-5, C086-6); the prospective
  falsifier rule (D-086-Q6); appends via temp + fsync +
  atomic rename + read-back hash, prefix-preserving
  (append-only, C086-4).
- **Intake routes (T103):** the four doors exist as the
  intake module's builders + `append_entry`, and each is
  exercised by a fixture test: extraction intake
  (`entry_from_extracted_record`), bundle import
  (`tools/ledger/import_bundle.py`, for freeze/adjudication
  events), research-check annotation intake
  (`annotation_from_sidecar` — sidecars stay advisory;
  annotation entries only), discovery promotion
  (`discovery_candidate` — named human + falsifier required).
  Named honestly: the historical extraction writers are
  one-off scripts, not a standing service, so route 1 is the
  door the next extraction run must use (and the door the
  migration used), not a hook inside a live pipeline.
- **Migrations (T104):** `tools/ledger/migrate_ledger.py`,
  one gated run per population — P1, then P3, then P2 —
  read-only against every source store. Reconciliation
  reports: `records/reconciliation-p1.md`,
  `records/reconciliation-p3.md`,
  `records/reconciliation-p2.md`.
- **Tests:** `backend/tests/test_spec086_ledger_intake.py`
  (validator teeth: malformed / duplicate-fingerprint /
  authorless-explanation / untraced-falsifier /
  falsifier-less-new-claim refusals, nothing written; the
  four routes; append-only prefix preservation) and
  `backend/tests/test_spec086_ledger_migration.py`
  (independent census + mirror recomputation against the
  built ledger).

## Gate output — validator over the built ledger (verbatim)

Filed at `records/stage-1-validator-output.txt`; reproduced
here verbatim as the stage report requires:

```text
Ledger validation — /home/hatch/workspace/glossa-run/spec086-stage1/glossa-indus/ledger/claims.jsonl
schema: ledger-schema v1 (glossa-indus/ledger/ledger-schema.json)
fingerprint rules: spec029-phase-i-v1
lines: 871
entries by kind: annotation 31, claim 840
claims by population: bundle 817, extracted 23
falsifier coverage: 831 of 840 claim entries carry a falsifier
falsifier coverage by population: bundle 817/817, extracted 14/23
does_not_establish coverage: 755 of 840 claim entries
aee_state present: 0 of 840 claim entries
errors: none
RESULT: PASS
```

Ledger file: 871 lines, SHA-256
`c4e2326ec8757bb700dac0142dd0adf17d7464b4d929f5b103868c9228f13ccf`
(the file is LF-pinned: its raw and canonical hashes
coincide. This is the rebuilt ledger — canonical source
hashes plus the adoption #3 confidence fields; the first
build's hash, `b1872456…`, is superseded and was never
published. The canonical rebuild's hash, `30eb6235…`, was
itself superseded before publication by the post-#477
provenance re-trace recorded in the correction section
below; the validator output above is unchanged by that
correction, as no count moved).

## Reconciliation headlines (full reports in `records/`)

- **P1 (extracted claims):** 31 source records in → 23
  canonical entries out; 8 merged evidence instances
  preserved as sources under D-B (the store's own
  `merged_into` pointers, each verified to name its group's
  canonical). Falsifier: 14 of 23 entries (the store's field
  is `falsification_condition`, carried on 15 of 31 records —
  see the correction below); does-not-establish 23 of 23 by
  canonical record; AEE state 0 (records carry no scores);
  6 records carry free-text `signs_involved`, counted as
  unresolved mentions, never resolved into `sign_refs`.
- **P3 (research checks):** 31 sidecars in → 31 annotation
  entries out; every target resolves to a P1 canonical
  entry; no claim field changed by any annotation.
- **P2 (spec bundles):** 1,624 source records in (777 in 52
  `claims.json` files + 847 in 58 `aee-claims.json` files;
  862 distinct (spec, claim) pairs, 762 in both
  serializations with text/status verified identical) → 817
  canonical entries out; 45 (spec, claim) pairs merged into
  another pair's entry across 44 cross-spec fingerprint
  groups (each preserved as an evidence instance and listed
  in the report); falsifier 817 of 817 (ordered union over
  each group's records — 26 groups carry differing test
  sets); boundary variants in 40 groups remain in their
  source bundles, the entry carrying the representative's
  line. Census delta vs the package audit (1,592): +11 is
  Spec 084's bundle (landed after the audit's worktree
  base); the remaining +21 is this spec's own Stage 0
  bundle, migrated with the rest — no silent exceptions.

## Harmonization adoption 2 — "Canonicalize before you hash"

Adopted 2026-11-01 (note from the Spec-Kit AEE chat) with the
scoping recorded at the head of `spec.md`. The one scoping
item that touches Stage 1 code: the migration's first build
recorded **raw-byte** SHA-256 hashes over source files. Those
call sites were switched, before this PR pushed, to the one
shared canonical-hash helper
(`glossa_lab.ledger_intake.sha256_file`: UTF-8, CRLF→LF
normalized), and the ledger was rebuilt with it — the
validator output and ledger hash cited in this record are
from the rebuilt, canonical-hash ledger. A checkout-invariance
test (LF vs CRLF bytes of one source hash identically) is in
`test_spec086_ledger_intake.py`. The freeze regime's raw-byte
pins are expressly not migrated (scoping item 3).

**Stage 3 design requirement (recorded now, built at
Stage 3):** the verification gate must be write-free,
bytecode caches included — it runs with interpreter bytecode
writing disabled (`sys.dont_write_bytecode` /
`PYTHONDONTWRITEBYTECODE`) and proves the property by
hashing the published tree before and after a red run, which
must show the published artifacts byte-untouched (the note's
corollary, tying to Amendment 1's corollary 5).

## Harmonization adoption 3 — MPCodec's six findings

Adopted 2026-11-01 with the dispositions recorded at the
head of `spec.md`. The two items that touch this stage:

- **Item 6 (BINDING NOW) — the confidence audit.** A full
  census of every migrated population (every record, every
  key, both P2 serializations): the only confidence present
  is P1's `confidence_in_source`, a NUMBER (float) on all 31
  records; all 23 canonical records carry it and the 8 merged
  instances' values agree with their canonicals' (0
  differences). The P2 bundles carry no confidence field of
  any name at any depth in 1,624 records; P3 sidecars carry
  none. **No qualitative confidence exists in any migrated
  population, and no code in the migration mapped anything
  to a number** — before this adoption the field was simply
  not carried (a provenance gap). The gap is closed: the
  claim-entry shape gains the additive pair
  `confidence_in_source` (numeric, verbatim) /
  `confidence_text` (qualitative, verbatim, never
  normalized), populated by one shared builder helper;
  migrated entries carry the numbers above and
  `confidence_text: null` throughout; a teeth test proves a
  `"low"` string lands in `confidence_text` untouched.
  Anchor pairs' `confidence: "low"` values live outside this
  repo tree and are recorded as a Stage 4 intake constraint
  (entry only through `confidence_text`).
- **Item 1 — measurements assessment.** ledger-schema v1
  discriminates entries by `kind` with per-kind shapes, so a
  `measurement` kind (value, unit, direction, condition
  class, artifact sha256) fits as an ADDITION without
  altering the pinned claim-entry shape. Adopted for
  Stage 2 (the matrix generator mints them); not extracted
  by this migration; the pinned schema is unchanged for it
  in this stage.

Items 2–5 are recorded at the head of `spec.md` as binding
design inputs for their stages (V4 numeric arm; layers
distinction; counter-decomposition before "not checkable";
the pure-builder rule for Stages 2–3, alongside the
canonical-hash and gate-write-freedom requirements).

## Defect found in this stage's own gate, and fixed

The intake validator's first version **passed vacuously on a
missing ledger**: it read an absent file as zero lines and
reported `RESULT: PASS` over 0 entries. Found 2026-11-01
while re-running the validator during the canonical-hash
rebuild (the ledger file was momentarily absent and the
gate said PASS). Fixed in the same stage: a missing or
empty ledger is now RED with a named error, and two teeth
tests (`test_validator_fails_on_missing_ledger`,
`test_validator_fails_on_empty_ledger`) pin the behavior.
A gate that certifies an absent artifact is exactly the
failure this spec exists to prevent; the defect, its
discovery, and its fix are recorded here rather than
quietly absorbed.

## Correction after an upstream source act (PR #477), and a provenance defect it exposed

After this record was first written, main merged into this
branch carrying PR #477 — the owner's 2026-11-01 lane-2
adoption act, which refreshed the `not_understood` field of
two P1 source records in place (the RT-21 refreshes, each
with its dated append block). CI run `41327195581` then
failed `test_ledger_validates_clean` with exactly two
provenance errors: the two migrated entries' mirrored
`does_not_establish` texts no longer traced to their moved
sources of record. The correction re-executed this stage's
D-E migration run (same run id and date, the stage's own
tool, state never published) against the current sources —
the form C086-4's falsifier excepts ("a D-E migration record
that itself reconciles") — rather than editing lines or
appending reclassifications that cannot cure a stale
migration mirror. The two claims' status, stage, and
falsifier are unchanged (verified byte-equal); only the
mirrored does-not-establish texts and the affected source
hashes moved. Full account:
`records/reconciliation-p1.md`, addendum of 2026-11-01.

The re-execution's diff exposed a second, older defect in
this stage's own provenance: 21 further P1 entries carried
recorded source hashes matching no committed state of their
source files (the first execution ran against the extraction
store's suite-regenerated transient bytes; the store was
restored to its committed state without re-running the
migration, and no Stage 1 check compares recorded source
hashes). The re-execution re-traced all 23 P1 entries'
source hashes to the committed files; no substance field of
the 21 moved. The gap is named here because the Stage 3
gate's V1 class ("migration entries' source hashes match
their source files") would have caught it — Stage 1's own
tests should have, and the addendum lists every affected
entry by name.

## Test evidence

- **Targeted (this stage's gate set):** the two Spec 086
  test files + `test_spec029_phase_i.py` (the D-B fingerprint
  family) + `test_policy_sync_conformance.py` (Spec 084):
  **47 passed** in the CI venv on the final tree (the 43 of
  the pre-adoption tree plus the canonical-hash invariance
  test, the verbatim-confidence test, and the two
  missing/empty-ledger teeth added by the adoption #2/#3 and
  defect-fix work).
- **Full backend suite, run 1 (no `-x`, CI env, GPU files
  ignored as CI ignores them):** executed all 2,190 tests in
  5,144.74 s — **74 failed, 2,079 passed, 14 skipped,
  23 errors**. This run is NOT clean and is not offered as
  the acceptance run. Classification of every failure body:
  77 carry `PermissionError: [Errno 1] Operation not
  permitted` on plain file writes and 16 carry sqlite
  `disk I/O error` on WAL pragmas — the signature of this
  VM's intermittent write-denial wave, independently
  confirmed active during the run window (the wave probe
  read WAVE; git itself failed with an index.lock EPERM).
  The remaining assertion failures are downstream symptoms
  of the same denial (files that could not be written, a
  backend whose database writes were denied, one subprocess
  return-code assertion), plus one `FileNotFoundError` for a
  `research_notes/` path outside the repo in a pre-existing
  non-086 test (an environmental dependency of that test,
  unrelated to this change). All 11 failures in this spec's
  own intake test file carry the PermissionError signature —
  the same file passes standalone in ~2 s. The process also
  hung on exit after printing its summary (non-daemon
  threads) and was terminated; the summary line above is
  from its own completed output. Nothing was weakened,
  skipped, or deleted to make any run pass.
- **Full backend suite, run 2 (the acceptance run)** —
  executed under probe-verified CLEAR write conditions on
  the final tree, same invocation: **1 failed, 2,179
  passed, 14 skipped, 0 errors in 2,204.82 s**. The single
  failure is
  `test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`,
  and it is pre-existing and environmental, proven three
  ways: (i) its test file is byte-identical between
  origin/main and this branch (blob `e0033d8d…` both sides;
  this PR touches no phase133 file or builder); (ii) the
  failure is a `FileNotFoundError` for
  `~/workspace/research_notes/indus-data-deep-sweep-20261008/downloads/horus84-computational-linguistics/data/inscriptions.csv`
  — a path OUTSIDE the repo; this VM holds a partial
  research_notes tree (the sweep directory exists, the
  downloads subtree does not), so the test's skip condition
  does not fire and its builder subprocess dies on the
  missing CSV; where the tree is wholly absent, as in CI,
  the test skips and main's CI is green; (iii) it failed
  identically in run 1. It is named here and in the PR body
  rather than repaired: repairing another spec's test is
  outside this stage's scope, and weakening or skipping it
  is prohibited. Every other test — including all of run
  1's wave casualties — passes.

## Corrections to package premises, found by the build

1. **P1's falsifier gap is smaller than the package
   states.** The audit looked for a field named `falsifier`
   and found none (0 of 31). The store carries the same
   content as `falsification_condition` on 15 of 31 records;
   the migration carries it, so 14 of 23 canonical entries
   hold a falsifier and the true null gap is 9 entries. The
   gap discipline (null counted, never invented, backfill
   only by human-authored reclassification) is unchanged.
2. **P2 restatements are not byte-identical governance
   records.** Successor specs restate proposition texts
   verbatim while carrying their own falsification tests
   (26 of 44 cross-spec groups) and boundary lines (40 of
   44). The D-B merge therefore takes the falsifier as the
   ordered union (every string traceable to a named source)
   and the boundary as the representative's, with variants
   enumerated in the reconciliation — recorded here so the
   merge rule is a decision on record, not a silent default.

## Claims assessed at Stage 1 (stage scope)

- **C086-1 — SUPPORTED (stage scope).** The ledger exists as
  the single artifact every later layer must read; the four
  intake routes are the only write path in code, and the
  migration accounts for every source record. (The full
  falsifier — matrix/map traceability — is testable only
  from Stage 2 on.)
- **C086-2 — SUPPORTED.** Validator enforces the pinned
  schema in tests; seeded malformed line fails validation
  (teeth test).
- **C086-3 — SUPPORTED.** Fingerprints recompute under the
  frozen rules; the built ledger has no shared fingerprint;
  a duplicate intake is refused naming both records, writing
  nothing (teeth test).
- **C086-4 — SUPPORTED (stage scope).** Appends are
  prefix-preserving verified writes (test); no ledger line
  has been edited in place outside the one D-E migration
  re-execution recorded in the correction section above
  (C086-4's own carve-out: a migration record that itself
  reconciles); no reclassification exists yet.
- **C086-5 — SUPPORTED.** Provenance checks refuse untraced
  falsifier text (teeth test); the validator publishes the
  coverage count on every run (831 of 840; the 9 nulls are
  P1's counted gap).
- **C086-6 — SUPPORTED.** An authorless explanation is
  refused (teeth test); the 23 P1 explanation records in the
  ledger all name the human author of the 2026-10-13
  adoption act (and its 2026-11-01 amendment for the two
  refreshed texts).
- **C086-20 — SUPPORTED.** Reconciliation mirror checks
  (status/stage byte-equal per claim, recomputed
  independently in the migration test) show no verdict,
  status, or stage moved by the migration.
- **C086-21 — SUPPORTED (Stage 1 leg).** The D-A
  generalization pattern note is written and filed
  (`records/pattern-note-ledger-schema-validator.md`);
  delivery to the RCPH and Atlas chats is the parent chat's
  act and is recorded there. The incoming Atlas note's
  adoption record is in the LEDGER.md entry (T003).
- C086-7…C086-19 are **not yet assessed** — their falsifiers
  execute against the matrix (Stage 2), the gate (Stage 3),
  settling (Stage 4), and the map (Stage 5), which do not
  exist yet.

## Stage 1's "does not establish" lines (from tasks.md)

- T101: *This does not establish that the schema is the
  right one — only that it is pinned and enforceable.*
- T102: *This does not establish that honest entries are
  true — only that unprovenanced ones cannot enter quietly.*
- T103: *This does not establish that future real intake
  will be clean — only that the four doors exist and are
  the only ones the code provides.*
- T104: *This does not establish that the migrated claims
  are correct — only that the ledger mirrors the record
  without loss or invention.*
- T105: *This does not establish the matrix will be right —
  only that what it will be generated from is now one
  validated artifact.*

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
