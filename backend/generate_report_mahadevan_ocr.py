"""Generate a PDF report summarising the Mahadevan (1977) OCR results.

Covers:
  1. Scope: pages OCR'd, inscriptions catalogued
  2. Bigram data: sign pair frequencies extracted from table pages
  3. Corpus statistics from the mapped bigram data
  4. Sign frequency analysis
  5. Next steps (glyph-to-M77 mapping required for full sequences)

Run with: shell.cmd python backend/generate_report_mahadevan_ocr.py
Output:   reports/mahadevan_ocr_report.pdf
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

NAVY  = HexColor("#1e3a5f")
BLUE  = HexColor("#2563eb")
GREEN = HexColor("#15803d")
RED   = HexColor("#dc2626")
GOLD  = HexColor("#ca8a04")
LGREY = HexColor("#f1f5f9")
MGREY = HexColor("#e2e8f0")

REPO  = Path(__file__).resolve().parent.parent
OCR_DIR = REPO / "data-import" / "mahadevan_ocr"
REPORTS = REPO / "reports"

# ── Load data ─────────────────────────────────────────────────────────

def load_bigrams() -> dict:
    """Load mapped bigram data (Fuls sign codes + M77 where known)."""
    # Prefer the mapped version which has Fuls sign codes
    for fname in ("mahadevan_bigrams_mapped.json", "mahadevan_bigrams.json"):
        p = REPORTS / fname
        if not p.exists() or p.stat().st_size < 100:
            continue
        raw = json.loads(p.read_text(encoding="utf-8"))
        entries = raw if isinstance(raw, list) else raw.get("pairs", [])
        pairs: dict[str, int] = {}
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            freq = int(entry.get("freq", entry.get("frequency", 1)))
            # Use Fuls codes if available, fall back to raw
            a = entry.get("sign_a_fuls") or entry.get("sign_a", "?")
            b = entry.get("sign_b_fuls") or entry.get("sign_b", "?")
            key = f"{a}+{b}"
            pairs[key] = pairs.get(key, 0) + freq
        if pairs:
            return {"bigrams": pairs, "source": fname}
    return {"bigrams": {}}

def load_mapped_bigrams() -> dict:
    p = REPORTS / "mahadevan_bigrams_mapped.json"
    if p.exists() and p.stat().st_size > 100:
        return json.loads(p.read_text(encoding="utf-8"))
    return {}

def count_ocr_pages() -> tuple[int, int]:
    """Return (text_pages, table_pages) processed."""
    text_pages  = len(list(OCR_DIR.glob("ocr_texts_*.txt")))
    table_pages = len(list(OCR_DIR.glob("ocr_freqs_*.txt")))
    return text_pages, table_pages

def parse_inscription_catalog() -> list[dict]:
    """Extract inscription numbers and site codes from OCR text files."""
    import re
    entries = []
    for txt_file in sorted(OCR_DIR.glob("ocr_texts_*.txt")):
        text = txt_file.read_text(encoding="utf-8", errors="replace")
        # Look for rows like: | 1001 | 103511 | ... |
        for m in re.finditer(r"\|\s*(\d{4,5})\s*\|\s*(\d+)\s*\|", text):
            insc_id = int(m.group(1))
            site_code = m.group(2)
            entries.append({"id": insc_id, "site_code": site_code})
    # Deduplicate by id
    seen = set()
    unique = []
    for e in entries:
        if e["id"] not in seen:
            seen.add(e["id"])
            unique.append(e)
    return sorted(unique, key=lambda x: x["id"])

def site_from_code(code: str) -> str:
    """Best-effort site name from Mahadevan site prefix codes."""
    prefixes = {
        "10": "Mohenjo-daro",
        "11": "Harappa",
        "12": "Chanhu-daro",
        "13": "Lothal",
        "14": "Kalibangan",
        "15": "Banawali",
        "16": "Dholavira",
        "17": "Other sites",
    }
    return prefixes.get(code[:2], "Unknown site")

# ── Styles ────────────────────────────────────────────────────────────

styles = getSampleStyleSheet()
H1     = ParagraphStyle("H1",   parent=styles["Heading1"], textColor=NAVY, fontSize=18, spaceAfter=6)
H2     = ParagraphStyle("H2",   parent=styles["Heading2"], textColor=NAVY, fontSize=13, spaceAfter=4)
H3     = ParagraphStyle("H3",   parent=styles["Heading3"], textColor=BLUE, fontSize=11, spaceAfter=3)
BODY   = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=8, alignment=TA_JUSTIFY)
CAPTION= ParagraphStyle("Cap",  parent=styles["Normal"], fontSize=9, textColor=HexColor("#64748b"), alignment=TA_CENTER, spaceAfter=12)
TITLE  = ParagraphStyle("Title",parent=styles["Title"], textColor=NAVY, fontSize=22, alignment=TA_CENTER, spaceAfter=4)
SUB    = ParagraphStyle("Sub",  parent=styles["Normal"], textColor=HexColor("#475569"), fontSize=11, alignment=TA_CENTER, spaceAfter=20)

ts = TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR",     (0, 0), (-1, 0), white),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, 0), 9),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
    ("TOPPADDING",    (0, 0), (-1, 0), 6),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [white, LGREY]),
    ("FONTSIZE",      (0, 1), (-1, -1), 9),
    ("GRID",          (0, 0), (-1, -1), 0.5, MGREY),
    ("TOPPADDING",    (0, 1), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
])

# ── Main ──────────────────────────────────────────────────────────────

def main() -> None:
    print("[1/4] Loading data...")
    bigrams        = load_bigrams()
    mapped         = load_mapped_bigrams()
    text_p, tbl_p  = count_ocr_pages()
    catalog        = parse_inscription_catalog()

    print(f"      Inscription pages OCR'd: {text_p}")
    print(f"      Table pages OCR'd:       {tbl_p}")
    print(f"      Inscriptions catalogued: {len(catalog)}")

    # Bigram statistics
    bigram_pairs: dict[str, int] = {}
    total_bigram_tokens = 0
    if isinstance(bigrams, dict) and "bigrams" in bigrams:
        for pair, freq in bigrams["bigrams"].items():
            bigram_pairs[pair] = freq
            total_bigram_tokens += freq
    elif isinstance(bigrams, dict):
        for k, v in bigrams.items():
            if isinstance(v, int):
                bigram_pairs[k] = v
                total_bigram_tokens += v

    top_bigrams = sorted(bigram_pairs.items(), key=lambda x: -x[1])[:15]
    sign_freq: Counter = Counter()
    for pair, freq in bigram_pairs.items():
        parts = pair.replace("-", " ").replace("+", " ").split()
        for p in parts:
            if p.isdigit():
                sign_freq[p] += freq

    print(f"      Bigram pairs extracted:  {len(bigram_pairs)}")
    print(f"      Total bigram tokens:     {total_bigram_tokens}")

    # Site breakdown
    site_counts: Counter = Counter()
    for e in catalog:
        site_counts[site_from_code(e["site_code"])] += 1

    print("[2/4] Building PDF...")
    REPORTS.mkdir(exist_ok=True)
    output = str(REPORTS / "mahadevan_ocr_report.pdf")
    doc = SimpleDocTemplate(
        output, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
    )

    s = []

    # Title
    s.append(Paragraph("Mahadevan (1977) Corpus OCR Report", TITLE))
    s.append(Paragraph(
        "Indus Script — Sign Sequences and Bigram Analysis · Glossa Lab", SUB,
    ))
    s.append(Paragraph(
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        CAPTION,
    ))
    s.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=16))

    # 1. Scope
    s.append(Paragraph("1. OCR Scope", H2))
    s.append(Paragraph(
        "Glossa Lab applied Mistral's mistral-ocr-latest model to Mahadevan (1977) "
        "<i>The Indus Script: Texts, Concordance and Tables</i>, targeting two sections:",
        BODY,
    ))
    scope = [
        ["Section", "Pages", "Status", "Result"],
        ["Inscription texts (§2: plates)", "39–162", f"{text_p} pages done",
         f"{len(catalog)} inscription IDs found"],
        ["Bigram frequency tables (§5)", "717–745", f"{tbl_p} pages done",
         f"{len(bigram_pairs):,} sign-pair frequencies extracted"],
    ]
    s.append(Table(scope, colWidths=[5.5*cm, 3*cm, 3.5*cm, 5*cm], style=ts))
    s.append(Spacer(1, 8))
    s.append(Paragraph(
        "<b>Note on inscription text pages:</b> Mahadevan's inscription plates show the Indus "
        "signs as typeset glyphs from a custom font, not as numeric codes. The OCR engine "
        "correctly transcribed the inscription catalog metadata (ID numbers, site codes) but "
        "could not convert the graphical sign glyphs to M77 numeric codes. Obtaining the "
        "full ordered sign sequences requires either (a) a glyph-font-to-M77 mapping "
        "applied to the OCR output, or (b) direct access to the ICIT database from "
        "Dr. Andreas Fuls (TU Berlin).",
        BODY,
    ))

    # 2. Inscription catalog
    s.append(Paragraph("2. Inscription Catalog", H2))
    s.append(Paragraph(
        f"The OCR successfully identified <b>{len(catalog)}</b> unique inscription entries "
        f"from {text_p} pages covering Mahadevan's reference numbers. "
        f"Range: M{catalog[0]['id'] if catalog else '—'} to M{catalog[-1]['id'] if catalog else '—'}.",
        BODY,
    ))
    if site_counts:
        site_data = [["Site", "Inscriptions", "% of total"]]
        total_sites = sum(site_counts.values())
        for site, cnt in site_counts.most_common(8):
            site_data.append([site, str(cnt), f"{100*cnt/total_sites:.1f}%"])
        s.append(Table(site_data, colWidths=[7*cm, 4*cm, 4*cm], style=ts))
        s.append(Paragraph("Table 1. Inscription distribution by site.", CAPTION))

    # 3. Bigram analysis
    s.append(Paragraph("3. Sign-Pair Bigram Frequencies", H2))
    s.append(Paragraph(
        f"The bigram frequency tables (Mahadevan §5, pages 717–745) were successfully "
        f"OCR'd and parsed. These tables record every pair of adjacent signs across the "
        f"full M77 corpus of 2,906 inscriptions.",
        BODY,
    ))
    bigram_stats = [
        ["Metric", "Value"],
        ["Sign-pair types (bigrams)", f"{len(bigram_pairs):,}"],
        ["Total bigram occurrences", f"{total_bigram_tokens:,}"],
        ["Unique signs in bigrams", f"{len(sign_freq):,}"],
        ["Most frequent pair", top_bigrams[0][0] if top_bigrams else "—"],
        ["Most frequent pair frequency", str(top_bigrams[0][1]) if top_bigrams else "—"],
    ]
    s.append(Table(bigram_stats, colWidths=[8*cm, 8*cm], style=ts))
    s.append(Spacer(1, 8))

    if top_bigrams:
        s.append(Paragraph("Top 15 Most Frequent Sign Pairs", H3))
        bp_data = [["Rank", "Sign Pair", "Frequency", "Significance"]]
        for i, (pair, freq) in enumerate(top_bigrams, 1):
            sig = "Very high — likely core grammatical sequence" if freq > 200 else ""
            bp_data.append([str(i), pair, str(freq), sig])
        s.append(Table(bp_data, colWidths=[1.5*cm, 4*cm, 3*cm, 7.5*cm], style=ts))
        s.append(Paragraph("Table 2. Top bigrams by frequency.", CAPTION))

    if sign_freq:
        s.append(Paragraph("Top 15 Signs by Bigram Appearance", H3))
        sf_data = [["Sign (M77)", "Bigram appearances", "Notes"]]
        for sign, cnt in sign_freq.most_common(15):
            note = "Most common sign in corpus (sign 342)" if sign == "342" else ""
            sf_data.append([sign, str(cnt), note])
        s.append(Table(sf_data, colWidths=[4*cm, 5*cm, 7*cm], style=ts))
        s.append(Paragraph("Table 3. Signs ranked by total bigram frequency.", CAPTION))

    # 4. Next steps
    s.append(Paragraph("4. Next Steps", H2))
    s.append(Paragraph(
        "The following steps are required to complete the M77 corpus analysis:",
        BODY,
    ))
    steps = [
        ["Priority", "Step", "Unlocks"],
        ["1 (immediate)", "Apply glyph-to-M77 font mapping to OCR text output",
         "Full ordered sign sequences for all 2,906 inscriptions"],
        ["2", "Request ICIT database from Dr. Andreas Fuls (TU Berlin)",
         "Ground-truth sequences, site metadata, NWSP validation"],
        ["3", "Run NWSP on real ordered sequences",
         "Validated TMK classification replacing aggregate estimates"],
        ["4", "Run Ventris grid on real sequences",
         "CV-clustering without phoneme assumptions on actual data"],
        ["5", "Bigram Markov model on real corpus",
         "Rao (2009) replication on actual M77 sequences"],
    ]
    s.append(Table(steps, colWidths=[3*cm, 7*cm, 6*cm], style=ts))

    print("[3/4] Writing PDF...")
    doc.build(s)
    print(f"[4/4] Done → {output}")


if __name__ == "__main__":
    main()
