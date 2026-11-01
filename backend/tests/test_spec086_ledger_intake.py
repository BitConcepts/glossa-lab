"""Spec 086 Stage 1 — ledger intake validator teeth + routes.

C086-2 (schema-pinned intake), C086-3 (D-B dedupe at intake),
C086-5/C086-6 (field provenance / OD-2), T102/T103 acceptance:
a malformed entry, a duplicate-fingerprint entry, and an
authorless-explanation entry are each refused loudly and
nothing is written; one fixture passes through each of the
four intake routes.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from glossa_lab import ledger_intake as li
from glossa_lab.proposition_fingerprint import DuplicatePropositionError

REPO = Path(__file__).resolve().parents[2]
REAL_SCHEMA = REPO / "glossa-indus" / "ledger" / "ledger-schema.json"


def _root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "glossa-indus" / "ledger").mkdir(parents=True)
    shutil.copy(REAL_SCHEMA, root / "glossa-indus" / "ledger" / "ledger-schema.json")
    bundle_dir = root / "specs" / "900-fixture"
    bundle_dir.mkdir(parents=True)
    (bundle_dir / "claims.json").write_text(
        json.dumps(
            {
                "claims": [
                    {
                        "id": "F900-C01",
                        "text": "The fixture proposition holds.",
                        "kind": "requirement",
                        "status": "draft",
                        "boundary": "Fixture records only.",
                        "depends_on": [],
                        "evidence": [],
                        "falsification_tests": [
                            "A fixture record contradicting it defeats it."
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    return root


def _extracted_record(**overrides):
    record = {
        "claim_id": "fixture_doc_manual_001",
        "normalized_claim": "The fixture literature proposition holds.",
        "claim_status": "untested",
        "stage": "created",
        "stage_source": "fixture",
        "stage_as_of": "2026-11-01",
        "source_document_id": "fixture_doc",
        "not_understood": "It does not establish the fixture mechanism.",
        "falsification_condition": "A fixture measurement against it.",
        "evidence_instances": [],
        "sign_ids": {"mahadevan": ["72"]},
    }
    record.update(overrides)
    return record


def _write_extracted(root: Path, record: dict) -> Path:
    path = root / "glossa-indus" / "claims" / "extracted_claims" / "fixture.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"document_id": "fixture_doc", "claims": [record]}),
        encoding="utf-8",
    )
    return path


def test_schema_loads_and_fixture_entry_validates(tmp_path):
    root = _root(tmp_path)
    groups = li.build_bundle_entries(
        root, [root / "specs" / "900-fixture"], date="2026-11-01"
    )
    assert len(groups) == 1
    assert li.validate_entry(groups[0].entry, root=root) == []


def test_route_bundle_import_appends_and_dedupes(tmp_path):
    root = _root(tmp_path)
    groups = li.build_bundle_entries(
        root, [root / "specs" / "900-fixture"], date="2026-11-01"
    )
    li.append_entry(root, groups[0].entry)
    report = li.validate_ledger(root)
    assert report.ok, report.render()
    with pytest.raises(DuplicatePropositionError):
        li.append_entry(root, groups[0].entry)
    lines = (root / li.LEDGER_REL).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1


def test_route_extraction_intake_appends(tmp_path):
    root = _root(tmp_path)
    record = _extracted_record()
    path = _write_extracted(root, record)
    entry = li.entry_from_extracted_record(
        record,
        source_path=str(path.relative_to(root)),
        source_sha256=li.sha256_file(path),
        date="2026-11-01",
    )
    assert entry["sign_refs"] == ["mahadevan:72"]
    li.append_entry(root, entry)
    assert li.validate_ledger(root).ok


def test_teeth_malformed_entry_refused(tmp_path):
    root = _root(tmp_path)
    record = _extracted_record()
    path = _write_extracted(root, record)
    entry = li.entry_from_extracted_record(
        record,
        source_path=str(path.relative_to(root)),
        source_sha256=li.sha256_file(path),
        date="2026-11-01",
    )
    del entry["statement"]
    with pytest.raises(ValueError):
        li.append_entry(root, entry)
    assert not (root / li.LEDGER_REL).exists()


def test_teeth_falsifierless_new_claim_refused(tmp_path):
    root = _root(tmp_path)
    record = _extracted_record()
    record.pop("falsification_condition")
    path = _write_extracted(root, record)
    entry = li.entry_from_extracted_record(
        record,
        source_path=str(path.relative_to(root)),
        source_sha256=li.sha256_file(path),
        date="2026-11-01",
    )
    assert entry["falsifier"] is None and entry["migration"] is None
    with pytest.raises(ValueError, match="prospective rule"):
        li.append_entry(root, entry)
    assert not (root / li.LEDGER_REL).exists()


def test_teeth_authorless_explanation_refused(tmp_path):
    root = _root(tmp_path)
    record = _extracted_record(
        explanation_record={"author_kind": "human", "artifact_uri": "x"}
    )
    path = _write_extracted(root, record)
    entry = li.entry_from_extracted_record(
        record,
        source_path=str(path.relative_to(root)),
        source_sha256=li.sha256_file(path),
        date="2026-11-01",
    )
    with pytest.raises(ValueError, match="OD-2"):
        li.append_entry(root, entry)
    assert not (root / li.LEDGER_REL).exists()


def test_teeth_untraced_falsifier_refused(tmp_path):
    root = _root(tmp_path)
    record = _extracted_record(
        falsification_condition="The traced fixture condition."
    )
    path = _write_extracted(root, record)
    entry = li.entry_from_extracted_record(
        record,
        source_path=str(path.relative_to(root)),
        source_sha256=li.sha256_file(path),
        date="2026-11-01",
        migration={"run_id": "fixture", "migrated_at": "2026-11-01"},
    )
    entry["falsifier"] = ["An invented falsifier appearing in no source."]
    errors = li.validate_entry(entry, root=root)
    assert any("traces to no source record" in e for e in errors)


def test_route_annotation_intake(tmp_path):
    root = _root(tmp_path)
    record = _extracted_record()
    path = _write_extracted(root, record)
    claim_entry = li.entry_from_extracted_record(
        record,
        source_path=str(path.relative_to(root)),
        source_sha256=li.sha256_file(path),
        date="2026-11-01",
    )
    li.append_entry(root, claim_entry)
    sidecar = {
        "claim_id": record["claim_id"],
        "document_id": "fixture_doc",
        "stage": "research_check",
        "advisory": True,
        "verdict": None,
        "checked_at": "2026-11-01T00:00:00+00:00",
        "protocol": "fixture-protocol",
        "sources_requested": ["crossref"],
        "neighbors": [{"title": "n"}],
        "gaps": [],
    }
    sidecar_path = (
        root
        / "glossa-indus"
        / "claims"
        / "research_checks"
        / "fixture_doc__fixture_doc_manual_001.research_check.json"
    )
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)
    sidecar_path.write_text(json.dumps(sidecar), encoding="utf-8")
    annotation = li.annotation_from_sidecar(
        root, sidecar_path, date="2026-11-01", canonical_map={}
    )
    li.append_entry(root, annotation)
    report = li.validate_ledger(root)
    assert report.ok, report.render()
    assert report.kind_counts == {"claim": 1, "annotation": 1}


def test_route_discovery_promotion(tmp_path):
    root = _root(tmp_path)
    entry = li.discovery_candidate(
        {"id": "item-1", "statement": "A promoted fixture candidate."},
        promoted_by="Fixture Human",
        falsifier=["A fixture check against the candidate."],
        date="2026-11-01",
    )
    li.append_entry(root, entry)
    assert li.validate_ledger(root).ok
    with pytest.raises(ValueError, match="requires a falsifier"):
        li.discovery_candidate(
            {"id": "item-2", "statement": "No falsifier."},
            promoted_by="Fixture Human",
            falsifier=[],
            date="2026-11-01",
        )
    with pytest.raises(ValueError, match="named human"):
        li.discovery_candidate(
            {"id": "item-3", "statement": "No human."},
            promoted_by="",
            falsifier=["x"],
            date="2026-11-01",
        )


def test_append_only_prefix_preserved(tmp_path):
    root = _root(tmp_path)
    record = _extracted_record()
    path = _write_extracted(root, record)
    first = li.entry_from_extracted_record(
        record,
        source_path=str(path.relative_to(root)),
        source_sha256=li.sha256_file(path),
        date="2026-11-01",
    )
    li.append_entry(root, first)
    before = (root / li.LEDGER_REL).read_bytes()
    groups = li.build_bundle_entries(
        root, [root / "specs" / "900-fixture"], date="2026-11-01"
    )
    li.append_entry(root, groups[0].entry)
    after = (root / li.LEDGER_REL).read_bytes()
    assert after.startswith(before) and len(after) > len(before)


def test_canonical_hash_is_checkout_invariant(tmp_path):
    """Adopted pattern 'Canonicalize before you hash'
    (2026-11-01): a source file hashes identically under LF
    and CRLF checkout bytes."""
    lf = tmp_path / "lf.json"
    crlf = tmp_path / "crlf.json"
    lf.write_bytes(b'{"a": 1}\n{"b": 2}\n')
    crlf.write_bytes(b'{"a": 1}\r\n{"b": 2}\r\n')
    assert li.sha256_file(lf) == li.sha256_file(crlf)
    assert li.sha256_file(lf) != li.sha256_bytes(crlf.read_bytes())


def test_confidence_text_carried_verbatim_never_numeric(tmp_path):
    """Adoption #3 item 6 (binding): narrative confidence is
    not a number. A qualitative confidence string migrates
    VERBATIM into confidence_text; a numeric one stays the
    same number in confidence_in_source; neither is coerced
    into the other."""
    root = _root(tmp_path)
    text_entry = li.entry_from_extracted_record(
        _extracted_record(confidence="low"),
        source_path="fixture.json",
        source_sha256="0" * 64,
        date="2026-11-01",
    )
    assert text_entry["confidence_text"] == "low"
    assert text_entry["confidence_in_source"] is None
    assert li.validate_entry(text_entry, root=root) == []
    numeric_entry = li.entry_from_extracted_record(
        _extracted_record(confidence_in_source=0.4),
        source_path="fixture.json",
        source_sha256="0" * 64,
        date="2026-11-01",
    )
    assert numeric_entry["confidence_in_source"] == 0.4
    assert numeric_entry["confidence_text"] is None
    absent_entry = li.entry_from_extracted_record(
        _extracted_record(),
        source_path="fixture.json",
        source_sha256="0" * 64,
        date="2026-11-01",
    )
    assert absent_entry["confidence_in_source"] is None
    assert absent_entry["confidence_text"] is None


def test_validator_fails_on_missing_ledger(tmp_path):
    """A gate that passes on an absent artifact certifies
    nothing: missing is RED (defect found and fixed
    2026-11-01 — the first version read a missing file as
    zero lines and reported PASS)."""
    report = li.validate_ledger(tmp_path)
    assert not report.ok
    assert any("does not exist" in e for e in report.errors)


def test_validator_fails_on_empty_ledger(tmp_path):
    (tmp_path / "glossa-indus" / "ledger").mkdir(parents=True)
    (tmp_path / "glossa-indus" / "ledger" / "claims.jsonl").write_text(
        "", encoding="utf-8"
    )
    report = li.validate_ledger(tmp_path)
    assert not report.ok
    assert any("no entries" in e for e in report.errors)


def test_validator_fails_on_seeded_malformed_line(tmp_path):
    root = _root(tmp_path)
    ledger = root / li.LEDGER_REL
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text('{"id": "x", "kind": "claim"}\n', encoding="utf-8")
    report = li.validate_ledger(root)
    assert not report.ok
    assert "RESULT: FAIL" in report.render()
