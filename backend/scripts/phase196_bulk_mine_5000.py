"""Phase 196 — Bulk Mine 5000 (Third Run)

Entirely fresh clusters targeting the specific gaps identified after Phase 195:
  - McAlpin 1981/follow-up responses and critiques of Elamo-Dravidian
  - Brahui contact studies (Persian, Balochi, Sindhi)
  - South Asian aDNA 2024-2026 (latest genomics)
  - Indus weights, measures, copper tablets, short inscriptions
  - Script direction and reading order (new computational approaches)
  - Zvelebil / Krishnamurti follow-up papers on PDr reconstruction
  - Dravidian substrate loans in Vedic Sanskrit (phoneme inventory)
  - 2025-2026 Indus preprints not captured in phases 183/184
  - Rakhigarhi 2024 follow-up papers
  - IVC collapse / post-urban continuity
  - McAlpin 57-cognate extension papers and counter-arguments

Six tracks: OpenAlex (24 new clusters), CrossRef (15), S2 (12),
arXiv (25 fixed XML), Wikipedia (13 new articles), CORE API.

Output: outputs/phase196_bulk_mine_5000.json
"""
from __future__ import annotations
import json, re, time, urllib.parse, urllib.request
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
    re.compile(r"McAlpin.*(?:Dravidian|Elamite|cognate|proto)", re.I),
    re.compile(r"Brahui.*(?:Dravidian|Pakistan|ancient|origin|language|genetic)", re.I),
    re.compile(r"(?:fish|min|meen).*(?:sign|Indus|rebus|Tamil|phoneme)", re.I),
    re.compile(r"proto-Dravidian.*(?:reconstruction|phoneme|cognate|ancestral|sound)", re.I),
]
MODERATE_EVIDENCE = [
    re.compile(r"(?:Harapp[ae]n|IVC|Indus Valley).*(?:ancestry|genome|aDNA|ancient DNA)", re.I),
    re.compile(r"South Asian.*(?:ancient DNA|archaeogenetics|population).*(?:Bronze Age|Chalcolithic|Neolithic)", re.I),
    re.compile(r"Rakhigarhi.*(?:genome|DNA|ancestry|language|Dravidian|2024|2025)", re.I),
    re.compile(r"Indus.*(?:script|civilization).*(?:Dravidian|language|linguistic)", re.I),
    re.compile(r"(?:Proto-Dravidian|Tamil-Brahmi).*(?:reconstruct|ancestor|root|origin)", re.I),
    re.compile(r"Brahui.*(?:Dravidian|Pakistan|isolate|language|Persian|contact)", re.I),
    re.compile(r"steppe.*(?:India|South Asia).*(?:Indo-Aryan|Dravidian|admixture)", re.I),
    re.compile(r"Dravidian.*(?:substrate|loan|Sanskrit|Vedic|contact|phoneme)", re.I),
    re.compile(r"(?:Elamite|proto-Elamite).*(?:Dravidian|Indus|contact|language)", re.I),
    re.compile(r"Indus.*(?:weight|tablet|copper|short|inscription|measure|seal)", re.I),
    re.compile(r"Zvelebil.*(?:Dravidian|Tamil|language|linguistics|reconstruction)", re.I),
    re.compile(r"Krishnamurti.*(?:Dravidian|language|comparative|reconstruction)", re.I),
]
NEW_SIGN_PATTERNS = [
    re.compile(r"M?(\d{3})\s*[=:]\s*['\"]?([a-zāīūṭḍṇṅñḷṉṟ]{2,10})['\"]?", re.I),
    re.compile(r"sign\s+(\d{1,3})\s+(?:reads?|=|is)\s+['\"]?([a-zāīūṭḍṇṅñḷ]{2,10})['\"]?", re.I),
    re.compile(r"proto-Dravidian\s+\*([a-zāīūṭḍṇ]{2,8})-?\s+(?:cognate|=|:)\s+(?:Elamite\s+)?([a-z]{2,8})", re.I),
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


# ── Track A: OpenAlex — 24 fresh clusters ─────────────────────────────────────
OA_CLUSTERS = [
    # McAlpin Elamo-Dravidian follow-up
    "McAlpin proto-Elamo-Dravidian language cognate Elamite",
    "Elamo-Dravidian hypothesis criticism response linguistics",
    "McAlpin 1974 Elamite Dravidian cognate vocabulary",
    # Brahui contact studies
    "Brahui language contact Persian Balochi Sindhi loanword",
    "Brahui Dravidian Pakistan linguist isolated community",
    "North Dravidian Kurukh Malto Gondi comparative phonology",
    # Latest aDNA 2024-2026
    "South Asian ancient DNA 2024 archaeogenomics Bronze Age steppe",
    "Rakhigarhi ancient genome 2024 2025 Harappan population",
    "India archaeogenetics steppe ancestry ANI ASI admixture 2024 2025",
    # Indus short inscriptions + tablets
    "Indus Valley copper tablet short inscription unique sign",
    "Indus weights binary system Harappan metrology balance",
    "Indus clay tablet writing administrative record",
    # Script direction and reading order
    "Indus script reading direction left right boustrophedon",
    "Indus inscription reading order computational direction detection",
    # Zvelebil + Krishnamurti works
    "Zvelebil Tamil language ancient comparative linguistics Dravidian",
    "Krishnamurti Dravidian languages comparative reconstruction",
    "proto-Dravidian phoneme inventory consonant vowel system",
    # Dravidian substrate in Vedic Sanskrit
    "Dravidian substrate loan Vedic Sanskrit Rigveda phoneme",
    "Indo-Aryan Dravidian language contact ancient India absorption",
    # IVC collapse post-urban continuity
    "Indus Valley Civilization collapse 2000 BCE post-urban continuity",
    "Harappan late period Cemetery H Painted Grey Ware successor",
    # 2025-2026 not yet mined
    "Indus script reading decipherment proposal 2025",
    "Harappan genetic study genomic ancient 2025 2026",
    "proto-Dravidian Indus ancestral population convergence",
]


def track_a_openalex():
    print("\n[Track A] OpenAlex (24 new clusters)...")
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


# ── Track B: CrossRef — 15 fresh queries ──────────────────────────────────────
CROSSREF_QUERIES = [
    "McAlpin Elamo-Dravidian language proto cognate",
    "Zvelebil Tamil Dravidian ancient literature linguistic",
    "Krishnamurti Dravidian languages comparative grammar",
    "Brahui Dravidian contact loanword Persian Pakistan",
    "proto-Dravidian consonant phoneme reconstruction sound change",
    "Dravidian substrate Sanskrit Vedic Rigveda loanword phoneme",
    "Rakhigarhi ancient DNA genome Harappan 2024",
    "South Asia archaeogenetics 2024 2025 Bronze Age population",
    "Indus copper tablet inscription rare unique sign",
    "Indus Valley civilization collapse aridification 4.2 kya",
    "Indus script reading order direction computational analysis",
    "Harappan Cemetery H late period successor culture",
    "North Dravidian Kurukh Gondi Malto language comparison",
    "Dravidian family tree subgroup classification phylogeny",
    "India population history ancient Neolithic Dravidian ANI ASI",
]


def track_b_crossref():
    print("\n[Track B] CrossRef (15 new queries)...")
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


# ── Track C: S2 — 12 fresh clusters ───────────────────────────────────────────
S2_QUERIES = [
    "McAlpin Elamite Dravidian cognate vocabulary comparison",
    "Brahui language Dravidian Pakistan isolate ancient",
    "Zvelebil Dravidian phonology vowel consonant reconstruction",
    "proto-Dravidian Indus Harappan ancestral language speaker",
    "South Asia ancient DNA steppe ancestry 2024 2025 genome",
    "Rakhigarhi Harappan ancient DNA population structure recent",
    "Indus Valley Civilization writing system direction reading",
    "Dravidian substrate Sanskrit loanword phoneme ancient",
    "Indus copper tablet inscription administrative weight",
    "Harappan post-urban Cemetery H Painted Grey Ware continuity",
    "Dravidian language family phylogenetics subgrouping",
    "IVC collapse aridification monsoon 4.2 kiloyear event",
]


def track_c_s2():
    print("\n[Track C] S2 deep (12 new clusters)...")
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


# ── Track D: arXiv — 25 new queries (fixed XML parser) ─────────────────────────
ARXIV_QUERIES = [
    "Elamo-Dravidian language family computational",
    "McAlpin Elamite Dravidian NLP cognate",
    "Brahui language computational classification",
    "proto-Dravidian reconstruction phoneme NLP",
    "South Asian ancient DNA archaeogenomics 2024",
    "Rakhigarhi genome population structure recent",
    "Indus Valley script computational reading direction",
    "Dravidian substrate Sanskrit loanword computational",
    "Harappan civilization collapse monsoon climate model",
    "India archaeogenomics Bronze Age steppe farmer 2025",
    "ancient DNA South Asia Dravidian Austroasiatic",
    "Indus script sign frequency entropy information",
    "Tamil language NLP historical ancient computational",
    "Dravidian phylogenetics language subgroup tree",
    "proto-language reconstruction computational Dravidian",
    "Indus Valley copper tablet inscription analysis",
    "Harappan weight system metrology computational",
    "South Asian population genetics ancient modern 2024",
    "Indus decipherment mathematical formal approach 2026",
    "Dravidian Vedic Sanskrit substrate contact phoneme",
    "Rakhigarhi ancient genome Harappan 2024 archaeo",
    "ancient South Asian DNA population admixture steppe farmer",
    "Brahui Dravidian Pakistan ancient origin genetic",
    "IVC Indus Valley Civilization genomics recent study",
    "Dravidian language family origin divergence date estimate",
]


def track_d_arxiv():
    print("\n[Track D] arXiv (25 queries, fixed XML)...")
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


# ── Track E: Wikipedia — 13 fresh articles ────────────────────────────────────
WIKI_ARTICLES = [
    "McAlpin_Elamo-Dravidian_hypothesis",
    "Dravidian_languages_subgroups",
    "Kurukh_language",
    "Gondi_language",
    "Brahui_people",
    "Cemetery_H_culture",
    "Painted_Grey_Ware_culture",
    "Indus_Valley_Civilisation_decline",
    "Proto-Indo-Aryan_language",
    "Vedic_Sanskrit_phonology",
    "Harappan_weights_and_measures",
    "Indus_script_direction",
    "Rakhigarhi",
]


def track_e_wikipedia():
    print("\n[Track E] Wikipedia (13 new articles)...")
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


# ── Track F: CORE (try with standard API key workaround) ──────────────────────
CORE_QUERIES = [
    "McAlpin Elamo-Dravidian cognate Elamite",
    "Brahui Dravidian language ancient Pakistan",
    "proto-Dravidian reconstruction phoneme",
    "Rakhigarhi ancient genome Harappan",
    "Indus script decipherment Dravidian",
    "Zvelebil Tamil Dravidian linguistics",
    "South Asia ancient DNA Bronze Age steppe",
    "Dravidian substrate Sanskrit loanword",
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
    print("Phase 196 — Bulk Mine 5000 (Third Run, McAlpin/Brahui/aDNA)")
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
    cumulative = 211 + 5 + 80 + 41 + 166 + 183 + 6376 + 2486 + len(all_papers)

    elapsed = round(time.time() - t0, 1)
    print(f"\n{'='*60}")
    print(f"Phase 196 complete in {elapsed}s")
    print(f"  Papers:       {len(all_papers)}")
    print(f"  STRONG:       {len(strong)}")
    print(f"  MODERATE:     {len(moderate)}")
    print(f"  Sign proposals: {len(proposals)}")
    print(f"  Total all phases: {cumulative}")

    result = {
        "phase": 196,
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

    out = OUTPUTS / "phase196_bulk_mine_5000.json"
    out.write_text(json.dumps(result, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "phase196_bulk_mine_5000.json").write_text(
        json.dumps(result, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
