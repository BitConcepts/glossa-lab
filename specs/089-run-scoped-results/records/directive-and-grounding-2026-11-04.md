# Directive and grounding record — Spec 089 (2026-11-04)

## The owner's directive (verbatim, Glossa-Lab chat, 2026-11-04)

> prevent previous runs from impacting new runs when it comes to results.
> we must lump results by the run and not allow contamination. if two
> similar runs produce different results or one produces results and one
> doesn't, we need extra scrutiny, perhaps an automatic red team analysis
> of the junction

The main chat routed the directive fleet-wide the same day (gatekeeper
runs; every program's experiment, benchmark, and evaluation runs).
Glossa-Lab takes it as this spec, over the run-bearing surfaces
inventoried below. The directive grows out of the fabricated-delivery
investigation closed the same morning
(`~/workspace/fabricated-delivery-redteam-2026-11-04/REPORT.md` and its
leakage-check addendum): that investigation established that *presented*
results can diverge from *recorded* results. This spec is about the
recorded side: when two recorded executions of comparable work diverge,
today nothing in the program's machinery forces the divergence to be
analyzed before either result is used.

## Grounding census (counted/read first-hand, 2026-11-04, clone on main at the Spec 088 S5 merge)

### Settling runs (`glossa-indus/ledger/runs/`, `backend/glossa_lab/settling.py`, `tools/ledger/run_settling.py`)

- The store holds exactly **2 records** today (the T405 pair:
  `t405-full-register-over-full-frame--070f8f0f476f.json`,
  `t405-incumbent-over-full-frame--5b1d1c866b0e.json`).
- A run record carries: artifact, label, semantics (`glossa-settle-1`),
  scenario, candidate, candidate_provenance, **pins** (ledger SHA-256 +
  lines; anchors-register raw SHA-256 + record/strict counts;
  phase108-register SHA-256; corpus-snapshot SHA-256), scope,
  out-of-scope assignments, and the result block. The pins are a
  proto-comparability-key over inputs.
- A run record carries **no run id, no execution timestamp, and no code
  version**. (The only date inside is `candidate_provenance.date` — the
  candidate's provenance date, not the run's.)
- The store filename is **content-addressed**:
  `run_record_filename` hashes {candidate, scope, pins, scenario} to 12
  hex chars; the docstring states the intent: "a rerun of one scenario
  overwrites its own record and never another's." A same-basis rerun
  therefore *replaces* the earlier record in the store; the earlier
  bytes survive only if they were committed to git in between.
- **Supersession precedent**: the Spec 087 adoption (commit `491f31c`)
  and the Spec 088 adoption (commit `3f30671`) each refreshed the T405
  pair after the ledger pin moved. Git renders the 088 refresh as
  renames (R099: `…--cf47a3fa5a80` → `…--070f8f0f476f`;
  `…--763e4f7b44f9` → `…--5b1d1c866b0e`); the superseded records are not
  in the store, only in git history. `settling-canonical.json`'s
  `re_derivations` list (2 entries) narrates the pin refreshes in prose.
- The **dual-run comparison** (semantics §7, `compare_runs`) compares
  two *candidates* over *one* ledger build: it refuses unless the
  semantics version, the ledger pin, and the corpus pin agree, and
  refuses when both runs carry the same candidate. It therefore cannot,
  by construction, compare two executions of the same work, and refuses
  exactly the cross-build pairs a junction analysis must speak to.
- `verify-canonicals` recomputes the **5 registered scenarios + 1
  comparison** against registered expectations in
  `settling-canonical.json`; `run_settling.py`'s `_first_divergences`
  localizes the first divergences (cap 8) — against the registered
  expectations, not between two live runs.
- Semantics §9: a run creates only a run record. §7: "Two readings are
  never blended into one verdict." The lumping principle exists in the
  semantics; the identity and junction machinery does not.
- `tools/ledger/run_settling.py materialize-sets` rewrites
  `glossa-indus/ledger/assignment-sets.json` (sets `incumbent`,
  `full-register`) **in place**, with no run record of the regeneration.

### The Spec 086/088 gate (`backend/glossa_lab/ledger_gate.py`, `backend/glossa_lab/gated_publish.py`)

- Check classes **V1–V10** (module header): V1 ledger validity, V2 count
  equivalence, V3 matrix recomputation, V4 relation-carrying citations,
  V5 map recomputation, V6 anchor shares, V7 lossless regeneration, V8
  settling canonicals (recomputation under the gate's own settle copies,
  plus the scenario/verdict separation check), V9 no write path (incl.
  the registered-writer census, `REGISTERED_WRITERS`), V10 program-map
  equivalence. The next free class number is **V11**.
- The gate never writes; publication (`gated_publish.py`:
  `publish_matrix`, `publish_map`, `publish_program_map`) replaces
  published artifacts only on ALL PASS.

### Backend experiment jobs (live backend, desktop host)

- Jobs live in the live database (`jobs`, `job_results` tables,
  `backend/glossa_lab/database.py`); a job id is execution-minted
  (`uuid.uuid4().hex[:12]`, `create_job`, line 916) and results are
  fetched per job id (`get_job_results`). Experiment graphs (27 live
  graphs per the Spec 087 census) execute as jobs.
- **There is no repo-side run record for a backend job.** When a stage
  record cites an experiment result, it cites numbers; the binding to
  the job id and the job's inputs lives, if anywhere, in prose. The
  surface has identity at execution and loses it at citation.

### Suite runs (pytest; CI and local)

- CI runs carry GitHub run ids, and the program's merge discipline
  already binds verdicts to them: `tools/delivery-check/check_delivery.py`
  resolves a run id + head SHA to per-job conclusions before any merge
  (used at every Spec 086/087/088 gate).
- Local evidence runs (the full-suite enumerations quoted in stage
  records) are cited by counts in prose. No run record exists for them.
- **Standing divergence instance class**: the tray teardown flake family
  (`test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named`,
  teardown ERROR, sqlite closed-database family) made CI attempt 1 and
  attempt 2 of the *same head SHA* diverge on PRs #497, #505, #509 and
  main's post-#503 run (2,512–2,549 passed, 0 failed, 1 ERROR vs clean
  rerun). Each was adjudicated by hand (log inspection + failed-jobs
  rerun) under a prose precedent. Two comparable runs, different
  results, no junction record — five times in three days.
