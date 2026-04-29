"""Scrape the entire DAMOS corpus via /ajaxitem/<id>/ endpoint.

DAMOS is an annotated electronic corpus of all published Mycenaean (Linear B)
texts (~5998 records). The React frontend at https://damos.hf.uio.no fetches
each inscription via GET /ajaxitem/<id>/ which returns a JSON object containing:
    item:       {collectionid, heading, content, series, subseries, year,
                 context, chronology1, ...}
    notes/bibliography/etc. nested objects

This script:
  1. Iterates id = 1..MAX (configurable; defaults to 6000) and tries each.
  2. Stops when 20 consecutive 500 errors are seen (signals we've passed the
     real corpus end).
  3. Throttles to ~5 req/s to be polite to the academic server.
  4. Stores raw JSON per record under corpora/damos/raw/{id}.json
  5. Builds aggregated outputs:
        corpora/damos/damos_inscriptions.csv  -- one row per inscription
        corpora/damos/damos_signs.txt         -- one inscription per line, signs
                                                 space-separated (CSV-friendly)

Run:
    py scripts/phase17/scrape_damos.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
import ssl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "corpora" / "damos" / "raw"
OUT_DIR = ROOT / "corpora" / "damos"
SIGNS_OUT = OUT_DIR / "damos_signs.txt"
CSV_OUT = OUT_DIR / "damos_inscriptions.csv"

API = "https://damos.hf.uio.no/ajaxitem/{id}/"
UA = {"User-Agent": "Mozilla/5.0 (academic research bot, CC-BY-NC-SA dataset)"}

MAX_ID = 6000
STOP_AFTER_CONSECUTIVE_500S = 25
MIN_DELAY_S = 0.2  # ~5 req/s

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def fetch_id(id_: int) -> dict | None:
    """Return parsed JSON for a single ID, or None on failure."""
    req = urllib.request.Request(API.format(id=id_), headers=UA)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return {"_error": "HTTP", "_status": e.code}
    except Exception as e:
        return {"_error": type(e).__name__, "_status": str(e)}
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        # Not all responses are pure JSON (some return HTML on error)
        return {"_error": "JSONDecodeError", "_body_first200": body[:200]}


# Sign extraction: split DAMOS .content field on whitespace + DAMOS line markers
LINE_MARKER_RE = re.compile(r"^\s*\.[a-z0-9'\.]+\s*", re.MULTILINE)
PUNCT_DROP = set([",", ";", ":", ".", "...", "/", "\\", "|", "[", "]", "<", ">", "(", ")", "<\\", ">\\"])


def extract_signs(content: str) -> list[str]:
    """Tokenize the DAMOS content field into a list of Linear B sign tokens.
    Linear B uses dash-separated syllabograms (e.g., "de-u-ki-jo-jo") plus
    logograms (uppercase like OLE, TELA;2) and numbers."""
    if not content:
        return []
    # Decode the JSON-style escapes that may remain
    content = content.replace("\\n", "\n").replace("\\/", "/")
    # Strip line markers like ".1", ".2", ".a", ".b"
    content = LINE_MARKER_RE.sub(" ", content)
    # Split on whitespace
    out = []
    for tok in content.split():
        # Remove enclosing brackets / damage markers but keep the token
        t = tok.strip("[]<>()")
        # Replace internal damage characters that don't carry sign-shape info
        t = t.rstrip("#?!")
        if not t or t in PUNCT_DROP:
            continue
        out.append(t)
    return out


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    n_ok = 0
    n_err = 0
    consec_500s = 0
    rows = []
    start = time.time()

    with SIGNS_OUT.open("w", encoding="utf-8") as sigs_fh, \
         CSV_OUT.open("w", encoding="utf-8", newline="") as csv_fh:
        csv_w = csv.DictWriter(csv_fh, fieldnames=[
            "id", "heading", "series", "subseries", "set", "tablenumber",
            "provenience", "year", "context", "chronology1", "n_signs",
            "signs_ws_joined",
        ])
        csv_w.writeheader()

        for id_ in range(1, MAX_ID + 1):
            raw_path = RAW_DIR / f"{id_}.json"
            if raw_path.exists() and raw_path.stat().st_size > 50:
                # Resume support: load from cache
                try:
                    data = json.loads(raw_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    data = fetch_id(id_)
            else:
                data = fetch_id(id_)
                time.sleep(MIN_DELAY_S)

            if data and "_error" in data:
                if data.get("_status") == 500 or data.get("_status") == "HTTP Error 500":
                    consec_500s += 1
                    if consec_500s >= STOP_AFTER_CONSECUTIVE_500S:
                        print(f"  Hit {consec_500s} consecutive 500s -- stopping at id={id_}", file=sys.stderr)
                        break
                else:
                    consec_500s = 0  # other errors don't count
                n_err += 1
                continue

            consec_500s = 0
            n_ok += 1
            # Save raw
            try:
                raw_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass

            item = data.get("item", {}) if isinstance(data, dict) else {}
            content = item.get("content", "") or ""
            signs = extract_signs(content)
            row = {
                "id": id_,
                "heading": item.get("heading", ""),
                "series": item.get("series", ""),
                "subseries": item.get("subseries", ""),
                "set": item.get("set", ""),
                "tablenumber": item.get("tablenumber", ""),
                "provenience": item.get("provenience", ""),
                "year": item.get("year", ""),
                "context": item.get("context", ""),
                "chronology1": item.get("chronology1", ""),
                "n_signs": len(signs),
                "signs_ws_joined": " ".join(signs),
            }
            csv_w.writerow(row)
            sigs_fh.write(" ".join(signs) + "\n")

            if id_ % 100 == 0:
                elapsed = time.time() - start
                eta = (elapsed / id_) * (MAX_ID - id_)
                print(f"  id={id_}  ok={n_ok}  err={n_err}  elapsed={elapsed:.0f}s  eta={eta:.0f}s",
                      file=sys.stderr)

    print(f"\nDone. ok={n_ok}  err={n_err}", file=sys.stderr)
    print(f"  CSV:    {CSV_OUT}", file=sys.stderr)
    print(f"  Signs:  {SIGNS_OUT}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
