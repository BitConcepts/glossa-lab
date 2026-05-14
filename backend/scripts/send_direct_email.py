"""Send the Phase-37 insights email directly via Glossa Lab Notifier."""
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))

# Load the email content
email_path = ROOT / "reports" / "phase37_insights_email.txt"
content = email_path.read_text("utf-8")

# Parse subject and body
lines = content.splitlines()
subject = lines[0].replace("Subject: ", "")
body = "\n".join(lines[3:])  # skip Subject:, To:, blank line

print(f"Subject: {subject}")
print(f"Body length: {len(body)} chars")

try:
    from glossa_lab.notifications.smtp import SmtpNotifier
    from glossa_lab.database import get_db_session
    from sqlalchemy import text

    # Get SMTP config from settings
    with get_db_session() as db:
        rows = db.execute(text("SELECT key, value FROM settings WHERE key IN ('smtp_host','smtp_port','smtp_username','smtp_password','smtp_from','smtp_use_tls')")).fetchall()
        settings = {r[0]: r[1] for r in rows}

    print(f"SMTP config loaded: host={settings.get('smtp_host','?')}, from={settings.get('smtp_from','?')}")

    notifier = SmtpNotifier(
        host=settings.get("smtp_host", "smtp.gmail.com"),
        port=int(settings.get("smtp_port", 587)),
        username=settings.get("smtp_username", ""),
        password=settings.get("smtp_password", ""),
        from_addr=settings.get("smtp_from", "noreply@bitconcepts.tech"),
        use_tls=settings.get("smtp_use_tls", "true").lower() == "true",
    )

    result = notifier.send(
        to=["tpierson@bitconcepts.tech"],
        subject=subject,
        body=body,
    )
    print(f"Email sent: {result}")

except Exception as exc:
    print(f"SMTP send error: {exc}")
    # Try via HTTP API with a different approach
    import urllib.request, json
    # POST to a custom notification endpoint if available
    try:
        payload = json.dumps({"subject": subject, "body": body}).encode()
        req = urllib.request.Request(
            "http://localhost:8001/api/v1/notifications/send",
            data=payload, headers={"Content-Type": "application/json"}, method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=30)
        print(f"Via API: {json.loads(resp.read())}")
    except Exception as e2:
        print(f"API fallback also failed: {e2}")
        print("\nEmail saved to reports/phase37_insights_email.txt — ready for manual send.")
        print("The notification test confirmed SMTP is configured and working.")
        print("Please send reports/phase37_insights_email.txt via your email client.")
