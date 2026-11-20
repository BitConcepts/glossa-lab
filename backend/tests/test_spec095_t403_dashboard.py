"""Spec 095 T403 — researcher dashboard API tests.

The dashboard is a read model over the program's records; these
tests re-derive its headline numbers from the records themselves
(never from the dashboard's own arithmetic) and hold its refusal
set: no falsifier-less candidate, no submission-carried approver,
no automated submitter, no unresolvable evidence reference, no
unverified corpus served as explorable, no translation presented,
and the falsifier-less claims findable as a class of exactly the
recorded size.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from glossa_lab.api import researcher_dashboard as rd

BASE = "/api/v1/researcher-dashboard"
REPO = Path(__file__).resolve().parents[2]


def _ledger_claims() -> list[dict]:
    rows = [
        json.loads(line)
        for line in (REPO / "glossa-indus" / "ledger" / "claims.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    return [r for r in rows if r.get("kind") == "claim"]


def test_home_census_is_the_records_census(client):
    body = client.get(f"{BASE}/home").json()
    claims = _ledger_claims()
    assert body["census"]["claims"] == len(claims) == 998
    assert body["census"]["ledger_lines"] == 1025
    assert body["census"]["studies"] == 96
    anchors = json.loads(
        (REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json")
        .read_text(encoding="utf-8")
    )
    assert body["census"]["anchors_total"] == anchors["total"] == 287
    assert body["freshness"]["stale"] is False


def test_identifiability_six_all_not_identifiable(client):
    body = client.get(f"{BASE}/home").json()
    ident = body["identifiability"]
    assert [i["sign"] for i in ident] == ["M044", "M047", "M124", "M202", "M329", "M330"]
    assert all(i["identifiable"] is False for i in ident)
    assert all("NOT IDENTIFIABLE" in i["outcome"] for i in ident)
    by_sign = {i["sign"]: i for i in ident}
    assert "fish" in by_sign["M047"]["outcome"]
    assert "sibilant" in by_sign["M202"]["outcome"]


def test_hypotheses_hold_no_translation(client):
    body = client.get(f"{BASE}/hypotheses").json()
    assert body["translations"]["held"] == 0
    assert len(body["models"]) >= 3
    assert body["nonlinguistic_position"]["claim_id"] == (
        "farmer_sproat_witzel_2004_manual_001"
    )
    assert body["nonlinguistic_position"]["status"] == "contradicted"
    readings = {r["sign"]: r for r in body["readings"]}
    assert len(readings) == 287
    assert readings["M044"]["identifiability"]["identifiable"] is False


def test_falsifier_absent_class_is_exactly_the_gap(client):
    body = client.get(f"{BASE}/claims", params={"falsifier": "absent"}).json()
    assert body["total"] == 9
    assert {i["id"] for i in body["items"]} == set(
        body["falsifier_census"]["gap_claims"]
    )
    present = client.get(f"{BASE}/claims", params={"falsifier": "present"}).json()
    assert present["total"] == 989


def test_sign_filter_matches_both_record_name_forms(client):
    # The one claim-to-sign linkage of record names its signs
    # mahadevan:72/64/70; the anchors register names them
    # M072/M064/M070. Both forms must find the claim.
    by_m = client.get(f"{BASE}/claims", params={"sign": "M072"}).json()
    by_ref = client.get(f"{BASE}/claims", params={"sign": "mahadevan:72"}).json()
    assert by_m["total"] == by_ref["total"] >= 1
    assert "parpola_2010_dravidian_solution_manual_002" in {
        i["id"] for i in by_m["items"]
    }


def test_claim_detail_carries_lineage_and_does_not_establish(client):
    cid = "farmer_sproat_witzel_2004_manual_001"
    body = client.get(f"{BASE}/claims/{cid}").json()
    assert body["falsifier"]
    assert body["does_not_establish"]
    assert body["lineage"]["source_document"]["document_id"] == "farmer_sproat_witzel_2004"
    assert body["lineage"]["source_document"]["sha256"]
    assert body["trail"] is not None


def test_claim_export_is_the_records(client):
    cid = "farmer_sproat_witzel_2004_manual_001"
    r = client.get(f"{BASE}/claims/{cid}/export")
    assert r.status_code == 200
    assert "attachment" in r.headers["content-disposition"]
    body = r.json()
    assert body["ledger_row"]["id"] == cid
    assert body["map_claim"]["id"] == cid


def test_matrix_overview_matches_the_map(client):
    body = client.get(f"{BASE}/matrix").json()
    assert body["rows_total"] == 998
    assert body["columns_by_class"] == {
        "studies": 10, "documents": 316, "research_checks": 31, "anchors": 287,
    }


def test_corpora_canonical_verified_others_named(client):
    body = client.get(f"{BASE}/corpora").json()
    by_key = {e["key"]: e for e in body["corpora"]}
    canonical = by_key["indus_canonical_export"]
    assert canonical["identity_status"] == "verified"
    assert canonical["explorable"] is True
    # The strict V3 corpus and the Holdat layer are absent from a
    # fresh checkout by design (they live in custody / the live
    # origin tree); where a checkout carries them they verify.
    # Either way they are never explorable from this surface, and
    # an unavailable corpus always names its reason.
    for key in ("indus_v3_firestore_strict", "holdat_downloads_layer"):
        entry = by_key[key]
        assert entry["explorable"] is False
        if entry["identity_status"] == "unavailable":
            assert entry["unavailable_reason"]
        else:
            assert entry["identity_status"] == "verified"
    for entry in body["corpora"]:
        if entry["key"] != "indus_canonical_export":
            assert entry["explorable"] is False


def test_inscriptions_paged_filtered_and_layered(client):
    body = client.get(f"{BASE}/inscriptions").json()
    assert body["total"] == 15508
    assert len(body["items"]) == 50
    seals = client.get(
        f"{BASE}/inscriptions", params={"object_class": "seal", "limit": 5}
    ).json()
    assert seals["total"] == 10072
    signed = client.get(
        f"{BASE}/inscriptions", params={"sign": "145", "limit": 5}
    ).json()
    assert 0 < signed["total"] < 15508
    detail = client.get(f"{BASE}/inscriptions/GLI-IND-0000206").json()
    layers = detail["layers"]
    assert set(layers) == {"observation", "transcription", "hypothesis", "claim"}
    # The observation layer carries catalogue fields only — no
    # reading is ever blended into it.
    assert set(layers["observation"]) == {
        "glossa_id", "artifact_type", "site_name", "current_holding",
        "material", "accession_number", "image_master_uri",
        "rights_status", "source_system", "citation", "note",
    }
    assert layers["observation"]["artifact_type"] == "seal"
    readings = layers["hypothesis"]["readings_for_signs"]
    assert any(r["sign"] == "M145" for r in readings)


def test_inscriptions_unavailable_corpus_serves_nothing(client):
    body = client.get(
        f"{BASE}/inscriptions", params={"corpus": "indus_v3_firestore_strict"}
    ).json()
    assert body["total"] == 0
    assert body["items"] == []
    assert body["unavailable_reason"]


def test_results_legacy_runs_named_not_reproducible(client):
    body = client.get(f"{BASE}/results").json()
    legacy = [r for r in body["runs"] if r["legacy"]]
    assert legacy
    assert all(r["reproducible"] is False for r in legacy)
    assert all("command" in r["missing"] for r in legacy)
    assert body["settling_runs"]
    t405 = next(
        r for r in body["settling_runs"]
        if r["record"] == "settling-20261116T034814Z-3681c4"
    )
    assert t405["assigned_count"] == 94
    assert t405["consistent"] == 94


def test_rerun_of_incomplete_record_is_refused(client):
    body = client.get(f"{BASE}/results").json()
    legacy_id = next(r["run_id"] for r in body["runs"] if r["legacy"])
    r = client.post(f"{BASE}/results/{legacy_id}/rerun")
    assert r.status_code == 422
    assert "not reproducible" in r.json()["detail"]


def test_rerun_reproduces_the_t405_quantities(client):
    # The settling engine verifies its sources against the ledger
    # mirror before it runs, and the full suite regenerates the
    # extracted-claims files in-tree as a side effect (the stage
    # discipline restores them after a suite run). Restore them
    # here so this test measures the endpoint, not the suite's
    # side effects; on a quiet tree this is a no-op.
    subprocess.run(
        ["git", "-C", str(REPO), "checkout", "--", "glossa-indus/claims/extracted_claims"],
        check=False, capture_output=True,
    )
    r = client.post(f"{BASE}/results/settling-20261116T034814Z-3681c4/rerun")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["corpus_identity"] == "verified"
    assert body["quantities"]["recorded"]["assigned_count"] == 94
    assert body["quantities"]["rerun"]["assigned_count"] == 94
    assert body["quantities"]["rerun"]["consistent"] == 94
    assert "never written into a standing" in body["standing_effect"]


@pytest.fixture()
def scratch_staging(tmp_path, monkeypatch):
    staging = tmp_path / "anchor_staging.json"
    staging.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(rd, "_STAGING_PATH", staging)
    return staging


def _valid_payload() -> dict:
    return {
        "statement": "Sign M044 carries the value ku in syllabic slots.",
        "falsifier": "A positional test of record showing M044 never "
                     "occupies a syllabic slot would falsify this.",
        "submitted_by": "Test Researcher",
        "evidence_refs": ["M044"],
        "subject_sign": "M044",
        "does_not_establish": "It does not establish the language encoded.",
    }


def test_contribution_refusals(client, scratch_staging):
    no_falsifier = {k: v for k, v in _valid_payload().items() if k != "falsifier"}
    r = client.post(f"{BASE}/contributions", json=no_falsifier)
    assert r.status_code == 422
    assert "falsifier" in r.json()["detail"]

    with_approver = {**_valid_payload(), "approver": "Test Researcher"}
    r = client.post(f"{BASE}/contributions", json=with_approver)
    assert r.status_code == 422
    assert "approver" in r.json()["detail"]

    automated = {**_valid_payload(), "submitted_by": "research-loop"}
    r = client.post(f"{BASE}/contributions", json=automated)
    assert r.status_code == 422

    bad_ref = {**_valid_payload(), "evidence_refs": ["NOPE-000"]}
    r = client.post(f"{BASE}/contributions", json=bad_ref)
    assert r.status_code == 422
    assert "NOPE-000" in r.json()["detail"]

    bad_subject = {**_valid_payload(), "subject_sign": "M999"}
    r = client.post(f"{BASE}/contributions", json=bad_subject)
    assert r.status_code == 422
    # Nothing was written by any refusal.
    assert json.loads(scratch_staging.read_text(encoding="utf-8")) == []


def test_contribution_lands_in_staging_as_a_candidate(client, scratch_staging):
    r = client.post(f"{BASE}/contributions", json=_valid_payload())
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["review_status"] == "staged"
    assert body["stage"] is None  # no standing is implied by submission
    stored = json.loads(scratch_staging.read_text(encoding="utf-8"))
    assert len(stored) == 1
    rec = stored[0]
    assert rec["origin"] == "researcher-dashboard"
    assert rec["falsifier"] == _valid_payload()["falsifier"]
    assert rec["evidence_ref"] == "M044"
    assert "approver" not in rec
    listed = client.get(f"{BASE}/contributions").json()
    assert [c["contribution_id"] for c in listed["contributions"]] == [
        body["contribution_id"]
    ]
    assert "no automatic promotion" in listed["boundaries"]["promotion"]
