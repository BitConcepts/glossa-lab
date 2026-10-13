"""Phase-396 (Spec 032) build-machinery fences.

Pins: (1) step 0.1 — the classification recomputed from the
recorded training corpus reproduces the recorded
global_class_stability output exactly, and the frozen
trained INITIAL set is the recorded 12 signs; (2) step 0.2
— the recorded training corpus's composition reproduces
(2,722 rows; 179 CISI rows, Mohenjo-daro only; 2,543
Yajnadevam rows, of which 970 are Harappa, carrying 1,013
occurrences of 11 of the 12 trained signs), so the
withholding check fails and the study closes as CANNOT BE
RUN AS WRITTEN at check 3.2, with 3.3 not reached and no
scoring run; (3) the registered scoring machinery behaves
on synthetic fixtures with known structure (share, the
0.40 bar, the 70 percent verdict mapping, unmappable
handling and its first-sentence coverage rule, conflict
flags) — the pipeline a passed step 0 would have run.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "backend" / "scripts"
sys.path.insert(0, str(REPO / "backend"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p396 = _load("phase396_pred006_step0")

TRAINED_INITIAL = [
    "P000", "P001", "P004", "P013", "P051", "P098",
    "P217", "P238", "P265", "P301", "P310", "P324",
]


def test_step0_1_reproduces_recorded_classification():
    records = p396.load_corpus_master()
    recorded = json.loads(p396.STABILITY_JSON.read_text(encoding="utf-8"))
    result = p396.check_3_1_trained_set(records, recorded)
    assert result["status"] == "pass"
    assert result["maps_identical"] is True
    assert result["trained_initial_set"] == TRAINED_INITIAL
    assert result["trained_initial_set_size"] == 12


def test_step0_2_withholding_fails_on_the_record():
    records = p396.load_corpus_master()
    result = p396.check_3_2_withholding(records, TRAINED_INITIAL)
    assert result["status"] == "fail"
    assert result["training_corpus_rows"] == 2722
    assert result["cisi_rows_sites"] == {"Mohenjo-daro": 179}
    assert result["yajnadevam_rows_in_training_corpus"] == 2543
    assert result["yajnadevam_harappa_rows_in_training_corpus"] == 970
    occ = result["trained_sign_occurrences_inside_yajnadevam_harappa"]
    assert occ["P324"] == 468
    assert occ["P098"] == 254
    assert occ["P000"] == 0
    assert result["trained_signs_present_inside_yajnadevam_harappa"] == 11
    assert result["total_trained_sign_occurrences_inside_yajnadevam_harappa"] == 1013
    assert result["fact_part_1_assignments_from_cisi_mohenjo_daro_only"] is False
    assert result["fact_part_2_harappa_yajnadevam_played_no_part"] is False
    assert result["failure_outcome"] == "CANNOT BE RUN AS WRITTEN"


def test_run_step0_closes_at_3_2_without_scoring():
    result = p396.run_step0()
    assert result["step0"]["check_3_1"]["status"] == "pass"
    assert result["step0"]["check_3_2"]["status"] == "fail"
    assert result["step0"]["check_3_3"] == {"status": "not_reached"}
    assert result["outcome"] == {
        "type": "step0_closure",
        "closure": "CANNOT BE RUN AS WRITTEN",
        "failed_check": "3.2",
        "scoring_run": False,
    }


def _fixture_crosswalk():
    return {
        "PA": {"glyph_ids": ["Y1"], "conflict": False},
        "PB": {"glyph_ids": ["Y2"], "conflict": True},
        "PC": {"glyph_ids": ["Y3"], "conflict": False},
        # PD deliberately absent: unmappable.
    }


def test_scoring_share_and_verdict_confirmed():
    trained = ["PA", "PB", "PC", "PD"]
    sequences = (
        [["Y1", "GX"]] * 5 + [["GX", "Y1"]] * 5      # PA: 10 occ, 5 init
        + [["Y2", "GX"]] * 3 + [["GX", "Y2"]] * 7    # PB: 10 occ, 3 init
        + [["Y3", "GX"]] * 1 + [["GX", "Y3"]] * 3    # PC: 4 occ, 1 init
    )
    out = p396.score_registered_test(trained, _fixture_crosswalk(), sequences)
    table = {row["sign"]: row for row in out["per_sign_table"]}
    # PA: 10 occurrences, 5 initial -> 0.50 meets the bar.
    assert table["PA"]["harappa_occurrences"] == 10
    assert table["PA"]["initial_occurrences"] == 5
    assert table["PA"]["start_rate"] == 0.5
    assert table["PA"]["meets_bar"] is True
    # PB: 10 occurrences, 3 initial -> 0.30, below the bar.
    assert table["PB"]["harappa_occurrences"] == 10
    assert table["PB"]["start_rate"] == 0.3
    assert table["PB"]["meets_bar"] is False
    assert table["PB"]["crosswalk_conflict"] is True
    # PC: 4 occurrences, 1 initial -> 0.25, below the bar.
    assert table["PC"]["harappa_occurrences"] == 4
    assert table["PC"]["start_rate"] == 0.25
    assert table["PC"]["meets_bar"] is False
    # PD: unmappable, no occurrences, never meets the bar.
    assert table["PD"]["unmappable"] is True
    assert table["PD"]["start_rate"] is None
    assert table["PD"]["meets_bar"] is False
    assert out["signs_meeting_bar"] == 1
    assert out["share"] == 0.25
    assert out["verdict"] == "NOT CONFIRMED"
    assert out["unmappable_share"] == 0.25
    assert out["unmappable_coverage_leads_verdict"] is True


def test_scoring_verdict_confirmed_at_threshold():
    trained = [f"S{i}" for i in range(10)]
    crosswalk = {
        s: {"glyph_ids": [f"G{i}"], "conflict": False}
        for i, s in enumerate(trained)
    }
    sequences = []
    for i, s in enumerate(trained):
        g = f"G{i}"
        if i < 7:  # 7 signs always initial -> start rate 1.0
            sequences += [[g, "GX"], [g, "GX"]]
        else:  # 3 signs never initial -> start rate 0.0
            sequences += [["GX", g], ["GX", g]]
    out = p396.score_registered_test(trained, crosswalk, sequences)
    assert out["signs_meeting_bar"] == 7
    assert out["share"] == 0.7
    assert out["verdict"] == "CONFIRMED"
    assert out["unmappable_signs"] == 0
    assert out["unmappable_coverage_leads_verdict"] is False
