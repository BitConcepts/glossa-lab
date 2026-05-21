"""
Ingest Mahadevan papers from RMRL + copy user-downloaded PDFs into corpora.

1. Downloads text content of all Mahadevan research papers from RMRL
   (rmrl.in/en/dl/research-papers/mahadevan) via book_config.js S3 paths.
2. Copies user-downloaded PDFs from Downloads into corpora/downloads/external_repos/
3. Runs PyMuPDF text extraction on each PDF; flags image-only ones for OCR.

Output locations:
  - Mahadevan papers:  corpora/downloads/external_repos/mahadevan_papers/<slug>.txt
  - Acquired PDFs:     corpora/downloads/external_repos/acquired_pdfs/<name>.pdf
  - Extraction report: corpora/downloads/external_repos/acquired_pdfs/extraction_report.json
"""
import sys, json, re, time, shutil
from pathlib import Path
import urllib.request, urllib.parse

REPO = Path(__file__).resolve().parents[2]
MAHADEVAN_DIR = REPO / "corpora/downloads/external_repos/mahadevan_papers"
PDF_DIR       = REPO / "corpora/downloads/external_repos/acquired_pdfs"
MAHADEVAN_DIR.mkdir(parents=True, exist_ok=True)
PDF_DIR.mkdir(parents=True, exist_ok=True)

S3_BASE = "https://s3.us-east-1.amazonaws.com/rmrldl.in/RP/IM"

# Complete paper ID list (from href scrape of RMRL page)
MAHADEVAN_PAPERS = [
    ("1970_dravidian_parallels",         "Dravidian Parallels in Proto Indian Script_1970"),
    ("1971_method_parallelisms",         "Method of parallelisms_1973"),
    ("1971_pallavas_jar_legends",        "Pallavas and jar legends_1971"),
    ("1972_bilingual_parallels",         "Study of the Indus script through Bi-lingual parallels_1975"),
    ("1973_computer_concordance",        "Computer concordance of proto-Indian signs_1973"),
    ("1977_text_concordance_tables",     "The Indus script -text , concordance and table_1977"),
    ("1978_recent_advances",             "Recent advantage in the study of the Indus script_1978"),
    ("1980_indian_historical_tradition", "Indus script in the Indian histroical tradition_1980"),
    ("1980_sealings_from_hulas",         "Indus Sealings from Hulas_1982c"),
    ("1981_place_signs",                 "Place signs in the Indus script_1981"),
    ("1982_terminal_ideograms",          "Terminal ideograms in the Indus script_1982a"),
    ("1982_sr_rao_decipherment",         "S.R. Roas decipherment of Indus script_1982b"),
    ("1983_cult_objects_unicorn",        "The Cult objects on unicorn seals_1983"),
    ("1985_claims_decipherment",         "Clamins of decipherment of the Indus script_1985"),
    ("1986_agastya_legend",              "Agastya legend and the Indus civilization_1986e"),
    ("1986_computer_study",              "Computer study of the Indus script_1986d"),
    ("1986_database_concordance",        "Database for the Indus Script.- A computerised concordance of the Indus texts_1986a"),
    ("1986_dravidian_models",            "Dravidian models of decipherment of the Indus script_1986c"),
    ("1986_bilingual_approach",          "Study of the Indus script a bi-lingual approach_1986a"),
    ("1986_bibliography",                "The Indus Script and Related subjects, a bibliography of recent studies_1986b"),
    ("1986_grammar_indus_texts",         "Towards a grammar of the Indus texts_1986b"),
    ("1987_archaeological_context",      "Archaeological context of Indus texts at Mohenjodaro_1987"),
    ("1989_what_do_we_know",             "What do we know about the Indus script_1989"),
    ("1993_sacred_filter",               "The Sacred filter standard facing the unicorn_1993"),
    ("1994_encyclopaedia",               "An encyclopedia of the Indus script_1995"),
    ("1998_phonetic_arrow_sign",         "Phonetic value of the arrow sign in the Indus script_1998"),
    ("1999_murukan",                     "Murukan in the Indus script_1999"),
    ("2001_megalithic_pottery",          "Indus like symbols on megalithic pottery_2001a"),
    ("2006_muruku_sign",                 "A note on the Muruku sign of the Indus script_2006a"),
    ("2006_agricultural_terms",          "Agricultural terms in the Indus script_2006b"),
    ("2007_megalithic_harappa",          "A Megalithic pottery inscription and a Harappa tablets_2007"),
    ("2008_blue_neck",                   "How did the _great god_ get a _blue neck_ - a bilingual clue to the Indus script_2008"),
    ("2008_meluhha_agastya",             "Meluhha and Agastya - Alpha and Omega of the Indus script_2008"),
    ("2009_text_context",                "The Indus Script Text and Context_2010"),
    ("2009_vestiges",                    "Vestiges of Indus Civilisation_2009"),
    ("2008_harappan_heritage_andhra",    "Harappan Heritage of Andhra_2008"),
    ("2011_akam_puram",                  "Akam and Puram-Address signs of Indus script_201x"),
    ("2018_toponyms",                    "toponyms_directions_placenames"),
]

