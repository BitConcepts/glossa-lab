"""Spec 082 — per-install API token authentication.

Claim coverage (specs/082-api-token-auth/aee-claims.json):

- C082-1  enforcement matrix: route families x {missing, wrong,
  empty} -> 401, install token -> not 401; plus an enumeration of
  every schema-visible /api route in the built app's OpenAPI
  document, each held to 401 without a token (enforcement is
  middleware-level, so the inventory is derived from the app,
  not a hand list).
- C082-2  token generation (CSPRNG, >= 43 chars, unique), file
  perms 0600, non-disclosure (token in no response body, no log
  line, never reflected, never accepted via query string).
- C082-3  (backend side) the in-repo MCP client and the in-process
  self-callers (cli_bridge) present the token. Tray + healthcheck
  legs live in tests/test_tray_token_auth.py (consumers PR).
- C082-4  rotation: atomic, byte-stable data dir, old token refused
  and new token accepted by the SAME running app (no restart), and
  the operator CLI never prints the value.
- C082-5  health posture: open, field set pinned to the identity
  set + the auth mode word; /docs, /redoc, /openapi.json gated.
- C082-6  no silent open state: dev-mode app enforces (this whole
  suite runs in dev mode), a missing token file self-generates and
  still enforces, and the only open configuration is the named
  GLOSSA_API_AUTH=off switch — startup warning + health report.

The session token comes from the conftest seam (GLOSSA_API_TOKEN).
"""

from __future__ import annotations

import logging
import os
import re
import stat
import types

import pytest
from fastapi.testclient import TestClient

from glossa_lab import auth
from glossa_lab.config import get_settings
from glossa_lab.main import create_app

TEST_TOKEN = os.environ["GLOSSA_API_TOKEN"]  # conftest seam value
WRONG_TOKEN = "wrong-token-that-is-not-the-install-token"


def _bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _anon_client(app) -> TestClient:
    """A TestClient presenting NO Authorization header by default."""
    c = TestClient(app)
    if "Authorization" in c.headers:
        del c.headers["Authorization"]
    return c


def _route_table(client) -> list[tuple[str, str]]:
    """(method, concrete path) for every schema-visible /api route.

    Read from the app's own OpenAPI document — the same source the
    MCP drift guard (tests/test_glossa_mcp.py) uses — because
    Starlette 1.x keeps included routers as lazy wrappers in
    ``app.routes`` rather than a flat route list.
    """
    spec = client.get("/openapi.json").json()
    found: set[tuple[str, str]] = set()
    for path, operations in spec.get("paths", {}).items():
        if not path.startswith("/api/") or path == "/api/v1/health":
            continue
        concrete = re.sub(r"\{[^}]+\}", "1", path)
        for method in operations:
            if method.upper() in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
                found.add((method.upper(), concrete))
    return sorted(found)


def _pick(client, prefix: str, method: str) -> str:
    """The shortest concrete route under ``prefix`` for ``method``."""
    candidates = [
        path
        for m, path in _route_table(client)
        if m == method and path.startswith(prefix)
    ]
    if not candidates:
        raise AssertionError(f"no {method} route under {prefix}")
    return sorted(candidates, key=lambda p: (len(p), p))[0]


# ── C082-1: enforcement matrix ────────────────────────────────────

FAMILIES = [
    ("GET", "/api/v1/projects"),
    ("GET", "/api/v1/spec-studies"),
    ("POST", "/api/v1/studies"),
    ("POST", "/api/v1/terminal"),
    ("GET", "/api/v1/settings"),
    ("POST", "/api/v1/shutdown"),
    ("GET", "/api/v1/indus-evidence"),
    ("GET", "/api/v1/jobs"),
]


@pytest.mark.parametrize("method,prefix", FAMILIES)
def test_route_family_matrix(app, client, method, prefix):
    path = _pick(client, prefix, method)
    anon = _anon_client(app)
    assert anon.request(method, path).status_code == 401
    assert (
        anon.request(method, path, headers=_bearer(WRONG_TOKEN)).status_code
        == 401
    )
    assert (
        anon.request(method, path, headers={"Authorization": "Bearer "})
        .status_code
        == 401
    )
    assert (
        anon.request(method, path, headers={"Authorization": ""}).status_code
        == 401
    )
    if prefix != "/api/v1/shutdown":
        # The shutdown route's install-token leg runs separately:
        # its handler SIGTERMs the process (see the shim test below).
        assert client.request(method, path).status_code != 401


