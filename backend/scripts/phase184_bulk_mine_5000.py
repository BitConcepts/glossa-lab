"""Phase 184 — Bulk Mine 5000 (second bulk run)

Entirely fresh query clusters not covered in Phase 183.
Six tracks targeting previously unmined territory:

  Track A: OpenAlex — 22 new clusters (economy, iconography, substrate, sites,
           Elam, BMAC, fish-sign phonology, rebus, metallurgy, Munda)

  Track B: CrossRef — 15 new queries (Dravidian sub-branches, Elamite,
           weights, allograph, substrate loans, archaeobotany)

  Track C: S2 — 12 new clusters (Elamo-Dravidian, Brahui, DEDR cognates,
           Parpola corpus, steppe aDNA 2024-2026)

  Track D: arXiv — fixed XML parser, 25 new cs.CL + q-bio.PE queries

  Track E: Wikipedia — 13 new articles not mined in Phase 183
           (Elamo-Dravidian, Tamil Brahmi, Dholavira, Lothal, Brahui,
            Linear A, Elamite, BMAC, Meluhha, Bronze Age India)

  Track F: CORE API (open-access repository) — new source entirely

Evidence pipeline: same STRONG/MODERATE/WEAK classifier as Phases 181-183.

Output: outputs/phase184_bulk_mine_5000.json
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

# ── H11 caps ────────────────────────────────────────────────────────────────
HTTP_TIMEOUT = 15
RATE_SLEEP   = 0.35
MAX_PAGES    = 8
PAGE_SIZE    = 200
TARGET       = 5000

# ── Evidence patterns (consistent with Phases 181-183) ───────────────────────
STRONG_DRAVIDIAN = [
    re.compile(r"(?:Harapp[ae]n|IVC|Indus Valley).*(?:Dravidian|proto-Dravidian).*(?:ancestor|origin|spoke|language|speaker)", re.I | re.S),
    re.compile(r"(?:Dravidian|proto-Dravidian).*(?:Harapp[ae]n|IVC).*(?:ancestor|origin|genetic|population)", re.I | re.S),
    re.compile(r"AASI.*(?:Dravidian|proto-Dravidian|language)", re.I),
    re.compile(r"(?:ancient|Harapp[ae]n).*(?:genome|DNA|ancestry).*Dravidian", re.I | re.S),
    re.compile(r"Indus.*script.*Dravidian.*(?:confirm|support|evidence|ancestral|answer)", re.I | re.S),
    re.compile(r"(?:Dravidian|Tamil).*(?:Indus|Harapp).*(?:origin|language|ancestor|prove)", re.I | re.S),
    re.compile(r"Elamo.Dravidian.*(?:language|family|hypothesis|speaker)", re.I),
    re.compile(r"fish.*sign.*(?:Tamil|Dravidian|phoneme|rebus|min|meen)", re.I | re.S),
    re.compile(r"rebus.*(?:Indus|Harapp).*(?:Tamil|Dravidian|phoneme|sign)", re.I | re.S),
]
MODERATE_EVIDENCE = [
    re.compile(r"(?:Harapp[ae]n|IVC|Indus Valley).*(?:ancestry|genome|aDNA|ancient DNA)", re.I),
    re.compile(r"South Asian.*(?:ancient DNA|archaeogenetics|population).*(?:Bronze Age|Chalcolithic|Neolithic)", re.I),
    re.compile(r"(?:AASI|Ancient Ancestral South Indian).*(?:ancestry|genetic|proportion)", re.I),
    re.compile(r"Indus.*(?:script|civilization).*(?:Dravidian|language|linguistic)", re.I),
    re.compile(r"(?:Proto-Dravidian|Tamil-Brahmi).*(?:reconstruct|ancestor|root|origin)", re.I),
    re.compile(r"Rakhigarhi.*(?:genome|DNA|ancestry|language|Dravidian)", re.I),
    re.compile(r"(?:Indus|Harapp).*(?:sign|decipherment).*(?:reading|phoneme|rebus|Dravidian)", re.I),
    re.compile(r"Brahui.*(?:Dravidian|Pakistan|isolate|language)", re.I),
    re.compile(r"BMAC.*(?:Indus|Harapp|contact|Bronze Age|language)", re.I),
    re.compile(r"steppe.*(?:India|South Asia).*(?:Indo-Aryan|Dravidian|admixture)", re.I),
    re.compile(r"Dravidian.*(?:substrate|loan|Sanskrit|Vedic|contact)", re.I),
    re.compile(r"(?:Elamite|proto-Elamite).*(?:Dravidian|Indus|contact|language)", re.I),
    re.compile(r"Indus.*(?:weight|metrology|count|number).*(?:trade|system|standard)", re.I),
    re.compile(r"Harappan.*(?:copper|bronze|trade|ivory|lapis).*(?:network|route|source)", re.I),
]
NEW_SIGN_PATTERNS = [
    re.compile(r"M?(\d{3})\s*[=:]\s*['\"]?([a-zāīūṭḍṇṅñḷṉṟ]{2,8})['\"]?", re.I),
    re.compile(r"sign\s+(\d{1,3})\s+(?:reads?|=|is)\s+['\"]?([a-zāīūṭḍṇṅñḷ]{2,8})['\"]?", re.I),
    re.compile(r"(?:P|M)-?(\d{3})\s+(?:reads?|=|represents?)\s+['\"]?([a-zāīūṭḍṇṅñḷ]{2,8})['\"]?", re.I),
    re.compile(r"fish sign.*?([a-zāīūṭḍṇṅñḷ]{2,8})\s+(?:Tamil|Dravidian|phoneme)", re.I),
]


def _get_json(url: str) -> dict | list | None:
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "GlossaLab/0.1 (research; tpierson@bitconcepts.tech)"}
            )
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception:  # noqa: BLE001
            time.sleep(RATE_SLEEP * (attempt + 1))
    return None


def _get_raw(url: str) -> str:
    """Fetch raw bytes as string — does NOT strip tags (for XML feeds)."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "GlossaLab/0.1"}
            )
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            time.sleep(RATE_SLEEP * (attempt + 1))
    return ""


