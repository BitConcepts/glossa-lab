"""Quick inspection of the parsed Laursen Table 1 JSON output."""
import json
from pathlib import Path

p = (Path(__file__).resolve().parents[2]
     / "corpora" / "downloads" / "contact_zone"
     / "gulf_seals" / "laursen_2010_table1.json")
d = json.loads(p.read_text(encoding="utf-8"))
rows = d["rows"]
print(f"rows={len(rows)}")
print()
print("First 15 rows:")
for r in rows[:15]:
    print(f"  seal {r['seal_no']:3d}: type='{r['gulf_type']:<14}' "
          f"site='{r['site']:<25}' ref={r['reference'][:55]}")
print()
print("Rows with empty site (first 10):")
empty_site = [r for r in rows if not r["site"]]
print(f"  total: {len(empty_site)}")
for r in empty_site[:10]:
    print(f"  seal {r['seal_no']:3d}: type='{r['gulf_type']:<14}' ref={r['reference'][:60]}")
print()
print("Rows with non-empty site (first 10):")
with_site = [r for r in rows if r["site"]]
print(f"  total: {len(with_site)}")
for r in with_site[:10]:
    print(f"  seal {r['seal_no']:3d}: site='{r['site']}'")
