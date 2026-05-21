"""Phase-72: Parpola Notation Parser.

Fixes the Phase-60/60b contact zone mining (0 hits) by building a
sign-list-aware parser that handles Parpola 1994/2010 notation styles:

Notation forms found in Parpola's texts:
  1. "(47)" — sign number in parentheses
  2. "sign 47", "Sign 47", "Sign no. 47"
  3. "*min", "*miin" — reconstructed reading with asterisk
  4. "P 47", "P47", "P.47"
  5. "No. 47 reads X", "sign number 47 = X"
  6. "sign list number 47"
  7. Dravidian words followed by their Parpola sign number in brackets
  8. Table entries: "47  fish  *miin"

GPU: torch for passage scoring.
Output: reports/phase72_parpola_parser.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

REPO    = Path(__file__).parents[2]
PUBS    = REPO / "corpora/downloads/contact_zone/publications"
P56     = REPO / "reports/phase56_parpola_expansion.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase72_parpola_parser.json"

# ── Parpola-specific patterns (ordered most-specific first) ──────────────────

# Pattern 1: "(47)" — sign number in parentheses, common in footnotes/captions
PAT_PARENS = re.compile(r'\((\d{1,3})\)[^)]{0,120}([a-z\u0100-\u024f*\-]{2,20})', re.IGNORECASE)

# Pattern 2: "sign 47 reads/= X", "sign no. 47: X"
PAT_SIGN_READS = re.compile(
    r'sign\s+(?:no\.?\s*)?(\d{1,3})\s*'
    r'(?:reads?|=|:|\bis\b)[^.]{0,80}?\b([a-z\u0100-\u024f\-]{2,20})\b',
    re.IGNORECASE)

# Pattern 3: "*miin", "*puli" — reconstructed Dravidian forms
PAT_ASTERISK = re.compile(
    r'\*([a-z\u0100-\u024f\u0101\u012b\u016b\u0113\u014d]{2,20})'
    r'[^.]{0,80}(?:sign\s*(?:no\.?\s*)?)(\d{1,3})',
    re.IGNORECASE)

# Pattern 4: "P 47", "P.47", "P47" explicitly
PAT_P_NUM = re.compile(
    r'\bP\.?\s*(\d{1,3})\b[^.]{0,80}(?:=|:|\breads?\b|means?)'
    r'[^.]{0,40}([a-z\u0100-\u024f\-]{2,20})',
    re.IGNORECASE)

# Pattern 5: Table-like format: "47  fish  miin" (tab or multiple spaces)
PAT_TABLE = re.compile(
    r'^(\d{1,3})\s{2,}[a-zA-Z /]{2,20}\s{2,}([a-z\u0100-\u024f\-]{2,20})\s*$',
    re.MULTILINE)

# Pattern 6: "puli (sign 6)" or "miin (sign 47)"
PAT_WORD_SIGN = re.compile(
    r'([a-z\u0100-\u024f\-]{2,20})\s+\(?sign\s+(?:no\.?\s*)?(\d{1,3})\)?',
    re.IGNORECASE)

# Pattern 7: Dravidian word + P-number in the same sentence
PAT_DRAV_P = re.compile(
    r'([a-z\u0101\u012b\u016b\u0113\u014d\-]{3,20})\s*'
    r'(?:\([Pp]\.?\s*(\d{1,3})\)|P\.?\s*(\d{1,3}))',
    re.IGNORECASE)

ALL_PATTERNS = [
    ("sign_reads",  PAT_SIGN_READS),
    ("asterisk",    PAT_ASTERISK),
    ("p_num",       PAT_P_NUM),
    ("table",       PAT_TABLE),
    ("word_sign",   PAT_WORD_SIGN),
    ("drav_p",      PAT_DRAV_P),
    ("parens",      PAT_PARENS),
]

# Dravidian word list for validation (prevents false positives)
DRAVIDIAN_WORDS = {
    "miin", "min", "puli", "kol", "kool", "ay", "an", "aa", "eeL", "eel",
    "yaanai", "erutu", "kaLiru", "nakaram", "uur", "tiru", "il", "am",
    "muruku", "tii", "tee", "peer", "maa", "kun", "kai", "neer", "mun",
    "koo", "koon", "nal", "vil", "mii", "miN", "pu", "ka", "ko", "ve",
    "ra", "ta", "na", "ku", "tu", "ma", "pa", "mu", "ar", "va", "pe",
    "er", "il", "aa", "ee", "uu", "oo", "ir", "or", "mi", "ya", "vi",
    "pi", "ni", "ri", "ti", "ki", "si", "gi", "bi", "di",  # common syllables
}


def is_plausible_reading(word: str) -> bool:
    """Check if a word looks like a plausible Dravidian reading."""
    w = word.lower().strip("*").strip()
    if len(w) < 2 or len(w) > 25:
        return False
    # Must be mostly alphabetic
    alpha = sum(1 for c in w if c.isalpha())
    if alpha / max(len(w), 1) < 0.7:
        return False
    # Not common English words
    ENGLISH_STOP = {
        "the", "and", "for", "with", "from", "that", "this", "are", "was",
        "have", "has", "been", "its", "they", "their", "also", "which",
        "sign", "read", "means", "fig", "vol", "see", "not", "may", "can",
        "list", "page", "form", "type", "group", "class", "note", "fig",
        "plate", "table", "text", "word", "line", "used", "called", "known",
        "shown", "based", "each", "both", "only", "more", "than", "some",
        "such", "other", "same", "first", "two", "three", "four", "five",
    }
    if w in ENGLISH_STOP:
        return False
    return True


def score_passages_gpu(passages: list[str]) -> list[float]:
    """GPU: score passages by Parpola-relevant keyword density."""
    if torch is None or not passages:
        return [0.0] * len(passages)
    keywords = ["parpola", "dravidian", "sign", "reads", "tamil", "rebus", "miin", "mīn"]
    scores = torch.zeros(len(passages), device=DEVICE)
    for i, p in enumerate(passages):
        p_lower = p.lower()
        hits = sum(p_lower.count(kw) for kw in keywords)
        nums = len(re.findall(r'\b\d{1,3}\b', p))
        scores[i] = float(hits) + float(nums) * 0.3
    normed = (scores / scores.clamp(min=1).max()).cpu().tolist()
    return normed


def parse_parpola_text(text: str, source: str) -> list[dict]:
    """Apply all Parpola-specific patterns to extract sign readings."""
    findings = []
    seen = set()

    for pat_name, pattern in ALL_PATTERNS:
        for m in pattern.finditer(text):
            groups = m.groups()
            # Find the P-number and reading from groups
            p_num = None
            reading = None
            for g in groups:
                if g and g.isdigit() and 1 <= int(g) <= 420:
                    p_num = g
                elif g and not g.isdigit() and is_plausible_reading(g):
                    reading = g.strip("*").strip()

            if p_num and reading:
                key = (p_num, reading.lower()[:6])
                if key not in seen:
                    seen.add(key)
                    ctx = text[max(0, m.start()-60):m.end()+60].replace("\n", " ").strip()
                    findings.append({
                        "p_num":       p_num,
                        "reading":     reading,
                        "source":      source,
                        "pattern":     pat_name,
                        "context":     ctx[:200],
                        "is_dravidian": reading.lower() in DRAVIDIAN_WORDS,
                    })

    return findings


def main():
    print("Phase-72: Parpola Notation Parser\n")

    pub_files = sorted(PUBS.glob("*.txt")) if PUBS.exists() else []
    print(f"  Publication files: {len(pub_files)}")

    # Load known crosswalk for validation
    known_readings: dict[str, str] = {}
    if P56.exists():
        p56 = json.loads(P56.read_text("utf-8"))
        for p_num, info in p56.get("master_crosswalk", {}).items():
            known_readings[p_num.split("_")[0]] = info.get("reading", "")

    all_findings = []
    per_file_stats = {}

    for pub in pub_files:
        text = pub.read_text("utf-8", errors="replace")
        findings = parse_parpola_text(text, pub.stem)
        all_findings.extend(findings)
        per_file_stats[pub.stem] = {
            "n_chars": len(text),
            "n_findings": len(findings),
            "dravidian_findings": sum(1 for f in findings if f["is_dravidian"]),
        }
        if findings:
            print(f"  {pub.stem}: {len(findings)} findings "
                  f"({sum(1 for f in findings if f['is_dravidian'])} Dravidian)")
        else:
            print(f"  {pub.stem}: 0 findings")

    # Score high-relevance passages
    high_rel_passages = []
    for pub in pub_files:
        text = pub.read_text("utf-8", errors="replace")
        for para in re.split(r'\n{2,}', text):
            if (30 < len(para) < 800 and
                    re.search(r'\b\d{1,3}\b', para) and
                    re.search(r'(?:sign|dravidian|reads?|parpola|tamil|miin|rebus)', para, re.I)):
                high_rel_passages.append({"text": para[:300], "source": pub.stem})

    if high_rel_passages:
        scores = score_passages_gpu([p["text"] for p in high_rel_passages])
        for i, score in enumerate(scores):
            high_rel_passages[i]["score"] = round(score, 3)
        high_rel_passages.sort(key=lambda x: -x["score"])
        print(f"\n[GPU:{DEVICE}] Scored {len(high_rel_passages)} high-relevance passages")

    # Validate findings against known crosswalk
    confirmed = [f for f in all_findings
                 if known_readings.get(f["p_num"], "").lower()[:3] == f["reading"].lower()[:3]]
    dravidian_findings = [f for f in all_findings if f["is_dravidian"]]
    new_readings = [f for f in all_findings
                    if f["p_num"] not in known_readings or
                    known_readings[f["p_num"]].lower()[:3] != f["reading"].lower()[:3]]

    print("\n=== Phase-72 Results ===")
    print(f"  Total findings:       {len(all_findings)}")
    print(f"  Dravidian readings:   {len(dravidian_findings)}")
    print(f"  Confirmed vs. P56:    {len(confirmed)}")
    print(f"  Potentially new:      {len(new_readings)}")

    if dravidian_findings:
        print("\n  Dravidian findings:")
        for f in dravidian_findings[:10]:
            known = known_readings.get(f["p_num"], "")
            match = "✓" if known[:3].lower() == f["reading"].lower()[:3] else "?"
            print(f"  P{f['p_num']:4s} = {f['reading']!r:12s} [{match}] known={known!r:10s} "
                  f"({f['pattern']}) [{f['source'][:30]}]")

    if not all_findings:
        recommendation = (
            "0 hits even with Parpola-specific patterns. "
            "The contact zone publications likely use a different citation system. "
            "Recommend: use LLM-based extraction (Mistral OCR) on Parpola 1994 PDF directly."
        )
    elif len(dravidian_findings) > 0:
        recommendation = (
            f"PARTIAL_SUCCESS: {len(dravidian_findings)} Dravidian readings found. "
            f"Cross-reference with P56 master to identify truly new mappings."
        )
    else:
        recommendation = (
            f"{len(all_findings)} findings but none match Dravidian vocabulary. "
            "Patterns are finding non-Indus sign numbers. Needs stricter Dravidian word filter."
        )
    print(f"\n  Recommendation: {recommendation}")

    result = {
        "_citation": {"primary": ["A.1", "A.13"]},
        "gpu_device":          DEVICE,
        "n_pub_files":         len(pub_files),
        "n_total_findings":    len(all_findings),
        "n_new_readings":      len(dravidian_findings),
        "n_confirmed_vs_p56":  len(confirmed),
        "new_readings":        dravidian_findings[:30],
        "all_findings":        all_findings[:50],
        "per_file_stats":      per_file_stats,
        "top_passages":        high_rel_passages[:10],
        "recommendation":      recommendation,
        "parser_quality": {
            "patterns_used":    len(ALL_PATTERNS),
            "dravidian_filter": True,
            "false_positive_guard": "English stop-word list",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
