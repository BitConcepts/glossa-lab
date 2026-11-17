# Spec 095 — Stage 2 record: validator and synthetic containment

Date: 2026-11-16. Branch `spec/095-s2-validator-containment`, base
`3de9bed4` (the Spec 095 Stage 1 merge). Claims discharged by this
stage: **C095-5** (T201–T203) and **C095-6** (T204). Built and tested
on the mini-server in a fresh full clone; the live origin was not
touched, the backend was not restarted, and the research loop was
not run.

## T201 — the five-validator consumer census, completed

Method, stated so the census can be re-run: (1) mechanical registry
enumeration on this tree (import `glossa_lab.experiment_graph`;
556 registered nodes; registry build report ok); (2) import and
call-graph greps over `backend/`, `frontend/src/`, `tools/` and
`cloud/` for every v1 and v2 module name, entry point and script
name; (3) an AST import scan for the synthetic module (T204). The
Stage 0 census was re-verified for the three families it completed
(phonotactics, site_stats, crosswalk): it holds on the current tree.
corpus_frames and replay076 are brought to the same standard below.

One registry fact the census turns on: the Spec 087 `legacy` flag
is **not** a guard. It curates the builder palette only; resolution
and execution are unchanged ("Flagging changes nothing about
resolution or execution: ATOMIC_NODES keeps every entry"). All four
v1 nodes below were already legacy-flagged and remained fully
executable before this stage. The registry total is 556 before and
after this stage: the guard changes no registration.

**phonotactics.** v2 (`glossa_lab/phonotactics_v2.py`) consumers:
its repair test only (`tests/test_repair_phonotactics_v2.py`). v1
consumers: the node `IndusPhonologicalGap`
(`experiment_graph_phase56_61.py`, runs
`scripts/phase58_phonological_gap.py`); the node
`IndusProvenanceRecompute` (phase108 script, below); the library
routines `provenance_audit.phonotactic_check`, which dynamically
loads the Phase-58 script module and calls
`analyze_phoneme_inventory`, called by the Phase-108 and Phase-109
step-5 scripts; and `scripts/phase109_step5_rebase.py` (historical
script). Test-only, historical: the Phase-113 and Phase-115 battery
tests load the Phase-58 script **as a module** and use
`is_valid_dravidian_initial` as a frozen battery validator; they do
not call the v1 analysis entry points.

**site_stats.** v2 (`glossa_lab/site_stats_v2.py`) consumers: its
repair test only. v1 consumers: the node `IndusSiteStratification`
(`experiment_graph_phase67_73.py`, runs
`scripts/phase69_site_stratification.py` and formats the script's
chi-squared p-value into its output text); the node
`IndusProvenanceRecompute` via `provenance_audit.site_invariance`,
which dynamically loads the Phase-69 script module's chi-squared
machinery; `scripts/phase109_step5_rebase.py` (historical).

**crosswalk.** v2 (`glossa_lab/crosswalk_provenance.py`) consumers:
its repair test, and the standalone repair generator
`glossa_lab/generate_crosswalk_provenance_overlay.py`. v1 consumer:
the node `IndusCisiCrosswalk116` (`experiment_graph_phase91_100.py`,
runs `scripts/phase96_cisi_crosswalk.py`). Data-only touches, not
validator consumers: `api/foundation_check.py` counts entries in
the v2 crosswalk JSON; `data/indus_sign_crosswalk.py` loads the v2
JSON (no code consumer); `calibration_scoring.py` references the v1
crosswalk CSV (test-only consumer); the phase125/127/128/131/398
runners import the v1 crosswalk **data** module (frozen study code
consuming data, not the validator routine).

**corpus_frames.** v2 (`glossa_lab/corpus_frames.py`) consumers:
its repair test only. v1: **no node and no live path exists.** The
v1 "compressed frame" is a convention (drop `000` placeholders and
`*`-marked tokens, then count positions), embodied in the frozen
Spec 076 pilot (`specs/076-projected-constraint-corpus-model/pilot/
pilot_run.py`) and described in `phase116_harmonization.py`
(historical runner). Nothing in the live application builds frames
by the convention.

**replay076.** Consumers: its repair test only. The wrapper is
invoked by nothing in the live application; `pilot_run` references
exist only in the test and in the wrapper's own docstring. The
wrapper is internally guarded (input hash gate, new-output-dir
rule, frozen-tree re-hash after the run).

## T202 — the four v1 node paths discharged: mechanically guarded

Disposition for all four paths (phonotactics, site_stats,
crosswalk, and the provenance path that carries the first two):
**mechanically guarded**. Reasoning, on the record:

- Migration rejected. The v2 modules replace individual routines,
  not the whole phase analyses the nodes run; a migration would be
  a new study implementation. It would also change computed
  results by construction (the v1 numbers are the defect the
  repair corrected), so the result-equivalence condition for
  migration cannot be met.
- Retirement rejected. The registry census is pinned at 556 by
  Spec 087's census of record (registry changes only by recorded
  acts); retiring four nodes would amend another spec's pin and
  break resolution of stored graph records that reference these
  node ids.
