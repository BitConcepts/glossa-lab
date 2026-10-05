"""AEE core adapter — Glossa claims on the Applied Epistemic Engineering library.

Glossa's core claim scoring runs on the same epistemic library the
project's spec-kit AEE extension is built on: ``applied-epistemic-engineering``
(the ``aee`` package, >=1.0.4). This module is the single mapping layer
between Glossa's extracted-claims JSON and AEE's typed model:

    glossa-indus/claims/extracted_claims/*.json   (per-document records)
        {"claims": [{claim_id, normalized_claim, claim_type, claim_status,
                     falsification_condition, glossa_lab_evidence,
                     contradicting_evidence, confidence_in_source, ...}]}
            │
            ▼  claim_from_glossa()
    aee.model.Claim / aee.model.Evidence  →  aee.graph.ClaimGraph
            │
            ▼  score_claims()
    aee.scoring.ScoringEngine  →  dict[str, aee.scoring.ClaimScore]

Mapping decisions (verified against aee 1.0.4, ``aee/model.py``):

* ``falsification_condition`` maps NATIVELY onto
  ``Claim.falsification_tests`` (a ``list[str]``) — AEE's scoring engine
  gives falsifiability credit for a non-empty list, which is exactly
  Glossa's "a claim without a stated way to be wrong is not a Glossa
  claim" rule (constitution §IV).
* ``claim_status`` maps onto ``ClaimStatus`` where AEE has the concept
  (``partially_supported`` → PARTIALLY_SUPPORTED, ``supported`` /
  ``strongly_supported`` → SUPPORTED, ``contradicted`` → CONTRADICTED).
  AEE has no UNTESTED status; Glossa's ``untested`` maps to DRAFT (not
  yet assessed) and the original string is preserved verbatim in
  ``Claim.metadata["glossa_claim_status"]``.
* The ScoringEngine takes no status input — it scores evidence only.
  Glossa's assessed status therefore enters scoring through the
  *evidence the adapter attaches*, which is where it epistemically
  belongs:
    - the source paper's assertion of the claim → ASSERTED evidence,
      SourceQuality.SECONDARY, direction SUPPORTS;
    - ``glossa_lab_evidence`` (Glossa's own phase-test results) →
      SourceQuality.TEST evidence, direction SUPPORTS, kind OBSERVED
      when the text carries a ``[VERIFIED]`` marker, INFERRED
      otherwise; for a claim Glossa marks ``contradicted`` that same
      material is attached as CONTRADICTS instead;
    - each ``contradicting_evidence`` string → OBSERVED / TEST evidence,
      direction CONTRADICTS.
  Consequence: a supported claim with verified Glossa test evidence
  scores strictly higher than an untested claim carrying only its
  source's assertion, and a contradicted claim is pulled down by the
  engine's contradiction penalty.
* ``confidence_in_source`` is NOT claim confidence. It is preserved in
  metadata and used only as the adapter's initial ``Claim.confidence``
  placeholder; ``ScoringEngine.score()`` overwrites ``Claim.confidence``
  with the propagated AEE score (that is the engine's documented
  contract), so after scoring, ``confidence`` means the AEE score.
* Fields AEE has no native concept for — ``claim_type`` (Glossa's
  taxonomy is finer than ``ClaimKind``), ``testability``,
  ``quote_fragment``, ``signs_involved`` / ``sign_ids``,
  ``proposed_value`` / ``proposed_language``, ``author``,
  ``extracted_at``, and the source file — are preserved in
  ``Claim.metadata`` (a native ``dict[str, Any]``) and in
  ``Claim.source_ref`` (the source document id). ``testability`` is
  additionally surfaced in ``Claim.boundary`` as
  ``testability=<value>`` so the engine's boundary component reflects
  that the claim declared how it could be tested.
* ``claim_type`` → ``ClaimKind``: ``statistical_claim`` → INFERENCE,
  every other ``*_claim`` → HYPOTHESIS (these are decipherment
  hypotheses about a past writing system).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Iterable

from aee.graph import ClaimGraph
from aee.model import (
    Claim,
    ClaimKind,
    ClaimStatus,
    Evidence,
    EvidenceDirection,
    EvidenceKind,
    SourceQuality,
)
from aee.scoring import ClaimScore, ScoringEngine

_log = logging.getLogger("glossa_lab.aee_core")

# Glossa claim_status → AEE ClaimStatus. "untested" has no AEE equivalent;
# it maps to DRAFT and the original is kept in metadata (see docstring).
_STATUS_MAP: dict[str, ClaimStatus] = {
    "supported": ClaimStatus.SUPPORTED,
    "strongly_supported": ClaimStatus.SUPPORTED,
    "partially_supported": ClaimStatus.PARTIALLY_SUPPORTED,
    "contradicted": ClaimStatus.CONTRADICTED,
    "unsupported": ClaimStatus.UNSUPPORTED,
    "unverifiable": ClaimStatus.UNVERIFIABLE,
    "superseded": ClaimStatus.SUPERSEDED,
    "untested": ClaimStatus.DRAFT,
    "draft": ClaimStatus.DRAFT,
}

# Statuses for which glossa_lab_evidence counts as supporting test evidence.
_SUPPORTED_STATUSES = {"supported", "strongly_supported", "partially_supported"}


def map_status(glossa_status: str | None) -> ClaimStatus:
    """Translate a Glossa ``claim_status`` string to an AEE ClaimStatus."""
    return _STATUS_MAP.get((glossa_status or "").strip().lower(), ClaimStatus.DRAFT)


def map_kind(claim_type: str | None) -> ClaimKind:
    """Translate a Glossa ``claim_type`` to the nearest AEE ClaimKind."""
    if (claim_type or "").strip().lower() == "statistical_claim":
        return ClaimKind.INFERENCE
    return ClaimKind.HYPOTHESIS


def claim_from_glossa(raw: dict[str, Any], *, source_file: str = "") -> Claim:
    """Build one AEE Claim (with Evidence) from one extracted-claims record."""
    claim_id = str(raw.get("claim_id") or "").strip()
    if not claim_id:
        raise ValueError("extracted claim is missing claim_id")
    glossa_status = str(raw.get("claim_status") or "untested")
    doc_id = str(raw.get("source_document_id") or "")
    is_contradicted = glossa_status.strip().lower() == "contradicted"

    evidence: list[Evidence] = []
    # 1. The source document's own assertion of the claim.
    if doc_id or raw.get("normalized_claim"):
        evidence.append(
            Evidence(
                ref=f"source:{doc_id or claim_id}",
                kind=EvidenceKind.ASSERTED,
                direction=EvidenceDirection.SUPPORTS,
                source_quality=SourceQuality.SECONDARY,
                description=str(raw.get("quote_fragment") or raw.get("normalized_claim") or ""),
                source_id=doc_id,
            )
        )
    # 2. Glossa Lab's own phase-test evidence, when recorded.
    glossa_ev = raw.get("glossa_lab_evidence")
    if isinstance(glossa_ev, str) and glossa_ev.strip():
        evidence.append(
            Evidence(
                ref=f"glossa-lab:{claim_id}",
                kind=EvidenceKind.OBSERVED if "[VERIFIED]" in glossa_ev else EvidenceKind.INFERRED,
                direction=(
                    EvidenceDirection.CONTRADICTS if is_contradicted else EvidenceDirection.SUPPORTS
                ),
                source_quality=SourceQuality.TEST,
                description=glossa_ev,
                source_id="glossa-lab",
            )
        )
    # 3. Explicit contradicting evidence strings.
    for i, item in enumerate(raw.get("contradicting_evidence") or []):
        if isinstance(item, str) and item.strip():
            evidence.append(
                Evidence(
                    ref=f"contradicting:{claim_id}:{i}",
                    kind=EvidenceKind.OBSERVED,
                    direction=EvidenceDirection.CONTRADICTS,
                    source_quality=SourceQuality.TEST,
                    description=item,
                    source_id="glossa-lab",
                )
            )

    falsification = str(raw.get("falsification_condition") or "").strip()
    testability = str(raw.get("testability") or "").strip()
    confidence_in_source = raw.get("confidence_in_source")
    try:
        initial_confidence = float(confidence_in_source) if confidence_in_source is not None else None
    except (TypeError, ValueError):
        initial_confidence = None

    metadata: dict[str, Any] = {
        "glossa_claim_status": glossa_status,
        "glossa_claim_type": str(raw.get("claim_type") or ""),
        "confidence_in_source": initial_confidence,
        "testability": testability,
        "quote_fragment": str(raw.get("quote_fragment") or ""),
        "source_file": source_file,
    }
    for key in ("signs_involved", "sign_ids", "proposed_value", "proposed_language",
                "author", "extracted_at", "required_data"):
        if raw.get(key) not in (None, "", []):
            metadata[key] = raw[key]

    return Claim(
        id=claim_id,
        text=str(raw.get("normalized_claim") or ""),
        kind=map_kind(str(raw.get("claim_type") or "")),
        status=map_status(glossa_status),
        boundary=[f"testability={testability}"] if testability else [],
        evidence=evidence,
        falsification_tests=[falsification] if falsification else [],
        source_ref=doc_id,
        domain="indus_script",
        confidence=initial_confidence,
        metadata=metadata,
    )


def claims_from_record(record: Any, *, source_file: str = "") -> list[Claim]:
    """Build AEE Claims from one extracted_claims file's parsed JSON.

    Accepts both on-disk shapes: a dict with a ``claims`` list, or a bare
    list of claim records.
    """
    rows: Iterable[Any]
    if isinstance(record, dict):
        rows = record.get("claims") or []
    elif isinstance(record, list):
        rows = record
    else:
        return []
    out: list[Claim] = []
    for row in rows:
        if isinstance(row, dict):
            try:
                out.append(claim_from_glossa(row, source_file=source_file))
            except ValueError as exc:
                _log.warning("skipping extracted claim in %s: %s", source_file, exc)
    return out


def load_claims_from_dir(claims_dir: str | Path) -> list[Claim]:
    """Load every extracted claim under *claims_dir* as AEE Claims.

    Duplicate claim_ids are skipped (ClaimGraph forbids duplicates);
    the first occurrence wins and the skip is logged.
    """
    base = Path(claims_dir)
    claims: list[Claim] = []
    seen: set[str] = set()
    if not base.exists():
        return claims
    for path in sorted(base.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            _log.warning("skipping unreadable claims file %s: %s", path.name, exc)
            continue
        for claim in claims_from_record(record, source_file=path.stem):
            if claim.id in seen:
                _log.warning("duplicate claim_id %s in %s — skipped", claim.id, path.name)
                continue
            seen.add(claim.id)
            claims.append(claim)
    return claims


def build_graph(claims: Iterable[Claim]) -> ClaimGraph:
    """Build the AEE ClaimGraph for *claims* (ids must be unique)."""
    return ClaimGraph(list(claims))


def score_claims(claims: Iterable[Claim]) -> dict[str, ClaimScore]:
    """Score *claims* with AEE's ScoringEngine (see module docstring for
    the engine's confidence-overwrite contract)."""
    return ScoringEngine().score(list(claims))


