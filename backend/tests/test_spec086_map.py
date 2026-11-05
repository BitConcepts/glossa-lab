"""Spec 086 Stage 5 (T502/T503) — the map builder and its API.

The builder tests pin the artifact's contract on the real tree
(the header exactly as Q3 approved it, the edge-citation rule,
the honest empty states) and its refusal modes (a stale matrix,
a run pinned to another ledger build). The API tests pin the
surface's contract: the published artifact served exactly, and
the C086-19 scoping oracle — an actor without an indus-script
role receives the scoped 404 and no element of the map.

Real-tree precondition: the builder tests build over the
committed tree, whose source files the ledger mirrors by
canonical hash; earlier suite tests (the indus-claims
carryover and the spec029 regeneration tests) regenerate
the extracted-claims source files in-tree with transient
bytes when they run first in a suite process, in which case
the builder refuses by design. The tests verify that
precondition mechanically before building — the builder's
own recorded-hash verification — and skip with the cause
named only when every divergence is inside that known
rewrite population (assertions unchanged wherever the
precondition holds); a divergence outside the population
fails loudly, never skips. The scratch-tree fixture shares
the precondition — its claims tree is a symlink to the real
one — so it applies the same guard (the Stage 2/3
discipline, as in test_spec086_ledger_gate.py).
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


# ── Real-tree precondition (the Stage 2/3 discipline) ────

_EXTRACTED_CLAIMS_PREFIX = "glossa-indus/claims/extracted_claims/"


def _recorded_source_hash_divergences(root: Path) -> list[str]:
    """The builder tests' precondition, checked mechanically:
    run the builder's own source verification — the recorded-
    hash comparison ``build_map`` performs through the
    ledger's pointers — over ``root`` and return the source
    paths it names as diverged. An empty list means every
    recorded hash still verifies: the precondition holds."""
    registers = mp._Registers(root)
    entries = li.read_ledger(root / li.LEDGER_REL)
    for entry in entries:
        for source in entry.get("sources", []):
            registers.verify(source["path"], source["sha256"])
        if entry.get("kind") == "annotation":
            sidecar = entry.get("sidecar") or {}
            if sidecar.get("path") and sidecar.get("sha256"):
                registers.verify(sidecar["path"], sidecar["sha256"])
    paths: list[str] = []
    for mismatch in registers.mismatches:
        path = mismatch.split(":", 1)[0]
        if path not in paths:
            paths.append(path)
    return paths


def _require_map_precondition(root: Path) -> None:
    """Skip-with-cause (the Stage 2/3 discipline) when the
    real-tree precondition is destroyed by the known in-tree
    rewrite population: an earlier suite test regenerated
    the extracted-claims source files, so the builder's
    recorded-hash refusal is the designed behavior. Where
    the precondition holds this returns, and the builder in
    the caller must pass exactly as before. A divergence
    OUTSIDE the rewrite population is not suite pollution:
    it fails loudly here and is never skipped over."""
    divergences = _recorded_source_hash_divergences(root)
    if not divergences:
        return
    outside = [
        p for p in divergences if not p.startswith(_EXTRACTED_CLAIMS_PREFIX)
    ]
    if outside:
        raise AssertionError(
            "recorded-source-hash divergence outside the known "
            "extracted-claims rewrite population — the map "
            "builder's refusal is not explained by suite "
            f"pollution and must not be skipped over: {outside}"
        )
    shown = ", ".join(divergences[:3])
    more = (
        f" (+{len(divergences) - 3} more)" if len(divergences) > 3 else ""
    )
    pytest.skip(
        "clean-tree precondition destroyed: the map builder's "
        "recorded-source-hash verification fails — the tree no "
        "longer matches the ledger's recorded hashes because "
        "an earlier suite test (tests/test_indus_claims_"
        "carryover.py and the spec029 regeneration tests) "
        "regenerated the extracted-claims source files in-tree "
        "with transient bytes; the builder's refusal is the "
        f"designed behavior. Diverged: {shown}{more}"
    )


def _mini_tree(root: Path, rel: str) -> Path:
    """A one-entry ledger tree for the precondition teeth:
    one source file under ``rel``, recorded by its canonical
    hash at assembly time."""
    src = root / rel
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_bytes(b'{"claim_id": "mini_001"}\n')
    entry = {
        "id": "mini_001",
        "kind": "claim",
        "sources": [
            {
                "path": rel,
                "claim_id": "mini_001",
                "sha256": li.sha256_file(src),
            }
        ],
    }
    ledger = root / li.LEDGER_REL
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(json.dumps(entry) + "\n", encoding="utf-8")
    return src


def test_precondition_holds_on_a_pristine_tree(tmp_path: Path) -> None:
    rel = "glossa-indus/claims/extracted_claims/mini.json"
    _mini_tree(tmp_path, rel)
    assert _recorded_source_hash_divergences(tmp_path) == []
    _require_map_precondition(tmp_path)  # must not skip or raise


def test_precondition_names_an_altered_extracted_claims_file(
    tmp_path: Path,
) -> None:
    """Teeth for the precondition itself: alter one
    extracted-claims source file and the precondition must
    trip, naming that file — in the helper's divergence
    list and in the skip reason."""
    rel = "glossa-indus/claims/extracted_claims/mini.json"
    src = _mini_tree(tmp_path, rel)
    src.write_bytes(src.read_bytes() + b"x")
    assert _recorded_source_hash_divergences(tmp_path) == [rel]
    with pytest.raises(pytest.skip.Exception) as excinfo:
        _require_map_precondition(tmp_path)
    reason = str(excinfo.value)
    assert "recorded-source-hash verification" in reason
    assert rel in reason


def test_precondition_fails_loudly_outside_the_rewrite_population(
    tmp_path: Path,
) -> None:
    """The other direction: a divergence outside the
    extracted-claims population is never skipped over —
    the guard raises, naming the file."""
    rel = "glossa-indus/claims/bundles/mini.json"
    src = _mini_tree(tmp_path, rel)
    src.write_bytes(src.read_bytes() + b"x")
    assert _recorded_source_hash_divergences(tmp_path) == [rel]
    with pytest.raises(AssertionError) as excinfo:
        _require_map_precondition(tmp_path)
    assert rel in str(excinfo.value)


@pytest.fixture(scope="module")
def built():
    _require_map_precondition(ROOT)
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
    assert h["claims_total"] == 913
    assert h["claims_by_status"]["draft"] == 889
    assert sum(h["claims_by_status"].values()) == 913
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
    assert as_of["ledger_lines"] == 944


def test_sections_census(built) -> None:
    data = json.loads(built.json_bytes)
    kinds = {}
    for el in data["elements"]:
        kinds[el["kind"]] = kinds.get(el["kind"], 0) + 1
    assert kinds["claim"] == 913
    assert kinds.get("corpus_texts", 0) == 0
    assert sum(kinds.values()) == 1557
    rels = {}
    for edge in data["edges"]:
        rels[edge["rel"]] = rels.get(edge["rel"], 0) + 1
    assert rels == {"supports": 1429, "opposes": 7}
    assert len(data["loads"]) == 913
    system = data["system"]
    assert system["falsifier_census"]["covered"] == 904
    assert system["falsifier_census"]["total"] == 913
    assert system["aee_state_census"] == {
        "with_state": 0,
        "without_state": 913,
        "total": 913,
    }
    assert system["claim_population"]["no_stage_recorded"] == 16


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
    assert settling["reach"]["claims_untouched_by_any_run"] == 912
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
    # The fixture shares the real-tree precondition: the
    # claims tree above is a symlink into the real tree, so
    # a polluted suite process pollutes this tree's inputs
    # identically. Skip with the cause named rather than
    # failing on a precondition the test never stated (the
    # run-pin refusal below is checked only after the
    # builder's source verification).
    _require_map_precondition(root)
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
    assert body["header"]["claims_total"] == 913
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
        "supports": 1429,
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
    assert resp.json()["header"]["claims_total"] == 913


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
        assert "913" not in resp.text
