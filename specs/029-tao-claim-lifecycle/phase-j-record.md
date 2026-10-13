# Spec 029 Phase J — Record (D-D: foundation annotations)

Phase J executes tasks J1–J4 of `tasks.md` (Phase J —
Foundation annotations, plan §2.7), disposing adjudication
item D-D. The audit (§5-P8 defect 3) found the foundation
status endpoint returning `last_checked_at: null, verdict:
null, n_ok/n_fail/n_warn: 0` in a fresh backend process while
a current report file (40/0/8, "READY WITH CAVEATS") existed
on disk, and the report's own annotations (`solid_claims` /
`caveated_claims`) embedding Phase-48-era figures — "37 HIGH
+ 36 MEDIUM (Phase-48+51 validated)… 75 LOW… 1 UNCERTAIN
(M267)" — contradicting the current anchor table (287
anchors: 166 HIGH + 5 MEDIUM + 3 LOW + 113 CANDIDATE; M267
resolved and reclassified). This phase changes how the
report annotates and how the endpoint serves it. It does
not change what the foundation check checks: the check list,
its thresholds, and its result (40 passed / 0 failed /
8 warnings, with the passed/failed/warnings lists
byte-identical to the pre-phase report) are untouched.

## J1 — Interim as-of label (permanent provenance line)

Every annotation in the generated report now carries an
`as_of` stamp, and the report carries the same text as its
top-level `annotations_as_of` field:

> As of <generation date> — computed at report generation
> from the canonical anchors file
> `backend/reports/INDUS_FINAL_ANCHORS.json` (SHA-256
> <anchors-file hash>) and the extracted-claims store
> `glossa-indus/claims/extracted_claims/` (combined SHA-256
> <claims digest>). Figures describe that anchor table; if
> the anchors file changes, this label's hash no longer
> matches and the report is stale.

Per the phase brief, J2's structural fix landed in the same
phase, so the label stands as the report's permanent
provenance line rather than a temporary flag on stale prose:
the stale prose itself is gone (J2/J4), and the label now
names the exact canonical data state every computed figure
describes.

## J2 — Computed annotations + hash stamp

New module `backend/glossa_lab/foundation_annotations.py`
is the single source of the computation; the foundation
script (`backend/scripts/foundation_check.py`) builds its
computed annotations from it, and the status endpoint uses
its hash helper for the staleness comparison.

**Computed from the canonical anchors file at report
generation** (verified against the live file at this main
head): total anchors (287); tier split by `confidence`
(166 HIGH + 5 MEDIUM + 3 LOW + 113 CANDIDATE); H+M count
(171); strict-core size and composition (`strict_set`:
94 = 90 HIGH + 4 MEDIUM); pending count
(`validation_status=pending_non_sa_validation`: 44);
`validation_status` distribution (strict_sa_independent
94, premise_superseded 113, pending_non_sa_validation 44,
sa_in_provenance_chain 33, no_validation_record 3); H+M
token coverage as recorded in the anchors file (92.2%);
M267's current state (MEDIUM, strict_sa_independent,
strict). **Computed from the extracted-claims store:**
claim total (31) and file count (10), plus a combined
SHA-256 over the store's files (per-file name + hash,
sorted) that changes if any claims file changes.

Two annotation entries are built entirely from that
snapshot:

- solid — "Canonical anchor table (computed)": the full
  figure set above, in one annotation.
