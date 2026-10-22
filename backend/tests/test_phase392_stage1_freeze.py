"""Spec 027 Stage 1 freeze fences (Phase-392).

Pins: (1) the margins audit contains NO outcome field anywhere
(the Phase-139 no-peeking pattern); (2) the frozen margins the
Stage 1 design relies on are exactly the audit's; (3) the
frozen design constants in stage1-freeze.md match the audit's
cell table.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
AUDIT = (REPO / "specs/027-movement-culture-language/stage1"
         / "margins-audit.json")
FREEZE_MD = REPO / "specs/027-movement-culture-language/stage1-freeze.md"

FORBIDDEN_KEYS = {
    "r_squared", "r2", "permanova", "pseudo_f", "p_value",
    "pvalue", "divergence", "association", "verdict", "chi_square",
    "tv_distance", "effect_size",
}


def _all_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _all_keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _all_keys(v)


def test_margins_audit_has_no_outcome_fields():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["outcome_fields_present"] is False
    keys = {k.lower() for k in _all_keys(audit)}
    assert not (keys & FORBIDDEN_KEYS), keys & FORBIDDEN_KEYS


def test_frozen_margins_match_audit():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    flow = audit["population_flow"]
    assert flow["layer_records"] == 5679
    assert flow["after_dedup_kept"] == 4531
    assert flow["excluded_site_unknown"] == 26
    assert flow["seal_tab"] == 3605
    assert flow["eligible_primary"] == 3144
    assert audit["eligible_sites"] == 52
    per_site = audit["per_site"]
    analysis = {s: v["inscriptions"] for s, v in per_site.items()
                if v["inscriptions"] >= 20}
    assert analysis == {
        "Harappa": 1437, "Mohenjo-daro": 1302, "Dholavira": 111,
        "Lothal": 74, "Chanhu-daro": 54, "Kalibangan": 52}
    assert sum(analysis.values()) == 3030
    assert audit["distinct_m_signs_mapped"] == 271
    assert audit["signs_ge10_tokens"] == 123
    cov = audit["crosswalk_sensitivity_token_coverage"]
    assert cov["share_unambiguous"] < 0.20  # NOT ESTIMABLE basis


def test_freeze_doc_carries_the_design_constants():
    text = FREEZE_MD.read_text(encoding="utf-8")
    for needle in ("n_cell = 49", "R = 199", "B = 499",
                   "20261011", "0.01", "NOT ESTIMABLE", "adjusted",
                   "M77 governs", "3,144", "3,030"):
        assert needle in text, needle
