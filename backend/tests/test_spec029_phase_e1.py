"""Spec 029 Phase E1 — display withdrawals (tasks E1.1–E1.4).

Pins the anti-gradability withdrawals the audit (§5-P5) demanded
(FR-029-08; claim F029-C06):

* E1.2 — the dashboard decipherment payload no longer serves
  ``sa_aggregate`` (the falsified SA method's aggregate),
  ``fully_decoded_pct``, or ``n_fully_decoded`` — at the top
  level or inside per-round progression entries — while every
  other field, including Phase A's lane-2 ``by_stage`` /
  ``n_unstamped_stage`` anchor fields, is still served.
* E1.3 — ``mean_propagated_score`` is withdrawn from the
  ``GET /claims/aee-scores`` summary position
  (``aee_core.assessment_summary``). Per-claim scores remain in
  their per-claim detail entries, each with its own falsifier
  and stage object — the withdrawal is of the summary mean,
  not of the lane-1 detail.
* E1.1/E1.4 — the DeciphermentPanel source no longer contains
  the withdrawn headline / tile / bar constructions or any
  consumption of the withdrawn fields. (The rendered-output
  side is verified by the phase's desktop + mobile screenshots
  in ``specs/029-tao-claim-lifecycle/phase-e1-evidence/``.)
"""
from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from glossa_lab.aee_core import assessment_summary
from glossa_lab.api.dashboard import dashboard_decipherment

_REPO = Path(__file__).resolve().parents[2]
_PANEL = _REPO / "frontend" / "src" / "components" / "DeciphermentPanel.tsx"
_CLAIMS_DIR = _REPO / "glossa-indus" / "claims" / "extracted_claims"

WITHDRAWN_DASHBOARD_FIELDS = ("sa_aggregate", "fully_decoded_pct", "n_fully_decoded")

#: Rendered constructions withdrawn from the panel (E1.1/E1.4).
#: This test file is the guard that greps for them, so it is the
#: one place they are quoted — as a purge list, never as copy.
WITHDRAWN_PANEL_STRINGS = (
    "signs deciphered",
    "Signs Deciphered",
    "SA Confidence",
    "Seals Decoded",
    "Inscriptions Fully Decoded",
    "Weighted Confidence",
    "Deciphered signs",
)


# ── E1.2: dashboard payload ──────────────────────────────────────────────


def test_dashboard_payload_withdraws_sa_and_fully_decoded_fields():
    payload = asyncio.run(dashboard_decipherment())
    assert payload["available"] is True
    for field in WITHDRAWN_DASHBOARD_FIELDS:
        assert field not in payload, field
    # Per-round progression entries carry the withdrawal too.
    for entry in payload["progression"]:
        assert "fully_decoded_pct" not in entry


def test_dashboard_payload_keeps_honest_fields_incl_phase_a_stage_fields():
    payload = asyncio.run(dashboard_decipherment())
    anchors = payload["anchors"]
    # Phase A's additive lane-2 fields must survive E1 untouched.
    assert "by_stage" in anchors
    assert "n_unstamped_stage" in anchors
    assert "by_confidence" in anchors
    # Untouched summary neighbours.
    assert "current_phase" in payload
    assert "n_evidence_items" in payload
    assert "total_seals" in payload


# ── E1.3: mean score out of summary position ─────────────────────────────


def test_aee_summary_has_no_mean_propagated_score():
    if not _CLAIMS_DIR.exists():
        pytest.skip("extracted_claims dir not present")
    summary = assessment_summary(_CLAIMS_DIR)
    assert "mean_propagated_score" not in summary
    assert summary["total_claims"] > 0


def test_per_claim_scores_remain_in_detail_entries():
    """The score survives only as per-claim detail (E1.3): each
    entry carries its own score object (with band and propagated
    score), its falsifier, and its stage object — nothing
    program-level is averaged into a headline."""
    if not _CLAIMS_DIR.exists():
        pytest.skip("extracted_claims dir not present")
    summary = assessment_summary(_CLAIMS_DIR)
    for entry in summary["claims"]:
        score = entry["aee_score"]
        assert score is not None
        assert "propagated_score" in score
        assert "band" in score
        assert "falsification_condition" in entry
        assert "stage" in entry
        assert entry["lane1_score"] == score


# ── E1.1/E1.4: panel source purge ────────────────────────────────────────


def test_panel_source_has_no_withdrawn_constructions():
    source = _PANEL.read_text(encoding="utf-8")
    for text in WITHDRAWN_PANEL_STRINGS:
        assert text not in source, text


def test_panel_source_does_not_consume_withdrawn_fields():
    source = _PANEL.read_text(encoding="utf-8")
    for field in WITHDRAWN_DASHBOARD_FIELDS:
        assert field not in source, field
