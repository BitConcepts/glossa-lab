"""Extract real Indus sign sequences from Fuls (2023) PDF books.

Processes:
  A Catalog of Indus Signs.pdf   -- per-sign stats + ICIT IDs
  Corpus of Indus Inscriptions.pdf -- actual inscription sign sequences

Strategy:
  1. Extract text page by page (chunked, never loads entire PDF at once).
  2. Scan the Corpus PDF for sign sequences (lines of 3-digit Fuls codes
     like "032 031 740" or numeric patterns near inscription IDs).
  3. Build ICIT_ID -> [sign_sequence] mapping.
  4. Fall back to the TXT-based inversion if the PDF has no text layer.
  5. Save results to reports/.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_CATALOG_PDF = Path(
    r"C:\Users\trist\OneDrive\Documents\My Kindle Content\A Catalog of Indus Signs.pdf"
)
_CORPUS_PDF = Path(
    r"C:\Users\trist\OneDrive\Documents\My Kindle Content\Corpus of Indus Inscriptions.pdf"
)
_REPORTS = Path(__file__).parent.parent / "reports"


# ── PDF text extraction (page-by-page, chunked) ───────────────────────


def extract_pages(pdf_path: Path, start: int = 0, end: int | None = None):
    """Yield (page_num, text) for pages [start, end) using pypdf."""
    import pypdf
    reader = pypdf.PdfReader(str(pdf_path))
    total = len(reader.pages)
    end = end or total
    end = min(end, total)
    print(f"  PDF: {total} pages total, extracting {start}–{end-1}")
    for i in range(start, end):
        text = reader.pages[i].extract_text() or ""
        yield i, text


def sample_pages(pdf_path: Path, pages: list[int]) -> dict[int, str]:
    """Extract a specific set of page numbers — fast diagnostic tool."""
    import pypdf
    reader = pypdf.PdfReader(str(pdf_path))
    total = len(reader.pages)
    result = {}
    for p in pages:
        if 0 <= p < total:
            result[p] = reader.pages[p].extract_text() or ""
    return result


# ── Step 1: Diagnose what's in the PDFs ───────────────────────────────


def diagnose(pdf_path: Path, sample_size: int = 10) -> dict:
    """Sample pages to understand the PDF's text layer structure."""
    import pypdf
    reader = pypdf.PdfReader(str(pdf_path))
    total = len(reader.pages)
    step = max(1, total // sample_size)
    samples = list(range(0, total, step))[:sample_size]

    results = []
    for p in samples:
        text = reader.pages[p].extract_text() or ""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        results.append({
            "page": p,
            "n_chars": len(text),
            "n_lines": len(lines),
            "first_3_lines": lines[:3],
            "last_3_lines": lines[-3:],
            # Check for numeric patterns that could be sign codes
            "has_sign_codes": bool(re.search(r"\b\d{3}\s+\d{3}\b", text)),
            "has_icit_pattern": bool(re.search(r"ICIT|CISI|\bH-\d+\b|\bM-\d+\b", text)),
        })

    return {"total_pages": total, "samples": results}


# ── Step 2: Parse Corpus PDF ──────────────────────────────────────────


def parse_corpus_pdf(pdf_path: Path) -> tuple[dict[int, list[str]], dict[int, dict]]:
    """
    Extract sign sequences and metadata from the Corpus PDF.

    Returns:
      sequences: {icit_id: [sign_ids_in_order]}
      metadata:  {icit_id: {cisi, site, type, direction}}
    """
    import pypdf
    reader = pypdf.PdfReader(str(pdf_path))
    total = len(reader.pages)

    sequences: dict[int, list[str]] = {}
    metadata: dict[int, dict] = {}
    site = "Unknown"

    # Patterns for the Corpus layout
    site_re = re.compile(r"^\d+\.\d+\.\s+([A-Z][A-Z\s\-]+?)(?:\s+\d+)?$")
    # Inscription header: "1234 H-567 R/L Bull"  or  "1234 M-567 ..."
    insc_re = re.compile(r"^(\d{1,5})\s+([\w\-]+)\s+(R/L|L/R|NR|-)\s+(\S+)")
    # Sign sequence: 3+ space-separated 3-digit numbers (Fuls codes)
    sign_seq_re = re.compile(r"^((?:\d{3}\s+){1,}\d{3})\s*$")
    # Also look for 3-digit codes on a line with an ICIT entry
    sign_inline_re = re.compile(r"\b(\d{3})\b")

    current_id: int | None = None

    for page_num in range(total):
        text = reader.pages[page_num].extract_text() or ""
        lines = text.splitlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Site heading
            m = site_re.match(line)
            if m and len(line) < 60:
                candidate = m.group(1).strip().title()
                if candidate not in ("Chapter", "Inscriptions", "Contents"):
                    site = candidate
                continue

            # Inscription header
            m = insc_re.match(line)
            if m:
                current_id = int(m.group(1))
                cisi = m.group(2)
                direction = m.group(3)
                if current_id not in metadata:
                    metadata[current_id] = {
                        "icit_id": current_id,
                        "cisi": cisi,
                        "direction": direction,
                        "site": site,
                        "type": "",
                    }
                continue

            # Type line
            if current_id and re.match(r"^(SEAL|TAB|POT|MISC)", line):
                if not metadata.get(current_id, {}).get("type"):
                    metadata.setdefault(current_id, {})["type"] = line.split()[0]
                continue

            # Sign sequence line: 3+ runs of 3-digit codes
            m = sign_seq_re.match(line)
            if m and current_id:
                codes = m.group(1).split()
                # Validate: all 3-digit codes between 001 and 999
                if all(c.isdigit() and len(c) == 3 for c in codes):
                    sequences.setdefault(current_id, []).extend(codes)
                continue

    return sequences, metadata


# ── Step 3: Parse Catalog PDF (ICIT IDs, enhanced) ────────────────────


def parse_catalog_pdf(pdf_path: Path) -> dict[str, dict]:
    """
    Extract per-sign statistics and ICIT_IDs from the Catalog PDF.
    More reliable than TXT version because long ID lists won't be truncated.
    """
    import pypdf
    reader = pypdf.PdfReader(str(pdf_path))
    total = len(reader.pages)

    full_text_parts: list[str] = []
    for i in range(total):
        full_text_parts.append(reader.pages[i].extract_text() or "")

    full_text = "\n".join(full_text_parts)

    # Parse sign blocks
    sign_blocks = re.split(r"\nSign\s+(\d+)\s*\n", full_text)
    signs: dict[str, dict] = {}

    for i in range(1, len(sign_blocks) - 1, 2):
        sign_id = sign_blocks[i].strip()
        block = sign_blocks[i + 1]

        tm_match = re.search(
            r"(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", block
        )
        total_occ = terminal = medial = initial = solo = 0
        if tm_match:
            total_occ = int(tm_match.group(3))
            terminal = int(tm_match.group(4))
            medial = int(tm_match.group(5))
            initial = int(tm_match.group(6))
            solo = int(tm_match.group(7))

        icit_match = re.search(r"ICIT ID:\s*([\d,\n\r ]+)", block)
        icit_ids: list[int] = []
        if icit_match:
            raw = icit_match.group(1).replace("\n", " ").strip()
            icit_ids = [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]

        t_rate = terminal / total_occ if total_occ > 0 else 0.0
        i_rate = initial / total_occ if total_occ > 0 else 0.0

        signs[sign_id] = {
            "sign_id": sign_id,
            "total": total_occ,
            "terminal": terminal,
            "medial": medial,
            "initial": initial,
            "solo": solo,
            "terminal_rate": round(t_rate, 4),
            "initial_rate": round(i_rate, 4),
            "icit_ids": icit_ids,
        }

    return signs


# ── Main ──────────────────────────────────────────────────────────────


def main() -> None:
    import pypdf

    # ── 1. Diagnose both PDFs ──────────────────────────────────────────
    print("=" * 60)
    print("DIAGNOSING PDFs")
    print("=" * 60)

    for label, path in [("CORPUS", _CORPUS_PDF), ("CATALOG", _CATALOG_PDF)]:
        if not path.exists():
            print(f"\n{label}: NOT FOUND at {path}")
            continue
        print(f"\n{label}: {path.name} ({path.stat().st_size / 1e6:.1f} MB)")
        diag = diagnose(path, sample_size=12)
        print(f"  Total pages: {diag['total_pages']}")
        for s in diag["samples"][:6]:
            has_codes = "✓ sign codes" if s["has_sign_codes"] else ""
            has_icit = "✓ ICIT/CISI" if s["has_icit_pattern"] else ""
            flags = " ".join(filter(None, [has_codes, has_icit]))
            print(f"  p{s['page']:>4}: {s['n_chars']:>5} chars | {flags}")
            if s["first_3_lines"]:
                print(f"         → {s['first_3_lines'][0][:80]}")

    # ── 2. Parse Corpus PDF ────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PARSING CORPUS PDF")
    print("=" * 60)

    if not _CORPUS_PDF.exists():
        print("ERROR: Corpus PDF not found.")
        sys.exit(1)

    print("\nExtracting sign sequences...")
    sequences, corpus_meta = parse_corpus_pdf(_CORPUS_PDF)
    n_with_seqs = sum(1 for v in sequences.values() if v)
    total_tokens = sum(len(v) for v in sequences.values())
    print(f"  Inscriptions with sign sequences: {n_with_seqs}")
    print(f"  Total sign tokens extracted:      {total_tokens}")
    print(f"  Inscription metadata entries:     {len(corpus_meta)}")

    if n_with_seqs == 0:
        print("\n  ⚠ No sign sequences found in PDF text layer.")
        print("  The sign sequences may be embedded as images.")
        print("  Falling back to TXT-based probabilistic reconstruction.")
        # Load existing TXT extraction
        txt_path = _REPORTS / "icit_extracted_corpus.json"
        if txt_path.exists():
            print(f"  Using existing {txt_path.name}")
        else:
            print("  Run parse_kindle_corpus.py first.")
    else:
        print(f"\n  ✓ Found real sign sequences!")
        # Sample a few
        sample_ids = list(sequences.keys())[:5]
        for sid in sample_ids:
            print(f"  ICIT {sid}: {sequences[sid]}")

    # ── 3. Parse Catalog PDF ───────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PARSING CATALOG PDF")
    print("=" * 60)

    if not _CATALOG_PDF.exists():
        print("ERROR: Catalog PDF not found. Using TXT-based data.")
    else:
        print("\nExtracting sign statistics (may take a minute for large PDF)...")
        signs = parse_catalog_pdf(_CATALOG_PDF)
        total_icit = sum(len(v["icit_ids"]) for v in signs.values())
        print(f"  Signs parsed:           {len(signs)}")
        print(f"  Total ICIT ID entries:  {total_icit}")

        if len(signs) >= 100:
            # Save enhanced catalog
            (_REPORTS / "icit_sign_stats_pdf.json").write_text(
                json.dumps(signs, indent=2), encoding="utf-8"
            )
            print(f"  Saved icit_sign_stats_pdf.json")

    # ── 4. Save whatever we got ────────────────────────────────────────
    print("\n" + "=" * 60)
    print("SAVING RESULTS")
    print("=" * 60)

    _REPORTS.mkdir(exist_ok=True)

    output = {
        "corpus_sequences": {str(k): v for k, v in sequences.items()},
        "corpus_metadata": {str(k): v for k, v in corpus_meta.items()},
        "n_inscriptions_with_sequences": n_with_seqs,
        "total_sign_tokens": total_tokens,
        "has_real_sequences": n_with_seqs > 0,
    }
    (_REPORTS / "icit_pdf_extraction.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8"
    )
    print(f"\nSaved icit_pdf_extraction.json")
    print(f"\n{'Real sequences extracted' if n_with_seqs > 0 else 'No sequences in text layer — PDF uses image-based glyphs'}")
    print("\nDone.")


if __name__ == "__main__":
    main()
