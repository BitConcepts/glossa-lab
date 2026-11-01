"""Spec 083 Step 2 (T018/T019/T023) — container workspace-scope claim tests.

The cross-product matrix from the plan (Step 2, container half),
exercised against a cloud-mode app (``GLOSSA_CLOUD=1``) with fabricated
edge headers and a test service credential:

* no service credential                       → 401
* service credential but no actor identity    → 401 (anonymous API)
* non-member → workspace resource             → scoped 404, body is
  exactly ``{"detail": "Not found"}`` — no data, indistinguishable
  from a nonexistent workspace
* Viewer → read succeeds, write refused       → scoped 404, never success
* Member → own-workspace work                 → succeeds, and mutating
  acts are stamped with the actor (T023)
* cross-workspace id probing                  → scoped 404; the other
  workspace's records never appear in lists
* global Owner/Admin                          → implicit Workspace Admin
* Guest granted a Member role in the map      → capped at Viewer
* terminal                                    → member/guest 403 with
  ``X-Glossa-Denial: terminal-admin-only``; admin passes
* desktop mode (no cloud env)                 → scope middleware inert

Workspace-scoped classes covered per-workspace below: claims,
digestion (the claim trail), evidence (library), notebooks,
hypotheses, citations (evidence class), projects/workspaces
themselves, discovery (topic→project linkage), and experiments
*when linked* (the seeded project links none in a fresh test DB, so
experiments exercise the global-class leg here).

MODEL-GAP classes — studies, jobs, anchor sets / data, research-loop,
reports — carry **no** project linkage in the current data model, so
true per-workspace isolation is impossible for them today. They are
covered by the global-class leg (authenticated actors only; writes
require a write-capable role somewhere): ``test_global_classes_*``
pins exactly that behaviour and nothing stronger. See the coverage
table in ``glossa_lab/cloud_scope.py``.
"""
from __future__ import annotations

import json
import os

import pytest
from fastapi.testclient import TestClient

from glossa_lab.config import get_settings

SERVICE_CREDENTIAL = "test-service-credential-083"
SCOPED_404_BODY = {"detail": "Not found"}

PRIMARY_PROJECT_ID = "indus_decipherment"


def _cred() -> dict[str, str]:
    return {"X-Glossa-Service-Credential": SERVICE_CREDENTIAL}


def _actor(
    user_id: str = "u-member",
    username: str = "alice",
    global_type: str = "member",
    roles: dict | None = None,
) -> dict[str, str]:
    headers = _cred()
    headers["X-Glossa-User-Id"] = user_id
    headers["X-Glossa-User-Name"] = username
    headers["X-Glossa-Global-Type"] = global_type
    headers["X-Glossa-Workspace-Roles"] = json.dumps(roles or {})
    return headers


MEMBER = _actor(roles={"indus-script": "member"})
VIEWER = _actor("u-viewer", "vera", "guest", {"indus-script": "viewer"})
OUTSIDER = _actor("u-outsider", "oscar", "member", {"other-ws": "member"})
ADMIN = _actor("u-admin", "glassbreak", "admin", {})
GUEST_CAPPED = _actor("u-guest", "gus", "guest", {"indus-script": "member"})


