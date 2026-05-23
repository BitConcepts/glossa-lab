"""Phase 194 — SSRN Fulltext Fetch for E17 and E18

Fetches the two highest-priority 2022/2025 papers from SSRN
(Social Science Research Network — typically open access):

  E17: DOI 10.2139/ssrn.5079207
       "Indus Script's Gemstone and Precious Shiny Commodity Related
        Fish-Signs, and Indus Gemstone Sign Phonology" (2025)

  E18: DOI 10.2139/ssrn.5083945
       "Pleonastic Compounding, Cults and Dynastic Titles: A Few
        Clues to the Indus Signs" (2025/2026)

SSRN paper IDs: 5079207 and 5083945
SSRN abstract pages are publicly accessible; PDFs are often too.

Extraction targets:
  - Sign-phoneme pairs (M-number = phoneme)
  - Fish-sign readings with Dravidian gloss
  - Pleonastic compound sign pairs
  - Comparison with INDUS_FINAL_ANCHORS (agree/conflict)
"""
from __future__ import annotations
import json, re, sys, urllib.parse, urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO_ROOT / "backend"))
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

HTTP_TIMEOUT = 20

PAPERS = [
    {
        "id":      "E17",
        "doi":     "10.2139/ssrn.5079207",
        "ssrn_id": "5079207",
        "title":   "Indus Script's Gemstone and Precious Shiny Commodity Related Fish-Signs",
        "year":    2025,
        "type":    "fish_signs",
    },
    {
        "id":      "E18",
        "doi":     "10.2139/ssrn.5083945",
        "ssrn_id": "5083945",
        "title":   "Pleonastic Compounding, Cults and Dynastic Titles: A Few Clues to the Indus Signs",
        "year":    2025,
        "type":    "pleonastic",
    },
]

# Sign-phoneme extraction patterns
SIGN_PHONEME_PATS = [
    re.compile(r"[Mm]-?(\d{3})\s*[=:]\s*['\"]?([a-zāīūṭḍṇṅñḷṉṟ]{2,12})['\"]?", re.I),
    re.compile(r"sign\s+(?:no\.?\s*)?([A-Z]?\d{2,4})\s+(?:reads?|=|represents?)\s+['\"]?([a-zāīū]{2,12})['\"]?", re.I),
    re.compile(r"(?:P|M)-?(\d{3})\s+(?:reads?|=)\s+['\"]?([a-zāīūṭḍ]{2,12})['\"]?", re.I),
    re.compile(r"fish[- ]sign\s+['\"]?(\d{3})['\"]?\s*(?:=|reads?)\s+['\"]?([a-zāīū]{2,12})['\"]?", re.I),
    re.compile(r"([a-zāīūṭḍṇṅñḷ]{2,10})\s+\((?:fish|min|meen|mīn|gemstone|precious)[^)]{0,30}\)", re.I),
    re.compile(r"(?:Parpola|Mahadevan)\s+(?:P|M)-?(\d{3})\s+(?:=|:)\s+['\"]?([a-zāīūṭ]{2,12})['\"]?", re.I),
]

# Pleonastic compound patterns
PLEONASTIC_PATS = [
    re.compile(r"([Mm]-?\d{3})\s*[+\-]\s*([Mm]-?\d{3})\s*=\s*(.{5,40})", re.I),
    re.compile(r"pleonastic\s+(?:compound\s+)?(?:of\s+)?([a-zāīū]{2,10})\s+(?:and|[+])\s+([a-zāīū]{2,10})", re.I),
]


def _fetch_url(url: str) -> str:
    """Fetch a URL and return raw text (no tag stripping)."""
    try:
        req = urllib.request.Request(
            url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; GlossaLab/0.1; research)",
                "Accept": "text/html,application/xhtml+xml,application/pdf",
            }
        )
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
            raw = r.read()
            try:
                return raw.decode("utf-8", errors="replace")
            except Exception:
                return raw.decode("latin-1", errors="replace")
    except Exception as exc:
        print(f"    Fetch error: {exc}")
        return ""


