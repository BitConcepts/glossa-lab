"""Dump indusscript.in indusarrays Firestore collection.

Full pagination dump of all ~5,473 Indus inscription records.

Usage:
    shell.cmd python backend/scripts/dump_indusscript_firestore.py --token TOKEN

Fields confirmed from Live query payload:
  texts   - array of sign IDs (strings, e.g. "342", "0342")
  posnum  - position number
  textnum - IM77 text number

_citation:
  primary_sources: ["I.6"]
  derivation: "indusarrays Firestore collection from indusscript.in.
               App by RMRL / Iravatham Mahadevan (2021).
               Data: Mahadevan, I. (1977). The Indus Script: Texts, Concordance
               and Tables. ASI Memoirs No.77. New Delhi.
               Accessed via Firebase Auth + REST API with user permission."
"""
from __future__ import annotations
import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parents[2]
OUT = REPO / "glossa-corpus" / "indus" / "sources" / "rmrl" / "raw" / "indusscript-probe"
OUT.mkdir(parents=True, exist_ok=True)

PROJECT = "theindusscript"
COLLECTION = "indusarrays"
FIRESTORE_BASE = (
    f"https://firestore.googleapis.com/v1/projects/{PROJECT}"
    f"/databases/(default)/documents"
)


def get_page(token: str, page_size: int = 300, page_token: str | None = None) -> dict | None:
    url = f"{FIRESTORE_BASE}/{COLLECTION}?pageSize={page_size}"
    if page_token:
        url += f"&pageToken={page_token}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Referer": "https://indusscript.in/",
        "Origin": "https://indusscript.in",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read()[:500].decode("utf-8", errors="replace")
        print(f"  HTTP {e.code}: {body}")
        return None
    except Exception as exc:
        print(f"  Error: {exc}")
        return None


def parse_firestore_value(val: dict) -> object:
    """Convert a Firestore REST API value object to a Python value."""
    if "stringValue" in val:
        return val["stringValue"]
    if "integerValue" in val:
        return int(val["integerValue"])
    if "doubleValue" in val:
        return float(val["doubleValue"])
    if "booleanValue" in val:
        return val["booleanValue"]
    if "nullValue" in val:
        return None
    if "arrayValue" in val:
        return [parse_firestore_value(v) for v in val["arrayValue"].get("values", [])]
    if "mapValue" in val:
        return {k: parse_firestore_value(v) for k, v in val["mapValue"].get("fields", {}).items()}
    if "referenceValue" in val:
        return val["referenceValue"]
    if "timestampValue" in val:
        return val["timestampValue"]
    return str(val)


def parse_doc(raw_doc: dict) -> dict:
    """Convert a raw Firestore document to a clean Python dict."""
    name = raw_doc.get("name", "")
    doc_id = name.split("/")[-1] if name else ""
    fields = raw_doc.get("fields", {})
    clean = {"_id": doc_id, "_ref": name}
    for field_name, field_val in fields.items():
        clean[field_name] = parse_firestore_value(field_val)
    return clean


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True, help="Firebase ID token from browser console")
    parser.add_argument("--page-size", type=int, default=300)
    args = parser.parse_args()

    token = args.token.strip()
    print(f"=== Dumping indusscript.in / Firestore / {COLLECTION} ===")
    print(f"Output: {OUT}")
    print()

    all_docs = []
    page_token = None
    page_num = 0
    start = time.time()

    while True:
        page_num += 1
        print(f"  Page {page_num}... ", end="", flush=True)
        result = get_page(token, args.page_size, page_token)

        if result is None:
            print("FAILED")
            print("Token may have expired. Re-run with a fresh token.")
            break

        raw_docs = result.get("documents", [])
        parsed = [parse_doc(d) for d in raw_docs]
        all_docs.extend(parsed)
        elapsed = time.time() - start
        print(f"{len(raw_docs)} docs | total: {len(all_docs)} | {elapsed:.0f}s")

        page_token = result.get("nextPageToken")
        if not page_token or len(raw_docs) == 0:
            print(f"\n  Pagination complete.")
            break

        time.sleep(0.2)  # polite rate limiting

    print(f"\n=== Dump complete: {len(all_docs)} documents ===")

    if not all_docs:
        print("No documents retrieved. Token may have expired or collection is empty.")
        return 1

    # Analyze the data
    sample = all_docs[:3]
    fields_seen = set()
    for doc in all_docs[:100]:
        fields_seen.update(k for k in doc.keys() if not k.startswith("_"))
    print(f"Fields found: {sorted(fields_seen)}")

    textnum_vals = [d.get("textnum") for d in all_docs if d.get("textnum") is not None]
    if textnum_vals:
        print(f"textnum range: {min(textnum_vals)} – {max(textnum_vals)}")

    # Save full dump
    out_path = OUT / f"firestore_indusarrays_full.json"
    out_path.write_text(json.dumps({
        "_citation": {
            "primary_sources": ["I.6"],
            "derivation": (
                "Complete dump of indusscript.in Firestore collection 'indusarrays'. "
                "App: RMRL / Mahadevan (2021). Data: Mahadevan 1977 IM77 concordance. "
                "Accessed 2026-05-14 via authenticated Firebase REST API with user permission."
            ),
        },
        "collection": COLLECTION,
        "project": PROJECT,
        "total_documents": len(all_docs),
        "fields": sorted(fields_seen),
        "fetched_at": datetime.utcnow().isoformat(),
        "documents": all_docs,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved: {out_path}")
    print(f"Size: {out_path.stat().st_size // 1024:,} KB")

    # Also save as JSONL for pipeline
    jsonl_path = OUT / f"firestore_indusarrays_full.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for doc in all_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    print(f"JSONL: {jsonl_path}")

    # Sample output
    print(f"\nSample documents (first 2):")
    for doc in sample[:2]:
        print(f"  {json.dumps(doc, ensure_ascii=False)[:300]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