@pytest.fixture(scope="module")
def cloud(tmp_path_factory):
    """One cloud-mode app + client for the module, with seeded records."""
    data_dir = tmp_path_factory.mktemp("glossa083") / "data"
    saved = {
        key: os.environ.get(key)
        for key in ("GLOSSA_CLOUD", "GLOSSA_SERVICE_CREDENTIAL", "GLOSSA_DATA_DIR")
    }
    # The app lifespan owns the process-global DB handle
    # (glossa_lab.database._db): entering the cloud client below
    # rebinds it to this module's data dir, and leaving the client
    # closes it to None. Capture the session binding now so teardown
    # can restore exactly what this fixture disturbs — otherwise
    # later modules reading through the session client see an
    # unbound database (GET /corpus-catalogue returns [] on None).
    from glossa_lab import database as _database

    saved_db = _database.get_db()
    os.environ["GLOSSA_CLOUD"] = "1"
    os.environ["GLOSSA_SERVICE_CREDENTIAL"] = SERVICE_CREDENTIAL
    os.environ["GLOSSA_DATA_DIR"] = str(data_dir)
    get_settings.cache_clear()
    from glossa_lab.main import create_app

    app = create_app()
    with TestClient(app) as client:
        seeded: dict = {"client": client}
        # A claim id from the primary workspace's register (read-only).
        claims = client.get(
            "/api/v1/indus-evidence/claims", headers=MEMBER
        ).json()["claims"]
        seeded["claim_id"] = claims[0]["claim_id"]
        # Workspace-owned records created by the member (T023 stamps).
        nb = client.post(
            "/api/v1/notebooks",
            headers=MEMBER,
            json={"title": "Scoped NB", "content": "x",
                  "project_id": PRIMARY_PROJECT_ID},
        )
        assert nb.status_code == 201, nb.text
        seeded["notebook"] = nb.json()
        hyp = client.post(
            "/api/v1/hypotheses",
            headers=MEMBER,
            json={"title": "Scoped HYP 083", "project_id": PRIMARY_PROJECT_ID},
        )
        assert hyp.status_code == 201, hyp.text
        seeded["hypothesis"] = hyp.json()
        cit = client.post(
            "/api/v1/citations",
            headers=MEMBER,
            json={"key": "scoped083", "title": "Scoped citation",
                  "project_id": PRIMARY_PROJECT_ID},
        )
        assert cit.status_code == 201, cit.text
        seeded["citation"] = cit.json()
        yield seeded
    for key, value in saved.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    get_settings.cache_clear()
    # Restore the DB binding captured at setup: exiting the cloud
    # client ran close_db(), leaving the global handle None. The
    # saved session Database was never closed (the cloud lifespan
    # only replaced the reference), so restoring the reference
    # reinstates the exact session state. Standalone, saved_db is
    # None — also the pre-fixture state.
    _database._db = saved_db


# ── Credential + login wall (container side) ─────────────────────────


def test_no_service_credential_is_401(cloud):
    client = cloud["client"]
    # No headers at all.
    assert client.get("/api/v1/projects").status_code == 401
    # Actor headers but no service credential.
    actor_only = {k: v for k, v in MEMBER.items()
                  if k != "X-Glossa-Service-Credential"}
    assert client.get("/api/v1/projects", headers=actor_only).status_code == 401
    # Wrong service credential.
    wrong = dict(MEMBER)
    wrong["X-Glossa-Service-Credential"] = "not-the-credential"
    assert client.get("/api/v1/projects", headers=wrong).status_code == 401


def test_service_credential_without_actor_is_401(cloud):
    client = cloud["client"]
    response = client.get("/api/v1/projects", headers=_cred())
    assert response.status_code == 401
    assert "Indus" not in response.text  # no data leaks anonymously


# ── Non-member → scoped 404 with no data, per resource class ────────


@pytest.mark.parametrize(
    "path_template",
    [
        "/api/v1/programs/{pid}/claims",                    # claims
        "/api/v1/programs/{pid}/claims/{cid}/trail",        # digestion
        "/api/v1/programs/{pid}/library",                   # evidence
        "/api/v1/indus-evidence/claims",                    # claims (shim)
        "/api/v1/indus-evidence/claims/{cid}/trail",        # digestion (shim)
        "/api/v1/indus-evidence/library",                   # evidence (shim)
        "/api/v1/projects/{pid}",                           # workspace itself
        "/api/v1/projects/{pid}/export",                    # workspace export
        "/api/v1/discovery/items?topic=indus_script",       # discovery
    ],
)
def test_nonmember_gets_scoped_404_with_no_data(cloud, path_template):
    client = cloud["client"]
    path = path_template.format(pid=PRIMARY_PROJECT_ID, cid=cloud["claim_id"])
    response = client.get(path, headers=OUTSIDER)
    assert response.status_code == 404, (path, response.status_code)
    assert response.json() == SCOPED_404_BODY, path


