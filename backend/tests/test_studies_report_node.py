"""Leg C hardening (C-11): study report-node path confinement.

_run_report_node writes to reports/<report_name> with report_name
taken from caller-supplied node params. A traversal name must land
inside reports/ as a plain file, never outside it.
"""
from __future__ import annotations

from pathlib import Path

from glossa_lab.api.studies import _run_report_node

_REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"


def test_report_node_traversal_name_is_confined():
    node = {"label": "LegC traversal probe",
            "params": {"report_name": "../../legc11_escape.json"}}
    result = _run_report_node(node, {}, {})
    assert result["status"] == "complete"
    escaped = _REPORTS_DIR.parent / "legc11_escape.json"
    confined = _REPORTS_DIR / "legc11_escape.json"
    try:
        assert not escaped.exists()
        assert confined.exists()
    finally:
        confined.unlink(missing_ok=True)


def test_report_node_normal_name_still_writes():
    node = {"label": "LegC normal probe",
            "params": {"report_name": "legc11_normal.json"}}
    _run_report_node(node, {}, {})
    written = _REPORTS_DIR / "legc11_normal.json"
    try:
        assert written.exists()
    finally:
        written.unlink(missing_ok=True)
