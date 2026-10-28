#!/usr/bin/env python3
"""Bounded identity health check for the Glossa Lab backend.

Liveness alone (HTTP 200 on /docs) does not prove that the process
on the port is Glossa Lab. This check requires all three:

* ``GET /docs`` answers HTTP 200;
* ``GET /api/v1/health`` reports a healthy/degraded status and a
  version string;
* ``GET /openapi.json`` identifies the application as "Glossa Lab"
  with the same version as the health payload.

Every wait is bounded (attempt count and per-request timeout), per
the project rule that polling loops carry a deadline. The result is
printed as one JSON object; with ``--state-dir`` it is also written
to ``health-status.json`` in that directory.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

EXPECTED_TITLE = "Glossa Lab"
OK_STATUSES = ("healthy", "degraded")


def fetch(url: str, timeout: float) -> tuple[int, bytes]:
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except (urllib.error.URLError, OSError):
        # Connection refused / timeout while the backend is still
        # starting: report "no answer" so the caller retries within
        # its bounded attempt budget instead of crashing.
        return 0, b""


def fetch_json(url: str, timeout: float) -> tuple[int, dict]:
    status, body = fetch(url, timeout)
    try:
        parsed = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return status, {}
    return status, parsed if isinstance(parsed, dict) else {}


def validate_identity(health: dict, openapi: dict) -> list[str]:
    """Return the list of identity problems (empty means verified)."""
    errors: list[str] = []
    if health.get("status") not in OK_STATUSES:
        errors.append(f"health status is {health.get('status')!r}, expected healthy/degraded")
    version = health.get("version")
    if not isinstance(version, str) or not version:
        errors.append("health payload carries no version string")
    info = openapi.get("info")
    if not isinstance(info, dict):
        errors.append("openapi payload carries no info object")
        return errors
    if info.get("title") != EXPECTED_TITLE:
        errors.append(f"openapi title is {info.get('title')!r}, expected {EXPECTED_TITLE!r}")
    if isinstance(version, str) and version and info.get("version") != version:
        errors.append(
            f"openapi version {info.get('version')!r} != health version {version!r}"
        )
    return errors


def check_once(base_url: str, timeout: float) -> tuple[bool, dict]:
    docs_status, _ = fetch(f"{base_url}/docs", timeout)
    _, health = fetch_json(f"{base_url}/api/v1/health", timeout)
    _, openapi = fetch_json(f"{base_url}/openapi.json", timeout)
    errors = validate_identity(health, openapi)
    if docs_status != 200:
        errors.append(f"/docs returned HTTP {docs_status}, expected 200")
    result = {
        "ok": not errors,
        "base_url": base_url,
        "docs_status": docs_status,
        "health": health,
        "app_title": (openapi.get("info") or {}).get("title"),
        "errors": errors,
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return not errors, result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default=os.environ.get("GLOSSA_BASE_URL", "http://127.0.0.1:8001"),
    )
    parser.add_argument("--attempts", type=int, default=30)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--state-dir", default=os.environ.get("GLOSSA_STATE_DIR", ""))
    args = parser.parse_args(argv)

    attempts = max(1, args.attempts)
    result: dict = {}
    ok = False
    for attempt in range(1, attempts + 1):
        ok, result = check_once(args.base_url.rstrip("/"), args.timeout)
        result["attempt"] = attempt
        if ok:
            break
        if attempt < attempts:
            time.sleep(max(0.0, args.interval))
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.state_dir:
        state_dir = Path(args.state_dir)
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "health-status.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if ok and (state_dir / "OWNER_NEEDED").exists():
            (state_dir / "OWNER_NEEDED").unlink()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