# Additional papers we'll try with guessed IDs
EXTRA_PAPERS = [
    ("2011_indus_fish_great_bath",       "The Indus fish swam in the Great Bath_2011"),
    ("2014_dravidian_proof_rig_veda",    "Dravidian Proof of the Indus Script via the Rig Veda_2014"),
    ("2002_aryan_dravidian",             "Aryan or Dravidian or Neither_2002"),
    ("2011_indus_fish_alt",              "Indus fish swam in the great bath_2011"),
    ("2011_fish_bath",                   "The Indus Fish Swam in the Great Bath_2011"),
]

def fetch_text(paper_id: str) -> str | None:
    """Download book_config.js and extract page text."""
    enc_id = urllib.parse.quote(paper_id, safe=" ")
    url = f"{S3_BASE}/{enc_id}/files/search/book_config.js"
    # Also try URI-encoded spaces as %20
    url2 = f"{S3_BASE}/{urllib.parse.quote(paper_id)}/files/search/book_config.js"
    for u in [url, url2]:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "glossa-lab/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                # Extract text array from: var textForPages = ["...", "..."]
                m = re.search(r'var\s+textForPages\s*=\s*(\[.*?\]);', raw, re.DOTALL)
                if m:
                    try:
                        pages = json.loads(m.group(1))
                        return "\n\n--- PAGE BREAK ---\n\n".join(pages)
                    except Exception:
                        return raw  # return raw if JSON parse fails
                return raw
        except Exception:
            continue
    return None

# ─── 1. Download Mahadevan papers ─────────────────────────────────────────
print("="*70)
print("STEP 1: DOWNLOADING MAHADEVAN PAPERS FROM RMRL")
print("="*70)

results = {}
all_papers = MAHADEVAN_PAPERS + EXTRA_PAPERS

for slug, paper_id in all_papers:
    out_path = MAHADEVAN_DIR / f"{slug}.txt"
    if out_path.exists() and out_path.stat().st_size > 100:
        print(f"  SKIP (exists): {slug}")
        results[slug] = "exists"
        continue

    print(f"  Fetching: {slug}...", end="", flush=True)
    text = fetch_text(paper_id)
    if text and len(text) > 100:
        out_path.write_text(text, encoding="utf-8")
        kb = len(text) // 1024
        print(f" OK ({kb}KB)")
        results[slug] = f"downloaded_{kb}KB"
    else:
        print(f" FAIL (id not found)")
        results[slug] = "not_found"
    time.sleep(0.3)  # polite rate limit

downloaded = sum(1 for v in results.values() if v.startswith("downloaded") or v == "exists")
print(f"\n  Papers downloaded/available: {downloaded}/{len(all_papers)}")

