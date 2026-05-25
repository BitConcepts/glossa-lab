"""Phase-259: Ceiling-Targeted Mine 5000

Targeted literature mine to find data/methods to break remaining ceilings:

TARGET 1 — ICIT CORPUS: Find papers referencing Fuls 2014 ICIT dataset,
  any digitised Indus corpus > 2000 objects, or new corpus releases.
TARGET 2 — RARE SIGN METHODS: Papers on rare/low-frequency sign analysis
  in undeciphered scripts (allograph, contextual, iconographic methods).
TARGET 3 — ABSENT PHONEMES: Papers covering /sum/, /gu/, /ab/, /ba/, /shu/
  in Elamo-Dravidian or PDr reconstructions.
TARGET 4 — SA METHODOLOGY: Papers on improving SA/EM decipherment convergence
  with small corpora — constraint methods, hybrid approaches.

Sources: CrossRef, OpenAlex, Semantic Scholar, arXiv
Target: 5000 papers

Output: outputs/phase259_ceiling_mine_5000.json
"""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase259_ceiling_mine_5000.json"

HTTP_TIMEOUT = 15
RATE_SLEEP = 0.35
MAX_PAGES = 6
PAGE_SIZE = 200
TARGET = 5000

# ── Ceiling-specific search patterns ─────────────────────────────────────────

CEILING_PATTERNS = {
    "T1_ICIT_CORPUS": [
        re.compile(r"(?:ICIT|Fuls.*2014|Fuls.*corpus|4[\.,]?537|Indus.*corpus.*new|digitised.*Indus)", re.I),
        re.compile(r"(?:Indus|Harappan).*(?:corpus|dataset|database).*(?:new|expanded|digital|open)", re.I),
        re.compile(r"(?:new|expanded|large).*(?:Indus|Harappan).*(?:corpus|inscription).*(?:data|object|seal)", re.I),
    ],
    "T2_RARE_SIGN": [
        re.compile(r"(?:rare|low.frequency|hapax|infrequent).*(?:sign|symbol|glyph).*(?:undeciphered|ancient|Indus)", re.I),
        re.compile(r"(?:allograph|variant|contextual).*(?:method|analysis|approach).*(?:rare|low.freq|undeciphered)", re.I),
        re.compile(r"(?:Indus|Harappan).*(?:rare|hapax|singleton).*(?:sign|symbol|reading|value)", re.I),
    ],
    "T3_ABSENT_PHONEME": [
        re.compile(r"(?:absent|missing|unattested).*(?:phoneme|phonology).*(?:Dravidian|Elamite|PDr)", re.I),
        re.compile(r"(?:Elamo.Dravidian|McAlpin|PDr).*(?:phoneme|phonology|reconstruct).*(?:gap|absent|missing)", re.I),
        re.compile(r"(?:sum|gu|ab|ba|shu).*(?:phoneme|syllable).*(?:Dravidian|Elamite|PDr|Proto)", re.I),
    ],
    "T4_SA_METHOD": [
        re.compile(r"(?:simulated annealing|EM algorithm|decipherment).*(?:small corpus|convergence|constraint)", re.I),
        re.compile(r"(?:decipher|decode).*(?:constraint|anchor|seed|bootstrap|hybrid).*(?:method|approach|improve)", re.I),
        re.compile(r"(?:NLP|computational).*(?:decipher|decode).*(?:ancient|unknown|undeciphered).*(?:2022|2023|2024|2025|2026)", re.I),
    ],
}

OA_QUERIES = [
    # T1: ICIT/new corpus
    "Indus script corpus digital dataset new expanded objects inscriptions",
    "Fuls 2014 ICIT Indus corpus 4537 objects digital",
    "Harappan seal inscription corpus database open access new",
    "Indus Valley inscription digitised corpus large 2020 2024",
    # T2: Rare sign methods
    "rare sign low frequency undeciphered script allograph method",
    "hapax undeciphered ancient script reading contextual analysis",
    "Indus script rare sign reading method allograph variant",
    "low frequency sign undeciphered writing system approach",
    # T3: Absent phonemes
    "Elamo-Dravidian phoneme reconstruction absent missing gap",
    "Proto-Dravidian phonology reconstruction new McAlpin 2020 2024",
    "Dravidian Elamite phoneme comparison bridge cognate",
    # T4: SA/decipherment methodology
    "simulated annealing decipherment small corpus convergence anchor",
    "computational decipherment constraint bootstrap hybrid neural 2022 2024",
    "ancient script decipherment NLP machine learning 2023 2024 2025",
    "undeciphered script decipherment method improvement recent",
    "Bayesian decipherment ancient writing constraint prior",
]

CROSSREF_QUERIES = [
    "Indus script corpus digital dataset new",
    "ICIT Fuls Indus corpus inscription",
    "rare sign undeciphered script allograph",
    "Elamo-Dravidian phoneme reconstruction",
    "simulated annealing decipherment convergence",
    "computational decipherment ancient script 2024",
    "Indus Harappan inscription database",
    "Proto-Dravidian phonology reconstruction",
    "undeciphered script low frequency sign method",
    "neural decipherment ancient writing system",
]

S2_QUERIES = [
    "Indus script corpus new digital expanded",
    "ICIT Fuls corpus Indus inscriptions",
    "rare sign undeciphered allograph method",
    "Elamo-Dravidian absent phoneme reconstruction",
    "simulated annealing decipherment constraint",
    "computational decipherment 2024 ancient script",
    "Indus Harappan seal inscription new corpus",
    "Proto-Dravidian phoneme gap missing",
]


