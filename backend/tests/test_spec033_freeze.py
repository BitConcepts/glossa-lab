"""Spec 033 freeze fences (the SA-free language comparison).

Pins: (1) the machine freeze record replays exactly
(framework026 verify_freeze over every frozen source);
(2) the frozen definition carries the design's criteria
and the SA-free construction exactly as frozen (margin,
percentile, control count, H26 bar, the freeze-time
estimator); (3) the governed claim register is the
recovered register (15 claims, integrity-clean); (4) the
strict-set census the design runs on is exactly the
anchors file's (287 total, 94 strict_sa_independent);
(5) the recorded original margins the bars were set from
are on record in the ledger archive (Phase-41 1.0566;
Phase-43 0.484). These tests compute no score.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/033-sa-free-language-comparison"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
ARCHIVE = REPO / "docs/ledger-archive.md"

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
        "spec033-sa-free-language-comparison"
    )
    assert definition["register"]["claims"] == 15
    assert definition["register"]["register_version"] == "0.4-draft"
    design = definition["design"]
    assert design["phase"] == "Phase-397"
    crit = design["criteria"]
    assert crit["supported_margin_log_units"] == 0.10
    assert crit["random_percentile"] == 99
    assert crit["random_controls"] == 999
    # The H26 construction and the execution gate must be
    # carried, not softened.
    assert "no semantic anchoring" in design["sa_free"]
    assert "no anchor promotion" in design["sa_free"]
    assert "add-one" in design["estimator"]
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
    from aee.model import Claim

    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert raw["register_version"] == "0.4-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F033-C{i:02d}" for i in range(1, 16)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
    report = check_dependency_integrity(
        [_claim_from_register(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_strict_set_census():
    data = json.loads(ANCHORS.read_text(encoding="utf-8"))
    anchors = data["anchors"]
    assert len(anchors) == 287
    strict = [a for a in anchors.values()
              if a["validation_status"] == "strict_sa_independent"]
    assert len(strict) == 94


def test_original_margins_on_record():
    archive = ARCHIVE.read_text(encoding="utf-8", errors="replace")
    assert "1.0566" in archive  # Phase-41 ratio
    assert "0.484" in archive    # Phase-43 log units