- caveated — "signs assigned": the audit's stale entry,
  rewritten computed (H+M with evidence, LOW/CANDIDATE
  standing, M267's current state). Its status text is
  unchanged in substance.

**Hash stamp.** The report is stamped with
`anchors_file_sha256` — the SHA-256 of the anchors file's
raw bytes, the same identity Phase H records for the file
(verified at this main head:
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`)
— plus `claims_store_sha256`, `anchors_file`,
`claims_store`, and `generated_at`.

**Regeneration test** (`test_spec029_phase_j.py`): an
unmutated scratch copy of the canonical inputs reproduces
the live computed annotations and hash stamp exactly; a
mutated scratch anchors file (one HIGH strict anchor
demoted to LOW/pending) changes the computed figures
(tier split, strict count, pending count) and the hash
stamp accordingly. An end-to-end test re-runs the script
itself and asserts the regenerated report's computed
annotations and stamp equal a fresh computation, at
40/0/8.

## J3 — Loud endpoint

`GET /api/v1/foundation/status`
(`backend/glossa_lab/api/foundation.py`):

- **Healthy report, no in-process run recorded:** the
  endpoint serves the on-disk report — verdict and counts
  from the report, `source: "on_disk_report"`,
  `last_checked_at` from the report's `generated_at`, and
  the full report under `report` (figures, as-of label,
  hash stamps). No nulls.
- **Missing or unreadable report, no recorded run:**
  HTTP 503 with an explicit detail naming the failure
  ("foundation report unavailable: … Run the foundation
  check to generate the report."). No null payload is
  ever served.
- **Stale hash:** a report whose stamped
  `anchors_file_sha256` differs from the current anchors
  file's hash is served with `report_stale: true`,
  `anchors_file_sha256_current`, and an explicit
  `staleness_warning` stating its figures do not describe
  the current anchor table. (Frozen J3 specifies the
  missing/unreadable behaviour; the stale case is served
  flagged rather than failed, because the report still
  truthfully describes its own stamped table under its
  as-of label — failing it would hide a healthy, honestly
  labelled report. Recorded here as this phase's reading.)
- A recorded in-process run keeps precedence for the
  headline fields (existing wiring unchanged); the disk
  report is attached alongside it, and if it cannot be
  read the failure is stated in `report_error` instead of
  being hidden.

Tests cover all three states plus the unreadable case.

## Stale figures purge (brief's J4; within tasks.md's J2/D-D)

(`tasks.md` Phase J numbers the phase gate as J4 and folds
the purge into J2's computed-annotations requirement; the
phase brief names the purge as its own J4. Both are done;
this section is the purge, the gate follows under its
tasks.md number.)

The audit's named Phase-48-era figures appear in no
annotation the report or endpoint can serve — grep-provable
over the regenerated report, the foundation script, the
annotations module, and the endpoint (the purge list itself
lives in the phase's test file, as a guard). Population
figures that are legitimately historical — a phase's own
result, recorded at its time — remain, each now carrying
an in-detail as-of label naming its phase: Phase-48
promotion coverage, Phase-56's then-total, Phase-69's
then-H/M population, Phase-71's crosswalk state, and the
Phase-51 crosswalk entry (whose "now mapped" wording is
also corrected to past tense). SA-era pinned counts
(Phases 52/57/61/73) already carry SUPERSEDED status text
and phase-named claims; they are historical results, not
anchor-table figures, and are unchanged.

## J4 — Phase gate (as A6)

- **Foundation check** (H21): 40 passed / 0 failed /
  8 warnings — identical to the pre-phase baseline; the
  passed/failed/warnings lists in the regenerated report
  are byte-identical to the pre-phase report's.
- **Full backend suite** (CI-identical invocation:
  `python -m pytest tests/ --tb=short -q
  --ignore=tests/test_pipelines_gpu.py
  --ignore=tests/test_install_gpu.py` in `backend/`,
  CI-parity venv, aee 1.4.0): **1368 passed, 6 skipped,
  0 failed** — the 1352 passed / 6 skipped merged
  baseline plus exactly this phase's 16 new tests.
- **Lint**: ruff clean on every authored/edited Python
  file.
- **Branding sweep** over authored and edited files:
  no other-company or other-program names.
- **PR / CI / merge**: PR_NUMBER (merge method; CI
  verified from the check runs' own conclusions; new
  main head verified via the GitHub API).

## Deviations and honest limitations

- **Worktree source.** The brief's `git clone --shared`
  from the Phase C worktree failed (a missing tree object
  in its alternates chain); the worktree was instead
  cloned `--shared` from the healthy Phase I worktree
  chain and fetched to the exact brief head
  `7f773d6b145fa77e13c87023935cc74b3749d16d` from GitHub.
  The resulting tree is identical; only the object source
  differs.
- **Stale-hash endpoint behaviour** is this phase's
  recorded reading (serve flagged), per J3's silence on
  that case — see J3 above.
- **The regenerated report is committed.** Running the
  foundation check rewrites `reports/
  foundation_check_report.json`; the copy in this PR is
  that regeneration (new annotations + stamps only; check
  lists identical). Its `generated_at` is the run's UTC
  stamp.
- **Frozen bytes**: nothing under
  `specs/029-tao-claim-lifecycle/` was edited except
  adding this record; `tasks.md`/`plan.md` untouched; no
  anchors-file content change (its hash is an input to
  stamp, verified unchanged); no PRED change; no aee pin
  change. Running the backend suite regenerates
  extraction timestamps in
  `glossa-indus/claims/extracted_claims/*.json` as a
  pre-existing side effect; those files were restored
  byte-identical before commit.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
