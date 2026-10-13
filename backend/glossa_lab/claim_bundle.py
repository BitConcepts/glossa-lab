"""Claim bundles and the Phase B stage gates — Spec 029 (FR-029-04…07).

Phase A built the stage axis and the transition core
(:mod:`glossa_lab.claim_stage`). This module builds what Phase A
explicitly deferred (see ``phase-a-record.md``): the bundle
representation, the attribution sub-claim template with the OD-3
contest cap, the explanation record that gates ``accepted``
(FR-029-06), and the digestion record that gates ``digested``
(FR-029-07 / OD-5) — each gate paired with discriminating controls
in ``backend/tests/test_spec029_phase_b.py`` (task B5, plan §2.4).

Governed rules implemented here, all from the frozen spec texts
(``tasks.md`` Phase B governs where summaries differ):

* **B1 — Bundle representation (FR-029-04; F029-C03, F029-C11).**
  A decipherment claim is a parent record plus sub-claim records
  of kinds ``reading_soundness``, ``scholarship_accounting``,
  ``attribution`` and ``explanation_intelligibility``. Each
  sub-claim is a first-class record: its own evidence list, its
  own falsification condition, and its own stage carried by the
  Phase A stage shape and moved only by the Phase A transition
  service (through this module's gate layer) — there is no
  parallel stage system. The parent's stage is **computed**:
  the minimum of the sub-claim stages, then the caps below. The
  stored parent stage is that computation's cache
  (``stage_source`` names the computation, plan §0) and is never
  directly assignable: :func:`glossa_lab.claim_stage.transition_stage`
  refuses a bundle parent, and so does the gate layer here.
* **B2 — Attribution as a claim (FR-029-05; F029-C05; OD-3).**
  The attribution sub-claim carries a template: prior readings
  with resolvable citations, and a completeness basis (a search
  record: corpora and literature searched, date, searcher). Its
  contest state is ``unexamined`` / ``uncontested`` /
  ``contested``. **Contested** — an active, evidenced dispute
  with no durable adjudication record resolving it — caps the
  parent at ``checked`` inside the parent-stage computation
  itself, not just in a display. **Unexamined** carries no cap;
  the bundle minimum rule alone applies. A contest resolved by a
  durable adjudication record lifts the cap.
* **B3 — Explanation record (FR-029-06; F029-C04; OD-2).** The
  ``accepted`` transition fails closed without a valid
  explanation record: one named accountable human author
  (internal or external; an AI system may be recorded as the
  drafter but may **never** be the named human — validation
  rejects AI / process actors), a resolvable artifact URI, the
  artifact's stored SHA-256 content hash, the venue where
  challenges are filed and answered, and an AI-assistance
  disclosure field.
* **B4 — Digestion record (FR-029-07; F029-C12; OD-5).** The
  ``digested`` transition fails closed without a valid digestion
  record in exactly one of the three OD-5 classes —
  ``independent_reuse``, ``published_challenge_answered``,
  ``mechanism_engaging_citation`` — each with resolvable
  references and a validated program-independence field
  (the engaging scholar is not a claim author and not program
  staff; the field is required, fail-closed, and cross-checked
  against any author / staff lists supplied). Class (iii)
  additionally requires a named intake reviewer with a stored
  rationale. **Adverse digestion**: an unanswered substantive
  refutation flags the claim ``contested``, blocks any advance
  above ``checked``, and pulls a claim (or bundle parent) back
  to at most ``checked`` by a recorded demotion.
* **Gate layer.** :func:`gated_transition_stage` is the Phase B
  transition path: it validates the gate records for the target
  stage, then delegates the write to the Phase A transition
  service. Validation runs on a trial copy — a refused
  transition writes nothing to the caller's record (the Phase A
  convention).

Scope boundary (hard limit of this phase): this module is
machinery only. It operates on records handed to it; no live
claim or anchor is promoted, decomposed, or given a real
explanation / digestion record by this phase — those are
lane-2 human acts for later work. Test fixtures are synthetic.
Nothing here reads or writes a lane-1 AEE score: bundle
machinery never touches score propagation (Phase A invariant).
"""

from __future__ import annotations

import copy
import re
from datetime import datetime, timezone
from typing import Any, Iterable

from glossa_lab.claim_stage import (
    STAGE_ORDER,
    StageTransitionError,
    is_automated_actor,
    is_named_human,
    serialize_stage,
    transition_stage,
    validate_stage_value,
    with_stage_defaults,
)

# ── Vocabulary ────────────────────────────────────────────────────────────

#: The four sub-claim kinds of a decipherment bundle (FR-029-04).
SUBCLAIM_KINDS: tuple[str, ...] = (
    "reading_soundness",
    "scholarship_accounting",
    "attribution",
    "explanation_intelligibility",
)

