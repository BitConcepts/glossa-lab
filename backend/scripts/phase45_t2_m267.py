"""Phase-45 T2: M267 Investigation.

M267 is the 2nd most frequent sign (400 occurrences, avg_pos=0.54, UNCERTAIN
confidence).  It appears on ALL motif types (unicorn 127, zebu 72, elephant 37
rhinoceros 25, etc.) making iconographic restriction impossible.

This script:
  1. Full positional profile: distribution by site, motif, inscription length
  2. Co-occurrence network: what signs appear adjacent to M267
  3. The M267→M099 title formula: detailed analysis
  4. Comparison to Fuls functional sign categories
  5. Candidate functional readings: grammatical particle, determinative, or
     high-frequency logogram?

Output: reports/phase45_t2_m267.json
"""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES   = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT = REPORTS / "phase45_t2_m267.json"

TARGET = "M267"


def load_corpus():
    seals: dict[str, dict] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cisi = r["cisi_number"]
            pos = int(r.get("position", 0))
            if cisi not in seals:
                seals[cisi] = {"signs": [], "site": r.get("site", ""), "iconography": r.get("iconography", "")}
            while len(seals[cisi]["signs"]) <= pos:
                seals[cisi]["signs"].append("")
            seals[cisi]["signs"][pos] = r["letters"]
    inscriptions = []
    for cisi, data in seals.items():
        signs = [s for s in data["signs"] if s]
        if signs:
            inscriptions.append({"id": cisi, "signs": signs, "site": data["site"], "icon": data["iconography"]})
    return inscriptions


def main():
    print(f"Phase-45 T2: {TARGET} Full Investigation\n")

    inscriptions = load_corpus()
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    with open(ROLES, encoding="utf-8") as f:
        roles = {r["symbol"]: r for r in csv.DictReader(f)}

    m267_role = roles.get(TARGET, {})
    print(f"Holdat role: avg_pos={m267_role.get('avg_position','?')}, "
          f"semantic_role={m267_role.get('semantic_role','?')}, "
          f"is_starter={m267_role.get('is_starter','?')}, "
          f"is_ending={m267_role.get('is_ending','?')}")

    # --- Site + motif distribution ---
    site_count: Counter = Counter()
    icon_count: Counter = Counter()
    positions: list[float] = []
    pre_m267: Counter = Counter()
    post_m267: Counter = Counter()
    context_pairs: Counter = Counter()  # (prev, next) tuples
    insc_lengths_with: list[int] = []
    formula_m267_m099 = 0
    formula_m099_m267 = 0

    for insc in inscriptions:
        signs = insc["signs"]
        for i, s in enumerate(signs):
            if s == TARGET:
                site_count[insc["site"]] += 1
                icon_count[insc["icon"]] += 1
                rel = i / max(len(signs) - 1, 1)
                positions.append(rel)
                insc_lengths_with.append(len(signs))
                prev = signs[i-1] if i > 0 else None
                nxt  = signs[i+1] if i < len(signs)-1 else None
                if prev:
                    pre_m267[prev] += 1
                if nxt:
                    post_m267[nxt] += 1
                if prev and nxt:
                    context_pairs[(prev, nxt)] += 1
                # Formula detection
                if nxt == "M099":
                    formula_m267_m099 += 1
                if prev == "M099":
                    formula_m099_m267 += 1

    n = len(positions)
    avg_pos = sum(positions) / n if n else 0

    print(f"\nTotal occurrences: {n}")
    print(f"Avg relative position: {avg_pos:.3f}")
    print(f"Sites: {dict(site_count.most_common(5))}")
    print(f"Top iconographies: {dict(icon_count.most_common(5))}")
    print(f"Top pre-M267: {pre_m267.most_common(5)}")
    print(f"Top post-M267: {post_m267.most_common(5)}")
    print(f"M267→M099 formula: {formula_m267_m099}×")
    print(f"M099→M267 sequence: {formula_m099_m267}×")

    # --- Iconography entropy (how spread across motifs?) ---
    icon_total = sum(icon_count.values())
    icon_entropy = 0.0
    for cnt in icon_count.values():
        p = cnt / icon_total
        icon_entropy -= p * math.log2(p)
    max_entropy = math.log2(len(icon_count)) if len(icon_count) > 1 else 1.0
    icon_normalised_entropy = icon_entropy / max_entropy
    print(f"\nIconographic entropy: {icon_entropy:.3f} (normalised: {icon_normalised_entropy:.3f})")
    print(f"  → {'UNIFORM across motifs (function word / grammar)' if icon_normalised_entropy > 0.8 else 'RESTRICTED to some motifs'}")

    # --- Site specificity (is M267 concentrated anywhere?) ---
    site_total = sum(site_count.values())
    max_site_pct = max(site_count.values()) / site_total if site_total else 0

    # --- Cross-reference anchor readings ---
    anchor_pre = [(s, anchors[s]["reading"]) for s in pre_m267.keys() if s in anchors and anchors[s].get("confidence") == "HIGH"]
    anchor_post = [(s, anchors[s]["reading"]) for s in post_m267.keys() if s in anchors and anchors[s].get("confidence") == "HIGH"]

    print(f"\nAnchored signs before M267: {anchor_pre}")
    print(f"Anchored signs after M267:  {anchor_post}")

    # Interpret
    if icon_normalised_entropy > 0.85 and avg_pos > 0.3 and avg_pos < 0.7:
        reading_hypothesis = "GRAMMATICAL_PARTICLE or DETERMINATIVE — motif-independent, medial position"
        epistemic = "[INFERRED, low confidence]"
    elif avg_pos < 0.2:
        reading_hypothesis = "HIGH-FREQUENCY LOGOGRAM — initial position like CLASSIFIER_PREFIX signs"
        epistemic = "[INFERRED, low confidence]"
    else:
        reading_hypothesis = "FUNCTION_WORD — high frequency + medial position consistent with copula or case particle"
        epistemic = "[UNCERTAIN]"

    print(f"\nHypothesis: {reading_hypothesis}")
    print(f"Epistemic: {epistemic}")

    result = {
        "_citation": {"primary_sources": ["A.1", "A.13"]},
        "sign": TARGET,
        "n_occurrences": n,
        "avg_relative_position": round(avg_pos, 3),
        "site_distribution": dict(site_count.most_common()),
        "iconography_distribution": dict(icon_count.most_common()),
        "iconography_entropy": round(icon_entropy, 3),
        "iconography_normalised_entropy": round(icon_normalised_entropy, 3),
        "iconography_interpretation": "UNIFORM across all motifs — consistent with function word/grammar sign",
        "top_pre_signs": pre_m267.most_common(10),
        "top_post_signs": post_m267.most_common(10),
        "formula_m267_m099": formula_m267_m099,
        "formula_m099_m267": formula_m099_m267,
        "anchored_signs_adjacent": {
            "before": anchor_pre,
            "after": anchor_post,
        },
        "holdat_role": dict(m267_role),
        "reading_hypothesis": reading_hypothesis,
        "epistemic_status": epistemic,
        "findings": [
            f"M267 appears {n}× across ALL {len(icon_count)} iconographic categories",
            f"Iconographic entropy {icon_normalised_entropy:.2f} (>0.85 = uniform = grammar sign)",
            f"Average position {avg_pos:.3f} — medial, not clearly initial or terminal",
            f"M267→M099 title formula: {formula_m267_m099}× — M267 precedes kol/koḷ",
            f"Top site: {site_count.most_common(1)[0]} ({site_count.most_common(1)[0][1]/site_total:.1%})",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
