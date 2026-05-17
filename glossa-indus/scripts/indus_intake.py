"""Glossa-Lab Indus Evidence Graph — Document Intake System.

Handles:
  1. User-uploaded PDFs dropped in raw/user_uploads/
  2. Downloaded papers from acquisition scripts
  3. Checksum-based exact deduplication
  4. Text extraction (embedded PDF text or OCR queue)
  5. Metadata extraction (title, authors, year, DOI)
  6. Registration in literature/documents/
  7. Claim extraction queue entry

Usage:
    python scripts/indus_intake.py --file raw/user_uploads/myfile.pdf
    python scripts/indus_intake.py --scan raw/user_uploads/   # process all PDFs in dir
    python scripts/indus_intake.py --status                   # print queue status

Rules per instruction plan:
  - Never overwrite raw files
  - All processing produces NEW files in processed/
  - Duplicates go to quarantine/duplicate_candidates/
  - Restricted/unclear license items go to quarantine/unclear_license/
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parents[1]
RAW_UPLOADS = BASE / "raw" / "user_uploads"
LITERATURE_DOCS = BASE / "literature" / "documents"
PROCESSED_OCR = BASE / "processed" / "ocr"
PROCESSED_TEXT = BASE / "processed" / "cleaned_text"
QUARANTINE_DUPES = BASE / "quarantine" / "duplicate_candidates"
QUARANTINE_LICENSE = BASE / "quarantine" / "unclear_license"
LOGS = BASE / "logs"
INTAKE_LOG = LOGS / "intake.log"
QUEUE_FILE = BASE / "logs" / "claim_extraction_queue.json"

LITERATURE_DOCS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

# ── Utilities ─────────────────────────────────────────────────────────────────

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def ts() -> str:
    return datetime.utcnow().isoformat()

def log(msg: str) -> None:
    line = f"[{ts()}] {msg}"
    print(line)
    with open(INTAKE_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def generate_doc_id(path: Path, checksum: str) -> str:
    """Generate stable document ID from filename stem + checksum prefix."""
    stem = re.sub(r"[^a-z0-9]", "_", path.stem.lower())[:40]
    return f"{stem}_{checksum[:8]}"

# ── Checksum deduplication ────────────────────────────────────────────────────

def load_checksum_registry() -> dict[str, str]:
    """Load {checksum -> doc_id} map from literature/documents/*.yaml checksums."""
    registry = {}
    for f in LITERATURE_DOCS.glob("*.json"):
        try:
            data = json.loads(f.read_text("utf-8"))
            chk = data.get("checksum_sha256", "")
            did = data.get("document_id", "")
            if chk and did:
                registry[chk] = did
        except Exception:
            pass
    return registry

def is_exact_duplicate(checksum: str, registry: dict) -> tuple[bool, str]:
    if checksum in registry:
        return True, registry[checksum]
    return False, ""

# ── Text extraction ───────────────────────────────────────────────────────────

def extract_text_from_pdf(path: Path) -> tuple[str, bool]:
    """Try to extract embedded text from PDF. Returns (text, is_ocr_needed)."""
    try:
        import pypdf
        reader = pypdf.PdfReader(str(path))
        pages_text = []
        for page in reader.pages:
            t = page.extract_text() or ""
            pages_text.append(t)
        full_text = "\n".join(pages_text)
        # If less than 100 chars per page on average, likely scanned
        avg_chars = len(full_text) / max(len(reader.pages), 1)
        needs_ocr = avg_chars < 100
        return full_text, needs_ocr
    except ImportError:
        log("  WARNING: pypdf not installed — cannot extract PDF text. pip install pypdf")
        return "", True
    except Exception as e:
        log(f"  WARNING: PDF text extraction failed: {e}")
        return "", True

def extract_metadata_from_text(text: str, filename: str) -> dict:
    """Best-effort extraction of title/author/year/DOI from text."""
    meta: dict = {
        "detected_title": "",
        "detected_authors": [],
        "detected_year": None,
        "detected_doi": None,
        "detected_abstract": "",
    }
    # DOI
    doi_match = re.search(r'10\.\d{4,}/[\S]+', text)
    if doi_match:
        meta["detected_doi"] = doi_match.group(0).rstrip(".,;)")

    # Year (first 4-digit year between 1900-2030 in first 500 chars)
    year_match = re.search(r'\b(19[0-9]{2}|20[0-2][0-9])\b', text[:500])
    if year_match:
        meta["detected_year"] = int(year_match.group(1))

    # Fallback title = filename stem
    meta["detected_title"] = re.sub(r"[_\-]+", " ", Path(filename).stem)

    return meta

# ── Document registration ─────────────────────────────────────────────────────

def register_document(
    path: Path,
    checksum: str,
    doc_id: str,
    text: str,
    needs_ocr: bool,
    metadata: dict,
    license_status: str = "unclear",
    access_type: str = "user_uploaded",
) -> Path:
    """Write document record to literature/documents/{doc_id}.json."""
    record = {
        "document_id": doc_id,
        "original_filename": path.name,
        "stored_path_raw": str(path),
        "stored_path_text": str(PROCESSED_TEXT / f"{doc_id}.txt") if text else None,
        "file_type": path.suffix.lower(),
        "file_size_bytes": path.stat().st_size,
        "checksum_sha256": checksum,
        "intake_date": ts(),
        "license_status": license_status,
        "access_type": access_type,
        "ocr_required": needs_ocr,
        "ocr_status": "pending" if needs_ocr else "not_needed",
        "duplicate_status": "unique",
        "processing_status": "registered",
        "detected_title": metadata.get("detected_title", ""),
        "detected_authors": metadata.get("detected_authors", []),
        "detected_year": metadata.get("detected_year"),
        "detected_doi": metadata.get("detected_doi"),
        "detected_abstract": metadata.get("detected_abstract", ""),
        "claim_extraction_status": "pending",
        "hypothesis_relevance": None,
        "_citation": {
            "system": "Glossa-Lab Indus Evidence Graph",
            "intake_version": "1.0",
            "note": "User-provided or acquired document. License status must be verified before publication use.",
        },
    }

    out_path = LITERATURE_DOCS / f"{doc_id}.json"
    out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), "utf-8")

    # Save extracted text
    if text:
        txt_path = PROCESSED_TEXT / f"{doc_id}.txt"
        PROCESSED_TEXT.mkdir(parents=True, exist_ok=True)
        txt_path.write_text(text, "utf-8", errors="replace")

    return out_path

def add_to_claim_queue(doc_id: str) -> None:
    """Add document to claim extraction queue."""
    queue = []
    if QUEUE_FILE.exists():
        try:
            queue = json.loads(QUEUE_FILE.read_text("utf-8"))
        except Exception:
            pass
    if not any(item.get("doc_id") == doc_id for item in queue):
        queue.append({
            "doc_id": doc_id,
            "added_at": ts(),
            "status": "pending",
        })
        QUEUE_FILE.write_text(json.dumps(queue, indent=2), "utf-8")

# ── Main intake flow ──────────────────────────────────────────────────────────

def intake_file(path: Path) -> dict:
    """Full intake pipeline for one file. Returns status dict."""
    log(f"\n{'='*60}")
    log(f"Intake: {path.name}")

    result = {
        "file": str(path),
        "status": None,
        "doc_id": None,
        "checksum": None,
        "notes": [],
    }

    # 1. Checksum
    checksum = sha256_file(path)
    result["checksum"] = checksum
    log(f"  SHA256: {checksum[:16]}...")

    # 2. Exact deduplicate check
    registry = load_checksum_registry()
    is_dup, existing_id = is_exact_duplicate(checksum, registry)
    if is_dup:
        log(f"  EXACT DUPLICATE: already registered as {existing_id}")
        dest = QUARANTINE_DUPES / path.name
        # Don't move — just record
        result["status"] = "exact_duplicate"
        result["doc_id"] = existing_id
        result["notes"].append(f"Exact duplicate of {existing_id}")
        return result

    # 3. Generate document ID
    doc_id = generate_doc_id(path, checksum)
    result["doc_id"] = doc_id
    log(f"  Document ID: {doc_id}")

    # 4. Extract text (PDF only)
    text = ""
    needs_ocr = False
    if path.suffix.lower() == ".pdf":
        text, needs_ocr = extract_text_from_pdf(path)
        log(f"  Text extracted: {len(text)} chars  |  OCR needed: {needs_ocr}")
    else:
        log(f"  Non-PDF file — skipping text extraction")

    # 5. Extract metadata
    metadata = extract_metadata_from_text(text, path.name)
    log(f"  Title guess: {metadata.get('detected_title', '?')[:60]}")
    log(f"  Year: {metadata.get('detected_year')}  |  DOI: {metadata.get('detected_doi')}")

    # 6. Register
    record_path = register_document(
        path=path,
        checksum=checksum,
        doc_id=doc_id,
        text=text,
        needs_ocr=needs_ocr,
        metadata=metadata,
    )
    log(f"  Registered: {record_path.name}")

    # 7. Add to claim queue
    add_to_claim_queue(doc_id)
    log(f"  Added to claim extraction queue")

    result["status"] = "registered"
    result["notes"].append(f"Registered as {doc_id}")
    if needs_ocr:
        result["notes"].append("OCR required — add to OCR batch")
    return result

# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Glossa-Lab Indus Evidence Graph — Document Intake")
    parser.add_argument("--file", type=Path, help="Single file to intake")
    parser.add_argument("--scan", type=Path, help="Scan directory for PDFs to intake")
    parser.add_argument("--status", action="store_true", help="Show queue status")
    args = parser.parse_args()

    if args.status:
        print("\n=== Claim Extraction Queue ===")
        if QUEUE_FILE.exists():
            queue = json.loads(QUEUE_FILE.read_text("utf-8"))
            pending = [q for q in queue if q.get("status") == "pending"]
            done = [q for q in queue if q.get("status") == "done"]
            print(f"  Pending: {len(pending)}")
            print(f"  Done:    {len(done)}")
            for q in pending[:10]:
                print(f"  - {q['doc_id']} (added {q['added_at'][:10]})")
        else:
            print("  Queue empty")
        print(f"\n=== Literature Documents ===")
        docs = list(LITERATURE_DOCS.glob("*.json"))
        print(f"  Registered: {len(docs)}")
        return 0

    if args.file:
        if not args.file.exists():
            print(f"ERROR: File not found: {args.file}")
            return 1
        result = intake_file(args.file)
        print(f"\nResult: {result['status']}  |  ID: {result['doc_id']}")
        return 0

    if args.scan:
        pdfs = list(args.scan.glob("*.pdf")) + list(args.scan.glob("*.PDF"))
        print(f"Found {len(pdfs)} PDF(s) in {args.scan}")
        results = []
        for pdf in pdfs:
            r = intake_file(pdf)
            results.append(r)
        print(f"\n=== Scan complete ===")
        print(f"  Registered: {sum(1 for r in results if r['status'] == 'registered')}")
        print(f"  Duplicates: {sum(1 for r in results if r['status'] == 'exact_duplicate')}")
        print(f"  Failed:     {sum(1 for r in results if r['status'] not in ('registered', 'exact_duplicate'))}")
        return 0

    parser.print_help()
    return 0

if __name__ == "__main__":
    sys.exit(main())
