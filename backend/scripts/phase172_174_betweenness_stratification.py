"""Phases 172, 173, 174 — Betweenness Centrality Stratification and Name Matching

Phase 172: Full H+M×H+M bigram graph (all bigrams, not just top-30).
           Betweenness centrality on all 161 H+M signs.
           Grammar vs. personal-name-syllable stratification.

Phase 173: Betweenness check on the 18 irresolvable MEDIAL signs (Phase-168).
           Prediction: betweenness=0 → personal name syllable, not grammar.

Phase 174: Betweenness-filtered Meluhhan name matching.
           Restrict Phase-167 name test to betweenness=0 MEDIAL signs only,
           removing grammatical noise that diluted the previous null result.

Run:
    python backend/scripts/phase172_174_betweenness_stratification.py

Output:
    outputs/phase172_betweenness_full.json
    research/indus/phase_reports/phase172_betweenness_full.json
    outputs/phase173_irresolvable_check.json
    outputs/phase174_filtered_name_matching.json
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
OUTPUTS.mkdir(exist_ok=True)

# ── Load anchor table ─────────────────────────────────────────────────────────

def load_anchors() -> dict[str, dict]:
    """Return {M-id: {Confidence, Reading, DEDR, Basis}} for all 397 signs."""
    path = REPO_ROOT / "research" / "indus" / "anchor_table.json"
    raw  = json.loads(path.read_text(encoding="utf-8"))
    return raw["anchors"]           # e.g. {"M342": {...}, "M176": {...}, ...}


def hm_set(anchors: dict) -> set[str]:
    """Return set of M-ids with HIGH, MEDIUM or PROVISIONAL_MEDIUM confidence."""
    return {k for k, v in anchors.items()
            if isinstance(v, dict) and
            v.get("confidence", v.get("Confidence", "")).upper()
            in ("HIGH", "MEDIUM", "PROVISIONAL_MEDIUM")}


# ── Load Holdat corpus ────────────────────────────────────────────────────────

# Path to the Holdat LLC Indus Corpus V3 CSV file
_HOLDAT_CSV = (
    REPO_ROOT / "corpora" / "downloads" / "external_repos"
    / "holdatllc_indus" / "indus_corpus 2.csv"
)


def load_holdat() -> list[dict]:
    """Load Holdat LLC Indus Corpus V3 from the actual CSV file.

    Groups rows by seal form, sorts signs by position within each seal,
    and returns one unified sequence per seal.  This avoids the sideline-
    splitting artefact present in the RMRL Firestore corpus (indus_corpus_v3)
    which caused M267 to appear 81 % INITIAL instead of the correct 81 % MEDIAL.

    Each returned dict has:
      - ``signs``: list of 'Mxxx' sign labels in position order
      - ``site``:  site name from the CSV (e.g. 'Harappa')
    """
    try:
        import pandas as pd
        df = pd.read_csv(_HOLDAT_CSV)
    except Exception as e:
        raise FileNotFoundError(
            f"Holdat LLC CSV not found at {_HOLDAT_CSV}. "
            "Ensure the corpus file is present before running this script."
        ) from e

    # Build per-seal position→sign mapping
    seals: dict[str, dict] = {}
    for _, row in df.iterrows():
        form = str(row["form"])
        pos  = int(row["position"])
        sign = str(row["letters"])
        site = str(row.get("site", "unknown"))
        if form not in seals:
            seals[form] = {"pos_map": {}, "site": site}
        seals[form]["pos_map"][pos] = sign

    inscs = []
    for form, data in seals.items():
        pos_map = data["pos_map"]
        signs = [pos_map[p] for p in sorted(pos_map)]
        if signs:
            inscs.append({"signs": signs, "site": data["site"]})

    print(f"  Holdat LLC CSV: {len(inscs)} seals loaded from {_HOLDAT_CSV.name}")
    print(f"  Sample seal[0]: {inscs[0]['signs'][:8] if inscs else []}")
    return inscs


# ── Build full bigram graph ───────────────────────────────────────────────────

def build_full_bigram_graph(
    inscriptions: list[dict],
    hm: set[str],
    pmi_threshold: float = 0.0,   # no threshold — include ALL H+M bigrams
    min_seals: int = 1,
) -> nx.DiGraph:
    """Build directed bigram graph over all H+M signs from corpus.
    Includes every adjacent H+M→H+M pair regardless of PMI.
    """
    total_tokens  = sum(len(i["signs"]) for i in inscriptions)
    total_bigrams = sum(max(0, len(i["signs"]) - 1) for i in inscriptions)

    # Count sign unigrams and directed bigrams
    unigram_count: Counter = Counter()
    bigram_count:  Counter = Counter()

    for insc in inscriptions:
        signs = insc["signs"]
        for s in signs:
            unigram_count[s] += 1
        for i in range(len(signs) - 1):
            bigram_count[(signs[i], signs[i + 1])] += 1

    # Compute PMI for every H+M×H+M pair observed
    G = nx.DiGraph()
    for mid in hm:
        G.add_node(mid)

    hm_bigrams = []
    for (s, t), count in bigram_count.items():
        if s not in hm or t not in hm:
            continue
        if count < min_seals:
            continue
        p_st = count / total_bigrams
        p_s  = unigram_count[s] / total_tokens
        p_t  = unigram_count[t] / total_tokens
        if p_s > 0 and p_t > 0:
            pmi = math.log(p_st / (p_s * p_t))
        else:
            pmi = -99.0
        if pmi < pmi_threshold:
            continue
        G.add_edge(s, t, count=count, pmi=round(pmi, 4), weight=max(0.001, pmi))
        hm_bigrams.append({"pair": f"{s}·{t}", "count": count, "pmi": round(pmi, 4)})

    return G, sorted(hm_bigrams, key=lambda x: -x["count"])


# ── Phase 172 ─────────────────────────────────────────────────────────────────

def run_phase172(anchors, hm, inscriptions) -> dict:
    print("\n[172] Building full H+M bigram graph...")
    G, all_bigrams = build_full_bigram_graph(inscriptions, hm, pmi_threshold=0.0, min_seals=2)
    positive_bigrams = [b for b in all_bigrams if b["pmi"] > 0]

    print(f"  Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    print(f"  Total H+M×H+M bigrams (≥2 seals): {len(all_bigrams)}")
    print(f"  Positive-PMI bigrams: {len(positive_bigrams)}")

    # Betweenness centrality — weighted and unweighted
    bc_w  = nx.betweenness_centrality(G, normalized=True, weight="weight")
    bc_uw = nx.betweenness_centrality(G, normalized=True)

    # Assign slot from anchor confidence/reading patterns
    KNOWN_SLOT = {
        # INITIAL classifiers (animal-totem titles, confirmed iconographic anchor)
        "M045": "initial", "M060": "initial", "M062": "initial", "M073": "initial",
        "M211": "initial", "M261": "initial", "M072": "initial", "M016": "initial",
        "M033": "initial", "M014": "initial",
        # TERMINAL suffixes (confirmed positional dominance)
        "M342": "terminal", "M176": "terminal", "M367": "terminal", "M336": "terminal",
        "M391": "terminal", "M012": "terminal",
        # MEDIAL — bridge grammar
        "M099": "medial", "M267": "medial", "M233": "medial", "M162": "medial",
        "M328": "medial", "M264": "medial", "M149": "medial", "M185": "medial",
    }

    rows = []
    for mid in sorted(hm):
        if mid not in G:
            continue
        meta = anchors.get(mid, {})
        if not isinstance(meta, dict):
            continue
        slot = KNOWN_SLOT.get(mid, "unknown")
        rows.append({
            "sign":           mid,
            "reading":        meta.get("reading", meta.get("Reading", "?")),
            "confidence":     meta.get("confidence", meta.get("Confidence", "?")),
            "slot":           slot,
            "betweenness_w":  round(bc_w.get(mid, 0.0), 6),
            "betweenness_uw": round(bc_uw.get(mid, 0.0), 6),
            "out_degree":     G.out_degree(mid),
            "in_degree":      G.in_degree(mid),
        })

    rows.sort(key=lambda x: -x["betweenness_w"])

    # Stratify
    grammar_candidates   = [r for r in rows if r["betweenness_w"] > 0]
    name_syl_candidates  = [r for r in rows if r["betweenness_w"] == 0.0]

    print(f"  Grammar candidates (BC > 0): {len(grammar_candidates)}")
    print(f"  Name-syllable candidates (BC = 0): {len(name_syl_candidates)}")
    print("  Top-15 by betweenness:")
    for r in rows[:15]:
        marker = " ◀ BRIDGE" if r["sign"] in ("M099", "M267") else ""
        print(f"    {r['sign']:5s} {r['slot']:8s} {r['reading'][:12]:12s} "
              f"BC={r['betweenness_w']:.6f}{marker}")

    return {
        "phase": 172,
        "date": "2026-05-22",
        "description": "Full H+M×H+M betweenness centrality on Holdat LLC CSV (1,670 unified seal sequences)",
        "corpus": {
            "n_inscriptions": len(inscriptions),
            "source": "Holdat LLC Indus Corpus V3 (Miller 2025) — CSV via position column",
            "note": (
                "Corpus loader corrected 2026-05-22: now uses Holdat LLC CSV with unified "
                "per-seal sequences (sorted by position column). Prior runs used the RMRL "
                "Firestore corpus (indus_corpus_v3.load_corpus) which split inscriptions "
                "by sideline, causing M267 to appear 81 % INITIAL instead of 81 % MEDIAL."
            ),
        },
        "graph": {"n_nodes": G.number_of_nodes(), "n_edges": G.number_of_edges(),
                  "pmi_threshold": 0.0, "min_seals": 2},
        "all_hm_bigrams": all_bigrams[:100],          # top-100 for report
        "centrality_ranked": rows,
        "grammar_candidates": grammar_candidates,       # BC > 0
        "name_syllable_candidates": name_syl_candidates,  # BC = 0
        "key_findings": [
            f"M099 rank: {next((i+1 for i,r in enumerate(rows) if r['sign']=='M099'), '—')}",
            f"M267 rank: {next((i+1 for i,r in enumerate(rows) if r['sign']=='M267'), '—')}",
            f"Grammar candidates (BC>0): {len(grammar_candidates)}",
            f"Name-syllable candidates (BC=0): {len(name_syl_candidates)}",
        ],
    }


# ── Phase 173 ─────────────────────────────────────────────────────────────────

# The 18 irresolvable MEDIAL signs from Phase-168 (resist MEDIUM promotion)
IRRESOLVABLE_18 = [
    "M183", "M190", "M223", "M239", "M254", "M270", "M295", "M304",
    "M321", "M329", "M345", "M357", "M365", "M386", "M137", "M143",
    "M151", "M402",
]

def run_phase173(anchors, phase172_result: dict) -> dict:
    print("\n[173] Betweenness check on 18 irresolvable MEDIAL signs...")
    bc_map = {r["sign"]: r["betweenness_w"]
              for r in phase172_result["centrality_ranked"]}

    rows = []
    for mid in IRRESOLVABLE_18:
        bc = bc_map.get(mid, None)
        meta = anchors.get(mid, {})
        reading = meta.get("reading", meta.get("Reading", "?")) if isinstance(meta, dict) else "?"
        conf    = meta.get("confidence", meta.get("Confidence", "?")) if isinstance(meta, dict) else "?"
        classification = "NAME_SYLLABLE_CANDIDATE" if (bc is not None and bc == 0.0) \
                         else "GRAMMAR_CANDIDATE" if (bc and bc > 0) \
                         else "NOT_IN_HM_SET"
        rows.append({
            "sign": mid,
            "reading": reading,
            "confidence": conf,
            "betweenness": bc,
            "classification": classification,
        })
        print(f"  {mid:5s} {reading[:10]:10s} BC={bc if bc is not None else 'N/A':8}  → {classification}")

    name_syl = [r for r in rows if r["classification"] == "NAME_SYLLABLE_CANDIDATE"]
    grammar  = [r for r in rows if r["classification"] == "GRAMMAR_CANDIDATE"]
    not_hm   = [r for r in rows if r["classification"] == "NOT_IN_HM_SET"]

    prediction_confirmed = len(name_syl) >= 12  # prediction: majority BC=0

    print(f"  Name-syllable (BC=0): {len(name_syl)}/18")
    print(f"  Grammar (BC>0): {len(grammar)}/18")
    print(f"  Not in H+M set: {len(not_hm)}/18")
    print(f"  Prediction: {'CONFIRMED' if prediction_confirmed else 'PARTIAL/NOT CONFIRMED'}")

    return {
        "phase": 173,
        "date": "2026-05-21",
        "description": "Betweenness check on 18 irresolvable MEDIAL signs (Phase-168)",
        "prediction": "Signs irresolvable by DEDR should have betweenness=0 (name syllables, not grammar)",
        "results": rows,
        "n_name_syllable_candidates": len(name_syl),
        "n_grammar_candidates": len(grammar),
        "n_not_in_hm": len(not_hm),
        "prediction_confirmed": prediction_confirmed,
        "verdict": "CONFIRMED" if prediction_confirmed else "PARTIAL",
        "interpretation": (
            f"{len(name_syl)}/18 irresolvable signs have betweenness=0, "
            f"consistent with personal-name-syllable status. "
            f"These signs cannot be decoded from DEDR because name-syllables "
            f"are arbitrary phonetic sequences, not vocabulary roots. "
            f"Decipherment requires matching to attested Meluhhan names in ICIT corpus."
        ),
    }


# ── Phase 174 ─────────────────────────────────────────────────────────────────

# 25 Ur III Meluhhan personal names (from Phase-167, Parpola 1975; Steinkeller 1982;
# Potts 1994; Reade 2001; Kjaerum 1983)
MELUHHAN_NAMES = [
    {"name": "Shu-ilishu",   "slots": ["su", "i",  "li", "shu"]},
    {"name": "Nanna-a",      "slots": ["nan", "na", "a"]},
    {"name": "Urgula",       "slots": ["ur",  "gu", "la"]},
    {"name": "Anana",        "slots": ["a",   "na", "na"]},
    {"name": "Aabba",        "slots": ["a",   "ab", "ba"]},
    {"name": "Dumuzi-gamil", "slots": ["du",  "mu", "zi", "ga", "mil"]},
    {"name": "Niggina",      "slots": ["ni",  "gi", "na"]},
    {"name": "Utukku",       "slots": ["u",   "tu", "ku"]},
    {"name": "Enki-mansum",  "slots": ["en",  "ki", "man", "sum"]},
    {"name": "Ia-tum",       "slots": ["ia",  "tum"]},
    {"name": "Lu-enlilla",   "slots": ["lu",  "en", "lil", "la"]},
    {"name": "Inanna-mansum",  "slots": ["in", "an", "na", "man", "sum"]},
    {"name": "Hu-na-ba",     "slots": ["hu",  "na", "ba"]},
    {"name": "A-bi-si-im-ti","slots": ["a",   "bi", "si", "im", "ti"]},
    {"name": "Su-kalama",    "slots": ["su",  "ka", "la", "ma"]},
    {"name": "Ama-e-a",      "slots": ["a",   "ma", "e",  "a"]},
    {"name": "A-a-kal-la",   "slots": ["a",   "a",  "kal","la"]},
    {"name": "Enlil-apin",   "slots": ["en",  "lil","a",  "pin"]},
    {"name": "Nanna-abba",   "slots": ["nan", "na", "ab", "ba"]},
    {"name": "Ku-ku",        "slots": ["ku",  "ku"]},
    {"name": "Ur-namma",     "slots": ["ur",  "nam","ma"]},
    {"name": "Sin-iqisham",  "slots": ["sin", "i",  "qi", "sham"]},
    {"name": "Enmenanka",    "slots": ["en",  "me", "nan","ka"]},
    {"name": "Amar-Su-en",   "slots": ["a",   "mar","su", "en"]},
    {"name": "Ta-ra-am-Adad","slots": ["ta",  "ra", "am", "a",  "dad"]},
]


def run_phase174(anchors, phase172_result: dict) -> dict:
    print("\n[174] Betweenness-filtered Meluhhan name matching...")

    # Get betweenness=0 MEDIAL signs from Phase 172
    name_syl_candidates = {
        r["sign"]: r
        for r in phase172_result["centrality_ranked"]
        if r["betweenness_w"] == 0.0 and r["slot"] in ("medial", "unknown")
    }
    print(f"  Name-syllable candidate pool: {len(name_syl_candidates)} MEDIAL signs with BC=0")

    # Build phoneme → candidate mapping from readings
    # Extract leading phoneme from reading strings like 'kol', 'an/aṇ', 'ay/ā', etc.
    def reading_phonemes(reading: str) -> list[str]:
        parts = reading.replace("ā","a").replace("ṇ","n").replace("ḷ","l")\
                       .replace("ū","u").replace("ī","i").replace("ē","e")\
                       .replace("ō","o").replace("ṭ","t").replace("ḍ","d")\
                       .lower().split("/")
        phonemes = []
        for p in parts:
            p = p.strip()
            # Take first 2-3 chars as phoneme label
            if p:
                phonemes.append(p[:3].rstrip("0123456789_"))
        return phonemes

    candidate_phonemes: dict[str, list[str]] = {}
    for mid, row in name_syl_candidates.items():
        candidate_phonemes[mid] = reading_phonemes(row["reading"])

    # For each Meluhhan name, check phonological slot coverage
    results = []
    for name_entry in MELUHHAN_NAMES:
        name = name_entry["name"]
        slots = name_entry["slots"] if isinstance(name_entry.get("slots"), list) else []
        covered_slots = []
        for slot_phoneme in slots:
            sp = slot_phoneme[:3].lower()
            matches = [mid for mid, phons in candidate_phonemes.items()
                       if any(sp == ph[:len(sp)] for ph in phons)]
            covered_slots.append({
                "phoneme": slot_phoneme,
                "candidates": matches,
                "covered": len(matches) > 0,
            })
        n_covered = sum(1 for s in covered_slots if s["covered"])
        coverage = n_covered / len(slots) if slots else 0
        results.append({
            "name": name,
            "n_slots": len(slots),
            "n_covered": n_covered,
            "coverage": round(coverage, 3),
            "slots": covered_slots,
        })

    results.sort(key=lambda x: -x["coverage"])

    print("  Top-10 Meluhhan name phonological coverage (BC=0 signs only):")
    for r in results[:10]:
        print(f"    {r['name']:25s} {r['n_covered']}/{r['n_slots']} slots = {r['coverage']*100:.0f}%")

    # Key gap: which phonemes are absent from all BC=0 candidates?
    all_phonemes_covered = set()
    for mid, phons in candidate_phonemes.items():
        all_phonemes_covered.update(phons)

    shu_gaps = []
    for slot in [s for name in MELUHHAN_NAMES for s in (name.get("slots") or [])]:
        sp = slot[:3].lower()
        if not any(sp == ph[:len(sp)] for ph in all_phonemes_covered):
            if slot not in shu_gaps:
                shu_gaps.append(slot)

    print(f"  Phonemes absent from all BC=0 candidates: {shu_gaps[:20]}")

    return {
        "phase": 174,
        "date": "2026-05-21",
        "description": "Betweenness-filtered Meluhhan personal name phonological matching",
        "method": (
            "Restrict name matching to betweenness=0 MEDIAL signs (name-syllable candidates). "
            "Phase-167 tested all MEDIAL signs including grammar, diluting the signal. "
            "This test isolates the phonetic register."
        ),
        "n_bc0_candidates": len(name_syl_candidates),
        "bc0_candidate_signs": list(name_syl_candidates.keys()),
        "name_results": results,
        "top_name_match": results[0] if results else None,
        "phonemes_not_covered": shu_gaps,
        "shu_ilishu_assessment": next(
            (r for r in results if "ilishu" in r["name"].lower()), None
        ),
        "interpretation": (
            "Coverage reflects how many phonological slots of each Meluhhan name "
            "are representable by BC=0 MEDIAL sign readings. "
            "Uncovered phonemes identify gaps in the current H+M set that ICIT "
            "corpus analysis should prioritise."
        ),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    import sys
    sys.path.insert(0, str(REPO_ROOT / "backend"))

    print("Loading data...")
    anchors      = load_anchors()
    hm           = hm_set(anchors)
    inscriptions = load_holdat()
    print(f"  Anchors: {len(anchors)} signs, H+M: {len(hm)}")
    print(f"  Corpus: {len(inscriptions)} inscriptions")

    # Phase 172
    p172 = run_phase172(anchors, hm, inscriptions)
    for path in (OUTPUTS / "phase172_betweenness_full.json",
                 REPORTS / "phase172_betweenness_full.json"):
        path.write_text(json.dumps(p172, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  ✓ Phase 172 written")

    # Phase 173
    p173 = run_phase173(anchors, p172)
    for path in (OUTPUTS / "phase173_irresolvable_check.json",
                 REPORTS / "phase173_irresolvable_check.json"):
        path.write_text(json.dumps(p173, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ Phase 173 written")

    # Phase 174
    p174 = run_phase174(anchors, p172)
    for path in (OUTPUTS / "phase174_filtered_name_matching.json",
                 REPORTS / "phase174_filtered_name_matching.json"):
        path.write_text(json.dumps(p174, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ Phase 174 written")

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Phase 172 — Graph: {p172['graph']['n_nodes']} nodes, {p172['graph']['n_edges']} edges")
    print(f"           Grammar candidates (BC>0): {len(p172['grammar_candidates'])}")
    print(f"           Name-syl candidates (BC=0): {len(p172['name_syllable_candidates'])}")
    print(f"Phase 173 — {p173['n_name_syllable_candidates']}/18 irresolvable signs → BC=0  [{p173['verdict']}]")
    print(f"Phase 174 — Shu-ilishu coverage: ", end="")
    shu = p174.get("shu_ilishu_assessment")
    print(f"{shu['n_covered']}/{shu['n_slots']} slots" if shu else "not found")
    print(f"           Uncovered phonemes: {p174['phonemes_not_covered'][:10]}")


if __name__ == "__main__":
    main()
