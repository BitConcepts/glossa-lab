"""Parser for Andreas Fuls' Indus corpus publications.

Extracts sign sequences, metadata, and sign catalog data from:
  - "Corpus of Indus Inscriptions" (Fuls 2022/2023)
  - "A Catalog of Indus Signs" (Fuls 2023)

The Fuls notation uses:
  - Sign numbers: 3-digit codes (001-676)
  - Separator: hyphen (-)
  - Text boundaries: plus sign (+)
  - Reading direction: R/L, L/R, T/B, BUS
  - Eroded sign: 000
  - Eroded text part: ++

Example inscription:
  +407-032-520-100-585-017-231+
  Read right-to-left: 231, 017, 585, 100, 520, 032, 407

Usage:
  1. Extract text from Kindle ebook (copy-paste or ebook tools)
  2. Save as .txt file
  3. Run: parse_corpus_file("corpus.txt")
  4. Load results into Glossa Lab database
"""

from __future__ import annotations

import re
from typing import Any


def parse_inscription_line(line: str) -> dict[str, Any] | None:
    """Parse a single inscription line in Fuls notation.

    Expected format:
      +407-032-520-100-585-017-231+
    or with multiple text parts:
      +144+700-033+

    Returns dict with sign_ids, text_parts, and raw text.
    """
    line = line.strip()
    if not line or not line.startswith("+"):
        return None

    # Extract all text parts (separated by +)
    # Remove leading/trailing +
    inner = line.strip("+")
    if not inner:
        return None

    text_parts = []
    for part in inner.split("+"):
        part = part.strip("-").strip()
        if not part:
            continue
        signs = [s.strip() for s in part.split("-") if s.strip()]
        if signs:
            text_parts.append(signs)

    if not text_parts:
        return None

    # Flatten all signs
    all_signs = [s for part in text_parts for s in part]

    return {
        "raw": line,
        "sign_ids": all_signs,
        "text_parts": text_parts,
        "num_parts": len(text_parts),
        "total_signs": len(all_signs),
        "has_eroded": "000" in all_signs,
    }


def parse_corpus_entry(text_block: str) -> dict[str, Any] | None:
    """Parse a full corpus entry with metadata.

    Fuls entries typically include:
      - ICIT ID or CISI number
      - Site/findspot
      - Object type
      - Reading direction
      - Sign sequence
      - Iconography description

    This parser extracts what it can from free-text entries.
    """
    lines = [l.strip() for l in text_block.strip().splitlines() if l.strip()]
    if not lines:
        return None

    entry: dict[str, Any] = {"raw_text": text_block}

    for line in lines:
        # Look for sign sequences
        if "+" in line and re.search(r"\d{3}", line):
            parsed = parse_inscription_line(line)
            if parsed:
                entry["inscription"] = parsed

        # Look for site names
        for site in [
            "Mohenjo-daro", "Harappa", "Lothal", "Kalibangan",
            "Dholavira", "Chanhu-daro", "Banawali", "Surkotada",
            "Balakot", "Shortughai",
        ]:
            if site.lower() in line.lower():
                entry["findspot"] = site
                break

        # Look for object types
        for obj_type, keywords in {
            "square_seal": ["square seal", "SEALS:S"],
            "rectangular_seal": ["rectangular seal", "SEALS:R"],
            "tablet_incised": ["incised tablet", "TAB:I"],
            "tablet_bas_relief": ["bas-relief tablet", "TAB:B"],
            "copper_tablet": ["copper tablet", "TAB:C"],
            "pottery": ["pottery", "POT"],
            "bangle": ["bangle", "BANG"],
        }.items():
            if any(kw.lower() in line.lower() for kw in keywords):
                entry["object_type"] = obj_type
                break

        # Look for reading direction
        for direction in ["R/L", "L/R", "T/B", "BUS"]:
            if direction in line:
                entry["reading_direction"] = direction
                break

        # Look for iconography
        for icon, keywords in {
            "unicorn_bull": ["unicorn"],
            "short_horned_bull": ["short-horned", "short horned"],
            "water_buffalo": ["buffalo"],
            "elephant": ["elephant"],
            "rhinoceros": ["rhinoceros", "rhino"],
            "tiger": ["tiger"],
            "zebu": ["zebu", "humped bull"],
        }.items():
            if any(kw.lower() in line.lower() for kw in keywords):
                entry["iconography"] = icon
                break

        # Look for ICIT ID or CISI number
        icit_match = re.search(r"ICIT[:\s]*(\d+)", line)
        if icit_match:
            entry["icit_id"] = icit_match.group(1)

        cisi_match = re.search(r"([MH])-(\d+)", line)
        if cisi_match:
            entry["cisi_id"] = cisi_match.group(0)

    return entry if "inscription" in entry else None


