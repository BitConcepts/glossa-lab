"""Phase-47 T2: Contact Zone Publication Deep Mining.

Systematically mines all extracted publication texts in the contact zone for:
  1. Explicit phoneme/reading assignments for Indus signs
  2. Formula descriptions and seal sequence analyses
  3. References to Dravidian etymologies for IVC signs
  4. Trade seal context and identity-marker discussions
  5. Mentions of our 7 HIGH anchor signs and M267

Publications mined (all have .txt extractions in contact_zone/publications/):
  - parpola_1994a_deciphering_indus_script.txt     (141 KB)
  - parpola_2010_dravidian_solution.txt            (69 KB)
  - laursen_2010_westward_transmission_AAE.txt     (149 KB)
  - frenez_2018_private_person_public_persona.txt  (122 KB)
  - frenez_2020_indus_oman_trade.txt               (32 KB)
  - levit_2010_meluhha_etymology.txt               (134 KB)
  - vidale_2004_melammu_iv_meluhha_villages.txt    (69 KB)
  - vidale_desset_frenez_2021_jalalabad.txt        (1.4 KB)

GPU: torch for embedding-style batch text search over publication corpus.

Output: reports/phase47_t2_publication_mining.json
"""
from __future__ import annotations
import json, re
from collections import defaultdict
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None
    DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

REPO    = Path(__file__).parents[2]
PUBS    = REPO / "corpora/downloads/contact_zone/publications"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase47_t2_publication_mining.json"

# Sign IDs we're looking for mentions of
TARGET_SIGNS = {
    "M006": ["M006", "sign 6", "sign 364", "tiger sign", "puli"],
    "M016": ["M016", "sign 16", "young elephant", "kaḷiṟu", "kaliru"],
    "M045": ["M045", "sign 147", "elephant sign", "yānai", "yanai"],
    "M062": ["M062", "sign 126", "bull sign", "zebu sign", "erutu", "ēṟu"],
    "M099": ["M099", "sign 99", "sign 125", "kol", "hammer sign"],
    "M176": ["M176", "sign 176", "an sign", "aṇ", "masculine suffix"],
    "M342": ["M342", "sign 145", "ay sign", "āy"],
    "M267": ["M267", "sign 267", "particle", "copula", "connective sign"],
}

# Patterns for phoneme/reading extractions
READING_PATTERNS = [
    r"sign\s+\w+\s+(?:reads?|represents?|stands?\s+for|means?)\s+['\"]([^'\"]+)['\"]",
    r"['\"]([^'\"]{2,20})['\"]?\s+(?:reading|phoneme|phonological\s+value)",
    r"dravidian\s+word\s+['\"]([^'\"]+)['\"]",
    r"(?:proto-dravidian|old\s+tamil)\s+['\*\*]([^\s'\"*]{2,15})",
    r"(?:reads?|phoneme)\s+/([^/]{1,15})/",
    r"tamil\s+['\"]([a-zāēīōūṭḍṇḷṟṉñśṣ]{2,12})['\"]",
]

# Dravidian linguistics terms to find context around
DRAVIDIAN_TERMS = [
    "dravidian", "proto-dravidian", "old tamil", "tamil",
    "rebus", "phonogram", "logogram",
    "genitive", "suffix", "postposition", "copula",
    "identity", "trade seal", "merchant",
    "janabiyah", "gulf seal", "dilmun",
    "unicorn", "zebu", "elephant",
]

# Formula-related patterns
FORMULA_PATTERNS = [
    r"formula\s+(?:type|class|structure)",
    r"(?:initial|terminal|medial)\s+sign",
    r"seal\s+inscription\s+reads?",
    r"(?:title|name|owner)\s+(?:formula|sequence|reading)",
    r"classifier.*suffix",
    r"prefix.*title",
]


def extract_context(text: str, match: re.Match, window: int = 120) -> str:
    start = max(0, match.start() - window)
    end   = min(len(text), match.end() + window)
    return text[start:end].replace("\n", " ").strip()


def mine_publication(path: Path) -> dict:
    """Mine a single publication for all relevant content."""
    text = path.read_text("utf-8", errors="replace")
    total_chars = len(text)
    result: dict = {
        "file": path.name,
        "size_kb": round(total_chars / 1024, 1),
        "sign_mentions": {},
        "phoneme_readings": [],
        "dravidian_contexts": [],
        "formula_contexts": [],
        "high_value_passages": [],
    }

    # 1. Sign-specific mentions
    for sign_id, aliases in TARGET_SIGNS.items():
        mentions = []
        for alias in aliases:
            pat = re.compile(re.escape(alias), re.IGNORECASE)
            for m in pat.finditer(text):
                ctx = extract_context(text, m, 150)
                if ctx not in mentions and len(ctx) > 20:
                    mentions.append(ctx)
                    if len(mentions) >= 3:
                        break
        if mentions:
            result["sign_mentions"][sign_id] = mentions[:3]

    # 2. Explicit phoneme/reading extractions
    for pat_str in READING_PATTERNS:
        for m in re.finditer(pat_str, text, re.IGNORECASE):
            ctx = extract_context(text, m, 100)
            entry = {
                "reading": m.group(1) if m.lastindex else "",
                "context": ctx,
            }
            if entry["reading"] and entry not in result["phoneme_readings"]:
                result["phoneme_readings"].append(entry)
                if len(result["phoneme_readings"]) >= 10:
                    break

    # 3. Dravidian term contexts
    for term in DRAVIDIAN_TERMS[:8]:
        pat = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
        count = len(pat.findall(text))
        if count > 0:
            # Get 2 context snippets
            for m in pat.finditer(text):
                ctx = extract_context(text, m, 80)
                if ctx not in result["dravidian_contexts"] and len(ctx) > 30:
                    result["dravidian_contexts"].append(f"[{term}×{count}] {ctx}")
                    break

    # 4. Formula/structural contexts
    for pat_str in FORMULA_PATTERNS:
        for m in re.finditer(pat_str, text, re.IGNORECASE):
            ctx = extract_context(text, m, 120)
            if ctx not in result["formula_contexts"]:
                result["formula_contexts"].append(ctx)
                if len(result["formula_contexts"]) >= 5:
                    break

    # 5. High-value passages: paragraphs containing 3+ target items
    paras = re.split(r"\n{2,}", text)
    for para in paras:
        if len(para) < 50 or len(para) > 2000:
            continue
        hits = sum(
            1 for aliases in TARGET_SIGNS.values()
            for alias in aliases
            if alias.lower() in para.lower()
        )
        drv_hits = sum(1 for t in DRAVIDIAN_TERMS if t.lower() in para.lower())
        if hits >= 2 or (hits >= 1 and drv_hits >= 2):
            snippet = para.replace("\n", " ").strip()[:400]
            if snippet not in result["high_value_passages"]:
                result["high_value_passages"].append({
                    "sign_hits": hits,
                    "dravidian_hits": drv_hits,
                    "text": snippet,
                })
                if len(result["high_value_passages"]) >= 5:
                    break

    return result


