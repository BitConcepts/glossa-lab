"""Tests for the AEE core adapter (backend/glossa_lab/aee_core.py).

Covers: Glossa→AEE status/kind translation, falsification-condition
preservation (native Claim.falsification_tests + round-trip), evidence
attachment from glossa_lab_evidence / contradicting_evidence, scoring
sanity (supported > untested > contradicted), and a round-trip over a
real extracted_claims fixture file from glossa-indus/.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from aee.model import ClaimStatus, EvidenceDirection

from glossa_lab.aee_core import (
    assessment_summary,
    claim_from_glossa,
    claims_from_record,
    load_claims_from_dir,
    map_status,
    score_claims,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_REAL_CLAIMS_DIR = _REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"

SUPPORTED = {
    "claim_id": "t_supported_001",
    "source_document_id": "doc_supported",
    "claim_type": "language_claim",
    "normalized_claim": "Indus script encodes Proto-Dravidian.",
    "claim_status": "partially_supported",
    "testability": "directly_testable",
    "falsification_condition": "If Dravidian phonotactics do not fit sign bigrams.",
    "glossa_lab_evidence": "Phase-41: 1.0566x SA advantage [VERIFIED]",
    "confidence_in_source": 0.85,
}

UNTESTED = {
    "claim_id": "t_untested_001",
    "source_document_id": "doc_untested",
    "claim_type": "sign_value_claim",
    "normalized_claim": "Sign value: 900 / number six",
    "claim_status": "untested",
    "testability": "directly_testable",
    "confidence_in_source": 0.6,
}

CONTRADICTED = {
    "claim_id": "t_contra_001",
    "source_document_id": "doc_contra",
    "claim_type": "non_linguistic_claim",
    "normalized_claim": "The Indus script is not a writing system.",
    "claim_status": "contradicted",
    "testability": "directly_testable",
    "falsification_condition": "Entropy in linguistic range.",
    "contradicting_evidence": ["Rao et al. 2009: entropy in linguistic range"],
    "confidence_in_source": 0.9,
}


# ── Mapping ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("glossa,expected", [
    ("partially_supported", ClaimStatus.PARTIALLY_SUPPORTED),
    ("strongly_supported", ClaimStatus.SUPPORTED),
    ("supported", ClaimStatus.SUPPORTED),
    ("contradicted", ClaimStatus.CONTRADICTED),
    ("untested", ClaimStatus.DRAFT),  # AEE has no UNTESTED; original kept in metadata
    ("zzz_unknown", ClaimStatus.DRAFT),
    (None, ClaimStatus.DRAFT),
])
def test_status_translation(glossa, expected):
    assert map_status(glossa) is expected


def test_original_status_preserved_in_metadata():
    claim = claim_from_glossa(UNTESTED)
    assert claim.status is ClaimStatus.DRAFT
    assert claim.metadata["glossa_claim_status"] == "untested"
    assert claim.metadata["glossa_claim_type"] == "sign_value_claim"
    assert claim.metadata["confidence_in_source"] == 0.6


def test_falsification_condition_preserved_natively():
    claim = claim_from_glossa(SUPPORTED)
    assert claim.falsification_tests == [
        "If Dravidian phonotactics do not fit sign bigrams."
    ]


def test_source_linkage_preserved():
    claim = claim_from_glossa(SUPPORTED)
    assert claim.source_ref == "doc_supported"
    assert claim.domain == "indus_script"
    assert any(ev.source_id == "doc_supported" for ev in claim.evidence)


def test_missing_claim_id_rejected():
    with pytest.raises(ValueError):
        claim_from_glossa({"normalized_claim": "no id"})


# ── Evidence attachment ──────────────────────────────────────────────────

def test_glossa_evidence_attached_as_test_evidence():
    claim = claim_from_glossa(SUPPORTED)
    test_ev = [e for e in claim.evidence if e.source_id == "glossa-lab"]
    assert len(test_ev) == 1
    assert test_ev[0].direction is EvidenceDirection.SUPPORTS
    assert "Phase-41" in test_ev[0].description


def test_contradicting_evidence_attached():
    claim = claim_from_glossa(CONTRADICTED)
    contra = [e for e in claim.evidence if e.direction is EvidenceDirection.CONTRADICTS]
    assert len(contra) == 1
    assert "Rao et al. 2009" in contra[0].description


def test_untested_claim_has_only_source_assertion():
    claim = claim_from_glossa(UNTESTED)
    assert len(claim.evidence) == 1
    assert claim.evidence[0].source_id == "doc_untested"


# ── Scoring sanity ───────────────────────────────────────────────────────

def test_supported_scores_higher_than_untested_and_contradicted():
    claims = [claim_from_glossa(r) for r in (SUPPORTED, UNTESTED, CONTRADICTED)]
    scores = score_claims(claims)
    assert scores["t_supported_001"].propagated_score > scores["t_untested_001"].propagated_score
    assert scores["t_supported_001"].propagated_score > scores["t_contra_001"].propagated_score
    assert scores["t_contra_001"].contradiction_penalty > 0


def test_score_dict_shape():
    scores = score_claims([claim_from_glossa(SUPPORTED)])
    d = scores["t_supported_001"].to_dict()
    assert d["claim_id"] == "t_supported_001"
    assert 0.0 <= d["propagated_score"] <= 1.0
    assert d["components"]["falsifiability"] == 1.0  # has a falsification test


# ── Real fixture round-trip ──────────────────────────────────────────────

def test_real_fixture_round_trip():
    fixture = _REAL_CLAIMS_DIR / "parpola_2010_dravidian_solution.json"
    if not fixture.exists():
        pytest.skip("real extracted_claims fixture not present")
    record = json.loads(fixture.read_text(encoding="utf-8"))
    claims = claims_from_record(record, source_file=fixture.stem)
    assert claims, "fixture produced no claims"
    target = next(c for c in claims if c.id.endswith("manual_001"))
    assert target.metadata["glossa_claim_status"] == "partially_supported"
    assert target.status is ClaimStatus.PARTIALLY_SUPPORTED
    assert target.falsification_tests  # falsification condition survived
    assert target.metadata["confidence_in_source"] == 0.85
    scores = score_claims(claims)
    assert target.id in scores


def test_load_real_claims_dir_and_summary():
    if not _REAL_CLAIMS_DIR.exists():
        pytest.skip("extracted_claims dir not present")
    claims = load_claims_from_dir(_REAL_CLAIMS_DIR)
    assert len(claims) >= 20  # 31 claims across 10 files at time of writing
    ids = [c.id for c in claims]
    assert len(ids) == len(set(ids))  # duplicates are dropped, graph-safe
    summary = assessment_summary(_REAL_CLAIMS_DIR)
    assert summary["engine"] == "applied-epistemic-engineering"
    assert summary["total_claims"] == len(claims)
    assert summary["status_counts"].get("partially_supported", 0) >= 1
    assert 0.0 <= summary["mean_propagated_score"] <= 1.0