def parse_corpus_file(filepath: str) -> list[dict[str, Any]]:
    """Parse an entire corpus file.

    The file can be:
    1. One inscription per line (sign sequences only)
    2. Multi-line entries separated by blank lines

    Returns list of parsed entries.
    """
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    entries = []

    # Try line-by-line first (most common format)
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue

        # Direct sign sequence
        if line.startswith("+") and "-" in line:
            parsed = parse_inscription_line(line)
            if parsed:
                entries.append({"inscription": parsed})
            continue

        # Try as corpus entry
        entry = parse_corpus_entry(line)
        if entry:
            entries.append(entry)

    # If line-by-line didn't work, try block parsing
    if not entries:
        blocks = re.split(r"\n\s*\n", content)
        for block in blocks:
            entry = parse_corpus_entry(block)
            if entry:
                entries.append(entry)

    return entries


def parse_sign_catalog_entry(line: str) -> dict[str, Any] | None:
    """Parse a sign catalog entry from Fuls' catalog.

    Extracts sign number, frequency, and positional classification.
    """
    # Look for patterns like: "Sign 342: frequency 580, terminal"
    match = re.search(r"[Ss]ign\s*(\d{1,3})", line)
    if not match:
        return None

    entry: dict[str, Any] = {"sign_id": match.group(1)}

    # Frequency
    freq_match = re.search(r"[Ff]req(?:uency)?[:\s]*(\d+)", line)
    if freq_match:
        entry["frequency"] = int(freq_match.group(1))

    # Positional classification
    for pos_type in ["initial", "terminal", "medial", "post-terminal"]:
        if pos_type.lower() in line.lower():
            entry["position_class"] = pos_type
            break

    # Function classification (from Wells)
    for func in ["NUM", "LON", "SHN", "TMK", "ITM", "LOG", "SYL"]:
        if func in line:
            entry["function"] = func
            break

    return entry


def entries_to_glossa_format(
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Convert parsed entries to Glossa Lab corpus format.

    Returns dict ready for upload via POST /api/v1/texts.
    """
    all_signs: list[str] = []
    inscription_lengths: list[int] = []
    metadata_entries: list[dict[str, Any]] = []

    for entry in entries:
        insc = entry.get("inscription", {})
        signs = insc.get("sign_ids", [])
        if not signs:
            continue

        # Filter eroded signs
        clean_signs = [s for s in signs if s != "000"]
        if not clean_signs:
            continue

        all_signs.extend(clean_signs)
        inscription_lengths.append(len(clean_signs))

        meta = {}
        for key in ("findspot", "object_type", "iconography",
                     "reading_direction", "icit_id", "cisi_id"):
            if key in entry:
                meta[key] = entry[key]
        metadata_entries.append(meta)

    return {
        "name": "Indus Corpus (Fuls)",
        "corpus_type": "target",
        "content": all_signs,
        "metadata": {
            "source": "Fuls (2022/2023) Corpus of Indus Inscriptions",
            "inscription_count": len(inscription_lengths),
            "inscription_lengths": inscription_lengths,
            "total_signs": len(all_signs),
            "unique_signs": len(set(all_signs)),
            "entries": metadata_entries[:100],  # Sample for reference
        },
    }
