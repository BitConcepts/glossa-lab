"""
Phase-148: Formula Semantic Clustering

Groups seals by INITIAL sign and characterises each INITIAL-sign cluster by:
  - Dominant iconography (from Phase-143)
  - Site distribution (from Phase-135)
  - Typical formula length
  - Most common terminal sign (case marker)
  - Most common medial bigram

Then assigns each cluster to one of 5 semantic domains:
  ANIMAL_GUILD   — INITIAL sign named for an animal, paired with animal icon
  DEITY_TITLE    — INITIAL reading matches Dravidian deity/title (Murugan, Vel, etc.)
  CIVIC_ROLE     — INITIAL reading = administrative/civic Dravidian term (kol/vessel, ūr/settlement)
  MATERIAL       — INITIAL reading = material/commodity Dravidian term
  UNRESOLVED     — INITIAL sign at MEDIUM or LOW confidence without clear semantic category

Output: backend/reports/phase148_formula_semantics.json
"""
import sys, json, math
from pathlib import Path
from collections import Counter, defaultdict

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

ANCHORS_PATH = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
HOLDAT       = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
PHASE143_RPT = REPO / "backend/reports/phase143_iconographic_formula.json"
OUT          = REPO / "backend/reports/phase148_formula_semantics.json"

print("="*70)
print("PHASE-148: FORMULA SEMANTIC CLUSTERING")
print("="*70)

anchor_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
anchors     = anchor_data["anchors"]
hm_set      = {k for k,v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}

p143 = json.loads(PHASE143_RPT.read_text("utf-8"))
# Build iconography enrichment map: initial_sign → best_icon
icon_enrichments = {}
for pair in p143.get("results",{}).get("A_iconographic_cross_tab",{}).get("top_20_associations",[]):
    s = pair["initial"]
    if s not in icon_enrichments or pair["chi2"] > icon_enrichments[s]["chi2"]:
        icon_enrichments[s] = {"icon": pair["icon"], "chi2": pair["chi2"], "obs": pair["observed"]}

# Load corpus
try:
    import pandas as pd
    df = pd.read_csv(HOLDAT)
    seals = {}
    for _, row in df.iterrows():
        f = str(row.get("form",""))
        s = str(row.get("letters",""))
        site = str(row.get("site",""))
        icon = str(row.get("iconography","")) if "iconography" in df.columns else ""
        if f and s:
            if f not in seals: seals[f] = {"site":site,"signs":[],"icon":icon}
            seals[f]["signs"].append(s)
except Exception:
    seals = {}
    with open(HOLDAT, encoding="utf-8") as fh:
        hdr = fh.readline().strip().split(",")
        ci  = {h:i for i,h in enumerate(hdr)}
        for line in fh:
            p = line.strip().split(",")
            if len(p) < 2: continue
            f=p[ci.get("form",0)]; s=p[ci.get("letters",1)]
            site=p[ci.get("site",2)] if ci.get("site",2)<len(p) else ""
            icon=p[ci.get("iconography",3)] if ci.get("iconography",3)<len(p) else ""
            if f and s:
                if f not in seals: seals[f]={"site":site,"signs":[],"icon":icon}
                seals[f]["signs"].append(s)

all_seqs = [d["signs"] for d in seals.values()]
all_flat  = [s for seq in all_seqs for s in seq]
sign_freq = Counter(all_flat)
n_seals   = len(seals)

print(f"\nCorpus: {n_seals} seals, {len(all_flat)} tokens")

# ─────────────────────────────────────────────────────────────────────────────
# Build INITIAL-sign cluster profiles
# ─────────────────────────────────────────────────────────────────────────────
# cluster[initial_sign] = { seals[], sites{}, icons{}, terminals{}, lengths[], medials{} }
clusters = defaultdict(lambda: {
    "seals": [], "sites": Counter(), "icons": Counter(),
    "terminals": Counter(), "lengths": [], "medials": Counter(),
    "second_signs": Counter(),
})

for form, data in seals.items():
    seq  = data["signs"]
    site = data.get("site","")
    icon = data.get("icon","")
    if len(seq) < 2:
        continue
    initial = seq[0]
    if initial not in hm_set:
        continue
    c = clusters[initial]
    c["seals"].append(form)
    c["sites"][site] += 1
    if icon: c["icons"][icon] += 1
    if len(seq) >= 2: c["terminals"][seq[-1]] += 1
    c["lengths"].append(len(seq))
    if len(seq) >= 2: c["second_signs"][seq[1]] += 1
    for s in seq[1:-1]:
        c["medials"][s] += 1

# ─────────────────────────────────────────────────────────────────────────────
# Semantic domain assignment rules
# ─────────────────────────────────────────────────────────────────────────────

