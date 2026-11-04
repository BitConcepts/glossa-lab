# Ratification + adoption record — Spec 089 (2026-11-04)

**Scope:** tasks.md Stage 0 (T003 + T004), executed on this
branch (`feat/089-spec-package` — the branch the package
itself names, tasks.md T001 / spec.md head) after the owner's
block ratification. This record covers the ratification act,
the claims-ledger intake the framework requires of an adopted
spec, and the regeneration of the generated layers over the
grown ledger. No build stage (S1–S5) is started by this
motion. T001 (package lands) is completed by this PR and
T002 (AEE verification) was completed at drafting; both are
recorded in the package itself.

## The ratification act (T003)

**Owner block ratification: Tristen Pierson, 2026-11-04**,
by option tap in the Glossa-Lab chat: "Ratify the Spec 089
package as a block." The act ratifies the spec, the 20 claims
(C089-1..20), the plan, and decisions D-089-1..6 as
recommended:

- **D-089-1 — Run-id format and minting point:**
  execution-minted opaque id, `<surface>-<UTC
  yyyymmddThhmmssZ>-<6 hex random>`, minted by the executing
  tool at start, before results exist (content addressing is
  the defect being removed; a counter fails across hosts).
- **D-089-2 — Junction analysis: standalone tool, gate
  verifies.** The junction tool produces junction reports as
  records; gate class V11 verifies their existence,
  vocabulary, and relations — the gate never originates
  analysis.
- **D-089-3 — Quarantine and relations live in a per-store
  run index** (supersedes / superseded-by links, quarantine
  state with junction and adjudication references, legacy
  entries) — never a flag edited onto an immutable record.
- **D-089-4 — The comparability key's constitutive
  components (the judgment row):** surface, command/tool,
  input pins, and seed are constitutive; code version and
  environment class are recorded and diffed but do not break
  comparability — otherwise a rerun after a code fix could
  never trigger a junction.
- **D-089-5 — Reach-back over existing run records:
  index-only.** Existing records receive index entries under
  legacy ids derived from their store paths, recoverable key
  components carried, `legacy — key partial` where components
  are unrecoverable; bytes untouched.
- **D-089-6 — Suite runs: bind at citation.** CI runs by
  GitHub run id + head SHA via the delivery-checker
  discipline; local evidence runs by a lightweight run
  record written by the citing stage's worker.

**Registry citation:** Spec 089 is registered in the VEXA
stack's improvement registry as the adoption of **IMP-0008**
(the owner's run-scoped results rule).

**T002 outcome noted:** the AEE assessor (aee 1.5.3, the
pinned CI-faithful venv) read the draft bundle as
**outcome: iterate** (91 failure modes; 20 claims below the
0.70 threshold; draft cap and stage cap binding by
construction) — the expected draft-stage reading, recorded
verbatim in `records/t002-note.md` with the assessment at
`records/t002-aee-assessment.json`. The owner's ratification
is the human act that carries the claims forward.

## Adopted grounding — the drafting brief's corrections, carried

The package's grounding record
(`records/directive-and-grounding-2026-11-04.md`) corrected
three assumptions of the drafting brief against the repo;
the ratification adopts the package with these corrections
as its grounding:

1. The run-record supersession precedent is the Spec 087 +
   Spec 088 **adoption** refreshes (commits `491f31c`,
   `3f30671`), not a Spec 088 S3/S4 act; git renders the 088
   refresh as renames because the result blocks are
   near-identical — the store-level fact (the superseded
   pair left the store, preserved in git history) is as the
   brief stated.
2. `compare_runs` is narrower than "dual-run comparison"
   suggests: it refuses same-candidate pairs and cross-build
   pairs by construction. The junction rule is therefore
   specified as a generalization beside it (with
   `run_settling.py`'s `_first_divergences` as the
   localization seed), not a configuration of it.
3. Backend experiment jobs already carry execution-minted
   ids (`uuid4().hex[:12]` in `create_job`); what is missing
   is the repo-side **citation binding**. The spec's claim
   for that surface (C089-8) is a binding claim, not a
   minting claim.

## A tension inside C089-18, named

C089-18 states that the spec's only ledger change is its
adoption intake append (plus the regeneration of the
generated layers that append forces), and FR-089-16 states
the same bound as a requirement. This append is that
change — by design: it is the framework's own intake of
this spec's claims, performed exactly as Spec 086's
adoption appended its own 21, Spec 087's its 17 (the
C087-14 precedent), and Spec 088's its 19 (the C088-15
precedent, named the same way in that adoption record). The
claim's operative scope is the build stages' treatment of
Indus claim content: **no Indus claim's status, stage, or
score moved in this motion** — the validator's mirror
counts and the reconciliation test prove the append is
additive only, the freeze records are untouched, and the 20
appended entries are this spec's own governance claims at
draft/created.

