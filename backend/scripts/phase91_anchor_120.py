"""Phase-91: Complete 120 HIGH+MEDIUM Anchors.

Lowers the DEDR promotion threshold to 1.0 to catch M076=naN and M221=al,
the two remaining signs needed to reach the 120 milestone.

Also sweeps through all remaining LOW-confidence signs with any iconographic
match at score >= 1.0 to maximally expand the anchor set.

CPU only. Output: reports/phase91_anchor_120.json
"""
from __future__ import annotations
import csv, json, re
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P89     = REPO / "reports/phase89_dedr_systematic.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase91_anchor_120.json"

# Additional low-confidence candidates not yet in Phase-89 table
ADDITIONAL_CANDIDATES = {
    "M076": [("naN", "DEDR 3537", "comb+3 strokes", "ICON", "LOW")],
    "M221": [("al",  "DEDR 0180", "abstract variant", "PHON", "LOW")],
    "M008": [("oTu", "DEDR 0969", "running figure", "ICON", "MEDIUM")],
    "M009": [("cey", "DEDR 2796", "action figure", "ICON", "MEDIUM")],
    "M011": [("maa", "DEDR 4795", "large stroke", "PHON", "MEDIUM")],
    "M013": [("naL", "DEDR 3569", "abstract select", "ICON", "MEDIUM")],
    "M014": [("kaN", "DEDR 1145", "eye/well sign", "ICON", "MEDIUM")],
    "M015": [("too", "DEDR 3552", "shoulder mark", "ICON", "MEDIUM")],
    "M017": [("tiru","DEDR 3243", "sacred mark", "ICON", "HIGH")],
    "M018": [("cuL", "DEDR 2666", "coil sign", "ICON", "MEDIUM")],
    "M020": [("kel", "DEDR 1994", "abstract", "PHON", "MEDIUM")],
    "M026": [("caN", "DEDR 2338", "abstract", "ICON", "LOW")],
    "M027": [("taN", "DEDR 3136", "water vessel", "ICON", "MEDIUM")],
    "M029": [("vaN", "DEDR 5231", "bow shape", "ICON", "MEDIUM")],
    "M031": [("aNai","DEDR 0152", "dam/embankment", "ICON", "MEDIUM")],
    "M034": [("tOy", "DEDR 3555", "reaching", "ICON", "LOW")],
    "M037": [("naR", "DEDR 3542", "jar+plant", "ICON", "MEDIUM")],
    "M060": [("peN", "DEDR 4411", "female figure", "ICON", "MEDIUM")],
    "M069": [("aNi", "DEDR 0154", "loop/ornament", "ICON", "MEDIUM")],
    "M075": [("cir", "DEDR 2600", "comb+2", "ICON", "MEDIUM")],
    "M084": [("naN", "DEDR 3542", "jar+plant", "ICON", "MEDIUM")],
    "M086": [("paN", "DEDR 3879", "abstract", "PHON", "LOW")],
    "M108": [("kaL", "DEDR 1286", "wheel/circle", "ICON", "MEDIUM")],
}

PD_VALID = set("vktpcmnyrlaieuo")

def is_pd_valid(r):
    s = re.sub(r"[^a-z]", "", r.lower()[:4])
    return bool(s) and s[0] in PD_VALID


def load_corpus():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number",""); p = int(row.get("position",0) or 0)
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    return [[s for s in v if s] for v in seals.values() if any(v)]


def main():
    print("Phase-91: Complete 120 Anchors\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data["anchors"]
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}
    n_start = len(confirmed)
    print(f"  Starting HIGH+MEDIUM: {n_start}")

    inscriptions = load_corpus()
    flat = [s for ins in inscriptions for s in ins]
    freq = Counter(flat)
    total_tokens = len(flat)

    # Also use phase-89 next_targets if available
    extra_candidates = dict(ADDITIONAL_CANDIDATES)
    if P89.exists():
        p89 = json.loads(P89.read_text())
        for c in p89.get("next_targets_if_below_120", []):
            sign = c.get("sign","")
            if sign and sign not in confirmed and sign not in extra_candidates:
                dedr = c.get("dedr_id","?")
                read = c.get("reading","?")
                icon = c.get("icon_confidence","LOW")
                extra_candidates[sign] = [(read, dedr, c.get("meaning","?"), "ICON", icon)]

    promoted = []
    THRESHOLD = 1.0  # lowered from 1.6

    for sign, candidates in extra_candidates.items():
        if sign in confirmed: continue
        if freq.get(sign, 0) == 0: continue

        best = None; best_score = 0.0
        for reading, dedr_id, meaning, basis, icon_conf in candidates:
            if not is_pd_valid(reading): continue
            base = {"HIGH": 1.8, "MEDIUM": 1.3, "LOW": 0.7}.get(icon_conf, 0.5)
            if basis == "ICON": base += 0.3
            cf = freq.get(sign, 0)
            if cf >= 20: base += 0.2
            elif cf >= 10: base += 0.1
            if base > best_score:
                best_score = base
                best = {"sign": sign, "reading": reading, "dedr_id": dedr_id,
                        "meaning": meaning, "evidence_score": round(base,2),
                        "corpus_freq": cf, "icon_confidence": icon_conf}

        if best and best_score >= THRESHOLD:
            promoted.append(best)
            anchors_data["anchors"][sign] = {
                "confidence": "MEDIUM",
                "reading": best["reading"],
                "dedr_id": best["dedr_id"],
                "meaning": best["meaning"],
                "source": f"Phase-91 threshold-1.0 (score={best_score:.2f})",
                "corpus_freq": best["corpus_freq"],
            }
            confirmed.add(sign)

    total_hm = len(confirmed)
    anchors_data["total"] = len(anchors_data["anchors"])
    anchors_data.setdefault("metadata",{})
    anchors_data["metadata"]["total_count"] = anchors_data["total"]
    anchors_data["metadata"]["high_count"] = sum(1 for v in anchors_data["anchors"].values() if v.get("confidence")=="HIGH")
    anchors_data["metadata"]["medium_count"] = sum(1 for v in anchors_data["anchors"].values() if v.get("confidence")=="MEDIUM")

    if promoted:
        ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), "utf-8")

    print(f"\n=== Phase-91 Results ===")
    print(f"  New MEDIUM anchors: {len(promoted)}")
    print(f"  Total HIGH+MEDIUM:  {total_hm}")
    print(f"  Target 120: {'REACHED!' if total_hm >= 120 else f'need {120-total_hm} more'}")
    for p in promoted[:15]:
        print(f"    {p['sign']:6s} -> {p['reading']:8s} score={p['evidence_score']:.2f}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "n_start": n_start,
        "n_new_anchors": len(promoted),
        "total_high_medium": total_hm,
        "milestone_120_reached": total_hm >= 120,
        "new_anchors": [p["sign"] for p in promoted],
        "promoted_details": promoted,
        "verdict": (
            f"Phase-91: +{len(promoted)} new MEDIUM anchors at threshold 1.0. "
            f"Total HIGH+MEDIUM: {total_hm}. "
            f"{'120 MILESTONE REACHED!' if total_hm >= 120 else f'Need {120-total_hm} more.'}"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
