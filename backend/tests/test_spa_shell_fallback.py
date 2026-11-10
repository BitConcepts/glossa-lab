"""Spec 083 — SPA shell fallback at the origin (Stage 2 fix 2).

The cloud edge Worker forwards the anonymous navigation paths
(/login, /setup, /invite/*) to this origin, and the SPA renders those
pages client-side from the shell. The backend mounted the built
frontend with plain ``StaticFiles(html=True)``, which serves real
files and directory indexes only — so once PR #543 made the origin
reachable through the edge, GET /login still answered this backend's
JSON 404 and the cloud login page could never load.

``_SpaShellStaticFiles`` (glossa_lab.main) serves the shell
(index.html, 200) for a GET/HEAD request on a shell path — the
FR-004 public-page set (/login, /setup, /invite, /invite/*),
mirroring the edge's own classification in cloud/edge/src/routes.ts —
that does not resolve to a real file. The fallback is deliberately
NOT blanket: TEST-API-003 (tests/test_health.py) pins that
unprefixed API-shaped paths such as /health must not answer 200, and
the app hash-routes every other screen. These tests pin the contract
against a TEMP dist (the tests must not be assumed to run in a tree
whose frontend/dist matches production):

* /login, /setup, /invite/<code> -> 200, the shell bytes;
* / and /index.html -> 200, the shell bytes;
* a real asset -> 200, its own bytes (never the shell);
* GET /api/v1/<missing> -> JSON 404, NOT the shell (API answers and
  scoped 404s are never swallowed by the fallback);
* GET /health and other non-shell paths -> 404, NOT the shell
  (plain StaticFiles answers, byte-identical to before);
* POST /login -> not the shell (404/405 family, as plain StaticFiles
  answers an unmatched POST — see test_cloud_mode.py's contract).
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import glossa_lab.main as main_module

SHELL = b"<!doctype html><html><body>spa-shell-marker</body></html>"
ASSET = b"console.log('real-asset-marker');\n"


@pytest.fixture()
def spa_client(tmp_path, monkeypatch):
    """An app whose frontend mount serves a temp dist with a marker shell."""
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_bytes(SHELL)
    (dist / "assets" / "app.js").write_bytes(ASSET)
    monkeypatch.setattr(main_module, "_FRONTEND_DIST", dist)
    app = main_module.create_app()
    return TestClient(app, raise_server_exceptions=False)


def test_root_serves_shell(spa_client):
    response = spa_client.get("/")
    assert response.status_code == 200
    assert response.content == SHELL


def test_index_html_serves_shell(spa_client):
    response = spa_client.get("/index.html")
    assert response.status_code == 200
    assert response.content == SHELL


@pytest.mark.parametrize(
    "path", ["/login", "/setup", "/invite", "/invite/ABC123", "/login/", "/invite/ABC123/"]
)
def test_navigation_paths_serve_shell(spa_client, path):
    response = spa_client.get(path)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert response.content == SHELL


def test_head_navigation_path_serves_shell(spa_client):
    response = spa_client.head("/login")
    assert response.status_code == 200


def test_real_asset_served_verbatim(spa_client):
    response = spa_client.get("/assets/app.js")
    assert response.status_code == 200
    assert response.content == ASSET


@pytest.mark.parametrize("path", ["/health", "/some/deep/route", "/assets/missing.js"])
def test_non_shell_paths_keep_plain_static_answers(spa_client, path):
    # The narrowing pins: outside the FR-004 public-page set, an
    # unresolved path answers exactly as plain StaticFiles did —
    # 404 JSON, never the shell. (/health is TEST-API-003's case.)
    response = spa_client.get(path)
    assert response.status_code == 404
    assert response.content != SHELL
    assert response.json() == {"detail": "Not Found"}


def test_api_miss_is_json_404_not_shell(spa_client):
    response = spa_client.get("/api/v1/definitely-not-a-route")
    assert response.status_code == 404
    assert response.content != SHELL
    assert response.json() == {"detail": "Not Found"}


def test_post_login_is_not_the_shell(spa_client):
    response = spa_client.post("/login")
    assert response.status_code in (404, 405)
    assert response.content != SHELL
