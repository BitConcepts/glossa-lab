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

## PR-C — families F4 (phoneme-map scoring & permutation tests) + F5 (name↔seal length matching & stratified readouts)

**Branch:** `feat/087-s3-conv-c`, built on main `3bd37594`
(PR #494 merged). **Commits:** `4624abd` (fixtures, captured
first), plus the implementation commit. **Seat:** build worker;
the parent gates and merges. The contract stated at the head
of this record governs unchanged.

### The generic machinery — appended to `backend/glossa_lab/generic_primitives.py`

PR-C appends six engines to PR-B's module (same stdlib-only
pattern), plus the shared helpers the F5 family had copied into
five phase modules: `_name_n_segments`, `_length_score`, the
greedy bipartite assignment and its random-assignment null,
and the readout null statistics (at-or-above p, sample-sd,
z). The three `_run_bipartite_test` copies in phases 25/26/27
were verified behaviourally identical before the conversion
(AST-equal modulo docstrings) — the engine carries the one
shared core. Two divergences inside the family are carried
as named data, never normalised away: MeluhhaNameMatcher's
length falloff is 1 − |Δ|/5.0 with no tolerance (the rest of
the family uses 1 − Δ/(tolerance+1), 0 beyond tolerance), and
the stratified nodes' per-stratum seed rules differ by node
(42 / 271 / 137 + len(stratum)).

The six primitives, registered in the core list immediately
after PMICentralityRanker, each with inputs/outputs mirroring
its domain nodes (unions where the pair of delegating nodes
differ) and a description naming the delegating nodes:

