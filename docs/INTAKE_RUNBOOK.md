# Intake Runbook — Independent-Data Intake Pack (Phase-130, spec 021)

How a newly arrived inscription dataset is received by Glossa
Lab: from first provenance capture to the Phase-119 harness's
labelled dry run — and no further.

> **STRUCTURAL RULE.** Intake output can only ever reach the
> Phase-119 harness's **dry-run** path (spec 018 §8). The
> intake module (`backend/glossa_lab/intake.py`) does not
> import the harness's scoring path at all — the gate is in
> the code, not in reviewer vigilance. **Evaluation of any
> prediction on an intake dataset requires its own future
> spec and separate owner authorization.** A completed intake
> is never an evaluation, produces no verdict, and updates no
> field of `docs/PREDICTION_REGISTER.md`.

Code: `backend/glossa_lab/intake.py` (validator, evaluability
assignment, pipeline `run_intake`), `backend/glossa_lab/dedup.py`
(shared spec 018 §5 dedup), schema
`data/intake/intake_dataset_schema_v1.json`.

## Stage 0 — Provenance capture

Before any file is opened for content, record — in the
candidate dataset JSON itself (intake schema v1):

- dataset-level: `dataset_name`, `source` (origin
  description / path / URL), `compiler`, `acquisition_date`,
  `upstream_lineage` (`derived_from`,
  `is_derivation_input`, optional `upstream_dataset_ids`).
- per-inscription: `inscription_id` (source-assigned),
  `provenance.source_reference` (where the record comes from
  in the source), plus declared `object_type`, `context`,
  `period`, `artifact_hash` where the supplier provides them.

If provenance cannot be stated, intake stops here. An
unprovenanced dataset is not validated "provisionally".

## Stage 1 — License gate

`license_basis` must be present and non-empty: the license
or acquisition basis, verbatim where known (spec 018 §7's
provenance `license` field; §6.1.2 makes it a precondition
of any downstream use).

**A dataset with no declared lawful basis is REJECTED —
never passed with a warning.** (Validator code:
`LICENSE_BASIS_MISSING`.) Precedent: Phase-122's mayig layer
is committed to the repo because its MIT license was
verified from the source's LICENSE file at acquisition; the
ICIT converted layers, whose terms do not permit that, live
in the gitignored downloads tree with statistics only
published. The gate is where that distinction is decided.

## Stage 2 — Schema validation

`validate_dataset(dataset)` →
`{"verdict": "pass" | "pass-with-warnings" | "reject",
"errors": [...], "warnings": [...], "summary": {...}}`.

Rejects carry named codes: `LICENSE_BASIS_MISSING`,
`SIGN_LIST_UNDECLARED` (missing/unknown declared sign list),
`DUPLICATE_INSCRIPTION_ID`, `SOURCE_CLASS_INVALID`,
`REQUIRED_FIELD_MISSING`, `TYPE_ERROR`, `EMPTY_DATASET`,
`SCHEMA_VERSION_UNSUPPORTED`, `INVALID_DATE`.

Required fields are exactly those spec 018 consumes (schema
§2 of spec 021). Missing optional-but-declared fields
(`compiler`, `acquisition_date`, `object_type`, ...) warn,
they do not reject; token/format mismatches against the
declared sign list warn (`TOKEN_FORMAT_MISMATCH`) because
segmentation variants are a crosswalk question (§Stage 5
note), not a validity question.

A `reject` ends intake: no dedup, no dry run, and the
dataset is not stored as an intake artifact. Fix the dataset
with the supplier — never edit a received dataset into
compliance locally.

## Stage 3 — Deduplication

`glossa_lab.dedup.dedup` — the frozen spec 018 §5 protocol,
shared verbatim with the Phase-119 harness:

- **Stage A — exact**: identical full token sequence → drop.
- **Stage B — sentinel-normalized exact:** `UNK`-stripped
  sequence identical (and non-empty) → drop.
- **Stage C — near-duplicate:** `UNK`-stripped length ≥ 4
  within Levenshtein distance ≤ 1 of an earlier KEPT record
  → drop (keep-first; kept anchors only, no chaining).

At intake this runs on the declared-space token lists as a
pre-adapter pre-check; the harness dry run (Stage 5)
re-applies the same module post-adapter, where §5 makes it
authoritative. Per-stage removed counts are mandatory
outputs of every run. Reference numbers (spec 018 App. A.6,
ICIT converted layer, P-space): 4,531 in → 1,468 / 370 / 247
removed → 2,446 kept (46.02% cumulative) — reproduced through
this module in the Phase-130 tests.

## Stage 4 — Evaluability-class assignment

`assign_evaluability(dataset)` assigns, from the declared
`source_class` and the frozen spec 018 §4 matrix
(`pred_harness.EVALUABILITY`):

- per prediction (PRED-2026-001/002/003): `QUALIFIES` / `NO`;
- `caveat_c1_required` for `icit_full` (verdicts on it must
  carry the §4 C1 adjacency caveat verbatim — recorded now,
  used only by a future authorized evaluation);
- the PRED-2026-003 site input: distinct non-null `site`
  count and `multi_site` (≥ 2) per §6.1.5;
- a lineage consistency note if an "independent" class is
  declared while `upstream_lineage.is_derivation_input` is
  true — that combination must be re-adjudicated by a human
  before the dataset's lineage is treated as independent;
  derivation-adjacency is a lineage fact, not a label.

Assignment is descriptive. It authorizes nothing by itself.

## Stage 5 — Harness dry-run

Only for datasets whose every record declares
`parpola_1982` (already P-space) does intake pass records
through token-for-token to `pred_harness.dry_run`. Any other
declared sign list stops here with a recorded skip reason:
mapping it to P-space is a spec 018 §7 adapter's job (RMRL
Mahadevan, image-transcription Wells, future-concordance
P-direct), built under its own authorization when a real
source of that class is in hand.

The dry run emits exactly what spec 018 §8 permits:
ingestion and per-stage dedup counts, token/sign counts, and
sign-set coverage — under the label
**"HARNESS DRY RUN — NOT A PRED EVALUATION"**, which the
intake report carries verbatim. It computes no rate against
any threshold, no template-conformance fraction, and no
verdict (the intake pipeline asserts the label and the
absence of verdict keys; tests assert the intake module
binds no scoring name).

## After intake

The intake report (`run_intake` output) is the artifact:
validation verdict, license-gate outcome, dedup counts,
evaluability assignment, dry-run block, and the dataset
content hash. Anything beyond this — an adapter build, a
crosswalk (see `docs/INTAKE_CROSSWALK_REQUIREMENTS.md`), or
an evaluation — is a separate, separately-authorized step.

**Worked example:** `backend/scripts/phase130_intake_pack.py`
runs the synthetic fixture
(`backend/tests/fixtures/intake/synthetic_dataset.json` —
invented signs/sites) through every stage above and writes
`reports/phase130_intake_pack_results.json`. The
license-missing variant fixture is rejected at Stage 1.
