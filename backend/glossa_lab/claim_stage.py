"""Claim lifecycle stage axis — Spec 029 Phase A core (FR-029-01…03).

This module is the single home of the lane-2 lifecycle vocabulary and
the machinery Phase A builds on it:

* the stage axis itself — Tao's five stage names verbatim (OD-4):
  ``created → checked → explained → accepted → digested``;
* the additive record shape (plan §2.1): ``stage``, ``stage_source``,
  ``stage_as_of`` and the append-only ``stage_history`` list, carried
  by extracted-claim records and by anchor records alike;
* the stage invariant (plan §0): a stored stage is a cache with
  provenance, never an assertion — every stage this module writes or
  serializes carries its ``stage_source`` and ``stage_as_of`` with it,
  and a record that has not been stamped (the state of every live
  record until the Phase D migration) serializes with ``stage=None``:
  an unstamped stage is never silently invented here;
* the transition service (:func:`transition_stage`) — the single
  writer of stage changes (FR-029-02);
* the ``verified_unexplained`` risk flag (FR-029-03).

Lane discipline (spec §3.3): stage is a lane-2 axis. It is never
folded into a lane-1 verdict, an AEE ``ClaimStatus``, a score, a band,
or a confidence tier, and nothing in this module reads those lane-1
values except the risk-flag computation, whose whole point is to name
the combination of a strong lane-1 state with a low lane-2 stage.

Scope boundary (Phase A): the explanation-record and digestion-record
gates for transitions above ``checked`` (FR-029-06/07) are Phase B
machinery. This service enforces the Phase A rules — one-step-forward
legality, reasoned demotion, the automated-actor allowlist, and the
named-human requirement above ``checked``, including a non-empty
evidence trail for those transitions — and fails closed on each.

Phase B extension (additive, 2026-10-12): the gate records live in
:mod:`glossa_lab.claim_bundle`, whose gate layer delegates the write
to this service. One Phase B shape is refused here directly: a
record carrying ``sub_claims`` is a bundle parent, and a bundle
parent's stage is computed as the minimum of its sub-claim stages
(F029-C11) — never directly assignable through this service. No
record shape that existed in Phase A carries ``sub_claims``, so no
Phase A behaviour changes.
"""

from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Any, Iterable

# ── Stage vocabulary (OD-4: Tao's names verbatim) ─────────────────────────

STAGES: tuple[str, ...] = ("created", "checked", "explained", "accepted", "digested")
STAGE_ORDER: dict[str, int] = {name: i for i, name in enumerate(STAGES)}

#: The additive stage fields, in record order (plan §2.1 / task A1).
STAGE_FIELDS: tuple[str, ...] = ("stage", "stage_source", "stage_as_of", "stage_history")

#: Keys of one append-only stage-history entry (task A1).
STAGE_HISTORY_KEYS: tuple[str, ...] = (
    "from_stage", "to_stage", "actor", "timestamp", "evidence_refs", "reason",
)

# ── Actor rules (FR-029-02) ───────────────────────────────────────────────

#: Automated actors, allowlisted to ``created``/``checked`` transitions
#: only. Names are matched in normalized form (see ``_normalize_actor``):
#: case-folded, with spaces / hyphens folded to underscores.
AUTOMATED_ACTORS: frozenset[str] = frozenset({
    "extraction",
    "claim_extraction",
    "indus_claims_extraction",
    "scoring",
    "aee_scoring",
    "research_loop",
    "batch",
    "batch_job",
})

#: Tokens that mark an actor name as a process, never a named human.
#: An actor whose normalized name is in ``AUTOMATED_ACTORS``, equals one
#: of these tokens, or contains one as a whole token is a process name
#: and can never validate as a named human (fail-closed).
_PROCESS_TOKENS: frozenset[str] = frozenset({
    "aee", "automated", "automation", "batch", "bot", "cron", "daemon",
    "evaluator", "extraction", "glossa", "intake", "job", "jobs", "loop",
    "migration", "pipeline", "research", "scheduler", "scoring",
    "script", "service", "system", "worker",
})

