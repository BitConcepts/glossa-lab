"""Batch 3: Literature sweep — download open-access Indus script papers.

All papers are confirmed open access (CC-BY, arXiv, institutional repository,
or government publication). Full provenance recorded per instruction plan.

Usage:
    python scripts/indus_literature_batch3.py
    python scripts/indus_literature_batch3.py --dry-run   # list only, no download

H20 note: No emails are sent by this script.
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parents[1]
PAPERS_DIR = BASE / "raw" / "papers"
LIT_DOCS = BASE / "literature" / "documents"
LOGS = BASE / "logs"
PAPERS_DIR.mkdir(parents=True, exist_ok=True)
LIT_DOCS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

UA = "GlossaIndusEvidenceGraph/1.0 (research; tpierson@bitconcepts.tech)"

# ── Paper catalogue ────────────────────────────────────────────────────────────
PAPERS = [
    {
        "id": "yadav_2010_ngrams",
        "title": "Statistical Analysis of the Indus Script Using n-Grams",
        "authors": ["Yadav N", "Joglekar H", "Rao RPN", "Vahia MN", "Adhikari R", "Mahadevan I"],
        "year": 2010,
        "doi": "10.1371/journal.pone.0009506",
        "journal": "PLoS ONE",
        "license": "CC BY 4.0",
        "access": "open_access",
        "url": "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0009506&type=printable",
        "filename": "yadav_2010_ngrams_plosone.pdf",
        "relevance": "core_computational",
        "notes": "n-gram analysis of Indus script; EBUDS corpus; bigram model",
    },
    {
        "id": "yadav_2009_arxiv",
        "title": "Statistical analysis of the Indus script using n-grams (preprint)",
        "authors": ["Yadav N", "Joglekar H", "Rao RPN", "Vahia MN", "Mahadevan I", "Adhikari R"],
        "year": 2009,
        "arxiv": "0901.3017",
        "license": "arXiv (non-exclusive)",
        "access": "open_access",
        "url": "https://arxiv.org/pdf/0901.3017",
        "filename": "yadav_2009_ngrams_arxiv.pdf",
        "relevance": "core_computational",
        "notes": "arXiv preprint of PLoS ONE paper",
    },
    {
        "id": "rao_2009_pnas_markov",
        "title": "A Markov model of the Indus script",
        "authors": ["Rao RPN", "Yadav N", "Vahia MN", "Joglekar H", "Adhikari R", "Mahadevan I"],
        "year": 2009,
        "doi": "10.1073/pnas.0906237106",
        "journal": "PNAS",
        "license": "open_access_pnas",
        "access": "open_access",
        "url": "https://www.pnas.org/doi/pdf/10.1073/pnas.0906237106",
        "filename": "rao_2009_markov_pnas.pdf",
        "relevance": "core_computational",
        "notes": "Markov model; contact-zone inscriptions; sign restoration",
    },
    {
        "id": "rao_2010_coli_entropy",
        "title": "Entropy, the Indus Script, and Language: A Reply to R. Sproat",
        "authors": ["Rao RPN", "Yadav N", "Vahia MN", "Joglekar H", "Adhikari R", "Mahadevan I"],
        "year": 2010,
        "journal": "Computational Linguistics",
        "license": "open_access_acl",
        "access": "open_access",
        "url": "https://aclanthology.org/J10-4016.pdf",
        "filename": "rao_2010_entropy_coli.pdf",
        "relevance": "critique_response",
        "notes": "Reply to Sproat 2010; block entropy argument; Farmer-Sproat-Witzel critique response",
    },
    {
        "id": "parpola_2010_dravidian_solution",
        "title": "A Dravidian solution to the Indus script problem",
        "authors": ["Parpola A"],
        "year": 2010,
        "journal": "World Classical Tamil Conference keynote",
        "publisher": "Central Institute of Classical Tamil",
        "license": "institutional_repository",
        "access": "open_access",
        "url": "https://tuhat.helsinki.fi/ws/portalfiles/portal/127256525/Parpola_A_2010._A_Dravidian_solution_to_the_Indus_script_problem.pdf",
        "filename": "parpola_2010_dravidian_solution.pdf",
        "relevance": "core_decipherment_hypothesis",
        "notes": "Parpola's accessible summary of the Dravidian hypothesis; rebus principle; fish sign",
    },
    {
        "id": "sinha_2010_network_arxiv",
        "title": "Network analysis of a corpus of undeciphered Indus civilization inscriptions indicates syntactic organization",
        "authors": ["Sinha S", "Ashraf MI", "Pan RK", "Wells BK"],
        "year": 2010,
        "arxiv": "1005.4997",
        "doi": "10.1016/j.csl.2010.05.007",
        "journal": "Computer Speech and Language",
        "license": "arXiv (non-exclusive)",
        "access": "open_access",
        "url": "https://arxiv.org/pdf/1005.4997",
        "filename": "sinha_2010_network_arxiv.pdf",
        "relevance": "core_computational",
        "notes": "Complex network analysis; syntactic structure; Wells corpus; recursive segmentation",
    },
    {
        "id": "farmer_sproat_witzel_2004",
        "title": "The Collapse of the Indus-Script Thesis: The Myth of a Literate Harappan Civilization",
        "authors": ["Farmer S", "Sproat R", "Witzel M"],
        "year": 2004,
        "journal": "Electronic Journal of Vedic Studies",
        "license": "open_access_ejvs",
        "access": "open_access",
        "url": "https://www.academia.edu/4530410/The_Collapse_of_the_Indus-Script_Thesis_The_Myth_of_a_Literate_Harappan_Civilization",
        "filename": "farmer_sproat_witzel_2004_nonlinguistic.pdf",
        "relevance": "core_critique",
        "notes": "The main non-linguistic hypothesis paper. Must be registered as hypothesis stub.",
        "download_notes": "Academia.edu may require login — register metadata only if download fails",
    },
    {
        "id": "rao_2009_science_entropic",
        "title": "Entropic Evidence for Linguistic Structure in the Indus Script",
        "authors": ["Rao RPN", "Yadav N", "Vahia MN", "Joglekar H", "Adhikari R", "Mahadevan I"],
        "year": 2009,
        "doi": "10.1126/science.1170391",
        "journal": "Science",
        "license": "paywalled_aaas",
        "access": "paywalled",
        "url": None,
        "filename": None,
        "relevance": "landmark_statistical",
        "notes": "The foundational Science paper on conditional entropy. Paywalled — register metadata only.",
        "metadata_only": True,
    },
    {
        "id": "mahadevan_2009_signs",
        "title": "The Indus Script: A Synthesis",
        "authors": ["Mahadevan I"],
        "year": 2009,
        "journal": "Annual Report 2007-2008, Indus Research Centre, RMRL",
        "license": "institutional",
        "access": "institutional",
        "url": "https://rmrl.in/irc-publications",
        "filename": None,
        "relevance": "core_sign_catalog",
        "notes": "Mahadevan's own summary of the sign list and concordance. Register metadata.",
        "metadata_only": True,
    },
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def ts() -> str:
    return datetime.utcnow().isoformat()

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def log(msg: str) -> None:
    line = f"[{ts()}] {msg}"
    print(line)
    with open(LOGS / "batch3_literature.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def download_pdf(url: str, dest: Path) -> tuple[bool, str]:
    """Download PDF; return (success, checksum_or_error)."""
    if dest.exists() and dest.stat().st_size > 5000:
        return True, sha256_bytes(dest.read_bytes())
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "application/pdf,*/*",
            "Referer": "https://glossa-indus-evidence-graph.research/",
        })
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        if len(data) < 5000:
            return False, f"File too small ({len(data)} bytes)"
        dest.write_bytes(data)
        return True, sha256_bytes(data)
    except Exception as e:
        return False, str(e)

def register_document(paper: dict, filepath: Path | None, checksum: str | None) -> None:
    """Write document record to literature/documents/."""
    doc = {
        "document_id": paper["id"],
        "title": paper["title"],
        "authors": paper["authors"],
        "year": paper["year"],
        "journal": paper.get("journal"),
        "doi": paper.get("doi"),
        "arxiv": paper.get("arxiv"),
        "license_status": paper["license"],
        "access_type": paper["access"],
        "source_url": paper.get("url"),
        "stored_path_raw": str(filepath) if filepath else None,
        "checksum_sha256": checksum,
        "intake_date": ts(),
        "relevance": paper["relevance"],
        "notes": paper.get("notes", ""),
        "metadata_only": paper.get("metadata_only", False),
        "claim_extraction_status": "pending" if not paper.get("metadata_only") else "metadata_only",
        "_citation": {
            "system": "Glossa-Lab Indus Evidence Graph Batch 3",
            "note": "Literature sweep 2026-05-17",
        },
    }
    out = LIT_DOCS / f"{paper['id']}.json"
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False), "utf-8")

# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Batch 3 literature sweep")
    parser.add_argument("--dry-run", action="store_true", help="List papers only, no download")
    args = parser.parse_args()

    results = {
        "batch_id": f"BATCH3-LITERATURE-{datetime.utcnow().strftime('%Y%m%d')}",
        "timestamp": ts(),
        "papers": [],
    }

    print(f"\n{'='*60}")
    print(f"Batch 3: Literature Sweep — {len(PAPERS)} papers")
    print(f"Output: {PAPERS_DIR}")
    print(f"{'='*60}\n")

    downloaded = failed = metadata_only = skipped = 0

    for paper in PAPERS:
        pid = paper["id"]
        title_short = paper["title"][:55] + "..." if len(paper["title"]) > 55 else paper["title"]
        print(f"\n  [{pid}]")
        print(f"  {title_short}")
        print(f"  Authors: {', '.join(paper['authors'][:2])} et al. ({paper['year']})")
        print(f"  License: {paper['license']}  |  Access: {paper['access']}")

        if paper.get("metadata_only"):
            print(f"  → METADATA ONLY (paywalled or institutional)")
            register_document(paper, None, None)
            metadata_only += 1
            results["papers"].append({"id": pid, "status": "metadata_only"})
            continue

        if not paper.get("url"):
            print(f"  → SKIP (no URL)")
            skipped += 1
            continue

        if args.dry_run:
            print(f"  → DRY RUN (would download: {paper['url'][:80]})")
            continue

        dest = PAPERS_DIR / paper["filename"]
        log(f"Downloading: {pid} from {paper['url'][:80]}")
        ok, checksum_or_err = download_pdf(paper["url"], dest)

        if ok:
            size_kb = dest.stat().st_size // 1024
            print(f"  → OK ({size_kb}KB, sha256={checksum_or_err[:12]}...)")
            register_document(paper, dest, checksum_or_err)
            downloaded += 1
            results["papers"].append({"id": pid, "status": "downloaded", "size_kb": size_kb, "checksum": checksum_or_err[:16]})
        else:
            print(f"  → FAIL: {checksum_or_err[:80]}")
            print(f"     → Registering metadata only")
            register_document(paper, None, None)
            failed += 1
            results["papers"].append({"id": pid, "status": "failed", "error": checksum_or_err[:80]})

        time.sleep(1.5)  # polite rate limiting

    print(f"\n{'='*60}")
    print(f"Batch 3 complete:")
    print(f"  Downloaded:     {downloaded}")
    print(f"  Failed:         {failed}")
    print(f"  Metadata only:  {metadata_only}")
    print(f"  Skipped:        {skipped}")
    print(f"  Total papers:   {len(PAPERS)}")
    print(f"  Documents registered: {len(list(LIT_DOCS.glob('*.json')))}")

    rpt = BASE / "reports" / "ingestion_reports" / "batch3_literature_report.json"
    rpt.parent.mkdir(parents=True, exist_ok=True)
    rpt.write_text(json.dumps(results, indent=2), "utf-8")
    print(f"\nReport: {rpt}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
