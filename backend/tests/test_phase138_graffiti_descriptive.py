"""Phase-138 (spec 024, FROZEN Stage 2(d)) — descriptive consistency pins.

These tests validate the COMMITTED results JSON
(reports/phase138_results.json) for internal consistency, so they
pass in CI where the local store (the script's inputs) does NOT
exist. The one recomputation test skips cleanly when the inputs
are absent (Phase-133 pattern).

Descriptive-only discipline (freeze §4): the results JSON must
contain NO p-value or test-statistic keys anywhere; the mandatory
statements of freeze §3 must be present; the anchors file must be
byte-unchanged.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_RESULTS = _REPO / "reports" / "phase138_results.json"
_REPORT = _REPO / "reports" / "phase138_report.md"
_SCRIPT = _REPO / "backend" / "scripts" / \
    "phase138_graffiti_descriptive.py"
_ANCHORS = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)

FORBIDDEN_KEYS = {
    "p_value", "p-value", "pvalue", "p", "test_statistic",
    "chi_square", "chi2", "t_statistic", "z_score", "f_statistic",
    "significance", "significant", "cohens_kappa", "kappa",
    "correlation", "effect_size",
}

_spec = importlib.util.spec_from_file_location(
    "phase138_graffiti_descriptive", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _res():
    return json.loads(_RESULTS.read_text("utf-8"))


def _all_keys(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield key
            yield from _all_keys(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from _all_keys(item)


def test_results_exist_and_parse():
    assert _RESULTS.exists()
    res = _res()
    assert res["phase"] == "Phase-138"
    assert res["family_role"] == "none (descriptive only)"
    assert res["descriptive_only"] is True
    assert len(res["inputs"]) == 2
    for entry in res["inputs"]:
        assert len(entry["sha256"]) == 64


def test_population_sums_across_volumes():
    res = _res()
    pop = res["population"]
    by_vol = pop["by_volume"]
    assert set(by_vol) == {"1", "2"}
    assert pop["rows_total"] == sum(
        d["rows"] for d in by_vol.values())
    assert pop["distinct_objects_total"] == sum(
        d["distinct_objects"] for d in by_vol.values())
    # design-audit expectation recorded in the freeze §1
    assert pop["rows_total"] == 417
    assert pop["distinct_objects_total"] == 395
    assert by_vol["1"]["rows"] == 119
    assert by_vol["2"]["rows"] == 298


def test_site_tables_sum_to_distinct_objects():
    res = _res()
    sections = [res["graffiti"]["pooled"],
                *res["graffiti"]["by_volume"].values()]
    sections += list(
        res["context_table"]["by_object_type"].values())
    for entry in res["context_table"]["by_object_type"].values():
        sections += list(entry["by_volume"].values())
    for section in sections:
        total = sum(e["distinct_objects"]
                    for e in section["distinct_objects_by_site"])
        assert total == section["distinct_objects"], section
        no_site = [e for e in section["distinct_objects_by_site"]
                   if e["site"] == ""]
        # a section with no no-site objects (e.g. Tablets Vol. 2)
        # carries no empty-site entry; its count must then be 0
        assert len(no_site) <= 1
        if no_site:
            assert no_site[0]["distinct_objects"] == \
                section["no_site_count"]
        else:
            assert section["no_site_count"] == 0
    # pooled site counts equal the sum of the by-volume counts
    pooled = {e["site"]: e["distinct_objects"] for e in
              res["graffiti"]["pooled"][
                  "distinct_objects_by_site"]}
    summed: dict[str, int] = {}
    for vol in res["graffiti"]["by_volume"].values():
        for e in vol["distinct_objects_by_site"]:
            summed[e["site"]] = summed.get(e["site"], 0) + \
                e["distinct_objects"]
    assert pooled == summed


def test_rows_per_object_distributions_sum():
    res = _res()
    sections = [res["graffiti"]["pooled"],
                *res["graffiti"]["by_volume"].values()]
    for entry in res["context_table"]["by_object_type"].values():
        sections.append(entry)
        sections += list(entry["by_volume"].values())
    for section in sections:
        dist = section["rows_per_object_distribution"]
        assert sum(dist.values()) == section["distinct_objects"]
        weighted = sum(int(k) * v for k, v in dist.items())
        assert weighted == section["rows"]


def test_value_counts_sum_to_rows():
    res = _res()
    for section in [res["graffiti"]["pooled"],
                    *res["graffiti"]["by_volume"].values()]:
        assert sum(e["count"] for e in
                   section["side_value_counts"]) == section["rows"]
        assert sum(e["count"] for e in
                   section["bis_value_counts"]) == section["rows"]
        motif = section["motif_chapter"]
        assert motif["total_rows"] == section["rows"]
        assert motif["filled_rows"] == sum(
            e["count"] for e in motif["distinct_values"])
        assert abs(motif["filled_rate"]
                   - motif["filled_rows"] / motif["total_rows"]) < 1e-12
        assert "Class C" in motif["field_class"]


def test_no_test_or_pvalue_keys_anywhere():
    keys = {k.lower() for k in _all_keys(_res())}
    assert not (keys & FORBIDDEN_KEYS), keys & FORBIDDEN_KEYS


def test_mandatory_statements_present():
    res = _res()
    joined = " ".join(res["mandatory_statements"])
    assert "not in hand" in joined and "0 records" in joined
    assert "2026-10-08" in joined
    assert "≥ 1,000 years" in joined
    assert "resemblance described" in joined
    assert "continuity" in joined and "descent" in joined \
        and "survival" in joined
    assert "no machine-readable sign-form repertoire" in \
        res["no_overlap_statistic_reason"]
    report = _REPORT.read_text("utf-8")
    for fragment in ("not in hand", "0 records", "≥ 1,000 years",
                     "resemblance described"):
        assert fragment in report, fragment


def test_median_iqr_unit():
    out = _mod.median_iqr([1.0, 2.0, 3.0, 4.0])
    assert out["present_count"] == 4
    assert out["median"] == 2.5
    assert out["q1"] == 1.75
    assert out["q3"] == 3.25
    assert out["iqr"] == 1.5
    single = _mod.median_iqr([7.0])
    assert single["median"] == 7.0 and single["iqr"] == 0.0
    empty = _mod.median_iqr([])
    assert empty["present_count"] == 0 and empty["median"] is None


def test_numeric_descriptors_present_counts():
    res = _res()
    for section in [res["graffiti"]["pooled"],
                    *res["graffiti"]["by_volume"].values()]:
        for field, desc in section["numeric_descriptors"].items():
            assert 0 <= desc["present_count"] <= section["rows"]
            if desc["present_count"]:
                assert desc["q1"] <= desc["median"] <= desc["q3"]
                assert abs(desc["iqr"]
                           - (desc["q3"] - desc["q1"])) < 1e-9


def test_context_table_labelled_not_repertoire_comparison():
    label = _res()["context_table"]["label"].lower()
    assert "catalogue-composition" in label
    assert "not a comparison of repertoires" in label
    assert "never pooled" in label


def test_anchors_sha256_unchanged():
    digest = hashlib.sha256(_ANCHORS.read_bytes()).hexdigest()
    assert digest == _ANCHORS_SHA256


def test_report_exists_and_carries_caveats():
    text = _REPORT.read_text("utf-8")
    assert "Phase-138" in text
    assert _ANCHORS_SHA256 in text
    assert "publication-selection" in text
    assert "225" in text and "175" in text  # Kodumanal inconsistency
    assert "Deviations" in text


def test_graph_node_registered():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase138GraffitiDescriptive" in ATOMIC_NODES


def test_recomputation_skips_without_inputs():
    """Recompute into a temp file iff the local store exists."""
    store = Path.home() / "workspace" / "glossa-lab" / "corpora" / \
        "downloads" / "cisi_image_layer" / "catalogue" / \
        "cisi_vol1_catalogue.csv"
    if not store.exists():
        pytest.skip("local store absent (CI): script inputs are "
                    "local-only by design")
    out = Path("/tmp/phase138_recomputed.json")
    r = subprocess.run(
        [sys.executable, str(_SCRIPT), "--out", str(out)],
        capture_output=True, text=True, timeout=600,
        cwd=str(_REPO))
    assert r.returncode == 0, r.stderr[-500:]
    recomputed = json.loads(out.read_text("utf-8"))
    committed = _res()
    assert recomputed["population"] == committed["population"]
    assert recomputed["graffiti"] == committed["graffiti"]
    assert recomputed["context_table"] == committed["context_table"]
    assert [i["sha256"] for i in recomputed["inputs"]] == \
        [i["sha256"] for i in committed["inputs"]]