def test_nonmember_lists_leak_nothing(cloud):
    client = cloud["client"]
    projects = client.get("/api/v1/projects", headers=OUTSIDER).json()
    assert all(p["id"] != PRIMARY_PROJECT_ID for p in projects)
    notebooks = client.get("/api/v1/notebooks", headers=OUTSIDER).json()
    assert all(n["id"] != cloud["notebook"]["id"] for n in notebooks)
    hyps = client.get("/api/v1/hypotheses", headers=OUTSIDER).json()
    assert all(h["id"] != cloud["hypothesis"]["id"] for h in hyps)
    citations = client.get("/api/v1/citations", headers=OUTSIDER).json()
    assert all(c["id"] != cloud["citation"]["id"] for c in citations)


def test_cross_workspace_id_probing_is_404(cloud):
    client = cloud["client"]
    nb_id = cloud["notebook"]["id"]
    hyp_id = cloud["hypothesis"]["id"]
    # Guessing another workspace's record ids never succeeds.
    assert client.put(
        f"/api/v1/notebooks/{nb_id}", headers=OUTSIDER, json={"title": "hax"}
    ).status_code == 404
    assert client.delete(
        f"/api/v1/notebooks/{nb_id}", headers=OUTSIDER
    ).status_code == 404
    assert client.put(
        f"/api/v1/hypotheses/{hyp_id}", headers=OUTSIDER, json={"status": "hax"}
    ).status_code == 404
    assert client.delete(
        f"/api/v1/hypotheses/{hyp_id}", headers=OUTSIDER
    ).status_code == 404
    # The records are untouched.
    notebooks = client.get("/api/v1/notebooks", headers=MEMBER).json()
    assert any(n["id"] == nb_id and n["title"] == "Scoped NB" for n in notebooks)


# ── Viewer: read yes, write never ────────────────────────────────────


def test_viewer_reads(cloud):
    client = cloud["client"]
    assert client.get(
        "/api/v1/indus-evidence/claims", headers=VIEWER
    ).status_code == 200
    assert client.get(
        f"/api/v1/projects/{PRIMARY_PROJECT_ID}", headers=VIEWER
    ).status_code == 200
    notebooks = client.get("/api/v1/notebooks", headers=VIEWER).json()
    assert any(n["id"] == cloud["notebook"]["id"] for n in notebooks)


@pytest.mark.parametrize(
    "method,path,body",
    [
        ("PUT", "/api/v1/notebooks/{nb}", {"title": "viewer write"}),
        ("POST", "/api/v1/notebooks",
         {"title": "viewer nb", "project_id": PRIMARY_PROJECT_ID}),
        ("POST", "/api/v1/hypotheses",
         {"title": "viewer hyp", "project_id": PRIMARY_PROJECT_ID}),
        ("PUT", "/api/v1/projects/{pid}", {"label": "Indus Script Decipherment"}),
        ("POST", "/api/v1/indus-evidence/priority-register",
         {"claim_id": "x", "claimant": "vera"}),
    ],
)
def test_viewer_writes_are_refused(cloud, method, path, body):
    client = cloud["client"]
    path = path.format(nb=cloud["notebook"]["id"], pid=PRIMARY_PROJECT_ID)
    response = client.request(method, path, headers=VIEWER, json=body)
    assert response.status_code == 404, (method, path, response.status_code)
    assert response.json() == SCOPED_404_BODY


def test_guest_is_capped_at_viewer(cloud):
    client = cloud["client"]
    # The roles map claims Member; a Guest is capped at Viewer.
    assert client.get(
        "/api/v1/indus-evidence/claims", headers=GUEST_CAPPED
    ).status_code == 200
    assert client.post(
        "/api/v1/notebooks",
        headers=GUEST_CAPPED,
        json={"title": "guest write", "project_id": PRIMARY_PROJECT_ID},
    ).status_code == 404


# ── Member: own-workspace work succeeds, stamped (T023) ─────────────


