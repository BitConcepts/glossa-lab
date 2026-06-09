"""Phase 322 — Mega Targeted Mine 5000+ (Decipherment Unlock Focus)

12 query clusters specifically targeting gaps that block decipherment:
  1. ALL scholars' sign-reading proposals (Fairservis, Wells, Hunter, Heras, Langdon, etc.)
  2. Mesopotamian Meluhha texts / CDLI bilingual evidence
  3. Proto-Dravidian missing phonemes: *b, *d, *ñ, *ḻ, *ṉ, *ṟ
  4. Tamil-Brahmi sign-value continuity (Keezhadi, Kodumanal)
  5. Dravidian substrate vocabulary in Rigvedic Sanskrit
  6. Indus commodity seals & trade terminology
  7. Sign co-occurrence / positional statistical studies
  8. Cryptanalytic / information-theoretic approaches to Indus
  9. Indus numeral & metrological system
  10. Seal impression contexts at foreign sites
  11. Old Tamil / Sangam personal name morphology
  12. Bayesian / neural computational decipherment methods

Sources: OpenAlex, CrossRef, SemanticScholar, arXiv, EuropePMC, Zenodo

Output: outputs/phase322_mega_mine_5000.json
"""
from __future__ import annotations
import json
import re
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

HTTP_TIMEOUT = 15
RATE_SLEEP   = 0.4
MAX_PAGES    = 10
PAGE_SIZE    = 200
TARGET       = 5000

# ── Relevance scoring ────────────────────────────────────────────────

STRONG_PATTERNS = [
    # Sign reading proposals by specific scholars
    re.compile(r"(?:Fairservis|Hunter|Heras|Langdon|Kinnier.Wilson|Knorozov).*(?:Indus|Harappan).*(?:sign|read|deciph)", re.I),
    re.compile(r"(?:Wells|Mahadevan|Parpola|Rao|Fuls|Nair).*(?:sign.value|reading|phonet)", re.I),
    re.compile(r"(?:Indus|Harappan).*sign.*(?:value|reading|phonetic|syllabic).*(?:propos|assign|identif)", re.I),
    # Meluhha bilingual
    re.compile(r"Meluhha.*(?:cuneiform|Akkadian|bilingual|personal.name|seal)", re.I),
    re.compile(r"(?:Shu.ili|Shu.Ilishu|Lu.Sunzida).*(?:Indus|Meluhha|seal)", re.I),
    re.compile(r"CDLI.*(?:Meluhha|Indus|Harappan)", re.I),
    # Missing phonemes
    re.compile(r"Proto.Dravidian.*(?:\*b|\*d|\*ñ|\*ḻ|\*ṉ|\*ṟ|retroflex|palatal.nasal)", re.I),
    re.compile(r"(?:DEDR|Dravidian).*(?:retroflex.lateral|alveolar.nasal|palatal)", re.I),
    # Tamil-Brahmi continuity
    re.compile(r"Tamil.Brahmi.*(?:sign.value|phonet|syllabary|aksara).*(?:Indus|Harappan|continu)", re.I),
    re.compile(r"(?:Keezhadi|Kodumanal|Arikamedu).*(?:Tamil.Brahmi|inscription|graffiti)", re.I),
    # Commodity trade
    re.compile(r"(?:Indus|Harappan).*(?:seal|tablet).*(?:commodity|trade|weight|measure|carnelian|lapis)", re.I),
    re.compile(r"(?:Indus|IVC).*(?:metrol|weight.*system|standard.*weight|cubical)", re.I),
    # Computational
    re.compile(r"(?:Bayesian|neural|transformer|LSTM).*(?:decipher|script|ancient|undeciphered)", re.I),
    re.compile(r"(?:Indus|Harappan).*(?:entropy|information.theory|Zipf|frequency|n.gram)", re.I),
    # Substrate
    re.compile(r"(?:Dravidian|Tamil|Proto.Drav).*(?:substrate|loanword|borrow).*(?:Rigved|Sanskrit|Vedic)", re.I),
    re.compile(r"(?:Witzel|Southworth|Krishnamurti).*(?:substrate|Dravidian|pre.Aryan)", re.I),
]

