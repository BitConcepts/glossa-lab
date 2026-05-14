import sqlite3, sys, urllib.request, json
from pathlib import Path

ROOT = Path(__file__).parents[2]

resend_key = None
resend_from = "Glossa Lab <noreply@bitconcepts.tech>"

# Search .keys.json files
for keys_path in [ROOT / "backend" / "data" / ".keys.json", ROOT / "data" / ".keys.json"]:
    if keys_path.exists():
        keys = json.loads(keys_path.read_text("utf-8"))
        if "resend_api_key" in keys:
            resend_key = keys["resend_api_key"]
            resend_from = keys.get("resend_from", resend_from)
            print(f"Found resend key in: {keys_path}")
            break

if not resend_key:
    print("resend_api_key not found"); sys.exit(1)

# Load email
email_path = ROOT / "reports" / "phase37_insights_email.txt"
content = email_path.read_text("utf-8")
lines = content.splitlines()
subject = lines[0].replace("Subject: ", "")
body = "\n".join(lines[3:])

print(f"Sending: {subject[:60]}...")
print(f"From: {resend_from}")

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
    print(f"HTTP {e.code}: {e.read().decode()}")
except Exception as exc:
    print(f"Error: {exc}")
