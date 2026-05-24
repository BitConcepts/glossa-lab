"""Phase-237: Blocker-Targeted Mine 5000

Laser-focused on the six concrete blockers that prevent further decipherment:

  BLOCKER-1: ICIT corpus access
    - Is Fuls' ICIT database (4,537 objects) publicly available anywhere?
    - Any alternative Indus corpus that fills the same gap?
    - New digitization projects 2020-2026
    - GitHub / Zenodo / OSF repositories with Indus sign data

  BLOCKER-2: Dilmun/Gulf dual-register seals
    - British Museum digital catalog — Bahrain/Dilmun Bronze Age seals
    - Bahrain National Museum, Tell Abraq (UAE), Failaka (Kuwait)
    - Any publication with Indus + cuneiform on same object
    - New Gulf Bronze Age excavation reports 2020-2026

  BLOCKER-3: CISI-exclusive P-sign readings
    - P324 (kuTi/clan-classifier) — any supporting literature
    - P122 phonetic value confirmation
    - P385 terminal suffix — comparative data
    - Any papers using CISI data computationally

  BLOCKER-4: Elamite cognate extension beyond McAlpin
    - Post-McAlpin Elamo-Dravidian literature (2000-2026)
    - Any new cognate proposals beyond the 20-pair McAlpin list
    - Elamite lexicon updates that add new PDr parallels

  BLOCKER-5: LOW anchor phonological confirmation
    - Papers mentioning specific Indus signs our LOW anchors map to
    - Any new DEDR analysis covering signs in our LOW set
    - Computational sign readings from other groups

  BLOCKER-6: Computational Indus 2024-2026
    - Any new ML/AI Indus decipherment papers
    - New sign corpus datasets published by other researchers
    - Indus script GitHub repositories with new data

Mine structure: 6 targeted track groups, each cluster designed to hit
one specific blocker. Classification includes blocker-ID tagging.

Output: outputs/phase237_blocker_targeted_mine.json
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

# ── Blocker classification patterns ──────────────────────────────────────────

BLOCKER_PATTERNS = {
    "B1_ICIT_CORPUS": [
        re.compile(r"ICIT.*(?:corpus|database|collection|Fuls|sign list)", re.I),
        re.compile(r"Fuls.*(?:ICIT|corpus|4537|4,537|inscriptions|database)", re.I),
        re.compile(r"Indus.*(?:corpus|dataset|digital|digitiz|GitHub|Zenodo|OSF).*(?:new|2020|2021|2022|2023|2024|2025|2026)", re.I),
        re.compile(r"(?:new|comprehensive|expanded).*Indus.*(?:sign|corpus|inscription|dataset)", re.I),
        re.compile(r"Indus.*(?:open|public|access|availabl).*(?:corpus|data|sign)", re.I),
    ],
    "B2_DILMUN_GULF_SEAL": [
        re.compile(r"(?:Dilmun|Bahrain|Failaka|Tell Abraq|Saar).*(?:seal|cuneiform|Indus|bilingual)", re.I),
        re.compile(r"(?:Persian Gulf|Arabian Gulf).*(?:seal|Indus|Bronze Age|bilingual)", re.I),
        re.compile(r"British Museum.*(?:Dilmun|Bahrain|Indus|Gulf).*seal", re.I),
        re.compile(r"(?:Indus|Harappan).*(?:Dilmun|Persian Gulf|Bahrain).*(?:seal|object|artifact)", re.I),
        re.compile(r"Gulf.*Bronze Age.*(?:seal|Indus|cuneiform|script|excavat)", re.I),
    ],
    "B3_CISI_PSIGNS": [
        re.compile(r"(?:CISI|Parpola).*(?:P-sign|sign list|P324|P122|P385|computational)", re.I),
        re.compile(r"Indus.*(?:P-number|Parpola numbering|CISI concordance).*(?:analysis|study|reading)", re.I),
        re.compile(r"(?:kuTi|kuṭi|clan.*classifier|title.*prefix|initial.*determinative).*Indus", re.I),
        re.compile(r"Indus.*(?:P324|P122|P385|P332).*(?:reading|phonetic|function|INITIAL|MEDIAL)", re.I),
    ],
    "B4_ELAMITE_EXTENSION": [
        re.compile(r"Elamite.*Dravidian.*(?:new|extended|additional|further|2000|2010|2020|cognate)", re.I),
        re.compile(r"(?:Elamo.Dravidian|Elamite.Dravidian).*(?:cognate|phoneme|lexicon|2[0-9]{3})", re.I),
        re.compile(r"(?:Proto.Dravidian|PDr).*Elamite.*(?:comparison|bridge|new|extension)", re.I),
        re.compile(r"Elamite.*(?:lexicon|vocabulary|grammar).*(?:update|new|2000|2010|2020)", re.I),
    ],
    "B5_LOW_ANCHOR_PHONOLOGY": [
        re.compile(r"Indus.*(?:phonetic|phonology|reading|sign value).*(?:DEDR|Dravidian|Tamil)", re.I),
        re.compile(r"(?:DEDR|Dravidian Etymological).*(?:Indus|Harappan|sign|seal)", re.I),
        re.compile(r"Indus.*(?:syllabic|phonogram|logogram|determinative).*(?:Tamil|Dravidian|PDr)", re.I),
        re.compile(r"(?:sign reading|sign value|phonetic assignment).*(?:Indus|Harappan).*(?:new|proposed|computational)", re.I),
    ],
    "B6_COMPUTATIONAL_2024_2026": [
        re.compile(r"Indus.*(?:machine learning|neural|deep learning|transformer|LLM|AI).*(?:2024|2025|2026)", re.I),
        re.compile(r"(?:computational|automated).*Indus.*(?:decipher|sign|corpus|analysis).*(?:2024|2025|2026)", re.I),
        re.compile(r"Indus.*(?:GitHub|code|model|dataset|open source).*(?:2024|2025|2026)", re.I),
        re.compile(r"(?:GPT|Claude|LLM|language model).*(?:Indus|Harappan|script|decipher)", re.I),
    ],
}

STRONG_ANY = [pat for pats in BLOCKER_PATTERNS.values() for pat in pats]

MODERATE_PATTERNS = [
    re.compile(r"(?:Indus|Harappan).*(?:sign|script|seal|inscription).*(?:new|recent|2020|2021|2022|2023|2024|2025)", re.I),
    re.compile(r"(?:Gulf|Oman|Bahrain|UAE|Kuwait).*(?:Bronze Age|excavat|archaeolog).*(?:2020|2021|2022|2023|2024|2025)", re.I),
    re.compile(r"(?:Dravidian|Tamil|PDr).*(?:phonolog|lexic|cognate|etymolog).*(?:new|2020|2021|2022|2023|2024|2025)", re.I),
    re.compile(r"(?:cuneiform|Akkadian|Sumerian).*(?:Indus|Meluhha|Harappan).*(?:new|2020|2021|2022|2023|2024|2025)", re.I),
]

# ── OpenAlex clusters (blocker-labelled) ─────────────────────────────────────

OA_CLUSTERS = [
    # B1: ICIT / corpus alternatives
    "ICIT Indus corpus Fuls digital database sign 4537",
    "Indus Valley inscription corpus digitization open access 2020 2025",
    "Harappan sign list new digitized database GitHub repository",
    "Indus script corpus new collection 2022 2023 2024 2025",
    "Indus sign concordance digital humanities computational 2020 2026",
    "Indus inscription dataset Zenodo OSF open source machine learning",
    # B2: Dilmun / Gulf seals
    "Dilmun seal Indus Bahrain cuneiform bilingual Bronze Age",
    "Persian Gulf seal Indus script inscription Harappan Bronze Age",
    "Tell Abraq UAE Indus seal Mesopotamia Bronze Age 2020",
    "British Museum Bahrain Dilmun seal Indus catalog digital",
    "Failaka Kuwait seal Indus Mesopotamia Akkadian inscription",
    "Gulf Bronze Age script seal excavation 2020 2021 2022 2023 2024",
    "Indus Persian Gulf trade bilingual inscription new find",
    # B3: CISI P-signs
    "Parpola CISI sign list P-number concordance computational analysis",
    "Indus script Parpola numbering sign frequency positional profile",
    "CISI corpus inscription computational Indus sign frequency analysis 2020",
    "clan classifier title prefix Indus seal determinative initial sign",
    # B4: Elamite extension
    "Elamite Dravidian new cognate extended phonological 2000 2020",
    "Elamo-Dravidian language family new evidence 2010 2020 2025",
    "Proto-Dravidian Elamite comparison lexicon new pairs bridge",
    "Elamite phonology vocabulary update new analysis 2020 2026",
    # B5: LOW anchor phonology
    "Indus sign phonetic value DEDR Dravidian reading computational",
    "Indus Harappan phonogram logogram determinative sign function Tamil",
    "Dravidian loanword Sanskrit Indus sign reading phonetic assignment",
    "Indus syllabic sign reading Proto-Dravidian phonotactic 2020 2026",
    # B6: Computational 2024-2026
    "Indus script machine learning deep learning 2024 2025 2026",
    "computational Indus decipherment artificial intelligence 2024 2025",
    "Indus script LLM neural network transformer 2024 2025 2026",
    "Indus sign corpus GitHub open source computational 2024 2025",
]

CROSSREF_QUERIES = [
    "ICIT Indus corpus digital database Fuls",
    "Dilmun Persian Gulf seal Indus cuneiform bilingual",
    "Bahrain seal Indus Mesopotamia Bronze Age",
    "Elamite Dravidian new cognate 2010 2020",
    "Indus sign phonetic reading computational 2020 2025",
    "Indus corpus digitization open access dataset",
    "Parpola CISI sign list computational analysis",
    "Indus machine learning neural network 2024",
    "Gulf Bronze Age excavation Indus 2020 2025",
    "Indus DEDR Dravidian phonotactic sign value",
    "Tell Abraq Failaka Dilmun Bronze Age seal",
    "Elamo-Dravidian phonological bridge new evidence",
    "Indus script GitHub dataset repository 2024",
    "Harappan inscription new corpus 2022 2023 2024",
]

S2_QUERIES = [
    "ICIT Indus corpus Fuls digital database",
    "Dilmun Gulf seal Indus cuneiform bilingual Bronze Age",
    "Elamite Dravidian new cognates extended 2020",
    "Indus sign phonetic DEDR Dravidian reading",
    "Indus machine learning 2024 2025 decipherment",
    "Harappan corpus digitization open access",
    "Parpola CISI computational sign frequency",
    "Gulf Bronze Age excavation seal Indus 2022",
    "Indus script neural network transformer AI",
    "Proto-Dravidian Elamite phonological comparison new",
    "Indus corpus GitHub open source dataset",
    "Dilmun Persian Gulf seal bilingual inscription",
]

ARXIV_QUERIES = [
    "Indus script machine learning 2024",
    "Indus Valley computational decipherment",
    "Indus corpus dataset new 2024 2025",
    "Dravidian Elamite language family",
    "Indus sign analysis computational 2025",
    "Gulf Bronze Age linguistics",
    "Indus neural network transformer",
    "Harappan corpus digitization",
    "Indus script new findings 2024 2025",
    "Dilmun Bahrain archaeology 2023 2024",
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
    """Returns (tier, blocker_id)."""
    t = text or ""
    for blocker_id, pats in BLOCKER_PATTERNS.items():
        for pat in pats:
            if pat.search(t):
                return "STRONG", blocker_id
    for pat in MODERATE_PATTERNS:
        if pat.search(t):
            return "MODERATE", "GENERAL"
    return "WEAK", "NONE"


def track_a_openalex(target):
    print("\n[Track A] OpenAlex (blocker clusters)...")
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


def blocker_analysis(papers: list) -> dict:
    """For each blocker, collect its STRONG papers and analyse what they tell us."""
    by_blocker: dict = {bid: [] for bid in BLOCKER_PATTERNS}
    by_blocker["GENERAL"] = []
    for p in papers:
        tier, blocker = _classify(p["text"])
        p["evidence_tier"] = tier
        p["blocker_id"]    = blocker
        if tier in ("STRONG", "MODERATE") and blocker in by_blocker:
            by_blocker[blocker].append(p)

    summary = {}
    for bid, hits in by_blocker.items():
        if not hits:
            summary[bid] = {"n": 0, "top_papers": [], "actionable_signal": "NO_SIGNAL"}
            continue
        sorted_hits = sorted(hits, key=lambda x: x.get("year", 0), reverse=True)
        # Look for actionable keywords in top hits
        actionable = "NO_SIGNAL"
        for p in sorted_hits[:10]:
            t = p["text"].lower()
            if any(kw in t for kw in ["open access", "github", "zenodo", "dataset available", "repository", "download"]):
                actionable = "DATA_AVAILABLE"
                break
            elif any(kw in t for kw in ["new find", "excavation", "2024", "2025", "2026", "recently"]):
                actionable = "NEW_EVIDENCE"
                break
            elif any(kw in t for kw in ["proposed", "suggest", "hypothesis", "possible", "candidate"]):
                actionable = "HYPOTHESIS_CANDIDATE"
                break
        summary[bid] = {
            "n": len(hits),
            "actionable_signal": actionable,
            "top_papers": [{"title": p["title"][:80], "year": p.get("year", 0),
                             "source": p.get("source", "")} for p in sorted_hits[:8]],
        }
    return summary


def main():
    t0 = time.time()
    print("=" * 65)
    print("Phase 237 — Blocker-Targeted Mine 5000")
    print("Targeting: ICIT | Dilmun seals | CISI P-signs | Elamite ext | LOW phonol | Comp 2024")
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

    # Classify and run blocker analysis
    strong = [p for p in all_papers if _classify(p["text"])[0] == "STRONG"]
    moderate = [p for p in all_papers if _classify(p["text"])[0] == "MODERATE"]
    print(f"  STRONG: {len(strong)}   MODERATE: {len(moderate)}")

    blocker_summary = blocker_analysis(all_papers)
    print("\n  === BLOCKER ANALYSIS ===")
    for bid, info in blocker_summary.items():
        signal = info["actionable_signal"]
        n = info["n"]
        marker = "🔓" if signal == "DATA_AVAILABLE" else ("🆕" if signal == "NEW_EVIDENCE" else ("💡" if signal == "HYPOTHESIS_CANDIDATE" else "—"))
        print(f"  {marker} {bid:30s}: {n:3d} hits  [{signal}]")
        for p in info["top_papers"][:3]:
            print(f"      [{p['year']}] {p['title'][:70]}")

    # Determine recommended next experiments
    next_experiments = []
    for bid, info in blocker_summary.items():
        if info["actionable_signal"] == "DATA_AVAILABLE" and info["n"] >= 3:
            next_experiments.append({
                "blocker": bid,
                "priority": "HIGH",
                "recommended_phase": f"Phase-238 ({bid})",
                "rationale": f"{info['n']} papers with data availability signals",
                "top_paper": info["top_papers"][0]["title"] if info["top_papers"] else "",
            })
        elif info["actionable_signal"] == "NEW_EVIDENCE" and info["n"] >= 5:
            next_experiments.append({
                "blocker": bid,
                "priority": "MEDIUM",
                "recommended_phase": f"Phase-238 ({bid})",
                "rationale": f"{info['n']} papers with new evidence signals",
                "top_paper": info["top_papers"][0]["title"] if info["top_papers"] else "",
            })
    next_experiments.sort(key=lambda x: ("HIGH", "MEDIUM", "LOW").index(x["priority"]))

    print("\n  === RECOMMENDED NEXT EXPERIMENTS ===")
    for e in next_experiments[:6]:
        print(f"  [{e['priority']}] {e['recommended_phase']}: {e['rationale']}")
        print(f"         Lead paper: {e['top_paper'][:70]}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 237,
        "elapsed_s": elapsed,
        "total_papers_fetched": len(all_papers),
        "n_strong": len(strong),
        "n_moderate": len(moderate),
        "blocker_analysis": blocker_summary,
        "recommended_next_experiments": next_experiments,
        "strong_papers": sorted(strong, key=lambda x: x.get("year", 0), reverse=True)[:60],
        "clusters": OA_CLUSTERS,
        "verdict": (
            f"Phase-237 blocker mine: {len(all_papers)} papers, {len(strong)} STRONG. "
            f"Blocker signals: " +
            " | ".join(f"{bid.split('_')[0]}={info['actionable_signal'][:3]}({info['n']})"
                       for bid, info in blocker_summary.items() if bid != "GENERAL")
        ),
    }

    out = OUTPUTS / "phase237_blocker_targeted_mine.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase237_blocker_targeted_mine.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase 237 complete in {elapsed}s | {out}")
    print(f"Verdict: {result['verdict']}")
    return result


if __name__ == "__main__":
    main()