ATTRIBUTION_KIND = "attribution"
EXPLANATION_KIND = "explanation_intelligibility"

#: Contest states of the attribution sub-claim. ``unexamined`` is
#: the not-yet-assessed state OD-3 names: it carries no cap.
CONTEST_STATES: tuple[str, ...] = ("unexamined", "uncontested", "contested")

#: The OD-3 cap: while attribution is contested, the parent stage
#: may not exceed this stage.
CONTESTED_ATTRIBUTION_CAP = "checked"

#: The three qualifying digestion classes (OD-5).
DIGESTION_CLASSES: tuple[str, ...] = (
    "independent_reuse",
    "published_challenge_answered",
    "mechanism_engaging_citation",
)

#: Provenance written into a bundle parent's ``stage_source``: the
#: stored stage is this computation's cache (plan §0).
PARENT_STAGE_SOURCE = "bundle-minimum-computation:spec029-phase-b-v1"

_CHECKED_RANK = STAGE_ORDER["checked"]

_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")

#: Tokens that mark an actor name as an AI system. An AI system may
#: draft an account but may never be the named human (OD-2); these
#: are rejected in addition to the Phase A process tokens, and the
#: check fails closed.
_AI_TOKENS: frozenset[str] = frozenset({
    "ai", "assistant", "chatbot", "chatgpt", "claude", "codex", "copilot",
    "gemini", "gpt", "llm", "muse",
})


class BundleValidationError(ValueError):
    """A bundle, template, or gate record is invalid (fail-closed)."""


class BundleGateError(StageTransitionError):
    """A Phase B gate refused a stage transition. Nothing was written."""


# ── Small shared validators ───────────────────────────────────────────────

def is_resolvable_ref(ref: Any) -> bool:
    """True when *ref* is a resolvable citation reference.

    Resolvable, mechanically: a non-empty string carrying a URI
    scheme (``https://…``), a ``doi:`` prefix, or a bare DOI.
    A bare title or a name is not a resolvable citation.
    """
    if not isinstance(ref, str):
        return False
    text = ref.strip()
    if not text:
        return False
    lowered = text.lower()
    if "://" in text or lowered.startswith("doi:"):
        return True
    return bool(_DOI_RE.match(text))


def is_ai_actor(actor: Any) -> bool:
    """True when *actor* names an AI system (never a named human)."""
    name = str(actor or "").strip()
    if not name:
        return False
    if is_automated_actor(name):
        return True
    tokens = set(re.split(r"[^a-z0-9]+", name.lower()))
    return bool(tokens & _AI_TOKENS)


def is_accountable_human(actor: Any, *, actor_kind: str | None = None) -> bool:
    """True when *actor* validates as one named accountable human.

    The Phase A named-human rule, tightened for the OD-2 gates:
    AI-system names are rejected as well as process names.
    """
    if isinstance(actor, (list, tuple, set, dict)):
        return False  # the gate names ONE accountable human, not a group
    if actor_kind is not None and str(actor_kind).strip().lower() != "human":
        return False
    return is_named_human(str(actor or "")) and not is_ai_actor(actor)


def _require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def _raise_if_errors(errors: list[str], what: str) -> None:
    if errors:
        raise BundleValidationError(f"invalid {what}: " + "; ".join(errors))


# ── B1: sub-claim and bundle representation ───────────────────────────────