## Why this motion appends to the ledger

Under the Winning Combination discipline (one claims
ledger, sole entry point, every claim enters through
intake), an adopted spec's bundle is appended through the
sanctioned intake path — and the bundle-reconciliation test
(`test_p2_reconciliation`) requires the ledger's bundle
population to equal the bundles on disk, so an
adopted-but-not-appended bundle fails CI. This is the same
self-intake Specs 086, 087, and 088 performed at their
adoptions.

## Intake path used (T004b)

`tools/ledger/import_bundle.py --spec
specs/089-run-scoped-results --date 2026-11-04` — Spec 086
intake route 2 (T103): `build_bundle_entries` forms the
entries and `append_entry` validates and appends each one
(schema, fingerprint recomputation, provenance, duplicate
refusal, verified append-only write). No entry was
hand-written and claims.jsonl was never hand-edited.

Output (verbatim): **20 appended, 0 already canonical, 20
propositions** — no refusal, no duplicate, no schema
failure.

Entry formation mirrors the migrated bundle convention:
id `089-run-scoped-results/C089-N`; population `bundle`;
a single `source_of_record` source naming this spec's
`aee-claims.json`; status/stage mirrored from the bundle
record (`draft` / `created`); falsifier carried from each
record's `falsification_tests` (all 20 carry one); the
appended entries carry an empty `sign_refs` list (the
ledger's only sign_refs-bearing entry remains the
pre-existing one).

## Ledger before / after

- Before: **907 lines**, SHA-256
  `9f8144c3fa73d7cfa4ffd02d3b6c23c3ea9e0c1e164e9497232dd2842e0a022c`
  (1,888,902 bytes).
- After: **927 lines**, SHA-256
  `b442ce7e5825e938fbd4bc0033bcb0582b37c71fe724a55f4584b5a4d5213712`
  (1,923,481 bytes).
- Append-only verified byte-wise: the after file's first
  1,888,902 bytes hash to the before file's SHA-256.

Validator output (verbatim):

