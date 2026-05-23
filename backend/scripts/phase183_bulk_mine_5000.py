"""Phase 183 — Bulk Mine 5000

10x larger than prior mine-500 operations. Five high-volume tracks:

  Track A: OpenAlex paginated bulk (200/page × up to 10 pages)
           Target: 2000+ papers across 10 topic clusters

  Track B: CrossRef full API (100/query × 15 queries)
           Target: 1000+ papers with proper DOI metadata

  Track C: Semantic Scholar deep pagination (50/page × 5 pages × 12 queries)
           New query clusters: Tamil linguistics, archaeometry, South Asian
           prehistory, Bronze Age collapse, Proto-Dravidian reconstruction

  Track D: arXiv expanded (30 queries across cs.CL, q-bio, physics.hist-ph)

  Track E: Wikipedia citation extraction
           Mine reference lists from Wikipedia articles:
           "Indus script", "Harappan civilization", "Dravidian languages",
           "Proto-Dravidian language", "Indus Valley Civilization"
           Each article has 100-300 references.

Evidence pipeline: same STRONG/MODERATE/WEAK classifier as Phase 181-182.

Output: outputs/phase183_bulk_mine_5000.json
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
MAX_PAGES    = 8     # cap per query to stay within reasonable time
PAGE_SIZE    = 200   # OpenAlex max per page
TARGET       = 5000

# ── Evidence patterns (consistent with Phases 181-182) ───────────────────────
STRONG_DRAVIDIAN = [
    re.compile(r"(?:Harapp[ae]n|IVC|Indus Valley).*(?:Dravidian|proto-Dravidian).*(?:ancestor|origin|spoke|language|speaker)", re.I | re.S),
    re.compile(r"(?:Dravidian|proto-Dravidian).*(?:Harapp[ae]n|IVC).*(?:ancestor|origin|genetic|population)", re.I | re.S),
    re.compile(r"AASI.*(?:Dravidian|proto-Dravidian|language)", re.I),
    re.compile(r"(?:ancient|Harapp[ae]n).*(?:genome|DNA|ancestry).*Dravidian", re.I | re.S),
    re.compile(r"Indus.*script.*Dravidian.*(?:confirm|support|evidence|ancestral|answer)", re.I | re.S),
    re.compile(r"(?:Dravidian|Tamil).*(?:Indus|Harapp).*(?:origin|language|ancestor|prove)", re.I | re.S),
]
MODERATE_EVIDENCE = [
    re.compile(r"(?:Harapp[ae]n|IVC|Indus Valley).*(?:ancestry|genome|aDNA|ancient DNA)", re.I),
    re.compile(r"South Asian.*(?:ancient DNA|archaeogenetics|population).*(?:Bronze Age|Chalcolithic|Neolithic)", re.I),
    re.compile(r"(?:AASI|Ancient Ancestral South Indian).*(?:ancestry|genetic|proportion)", re.I),
    re.compile(r"Indus.*(?:script|civilization).*(?:Dravidian|language|linguistic)", re.I),
    re.compile(r"(?:Proto-Dravidian|Tamil-Brahmi).*(?:reconstruct|ancestor|root|origin)", re.I),
    re.compile(r"Rakhigarhi.*(?:genome|DNA|ancestry|language|Dravidian)", re.I),
    re.compile(r"(?:Indus|Harapp).*(?:sign|decipherment).*(?:reading|phoneme|rebus|Dravidian)", re.I),
]
NEW_SIGN_PATTERNS = [
    re.compile(r"M?(\d{3})\s*[=:]\s*['\"]?([a-zāīūṭḍṇṅñḷṉṟ]{2,8})['\"]?", re.I),
    re.compile(r"sign\s+(\d{1,3})\s+(?:reads?|=|is)\s+['\"]?([a-zāīūṭḍṇṅñḷ]{2,8})['\"]?", re.I),
    re.compile(r"(?:P|M)-?(\d{3})\s+(?:reads?|=|represents?)\s+['\"]?([a-zāīūṭḍṇṅñḷ]{2,8})['\"]?", re.I),
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


def _get_text(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.1"})
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
            text = r.read().decode("utf-8", errors="replace")
            # Strip HTML
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text)
            return text[:6000]
    except Exception:  # noqa: BLE001
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


# ── Track A: OpenAlex paginated bulk ─────────────────────────────────────────

OA_QUERY_CLUSTERS = [
    # Core Indus/Dravidian
    "Indus script Dravidian decipherment phoneme",
    "Harappan civilization language proto-Dravidian",
    "Indus Valley script sign reading proposal",
    # Genetics / aDNA
    "Harappan ancient DNA archaeogenetics South Asia",
    "South Asian Bronze Age ancient DNA population admixture",
    "Rakhigarhi genome Dravidian ancestry",
    "AASI Ancient Ancestral South Indian Dravidian",
    # Tamil / Dravidian linguistics
    "Proto-Dravidian language reconstruction phonology",
    "Tamil Brahmi inscription ancient South India",
    "Dravidian languages origin ancestor population",
    # Archaeology
    "Indus Valley Civilization Bronze Age archaeology",
    "Harappan seal inscription material culture",
    "Mohenjo-daro Harappa excavation recent",
    # Contact zone
    "Meluhha Mesopotamia Indus Gulf Bronze Age contact",
    "Persian Gulf trade Indus Dilmun Magan archaeology",
    # Archaeometry / dating
    "Harappan radiocarbon dating climate Bronze Age collapse",
    "Indus Valley arid period monsoon collapse",
    # Writing systems
    "Bronze Age writing system undeciphered script",
    "Proto-writing sign inventory corpus analysis",
    # Recent 2020-2026
    "Indus script computational 2022 2023 2024",
    "Harappan genetics ancient South Asian 2023 2024",
]


def track_a_openalex_bulk() -> list[dict]:
    """OpenAlex paginated — up to PAGE_SIZE × MAX_PAGES per query."""
    print("\n[Track A] OpenAlex bulk paginated...")
    papers = []
    seen: set = set()
    deadline = time.time() + 600  # 10-minute cap

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
            print(f"  OA '{q[:35]}' p{page}: +{added} (total {len(papers)})")
            # Check if there are more pages
            meta = data.get("meta", {})
            total_count = meta.get("count", 0)
            if page * PAGE_SIZE >= total_count:
                break
            page += 1
            time.sleep(RATE_SLEEP)
        time.sleep(RATE_SLEEP)

    print(f"  [A] {len(papers)} OpenAlex papers")
    return papers


# ── Track B: CrossRef full API ───────────────────────────────────────────────

CROSSREF_QUERIES = [
    "Indus script Dravidian phoneme decipherment",
    "Harappan Indus Valley civilization language",
    "proto-Dravidian Tamil ancient South Asia linguistics",
    "Indus inscription sign reading proposal",
    "Rakhigarhi ancient genome South Asia",
    "AASI South Asian ancestral population genetics",
    "Harappan Bronze Age agriculture climate",
    "Meluhha Mesopotamia cuneiform Indus trade",
    "Dravidian language family origin reconstruction",
    "Indus Valley Civilization undeciphered writing",
    "South Asian ancient DNA archaeogenetics Bronze Age",
    "Tamil Brahmi inscription Dravidian ancient",
    "Harappan script statistical entropy analysis",
    "Indus sign corpus frequency positional",
    "Dravidian Indus ancestral speaker hypothesis",
]


def track_b_crossref() -> list[dict]:
    """CrossRef API with rows=100 per query."""
    print("\n[Track B] CrossRef bulk API...")
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
            # Strip JATS XML tags
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
        print(f"  CR '{q[:35]}': +{added}")
        time.sleep(RATE_SLEEP)

    print(f"  [B] {len(papers)} CrossRef papers")
    return papers


# ── Track C: S2 deep pagination ──────────────────────────────────────────────

S2_DEEP_QUERIES = [
    # New clusters not covered before
    "Tamil inscription ancient South India Dravidian epigraphy",
    "Proto-Dravidian reconstruction morphology phonology",
    "Indus Valley Civilization origin migration population",
    "Bronze Age South Asia climate monsoon settlement",
    "Harappan craft production trade network seal",
    "undeciphered script corpus statistical analysis",
    "ancient DNA India Pakistan subcontinent migration",
    "Dravidian substrate Indo-Aryan loanword",
    "South Asian archaeogenetics Chalcolithic Neolithic",
    "Indus script logographic syllabic hypothesis",
    "Harappan Mesopotamia Persian Gulf maritime trade",
    "ancient Tamil Sangam literature historical linguistics",
]


def track_c_s2_deep() -> list[dict]:
    """S2 with offset pagination — 5 pages of 50 per query."""
    print("\n[Track C] Semantic Scholar deep pagination...")
    papers = []
    seen: set = set()
    deadline = time.time() + 360

    for q in S2_DEEP_QUERIES:
        if time.time() > deadline:
            break
        for offset in range(0, 250, 50):  # 5 pages of 50
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
                title = item.get("title", "")
                abstract = item.get("abstract") or ""
                year = item.get("year", 0)
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


# ── Track D: arXiv expanded ──────────────────────────────────────────────────

ARXIV_QUERIES = [
    "Indus script decipherment",
    "Harappan civilization computational",
    "Dravidian language machine learning",
    "South Asian archaeogenetics ancient DNA",
    "proto-Dravidian language NLP",
    "Indus Valley corpus analysis",
    "ancient script undeciphered deep learning",
    "Tamil ancient inscription",
    "Bronze Age South Asia climate",
    "Indus sign frequency distribution",
    "Harappan script statistical",
    "South Asian population genetics ancient",
    "Dravidian phonology reconstruction computational",
    "Indus script entropy information theory",
    "ancient DNA India archaeogenomics",
    "Bronze Age writing system",
    "Rakhigarhi ancient genome",
    "South Asia ancient population migration",
    "Tamil Sangam literature computational",
    "Indus Valley sign network graph",
    "Harappan seal inscription analysis",
    "proto-Dravidian vocabulary DEDR",
    "undeciphered corpus inscription analysis",
    "South Asian Bronze Age Indus",
    "Dravidian language contact archaeology",
    "Harappan genome population structure",
    "ancient South Asian DNA AASI",
    "Indus script linguistic hypothesis",
    "Tamil Brahmi ancient epigraphy",
    "Harappan writing system hypothesis",
]


def track_d_arxiv_expanded() -> list[dict]:
    """arXiv with 30 queries, 50 results each."""
    print("\n[Track D] arXiv expanded (30 queries)...")
    papers = []
    seen: set = set()
    deadline = time.time() + 300

    for q in ARXIV_QUERIES:
        if time.time() > deadline:
            break
        encoded = urllib.parse.quote(q)
        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query=all:{encoded}&start=0&max_results=50"
            f"&sortBy=relevance&sortOrder=descending"
        )
        text = _get_text(url)
        if not text:
            time.sleep(RATE_SLEEP)
            continue

        entries = re.findall(r"<entry>(.*?)</entry>", text, re.S)
        added = 0
        for entry in entries[:40]:
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

            title    = title_m.group(1).strip() if title_m else ""
            abstract = abstract_m.group(1).strip()[:2000] if abstract_m else ""
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
        time.sleep(RATE_SLEEP)

    print(f"  [D] {len(papers)} arXiv papers")
    return papers


# ── Track E: Wikipedia citation extraction ────────────────────────────────────

WIKI_ARTICLES = [
    "Indus_script",
    "Indus_Valley_Civilisation",
    "Dravidian_languages",
    "Proto-Dravidian_language",
    "Harappa",
    "Mohenjo-daro",
    "Rakhigarhi",
    "Tamil_language",
    "Asko_Parpola",
    "Iravatham_Mahadevan",
    "Yajur_Veda",  # Sanskrit contact
    "Indus–Mesopotamia_relations",
    "Shu-ilishu",  # Meluhhan interpreter
]


def track_e_wikipedia() -> list[dict]:
    """Extract references from Wikipedia articles via the MediaWiki API."""
    print("\n[Track E] Wikipedia citation extraction...")
    papers = []
    seen: set = set()
    deadline = time.time() + 240

    for article in WIKI_ARTICLES:
        if time.time() > deadline:
            break

        # Get article content via MediaWiki API
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

        # Extract citation titles from the references section
        # Wikipedia refs look like: |title = Foo Bar | author = ...
        title_matches = re.findall(r"\|\s*title\s*=\s*([^\|\}\n]+)", content)
        author_matches = re.findall(r"\|\s*(?:last|author)\s*=\s*([^\|\}\n]+)", content)
        year_matches   = re.findall(r"\|\s*year\s*=\s*(\d{4})", content)
        doi_matches    = re.findall(r"\|\s*doi\s*=\s*([^\|\}\s\n]+)", content)
        url_matches    = re.findall(r"\|\s*url\s*=\s*(https?://[^\|\}\s\n]+)", content)

        added = 0
        for i, title in enumerate(title_matches[:200]):
            title = title.strip()
            if not title or len(title) < 5:
                continue
            doi   = doi_matches[i] if i < len(doi_matches) else ""
            year_raw = year_matches[i] if i < len(year_matches) else ""
            year  = int(year_raw) if year_raw.isdigit() else 0
            ref_url = url_matches[i] if i < len(url_matches) else ""
            ref_id = doi or ref_url or f"wiki_{article}_{i}"

            if ref_id in seen:
                continue
            seen.add(ref_id)

            papers.append({
                "source":  "wikipedia",
                "id":      ref_id,
                "title":   title,
                "year":    year,
                "text":    title,  # title is the only reliable text here
                "url":     f"https://doi.org/{doi}" if doi else ref_url,
                "wiki_article": article,
            })
            added += 1

        print(f"  Wiki '{article}': +{added} refs")
        time.sleep(RATE_SLEEP)

    print(f"  [E] {len(papers)} Wikipedia refs")
    return papers


# ── Evidence classification ──────────────────────────────────────────────────

def classify_papers(papers: list[dict]) -> dict:
    strong, moderate, weak, sign_proposals = [], [], [], []

    for p in papers:
        text = p.get("text", "")
        if not text or len(text) < 10:
            continue

        entry = {
            "title":  p.get("title", "")[:80],
            "year":   p.get("year") or 0,
            "source": p.get("source", ""),
            "url":    p.get("url", ""),
        }

        is_strong   = any(pat.search(text) for pat in STRONG_DRAVIDIAN)
        is_moderate = any(pat.search(text) for pat in MODERATE_EVIDENCE)

        if is_strong:
            for pat in STRONG_DRAVIDIAN:
                m = pat.search(text)
                if m:
                    entry["key_evidence"] = text[max(0, m.start()-30):m.end()+120].replace("\n", " ")
                    break
            strong.append(entry)
        elif is_moderate:
            for pat in MODERATE_EVIDENCE:
                m = pat.search(text)
                if m:
                    entry["key_evidence"] = text[max(0, m.start()-30):m.end()+80].replace("\n", " ")
                    break
            moderate.append(entry)
        else:
            t = text.lower()
            if any(kw in t for kw in ["indus", "harapp", "dravidian", "sign reading", "decipherment", "tamil brahmi"]):
                weak.append(entry)

        # Check for sign proposals
        for pat in NEW_SIGN_PATTERNS:
            for m in pat.finditer(text):
                grp = m.groups()
                if len(grp) >= 2 and 2 <= len(grp[1]) <= 8:
                    sign_proposals.append({
                        "sign":    f"M{grp[0].zfill(3)}",
                        "phoneme": grp[1].lower(),
                        "source":  p.get("title", "")[:60],
                        "year":    p.get("year", 0),
                        "context": text[max(0, m.start()-40):m.end()+60].replace("\n", " "),
                    })

    # Deduplicate sign proposals
    seen_sp: set = set()
    unique_sp = []
    for sp in sign_proposals:
        k = (sp["sign"], sp["phoneme"])
        if k not in seen_sp:
            seen_sp.add(k)
            unique_sp.append(sp)

    return {
        "strong":        strong[:40],
        "moderate":      moderate[:60],
        "weak":          weak[:30],
        "sign_proposals": unique_sp[:50],
        "n_strong":      len(strong),
        "n_moderate":    len(moderate),
        "n_weak":        len(weak),
        "n_sign_proposals": len(unique_sp),
    }


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Phase 183 — Bulk Mine 5000")
    print("=" * 55)
    t_start = time.time()

    a_papers = track_a_openalex_bulk()
    b_papers = track_b_crossref()
    c_papers = track_c_s2_deep()
    d_papers = track_d_arxiv_expanded()
    e_papers = track_e_wikipedia()

    all_papers = a_papers + b_papers + c_papers + d_papers + e_papers

    # Deduplicate by title (case-insensitive, first 70 chars)
    seen_t: set = set()
    unique: list[dict] = []
    for p in all_papers:
        key = (p.get("title") or "").lower()[:70]
        if key and key not in seen_t:
            seen_t.add(key)
            unique.append(p)

    elapsed = time.time() - t_start
    print(f"\n  Total raw: {len(all_papers)}, unique: {len(unique)}, elapsed: {elapsed:.0f}s")
    print("  Classifying evidence...")

    evidence = classify_papers(unique)
    n_strong   = evidence["n_strong"]
    n_moderate = evidence["n_moderate"]
    n_weak     = evidence["n_weak"]
    n_sign     = evidence["n_sign_proposals"]

    print(f"\n=== Phase 183 Results ===")
    print(f"  Papers retrieved:    {len(unique)}")
    print(f"    OpenAlex paginated: {len(a_papers)}")
    print(f"    CrossRef:           {len(b_papers)}")
    print(f"    S2 deep:            {len(c_papers)}")
    print(f"    arXiv expanded:     {len(d_papers)}")
    print(f"    Wikipedia refs:     {len(e_papers)}")
    print(f"  Evidence classification:")
    print(f"    STRONG:   {n_strong}")
    print(f"    MODERATE: {n_moderate}")
    print(f"    WEAK:     {n_weak}")
    print(f"    Sign proposals: {n_sign}")

    if evidence["strong"]:
        print("\n  STRONG evidence (all):")
        for item in evidence["strong"][:10]:
            print(f"    [{item['year']}] {item['title'][:65]}")
            if item.get("key_evidence"):
                print(f"           → {item['key_evidence'][:100]}")

    if evidence["sign_proposals"]:
        print("\n  Sign proposals found:")
        for sp in evidence["sign_proposals"][:10]:
            print(f"    {sp['sign']} = {sp['phoneme']} — from: {sp['source'][:50]}")

    # Source breakdown
    src: dict = {}
    for p in unique:
        s = p.get("source", "?")
        src[s] = src.get(s, 0) + 1

    # Cumulative totals across all mines
    cumulative = {
        "phase88":  211,  "phase94":  5,   "phase179": 80,
        "phase180": 41,   "phase181": 166, "phase182": 183,
        "phase183": len(unique),
    }
    total_mined = sum(cumulative.values())

    report = {
        "phase":             183,
        "date":              "2026-05-22",
        "description":       "Bulk mine 5000: OpenAlex paginated + CrossRef + S2 deep + arXiv expanded + Wikipedia",
        "n_papers":          len(unique),
        "n_raw":             len(all_papers),
        "source_breakdown":  src,
        "n_strong_evidence": n_strong,
        "n_moderate_evidence": n_moderate,
        "n_weak_evidence":   n_weak,
        "n_sign_proposals":  n_sign,
        "evidence":          evidence,
        "cumulative_mining": cumulative,
        "total_papers_mined_all_phases": total_mined,
        "elapsed_seconds":   round(elapsed),
        "gpu_device":        "cpu",
    }

    out_path = OUTPUTS / "phase183_bulk_mine_5000.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (REPORTS / "phase183_bulk_mine_5000.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Report: {out_path}")
    print(f"  Total papers mined across all phases: {total_mined}")


if __name__ == "__main__":
    main()
