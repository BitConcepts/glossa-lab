"""Quick inspector for the parsed Tamil-Brahmi corpus."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "backend" / "glossa_lab" / "data" / "mahadevan_2003_tamil_brahmi.json"
d = json.loads(p.read_text(encoding="utf-8"))
inscs = d["inscriptions"]
print(f"Total: {len(inscs)}")
n_tb = sum(1 for i in inscs if i["section"] == "tamil_brahmi")
n_vatt = sum(1 for i in inscs if i["section"] == "vatteluttu")
print(f"Sections: tamil_brahmi={n_tb}, vatteluttu={n_vatt}")
print()
for i in inscs:
    site = str(i.get("site"))
    no = i.get("inscription_no")
    n = i["n_aksharas"]
    date = (i.get("date") or "")[:30]
    print(f"  {i['inscription_id']:25s} site={site:20s} no={no} n_akshara={n:3d} date={date}")
