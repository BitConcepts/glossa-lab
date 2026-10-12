# Spec 029 — Phase D Record: OD-1 Re-staging Migration

> Phase D of `tasks.md` (OD-1; plan §0, §2.2; D-E: the
> migration runs early, immediately after Phase A). Base:
> main `028d416c` (Phase A merged as PR #169). Branch:
> `impl/029-phase-d-restaging`. Date: 2026-10-12.
>
> The migration is mechanical: it exercises judgment
> nowhere, because the frozen `reclassification-ledger.json`
> (345 entries, SHA-256
> `e53a037e71439401f4114100b32495ff98adb58f8529fe83dfedde3b94d22b90`,
> matching `freeze.json`) is its single source of truth.
> It is **additive only**: it adds `stage`, `stage_source`,
> `stage_as_of`, `stage_history`, and the ledger-stamped
> `verified_unexplained` flag state to records; it never
> alters a pre-existing field. The D1 inventory below was
> completed and recorded **before any run** (dry or live).

## D1 — Consumer inventory (recorded before any run)

### The anchors file and its hash

Store: `backend/reports/INDUS_FINAL_ANCHORS.json` —
287 anchor records under `anchors{}`, keyed by sign id;
ledger items `ANCHOR-<sign-id>` map to those keys verbatim
(all 287 verified present). Pre-migration SHA-256:
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`.
The file serializes canonically as
`json.dumps(..., indent=2, ensure_ascii=False)` with no
trailing newline (round-trip byte-identical pre-migration),
which is the serialization the migration preserves.

Live consumers of the file (read the records):

- `backend/glossa_lab/api/signs.py` — `_load_final_anchors`
  builds the signs index behind `GET /signs` (Phase A
  serializes each anchor's stage object from its record).
- `backend/glossa_lab/api/dashboard.py` —
  `dashboard_decipherment` summary (confidence counts and
  the Phase A lane-2 `by_stage` / `n_unstamped_stage`).
- `backend/glossa_lab/api/foundation_check.py` and
  `backend/scripts/foundation_check.py` — the H21
  foundation gate: counts by confidence and named-anchor
  assertions over pre-existing fields only.
- `backend/glossa_lab/api/research_loop.py` — reads the
  file, and is its promotion **writer** path (promotion
  appends anchors; it does not read stage fields).
- `backend/glossa_lab/config.py` — `anchors_json` default
  path configuration.
- `backend/glossa_lab/pipelines/` — `research_loop.py`,
  `study_loop.py`, `phase_advancer.py`,
  `provenance_audit.py`, `sa_validation.py`,
  `phase109_followthrough.py`; the `phase*_run.py`
  experiment modules and `experiment_graph_*` node
  modules (Kalyanaraman cross-validation, Phases 30,
  48–55 and successors); `backend/glossa_lab/tools/
  sign_image_processor.py`; `backend/glossa_mcp/server.py`
  (foundation / report tools). All read pre-existing
  fields (reading, confidence, basis); none reads a stage
  field except the Phase A surfaces above.

Consumers of the file's **hash** (the plan §4 risk:
byte-identity checks downstream of OD-1's authorised
additive change):

- Historical phase runners pin the pre-migration hash as
  the record of their run-time input and assert it when
  **re-run**: `backend/glossa_lab/phase125_run.py`,
  `phase126_run.py`, `phase127_run.py` (imports the
  constant), `phase128_dossiers.py`
  (`EXPECTED_ANCHORS_SHA256`), `phase131_run.py`
  (imports), and `backend/scripts/
  phase137_site_repertoire.py`, `phase139_covariate_
  audit.py`, `phase140_g1_controlled.py`,
  `phase141_loso.py`. **Disposition (amended during
  execution, recorded in D5): canonicalized, constants
  untouched.** The inventory initially left these
  modules untouched as historical records; execution
  showed the backend suite itself exercises several of
  them against the live file (Phase-128 dossiers build
  unconditionally in its tests; the Phase-137/139/140/
  141 recomputation tests run their scripts whenever
  the local store exists), so their raw-byte assertions
  failed on the OD-1 file although no pre-existing
  content changed. Each now computes the anchors hash
  canonically — the Phase D additive keys removed, the
  result re-serialized and hashed — via a local
  `_canonical_anchors_sha256` helper with the change
  cited in its docstring. The pinned constants and
  every recorded hash value are byte-identical to
  before (the canonical hash of the migrated file *is*
  the pinned hash); only the digest's definition gained
  the OD-1 canonicalization, which restores each
  assertion's original meaning ("pre-existing anchor
  content unchanged").
- Eight backend test files assert the **live** file's
  SHA-256 equals that pinned hash:
  `test_phase126_wells_split_candidates.py`,
  `test_phase132_pilot_report.py`,
  `test_phase133_stage0_inventory.py`,
  `test_phase136_terminal_type.py`,
  `test_phase137_site_repertoire.py`,
  `test_phase138_graffiti_descriptive.py`,
  `test_phase140_g1_controlled.py`,
  `test_phase141_loso.py` (each a
  `test_anchors_sha256_unchanged` / equivalent live-digest
  assertion). **Disposition: updated in this phase** —
  the assertion now canonicalizes the live file by
  removing exactly the Phase D additive keys from each
  anchor record and asserts the stripped serialization
  hashes to the same pinned pre-migration hash. The
  intent of those tests (no pre-existing anchor content
  changed) is preserved and is exactly the migration's
  additive-only assertion; the stored phase-result
  records and the pinned constant itself are unchanged.
- Tests that compare a **stored** phase record's
  `anchors_sha256` field against the pinned constant
  (e.g. `test_phase128_evidence_dossiers.py`,
  `test_phase139_covariate_audit.py`) do not read the
  live file's hash and are unaffected.

Not consumers of this file: the frontend (API only; no
file, no hash), the Indus public validation suite under
`research/indus/` (its own public data copy), and the
anchor-sets DB store below.

### Extracted claims — live store

Store: `glossa-indus/claims/extracted_claims/*.json` —
10 per-document files, 31 claim records in their
`claims[]` lists, keyed by `claim_id` (ledger
`extracted_claim` item ids are the claim ids verbatim;
all 31 verified present). Each file serializes
canonically as above (round-trip byte-identical
pre-migration). Consumers:

- `backend/glossa_lab/api/indus_evidence.py` —
  `GET /claims` and `GET /claims/aee-scores`.
- `backend/glossa_lab/aee_core.py` —
  `assessment_summary` / `claim_from_glossa` (the AEE
  adapter; Phase A pinned its score propagation
  byte-identical over this set, and the migration adds
  no field the adapter reads as a score input).
- `backend/glossa_lab/experiment_graph_indus_evidence.py`
  and `backend/glossa_lab/pipelines/provenance_audit.py`.
- `glossa-indus/scripts/indus_claims.py` and the intake /
  extraction pipeline — the store's **writer**: test runs
  regenerate `extracted_at` timestamps in these files as
  a pre-existing side effect (Phase A record). Byte
  discipline for this phase: after any test run, the
  stamped files are restored to exactly the bytes the
  migration wrote (see D5).
- Tests reading the real directory as a fixture:
  `backend/tests/test_aee_core.py`,
  `backend/tests/test_spec029_phase_a.py`.

### Anchor sets

Anchor sets live in the backend runtime DB
(`backend/glossa_lab/api/anchor_sets.py`,
`database.py:list_anchor_sets`, under `GLOSSA_DATA_DIR`);
`signs.py` merges their pairs into the signs index.
**The ledger covers no anchor-set record**: its 287
anchors are the final-anchors file's records. Decision:
anchor sets are not stamped; their index entries keep
serializing as unstamped (Phase A behaviour), which is
the honest state for records no ledger entry stages.
The staging files in `backend/outputs/` are likewise
not ledger stores and are untouched.

### Hypothesis library

Store: `glossa-indus/hypotheses/models/*.yaml` — three
model files (`hunt_civic_ritual.yaml`,
`parpola_proto_dravidian.yaml`, `roif_guild_ledger.yaml`);
ledger items are `HYP-<model_id>`, mapping to the file
whose top-level `model_id` is the suffix (all 3 verified).
Pre-migration SHA-256: hunt
`8d296dd46b0a8c8052ab9edb7486acbf5b51da5f6c6f46ebc5386dfc93c8c93a`,
parpola
`5cb6c2cb7de45328a57549fb94a0b54091135b1ca0b19ef522acc99a9e305137`,
roif
`42b4d87917893dc450752009252191b2afb51ca38a37350f73848f7498730f20`.
Consumers: `backend/glossa_lab/api/indus_evidence.py`
`GET /hypotheses` (`_load_yaml` over the models dir) and
`backend/glossa_lab/experiment_graph_indus_evidence.py`.
Pre-existing defect noted, not repaired here:
`roif_guild_ledger.yaml` does not parse under PyYAML
(line 24), so the API already falls back to an empty
record for it; the other two parse.

### PRED register (document class)

Ledger class `registered_prediction`: 5 live items
(PRED-2026-001/002/003 created; 006/007 checked) whose
live record is a section of the document
`docs/PREDICTION_REGISTER.md` (pre-migration SHA-256
`3fb5eff1df6c4b8844bbcb8c769a8739b296c962a825557b3b1a6fe0fce75dc1`).
Consumers of the register: `backend/glossa_lab/
pred_harness.py` and `experiment_graph_phase119.py`
(the Spec 018 readiness harness for PRED-2026-001..003)
and the Spec 018/020 adjudication records.
**Representation decision (before any run):** the
register document is **not edited** — it is an
append-only human register whose entries are prose, and
the Spec 029 closeout verifies it untouched. Its items
are document-class items with no per-record store, so
their stamping takes the dated machine-readable form
below (the sidecar), with each record naming the
register as its `live_source`.

### Study-headline records (document class)

Ledger class `study_headline_claim`: 10 items, all
`checked`, whose live records are the per-spec outcome
records under `specs/` (Spec 019 / Phase-125; Spec 023;
Spec 024 F1, F2-HOLDAT, F3-ICIT; Spec 025 G1; Spec 027
Stage-1 / Phase-392; Spec 028 Arms A and B; and the
grouped Specs 001–023 + phases-to-141 headline), plus
the Spec 026 impact register named in their ledger
evidence. There is no claim store, API, or DB holding
these as records. **Representation decision (before any
run):** same dated machine-readable form as the PRED
items — the sidecar — with each record naming its spec
outcome record as `live_source`. The spec outcome
records themselves are frozen history and are not
edited.

### The sidecar (dated machine-readable form)

`specs/029-tao-claim-lifecycle/phase-d-stamped-records.json`
— created by the live run (it does not exist
pre-migration), holding one stamped record per
`registered_prediction` and `study_headline_claim`
ledger entry (15 records), each carrying `item_id`,
`class`, `live_source`, `stage`, `stage_source`,
`stage_as_of`, `stage_history`, and
`verified_unexplained`, in the same shape the file
stores carry. It is the live store the post-run
reconciliation reads for those two classes.

### Grouped / surface ledger records (9, no stage)

The ledger's remaining 9 entries
(`presentation_surface` ×6, `integrity_check_suite`,
`intake_records`, `experiment_definitions`) carry
`honest_stage: null` by design — dispositions, not
record writes (plan §2.2: consumed by Workstream 3 /
later phases). The migration stamps none of them and
its reconciliation accounts for them as non-record
entries; the staged population is 336.

## Representation decisions (summary, before any run)

- Anchors, extracted claims: stamped **in place** in
  their JSON stores, preserving the canonical
  serialization byte-for-byte outside the additive keys.
- Hypothesis models: stamped **in place** in their YAML
  files by appending one top-level block; pre-existing
  bytes are a strict prefix of the stamped bytes, and
  for the two parseable files the parsed pre-existing
  keys are unchanged. No YAML re-serialization (which
  would reformat the whole file and, for the roif file,
  could not round-trip at all).
- PRED live items, study headlines: stamped in the
  sidecar (above); their documents are untouched.
- Every stamped record also carries
  `verified_unexplained` (boolean): `true` exactly when
  the ledger entry's flags include
  `verified_unexplained` (94 anchors + 8 extracted
  claims + 3 study headlines = 105). This is the
  ledger-stamped flag state Phase A's record assigns to
  this phase; the Phase A computed flag is unchanged
  for lane-1 inputs a record itself carries, and
  `claim_stage.compute_verified_unexplained` now also
  honours a stamped `true` on the record (below
  `explained`), so the stamped anchors surface their
  flags instead of serializing a computed `false`.
- `stage_source` is
  `specs/029-tao-claim-lifecycle/reclassification-ledger.json:<item_id>`;
  `stage_as_of` is `2026-10-12`; the initial
  `stage_history` entry has `from_stage: null`,
  `to_stage` = the ledger stage, actor
  `spec029-phase-d-restaging-migration`, timestamp
  `2026-10-12`, the ledger entry as its sole evidence
  ref, and a reason citing OD-1 and the ledger entry.
  The migration writes this initial entry directly
  (it is a reclassification event, plan §2.2), not via
  `transition_stage`: a first stamp to `checked` is not
  a one-step transition of a live record, and the
  plan prescribes exactly one initial history entry.
  Stage values are validated with Phase A's
  `claim_stage.validate_stage_value`.

## D2 — Migration script

`specs/029-tao-claim-lifecycle/migrate_phase_d_restaging.py`
(house style: module docstring with run instructions,
repo root derived from the file's location, the Glossa
venv as runner). Properties, by construction:

- **Single input:** the frozen
  `reclassification-ledger.json` only; its SHA-256 is
  asserted against `freeze.json` before anything else.
  Stage values are validated with Phase A's
  `claim_stage.validate_stage_value`.
- **Modes:** `--dry-run` (writes nothing, emits the
  reconciliation report), `--live --snapshot-dir <dir>`
  (snapshots first, stamps, re-reads and reconciles),
  `--verify` (read-only reconciliation from the live
  stores), `--report <path>` (also save the JSON report).
- **Idempotent:** a record whose stage fields differ in
  any way from the ledger stamp is a *conflict* and
  stops the run; a population already fully stamped is
  reported as a no-op and nothing is written; a
  partially stamped population stops the run.
- **Additive-only, asserted before writing:** for each
  JSON store, removing exactly the five additive keys
  from the post-stamp data must reproduce the pre-run
  canonical bytes; for each YAML store, the stamped
  bytes must have the pre-run bytes as a strict prefix.
  Before/after SHA-256 per store is recorded in the run
  record.
- **Snapshots:** the live run copies every touched
  store to the snapshot directory (named in the run
  record) before writing; the sidecar's pre-run state
  (absent) is recorded there too.

Companion code change (the stamped-flag surfacing
decided in D1): `backend/glossa_lab/claim_stage.py` —
`compute_verified_unexplained` now also honours a
ledger-stamped `verified_unexplained: true` on the
record (OR-ed with the FR-029-03 computed rule, below
`explained` only). Without it, the 94 stamped anchor
flags would serialize as a computed `false` on the
signs surface, because no field an anchor record
carries can recompute the strict-set derivation.

## D3 — Dry run

Executed before the live run; **reconciliation matched
the ledger exactly** (no mismatch; the phase was not
stopped):

| Class | Dry-run reconciliation | Ledger §3 |
|---|---|---|
| anchors | 193 created / 94 checked | 193 / 94 |
| extracted claims | 21 created / 10 checked | 21 / 10 |
| PRED-2026 live | 3 created / 2 checked | 3 / 2 |
| hypothesis models | 3 created | 3 |
| study headlines | 10 checked | 10 |
| **Totals** | **220 created / 116 checked / 0 explained / 0 accepted / 0 digested** | **220 / 116 / 0 / 0 / 0** |
| `verified_unexplained` flags | **105** | **105** |

Population state at dry run: 336 unstamped, 0 stamped,
0 conflicts; grouped/non-record entries accounted: 9.
Dry run wrote nothing (`git status` after it showed
only this phase's authored files).

## D4 — Live run (2026-10-12)

Executed once: `migrate_phase_d_restaging.py --live
--snapshot-dir <pre-run snapshots>`, snapshots taken
before any write (named in the run record). Full inputs,
snapshots, before/after SHA-256 per store, the additive
assertion output, and the reconciliation are in
`phase-d-run-record.md`. Headline: 336 records stamped
(287 anchors in place; 31 extracted claims in place; 3
hypothesis models in place by appended block; 15
document-class records in the sidecar
`phase-d-stamped-records.json`); anchors file SHA-256
`eccea6d5…` → `18e6f4b2…`; post-run `--verify` and a
second `--live` run: reconciliation exact, second run a
no-op ("every record already carries this migration's
stamp; nothing written"). The anchors file's additive
change and the stamped extracted-claims files land in
this phase's PR; hypothesis model files land stamped;
the runtime-DB anchor sets are not ledger records and
were not stamped (D1).

## D5 — Post-run verification

- **Ledger-vs-live reconciliation from the live
  stores**: `--verify` recomputes from the mutated
  stores and matches exactly (220 created / 116
  checked / 0 / 0 / 0; 105 flags; per-class table as
  D3). Pinned in CI by
  `backend/tests/test_spec029_phase_d.py`, which also
  asserts every stamped record's `stage_source`
  (ledger name + its entry id) and `stage_as_of`
  (2026-10-12), the initial history entry's shape, and
  the additive-only canonical comparison for the
  anchors file against the pinned pre-migration hash.
- **Foundation check** (H21 anchor-data gate):
  40 passed / 0 failed / 8 warnings — identical to the
  pre-Phase-A baseline.
- **Full backend suite** (CI-identical invocation:
  `pytest tests/` in `backend/`, GPU-only files
  ignored as in CI): **1207 passed, 6 skipped,
  0 failed** in 15m33s on the final branch state.
  (Phase A's record quotes 2112 passed for its local
  run; that run used a broader invocation — the
  backend/tests collection under the CI command is
  1212 tests. The CI-identical command is the gate
  used here.)
- **Repairs the migration required in consumers**
  (each documented at its site; no stored value
  changed anywhere): (a) the eight phase tests that
  asserted the anchors file's *live raw digest* now
  assert its canonical digest (additive keys removed)
  against the same pinned constant; (b) the
  hash-pinned phase runners/scripts (125–128, 131,
  137, 139–141) compute the anchors hash canonically
  via `_canonical_anchors_sha256` — their assertions
  failed on the raw bytes even though no pre-existing
  content changed, and the suite itself exercises
  several of them against the live file; (c)
  `glossa-lab`'s `compute_verified_unexplained` honours
  a ledger-stamped flag (Phase A design note); (d) the
  claim-extraction script `glossa-indus/scripts/
  indus_claims.py` now preserves stage fields by claim
  identity across its wholesale regenerations (plan §4
  risk control) — before this fix, a regeneration
  (e.g. triggered by the evidence API's intake test)
  silently dropped every stamp; verified by direct
  re-run: `--verify` still matches after regeneration.
- **Byte discipline**: backend test runs regenerate
  extraction timestamps in the extracted-claims files;
  after every local test run the stamped files were
  restored to the exact bytes the migration wrote
  (post-restore hashes re-verified against the run
  record). The committed state is the migration's
  state; in CI, any in-suite regeneration now
  preserves the stamps per (d), changing only the
  pre-existing volatile timestamps.

## D6 — Phase gate

<!-- Filled after the PR/CI/merge sequence completes:
     suite totals, PR number, the seven check-run
     conclusions, merge commit, new main head. -->

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