def _invert(inv: dict) -> str:
    if not inv:
        return ""
    pos: dict[int, str] = {}
    for w, locs in inv.items():
        if isinstance(locs, list):
            for p in locs:
                pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))[:2000]


# ── Track A: OpenAlex — 22 fresh clusters ─────────────────────────────────────

OA_QUERY_CLUSTERS = [
    # Fish-sign and rebus phonology (new angle)
    "fish sign Tamil phoneme rebus Indus script",
    "rebus writing system Harappan pictographic sign phoneme",
    # Iconographic / semantic origins
    "Indus script zoomorphic iconographic animal sign origin",
    "Harappan seal motif unicorn fish deity interpretation",
    # Economy / weights / numerals
    "Harappan weight stone cuboid metrology bronze age",
    "Indus Valley numerals counting system tablet",
    # Substrate and contact
    "Dravidian substrate Indo-Aryan loan word Vedic Sanskrit",
    "Munda Austroasiatic Dravidian substrate ancient India",
    # Elam / BMAC
    "Elamite proto-Elamite Indus Valley script contact comparison",
    "BMAC Bactria Margiana Archaeological Complex Indus contact language",
    # Regional sites
    "Dholavira Lothal Kalibangan Banawali inscription seal",
    "Shortugai Afghanistan Harappan frontier outpost sign",
    # Brahui and isolated Dravidian
    "Brahui Dravidian Balochistan Pakistan isolate language ancient",
    # Sub-branches of Dravidian
    "Kannada Telugu Malayalam ancient inscription epigraphy Dravidian",
    "Gondi Kurukh Brahu Kolami south-central Dravidian",
    # Comparative undeciphered scripts
    "Linear A Minoan undeciphered script comparison Indus",
    "Proto-Sinaitic Indus Valley script comparison Bronze Age",
    # Archaeobotany / agriculture vocabulary
    "Harappan archaeobotany crop grain cotton sesame vocabulary",
    # Trade materials / lapis lazuli
    "lapis lazuli carnelian Indus trade Afghanistan mine Bronze Age",
    # Climate / migration links
    "4.2 kiloyear event climate Indus Valley Harappan collapse",
    # Recent papers 2025 2026
    "Indus script decipherment 2025 2026 new proposal",
    "Harappan genome ancient 2025 2026 archaeogenetics",
]


