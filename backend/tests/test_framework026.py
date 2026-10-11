"""Tests for Spec 026 framework machinery (framework026.py).

Covers FR-026-2 (claim-register integrity: cycles, missing
dependencies, forbidden-assumption inheritance — including the
planted cases that must fail loudly) and FR-026-3 (freeze/replay:
tampered definition or source must be detected).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from glossa_lab.aee_core import Claim
from glossa_lab.framework026 import (
    build_freeze,
    check_dependency_integrity,
    verify_freeze,
)


def _claim(cid: str, **overrides) -> Claim:
    base = {
        "id": cid,
        "text": f"claim {cid}",
        "kind": "inference",
        "status": "draft",
        "boundary": "test boundary",
        "depends_on": [],
        "assumptions": [],
        "metadata": {},
    }
    base.update(overrides)
    return Claim.from_dict(base)


def test_clean_register_passes() -> None:
    claims = [
        _claim("A"),
        _claim("B", depends_on=["A"], assumptions=["ASM-OK"]),
    ]
    report = check_dependency_integrity(claims)
    assert report["ok"] is True
    assert report["cycles"] == []
    assert report["forbidden_inheritance"] == []


def test_planted_cycle_is_reported() -> None:
    claims = [
        _claim("A", depends_on=["B"]),
        _claim("B", depends_on=["A"]),
    ]
    report = check_dependency_integrity(claims)
    assert report["ok"] is False
    assert report["cycles"], "planted cycle must be detected"


def test_missing_dependency_is_reported() -> None:
    claims = [_claim("A", depends_on=["GHOST"])]
    report = check_dependency_integrity(claims)
    assert report["ok"] is False
    assert report["missing_dependencies"] == ["GHOST"]


def test_planted_forbidden_inheritance_is_reported() -> None:
    claims = [
        _claim("BASE", assumptions=["ASM-SA-VALID"]),
        _claim(
            "TOP",
            depends_on=["BASE"],
            metadata={"forbidden_assumptions": ["ASM-SA-VALID"]},
        ),
    ]
    report = check_dependency_integrity(claims)
    assert report["ok"] is False
    hits = report["forbidden_inheritance"]
    assert len(hits) == 1
    assert hits[0]["claim_id"] == "TOP"
    assert hits[0]["forbidden"] == "ASM-SA-VALID"
    assert hits[0]["inherited_from"] == "BASE"


def test_forbidden_inheritance_through_intermediate() -> None:
    claims = [
        _claim("BASE", assumptions=["ASM-KERNEL-PROOF"]),
        _claim("MID", depends_on=["BASE"]),
        _claim(
            "TOP",
            depends_on=["MID"],
            metadata={"forbidden_assumptions": ["ASM-KERNEL-PROOF"]},
        ),
    ]
    report = check_dependency_integrity(claims)
    assert report["ok"] is False
    assert report["forbidden_inheritance"][0]["inherited_from"] == "BASE"


def test_unrelated_forbidden_assumption_passes() -> None:
    claims = [
        _claim("BASE", assumptions=["ASM-OTHER"]),
        _claim(
            "TOP",
            depends_on=["BASE"],
            metadata={"forbidden_assumptions": ["ASM-SA-VALID"]},
        ),
    ]
    assert check_dependency_integrity(claims)["ok"] is True


def test_spec026_register_itself_is_clean() -> None:
    register = Path(__file__).resolve().parents[2] / (
        "specs/026-rcph-framework-transfer/claims.json"
    )
    rows = json.loads(register.read_text())["claims"]
    claims = [Claim.from_dict(r) for r in rows]
    report = check_dependency_integrity(claims)
    assert report["ok"] is True, report


def _freeze_fixture(tmp_path: Path) -> tuple[dict, Path]:
    src = tmp_path / "source.py"
    src.write_text("VALUE = 1\n")
    definition = {"experiment_id": "TEST-001", "threshold": 0.5, "seeds": [1, 2]}
    record = build_freeze(definition, tmp_path, ["source.py"])
    return record, src


def test_freeze_roundtrip_verifies(tmp_path: Path) -> None:
    record, _ = _freeze_fixture(tmp_path)
    assert record["digest"]
    assert verify_freeze(record, tmp_path) == []


def test_freeze_detects_source_change(tmp_path: Path) -> None:
    record, src = _freeze_fixture(tmp_path)
    src.write_text("VALUE = 2\n")
    errors = verify_freeze(record, tmp_path)
    assert any("source changed" in e for e in errors)


def test_freeze_detects_definition_tamper(tmp_path: Path) -> None:
    record, _ = _freeze_fixture(tmp_path)
    record["definition"]["threshold"] = 0.9
    errors = verify_freeze(record, tmp_path)
    assert any("digest mismatch" in e for e in errors)


def test_freeze_rejects_escaping_source(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        build_freeze({"x": 1}, tmp_path, ["../outside.py"])
