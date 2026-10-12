# Spec 029 — Phase H Record: Anchor Annotation and Schema (D-A)

> Phase H of `tasks.md` (D-A; plan §2.5; after A6 + D6 —
> same file, one writer at a time). Base: main `712f3b99`
> (Phase D merged as PR #171). Branch:
> `impl/029-phase-h-da`. Date: 2026-10-12.
>
> D-A (ratified 2026-10-12, `adjudication.md` addendum):
> annotate in place, additively; pin the schema. **No
> demotion of the display tier, no alteration of any
> existing field.** The annotation's only inputs are the
> Phase-D-stamped anchors file, the Phase-108 provenance
> register, and the Phase-109 strict rule — the same join
> the audit used. It exercises judgment nowhere else:
> where `tasks.md` Phase H and the phase instructions
> differed in summarisation, `tasks.md` governed (see
> Deviations).

## Consumer inventory (recorded before any run)

The store is the one Phase D inventoried:
`backend/reports/INDUS_FINAL_ANCHORS.json` — 287 anchor
records under `anchors{}`, Phase-D-stamped SHA-256
`18e6f4b2caa7bc9ae1f5cc92dd96f95ce191a77c56144b95820a368d75a316d6`
at this phase's start (verified). Phase D's D1
inventory of live readers stands unchanged. The
consumers this phase had to repair are the ones Phase D
canonicalized: the seven `_canonical_anchors_sha256`
helpers (phase runners 125/126/128, scripts
137/139/140/141 — 127 and 131 import theirs), the eight
backend test files asserting the live file's canonical
digest against the pinned pre-migration hash, and Phase
D's own strip test. Each asserted "pre-existing anchor
content unchanged" by removing exactly the Phase D
additive keys; Phase H's annotation is additive in the
same sense, so each now also removes exactly the Phase
H annotation (see H3/H4 dispositions). The pinned
constants and every recorded hash value are
byte-identical to before.

## H1 — `validation_status` made total

Every anchor now carries an explicit
`validation_status`. Values already present were
preserved verbatim (157 records); the 130 records that
carried none gained the value their own provenance
establishes, derived by
`annotate_phase_h_anchors.derive_validation_status` in
this order: an existing value stands; else the computed
strict set; else the Phase-108 register's
`sa_in_chain` fact; else the absence of any validation
record. The declared vocabulary (in
`anchors-schema.json`, with a definition per value):

| Value | Count | Provenance |
|---|---|---|
| `strict_sa_independent` | 94 | NEW — passed the Phase-108/109 strict SA-independence rule (H+M, register category not SA-lineage, no SA in chain) |
| `sa_in_provenance_chain` | 33 | NEW — HIGH; register `sa_in_chain` true, category DEDR 15 / LITERATURE 9 / MIXED 9; not flagged pending by Phase-109 Step 2, fails the strict rule, no SA-free validation outcome (the audit's 33 chained HIGH, §4 item 2) |
| `no_validation_record` | 3 | NEW — LOW (H003, M231, M252); the audit ledger's own flag for these records: no validation outcome recorded under any live method |
| `pending_non_sa_validation` | 44 | pre-existing (Phase-109 Step 2) — 43 HIGH + 1 MEDIUM, exactly the register's SA-lineage set (SA_DERIVED 24 + SA_CONFIRMED_ONLY 20) |
| `premise_superseded` | 113 | pre-existing (Phase-110/111) — the CANDIDATE 'kur' cohort |
| **Total** | **287** | |

The 33 carry a value distinct from
`pending_non_sa_validation` deliberately: the pending
value names the Phase-109 Step 2 flag, and live code
and tests across the program (Phase-120/123/126/128
consumers, the battery suites) take it to denote
exactly the 44-set SA-lineage population. Assigning it
to the 33 would have falsified those records' meaning;
the chained value names the register fact that
distinguishes them. The 94's value names the rule they
passed, not the Phase-113/115 battery outcome
(`validated_non_sa`): those batteries applied their
outcomes only to the pending set and used the 94 as
their calibration core, so the battery's term would
misstate what checked these records — the audit's
staging rule for anchors is passage of the
Phase-108/109 SA-free provenance rule.

By this field alone, strict records
(`strict_sa_independent`), the 44 pending, and the 33
chained are mutually distinguishable in the file
itself — the audit §5-P8 defect 1 closed for the
validation axis. No tier, reading, basis, or existing
value changed (canonical comparisons under H3).

## H2 — Computed `strict_set` flag

Every anchor carries a boolean `strict_set`, computed
by the program's own rule —
`backend/glossa_lab/pipelines/phase109_followthrough.py:
strict_sa_independent_hm` over
`reports/phase108_provenance_register.json` — imported
by the annotation script, never re-implemented. The
rule's identifier and version are recorded in the file
metadata (`metadata.spec029_phase_h_annotation`:
`rule_id` `strict_sa_independent_hm`, `rule_source`,
`rule_version` "Phase-109 follow-through (spec 007,
2026-10-06) applying the Phase-108 strict definition",
`register`, `strict_count` 94 — the rule's own
identification read from its source, per plan §5
§VIII; no version string was invented).

**Reconciliation: exact.** The computed set is 94
records (90 HIGH + 4 MEDIUM), and its membership is
the canonical strict core, verified four ways in this
phase: (1) the imported Phase-109 rule; (2) an
independent inline recomputation from the register's
`category` / `sa_in_chain` fields and each record's
confidence; (3) the battery suites' register-driven
computation (Phase-113 `compute_sets` shape); (4) the
frozen reclassification ledger's `checked` anchor set
(the Phase D staging population). All four sets are
identical. The stored flags equal the recomputation
for every record, and `strict_set` true holds exactly
for the `strict_sa_independent` records. Had the rule
not reproduced 94 with this membership, the annotation
script's plan step stops the run (it asserts the count
before any write); it did reproduce it, so no
discrepancy report replaces this phase.

