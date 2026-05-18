"""Phase-102: pdfplumber PDF Extraction Pipeline.

Extracts sign reading tables and text from available Indus-related PDFs:
  1. im77intro.pdf — Mahadevan 1977 introduction (sign descriptions)
  2. Any other Indus-related PDFs found in glossa-corpus/indus/sources/

Extraction targets:
  - Sign number tables (e.g., "Sign 47 = meen")
  - Phoneme/reading proposals
  - Crosswalk entries (P-number ↔ M-number)
  - Sign descriptions mentioning specific depictions

CPU only. Output: reports/phase102_pdf_extraction.json
"""
from __future__ import annotations
import json, re
from pathlib import Path

REPO    = Path(__file__).parents[2]
INDUS_SOURCES = REPO / "glossa-corpus/indus/sources"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase102_pdf_extraction.json"

# Sign reading patterns for full-text matching
READING_PATTERNS = [
    re.compile(r"sign\s+(?:no\.?\s*)?(\d{1,3})\s*[=:\-]\s*['\"]?([a-zāīūṭṇḷṟñ]{2,10})['\"]?", re.I),
    re.compile(r"\bno\.\s*(\d{1,3})\b.*?\b([a-zāīūṭṇḷṟñ]{3,10})\b.*?(?:fish|bow|bull|elephant|jar|comb|person)", re.I),
    re.compile(r"DEDR\s+(\d{3,5})[,\s]+['\"]?([a-zāīūṭṇḷṟñ]{2,10})['\"]?", re.I),
    re.compile(r"(\d{3})\s+([a-zāīūṭṇḷṟñ]{3,8})[\s,]+(?:fish|bow|bull|elephant|jar)", re.I),
]

PD_VALID = set("vktpcmnyrlaieuo")

def is_pd_plausible(r: str) -> bool:
    s = re.sub(r"[^a-z]", "", r.lower()[:5])
    return bool(s) and s[0] in PD_VALID and len(s) >= 2


def extract_pdf(pdf_path: Path, max_pages: int = 100) -> dict:
    """Extract text and sign readings from a PDF."""
    result = {
        "path": str(pdf_path),
        "n_pages": 0,
        "total_chars": 0,
        "sign_readings": [],
        "dedr_entries": [],
        "table_data": [],
        "raw_text_sample": "",
        "error": None,
    }

    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            result["n_pages"] = len(pdf.pages)
            full_text = ""
            tables_found = []

            for page_num, page in enumerate(pdf.pages[:max_pages]):
                # Extract text
                text = page.extract_text() or ""
                full_text += f"\n--- PAGE {page_num+1} ---\n" + text

                # Extract tables
                tables = page.extract_tables() or []
                for table in tables:
                    if table and len(table) > 1:
                        # Filter tables that look like sign lists (numbers in first col)
                        has_numbers = any(
                            row and row[0] and re.match(r"^\d{1,3}$", str(row[0]).strip())
                            for row in table[:10]
                        )
                        if has_numbers:
                            tables_found.append({
                                "page": page_num + 1,
                                "rows": [[str(c or "").strip() for c in row]
                                         for row in table[:30]],
                            })

            result["total_chars"] = len(full_text)
            result["raw_text_sample"] = full_text[:2000]
            result["table_data"] = tables_found[:10]

            # Extract sign readings from text
            readings = []
            for pat in READING_PATTERNS:
                for m in pat.finditer(full_text):
                    groups = m.groups()
                    if len(groups) >= 2:
                        sign_num, reading = groups[0], groups[1]
                        if is_pd_plausible(reading):
                            readings.append({
                                "sign_num": sign_num,
                                "m_sign": f"M{int(sign_num):03d}" if sign_num.isdigit() else sign_num,
                                "reading": reading.lower(),
                                "context": full_text[max(0,m.start()-50):m.end()+80].replace("\n"," ")[:200],
                            })

            # Deduplicate
            seen = set()
            for r in readings:
                key = f"{r['sign_num']},{r['reading']}"
                if key not in seen:
                    seen.add(key)
                    result["sign_readings"].append(r)

            print(f"  {pdf_path.name}: {result['n_pages']} pages, {result['total_chars']:,} chars, "
                  f"{len(result['sign_readings'])} sign readings, {len(tables_found)} tables")

    except Exception as e:
        result["error"] = str(e)
        print(f"  ERROR {pdf_path.name}: {e}")

    return result