MODERATE_PATTERNS = [
    re.compile(r"Indus.*(?:script|sign|seal).*(?:analys|stud|corpus|frequen)", re.I),
    re.compile(r"(?:Dravidian|Tamil).*(?:morpho|agglut|suffix|case|genitive|SOV)", re.I),
    re.compile(r"(?:Gulf|Dilmun|Failaka|Bahrain).*(?:seal|Indus|round.*stamp)", re.I),
    re.compile(r"Harappan.*(?:urban|craft|bead|pottery|workshop|trade)", re.I),
    re.compile(r"(?:Sangam|Cankam|Old Tamil).*(?:personal.name|onomast|morpholog)", re.I),
    re.compile(r"(?:Indus|IVC).*(?:numeral|number|count|stroke.*mark)", re.I),
    re.compile(r"(?:Linear.Elamite|Proto.Elamite).*(?:decipher|sign|phonet)", re.I),
    re.compile(r"Brahui.*(?:Dravidian|isogloss|phonolog|Balochistan)", re.I),
    re.compile(r"(?:allograph|sign.variant|graphic.variant).*(?:Indus|Harappan)", re.I),
    re.compile(r"(?:McAlpin|Elamo.Dravidian).*(?:cognate|phoneme|evidence)", re.I),
]


def _score_paper(title, abstract=""):
    text = f"{title} {abstract}"
    s = 0
    for p in STRONG_PATTERNS:
        if p.search(text):
            s += 3
    for p in MODERATE_PATTERNS:
        if p.search(text):
            s += 1
    return s


# ── Query clusters ───────────────────────────────────────────────────

OA_QUERIES = [
    # Cluster 1: All scholars' reading proposals
    "Fairservis Indus script sign value reading 1992",
    "Hunter Indus script sign meaning 1934",
    "Heras Indus script Proto-Dravidian reading 1953",
    "Langdon Indus script reading Sumerian comparison",
    "Kinnier Wilson Indus script reading Indo-Aryan Sumerian",
    "Knorozov Indus script Proto-Dravidian decipherment USSR",
    "Wells Indus sign list concordance 2011 2015",
    "Mahadevan Indus sign concordance 1977 reading Tamil",
    "Parpola Indus sign value reading Dravidian 1994 2010",
    "Rao Indus Markov statistical sign analysis 2009 2015 2024",
    "Fuls ICIT Indus sign positional analysis 2024 2025",
    "Mukhopadhyay Indus script semasiographic fish gemstone 2019 2024",
    # Cluster 2: Meluhha bilingual
    "Meluhha personal name cuneiform Akkadian Sargonic record",
    "Meluhha merchant Akkadian text Ur Lagash Tell Asmar seal",
    "Shu-ilishu Meluhha interpreter Akkadian seal inscription",
    "CDLI Meluhha cuneiform text transliteration 2024 2025",
    "Indus seal impression Mesopotamia Ur Kish Nippur Tell Asmar",
    "Meluhha Dilmun Magan cuneiform trade text commodity",
    # Cluster 3: Missing phonemes
    "Proto-Dravidian retroflex lateral ḻ reconstruction DEDR",
    "Proto-Dravidian alveolar nasal ṉ trill ṟ reconstruction",
    "Proto-Dravidian palatal nasal ñ reconstruction Krishnamurti",
    "Proto-Dravidian voiced stops *b *d reconstruction evidence",
    "Dravidian phonological inventory complete reconstruction 2024 2025",
    "Krishnamurti Proto-Dravidian consonant system reconstruction 2003",
    # Cluster 4: Tamil-Brahmi continuity
    "Tamil Brahmi sign phonetic value aksara syllabary inventory",
    "Tamil Brahmi Keezhadi inscription sign value name 2024 2025 2026",
    "Tamil Brahmi Kodumanal Porunthal Arikamedu graffiti inscription",
    "Tamil Brahmi to Indus script sign continuity comparison",
    "Early Tamil writing system evolution pre-Ashokan Brahmi",
    # Cluster 5: Dravidian substrate
    "Dravidian substrate vocabulary Rigveda Sanskrit loanword",
    "Witzel Dravidian substrate pre-Aryan South Asian",
    "Southworth Dravidian substrate agriculture craft vocabulary",
    "Proto-Dravidian loanword Sanskrit flora fauna metal craft",
    "Dravidian etymological origin Sanskrit word borrowing evidence",
    # Cluster 6: Commodity seals
    "Indus seal tablet commodity trade weight marking",
    "Harappan seal workshop craft specialist pottery bead",
    "Indus sealing administrative economic function context",
    "Indus script seal function identity guild merchant trade",
    "Harappan weight system metrology cubical chert standard",
    # Cluster 7: Co-occurrence / positional
    "Indus sign co-occurrence bigram trigram positional frequency",
    "Indus inscription formula template repeating pattern",
    "Harappan seal text structure word boundary segmentation",
    "Indus sign initial terminal medial positional distribution",
    # Cluster 8: Information theory / cryptanalysis
    "Indus script entropy Shannon information linguistic test",
    "Indus script Zipf law frequency distribution sign",
    "undeciphered script information theory entropy bigram analysis",
    "cryptanalysis ancient script frequency substitution cipher",
    # Cluster 9: Numerals / metrology
    "Indus numeral stroke counting system decimal base",
    "Harappan number system numeral sign interpretation",
    "Indus weight metrological system standard ratio",
    # Cluster 10: Foreign site seals
    "Indus seal impression Ur Kish Nippur foreign context",
    "Indus type seal Gulf Bahrain Failaka Kuwait Oman",
    "round stamp seal Persian Gulf Indus Dilmun trade",
    "Harappan seal Central Asia Shortugai Mundigak BMAC",
    # Cluster 11: Old Tamil name morphology
    "Old Tamil personal name morphology Sangam literature",
    "Tamil personal name structure suffix aṉ āṉ aḷ iṉ",
    "Sangam Tamil inscription personal name analysis Mahadevan",
    "Tamil Brahmi name formula hero stone memorial inscription",
    # Cluster 12: Computational decipherment
    "Bayesian decipherment ancient script undeciphered 2024 2025 2026",
    "neural network decipherment ancient writing system transformer",
    "Luo Jaeger cognate detection Bayesian phylogenetic language",
    "machine learning undeciphered script decipherment 2025",
    "Berg Ravi Snyder decipherment statistical NLP computational 2024",
]

