"""R2 dataset-bundle plumbing — container side (Spec 083, T011).

A dataset *bundle* is the unit in which research state moves between
the repo/desktop side and the cloud container (spec 083 FR-013,
claim C083-13). A bundle is a set of artifacts (files, addressed by
paths relative to the data-directory root) plus a manifest:

    {
      "format": "glossa-dataset-bundle/1",
      "bundle_id": "<id>",
      "built_at": "<ISO-8601 UTC>",
      "source_commit": "<git SHA the bundle was built from>",
      "artifacts": [
        {"path": "glossa.db", "sha256": "<hex>", "size": 12345},
        ...
      ]
    }

Hydration contract (the interface the app/platform relies on):

* ``hydrate(transport, data_dir, prefix="")`` downloads the manifest
  and **every** artifact into a staging directory beside ``data_dir``,
  verifies each artifact's size and SHA-256 against the manifest, and
  only then swaps: the staging directory is renamed over ``data_dir``
  in one rename (same filesystem), with the previous directory kept
  as a sibling backup until the swap has landed, then removed. The
  served dataset is therefore always exactly one manifest — never a
  mixture of two. Any failure before the swap leaves the previously
  served dataset byte-for-byte intact.
* The bundle's job state is simply the ``jobs`` table inside the
  bundled ``glossa.db`` artifact: because hydration restores the
  whole data directory atomically, job state is back in place before
  the engine resumes. Hydration MUST run before the app starts
  (entrypoint order: hydrate, then launch the backend).
* ``jobs_running(data_dir)`` is the guard the platform consults to
  suppress container sleep (FR-010 / C083-10): it opens the restored
  ``glossa.db`` read-only and reports whether any job row is in
  ``running`` state.
* ``served_manifest(data_dir)`` returns the manifest of the dataset
  currently in place (the manifest file is stored at the root of the
  served directory during hydration), or ``None`` when no bundle has
  been hydrated there. This backs the Status surface's bundle-id /
  source-commit / hydrated-at display (C083-13).

Transports are deliberately tiny (``fetch(key) -> bytes``) so the
hydration logic is fully unit-testable without R2:

* ``DirectoryTransport`` — a local directory standing in for a bucket
  (tests, the local production-shaped build).
* ``R2Transport`` — R2 over its S3-compatible HTTPS API. boto3 is not
  among the backend dependencies (checked ``backend/pyproject.toml``
  for T011), so this client signs requests with AWS Signature
  Version 4 using only the standard library. Credentials come from
  the environment (``GLOSSA_R2_ACCESS_KEY_ID`` /
  ``GLOSSA_R2_SECRET_ACCESS_KEY``, or the conventional
  ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY``); the endpoint
  from ``GLOSSA_R2_ENDPOINT`` and the bucket from
  ``GLOSSA_R2_BUCKET`` (default ``glossa-datasets``).

CLI (operator / entrypoint use)::

    python -m glossa_lab.cloud_bundles manifest --root DIR \
        --bundle-id ID --source-commit SHA [--out FILE] [PATH ...]
    python -m glossa_lab.cloud_bundles hydrate --data-dir DIR \
        (--from-dir DIR | --r2) [--prefix PREFIX]
    python -m glossa_lab.cloud_bundles served --data-dir DIR
    python -m glossa_lab.cloud_bundles jobs-running --data-dir DIR
        # exit 0 when jobs are running (suppress sleep), 1 when not
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import shutil
import sqlite3
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

BUNDLE_FORMAT = "glossa-dataset-bundle/1"
MANIFEST_NAME = "manifest.json"
DEFAULT_BUCKET = "glossa-datasets"
_HTTP_TIMEOUT_SECONDS = 60


class BundleError(Exception):
    """A bundle is malformed, fails verification, or cannot hydrate."""


# ── Manifest ─────────────────────────────────────────────────────────


def _check_artifact_path(path: str) -> str:
    """Validate an artifact path: relative, no traversal, no manifest."""
    if not path or path != path.strip():
        raise BundleError(f"invalid artifact path: {path!r}")
    pure = Path(path)
    if pure.is_absolute() or ".." in pure.parts or path == MANIFEST_NAME:
        raise BundleError(f"unsafe artifact path: {path!r}")
    return path


@dataclass(frozen=True)
class Artifact:
    path: str
    sha256: str
    size: int

    def to_dict(self) -> dict[str, Any]:
        return {"path": self.path, "sha256": self.sha256, "size": self.size}

    @classmethod
    def from_dict(cls, data: Any) -> Artifact:
        if not isinstance(data, dict):
            raise BundleError(f"artifact entry is not an object: {data!r}")
        path = _check_artifact_path(str(data.get("path", "")))
        sha = str(data.get("sha256", "")).lower()
        if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise BundleError(f"artifact {path!r}: bad sha256 {sha!r}")
        size = data.get("size")
        if not isinstance(size, int) or size < 0:
            raise BundleError(f"artifact {path!r}: bad size {size!r}")
        return cls(path=path, sha256=sha, size=size)


@dataclass(frozen=True)
class Manifest:
    bundle_id: str
    built_at: str
    source_commit: str
    artifacts: tuple[Artifact, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": BUNDLE_FORMAT,
            "bundle_id": self.bundle_id,
            "built_at": self.built_at,
            "source_commit": self.source_commit,
            "artifacts": [a.to_dict() for a in self.artifacts],
        }

    def to_bytes(self) -> bytes:
        return (json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n").encode()

    @classmethod
    def from_dict(cls, data: Any) -> Manifest:
        if not isinstance(data, dict):
            raise BundleError("manifest is not a JSON object")
        if data.get("format") != BUNDLE_FORMAT:
            raise BundleError(f"unknown bundle format: {data.get('format')!r}")
        bundle_id = str(data.get("bundle_id", "")).strip()
        source_commit = str(data.get("source_commit", "")).strip()
        built_at = str(data.get("built_at", "")).strip()
        if not bundle_id or not source_commit or not built_at:
            raise BundleError("manifest lacks bundle_id / built_at / source_commit")
        raw_artifacts = data.get("artifacts")
        if not isinstance(raw_artifacts, list):
            raise BundleError("manifest artifacts is not a list")
        artifacts = tuple(Artifact.from_dict(a) for a in raw_artifacts)
        paths = [a.path for a in artifacts]
        if len(paths) != len(set(paths)):
            raise BundleError("manifest lists an artifact path twice")
        return cls(
            bundle_id=bundle_id,
            built_at=built_at,
            source_commit=source_commit,
            artifacts=artifacts,
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> Manifest:
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            raise BundleError(f"manifest is not valid JSON: {exc}") from exc
        return cls.from_dict(data)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(
    root: Path,
    bundle_id: str,
    source_commit: str,
    artifact_paths: list[str] | None = None,
    built_at: str | None = None,
) -> Manifest:
    """Build a manifest over files under *root*.

    With ``artifact_paths=None`` every file under *root* is included
    (recursively, excluding the manifest file itself).
    """
    root = Path(root)
    if artifact_paths is None:
        artifact_paths = sorted(
            str(p.relative_to(root))
            for p in root.rglob("*")
            if p.is_file() and p.name != MANIFEST_NAME
        )
    artifacts = []
    for rel in artifact_paths:
        _check_artifact_path(rel)
        full = root / rel
        if not full.is_file():
            raise BundleError(f"artifact not found under bundle root: {rel!r}")
        artifacts.append(
            Artifact(path=rel, sha256=sha256_file(full), size=full.stat().st_size)
        )
    return Manifest(
        bundle_id=bundle_id,
        built_at=built_at or datetime.now(timezone.utc).isoformat(),
        source_commit=source_commit,
        artifacts=tuple(artifacts),
    )


# ── Transports ───────────────────────────────────────────────────────


class BundleTransport(Protocol):
    """Anything that can fetch one bundle object by key."""

    def fetch(self, key: str) -> bytes:
        """Return the object's bytes; raise BundleError when absent."""
        ...


