"""Phase-262: Collocate-Based MEDIUM→HIGH Batch Upgrade

Signs that always co-occur with HIGH signs in fixed bigrams have constrained
reading spaces. If a MEDIUM sign appears in a bigram with a HIGH sign at
least N times AND that bigram accounts for ≥50% of the MEDIUM sign's total
occurrences, the MEDIUM sign gets upgraded to HIGH.

Logic: if M_unknown always appears next to M342=ay (HIGH), it must be a
grammatically compatible element — the HIGH anchor constrains its function.

Uses the Holdat corpus directly (no SA needed).

Output: outputs/phase262_collocate_upgrade.json
"""
from __future__ import annotations

import json, os, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase262_collocate_upgrade.json"
ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "data"))


def main():
    print("=" * 70)
    print("PHASE-262: COLLOCATE-BASED MEDIUM→HIGH BATCH UPGRADE")
    print("=" * 70)

    from glossa_lab.data.indus_m77 import get_corpus_inscriptions
    inscs = get_corpus_inscriptions(min_length=2)

    anchors_raw = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_raw["anchors"]

    high_m77 = set()
    medium_m77 = {}
    for k, v in anchors.items():
        m77 = k.lstrip("M")
        if v.get("confidence") == "HIGH":
            high_m77.add(m77)
        elif v.get("confidence") == "MEDIUM":
            medium_m77[m77] = k  # m77 → anchor key

    print(f"\n  Inscriptions (len≥2): {len(inscs)}")
    print(f"  HIGH signs in M77: {len(high_m77)}")
    print(f"  MEDIUM signs in M77: {len(medium_m77)}")

    # Count bigrams involving MEDIUM signs
    # For each MEDIUM sign, track how often it appears next to each HIGH sign
    med_high_bigrams: dict[str, Counter] = defaultdict(Counter)  # med_m77 → {high_m77: count}
    med_total: Counter = Counter()

    for seq in inscs:
        for i in range(len(seq) - 1):
            a, b = seq[i], seq[i + 1]
            # Check a=MEDIUM, b=HIGH
            if a in medium_m77 and b in high_m77:
                med_high_bigrams[a][b] += 1
            # Check a=HIGH, b=MEDIUM
            if a in high_m77 and b in medium_m77:
                med_high_bigrams[b][a] += 1
        for s in seq:
            if s in medium_m77:
                med_total[s] += 1

    # Upgrade criteria:
    # 1. MEDIUM sign has ≥3 bigram occurrences with HIGH signs
    # 2. Sum of HIGH-bigram counts ≥ 50% of MEDIUM sign's total occurrences
    # 3. MEDIUM sign has a DEDR entry
    MIN_BIGRAM_COUNT = 3
    MIN_HIGH_RATIO = 0.50

    upgrade_candidates = []
    for med_m77_id, high_counts in med_high_bigrams.items():
        total_high_bigrams = sum(high_counts.values())
        total_occ = med_total.get(med_m77_id, 0)
        if total_occ == 0:
            continue
        high_ratio = total_high_bigrams / total_occ
        anchor_key = medium_m77[med_m77_id]
        has_dedr = bool(anchors[anchor_key].get("dedr", ""))

        if total_high_bigrams >= MIN_BIGRAM_COUNT and high_ratio >= MIN_HIGH_RATIO:
            top_partner = high_counts.most_common(1)[0]
            partner_key = f"M{top_partner[0]}"
            partner_reading = anchors.get(partner_key, {}).get("reading", "?")
            upgrade_candidates.append({
                "sign": anchor_key,
                "m77": med_m77_id,
                "reading": anchors[anchor_key].get("reading", ""),
                "total_occ": total_occ,
                "high_bigram_count": total_high_bigrams,
                "high_ratio": round(high_ratio, 3),
                "top_partner": partner_key,
                "top_partner_reading": partner_reading,
                "top_partner_count": top_partner[1],
                "n_high_partners": len(high_counts),
                "has_dedr": has_dedr,
            })

    upgrade_candidates.sort(key=lambda x: (-x["high_ratio"], -x["high_bigram_count"]))

    print(f"\n  Upgrade candidates (bigram≥{MIN_BIGRAM_COUNT}, ratio≥{MIN_HIGH_RATIO:.0%}): "
          f"{len(upgrade_candidates)}")
    print(f"\n  {'Sign':<8} {'Reading':<14} {'Occ':>4} {'H-big':>5} {'Ratio':>6} "
          f"{'TopPartner':<12} {'DEDR':>5}")
    for uc in upgrade_candidates[:20]:
        print(f"  {uc['sign']:<8} {uc['reading'][:13]:<14} {uc['total_occ']:>4} "
              f"{uc['high_bigram_count']:>5} {uc['high_ratio']:>5.0%} "
              f"{uc['top_partner']+'='+uc['top_partner_reading'][:6]:<12} "
              f"{'✓' if uc['has_dedr'] else '✗':>5}")

    # Apply upgrades
    n_upgraded = 0
    upgrade_log = []
    for uc in upgrade_candidates:
        sign = uc["sign"]
        if anchors[sign].get("confidence") != "MEDIUM":
            continue
        # Require DEDR for upgrade
        if not uc["has_dedr"]:
            continue

        anchors[sign]["confidence"] = "HIGH"
        anchors[sign]["phase_upgraded"] = 262
        basis = anchors[sign].get("basis", "")
        anchors[sign]["basis"] = (
            f"{basis}; Phase-262: collocate upgrade — "
            f"{uc['high_bigram_count']} bigrams with HIGH signs "
            f"({uc['high_ratio']:.0%} of occurrences), "
            f"top partner {uc['top_partner']}='{uc['top_partner_reading']}'"
        )
        n_upgraded += 1
        upgrade_log.append(uc)
        print(f"  ↑ {sign}='{uc['reading']}': MEDIUM → HIGH "
              f"({uc['high_bigram_count']} HIGH bigrams, {uc['high_ratio']:.0%})")

    if n_upgraded > 0:
        anchors_raw["anchors"] = anchors
        ANCHORS.write_text(json.dumps(anchors_raw, indent=2, ensure_ascii=False), encoding="utf-8")

    by_conf = Counter(v.get("confidence", "?") for v in anchors.values())
    n_hm = by_conf.get("HIGH", 0) + by_conf.get("MEDIUM", 0)

    print(f"\n  Final state: H:{by_conf.get('HIGH',0)} M:{by_conf.get('MEDIUM',0)} "
          f"→ H+M={n_hm}/{len(anchors)}")

    result = {
        "phase": 262, "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_upgrade_candidates": len(upgrade_candidates),
        "n_upgraded": n_upgraded, "upgrade_log": upgrade_log[:50],
        "all_candidates": upgrade_candidates[:30],
        "final_state": {"HIGH": by_conf.get("HIGH", 0), "MEDIUM": by_conf.get("MEDIUM", 0),
                        "H_plus_M": n_hm, "total": len(anchors)},
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{'='*70}")
    print(f"PHASE-262 COMPLETE: {n_upgraded} MEDIUM→HIGH upgrades via collocate analysis")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