CROSSREF_QUERIES = [
    "Indus script sign reading proposal survey",
    "Fairservis Indus script writing system",
    "Meluhha personal name cuneiform Akkadian",
    "Proto-Dravidian phonological reconstruction retroflex",
    "Tamil Brahmi sign value phonetic inventory",
    "Dravidian substrate Rigvedic Sanskrit loanword",
    "Indus seal commodity trade administrative function",
    "Indus sign co-occurrence positional analysis",
    "Indus script entropy information theory linguistic",
    "Harappan numeral weight metrological system",
    "Indus seal impression Mesopotamia foreign site",
    "Old Tamil Sangam personal name morphology suffix",
    "Bayesian neural decipherment ancient script",
    "Shu-ilishu Meluhha interpreter seal Akkadian",
    "Keezhadi Tamil Brahmi inscription excavation 2025",
    "Krishnamurti Proto-Dravidian consonant 2003",
    "Indus seal text formula repeating pattern structure",
    "Mukhopadhyay Indus fish gemstone semasiographic",
    "Elamo-Dravidian McAlpin cognate phonological",
    "Wells Indus sign concordance frequency",
]

S2_QUERIES = [
    "Indus script sign value reading proposals all scholars survey",
    "Meluhha cuneiform personal name bilingual evidence",
    "Proto-Dravidian missing phonemes retroflex lateral alveolar",
    "Tamil Brahmi inscription sign value phonetic",
    "Dravidian substrate Sanskrit loanword",
    "Indus seal administrative function commodity trade",
    "Indus sign bigram trigram co-occurrence statistical",
    "information theory entropy Indus script linguistic test",
    "Harappan numeral metrological weight system",
    "Indus seal impression foreign Mesopotamia Gulf",
    "Sangam Tamil personal name morphology onomastics",
    "Bayesian neural decipherment undeciphered script 2024 2025",
    "Shu-ilishu Meluhha interpreter Akkadian inscription",
    "Indus script computational analysis NLP 2025 2026",
    "Keezhadi Kodumanal Tamil Brahmi graffiti inscription",
    "Proto-Dravidian phonological reconstruction Krishnamurti 2003",
]

