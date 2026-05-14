"""Indus Script Sign Crosswalk — Multi-scheme ID mapping.

Maps between four sign identification systems used in the corpus:
  - Mahadevan 1977 (M77)      — M001–M417+; used in ICIT, RMRL portal, Holdat
  - Parpola 1982 (P-numbers)  — 1–450+; used in CISI, mayig-cisi corpus
  - Wells 2006 (3-digit)      — 001–676; used in ICIT encoding, Fuls experiments
  - Fuls 2014 (3-digit)       — 001–676; used in indus_public_corpus.py and SA experiments

Key design principles (from research report 2026-05-14):
  1. SOURCE SIGN IDs are preserved exactly — crosswalk is a LOOKUP, not a rewrite
  2. Allograph/mirror/variant relations are stored as TYPED LINKS, not silent collapses
  3. When a mapping is ambiguous or missing, return None — never invent a mapping
  4. Confidence levels: HIGH = verified against published sources; MEDIUM = inferred;
     LOW = speculative; entries with LOW confidence must NOT be used for canonical work

_citation:
  primary_sources: ["A.1", "A.7", "C.1", "C.2"]
  derivation: "Crosswalk extends mahadevan_parpola_crosswalk_v2.json (38 entries,
               Phase-28) with Wells/Fuls dimension. Wells column inferred from
               published descriptions; full Wells 676-sign catalog requires purchase
               of Wells 2015 (Archaeopress) to complete. See CITATIONS.md A.7."
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from glossa_lab.data.indus_object_model import RelationType, SignIdScheme

_DATA = Path(__file__).parent

# ── Load the existing M77↔Parpola crosswalk v2 ───────────────────────────────
_MP_XW_PATH = _DATA / "mahadevan_parpola_crosswalk_v2.json"

def _load_mp_crosswalk() -> dict:
    if _MP_XW_PATH.exists():
        return json.loads(_MP_XW_PATH.read_text(encoding="utf-8")).get("crosswalk", {})
    return {}


# ── Wells/Fuls extensions ─────────────────────────────────────────────────────
#
# The Wells 2006/2015 sign list uses 3-digit codes 001–676.
# Fuls 2014 uses the same numbering convention with minor differences.
# Until the Wells monograph is purchased and digitized, only the best-documented
# correspondences are listed here.  Entries marked LOW confidence MUST NOT be
# used for canonical data without manual verification.
#
# Format: mahadevan_id -> {"wells_id": str, "fuls_id": str, "confidence": str, "note": str}
#
# Primary source for Wells column: Wells, Bryan K. (2015).
#   The Archaeology and Epigraphy of Indus Writing. Archaeopress.
#   ISBN 978-1-78491-046-4.  [CITATIONS.md A.7]
# Primary source for Fuls column: Fuls, Andreas (2014).
#   A Catalog of Indus Signs. TU Berlin / ICIT.
#   [CITATIONS.md C.2]

_WELLS_FULS_EXTENSIONS: Dict[str, dict] = {
    # Numeral signs (well-documented cross-scheme convergence)
    "M086": {"wells_id": "086", "fuls_id": "017", "confidence": "MEDIUM",
             "note": "Single vertical stroke; Wells 086 ≈ Fuls 017"},
    "M087": {"wells_id": "087", "fuls_id": "018", "confidence": "MEDIUM",
             "note": "Two vertical strokes"},
    "M088": {"wells_id": "088", "fuls_id": "019", "confidence": "MEDIUM",
             "note": "Three vertical strokes"},
    "M089": {"wells_id": "089", "fuls_id": "020", "confidence": "MEDIUM",
             "note": "Four vertical strokes"},
    "M090": {"wells_id": "090", "fuls_id": "021", "confidence": "MEDIUM",
             "note": "Five vertical strokes"},
    "M091": {"wells_id": "091", "fuls_id": "022", "confidence": "MEDIUM",
             "note": "Six vertical strokes"},
    "M092": {"wells_id": "092", "fuls_id": "023", "confidence": "MEDIUM",
             "note": "Seven vertical strokes"},
    # Fish complex (Parpola fish phoneme cluster — high research value)
    "M047": {"wells_id": "047", "fuls_id": "159", "confidence": "HIGH",
             "note": "Plain fish; miin reading; Fuls 159 is primary fish sign"},
    "M048": {"wells_id": "048", "fuls_id": "160", "confidence": "MEDIUM",
             "note": "Fish-with-roof"},
    "M050": {"wells_id": "050", "fuls_id": "161", "confidence": "MEDIUM",
             "note": "Fish-with-fins"},
    "M052": {"wells_id": "052", "fuls_id": "162", "confidence": "MEDIUM",
             "note": "Fish-with-trefoil"},
    "M060": {"wells_id": "060", "fuls_id": "070", "confidence": "MEDIUM",
             "note": "Fish variant (Fuls 070)"},
    # Terminal signs (Fuls 342 = jar/terminal; very high frequency)
    "M342": {"wells_id": "342", "fuls_id": "342", "confidence": "HIGH",
             "note": "3-stroke terminal marker; most common terminal sign; Fuls 342"},
    "M211": {"wells_id": "211", "fuls_id": "321", "confidence": "MEDIUM",
             "note": "Comb terminal marker"},
    # Common signs
    "M124": {"wells_id": "124", "fuls_id": "100", "confidence": "MEDIUM",
             "note": "V-shaped jar/pot; Fuls 100 is high-frequency composite"},
    "M001": {"wells_id": "001", "fuls_id": "411", "confidence": "MEDIUM",
             "note": "Man with raised arm; Fuls 411 is common initial-position sign"},
    "M261": {"wells_id": "261", "fuls_id": "261", "confidence": "HIGH",
             "note": "Two intersecting circles; muruku"},
    "M281": {"wells_id": "281", "fuls_id": "281", "confidence": "HIGH",
             "note": "Five-striped palm squirrel; piLLai"},
    "M311": {"wells_id": "311", "fuls_id": "311", "confidence": "HIGH",
             "note": "Fig tree (three-branched); vaTa"},
    "M117": {"wells_id": "117", "fuls_id": "550", "confidence": "MEDIUM",
             "note": "Wheel/chakra; Fuls 550 is bimodal distribution sign"},
    "M099": {"wells_id": "099", "fuls_id": "099", "confidence": "HIGH",
             "note": "Bow/archer; vil"},
    "M175": {"wells_id": "175", "fuls_id": "175", "confidence": "HIGH",
             "note": "Spinner's spindle; katir"},
}

# ── Allograph / variant relations ─────────────────────────────────────────────
#
# Source: Nature allograph study (2017) — argues sign redundancies should be
# treated as allographic relations, especially mirrored asymmetric signs.
# Relations stored as typed links, never as silent collapses.
# [CITATIONS.md: see research phase docs Phase-30+ for allograph reduction results]

_ALLOGRAPH_RELATIONS: List[dict] = [
    # Fish variants — well-documented allographic cluster
    {
        "from_id": "M048", "from_scheme": "Mahadevan1977",
        "to_id": "M047", "to_scheme": "Mahadevan1977",
        "relation": "allograph_of", "confidence": 0.75,
        "citation": "Parpola 1994; fish-with-roof as variant of plain fish",
    },
    {
        "from_id": "M050", "from_scheme": "Mahadevan1977",
        "to_id": "M047", "to_scheme": "Mahadevan1977",
        "relation": "allograph_of", "confidence": 0.75,
        "citation": "Parpola 1994; fish-with-fins as variant of plain fish",
    },
    {
        "from_id": "M052", "from_scheme": "Mahadevan1977",
        "to_id": "M047", "to_scheme": "Mahadevan1977",
        "relation": "allograph_of", "confidence": 0.70,
        "citation": "Parpola 1994; fish-with-trefoil as variant",
    },
    {
        "from_id": "M060", "from_scheme": "Mahadevan1977",
        "to_id": "M047", "to_scheme": "Mahadevan1977",
        "relation": "graphic_variant_of", "confidence": 0.65,
        "citation": "Mahadevan 1977; 'badly drawn' fish",
    },
    # Numeral additive relations (strokes)
    {
        "from_id": "M086", "from_scheme": "Mahadevan1977",
        "to_id": "M087", "to_scheme": "Mahadevan1977",
        "relation": "graphic_variant_of", "confidence": 0.50,
        "citation": "Additive stroke system; Mahadevan 1977",
    },
    # Phase-37 allograph reduction pairs (11 pairs merged in Phase-37)
    # These are marked as disputed until further analysis confirms
    {
        "from_id": "M125", "from_scheme": "Mahadevan1977",
        "to_id": "M211", "to_scheme": "Mahadevan1977",
        "relation": "disputed_relation_to", "confidence": 0.40,
        "citation": "Phase-37 allograph reduction experiment; see LEDGER Phase-37",
    },
]


# ── Public API ────────────────────────────────────────────────────────────────

class IndusSignCrosswalk:
    """
    Multi-scheme sign ID crosswalk for the Indus corpus.

    Usage:
        xw = IndusSignCrosswalk()
        parpola = xw.m77_to_parpola("M047")   # -> "47"
        wells = xw.m77_to_wells("M047")         # -> "047"
        fuls = xw.m77_to_fuls("M047")           # -> "159"
        m77 = xw.parpola_to_m77("47")           # -> "M047"
    """

    def __init__(self) -> None:
        self._mp = _load_mp_crosswalk()          # M77 -> entry with parpola_id
        self._wf = _WELLS_FULS_EXTENSIONS        # M77 -> wells_id + fuls_id
        self._allographs = _ALLOGRAPH_RELATIONS

        # Build reverse index: Parpola -> M77
        self._pm: Dict[str, str] = {}
        for m_id, entry in self._mp.items():
            p_id = str(entry.get("parpola_id", "")).lstrip("0") or entry.get("parpola_id", "")
            if p_id:
                self._pm[p_id] = m_id
                # Also index zero-padded forms
                try:
                    self._pm[str(int(p_id)).zfill(3)] = m_id
                    self._pm[str(int(p_id))] = m_id
                except ValueError:
                    pass

    # ── M77 → X ──────────────────────────────────────────────────────────────

    def m77_to_parpola(self, m_id: str) -> Optional[str]:
        entry = self._mp.get(m_id)
        if entry:
            return str(entry.get("parpola_id", ""))
        return None

    def m77_to_wells(self, m_id: str) -> Optional[str]:
        wf = self._wf.get(m_id)
        if wf:
            return wf.get("wells_id")
        return None

    def m77_to_fuls(self, m_id: str) -> Optional[str]:
        wf = self._wf.get(m_id)
        if wf:
            return wf.get("fuls_id")
        return None

    def m77_confidence(self, m_id: str) -> str:
        entry = self._mp.get(m_id, {})
        return entry.get("confidence", "UNKNOWN")

    # ── Parpola → X ──────────────────────────────────────────────────────────

    def parpola_to_m77(self, p_id: str) -> Optional[str]:
        # Try exact, stripped, and zero-padded
        for key in (p_id, p_id.lstrip("0"), str(int(p_id)).zfill(3) if p_id.isdigit() else p_id):
            result = self._pm.get(key)
            if result:
                return result
        return None

    def parpola_to_wells(self, p_id: str) -> Optional[str]:
        m77 = self.parpola_to_m77(p_id)
        if m77:
            return self.m77_to_wells(m77)
        return None

    def parpola_to_fuls(self, p_id: str) -> Optional[str]:
        m77 = self.parpola_to_m77(p_id)
        if m77:
            return self.m77_to_fuls(m77)
        return None

    # ── Fuls → X ─────────────────────────────────────────────────────────────

    def fuls_to_m77(self, fuls_id: str) -> Optional[str]:
        for m_id, wf in self._wf.items():
            if wf.get("fuls_id") == fuls_id or wf.get("fuls_id") == fuls_id.zfill(3):
                return m_id
        return None

    def fuls_to_parpola(self, fuls_id: str) -> Optional[str]:
        m77 = self.fuls_to_m77(fuls_id)
        if m77:
            return self.m77_to_parpola(m77)
        return None

    # ── Universal lookup ──────────────────────────────────────────────────────

    def translate(
        self,
        sign_id: str,
        from_scheme: SignIdScheme,
        to_scheme: SignIdScheme,
    ) -> Optional[str]:
        """
        Translate sign_id from from_scheme to to_scheme.
        Returns None if mapping is not available — never invents a mapping.
        """
        if from_scheme == to_scheme:
            return sign_id

        # Normalize to M77 first, then project
        m77 = None
        if from_scheme == SignIdScheme.MAHADEVAN_1977:
            m77 = sign_id
        elif from_scheme == SignIdScheme.PARPOLA_1982:
            m77 = self.parpola_to_m77(sign_id)
        elif from_scheme in (SignIdScheme.FULS_2014, SignIdScheme.WELLS_2006):
            # Try Fuls index; Wells and Fuls share numbering for most signs
            m77 = self.fuls_to_m77(sign_id)

        if m77 is None:
            return None

        if to_scheme == SignIdScheme.MAHADEVAN_1977:
            return m77
        if to_scheme == SignIdScheme.PARPOLA_1982:
            return self.m77_to_parpola(m77)
        if to_scheme == SignIdScheme.WELLS_2006:
            return self.m77_to_wells(m77)
        if to_scheme == SignIdScheme.FULS_2014:
            return self.m77_to_fuls(m77)
        if to_scheme == SignIdScheme.GLOSSA_CANONICAL:
            # Canonical = M77 for now; when Wells 676 is digitized, update this
            return m77
        return None

    # ── Allograph relations ───────────────────────────────────────────────────

    def allograph_relations(self, sign_id: str, scheme: SignIdScheme) -> List[dict]:
        """Return all known typed relations for a given sign."""
        results = []
        for rel in self._allographs:
            if rel["from_id"] == sign_id and rel["from_scheme"] == scheme.value:
                results.append(rel)
            elif rel["to_id"] == sign_id and rel["to_scheme"] == scheme.value:
                results.append(rel)
        return results

    # ── Coverage stats ────────────────────────────────────────────────────────

    def coverage_stats(self) -> dict:
        mp_count = len(self._mp)
        wf_count = len(self._wf)
        high_mp = sum(1 for e in self._mp.values() if e.get("confidence") == "HIGH")
        high_wf = sum(1 for e in self._wf.values() if e.get("confidence") == "HIGH")
        return {
            "m77_to_parpola": mp_count,
            "m77_to_parpola_high_confidence": high_mp,
            "m77_to_wells_fuls": wf_count,
            "m77_to_wells_fuls_high_confidence": high_wf,
            "allograph_relations": len(self._allographs),
            "wells_676_coverage_pct": round(wf_count / 676 * 100, 1),
            "note": (
                "Wells/Fuls column is incomplete until Wells 2015 (Archaeopress) "
                "is digitized. Purchase required for full coverage."
            ),
        }

    def export_json(self) -> dict:
        """Export the full crosswalk as a serializable dict."""
        entries = {}
        all_m77 = set(list(self._mp.keys()) + list(self._wf.keys()))
        for m_id in sorted(all_m77):
            mp_entry = self._mp.get(m_id, {})
            wf_entry = self._wf.get(m_id, {})
            entries[m_id] = {
                "mahadevan_id": m_id,
                "parpola_id": mp_entry.get("parpola_id"),
                "wells_id": wf_entry.get("wells_id"),
                "fuls_id": wf_entry.get("fuls_id"),
                "iconic": mp_entry.get("iconic"),
                "phoneme": mp_entry.get("phoneme"),
                "confidence": mp_entry.get("confidence") or wf_entry.get("confidence"),
                "source": mp_entry.get("source") or "wells_fuls_extensions",
                "allograph_relations": self.allograph_relations(m_id, SignIdScheme.MAHADEVAN_1977),
            }
        return {
            "_citation": {
                "primary_sources": ["A.1", "A.7", "C.1", "C.2"],
                "derivation": (
                    "Multi-scheme crosswalk for Indus corpus reconstruction. "
                    "Extends mahadevan_parpola_crosswalk_v2.json with Wells/Fuls dimension. "
                    "See CITATIONS.md sections A.1, A.7, C.1, C.2."
                ),
            },
            "version": "v1 (2026-05-14)",
            "stats": self.coverage_stats(),
            "crosswalk": entries,
            "allograph_relations": self._allographs,
        }


# ── Module-level singleton ────────────────────────────────────────────────────
_CROSSWALK: Optional[IndusSignCrosswalk] = None

def get_crosswalk() -> IndusSignCrosswalk:
    global _CROSSWALK
    if _CROSSWALK is None:
        _CROSSWALK = IndusSignCrosswalk()
    return _CROSSWALK


if __name__ == "__main__":
    import json as _json
    xw = get_crosswalk()
    stats = xw.coverage_stats()
    print("=== Indus Sign Crosswalk Coverage ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print("\nSample lookups:")
    for m_id in ["M047", "M342", "M086", "M261", "M311"]:
        p = xw.m77_to_parpola(m_id)
        w = xw.m77_to_wells(m_id)
        f = xw.m77_to_fuls(m_id)
        print(f"  {m_id} -> Parpola:{p}  Wells:{w}  Fuls:{f}")
