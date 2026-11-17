# Spec 094 — Stage 3 design note (the per-candidate verification method)

**Stage:** 3 — Verification redefined (C094-6..9)
**Date:** 2026-11-16
**Status:** written BEFORE the Stage 3 route was built, as plan.md
Stage 3 and task T302 require ("method fixed in the stage's design
note before the route is built"). The build follows this note; the
stage record (`stage-3-record-2026-11-16.md`) reports the build
against it.

## The question the method answers

C094-6 binds the granularity and the record — a candidate reaches
`verified` only through a recorded evaluation of that candidate,
citing the per-candidate evidence it rests on, effected by a named
human — and expressly does not establish a particular evaluation
method; Stage 3 fixes the method. This note is that fixing.

## The method

1. **Unit of evaluation: one candidate record.** A verification is
   an evaluation of exactly one candidate (one sign, one proposed
   reading). There is no batch act, no run-level act, and no
   aggregate signal that verifies: a foundation check, a test-suite
   result, a run's overall delta, and an SA delta are not
   evaluations of a candidate and cannot confer the status
   (C094-6, C094-7).
2. **Evaluator: a named human on the D-094-1 list.** The evaluator
   must validate as a named human on the D-094-1 approvers list
   under the `claim_stage` actor rules (`is_listed_approver`,
   reused, not redefined) — the same discipline Stages 1–2 applied
   to approval and pinning (D-094-1, C094-2). An automated identity
   can never verify; auto-verification stays abolished (D-094-3).
3. **What the evaluator does.** For that candidate alone, the
   evaluator examines the candidate's proposed reading against the
   per-candidate evidence the record cites — in the ordinary case
   the record's own pinned evidence artifact (Stage 2's standard:
   `evidence_ref` + `evidence_sha256` + `evidence_class`) — and
   records a judgement of that candidate: whether the cited
   evidence, read for this sign and this reading, supports treating
   the candidate as verified, and what would have changed the
   judgement is already on the record as the candidate's falsifier
   (Stage 1). The evaluation is a reading of evidence about one
   candidate, not a re-run of any pipeline.
4. **The record.** The evaluation is recorded on the candidate
   record itself, as first-class fields (C094-3's construction —
   gate inputs live on the record, never in the request that asks
   for a transition):
   - `verification_evaluator` — the named human who evaluated;
   - `verification_evaluated_at` — when;
   - `verification_evaluation` — the evaluation statement for this
     candidate: what was checked, for this sign and reading, and
     what the evidence showed (non-empty);
   - `verification_evidence_ref` — the per-candidate evidence the
     evaluation rests on (non-empty; see the run-level refusal in
     point 5);
   - `verification_outcome` — the evaluation's outcome:
     `verified` or `not_verified`. Only `verified` confers.
   These are `CANDIDATE_VERIFICATION_FIELDS`, carried by the
   pipeline's staging write beside Stage 1's gate fields and Stage
   2's evidence fields — starting empty, because the pipeline
   stages candidates and does not evaluate them.
5. **Run-level citations refuse.** A recorded
   `verification_evidence_ref` that names a run-level signal — a
   foundation check, a suite result, a run or SA delta — is a
   refusal, mechanically: the citation's normalized tokens are
   checked against a run-level token set, so a verification whose
   record cites only a run-level signal does not exist as a
   verification (C094-6's falsifier, second clause). Beyond that
   mechanical bar, whether the cited evidence is *relevant* is the
   evaluator's recorded judgement, not a machine check — the same
   presence-and-attribution posture Stage 1 took for falsifier
   quality (C094-1's cap).
6. **The recording act is a library act, not an endpoint.**
   Following Stage 2's design choice 3 (no pin route was added),
   `record_verification` in `glossa_lab/verification.py` is the
   recording act as a library function over a record: it validates
   the evaluator, the evaluation statement, the evidence citation,
   and the outcome, and returns a new record dict carrying the
   fields; the input record is not mutated, and a refusal raises
   and records nothing. No endpoint supplies verification inputs,
   and no transition route reads them from a request.
7. **Enforcement points.**
   - The verify transitions (`staging_verify_archive` and its
     deprecated alias, and `cleanup_staging`'s approved→verified
     flip) transition a candidate to `verified` only when its
     record passes BOTH the Stage 1 approval gate AND
     `verification_refusal` (the single verification check in
     `verification.py`). A candidate that passes approval but
     carries no valid per-candidate verification stays in staging,
     status untouched, reported in the new
     `blocked_no_verification` response field; when no approved
     candidate passes both gates, verify-archive refuses and
     writes nothing.
   - Promotion's MEDIUM binding (C094-8): MEDIUM is conferred
     exactly when `verification_refusal(candidate)` is None — the
     candidate carries a valid per-candidate verification
     evaluation recorded under this method. Status alone never
     suffices: a record whose `review_status` is `verified` but
     which carries no verification evaluation (the pre-094 archive
     stock's shape, per C094-12) promotes at LOW at most, as does
     an approved candidate whatever its evidence score. HIGH is
     untouched — promotion has never conferred it.
8. **Pre-gate stock.** Nothing already standing is moved
   (C094-12): pre-094 `verified` archive entries keep their
   recorded status as history. The binding in point 7 is the only
   consequence: without a recorded per-candidate evaluation they
   are not verified *under this spec*, so MEDIUM is not available
   to them until an evaluation is recorded.

## What this method does not establish

The claim binds granularity and record, not the method's
soundness: this note fixes *what counts as* a verification act and
*where it is recorded*, and the gates enforce exactly that shape.
Whether any individual evaluation is a *good* evaluation — whether
the evaluator read the evidence well — is not machine-checked and
is not claimed. The evaluation statement and its citation are on
the record precisely so that judgement stays attributable and
auditable after the fact.
