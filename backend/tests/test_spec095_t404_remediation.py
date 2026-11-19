"""Remediation tests for the audit failures closed by the T404
remediation stage. Each test exercises the real component that failed
the audit — the live app and engine for the API legs, the real ledger
write path for the rollback leg — not a stand-in.

Legs:
  - project create: POST /projects/import accepts a flat minimal body
    ({name, description}); the full bundle shape still works; an empty
    body still refuses.
  - job pause/resume: a job whose pipeline is not registered stays
    pending (dispatch-deferred, reason stamped) instead of being
    claimed and failed within seconds, so pause/resume/cancel work on
    it; an undispatchable head does not starve the jobs behind it.
  - report generation: the first template is ready and generates
    (its generator script resolves and its stated inputs exist).
  - ledger rollback: snapshot / restore / rollback_migration round-trip
    a migration write, refuse corrupt snapshots, and restore absence.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from glossa_lab import ledger_intake as li

REPO = Path(__file__).resolve().parents[2]


# ── Project create via import ────────────────────────────────────────────────


def _project_labels(client) -> list[str]:
    body = client.get("/api/v1/projects").json()
    items = body if isinstance(body, list) else body.get("projects", [])
    return [p["label"] for p in items]


def test_import_accepts_flat_minimal_body(client):
    name = "Remediation Probe Project"
    resp = client.post(
        "/api/v1/projects/import",
        json={"name": name, "description": "Created from a flat minimal body."},
    )
    assert resp.status_code == 200, resp.text
    assert name in _project_labels(client)


def test_import_still_accepts_full_bundle(client):
    resp = client.post(
        "/api/v1/projects/import",
        json={"project": {"label": "Remediation Bundle Project"}},
    )
    assert resp.status_code == 200, resp.text
    assert "Remediation Bundle Project" in _project_labels(client)


def test_import_refuses_body_without_any_label(client):
    resp = client.post("/api/v1/projects/import", json={"description": "no name"})
    assert resp.status_code == 422


# ── Job dispatch deferral (pause / resume) ───────────────────────────────────


def _wait_for(client, job_id: str, predicate, timeout: float = 30.0):
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = client.get(f"/api/v1/jobs/{job_id}").json()
        if predicate(last):
            return last
        time.sleep(0.5)
    raise AssertionError(f"job {job_id} never satisfied the predicate; last={last}")


def test_unregistered_pipeline_job_stays_pending_and_pausable(client):
    # No pipeline key: the create schema's default pipeline name, which
    # no instance registers — the audit's probe shape.
    resp = client.post(
        "/api/v1/jobs",
        json={"name": "remediation-dispatch-probe", "params": {}},
    )
    assert resp.status_code in (200, 201), resp.text
    job_id = resp.json()["id"]

    job = _wait_for(
        client, job_id, lambda j: "dispatch_wait" in (j.get("params") or {})
    )
    assert job["status"] == "pending"

    paused = client.post(f"/api/v1/jobs/{job_id}/pause")
    assert paused.status_code == 200, paused.text
    assert client.get(f"/api/v1/jobs/{job_id}").json()["status"] == "paused"

    resumed = client.post(f"/api/v1/jobs/{job_id}/resume")
    assert resumed.status_code == 200, resumed.text
    assert client.get(f"/api/v1/jobs/{job_id}").json()["status"] == "pending"

    # It must still be pending (never claimed and failed) after the
    # engine has had several chances to pick it up.
    time.sleep(3)
    after = client.get(f"/api/v1/jobs/{job_id}").json()
    assert after["status"] == "pending"

    # The API's cancel is DELETE: the record is removed, returned as
    # cancelled. A dispatch-deferred job is always caught before the
    # engine, so the cancelled state is deterministic here.
    cancelled = client.delete(f"/api/v1/jobs/{job_id}")
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"
    assert client.get(f"/api/v1/jobs/{job_id}").status_code == 404


def test_undispatchable_head_does_not_starve_queue(client):
    ids = []
    for name in ("remediation-starve-a", "remediation-starve-b"):
        resp = client.post("/api/v1/jobs", json={"name": name, "params": {}})
        assert resp.status_code in (200, 201), resp.text
        ids.append(resp.json()["id"])
    # The second job can only earn its own dispatch_wait stamp if the
    # engine's peek advances past the first undispatchable job.
    for job_id in ids:
        job = _wait_for(
            client, job_id, lambda j: "dispatch_wait" in (j.get("params") or {})
        )
        assert job["status"] == "pending"
        client.delete(f"/api/v1/jobs/{job_id}")


# ── Report generation ────────────────────────────────────────────────────────


def test_first_report_template_ready_and_generates(client):
    templates = client.get("/api/v1/reports/templates").json()
    assert templates, "template registry is empty"
    first = templates[0]
    assert first["ready"] is True, f"first template not ready: {first}"
    resp = client.post(
        "/api/v1/reports/generate", json={"template_id": first["id"]}
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["started"] is True


def test_generate_unknown_template_404(client):
    resp = client.post(
        "/api/v1/reports/generate", json={"template_id": "no-such-template"}
    )
    assert resp.status_code == 404


# ── Ledger snapshot / rollback ───────────────────────────────────────────────


def _write_lines(path: Path, rows: list[dict]) -> bytes:
    body = "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows).encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    return body


def test_snapshot_restore_round_trip(tmp_path):
    ledger = tmp_path / "claims.jsonl"
    original = _write_lines(ledger, [{"id": "a", "kind": "claim"}, {"id": "b", "kind": "claim"}])
    snap = li.snapshot_ledger(ledger)
    _write_lines(ledger, [{"id": "a", "kind": "claim"}, {"id": "b", "kind": "claim"}, {"id": "c", "kind": "claim"}])
    li.restore_snapshot(ledger, snap)
    assert ledger.read_bytes() == original


def test_snapshot_restores_absence(tmp_path):
    ledger = tmp_path / "claims.jsonl"
    snap = li.snapshot_ledger(ledger)
    _write_lines(ledger, [{"id": "a", "kind": "claim"}])
    li.restore_snapshot(ledger, snap)
    assert not ledger.exists()


def test_corrupt_snapshot_refused_and_ledger_untouched(tmp_path):
    ledger = tmp_path / "claims.jsonl"
    original = _write_lines(ledger, [{"id": "a", "kind": "claim"}])
    snap = li.snapshot_ledger(ledger)
    manifest = json.loads(snap.read_text(encoding="utf-8"))
    payload = bytearray(__import__("base64").b64decode(manifest["bytes_b64"]))
    payload[0] ^= 0xFF
    manifest["bytes_b64"] = __import__("base64").b64encode(bytes(payload)).decode()
    snap.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError):
        li.restore_snapshot(ledger, snap)
    assert ledger.read_bytes() == original


def test_missing_snapshot_refused(tmp_path):
    ledger = tmp_path / "claims.jsonl"
    _write_lines(ledger, [{"id": "a", "kind": "claim"}])
    with pytest.raises(FileNotFoundError):
        li.restore_snapshot(ledger, tmp_path / "nope.snapshot.json")


def test_rollback_migration_uses_latest_snapshot(tmp_path):
    ledger = tmp_path / "claims.jsonl"
    _write_lines(ledger, [{"id": "a", "kind": "claim"}])
    li.snapshot_ledger(ledger)
    second = _write_lines(ledger, [{"id": "a", "kind": "claim"}, {"id": "b", "kind": "claim"}])
    li.snapshot_ledger(ledger)
    _write_lines(ledger, [{"id": "z", "kind": "claim"}])
    restored = li.rollback_migration(ledger_path=ledger)
    assert restored in li.list_snapshots(ledger)
    assert ledger.read_bytes() == second


def test_write_ledger_snapshots_pre_state_for_rollback(tmp_path):
    entries = li.read_ledger(REPO / li.LEDGER_REL)[:2]
    assert entries, "the real ledger is empty"
    target = tmp_path / "claims.jsonl"
    li.write_ledger(REPO, entries, ledger_path=target)
    assert target.is_file()
    snapshots = li.list_snapshots(target)
    assert snapshots, "write_ledger left no rollback snapshot"
    li.rollback_migration(ledger_path=target)
    assert not target.exists(), "rollback did not restore the pre-migration absence"
