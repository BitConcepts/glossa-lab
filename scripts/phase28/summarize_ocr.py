"""Phase-28 helper: summarize Mistral OCR extractions from CISI Vol 3 Part 3."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def main() -> None:
    p = Path(__file__).resolve().parents[2] / "reports" / "cisi_vol3_extracted_signs.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    print(f"Total entries: {len(data)}")
    types = Counter(e.get("type", "?") for e in data)
    print(f"Types: {dict(types)}")
    print()
    print("=== Seals (with raw 'signs' field) ===")
    for e in data:
        if e.get("type") == "seal":
            print(f"  page={e.get('page')} | {e.get('seal_id')} | signs: {e.get('signs', '')[:100]}")
    print()
    print("=== Sign references ===")
    for e in data:
        if e.get("type") == "sign_ref":
            print(f"  page={e.get('page')} | {e.get('sign_id')} | meaning: {e.get('meaning', '')[:100]}")
    print()
    print("=== Iconography ===")
    for e in data:
        if e.get("type") == "iconography":
            print(f"  page={e.get('page')} | {e.get('seal_id')} | motif: {e.get('motif', '')[:100]}")


if __name__ == "__main__":
    main()
