"""Phase-110: Targeted SA Sprint — UNKNOWN-tier signs (freq >= 5).

Runs a fresh 10-seed SA with all 130 H+M anchors pinned, specifically
targeting the 47 signs that Phase-73 missed (ENSEMBLE_TIER=UNKNOWN).
Uses the Dravidian syllabic LM. GPU if available.

Output: reports/phase110_targeted_sa_unknown.json
Also updates backend/reports/INDUS_FINAL_ANCHORS.json
"""
from __future__ import annotations

import csv
import json
import os
import sys
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P73     = REPO / "reports/phase73_ensemble_calibration.json"
P108    = REPO / "reports/phase108_phon_exhaustion.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase110_targeted_sa_unknown.json"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

N_SEEDS   = 10
MIN_FREQ  = 5
CONS_MIN  = 0.40   # minimum consistency to accept

PD_VALID_INITIALS = {
    "a","ā","i","ī","u","ū","e","ē","o","ō",
    "k","ka","ki","ku","ko","kā","kō","kē",
    "c","ca","ci","cu","co",
    "t","ta","ti","tu","to","tā",
    "n","na","ni","nu","nē",
    "p","pa","pi","pu","po","pā",
    "m","ma","mi","mu",
    "v","va","vi",
    "y","ya","r","ra","l","la",
    "ay","an","am","al","ar","ir","il","in",
}

DEDR_QUICK = {
    "vel":("5469","spear/victory"), "pon":("4533","gold"), "nal":("3569","good"),
    "van":("5231","strong"), "kan":("1145","eye/lord"), "per":("4442","great"),
    "tan":("3136","self/cool"), "ko":("1570","king"), "ka":("1145","eye"),
    "mu":("5012","face"), "pu":("4317","flower"), "tu":("3385","pierce"),
    "ma":("4751","great"), "na":("3549","word"), "va":("5231","strong"),
    "cu":("2732","small"), "nē":("3741","true"), "ay":("0206","noble"),
    "an":("0149","man"), "am":("0200","beautiful"), "ar":("0359","great"),
    "ir":("0488","two"), "il":("0486","house"),
}


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


def is_pd_valid(reading: str) -> bool:
    if not reading:
        return False
    r = reading.lower().strip()
    for init in sorted(PD_VALID_INITIALS, key=len, reverse=True):
        if r.startswith(init):
            return True
    return False


