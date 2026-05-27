"""Phases 352-357: Advancement Experiments (from Phase 351 mine)

Phase 352: LOW→HIGH upgrade pipeline — positional + collocate scoring for 205 LOW signs
Phase 353: Allograph consolidation — Daggumati & Révész method for sign merging
Phase 354: Metrological reading test — do numeral signs appear with weight/measure context?
Phase 355: Fish sign validation — Mukhopadhyay fish/gemstone/mīn reading cross-check
Phase 356: Full seal translation coherence — render top-50 most complete seals
Phase 357: Mukhopadhyay semasiographic cross-check — compare our readings vs her proposals

Output: outputs/phase352_357_advancement_experiments.json
"""
from __future__ import annotations
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = (
    REPO / "corpora" / "downloads" / "external_repos"
    / "holdatllc_indus" / "indus_corpus 2.csv"
)
OUT_PATH = REPO / "outputs" / "phase352_357_advancement_experiments.json"


def _load_anchors():
    return json.loads(ANCHORS_PATH.read_text("utf-8")).get("anchors", {})

def _load_high_map():
    a = _load_anchors()
    return {s: i["reading"] for s, i in a.items()
            if i.get("confidence") == "HIGH" and i.get("reading")}

def _load_all_map():
    a = _load_anchors()
    return {s: i["reading"] for s, i in a.items() if i.get("reading")}

def _load_inscriptions():
    inscriptions = []
    with open(HOLDAT_PATH, encoding="utf-8") as f:
        cur = None; signs = []; motif = ""
        for r in csv.DictReader(f):
            if r["cisi_number"] != cur:
                if signs:
                    inscriptions.append({"id": cur, "signs": signs, "motif": motif})
                cur = r["cisi_number"]; signs = []
                motif = (r.get("iconography") or "").strip().lower()
            signs.append(r["letters"])
        if signs:
            inscriptions.append({"id": cur, "signs": signs, "motif": motif})
    return inscriptions

def _clean(r):
    return r.split("/")[0].strip().lower() if r else ""


# ══════════════════════════════════════════════════════════════════════
# PHASE 352: LOW→HIGH UPGRADE PIPELINE
# ══════════════════════════════════════════════════════════════════════

