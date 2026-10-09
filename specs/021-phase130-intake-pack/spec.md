# Spec 021 — Phase-130: Independent-Data Intake Pack

**Status:** BUILT 2026-10-08 on `phase/130-intake-pack`
(from main `9f0ec4da`, after PR #92). Owner-ordered program
(Workstream 5 of 5, 2026-10-08): build the intake machinery
so that when a genuinely independent inscription dataset
lands, receiving it is a procedure, not a negotiation —
the intake-side companion to spec 018 (Phase-119), whose
harness waits downstream.

**This spec ingests NO real external data, contacts NO ONE,
and sends NOTHING.** Its only end-to-end exercise is on a
synthetic fixture dataset (invented signs P901–P905,
invented sites) authored for tests.

**AI disclosure:** this phase is executed by an AI agent
(Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.

## Epistemic boundaries (H13)

- **B1 — What "required" means.** Intake-schema REQUIRED
  fields are exactly the fields spec 018's machinery
  consumes: the §4 evaluability matrix and §6.1 gates
  (source class, provenance/license basis, site values,
  dataset identity), the §5 dedup protocol (inscription ID,
  token sequence), and the §7 adapter inputs (declared sign
  list, per-inscription provenance). Everything else in the
  schema is optional-but-declared.
- **B2 — Dedup naming.** The tasking memo's stage names
  (exact-ID → witness-identity → artifact-hash → lineage-key)
  do not match any protocol in the repo. The frozen protocol
  of record is spec 018 §5 — Stage A exact, Stage B
  sentinel-normalized exact, Stage C near-duplicate — as
  implemented in the Phase-119 harness, and §5 of this spec
  lifts THAT protocol unchanged. (Duplicate-ID detection is
  a validator duty here, §3, not a §5 stage.)
- **B3 — Intake dedup is a pre-check.** §5 operates on
  adapter-emitted P-space sequences. Intake runs the same
  module on declared-space token lists as a pre-adapter
  pre-check; the authoritative dedup is the one the harness
  applies post-adapter (the dry run re-applies it — same
  module, so the counts cannot diverge in algorithm).
- **B4 — No verdict exists in this phase.** Intake output
  reaches only the harness dry-run path (§5 below).
  PRED-2026-001–003 remain PENDING; this phase evaluates
  nothing and changes no register field.

## 1. Scope

In scope: the intake dataset schema (§2); the validator
with the license gate (§3); the shared dedup module (§4);
the structural dry-run-only rule (§5); crosswalk adapter
requirements (§6, requirements only — no crosswalk built);
the intake runbook (§7); a synthetic fixture exercising
every stage (§8).

Out of scope: acquiring or ingesting any real dataset;
building any new crosswalk; any adapter for a real source;
any evaluation (see §5); anchor changes of any kind.

## 2. Dataset schema (deliverable 1)

Canonical artifact: `data/intake/intake_dataset_schema_v1.json`
(JSON Schema draft 2020-12, versioned via `schema_version`
const `"1.0"`).

**Choice and justification.** JSON Schema is the published,
language-neutral contract a future dataset supplier can be
handed; the enforcing validator is stdlib-only Python
(`glossa_lab/intake.py`), because core `glossa_lab` modules
are stdlib-only by precedent (`pred_harness.py` imports no
third-party package), `jsonschema` is not a project
dependency, and pydantic in this repo is confined to the
API layer. Tests assert the two agree on required fields,
enums and version, so the document cannot drift silently
from the code.

Dataset level — REQUIRED: `schema_version`, `dataset_name`,
`source`, `source_class` (one of spec 018 §4's six classes),
`license_basis`, `upstream_lineage` (`derived_from`,
`is_derivation_input`), `inscriptions` (≥ 1).
Optional-but-declared: `compiler`, `acquisition_date`,
`text_rule`, `unit_rule`.

Per inscription — REQUIRED: `inscription_id` (source-assigned,
unique in the dataset), `site` (key required; null permitted
with a warning — §6.1.5 consumes site values for
PRED-2026-003), `tokens` (sign sequence as a token list, in
source transcription order, spec 018 A1), `sign_list`
(declared numbering/segmentation: `parpola_1982`,
`mahadevan_1977`, `wells`, `marshall`, `other`),
`provenance` (`source_reference` required inside).
Optional-but-declared: `object_type`, `context`, `period`,
`artifact_hash`, `sign_list_detail`.

## 3. Validator + license gate (deliverable 2)

`glossa_lab.intake.validate_dataset` returns a structured
verdict — `pass` / `pass-with-warnings` / `reject` — with
named reason codes on every finding (`LICENSE_BASIS_MISSING`,
`SIGN_LIST_UNDECLARED`, `DUPLICATE_INSCRIPTION_ID`,
`SOURCE_CLASS_INVALID`, `REQUIRED_FIELD_MISSING`,
`TYPE_ERROR`, `EMPTY_DATASET`,
`SCHEMA_VERSION_UNSUPPORTED`, `INVALID_DATE`, and warning
codes `RECOMMENDED_FIELD_MISSING`, `SITE_MISSING`,
`EMPTY_TOKEN_SEQUENCE`, `TOKEN_FORMAT_MISMATCH`,
`SIGN_LIST_DETAIL_MISSING`, `ARTIFACT_HASH_FORMAT`).

**License gate (hard).** A dataset with no declared lawful
basis (missing or empty `license_basis`) is a REJECT, not a
warning — mirroring spec 018 §6.1.2, which makes a complete
provenance log (license included) a precondition of any
evaluation. Duplicate source-assigned IDs and an undeclared
or unknown sign list are likewise rejects.

## 4. Dedup as a reusable module (deliverable 3)

The frozen §5 implementation is lifted verbatim from
`pred_harness.py` into `backend/glossa_lab/dedup.py`
(`dedup`, `levenshtein_le1`). `pred_harness` imports and
re-exports it, so every existing import keeps working and
the harness's behaviour cannot change: its existing tests
pass unmodified in outcome, and the Phase-119 measured
numbers (spec 018 Appendix A.6 on the ICIT converted layer:
input 4,531; stage removals 1,468 / 370 / 247; kept 2,446;
cumulative removal 46.02%) reproduce through the module on
the same fixture the harness tests use (and, where the
converted layer file is present, on the layer itself) —
asserted in `backend/tests/test_phase130_intake_pack.py`.

**Note on the measured figure:** the tasking memo cited
46.02% "cumulative removal on the ICIT layer"; that is the
P-space figure of spec 018 Appendix A.6 (the A.1 design-stage
M-space prototype measured 45.51%). The module reproduces
A.6, the spec-conformant number.

## 5. Structural rule — dry-run only

Intake output can only ever reach the harness's dry-run
path. `glossa_lab/intake.py` imports `dry_run` — and NOT
`evaluate` or any scoring function — from
`glossa_lab.pred_harness`; tests assert no scoring name is
bound in the intake module and that an intake report carries
the §8 label (`HARNESS DRY RUN — NOT A PRED EVALUATION`) and
no verdict/rate/conformance keys. Evaluation of any
prediction on any intake dataset requires its own future
spec and separate owner authorization. This mirrors spec
018 §8: the gate is in the code path, not in reviewer
vigilance.

## 6. Crosswalk adapter requirements (deliverable 4)

`docs/INTAKE_CROSSWALK_REQUIREMENTS.md`: what an incoming
dataset's sign list must supply for a Phase-122-style
crosswalk to be built from it — mapping evidence types,
confidence-rubric inputs (after the Phase-122 v1 rubric),
and conflict handling (never silently resolved; spec 018 §3
tie rules; honest unmapped). Requirements only; no new
crosswalk is built in this phase.

## 7. Intake runbook (deliverable 5)

`docs/INTAKE_RUNBOOK.md`: provenance capture → license gate
→ schema validation → dedup → evaluability-class assignment
(spec 018 §4) → harness dry-run, with the §5 structural rule
restated at the head of the pipeline.

## 8. Synthetic fixture

`backend/tests/fixtures/intake/synthetic_dataset.json`
(invented signs P901–P905, invented sites `site-alpha` /
`site-beta`, invented contexts) walks every runbook stage,
including a deliberate duplicate cluster the dedup must
catch (one Stage-A exact, one Stage-B sentinel-normalized,
one Stage-C near-duplicate record; 7 in → 4 kept) and, in
`synthetic_dataset_no_license.json`, a license-missing
variant the validator must reject at the license gate.
No real corpus data appears in any fixture.

## 9. Implementation (this phase)

Following the Phase-113–122 file pattern (H15/H23):

1. `backend/glossa_lab/dedup.py` — shared §5 module (§4).
2. `backend/glossa_lab/pred_harness.py` — import/re-export
   only; no behaviour change.
3. `backend/glossa_lab/intake.py` — validator (§3),
   evaluability assignment, intake pipeline, dry-run bridge.
4. `data/intake/intake_dataset_schema_v1.json` — schema (§2).
5. `backend/scripts/phase130_intake_pack.py` — runs the
   fixture end-to-end through the runbook; writes
   `reports/phase130_intake_pack_results.json` (incl.
   `gpu_device`, H20 pattern; no SA is run).
6. `backend/glossa_lab/experiment_graph_phase130_intake.py`
   — node `IndusPhase130IntakePack`, registered in
   `experiment_graph.py` by try/except import, asserted
   present in `ATOMIC_NODES` in tests.
   (Node name is Phase-130 in the ledger sequence of this
   program; it is distinct from the legacy Phase-130
   decode-blocker node `IndusDecodeBlockerAudit`.)
7. `backend/tests/test_phase130_intake_pack.py` — schema/
   validator, license gate, duplicate-ID, dedup module vs
   harness reproducibility (incl. Appendix A.6 numbers where
   the layer file exists), evaluability assignment,
   structural separation, full synthetic E2E, graph
   registration.
8. Docs: `docs/INTAKE_RUNBOOK.md`,
   `docs/INTAKE_CROSSWALK_REQUIREMENTS.md`.
9. Full backend suite + foundation check; ruff clean;
   ledger entries (append-only) in `LEDGER.md` and
   `glossa-indus/LEDGER.md`; one PR; merge only if all CI
   checks are green.

## 10. What this phase does not do

It evaluates no prediction, acquires no dataset, contacts
no one, builds no crosswalk, and touches no anchor, claim,
or language-model file (anchors asserted unchanged:
sha256 `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`).
