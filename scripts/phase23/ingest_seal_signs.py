"""Phase-23 — Seal sign-sequence ingestion.

Augments
``corpora/downloads/contact_zone/indus_seals_mesopotamia/seals_at_mesopotamia.json``
with two new fields per seal:

  inscription_length   int   Best-published count of Indus signs on
                             the seal. 0 for cuneiform-only / pure
                             iconographic seals.
  indus_signs          list  Sign-ID list. ``"?"`` placeholders are
                             used when the sign sequence is published
                             but the IDs are not yet ingested with
                             confidence (e.g. requires CISI Vol 3
                             plate consultation). Empty list ``[]``
                             when the seal carries no Indus signs.
  signs_confidence     str   ``"high"`` (sign IDs from cited source),
                             ``"length_only"`` (count published, IDs
                             pending), ``"none"`` (no Indus signs).
  signs_source         str   Citation for the sign-sequence reading.

This is the WARP.md G1 acceptable-exception data-ingestion script that
unblocks the Phase-23 ``EnhancedNameMatcher`` and ``BilingualReadoutTest``
graph nodes.
"""

from __future__ import annotations

import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SEALS_JSON = (
    _ROOT / "corpora" / "downloads" / "contact_zone"
    / "indus_seals_mesopotamia" / "seals_at_mesopotamia.json"
)


