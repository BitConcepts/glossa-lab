"""Phase-111: Allograph / Variant Resolution.

Groups the 220 rare signs (freq 1-4) onto confirmed signs by positional
profile similarity (L1 distance on I/M/T rates). Allographs inherit the
confirmed sign's reading. Extends token coverage toward 100%.

CPU only. Output: reports/phase111_allograph_resolution.json
Also updates backend/reports/INDUS_FINAL_ANCHORS.json
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase111_allograph_resolution.json"

MAX_L1_DIST = 0.35  # max L1 distance to call two signs allographs
MIN_FREQ_CONFIRMED = 5   # confirmed signs need enough data for reliable profile
MAX_FREQ_RARE = 4        # rare signs are freq 1-4


def load_corpus():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number", ""); p = int(row.get("position", 0) or 0)
            if not c: continue
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    return {c: [s for s in v if s] for c, v in seals.items() if any(v)}


def compute_profiles(seals: dict, min_count: int = 1) -> dict:
    """Compute I/M/T positional profile per sign."""
    total  = Counter(s for signs in seals.values() for s in signs)
    init_c = Counter(signs[0]  for signs in seals.values() if len(signs) > 1)
    term_c = Counter(signs[-1] for signs in seals.values() if len(signs) > 1)
    med_c  = Counter(s for signs in seals.values() for s in signs[1:-1])

    profiles = {}
    for sign, n in total.items():
        if n < min_count:
            continue
        i_rate = init_c[sign] / n
        t_rate = term_c[sign] / n
        m_rate = med_c[sign]  / n
        profiles[sign] = {"i": round(i_rate, 4), "t": round(t_rate, 4),
                          "m": round(m_rate, 4), "freq": n}
    return profiles


def l1_dist(a: dict, b: dict) -> float:
    return abs(a["i"] - b["i"]) + abs(a["t"] - b["t"]) + abs(a["m"] - b["m"])


def main():
    print("Phase-111: Allograph / Variant Resolution\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}
    print(f"  Confirmed signs: {len(confirmed)}")

    seals = load_corpus()
    flat_freq = Counter(s for signs in seals.values() for s in signs)
    print(f"  Corpus: {len(seals)} seals, {sum(flat_freq.values())} tokens, {len(flat_freq)} distinct signs")

    # Compute profiles for all signs
    profiles = compute_profiles(seals, min_count=1)

    # Confirmed profiles (need freq >= MIN_FREQ_CONFIRMED for reliable data)
    conf_profiles = {s: p for s, p in profiles.items()
                     if s in confirmed and p["freq"] >= MIN_FREQ_CONFIRMED}

    # Rare signs not yet assigned
    rare_signs = [(s, flat_freq[s]) for s in flat_freq
                  if s not in confirmed and flat_freq[s] <= MAX_FREQ_RARE and s in profiles]
    rare_signs.sort(key=lambda x: -x[1])
    print(f"  Rare unread signs (freq 1-{MAX_FREQ_RARE}): {len(rare_signs)}")

    # For each rare sign, find nearest confirmed sign by L1 profile distance
    allograph_map = []
    n_resolved = 0

    for rare_sign, freq in rare_signs:
        rare_p = profiles[rare_sign]
        best_sign = None
        best_dist = float("inf")

        for conf_sign, conf_p in conf_profiles.items():
            d = l1_dist(rare_p, conf_p)
            if d < best_dist:
                best_dist = d
                best_sign = conf_sign

        if best_sign and best_dist <= MAX_L1_DIST:
            confirmed_reading = anchors[best_sign].get("reading", "")
            confirmed_conf    = anchors[best_sign].get("confidence", "")
            allograph_map.append({
                "rare_sign": rare_sign,
                "freq": freq,
                "matched_to": best_sign,
                "l1_dist": round(best_dist, 4),
                "inherited_reading": confirmed_reading,
                "base_confidence": confirmed_conf,
                "rare_profile": rare_p,
                "base_profile": conf_profiles[best_sign],
            })

            # Add as LOW confidence (allograph — positional profile match only)
            anchors[rare_sign] = {
                "reading": confirmed_reading,
                "confidence": "LOW",
                "basis": (
                    f"Phase-111 allograph resolution: positional profile L1={best_dist:.3f} "
                    f"matches {best_sign} ('{confirmed_reading}', {confirmed_conf}). "
                    f"I={rare_p['i']:.3f} T={rare_p['t']:.3f} M={rare_p['m']:.3f}. freq={freq}."
                ),
                "source": "Phase-111",
            }
            n_resolved += 1
            print(f"  {rare_sign}(f={freq}) → {best_sign}='{confirmed_reading}' L1={best_dist:.3f}")
        else:
            dist_str = f"{best_dist:.3f}" if best_dist < float("inf") else "∞"
            allograph_map.append({
                "rare_sign": rare_sign, "freq": freq,
                "matched_to": None, "l1_dist": best_dist,
                "reason": f"best_dist={dist_str} > threshold {MAX_L1_DIST}",
            })

    # Save anchors
    anchors_data["anchors"] = anchors
    anchors_data["total"] = len(anchors)
    ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Coverage after allograph resolution (including LOW)
    total_tokens = sum(flat_freq.values())
    cov_hm  = sum(flat_freq.get(s, 0) for s in anchors
                  if anchors[s].get("confidence") in ("HIGH", "MEDIUM"))
    cov_all = sum(flat_freq.get(s, 0) for s in anchors
                  if anchors[s].get("confidence") in ("HIGH", "MEDIUM", "LOW"))
    print(f"\n  Allographs resolved: {n_resolved}/{len(rare_signs)}")
    print(f"  H+M token coverage: {cov_hm/total_tokens:.1%}")
    print(f"  H+M+LOW (inc. allographs): {cov_all/total_tokens:.1%}")

    result = {
        "phase": 111,
        "max_l1_threshold": MAX_L1_DIST,
        "n_rare_signs": len(rare_signs),
        "n_resolved": n_resolved,
        "n_unresolved": len(rare_signs) - n_resolved,
        "hm_token_coverage": round(cov_hm / total_tokens, 4),
        "hml_token_coverage": round(cov_all / total_tokens, 4),
        "allograph_map": allograph_map,
        "resolved_signs": [e["rare_sign"] for e in allograph_map if e.get("matched_to")],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"  Phase-111 complete: {n_resolved} allographs resolved, coverage inc. LOW = {cov_all/total_tokens:.1%}")
    return result


if __name__ == "__main__":
    main()