def make_subclaim(
    kind: str,
    subclaim_id: str,
    *,
    proposition: str,
    evidence: Iterable[Any] | None = None,
    falsification_condition: str,
    stage: str | None = None,
    stage_source: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Create one first-class sub-claim record (validated).

    The record carries the Phase A stage shape; when *stage* is
    given it is stamped with its provenance, otherwise the
    sub-claim is honestly unstamped (``stage=None``).
    """
    errors: list[str] = []
    _require(kind in SUBCLAIM_KINDS, errors, f"unknown sub-claim kind {kind!r}")
    _require(bool(str(subclaim_id or "").strip()), errors, "sub-claim id is required")
    _require(bool(str(proposition or "").strip()), errors, "proposition is required")
    _require(
        isinstance(falsification_condition, str) and bool(falsification_condition.strip()),
        errors, "falsification_condition is required (every sub-claim carries its own falsifier)",
    )
    ev = list(evidence) if evidence is not None else []
    _require(isinstance(ev, list), errors, "evidence must be a list")
    if stage is not None:
        try:
            validate_stage_value(stage)
        except ValueError as exc:
            errors.append(str(exc))
    _raise_if_errors(errors, "sub-claim")
    record = with_stage_defaults({
        "claim_id": str(subclaim_id),
        "kind": kind,
        "proposition": str(proposition),
        "evidence": ev,
        "falsification_condition": str(falsification_condition),
    })
    if stage is not None:
        record["stage"] = stage
        record["stage_source"] = stage_source or "claim-bundle:subclaim-record"
        record["stage_as_of"] = timestamp or datetime.now(timezone.utc).isoformat()
    return record


def validate_subclaim(record: Any) -> None:
    """Raise :class:`BundleValidationError` unless *record* is a
    well-formed sub-claim record (kind, evidence list, falsifier,
    and a valid-or-unstamped Phase A stage)."""
    errors: list[str] = []
    if not isinstance(record, dict):
        raise BundleValidationError("sub-claim record is not a mapping")
    _require(record.get("kind") in SUBCLAIM_KINDS, errors,
             f"unknown sub-claim kind {record.get('kind')!r}")
    _require(bool(str(record.get("claim_id") or "").strip()), errors, "claim_id is required")
    _require(isinstance(record.get("evidence"), list), errors,
             "evidence must be a list (present, possibly empty)")
    fc = record.get("falsification_condition")
    _require(isinstance(fc, str) and bool(fc.strip()), errors,
             "falsification_condition is required")
    try:
        validate_stage_value(record.get("stage"))
    except ValueError as exc:
        errors.append(str(exc))
    if record.get("kind") == ATTRIBUTION_KIND:
        state = record.get("contest_state", "unexamined")
        _require(state in CONTEST_STATES, errors, f"unknown contest_state {state!r}")
    _raise_if_errors(errors, f"sub-claim {record.get('claim_id')!r}")


def is_bundle(record: Any) -> bool:
    """True when *record* is a bundle parent (carries sub-claims)."""
    return (
        isinstance(record, dict)
        and isinstance(record.get("sub_claims"), list)
        and len(record["sub_claims"]) > 0
    )


def get_subclaim(parent: dict[str, Any], kind: str) -> dict[str, Any] | None:
    """The parent's sub-claim of *kind*, or ``None``."""
    for sub in parent.get("sub_claims") or []:
        if isinstance(sub, dict) and sub.get("kind") == kind:
            return sub
    return None


def make_bundle(
    parent: dict[str, Any],
    subclaims: Iterable[dict[str, Any]],
    *,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Attach *subclaims* to *parent* as a bundle and compute its stage.

    A bundle is exactly the four governed kinds, each once
    (FR-029-04). The sub-claim records are deep-copied onto the
    parent under ``sub_claims``; the parent's stage becomes the
    computed cache via :func:`sync_parent_stage`. Returns the
    parent record.
    """
    if not isinstance(parent, dict):
        raise BundleValidationError("bundle parent is not a mapping")
    subs = [copy.deepcopy(s) for s in subclaims]
    errors: list[str] = []
    kinds = [s.get("kind") if isinstance(s, dict) else None for s in subs]
    for kind in SUBCLAIM_KINDS:
        _require(kinds.count(kind) == 1, errors,
                 f"bundle requires exactly one {kind!r} sub-claim (found {kinds.count(kind)})")
    for extra in kinds:
        _require(extra in SUBCLAIM_KINDS, errors, f"unknown sub-claim kind {extra!r}")
    _raise_if_errors(errors, "bundle")
    for sub in subs:
        validate_subclaim(sub)
        if sub["kind"] == ATTRIBUTION_KIND:
            validate_attribution_subclaim(sub)
    parent["sub_claims"] = subs
    sync_parent_stage(parent, timestamp=timestamp)
    return parent


# ── B2: attribution template and the OD-3 cap ─────────────────────────────

def validate_attribution_subclaim(record: dict[str, Any]) -> None:
    """Validate the attribution template (FR-029-05 / task B2).

    * ``unexamined``: the template may be incomplete — the state
      itself is the honest record that accounting has not been
      assessed. No completeness requirement, and (OD-3) no cap.
    * ``uncontested`` / ``contested``: the template must be
      complete — prior readings each with a resolvable citation,
      and a completeness basis (search record naming the corpora
      and literature searched, the date, and the searcher).
    * ``contested`` additionally requires a contest record: who
      contests, on what (resolvable) evidence, and when. A
      resolution, when present, must be a durable adjudication
      record (resolvable reference, date, named human resolver).
    """
    errors: list[str] = []
    state = record.get("contest_state", "unexamined")
    if state not in CONTEST_STATES:
        raise BundleValidationError(f"unknown contest_state {state!r}")
    if state == "unexamined":
        return
    prior = record.get("prior_readings")
    _require(isinstance(prior, list) and len(prior) > 0, errors,
             "prior_readings must be a non-empty list")
    if isinstance(prior, list):
        for i, entry in enumerate(prior):
            citation = entry.get("citation") if isinstance(entry, dict) else entry
            _require(is_resolvable_ref(citation), errors,
                     f"prior_readings[{i}] lacks a resolvable citation")
    basis = record.get("search_record")
    _require(isinstance(basis, dict), errors, "search_record (completeness basis) is required")
    if isinstance(basis, dict):
        for key in ("corpora_searched", "literature_searched"):
            value = basis.get(key)
            _require(isinstance(value, list) and len(value) > 0, errors,
                     f"search_record.{key} must be a non-empty list")
        _require(bool(str(basis.get("searched_on") or "").strip()), errors,
                 "search_record.searched_on is required")
        _require(is_accountable_human(basis.get("searcher")), errors,
                 "search_record.searcher must be a named human")
    if state == "contested":
        contest = record.get("contest_record")
        _require(isinstance(contest, dict), errors,
                 "a contested attribution requires a contest_record")
        if isinstance(contest, dict):
            _require(bool(str(contest.get("contested_by") or "").strip()), errors,
                     "contest_record.contested_by is required")
            ev = contest.get("evidence")
            _require(isinstance(ev, list) and len(ev) > 0
                     and all(is_resolvable_ref(e) for e in ev), errors,
                     "contest_record.evidence must be a non-empty list of resolvable refs")
            _require(bool(str(contest.get("contested_on") or "").strip()), errors,
                     "contest_record.contested_on is required")
            resolution = contest.get("resolution")
            if resolution is not None:
                _require(isinstance(resolution, dict), errors,
                         "contest_record.resolution must be a mapping")
                if isinstance(resolution, dict):
                    _require(is_resolvable_ref(resolution.get("adjudication_ref")), errors,
                             "resolution requires a resolvable adjudication_ref "
                             "(a durable adjudication record)")
                    _require(bool(str(resolution.get("resolved_on") or "").strip()), errors,
                             "resolution.resolved_on is required")
                    _require(is_accountable_human(resolution.get("resolved_by")), errors,
                             "resolution.resolved_by must be a named human")
    _raise_if_errors(errors, "attribution sub-claim")


def make_attribution_subclaim(
    subclaim_id: str,
    *,
    proposition: str,
    evidence: Iterable[Any] | None = None,
    falsification_condition: str,
    prior_readings: Iterable[Any] | None = None,
    search_record: dict[str, Any] | None = None,
    contest_state: str = "unexamined",
    contest_record: dict[str, Any] | None = None,
    stage: str | None = None,
    stage_source: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Create the attribution sub-claim with its template fields."""
    record = make_subclaim(
        ATTRIBUTION_KIND, subclaim_id, proposition=proposition, evidence=evidence,
        falsification_condition=falsification_condition, stage=stage,
        stage_source=stage_source, timestamp=timestamp,
    )
    record["prior_readings"] = list(prior_readings) if prior_readings is not None else []
    record["search_record"] = copy.deepcopy(search_record)
    record["contest_state"] = contest_state
    if contest_record is not None:
        record["contest_record"] = copy.deepcopy(contest_record)
    validate_attribution_subclaim(record)
    return record


def contest_is_resolved(attribution: dict[str, Any]) -> bool:
    """True when a contested attribution carries a valid durable
    resolution (which lifts the OD-3 cap)."""
    if attribution.get("contest_state") != "contested":
        return False
    contest = attribution.get("contest_record")
    if not isinstance(contest, dict):
        return False
    resolution = contest.get("resolution")
    if not isinstance(resolution, dict):
        return False
    return (
        is_resolvable_ref(resolution.get("adjudication_ref"))
        and bool(str(resolution.get("resolved_on") or "").strip())
        and is_accountable_human(resolution.get("resolved_by"))
    )


def attribution_is_contested(attribution: dict[str, Any] | None) -> bool:
    """True when attribution is *actively* contested (OD-3): the
    contest state is ``contested`` and no durable adjudication
    record has resolved it. Unexamined is not contested."""
    if not isinstance(attribution, dict):
        return False
    if attribution.get("contest_state", "unexamined") != "contested":
        return False
    return not contest_is_resolved(attribution)


# ── B1 continued: the parent-stage computation ────────────────────────────

def has_unanswered_refutation(record: dict[str, Any]) -> bool:
    """True when the record carries an adverse-digestion record
    (unanswered substantive refutation)."""
    adverse = record.get("adverse_digestion") if isinstance(record, dict) else None
    return isinstance(adverse, dict) and not adverse.get("answered", False)


def compute_parent_stage_detail(parent: dict[str, Any]) -> dict[str, Any]:
    """The parent-stage computation, with its workings exposed.

    Stage = minimum of the sub-claim stages (F029-C11), then the
    caps: contested attribution caps at ``checked`` (OD-3), and an
    unanswered refutation caps at ``checked`` (adverse digestion,
    OD-5). An unstamped sub-claim makes the parent unstamped —
    the computation invents no stage the evidence does not carry.
    """
    if not is_bundle(parent):
        raise BundleValidationError("record is not a bundle parent (no sub_claims)")
    stages: dict[str, str | None] = {}
    for sub in parent["sub_claims"]:
        validate_subclaim(sub)
        stages[str(sub.get("kind"))] = sub.get("stage")
    unstamped = [k for k, s in stages.items() if s is None]
    minimum: str | None = None
    if not unstamped:
        minimum = min(stages.values(), key=lambda s: STAGE_ORDER[s])  # type: ignore[arg-type]
    caps: list[str] = []
    stage = minimum
    attribution = get_subclaim(parent, ATTRIBUTION_KIND)
    if attribution_is_contested(attribution):
        caps.append(f"od3-contested-attribution-caps-at-{CONTESTED_ATTRIBUTION_CAP}")
        if stage is not None and STAGE_ORDER[stage] > _CHECKED_RANK:
            stage = CONTESTED_ATTRIBUTION_CAP
    if has_unanswered_refutation(parent):
        caps.append(f"od5-adverse-digestion-caps-at-{CONTESTED_ATTRIBUTION_CAP}")
        if stage is not None and STAGE_ORDER[stage] > _CHECKED_RANK:
            stage = CONTESTED_ATTRIBUTION_CAP
    return {
        "stage": stage,
        "minimum_stage": minimum,
        "subclaim_stages": stages,
        "unstamped_subclaims": unstamped,
        "attribution_contested": attribution_is_contested(attribution),
        "caps_applied": caps,
    }


def compute_parent_stage(parent: dict[str, Any]) -> str | None:
    """The bundle parent's computed stage (``None`` if unstamped)."""
    return compute_parent_stage_detail(parent)["stage"]


def sync_parent_stage(
    parent: dict[str, Any],
    *,
    timestamp: str | None = None,
    reason: str | None = None,
) -> str | None:
    """Recompute the parent's stage and store it as the cache.

    Writes ``stage``, ``stage_source`` (the computation) and
    ``stage_as_of`` together (plan §0). When the computed stage
    changes, the change is appended to the parent's
    ``stage_history`` as a dated computation entry naming the
    sub-claim stages it derived from — a demotion produced by
    decomposition or by a cap is a recorded, publishable event,
    never a silent edit. This computation is the **only** writer
    of a bundle parent's stage.
    """
    detail = compute_parent_stage_detail(parent)
    computed = detail["stage"]
    ts = timestamp or datetime.now(timezone.utc).isoformat()
    previous = parent.get("stage")
    if previous is not None:
        validate_stage_value(previous)
    parent["stage"] = computed
    parent["stage_source"] = PARENT_STAGE_SOURCE
    parent["stage_as_of"] = ts
    history = parent.get("stage_history")
    if not isinstance(history, list):
        history = []
        parent["stage_history"] = history
    if previous != computed:
        history.append({
            "from_stage": previous,
            "to_stage": computed,
            "actor": "bundle-minimum-computation",
            "timestamp": ts,
            "evidence_refs": [
                str(sub.get("claim_id")) for sub in parent["sub_claims"]
            ],
            "reason": reason or (
                "parent stage recomputed as the minimum of sub-claim stages "
                f"{detail['subclaim_stages']}"
                + (f"; caps applied: {', '.join(detail['caps_applied'])}"
                   if detail["caps_applied"] else "")
            ),
        })
    parent["stage_computation"] = detail
    return computed


def serialize_bundle(parent: dict[str, Any]) -> dict[str, Any]:
    """Serialize a bundle for any surface that renders the parent.

    The contest travels with the parent (FR-029-05: a contested
    attribution renders wherever the parent renders): the
    serialized form carries ``attribution_contested``, the contest
    record itself, and the adverse-digestion state alongside the
    parent's stage object and each sub-claim's stage object.
    """
    if not is_bundle(parent):
        raise BundleValidationError("record is not a bundle parent (no sub_claims)")
    detail = compute_parent_stage_detail(parent)
    attribution = get_subclaim(parent, ATTRIBUTION_KIND) or {}
    subs = []
    for sub in parent["sub_claims"]:
        entry = {
            "claim_id": sub.get("claim_id"),
            "kind": sub.get("kind"),
            "proposition": sub.get("proposition"),
            "evidence": list(sub.get("evidence") or []),
            "falsification_condition": sub.get("falsification_condition"),
            "stage": serialize_stage(sub),
        }
        if sub.get("kind") == ATTRIBUTION_KIND:
            entry["contest_state"] = sub.get("contest_state", "unexamined")
            entry["attribution_contested"] = attribution_is_contested(sub)
            if sub.get("contest_record") is not None:
                entry["contest_record"] = copy.deepcopy(sub["contest_record"])
        subs.append(entry)
    return {
        "claim_id": parent.get("claim_id"),
        "stage": serialize_stage(parent),
        "stage_computation": detail,
        "sub_claims": subs,
        "attribution_contested": detail["attribution_contested"],
        "contest_record": copy.deepcopy(attribution.get("contest_record")),
        "contested": bool(detail["attribution_contested"]
                           or has_unanswered_refutation(parent)),
        "adverse_digestion": copy.deepcopy(parent.get("adverse_digestion")),
    }


# ── B3: the explanation record (gate for ``accepted``) ────────────────────

def validate_explanation_record(record: Any) -> None:
    """Validate an explanation record (FR-029-06; OD-2).

    Required: ``author`` — one named accountable human (an AI
    system recorded as ``drafter`` is permitted; as ``author``
    it is rejected); ``artifact_uri`` — resolvable; the artifact's
    stored content hash (``content_hash``, SHA-256 hex);
    ``challenge_venue`` — where challenges are filed and
    answered; ``ai_assistance_disclosure`` — the disclosure
    field, present and non-empty (constitution §VI).
    """
    errors: list[str] = []
    if not isinstance(record, dict):
        raise BundleValidationError("explanation record is not a mapping")
    author = record.get("author")
    _require(is_accountable_human(author, actor_kind=record.get("author_kind")), errors,
             "author must be one named accountable human — an AI system or process "
             "may draft but may never be the named human (OD-2)")
    _require(is_resolvable_ref(record.get("artifact_uri")), errors,
             "artifact_uri must be a resolvable reference to the durable account artifact")
    content_hash = record.get("content_hash") or record.get("artifact_hash")
    _require(isinstance(content_hash, str) and bool(_SHA256_RE.match(content_hash.strip())),
             errors, "content_hash must be the artifact's stored SHA-256 content hash")
    _require(bool(str(record.get("challenge_venue") or "").strip()), errors,
             "challenge_venue is required (where challenges are filed and answered)")
    disclosure = record.get("ai_assistance_disclosure")
    _require(isinstance(disclosure, str) and bool(disclosure.strip()), errors,
             "ai_assistance_disclosure is required (constitution §VI)")
    _raise_if_errors(errors, "explanation record")


def is_valid_explanation_record(record: Any) -> bool:
    try:
        validate_explanation_record(record)
    except BundleValidationError:
        return False
    return True


# ── B4: the digestion record (gate for ``digested``) and adverse digestion ─

def validate_digestion_record(
    record: Any,
    *,
    claim_authors: Iterable[str] = (),
    program_staff: Iterable[str] = (),
) -> None:
    """Validate a digestion record (FR-029-07; OD-5).

    Required on every class: ``digestion_class`` (one of the three
    OD-5 classes); ``independent_scholar`` — a named human;
    the program-independence fields ``scholar_is_claim_author``
    and ``scholar_is_program_staff``, each explicitly ``False``
    (missing is a failure, fail-closed), cross-checked against
    any supplied author / staff lists; and ``references`` — a
    non-empty list of resolvable references. Class-specific:
    ``independent_reuse`` requires ``reuse_reference``;
    ``published_challenge_answered`` requires both
    ``challenge_reference`` and a durable ``response_reference``;
    ``mechanism_engaging_citation`` requires a named
    ``intake_reviewer`` (a named human) with a stored
    ``intake_rationale``.
    """
    errors: list[str] = []
    if not isinstance(record, dict):
        raise BundleValidationError("digestion record is not a mapping")
    cls = record.get("digestion_class")
    _require(cls in DIGESTION_CLASSES, errors,
             f"digestion_class must be one of {DIGESTION_CLASSES}")
    scholar = record.get("independent_scholar")
    _require(is_accountable_human(scholar), errors,
             "independent_scholar must be a named human")
    _require(record.get("scholar_is_claim_author") is False, errors,
             "scholar_is_claim_author must be explicitly False "
             "(program-independence field, validated fail-closed)")
    _require(record.get("scholar_is_program_staff") is False, errors,
             "scholar_is_program_staff must be explicitly False "
             "(program-independence field, validated fail-closed)")
    if isinstance(scholar, str):
        lowered = scholar.strip().lower()
        _require(lowered not in {str(a).strip().lower() for a in claim_authors}, errors,
                 "independent_scholar is a claim author — not program-independent")
        _require(lowered not in {str(s).strip().lower() for s in program_staff}, errors,
                 "independent_scholar is program staff — not program-independent")
    refs = record.get("references")
    _require(isinstance(refs, list) and len(refs) > 0
             and all(is_resolvable_ref(r) for r in refs), errors,
             "references must be a non-empty list of resolvable references")
    if cls == "independent_reuse":
        _require(is_resolvable_ref(record.get("reuse_reference")), errors,
                 "independent_reuse requires a resolvable reuse_reference")
    elif cls == "published_challenge_answered":
        _require(is_resolvable_ref(record.get("challenge_reference")), errors,
                 "published_challenge_answered requires a resolvable challenge_reference")
        _require(is_resolvable_ref(record.get("response_reference")), errors,
                 "published_challenge_answered requires a durable response_reference "
                 "(the answer, in a durable record)")
    elif cls == "mechanism_engaging_citation":
        _require(is_accountable_human(record.get("intake_reviewer")), errors,
                 "mechanism_engaging_citation requires a named intake_reviewer")
        _require(bool(str(record.get("intake_rationale") or "").strip()), errors,
                 "mechanism_engaging_citation requires the intake reviewer's "
                 "stored intake_rationale")
    _raise_if_errors(errors, "digestion record")


def is_valid_digestion_record(
    record: Any,
    *,
    claim_authors: Iterable[str] = (),
    program_staff: Iterable[str] = (),
) -> bool:
    try:
        validate_digestion_record(
            record, claim_authors=claim_authors, program_staff=program_staff)
    except BundleValidationError:
        return False
    return True


def make_adverse_digestion_record(
    *,
    refuted_by: str,
    reference: str,
    recorded_on: str,
    summary: str = "",
) -> dict[str, Any]:
    """An adverse-digestion record: a substantive refutation that
    stands unanswered (OD-5)."""
    errors: list[str] = []
    _require(is_accountable_human(refuted_by), errors,
             "refuted_by must be a named human scholar")
    _require(is_resolvable_ref(reference), errors,
             "reference must be a resolvable reference to the refutation")
    _require(bool(str(recorded_on or "").strip()), errors, "recorded_on is required")
    _raise_if_errors(errors, "adverse digestion record")
    return {
        "kind": "adverse_digestion",
        "refuted_by": str(refuted_by),
        "reference": str(reference),
        "recorded_on": str(recorded_on),
        "summary": str(summary or ""),
        "answered": False,
    }


def record_adverse_digestion(
    record: dict[str, Any],
    adverse: dict[str, Any],
    *,
    actor: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Record an unanswered refutation on a claim or bundle parent.

    Flags the record ``contested`` and pulls it back to at most
    ``checked``: for a bundle parent the pullback is the parent
    computation's adverse cap, recorded by
    :func:`sync_parent_stage`; for a plain claim above ``checked``
    it is a recorded demotion transition through the Phase A
    service (named-human actor, recorded reason). Works on a
    trial copy — a refusal writes nothing. Returns the record.
    """
    errors: list[str] = []
    if not isinstance(adverse, dict) or adverse.get("kind") != "adverse_digestion":
        errors.append("adverse must be an adverse-digestion record "
                      "(see make_adverse_digestion_record)")
    elif adverse.get("answered"):
        errors.append("an answered refutation is not adverse digestion")
    else:
        _require(is_accountable_human(adverse.get("refuted_by")), errors,
                 "adverse record's refuted_by must be a named human")
        _require(is_resolvable_ref(adverse.get("reference")), errors,
                 "adverse record's reference must be resolvable")
    _raise_if_errors(errors, "adverse digestion")
    trial = copy.deepcopy(record)
    trial["adverse_digestion"] = copy.deepcopy(adverse)
    trial["contested"] = True
    ts = timestamp or datetime.now(timezone.utc).isoformat()
    if is_bundle(trial):
        sync_parent_stage(
            trial, timestamp=ts,
            reason=(f"adverse digestion: unanswered refutation by "
                    f"{adverse.get('refuted_by')} ({adverse.get('reference')}); "
                    "parent pulled back under the bundle rule (OD-5)"),
        )
    else:
        current = trial.get("stage")
        if current is not None and STAGE_ORDER[current] > _CHECKED_RANK:
            transition_stage(
                trial, CONTESTED_ATTRIBUTION_CAP, actor=actor,
                reason=(f"adverse digestion: unanswered refutation by "
                        f"{adverse.get('refuted_by')} ({adverse.get('reference')})"),
                evidence_refs=[str(adverse.get("reference"))],
                timestamp=ts,
            )
    record.clear()
    record.update(trial)
    return record


def answer_adverse_digestion(
    record: dict[str, Any],
    *,
    response_reference: str,
    answered_by: str,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Record a durable answer to an adverse refutation.

    Marks the adverse record answered (with the resolvable
    response reference and the named human who answered) and
    clears the record's adverse ``contested`` flag. A bundle
    parent's stage is then recomputed; whether the answered
    exchange itself qualifies the claim for ``digested`` is a
    separate digestion record (class
    ``published_challenge_answered``) judged at that gate.
    """
    if not has_unanswered_refutation(record):
        raise BundleValidationError("no unanswered refutation on this record to answer")
    if not is_resolvable_ref(response_reference):
        raise BundleValidationError("response_reference must be resolvable (a durable record)")
    if not is_accountable_human(answered_by):
        raise BundleValidationError("answered_by must be a named human")
    adverse = record["adverse_digestion"]
    adverse["answered"] = True
    adverse["response_reference"] = str(response_reference)
    adverse["answered_by"] = str(answered_by)
    adverse["answered_on"] = timestamp or datetime.now(timezone.utc).isoformat()
    if not (is_bundle(record) and attribution_is_contested(get_subclaim(record, ATTRIBUTION_KIND))):
        record["contested"] = False
    if is_bundle(record):
        sync_parent_stage(record, timestamp=timestamp)
    return record


# ── The gate layer: transition path for stages above ``checked`` ──────────

def gated_transition_stage(
    record: dict[str, Any],
    to_stage: str,
    *,
    actor: str,
    actor_kind: str | None = None,
    reason: str | None = None,
    evidence_refs: Iterable[str] | None = None,
    timestamp: str | None = None,
    explanation_record: dict[str, Any] | None = None,
    digestion_record: dict[str, Any] | None = None,
    claim_authors: Iterable[str] = (),
    program_staff: Iterable[str] = (),
) -> dict[str, Any]:
    """Apply one stage transition through the Phase B gates.

    The Phase A transition service remains the single writer; this
    layer validates the Phase B gate records first and delegates:

    * a **bundle parent** refuses every direct transition — its
      stage is computed (:func:`sync_parent_stage`), never
      assigned;
    * an advance above ``checked`` is refused while an
      unanswered refutation stands on the record (adverse
      digestion, OD-5);
    * ``accepted`` requires a valid explanation record
      (FR-029-06) — supplied here or already carried on the
      record; a supplied record is stored on the record only
      when the transition succeeds;
    * ``digested`` requires a valid digestion record
      (FR-029-07 / OD-5), validated against the supplied
      claim-author / program-staff lists (falling back to any
      ``claim_authors`` / ``program_staff`` lists the record
      itself carries), and the explanation record the
      ``accepted`` gate required must still validate.

    Everything runs on a trial copy first: a refused transition
    writes nothing. Returns the appended history entry.
    """
    if is_bundle(record):
        raise BundleGateError(
            "a bundle parent's stage is computed as the minimum of its "
            "sub-claim stages (sync_parent_stage); direct assignment is refused"
        )
    trial = copy.deepcopy(record)
    try:
        target = validate_stage_value(to_stage)
    except ValueError as exc:
        raise BundleGateError(str(exc)) from exc
    if target is None:
        raise BundleGateError("to_stage is required")
    target_rank = STAGE_ORDER[target]
    current = trial.get("stage")
    current_rank = STAGE_ORDER[current] if current is not None else -1
    advancing = target_rank > current_rank

    if advancing and target_rank > _CHECKED_RANK and has_unanswered_refutation(trial):
        raise BundleGateError(
            "adverse digestion: an unanswered refutation stands on this record; "
            "no advance above 'checked' until it is answered in a durable record (OD-5)"
        )

    if target == "accepted" and advancing:
        effective = explanation_record if explanation_record is not None \
            else trial.get("explanation_record")
        try:
            validate_explanation_record(effective)
        except BundleValidationError as exc:
            raise BundleGateError(
                f"the 'accepted' transition requires a valid explanation record "
                f"(FR-029-06): {exc}"
            ) from exc
        if explanation_record is not None:
            trial["explanation_record"] = copy.deepcopy(explanation_record)

    if target == "digested" and advancing:
        authors = list(claim_authors) or list(trial.get("claim_authors") or [])
        staff = list(program_staff) or list(trial.get("program_staff") or [])
        effective_digestion = digestion_record if digestion_record is not None \
            else trial.get("digestion_record")
        try:
            validate_digestion_record(
                effective_digestion, claim_authors=authors, program_staff=staff)
        except BundleValidationError as exc:
            raise BundleGateError(
                f"the 'digested' transition requires a valid digestion record "
                f"evidencing independent scholarly engagement (FR-029-07 / OD-5): {exc}"
            ) from exc
        effective_explanation = explanation_record if explanation_record is not None \
            else trial.get("explanation_record")
        try:
            validate_explanation_record(effective_explanation)
        except BundleValidationError as exc:
            raise BundleGateError(
                f"the 'digested' transition requires the explanation record the "
                f"'accepted' gate required to still validate (FR-029-06): {exc}"
            ) from exc
        if explanation_record is not None:
            trial["explanation_record"] = copy.deepcopy(explanation_record)
        if digestion_record is not None:
            trial["digestion_record"] = copy.deepcopy(digestion_record)

    entry = transition_stage(
        trial, target, actor=actor, actor_kind=actor_kind, reason=reason,
        evidence_refs=evidence_refs, timestamp=timestamp,
    )
    record.clear()
    record.update(trial)
    return entry
