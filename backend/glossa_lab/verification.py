"""Spec 094 Stage 3 — per-candidate verification (C094-6, C094-8).

"Verified" is a per-candidate act again, and nothing else confers
it. The method is fixed in the stage's design note
(``specs/094-research-loop-acceptance-hardening/records/``
``stage-3-design-note-2026-11-16.md``), written before this module:

- **Unit.** A verification is a recorded evaluation of exactly one
  candidate — one sign, one proposed reading. No run-level
  aggregate (a foundation check, a suite result, a run's overall
  delta, an SA delta) is an evaluation of a candidate and none
  confers the status.
- **Evaluator.** The evaluation is effected by a named human on the
  D-094-1 approvers list, validated by the ``claim_stage`` actor
  rules (:func:`glossa_lab.claim_stage.is_listed_approver`, reused,
  not redefined). Automated identities never verify; the automatic
  route stays abolished (D-094-3).
- **Record.** The evaluation lives on the candidate record as
  first-class fields (:data:`CANDIDATE_VERIFICATION_FIELDS`): the
  evaluator, the timestamp, the evaluation statement for this
  candidate, the per-candidate evidence it rests on, and its
  outcome. Gate inputs live on the record, never in the request
  that asks for a transition (C094-3's construction rule, applied
  here as at Stages 1–2: the recording act is a library function,
  :func:`record_verification`; no endpoint supplies its inputs).
- **Run-level citations refuse.** A recorded evidence citation that
  names a run-level signal is a refusal, mechanically
  (:func:`is_run_level_citation`). Beyond that bar, whether the
  cited evidence is relevant is the evaluator's recorded
  judgement, not a machine check — the claim binds granularity and
  record, not the method's soundness, and this module claims no
  more than the design note does.

The verify transitions and the promotion MEDIUM binding both read
:func:`verification_refusal` — the single check — so "verified
under this spec" has exactly one meaning on every surface.

This module reads and writes nothing: it computes over record
dicts supplied by the caller.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from glossa_lab.claim_stage import is_automated_actor, is_listed_approver

__all__ = [
    "CANDIDATE_VERIFICATION_FIELDS",
    "VERIFICATION_OUTCOMES",
    "VerificationError",
    "is_run_level_citation",
    "is_verified_under_spec094",
    "record_verification",
    "verification_refusal",
]


class VerificationError(ValueError):
    """A verification recording was refused (fail-closed)."""


#: The Stage 3 verification fields of an anchor-path candidate
#: record (Spec 094, C094-6): the recorded per-candidate evaluation
#: the verify transitions and the MEDIUM binding read. They are
#: first-class fields of the candidate record, carried by the
#: pipeline's staging write beside Stage 1's gate fields and Stage
#: 2's evidence fields — never supplied in the request that asks
#: for a transition.
CANDIDATE_VERIFICATION_FIELDS: tuple[str, ...] = (
    "verification_evaluator", "verification_evaluated_at",
    "verification_evaluation", "verification_evidence_ref",
    "verification_outcome",
)

#: The outcomes a recorded evaluation may carry. Only "verified"
#: confers the status; a "not_verified" evaluation is a recorded
#: per-candidate judgement too, and it confers nothing.
VERIFICATION_OUTCOMES: tuple[str, ...] = ("verified", "not_verified")


def _tokens(text: Any) -> set[str]:
    """Normalized token set of a citation or name: case-folded, with
    spaces / hyphens / punctuation folded to token boundaries (the
    ``claim_stage`` actor normalization shape, applied to
    citations)."""
    norm = str(text or "").strip().lower()
    for ch in "-/.:#":
        norm = norm.replace(ch, " ")
    return set("_".join(norm.split()).split("_")) - {""}


def is_run_level_citation(ref: Any) -> bool:
    """True when an evidence citation names a run-level signal — a
    foundation check, a test-suite result, a run or SA delta —
    rather than per-candidate evidence. Fail-closed in the other
    direction: an empty citation is not run-level, it is absent,
    and the refusal handles absence."""
    if not isinstance(ref, str) or not ref.strip():
        return False
    tokens = _tokens(ref)
    # "foundation_check" and its kin: the token pairs that name the
    # run-level machinery. Bare "delta"/"run" tokens are checked as
    # part of those compounds so a per-candidate ref that merely
    # contains an ordinary word is not refused on shape alone.
    if "foundation" in tokens or "suite" in tokens:
        return True
    if "delta" in tokens and tokens & {"sa", "run", "aggregate", "overall"}:
        return True
    return "run" in tokens and "delta" in tokens


def record_verification(
    record: dict[str, Any],
    *,
    evaluator: Any,
    evaluation: Any,
    evidence_ref: Any,
    outcome: str = "verified",
    evaluated_at: str | None = None,
) -> dict[str, Any]:
    """Record a per-candidate verification evaluation on a candidate
    record (C094-6).

    The evaluator must validate as a named human on the D-094-1
    approvers list (an automated identity cannot verify —
    C094-2/D-094-3); the evaluation statement must be non-empty;
    the cited evidence must be non-empty per-candidate evidence,
    not a run-level signal; the outcome must be one of
    :data:`VERIFICATION_OUTCOMES`. Returns a NEW record dict
    carrying the verification fields; the input record is not
    mutated. Refusals raise :class:`VerificationError` and record
    nothing.
    """
    if not is_listed_approver(str(evaluator or "")):
        raise VerificationError(
            f"evaluator {evaluator!r} does not validate as a named "
            "human on the D-094-1 approvers list; verification is a "
            "named-human act and automated identities cannot verify "
            "(Spec 094 C094-2, C094-6)")
    if not isinstance(evaluation, str) or not evaluation.strip():
        raise VerificationError(
            "a verification requires a non-empty evaluation statement "
            "for this candidate (Spec 094 C094-6)")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        raise VerificationError(
            "a verification must cite the per-candidate evidence it "
            "rests on (Spec 094 C094-6)")
    if is_run_level_citation(evidence_ref):
        raise VerificationError(
            f"verification evidence {evidence_ref.strip()!r} names a "
            "run-level signal; no run-level aggregate — a foundation "
            "check, a suite result, a run's overall delta — confers "
            "verified status (Spec 094 C094-6)")
    if outcome not in VERIFICATION_OUTCOMES:
        raise VerificationError(
            f"verification outcome {outcome!r} is not one of "
            f"{VERIFICATION_OUTCOMES} (Spec 094 C094-6)")
    verified = dict(record)
    verified["verification_evaluator"] = str(evaluator)
    verified["verification_evaluated_at"] = (
        evaluated_at or datetime.now(UTC).isoformat(timespec="seconds")
        .replace("+00:00", "Z"))
    verified["verification_evaluation"] = evaluation
    verified["verification_evidence_ref"] = evidence_ref
    verified["verification_outcome"] = outcome
    return verified


def verification_refusal(candidate: dict[str, Any]) -> str | None:
    """The refusal reason for a candidate that is not verified under
    Spec 094 (C094-6), or None when the candidate carries a valid
    per-candidate verification evaluation.

    Every input is read from the candidate RECORD — never from a
    request. Refuses when the recorded evaluation is absent or
    incomplete, when its outcome is not `verified`, when it cites
    only a run-level signal, when its evaluator is an automated
    identity, or when its evaluator does not validate as a listed
    named human. A record whose `review_status` is `verified` but
    which carries no such evaluation — the pre-094 archive stock's
    shape — refuses here: status alone is not verification under
    this spec (C094-8, C094-12).
    """
    evaluator = candidate.get("verification_evaluator")
    if not isinstance(evaluator, str) or not evaluator.strip():
        return ("candidate record carries no verification evaluator; "
                "verified status requires a per-candidate evaluation "
                "recorded by a named human (Spec 094 C094-6)")
    if is_automated_actor(evaluator):
        return (f"recorded verification evaluator {evaluator!r} is an "
                "automated identity; automated actors cannot verify "
                "(Spec 094 C094-2)")
    if not is_listed_approver(evaluator):
        return (f"recorded verification evaluator {evaluator!r} does "
                "not validate as a named human on the D-094-1 "
                "approvers list (Spec 094 C094-6)")
    evaluated_at = candidate.get("verification_evaluated_at")
    if not isinstance(evaluated_at, str) or not evaluated_at.strip():
        return ("candidate record carries no verification timestamp; "
                "a verification is a recorded evaluation, dated on "
                "the record (Spec 094 C094-6)")
    evaluation = candidate.get("verification_evaluation")
    if not isinstance(evaluation, str) or not evaluation.strip():
        return ("candidate record carries no verification evaluation "
                "statement; a run-level signal is not an evaluation "
                "of this candidate (Spec 094 C094-6)")
    evidence_ref = candidate.get("verification_evidence_ref")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        return ("candidate record's verification cites no "
                "per-candidate evidence (Spec 094 C094-6)")
    if is_run_level_citation(evidence_ref):
        return (f"candidate record's verification cites "
                f"{evidence_ref.strip()!r}, a run-level signal; no "
                "run-level aggregate confers verified status "
                "(Spec 094 C094-6)")
    if candidate.get("verification_outcome") != "verified":
        return ("candidate record's verification outcome is not "
                "'verified'; a recorded evaluation that did not "
                "conclude verified confers nothing (Spec 094 C094-6)")
    return None


def is_verified_under_spec094(candidate: dict[str, Any]) -> bool:
    """True when the candidate is verified under Spec 094: it
    carries a recorded per-candidate verification evaluation that
    passes :func:`verification_refusal`. This — not the
    `review_status` string alone — is what promotion's MEDIUM
    binding reads (C094-8)."""
    return verification_refusal(candidate) is None
