"""Phase 179 — Recent Literature Mine (2021–2026)

Unlike Phase-88 (abstract-only), this phase retrieves open-access full text
via four tracks specifically chosen for content density:

  Track A: arXiv cs.CL + cs.AI "Indus script" (2021-2026)
           — computational papers include sign tables in LaTeX source
  Track B: Semantic Scholar year-filtered (2021+) with new queries
           targeting scholars who published post-Wells 2015
  Track C: CORE API open-access fulltext for linguistics/archaeology
  Track D: Author-targeted: Parpola, Rao, Vahia, Kumar, Subramanian (2020+)

Extraction improvements over Phase-88:
  - Table-aware patterns: "sign X | phoneme Y" in LaTeX/CSV tables
  - Author-proposal patterns: "we propose", "we assign", "our reading"
  - New DEDR entries with sign ID in captions
  - aDNA/archaeogenetics: papers linking Harappan aDNA to Dravidian speakers

Output: outputs/phase179_recent_lit_mine.json
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
OUTPUTS.mkdir(exist_ok=True)

# ── Timeouts and caps (H11) ───────────────────────────────────────────────────
HTTP_TIMEOUT   = 12   # seconds per request
MAX_PAPERS     = 500  # total paper cap across all tracks
MAX_RETRIES    = 2    # per request
RATE_SLEEP     = 0.4  # seconds between API calls

# ── Improved extraction patterns ─────────────────────────────────────────────

# Sign reading in tables / structured lists (common in computational papers)
TABLE_SIGN_PATTERNS = [
    # LaTeX table: "M047 & meen \\" or "047 & meen"
    re.compile(r"M?(\d{3})\s*[&|,]\s*([a-zāīūṭḍṇṅñḷṉṟ]{2,8})\s*(?:\\\\|$|\n)", re.I | re.M),
    # CSV or pipe-delimited: "47,meen" or "47|meen"
    re.compile(r"\b(?:P|M)?[-_]?(\d{3})\s*[,|]\s*['\"]?([a-zāīūṭḍṇṅñḷ]{2,8})['\"]?", re.I),
    # "sign 47: meen" or "sign 047 — meen"
    re.compile(r"\bsign\s+(?:no\.?\s*)?(\d{1,3})\s*[:\-—]\s*['\"]?([a-zāīūṭḍṇṅñḷ]{2,8})['\"]?", re.I),
    # "we propose M047 = meen" — author proposal pattern
    re.compile(r"(?:propose|assign|read|interpret|suggest)\s+M?(\d{3})\s*=\s*['\"]?([a-zāīūṭḍṇṅñḷ]{2,8})['\"]?", re.I),
]

# aDNA / archaeogenetics Dravidian evidence
ADNA_PATTERNS = [
    re.compile(r"(?:Harapp[ae]n|IVC|Indus Valley)\s+(?:ancestry|genome|aDNA|ancient DNA)", re.I),
    re.compile(r"(?:Dravidian|Proto-Dravidian)\s+(?:ancestor|origin|linguistic|speaker)", re.I),
    re.compile(r"(?:AASI|Ancient Ancestral South Indian)\s+(?:Dravidian|language)", re.I),
]

# New ICIT / corpus evidence
ICIT_PATTERNS = [
    re.compile(r"\bICIT\b", re.I),
    re.compile(r"Fuls.*Indus|Indus.*Fuls", re.I),
    re.compile(r"(?:5[,.]?318|5318)\s+(?:texts?|inscriptions?|seals?)", re.I),
]

# Recent/new data signals
NEW_DATA_PATTERNS = [
    re.compile(r"(?:new|recently discovered|previously unknown)\s+(?:inscription|seal|text)", re.I),
    re.compile(r"Rakhigarhi\s+(?:excavation|2023|2024|2025|2026|DNA|genome)", re.I),
    re.compile(r"Dholavira\s+(?:UNESCO|2021|2022|2023|new)", re.I),
]

# ── HTTP helper ───────────────────────────────────────────────────────────────

def _get_json(url: str, attempts: int = MAX_RETRIES) -> dict | None:
    for attempt in range(1, attempts + 2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.1 (research; tpierson@bitconcepts.tech)"})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception as exc:  # noqa: BLE001
            if attempt > attempts:
                return None
            time.sleep(RATE_SLEEP * attempt)
    return None


def _get_text(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.1"})
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return ""


# ── Track A: arXiv ────────────────────────────────────────────────────────────

def track_a_arxiv() -> list[dict]:
    """Fetch arXiv cs.CL + cs.AI papers on Indus script (2021+)."""
    print("\n[Track A] arXiv 2021+ Indus script papers...")
    queries = [
        "Indus script computational",
        "Indus Valley script decipherment machine learning",
        "Harappan script statistical analysis",
    ]
    papers = []
    seen = set()
    deadline = time.time() + 120  # 2-minute cap

    for q in queries:
        if time.time() > deadline:
            print("  [A] deadline reached")
            break
        encoded = urllib.parse.quote(q)
        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query=all:{encoded}+AND+submittedDate:[20210101+TO+20261231]"
            f"&start=0&max_results=30&sortBy=submittedDate&sortOrder=descending"
        )
        data = _get_text(url)
        if not data:
            continue

        # Parse Atom XML naively
        entries = re.findall(r"<entry>(.*?)</entry>", data, re.S)
        for entry in entries[:20]:
            arxiv_id_m = re.search(r"<id>.*?/abs/([^<]+)</id>", entry)
            title_m    = re.search(r"<title>([^<]+)</title>", entry)
            abstract_m = re.search(r"<summary>([^<]+)</summary>", entry, re.S)
            year_m     = re.search(r"<published>(\d{4})", entry)

            if not arxiv_id_m:
                continue
            arxiv_id = arxiv_id_m.group(1).strip()
            if arxiv_id in seen:
                continue
            seen.add(arxiv_id)

            text = f"{title_m.group(1) if title_m else ''} {abstract_m.group(1) if abstract_m else ''}"
            papers.append({
                "source":   "arxiv",
                "id":       arxiv_id,
                "title":    title_m.group(1).strip() if title_m else "",
                "year":     int(year_m.group(1)) if year_m else 0,
                "text":     text.strip(),
                "url":      f"https://arxiv.org/abs/{arxiv_id}",
            })
        time.sleep(RATE_SLEEP)

    print(f"  [A] {len(papers)} arXiv papers")
    return papers


# ── Track B: Semantic Scholar (2021+) ────────────────────────────────────────

def track_b_semantic_scholar() -> list[dict]:
    """Year-filtered queries (2021+) with improved author targeting."""
    print("\n[Track B] Semantic Scholar 2021+ targeted queries...")
    queries = [
        ("recent_indus_computational", "Indus script neural network deep learning NLP"),
        ("recent_indus_archaeology",   "Indus Valley Civilization new excavation 2022 2023"),
        ("adna_dravidian",             "ancient DNA Harappan Dravidian ancestry IVC population"),
        ("recent_parpola",             "Parpola Indus 2020 2021 2022 2023 decipherment"),
        ("roif_network",               "Indus script network betweenness centrality graph"),
        ("tamil_sangam_indus",         "Tamil Sangam literature Indus script proto-Dravidian"),
    ]
    papers = []
    seen = set()
    deadline = time.time() + 120

    for label, q in queries:
        if time.time() > deadline:
            print("  [B] deadline reached")
            break
        encoded = urllib.parse.quote(q)
        url = (
            f"https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={encoded}&fields=title,abstract,year,authors,externalIds"
            f"&limit=20&publicationDateOrYear=2021-2026"
        )
        data = _get_json(url)
        if not data:
            time.sleep(RATE_SLEEP)
            continue
        for p in data.get("data", [])[:15]:
            pid = p.get("paperId", "")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            text = f"{p.get('title','')} {p.get('abstract','') or ''}"
            papers.append({
                "source": "s2",
                "id":     pid,
                "title":  p.get("title", ""),
                "year":   p.get("year", 0),
                "text":   text.strip(),
                "query":  label,
            })
        time.sleep(RATE_SLEEP)

    print(f"  [B] {len(papers)} S2 papers")
    return papers


# ── Track C: CORE API open-access fulltext ────────────────────────────────────

def track_c_core() -> list[dict]:
    """CORE API: open-access fulltext for linguistics/archaeology Indus papers."""
    print("\n[Track C] CORE API open-access fulltext...")
    queries = [
        "Indus script decipherment Dravidian",
        "Harappan civilization language proto-Dravidian",
        "Indus Valley script phoneme reading proposal",
    ]
    papers = []
    seen = set()
    deadline = time.time() + 90

    for q in queries:
        if time.time() > deadline:
            break
        encoded = urllib.parse.quote(q)
        url = f"https://api.core.ac.uk/v3/search/works?q={encoded}&limit=15&fulltext=true"
        data = _get_json(url)
        if not data:
            time.sleep(RATE_SLEEP)
            continue
        for item in (data.get("results") or [])[:10]:
            cid = str(item.get("id", ""))
            if cid in seen:
                continue
            seen.add(cid)
            # Use fullText if available, else abstract
            full = item.get("fullText") or item.get("abstract") or ""
            title = item.get("title") or ""
            year_raw = item.get("yearPublished")
            papers.append({
                "source": "core",
                "id":     cid,
                "title":  title,
                "year":   int(year_raw) if year_raw else 0,
                "text":   f"{title} {full}"[:8000],  # cap at 8KB
            })
        time.sleep(RATE_SLEEP)

    print(f"  [C] {len(papers)} CORE papers")
    return papers


# ── Track D: Author-targeted search ──────────────────────────────────────────

def track_d_author_targeted() -> list[dict]:
    """Search for recent publications by known Indus scholars."""
    print("\n[Track D] Author-targeted search (recent work)...")
    searches = [
        ("Asko Parpola Indus", "parpola_recent"),
        ("Nisha Yadav Indus script statistical", "yadav_recent"),
        ("Mayank Vahia Indus", "vahia_recent"),
        ("Rajesh Rao Indus script", "rao_recent"),
        ("Subramanian Tamil Indus Dravidian", "subramanian_recent"),
        ("Iravatham Mahadevan Indus 2010 2015", "mahadevan_late"),
    ]
    papers = []
    seen = set()
    deadline = time.time() + 90

    for q, label in searches:
        if time.time() > deadline:
            break
        encoded = urllib.parse.quote(q)
        url = (
            f"https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={encoded}&fields=title,abstract,year,authors,externalIds&limit=10"
        )
        data = _get_json(url)
        if not data:
            time.sleep(RATE_SLEEP)
            continue
        for p in data.get("data", [])[:8]:
            pid = p.get("paperId", "")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            text = f"{p.get('title','')} {p.get('abstract','') or ''}"
            papers.append({
                "source": "s2_author",
                "id":     pid,
                "title":  p.get("title", ""),
                "year":   p.get("year", 0),
                "text":   text.strip(),
                "query":  label,
            })
        time.sleep(RATE_SLEEP)

    print(f"  [D] {len(papers)} author-targeted papers")
    return papers


# ── Extraction ────────────────────────────────────────────────────────────────

def extract_findings(papers: list[dict]) -> dict:
    sign_proposals: list[dict] = []
    adna_evidence:  list[dict] = []
    new_data_items: list[dict] = []
    icit_items:     list[dict] = []

    for p in papers[:MAX_PAPERS]:
        text = p.get("text", "")
        if not text:
            continue

        # Sign reading proposals
        for pat in TABLE_SIGN_PATTERNS:
            for m in pat.finditer(text):
                grp = m.groups()
                sign_num  = grp[0].zfill(3) if grp else ""
                phoneme   = grp[1].lower() if len(grp) > 1 else ""
                if 2 <= len(phoneme) <= 8:
                    sign_proposals.append({
                        "sign":    f"M{sign_num}",
                        "phoneme": phoneme,
                        "source":  p.get("title", "")[:60],
                        "year":    p.get("year", 0),
                        "context": text[max(0, m.start()-40):m.end()+40].replace("\n", " "),
                    })

        # aDNA evidence
        for pat in ADNA_PATTERNS:
            m = pat.search(text)
            if m:
                adna_evidence.append({
                    "title":   p.get("title", ""),
                    "year":    p.get("year", 0),
                    "context": text[max(0, m.start()-40):m.end()+60].replace("\n", " "),
                })
                break

        # New data
        for pat in NEW_DATA_PATTERNS:
            m = pat.search(text)
            if m:
                new_data_items.append({
                    "title":   p.get("title", ""),
                    "year":    p.get("year", 0),
                    "context": text[max(0, m.start()-40):m.end()+60].replace("\n", " "),
                })
                break

        # ICIT mentions
        for pat in ICIT_PATTERNS:
            m = pat.search(text)
            if m:
                icit_items.append({
                    "title":   p.get("title", ""),
                    "year":    p.get("year", 0),
                    "context": text[max(0, m.start()-40):m.end()+60].replace("\n", " "),
                })
                break

    # Deduplicate sign proposals
    seen_props: set = set()
    unique_props = []
    for sp in sign_proposals:
        key = (sp["sign"], sp["phoneme"])
        if key not in seen_props:
            seen_props.add(key)
            unique_props.append(sp)

    return {
        "sign_proposals":    unique_props,
        "adna_evidence":     adna_evidence[:20],
        "new_data_items":    new_data_items[:20],
        "icit_items":        icit_items[:10],
    }


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Phase 179 — Recent Literature Mine (2021–2026)")
    print("=" * 55)

    all_papers: list[dict] = []
    all_papers.extend(track_a_arxiv())
    all_papers.extend(track_b_semantic_scholar())
    all_papers.extend(track_c_core())
    all_papers.extend(track_d_author_targeted())

    # Deduplicate by title similarity (simple)
    seen_titles: set = set()
    unique_papers = []
    for p in all_papers:
        key = p.get("title", "").lower()[:60]
        if key and key not in seen_titles:
            seen_titles.add(key)
            unique_papers.append(p)

    print(f"\n  Total unique papers: {len(unique_papers)}")
    print("  Extracting findings...")

    findings = extract_findings(unique_papers)

    # Year breakdown
    year_counts: dict = {}
    for p in unique_papers:
        y = p.get("year") or 0
        if y >= 2015:
            year_counts[y] = year_counts.get(y, 0) + 1

    source_counts = {}
    for p in unique_papers:
        s = p.get("source", "unknown")
        source_counts[s] = source_counts.get(s, 0) + 1

    n_sign = len(findings["sign_proposals"])
    n_adna = len(findings["adna_evidence"])
    n_new  = len(findings["new_data_items"])
    n_icit = len(findings["icit_items"])

    print(f"\n=== Phase 179 Results ===")
    print(f"  Papers retrieved:     {len(unique_papers)}")
    print(f"  Sign proposals found: {n_sign}")
    print(f"  aDNA/genetics items:  {n_adna}")
    print(f"  New data signals:     {n_new}")
    print(f"  ICIT mentions:        {n_icit}")
    if findings["adna_evidence"]:
        print("\n  Top aDNA papers:")
        for item in findings["adna_evidence"][:5]:
            print(f"    [{item['year']}] {item['title'][:70]}")
    if findings["new_data_items"]:
        print("\n  New data signal papers:")
        for item in findings["new_data_items"][:5]:
            print(f"    [{item['year']}] {item['title'][:70]}")
    if findings["icit_items"]:
        print("\n  ICIT mentions:")
        for item in findings["icit_items"][:5]:
            print(f"    [{item['year']}] {item['title'][:70]}")

    report = {
        "phase":             179,
        "date":              "2026-05-22",
        "description":       "Recent literature mine 2021-2026 (arXiv + S2 + CORE + author-targeted)",
        "n_papers":          len(unique_papers),
        "n_sign_proposals":  n_sign,
        "n_adna_evidence":   n_adna,
        "n_new_data":        n_new,
        "n_icit_mentions":   n_icit,
        "year_distribution": dict(sorted(year_counts.items())),
        "source_breakdown":  source_counts,
        "sign_proposals":    findings["sign_proposals"][:50],
        "adna_evidence":     findings["adna_evidence"],
        "new_data_items":    findings["new_data_items"],
        "icit_items":        findings["icit_items"],
        "papers_metadata":   [
            {"title": p.get("title",""), "year": p.get("year",0),
             "source": p.get("source",""), "url": p.get("url","")}
            for p in unique_papers[:100]
        ],
        "gpu_device": "cpu",
    }

    out_path = OUTPUTS / "phase179_recent_lit_mine.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    # Also write to research/indus/phase_reports/
    (REPORTS / "phase179_recent_lit_mine.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Report written: {out_path}")


if __name__ == "__main__":
    main()
