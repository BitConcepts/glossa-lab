"""PRED-2026-011 — registration pins (2026-10-20).

The successor screens PRED-2026-010's clean
CISI Mohenjo-daro INITIAL set through the frozen public
crosswalk before registration. These tests pin the
recomputed derivation and the screened set so the
registration cannot quietly change. They also pin the
package's status: PRED-2026-011 was registered on
2026-10-20 (register entry appended by PR #220; OSF
registration t6whq approved and public, DOI
10.17605/OSF.IO/T6WHQ), and the prediction stands
PENDING and unscored. The derivation record's status
field keeps its derivation-time value
(DRAFT_NOT_REGISTERED): the derivation was performed
and committed while the package was a draft, and that
record is not rewritten by the registration act.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "docs" / "research" / "pred-2026-011-registration"

CORPUS_SHA256 = "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
POOL_MANIFEST_SHA256 = "ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a"
CROSSWALK_SHA256 = "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
WITHHELD_SHA256 = "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
UNDERLYING_INITIAL = ["P000", "P217", "P324"]
SCREENED_INITIAL = ["P217", "P324"]


def _load_derivation():
    spec = importlib.util.spec_from_file_location(
        "pred011_register_derivation",
        REPO / "backend" / "scripts" / "pred011_register_derivation.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pred011_derivation_reproduces_the_screened_set():
    record = _load_derivation().derive()

    assert record["prediction"] == "PRED-2026-011"
    assert record["status"] == "DRAFT_NOT_REGISTERED"

    pool = record["training_pool"]
    assert pool["file_sha256"] == CORPUS_SHA256
    assert pool["pool_manifest_sha256"] == POOL_MANIFEST_SHA256
    assert pool["pool_rows"] == 179
    assert pool["pool_sites"] == {"Mohenjo-daro": 179}
    assert pool["yajnadevam_rows_in_pool"] == 0

    assert record["crosswalk_fixed_by_reference"]["file_sha256"] == CROSSWALK_SHA256
    assert (
        record["withheld_data_fixed_by_reference"]["file_sha256"]
        == WITHHELD_SHA256
    )

    underlying = record["underlying_classification"]
    assert underlying["classifiable_signs"] == 28
    assert underlying["class_counts"] == {
        "INITIAL": 3,
        "MEDIAL": 19,
        "MIXED": 3,
        "TERMINAL": 3,
    }
    assert underlying["unscreened_initial_set"] == UNDERLYING_INITIAL

    screen = record["mappability_screen"]
    assert screen["screening_input"]["file_sha256"] == CROSSWALK_SHA256
    assert screen["trained_initial_set"] == SCREENED_INITIAL
    assert screen["trained_initial_set_size"] == 2

    counterparts = screen["counterparts_by_underlying_initial_sign"]
    assert counterparts["P000"] == []
    assert [row["yajnadevam_glyph"] for row in counterparts["P217"]] == ["Y0520"]
    assert [row["yajnadevam_glyph"] for row in counterparts["P324"]] == ["Y0740"]

    excluded = screen["excluded_signs"]
    assert [row["sign"] for row in excluded] == ["P000"]
    assert [
        row["yajnadevam_glyph"] for row in excluded[0]["top3_only_appearances"]
    ] == ["Y0527", "Y0740", "Y0820", "Y0892"]

    arithmetic = record["criterion_arithmetic"]
    assert arithmetic["possible_shares"] == [0.0, 0.5, 1.0]
    assert arithmetic["minimum_passing_signs"] == 2


def test_committed_pred011_record_matches_the_derivation():
    committed = json.loads((PACKAGE / "derivation-record.json").read_text("utf-8"))
    assert committed == _load_derivation().derive()


def test_pred011_package_records_the_registration():
    readme = (PACKAGE / "README.md").read_text("utf-8")
    proposed = (PACKAGE / "proposed-prediction-register-entry.md").read_text("utf-8")
    payload = (PACKAGE / "osf-registration-payload.md").read_text("utf-8")

    assert "REGISTERED — 2026-10-20" in readme
    assert "Trained INITIAL set: P217, P324" in readme
    assert "only 2 of 2 passes" in readme
    assert "https://osf.io/t6whq/" in readme
    assert "10.17605/OSF.IO/T6WHQ" in readme

    assert "Registration status**: REGISTERED" in proposed
    assert "P217, P324 — 2 signs" in proposed
    assert "OSF completion (2026-10-20)" in proposed
    assert "10.17605/OSF.IO/T6WHQ" in proposed

    assert "FILED — 2026-10-20" in payload
    assert "only at **2 of 2**" in payload
    assert "would not validate the INITIAL class in general" in " ".join(
        payload.split()
    )


def test_register_carries_the_pred011_entry():
    # Registration act of 2026-10-20 (owner order): the
    # entry and its dated section 6 note are appended to
    # the authoritative register, insertions only. The
    # completion append of the same date records the
    # OSF registration's approval and public state.
    register = (REPO / "docs" / "PREDICTION_REGISTER.md").read_text("utf-8")
    assert "### PRED-2026-011" in register
    assert "P217, P324" in register
    assert CROSSWALK_SHA256 in register
    assert "### 2026-10-20 — PRED-2026-011 registered" in register
    assert "PRED-2026-011 OSF registration approved and public" in register
    assert "https://osf.io/t6whq/" in register
    assert "10.17605/OSF.IO/T6WHQ" in register
