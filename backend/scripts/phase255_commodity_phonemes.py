"""Phase-255: Trade Commodity Phoneme Mapping

Ceiling-breaker experiment #3 from Phase-249 queue (C2b).

Strategy: Map known Harappan trade commodities to Proto-Dravidian names,
then cross-reference MEDIUM signs appearing on zebu/bull/trade seals.
Signs whose reading matches a commodity PDr name AND appear on commodity
seals get additional corroboration → MEDIUM→HIGH upgrade candidates.

Known IVC exports (archaeological evidence):
  carnelian, agate, lapis lazuli, cotton, ivory, copper, tin,
  shells, timber, sesame, barley, dried fish, textiles

Output: outputs/phase255_commodity_phonemes.json
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase255_commodity_phonemes.json"
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_CSV = REPO / "corpora" / "downloads" / "external_repos" / "holdatllc_indus" / "indus_corpus 2.csv"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "data"))

# ── Known IVC trade commodities → PDr names ─────────────────────────────────
# Sources: Parpola 1994, Kenoyer 1998, Possehl 2002, DEDR
COMMODITY_MAP = [
    {"commodity": "carnelian",    "pdr": "cēṭi",   "dedr": "2806", "phonemes": ["cē", "ṭi"],
     "notes": "Red stone bead — major Harappan export to Mesopotamia"},
    {"commodity": "agate",        "pdr": "akatti",  "dedr": "7",    "phonemes": ["a", "ka", "tti"],
     "notes": "Layered chalcedony — Gujarat workshops (Lothal, Dholavira)"},
    {"commodity": "lapis lazuli", "pdr": "nīlam",   "dedr": "3675", "phonemes": ["nī", "lam"],
     "notes": "Imported from Afghanistan via Shortughai; re-exported to Mesopotamia"},
    {"commodity": "cotton",       "pdr": "parutti",  "dedr": "3986", "phonemes": ["pa", "ru", "tti"],
     "notes": "Gossypium arboreum — earliest known cotton textiles (Mohenjo-daro)"},
    {"commodity": "ivory",        "pdr": "kōṭu",    "dedr": "2071", "phonemes": ["kō", "ṭu"],
     "notes": "Elephant ivory — combs, ornaments, seals. PDr kōṭu = tusk/horn"},
    {"commodity": "copper",       "pdr": "cempu",    "dedr": "2781", "phonemes": ["ce", "mpu"],
     "notes": "From Khetri (Rajasthan). PDr cempu = copper (DEDR 2781)"},
    {"commodity": "tin",          "pdr": "kaḷimpu",  "dedr": "1313", "phonemes": ["ka", "ḷi", "mpu"],
     "notes": "Imported for bronze alloying. PDr kaḷimpu (DEDR 1313)"},
    {"commodity": "shell",        "pdr": "ciṉṉi",   "dedr": "2519", "phonemes": ["ci", "ṉṉi"],
     "notes": "Conch/turbinella — Gujarat coast. Bangles, ladles, inlay"},
    {"commodity": "sesame",       "pdr": "eḷḷu",    "dedr": "839",  "phonemes": ["e", "ḷḷu"],
     "notes": "Sesamum indicum — oil crop. PDr eḷḷu = sesame (DEDR 839)"},
    {"commodity": "barley",       "pdr": "yavam",    "dedr": "5151", "phonemes": ["ya", "vam"],
     "notes": "Hordeum vulgare — primary grain crop at IVC sites"},
    {"commodity": "dried fish",   "pdr": "kaṟuvāṭu", "dedr": "1278", "phonemes": ["ka", "ṟu", "vā", "ṭu"],
     "notes": "Coastal export. PDr kaṟuvāṭu = dried fish (DEDR 1278)"},
    {"commodity": "gold",         "pdr": "poṉ",     "dedr": "4570", "phonemes": ["poṉ"],
     "notes": "From Karnataka/Kolar. PDr poṉ = gold (DEDR 4570)"},
    {"commodity": "timber",       "pdr": "maram",    "dedr": "4711", "phonemes": ["ma", "ram"],
     "notes": "Teak, sissoo — exported to timber-poor Mesopotamia"},
    {"commodity": "honey",        "pdr": "tēṉ",     "dedr": "3455", "phonemes": ["tēṉ"],
     "notes": "Wild honey. PDr tēṉ = honey (DEDR 3455)"},
    {"commodity": "weight/measure", "pdr": "pala",   "dedr": "3987", "phonemes": ["pa", "la"],
     "notes": "Standard weight unit. PDr pala = weight (DEDR 3987)"},
    {"commodity": "stone standard", "pdr": "kal",    "dedr": "1298", "phonemes": ["kal"],
     "notes": "Weight stone. PDr kal = stone (DEDR 1298)"},
]


def norm_icon(s: str) -> str:
    s = s.strip().lower() if s and s != "nan" else ""
    if not s:
        return "none"
    for kw in ["unicorn", "rhinoceros", "elephant", "buffalo", "tiger",
               "zebu", "bull", "gharial", "bison"]:
        if kw in s:
            return "zebu" if kw in ("bull", "buffalo", "bison") else kw
    return "other"


def load_holdat_with_motif() -> list[dict]:
    seals = []
    with open(HOLDAT_CSV, encoding="utf-8") as fh:
        hdr = fh.readline().strip().split(",")
        ci = {h.strip(): i for i, h in enumerate(hdr)}
        cur_form, cur_signs, cur_site, cur_icon = None, [], "", ""
        for line in fh:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            form = parts[ci.get("form", 0)].strip()
            sign = parts[ci.get("letters", 1)].strip()
            site = parts[ci.get("site", 2)].strip() if "site" in ci else ""
            icon = (parts[ci.get("iconography", 3)].strip()
                    if "iconography" in ci and ci.get("iconography", 3) < len(parts) else "")
            if form != cur_form:
                if cur_form and cur_signs:
                    seals.append({"form": cur_form, "signs": list(cur_signs),
                                  "motif": norm_icon(cur_icon), "site": cur_site})
                cur_form, cur_signs, cur_site, cur_icon = form, [], site, icon
            cur_signs.append(sign)
        if cur_form and cur_signs:
            seals.append({"form": cur_form, "signs": list(cur_signs),
                          "motif": norm_icon(cur_icon), "site": cur_site})
    return seals


def reading_matches_commodity(reading: str, commodity_phonemes: list[list[str]]) -> list[dict]:
    """Check if a sign reading matches any commodity phoneme pattern."""
    if not reading:
        return []
    r = reading.lower().split("/")[0].split("(")[0].strip()
    matches = []
    for cm in COMMODITY_MAP:
        for ph in cm["phonemes"]:
            if ph.lower() in r or r in ph.lower():
                matches.append({"commodity": cm["commodity"], "pdr": cm["pdr"],
                                "dedr": cm["dedr"], "matched_phoneme": ph})
                break
    return matches


def main():
    print("=" * 70)
    print("PHASE-255: TRADE COMMODITY PHONEME MAPPING")
    print("=" * 70)

    anchors_raw = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_raw.get("anchors", {})
    seals = load_holdat_with_motif()

    # Trade seals = zebu/bull motif
    trade_seals = [s for s in seals if s["motif"] == "zebu"]
    print(f"\n  Total seals: {len(seals)}")
    print(f"  Trade (zebu/bull) seals: {len(trade_seals)}")

    medium_signs = {k: v for k, v in anchors.items() if v.get("confidence") == "MEDIUM"}
    print(f"  MEDIUM signs: {len(medium_signs)}")

    # Signs appearing on trade seals
    trade_sign_freq: Counter = Counter()
    for seal in trade_seals:
        for sign in seal["signs"]:
            s = f"M{sign}" if not sign.startswith("M") else sign
            trade_sign_freq[s] += 1

    # ── Step 1: MEDIUM signs on trade seals with commodity reading match ─────
    print("\n" + "─" * 70)
    print("STEP 1: MEDIUM SIGNS × COMMODITY PHONEME MATCHING")
    print("─" * 70)

    commodity_matches = []
    for sign, info in medium_signs.items():
        reading = info.get("reading", "")
        trade_count = trade_sign_freq.get(sign, 0)
        matches = reading_matches_commodity(reading, [cm["phonemes"] for cm in COMMODITY_MAP])
        if matches:
            commodity_matches.append({
                "sign": sign, "reading": reading, "trade_seal_count": trade_count,
                "total_freq": sum(1 for s in seals for sg in s["signs"]
                                  if (f"M{sg}" if not sg.startswith("M") else sg) == sign),
                "commodity_matches": matches,
                "n_commodities": len(matches),
            })

    commodity_matches.sort(key=lambda x: (-x["n_commodities"], -x["trade_seal_count"]))
    print(f"\n  MEDIUM signs matching commodity phonemes: {len(commodity_matches)}")
    print(f"\n  {'Sign':<8} {'Reading':<14} {'Trade#':>6} {'Total#':>6} Commodity matches")
    for cm in commodity_matches[:20]:
        cnames = ", ".join(f"{m['commodity']}({m['pdr']})" for m in cm["commodity_matches"])
        print(f"  {cm['sign']:<8} {cm['reading'][:13]:<14} {cm['trade_seal_count']:>6} "
              f"{cm['total_freq']:>6} {cnames[:60]}")

    # ── Step 2: Upgrade candidates ──────────────────────────────────────────
    # Require: trade_seal_count >= 3 AND at least 1 commodity match
    print("\n" + "─" * 70)
    print("STEP 2: COMMODITY-CORROBORATED MEDIUM→HIGH UPGRADE CANDIDATES")
    print("─" * 70)

    upgrade_candidates = [cm for cm in commodity_matches
                          if cm["trade_seal_count"] >= 3 and cm["n_commodities"] >= 1]
    print(f"\n  Upgrade candidates (trade≥3, commodity match): {len(upgrade_candidates)}")

    n_upgraded = 0
    upgrade_log = []
    for uc in upgrade_candidates:
        sign = uc["sign"]
        if anchors[sign].get("confidence") != "MEDIUM":
            continue
        best_match = uc["commodity_matches"][0]
        anchors[sign]["confidence"] = "HIGH"
        anchors[sign]["phase_upgraded"] = 255
        anchors[sign]["commodity_corroboration"] = {
            "commodity": best_match["commodity"],
            "pdr": best_match["pdr"],
            "dedr": best_match["dedr"],
            "trade_seal_count": uc["trade_seal_count"],
        }
        basis = anchors[sign].get("basis", "")
        anchors[sign]["basis"] = (
            f"{basis}; Phase-255: commodity phoneme corroboration — "
            f"matches PDr '{best_match['pdr']}'={best_match['commodity']} (DEDR {best_match['dedr']}), "
            f"appears on {uc['trade_seal_count']} trade/zebu seals"
        )
        n_upgraded += 1
        upgrade_log.append({
            "sign": sign, "reading": uc["reading"],
            "commodity": best_match["commodity"], "pdr": best_match["pdr"],
            "dedr": best_match["dedr"], "trade_seal_count": uc["trade_seal_count"],
            "upgrade": "MEDIUM→HIGH",
        })
        print(f"  ↑ {sign}='{uc['reading']}': MEDIUM → HIGH "
              f"({best_match['commodity']}={best_match['pdr']}, {uc['trade_seal_count']} trade seals)")

    # Save if upgrades applied
    if n_upgraded > 0:
        anchors_raw["anchors"] = anchors
        ANCHORS.write_text(json.dumps(anchors_raw, indent=2, ensure_ascii=False), encoding="utf-8")

    by_conf = Counter(v.get("confidence", "?") for v in anchors.values())
    n_hm = by_conf.get("HIGH", 0) + by_conf.get("MEDIUM", 0)
    print(f"\n  Final state: H:{by_conf.get('HIGH',0)} M:{by_conf.get('MEDIUM',0)} "
          f"CANDIDATE:{by_conf.get('CANDIDATE',0)} → H+M={n_hm}/{len(anchors)}")

    result = {
        "phase": 255,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_trade_seals": len(trade_seals),
        "n_medium_analysed": len(medium_signs),
        "n_commodity_matches": len(commodity_matches),
        "n_upgrade_candidates": len(upgrade_candidates),
        "n_upgraded": n_upgraded,
        "upgrade_log": upgrade_log,
        "commodity_matches": commodity_matches[:30],
        "commodity_map_used": [{"commodity": c["commodity"], "pdr": c["pdr"], "dedr": c["dedr"]}
                               for c in COMMODITY_MAP],
        "final_state": {"HIGH": by_conf.get("HIGH", 0), "MEDIUM": by_conf.get("MEDIUM", 0),
                        "CANDIDATE": by_conf.get("CANDIDATE", 0), "H_plus_M": n_hm, "total": len(anchors)},
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Output: {OUT}")
    print(f"\n{'=' * 70}")
    print(f"PHASE-255 COMPLETE: {n_upgraded} MEDIUM→HIGH upgrades")
    print(f"{'=' * 70}")
    return result


if __name__ == "__main__":
    main()
