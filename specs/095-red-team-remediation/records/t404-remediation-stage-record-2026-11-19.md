# Spec 095 — T404 remediation stage record (2026-11-19)

**Stage.** The dedicated T404 remediation stage, run 2026-11-19 on
the owner's order of that day ("everything doable done today"),
following the route prepared for the owner with "dedicated
remediation stage" as the recommendation. Branch
`feat/095-t404-remediation` off main `66d9eab2`; PR #595; code
commits `c6f63ce3` and `8b271cc5`; this record and the re-run
records land as the stage's third commit on the same PR.

**What it answers.** The T404 audit of record
(`records/t404-run-2026-11-17.json`, `records/stage-4-record-2026-11-17.md`,
`records/t404-dashboard-leg-addendum-2026-11-18.md`) failed its
pre-fixed thresholds (`records/t404-thresholds-2026-11-17.md`):
functional corrected 10/15 (F2 not met), protocol corrected 2/8
(P1 not met), A2 not met (color-contrast serious on all six legacy
surfaces); the dashboard leg added A1 criticals (`label`,
`select-name`) on the new surfaces. Claim C095-13 stood open on
those failures, and T503 waits on this stage.

## 1. The remediation, item by item

**F01 — project create/update (was 422).** `POST /projects/import`
is the only create path and demanded a full bundle; the flat
minimal body the audit (and any simple caller) sends was refused.
It now normalizes a flat body (`name`/`label` plus the optional
fields) into a minimal bundle; a body with neither still refuses.
The re-run then exposed the same defect one layer down: `PUT
/projects/{id}` refused a partial update body (description alone)
because the schema required a label. The handler now merges a
partial body against the stored project — fields sent win, fields
not sent keep their stored values — and a create without a label
still refuses. Audit evidence after the fix: import 200, open 200,
update 200, delete 200, reopen-after-delete 404.

**F05/F06 — job pause/resume (was 409).** The Stage 4 record's
gloss was wrong; the mechanism, found by reproduction: a job
created with the default pipeline name is claimed by the engine
and fails within seconds, because that pipeline name is not
registered — and a failed job can no longer be paused or resumed.
The engine now has a dispatch gate: a job whose pipeline is not
registered is left pending, stamped with a `dispatch_wait` reason
on its params (the Jobs panel surfaces it, as it does
`resource_wait`), and excluded from later peeks so it cannot
starve the queue. Pause, resume, and cancel all work on such a
job. Two defects found in this fix during verification are fixed
with it: the peek/claim seam passes its exclusion argument only
when the set is non-empty (existing no-argument test doubles keep
working), and the exclusion set is keyed per database, because
the engine captures one Database per lifespan and one database's
deferred jobs must never exclude another's.

**F08 — report generation (was 503).** Two layers: the generator
script path resolved to `backend/` while every generator script
lives in `backend/scripts/`, and the lead template's readiness
named an input file that exists nowhere. Script resolution now
searches the scripts directory first; the template's stated
inputs name the benchmark file that exists. The audit's leg
generates the lead template at 200.

**F13 — migration rollback (no facility existed).** The ledger
gains a snapshot/restore facility in `ledger_intake.py`:
`snapshot_ledger` writes a self-contained manifest (existence,
size, raw-byte digest, embedded bytes) beside the ledger;
`restore_snapshot` verifies size and digest before writing,
refuses a missing or corrupt snapshot without touching the
ledger, and restores absence by unlinking; `rollback_migration`
restores the latest snapshot. Every migration write through
`write_ledger` snapshots its pre-state first, so every migration
write is rollback-able. The audit's F13 leg runs the migration
test suite in the audit tree and finds the facility: PASS.

**F09, F15 — no product defect.** Both raw failures are the
filed driver's own artifacts (a byte counter that cannot size a
parsed JSON payload; a hardcoded base-commit bundle name). They
are corrected, with the checks re-performed, in
`records/t404-remediation-scoring-corrections.json`.

