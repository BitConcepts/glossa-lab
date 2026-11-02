"""Spec 086 Stage 5 (T502/T503) — the map builder and its API.

The builder tests pin the artifact's contract on the real tree
(the header exactly as Q3 approved it, the edge-citation rule,
the honest empty states) and its refusal modes (a stale matrix,
a run pinned to another ledger build). The API tests pin the
surface's contract: the published artifact served exactly, and
the C086-19 scoping oracle — an actor without an indus-script
role receives the scoped 404 and no element of the map.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path

import pytest

from glossa_lab import ledger_intake as li
from glossa_lab import map_generate as mp

ROOT = Path(__file__).resolve().parents[2]
PARPOLA = "parpola_2010_dravidian_solution_manual_002"
YADAV = "yadav_2009_arxiv_manual_002"
GOVERNING_PTR = (
    "glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json:"
    "yadav_2009_arxiv_manual_002#spec054_outcome_append_2026_10_25"
)


@pytest.fixture(scope="module")
def built():
    return mp.build_map(ROOT)


def test_builder_is_deterministic_and_matches_the_published(
    built,
) -> None:
    again = mp.build_map(ROOT)
    assert again.json_bytes == built.json_bytes
    published = (ROOT / mp.MAP_REL).read_bytes()
    assert built.json_bytes == published


def test_header_contract_q3(built) -> None:
    header = built.output  # human summary renders without error
    assert header
    data = json.loads(built.json_bytes)
    h = data["header"]
    assert h["claims_total"] == 840
    assert h["claims_by_status"]["draft"] == 816
    assert sum(h["claims_by_status"].values()) == 840
    assert h["anchors_strict"] == 94
    assert h["anchors_total"] == 287
    assert h["validated_anchor_share"] == pytest.approx(94 / 287)
    assert h["pending_validations"]["count"] == 44
    assert "no review dates" in h["pending_validations"]["reason"]
    nearest = h["nearest_dated_items"]
    assert [(i["date"], i["study"], len(i["claims"])) for i in nearest] == [
        ("2026-10-25", "054", 1),
        ("2026-10-24", "052", 4),
        ("2026-10-24", "074", 1),
    ]
    as_of = h["as_of"]
    assert as_of["ledger_sha256"] == li.sha256_file(ROOT / li.LEDGER_REL)
    assert as_of["map_defs"] == "map-defs v1"
    assert as_of["ledger_lines"] == 871


def test_sections_census(built) -> None:
    data = json.loads(built.json_bytes)
    kinds = {}
    for el in data["elements"]:
        kinds[el["kind"]] = kinds.get(el["kind"], 0) + 1
    assert kinds["claim"] == 840
    assert kinds.get("corpus_texts", 0) == 0
    assert sum(kinds.values()) == 1484
    rels = {}
    for edge in data["edges"]:
        rels[edge["rel"]] = rels.get(edge["rel"], 0) + 1
    assert rels == {"supports": 1356, "opposes": 7}
    assert len(data["loads"]) == 840
    system = data["system"]
    assert system["falsifier_census"]["covered"] == 831
    assert system["falsifier_census"]["total"] == 840
    assert system["aee_state_census"] == {
        "with_state": 0,
        "without_state": 840,
        "total": 840,
    }
    assert system["claim_population"]["no_stage_recorded"] == 15


def test_edge_citation_rule_governing_pointer_only(built) -> None:
    data = json.loads(built.json_bytes)
    edge = next(
        e
        for e in data["edges"]
        if e["to"] == YADAV and e["column_class"] == "studies"
    )
    assert edge["rel"] == "opposes"
    assert edge["citations"] == [YADAV, GOVERNING_PTR]
    # The embedded cell keeps both appends, as the matrix's own
    # record carries them; only the edge is reduced.
    study_cell = next(
        c for c in data["claims"][YADAV]["matrix_row"]["cells"]
        if c["column_class"] == "studies"
    )
    assert len(study_cell["citations"]) == 3
    assert GOVERNING_PTR in study_cell["citations"]


def test_parpola_record_honest_states(built) -> None:
    data = json.loads(built.json_bytes)
    rec = data["claims"][PARPOLA]
    assert rec["falsifier_counts"] == {"present": 1, "evaluable": 0}
    assert rec["displayed_score"] == {"state": "empty"}
    assert rec["aee_state"] is None
    assert rec["matrix_row"]["cells"] == []
    signs = {r["sign_ref"]: r for r in rec["evidence"]["sign_records"]}
    assert set(signs) == {"mahadevan:64", "mahadevan:70", "mahadevan:72"}
    for rec_sign in signs.values():
        assert rec_sign["matrix_record"] is None
        assert rec_sign["divergence"] is True
    readings = {
        r["settle_key"]: r["settle_record"]["reading"]
        for r in rec["evidence"]["sign_records"]
    }
    assert readings == {"M064": "va", "M070": "vēl", "M072": "mā"}
    assert len(rec["annotations"]) == 1
    annotation = rec["annotations"][0]
    assert annotation["bearing"]["verdict"] is None
    assert annotation["bearing"]["neighbors_surfaced"] == 26
    assert annotation["sidecar"]["sha256"].startswith("3c8c5312")


def test_settling_section_opens_on_the_stored_comparison(built) -> None:
    data = json.loads(built.json_bytes)
    settling = data["settling"]
    assert len(settling["runs"]) == 2
    result = settling["comparison"]["result"]
    assert len(result["claims_compared"]) == 1
    assert result["per_claim_divergences"] == []
    assert len(settling["canonicals"]["scenarios"]) == 5
    assert settling["reach"]["s_r3"]["status"] == "UNMEASURED"
    assert settling["reach"]["claims_untouched_by_any_run"] == 839
    assert settling["label"] == mp.SETTLING_LABEL


# ── Refusal modes on a scratch tree ─────────────────────────────

_COPIES = (
    "glossa-indus/ledger/claims.jsonl",
    "glossa-indus/matrix/matrix.json",
    "backend/reports/INDUS_FINAL_ANCHORS.json",
    "reports/phase108_provenance_register.json",
    "glossa-indus/ledger/assignment-sets.json",
    "glossa-indus/ledger/settling-canonical.json",
)


@pytest.fixture()
def map_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    for rel in _COPIES:
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst)
    runs_dst = root / "glossa-indus/ledger/runs"
    runs_dst.mkdir(parents=True, exist_ok=True)
    for f in sorted((ROOT / "glossa-indus/ledger/runs").glob("*.json")):
        shutil.copyfile(f, runs_dst / f.name)
    for tree in ("glossa-indus/claims", "glossa-indus/corpus_texts", "specs"):
        (root / tree).parent.mkdir(parents=True, exist_ok=True)
        os.symlink(ROOT / tree, root / tree)
    (root / "docs").mkdir()
    os.symlink(
        ROOT / "docs/research-evidence", root / "docs/research-evidence"
    )
    return root


def test_builder_refuses_a_stale_matrix(map_tree: Path) -> None:
    matrix_path = map_tree / "glossa-indus/matrix/matrix.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    matrix["as_of"]["ledger_sha256"] = "0" * 64
    matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
    with pytest.raises(mp.MapBuildError, match="stale"):
        mp.build_map(map_tree)


def test_builder_refuses_a_run_pinned_to_another_build(
    map_tree: Path,
) -> None:
    run_path = next((map_tree / "glossa-indus/ledger/runs").glob("*.json"))
    run = json.loads(run_path.read_text(encoding="utf-8"))
    run["pins"]["ledger"]["sha256"] = "0" * 64
    run_path.write_text(json.dumps(run), encoding="utf-8")
    with pytest.raises(mp.MapBuildError, match="different build"):
        mp.build_map(map_tree)


# ── The surface API (desktop/token mode) ────────────────────────


def test_api_header_and_stamp(client) -> None:
    resp = client.get("/api/v1/indus-map/header")
    assert resp.status_code == 200
    body = resp.json()
    assert body["header"]["claims_total"] == 840
    assert body["stamp"]["stale"] is False
    published = (ROOT / mp.MAP_REL).read_bytes()
    assert body["stamp"]["map_sha256"] == hashlib.sha256(
        published
    ).hexdigest()


def test_api_sections_serve_the_artifact(client) -> None:
    system = client.get("/api/v1/indus-map/system").json()["system"]
    assert system["sign_inventory"]["frame_scope"] == 286
    matrix = client.get("/api/v1/indus-map/matrix").json()["matrix"]
    assert matrix["coverage"]["cells_by_relation"] == {
        "supports": 1356,
        "opposes": 7,
        "constrains": 0,
    }
    settling = client.get("/api/v1/indus-map/settling").json()["settling"]
    assert settling["comparison"]["result"]["per_claim_divergences"] == []


def test_api_claim_and_evidence(client) -> None:
    claim = client.get(f"/api/v1/indus-map/claims/{PARPOLA}").json()
    assert claim["claim"]["statement"].startswith("The fish sign")
    assert claim["claim"]["displayed_score"]["state"] == "empty"
    evidence = client.get(
        f"/api/v1/indus-map/claims/{PARPOLA}/evidence"
    ).json()["evidence"]
    assert evidence["column_summary"]["anchors"] == {
        "columns": 287,
        "cells": 0,
    }
    assert len(evidence["sign_records"]) == 3


def test_api_unknown_claim_is_404(client) -> None:
    resp = client.get("/api/v1/indus-map/claims/no_such_claim")
    assert resp.status_code == 404


# ── The C086-19 scoping oracle (cloud mode) ─────────────────────

SERVICE_CREDENTIAL = "test-service-credential-086"
SCOPED_404_BODY = {"detail": "Not found"}


def _actor(user_id, username, global_type, roles):
    return {
        "X-Glossa-Service-Credential": SERVICE_CREDENTIAL,
        "X-Glossa-User-Id": user_id,
        "X-Glossa-User-Name": username,
        "X-Glossa-Global-Type": global_type,
        "X-Glossa-Workspace-Roles": json.dumps(roles),
    }


MEMBER = _actor("u-m086", "mapmember", "member", {"indus-script": "member"})
OUTSIDER = _actor(
    "u-o086", "mapoutsider", "member", {"other-ws": "member"}
)


@pytest.fixture(scope="module")
def cloud_client(tmp_path_factory):
    data_dir = tmp_path_factory.mktemp("glossa086") / "data"
    keys = ("GLOSSA_CLOUD", "GLOSSA_SERVICE_CREDENTIAL", "GLOSSA_DATA_DIR")
    saved = {k: os.environ.get(k) for k in keys}
    from glossa_lab import database as _database

    saved_db = _database.get_db()
    os.environ["GLOSSA_CLOUD"] = "1"
    os.environ["GLOSSA_SERVICE_CREDENTIAL"] = SERVICE_CREDENTIAL
    os.environ["GLOSSA_DATA_DIR"] = str(data_dir)
    from glossa_lab.config import get_settings

    get_settings.cache_clear()
    from fastapi.testclient import TestClient

    from glossa_lab.main import create_app

    with TestClient(create_app()) as client:
        yield client
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    get_settings.cache_clear()
    _database._db = saved_db


def test_scoping_member_reads_the_map(cloud_client) -> None:
    resp = cloud_client.get("/api/v1/indus-map/header", headers=MEMBER)
    assert resp.status_code == 200
    assert resp.json()["header"]["claims_total"] == 840


def test_scoping_outsider_gets_the_scoped_404(cloud_client) -> None:
    for path in (
        "/api/v1/indus-map/header",
        "/api/v1/indus-map/system",
        f"/api/v1/indus-map/claims/{PARPOLA}",
        f"/api/v1/indus-map/claims/{PARPOLA}/evidence",
        "/api/v1/indus-map/settling",
    ):
        resp = cloud_client.get(path, headers=OUTSIDER)
        assert resp.status_code == 404, path
        assert resp.json() == SCOPED_404_BODY, path
        # No element of the map leaks into the refusal body.
        assert PARPOLA not in resp.text
        assert "840" not in resp.text
