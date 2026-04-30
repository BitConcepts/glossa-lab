"""Mistral Pixtral OCR pipeline for CISI Vol 3 Part 3 plates.

Uses Mistral's `mistral-ocr-latest` vision model to extract Parpola sign 
sequences from the scanned pages of the Indo-Iranian Borderlands corpus:
  - cisi_vol3_part3_2022_desset.pdf

Target:
  - Pages 137-523 containing the site catalogues (Shahdad to Shortughai).
  - We look for seal IDs (e.g., 'Shd-1', 'Failaka_seal') and their 
    associated sign sequences (Parpola P-numbers, or visual descriptions 
    if Parpola IDs are missing).

Usage:
  # Set API key as environment variable first:
  $env:MISTRAL_API_KEY = "your-key-here"

  python scripts/phase28/ocr_cisi_vol3.py --page 140     # Test single page
  python scripts/phase28/ocr_cisi_vol3.py --all          # OCR all catalog pages
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import fitz  # PyMuPDF

_BASE = Path(__file__).resolve().parents[2]
if str(_BASE / "backend") not in sys.path:
    sys.path.insert(0, str(_BASE / "backend"))

from glossa_lab.ai_pacing import AIModelPacer, ModelLimit

_PDF_PATH = _BASE / "corpora" / "downloads" / "contact_zone" / "publications" / "cisi_vol3_part3_2022_desset.pdf"
_OUTDIR = _BASE / "data-import" / "cisi_vol3_ocr"
_OUTDIR.mkdir(parents=True, exist_ok=True)
_OUTPUT_JSON = _BASE / "reports" / "cisi_vol3_extracted_signs.json"

MODEL_NAME = os.environ.get("MISTRAL_OCR_MODEL", "pixtral-12b-2409")
_OCR_RPM = int(os.environ.get("MISTRAL_OCR_RPM", "3"))
_OCR_DELAY = float(os.environ.get("MISTRAL_OCR_DELAY", "25"))

# The PDF on disk is only 40 pages (introduction/front-matter of CISI Vol 3 Part 3).
# We OCR all 40 pages to extract any sign references that may be present in the
# discussion sections or summary tables.
PAGE_START = 0
PAGE_END = 40


def get_model_pacer() -> AIModelPacer:
    return AIModelPacer({
        MODEL_NAME: ModelLimit(
            rpm_limit=_OCR_RPM,
            tpm_limit=int(os.environ.get("MISTRAL_OCR_TPM", "50000")),
            utilization_target=0.80,
            max_concurrency=1,
            image_token_estimate=2048,
        )
    })


PROMPT_CISI_SEALS = """This is a page from the 'Corpus of Indus Seals and Inscriptions, Vol 3, Part 3' (Desset ed. 2022) -- introduction/front-matter section.

YOUR TASK: Extract any of the following data present on this page.

1. SEAL CATALOGUE ENTRIES: Look for seal IDs (e.g. Shd-1, Bam-2, Alt-14, Sh-5, M-410, H-9) with associated sign sequences or Parpola sign numbers (e.g. P145, P047).

2. SIGN-LIST REFERENCES: Lists or tables that describe specific signs, their iconic meaning, or their phonetic readings (e.g. 'sign 47 = fish', 'M-410 has fish-in-crocodile-mouth iconography').

3. PARPOLA NUMBER REFERENCES: Any sentences mentioning specific Parpola or Mahadevan sign IDs (P145, M77 047, etc).

4. ICONOGRAPHIC REFERENCES: Any sentences linking specific seals to iconographic motifs (fish, fig tree, intersecting circles, squirrel, etc).

Output format:
For seal entries: 'SEAL: [id] | SIGNS: [P-numbers OR description]'
For sign references: 'SIGN_REF: [sign id] | MEANING: [iconic/phonetic info]'
For iconographic references: 'ICONOGRAPHY: [seal id] | MOTIF: [description]'
If nothing relevant on this page: 'NONE'

