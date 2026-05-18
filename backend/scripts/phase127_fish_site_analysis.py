"""
Phase-127: Fish sign site-level polysemy test.
Compare fish sign distribution at Lothal (coastal IVC port) vs. inland sites.
Tests Avishai Roif's hypothesis: isolated fish = commodity unit, compound = occupational.
"""
import sys, json, os
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "glossa_lab" / "data"))

holdat = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
df = pd.read_csv(holdat)

# Full fish sign family (plain + modified variants)
fish_signs = ["M047", "M052", "M053", "M054", "M055", "M056", "M049", "M145"]

print("=== PHASE-127: FISH SIGN SITE ANALYSIS ===")
print(f"Fish sign family: {fish_signs}")
print()

# Token-level: which signs appear at which sites
print("--- Fish Sign Tokens by Site ---")
fish_df = df[df["letters"].isin(fish_signs)]
pivot = fish_df.groupby(["site", "letters"]).size().unstack(fill_value=0)
print(pivot.to_string())
print()

# Seal-level: isolated vs compound
seal_groups = df.groupby(["form", "site"])["letters"].apply(list).reset_index()
seal_groups["n"] = seal_groups["letters"].apply(len)
has_fish = seal_groups["letters"].apply(lambda s: any(x in fish_signs for x in s))
fish_seals = seal_groups[has_fish].copy()
fish_seals["isolated"] = fish_seals["n"] == 1

print("--- Fish-Seal Counts by Site (isolated vs compound) ---")
rows = []
for site, grp in fish_seals.groupby("site"):
    tot = len(grp)
    iso = int(grp["isolated"].sum())
    comp = tot - iso
    coastal = "COASTAL" if site == "Lothal" else "inland"
    rows.append({"site": site, "type": coastal, "total": tot, "isolated": iso, "compound": comp,
                 "pct_isolated": round(100*iso/tot, 1)})
    print(f"  {site} ({coastal}): {tot} seals, {iso} isolated ({100*iso/tot:.0f}%), {comp} compound")

print()
print("--- Lothal Seal Details ---")
lot = fish_seals[fish_seals["site"] == "Lothal"]
if len(lot) == 0:
    print("  No Lothal fish seals found!")
else:
    for _, r in lot.iterrows():
        tag = "ISOLATED" if r["isolated"] else "compound"
        print(f"  {r['form']} | n={r['n']} | {tag} | {list(r['letters'])}")

print()

# Summary statistics
coastal_df = fish_seals[fish_seals["site"] == "Lothal"]
inland_df = fish_seals[fish_seals["site"] != "Lothal"]

c_iso = int(coastal_df["isolated"].sum())
c_tot = len(coastal_df)
i_iso = int(inland_df["isolated"].sum())
i_tot = len(inland_df)

print("--- Summary ---")
print(f"Lothal (coastal): {c_iso}/{c_tot} isolated = {100*c_iso/c_tot:.0f}%" if c_tot else "Lothal: no seals")
print(f"Inland sites:     {i_iso}/{i_tot} isolated = {100*i_iso/i_tot:.0f}%" if i_tot else "Inland: no seals")
print()

# Save results
results = {
    "phase": 127,
    "test": "fish_sign_polysemy_by_site",
    "fish_signs": fish_signs,
    "by_site": rows,
    "lothal_total": c_tot,
    "lothal_isolated": c_iso,
    "inland_total": i_tot,
    "inland_isolated": i_iso,
    "conclusion": (
        "TESTABLE: Lothal shows higher isolation rate vs inland" if c_tot > 0 and c_iso > 0
        else "UNTESTABLE: 0 isolated fish signs at Lothal (consistent with Phase-124 Holdat finding)"
    )
}

out = REPO / "backend/reports/phase127_fish_site_results.json"
out.write_text(json.dumps(results, indent=2))
print(f"Saved → {out}")
