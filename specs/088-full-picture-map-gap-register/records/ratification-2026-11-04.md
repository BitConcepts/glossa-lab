# Ratification + adoption record — Spec 088 (2026-11-04)

**Scope:** tasks.md Stage 0 (T003 + T004), executed on this
branch (`feat/088-adoption`) after the owner's block
ratification. This record covers the ratification act, the
claims-ledger intake the framework requires of an adopted
spec, and the regeneration of the generated layers over the
grown ledger. No build stage (S1–S6) is started by this
motion. T001 (package lands) is completed by this PR and
T002 (AEE verification) was completed at drafting; both are
recorded in the package itself.

## The ratification act (T003)

**Owner block ratification: Tristen Pierson, 2026-11-04**,
by option tap in the Glossa-Lab chat: "Ratify the package
as a block." The act ratifies the spec, the 19 claims
(C088-1..19), the plan, the taxonomy v0 draft
(`records/taxonomy-v0-draft.md`), and decisions D-088-1..6
as recommended:

- **D-088-1 — Node granularity: one node per claim, one
  per study** (857 claim nodes + 88 study nodes at drafting;
  the taxonomy supplies grouping for display).
- **D-088-2 — No curated standings (C2 applied).** RCPH's
  `curated` mechanism is rejected for Glossa; the unjudged
  class and the find list replace it.
- **D-088-3 — The derivation table's two judgment rows
  ratified as drawn**, including **partially_supported →
  open** (partial support is not a program judgement of
  support; v1 has no "mixed" class; the verbatim status
  still shows in the standing text). The full table:
  strongly_supported → positive; contradicted / unsupported
  / partially_falsified → negative; superseded →
  closed_other; draft / untested → open. Any status outside
  the table fails the build.
- **D-088-4 — `in_flight` is registered with an empty v1
  population** (no record of record carries study run-state;
  deriving it from prose is C2-forbidden).
- **D-088-5 — Map home and stamp.** Artifacts live in
  `glossa-indus/map/` beside Spec 086's map; the as-of stamp
  carries only input-derived values — no wall-clock date.
- **D-088-6 — Restricted studies render name-only** (the
  v1 population is exactly Spec 072, under its standing
  owner restriction).

**Taxonomy v0 ratified including its two judgment calls:**
Spec 027 sits in Domain 4 (Contact zone & external corpora)
rather than Domain 3, so the contact domain is not a
single-study domain; and Domain 3 carries a fourth
subdomain, "Extracted literature claims," for the 3
extracted documents (12 claims) with no testing line.

**T002 outcome noted:** the AEE assessor (aee 1.5.3) read
the draft bundle as **outcome: iterate** (80 failure
modes; 19 claims below the 0.70 threshold; draft cap and
stage cap binding by construction) — the expected
draft-stage reading, recorded verbatim in
`records/t002-note.md`. The owner's ratification is the
human act that carries the claims forward.

## A tension inside C088-15, named

C088-15 states that the spec's only ledger change is its
adoption intake append, and its falsifier names any other
ledger diff attributable to a Spec 088 PR. This append is
that change — by design: it is the framework's own intake
of this spec's claims, performed exactly as Spec 086's
adoption appended its own 21 and Spec 087's its 17 (the
C087-14 precedent, named the same way in that adoption
record). The claim's operative scope is the build stages'
treatment of Indus claim content: **no Indus claim's
status, stage, or score moved in this motion** — the
validator's mirror counts and the reconciliation test
prove the append is additive only, the freeze records are
untouched, and the 19 appended entries are this spec's own
governance claims at draft/created.

## Why this motion appends to the ledger

Under the Winning Combination discipline (one claims
ledger, sole entry point, every claim enters through
intake), an adopted spec's bundle is appended through the
sanctioned intake path — and the bundle-reconciliation
test (`test_p2_reconciliation`) requires the ledger's
bundle population to equal the bundles on disk, so an
adopted-but-not-appended bundle fails CI. This is the same
self-intake Specs 086 and 087 performed at their adoptions.

## Intake path used (T004b)

`tools/ledger/import_bundle.py --spec
specs/088-full-picture-map-gap-register --date 2026-11-04`
— Spec 086 intake route 2 (T103): `build_bundle_entries`
forms the entries and `append_entry` validates and appends
each one (schema, fingerprint recomputation, provenance,
duplicate refusal, verified append-only write). No entry
was hand-written and claims.jsonl was never hand-edited.

Output (verbatim): **19 appended, 0 already canonical, 19
propositions** — no refusal, no duplicate, no schema
failure.

Entry formation mirrors the migrated bundle convention:
id `088-full-picture-map-gap-register/C088-N`; population
`bundle`; a single `source_of_record` source naming this
spec's `aee-claims.json`; status/stage mirrored from the
bundle record (`draft` / `created`); falsifier carried
from each record's `falsification_tests` (all 19 carry
one); the appended entries carry no sign_refs (the
ledger's only sign_refs-bearing entry remains the
pre-existing one).