#: Rank of ``checked`` — the ceiling for automated actors and the floor
#: above which a named human is required.
_CHECKED_RANK = STAGE_ORDER["checked"]
#: Rank of ``explained`` — the risk flag fires below this stage.
_EXPLAINED_RANK = STAGE_ORDER["explained"]


class StageTransitionError(ValueError):
    """A stage transition was refused (fail-closed). Nothing was written."""


def _normalize_actor(actor: str) -> str:
    return "_".join(str(actor or "").strip().lower().replace("-", " ").split()).replace(" ", "_")


def is_automated_actor(actor: str, *, actor_kind: str | None = None) -> bool:
    """True when *actor* is an automated process actor.

    An explicit ``actor_kind="automated"`` always counts; otherwise the
    actor is automated when its normalized name is allowlisted in
    ``AUTOMATED_ACTORS`` or is / contains a process token.
    """
    if actor_kind is not None:
        return actor_kind.strip().lower() == "automated"
    norm = _normalize_actor(actor)
    if not norm:
        return False
    if norm in AUTOMATED_ACTORS:
        return True
    tokens = set(norm.split("_"))
    return bool(tokens & _PROCESS_TOKENS)


def is_named_human(actor: str, *, actor_kind: str | None = None) -> bool:
    """True when *actor* validates as a named human (fail-closed).

    A process name never validates: automated/process actors (by
    allowlist, process token, or an explicit non-human ``actor_kind``)
    are rejected, as are empty names and names with no letters.
    """
    if actor_kind is not None and actor_kind.strip().lower() != "human":
        return False
    name = str(actor or "").strip()
    if not name or not any(ch.isalpha() for ch in name):
        return False
    return not is_automated_actor(name)


# ── Record shape (A1) ─────────────────────────────────────────────────────

def stage_defaults() -> dict[str, Any]:
    """The additive stage shape with unstamped defaults.

    ``stage``/``stage_source``/``stage_as_of`` are ``None`` — unstamped,
    never invented — and ``stage_history`` is an empty list.
    """
    return {"stage": None, "stage_source": None, "stage_as_of": None, "stage_history": []}


def with_stage_defaults(record: dict[str, Any]) -> dict[str, Any]:
    """A copy of *record* with any missing stage keys present as defaults.

    Existing values are carried verbatim (append-only discipline: no
    existing field changes meaning, and a stamped value is never
    overwritten by a default).
    """
    out = dict(record)
    for key, default in stage_defaults().items():
        if key not in out:
            out[key] = copy.deepcopy(default)
    if not isinstance(out.get("stage_history"), list):
        out["stage_history"] = []
    return out


def validate_stage_value(stage: Any) -> str | None:
    """Return *stage* if it is a valid stage name (or ``None``), else raise."""
    if stage is None:
        return None
    if not isinstance(stage, str) or stage not in STAGE_ORDER:
        raise ValueError(f"unknown lifecycle stage: {stage!r} (expected one of {STAGES})")
    return stage


def serialize_stage(record: dict[str, Any]) -> dict[str, Any]:
    """Serialize a record's lane-2 stage as one distinct object.

    Carries the stage with its provenance (``stage_source`` /
    ``stage_as_of``, plan §0) and a history summary: the full
    append-only history, its length, and the latest transition. An
    unstamped record serializes honestly: ``stage`` is ``None`` and
    ``stamped`` is ``False``.
    """
    stage = record.get("stage")
    if stage is not None:
        validate_stage_value(stage)
    history = record.get("stage_history")
    entries = [dict(e) for e in history if isinstance(e, dict)] if isinstance(history, list) else []
    return {
        "stage": stage,
        "stage_source": record.get("stage_source"),
        "stage_as_of": record.get("stage_as_of"),
        "stamped": stage is not None,
        "stage_history": entries,
        "stage_history_count": len(entries),
        "latest_transition": entries[-1] if entries else None,
    }