ARXIV_QUERIES = [
    "Indus script decipherment computational",
    "Bayesian decipherment ancient writing",
    "neural network undeciphered script",
    "information theory ancient script linguistic test",
    "machine learning archaeological text analysis",
    "Proto-Dravidian computational linguistics",
    "ancient South Asian DNA archaeogenetics",
    "NLP undeciphered language decipherment",
    "Indus script statistical model entropy",
    "language identification ancient inscriptions",
    "sign language computational cryptanalysis ancient",
    "Dravidian phylogenetic computational model",
]

EUROPEPMC_QUERIES = [
    "Indus script decipherment reading proposal",
    "Meluhha cuneiform bilingual personal name",
    "Proto-Dravidian phonological reconstruction 2024",
    "Tamil Brahmi inscription sign value",
    "Harappan seal administrative economic function",
    "Bayesian decipherment ancient script computational",
    "Indus Valley trade commodity seal tablet",
    "Dravidian substrate Sanskrit loanword vocabulary",
]

ZENODO_QUERIES = [
    "Indus script sign reading decipherment",
    "Proto-Dravidian reconstruction phonological",
    "Tamil Brahmi inscription corpus",
    "Meluhha cuneiform text bilingual",
    "Harappan seal corpus computational analysis",
    "undeciphered script decipherment method",
]


# ── HTTP helpers ─────────────────────────────────────────────────────

def _get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "GlossaLab/0.2 (research; tpierson@bitconcepts.tech)"
            })
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception:
            time.sleep(RATE_SLEEP * (attempt + 1))
    return None


# ── Source harvesters ────────────────────────────────────────────────

def harvest_openalex(queries, bucket):
    """Harvest from OpenAlex API."""
    print(f"  OpenAlex: {len(queries)} queries...")
    for i, q in enumerate(queries):
        enc = urllib.parse.quote(q)
        cursor = "*"
        pages = 0
        while cursor and pages < MAX_PAGES and len(bucket) < TARGET * 2:
            url = (f"https://api.openalex.org/works?search={enc}"
                   f"&per-page={PAGE_SIZE}&cursor={cursor}"
                   f"&select=id,title,doi,publication_year,authorships,abstract_inverted_index"
                   f"&mailto=tpierson@bitconcepts.tech")
            data = _get_json(url)
            if not data or "results" not in data:
                break
            for w in data["results"]:
                title = w.get("title") or ""
                abstract = ""
                aii = w.get("abstract_inverted_index")
                if aii:
                    pairs = []
                    for word, positions in aii.items():
                        for pos in positions:
                            pairs.append((pos, word))
                    pairs.sort()
                    abstract = " ".join(w for _, w in pairs)

                score = _score_paper(title, abstract)
                if score > 0:
                    authors = []
                    for a in (w.get("authorships") or [])[:5]:
                        ad = a.get("author", {})
                        if ad.get("display_name"):
                            authors.append(ad["display_name"])

                    bucket.append({
                        "title": title,
                        "doi": w.get("doi", ""),
                        "year": w.get("publication_year"),
                        "authors": authors,
                        "score": score,
                        "source": "openalex",
                        "query_cluster": i // 6,  # map to cluster
                        "abstract_snippet": abstract[:500],
                    })
            cursor = data.get("meta", {}).get("next_cursor")
            pages += 1
            time.sleep(RATE_SLEEP)
        if (i + 1) % 10 == 0:
            print(f"    ... {i+1}/{len(queries)} queries, {len(bucket)} papers so far")
    print(f"    OpenAlex total: {len(bucket)} papers")


