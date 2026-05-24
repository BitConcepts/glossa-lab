"""Phase-231: Mine 5000 #6 — Indirect Bilingual / Contact Evidence Focus

Fresh clusters NOT covered by Phases 183/184/196/202/208.
Primary mission: find literature directly relevant to INDIRECT BILINGUAL
evidence connecting Indus script to deciphered or partially-deciphered sources.

New cluster targets:
  - Shu-ilishu seal and Meluhhan interpreter texts (deep dive)
  - Dilmun / Persian Gulf seals with cuneiform + Indus elements
  - Sanskrit substrate Dravidian loanwords (Witzel, Kuiper, Southworth)
  - Elamite-Dravidian phonological bridges (McAlpin extensions post-1981)
  - Vedic river-name substrates (non-IE toponymy in Rgveda)
  - Ur III Meluhhan personal name corpus (new CDLI releases)
  - Harappan weight system in Mesopotamia and Elamite sites
  - Black-and-red ware cultural continuity IVC → Iron Age Tamil Nadu
  - Ancient South Asian DNA new 2025/2026 (AASI, Iranian farmer, steppe)
  - Keezhadi Phase 7/8 2024/2025 results (Tamil Iron Age literacy)
  - Tamil-Brahmi Sangam onomastics (personal names, clan markers)
  - Proto-Dravidian reconstruction: Krishnamurti, Burrow, Emeneau updates
  - Harappan collapse and population dispersal models
  - Gulf Bronze Age trade networks (Oman, Bahrain, UAE archaeological)
  - Elamo-Dravidian: new computational/phylogenetic approaches 2020-2026

Output: outputs/phase231_indirect_bilingual_mine.json
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

# ── Classification patterns ───────────────────────────────────────────────────

STRONG_PATTERNS = [
    re.compile(r"Shu.ilishu|eme\.ba\.la|meluhh.+interpret", re.I),
    re.compile(r"Meluhh.+(?:name|personal|onomastic|language|speak)", re.I),
    re.compile(r"(?:Dilmun|Persian Gulf).+(?:Indus|cuneiform|bilingual|seal)", re.I),
    re.compile(r"(?:Sanskrit|Vedic).+(?:Dravidian|substrate|loanword|non-IE)", re.I),
    re.compile(r"(?:Witzel|Kuiper|Southworth).+(?:substrate|loanword|Dravidian|Indo-European)", re.I),
    re.compile(r"Elamite.+(?:Dravidian|PDr|McAlpin|cognate|family|related)", re.I),
    re.compile(r"McAlpin.+(?:Elamite|Dravidian|cognate|2[0-9]{3})", re.I),
    re.compile(r"(?:Harappan|IVC|Indus).+(?:weight|metrolog|standard).+(?:Mesopotam|Elam|Ur|Nippur)", re.I),
    re.compile(r"Black.and.red ware.+(?:IVC|Harappan|Iron Age|Tamil|Megalith)", re.I),
    re.compile(r"(?:AASI|Ancestral South Asian).+(?:Dravidian|Tamil|IVC|Harappan)", re.I),
    re.compile(r"Keezhadi.+(?:2024|2025|Phase [789]|Tamil|Iron Age|literacy|inscription)", re.I),
    re.compile(r"Tamil.Brahmi.+(?:name|onomastic|personal|Sangam|clan|concordance)", re.I),
    re.compile(r"(?:Rgveda|Rigveda).+(?:substrate|non-IE|pre-Indo|Dravidian|Harappan|toponym)", re.I),
    re.compile(r"Sarasvati.+(?:river|non-IE|substrate|Dravidian|pre-Indo)", re.I),
]

MODERATE_PATTERNS = [
    re.compile(r"(?:Ur III|Sargonic|Akkadian).+(?:Meluhh|Indus|Harappan|melukhha)", re.I),
    re.compile(r"(?:Indus|Harappan).+(?:Gulf|Oman|Bahrain|UAE|Dilmun|Magan).+trade", re.I),
    re.compile(r"proto.Dravidian.+(?:reconstruct|phonolog|morpholog|lexic|2020|2021|2022|2023|2024|2025)", re.I),
    re.compile(r"Brahui.+(?:Dravidian|IVC|ancient|relic|isolat|aDNA|genetic)", re.I),
    re.compile(r"(?:Harappan|IVC).+(?:collapse|dispers|migrat|population|1900 BCE|2100 BCE)", re.I),
    re.compile(r"(?:Dravidian|Tamil).+(?:kinship|clan|totem|onomastic|name system|suffix)", re.I),
    re.compile(r"(?:Indus|Harappan).+(?:sign list|sign variant|allograph|catalog).+(?:2020|2021|2022|2023|2024)", re.I),
    re.compile(r"South Asian.+(?:Bronze Age|Chalcolithic|Neolithic).+(?:genetic|aDNA|ancient DNA)", re.I),
]

# ── OpenAlex clusters ─────────────────────────────────────────────────────────

OA_CLUSTERS = [
    # Shu-ilishu / Meluhhan interpreter
    "Shu-ilishu interpreter Meluhhan language cuneiform Ur III",
    "Meluhha Melukhha personal names cuneiform Akkadian Ur III phonology",
    "lu2-eme-meluhhaki Meluhhan language speaker Ur III Drehem",
    # Dilmun Gulf seals
    "Dilmun Persian Gulf seal Indus cuneiform bilingual Bronze Age",
    "Bahrain seal Indus derived motif cuneiform inscription",
    "Tell Abraq UAE Indus seal cuneiform token coexistence",
    "Gulf Bronze Age trade Indus Mesopotamia Dilmun Magan Oman seal",
    # Sanskrit substrate loanwords
    "Sanskrit Vedic Dravidian substrate loanword non-Indo-European",
    "Witzel Kuiper Southworth Sanskrit Dravidian substrate",
    "Vedic Sanskrit loanword Dravidian substrate retroflex phonology",
    "Indo-Aryan Dravidian contact loanword borrowing substrate ancient",
    # Elamo-Dravidian
    "Elamite Dravidian language family McAlpin cognate phonological",
    "Elamo-Dravidian relationship new evidence computational 2020 2025",
    "Proto-Dravidian Elamite comparison morphology vocabulary",
    # Rgveda substrate
    "Rigveda substrate non-Indo-European river name toponym pre-Aryan",
    "Sarasvati river name non-IE substrate Harappan Dravidian",
    "Rgvedic place names Dravidian substrate Witzel 1999",
    # Weight system
    "Harappan weight standard Mesopotamia Ur Nippur Susa Bronze Age",
    "Indus metrological system Persian Gulf trade Bronze Age",
    "Harappan binary weight ratio Akkadian mina trade vocabulary",
    # Black-and-red ware
    "Black-and-red ware IVC Iron Age Tamil Nadu cultural continuity",
    "BRW pottery Deccan Megalithic South India Harappan continuity",
    # aDNA AASI 2025-2026
    "AASI ancestral South Asian Dravidian IVC genetics 2025 2026",
    "South Asian ancient DNA Rakhigarhi AASI Iranian farmer mixture",
    "Harappan aDNA population dispersal 1900 BCE genetic continuity",
    # Keezhadi 2024-2025
    "Keezhadi Tamil excavation 2024 2025 Phase 7 8 Iron Age literacy",
    "Keezhadi inscription Tamil Brahmi writing 2025 ancient",
]

CROSSREF_QUERIES = [
    "Shu-ilishu Meluhhan interpreter cuneiform",
    "Sanskrit Dravidian substrate loanword Witzel",
    "Elamite Dravidian McAlpin cognate",
    "Dilmun Persian Gulf seal Indus cuneiform",
    "Harappan weight Mesopotamia Ur Bronze Age",
    "Black-and-red ware IVC Tamil Iron Age",
    "AASI Dravidian ancient DNA IVC 2025",
    "Keezhadi Tamil 2024 2025 excavation",
    "Rgveda non-IE substrate Dravidian",
    "Tamil Brahmi onomastics Sangam personal name",
    "Meluhha personal names Akkadian phonology",
    "Proto-Dravidian reconstruction 2020 2024",
    "Harappan collapse migration population 1900 BCE",
    "Gulf Bronze Age trade Oman Bahrain Indus",
    "Elamo-Dravidian computational 2020 2025",
]

S2_QUERIES = [
    "Meluhha cuneiform personal names Akkadian",
    "Sanskrit Dravidian substrate loanword non-IE",
    "Elamite Dravidian McAlpin language family",
    "Gulf seal Indus cuneiform bilingual Dilmun",
    "Harappan weight system Mesopotamia Elamite",
    "Black-and-red ware cultural continuity Tamil",
    "AASI ancient DNA South Asian Dravidian IVC",
    "Keezhadi Tamil Iron Age inscription 2024",
    "Rgveda substrate Dravidian non-IE toponym",
    "Tamil Brahmi onomastics personal name Sangam",
    "Harappan collapse dispersal migration model",
    "Proto-Dravidian phonological reconstruction",
]

ARXIV_QUERIES = [
    "Dravidian Sanskrit substrate loanword",
    "Elamite Dravidian language family",
    "South Asian ancient DNA AASI IVC",
    "Harappan Indus collapse migration",
    "Tamil Iron Age literacy inscription",
    "Indus script Gulf Bronze Age",
    "proto-Dravidian reconstruction phylogenetics",
    "Brahui Dravidian Balochistan ancient",
    "Vedic non-IE substrate toponym",
    "Keezhadi Tamil excavation",
    "Harappan weight metrological system",
    "Indus script computational 2025",
    "Bronze Age Gulf trade Indus Mesopotamia",
    "AASI Ancestral South Asian genetics",
    "Meluhha Mesopotamia cuneiform trade",
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
    print("\n[Track A] OpenAlex (indirect bilingual clusters)...")
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
                title = item.get("display_name", "")
                year  = item.get("publication_year", 0)
                abstract = _invert(item.get("abstract_inverted_index") or {})
                papers.append({"source": "openalex", "id": oid, "title": title,
                               "year": year or 0, "text": f"{title} {abstract}".strip()})
                added += 1
            print(f"  OA '{q[:45]}' p{page}: +{added} (total {len(papers)})")
            meta = data.get("meta", {})
            if page * PAGE_SIZE >= meta.get("count", 0): break
            page += 1
            time.sleep(RATE_SLEEP)
        time.sleep(RATE_SLEEP)
    print(f"  [A] {len(papers)} papers")
    return papers


def track_b_crossref(target):
    print("\n[Track B] CrossRef...")
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
        print(f"  CR '{q[:45]}': +{added} (total {len(papers)})")
        time.sleep(RATE_SLEEP)
    print(f"  [B] {len(papers)} papers")
    return papers


def track_c_s2(target):
    print("\n[Track C] Semantic Scholar...")
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
            title = item.get("title", "")
            year  = item.get("year", 0) or 0
            abstract = (item.get("abstract", "") or "")[:800]
            papers.append({"source": "s2", "id": pid, "title": title,
                           "year": year, "text": f"{title} {abstract}".strip()})
            added += 1
        print(f"  S2 '{q[:45]}': +{added} (total {len(papers)})")
        time.sleep(RATE_SLEEP * 2)
    print(f"  [C] {len(papers)} papers")
    return papers


def track_d_arxiv(target):
    print("\n[Track D] arXiv...")
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
            title_m   = re.search(r"<title>(.*?)</title>", entry, re.S)
            summary_m = re.search(r"<summary>(.*?)</summary>", entry, re.S)
            title   = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
            summary = re.sub(r"\s+", " ", summary_m.group(1)).strip()[:600] if summary_m else ""
            year_m  = re.search(r"<published>(\d{4})", entry)
            year    = int(year_m.group(1)) if year_m else 0
            papers.append({"source": "arxiv", "id": arxiv_id, "title": title,
                           "year": year, "text": f"{title} {summary}".strip()})
            added += 1
        print(f"  arXiv '{q[:45]}': +{added} (total {len(papers)})")
        time.sleep(RATE_SLEEP)
    print(f"  [D] {len(papers)} papers")
    return papers


def extract_indirect_bilingual_hits(papers: list) -> dict:
    """Scan all paper texts for indirect bilingual evidence patterns."""
    hits = {
        "shu_ilishu_refs": [],
        "gulf_seal_refs": [],
        "substrate_loanword_refs": [],
        "elamo_dravidian_refs": [],
        "rgveda_substrate_refs": [],
        "weight_system_refs": [],
        "brw_continuity_refs": [],
        "keezhadi_refs": [],
        "adna_corridor_refs": [],
        "tamil_brahmi_onomastic_refs": [],
    }
    patterns = {
        "shu_ilishu_refs": re.compile(r"Shu.ilishu|eme\.ba\.la|meluhh.+interpret", re.I),
        "gulf_seal_refs": re.compile(r"(?:Dilmun|Persian Gulf|Bahrain|Tell Abraq).+(?:seal|cuneiform|Indus)", re.I),
        "substrate_loanword_refs": re.compile(r"(?:Sanskrit|Vedic).+(?:substrate|loanword|Dravidian|non-IE)", re.I),
        "elamo_dravidian_refs": re.compile(r"Elamo.Dravidian|Elamite.+Dravidian|McAlpin.+cognate", re.I),
        "rgveda_substrate_refs": re.compile(r"(?:Rgveda|Rigveda|Sarasvati).+(?:substrate|non-IE|Dravidian)", re.I),
        "weight_system_refs": re.compile(r"Harappan.+weight.+(?:Mesopotam|Ur|Nippur|Susa|Elamite)", re.I),
        "brw_continuity_refs": re.compile(r"Black.and.red ware|BRW.+(?:Harappan|Tamil|Iron Age|Megalith)", re.I),
        "keezhadi_refs": re.compile(r"Keezhadi", re.I),
        "adna_corridor_refs": re.compile(r"AASI|ancestral South Asian.+(?:Dravidian|IVC|Harappan)", re.I),
        "tamil_brahmi_onomastic_refs": re.compile(r"Tamil.Brahmi.+(?:name|onomastic|Sangam|clan|personal)", re.I),
    }
    for p in papers:
        text = p.get("text", "")
        for key, pat in patterns.items():
            if pat.search(text):
                hits[key].append({"title": p.get("title", "")[:80], "year": p.get("year", 0)})
    return {k: {"n": len(v), "papers": v[:5]} for k, v in hits.items()}


def main():
    t0 = time.time()
    print("=" * 60)
    print("Phase 231 -- Indirect Bilingual Mine 5000 (Sixth Run)")
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

    # Extract indirect bilingual hits
    ib_hits = extract_indirect_bilingual_hits(all_papers)
    print("\n  === Indirect Bilingual Evidence Hits ===")
    for key, val in ib_hits.items():
        print(f"  {key}: {val['n']} papers")

    strong_sorted = sorted(strong_ev, key=lambda x: x.get("year", 0), reverse=True)
    print("\n=== Top 20 STRONG papers ===")
    for i, p in enumerate(strong_sorted[:20]):
        print(f"  {i+1}. [{p['year']}] {p['title'][:80]}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 231,
        "elapsed_s": elapsed,
        "total_papers_fetched": len(all_papers),
        "n_strong_evidence": len(strong_ev),
        "n_moderate_evidence": len(moderate_ev),
        "n_weak_evidence": len(weak_ev),
        "indirect_bilingual_hits": ib_hits,
        "strong_papers": strong_sorted[:50],
        "moderate_papers": sorted(moderate_ev, key=lambda x: x.get("year", 0), reverse=True)[:50],
        "target_clusters": OA_CLUSTERS,
        "verdict": (
            f"Phase 231 mine: {len(all_papers)} total papers. "
            f"{len(strong_ev)} STRONG, {len(moderate_ev)} MODERATE. "
            f"Targeting: Shu-ilishu ({ib_hits['shu_ilishu_refs']['n']}), "
            f"Gulf seals ({ib_hits['gulf_seal_refs']['n']}), "
            f"Sanskrit substrate ({ib_hits['substrate_loanword_refs']['n']}), "
            f"Elamo-Dravidian ({ib_hits['elamo_dravidian_refs']['n']}), "
            f"Keezhadi ({ib_hits['keezhadi_refs']['n']})."
        ),
    }

    out = OUTPUTS / "phase231_indirect_bilingual_mine.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase231_indirect_bilingual_mine.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase 231 complete in {elapsed}s | Saved: {out}")
    print(f"Verdict: {result['verdict']}")


if __name__ == "__main__":
    main()