## H3 — Declared schema

`specs/029-tao-claim-lifecycle/anchors-schema.json`
declares the anchors file's shape: required core
fields (`reading`, `confidence`, `basis`), the Phase
D additive fields, this phase's additive fields
(`validation_status` with its controlled vocabulary,
`strict_set`), and the 30 optional fields — together
exactly the field union the 287 records carry, so the
56 accreted shapes are precisely the declared
combinations. It also declares the vocabulary's
per-value definitions and expected counts, the strict
rule's identity and expected reconciliation, the
derivation rule for assigned values, the canonical
serialization, and the metadata annotation block.

The annotation pass normalised the shapes additively
in the only sense D-A permits: every record gained the
total Phase H fields; no record gained or lost any
other field (proven by the canonical comparisons).

**Canonical comparisons (additive-only proof).**
Stripping exactly the Phase H annotation from the
annotated file — `strict_set` everywhere, the
`validation_status` values this pass assigned (the
three new values; pre-existing values stand), and the
metadata block — reproduces the Phase-D-stamped bytes
exactly: SHA-256
`18e6f4b2caa7bc9ae1f5cc92dd96f95ce191a77c56144b95820a368d75a316d6`.
Stripping Phase D + Phase H reproduces the
pre-migration bytes (`eccea6d5…`, Phase D's pinned
hash). Both comparisons are pinned in
`backend/tests/test_spec029_phase_h.py`.

**Dispositions (consumers repaired, no stored value
changed anywhere):** the seven canonical-hash helpers
and the eight hash-asserting test files now also
remove exactly the Phase H annotation before digesting
(the same disposition Phase D applied to them; each
site carries the Phase H comment, and the helpers'
docstrings record it). All seven helpers were executed
against the annotated file and reproduce the pinned
pre-migration hash. `backend/tests/
test_spec029_phase_d.py`'s additive-only comparison
strips Phase H as well as Phase D, its assertion
(pinned pre-migration hash) unchanged.

## H4 — CI validator

`annotate_phase_h_anchors.validate_anchors_doc` is the
validator core; `backend/tests/
test_spec029_phase_h.py` runs it in the backend suite
(CI) against the live file and fails on: any record
whose shape is undeclared under H3's schema (missing
governed field, undeclared field, wrong declared
type/enum); any `validation_status` missing or outside
the declared vocabulary; any assigned value that
disagrees with its provenance derivation, any pending
value whose register category is not SA-lineage, any
`premise_superseded` outside the CANDIDATE 'kur'
cohort; any `strict_set` that disagrees with its
recomputation; any strict count ≠ 94 or composition
≠ 90 HIGH + 4 MEDIUM; vocabulary counts off the
declared expectations; a missing or altered metadata
rule block. The suite pairs each check with a
must-fail control on a mutated copy of the live
document (missing field / out-of-vocabulary value /
flipped flag / undeclared field / wrong provenance
value / missing metadata block) — every control fails
the validator, so the gate is differential, per the
program's Spec 026 discipline. `--verify` mode runs
the same validation standalone.

