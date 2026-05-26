"""Phase 295 -- Bulk Mine 5000 (May 2026 Focus)

Targeted clusters:
  1. Works by emailed researchers: Rao, Fuls, Nair, Sproat, Parpola,
     Renganathan, Murugaiyan, Kobayashi, Roif, Kolichala
  2. Indus script decipherment 2025-2026 (peer-reviewed + preprints)
  3. Dravidian computational linguistics / DEDR / corpus 2025-2026
  4. aDNA / archaeogenetics South Asia latest (Narasimhan follow-ups)
  5. Tamil-Brahmi / Keezhadi / Sangam recent
  6. Gulf seals / Dilmun / Meluhha cuneiform 2024-2026
  7. IVC urbanism / trade / collapse recent
  8. Proto-Dravidian reconstruction / Krishnamurti follow-ups
  9. Indus sign computational analysis / entropy / NLP 2025-2026
  10. Bronze Age South/Central Asian language contact

Six tracks: OpenAlex (30 queries), CrossRef (18), SemanticScholar (14),
arXiv (25), EuropePMC (6), Wikipedia survey (6).

Output: outputs/phase295_bulk_mine_5000.json
"""
from __future__ import annotations
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

HTTP_TIMEOUT = 15
RATE_SLEEP   = 0.35
MAX_PAGES    = 8
PAGE_SIZE    = 200
TARGET       = 5000

# ── Relevance patterns ──────────────────────────────────────────────

STRONG_PATTERNS = [
    re.compile(r"Indus.*script.*(?:decipher|decod|phonet|syllab|read)", re.I),
    re.compile(r"(?:Indus|Harappan).*(?:Dravidian|Proto.Dravidian|Tamil)", re.I),
    re.compile(r"Indus.*(?:simulated annealing|bigram|entropy|Markov|n-gram)", re.I),
    re.compile(r"(?:Rao|Parpola|Fuls|Nair|Sproat|Mahadevan).*(?:Indus|Harappan|script)", re.I),
    re.compile(r"(?:Indus|IVC).*(?:seal|inscription).*(?:corpus|database|catalog)", re.I),
    re.compile(r"Tamil.Brahmi.*(?:inscription|epigraphy|name|personal)", re.I),
    re.compile(r"(?:DEDR|Dravidian Etymological).*(?:comput|digital|database)", re.I),
    re.compile(r"Elamo.Dravidian.*(?:cognate|phoneme|evidence|McAlpin)", re.I),
    re.compile(r"Keezhadi.*(?:2025|2026|excavation|inscription|Tamil)", re.I),
    re.compile(r"(?:Indus|IVC|Harappan).*(?:2025|2026).*(?:peer|review|journal)", re.I),
    re.compile(r"South Asia.*(?:aDNA|ancient DNA|archaeogenetics).*(?:2025|2026)", re.I),
    re.compile(r"(?:Renganathan|Murugaiyan|Kobayashi|Kolichala).*(?:Tamil|Dravidian)", re.I),
]

MODERATE_PATTERNS = [
    re.compile(r"Dravidian.*(?:morpho|agglut|SOV|case|suffix|genitive)", re.I),
    re.compile(r"(?:Gulf|Dilmun|Failaka|Bahrain).*(?:seal|Indus|Harappan)", re.I),
    re.compile(r"Meluhha.*(?:cuneiform|Akkadian|Sargonic|CDLI)", re.I),
    re.compile(r"Brahui.*(?:Dravidian|contact|Balochistan|isogloss)", re.I),
    re.compile(r"(?:Indus|Harappan).*(?:trade|weight|metrolog|urban)", re.I),
    re.compile(r"(?:allograph|sign variant).*(?:Indus|Harappan|script)", re.I),
    re.compile(r"(?:Dravidian|Tamil).*(?:personal name|onomast|kinship)", re.I),
    re.compile(r"(?:Sangam|Cankam).*(?:Tamil|literatur|inscript)", re.I),
    re.compile(r"Proto.Dravidian.*(?:reconstruct|phonolog|lexicon)", re.I),
    re.compile(r"(?:Indus|IVC).*(?:collapse|decline|migration|climate).*(?:1900|late)", re.I),
]

# ── Query clusters ──────────────────────────────────────────────────

