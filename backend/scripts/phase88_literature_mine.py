"""Phase-88: Targeted Literature Mine + Indus Extraction Pipeline.

Fetches 500+ papers from SemanticScholar, OpenAlex, CrossRef, and EuropePMC
using targeted queries for Indus script decipherment research.

Extraction pipeline applied to each paper:
  1. Parpola-style sign reading patterns (sign ID + phoneme)
  2. P→M crosswalk entries (Parpola number + Mahadevan number)
  3. DEDR rebus candidates (sign depiction + Tamil/DEDR word)
  4. M293-specific evidence (bow reading, ta reading, sign context)
  5. New formula types or grammar patterns

Output: ranked actionable findings with source citations.
CPU only. Output: reports/phase88_literature_mine.json

Note: May take 5-10 minutes due to API rate limiting.
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase88_literature_mine.json"

# Add backend to path for fetchers
sys.path.insert(0, str(REPO / "backend"))
import os

os.environ.setdefault("GLOSSA_DATA_DIR",
                      str(REPO / "backend/data"))

# ── Targeted queries ─────────────────────────────────────────────────────────
# Ordered by specificity / expected yield

QUERIES = [
    # Core Indus/Dravidian reading proposals
    ("indus_dravidian_core",
     "Indus script Dravidian decipherment sign reading",
     ["semanticscholar", "openalex"]),
    # Parpola / Mahadevan sign proposals
    ("parpola_sign_readings",
     "Parpola Indus sign rebus reading Proto-Dravidian",
     ["semanticscholar", "openalex"]),
    # DEDR-based rebus
    ("dedr_rebus_indus",
     "DEDR Dravidian Etymological Dictionary Indus rebus sign",
     ["semanticscholar", "openalex"]),
    # Mahadevan concordance / crosswalk
    ("mahadevan_crosswalk",
     "Mahadevan concordance Indus sign number Parpola crosswalk",
     ["semanticscholar", "openalex"]),
    # M293 specific
    ("m293_bow_sign",
     "Indus script sign bow Tamil Dravidian phoneme",
     ["semanticscholar"]),  # OA hangs on this query
    # Sign-phoneme proposals from scholars
    ("indus_phoneme_proposals",
     "Indus Valley script phoneme syllable Tamil reading proposal",
     ["semanticscholar", "europepmc"]),
    # Grammar / formula structure
    ("indus_grammar_formula",
     "Indus script grammar formula syntactic structure morpheme",
     ["semanticscholar", "openalex"]),
    # Recent work (2020-2026)
    ("recent_indus_work",
     "Indus script decipherment 2020 2021 2022 2023 2024",
     ["semanticscholar", "openalex"]),
]

# ── Sign reading extraction patterns ─────────────────────────────────────────
# Pattern: "sign X/M-NNN reads as/is/= 'WORD'" in various notations

SIGN_READING_PATTERNS = [
    # "sign 47 = 'meen'" style
    re.compile(r"sign\s+(?:no\.?\s*)?(\d{1,3})\s+(?:=|reads?\s+as|represents?|phoneme)\s+['\"]?([a-zāīūṭḍṇṅñḷ]+)['\"]?", re.I),
    # "M047 = meen" style
    re.compile(r"\bM[-_]?(\d{3})\s*=\s*['\"]?([a-zāīūṭḍṇṅñḷ]+)['\"]?", re.I),
    # "P47/M47 reads meen"
    re.compile(r"\b[PM][-_]?(\d{1,3})\s+reads?\s+['\"]?([a-zāīūṭḍṇṅñḷ]+)['\"]?", re.I),
    # "bow sign = vil" style (iconographic description + reading)
    re.compile(r"(bow|fish|unicorn|elephant|tiger|buffalo|tree|jar|comb|arrow|stroke)\s+sign\s+(?:=|reads?|is)\s+['\"]?([a-zāīūṭḍṇṅñḷ]+)['\"]?", re.I),
    # Parpola notation "sign 293 represents 'ta'"
    re.compile(r"sign\s+293\s+(?:=|reads?|represents?|is)\s+['\"]?([a-zāīūṭḍṇṅñḷ]+)['\"]?", re.I),
]

# ── P→M crosswalk patterns ───────────────────────────────────────────────────
CROSSWALK_PATTERNS = [
    # "Parpola sign 47 = Mahadevan M047"
    re.compile(r"Parpola\s+(?:sign\s+)?(?:no\.?\s*)?(\d{1,3})\s+(?:=|corresponds?\s+to|is)\s+Mahadevan\s+(?:M[-_]?)(\d{1,3})", re.I),
    # "P47 = M047"
    re.compile(r"\bP(\d{1,3})\s*=\s*M[-_]?(\d{1,3})\b", re.I),
    # Table entries like "47 | 047"
    re.compile(r"\b(?:P[-_]?)?(\d{1,3})\s+[|:]\s+(?:M[-_]?)?(\d{3})\b"),
]

# ── M293 evidence patterns ────────────────────────────────────────────────────
M293_PATTERNS = [
    re.compile(r"sign\s+293\b", re.I),
    re.compile(r"bow\s+sign\b.*\b(?:vil|ta|ar|val)\b", re.I),
    re.compile(r"\bvil\b.*\bbow\b.*\bindus\b", re.I),
    re.compile(r"\bM[-_]?293\b", re.I),
]

# ── DEDR candidate patterns ───────────────────────────────────────────────────
DEDR_PATTERNS = [
    re.compile(r"DEDR\s+(?:no\.?\s*)?(\d{3,5})\s+['\"]?([a-zāīūṭḍṇṅñḷ]+)['\"]?", re.I),
    re.compile(r"DED\s+(?:no\.?\s*)?(\d{3,5})\s+['\"]?([a-zāīūṭḍṇṅñḷ]+)['\"]?", re.I),
    re.compile(r"Burrow\s+(?:&|and)\s+Emeneau\s+(?:no\.?\s*)?(\d{3,5})", re.I),
]

# ── PD validity check ─────────────────────────────────────────────────────────
PD_VALID_INITIALS = set("vktpcmnyrlaieuo")


def is_pd_plausible(reading: str) -> bool:
    """Quick plausibility check for a Proto-Dravidian reading."""
    r = re.sub(r"[^a-z]", "", reading.lower()[:8])
    if not r or len(r) < 1: return False
    return r[0] in PD_VALID_INITIALS


# ── HTTP fetch helper ─────────────────────────────────────────────────────────

def http_get_json(url: str, params: dict = None, timeout: float = 15.0) -> dict:
    """Simple synchronous JSON GET with User-Agent."""
    import urllib.error
    import urllib.parse
    import urllib.request
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "GlossaLab-IndusMine/0.1 (+glossa-lab@bitconcepts.tech)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"_error": str(e)}


# ── Fetcher implementations ───────────────────────────────────────────────────

def fetch_semanticscholar(query: str, n: int = 100) -> list[dict]:
    """Fetch from SemanticScholar API."""
    from glossa_lab.api.settings import get_key
    api_key = get_key("semantic_scholar_api_key") or ""
    headers = {"x-api-key": api_key} if api_key else {}

    try:
        import concurrent.futures as _cf

        from semanticscholar import SemanticScholar
        sch = SemanticScholar(api_key=api_key or None, timeout=20)
        fields = ["paperId", "title", "abstract", "authors", "year",
                  "citationCount", "tldr", "externalIds"]

        def _do_search():
            return list(sch.search_paper(query, fields=fields, limit=min(n, 100)))

        with _cf.ThreadPoolExecutor(max_workers=1) as ex:
            future = ex.submit(_do_search)
            try:
                raw_results = future.result(timeout=45)  # max 45s per query
            except _cf.TimeoutError:
                print(f"    S2-SDK: timed out for '{query[:40]}' — skipping")
                return []

        papers = []
        for p in raw_results:
            if len(papers) >= n: break
            tldr = getattr(p, "tldr", None)
            tldr_text = ""
            if isinstance(tldr, dict): tldr_text = tldr.get("text", "")
            elif hasattr(tldr, "text"): tldr_text = str(tldr.text or "")
            elif tldr is not None: tldr_text = str(tldr)
            papers.append({
                "title": str(getattr(p, "title", "") or ""),
                "abstract": str(getattr(p, "abstract", "") or ""),
                "year": getattr(p, "year", None),
                "tldr": tldr_text,
                "source": "semanticscholar",
                "citations": getattr(p, "citationCount", 0) or 0,
            })
        print(f"    S2-SDK: {len(papers)} papers for '{query[:40]}'")
        time.sleep(1.2)  # rate limit with API key = 1 req/sec
        return papers
    except Exception as e:
        print(f"    S2 SDK error: {e} — trying HTTP fallback")

    # HTTP fallback
    data = http_get_json(
        "https://api.semanticscholar.org/graph/v1/paper/search",
        params={"query": query, "fields": "title,abstract,year,tldr,citationCount", "limit": min(n, 100)},
    )
    papers = []
    for p in (data.get("data") or []):
        tldr = p.get("tldr") or {}
        papers.append({
            "title": p.get("title", ""),
            "abstract": p.get("abstract", "") or "",
            "year": p.get("year"),
            "tldr": tldr.get("text", "") if isinstance(tldr, dict) else "",
            "source": "semanticscholar",
            "citations": p.get("citationCount", 0) or 0,
        })
    print(f"    S2-HTTP: {len(papers)} papers for '{query[:40]}'")
    time.sleep(2.0)
    return papers


def fetch_openalex(query: str, n: int = 100) -> list[dict]:
    """Fetch from OpenAlex API."""
    from glossa_lab.api.settings import get_key
    oa_email = get_key("openalex_email") or ""
    params = {
        "search": query,
        "per-page": min(n, 200),
        "sort": "cited_by_count:desc",
    }
    if oa_email:
        params["mailto"] = oa_email

    def reconstruct(inv_idx: dict) -> str:
        if not inv_idx: return ""
        pos = sorted((int(i), w) for w, idxs in inv_idx.items() for i in idxs)
        return " ".join(w for _, w in pos)

    data = http_get_json("https://api.openalex.org/works", params=params, timeout=12.0)
    papers = []
    for w in (data.get("results") or []):
        title = (w.get("title") or w.get("display_name") or "").strip()
        abstract = reconstruct(w.get("abstract_inverted_index") or {})
        if not title: continue
        papers.append({
            "title": title,
            "abstract": abstract[:2000],
            "year": w.get("publication_year"),
            "source": "openalex",
            "citations": w.get("cited_by_count", 0) or 0,
        })
    print(f"    OA: {len(papers)} papers for '{query[:40]}'")
    time.sleep(1.0)
    return papers[:n]


def fetch_europepmc(query: str, n: int = 50) -> list[dict]:
    """Fetch from EuropePMC REST API."""
    data = http_get_json(
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        params={"query": query, "resultType": "lite", "pageSize": min(n, 100),
                "format": "json"},
    )
    papers = []
    for p in ((data.get("resultList") or {}).get("result") or []):
        title = p.get("title", "").strip()
        abstract = (p.get("abstractText") or "").strip()
        if not title: continue
        papers.append({
            "title": title,
            "abstract": abstract[:2000],
            "year": p.get("pubYear"),
            "source": "europepmc",
            "citations": p.get("citedByCount", 0) or 0,
        })
    print(f"    EPMC: {len(papers)} papers for '{query[:40]}'")
    time.sleep(1.0)
    return papers[:n]


# ── Extraction functions ──────────────────────────────────────────────────────

def extract_sign_readings(text: str) -> list[dict]:
    """Extract sign-phoneme proposals from text."""
    findings = []
    for pat in SIGN_READING_PATTERNS:
        for m in pat.finditer(text):
            groups = m.groups()
            if len(groups) == 2:
                sign_ref, reading = groups[0], groups[1]
                if is_pd_plausible(reading) and len(reading) >= 2:
                    findings.append({
                        "type": "SIGN_READING",
                        "sign_ref": sign_ref.strip(),
                        "reading": reading.lower().strip(),
                        "context": text[max(0, m.start()-50):m.end()+80].strip(),
                    })
            elif len(groups) == 1:
                # M293-specific match
                reading = groups[0]
                if is_pd_plausible(reading):
                    findings.append({
                        "type": "M293_READING",
                        "sign_ref": "293",
                        "reading": reading.lower().strip(),
                        "context": text[max(0, m.start()-50):m.end()+80].strip(),
                    })
    return findings[:10]  # cap per paper


def extract_crosswalk_entries(text: str) -> list[dict]:
    """Extract P→M crosswalk entries from text."""
    findings = []
    for pat in CROSSWALK_PATTERNS:
        for m in pat.finditer(text):
            groups = m.groups()
            if len(groups) == 2:
                p_num, m_num = groups
                p_id = f"P{int(p_num):03d}"
                m_id = f"M{int(m_num):03d}"
                findings.append({
                    "type": "CROSSWALK_ENTRY",
                    "parpola_id": p_id,
                    "mahadevan_id": m_id,
                    "context": text[max(0, m.start()-30):m.end()+50].strip(),
                })
    return findings[:5]


def extract_m293_evidence(text: str) -> list[dict]:
    """Extract M293-specific evidence from text."""
    findings = []
    for pat in M293_PATTERNS:
        for m in pat.finditer(text):
            ctx = text[max(0, m.start()-80):m.end()+120].strip()
            findings.append({
                "type": "M293_EVIDENCE",
                "context": ctx,
            })
    return findings[:3]


def extract_dedr_entries(text: str) -> list[dict]:
    """Extract DEDR references from text."""
    findings = []
    for pat in DEDR_PATTERNS:
        for m in pat.finditer(text):
            groups = m.groups()
            if len(groups) >= 2:
                dedr_id, reading = groups[0], groups[1]
                findings.append({
                    "type": "DEDR_ENTRY",
                    "dedr_id": f"DEDR {dedr_id}",
                    "reading": reading.lower() if reading else "",
                    "context": text[max(0, m.start()-30):m.end()+60].strip(),
                })
            elif len(groups) == 1:
                findings.append({
                    "type": "DEDR_REFERENCE",
                    "dedr_id": f"DEDR {groups[0]}",
                    "context": text[max(0, m.start()-30):m.end()+60].strip(),
                })
    return findings[:5]


def process_paper(paper: dict) -> list[dict]:
    """Apply full extraction pipeline to a paper."""
    text = f"{paper.get('title','')} {paper.get('abstract','')} {paper.get('tldr','')}"
    if not text.strip(): return []

    findings = []
    findings.extend(extract_sign_readings(text))
    findings.extend(extract_crosswalk_entries(text))
    findings.extend(extract_m293_evidence(text))
    findings.extend(extract_dedr_entries(text))

    # Tag each finding with source
    for f in findings:
        f["paper_title"] = paper.get("title", "")[:100]
        f["paper_year"] = paper.get("year")
        f["paper_source"] = paper.get("source", "")
        f["paper_citations"] = paper.get("citations", 0)

    return findings


def score_finding(f: dict) -> float:
    """Score a finding by actionability."""
    base = {
        "SIGN_READING": 3.0,
        "M293_READING": 5.0,  # highest priority
        "M293_EVIDENCE": 4.0,
        "CROSSWALK_ENTRY": 3.5,
        "DEDR_ENTRY": 2.5,
        "DEDR_REFERENCE": 1.0,
    }.get(f["type"], 1.0)

    # Boost for high-citation papers
    cit = f.get("paper_citations", 0) or 0
    if cit >= 100: base += 1.0
    elif cit >= 20: base += 0.5

    # Boost for recent papers
    year = f.get("paper_year") or 0
    if year >= 2020: base += 0.5
    elif year >= 2010: base += 0.2

    return round(base, 2)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Phase-88: Targeted Literature Mine + Indus Extraction Pipeline\n")

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}
    print(f"  Current HIGH+MEDIUM anchors: {len(confirmed)}")
    print(f"  Target queries: {len(QUERIES)}")
    print("  Sources: SemanticScholar, OpenAlex, EuropePMC\n")

    all_papers: list[dict] = []
    seen_titles: set = set()

    for query_id, query, sources in QUERIES:
        print(f"  Query '{query_id}':")
        per_source = max(60, 500 // (len(QUERIES) * len(sources)))

        for source in sources:
            try:
                import concurrent.futures as _cf2
                def _fetch(src=source, q=query, n=per_source):
                    if src == "semanticscholar":
                        return fetch_semanticscholar(q, n=n)
                    elif src == "openalex":
                        return fetch_openalex(q, n=n)
                    elif src == "europepmc":
                        return fetch_europepmc(q, n=n)
                    return []

                _ex2 = _cf2.ThreadPoolExecutor(max_workers=1)
                _fut2 = _ex2.submit(_fetch)
                try:
                    papers = _fut2.result(timeout=25)  # hard 25s per source/query
                except _cf2.TimeoutError:
                    print(f"    TIMEOUT {source} for '{query[:40]}' — skipping")
                    papers = []
                finally:
                    _ex2.shutdown(wait=False)  # don't block on hanging threads

                # Deduplicate by title
                for p in papers:
                    title_key = re.sub(r"[^a-z0-9]", "", (p.get("title") or "").lower())[:60]
                    if title_key and title_key not in seen_titles:
                        seen_titles.add(title_key)
                        all_papers.append(p)

            except Exception as e:
                print(f"    ERROR {source}: {e}")

    print(f"\n  Total unique papers fetched: {len(all_papers)}")

    # Apply extraction pipeline
    print("\n  Applying Indus extraction pipeline...")
    all_findings: list[dict] = []
    n_with_findings = 0

    for paper in all_papers:
        findings = process_paper(paper)
        if findings:
            n_with_findings += 1
            all_findings.extend(findings)

    print(f"  Papers with findings: {n_with_findings}/{len(all_papers)}")
    print(f"  Raw findings extracted: {len(all_findings)}")

    # Deduplicate findings by (type, sign_ref/dedr_id, reading)
    deduped: dict[str, dict] = {}
    for f in all_findings:
        key = f"{f['type']}|{f.get('sign_ref','')}{f.get('parpola_id','')}{f.get('dedr_id','')}|{f.get('reading','')}"
        if key not in deduped or f.get("paper_citations", 0) > deduped[key].get("paper_citations", 0):
            deduped[key] = f

    unique_findings = list(deduped.values())

    # Score and rank
    for f in unique_findings:
        f["actionability_score"] = score_finding(f)

    unique_findings.sort(key=lambda x: -x["actionability_score"])

    # Categorize
    sign_readings = [f for f in unique_findings if f["type"] in ("SIGN_READING", "M293_READING")]
    m293_evidence = [f for f in unique_findings if "M293" in f["type"]]
    crosswalk_entries = [f for f in unique_findings if f["type"] == "CROSSWALK_ENTRY"]
    dedr_entries = [f for f in unique_findings if f["type"] in ("DEDR_ENTRY", "DEDR_REFERENCE")]

    # Filter sign readings to non-confirmed signs
    new_sign_proposals = []
    for f in sign_readings:
        ref = f.get("sign_ref", "")
        m_id = f"M{int(ref):03d}" if ref.isdigit() else None
        if m_id and m_id not in confirmed:
            f["m_sign_id"] = m_id
            new_sign_proposals.append(f)
        elif not ref.isdigit():  # iconographic reference
            new_sign_proposals.append(f)

    # Filter crosswalk entries to new ones
    existing_crosswalk = {
        entry["parpola_id"] for entry in
        json.loads((REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json").read_text())
        .get("crosswalk", {}).values()
        if "parpola_id" in entry
    }
    new_crosswalk = [f for f in crosswalk_entries
                     if f.get("parpola_id") not in existing_crosswalk]

    print("\n  Extraction results:")
    print(f"    Total unique findings:    {len(unique_findings)}")
    print(f"    Sign reading proposals:   {len(sign_readings)}")
    print(f"    New sign proposals:       {len(new_sign_proposals)}")
    print(f"    M293 evidence items:      {len(m293_evidence)}")
    print(f"    Crosswalk entries:        {len(crosswalk_entries)}")
    print(f"    New crosswalk entries:    {len(new_crosswalk)}")
    print(f"    DEDR references:          {len(dedr_entries)}")

    # Top actionable findings
    print("\n  Top 20 actionable findings:")
    for i, f in enumerate(unique_findings[:20]):
        print(f"    {i+1:2d}. [{f['type']:20s}] score={f['actionability_score']:.1f}  "
              f"{f.get('paper_title','?')[:50]} ({f.get('paper_year','?')})")
        if f.get("reading"):
            print(f"        sign={f.get('sign_ref',f.get('m_sign_id','?'))} reading='{f['reading']}'")
        if f.get("context"):
            print(f"        context: {f['context'][:80]}")

    # M293 summary
    if m293_evidence:
        print(f"\n  M293 evidence summary ({len(m293_evidence)} items):")
        for f in m293_evidence[:5]:
            print(f"    [{f.get('paper_year','?')}] {f.get('paper_title','?')[:60]}")
            print(f"    Context: {f.get('context','?')[:100]}")

    print("\n=== Phase-88 Results ===")
    print(f"  Papers fetched:           {len(all_papers)}")
    print(f"  Unique findings:          {len(unique_findings)}")
    print(f"  New sign proposals:       {len(new_sign_proposals)}")
    print(f"  M293 evidence items:      {len(m293_evidence)}")
    print(f"  New crosswalk entries:    {len(new_crosswalk)}")
    print(f"  High actionability (>=3): {sum(1 for f in unique_findings if f['actionability_score']>=3.0)}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "n_papers_fetched": len(all_papers),
        "n_unique_findings": len(unique_findings),
        "n_actionable_findings": sum(1 for f in unique_findings if f["actionability_score"] >= 2.5),
        "n_new_sign_proposals": len(new_sign_proposals),
        "n_m293_evidence": len(m293_evidence),
        "n_new_crosswalk_entries": len(new_crosswalk),
        "n_dedr_entries": len(dedr_entries),
        "queries_run": [q[0] for q in QUERIES],
        "actionable_findings": unique_findings[:100],  # top 100
        "new_sign_proposals": new_sign_proposals[:30],
        "m293_evidence": m293_evidence[:20],
        "new_crosswalk_entries": new_crosswalk[:30],
        "dedr_entries": dedr_entries[:30],
        "paper_source_breakdown": dict(Counter(p["source"] for p in all_papers)),
        "verdict": (
            f"Phase-88: {len(all_papers)} papers mined from SemanticScholar/OpenAlex/EuropePMC. "
            f"{len(unique_findings)} unique findings extracted. "
            f"{len(new_sign_proposals)} new sign proposals (not yet in anchor set). "
            f"{len(m293_evidence)} M293-specific evidence items found. "
            f"{len(new_crosswalk)} new P→M crosswalk entries. "
            f"Top finding actionability: {unique_findings[0]['actionability_score'] if unique_findings else 0:.1f}/5.0."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