Return ONLY structured data. No headers, no preamble."""


def get_client():
    from mistralai import Mistral
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("ERROR: MISTRAL_API_KEY environment variable not set.")
        sys.exit(1)
    return Mistral(api_key=api_key)


def pdf_page_to_base64(pdf_doc: fitz.Document, page_num: int) -> str:
    """Render a PDF page to a PNG image and return as a base64 data URI."""
    page = pdf_doc.load_page(page_num)
    # 2x zoom for better OCR resolution
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    png_data = pix.tobytes("png")
    b64 = base64.b64encode(png_data).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def run_ocr_on_page(client, pdf_doc: fitz.Document, pacer: AIModelPacer, page_num: int) -> list[dict]:
    b64_image = pdf_page_to_base64(pdf_doc, page_num)
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT_CISI_SEALS},
                {"type": "image_url", "image_url": {"url": b64_image}},
            ],
        }
    ]

    pacer.acquire(MODEL_NAME, reserved_tokens=2048)
    print(f"  [API] Sending Page {page_num+1} to {MODEL_NAME}...")
    
    t0 = time.time()
    try:
        response = client.chat.complete(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.1,
        )
        content = response.choices[0].message.content
        elapsed = time.time() - t0
        print(f"  [API] Success in {elapsed:.1f}s.")
        
        # Parse output - flexible to handle SEAL/SIGN_REF/ICONOGRAPHY lines
        results = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.upper() == "NONE":
                continue
            entry: dict = {"page": page_num + 1, "raw": line}
            if line.startswith("SEAL:") and "SIGNS:" in line:
                parts = line.split("|")
                seal_part = parts[0].replace("SEAL:", "").strip()
                signs_part = parts[1].replace("SIGNS:", "").strip() if len(parts) > 1 else ""
                entry.update({"type": "seal", "seal_id": seal_part, "signs": signs_part})
                results.append(entry)
            elif line.startswith("SIGN_REF:"):
                parts = line.split("|")
                sid = parts[0].replace("SIGN_REF:", "").strip()
                meaning = parts[1].replace("MEANING:", "").strip() if len(parts) > 1 else ""
                entry.update({"type": "sign_ref", "sign_id": sid, "meaning": meaning})
                results.append(entry)
            elif line.startswith("ICONOGRAPHY:"):
                parts = line.split("|")
                seal_id = parts[0].replace("ICONOGRAPHY:", "").strip()
                motif = parts[1].replace("MOTIF:", "").strip() if len(parts) > 1 else ""
                entry.update({"type": "iconography", "seal_id": seal_id, "motif": motif})
                results.append(entry)
        
        # Save raw output for debugging
        raw_out = _OUTDIR / f"page_{page_num+1:04d}_raw.txt"
        raw_out.write_text(content, encoding="utf-8")
        
        return results

    except Exception as exc:
        print(f"  [API] Error on page {page_num+1}: {exc}")
        return []
    finally:
        pacer.release(MODEL_NAME)


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR CISI Vol 3 Part 3 plates using Mistral.")
    parser.add_argument("--page", type=int, help="Run OCR on a single specific page number (1-based index).")
    parser.add_argument("--all", action="store_true", help="Run OCR on the entire catalog section.")
    parser.add_argument("--from", dest="start_from", type=int, default=0, help="Resume from this 1-based page number.")
    args = parser.parse_args()

    if not _PDF_PATH.exists():
        print(f"ERROR: PDF not found at {_PDF_PATH}")
        sys.exit(1)

    client = get_client()
    pacer = get_model_pacer()
    doc = fitz.open(_PDF_PATH)
    
    all_extracted = []

    if args.page:
        page_idx = args.page - 1
        if 0 <= page_idx < len(doc):
            print(f"Processing single page {args.page}...")
            seals = run_ocr_on_page(client, doc, pacer, page_idx)
            all_extracted.extend(seals)
        else:
            print(f"Page {args.page} out of bounds (1-{len(doc)}).")
            
    elif args.all:
        start_idx = max(PAGE_START, args.start_from - 1) if args.start_from else PAGE_START
        end_idx = min(PAGE_END, len(doc))
        print(f"Processing catalog pages {start_idx+1} to {end_idx}...")
        for i in range(start_idx, end_idx):
            seals = run_ocr_on_page(client, doc, pacer, i)
            all_extracted.extend(seals)
            if seals:
                for s in seals:
                    label = s.get("seal_id") or s.get("sign_id") or s.get("raw", "")[:50]
                    detail = s.get("signs") or s.get("meaning") or s.get("motif") or ""
                    print(f"    Found ({s.get('type','?')}): {label} -> {detail}")
            time.sleep(_OCR_DELAY)
    else:
        print("Please specify --page N or --all.")
        sys.exit(1)

    if all_extracted:
        # Merge with existing if any (entries dedupe-keyed by raw line+page)
        if _OUTPUT_JSON.exists():
            try:
                existing = json.loads(_OUTPUT_JSON.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                existing = []
        else:
            existing = []
        merged = { (s.get("page"), s.get("raw", "")): s for s in existing }
        for s in all_extracted:
            merged[(s.get("page"), s.get("raw", ""))] = s
        _OUTPUT_JSON.write_text(json.dumps(list(merged.values()), indent=2), encoding="utf-8")
        print(f"Saved {len(all_extracted)} entries from this run. Total unique entries: {len(merged)}. Wrote to {_OUTPUT_JSON.name}")
    else:
        # Always write at least an empty file so consumers don't fail
        if not _OUTPUT_JSON.exists():
            _OUTPUT_JSON.write_text("[]", encoding="utf-8")
        print("No extracted entries.")

if __name__ == "__main__":
    main()