def harvest_crossref(queries, bucket):
    """Harvest from CrossRef API."""
    print(f"  CrossRef: {len(queries)} queries...")
    start_count = len(bucket)
    for i, q in enumerate(queries):
        enc = urllib.parse.quote(q)
        url = (f"https://api.crossref.org/works?query={enc}"
               f"&rows=100&mailto=tpierson@bitconcepts.tech")
        data = _get_json(url)
        if not data:
            continue
        items = data.get("message", {}).get("items", [])
        for item in items:
            title = " ".join(item.get("title", []))
            abstract = item.get("abstract", "")
            score = _score_paper(title, abstract)
            if score > 0:
                authors = []
                for a in (item.get("author") or [])[:5]:
                    name = f"{a.get('given', '')} {a.get('family', '')}".strip()
                    if name:
                        authors.append(name)
                bucket.append({
                    "title": title,
                    "doi": item.get("DOI", ""),
                    "year": (item.get("published-print", {}).get("date-parts") or
                             item.get("published-online", {}).get("date-parts") or [[None]])[0][0],
                    "authors": authors,
                    "score": score,
                    "source": "crossref",
                    "abstract_snippet": abstract[:500] if abstract else "",
                })
        time.sleep(RATE_SLEEP)
    print(f"    CrossRef added: {len(bucket) - start_count}")


def harvest_semantic_scholar(queries, bucket):
    """Harvest from Semantic Scholar API."""
    print(f"  SemanticScholar: {len(queries)} queries...")
    start_count = len(bucket)
    for i, q in enumerate(queries):
        enc = urllib.parse.quote(q)
        url = (f"https://api.semanticscholar.org/graph/v1/paper/search"
               f"?query={enc}&limit=100&fields=title,authors,year,externalIds,abstract")
        data = _get_json(url)
        if not data:
            continue
        for paper in data.get("data", []):
            title = paper.get("title") or ""
            abstract = paper.get("abstract") or ""
            score = _score_paper(title, abstract)
            if score > 0:
                authors = [a.get("name", "") for a in (paper.get("authors") or [])[:5]]
                ext_ids = paper.get("externalIds") or {}
                bucket.append({
                    "title": title,
                    "doi": ext_ids.get("DOI", ""),
                    "year": paper.get("year"),
                    "authors": authors,
                    "score": score,
                    "source": "semantic_scholar",
                    "abstract_snippet": abstract[:500] if abstract else "",
                })
        time.sleep(RATE_SLEEP * 3)  # S2 rate limit is stricter
    print(f"    S2 added: {len(bucket) - start_count}")


def harvest_arxiv(queries, bucket):
    """Harvest from arXiv API (Atom XML, parse manually)."""
    print(f"  arXiv: {len(queries)} queries...")
    start_count = len(bucket)
    for i, q in enumerate(queries):
        enc = urllib.parse.quote(q)
        url = f"http://export.arxiv.org/api/query?search_query=all:{enc}&max_results=100"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "GlossaLab/0.2 (research)"
            })
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                xml_text = r.read().decode("utf-8", errors="replace")
        except Exception:
            continue

        # Simple XML parsing for arXiv Atom feed
        entries = xml_text.split("<entry>")[1:]  # skip header
        for entry in entries:
            title_m = re.search(r"<title>(.*?)</title>", entry, re.S)
            summary_m = re.search(r"<summary>(.*?)</summary>", entry, re.S)
            title = title_m.group(1).strip().replace("\n", " ") if title_m else ""
            abstract = summary_m.group(1).strip().replace("\n", " ") if summary_m else ""
            score = _score_paper(title, abstract)
            if score > 0:
                authors = re.findall(r"<name>(.*?)</name>", entry)
                arxiv_id_m = re.search(r"<id>http://arxiv\.org/abs/(.*?)</id>", entry)
                bucket.append({
                    "title": title,
                    "doi": "",
                    "arxiv_id": arxiv_id_m.group(1) if arxiv_id_m else "",
                    "authors": authors[:5],
                    "score": score,
                    "source": "arxiv",
                    "abstract_snippet": abstract[:500],
                })
        time.sleep(RATE_SLEEP * 2)
    print(f"    arXiv added: {len(bucket) - start_count}")


