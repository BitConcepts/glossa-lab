"""Spec 086 Stage 1 — migration reconciliation invariants (T104).

Recomputes the census and the mirror checks independently of
the migration tool and compares them against the built ledger
and the filed reconciliation reports: counts in == out per
population, every source record accounted for in some entry's
``sources``, mirrored status/stage byte-equal to the source of
record (C086-20), falsifier coverage as recorded (C086-5).
"""

from __future__ import annotations

import json
from pathlib import Path

from glossa_lab import ledger_intake as li
from glossa_lab.proposition_fingerprint import proposition_fingerprint

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs" / "086-winning-combination-adoption"
ENTRIES = li.read_ledger(REPO / li.LEDGER_REL)
CLAIMS = [e for e in ENTRIES if e["kind"] == "claim"]
ANNOTATIONS = [e for e in ENTRIES if e["kind"] == "annotation"]


def _p1_records():
    records = {}
    claims_dir = REPO / "glossa-indus" / "claims" / "extracted_claims"
    for path in sorted(claims_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data["claims"]:
            records[record["claim_id"]] = record
    return records


def _p2_records():
    records = []
    for pattern in ("specs/*/claims.json", "specs/*/aee-claims.json"):
        for path in sorted(REPO.glob(pattern)):
            data = json.loads(path.read_text(encoding="utf-8"))
            for record in data["claims"]:
                records.append((path.parent.name, str(record["id"]), record))
    return records


def test_ledger_validates_clean():
    report = li.validate_ledger(REPO)
    assert report.ok, report.render()
    assert report.lines == len(ENTRIES)


def test_p1_reconciliation():
    records = _p1_records()
    assert len(records) == 31
    extracted = [e for e in CLAIMS if e["population"] == "extracted"]
    canonical_ids = {
        cid for cid, r in records.items() if not r.get("merged_into")
    }
    assert {e["id"] for e in extracted} == canonical_ids
    assert len(extracted) == 23
    # every source record is accounted for in some entry's sources
    accounted = {
        s["claim_id"]
        for e in extracted
        for s in e["sources"]
        if s.get("claim_id")
    }
    assert accounted == set(records)
    # mirror: status/stage byte-equal to the canonical source record
    for entry in extracted:
        record = records[entry["id"]]
        assert entry["status"] == record["claim_status"]
        assert entry["stage"] == record["stage"]
        assert entry["proposition_fingerprint"] == proposition_fingerprint(
            record["normalized_claim"]
        )
        # confidence carriage (adoption #3 item 6): the source's
        # numeric confidence_in_source is carried verbatim; no
        # entry anywhere carries a numericized narrative value
        assert entry["confidence_in_source"] == record.get(
            "confidence_in_source"
        )
        assert entry["confidence_text"] is None


def test_p3_reconciliation():
    sidecars = sorted(
        (REPO / "glossa-indus" / "claims" / "research_checks").glob(
            "*.research_check.json"
        )
    )
    assert len(sidecars) == len(ANNOTATIONS) == 31
    claim_ids = {e["id"] for e in CLAIMS}
    for annotation in ANNOTATIONS:
        assert annotation["canonical_claim_id"] in claim_ids
        sidecar = json.loads(
            (REPO / annotation["sidecar"]["path"]).read_text(encoding="utf-8")
        )
        assert annotation["target_claim_id"] == sidecar["claim_id"]
        assert annotation["bearing"]["advisory"] is True


def test_p2_reconciliation():
    records = _p2_records()
    bundle = [e for e in CLAIMS if e["population"] == "bundle"]
    expected_fps = {proposition_fingerprint(r["text"]) for _, _, r in records}
    assert {e["proposition_fingerprint"] for e in bundle} == expected_fps
    # every source record is accounted for exactly once across sources
    accounted = []
    for entry in bundle:
        for source in entry["sources"]:
            accounted.append((source["spec"], source["claim_id"], source["path"]))
    assert len(accounted) == len(records)
    assert len(set(accounted)) == len(records)
    # mirror: status byte-equal to the representative source record
    by_key = {(spec, cid): r for spec, cid, r in records}
    for entry in bundle:
        rep = next(
            s for s in entry["sources"] if s["role"] == "source_of_record"
        )
        record = by_key[(rep["spec"], rep["claim_id"])]
        assert entry["status"] == record["status"]
        assert entry["statement"] == record["text"]


def test_falsifier_coverage_as_recorded():
    extracted = [e for e in CLAIMS if e["population"] == "extracted"]
    bundle = [e for e in CLAIMS if e["population"] == "bundle"]
    assert sum(1 for e in extracted if e["falsifier"]) == 14
    assert all(e["falsifier"] for e in bundle)
    report = li.validate_ledger(REPO)
    assert report.falsifier_covered == sum(
        1 for e in CLAIMS if e["falsifier"]
    )


def test_reconciliation_reports_filed():
    for name in (
        "reconciliation-p1.md",
        "reconciliation-p2.md",
        "reconciliation-p3.md",
    ):
        text = (SPEC_DIR / "records" / name).read_text(encoding="utf-8")
        assert "Headline counts" in text
    p2 = (SPEC_DIR / "records" / "reconciliation-p2.md").read_text(
        encoding="utf-8"
    )
    assert "1624 source records" in p2
    assert "double-format question" in p2.lower()