OA_QUERIES = [
    # Emailed researchers' recent work
    "Rajesh Rao Indus script 2024 2025 2026",
    "Andreas Fuls Indus script positional ICIT 2024 2025",
    "Ashish Nair Indus script synthetic baseline 2025 2026",
    "Richard Sproat Indus script non-linguistic 2023 2024 2025",
    "Parpola Indus Dravidian 2023 2024 2025 2026",
    "Vasu Renganathan Tamil computational South Asia 2024 2025",
    "Appasamy Murugaiyan Tamil Brahmi epigraphy Proto-Dravidian",
    "Masato Kobayashi Proto-Dravidian reconstruction Kurux Malto Brahui",
    "Suresh Kolichala Dravidian historical linguistics DEDR JAMBU",
    # Indus decipherment peer-reviewed 2025-2026
    "Indus script decipherment 2025 2026 peer reviewed",
    "Indus Valley script reading phonetic syllabic 2025",
    "Harappan seal inscription analysis corpus 2026",
    "Indus sign entropy conditional Markov model 2025",
    "Indus script computational neural LLM transformer 2025 2026",
    # Dravidian linguistics
    "Proto-Dravidian phonological reconstruction 2024 2025",
    "Dravidian language computational corpus 2025 2026",
    "DEDR digital database cognate Dravidian etymological",
    "Tamil Brahmi inscription personal name Sangam 2025",
    # aDNA
    "South Asian ancient DNA 2025 2026 Harappan genome",
    "AASI ancestry Dravidian genetic India 2025 2026",
    "Rakhigarhi genome IVC ancient DNA follow-up",
    # Contact zones
    "Gulf seal Dilmun Failaka Indus Harappan 2024 2025",
    "Meluhha cuneiform CDLI trade record 2024 2025 2026",
    # IVC studies
    "Keezhadi excavation Tamil inscription 2025 2026",
    "Harappan urbanism trade network 2025 2026",
    "Indus Valley civilization collapse decline climate 2025",
    # Sign analysis
    "Indus sign allograph variant grapheme 2024 2025",
    "Indus corpus statistical analysis sign frequency 2025",
    "Dravidian agglutinative morphology Elamite comparison 2025",
]

CROSSREF_QUERIES = [
    "Indus script decipherment 2025",
    "Indus Valley sign analysis 2026",
    "Proto-Dravidian reconstruction computational",
    "Rao Indus Markov entropy",
    "Fuls Indus positional analysis",
    "Parpola Dravidian seal 2024",
    "Sproat Indus non-linguistic symbols 2023",
    "South Asian ancient DNA archaeogenetics 2025",
    "Tamil Brahmi epigraphy inscription 2025",
    "Keezhadi Tamil excavation 2025",
    "Dravidian morphology agglutination SOV",
    "Gulf seal Dilmun Bahrain Indus",
    "Meluhha cuneiform CDLI Sargonic 2024",
    "Indus sign allograph variant study",
    "DEDR Dravidian etymological digital",
    "Elamo-Dravidian McAlpin cognate evidence",
    "Brahui North Dravidian phylogenetic",
    "Indus Valley trade urbanism weight 2025",
]

S2_QUERIES = [
    "Indus script decipherment 2025 2026",
    "Rao Indus Markov model sign",
    "Fuls ICIT Indus corpus positional",
    "Nair Indus synthetic baseline scorecard",
    "Proto-Dravidian phonological reconstruction",
    "South Asian ancient DNA archaeogenetics 2025",
    "Tamil Brahmi inscription personal name",
    "Dravidian computational historical linguistics JAMBU",
    "Gulf Dilmun seal Indus Harappan",
    "Keezhadi Tamil Iron Age excavation 2025",
    "Elamo-Dravidian McAlpin cognate",
    "Indus sign entropy statistical analysis 2025",
    "Brahui North Dravidian language contact",
    "Meluhha cuneiform Akkadian trade 2024",
]

ARXIV_QUERIES = [
    "Indus script decipherment",
    "Dravidian language computational",
    "South Asian archaeogenetics ancient DNA",
    "Harappan script analysis",
    "Indus Valley Civilization language",
    "proto-Dravidian reconstruction",
    "Tamil Brahmi inscription ancient",
    "Indus seal analysis computational",
    "ancient South Asia linguistics",
    "Elamo-Dravidian language family",
    "Indus corpus statistics entropy",
    "Dravidian agglutination morphology",
    "Harappan collapse climate change",
    "Indus sign frequency analysis",
    "South Asian Bronze Age genetics",
    "Parpola Indus script",
    "Keezhadi excavation Tamil",
    "Indus sign variant allograph",
    "Kolichala Dravidian JAMBU",
    "Sproat Indus non-linguistic",
    "Nair Indus baseline scorecard",
    "Rao Markov Indus script",
    "Indus Valley script NLP transformer",
    "Dravidian etymological database computational",
    "Gulf seal Dilmun Indus",
]

