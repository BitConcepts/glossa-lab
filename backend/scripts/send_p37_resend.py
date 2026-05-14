"""Send Phase-37 insights email using ResendConfig directly (same as phase33_send_email.py)."""
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))

RECIPIENT = "tpierson@bitconcepts.tech"
email_path = ROOT / "reports" / "phase37_insights_email.txt"
content = email_path.read_text("utf-8")
lines = content.splitlines()
subject = lines[0].replace("Subject: ", "")
body = "\n".join(lines[3:])

try:
    from glossa_lab.notifications.resend import ResendConfig, send_mail
    cfg = ResendConfig.from_settings()
    if cfg.is_configured():
        result = send_mail(cfg, recipient=RECIPIENT, subject=subject, body_text=body)
        if result.success:
            print(f"Email sent to {RECIPIENT} (id: {result.message_id})")
        else:
            print(f"Resend failed: {result.error}")
    else:
        print("Resend not configured — check resend_api_key in settings")
except Exception as e:
    print(f"Error: {e}")
    import traceback; traceback.print_exc()