def harvest_europepmc(queries, bucket):
    """Harvest from Europe PMC API."""
    print(f"  EuropePMC: {len(queries)} queries...")
    start_count = len(bucket)
    for q in queries:
        enc = urllib.parse.quote(q)
        url = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search"
               f"?query={enc}&format=json&pageSize=100&resultType=core")
        data = _get_json(url)
        if not data:
            continue
        for r in data.get("resultList", {}).get("result", []):
            title = r.get("title", "")
            abstract = r.get("abstractText", "")
            score = _score_paper(title, abstract)
            if score > 0:
                bucket.append({
                    "title": title,
                    "doi": r.get("doi", ""),
                    "year": r.get("pubYear"),
                    "authors": [r.get("authorString", "")][:5],
                    "score": score,
                    "source": "europepmc",
                    "abstract_snippet": abstract[:500] if abstract else "",
                })
        time.sleep(RATE_SLEEP)
    print(f"    EuropePMC added: {len(bucket) - start_count}")


def harvest_zenodo(queries, bucket):
    """Harvest from Zenodo API."""
    print(f"  Zenodo: {len(queries)} queries...")
    start_count = len(bucket)
    for q in queries:
        enc = urllib.parse.quote(q)
        url = f"https://zenodo.org/api/records?q={enc}&size=50&type=publication"
        data = _get_json(url)
        if not data:
            continue
        for hit in data.get("hits", {}).get("hits", []):
            meta = hit.get("metadata", {})
            title = meta.get("title", "")
            desc = meta.get("description", "")
            score = _score_paper(title, desc)
            if score > 0:
                creators = [c.get("name", "") for c in meta.get("creators", [])[:5]]
                bucket.append({
                    "title": title,
                    "doi": meta.get("doi", ""),
                    "year": (meta.get("publication_date") or "")[:4] or None,
                    "authors": creators,
                    "score": score,
                    "source": "zenodo",
                    "abstract_snippet": desc[:500],
                })
        time.sleep(RATE_SLEEP)
    print(f"    Zenodo added: {len(bucket) - start_count}")


# ── Deduplication & ranking ──────────────────────────────────────────

def deduplicate(bucket):
    """Deduplicate by DOI, then by normalized title."""
    seen_dois = set()
    seen_titles = set()
    unique = []
    for paper in sorted(bucket, key=lambda x: -x["score"]):
        doi = (paper.get("doi") or "").strip().lower()
        if doi and doi in seen_dois:
            continue
        norm_title = re.sub(r"\s+", " ", (paper.get("title") or "").lower().strip())
        if norm_title and norm_title in seen_titles:
            continue
        if doi:
            seen_dois.add(doi)
        if norm_title:
            seen_titles.add(norm_title)
        unique.append(paper)
    return unique


def extract_actionable_findings(papers):
    """Extract specific actionable findings from top papers."""
    findings = {
        "sign_reading_proposals": [],
        "meluhha_bilingual_evidence": [],
        "missing_phoneme_evidence": [],
        "tamil_brahmi_continuity": [],
        "dravidian_substrate": [],
        "commodity_trade_terms": [],
        "computational_methods": [],
        "metrological_evidence": [],
        "foreign_seal_contexts": [],
        "name_morphology": [],
    }

    for p in papers[:500]:  # analyze top-500 by score
        text = f"{p.get('title', '')} {p.get('abstract_snippet', '')}".lower()

        # Sign reading proposals
        if any(w in text for w in ["sign value", "reading propos", "phonetic value",
                                    "sign meaning", "sign identif"]):
            findings["sign_reading_proposals"].append({
                "title": p["title"], "doi": p.get("doi", ""),
                "authors": p.get("authors", []), "year": p.get("year")
            })

        # Meluhha bilingual
        if "meluhha" in text and any(w in text for w in ["bilingual", "personal name",
                                                          "akkadian", "cuneiform", "shu-ili"]):
            findings["meluhha_bilingual_evidence"].append({
                "title": p["title"], "doi": p.get("doi", ""),
                "authors": p.get("authors", []), "year": p.get("year")
            })

        # Missing phonemes
        if any(w in text for w in ["retroflex lateral", "alveolar nasal", "palatal nasal",
                                    "ḻ", "ṉ", "ṟ", "ñ", "*b", "*d"]):
            findings["missing_phoneme_evidence"].append({
                "title": p["title"], "doi": p.get("doi", ""),
                "authors": p.get("authors", []), "year": p.get("year")
            })

        # Tamil-Brahmi
        if "tamil brahmi" in text and any(w in text for w in ["sign", "value", "phonetic",
                                                               "syllable", "aksara", "keezhadi"]):
            findings["tamil_brahmi_continuity"].append({
                "title": p["title"], "doi": p.get("doi", ""),
                "authors": p.get("authors", []), "year": p.get("year")
            })

        # Substrate
        if "substrate" in text or ("loanword" in text and "dravidian" in text):
            findings["dravidian_substrate"].append({
                "title": p["title"], "doi": p.get("doi", ""),
                "authors": p.get("authors", []), "year": p.get("year")
            })

        # Computational
        if any(w in text for w in ["bayesian decipher", "neural decipher",
                                    "transformer decipher", "machine learning decipher"]):
            findings["computational_methods"].append({
                "title": p["title"], "doi": p.get("doi", ""),
                "authors": p.get("authors", []), "year": p.get("year")
            })

    return findings