def test_member_own_workspace_work_and_attribution(cloud):
    client = cloud["client"]
    notebook = cloud["notebook"]
    # The create was stamped with the acting user at record level.
    assert notebook["created_by"]["user_id"] == "u-member"
    assert notebook["created_by"]["username"] == "alice"
    assert notebook["created_by"]["at"]
    assert notebook["attribution_label"] == "alice"
    # Update stamps modified_by.
    updated = client.put(
        f"/api/v1/notebooks/{notebook['id']}",
        headers=MEMBER,
        json={"title": "Scoped NB (edited)"},
    )
    assert updated.status_code == 200
    assert updated.json()["modified_by"]["username"] == "alice"
    # Claims work: the register reads, and the trail (digestion) reads.
    assert client.get(
        "/api/v1/indus-evidence/claims", headers=MEMBER
    ).status_code == 200
    trail = client.get(
        f"/api/v1/indus-evidence/claims/{cloud['claim_id']}/trail",
        headers=MEMBER,
    )
    assert trail.status_code == 200
    # Workspace write: the project upsert stamps modified_by.
    project = client.put(
        f"/api/v1/projects/{PRIMARY_PROJECT_ID}",
        headers=MEMBER,
        json={"label": "Indus Script Decipherment"},
    )
    assert project.status_code == 200
    assert project.json()["modified_by"]["username"] == "alice"


def test_desktop_import_label_for_unstamped_records(cloud):
    client = cloud["client"]
    claims = client.get(
        "/api/v1/indus-evidence/claims", headers=MEMBER
    ).json()["claims"]
    assert claims, "primary register must not be empty"
    # The register arrived via bundle/desktop — no cloud actor exists,
    # so every entry renders the import label, never a fake author.
    assert all(
        entry["attribution_label"] == "via desktop import" for entry in claims
    )
    trail = client.get(
        f"/api/v1/indus-evidence/claims/{cloud['claim_id']}/trail",
        headers=MEMBER,
    ).json()
    assert trail["attribution_label"] == "via desktop import"


# ── Global admin: implicit Workspace Admin ───────────────────────────


def test_global_admin_has_implicit_workspace_admin(cloud):
    client = cloud["client"]
    assert client.get(
        "/api/v1/indus-evidence/claims", headers=ADMIN
    ).status_code == 200
    updated = client.put(
        f"/api/v1/notebooks/{cloud['notebook']['id']}",
        headers=ADMIN,
        json={"content": "admin edit"},
    )
    assert updated.status_code == 200
    projects = client.get("/api/v1/projects", headers=ADMIN).json()
    assert any(p["id"] == PRIMARY_PROJECT_ID for p in projects)


# ── Workspace materialization ────────────────────────────────────────


def test_workspace_materialization_is_idempotent_and_stamped(cloud):
    client = cloud["client"]
    # other-ws is authorized for OUTSIDER (edge/D1 side) but has no
    # local project yet: the first scoped request materializes it.
    response = client.get("/api/v1/programs/other-ws/claims", headers=OUTSIDER)
    assert response.status_code == 200
    assert response.json()["claims"] == []
    project = client.get("/api/v1/projects/other-ws", headers=OUTSIDER)
    assert project.status_code == 200
    record = project.json()
    assert record["slug"] == "other-ws"
    assert record["created_by"]["username"] == "oscar"
    assert record["created_by"]["via"] == "cloud"
    # Idempotent: a second request serves the same single record.
    again = client.get("/api/v1/programs/other-ws/claims", headers=OUTSIDER)
    assert again.status_code == 200
    projects = client.get("/api/v1/projects", headers=ADMIN).json()
    assert sum(1 for p in projects if p["slug"] == "other-ws") == 1
    # And the indus member still cannot see it.
    member_projects = client.get("/api/v1/projects", headers=MEMBER).json()
    assert all(p["slug"] != "other-ws" for p in member_projects)


# ── Project-slug linkage ─────────────────────────────────────────────


def test_primary_workspace_slug_is_indus_script(cloud):
    client = cloud["client"]
    projects = client.get("/api/v1/projects", headers=MEMBER).json()
    primary = [p for p in projects if p["id"] == PRIMARY_PROJECT_ID]
    assert primary and primary[0]["slug"] == "indus-script"


