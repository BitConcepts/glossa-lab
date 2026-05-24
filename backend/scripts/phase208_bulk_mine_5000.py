"""Phase 208 -- Bulk Mine 5000 (Fifth Run)

Fresh clusters targeting gaps from Phases 183/184/196/202:
  - Brahui language contact zone and IVC NW corridor (Phase 205 flagged as priority)
  - McAlpin post-1981 follow-up (any responses, counter-arguments, extensions)
  - Computational Indus script 2025/2026 (Neural, LLM, new corpus work)
  - aDNA South Asia 2025/2026 -- newest papers not in prior mining
  - North Dravidian phylogeny (Brahui/Kurukh/Malto divergence)
  - Keezhadi 2024/2025 latest excavations
  - Harappan territorial extent and late phase (2100-1900 BCE)
  - Parpola recent work (post-2020 papers)
  - Indus sign list revisions (Parpola, Wells, Mahadevan cross-system)
  - Dravidian morphosyntax: agglutination, SOV, case marking
  - Bronze Age Balochistan/Mehrgarh continuity
  - Sargonic Akkadian Meluhha records (new CDLI releases 2024-2025)
  - IVC weight and measurement system
  - Allograph and sign variant studies 2020-2026

Six tracks: OpenAlex (26), CrossRef (16), S2 (12),
arXiv (25 fixed XML), Wikipedia (13 new), CORE API.

Output: outputs/phase208_bulk_mine_5000.json
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

STRONG_PATTERNS = [
    re.compile(r"Brahui.*(?:Dravidian|contact|IVC|Balochistan|linguistic)", re.I),
    re.compile(r"(?:IVC|Harappan|Indus).*(?:Brahui|North Dravidian|Balochistan)", re.I),
    re.compile(r"McAlpin.*(?:Dravidian|Elamite|follow|response|refut|extend)", re.I),
    re.compile(r"(?:Elamo.Dravidian|Dravidian.Elamite).*(?:2025|2026|new|further|additional)", re.I),
    re.compile(r"Indus.*script.*(?:neural|machine learning|deep learning|LLM|2025|2026)", re.I),
    re.compile(r"(?:computational|machine).*Indus.*(?:script|sign|decipher)", re.I | re.S),
    re.compile(r"South Asian.*(?:ancient DNA|aDNA|archaeogenetics).*(?:2025|2026)", re.I),
    re.compile(r"(?:Harappan|IVC).*(?:genome|aDNA|genetic).*(?:2025|2026)", re.I),
    re.compile(r"Parpola.*(?:Indus|Dravidian|2020|2021|2022|2023|2024|2025)", re.I),
    re.compile(r"Keezhadi.*(?:2024|2025|new|excavation|latest)", re.I),
    re.compile(r"North Dravidian.*(?:Brahui|Kurukh|Malto|phylogen|diverge)", re.I),
    re.compile(r"Harappan.*(?:Balochistan|Mehrgarh|late phase|collapse|2100|1900 BCE)", re.I),
]
MODERATE_PATTERNS = [
    re.compile(r"Dravidian.*(?:morphology|agglutination|SOV|case marker|syntax)", re.I),
    re.compile(r"(?:Indus|Harappan).*(?:weight|measurement|metrolog|standard)", re.I),
    re.compile(r"Indus.*sign.*(?:allograph|variant|list|catalog|2020|2021|2022|2023|2024)", re.I),
    re.compile(r"Sargonic.*(?:Meluhha|Indus|cuneiform|2024|2025)", re.I),
    re.compile(r"CDLI.*(?:Meluhha|Indus|cuneiform).*(?:new|2024|2025)", re.I),
    re.compile(r"Bronze Age.*(?:Balochistan|Mehrgarh|Chalcolithic|continuity|Dravidian)", re.I),
    re.compile(r"Tamil.*(?:Brahmi|Iron Age|literacy|script|ancient.*writing)", re.I),
    re.compile(r"(?:Dravidian|Tamil).*(?:personal name|onomastics|kinship|caste)", re.I),
]

OA_CLUSTERS = [
    # Brahui / IVC NW corridor
    "Brahui language Dravidian Balochistan contact linguistic",
    "Brahui Dravidian isolation Balochistan IVC north",
    "North Dravidian Kurukh Malto Brahui phylogenetic divergence",
    "Brahui Balochistan Bronze Age Harappan Indus contact",
    # McAlpin extensions
    "McAlpin Elamite Dravidian hypothesis response counter",
    "Elamo-Dravidian language family 2000 2010 2020 new evidence",
    "Elamite Dravidian cognate extended additional words",
    # Computational / AI 2025-2026
    "Indus script computational neural network 2025 2026",
    "Indus Valley script machine learning deep learning decipher",
    "Harappan script natural language processing sign frequency",
    "Indus script LLM transformer language model 2024 2025",
    # aDNA 2025-2026
    "South Asian ancient DNA 2025 2026 new population Harappan",
    "Indus Valley genome archaeogenetics new sample 2025",
    "AASI Ancestral South Asian ancestry Dravidian 2025 2026",
    "Harappan ancient genome AASI steppe mixture 2024 2025",
    # Parpola recent
    "Parpola Indus script Dravidian 2020 2021 2022 2023 2024",
    "Parpola Harappan seal text translation new",
    # Keezhadi latest
    "Keezhadi Tamil excavation inscription 2024 2025 recent",
    "Keezhadi Tamil Iron Age urbanization writing new find",
    # Sign list / allographs
    "Indus sign list allograph variant catalog 2020 2021",
    "Harappan script sign variant grapheme allograph study",
    "Mahadevan Wells Parpola sign list cross-reference update",
    # Harappan late phase / collapse
    "Harappan late phase collapse 2100 1900 BCE territory",
    "IVC urban decline migration climate 1900 BCE",
    # Meluhha Sargonic new CDLI
    "Meluhha Sargonic Akkadian cuneiform CDLI 2024 2025",
    "Meluhha Indus merchant cuneiform record new",
    # Dravidian morphology
    "Dravidian agglutinative morphology SOV case marker comparison Elamite",
]

CROSSREF_QUERIES = [
    "Brahui language Dravidian Balochistan contact",
    "North Dravidian Kurukh Malto phylogenetic divergence",
    "Indus script computational neural machine learning 2025",
    "Elamo-Dravidian language evidence new",
    "McAlpin Elamite Dravidian extensions",
    "South Asian ancient DNA aDNA 2025 2026 Harappan",
    "Parpola Indus script Dravidian 2022 2023 2024",
    "Keezhadi Tamil excavation 2024 2025",
    "Indus sign allograph variant list",
    "Harappan late phase collapse territory 1900 BCE",
    "Meluhha Sargonic CDLI cuneiform 2024",
    "Dravidian morphology agglutination SOV",
    "Harappan Balochistan Bronze Age Mehrgarh",
    "Indus Valley weight measurement standard",
    "AASI ancient South Asian ancestry 2025 new",
    "Tamil Brahmi Iron Age inscription literacy",
]

S2_QUERIES = [
    "Brahui Dravidian language contact Indus Valley",
    "Indus script neural network computational 2025",
    "South Asian aDNA ancient DNA Harappan 2025",
    "Elamo-Dravidian new evidence cognate",
    "Parpola Indus Dravidian recent",
    "Indus sign allograph variant study",
    "North Dravidian phylogenetics Kurukh Brahui",
    "Harappan collapse late phase climate",
    "Meluhha cuneiform trade Sargonic",
    "Keezhadi Tamil ancient inscription",
    "Dravidian agglutinative morphology Elamite",
    "Indus Valley metrological weight system",
]

ARXIV_QUERIES = [
    "Indus script decipherment",
    "Dravidian language computational",
    "South Asian archaeogenetics ancient DNA",
    "Harappan script analysis",
    "Brahui language phylogenetics",
    "Indus Valley Civilization language",
    "Dravidian morphology computational",
    "proto-Dravidian reconstruction",
    "Tamil Brahmi inscription ancient",
    "Indus seal analysis",
    "ancient South Asia linguistics",
    "Elamo-Dravidian language family",
    "Harappan civilization language question",
    "Indus corpus statistics entropy",
    "Keezhadi excavation Tamil",
    "Dravidian agglutination morphology",
    "Harappan collapse climate change",
    "McAlpin Elamite Dravidian",
    "Indus sign frequency analysis",
    "South Asian Bronze Age genetics",
    "Brahui Balochistan language",
    "Parpola Indus script",
    "ancient DNA India Dravidian",
    "Tamil Iron Age inscription",
    "Indus Valley weight standardization",
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


def _classify(text):
    t = text or ""
    for pat in STRONG_PATTERNS:
        if pat.search(t): return "STRONG"
    for pat in MODERATE_PATTERNS:
        if pat.search(t): return "MODERATE"
    return "WEAK"


def track_a_openalex(target):
    print("\n[Track A] OpenAlex (26 clusters)...")
    papers = []; seen = set(); deadline = time.time() + 600
    for q in OA_CLUSTERS:
        if time.time() > deadline or len(papers) >= target: break
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
                title    = item.get("display_name", "")
                year     = item.get("publication_year", 0)
                abstract = _invert(item.get("abstract_inverted_index") or {})
                papers.append({"source": "openalex", "id": oid, "title": title,
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


def track_b_crossref(target):
    print("\n[Track B] CrossRef (16 queries)...")
    papers = []; seen = set(); deadline = time.time() + 300
    for q in CROSSREF_QUERIES:
        if time.time() > deadline or len(papers) >= target: break
        encoded = urllib.parse.quote(q)
        url = (f"https://api.crossref.org/works?query={encoded}&rows=200"
               f"&mailto=tpierson@bitconcepts.tech")
        data = _get_json(url)
        if not data: continue
        items = data.get("message", {}).get("items", [])
        added = 0
        for item in items:
            doi = item.get("DOI", "")
            if doi in seen: continue
            seen.add(doi)
            title_list = item.get("title", [])
            title = title_list[0] if title_list else ""
            year = (item.get("published", {}).get("date-parts", [[0]])[0][0]) or 0
            abstract = re.sub(r"<[^>]+>", " ", item.get("abstract", ""))[:1000]
            papers.append({"source": "crossref", "id": doi, "title": title,
                           "year": year, "text": f"{title} {abstract}".strip()})
            added += 1
        print(f"  CR '{q[:40]}': +{added} (total {len(papers)})")
        time.sleep(RATE_SLEEP)
    print(f"  [B] {len(papers)} papers")
    return papers


def track_c_s2(target):
    print("\n[Track C] Semantic Scholar (12 queries)...")
    papers = []; seen = set(); deadline = time.time() + 240
    for q in S2_QUERIES:
        if time.time() > deadline or len(papers) >= target: break
        encoded = urllib.parse.quote(q)
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded}&limit=100&fields=title,year,abstract,externalIds"
        data = _get_json(url)
        if not data: continue
        added = 0
        for item in data.get("data", []):
            pid = item.get("paperId", "")
            if pid in seen: continue
            seen.add(pid)
            title    = item.get("title", "")
            year     = item.get("year", 0) or 0
            abstract = (item.get("abstract", "") or "")[:800]
            papers.append({"source": "s2", "id": pid, "title": title,
                           "year": year, "text": f"{title} {abstract}".strip()})
            added += 1
        print(f"  S2 '{q[:40]}': +{added} (total {len(papers)})")
        time.sleep(RATE_SLEEP * 2)
    print(f"  [C] {len(papers)} papers")
    return papers


def track_d_arxiv(target):
    print("\n[Track D] arXiv (25 queries)...")
    papers = []; seen = set(); deadline = time.time() + 300
    for q in ARXIV_QUERIES:
        if time.time() > deadline or len(papers) >= target: break
        encoded = urllib.parse.quote(q)
        url = f"https://export.arxiv.org/api/query?search_query=all:{encoded}&max_results=100"
        raw = _get_raw(url)
        if not raw: continue
        entries = raw.split("<entry>")[1:]
        added = 0
        for entry in entries:
            arxiv_id_m = re.search(r"<id>(.*?)</id>", entry)
            if not arxiv_id_m: continue
            arxiv_id = arxiv_id_m.group(1)
            if arxiv_id in seen: continue
            seen.add(arxiv_id)
            title_m = re.search(r"<title>(.*?)</title>", entry, re.S)
            summary_m = re.search(r"<summary>(.*?)</summary>", entry, re.S)
            title   = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
            summary = re.sub(r"\s+", " ", summary_m.group(1)).strip()[:600] if summary_m else ""
            year_m  = re.search(r"<published>(\d{4})", entry)
            year    = int(year_m.group(1)) if year_m else 0
            papers.append({"source": "arxiv", "id": arxiv_id, "title": title,
                           "year": year, "text": f"{title} {summary}".strip()})
            added += 1
        print(f"  arXiv '{q[:40]}': +{added} (total {len(papers)})")
        time.sleep(RATE_SLEEP)
    print(f"  [D] {len(papers)} papers")
    return papers


def main():
    t0 = time.time()
    print("=" * 60)
    print("Phase 208 -- Bulk Mine 5000 (Fifth Run)")
    print("=" * 60)

    all_papers = []
    seen_ids: set = set()

    def _dedup(batch):
        out = []
        for p in batch:
            pid = p.get("id", "") or p.get("title", "")
            if pid and pid not in seen_ids:
                seen_ids.add(pid)
                out.append(p)
        return out

    batch_a = _dedup(track_a_openalex(TARGET))
    all_papers.extend(batch_a)
    batch_b = _dedup(track_b_crossref(TARGET))
    all_papers.extend(batch_b)
    batch_c = _dedup(track_c_s2(TARGET))
    all_papers.extend(batch_c)
    batch_d = _dedup(track_d_arxiv(TARGET))
    all_papers.extend(batch_d)

    print(f"\nTotal papers before classification: {len(all_papers)}")

    # Classify
    strong_ev = []; moderate_ev = []; weak_ev = []
    for p in all_papers:
        ev = _classify(p["text"])
        p["evidence_tier"] = ev
        if ev == "STRONG": strong_ev.append(p)
        elif ev == "MODERATE": moderate_ev.append(p)
        else: weak_ev.append(p)

    print(f"  STRONG:   {len(strong_ev)}")
    print(f"  MODERATE: {len(moderate_ev)}")
    print(f"  WEAK:     {len(weak_ev)}")

    # Top strong papers
    strong_sorted = sorted(strong_ev, key=lambda x: x.get("year", 0), reverse=True)
    print("\n=== Top 20 STRONG papers ===")
    for i, p in enumerate(strong_sorted[:20]):
        print(f"  {i+1}. [{p['year']}] {p['title'][:80]}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 208,
        "elapsed_s": elapsed,
        "total_papers_fetched": len(all_papers),
        "n_strong_evidence": len(strong_ev),
        "n_moderate_evidence": len(moderate_ev),
        "n_weak_evidence": len(weak_ev),
        "strong_papers": strong_sorted[:50],
        "moderate_papers": sorted(moderate_ev, key=lambda x: x.get("year", 0), reverse=True)[:50],
        "target_clusters": OA_CLUSTERS,
        "verdict": (
            f"Phase 208 mine: {len(all_papers)} total papers. "
            f"{len(strong_ev)} STRONG, {len(moderate_ev)} MODERATE. "
            f"Targeting Brahui/IVC NW corridor, computational 2025/2026, aDNA 2025/2026, McAlpin extensions."
        ),
    }

    out = OUTPUTS / "phase208_bulk_mine_5000.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase208_bulk_mine_5000.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase 208 complete in {elapsed}s | Saved: {out}")
    print(f"Verdict: {result['verdict']}")


if __name__ == "__main__":
    main()
