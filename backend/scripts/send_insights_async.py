"""Send Phase-37 insights email using Glossa Lab Notifier (async)."""
import asyncio, sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))

email_path = ROOT / "reports" / "phase37_insights_email.txt"
content = email_path.read_text("utf-8")
lines = content.splitlines()
subject = lines[0].replace("Subject: ", "")
body = "\n".join(lines[3:])

async def main():
    from glossa_lab.notifications.smtp import Notifier
    n = Notifier()
    print(f"Transport: {n.transport}")
    result = await n.send(
        subject=subject,
        body_text=body,
        recipients=["tpierson@bitconcepts.tech"],
        kind="research_insights",
    )
    for r in result.results:
        print(f"  {r.recipient}: {r.status} {r.error or ''}")
    print(f"Sent: {result.sent_count}, Failed: {result.failed_count}")

asyncio.run(main())