## Ledger before / after

- Before: **888 lines**, SHA-256
  `f988ed61404daf8200479e9d1a6580526c7b419ba7e802a3b6b41a5a73a167ac`
  (1,858,984 bytes).
- After: **907 lines**, SHA-256
  `9f8144c3fa73d7cfa4ffd02d3b6c23c3ea9e0c1e164e9497232dd2842e0a022c`
  (1,888,902 bytes).
- Append-only verified byte-wise: the after file's first
  1,858,984 bytes hash to the before file's SHA-256.

Validator output (verbatim):

```text
Ledger validation — /home/hatch/workspace/glossa-run/system-coupling-audit/glossa-indus/ledger/claims.jsonl
schema: ledger-schema v1 (glossa-indus/ledger/ledger-schema.json)
fingerprint rules: spec029-phase-i-v1
lines: 907
entries by kind: annotation 31, claim 876
claims by population: bundle 853, extracted 23
falsifier coverage: 867 of 876 claim entries carry a falsifier
falsifier coverage by population: bundle 853/853, extracted 14/23
does_not_establish coverage: 755 of 876 claim entries
aee_state present: 0 of 876 claim entries
errors: none
RESULT: PASS
```

## Pre-append gate run (T004a)

Recorded on the un-appended tree before the intake ran
(standalone gate CLI, verbatim summaries):

```text
full:    summary: 20 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 23 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

## Regeneration of the generated layers (T004c)

First attempt — `tools/ledger/generate_matrix.py --gated`
— **gate RED: 15 PASS / 4 FAIL / 2 NOT-RUN, RESULT:
FAIL**, and the published artifacts stayed byte-untouched
(verified by hash). The four failures are the precedent's
four: V2 claims-by-status and both V5 map legs (the gate
reads the then-stale published map) and V8 settling
canonicals (the canonicals' provenance pin names the
previous ledger build). The settling chain refresh below
resolved V8; the ordering then closed:

1. Matrix regenerated by the pure builder
   (`generate_matrix.py`; `--check` → CHECK: MATCH):
   matrix.json `ff0788a1…` → `4b40d126…` (760,400 bytes),
   matrix.md `5364bd8b…` → `470570ab…`.
2. Map published through gated publication
   (`generate_map.py --gated`): gate **20 PASS / 0 FAIL /
   1 NOT-RUN, RESULT: PASS**; map-data.json `ad4ee299…` →
   `b419f90b…` (4,628,533 bytes).
3. Matrix republished through `generate_matrix.py
   --gated` with the gate at **20 PASS / 0 FAIL / 1
   NOT-RUN, RESULT: PASS** (identical bytes; the final
   state of both artifacts is the product of a passing
   gated run).

Standalone gate of record (verbatim summaries):

```text
full:    summary: 20 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 23 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

Census after regeneration: 876 claims (bundle 853,
extracted 23); falsifier coverage 867/876; matrix 1,399
cells (supports 1,392 / opposes 7 / constrains 0); 4,198
citations tied under V4; map 1,520 elements, 1,399 edges.

## The settling chain refresh (the precedent's procedure, executed in full)

As at Spec 087's adoption, matrix + map regeneration
alone could not return the gate to green: the settling
layer's registered pins name the ledger build they were
derived over. Every refresh below was executed only after
independent recomputation proved the expectations
unchanged. Nothing was force-fit and no gate check was
loosened.

1. **Canonicals provenance pin (V8).**
   `glossa-indus/ledger/settling-canonical.json` governs
   one pinned build by design. Before the pin was touched,
   `tools/ledger/run_settling.py verify-canonicals` was
   run over the new build: **6/6 registered canonicals
   reproduce**, field-for-field. Only then was the pin
   refreshed (provenance.ledger and the comparison's
   inputs.ledger_sha256: `f988ed61…`/888 → `9f8144c3…`/907),
   with the re-derivation recorded in the file itself
   (`re_derivations[1]`, 2026-11-04: act, reason, both
   pins, verification). Expectations did not change; the
   semantics (glossa-settle-1) did not change, so no new
   semantics version is registered.
2. **T405 run records (map builder D-D refusal).** Both
   T405 scenarios were re-executed through
   `run_settling.py run` under the Stage 4 protocol (same
   candidates, same 286-sign full-frame scope): new
   records `t405-incumbent-over-full-frame--5b1d1c866b0e
   .json` (SHA-256 `a5597836…`) and
   `t405-full-register-over-full-frame--070f8f0f476f.json`
   (SHA-256 `ab3db0ec…`). Their result blocks are
   byte-equal to the superseded runs'. The two superseded
   old-build records (`…--763e4f7b44f9.json`, SHA-256
   `5fb7ffb9…`; `…--cf47a3fa5a80.json`, SHA-256
   `60aa698c…`) were removed from the store, because the
   builder's registered rule admits no stale-pinned record
   there; both stand preserved in git history and in the
   Spec 087 adoption record with their hashes.
