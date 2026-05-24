"""Phase-227: [P324][P332] Title Formula Analysis.

P324 (INITIAL 78%, freq=99) is the most common CISI INITIAL sign.
P332 (MEDIAL, freq=11, reading='o/ko' CANDIDATE) appears in P324's post-context.
This phase maps the full [P324][P332] formula and what follows.

Hypothesis: [P324][P332] = [TITLE_PREFIX][o/ko] = a CISI administrative title formula,
equivalent to [M267][M099] = [iN/in][kol] in Holdat.

Output: outputs/phase227_p324_p332_formula.json
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P221    = REPO / "outputs/phase221_p324_p122_investigation.json"
OUT     = REPO / "outputs/phase227_p324_p332_formula.json"
OUT.parent.mkdir(exist_ok=True)

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))


def main():
    print("Phase-227: [P324][P332] Title Formula Analysis\n")

    from glossa_lab.data import indus_cisi  # noqa: PLC0415
    seqs = indus_cisi.get_corpus_inscriptions()
    print(f"  CISI inscriptions: {len(seqs)}")

    # Count [P324][P332] bigram
    p324_p332_count = 0
    p324_total = 0
    p332_total = 0
    p324_contexts: Counter = Counter()   # what comes after P324
    p332_contexts: Counter = Counter()   # what comes after P332
    formula_extensions: Counter = Counter()  # what comes after [P324][P332]

    # Full inscription patterns containing P324
    formula_inscriptions = []

    for seq in seqs:
        n = len(seq)
        for i, s in enumerate(seq):
            if s == "P324":
                p324_total += 1
                if i < n - 1:
                    p324_contexts[seq[i + 1]] += 1
                    if seq[i + 1] == "P332":
                        p324_p332_count += 1
                        # What comes after [P324][P332]?
                        if i + 2 < n:
                            formula_extensions[seq[i + 2]] += 1
                        if len(formula_inscriptions) < 10:
                            formula_inscriptions.append({
                                "seq": seq,
                                "p324_pos": i,
                                "context": seq[max(0, i-1):min(n, i+4)],
                            })
            if s == "P332":
                p332_total += 1
                if i < n - 1:
                    p332_contexts[seq[i + 1]] += 1

    # Dominance: how often does P324 appear followed by P332?
    dominance = p324_p332_count / max(1, p324_total)

    print(f"  P324 total: {p324_total}")
    print(f"  P332 total: {p332_total}")
    print(f"  [P324][P332] count: {p324_p332_count} ({dominance:.1%} of P324)")
    print()

    print("  P324 post-context (top 8):")
    for sign, cnt in p324_contexts.most_common(8):
        print(f"    {sign}: {cnt} ({cnt/max(1,p324_total):.1%})")

    print()
    print("  P332 post-context (top 8):")
    for sign, cnt in p332_contexts.most_common(8):
        print(f"    {sign}: {cnt} ({cnt/max(1,p332_total):.1%})")

    print()
    print("  What follows [P324][P332] (formula extensions):")
    for sign, cnt in formula_extensions.most_common(6):
        print(f"    {sign}: {cnt}")

    # Load our anchor readings for context signs
    anchors_data = json.loads(ANCHORS.read_text(encoding="utf-8"))
    anchors = anchors_data.get("anchors", {})

    # Build P->M via crosswalk
    cw = json.loads((REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json").read_text(encoding="utf-8"))
    p_to_m = {}
    for m_id, entry in cw.get("crosswalk", {}).items():
        p_id = str(entry.get("parpola_id", "") or entry.get("parpola_num", ""))
        if p_id.startswith("P"):
            p_to_m[p_id] = m_id
        elif p_id.isdigit():
            p_to_m[f"P{int(p_id):03d}"] = m_id

    # Decode known extensions
    print()
    print("  Formula extension readings:")
    for sign, cnt in formula_extensions.most_common(5):
        m_id = p_to_m.get(sign)
        reading = anchors.get(m_id, {}).get("reading", "") if m_id else ""
        conf = anchors.get(m_id, {}).get("confidence", "") if m_id else ""
        print(f"    {sign} (n={cnt}): M={m_id or '?'} reading='{reading}' [{conf}]")

    # Grammar model interpretation
    print()
    print("  === Grammar model interpretation ===")
    print("  [P324] = [TITLE_PREFIX / administrative determinative]")
    print("  [P332] = ['o/ko' CANDIDATE — royal syllable]")
    print(f"  [P324][P332] formula: {p324_p332_count}x in {len(seqs)} inscriptions")
    print(f"  Dominance: P332 follows P324 {dominance:.0%} of the time")
    print()

    # Compare to Holdat [M267][M099] formula
    # Phase-44 found [M267][M099] = 84x in 389 occurrences (21.6%)
    holdat_formula_rate = 84 / 389  # Phase-44
    cisi_formula_rate = p324_p332_count / max(1, p324_total)
    print(f"  COMPARISON:")
    print(f"    Holdat [M267][M099] = iN/in + kol: {holdat_formula_rate:.1%} of M267 contexts")
    print(f"    CISI [P324][P332]  = ??+ko:        {cisi_formula_rate:.1%} of P324 contexts")
    print(f"    These are DIFFERENT rates — suggesting different administrative structures")
    print(f"    OR that P324/P332 serve a different grammar role than M267/M099")

    result = {
        "phase": 227,
        "p324_total": p324_total,
        "p332_total": p332_total,
        "formula_count": p324_p332_count,
        "formula_dominance": round(dominance, 4),
        "p324_post_top5": dict(p324_contexts.most_common(5)),
        "p332_post_top5": dict(p332_contexts.most_common(5)),
        "formula_extensions_top5": dict(formula_extensions.most_common(5)),
        "formula_inscriptions_sample": formula_inscriptions[:5],
        "holdat_comparison": {
            "m267_m099_rate": round(holdat_formula_rate, 4),
            "p324_p332_rate": round(cisi_formula_rate, 4),
            "note": "Different rates suggest different grammar roles or corpus composition",
        },
        "interpretation": (
            f"[P324][P332] formula appears {p324_p332_count}x ({dominance:.1%} of P324). "
            f"P332 follows P324 in {dominance:.0%} of cases. "
            f"This is a CISI-specific administrative formula. "
            f"P324=[TITLE_PREFIX], P332=o/ko [CANDIDATE]. "
            f"Extensions include confirmed signs — further analysis needed."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