def try_ssrn_abstract(ssrn_id: str) -> str:
    """Fetch SSRN abstract page."""
    url = f"https://ssrn.com/abstract={ssrn_id}"
    print(f"    Trying SSRN abstract: {url}")
    text = _fetch_url(url)
    if text:
        # Extract abstract div
        m = re.search(r'(?:abstract|Abstract)[^>]*>([^<]{100,3000})', text, re.S)
        if m:
            return re.sub(r'\s+', ' ', m.group(1))[:4000]
        # Try meta description
        m2 = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']{50,})["\']', text, re.I)
        if m2:
            return m2.group(1)[:4000]
    return text[:4000] if text else ""


def try_unpaywall(doi: str) -> tuple[str, str]:
    """Get fulltext URL via Unpaywall."""
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email=tpierson@bitconcepts.tech"
    print(f"    Trying Unpaywall: {doi}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.1"})
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
            data = json.loads(r.read().decode("utf-8", errors="replace"))
        # Find best OA location
        oa = data.get("oa_locations", [])
        for loc in oa:
            pdf_url = loc.get("url_for_pdf") or loc.get("url", "")
            if pdf_url and ("ssrn" in pdf_url.lower() or ".pdf" in pdf_url.lower()):
                return pdf_url, "unpaywall"
        # Fallback: best_oa_location
        best = data.get("best_oa_location") or {}
        url2 = best.get("url_for_pdf") or best.get("url", "")
        return url2, "unpaywall_best"
    except Exception as exc:
        print(f"    Unpaywall error: {exc}")
        return "", ""


def try_crossref_abstract(doi: str) -> str:
    """Get abstract from CrossRef."""
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto=tpierson@bitconcepts.tech"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.1"})
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
            data = json.loads(r.read().decode("utf-8", errors="replace"))
        msg = data.get("message", {})
        abstract = msg.get("abstract", "")
        abstract = re.sub(r"<[^>]+>", " ", abstract)
        title = (msg.get("title", [""])[0]) if msg.get("title") else ""
        return f"{title} {abstract}".strip()[:4000]
    except Exception:
        return ""


def extract_proposals(text: str, paper_type: str) -> list[dict]:
    """Extract sign-phoneme proposals from text."""
    proposals = []
    seen = set()

    for pat in SIGN_PHONEME_PATS:
        for m in pat.finditer(text):
            groups = m.groups()
            if len(groups) >= 2:
                sign_raw  = str(groups[0]).strip()
                phoneme   = str(groups[1]).strip()[:12]
                sign_id   = f"M{sign_raw.zfill(3)}" if sign_raw.isdigit() else sign_raw
                key = (sign_id, phoneme[:4])
                if key in seen:
                    continue
                seen.add(key)
                context = text[max(0, m.start()-60): m.end()+100]
                context = re.sub(r'\s+', ' ', context)
                proposals.append({
                    "sign_id":   sign_id,
                    "phoneme":   phoneme,
                    "context":   context,
                    "pattern":   pat.pattern[:40],
                    "type":      paper_type,
                })

    if paper_type == "pleonastic":
        for pat in PLEONASTIC_PATS:
            for m in pat.finditer(text):
                context = text[max(0, m.start()-40): m.end()+80]
                proposals.append({
                    "sign_id":  "compound",
                    "phoneme":  " + ".join(g for g in m.groups() if g),
                    "context":  re.sub(r'\s+', ' ', context),
                    "pattern":  "pleonastic",
                    "type":     "pleonastic_compound",
                })

    return proposals


