"""
IndusScript.in data acquisition + RMRL M77 concordance manual download.

The indusscript.in website is a Firebase/Firestore-backed Flutter SPA.
Direct scraping of Firestore data requires Google OAuth authentication,
which is not feasible without user credentials. This script:

1. Downloads the M77 concordance manual PDF from RMRL
2. Attempts to access any public Firestore REST endpoints
3. Documents what data is available and how to access it

For full Firestore access, the user would need to:
- Sign in with Google on indusscript.in
- Export the session cookie
- Use the Firestore REST API with the session token
"""
import json
import os
import urllib.request
import urllib.error
from pathlib import Path

CORPORA_DIR = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\corpora\downloads\rmrl")
CORPORA_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\backend\reports")


def download_m77_manual():
    """Download the Iravatham Mahadevan 1977 concordance manual PDF from RMRL."""
    url = "https://rmrl.in/wp-content/uploads/IM77-Manual.pdf"
    out_path = CORPORA_DIR / "IM77-Manual.pdf"
    if out_path.exists():
        print(f"  Already downloaded: {out_path} ({out_path.stat().st_size // 1024}KB)")
        return str(out_path)
    print(f"  Downloading M77 manual from {url}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        out_path.write_bytes(data)
        print(f"  Downloaded: {out_path} ({len(data) // 1024}KB)")
        return str(out_path)
    except Exception as e:
        print(f"  Failed to download: {e}")
        return None


def check_firestore_public():
    """Check if indusscript.in's Firestore has any public collections."""
    # The Firebase project ID from the JS source
    # Try common Firestore REST API patterns
    project_ids = ["indus-script-app", "indusscript", "indus-script"]
    results = {}
    for pid in project_ids:
        url = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents"
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                results[pid] = {"status": "accessible", "collections": list(data.keys())[:20]}
                print(f"  Firestore {pid}: ACCESSIBLE - {list(data.keys())[:5]}")
        except urllib.error.HTTPError as e:
            results[pid] = {"status": f"HTTP {e.code}", "note": str(e.reason)}
            print(f"  Firestore {pid}: HTTP {e.code} ({e.reason})")
        except Exception as e:
            results[pid] = {"status": "error", "note": str(e)}
            print(f"  Firestore {pid}: {e}")
    return results


def document_data_availability():
    """Document what data is available from indusscript.in and how to access it."""
    return {
        "source": "https://indusscript.in/",
        "operator": "RMRL (Roja Muthiah Research Library) / Tamil Nadu Archaeology Dept",
        "technology": "Flutter web app backed by Firebase/Firestore",
        "data_content": {
            "concordance": "Iravatham Mahadevan's 1977 concordance (M77) — complete",
            "sign_list": "417 signs per M77, with variants",
            "inscriptions": "~2,900+ inscriptions from M77 corpus",
            "field_symbols": "Animal motifs and field symbols",
        },
        "access_methods": {
            "public_pdf": "https://rmrl.in/wp-content/uploads/IM77-Manual.pdf (manual/guide)",
            "firestore_api": "Requires Google OAuth via the web app — not publicly accessible",
            "contact": "RMRL, Chennai — scholarly access may be available on request",
        },
        "alternative_sources": {
            "mahadevan_1977_ocr": "Already in our corpus (mahadevan_1977_full.txt, 674KB)",
            "holdat_llc": "1,670 seals with Mahadevan numbering (already in corpus)",
            "cisi_mayig": "179 Mohenjo-daro inscriptions with Parpola numbering (already in corpus)",
            "fuls_icit": "~4,537 inscriptions — contact andreas.fuls@tu-berlin.de for access",
        },
        "recommendation": "The M77 concordance data we already have from the OCR'd text + Holdat corpus "
                         "covers the same underlying dataset. The indusscript.in app adds a digital "
                         "interface but the raw data is the same M77 concordance. Priority should be "
                         "acquiring the ICIT (Fuls/Wells) corpus which has 4,537 inscriptions including "
                         "multi-line texts not in M77.",
    }


def main():
    print("=" * 60)
    print("IndusScript.in Data Acquisition")
    print("=" * 60)

    # 1. Download M77 manual
    print("\n1. M77 Concordance Manual (RMRL)")
    m77_path = download_m77_manual()

    # 2. Check Firestore
    print("\n2. Firestore Public Access Check")
    firestore_results = check_firestore_public()

    # 3. Document availability
    print("\n3. Data Availability Assessment")
    availability = document_data_availability()
    print(f"  Recommendation: {availability['recommendation'][:100]}...")

    # Save report
    report = {
        "title": "IndusScript.in Data Acquisition Report",
        "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "m77_manual": {"downloaded": m77_path is not None, "path": m77_path},
        "firestore": firestore_results,
        "availability": availability,
    }
    out = REPORT_DIR / "indusscript_in_acquisition.json"
    with open(out, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\n  Report saved: {out}")
    print("=" * 60)


if __name__ == "__main__":
    main()
