"""Phase-133 (spec 024, FROZEN Stage 0) — inventory consistency pins.

These tests validate the COMMITTED inventory JSON
(data/evidence_integration/phase133_stage0_inventory.json) for
internal consistency, so they pass in CI where the local store
(the builder's inputs) does NOT exist. The one recomputation
test skips cleanly when the builder inputs are absent.

Facts-only discipline (spec section 3.1): the inventory carries
coverage and joinability only; these tests also pin that the
prohibited key was never joined on, that the Class I exclusion
list is present and names the fields the spec requires, and
that the anchors file is byte-unchanged.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_INVENTORY = (_REPO / "data" / "evidence_integration"
              / "phase133_stage0_inventory.json")
_META = (_REPO / "data" / "evidence_integration"
         / "phase133_stage0_inventory_meta.json")
_REPORT = _REPO / "reports" / "phase133_stage0_report.md"
_BUILDER = _REPO / "backend" / "scripts" / \
    "phase133_stage0_inventory.py"
_ANCHORS = _REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)

EXPECTED_LAYERS = {
    "cisi_vol1_catalogue": 3320,
    "cisi_vol2_catalogue": 4385,
    "holdat_indus_corpus": 7002,
    "holdat_symbol_semantic_roles": 151,
    "mayig_cisi_layer": 179,
    "mayig_source_corpus": 179,
    "horus84_inscriptions": 5679,
    "museum_met_indus": 28,
    "museum_cleveland_indus_search": 10,
}


def _inv():
    return json.loads(_INVENTORY.read_text("utf-8"))


def test_inventory_and_meta_exist_and_parse():
    assert _INVENTORY.exists()
    assert _META.exists()
    inv = _inv()
    meta = json.loads(_META.read_text("utf-8"))
    assert inv["phase"] == "Phase-133"
    assert meta["dataset_name"] == "phase133_stage0_inventory"
    assert meta["license_basis_per_layer"], "license basis required"
    assert set(meta["license_basis_per_layer"]) == {
        layer["layer_id"] for layer in inv["layers"]}


def test_layer_row_counts():
    inv = _inv()
    by_id = {layer["layer_id"]: layer for layer in inv["layers"]}
    assert set(by_id) == set(EXPECTED_LAYERS)
    for layer_id, expected in EXPECTED_LAYERS.items():
        assert by_id[layer_id]["row_count"] == expected, layer_id


def test_coverage_matrix_internal_consistency():
    inv = _inv()
    matrix = inv["coverage_matrix"]
    assert matrix, "coverage matrix must not be empty"
    layer_rows = {(layer["layer_id"], layer["row_count"])
                  for layer in inv["layers"]}
    for row in matrix:
        assert (row["layer"], row["row_count"]) in layer_rows
        assert 0 <= row["filled_count"] <= row["row_count"]
        assert 0.0 <= row["filled_rate"] <= 1.0
        expected_rate = (row["filled_count"] / row["row_count"]
                         if row["row_count"] else 0.0)
        assert abs(row["filled_rate"] - expected_rate) < 1e-6
        assert row["provenance_grade"] in {"O", "C", "I"}
        assert row["grade_reason"], "every field needs a reason"
        assert row["distinct_value_count"] >= 0
        counts = [t["count"] for t in row["top_values"]]
        assert counts == sorted(counts, reverse=True)
        assert len(row["top_values"]) <= 5
    # the flat matrix is exactly the layers' field rows
    assert len(matrix) == sum(len(layer["fields"])
                              for layer in inv["layers"])


def test_coverage_row_sums_for_key_fields():
    inv = _inv()
    fields = {(r["layer"], r["field"]): r
              for r in inv["coverage_matrix"]}
    assert fields[("cisi_vol1_catalogue", "material")][
        "filled_count"] == 0
    assert fields[("cisi_vol2_catalogue", "dimensions")][
        "filled_count"] == 0
    motif_total = sum(
        fields[(f"cisi_vol{v}_catalogue", "motif_chapter")][
            "filled_count"] for v in (1, 2))
    assert motif_total == 2005
    assert fields[("holdat_indus_corpus", "site")][
        "filled_rate"] == 1.0
    assert fields[("holdat_indus_corpus", "iconography")][
        "filled_rate"] == 1.0
    assert fields[("horus84_inscriptions", "site")][
        "filled_count"] == 5679


def test_join_key_audit_sections_and_results():
    ja = _inv()["join_key_audit"]
    for section in ("canonical_cisi_key", "mayig_cisi_object_id",
                    "horus84_cisi", "holdat_cisi_number",
                    "holdat_seal_id", "museum_cross_references",
                    "within_volume_duplicate_printed_ids"):
        assert section in ja, section
    assert ja["distinct_objects_vol1"] == 1475
    assert ja["distinct_objects_vol2"] == 2019
    assert ja["distinct_volume_scoped_objects"] == 3494
    assert ja["printed_ids_present_in_both_volumes"] == ["H-311"]
    mayig = ja["mayig_cisi_object_id"]
    total = (mayig["matched_single_volume"]
             + mayig["ambiguous_present_in_both_volumes"]
             + mayig["unmatched"])
    assert total == mayig["n_values_tested"] == 179
    assert mayig["matched_single_volume"] == 179
    assert mayig["ambiguous_present_in_both_volumes"] == 0
    assert mayig["unmatched"] == 0
    horus = ja["horus84_cisi"]
    rows = horus["rows"]
    assert (rows["matched_single_volume"]
            + rows["ambiguous_present_in_both_volumes"]
            + rows["unmatched"]) == horus["n_rows_tested"] == 5679
    assert rows["matched_single_volume"] == 2895
    assert rows["ambiguous_present_in_both_volumes"] == 2
    assert rows["unmatched"] == 2782
    assert "NOT USABLE" in horus["verdict"]


def test_holdat_cisi_number_prohibited_and_never_joined():
    detail = _inv()["join_key_audit"]["holdat_cisi_number"]
    assert "PROHIBITED" in detail["status"]
    exact = detail["exact_string_match_to_a_catalogue_printed_id"]
    assert exact["token_rows"] == 0
    assert exact["distinct_values"] == 0
    seal = _inv()["join_key_audit"]["holdat_seal_id"]
    assert seal["n_distinct_seal_ids"] == 1670
    assert sum(seal["rows_per_id_distribution"].values()) == 1670
    # rows-per-id distribution accounts for every token row
    weighted = sum(int(k) * v for k, v in
                   seal["rows_per_id_distribution"].items())
    assert weighted == 7002


def test_museum_census_no_cross_references():
    census = _inv()["join_key_audit"]["museum_cross_references"]
    assert census["total_with_cisi_cross_reference"] == 0
    assert census["total_records_censused"] == 40


def test_provenance_grading_and_class_i_list():
    grading = _inv()["provenance_grading"]
    assert grading["class_i_count"] == len(grading["class_i_fields"])
    assert grading["class_i_count"] > 0
    class_i = {(g["layer"], g["field"])
               for g in grading["class_i_fields"]}
    required = {
        ("holdat_indus_corpus", "morpheme boundary"),
        ("holdat_indus_corpus", "noun"),
        ("holdat_indus_corpus", "verb"),
        ("holdat_indus_corpus", "upos"),
        ("holdat_indus_corpus", "xpos"),
        ("holdat_symbol_semantic_roles", "semantic_role"),
        ("horus84_inscriptions", "sanskrit"),
        ("horus84_inscriptions", "translation"),
    }
    assert required <= class_i
    counts = grading["counts"]
    assert set(counts) == {"O", "C", "I"}
    assert sum(counts.values()) == len(
        grading["grades_by_layer_field"])


def test_mayig_parseability_counts_sum():
    p = _inv()["mayig_description_parseability"]
    assert p["n_descriptions"] == 179
    assert p["with_both"] + 0 <= p["n_descriptions"]
    assert (p["with_at_least_one_motif_term"]
            + p["with_at_least_one_object_type_term"]
            - p["with_both"] + p["with_neither"]
            == p["n_descriptions"])
    assert p["motif_term_list"], "rule terms must be recorded"
    assert p["object_type_term_list"]


def test_drift_table_and_anomalies_present():
    inv = _inv()
    verdicts = {row["verdict"] for row in
                inv["appendix_a_drift_table"]}
    assert "MATCH" in verdicts
    assert any(v.startswith("DRIFT") for v in verdicts)
    horus_fields = [r for r in inv["appendix_a_drift_table"]
                    if r["item"] == "horus84 fields"]
    assert horus_fields and horus_fields[0]["measured_value"] == 38
    anomaly_ids = {a["id"] for a in inv["anomalies"]}
    assert "holdatllc_seal_catalog_content_mismatch" in anomaly_ids
    finding = [a for a in inv["anomalies"]
               if a["id"] ==
               "holdatllc_seal_catalog_content_mismatch"][0]
    assert "Ollama" in finding["finding"]
    assert finding["model_names_listed"], "models listed as found"
    assert len(inv["non_machine_readable_pass"]) == 3


def test_anchors_sha256_unchanged():
    digest = hashlib.sha256(_ANCHORS.read_bytes()).hexdigest()
    assert digest == _ANCHORS_SHA256


def test_report_exists_and_states_no_publication():
    text = _REPORT.read_text("utf-8")
    assert "Stage 0" in text
    assert _ANCHORS_SHA256 in text
    assert "NOT USABLE" in text


def test_graph_node_registered():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase133Stage0Inventory" in ATOMIC_NODES


def test_builder_recomputation_skips_without_inputs():
    """Recompute into a temp dir iff the local store exists."""
    store = Path.home() / "workspace" / "glossa-lab" / "corpora" / \
        "downloads" / "cisi_image_layer" / "catalogue" / \
        "cisi_vol1_catalogue.csv"
    if not store.exists():
        pytest.skip("local store absent (CI): builder inputs "
                    "are local-only by design")
    out = Path("/tmp/phase133_recomputed.json")
    meta = Path("/tmp/phase133_recomputed_meta.json")
    r = subprocess.run(
        [sys.executable, str(_BUILDER), "--out", str(out),
         "--meta-out", str(meta)],
        capture_output=True, text=True, timeout=1200,
        cwd=str(_REPO))
    assert r.returncode == 0, r.stderr[-500:]
    recomputed = json.loads(out.read_text("utf-8"))
    committed = _inv()
    assert recomputed["coverage_matrix"] == \
        committed["coverage_matrix"]
    assert recomputed["join_key_audit"] == \
        committed["join_key_audit"]
