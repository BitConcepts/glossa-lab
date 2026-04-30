"""Phase-24 — Laursen 2010 Table 1 parser.

Reads the natively-extracted text of Laursen 2010 (Arabian Archaeology
and Epigraphy 21:96-134) and parses Table 1 — the canonical catalogue
of 121 'Gulf Type' seals — into structured JSON.

Each output row records:
  seal_no        Laursen 2010 paper-internal seal number (1-121)
  reference      Source publication / catalogue citation
  al_sindi_no    Al-Sindi 1999 catalogue number ("N/A" or integer)
  gulf_type      "Gulf INDUS" / "Gulf Type" / "Linear-Elamite" etc.
  site           Find-spot string
  bbm_no         Bahrain Burial Mound number ("N/A" or integer)

Output: corpora/downloads/contact_zone/gulf_seals/laursen_2010_table1.json

Plus a supplementary block ``parpola_readings`` recording the only
seal in the paper for which Asko Parpola provided sign-by-sign
Parpola-1994b sign IDs (Laursen seal #10 = Janabiyah Cemetery).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_PUB = _ROOT / "corpora" / "downloads" / "contact_zone" / "publications"
_TXT = _PUB / "laursen_2010_westward_transmission_AAE.txt"
_OUT_DIR = _ROOT / "corpora" / "downloads" / "contact_zone" / "gulf_seals"
_OUT_JSON = _OUT_DIR / "laursen_2010_table1.json"


# Known Gulf-Type-string fragments to match column 8 ("Gulf Type")
_GULF_TYPE_TOKENS = [
    "Gulf INDUS", "Gulf Type", "Linear-Elamite", "Persian Gulf",
    "Proto-Dilmun", "Dilmun Type",
]

# Known site substrings to match column 9 ("Area / Site")
_SITES = [
    "Mohenjo-Daro", "Mohenjo Daro", "Chanhu-Daro", "Chanhu Daro",
    "Harappa", "Lothal",
    "Qala'at al-Bahrain", "Qala\u2019at al-Bahrain", "Qala\u2032at al-Bahrain",
    "Karzakkan Cemetery", "Saar Cemetery", "Saar",
    "Janabiyah Cemetery", "Janabiyah",
    "Rifa mounds", "Rifa", "Bahrain",
    "Failaka", "Susa", "Luristan",
    "Ur", "Girsu", "Mesopotamia?", "Mesopotamia",
    "Near East", "Iran", "Tell Asmar", "Eshnunna",
    "Kish", "Nippur",
    "western Iranian plateau",
]


def _is_seal_no_line(line: str) -> int | None:
    """If line is just a seal number 1-121, return it. Otherwise None."""
    s = line.strip()
    if s.isdigit():
        n = int(s)
        if 1 <= n <= 121:
            return n
    return None


def _looks_like_reference(line: str) -> bool:
    """Heuristic: a Laursen Table 1 reference line cites an
    author + year + plate / no. / fig. / cat."""
    if not line:
        return False
    if not re.search(r"(19|20)\d{2}", line):
        # No year
        if not re.search(r"This paper", line, re.I):
            return False
    return bool(
        re.search(
            r"(pl\.|no\.|fig\.|f\u00ecg\.|cat\.|abb\.|This paper|CISI vol|p\.\s*\d+)",
            line,
            re.I,
        )
    )


def _find_site(block: list[str]) -> str:
    """Return the first matching site token in *block*."""
    text = " | ".join(block)
    # Prefer longer matches first (Mohenjo-Daro before Daro)
    for site in sorted(_SITES, key=len, reverse=True):
        if site in text:
            return site
    return ""


def _find_gulf_type(block: list[str]) -> str:
    text = " | ".join(block)
    for tok in sorted(_GULF_TYPE_TOKENS, key=len, reverse=True):
        if tok in text:
            return tok
    return ""


def _parse_table(text: str) -> list[dict]:
    lines = text.splitlines()
    rows: list[dict] = []
    seen_seal_nos: set[int] = set()

    i = 0
    while i < len(lines):
        n = _is_seal_no_line(lines[i])
        if n is None or n in seen_seal_nos:
            i += 1
            continue
        # Collect the next ~12 lines as candidate row context.
        # Critical: numeric *cells* in the row (grooves, dimensions) can
        # collide with seal-number values. We only treat a numeric line
        # as the next seal# if it equals current_n + 1 (rows are
        # monotonically increasing in Laursen Table 1).
        context = []
        j = i + 1
        max_block = 14
        while j < len(lines) and (j - i) <= max_block:
            ln = lines[j]
            nxt = _is_seal_no_line(ln)
            if nxt is not None and nxt == n + 1:
                break
            if "Table 1." in ln:  # next continuation block header
                break
            context.append(ln)
            j += 1

        if not context:
            i += 1
            continue

        # The first non-empty context line should be a reference
        ref_line = ""
        ref_idx = -1
        for idx, ln in enumerate(context):
            if ln.strip() and _looks_like_reference(ln):
                ref_line = ln.strip()
                ref_idx = idx
                break
        if not ref_line:
            # Not a real table row - skip
            i += 1
            continue

        # Al-Sindi 1999 no.  -- the line just after the reference
        al_sindi = ""
        if ref_idx + 1 < len(context):
            al_candidate = context[ref_idx + 1].strip()
            if al_candidate and (al_candidate == "N \u2044 A"
                                  or re.fullmatch(r"\d+", al_candidate)
                                  or al_candidate == "N/A"):
                al_sindi = al_candidate.replace("N \u2044 A", "N/A")

        site = _find_site(context)
        gulf_type = _find_gulf_type(context)

        # BBM number -- last line of the block sometimes
        bbm_no = ""
        for ln in reversed(context):
            s = ln.strip()
            if not s:
                continue
            if s == "N \u2044 A" or s == "N/A":
                bbm_no = "N/A"
                break
            if re.fullmatch(r"\d{1,6}", s):
                bbm_no = s
                break
            break  # last non-empty line was something else; bail

        rows.append({
            "seal_no": n,
            "reference": ref_line,
            "al_sindi_1999_no": al_sindi or "N/A",
            "gulf_type": gulf_type,
            "site": site,
            "bbm_no": bbm_no or "N/A",
        })
        seen_seal_nos.add(n)
        i = j

    # Sort by seal_no for determinism
    rows.sort(key=lambda r: r["seal_no"])
    return rows


# ── Parpola sign-list readings transcribed from Laursen 2010 footnote 2 ──
# Seal #10 (Janabiyah Cemetery) is the ONLY seal in the paper for which
# Parpola provided sign-by-sign Parpola-1994b IDs. Recorded here verbatim.
PARPOLA_READINGS = {
    10: {
        "site": "Janabiyah Cemetery, Bahrain",
        "reading_source": "Asko Parpola, personal communication, "
                           "in Laursen 2010 footnote 2",
        "sign_list": "Parpola 1994b: 70-78, fig. 5.1",
        "n_signs": 7,
        # Reading right-to-left on the impression (per Laursen footnote)
        "indus_signs": [
            {"position": 1, "primary": "53", "alternates": ["60"],
             "note": "uncertain 53 OR unidentified (possibly badly-drawn 'fish' 60)"},
            {"position": 1, "primary": "147", "alternates": [],
             "note": "follows position 1a"},
            {"position": 2, "primary": "364", "alternates": []},
            {"position": 3, "primary": "145", "alternates": []},
            {"position": 4, "primary": "126", "alternates": ["125", "128"],
             "note": "very uncertain; cf. Parpola 1994a fig. 1718 text 5"},
            {"position": 5, "primary": "16", "alternates": [],
             "note": "uncertain; rare in Indus Valley but common in Near East"},
            {"position": 6, "primary": "145", "alternates": []},
        ],
        "linear_sign_ids": ["53|60", "147", "364", "145", "126", "16", "145"],
        "noted_parallels": [
            {"sign_seq": ["16", "145"],
             "found_at": "Kalibangan sealings K-69 to K-75",
             "ref": "Joshi & Parpola 1987:312-313"},
            {"sign_seq": ["16", "364"],
             "found_at": "Mohenjo-Daro M-798 unicorn seal",
             "ref": "Shah & Parpola 1991:68"},
            {"sign_id": "145",
             "found_at": "Parpola 1994a Near Eastern texts nos. 5, 8, 29"},
            {"sign_id": "16",
             "found_at": "Parpola 1994a Near Eastern texts nos. 6-8, 31, 35"},
            {"sign_id": "125",
             "found_at": "Parpola 1994a Near Eastern texts nos. 29, 18, 34, 39, 15, 36"},
        ],
    },
}


def main() -> None:
    if not _TXT.exists():
        raise SystemExit(f"Laursen 2010 .txt not found: {_TXT}")
    text = _TXT.read_text(encoding="utf-8", errors="replace")
    rows = _parse_table(text)

    # Sub-divide for reporting
    by_type: dict[str, int] = {}
    by_site: dict[str, int] = {}
    n_inscribed = 0
    for r in rows:
        by_type[r["gulf_type"]] = by_type.get(r["gulf_type"], 0) + 1
        by_site[r["site"]] = by_site.get(r["site"], 0) + 1
        if "INDUS" in r["gulf_type"].upper():
            n_inscribed += 1

    out = {
        "source_paper": "Laursen 2010, Arabian Archaeology and Epigraphy "
                         "21:96-134 (Wiley)",
        "n_rows_parsed": len(rows),
        "n_rows_expected": 121,
        "n_inscribed_with_indus_text": n_inscribed,
        "by_gulf_type": dict(sorted(by_type.items())),
        "by_site": dict(sorted(by_site.items(), key=lambda kv: -kv[1])),
        "rows": rows,
        "parpola_readings": PARPOLA_READINGS,
        "ingestion_method": (
            "Lightweight regex parser; cells are emitted line-by-line "
            "by PyMuPDF text extraction. Each row identified by its "
            "seal_no line followed by an author-year reference. Site "
            "and gulf_type fields use longest-match against curated "
            "vocabularies."
        ),
    }
    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    _OUT_JSON.write_text(
        json.dumps(out, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Parsed {len(rows)}/121 rows.")
    print(f"  Inscribed (Gulf INDUS): {n_inscribed}")
    print(f"  Top sites:")
    for site, n in list(by_site.items())[:8]:
        print(f"    {site or '(unmatched)':<30} {n}")
    print(f"Wrote {_OUT_JSON}")


if __name__ == "__main__":
    main()
