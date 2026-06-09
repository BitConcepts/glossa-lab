import json
from pathlib import Path

m = json.loads(Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\static\signs\manifest.json").read_text())

for sid in ["M004", "M062", "M066", "M100"]:
    info = m.get(sid, {})
    src = info.get("source", "MISSING")
    print(f"{sid}: {src}")

sources = {}
for sid, info in m.items():
    src = info.get("source", "").split(":")[0]
    sources[src] = sources.get(src, 0) + 1
print(f"\n{json.dumps(sources, indent=2)}")

fb = sorted(s for s, i in m.items() if i.get("source") == "fallback_icon")
print(f"\nFallback: {len(fb)}")
print(fb)

# Check Table III sequential mapping - what M-numbers got mapped
t3 = sorted(s for s, i in m.items() if "table_iii" in i.get("source", ""))
print(f"\nTable III: {len(t3)}")
# Which M001-M417 are NOT covered by appendix_i or table_iii?
covered = set(s for s, i in m.items() if "mahadevan" in i.get("source", ""))
missing_mah = sorted(f"M{n:03d}" for n in range(1, 418) if f"M{n:03d}" not in covered)
print(f"Missing from Mahadevan (M001-M417): {len(missing_mah)}: {missing_mah}")
