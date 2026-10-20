"""Spec 032 freeze fences (PRED-2026-006 Harappa breakdown).

Pins: (1) the machine freeze record replays exactly
(framework026 verify_freeze over every frozen source);
(2) the frozen definition carries the registered
criterion and the design constants exactly as frozen
(share bar, start-rate bar, step-0 closures, the
unmappable rule); (3) the governed claim register is
the recovered register (12 claims, integrity-clean);
(4) the withheld-data census the design rests on is
exactly the data file's; (5) the PRED register still
carries the entry as registered (the freeze edited no
register text and no outcome).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/032-pred-2026-006-harappa-breakdown"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
PRED_REGISTER = REPO / "docs/PREDICTION_REGISTER.md"
WITHHELD = (REPO / "backend/glossa_lab/data"
            / "yajnadevam_inscriptions.csv")

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
        "spec032-pred-2026-006-harappa-breakdown"
    )
    assert definition["register"]["claims"] == 12
    assert definition["register"]["register_version"] == "0.4-draft"
    design = definition["design"]
    assert design["phase"] == "Phase-396"
    crit = design["registered_criterion"]
    assert crit["share_min"] == 0.70
    assert crit["start_rate_bar"] == 0.40
    # The fail-closed step 0, the unmappable rule, and the
    # no-invented-band verdict mapping must be carried, not
    # softened.
    assert "CANNOT BE RUN AS WRITTEN" in design["step0"]
    assert "20 percent" in design["unmappable_rule"]
    assert "NOT CONFIRMED" in design["verdict_mapping"]
    assert "no inconclusive band" in design["verdict_mapping"]
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
        f"F032-C{i:02d}" for i in range(1, 13)
    ]
    for claim in raw["claims"]:
        assert claim["falsification_tests"]
        assert claim["evidence"]
        assert claim["metadata"]["boundary_confirmation"]
    report = check_dependency_integrity(
        [_claim_from_register(c) for c in raw["claims"]]
    )
    assert report["ok"]


def test_withheld_census_pinned():
    rows = list(csv.DictReader(
        WITHHELD.open(encoding="utf-8", newline="")))
    assert len(rows) == 5679
    sites = {r["site"] for r in rows}
    assert len(sites) == 77
    assert sum(1 for r in rows if r["site"] == "Harappa") == 2717
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    pinned = record["definition"]["inputs"]["yajnadevam_csv"]
    assert pinned["rows"] == 5679
    assert pinned["sites"] == 77
    assert pinned["harappa_rows"] == 2717


def test_pred_register_entry_unchanged():
    text = PRED_REGISTER.read_text(encoding="utf-8")
    start = text.index("### PRED-2026-006")
    end = text.index("### PRED-2026-007")
    entry = text[start:end]
    # The registered criterion and the recorded state the
    # freeze rests on, exactly as registered 2026-04-22.
    assert "start_rate ≥ 0.40" in entry
    assert "≥ 70% of CISI-trained INITIAL signs" in entry
    assert "Harappa-specific breakdown pending" in entry
    assert "PARTIALLY CONFIRMED" in entry
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    pinned = record["definition"]["inputs"]["prediction"]
    assert pinned["id"] == "PRED-2026-006"
    assert pinned["recorded_outcome"] == "PARTIALLY CONFIRMED"
    assert pinned["global_initial_stability"] == 0.727
