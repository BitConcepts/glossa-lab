"""Spec 051 execution tests (Phase-409).

The execution's terminal outcome is INCONCLUSIVE —
the classification is the finding: step 0 ran in
the frozen gate order (0.1-0.5 PASS), and gate
0.6's floors fired — no testable gateway/border
site carries M391 (floor 3) and the contrast side
of the frozen groupings is empty in the test
population — so no share was computed and the
claim stands UNTESTED. These tests pin the
delivered form: the results record's gate facts,
the Asset B digest asserted at gate 0.2 against
Spec 047's step-1 outcome record (DD-051-14), the
counting layer's exact census reproduction, the
join census accounting, the gate-0.6 census and
floors, and the claim-record append with the
claim's status and stage unchanged.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RESULTS = REPO / "reports/phase409_results.json"
ASSET_B = (REPO / "specs/047-roif-ledger-distribution/"
           "asset-b/site-functions.jsonl")
CLAIM_FILE = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "indus_valley_script_deciphered_from_myth_"
    "65ff0a26.json")
CLAIM_ID = ("indus_valley_script_deciphered_from_myth_"
            "65ff0a26_manual_003")
ASSET_B_SHA256 = (
    "a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d7"
    "7d2e5739c9f85")
LAYER_SHA256 = (
    "62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f"
    "7f40cbe28218e")
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e608"
    "6592b32d34f569")
CENSUS = {
    "Mohenjo-daro": 75, "Harappa": 52, "Dholavira": 16,
    "Lothal": 14, "Surkotada": 11, "Kalibangan": 10,
    "Chanhu-daro": 10, "Banawali": 3, "Rakhigarhi": 2,
}


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def _claim_entry() -> dict:
    doc = json.loads(CLAIM_FILE.read_text(encoding="utf-8"))

    def find(node):
        if isinstance(node, dict):
            if node.get("claim_id") == CLAIM_ID:
                return node
            for value in node.values():
                hit = find(value)
                if hit is not None:
                    return hit
        elif isinstance(node, list):
            for value in node:
                hit = find(value)
                if hit is not None:
                    return hit
        return None

    entry = find(doc)
    assert entry is not None
    return entry


def _gate(rec: dict, gate: str) -> dict:
    return {g["gate"]: g for g in rec["gates"]}[gate]


def test_results_record_outcome_and_gates():
    rec = _results()
    assert rec["phase"] == 409
    assert rec["spec"] == "051-roif-arrow-sign"
    assert rec["claim_id"] == CLAIM_ID
    assert rec["outcome"] == (
        "INCONCLUSIVE — THE CLASSIFICATION IS THE FINDING")
    assert rec["freeze_digest"] == (
        "818cfa4ecd32d286dbe0fcc8d73f4a79f42610f181e5f19594d"
        "057a32dab64b1")
    for gate in ("0.1", "0.2", "0.3", "0.4", "0.5"):
        assert _gate(rec, gate)["verdict"] == "PASS", gate
    assert _gate(rec, "0.6")["verdict"] == (
        "INCONCLUSIVE — THE CLASSIFICATION IS THE FINDING")
    assert rec["anchors_assertion"]["byte_identical"] is True
    assert rec["anchors_assertion"]["before_sha256"] == (
        ANCHORS_SHA256)
    # No share quantity exists anywhere in the record.
    text = RESULTS.read_text(encoding="utf-8")
    assert '"primary_ratio"' not in text
    assert '"permutation"' not in text


def test_gate_02_asset_b_digest():
    rec = _results()
    g = _gate(rec, "0.2")
    assert g["observed_sha256"] == ASSET_B_SHA256
    assert g["pin_source_digest"] == ASSET_B_SHA256
    assert g["digest_present_in_pin_source"] is True
    assert hashlib.sha256(
        ASSET_B.read_bytes()).hexdigest() == ASSET_B_SHA256
    assert rec["asset_b"]["rows"] == 30
    assert rec["asset_b"]["status_counts"] == {
        "AGREED": 3, "DISAGREED": 1,
        "NO-SOURCE": 16, "SINGLE-SOURCE": 10}
    assert rec["asset_b"]["testable_count"] == 2
    assert {t["program_site_id"]
            for t in rec["asset_b"]["testable_sites"]} == {
        "harappa", "lothal"}


def test_gate_04_census_reproduction():
    rec = _results()
    layer = rec["counting_layer"]
    assert layer["sha256"] == LAYER_SHA256
    assert layer["token_rows"] == 7002
    assert layer["inscriptions"] == 1670
    assert layer["m391_census_reproduced"] is True
    observed = {site: v["m391_occurrences"]
                for site, v in layer["per_site"].items()}
    assert observed == CENSUS
    assert layer["per_site"]["Harappa"]["inscriptions"] == 492
    assert layer["per_site"]["Lothal"]["inscriptions"] == 124


def test_gate_05_join_census():
    rec = _results()
    join = rec["join_census"]
    assert join["accounted_exactly_once"] is True
    assert join["total_records"] == 7002
    assert (join["joined_records"]
            + join["non_spine_records"]
            + join["no_site_value_records"]) == 7002
    assert join["no_site_value_records"] == 0
    non_spine = {e["site_as_in_layer"]: e["m391_occurrences"]
                 for e in join["non_spine_sites"]}
    assert non_spine == {"Chanhu-daro": 10, "Dholavira": 16,
                         "Rakhigarhi": 2}
    assert join["non_spine_m391_total"] == 28


def test_gate_06_floors():
    rec = _results()
    pop = rec["test_population_census"]
    floors = pop["floors"]
    assert floors["gateway_border_sites_carrying_m391"] == 0
    assert floors["gateway_floor"] == 3
    assert floors["gateway_floor_pass"] is False
    assert floors["pooled_side_non_empty"] is True
    assert floors["contrast_side_non_empty"] is False
    per_class = pop["per_class"]
    assert per_class["administrative"]["testable_sites"] == 1
    assert per_class["port/trade"]["testable_sites"] == 1
    assert per_class["gateway/border"]["testable_sites"] == 0
    assert per_class["domestic"]["testable_sites"] == 0
    assert per_class["ritual"]["testable_sites"] == 0
    sites = {t["program_site_id"]: t
             for t in pop["test_population"]}
    assert sites["harappa"]["m391_occurrences"] == 52
    assert sites["harappa"]["joined_inscriptions"] == 492
    assert sites["lothal"]["m391_occurrences"] == 14
    assert sites["lothal"]["joined_inscriptions"] == 124
    # The excluded list names every non-testable row.
    assert len(pop["excluded_sites"]) == 28


def test_claim_record_append():
    entry = _claim_entry()
    # The frozen record stands: status and stage unchanged.
    assert entry["claim_status"] == "untested"
    assert entry["stage"] == "created"
    append = entry["spec051_execution"]
    assert append["spec"] == "051"
    assert append["phase"] == "Phase-409"
    assert append["date"] == "2026-10-21"
    assert append["outcome"] == (
        "INCONCLUSIVE — THE CLASSIFICATION IS THE FINDING")
    assert append["record"] == (
        "specs/051-roif-arrow-sign/outcome.md")
    assert append["asset_b_sha256"] == ASSET_B_SHA256
