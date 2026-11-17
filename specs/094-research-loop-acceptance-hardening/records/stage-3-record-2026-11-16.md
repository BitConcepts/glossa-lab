# Spec 094 — Stage 3 record (verification redefined)

**Stage:** 3 — Verification redefined (C094-6..9)
**Date:** 2026-11-16
**Base:** `81083cf6d944a6d196c6f685b712b19c0b6aa1cf` (origin/main, the
Spec 094 Stage 2 merge)
**Branch:** `spec/094-s3-verification-redefined`
**Tasks discharged:** T301, T302, T303.
**Claims discharged:** C094-6, C094-7, C094-8, C094-9 (on the
evidence named per claim below).
**Design note (written before the build, as T302 requires):**
`records/stage-3-design-note-2026-11-16.md`.

Nothing in this stage touched the live backend or its stores: all
work ran in a fresh clone on the mini-server against synthetic
fixtures, the research loop was never run against live stores, and
no live store was read or written (C094-13 held throughout).

## The T303 demonstration (before any change)

C094-9 rests on a drafting observation, so the current behaviour
was demonstrated from the code first, on synthetic stores, with
the base tree unmodified (demonstration script run against
`backend/glossa_lab/api/research_loop.py` at the base commit; the
same script was re-run after the build — see below):

- **T303.** A staged candidate with `evidence_score` 0.9 and NO
  recorded `sa_delta`, read through `get_staging`, came back
  carrying `"sa_delta": 0.108` — exactly `round(0.9 * 0.12, 3)`,
  the fabricated fallback. The observation reproduces. It is
  response-shaping only: `get_staging` writes nothing, and the
  staging file on disk was unchanged by the read.
- **T301 (companion demonstration).** An approved candidate run
  through `_run_anchor_lifecycle` with a clean foundation check
  (`foundation_check: {n_fail: 0}`) came back in the archive file
  as `review_status: "verified"` with `sa_delta: 0.1`,
  `archived_reason: "auto_verified"`; the staging file was left
  empty. The flat-delta flip reproduces exactly as claimed.

After the build, the identical script shows: the staging response
carries **no `sa_delta` key at all** for the same candidate, and
the lifecycle leaves the approved candidate in staging, status
untouched, with the archive still empty.

## What was built

### T301 — Flat-delta flip removed (C094-7)

- `_run_anchor_lifecycle` no longer reads the synthesis foundation
  check, no longer derives a flat `sa_delta` (`0.1` / `-0.05`), and
  no longer flips `approved` → `verified` or auto-archives flipped
  candidates. The `lifecycle_advance` event no longer carries an
  `auto_verified` count, and the log line reports expiries only.
- Its other duty is unchanged, exactly: rejected candidates older
  than 7 days still expire and are archived
  (`expired_after_7d`), proven by test. The manual-archive route's
  docstring no longer claims the lifecycle archives verified
  candidates.

### T302 — Per-candidate verification + the MEDIUM binding (C094-6, C094-8)

- The method is fixed in the design note (see header), written
  before the route was built: one candidate per evaluation; a
  named human on the D-094-1 list as evaluator; the evaluation
  examines that candidate's proposed reading against the
  per-candidate evidence the record cites; the outcome is recorded
  as `verified` or `not_verified`. As the design note and the
  claim both state, this binds granularity and record — it does
  not establish the method's soundness, and no machine check of
  evaluation quality is claimed.
- New module `backend/glossa_lab/verification.py` carries the
  method. `record_verification(record, *, evaluator, evaluation,
  evidence_ref, outcome="verified", evaluated_at=None)` is the
  recording act: it validates the evaluator as a listed named
  human (`is_listed_approver`, reused, not redefined), requires a
  non-empty evaluation statement and a non-empty per-candidate
  evidence citation, refuses a citation naming a run-level signal
  (a foundation check, a suite result, a run or SA delta —
  `is_run_level_citation`), and returns a NEW record dict carrying
  the five `CANDIDATE_VERIFICATION_FIELDS`
  (`verification_evaluator`, `verification_evaluated_at`,
  `verification_evaluation`, `verification_evidence_ref`,
  `verification_outcome`). The input record is not mutated; a
  refusal raises `VerificationError` and records nothing.
