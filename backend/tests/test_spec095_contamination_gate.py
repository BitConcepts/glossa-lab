"""Spec 095 Stage 3 (T301) — the contamination gate class.

Acceptance, per C095-7 and the RT-14 acceptance line: planted
instances of each of the six contamination shapes are flagged at
intake; the six historical instances are re-detected from their
records (the fixtures in the spec's records, each reconstructed
from the GR-088-01 / GR-088-11 / GR-088-16 / GR-088-29 family
records it cites); legitimate presentations that merely resemble
the shapes are not flagged; and the class passes on the current
ledger, whose entries carry no contaminated presentation in the
fields they carry.
"""

from __future__ import annotations

import json
from pathlib import Path

from glossa_lab import ledger_contamination as lc

ROOT = Path(__file__).resolve().parents[2]
FIXTURES_PATH = (
    ROOT
    / "specs"
    / "095-red-team-remediation"
    / "records"
    / "t301-fixtures-2026-11-16.json"
)


def _fixtures() -> list[dict]:
    return json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))["fixtures"]


def _flag_shapes(presentation: dict) -> set[str]:
    return {f.shape for f in lc.scan_presentation(presentation)}


def test_the_six_shapes_are_the_claims_six():
    assert [sid for sid, _ in lc.SHAPES] == ["S1", "S2", "S3", "S4", "S5", "S6"]
    assert lc.SHAPE_NAMES["S1"] == "a source-derived value labelled independent"
    assert lc.SHAPE_NAMES["S6"] == (
        "a summary or delivery presented as the underlying record"
    )


def test_fixture_set_covers_all_six_shapes_historically_and_planted():
    fixtures = _fixtures()
    for kind in ("historical", "planted"):
        primaries = {
            f["primary_shape"] for f in fixtures if f["fixture_kind"] == kind
        }
        assert primaries == {"S1", "S2", "S3", "S4", "S5", "S6"}, kind


def test_historical_instances_are_redetected_from_their_records():
    for fixture in _fixtures():
        if fixture["fixture_kind"] != "historical":
            continue
        shapes = _flag_shapes(fixture["presentation"])
        assert fixture["primary_shape"] in shapes, fixture["id"]
        assert set(fixture["expected_shapes"]) <= shapes, fixture["id"]
        # Every historical fixture carries the record it was
        # reconstructed from; a fixture without a citation is an
        # invented instance, which the stage brief forbids.
        assert "GR-088" in fixture["citation"], fixture["id"]


def test_planted_instances_trip_exactly_their_shape():
    for fixture in _fixtures():
        if fixture["fixture_kind"] != "planted":
            continue
        shapes = _flag_shapes(fixture["presentation"])
        assert shapes == {fixture["primary_shape"]}, fixture["id"]


def test_negative_presentations_are_not_flagged():
    for fixture in _fixtures():
        if fixture["fixture_kind"] != "negative":
            continue
        assert _flag_shapes(fixture["presentation"]) == set(), fixture["id"]


def test_the_class_passes_on_the_current_ledger():
    n_scanned, flags = lc.scan_ledger(ROOT)
    assert n_scanned > 1000  # the real ledger, not a stub
    assert flags == [], [f.render() for f in flags]


def test_the_class_has_teeth_on_a_mutated_ledger_entry():
    """A real ledger entry, mutated to carry the same content pin
    under a second source identity, is flagged S5: the class is
    not vacuously green on ledger-shaped data."""
    from glossa_lab import ledger_intake as li

    entries = li.read_ledger(ROOT / "glossa-indus" / "ledger" / "claims.jsonl")
    entry = next(e for e in entries if e.get("sources"))
    presentation = lc.presentation_from_entry(entry)
    first = presentation["sources"][0]
    presentation["sources"].append({
        "path": "planted/second-identity.json",
        "role": "evidence_instance",
        "sha256": first["sha256"],
        "declared_identity": "planted/second-identity.json",
    })
    assert "S5" in _flag_shapes(presentation)


def test_render_scan_reports_its_own_summary():
    text = lc.render_scan(3, [])
    assert "3 presentations scanned, 0 flag(s)" in text
    assert text.rstrip().endswith("CONTAMINATION: PASS")
    flags = lc.scan_presentation({
        "id": "x",
        "subject_lineage": "L",
        "sources": [{
            "path": "p", "kind": "result", "lineage": "L",
            "independence_asserted": True,
        }],
    })
    text = lc.render_scan(1, flags)
    assert "CONTAMINATION: FLAGS RAISED" in text
    assert "S4" in text