| primitive | category | mechanism |
|---|---|---|
| IconographicAnchorScorer | Decipherment | anchors matched to a phoneme map through an ordered reading→alias table as data; confidence weights (2.0/1.0/0.5) and the ×1.5 high-confidence bonus as data; optional allograph mode: a per-entry family, the two-pass family resolution (the matching entry's family, else the last contained entry's), and a per-member extension bonus (+0.25 for Phase-28). |
| PhonemeMapCoverage | Decipherment | per-seal phoneme skeletons under a map; readability = any attributed phoneme that is neither the unknown token nor marked uncertain; placeholder-only seals reported with the placeholder skeleton; the tokens and the verdict text are spec data. |
| PhonemeMapPermutationTest | Analysis | observed confidence-weighted coverage vs null maps shuffling ONE dimension — confidence labels (V1) or phoneme values with compound-plausibility reweighting (V2: pattern table of 8 pairs, +1.0 per attested compound, +0.2 per repeated token, both as data); output key names, null gloss, row limit, verdict and interpretation are spec data. |
| LengthMatchScorer | Decipherment | name↔seal length pairings under a named score spec (tolerance falloff, or the named `linear_falloff_divisor_5`); three assignment modes — all_pairs (Phase-23, best-per-name), bipartite (Phase-24, greedy one-to-one), aggregate_pairs (Phase-22, candidates counted from raw persons, seals filtered to sign-bearing); each mode returns its historical output shape. |
| LengthMatchPermutationTest | Decipherment | the readout permutation test with the statistic as data: best_match (per-name best score summed; null shuffles the seal-length list in place, one rng) or bipartite (assignment sum; null = random one-to-one assignments); verdict bands, the insufficient-data verdict (which differs between V1 and V2 and is carried verbatim), the optional observed-assignment rows, and the interpretation are spec data. |
| StratifiedPermutationTest | Decipherment | the bipartite readout test per stratum + a merged overall: strata assigned by an ordered substring→bucket rule table as data (case sensitivity, value stripping, empty/fallback buckets all as data — Phase-25's inline case-sensitive coarsening chain becomes a 5-rule table), per-stratum seed = seed_base + len(bucket), strata with <2 distinct candidates skipped, the overall run merging only the tested strata. One engine proves the two period variants and the provenience variant are one primitive: the fixtures run all three over one shared person set and they diverge observably (2 / 1 / 0 significant strata). |

### The thirteen delegations

Each registered AtomicNodeDef is unchanged; each fn keeps
its original docstring, gains a Spec 087 S3 note naming its
family, and delegates with its specifics as spec data at the
delegation point:

- **IconographicAnchorScore** (F4, phase27) →
  IconographicAnchorScorer with the 16-entry alias table
  lifted to the module constant `_ICONOGRAPHIC_ALIAS_TABLE`
  (families unused) and the verbatim verdict template.
- **AllographAwareIconographicScore** (F4, phase28) →
  IconographicAnchorScorer in allograph mode
  (`extension_bonus` 0.25) with its (alias, family) table as
  `_ICONOGRAPHIC_ALIAS_TABLE_28` and the verbatim verdict
  template.
- **BlindHeldOutTest** (F4, phase25) → PhonemeMapCoverage
  with the verbatim verdict template (its text names the
  Janabiyah/CISI study, carried as spec data).
- **BayesianDecoder** (F4, phase26) →
  PhonemeMapPermutationTest, shuffle_dimension `confidence`,
  seed default 1234, rows limited to the top 10 under the
  historical key `obs_per_seal_top10`, verbatim verdict +
  interpretation.
- **BayesianDecoderV2** (F4, phase27) →
  PhonemeMapPermutationTest, shuffle_dimension `value`,
  seed default 2727, all rows under `obs_per_seal`, the
  8-pair `_DRAVIDIAN_COMPOUND_PATTERNS` table (kept in
  phase27 as delegation data) driving the plausibility
  reweighting, verbatim verdict + interpretation.
- **EnhancedNameMatcher** (F5, phase23) → LengthMatchScorer
  `all_pairs`, min-frequency default 2, verbatim templates.
- **EnhancedNameMatcherV2** (F5, phase24) → LengthMatchScorer
  `bipartite`, min-frequency default 1, verbatim templates.
- **MeluhhaNameMatcher** (F5, phase22) → LengthMatchScorer
  `aggregate_pairs` with score spec
  `{"kind": "linear", "divisor": 5.0, "name":
  "linear_falloff_divisor_5"}` — the divergent falloff,
  carried as a named spec and pinned by fixture (the
  meluhha_default case's pairings score 1.0 / 0.8 / 0.6 /
  0.2 under it; under the family tolerance falloff they
  would read 1.0 / 0.667 / 0.333 / 0.0-skipped).
- **BilingualReadoutTest** (F5, phase23) →
  LengthMatchPermutationTest `best_match`, defaults
  1000 / 2, insufficient verdict `INSUFFICIENT_DATA: cannot
  run readout test` (V1's longer text, verbatim).
- **BilingualReadoutTestV2** (F5, phase24) →
  LengthMatchPermutationTest `bipartite`, defaults
  2000 / 1, insufficient verdict `INSUFFICIENT_DATA`,
  observed-assignment rows on.
- **PeriodStratifiedReadout** (F5, phase25) →
  StratifiedPermutationTest over `period`: the inline
  coarsening chain as ordered rules (case-sensitive, on the
  stripped value; the Old Akkadian rule carries both of the
  chain's keys, `Old Akkadian` and `Akkadian`), empty value
  → fallback `Other`, seed base 42, verbatim verdict.
- **PeriodStratifiedReadout6Bucket** (F5, phase27) →
  StratifiedPermutationTest over `period` with
  `_PERIOD_BUCKETS_6` as data (kept in phase27), empty →
  `Unknown`, seed base 271, verbatim verdict.
- **ProvenienceStratifiedReadout** (F5, phase26) →
  StratifiedPermutationTest over `provenience` with
  `_PROVENIENCE_BUCKETS` as data (kept in phase26), empty →
  `Unknown`, seed base 137, verbatim verdict (it names its
  own study and the Phase-25c cross-reference).

Callerless helpers removed with the delegations (each
verified by tree-wide grep to have had no other caller; the
engine carries the shared copies): phase23 `_name_n_segments`
+ `_length_score`; phase24 `_name_n_segments` +
`_length_score` + `_greedy_bipartite_assignment`; phase25
`_length_score` + `_greedy_score` + `_run_bipartite_test`
(phase25's `_name_n_segments` STAYS — the Persons-v3
extractor, family F6, still uses it); phase26
`_name_n_segments` + `_length_score` + `_greedy_score` +
`_run_bipartite_test` + `_classify_provenience` +
`_seal_phoneme_match_score`; phase27 `_name_n_segments` +
`_length_score` + `_greedy_score` + `_run_bipartite_test` +
`_classify_period_6` + `_seal_phoneme_match_score` +
`_compound_plausibility_score`. The now-unused `math` /
`random` imports in phases 23–27 went with them.

### Counts — the re-pin (C087-17 act for this PR)

| | before | after |
|---|---|---|
| registered | 528 | **534** (+ the six primitives above) |
| legacy | 374 | **387** (+ the thirteen F4/F5 conversions) |
| palette | 154 | **147** (−13 converted, +6 primitives) |
| core definitions | 53 | **59** |
| categories | 65 | **65** (no change) |

Per-category deltas: `Decipherment` 14 → 19
(IconographicAnchorScorer, PhonemeMapCoverage,
LengthMatchScorer, LengthMatchPermutationTest,
StratifiedPermutationTest), `Analysis` 13 → 14
(PhonemeMapPermutationTest). Legacy-by-category:
`Phase-22 / Decipherment` 0 → 1, `Phase-23 / Decipherment`
0 → 2, `Phase-24 / Decipherment` 0 → 2,
`Phase-25 / Decipherment` 1 → 3, `Phase-26 / Decipherment`
0 → 2, `Phase-27 / Decipherment` 0 → 3,
`Phase-28 / Decipherment` 0 → 1. The migration data file
gains the thirteen ids under `s3_additions["PR-C (F4+F5)"]`;
the census pin fixture is regenerated from the live
registry; the S2 agreement test's converted set now holds
PR-A's six, PR-B's nine, and these thirteen.

### Equivalence and comparison results

**Fixture equivalence (contract item 3):** 34 cases captured
from the pre-change implementations in commit `4624abd`,
before any implementation changed, and replayed
post-conversion — **34/34 byte-identical** (all full-mode
canonical-JSON equality; the permutation outputs are
seed-determined), in `tests/test_spec087_s3_conversions_c.py`,
alongside the converted-ids flag/provenance test and the
primitives-in-palette test. Fixture sources: the loaders
behind the historical graphs read the gitignored corpora/
download tree, absent from this repository, so — PR-A's
precedent for ContactCorpusLoader — the inputs are synthetic
records in exactly the mesopotamian_contact shapes, built to
exercise every branch the conversion could move:
placeholder-only and empty-sign seals, a compound sign_id
(`99+12`), a missing-sign anchor, the allograph second pass
on both a matched row (family fish, 2 extensions) and a
non-matched row (family assigned, no score), hand-verified
plausibility arithmetic (2.0 and 1.2 on two seals), the
pinned Meluhha falloff, every stratifier branch of all three
rule sets over one shared 20-row person set, and an
insufficient-inputs case per node family. Sanity was checked
against hand computation at capture (allograph: 7 matches,
5 extensions, extended ids ['130', '48', '50'], total
13.75; iconographic: 7 matches, total 12.5; blind: 5
readable, 3 high-confidence seals).

**27-graph comparison (contract item 4):** the S2 runner was
executed on a fresh worktree of `3bd37594` (pre) and on this
branch (post), under the same two normalizations as PR-A/PR-B
(LanguageModel repr addresses; each tree's own root path).
Database state: CGSA reads resolve to
`<tree>/backend/data/glossa.db` (untracked runtime state),
so the fresh pre worktree had no such file and read absent
tables, while the post side read the build clone's DB,
whose CGSA tables are empty (canonical_signs 0 rows,
sign_cluster_assignments 0 rows, verified read-only) —
both sides exercised the same empty-table state.
(Correction, post-delivery: the first delivered text of
this section said the clone's DB "was copied into the pre
worktree"; the copy in fact failed — a fresh worktree has
no `backend/data/` directory — and the second leg of the
copy command never ran. The comparison result below is
unaffected.)
**27/27 graphs byte-identical pre vs post**, and every
normalized hash also equals the PR-B table's hash for the
same graph (the environment's cross-check):

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

None of the 27 live graphs wires an F4/F5 node (the census's
live working set is 36 atomicIds; the F4/F5 nodes' graphs
live in `_archive/`, out of scope) — the comparison here is
the no-live-behaviour-change proof for the shared helpers'
removal and the registry edits; the per-node proof is the
fixture equivalence above. The runs regenerate
`reports/*.json` in-tree as a side effect; those files were
restored and are not in this PR's diff.

### Test results

- Targeted suites (this branch): all five Spec 087 test
  files — `test_spec087_registry_integrity.py`,
  `test_spec087_palette_curation.py`,
  `test_spec087_s3_conversions.py` (PR-A),
  `test_spec087_s3_conversions_b.py` (PR-B),
  `test_spec087_s3_conversions_c.py` (this PR: 34 equivalence
  cases + flag/provenance + palette tests) — **150 passed**.
- Full backend suite (this branch, TMPDIR on disk, the one
  named deselection
  `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`):
  the single-process run executed 2,345 tests to ~95% of the
  suite — **2,262 passed, 82 skipped, 1 failed** — and then
  the process died silently: no summary, no traceback, the
  log frozen — a platform kill of the same family this VM
  has shown before. The one failure is the known phase133
  local-only baseline
  (`test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`,
  missing local download; it does not fail CI), confirmed by
  re-running that file standalone (1 failed, 13 passed — the
  same single failure).
  The unexecuted tail (the t-range files:
  `test_terminal_log.py`, `test_texts_crud.py`,
  `test_tray_step8.py`, `test_tray_supervision.py`,
  `test_tray_token_auth.py`, `test_supervision_installer.py`)
  was then run explicitly: **80 passed**, the tray teardown
  flake family not appearing. The full-suite verdict for the
  remaining slice is carried to CI — the suite's
  authoritative runner — exactly as PR-B's record carried
  its wave-cut remainder. This is a stated departure from a
  complete local full-suite proof, forced by the platform
  incident and recorded, not smoothed over.
- `python -m ruff check backend/` — clean.
- No frontend surface changed, so no builder-area frontend
  tests were required and no dist rebuild was needed.

### Claim assessments (this PR's legs)

- **C087-7 — PR-C leg supported.** 13 of the 64 CONVERT
  dispositions (families F4 + F5) are converted here with
  byte-identical fixture equivalence; cumulatively 28 of 64
  with PR-A and PR-B. The remaining families' legs land with
  their own PRs.
- **C087-13 — PR-C leg supported.** The comparison runs over
  all 27 live graphs hold byte-identical under the named
  normalizations (above).
- **C087-17 — PR-C act recorded.** The census pin, the
  migration data file, and the S1/S2 test pins were re-pinned
  in this same PR, from the live registry, with the deltas
  tabled above.
- **C087-15 — PR-C manual leg.** `docs/user-manual.md`'s
  legacy section gains the short factual note (the six new
  generic blocks in the Palette; the thirteen converted nodes
  now legacy). The generated node reference is S4's scope.

### Departures from the brief's letter, stated plainly

- **T303 is still not ticked.** Its F4 + F5 legs are
  discharged here; eight families remain (F2, F6, F7, F9,
  F10, F11, F12, F13), plus family F15 and the final
  retire-flagging batch. The progress note under T303 in
  tasks.md is updated instead of a tick.
- **The brief's expected arithmetic was right this time**
  (registered +6, legacy +13); the re-pin is nevertheless
  counted from the live registry, per the contract: 534 /
  387 / 147, core 59, categories 65.
- **Helper removals are broader than PR-B's single case**:
  the F5 family's helpers were per-module copies, so the
  delegations made 15 helper functions callerless across
  phases 23–27 (listed above). Each removal is grep-proven;
  phase25's `_name_n_segments` is deliberately NOT among
  them (a live F6 caller remains).
- **The graph-runner outputs were read from files, not
  process reports**: both comparison runs were launched
  through a shell pipeline whose exit status masked the
  runner's own; the runs' completion and results were
  verified from the summary/output files they wrote (27
  graphs, all status ok, on both sides) before the hashes
  above were computed.

## PR-D — families F7 (Janabiyah skeleton search, forward + reverse) + F6 (Meluhhan persons extractors)

**Branch:** `feat/087-s3-conv-d`, built on main `702cc717`
(PR #495 merged). **Commits:** `09d7784` (fixtures, captured
first), plus the implementation commit. **Seat:** build worker;
the parent gates and merges. The contract stated at the head
of this record governs unchanged.

### The generic machinery — appended to `backend/glossa_lab/generic_primitives.py`

PR-D appends three engines to PR-C's module (same stdlib-only
pattern). The F7 family's two directions are two engines; the
four reverse searches share ONE scoring core inside the
second engine (target segment positions {1,3,6}, target
length 7, length score 3.0 − 0.5·δ, +1.5 per position match,
+0.5 per free occurrence, −1.5 penalty for names ending
-me-luh-ha / -me-luh-ha-ki — all as data of the core). One
divergence inside the family is carried as data of the
candidate mode, never normalised away: the persons modes
(Phases 27/28) match renderings as substrings of cleaned
segments, while the ePSD2 modes (Phases 29/30) match whole
segments against the rendering token set exactly — the
current code has both rules, and no behaviour was harmonised
to make the family tidier. The ePSD2 segmenter (strip {…}
determinatives, split on hyphen runs, drop trailing digits
per part) is carried by the engine, as is the Phase-28/29/30
dynamic rendering expansion (phoneme tokens of the named
allograph family's members, from the phoneme map).

The three primitives, registered in the core list immediately
after StratifiedPermutationTest, each with inputs/outputs
mirroring its domain nodes (unions where the delegating nodes
differ) and a description naming the delegating nodes:

| primitive | category | mechanism |
|---|---|---|
| SkeletonTabletSearch | Decipherment | the forward readout: predictions + phonetic skeleton from a reading via a phoneme map (unmapped sign → "?" / "(unmapped)" / "none"), then one or more rendering scans over tablet lines gated on a keyword in the tablet's matched keywords, hits = rendering substrings per line, kept at hits ≥ a spec minimum; scan set, hit key, count differences between scans, verdict and interpretation are spec data. |
| ReverseSkeletonSearch | Decipherment | the reverse search over the shared scoring core, in three candidate modes: persons (aggregate a persons list by name, substring matching, penalty suffixes, optional dynamic rendering expansion, optional n_renderings report), pn (ePSD2 entries filtered by icount, best alternate form scored, exact-token matching), pn_cohorts (the pn scoring stratified by best-form segment count into a cohort table — the node's own cohorts param — with per-cohort hit rates and the 5x concentration verdict rule as data). |
| PersonsAggregator | Transforms | the persons aggregation pass: count occurrences per candidate name, collect periods / proveniences / source patterns / example lines, optional distinct-tablet counts, optional segment-count enrichment, known-name confirmation from a names set carried as data or from the upstream rows' is_known flag, optional by-pattern distribution over all rows; output key names, example-line truncation, and the verdict text are spec data. |

### The ten delegations

Each domain fn keeps its id, def, and docstring, and now
builds its spec and delegates. Fixed content at the delegation
points:

- **JanabiyahPhoneticReadout** (phase25) → SkeletonTabletSearch:
  one scan whose renderings are the constant 11-item list
  (`mi-in, me-en, mi-na, me-na, mi-il, me-il, mi-en, me-in,
  mu-li, min-, men-`), the "me-luh" keyword gate, hits ≥ 2,
  hit key `n_miin_hits`, verdict + interpretation verbatim.
- **JanabiyahPhoneticReadoutV2** (phase26) → SkeletonTabletSearch:
  two scans over the input-port rendering lists (direct-only,
  then the full list), hit key `n_hits`, and the
  expanded-minus-direct count difference
  (`n_new_matches_from_translation`) as spec data.
- **ReverseJanabiyahSearch** (phase27) → ReverseSkeletonSearch,
  persons mode: the 15-item rendering set, penalty suffixes
  `-me-luh-ha` / `-me-luh-ha-ki` at −1.5, top_k default 20,
  floor 10.
- **ReverseJanabiyahSearchV2** (phase28) → ReverseSkeletonSearch,
  persons mode: the 16-item base set (Phase-27's 15 + `asz`),
  expansion on with family source `fish`, n_renderings
  reported, top_k default 30, floor 10.
- **M77ReverseJanabiyahSearchV3** (phase29) →
  ReverseSkeletonSearch, pn mode: the ePSD2 name source, the
  carried segmenter, expansion on (family `fish`), top_k
  default 30, floor 10, verdict assembled from the head / top /
  no-top / suffix pieces verbatim.
- **LengthCohortReverseJanabiyahSearch** (phase30) →
  ReverseSkeletonSearch, pn_cohorts mode: the pn scoring plus
  cohorts from the node's own param (default
  [[3,4],[5,6],[7,8],[9,99]]), concentration factor 5.0,
  top_k default 15, floor 5, verdict pieces verbatim
  (including the en dash in the rate range and the em dash in
  the flat text).
- **MeluhhanPersonsExtractor** (phase22) → PersonsAggregator:
  the `persons` port, provenience + distinct-tablet
  collection, example lines untruncated, confirmation against
  the known-names set {lu-sun-zi-da, lu2-sun-zi-da, shu-ilishu,
  shu-ilisu, su-ilisu} as a data param (matched
  case-insensitively, as today), `all_rows_count` in place of
  `rows_all`.
- **RefinedMeluhhanPersonsExtractor** (phase23) →
  PersonsAggregator: the `strict_persons` port, provenience +
  source-pattern + distinct-tablet collection, example lines
  untruncated, by-pattern distribution over all rows
  (including empty names, as today), known source = the
  upstream rows' `is_known` flag.
- **RefinedMeluhhanPersonsExtractorV2** (phase24) →
  PersonsAggregator: the Phase-23 parameterisation on the
  `persons_v2` port with example_line[:120] and its own
  verdict text. Its pre-conversion body was a near-verbatim
  copy of Phase-23's; the copy is deleted by this conversion,
  and its fixtures are the Phase-23 fixture rows.
- **Persons_v3_Extractor** (phase25) → PersonsAggregator:
  segment-count enrichment on (the triage's toggle), example
  lines truncated to 160, no provenience/pattern/tablet
  collection, no known-name confirmation (`confirmed_hits`
  stays empty, as today), n under the `n_unique` key.

Callerless helpers removed, each grep-proven to have had the
converted node as its only caller: phase29's
`_epsd_pn_to_segments` and phase30's `_pn_to_segments` (the
engine carries the shared segmenter), phase25's
`_name_n_segments` (the engine carries the segment counter —
PR-C deliberately kept this helper because this F6 caller
remained; the caller is converted here, so the keep lapses),
and the `re` / `Counter` imports the delegations left unused
in phases 28, 29, and 30 (ruff-verified).

### Counts — the re-pin (C087-17 act for this PR)

| | before | after |
|---|---|---|
| registered | 534 | **537** (+ the three primitives above) |
| legacy | 387 | **397** (+ the ten F7/F6 conversions) |
| palette | 147 | **140** (−10 converted, +3 primitives) |
| core definitions | 59 | **62** |
| categories | 65 | **65** (no change) |

Per-category deltas: palette `Decipherment` 19 → 21
(SkeletonTabletSearch, ReverseSkeletonSearch), palette
`Transforms` 7 → 8 (PersonsAggregator). Legacy-by-category:
`Phase-22 / Reporters` 0 → 1, `Phase-23 / Reporters` 0 → 1,
`Phase-24 / Reporters` 0 → 1, `Phase-25 / Decipherment`
3 → 4, `Phase-25 / Reporters` 2 → 3, `Phase-26 / Decipherment`
2 → 3, `Phase-27 / Decipherment` 3 → 4,
`Phase-28 / Decipherment` 1 → 2, `Phase-29 / Decipherment`
0 → 1, `Phase-30 / Decipherment` 0 → 1. The migration data
file gains the ten ids under `s3_additions["PR-D (F7+F6)"]`;
the census pin fixture is regenerated from the live
registry; the S2 agreement test's converted set now holds
PR-A's six, PR-B's nine, PR-C's thirteen, and these ten.

### Equivalence and comparison results

**Fixture equivalence (contract item 3):** 31 cases captured
from the pre-change implementations in commit `09d7784`,
before any implementation changed, and replayed
post-conversion — **31/31 byte-identical** (all full-mode
canonical-JSON equality), in
`tests/test_spec087_s3_conversions_d.py`, alongside a
Refined-V2-vs-V1 cross-check (on identical rows the two
extractors differ only in verdict text and the [:120]
example-line truncation, in the rows and in confirmed_hits),
the converted-ids flag/provenance test, and the
primitives-in-palette test (34 tests in the file). Fixture
sources: the loaders behind the historical graphs read the
gitignored corpora/ tree, absent from this repository, so —
the PR-A/PR-C precedent — the inputs are synthetic records
in exactly the mesopotamian_contact shapes, built to exercise
every branch the conversion could move: an unmapped sign in
the reading (skeleton segment "?", gloss "(unmapped)"), a
keyword-gated tablet below the hit threshold, both readout
insufficient-input cases, penalty-bearing and
position-matching names, the allograph expansion adding a
rendering the static set lacks (16 → 17 renderings, and a
name that scores only through the added token), ePSD2 forms
with determinatives and subscript digits, a multi-form entry
whose best form is not its longest, the icount filter, cohort
boundaries (an empty cohort, the open-ended S9+ bin),
known-name matches in mixed case, empty candidate names
(skipped in rows, counted in by-pattern), and a 200-character
example line proving the three truncation rules (untruncated
/ [:120] / [:160]). Sanity was checked against hand
computation at capture (readout skeleton
`miin-vaTa-miin-?-muruku-eZu--miin`, n_miin 3; V1 matches 2,
V2 direct 2 / expanded 3 / new 1; reverse-V1 top candidate
`ur-miin-ba-kakkab-lu-x-mul` at 9.0 with positions [1,3,6]
and three penalty rows at −1.5; reverse-V3 top `MiinTest`
at 9.0; persons-v3 example line exactly 160 chars).

**27-graph comparison (contract item 4):** the S2 runner was
executed on a fresh worktree of `702cc717` (pre) and on this
branch (post), under the same two normalizations as
PR-A/PR-B/PR-C (LanguageModel repr addresses; each tree's
own root path). Database state, stated exactly as verified
first-hand (read-only): the pre side was a fresh worktree,
which has no `backend/data/` directory at all — its CGSA
reads met absent tables; the post side read this clone's
`backend/data/glossa.db`, whose CGSA tables are empty
(canonical_signs 0 rows, sign_cluster_assignments 0 rows) —
both sides exercised the same empty state. **27/27 graphs
byte-identical pre vs post** under the normalizations, and
every normalized hash also equals the PR-C table's hash for
the same graph (the environment's cross-check):

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

None of the 27 live graphs wires an F7/F6 node — the
comparison here is the no-live-behaviour-change proof for
the helper removals and the registry edits; the per-node
proof is the fixture equivalence above. The runs regenerate
`reports/*.json` in-tree as a side effect; those files were
restored and are not in this PR's diff.

### Test results

- Targeted suites (this branch): all six Spec 087 test
  files — `test_spec087_registry_integrity.py`,
  `test_spec087_palette_curation.py`,
  `test_spec087_s3_conversions.py` (PR-A),
  `test_spec087_s3_conversions_b.py` (PR-B),
  `test_spec087_s3_conversions_c.py` (PR-C),
  `test_spec087_s3_conversions_d.py` (this PR: 31 equivalence
  cases + the cross-check + flag/provenance + palette tests)
  — **184 passed**; plus the affected loader area,
  `test_mesopotamian_contact_loader.py` — in the same run as
  the PR-D file, **39 passed** combined.
- Full backend suite (this branch, TMPDIR on disk, the one
  named deselection
  `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`):
  completed in a single run (236.83s) — **2,404 passed, 84
  skipped, 1 failed, 1 error**. The one failure is the known
  phase133 local-only baseline
  (`test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`,
  missing local download; it does not fail CI). The one error
  is a teardown error of the session TestClient fixture
  surfaced at `test_tray_token_auth.py` (the test itself
  passed) — the tray teardown flake family PR-C's record
  names; it is in the shared fixture teardown, not in any
  module this PR touches.
- `python -m ruff check backend/` — clean.
- No frontend surface changed, so no builder-area frontend
  tests were required and no dist rebuild was needed.

### Claim assessments (this PR's legs)

- **C087-7 — PR-D leg supported.** 10 of the 64 CONVERT
  dispositions (families F7 + F6) are converted here with
  byte-identical fixture equivalence; cumulatively 38 of 64
  with PR-A, PR-B and PR-C. The remaining families' legs land
  with their own PRs.
- **C087-13 — PR-D leg supported.** The comparison runs over
  all 27 live graphs hold byte-identical under the named
  normalizations (above).
- **C087-17 — PR-D act recorded.** The census pin, the
  migration data file, and the S1/S2 test pins were re-pinned
  in this same PR, from the live registry, with the deltas
  tabled above.
- **C087-15 — PR-D manual leg.** `docs/user-manual.md`'s
  legacy section gains the short factual note (the three new
  generic blocks in the Palette; the ten converted nodes now
  legacy). The generated node reference is S4's scope.

### Departures from the brief's letter, stated plainly

- **T303 is still not ticked.** Its F7 + F6 legs are
  discharged here; six families remain (F2, F9, F10, F11,
  F12, F13), plus family F15 and the final retire-flagging
  batch. The progress note under T303 in tasks.md is updated
  instead of a tick.
- **The brief's expected arithmetic was right** (registered
  +3, legacy +10); the re-pin is nevertheless counted from
  the live registry, per the contract: 537 / 397 / 140,
  core 62, categories 65.
- **The brief's "one scoring core" needed one qualification**:
  the scoring core (positions, length, weights, penalty) is
  shared exactly as specified, but the family's two matching
  rules (substring for persons, exact-token for ePSD2) are
  both in the current code; the engine carries the matching
  rule as candidate-mode data rather than forcing one rule
  on both sources. Byte-identical fixtures are the proof no
  behaviour moved.
- **F6's "one aggregation pass" is likewise a family, not a
  single shape**: output key names (`all_rows_count` vs
  `rows_all`, `n_unique_candidates` vs `n_unique`), the three
  example-line truncation rules, and the two known-name
  sources differ by node in the current code; all are carried
  as spec data, none normalised.

## PR-E — family F9 (Phase-14 epistatic / grounding / structural / integrative machinery, the Phase-20 positional classifier, and the Indus-evidence null test)

**Branch:** `feat/087-s3-conv-e`, built on main `f40b1a99`
(PR #497 merged). **Commits:** `3b004db` (fixtures, captured
first), plus the implementation commit. **Seat:** build worker;
the parent gates and merges. The contract stated at the head
of this record governs unchanged.

### The generic machinery — appended to `backend/glossa_lab/generic_primitives.py`

PR-E appends eight engines to PR-D's module (same stdlib-only
pattern). F9 is the stage's most heterogeneous family — eight
nodes with no shared surface — so each node gets its own small
primitive, with its fixed content (rule tables, label sets,
thresholds, verdict texts) carried as spec data, per the
triage's per-node targets. Three of the engines codify
behaviour the batch's preparation had to read off the live
code exactly: the comparator's template is a per-key mean over
reference bundles with spread-normalised distances (not a
centroid over a nested feature tuple); the context
association's null re-accumulates token counts per shuffle and
z-scores the ROUNDED observed PMI; the null test's p-value is
the one-sided share of null rates at or above the observed
rate, floored at 1/n_null, with a population standard
deviation. The triage's caution for the null test is honoured:
the existing generic PermutationTest has score-shaped ports,
not sequence-shaped, so SignPositionNullTest is a separate
primitive and does not reuse it.

The eight primitives, registered in the core list immediately
after PersonsAggregator, each with inputs/outputs mirroring
its domain node and a description naming the delegating node:

| primitive | category | mechanism |
|---|---|---|
| InteractionSurplusProfile | Analysis | bigram PMI and trigram surplus over the pairwise baseline for frequent n-grams; counts at or above a spec-carried significance cut (nats) are significant; min counts, top_k, label are plain params. |
| OrderInformationProfile | Analysis | HED decomposition: per-symbol block entropies, successive differences as order contributions, unigram skew prepended; the regime is the first match of an ordered rule table over the f2/f1 and f3/f2 metrics, with a fallback regime — all spec data. |
| TokenContextAssociation | Analysis | per-token PMI between signs and a metadata context field against a context-shuffle permutation null (z-score + surplus over the null mean); significance cut, strong-verdict minimum, verdict templates, and the optional length binning (binned field, source field, [bound, name] bins, default bin) are spec data. |
| MetricFieldExtractor | Transforms | a flat metric vector from wired profiler bundles, driven by a field_map parameter: ordered extraction entries (a field of an input dict, the first row's field of a carried list, the field of the list row whose n equals a carried value, or the field of a list row at an index), each with a default and optional float coercion. |
| SignatureComparator | Analysis | flat signature bundles (one per port a..f) classified candidate / negative / reference by spec data (candidate tag + marker, negative-tag set); per-key mean template over references, spread-normalised Euclidean distances to the language template and the negative centroid, all bundles ranked; the target row's lang-minus-neg delta against the spec margin picks among spec verdict templates. |
| EvidenceRuleAggregator | Analysis | an ordered evidence rule table as data (range_pair, field_equals, list_fraction_checks, success_threshold kinds), each rule emitting a formatted for/against line; score = for − against, is_language at a spec score threshold, three verdict bands as spec templates gated by a spec confidence threshold; the CAS thresholds stay plain params named by the success_threshold rule. |
| PositionalClassClassifier | Analysis | index-based I/M/T position counts (a length-1 token counts as both initial and terminal), rates over the position-count total, adjacent-repetition rate; classification by a spec label set and ordered dominant-position rules (dominance threshold + secondary threshold as plain params), verdict as a spec template. |
| SignPositionNullTest | Analysis | a sign's edge rate (initial, or terminal for any other test type) against n_null shuffled re-deals (random.sample on the seeded global stream); population-std z-score, one-sided p floored at 1/n_null, verdict from a spec band table of [|z| threshold, verdict] pairs with a fallback. |

### The eight delegations

Each domain fn keeps its id, def, and docstring, and now
builds its spec and delegates. Fixed content at the delegation
point:

| domain node (module) | primitive | spec data passed |
|---|---|---|
| EpistaticInteractionDetector (phase14) | InteractionSurplusProfile | profile_spec.significance_cut = 2.0 |
| EpistaticOrderProfile (phase14) | OrderInformationProfile | profile_spec.regime_rules = [{language_like: f2/f1 >= 0.10 and f3/f2 >= 0.05}, {non_linguistic: f2/f1 < 0.05}], fallback_regime = ambiguous |
| SignContextAssociation (phase14) | TokenContextAssociation | association_spec: significance_cut 2.0, strong_min 5, binned_field length_bin over source field length with bins [[2, short], [5, medium]] and default long, the three verdict templates |
| DoFExtractor (phase14) | MetricFieldExtractor | field_map (setdefault): the eight-entry CAS renaming table — h1_norm from the block row with n == 3, h1_nats from the first block row, zipf_alpha / zipf_r2, mi_gamma / mi_r2_pow, epistatic_2nd / 3rd_norm from HED order rows 1 / 2 — every entry float-coerced with default 0.0. This is the parameter surface the triage says the node gains. |
| LanguageSignatureComparator (phase14) | SignatureComparator | comparator_spec: candidate_tag "indus" (the node's literal becomes the tag's default at the delegation point), candidate_marker "candidate", negative_tags [permut, shuffle, random, uniform], verdict_margin 0.25, feature_keys [alpha, gamma_mi, plateau_norm, epistatic_2, epistatic_3, h_norm_n3], the four verdict templates |
| LanguageDetectorVerdict (phase14) | EvidenceRuleAggregator | aggregator_spec.rules: the Zipf range_pair (alpha 0.85–1.30 and R² >= 0.85 for; alpha < 0.50 or R² < 0.50 against, r_squared with r2_zipf fallback), plateau field_equals, MI regime field_equals ×3 (power_law for with gamma; flat, exponential against), HED regime field_equals ×2 (language_like for with both ratios; non_linguistic against), the HED list_fraction_checks (orders[1] >= 0.10 for; orders[2] >= 0.05 for; orders[1] < 0.05 against), the CAS success_threshold (low/high from the cas_violation_low / cas_violation_high params, defaults 0.1 / 1.0); language_min_score 2, confidence_threshold 0.5, the three verdict templates. The node's live test consumer (test_spec086_stub_disposition.py, which calls the phase14 wrapper directly, fed and unfed) is in the targeted suites and passes unchanged. |
| FulsPositionalClassifier (phase20) | PositionalClassClassifier | classifier_spec: class_labels {numerical NUMERICAL, initial INITIAL, medial MEDIAL, terminal TERMINAL, mixed MIXED}, position_classes [initial I, terminal T, medial M] in the current code's evaluation order, the PREDICTION 4 verdict template. Every threshold was already a plain param (defaults min_count 5, dom 0.55, secondary 0.30, numerical_rr 0.20 — the fn's own defaults, unchanged). |
| IndusNullModelTest (indus_evidence) | SignPositionNullTest | null_spec.verdict_bands = [[3, STRONGLY_SIGNIFICANT], [2, SIGNIFICANT], [1.5, BORDERLINE]], verdict_fallback NOT_SIGNIFICANT |

The converted fns keep their modules, so the flag/provenance
test's `fn.__module__` pins hold. Phase-14's module-level
`random` import became unused with the SignContextAssociation
delegation and is removed (grep-verified: no remaining
`random.` use in the module outside a docstring word).

### Counts — the re-pin (C087-17 act for this PR)

| | before | after |
|---|---|---|
| registered | 537 | **545** (+ the eight primitives above) |
| legacy | 397 | **405** (+ the eight F9 conversions) |
| palette | 140 | **140** (−8 converted, +8 primitives) |
| core definitions | 62 | **70** |
| categories | 65 | **65** (no change) |

Per-category deltas: palette `Analysis` 14 → 21 (seven of the
eight primitives), palette `Transforms` 8 → 9
(MetricFieldExtractor). Legacy-by-category: `Phase-14 /
Epistatic` 1 → 3, `Phase-14 / Grounding` 2 → 3, `Phase-14 /
Structural` 0 → 2, `Phase-14 / Integrative` 0 → 1,
`Phase-20 / Sign function` 0 → 1, `Evidence Graph` 1 → 2.
The migration data file gains the eight ids under
`s3_additions["PR-E (F9)"]`; the census pin fixture is
regenerated from the live registry; the S2 agreement test's
converted set now holds PR-A's six, PR-B's nine, PR-C's
thirteen, PR-D's ten, and these eight — 46 of the 64 CONVERT
dispositions cumulatively.

### Equivalence and comparison results

**Fixture equivalence (contract item 3):** 36 cases captured
from the pre-change implementations in commit `3b004db`,
before any implementation changed, and replayed
post-conversion — **36/36 byte-identical** (all full-mode
canonical-JSON equality), in
`tests/test_spec087_s3_conversions_e.py`, alongside the
converted-ids flag/provenance test and the
primitives-in-palette test (38 tests in the file). All eight
nodes are pure functions of (inputs, params) over synthetic
inputs — no corpus files, no DB — so the inputs are built
deterministically (dedicated Random instances) to exercise
every branch the conversion could move: the detector's
significance cuts, parameterised min-counts, top_k slicing,
and the empty return; all three HED regime branches, the
max_order=2 shape (f3/f2 reads 0.0), and the empty return;
the length_bin bucketing with a strong verdict, top_k
slicing, a plain-field weak verdict, a uniform zero verdict,
and the misalignment error return; the DoF table full,
partial (no n == 3 block row, HED orders shorter than the
table), and empty; the comparator's three verdict bands, its
candidate classification by tag and by marker, the refs
fallback (no reference bundles), and the no-bundles early
return; the verdict aggregator's rule table branch by branch
(likely-language with seven for-lines, likely-not with five
against-lines, a mixed AMBIGUOUS at score 1, the CAS
between-thresholds silence, the same CAS input flipped to a
for-line by widening cas_violation_low, and the unfed shape
the Spec 086 stub-disposition test pins); the positional
classifier's five classes in one corpus (including the
length-1 I+T path and a below-min_count sign), a
custom-threshold run classifying a second INITIAL, and the
empty corpus; the null test's STRONGLY_SIGNIFICANT and
NOT_SIGNIFICANT bands and its three error returns (empty
sequences, no target, absent sign). Every case asserted its
intended branch at capture time; a failed assertion aborts
the capture rather than pinning a case that does not exercise
what its name claims. Sanity was checked against hand
computation at capture: for the locked-block detector corpus,
count(a1) = count(a2) = 30 of 270 unigrams and bigram
(a1, a2) = 30 of 180, so PMI = log((30/180) / ((30/270) ·
(30/270))) = log(13.5) = 2.6027, matching the capture.

**27-graph comparison (contract item 4):** the S2 runner was
executed on a fresh worktree of `f40b1a99` (pre) and on this
branch (post), under the same two normalizations as
PR-A/PR-B/PR-C/PR-D (LanguageModel repr addresses; each
tree's own root path). Database state, stated exactly as
verified first-hand (read-only): the pre side was a fresh
worktree, which has no `backend/data/` directory at all —
its CGSA reads met absent tables; the post side read this
clone's `backend/data/glossa.db`, whose CGSA tables are
empty (canonical_signs 0 rows, sign_cluster_assignments
0 rows, verified by a read-only sqlite query) — both sides
exercised the same empty state. **27/27 graphs
byte-identical pre vs post** under the normalizations:

| graph | normalized sha256 (pre == post) |
|---|---|
| fuls_independence_suite | d342f369479aa7fa48f0ee6716b1a552609a24a8ff8cdb4bbce22efe7fd199b5 |
| fuls_nw_semitic_benchmark | 0db9ea0aa6e3d7ac8e8b45432e1975302ee6151456e0bfd8fb5d3906d63c5aa0 |
| fuls_validation_suite | 4bac5b7e0291658e4976b74f6a9e66a8862a9f7816180f040e00b2655bd5316f |
| generic_sa_multi_comparison | 63d6cf5a4ec488ba46a2e4eb09f517bddb77789c3ecaad643fb3f3fd4fabbf45 |
| indus_anchor_sweep | 20472e8966640ff8ecef3030b388dc75ad54ec1e2578e5e68e07c8540133b1ad |
| indus_cgsa_cluster_analysis | 5a8447a60f9d7de9be9204c3b153614f76070ab3ea1aef2956e97c2c7b6096f6 |
| indus_cisi_anchored_10 | 002318a287ccbfba6dc2da9b5ac82f357464eab2c3bd283b147729a6d5488f3a |
| indus_cisi_dravidian_vs_pali | da9ede56e4b23f5b70ef4845a72de996fa50a62cab9545f897b4abdd49a370ad |
| indus_cisi_dravidian_vs_sanskrit | 95067e3ffce2c6f8ea8f90c3a43afcaeb2de02337de18811201cf87febbcd62d |
| indus_cisi_sa_dravidian_vs_nw_semitic | 9d64143ea94b42661f1571dd585c69324d3b2ffaef97ed85937681b75544b8aa |
| indus_cisi_sa_dravidian_vs_sanskrit | 1994a12beb209dbc6c640fbb83c0530a28e5f951adb9f7423515aef1e7f3a3cf |
| indus_cisi_structural | 16aa6dd0a0f3e5321dba5a351295123125c8e7e85186bf518936f1f443e55a0a |
| indus_contact_zone_v2 | f5079c8eb69f61a47969756c6182e4096021df1316bcb04946679aa86d4d7915 |
| indus_dravidian_vs_sanskrit | b2dbfa339103821e63594cbe61826dd0b343e6e350d7016d0f36607754914aea |
| indus_kalyanaraman_crossval | 46edd9a500ff6c7ecd7fbf62743af678c27ceb7418bba5c69cfad8e35306e777 |
| indus_sa_dravidian | 16ad6cb0aa2d04d74e3a63cebf157229af7e819f226a5fbc3ee13438fe5f0379 |
| indus_sa_dravidian_syllable | c8717ef983f6c2366bd0ef58e6bc05751fd933fb90a6c88e5a3fbdeb46314a90 |
| indus_sa_dravidian_vs_nw_semitic | b281219fd42efe0f30ec5ffeea866198944fa5b439786b022a1e687ba3a7e14b |
| indus_sa_dravidian_vs_sanskrit | d54156e6c2bfd720489570363d67c13d0e78c06e0556cbdb7ef9826a4ab1a09d |
| indus_sa_sanskrit_falsification | fa37f9a1fc055dda56ad819457fa788238d084341effa98e5fee40c780df6d31 |
| indus_sign_function_dravidian | 5e4cb13821f0cf3a93132d047e9ed0a5238a35121f976ef6e0b851166d1ab102 |
| indus_structural_atlas | b4b880f475f8cbe4b7c401b1caf2ba66c01fbc7ac52c3cc11975ca9a73441760 |
| indus_validation_a1_a3_holdout | 142f9657df4639734d3ead8d1a4322262f295de400c2028027bc188e9600196a |
| indus_validation_neg_controls | 72999b71c688353c1d0890c46729c07de8a98795b303a4ac7e66eb66de376c39 |
| kl_comparison | cf9a8e10b3043bc8942c29483118739688a02439fe20d5237f9d98e1647cca9c |
| ugaritic_sa_decipher | 8218b59a5f191723c26744aaf1dcf7933373c37e4a1a23843a161b8f9e498181 |
| ventris_validation | 78b20ce88b05687528375526e0c92015a588e6ebf0e5c0819851eb493da30312 |

None of the 27 live graphs wires an F9 node — the comparison
here is the no-live-behaviour-change proof for the registry
edits; the per-node proof is the fixture equivalence above.
The runs regenerate `reports/*.json` in-tree as a side
effect; those files were restored and are not in this PR's
diff. (The post-side run was repeated after a VM replacement
killed the first attempt mid-run; the pre-side outputs,
written before the replacement, were re-verified on disk and
the comparison is over the two output files, both read
first-hand. The normalized hashes differ from PR-D's table
for 25 of the 27 graphs — the two runs' environments are not
the same state — so, unlike PR-B/PR-C/PR-D, no cross-batch
hash equality is claimed; the contract's proof is pre vs post
within this PR, and it holds 27/27.)

### Test results

- Targeted suites (this branch): all seven Spec 087 test
  files — `test_spec087_registry_integrity.py`,
  `test_spec087_palette_curation.py`,
  `test_spec087_s3_conversions.py` (PR-A),
  `test_spec087_s3_conversions_b.py`,
  `test_spec087_s3_conversions_c.py`,
  `test_spec087_s3_conversions_d.py`,
  `test_spec087_s3_conversions_e.py` (this PR) — plus the two
  affected-area suites named in the brief,
  `test_spec086_stub_disposition.py` (the
  LanguageDetectorVerdict live consumer) and
  `test_indus_evidence_api.py`: **256 passed** (237.97s).
- Full backend suite (this branch, with the single named
  deselection
  `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`):
  completed in a single run (257.95s) — **2,442 passed, 84
  skipped, 1 failed, 1 deselected**. The one failure is the
  known phase133 local-only baseline
  (`test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`,
  missing local download; it does not fail CI). No teardown
  error appeared in this run (the tray flake family did not
  fire).
- `python -m ruff check backend/` — clean.
- No frontend surface changed, so no builder-area frontend
  tests were required and no dist rebuild was needed.

### Claim assessments (this PR's legs)

- **C087-7 — PR-E leg supported.** 8 of the 64 CONVERT
  dispositions (family F9) are converted here with
  byte-identical fixture equivalence; cumulatively 46 of 64
  with PR-A, PR-B, PR-C and PR-D. The remaining families'
  legs land with their own PRs.
- **C087-13 — PR-E leg supported.** The comparison runs over
  all 27 live graphs hold byte-identical under the named
  normalizations (above).
- **C087-17 — PR-E act recorded.** The census pin, the
  migration data file, and the S1/S2 test pins were re-pinned
  in this same PR, from the live registry, with the deltas
  tabled above.
- **C087-15 — PR-E manual leg.** `docs/user-manual.md`'s
  legacy section gains the short factual note (the eight new
  generic blocks in the Palette; the eight converted nodes
  now legacy). The generated node reference is S4's scope.

### Departures from the brief's letter, stated plainly

- **T303 is still not ticked.** Its F9 leg is discharged
  here; five families remain (F2, F10, F11, F12, F13), plus
  family F15 and the final retire-flagging batch. The
  progress note under T303 in tasks.md is updated instead of
  a tick.
- **The brief's expected arithmetic was right** (registered
  +8, legacy +8, palette unchanged); the re-pin is
  nevertheless counted from the live registry, per the
  contract: 545 / 405 / 140, core 70, categories 65.
- **No cross-batch graph-hash equality is claimed** (see the
  comparison note above): PR-D's published table was produced
  in a different environment state, and 25 of 27 normalized
  hashes differ from it. The within-PR pre/post proof is
  unaffected.
- **Two engines carry documented simplifications of
  malformed-input behaviour, neither reachable from the
  fixture set or the defs' shapes:** MetricFieldExtractor's
  field-map reads default rather than raise on a missing key
  inside a present row (the pre-change DoFExtractor indexed
  one such read directly), and EvidenceRuleAggregator's
  range_pair coerces a null alpha / R² to 0.0 where the
  pre-change verdict fn would raise on float(None). On every
  well-formed input the outputs are byte-identical, which the
  36 fixtures prove over the branches the conversion could
  move.

## PR-F — families F2, F10, F11, F12, F13 and F15 (the final conversion batch), plus the retire-candidate flags

**Branch:** `feat/087-s3-conv-f`, built on main `01fb4c57`
(PR #498 merged). **Commits:** fixtures captured per family
before that family's implementation, in family order —
`bfeeaff` + `d0133d9` (F2), `c488e01` + `e9a757a` (F10),
`4fd4d31` + `c5e3b4b` (F11), `92031e2` + `dc22393` (F12),
`f516015` + `b691e74` (F13), `e92b64b` + `900d80e` (F15) —
then `efc853f` (the legacy flags and the census re-pin) and
`89472a0` (imports left unused by the delegations, removed;
ruff clean). **Seat:** build worker; the parent gates and
merges. The contract stated at the head of this record
governs unchanged. This batch closes Stage S3's conversion
programme: every CONVERT disposition in the triage is now
discharged, and the four RETIRE-CANDIDATE dispositions are
executed as legacy flags with no implementation change.

### The generic machinery

Ten engines are appended to `backend/glossa_lab/
generic_primitives.py` and one to `backend/glossa_lab/
generic_loaders.py`, in the established stdlib-only pattern.
Each carries its family's fixed content (thresholds, caps,
templates, grammars, band tables) as spec data:

| primitive | category | mechanism |
|---|---|---|
| JsonRecordDirLoader (generic_loaders.py) | Sources | a directory of JSON record files in two modes: search (filter one directory's records by query fields over a second directory's id set) and records (load a record set with counts by a field), with record-shaping fill templates and a schema-defaults mechanism as spec data. |
| PositionalClaimTester | Analysis | positional claims about signs tested against corpus statistics: claims classified by type keywords, the prediction parsed for the claimed position, the observed rate compared against the corpus average under a spec support multiplier; claims the corpus cannot test produce no verdict row, as before. |
| RecordGroupSummary | Analysis | record-group summaries driven by ordered section specs (counts, counters, rows, derived rows, match and presence counts, verdict blocks) with per-record computed fields; one engine covers reporter, auditor and upgrade shapes whose differences are entirely spec data. |
| CorpusComparisonStats | Analysis | per-corpus sign statistics across compared corpora (loaded, direct, and direct-counts legs), with the "?" filter, the scale-up rounding and the corpus specs as data. |
| PrefixFindspotAssigner | Analysis | findspot assignment by catalogue-id prefix in two modes — reporter (key-presence match) and filter (truthy-info match) — with the prefix lengths [4, 3, 2, 1] as data. |
| CorpusCooccurrenceCheck | Analysis | co-occurrence of place-name terms across two corpora: the term set is every string value of the reference entries lowercased, matched bidirectionally as substrings with a length guard, hits and misses capped as data. |
| PredictionVerdictAggregator | Analysis | per-prediction verdicts assembled from shaping specs (per-bin extraction, verdict shaping, numerical-weights synthesis) and rule kinds as data (text_match, count_threshold, gap_rise, gap_spread, poisson_fraction), in flat and nested assemblies. |
| VisionOCRNode | Sources | vision OCR over a PDF catalogue under a spec line grammar (SEAL:/SIGNS:, ICONOGRAPHY:/MOTIF:, SIGN_REF:/MEANING:), with a pinned prior-results no-OCR branch, per-page error records, and results written back as data; paths, prompt, dpi and grammar are spec data. |
| CatalogTextParser | Analysis | inscription records parsed from catalogue text: the site-prefix set, tail patterns, the sign-sequence pattern, the Unicode block and the four verdict thresholds are spec data. |
| SyllableLMLoader | Sources | a syllable-level LM built from its JSON form: stored bigram log-probs exponentiated, unigram counts derived from bigram endpoints, the ranked list ordered by those counts; the phase module's shared builder delegates here, so the Sanskrit loader's code path is the same engine. |
| LexiconCrossValidator | Analysis | an anchor set cross-validated against an external rebus lexicon: readings normalised to root sets, each lexicon reading corroborated, conflicting or a new candidate under spec caps; rebus pairs matched through the root index; a grammar/content split and a banded complementarity score close the summary; paths, markers, caps, bands and frames are spec data. |

### The eighteen delegations

Each domain fn keeps its id, def, and docstring, and now
builds its spec and delegates:

| domain node (module) | primitive |
|---|---|
| IndusLiteratureLoader (indus_evidence) | JsonRecordDirLoader, search mode; the evidence-base paths resolve from the module constants at call time |
| IndusClaimsLoader (indus_evidence) | JsonRecordDirLoader, records mode |
| IndusClaimTester (indus_evidence) | PositionalClaimTester; type keywords position/sign_value/sign_function, support multiplier 1.2 |
| IndusSealsAtMesopotamiaSummary (phase22) | RecordGroupSummary |
| MeluhhaCorpusReporter (phase22) | RecordGroupSummary |
| SealSignAuditor (phase23) | RecordGroupSummary |
| LaursenTable1Auditor (phase24) | RecordGroupSummary; the "INDUS" substring rule, the 121-row expectation and the [:80] cap as spec data |
| SealSignUpgradeAuditor (phase24) | RecordGroupSummary; the xref field laursen_2010_seal_no and the [:120] rationale truncation as spec data |
| Phase29CorpusStats (phase29) | CorpusComparisonStats; the wrapper still calls the module-level F1 loaders and passes their outputs as the direct leg, which is the fixture stub point — both loaders return available: false in this tree, verified by direct call |
| CISIFindspotReporter (phase27) | PrefixFindspotAssigner, reporter mode |
| ShuIlishuContactZoneFilter (phase26) | PrefixFindspotAssigner, filter mode; its contact_zone_prefixes input is evaluated and discarded by the engine, exactly as the original — classification comes from the findspot map |
| MeluhhaCooccurrenceCheck (phase22) | CorpusCooccurrenceCheck, under the named pin below |
| Phase20Verdict (phase20) | PredictionVerdictAggregator; its four prediction specs as data, including P3's partial_first text rule (P3 has no plain-CONFIRMED outcome) |
| Phase21Verdict (phase21) | PredictionVerdictAggregator; its numeric rule set as data, nested assembly |
| CISIVol3OCRNode (phase28) | VisionOCRNode; the module's default OCR prompt passed as spec data |
| CMCatalogParser (phase20) | CatalogTextParser; site prefixes, Unicode block U+12F90–U+12FFF, thresholds 30/100/50/20 as data |
| DravidianSyllableLM (phase30) | SyllableLMLoader; an lm_path param may override the bundled file |
| KalyanCrossValidation (kalyanaraman) | LexiconCrossValidator; paths resolve from the module constants at call time; the module's private _normalise helper is removed with the delegation (no external users, grep-verified) |

**The Meluhha named pin (F11):** the node's corpus file
`backend/reports/meluhha_corpus_audit.json` is ABSENT from
the repo, and the node runs against an empty term set today.
The conversion fixture creates the file for the presence
cases (staged from the fixtures tree and removed in a
finally block, absence asserted before and after) and pins
the absence behaviour; the committed fixture corpus lives
under `tests/fixtures/spec087_s3_conv_f/`, never in
`backend/reports/`.

**The F13 OCR pin:** no fixture makes a live OCR or
provider call, and no restricted scan content appears in
fixtures. The no-OCR branch replays against pinned
prior-results files; the OCR branch replays as the parse of
pinned synthetic transcripts, with the vision entry point
stubbed and the prompts the engine sends merged into the
compared result. Two capture-time assertions were corrected
to the code's real behaviour: ID-only pages do not set
page_signs_found (only sequence/Unicode matches do), and
duplicate inscription ids on different pages survive the
per-(page, id) dedupe.

### The four retire-candidate flags

Executed per the owner's 2026-11-03 ruling (legacy-flagged,
never deleted), with NO implementation change — the fns are
byte-identical to their pre-PR state; only the flag data
moves:

| id | module |
|---|---|
| ShuIlishuCandidateFilter | experiment_graph_phase26 |
| Phase22Verdict | experiment_graph_phase22 |
| Phase23Verdict | experiment_graph_phase23 |
| Phase24Verdict | experiment_graph_phase24 |

They are recorded in the migration data file under their
own `s3_additions` key, `"PR-F retire-candidates"`, distinct
from the converts' `"PR-F (F2+F10+F11+F12+F13+F15)"`.

### Counts — the re-pin (C087-17 act for this PR)

Counted from the live registry after the conversions and
flags landed (never assumed):

| measure | before | after | delta |
|---|---|---|---|
| registered | 545 | 556 | +11 primitives |
| legacy-flagged | 405 | 425 | +20 newly flagged |
| default palette | 140 | 131 | +11 in, −20 out |
| core-registered | 70 | 81 | +11 |
| categories | 65 | 65 | unchanged |

The flag delta is +20, not +22: the eighteen converts and
four retire-candidates take the flag in this PR, but the two
F15 wrappers (DravidianSyllableLM, KalyanCrossValidation)
were already legacy-flagged in S2 — they are census WRAPPERs
(no input ports, empty params schema) — so their conversion
adds no new flag. The palette test's identity is amended
accordingly, with the overlap named as a set of two
(WRAPPER_CONVERTED_OVERLAP) rather than absorbed silently.
All eleven new primitives sit in existing categories
(Sources: JsonRecordDirLoader, VisionOCRNode,
SyllableLMLoader; Analysis: the other eight), so the
category count does not move. Cumulative S3 dispositions:
46 prior converts + 16 family converts here = 62 conversions,
+ F14's 2 relabels = the triage's 64 CONVERT dispositions
discharged; 4 RETIRE-CANDIDATEs flagged; the 2 F15 live
wrappers (outside the 68) converted. Nothing stopped: every
node in scope reached byte-identical equivalence.

### Equivalence and comparison results

**Fixture equivalence (contract item 3):** 74 cases
captured from the pre-change implementations, per family,
before any implementation changed (F2 15, F10 13, F11 12,
F12 10, F13 13, F15 11), and replayed post-conversion —
**74/74 byte-identical** in
`tests/test_spec087_s3_conversions_f.py`, alongside the
converted-ids flag/provenance test (which also pins the
four retire-flagged ids' provenance), the
primitives-in-palette test, and the LM-mode digest
comparison for the syllable LM (the LanguageModel object
itself is compared through a canonical digest of its
symbols, alphabet, size, ranked list and frequency tables).
Real-file cases pin measured behaviour: the Dravidian LM
file yields 2,293 bigrams and 655 syllables; the Kalyan
cross-validation over the real files yields 287 anchors,
144 Kalyanaraman signs, 105 overlap, 0 corroborated, 384
conflicting, 113 new candidates, complementarity 1.0,
verdict COMPLEMENTARY. Synthetic cases pin every verdict
band of both F15 engines (including HIGH_AGREEMENT at score
0.0 and the no-overlap COMPLEMENTARY), the per-sign and
output caps, and both missing-file error texts. The
Shu-ilishu filter cases run against the real CISI corpus
(170 records of length ≥ 3, 138 in the 3–7 band).

**27-graph comparison (contract item 4):** the S2 runner
was executed on a fresh worktree of `01fb4c57` (pre) and on
this branch (post), under the same two normalizations as
PR-A…PR-E (LanguageModel repr addresses; each tree's own
root path). Database state, stated exactly as verified
first-hand (read-only): the pre side was a fresh worktree,
which has no `backend/data/` directory at all — its CGSA
reads met absent tables; the post side read this clone's
`backend/data/glossa.db`, whose CGSA tables are empty
(canonical_signs 0 rows, sign_cluster_assignments 0 rows,
verified by a read-only sqlite query before the run) —
both sides exercised the same empty state. **27/27 graphs
byte-identical pre vs post** under the normalizations,
including the two graphs that wire the F15 wrappers
(`indus_sa_dravidian_syllable`, `indus_kalyanaraman_crossval`)
and the graph wiring MeluhhaCooccurrenceCheck
(`indus_validation_a1_a3_holdout`):

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

The runs regenerate `reports/*.json` in-tree as a side
effect; those files were restored and are not in this PR's
diff. No cross-batch hash equality is claimed (the runs'
environment states differ across batches); the contract's
proof is pre vs post within this PR, and it holds 27/27.

### Test results

- Targeted suites (this branch): all eight Spec 087 test
  files: **298 passed, 1 skipped**. The F2 loaders' live
  consumers named in the brief —
  `test_evidence_atomic_nodes.py`,
  `test_graph_experiments.py` — plus
  `test_indus_evidence_api.py`: **96 passed**.
- Full backend suite (this branch, with the single named
  deselection
  `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`):
  completed in a single run (521.91s) — **2,519 passed, 84
  skipped, 1 failed, 1 deselected**. The one failure is the
  known phase133 local-only baseline
  (`test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`,
  missing local download; it does not fail CI). No teardown
  error appeared in this run (the tray flake family did
  not fire).
- `python -m ruff check backend/` — clean.
- No frontend surface changed, so no builder-area frontend
  tests were required and no dist rebuild was needed.

### Claim assessments (this PR's legs)

- **C087-7 — supported, and the S3 conversion programme is
  complete.** All 64 CONVERT dispositions are discharged
  (62 conversions + the 2 F14 relabels), the 4
  RETIRE-CANDIDATE dispositions are executed as flags, and
  the 2 F15 live wrappers are converted — every conversion
  with byte-identical fixture equivalence, none stopped.
- **C087-13 — PR-F leg supported.** The comparison runs
  over all 27 live graphs hold byte-identical under the
  named normalizations (above), including the two graphs
  wiring the converted live wrappers.
- **C087-17 — PR-F act recorded.** The census pin, the
  migration data file, and the S1/S2 test pins were
  re-pinned in this same PR, from the live registry, with
  the deltas tabled above.
- **C087-15 — PR-F manual leg.** `docs/user-manual.md`'s
  legacy section gains the short factual note (the eleven
  new generic blocks in the palette; the eighteen converted
  nodes now legacy; the four retire-candidates flagged). The
  generated node reference is S4's scope.
- **T303 is ticked in this PR.** Every S3 conversion and
  retire-flag disposition has landed, which is the tick
  condition; the progress note under T303 records the
  completion arithmetic.

### Departures from the brief's letter, stated plainly

- **The brief's expected arithmetic was off in two places;
  the re-pin is counted from the live registry, per the
  contract.** Registered grows by +11 primitives, not +10:
  F15's two wrappers take two distinct primitives
  (SyllableLMLoader, LexiconCrossValidator), not one shared
  form. Legacy grows by +20, not +22: the two F15 wrappers
  were already legacy-flagged as census WRAPPERs in S2 (see
  the counts section). The counted values are 556 / 425 /
  131, core 81, categories 65.
- **The triage's IndusClaimsLoader schema defaults do not
  exist in the code.** The brief (after the triage) names
  schema defaults — status "needs_extraction", confidence
  "UNCERTAIN" — as data params; the pre-change loader
  passes claims through unchanged (its counts read
  `.get(..., "unknown")`). The delegation therefore passes
  `schema_defaults: {}`: the JsonRecordDirLoader mechanism
  exists and is exercised by the fill templates, inert for
  this node, and the fixtures pin the pass-through
  behaviour. Two further first-hand corrections to the
  triage's F2 account: the literature loader's claim_count
  reads the claims file's `total_claims` field, and the
  claims restriction is by file stem against the upstream
  papers' document_ids.
- **F10's fixture capture initially destroyed input dict
  order.** The first capture canonicalized inputs with
  sorted keys; two F10 nodes stable-sort on keys whose ties
  follow insertion order (Meluhha period/provenience), so
  the pinned inputs no longer represented the code's real
  inputs. The capture was fixed to store inputs
  order-faithfully (expected outputs remain canonical) and
  F10 was re-captured against the pre-change worktree
  before its implementation commit; the other families'
  captures were audited for the same defect (their inputs
  carry no order-sensitive ties; F2/F11 corpora are read
  from disk in both capture and replay).
- **The F2 implementation was first committed with
  in-tree regenerations included** (test runs rewrite
  `glossa-indus/claims/extracted_claims/`). The commit was
  soft-reset before pushing, the tree restored, and the
  implementation recommitted with explicit paths only; no
  regeneration is in this PR's diff. Later families
  committed with explicit paths throughout.
- **pymupdf was missing from the local venv** although
  `backend/pyproject.toml` declares it (`pymupdf>=1.24,<2`);
  it was installed into the venv (1.28.2) for the F13
  fixtures. CI installs it from pyproject, so this is a
  local-environment note, not a code change.
