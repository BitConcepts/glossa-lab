"""Spec 031 freeze fences (Spec 027 Stage 2 / Q7 design).

Pins: (1) the machine freeze record replays exactly
(framework026 verify_freeze over every frozen source);
(2) the frozen definition carries the design constants
fixed from the D8 margins (support rules, margin, seed,
the ceramic arm's conditional estimability); (3) the
governed claim register is the recovered register
(12 claims, integrity-clean); (4) the D8 margins and
the Stage 0 gazetteer counts the design rests on are
exactly their records'.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/031-stage2-q7-provenance-networks"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
D8_AUDIT = (REPO / "specs/027-movement-culture-language"
            / "stage2-d8-audit.md")
GAZETTEER = REPO / "data/movement/gazetteer_rows.jsonl"

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
        "spec031-stage2-q7-provenance-networks"
    )
    assert definition["register"]["claims"] == 12
    assert definition["register"]["register_version"] == "0.3-draft"
    design = definition["design"]
    assert design["phase"] == "Phase-395"
    rules = design["support_rules"]
    assert rules["site_link_eligible_min_primary_determinations"] == 3
    assert rules["ceramic_site_min_classified_items"] == 20
    assert rules["bead_site_min_classified_beads"] == 10
    assert rules["arm_min_eligible_sites"] == 8
    assert rules["arm_min_linked_pairs"] == 10
    assert design["practical_margin_partial_r2"] == 0.02
    assert design["permutations"] == 9999
    assert design["bootstrap_replicates"] == 9999
    assert design["seed"] == 20261013
    # The ceramic arm's conditional estimability and the
    # execution gate must be carried, not softened.
    assert "NOT ESTIMABLE" in design["ceramic_arm"]
    assert "not ordered" in design["execution_gate"]


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
    assert raw["register_version"] == "0.3-draft"
    assert [c["id"] for c in raw["claims"]] == [
        f"F031-C{i:02d}" for i in range(1, 13)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
        assert claim["metadata"]["boundary_confirmation"]
    report = check_dependency_integrity(
        [_claim_from_register(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_d8_margins_pinned():
    audit = D8_AUDIT.read_text(encoding="utf-8")
    # The operative margins, as the audit states them.
    assert "2,100" in audit
    assert "120 for artifacts from other sites" in audit
    assert "95% of the determinations" in audit
    assert "76 cuneiform" in audit
    # The frozen definition's inputs state the same values.
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    inputs = record["definition"]["inputs"]
    assert inputs["law_determinations"] == {
        "harappa": ">2100",
        "other_sites_combined": "~120",
        "single_site_concentration": "~95%",
    }
    assert inputs["meluhha_citations"] == 76


def test_gazetteer_counts_pinned():
    rows = [json.loads(line) for line in
            GAZETTEER.read_text(encoding="utf-8").splitlines()
            if line.strip()]
    assert len(rows) == 36
    assert len({r["program_site_id"] for r in rows}) == 30
    postures = {}
    for row in rows:
        postures[row["licence_state"]] = (
            postures.get(row["licence_state"], 0) + 1
        )
    assert postures == {"verified_open": 21,
                        "open_access_read_only": 15}
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    pinned = record["definition"]["inputs"]["gazetteer"]
    assert pinned["rows"] == 36
    assert pinned["program_sites"] == 30
    assert pinned["verified_open_rows"] == 21
    assert pinned["open_access_read_only_rows"] == 15
