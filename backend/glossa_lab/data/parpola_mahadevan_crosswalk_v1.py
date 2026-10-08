"""Parpola<->Mahadevan sign crosswalk v1 loader (Phase-122).

Loads the committed crosswalk built by
``backend/scripts/phase122_build_crosswalk_mayig.py`` from
``data/crosswalks/parpola_mahadevan_crosswalk_v1.json``.

Design rules (inherited from indus_sign_crosswalk.py):
  - source sign IDs are preserved exactly; this is a LOOKUP,
    not a rewrite;
  - splits/merges are multiple rows — never silently collapsed
    to a forced 1:1;
  - where sources disagree, both mappings are present and the
    rows carry ``conflict: true`` with the dissenting source
    named in ``conflict_detail``;
  - confidence is per the frozen v1 rubric (see the builder):
    high = canonical registry AND mayig features agree;
    medium = exactly one of those two; low = crosswalk_v2-only
    (the map spec 018 rejected as canonical) or candidate-only
    (no explicit source).

The crosswalk is a working v1 with stated confidence. It is
NOT an adjudication of sign identity, and no anchor status
implication follows from any row.
"""
from __future__ import annotations

import json
from pathlib import Path

_PATH = (Path(__file__).resolve().parents[3] / "data" / "crosswalks"
         / "parpola_mahadevan_crosswalk_v1.json")
_CACHE: dict | None = None


def _load() -> dict:
    global _CACHE  # noqa: PLW0603
    if _CACHE is None:
        if not _PATH.exists():
            raise FileNotFoundError(
                f"crosswalk v1 not found at {_PATH}; run "
                "backend/scripts/phase122_build_crosswalk_mayig.py")
        _CACHE = json.loads(_PATH.read_text(encoding="utf-8"))
    return _CACHE


def load_crosswalk() -> list[dict]:
    """All crosswalk rows (pair rows + unmapped-P rows)."""
    return list(_load()["rows"])


def crosswalk_stats() -> dict:
    return dict(_load()["stats"])


def p_to_m(parpola_id: str, min_confidence: str = "low") -> list[str]:
    """All M signs asserted for a P sign at >= min_confidence.

    Returns a sorted list — possibly several (split/merge) or
    empty (unmapped). Never invents a mapping.
    """
    order = {"low": 0, "medium": 1, "high": 2}
    floor = order[min_confidence]
    return sorted({r["mahadevan_id"] for r in _load()["rows"]
                   if r["parpola_id"] == parpola_id
                   and r["mahadevan_id"]
                   and order.get(r["confidence"], -1) >= floor})


def m_to_p(mahadevan_id: str, min_confidence: str = "low") -> list[str]:
    """All P signs asserted for an M sign at >= min_confidence."""
    order = {"low": 0, "medium": 1, "high": 2}
    floor = order[min_confidence]
    return sorted({r["parpola_id"] for r in _load()["rows"]
                   if r["mahadevan_id"] == mahadevan_id
                   and order.get(r["confidence"], -1) >= floor})


def conflicts() -> list[dict]:
    """Rows flagged as source disagreements (both sides kept)."""
    return [r for r in _load()["rows"] if r["conflict"]]


def unmapped_p_signs() -> list[str]:
    return sorted(r["parpola_id"] for r in _load()["rows"]
                  if r["relation_type"] == "unmapped")


def unmapped_m_signs() -> list[str]:
    return list(_load()["m_unmapped"])