EUROPEPMC_QUERIES = [
    "Indus script decipherment 2025",
    "Proto-Dravidian language reconstruction",
    "Tamil Brahmi epigraphy 2025",
    "South Asian ancient DNA 2025 2026",
    "Keezhadi excavation Tamil inscription",
    "Harappan seal corpus analysis",
]


# ── HTTP helpers ────────────────────────────────────────────────────

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


# ── Track helpers ───────────────────────────────────────────────────

all_items: list[dict] = []
seen_titles: set[str] = set()

def _norm(t: str) -> str:
    return re.sub(r"\s+", " ", t.strip().lower())

def _add(title, authors, year, source, doi="", url="", abstract=""):
    key = _norm(title)
    if not key or key in seen_titles:
        return
    seen_titles.add(key)
    # Score relevance
    text = f"{title} {abstract}"
    strength = "WEAK"
    for p in STRONG_PATTERNS:
        if p.search(text):
            strength = "STRONG"
            break
    if strength != "STRONG":
        for p in MODERATE_PATTERNS:
            if p.search(text):
                strength = "MODERATE"
                break
    all_items.append({
        "title": title, "authors": authors, "year": year,
        "source": source, "doi": doi, "url": url,
        "strength": strength, "abstract": abstract[:500] if abstract else "",
    })


# ── Track 1: OpenAlex ──────────────────────────────────────────────

def _mine_openalex():
    print(f"[OpenAlex] {len(OA_QUERIES)} queries...")
    for q in OA_QUERIES:
        enc = urllib.parse.quote(q)
        for page in range(1, MAX_PAGES + 1):
            url = (f"https://api.openalex.org/works?search={enc}"
                   f"&per_page={PAGE_SIZE}&page={page}"
                   f"&mailto=tpierson@bitconcepts.tech")
            data = _get_json(url)
            if not data or "results" not in data:
                break
            for w in data["results"]:
                title = w.get("title", "")
                if not title:
                    continue
                authors = ", ".join(
                    a.get("author", {}).get("display_name", "?")
                    for a in (w.get("authorships") or [])[:5]
                )
                year = w.get("publication_year", 0)
                doi  = w.get("doi", "") or ""
                ab   = (w.get("abstract_inverted_index") or {})
                if ab:
                    # Reconstruct abstract from inverted index
                    pos = {}
                    for word, positions in ab.items():
                        for p in positions:
                            pos[p] = word
                    ab_text = " ".join(pos[k] for k in sorted(pos))
                else:
                    ab_text = ""
                _add(title, authors, year, "OpenAlex", doi, "", ab_text)
            if len(data["results"]) < PAGE_SIZE:
                break
            time.sleep(RATE_SLEEP)
        if len(all_items) >= TARGET:
            break
    print(f"  → {len(all_items)} total after OpenAlex")


# ── Track 2: CrossRef ──────────────────────────────────────────────

def _mine_crossref():
    print(f"[CrossRef] {len(CROSSREF_QUERIES)} queries...")
    for q in CROSSREF_QUERIES:
        enc = urllib.parse.quote(q)
        url = (f"https://api.crossref.org/works?query={enc}"
               f"&rows=100&mailto=tpierson@bitconcepts.tech")
        data = _get_json(url)
        if not data:
            continue
        items = (data.get("message") or {}).get("items") or []
        for w in items:
            titles = w.get("title") or []
            title  = titles[0] if titles else ""
            if not title:
                continue
            auths = ", ".join(
                f"{a.get('given','')} {a.get('family','')}"
                for a in (w.get("author") or [])[:5]
            )
            year = 0
            for dk in ["published-print", "published-online", "created"]:
                dp = w.get(dk, {}).get("date-parts", [[0]])
                if dp and dp[0] and dp[0][0]:
                    year = dp[0][0]
                    break
            doi = w.get("DOI", "")
            ab  = w.get("abstract", "")
            if ab:
                ab = re.sub(r"<[^>]+>", "", ab)  # strip HTML
            _add(title, auths, year, "CrossRef", doi, "", ab)
        time.sleep(RATE_SLEEP)
    print(f"  → {len(all_items)} total after CrossRef")


# ── Track 3: SemanticScholar ───────────────────────────────────────