def track_a_openalex_bulk() -> list[dict]:
    """OpenAlex paginated — up to PAGE_SIZE × MAX_PAGES per query."""
    print("\n[Track A] OpenAlex bulk paginated (22 new clusters)...")
    papers = []
    seen: set = set()
    deadline = time.time() + 600

    for q in OA_QUERY_CLUSTERS:
        if time.time() > deadline or len(papers) >= TARGET:
            break
        encoded = urllib.parse.quote(q)
        page = 1
        while page <= MAX_PAGES and time.time() < deadline:
            url = (
                f"https://api.openalex.org/works?"
                f"search={encoded}&per-page={PAGE_SIZE}&page={page}"
                f"&mailto=tpierson@bitconcepts.tech"
            )
            data = _get_json(url)
            if not data or not data.get("results"):
                break
            results = data["results"]
            if not results:
                break
            added = 0
            for item in results:
                oid = item.get("id", "")
                if oid in seen:
                    continue
                seen.add(oid)
                title = item.get("display_name", "")
                year  = item.get("publication_year", 0)
                inv   = item.get("abstract_inverted_index") or {}
                abstract = _invert(inv)
                papers.append({
                    "source": "openalex_bulk",
                    "id":     oid,
                    "title":  title,
                    "year":   year or 0,
                    "text":   f"{title} {abstract}".strip(),
                })
                added += 1
            print(f"  OA '{q[:40]}' p{page}: +{added} (total {len(papers)})")
            meta = data.get("meta", {})
            total_count = meta.get("count", 0)
            if page * PAGE_SIZE >= total_count:
                break
            page += 1
            time.sleep(RATE_SLEEP)
        time.sleep(RATE_SLEEP)

    print(f"  [A] {len(papers)} OpenAlex papers")
    return papers


# ── Track B: CrossRef — 15 fresh queries ──────────────────────────────────────

CROSSREF_QUERIES = [
    "Dravidian Kannada Telugu Malayalam ancient inscription",
    "Indus script sign allograph variant grapheme inventory",
    "Elamite language Elamo-Dravidian hypothesis phonology",
    "Harappan weight system cuboid stone trade standard",
    "Dravidian substrate Sanskrit Vedic loanword contact",
    "Brahui Dravidian Balochistan language isolate",
    "ancient South Asia Y chromosome haplogroup population",
    "Indus Valley archaeobotany agricultural surplus storage",
    "Bronze Age maritime trade Persian Gulf Oman India",
    "Tamil Sangam classical literature historical evidence",
    "Indus script corpus bigram trigram positional statistics",
    "ancient India Chalcolithic Neolithic transition population",
    "Harappan copper trade network source ore Bronze Age",
    "Indus inscription tablet unique signs graffiti",
    "4.2 kya Harappan climate collapse monsoon failure",
]


def track_b_crossref() -> list[dict]:
    """CrossRef API with rows=100 per query."""
    print("\n[Track B] CrossRef (15 new queries)...")
    papers = []
    seen: set = set()
    deadline = time.time() + 300

    for q in CROSSREF_QUERIES:
        if time.time() > deadline:
            break
        encoded = urllib.parse.quote(q)
        url = (
            f"https://api.crossref.org/works?"
            f"query={encoded}&rows=100&select=DOI,title,abstract,published,type"
            f"&mailto=tpierson%40bitconcepts.tech"
        )
        data = _get_json(url)
        if not data:
            time.sleep(RATE_SLEEP)
            continue
        items = (data.get("message") or {}).get("items", [])
        added = 0
        for item in items[:80]:
            doi = item.get("DOI", "")
            if doi in seen:
                continue
            seen.add(doi)
            titles = item.get("title", [])
            title  = titles[0] if titles else ""
            abstract = item.get("abstract", "")
            abstract = re.sub(r"<[^>]+>", " ", abstract)[:2000]
            pub = item.get("published", {})
            date_parts = pub.get("date-parts", [[0]])
            year = date_parts[0][0] if date_parts and date_parts[0] else 0
            papers.append({
                "source": "crossref",
                "id":     doi,
                "title":  title,
                "year":   year or 0,
                "text":   f"{title} {abstract}".strip(),
                "url":    f"https://doi.org/{doi}",
            })
            added += 1
        print(f"  CR '{q[:40]}': +{added}")
        time.sleep(RATE_SLEEP)

    print(f"  [B] {len(papers)} CrossRef papers")
    return papers


# ── Track C: S2 — 12 fresh clusters ──────────────────────────────────────────

S2_DEEP_QUERIES = [
    "Elamo-Dravidian language family Elamite hypothesis",
    "Brahui Dravidian isolate Pakistan ancient origin",
    "DEDR Dravidian Etymological Dictionary cognate root",
    "Parpola Indus sign list decipherment reading",
    "steppe ancestry Indo-Aryan South Asia ancient DNA 2024 2025",
    "Harappan fishing economy coastal ecology vocabulary",
    "Indus seal unicorn fish anthropomorphic iconography",
    "South Asian Chalcolithic Neolithic archaeology migration",
    "Munda Austroasiatic ancient subcontinent language contact",
    "Indus copper tablet short inscription unique",
    "ancient Tamil epigraphy Brahmi cave inscription",
    "Harappan urban planning sanitation craft specialist",
]


