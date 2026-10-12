"""Phase-132 (spec 023, FROZEN) — pilot report pins.

Pins the verdicts of record in reports/phase132_pilot_metrics.json
(stop-rule fired on exact-sequence agreement; error arm not
fired; all three gold-scope release gates fail), the anchors
sha256 asserted unchanged, the pilot report's verdict text,
and the experiment-graph registration (H23).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_METRICS = _REPO / "reports" / "phase132_pilot_metrics.json"
_REPORT = _REPO / "reports" / "phase132_pilot_report.md"
_ANCHORS = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)


def _metrics():
    return json.loads(_METRICS.read_text("utf-8"))


def test_stop_rule_fired_on_agreement_not_error():
    stop = _metrics()["verdicts"]["stop_rule"]
    assert stop["stop_rule_fired"] is True
    assert stop["exact_condition_fires"] is True
    assert stop["exact_sequence_agreement_all_50_p"] == 0.2
    assert stop["error_condition_fires"] is False
    assert stop["gold_error_estimator_p"] == 0.05


def test_release_gates_all_fail():
    gates = _metrics()["verdicts"]["release_gates"]
    assert gates["all_pass"] is False
    assert gates["gate_i_exact_sequence"]["pass"] is False
    assert gates["gate_ii_per_token"]["pass"] is False
    assert gates["gate_iii_gold_error_estimator"]["pass"] is False


def test_anchors_sha256_unchanged():
    # Spec 029 Phase D (OD-1, 2026-10-12): the live anchors file
    # carries additive stage stamps; its pre-existing content is
    # unchanged — canonicalizing by removing exactly the Phase D
    # additive keys reproduces the pinned pre-migration hash.
    doc = json.loads(_ANCHORS.read_text("utf-8"))
    for rec in doc["anchors"].values():
        for k in ("stage", "stage_source", "stage_as_of",
                  "stage_history", "verified_unexplained"):
            rec.pop(k, None)
        # Spec 029 Phase H (D-A, 2026-10-12): also remove the
        # additive annotation — ``strict_set`` on every record,
        # ``validation_status`` on the records that carried none
        # (exactly the Phase H values named below; pre-existing
        # values are untouched), and the metadata block — so the
        # digest still reproduces the pre-migration content.
        rec.pop("strict_set", None)
        if rec.get("validation_status") in (
                "strict_sa_independent", "sa_in_provenance_chain",
                "no_validation_record"):
            rec.pop("validation_status", None)
    doc.get("metadata", {}).pop("spec029_phase_h_annotation", None)
    digest = hashlib.sha256(
        json.dumps(doc, indent=2, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    assert digest == _ANCHORS_SHA256


def test_report_states_verdict_and_no_publication():
    text = _REPORT.read_text("utf-8")
    assert "STOP-RULE FIRED" in text
    assert "NO dataset publication occurs" in text
    assert _ANCHORS_SHA256 in text


def test_graph_node_registered():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase132PilotMetrics" in ATOMIC_NODES
