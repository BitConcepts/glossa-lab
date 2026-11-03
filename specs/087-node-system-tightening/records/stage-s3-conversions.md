# Stage S3 conversions record — PR-A: families F14 + F1 (Spec 087)

**Stage:** S3 (tasks T302, T303 in part). **Branch:**
`feat/087-s3-conv-a`, built on main `ec445f1a` (PR #490, the
merged S3 triage record). **Date:** 2026-11-02. **Seat:** build
worker; the parent gates and merges. This file is the standing
conversions record for Stage S3; later conversion PRs append
their entries here.

## The S3 conversion contract (parent ruling at the triage gate)

1. Registered ids never disappear in S3. A converted node's
   implementation becomes generic machinery driven by
   parameters; where the triage names a new generic primitive,
   register the primitive under its own generic id AND make the
   domain node's implementation delegate to it with today's
   domain specifics as parameter defaults.
2. In the same PR, each converted domain id takes the legacy
   flag (resolvable forever, not offered). The S2
   rule-vs-flags agreement test's pinned identity is amended
   on this record's authority to: flagged == census WRAPPER
   set ∪ {ids recorded converted or retire-flagged in the S3
   records}; the registry-health three-way counts and census
   pins re-pin accordingly (registered stays 517 + any NEW
   generic primitive ids the PR adds — counted explicitly).
3. Fixture output-equivalence per converted node: BEFORE
   changing an implementation, capture its outputs on the
   triage-specified fixtures from the current code and commit
   them as test fixtures; after conversion the same inputs
   must produce byte-identical outputs. A node whose
   equivalence cannot be proven stops that node's conversion
   (leave it unconverted, unflagged) and is reported, not
   forced.
4. After the PR's conversions, run the S2-style comparison:
   all 27 stored graphs executed; outputs byte-identical to
   the pre-change pin modulo the single named normalization
   (LanguageModel repr memory addresses).
5. F14 exception: relabel-only nodes get their
   category/classification corrected to GENERIC, implementation
   untouched, NO legacy flag, and a test pinning their generic
   status.

## What was built

### The generic machinery — `backend/glossa_lab/generic_loaders.py`

A new stdlib-only module (it imports nothing from glossa_lab,
so phase modules and the core list can both use it without a
cycle) carrying the two engines the F1 triage designs name:

- `json_corpus_loader_execute(inputs, params)` — the
  **JsonCorpusLoader** engine. A declarative `corpus_spec`
  (passed as a param, or assembled from flat params for
  standalone palette use) drives it: a fallback chain of file
  sources, first existing file wins — source kinds `json`
  (a top-level list unwraps to its first element; parse errors
  raise or return an error dict, per spec) and `csv_grouped`
  (rows grouped by a key column, ordered by a position column,
  sequences from a value column) — then one of three
  projections: `sequence_corpus` (field-mapped
  id/site/sequence/raw records with length filters and
  use_raw mode), `record_list` (records passthrough + a
  top-sites counter + a verdict template), `cache_summary`
  (record count + a named count field + metadata + a verdict
  template). Absent-source results and verdict texts are spec
  data rendered through `{placeholder}` templates.
- `dataset_record_loader_execute(inputs, params)` — the
  **DatasetRecordLoader** engine. A declarative `dataset_spec`
  names a bundled data module (`glossa_lab.data.*`), its
  getters (with parameter-shaped kwargs: from-param values
  with defaults, safe-int coercion, min/max clamps, or literal
  values), record filters (case-insensitive substring,
  any-of-list substring, equality — each active only when its
  driving param is non-empty), and an ordered output assembly
  (value / length / sum-of-lengths / distinct-count /
  top-N counter / param echo / literal / verdict template
  with conditional context entries). A module that fails to
  import or lacks a named getter yields the historical
  `{"error": "data module not available: …"}` result.

Both primitives are registered in the core list of
`experiment_graph.py`, category **Sources**, and are in the
palette: **JsonCorpusLoader** and **DatasetRecordLoader**
(registered 517 → **519**, core 42 → **44**).

### F1 — the six delegations

Each domain function below is now a thin wrapper that builds
its spec and delegates; its registered definition (name,
category, description, params schema, outputs) is unchanged,
and it takes the legacy flag in this same PR (contract item
2). Fixtures were captured from the pre-conversion code
(commit `b7094e7`, before any implementation changed) and are
replayed by `backend/tests/test_spec087_s3_conversions.py`.