# ── Risk flag (FR-029-03 / A5) ────────────────────────────────────────────

#: Lane-1 claim statuses in the SUPPORTED class: the program's own
#: supported / strongly_supported verdicts and their partial form —
#: exactly the supported-class shapes the retroactive audit flagged
#: (8 extracted-claim records, all AEE band ``high``, staged ``checked``).
SUPPORTED_CLASS_STATUSES: frozenset[str] = frozenset({
    "supported", "strongly_supported", "partially_supported",
})

#: Program verdict vocabulary (lane 1) in its SUPPORTED class.
SUPPORTED_CLASS_VERDICTS: frozenset[str] = frozenset({"supported"})

#: The high AEE score band (``aee`` ConfidenceBand ``high``).
HIGH_BAND = "high"


def stage_below_explained(stage: Any) -> bool:
    """True when *stage* sits below ``explained``.

    An unstamped stage (``None``) is below ``explained``: the record
    carries no evidence of having reached it. That is a statement
    about the evidence on the record, not an invented stage value.
    """
    if stage is None:
        return True
    return STAGE_ORDER[validate_stage_value(stage)] < _EXPLAINED_RANK  # type: ignore[index]


def is_supported_class(*, status: Any = None, verdict: Any = None) -> bool:
    """True when a lane-1 status/verdict is in the SUPPORTED class."""
    s = str(status or "").strip().lower()
    v = str(verdict or "").strip().lower()
    return s in SUPPORTED_CLASS_STATUSES or v in SUPPORTED_CLASS_VERDICTS


def compute_verified_unexplained(
    record: dict[str, Any],
    *,
    score: dict[str, Any] | None = None,
    status: Any = None,
    verdict: Any = None,
    band: Any = None,
) -> bool:
    """The FR-029-03 risk flag for one record.

    True exactly when the record's lane-1 state includes a
    SUPPORTED-class verdict/status or a high score band **while** its
    stage is below ``explained``.

    Lane-1 inputs are read, in order, from the explicit arguments,
    from *score* (an AEE ``ClaimScore`` dict: its ``band``), and from
    the record itself (``claim_status`` / ``verdict`` / ``band``
    fields when present). The record's confidence tier is *not* a
    lane-1 verdict or band and never fires this flag on its own.

    A record may also carry a **ledger-stamped** flag state: the
    Spec 029 Phase D migration stamps ``verified_unexplained``
    (from the frozen reclassification ledger — for anchors, the
    Phase-108/109 strict-set derivation the audit used, which no
    field a record itself carries can recompute) onto the record.
    A stamped ``True`` fires the flag while the stage is below
    ``explained``; it is OR-ed with the computed rule above, never
    a replacement for it.
    """
    if record.get("verified_unexplained") is True:
        return stage_below_explained(record.get("stage"))
    eff_status = status if status is not None else record.get("claim_status")
    eff_verdict = verdict if verdict is not None else record.get("verdict")
    eff_band = band
    if eff_band is None and isinstance(score, dict):
        eff_band = score.get("band")
    if eff_band is None:
        eff_band = record.get("band")
    high_band = str(eff_band or "").strip().lower() == HIGH_BAND
    if not (is_supported_class(status=eff_status, verdict=eff_verdict) or high_band):
        return False
    return stage_below_explained(record.get("stage"))


# ── Transition service (FR-029-02 / A3) ──────────────────────────────────

