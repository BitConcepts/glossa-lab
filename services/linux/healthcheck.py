#!/usr/bin/env python3
"""Bounded identity health check for the Glossa Lab backend.

Liveness alone (HTTP 200 on /docs) does not prove that the process
on the port is Glossa Lab. This check requires all three:

* ``GET /docs`` answers HTTP 200;
* ``GET /api/v1/health`` reports a healthy/degraded status and a
  version string;
* ``GET /openapi.json`` identifies the application as "Glossa Lab"
  with the same version as the health payload.

Since Spec 082 the schema surfaces (/docs, /openapi.json) are
token-gated while health stays open. The check resolves this
install's API token (GLOSSA_API_TOKEN, then GLOSSA_TOKEN_FILE,
then the candidate token files) and presents it on those two legs
only. When the backend reports ``auth: token`` and no token can be
resolved, the check fails with a named error listing every source
tried — an unauthenticated 401 is never mistaken for downtime or
for a wrong process.

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


def token_candidates() -> list[tuple[str, Path]]:
    """(description, path) token-file candidates in resolution order."""
    candidates: list[tuple[str, Path]] = []
    named = os.environ.get("GLOSSA_TOKEN_FILE", "").strip()
    if named:
        candidates.append((f"GLOSSA_TOKEN_FILE={named}", Path(named).expanduser()))
    data_dir = os.environ.get("GLOSSA_DATA_DIR", "").strip()
    if data_dir:
        candidates.append(
            (f"GLOSSA_DATA_DIR={data_dir}", Path(data_dir).expanduser() / "api_token")
        )
    if sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA", "")
        if local:
            candidates.append(
                ("installed data dir", Path(local) / "GlossaLab" / "data" / "api_token")
            )
    elif sys.platform == "darwin":
        candidates.append(
            (
                "installed data dir",
                Path.home()
                / "Library"
                / "Application Support"
                / "GlossaLab"
                / "data"
                / "api_token",
            )
        )
    else:
        xdg = os.environ.get("XDG_DATA_HOME", "").strip()
        base = Path(xdg).expanduser() if xdg else Path.home() / ".local" / "share"
        candidates.append(("installed data dir", base / "glossa-lab" / "api_token"))
    candidates.append(
        ("repo data dir", Path(__file__).resolve().parents[2] / "backend" / "data" / "api_token")
    )
    return candidates


def resolve_token() -> tuple[str | None, list[str]]:
    """Resolve the install API token; also return what was tried.

    The tried list carries descriptions and paths only — never a
    token value — so it is safe to print in a failure.
    """
    env_token = os.environ.get("GLOSSA_API_TOKEN", "").strip()
    if env_token:
        return env_token, ["GLOSSA_API_TOKEN (set)"]
    tried = ["GLOSSA_API_TOKEN (unset)"]
    for description, path in token_candidates():
        tried.append(f"{description}: {path}")
        try:
            if path.is_file():
                value = path.read_text(encoding="utf-8").strip()
                if value:
                    return value, tried
        except OSError:
            continue
    return None, tried


def fetch(url: str, timeout: float, headers: dict | None = None) -> tuple[int, bytes]:
    request = urllib.request.Request(url, method="GET", headers=headers or {})
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


def fetch_json(url: str, timeout: float, headers: dict | None = None) -> tuple[int, dict]:
    status, body = fetch(url, timeout, headers=headers)
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
    token, tried = resolve_token()
    auth_headers = {"Authorization": f"Bearer {token}"} if token else None
    docs_status, _ = fetch(f"{base_url}/docs", timeout, headers=auth_headers)
    _, health = fetch_json(f"{base_url}/api/v1/health", timeout)
    _, openapi = fetch_json(f"{base_url}/openapi.json", timeout, headers=auth_headers)
    errors = validate_identity(health, openapi)
    if docs_status != 200:
        errors.append(f"/docs returned HTTP {docs_status}, expected 200")
    if token is None and health.get("auth") == "token":
        errors.append(
            "backend requires an API token (health reports auth: token) "
            "but no token could be resolved; tried: " + "; ".join(tried)
        )
    if token is not None and docs_status == 401:
        errors.append(
            "the resolved API token was refused (HTTP 401 on /docs); "
            "the token file may be stale — rotate it "
            "(python -m glossa_lab.auth rotate) or update GLOSSA_API_TOKEN"
        )
    result = {
        "ok": not errors,
        "base_url": base_url,
        "docs_status": docs_status,
        "health": health,
        "app_title": (openapi.get("info") or {}).get("title"),
        "token_resolved": token is not None,
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