def score_claim_dicts(raw_claims: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Score raw Glossa claim dicts; return ``{claim_id: ClaimScore.to_dict()}``."""
    claims = []
    for raw in raw_claims:
        if isinstance(raw, dict):
            try:
                claims.append(claim_from_glossa(raw))
            except ValueError:
                continue
    if not claims:
        return {}
    scores = score_claims(claims)
    return {cid: score.to_dict() for cid, score in scores.items()}


def assessment_summary(claims_dir: str | Path) -> dict[str, Any]:
    """Full AEE assessment summary over an extracted_claims directory.

    Returns per-claim scores (ClaimScore dicts plus the preserved Glossa
    fields the API surfaces), graph-health facts, and status counts.
    """
    claims = load_claims_from_dir(claims_dir)
    if not claims:
        return {
            "engine": "applied-epistemic-engineering",
            "total_claims": 0,
            "claims": [],
            "graph": {"healthy": True, "conflicts": [], "cycles": [],
                      "missing_dependencies": {}},
            "status_counts": {},
        }
    graph = build_graph(claims)
    scores = score_claims(claims)
    report = {
        "healthy": not graph.missing_dependencies() and not graph.cycles()
        and not graph.conflicts(),
        "conflicts": [list(pair) for pair in graph.conflicts()],
        "cycles": graph.cycles(),
        "missing_dependencies": graph.missing_dependencies(),
    }
    status_counts: dict[str, int] = {}
    per_claim: list[dict[str, Any]] = []
    for claim in claims:
        status = str(claim.metadata.get("glossa_claim_status", ""))
        status_counts[status] = status_counts.get(status, 0) + 1
        score = scores.get(claim.id)
        per_claim.append({
            "claim_id": claim.id,
            "glossa_claim_status": status,
            "aee_status": claim.status.value,
            "falsification_condition": claim.falsification_tests[0]
            if claim.falsification_tests else "",
            "confidence_in_source": claim.metadata.get("confidence_in_source"),
            "aee_score": score.to_dict() if score else None,
        })
    mean_score = (
        sum(s.propagated_score for s in scores.values()) / len(scores) if scores else 0.0
    )
    return {
        "engine": "applied-epistemic-engineering",
        "total_claims": len(claims),
        "mean_propagated_score": round(mean_score, 6),
        "claims": per_claim,
        "graph": report,
        "status_counts": status_counts,
    }