def _mine_s2():
    print(f"[S2] {len(S2_QUERIES)} queries...")
    for q in S2_QUERIES:
        enc = urllib.parse.quote(q)
        url = (f"https://api.semanticscholar.org/graph/v1/paper/search"
               f"?query={enc}&limit=100&fields=title,authors,year,externalIds,abstract")
        data = _get_json(url)
        if not data or "data" not in data:
            time.sleep(1)
            continue
        for p in data["data"]:
            title = p.get("title", "")
            auths = ", ".join(a.get("name", "?") for a in (p.get("authors") or [])[:5])
            year  = p.get("year", 0)
            doi   = (p.get("externalIds") or {}).get("DOI", "")
            ab    = p.get("abstract", "") or ""
            _add(title, auths, year, "S2", doi, "", ab)
        time.sleep(1.0)  # S2 rate limit is strict
    print(f"  → {len(all_items)} total after S2")


# ── Track 4: arXiv ─────────────────────────────────────────────────

def _mine_arxiv():
    print(f"[arXiv] {len(ARXIV_QUERIES)} queries...")
    for q in ARXIV_QUERIES:
        enc = urllib.parse.quote(q)
        url = f"http://export.arxiv.org/api/query?search_query=all:{enc}&max_results=100"
        raw = _get_raw(url)
        if not raw:
            continue
        # Simple XML parsing for entries
        for entry in re.findall(r"<entry>(.*?)</entry>", raw, re.S):
            title = ""
            m = re.search(r"<title>(.*?)</title>", entry, re.S)
            if m:
                title = re.sub(r"\s+", " ", m.group(1).strip())
            authors_list = re.findall(r"<name>(.*?)</name>", entry)
            auths = ", ".join(authors_list[:5])
            year = 0
            m2 = re.search(r"<published>(\d{4})", entry)
            if m2:
                year = int(m2.group(1))
            ab = ""
            m3 = re.search(r"<summary>(.*?)</summary>", entry, re.S)
            if m3:
                ab = re.sub(r"\s+", " ", m3.group(1).strip())
            link = ""
            m4 = re.search(r'<id>(.*?)</id>', entry)
            if m4:
                link = m4.group(1)
            _add(title, auths, year, "arXiv", "", link, ab)
        time.sleep(RATE_SLEEP)
    print(f"  → {len(all_items)} total after arXiv")


# ── Track 5: EuropePMC ─────────────────────────────────────────────

def _mine_europepmc():
    print(f"[EuropePMC] {len(EUROPEPMC_QUERIES)} queries...")
    for q in EUROPEPMC_QUERIES:
        enc = urllib.parse.quote(q)
        url = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search"
               f"?query={enc}&format=json&pageSize=100")
        data = _get_json(url)
        if not data:
            continue
        for r in (data.get("resultList") or {}).get("result") or []:
            title = r.get("title", "")
            auths = r.get("authorString", "")
            year  = r.get("pubYear", 0)
            doi   = r.get("doi", "") or ""
            ab    = r.get("abstractText", "") or ""
            _add(title, auths, int(year) if year else 0, "EuropePMC", doi, "", ab)
        time.sleep(RATE_SLEEP)
    print(f"  → {len(all_items)} total after EuropePMC")


# ── Main ────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("PHASE 295 — BULK MINE 5000 (MAY 2026 FOCUS)")
    print("=" * 60)

    _mine_openalex()
    _mine_crossref()
    _mine_s2()
    _mine_arxiv()
    _mine_europepmc()

    # Summary stats
    strong   = [i for i in all_items if i["strength"] == "STRONG"]
    moderate = [i for i in all_items if i["strength"] == "MODERATE"]
    recent   = [i for i in all_items if (i.get("year") or 0) >= 2024]

    result = {
        "phase": 295,
        "description": "Bulk mine 5000 — May 2026 focus, emailed researchers, peer-reviewed Indus/Dravidian studies",
        "total_papers": len(all_items),
        "strong_count": len(strong),
        "moderate_count": len(moderate),
        "recent_2024_plus": len(recent),
        "by_source": {},
        "strong_papers": sorted(strong, key=lambda x: -(x.get("year") or 0))[:100],
        "moderate_papers": sorted(moderate, key=lambda x: -(x.get("year") or 0))[:50],
        "all_papers": all_items,
    }
    # Source breakdown
    for item in all_items:
        src = item["source"]
        result["by_source"][src] = result["by_source"].get(src, 0) + 1

    out_path = OUTPUTS / "phase295_bulk_mine_5000.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print()
    print(f"TOTAL: {len(all_items)} papers")
    print(f"STRONG: {len(strong)}")
    print(f"MODERATE: {len(moderate)}")
    print(f"RECENT (2024+): {len(recent)}")
    print(f"By source: {result['by_source']}")
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
