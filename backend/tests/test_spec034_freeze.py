"""Spec 034 freeze fences (the matched-object attribution).

Pins: (1) the machine freeze record replays exactly
(framework026 verify_freeze over every frozen source);
(2) the frozen definition carries the design's gate,
lines, and prohibitions exactly as frozen (150-object
gate, 0.20 / 0.32 lines, the Holdat prohibition, the
census closure); (3) the governed claim register is the
recovered register (14 claims, integrity-clean); (4) the
cited settled records still carry the numbers the design
rests on (Phase-125: 16 judgeable of 286, median TV
0.636931; Phase-131: 0 shared keys; Phase-124: 7,705
catalogue rows; the dossiers file: 44 rows). These tests
match no objects and compute no distance.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/034-matched-object-attribution"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
P125 = REPO / "reports/phase125_cross_compilation_summary.md"
P131 = REPO / "reports/phase131_attribution.md"
P124 = REPO / "reports/phase124_cisi_image_layer.md"
DOSSIERS = REPO / "reports/phase128_evidence_dossiers_44.csv"

sys.path.insert(0, str(REPO / "backend"))


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == (
        "spec034-matched-object-attribution"
    )
    assert definition["register"]["claims"] == 14
    assert definition["register"]["register_version"] == "0.5-draft"
    design = definition["design"]
    assert design["phase"] == "Phase-398"
    assert design["gate"]["matched_objects_min"] == 150
    assert design["gate"]["min_signs_each_compilation"] == 3
    assert "TOO THIN TO ATTRIBUTE" in (
        design["gate"]["below_gate_closure"])
    crit = design["criteria"]
    assert crit["composition_line"] == 0.20
    assert crit["transcription_line"] == 0.32
    # The prohibition and the gate must be carried, not
    # softened.
    assert "never a join key" in design["prohibited_join"]
    assert "OSF registration" in design["execution_gate"]


def _claim_from_register(raw_claim: dict):
    """Load one frozen-register claim under aee >= 1.5.

    The frozen registers store ``boundary`` as a plain string (the
    pre-1.5 serialization). aee 1.5.0's strict bundle loader refuses
    a scalar where the model declares a list of strings, so the
    string is wrapped at load time; the frozen register bytes are
    never modified.
    """
    from aee.model import Claim

    claim = dict(raw_claim)
    if isinstance(claim.get("boundary"), str):
        claim["boundary"] = [claim["boundary"]]
    return Claim.from_dict(claim)


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.5-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F034-C{i:02d}" for i in range(1, 15)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [_claim_from_register(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_cited_records_carry_the_design_numbers():
    p125 = P125.read_text(encoding="utf-8")
    assert "16 judgeable pairs of 286" in p125
    assert "0.636931" in p125
    p131 = P131.read_text(encoding="utf-8")
    assert "0 shared keys" in p131
    p124 = P124.read_text(encoding="utf-8")
    assert "7,705" in p124
    rows = list(csv.DictReader(DOSSIERS.open(encoding="utf-8")))
    assert len(rows) == 44
