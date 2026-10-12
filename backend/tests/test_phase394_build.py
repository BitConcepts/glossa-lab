"""Phase-394 (Spec 030) build-machinery fences.

Pins: (1) the re-test is verbatim — the assessment the
build script imports from the Phase-391 script reproduces
the recorded Stage 0 criteria on the untouched baseline
exactly; (2) dedupe (integrity rule 2) merges the
OxA-1097 triple measurement into one row and refuses to
merge a lab-code collision with differing ages; (3) a
grade correction without the feature naming text fails
loud; (4) a route new-row whose lab code is already
pooled becomes a citation, never a second row (rule 2).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "backend" / "scripts"
sys.path.insert(0, str(REPO / "backend"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p394 = _load("phase394_spine_extension")
p391 = _load("phase391_stage0_spine")


def _baseline_rows() -> list[dict]:
    path = REPO / "data" / "movement" / "chronology_rows.jsonl"
    return [json.loads(line) for line in
            path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def test_assessment_is_the_phase391_function():
    # The build script must import the Stage 0 machinery, never
    # re-implement it: no local definitions of the assessment,
    # the material mapping, or the normaliser in its source.
    src = (SCRIPTS / "phase394_spine_extension.py").read_text(
        encoding="utf-8")
    for forbidden in ("def q6_assessment", "def classify_material",
                      "def normalise_name"):
        assert forbidden not in src
    assert "phase391_stage0_spine" in src
    assert p394.WINDOW_BP == p391.WINDOW_BP == (3850, 5250)


def test_baseline_reproduces_phase391_record():
    rows = _baseline_rows()
    assert len(rows) == 177
    result = p394.q6_assessment(rows)
    assert result["criteria"] == p394.BASELINE_CRITERIA
    assert result["window_rows_direct_or_associated"] == 31
    assert result["status"] == "NOT-YET-TESTABLE"


def test_dedupe_merges_oxa1097_triple():
    pool = p394.Pool(_baseline_rows())
    before = len(pool.rows)
    pool.dedupe()
    keys = [p394.lab_key(r.get("lab_code")) for r in pool.rows]
    assert keys.count(p394.lab_key("OxA-1097")) == 1
    report = pool.dedupe_report
    # The baseline carries 42 duplicate sightings of already-
    # pooled measurements (the Sheri Khan Tarakai / Bannu series
    # ingested once per XRONOS source database).
    assert report["measurements_merged"] == 42
    assert len(report["rows_removed"]) == \
        report["measurements_merged"]
    assert len(pool.rows) == before - report["measurements_merged"]
    merged = next(r for r in pool.rows
                  if p394.lab_key(r.get("lab_code"))
                  == p394.lab_key("OxA-1097"))
    kinds = [c["kind"] for c in
             merged.get("extension", {}).get("citations", [])]
    assert kinds.count("dedupe_merged_measurement") == 3
    # The surviving copy is the richest traced one: a sibling
    # copy named a feature, so the merged measurement is graded
    # associated (the union of the traced evidence, rule 2/3).
    assert merged["context_association_grade"] == "associated"
    # The merged rows disagreed on the site assertion (SKT vs
    # SKT 3): the conflict is reported, not silently resolved.
    assert any(p394.lab_key(c["lab_code"]) == p394.lab_key("OxA-1097")
               for c in report["site_assertion_conflicts"])
    # Dedupe must not lose graded evidence: the deduped
    # baseline still holds all 31 window d/a measurements at
    # the same 5 sites, so the criteria stand as recorded.
    result = p394.q6_assessment(pool.rows)
    assert result["window_rows_direct_or_associated"] == 31
    assert result["criteria"] == p394.BASELINE_CRITERIA


def test_dedupe_refuses_age_conflict():
    rows = [
        {"chronology_row_id": "CHR-T-1", "program_site_id": "a",
         "lab_code": "XX-1", "bp": 4000, "std": 40,
         "context_association_grade": "unassessed",
         "dated_material": "charcoal", "material_class": "long_lived",
         "short_lived_sample": False, "old_wood_risk": True,
         "region_as_recorded": "IN", "scenario": None},
        {"chronology_row_id": "CHR-T-2", "program_site_id": "a",
         "lab_code": "XX-1", "bp": 4100, "std": 40,
         "context_association_grade": "unassessed",
         "dated_material": "charcoal", "material_class": "long_lived",
         "short_lived_sample": False, "old_wood_risk": True,
         "region_as_recorded": "IN", "scenario": None},
    ]
    pool = p394.Pool(rows)
    pool.dedupe()
    assert len(pool.rows) == 2
    assert pool.dedupe_report["age_conflicts_not_merged"]


def test_grade_correction_requires_naming_text():
    pool = p394.Pool(_baseline_rows())
    payload = {"corrections": [{
        "chronology_row_id": "CHR-XRO-296254",
        "field": "context_association_grade", "to": "associated",
        "origin_source": "test", "locator": "test",
        "evidence_text": ""}]}
    with pytest.raises(SystemExit):
        p394.apply_record_route(pool, "R1", payload)


def test_new_row_with_existing_lab_code_becomes_citation():
    pool = p394.Pool(_baseline_rows())
    n_before = len(pool.rows)
    row = {
        "chronology_row_id": "CHR-T-NEW",
        "program_site_id": "tigrana",
        "site_name_as_published": "Tigrana",
        "region_as_recorded": "IN",
        "lab_code": "OxA-30023",
        "dated_material": "Wheat",
        "context_association_grade": "unassessed",
        "bp": 4058, "std": 32,
        "source_database": "test-db", "source_record_id": "t1",
        "licence_state": "verified_open",
        "origin_group": "test", "extension_route": "R2",
        "context_description": None,
        "publication_citation": "test citation",
    }
    detail = p394.apply_record_route(pool, "R2", {"new_rows": [row]})
    assert len(pool.rows) == n_before
    assert detail["new_rows"] == 0
    assert detail["citations_attached"] == 1


def test_material_correction_recomputes_frozen_class():
    pool = p394.Pool(_baseline_rows())
    payload = {"corrections": [{
        "chronology_row_id": "CHR-XRO-289662",
        "field": "dated_material", "to": "charcoal",
        "origin_source": "test origin",
        "locator": "test locator",
        "evidence_text": "origin record material string"}]}
    p394.apply_record_route(pool, "R1", payload)
    row = next(r for r in pool.rows
               if r["chronology_row_id"] == "CHR-XRO-289662")
    assert row["dated_material"] == "charcoal"
    assert row["material_class"] == "long_lived"
    corr = row["extension"]["corrections"][0]
    assert corr["from"] == "Charcoal/QB8"
    assert corr["to"] == "charcoal"
