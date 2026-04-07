"""OCR extraction of the real ICIT corpus from Fuls (2023) PDF books.

Uses pymupdf to render pages to images + Tesseract 5 for OCR.

Produces:
  reports/icit_pdf_ocr_corpus.json      -- per-inscription sign sequences
  reports/icit_pdf_ocr_catalog.json     -- per-sign statistics
  reports/icit_pdf_ocr_corpus_flat.txt  -- flat text corpus (one line per inscription)
  reports/icit_pdf_ocr_progress.json    -- checkpoint for resuming interrupted runs

Usage:
  python ocr_icit_corpus.py [--mode corpus|catalog|both] [--dpi 200] [--sample N]

Modes:
  corpus  -- extract sign sequences from Corpus of Indus Inscriptions.pdf
  catalog -- extract sign statistics from A Catalog of Indus Signs.pdf
  both    -- run both (default)

Flags:
  --sample N   -- only process first N content pages (for testing)
  --dpi N      -- render resolution (default 200, higher = slower but more accurate)
  --resume     -- skip pages already in progress checkpoint
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import pymupdf
import pytesseract
from PIL import Image

# ── Paths ──────────────────────────────────────────────────────────────────────

CATALOG_PDF = Path(
    r"C:\Users\trist\OneDrive\Documents\My Kindle Content\A Catalog of Indus Signs.pdf"
)
CORPUS_PDF = Path(
    r"C:\Users\trist\OneDrive\Documents\My Kindle Content\Corpus of Indus Inscriptions.pdf"
)
REPORTS = Path(__file__).parent.parent / "reports"

# Windows Tesseract path
_TESS_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(_TESS_PATH):
    pytesseract.pytesseract.tesseract_cmd = _TESS_PATH


# ── Page rendering ─────────────────────────────────────────────────────────────


def render_page(doc: pymupdf.Document, page_num: int, dpi: int = 200) -> Image.Image:
    """Render a PDF page to a PIL Image."""
    page = doc[page_num]
    mat = pymupdf.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, colorspace=pymupdf.csGRAY)
    return Image.frombytes("L", [pix.width, pix.height], pix.samples)


# ── OCR helpers ────────────────────────────────────────────────────────────────


def ocr_page(img: Image.Image, config: str = "--oem 3 --psm 6") -> str:
    """Run Tesseract OCR on a PIL image, return text."""
    return pytesseract.image_to_string(img, config=config, lang="eng")


def ocr_page_digits(img: Image.Image) -> str:
    """OCR tuned for digit-heavy pages (sign sequences)."""
    # Whitelist: digits, spaces, newlines, hyphens, slashes (for H-123, R/L)
    config = (
        r"--oem 3 --psm 6 "
        r"-c tessedit_char_whitelist='0123456789 /-\nABCDEFGHIJKLMNOPQRSTUVWXYZ:.,()?'"
    )
    return pytesseract.image_to_string(img, config=config, lang="eng")


# ── Corpus PDF parsing ─────────────────────────────────────────────────────────


# Inscription header — handles both plain TXT and OCR table format with | separators
# Plain:  "750 H-2101 R/L None"
# OCR:    "750 | H-2101 R/L None EK"
_INSC_RE = re.compile(r"^(\d{1,5})\s*\|?\s*([\w\-]+)\s+(R/L|L/R|NR|-)", re.IGNORECASE)
# Sign sequence: 2+ runs of 3-digit codes (unlikely in PDF OCR, keep as fallback)
_SEQ_RE = re.compile(r"^\s*((?:\d{3}\s+){1,}\d{3})\s*$")
# Site heading: "3.26. HARAPPA" or "3.45. MOHENJO-DARO"
_SITE_RE = re.compile(r"^\d+\.\d+\.\s+([A-Z][A-Z\s\-]+?)(?:\s+\d+)?\s*$")
# Type line
_TYPE_RE = re.compile(r"^(SEAL:\w+|TAB:\w+|POT:\w+|MISC)", re.IGNORECASE)


def _clean_ocr_line(line: str) -> str:
    """Strip OCR artefacts: leading/trailing pipes, double spaces."""
    return re.sub(r"\s+", " ", line.replace("|", " ")).strip()


def parse_corpus_page(text: str, state: dict) -> None:
    """Update shared state from OCR'd page text (in-place)."""
    lines = text.splitlines()
    for line in lines:
        line_s = _clean_ocr_line(line)
        if not line_s:
            continue

        # Site heading: "3.26. HARAPPA 123" (page number at end)
        m = _SITE_RE.match(line_s)
        if m and len(line_s) < 70:
            candidate = m.group(1).strip().title()
            skip = {"Chapter", "Inscriptions", "Contents", "Table", "Appendix", "Index"}
            if candidate not in skip and len(candidate) > 2:
                state["site"] = candidate
            continue

        # Inscription header: "750 H-2101 R/L ..."
        m = _INSC_RE.match(line_s)
        if m:
            try:
                icit_id = int(m.group(1))
            except ValueError:
                continue
            cisi = m.group(2)
            direction = m.group(3).upper()
            # Keep earliest occurrence (sometimes duplicated across pages)
            if icit_id not in state["metadata"]:
                state["metadata"][icit_id] = {
                    "icit_id": icit_id,
                    "cisi": cisi,
                    "direction": direction,
                    "site": state["site"],
                    "type": "",
                    "complete": "",
                    "n_positions": 1,
                }
            else:
                # Count additional sign positions for this inscription
                state["metadata"][icit_id]["n_positions"] = (
                    state["metadata"][icit_id].get("n_positions", 1) + 1
                )
            state["current_id"] = icit_id
            continue

        # Type line: "TAB:I Y None"
        m = _TYPE_RE.match(line_s)
        if m and state["current_id"]:
            cid = state["current_id"]
            if cid in state["metadata"] and not state["metadata"][cid]["type"]:
                state["metadata"][cid]["type"] = m.group(1).upper()
                # Completeness is the next token
                parts = line_s.split()
                if len(parts) >= 2 and parts[1] in ("Y", "N", "?"):
                    state["metadata"][cid]["complete"] = parts[1]
            continue

        # Sign sequence (fallback — unlikely in PDF OCR but handle anyway)
        m = _SEQ_RE.match(line_s)
        if m and state["current_id"]:
            codes = m.group(1).split()
            valid = all(c.isdigit() and len(c) == 3 for c in codes)
            if valid and len(codes) >= 2:
                cid = state["current_id"]
                state["sequences"].setdefault(cid, []).extend(codes)


