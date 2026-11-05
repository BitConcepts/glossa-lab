"""Spec 083 Amendment 5 (T056) — desktop hosted posture tests.

The hosted edition's origin is the desktop application itself
(Amendment 5). These tests pin the desktop posture of
``CloudScopeMiddleware`` on an app built WITHOUT ``GLOSSA_CLOUD``:

* local Spec 082 use (Bearer token, no edge headers) is untouched,
  even while a service credential is configured;
* an edge forward (valid service credential + identity headers, NO
  Bearer token) is accepted, scoped, and attributed exactly as in
  cloud mode — ``ApiTokenMiddleware`` stands down for it;
* identity headers without a valid credential confer nothing (401);
* host management (POST /api/v1/shutdown, /api/v1/env/*) answers the
  scoped 404 through the edge whatever the role, while staying
  reachable locally;
* the terminal gate keeps its 403 + ``X-Glossa-Denial`` marker;
* the credential also resolves from the desktop's protected keys
  store (T024) when the environment does not carry it;
* with NO credential configured anywhere, the middleware is not
  installed and forged edge headers confer nothing at all.
"""
from __future__ import annotations

import json
import os

import pytest
from fastapi.testclient import TestClient

from glossa_lab.config import get_settings

SERVICE_CREDENTIAL = "test-desktop-service-credential-083"
KEYS_STORE_CREDENTIAL = "test-keys-store-credential-083"
SCOPED_404_BODY = {"detail": "Not found"}
PRIMARY_PROJECT_ID = "indus_decipherment"
ENV_KEYS = ("GLOSSA_CLOUD", "GLOSSA_SERVICE_CREDENTIAL", "GLOSSA_DATA_DIR")


def _actor(
    credential: str = SERVICE_CREDENTIAL,
    user_id: str = "u-member",
    username: str = "alice",
    global_type: str = "member",
    roles: dict | None = None,
) -> dict[str, str]:
    """Edge-provenance headers; Authorization suppressed (no Bearer)."""
    return {
        "Authorization": "",
        "X-Glossa-Service-Credential": credential,
        "X-Glossa-User-Id": user_id,
        "X-Glossa-User-Name": username,
        "X-Glossa-Global-Type": global_type,
        "X-Glossa-Workspace-Roles": json.dumps(roles or {}),
    }


MEMBER = _actor(roles={"indus-script": "member"})
OUTSIDER = _actor(user_id="u-outsider", username="oscar",
                  global_type="member", roles={"other-ws": "member"})
ADMIN = _actor(user_id="u-admin", username="glassbreak",
               global_type="admin", roles={})


def _build(tmp_path_factory, label, *, env_credential=None, keys_credential=None):
    """A desktop-posture app + client, with one locally-seeded notebook."""
    data_dir = tmp_path_factory.mktemp(label) / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    saved = {key: os.environ.get(key) for key in ENV_KEYS}
    from glossa_lab import database as _database

    saved_db = _database.get_db()
    os.environ.pop("GLOSSA_CLOUD", None)
    if env_credential is None:
        os.environ.pop("GLOSSA_SERVICE_CREDENTIAL", None)
    else:
        os.environ["GLOSSA_SERVICE_CREDENTIAL"] = env_credential
    os.environ["GLOSSA_DATA_DIR"] = str(data_dir)
    if keys_credential is not None:
        (data_dir / ".keys.json").write_text(
            json.dumps({"glossa_service_credential": keys_credential}),
            encoding="utf-8",
        )
    get_settings.cache_clear()
    from glossa_lab.main import create_app

    return data_dir, saved, saved_db, _database, create_app


def _finish(saved, saved_db, _database):
    for key, value in saved.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    get_settings.cache_clear()
    _database._db = saved_db


@pytest.fixture(scope="module")
def desktop(tmp_path_factory):
    """Desktop posture: credential in the environment, no GLOSSA_CLOUD."""
    _dir, saved, saved_db, _database, create_app = _build(
        tmp_path_factory, "glossa083desk", env_credential=SERVICE_CREDENTIAL
    )
    app = create_app()
    with TestClient(app) as client:
        nb = client.post(
            "/api/v1/notebooks",
            json={"title": "Desktop NB", "content": "x",
                  "project_id": PRIMARY_PROJECT_ID},
        )
        assert nb.status_code == 201, nb.text
        yield {"client": client, "notebook": nb.json()}
    _finish(saved, saved_db, _database)


@pytest.fixture(scope="module")
def desktop_keys(tmp_path_factory):
    """Desktop posture: credential ONLY in the protected keys store."""
    _dir, saved, saved_db, _database, create_app = _build(
        tmp_path_factory, "glossa083keys", keys_credential=KEYS_STORE_CREDENTIAL
    )
    app = create_app()
    with TestClient(app) as client:
        yield {"client": client}
    _finish(saved, saved_db, _database)


