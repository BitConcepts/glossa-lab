# Stage S1 record — registry integrity (Spec 087)

**Stage:** S1 (tasks T101–T106). **Branch:**
`feat/087-s1-registry-integrity`, built on main `8445da1f`
(PR #487, the Spec 087 package + adoption intake).
**Date:** 2026-11-02. **Seat:** build worker; the parent
gates and merges.

## What was built

### T101 — Registry build records failures and can fail fast

`backend/glossa_lab/experiment_graph.py` no longer swallows
plugin import failures behind a lone warning and no longer
overwrites duplicate ids silently:

- Every plugin import block (145) and every registration
  loop now routes through two helpers inserted beside
  `ATOMIC_NODES`: `_record_registration_failure(label, exc)`
  (records the failure and logs it at ERROR) and
  `_register_node(def)` (records a duplicate id — id, both
  defining modules — and logs it at ERROR; the later
  definition still wins at runtime, so lenient behaviour is
  unchanged).
- After the last registration block, `_finalize_registry_build()`
  runs: a complete build logs its census at INFO; an
  incomplete build logs ERROR, and in strict mode raises
  `RuntimeError`, so the application does not start over a
  silently shrunk registry. Strict mode:
  `GLOSSA_REGISTRY_STRICT` (1/true/yes/on) wins when set;
  otherwise strict everywhere except `GLOSSA_MODE=installed`
  (production keeps the lenient path — it surfaces the
  failure as an ERROR log plus the report below instead of
  refusing to start).
- `registry_build_report()` returns the build snapshot
  `{ok, registered, failures, duplicates, strict}`.

**Surface choice (spec left it open; smallest visible one):**
a new endpoint `GET /experiment-graphs/registry-health`
returns `registry_build_report()`. The catalog endpoint
returns a bare list (its shape is S2's to change) and the
Spec 082 health payload is pinned to exactly six fields, so
neither could carry the report. Verified live against a
locally started backend: `{"ok":true,"registered":517,
"failures":[],"duplicates":[],"strict":true}`.

### T102 — Registry-completeness pin and self-check

New module `backend/glossa_lab/registry_check.py`:

- `loader_plugin_imports()` AST-parses `experiment_graph.py`
  and returns the (module, defs-functions) pairs the loader
  itself imports — the expected module list is derived from
  the loader, so the check cannot drift from it. Expected
  plugin modules: **144**.
- `collect_plugin_nodes()` imports each module and calls
  exactly the loader-imported defs functions, yielding the
  produced node ids per source and any module error by name.
- `duplicate_node_id_literals()` AST-scans every
  `experiment_graph*.py` for `AtomicNodeDef` id literals
  defined in more than one place.
- `registry_self_check()` recomputes the census and compares
  it with the built `ATOMIC_NODES`;
  `assert_registry_complete()` raises naming every defect.

Pin fixture `backend/tests/fixtures/spec087_registry_census.json`,
generated from the census evidence (records/census-evidence.md
Table 1) and verified against the running registry:

- **registered total: 517**
- **categories: 66** (largest: Indus Decipherment 319;
  CTT / Constraint Topology 25; Decipherment 13; Analysis 9;
  Indus Decipherment (Phase 322–362) 8)
- **plugin modules: 144**; core definitions: 42.

### T103 — Shadowed pairs: NAMED FINDING (pairs differed)

`IndusPhase254SemanticConstraint`, `IndusPhase255CommodityPhonemes`,
and `IndusPhase256LEExtension` were each defined twice:
in `experiment_graph_phase248_253.py` (the dead definitions)
and in `experiment_graph_phase_misc_gaps.py` (the live ones —
imported later, so they won). **The pairs are NOT
functionally identical.** Both sides run the same three
scripts (`backend/scripts/phase254_semantic_constraint.py`,
`phase255_commodity_phonemes.py`, `phase256_le_extension.py`),
which write `outputs/phase25X_*.json` at the repo root, and
all three report files exist there. The differences:

| Aspect | Dead (phase248_253) | Live (misc_gaps) |
|---|---|---|
| subprocess timeout | 120 s | 900 s |
| working directory | repo/backend | backend |
| report lookup | repo `outputs/` only | repo `outputs/`, then `backend/reports/` |
| return value | first-10-keys spread + stdout tail (800 chars) | the full report JSON |
| output ports | rich, typed (n_upgraded, upgrade_log, top_enrichments / commodity_matches / le_backed_medium) | one port: `report` (object) |
| names/descriptions | detailed; match the scripts' actual content (motif enrichment chi2>6.64, lift>2.0; 16 commodities to PDr names; LE+DEDR+McAlpin corroboration) | shorter; partly inaccurate (254 described as testing "semantically coherent fields within inscription slots", not motif enrichment) |

The rich output ports of the dead definitions do correspond
to real keys in the actual report fixtures, so the dead
definitions were in that respect the more faithful
description of the same scripts. No test, document, or
experiment record in the tree references these ids (they are
used by no live graph).

**Disposition (per the stage rule for differing pairs — do
not guess):** the currently-live misc_gaps definitions are
kept unchanged (zero behaviour change for anything that
could have run); the three dead definitions are deleted from
`experiment_graph_phase248_253.py`, whose module docstring
now records the resolution. The description/port fidelity
gap in the kept definitions is recorded here as a finding
for a later stage or an owner ruling; S1 does not swap live
behaviour. The module now yields exactly 5 definitions
(phases 248, 249, 250/251, 252, 253).

Guards added: the registry build records + ERROR-logs any
duplicate registration (T101), and the suite pins both the
AST literal scan (no id literal defined twice anywhere) and
the runtime provenance of the three ids (their compute
functions' module is `experiment_graph_phase_misc_gaps`).

### T104 — Palette failure surface

`ExperimentBuilderView` now loads the catalog through a
`loadCatalog` callback that records failures in a
`catalogError` state. On failure the palette renders a named
error box (`data-testid="palette-error"`, `role="alert"`:
"Node palette failed to load" + the error message + a Retry
button wired to `loadCatalog`) instead of the silently empty
list the old `.catch(() => {})` produced. Minimal change in
the file's existing styling; no redesign.

### T105 — Rename: `node_registry.py` → `study_node_registry.py`

`git mv backend/glossa_lab/node_registry.py
backend/glossa_lab/study_node_registry.py`; the sole importer
(`main.py`) updated; the module docstring retitled with a
rename note. Endpoint path and behaviour unchanged
(`GET /node-registry/{node_type}/{ref_id}`), verified live
and by test. Tree-wide, the only remaining references to the
old module name are in this spec package's own documents,
which govern the rename. The rename has **no user-manual
surface**: module names are internal, and the manual never
referenced the old name — so no manual edit belongs to this
item (C087-15's falsifier is satisfied by naming the reason).

### Manual (C087-15, S1 leg)

`docs/user-manual.md`, "Using the Builder": a short note
after the steps — if the palette list cannot be loaded, the
palette shows a "Node palette failed to load" error with a
Retry button instead of an empty list; an empty palette with
no error means the list loaded and the search matched
nothing. No Node Reference changes (S4 owns those).

## Test evidence

New suite `backend/tests/test_spec087_registry_integrity.py`
— **16 passed**. It covers: the 144-module pin; the census
pin (517 / 66 categories); the self-check and
`assert_registry_complete`; teeth runs (a fixture module
raising ImportError is named by the check and by the raised
assertion; a raising defs function likewise; a fixture
module producing an already-produced plugin id is caught as
a duplicate source); strict finalize raises on a recorded
failure while the lenient finalize reports without raising;
strict-gate env semantics (4 combinations); the AST
duplicate-literal guard returning empty; the shadow
resolution (provenance + the 5 surviving ids); the rename
(old module unimportable, both registries import in one
process, endpoint answers); and the registry-health endpoint
(ok, 517, no failures/duplicates).

Targeted backend run over every touched area (the S1 file
plus test_atomic_nodes, test_experiment_graph,
test_graph_experiments, test_evidence_atomic_nodes,
test_catalog): **164 passed, 1 skipped**.

Full backend suite, local, no `-x`: **2236 passed, 84
skipped, 1 failed, 1 error, 1 deselected** (282.7 s).

- The 1 failure is the known phase133 environmental baseline
  (`test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`
  — a missing local download; it does not fail CI), exactly
  the expected local baseline.
- The 1 error is the known tray teardown flake
  (`test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named`,
  sqlite "Cannot operate on a closed database" at teardown;
  seventh sighting of the family). Rerun standalone per the
  standing instruction: **14 passed**.
- The 1 deselected test is
  `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`,
  excluded after a first full run stalled inside it for
  ~35 minutes: it runs a pure-numpy permutation pipeline
  twice and is pathologically slow on this shared VM. The
  identical test on a pristine `origin/main` worktree also
  exceeded a 200 s timeout here, so the stall is a
  pre-existing property of this environment, not of this
  stage; CI (dedicated runner) is its authoritative run and
  was green on this code at PR #487. Every other test in the
  file ran in the full suite (its first test passed in
  sequence; the third is store-gated and skipped).

Frontend: `npm run build` clean (typecheck + bundle; the
rebuilt `frontend/dist` is committed with the change, per
repo convention — cf. PR #486). Playwright against a locally
started backend: `e2e/palette-error.spec.ts` **2 passed**
(500 → named error state with no categories rendered;
500-then-200 → Retry populates the palette and clears the
error); `e2e/experiment-builder.spec.ts` **23 passed,
1 skipped** (the conditional inspector test).

Ruff: `python -m ruff check backend/` — all checks passed.

## Gate-neutral statement

S1 changes no Indus claim content. The PR diff names no
files under `glossa-indus/ledger/`, `glossa-indus/matrix/`,
or `glossa-indus/map/` (verified from the branch diff
against `origin/main` before push). Test runs regenerated
some `glossa-indus/claims/extracted_claims/` files in-tree
transiently; they were restored (`git checkout --`) and are
not in the diff.

## Claim assessments (stage scope)

- **C087-1 — SUPPORTED at S1 scope.** The completeness test
  pins the 144 loader-derived module names and the
  517-by-66-category census; seeded broken modules fail the
  check loudly by name in the teeth runs; strict contexts
  raise at build finalization, production keeps the lenient
  path with an ERROR log and the registry-health report.
- **C087-2 — SUPPORTED at S1 scope.** One definition per id
  survives: the three dead definitions are deleted, the
  kept (live) definitions are pinned by provenance tests,
  the AST guard finds no duplicated id literal, and the
  build records any duplicate registration. The behaviour
  diff and the kept-definition reasoning are the named
  finding above; which definition is scientifically
  preferable is expressly NOT established (the claim's own
  DNE line).
- **C087-3 — SUPPORTED at S1 scope.** A failing catalog
  fetch renders the named palette error state with retry;
  the two Playwright runs above are the falsifier's test.
- **C087-16 — SUPPORTED at S1 scope.** The module is
  renamed, the endpoint answers unchanged (live + test),
  both registries import in one process, and no document
  outside this package points at the old name.
- **C087-17 — S1 leg only.** The claim's operative scope
  begins "after S2's re-pin"; the S1 leg is that the pin now
  exists and this stage itself moved no count (517 before
  and after; the dedupe removed only definitions the
  registry never held).

Assessments are recorded here, in the stage record, per
this repo's stage-record convention (Spec 086 stage records;
the Spec 087 adoption record's C087-14 assessment).
`claims.md` is not edited: its claim texts are the bundle
the adoption intake appended to the claims ledger, and the
Spec 086 migration reconciliation pins that population —
annotations belong in records, not in the bundle text.
