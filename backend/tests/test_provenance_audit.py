"""Unit tests for the provenance audit library (spec 006)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from glossa_lab.pipelines.provenance_audit import (  # noqa: E402
    artifact_kind, classify_pass1, first_segment, normalize_reading,
    phase_of_filename, sa_dependent, token_coverage)


def test_normalize_reading():
    assert normalize_reading("ay/ā") == "ay"
    assert normalize_reading("mīn (fish)") == "min"
    assert normalize_reading("iN/in (genitive of)") == "in"
    assert normalize_reading("Ṭōḷ") == "tol"
    assert normalize_reading("") == ""


def test_first_segment():
    assert first_segment("an/aṇ") == "an"
    assert first_segment("kol") == "kol"


def test_phase_of_filename():
    assert phase_of_filename("phase52_syllabic_sa.json") == (52, 52)
    assert phase_of_filename("phase157_160_reference_mining.json") == (157, 160)
    assert phase_of_filename("README.md") is None


def test_artifact_kind():
    assert artifact_kind("phase52_full_decipherment_table.json") == "sa_table"
    assert artifact_kind("phase190_elamo_anchor_injection.json") == "injection"
    assert artifact_kind("phase128_129_anchor_upgrades.json") == "upgrade"
    assert artifact_kind("phase104_claims_evaluation.json") == "other"


def _trail(entry_fields, reading="kol", confidence="HIGH", dedr=None,
           phase_upgraded=None, structured=None):
    return {"sign": "M999", "reading": reading, "confidence": confidence,
            "entry_fields": entry_fields, "phase_upgraded": phase_upgraded,
            "dedr": dedr, "structured": structured or {},
            "ledger_mentions": [], "claims_citing": []}


def test_classify_explicit_dedr():
    t = _trail({"basis": "DEDR 1234 rebus", "dedr": "1234"}, dedr="1234")
    r = classify_pass1(t)
    assert r["decision"] == "explicit" and r["category"] == "DEDR"


def test_classify_explicit_sa_origin():
    t = _trail({"basis": "Reading proposed by Phase-57 SA consensus"})
    r = classify_pass1(t)
    assert r["decision"] == "explicit" and r["category"] == "SA_DERIVED"


def test_classify_ambiguous_needs_review():
    t = _trail({"basis": "Terminal marker, Dravidian case suffix"})
    r = classify_pass1(t)
    # grammar signal alone is explicit per rules; SA+non-SA mix is not
    assert r["decision"] in ("explicit", "needs_review")
    t2 = _trail({"basis": "SA agreement confirms DEDR 55 assignment"})
    r2 = classify_pass1(t2)
    assert r2["decision"] == "needs_review"


def test_classify_no_signal_needs_review():
    t = _trail({"basis": "Common sign"})
    r = classify_pass1(t)
    assert r["decision"] == "needs_review" and r["category"] is None


def test_token_coverage():
    r = token_coverage(["M001", "M002", "M001", "M003"], {"M001", "M003"})
    assert r["n_tokens"] == 4 and r["n_covered"] == 3
    assert r["coverage"] == 0.75


def test_sa_dependent():
    assert sa_dependent({"category": "SA_DERIVED", "sa_in_chain": True})
    assert sa_dependent({"category": "MIXED", "sa_in_chain": True})
    assert not sa_dependent({"category": "DEDR", "sa_in_chain": False})
    assert not sa_dependent({"category": "UNTRACEABLE", "sa_in_chain": False})