# Hand-curated overlay: catalogue_id -> sign-sequence augmentation.
# Conservative: where Parpola/Frenez/CISI publish a definitive count
# but not (or only partially) the Parpola/Mahadevan IDs, we use "?"
# placeholders of the correct length. The matcher's length-score
# operates on count, not IDs.
_OVERLAY: dict[str, dict] = {
    "AO_22310": {
        # Possehl 2006 / Parpola 1977: this is a *cuneiform-only*
        # Akkadian seal. The text reads "Shu-ilishu, EME.BAL.ME.LUH.HA.KI"
        # ("Shu-ilishu, interpreter of Meluhha"). It is NOT an Indus
        # seal and carries no Indus signs.
        "inscription_length": 0,
        "indus_signs": [],
        "signs_confidence": "none",
        "signs_source": "Possehl 2006 (Expedition 48:1) — cuneiform-only",
    },
    "BM_122187_UR_seal_1": {
        # Gadd 1932 / Frenez 2018: round Ur seal with zebu motif and
        # a 5-sign Indus inscription.
        "inscription_length": 5,
        "indus_signs": ["?", "?", "?", "?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "Gadd 1932 (Iraq); Frenez 2018 plate IV",
    },
    "GADD_1": {
        # Gadd 1932 #1 / Parpola 1994 corpus #2050: short 3-sign Indus
        # inscription on a square Ur seal.
        "inscription_length": 3,
        "indus_signs": ["?", "?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "Gadd 1932 #1; Laursen 2010 PCA classification",
    },
    "GADD_2": {
        # Gadd 1932 #2: 4-sign Indus inscription.
        "inscription_length": 4,
        "indus_signs": ["?", "?", "?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "Gadd 1932 #2; Laursen 2010",
    },
    "ASMAR_TA": {
        # Tell Asmar TA seal — Mallowan 1947 / Wheeler 1968: 3-sign
        # short inscription with bull motif.
        "inscription_length": 3,
        "indus_signs": ["?", "?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "Mallowan 1947 (Iraq); Wheeler 1968",
    },
    "KISH_INDUS_1": {
        # Kish square seal (Ashmolean) — short ~3-sign inscription.
        "inscription_length": 3,
        "indus_signs": ["?", "?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "Mallowan 1947; CISI Vol 3 (pending plate)",
    },
    "SUSA_INDUS_1": {
        # Susa-found Indus seal (Louvre) — typically 4 signs.
        "inscription_length": 4,
        "indus_signs": ["?", "?", "?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "Wheeler 1968; Possehl 2002",
    },
    "LOTHAL_PERSIAN_GULF_SEAL": {
        # Lothal Persian-Gulf-type circular seal (Rao 1963): only
        # 1 short Indus sign group.
        "inscription_length": 2,
        "indus_signs": ["?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "Rao 1963 (Antiquity 37); Laursen 2010",
    },
    "FAILAKA_KM_1113": {
        # Failaka Dilmun-style seal (David-Cuny & Neyme 2016) carrying
        # Indus signs in the distinctive 'twins' Persian-Gulf style.
        "inscription_length": 4,
        "indus_signs": ["?", "?", "?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "David-Cuny & Neyme 2016 (Failaka Vol 2)",
    },
    "VA_243_BERLIN": {
        # Berlin VA 243 — markhor + Indus hieroglyphs, ~5 signs.
        "inscription_length": 5,
        "indus_signs": ["?", "?", "?", "?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "Kalyanaraman ANE; Frenez 2018",
    },
    "KONAR_SANDAL_S_CYLINDER": {
        # Konar Sandal South cylinder — purely iconographic, no
        # Indus signs.
        "inscription_length": 0,
        "indus_signs": [],
        "signs_confidence": "none",
        "signs_source": "Vidale & Frenez 2015 — iconographic-only",
    },
    "JALALABAD_FARS": {
        # Vidale, Desset & Frenez 2021: 4-sign Indus sequence.
        "inscription_length": 4,
        "indus_signs": ["?", "?", "?", "?"],
        "signs_confidence": "length_only",
        "signs_source": "Vidale, Desset & Frenez 2021; Ascalone 2008",
    },
    "AL_MAQSHA_TOKEN_2": {
        # Laursen et al. 2026 JNES: Akkadian inscription "Yagli'el,
        # servant of the goddess Panipa". No Indus signs.
        "inscription_length": 0,
        "indus_signs": [],
        "signs_confidence": "none",
        "signs_source": "Laursen et al. 2026 JNES — Akkadian-only",
    },
}


def main() -> None:
    if not _SEALS_JSON.exists():
        raise SystemExit(f"Seals JSON not found: {_SEALS_JSON}")
    data = json.loads(_SEALS_JSON.read_text(encoding="utf-8"))
    seals = data.get("seals") or []
    if not seals:
        raise SystemExit("Seals JSON has no 'seals' array")

    n_updated = 0
    n_with_signs = 0
    n_without = 0
    total_signs = 0
    for seal in seals:
        cid = seal.get("catalogue_id")
        overlay = _OVERLAY.get(cid or "")
        if not overlay:
            # Default for unmapped seals: 0 signs, none confidence
            seal.setdefault("inscription_length", 0)
            seal.setdefault("indus_signs", [])
            seal.setdefault("signs_confidence", "unknown")
            seal.setdefault("signs_source", "")
            continue
        seal["inscription_length"] = overlay["inscription_length"]
        seal["indus_signs"] = list(overlay["indus_signs"])
        seal["signs_confidence"] = overlay["signs_confidence"]
        seal["signs_source"] = overlay["signs_source"]
        n_updated += 1
        if seal["inscription_length"] > 0:
            n_with_signs += 1
            total_signs += seal["inscription_length"]
        else:
            n_without += 1

    # Update the wrapper meta block
    data.setdefault("metadata", {})
    data["metadata"]["phase23_sign_ingestion"] = {
        "n_seals": len(seals),
        "n_updated": n_updated,
        "n_with_signs": n_with_signs,
        "n_without_signs": n_without,
        "total_indus_signs": total_signs,
        "method": (
            "Hand-curated overlay from Parpola 1994, Frenez 2018, "
            "Gadd 1932, Mallowan 1947, Vidale/Desset/Frenez 2021, "
            "David-Cuny/Neyme 2016, Laursen 2010 + 2026. Sign IDs "
            "placeheld with '?' pending CISI Vol 3 plate ingestion."
        ),
    }

    _SEALS_JSON.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Updated {n_updated}/{len(seals)} seals.")
    print(f"  with Indus signs:  {n_with_signs} (total {total_signs} signs)")
    print(f"  without:           {n_without}")
    print(f"Wrote {_SEALS_JSON}")


if __name__ == "__main__":
    main()
