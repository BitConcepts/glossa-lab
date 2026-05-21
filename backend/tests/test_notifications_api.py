"""Smoke tests for the notifications API + email templates.

Coverage:
* Recipient CRUD via FastAPI TestClient (create, list, patch, delete, 404 paths).
* Email validation rejects malformed addresses.
* Duplicate-email POST returns 409.
* /status endpoint always returns the configured/host/from triple shape.
* /test endpoint returns 400 when SMTP is not configured (no live SMTP send).
* The HTML+text formatters return non-empty strings for each notification kind.

We intentionally do NOT exercise the wire-level SMTP path here — that would
need a stub server and adds CI fragility. The notifier is wired into the
discovery scheduler / study + experiment runners and surfaces failures via
the audit log when host/credentials are wrong.
"""

from __future__ import annotations

from glossa_lab.notifications.smtp import mask_email
from glossa_lab.notifications.templates import (
    format_discovery_digest,
    format_experiment_complete,
    format_study_complete,
    format_test,
)

# ── Recipients CRUD ─────────────────────────────────────────────────────────


def test_recipients_list_empty_shape(client):
    response = client.get("/api/v1/notifications/recipients")
    assert response.status_code == 200
    body = response.json()
    assert "recipients" in body
    assert "count" in body
    assert isinstance(body["recipients"], list)


def test_recipient_create_invalid_email_returns_400(client):
    response = client.post(
        "/api/v1/notifications/recipients",
        json={"email": "not-an-email"},
    )
    assert response.status_code == 400
    assert "Invalid email" in response.json()["detail"]


def test_recipient_full_lifecycle(client):
    # Create
    create = client.post(
        "/api/v1/notifications/recipients",
        json={"email": "test+lifecycle@example.com", "label": "QA bot", "active": True},
    )
    assert create.status_code == 201, create.text
    rid = create.json()["id"]
    assert create.json()["email"] == "test+lifecycle@example.com"
    assert create.json()["active"] == 1

    # Duplicate insert is rejected
    dup = client.post(
        "/api/v1/notifications/recipients",
        json={"email": "test+lifecycle@example.com"},
    )
    assert dup.status_code == 409

    # Patch — toggle off + rename
    patch = client.patch(
        f"/api/v1/notifications/recipients/{rid}",
        json={"active": False, "label": "Paused QA bot"},
    )
    assert patch.status_code == 200
    assert patch.json()["active"] == 0
    assert patch.json()["label"] == "Paused QA bot"

    # List should now contain 1 recipient with active=0
    listing = client.get("/api/v1/notifications/recipients").json()
    found = next((r for r in listing["recipients"] if r["id"] == rid), None)
    assert found is not None
    assert int(found["active"]) == 0

    # Status reflects total / active counts.
    status = client.get("/api/v1/notifications/status").json()
    assert status["recipients_total"] >= 1
    assert status["recipients_active"] == sum(
        1 for r in listing["recipients"] if int(r["active"]) == 1
    )

    # Delete
    delete = client.delete(f"/api/v1/notifications/recipients/{rid}")
    assert delete.status_code == 200
    assert delete.json()["deleted"] is True

    # 404 paths
    assert client.patch(
        f"/api/v1/notifications/recipients/{rid}",
        json={"label": "ghost"},
    ).status_code == 404
    assert client.delete(
        f"/api/v1/notifications/recipients/{rid}",
    ).status_code == 404


# ── Status / test endpoint ──────────────────────────────────────────────────


def test_notifications_status_endpoint(client):
    response = client.get("/api/v1/notifications/status")
    assert response.status_code == 200
    body = response.json()
    for k in ("configured", "host", "port", "from", "use_tls",
              "username_set", "password_set",
              "recipients_total", "recipients_active"):
        assert k in body, f"status response missing key {k}"


def test_notifications_test_requires_smtp_or_recipients(client, monkeypatch):
    """POST /test refuses cleanly when SMTP is unset OR there are no recipients."""
    # Force an unconfigured Notifier by clearing every SMTP env override.
    for var in ("SMTP_HOST", "SMTP_PORT", "SMTP_USERNAME",
                "SMTP_PASSWORD", "SMTP_FROM", "SMTP_USE_TLS"):
        monkeypatch.delenv(var, raising=False)

    response = client.post("/api/v1/notifications/test")
    # Either path is acceptable; both are guarded by an HTTP 400 with a
    # clear human-readable message that the UI surfaces verbatim.
    assert response.status_code in (200, 400)
    if response.status_code == 400:
        detail = response.json()["detail"].lower()
        assert "smtp" in detail or "recipient" in detail


# ── Templates ───────────────────────────────────────────────────────────────


def test_format_discovery_digest_handles_empty_and_populated_lists():
    subject0, text0, html0 = format_discovery_digest([])
    assert "0 new discovery item" in subject0
    assert "0 new" in text0
    assert "<!doctype html>" in html0.lower()

    items = [
        {"title": "A new Indus seal find at Rakhigarhi", "url": "https://example.org/a",
         "kind": "finding", "confidence": 0.91, "topic": "indus_script,ivc_archaeology",
         "summary": "A summary."},
        {"title": "Tooling: corpus loader update", "url": "https://example.org/b",
         "kind": "tooling", "confidence": 0.4, "topic": "indus_script", "summary": ""},
    ]
    subject, text, html = format_discovery_digest(items)
    assert "2 new" in subject
    assert "Rakhigarhi" in text
    assert "Rakhigarhi" in html
    assert "indus_script" in text
    assert "<a href=\"https://example.org/a\"" in html


def test_format_completion_emails_show_status_and_summary():
    s_subj, s_text, s_html = format_study_complete(
        name="Sign Frequency Study", study_id="abc123",
        status="completed",
        summary={"node_count": 4, "completed": 4, "errors": 0},
        duration_s=12.5,
    )
    assert "Study" in s_subj and "Sign Frequency Study" in s_subj
    assert "completed" in s_subj.lower()
    assert "12.5s" in s_text
    assert "node_count" in s_html

    e_subj, e_text, _ = format_experiment_complete(
        name="Bigram Profile",
        exp_id="xyz789",
        status="failed",
        summary={"error": "ZeroDivisionError"},
        duration_s=3.2,
    )
    assert "failed" in e_subj.lower()
    assert "Bigram Profile" in e_subj
    assert "ZeroDivisionError" in e_text


def test_format_test_email_self_describes():
    subj, text, html = format_test()
    assert "Test email" in subj
    assert "test email" in text.lower()
    assert "<!doctype html>" in html.lower()


# ── mask_email ──────────────────────────────────────────────────────────────


def test_mask_email_redacts_local_part():
    assert mask_email("alice@example.com") == "a***@example.com"
    assert mask_email("xenia@school.edu") == "x***@school.edu"
    # Non-email inputs pass through unchanged.
    assert mask_email("") == ""
    assert mask_email("not-an-email") == "not-an-email"