def gpu_score_passages(all_passages: list[str]) -> list[float]:
    """Score passages by relevance using torch tensor ops."""
    if torch is None or not all_passages:
        return [1.0] * len(all_passages)

    # Build a simple term-frequency scoring on GPU
    terms = [t.lower() for t in (
        list(TARGET_SIGNS.keys()) +
        [a for aliases in TARGET_SIGNS.values() for a in aliases[:2]] +
        DRAVIDIAN_TERMS
    )]

    n = len(all_passages)
    scores = torch.zeros(n, device=DEVICE)

    for i, passage in enumerate(all_passages):
        p_lower = passage.lower()
        count = sum(1 for t in terms if t in p_lower)
        scores[i] = float(count)

    # Normalise
    max_s = scores.max().item()
    if max_s > 0:
        scores = scores / max_s
    print(f"[GPU:{DEVICE}] Scored {n} passages")
    return scores.cpu().tolist()


def main() -> None:
    print("Phase-47 T2: Contact Zone Publication Deep Mining\n")

    pub_files = sorted(PUBS.glob("*.txt"))
    print(f"Mining {len(pub_files)} publication texts:")
    for f in pub_files:
        print(f"  {f.name} ({f.stat().st_size // 1024} KB)")

    all_results = []
    all_high_value = []

    for pub in pub_files:
        print(f"\n  Mining {pub.name}…")
        r = mine_publication(pub)
        all_results.append(r)
        n_signs = len(r["sign_mentions"])
        n_readings = len(r["phoneme_readings"])
        n_formulas = len(r["formula_contexts"])
        n_hv = len(r["high_value_passages"])
        print(f"    Sign mentions: {n_signs} signs | Readings: {n_readings} | "
              f"Formulas: {n_formulas} | High-value passages: {n_hv}")
        for hv in r["high_value_passages"]:
            all_high_value.append({
                "source": pub.stem,
                **hv,
            })

    # Score all high-value passages with GPU
    texts = [hv["text"] for hv in all_high_value]
    scores = gpu_score_passages(texts)
    for hv, s in zip(all_high_value, scores):
        hv["relevance_score"] = round(s, 3)
    all_high_value.sort(key=lambda x: -x["relevance_score"])

    # Aggregate: which signs are most discussed across publications?
    sign_pub_count: dict[str, int] = defaultdict(int)
    for r in all_results:
        for sig in r["sign_mentions"]:
            sign_pub_count[sig] += 1

    # Aggregate all phoneme readings
    all_readings = []
    for r in all_results:
        for reading in r["phoneme_readings"]:
            all_readings.append({
                "source": r["file"],
                **reading,
            })

    # Deduplicate readings
    seen_readings = set()
    unique_readings = []
    for r in all_readings:
        key = r["reading"].lower().strip()[:20]
        if key not in seen_readings and len(key) > 1:
            seen_readings.add(key)
            unique_readings.append(r)

    print(f"\n=== Publication Mining Summary ===")
    print(f"Total publications: {len(all_results)}")
    print(f"Unique phoneme readings found: {len(unique_readings)}")
    print(f"High-value passages (multi-hit): {len(all_high_value)}")
    print(f"Sign mention frequency: {dict(sorted(sign_pub_count.items()))}")

    if all_high_value:
        print(f"\nTop passage:")
        print(f"  [{all_high_value[0]['source']}] {all_high_value[0]['text'][:150]}…")

    result = {
        "_citation": {
            "sources_mined": [f.name for f in pub_files],
            "total_kb": sum(f.stat().st_size for f in pub_files) // 1024,
        },
        "gpu_device": DEVICE,
        "per_publication": all_results,
        "aggregated": {
            "sign_mention_by_publication_count": dict(sign_pub_count),
            "unique_phoneme_readings": unique_readings[:30],
            "top_high_value_passages": all_high_value[:20],
        },
        "summary": {
            "n_publications": len(all_results),
            "n_unique_readings": len(unique_readings),
            "n_high_value_passages": len(all_high_value),
            "most_discussed_signs": sorted(sign_pub_count, key=lambda x: -sign_pub_count[x])[:5],
        },
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
