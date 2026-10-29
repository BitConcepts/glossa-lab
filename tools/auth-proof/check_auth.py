#!/usr/bin/env python3
"""Spec 082 auth proof kit — verify a running install enforces the
per-install API token exactly as the spec requires.

Stdlib only, no retries: one pass, six legs, every request bounded
by ``--timeout``. Output is one ``AUTH_PROOF`` marker line per leg
plus a final ``AUTH_PROOF_RESULT PASS|FAIL`` line; the exit code is
0 only when every leg passes. The token value is never printed —
only its SHA-256 fingerprint (first 8 hex chars), matching
``glossa_lab.auth``.

Legs (specs/082-api-token-auth/spec.md, FR-001/003/007):

1. health is open without a token and reports ``auth: token``;
2. a data route without a token answers 401 (+ ``WWW-Authenticate``);
3. a data route with a wrong token answers 401;
4. a data route with the install token answers 200;
5. the OpenAPI schema identifies the app ("Glossa Lab") with the
   install token, and answers 401 without one;
6. a state-changing POST without a token answers 401.

Usage:
    python tools/auth-proof/check_auth.py [--base-url URL]
        (--token VALUE | --token-file PATH)
    # or set GLOSSA_API_TOKEN in the environment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DATA_ROUTE = "/api/v1/projects"
POST_PROBE = "/api/v1/terminal/log/frontend"


def fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]


def request(
    base_url: str, method: str, path: str, token: str | None, timeout: float
) -> tuple[int, dict, bytes]:
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        base_url.rstrip("/") + path, method=method, headers=headers
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()
    except (urllib.error.URLError, OSError):
        return 0, {}, b""


def request_json(
    base_url: str, method: str, path: str, token: str | None, timeout: float
) -> tuple[int, dict, dict]:
    status, headers, body = request(base_url, method, path, token, timeout)
    try:
        parsed = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return status, headers, {}
    return status, headers, parsed if isinstance(parsed, dict) else {}


def resolve_token(args: argparse.Namespace) -> str:
    if args.token:
        return args.token.strip()
    if args.token_file:
        return Path(args.token_file).read_text(encoding="utf-8").strip()
    env_token = os.environ.get("GLOSSA_API_TOKEN", "").strip()
    if env_token:
        return env_token
    raise SystemExit(
        "no token supplied: pass --token or --token-file, "
        "or set GLOSSA_API_TOKEN"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default=os.environ.get("GLOSSA_BASE_URL", "http://127.0.0.1:8001"),
    )
    parser.add_argument("--token", default="")
    parser.add_argument("--token-file", default="")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args(argv)

    token = resolve_token(args)
    wrong_token = "proof-kit-wrong-token"
    failures = 0

    def leg(name: str, ok: bool, detail: str) -> None:
        nonlocal failures
        failures += 0 if ok else 1
        print(f"AUTH_PROOF {name} {'PASS' if ok else 'FAIL'} {detail}")

    # Leg 1 — health open + auth mode reported.
    status, _headers, health = request_json(
        args.base_url, "GET", "/api/v1/health", None, args.timeout
    )
    leg(
        "health-open",
        status == 200 and health.get("auth") == "token",
        f"status={status} auth={health.get('auth')!r}",
    )

    # Leg 2 — data route refuses a missing token, Bearer challenge.
    status, headers, _ = request(
        args.base_url, "GET", DATA_ROUTE, None, args.timeout
    )
    leg(
        "no-token-401",
        status == 401 and headers.get("WWW-Authenticate") == "Bearer",
        f"status={status} www-authenticate={headers.get('WWW-Authenticate')!r}",
    )

    # Leg 3 — data route refuses a wrong token.
    status, _headers, _ = request(
        args.base_url, "GET", DATA_ROUTE, wrong_token, args.timeout
    )
    leg("wrong-token-401", status == 401, f"status={status}")

    # Leg 4 — data route accepts the install token.
    status, _headers, _ = request(
        args.base_url, "GET", DATA_ROUTE, token, args.timeout
    )
    leg("install-token-200", status == 200, f"status={status}")

    # Leg 5 — schema identity with the token; gated without it.
    status, _headers, openapi = request_json(
        args.base_url, "GET", "/openapi.json", token, args.timeout
    )
    title = (openapi.get("info") or {}).get("title")
    anon_status, _h, _b = request(
        args.base_url, "GET", "/openapi.json", None, args.timeout
    )
    leg(
        "schema-identity",
        status == 200 and title == "Glossa Lab" and anon_status == 401,
        f"status={status} title={title!r} anonymous={anon_status}",
    )

    # Leg 6 — a state-changing POST refuses a missing token.
    status, _headers, _ = request(
        args.base_url, "POST", POST_PROBE, None, args.timeout
    )
    leg("post-no-token-401", status == 401, f"status={status}")

    print(f"AUTH_PROOF token fingerprint={fingerprint(token)}")
    print(f"AUTH_PROOF_RESULT {'PASS' if failures == 0 else 'FAIL'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