## The annotation run (2026-10-12)

Executed once: `annotate_phase_h_anchors.py --live
--snapshot-dir ~/workspace/glossa-wt-029H-snapshots/
phase-h-pre-run-2026-10-12/` (snapshot of the anchors
file taken before the write, named here; outside the
repo, not committed — the identical pre-run bytes are
also main `712f3b99`'s state of the file). Dry run
first: population 287 unannotated / 0 annotated /
0 conflicts, would-be reconciliation exact (table
under H1; strict 94 = 90 HIGH + 4 MEDIUM). Live run:
additive-only assertion passed before writing; the
annotated document validated clean before writing;
post-write `--verify` valid. Anchors file SHA-256
`18e6f4b2…` → `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`.
A second `--live` run is a no-op and says so ("every
record already carries this annotation; nothing
written") — verified, file hash unchanged.

## H5 — Phase gate

- **Foundation check** (H21): 40 passed / 0 failed /
  8 warnings — identical to the pre-Phase-A baseline;
  no new warnings.
- **Full backend suite** (CI-identical invocation:
  `python -m pytest tests/ --tb=short -q
  --ignore=tests/test_pipelines_gpu.py
  --ignore=tests/test_install_gpu.py` in `backend/`,
  per `.github/workflows/ci.yml`): **1227 passed,
  6 skipped, 0 failed** in 16m33s (Phase D's gate run:
  1207 passed / 6 skipped; the +20 are this phase's new
  tests). Collection under the CI command is now 1233.
  Targeted runs before it: Phase H + Phase D + Phase A
  suites 65 passed; the 20 hash-sensitive and battery
  files (Phase 109–141 anchors consumers, sign images,
  staging promotion, release gate) 281 passed /
  1 skipped.
- **Lint**: ruff clean on every authored/edited
  Python file.
- **Branding sweep** over authored and edited files:
  no other-company or other-program names.
- **PR / CI / merge**: PR: BitConcepts/glossa-lab
  **#175** (`impl/029-phase-h-da` → `main`). CI on head
  `adfdbbd1` (workflow run 38286751077): **all 7 checks
  success, read from the check runs' own conclusions**
  — Backend tests (pytest) pass; Frontend tests
  (Playwright) pass; Evidence Graph script smoke tests
  pass; Indus public validation checks pass; Shell
  wrappers (ubuntu-latest, macos-latest, windows-latest)
  pass. This record's H5 completion commit re-verified
  green on the final head before merging (same
  workflow, all 7 checks success on the final head —
  conclusions read again after that run). Merge:
  method `merge`; the merge commit SHA and the new
  main head were verified via the GitHub API
  immediately after merging (a merge commit cannot
  name itself in the content it merges; the SHAs are
  stated in the PR timeline and in this phase's
  delivery report).

## Deviations and honest limitations

- **`tasks.md` governs over the phase summary.** The
  phase instructions summarised H3/H4 as one item and
  raised display/API surfacing as a conditional H4;
  `tasks.md` Phase H has H1–H5 with H3 = declared
  schema, H4 = CI validator, and **no surfacing task**.
  No display or API change was made in this phase:
  surfacing `validation_status` / `strict_set` belongs
  to the display phases (E2's anchor surfaces), and the
  fields are inspectable from the canonical file alone,
  which is what D-A required.
- **The chained-33 value is a derivation, recorded as
  such.** `sa_in_provenance_chain` is not a value any
  earlier phase wrote; it is the Phase-108 register's
  `sa_in_chain` fact made explicit, per H1's "the value
  the record's own provenance establishes". Its
  definition, and the reasons the 33 do not carry the
  pending value, are recorded under H1 and in the
  schema.
- **Writers are not yet schema-gated at write time.**
  The CI validator fails the suite on an undeclared
  shape in the committed file (H4 as specified); the
  research-loop promotion writer, which appends new
  anchors, does not yet stamp the Phase H fields at
  write time — the schema is the contract it must be
  brought under, and a promotion landing without the
  fields now fails CI rather than drifting silently.
- **Frozen bytes**: nothing digest-covered under
  `specs/029-tao-claim-lifecycle/` was edited; the
  schema, the annotation script, and this record are
  new files in that directory. (Running the backend
  suite regenerates extraction timestamps in
  `glossa-indus/claims/extracted_claims/*.json` as a
  pre-existing side effect; those files were restored
  byte-identical before commit and are not part of
  this phase's diff.)

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
