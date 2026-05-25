"""Phase 202 — Bulk Mine 5000 (Fourth Run)

Fresh clusters targeting angles not covered in Phases 183, 184, or 196:
  - Dravidian personal name patterns (onomastics, Sangam Tamil names)
  - Indus trade goods in cuneiform records (Akkadian Meluhha mentions)
  - Munda/Austroasiatic substrate in Dravidian and Sanskrit
  - Elamite grammar morphology (SOV, agglutinative parallels with Dravidian)
  - Keezhadi excavations (Tamil Iron Age writing)
  - Gondi/Kolami/Konda — South-Central Dravidian sub-branches
  - South Indian megalithic culture and pre-Sangam population
  - Sumerian-Dravidian comparative hypotheses
  - IVC numerals and counting system vocabulary
  - 2024-2026 South Asian paleogenomics (not yet captured)
  - Balochi and Brahui contact linguistics
  - Deccan Neolithic continuity into Dravidian speakers
  - Harappan seals found in Mesopotamia (physical trade evidence)
  - Post-Harappan copper hoards and cultural continuity
  - Vedic vs Dravidian syntax comparison (SOV parallels)

Six tracks: OpenAlex (24), CrossRef (15), S2 (12),
arXiv (25 fixed XML), Wikipedia (13 new), CORE API.

Output: outputs/phase202_bulk_mine_5000.json
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
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

HTTP_TIMEOUT = 15
RATE_SLEEP   = 0.35
MAX_PAGES    = 8
PAGE_SIZE    = 200
TARGET       = 5000

STRONG_DRAVIDIAN = [
    re.compile(r"(?:Harapp[ae]n|IVC|Indus Valley).*(?:Dravidian|proto-Dravidian).*(?:ancestor|origin|spoke|language|speaker)", re.I | re.S),
    re.compile(r"(?:Dravidian|proto-Dravidian).*(?:Harapp[ae]n|IVC).*(?:ancestor|origin|genetic|population)", re.I | re.S),
    re.compile(r"AASI.*(?:Dravidian|proto-Dravidian|language)", re.I),
    re.compile(r"(?:ancient|Harapp[ae]n).*(?:genome|DNA|ancestry).*Dravidian", re.I | re.S),
    re.compile(r"Indus.*script.*Dravidian.*(?:confirm|support|evidence|ancestral|answer)", re.I | re.S),
    re.compile(r"(?:Dravidian|Tamil).*(?:Indus|Harapp).*(?:origin|language|ancestor|prove)", re.I | re.S),
    re.compile(r"Elamo.Dravidian.*(?:language|family|hypothesis|speaker)", re.I),
    re.compile(r"Keezhadi.*(?:Tamil|Dravidian|inscription|writing|ancient)", re.I),
    re.compile(r"Munda.*(?:Dravidian|substrate|ancient|contact|language|loan)", re.I),
    re.compile(r"Meluhha.*(?:cuneiform|Akkadian|Sumerian|trade|merchant|name)", re.I),
    re.compile(r"Dravidian.*(?:personal name|onomastic|given name|proper name)", re.I),
    re.compile(r"Elamite.*(?:Dravidian|SOV|agglutinative|morphology|syntax)", re.I),
]
MODERATE_EVIDENCE = [
    re.compile(r"(?:Harapp[ae]n|IVC|Indus Valley).*(?:ancestry|genome|aDNA|ancient DNA)", re.I),
    re.compile(r"South Asian.*(?:ancient DNA|archaeogenetics|population).*(?:Bronze Age|Chalcolithic|Neolithic)", re.I),
    re.compile(r"Indus.*(?:script|civilization).*(?:Dravidian|language|linguistic)", re.I),
    re.compile(r"(?:Proto-Dravidian|Tamil-Brahmi).*(?:reconstruct|ancestor|root|origin)", re.I),
    re.compile(r"Gondhi?.*(?:Dravidian|language|phoneme|South-Central)", re.I),
    re.compile(r"(?:Kolami|Konda|Kui|Kuvi).*(?:Dravidian|language|South-Central)", re.I),
    re.compile(r"South Indian megalithic.*(?:Dravidian|language|population|continuity)", re.I),
    re.compile(r"Deccan Neolithic.*(?:Dravidian|population|continuity|language)", re.I),
    re.compile(r"Keezhadi.*(?:excavation|archaeology|Tamil|ancient|2024|2025)", re.I),
    re.compile(r"Indus.*(?:seal|copper|Mesopotamia|Ur|Akkad|trade)", re.I),
    re.compile(r"Munda.*(?:Austroasiatic|substrate|loan|ancient|India)", re.I),
    re.compile(r"Balochi.*(?:Brahui|Dravidian|contact|language|loanword)", re.I),
    re.compile(r"(?:Sumerian|cuneiform).*(?:Dravidian|loan|contact|comparison)", re.I),
]
NEW_SIGN_PATTERNS = [
    re.compile(r"M?(\d{3})\s*[=:]\s*['\"]?([a-zāīūṭḍṇṅñḷṉṟ]{2,10})['\"]?", re.I),
    re.compile(r"sign\s+(\d{1,3})\s+(?:reads?|=|is)\s+['\"]?([a-zāīūṭḍṇṅñḷ]{2,10})['\"]?", re.I),
]


def _get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.1 (research; tpierson@bitconcepts.tech)"})
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


def _invert(inv):
    if not inv: return ""
    pos = {}
    for w, locs in inv.items():
        if isinstance(locs, list):
            for p in locs: pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))[:2000]


OA_CLUSTERS = [
    # Dravidian onomastics
    "Dravidian Tamil personal name ancient onomastics",
    "Sangam Tamil literature personal name historical",
    "proto-Dravidian personal name kinship term vocabulary",
    # Meluhha in cuneiform
    "Meluhha Akkadian cuneiform trade merchant Indus",
    "Indus seal Mesopotamia Ur excavation physical",
    "Harappan trader Susa Akkad cuneiform mention",
    # Munda substrate
    "Munda Austroasiatic substrate proto-Dravidian loanword ancient",
    "Munda Kharia Santhali Mundari ancient India contact",
    "Austroasiatic substrate Sanskrit Rigveda loan ancient",
    # Elamite grammar parallels
    "Elamite grammar SOV agglutinative suffix morphology",
    "Elamite verb morphology comparison Dravidian syntax",
    # Keezhadi
    "Keezhadi excavation Tamil ancient writing inscription",
    "Keezhadi Tamil Iron Age urbanization 2024 2025",
    # South-Central Dravidian
    "Gondi language Dravidian South-Central phoneme grammar",
    "Kolami Konda Kui Kuvi Dravidian language subgroup",
    # South Indian megalithic
    "South Indian megalithic culture iron age Dravidian",
    "Deccan Neolithic Brahmagiri Dravidian population continuity",
    # Sumerian comparison
    "Sumerian Dravidian comparison language contact Jacobsen",
    "cuneiform Dravidian loanword comparison ancient",
    # IVC numerals
    "Indus Valley numeral counting system mathematics binary",
    "Harappan weight numerical binary system decimal",
    # Balochi contact
    "Balochi Brahui contact loanword phoneme language",
    "post-Harappan copper hoard cultural continuity Iron Age",
    # New 2025-2026
    "Indus Valley genetic study 2025 new population",
]


def track_a_openalex():
    print("\n[Track A] OpenAlex (24 clusters)...")
    papers = []; seen = set(); deadline = time.time() + 600
    for q in OA_CLUSTERS:
        if time.time() > deadline or len(papers) >= TARGET: break
        encoded = urllib.parse.quote(q)
        page = 1
        while page <= MAX_PAGES and time.time() < deadline:
            url = (f"https://api.openalex.org/works?search={encoded}"
                   f"&per-page={PAGE_SIZE}&page={page}&mailto=tpierson@bitconcepts.tech")
            data = _get_json(url)
            if not data or not data.get("results"): break
            results = data["results"]
            if not results: break
            added = 0
            for item in results:
                oid = item.get("id", "")
                if oid in seen: continue
                seen.add(oid)
                title = item.get("display_name", "")
                year  = item.get("publication_year", 0)
                abstract = _invert(item.get("abstract_inverted_index") or {})
                papers.append({"source": "openalex_bulk", "id": oid, "title": title,
                                "year": year or 0, "text": f"{title} {abstract}".strip()})
                added += 1
            print(f"  OA '{q[:40]}' p{page}: +{added} (total {len(papers)})")
            meta = data.get("meta", {})
            if page * PAGE_SIZE >= meta.get("count", 0): break
            page += 1
            time.sleep(RATE_SLEEP)
        time.sleep(RATE_SLEEP)
    print(f"  [A] {len(papers)} papers")
    return papers


CROSSREF_QUERIES = [
    "Keezhadi Tamil ancient inscription writing excavation",
    "Munda Austroasiatic Dravidian substrate ancient loanword",
    "Meluhha Akkadian cuneiform Indus trader merchant",
    "Dravidian personal name onomastics ancient Sangam",
    "Elamite grammar agglutinative SOV Dravidian comparison",
    "Gondi Kolami Konda Kui Dravidian South-Central subgroup",
    "South Indian megalithic culture ancient population",
    "Deccan Neolithic Dravidian continuity archaeogenetics",
    "Sumerian Dravidian language comparison contact hypothesis",
    "Indus Valley numeral mathematical counting system",
    "Balochi Brahui contact loanword phoneme language",
    "post-Harappan copper hoard transition Iron Age",
    "South Asian paleogenomics steppe AASI 2024 2025 2026",
    "Indus seal Mesopotamia physical excavation cuneiform",
    "proto-Dravidian kinship term personal name reconstruction",
]


def track_b_crossref():
    print("\n[Track B] CrossRef (15 queries)...")
    papers = []; seen = set(); deadline = time.time() + 300
    for q in CROSSREF_QUERIES:
        if time.time() > deadline: break
        encoded = urllib.parse.quote(q)
        url = (f"https://api.crossref.org/works?query={encoded}&rows=100"
               f"&select=DOI,title,abstract,published,type&mailto=tpierson%40bitconcepts.tech")
        data = _get_json(url)
        if not data: time.sleep(RATE_SLEEP); continue
        items = (data.get("message") or {}).get("items", [])
        added = 0
        for item in items[:80]:
            doi = item.get("DOI", "")
            if doi in seen: continue
            seen.add(doi)
            titles = item.get("title", [])
            title  = titles[0] if titles else ""
            abstract = re.sub(r"<[^>]+>", " ", item.get("abstract", ""))[:2000]
            pub = item.get("published", {})
            dp = pub.get("date-parts", [[0]])
            year = dp[0][0] if dp and dp[0] else 0
            papers.append({"source": "crossref", "id": doi, "title": title,
                            "year": year or 0, "text": f"{title} {abstract}".strip(),
                            "url": f"https://doi.org/{doi}"})
            added += 1
        print(f"  CR '{q[:40]}': +{added}")
        time.sleep(RATE_SLEEP)
    print(f"  [B] {len(papers)} papers")
    return papers


S2_QUERIES = [
    "Keezhadi Tamil ancient writing urbanization excavation",
    "Munda Austroasiatic substrate ancient India Dravidian",
    "Meluhha Akkadian cuneiform Indus Valley merchant",
    "Elamite agglutinative grammar morphology Dravidian",
    "Gondi Kolami South-Central Dravidian language phonology",
    "South Indian megalithic iron age Dravidian ancient",
    "Sumerian cuneiform Dravidian comparative loan word",
    "Indus Valley numeral mathematics counting script",
    "Balochi Brahui contact loanword phoneme phonology",
    "Dravidian personal name ancient kinship term onomastics",
    "South Asia paleogenomics 2025 2026 steppe ancestry",
    "post-Harappan copper hoard cultural Bronze Iron Age",
]


def track_c_s2():
    print("\n[Track C] S2 deep (12 clusters)...")
    papers = []; seen = set(); deadline = time.time() + 360
    for q in S2_QUERIES:
        if time.time() > deadline: break
        for offset in range(0, 250, 50):
            if time.time() > deadline: break
            encoded = urllib.parse.quote(q)
            url = (f"https://api.semanticscholar.org/graph/v1/paper/search?"
                   f"query={encoded}&fields=title,abstract,year&limit=50&offset={offset}")
            data = _get_json(url)
            if not data or not data.get("data"): break
            items = data["data"]
            if not items: break
            for item in items:
                pid = item.get("paperId", "")
                if pid in seen: continue
                seen.add(pid)
                title = item.get("title", "")
                abstract = item.get("abstract") or ""
                year  = item.get("year", 0)
                papers.append({"source": "s2_deep", "id": pid, "title": title,
                                "year": year or 0, "text": f"{title} {abstract[:2000]}".strip()})
            time.sleep(RATE_SLEEP)
    print(f"  [C] {len(papers)} papers")
    return papers


ARXIV_QUERIES = [
    "Keezhadi Tamil ancient inscription NLP",
    "Munda Austroasiatic Dravidian substrate computational",
    "Elamite grammar SOV agglutinative computational",
    "Gondi Kolami Dravidian South-Central computational",
    "Meluhha cuneiform Akkadian Indus computational",
    "Sumerian Dravidian language comparison NLP",
    "South Indian megalithic ancient DNA archaeogenomics",
    "Dravidian personal name historical computational NLP",
    "Indus Valley mathematics numeral counting",
    "Balochi Brahui contact phoneme computational",
    "South Asia ancient DNA 2025 2026 archaeogenomics",
    "Deccan Neolithic ancient population genetics",
    "post-Harappan cultural continuity ancient",
    "proto-Dravidian kinship term reconstruction",
    "Indus seal Mesopotamia trade computational",
    "South Asian paleogenomics steppe admixture recent",
    "Dravidian SOV syntax comparison historical",
    "Elamite Dravidian cognate vocabulary computational",
    "Tamil ancient inscription computational NLP 2025",
    "Keezhadi archaeology Tamil 2024 2025 new",
    "Munda loan word ancient India subcontinent",
    "Indus script decipherment Dravidian evidence 2025",
    "South India iron age ancient DNA genome",
    "Harappan trade route Gulf Oman Arabia ancient",
    "Brahui Balochi language contact loanword phoneme",
]


def track_d_arxiv():
    print("\n[Track D] arXiv (25 queries)...")
    papers = []; seen = set(); deadline = time.time() + 300
    for q in ARXIV_QUERIES:
        if time.time() > deadline: break
        encoded = urllib.parse.quote(q)
        url = (f"http://export.arxiv.org/api/query?"
               f"search_query=all:{encoded}&start=0&max_results=40"
               f"&sortBy=relevance&sortOrder=descending")
        raw = _get_raw(url)
        if not raw: time.sleep(RATE_SLEEP); continue
        entries = re.findall(r"<entry>(.*?)</entry>", raw, re.S)
        added = 0
        for entry in entries:
            id_m  = re.search(r"<id>https?://arxiv\.org/abs/([^<\s]+)</id>", entry)
            title_m = re.search(r"<title[^>]*>([^<]+)</title>", entry)
            summ_m  = re.search(r"<summary[^>]*>(.*?)</summary>", entry, re.S)
            year_m  = re.search(r"<published>(\d{4})", entry)
            if not id_m: continue
            arxiv_id = id_m.group(1).strip()
            if arxiv_id in seen: continue
            seen.add(arxiv_id)
            title    = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
            abstract = re.sub(r"\s+", " ", summ_m.group(1)).strip()[:2000] if summ_m else ""
            year     = int(year_m.group(1)) if year_m else 0
            papers.append({"source": "arxiv_bulk", "id": arxiv_id, "title": title,
                            "year": year, "text": f"{title} {abstract}".strip(),
                            "url": f"https://arxiv.org/abs/{arxiv_id}"})
            added += 1
        print(f"  arXiv '{q[:40]}': +{added}")
        time.sleep(RATE_SLEEP)
    print(f"  [D] {len(papers)} papers")
    return papers


WIKI_ARTICLES = [
    "Keezhadi_excavations",
    "Munda_languages",
    "Gondi_language",
    "Kolami_language",
    "South_Indian_megalithic_culture",
    "Deccan_Neolithic",
    "Meluhha",
    "Elamite_language_grammar",
    "Tamil_personal_names",
    "Harappan_trade",
    "Copper_hoard_culture",
    "Iron_Age_India",
    "Sangam_literature",
]


def track_e_wikipedia():
    print("\n[Track E] Wikipedia (13 articles)...")
    papers = []; seen = set(); deadline = time.time() + 240
    for article in WIKI_ARTICLES:
        if time.time() > deadline: break
        encoded = urllib.parse.quote(article)
        url = (f"https://en.wikipedia.org/w/api.php?"
               f"action=query&prop=revisions&rvprop=content&format=json"
               f"&titles={encoded}&rvslots=main")
        data = _get_json(url)
        if not data: time.sleep(RATE_SLEEP); continue
        pages = data.get("query", {}).get("pages", {})
        content = ""
        for page_data in pages.values():
            rev = page_data.get("revisions", [{}])
            slots = rev[0].get("slots", {}).get("main", {}) if rev else {}
            content = slots.get("*", ""); break
        if not content: time.sleep(RATE_SLEEP); continue
        title_matches = re.findall(r"\|\s*title\s*=\s*([^\|\}\n]+)", content)
        year_matches  = re.findall(r"\|\s*year\s*=\s*(\d{4})", content)
        doi_matches   = re.findall(r"\|\s*doi\s*=\s*([^\|\}\s\n]+)", content)
        url_matches   = re.findall(r"\|\s*url\s*=\s*(https?://[^\|\}\s\n]+)", content)
        added = 0
        for i, title in enumerate(title_matches[:200]):
            title = title.strip()
            if not title or len(title) < 5: continue
            doi     = doi_matches[i] if i < len(doi_matches) else ""
            year_r  = year_matches[i] if i < len(year_matches) else ""
            year    = int(year_r) if year_r.isdigit() else 0
            ref_url = url_matches[i] if i < len(url_matches) else ""
            ref_id  = doi or ref_url or f"wiki_{article}_{i}"
            if ref_id in seen: continue
            seen.add(ref_id)
            papers.append({"source": "wikipedia_refs", "id": ref_id, "title": title,
                            "year": year, "text": title,
                            "url": f"https://doi.org/{doi}" if doi else ref_url})
            added += 1
        print(f"  Wiki '{article[:40]}': +{added}")
        time.sleep(RATE_SLEEP)
    print(f"  [E] {len(papers)} papers")
    return papers


CORE_QUERIES = [
    "Keezhadi Tamil ancient inscription",
    "Munda Austroasiatic Dravidian substrate",
    "Elamite grammar Dravidian comparison",
    "South Indian megalithic Dravidian",
    "Meluhha cuneiform Akkadian ancient",
    "Gondi Kolami South-Central Dravidian",
    "Dravidian onomastics personal name ancient",
    "South Asia ancient DNA paleogenomics 2024",
]


def track_f_core():
    print("\n[Track F] CORE API...")
    papers = []; seen = set(); deadline = time.time() + 180
    for q in CORE_QUERIES:
        if time.time() > deadline: break
        encoded = urllib.parse.quote(q)
        url = f"https://api.core.ac.uk/v3/search/works?q={encoded}&limit=50"
        data = _get_json(url)
        if not data: time.sleep(RATE_SLEEP); continue
        results = data.get("results") or []
        added = 0
        for item in results:
            core_id = str(item.get("id", ""))
            if core_id in seen: continue
            seen.add(core_id)
            title    = item.get("title", "") or ""
            abstract = item.get("abstract", "") or ""
            year     = item.get("yearPublished", 0) or 0
            papers.append({"source": "core_api", "id": core_id, "title": title,
                            "year": year, "text": f"{title} {abstract[:2000]}".strip(),
                            "url": item.get("downloadUrl", "")})
            added += 1
        print(f"  CORE '{q[:40]}': +{added}")
        time.sleep(RATE_SLEEP)
    print(f"  [F] {len(papers)} papers")
    return papers


def _classify(paper):
    text = paper.get("text", "")
    for pat in STRONG_DRAVIDIAN:
        if pat.search(text): return "strong"
    for pat in MODERATE_EVIDENCE:
        if pat.search(text): return "moderate"
    return "weak"


def _extract_proposals(papers):
    proposals = []
    for p in papers:
        text = p.get("text", "")
        for pat in NEW_SIGN_PATTERNS:
            for m in pat.finditer(text):
                if len(m.groups()) >= 2:
                    proposals.append({
                        "sign": f"M{m.group(1).zfill(3)}" if m.group(1).isdigit() else m.group(1),
                        "phoneme": m.group(2)[:10],
                        "source": p.get("title", "")[:60],
                        "year": p.get("year", 0),
                        "context": text[max(0, m.start()-50): m.end()+80],
                    })
    return proposals[:60]


def main():
    t0 = time.time()
    print("=" * 60)
    print("Phase 202 — Bulk Mine 5000 (Fourth Run: Onomastics/Munda/Keezhadi)")
    print("=" * 60)

    all_papers = []
    all_papers += track_a_openalex()
    all_papers += track_b_crossref()
    all_papers += track_c_s2()
    all_papers += track_d_arxiv()
    all_papers += track_e_wikipedia()
    all_papers += track_f_core()

    strong, moderate, weak = [], [], []
    for p in all_papers:
        cls = _classify(p)
        if cls == "strong": strong.append(p)
        elif cls == "moderate": moderate.append(p)
        else: weak.append(p)

    proposals = _extract_proposals(strong + moderate)
    cumulative = 211 + 5 + 80 + 41 + 166 + 183 + 6376 + 2486 + 2336 + len(all_papers)

    elapsed = round(time.time() - t0, 1)
    print(f"\n{'='*60}")
    print(f"Phase 202 complete in {elapsed}s")
    print(f"  Papers:       {len(all_papers)}")
    print(f"  STRONG:       {len(strong)}")
    print(f"  MODERATE:     {len(moderate)}")
    print(f"  Sign proposals: {len(proposals)}")
    print(f"  Total all phases: {cumulative}")

    result = {
        "phase": 202,
        "n_papers": len(all_papers),
        "n_strong_evidence": len(strong),
        "n_moderate_evidence": len(moderate),
        "n_weak_evidence": len(weak),
        "total_papers_mined_all_phases": cumulative,
        "elapsed_seconds": elapsed,
        "tracks": {
            "openalex_bulk":  sum(1 for p in all_papers if p["source"] == "openalex_bulk"),
            "crossref":       sum(1 for p in all_papers if p["source"] == "crossref"),
            "s2_deep":        sum(1 for p in all_papers if p["source"] == "s2_deep"),
            "arxiv_bulk":     sum(1 for p in all_papers if p["source"] == "arxiv_bulk"),
            "wikipedia_refs": sum(1 for p in all_papers if p["source"] == "wikipedia_refs"),
            "core_api":       sum(1 for p in all_papers if p["source"] == "core_api"),
        },
        "evidence": {
            "strong":         strong[:30],
            "moderate":       moderate[:50],
            "sign_proposals": proposals,
        },
    }

    out = OUTPUTS / "phase202_bulk_mine_5000.json"
    out.write_text(json.dumps(result, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "phase202_bulk_mine_5000.json").write_text(
        json.dumps(result, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
