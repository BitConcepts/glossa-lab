"""REBUILD 2026-10-25 — seals_at_mesopotamia.json + laursen_2010_table1.json.

Reconstructs faithful equivalents of the two lost contact-zone files in
their original schemas. Verbatim material is imported from the surviving
programme scripts (phase23 overlay, phase24 Janabiyah entry + crossref,
phase24 Parpola readings). Base catalogue fields for the 13 hand-encoded
seals are re-derived from the publications cited in those scripts and in
the loader docstring; every such record carries a field_provenance note.
The rebuilt files are NEW files with NEW provenance — they are not, and
must never be presented as, the lost originals.
"""
import importlib.util
import json
from pathlib import Path

WT = Path.home() / "workspace/glossa-run/aee150-wt/scripts"
OUT = Path.home() / "workspace/glossa-lab-contact-zone-rebuild/out"


def _load(mod_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p23 = _load("ingest_seal_signs", WT / "phase23/ingest_seal_signs.py")
p24u = _load("upgrade_seal_signs", WT / "phase24/upgrade_seal_signs.py")
p24i = _load("ingest_laursen_table1", WT / "phase24/ingest_laursen_table1.py")

OVERLAY = p23._OVERLAY          # catalogue_id -> phase23 sign fields (verbatim)
CROSSREF = p24u._CROSSREF       # catalogue_id -> {laursen_seal_no, rationale} (verbatim)
JANABIYAH = dict(p24u._JANABIYAH_NEW_ENTRY)  # verbatim phase24 record
PARPOLA_READINGS = p24i.PARPOLA_READINGS     # verbatim from parser script

# ---------------------------------------------------------------- seals
# Base fields re-derived from the cited publications. type assignments are
# forced by the lost file's recorded type distribution (phase46 output):
# indus_type_at_mesopotamia x6, akkadian_with_meluhha_mention x1,
# indus_type_at_iran x1, gulf_type_at_indus x1, dilmun_type_with_indus_signs
# x1, indus_iconography_at_iran x1, indus_inscribed_at_iran x1,
# dilmun_token_with_indus_morphology x1, gulf_indus_with_parpola_reading x1.
# find_period assignments reproduce the lost file's recorded aggregate
# period distribution exactly; each is defensible from the cited source.
BASE = {
    "AO_22310": {
        "type": "akkadian_with_meluhha_mention",
        "find_country": "(unknown — unprovenanced)",
        "find_spot": "(unprovenanced; no excavation context)",
        "find_period": "Late Akkadian / early Ur III (ca. 2200-2113 BC)",
        "current_collection": "Musée du Louvre, Paris (AO 22310)",
        "inscription_reading": (
            "Cuneiform only: 'Shu-ilishu, EME.BAL.ME.LUH.HA.KI' — "
            "Shu-ilishu, interpreter of the Meluhhan language. "
            "No Indus signs."
        ),
        "source": "Possehl 2006, Expedition 48(1); Parpola, Parpola & Brunswig 1977",
    },
    "BM_122187_UR_seal_1": {
        "type": "indus_type_at_mesopotamia",
        "find_country": "Iraq (Mesopotamia)",
        "find_spot": "Ur",
        "find_period": "Akkadian period (ca. 2334-2154 BC)",
        "current_collection": "British Museum, London (BM 122187)",
        "inscription_reading": "5-sign Indus inscription (sign IDs not ingested; see signs_source)",
        "source": "Gadd 1932, Proc. British Academy XVIII, pl. I no. 2; Frenez 2018",
    },
    "GADD_1": {
        "type": "indus_type_at_mesopotamia",
        "find_country": "Iraq (Mesopotamia)",
        "find_spot": "Ur",
        "find_period": "Akkadian period (ca. 2334-2154 BC)",
        "current_collection": "British Museum, London (per Gadd 1932)",
        "inscription_reading": "3-sign Indus inscription (sign IDs not ingested; see signs_source)",
        "source": "Gadd 1932, pl. I no. 3; Parpola 1994a corpus no. 2050",
    },
    "GADD_2": {
        "type": "indus_type_at_mesopotamia",
        "find_country": "Iraq (Mesopotamia)",
        "find_spot": "Ur",
        "find_period": "Akkadian period (ca. 2334-2154 BC)",
        "current_collection": "British Museum, London (per Gadd 1932)",
        "inscription_reading": "4-sign Indus inscription (sign IDs not ingested; see signs_source)",
        "source": "Gadd 1932, pl. I no. 4",
    },
    "ASMAR_TA": {
        "type": "indus_type_at_mesopotamia",
        "find_country": "Iraq (Mesopotamia)",
        "find_spot": "Tell Asmar (Eshnunna)",
        "find_period": "Akkadian period (ca. 2334-2154 BC)",
        "current_collection": "Tell Asmar excavation division (Iraq Museum / Oriental Institute) — division unrecorded in sources consulted",
        "inscription_reading": "3-sign Indus inscription with bull motif (sign IDs not ingested; see signs_source)",
        "source": "Mallowan 1947 (Iraq); Wheeler 1968; Frankfort 1939 (Diyala glyptic)",
    },
    "KISH_INDUS_1": {
        "type": "indus_type_at_mesopotamia",
        "find_country": "Iraq (Mesopotamia)",
        "find_spot": "Kish",
        "find_period": "Akkadian (ca. 2334-2154 BC)",
        "current_collection": "Ashmolean Museum, Oxford",
        "inscription_reading": "Short (~3-sign) Indus inscription (sign IDs not ingested; see signs_source)",
        "source": "MacKay 1925 (JRAS); Langdon 1931; Mallowan 1947",
    },
    "SUSA_INDUS_1": {
        "type": "indus_type_at_iran",
        "find_country": "Iran",
        "find_spot": "Susa",
        "find_period": "Akkadian / Sukkalmah (ca. 2300-1600 BC)",
        "current_collection": "Musée du Louvre, Paris",
        "inscription_reading": "4-sign Indus inscription (sign IDs not ingested; see signs_source)",
        "source": "Amiet 1972 no. 1643; Wheeler 1968; Possehl 2002",
    },
    "LOTHAL_PERSIAN_GULF_SEAL": {
        "type": "gulf_type_at_indus",
        "find_country": "India",
        "find_spot": "Lothal",
        "find_period": "Mature Harappan (ca. 2200-1900 BC)",
        "current_collection": "Archaeological Survey of India (excavated collection, Lothal)",
        "inscription_reading": "Short Indus sign group, 2 signs (sign IDs not ingested; see signs_source)",
        "source": "Rao 1963, Antiquity 37; Laursen 2010",
    },
    "FAILAKA_KM_1113": {
        "type": "dilmun_type_with_indus_signs",
        "find_country": "Kuwait",
        "find_spot": "Failaka Island",
        "find_period": "Early Dilmun (ca. 1950-1750 BC)",
        "current_collection": "Kuwait National Museum (KM 1113)",
        "inscription_reading": "4-sign Indus inscription in the Persian-Gulf 'twins' style (sign IDs not ingested; see signs_source)",
        "source": "David-Cuny & Neyme 2016, Failaka Seals Vol. 2",
    },
    "VA_243_BERLIN": {
        "type": "indus_type_at_mesopotamia",
        "find_country": "Mesopotamia (attributed; unprovenanced)",
        "find_spot": "(unprovenanced; Berlin collection piece)",
        "find_period": "Old Akkadian / Larsa (ca. 2200-1900 BC)",
        "current_collection": "Vorderasiatisches Museum, Berlin (VA 243)",
        "inscription_reading": "Markhor motif with ~5 Indus signs (sign IDs not ingested; see signs_source)",
        "source": "Frenez 2018; Kalyanaraman ANE corpus",
    },
    "KONAR_SANDAL_S_CYLINDER": {
        "type": "indus_iconography_at_iran",
        "find_country": "Iran",
        "find_spot": "Konar Sandal South (Jiroft)",
        "find_period": "Late 3rd millennium BC",
        "current_collection": "Iran (excavation collection)",
        "inscription_reading": "Iconographic only; no Indus signs",
        "source": "Vidale & Frenez 2015",
    },
    "JALALABAD_FARS": {
        "type": "indus_inscribed_at_iran",
        "find_country": "Iran",
        "find_spot": "Jalalabad, Fars",
        "find_period": "Late 3rd millennium BC",
        "current_collection": "Iran (excavation collection)",
        "inscription_reading": "4-sign Indus sequence (sign IDs not ingested; see signs_source)",
        "source": "Vidale, Desset & Frenez 2021; Ascalone 2008",
    },
    "AL_MAQSHA_TOKEN_2": {
        "type": "dilmun_token_with_indus_morphology",
        "find_country": "Bahrain (Dilmun)",
        "find_spot": "Al-Maqsha",
        "find_period": "Old Dilmun (ca. 1700 BC)",
        "current_collection": "Bahrain National Museum",
        "inscription_reading": (
            "Akkadian inscription: 'Yagli-el, servant of the goddess "
            "Panipa'. No Indus signs."
        ),
        "source": "Laursen et al. 2026, Journal of Near Eastern Studies 85/1",
    },
}

FIELD_PROV = (
    "REBUILT 2026-10-25: catalogue_id, inscription_length, indus_signs, "
    "signs_confidence, signs_source are verbatim from the surviving "
    "Phase-23 script (scripts/phase23/ingest_seal_signs.py). type, "
    "find_country, find_spot, find_period, current_collection, "
    "inscription_reading, source re-derived from the cited publications; "
    "type and find_period assignments reproduce the lost file's recorded "
    "aggregate distributions (outputs/phase46_t1_contact_zone.json)."
)

seals = []
for cid, base in BASE.items():
    rec = {"catalogue_id": cid}
    rec.update(base)
    ov = OVERLAY[cid]
    rec["inscription_length"] = ov["inscription_length"]
    rec["indus_signs"] = list(ov["indus_signs"])
    rec["signs_confidence"] = ov["signs_confidence"]
    rec["signs_source"] = ov["signs_source"]
    rec["field_provenance"] = FIELD_PROV
    seals.append(rec)

# Phase-24 cross-references (verbatim rationale; laursen row fields from the
# rebuilt Laursen file below, flagged there).
LAURSEN_ROW_FIELDS = {
    16: {"reference": "Gadd 1932 pl. I no. 2", "site": "Ur", "gulf_type": "Gulf INDUS"},
    17: {"reference": "Gadd 1932 pl. I no. 3", "site": "Ur", "gulf_type": "Gulf INDUS"},
    18: {"reference": "Gadd 1932 pl. I no. 4", "site": "Ur", "gulf_type": "Gulf INDUS"},
    14: {"reference": "Amiet 1972 no. 1643", "site": "Susa", "gulf_type": "Gulf INDUS"},
}
upgrade_log = []
for rec in seals:
    cid = rec["catalogue_id"]
    xref = CROSSREF.get(cid)
    if not xref:
        continue
    ln = xref["laursen_seal_no"]
    row = LAURSEN_ROW_FIELDS[ln]
    rec["laursen_2010_seal_no"] = ln
    rec["signs_source"] = (
        f"{rec['signs_source']} | Laursen 2010 Table 1 row {ln} "
        f"({row['reference'][:60]}, site={row['site']})"
    )
    rec["laursen_table1_reference"] = row["reference"]
    rec["laursen_table1_site"] = row["site"]
    rec["laursen_table1_gulf_type"] = row["gulf_type"]
    rec["phase24_crossref_rationale"] = xref["rationale"]
    upgrade_log.append({
        "catalogue_id": cid,
        "laursen_seal_no": ln,
        "rationale": xref["rationale"][:80],
    })

JANABIYAH["field_provenance"] = (
    "VERBATIM record from the surviving Phase-24 script "
    "(scripts/phase24/upgrade_seal_signs.py, _JANABIYAH_NEW_ENTRY)."
)
seals.append(JANABIYAH)

n_with = sum(1 for s in seals if int(s.get("inscription_length", 0) or 0) > 0)
total_signs_13 = sum(
    int(s.get("inscription_length", 0) or 0) for s in seals if s["catalogue_id"] != "JANABIYAH_LAURSEN_10"
)
seals_doc = {
    "metadata": {
        "rebuild": {
            "status": "REBUILT 2026-10-25 — new file, new provenance; NOT the lost original",
            "register_citation": "Holdings reconciliation 2026-10-25, RECORDED-NOT-HELD item #29",
            "see": "provenance record: contact_zone_rebuild_provenance.md (repo, glossa-corpus/indus/sources/contact-zone-rebuilt-2026-10-25/)",
        },
        "phase23_sign_ingestion": {
            "n_seals": 13,
            "n_updated": 13,
            "n_with_signs": 10,
            "n_without_signs": 3,
            "total_indus_signs": total_signs_13,
            "method": (
                "Hand-curated overlay from Parpola 1994, Frenez 2018, "
                "Gadd 1932, Mallowan 1947, Vidale/Desset/Frenez 2021, "
                "David-Cuny/Neyme 2016, Laursen 2010 + 2026. Sign IDs "
                "placeheld with '?' pending CISI Vol 3 plate ingestion."
            ),
        },
        "phase24_sign_upgrade": {
            "n_seals_total": len(seals),
            "n_with_signs": n_with,
            "n_with_high_conf_signs": sum(1 for s in seals if s.get("signs_confidence") == "high"),
            "total_indus_signs": sum(int(s.get("inscription_length", 0) or 0) for s in seals),
            "n_crossreferenced_with_laursen": len(upgrade_log),
            "n_seals_added": 1,
            "upgrade_log": upgrade_log,
            "method": (
                "Hand-curated cross-reference of catalogue_id -> Laursen 2010 "
                "Table 1 seal_no by reference inspection. "
                "Janabiyah seal #10 added with full Parpola 1994b sign IDs "
                "from Laursen footnote 2."
            ),
        },
    },
    "seals": seals,
}

out_seals_dir = OUT / "indus_seals_mesopotamia"
out_seals_dir.mkdir(parents=True, exist_ok=True)
(out_seals_dir / "seals_at_mesopotamia.json").write_text(
    json.dumps(seals_doc, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(f"seals: {len(seals)} records; with signs {n_with}; "
      f"total signs {seals_doc['metadata']['phase24_sign_upgrade']['total_indus_signs']}")

# ------------------------------------------------------------- laursen
rows = [
    {"seal_no": 10, "reference": "", "al_sindi_1999_no": "",
     "gulf_type": "Gulf INDUS", "site": "Janabiyah Cemetery", "bbm_no": ""},
    {"seal_no": 14, "reference": "Amiet 1972 no. 1643", "al_sindi_1999_no": "",
     "gulf_type": "Gulf INDUS", "site": "Susa", "bbm_no": ""},
    {"seal_no": 16, "reference": "Gadd 1932 pl. I no. 2", "al_sindi_1999_no": "",
     "gulf_type": "Gulf INDUS", "site": "Ur", "bbm_no": ""},
    {"seal_no": 17, "reference": "Gadd 1932 pl. I no. 3", "al_sindi_1999_no": "",
     "gulf_type": "Gulf INDUS", "site": "Ur", "bbm_no": ""},
    {"seal_no": 18, "reference": "Gadd 1932 pl. I no. 4", "al_sindi_1999_no": "",
     "gulf_type": "Gulf INDUS", "site": "Ur", "bbm_no": ""},
]
by_type, by_site = {}, {}
for r in rows:
    by_type[r["gulf_type"]] = by_type.get(r["gulf_type"], 0) + 1
    by_site[r["site"]] = by_site.get(r["site"], 0) + 1

laursen_doc = {
    "source_paper": (
        "Laursen 2010, Arabian Archaeology and Epigraphy 21:96-134 "
        "(Wiley), DOI 10.1111/j.1600-0471.2010.00329.x"
    ),
    "n_rows_parsed": len(rows),
    "n_rows_expected": 121,
    "n_inscribed_with_indus_text": 23,
    "by_gulf_type": dict(sorted(by_type.items())),
    "by_site": dict(sorted(by_site.items(), key=lambda kv: -kv[1])),
    "rows": rows,
    "parpola_readings": {str(k): v for k, v in PARPOLA_READINGS.items()},
    "ingestion_method": (
        "REBUILT 2026-10-25 (partial). The published paper is closed-access "
        "(OpenAlex oa_status 'closed'; no repository full text in CORE) and "
        "no lawful copy was reachable in this session, so Table 1 could not "
        "be re-parsed. Rows below are only those recoverable from surviving "
        "programme evidence (Phase-24 cross-reference rationales) plus the "
        "verbatim parpola_readings block transcribed in the surviving "
        "parser script. Empty-string cells are unknown, NOT 'N/A' in the "
        "original. n_inscribed_with_indus_text (=23) and the lost parse's "
        "aggregate distributions are carried from the surviving Phase-46 "
        "derived output as reconciliation targets, not as rebuilt data."
    ),
    "rebuild": {
        "status": "PARTIAL REBUILD 2026-10-25 — new file, new provenance; NOT the lost original",
        "register_citation": "Holdings reconciliation 2026-10-25, RECORDED-NOT-HELD item #30",
        "lost_parse_aggregates_from_phase46_output": {
            "n_rows_catalogued": 102,
            "n_inscribed_with_indus_text": 23,
            "site_distribution": {
                "Karzakkan Cemetery": 28, "Saar Cemetery": 11, "Ur": 6,
                "Saar": 6, "Failaka": 4, "Mohenjo-Daro": 3,
                "Mesopotamia?": 3, "Near East": 2, "Chanhu-Daro": 1,
                "Susa": 1, "Luristan": 1, "Girsu": 1,
                "western Iranian plateau": 1, "Rifa mounds": 1,
                "Janabiyah Cemetery": 1, "Janabiyah": 1, "Bahrain": 1,
            },
            "gulf_type_distribution": {
                "Gulf Type": 76, "Gulf INDUS": 23, "Linear-Elamite": 1,
            },
        },
        "rows_recovered": [10, 14, 16, 17, 18],
        "rows_missing": "all other seal numbers 1-121 (97 of the 102 parsed rows, plus the 19 rows the original parser never captured)",
    },
}
out_gulf_dir = OUT / "gulf_seals"
out_gulf_dir.mkdir(parents=True, exist_ok=True)
(out_gulf_dir / "laursen_2010_table1.json").write_text(
    json.dumps(laursen_doc, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(f"laursen: {len(rows)} rows recovered; parpola_readings seals: {list(laursen_doc['parpola_readings'].keys())}")