def test_project_slug_derivation():
    from glossa_lab.cloud_scope import project_slug

    assert project_slug({"id": "x", "label": "Y", "slug": "explicit"}) == "explicit"
    assert project_slug({"id": "indus_decipherment", "label": "Indus Script Decipherment"}) == "indus-script"
    assert project_slug({"id": "p2", "label": "Linear A Study"}) == "linear-a-study"
    assert project_slug({"id": "some_id", "label": ""}) == "some-id"


# ── Terminal gating (D-5) ────────────────────────────────────────────


def test_terminal_requires_global_admin(cloud):
    client = cloud["client"]
    for headers in (MEMBER, VIEWER, OUTSIDER):
        response = client.post(
            "/api/v1/terminal/run", headers=headers, json={"command": "ls"}
        )
        assert response.status_code == 403
        assert response.headers.get("x-glossa-denial") == "terminal-admin-only"
    # Admin passes the gate (the log read is the harmless surface).
    assert client.get(
        "/api/v1/terminal/log", headers=ADMIN, params={"lines": 1}
    ).status_code == 200


# ── Global classes (model gap): authenticated gating only ───────────


def test_global_classes_require_authentication_and_write_role(cloud):
    """Studies/jobs/anchors/research-loop/reports/experiments have no
    project linkage in the model — the strongest honest scoping is:
    authenticated actors may read; writes need a write-capable role
    somewhere. This test pins that, and no more."""
    client = cloud["client"]
    # Reads succeed for any authenticated actor (incl. the outsider —
    # there is no workspace that owns these records in the model).
    assert client.get("/api/v1/studies", headers=OUTSIDER).status_code == 200
    assert client.get("/api/v1/jobs", headers=OUTSIDER).status_code == 200
    assert client.get("/api/v1/anchor-sets", headers=OUTSIDER).status_code == 200
    assert client.get(
        "/api/v1/research-loop/status", headers=OUTSIDER
    ).status_code == 200
    assert client.get("/api/v1/reports", headers=OUTSIDER).status_code == 200
    assert client.get("/api/v1/experiments", headers=OUTSIDER).status_code == 200
    assert client.get(
        "/api/v1/discovery/stats", headers=OUTSIDER
    ).status_code == 200
    # Writes by a Viewer-only actor are refused across all of them.
    assert client.post(
        "/api/v1/jobs", headers=VIEWER, json={"name": "j", "pipeline": "p"}
    ).status_code == 404
    assert client.post(
        "/api/v1/studies", headers=VIEWER, json={"name": "viewer study"}
    ).status_code == 404
    assert client.post(
        "/api/v1/anchor-sets", headers=VIEWER, json={"name": "v", "pairs": []}
    ).status_code == 404
    assert client.post(
        "/api/v1/research-loop/stop", headers=VIEWER
    ).status_code == 404
    assert client.post(
        "/api/v1/experiments/whatever/run", headers=VIEWER, json={}
    ).status_code == 404
    # A member's global-class write succeeds.
    assert client.post(
        "/api/v1/studies", headers=MEMBER, json={"name": "member study"}
    ).status_code == 201


# ── Desktop mode: the middleware is inert ────────────────────────────


def test_desktop_mode_scope_middleware_inert():
    saved = {
        key: os.environ.get(key)
        for key in ("GLOSSA_CLOUD", "GLOSSA_SERVICE_CREDENTIAL")
    }
    os.environ.pop("GLOSSA_CLOUD", None)
    os.environ.pop("GLOSSA_SERVICE_CREDENTIAL", None)
    get_settings.cache_clear()
    try:
        from glossa_lab.cloud_scope import CloudScopeMiddleware
        from glossa_lab.main import create_app

        app = create_app()
        stack = [entry.cls for entry in app.user_middleware]
        assert CloudScopeMiddleware not in stack
        # The request is answered by the handler itself (the in-process
        # DB singleton from the cloud fixture serves it) — the point is
        # it is NOT refused by cloud scope (no 401, no scoped 404) even
        # with no edge headers at all.
        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/api/v1/projects")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        get_settings.cache_clear()