def track_c_s2_deep() -> list[dict]:
    """S2 with offset pagination — 5 pages of 50 per query."""
    print("\n[Track C] Semantic Scholar deep (12 new clusters)...")
    papers = []
    seen: set = set()
    deadline = time.time() + 360

    for q in S2_DEEP_QUERIES:
        if time.time() > deadline:
            break
        for offset in range(0, 250, 50):
            if time.time() > deadline:
                break
            encoded = urllib.parse.quote(q)
            url = (
                f"https://api.semanticscholar.org/graph/v1/paper/search?"
                f"query={encoded}&fields=title,abstract,year&limit=50&offset={offset}"
            )
            data = _get_json(url)
            if not data or not data.get("data"):
                break
            items = data["data"]
            if not items:
                break
            for item in items:
                pid = item.get("paperId", "")
                if pid in seen:
                    continue
                seen.add(pid)
                title    = item.get("title", "")
                abstract = item.get("abstract") or ""
                year     = item.get("year", 0)
                papers.append({
                    "source": "s2_deep",
                    "id":     pid,
                    "title":  title,
                    "year":   year or 0,
                    "text":   f"{title} {abstract[:2000]}".strip(),
                })
            time.sleep(RATE_SLEEP)

    print(f"  [C] {len(papers)} S2 papers")
    return papers


# ── Track D: arXiv — fixed XML parser, 25 new queries ────────────────────────

ARXIV_QUERIES = [
    "Dravidian language NLP computational phonology",
    "ancient script decipherment neural network",
    "proto-Dravidian reconstruction lexicon",
    "South Asia genetic ancestry steppe farmer hunter-gatherer",
    "Indus Valley Civilization mathematical analysis",
    "Tamil language ancient computational corpus",
    "undeciphered script Markov model probabilistic",
    "Harappan site GIS spatial analysis",
    "Bronze Age trade network isotope archaeometry",
    "ancient DNA India Bronze Age steppe",
    "Elamite language computational analysis",
    "Dravidian morphology agglutinative NLP",
    "rebus acrophonic writing system origin",
    "South Asian archaeogenomics population structure",
    "Indus Valley climate change monsoon",
    "ancient script information entropy writing",
    "Tamil Brahmi inscription digital database",
    "Proto-Dravidian DEDR etymology cognate",
    "Harappan genome 2024 2025",
    "Indus corpus sign distribution",
    "Brahui Dravidian language classification",
    "ancient South Asia Y-chromosome haplogroup",
    "Bronze Age writing comparison undeciphered",
    "Dravidian linguistics historical reconstruction",
    "Linear A decipherment comparison methodology",
]


def track_d_arxiv() -> list[dict]:
    """arXiv with raw XML parsing (fixed from Phase 183)."""
    print("\n[Track D] arXiv (fixed XML parser, 25 queries)...")
    papers = []
    seen: set = set()
    deadline = time.time() + 300

    for q in ARXIV_QUERIES:
        if time.time() > deadline:
            break
        encoded = urllib.parse.quote(q)
        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query=all:{encoded}&start=0&max_results=40"
            f"&sortBy=relevance&sortOrder=descending"
        )
        raw = _get_raw(url)
        if not raw:
            time.sleep(RATE_SLEEP)
            continue

        entries = re.findall(r"<entry>(.*?)</entry>", raw, re.S)
        added = 0
        for entry in entries:
            id_m  = re.search(r"<id>https?://arxiv\.org/abs/([^<\s]+)</id>", entry)
            title_m = re.search(r"<title[^>]*>([^<]+)</title>", entry)
            summ_m  = re.search(r"<summary[^>]*>(.*?)</summary>", entry, re.S)
            year_m  = re.search(r"<published>(\d{4})", entry)

            if not id_m:
                continue
            arxiv_id = id_m.group(1).strip()
            if arxiv_id in seen:
                continue
            seen.add(arxiv_id)

            title    = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
            abstract = re.sub(r"\s+", " ", summ_m.group(1)).strip()[:2000] if summ_m else ""
            year     = int(year_m.group(1)) if year_m else 0

            papers.append({
                "source": "arxiv_bulk",
                "id":     arxiv_id,
                "title":  title,
                "year":   year,
                "text":   f"{title} {abstract}".strip(),
                "url":    f"https://arxiv.org/abs/{arxiv_id}",
            })
            added += 1
        print(f"  arXiv '{q[:40]}': +{added}")
        time.sleep(RATE_SLEEP)

    print(f"  [D] {len(papers)} arXiv papers")
    return papers


