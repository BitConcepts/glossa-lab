"""Security and CORS tests (TEST-SEC-001, TEST-SEC-002, TEST-API-004)."""

from glossa_lab.config import Settings


def test_default_host_is_localhost():
    """TEST-SEC-001: Default binding is localhost only."""
    settings = Settings()
    assert settings.host == "127.0.0.1"


def test_health_no_secrets(client):
    """TEST-SEC-002: Health endpoint contains no secrets."""
    response = client.get("/api/v1/health")
    data = response.json()
    # Should only contain status, version, uptime_seconds
    assert set(data.keys()) == {"status", "version", "uptime_seconds"}


def test_cors_preflight_in_dev_mode(client):
    """TEST-API-004: CORS preflight allows localhost origins."""
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Should not be 405 Method Not Allowed
    assert response.status_code != 405
    # CORS header should be present
    acl = response.headers.get("access-control-allow-origin", "")
    assert "localhost" in acl or acl == "*"
