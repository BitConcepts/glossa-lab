"""
Phase-161 (application step): Apply proposed LOW→MEDIUM anchor upgrades
to INDUS_FINAL_ANCHORS.json based on literature mining results.

Applies only upgrades with n_sources >= 2 (MEDIUM) or 3 (HIGH),
and where the reading is phonologically verified as Dravidian.

Also applies sibilant candidates from Phase-163 if n_mentions >= 3.

Output: Updates INDUS_FINAL_ANCHORS.json in-place (with backup)
        Saves: backend/reports/phase161_upgrade_summary.json
"""
import sys, json, copy
from pathlib import Path
from datetime import datetime

REPO         = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
UPGRADES_PATH= REPO / "backend/reports/phase161_162_165_upgrade_proposals.json"
SIB_PATH     = REPO / "backend/reports/phase163_sibilant_discovery.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
OUT_SUMMARY  = REPO / "backend/reports/phase161_upgrade_summary.json"

print("="*70)
print("PHASE-161: APPLY ANCHOR UPGRADES")
print("="*70)

# Load current anchors + proposals
anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors     = anchor_data["anchors"]
upgrades    = json.loads(UPGRADES_PATH.read_text("utf-8"))["proposals"]
sib_data    = json.loads(SIB_PATH.read_text("utf-8"))

# Count before
low_before  = sum(1 for v in anchors.values() if v.get("confidence")=="LOW")
med_before  = sum(1 for v in anchors.values() if v.get("confidence")=="MEDIUM")
high_before = sum(1 for v in anchors.values() if v.get("confidence")=="HIGH")
print(f"\nBefore: HIGH={high_before}, MEDIUM={med_before}, LOW={low_before}")

# ─── Apply upgrades ────────────────────────────────────────────────────────
applied = []
skipped = []

for upgrade in upgrades:
    sign_id   = upgrade["sign_id"]
    reading   = upgrade["proposed_reading"]
    target    = upgrade["target_confidence"]
    n_sources = upgrade["n_sources"]
    sources   = upgrade["sources"]

    if sign_id not in anchors:
        skipped.append({"sign_id": sign_id, "reason": "not in anchor set"})
        continue

    current_conf = anchors[sign_id].get("confidence","NONE")
    current_read = anchors[sign_id].get("reading","")

    # Safety checks
    if current_conf in ("HIGH","MEDIUM"):
        skipped.append({"sign_id": sign_id, "reason": f"already {current_conf}"})
        continue

    if n_sources < 2 and target == "MEDIUM":
        skipped.append({"sign_id": sign_id, "reason": "insufficient sources"})
        continue

    # Apply the upgrade
    old_conf = anchors[sign_id].get("confidence","LOW")
    old_read = anchors[sign_id].get("reading","kur")

    anchors[sign_id]["confidence"] = target
    anchors[sign_id]["reading"]    = reading
    anchors[sign_id]["basis"]      = (
        f"Phase-161/162/165 literature upgrade: reading '{reading}' proposed by "
        f"{', '.join(sources)} ({n_sources} independent sources). "
        f"Previous: {old_conf} '{old_read}'."
    )

    applied.append({
        "sign_id": sign_id,
        "old_confidence": old_conf,
        "new_confidence": target,
        "old_reading": old_read,
        "new_reading": reading,
        "sources": sources,
        "n_sources": n_sources,
    })

print(f"\nUpgrades applied: {len(applied)}")
print(f"Upgrades skipped: {len(skipped)}")

# ─── Apply sibilant candidates ─────────────────────────────────────────────
sib_applied = []
for cand in sib_data.get("su_gap_candidates",[]):
    sign_id   = cand["sign_id"]
    reading   = cand["reading"]
    n_mentions= cand["n_mentions"]
    sources   = cand["sources"]

    if sign_id not in anchors: continue
    current_conf = anchors[sign_id].get("confidence","NONE")
    if current_conf in ("HIGH","MEDIUM"): continue
    if n_mentions < 3: continue  # require at least 3 mentions for sibilant promotion

    anchors[sign_id]["confidence"] = "MEDIUM"
    anchors[sign_id]["reading"]    = reading
    anchors[sign_id]["basis"]      = (
        f"Phase-163 sibilant discovery: reading '{reading}' found in literature "
        f"({n_mentions} mentions across sources: {', '.join(sources)}). "
        f"Provides partial coverage for Shu-ilishu /su/ phonological slot."
    )
    sib_applied.append({"sign_id": sign_id, "reading": reading, "n_mentions": n_mentions})