def main():
    print("Phase-102: PDF Extraction Pipeline\n")

    # Find all PDFs
    pdf_files = []
    if INDUS_SOURCES.exists():
        pdf_files = sorted(INDUS_SOURCES.rglob("*.pdf"))
    print(f"  PDF files found: {len(pdf_files)}")
    for p in pdf_files[:10]:
        print(f"    {p.name}")

    # Load anchors
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH","MEDIUM")}

    all_results = []
    all_sign_readings = []
    all_tables = []

    # Process each PDF (limit to key ones)
    key_pdfs = [p for p in pdf_files if any(kw in p.name.lower()
                for kw in ["im77", "mahadevan", "parpola", "indus", "bulletin", "concordance"])]
    if not key_pdfs:
        key_pdfs = pdf_files[:5]  # fallback: first 5

    print(f"\n  Processing {len(key_pdfs)} key PDFs...")
    for pdf_path in key_pdfs[:10]:
        print(f"\n  [{pdf_path.name}]")
        r = extract_pdf(pdf_path, max_pages=80)
        all_results.append(r)
        all_sign_readings.extend(r["sign_readings"])
        all_tables.extend(r["table_data"])

    # Filter to new anchor candidates
    new_candidates = [sr for sr in all_sign_readings
                      if sr.get("m_sign") and sr["m_sign"] not in confirmed]

    # Show top findings
    print(f"\n  Total sign readings extracted: {len(all_sign_readings)}")
    print(f"  New anchor candidates:         {len(new_candidates)}")
    print(f"  Tables found:                  {len(all_tables)}")

    if new_candidates:
        print(f"\n  Top new candidates:")
        for c in new_candidates[:10]:
            print(f"    {c['m_sign']:6s} -> '{c['reading']}' | {c.get('context','')[:60]}")

    if all_tables:
        print(f"\n  Sample table (first found):")
        t = all_tables[0]
        print(f"    Page {t['page']}, {len(t['rows'])} rows")
        for row in t["rows"][:5]:
            print(f"    {row}")

    # Specific M293 search across all PDFs
    m293_contexts = []
    for r in all_results:
        text = r.get("raw_text_sample", "")
        for pat in [re.compile(r"293", re.I), re.compile(r"\bbow\b", re.I)]:
            for m in pat.finditer(text):
                ctx = text[max(0,m.start()-80):m.end()+150].strip()
                m293_contexts.append({
                    "pdf": Path(r["path"]).name,
                    "context": ctx[:200],
                })

    print(f"\n  M293/bow contexts found: {len(m293_contexts)}")
    for ctx in m293_contexts[:3]:
        print(f"    [{ctx['pdf']}] {ctx['context'][:100]}")

    print(f"\n=== Phase-102 Results ===")
    print(f"  PDFs processed:     {len(all_results)}")
    print(f"  Sign readings:      {len(all_sign_readings)}")
    print(f"  New candidates:     {len(new_candidates)}")
    print(f"  Tables extracted:   {len(all_tables)}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "n_pdfs_processed": len(all_results),
        "n_sign_readings": len(all_sign_readings),
        "n_new_candidates": len(new_candidates),
        "n_tables": len(all_tables),
        "pdf_results": [{
            "name": Path(r["path"]).name,
            "n_pages": r["n_pages"],
            "total_chars": r["total_chars"],
            "n_sign_readings": len(r["sign_readings"]),
            "n_tables": len(r["table_data"]),
            "error": r.get("error"),
        } for r in all_results],
        "new_anchor_candidates": new_candidates[:30],
        "all_sign_readings": all_sign_readings[:50],
        "sample_tables": all_tables[:3],
        "m293_contexts": m293_contexts[:10],
        "verdict": (
            f"Phase-102: Extracted from {len(all_results)} PDFs. "
            f"{len(all_sign_readings)} sign readings found, "
            f"{len(new_candidates)} new anchor candidates. "
            f"{len(all_tables)} tables extracted. "
            f"Key source: im77intro.pdf (Mahadevan 1977 intro)."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
