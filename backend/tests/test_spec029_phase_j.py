"""Spec 029 Phase J — D-D foundation annotations (tasks J1–J4).

Pins:

* J2 computed annotations: every canonical figure in the
  foundation report's computed annotations comes from the
  canonical stores at generation time (anchors file +
  extracted-claims store), and the report is stamped with the
  anchors file's SHA-256.
* Regeneration proof: mutating a scratch copy of the canonical
  anchors file changes the computed annotations AND the hash
  stamp accordingly; an unmutated regeneration reproduces the
  live computed annotations exactly.
* J1 as-of label: the label names the anchor table (file +
  SHA-256 + date) the figures describe, and every annotation in
  the on-disk report carries it.
* J4 stale-figure purge: the Phase-48-era figures the audit
  named appear in no annotation the report can serve; historical
  population figures that remain are labelled with their as-of
  phase.
* J3 loud endpoint: GET /api/v1/foundation/status serves the
  on-disk report (figures, as-of label, hash stamp) when no run
  is recorded in-process; a missing or unreadable report is an
  explicit 503 error, never a silent null payload; a report
  whose stamped hash no longer matches the anchors file on disk
  is served with an explicit staleness flag.
* J-gate: the foundation check itself is untouched in what it
  checks — the live report still reads 40 passed / 0 failed /
  8 warnings (asserted against the script's own run in
  test_foundation_check_script.py; here the committed report's
  counts are pinned).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import glossa_lab.api.foundation as foundation_api
from glossa_lab.foundation_annotations import (
    ANCHORS_REL,
    CLAIMS_REL,
    anchors_file_sha256,
    computed_annotation_entries,
    compute_canonical_snapshot,
)

#: The Phase-48-era figures the audit (§5-P8 defect 3) named.
#: They must never again appear in a served annotation (J4 purge);
#: this test file is the guard that greps for them, so it is the
#: one place they are quoted — as a purge list, never as data.
STALE_PHASE48_FIGURES = (
    "37 HIGH + 36 MEDIUM",
    "75 LOW (distributional only), 1 UNCERTAIN",
    "1 UNCERTAIN (M267)",
)

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / ANCHORS_REL
CLAIMS_DIR = REPO / CLAIMS_REL
REPORT_PATH = REPO / "reports" / "foundation_check_report.json"
SCRIPT = REPO / "backend" / "scripts" / "foundation_check.py"
HOLDAT = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"

AS_OF = "2026-10-12"


def _live_snapshot() -> dict:
    return compute_canonical_snapshot(REPO, as_of=AS_OF)


# ── J2: computed figures match the canonical stores ─────────────────

def test_computed_figures_match_canonical_stores():
    snap = _live_snapshot()
    doc = json.loads(ANCHORS_PATH.read_text("utf-8"))
    anchors = doc["anchors"]
    assert snap["anchors_total"] == len(anchors) == 287
    assert snap["tier_counts"] == {
        "CANDIDATE": 113, "HIGH": 166, "LOW": 3, "MEDIUM": 5,
    }
    assert snap["hm_count"] == 171
    assert snap["strict_count"] == 94
    assert snap["strict_composition"] == {"HIGH": 90, "MEDIUM": 4}
    assert snap["pending_count"] == 44
    assert snap["validation_status_counts"] == {
        "no_validation_record": 3,
        "pending_non_sa_validation": 44,
        "premise_superseded": 113,
        "sa_in_provenance_chain": 33,
        "strict_sa_independent": 94,
    }
    assert snap["claims_total"] == 31
    assert snap["m267"]["confidence"] == "MEDIUM"
    assert snap["m267"]["validation_status"] == "strict_sa_independent"


def test_hash_stamp_is_the_anchors_file_sha256():
    snap = _live_snapshot()
    expected = hashlib.sha256(ANCHORS_PATH.read_bytes()).hexdigest()
    assert snap["anchors_file_sha256"] == expected
    assert anchors_file_sha256(ANCHORS_PATH) == expected
    # The stamp Phase H recorded for this file at this main head.
    assert expected == (
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
    )


def test_computed_annotations_carry_computed_figures():
    snap = _live_snapshot()
    solid, caveated = computed_annotation_entries(snap)
    assert solid[0] == "Canonical anchor table (computed)"
    for figure in ("287 anchors", "166 HIGH", "5 MEDIUM", "3 LOW",
                   "113 CANDIDATE", "Strict core", "94 anchors "
                   "(90 HIGH + 4 MEDIUM)", "Pending validation: 44",
                   "31 claims in 10 files"):
        assert figure in solid[1], figure
    assert caveated[0] == "signs assigned"
    for figure in ("171 signs (166 HIGH + 5 MEDIUM)",
                   "M267 is MEDIUM", "not UNCERTAIN"):
        assert figure in caveated[1], figure


def test_as_of_label_names_the_anchor_table():
    snap = _live_snapshot()
    label = snap["as_of_label"]
    assert label.startswith(f"As of {AS_OF}")
    assert ANCHORS_REL in label
    assert snap["anchors_file_sha256"] in label
    assert snap["claims_store_sha256"] in label


# ── J2: regeneration proof (mutation tracks, unmutated reproduces) ─

def _scratch_repo(tmp_path: Path) -> Path:
    scratch = tmp_path / "repo"
    (scratch / "backend" / "reports").mkdir(parents=True)
    shutil.copy2(ANCHORS_PATH, scratch / ANCHORS_REL)
    shutil.copytree(CLAIMS_DIR, scratch / CLAIMS_REL)
    return scratch


def test_regeneration_unmutated_reproduces_live_annotations(tmp_path):
    scratch = _scratch_repo(tmp_path)
    live = computed_annotation_entries(_live_snapshot())
    regen = computed_annotation_entries(
        compute_canonical_snapshot(scratch, as_of=AS_OF)
    )
    assert regen == live
    assert (
        compute_canonical_snapshot(scratch, as_of=AS_OF)["anchors_file_sha256"]
        == _live_snapshot()["anchors_file_sha256"]
    )


def test_regeneration_mutated_input_tracks_and_restamps(tmp_path):
    scratch = _scratch_repo(tmp_path)
    target = scratch / ANCHORS_REL
    doc = json.loads(target.read_text("utf-8"))
    # Mutate: demote one HIGH strict anchor to LOW / pending.
    victim = next(
        k for k, v in doc["anchors"].items()
        if v.get("confidence") == "HIGH" and v.get("strict_set")
    )
    doc["anchors"][victim]["confidence"] = "LOW"
    doc["anchors"][victim]["strict_set"] = False
    doc["anchors"][victim]["validation_status"] = (
        "pending_non_sa_validation"
    )
    target.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    before = _live_snapshot()
    after = compute_canonical_snapshot(scratch, as_of=AS_OF)
    assert after["anchors_file_sha256"] != before["anchors_file_sha256"]
    assert after["tier_counts"]["HIGH"] == before["tier_counts"]["HIGH"] - 1
    assert after["tier_counts"]["LOW"] == before["tier_counts"]["LOW"] + 1
    assert after["strict_count"] == before["strict_count"] - 1
    assert after["pending_count"] == before["pending_count"] + 1
    solid_before, _ = computed_annotation_entries(before)
    solid_after, _ = computed_annotation_entries(after)
    assert solid_after[1] != solid_before[1]
    assert "93 anchors (89 HIGH + 4 MEDIUM)" in solid_after[1]
    assert after["as_of_label"] != before["as_of_label"]


# ── J1/J4: the on-disk report's annotations ─────────────────────────

def _report() -> dict:
    return json.loads(REPORT_PATH.read_text("utf-8"))


def test_disk_report_is_stamped_and_labelled():
    report = _report()
    assert report["anchors_file_sha256"] == anchors_file_sha256(ANCHORS_PATH)
    assert report["anchors_file"] == ANCHORS_REL
    assert report["annotations_as_of"].startswith("As of ")
    assert report["anchors_file_sha256"] in report["annotations_as_of"]
    assert report["claims_store_sha256"]
    for entry in report["solid_claims"] + report["caveated_claims"]:
        assert entry["as_of"] == report["annotations_as_of"]


def test_disk_report_annotations_equal_computed():
    """The committed report's computed entries are exactly what
    regeneration from the live canonical stores produces (the
    report's own as-of date is its generation date)."""
    report = _report()
    snap = compute_canonical_snapshot(
        REPO, as_of=report["annotations_as_of"].split(" — ")[0].removeprefix("As of ")
    )
    solid, caveated = computed_annotation_entries(snap)
    by_claim = {
        e["claim"]: e for e in report["solid_claims"] + report["caveated_claims"]
    }
    assert by_claim[solid[0]]["detail"] == solid[1]
    assert by_claim[caveated[0]]["detail"] == caveated[1]


def test_stale_phase48_figures_purged_from_all_annotations():
    report = _report()
    served = json.dumps(
        report["solid_claims"] + report["caveated_claims"]
    )
    for figure in STALE_PHASE48_FIGURES:
        assert figure not in served
    for source in (
        SCRIPT,
        REPO / "backend/glossa_lab/foundation_annotations.py",
        REPO / "backend/glossa_lab/api/foundation.py",
    ):
        src = source.read_text("utf-8")
        for figure in STALE_PHASE48_FIGURES:
            assert figure not in src, (source, figure)


def test_historical_population_figures_are_labelled():
    report = _report()
    by_claim = {
        e["claim"]: e for e in report["solid_claims"] + report["caveated_claims"]
    }
    for claim, phase in (
        ("Phase-48 30 signs promoted to HIGH", "Phase-48"),
        ("Phase-56 expanded Parpola crosswalk", "Phase-56"),
        ("Phase-69 grammar 100% site-invariant", "Phase-69"),
        ("Phase-71 M<->P crosswalk 84.5% token coverage", "Phase-71"),
        ("M↔P crosswalk", "Phase-51"),
    ):
        detail = by_claim[claim]["detail"]
        assert f"[Historical figure — as of {phase}" in detail, claim


def test_disk_report_counts_unchanged():
    report = _report()
    assert (report["n_ok"], report["n_fail"], report["n_warn"]) == (40, 0, 8)
    assert report["verdict"] == "READY WITH CAVEATS"


# ── J3: the loud endpoint ───────────────────────────────────────────

def _write_report(path: Path, **overrides) -> dict:
    report = {
        "n_ok": 40, "n_fail": 0, "n_warn": 8,
        "verdict": "READY WITH CAVEATS",
        "generated_at": "2026-10-12T00:00:00+00:00",
        "annotations_as_of": "As of 2026-10-12 — test label",
        "anchors_file": ANCHORS_REL,
        "anchors_file_sha256": anchors_file_sha256(ANCHORS_PATH),
        "claims_store_sha256": "0" * 64,
        "solid_claims": [{"claim": "c", "detail": "d", "status": "s",
                          "as_of": "As of 2026-10-12 — test label"}],
        "caveated_claims": [],
    }
    report.update(overrides)
    path.write_text(json.dumps(report), encoding="utf-8")
    return report


@pytest.fixture()
def fresh_status(client, monkeypatch, tmp_path):
    """Status endpoint with no in-process run recorded, pointed at
    a scratch report + the live anchors file."""
    report_path = tmp_path / "foundation_check_report.json"
    monkeypatch.setattr(foundation_api, "_last_result", None)
    monkeypatch.setattr(foundation_api, "_last_checked_at", None)
    monkeypatch.setattr(foundation_api, "_REPORT_PATH", report_path)
    monkeypatch.setattr(foundation_api, "_ANCHORS_PATH", ANCHORS_PATH)
    return report_path


def test_endpoint_serves_disk_report_with_figures(client, fresh_status):
    _write_report(fresh_status)
    resp = client.get("/api/v1/foundation/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["verdict"] == "READY WITH CAVEATS"
    assert (data["n_ok"], data["n_fail"], data["n_warn"]) == (40, 0, 8)
    assert data["source"] == "on_disk_report"
    assert data["last_checked_at"] == "2026-10-12T00:00:00+00:00"
    block = data["report"]
    assert block["solid_claims"][0]["claim"] == "c"
    assert block["annotations_as_of"] == "As of 2026-10-12 — test label"
    assert block["anchors_file_sha256"] == anchors_file_sha256(ANCHORS_PATH)
    assert block["report_stale"] is False
    assert "staleness_warning" not in block


def test_endpoint_missing_report_fails_loudly(client, fresh_status):
    assert not fresh_status.exists()
    resp = client.get("/api/v1/foundation/status")
    assert resp.status_code == 503
    body = resp.json()
    assert "foundation report unavailable" in body["detail"]
    # No silent-null payload: the null fields are never served.
    assert body.get("verdict") is None
    assert "n_ok" not in body


def test_endpoint_unreadable_report_fails_loudly(client, fresh_status):
    fresh_status.write_text("{ not json", encoding="utf-8")
    resp = client.get("/api/v1/foundation/status")
    assert resp.status_code == 503
    assert "foundation report unavailable" in resp.json()["detail"]


def test_endpoint_stale_hash_flagged_not_silent(client, fresh_status):
    _write_report(fresh_status, anchors_file_sha256="f" * 64)
    resp = client.get("/api/v1/foundation/status")
    assert resp.status_code == 200
    block = resp.json()["report"]
    assert block["report_stale"] is True
    assert block["anchors_file_sha256"] == "f" * 64
    assert block["anchors_file_sha256_current"] == (
        anchors_file_sha256(ANCHORS_PATH)
    )
    assert "do not describe the current anchor table" in (
        block["staleness_warning"]
    )


# ── J2 end-to-end: the script regenerates the stamped report ────────

@pytest.mark.skipif(
    not HOLDAT.exists(), reason="Holdat corpus not downloaded (gitignored corpora/)"
)
def test_script_regeneration_reproduces_annotations(tmp_path):
    """Run the foundation script against a scratch copy of the
    repo layout it needs is impractical (it reads the whole repo),
    so run it in place: the regenerated report's computed
    annotations and hash stamp must equal a fresh computation from
    the canonical stores, and the check counts stay 40/0/8."""
    env = dict(os.environ, GLOSSA_REPO_ROOT=str(REPO))
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, timeout=600, env=env, cwd=str(REPO),
    )
    assert proc.returncode == 0, proc.stderr[-500:]
    report = _report()
    assert (report["n_ok"], report["n_fail"], report["n_warn"]) == (40, 0, 8)
    snap = compute_canonical_snapshot(
        REPO,
        as_of=report["annotations_as_of"].split(" — ")[0].removeprefix("As of "),
    )
    assert report["anchors_file_sha256"] == snap["anchors_file_sha256"]
    solid, caveated = computed_annotation_entries(snap)
    by_claim = {
        e["claim"]: e for e in report["solid_claims"] + report["caveated_claims"]
    }
    assert by_claim[solid[0]]["detail"] == solid[1]
    assert by_claim[caveated[0]]["detail"] == caveated[1]
