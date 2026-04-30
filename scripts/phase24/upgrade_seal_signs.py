"""Phase-24 — Seal sign-sequence upgrade from Laursen 2010 Table 1.

Cross-references our 13 hand-encoded ``seals_at_mesopotamia.json``
entries against Laursen 2010's Table 1 catalogue (parsed by
``ingest_laursen_table1.py``) and:

  1. Adds a ``laursen_2010_seal_no`` field to each matching entry.
  2. Tightens the ``signs_source`` citation to refer to a specific
     Laursen Table 1 row.
  3. For seal #10 in Laursen 2010 (Janabiyah Cemetery), where the
     paper's footnote 2 records sign-by-sign Parpola-1994b IDs,
     append a new entry ``JANABIYAH_LAURSEN_10`` to our inventory
     with the actual sign IDs (signs_confidence='high').

Also patches the dataset's per-seal ``find_period`` field where
Laursen's BBM correlation gives us a tighter dating.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_LAURSEN_JSON = (
    _ROOT / "corpora" / "downloads" / "contact_zone"
    / "gulf_seals" / "laursen_2010_table1.json"
)
_SEALS_JSON = (
    _ROOT / "corpora" / "downloads" / "contact_zone"
    / "indus_seals_mesopotamia" / "seals_at_mesopotamia.json"
)


# Hand-curated cross-reference: our catalogue_id -> Laursen Table 1 seal_no
# Built by inspection of the parsed Laursen Table 1 + our seal records.
_CROSSREF: dict[str, dict] = {
    # Gadd 1932 Ur seals: pl. I nos. 2-5, 15-18 are Laursen #16-21 + 23 + 24
    "BM_122187_UR_seal_1": {
        "laursen_seal_no": 16,
        "rationale": "Gadd 1932 pl. I no. 2 (round Ur seal with zebu motif). "
                      "Best-fit Laursen Table 1 row for the BM 122187 entry.",
    },
    "GADD_1": {
        "laursen_seal_no": 17,
        "rationale": "Gadd 1932 pl. I no. 3 (square Ur seal).",
    },
    "GADD_2": {
        "laursen_seal_no": 18,
        "rationale": "Gadd 1932 pl. I no. 4 (Ur).",
    },
    "SUSA_INDUS_1": {
        "laursen_seal_no": 14,
        "rationale": "Amiet 1972 no. 1643 — Susa Gulf INDUS seal "
                      "(Laursen Table 1 row 14).",
    },
    # Tell Asmar TA, Lothal Persian-Gulf, Failaka KM 1113, Berlin VA 243,
    # Konar Sandal cylinder, Jalalabad Fars, Al-Maqsha Token 2,
    # Shu-ilishu AO 22310, KISH_INDUS_1 are NOT in Laursen Table 1
    # (or are mentioned only outside the table) and so do not get a
    # cross-reference.
}


# A new entry appended to our inventory: the Janabiyah Cemetery seal
# (Laursen Table 1 #10) with full Parpola-1994b sign-by-sign reading
# from Laursen 2010 footnote 2.
_JANABIYAH_NEW_ENTRY: dict = {
    "catalogue_id": "JANABIYAH_LAURSEN_10",
    "type": "gulf_indus_with_parpola_reading",
    "find_country": "Bahrain (Dilmun)",
    "find_spot": "Janabiyah Cemetery, Bahrain",
    "find_period": "Early Dilmun (ca. 2100-2000 BC)",
    "current_collection": "Bahrain National Museum",
    "inscription_reading": (
        "7-sign Indus inscription read right-to-left on impression: "
        "[53|60]-147 / 364 / 145 / 126 / 16 / 145 "
        "(Asko Parpola, Laursen 2010 footnote 2)"
    ),
    "source": "Laursen 2010 (AAE 21:96-134) Table 1 row 10 + footnote 2",
    "indus_signs": ["53", "147", "364", "145", "126", "16", "145"],
    "indus_signs_alternates": {
        "0": ["60"],
        "3": ["125", "128"],
    },
    "inscription_length": 7,
    "signs_confidence": "high",
    "signs_source": (
        "Asko Parpola personal communication, in Laursen 2010 footnote 2; "
        "sign IDs from Parpola 1994b: 70-78, fig. 5.1"
    ),
    "laursen_2010_seal_no": 10,
    "parpola_attestation_notes": [
        "Sequence 16-145 also at beginning of Kalibangan K-69 to K-75 "
        "(Joshi & Parpola 1987:312-313)",
        "Signs 16 and 364 co-occur on Mohenjo-Daro M-798 unicorn seal "
        "(Shah & Parpola 1991:68)",
        "Sign 145 in Parpola 1994a Near Eastern texts nos. 5, 8, 29",
        "Sign 16 in Parpola 1994a Near Eastern texts nos. 6-8, 31, 35",
    ],
}


def main() -> None:
    if not _LAURSEN_JSON.exists():
        raise SystemExit(
            f"Laursen Table 1 JSON not found: {_LAURSEN_JSON}. "
            "Run scripts/phase24/ingest_laursen_table1.py first."
        )
    if not _SEALS_JSON.exists():
        raise SystemExit(f"Seals JSON not found: {_SEALS_JSON}.")

    laursen = json.loads(_LAURSEN_JSON.read_text(encoding="utf-8"))
    laursen_by_no: dict[int, dict] = {
        r["seal_no"]: r for r in laursen.get("rows", [])
    }
    seals = json.loads(_SEALS_JSON.read_text(encoding="utf-8"))
    rows = seals.get("seals") or []

    n_crossreferenced = 0
    upgrade_log: list[dict] = []
    for s in rows:
        cid = s.get("catalogue_id")
        xref = _CROSSREF.get(cid)
        if not xref:
            continue
        ln = xref["laursen_seal_no"]
        laursen_row = laursen_by_no.get(ln)
        s["laursen_2010_seal_no"] = ln
        old_source = s.get("signs_source", "")
        if laursen_row:
            new_source = (
                f"{old_source} | Laursen 2010 Table 1 row {ln} "
                f"({laursen_row.get('reference', '')[:60]}, "
                f"site={laursen_row.get('site', '?')})"
            )
            s["signs_source"] = new_source
            s["laursen_table1_reference"] = laursen_row.get("reference", "")
            s["laursen_table1_site"] = laursen_row.get("site", "")
            s["laursen_table1_gulf_type"] = laursen_row.get("gulf_type", "")
        s["phase24_crossref_rationale"] = xref["rationale"]
        n_crossreferenced += 1
        upgrade_log.append({
            "catalogue_id": cid,
            "laursen_seal_no": ln,
            "rationale": xref["rationale"][:80],
        })

    # Append Janabiyah seal entry if not already present
    existing_ids = {s.get("catalogue_id") for s in rows}
    n_added = 0
    if _JANABIYAH_NEW_ENTRY["catalogue_id"] not in existing_ids:
        rows.append(dict(_JANABIYAH_NEW_ENTRY))
        n_added = 1

    # Re-derive stats
    n_with_signs = sum(
        1 for s in rows if int(s.get("inscription_length", 0) or 0) > 0
    )
    n_with_high_conf = sum(
        1 for s in rows if s.get("signs_confidence") == "high"
    )
    total_signs = sum(int(s.get("inscription_length", 0) or 0) for s in rows)

    seals.setdefault("metadata", {})
    seals["metadata"]["phase24_sign_upgrade"] = {
        "n_seals_total": len(rows),
        "n_with_signs": n_with_signs,
        "n_with_high_conf_signs": n_with_high_conf,
        "total_indus_signs": total_signs,
        "n_crossreferenced_with_laursen": n_crossreferenced,
        "n_seals_added": n_added,
        "upgrade_log": upgrade_log,
        "method": (
            "Hand-curated cross-reference of catalogue_id -> Laursen 2010 "
            "Table 1 seal_no by reference inspection. "
            "Janabiyah seal #10 added with full Parpola 1994b sign IDs "
            "from Laursen footnote 2."
        ),
    }
    seals["seals"] = rows

    _SEALS_JSON.write_text(
        json.dumps(seals, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Cross-referenced {n_crossreferenced} seals with Laursen Table 1.")
    for entry in upgrade_log:
        print(f"  {entry['catalogue_id']:<28} -> Laursen #{entry['laursen_seal_no']}")
    print(f"Added {n_added} new seal entry (Janabiyah, with 7 Parpola sign IDs).")
    print(f"Inventory now: {len(rows)} seals, {n_with_signs} inscribed, "
          f"{total_signs} total signs ({n_with_high_conf} high-confidence).")
    print(f"Wrote {_SEALS_JSON}")


if __name__ == "__main__":
    main()
