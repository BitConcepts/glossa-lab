# Stage S3 record — M77 silent Holdat fallback retirement (Spec 087)

**Stage:** S3 follow-on to the M77 Step 0 record (PR #492).
**Branch:** `feat/087-s3-m77-fallback`, built on main `50e91a63`
(PR #492, the merged M77 Step 0 record). **Date:** 2026-11-03.
**Seat:** build worker; the parent gates and merges.

## Owner approval

Tristen approved this change on 2026-11-03, tapping the option:
"Proceed as recommended: finish the desktop check, bring the
decoded file into the record, run the real comparison, and retire
the silent Holdat fallback." This PR is the fallback-retirement
leg of that approval. The defect it retires was recorded in the
merged M77 Step 0 record (PR #492): when the decoded JSON
(`reports/mahadevan_texts_decoded.json`) was missing, the M77
inscription loading path silently substituted the Holdat
CISI-grouped corpus — which corpus a consumer received depended
on which files happened to exist, with no signal.

## Where the fallback lived

- `backend/glossa_lab/experiment_graph_phase20.py`,
  `_m77_inscription_loader`: the loader's spec listed the decoded
  JSON report first and the Holdat CSV (grouped) second.
- `backend/glossa_lab/generic_loaders.py`,
  `json_corpus_loader_execute` (the generic JsonCorpusLoader
  engine the loader delegates to since PR-A): its source loop
  picked the **first existing** source. That first-existing-wins
  loop is the silent substitution — no parameter, no log, no
  output field named which corpus was served.

The M77 spec chain is the only multi-source JsonCorpusLoader
chain in the tree (the phase29 specs are single-source JSON), so
the engine change below is opt-in per spec and cannot move any
other loader.

## The change

Engine (`generic_loaders.py`), two opt-in spec features,
documented in the module docstring:

- `source_select_param`: the name of a node param that selects
  one source by its `"name"`. When the param is set, the chain
  is restricted to exactly the named source; an unknown name
  returns an explicit error
  (`JsonCorpusLoader: unknown source '<value>'; choose one of:
  <names>`).
- A source may carry `"explicit_only": True`: it is skipped by
  the default chain and served only when named through
  `source_select_param`.

The engine's absent-corpus context computation (including the
`fallback_path` taken from `sources[1]`) is untouched, so the
M77 absent-corpus error text is byte-identical to before.

M77 loader (`experiment_graph_phase20.py`):

- The decoded source is named `"decoded"`; the Holdat source is
  named `"holdat"` and marked `explicit_only`; the spec gains
  `"source_select_param": "source"`.
- The node definition gains a `source` parameter:
  `{"type": "string", "default": "decoded", "enum": ["decoded",
  "holdat"]}`. The node description now states plainly that the
  Holdat CSV corpus is loaded only when `source='holdat'` is set
  explicitly and that there is no automatic fallback. The
  `_m77_inscription_loader` docstring was rewritten to match.

### What changed

- Default behaviour with the decoded JSON absent: the loader no
  longer serves the Holdat corpus silently. It returns the
  explicit absent-corpus error — the same error it already
  returned when both files were absent.
- Holdat is reachable only as a deliberate choice:
  `source="holdat"`.
- An unknown `source` value is an explicit error naming the
  valid choices.

### What did not change

- Any output when the decoded JSON is present (default or
  `source="decoded"`): byte-identical, pinned.
- The Holdat path's own outputs when explicitly selected:
  byte-identical, pinned (same payloads as the retired fallback
  cases carried).
- The absent-corpus error text: byte-identical.
- Every other loader and node: the engine features are opt-in
  and only the M77 spec uses them.

## Re-pinned conversion cases

File: `backend/tests/fixtures/spec087_s3_conv_a/expected.json`
(the PR-A conversion pins for `M77InscriptionLoader`; 39 cases
after this change). Three cases exercised the silent fallback —
absent decoded JSON silently yielding Holdat output. Each is
re-pinned as explicit-source behaviour with its expected payload
**unchanged**; the move is the approved behaviour change above,
not a regression: the corpus served is now the one the caller
named.

- `m77_fallback_default` → `m77_holdat_explicit_default`
  (params gained `"source": "holdat"`).
- `m77_fallback_min3` → `m77_holdat_explicit_min3`
  (params gained `"source": "holdat"`).
- `m77_fallback_raw_ignored` → `m77_holdat_explicit_raw_ignored`
  (params gained `"source": "holdat"`).

Three new cases pin the retired behaviour:

- `m77_no_silent_fallback`: decoded JSON absent, Holdat CSV
  present, no `source` param → the absent-corpus error (the
  pre-existing `m77_absent` error payload, verbatim).
- `m77_holdat_selected_but_absent`: decoded JSON present,
  Holdat CSV absent, `source="holdat"` → the same absent-corpus
  error. An explicit choice is honoured exactly, never widened
  to another corpus.
- `m77_unknown_source`: `source="bogus"` →
  `{"error": "JsonCorpusLoader: unknown source 'bogus'; choose
  one of: decoded, holdat"}`.

No byte-identical pin for the JSON-present path or the Holdat
path moved.

## Manual and in-app help prose

Grep evidence, 2026-11-03: `docs/user-manual.md` contains no
mention of Holdat at all, and its only "fallback" passage
concerns MappingInference GPU→CPU. `docs/USER_GUIDE.md`'s
"fallback" passages concern model-bucket primary/fallback slots.
The frontend's Holdat mentions concern a separate `corpus_file`
API and program-item text, not this loader. No prose anywhere
described the M77 fallback as automatic except the loader's own
docstring and node description, both corrected in this PR. No
manual correction is owed.

## Proofs

- Targeted suites (`tests/test_spec087_s3_conversions.py`,
  `tests/test_spec087_registry_integrity.py`,
  `tests/test_spec087_palette_curation.py`): 68 passed,
  0 skipped — includes all 39 conversion cases with the new
  pins.
- 27-graph execution comparison (S2/S3 method; per-graph
  SHA-256 over canonicalised per-node results, LanguageModel
  repr addresses normalised): **27/27 byte-identical** to the
  pre-change run in this same tree. In this tracked-only tree
  both the decoded JSON and the Holdat CSV are absent, so the
  three live graphs using `M77InscriptionLoader`
  (`indus_sa_dravidian_syllable`,
  `indus_sa_sanskrit_falsification`,
  `indus_validation_neg_controls`) returned the absent-corpus
  error before the change and return the identical error after;
  the comparison proves nothing else moved.
- Full backend suite (only deselection:
  `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`,
  the named VM-environmental stall): **2288 passed, 84 skipped,
  1 deselected, 1 failed** — the single failure is the known
  local-only baseline,
  `test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`;
  CI is authoritative for it.
- `python -m ruff check backend/`: all checks passed.
