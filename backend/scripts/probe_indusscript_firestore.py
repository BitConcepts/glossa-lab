"""Query indusscript.in Firestore directly via REST API.

We now know:
  - Backend: Cloud Firestore (NOT Realtime Database)
  - Project: theindusscript
  - Field names: textnum, posnum, inscobj, signnum, fsymbols (from bundle analysis)
  - Text numbering: 4-digit IM77 style (0001-9999)

Strategy:
  1. Anonymous Firebase Auth -> get idToken
  2. Query Firestore REST API with idToken
  3. Try candidate collection names: texts, LaunchDocuments, inscriptions, signs, etc.
  4. If collection found: dump all documents (paginated)

Firestore REST endpoint:
  https://firestore.googleapis.com/v1/projects/{project}/databases/(default)/documents/{collection}

Usage:
    shell.cmd python backend/scripts/probe_indusscript_firestore.py
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).parents[2]
OUT = REPO / "glossa-corpus" / "indus" / "sources" / "rmrl" / "raw" / "indusscript-probe"
OUT.mkdir(parents=True, exist_ok=True)

API_KEY = "AIzaSyDcdVosJjI2xFkLGrw5-TYhZLvCRquh8nM"
PROJECT = "theindusscript"
FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents"

# Candidate collection names from bundle analysis
CANDIDATE_COLLECTIONS = [
    "texts",           # most likely — primary field is 'textnum'
    "LaunchDocuments", # appears 3x in bundle
    "inscriptions",
    "signs",
    "sites",
    "concordance",
    "symbols",
    "fsymbols",
    "records",
    "texts_im77",
    "im77",
    "indus_texts",
    "corpus",
    "seals",
]


HEADERS = {
    "Referer": "https://indusscript.in/",
    "Origin": "https://indusscript.in",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0",
}

def http_post_json(url: str, body: dict) -> dict | None:
    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json", **HEADERS}
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read()[:200]}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def http_get_json(url: str, token: str | None = None) -> dict | None:
    headers = {**HEADERS}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read()[:300].decode("utf-8", errors="replace")
        print(f"  HTTP {e.code}: {body}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def get_anonymous_token() -> str | None:
    """Get Firebase anonymous auth token."""
    print("Getting anonymous Firebase auth token...")
    auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    result = http_post_json(auth_url, {"returnSecureToken": True})
    if result and "idToken" in result:
        token = result["idToken"]
        print(f"  Token acquired (uid: {result.get('localId', '?')})")
        return token
    print("  Failed to get anonymous token")
    return None


def try_collection(collection: str, token: str) -> dict | None:
    """Try to list documents in a Firestore collection."""
    url = f"{FIRESTORE_BASE}/{collection}?pageSize=5"
    result = http_get_json(url, token)
    return result


def dump_collection(collection: str, token: str, out_path: Path) -> int:
    """Dump all documents from a collection with pagination."""
    docs = []
    page_token = None
    page = 0

    while True:
        url = f"{FIRESTORE_BASE}/{collection}?pageSize=100"
        if page_token:
            url += f"&pageToken={page_token}"

        result = http_get_json(url, token)
        if not result:
            break

        batch = result.get("documents", [])
        docs.extend(batch)
        page += 1
        print(f"  Page {page}: {len(batch)} documents (total: {len(docs)})")

        page_token = result.get("nextPageToken")
        if not page_token or len(batch) == 0:
            break

    if docs:
        out_path.write_text(json.dumps({
            "_citation": {
                "primary_sources": ["I.6"],
                "derivation": f"Firestore collection '{collection}' via anonymous REST API. Project: theindusscript.",
            },
            "collection": collection,
            "total_documents": len(docs),
            "fetched_at": datetime.utcnow().isoformat(),
            "documents": docs,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  Saved: {out_path} ({len(docs)} docs)")

    return len(docs)


def main():
    print("=== indusscript.in Firestore REST API Probe ===")
    print(f"Project: {PROJECT}")
    print(f"Output: {OUT}")
    print()

    # Step 1: Get token
    token = get_anonymous_token()
    if not token:
        print("Cannot proceed without auth token.")
        return

    print()
    print("=== Testing candidate collection names ===")

    found_collections = []
    for coll in CANDIDATE_COLLECTIONS:
        print(f"  Testing: {coll} ... ", end="", flush=True)
        result = try_collection(coll, token)
        if result is None:
            print("403/404")
            continue

        # Check if we got actual documents or just an empty result
        docs = result.get("documents", [])
        if docs:
            print(f"FOUND! {len(docs)} documents in first page")
            found_collections.append((coll, len(docs)))
        elif "documents" in result:
            print(f"EXISTS (empty) — 0 documents")
            found_collections.append((coll, 0))
        elif result:
            # Got something — might be a different format
            keys = list(result.keys())[:5]
            print(f"RESPONSE: {keys}")
            found_collections.append((coll, -1))
        else:
            print("empty response")

    print()
    print("=== Results ===")
    if not found_collections:
        print("No collections accessible with anonymous token.")
        print()
        print("This confirms Firebase rules require authenticated (non-anonymous) user.")
        print("Next options:")
        print("  1. Contact RMRL for formal data export (already done)")
        print("  2. Install real Chrome: https://www.google.com/chrome/")
        print("     Then re-run probe_indusscript.py --phase C")
        print("  3. Use Chrome DevTools manually:")
        print("     a. Open https://indusscript.in in your regular Chrome")
        print("     b. Sign in with Google")
        print("     c. Open DevTools (F12) -> Network tab")
        print("     d. Click on some inscription records")
        print("     e. Look for requests to firestore.googleapis.com")
        print("     f. Note the collection name in the URL path")
    else:
        print(f"Found {len(found_collections)} accessible collection(s):")
        for coll, count in found_collections:
            print(f"  {coll}: {count} documents")
        print()

        # Dump all found collections
        for coll, count in found_collections:
            if count > 0:
                print(f"\nDumping collection: {coll}")
                out_path = OUT / f"firestore_{coll}.json"
                total = dump_collection(coll, token, out_path)
                print(f"  Total documents dumped: {total}")

    # Save probe report
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "project": PROJECT,
        "api_key_used": API_KEY[:20] + "...",
        "auth_method": "anonymous",
        "collections_tested": CANDIDATE_COLLECTIONS,
        "collections_found": found_collections,
        "note": "Anonymous auth — Firestore rules may deny reads even with valid token",
    }
    (OUT / "firestore_probe_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(f"\nReport: {OUT / 'firestore_probe_report.json'}")


if __name__ == "__main__":
    main()
