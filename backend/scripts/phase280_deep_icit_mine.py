"""Phase-280: Deep Mine — ICIT Corpus Data + Missing Sign Lists

Targeted deep search for:
1. ICIT corpus actual DATA — sign lists, frequency tables, inscription sequences
   published in Fuls papers, supplementary materials, or third-party digitizations
2. Fuls publications that contain sign-level data (not just methodology)
3. Any other digitized Indus corpora beyond Holdat (1670) and CISI (178)
4. The 97 CISI-exclusive P-signs identified in Phase-220 — are readings proposed?
5. Holdatllc updates — has the GitHub corpus been expanded since our download?

Strategy: search for specific Fuls paper titles, ICIT mentions with data/table/list,
Wells 2015 data, Mahadevan concordance digitizations, and any Indus sign frequency
tables published in supplementary materials.

Output: outputs/phase280_deep_icit_mine.json
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase280_deep_icit_mine.json"

sys.path.insert(0, str(REPO / "backend"))

HTTP_TIMEOUT = 15
RATE_SLEEP = 0.35


def _get_json(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "GlossaLab/1.0 (tpierson@bitconcepts.tech)"}
        )
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def _get_text(url):
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "GlossaLab/1.0 (tpierson@bitconcepts.tech)"}
        )
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def mine_oa(queries, max_total=3000):
    papers, seen = [], set()
    for q in queries:
        if len(papers) >= max_total:
            break
        enc = urllib.parse.quote(q)
        for page in range(1, 6):
            if len(papers) >= max_total:
                break
            data = _get_json(
                f"https://api.openalex.org/works?search={enc}"
                f"&per_page=200&page={page}&mailto=tpierson@bitconcepts.tech"
            )
            if not data or "results" not in data:
                break
            for w in data["results"]:
                wid = w.get("id", "")
                if wid in seen:
                    continue
                seen.add(wid)
                title = w.get("title") or ""
                inv = w.get("abstract_inverted_index") or {}
                pos = {}
                for word, locs in inv.items():
                    if isinstance(locs, list):
                        for p in locs:
                            pos[p] = word
                abstract = (
                    " ".join(pos[i] for i in sorted(pos))[:800] if pos else ""
                )
                papers.append(
                    {
                        "title": title[:250],
                        "year": w.get("publication_year"),
                        "source": "openalex",
                        "id": wid,
                        "abstract": abstract,
                        "doi": w.get("doi", ""),
                        "host": ((w.get("primary_location") or {}).get("source") or {})
                        .get("display_name", ""),
                    }
                )
            time.sleep(RATE_SLEEP)
    return papers


def mine_cr(queries, max_total=2000):
    papers, seen = [], set()
    for q in queries:
        if len(papers) >= max_total:
            break
        enc = urllib.parse.quote(q)
        for offset in range(0, 600, 200):
            if len(papers) >= max_total:
                break
            data = _get_json(
                f"https://api.crossref.org/works?query={enc}"
                f"&rows=200&offset={offset}&mailto=tpierson@bitconcepts.tech"
            )
            if not data:
                break
            for it in data.get("message", {}).get("items", []):
                doi = it.get("DOI", "")
                if doi in seen:
                    continue
                seen.add(doi)
                title = (
                    " ".join(it.get("title", []))
                    if isinstance(it.get("title"), list)
                    else str(it.get("title", ""))
                )
                papers.append(
                    {
                        "title": title[:250],
                        "year": (
                            it.get("published-print")
                            or it.get("published-online")
                            or {}
                        )
                        .get("date-parts", [[None]])[0][0],
                        "source": "crossref",
                        "id": doi,
                        "abstract": "",
                        "doi": doi,
                    }
                )
            time.sleep(RATE_SLEEP)
    return papers


def mine_s2(queries, max_total=500):
    papers, seen = [], set()
    for q in queries:
        if len(papers) >= max_total:
            break
        enc = urllib.parse.quote(q)
        data = _get_json(
            f"https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={enc}&limit=100&fields=title,year,abstract,externalIds"
        )
        if not data or "data" not in data:
            time.sleep(1)
            continue
        for p in data["data"]:
            pid = p.get("paperId", "")
            if pid in seen:
                continue
            seen.add(pid)
            papers.append(
                {
                    "title": (p.get("title") or "")[:250],
                    "year": p.get("year"),
                    "source": "s2",
                    "id": pid,
                    "abstract": (p.get("abstract") or "")[:800],
                    "doi": (p.get("externalIds") or {}).get("DOI", ""),
                }
            )
        time.sleep(1)
    return papers


# ── Targeted queries for ICIT data ───────────────────────────────────────────
ICIT_DATA_QUERIES = [
    # Fuls specific publications with data
    "Fuls Andreas Indus inscriptions corpus texts table 2014",
    "Fuls ICIT Indus corpus inscriptions texts 4537",
    "Fuls 2023 Indus script positional analysis new writing system perspective",
    "Fuls Berlin Indus sign frequency table list corpus",
    "Fuls Indus script sign list frequency concordance digital",
    # ICIT and large corpora
    "ICIT Indus corpus inscriptions texts digital download supplementary",
    "Indus Valley inscription corpus 4000 objects signs digital",
    "Indus script sign list complete frequency table machine readable",
    "Indus seal inscription database all sites digital corpus 2024 2025",
    # Wells and other digitizations
    "Wells 2015 Indus epigraphy archaeology sign list table",
    "Wells Indus writing corpus dataset sign frequency",
    # Mahadevan concordance
    "Mahadevan 1977 Indus script concordance digital machine readable table",
    "Mahadevan concordance sign list frequency Indus digitized",
    # Holdatllc / GitHub
    "holdatllc Indus corpus GitHub seal inscription digital",
    "Indus script open data GitHub corpus inscription sign list",
    # Specific sign data
    "Indus script sign frequency distribution table all signs complete",
    "Indus seal inscription sign sequence complete list all sites",
    "Parpola CISI Indus sign list corpus volume complete digital",
    # Recent computational work with data
    "Indus script computational analysis corpus data 2024 2025 sign",
    "Indus Valley script dataset open access inscription sequence",
]

SIGN_DATA_PATTERNS = {
    "has_sign_list": re.compile(
        r"(?:sign\s+list|sign\s+table|frequency\s+table|concordance|"
        r"inscription\s+sequence|corpus.*complete|all.*signs|"
        r"supplementary\s+(?:data|material|table))",
        re.I,
    ),
    "has_icit_ref": re.compile(
        r"(?:ICIT|4[\.,]?537|Fuls.*corpus|Fuls.*2014|inscriptions.*texts)", re.I
    ),
    "has_digital_data": re.compile(
        r"(?:download|machine.?readable|digital.*corpus|open\s+(?:data|access)|"
        r"supplementary|GitHub|dataset|CSV|JSON|XML)",
        re.I,
    ),
    "has_fuls": re.compile(r"Fuls", re.I),
    "has_wells": re.compile(r"Wells.*(?:Indus|2015|epigraphy)", re.I),
    "has_mahadevan_digital": re.compile(
        r"Mahadevan.*(?:digital|machine|concordance.*table)", re.I
    ),
    "has_new_corpus": re.compile(
        r"(?:new|expanded|large|complete).*(?:corpus|dataset|database).*"
        r"(?:Indus|Harappan|inscription)",
        re.I,
    ),
}


def classify(papers):
    results = {k: [] for k in SIGN_DATA_PATTERNS}
    for p in papers:
        text = f"{p['title']} {p.get('abstract', '')}"
        for cat, pat in SIGN_DATA_PATTERNS.items():
            if pat.search(text):
                results[cat].append(p)
    return results


def main():
    t0 = time.time()
    print("=" * 70)
    print("PHASE-280: DEEP MINE — ICIT DATA + MISSING SIGN LISTS")
    print("=" * 70)

    print("\n  Mining OpenAlex (deep)...")
    oa = mine_oa(ICIT_DATA_QUERIES, max_total=4000)
    print(f"  OpenAlex: {len(oa)}")

    print("  Mining CrossRef...")
    cr = mine_cr(ICIT_DATA_QUERIES[:12], max_total=2000)
    print(f"  CrossRef: {len(cr)}")

    print("  Mining Semantic Scholar...")
    s2 = mine_s2(ICIT_DATA_QUERIES[:8], max_total=500)
    print(f"  S2: {len(s2)}")

    all_papers = oa + cr + s2
    print(f"\n  Total: {len(all_papers)}")

    # Classify
    results = classify(all_papers)

    print("\n=== CLASSIFICATION ===")
    for cat, papers in results.items():
        # Deduplicate by title
        unique = []
        seen_titles = set()
        for p in sorted(papers, key=lambda x: -(x.get("year") or 0)):
            t_norm = p["title"].lower()[:60]
            if t_norm not in seen_titles:
                seen_titles.add(t_norm)
                unique.append(p)
        results[cat] = unique
        print(f"\n  {cat}: {len(unique)} papers")
        for p in unique[:5]:
            print(f"    [{p.get('year', '?')}] {p['title'][:80]}")
            if p.get("doi"):
                print(f"           doi: {p['doi']}")
            if p.get("abstract"):
                # Show relevant snippet
                text = p["abstract"]
                for kw in [
                    "corpus",
                    "sign",
                    "ICIT",
                    "Fuls",
                    "table",
                    "frequency",
                    "data",
                    "download",
                    "supplementary",
                ]:
                    idx = text.lower().find(kw.lower())
                    if idx >= 0:
                        start = max(0, idx - 30)
                        print(f"           ...{text[start:start+120]}...")
                        break

    # ── Check holdatllc GitHub for updates ───────────────────────────────────
    print("\n=== HOLDATLLC GITHUB CHECK ===")
    gh_data = _get_json(
        "https://api.github.com/repos/holdatllc/indus/commits?per_page=5"
    )
    if gh_data and isinstance(gh_data, list):
        print(f"  Latest commits: {len(gh_data)}")
        for c in gh_data[:3]:
            msg = c.get("commit", {}).get("message", "")[:80]
            date = c.get("commit", {}).get("author", {}).get("date", "")[:10]
            print(f"    [{date}] {msg}")
    else:
        print("  Could not fetch (may be rate-limited)")

    elapsed = round(time.time() - t0, 1)

    # ── Actionable findings ─────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("ACTIONABLE FINDINGS")
    print("=" * 70)

    actionable = []
    if results["has_fuls"]:
        actionable.append(
            {
                "action": "Contact Fuls",
                "detail": f"{len(results['has_fuls'])} Fuls papers found. "
                "ICIT corpus is his creation. Direct contact is the fastest path.",
                "papers": [p["title"][:80] for p in results["has_fuls"][:3]],
            }
        )
    if results["has_digital_data"]:
        actionable.append(
            {
                "action": "Check supplementary materials",
                "detail": f"{len(results['has_digital_data'])} papers mention "
                "downloadable/digital data. Check DOIs for supplementary files.",
                "papers": [p["title"][:80] for p in results["has_digital_data"][:3]],
            }
        )
    if results["has_new_corpus"]:
        actionable.append(
            {
                "action": "New corpus leads",
                "detail": f"{len(results['has_new_corpus'])} papers mention new/expanded corpora.",
                "papers": [p["title"][:80] for p in results["has_new_corpus"][:3]],
            }
        )
    if results["has_sign_list"]:
        actionable.append(
            {
                "action": "Sign list/frequency data",
                "detail": f"{len(results['has_sign_list'])} papers have sign lists or frequency tables.",
                "papers": [p["title"][:80] for p in results["has_sign_list"][:3]],
            }
        )

    for a in actionable:
        print(f"\n  [{a['action']}] {a['detail']}")
        for p in a["papers"]:
            print(f"    → {p}")

    result = {
        "phase": 280,
        "elapsed_s": elapsed,
        "total_papers": len(all_papers),
        "by_category": {k: len(v) for k, v in results.items()},
        "top_papers": {
            k: [
                {
                    "title": p["title"],
                    "year": p.get("year"),
                    "doi": p.get("doi", ""),
                    "abstract_snippet": p.get("abstract", "")[:200],
                }
                for p in v[:5]
            ]
            for k, v in results.items()
        },
        "actionable": actionable,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Output: {OUT}")
    print(f"  Elapsed: {elapsed}s")
    print(f"\n{'='*70}")
    print("PHASE-280 COMPLETE")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
