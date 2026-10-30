"""Spec 083 (T011) — R2 dataset-bundle plumbing tests.

The hydration contract (claim C083-13): verify the FULL manifest
before the swap, swap atomically, never serve a mixture of two
manifests. Job state rides inside the bundle's ``glossa.db`` artifact
and the ``jobs_running`` guard reports it (FR-010 / C083-10).

All transports here are local stand-ins — no R2 access is needed to
prove the hydration logic.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from glossa_lab.cloud_bundles import (
    BundleError,
    DirectoryTransport,
    Manifest,
    build_manifest,
    count_running_jobs,
    hydrate,
    jobs_running,
    served_manifest,
    sha256_bytes,
)


def _make_bundle(bucket: Path, files: dict[str, bytes], bundle_id: str) -> Manifest:
    """Write *files* into a bucket dir and place a manifest over them."""
    bucket.mkdir(parents=True, exist_ok=True)
    for rel, data in files.items():
        target = bucket / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    manifest = build_manifest(
        bucket,
        bundle_id=bundle_id,
        source_commit="a" * 40,
        built_at="2026-10-30T00:00:00+00:00",
    )
    (bucket / "manifest.json").write_bytes(manifest.to_bytes())
    return manifest


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(root)): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


# ── Manifest format ──────────────────────────────────────────────────


def test_manifest_roundtrip_and_fields(tmp_path):
    manifest = _make_bundle(
        tmp_path / "bucket", {"glossa.db": b"db-bytes", "notes/x.txt": b"hi"},
        "bundle-1",
    )
    assert manifest.bundle_id == "bundle-1"
    assert manifest.source_commit == "a" * 40
    assert manifest.built_at == "2026-10-30T00:00:00+00:00"
    by_path = {a.path: a for a in manifest.artifacts}
    assert by_path["glossa.db"].sha256 == sha256_bytes(b"db-bytes")
    assert by_path["glossa.db"].size == 8
    assert Manifest.from_bytes(manifest.to_bytes()) == manifest


def test_manifest_rejects_traversal_paths():
    with pytest.raises(BundleError):
        Manifest.from_dict({
            "format": "glossa-dataset-bundle/1",
            "bundle_id": "b",
            "built_at": "2026-10-30T00:00:00+00:00",
            "source_commit": "abc",
            "artifacts": [
                {"path": "../escape.txt", "sha256": "0" * 64, "size": 1},
            ],
        })


# ── Hydration: happy path + atomic swap ──────────────────────────────


def test_hydrate_serves_exactly_the_new_manifest(tmp_path):
    data_dir = tmp_path / "data"
    v1 = _make_bundle(
        tmp_path / "bucket1",
        {"glossa.db": b"v1-db", "only-in-v1.txt": b"old"},
        "bundle-v1",
    )
    served = hydrate(DirectoryTransport(tmp_path / "bucket1"), data_dir)
    assert served == v1
    assert served_manifest(data_dir) == v1
    assert (data_dir / "glossa.db").read_bytes() == b"v1-db"

    v2 = _make_bundle(
        tmp_path / "bucket2",
        {"glossa.db": b"v2-db", "only-in-v2.txt": b"new"},
        "bundle-v2",
    )
    served = hydrate(DirectoryTransport(tmp_path / "bucket2"), data_dir)
    assert served == v2
    assert served_manifest(data_dir) == v2
    # Exactly one manifest is served: no v1-only file survives the swap.
    assert not (data_dir / "only-in-v1.txt").exists()
    assert (data_dir / "only-in-v2.txt").read_bytes() == b"new"
    assert (data_dir / "glossa.db").read_bytes() == b"v2-db"
    # No staging/backup siblings are left behind.
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "bucket1", "bucket2", "data",
    ]


# ── Hydration: verification failure → no swap ────────────────────────


def test_verify_failure_leaves_old_dataset_intact(tmp_path):
    data_dir = tmp_path / "data"
    _make_bundle(tmp_path / "bucket1", {"glossa.db": b"good-db"}, "bundle-v1")
    hydrate(DirectoryTransport(tmp_path / "bucket1"), data_dir)
    before = _snapshot(data_dir)

    bucket2 = tmp_path / "bucket2"
    _make_bundle(bucket2, {"glossa.db": b"tampered-db"}, "bundle-v2")
    # Corrupt the artifact AFTER the manifest was built over it.
    (bucket2 / "glossa.db").write_bytes(b"tampered-db!")

    with pytest.raises(BundleError, match="SHA-256|size"):
        hydrate(DirectoryTransport(bucket2), data_dir)

    assert _snapshot(data_dir) == before
    assert served_manifest(data_dir).bundle_id == "bundle-v1"


# ── Hydration: interrupted transfer → old dataset intact ─────────────


class _InterruptingTransport:
    """Serves the manifest, then dies mid-transfer (bounded calls)."""

    def __init__(self, inner: DirectoryTransport, fail_after: int) -> None:
        self.inner = inner
        self.fail_after = fail_after
        self.calls = 0

    def fetch(self, key: str) -> bytes:
        self.calls += 1
        if self.calls > self.fail_after:
            raise BundleError("simulated interrupted transfer")
        return self.inner.fetch(key)


def test_interrupted_transfer_leaves_old_dataset_intact(tmp_path):
    data_dir = tmp_path / "data"
    _make_bundle(
        tmp_path / "bucket1",
        {"glossa.db": b"stable-db", "keep.txt": b"keep"},
        "bundle-v1",
    )
    hydrate(DirectoryTransport(tmp_path / "bucket1"), data_dir)
    before = _snapshot(data_dir)

    bucket2 = tmp_path / "bucket2"
    _make_bundle(
        bucket2,
        {"glossa.db": b"new-db", "a.txt": b"a", "b.txt": b"b"},
        "bundle-v2",
    )
    # Manifest + first artifact arrive; the transfer dies after that.
    transport = _InterruptingTransport(DirectoryTransport(bucket2), fail_after=2)
    with pytest.raises(BundleError, match="interrupted"):
        hydrate(transport, data_dir)

    assert _snapshot(data_dir) == before
    assert served_manifest(data_dir).bundle_id == "bundle-v1"
    leftovers = [p.name for p in tmp_path.iterdir() if "hydrate" in p.name]
    assert leftovers == []


# ── Job-state guard (restored before the engine resumes) ─────────────


def _make_jobs_db(path: Path, statuses: list[str]) -> None:
    path.unlink(missing_ok=True)  # each call builds a fresh database file
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE jobs (id TEXT PRIMARY KEY, status TEXT)")
    conn.executemany(
        "INSERT INTO jobs (id, status) VALUES (?, ?)",
        [(f"job-{i}", status) for i, status in enumerate(statuses)],
    )
    conn.commit()
    conn.close()


def test_jobs_running_guard_reads_restored_job_state(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    # Nothing hydrated yet: no database → not running.
    assert jobs_running(data_dir) is False
    assert count_running_jobs(data_dir) == 0

    _make_jobs_db(data_dir / "glossa.db", ["completed", "failed"])
    assert jobs_running(data_dir) is False

    _make_jobs_db(data_dir / "glossa.db", ["completed", "running", "pending"])
    # 'pending' is queued, not running; exactly the running row counts.
    assert count_running_jobs(data_dir) == 1
    assert jobs_running(data_dir) is True


def test_jobs_state_rides_inside_the_bundle(tmp_path):
    bucket = tmp_path / "bucket"
    bucket.mkdir()
    _make_jobs_db(bucket / "glossa.db", ["running"])
    manifest = build_manifest(
        bucket, bundle_id="bundle-jobs", source_commit="b" * 40,
        built_at="2026-10-30T00:00:00+00:00",
    )
    (bucket / "manifest.json").write_bytes(manifest.to_bytes())

    data_dir = tmp_path / "data"
    hydrate(DirectoryTransport(bucket), data_dir)
    # After hydration, before the engine resumes, the guard already
    # sees the restored running job and can suppress sleep.
    assert jobs_running(data_dir) is True


# ── CLI ──────────────────────────────────────────────────────────────


def test_cli_manifest_served_and_jobs_running(tmp_path, capsys):
    from glossa_lab.cloud_bundles import main

    root = tmp_path / "src"
    root.mkdir()
    (root / "glossa.db").write_bytes(b"db")
    out = tmp_path / "manifest.json"
    assert main([
        "manifest", "--root", str(root), "--bundle-id", "b1",
        "--source-commit", "c" * 40, "--out", str(out),
    ]) == 0
    parsed = json.loads(out.read_text())
    assert parsed["bundle_id"] == "b1"
    assert parsed["artifacts"][0]["sha256"] == sha256_bytes(b"db")

    data_dir = tmp_path / "data"
    assert main(["served", "--data-dir", str(data_dir)]) == 3
    capsys.readouterr()
    # No database → jobs-running exits 1 (do not suppress sleep).
    assert main(["jobs-running", "--data-dir", str(data_dir)]) == 1
    assert json.loads(capsys.readouterr().out)["jobs_running"] is False