**P3 — inscription-level entry from Data (was unreachable).**
Data now lands on an Inscriptions tab: the canonical export's
inscriptions in a real table, one click from any inscription's
own record with its four layers (observation, transcription,
hypothesis, and the claim layer named as its evidence trail).
Corpora and anchor sets keep their own tabs. The audit's P3 leg
opens an entry and finds the evidence trail: PASS.

**P4 — statement kinds on the claim surface (was two of six).**
A claim's detail now carries, as genuine content: its falsifier,
a "What this does not establish" card (the claim's recorded
does-not-establish statement, or an honest statement that none is
recorded), and a statement-kinds paragraph naming observation,
transcription, hypothesis, and claim and placing the entry. The
audit finds all six labels: PASS.

**P5 — reproduce one result (was unlabelled icons, no row).**
The saved-experiments list is a true grid (grid / row / gridcell
roles) whose run controls carry accessible names ("Run <name>",
"Add to sequential queue", "Run and email recipients on
completion", Pin/Unpin, Delete). The audit opens an experiment,
finds and activates the run affordance: PASS.

**P6 — submit a candidate (doorways landed on a dead surface).**
Both "Register a claim" doorways (program home, claims register)
now land on the researcher dashboard's contribution form — the
sanctioned staging-queue path, which requires a falsifier, a
named submitter, and an evidence reference that resolves to a
record. The filed legacy driver's fill cannot satisfy those
requirements and its candidate does not land; scored FAIL under
the corrections standard (see the corrections file). The
dashboard leg's P6 meets the form's real requirements and is
verified in the store: PASS.

**P7 — follow a candidate (was nothing to follow).** The claims
register now carries a "Candidates in the staging queue" card:
every staged candidate with its statement, stage, status,
submitter, and falsifier, labelled as candidates awaiting
adjudication, not register claims. The dashboard leg's
P7-capability check follows its store-verified candidate to this
card and finds it with its stage: PASS. The legacy step as driven
remains a fail on the record (its premise candidate never
registered).

**P8 — export (was no affordance).** Report rows now carry a
Download action beside Open (fetch, blob, named download). The
legacy leg downloads a real report file (17,299 bytes); the
dashboard leg exports a claim's audit trail from its detail and
verifies the downloaded file's contents against the record:
PASS both.

**Contrast (A2; was serious on every surface).** The shell
sidebar headers, the navigation badge, the service chips, the
shared palette's muted/faint tones in both themes, the stage
colours (a dark variant set), the claims filter chip's
on-accent text, the experiment builder's theme grays, the
corpora emerald family, the evidence violet family, and the
settings furniture are lifted to pass. The audit's axe pass over
the six legacy surfaces reports zero critical and zero serious;
the dashboard leg's axe pass over the seven dashboard surfaces
reports the same. (The moderate `heading-order` and `region`
classes — the app shell's landmark structure — remain, unscored,
exactly as the addendum recorded them.)

**Dashboard A1 (was critical: `label`, `select-name`).** Every
form control on the inscription explorer, evidence inspection,
and researcher contribution surfaces now carries an accessible
name (ids with matching labels); the hypothesis comparison's
scrollable readings region is keyboard-focusable. The dashboard
leg's axe pass reports zero critical on all seven surfaces.

## 2. Test evidence (payload verdicts)

- New backend tests, `backend/tests/test_spec095_t404_remediation.py`:
  15 tests over the five functional legs (import shapes, PUT merge,
  dispatch deferral incl. queue non-starvation, report readiness
  and generation, snapshot/restore/rollback incl. corrupt-snapshot
  refusal) — all pass against the real app, engine, and ledger
  write path.
- Targeted backend set (remediation + projects + jobs + engine
  shutdown race + ledger migration), run in adversarial order:
  48 passed, 0 failed.
- This PR's CI, per job, on the code as merged-ready: all 10 jobs
  pass (Backend tests; Frontend tests; Indus public validation;
  Shell wrappers on three systems; Evidence Graph smoke; Freeze
  gate; Ledger/matrix/map gate; Cloud image smoke). The first CI
  round on this branch failed Backend (one test: the shutdown-race
  claim test, whose job shape the dispatch gate legitimately
  intercepts — repaired by naming a registered pipeline, assertion
  unchanged) and Frontend (9 tests: the claims-register crash on
  an unexpected contributions shape, since guarded; eight
  surface-navigation expectations updated to the remediated
  surfaces). Both repairs are in `8b271cc5` and are covered by the
  green round.
- Playwright, locally against the remediated build: the affected
  and adjacent specs pass (program home, claims, corpora, reports,
  researcher dashboard, experiment builder, jobs, navigation
  including the updated Data test). The two API specs that
  hardcode the CI backend's port were verified against a ported
  copy on a free port (11/11), since this machine's port 8001 is
  its standing service; the specs themselves run unmodified in CI.
  A local full-suite backend run was stopped at 73% with no
  failures observed; the CI per-job verdicts above supersede it.
- An axe sweep of all fourteen surfaces in both themes (own
  instrument, pre-audit): zero violations in the default (light)
  theme everywhere; in the dark theme, zero everywhere except the
  Settings view's legacy section (9 color-contrast nodes,
  pre-existing hardcoded grays in a section this stage did not
  rebuild) — recorded here as an observation outside the audit's
  scored theme, not as a threshold item.

