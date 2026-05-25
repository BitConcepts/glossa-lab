"""Phase-253: CISI Allograph Clustering

Extends Phase-252 allograph method to the CISI corpus (P-signs).
Computes positional profiles for all 181 CISI P-signs, then cross-references
against HIGH Holdat M-sign profiles.

A CISI P-sign that has high positional correlation with a HIGH M-sign is a
probable allograph → it encodes the same phoneme in a different graphic form.

Results:
  - CANDIDATE P-signs (P324, P385, P332 etc.) may be allographs of HIGH M-signs
    → confirm/reinforce their proposed readings
  - CISI-exclusive P-signs with no proposed reading that match a HIGH M-sign
    → get a reading via allograph inheritance

Output: outputs/phase253_cisi_allograph.json
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO    = Path(__file__).resolve().parents[2]
OUT     = REPO / "outputs" / "phase253_cisi_allograph.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

def load(p: Path) -> dict:
    return json.loads(p.read_text("utf-8")) if p.exists() else {}

def pearson(va: list, vb: list) -> float:
    n = len(va)
    if n == 0: return 0.0
    ma = sum(va)/n; mb = sum(vb)/n
    num = sum((va[k]-ma)*(vb[k]-mb) for k in range(n))
    da = math.sqrt(sum((x-ma)**2 for x in va))
    db = math.sqrt(sum((x-mb)**2 for x in vb))
    return round(num/(da*db), 4) if da > 0 and db > 0 else 0.0

def build_profiles(inscriptions: list, min_freq: int = 3, prefix: str = "") -> dict:
    tot: Counter = Counter(); ini: Counter = Counter()
    ter: Counter = Counter(); med: Counter = Counter()
    for seq in inscriptions:
        if not seq: continue
        for i, s in enumerate(seq):
            if prefix and not s.startswith(prefix):
                s = prefix + s
            tot[s] += 1
            if i == 0 and len(seq) > 1:        ini[s] += 1
            elif i == len(seq)-1 and len(seq)>1: ter[s] += 1
            elif 0 < i < len(seq)-1:             med[s] += 1
    return {s: {"i": round(ini[s]/n,4), "m": round(med[s]/n,4),
                "t": round(ter[s]/n,4), "n": n}
            for s, n in tot.items() if n >= min_freq}


def main():
    print("Phase-253: CISI Allograph Clustering\n")

    # Load CISI corpus
    try:
        from glossa_lab.data.indus_cisi import get_corpus_inscriptions as cisi_inscs
        cisi_raw = cisi_inscs()
    except Exception as e:
        print(f"  CISI load failed: {e}")
        return {"error": str(e)}

    # Load Holdat corpus
    try:
        from glossa_lab.data.indus_m77 import get_corpus_inscriptions as m77_inscs
        holdat_raw = m77_inscs()
    except Exception as e:
        print(f"  Holdat load failed: {e}")
        return {"error": str(e)}

    print(f"  CISI inscriptions: {len(cisi_raw)}")
    print(f"  Holdat inscriptions: {len(holdat_raw)}")

    # Detect ID formats
    cisi_sample = {s for seq in cisi_raw[:5] for s in seq}
    holdat_sample = {s for seq in holdat_raw[:5] for s in seq}
    print(f"  CISI IDs sample: {sorted(cisi_sample)[:5]}")
    print(f"  Holdat IDs sample: {sorted(holdat_sample)[:5]}")

    # Fix Holdat IDs to M-prefix
    holdat = []
    for seq in holdat_raw:
        holdat.append([f"M{s}" if not s.startswith("M") else s for s in seq])

    # Fix CISI IDs to P-prefix
    cisi = []
    for seq in cisi_raw:
        fixed = []
        for s in seq:
            if not s.startswith("P") and not s.startswith("M"):
                s = f"P{s}"
            fixed.append(s)
        cisi.append(fixed)

    # Build profiles
    holdat_profiles = build_profiles(holdat, min_freq=3)
    cisi_profiles   = build_profiles(cisi,   min_freq=2)  # lower threshold for CISI

    print(f"  Holdat profiles (n>=3): {len(holdat_profiles)}")
    print(f"  CISI profiles (n>=2):   {len(cisi_profiles)}")

    # Load anchors
    anchors_raw = load(ANCHORS)
    anchors = anchors_raw.get("anchors", {})
    n_before_high = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
    print(f"  Current HIGH: {n_before_high}")

    # HIGH Holdat signs with profiles
    high_with_profiles = {s: holdat_profiles[s] for s in holdat_profiles
                          if s in anchors and anchors[s].get("confidence") == "HIGH"}
    print(f"  HIGH M-signs with Holdat profiles: {len(high_with_profiles)}")

    # Cross-correlate CISI P-signs vs HIGH Holdat signs
    cisi_allograph_hits = []
    for ps, pp in cisi_profiles.items():
        for hs, hp in high_with_profiles.items():
            r = pearson([pp["i"], pp["m"], pp["t"]], [hp["i"], hp["m"], hp["t"]])
            if r >= 0.88:
                cisi_allograph_hits.append({
                    "cisi_sign": ps,
                    "holdat_sign": hs,
                    "holdat_reading": anchors[hs].get("reading", ""),
                    "correlation": r,
                    "cisi_profile": pp,
                    "holdat_profile": hp,
                    "cisi_in_anchors": ps in anchors,
                    "cisi_confidence": anchors.get(ps, {}).get("confidence", "NOT_IN_ANCHORS"),
                    "verdict": "STRONG_ALLOGRAPH" if r >= 0.95 else "CANDIDATE_ALLOGRAPH",
                })

    cisi_allograph_hits.sort(key=lambda x: -x["correlation"])
    strong = [x for x in cisi_allograph_hits if x["verdict"] == "STRONG_ALLOGRAPH"]
    print(f"\n  CISI↔Holdat allograph hits (r>=0.88): {len(cisi_allograph_hits)}")
    print(f"  STRONG (r>=0.95): {len(strong)}")

    # Show top hits
    print("\n  TOP 20 CISI↔HOLDAT ALLOGRAPH PAIRS:")
    for h in cisi_allograph_hits[:20]:
        print(f"    {h['cisi_sign']}(CISI,{h['cisi_confidence']}) ↔ "
              f"{h['holdat_sign']}='{h['holdat_reading']}'(HIGH) r={h['correlation']}")

    # Check our 6 CANDIDATE P-signs specifically
    candidates = {k: v for k, v in anchors.items() if v.get("confidence") == "CANDIDATE"}
    print(f"\n  Our CANDIDATE P-signs: {list(candidates.keys())}")
    candidate_allographs = [h for h in cisi_allograph_hits if h["cisi_sign"] in candidates]
    print(f"  CANDIDATE signs with allograph matches: {len(candidate_allographs)}")
    for h in candidate_allographs:
        print(f"    {h['cisi_sign']}='{anchors[h['cisi_sign']].get('reading','')}' ↔ "
              f"{h['holdat_sign']}='{h['holdat_reading']}' r={h['correlation']}")

    # Apply upgrades: CANDIDATE P-signs with HIGH allograph match → upgrade to MEDIUM
    # (require r>=0.92 for CANDIDATE → MEDIUM; r>=0.95 for MEDIUM → HIGH)
    n_upgraded = 0
    upgrade_log = []

    for h in cisi_allograph_hits:
        ps = h["cisi_sign"]
        hs = h["holdat_sign"]
        r  = h["correlation"]
        holdat_reading = h["holdat_reading"]
        ps_conf = anchors.get(ps, {}).get("confidence", "NOT_IN_ANCHORS")

        if ps_conf == "CANDIDATE" and r >= 0.92:
            # CANDIDATE → MEDIUM via allograph
            anchors[ps]["confidence"] = "MEDIUM"
            anchors[ps]["phase_upgraded"] = 253
            anchors[ps]["allograph_of"] = hs
            anchors[ps]["allograph_corr"] = r
            anchors[ps]["upgrade_basis"] = (
                f"Phase-253: CISI allograph of {hs}='{holdat_reading}' (HIGH, r={r:.3f}). "
                f"Same positional profile in CISI corpus as HIGH Holdat sign. "
                f"Inherits reading family and grammatical function."
            )
            if not anchors[ps].get("reading"):
                anchors[ps]["reading"] = holdat_reading
                anchors[ps]["reading_source"] = f"allograph_of_{hs}"
            n_upgraded += 1
            upgrade_log.append({
                "cisi": ps, "holdat": hs, "holdat_reading": holdat_reading,
                "corr": r, "upgrade": "CANDIDATE→MEDIUM",
            })
            print(f"  ↑ {ps}: CANDIDATE → MEDIUM (allograph of {hs}='{holdat_reading}', r={r:.3f})")

        elif ps_conf == "MEDIUM" and r >= 0.95:
            # MEDIUM → HIGH via allograph (only for very high correlation)
            anchors[ps]["confidence"] = "HIGH"
            anchors[ps]["phase_upgraded"] = 253
            anchors[ps]["allograph_of"] = hs
            anchors[ps]["allograph_corr"] = r
            anchors[ps]["upgrade_basis"] = (
                f"Phase-253: CISI allograph of {hs}='{holdat_reading}' (HIGH, r={r:.3f}). "
                f"CISI sign positionally identical to HIGH Holdat sign → HIGH confidence."
            )
            n_upgraded += 1
            upgrade_log.append({
                "cisi": ps, "holdat": hs, "holdat_reading": holdat_reading,
                "corr": r, "upgrade": "MEDIUM→HIGH",
            })
            print(f"  ↑↑ {ps}: MEDIUM → HIGH (allograph of {hs}='{holdat_reading}', r={r:.3f})")

    # Recount
    n_high = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
    n_med  = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")
    n_low  = sum(1 for v in anchors.values() if v.get("confidence") == "LOW")
    n_cand = sum(1 for v in anchors.values() if v.get("confidence") == "CANDIDATE")

    print(f"\n  Upgrades applied: {n_upgraded}")
    print(f"  After: {n_high} HIGH + {n_med} MEDIUM + {n_low} LOW + {n_cand} CANDIDATE")
    print(f"  H+M: {n_high + n_med}/413 = {(n_high+n_med)/413:.1%}")

    # Save
    anchors_raw["anchors"] = anchors
    ANCHORS.write_text(json.dumps(anchors_raw, indent=2, ensure_ascii=False), encoding="utf-8")
    print("  INDUS_FINAL_ANCHORS.json saved.")

    # Summary of CISI-specific insights
    # How many CISI-exclusive P-signs now have allograph-derived readings?
    cisi_with_readings = [(h["cisi_sign"], h["holdat_reading"], h["correlation"])
                          for h in cisi_allograph_hits if h["cisi_sign"] not in
                          {k for k, v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")
                           and "allograph" not in v.get("upgrade_basis","")[:20]}]

    result = {
        "phase": 253,
        "generated_at": datetime.now().isoformat(),
        "n_cisi_profiles": len(cisi_profiles),
        "n_holdat_high_profiles": len(high_with_profiles),
        "n_allograph_hits": len(cisi_allograph_hits),
        "n_strong_hits": len(strong),
        "n_upgrades": n_upgraded,
        "upgrade_log": upgrade_log,
        "candidate_allographs": candidate_allographs,
        "top_hits": cisi_allograph_hits[:40],
        "after": {"HIGH": n_high, "MEDIUM": n_med, "LOW": n_low,
                  "CANDIDATE": n_cand, "HM_total": n_high+n_med},
        "ceiling_impact": (
            f"CISI allograph analysis: {len(cisi_allograph_hits)} P-sign↔M-sign pairs (r>=0.88). "
            f"{len(strong)} STRONG (r>=0.95). {n_upgraded} upgrades applied. "
            f"Ceiling 1 impact: CISI exclusive signs with Holdat allographs inherit readings "
            f"→ effectively extends our HIGH count to CISI corpus."
        ),
        "verdict": (
            f"Phase-253: {len(cisi_allograph_hits)} CISI↔Holdat allograph matches. "
            f"{n_upgraded} upgrades. H: {n_before_high}→{n_high}. "
            f"H+M: {n_high+n_med}/413 ({(n_high+n_med)/413:.1%})."
        ),
    }

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"\n  VERDICT: {result['verdict']}")
    return result


if __name__ == "__main__":
    main()
