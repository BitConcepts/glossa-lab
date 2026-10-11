"""Spec 028 freeze fences (Phase-393).

Pins: (1) the margins audit contains NO outcome field
anywhere (the Phase-139 no-peeking pattern); (2) the frozen
margins are exactly the audit's; (3) the synthetic
calibration passed both arms' controls under the final
(Amendment 1) design and computed no real outcome; (4) the
freeze doc carries the design constants; (5) the machine
freeze record replays (framework026 verify_freeze).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/028-harappa-robustness"
AUDIT = SPEC / "margins-audit.json"
CALIB = SPEC / "calibration.json"
FREEZE_MD = SPEC / "freeze.md"
FREEZE_JSON = SPEC / "freeze.json"

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
    assert audit["sign_columns"] == 125
    assert audit["analysis_population"]["records"] == 3030
    a = audit["arm_a_harappa_excluded"]
    assert a["records"] == 1593
    assert a["n_cells_included"] == 6
    assert a["inscriptions_per_draw"] == 294
    assert a["cells_included_ge49"] == {
        "Chanhu-daro|SEAL": 52, "Dholavira|SEAL": 96,
        "Kalibangan|SEAL": 49, "Lothal|SEAL": 72,
        "Mohenjo-daro|SEAL": 1138, "Mohenjo-daro|TAB": 164}
    assert a["s_complete_records"] == 1303
    assert all(v["cells_ge_cell"] >= 4
               for v in a["loso_support"].values())
    b = audit["arm_b_site_equal"]
    assert b["quota_per_site"] == 52
    assert b["quota_is_min_site_total"] is True
    assert b["inscriptions_per_draw"] == 312
    assert all(b["loso_quota_feasible"].values())
    assert audit["arm_c_harappa_counts"]["records"] == 1437


def test_calibration_passed_and_is_synthetic_only():
    calib = json.loads(CALIB.read_text(encoding="utf-8"))
    assert calib["real_outcomes_computed"] is False
    assert calib["seed"] == 20261012
    for arm in ("arm_a", "arm_b"):
        assert calib[arm]["negative_control"]["pass"] is True
        assert calib[arm]["positive_control"]["pass"] is True
        neg = calib[arm]["negative_control"]
        assert neg["median_adj_r2"] < 0.01
        # Amendment 1 part 3 frozen bound (binomial tolerance
        # for 199 independent regenerated worlds).
        assert neg["share_draws_rejecting"] <= 0.10
        pos = calib[arm]["positive_control"]
        assert pos["share_draws_rejecting"] >= 0.95
        assert pos["adj_r2_interval_95"][0] > 0.01


def test_freeze_doc_carries_the_design_constants():
    text = FREEZE_MD.read_text(encoding="utf-8")
    for needle in ("n_cell = 49", "Q = 52", "20261012", "199",
                   "499", "0.01", "regenerated per draw",
                   "Amendment 1", "1,593", "3,030", "3,144",
                   "INCONCLUSIVE", "NOT ESTIMABLE"):
        assert needle in text, needle


def test_freeze_record_replays():
    sys.path.insert(0, str(REPO / "backend"))
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["definition"]["phase"] == 393
    assert verify_freeze(record, REPO) == []