```text
Ledger validation — /home/hatch/workspace/glossa-run/system-coupling-audit/glossa-indus/ledger/claims.jsonl
schema: ledger-schema v1 (glossa-indus/ledger/ledger-schema.json)
fingerprint rules: spec029-phase-i-v1
lines: 927
entries by kind: annotation 31, claim 896
claims by population: bundle 873, extracted 23
falsifier coverage: 887 of 896 claim entries carry a falsifier
falsifier coverage by population: bundle 873/873, extracted 14/23
does_not_establish coverage: 755 of 896 claim entries
aee_state present: 0 of 896 claim entries
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

## The taxonomy precondition (a mechanical necessity, recorded before the chain)

The generated chain could not start the way Spec 088's
did. The first gated publication attempt
(`generate_matrix.py --gated`) did not reach a gate verdict
at all: the gate's V10 derivation crashed on the grown
ledger with `KeyError: '089-run-scoped-results'`
(`ledger_gate.py`, `_derive_program_map`: the recomputation
resolves every claim's home spec through the taxonomy, and
the new spec had no assignment). Nothing was published —
the attempt died inside `run_gate`, before any artifact
write, and every published artifact's hash was verified
unchanged afterward.

The amendment the gate's own coverage rule requires was
therefore executed before the chain: one study row added
to `glossa-indus/map/program-map-taxonomy.json` —
`089-run-scoped-results` under **Program infrastructure /
Governance, lifecycle & generated layers**, beside Specs
084, 086, 087, and 088. The registered version string
(`program-map-taxonomy v1`, pinned identically in the
definitions document, the builder, and the gate's own
copies) is unchanged: adding a study assignment is the
file's normal operation under v1, and a version change
would itself be a program-map-defs amendment, which no
adoption motion may make unilaterally. The taxonomy
carries grouping only — no standing of any kind was added
(C2 holds).

## Regeneration of the generated layers (T004c)

With the taxonomy amended, the precedent's chain executed
in its order. The first gated attempt
(`generate_matrix.py --gated`) now ran and went **gate
RED: 16 PASS / 8 FAIL / 2 NOT-RUN, RESULT: FAIL**, and the
published artifacts stayed byte-untouched (verified by
hash). The eight failures are the precedent's four plus
the program-map layer Spec 088's stages added since: V2
claims-by-status (map header leg), both V5 map legs, V8
settling canonicals, and the four V10 legs (program-map
bytes, find list, stamp freshness, page). The settling
chain refresh below resolved V8; the ordering then closed:

1. Matrix regenerated by the pure builder
   (`generate_matrix.py`; `--check` → CHECK: MATCH):
   matrix.json `4b40d126…` → `2509201b…` (767,393 bytes),
   matrix.md `470570ab…` → `daf9352f…`.
2. Program map regenerated by the pure builder
   (`tools/map/generate_program_map.py`; `--check` → OK):
   program-map.json `672cfb78…` → `f329b7bd…`,
   program-map-finds.json `7a6cd137…` → `1b6fb256…`,
   program-map.html `b99d636e…` → `887bfad1…`.
3. Map published through gated publication
   (`generate_map.py --gated`): gate **25 PASS / 0 FAIL /
   1 NOT-RUN, RESULT: PASS**; map-data.json `b419f90b…` →
   `c8d920e2…` (4,715,239 bytes).
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

Census after regeneration: 896 claims (bundle 873,
extracted 23); falsifier coverage 887/896; matrix 1,419
cells (supports 1,412 / opposes 7 / constrains 0); 4,258
citations tied under V4; map 1,540 elements, 1,419 edges;
program map 896 claim nodes (open 887 / negative 6 /
positive 2 / closed_other 1) and 90 study nodes (open 61 /
unjudged 28, +1 restricted name-only), judgment calls 0,
find list unchanged at 38 (28 bundle-less studies, 9
extracted null falsifiers, 1 restricted node).

## The settling chain refresh (the precedent's procedure, executed in full)

As at Specs 087's and 088's adoptions, matrix + map
regeneration alone could not return the gate to green: the
settling layer's registered pins name the ledger build they
were derived over. Every refresh below was executed only
after independent recomputation proved the expectations
unchanged. Nothing was force-fit and no gate check was
loosened.

1. **Canonicals provenance pin (V8).**
   `glossa-indus/ledger/settling-canonical.json` governs
   one pinned build by design. Before the pin was touched,
   `tools/ledger/run_settling.py verify-canonicals` was
   run over the new build: **6/6 registered canonicals
   reproduce**, field-for-field. Only then was the pin
   refreshed (provenance.ledger and the comparison's
   inputs.ledger_sha256: `9f8144c3…`/907 → `b442ce7e…`/927),
   with the re-derivation recorded in the file itself
   (`re_derivations[2]`, 2026-11-04: act, reason, both
   pins, verification). Expectations did not change; the
   semantics (glossa-settle-1) did not change, so no new
   semantics version is registered.
2. **T405 run records (map builder D-D refusal).** Both
   T405 scenarios were re-executed through
   `run_settling.py run` under the Stage 4 protocol (same
   candidates, same 286-sign full-frame scope): new
   records `t405-incumbent-over-full-frame--c78f3e07ec82
   .json` (SHA-256 `89fb596c…`) and
   `t405-full-register-over-full-frame--fb1697b3f6de.json`
   (SHA-256 `018c99ca…`). Their result blocks are
   byte-equal to the superseded runs'; the only differing
   field is the pins block. The two superseded old-build
   records (`…--5b1d1c866b0e.json`, SHA-256 `a5597836…`;
   `…--070f8f0f476f.json`, SHA-256 `ab3db0ec…`) were
   removed from the store, because the builder's
   registered rule admits no stale-pinned record there;
   both stand preserved in git history and are cited here
   with their hashes.
3. **Filed dual-run comparison (map builder D-D
   refusal).** `specs/086-winning-combination-adoption/
   records/stage-4-dual-run-comparison.json` was re-filed
   from the new runs via `run_settling.py compare`, after
   verifying its content is identical to the previous
   filing except the ledger pin: SHA-256 `fce929e6…` →
   `d5997c14…`; the comparison over the new pair compares
   1 claim with **per_claim_divergences: []** and Stage
   4's coverage numbers (94 / 286 assigned, 0 conflicts).
   The Spec 088 adoption record's citation of `fce929e6…`
   stands as the historical citation of the filing as made
   at that adoption.

**This refresh under the discipline this spec retires —
stated plainly.** The chain above executes under the
pre-089 precedent: the content-addressed run store, in
which a superseded record leaves the store and survives in
git history. Spec 089's own T004(c) names this refresh
"the last pre-spec refresh" executed "under the old
content-addressed discipline," and this record confirms
that is what happened — the adoption does not pretend to
satisfy the spec it adopts. Under D-089-5's index-only
reach-back, Stage 5's T501 builds the legacy index over
exactly these generations (its text names the T403
originals and the 087, 088, and T004 adoption-refresh
generations), at which point the records superseded here
receive their `legacy — key partial` index entries like
the rest. From Stage 2 onward, supersession on the
settling surface is a labeled index relation and records
no longer leave the store (FR-089-02).

## Test maintenance — census re-pins

Spec 086's Stage 5 tests and the gate battery pin the
artifact census of their build; the append moved every
census number by exactly the 20 claims (each new claim
adds one supports cell: its own document's). The pins were
re-set to the regenerated artifacts' actuals — every value
below recomputed from matrix.json / map-data.json /
program-map.json / the gate's own evidence text, none
adjusted to fit:

- `backend/tests/test_spec086_map.py`: claims_total 876 →
  896 (3 sites); draft 852 → 872; status sum 876 → 896;
  ledger_lines 907 → 927; claim elements 876 → 896;
  elements total 1,520 → 1,540; supports 1,392 → 1,412
  (2 sites); loads 876 → 896; falsifier census 867/876 →
  887/896; AEE census 876 → 896 (2 sites);
  claims untouched by any run 875 → 895; the scoped-404
  leak marker `"876"` → `"896"`.
- `backend/tests/test_spec086_ledger_gate.py`: "1399
  matrix cells" → "1419 matrix cells"; "876 claims counted
  across 8 statuses" → "896…"; "1399 map edges by relation"
  → "1419…"; "supports 1392, opposes 7, constrains 0" →
  "supports 1412, opposes 7, constrains 0"; "876 claim
  nodes" → "896 claim nodes"; "89 study nodes" → "90 study
  nodes".
- `frontend/e2e/system-graph.spec.ts`: "876 claims in the
  ledger" → "896 claims in the ledger".

No assertion was weakened, skipped, or deleted; each pin
still asserts the exact census, now of the current build.
Anchors (287, strict 94), `no_stage_recorded` (15), the
find-list pins (28 bundle-less, 1 restricted), and the map
header's nearest-dated items did not move.

## Targeted test results

Per the precedents' surface, in the CI venv
(`~/workspace/venvs/glossa-ci`) with TMPDIR on disk, seven
files: test_spec086_ledger_migration.py (including
`test_p2_reconciliation`, the bundle-reconciliation test
of T004d), test_spec086_ledger_gate.py,
test_spec086_map.py, test_spec086_matrix.py,
test_settling_canonical.py, test_spec086_ledger_intake.py,
test_spec088_program_map.py — **152 tests in total**. The
first run showed 9 failed / 143 passed: every failure a
census literal of the old build differing by exactly the
append's arithmetic (enumerated above), no ERROR and no
flake signature. After the re-pins, the two affected files
were re-run in full: **69 passed**. The seven-file surface
therefore stands at 152 passed in its final state. Ruff on
the two touched Python test files: all checks passed.
After every suite run, `git status` was checked; the final
tree carries only this motion's intended changes (no
extracted-claims or report rewrites persisted).

## Naming — no departure this time

Unlike Spec 088's adoption (whose brief moved it to
`feat/088-adoption` / `specs/088-full-picture-map-gap-
register/`), this motion executed under the names the
package itself carries: branch `feat/089-spec-package`,
directory `specs/089-run-scoped-results/`. The package
files were copied byte-identical, so no internal reference
stands at odds with the executed names.

## Claims assessed at adoption (adoption scope)

- **C089-18 — adoption leg holds.** The ledger diff of
  this motion is exactly the 20-entry intake append this
  record describes, plus the regeneration of the generated
  layers that append forces; no other ledger change is
  attributable to this PR, and no Indus claim's
  status/stage/score moved. The claim's build-stage scope
  is not yet assessed.
- All other C089 claims are **not yet assessed** — their
  falsifiers execute against stages S1–S5, which have not
  started.

## Stage 0's "does not establish" lines (from tasks.md)

- T003: *This does not establish: approval of any later
  stage's output — each lands on its own evidence.*
- T004: *This does not establish: anything about the
  appended claims' truth — only that the ledger grew by
  the sanctioned path and the generated layers match it.*

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