- The guard meets C095-5's bar (no v1 routine executable
  unguarded in a claim-bearing path) with the smallest blast
  radius: node ids, names, categories and declared inputs/outputs
  are unchanged, and the registry census is untouched.

Guard construction (new module
`backend/glossa_lab/legacy_validator_guard.py`), six guarded paths:

- the four node functions return `refusal_result(...)`: a labelled
  refusal dict (`error`, `text`, and a `legacy_validator_refusal`
  block naming the path, node id, v1 routine, v2 successor, claim
  C095-5 and this stage), carrying no v1-computed values. The
  Phase-91/100 and Phase-108 table-driven builders special-case
  their guarded node ids; the Phase-56/61 and Phase-67/73 node
  functions return the refusal directly. The four node
  descriptions carry the GUARDED note.
- `provenance_audit.phonotactic_check` and
  `provenance_audit.site_invariance` raise
  `LegacyValidatorRefused` at entry; their bodies are retained
  below the raise, for the record, unreachable. Their historical
  script callers (Phase-108/109) now fail if run; that is the
  intended containment, recorded here.
- the three v1 scripts (`phase58_phonological_gap.py`,
  `phase69_site_stratification.py`, `phase96_cisi_crosswalk.py`)
  refuse direct execution as the first statement of `main()`
  (self-contained `SystemExit`, since the scripts run standalone
  via subprocess). Module import is unaffected.

Result equivalence: no surviving live path's computed results
change. The guarded paths produced v1 validator outputs, which is
exactly what is now refused; every other node and loader is
untouched. The Phase-113/115 frozen batteries, the only test
consumers of Phase-58 module functions, pass unchanged:
`is_valid_dravidian_initial` and `analyze_phoneme_inventory` are
not modified. corpus_frames and replay076 need no act: no live
path exists for either (T201), and replay076's wrapper guards
stand as built.

## T203 — the planted legacy-rule pinning test

`backend/tests/test_spec095_validator_pinning.py` (16 tests) runs
in the normal suite. What it plants, as fixtures inside the tests
(never live code changes):

1. a temporary node whose function calls
   `provenance_audit.phonotactic_check`, registered through the
   registry's own funnel and executed through the registry: the
   guard raises `LegacyValidatorRefused` before any v1
   computation; the registry entry is removed again in a
   `finally` block.
2. a direct invocation of the Phase-58 v1 script through the
   phase modules' own script runner, bypassing the guarded node
   function: the runner surfaces the script's labelled refusal,
   never v1 output.

The file also pins: the guard registry covers exactly the four
paths of record; the four nodes remain registered and return
labelled refusals with none of the keys a genuine v1 run would
produce; both provenance-audit entry points raise directly; the
three v1 scripts refuse direct execution (subprocess, non-zero
exit, refusal on stderr); and the non-validator surface of
`provenance_audit` (reading normalization, coverage) is
unaffected by the guard.

## T204 — synthetic containment

Census method: AST import scan over `backend/glossa_lab`,
`backend/scripts` and `backend/tests`, pinned by
`test_consumer_census_is_complete` (a new import consumer fails
the suite until this census is updated), plus a reference scan
for non-import mentions. Consumers of
`backend/glossa_lab/data/indus_public_corpus.py`:

- `glossa_lab/corpus_seeder.py` — seeded at application startup
  under the id `indus_synthetic`; the display name and the seed
  metadata status both carry the synthetic marking.
  Classification: demonstration seed, labelled.
- `glossa_lab/experiment_graph.py` — the `BuiltinCorpus` node;
  see Finding 1.
- `glossa_lab/analyze_script.py` — demo analysis loader; returns
  the label "Indus (Synthetic — Yadav 2010 / Fuls 2014
  parameters)" beside the data. Classification: demonstration,
  labelled.
- `glossa_lab/experiments/_legacy/` (five modules:
  tier5_indus_decipherment, progression_report,
  tier5_indus_readings, indus_structural_atlas,
  remaining_experiments) — legacy demonstration code, no live
  consumers. Classification: legacy demonstration.
- tests: the Spec 095 Stage 1 corpus battery and this stage's
  containment tests. Classification: test.

Reference-only (no import): `glossa_lab/corpus_catalogue_seeder.py`
names the module in its catalogue entry's `local_module` field;
the entry's name and description carry "synthetic"
(classification: catalogue, labelled).
`scripts/foundation_check.py` checks the module file's presence
only and consumes no data.