class DirectoryTransport:
    """A local directory standing in for a bucket (tests / local build)."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def fetch(self, key: str) -> bytes:
        pure = Path(key)
        if pure.is_absolute() or ".." in pure.parts:
            raise BundleError(f"unsafe object key: {key!r}")
        target = self.root / key
        if not target.is_file():
            raise BundleError(f"object not found: {key!r}")
        return target.read_bytes()


def _sigv4_headers(
    *,
    method: str,
    host: str,
    path: str,
    access_key: str,
    secret_key: str,
    region: str = "auto",
    service: str = "s3",
    now: datetime | None = None,
) -> dict[str, str]:
    """AWS Signature Version 4 headers for an unsigned-payload GET."""
    moment = now or datetime.now(timezone.utc)
    amz_date = moment.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = moment.strftime("%Y%m%d")
    payload_hash = hashlib.sha256(b"").hexdigest()
    signed_headers = "host;x-amz-content-sha256;x-amz-date"
    canonical_headers = (
        f"host:{host}\n"
        f"x-amz-content-sha256:{payload_hash}\n"
        f"x-amz-date:{amz_date}\n"
    )
    canonical_request = "\n".join(
        [method, path, "", canonical_headers, signed_headers, payload_hash]
    )
    scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amz_date,
            scope,
            hashlib.sha256(canonical_request.encode()).hexdigest(),
        ]
    )

    def _sign(key: bytes, msg: str) -> bytes:
        return hmac.new(key, msg.encode(), hashlib.sha256).digest()

    k_date = _sign(("AWS4" + secret_key).encode(), date_stamp)
    k_region = _sign(k_date, region)
    k_service = _sign(k_region, service)
    k_signing = _sign(k_service, "aws4_request")
    signature = hmac.new(
        k_signing, string_to_sign.encode(), hashlib.sha256
    ).hexdigest()
    return {
        "Authorization": (
            f"AWS4-HMAC-SHA256 Credential={access_key}/{scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        ),
        "x-amz-date": amz_date,
        "x-amz-content-sha256": payload_hash,
    }


class R2Transport:
    """Cloudflare R2 via its S3-compatible HTTPS API (stdlib signing)."""

    def __init__(
        self,
        endpoint: str,
        bucket: str,
        access_key: str,
        secret_key: str,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key

    @classmethod
    def from_env(cls) -> R2Transport:
        endpoint = os.environ.get("GLOSSA_R2_ENDPOINT", "").strip()
        bucket = os.environ.get("GLOSSA_R2_BUCKET", DEFAULT_BUCKET).strip()
        access_key = (
            os.environ.get("GLOSSA_R2_ACCESS_KEY_ID")
            or os.environ.get("AWS_ACCESS_KEY_ID", "")
        ).strip()
        secret_key = (
            os.environ.get("GLOSSA_R2_SECRET_ACCESS_KEY")
            or os.environ.get("AWS_SECRET_ACCESS_KEY", "")
        ).strip()
        if not endpoint or not access_key or not secret_key:
            raise BundleError(
                "R2 transport needs GLOSSA_R2_ENDPOINT and R2 credentials "
                "in the environment (GLOSSA_R2_ACCESS_KEY_ID / "
                "GLOSSA_R2_SECRET_ACCESS_KEY or the AWS_* pair)"
            )
        return cls(endpoint, bucket, access_key, secret_key)

    def fetch(self, key: str) -> bytes:
        quoted_key = urllib.parse.quote(key, safe="/")
        path = f"/{self.bucket}/{quoted_key}"
        url = f"{self.endpoint}{path}"
        host = urllib.parse.urlparse(self.endpoint).netloc
        headers = _sigv4_headers(
            method="GET",
            host=host,
            path=path,
            access_key=self.access_key,
            secret_key=self.secret_key,
        )
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(  # noqa: S310 - endpoint is operator config
                request, timeout=_HTTP_TIMEOUT_SECONDS
            ) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            raise BundleError(f"R2 fetch of {key!r} failed: HTTP {exc.code}") from exc
        except Exception as exc:  # noqa: BLE001
            raise BundleError(f"R2 fetch of {key!r} failed: {exc}") from exc


# ── Hydration ────────────────────────────────────────────────────────


def _verify_artifact(manifest_path: str, data: bytes, artifact: Artifact) -> None:
    if len(data) != artifact.size:
        raise BundleError(
            f"artifact {artifact.path!r}: size {len(data)} != manifest {artifact.size}"
        )
    if sha256_bytes(data) != artifact.sha256:
        raise BundleError(f"artifact {artifact.path!r}: SHA-256 mismatch")


def hydrate(
    transport: BundleTransport,
    data_dir: str | Path,
    prefix: str = "",
    manifest_key: str = MANIFEST_NAME,
) -> Manifest:
    """Hydrate *data_dir* from the bundle reachable via *transport*.

    Verifies the full manifest before the swap and swaps atomically;
    see the module docstring for the contract. Returns the manifest
    now being served. On any failure the previously served dataset is
    left untouched and the staging directory is removed.
    """
    data_dir = Path(data_dir)
    parent = data_dir.parent
    parent.mkdir(parents=True, exist_ok=True)
    key_prefix = prefix.strip("/")

    def _key(name: str) -> str:
        return f"{key_prefix}/{name}" if key_prefix else name

    manifest = Manifest.from_bytes(transport.fetch(_key(manifest_key)))

    staging = parent / f".{data_dir.name}.hydrate-{os.getpid()}"
    backup = parent / f".{data_dir.name}.previous-{os.getpid()}"
    for stale in (staging, backup):
        if stale.exists():
            shutil.rmtree(stale)
    staging.mkdir(parents=True)
    try:
        # Download and verify EVERY artifact before anything is served.
        for artifact in manifest.artifacts:
            data = transport.fetch(_key(artifact.path))
            _verify_artifact(artifact.path, data, artifact)
            target = staging / artifact.path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        # The served directory carries its own manifest, so exactly one
        # manifest describes what is being served at any moment.
        (staging / MANIFEST_NAME).write_bytes(manifest.to_bytes())

        # Atomic swap: both renames are on the same filesystem (the
        # staging/backup dirs are siblings of data_dir).
        had_previous = data_dir.exists()
        if had_previous:
            os.rename(data_dir, backup)
        try:
            os.rename(staging, data_dir)
        except Exception:
            if had_previous and backup.exists() and not data_dir.exists():
                os.rename(backup, data_dir)  # roll back
            raise
        if backup.exists():
            shutil.rmtree(backup)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def served_manifest(data_dir: str | Path) -> Manifest | None:
    """The manifest of the dataset currently served from *data_dir*."""
    manifest_file = Path(data_dir) / MANIFEST_NAME
    if not manifest_file.is_file():
        return None
    return Manifest.from_bytes(manifest_file.read_bytes())


def count_running_jobs(data_dir: str | Path) -> int:
    """Number of jobs in ``running`` state in the restored dataset.

    Reads ``<data_dir>/glossa.db`` read-only; a missing database or
    jobs table (nothing hydrated yet) counts as zero.
    """
    db_path = Path(data_dir) / "glossa.db"
    if not db_path.is_file():
        return 0
    uri = f"file:{urllib.parse.quote(str(db_path))}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True, timeout=5)
        try:
            row = conn.execute(
                "SELECT COUNT(*) FROM jobs WHERE status = 'running'"
            ).fetchone()
        finally:
            conn.close()
    except sqlite3.Error:
        return 0
    return int(row[0]) if row else 0


def jobs_running(data_dir: str | Path) -> bool:
    """Sleep-suppression guard (FR-010): True while any job runs."""
    return count_running_jobs(data_dir) > 0


# ── CLI ──────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="glossa_lab.cloud_bundles",
        description="Spec 083 dataset-bundle manifest / hydration tooling.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_manifest = sub.add_parser("manifest", help="build a manifest over a directory")
    p_manifest.add_argument("--root", required=True)
    p_manifest.add_argument("--bundle-id", required=True)
    p_manifest.add_argument("--source-commit", required=True)
    p_manifest.add_argument("--out")
    p_manifest.add_argument("paths", nargs="*")

    p_hydrate = sub.add_parser("hydrate", help="verify + atomically hydrate a data dir")
    p_hydrate.add_argument("--data-dir", required=True)
    p_hydrate.add_argument("--from-dir", help="local bucket stand-in directory")
    p_hydrate.add_argument("--r2", action="store_true", help="fetch from R2 (env config)")
    p_hydrate.add_argument("--prefix", default="")

    p_served = sub.add_parser("served", help="print the served manifest, if any")
    p_served.add_argument("--data-dir", required=True)

    p_jobs = sub.add_parser(
        "jobs-running", help="exit 0 if jobs are running in the dataset, else 1"
    )
    p_jobs.add_argument("--data-dir", required=True)

    args = parser.parse_args(argv)

    if args.command == "manifest":
        manifest = build_manifest(
            Path(args.root),
            bundle_id=args.bundle_id,
            source_commit=args.source_commit,
            artifact_paths=args.paths or None,
        )
        text = manifest.to_bytes().decode()
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
        else:
            sys.stdout.write(text)
        return 0

    if args.command == "hydrate":
        if args.from_dir:
            transport: BundleTransport = DirectoryTransport(args.from_dir)
        elif args.r2:
            transport = R2Transport.from_env()
        else:
            parser.error("hydrate needs --from-dir or --r2")
        manifest = hydrate(transport, Path(args.data_dir), prefix=args.prefix)
        print(
            json.dumps(
                {
                    "hydrated": manifest.bundle_id,
                    "source_commit": manifest.source_commit,
                    "artifacts": len(manifest.artifacts),
                }
            )
        )
        return 0

    if args.command == "served":
        manifest = served_manifest(Path(args.data_dir))
        if manifest is None:
            print(json.dumps({"served": None}))
            return 3
        print(json.dumps(manifest.to_dict(), indent=2, sort_keys=True))
        return 0

    if args.command == "jobs-running":
        count = count_running_jobs(Path(args.data_dir))
        print(json.dumps({"jobs_running": count > 0, "running": count}))
        return 0 if count > 0 else 1

    return 2  # pragma: no cover - argparse enforces the subcommand set


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