# ── Catalog PDF parsing ────────────────────────────────────────────────────────


# Sign header: "Sign 209" standalone OR with leading OCR noise ("Q Sign 220", "8 Sign 215")
_SIGN_HDR = re.compile(r"(?:^|\S+\s+)Sign\s+(\d{1,4})\s*$", re.IGNORECASE)
# ICIT ID line start
_ICIT_START = re.compile(r"ICIT\s+ID:\s*([\d,\s]+)", re.IGNORECASE)
# ICIT continuation: a line that looks like pure numbers/commas (no letters)
_ICIT_CONT = re.compile(r"^[\d,\s\.]+$")


def parse_catalog_page(text: str, state: dict) -> None:
    """
    Update catalog state from OCR'd page text.

    Strategy:
    - Match 'Sign NNN' headers (with optional leading OCR noise)
    - Collect ICIT IDs including multi-line continuations
    - Skip sign stats (too noisy from table OCR; use TXT-based stats as fallback)
    """
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # ── ICIT ID start — may span multiple lines ────────────────────────────
        if state.get("collecting_icit") and state["current_sign"]:
            # Check if this line is a continuation (pure digits/commas)
            if _ICIT_CONT.match(line) and re.search(r"\d", line):
                raw = re.sub(r"[^\d,]", " ", line)
                ids = [int(x) for x in re.split(r"[,\s]+", raw) if x.strip().isdigit()]
                existing = state["signs"][state["current_sign"]]["icit_ids"]
                for id_ in ids:
                    if id_ not in existing:
                        existing.append(id_)
                i += 1
                continue
            else:
                state["collecting_icit"] = False

        # ── Sign header ────────────────────────────────────────────────────────
        m = _SIGN_HDR.search(line)
        if m:
            sign_id = m.group(1).strip()
            state["current_sign"] = sign_id
            if sign_id not in state["signs"]:
                state["signs"][sign_id] = {
                    "sign_id": sign_id,
                    "icit_ids": [],
                }
            state["collecting_icit"] = False
            i += 1
            continue

        # ── ICIT ID start ──────────────────────────────────────────────────────
        im = _ICIT_START.search(line)
        if im and state["current_sign"] and state["current_sign"] in state["signs"]:
            raw = re.sub(r"[^\d,]", " ", im.group(1))
            ids = [int(x) for x in re.split(r"[,\s]+", raw) if x.strip().isdigit()]
            existing = state["signs"][state["current_sign"]]["icit_ids"]
            for id_ in ids:
                if id_ not in existing:
                    existing.append(id_)
            state["collecting_icit"] = True
            i += 1
            continue

        i += 1


