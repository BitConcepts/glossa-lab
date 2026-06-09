"""Phase 313-316: Grammar + Formulas + Scorecard + Literature Mine

Phase 313: Proto-Dravidian grammar validation — test whether reading
           bigrams obey PD suffix ordering (Krishnamurti 2003).
Phase 314: Seal formula template mining — extract recurring patterns,
           classify by guild-identity model slots.
Phase 315: Nair 2026 scorecard — test decoded corpus against 4 structural
           metrics (brevity, repetition, hapax, positional rigidity).
Phase 316: Targeted literature mine for PD morphology, Keezhadi, new
           computational approaches, Mukhopadhyay updates.

Output: outputs/phase313_316_grammar_formulas_scorecard_mine.json
"""
from __future__ import annotations
import csv
import json
import math
import re
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
OUT_PATH = REPO / "outputs" / "phase313_316_grammar_formulas_scorecard_mine.json"


def _load_anchors():
    raw = json.loads(ANCHORS_PATH.read_text("utf-8"))
    return raw.get("anchors", {})


def _load_corpus():
    """Load Holdat as list of inscriptions (list of sign lists)."""
    inscriptions = []
    with open(HOLDAT_PATH, encoding="utf-8") as f:
        cur_seal = None
        cur_signs = []
        for r in csv.DictReader(f):
            if r["cisi_number"] != cur_seal:
                if cur_signs:
                    inscriptions.append(cur_signs)
                cur_seal = r["cisi_number"]
                cur_signs = []
            cur_signs.append(r["letters"])
        if cur_signs:
            inscriptions.append(cur_signs)
    return inscriptions


# ══════════════════════════════════════════════════════════════════════
# PHASE 313: PROTO-DRAVIDIAN GRAMMAR VALIDATION
# ══════════════════════════════════════════════════════════════════════

# Proto-Dravidian morphological categories (Krishnamurti 2003, Ch. 7-8)
# In PD agglutination, suffixes follow this order:
#   STEM + (number) + (case) + (emphasis/clitic)
# Nominal: stem-oblique-case; stem-number-case
# Valid transitions between morpheme types:
PD_CATEGORIES = {
    # Stems (nouns, titles, professions)
    "STEM": {"kol", "koḷ", "il", "iḷ", "ūr", "maṇ", "kaṇ", "pon", "kal",
             "nīr", "vaḷ", "tiru", "kōṉ", "yānai", "kaḷiṟu", "erutu",
             "puli", "māṉ", "nakaram", "vēḷ", "cēy", "mā", "veL",
             "kāṇṭāmirukam", "cem", "kuTam", "vil", "kalam",
             "ōṭu", "nēr", "cēr", "māṟ", "pōr", "oṉṟu/1",
             "taṇ", "ḷā", "nallavar", "ce"},
    # Number markers
    "NUMBER": {"ar", "kaḷ"},
    # Case suffixes
    "CASE": {"iN/in (genitive of)", "iṉ/locative", "āl", "ā/āl",
             "ōṭu/comitative", "ku", "ai"},
    # Gender/class suffixes
    "GENDER": {"aṉ", "an/aṇ", "ay", "ay/ā", "am", "am/neuter", "āṉ", "āṇ", "āḷ"},
    # Clitics / emphasis
    "CLITIC": {"ē", "um", "ō"},
    # Verbal roots (rare on seals)
    "VERB": {"kol/koḷ", "vē", "iṭ", "ta", "ci", "mu", "pa", "na",
             "ru", "tu", "tu/tū", "ka", "ka/kaṇ", "vi", "ku",
             "al", "su", "ki"},
}

# Valid PD bigram transitions (Krishnamurti 2003 Ch. 7-8):
VALID_TRANSITIONS = {
    "STEM":   {"GENDER", "NUMBER", "CASE", "CLITIC", "STEM", "VERB"},
    "NUMBER": {"CASE", "CLITIC", "STEM"},
    "CASE":   {"CLITIC", "STEM", "VERB"},
    "GENDER": {"CASE", "CLITIC", "STEM", "VERB", "GENDER"},
    "CLITIC": {"STEM", "VERB"},
    "VERB":   {"GENDER", "CASE", "CLITIC", "STEM", "VERB"},
}


def _categorize(reading: str) -> str:
    for cat, members in PD_CATEGORIES.items():
        if reading in members:
            return cat
    return "UNKNOWN"