# ── Track E: Wikipedia — 13 fresh articles ────────────────────────────────────

WIKI_ARTICLES = [
    "Elamo-Dravidian_languages",
    "Tamil_Brahmi",
    "Dholavira",
    "Lothal",
    "Brahui_language",
    "Linear_A",
    "Elamite_language",
    "Bactria–Margiana_Archaeological_Complex",
    "Meluhha",
    "Bronze_Age_in_South_Asia",
    "List_of_Indus_Valley_civilization_sites",
    "Vedic_Sanskrit",
    "Indus_Valley_civilisation_religion",
]


def track_e_wikipedia() -> list[dict]:
    """Extract references from fresh Wikipedia articles."""
    print("\n[Track E] Wikipedia (13 new articles)...")
    papers = []
    seen: set = set()
    deadline = time.time() + 240

    for article in WIKI_ARTICLES:
        if time.time() > deadline:
            break
        encoded = urllib.parse.quote(article)
        url = (
            f"https://en.wikipedia.org/w/api.php?"
            f"action=query&prop=revisions&rvprop=content&format=json"
            f"&titles={encoded}&rvslots=main"
        )
        data = _get_json(url)
        if not data:
            time.sleep(RATE_SLEEP)
            continue

        pages = data.get("query", {}).get("pages", {})
        content = ""
        for page_data in pages.values():
            rev = page_data.get("revisions", [{}])
            slots = rev[0].get("slots", {}).get("main", {}) if rev else {}
            content = slots.get("*", "")
            break

        if not content:
            time.sleep(RATE_SLEEP)
            continue

        title_matches  = re.findall(r"\|\s*title\s*=\s*([^\|\}\n]+)", content)
        year_matches   = re.findall(r"\|\s*year\s*=\s*(\d{4})", content)
        doi_matches    = re.findall(r"\|\s*doi\s*=\s*([^\|\}\s\n]+)", content)
        url_matches    = re.findall(r"\|\s*url\s*=\s*(https?://[^\|\}\s\n]+)", content)

        added = 0
        for i, title in enumerate(title_matches[:200]):
            title = title.strip()
            if not title or len(title) < 5:
                continue
            doi      = doi_matches[i] if i < len(doi_matches) else ""
            year_raw = year_matches[i] if i < len(year_matches) else ""
            year     = int(year_raw) if year_raw.isdigit() else 0
            ref_url  = url_matches[i] if i < len(url_matches) else ""
            ref_id   = doi or ref_url or f"wiki_{article}_{i}"
            if ref_id in seen:
                continue
            seen.add(ref_id)
            papers.append({
                "source": "wikipedia_refs",
                "id":     ref_id,
                "title":  title,
                "year":   year,
                "text":   title,
                "url":    f"https://doi.org/{doi}" if doi else ref_url,
            })
            added += 1
        print(f"  Wiki '{article[:40]}': +{added}")
        time.sleep(RATE_SLEEP)

    print(f"  [E] {len(papers)} Wikipedia refs")
    return papers


# ── Track F: CORE API (new source) ───────────────────────────────────────────

CORE_QUERIES = [
    "Indus script Dravidian decipherment",
    "Harappan civilization language origin",
    "proto-Dravidian Tamil ancient",
    "Indus Valley archaeological recent",
    "ancient DNA South Asia Bronze Age",
    "Rakhigarhi genome Harappan",
    "Dravidian language history reconstruction",
    "Indus seal inscription sign",
    "Brahui Dravidian language",
    "fish sign Tamil phoneme",
]


def track_f_core() -> list[dict]:
    """CORE API — open-access repository, new source for Phase 184."""
    print("\n[Track F] CORE API (new source)...")
    papers = []
    seen: set = set()
    deadline = time.time() + 300

    for q in CORE_QUERIES:
        if time.time() > deadline:
            break
        encoded = urllib.parse.quote(q)
        url = f"https://api.core.ac.uk/v3/search/works?q={encoded}&limit=50"
        data = _get_json(url)
        if not data:
            time.sleep(RATE_SLEEP)
            continue

        results = data.get("results") or []
        added = 0
        for item in results:
            core_id = str(item.get("id", ""))
            if core_id in seen:
                continue
            seen.add(core_id)
            title    = item.get("title", "") or ""
            abstract = item.get("abstract", "") or ""
            year     = item.get("yearPublished", 0) or 0
            papers.append({
                "source": "core_api",
                "id":     core_id,
                "title":  title,
                "year":   year,
                "text":   f"{title} {abstract[:2000]}".strip(),
                "url":    item.get("downloadUrl", ""),
            })
            added += 1
        print(f"  CORE '{q[:40]}': +{added}")
        time.sleep(RATE_SLEEP)

    print(f"  [F] {len(papers)} CORE papers")
    return papers


