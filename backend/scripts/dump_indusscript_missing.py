"""Probe indusscript.in Firestore for texts missing from first dump.

First dump got textnums 1001-9905 (2,906 unique texts = 56% of ICIT).
This script:
1. Uses Firestore runQuery to find texts with textnum < 1001 (likely 1-999)
2. Probes additional collection names that might contain the rest
3. Tries a full runQuery ordered by textnum to find any we missed

Usage:
    shell.cmd python backend/scripts/dump_indusscript_missing.py --token TOKEN
"""
from __future__ import annotations
import argparse, json, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parents[2]
OUT = REPO / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe"
OUT.mkdir(parents=True, exist_ok=True)
PROJECT = "theindusscript"
DB = f"projects/{PROJECT}/databases/(default)"
FIRESTORE = f"https://firestore.googleapis.com/v1/{DB}"

ADDITIONAL_COLLECTIONS = [
    "indusarrays2", "indusarray", "texts", "textarrays",
    "concordance", "signarr", "signarray", "inscriptions",
    "indus", "mahadevan", "im77texts", "textlist",
]

def headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Referer": "https://indusscript.in/",
        "Origin": "https://indusscript.in",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

def get(url: str, token: str) -> dict | None:
    req = urllib.request.Request(url, headers=headers(token))
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read()[:200].decode('utf-8','replace')}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def post(url: str, body: dict, token: str) -> dict | None:
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=headers(token))
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read()[:300].decode('utf-8','replace')}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def parse_val(v: dict):
    if "integerValue" in v: return int(v["integerValue"])
    if "stringValue" in v: return v["stringValue"]
    if "arrayValue" in v: return [parse_val(x) for x in v["arrayValue"].get("values", [])]
    if "doubleValue" in v: return float(v["doubleValue"])
    if "booleanValue" in v: return v["booleanValue"]
    if "nullValue" in v: return None
    return str(v)

def parse_doc(raw: dict) -> dict:
    name = raw.get("name", "")
    doc = {"_id": name.split("/")[-1], "_ref": name}
    for k, v in raw.get("fields", {}).items():
        doc[k] = parse_val(v)
    return doc

def run_structured_query(token: str, collection: str, field: str, op: str, value: int, limit: int = 300) -> list[dict]:
    """Run a Firestore structured query with a filter."""
    url = f"{FIRESTORE}/documents:runQuery"
    body = {
        "structuredQuery": {
            "from": [{"collectionId": collection}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": field},
                    "op": op,
                    "value": {"integerValue": str(value)}
                }
            },
            "orderBy": [{"field": {"fieldPath": field}, "direction": "ASCENDING"}],
            "limit": limit,
        }
    }
    result = post(url, body, token)
    if not result:
        return []
    docs = []
    for item in result:
        if "document" in item:
            docs.append(parse_doc(item["document"]))
    return docs

def probe_collection(token: str, coll: str, page_size: int = 5) -> bool:
    """Check if a collection exists and has documents. Returns True if found."""
    url = f"{FIRESTORE}/documents/{coll}?pageSize={page_size}"
    result = get(url, token)
    if result is None:
        return False
    docs = result.get("documents", [])
    if docs:
        print(f"  FOUND: {coll} — {len(docs)} docs in first page")
        return True
    if "documents" in result:
        print(f"  EXISTS (empty): {coll}")
        return True
    return False

def dump_collection(token: str, coll: str, page_size: int = 300) -> list[dict]:
    """Full pagination dump of a collection."""
    all_docs, page_token, page = [], None, 0
    while True:
        url = f"{FIRESTORE}/documents/{coll}?pageSize={page_size}"
        if page_token:
            url += f"&pageToken={page_token}"
        result = get(url, token)
        if not result:
            break
        batch = [parse_doc(d) for d in result.get("documents", [])]
        all_docs.extend(batch)
        page += 1
        print(f"  Page {page}: {len(batch)} docs (total: {len(all_docs)})")
        page_token = result.get("nextPageToken")
        if not page_token or not batch:
            break
        time.sleep(0.2)
    return all_docs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True)
    args = parser.parse_args()
    token = args.token.strip()

    print("=== indusscript.in — Missing Text Probe ===")
    all_new_docs = []

    # 1. Query indusarrays for textnum < 1001 (IM77 lower-numbered texts)
    print("\n[1] Querying indusarrays where textnum < 1001...")
    low_docs = run_structured_query(token, "indusarrays", "textnum", "LESS_THAN", 1001, limit=1000)
    print(f"  Found: {len(low_docs)} docs with textnum < 1001")
    if low_docs:
        textnums = set(d.get("textnum") for d in low_docs if d.get("textnum") is not None)
        print(f"  Unique textnums: {len(textnums)}, range: {min(textnums)}-{max(textnums)}")
        all_new_docs.extend(low_docs)

    # 2. Query indusarrays for textnum > 9905 (might be more beyond our range)
    print("\n[2] Querying indusarrays where textnum > 9905...")
    high_docs = run_structured_query(token, "indusarrays", "textnum", "GREATER_THAN", 9905, limit=1000)
    print(f"  Found: {len(high_docs)} docs with textnum > 9905")
    if high_docs:
        textnums = set(d.get("textnum") for d in high_docs if d.get("textnum") is not None)
        print(f"  Unique textnums: {len(textnums)}, range: {min(textnums)}-{max(textnums)}")
        all_new_docs.extend(high_docs)

    # 3. Probe additional collections
    print("\n[3] Probing additional collection names...")
    found_new = []
    for coll in ADDITIONAL_COLLECTIONS:
        print(f"  {coll}... ", end="", flush=True)
        if probe_collection(token, coll):
            found_new.append(coll)
        else:
            print("  not found")
        time.sleep(0.1)

    # 4. Dump any newly found collections
    for coll in found_new:
        print(f"\n[4] Dumping {coll}...")
        docs = dump_collection(token, coll)
        if docs:
            out = OUT / f"firestore_{coll}_extra.json"
            out.write_text(json.dumps({
                "_citation": {"primary_sources": ["I.6", "A.1"],
                              "derivation": f"Additional Firestore collection '{coll}' from indusscript.in."},
                "collection": coll, "total": len(docs),
                "fetched_at": datetime.utcnow().isoformat(),
                "documents": docs
            }, indent=2), encoding="utf-8")
            print(f"  Saved: {out} ({len(docs)} docs)")
            all_new_docs.extend(docs)

    # 5. Save all new docs
    if all_new_docs:
        out = OUT / "firestore_missing_texts.json"
        out.write_text(json.dumps({
            "_citation": {"primary_sources": ["I.6", "A.1"]},
            "total": len(all_new_docs),
            "fetched_at": datetime.utcnow().isoformat(),
            "documents": all_new_docs
        }, indent=2), encoding="utf-8")
        print(f"\nTotal new documents: {len(all_new_docs)}")
        print(f"Saved: {out}")

        # Unique textnums
        tn = set(d.get("textnum") for d in all_new_docs if d.get("textnum") is not None)
        print(f"New unique textnums: {len(tn)}")
        if tn:
            print(f"Range: {min(tn)} – {max(tn)}")
    else:
        print("\nNo new documents found beyond the original 2,906 texts.")
        print("The indusscript.in concordance appears to contain only 2,906 IM77 texts.")
        print("Remaining ~2,600 ICIT texts are likely:")
        print("  1. In CISI volumes not digitized in indusscript.in")
        print("  2. Texts numbered outside 1001-9905 that weren't in the app")
        print("  3. Texts requiring CISI purchase to access")

    print("\nDone.")

if __name__ == "__main__":
    import sys; sys.exit(main())
