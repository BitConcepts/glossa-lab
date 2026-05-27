"""Mining Discovery Loop — 5 rounds with evolving queries

Each round targets a different gap identified from Phases 371-376:
  Round 1: One-sign blockers — find papers on rare/hapax signs in Indus corpus
  Round 2: Compound word semantics — Dravidian compound noun formation patterns
  Round 3: Guild title parallels — Sangam/Tamil-Brahmi professional title evidence
  Round 4: Motif-specific vocabulary — archaeological seal function studies
  Round 5: Length-dependent structure — Indus inscription structure and syntax

Output: outputs/mining_discovery_loop.json
"""
from __future__ import annotations
import json, re, time, urllib.parse, urllib.request
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT_PATH = REPO / "outputs" / "mining_discovery_loop.json"

def _get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "GlossaLab/0.6 (research; tpierson@bitconcepts.tech)"})
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception: time.sleep(0.5 * (attempt + 1))
    return None

ROUND_QUERIES = {
    1: {
        "name": "One-sign blockers & hapax signs",
        "queries": [
            "Indus script hapax legomena rare sign frequency analysis",
            "undeciphered script low frequency sign reading strategy",
            "Indus sign variant rare glyph identification classification",
            "ancient script rare symbol context-based reading method",
            "Harappan seal uncommon sign positional analysis assignment",
        ],
    },
    2: {
        "name": "Dravidian compound word formation",
        "queries": [
            "Dravidian compound noun formation puṟaṉāṉūṟu Sangam Tamil",
            "Tamil compound word morphology agglutination pattern",
            "Proto-Dravidian compound name personal title formation rule",
            "Old Tamil compound verb noun structure Tolkāppiyam grammar",
            "Dravidian compound word semantic head modifier order",
        ],
    },
    3: {
        "name": "Guild title parallels in Sangam/Tamil-Brahmi",
        "queries": [
            "Sangam Tamil guild merchant title nakarattar vaṇikar inscription",
            "Tamil Brahmi hero stone personal name title formula",
            "ancient Tamil professional title inscription craft guild",
            "Sangam literature occupation title name structure",
            "South Indian ancient guild seal inscription trade organization",
        ],
    },
    4: {
        "name": "Seal function and motif-specific vocabulary",
        "queries": [
            "Indus seal unicorn function meaning administrative identity",
            "Harappan seal motif animal symbol meaning social function",
            "ancient seal administrative function identity marker Near East comparison",
            "Indus seal impression context find spot archaeological function",
            "cylinder seal stamp seal function administrative commercial ancient",
        ],
    },
    5: {
        "name": "Inscription structure and syntax",
        "queries": [
            "Indus inscription structure syntax word order analysis",
            "Indus script text structure formula pattern computational",
            "ancient short inscription structure syntax interpretation method",
            "seal inscription syntax name title structure ancient Near East",
            "Indus sign sequence pattern structure Rao Sproat Farmer analysis",
        ],
    },
}


def mine_round(round_num, queries, all_seen):
    """Mine one round, dedup against previous rounds."""
    bucket = []
    for q in queries:
        enc = urllib.parse.quote(q)
        # OpenAlex
        url = (f"https://api.openalex.org/works?search={enc}&per-page=100&cursor=*"
               f"&select=id,title,doi,publication_year,authorships,abstract_inverted_index"
               f"&mailto=tpierson@bitconcepts.tech")
        data = _get_json(url)
        if data and "results" in data:
            for w in data["results"]:
                title = w.get("title") or ""
                abstract = ""
                aii = w.get("abstract_inverted_index")
                if aii:
                    pairs = sorted([(pos, word) for word, positions in aii.items() for pos in positions])
                    abstract = " ".join(w for _, w in pairs)
                if title:
                    bucket.append({"title": title, "doi": w.get("doi", ""),
                                  "year": w.get("publication_year"),
                                  "abstract_snippet": abstract[:600]})
        time.sleep(0.4)

        # Semantic Scholar
        s2_url = (f"https://api.semanticscholar.org/graph/v1/paper/search"
                  f"?query={enc}&limit=50&fields=title,authors,year,abstract")
        s2_data = _get_json(s2_url)
        if s2_data:
            for paper in s2_data.get("data", []):
                title = paper.get("title") or ""
                if title:
                    bucket.append({"title": title, "doi": "",
                                  "year": paper.get("year"),
                                  "abstract_snippet": (paper.get("abstract") or "")[:600]})
        time.sleep(1.0)

    # Dedup within round and against previous
    unique = []
    for p in bucket:
        norm = re.sub(r"\s+", " ", p["title"].lower().strip())
        if norm and norm not in all_seen:
            all_seen.add(norm)
            unique.append(p)

    # Extract insights from abstracts
    insights = []
    for p in unique:
        text = f"{p['title']} {p['abstract_snippet']}".lower()
        for keyword, insight_type in [
            ("sign value", "sign_reading"), ("reading propos", "sign_reading"),
            ("guild", "guild_title"), ("merchant", "guild_title"), ("title", "guild_title"),
            ("compound", "compound_word"), ("agglut", "morphology"),
            ("hapax", "rare_sign"), ("rare sign", "rare_sign"), ("low frequency", "rare_sign"),
            ("seal function", "seal_function"), ("administrative", "seal_function"),
            ("syntax", "syntax"), ("word order", "syntax"), ("structure", "syntax"),
        ]:
            if keyword in text:
                insights.append({"type": insight_type, "title": p["title"][:80]})
                break

    return unique, insights


def main():
    print("=" * 70)
    print("MINING DISCOVERY LOOP — 5 ROUNDS")
    print("=" * 70)

    all_seen = set()
    all_results = []
    total_papers = 0
    total_insights = 0

    for round_num in range(1, 6):
        info = ROUND_QUERIES[round_num]
        print(f"\n{'─' * 70}")
        print(f"ROUND {round_num}/5: {info['name']}")
        print(f"{'─' * 70}")

        papers, insights = mine_round(round_num, info["queries"], all_seen)
        total_papers += len(papers)
        total_insights += len(insights)

        print(f"  Papers: {len(papers)} new unique")
        print(f"  Insights: {len(insights)}")
        if insights:
            for ins in insights[:5]:
                print(f"    [{ins['type']}] {ins['title']}")

        all_results.append({
            "round": round_num,
            "name": info["name"],
            "n_papers": len(papers),
            "n_insights": len(insights),
            "insights": insights[:10],
            "top_5_papers": [{"title": p["title"][:100], "year": p.get("year")} for p in papers[:5]],
        })

    result = {
        "protocol": "mining_discovery_loop",
        "rounds": 5,
        "total_new_papers": total_papers,
        "total_insights": total_insights,
        "results": all_results,
        "verdict": (
            f"Mining discovery: {total_papers} new papers across 5 rounds, "
            f"{total_insights} actionable insights extracted."
        ),
    }

    OUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{'=' * 70}")
    print(f"TOTAL: {total_papers} papers, {total_insights} insights")
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
