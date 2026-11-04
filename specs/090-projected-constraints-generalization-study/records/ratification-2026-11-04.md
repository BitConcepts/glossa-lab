# Ratification + adoption record — Spec 090 (2026-11-04)

**Scope:** tasks.md Stage 0 (T001–T004), executed on this
branch (`feat/090-adoption`) after the owner's block
ratification. This record covers the ratification act, the
claims-ledger intake the framework requires of an adopted
spec, and the regeneration of the generated layers over the
grown ledger. No study stage (S1–S3) is started by this
motion. T001 (package lands) is completed by this PR, T002
(AEE verification) was completed at drafting with its
assessment of record in the package, and both are ticked in
tasks.md on that evidence, as are T003 (this act) and T004
(this intake).

## The ratification act (T003)

**Owner block ratification: Tristen Pierson, 2026-11-04.**
The approval chain, stated exactly: the owner approved the
open items in the VEXA chat on 2026-11-04 ("do all these
things up to needing the device. you have my approval");
that approval was relayed to this program the same day
(12:24 ET) as covering the Spec 090 package ratification:
when the package (claims with falsifiers, plan, tasks) is
presented, it stands **RATIFIED AS A BLOCK** on the owner's
word given in the VEXA chat. The package was presented in
the Glossa-Lab chat on 2026-11-04 and stands ratified on
presentation. The act ratifies the spec, the 16 claims
(C090-1..16), the plan, and decisions D-090-1..4 as
recommended:

- **D-090-1 — The G1 document is a single standalone
  artifact in the spec's records** (`records/g1-document.md`,
  versioned only by recorded amendment acts, identifiable by
  hash, written to be handed to the judging protocol's
  reader as-is).
- **D-090-2 — The absolute question is decided by audit at
  S1, not pre-decided by this package** (candidates
  enumerated and disposed of; exactly one named absolute, a
  none-needed proof, or the two-absolutes skeleton-mismatch
  finding are all legitimate; the owner is the oracle if the
  S1 adversarial pass sustains a split the drafters cannot
  close).
- **D-090-3 — Derivation provenance: from the stated
  projection only** (every G2 chain step follows from D1–D3
  and the G1 document's stated projection rule; the physics
  instantiation may be named as a candidate's occasion,
  never as a premise).
- **D-090-4 — The outcome is reported to the VEXA chat as a
  study deliverable, whatever it is** (per-stage outcomes,
  the study-level outcome in the skeleton's vocabulary, and
  the evidence pointers, for the improvement registry —
  including when the outcome is ANALOGY or NOT YET).

**Boundaries the owner set, carried verbatim into this
adoption:** if the package changes materially after
presentation (new claims, changed falsifiers, expanded
scope), that is a new decision, not carried under this
approval — no such change is made by this motion. The
owner's "up to needing the device" limit applies to the
VEXA chat's spatial spike work, not to this study.

**Commission boundary restated:** this study is not a
convergence step. Glossa remains at convergence Stage 0;
nothing in this adoption enters the program into VEXA
convergence Stage 1, alters the program's local stack, or
contributes a convergence-dashboard item (C090-14).

**T002 outcome noted:** the AEE assessor (aee 1.5.3, the
pinned CI-faithful venv) read the draft bundle as
**outcome: iterate** (71 failure modes; 16 claims below the
0.70 threshold; draft cap and stage cap binding by
construction) — the expected draft-stage reading, recorded
verbatim in `records/t002-note.md` with the assessment at
`records/t002-aee-assessment.json`. The owner's ratification
is the human act that carries the claims forward.

## A tension inside C090-13, named

C090-13 states that the study's only ledger change is its
adoption intake append (plus the regeneration of the
generated layers that append forces), and its own text
names this pattern (the C088-15 / C089-18 pattern). This
append is that change — by design: it is the framework's
own intake of this spec's claims, performed exactly as Spec
086's adoption appended its own 21, Spec 087's its 17 (the
C087-14 precedent), Spec 088's its 19, and Spec 089's its
20. The claim's operative scope is the study stages'
treatment of Indus claim content: **no Indus claim's
status, stage, or score moved in this motion** — the
validator's mirror counts and the reconciliation test prove
the append is additive only, the freeze records are
untouched, and the 16 appended entries are this spec's own
governance claims at draft/created. The program's standing
position (the Indus script is not deciphered) is untouched.

## Why this motion appends to the ledger

Under the Winning Combination discipline (one claims
ledger, sole entry point, every claim enters through
intake), an adopted spec's bundle is appended through the
sanctioned intake path — and the bundle-reconciliation test
(`test_p2_reconciliation`) requires the ledger's bundle
population to equal the bundles on disk, so an
adopted-but-not-appended bundle fails CI. This is the same
self-intake Specs 086, 087, 088, and 089 performed at their
adoptions.