- **In-tree rewrites**: suite runs regenerate
  `glossa-indus/claims/extracted_claims/*.json` (and occasionally
  `glossa-indus/reports/claim_reports/*.json`) in the working tree
  mid-run — one run's outputs become the next run's inputs. Today's
  controls are procedural: stage records restore the files (git
  checkout) before committing, and checks whose pristine-tree
  precondition is destroyed mid-run skip with the cause named. The
  rewrite itself is not part of any run record.

### Study freeze / re-execution records

- Studies freeze against hash-pinned records (per-spec freeze tests,
  `backend/tests/test_specNNN_freeze.py`; the C4 freeze gate,
  `tools/freeze-gate/check_freeze_gate.py`). The freeze-gate's **C2
  component is a manual junction precedent**: an independent worker
  recomputes gate-turning quantities from the spec text and pinned
  inputs only, and the recomputation is compared against the frozen
  values (`tools/freeze-gate/freeze_records.py scaffold-c2`).
- Study re-executions and invalidations are recorded as prose records
  in spec directories (e.g. Spec 054's governing append of 2026-10-25;
  the rerun/invalidation audit's 16 items). No run identity binds a
  re-execution's record to the execution that produced it.

### The ledger itself

- 907 lines, 876 claim entries (853 bundle + 23 extracted). Entry kinds:
  claim, annotation, reclassification, and `measurement` (registered
  2026-11-01; zero minted). **There is no run kind**, and this spec does
  not propose one: run records belong in run stores, not in the claims
  ledger (claim C089-18).

## Where the drafting brief's assumptions needed correction

1. The run-record supersession precedent is the Spec 087 + Spec 088
   **adoption** refreshes (commits `491f31c`, `3f30671`), not a
   Spec 088 S3/S4 act; git renders the 088 refresh as renames because
   the result blocks are near-identical — the store-level fact (old
   pair gone from the store, preserved in git history) is as the brief
   states.
2. `compare_runs` is narrower than "dual-run comparison" suggests: it
   refuses same-candidate pairs and cross-build pairs by construction.
   The junction rule must be built as a generalization beside it, not
   as a configuration of it.
3. Backend experiment jobs have execution-minted ids already; what is
   missing is not identity at execution but the repo-side citation
   binding. The spec's claim for that surface is a binding claim, not
   a minting claim.
4. Suite runs cited as evidence are of two kinds with different
   identity situations: CI runs (ids exist; the delivery checker binds
   verdicts to them) and local enumerations (no identity at all). The
   spec treats them separately (decision D-089-6).

## The boundary with the fabricated-delivery protocol

The 2026-11-04 fabricated-delivery protocol governs *presented*
results (background-delivery presentations are claims, never results;
gate reads run in the foreground). This spec governs *recorded
executions*: what a run is, how its results are stored and cited, and
what must happen when two recorded runs diverge. Neither substitutes
for the other: a fabricated delivery is not a run and creates no run
record; a run record does not certify that any presentation of it was
honest. Claim C089-20 states the boundary inside the spec.