def compare_with_anchors(proposals: list[dict], anchors: dict) -> list[dict]:
    """Compare extracted proposals with current anchor set."""
    for p in proposals:
        sid = p.get("sign_id", "")
        ph  = p.get("phoneme", "")
        existing = anchors.get(sid, {})
        if isinstance(existing, dict):
            current_reading = existing.get("reading", "")
            current_conf    = existing.get("confidence", "")
            agrees = ph.lower()[:3] in current_reading.lower() if current_reading else False
            p["current_anchor"] = current_reading
            p["current_conf"]   = current_conf
            p["agrees"]         = agrees
            p["status"] = (
                "CONFIRM_EXISTING" if agrees else
                "CONFLICT"         if current_reading else
                "NEW_PROPOSAL"
            )
        else:
            p["current_anchor"] = ""
            p["current_conf"]   = ""
            p["agrees"]         = False
            p["status"]         = "NEW_PROPOSAL"
    return proposals


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 194 — SSRN Fulltext Fetch for E17/E18")
    print("=" * 60)

    anchors = json.loads(ANCHOR_F.read_text())["anchors"]
    all_results = []

    for paper in PAPERS:
        print(f"\n[{paper['id']}] {paper['title'][:60]}...")
        full_text = ""

        # Try 1: CrossRef abstract
        print("  Try 1: CrossRef abstract")
        abstract = try_crossref_abstract(paper["doi"])
        if abstract and len(abstract) > 100:
            full_text = abstract
            print(f"    Got {len(abstract)} chars from CrossRef")

        # Try 2: Unpaywall → fulltext URL
        if len(full_text) < 500:
            print("  Try 2: Unpaywall")
            ft_url, source = try_unpaywall(paper["doi"])
            if ft_url:
                print(f"    Fulltext URL: {ft_url[:80]}")
                ft_text = _fetch_url(ft_url)
                if ft_text and len(ft_text) > 500:
                    full_text = ft_text[:12000]
                    print(f"    Got {len(full_text)} chars from {source}")

        # Try 3: SSRN abstract page
        if len(full_text) < 200:
            print("  Try 3: SSRN abstract page")
            ssrn_text = try_ssrn_abstract(paper["ssrn_id"])
            if ssrn_text:
                full_text = (full_text + " " + ssrn_text).strip()
                print(f"    Got {len(ssrn_text)} chars from SSRN")

        print(f"  Total text retrieved: {len(full_text)} chars")

        # Extract proposals
        proposals = extract_proposals(full_text, paper["type"])
        proposals = compare_with_anchors(proposals, anchors)

        new_props    = [p for p in proposals if p["status"] == "NEW_PROPOSAL"]
        confirms     = [p for p in proposals if p["status"] == "CONFIRM_EXISTING"]
        conflicts    = [p for p in proposals if p["status"] == "CONFLICT"]

        print(f"  Proposals extracted: {len(proposals)}")
        print(f"    New:      {len(new_props)}")
        print(f"    Confirms: {len(confirms)}")
        print(f"    Conflicts: {len(conflicts)}")

        for p in proposals[:15]:
            print(f"    {p['sign_id']} → {p['phoneme'][:10]} [{p['status']}] {p['context'][:60]}")

        all_results.append({
            "paper_id":   paper["id"],
            "doi":        paper["doi"],
            "title":      paper["title"],
            "text_len":   len(full_text),
            "n_proposals": len(proposals),
            "proposals":  proposals,
            "new":        new_props,
            "confirms":   confirms,
            "conflicts":  conflicts,
            "text_sample": full_text[:1000],
        })

    elapsed = round(time.time() - t0, 1)
    total_new = sum(len(r["new"]) for r in all_results)
    total_confirm = sum(len(r["confirms"]) for r in all_results)

    result = {
        "phase":          194,
        "elapsed_s":      elapsed,
        "papers":         all_results,
        "total_new_proposals": total_new,
        "total_confirms": total_confirm,
        "verdict": (
            f"{total_new} NEW proposals + {total_confirm} confirmations extracted from SSRN fulltext"
            if total_new + total_confirm > 0
            else "No sign-phoneme proposals extracted — papers may be paywalled or abstract-only"
        ),
    }

    print(f"\nPhase 194 complete in {elapsed}s")
    print(f"Verdict: {result['verdict']}")

    out = OUTPUTS / "phase194_ssrn_fulltext.json"
    out.write_text(json.dumps(result, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    (REPORTS / "phase194_ssrn_fulltext.json").write_text(
        json.dumps(result, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