def _get_json(url: str) -> dict | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/1.0 (tpierson@bitconcepts.tech)"})
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def _classify(title: str, abstract: str = "") -> list[str]:
    text = f"{title} {abstract}"
    hits = []
    for cat, patterns in CEILING_PATTERNS.items():
        for pat in patterns:
            if pat.search(text):
                hits.append(cat)
                break
    return hits


def mine_openalex(queries: list[str], max_total: int = 2000) -> list[dict]:
    papers = []
    seen = set()
    for q in queries:
        if len(papers) >= max_total:
            break
        enc = urllib.parse.quote(q)
        for page in range(1, MAX_PAGES + 1):
            if len(papers) >= max_total:
                break
            url = (f"https://api.openalex.org/works?search={enc}&per_page={PAGE_SIZE}"
                   f"&page={page}&mailto=tpierson@bitconcepts.tech")
            data = _get_json(url)
            if not data or "results" not in data:
                break
            for w in data["results"]:
                wid = w.get("id", "")
                if wid in seen:
                    continue
                seen.add(wid)
                title = w.get("title", "") or ""
                inv = w.get("abstract_inverted_index") or {}
                pos = {}
                for word, locs in inv.items():
                    if isinstance(locs, list):
                        for p in locs:
                            pos[p] = word
                abstract = " ".join(pos[i] for i in sorted(pos))[:500] if pos else ""
                cats = _classify(title, abstract)
                papers.append({
                    "title": title[:200], "year": w.get("publication_year"),
                    "source": "openalex", "id": wid,
                    "ceiling_categories": cats,
                })
            time.sleep(RATE_SLEEP)
    return papers


def mine_crossref(queries: list[str], max_total: int = 1500) -> list[dict]:
    papers = []
    seen = set()
    for q in queries:
        if len(papers) >= max_total:
            break
        enc = urllib.parse.quote(q)
        for offset in range(0, PAGE_SIZE * 3, PAGE_SIZE):
            if len(papers) >= max_total:
                break
            url = (f"https://api.crossref.org/works?query={enc}&rows={PAGE_SIZE}"
                   f"&offset={offset}&mailto=tpierson@bitconcepts.tech")
            data = _get_json(url)
            if not data:
                break
            items = data.get("message", {}).get("items", [])
            if not items:
                break
            for it in items:
                doi = it.get("DOI", "")
                if doi in seen:
                    continue
                seen.add(doi)
                title = " ".join(it.get("title", [])) if isinstance(it.get("title"), list) else str(it.get("title", ""))
                cats = _classify(title)
                papers.append({
                    "title": title[:200], "year": (it.get("published-print") or it.get("published-online") or {}).get("date-parts", [[None]])[0][0],
                    "source": "crossref", "id": doi,
                    "ceiling_categories": cats,
                })
            time.sleep(RATE_SLEEP)
    return papers


def mine_s2(queries: list[str], max_total: int = 1000) -> list[dict]:
    papers = []
    seen = set()
    for q in queries:
        if len(papers) >= max_total:
            break
        enc = urllib.parse.quote(q)
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={enc}&limit=100&fields=title,year,abstract"
        data = _get_json(url)
        if not data or "data" not in data:
            time.sleep(1)
            continue
        for p in data["data"]:
            pid = p.get("paperId", "")
            if pid in seen:
                continue
            seen.add(pid)
            title = p.get("title", "") or ""
            abstract = (p.get("abstract") or "")[:500]
            cats = _classify(title, abstract)
            papers.append({
                "title": title[:200], "year": p.get("year"),
                "source": "s2", "id": pid,
                "ceiling_categories": cats,
            })
        time.sleep(1)
    return papers


def main():
    t0 = time.time()
    print("=" * 70)
    print("PHASE-259: CEILING-TARGETED MINE 5000")
    print("=" * 70)

    print("\n  Mining OpenAlex...")
    oa = mine_openalex(OA_QUERIES, max_total=2500)
    print(f"  OpenAlex: {len(oa)} papers")

    print("  Mining CrossRef...")
    cr = mine_crossref(CROSSREF_QUERIES, max_total=1500)
    print(f"  CrossRef: {len(cr)} papers")

    print("  Mining Semantic Scholar...")
    s2 = mine_s2(S2_QUERIES, max_total=1000)
    print(f"  Semantic Scholar: {len(s2)} papers")

    all_papers = oa + cr + s2
    print(f"\n  Total papers fetched: {len(all_papers)}")

    # Classify by ceiling target
    by_target = {}
    for cat in CEILING_PATTERNS:
        matching = [p for p in all_papers if cat in p.get("ceiling_categories", [])]
        by_target[cat] = {
            "n": len(matching),
            "top_papers": sorted(matching, key=lambda x: -(x.get("year") or 0))[:10],
        }
        print(f"  {cat}: {len(matching)} papers")

    # Actionable findings
    actionable = []
    for cat, info in by_target.items():
        if info["n"] > 0:
            signal = "NEW_EVIDENCE" if info["n"] >= 3 else "HYPOTHESIS"
            actionable.append({"target": cat, "n_papers": info["n"], "signal": signal,
                               "top_paper": info["top_papers"][0]["title"] if info["top_papers"] else ""})

    elapsed = round(time.time() - t0, 1)
    print(f"\n  Actionable targets: {len(actionable)}")
    print(f"  Elapsed: {elapsed}s")

    result = {
        "phase": 259,
        "elapsed_s": elapsed,
        "total_papers_fetched": len(all_papers),
        "by_target": by_target,
        "actionable": actionable,
        "sources": {"openalex": len(oa), "crossref": len(cr), "s2": len(s2)},
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Output: {OUT}")
    print(f"\n{'=' * 70}")
    print(f"PHASE-259 COMPLETE: {len(all_papers)} papers | {len(actionable)} actionable targets")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
