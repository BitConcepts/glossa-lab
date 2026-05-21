"""Phase-22 contact-zone acquisition v2.

Improvements over v1:
- Resolves Zenodo records via the Zenodo API to get exact file URLs.
- Extracts the HAL embedded PDF URL from the viewer HTML when /document
  returns HTML.
- Tries multiple URL fallbacks per item.
- Records detailed provenance (source URL, sha256, byte size) into a
  manifest JSON so downstream steps know what's local.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TARGET_DIR = ROOT / "corpora" / "downloads" / "contact_zone" / "publications"
TARGET_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_PATH = TARGET_DIR / "_manifest.json"

UA = (
    "Mozilla/5.0 (compatible; GlossaLab-ContactZoneAcquisition/2.0; "
    "research; +https://github.com/BitConcepts/glossa-lab)"
)


def _http_bytes(url: str, timeout: int = 90,
                accept: str = "application/pdf,*/*;q=0.5") -> tuple[bool, bytes, str]:
    headers = {"User-Agent": UA, "Accept": accept}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        return True, data, f"HTTP {resp.status}"
    except Exception as exc:  # noqa: BLE001
        return False, b"", f"{type(exc).__name__}: {exc}"


def _save_pdf(url: str, dest: Path) -> tuple[bool, int, str]:
    ok, data, note = _http_bytes(url)
    if not ok:
        return False, 0, note
    if len(data) < 1024 or not data[:8].startswith(b"%PDF"):
        return False, len(data), f"not a PDF (head={data[:8]!r})"
    dest.write_bytes(data)
    return True, len(data), note


def _resolve_zenodo(record_id: str) -> list[str]:
    """Query Zenodo API to get direct file download URLs."""
    api_url = f"https://zenodo.org/api/records/{record_id}"
    ok, data, note = _http_bytes(api_url, accept="application/json")
    if not ok:
        return []
    try:
        meta = json.loads(data.decode("utf-8"))
    except Exception:  # noqa: BLE001
        return []
    files = meta.get("files") or []
    urls = []
    for f in files:
        u = (f.get("links") or {}).get("self") or f.get("self")
        if isinstance(u, str):
            urls.append(u)
    return urls


def _extract_hal_pdf_url(html_url: str) -> list[str]:
    """Some HAL /document URLs return an HTML viewer; parse for the
    embedded PDF URL."""
    ok, data, _ = _http_bytes(html_url, accept="text/html,*/*;q=0.5")
    if not ok:
        return []
    text = data.decode("utf-8", errors="ignore")
    candidates: list[str] = []
    for m in re.finditer(r'href="([^"]+\.pdf)"', text):
        candidates.append(m.group(1))
    for m in re.finditer(r'src="([^"]+\.pdf)"', text):
        candidates.append(m.group(1))
    # Resolve relative URLs
    from urllib.parse import urljoin
    out = []
    for c in candidates:
        out.append(urljoin(html_url, c))
    # Deduplicate keeping order
    seen, dedup = set(), []
    for u in out:
        if u not in seen:
            seen.add(u)
            dedup.append(u)
    return dedup


def _try_urls(filename: str, urls: list[str]) -> tuple[bool, int, str, str]:
    """Try each URL in turn, return (ok, size, source_url, note)."""
    dest = TARGET_DIR / filename
    for url in urls:
        ok, size, note = _save_pdf(url, dest)
        if ok:
            return True, size, url, note
        # Polite backoff between attempts
        time.sleep(0.6)
    return False, 0, "", "all URL fallbacks failed"


# Targets: each entry is a list of candidate URLs to try in order.
TARGETS: list[tuple[str, str, list[str]]] = [
    # Frenez 2005 Lothal sealings - Zenodo record 5514282; also Zenodo 5513706 (Oman)
    (
        "frenez_2005_lothal_sealings.pdf",
        "Frenez 2005 Lothal sealings (Zenodo 5514282)",
        # URLs filled in via Zenodo API at runtime
        [],
    ),
    (
        "frenez_2020_indus_oman_trade.pdf",
        "Frenez 2020 'Indus Civilization Trade with Oman Peninsula' (Zenodo 5513706)",
        [],
    ),
    # HAL Failaka Vol 2 - needs viewer parse
    (
        "david-cuny_neyme_2016_failaka_seals_vol2.pdf",
        "David-Cuny & Neyme 2016 - Failaka Seals Vol 2 (HAL hal-01980283)",
        [
            "https://hal.science/hal-01980283/file/Failaka_Seals_Catalogue_Vol_2.pdf",
            "https://hal.science/hal-01980283/document",
            "https://hal.science/hal-01980283v1/document",
        ],
    ),
    # HAL Lombard 2015 review
    (
        "lombard_2015_failaka_vol1_review.pdf",
        "Lombard 2015 review of Failaka Seals Vol 1 (HAL halshs-01842487)",
        [
            "https://shs.hal.science/halshs-01842487/document",
            "https://shs.hal.science/halshs-01842487v1/document",
            "https://shs.hal.science/halshs-01842487/file/CR_Failaka_seals_vol1.pdf",
        ],
    ),
    # Vidale 2004 (already obtained, but include for idempotency)
    (
        "vidale_2004_melammu_iv_meluhha_villages.pdf",
        "Vidale 2004 'Growing in a Foreign World' (Melammu IV)",
        [
            "https://www.harappa.com/sites/default/files/201402/Vidale-Indus-Mesopotamia.pdf",
        ],
    ),
    # Levit 2010 (already obtained)
    (
        "levit_2010_meluhha_etymology_studia_orientalia.pdf",
        "Levit 2010 'The Ancient Mesopotamian Meluhha' (Studia Orientalia 112)",
        [
            "https://journal.fi/store/article/view/51787/16150",
            "https://journal.fi/store/article/download/51787/16150",
        ],
    ),
    # Internet Archive Crawford 2001 Saar - try a different IA mirror
    (
        "crawford_2001_early_dilmun_seals_saar.pdf",
        "Crawford 2001 Early Dilmun Seals from Saar",
        [
            "https://archive.org/download/EarlyDilmunSealsFromSaarH.Crawford/Early%20Dilmun%20Seals%20from%20Saar-H.%20crawford.pdf",
            "https://ia803109.us.archive.org/items/EarlyDilmunSealsFromSaarH.Crawford/Early%20Dilmun%20Seals%20from%20Saar-H.%20crawford.pdf",
        ],
    ),
    # Possehl 2006 Shu-ilishu - the canonical Penn Museum URL is the HTML article;
    # the article itself notes a "View PDF" link. Let's try both URL forms.
    (
        "possehl_2006_shu_ilishu_seal_expedition.pdf",
        "Possehl 2006 'Shu-ilishu's Cylinder Seal' (Penn Expedition 48:1)",
        [
            "https://www.penn.museum/sites/expedition/PDFs/48-1/Possehl.pdf",
            "https://www.penn.museum/documents/publications/expedition/PDFs/48-1/What%20in%20the%20World.pdf",
            "https://www.penn.museum/sites/expedition/?p=2538",
        ],
    ),
    # Frenez "Private Person or Public Persona" - Harappa.com PDF
    (
        "frenez_2018_private_person_public_persona.pdf",
        "Frenez 2018 'Private Person or Public Persona' (Walking with the Unicorn) - Harappa.com",
        [
            "https://www.harappa.com/sites/default/files/pdf/private-person.pdf",
        ],
    ),
]


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    print(f"Phase-22 contact-zone acquisition v2\nTarget dir: {TARGET_DIR}\n")
    manifest: dict[str, Any] = {"items": [], "fetched_at": int(time.time())}

    # Resolve Zenodo records
    print("Resolving Zenodo records...")
    zenodo_5514282 = _resolve_zenodo("5514282")
    zenodo_5513706 = _resolve_zenodo("5513706")
    print(f"  5514282 -> {len(zenodo_5514282)} files: {zenodo_5514282[:2]}")
    print(f"  5513706 -> {len(zenodo_5513706)} files: {zenodo_5513706[:2]}")

    n_ok = 0
    n_fail = 0
    n_skipped = 0
    for filename, desc, fallback_urls in TARGETS:
        urls = list(fallback_urls)
        if filename.startswith("frenez_2005_lothal_sealings"):
            urls = zenodo_5514282 + urls
        elif filename.startswith("frenez_2020_indus_oman_trade"):
            urls = zenodo_5513706 + urls

        # If HAL viewer - extract embedded PDF URLs
        extra_urls: list[str] = []
        for u in urls:
            if "hal.science" in u and "/document" in u:
                extra_urls.extend(_extract_hal_pdf_url(u))
        urls = urls + extra_urls

        dest = TARGET_DIR / filename
        if dest.exists() and dest.stat().st_size > 1024 and dest.read_bytes()[:4] == b"%PDF":
            n_skipped += 1
            print(f"  SKIP  {filename}  ({dest.stat().st_size} bytes, valid PDF)")
            manifest["items"].append({
                "filename": filename, "desc": desc,
                "size": dest.stat().st_size,
                "sha256": _sha256(dest.read_bytes()),
                "source_url": "(already on disk)",
                "status": "skipped",
            })
            continue

        # Remove invalid file from prior run
        if dest.exists():
            try:
                dest.unlink()
            except Exception:  # noqa: BLE001
                pass

        print(f"  TRY   {filename}  ({len(urls)} candidates)")
        ok, size, source_url, note = _try_urls(filename, urls)
        if ok:
            n_ok += 1
            sha = _sha256(dest.read_bytes())
            print(f"        -> OK {size} bytes from {source_url}")
            manifest["items"].append({
                "filename": filename, "desc": desc,
                "size": size, "sha256": sha,
                "source_url": source_url,
                "status": "fetched",
            })
        else:
            n_fail += 1
            print(f"        -> FAIL: {note}")
            manifest["items"].append({
                "filename": filename, "desc": desc,
                "size": 0, "sha256": "",
                "source_url": "",
                "status": "failed",
                "note": note,
                "tried_urls": urls,
            })
        time.sleep(0.5)

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nSummary: {n_ok} fetched, {n_skipped} already-present, {n_fail} failed.")
    print(f"Manifest: {MANIFEST_PATH}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
