"""Phase-16 extraction: DEDR (Burrow & Emeneau 1984) OCR -> normalized cognate-set CSV.

Input:  corpora/downloads/dedr_burrow_emeneau_1984_OCR.txt (Tesseract output, 430 pages,
        per-page markers '===== PAGE NNNN =====').
Output: backend/glossa_lab/data/phase16_corpora/dedr_cognates.csv with columns:
            entry_id, page, languages, n_languages, n_forms, raw_text

Each DEDR entry begins with a 1-5 digit entry number followed by whitespace and a
language abbreviation (Ta./Ma./Te./Ka./...). We accept OCR noise: line breaks
inside entries are joined; entries spanning multiple lines are concatenated until
the next entry-number-prefixed line is seen.

We do NOT attempt full per-language token extraction here -- DEDR's typography
(diacritics, hyphenated derivational suffixes) is too OCR-noisy for clean
extraction without manual rules per language. We capture which Dravidian
languages are attested per entry plus the raw entry text; downstream nodes can
re-tokenize if needed.

Run:
    py scripts/phase16/extract_dedr_cognates.py
"""
from __future__ import annotations

import csv
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "corpora" / "downloads" / "dedr_burrow_emeneau_1984_OCR.txt"
OUT = ROOT / "backend" / "glossa_lab" / "data" / "phase16_corpora" / "dedr_cognates.csv"

# Recognized language abbreviations in DEDR. Two-letter codes anchor more reliably
# under OCR noise than full names. Ordered by frequency / prefix-disambiguation
# (longer codes first so 'Naikr.' wins over 'Na.').
LANGS = [
    "Naikr.", "Naik.", "Manda", "Malt.", "Mand.", "Brah.", "Pkt.",
    "Skt.", "Tu.", "Te.", "Ta.", "Ma.", "Ka.", "To.", "Ko.", "Ir.",
    "Kod.", "Bel.", "Bad.", "Pa.", "Ga.", "Go.", "Kui", "Kuwi",
    "Pe.", "Kol.", "Br.", "Mal.", "Ku.", "Kur.", "Knd.",
]

ENTRY_RE = re.compile(r"^\s*(\d{1,5})\s+(?=[A-Z][a-z]?\.?\s)")
PAGE_RE = re.compile(r"^=====\s*PAGE\s+0*(\d+)\s*=====")


def normalize(line: str) -> str:
    """Strip leading/trailing whitespace and collapse internal whitespace."""
    return re.sub(r"\s+", " ", line).strip()


def detect_languages(entry_text: str) -> list[str]:
    """Return list of language abbreviations found in this entry, in order
    (deduplicated, preserving first-occurrence order)."""
    seen: dict[str, None] = {}
    # Walk through tokens; match each candidate code at a word boundary.
    for code in LANGS:
        # Use word-boundary at end (or '.' followed by space).
        pat = r"(?:^|\s)" + re.escape(code) + r"(?:\s|$)"
        if re.search(pat, entry_text):
            seen.setdefault(code, None)
    return list(seen.keys())


def parse_dedr(src: Path) -> list[dict]:
    """Stream the OCR file and yield one dict per detected entry."""
    entries: list[dict] = []
    cur_id = None
    cur_page = None
    buf: list[str] = []
    last_page_seen = 0

    def flush():
        nonlocal cur_id, cur_page, buf
        if cur_id is None or not buf:
            cur_id = None
            buf = []
            return
        text = normalize(" ".join(buf))
        langs = detect_languages(text)
        # Heuristic: require >=1 Dravidian-core language to reduce false positives
        # from page numbers, addenda numbers, etc. that happen to be 1-5 digits.
        core = {"Ta.", "Ma.", "Te.", "Ka.", "Tu."}
        if not (set(langs) & core):
            cur_id = None
            buf = []
            return
        # Crude "n_forms" estimate: count comma-separated tokens after
        # each language code, summed.
        n_forms = 0
        for code in langs:
            m = re.search(re.escape(code) + r"\s+([^.;]*)", text)
            if m:
                n_forms += len([t for t in m.group(1).split(",") if t.strip()])
        entries.append({
            "entry_id": int(cur_id),
            "page": cur_page if cur_page else last_page_seen,
            "languages": ",".join(langs),
            "n_languages": len(langs),
            "n_forms": n_forms,
            "raw_text": text[:1500],  # cap to keep CSV size reasonable
        })
        cur_id = None
        buf = []

    with src.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            m_page = PAGE_RE.match(line)
            if m_page:
                last_page_seen = int(m_page.group(1))
                continue
            stripped = line.strip()
            if not stripped:
                continue
            m_entry = ENTRY_RE.match(line)
            if m_entry:
                # Boundary between entries: flush previous, start new
                flush()
                cur_id = m_entry.group(1)
                cur_page = last_page_seen
                buf = [line[m_entry.end():].lstrip()]  # text after entry id
            else:
                if cur_id is not None:
                    buf.append(stripped)
        flush()
    return entries


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: source not found: {SRC}", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"Reading {SRC} ...", file=sys.stderr)
    entries = parse_dedr(SRC)
    print(f"Detected {len(entries)} cognate entries", file=sys.stderr)

    # Filter to plausibly-valid entries (id in DEDR's known range 1..6000)
    entries = [e for e in entries if 1 <= e["entry_id"] <= 6000]
    print(f"After id-range filter: {len(entries)}", file=sys.stderr)

    # Deduplicate by entry_id (keep richest = most languages)
    by_id: dict[int, dict] = {}
    for e in entries:
        prev = by_id.get(e["entry_id"])
        if prev is None or e["n_languages"] > prev["n_languages"]:
            by_id[e["entry_id"]] = e
    entries = sorted(by_id.values(), key=lambda x: x["entry_id"])
    print(f"After dedup: {len(entries)} unique entries", file=sys.stderr)

    fields = ["entry_id", "page", "languages", "n_languages", "n_forms", "raw_text"]
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for e in entries:
            w.writerow(e)

    # Quick stats
    if entries:
        lang_counter: dict[str, int] = {}
        for e in entries:
            for code in e["languages"].split(","):
                if code:
                    lang_counter[code] = lang_counter.get(code, 0) + 1
        print(f"Wrote {OUT}", file=sys.stderr)
        print(f"  Total entries: {len(entries)}", file=sys.stderr)
        print(f"  Mean languages per entry: {sum(e['n_languages'] for e in entries)/len(entries):.2f}", file=sys.stderr)
        print(f"  Top 12 attested languages:", file=sys.stderr)
        for code, n in sorted(lang_counter.items(), key=lambda kv: -kv[1])[:12]:
            print(f"    {code:8s}  {n}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