**Finding 1 (contained).** The core node `BuiltinCorpus`
(palette-live, not legacy) serves the synthetic prototype as its
`indus` corpus with **no synthetic label in the output**, beside
sibling branches serving real CISI and M77 data — synthetic
material reaching an experiment path unlabelled. Containment
(mechanical and small): the `indus` branch now adds a
`corpus_status` string to the output ("SYNTHETIC — generated
prototype (indus_public_corpus), calibrated to published
statistics; not inscription data"); the sequences served are
unchanged, and the existing node tests pass unchanged. The
node's demonstration role itself is pre-existing and unchanged.

**Finding 2 (removed).** `glossa_lab/data/indus_corpus_v2.py`,
the claim-bearing V1 loader, named the synthetic prototype as
its Tier-3 "last resort" fallback. The tier was **dead code**:
it imported `indus_public_corpus.load_corpus`, a function the
synthetic module does not define, and the `ImportError` was
swallowed. The hazard was latent: adding that one function to
the synthetic module would have silently revived an unlabelled
synthetic fallback in a claim-bearing loader (the loader's
returned data carries no label; the tier is recorded only in a
status global). Containment: Tier 3 is removed, the loader's
docstrings corrected, and an AST pin asserts the loader has no
synthetic import. Stage 1's `load_corpus_verified` never fell
back and is unchanged.

**Finding 3 (noted, not acted on).** The same loader's Tier 2 is
likewise dead code: it imports `load_corpus` from
`indus_cisi`, which defines only `_load_corpus()`; the
`ImportError` is caught. Tier 2 names real CISI data, not
synthetic material, so it sits outside C095-6; repairing or
removing it would change loader behaviour and is left to a
future stage. Recorded here so the loader's documented fallback
chain is not mistaken for a live one: today only Tier 1
(identity-enforced since Stage 1) and `load_corpus_verified`
serve data.

Labelling, machine-checked (not comment-only): the synthetic
module now carries `SYNTHETIC = True`, `CORPUS_KIND =
"SYNTHETIC"` and `SYNTHETIC_LABEL`, and `corpus_statistics()`
reports `corpus_kind` and `synthetic` keys alongside its status
string. The containment tests assert the labelling at every
surface: module constants and statistics, the seeder's name and
metadata, the catalogue entry's name and description, and the
`BuiltinCorpus` output.

Planted synthetic-as-real fixtures
(`backend/tests/test_spec095_synthetic_containment.py`, 8 tests):

1. no-real-tier plant: with the research export missing and the
   CISI tier unavailable, while synthetic data exists and is
   importable (the exact condition the removed Tier 3 named as
   its trigger), the claim-bearing loader returns an empty list
   with tier "empty (no corpus data available)" — never
   synthetic data.
2. identity plant: synthetic inscriptions written out as a
   corpus file and presented to
   `corpus_identity.enforce_file_identity` under the strict
   corpus's identity of record (`indus_v3_firestore_strict`):
   refused with `CorpusIdentityError`.

## Test actuals

- New tests: 24 passed (validator pinning 16, synthetic
  containment 8).
- Targeted regression batch, 18 files (Spec 087 registry
  integrity and palette curation, provenance audit, atomic
  nodes, evidence atomic nodes, experiment graph, graph
  experiments, Phase-113 and Phase-115 batteries, the five v2
  repair tests, the Stage 1 corpus battery, Phase-116
  harmonization, Spec 086 stub disposition, research loop):
  409 passed, 3 skipped, 0 failed.
- Full backend suite (CI invocation; GPU files ignored; the
  phase392 deterministic test deselected locally by its plain
  nodeid, CI authoritative; two-part run split at
  `test_spec086_ledger_gate.py`, union complete):
  part 1 (all tests except the ledger-gate file) 2,865 passed,
  66 skipped, 1 deselected in 617.57s; part 2
  (`test_spec086_ledger_gate.py`) 23 passed, 44 skipped in
  572.98s; union 2,888 passed, 110 skipped, 1 deselected,
  0 failed. Suite side-effects in tree (extracted-claims JSONs,
  one claim report, `outputs/partial_loop_result.json`) were
  restored before committing.
- Ledger gate, run sequentially on a quiet tree:
  `--all`: `summary: 29 PASS / 0 FAIL / 1 NOT-RUN`, `RESULT:
  PASS`. `--regen`: `summary: 32 PASS / 0 FAIL / 0 NOT-RUN`,
  `RESULT: PASS`. The standing profile exactly. In-tree
  regenerations restored after each mode.
- Ruff: clean on all 14 changed and new code files.

## Deviations

- One broad restore command during suite side-effect cleanup
  (`git checkout -- glossa-indus backend`) also reverted this
  stage's own backend edits. The patch set was re-applied from
  its recorded patch script (all 21 exact-match replacements
  re-applied cleanly against the pristine files), the new tests
  were re-run green (24 passed) before the gates, and the final
  commit's file list is verified from `git show --stat`. No
  state was lost.
- The disposition choice (mechanical guard for all four paths,
  over migration or retirement) is a judgment the brief left to
  the stage; the reasoning is recorded under T202 and follows
  the C095-5 falsifier and decisions D-095-1..6.
- Finding 3 (the loader's dead Tier 2) is recorded, not fixed:
  it names real data, sits outside C095-6, and any change to it
  alters loader behaviour.
