"""Spec 083 (T007) — cloud configuration switch tests.

Under ``GLOSSA_CLOUD=1``:

* the env-mutation router (``api/env.py``: POST /setup, /rebuild,
  /upgrade — the whole router, including its read-only status routes)
  and the shutdown router (``api/shutdown.py``) are NOT registered:
  they are absent from the app's route surface and answer as absent;
* Ollama is neither bundled nor probed: the provider registry reports
  it offline without any network probe, auto-detection finds nothing,
  and the lifespan Ollama starter is a no-op.

With the switch unset, desktop registration is unchanged: the same
routes are present. (The mutation endpoints themselves are never
invoked by these tests in either mode — a POST to /env/rebuild or
/shutdown against a live app would be destructive; route-surface
presence plus the cloud-mode absence answers are the proof.)

Registration is asserted through ``app.openapi()``: on this
Starlette version ``include_router`` nests routers under a single
``path=""`` route in ``app.routes``, so raw route enumeration does
not flatten to real paths, while the OpenAPI surface does. For the
cloud-mode POSTs, "absent" answers 404 on an API-only tree (the CI
backend job, where no SPA dist exists) and 405 where the SPA
``StaticFiles`` mount is present (it serves GET/HEAD only, so an
unmatched POST falls through to it) — in both cases the handler is
not registered and never runs; a merely *gated* route would still
appear in the OpenAPI surface and answer from its own chain.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from glossa_lab.config import cloud_mode_enabled, get_settings

# Paths owned by the two host-management routers, as registered with
# the /api/v1 prefix in create_app().
ENV_PATHS = {
    "/api/v1/env/status",
    "/api/v1/env/setup",
    "/api/v1/env/rebuild",
    "/api/v1/env/upgrade",
    "/api/v1/env/packages",
}
SHUTDOWN_PATH = "/api/v1/shutdown"
HOST_MANAGEMENT_PATHS = ENV_PATHS | {SHUTDOWN_PATH}
ABSENT_POST_STATUSES = (404, 405)  # see module docstring


@pytest.fixture()
def cloud_app(monkeypatch):
    """A fresh app built with GLOSSA_CLOUD=1."""
    monkeypatch.setenv("GLOSSA_CLOUD", "1")
    get_settings.cache_clear()
    from glossa_lab.main import create_app

    app = create_app()
    yield app
    monkeypatch.delenv("GLOSSA_CLOUD", raising=False)
    get_settings.cache_clear()


@pytest.fixture()
def desktop_app(monkeypatch):
    """A fresh app built with the switch unset."""
    monkeypatch.delenv("GLOSSA_CLOUD", raising=False)
    get_settings.cache_clear()
    from glossa_lab.main import create_app

    app = create_app()
    yield app
    get_settings.cache_clear()


def _route_paths(app) -> set[str]:
    return set(app.openapi()["paths"].keys())


def _route_path_methods(app) -> set[tuple[str, str]]:
    return {
        (method.upper(), path)
        for path, operations in app.openapi()["paths"].items()
        for method in operations
    }


# ── Switch plumbing ──────────────────────────────────────────────────


def test_cloud_mode_flag_defaults_off(monkeypatch):
    monkeypatch.delenv("GLOSSA_CLOUD", raising=False)
    get_settings.cache_clear()
    try:
        assert cloud_mode_enabled() is False
    finally:
        get_settings.cache_clear()


def test_cloud_mode_flag_on(cloud_app):
    assert cloud_mode_enabled() is True


# ── Cloud mode: host-management routes absent ────────────────────────


def test_cloud_route_table_lacks_env_and_shutdown(cloud_app):
    paths = _route_paths(cloud_app)
    assert not (paths & HOST_MANAGEMENT_PATHS), paths & HOST_MANAGEMENT_PATHS


def test_cloud_env_mutation_and_shutdown_routes_absent(cloud_app):
    client = TestClient(cloud_app, raise_server_exceptions=False)
    for path in (
        "/api/v1/env/setup",
        "/api/v1/env/rebuild",
        "/api/v1/env/upgrade",
        "/api/v1/shutdown",
    ):
        response = client.post(path)
        assert response.status_code in ABSENT_POST_STATUSES, (
            path,
            response.status_code,
        )
    # The router is absent as a whole, not gated per-endpoint.
    assert client.get("/api/v1/env/status").status_code == 404
    assert client.get("/api/v1/env/packages").status_code == 404


def test_cloud_health_route_still_registered(cloud_app):
    assert "/api/v1/health" in _route_paths(cloud_app)


# ── Desktop mode: registration unchanged ─────────────────────────────


def test_desktop_route_table_has_env_and_shutdown(desktop_app):
    pairs = _route_path_methods(desktop_app)
    for path in ENV_PATHS:
        assert path in _route_paths(desktop_app), path
    assert SHUTDOWN_PATH in _route_paths(desktop_app)
    for path in ("/api/v1/env/setup", "/api/v1/env/rebuild",
                 "/api/v1/env/upgrade", SHUTDOWN_PATH):
        assert ("POST", path) in pairs, path


def test_desktop_env_status_route_answers(desktop_app):
    client = TestClient(desktop_app, raise_server_exceptions=False)
    response = client.get("/api/v1/env/status")
    assert response.status_code == 200
    assert "venv_exists" in response.json()


# ── Cloud mode: Ollama is not probed ─────────────────────────────────


def test_cloud_ollama_probe_reports_offline_without_probing(
    cloud_app, monkeypatch
):
    from glossa_lab.api import provider_registry

    def _boom(base_url):  # pragma: no cover - must never run in cloud mode
        raise AssertionError("Ollama was probed in cloud mode")

    monkeypatch.setattr(provider_registry, "_probe_ollama", _boom)
    result = provider_registry.probe_provider(
        "ollama", "ollama", "http://localhost:11434", ""
    )
    assert result["valid"] is False
    assert result["models"] == []


@pytest.mark.asyncio
async def test_cloud_detect_ollama_finds_nothing_without_probing(
    cloud_app, monkeypatch
):
    from glossa_lab.api import provider_registry

    def _boom(base_url):  # pragma: no cover - must never run in cloud mode
        raise AssertionError("Ollama was probed in cloud mode")

    monkeypatch.setattr(provider_registry, "_probe_ollama", _boom)
    assert await provider_registry.detect_ollama() == {"detected": []}


def test_cloud_try_start_ollama_is_a_noop(cloud_app, monkeypatch):
    import glossa_lab.main as main_module

    def _boom(name):  # pragma: no cover - must never run in cloud mode
        raise AssertionError("shutil.which was consulted in cloud mode")

    monkeypatch.setattr(main_module.shutil, "which", _boom)
    main_module._try_start_ollama()
    assert main_module.get_ollama_state() == {"installed": False, "started": False}