- The fields are first-class on the candidate record, carried by
  the pipeline's staging write (`pipelines/research_loop.py::
  _save_staging`, `setdefault`, beside Stage 1's gate fields and
  Stage 2's evidence fields) — they start empty, and a record
  carrying no evaluation is not verified. Pre-existing records are
  not rewritten (C094-12).
- `verification_refusal(candidate)` is the single check every
  surface reads: it refuses on an absent or incomplete evaluation,
  an outcome other than `verified`, a run-level-only citation, an
  automated evaluator, or an evaluator who is not a listed named
  human. A record whose `review_status` is `verified` but which
  carries no evaluation — the pre-094 archive stock's shape —
  refuses here: status alone is not verification under this spec.
- The verify transitions enforce it. `staging_verify_archive`
  (and its deprecated alias) and `cleanup_staging` transition a
  candidate to `verified` only when its record passes BOTH the
  Stage 1 approval gate AND `verification_refusal`. Candidates
  passing approval but carrying no valid evaluation stay in
  staging, status untouched, reported in the new
  `blocked_no_verification` response field; when no approved
  candidate passes both gates, verify-archive refuses
  (`ok: False`) and writes nothing. The routes perform the
  transition for records that carry the evaluation; they do not
  themselves confer the evaluation.
- The MEDIUM binding at promotion: `promote_to_anchors` confers
  MEDIUM exactly when `verification_refusal(c)` is None. The
  former rule (`review_status == 'verified' OR
  evidence_score >= 0.8`) is removed: an approved-but-unverified
  candidate caps at LOW whatever its score, and a `verified`
  record carrying no evaluation caps at LOW too. A promoted
  anchor's `basis` records the `verification_evaluator` its
  MEDIUM rests on. HIGH is untouched.

### T303 — Fabricated fallback delta removed (C094-9)

- `get_staging` no longer substitutes `round(score * 0.12, 3)`.
  Where no SA comparison has run, the candidate's response carries
  no `sa_delta` key at all (absent, including a recorded null,
  which is normalized to absent); where a comparison did record a
  delta, the recorded value is carried as recorded. The
  `recommended` derivation now rests on the recorded delta only,
  or on the score alone. The committed frontend already guards on
  `sa_delta !== undefined`, so the absent shape is the one its
  surface expects.

## Design choices taken inside the adopted decisions

1. **The MEDIUM binding reads the evaluation, not the status.**
   "Verified under C094-6" (C094-8's phrase) is the recorded
   per-candidate evaluation passing `verification_refusal`. Two
   consequences, both intended: a `verified`-status record with no
   evaluation (pre-094 stock) caps at LOW, and a candidate whose
   evaluation is recorded but whose status has not yet been
   transitioned is verified under the spec and promotes at MEDIUM.
   Status is bookkeeping; the evaluation is the act.
2. **No verification route was added.** Stages 1–2's pattern holds:
   gate inputs are recorded by adjudication, and no endpoint exists
   whose request supplies them (C094-3). `record_verification` is
   the recording act as a library function; wiring an adjudication
   surface that calls it is operations work, not a gate.
3. **Gate composition at the verify transitions.** The approval
   gate runs first, the verification gate second, so the
   established `blocked_no_approval_gate` list keeps its meaning
   and `blocked_no_verification` names exactly the records that
   passed approval and failed verification.
4. **The run-level citation bar is mechanical and narrow.** Token
   compounds naming the run-level machinery (foundation check,
   suite, run/SA/overall delta) refuse; an ordinary per-candidate
   citation that merely contains a word like "run" in another
   sense (a concordance run number) is not refused on shape.
   Beyond that bar, citation relevance is the evaluator's recorded
   judgement — the design note states this cap plainly.
5. **Absent means the key is absent.** For T303 the surface
   presents the delta as absent by omitting `sa_delta` from the
   response candidate entirely, not by nulling it: a null would
   still be a carried `sa_delta` field, and the frontend's guard
   treats absence (undefined) as the no-comparison shape.

## Test actuals

New battery: `backend/tests/test_spec094_stage3_verification.py`
(18 tests) — the recording act (fields recorded, input unmutated;
automated and unlisted evaluators refused; run-level and empty
inputs refused); the run-level citation shapes; the refusal units
(bare `verified` status, run-level citation, a `not_verified`
outcome, an automated evaluator recorded after the fact); the
staging write carrying all five verification fields; T301's
acceptance test (a lifecycle run over approved candidates under a
clean foundation check flips nothing) plus the unchanged expiry
duty; the verify transitions (unevaluated refuses outright,
evaluated verifies with the evaluation on the archived record, a
mixed batch partitions, cleanup does not verify an unevaluated
record); the MEDIUM binding (verified promotes at MEDIUM with the
evaluator in the basis; unverified caps at LOW at score 0.99;
`verified` status without an evaluation caps at LOW; an evaluated
candidate promotes at MEDIUM on the evaluation); and T303 (no
`sa_delta` in the response for candidates with no recorded
comparison, incl. a recorded null; a recorded delta carried as
recorded).

Targeted run (the new battery plus the Stage 1 and Stage 2
batteries and the three pre-existing integrity batteries), CI
invocation and environment, local: **75 passed** (18 new + 15
Stage 1 + 19 Stage 2 + 11 promotion-integrity + 5
promotion-evidence + 7 staging-action).

Full backend suite, CI invocation (GPU files ignored) with the
one local deselect noted in Deviations — completed locally in
two parts split at the slow Spec 086 gate file:

- Part 1 (the whole suite except `test_spec086_ledger_gate.py`):
  **2,807 passed, 64 skipped, 1 deselected, 0 failed** (197.22s,
  exit 0).
- Part 2 (`test_spec086_ledger_gate.py` alone, same invocation
  and environment): **23 passed, 44 skipped, 0 failed** (629.92s,
  exit 0).

Union: 2,939 tests collected across the two parts — 2,830 passed,
108 skipped, 1 deselected, 0 failed. The union is complete: every
collected test ran in exactly one part.

Ruff on all changed files: clean.

## Existing-test fixture updates (named, per the stage's effect)

The stage changes what a conforming candidate record is and what
the verify transitions require, so three pre-existing fixtures
were updated to the conforming shape — a recorded per-candidate
verification evaluation (evaluator "Tristen Pierson", evidence
cited as LEDGER.md, outcome `verified`). No assertion in them was
weakened and their deciding gates are unchanged:

- `tests/test_spec094_stage1_approval_gate.py` — `_gated()` gains
  the five verification fields, so the Stage 1 verify-route tests
  keep the approval gate as their deciding gate.
- `tests/test_promotion_integrity.py` — `_candidate()` gains the
  five verification fields, so its MEDIUM positive control
  promotes at MEDIUM under the C094-8 binding (verified under
  C094-6), not on status or score.
- `tests/test_staging_promotion_evidence.py` — the verify-archive
  route/alias test's inline candidate gains the five verification
  fields; the H26 evidence-gate tests in that file are untouched
  (they assert promotion counts, not confidence).

## Ledger gate (this tree, before push)

- `tools/ledger/check_ledger_gate.py --all`:
  `summary: 29 PASS / 0 FAIL / 1 NOT-RUN` — `RESULT: PASS`
- `tools/ledger/check_ledger_gate.py --regen`:
  `summary: 32 PASS / 0 FAIL / 0 NOT-RUN` — `RESULT: PASS`

Both hold the standing profile exactly, read from sequential runs
on the restored, quiet tree (see Deviations for the voided first
attempt). In-tree regenerations from the gate and suite runs were
restored before committing; the committed tree carries only this
stage's changes. (Local gate runs are recorded here as stage
evidence; no CI claim is made from them — the PR's CI read is the
parent's gate.)

## Claims discharged

- **C094-6** — "verified" is per-candidate or it is nothing:
  verification is a recorded evaluation of one candidate, citing
  the per-candidate evidence it rests on, effected by a named
  human on the D-094-1 list; the verify transitions refuse any
  record without one, and a verification citing only a run-level
  signal is refused at recording time and at every gate.
- **C094-7** — the flat-delta auto-verification mechanism is
  gone: the `sa_delta = 0.1` construction and the approved →
  verified flip are removed from `_run_anchor_lifecycle` (not
  tuned), demonstrated before and after from the code, and proven
  by the lifecycle acceptance test; its expiry duty is unchanged.
- **C094-8** — MEDIUM means verified under this spec: promotion
  confers MEDIUM exactly on candidates carrying a valid
  per-candidate verification evaluation; an unverified candidate
  caps at LOW at score 0.99, and a `verified` record carrying no
  evaluation — the pre-094 stock's shape — caps at LOW too.
- **C094-9** — no fabricated SA delta is presented as measured:
  the current behaviour was first demonstrated from the code
  (0.9 → 0.108, exactly the claimed construction), and after the
  build no staging response carries an `sa_delta` for a candidate
  with no recorded comparison, while a recorded delta is carried
  as recorded.

## Deviations

- The full local suite deselects
  `tests/test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`
  by its plain nodeid, per the standing local-run discipline for
  that environment-sensitive test; CI is authoritative for it. No
  CI claim is made from any local run in this record.
- The local full-suite evidence was gathered in two parts, split
  at `tests/test_spec086_ledger_gate.py` (whose tests re-run the
  ledger gate machinery against the real tree and crawl on this
  box — part 2 took 629.92s here). Both parts ran to completion
  as separate invocations with identical environment and exit 0;
  the union covers all 2,939 collected tests.
- The first `--regen` gate attempt was run concurrently with the
  suite and read `22 PASS / 7 FAIL / 1 NOT-RUN`: the suite was
  concurrently regenerating the extracted-claims files in-tree,
  so recorded hashes mismatched mid-run. That reading is VOID —
  a concurrency artifact of this stage's own evidence gathering,
  not a tree state. Both gate modes were re-run sequentially on
  the restored quiet tree and hold the standing profile exactly,
  as recorded above.
- Two detached-run ssh sessions dropped (the known tunnel-proxy
  broken-pipe); the detached jobs on the box were unaffected, and
  every result above was read from the runs' own log files on the
  box.
- No other deviations. Scope held to T301 + T302 + T303 exactly:
  no Stage 4–5 work, no live-store access, no loop run.