@pytest.fixture(scope="module")
def unarmed(tmp_path_factory):
    """No credential anywhere: the middleware must not be installed."""
    _dir, saved, saved_db, _database, create_app = _build(
        tmp_path_factory, "glossa083unarmed"
    )
    app = create_app()
    with TestClient(app) as client:
        nb = client.post(
            "/api/v1/notebooks",
            json={"title": "Unarmed NB", "content": "x",
                  "project_id": PRIMARY_PROJECT_ID},
        )
        assert nb.status_code == 201, nb.text
        yield {"client": client, "notebook": nb.json()}
    _finish(saved, saved_db, _database)


# ── Local use is untouched by the posture ────────────────────────────


def test_local_requests_pass_untouched(desktop):
    client = desktop["client"]
    assert client.get("/api/v1/projects").status_code == 200
    nb_id = desktop["notebook"]["id"]
    notebooks = client.get("/api/v1/notebooks").json()
    assert any(n["id"] == nb_id for n in notebooks)


# ── Edge forwards: accepted, scoped, no Bearer token ────────────────


def test_edge_forward_without_bearer_is_accepted_and_scoped(desktop):
    client = desktop["client"]
    nb_id = desktop["notebook"]["id"]
    response = client.get("/api/v1/notebooks", headers=MEMBER)
    assert response.status_code == 200
    assert any(n["id"] == nb_id for n in response.json())
    assert client.get("/api/v1/projects", headers=MEMBER).status_code == 200


def test_edge_outsider_gets_scoped_404(desktop):
    client = desktop["client"]
    nb_id = desktop["notebook"]["id"]
    # The outsider's list is filtered (the record never appears)…
    notebooks = client.get("/api/v1/notebooks", headers=OUTSIDER).json()
    assert all(n["id"] != nb_id for n in notebooks)
    # …and id probing answers the uniform scoped 404.
    response = client.put(
        f"/api/v1/notebooks/{nb_id}", headers=OUTSIDER, json={"title": "hax"}
    )
    assert response.status_code == 404
    assert response.json() == SCOPED_404_BODY


def test_edge_wrong_credential_is_401(desktop):
    client = desktop["client"]
    forged = _actor(credential="not-the-credential",
                    roles={"indus-script": "member"})
    assert client.get("/api/v1/projects", headers=forged).status_code == 401


def test_edge_identity_without_credential_is_401(desktop):
    client = desktop["client"]
    actor_only = {k: v for k, v in MEMBER.items()
                  if k != "X-Glossa-Service-Credential"}
    assert client.get("/api/v1/projects", headers=actor_only).status_code == 401


# ── Host management: denied through the edge, alive locally ─────────


def test_edge_host_management_is_scoped_404_even_for_admin(desktop):
    client = desktop["client"]
    shutdown = client.post("/api/v1/shutdown", headers=ADMIN)
    assert shutdown.status_code == 404
    assert shutdown.json() == SCOPED_404_BODY
    env_status = client.get("/api/v1/env/status", headers=ADMIN)
    assert env_status.status_code == 404
    assert env_status.json() == SCOPED_404_BODY


def test_host_management_stays_reachable_locally(desktop):
    client = desktop["client"]
    assert client.get("/api/v1/env/status").status_code == 200


# ── Terminal gate in the desktop posture ─────────────────────────────


def test_edge_terminal_gate_keeps_its_denial_marker(desktop):
    client = desktop["client"]
    response = client.get("/api/v1/terminal/sessions", headers=MEMBER)
    assert response.status_code == 403
    assert response.headers.get("x-glossa-denial") == "terminal-admin-only"
    admin = client.get("/api/v1/terminal/sessions", headers=ADMIN)
    assert admin.headers.get("x-glossa-denial") is None


# ── Credential from the protected keys store (T024) ──────────────────


def test_credential_resolves_from_keys_store(desktop_keys):
    client = desktop_keys["client"]
    member = _actor(credential=KEYS_STORE_CREDENTIAL,
                    roles={"indus-script": "member"})
    assert client.get("/api/v1/projects", headers=member).status_code == 200
    forged = _actor(credential="not-the-credential",
                    roles={"indus-script": "member"})
    assert client.get("/api/v1/projects", headers=forged).status_code == 401


# ── Unarmed desktop: forged headers confer nothing ───────────────────


def test_unarmed_desktop_ignores_forged_edge_headers(unarmed):
    client = unarmed["client"]
    nb_id = unarmed["notebook"]["id"]
    # With the local Bearer the request is plain local use: an
    # "outsider" forged actor does not scope it (middleware absent).
    forged = {k: v for k, v in OUTSIDER.items() if k != "Authorization"}
    response = client.get("/api/v1/notebooks", headers=forged)
    assert response.status_code == 200
    assert any(n["id"] == nb_id for n in response.json())
    # Without the Bearer, forged headers alone buy nothing: the token
    # middleware refuses (no edge stand-down exists to invoke).
    assert client.get("/api/v1/projects",
                      headers=OUTSIDER).status_code == 401
