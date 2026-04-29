"""Phase-22: extract Meluhha / Magan / Dilmun / Guabba mentions from
the on-disk CDLI ATF dump.

This is data plumbing per WARP.md G1's acceptable-exceptions clause —
its output (`corpora/downloads/contact_zone/cdli_meluhha/meluhha_tablets.json`)
is consumed by Phase-22 graph experiments.

Inputs:
  corpora/downloads/external_repos/cdli_gh_data/cdliatf_unblocked.atf
  corpora/downloads/external_repos/cdli_gh_data/cdli_cat.csv

Logic:
  Stream-parse the ATF file (108k+ texts, one block per "&P" header)
  and flag any text whose body contains a Meluhha-family keyword.
  Cross-reference each hit's CDLI P-number with cdli_cat.csv to attach
  period / provenience / collection / publication metadata.

Output JSON shape:
{
  "n_total_atf_texts": int,
  "n_hits": int,
  "keyword_counts": {keyword: int, ...},
  "hits_by_period": {period_label: int, ...},
  "tablets": [
    {
      "p_number": "P012345",
      "designation": "BIN VIII 298",
      "period": "Old Akkadian (ca. 2340-2200 BC)",
      "provenience": "Adab (mod. Bismaya)",
      "collection": "...",
      "primary_publication": "...",
      "atf_excerpt": "first 600 chars of ATF body",
      "matched_keywords": ["me-luh-ha", "magan"],
      "match_count": 3,
      "atf_lines_with_match": ["10. dam-gar3 me-luh-ha-ki", ...]
    }, ...
  ]
}
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ATF_PATH = ROOT / "corpora" / "downloads" / "external_repos" / "cdli_gh_data" / "cdliatf_unblocked.atf"
CAT_PATH = ROOT / "corpora" / "downloads" / "external_repos" / "cdli_gh_data" / "cdli_cat.csv"
OUT_DIR = ROOT / "corpora" / "downloads" / "contact_zone" / "cdli_meluhha"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_JSON = OUT_DIR / "meluhha_tablets.json"
OUT_TXT = OUT_DIR / "meluhha_tablets_summary.txt"

# Keywords (case-insensitive substring match).
# Use forms common in CDLI ATF transliterations.
KEYWORDS = [
    # Meluhha
    "me-luh-ha", "me-luh-ha-ki", "me-luh-haki",
    "me-luh3-ha", "me-luh3-haki",
    # Magan
    "ma2-gan", "ma2-gan-ki", "ma2-ganki",
    "ma-gan", "ma-gan-ki", "ma-ganki",
    # Dilmun / Tilmun
    "dilmun", "dilmunki", "dilmun-ki",
    "tilmun", "tilmunki", "tilmun-ki",
    # Gu'abba (the Meluhhan village identified by Vermaak 2008)
    "gu2-ab-ba", "gu2-ab-baki", "gu-ab-ba", "gu-ab-baki",
    # Marhashi (the eastern Iranian neighbour)
    "mar-ha-shi", "mar-ha-shiki", "mar-ha-si", "mar-ha-siki",
    "marhashi", "parahshum",
    # Tukrish (an eastern toponym sometimes paired with Meluhha)
    "tukrish", "tukris",
    # Sargonic / Lagash key names from Parpola/Brunswig 1977
    "su-ilisu", "shu-ilisu", "shu-ilishu",
    "lu-sun-zi-da", "lu2-sun-zi-da",
]


def _extract_p_header(line: str) -> str | None:
    """Return the P-number (e.g. P012345) for an ATF '&P' header line."""
    m = re.match(r"^&\s*(P\d{6,8})\b", line)
    return m.group(1) if m else None


def _stream_atf(path: Path):
    """Yield (p_number, full_text, lines) per text block."""
    cur_p: str | None = None
    cur_lines: list[str] = []
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            p = _extract_p_header(line)
            if p is not None:
                if cur_p is not None:
                    yield cur_p, "\n".join(cur_lines), cur_lines
                cur_p = p
                cur_lines = [line.rstrip("\n")]
            else:
                if cur_p is not None:
                    cur_lines.append(line.rstrip("\n"))
        if cur_p is not None:
            yield cur_p, "\n".join(cur_lines), cur_lines


def _load_catalogue(path: Path) -> dict[str, dict]:
    """Load CDLI catalogue keyed by P-number.

    The CDLI bulk-data CSV stores numeric `id_text` (1, 2, ...). The
    canonical P-number is formed as ``P`` + zero-padded `id_text` to 6
    digits (e.g. id_text=298 -> P000298).
    """
    cat: dict[str, dict] = {}
    if not path.exists():
        return cat
    csv.field_size_limit(2 ** 25)  # ATF excerpts can be large
    with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        r = csv.DictReader(fh)
        for row in r:
            id_text = (row.get("id_text") or "").strip()
            if not id_text or not id_text.isdigit():
                continue
            p = f"P{int(id_text):06d}"
            cat[p] = row
    return cat


def main() -> int:
    if not ATF_PATH.exists():
        print(f"ERROR: ATF not found: {ATF_PATH}", file=sys.stderr)
        return 1
    print(f"Loading CDLI catalogue: {CAT_PATH}", flush=True)
    cat = _load_catalogue(CAT_PATH)
    print(f"  Catalogue rows: {len(cat)}", flush=True)

    keyword_counts: Counter[str] = Counter()
    hits_by_period: Counter[str] = Counter()
    hits_by_provenience: Counter[str] = Counter()
    tablets: list[dict] = []
    n_total = 0

    print(f"Streaming ATF file: {ATF_PATH}", flush=True)
    for p_number, text, lines in _stream_atf(ATF_PATH):
        n_total += 1
        if n_total % 20000 == 0:
            print(f"  scanned {n_total} texts; hits so far: {len(tablets)}", flush=True)
        text_lower = text.lower()
        matched: list[str] = []
        match_count = 0
        for kw in KEYWORDS:
            n = text_lower.count(kw.lower())
            if n > 0:
                matched.append(kw)
                keyword_counts[kw] += n
                match_count += n
        if not matched:
            continue
        # Save the lines that triggered the match (small, useful for review)
        match_lines: list[str] = []
        for ln in lines:
            ll = ln.lower()
            if any(kw.lower() in ll for kw in matched):
                match_lines.append(ln)
                if len(match_lines) >= 12:
                    break
        cat_row = cat.get(p_number, {})
        period = (cat_row.get("period") or "").strip() or "(unknown)"
        provenience = (cat_row.get("provenience") or "").strip() or "(unknown)"
        hits_by_period[period] += 1
        hits_by_provenience[provenience] += 1
        tablets.append({
            "p_number": p_number,
            "designation": (cat_row.get("designation") or "").strip(),
            "period": period,
            "provenience": provenience,
            "collection": (cat_row.get("collection") or "").strip(),
            "primary_publication": (cat_row.get("primary_publication") or "").strip(),
            "atf_excerpt": text[:600],
            "matched_keywords": matched,
            "match_count": match_count,
            "atf_lines_with_match": match_lines,
        })

    output = {
        "n_total_atf_texts": n_total,
        "n_hits": len(tablets),
        "keyword_counts": dict(keyword_counts.most_common()),
        "hits_by_period": dict(hits_by_period.most_common()),
        "hits_by_provenience": dict(hits_by_provenience.most_common(30)),
        "tablets": tablets,
    }
    OUT_JSON.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}", flush=True)
    print(f"  texts scanned: {n_total}", flush=True)
    print(f"  hits          : {len(tablets)}", flush=True)
    print(f"  top keywords  : {keyword_counts.most_common(10)}", flush=True)
    print(f"  top periods   : {hits_by_period.most_common(8)}", flush=True)
    print(f"  top provenience: {hits_by_provenience.most_common(8)}", flush=True)

    # Plain-text summary
    summary_lines: list[str] = []
    summary_lines.append(f"CDLI Meluhha/Magan/Dilmun-mention summary")
    summary_lines.append(f"Total ATF texts scanned: {n_total}")
    summary_lines.append(f"Total hits             : {len(tablets)}")
    summary_lines.append("")
    summary_lines.append("Keyword counts:")
    for k, v in keyword_counts.most_common():
        summary_lines.append(f"  {k:24s}  {v}")
    summary_lines.append("")
    summary_lines.append("Hits by period:")
    for k, v in hits_by_period.most_common():
        summary_lines.append(f"  {v:5d}  {k}")
    summary_lines.append("")
    summary_lines.append("Hits by provenience (top 30):")
    for k, v in hits_by_provenience.most_common(30):
        summary_lines.append(f"  {v:5d}  {k}")
    OUT_TXT.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"  summary       : {OUT_TXT}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