# ── Evidence classifier ───────────────────────────────────────────────────────

def _classify(paper: dict) -> str:
    text = paper.get("text", "")
    for pat in STRONG_DRAVIDIAN:
        if pat.search(text):
            return "strong"
    for pat in MODERATE_EVIDENCE:
        if pat.search(text):
            return "moderate"
    return "weak"


def _extract_sign_proposals(papers: list[dict]) -> list[dict]:
    proposals = []
    for p in papers:
        text = p.get("text", "")
        for pat in NEW_SIGN_PATTERNS:
            for m in pat.finditer(text):
                proposals.append({
                    "sign":    f"M{m.group(1).zfill(3)}" if m.group(1).isdigit() else m.group(1),
                    "phoneme": m.group(2)[:8],
                    "source":  p.get("title", "")[:60],
                    "year":    p.get("year", 0),
                    "context": text[max(0, m.start()-50): m.end()+80],
                })
    return proposals[:50]


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    t0 = time.time()
    print("=" * 60)
    print("Phase 184 — Bulk Mine 5000 (fresh query clusters)")
    print("=" * 60)

    all_papers: list[dict] = []
    all_papers += track_a_openalex_bulk()
    all_papers += track_b_crossref()
    all_papers += track_c_s2_deep()
    all_papers += track_d_arxiv()
    all_papers += track_e_wikipedia()
    all_papers += track_f_core()

    # Classify
    strong, moderate, weak = [], [], []
    for p in all_papers:
        cls = _classify(p)
        if cls == "strong":
            strong.append(p)
        elif cls == "moderate":
            moderate.append(p)
        else:
            weak.append(p)

    sign_proposals = _extract_sign_proposals(strong + moderate)

    # Cumulative total across all mine phases
    cumulative = 211 + 5 + 80 + 41 + 166 + 183 + 6376 + len(all_papers)

    elapsed = round(time.time() - t0, 1)
    print(f"\n{'='*60}")
    print(f"Phase 184 complete in {elapsed}s")
    print(f"  Papers retrieved : {len(all_papers)}")
    print(f"  STRONG           : {len(strong)}")
    print(f"  MODERATE         : {len(moderate)}")
    print(f"  WEAK             : {len(weak)}")
    print(f"  Sign proposals   : {len(sign_proposals)}")
    print(f"  Total all phases : {cumulative}")
    print("=" * 60)

    report = {
        "phase":                   184,
        "n_papers":                len(all_papers),
        "n_strong_evidence":       len(strong),
        "n_moderate_evidence":     len(moderate),
        "n_weak_evidence":         len(weak),
        "total_papers_mined_all_phases": cumulative,
        "elapsed_seconds":         elapsed,
        "tracks": {
            "openalex_bulk": sum(1 for p in all_papers if p["source"] == "openalex_bulk"),
            "crossref":      sum(1 for p in all_papers if p["source"] == "crossref"),
            "s2_deep":       sum(1 for p in all_papers if p["source"] == "s2_deep"),
            "arxiv_bulk":    sum(1 for p in all_papers if p["source"] == "arxiv_bulk"),
            "wikipedia_refs":sum(1 for p in all_papers if p["source"] == "wikipedia_refs"),
            "core_api":      sum(1 for p in all_papers if p["source"] == "core_api"),
        },
        "evidence": {
            "strong":        strong[:30],
            "moderate":      moderate[:50],
            "sign_proposals": sign_proposals,
        },
    }

    out = OUTPUTS / "phase184_bulk_mine_5000.json"
    out.write_text(json.dumps(report, indent=2, default=str, ensure_ascii=False), encoding="utf-8")

    rep_dir = REPORTS
    rep_dir.mkdir(parents=True, exist_ok=True)
    (rep_dir / "phase184_bulk_mine_5000.json").write_text(
        json.dumps(report, indent=2, default=str, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Report saved: {out}")


if __name__ == "__main__":
    main()
