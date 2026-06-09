"""Phase 298: Deep Targeted Mine — Proto-Munda SA + Archaeological Discoveries

Two critical blockers from Phase 297 gap analysis:
  1. Proto-Munda not formally tested as competing SA baseline
  2. No bilingual inscription discovered

This script does exhaustive multi-source mining for:
  A. Proto-Munda / Austroasiatic language data, wordlists, corpora, computational work
  B. Bilingual inscriptions, Gulf trade site discoveries 2023-2026
  C. New IVC archaeological excavations 2024-2026 (Rakhigarhi, Dholavira, Keezhadi)
  D. Indus seals found outside IVC (Mesopotamia, Oman, Bahrain, Iran)

Loops through 6 APIs with progressively broader queries until exhausted.
Output: outputs/phase298_deep_munda_archaeology_mine.json
"""
from __future__ import annotations
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase298_deep_munda_archaeology_mine.json"
OUT.parent.mkdir(exist_ok=True)

HTTP_TIMEOUT = 15
RATE_SLEEP = 0.4

all_items: list[dict] = []
seen: set[str] = set()

def _norm(t): return re.sub(r"\s+", " ", t.strip().lower())

def _add(title, authors, year, source, doi="", url="", abstract="", category=""):
    key = _norm(title)
    if not key or key in seen: return
    seen.add(key)
    all_items.append({
        "title": title, "authors": authors, "year": year,
        "source": source, "doi": doi, "url": url,
        "abstract": abstract[:600] if abstract else "",
        "category": category,
    })

def _get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "GlossaLab/0.1 (research; tpierson@bitconcepts.tech)"
            })
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception:
            time.sleep(RATE_SLEEP * (attempt + 1))
    return None