# ── Progress checkpoint ────────────────────────────────────────────────────────


def load_progress(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"corpus_pages_done": [], "catalog_pages_done": []}


def save_progress(path: Path, prog: dict) -> None:
    path.write_text(json.dumps(prog, indent=2), encoding="utf-8")


# ── Sequence reconstruction (same logic as parse_kindle_corpus.py) ──────────────


def reconstruct_sequences_from_catalog(
    catalog: dict[str, dict],
    corpus_meta: dict[int, dict],
) -> list[dict]:
    """
    Rebuild ordered inscription sequences from the catalog ICIT→sign mapping.
    Sign ordering is probabilistic (initial_rate first, terminal_rate last).
    Same algorithm as parse_kindle_corpus.py:reconstruct_sequences().
    """
    from collections import defaultdict

    # Invert: icit_id → [sign_ids]
    icit_to_signs: dict[int, list[str]] = defaultdict(list)
    for sign_id, data in catalog.items():
        for icit_id in data.get("icit_ids", []):
            icit_to_signs[icit_id].append(sign_id)

    all_icit = set(icit_to_signs.keys()) | set(corpus_meta.keys())
    inscriptions = []

    for icit_id in sorted(all_icit):
        # deduplicate, preserve order
        sign_set = list(dict.fromkeys(icit_to_signs.get(icit_id, [])))
        meta = corpus_meta.get(
            icit_id,
            {
                "site": "Unknown", "type": "", "complete": "",
                "direction": "", "cisi": "", "n_positions": 0,
            },
        )
        if not sign_set:
            continue

        if len(sign_set) == 1:
            ordered = sign_set
        else:
            sorted_initial = sorted(
                sign_set,
                key=lambda s: catalog.get(s, {}).get("initial_rate", 0),
                reverse=True,
            )
            sorted_terminal = sorted(
                sign_set,
                key=lambda s: catalog.get(s, {}).get("terminal_rate", 0),
            )
            if len(sign_set) == 2:
                ordered = sorted_initial
            else:
                first = sorted_initial[0]
                last = sorted_terminal[-1]
                middle = [s for s in sign_set if s != first and s != last]
                middle.sort(
                    key=lambda s: (
                        catalog.get(s, {}).get("terminal_rate", 0)
                        + catalog.get(s, {}).get("initial_rate", 0)
                    )
                )
                ordered = [first] + middle + [last]

        inscriptions.append({
            "icit_id": icit_id,
            "sequence": ordered,
            "length": len(ordered),
            "site": meta.get("site", "Unknown"),
            "type": meta.get("type", ""),
            "complete": meta.get("complete", ""),
            "direction": meta.get("direction", ""),
            "cisi": meta.get("cisi", ""),
        })

    return inscriptions


# ── Main OCR loops ─────────────────────────────────────────────────────────────


def run_corpus_ocr(
    pdf: Path,
    dpi: int,
    sample: int | None,
    resume_pages: set[int],
) -> tuple[dict[int, list[str]], dict[int, dict]]:
    """OCR the Corpus PDF and return (sequences, metadata)."""
    doc = pymupdf.open(str(pdf))
    total = len(doc)
    pages_to_do = list(range(total))
    if sample:
        pages_to_do = pages_to_do[:sample]

    state: dict[str, Any] = {
        "site": "Unknown",
        "current_id": None,
        "sequences": {},
        "metadata": {},
    }

    n_done = 0
    t0 = time.time()
    for p in pages_to_do:
        if p in resume_pages:
            n_done += 1
            continue
        try:
            img = render_page(doc, p, dpi)
            text = ocr_page(img)
            parse_corpus_page(text, state)
        except Exception as e:
            print(f"    [WARN] p{p}: {e}", file=sys.stderr)
        n_done += 1
        if n_done % 20 == 0:
            elapsed = time.time() - t0
            rate = n_done / max(elapsed, 1)
            remaining = (len(pages_to_do) - n_done) / max(rate, 0.001)
            n_seq = sum(1 for v in state["sequences"].values() if v)
            eta = remaining / 60
            print(f"  Corpus p{p}/{total} | seqs:{n_seq} | {rate:.1f} pg/s | ETA {eta:.0f}m")

    doc.close()
    return state["sequences"], state["metadata"]