# ─── 2. Copy user-downloaded PDFs ─────────────────────────────────────────
print("\n" + "="*70)
print("STEP 2: COPYING USER-DOWNLOADED PDFs TO CORPORA")
print("="*70)

USER_PDFS = {
    "bahrain_through_the_ages.pdf":       r"C:\Users\trist\Downloads\bahrain through the ages.pdf",
    "rao_yadav_conditional_entropy.pdf":  r"C:\Users\trist\Downloads\Rao_Yadav_Mahadevan conditional entropy paper.pdf",
    "cisi_collections_india.pdf":         r"C:\Users\trist\Downloads\Corpus of Indus Seals and Inscriptions. Collections in India.pdf",
    "parpola_1994_deciphering.pdf":       r"C:\Users\trist\Downloads\Parpola 1994 — Deciphering the Indus Script.pdf",
    "laursen_2010_gulf_type_seals.pdf":   r"C:\Users\trist\Downloads\The_westward_transmission_of_Indus_Valle.pdf",
    "wells_2015_archaeology_epigraphy.pdf": r"C:\Users\trist\Downloads\The Archaeology And Epigraphy of Indus Writing.pdf",
}

pdf_results = {}
for dest_name, src_path in USER_PDFS.items():
    src = Path(src_path)
    dest = PDF_DIR / dest_name
    if not src.exists():
        print(f"  MISSING SOURCE: {src_path}")
        pdf_results[dest_name] = "source_missing"
        continue
    if dest.exists():
        print(f"  SKIP (exists): {dest_name} ({dest.stat().st_size//1024}KB)")
        pdf_results[dest_name] = "exists"
        continue
    shutil.copy2(src, dest)
    sz = dest.stat().st_size // 1024
    print(f"  COPIED: {dest_name} ({sz}KB)")
    pdf_results[dest_name] = f"copied_{sz}KB"

# ─── 3. Extract text from PDFs + flag OCR needs ───────────────────────────
print("\n" + "="*70)
print("STEP 3: TEXT EXTRACTION FROM PDFs")
print("="*70)

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False
    print("  PyMuPDF not available — skipping text extraction")

extraction_report = {}
if HAS_FITZ:
    for pdf_file in sorted(PDF_DIR.glob("*.pdf")):
        print(f"\n  {pdf_file.name}:")
        try:
            doc = fitz.open(str(pdf_file))
            n_pages = len(doc)
            all_text = []
            for page in doc:
                all_text.append(page.get_text())
            doc.close()
            total_text = " ".join(all_text)
            char_count = len(total_text.strip())
            txt_per_page = char_count / max(n_pages, 1)

            if txt_per_page < 50:
                status = "IMAGE_ONLY_NEEDS_OCR"
                print(f"    Pages: {n_pages} | Chars: {char_count} → IMAGE-ONLY (needs OCR)")
            else:
                status = "TEXT_EXTRACTED"
                # Save extracted text
                txt_path = PDF_DIR / (pdf_file.stem + "_extracted.txt")
                txt_path.write_text(total_text, encoding="utf-8")
                print(f"    Pages: {n_pages} | Chars: {char_count} | {txt_per_page:.0f} chars/page → TEXT OK")

            extraction_report[pdf_file.name] = {
                "pages": n_pages,
                "total_chars": char_count,
                "chars_per_page": round(txt_per_page, 1),
                "status": status,
            }
        except Exception as e:
            print(f"    ERROR: {e}")
            extraction_report[pdf_file.name] = {"status": f"error: {e}"}

# Save extraction report
report = {
    "mahadevan_download_results": results,
    "pdf_copy_results": pdf_results,
    "pdf_extraction": extraction_report,
    "mahadevan_papers_dir": str(MAHADEVAN_DIR),
    "acquired_pdfs_dir": str(PDF_DIR),
}
report_path = PDF_DIR / "extraction_report.json"
report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\n\nReport saved → {report_path}")
print("="*70)