def phase313_grammar_validation():
    """Test reading bigrams against PD suffix ordering rules."""
    anchors = _load_anchors()
    inscriptions = _load_corpus()
    high = {s: i for s, i in anchors.items()
            if i.get("confidence") == "HIGH" and i.get("reading")}

    n_valid = 0
    n_invalid = 0
    n_unknown = 0
    violations = Counter()
    valid_patterns = Counter()

    for ins in inscriptions:
        readings = [high.get(s, {}).get("reading", "") for s in ins]
        for i in range(len(readings) - 1):
            r1, r2 = readings[i], readings[i + 1]
            if not r1 or not r2:
                continue
            cat1 = _categorize(r1)
            cat2 = _categorize(r2)
            if cat1 == "UNKNOWN" or cat2 == "UNKNOWN":
                n_unknown += 1
                continue
            if cat2 in VALID_TRANSITIONS.get(cat1, set()):
                n_valid += 1
                valid_patterns[(cat1, cat2)] += 1
            else:
                n_invalid += 1
                violations[(cat1, cat2, r1, r2)] += 1

    total = n_valid + n_invalid
    conformance = n_valid / total if total else 0

    return {
        "total_bigrams_tested": total,
        "valid": n_valid,
        "invalid": n_invalid,
        "unknown_category": n_unknown,
        "conformance_rate": round(conformance, 4),
        "top_valid_patterns": [
            {"pattern": f"{a}->{b}", "count": c}
            for (a, b), c in valid_patterns.most_common(10)
        ],
        "top_violations": [
            {"pattern": f"{a}->{b}", "example": f"{r1}+{r2}", "count": c}
            for (a, b, r1, r2), c in violations.most_common(10)
        ],
        "verdict": (
            f"PD grammar conformance: {conformance:.1%} ({n_valid}/{total} bigrams). "
            f"{n_invalid} violations, {n_unknown} uncategorized. "
            + ("STRONG conformance — readings follow PD suffix ordering."
               if conformance >= 0.75
               else "MODERATE conformance — some violations need investigation."
               if conformance >= 0.50
               else "WEAK conformance — significant deviation from PD rules.")
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 314: SEAL FORMULA TEMPLATE MINING
# ══════════════════════════════════════════════════════════════════════

def phase314_formula_mining():
    """Extract recurring reading-level formulas from decoded seals."""
    anchors = _load_anchors()
    inscriptions = _load_corpus()
    high = {s: i for s, i in anchors.items()
            if i.get("confidence") == "HIGH" and i.get("reading")}

    # Translate all inscriptions to reading sequences
    reading_seqs = []
    for ins in inscriptions:
        readings = tuple(high.get(s, {}).get("reading", "?") for s in ins)
        if all(r != "?" for r in readings):
            reading_seqs.append(readings)

    print(f"    Fully decoded inscriptions: {len(reading_seqs)}")

    # Count reading-level n-grams (formulas)
    bigrams = Counter()
    trigrams = Counter()
    tetragrams = Counter()
    for seq in reading_seqs:
        for i in range(len(seq) - 1):
            bigrams[seq[i:i+2]] += 1
        for i in range(len(seq) - 2):
            trigrams[seq[i:i+3]] += 1
        for i in range(len(seq) - 3):
            tetragrams[seq[i:i+4]] += 1

    # Classify formulas by guild-identity model slots
    def _classify_formula(formula):
        cats = [_categorize(r) for r in formula]
        pattern = "->".join(cats)

        if cats[0] == "STEM" and any(c == "GENDER" for c in cats[1:]):
            return "TITLE+SUFFIX"
        if any(c == "VERB" for c in cats) and any(c == "GENDER" for c in cats):
            return "PROFESSION+SUFFIX"
        if "STEM" in cats and "CASE" in cats:
            return "PLACE+CASE"
        if all(c == "GENDER" for c in cats):
            return "SUFFIX_CHAIN"
        return "OTHER"

    classified_trigrams = []
    for formula, count in trigrams.most_common(30):
        classified_trigrams.append({
            "formula": " + ".join(formula),
            "count": count,
            "categories": "->".join(_categorize(r) for r in formula),
            "type": _classify_formula(formula),
        })

    # Most repeated full inscriptions (exact reading matches)
    full_seqs = Counter(reading_seqs)
    repeated = [(seq, c) for seq, c in full_seqs.most_common(20) if c >= 3]

    formula_types = Counter(f["type"] for f in classified_trigrams)

    return {
        "n_decoded_inscriptions": len(reading_seqs),
        "n_distinct_bigrams": len(bigrams),
        "n_distinct_trigrams": len(trigrams),
        "n_distinct_tetragrams": len(tetragrams),
        "top_bigrams": [
            {"formula": " + ".join(b), "count": c}
            for b, c in bigrams.most_common(10)
        ],
        "top_trigrams_classified": classified_trigrams[:15],
        "formula_type_distribution": dict(formula_types),
        "repeated_full_inscriptions": [
            {"reading": " ".join(s), "count": c, "length": len(s)}
            for s, c in repeated
        ],
        "n_repeated_formulas": len(repeated),
        "verdict": (
            f"{len(reading_seqs)} fully decoded inscriptions. "
            f"{len(bigrams)} distinct bigrams, {len(trigrams)} trigrams. "
            f"{len(repeated)} inscriptions repeated 3+ times. "
            f"Formula types: {dict(formula_types)}."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 315: NAIR 2026 SCORECARD
# ══════════════════════════════════════════════════════════════════════

def phase315_nair_scorecard():
    """Apply Nair's 4-metric discrimination scorecard to our corpus.

    Metrics from Nair 2026 (arXiv:2604.17828):
    1. Text brevity — mean inscription length
    2. Formulaic repetition — repeated phrases of length 3-6
    3. Hapax legomenon rate — fraction of signs appearing once
    4. Positional rigidity — Cramer's V for top-10 signs
    """
    inscriptions = _load_corpus()
    flat = [s for ins in inscriptions for s in ins]
    freq = Counter(flat)

    # Metric 1: Text brevity
    lengths = [len(ins) for ins in inscriptions]
    mean_length = sum(lengths) / len(lengths)
    median_length = sorted(lengths)[len(lengths) // 2]

    # Metric 2: Formulaic repetition (phrases of length 3-6 in 2+ inscriptions)
    repeat_counts = {}
    for n in [3, 4, 5, 6]:
        phrase_where = defaultdict(set)
        for idx, ins in enumerate(inscriptions):
            for i in range(len(ins) - n + 1):
                phrase = tuple(ins[i:i+n])
                phrase_where[phrase].add(idx)
        repeated = sum(1 for phrase, idxs in phrase_where.items() if len(idxs) >= 2)
        repeat_counts[n] = repeated

    # Metric 3: Hapax legomenon rate
    hapax = sum(1 for s, c in freq.items() if c == 1)
    hapax_rate = hapax / len(freq) if freq else 0

    # Metric 4: Positional rigidity (Cramer's V for top-10 signs)
    top10 = [s for s, _ in freq.most_common(10)]
    cramers = []
    total_ins = len(inscriptions)

    for sign in top10:
        # Count start/middle/end occurrences
        start = sum(1 for ins in inscriptions if ins and ins[0] == sign)
        end = sum(1 for ins in inscriptions if ins and ins[-1] == sign)
        middle = sum(1 for ins in inscriptions for s in ins[1:-1] if s == sign)
        total = start + middle + end
        if total < 5:
            continue

        # Expected under uniform distribution
        # Cramer's V approximation from positional preference
        positions = [start, middle, end]
        n = sum(positions)
        expected = n / 3
        chi2 = sum((o - expected) ** 2 / max(expected, 1) for o in positions)
        v = math.sqrt(chi2 / max(n * 2, 1))  # df = min(rows,cols)-1 = 2
        cramers.append({"sign": sign, "cramers_v": round(v, 4),
                         "start": start, "middle": middle, "end": end})

    mean_v = sum(c["cramers_v"] for c in cramers) / len(cramers) if cramers else 0

    # Nair's reference values (from paper)
    nair_ref = {
        "indus_corpus": {"mean_length": 4.4, "hapax_rate": 0.35,
                          "positional_rigidity": 0.45},
        "heraldic_baseline": {"mean_length": 4.4, "hapax_rate": 0.30,
                               "positional_rigidity": 0.25},
        "administrative_baseline": {"mean_length": 4.4, "hapax_rate": 0.20,
                                      "positional_rigidity": 0.35},
    }

    return {
        "metric1_brevity": {
            "mean_length": round(mean_length, 2),
            "median_length": median_length,
            "nair_indus": 4.4,
            "match": abs(mean_length - 4.4) < 1.0,
        },
        "metric2_repetition": {
            "repeated_phrases": repeat_counts,
            "nair_note": "Nair found Indus has moderate repetition, between heraldic and admin baselines",
        },
        "metric3_hapax": {
            "hapax_count": hapax,
            "vocab_size": len(freq),
            "hapax_rate": round(hapax_rate, 4),
            "nair_indus": 0.35,
            "match": abs(hapax_rate - 0.35) < 0.15,
        },
        "metric4_positional_rigidity": {
            "mean_cramers_v": round(mean_v, 4),
            "top10_details": cramers,
            "nair_indus": 0.45,
            "match": abs(mean_v - 0.45) < 0.20,
        },
        "scorecard_summary": {
            "our_metrics": {
                "mean_length": round(mean_length, 2),
                "hapax_rate": round(hapax_rate, 4),
                "positional_rigidity": round(mean_v, 4),
                "repeated_3grams": repeat_counts.get(3, 0),
            },
            "nair_indus_reference": nair_ref["indus_corpus"],
            "consistent_with_nair": (
                abs(mean_length - 4.4) < 1.0
                and abs(hapax_rate - 0.35) < 0.15
            ),
        },
        "verdict": (
            f"Scorecard: mean length {mean_length:.1f} (Nair: 4.4), "
            f"hapax rate {hapax_rate:.2f} (Nair: 0.35), "
            f"positional rigidity {mean_v:.3f} (Nair: 0.45). "
            f"Repeated 3-grams: {repeat_counts.get(3, 0)}. "
            + ("Our corpus is CONSISTENT with Nair's Indus measurements."
               if abs(mean_length - 4.4) < 1.0 and abs(hapax_rate - 0.35) < 0.15
               else "Some metrics DIVERGE from Nair's measurements.")
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# PHASE 316: TARGETED LITERATURE MINE
# ══════════════════════════════════════════════════════════════════════

def _search_openalex(query: str, n: int = 25) -> list[dict]:
    """Search OpenAlex for papers matching query."""
    url = (
        "https://api.openalex.org/works?"
        + urllib.parse.urlencode({
            "search": query,
            "per_page": n,
            "sort": "relevance_score:desc",
            "filter": "from_publication_date:2023-01-01",
        })
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        results = []
        for w in data.get("results", []):
            results.append({
                "title": w.get("title", ""),
                "year": w.get("publication_year"),
                "authors": ", ".join(
                    a.get("author", {}).get("display_name", "")
                    for a in (w.get("authorships") or [])[:3]
                ),
                "doi": w.get("doi", ""),
                "cited_by": w.get("cited_by_count", 0),
                "type": w.get("type", ""),
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]


def phase316_literature_mine():
    """Targeted mine for 5 specific research areas."""
    print("    Mining OpenAlex for targeted topics...")

    targets = {
        "pd_morphology": (
            "Proto-Dravidian morphology suffix agglutination "
            "case markers grammatical structure"
        ),
        "keezhadi_ivc": (
            "Keezhadi excavation Tamil Brahmi Indus Valley "
            "continuity archaeological"
        ),
        "mukhopadhyay_indus": (
            "Mukhopadhyay Indus script semasiographic "
            "logographic fish sign gemstone"
        ),
        "computational_indus": (
            "computational decipherment Indus script "
            "machine learning deep learning 2024 2025"
        ),
        "sangam_seals": (
            "Sangam Tamil seal coin vocabulary inscription "
            "proto-Dravidian trade guild"
        ),
    }

    mine_results = {}
    total_papers = 0

    for topic, query in targets.items():
        print(f"      Mining: {topic}...")
        papers = _search_openalex(query, n=20)
        mine_results[topic] = {
            "query": query,
            "n_results": len([p for p in papers if "error" not in p]),
            "papers": papers[:10],
        }
        total_papers += len([p for p in papers if "error" not in p])

    # Assess relevance
    strong = []
    for topic, data in mine_results.items():
        for p in data["papers"]:
            title = (p.get("title") or "").lower()
            if any(kw in title for kw in [
                "dravidian", "indus", "harappan", "keezhadi",
                "proto-dravidian", "agglutinati", "seal", "decipher",
            ]):
                strong.append({
                    "topic": topic,
                    "title": p.get("title"),
                    "authors": p.get("authors"),
                    "year": p.get("year"),
                    "cited_by": p.get("cited_by", 0),
                })

    return {
        "topics_mined": len(targets),
        "total_papers": total_papers,
        "strong_relevant": len(strong),
        "strong_papers": strong[:15],
        "by_topic": {
            topic: {"n_results": data["n_results"], "top_paper": data["papers"][0]["title"] if data["papers"] else "none"}
            for topic, data in mine_results.items()
        },
        "verdict": (
            f"Mined {total_papers} papers across {len(targets)} topics. "
            f"{len(strong)} strongly relevant papers found."
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("PHASE 313-316: GRAMMAR + FORMULAS + SCORECARD + MINE")
    print("=" * 60)

    print("\n── Phase 313: PD Grammar Validation ──")
    p313 = phase313_grammar_validation()
    print(f"  {p313['verdict']}")

    print("\n── Phase 314: Seal Formula Mining ──")
    p314 = phase314_formula_mining()
    print(f"  {p314['verdict']}")

    print("\n── Phase 315: Nair 2026 Scorecard ──")
    p315 = phase315_nair_scorecard()
    print(f"  {p315['verdict']}")

    print("\n── Phase 316: Literature Mine ──")
    p316 = phase316_literature_mine()
    print(f"  {p316['verdict']}")

    result = {
        "phase313_grammar": p313,
        "phase314_formulas": p314,
        "phase315_scorecard": p315,
        "phase316_mine": p316,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
