"""Phase-391 (Spec 027 Stage 0) — validators over the tracked
products and the frozen build rules.

The build's inputs live in a gitignored local store, so these
tests validate the committed products (data/movement/) and the
script's pure rule functions — the same split the phase graph
node uses (serve committed results when inputs are absent).
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "backend" / "scripts" / "phase391_stage0_spine.py"
DATA = REPO / "data" / "movement"
RELEASE = (REPO / "specs" / "027-movement-culture-language"
           / "stage0-release")


def _load_script():
    spec = importlib.util.spec_from_file_location("phase391", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in
            path.read_text(encoding="utf-8").splitlines() if line]


def test_material_classification_frozen_mapping():
    m = _load_script()
    assert m.classify_material("Charcoal") == ("long_lived", True, False)
    assert m.classify_material("wood") == ("long_lived", True, False)
    assert m.classify_material("Wheat") == ("short_lived", False, True)
    assert m.classify_material("Human bone") == ("short_lived", False, True)
    assert m.classify_material("") == ("unknown", False, "unknown")
    assert m.classify_material("miscellaneous") == ("unknown", False,
                                                    "unknown")


def test_normalise_name():
    m = _load_script()
    assert m.normalise_name("Mohenjo-Daro") == "mohenjo daro"
    assert m.normalise_name("Shahr-i Sokhta") == "shahr i sokhta"
    assert m.normalise_name("  Chanhu-daro ") == "chanhu daro"


def test_gazetteer_rows_carry_contract_fields():
    rows = _jsonl(DATA / "gazetteer_rows.jsonl")
    assert rows
    for row in rows:
        for key in ("gazetteer_row_id", "program_site_id",
                    "site_name_as_published", "source_gazetteer",
                    "source_citation", "source_locator",
                    "licence_state", "origin_group",
                    "coordinate_state"):
            assert row.get(key) not in (None, ""), (key, row)
        if row["coordinate_state"] == "exact_published":
            assert row["latitude"] is not None
            assert row["longitude"] is not None
            assert row["licence_state"] == "verified_open"


def test_chronology_rows_traced_and_graded():
    rows = _jsonl(DATA / "chronology_rows.jsonl")
    assert rows
    for row in rows:
        assert row["lab_code"]
        assert row["context_association_grade"] in (
            "direct", "associated", "residual_or_intrusive_risk",
            "unassessed")
        assert row["source_record_id"]
    mutin = [r for r in rows if r["scenario"] == "CONTESTED"]
    assert len(mutin) == 33  # Mutin SI Table S2: 26 ECHo + 7 UBA
    assert all(r["program_site_id"] == "mehrgarh" for r in mutin)
    assert all(r["context_association_grade"] == "direct"
               for r in mutin)
    xronos = [r for r in rows if r["source_database"] == "XRONOS"]
    assert len(xronos) == 144  # frozen region filter on the export


def test_release_package_lawful_rows_only():
    results = json.loads((REPO / "reports" / "phase391_results.json")
                         .read_text(encoding="utf-8"))
    gaz = _jsonl(DATA / "gazetteer_rows.jsonl")
    lawful = [r for r in gaz if r["licence_state"] == "verified_open"]
    with open(RELEASE / "indus_gazetteer_stage0_ccby.csv",
              newline="", encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
    assert len(csv_rows) == len(lawful)
    assert results["release_package"]["gazetteer_csv_rows"] == len(lawful)
    assert results["release_package"]["deposit_made"] is False
    # No CISI-derived (open_access_read_only) site leaks into the CSV.
    ccby_sites = {r["site_name_as_published"] for r in csv_rows}
    assert ccby_sites <= {r["site_name_as_published"] for r in lawful}


def test_q6_assessment_recomputes_from_rows():
    m = _load_script()
    rows = _jsonl(DATA / "chronology_rows.jsonl")
    q6 = m.q6_assessment(rows)
    results = json.loads((REPO / "reports" / "phase391_results.json")
                         .read_text(encoding="utf-8"))
    assert q6["status"] == results["q6_timing_support"]["status"]
    assert q6["criteria"] == results["q6_timing_support"]["criteria"]