def main():
    print("Phase-110: Targeted SA Sprint — UNKNOWN-tier Signs\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}
    anchor_map = {s: v["reading"] for s, v in anchors.items()
                  if v.get("confidence") in ("HIGH", "MEDIUM") and v.get("reading")}
    print(f"  Pinned anchors: {len(anchor_map)}")

    # Load Phase-73 map
    p73_map = {}
    if P73.exists():
        for entry in json.loads(P73.read_text()).get("calibrated_table", []):
            p73_map[entry["sign"]] = entry

    # Load Phase-108 sweep log to find the UNKNOWN signs
    unknown_targets = []
    if P108.exists():
        p108 = json.loads(P108.read_text())
        for entry in p108.get("sweep_log", []):
            if entry.get("skipped") and entry.get("freq", 0) >= MIN_FREQ:
                unknown_targets.append((entry["sign"], entry["freq"]))
    if not unknown_targets:
        # Fallback: compute from corpus directly
        seals = load_corpus()
        flat_freq = Counter(s for signs in seals.values() for s in signs)
        unknown_targets = [
            (s, f) for s, f in flat_freq.items()
            if s not in confirmed and f >= MIN_FREQ
        ]
    unknown_targets.sort(key=lambda x: -x[1])
    print(f"  UNKNOWN-tier targets: {len(unknown_targets)}")

    # Load corpus
    seals = load_corpus()
    flat = [s for signs in seals.values() for s in signs]
    print(f"  Corpus: {len(seals)} seals, {len(flat)} tokens")

    # Build Dravidian LM
    lm = None
    try:
        from glossa_lab.data.dravidian import get_word_symbols  # noqa: PLC0415
        from glossa_lab.pipelines.decipher import LanguageModel  # noqa: PLC0415
        lm = LanguageModel(get_word_symbols())
        print(f"  LM: Dravidian, {lm.size} signs")
    except Exception as exc:  # noqa: BLE001
        print(f"  [WARN] LM unavailable: {exc}")

    results = []
    n_promoted = 0

    for sign, freq in unknown_targets:
        if sign in confirmed:
            continue

        # Run SA with all anchors pinned
        if lm:
            try:
                from glossa_lab.experiments._parallel import run_seeds_parallel  # noqa: PLC0415
                from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415

                def _one(seed: int, a=anchor_map, f=flat) -> dict:
                    r = decipher(f, lm, seed=seed, max_iterations=8000, restarts=5,
                                 cipher_inscriptions=None, surjective=True,
                                 ocp_weight=0.0, positional_weight=0.0, anchors=a)
                    return r.get("proposed_mapping", {})

                maps = run_seeds_parallel(_one, list(range(N_SEEDS)))
                proposals = [m.get(sign) for m in maps if m.get(sign)]
                if proposals:
                    cnt = Counter(proposals)
                    modal, mc = cnt.most_common(1)[0]
                    cons = mc / len(proposals)
                    pd_ok = is_pd_valid(modal)
                    dedr_num, dedr_gloss = DEDR_QUICK.get(modal.lower(), ("", ""))
                    entry = {
                        "sign": sign, "freq": freq,
                        "sa_modal": modal, "consistency": round(cons, 3),
                        "pd_valid": pd_ok, "n_seeds": len(proposals),
                        "dedr": dedr_num, "dedr_gloss": dedr_gloss,
                    }
                    results.append(entry)
                    print(f"  {sign} (f={freq}): '{modal}' (cons={cons:.2f}, PD={pd_ok})", end="")
                    if pd_ok and cons >= CONS_MIN:
                        anchors[sign] = {
                            "reading": modal,
                            "confidence": "MEDIUM",
                            "basis": (f"Phase-110 targeted SA: modal='{modal}', "
                                      f"consistency={cons:.2f}, {N_SEEDS} seeds, "
                                      f"130 anchors pinned. DEDR {dedr_num}: {dedr_gloss}. freq={freq}."),
                            "source": "Phase-110",
                        }
                        n_promoted += 1
                        print(" → MEDIUM ✓")
                    else:
                        print()
                else:
                    results.append({"sign": sign, "freq": freq, "sa_modal": "", "consistency": 0,
                                    "pd_valid": False, "error": "no proposals"})
            except Exception as exc:  # noqa: BLE001
                results.append({"sign": sign, "freq": freq, "error": str(exc)})
        else:
            results.append({"sign": sign, "freq": freq, "sa_modal": "", "consistency": 0,
                             "pd_valid": False, "error": "no LM"})

    # Save anchors
    anchors_data["anchors"] = anchors
    anchors_data["total"] = len(anchors)
    ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")

    n_after = len({s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")})
    flat_freq_all = Counter(s for signs in seals.values() for s in signs)
    total_tokens = sum(flat_freq_all.values())
    covered = sum(flat_freq_all.get(s, 0) for s in anchors
                  if anchors[s].get("confidence") in ("HIGH", "MEDIUM"))
    cov = round(covered / max(1, total_tokens), 4)

    print(f"\n  Promoted: {n_promoted} new MEDIUM signs")
    print(f"  Total H+M anchors: {n_after}")
    print(f"  Token coverage: {cov:.1%}")

    result = {
        "phase": 110,
        "n_unknown_targets": len(unknown_targets),
        "n_promoted": n_promoted,
        "n_after": n_after,
        "token_coverage": cov,
        "results": results,
        "promoted_signs": [r["sign"] for r in results
                           if r.get("pd_valid") and r.get("consistency", 0) >= CONS_MIN],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