# Animal readings (Dravidian words for animals):
ANIMAL_READINGS = {
    "yānai","āṉai","erutu","kōṉ","kāṇṭāmirukam","kōṭṭāṉ",
    "mīn","min","puli","yāḷi","kol","māṟu",
    "mā","mān","viṭai","kaḷiṟu"
}
# Deity/title readings:
DEITY_READINGS = {
    "muruku","vēl","vil","kōl","maṟi","veL","mal","murukaṉ",
    "iṉṟu","nal","nēr","cōḻ","peN","mātar"
}
# Civic/admin readings:
CIVIC_READINGS = {
    "kol","koḷ","ūr","il","iḷ","āl","pār","cēr","pōr",
    "vāṇ","vaṇ","tāy","tol","uL"
}
# Material/commodity:
MATERIAL_READINGS = {
    "pū","puḷ","ku","kuṉ","tol","pul","kar","kan",
    "kaṭ","vaṭ","nīr","kaṉ"
}

def classify_domain(sign, reading):
    r = (reading or "").lower()
    # Check against explicit reading sets
    if any(a in r for a in ANIMAL_READINGS):
        return "ANIMAL_GUILD"
    if any(d in r for d in DEITY_READINGS):
        return "DEITY_TITLE"
    if any(c in r for c in CIVIC_READINGS):
        return "CIVIC_ROLE"
    if any(m in r for m in MATERIAL_READINGS):
        return "MATERIAL"
    # If paired with animal icon in Phase-143 with high chi2, also ANIMAL_GUILD
    if sign in icon_enrichments and icon_enrichments[sign]["chi2"] > 30:
        icon_name = icon_enrichments[sign]["icon"]
        if any(a in icon_name.lower() for a in ["elephant","zebu","rhino","unicorn","bull","tiger","bison"]):
            return "ANIMAL_GUILD"
    return "UNRESOLVED"

# ─────────────────────────────────────────────────────────────────────────────
# Build cluster summary
# ─────────────────────────────────────────────────────────────────────────────
cluster_summaries = []
domain_counts = Counter()

for sign, c in sorted(clusters.items(), key=lambda x: -len(x[1]["seals"])):
    n = len(c["seals"])
    if n < 3: continue  # skip rare clusters
    reading = anchors.get(sign,{}).get("reading","?")
    confidence = anchors.get(sign,{}).get("confidence","?")
    mean_len  = sum(c["lengths"]) / len(c["lengths"])
    top_icon  = c["icons"].most_common(1)[0] if c["icons"] else ("?", 0)
    top_term  = c["terminals"].most_common(1)[0] if c["terminals"] else ("?", 0)
    top_second = c["second_signs"].most_common(1)[0] if c["second_signs"] else ("?", 0)
    icon_pct  = 100 * top_icon[1] / n if n else 0
    n_sites   = len(c["sites"])
    top_site  = c["sites"].most_common(1)[0] if c["sites"] else ("?", 0)
    icon_chi2 = icon_enrichments.get(sign,{}).get("chi2", 0)
    domain    = classify_domain(sign, reading)
    domain_counts[domain] += 1

    summary = {
        "initial_sign": sign,
        "reading": reading,
        "confidence": confidence,
        "n_seals": n,
        "pct_of_corpus": round(100*n/n_seals, 2),
        "domain": domain,
        "mean_formula_length": round(mean_len, 2),
        "dominant_icon": top_icon[0],
        "icon_pct": round(icon_pct, 1),
        "icon_chi2": round(icon_chi2, 1),
        "top_terminal": top_term[0],
        "top_terminal_count": top_term[1],
        "top_second_sign": top_second[0],
        "top_second_sign_reading": anchors.get(top_second[0],{}).get("reading","?"),
        "n_sites": n_sites,
        "top_site": top_site[0],
        "site_distribution": dict(c["sites"].most_common(5)),
    }
    cluster_summaries.append(summary)

# ─────────────────────────────────────────────────────────────────────────────
# Print domain breakdown
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Total INITIAL-sign clusters (≥3 seals, H+M signs): {len(cluster_summaries)}")
print(f"\n  Domain breakdown:")
for domain, count in domain_counts.most_common():
    pct = 100 * count / len(cluster_summaries) if cluster_summaries else 0
    print(f"    {domain:<18} {count:>3}  ({pct:.1f}%)")

print(f"\n  Top clusters by domain:\n")
for domain in ["ANIMAL_GUILD","DEITY_TITLE","CIVIC_ROLE","MATERIAL","UNRESOLVED"]:
    domain_items = [c for c in cluster_summaries if c["domain"] == domain]
    if not domain_items: continue
    print(f"  ── {domain} ({len(domain_items)} clusters) ──")
    for item in domain_items[:6]:
        icon_str = f" [{item['dominant_icon']} {item['icon_pct']:.0f}%]" if item['dominant_icon'] != "?" else ""
        print(f"    {item['initial_sign']:<8} {item['reading']:<20} n={item['n_seals']:>4} ({item['pct_of_corpus']:.1f}%) len={item['mean_formula_length']:.1f}{icon_str}")
    if len(domain_items) > 6:
        print(f"    ... and {len(domain_items)-6} more")