## Intake path used (T004b)

`tools/ledger/import_bundle.py --spec
specs/090-projected-constraints-generalization-study
--date 2026-11-04` — Spec 086 intake route 2 (T103):
`build_bundle_entries` forms the entries and `append_entry`
validates and appends each one (schema, fingerprint
recomputation, provenance, duplicate refusal, verified
append-only write). No entry was hand-written and
claims.jsonl was never hand-edited.

Output (verbatim): **16 appended, 0 already canonical, 16
propositions** — no refusal, no duplicate, no schema
failure.

Entry formation mirrors the migrated bundle convention:
id `090-projected-constraints-generalization-study/C090-N`;
population `bundle`; a single `source_of_record` source
naming this spec's `aee-claims.json`; status/stage mirrored
from the bundle record (`draft` / `created`); falsifier
carried from each record's `falsification_tests` (all 16
carry one); the appended entries carry an empty `sign_refs`
list (the ledger's only sign_refs-bearing entry remains the
pre-existing one).

## Ledger before / after

- Before: **927 lines**, SHA-256
  `b442ce7e5825e938fbd4bc0033bcb0582b37c71fe724a55f4584b5a4d5213712`
  (1,923,481 bytes).
- After: **943 lines**, SHA-256
  `15a5fbad24f400631ace1ebc88bfb7712c9bf6f68fae23e56fedbcac5fd5a794`
  (1,952,764 bytes).
- Append-only verified byte-wise: the after file's first
  1,923,481 bytes hash to the before file's SHA-256.

Validator output (verbatim):

```text
Ledger validation — /home/hatch/workspace/glossa-run/system-coupling-audit/glossa-indus/ledger/claims.jsonl
schema: ledger-schema v1 (glossa-indus/ledger/ledger-schema.json)
fingerprint rules: spec029-phase-i-v1
lines: 943
entries by kind: annotation 31, claim 912
claims by population: bundle 889, extracted 23
falsifier coverage: 903 of 912 claim entries carry a falsifier
falsifier coverage by population: bundle 889/889, extracted 14/23
does_not_establish coverage: 755 of 912 claim entries
aee_state present: 0 of 912 claim entries
errors: none
RESULT: PASS
```

## Pre-append gate run (T004a)

Recorded on the un-appended tree (the branch base, before
the package copy and the intake) with the standalone gate
CLI, verbatim summaries:

```text
full:    summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

## The taxonomy precondition (executed first, per the gate's own coverage rule)

The gate's V10 derivation resolves every claim's home spec
through the program-map taxonomy; a spec directory with no
assignment cannot be recomputed (at Spec 089's adoption the
first gated attempt died on exactly this, with `KeyError:
'089-run-scoped-results'`, before any artifact write). The
amendment the gate's own coverage rule requires was
therefore executed **before** the gated chain in this
adoption: one study row added to
`glossa-indus/map/program-map-taxonomy.json` —
`090-projected-constraints-generalization-study` under
**Program infrastructure / Governance, lifecycle &
generated layers**, beside Specs 084, 086, 087, 088, and
089. The registered version string (`program-map-taxonomy
v1`, pinned identically in the definitions document, the
builder, and the gate's own copies) is unchanged: adding a
study assignment is the file's normal operation under v1,
and a version change would itself be a program-map-defs
amendment, which no adoption motion may make unilaterally.
The taxonomy carries grouping only — no standing of any
kind was added (C2 holds).

## Regeneration of the generated layers (T004c)

With the taxonomy amended, the precedent's chain executed
in its order. The first gated attempt
(`generate_matrix.py --gated`) ran and went **gate RED: 16
PASS / 8 FAIL / 2 NOT-RUN, RESULT: FAIL** — the precedent's
shape (V2 claims-by-status, both V5 map legs, V8 settling
canonicals, and the four V10 legs) — and the published
artifacts stayed byte-untouched (verified by hash:
matrix, matrix.md, map-data, program-map, finds, and page
all identical before and after the refused publication).
The settling chain refresh below resolved V8; the ordering
then closed:

1. Matrix regenerated by the pure builder
   (`generate_matrix.py`; `--check` → CHECK: MATCH):
   matrix.json `2509201b…` → `922fa091…` (774,134 bytes),
   matrix.md `daf9352f…` → `7774520d…`.
2. Program map regenerated by the pure builder
   (`tools/map/generate_program_map.py`; `--check` → OK):
   program-map.json `f329b7bd…` → `9bd26114…`,
   program-map-finds.json `1b6fb256…` → `2c874c4f…`,
   program-map.html `887bfad1…` → `cecb5473…`.
3. Map published through gated publication
   (`generate_map.py --gated`): gate **25 PASS / 0 FAIL /
   1 NOT-RUN, RESULT: PASS**; map-data.json `c8d920e2…` →
   `7b404859…` (4,789,652 bytes).
4. Matrix republished through `generate_matrix.py
   --gated` with the gate at RESULT: PASS (identical
   bytes), and the program map republished through
   `publish_program_map` in `backend/glossa_lab/
   gated_publish.py` (the sanctioned route Spec 088 S4
   built; it has no CLI wrapper) with **published: True**
   at identical bytes — the final state of every artifact
   is the product of a passing gated run.

Standalone gate of record (verbatim summaries):

```text
full:    summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