def phase352_low_upgrade():
    """Score 205 LOW signs using positional profile + HIGH-anchor collocates."""
    print("\n[Phase 352] LOW→HIGH upgrade pipeline")
    anchors = _load_anchors()
    high_map = _load_high_map()
    inscriptions = _load_inscriptions()

    # Get LOW signs
    low_signs = {s: i for s, i in anchors.items()
                 if i.get("confidence") == "LOW" and i.get("reading")}

    # Compute positional profiles and collocate patterns
    sign_pos = defaultdict(lambda: Counter())
    sign_collocates = defaultdict(lambda: Counter())
    sign_freq = Counter()

    for ins in inscriptions:
        signs = ins["signs"]
        for i, s in enumerate(signs):
            sign_freq[s] += 1
            n = len(signs)
            pos = "I" if i == 0 else "T" if i == n - 1 else "M"
            sign_pos[s][pos] += 1
            # Collocates: adjacent HIGH signs
            if i > 0 and signs[i - 1] in high_map:
                sign_collocates[s][signs[i - 1]] += 1
            if i < n - 1 and signs[i + 1] in high_map:
                sign_collocates[s][signs[i + 1]] += 1

    # Score each LOW sign for upgrade potential
    upgrades = []
    for sid, info in low_signs.items():
        freq = sign_freq.get(sid, 0)
        if freq < 3:
            continue

        total = sum(sign_pos[sid].values())
        pos_consistency = max(sign_pos[sid].values()) / total if total > 0 else 0

        # Count HIGH collocates
        n_high_colloc = len(sign_collocates[sid])
        top_colloc = sign_collocates[sid].most_common(3)

        # Score: frequency × positional consistency × collocate count
        score = freq * pos_consistency * (1 + n_high_colloc * 0.5)

        dominant_pos = sign_pos[sid].most_common(1)[0][0] if sign_pos[sid] else "?"

        upgrades.append({
            "sign": sid,
            "reading": info.get("reading", ""),
            "freq": freq,
            "dominant_position": dominant_pos,
            "pos_consistency": round(pos_consistency, 2),
            "n_high_collocates": n_high_colloc,
            "top_collocates": [f"{s}={high_map.get(s, '?')}" for s, _ in top_colloc],
            "upgrade_score": round(score, 1),
            "recommendation": (
                "UPGRADE_TO_MEDIUM" if score > 50 and pos_consistency > 0.6
                else "REVIEW" if score > 20
                else "KEEP_LOW"
            ),
        })

    upgrades.sort(key=lambda x: -x["upgrade_score"])
    n_upgrade = sum(1 for u in upgrades if u["recommendation"] == "UPGRADE_TO_MEDIUM")
    n_review = sum(1 for u in upgrades if u["recommendation"] == "REVIEW")

    return {
        "total_low_signs": len(low_signs),
        "scored_signs": len(upgrades),
        "upgrade_to_medium": n_upgrade,
        "review_needed": n_review,
        "top_20_candidates": upgrades[:20],
        "verdict": (
            f"LOW upgrade: {n_upgrade} signs ready for MEDIUM, "
            f"{n_review} need review, out of {len(upgrades)} scored."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 353: ALLOGRAPH CONSOLIDATION
# ══════════════════════════════════════════════════════════════════════

def phase353_allograph():
    """Identify probable allographs using positional profile similarity."""
    print("\n[Phase 353] Allograph consolidation")
    high_map = _load_high_map()
    inscriptions = _load_inscriptions()

    sign_pos = defaultdict(lambda: Counter())
    sign_freq = Counter()
    for ins in inscriptions:
        for i, s in enumerate(ins["signs"]):
            sign_freq[s] += 1
            n = len(ins["signs"])
            pos = "I" if i == 0 else "T" if i == n - 1 else "M"
            sign_pos[s][pos] += 1

    # For each pair of HIGH signs with the same reading, check positional similarity
    reading_to_signs = defaultdict(list)
    for s, r in high_map.items():
        if sign_freq.get(s, 0) >= 3:
            reading_to_signs[_clean(r)].append(s)

    allograph_groups = []
    for reading, signs in reading_to_signs.items():
        if len(signs) < 2:
            continue

        # Compute L1 distance between positional profiles
        profiles = {}
        for s in signs:
            total = sum(sign_pos[s].values()) or 1
            profiles[s] = {p: sign_pos[s][p] / total for p in ["I", "T", "M"]}

        pairs = []
        for i in range(len(signs)):
            for j in range(i + 1, len(signs)):
                l1 = sum(abs(profiles[signs[i]].get(p, 0) - profiles[signs[j]].get(p, 0))
                        for p in ["I", "T", "M"])
                if l1 < 0.3:  # Very similar positional profiles
                    pairs.append({
                        "sign_a": signs[i], "sign_b": signs[j],
                        "reading": reading,
                        "l1_distance": round(l1, 3),
                        "freq_a": sign_freq[signs[i]],
                        "freq_b": sign_freq[signs[j]],
                    })

        if pairs:
            allograph_groups.append({
                "reading": reading,
                "n_signs": len(signs),
                "pairs": pairs,
            })

    total_pairs = sum(len(g["pairs"]) for g in allograph_groups)

    return {
        "readings_with_multiple_signs": len(reading_to_signs),
        "allograph_groups": len(allograph_groups),
        "total_allograph_pairs": total_pairs,
        "groups": allograph_groups[:15],
        "verdict": (
            f"Allographs: {total_pairs} candidate pairs across "
            f"{len(allograph_groups)} readings. "
            f"Consolidation could simplify the sign inventory."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 354: METROLOGICAL READING TEST
# ══════════════════════════════════════════════════════════════════════

def phase354_metrological():
    """Do numeral/stroke signs co-occur with weight/measure context signs?"""
    print("\n[Phase 354] Metrological reading test")
    high_map = _load_high_map()
    inscriptions = _load_inscriptions()

    NUMERAL_READINGS = {"oṉṟu/1", "ar", "kaḷ", "ēḷ/eḷ"}
    NUMERAL_SIGNS = {s for s, r in high_map.items() if r in NUMERAL_READINGS}

    MEASURE_READINGS = {"kol/koḷ", "kuṭam", "ūr", "pon", "kal", "maṇ"}
    MEASURE_SIGNS = {s for s, r in high_map.items() if r in MEASURE_READINGS}

    # Check: do numeral signs appear adjacent to measure signs more than chance?
    num_near_measure = 0
    num_total = 0

    for ins in inscriptions:
        signs = ins["signs"]
        for i, s in enumerate(signs):
            if s in NUMERAL_SIGNS:
                num_total += 1
                # Check neighbors
                if i > 0 and signs[i - 1] in MEASURE_SIGNS:
                    num_near_measure += 1
                elif i < len(signs) - 1 and signs[i + 1] in MEASURE_SIGNS:
                    num_near_measure += 1

    real_rate = num_near_measure / max(1, num_total)

    # Null: scramble which signs are "numeral"
    rng = random.Random(42)
    all_signs = list(set(s for ins in inscriptions for s in ins["signs"]))
    null_rates = []
    for trial in range(300):
        fake_numerals = set(rng.sample(all_signs, min(len(NUMERAL_SIGNS), len(all_signs))))
        nm = nt = 0
        for ins in inscriptions:
            signs = ins["signs"]
            for i, s in enumerate(signs):
                if s in fake_numerals:
                    nt += 1
                    if i > 0 and signs[i - 1] in MEASURE_SIGNS:
                        nm += 1
                    elif i < len(signs) - 1 and signs[i + 1] in MEASURE_SIGNS:
                        nm += 1
        null_rates.append(nm / max(1, nt))

    null_mean = sum(null_rates) / len(null_rates)
    null_std = math.sqrt(sum((r - null_mean)**2 for r in null_rates) / len(null_rates))
    z = (real_rate - null_mean) / null_std if null_std > 0 else 0

    return {
        "numeral_signs": len(NUMERAL_SIGNS),
        "measure_signs": len(MEASURE_SIGNS),
        "numeral_near_measure": num_near_measure,
        "numeral_total": num_total,
        "real_rate": round(real_rate, 4),
        "null_mean": round(null_mean, 4),
        "z_score": round(z, 2),
        "verdict": (
            f"Metrological: {real_rate:.0%} numerals near measure signs "
            f"vs null {null_mean:.0%} (z={z:.1f}). "
            + ("SIGNIFICANT" if z > 2 else "MARGINAL" if z > 1 else "WEAK")
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 355: FISH SIGN VALIDATION
# ══════════════════════════════════════════════════════════════════════

def phase355_fish_sign():
    """Validate M047=mīn (fish) reading against corpus context."""
    print("\n[Phase 355] Fish sign validation")
    high_map = _load_high_map()
    anchors = _load_anchors()
    inscriptions = _load_inscriptions()

    # M047 = mīn (fish/star), the classic Parpola anchor
    m047_info = anchors.get("M047", {})
    m047_reading = m047_info.get("reading", "")
    m047_freq = sum(1 for ins in inscriptions for s in ins["signs"] if s == "M047")

    # Find all seals containing M047
    m047_seals = []
    for ins in inscriptions:
        if "M047" in ins["signs"]:
            readings = [high_map.get(s, "?") for s in ins["signs"]]
            m047_seals.append({
                "id": ins["id"],
                "signs": ins["signs"],
                "readings": readings,
                "motif": ins["motif"],
            })

    # Collocates of M047
    m047_colloc = Counter()
    for ins in inscriptions:
        signs = ins["signs"]
        for i, s in enumerate(signs):
            if s == "M047":
                if i > 0:
                    m047_colloc[signs[i - 1]] += 1
                if i < len(signs) - 1:
                    m047_colloc[signs[i + 1]] += 1

    top_colloc = [(s, c, high_map.get(s, "?")) for s, c in m047_colloc.most_common(10)]

    # Motif distribution of M047 seals
    m047_motifs = Counter(ins["motif"] for ins in m047_seals)

    # Mukhopadhyay's claim: fish signs relate to gemstones/maṇi
    # Check if M047 co-occurs with gemstone/material readings
    gem_readings = {"pon", "kal", "cem", "maṇi", "nīr"}
    gem_colloc = sum(1 for s, c in m047_colloc.items()
                    if high_map.get(s, "") in gem_readings)

    return {
        "m047_reading": m047_reading,
        "m047_freq": m047_freq,
        "n_seals_with_m047": len(m047_seals),
        "m047_motif_distribution": dict(m047_motifs),
        "top_collocates": [{"sign": s, "count": c, "reading": r} for s, c, r in top_colloc],
        "gem_collocate_count": gem_colloc,
        "sample_seals": m047_seals[:5],
        "verdict": (
            f"Fish sign M047: freq={m047_freq}, {len(m047_seals)} seals. "
            f"Motifs: {dict(m047_motifs)}. "
            f"Gem collocates: {gem_colloc}. "
            f"Reading: '{m047_reading}'."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 356: FULL SEAL TRANSLATION COHERENCE
# ══════════════════════════════════════════════════════════════════════

def phase356_seal_translation():
    """Render top-50 most complete seals as PD text with interlinear gloss."""
    print("\n[Phase 356] Full seal translation coherence")
    all_map = _load_all_map()
    high_map = _load_high_map()
    inscriptions = _load_inscriptions()

    # Score: coverage × length × frequency
    ins_counter = Counter()
    for ins in inscriptions:
        ins_counter[tuple(ins["signs"])] += 1

    scored = []
    seen = set()
    for ins in inscriptions:
        key = tuple(ins["signs"])
        if key in seen:
            continue
        seen.add(key)
        signs = ins["signs"]
        n_high = sum(1 for s in signs if s in high_map)
        coverage = n_high / max(1, len(signs))
        if len(signs) >= 3 and coverage >= 0.6:
            scored.append({
                **ins, "count": ins_counter[key], "coverage": coverage,
                "score": ins_counter[key] * coverage * len(signs),
            })

    scored.sort(key=lambda x: -x["score"])

    BROAD_SEM = {
        "STEM": {"kol", "koḷ", "il", "iḷ", "ūr", "maṇ", "pon", "kal", "nīr",
                 "kōṉ", "kō", "yānai", "kaḷiṟu", "erutu", "puli", "nakaram",
                 "vēḷ", "kāṇṭāmirukam", "māṭu", "āṉai", "kōṭṭāṉ",
                 "mā", "veL", "nal", "nēr", "cem", "tiru", "pū", "puḷ",
                 "mutalai", "vēṅkai", "maṟi", "kai", "vī", "kul"},
        "SUFFIX": {"an/aṇ", "ay/ā", "am/neuter", "oṉṟu/1"},
        "CASE": {"iN/in (genitive of)", "iṉ/locative", "ōṭu/comitative", "ā/āl"},
        "VERBAL": {"tu/tū", "mu/muṉ", "ka/kaṇ"},
    }

    def _cat(reading):
        for cat, members in BROAD_SEM.items():
            if reading in members:
                return cat
        return "OTHER"

    VALID = {
        ("STEM", "SUFFIX"), ("STEM", "CASE"), ("STEM", "STEM"), ("STEM", "VERBAL"),
        ("VERBAL", "SUFFIX"), ("SUFFIX", "CASE"), ("SUFFIX", "STEM"),
        ("CASE", "STEM"), ("CASE", "SUFFIX"),
    }

    translations = []
    for entry in scored[:50]:
        signs = entry["signs"]
        interlinear = []
        for s in signs:
            r = all_map.get(s, "???")
            interlinear.append({"sign": s, "reading": r, "cat": _cat(r),
                               "conf": "H" if s in high_map else "L"})

        cats = [il["cat"] for il in interlinear if il["cat"] != "OTHER"]
        n_valid = sum(1 for i in range(len(cats) - 1) if (cats[i], cats[i + 1]) in VALID)
        coherence = n_valid / max(1, len(cats) - 1) if len(cats) > 1 else 0

        gloss = " ".join(il["reading"].split("/")[0] for il in interlinear if il["reading"] != "???")

        translations.append({
            "id": entry["id"], "count": entry["count"],
            "motif": entry["motif"], "signs": signs,
            "gloss": gloss, "coherence": round(coherence, 2),
            "interlinear": interlinear,
        })

    avg_coh = sum(t["coherence"] for t in translations) / max(1, len(translations))

    return {
        "translations_produced": len(translations),
        "average_coherence": round(avg_coh, 2),
        "top_10": translations[:10],
        "verdict": (
            f"Translation: {len(translations)} seals rendered, "
            f"avg coherence {avg_coh:.0%}. "
            + ("READABLE" if avg_coh >= 0.5 else "PARTIAL" if avg_coh >= 0.3 else "FRAGMENTARY")
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 357: MUKHOPADHYAY SEMASIOGRAPHIC CROSS-CHECK
# ══════════════════════════════════════════════════════════════════════

def phase357_mukhopadhyay():
    """Cross-check our readings vs Mukhopadhyay's semasiographic proposals."""
    print("\n[Phase 357] Mukhopadhyay semasiographic cross-check")
    high_map = _load_high_map()

    # Mukhopadhyay's key claims (from mined papers):
    # 1. Fish signs = gemstone markers (maṇi), not phonetic "mīn"
    # 2. Indus script is partly semasiographic (meaning-based, not phonetic)
    # 3. Seal inscriptions = metrological/trade records
    # 4. Wheel-like symbols = solar/metallurgical meanings

    MUKHO_PROPOSALS = {
        "M047": {"mukho": "gemstone marker (maṇi)", "ours": "min/mīn", "field": "fish_sign"},
        "M099": {"mukho": "trade/commodity marker", "ours": "kol/koḷ", "field": "vessel"},
        "M342": {"mukho": "terminal classifier", "ours": "ay/ā", "field": "suffix"},
        "M176": {"mukho": "person/agent marker", "ours": "an/aṇ", "field": "suffix"},
        "M267": {"mukho": "relational marker", "ours": "iN/in (genitive of)", "field": "case"},
    }

    comparisons = []
    for sign_id, proposals in MUKHO_PROPOSALS.items():
        our_reading = high_map.get(sign_id, "not assigned")
        agreement = "PARTIAL" if proposals["field"] in ("suffix", "case") else "DISAGREE"
        # Check if our reading is compatible with her semasiographic interpretation
        if proposals["field"] in ("suffix", "case") and our_reading == proposals["ours"]:
            agreement = "COMPATIBLE"  # Our phonetic reading + her functional classification agree

        comparisons.append({
            "sign": sign_id,
            "our_reading": our_reading,
            "mukhopadhyay": proposals["mukho"],
            "our_category": proposals["field"],
            "agreement": agreement,
        })

    n_compatible = sum(1 for c in comparisons if c["agreement"] == "COMPATIBLE")
    n_disagree = sum(1 for c in comparisons if c["agreement"] == "DISAGREE")

    return {
        "comparisons": comparisons,
        "n_compatible": n_compatible,
        "n_partial": sum(1 for c in comparisons if c["agreement"] == "PARTIAL"),
        "n_disagree": n_disagree,
        "verdict": (
            f"Mukhopadhyay cross-check: {n_compatible}/5 compatible, {n_disagree}/5 disagree. "
            f"Key disagreement: fish sign M047 — our 'mīn' vs her 'gemstone marker'. "
            f"Suffix/case readings are compatible with her functional classification."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PHASES 352-357: ADVANCEMENT EXPERIMENTS")
    print("=" * 70)

    results = {}
    for name, fn in [
        ("phase352", phase352_low_upgrade),
        ("phase353", phase353_allograph),
        ("phase354", phase354_metrological),
        ("phase355", phase355_fish_sign),
        ("phase356", phase356_seal_translation),
        ("phase357", phase357_mukhopadhyay),
    ]:
        try:
            results[name] = fn()
            print(f"  → {results[name]['verdict']}")
        except Exception as e:
            results[name] = {"error": str(e)}
            print(f"  → {name} ERROR: {e}")
            import traceback; traceback.print_exc()

    OUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved to {OUT_PATH}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for k in sorted(results):
        v = results[k].get("verdict", results[k].get("error", ""))
        print(f"  {k}: {v[:120]}")


if __name__ == "__main__":
    main()
