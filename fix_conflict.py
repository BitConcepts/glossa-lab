"""Resolve the single conflict in DashboardView.tsx: keep both Phase A and Phase B additions."""
import re

path = "frontend/src/components/DashboardView.tsx"
with open(path, encoding="utf-8") as f:
    content = f.read()

# Check for conflict markers
if "<<<<<<< HEAD" not in content:
    print("No conflict markers found — already clean.")
    raise SystemExit(0)

# Remove conflict markers, keeping BOTH sides (they are additive)
# Pattern: replace <<<< HEAD ... ======= ... >>>>  with HEAD_content + separator + THEIRS_content
def resolve_conflict(m):
    head_part = m.group(1)
    theirs_part = m.group(2)
    # Both are additive module-level declarations — keep both
    return head_part.rstrip() + "\n}\n\n" + theirs_part.lstrip()

result = re.sub(
    r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> overhaul/automation\n",
    resolve_conflict,
    content,
    flags=re.DOTALL,
)

if "<<<<<<< HEAD" in result or "=======" in result:
    print("ERROR: conflict markers still present after resolution")
    raise SystemExit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(result)

print("Conflict resolved — both Phase A and Phase B blocks retained.")
