"""Internet Archive IIIF — Batch image downloader for OCR seeding.

Downloads page images from the staged IIIF URL lists:
  - mahadevan1977: 842 pages (Mahadevan 1977 Indus Script Concordance scan)
  - corpus-vol-2:  431 pages (CISI vol. 2 scan)

Acquisition mode: iiif_batch
Rights class: internet-archive-derivative (OCR seeding ONLY — do not canonicalize)

Usage:
    shell.cmd python backend/scripts/acquire_ia_iiif_images.py
        [--item mahadevan1977|corpus-vol-2|all]
        [--resolution 1200|1800|max]
        [--force]              # re-download files that already exist
        [--workers N]          # parallel workers (default: 4)
        [--retries N]          # retry attempts per image (default: 3)
        [--timeout N]          # HTTP timeout in seconds (default: 120)

Output:
    glossa-corpus/indus/sources/internet-archive/raw/{date}/images/{item}/

Images are saved with SHA-256-based filenames and a sidecar .url.txt for provenance.
A download log (download_log.tsv) tracks all results for resuming.
Press Ctrl+C at any time to abort gracefully — partial progress is saved.

CRITICAL: These images are for OCR/image pipeline training only.
Do NOT canonicalize readings from these scans without reconciliation
against official CISI/Mahadevan editions.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import signal
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parents[2]
IA_RAW = REPO / "glossa-corpus" / "indus" / "sources" / "internet-archive" / "raw"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")

UA = "GlossaLabResearchBot/0.1 (indus-corpus-reconstruction; contact=research@layer1labs.ai)"

ITEMS = {
    "mahadevan1977": {
        "url_list": "mahadevan1977_page_image_urls.json",
        "description": "Mahadevan 1977 — The Indus Script: Texts, Concordance and Tables",
        "expected_pages": 842,
    },
    "corpus-vol-2": {
        "url_list": "corpus-vol-2_page_image_urls.json",
        "description": "Corpus of Indus Seals and Inscriptions, Vol. 2",
        "expected_pages": 431,
    },
}

# Defaults — overridden by CLI args in main()
MAX_WORKERS = 4
SLEEP_BETWEEN = 0.3
TIMEOUT = 120
MAX_RETRIES = 3
RETRY_BASE_DELAY = 1.0  # seconds; doubles each attempt

# Global abort flag — set by Ctrl+C handler
_shutdown = threading.Event()


def _handle_sigint(sig, frame) -> None:  # noqa: ANN001
    if _shutdown.is_set():
        print("\n  [!] Force-exiting.", flush=True)
        sys.exit(1)
    print("\n  [!] Abort requested — finishing in-flight downloads then stopping...", flush=True)
    _shutdown.set()


signal.signal(signal.SIGINT, _handle_sigint)


def sha256_url(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def rewrite_url(url: str, resolution: str) -> str:
    """Rewrite IIIF image URL to requested resolution.

    Uses the ^ prefix (IIIF Image API 3) so the server returns the native
    size when the image is smaller than the requested width, rather than
    refusing with HTTP 400.  If the server does not support ^ (also 400),
    download_one falls back to the original max URL automatically.
    """
    if resolution == "max":
        return url
    if "/full/" in url:
        return (
            url
            .replace("/full/max/", f"/full/^{resolution},/")
            .replace("/full/full/", f"/full/^{resolution},/")
        )
    return url


def download_one(args: tuple) -> tuple[str, str, str]:
    """Download one IIIF image with retries.  Returns (status, url, detail)."""
    url, original_url, dest, sidecar, force = args

    if not force and dest.exists() and dest.stat().st_size > 0:
        return ("skip", url, str(dest))

    if _shutdown.is_set():
        return ("abort", url, "aborted")

    headers = {
        "User-Agent": UA,
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }

    # Candidate URLs to try: rewritten first, then original as fallback
    candidates = [url] if url == original_url else [url, original_url]
    last_error = "unknown error"

    for candidate in candidates:
        if _shutdown.is_set():
            return ("abort", url, "aborted")

        for attempt in range(MAX_RETRIES):
            if _shutdown.is_set():
                return ("abort", url, "aborted")
            try:
                req = urllib.request.Request(candidate, headers=headers)
                with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                    content = r.read()
                if not content:
                    last_error = "empty response"
                    break  # don't retry empty — try next candidate
                dest.write_bytes(content)
                sidecar.write_text(candidate, encoding="utf-8")
                time.sleep(SLEEP_BETWEEN)
                return ("ok", candidate, str(dest))
            except urllib.error.HTTPError as exc:
                last_error = f"HTTP {exc.code} {exc.reason}"
                if exc.code in (400, 403, 404, 410):
                    break  # permanent for this candidate — try next
                # 5xx / other: retry with backoff
            except urllib.error.URLError as exc:
                last_error = f"URLError: {exc.reason}"
            except Exception as exc:
                last_error = str(exc)

            if attempt < MAX_RETRIES - 1 and not _shutdown.is_set():
                time.sleep(RETRY_BASE_DELAY * (2 ** attempt))

    return ("fail", url, last_error)


def download_item(
    item_name: str,
    resolution: str,
    date_dir: Path,
    force: bool,
) -> dict:
    """Download all images for one IA item."""
    meta = ITEMS[item_name]

    url_list_path = None
    for d in sorted(IA_RAW.iterdir(), reverse=True):
        p = d / meta["url_list"]
        if p.exists():
            url_list_path = p
            break
    if not url_list_path:
        print(f"  ERROR: URL list not found for {item_name}. Run acquire_free.py --tier 3 first.")
        return {"status": "no_url_list"}

    urls = json.loads(url_list_path.read_text(encoding="utf-8"))
    print(f"\n  {item_name}: {len(urls)} URLs from {url_list_path}")
    print(f"  Description: {meta['description']}")
    print(f"  Resolution: {resolution} | Workers: {MAX_WORKERS} | Retries: {MAX_RETRIES} | Timeout: {TIMEOUT}s")
    if force:
        print("  Force re-download: ON")

    img_dir = date_dir / "images" / item_name
    img_dir.mkdir(parents=True, exist_ok=True)
    log_path = date_dir / f"{item_name}_download_log.tsv"

    # Build tasks: (rewritten_url, original_url, dest, sidecar, force)
    tasks = []
    for i, original_url in enumerate(urls):
        rewritten = rewrite_url(original_url, resolution)
        h = sha256_url(rewritten)
        dest = img_dir / f"{i:04d}_{h}.jpg"
        sidecar = img_dir / f"{i:04d}_{h}.url.txt"
        tasks.append((rewritten, original_url, dest, sidecar, force))

    results: dict[str, int] = {"ok": 0, "skip": 0, "fail": 0, "empty": 0, "abort": 0}
    log_lines = ["status\tindex\turl\tdetail"]
    first_errors: list[str] = []
    SHOW_ERRORS = 5  # print first N distinct errors to console

    print(f"  Downloading {len(tasks)} images... (Ctrl+C to abort)")

    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    try:
        futures = {executor.submit(download_one, t): i for i, t in enumerate(tasks)}
        for future in as_completed(futures):
            idx = futures[future]
            status, url, detail = future.result()
            results[status] += 1
            log_lines.append(f"{status}\t{idx}\t{url}\t{detail}")

            total = sum(results.values())
            show_progress = (total % 50 == 0) or (total == len(tasks))

            if status in ("fail", "empty"):
                if len(first_errors) < SHOW_ERRORS:
                    first_errors.append(f"    [{idx:04d}] {detail}")
                    print(f"  Progress: {total}/{len(tasks)} | ok:{results['ok']} skip:{results['skip']} "
                          f"fail:{results['fail']} | {detail}", flush=True)
                elif show_progress:
                    print(f"  Progress: {total}/{len(tasks)} | ok:{results['ok']} skip:{results['skip']} "
                          f"fail:{results['fail']}", flush=True)
            elif show_progress:
                print(f"  Progress: {total}/{len(tasks)} | ok:{results['ok']} skip:{results['skip']} "
                      f"fail:{results['fail']}", flush=True)

            if _shutdown.is_set():
                for f in futures:
                    f.cancel()
                break
    except KeyboardInterrupt:
        _shutdown.set()
    finally:
        executor.shutdown(wait=False, cancel_futures=True)

    log_path.write_text("\n".join(log_lines), encoding="utf-8")

    aborted = _shutdown.is_set() and results["abort"] > 0
    prefix = "[ABORTED] " if aborted else ""
    print(f"\n  {prefix}Done: ok={results['ok']}, skip={results['skip']}, "
          f"fail={results['fail']}, abort={results['abort']}")
    if first_errors:
        print(f"  First {len(first_errors)} error(s):")
        for e in first_errors:
            print(e)
    print(f"  Images: {img_dir}")
    print(f"  Log:    {log_path}")

    return {
        "status": "aborted" if aborted else "complete",
        "total": len(tasks),
        **results,
        "img_dir": str(img_dir),
    }


def main() -> int:
    global MAX_WORKERS, MAX_RETRIES, TIMEOUT

    parser = argparse.ArgumentParser(
        description="Download IA IIIF page images for OCR seeding."
    )
    parser.add_argument("--item", choices=list(ITEMS.keys()) + ["all"], default="all")
    parser.add_argument(
        "--resolution", choices=["1200", "1800", "max"], default="1800",
        help="IIIF width (default: 1800). Falls back to native size if image is smaller.",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Re-download files that already exist on disk.",
    )
    parser.add_argument(
        "--workers", type=int, default=MAX_WORKERS,
        help=f"Parallel download workers (default: {MAX_WORKERS})",
    )
    parser.add_argument(
        "--retries", type=int, default=MAX_RETRIES,
        help=f"Max retry attempts per image (default: {MAX_RETRIES})",
    )
    parser.add_argument(
        "--timeout", type=int, default=TIMEOUT,
        help=f"HTTP timeout in seconds (default: {TIMEOUT})",
    )
    args = parser.parse_args()

    MAX_WORKERS = args.workers
    MAX_RETRIES = args.retries
    TIMEOUT = args.timeout

    date_dir = IA_RAW / TODAY
    date_dir.mkdir(parents=True, exist_ok=True)

    print("=== Internet Archive IIIF Batch Downloader ===")
    print("NOTE: Images are for OCR seeding ONLY.")
    print("Do NOT canonicalize without reconciliation against official CISI/Mahadevan editions.")
    print(f"Output: {date_dir}")
    print(f"Resolution: {args.resolution}")

    items_to_run = list(ITEMS.keys()) if args.item == "all" else [args.item]
    all_results = {}

    for item in items_to_run:
        if _shutdown.is_set():
            print(f"\n  Skipping {item} — aborted.")
            break
        all_results[item] = download_item(item, args.resolution, date_dir, args.force)

    report = {
        "_citation": {
            "primary_sources": ["I.8"],
            "derivation": "Internet Archive IIIF image batch download for OCR seeding. Derivative fallback only.",
        },
        "batch_id": f"{TODAY}-IA-IIIF-IMAGES",
        "timestamp": datetime.utcnow().isoformat(),
        "resolution": args.resolution,
        "rights_class": "internet-archive-derivative",
        "usage": "OCR seeding ONLY — do not canonicalize without official reconciliation",
        "results": all_results,
    }
    rpt = date_dir / f"ia_images_report_{TODAY}.json"
    rpt.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport: {rpt}")
    return 1 if _shutdown.is_set() else 0


if __name__ == "__main__":
    sys.exit(main())