def _get_raw(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.1"})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception:
            time.sleep(RATE_SLEEP * (attempt + 1))
    return ""

# ── QUERY CLUSTERS ──────────────────────────────────────────────────

MUNDA_QUERIES = [
    # Proto-Munda reconstruction
    "Proto-Munda language reconstruction phonology",
    "Proto-Munda wordlist vocabulary cognate",
    "Munda language family Austroasiatic South Asia",
    "Munda substrate Indo-Aryan Dravidian loanwords",
    "Munda Khasi Santali Ho Mundari historical linguistics",
    "Austroasiatic South Asia Bronze Age contact",
    "Munda language computational corpus digital",
    "Proto-Austroasiatic reconstruction Southeast Asia South Asia",
    "Munda Dravidian contact substrate borrowing lexicon",
    "Witzel Munda substrate Indo-Aryan 1999",
    "Munda language Indus Valley civilization Harappan",
    "Austroasiatic phylogenetics South Asia divergence",
    "Santali language corpus computational",
    "Mundari phonology morphology agglutinative",
    "Munda script Ol Chiki writing system",
    "Proto-Munda agriculture vocabulary rice millet",
    "Munda Dravidian shared vocabulary DEDR",
    "Austroasiatic migration South Asia archaeology genetics",
    "Munda language isolate Nihali Kusunda South Asia",
    "Anderson Munda languages handbook 2008",
    # Proto-Munda + IVC
    "Proto-Munda Indus script hypothesis",
    "Munda language Harappan civilization evidence",
    "Austroasiatic Bronze Age South Asia Indus",
    "Munda substrate Indus Valley loanwords",
    "Fuller Munda agriculture Neolithic South Asia",
]

ARCHAEOLOGY_QUERIES = [
    # Bilingual inscriptions
    "bilingual inscription Indus script cuneiform",
    "bilingual text Harappan Mesopotamian",
    "Indus seal bilingual Akkadian Sumerian",
    "bilingual artifact Bronze Age South Asia Gulf",
    "seal inscription translation Indus Mesopotamia",
    # Gulf trade site discoveries
    "Gulf seal discovery 2024 2025 2026 Bahrain Oman Failaka",
    "Dilmun seal new discovery excavation 2024 2025",
    "Indus seal found Mesopotamia Iraq 2024 2025 2026",
    "Indus seal Oman Ras al-Jinz Bronze Age 2024 2025",
    "Indus artifacts Persian Gulf trade recent discovery",
    "Failaka Island excavation seal 2024 2025",
    "Bahrain seal Indus Harappan new find",
    "Indus seal Iran Jiroft Shahr-i Sokhta 2024 2025",
    # New IVC excavations
    "Rakhigarhi excavation 2024 2025 2026 new findings",
    "Dholavira excavation inscription 2024 2025 2026",
    "Keezhadi excavation 2024 2025 2026 inscription Tamil",
    "Harappa excavation new season 2024 2025",
    "Mohenjo-daro conservation excavation 2024 2025",
    "Indus Valley new site discovery 2024 2025 2026",
    "IVC excavation Pakistan India new seal inscription",
    "Ganweriwala excavation Cholistan Indus 2024",
    # Indus seals outside IVC
    "Indus seal Susa Elam Iran find",
    "Indus seal Tell Asmar Mesopotamia",
    "Indus artifacts Ur Tell Abraq Abu Dhabi",
    "Meluhha seal cylinder round stamp Mesopotamia find",
    "Harappan object Gulf Emirates archaeological",
    # Specific recent discoveries
    "Indus Valley civilization new discovery breakthrough 2025 2026",
    "Harappan seal decipherment new evidence 2025 2026",
    "ancient South Asia Bronze Age inscription discovery 2025",
    "IVC inscription pottery graffiti Dholavira signboard new",
]

def _mine_openalex(queries, category, max_per_query=200):
    print(f"  [OpenAlex] {len(queries)} queries for {category}...")
    for q in queries:
        enc = urllib.parse.quote(q)
        for page in range(1, 4):
            url = (f"https://api.openalex.org/works?search={enc}"
                   f"&per_page={max_per_query}&page={page}"
                   f"&mailto=tpierson@bitconcepts.tech")
            data = _get_json(url)
            if not data or "results" not in data: break
            for w in data["results"]:
                title = w.get("title", "")
                if not title: continue
                authors = ", ".join(
                    a.get("author", {}).get("display_name", "?")
                    for a in (w.get("authorships") or [])[:5]
                )
                year = w.get("publication_year", 0)
                doi = w.get("doi", "") or ""
                ab = w.get("abstract_inverted_index") or {}
                if ab:
                    pos = {}
                    for word, positions in ab.items():
                        for p in positions: pos[p] = word
                    ab_text = " ".join(pos[k] for k in sorted(pos))
                else:
                    ab_text = ""
                _add(title, authors, year, "OpenAlex", doi, "", ab_text, category)
            if len(data["results"]) < max_per_query: break
            time.sleep(RATE_SLEEP)

def _mine_crossref(queries, category):
    print(f"  [CrossRef] {len(queries)} queries for {category}...")
    for q in queries:
        enc = urllib.parse.quote(q)
        url = f"https://api.crossref.org/works?query={enc}&rows=100&mailto=tpierson@bitconcepts.tech"
        data = _get_json(url)
        if not data: continue
        for w in (data.get("message") or {}).get("items") or []:
            titles = w.get("title") or []
            title = titles[0] if titles else ""
            if not title: continue
            auths = ", ".join(f"{a.get('given','')} {a.get('family','')}" for a in (w.get("author") or [])[:5])
            year = 0
            for dk in ["published-print", "published-online", "created"]:
                dp = w.get(dk, {}).get("date-parts", [[0]])
                if dp and dp[0] and dp[0][0]:
                    year = dp[0][0]; break
            doi = w.get("DOI", "")
            ab = w.get("abstract", "")
            if ab: ab = re.sub(r"<[^>]+>", "", ab)
            _add(title, auths, year, "CrossRef", doi, "", ab, category)
        time.sleep(RATE_SLEEP)

def _mine_s2(queries, category):
    print(f"  [S2] {len(queries)} queries for {category}...")
    for q in queries:
        enc = urllib.parse.quote(q)
        url = (f"https://api.semanticscholar.org/graph/v1/paper/search"
               f"?query={enc}&limit=100&fields=title,authors,year,externalIds,abstract")
        data = _get_json(url)
        if not data or "data" not in data:
            time.sleep(1); continue
        for p in data["data"]:
            title = p.get("title", "")
            auths = ", ".join(a.get("name", "?") for a in (p.get("authors") or [])[:5])
            year = p.get("year", 0)
            doi = (p.get("externalIds") or {}).get("DOI", "")
            ab = p.get("abstract", "") or ""
            _add(title, auths, year, "S2", doi, "", ab, category)
        time.sleep(1.0)

def _mine_arxiv(queries, category):
    print(f"  [arXiv] {len(queries)} queries for {category}...")
    for q in queries:
        enc = urllib.parse.quote(q)
        url = f"http://export.arxiv.org/api/query?search_query=all:{enc}&max_results=100"
        raw = _get_raw(url)
        if not raw: continue
        for entry in re.findall(r"<entry>(.*?)</entry>", raw, re.S):
            m = re.search(r"<title>(.*?)</title>", entry, re.S)
            title = re.sub(r"\s+", " ", m.group(1).strip()) if m else ""
            authors_list = re.findall(r"<name>(.*?)</name>", entry)
            auths = ", ".join(authors_list[:5])
            m2 = re.search(r"<published>(\d{4})", entry)
            year = int(m2.group(1)) if m2 else 0
            m3 = re.search(r"<summary>(.*?)</summary>", entry, re.S)
            ab = re.sub(r"\s+", " ", m3.group(1).strip()) if m3 else ""
            m4 = re.search(r'<id>(.*?)</id>', entry)
            link = m4.group(1) if m4 else ""
            _add(title, auths, year, "arXiv", "", link, ab, category)
        time.sleep(RATE_SLEEP)

def _mine_europepmc(queries, category):
    print(f"  [EuropePMC] {len(queries)} queries for {category}...")
    for q in queries:
        enc = urllib.parse.quote(q)
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={enc}&format=json&pageSize=100"
        data = _get_json(url)
        if not data: continue
        for r in (data.get("resultList") or {}).get("result") or []:
            title = r.get("title", "")
            auths = r.get("authorString", "")
            year = r.get("pubYear", 0)
            doi = r.get("doi", "") or ""
            ab = r.get("abstractText", "") or ""
            _add(title, auths, int(year) if year else 0, "EuropePMC", doi, "", ab, category)
        time.sleep(RATE_SLEEP)

def _score_relevance():
    """Score each paper for actionability."""
    munda_patterns = [
        re.compile(r"(?:Proto.)?Munda.*(?:reconstruct|phonol|wordlist|cognate|vocab|corpus)", re.I),
        re.compile(r"Austroasiatic.*(?:South Asia|India|Bronze|migration|phylo)", re.I),
        re.compile(r"Munda.*(?:Dravidian|substrate|contact|loanword|Indus|Harappan)", re.I),
        re.compile(r"(?:Santali|Mundari|Ho|Khasi|Korku).*(?:corpus|dictionary|lexicon|phonol)", re.I),
    ]
    archaeology_patterns = [
        re.compile(r"bilingual.*(?:Indus|Harappan|seal|inscription|cuneiform)", re.I),
        re.compile(r"(?:Indus|Harappan).*(?:seal|artifact).*(?:found|discover|excavat).*(?:Gulf|Mesopotam|Oman|Bahrain|Iran)", re.I),
        re.compile(r"(?:Rakhigarhi|Dholavira|Keezhadi|Ganweriwala).*(?:excavat|inscription|seal|new|2024|2025|2026)", re.I),
        re.compile(r"(?:Failaka|Dilmun|Ras al.Jinz|Tell Abraq).*(?:seal|Indus|excavat|2024|2025)", re.I),
        re.compile(r"(?:Indus|IVC|Harappan).*(?:new discovery|breakthrough|new site).*(?:2024|2025|2026)", re.I),
    ]

    for item in all_items:
        text = f"{item['title']} {item['abstract']}"
        score = "WEAK"
        for p in munda_patterns:
            if p.search(text):
                score = "MUNDA_RELEVANT"; break
        if score == "WEAK":
            for p in archaeology_patterns:
                if p.search(text):
                    score = "ARCHAEOLOGY_RELEVANT"; break
        item["relevance"] = score


def main():
    print("=" * 60)
    print("PHASE 298: DEEP MUNDA + ARCHAEOLOGY MINE")
    print("=" * 60)

    # ── Round 1: All APIs for both categories ──
    print("\n── Round 1: Proto-Munda / Austroasiatic ──")
    _mine_openalex(MUNDA_QUERIES, "munda")
    _mine_crossref(MUNDA_QUERIES, "munda")
    _mine_s2(MUNDA_QUERIES[:15], "munda")
    _mine_arxiv(MUNDA_QUERIES[:10], "munda")
    _mine_europepmc(MUNDA_QUERIES[:8], "munda")
    print(f"  Total after Munda round: {len(all_items)}")

    print("\n── Round 2: Archaeological Discoveries ──")
    _mine_openalex(ARCHAEOLOGY_QUERIES, "archaeology")
    _mine_crossref(ARCHAEOLOGY_QUERIES, "archaeology")
    _mine_s2(ARCHAEOLOGY_QUERIES[:15], "archaeology")
    _mine_arxiv(ARCHAEOLOGY_QUERIES[:10], "archaeology")
    _mine_europepmc(ARCHAEOLOGY_QUERIES[:8], "archaeology")
    print(f"  Total after Archaeology round: {len(all_items)}")

    # ── Round 3: Expanded queries for thin results ──
    EXPANDED_MUNDA = [
        "Munda language family classification subgrouping",
        "Kherwarian North Munda Proto language",
        "South Munda Kharia Juang Sora reconstruction",
        "Anderson Munda languages Oxford handbook",
        "Diffloth Austroasiatic classification 2005",
        "Zide Munda languages bibliography",
        "Pinnow Munda Austroasiatic cognate",
        "Donegan Stampe Munda word structure",
        "Munda verb morphology prefixing",
        "Munda numeral system counting vocabulary",
    ]
    EXPANDED_ARCH = [
        "Indus civilization sealing technology transmission",
        "Harappan maritime trade Persian Gulf 2024 2025",
        "Lothal dock excavation recent 2024 2025",
        "Indus script potsherd graffiti new discovery",
        "Dholavira signboard inscription analysis 2024",
        "Indus seal Shortughai Afghanistan",
        "Harappan seal Gonur Depe Turkmenistan BMAC",
        "Indus artifact found outside South Asia new",
        "ancient trade route Indus Mesopotamia new evidence 2025",
        "Indus Valley writing new find 2025 2026",
    ]
    print("\n── Round 3: Expanded queries ──")
    _mine_openalex(EXPANDED_MUNDA, "munda_expanded")
    _mine_crossref(EXPANDED_MUNDA, "munda_expanded")
    _mine_openalex(EXPANDED_ARCH, "archaeology_expanded")
    _mine_crossref(EXPANDED_ARCH, "archaeology_expanded")
    print(f"  Total after expanded round: {len(all_items)}")

    # ── Score relevance ──
    _score_relevance()

    munda_rel = [i for i in all_items if i["relevance"] == "MUNDA_RELEVANT"]
    arch_rel = [i for i in all_items if i["relevance"] == "ARCHAEOLOGY_RELEVANT"]
    by_cat = {}
    for i in all_items:
        by_cat[i["category"]] = by_cat.get(i["category"], 0) + 1

    # Find specific high-value items
    munda_corpora = [i for i in munda_rel if any(w in (i["title"] + " " + i["abstract"]).lower()
                     for w in ["corpus", "wordlist", "dictionary", "lexicon", "digital"])]
    bilingual = [i for i in all_items if "bilingual" in (i["title"] + " " + i["abstract"]).lower()
                 and any(w in (i["title"] + " " + i["abstract"]).lower()
                         for w in ["indus", "harappan", "seal", "cuneiform"])]
    new_discoveries = [i for i in arch_rel if (i.get("year") or 0) >= 2024]

    result = {
        "phase": 298,
        "total_papers": len(all_items),
        "munda_relevant": len(munda_rel),
        "archaeology_relevant": len(arch_rel),
        "by_category": by_cat,
        "munda_corpora_found": len(munda_corpora),
        "bilingual_mentions": len(bilingual),
        "new_discoveries_2024_plus": len(new_discoveries),
        "munda_relevant_papers": sorted(munda_rel, key=lambda x: -(x.get("year") or 0))[:50],
        "archaeology_relevant_papers": sorted(arch_rel, key=lambda x: -(x.get("year") or 0))[:50],
        "munda_corpora": munda_corpora[:20],
        "bilingual_papers": bilingual[:20],
        "new_discoveries": new_discoveries[:30],
        "verdict": {
            "munda_sa_feasible": len(munda_corpora) > 0,
            "munda_corpus_sources": [i["title"][:80] for i in munda_corpora[:5]],
            "bilingual_found": len(bilingual) > 0 and any((i.get("year") or 0) >= 2024 for i in bilingual),
            "new_ivc_discoveries": len(new_discoveries),
        },
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print()
    print(f"TOTAL: {len(all_items)} papers")
    print(f"MUNDA RELEVANT: {len(munda_rel)}")
    print(f"  - Corpora/wordlists found: {len(munda_corpora)}")
    print(f"ARCHAEOLOGY RELEVANT: {len(arch_rel)}")
    print(f"  - Bilingual mentions: {len(bilingual)}")
    print(f"  - New discoveries 2024+: {len(new_discoveries)}")
    print(f"\nMunda SA feasible: {'YES' if munda_corpora else 'NO — no digital corpus found'}")
    if munda_corpora:
        print("  Top Munda corpus sources:")
        for c in munda_corpora[:5]:
            print(f"    {c.get('year',0)} | {c['authors'][:30]} | {c['title'][:80]}")
    if bilingual:
        print(f"\nBilingual inscription papers ({len(bilingual)}):")
        for b in bilingual[:5]:
            print(f"    {b.get('year',0)} | {b['title'][:80]}")
    print(f"\nSaved: {OUT}")


if __name__ == "__main__":
    main()
