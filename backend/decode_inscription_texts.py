"""Decode OCR'd Mahadevan inscription glyphs to Fuls sign numbers.

The inscription plate pages (39-162) were OCR'd to produce text like:
    |  1001 | 100101 | U¥¥¥¥  |
The third column contains the sign sequence rendered via Mahadevan's
custom font, OCR'd as various Unicode characters.

Strategy (same rank-correlation we used for bigrams):
  1. Parse all ocr_texts_*.txt files, extract sign character sequences
  2. Count frequency of each character across all inscriptions
  3. Load Fuls (2023) catalog sign frequencies (real_indus_catalog_analysis.json)
  4. Match by rank order (most-frequent OCR char = most-frequent Fuls sign)
  5. Also incorporate existing cjk_m77_mapping.json for any direct matches
  6. Output decoded sequences to reports/mahadevan_texts_decoded.json
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).parent.parent
_OCR_DIR = _REPO / "data-import" / "mahadevan_ocr"
_REPORTS = _REPO / "reports"
sys.path.insert(0, str(Path(__file__).parent))


# ── Step 1: Parse inscription text OCR files ──────────────────────────


def parse_ocr_texts() -> list[dict]:
    """Extract inscription entries from ocr_texts_*.txt files.

    Format: | NNNN | SITECODE | SIGN_SEQUENCE |
    Returns list of {id, site_code, raw_chars} dicts.
    """
    entries = []
    seen_ids: set[int] = set()

    for txt_file in sorted(_OCR_DIR.glob("ocr_texts_*.txt")):
        text = txt_file.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            # Expect at least 3 non-empty parts: id, site_code, sign_chars
            parts = [p for p in parts if p]
            if len(parts) < 3:
                continue
            id_str, site_code, sign_str = parts[0], parts[1], parts[2]
            if not id_str.isdigit() or not (1000 <= int(id_str) <= 9999):
                continue
            insc_id = int(id_str)
            if insc_id in seen_ids:
                continue
            seen_ids.add(insc_id)
            # Clean sign string: remove whitespace, special table chars
            signs = sign_str.replace(" ", "").replace("°", "").replace("(", "").replace(")", "")
            if signs:
                entries.append({"id": insc_id, "site_code": site_code, "raw": signs})

    return sorted(entries, key=lambda x: x["id"])


# ── Step 2: Build glyph frequency map ────────────────────────────────


def build_glyph_freq(entries: list[dict]) -> Counter:
    """Count how often each glyph character appears across all inscriptions."""
    freq: Counter = Counter()
    for e in entries:
        for char in e["raw"]:
            freq[char] += 1
    return freq


# ── Step 3: Load Fuls catalog sign frequencies ────────────────────────


def load_fuls_sign_freq() -> list[tuple[str, int]]:
    """Return [(fuls_sign_id, frequency), ...] sorted by frequency desc."""
    p = _REPORTS / "real_indus_catalog_analysis.json"
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    # The catalog has top TMK signs by total count — use those as anchor
    signs = []
    # Use sign stats if available; fall back to TMK list
    for entry in data.get("tmk_signs", []):
        signs.append((str(entry["sign"]), entry["total"]))
    for entry in data.get("initial_signs", []):
        if not any(s[0] == str(entry["sign"]) for s in signs):
            signs.append((str(entry["sign"]), entry["total"]))
    return sorted(signs, key=lambda x: -x[1])


# ── Step 4: Load existing CJK-to-Fuls mapping ────────────────────────


def load_existing_mapping() -> dict[str, str]:
    """Load cjk_m77_mapping.json: char -> fuls_id."""
    p = _REPORTS / "cjk_m77_mapping.json"
    if not p.exists():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    mapping = data.get("mapping", data)
    result: dict[str, str] = {}
    for char, info in mapping.items():
        if isinstance(info, dict) and info.get("fuls"):
            result[char] = str(info["fuls"]).zfill(3)
    return result


# ── Step 5: Rank-correlate unmapped glyphs ───────────────────────────


def build_full_mapping(
    glyph_freq: Counter,
    fuls_freq: list[tuple[str, int]],
    existing: dict[str, str],
) -> dict[str, dict]:
    """Build char -> {fuls, confidence} mapping for inscription glyphs."""
    mapping: dict[str, dict] = {}

    # First: direct matches from existing CJK mapping
    for char, fuls in existing.items():
        if char in glyph_freq:
            mapping[char] = {"fuls": fuls, "confidence": "direct"}

    # Second: rank-correlation for unmapped glyphs
    unmapped_by_freq = [
        (char, cnt) for char, cnt in glyph_freq.most_common()
        if char not in mapping and len(char.strip()) > 0 and char not in ("∅", "?", "-", "·")
    ]
    fuls_unmatched = [
        (fid, cnt) for fid, cnt in fuls_freq
        if fid not in {v["fuls"] for v in mapping.values()}
    ]

    for (char, _), (fuls, _) in zip(unmapped_by_freq, fuls_unmatched):
        mapping[char] = {"fuls": fuls, "confidence": "rank_corr"}

    return mapping


# ── Step 6: Decode sequences ──────────────────────────────────────────


def decode_entries(
    entries: list[dict],
    char_map: dict[str, dict],
) -> list[dict]:
    """Apply mapping to produce decoded sign sequences."""
    decoded = []
    for e in entries:
        seq = []
        for char in e["raw"]:
            info = char_map.get(char)
            if info:
                seq.append(info["fuls"])
            # else: skip unmapped characters (often noise)
        if seq:
            decoded.append({
                "id": e["id"],
                "site_code": e["site_code"],
                "sequence": seq,
                "length": len(seq),
                "raw": e["raw"],
            })
    return decoded


# ── Main ──────────────────────────────────────────────────────────────


def main() -> None:
    print("[1/5] Parsing inscription OCR text files...")
    entries = parse_ocr_texts()
    print(f"      {len(entries)} unique inscriptions found")

    print("[2/5] Building glyph frequency map...")
    glyph_freq = build_glyph_freq(entries)
    print(f"      {len(glyph_freq)} unique glyph characters")
    print("      Top 10 glyphs by frequency:")
    for char, cnt in glyph_freq.most_common(10):
        print(f"        {repr(char):<12} {cnt:>5}")

    print("[3/5] Loading Fuls catalog sign frequencies...")
    fuls_freq = load_fuls_sign_freq()
    existing = load_existing_mapping()
    print(f"      {len(fuls_freq)} Fuls catalog signs | {len(existing)} direct matches")

    print("[4/5] Building glyph-to-Fuls mapping...")
    char_map = build_full_mapping(glyph_freq, fuls_freq, existing)
    direct = sum(1 for v in char_map.values() if v["confidence"] == "direct")
    rank = sum(1 for v in char_map.values() if v["confidence"] == "rank_corr")
    print(f"      {direct} direct matches + {rank} rank-correlation matches")

    print("[5/5] Decoding inscription sequences...")
    decoded = decode_entries(entries, char_map)
    lengths = [d["length"] for d in decoded]
    total_tokens = sum(lengths)
    mean_len = total_tokens / max(len(decoded), 1)
    print(f"      {len(decoded)} decoded inscriptions")
    print(f"      {total_tokens} sign tokens | mean length: {mean_len:.2f}")

    # Save
    out_corpus = {
        "source": "Mahadevan (1977) OCR + rank-correlation glyph mapping",
        "n_inscriptions": len(decoded),
        "total_tokens": total_tokens,
        "mean_length": round(mean_len, 3),
        "n_unique_glyphs": len(glyph_freq),
        "mapping_entries": {k: v["fuls"] for k, v in char_map.items()},
        "inscriptions": decoded,
    }
    out_path = _REPORTS / "mahadevan_texts_decoded.json"
    out_path.write_text(json.dumps(out_corpus, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved → {out_path}")

    # Also save a flat corpus for Glossa Lab analysis
    flat = "\n".join(" ".join(d["sequence"]) for d in decoded if d["sequence"])
    flat_path = _REPORTS / "mahadevan_corpus_flat.txt"
    flat_path.write_text(flat, encoding="utf-8")
    print(f"Flat corpus → {flat_path}")

    print(f"\nTop 10 most frequent decoded signs:")
    sign_freq: Counter = Counter()
    for d in decoded:
        for s in d["sequence"]:
            sign_freq[s] += 1
    for sign, cnt in sign_freq.most_common(10):
        print(f"  Fuls {sign:<6} {cnt:>5} occurrences")


if __name__ == "__main__":
    main()
