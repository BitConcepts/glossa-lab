"""Phase 351: Decipherment Advancement Mine

Now that convergence is at 6/6 strong (18/18), we pivot from
validation to ADVANCEMENT — pushing toward actual decipherment:

1. Mine for specific sign-reading proposals we haven't incorporated
2. Mine for seal formula interpretations and trade terminology
3. Mine for Tamil-Brahmi sign continuity (direct reading transfer)
4. Mine for Mesopotamian bilingual evidence (Meluhha personal names)
5. Mine for computational methods that could upgrade LOW→HIGH readings
6. Extract and test new reading candidates from all mined evidence

Output: outputs/phase351_advancement_mine.json
"""
from __future__ import annotations
import json
import re
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
OUT_PATH = REPO / "outputs" / "phase351_advancement_mine.json"


def _load_anchors():
    return json.loads(ANCHORS_PATH.read_text("utf-8")).get("anchors", {})


def _get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "GlossaLab/0.5 (research; tpierson@bitconcepts.tech)"
            })
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception:
            time.sleep(0.5 * (attempt + 1))
    return None


# ── Targeted advancement queries ─────────────────────────────────────

ADVANCEMENT_QUERIES = {
    "sign_readings": [
        "Indus script sign reading value proposal 2024 2025 2026",
        "Parpola Indus sign value update revised reading",
        "Mahadevan Indus sign identification reading Tamil",
        "Fairservis Indus sign meaning writing system",
        "Indus script fish sign reading star planet Dravidian",
        "Indus unicorn sign meaning kol bull vessel",
    ],
    "seal_formulas": [
        "Indus seal inscription formula template guild title",
        "Harappan seal text structure personal name title suffix",
        "Indus inscription tripartite structure classifier title name",
        "seal formula interpretation merchant guild identity Indus",
    ],
    "tamil_brahmi": [
        "Tamil Brahmi sign value phonetic reading aksara inventory",
        "Keezhadi Tamil Brahmi pottery graffiti personal name 2025 2026",
        "Tamil Brahmi hero stone name formula reading",
        "early Tamil writing Brahmi adaptation Indus continuity",
        "Mahadevan Tamil Brahmi personal name structure morphology",
    ],
    "meluhha_names": [
        "Meluhha personal name Akkadian cuneiform Shu-ilishu translation",
        "Meluhha merchant name Ur III Lagash cuneiform record",
        "Lu-Sunzida Meluhha man buffalo cow name translation",
        "Indus personal name structure seal owner identity",
    ],
    "computational": [
        "Bayesian decipherment undeciphered script reading upgrade 2025 2026",
        "neural network ancient script sign reading prediction",
        "transfer learning decipherment related script Tamil Brahmi",
        "machine learning sign classification reading assignment",
    ],
    "trade_vocabulary": [
        "Indus trade commodity seal marking weight standard",
        "Harappan craft specialist bead carnelian shell worker guild",
        "Dravidian trade vocabulary craft term loanword Sanskrit",
        "Indus seal economic administrative meaning function",
    ],
}

STRONG_PAT = [
    re.compile(r"(?:Indus|Harappan).*(?:sign|script).*(?:reading|value|meaning|phonet)", re.I),
    re.compile(r"(?:Tamil.Brahmi|Keezhadi).*(?:sign|reading|name|graffiti)", re.I),
    re.compile(r"Meluhha.*(?:name|personal|seal|interpreter|translate)", re.I),
    re.compile(r"(?:Parpola|Mahadevan|Fairservis|Wells).*(?:sign|reading|Indus)", re.I),
    re.compile(r"(?:seal|inscription).*(?:formula|template|guild|title|name)", re.I),
    re.compile(r"(?:Bayesian|neural|machine.learn).*(?:decipher|script|reading)", re.I),
    re.compile(r"(?:Dravidian|Tamil).*(?:trade|craft|loanword|vocabulary)", re.I),
]


