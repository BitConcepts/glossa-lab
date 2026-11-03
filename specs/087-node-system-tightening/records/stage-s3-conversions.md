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
