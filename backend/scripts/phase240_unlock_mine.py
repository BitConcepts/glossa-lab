"""Phase-240: Next-Round Blocker-Unlock Mine

Targets the remaining specific unlocks after Phase-239 achievements:

  UNLOCK-1: Non-Linguistic Scorecard full text
    - Search for preprint / ResearchGate / Academia.edu version
    - Author names, institution, arxiv ID
    - Any additional context about their method/conclusion

  UNLOCK-2: AI-EPIGRAPHY corpus identification
    - Search for preprint or extended version of ACM paper
    - What dataset do they use? Any GitHub/Zenodo link?
    - Authors: contact info for collaboration

  UNLOCK-3: ICIT corpus Fuls post-2014 publications
    - Did Fuls publish ICIT data in any form 2015-2026?
    - Any PhD theses using ICIT data?
    - Related corpora (Possehl, Meadow, other digital Indus)

  UNLOCK-4: 15 remaining LOW anchor phonemes
    - Specific phoneme values needed: search for those PDr roots
    - Signs like M386(maṇ), M321(kol_var), M357(kuḷ) — variant readings
    - Any new computational sign studies covering these

  UNLOCK-5: Gulf seal digital databases
    - British Museum Online Collection search (Dilmun/Failaka)
    - Qatar Museums digital catalog
    - National Museum of Bahrain online
    - Kuwait National Museum Failaka seals

  UNLOCK-6: Keezhadi 2025 new findings
    - Phase 7/8 latest excavation results
    - Any new Tamil-Brahmi graffiti not in our corpus
    - Tamil literacy timeline refinements

  UNLOCK-7: New Elamite lexicon / phonology 2020-2026
    - Updated Elamite dictionaries (Vallat, Tavernier, Malbran-Labat)
    - Any new Linear Elamite decipherment (2022 Desset et al.)
    - Linear Elamite = potential new PDr bridge?

Output: outputs/phase240_unlock_mine.json
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
MAX_PAGES    = 6
PAGE_SIZE    = 200
TARGET       = 5000

# ── Unlock classification patterns ───────────────────────────────────────────

UNLOCK_PATTERNS = {
    "U1_NONLINGUISTIC_SCORECARD": [
        re.compile(r"non.linguistic.*(?:Indus|Harappan).*(?:scorecard|synthetic|baseline|framework)", re.I),
        re.compile(r"(?:Indus|Harappan).*(?:linguistic|non-linguistic).*(?:scorecard|baseline|synthetic|test)", re.I),
        re.compile(r"synthetic.baseline.*(?:Indus|script|linguistic)", re.I),
    ],
    "U2_AI_EPIGRAPHY": [
        re.compile(r"AI.EPIGRAPHY.*(?:Indus|corpus|tool|decipherment)", re.I),
        re.compile(r"(?:Indus|Harappan).*(?:interactive|tool|web|application).*(?:computational|AI|decipher)", re.I),
        re.compile(r"epigraph.*(?:AI|machine|computational).*(?:Indus|ancient|script)", re.I),
    ],
    "U3_ICIT_FULS": [
        re.compile(r"(?:Fuls|ICIT).*(?:Indus|corpus|inscription|database|2015|2016|2017|2018|2019|2020|2021|2022|2023|2024|2025)", re.I),
        re.compile(r"Indus.*(?:Possehl|Meadow|Vidale).*(?:corpus|catalog|database|digital)", re.I),
        re.compile(r"(?:Indus|Harappan).*(?:corpus|catalog|inscription).*(?:digital|database|complete|comprehensive).*(?:2015|2020|2025)", re.I),
    ],
    "U4_LOW_ANCHOR_PHONEMES": [
        re.compile(r"(?:DEDR|Dravidian).*(?:maṇi?|kuḷ|maṇam|nāṭ|kuṟ).*(?:Indus|sign|seal)", re.I),
        re.compile(r"Proto.Dravidian.*(?:variant|allograph|alternant).*(?:sign|syllable|phoneme)", re.I),
        re.compile(r"(?:Indus|Harappan).*(?:sign variant|allograph|grapheme).*(?:reading|phonetic|DEDR)", re.I),
    ],
    "U5_GULF_SEAL_DATABASES": [
        re.compile(r"(?:British Museum|BM).*(?:Dilmun|Failaka|Bahrain|Gulf).*(?:seal|catalog|digital|online)", re.I),
        re.compile(r"(?:Failaka|Bahrain|Kuwait|Qatar).*(?:seal|catalog|museum|digital|online).*(?:Indus|Bronze Age)", re.I),
        re.compile(r"(?:Dilmun|Gulf).*(?:seal catalog|database|digital|online access|museum collection)", re.I),
        re.compile(r"(?:Kuwait National Museum|Bahrain National Museum|Qatar Museums).*(?:seal|Bronze Age|Dilmun)", re.I),
    ],
    "U6_KEEZHADI_2025": [
        re.compile(r"Keezhadi.*(?:Phase [789]|2025|2026|new|latest|finding|discover)", re.I),
        re.compile(r"Keezhadi.*(?:Tamil|Brahmi|inscription|graffiti|literacy).*(?:2025|2026|new)", re.I),
    ],
    "U7_LINEAR_ELAMITE": [
        re.compile(r"Linear Elamite.*(?:decipherment|decoded|solved|read|2022|2023|2024|2025|Desset)", re.I),
        re.compile(r"(?:Desset|Malbran.Labat|Tavernier).*(?:Elamite|Linear Elamite|Proto-Elamite)", re.I),
        re.compile(r"Elamite.*(?:lexicon|dictionary|vocabulary).*(?:update|new|2020|2021|2022|2023|2024|2025)", re.I),
    ],
}

STRONG_ANY = [pat for pats in UNLOCK_PATTERNS.values() for pat in pats]

MODERATE_PATTERNS = [
    re.compile(r"(?:Indus|Harappan).*(?:sign|script|seal).*(?:new|2024|2025|2026)", re.I),
    re.compile(r"(?:Elamite|Proto-Elamite).*(?:2020|2021|2022|2023|2024|2025)", re.I),
    re.compile(r"(?:Gulf|Dilmun|Bahrain|Failaka).*(?:Bronze Age|seal|excavat)", re.I),
    re.compile(r"Keezhadi.*(?:Tamil|Iron Age|excavat)", re.I),
]

OA_CLUSTERS = [
    # U1: Non-Linguistic Scorecard
    "non-linguistic Indus sign system synthetic baseline scorecard 2026",
    "Indus script linguistic test synthetic baseline entropy 2026",
    "Harappan sign system linguistic non-linguistic discrimination framework",
    # U2: AI-EPIGRAPHY
    "AI EPIGRAPHY Indus Valley computational decipherment interactive tool 2025",
    "Indus script computational AI web tool corpus 2025 ACM",
    "machine learning Indus script decipherment tool application 2025",
    # U3: ICIT Fuls
    "Fuls Indus inscription database corpus 2015 2016 2017 2018 2019 2020",
    "Indus corpus digital catalog comprehensive Possehl Meadow 2020 2025",
    "Harappan inscription digitization database comprehensive new 2020 2025",
    # U4: LOW anchor phonemes
    "Proto-Dravidian DEDR variant allograph sign Indus phoneme",
    "Dravidian phonology sign reading variant Indus Harappan DEDR",
    "Indus sign allograph grapheme variant positional reading 2020 2025",
    # U5: Gulf seal databases
    "British Museum Dilmun seal catalog online digital",
    "Failaka Kuwait Bahrain seal catalog database online museum",
    "Gulf Bronze Age seal collection digital museum Dilmun Harappan",
    "Kuwait National Museum Failaka seal Bronze Age Indus cuneiform",
    "Qatar Museums Bronze Age Gulf seal Indus Mesopotamia digital",
    # U6: Keezhadi 2025
    "Keezhadi Phase 7 8 2025 Tamil iron age inscription literacy new",
    "Keezhadi excavation Tamil Brahmi 2025 finding discover",
    "Keezhadi Tamil iron age urbanization 2025 2026 latest results",
    # U7: Linear Elamite
    "Linear Elamite decipherment 2022 2023 2024 Desset decoded",
    "Elamite lexicon dictionary 2020 2021 2022 2023 2024 update new",
    "Proto-Elamite Linear Elamite Dravidian connection bridge PDr",
    "Desset Linear Elamite decipherment Proto-Dravidian phonology",
]

CROSSREF_QUERIES = [
    "non-linguistic Indus sign system synthetic baseline 2026",
    "AI EPIGRAPHY Indus Valley computational tool 2025",
    "Fuls Indus inscription corpus database 2015 2020",
    "Linear Elamite decipherment 2022 2023 Desset",
    "Keezhadi 2025 Tamil iron age literacy",
    "Failaka Bahrain Gulf seal catalog digital museum",
    "Indus corpus comprehensive digital 2020 2025",
    "Elamite lexicon update new vocabulary 2022",
    "British Museum Dilmun seal online catalog",
    "Proto-Dravidian DEDR sign reading variant allograph",
]

S2_QUERIES = [
    "non-linguistic Indus sign synthetic baseline scorecard",
    "AI EPIGRAPHY Indus decipherment tool 2025",
    "Fuls Indus inscription database ICIT",
    "Linear Elamite decipherment Desset 2022",
    "Keezhadi Tamil iron age 2025 literacy",
    "Dilmun Failaka seal Gulf Bronze Age digital",
    "Indus script comprehensive corpus digital 2024",
    "Elamite vocabulary lexicon new 2022 2024",
    "Proto-Dravidian DEDR allograph variant sign reading",
]

ARXIV_QUERIES = [
    "Indus script non-linguistic baseline 2026",
    "Linear Elamite decipherment 2022 2023",
    "Indus script computational tool 2025",
    "Indus corpus dataset new 2025",
    "Elamite Dravidian linguistic family 2024",
    "Keezhadi Tamil inscription 2025",
    "Gulf Bronze Age seal Indus 2024",
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
    for uid, pats in UNLOCK_PATTERNS.items():
        for pat in pats:
            if pat.search(t):
                return "STRONG", uid
    for pat in MODERATE_PATTERNS:
        if pat.search(t):
            return "MODERATE", "GENERAL"
    return "WEAK", "NONE"


def track_a_openalex(target):
    print("\n[Track A] OpenAlex (unlock clusters)...")
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


def unlock_analysis(papers: list) -> dict:
    by_unlock: dict = {uid: [] for uid in UNLOCK_PATTERNS}
    by_unlock["GENERAL"] = []
    for p in papers:
        tier, uid = _classify(p["text"])
        p["evidence_tier"] = tier
        p["unlock_id"] = uid
        if tier in ("STRONG", "MODERATE") and uid in by_unlock:
            by_unlock[uid].append(p)

    summary = {}
    for uid, hits in by_unlock.items():
        if not hits:
            summary[uid] = {"n": 0, "top_papers": [], "signal": "NO_SIGNAL"}
            continue
        sorted_hits = sorted(hits, key=lambda x: x.get("year", 0), reverse=True)
        signal = "NO_SIGNAL"
        for p in sorted_hits[:10]:
            t = p["text"].lower()
            if any(kw in t for kw in ["open access", "github", "zenodo", "preprint", "arxiv", "download", "available"]):
                signal = "DATA_AVAILABLE"
                break
            elif any(kw in t for kw in ["2025", "2026", "new find", "recently", "decoded", "solved"]):
                signal = "NEW_EVIDENCE"
                break
            elif any(kw in t for kw in ["proposed", "suggest", "candidate", "possible"]):
                signal = "HYPOTHESIS"
                break
        summary[uid] = {
            "n": len(hits),
            "signal": signal,
            "top_papers": [{"title": p["title"][:80], "year": p.get("year", 0),
                             "source": p.get("source", ""), "id": p.get("id", "")}
                            for p in sorted_hits[:6]],
        }
    return summary


def main():
    t0 = time.time()
    print("=" * 65)
    print("Phase-240 — Next-Round Blocker-Unlock Mine")
    print("Targets: NonLing Scorecard | AI-EPIGRAPHY | ICIT | LOW anchors | Gulf seals | Keezhadi | Linear Elamite")
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

    strong = [p for p in all_papers if p.get("evidence_tier") == "STRONG" or _classify(p["text"])[0] == "STRONG"]
    # Run analysis (also classifies)
    unlock_summary = unlock_analysis(all_papers)

    strong_count = sum(info["n"] for info in unlock_summary.values() if info.get("n", 0) > 0)
    print(f"  Unlock hits: {strong_count}")

    print("\n  === UNLOCK ANALYSIS ===")
    for uid, info in unlock_summary.items():
        if uid == "GENERAL": continue
        n = info["n"]
        sig = info["signal"]
        marker = "🔓" if sig == "DATA_AVAILABLE" else ("🆕" if sig == "NEW_EVIDENCE" else ("💡" if sig == "HYPOTHESIS" else "—"))
        print(f"  {marker} {uid:30s}: {n:3d} hits [{sig}]")
        for p in info["top_papers"][:2]:
            print(f"       [{p['year']}] {p['title'][:68]}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 240,
        "elapsed_s": elapsed,
        "total_papers_fetched": len(all_papers),
        "unlock_analysis": unlock_summary,
        "strong_papers": sorted(
            [p for p in all_papers if _classify(p["text"])[0] == "STRONG"],
            key=lambda x: x.get("year", 0), reverse=True
        )[:60],
        "verdict": (
            f"Phase-240 unlock mine: {len(all_papers)} papers. "
            + " | ".join(f"{uid.split('_')[0]}={info['signal'][:3]}({info['n']})"
                         for uid, info in unlock_summary.items() if uid != "GENERAL")
        ),
    }

    out = OUTPUTS / "phase240_unlock_mine.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase240_unlock_mine.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase-240 complete in {elapsed}s | {out}")
    print(f"Verdict: {result['verdict']}")
    return result


if __name__ == "__main__":
    main()