def test_every_api_route_requires_the_token(app, client):
    routes = _route_table(client)
    assert len(routes) >= 50, f"route enumeration too small: {len(routes)}"
    anon = _anon_client(app)
    failures = [
        (method, path, anon.request(method, path).status_code)
        for method, path in routes
    ]
    failures = [f for f in failures if f[2] != 401]
    assert not failures, f"routes answering without a token: {failures[:10]}"


def test_401_shape_and_no_reflection(app):
    anon = _anon_client(app)
    response = anon.get("/api/v1/projects")
    assert response.status_code == 401
    assert response.headers.get("www-authenticate") == "Bearer"
    assert response.json() == {"detail": auth.UNAUTHORIZED_DETAIL}
    wrong = anon.get("/api/v1/projects", headers=_bearer(WRONG_TOKEN))
    assert wrong.status_code == 401
    assert wrong.json() == response.json()
    assert WRONG_TOKEN not in wrong.text  # presented value never reflected


def test_shutdown_accepts_the_install_token(app, monkeypatch):
    """The shutdown handler os.kill()s the process; shim its ``os``
    so the matrix can prove the middleware admits the install token
    without the test process dying. The falsifier under test is the
    middleware's answer, not the shutdown itself."""
    import glossa_lab.api.shutdown as shutdown_module

    killed: list[int] = []
    fake_os = types.SimpleNamespace(
        kill=lambda pid, sig: killed.append(pid), getpid=os.getpid
    )
    monkeypatch.setattr(shutdown_module, "os", fake_os)
    client = TestClient(app)  # default header = session test token
    response = client.post("/api/v1/shutdown")
    assert response.status_code == 200
    assert killed == [os.getpid()]


# ── C082-5: health posture + schema gating ────────────────────────


def test_health_is_open_and_its_field_set_is_pinned(app, client):
    anon = _anon_client(app)
    response = anon.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert set(data) == {
        "status",
        "version",
        "uptime_seconds",
        "component",
        "build",
        "auth",
    }
    assert data["auth"] == "token"
    assert TEST_TOKEN not in response.text


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_schema_surfaces_require_the_token(app, client, path):
    anon = _anon_client(app)
    assert anon.get(path).status_code == 401
    assert client.get(path).status_code == 200


# ── C082-2: generation, storage, non-disclosure ───────────────────


def test_generated_tokens_are_unique_and_long_enough():
    first, second = auth.generate_token(), auth.generate_token()
    assert first != second
    assert len(first) >= 43 and len(second) >= 43


@pytest.mark.skipif(os.name != "posix", reason="POSIX mode assertion")
def test_token_file_is_mode_0600(tmp_path):
    auth.ensure_token(data_dir=tmp_path)
    mode = stat.S_IMODE((tmp_path / "api_token").stat().st_mode)
    assert mode == 0o600


def test_token_appears_in_no_response_body_or_log(app, client, caplog):
    anon = _anon_client(app)
    with caplog.at_level(logging.DEBUG):
        bodies = [
            client.get("/api/v1/projects").text,
            client.get("/openapi.json").text,
            client.get("/api/v1/health").text,
            anon.get("/api/v1/projects").text,
            anon.get("/api/v1/projects", headers=_bearer(WRONG_TOKEN)).text,
        ]
    for body in bodies:
        assert TEST_TOKEN not in body
    assert TEST_TOKEN not in caplog.text
    assert WRONG_TOKEN not in caplog.text


def test_query_string_token_is_refused(app):
    anon = _anon_client(app)
    assert anon.get(f"/api/v1/projects?token={TEST_TOKEN}").status_code == 401
    assert (
        anon.get(f"/api/v1/projects?api_token={TEST_TOKEN}").status_code == 401
    )


# ── C082-3 (backend side): named consumers present the token ──────


def test_consumer_resolution_prefers_the_env_token():
    assert auth.consumer_token() == TEST_TOKEN
    assert auth.auth_headers() == {"Authorization": f"Bearer {TEST_TOKEN}"}


def test_cli_bridge_sends_the_token(monkeypatch):
    import urllib.request

    from glossa_lab import cli_bridge

    captured: dict = {}

    class _Response:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return b"{}"

    def fake_urlopen(req, timeout=None):  # noqa: ANN001, ANN202
        captured["headers"] = dict(req.header_items())
        return _Response()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    assert cli_bridge._http("GET", "/jobs") == {}
    assert captured["headers"].get("Authorization") == f"Bearer {TEST_TOKEN}"


