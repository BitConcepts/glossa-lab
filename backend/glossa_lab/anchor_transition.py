"""Gated transition service for the anchor path — Spec 094 Stage 4
(T401; claim C094-10).

Every status transition on an anchor-path record (the candidate
records carried by ``outputs/anchor_staging.json`` and
``outputs/anchor_staging_archive.json``) is effected through this
module. It is the single writer of ``review_status`` on those
records: no endpoint or lifecycle code writes the field directly,
and the removal of the direct writes is proven by census, not by
reading the diff (see the Stage 4 record).

The service carries the guarantees of the claim lifecycle's
transition service (:func:`glossa_lab.claim_stage.transition_stage`)
onto the anchor path's own vocabulary:

* **one-step moves** — the only forward moves are the anchor
  lifecycle's own steps: ``staged``/``blocked`` → ``approved`` →
  ``verified`` → ``promoted``. No route skips a step: there is no
  staged → verified and no staged → promoted move. Promotion from
  ``approved`` is a step of the anchor graph in its own right (the
  promote route has always acted on approved and verified records
  alike); what it may confer is bound elsewhere — an unverified
  candidate promotes at LOW at most (C094-8), and its basis records
  the true status it promoted from.
* **actor validation with the automated ceiling** — actors are
  classified by the ``claim_stage`` actor rules, reused not
  redefined. An automated actor may effect only transitions whose
  mapped stages (below) both sit at or below ``checked``; a
  transition touching a mapped stage above ``checked`` requires a
  named-human actor, and advancing into a mapped stage above
  ``checked`` additionally requires a non-empty evidence trail.
* **an evidence trail** — every transition appends one entry to the
  record's append-only ``review_history`` (keys in
  ``REVIEW_HISTORY_KEYS``: the anchor statuses, the mapped stages,
  the actor, the timestamp, the evidence refs, the reason). A
  refused transition appends nothing and changes nothing.

**The stage-vocabulary mapping** (the design question T401 leaves
to the stage record; answered here and in
``records/stage-4-record-2026-11-16.md``): the anchor path's
``review_status`` values map onto the claim-stage axis
(``created → checked → explained → accepted → digested``) as

* ``staged`` → ``created`` — a candidate exists and is unexamined;
* ``blocked`` → ``created`` — a candidate the pipeline could not
  stage cleanly; the same lifecycle rank as ``staged`` (approval is
  valid from either, per the approve route's state guard);
* ``approved`` → ``checked`` — a named human has examined the
  record and approved it: it has been *checked*, and nothing above
  ``checked`` is implied by approval;
* ``verified`` → ``explained`` — the first rank above ``checked``:
  a recorded per-candidate evaluation (C094-6) states the basis on
  which this candidate stands verified, which is exactly the
  named-human-plus-evidence crossing ``transition_stage`` guards;
* ``promoted`` → ``accepted`` — the anchor register accepts the
  candidate: its reading enters the accepted register on the
  recorded basis the promotion gates verified;
* ``rejected`` → ``created`` — rejection returns a candidate to
  unaccepted standing; the rejection itself is preserved in the
  record's append-only ``rejection_history`` (never erased), and
  the transition is demotion-class: it requires a recorded reason;
* ``expired`` → ``created`` — an expired rejection is a
  created-standing record archived out of the queue; expiry is the
  lifecycle's bookkeeping on a rejected record.

``digested`` has no anchor-path counterpart and is deliberately
unmapped: digestion on the claim axis is independent scholarly
engagement with a claim, an act the anchor path never performs.
Promotion is acceptance, not digestion, and no anchor record is
ever stamped ``digested`` by this path.

Two scope notes, stated plainly. First, the service maintains the
record's ``review_history`` trail and its ``review_status``; it
does not stamp the claim-stage cache fields (``stage``,
``stage_source``, ``stage_as_of``, ``stage_history``) onto anchor
records — pre-094 anchor records carry no such fields (C094-12:
nothing standing is rewritten), and the mapping above is the
service's rule parameter, not a stored assertion. Second, the
closure is **path-scoped** (C094-10's own cap): record *creation*
(the pipeline's staging write, which sets ``staged``/``blocked``
on new records and never rewrites an existing record's status) and
record *removal* (delete / prune) are not transitions and do not
pass through this service; a bare edit of a store file is outside
any code path by construction, which is what the storage-edit
probe measures (T403) and why the claim binds code paths, not
storage.

The actor each route passes is the most truthful identity it has:
for the gated transitions it is the human the record itself names
(approve → the recorded approver; verify → the recorded
verification evaluator; promote → the recorded approver — the
Stages 1–3 gates have already validated that identity from the
record before the service is called). For operator bookkeeping
with no record-carried human (reject, re-stage, manual archive),
the route names its own surface (``staging_action``,
``staging_archive``); for the lifecycle's expiry it names the
loop (``research_loop``, an allowlisted automated actor, bound by
the ceiling — expiry sits at ``created`` rank on both sides, so
the ceiling admits it).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Iterable

from glossa_lab.claim_stage import (
    STAGE_ORDER,
    is_automated_actor,
    is_named_human,
    validate_stage_value,
)

#: The anchor path's status vocabulary (the values ``review_status``
#: takes on staging and archive records).
ANCHOR_STATUSES: tuple[str, ...] = (
    "staged", "blocked", "approved", "verified", "promoted",
    "rejected", "expired",
)

#: The stage-vocabulary mapping (see the module docstring): each
#: anchor-path status, mapped to the claim-stage axis name whose
#: rank governs the transition rules for moves touching it.
ANCHOR_STAGE_MAP: dict[str, str] = {
    "staged": "created",
    "blocked": "created",
    "approved": "checked",
    "verified": "explained",
    "promoted": "accepted",
    "rejected": "created",
    "expired": "created",
}

#: Keys of one append-only review-history entry — the evidence
#: trail every transition appends. ``from_stage``/``to_stage`` are
#: the mapped claim-stage names (the mapping is part of the trail,
#: so a reader never has to re-derive it).
REVIEW_HISTORY_KEYS: tuple[str, ...] = (
    "from_status", "to_status", "from_stage", "to_stage",
    "actor", "timestamp", "evidence_refs", "reason",
)

#: Rank of ``checked`` — the ceiling for automated actors, exactly
#: as in ``claim_stage`` (the floor above which a named human is
#: required).
_CHECKED_RANK = STAGE_ORDER["checked"]

#: The anchor lifecycle's legal transitions: from_status → the set
#: of to_status values the service will effect. Anything outside
#: this table does not exist to attempt. The forward spine is
#: staged/blocked → approved → verified → promoted; rejection is
#: reachable from every live review state; re-stage returns an
#: approved or rejected record to the queue; expiry is the
#: lifecycle's move on a stale rejection; ``verified`` → ``verified``
#: is the archival bookkeeping of cleanup (status unchanged, the
#: move to the archive file is the act — see archive_anchor_record).
ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    "staged": frozenset({"approved", "rejected"}),
    "blocked": frozenset({"approved", "rejected"}),
    "approved": frozenset({"verified", "promoted", "rejected", "staged"}),
    "verified": frozenset({"promoted", "rejected", "staged", "verified"}),
    "rejected": frozenset({"staged", "expired"}),
    "promoted": frozenset(),
    "expired": frozenset(),
}


class AnchorTransitionError(ValueError):
    """An anchor-path transition was refused (fail-closed).

    Nothing was written: the record is unchanged and no trail entry
    was appended."""


def anchor_stage(status: str) -> str:
    """The claim-stage name an anchor-path status maps to."""
    try:
        return ANCHOR_STAGE_MAP[status]
    except KeyError:
        raise AnchorTransitionError(
            f"unknown anchor-path status: {status!r} "
            f"(expected one of {ANCHOR_STATUSES})") from None


def _status_of(record: dict[str, Any]) -> str:
    """The record's current anchor-path status.

    A record carrying no ``review_status`` stands as ``staged`` —
    the reading the anchor path's routes have always applied to a
    freshly staged record."""
    status = record.get("review_status") or "staged"
    if status not in ANCHOR_STAGE_MAP:
        raise AnchorTransitionError(
            f"record carries unknown review_status {status!r}; "
            "the transition service fails closed")
    return str(status)


def transition_anchor_status(
    record: dict[str, Any],
    to_status: str,
    *,
    actor: str,
    actor_kind: str | None = None,
    reason: str | None = None,
    evidence_refs: Iterable[str] | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Effect one anchor-path status transition on *record*.

    Mutates *record* in place (its ``review_status`` and its
    append-only ``review_history``) and returns the appended trail
    entry. Every rule is fail-closed; a refused transition changes
    nothing:

    * the (from, to) pair must exist in ``ALLOWED_TRANSITIONS`` —
      a transition outside the table does not exist to attempt;
    * a no-op move (to == from, other than cleanup's archival
      ``verified`` → ``verified`` bookkeeping) is refused;
    * backward moves on the mapped axis (demotions) and the
      terminal laterals (rejection, expiry) require a recorded
      ``reason``;
    * an automated actor (per the ``claim_stage`` rules) may effect
      only transitions whose mapped stages both sit at or below
      ``checked``;
    * a transition touching a mapped stage above ``checked``
      requires a named-human actor; advancing into a mapped stage
      above ``checked`` additionally requires a non-empty
      ``evidence_refs`` trail.
    """
    if to_status not in ANCHOR_STAGE_MAP:
        raise AnchorTransitionError(
            f"unknown anchor-path status: {to_status!r} "
            f"(expected one of {ANCHOR_STATUSES})")
    current = _status_of(record)
    history = record.get("review_history")
    if history is not None and not isinstance(history, list):
        raise AnchorTransitionError(
            "review_history is not a list — record is defective")

    actor_name = str(actor or "").strip()
    if not actor_name:
        raise AnchorTransitionError("actor is required")
    automated = is_automated_actor(actor_name, actor_kind=actor_kind)

    if to_status == current and current != "verified":
        raise AnchorTransitionError(
            f"no-op transition: already at status {current!r}")
    if to_status not in ALLOWED_TRANSITIONS[current]:
        raise AnchorTransitionError(
            f"illegal anchor-path transition {current!r} → "
            f"{to_status!r}: not a step of the anchor lifecycle")

    from_stage = validate_stage_value(anchor_stage(current))
    to_stage = validate_stage_value(anchor_stage(to_status))
    cur_rank = STAGE_ORDER[from_stage]  # type: ignore[index]
    tgt_rank = STAGE_ORDER[to_stage]  # type: ignore[index]
    backward = tgt_rank < cur_rank
    lateral = tgt_rank == cur_rank
    reason_text = str(reason or "").strip()
    if backward and not reason_text:
        raise AnchorTransitionError(
            "backward anchor-path transitions require a recorded "
            "reason (demotion record)")
    if lateral and current != to_status and not reason_text:
        # The terminal laterals — rejection and expiry — are the
        # lateral moves that change status; each is an auditable
        # act and carries its reason (the rejection's reason, the
        # expiry's archived_reason).
        raise AnchorTransitionError(
            f"the {current!r} → {to_status!r} transition requires "
            "a recorded reason")

    refs = [str(r) for r in (evidence_refs or []) if str(r).strip()]
    touches_above_checked = max(cur_rank, tgt_rank) > _CHECKED_RANK
    if automated and touches_above_checked:
        raise AnchorTransitionError(
            f"automated actor {actor_name!r} may write only "
            f"transitions at or below 'checked'; {current!r} → "
            f"{to_status!r} (mapped {from_stage!r} → {to_stage!r}) "
            "fails closed")
    if touches_above_checked:
        if automated or not is_named_human(actor_name,
                                           actor_kind=actor_kind):
            raise AnchorTransitionError(
                "transitions above 'checked' require a named-human "
                f"actor; {actor_name!r} does not validate as one")
        if tgt_rank > _CHECKED_RANK and not backward and not refs:
            # Advancing into explained/accepted must carry its
            # evidence trail. A demotion out of those stages
            # carries its recorded reason instead (required above).
            raise AnchorTransitionError(
                "transitions above 'checked' require evidence_refs "
                "(an inspectable trail)")

    ts = timestamp or datetime.now(UTC).isoformat()
    entry = {
        "from_status": current,
        "to_status": to_status,
        "from_stage": from_stage,
        "to_stage": to_stage,
        "actor": actor_name,
        "timestamp": ts,
        "evidence_refs": refs,
        "reason": reason_text,
    }
    new_history = list(history) if isinstance(history, list) else []
    new_history.append(entry)
    record["review_status"] = to_status
    record["review_history"] = new_history
    return entry