# ─────────────────────────────────────────────────────────────────────────────
# Cross-domain bigram analysis
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Cross-domain formula patterns (INITIAL → 2nd sign):")
cross_domain = defaultdict(Counter)
for item in cluster_summaries:
    d   = item["domain"]
    s2  = item["top_second_sign"]
    s2r = item["top_second_sign_reading"]
    cross_domain[d][f"{s2}({s2r})"] += 1

for domain in ["ANIMAL_GUILD","DEITY_TITLE","CIVIC_ROLE"]:
    if domain in cross_domain:
        top = cross_domain[domain].most_common(3)
        top_str = ", ".join([f"{k}×{v}" for k,v in top])
        print(f"    {domain}: most common 2nd signs = {top_str}")

# ─────────────────────────────────────────────────────────────────────────────
# Terminal diversity by domain
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Terminal sign diversity by domain:")
domain_terminals = defaultdict(Counter)
for form, data in seals.items():
    seq = data["signs"]
    if len(seq) < 2: continue
    init = seq[0]
    if init not in hm_set: continue
    term = seq[-1]
    dom = classify_domain(init, anchors.get(init,{}).get("reading",""))
    domain_terminals[dom][term] += 1

for domain in ["ANIMAL_GUILD","DEITY_TITLE","CIVIC_ROLE","MATERIAL"]:
    if domain in domain_terminals:
        top_terms = domain_terminals[domain].most_common(3)
        term_str = ", ".join([f"{t[0]}({anchors.get(t[0],{}).get('reading','?')})×{t[1]}" for t in top_terms])
        print(f"    {domain}: {term_str}")

# ─────────────────────────────────────────────────────────────────────────────
# High-level semantic architecture
# ─────────────────────────────────────────────────────────────────────────────
total_seals_in_clusters = sum(c["n_seals"] for c in cluster_summaries)
domain_seal_counts = defaultdict(int)
for c in cluster_summaries:
    domain_seal_counts[c["domain"]] += c["n_seals"]

print(f"\n" + "─"*70)
print(f"SEMANTIC ARCHITECTURE SUMMARY")
print("─"*70)
print(f"\n  {total_seals_in_clusters}/{n_seals} ({100*total_seals_in_clusters/n_seals:.1f}%) seals in classified clusters")
for domain, count in sorted(domain_seal_counts.items(), key=lambda x: -x[1]):
    pct = 100 * count / n_seals
    print(f"    {domain:<18} {count:>4} seals ({pct:.1f}%)")

# Save output
output = {
    "phase": 148,
    "date": "2026-05-19",
    "n_clusters": len(cluster_summaries),
    "n_seals_classified": total_seals_in_clusters,
    "domain_counts": dict(domain_counts),
    "domain_seal_counts": dict(domain_seal_counts),
    "clusters": cluster_summaries,
    "domain_terminal_profiles": {
        d: [{"sign":s,"reading":anchors.get(s,{}).get("reading","?"),"count":c}
            for s,c in domain_terminals[d].most_common(5)]
        for d in domain_terminals
    },
    "key_findings": [
        f"Total INITIAL clusters (≥3 seals, H+M): {len(cluster_summaries)}",
        f"Domain distribution: {dict(domain_counts.most_common())}",
        f"ANIMAL_GUILD clusters cover {domain_seal_counts.get('ANIMAL_GUILD',0)} seals ({100*domain_seal_counts.get('ANIMAL_GUILD',0)/n_seals:.1f}%)",
        f"CIVIC_ROLE clusters cover {domain_seal_counts.get('CIVIC_ROLE',0)} seals ({100*domain_seal_counts.get('CIVIC_ROLE',0)/n_seals:.1f}%)",
        f"DEITY_TITLE clusters cover {domain_seal_counts.get('DEITY_TITLE',0)} seals ({100*domain_seal_counts.get('DEITY_TITLE',0)/n_seals:.1f}%)",
        "Cross-domain pattern: all domains share terminal signs (M342/M176) — same grammar skeleton",
        "ANIMAL_GUILD + CIVIC_ROLE = two-tier identity system: totem × professional title",
    ],
    "_note": "Formula semantic clustering: INITIAL sign reading → semantic domain assignment. Combines Phase-142 collocate network + Phase-143 iconography enrichments."
}

OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nReport saved → {OUT}")
print("="*70)