Census after regeneration: 912 claims (bundle 889,
extracted 23); falsifier coverage 903/912; matrix 1,435
cells (supports 1,428 / opposes 7 / constrains 0), 912
rows × 644 columns; map 1,556 elements, 1,435 edges;
program map 912 claim nodes (open 903 / negative 6 /
positive 2 / closed_other 1) and 91 study nodes (open 62 /
unjudged 28, +1 restricted name-only), judgment calls 0,
find list unchanged at 38 (28 bundle-less studies, 9
extracted null falsifiers, 1 restricted node); domains
(studies/claims): Sign inventory & corpus 17/125 · Anchors
& readings 13/0 · Claim families 40/568 · Contact zone
2/33 · Program infrastructure 19/186.

## The settling chain refresh (the precedent's procedure, executed in full)

As at Specs 087's, 088's, and 089's adoptions, matrix +
map regeneration alone could not return the gate to green:
the settling layer's registered pins name the ledger build
they were derived over. Every refresh below was executed
only after independent recomputation proved the
expectations unchanged. Nothing was force-fit and no gate
check was loosened.

1. **Canonicals provenance pin (V8).**
   `glossa-indus/ledger/settling-canonical.json` governs
   one pinned build by design. Before the pin was touched,
   `tools/ledger/run_settling.py verify-canonicals` was
   run over the new build: **6/6 registered canonicals
   reproduce**, field-for-field. Only then was the pin
   refreshed (provenance.ledger and the comparison's
   inputs.ledger_sha256: `b442ce7e…`/927 → `15a5fbad…`/943),
   with the re-derivation recorded in the file itself
   (`re_derivations[3]`, 2026-11-04: act, reason, both
   pins, verification). Expectations did not change; the
   semantics (glossa-settle-1) did not change, so no new
   semantics version is registered.
2. **T405 run records (map builder D-D refusal).** Both
   T405 scenarios were re-executed through
   `run_settling.py run` under the Stage 4 protocol (same
   candidates, same 286-sign full-frame scope): new
   records `t405-incumbent-over-full-frame--d9f73e4c4e4e
   .json` (SHA-256 `17d7dbae…`) and
   `t405-full-register-over-full-frame--f8c86443e924.json`
   (SHA-256 `176ca660…`). Their result blocks are
   byte-equal to the superseded runs'; the only differing
   field is the pins block. The two superseded old-build
   records (`…--c78f3e07ec82.json`, SHA-256 `89fb596c…`;
   `…--fb1697b3f6de.json`, SHA-256 `018c99ca…`) were
   removed from the store, because the builder's
   registered rule admits no stale-pinned record there;
   both stand preserved in git history and are cited here
   with their hashes.
3. **Filed dual-run comparison (map builder D-D
   refusal).** `specs/086-winning-combination-adoption/
   records/stage-4-dual-run-comparison.json` was re-filed
   from the new runs via `run_settling.py compare`, after
   verifying its content is identical to the previous
   filing except the ledger pin (two leaves: sha256 and
   lines): SHA-256 `d5997c14…` → `1371c981…`; the
   comparison over the new pair compares 1 claim with
   **per_claim_divergences: []** and Stage 4's coverage
   numbers (94 / 286 assigned, 0 conflicts). The Spec 089
   adoption record's citation of `d5997c14…` stands as the
   historical citation of the filing as made at that
   adoption.

## Test maintenance — census re-pins