def archive_anchor_record(
    record: dict[str, Any],
    *,
    actor: str,
    actor_kind: str | None = None,
    reason: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Record a record's move to the archive file (status unchanged).

    Archival is a move between stores, not a status: the record
    keeps its ``review_status`` and gains ``archived_at`` /
    ``archived_reason``. It is nevertheless an act on the record,
    so it passes through this service: the service validates that
    the record stands in an archivable status, stamps the archive
    fields, and appends the trail entry (``from_status`` ==
    ``to_status``, reason naming the archival). The verify and
    expiry transitions that themselves archive are effected by
    :func:`transition_anchor_status` plus this function's stamping
    at their call sites, through :func:`stamp_archive_fields`.
    """
    current = _status_of(record)
    if current in ("staged", "blocked"):
        raise AnchorTransitionError(
            f"a {current!r} record is not archivable: it has not "
            "been through review")
    entry = stamp_archive_fields(
        record, actor=actor, actor_kind=actor_kind, reason=reason,
        timestamp=timestamp)
    return entry


def stamp_archive_fields(
    record: dict[str, Any],
    *,
    actor: str,
    actor_kind: str | None = None,
    reason: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Stamp ``archived_at``/``archived_reason`` and append the
    archival trail entry, without changing ``review_status``.

    The actor rules are the service's own: an automated actor may
    stamp only a record whose mapped stage sits at or below
    ``checked``; above it, a named human is required — the same
    ceiling, applied to the archival act.
    """
    current = _status_of(record)
    history = record.get("review_history")
    if history is not None and not isinstance(history, list):
        raise AnchorTransitionError(
            "review_history is not a list — record is defective")
    actor_name = str(actor or "").strip()
    if not actor_name:
        raise AnchorTransitionError("actor is required")
    reason_text = str(reason or "").strip()
    if not reason_text:
        raise AnchorTransitionError(
            "an archival requires a recorded reason (archived_reason)")
    automated = is_automated_actor(actor_name, actor_kind=actor_kind)
    stage = validate_stage_value(anchor_stage(current))
    rank = STAGE_ORDER[stage]  # type: ignore[index]
    if rank > _CHECKED_RANK:
        if automated or not is_named_human(actor_name,
                                           actor_kind=actor_kind):
            raise AnchorTransitionError(
                "archiving a record above 'checked' requires a "
                f"named-human actor; {actor_name!r} does not "
                "validate as one")
    # At or below 'checked', archival is bookkeeping the ceiling
    # admits for any actor, automated included (the lifecycle's
    # expiry archival sits at 'created' on both sides).
    ts = timestamp or datetime.now(UTC).isoformat()
    record["archived_at"] = ts
    record["archived_reason"] = reason_text
    entry = {
        "from_status": current,
        "to_status": current,
        "from_stage": stage,
        "to_stage": stage,
        "actor": actor_name,
        "timestamp": ts,
        "evidence_refs": [],
        "reason": reason_text,
    }
    new_history = list(history) if isinstance(history, list) else []
    new_history.append(entry)
    record["review_history"] = new_history
    return entry