def mine_advancement():
    """Mine across all advancement categories."""
    print("=" * 70)
    print("PHASE 351: DECIPHERMENT ADVANCEMENT MINE")
    print("=" * 70)

    all_papers = []
    category_counts = {}

    for category, queries in ADVANCEMENT_QUERIES.items():
        print(f"\n  [{category}] Mining {len(queries)} queries...")
        cat_papers = []

        for q in queries:
            enc = urllib.parse.quote(q)

            # OpenAlex
            url = (f"https://api.openalex.org/works?search={enc}"
                   f"&per-page=100&cursor=*"
                   f"&select=id,title,doi,publication_year,authorships,abstract_inverted_index"
                   f"&mailto=tpierson@bitconcepts.tech")
            data = _get_json(url)
            if data and "results" in data:
                for w in data["results"]:
                    title = w.get("title") or ""
                    abstract = ""
                    aii = w.get("abstract_inverted_index")
                    if aii:
                        pairs = sorted([(pos, word) for word, positions in aii.items()
                                       for pos in positions])
                        abstract = " ".join(w for _, w in pairs)

                    score = sum(3 for p in STRONG_PAT if p.search(f"{title} {abstract}"))
                    if score > 0:
                        authors = [a.get("author", {}).get("display_name", "")
                                  for a in (w.get("authorships") or [])[:5]]
                        cat_papers.append({
                            "title": title,
                            "doi": w.get("doi", ""),
                            "year": w.get("publication_year"),
                            "authors": [a for a in authors if a],
                            "score": score,
                            "category": category,
                            "abstract_snippet": abstract[:500],
                        })
            time.sleep(0.4)

            # Semantic Scholar for sign readings and computational
            if category in ("sign_readings", "computational", "tamil_brahmi"):
                s2_url = (f"https://api.semanticscholar.org/graph/v1/paper/search"
                          f"?query={enc}&limit=50&fields=title,authors,year,externalIds,abstract")
                s2_data = _get_json(s2_url)
                if s2_data:
                    for paper in s2_data.get("data", []):
                        title = paper.get("title") or ""
                        abstract = paper.get("abstract") or ""
                        score = sum(3 for p in STRONG_PAT if p.search(f"{title} {abstract}"))
                        if score > 0:
                            cat_papers.append({
                                "title": title,
                                "doi": (paper.get("externalIds") or {}).get("DOI", ""),
                                "year": paper.get("year"),
                                "authors": [a.get("name", "") for a in (paper.get("authors") or [])[:5]],
                                "score": score,
                                "category": category,
                                "abstract_snippet": (abstract or "")[:500],
                            })
                time.sleep(1.2)

        # Dedup within category
        seen = set()
        unique = []
        for p in sorted(cat_papers, key=lambda x: -x["score"]):
            norm = re.sub(r"\s+", " ", p["title"].lower().strip())
            if norm and norm not in seen:
                seen.add(norm)
                unique.append(p)

        category_counts[category] = len(unique)
        all_papers.extend(unique)
        print(f"    → {len(unique)} unique papers")

    # Global dedup
    seen = set()
    final = []
    for p in sorted(all_papers, key=lambda x: -x["score"]):
        norm = re.sub(r"\s+", " ", p["title"].lower().strip())
        if norm and norm not in seen:
            seen.add(norm)
            final.append(p)

    print(f"\n  Total unique papers: {len(final)}")

    # Extract advancement insights
    insights = {
        "new_sign_readings": [],
        "formula_patterns": [],
        "tamil_brahmi_links": [],
        "meluhha_evidence": [],
        "computational_methods": [],
        "trade_terms": [],
    }

    for p in final[:200]:
        text = f"{p.get('title', '')} {p.get('abstract_snippet', '')}".lower()

        if any(w in text for w in ["sign value", "reading propos", "phonetic value",
                                    "sign identif", "sign meaning"]):
            insights["new_sign_readings"].append({
                "title": p["title"], "year": p.get("year"),
                "authors": p.get("authors", [])[:3],
            })

        if any(w in text for w in ["seal formula", "guild title", "personal name",
                                    "inscription structure", "tripartite"]):
            insights["formula_patterns"].append({
                "title": p["title"], "year": p.get("year"),
            })

        if "tamil brahmi" in text and any(w in text for w in ["sign", "reading", "name"]):
            insights["tamil_brahmi_links"].append({
                "title": p["title"], "year": p.get("year"),
            })

        if "meluhha" in text and any(w in text for w in ["name", "personal", "seal", "translat"]):
            insights["meluhha_evidence"].append({
                "title": p["title"], "year": p.get("year"),
            })

        if any(w in text for w in ["bayesian decipher", "neural decipher",
                                    "machine learn decipher", "transfer learn"]):
            insights["computational_methods"].append({
                "title": p["title"], "year": p.get("year"),
            })

    # Current anchor stats
    anchors = _load_anchors()
    high = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
    medium = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")
    low = sum(1 for v in anchors.values() if v.get("confidence") == "LOW")
    no_reading = sum(1 for v in anchors.values() if not v.get("reading"))

    result = {
        "phase": 351,
        "total_papers": len(final),
        "category_counts": category_counts,
        "top_30_papers": [{
            "title": p["title"],
            "doi": p.get("doi", ""),
            "year": p.get("year"),
            "authors": p.get("authors", [])[:3],
            "score": p["score"],
            "category": p["category"],
        } for p in final[:30]],
        "advancement_insights": {
            k: {"count": len(v), "top_5": v[:5]} for k, v in insights.items()
        },
        "current_anchor_stats": {
            "HIGH": high, "MEDIUM": medium, "LOW": low,
            "no_reading": no_reading, "total": len(anchors),
        },
        "next_priorities": [
            f"Upgrade {medium} MEDIUM readings using new evidence from {len(insights['new_sign_readings'])} sign-reading papers",
            f"Cross-check {len(insights['tamil_brahmi_links'])} Tamil-Brahmi continuity papers for direct sign-value transfers",
            f"Extract personal name formulas from {len(insights['formula_patterns'])} formula papers",
            f"Investigate {len(insights['meluhha_evidence'])} Meluhha bilingual sources for phonetic constraints",
            f"Evaluate {len(insights['computational_methods'])} computational methods for LOW→HIGH upgrade pipeline",
        ],
        "verdict": (
            f"Advancement mine: {len(final)} papers across 6 categories. "
            f"Insights: {sum(len(v) for v in insights.values())} actionable items. "
            f"Current: {high} HIGH / {medium} MEDIUM / {low} LOW readings."
        ),
    }

    OUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved to {OUT_PATH}")
    print(f"  {result['verdict']}")

    print("\n  NEXT PRIORITIES:")
    for p in result["next_priorities"]:
        print(f"    → {p}")

    return result


if __name__ == "__main__":
    mine_advancement()