def transition_stage(
    record: dict[str, Any],
    to_stage: str,
    *,
    actor: str,
    actor_kind: str | None = None,
    reason: str | None = None,
    evidence_refs: Iterable[str] | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Apply one stage transition to *record* — the single stage writer.

    Mutates *record* in place and returns the appended history entry.
    Rules (all fail-closed; a refused transition writes nothing):

    * forward moves go exactly one step along
      ``created → checked → explained → accepted → digested`` (an
      unstamped record's first transition is to ``created``);
    * backward moves go to any earlier stage and require a recorded
      ``reason`` (demotion is a normal, publishable event);
    * automated actors are allowlisted to ``created``/``checked``
      transitions only — any automated attempt at or above
      ``explained``, on either side of the move, fails closed;
    * any transition touching a stage above ``checked`` requires a
      named-human actor (a process name never validates) and a
      non-empty ``evidence_refs`` trail;
    * every successful write updates ``stage``, ``stage_source`` (the
      transition-service history entry) and ``stage_as_of`` together,
      and appends the ``stage_history`` entry;
    * a bundle parent (a record carrying ``sub_claims``, Phase B)
      refuses every direct transition: its stage is computed, never
      assigned (F029-C11).
    """
    try:
        target = validate_stage_value(to_stage)
        current = record.get("stage")
        if current is not None:
            validate_stage_value(current)
    except ValueError as exc:
        raise StageTransitionError(str(exc)) from exc
    if target is None:
        raise StageTransitionError("to_stage is required")
    sub_claims = record.get("sub_claims")
    if isinstance(sub_claims, list) and sub_claims:
        raise StageTransitionError(
            "a bundle parent's stage is computed as the minimum of its "
            "sub-claim stages (claim_bundle.sync_parent_stage); "
            "direct assignment is refused"
        )
    history = record.get("stage_history")
    if history is not None and not isinstance(history, list):
        raise StageTransitionError("stage_history is not a list — record is defective")

    actor_name = str(actor or "").strip()
    if not actor_name:
        raise StageTransitionError("actor is required")
    automated = is_automated_actor(actor_name, actor_kind=actor_kind)

    cur_rank = STAGE_ORDER[current] if current is not None else -1
    tgt_rank = STAGE_ORDER[target]
    if tgt_rank == cur_rank:
        raise StageTransitionError(f"no-op transition: already at stage {target!r}")
    backward = tgt_rank < cur_rank
    if backward:
        if not str(reason or "").strip():
            raise StageTransitionError(
                "backward stage transitions require a recorded reason (demotion record)"
            )
    elif tgt_rank - cur_rank != 1:
        raise StageTransitionError(
            f"illegal forward transition {current!r} → {target!r}: "
            "forward moves go exactly one step"
        )

    refs = [str(r) for r in (evidence_refs or []) if str(r).strip()]
    touches_above_checked = max(cur_rank, tgt_rank) > _CHECKED_RANK
    if automated and (tgt_rank > _CHECKED_RANK or cur_rank > _CHECKED_RANK):
        raise StageTransitionError(
            f"automated actor {actor_name!r} may write only created/checked transitions; "
            f"{current!r} → {target!r} fails closed"
        )
    if touches_above_checked:
        if automated or not is_named_human(actor_name, actor_kind=actor_kind):
            raise StageTransitionError(
                f"transitions above 'checked' require a named-human actor; "
                f"{actor_name!r} does not validate as one"
            )
        if tgt_rank > _CHECKED_RANK and not refs:
            # Advancing into explained/accepted/digested must carry its
            # evidence trail. A demotion out of those stages carries
            # its recorded reason instead (required above).
            raise StageTransitionError(
                "transitions above 'checked' require evidence_refs (an inspectable trail)"
            )

    ts = timestamp or datetime.now(timezone.utc).isoformat()
    entry = {
        "from_stage": current,
        "to_stage": target,
        "actor": actor_name,
        "timestamp": ts,
        "evidence_refs": refs,
        "reason": str(reason or ""),
    }
    new_history = list(history) if isinstance(history, list) else []
    new_history.append(entry)
    record["stage"] = target
    record["stage_source"] = f"transition-service:stage_history[{len(new_history) - 1}]"
    record["stage_as_of"] = ts
    record["stage_history"] = new_history
    return entry
