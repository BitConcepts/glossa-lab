"""Resolve main.py conflict: keep all routers from both sides."""
import re

path = "backend/glossa_lab/main.py"
with open(path, encoding="utf-8") as f:
    content = f.read()

if "<<<<<<< HEAD" not in content:
    print("No conflict markers — already clean.")
    raise SystemExit(0)

# Replace conflict block, keeping all three router registrations
merged_routers = (
    "    application.include_router(events_router)  # already prefixed at /api/v1/events\n"
    "    application.include_router(foundation_automation_router)  # already prefixed at /api/v1/foundation\n"
    "    application.include_router(signs_router)  # already prefixed at /api/v1/signs\n"
)

result = re.sub(
    r"<<<<<<< HEAD\n.*?>>>>>>> overhaul/signs\n",
    merged_routers,
    content,
    flags=re.DOTALL,
)

if "<<<<<<< HEAD" in result:
    print("ERROR: conflict markers still present")
    raise SystemExit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(result)
print("main.py conflict resolved — all 3 routers registered.")
