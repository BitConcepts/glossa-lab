"""One-shot fix script: update INDUS_FINAL_ANCHORS.json metadata and graph_type fields."""
import json
import pathlib
from collections import Counter

REPO = pathlib.Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab")

# ── 1. Fix INDUS_FINAL_ANCHORS.json metadata ────────────────────────────────
anchors_path = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
fa = json.loads(anchors_path.read_text(encoding="utf-8"))

conf = Counter(v.get("confidence") for v in fa["anchors"].values())
n_high   = conf["HIGH"]
n_medium = conf["MEDIUM"]
n_low    = conf["LOW"]
total_hm = n_high + n_medium
total_all = len(fa["anchors"])

print(f"ANCHORS: total {fa['total']} -> {total_hm}  |  n_medium {fa['n_medium']} -> {n_medium}  |  n_low {fa['n_low']} -> {n_low}")

fa["total"]             = total_hm
fa["n_high"]            = n_high
fa["n_medium"]          = n_medium
fa["n_low"]             = n_low
fa["by_confidence"]     = {"HIGH": n_high, "MEDIUM": n_medium, "LOW": n_low}
fa["total_all_entries"] = total_all
if "_phase163_note" not in fa:
    fa["_phase163_note"] = (
        "Phase-163 sibilant discovery: 4 MEDIUM upgrades "
        "(M165=cul, M330=can, M202=can, M372=can). total updated 157->161."
    )

anchors_path.write_text(json.dumps(fa, indent=2, ensure_ascii=False), encoding="utf-8")
print("  -> Saved INDUS_FINAL_ANCHORS.json")

# ── 2. Set graph_type="experiment" on all 153 graph JSON files ───────────────
graphs_dir = REPO / "backend" / "glossa_lab" / "experiments" / "graphs"
updated = 0
for f in sorted(graphs_dir.glob("*.json")):
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        if data.get("graph_type") is None or data.get("graph_type") == "":
            data["graph_type"] = "experiment"
            f.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            updated += 1
    except Exception as exc:
        print(f"  SKIP {f.name}: {exc}")

print(f"GRAPH_TYPE: updated {updated} files -> graph_type='experiment'")
print("Done.")
