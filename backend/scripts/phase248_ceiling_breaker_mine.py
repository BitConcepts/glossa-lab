"""Phase-248: Ceiling-Breaker Mine 5000

Targets the two fundamental decipherment ceilings with creative cross-domain approaches:

CEILING 1: Ultra-rare sign tail (~30-50 signs appearing <5 times)
  Path C1a — ALLOGRAPH CLUSTERING: Rare signs may be positional allographs of
    known signs. If proven, they inherit the known sign's reading.
  Path C1b — BIGRAM FORCING: Rare signs in fixed bigrams with known signs have
    constrained reading spaces (e.g., if X always precedes M099='kol', X is likely
    a TITLE/GENITIVE prefix from the known PDr inventory)
  Path C1c — ICONOGRAPHIC DETERMINATIVES: Rare signs on seals with specific animals
    constrain the reading to phonemes of that animal's name in PDr.
  Path C1d — PERSONAL NAME ZIPF: Real name systems have Zipf distributions.
    Rare phoneme combinations in PDr names predict which rare signs encode.
  Path C1e — MUNDA SUBSTRATE: Eastern Indus rare signs may encode Munda (Austroasiatic)
    rather than PDr. Munda phonology = different constraint set for those signs.

CEILING 2: No bilingual text
  Path C2a — LINEAR ELAMITE VOCABULARY: Desset 2022 established 80+ LE sign values.
    Mining for papers with specific LE word lists → extend Elamite-PDr bridge
    directly to rare Indus signs via comparative phonology
  Path C2b — TRADE COMMODITY PHONOLOGY: Akkadian/Sumerian names for Harappan exports
    (carnelian, cotton, tin, ivory, sesame) preserve PDr phonology. If rare Indus
    sign appears on commodity seal → Akkadian trade name → PDr phonology → reading.
  Path C2c — PROTO-ELAMITE FUNCTIONAL PARALLELS: PE (~3000 BCE) predates Linear Elamite.
    Some PE sign functions parallel Indus. If PE sign function = PDr reading context
    → constrain Indus sign readings via functional parallel.
  Path C2d — SANGAM RARE VOCABULARY: Old Tamil hapax legomena (rare words appearing
    once in Sangam corpus) may preserve Harappan-era vocabulary. Mining for
    Sangam vocabulary reconstruction studies.
  Path C2e — MELUHHA COMMODITY VOCABULARY: Cuneiform records list specific Meluhhan
    goods by name. Some names in Akkadian transliteration preserve Harappan phonology.
    Mining for new CDLI releases and Mesopotamian trade vocabulary studies.

Each path is a potential independent route to break a ceiling.
Mine 5000+ papers across all 10 paths simultaneously.

Output: outputs/phase248_ceiling_breaker_mine.json
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
MAX_PAGES    = 6
PAGE_SIZE    = 200
TARGET       = 5000

# ── Ceiling-breaker patterns ──────────────────────────────────────────────────

CEILING_PATTERNS = {
    "C1a_ALLOGRAPH": [
        re.compile(r"(?:allograph|grapheme variant|sign variant).*(?:Indus|Harappan|Proto-Dravidian)", re.I),
        re.compile(r"Indus.*(?:allograph|variant form|positional variant|writing variant)", re.I),
        re.compile(r"(?:sign cluster|sign family|grapheme cluster).*(?:Indus|Harappan)", re.I),
    ],
    "C1b_BIGRAM_CONTEXT": [
        re.compile(r"Indus.*(?:bigram|trigram|n-gram|co-occurrence|context).*(?:rare|low frequency|hapax)", re.I),
        re.compile(r"(?:hapax|rare sign|infrequent).*(?:Indus|Harappan).*(?:context|reading|function)", re.I),
        re.compile(r"Indus.*(?:fixed pair|invariant sequence|frozen expression)", re.I),
    ],
    "C1c_ICONOGRAPHIC": [
        re.compile(r"(?:iconograph|animal motif|pictograph).*(?:Indus|Harappan).*(?:reading|phonetic|DEDR|Dravidian)", re.I),
        re.compile(r"Indus.*(?:seal motif|unicorn|zebu|rhinoceros|elephant|tiger).*(?:sign|reading|name)", re.I),
        re.compile(r"(?:rebus|icon).*(?:Indus|Harappan|script).*(?:sound value|phonetic)", re.I),
    ],
    "C1d_NAME_ZIPF": [
        re.compile(r"(?:personal name|onomastic|anthroponym).*(?:Indus|Harappan|Proto-Dravidian|PDr)", re.I),
        re.compile(r"(?:Dravidian|Tamil|PDr).*(?:name system|onomastic|personal name|anthroponym)", re.I),
        re.compile(r"(?:Zipf|frequency distribution).*(?:name|onomastic|personal).*(?:Dravidian|Tamil|ancient)", re.I),
    ],
    "C1e_MUNDA_SUBSTRATE": [
        re.compile(r"(?:Munda|Austroasiatic|Santali|Mundari).*(?:Indus|Harappan|IVC|substrate)", re.I),
        re.compile(r"(?:Indus|Harappan).*(?:Munda|Austroasiatic|Kolarian).*(?:language|substrate|contact)", re.I),
        re.compile(r"(?:BMAC|Bactria.Margiana).*(?:Munda|Austroasiatic|substrate).*(?:2020|2021|2022|2023|2024|2025)", re.I),
    ],
    "C2a_LINEAR_ELAMITE_VOCAB": [
        re.compile(r"Linear Elamite.*(?:vocabulary|word list|lexicon|sign value|reading|text)", re.I),
        re.compile(r"(?:Desset|Linear Elamite).*(?:2022|2023|2024|2025).*(?:sign|value|word|text|inscription)", re.I),
        re.compile(r"Elamite.*(?:vocabulary|lexicon|word).*(?:new|updated|2020|2022|2024).*(?:Dravidian|PDr|Proto)", re.I),
    ],
    "C2b_TRADE_COMMODITY": [
        re.compile(r"(?:Meluhha|Harappan).*(?:carnelian|cotton|tin|ivory|sesame|lapis).*(?:Akkadian|cuneiform|trade name)", re.I),
        re.compile(r"(?:Akkadian|Sumerian).*(?:Meluhhan|Harappan|Indus).*(?:commodity|trade good|export|import).*(?:name|word)", re.I),
        re.compile(r"Bronze Age.*(?:commodity|trade).*(?:phonology|name|vocabulary).*(?:Indus|Meluhha|IVC)", re.I),
        re.compile(r"(?:carnelian|lapis lazuli|cotton|tin).*(?:Harappan|IVC|Indus).*(?:trade|vocabulary|phonology)", re.I),
    ],
    "C2c_PROTO_ELAMITE": [
        re.compile(r"Proto.Elamite.*(?:Indus|Harappan|sign function|parallel|comparison)", re.I),
        re.compile(r"(?:Indus|Harappan).*Proto.Elamite.*(?:sign|function|parallel|comparison|decipherment)", re.I),
        re.compile(r"Proto.Elamite.*(?:2020|2021|2022|2023|2024|2025).*(?:decipherment|function|sign|reading)", re.I),
    ],
    "C2d_SANGAM_HAPAX": [
        re.compile(r"(?:Sangam|Tamil).*(?:hapax|rare word|uncommon|archaic).*(?:vocabulary|lexicon|word)", re.I),
        re.compile(r"Old Tamil.*(?:vocabulary|lexicon|hapax|rare).*(?:Harappan|IVC|Indus|ancient|substratum)", re.I),
        re.compile(r"(?:Purananuru|Akananuru|Sangam corpus).*(?:reconstruction|vocabulary|rare|archaic)", re.I),
        re.compile(r"Tamil.*(?:substrate|loanword|borrowing).*(?:Harappan|IVC|Bronze Age|pre-Dravidian)", re.I),
    ],
    "C2e_MELUHHA_COMMODITY_VOCAB": [
        re.compile(r"(?:Meluhha|melukhha).*(?:vocabulary|word|name|commodity|trade).*(?:Akkadian|Sumerian|cuneiform)", re.I),
        re.compile(r"(?:CDLI|cuneiform).*(?:Meluhha|Harappan|Indus).*(?:new|2024|2025|vocabulary|word)", re.I),
        re.compile(r"(?:Ur III|Sargonic|Akkadian).*(?:trade word|commodity name).*(?:Meluhha|Indus|IVC|loanword)", re.I),
    ],
}

MODERATE_PATTERNS = [
    re.compile(r"(?:Indus|Harappan).*(?:sign|script|decipher).*(?:new|2024|2025|2026)", re.I),
    re.compile(r"(?:Dravidian|Tamil|PDr).*(?:ancient|archaic|substrate|rare).*(?:vocabulary|phonology)", re.I),
    re.compile(r"(?:Munda|Austroasiatic|Proto-Elamite|Linear Elamite).*(?:2022|2023|2024|2025)", re.I),
    re.compile(r"(?:Bronze Age|Harappan).*(?:trade|commodity).*(?:vocabulary|name|phonology)", re.I),
]

OA_CLUSTERS = [
    # C1a Allograph
    "Indus script sign allograph variant grapheme positional",
    "Indus Harappan sign cluster grapheme family variant study",
    "Proto-Dravidian sign allograph writing variant phonetic",
    # C1b Bigram/hapax
    "Indus script rare sign low frequency hapax context bigram",
    "Harappan hapax legomenon sign reading function rare inscription",
    # C1c Iconographic
    "Indus seal animal motif sign reading phonetic DEDR Dravidian rebus",
    "Indus iconographic rebus determinative animal clan phonetic Tamil",
    "Indus unicorn zebu rhinoceros seal sign phonetic value reading",
    # C1d Name Zipf
    "Dravidian Tamil personal name system onomastic frequency distribution",
    "Proto-Dravidian anthroponym personal name ancient frequency Zipf",
    "Tamil Sangam personal name frequency onomastic rare common",
    # C1e Munda
    "Munda Austroasiatic Indus Valley Harappan substrate language contact",
    "Munda Santali Mundari IVC language substrate 2020 2025",
    "Austroasiatic Indus substrate phonology sign language ancient",
    # C2a Linear Elamite vocabulary
    "Linear Elamite vocabulary word list sign value Desset 2022 2023 2024",
    "Linear Elamite text inscription reading vocabulary new 2023 2024 2025",
    "Elamite Proto-Dravidian phonological comparison vocabulary bridge new",
    # C2b Trade commodity
    "Meluhha Harappan carnelian cotton ivory trade name Akkadian Sumerian",
    "Bronze Age trade vocabulary commodity name Meluhha Indus phonology",
    "Harappan export import commodity name Akkadian cuneiform PDr phonology",
    "Indus Valley trade carnelian lapis cotton tin name word IVC Mesopotamia",
    # C2c Proto-Elamite
    "Proto-Elamite sign function Indus Harappan parallel comparison",
    "Proto-Elamite decipherment 2020 2022 2024 2025 sign reading",
    "Proto-Elamite Indus script comparison parallel sign function ancient",
    # C2d Sangam hapax
    "Sangam Tamil hapax rare vocabulary archaic substratum Harappan",
    "Old Tamil rare word hapax vocabulary Indus substrate Bronze Age",
    "Sangam corpus vocabulary reconstruction archaic rare Tamil word",
    "Tamil Bronze Age Harappan substrate loanword ancient vocabulary IVC",
    # C2e Meluhha commodity
    "Meluhha trade vocabulary Akkadian Sumerian CDLI new 2024 2025 cuneiform",
    "Ur III Meluhha commodity name trade word vocabulary new",
    "Sargonic Akkadian Meluhhan word name vocabulary cuneiform trade",
]

CROSSREF_QUERIES = [
    "Indus script sign allograph variant grapheme",
    "Munda Austroasiatic Indus Valley substrate language",
    "Linear Elamite vocabulary word sign value 2022 2024",
    "Meluhha trade commodity name Akkadian cuneiform",
    "Sangam Tamil rare hapax vocabulary archaic Harappan",
    "Proto-Elamite Indus comparison sign function",
    "Indus seal iconographic rebus determinative phonetic",
    "Dravidian personal name system onomastic frequency",
    "Bronze Age trade commodity vocabulary phonology India",
    "Harappan carnelian cotton trade name PDr phonology",
]

S2_QUERIES = [
    "Indus script allograph sign variant grapheme positional",
    "Munda Austroasiatic Harappan substrate language contact",
    "Linear Elamite vocabulary new sign values Desset",
    "Meluhha Harappan trade commodity Akkadian name",
    "Sangam Tamil hapax rare vocabulary substratum",
    "Proto-Elamite sign function Indus parallel",
    "Indus iconographic rebus animal seal phonetic",
    "Dravidian onomastic personal name frequency ancient",
    "Harappan trade Bronze Age commodity vocabulary PDr",
]

ARXIV_QUERIES = [
    "Indus script allograph variant rare sign",
    "Munda Austroasiatic Indus Valley language",
    "Linear Elamite vocabulary 2022 2024",
    "Sangam Tamil ancient substrate vocabulary",
    "Proto-Elamite sign function parallel",
    "Dravidian personal name onomastic ancient",
    "Bronze Age trade commodity vocabulary phonology",
    "Indus iconographic determinative rebus",
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


def _classify(text: str) -> tuple[str, str]:
    t = text or ""
    for cid, pats in CEILING_PATTERNS.items():
        for pat in pats:
            if pat.search(t):
                return "STRONG", cid
    for pat in MODERATE_PATTERNS:
        if pat.search(t):
            return "MODERATE", "GENERAL"
    return "WEAK", "NONE"


def track_a_openalex(target):
    print("\n[Track A] OpenAlex (ceiling-breaker clusters)...")
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
            print(f"  OA '{q[:50]}' p{page}: +{added} (total {len(papers)})")
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
        print(f"  CR '{q[:50]}': +{added} (total {len(papers)})")
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
        print(f"  S2 '{q[:50]}': +{added} (total {len(papers)})")
        time.sleep(RATE_SLEEP * 2)
    print(f"  [C] {len(papers)} papers")
    return papers


def track_d_arxiv(target):
    print("\n[Track D] arXiv...")
    papers = []; seen = set(); deadline = time.time() + 240
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
        print(f"  arXiv '{q[:50]}': +{added} (total {len(papers)})")
        time.sleep(RATE_SLEEP)
    print(f"  [D] {len(papers)} papers")
    return papers


def ceiling_analysis(papers: list) -> dict:
    by_ceiling: dict = {cid: [] for cid in CEILING_PATTERNS}
    by_ceiling["GENERAL"] = []
    for p in papers:
        tier, cid = _classify(p["text"])
        p["evidence_tier"] = tier
        p["ceiling_path"]  = cid
        if tier in ("STRONG", "MODERATE") and cid in by_ceiling:
            by_ceiling[cid].append(p)

    summary = {}
    for cid, hits in by_ceiling.items():
        if not hits:
            summary[cid] = {"n": 0, "top_papers": [], "signal": "NO_SIGNAL",
                             "ceiling": cid[0] if cid.startswith("C") else "GEN",
                             "actionable": False}
            continue
        sorted_hits = sorted(hits, key=lambda x: x.get("year", 0), reverse=True)
        signal = "NO_SIGNAL"
        for p in sorted_hits[:10]:
            t = p["text"].lower()
            if any(kw in t for kw in ["open access", "github", "zenodo", "preprint", "download", "available", "dataset"]):
                signal = "DATA_AVAILABLE"; break
            elif any(kw in t for kw in ["2025", "2026", "new find", "recently", "decoded", "solved", "new evidence"]):
                signal = "NEW_EVIDENCE"; break
            elif any(kw in t for kw in ["proposed", "suggest", "candidate", "possible", "potential"]):
                signal = "HYPOTHESIS"; break
        summary[cid] = {
            "n": len(hits),
            "signal": signal,
            "ceiling": "C1" if cid.startswith("C1") else ("C2" if cid.startswith("C2") else "GEN"),
            "actionable": signal in ("DATA_AVAILABLE", "NEW_EVIDENCE"),
            "top_papers": [{"title": p["title"][:80], "year": p.get("year", 0),
                             "source": p.get("source", ""), "id": p.get("id", "")}
                            for p in sorted_hits[:6]],
        }
    return summary


def determine_round2_clusters(ceiling_summary: dict) -> list:
    """Decide whether Round 2 is needed and what additional clusters to target."""
    high_signal = [(cid, info) for cid, info in ceiling_summary.items()
                   if info.get("n", 0) >= 5 and info.get("actionable")]
    low_signal = [(cid, info) for cid, info in ceiling_summary.items()
                  if info.get("n", 0) < 3 and cid != "GENERAL"]

    round2 = []
    for cid, info in low_signal:
        if cid == "C1e_MUNDA_SUBSTRATE":
            round2.extend([
                "Mundari Santali Kurux phonology ancient vocabulary substrate",
                "Austroasiatic Mon-Khmer Bronze Age South Asia language contact",
                "Munda language IVC contact zone Bihar Jharkhand ancient",
            ])
        elif cid == "C2c_PROTO_ELAMITE":
            round2.extend([
                "Proto-Elamite tablet sign distribution function administrative",
                "Proto-Elamite Jemdet Nasr period sign function numerical",
            ])
        elif cid == "C2d_SANGAM_HAPAX":
            round2.extend([
                "Sangam Tamil akam puram rare word lexicography",
                "Old Tamil epigraphy inscription rare word vocabulary Iron Age",
            ])
    return round2


def main():
    t0 = time.time()
    print("=" * 65)
    print("Phase-248 — Ceiling-Breaker Mine 5000")
    print("Targets: C1(allograph/bigram/icon/name/Munda) + C2(LE-vocab/trade/PE/Sangam/Meluhha)")
    print("=" * 65)

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

    print(f"\nTotal papers: {len(all_papers)}")

    ceiling_summary = ceiling_analysis(all_papers)

    print("\n  === CEILING ANALYSIS ===")
    c1_total = sum(info["n"] for cid, info in ceiling_summary.items() if info["ceiling"] == "C1")
    c2_total = sum(info["n"] for cid, info in ceiling_summary.items() if info["ceiling"] == "C2")
    print(f"  Ceiling 1 hits: {c1_total}  |  Ceiling 2 hits: {c2_total}")
    print()
    for cid, info in ceiling_summary.items():
        if cid == "GENERAL": continue
        n = info["n"]
        sig = info["signal"]
        act = "✓" if info["actionable"] else "—"
        marker = "🔓" if sig == "DATA_AVAILABLE" else ("🆕" if sig == "NEW_EVIDENCE" else ("💡" if sig == "HYPOTHESIS" else "·"))
        print(f"  {act} {marker} {cid:30s}: {n:3d} [{sig}]")
        for p in info["top_papers"][:2]:
            print(f"       [{p['year']}] {p['title'][:68]}")

    round2_clusters = determine_round2_clusters(ceiling_summary)
    print(f"\n  Round 2 additional clusters needed: {len(round2_clusters)}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 248,
        "elapsed_s": elapsed,
        "total_papers_fetched": len(all_papers),
        "ceiling_analysis": ceiling_summary,
        "round2_clusters_needed": round2_clusters,
        "strong_papers": sorted(
            [p for p in all_papers if _classify(p["text"])[0] == "STRONG"],
            key=lambda x: x.get("year", 0), reverse=True
        )[:80],
        "c1_total_hits": c1_total,
        "c2_total_hits": c2_total,
        "verdict": (
            f"Phase-248 ceiling-breaker mine: {len(all_papers)} papers. "
            f"C1(rare sign)={c1_total} hits, C2(bilingual)={c2_total} hits. "
            + " | ".join(f"{cid.split('_')[1]}={info['signal'][:3]}({info['n']})"
                         for cid, info in ceiling_summary.items() if cid != "GENERAL")
        ),
    }

    out = OUTPUTS / "phase248_ceiling_breaker_mine.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase248_ceiling_breaker_mine.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase-248 complete in {elapsed}s | {out}")
    print(f"Verdict: {result['verdict'][:200]}")
    return result


if __name__ == "__main__":
    main()
