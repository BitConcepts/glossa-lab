#!/usr/bin/env python3
"""Route 2 — Firestore `indusarrays` read script (re-authored 2026-10-25).

Implements Part 3B of the Route 2 recovery procedure
(files/2026-10-24-route2-indusarrays-recovery.md). The original May 2026
dump script is lost; this is its replacement.

WHAT IT DOES
  Reads the `indusarrays` collection of Firebase project `theindusscript`
  through the Firestore REST API, paging at 300 documents, unwraps
  Firestore typed values into plain values, and writes the two recovery
  artifacts into the output directory:

    firestore_indusarrays_full.json   {"documents": [...], "fields": [...]}
    firestore_indusarrays_full.jsonl  one document per line

  Each document gains `_id` from the final segment of its REST `name`.

TOKEN DISCIPLINE (read before use)
  Live mode needs a Firebase Auth ID token from the OWNER'S signed-in
  indusscript.in session on the OWNER'S machine (the May 2026 method:
  DevTools console on the signed-in site). The token is read from the
  environment variable ROUTE2_FIRESTORE_TOKEN, is used only as the
  Authorization header of these requests, and is never printed, logged,
  or written to any file by this script. It never leaves the machine
  the owner is signed in on. Do not paste it into chat, email, or a
  file that syncs anywhere.

SHAPE CHECK (Part 3B: prove on one page before the full read)
  Page 1 must satisfy, for EVERY document: keys `dockey`, `sideline`,
  `texts`, and every one of `S1`..`S14` present in the document's
  fields. If page 1 fails, the script halts with SHAPE-FAIL, writes no
  artifacts, and exits 2. No retries under a different shape.

MODES
  live:     python3 route2_firestore_read.py live --out DIR
            (ROUTE2_FIRESTORE_TOKEN must be set in the environment)
  fixture:  python3 route2_firestore_read.py fixture --pages DIR --out DIR
            Reads saved REST page responses (page1.json, page2.json, ...
            in order) from DIR instead of the network. Used to prove
            the unwrap/paging/shape logic offline. No token needed.

Exit codes: 0 = artifacts written; 2 = shape failure; 3 = usage/IO error.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

PROJECT = "theindusscript"
COLLECTION = "indusarrays"
PAGE_SIZE = 300
BASE = (
    f"https://firestore.googleapis.com/v1/projects/{PROJECT}"
    f"/databases/(default)/documents/{COLLECTION}"
)
S_FIELDS = [f"S{i}" for i in range(1, 15)]
REQUIRED_KEYS = ["dockey", "sideline", "texts"] + S_FIELDS


def unwrap(value):
    """Firestore REST typed value -> plain Python value."""
    if not isinstance(value, dict) or len(value) != 1:
        return value
    (kind, raw), = value.items()
    if kind == "stringValue":
        return raw
    if kind == "integerValue":
        return int(raw)
    if kind == "doubleValue":
        return float(raw)
    if kind == "booleanValue":
        return bool(raw)
    if kind == "nullValue":
        return None
    if kind == "arrayValue":
        return [unwrap(v) for v in raw.get("values", [])]
    if kind == "mapValue":
        return {k: unwrap(v) for k, v in raw.get("fields", {}).items()}
    # timestampValue / referenceValue / geoPointValue: keep as string/dict
    return raw


def unwrap_document(doc: dict) -> dict:
    fields = doc.get("fields", {})
    out = {k: unwrap(v) for k, v in fields.items()}
    name = doc.get("name", "")
    if name:
        out["_id"] = name.rstrip("/").split("/")[-1]
    return out


def shape_check(documents: list[dict]) -> list[str]:
    """Return a list of shape violations for a page of RAW documents."""
    problems = []
    if not documents:
        return ["page contains no documents"]
    for idx, doc in enumerate(documents):
        fields = doc.get("fields", {})
        for key in REQUIRED_KEYS:
            if key not in fields:
                problems.append(f"document {idx}: missing field '{key}'")
    return problems


def fetch_page_live(page_token: str | None, token: str) -> dict:
    url = f"{BASE}?pageSize={PAGE_SIZE}"
    if page_token:
        url += f"&pageToken={page_token}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def collect_live(token: str) -> list[dict]:
    pages, page_token = [], None
    while True:
        page = fetch_page_live(page_token, token)
        docs = page.get("documents", [])
        if not pages:
            problems = shape_check(docs)
            if problems:
                print("SHAPE-FAIL on page 1:", file=sys.stderr)
                for p in problems[:20]:
                    print(f"  {p}", file=sys.stderr)
                sys.exit(2)
        pages.append(page)
        page_token = page.get("nextPageToken")
        if not page_token:
            return pages


def collect_fixture(pages_dir: Path) -> list[dict]:
    files = sorted(pages_dir.glob("page*.json"))
    if not files:
        print(f"no page*.json files in {pages_dir}", file=sys.stderr)
        sys.exit(3)
    pages = []
    for i, f in enumerate(files):
        page = json.loads(f.read_text(encoding="utf-8"))
        if i == 0:
            problems = shape_check(page.get("documents", []))
            if problems:
                print("SHAPE-FAIL on page 1:", file=sys.stderr)
                for p in problems[:20]:
                    print(f"  {p}", file=sys.stderr)
                sys.exit(2)
        pages.append(page)
    return pages


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in ("live", "fixture"):
        print(__doc__)
        return 3
    mode = argv[1]
    out_dir = None
    pages_dir = None
    args = argv[2:]
    while args:
        if args[0] == "--out" and len(args) > 1:
            out_dir = Path(args[1]); args = args[2:]
        elif args[0] == "--pages" and len(args) > 1:
            pages_dir = Path(args[1]); args = args[2:]
        else:
            print(f"unknown argument: {args[0]}", file=sys.stderr)
            return 3
    if out_dir is None:
        print("--out DIR is required", file=sys.stderr)
        return 3

    if mode == "live":
        token = os.environ.get("ROUTE2_FIRESTORE_TOKEN", "")
        if not token:
            print("ROUTE2_FIRESTORE_TOKEN is not set — the owner's session "
                  "token must be in the environment of this invocation, "
                  "on the owner's machine only.", file=sys.stderr)
            return 3
        pages = collect_live(token)
    else:
        if pages_dir is None:
            print("--pages DIR is required in fixture mode", file=sys.stderr)
            return 3
        pages = collect_fixture(pages_dir)

    documents = []
    field_names = set()
    for page in pages:
        for raw_doc in page.get("documents", []):
            field_names.update(raw_doc.get("fields", {}).keys())
            documents.append(unwrap_document(raw_doc))

    out_dir.mkdir(parents=True, exist_ok=True)
    companion = {"documents": documents, "fields": sorted(field_names)}
    (out_dir / "firestore_indusarrays_full.json").write_text(
        json.dumps(companion, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(out_dir / "firestore_indusarrays_full.jsonl", "w", encoding="utf-8") as fh:
        for doc in documents:
            fh.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"pages: {len(pages)}  documents: {len(documents)}  "
          f"fields: {len(field_names)}")
    print(f"wrote: {out_dir / 'firestore_indusarrays_full.json'}")
    print(f"wrote: {out_dir / 'firestore_indusarrays_full.jsonl'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