def test_mcp_client_carries_the_token():
    from glossa_mcp import server as mcp_server

    with mcp_server._get() as client:
        assert client.headers.get("authorization") == f"Bearer {TEST_TOKEN}"


def test_mcp_401_error_names_the_token():
    import httpx

    from glossa_mcp import server as mcp_server

    request = httpx.Request("GET", "http://127.0.0.1:8001/api/v1/jobs")
    response = httpx.Response(401, request=request)
    exc = httpx.HTTPStatusError("401", request=request, response=response)
    rendered = mcp_server._err(exc)
    assert "401" in rendered and "GLOSSA_API_TOKEN" in rendered


# ── File-backed installs: generation, rotation, CLI ───────────────


@pytest.fixture()
def file_backed_app(client, monkeypatch, tmp_path):
    """A fresh app whose expected token comes from a tmp data dir.

    Depends on the session ``client`` first so the session app and
    settings exist before this fixture juggles the settings cache.
    """
    monkeypatch.delenv("GLOSSA_API_TOKEN", raising=False)
    monkeypatch.delenv("GLOSSA_API_AUTH", raising=False)
    monkeypatch.setenv("GLOSSA_DATA_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield create_app(), tmp_path
    get_settings.cache_clear()


def test_missing_token_file_self_generates_and_still_enforces(file_backed_app):
    app2, data_dir = file_backed_app
    anon = _anon_client(app2)
    assert not (data_dir / "api_token").exists()
    assert anon.get("/api/v1/projects").status_code == 401
    token_file = data_dir / "api_token"
    assert token_file.exists()  # generated by the enforcement path
    token = token_file.read_text(encoding="utf-8").strip()
    assert token
    assert (
        anon.get("/api/v1/projects", headers=_bearer(token)).status_code != 401
    )


def test_rotation_takes_effect_without_a_restart(file_backed_app):
    app2, _data_dir = file_backed_app
    anon = _anon_client(app2)
    old = auth.ensure_token()
    assert anon.get("/api/v1/projects", headers=_bearer(old)).status_code != 401
    new = auth.rotate_token()
    assert new != old
    assert anon.get("/api/v1/projects", headers=_bearer(old)).status_code == 401
    assert anon.get("/api/v1/projects", headers=_bearer(new)).status_code != 401


def test_rotation_touches_no_other_file(tmp_path):
    first = auth.ensure_token(data_dir=tmp_path)
    (tmp_path / "glossa.db").write_bytes(b"sentinel-db-bytes")
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    second = auth.rotate_token(data_dir=tmp_path)
    assert second != first
    after = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    assert set(after) == set(before)
    assert after["glossa.db"] == before["glossa.db"]
    assert (tmp_path / "api_token").read_text(encoding="utf-8").strip() == second


def test_cli_never_prints_the_value(file_backed_app, capsys):
    _app2, data_dir = file_backed_app
    assert auth.main(["ensure"]) == 0
    out = capsys.readouterr().out
    token = (data_dir / "api_token").read_text(encoding="utf-8").strip()
    assert token not in out
    assert auth.token_fingerprint(token) in out

    assert auth.main(["rotate"]) == 0
    out = capsys.readouterr().out
    new_token = (data_dir / "api_token").read_text(encoding="utf-8").strip()
    assert new_token != token
    assert new_token not in out and token not in out
    assert auth.token_fingerprint(new_token) in out

    assert auth.main(["path"]) == 0
    assert str(data_dir / "api_token") in capsys.readouterr().out

    assert auth.main(["fingerprint"]) == 0
    assert capsys.readouterr().out.strip() == auth.token_fingerprint(new_token)


def test_cli_rotate_refuses_an_env_carried_token(capsys):
    # The session env carries GLOSSA_API_TOKEN (conftest seam): the
    # file is not authoritative, so rotation refuses, named (FR-004).
    assert auth.main(["rotate"]) == 2
    assert "GLOSSA_API_TOKEN" in capsys.readouterr().err


# ── C082-6: the named off switch, and nothing else ────────────────


def test_auth_off_switch_warns_and_reports(monkeypatch, caplog):
    monkeypatch.setenv("GLOSSA_API_AUTH", "off")
    with caplog.at_level(logging.WARNING, logger="glossa_lab.main"):
        app2 = create_app()
    assert "GLOSSA_API_AUTH=off" in caplog.text
    anon = _anon_client(app2)
    health = anon.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["auth"] == "disabled"
    assert anon.get("/api/v1/projects").status_code != 401