def run_catalog_ocr(
    pdf: Path,
    dpi: int,
    sample: int | None,
    resume_pages: set[int],
    start_page: int = 0,
) -> dict[str, dict]:
    """OCR the Catalog PDF and return sign stats dict."""
    doc = pymupdf.open(str(pdf))
    total = len(doc)
    pages_to_do = list(range(start_page, total))
    if sample:
        pages_to_do = pages_to_do[:sample]

    state: dict[str, Any] = {
        "current_sign": None,
        "sign_buffer": "",
        "signs": {},
        "collecting_icit": False,
    }

    n_done = 0
    t0 = time.time()
    for p in pages_to_do:
        if p in resume_pages:
            n_done += 1
            continue
        try:
            img = render_page(doc, p, dpi)
            text = ocr_page(img)
            parse_catalog_page(text, state)
        except Exception as e:
            print(f"    [WARN] p{p}: {e}", file=sys.stderr)
        n_done += 1
        if n_done % 20 == 0:
            elapsed = time.time() - t0
            rate = n_done / max(elapsed, 1)
            remaining = (len(pages_to_do) - n_done) / max(rate, 0.001)
            n_signs = len(state["signs"])
            eta = remaining / 60
            print(f"  Catalog p{p}/{total} | signs:{n_signs} | {rate:.1f} pg/s | ETA {eta:.0f}m")

    doc.close()
    return state["signs"]


# ── Sample mode (quick test) ──────────────────────────────────────────────────