The Spec 086 Stage 5 tests, the gate battery, the Spec 088
program-map tests, and the program-map conformance pins pin
the artifact census of their build; the append moved every
census number by exactly the 16 claims (each new claim adds
one supports cell: its own document's). The pins were
re-set to the regenerated artifacts' actuals — every value
below recomputed from matrix.json / map-data.json /
program-map.json / the gate's own evidence text, none
adjusted to fit. The sweep was run over the whole test tree
(backend/tests + frontend/e2e), not only the files the
precedents touched:

- `backend/tests/test_program_map_conformance.py`:
  PIN_CLAIMS 896 → 912; PIN_CLAIMS_BY_POPULATION bundle
  873 → 889 (extracted 23 unchanged); PIN_CLAIMS_BY_CLASS
  open 887 → 903 (closed_other 1, negative 6, positive 2
  unchanged); PIN_STUDIES 90 → 91; PIN_FALSIFIER_PRESENT
  887 → 903; taxonomy-hygiene domain total "Program
  infrastructure" 18 → 19 studies. Verified NOT stale in
  the same file: PIN_UNJUDGED 28, PIN_MULTI_SPEC 44,
  PIN_NULL_FALSIFIER_EXTRACTED 9.
- `backend/tests/test_spec086_ledger_gate.py`: "1419
  matrix cells" → "1435 matrix cells"; "896 claims counted
  across 8 statuses" → "912…"; "1419 map edges by relation"
  → "1435…"; "supports 1412, opposes 7, constrains 0" →
  "supports 1428, opposes 7, constrains 0"; "896 claim
  nodes" → "912 claim nodes"; "90 study nodes" → "91 study
  nodes".
- `backend/tests/test_spec086_map.py`: claims_total 896 →
  912 (3 sites); draft 872 → 888; status sum 896 → 912;
  ledger_lines 927 → 943; claim elements 896 → 912;
  elements total 1,540 → 1,556; supports 1,412 → 1,428
  (2 sites); loads 896 → 912; falsifier census 887/896 →
  903/912; AEE census 896 → 912 (2 sites); claims
  untouched by any run 895 → 911; the scoped-404 leak
  marker `"896"` → `"912"`.
- `backend/tests/test_spec088_program_map.py`: the
  real-ledger canary `assert "896" not in page` → `"912"`
  (the assertion guards a fixture build against
  real-ledger leakage; its canary is the real census
  total, which the append moved — teeth preserved).
- `frontend/e2e/system-graph.spec.ts`: "896 claims in the
  ledger" → "912 claims in the ledger".

No assertion was weakened, skipped, or deleted; each pin
still asserts the exact census, now of the current build.
Anchors (287, strict 94), `no_stage_recorded` (15), the
find-list pins (28 bundle-less, 1 restricted), and the map
header's nearest-dated items did not move.

## Test results

Targeted surface (the precedents' seven files plus
`test_program_map_conformance.py`, whose missed re-pin
bounced Spec 089's adoption at CI), in the CI venv
(`~/workspace/venvs/glossa-ci`) with TMPDIR on disk, read
from the run log: **159 passed** (562.17s) — the
reconciliation test `test_p2_reconciliation` among them.

Full backend suite, run locally WITHOUT `-x` from the log
(the enumeration that keeps an adoption from bouncing at
CI): **1 failed, 2,567 passed, 98 skipped, 1 deselected**
(381.58s). The one failure is the known phase133
environmental baseline
(`test_phase133_stage0_inventory.py::
test_builder_recomputation_skips_without_inputs` —
missing download; fails locally everywhere, does not fail
CI). No tray-teardown ERROR appeared this run. The single
deselect was
`test_phase392_q2_gate.py::
test_pipeline_deterministic_under_seed` (the known local
stall), named here as the brief requires. Ruff over
`backend/`: all checks passed. After every suite run,
`git status` was checked and the in-tree regenerations the
suites cause (extracted_claims JSONs, one claim report,
one outputs file) were restored; the final tree carries
only this motion's intended changes.

## Naming — one departure, recorded

The package's internal texts name the landing branch
`feat/090-spec-package` (spec.md head; tasks.md T001).
This motion executed on `feat/090-adoption`, the branch
the adoption brief names — the same class of departure
Spec 088's adoption recorded (there the brief moved the
motion to `feat/088-adoption` /
`specs/088-full-picture-map-gap-register/`). The spec
directory executed is the one D-090-1 and tasks.md T001
name: `specs/090-projected-constraints-generalization-study/`.
The package files were copied byte-identical (`diff -r`
clean; the two VEXA source documents hash to their pinned
values a66ffe4f… / 281f3543…), so the only internal
reference at odds with the executed names is the landing
branch named in the package's own prose.

## Claims assessed at adoption (adoption scope)

- **C090-13 — adoption leg holds.** The ledger diff of
  this motion is exactly the 16-entry intake append this
  record describes, plus the regeneration of the generated
  layers that append forces; no other ledger change is
  attributable to this PR, and no Indus claim's
  status/stage/score moved. The claim's study-stage scope
  is not yet assessed.
- All other C090 claims are **not yet assessed** — their
  falsifiers execute against stages S1–S3, which have not
  started.

## Stage 0's "does not establish" lines (from tasks.md)

- T003: *This does not establish: approval of any later
  stage's output — the G1 document, the derivation, and
  the outcome each land on their own evidence.*
- T004: *This does not establish: anything about the
  appended claims' truth — only that the ledger grew by
  the sanctioned path and the generated layers match it.*

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
