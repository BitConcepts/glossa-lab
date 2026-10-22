"""Spec 026 S5 — historical assessments completeness pins."""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs" / "026-rcph-framework-transfer"


def _doc():
    return json.loads((SPEC / "historical-assessments.json").read_text("utf-8"))


def test_assessments_cover_register():
    doc = _doc()
    register = json.loads((SPEC / "impact-register.json").read_text("utf-8"))
    assert doc["register_items"] == len(register["register"]) == 116
    assert len(doc["rows"]) == 116
    assert {r["item_id"] for r in doc["rows"]} == {
        r["item_id"] for r in register["register"]
    }


def test_changed_set():
    doc = _doc()
    changed = {r["item_id"] for r in doc["rows"] if r["status_changed"]}
    assert doc["status_changed_items"] == len(changed) == 75
    for item in ("PHASE-132", "PHASE-134", "PHASE-135", "PHASE-137",
                 "PHASE-140", "PHASE-111", "PHASE-115", "PHASE-125",
                 "PHASE-92", "SPEC-023", "SPEC-024", "SPEC-025"):
        assert item in changed, item
    for item in ("PHASE-107", "PHASE-136", "PHASE-139", "PHASE-141"):
        assert item not in changed, item


def test_originals_referenced_not_rewritten():
    doc = _doc()
    for r in doc["rows"]:
        assert r["historical_label"]  # label of record carried, not blanked