def run_sample(dpi: int, n: int = 20) -> None:
    """OCR a small sample and show raw text to validate quality."""
    for label, pdf in [("CORPUS", CORPUS_PDF), ("CATALOG", CATALOG_PDF)]:
        if not pdf.exists():
            print(f"{label}: NOT FOUND")
            continue
        doc = pymupdf.open(str(pdf))
        total = len(doc)
        # Pick pages spread across the document body (skip first/last 5%)
        start = max(1, int(total * 0.05))
        end = min(total - 1, int(total * 0.95))
        step = max(1, (end - start) // n)
        samples = list(range(start, end, step))[:n]

        print(f"\n{'='*60}")
        print(f"  {label}: {pdf.name} — {total} pages")
        print(f"  Sampling {len(samples)} pages at {dpi} DPI")
        print("=" * 60)

        found_seqs = 0
        found_icit = 0
        for p in samples[:5]:  # show only first 5 in full
            img = render_page(doc, p, dpi)
            text = ocr_page(img)
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            has_seq = bool(_SEQ_RE.search(text))
            has_icit = bool(_INSC_RE.search(text)) or bool(re.search(r"ICIT|Sign \d+", text))
            if has_seq:
                found_seqs += 1
            if has_icit:
                found_icit += 1
            print(f"\n  --- Page {p} {'[SEQS]' if has_seq else ''} {'[ICIT]' if has_icit else ''}")
            for ln in lines[:8]:
                print(f"    {ln[:100]}")

        # Quick count pass on remaining samples
        for p in samples[5:]:
            img = render_page(doc, p, dpi)
            text = ocr_page(img)
            if _SEQ_RE.search(text):
                found_seqs += 1
            if _INSC_RE.search(text) or re.search(r"ICIT|Sign \d+", text):
                found_icit += 1

        print(f"\n  Pages with sign sequences: {found_seqs}/{len(samples)}")
        print(f"  Pages with ICIT/Sign data: {found_icit}/{len(samples)}")
        doc.close()


# ── Entry point ────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR ICIT PDFs with Tesseract")
    parser.add_argument("--mode", choices=["corpus", "catalog", "both", "sample"], default="both")
    parser.add_argument("--dpi", type=int, default=200, help="Render DPI (default 200)")
    parser.add_argument("--sample", type=int, default=None, help="Only process first N pages")
    parser.add_argument("--resume", action="store_true", help="Skip already-processed pages")
    args = parser.parse_args()

    REPORTS.mkdir(exist_ok=True)
    progress_path = REPORTS / "icit_pdf_ocr_progress.json"
    progress = load_progress(progress_path)

    if args.mode == "sample":
        run_sample(dpi=args.dpi, n=args.sample or 20)
        return

    corpus_meta: dict[int, dict] = {}
    signs: dict[str, dict] = {}

    # ── Corpus (metadata) ──────────────────────────────────────────────────────
    if args.mode in ("corpus", "both"):
        if not CORPUS_PDF.exists():
            print(f"ERROR: Corpus PDF not found at {CORPUS_PDF}")
            if args.mode == "corpus":
                sys.exit(1)
        else:
            resume_set = set(progress.get("corpus_pages_done", [])) if args.resume else set()
            doc_tmp = pymupdf.open(str(CORPUS_PDF))
            n_pages = len(doc_tmp)
            doc_tmp.close()
            print(f"\nOCR: Corpus of Indus Inscriptions ({CORPUS_PDF.stat().st_size/1e6:.0f} MB)")
            mode_str = 'Resuming' if resume_set else 'Fresh run'
            print(f"     {n_pages} pages | DPI={args.dpi} | {mode_str}")
            t0 = time.time()
            _sequences, corpus_meta = run_corpus_ocr(CORPUS_PDF, args.dpi, args.sample, resume_set)
            elapsed = time.time() - t0
            print(f"\n  ✓ Corpus metadata OCR complete in {elapsed/60:.1f}m")
            print(f"    Inscription metadata entries: {len(corpus_meta)}")
            # Save raw corpus metadata
            (REPORTS / "icit_pdf_ocr_corpus_meta.json").write_text(
                json.dumps({str(k): v for k, v in corpus_meta.items()}, indent=2), encoding="utf-8"
            )

    # ── Catalog (sign stats + ICIT IDs) ────────────────────────────────────────
    if args.mode in ("catalog", "both"):
        if not CATALOG_PDF.exists():
            print(f"ERROR: Catalog PDF not found at {CATALOG_PDF}")
            if args.mode == "catalog":
                sys.exit(1)
        else:
            resume_set = set(progress.get("catalog_pages_done", [])) if args.resume else set()
            # Chapter 5 (statistical data) starts ~page 200; skip front matter for sample mode
            cat_start = 200 if args.sample else 0
            print(f"\nOCR: A Catalog of Indus Signs ({CATALOG_PDF.stat().st_size/1e6:.0f} MB)")
            t0 = time.time()
            signs = run_catalog_ocr(
                CATALOG_PDF, args.dpi, args.sample, resume_set, start_page=cat_start
            )
            elapsed = time.time() - t0

            total_icit = sum(len(v["icit_ids"]) for v in signs.values())
            print(f"\n  ✓ Catalog OCR complete in {elapsed/60:.1f}m")
            print(f"    Signs parsed:          {len(signs)}")
            print(f"    Total ICIT ID entries: {total_icit}")
            (REPORTS / "icit_pdf_ocr_catalog.json").write_text(
                json.dumps(signs, indent=2), encoding="utf-8"
            )
            print("    Saved icit_pdf_ocr_catalog.json")

    # ── Reconstruct combined corpus ─────────────────────────────────────────────
    if args.mode == "both" and signs and corpus_meta:
        print("\nReconstructing inscription sequences from catalog + corpus metadata...")
        inscriptions = reconstruct_sequences_from_catalog(signs, corpus_meta)
        lengths = [i["length"] for i in inscriptions]
        total_tokens = sum(lengths)
        print(f"  Inscriptions: {len(inscriptions)}")
        print(f"  Sign tokens:  {total_tokens}")
        print(f"  Mean length:  {sum(lengths)/max(len(lengths),1):.2f}")

        summary = {
            "n_inscriptions": len(inscriptions),
            "total_sign_tokens": total_tokens,
            "n_signs": len(signs),
            "mean_inscription_length": round(total_tokens / max(len(inscriptions), 1), 2),
            "max_inscription_length": max(lengths) if lengths else 0,
            "source": "PDF OCR (Tesseract 5, pymupdf render)",
            "dpi": args.dpi,
            "method": (
                "Sign sequences reconstructed from Catalog ICIT_ID lists (OCR). "
                "Ordering is probabilistic (initial_rate -> first, terminal_rate -> last). "
                "True ordering requires computer-vision-based sign image recognition."
            ),
        }
        full_out = {"summary": summary, "inscriptions": inscriptions}
        (REPORTS / "icit_extracted_corpus.json").write_text(
            json.dumps(full_out, indent=2), encoding="utf-8"
        )
        flat_lines = [" ".join(i["sequence"]) for i in inscriptions if i["sequence"]]
        (REPORTS / "icit_corpus_flat.txt").write_text("\n".join(flat_lines), encoding="utf-8")
        (REPORTS / "icit_corpus_summary.json").write_text(
            json.dumps(summary, indent=2), encoding="utf-8"
        )
        print("  Saved icit_extracted_corpus.json + icit_corpus_flat.txt (overwriting TXT-based)")

    print("\nDone.")


if __name__ == "__main__":
    main()
