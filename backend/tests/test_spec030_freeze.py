"""Spec 030 freeze fences (Q6 chronology-spine extension).

Pins: (1) the machine freeze record replays exactly
(framework026 verify_freeze over every frozen source);
(2) the frozen definition carries the adjudicated
design constants, including Ask 2's express
non-coverage; (3) the governed claim register is the
recovered register (7 claims, integrity-clean); (4) the
Stage 0 Q6 gap values the design rests on are exactly
the Phase-391 record's.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/030-q6-chronology-spine-extension"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
STAGE0_RESULTS = REPO / "reports/phase391_results.json"

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
        "spec030-q6-chronology-spine-extension"
    )
    assert definition["register"]["claims"] == 7
    assert definition["register"]["register_version"] == "0.2-draft"
    design = definition["design"]
    assert design["phase"] == "Phase-394"
    assert design["routes_order"] == ["R5", "R1", "R2", "R4", "R3"]
    # Ask 2 was expressly not covered by the adjudication;
    # the frozen record must carry that, not an answer.
    assert "NOT decided" in design["contested_sensitivity"]
    assert "not performed" in design["execution_gate"]


def test_register_integrity():
    from glossa_lab.framework026 import check_dependency_integrity
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.2-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F030-C0{i}" for i in range(1, 8)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
        assert claim["metadata"]["boundary_confirmation"]
    report = check_dependency_integrity(
        [Claim.from_dict(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_stage0_gap_values_pinned():
    results = json.loads(STAGE0_RESULTS.read_text(encoding="utf-8"))
    q6 = results["q6_timing_support"]
    assert q6["status"] == "NOT-YET-TESTABLE"
    criteria = q6["criteria"]
    assert criteria["c1_regions_with_2plus_sites"] == {
        "value": 1, "threshold": 3, "pass": False,
    }
    assert criteria["c2_window_sites_direct_or_associated"] == {
        "value": 5, "threshold": 10, "pass": False,
    }
    assert criteria["c3_window_short_lived_share"] == {
        "value": 0.0, "threshold": 0.5, "pass": False,
    }
    assert criteria["c4_window_median_std_bp"] == {
        "value": 70, "threshold": 80, "pass": True,
    }
    assert q6["window_rows_direct_or_associated"] == 31
    # The frozen definition's inputs must state the same values.
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    pinned = record["definition"]["inputs"]["q6_timing_support"]
    assert pinned["status"] == q6["status"]
    assert pinned["window_rows_direct_or_associated"] == 31