# ── Main ─────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("PHASE 322: MEGA TARGETED MINE 5000+")
    print("=" * 70)

    bucket = []

    harvest_openalex(OA_QUERIES, bucket)
    harvest_crossref(CROSSREF_QUERIES, bucket)
    harvest_semantic_scholar(S2_QUERIES, bucket)
    harvest_arxiv(ARXIV_QUERIES, bucket)
    harvest_europepmc(EUROPEPMC_QUERIES, bucket)
    harvest_zenodo(ZENODO_QUERIES, bucket)

    print(f"\n  Raw total: {len(bucket)} papers")

    unique = deduplicate(bucket)
    print(f"  After dedup: {len(unique)} unique papers")

    # Score distribution
    score_dist = Counter(p["score"] for p in unique)
    source_dist = Counter(p["source"] for p in unique)

    # Top papers
    top50 = unique[:50]

    # Extract actionable findings
    findings = extract_actionable_findings(unique)

    result = {
        "phase": 322,
        "total_raw": len(bucket),
        "total_unique": len(unique),
        "score_distribution": dict(sorted(score_dist.items(), reverse=True)),
        "source_distribution": dict(source_dist),
        "query_clusters": {
            "1_scholar_readings": len(OA_QUERIES[:12]),
            "2_meluhha_bilingual": len(OA_QUERIES[12:18]),
            "3_missing_phonemes": len(OA_QUERIES[18:24]),
            "4_tamil_brahmi": len(OA_QUERIES[24:29]),
            "5_dravidian_substrate": len(OA_QUERIES[29:34]),
            "6_commodity_seals": len(OA_QUERIES[34:39]),
            "7_co_occurrence": len(OA_QUERIES[39:43]),
            "8_information_theory": len(OA_QUERIES[43:47]),
            "9_numerals_metrology": len(OA_QUERIES[47:50]),
            "10_foreign_seals": len(OA_QUERIES[50:54]),
            "11_name_morphology": len(OA_QUERIES[54:58]),
            "12_computational": len(OA_QUERIES[58:]),
        },
        "top_50_papers": [{
            "title": p["title"],
            "doi": p.get("doi", ""),
            "year": p.get("year"),
            "authors": p.get("authors", []),
            "score": p["score"],
            "source": p["source"],
        } for p in top50],
        "actionable_findings": {
            k: {"count": len(v), "papers": v[:10]}
            for k, v in findings.items()
        },
        "verdict": "",
    }

    # Build verdict
    n_readings = len(findings["sign_reading_proposals"])
    n_bilingual = len(findings["meluhha_bilingual_evidence"])
    n_phoneme = len(findings["missing_phoneme_evidence"])
    n_methods = len(findings["computational_methods"])

    result["verdict"] = (
        f"Phase 322: {len(unique)} unique papers mined from 6 sources. "
        f"Actionable: {n_readings} sign-reading proposals, "
        f"{n_bilingual} Meluhha bilingual evidence, "
        f"{n_phoneme} missing phoneme evidence, "
        f"{n_methods} computational methods. "
        f"Top score: {unique[0]['score'] if unique else 0}."
    )

    OUTPUTS.mkdir(exist_ok=True)
    out_path = OUTPUTS / "phase322_mega_mine_5000.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Output: {out_path}")
    print(f"  {result['verdict']}")
    return result


if __name__ == "__main__":
    main()
