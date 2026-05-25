"""Phase-252: Allograph Crosswalk Fix + HIGH Upgrades

Phase-250 found 341 STRONG allograph pairs but couldn't apply HIGH upgrades
because the Holdat corpus uses bare numeric IDs ("034") while the anchor table
uses M-prefixed IDs ("M034").

This script:
  1. Re-runs allograph detection with M-prefix added to corpus sign IDs
  2. For each STRONG pair (r >= 0.95):
     - If one sign is HIGH and the other is MEDIUM → upgrade MEDIUM to HIGH
     - Document the allograph relationship
  3. Also identify allograph clusters (signs with identical positional profiles)
     and assign them group labels — within a group, all signs share function
  4. Apply upgrades to INDUS_FINAL_ANCHORS.json

Output: outputs/phase252_allograph_upgrade.json
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO    = Path(__file__).resolve().parents[2]
OUT     = REPO / "outputs" / "phase252_allograph_upgrade.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

def load(p: Path) -> dict:
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


def pearson(va: list, vb: list) -> float:
    n = len(va)
    ma = sum(va) / n
    mb = sum(vb) / n
    num = sum((va[k]-ma)*(vb[k]-mb) for k in range(n))
    da = math.sqrt(sum((x-ma)**2 for x in va))
    db = math.sqrt(sum((x-mb)**2 for x in vb))
    return round(num/(da*db), 4) if da > 0 and db > 0 else 0.0


def main():
    print("Phase-252: Allograph Crosswalk Fix + HIGH Upgrades\n")

    # Load corpus with M-prefix fix
    import sys, os
    sys.path.insert(0, str(REPO / "backend"))
    os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))
    try:
        from glossa_lab.data.indus_m77 import get_corpus_inscriptions
        raw_inscriptions = get_corpus_inscriptions()
    except Exception as e:
        print(f"  Corpus load failed: {e}")
        return {"error": str(e)}

    # Check ID format in corpus
    sample_ids = {s for seq in raw_inscriptions[:10] for s in seq}
    has_m_prefix = any(s.startswith("M") for s in sample_ids)
    print(f"  Corpus ID format: {'M-prefixed' if has_m_prefix else 'numeric only'}")
    print(f"  Sample IDs: {sorted(sample_ids)[:5]}")

    # Fix: add M prefix if needed
    inscriptions = []
    for seq in raw_inscriptions:
        fixed = [f"M{s}" if not s.startswith("M") else s for s in seq]
        inscriptions.append(fixed)

    print(f"  Inscriptions: {len(inscriptions)}")
    sample_fixed = {s for seq in inscriptions[:5] for s in seq}
    print(f"  Fixed IDs: {sorted(sample_fixed)[:5]}")

    # Compute I/M/T rates
    total_c: Counter = Counter()
    init_c: Counter  = Counter()
    term_c: Counter  = Counter()
    med_c: Counter   = Counter()

    for seq in inscriptions:
        if not seq: continue
        for i, s in enumerate(seq):
            total_c[s] += 1
            if i == 0 and len(seq) > 1:       init_c[s] += 1
            elif i == len(seq)-1 and len(seq) > 1: term_c[s] += 1
            elif 0 < i < len(seq)-1:           med_c[s] += 1

    profiles: dict[str, dict] = {}
    for sign, n in total_c.items():
        if n < 3: continue
        profiles[sign] = {
            "i": round(init_c[sign]/n, 4),
            "m": round(med_c[sign]/n, 4),
            "t": round(term_c[sign]/n, 4),
            "n": n,
        }

    print(f"  Signs with n >= 3: {len(profiles)}")

    # Load anchors
    anchors_raw = load(ANCHORS)
    anchors = anchors_raw.get("anchors", {})

    n_before_high = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
    n_before_med  = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")
    print(f"  Before: {n_before_high} HIGH + {n_before_med} MEDIUM")

    # Compute pairwise correlations (only for signs in anchor table)
    anchor_sign_ids = set(anchors.keys())
    profiled_in_anchors = {s: profiles[s] for s in profiles if s in anchor_sign_ids}
    print(f"  Signs with profiles AND in anchor table: {len(profiled_in_anchors)}")

    # Find allograph pairs
    allograph_pairs = []
    signs = sorted(profiled_in_anchors.keys())
    for i, s1 in enumerate(signs):
        p1 = profiled_in_anchors[s1]
        for s2 in signs[i+1:]:
            p2 = profiled_in_anchors[s2]
            r = pearson([p1["i"], p1["m"], p1["t"]], [p2["i"], p2["m"], p2["t"]])
            if r < 0.90: continue
            c1 = anchors[s1].get("confidence", "?")
            c2 = anchors[s2].get("confidence", "?")
            r1 = anchors[s1].get("reading", "")
            r2 = anchors[s2].get("reading", "")
            allograph_pairs.append({
                "s1": s1, "c1": c1, "r1": r1, "n1": p1["n"],
                "s2": s2, "c2": c2, "r2": r2, "n2": p2["n"],
                "corr": r,
                "strong": r >= 0.95,
            })

    allograph_pairs.sort(key=lambda x: -x["corr"])
    n_strong = sum(1 for x in allograph_pairs if x["strong"])
    print(f"  Allograph pairs (r>=0.90): {len(allograph_pairs)} ({n_strong} strong r>=0.95)")

    # Show top 20
    print("\n  TOP 20 ALLOGRAPH PAIRS:")
    for p in allograph_pairs[:20]:
        print(f"    {p['s1']}({p['r1']},{p['c1']},n={p['n1']}) ↔ "
              f"{p['s2']}({p['r2']},{p['c2']},n={p['n2']}) r={p['corr']}")

    # Build allograph CLUSTERS using union-find
    parent: dict[str, str] = {s: s for s in signs}
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(x, y):
        px, py = find(x), find(y)
        if px != py: parent[px] = py

    for p in allograph_pairs:
        if p["corr"] >= 0.95:
            union(p["s1"], p["s2"])

    clusters: dict[str, list] = defaultdict(list)
    for s in signs:
        clusters[find(s)].append(s)

    multi_clusters = {k: v for k, v in clusters.items() if len(v) >= 2}
    print(f"\n  Allograph clusters (>=2 signs, r>=0.95): {len(multi_clusters)}")
    for root, members in sorted(multi_clusters.items(), key=lambda x: -len(x[1]))[:10]:
        confs = [f"{m}({anchors.get(m,{}).get('confidence','?')})" for m in members]
        print(f"    Cluster: {', '.join(confs)}")

    # Apply HIGH upgrades: within a cluster, if any sign is HIGH and another is MEDIUM,
    # upgrade MEDIUM to HIGH (they are allographs → same reading family)
    n_upgraded = 0
    upgrade_log = []
    for root, members in multi_clusters.items():
        high_members = [m for m in members if anchors.get(m, {}).get("confidence") == "HIGH"]
        med_members  = [m for m in members if anchors.get(m, {}).get("confidence") == "MEDIUM"]
        if not high_members or not med_members:
            continue
        # Check correlation between HIGH and MEDIUM members
        for hm in high_members:
            for mm in med_members:
                ph = profiled_in_anchors[hm]
                pm = profiled_in_anchors[mm]
                r = pearson([ph["i"], ph["m"], ph["t"]], [pm["i"], pm["m"], pm["t"]])
                if r >= 0.92:
                    # Upgrade MEDIUM to HIGH
                    rh = anchors[hm].get("reading", "")
                    rm = anchors[mm].get("reading", "")
                    anchors[mm]["confidence"] = "HIGH"
                    anchors[mm]["phase_upgraded"] = 252
                    anchors[mm]["upgrade_basis"] = (
                        f"Phase-252: Allograph of {hm} (r={r:.3f}, HIGH). "
                        f"Daggumati & Revesz (2021) positional correlation method. "
                        f"Same positional profile → same grammatical function → allograph. "
                        f"Inherits HIGH confidence from {hm}='{rh}'."
                    )
                    n_upgraded += 1
                    upgrade_log.append({
                        "upgraded": mm, "reading_m": rm,
                        "allograph_of": hm, "reading_h": rh,
                        "correlation": r,
                    })
                    print(f"    HIGH: {mm}('{rm}') ↔ {hm}('{rh}') r={r:.3f}")

    # Recount
    n_after_high = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
    n_after_med  = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")
    n_after_low  = sum(1 for v in anchors.values() if v.get("confidence") == "LOW")

    print(f"\n  HIGH upgrades applied: {n_upgraded}")
    print(f"  After: {n_after_high} HIGH + {n_after_med} MEDIUM + {n_after_low} LOW")
    print(f"  H+M total: {n_after_high + n_after_med}/413")

    # Save
    anchors_raw["anchors"] = anchors
    ANCHORS.write_text(json.dumps(anchors_raw, indent=2, ensure_ascii=False), encoding="utf-8")
    print("  INDUS_FINAL_ANCHORS.json saved.")

    result = {
        "phase": 252,
        "generated_at": datetime.now().isoformat(),
        "n_profiles_in_anchors": len(profiled_in_anchors),
        "n_allograph_pairs_090": len(allograph_pairs),
        "n_allograph_strong_095": n_strong,
        "n_clusters": len(multi_clusters),
        "n_high_upgrades": n_upgraded,
        "upgrade_log": upgrade_log,
        "before": {"HIGH": n_before_high, "MEDIUM": n_before_med},
        "after": {"HIGH": n_after_high, "MEDIUM": n_after_med, "LOW": n_after_low,
                  "HM_total": n_after_high + n_after_med},
        "top_pairs": allograph_pairs[:30],
        "clusters": [{"root": k, "members": v} for k, v in
                     sorted(multi_clusters.items(), key=lambda x: -len(x[1]))[:20]],
        "verdict": (
            f"Phase-252: {len(allograph_pairs)} allograph pairs (r>=0.90) in anchor corpus. "
            f"{n_strong} strong (r>=0.95). {len(multi_clusters)} clusters. "
            f"{n_upgraded} HIGH upgrades applied. "
            f"H: {n_before_high} → {n_after_high}. "
            f"H+M: {n_before_high+n_before_med} → {n_after_high+n_after_med}/413."
        ),
    }

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"\n  VERDICT: {result['verdict']}")
    return result


if __name__ == "__main__":
    main()