3. **Filed dual-run comparison (map builder D-D
   refusal).** `specs/086-winning-combination-adoption/
   records/stage-4-dual-run-comparison.json` was re-filed
   from the new runs via `run_settling.py compare`, after
   verifying its content is identical to the previous
   filing except the pins: SHA-256 `ac0d5310…` →
   `fce929e6…`; the comparison over the new pair compares
   1 claim with **per_claim_divergences: []** and Stage
   4's coverage numbers (94 / 286 assigned, 0 conflicts).
   The Spec 087 adoption record's citation of `ac0d5310…`
   stands as the historical citation of the filing as made
   at that adoption.

## Test maintenance — census re-pins

Spec 086's Stage 5 tests pin the artifact census of their
build; the append moved every census number by exactly
the 19 claims (each new claim adds one supports cell: its
own document's). The pins were re-set to the regenerated
artifacts' actuals — every value below recomputed from
matrix.json / map-data.json / the gate's own evidence,
none adjusted to fit:

- `backend/tests/test_spec086_map.py`: claims_total 857 →
  876 (3 sites); draft 833 → 852; status sum 857 → 876;
  ledger_lines 888 → 907; claim elements 857 → 876;
  elements total 1,501 → 1,520; supports 1,373 → 1,392
  (2 sites); loads 857 → 876; falsifier census 848/857 →
  867/876; AEE census 857 → 876; claims untouched by any
  run 856 → 875; the scoped-404 leak marker `"857"` →
  `"876"`.
- `backend/tests/test_spec086_ledger_gate.py`: "1380
  matrix cells" → "1399 matrix cells"; "857 claims counted
  across 8 statuses" → "876…"; "1380 map edges by
  relation" → "1399…"; "supports 1373, opposes 7,
  constrains 0" → "supports 1392, opposes 7, constrains
  0".
- `frontend/e2e/system-graph.spec.ts`: "857 claims in the
  ledger" → "876 claims in the ledger".

No assertion was weakened, skipped, or deleted; each pin
still asserts the exact census, now of the current build.
Anchors (287, strict 94) and `no_stage_recorded` (15) did
not move, and the map header's nearest-dated items are
unchanged.

## Targeted test results

Per the precedent's surface, in the CI venv
(`~/workspace/venvs/glossa-ci`) with TMPDIR on disk:
**108 tests across the six files, all passing** in the
final run — test_spec086_ledger_migration.py (including
`test_p2_reconciliation`, the bundle-reconciliation test
of T004d), test_spec086_ledger_gate.py,
test_spec086_map.py, test_spec086_matrix.py,
test_settling_canonical.py, test_spec086_ledger_intake.py.
Before the re-pins, the same batch showed 8 failed / 100
passed / 1 error: every failure a census literal of the
old build differing by exactly the append's arithmetic,
and the single ERROR a session-fixture teardown fault
(sqlite "Cannot operate on a closed database" — the known
teardown flake signature) that did not recur in the final
run. Ruff on the two touched Python test files: all checks
passed. After every suite run, `git status` was checked;
the final tree carries only this motion's intended changes
(no extracted-claims or report rewrites persisted).

## Departures from the package draft's naming, recorded

- The package draft names its landing directory
  `specs/088-program-map-gap-register/` and branch
  `feat/088-spec-package` (tasks.md T001, spec.md head).
  This motion executed as
  `specs/088-full-picture-map-gap-register/` on branch
  `feat/088-adoption`, per the adoption brief. The package
  files were copied byte-identical, so their internal
  references to the draft path stand as drafted; the
  intake, this record, and the PR use the executed names.
- T004's text names `tools/ledger/gated_publish.py` for
  republication; no such file exists. Republication ran
  through the precedent's sanctioned route
  (`generate_matrix.py` / `generate_map.py --gated`,
  backed by `backend/glossa_lab/gated_publish.py`), which
  is what T004's acceptance (the ledger-gate job green
  incl. the reconciliation test) turns on.

## Claims assessed at adoption (adoption scope)

- **C088-15 — adoption leg holds.** The ledger diff of
  this motion is exactly the 19-entry intake append this
  record describes; no other ledger change is attributable
  to this PR, and no Indus claim's status/stage/score
  moved. The claim's build-stage scope is not yet assessed.
- All other C088 claims are **not yet assessed** — their
  falsifiers execute against stages S1–S6, which have not
  started.

## Stage 0's "does not establish" lines (from tasks.md)

- T003: *This does not establish: approval of any later
  stage's output — each lands on its own evidence; and
  the register is ratified separately at T603.*
- T004: *This does not establish: anything about the
  appended claims' truth — only that the ledger grew by
  the sanctioned path and the generated layers match it.*

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