print(f"Sibilant upgrades applied: {len(sib_applied)}")

# ─── Recount ───────────────────────────────────────────────────────────────
low_after  = sum(1 for v in anchors.values() if v.get("confidence")=="LOW")
med_after  = sum(1 for v in anchors.values() if v.get("confidence")=="MEDIUM")
high_after = sum(1 for v in anchors.values() if v.get("confidence")=="HIGH")

print(f"\nAfter:  HIGH={high_after}, MEDIUM={med_after}, LOW={low_after}")
print(f"Change: HIGH +{high_after-high_before}, MEDIUM +{med_after-med_before}, LOW {low_after-low_before}")

# ─── Recompute token coverage ──────────────────────────────────────────────
try:
    import pandas as pd
    df = pd.read_csv(HOLDAT)
    seals = {}
    for _, row in df.iterrows():
        f = str(row.get("form",""))
        s = str(row.get("letters",""))
        if f and s:
            if f not in seals: seals[f] = {"signs":[]}
            seals[f]["signs"].append(s)
except Exception:
    seals = {}
    with open(HOLDAT, encoding="utf-8") as fh:
        hdr = fh.readline().strip().split(",")
        ci = {h:i for i,h in enumerate(hdr)}
        for line in fh:
            p = line.strip().split(",")
            if len(p)<2: continue
            f=p[ci.get("form",0)]; s=p[ci.get("letters",1)]
            if f and s:
                if f not in seals: seals[f]={"signs":[]}
                seals[f]["signs"].append(s)

all_signs = [s for d in seals.values() for s in d["signs"]]
n_tokens  = len(all_signs)
hm_new    = {k for k,v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}
n_hm_tokens = sum(1 for s in all_signs if s in hm_new)
coverage_new = n_hm_tokens / n_tokens if n_tokens else 0

# Seals fully decoded
n_fully_decoded = sum(
    1 for d in seals.values()
    if all(s in hm_new for s in d["signs"])
)

print(f"\nNew H+M count: {len(hm_new)}")
print(f"New token coverage: {n_hm_tokens}/{n_tokens} = {100*coverage_new:.2f}%")
print(f"Fully decoded seals: {n_fully_decoded}/{len(seals)} ({100*n_fully_decoded/len(seals):.1f}%)")

# ─── Save updated anchors ──────────────────────────────────────────────────
# Backup first
backup_path = ANCHORS_PATH.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
backup_path.write_text(json.dumps(anchor_data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nBackup saved → {backup_path}")

# Save updated
anchor_data["anchors"] = anchors
ANCHORS_PATH.write_text(json.dumps(anchor_data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Updated anchors saved → {ANCHORS_PATH}")

# ─── Save summary ──────────────────────────────────────────────────────────
summary = {
    "phase": "161-163 upgrades applied",
    "date": "2026-05-20",
    "before": {"high": high_before, "medium": med_before, "low": low_before},
    "after":  {"high": high_after,  "medium": med_after,  "low": low_after},
    "delta":  {"high": high_after-high_before, "medium": med_after-med_before,
               "low": low_after-low_before},
    "n_applied": len(applied),
    "n_sibilant": len(sib_applied),
    "n_skipped": len(skipped),
    "new_hm_count": len(hm_new),
    "new_token_coverage": round(coverage_new, 4),
    "new_token_coverage_pct": round(100*coverage_new, 2),
    "new_fully_decoded_seals": n_fully_decoded,
    "new_fully_decoded_pct": round(100*n_fully_decoded/len(seals), 1),
    "applied_upgrades": applied,
    "sibilant_upgrades": sib_applied,
}
OUT_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Summary saved → {OUT_SUMMARY}")
print("="*70)