| node | engine | spec home | fixture cases |
|---|---|---|---|
| M77InscriptionLoader (phase20) | JsonCorpusLoader, `sequence_corpus` | built at call time from phase20's own path resolvers | 11 |
| ContactCorpusLoader (phase22) | DatasetRecordLoader | `_CONTACT_DATASET_SPEC` in phase22 | 5 (hash) |
| MahadevanInscriptionLoader (phase29) | DatasetRecordLoader | `_MAHADEVAN_DATASET_SPEC` in phase29 | 4 (hash) |
| EPSD2NamesLoader (phase29) | DatasetRecordLoader | `_EPSD2_DATASET_SPEC` in phase29 | 3 (hash) |
| ICITCorpusLoader (phase29) | JsonCorpusLoader, `cache_summary` | built in the wrapper (path default is the node's own) | 4 |
| MathematicaEpigraphicaLoader (phase29) | JsonCorpusLoader, `record_list` | built in the wrapper | 3 |

Per-node notes:

- **M77InscriptionLoader.** The spec's fallback chain is the
  decoded report (`reports/mahadevan_texts_decoded.json`,
  JSON source, `site_coerce_str` on — the report's site codes
  are coerced to strings, the CSV's are not, exactly as the
  two original branches did) then the Holdat CSV
  (`csv_grouped`: group `cisi_number`, order `position`,
  values `letters`, site `site`). The node's historical
  defaults (label `indus_m77`, min_length 1, max_length 0,
  use_raw False) travel as the spec's `behavior_defaults`.
  The absent-corpus error text is the original, rendered from
  the chain's source/fallback names.
- **ContactCorpusLoader.** Getter call order, the two tablet
  filters (period substring, keyword any-substring), and the
  nine-key output assembly are the spec. The counters stay
  unfiltered getter results, as before. Its data files are
  absent from the repo (the getters raise FileNotFoundError
  by design since the 2026-10-26 hardening); the fixtures
  point the module's two path constants at committed
  synthetic files and clear the loaders' caches around each
  case.
- **MahadevanInscriptionLoader.** The `min_length` shaping
  (safe-int, default 1, clamped to ≥ 1 — so 0 and `"bad"`
  both land on the default behaviour) is a kwargs rule in
  the spec; the verdict is a template over the assembled
  outputs and the metadata dict.
- **EPSD2NamesLoader.** The POS equality filter, the
  `"(all)"` param echo, and the conditional ` (POS=…)`
  verdict suffix (a context entry rendered only when the
  param is non-empty) are spec data.
- **ICITCorpusLoader / MathematicaEpigraphicaLoader.** Each
  wrapper keeps its own path resolution (repo-root-relative
  default, overridable by the `data_path` param) and hands
  the engine a single-source spec whose absent result and
  verdict template are the node's historical texts.

**Two defects the fixtures caught before merge** (the reason
the contract captures first):

1. *M77 raw mode.* The first engine draft applied raw mode
   per record — only to records carrying a raw field. The
   captured `m77_primary_raw` case proves the original
   applies raw mode to every record of the JSON source: a
   record without raw text yields an empty sequence and is
   filtered out (2 of 4 fixture records survive, not 4). The
   engine now marks raw-mode applicability per source kind:
   JSON records yes, grouped-CSV records no (the CSV fallback
   ignores `use_raw`, as the original did).
2. *A doubled percent, preserved.* The Mathematica absent
   verdict's captured text contains `~30%% overlap` — the
   original f-string printed the doubled percent literally.
   The spec template carries `%%`, byte-identical. This is a
   pre-existing output quirk kept by the equivalence
   contract, not a conversion defect; fixing the text is a
   separate recorded act if the owner wants it.

### F14 — the two relabels (contract item 5)

Category strings only; implementations, names, descriptions,
and params schemas untouched; no legacy flag:

- **LegacyPhaseScriptRunner**: `Phase-16-19 / Migration` →
  **Experiments**. The `Phase-16-19 / Migration` category is
  retired (it held this one node).
- **PDFTextExtractor**: `Phase-20 / Sources` → **Sources**.

Interpretation recorded: the triage's remark that the
ScriptRunner "also takes a generic id" is discharged by the
generic classification itself. No alias id (e.g. a second
`ScriptRunner` registration for the same implementation) was
created — one implementation under two ids is the drift
S1/S2 removed, and the contract's F14 exception specifies
relabel only. Its fixture cases (no path / missing script /
a real subprocess run of a committed tiny script) pin the
unchanged behaviour; the PDF cases pin the no-path error and,
where PyMuPDF is installed, the extraction outputs (locally
the venv has no `fitz`, so the extraction cases assert the
node's `PyMuPDF not available:` error there and the fixtures
in CI, where pyproject installs pymupdf — the extraction
cases were additionally verified locally against a scratch
PyMuPDF 1.28.6 environment: 3/3 pass).

### The two M77 corpus pipelines — recorded, not unified

The triage (F1) forbids silently unifying the two pipelines
that both answer to "M77". After this PR both survive, as
separate parameterizations:

- **Pipeline A — MahadevanInscriptionLoader** →
  `glossa_lab.data.mesopotamian_contact.get_mahadevan_inscriptions`
  → `glossa_lab.data.indus_m77.get_corpus_inscriptions`: the
  bundled, versioned data module. Returns bare sign
  sequences; metadata comes from `get_corpus_metadata`
  (whose source line cites `reports/mahadevan_corpus_flat.txt`).
  Pinned by the `mahadevan_*` hash cases (1,669 inscriptions /
  5,361 tokens / 64 distinct at the default; 478 / 3,273 / 56
  at min_length 4).
- **Pipeline B — M77InscriptionLoader** →
  `reports/mahadevan_texts_decoded.json` (a generated report
  file, regenerated by `backend/scripts/decode_inscription_texts.py`)
  with the Holdat CSV as fallback: per-inscription
  id/site_code/length records. It feeds the three live graphs
  `indus_sa_dravidian_syllable`,
  `indus_sa_sanskrit_falsification`,
  `indus_validation_neg_controls`. Pinned by the `m77_*`
  cases over committed synthetic source files for both the
  primary and the fallback path.

Different provenance and update path, different record
enrichment, different consumers — recorded here per the
brief; no unification attempted.

### Counts — the re-pin (C087-17 act for this PR)

| | before | after |
|---|---|---|
| registered | 517 | **519** (+ JsonCorpusLoader, DatasetRecordLoader) |
| legacy | 359 | **365** (+ the six F1 conversions) |
| palette | 158 | **154** (−6 converted, +2 primitives) |
| core definitions | 42 | **44** |
| categories | 66 | **65** (`Phase-16-19 / Migration` retired) |

Per-category deltas: `Sources` 3 → 6 (two primitives +
PDFTextExtractor), `Experiments` 3 → 4 (LegacyPhaseScriptRunner),
`Phase-20 / Sources` 3 total / 0 legacy → 2 total / 1 legacy
(M77 converted, PDF relabelled out), `Phase-22 / Sources`
1 / 0 → 1 / 1 (Contact), `Phase-29 / Sources` 5 / 1 → 5 / 5
(the four phase29 conversions join the already-legacy
Phase29CorpusLoader). The migration data file
(`spec087_s2_legacy_ids.json`) gains the six ids under an
`s3_additions` key; the census pin fixture is re-pinned from
the live registry; the S2 agreement test now pins
flagged − wrapper-shape == {the six S3 ids} alongside the
original exception (ResearchLoopRunner, still unflagged).

## Equivalence and comparison results

**Fixture equivalence (contract item 3):** 36 captured cases
replayed post-conversion — **36/36 byte-identical** (full-mode
canonical-JSON equality; hash-mode canonical-JSON SHA-256 +
key set + verbatim fields), in
`tests/test_spec087_s3_conversions.py`, alongside the F14
generic-status test, the primitives-in-palette test, and the
converted-ids flag/provenance test. S1 + S2 registry suites
updated to the amended pins and green.

**27-graph comparison (contract item 4):** the S2 runner
(every node's result dict, canonical JSON, per-graph SHA-256)
was executed on a fresh worktree of origin/main `ec445f1a`
(pre) and on this branch (post). Two normalizations apply:
the contract's LanguageModel repr-address normalization, and
— new in this PR, an artifact of method, not of the change —
each tree's own root path, because node outputs embed
absolute paths and the two runs necessarily ran in two
different trees (S2's runs shared one tree, so the path
component never appeared there). Under both, **27/27 graphs
are byte-identical pre vs post**:

| graph | normalized sha256 (pre == post) |
|---|---|
| fuls_independence_suite | d669bedeea775d14a99805181e7e0509f92ddbea36bb55179a871cbafd675563 |
| fuls_nw_semitic_benchmark | 366fef925d4a7e701055eea38694264342c3a5a252419da58ba9ac8b0cdfaf71 |
| fuls_validation_suite | 107cd6e14c82604f44297e523cfdea1953bcadceac4b1750f890cc2e48048456 |
| generic_sa_multi_comparison | e0edbeb050a0898011c1915bc7eaf7feb09c692cacb8a8d227cf59f09c3adc1c |
| indus_anchor_sweep | fd82f1f152a345b9c9a4ba1edad0119e671caaae642fbfc6b7c4f692cce9ddad |
| indus_cgsa_cluster_analysis | 2d51ee50596a5b86fa95c53af96dffb87ab7540036a15d597f44a8ad2acdc48a |
| indus_cisi_anchored_10 | 26683194d84828247ac93ef952dd971e9ef5c1d5c916140395fd16f38ec4153f |
| indus_cisi_dravidian_vs_pali | 4526b2ba2ffbe7083b9ba4c56ed8407246563ff7632051e58e5dd9dec419c9ce |
| indus_cisi_dravidian_vs_sanskrit | 44d8f3333b044c386f3faf839a71e83f798bb36f44944110d8889faee3dd075a |
| indus_cisi_sa_dravidian_vs_nw_semitic | 9f0cfb7610c5cecec135e1dc6943baed6a7d091f8ef997384004a33e40b717f8 |
| indus_cisi_sa_dravidian_vs_sanskrit | eef14c7c07dcee28e08973a0a4450fbf00312736afce7def5c117553edcdfb69 |
| indus_cisi_structural | 6b5b303a8f450f28d7c1c98c4ff26fe3aa3163b48c7ccfd298c6a876d509a637 |
| indus_contact_zone_v2 | 27225e5adae04e376c57d05ec1a24b026a69f89e3f4fab6262a5b2c93a95ee7c |
| indus_dravidian_vs_sanskrit | e5fc51d783f3684b9057d3cfec5d7fcc42b26ee6b4ba75851870d33539821328 |
| indus_kalyanaraman_crossval | 4cff1eb5ca1bfa90247dee4cd6b7222244529e286454e4e240eb894b7d7b7e15 |
| indus_sa_dravidian | fcc1c17bae34a3d2d2be2269b452ff5579f9575db07a67d609e2a696c6fb6836 |
| indus_sa_dravidian_syllable | b2c65d3ab1927bde9d6a586b13e2691eec239de61757929eebb20a4884ff2706 |
| indus_sa_dravidian_vs_nw_semitic | 3a0b9c0b60ed828d14b819b54b1b4952e6ffcb74051762371820178185c4b55e |
| indus_sa_dravidian_vs_sanskrit | 9382d46cad4f92aba4cf33a351df1d4788f5609eb368d7e192d37d174cab8dec |
| indus_sa_sanskrit_falsification | 83f60e4583a9542216517a9de4e0effe1fb3438fa2c012f811d18df15b4d6222 |
| indus_sign_function_dravidian | ce26dd9074d5b86086a5d9414e2a291bb2ea9c7761e3233f9183feabe50d3c29 |
| indus_structural_atlas | efc70972c16978b2b64d4ea5c966be89b43123a4efa8ea138a24fabbdf92ae92 |
| indus_validation_a1_a3_holdout | 206b54d921201233c309ac08e46004a6e0cfe9e5deca2ef37158dcafa0400d9c |
| indus_validation_neg_controls | 1e0c4a2ee454d8b47ec395f083ae80fa3ae405c17c4ab5ee4c1f836b82585134 |
| kl_comparison | cf9a8e10b3043bc8942c29483118739688a02439fe20d5237f9d98e1647cca9c |
| ugaritic_sa_decipher | 13cb56ac1a5ae3cf163c95c9515d6ad7f0ad1076b2cab6dfa98fe20ef0a96172 |
| ventris_validation | 690015b0ae7f126bbc8f8cef1cc02e801fb0858af6e4686bf9a6a8dafc541c1e |

One measured caveat, stated plainly: this environment's
fresh-tree pre-change hashes do **not** reproduce the S2
record's pin table (26 of 27 differ; only `kl_comparison`
matches, which is also the one graph identical here without
the path normalization). The consistent explanation is tree
state: S2's runs executed in a working tree carrying local,
gitignored data (corpora downloads and generated reports)
that a fresh tracked-only checkout does not have — the M77
report file and the Holdat CSV are both absent in a fresh
tree, and both runs here therefore exercised the loaders'
absent/fallback behaviour identically on both sides. PR-A's
comparison accordingly pins pre vs post within this
environment (identical tree state on both sides) rather than
against the S2 table; the S2 table stands as S2's record of
its own environment. The runs regenerate `reports/*.json`
in-tree as a side effect; those files were restored
(`git checkout --`) and are not in this PR's diff.

## Test results

- Targeted suites (this branch): `test_spec087_s3_conversions.py`
  (36 equivalence cases + F14/primitives/converted-id tests),
  `test_spec087_registry_integrity.py`,
  `test_spec087_palette_curation.py` — **65 passed**.
- Full backend suite (this branch, TMPDIR on disk, the one
  named deselection `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`
  — the VM-environmental stall, CI is its authoritative
  runner): **1 failed, 2285 passed, 84 skipped, 1
  deselected**. The single failure is the known phase133
  local-only baseline
  (`test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`,
  missing local download; it does not fail CI). No tray
  teardown error appeared in this run.
- `python -m ruff check backend/` — clean. (One fixture
  consequence: the committed ScriptRunner source fixture
  `tiny_script.py` carried a dead `import json` from its
  capture draft; the import is removed in this PR — the
  script's behaviour and every pinned output are unchanged,
  and its equivalence case passes.)
- No frontend surface changed, so no builder-area frontend
  tests were required.

## Claim assessments (this PR's legs)

- **C087-6 / T302 — complete by vacuity.** The merged triage
  dispositioned zero of the 68 nodes as retain (disposition
  (c)); the parent accepted the zero-retention outcome at
  the triage gate. There are no retention files to write;
  T302 is ticked with this note in tasks.md.
- **C087-7 — PR-A leg supported.** 6 of the 64 CONVERT
  dispositions (family F1) are converted here with
  byte-identical fixture equivalence; the remaining families'
  legs land with their own PRs. (F14's two nodes were never
  part of the 68; their relabel is contract item 5, above.)
- **C087-13 — S3 PR-A leg supported.** The comparison runs
  over all 27 live graphs hold byte-identical under the
  named normalizations (above).
- **C087-17 — PR-A act recorded.** The census pin, the
  migration data file, and the S1/S2 test pins were re-pinned
  in this same PR, from the live registry, with the deltas
  tabled above.
- **C087-15 — PR-A manual leg.** `docs/user-manual.md`'s
  legacy section gains the short factual note (the two
  generic loaders in the palette; the six converted loaders
  now legacy). The generated node reference is S4's scope.

## Departures from the brief's letter, stated plainly

- **T303 is not ticked.** Only its F14 + F1 legs are
  discharged; 12 families remain. A progress note is recorded
  under T303 in tasks.md instead of a tick that would falsely
  record all conversion PRs complete.
- **No `ScriptRunner` alias id** was registered for
  LegacyPhaseScriptRunner (see the F14 interpretation note).
- The H4 fixture note in the triage concerns
  CanonicalSignLoader (family F3), not F1; it lands with
  PR-B. No F1 fixture needed CGSA seeding.

## M77 corpus-pipeline unification — Step 0 divergence check: STOP

**Order:** the owner, 2026-11-03 — unify the two M77 corpus
pipelines that PR-A recorded and pinned separately (above).
**Branch:** `feat/087-s3-m77-unify`, built on main `c817b04f`
(PR-A merged). **Date:** 2026-11-03. **Seat:** build worker;
the parent gates. The brief gated the build on a Step 0
divergence check: run both pipelines over the real corpus
data, compare field by field, and STOP — records only, no
unification — if any difference is observable by any
consumer. **That is the outcome. No code changed in this
PR.** The quantified record follows; the unification is an
owner decision on this evidence.

### The two pipelines, as they stand after PR-A

- **Pipeline A — the data module.** `glossa_lab/data/indus_m77.py`
  parses `reports/mahadevan_corpus_flat.txt` (first existing of
  three candidate paths) into bare sign sequences: no ids, no
  site codes, no raw layer. Getters:
  `get_corpus_inscriptions(min_length)`, `get_corpus_symbols()`,
  `get_corpus_metadata()`.
- **Pipeline B — the report chain.** `M77InscriptionLoader`
  (phase20) delegates to the JsonCorpusLoader engine with a
  fallback chain: `reports/mahadevan_texts_decoded.json`
  (records with `id`, `site_code`, `sequence`, `length`,
  `raw`), falling back to the Holdat CSV
  (`corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`,
  grouped by `cisi_number`, sequences from its `letters`
  column, site from its `site` column). Generator of the JSON:
  `backend/scripts/decode_inscription_texts.py` (OCR plate
  text → glyph-frequency rank correlation against the Fuls
  catalog → decoded sequences).

### Consumer census (Step 0a)

Pipeline A consumers:

- **Nodes:** `BuiltinCorpus` (`experiment_graph.py`; corpus
  names `indus_m77` / `m77` / `mahadevan` / `mahadevan_1977`),
  `BuiltinLM` (`experiment_graph_phase14.py`),
  `experiment_graph_ab_language.py` (through BuiltinCorpus).
- **Data-module callers:** `mesopotamian_contact.get_mahadevan_inscriptions`
  / `get_mahadevan_metadata` → the phase29 `DatasetRecordLoader`
  spec behind `MahadevanInscriptionLoader`.
- **API name routing:** `api/experiments.py` and
  `api/ai_tools.py` accept the `indus_m77` corpus name.
- **Scripts:** 40 files under `backend/scripts/` import
  `glossa_lab.data.indus_m77` (`audit_data_integrity.py`,
  `auto_decipher_loop.py`, `release_validation.py`,
  `translate_all_seals.py`, and 36 phase scripts);
  `scripts/phase16/rerun_indus_grounded.py` (through the
  corpus-name path), `scripts/phase18/measure_and_rerun.py`
  and `scripts/phase19/omnibus.py` /
  `sign_clusters_genre_cm.py` read the flat file directly.

Pipeline B consumers:

- **Node:** `M77InscriptionLoader` in three live graphs
  (`indus_sa_dravidian_syllable`,
  `indus_sa_sanskrit_falsification`,
  `indus_validation_neg_controls`). Their wiring observes
  exactly two outputs: `sequences` and `n_inscriptions`.
- **Registered consumer of the B-only fields:**
  `ClusterArchaeology` (phase20) takes an `inscriptions`
  input and reads `site_code` per inscription
  (`experiment_graph_phase20.py:463–487`). It is in no live
  graph, but it is a registered consumer of precisely the
  fields pipeline A does not have.
- **Direct file consumer:** `scripts/phase19/omnibus.py`
  `build_m77_raw_corpus()` reads the decoded JSON's `raw`
  field as a separate corpus (below).
- The Holdat CSV is a shared external corpus, not
  B-private: `api/foundation_check.py`, `api/signs.py`,
  `api/texts.py`, `api/research_loop.py`, `config.py`,
  `experiment_graph_phase137.py`, and the phase113/115/116
  runners also read it.

### The comparison (Step 0b), over the real data present

Run 2026-11-03 in this tree (`reports/mahadevan_corpus_flat.txt`
present, sha256 `878fd223…` — byte-identical in all six VM
trees checked, including the protected checkout):

- **Pipeline A:** 1,669 inscriptions / 5,361 tokens / 64
  distinct signs; canonical-JSON sha256 of the sequence list
  `095751a9…`; identical sequences via the
  `mesopotamian_contact` wrapper. Length histogram runs to a
  **maximum of 72 tokens** (25 inscriptions longer than 14),
  which contradicts `indus_m77.py`'s own docstring claim of
  a 1–14 range — the module's stated stats match its counts
  (1,669 / 5,361) but not its data's shape.
- **Pipeline B: cannot be run over its real data on this
  machine.** `reports/mahadevan_texts_decoded.json` exists
  in **no** tree on this VM (searched: every `glossa-run`
  tree, the goal workspaces, the protected checkout; the
  only copies anywhere are the synthetic PR-A test
  fixtures). The Holdat CSV is likewise absent
  (`corpora/` is a gitignored download tree, not present in
  this clone). Executed here, `M77InscriptionLoader`
  returns its absent-corpus error dict — no `sequences`,
  no `n_inscriptions`. Nor can the JSON be regenerated
  here: every input of `decode_inscription_texts.py` is
  absent (`backend/data-import/mahadevan_ocr/`,
  `backend/reports/real_indus_catalog_analysis.json`,
  `cjk_m77_mapping.json`, `mahadevan_bigrams_mapped.json`).
- **Present-tense observable difference, same tree, same
  corpus state:** pipeline A serves the full corpus
  (1,669 / 5,361 / 64) to its ~45 consumers; pipeline B
  serves an error to its node consumers. (PR-A's 27-graph
  comparison recorded exactly this absent behaviour for the
  three live graphs on both sides of that PR.) Unifying in
  either direction on this evidence changes observed
  output: onto B's source, every A consumer on this machine
  loses the corpus to a missing file; onto A's source,
  B's consumers gain records whose `id` is null and
  `site_code` empty where the JSON, when present, carries
  real values — and gain a corpus where they currently get
  a named error.

### Structural differences (provable from code, independent of file presence)

1. **Fields.** B's records carry `id`, `site_code`,
   `length`, and `raw`; A's carry none of these. B's node
   output exposes `inscriptions[{id, site_code, length,
   sequence}]`; `ClusterArchaeology` consumes the
   `site_code`. A has no equivalent surface to unify onto
   without inventing values.
2. **The raw layer.** B's JSON branch supports `use_raw`:
   per-character OCR glyph sequences — the *unmerged*
   glyph stream. The Phase-19 studies consume the two
   artifacts as **different corpora side by side**:
   `omnibus.py` measures `indus_m77` (the flat file) and
   `indus_m77_raw` (the JSON's raw field, "no rank-corr
   collapse", a type count the script prints as distinct
   from "64 in mapped"); `sign_clusters_genre_cm.py`
   clusters `indus_m77_mapped` and `indus_m77_raw`
   separately. A cannot express the raw layer at all.
3. **Fallback corpus identity.** When the JSON is missing,
   B silently substitutes a different corpus — the Holdat
   CSV, CISI-grouped, its own sign tokens — so which corpus
   B serves depends on which files happen to be present.
   A has exactly one source and fails loudly without it.
4. **Provenance / numbering conflict.** B's generator maps
   glyphs to **Fuls** sign numbers (`decode_inscription_texts.py`
   steps 3–5: Fuls catalog frequencies; `cjk_m77_mapping`'s
   `fuls` field). A's metadata asserts the flat file's
   tokens are "Mahadevan M77 (1977)" numbering
   (`get_corpus_metadata`), and the flat file is asserted
   by docstrings to be the same generator's sibling output
   — an assertion the records do not certify: the generator
   writes its outputs under `backend/reports/`, while both
   loaders read repo-root `reports/`, and its decoded
   entries are single OCR table rows while the flat data
   contains 72-token lines. Whether the flat file in the
   trees today is that generator's output, and whether its
   tokens are Fuls numbers wearing an M77 label, cannot be
   settled from this machine.

### Verdict and what the owner decision needs

**STOP.** The gate's proceed condition — output-equivalent
for every consumer, or differing only in ways proven
unobservable consumer by consumer — is not met and cannot
be met on the evidence available here: equivalence of the
sequence sets is unprovable without the decoded JSON, and
differences 1–3 are observable by named consumers
regardless. The open questions for the owner:

- Does `mahadevan_texts_decoded.json` exist in the live
  desktop tree (the Spec 080 backend's tree), and if so,
  can a copy be brought into the record so the field-by-field
  comparison can actually be run?
- Which artifact is canonical: the decoded JSON (with ids,
  sites, and the raw layer) or the flat file (the corpus
  every script consumer actually reads today)?
- Is the Holdat fallback a behaviour to keep in a unified
  loader, or a silent corpus substitution to retire?

Until those are answered, both pipelines stand as PR-A left
them: separately parameterised, separately pinned. This PR
changes no code, no fixture, and no consumer default; the
manual is untouched (no user-visible change).

## Repair note (PR-A, post-CI)

The first CI run of this PR failed exactly one case,
`pdf_extract`: the equivalence test read the two-page
fixture PDF from the fixtures directory, but `*.pdf` is
gitignored, so the file existed only in the build clone's
working tree and was never committed — a clean checkout got
the node's `PDF not found:` error instead of the pinned
extraction. The test now generates the PDF at run time with
PyMuPDF (the library the node itself requires) from the two
pinned page texts, and the byte-identical comparison against
`expected.json` is unchanged; no gitignored path is read.

## PR-B — families F3 (CGSA/CTT machinery) + F8 (anchor derivation & syllabification)

**Branch:** `feat/087-s3-conv-b`, built on main `50e91a63`
(PR #492 merged). **Commits:** `414c370` (fixtures, captured
first), `81b6624` (implementation). **Seat:** build worker;
the parent gates and merges. The contract stated at the head
of this record governs unchanged.

### The generic machinery — `backend/glossa_lab/generic_primitives.py`

One new stdlib-only module (it imports nothing from
glossa_lab, the generic_loaders.py pattern), holding the nine
engines the triage names for F3 + F8. Its `_db_all` is a copy
of `experiment_graph._sync_db_all`'s semantics — same
signature `(table, where, params)`, same database path (the
module sits in the same directory, so the parents[] math is
identical), same JSON-string coercion — so a delegating node
reads the database exactly as the original did.

The nine primitives, registered in the core list immediately
after DatasetRecordLoader, each with inputs/outputs mirroring
its domain node and a description naming the delegating node:

| primitive | category | mechanism |
|---|---|---|
| RegistryTableLoader | Sources | a registry table read as data: table name, param-driven filter clauses (truthy / argument), id mapping, count filters, the empty-result and error texts as spec fields. No-spec defaults are the canonical-signs shape. |
| LabelMapApplier | Transforms | a label map from an ordered source chain (database table, JSON file, frequency-rank fallback), with the unmapped label and the unavailable-error text as spec fields. |
| TemplateMiner | Analysis | per-length n-gram template mining (a sequence is abstracted to its equality pattern) plus the four summary fields a composition cannot express — the triage's H1 effort gap, closed as a primitive. |
| ClusterContingencyProfile | Analysis | cluster-vs-strata contingency profiling: strata rule, chi-squared, per-strata rates/enrichment, significance rule, and the verdict text as a `{placeholder}` template. |
| SignRoleClassifier | Analysis | the six-role corpus-statistics classifier (terminal/initial/medial rates, repetition and solo statistics, bigram-PMI compound detection, the behaviour-based logogram detector). Its `numeral_signs` parameter defaults EMPTY in the engine. |
| ValueRoleMapSource | Sources | a value→role map assembled from a base map plus per-family tables carried as data: seed roles applied first, vocabulary gathered per data module (a module whose import or attribute fails contributes nothing — the historical builders' single-try failure shape), filled with a default role or classified by determinative/numeral sets. |
| AnchorSyllabifier | Sources | anchor readings → syllable tokens: confidence gate over a caller-supplied order, diacritic table as ordered data pairs, positional-label skip pattern, CV syllable splitting, vocab-coverage fallbacks. |
| AssociationAnchorDeriver | Decipherment | anchors from sign↔context associations ranked by z-score, one anchor per sign, the anchor-id prefix as a parameter (engine default empty). |
| PMICentralityRanker | Analysis | signs ranked by count-weighted PMI centrality over bigram partners. |

### The nine delegations

Each registered AtomicNodeDef is unchanged; each fn keeps its
original docstring, gains a Spec 087 S3 note naming its
family, and delegates. The domain specifics now sit at the
delegation point as parameter defaults:

- **CanonicalSignLoader** (F3, `experiment_graph.py`, LIVE ×1)
  → RegistryTableLoader with the spec built inline: table
  `canonical_signs`, the `in_corpus` / `numbering_system`
  filters, the `n_parpola` count filter, and the historical
  empty-registry result and `Failed to load registry:` prefix
  carried verbatim in the spec.
- **ClusterMapper** (F3, `experiment_graph.py`, LIVE ×1) →
  LabelMapApplier with the historical source priority as the
  spec's chain: the `sign_cluster_assignments` table, then
  the JSON file at the path the original computed
  (parents[3] of experiment_graph.py / `analysis/sign_clusters.json`),
  then the frequency-rank fallback at 40 bins; unmapped label
  −1 and the historical unavailable-error text in the spec.
- **StructuralTemplateAnalyzer** (F3, `experiment_graph.py`,
  LIVE ×1) → TemplateMiner directly; the node's historical
  defaults are the engine's defaults. (Triage H1: the mining
  reproduces exactly under composition — 13/13 templates,
  identical counts; TemplateMiner exists for the four summary
  fields, as the triage named.)
- **ClusterArchaeology** (F3, phase20) →
  ClusterContingencyProfile with the Phase-20 parameterisation
  as data: strata field `site_code`, 2-character prefix +
  `"0000"`, critical value 3.84 per dof, 25-row site table,
  and the `PREDICTION 2 …` verdict text as the template. The
  module's now-callerless `_chi_squared` copy is removed in
  this PR (the engine carries its own; a tree-wide grep shows
  no other user).
- **IndusSignRoleClassifier** (F3, CTT) →
  SignRoleClassifier. Per triage H3, the node's entire domain
  content is the Indus numeral set as the `numeral_signs`
  default, so the wrapper injects
  `list(_DEFAULT_NUMERAL_SIGNS)` only when the caller did not
  pass the key — an explicit caller value, including `[]`,
  passes through untouched. `role_bits` is the CTT six
  (ROLE_BITS), passed as data.
- **DefaultIndusValueRoleMap** (F3, CTT) →
  ValueRoleMapSource with `base_map` =
  DEFAULT_INDUS_VALUE_ROLE_MAP (the constant stays in CTT as
  data, unchanged) and `family_tables` = the eight alias keys
  mapped to three family specs. The three per-language
  builder functions are replaced by those specs as data: the
  Tamil spec's seed roles are the DEDR suffix and numeral
  sets (Krishnamurti 2003 §6.2, cited in place), filled from
  the dravidian module's VOCABULARY + TAMIL_BRAHMI_ATTESTED;
  the Luwian spec classifies the hieroglyphic_luwian
  vocabulary by the determinative/numeral sets already held
  in CTT; the Linear B spec's base values are the Ventris
  grid syllables, filled from `get_corpus_symbols()` under
  the historical filter (lowercase, 1–4 chars, alpha).
- **IndusAnchorSetSyllable** (F8, phase30, LIVE ×1) →
  AnchorSyllabifier. Per triage H2 (byte-identical
  anchor_dict at MEDIUM/HIGH/LOW when parameterised), the
  wrapper resolves both file paths from its own module file
  exactly as the original did and passes the Tamil diacritic
  table (lifted to the module constant
  `_TAMIL_DIACRITIC_TABLE`, 22 ordered pairs including the
  historical duplicate pair, kept as-is), the confidence
  order {HIGH 3, MEDIUM 2, LOW 1, UNCERTAIN 0}, the
  positional-label skip pattern, and the missing-file error
  text as data.
- **DerivedAnchorSet** (F8, phase14) →
  AssociationAnchorDeriver with `anchor_prefix` `"ctx:"` —
  the node's one domain convention — as the parameter.
- **EpistaticAnchorRanker** (F8, phase14) →
  PMICentralityRanker directly; the triage found no domain
  constants in this node at all.

### Counts — the re-pin (C087-17 act for this PR)

| | before | after |
|---|---|---|
| registered | 519 | **528** (+ the nine primitives above) |
| legacy | 365 | **374** (+ the nine F3/F8 conversions) |
| palette | 154 | **154** (−9 converted, +9 primitives) |
| core definitions | 44 | **53** |
| categories | 65 | **65** (no change) |

Per-category deltas: `Sources` 6 → 9 (RegistryTableLoader,
ValueRoleMapSource, AnchorSyllabifier), `Transforms` 6 → 7
(LabelMapApplier), `Analysis` 9 → 13 (TemplateMiner,
ClusterContingencyProfile, SignRoleClassifier,
PMICentralityRanker), `Decipherment` 13 → 14
(AssociationAnchorDeriver). Legacy-by-category:
`CGSA / Structural` 0 → 3 (all three F3 CGSA nodes),
`CTT / Constraint Topology` 0 → 2, `Phase-20 / Archaeology`
0 → 1, `Phase-33 / Decipherment` 1 → 2
(IndusAnchorSetSyllable joins the already-legacy
DravidianSyllableLM), `Phase-14 / Grounding` 1 → 2,
`Phase-14 / Epistatic` 0 → 1. The migration data file gains
the nine ids under `s3_additions["PR-B (F3+F8)"]`; the census
pin fixture is regenerated from the live registry; the S2
agreement test's converted set now holds PR-A's six plus
these nine.

One arithmetic correction, stated plainly: the working
figures carried into this PR (registered 525, palette 151,
core 50) were wrong — 519 + 9 = 528, and the palette is
unchanged because the nine primitives entering it exactly
offset the nine conversions leaving it. The re-pin above is
counted from the live registry, not from those figures.

### Equivalence and comparison results

**Fixture equivalence (contract item 3):** 44 cases captured
from the pre-change implementations in commit `414c370`,
before any implementation changed, and replayed
post-conversion — **44/44 byte-identical** (39 full-mode
canonical-JSON equality; 5 hash-mode canonical-JSON SHA-256
+ key set + verbatim fields, the DefaultIndusValueRoleMap
family cases whose maps run to thousands of entries), in
`tests/test_spec087_s3_conversions_b.py`, alongside the
converted-ids flag/provenance test and the
primitives-in-palette test. Fixture sources per family: the
CGSA nodes run against a fake `_db_all` over two fixed
tables (the capture's fake re-implemented identically in the
test; H4's disposition — a fresh tree's backend DB holds
empty CGSA tables, so no seeding is needed or wanted); the
anchor cases run against the repo's real
INDUS_FINAL_ANCHORS.json and dravidian_syllable_lm.json.
Cross-checks against the triage's executed attempts: the
anchor counts reproduce H2 exactly (171 / 166 / 174 anchors
at MEDIUM / HIGH / LOW, 287 at UNCERTAIN, `n_skipped` 0 at
every level), and the role default-vs-empty-numerals
difference is exactly the numeral role on the default-set
signs (H3's pattern).

One case is split, and says so in the bundle: ClusterMapper's
JSON-file branch reads a file at a path outside the
repository, which CI cannot recreate. The capture ran it
with a real `sign_clusters.json` placed at the node's
historical path (removed again before the capture script
exited; absence asserted before and after). The replay runs
that branch through the LabelMapApplier primitive with a
temporary file carrying the same content and the same source
chain the domain node builds, its database source emptied
exactly as in the capture. The domain node's database,
frequency, and error branches replay directly.

**27-graph comparison (contract item 4):** the S2 runner was
executed on a fresh worktree of origin/main `50e91a63` (pre)
and on this branch (post), under the same two normalizations
as PR-A (LanguageModel repr addresses; each tree's own root
path). Both sides saw the same database state: the build
clone's local backend DB (empty CGSA tables) was copied into
the pre worktree, and the ClusterMapper file path is absent
in both trees, so both sides exercised the same branches.
**27/27 graphs byte-identical pre vs post**:

| graph | normalized sha256 (pre == post) |
|---|---|
| fuls_independence_suite | 991cfc445a85250a29cb4f6e58cb21e5ce000f8f856d67e83ffc9d4c667761bb |
| fuls_nw_semitic_benchmark | ba8955b51e54d766e73beb0045bf56ad3412df0f6668af7ef3ffd58a80899bcd |
| fuls_validation_suite | 13eeae07336b9add444308c3a4c2e80650223cdc25ff3e49112dff190a3b89ee |
| generic_sa_multi_comparison | 5cc9d5c05d6bc4d601ec03620efc069eeecf9be48ed3e2b31f98fb38734a37be |
| indus_anchor_sweep | 6aa045a2d574c0cc187088edeb58d05b930fb3565c7680257046665b2b839f37 |
| indus_cgsa_cluster_analysis | 23b729b0b0beca767397b75331418fc71f7897543432cc9bc094c4dc7eaa9d9e |
| indus_cisi_anchored_10 | cbd24cb40f154f745d99ff23192acb395147d37fa736288400af37827fb498fe |
| indus_cisi_dravidian_vs_pali | bfe729e9c1d3580e72ffd4f3c9f430a315bc65101abcd0804da2ecba272134d8 |
| indus_cisi_dravidian_vs_sanskrit | 754f4132ac83ed0c698a8470355bb0eceeea17248aa9f00c220a5e5c806791de |
| indus_cisi_sa_dravidian_vs_nw_semitic | 0ef2599aec2d78dc2708c6afc72ab607561e27c3bbb86a98aacde0574d01ff03 |
| indus_cisi_sa_dravidian_vs_sanskrit | 07b31b9db57b4f79358afe4224f852fb9c0ed8c8d42d50a613442a7c397dd28f |
| indus_cisi_structural | 14874f0aca115af7bc0cca8318e63cbefae564f4df54dfef576dc03604db6578 |
| indus_contact_zone_v2 | 39506ed67256454feab5b6901c191a13977d8697dd50e3bf0926dadeaddc24ad |
| indus_dravidian_vs_sanskrit | 0035134bb5d80c043847e74910db8a2e3bbdbbc1782f583d8c45b96313e9274c |
| indus_kalyanaraman_crossval | b91979cb7db634ff88388eb94187c2903bcead561a3b9a01f58deca79378b941 |
| indus_sa_dravidian | d1c55048bf705a69a2521ec836e26a5e3fd5f255becfee9e9804ece0d2adb553 |
| indus_sa_dravidian_syllable | 59d53741f123d1dac96a7e26f96573ab01fbbb7ccdc008f75e327da56e4f5bfa |
| indus_sa_dravidian_vs_nw_semitic | 9481fac660430ef9d384aa74ee9a61a7984126a001b5d022678d8cf20bfcac0a |
| indus_sa_dravidian_vs_sanskrit | 14281066e98477493620159207b241ede475afbd29165dfb7a4f5b4bfcd77a56 |
| indus_sa_sanskrit_falsification | 6f730bda1effd69cdbd1bf88cd8987e2c4e416fb8f2875fcab1292ba72069cb7 |
| indus_sign_function_dravidian | cfa805f2eb873f87e42d79ded34ec867acc83da56b54364b045f574d7df3a034 |
| indus_structural_atlas | 86f0d2865f14a2686b20802771bb4284098b83dd30a5b04e570b34f88f6f057a |
| indus_validation_a1_a3_holdout | 912f58147de96ba82c33e2dc8214bd9b3b0d1c096b3a57b9afe835998fdcb6c1 |
| indus_validation_neg_controls | 729d59ebbbca788e670b49e85843a4a3484a3efeb9b66e22d7231af7899b90f7 |
| kl_comparison | cf9a8e10b3043bc8942c29483118739688a02439fe20d5237f9d98e1647cca9c |
| ugaritic_sa_decipher | af1b203f637ef67e4b3705a61697471fffdfd591d28934aa0c32d438cf41155b |
| ventris_validation | 05580212a0a65a5ae9896ee610564fb4a7937c01b1a200f10724705c29fc8921 |

PR-A's environment caveat applies unchanged: the comparison
pins pre vs post within this environment (identical tree
state on both sides); `kl_comparison` again matches the S2
and PR-A tables exactly. Environment note: the build VM was
replaced mid-comparison and the first post-side run died
with it; the run was repeated detached and every number
above was read from the two runs' output files on disk. The
runs regenerate `reports/*.json` in-tree as a side effect;
those files were restored and are not in this PR's diff.

### Test results

- Targeted suites (this branch):
  `test_spec087_registry_integrity.py`,
  `test_spec087_palette_curation.py`,
  `test_spec087_s3_conversions.py` (PR-A),
  `test_spec087_s3_conversions_b.py` (44 equivalence cases +
  flag/provenance + palette tests) — **111 passed**.
- Full backend suite (this branch, TMPDIR on disk, the one
  named deselection): run in checkpointed segments after two
  VM replacements killed two single-process attempts.
  Completed locally: **1,173 tests over 94 of 219 files —
  1,152 passed, 18 skipped, 3 failed, 0 errors**. The three
  failures: the known phase133 local-only baseline
  (`test_builder_recomputation_skips_without_inputs`, missing
  local download; it does not fail CI), and two failures
  recorded inside platform-incident windows that this
  environment prevented from being adjudicated locally —
  `test_auth_consumers.py::test_auth_proof_kit_end_to_end`
  (ran in the unsettled window after the second replacement)
  and `test_phase394_build.py::test_grade_correction_requires_naming_text`
  (recorded at the tail of the 55-minute segment, at the
  onset of the write wave below); neither touches this PR's
  change surface, and both are named here for CI to adjudicate.
  The remaining 125 files were **not run locally**: from the
  wave's onset, every fresh Python process on this VM died
  at tempfile creation (tempfile's probe write is
  EPERM-denied under the VM write restriction), verified
  repeatedly with the wave probe across ~50 minutes. Those
  files are carried to CI — the suite's authoritative
  runner — for this PR's full-suite verdict. This is a
  stated departure from the full local-suite proof, forced
  by the platform incidents and recorded, not smoothed over.
  (The phase20 `_chi_squared` removal above landed after the
  targeted suites ran; it removes a function with no caller
  anywhere in the tree — tree-wide grep — and the final tree
  is ruff-clean; its re-run also waits on the wave / CI.)
- `python -m ruff check backend/` — clean. (One import
  consequence: `math` became unused in experiment_graph_ctt.py
  when the role classifier delegated, and the import is
  removed in this PR.)
- No frontend surface changed, so no builder-area frontend
  tests were required and no dist rebuild was needed.

### Claim assessments (this PR's legs)

- **C087-7 — PR-B leg supported.** 9 of the 64 CONVERT
  dispositions (families F3 + F8) are converted here with
  byte-identical fixture equivalence; cumulatively 15 of 64
  with PR-A. The remaining families' legs land with their
  own PRs.
- **C087-13 — PR-B leg supported.** The comparison runs over
  all 27 live graphs hold byte-identical under the named
  normalizations (above), including the two live graphs that
  carry converted nodes (`indus_cgsa_cluster_analysis`,
  `indus_sa_dravidian_syllable`).
- **C087-17 — PR-B act recorded.** The census pin, the
  migration data file, and the S1/S2 test pins were re-pinned
  in this same PR, from the live registry, with the deltas
  tabled above.
- **C087-15 — PR-B manual leg.** `docs/user-manual.md`'s
  legacy section gains the short factual note (the nine new
  generic blocks in the Palette; the nine converted nodes
  now legacy). The generated node reference is S4's scope.

### Departures from the brief's letter, stated plainly

- **T303 is still not ticked.** Its F3 + F8 legs are
  discharged here; ten families remain (F2, F4, F5, F6, F7,
  F9, F10, F11, F12, F13), plus family F15 and the final
  retire-flagging batch. The progress note under T303 in
  tasks.md is updated instead of a tick.
- **The count figures in the working brief were wrong**
  (registered 525 / palette 151 / core 50); the correct
  figures, counted from the live registry, are 528 / 154 /
  53. Recorded in the counts section above.
- **phase20's `_chi_squared` helper is removed**, not just
  bypassed: its only caller was the converted node, and the
  engine's copy is the one that now runs. No other module or
  test referenced it (tree-wide grep).
- **The full local suite is incomplete** (see Test results):
  two VM replacements and an EPERM write wave cut it at
  1,173 of ~2,420 tests, with two of its three failures
  unadjudicated locally. The brief's full-suite proof is
  discharged in part locally and in full by this PR's CI,
  which the parent's merge gate reads; the local remainder
  can be re-run when the wave clears.
