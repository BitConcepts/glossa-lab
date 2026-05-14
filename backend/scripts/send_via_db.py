"""Send insights email by reading Resend API key directly from SQLite."""
import sqlite3, sys, urllib.request, json, os
from pathlib import Path

ROOT = Path(__file__).parents[2]

# Try to find the right database
DB_PATHS = [
    ROOT / "data" / "glossa.db",
    ROOT / "backend" / "data" / "glossa.db",
]
db_path = next((p for p in DB_PATHS if p.exists()), None)
if not db_path:
    print("No glossa.db found"); sys.exit(1)

print(f"Using DB: {db_path}")

# Read settings
conn = sqlite3.connect(str(db_path))
rows = {k: v for k, v in conn.execute("SELECT key, value FROM settings WHERE key LIKE '%resend%' OR key LIKE '%smtp%'").fetchall()}
conn.close()

print(f"Settings found: {list(rows.keys())}")

resend_key = rows.get("resend_api_key", "")
resend_from = rows.get("resend_from", "Glossa Lab <noreply@bitconcepts.tech>")

if not resend_key or "dummy" in resend_key.lower():
    print("No valid resend_api_key in database")
    sys.exit(1)

# Load email
email_path = ROOT / "reports" / "phase37_insights_email.txt"
content = email_path.read_text("utf-8")
lines = content.splitlines()
subject = lines[0].replace("Subject: ", "")
body = "\n".join(lines[3:])

# Send via Resend API
payload = json.dumps({
    "from": resend_from,
    "to": ["tpierson@bitconcepts.tech"],
    "subject": subject,
    "text": body,
}).encode()

req = urllib.request.Request(
    "https://api.resend.com/emails",
    data=payload,
    headers={
        "Authorization": f"Bearer {resend_key}",
        "Content-Type": "application/json",
        "User-Agent": "glossa-lab-notifier/1.0 (resend-python-compat)",
    },
    method="POST",
)

try:
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read())
    print(f"Email sent! ID: {result.get('id')}")
except urllib.error.HTTPError as e:
    body_err = e.read().decode()
    print(f"HTTP {e.code}: {body_err}")
except Exception as exc:
    print(f"Error: {exc}")
