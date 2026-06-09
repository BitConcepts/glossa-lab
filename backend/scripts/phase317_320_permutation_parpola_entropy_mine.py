"""Phase 317-320: Permutation Null + Parpola Cross-Check + Reading Entropy + Deep Mine

Phase 317: Permutation null test — shuffle reading assignments 1000x,
           measure grammar conformance each time. Proves 91.8% is
           significantly above chance (or not).
Phase 318: Parpola reading cross-check — compare our 400 HIGH readings
           against Parpola's classic sign-value proposals.
Phase 319: Reading-level conditional entropy — does decoded text behave
           like language or like an administrative code?
Phase 320: Deep mine for Tamil-Brahmi formulas, Old Tamil serial case
           constructions, and Parpola 2010 sign values.

Output: outputs/phase317_320_permutation_parpola_entropy_mine.json
"""
from __future__ import annotations
import csv
import json
import math
import random
import urllib.request
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = (
    REPO / "corpora" / "downloads" / "external_repos"
    / "holdatllc_indus" / "indus_corpus 2.csv"
)
OUT_PATH = REPO / "outputs" / "phase317_320_permutation_parpola_entropy_mine.json"

# PD categories and transitions (same as Phase 313)
PD_CATEGORIES = {
    "STEM": {"kol", "koḷ", "il", "iḷ", "ūr", "maṇ", "kaṇ", "pon", "kal",
             "nīr", "vaḷ", "tiru", "kōṉ", "yānai", "kaḷiṟu", "erutu",
             "puli", "māṉ", "nakaram", "vēḷ", "cēy", "mā", "veL",
             "kāṇṭāmirukam", "cem", "kuTam", "vil", "kalam",
             "ōṭu", "nēr", "cēr", "māṟ", "pōr", "oṉṟu/1",
             "taṇ", "ḷā", "nallavar", "ce"},
    "NUMBER": {"ar", "kaḷ"},
    "CASE": {"iN/in (genitive of)", "iṉ/locative", "āl", "ā/āl",
             "ōṭu/comitative", "ku", "ai"},
    "GENDER": {"aṉ", "an/aṇ", "ay", "ay/ā", "am", "am/neuter", "āṉ", "āṇ", "āḷ"},
    "CLITIC": {"ē", "um", "ō"},
    "VERB": {"kol/koḷ", "vē", "iṭ", "ta", "ci", "mu", "pa", "na",
             "ru", "tu", "tu/tū", "ka", "ka/kaṇ", "vi", "ku",
             "al", "su", "ki"},
}
VALID_TRANSITIONS = {
    "STEM":   {"GENDER", "NUMBER", "CASE", "CLITIC", "STEM", "VERB"},
    "NUMBER": {"CASE", "CLITIC", "STEM"},
    "CASE":   {"CLITIC", "STEM", "VERB"},
    "GENDER": {"CASE", "CLITIC", "STEM", "VERB", "GENDER"},
    "CLITIC": {"STEM", "VERB"},
    "VERB":   {"GENDER", "CASE", "CLITIC", "STEM", "VERB"},
}

ALL_READINGS = set()
for members in PD_CATEGORIES.values():
    ALL_READINGS |= members


def _categorize(reading):
    for cat, members in PD_CATEGORIES.items():
        if reading in members:
            return cat
    return "UNKNOWN"


def _load_anchors():
    return json.loads(ANCHORS_PATH.read_text("utf-8")).get("anchors", {})


def _load_inscriptions():
    inscriptions = []
    with open(HOLDAT_PATH, encoding="utf-8") as f:
        cur = None; signs = []
        for r in csv.DictReader(f):
            if r["cisi_number"] != cur:
                if signs: inscriptions.append(signs)
                cur = r["cisi_number"]; signs = []
            signs.append(r["letters"])
        if signs: inscriptions.append(signs)
    return inscriptions


