"""Phase-398 (Spec 034) build-machinery fences.

Pins: (1) the bridge joins ONLY on the published CISI
object ID carried in the intake record's
provenance.object_id — a Holdat-style sequential
namesake (an inscription whose own id reads M-0001
while its published object reference is another
object) never pairs; (2) the frozen gate arithmetic
(>= 150 matched objects with texts of >= 3 signs in
BOTH compilations) on synthetic fixtures, at the
boundary; (3) the frozen verdict lines (0.20 / 0.32)
including the boundary values; (4) the intake dataset
built from ICIT-shaped records validates under the
Phase-130 schema (UNK sentinels permitted); (5) the
decomposition reuses Phase-131's classification on a
known pair (one substitution block), and the primary
map is all-or-nothing.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab import phase398_matched_object as p398  # noqa: E402
from glossa_lab.intake import validate_dataset  # noqa: E402


def _mayig(oid, tokens):
    return {"cisi_object_id": oid, "side_id": f"{oid}A",
            "tokens": list(tokens), "token_count": len(tokens),
            "source_file": "fixture"}


def _intake(oid, tokens, row=1, site="Mohenjo-daro"):
    return {"inscription_id": f"icit-v2-row-{row}",
            "source_row": row, "site": site,
            "tokens": list(tokens), "sign_list": "mahadevan_1977",
            "object_type": "SEAL:S",
            "provenance": {
                "source_reference": f"fixture row {row}",
                "object_id": oid,
                "transcriber": "fixture"}}


def _catalogue(*oids):
    return {oid: {"n_rows": 1, "sites": {"Mohenjo-Daro"},
                  "object_types": {"Seals"}, "volumes": {1}}
            for oid in oids}


def test_bridge_joins_only_on_published_object_id():
    mayig = [_mayig("M-1", ["P001", "P002", "P003"])]
    # A namesake trap: the intake record's own id echoes
    # a sequential number, but its published object
    # reference is a different object — no pair may form.
    intake = [_intake("H-15", ["M001", "M002", "M003"], row=7)]
    intake[0]["inscription_id"] = "M-0001"
    bridge = p398.build_bridge(mayig, intake, _catalogue("M-1"))
    assert bridge["pairs"][0]["matched"] is False
    intake[0]["provenance"]["object_id"] = "M-1"
    bridge = p398.build_bridge(mayig, intake, _catalogue("M-1"))
    assert bridge["pairs"][0]["matched"] is True


def test_bridge_ambiguous_reference_never_pairs():
    mayig = [_mayig("M-2", ["P001", "P002", "P003"])]
    intake = [_intake("M-2", ["M001", "M002", "M003"], row=1),
              _intake("M-2", ["M004", "M005", "M006"], row=2)]
    bridge = p398.build_bridge(mayig, intake, _catalogue("M-2"))
    assert bridge["pairs"][0]["matched"] is False
    assert bridge["ambiguous"][0]["cisi_object_id"] == "M-2"


def _gate_pairs(n_ok, n_short_mayig=0, n_short_icit=0):
    pairs = []
    for i in range(n_ok):
        pairs.append((_mayig(f"M-{1000+i}", ["P001"] * 4),
                      _intake(f"M-{1000+i}", ["M001"] * 4, row=i)))
    for i in range(n_short_mayig):
        pairs.append((_mayig(f"M-{2000+i}", ["P001"] * 2),
                      _intake(f"M-{2000+i}", ["M001"] * 4,
                              row=100 + i)))
    for i in range(n_short_icit):
        pairs.append((_mayig(f"M-{3000+i}", ["P001"] * 4),
                      _intake(f"M-{3000+i}", ["M001"] * 2,
                              row=200 + i)))
    mayig = [m for m, _ in pairs]
    intake = [t for _, t in pairs]
    cat = _catalogue(*[m["cisi_object_id"] for m in mayig])
    return p398.build_bridge(mayig, intake, cat)["pairs"]


def test_gate_boundary_exactly_150_passes():
    pairs = _gate_pairs(150, n_short_mayig=3, n_short_icit=2)
    gate = p398.apply_gate(pairs)
    assert gate["n_matched_objects"] == 155
    assert gate["n_gate_objects"] == 150
    assert gate["gate_passed"] is True


def test_gate_149_closes_too_thin():
    pairs = _gate_pairs(149)
    gate = p398.apply_gate(pairs)
    assert gate["n_gate_objects"] == 149
    assert gate["gate_passed"] is False


def test_verdict_lines_boundaries():
    assert p398.verdict_for(0.20) == "ATTRIBUTED TO COMPOSITION"
    assert p398.verdict_for(0.199) == "ATTRIBUTED TO COMPOSITION"
    assert p398.verdict_for(0.32) == "ATTRIBUTED TO TRANSCRIPTION"
    assert p398.verdict_for(0.45) == "ATTRIBUTED TO TRANSCRIPTION"
    assert p398.verdict_for(0.25) == "SPLIT ATTRIBUTION"
    assert p398.verdict_for(None) is None


def test_intake_dataset_validates_with_unk_sentinels():
    icit = {"inscriptions": [
        {"row": 5, "id": "9.1", "cisi": "M-1",
         "site": "Mohenjo-daro", "type": "SEAL:S",
         "tokens": ["M342", "UNK", "M267"]},
        {"row": 6, "id": "9.2", "cisi": "-",
         "site": "Harappa", "type": "SEAL:S",
         "tokens": ["M001", "M002"]},
        {"row": 7, "id": "9.3", "cisi": None,
         "site": "Harappa", "type": "SEAL:S",
         "tokens": ["M001"]},
    ]}
    dataset = p398.build_intake_dataset(icit)
    # Only the record carrying a published CISI
    # reference is admitted.
    assert len(dataset["inscriptions"]) == 1
    assert dataset["inscriptions"][0]["provenance"]["object_id"] \
        == "M-1"
    report = validate_dataset(dataset)
    assert report["verdict"] != "reject", report["errors"]
    assert report["summary"]["inscriptions"] == 1


def test_decomposition_known_pair_one_substitution():
    rows = [{"parpola_id": "P342", "mahadevan_id": "M342",
             "confidence": "high", "conflict": False},
            {"parpola_id": "P296", "mahadevan_id": "M296",
             "confidence": "high", "conflict": False},
            {"parpola_id": "P059", "mahadevan_id": "M059",
             "confidence": "high", "conflict": False},
            {"parpola_id": "P087", "mahadevan_id": "M087",
             "confidence": "high", "conflict": False}]
    # build_arms expects the full crosswalk row shape;
    # primary_map works off build_arms, so extend rows
    # with the fields it reads if any are missing.
    pair = {"cisi_object_id": "M-124",
            "mayig": {"side_id": "M-124A",
                      "tokens": ["P342", "P296", "P059", "P087"],
                      "token_count": 4, "source_file": "fixture"},
            "icit": {"inscription_id": "icit-v2-row-1",
                     "source_row": 1,
                     "tokens": ["M342", "M410", "M059", "M087"],
                     "token_count": 4, "site": "Mohenjo-daro",
                     "object_type": "SEAL:S"},
            "catalogue": None, "matched": True, "gate_ok": True,
            "icit_build_status": "kept"}
    out = p398.decompose([pair], rows)
    assert out["n_eligible"] == 1
    rec = out["per_object"][0]
    assert rec["pair_class"] == "substitution"
    assert out["block_token_totals"]["substitution"] == 2
    assert out["shares_phase131_estimators"]["substitution"] == 1.0
    # (P296, M410) has no crosswalk row.
    assert out["substitution_crosswalk_check"] == {
        "no_crosswalk_row": 1}


def test_decomposition_unmapped_token_ineligible():
    rows = [{"parpola_id": "P342", "mahadevan_id": "M342",
             "confidence": "high", "conflict": False}]
    pair = {"cisi_object_id": "M-9",
            "mayig": {"side_id": "M-9A",
                      "tokens": ["P342", "P999"],
                      "token_count": 2, "source_file": "fixture"},
            "icit": {"inscription_id": "icit-v2-row-2",
                     "source_row": 2, "tokens": ["M342", "M001"],
                     "token_count": 2, "site": "Mohenjo-daro",
                     "object_type": "SEAL:S"},
            "catalogue": None, "matched": True, "gate_ok": True,
            "icit_build_status": "kept"}
    out = p398.decompose([pair], rows)
    assert out["n_eligible"] == 0
    assert out["n_ineligible"] == 1
    assert out["per_object"][0]["distance"] is None
