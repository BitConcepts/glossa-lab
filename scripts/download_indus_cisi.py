#!/usr/bin/env python3
"""Download the Indus CISI corpus from mayig/indus-valley-script-corpus.

Source: https://github.com/mayig/indus-valley-script-corpus (MIT License)
Saves 179 inscription JSON files as a single combined JSON to data/.

Usage:
    python scripts/download_indus_cisi.py

The script retries on failure and uses a realistic User-Agent to avoid
GitHub raw content serving issues (some Python urlopeners get 406 blocked).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

_REPO    = Path(__file__).resolve().parents[1]
_OUT     = _REPO / "data" / "indus_cisi_corpus.json"
_BASE_URL = "https://raw.githubusercontent.com/mayig/indus-valley-script-corpus/main"
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# All 179 inscription file paths (as of April 2026 — add new paths when repo updates)
_PATHS: list[str] = [
    # m001–m099
    *[f"corpus/m001_m099/m{i:03d}.json" for i in
      [1,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,
       28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,
       50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,
       72,73,74,75,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,
       95,96,97,98,99]],
    # m100–m184
    *[f"corpus/m100_m199/m{i:03d}.json" for i in
      [100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,
       117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,
       134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,
       151,152,153,154,155,157,158,159,160,161,162,163,164,165,166,167,169,
       170,171,172,173,174,175,176,177,178,179,180,181,182,183,184]],
]


def _fetch_json(url: str, retries: int = 3) -> object:
    """Fetch JSON from URL with retries and realistic User-Agent."""
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": _UA})
            with urlopen(req, timeout=15) as r:
                return json.loads(r.read().decode("utf-8"))
        except (URLError, json.JSONDecodeError) as exc:
            if attempt < retries - 1:
                time.sleep(1.5 ** attempt)
            else:
                raise exc


def main() -> None:
    _OUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {len(_PATHS)} inscription files from mayig/indus-valley-script-corpus...")

    all_inscriptions: list[dict] = []
    failed: list[str] = []

    for i, path in enumerate(_PATHS, 1):
        url = f"{_BASE_URL}/{path}"
        try:
            data = _fetch_json(url)
            if isinstance(data, list):
                all_inscriptions.extend(data)
            else:
                all_inscriptions.append(data)
            if i % 20 == 0:
                print(f"  {i}/{len(_PATHS)} files downloaded, {len(all_inscriptions)} inscriptions so far")
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {path}: {exc}", file=sys.stderr)
            failed.append(path)

    print(f"\nDownloaded {len(_PATHS) - len(failed)}/{len(_PATHS)} files")
    print(f"Total inscriptions: {len(all_inscriptions)}")

    if failed:
        print(f"Failed ({len(failed)}):", file=sys.stderr)
        for f in failed:
            print(f"  {f}", file=sys.stderr)

    _OUT.write_text(json.dumps(all_inscriptions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved → {_OUT}")

    # Quick stats
    all_signs = [g["id"] for insc in all_inscriptions for g in (insc.get("graphemes") or [])]
    print(f"Stats: {len(all_inscriptions)} inscription sides, {len(all_signs)} sign tokens")


if __name__ == "__main__":
    main()
