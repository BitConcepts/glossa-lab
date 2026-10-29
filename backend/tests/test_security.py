"""Security and CORS tests (TEST-SEC-001, TEST-SEC-002, TEST-API-004)."""

from glossa_lab.config import Settings


def test_default_host_is_localhost():
    """TEST-SEC-001: Default binding is localhost only."""
    settings = Settings()
    assert settings.host == "127.0.0.1"


def test_health_no_secrets(client):
    """TEST-SEC-002: Health endpoint contains no secrets.

    Leg C C-08: the response also carries served identity
    (component + build stamp) — still no secrets, and the key set is
    pinned exactly so identity cannot silently drift again.
    Spec 082: the pinned set gains the `auth` mode word
    (token|disabled) — a mode, never a credential — per the
    ui-contract.md field set.
    """
    response = client.get("/api/v1/health")
    data = response.json()
    assert set(data.keys()) == {
        "status", "version", "uptime_seconds", "component", "build", "auth"}
    assert data["component"] == "glossa-lab-backend"


def test_cors_preflight_in_dev_mode(client):
    """TEST-API-004: CORS preflight allows localhost origins."""
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:5174",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Should not be 405 Method Not Allowed
    assert response.status_code != 405
    # CORS header should be present
    acl = response.headers.get("access-control-allow-origin", "")
    assert "localhost" in acl or acl == "*"
