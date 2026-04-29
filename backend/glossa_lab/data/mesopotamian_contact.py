"""MesopotamianContactCorpus data module.

Loads Phase-22 contact-zone artefacts:

  - Meluhha / Magan / Dilmun / Guabba mentions extracted from the CDLI
    cuneiform corpus (1,462 tablets, scanned 2026-04 from the on-disk
    cdli-gh/data dump).
  - Hand-encoded Indus and Indus-related seals found in Mesopotamian,
    Iranian, and Persian Gulf contexts (13 seals from Gadd 1932,
    Parpola/Brunswig 1977, Possehl 2006, Laursen 2010, Frenez
    2018/2020/2024, Vidale & Frenez 2015, Vidale/Desset/Frenez 2021,
    Laursen et al. 2026).

These two datasets together constitute the *contact-zone anchor*
inventory the project identified as the biggest gap in current
Glossa-Lab work (see `corpora/downloads/contact_zone_anchors_inventory.md`).

Functions:
  get_meluhha_tablets()           -> list[dict]
  get_meluhhan_persons()          -> list[dict]
  get_indus_seals_at_mesopotamia()-> list[dict]
  get_meluhha_keyword_counts()    -> dict[str,int]
  get_meluhha_period_counts()     -> dict[str,int]
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_CDLI_MELUHHA = _ROOT / "corpora" / "downloads" / "contact_zone" / "cdli_meluhha" / "meluhha_tablets.json"
_INDUS_SEALS_MES = _ROOT / "corpora" / "downloads" / "contact_zone" / "indus_seals_mesopotamia" / "seals_at_mesopotamia.json"


def _safe_load(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


@lru_cache(maxsize=1)
def _load_meluhha_tablets_data() -> dict:
    return _safe_load(_CDLI_MELUHHA)


@lru_cache(maxsize=1)
def _load_indus_seals_at_mesopotamia_data() -> dict:
    return _safe_load(_INDUS_SEALS_MES)


def get_meluhha_tablets() -> list[dict]:
    """Return the list of CDLI tablets with Meluhha-family mentions.

    Each tablet has p_number, designation, period, provenience,
    collection, primary_publication, atf_excerpt, matched_keywords,
    match_count, atf_lines_with_match.
    """
    return list(_load_meluhha_tablets_data().get("tablets") or [])


def get_meluhha_keyword_counts() -> dict[str, int]:
    return dict(_load_meluhha_tablets_data().get("keyword_counts") or {})


def get_meluhha_period_counts() -> dict[str, int]:
    return dict(_load_meluhha_tablets_data().get("hits_by_period") or {})


def get_meluhha_provenience_counts() -> dict[str, int]:
    return dict(_load_meluhha_tablets_data().get("hits_by_provenience") or {})


def get_indus_seals_at_mesopotamia() -> list[dict]:
    """Return the hand-encoded list of Indus / Indus-related seals
    found in Mesopotamia, Iran, and the Persian Gulf."""
    return list(_load_indus_seals_at_mesopotamia_data().get("seals") or [])


# ── Meluhhan-named-person extraction ─────────────────────────────────


# Heuristic regex for Sumerian-style personal names that include a
# "me-luh-ha" qualifier or are flanked by it. Examples from the
# literature:
#   "lu2-me-luh-haki"            "man of Meluhha"
#   "dam-gar3 me-luh-ha"         "Meluhhan merchant"
#   "PN dumu me-luh-ha"          "PN, son of Meluhha"
#   "lu-sun-zi-da PN me-luh-ha"  "Lu-sunzida, a Meluhhan"
# We capture the line; downstream nodes can parse out the personal
# name candidates.

_MELUHHA_PERSON_RE = re.compile(
    r"\b("
    r"lu2?-me-luh-?ha(?:ki)?"
    r"|dumu-me-luh-?ha(?:ki)?"
    r"|me-luh-?ha-?ki"
    r"|me-luh-?ha"
    r")\b",
    re.IGNORECASE,
)

# Sumerian / Akkadian personal-name pattern: word with at least one
# hyphen, made up of cuneiform-like graphemes. Conservative: 3-30
# chars, lowercase, may include digits 1-9.
_NAME_RE = re.compile(r"\b[a-z][a-z0-9]*(?:-[a-z][a-z0-9]*){1,4}\b")


def get_meluhhan_persons() -> list[dict]:
    """Heuristically extract personal-name candidates that co-occur
    on tablets with Meluhha-family keywords.

    Output: list of {p_number, period, provenience, candidate_name,
    line, match_keyword}.

    This is a *coarse* extractor — the goal is to surface Meluhhan
    person names that should be checked manually against the
    Akkadian-name corpus (Lu-sunzida, Shu-ilishu, etc.). False
    positives are expected.
    """
    persons: list[dict] = []
    seen: set[tuple[str, str, str]] = set()
    for t in get_meluhha_tablets():
        if "me-luh" not in " ".join(t.get("matched_keywords") or []).lower():
            continue
        for line in t.get("atf_lines_with_match") or []:
            ll = line.lower()
            if "me-luh" not in ll:
                continue
            for m in _NAME_RE.finditer(ll):
                cand = m.group(0)
                # Drop the keyword itself
                if cand.startswith(("me-luh", "lu-me-luh", "lu2-me-luh", "dumu-me-luh")):
                    continue
                # Drop common Sumerian function words
                if cand in {"dam-gar3", "lugal-sa", "lugal-i-de6-a", "ki-min",
                             "i-dux", "lu-dux"}:
                    continue
                # Drop pure "X-ki" tokens (toponym suffix)
                if cand.endswith("-ki"):
                    continue
                key = (t["p_number"], cand, line)
                if key in seen:
                    continue
                seen.add(key)
                persons.append({
                    "p_number": t["p_number"],
                    "designation": t.get("designation", ""),
                    "period": t.get("period", ""),
                    "provenience": t.get("provenience", ""),
                    "candidate_name": cand,
                    "line": line,
                    "match_keyword": "me-luh-ha",
                })
    return persons


__all__ = [
    "get_meluhha_tablets",
    "get_meluhha_keyword_counts",
    "get_meluhha_period_counts",
    "get_meluhha_provenience_counts",
    "get_indus_seals_at_mesopotamia",
    "get_meluhhan_persons",
]
