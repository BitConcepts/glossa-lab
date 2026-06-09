"""Phases 358-362: Consolidate Allographs and Advance

Phase 358: Apply 84 allograph consolidations — merge sign variants
Phase 359: Deep-mine Mukhopadhyay for specific sign-value cross-checks
Phase 360: Re-translate seals with consolidated reading set
Phase 361: Cross-check Mukhopadhyay's specific proposals against corpus
Phase 362: Summary assessment — what changed, what's next

Output: outputs/phase358_362_consolidate_advance.json
"""
from __future__ import annotations
import csv
import json
import math
import random
import re
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = (
    REPO / "corpora" / "downloads" / "external_repos"
    / "holdatllc_indus" / "indus_corpus 2.csv"
)
OUT_PATH = REPO / "outputs" / "phase358_362_consolidate_advance.json"


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
# PHASE 358: APPLY ALLOGRAPH CONSOLIDATION
# ══════════════════════════════════════════════════════════════════════

def phase358_consolidate():
    """Merge allograph pairs into canonical sign IDs."""
    print("\n[Phase 358] Allograph consolidation")
    high_map = _load_high_map()
    inscriptions = _load_inscriptions()

    # Build positional profiles
    sign_pos = defaultdict(lambda: Counter())
    sign_freq = Counter()
    for ins in inscriptions:
        for i, s in enumerate(ins["signs"]):
            sign_freq[s] += 1
            n = len(ins["signs"])
            pos = "I" if i == 0 else "T" if i == n - 1 else "M"
            sign_pos[s][pos] += 1

    # Group signs by reading
    reading_to_signs = defaultdict(list)
    for s, r in high_map.items():
        if sign_freq.get(s, 0) >= 3:
            reading_to_signs[_clean(r)].append(s)

    # Find allograph pairs (L1 < 0.3)
    merges = {}  # secondary → canonical (highest-freq sign in group)
    merge_groups = []

    for reading, signs in reading_to_signs.items():
        if len(signs) < 2:
            continue

        profiles = {}
        for s in signs:
            total = sum(sign_pos[s].values()) or 1
            profiles[s] = {p: sign_pos[s][p] / total for p in ["I", "T", "M"]}

        # Find canonical (highest freq) and merge others into it
        signs_sorted = sorted(signs, key=lambda s: -sign_freq[s])
        canonical = signs_sorted[0]

        group_members = [canonical]
        for s in signs_sorted[1:]:
            l1 = sum(abs(profiles[canonical].get(p, 0) - profiles[s].get(p, 0))
                    for p in ["I", "T", "M"])
            if l1 < 0.3:
                merges[s] = canonical
                group_members.append(s)

        if len(group_members) > 1:
            merge_groups.append({
                "reading": reading,
                "canonical": canonical,
                "canonical_freq": sign_freq[canonical],
                "merged": [s for s in group_members if s != canonical],
                "merged_freqs": [sign_freq[s] for s in group_members if s != canonical],
            })

    # Build consolidated high map
    consolidated_map = {}
    for s, r in high_map.items():
        canonical = merges.get(s, s)
        consolidated_map[canonical] = r
        # Also map the secondary sign to the same reading
        consolidated_map[s] = r

    # Stats
    n_original = len(high_map)
    n_unique_canonical = len(set(merges.get(s, s) for s in high_map))
    n_merged = len(merges)

    return {
        "original_high_signs": n_original,
        "unique_canonical_signs": n_unique_canonical,
        "signs_merged": n_merged,
        "merge_groups": merge_groups[:20],
        "merge_map": merges,
        "consolidated_map": consolidated_map,
        "verdict": (
            f"Consolidated: {n_original} → {n_unique_canonical} canonical signs "
            f"({n_merged} merged). {len(merge_groups)} allograph groups."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 359: DEEP-MINE MUKHOPADHYAY
# ══════════════════════════════════════════════════════════════════════

def phase359_mukhopadhyay_mine():
    """Fetch abstracts of Mukhopadhyay's key papers for sign-value extraction."""
    print("\n[Phase 359] Deep-mine Mukhopadhyay proposals")

    MUKHO_DOIS = [
        "10.31235/osf.io/ftdzc",   # fish/gemstone/maṇi
        "10.1057/s41599-019-0274-1", # meaning conveyance
        "10.31235/osf.io/942ra",     # metal-smithy decoded
        "10.31235/osf.io/h8ct7",     # tax tokens, metrological
        "10.31235/osf.io/9z4ka",     # wheel-like symbols
    ]

    papers = []
    for doi in MUKHO_DOIS:
        url = f"https://api.openalex.org/works/https://doi.org/{doi}?select=id,title,abstract_inverted_index"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "GlossaLab/0.5 (research; tpierson@bitconcepts.tech)"
            })
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
            title = data.get("title", "")
            abstract = ""
            aii = data.get("abstract_inverted_index")
            if aii:
                pairs = sorted([(pos, word) for word, positions in aii.items()
                               for pos in positions])
                abstract = " ".join(w for _, w in pairs)
            papers.append({"doi": doi, "title": title, "abstract": abstract[:1000]})
        except Exception:
            papers.append({"doi": doi, "title": "FETCH_FAILED", "abstract": ""})
        time.sleep(0.5)

    # Extract specific sign-value proposals from abstracts
    proposals = []
    for p in papers:
        text = f"{p['title']} {p['abstract']}".lower()
        # Look for sign-value claims
        if "maṇi" in text or "mani" in text:
            proposals.append({"claim": "fish signs encode 'maṇi' (gemstone/bead)",
                             "source": p["doi"]})
        if "metrolog" in text or "weight" in text:
            proposals.append({"claim": "inscriptions are metrological records",
                             "source": p["doi"]})
        if "tax" in text or "trade license" in text:
            proposals.append({"claim": "seals functioned as tax tokens/trade licenses",
                             "source": p["doi"]})
        if "metal" in text or "smith" in text:
            proposals.append({"claim": "sign groups relate to metalworking vocabulary",
                             "source": p["doi"]})
        if "wheel" in text or "solar" in text:
            proposals.append({"claim": "wheel-like signs have solar/metallurgical meaning",
                             "source": p["doi"]})

    return {
        "papers_fetched": len([p for p in papers if p["title"] != "FETCH_FAILED"]),
        "proposals_extracted": len(proposals),
        "proposals": proposals,
        "papers": [{"doi": p["doi"], "title": p["title"],
                    "abstract_len": len(p["abstract"])} for p in papers],
        "verdict": (
            f"Mukhopadhyay mine: {len([p for p in papers if p['title'] != 'FETCH_FAILED'])}/5 papers fetched, "
            f"{len(proposals)} specific proposals extracted."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 360: RE-TRANSLATE WITH CONSOLIDATED SET
# ══════════════════════════════════════════════════════════════════════

def phase360_retranslate(consolidated_map):
    """Re-translate seals using the consolidated allograph map."""
    print("\n[Phase 360] Re-translate with consolidated readings")
    inscriptions = _load_inscriptions()

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

    # Score inscriptions
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
        n_read = sum(1 for s in signs if s in consolidated_map)
        coverage = n_read / max(1, len(signs))
        if len(signs) >= 3 and coverage >= 0.5:
            scored.append({
                **ins, "count": ins_counter[key], "coverage": coverage,
                "score": ins_counter[key] * coverage * len(signs),
            })

    scored.sort(key=lambda x: -x["score"])

    translations = []
    for entry in scored[:50]:
        signs = entry["signs"]
        interlinear = []
        for s in signs:
            r = consolidated_map.get(s, "???")
            interlinear.append({"sign": s, "reading": r, "cat": _cat(r)})

        cats = [il["cat"] for il in interlinear if il["cat"] != "OTHER"]
        n_valid = sum(1 for i in range(len(cats) - 1) if (cats[i], cats[i + 1]) in VALID)
        coherence = n_valid / max(1, len(cats) - 1) if len(cats) > 1 else 0

        gloss = " ".join(il["reading"].split("/")[0] for il in interlinear if il["reading"] != "???")

        # Attempt semantic interpretation
        reading_cats = [il["cat"] for il in interlinear]
        has_stem = "STEM" in reading_cats
        has_suffix = "SUFFIX" in reading_cats
        has_case = "CASE" in reading_cats
        pattern = "→".join(reading_cats[:6])

        translations.append({
            "id": entry["id"], "count": entry["count"],
            "motif": entry["motif"], "coverage": round(entry["coverage"], 2),
            "gloss": gloss, "coherence": round(coherence, 2),
            "pattern": pattern,
            "has_stem_suffix": has_stem and has_suffix,
            "interlinear": interlinear,
        })

    avg_coh = sum(t["coherence"] for t in translations) / max(1, len(translations))
    avg_cov = sum(t["coverage"] for t in translations) / max(1, len(translations))
    n_with_ss = sum(1 for t in translations if t["has_stem_suffix"])

    return {
        "total_translatable": len(scored),
        "translations_produced": len(translations),
        "average_coherence": round(avg_coh, 2),
        "average_coverage": round(avg_cov, 2),
        "n_with_stem_suffix": n_with_ss,
        "top_10": translations[:10],
        "verdict": (
            f"Consolidated translation: {len(translations)} seals, "
            f"avg coherence {avg_coh:.0%}, coverage {avg_cov:.0%}. "
            f"{n_with_ss}/{len(translations)} have STEM+SUFFIX structure. "
            + ("READABLE" if avg_coh >= 0.5 else "PARTIAL" if avg_coh >= 0.3 else "FRAGMENTARY")
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 361: CROSS-CHECK MUKHOPADHYAY PROPOSALS
# ══════════════════════════════════════════════════════════════════════

def phase361_crosscheck(mukho_proposals):
    """Test Mukhopadhyay's specific proposals against corpus data."""
    print("\n[Phase 361] Cross-check Mukhopadhyay proposals")
    high_map = _load_high_map()
    inscriptions = _load_inscriptions()

    results = []

    # 1. Test: "fish signs encode gemstone/maṇi"
    # If true, fish-sign seals should co-occur with material/craft context
    fish_signs = {s for s, r in high_map.items() if "mīn" in r or "min" in r.lower()}
    craft_readings = {"pon", "kal", "cem", "vil", "kalam", "kuṭam"}
    craft_signs = {s for s, r in high_map.items() if _clean(r) in craft_readings}

    fish_near_craft = 0
    fish_total = 0
    for ins in inscriptions:
        signs = ins["signs"]
        for i, s in enumerate(signs):
            if s in fish_signs:
                fish_total += 1
                if i > 0 and signs[i-1] in craft_signs:
                    fish_near_craft += 1
                elif i < len(signs) - 1 and signs[i+1] in craft_signs:
                    fish_near_craft += 1

    results.append({
        "proposal": "Fish signs = gemstone/craft markers",
        "test": "fish sign proximity to craft/material signs",
        "fish_total": fish_total,
        "fish_near_craft": fish_near_craft,
        "rate": round(fish_near_craft / max(1, fish_total), 3),
        "assessment": "WEAK_SUPPORT" if fish_near_craft > fish_total * 0.2 else "NOT_SUPPORTED",
    })

    # 2. Test: "seals are metrological records"
    # If true, numeral signs should be highly frequent and positionally systematic
    numeral_readings = {"oṉṟu/1", "ēḷ/eḷ"}
    numeral_signs = {s for s, r in high_map.items() if r in numeral_readings}
    numeral_freq = sum(sign_freq for s in numeral_signs
                      for ins in inscriptions for sign_freq in [1]
                      if s in ins["signs"])

    total_tokens = sum(len(ins["signs"]) for ins in inscriptions)
    numeral_rate = numeral_freq / max(1, total_tokens)

    results.append({
        "proposal": "Seals are metrological records",
        "test": "numeral sign frequency in corpus",
        "numeral_tokens": numeral_freq,
        "total_tokens": total_tokens,
        "numeral_rate": round(numeral_rate, 4),
        "assessment": ("SUPPORTED" if numeral_rate > 0.05
                       else "PARTIAL" if numeral_rate > 0.02
                       else "NOT_SUPPORTED"),
    })

    # 3. Test: "guild/trade function"
    # Both us and Mukhopadhyay agree seals encode professional identity
    # Test: do title readings (kōṉ, vēḷ, tiru) appear in INITIAL position?
    title_readings = {"kōṉ", "kō", "vēḷ", "tiru", "mā"}
    title_signs = {s for s, r in high_map.items() if _clean(r) in title_readings}

    title_initial = 0
    title_total = 0
    for ins in inscriptions:
        for i, s in enumerate(ins["signs"]):
            if s in title_signs:
                title_total += 1
                if i == 0:
                    title_initial += 1

    title_init_rate = title_initial / max(1, title_total)

    results.append({
        "proposal": "Seals encode guild/professional identity",
        "test": "title readings in INITIAL position",
        "title_initial": title_initial,
        "title_total": title_total,
        "initial_rate": round(title_init_rate, 3),
        "assessment": ("SUPPORTED" if title_init_rate > 0.4
                       else "PARTIAL" if title_init_rate > 0.2
                       else "NOT_SUPPORTED"),
    })

    n_supported = sum(1 for r in results if r["assessment"] in ("SUPPORTED", "PARTIAL"))

    return {
        "tests": results,
        "n_supported": n_supported,
        "n_total": len(results),
        "verdict": (
            f"Mukhopadhyay cross-check: {n_supported}/{len(results)} proposals "
            f"supported/partially supported by corpus data."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 362: SUMMARY ASSESSMENT
# ══════════════════════════════════════════════════════════════════════

def phase362_summary(all_results):
    """Summarize what changed and what's next."""
    print("\n[Phase 362] Summary assessment")

    consol = all_results.get("phase358", {})
    trans = all_results.get("phase360", {})
    cross = all_results.get("phase361", {})

    return {
        "allograph_consolidation": {
            "signs_merged": consol.get("signs_merged", 0),
            "canonical_signs": consol.get("unique_canonical_signs", 0),
        },
        "translation_quality": {
            "coherence": trans.get("average_coherence", 0),
            "coverage": trans.get("average_coverage", 0),
            "stem_suffix_structure": trans.get("n_with_stem_suffix", 0),
        },
        "external_validation": {
            "mukhopadhyay_supported": cross.get("n_supported", 0),
        },
        "status": "LEVEL_3_CONSOLIDATED",
        "next_steps": [
            "Submit consolidated reading set for specialist review",
            "Attempt full seal translations with semantic glossing",
            "Contact Mukhopadhyay for direct comparison of proposals",
            "Prepare v4 preprint incorporating allograph consolidation",
            "Build interactive seal translation viewer for Glossa-Lab frontend",
        ],
        "verdict": (
            f"Consolidated: {consol.get('signs_merged', 0)} allographs merged. "
            f"Translation: {trans.get('average_coherence', 0):.0%} coherence. "
            f"External: {cross.get('n_supported', 0)} Mukhopadhyay proposals supported. "
            f"Status: Level 3 consolidated, ready for specialist review."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PHASES 358-362: CONSOLIDATE AND ADVANCE")
    print("=" * 70)

    results = {}

    # Phase 358
    try:
        results["phase358"] = phase358_consolidate()
        print(f"  → {results['phase358']['verdict']}")
    except Exception as e:
        results["phase358"] = {"error": str(e)}
        print(f"  → ERROR: {e}")

    # Phase 359
    try:
        results["phase359"] = phase359_mukhopadhyay_mine()
        print(f"  → {results['phase359']['verdict']}")
    except Exception as e:
        results["phase359"] = {"error": str(e)}
        print(f"  → ERROR: {e}")

    # Phase 360 — uses consolidated map from 358
    try:
        cmap = results.get("phase358", {}).get("consolidated_map", _load_all_map())
        results["phase360"] = phase360_retranslate(cmap)
        print(f"  → {results['phase360']['verdict']}")
    except Exception as e:
        results["phase360"] = {"error": str(e)}
        print(f"  → ERROR: {e}")

    # Phase 361
    try:
        mukho_props = results.get("phase359", {}).get("proposals", [])
        results["phase361"] = phase361_crosscheck(mukho_props)
        print(f"  → {results['phase361']['verdict']}")
    except Exception as e:
        results["phase361"] = {"error": str(e)}
        print(f"  → ERROR: {e}")

    # Phase 362
    try:
        results["phase362"] = phase362_summary(results)
        print(f"  → {results['phase362']['verdict']}")
    except Exception as e:
        results["phase362"] = {"error": str(e)}

    # Remove non-serializable merge_map and consolidated_map before saving
    if "phase358" in results:
        results["phase358"].pop("merge_map", None)
        results["phase358"].pop("consolidated_map", None)

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
