"""Quick quality check on the scraped RMRL papers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RMRL = ROOT / "corpora" / "downloads" / "rmrl"

# Pick one Mahadevan paper, one Balakrishnan paper, and stats
samples = [
    RMRL / "research_papers" / "mahadevan" / "Murukan in the Indus script_1999" / "text.json",
    RMRL / "research_papers" / "mahadevan" / "Akam and Puram-Address signs of Indus script_201x" / "text.json",
    RMRL / "research_papers" / "balakrishnan" / "REMNANTS OF DRAVIDIAN NAME HERITAGE IN INDUS AND BEYOND" / "text.json",
]

for p in samples:
    if not p.exists():
        print(f"MISSING: {p}")
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    pages = d.get("pages", [])
    total_chars = sum(len(pp) for pp in pages)
    print(f"\n=== {p.parent.name} ===")
    print(f"  Pages: {len(pages)}, total chars: {total_chars}")
    if pages and len(pages) > 1:
        # First non-trivial page
        for i, pp in enumerate(pages):
            if len(pp) > 100:
                print(f"  --- Page {i+1} (first {1200} chars) ---")
                print(pp[:1200])
                break

print("\n=== Aggregate stats ===")
for author in ("mahadevan", "balakrishnan"):
    base = RMRL / "research_papers" / author
    if not base.exists():
        continue
    n_papers = 0
    n_pages_total = 0
    n_chars_total = 0
    for paper_dir in base.iterdir():
        if not paper_dir.is_dir():
            continue
        text_path = paper_dir / "text.json"
        if not text_path.exists():
            continue
        try:
            d = json.loads(text_path.read_text(encoding="utf-8"))
            pages = d.get("pages", [])
            n_papers += 1
            n_pages_total += len(pages)
            n_chars_total += sum(len(pp) for pp in pages)
        except Exception:
            continue
    print(f"  {author}: {n_papers} papers with text, {n_pages_total} pages, {n_chars_total:,} chars")

print("\n=== Manuscripts (Manivannan) ===")
mss_dir = RMRL / "manuscripts"
if mss_dir.exists():
    pdfs = list(mss_dir.glob("*.pdf"))
    total_size_mb = sum(p.stat().st_size for p in pdfs) / 1024 / 1024
    print(f"  {len(pdfs)} PDFs, total {total_size_mb:.1f} MB")

print("\n=== Notebooks (Mahadevan) ===")
nb_dir = RMRL / "notebooks"
if nb_dir.exists():
    n_total_pages = 0
    for d_dir in sorted(nb_dir.iterdir()):
        if not d_dir.is_dir():
            continue
        meta_path = d_dir / "meta.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        pc = meta.get("page_count", 0)
        n_total_pages += pc
        print(f"  {d_dir.name}: {pc} pages, OCR={meta.get('n_pages_with_ocr_text', 0)}")
    print(f"  TOTAL: {n_total_pages} notebook pages (image-only, OCR pending)")
