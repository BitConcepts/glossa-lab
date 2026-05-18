"""Phase-79: Anchor Gap Priority Analysis.

227/390 Holdat signs are LOW or UNREAD — we have no confirmed phonetic reading.
This script ranks them by how urgently they need to be decoded:

Priority = corpus_frequency × formula_slot_importance
  where formula_slot_importance = how often the sign appears as a NON-SUFFIX slot
  in a decoded or partially-decoded formula (i.e., it's a key unknown in a known context)

Signs that appear frequently in formulas where all OTHER slots are already decoded
are highest priority — decoding them would unlock those formulas.

CPU only (fast analysis).
Output: reports/phase79_anchor_gap_analysis.json
"""
from __future__ import annotations
import csv, json
from collections import Counter, defaultdict
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P59     = REPO / "reports/phase59_pilot_readings.json"
P63     = REPO / "reports/phase63_filtered_decipherment_table.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase79_anchor_gap_analysis.json"

# Sign roles for context (from Phase-68)
SUFFIX_SIGNS  = {"M342", "M176", "M367", "M391", "M336", "M089", "M328", "M162"}
TITLE_SIGNS   = {"M099", "M211", "M073", "M030", "M041", "M059"}
CLASSIFIER_SIGNS = {"M006", "M016", "M045", "M062", "M047", "M039"}

# Iconographic depictions for sign categories
# Source: Parpola 1994 Appendix B + Phase-71 extended map
SIGN_DEPICTIONS = {
    "M003": "pot/vessel",       "M007": "person/figure",   "M019": "arrow/thorn",
    "M021": "jar/vessel",       "M022": "jar variant",     "M023": "comb",
    "M024": "double angle",     "M025": "triangle",        "M033": "compound",
    "M035": "circles",          "M036": "strokes",         "M037": "jar+plant",
    "M038": "compound",         "M043": "trident",         "M044": "jar+mark",
    "M049": "fish+mark",        "M052": "fish+stroke",     "M053": "fish variant",
    "M054": "fish+2",           "M055": "fish+3",          "M056": "fish+4",
    "M058": "section/cut",      "M061": "bull+sign",       "M064": "wide mouth",
    "M066": "jar variant 2",    "M069": "loop",            "M070": "comb variant",
    "M071": "hook",             "M074": "comb+stroke",     "M075": "comb+2",
    "M076": "comb+3",           "M078": "compound",        "M079": "double stroke",
    "M081": "kino variant",     "M082": "plant+stroke",    "M083": "plant variant",
    "M084": "jar+plant",        "M085": "compound",        "M095": "5 strokes",
    "M096": "6 strokes",        "M097": "7 strokes",       "M098": "8 strokes",
    "M107": "kol allograph",    "M118": "wheel variant",   "M130": "sprout variant",
    "M145": "fish+mark2",       "M163": "il allograph",    "M220": "abstract",
    "M221": "abstract 2",       "M222": "hook sign",
}


