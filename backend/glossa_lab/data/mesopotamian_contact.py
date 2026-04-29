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
    found in Mesopotamia, Iran, and the Persian Gulf.

    Phase-23 augments each seal with ``inscription_length``,
    ``indus_signs`` (placeholder list of length N), ``signs_confidence``
    and ``signs_source`` fields. See
    ``scripts/phase23/ingest_seal_signs.py``.
    """
    return list(_load_indus_seals_at_mesopotamia_data().get("seals") or [])


def get_seals_with_inscription() -> list[dict]:
    """Return only the subset of seals that carry Indus signs
    (``inscription_length > 0``). Phase-23."""
    return [
        s for s in get_indus_seals_at_mesopotamia()
        if int(s.get("inscription_length", 0) or 0) > 0
    ]


def get_seal_sign_metadata() -> dict:
    """Return Phase-23 sign-ingestion metadata block (counts, method)."""
    md = _load_indus_seals_at_mesopotamia_data().get("metadata") or {}
    return md.get("phase23_sign_ingestion") or {}


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


# ── Phase-23: refined Meluhhan-name extractor ────────────────────────
#
# The Phase-22 heuristic returned every hyphenated token, which was
# dominated by Akkadian particles ('a-na', 'i-na', 'a-di'...) and
# Sumerian content words. Phase-23 replaces it with a strict pipeline:
#
#   1. Drop any candidate that appears in the Akkadian-particle /
#      Sumerian-function-word stoplist.
#   2. Accept a candidate only if it satisfies AT LEAST ONE of:
#        a) prefixed with `lu2-`, `lu-`, or `dumu-` (canonical PN
#           prefixes in Sumerian);
#        b) suffixed with `-me-luh-ha`, `-me-luh-ha-ki`, or
#           `-meluhha-ki` (the "of Meluhha" attribution suffix);
#        c) explicitly matches one of the historically-attested
#           Meluhhan personal names (Lu-sun-zi-da, Shu-ilishu, etc.).
#   3. Reject candidates that consist entirely of digits-with-hyphens
#      ("3-disz", "1-szar") — these are number constructions, not PNs.

# Common Akkadian particles, prepositions, conjunctions, and frequent
# Sumerian function words that should never be treated as personal
# names. Built from the Phase-22b top-50 noise list + standard
# Akkadian-grammar stop tokens.
_AKKADIAN_STOPLIST: frozenset[str] = frozenset({
    # Akkadian particles + prepositions
    "a-na", "i-na", "a-di", "u3", "u2", "sza", "sza2", "isz-tu",
    "ul-tu", "ul-tu2", "ki-i", "ki-ma", "la", "la-a", "u-la",
    "u-ul", "asz-szum", "asz-szu2", "ma-har", "qe2-reb", "qe-reb",
    "i-na-an-na", "i-da-a", "e-li", "e-le-nu", "szap-la", "sza-pal",
    "e-mu-qi2", "e-mu-qi", "e-mu-qa", "ni-bi", "ni-ba",
    # Akkadian frequent verb fragments
    "u-sza2-asz2-kin", "u2-sza2-as,-bi-ta", "usz-te-sze-ra",
    "ik-szu-du", "ip-lah", "il-li-ku", "ik-te-ru-nim-ma",
    "ad-ke-e-ma", "al-lik", "e-pu-szu", "u2-sza2-asz2-kin",
    # Akkadian noun fragments / suffixes
    "mu-s", "mu-s,ur", "mu-s,u-ri", "mu-s,u-ra-a-a",
    "u-su-un", "u-ra-a-a", "szu2-un", "sza2-szu2-un",
    "bal-t", "bal-t,u-su-un", "bal-tu-su-un", "re-s,u-szu2-un",
    "har-ra-nu", "tam-ha-ri", "tam-ha-ru", "an-zil-li",
    "szu-min", "szu-min-a-a", "_szu-min_-a-a", "sza3", "_sza3_",
    # Sumerian content words / determinatives
    "gigir-mesz", "ansze-kur-ra", "ansze-kur-ra-mesz", "erin2-mesz",
    "_erin2-mesz_", "_{lu2}erin2-mesz", "dumu-mesz", "lugal-mesz",
    "i3-dub", "mes-me-luh-ha", "ma2-kan", "ma2-gan", "i-dux",
    "lu-dux", "dam-gar3", "lugal-sa", "lugal-i-de6-a", "ki-min",
    "ab-ba", "ab-ba-mesz", "gu2-ab-ba", "a-ab-ba",
    "gesz-pan", "gesz-gigir-mesz", "_gesz_pan", "_gesz_gigir-mesz_",
    "muru2", "_muru2_", "karasz", "_karasz_", "lu2", "lugal",
    "en", "_lu2", "_lu2}en", "_lu2_",
    # Misc fragments observed in the Phase-22b top list
    "ka-bal", "sze-ga", "ma-ru", "a-na-asz", "la-bi", "ka-tar",
})


_PN_PREFIX_RE = re.compile(
    r"\b(?P<full>(?:lu2|lu|dumu)-(?:[a-z][a-z0-9']*)(?:-[a-z][a-z0-9']*){0,4})\b",
    re.IGNORECASE,
)
_PN_MELUHHA_SUFFIX_RE = re.compile(
    r"\b(?P<full>(?:[a-z][a-z0-9']*)(?:-[a-z][a-z0-9']*){0,4}-me-luh-?ha(?:-ki)?)\b",
    re.IGNORECASE,
)
_DIGIT_TOKEN_RE = re.compile(r"^[0-9]+(?:-[0-9a-z]+)*$")

# Historically-attested Meluhhan personal names (Sumerian / Akkadian
# transcription). Always accepted when seen in a me-luh-ha-mention
# line, regardless of the structural rules above.
_KNOWN_MELUHHAN_NAMES: frozenset[str] = frozenset({
    "lu-sun-zi-da", "lu2-sun-zi-da",
    "shu-ilishu", "shu-i-li-szu", "szu-i-li-szu", "shu-ilisu",
    "su-ilisu", "shu-i-li-shu",
    "ur-{d}lamma-meluhha", "ur-lamma-me-luh-ha",
    "za-bar-da-bi", "ses-kal-la-me-luh-ha",
    "ur-{d}suen-me-luh-ha", "ur-suen-me-luh-ha",
})


def _is_personal_name_candidate(token: str) -> bool:
    """True iff *token* satisfies the Phase-23 strict PN heuristic."""
    t = token.lower().strip()
    if not t or t in _AKKADIAN_STOPLIST:
        return False
    if _DIGIT_TOKEN_RE.match(t):
        return False
    if t in _KNOWN_MELUHHAN_NAMES:
        return True
    if _PN_PREFIX_RE.fullmatch(t):
        return True
    if _PN_MELUHHA_SUFFIX_RE.fullmatch(t):
        return True
    return False


def get_meluhhan_persons_strict() -> list[dict]:
    """Strict Phase-23 Meluhhan personal-name extractor.

    For each tablet line that contains ``me-luh-ha`` we scan for two
    candidate patterns:

      - the *prefix pattern* ``(lu2|lu|dumu)-X[-Y[-Z[-W[-V]]]]``
        (the canonical Sumerian PN morphology), and
      - the *suffix pattern* ``X[-Y[-Z]]-me-luh-ha[-ki]`` (the
        "X of Meluhha" attribution).

    Candidates that fall in ``_AKKADIAN_STOPLIST`` or that are pure
    digit-and-hyphen tokens are dropped. Historically-attested
    Meluhhan personal names (``_KNOWN_MELUHHAN_NAMES``) are always
    surfaced when seen.

    Output: list of {p_number, period, provenience, candidate_name,
    line, source_pattern, is_known}.
    """
    persons: list[dict] = []
    seen: set[tuple[str, str, str]] = set()
    for t in get_meluhha_tablets():
        kw = " ".join(t.get("matched_keywords") or []).lower()
        if "me-luh" not in kw:
            continue
        for line in t.get("atf_lines_with_match") or []:
            ll = line.lower()
            if "me-luh" not in ll:
                continue
            for regex, pattern in (
                (_PN_PREFIX_RE,         "prefix:lu2/lu/dumu"),
                (_PN_MELUHHA_SUFFIX_RE, "suffix:-me-luh-ha"),
            ):
                for m in regex.finditer(ll):
                    cand = m.group("full")
                    if not _is_personal_name_candidate(cand):
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
                        "source_pattern": pattern,
                        "is_known": cand.lower() in _KNOWN_MELUHHAN_NAMES,
                    })
    return persons


__all__ = [
    "get_meluhha_tablets",
    "get_meluhha_keyword_counts",
    "get_meluhha_period_counts",
    "get_meluhha_provenience_counts",
    "get_indus_seals_at_mesopotamia",
    "get_seals_with_inscription",
    "get_seal_sign_metadata",
    "get_meluhhan_persons",
    "get_meluhhan_persons_strict",
]