## 3. The re-run, scored against the pre-fixed thresholds

Instance: a fresh copy of the remediated committed tree
(`8b271cc5`) at `~/glossa-work/spec095-s4/audit-instance`, backend
on 127.0.0.1:8417 with `GLOSSA_API_AUTH=off`, the committed
`frontend/dist` — the Stage 4 instance definition. The legacy leg
was run with the filed driver byte-identical
(`records/t404-audit-driver.py`); the dashboard leg with
`records/t404-remediation-dashboard-leg-driver.py`, implementing
the addendum's eight steps and evidence standards.

| Threshold (fixed 2026-11-17) | Stage 4 / addendum | Re-run (raw) | Re-run (corrected) |
| --- | --- | --- | --- |
| F1 — at least 12 of 15 functional items attempted | 15 attempted | 15 attempted | 15 attempted |
| F2 — at least 75% of attempted pass | 66.7% corrected — NOT MET | 13/15 (86.7%) | 15/15 (100%) — MET |
| P1 — at least 6 of 8 protocol steps | 2/8 corrected — NOT MET | 7/8 | 6/8 — MET |
| A1 — zero axe critical | met (legacy); NOT MET (dashboard) | zero, both legs | zero, both legs — MET |
| A2 — at most 3 serious + keyboard | NOT MET (contrast, all surfaces) | zero serious, both legs; keyboard PASS both legs | MET |

Dashboard leg, its own scores: protocol 8/8 (P1 met), A1 met,
A2 met. Its P6 candidate (`RDC-20261119222801-001`) is verified
in the instance's staging store exactly once; its P7 re-ran the
settling run of record on scratch (assigned_count recorded 94,
re-run 94; assigned_share identical; corpus identity verified);
its P8 verified the downloaded audit trail against the record.

**Package verdict: PASS** — the filed driver's own scoring reads
PASS on the raw output, and every threshold is still met with
the corrections applied.

## 4. Dispositions

- **T404 is complete.** Its box in `tasks.md` is ticked by this
  stage's records commit.
- **C095-13 is discharged** on this re-run, with one named
  remainder carried, exactly as the thresholds record declared in
  advance: the audit's authenticated cloud legs were out of scope
  for the scratch instance (auth off) and remain with the standing
  Spec 083 proofs remainder, for the owner's sessions. Nothing in
  this stage's verdict rests on them.
- **T503 may proceed.** The closeout's other named remainders are
  untouched by this stage and carry to it: the T303 ledger
  re-statement (filed-not-applied, no vehicle exists), and the
  RT-03 README supersession banner (owner-gated, D-095-5 — not
  done here, flagged for the closeout record).

## 5. What was not done

- The RT-03 README supersession banner: owner-gated, out of
  scope; flagged, not done.
- The Settings view's legacy section keeps its hardcoded grays in
  the dark theme (see §2). The audit scores the default theme,
  where the view is clean; the dark-theme debt is recorded here
  for whichever stage next rebuilds that section.
- No authenticated or cloud leg was run; see the C095-13
  remainder above.