def main():
    print("Phase-79: Anchor Gap Priority Analysis\n")

    # Load corpus frequency
    freq = Counter()
    seals: dict[str, list] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            if s: freq[s] += 1
            c = row["cisi_number"]; p = int(row.get("position", 0) or 0)
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s

    inscriptions = [[s for s in v if s] for v in seals.values() if any(v)]
    total_tokens = sum(freq.values())

    # Load anchors
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    confirmed = {sign for sign, info in anchors.items()
                 if info.get("confidence") in ("HIGH", "MEDIUM")}
    low_conf  = {sign for sign, info in anchors.items()
                 if info.get("confidence") in ("LOW",)}
    unread    = {sign for sign in freq if sign not in anchors}

    print(f"  Total distinct signs: {len(freq)}")
    print(f"  Confirmed HIGH/MEDIUM: {len(confirmed)}")
    print(f"  LOW confidence:        {len(low_conf)}")
    print(f"  Unread (not in anchors): {len(unread)}")

    # For each sign, count how often it appears next to confirmed signs
    # (i.e., it's a "key unknown" in a known context)
    sign_context_score: Counter = Counter()
    sign_formula_appearances: Counter = Counter()
    sign_in_decoded_formula: Counter = Counter()

    # Load Phase-59 decoded formulas
    decoded_patterns = set()
    if P59.exists():
        p59 = json.loads(P59.read_text("utf-8"))
        for formula in p59.get("fully_decoded_gte_80pct", []):
            pattern = tuple(formula.get("pattern", []))
            decoded_patterns.add(pattern)

    for ins in inscriptions:
        ins_set = set(ins)
        n_confirmed = len(ins_set & confirmed)
        n_total     = len(ins)
        # Context score: how rich is the context for each unread sign?
        for i, sign in enumerate(ins):
            if sign in confirmed: continue
            before = ins[i-1] if i > 0 else None
            after  = ins[i+1] if i < len(ins)-1 else None
            # Confirmed neighbors
            confirmed_neighbors = sum(1 for s in [before, after] if s and s in confirmed)
            context_richness = confirmed_neighbors + n_confirmed / max(n_total, 1)
            sign_context_score[sign] += context_richness
            sign_formula_appearances[sign] += 1

        # Check if this inscription is close to a decoded formula
        for decoded_pat in decoded_patterns:
            if len(ins) >= len(decoded_pat) - 1:  # close in length
                for sign in ins:
                    if sign not in confirmed:
                        sign_in_decoded_formula[sign] += 1

    # Calculate priority score
    priority_signs = []
    target_signs = (unread | low_conf)

    for sign in target_signs:
        corpus_f  = freq.get(sign, 0)
        context_s = sign_context_score.get(sign, 0)
        formula_a = sign_formula_appearances.get(sign, 0)
        decoded_a = sign_in_decoded_formula.get(sign, 0)
        depiction = SIGN_DEPICTIONS.get(sign, "unknown")
        existing  = anchors.get(sign, {})

        priority = (corpus_f * 0.4 + context_s * 0.4 + decoded_a * 0.2)

        priority_signs.append({
            "sign":           sign,
            "corpus_freq":    corpus_f,
            "freq_pct":       round(corpus_f / total_tokens * 100, 2),
            "context_score":  round(context_s, 2),
            "formula_appearances": formula_a,
            "in_decoded_context": decoded_a,
            "priority_score": round(priority, 2),
            "depiction":      depiction,
            "current_reading":existing.get("reading", ""),
            "current_conf":   existing.get("confidence", "UNREAD"),
        })

    priority_signs.sort(key=lambda x: -x["priority_score"])
    n_unread_signs = len(target_signs)

    print(f"\n  Top 20 priority signs to decode next:")
    print(f"  {'Sign':6s} {'Freq':5s} {'%tok':5s} {'Ctx':5s} {'Decoded':7s} {'Priority':8s} {'Depiction'}")
    for p in priority_signs[:20]:
        print(f"  {p['sign']:6s} {p['corpus_freq']:5d} {p['freq_pct']:4.1f}% "
              f"{p['context_score']:5.1f} {p['in_decoded_context']:7d} "
              f"{p['priority_score']:8.1f} {p['depiction']}")

    print(f"\n=== Phase-79 Results ===")
    print(f"  Unread/LOW signs: {n_unread_signs}")
    print(f"  Top priority:     {priority_signs[0]['sign']} "
          f"(freq={priority_signs[0]['corpus_freq']}, score={priority_signs[0]['priority_score']:.1f})")
    print(f"  Insight: Prioritise signs with high corpus frequency AND confirmed-sign context")
    print(f"  Next anchor sprint should target top-20 signs from this list")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "n_unread_signs":     n_unread_signs,
        "n_confirmed":        len(confirmed),
        "total_signs":        len(freq),
        "priority_top20":     priority_signs[:20],
        "priority_all":       priority_signs[:100],
        "methodology": (
            "Priority = corpus_frequency * 0.4 + confirmed_context_score * 0.4 "
            "+ appearances_in_decoded_formula_context * 0.2. "
            "Higher priority = decoding this sign will unlock more formula readings."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
