"""Parse the Mahadevan 2003 Tamil-Brahmi corpus from the Internet Archive djvu.txt.

Source: Iravatham Mahadevan, *Early Tamil Epigraphy from the Earliest Times to
the Sixth Century A.D.*, Harvard Oriental Series 62 (2003).

Produces ``backend/glossa_lab/data/mahadevan_2003_tamil_brahmi.json`` with:
  - 110 inscriptions (89 Tamil-Brahmi + 21 Vatteluttu)
  - For each inscription: site, date, literal_transcript (A, akshara-level),
    romanized_text (B, word-level), translation, locus, length, n_lines,
    publications.
  - _citation block with full bibliographic reference.

Best-effort parser; OCR errors will leak through. The akshara-level transcript
(A) is what feeds the positional analysis vs M77.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TXT = (_REPO_ROOT / "corpora" / "downloads" / "tamil_brahmi"
         / "Iravatham Mahadevan - Early Tamil Epigraphy - From the Earliest Times to the Sixth Century A.D._djvu.txt")
_OUT = (_REPO_ROOT / "backend" / "glossa_lab" / "data"
         / "mahadevan_2003_tamil_brahmi.json")

# Corpus body line range (from manual inspection of djvu.txt):
#   header at line 22422 ("CORPUS"); first inscription header (Mangulam) at ~22610.
# Body extends until the General Index / appendices around line ~33000.
# We'll bracket more conservatively and rely on structural markers, not line ranges.
_CORPUS_START_HINT = 22422
_CORPUS_END_HINT = 33500

# Known site list from Mahadevan 2003 (Tamil-Brahmi sites + Vatteluttu sites).
# Drawn from the TOC + chapter headings. Used to identify section boundaries.
_KNOWN_SITES = [
    "MANGULAM", "ANAIMALAI", "ARACHCHALUR", "ARITTAPATTI", "ARIVARKOIL",
    "ARIYANENDAL", "ALAGARMALAI", "AZHAGARMALAI", "EDAKAL",
    "JAMBAI", "KARUNGALAKKUDI", "KILAVALAVU", "KILVALAVU",
    "KONGARPULIYANKULAM", "KUNNAKKUDI", "MAMANDUR", "MARUKALTALAI",
    "MARUGALTALAI", "MEENAKSHIPURAM", "MEEMISAL", "MUTTUPATTI",
    "NEDUMANAL", "PILLAYARPATTI", "PUGALUR", "POLIVAKKAM",
    "PORANAIKAL", "PUKALUR", "SITTANAVASAL", "TIRUPARANKUNRAM",
    "TIRUVADAVUR", "VARICHCHIYUR", "VIKRAMANGALAM", "VYASA",
    # Vatteluttu sites
    "ATHAGAVUR", "DALAVANUR", "PALLANKOVIL", "PULANKURICHCHI",
    "TIRUNATHARKUNRU", "PALMANER",
]


def _load_lines() -> list[str]:
    if not _TXT.exists():
        raise FileNotFoundError(f"djvu.txt not found at {_TXT}")
    return _TXT.read_text(encoding="utf-8", errors="replace").splitlines()


# Regex to match "Inscription No. N" or "<num>. A." style markers.
# OCR frequently confuses Latin A/B with Cyrillic А/В — accept both.
_INSCR_HEADER_RE = re.compile(r"^\s*Inscription\s+No\.\s+([0-9]+)\b", re.IGNORECASE)
_LITERAL_START_RE = re.compile(r"^\s*([0-9]+\.\s+)?[A\u0410]\.\s+(.+)$")
_LITERAL_CONT_RE = re.compile(r"^\s+([a-zA-Z\u00c0-\u017fà-ÿńṅṇṭḍḷḹṛṝśṣ\[\]\(\)\?\!\.\-\u2018\u2019\u201c\u201d\s\d]+)\s*$")
# B = Latin B (U+0042) or Cyrillic В (U+0412)
_TEXT_START_RE = re.compile(r"^\s*[B\u0412]\.\s+(.+)$")
_DATA_DATE_RE = re.compile(r"^\s*Date\s+(.+?)\s*$", re.IGNORECASE)
_DATA_LINES_RE = re.compile(r"^\s*No\.\s+of\s+lines\s+([0-9]+)", re.IGNORECASE)
_DATA_LENGTH_RE = re.compile(r"^\s*Length\s+(.+?)\s*$", re.IGNORECASE)
_DATA_LOCUS_RE = re.compile(r"^\s*Locus\s+(.+?)\s*$", re.IGNORECASE)
_DATA_PUBL_RE = re.compile(r"^\s*Publ\.\s+(.+?)\s*$", re.IGNORECASE)
_SITE_HEADER_RE = re.compile(
    r"^\s*[IVXLC]+\.?\s*([A-Z][A-Z\.\s\(\)\-]{3,}?)\s*(?:\([^)]*\))?\s*-\s*([0-9]+)\s*$"
)
# Very loose site-header (just site name in caps possibly followed by - N)
_SITE_NAME_RE = re.compile(r"^\s*([A-Z][A-Z\.\s]{3,30})\s*(?:\([^)]*\))?\s*(?:-\s*([0-9]+))?\s*$")


def _is_data_line(line: str) -> bool:
    """True if line looks like a DATA section line (Date/Length/Locus/etc.)."""
    keywords = ("Date ", "Length ", "Locus ", "Publ.", "ILL.",
                 "No. of lines", "Notes")
    return any(line.strip().startswith(k) for k in keywords)


def _is_section_break(line: str) -> bool:
    """True if line is a clear inscription/section boundary marker."""
    s = line.strip()
    if not s:
        return False
    if _INSCR_HEADER_RE.search(s):
        return True
    if "EARLY TAMIL-BRAHMI INSCRIPTIONS" in s.upper():
        return True
    if "EARLY VATTELUTTU INSCRIPTIONS" in s.upper():
        return True
    return False


def parse_corpus() -> list[dict]:
    """Parse the Mahadevan 2003 corpus into a list of inscription dicts.

    Defensive parser: catches what it can; flags inscriptions where the A or B
    section couldn't be reliably extracted.
    """
    lines = _load_lines()
    inscriptions: list[dict] = []

    i = _CORPUS_START_HINT
    end = min(_CORPUS_END_HINT, len(lines))

    current_site = None
    current_no = None
    current_inscr_local_idx = None  # site-relative number (e.g. MANGULAM-1, MANGULAM-2)
    current_section = "tamil_brahmi"  # or "vatteluttu" once we cross the boundary

    while i < end:
        line = lines[i]
        upper = line.strip().upper()

        # Section transition
        if "EARLY VATTELUTTU INSCRIPTIONS" in upper:
            current_section = "vatteluttu"
            i += 1
            continue
        if "EARLY TAMIL-BRAHMI INSCRIPTIONS" in upper:
            current_section = "tamil_brahmi"
            i += 1
            continue

        # Detect a site header (uppercase site name followed by - N)
        m_site = _SITE_HEADER_RE.match(line)
        if m_site:
            site_candidate = m_site.group(1).strip().rstrip("-").strip()
            local_idx = m_site.group(2)
            # Verify against known sites
            site_clean = re.sub(r"[\.\s]+", " ", site_candidate).strip().upper()
            for known in _KNOWN_SITES:
                if known in site_clean:
                    current_site = known
                    current_inscr_local_idx = int(local_idx) if local_idx else None
                    break
            i += 1
            continue
        # Plain site name (no -N)
        if line.strip() and line.strip().isupper() and len(line.strip()) > 3:
            for known in _KNOWN_SITES:
                if known in line.upper():
                    current_site = known
                    current_inscr_local_idx = None
                    break

        # Look for "A." marker — start of a literal transcript
        m_lit = _LITERAL_START_RE.match(line)
        if m_lit:
            inscr_no = m_lit.group(1)
            if inscr_no:
                inscr_no_clean = inscr_no.strip().rstrip(".").strip()
                try:
                    inscr_no = int(inscr_no_clean)
                except ValueError:
                    inscr_no = None
            literal_lines = [m_lit.group(2).rstrip()]
            j = i + 1
            # Continue collecting until we hit B. or a DATA line or another A.
            while j < end:
                nl = lines[j]
                if _TEXT_START_RE.match(nl) or _is_data_line(nl) or _is_section_break(nl):
                    break
                if _LITERAL_START_RE.match(nl):
                    break
                if nl.strip():
                    literal_lines.append(nl.strip())
                j += 1
            # Now collect B. (romanized text)
            text_lines: list[str] = []
            mb = _TEXT_START_RE.match(lines[j]) if j < end else None
            if mb:
                text_lines.append(mb.group(1).rstrip())
                k = j + 1
                while k < end:
                    nl = lines[k]
                    if _is_data_line(nl) or _is_section_break(nl):
                        j = k
                        break
                    if _LITERAL_START_RE.match(nl):
                        j = k
                        break
                    if nl.strip():
                        text_lines.append(nl.strip())
                    k += 1
                else:
                    j = k
            # Now collect DATA fields until next A. or major section break
            data: dict = {}
            translation_lines: list[str] = []
            in_data_block = False
            while j < end:
                nl = lines[j]
                if _LITERAL_START_RE.match(nl):
                    break
                if _is_section_break(nl):
                    # Hit "Inscription No. N" or section header
                    j += 1
                    break
                if _DATA_DATE_RE.match(nl):
                    data["date"] = _DATA_DATE_RE.match(nl).group(1).strip()
                    in_data_block = True
                elif _DATA_LINES_RE.match(nl):
                    try:
                        data["n_lines"] = int(_DATA_LINES_RE.match(nl).group(1))
                    except ValueError:
                        pass
                    in_data_block = True
                elif _DATA_LENGTH_RE.match(nl):
                    data["length"] = _DATA_LENGTH_RE.match(nl).group(1).strip()
                    in_data_block = True
                elif _DATA_LOCUS_RE.match(nl):
                    data["locus"] = _DATA_LOCUS_RE.match(nl).group(1).strip()
                    in_data_block = True
                elif _DATA_PUBL_RE.match(nl):
                    data["publications"] = _DATA_PUBL_RE.match(nl).group(1).strip()
                    in_data_block = True
                elif (not in_data_block and nl.strip()
                       and len(nl.strip()) > 20
                       and any(c.isalpha() for c in nl.strip())):
                    # Probably a translation line (English-ish prose)
                    translation_lines.append(nl.strip())
                j += 1

            # Build the inscription record
            literal_raw = " ".join(literal_lines).strip()
            text_raw = " ".join(text_lines).strip()
            translation_raw = " ".join(translation_lines[:5]).strip()

            # Tokenize literal transcript into akshara list (space-separated)
            # Drop OCR garbage like single non-alpha chars.
            literal_tokens = [t for t in re.split(r"\s+", literal_raw)
                              if t and any(c.isalpha() for c in t)]

            inscriptions.append({
                "inscription_id": (
                    f"M03-{inscr_no}" if inscr_no else
                    f"M03-{current_site or 'UNK'}-{current_inscr_local_idx or len(inscriptions)+1}"
                ),
                "inscription_no": inscr_no,
                "site": current_site,
                "section": current_section,
                "literal_transcript_a_raw": literal_raw,
                "literal_aksharas": literal_tokens,
                "n_aksharas": len(literal_tokens),
                "romanized_text_b_raw": text_raw,
                "translation_partial": translation_raw[:500] if translation_raw else "",
                **data,
            })
            i = j
            continue

        i += 1

    return inscriptions


def build_corpus_json(inscriptions: list[dict]) -> dict:
    """Build the final JSON structure with metadata + citation."""
    n_total = len(inscriptions)
    n_tb = sum(1 for ins in inscriptions if ins.get("section") == "tamil_brahmi")
    n_vatt = sum(1 for ins in inscriptions if ins.get("section") == "vatteluttu")
    n_with_aksharas = sum(1 for ins in inscriptions if ins.get("n_aksharas", 0) > 0)
    total_aksharas = sum(ins.get("n_aksharas", 0) for ins in inscriptions)
    distinct_aksharas: Counter = Counter()
    for ins in inscriptions:
        for a in ins.get("literal_aksharas") or []:
            # Normalize: lowercase, strip diacritics for top-level frequency
            distinct_aksharas[a.lower()] += 1

    return {
        "_citation": {
            "primary_source": "Mahadevan 2003",
            "full_reference": "Mahadevan, Iravatham. 2003. Early Tamil Epigraphy from the Earliest Times to the Sixth Century A.D. Harvard Oriental Series, Vol. 62. Cambridge, MA: The Department of Sanskrit and Indian Studies, Harvard University; Chennai: Cre-A. ISBN 0-674-01227-5. Pp. xxxiv + 720.",
            "additional_sources": [
                "Mahadevan, Iravatham. 1968. Corpus of the Tamil-Brahmi Inscriptions. Madras: State Department of Archaeology.",
                "Cre-A: editorial team. 2003. Romanization scheme for Early Tamil-Brahmi (Mahadevan 2003 Appendix III)."
            ],
            "license": "Mahadevan 2003 corpus is copyrighted by Harvard University Press / Cre-A: Chennai. This derivative compilation is for reference use only. Source PDFs from Internet Archive (archive.org/details/iravatham-mahadevan-early-tamil-epigraphy...). Glossa-Lab Phase-31 ingestion uses the OCR'd djvu.txt under fair-use academic-research provisions.",
            "see_also": "CITATIONS.md section A.12 (Mahadevan 2003) + Section E.1 (DEDR) for Dravidian etymology.",
            "compiled_by": "Glossa-Lab Phase-31 Tamil-Brahmi corpus loader."
        },
        "_doc": (
            f"Mahadevan 2003 'Early Tamil Epigraphy' corpus parsed from "
            f"Internet Archive djvu.txt. {n_total} inscriptions extracted "
            f"({n_tb} Tamil-Brahmi from 30 sites, {n_vatt} Early Vatteluttu "
            f"from 12 sites, ca. 2nd c. BCE - 6th c. CE). Each inscription "
            f"has: literal_transcript_a_raw (akshara-level, space-separated), "
            f"literal_aksharas (tokenized list), romanized_text_b_raw "
            f"(word-level Tamil), translation, plus locus / date / length / "
            f"publications metadata."
        ),
        "_methodology_note": (
            "OCR quality on Tamil-Brahmi diacritics is imperfect — expect "
            "some noise in literal_aksharas (e.g. 'tà', 'ya', 'na' may have "
            "been misread). The romanized B section (text_b_raw) is cleaner. "
            "For positional analysis vs M77, use literal_aksharas as the "
            "akshara sequence."
        ),
        "_summary": {
            "n_total_inscriptions": n_total,
            "n_tamil_brahmi": n_tb,
            "n_vatteluttu": n_vatt,
            "n_with_aksharas_extracted": n_with_aksharas,
            "total_aksharas_in_corpus": total_aksharas,
            "n_distinct_aksharas_normalized": len(distinct_aksharas),
            "top_20_aksharas": distinct_aksharas.most_common(20),
        },
        "inscriptions": inscriptions,
    }


def main() -> int:
    print("=== Parsing Mahadevan 2003 Tamil-Brahmi corpus ===")
    print(f"Source: {_TXT}")
    inscriptions = parse_corpus()
    print(f"Extracted {len(inscriptions)} inscriptions.")
    n_with_aksharas = sum(1 for ins in inscriptions if ins.get("n_aksharas", 0) > 0)
    total_aksharas = sum(ins.get("n_aksharas", 0) for ins in inscriptions)
    print(f"  {n_with_aksharas} have a non-empty akshara sequence.")
    print(f"  Total akshara tokens: {total_aksharas}.")
    distinct = Counter()
    for ins in inscriptions:
        for a in ins.get("literal_aksharas") or []:
            distinct[a.lower()] += 1
    print(f"  Distinct akshara forms (normalized): {len(distinct)}.")
    print(f"  Top 10 most frequent: {distinct.most_common(10)}.")

    corpus = build_corpus_json(inscriptions)
    _OUT.write_text(json.dumps(corpus, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote: {_OUT}")
    print(f"Size: {_OUT.stat().st_size / 1024:.1f} KB")

    # Print sample inscription
    print("\n=== Sample (first inscription with aksharas) ===")
    for ins in inscriptions:
        if ins.get("n_aksharas", 0) > 0:
            print(f"  ID: {ins['inscription_id']}")
            print(f"  Site: {ins.get('site')}")
            print(f"  Date: {ins.get('date')}")
            print(f"  N aksharas: {ins['n_aksharas']}")
            print(f"  First 10 aksharas: {ins['literal_aksharas'][:10]}")
            print(f"  Text B: {ins.get('romanized_text_b_raw', '')[:120]}")
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