def _grammar_conformance(sign_to_reading, inscriptions):
    """Compute PD grammar conformance for a given sign→reading mapping."""
    n_valid = n_invalid = 0
    for ins in inscriptions:
        readings = [sign_to_reading.get(s, "") for s in ins]
        for i in range(len(readings) - 1):
            r1, r2 = readings[i], readings[i + 1]
            if not r1 or not r2:
                continue
            cat1, cat2 = _categorize(r1), _categorize(r2)
            if cat1 == "UNKNOWN" or cat2 == "UNKNOWN":
                continue
            if cat2 in VALID_TRANSITIONS.get(cat1, set()):
                n_valid += 1
            else:
                n_invalid += 1
    total = n_valid + n_invalid
    return n_valid / total if total else 0


# ══════════════════════════════════════════════════════════════════════
# PHASE 317: PERMUTATION NULL TEST
# ══════════════════════════════════════════════════════════════════════

def phase317_permutation_null():
    """Shuffle readings across signs 1000 times, measure grammar conformance."""
    print("  Loading data...")
    anchors = _load_anchors()
    inscriptions = _load_inscriptions()

    # Build real mapping (HIGH only)
    real_map = {s: i["reading"] for s, i in anchors.items()
                if i.get("confidence") == "HIGH" and i.get("reading")}
    real_conformance = _grammar_conformance(real_map, inscriptions)
    print(f"  Real conformance: {real_conformance:.4f}")

    # Get list of signs and readings for shuffling
    signs = list(real_map.keys())
    readings = list(real_map.values())

    n_trials = 1000
    null_scores = []
    rng = random.Random(42)

    print(f"  Running {n_trials} permutation trials...")
    for trial in range(n_trials):
        shuffled_readings = list(readings)
        rng.shuffle(shuffled_readings)
        shuffled_map = dict(zip(signs, shuffled_readings))
        score = _grammar_conformance(shuffled_map, inscriptions)
        null_scores.append(score)
        if trial % 200 == 0:
            print(f"    Trial {trial}/{n_trials}...")

    null_mean = sum(null_scores) / len(null_scores)
    null_std = math.sqrt(sum((s - null_mean)**2 for s in null_scores) / len(null_scores))
    z_score = (real_conformance - null_mean) / null_std if null_std > 0 else float("inf")
    p_value = sum(1 for s in null_scores if s >= real_conformance) / len(null_scores)

    # Percentile
    rank = sum(1 for s in null_scores if s < real_conformance)
    percentile = rank / len(null_scores) * 100

    return {
        "real_conformance": round(real_conformance, 4),
        "null_mean": round(null_mean, 4),
        "null_std": round(null_std, 4),
        "null_min": round(min(null_scores), 4),
        "null_max": round(max(null_scores), 4),
        "z_score": round(z_score, 2),
        "p_value": p_value,
        "percentile": round(percentile, 1),
        "n_trials": n_trials,
        "verdict": (
            f"Real conformance {real_conformance:.1%} vs null mean {null_mean:.1%} "
            f"(std={null_std:.4f}). Z-score={z_score:.1f}, p={p_value:.4f}. "
            f"Percentile: {percentile:.1f}%. "
            + ("HIGHLY SIGNIFICANT — readings carry genuine PD morphological signal."
               if z_score > 3
               else "SIGNIFICANT — readings are above chance."
               if z_score > 2
               else "NOT SIGNIFICANT — conformance may be due to chance.")
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 318: PARPOLA READING CROSS-CHECK
# ══════════════════════════════════════════════════════════════════════

# Parpola's classic sign-value proposals (Parpola 1994, 2010)
PARPOLA_READINGS = {
    "M047": {"parpola": "mīn", "meaning": "fish/star", "source": "Parpola 1994"},
    "M048": {"parpola": "mīn", "meaning": "fish variant", "source": "Parpola 1994"},
    "M176": {"parpola": "kō/an", "meaning": "king/male suffix", "source": "Parpola 1994"},
    "M342": {"parpola": "jar/pot marker", "meaning": "terminal marker", "source": "Parpola 1994"},
    "M099": {"parpola": "kol/vil", "meaning": "bow/weapon", "source": "Parpola 1994"},
    "M001": {"parpola": "tōḷ", "meaning": "shoulder/man", "source": "Parpola 1994"},
    "M086": {"parpola": "oru/oṉṟu", "meaning": "one", "source": "Parpola 1994"},
    "M087": {"parpola": "veḷ/iraṇṭu", "meaning": "two/white", "source": "Parpola 1994"},
    "M088": {"parpola": "mūṉṟu", "meaning": "three", "source": "Parpola 1994"},
    "M091": {"parpola": "āṟu", "meaning": "six", "source": "Parpola 1994"},
    "M092": {"parpola": "ēḻu", "meaning": "seven", "source": "Parpola 1994"},
    "M060": {"parpola": "kāṇṭā-mṛga", "meaning": "unicorn/rhinoceros", "source": "Parpola 1994"},
    "M261": {"parpola": "muruku", "meaning": "deity/youth", "source": "Parpola 1994"},
    "M281": {"parpola": "piḷḷai", "meaning": "child/squirrel", "source": "Parpola 1994"},
    "M175": {"parpola": "katir", "meaning": "spindle/ray", "source": "Parpola 1994"},
    "M211": {"parpola": "kō", "meaning": "king/chieftain", "source": "Parpola 2010"},
    "M124": {"parpola": "kuṭam", "meaning": "pot/water vessel", "source": "Parpola 1994"},
    "M117": {"parpola": "ar/cakra", "meaning": "wheel/circle", "source": "Parpola 1994"},
    "M233": {"parpola": "ūr", "meaning": "village/settlement", "source": "Parpola 1994"},
    "M162": {"parpola": "il", "meaning": "house", "source": "Parpola 2010"},
}


def phase318_parpola_crosscheck():
    """Compare our HIGH readings against Parpola's classic proposals."""
    anchors = _load_anchors()

    agreements = []
    partial_agreements = []
    contradictions = []
    no_our_reading = []

    for sign_id, parpola_info in PARPOLA_READINGS.items():
        our_anchor = anchors.get(sign_id, {})
        our_reading = our_anchor.get("reading", "")
        our_conf = our_anchor.get("confidence", "")
        parpola_reading = parpola_info["parpola"]

        if not our_reading:
            no_our_reading.append(sign_id)
            continue

        # Check agreement (allow partial matches)
        our_clean = our_reading.lower().split("/")[0].strip()
        par_clean = parpola_reading.lower().split("/")[0].strip()

        if our_clean == par_clean or our_reading == parpola_reading:
            agreements.append({
                "sign": sign_id, "our": our_reading,
                "parpola": parpola_reading, "match": "EXACT",
            })
        elif our_clean[:3] == par_clean[:3] or par_clean in our_reading.lower():
            partial_agreements.append({
                "sign": sign_id, "our": our_reading,
                "parpola": parpola_reading, "match": "PARTIAL",
            })
        else:
            contradictions.append({
                "sign": sign_id, "our": our_reading,
                "parpola": parpola_reading, "match": "DISAGREE",
            })

    total_compared = len(agreements) + len(partial_agreements) + len(contradictions)
    agreement_rate = (len(agreements) + len(partial_agreements)) / total_compared if total_compared else 0

    return {
        "parpola_signs_checked": len(PARPOLA_READINGS),
        "exact_agreements": len(agreements),
        "partial_agreements": len(partial_agreements),
        "contradictions": len(contradictions),
        "no_reading": len(no_our_reading),
        "agreement_rate": round(agreement_rate, 4),
        "agreements": agreements,
        "partial": partial_agreements,
        "contradictions_detail": contradictions,
        "verdict": (
            f"Parpola cross-check: {len(agreements)} exact + {len(partial_agreements)} partial "
            f"agreements out of {total_compared} compared ({agreement_rate:.0%}). "
            f"{len(contradictions)} contradictions. "
            + ("STRONG agreement with Parpola's independent proposals."
               if agreement_rate >= 0.50
               else "MODERATE agreement."
               if agreement_rate >= 0.25
               else "WEAK agreement — readings diverge significantly from Parpola.")
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 319: READING-LEVEL CONDITIONAL ENTROPY
# ══════════════════════════════════════════════════════════════════════

def phase319_reading_entropy():
    """Compute conditional entropy on decoded reading sequences.

    Compare against:
    - Rao et al. 2009 sign-level entropy: 3.23 bits
    - Natural languages: 2-4 bits
    - Random: ~log2(vocab)
    """
    anchors = _load_anchors()
    inscriptions = _load_inscriptions()
    high = {s: i["reading"] for s, i in anchors.items()
            if i.get("confidence") == "HIGH" and i.get("reading")}

    # Build reading sequences
    reading_seqs = []
    for ins in inscriptions:
        readings = [high.get(s, "") for s in ins]
        clean = [r for r in readings if r]
        if len(clean) >= 2:
            reading_seqs.append(clean)

    # Unigram entropy
    all_readings = [r for seq in reading_seqs for r in seq]
    freq = Counter(all_readings)
    total = sum(freq.values())
    h1 = -sum((c/total) * math.log2(c/total) for c in freq.values() if c > 0)

    # Bigram conditional entropy H(R_i | R_{i-1})
    bigram_freq = Counter()
    for seq in reading_seqs:
        for i in range(len(seq) - 1):
            bigram_freq[(seq[i], seq[i+1])] += 1

    bi_total = sum(bigram_freq.values())
    h2 = 0.0
    if bi_total > 0:
        joint_h = -sum(
            (c / bi_total) * math.log2(c / bi_total)
            for c in bigram_freq.values() if c > 0
        )
        h2 = joint_h - h1  # H(X,Y) - H(X) = H(Y|X)

    # Sign-level entropy for comparison
    sign_flat = [s for ins in inscriptions for s in ins]
    sign_freq = Counter(sign_flat)
    sign_total = sum(sign_freq.values())
    sign_h1 = -sum((c/sign_total) * math.log2(c/sign_total)
                    for c in sign_freq.values() if c > 0)

    sign_bigrams = Counter()
    for ins in inscriptions:
        for i in range(len(ins) - 1):
            sign_bigrams[(ins[i], ins[i+1])] += 1
    sbi_total = sum(sign_bigrams.values())
    sign_h2 = 0.0
    if sbi_total > 0:
        sign_joint_h = -sum(
            (c / sbi_total) * math.log2(c / sbi_total)
            for c in sign_bigrams.values() if c > 0
        )
        sign_h2 = sign_joint_h - sign_h1

    # Random baseline: H = log2(vocab)
    vocab = len(freq)
    random_h1 = math.log2(vocab) if vocab > 1 else 0

    return {
        "reading_level": {
            "vocab_size": vocab,
            "h1_unigram": round(h1, 4),
            "h2_conditional": round(h2, 4),
            "random_h1": round(random_h1, 4),
            "compression_ratio": round(h1 / random_h1, 4) if random_h1 > 0 else 0,
        },
        "sign_level": {
            "vocab_size": len(sign_freq),
            "h1_unigram": round(sign_h1, 4),
            "h2_conditional": round(sign_h2, 4),
        },
        "reference_values": {
            "rao_2009_indus_h2": 3.23,
            "natural_language_range": "2-4 bits",
            "administrative_codes": "1-3 bits",
            "random_baseline": round(random_h1, 2),
        },
        "verdict": (
            f"Reading-level: H1={h1:.2f} bits, H2(conditional)={h2:.2f} bits "
            f"(vocab={vocab}). Sign-level: H1={sign_h1:.2f}, H2={sign_h2:.2f} "
            f"(vocab={len(sign_freq)}). Rao 2009 reference: H2=3.23. "
            f"Compression ratio: {h1/random_h1:.2f} (1.0=random, <0.7=structured). "
            + ("Reading entropy is in the LINGUISTIC range."
               if 2.0 <= h2 <= 4.5
               else "Reading entropy is in the ADMINISTRATIVE range."
               if h2 < 2.0
               else "Reading entropy is HIGHER than expected for language.")
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 320: DEEP TARGETED MINE
# ══════════════════════════════════════════════════════════════════════

def _search_openalex(query, n=20):
    url = (
        "https://api.openalex.org/works?"
        + urllib.parse.urlencode({
            "search": query, "per_page": n,
            "sort": "relevance_score:desc",
            "filter": "from_publication_date:2020-01-01",
        })
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        return [
            {"title": w.get("title", ""),
             "year": w.get("publication_year"),
             "authors": ", ".join(
                 a.get("author", {}).get("display_name", "")
                 for a in (w.get("authorships") or [])[:3]),
             "doi": w.get("doi", ""),
             "cited_by": w.get("cited_by_count", 0)}
            for w in data.get("results", [])
        ]
    except Exception as e:
        return [{"error": str(e)}]


def phase320_deep_mine():
    """Deep mine for 4 targeted topics based on latest findings."""
    print("    Mining targeted topics...")
    targets = {
        "tamil_brahmi_seal_formulas": (
            "Tamil-Brahmi inscription seal formula Keezhadi "
            "Kodumanal Arikamedu potter merchant guild"
        ),
        "old_tamil_case_serial": (
            "Old Tamil serial case construction double case "
            "suffix stacking agglutination Tolkappiyam"
        ),
        "parpola_indus_values": (
            "Parpola Indus script sign values phonetic readings "
            "fish miin comb rebus 2010 2020"
        ),
        "indus_guild_identity": (
            "Indus Valley seal guild identity profession craft "
            "specialist occupation trade mark"
        ),
    }

    results = {}
    total = 0
    for topic, query in targets.items():
        print(f"      {topic}...")
        papers = _search_openalex(query, n=15)
        good = [p for p in papers if "error" not in p]
        results[topic] = {
            "n_results": len(good),
            "papers": good[:8],
        }
        total += len(good)

    # Find strong hits
    strong = []
    for topic, data in results.items():
        for p in data["papers"]:
            t = (p.get("title") or "").lower()
            if any(k in t for k in [
                "tamil-brahmi", "keezhadi", "parpola", "indus seal",
                "guild", "craft", "dravidian", "agglutina", "tolkappiyam",
                "harappan", "case suffix", "case marking",
            ]):
                strong.append({
                    "topic": topic, "title": p["title"],
                    "authors": p["authors"], "year": p["year"],
                    "cited_by": p["cited_by"],
                })

    return {
        "topics_mined": len(targets),
        "total_papers": total,
        "strong_relevant": len(strong),
        "strong_papers": strong[:12],
        "by_topic": {
            t: {"n": d["n_results"],
                "top": d["papers"][0]["title"] if d["papers"] else "none"}
            for t, d in results.items()
        },
        "verdict": (
            f"Mined {total} papers across {len(targets)} topics. "
            f"{len(strong)} strongly relevant."
        ),
    }


# ══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("PHASE 317-320: PERMUTATION + PARPOLA + ENTROPY + MINE")
    print("=" * 60)

    print("\n── Phase 317: Permutation Null Test ──")
    p317 = phase317_permutation_null()
    print(f"  {p317['verdict']}")

    print("\n── Phase 318: Parpola Cross-Check ──")
    p318 = phase318_parpola_crosscheck()
    print(f"  {p318['verdict']}")

    print("\n── Phase 319: Reading-Level Entropy ──")
    p319 = phase319_reading_entropy()
    print(f"  {p319['verdict']}")

    print("\n── Phase 320: Deep Mine ──")
    p320 = phase320_deep_mine()
    print(f"  {p320['verdict']}")

    result = {
        "phase317_permutation": p317,
        "phase318_parpola": p318,
        "phase319_entropy": p319,
        "phase320_mine": p320,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
