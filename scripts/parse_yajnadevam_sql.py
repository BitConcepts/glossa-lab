"""
Parse Yajnadevam indus-website population-script.sql into Glossa-Lab corpus format.
Extracts: SITE, SEAL, INSCRIPTION, GLYPHSEQUENCE tables.

Source: https://github.com/yajnadevam/indus-website (GPL-3.0 license)
Sign numbering: Yajnadevam GLYPHID system (custom; needs crosswalk to Parpola/Mahadevan)
Interpretation note: Yajnadevam interprets the script as Sanskrit/proto-abugida.
  We use ONLY the structural data (sign sequences, site IDs, directions),
  NOT the phonetic interpretation.

Run from glossa-lab root:
    python scripts/parse_yajnadevam_sql.py

Outputs:
    data_raw/other_sites/yajnadevam_inscriptions.json    (raw parsed data)
    data_raw/other_sites/yajnadevam_sites.json           (site table)
    logs/yajnadevam_ingestion_log.md
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL_PATH = ROOT / "data_raw" / "other_sites" / "yajnadevam_population.sql"
OUT_RAW = ROOT / "data_raw" / "other_sites"
LOGS = ROOT / "logs"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Site ID mapping (from SITE table)
_SITE_MAP: dict[str, tuple[str, str]] = {}  # SI1 -> (name, country)

_COUNTRY_MAP = {
    "Mohenjo-daro": "Pakistan",
    "Harappa": "Pakistan",
    "Dholavira": "India",
    "Rakhigarhi": "India",
    "Gonur Depe": "Turkmenistan",
    "Salut": "Oman",
    "Alamgirpur": "India",
    "Allahdino": "Pakistan",
    "Altyn Depe": "Turkmenistan",
    "Amri": "Pakistan",
    "Bakkar Buthi": "Pakistan",
    "Bala-kot": "Pakistan",
    "Banawali": "India",
    "Bhirrana": "India",
    "Chandigarh": "India",
    "Chanhujo-daro": "Pakistan",
    "Desalpur": "India",
    "Farmana": "India",
    "Gharo Bhiro": "Pakistan",
    "Gola Dhoro (Bagasra)": "India",
    "Kalibangan": "India",
    "Khirsara": "India",
    "Kish": "Iraq",
    "Lohumjo-daro": "Pakistan",
    "Lothal": "India",
    "Luristan": "Iran",
    "Ganweriwala": "Pakistan",
    "Nausharo": "Pakistan",
    "Nindowari-damb": "Pakistan",
    "Qala'at al-Bahrain": "Bahrain",
    "Ra's al-Junayz": "Oman",
    "Rupar": "India",
    "Shortughai": "Afghanistan",
    "Surkotada": "India",
    "Susa": "Iran",
    "Tell Umma": "Iraq",
    "Ur": "Iraq",
    "Kanmer": "India",
    "Wattoowala": "Pakistan",
    "Rajanpur": "Pakistan",
    "Unknown": "unknown",
}


def _extract_table_block(sql: str, table_name: str) -> str:
    """Extract the full INSERT INTO <table_name> ... ; block."""
    start = sql.find(f"INSERT INTO {table_name}")
    if start < 0:
        return ""
    end = sql.find(";", start)
    if end < 0:
        return ""
    return sql[start: end + 1]


def parse_site_table(sql: str) -> dict[str, dict]:
    """Parse SITE table → {site_id: {name, country}}"""
    block = _extract_table_block(sql, "SITE")
    sites = {}
    for m in re.finditer(r'\("(SI\d+)","([^"]+)"\)', block):
        site_id, name = m.group(1), m.group(2)
        country = _COUNTRY_MAP.get(name, "unknown")
        sites[site_id] = {"name": name, "country": country}
    return sites


def parse_seal_table(sql: str) -> dict[int, dict]:
    """Parse SEAL table → {seal_id: {site_id, material, external_id, ...}}"""
    block = _extract_table_block(sql, "SEAL (")
    if not block:
        block = _extract_table_block(sql, "SEAL")
    seals = {}
    # Pattern: (SEALID, SITEID, MATERIAL, EXTERNAL_ID, ...)
    # From schema: SEAL (SEALID INT, SITEID VARCHAR, MATERIAL VARCHAR, EXTERNALID VARCHAR, ...)
    # Some fields may be NULL
    for m in re.finditer(
        r'\((\d+),\s*"(SI\d+|NULL)",\s*"?([^",]*)"?,\s*"?([^",]*)"?',
        block,
    ):
        seal_id = int(m.group(1))
        site_id = m.group(2) if m.group(2) != "NULL" else None
        material = m.group(3) if m.group(3) not in ("NULL", "") else None
        external_id = m.group(4) if m.group(4) not in ("NULL", "") else None
        seals[seal_id] = {
            "site_id": site_id,
            "material": material,
            "external_id": external_id,
        }
    return seals


def parse_inscription_table(sql: str) -> dict[int, dict]:
    """Parse INSCRIPTION table → {seal_id: {is_complete, direction}}"""
    block = _extract_table_block(sql, "INSCRIPTION")
    inscriptions = {}
    for m in re.finditer(r'\((\d+),\s*"([^"]+)",\s*"([^"]+)"\)', block):
        seal_id = int(m.group(1))
        is_complete = m.group(2)
        direction = m.group(3)
        inscriptions[seal_id] = {
            "is_complete": is_complete,
            "direction": direction,
        }
    return inscriptions


def parse_glyphsequence_table(sql: str) -> dict[int, list[tuple[int, int]]]:
    """Parse GLYPHSEQUENCE table → {seal_id: [(glyph_id, idx), ...]}"""
    block = _extract_table_block(sql, "GLYPHSEQUENCE")
    sequences: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for m in re.finditer(r'\((\d+),(\d+),(\d+)\)', block):
        seal_id = int(m.group(1))
        glyph_id = int(m.group(2))
        idx = int(m.group(3))
        sequences[seal_id].append((glyph_id, idx))
    # Sort each sequence by idx
    for seal_id in sequences:
        sequences[seal_id].sort(key=lambda x: x[1])
    return dict(sequences)


def build_corpus(
    sites: dict[str, dict],
    seals: dict[int, dict],
    inscriptions: dict[int, dict],
    sequences: dict[int, list],
) -> list[dict]:
    """Build the inscription corpus joining all tables."""
    records = []
    for seal_id, insc in inscriptions.items():
        seal = seals.get(seal_id, {})
        site_id = seal.get("site_id")
        site_info = sites.get(site_id, {"name": "unknown", "country": "unknown"}) if site_id else {"name": "unknown", "country": "unknown"}

        # Get glyph sequence
        seq = sequences.get(seal_id, [])
        sign_ids = [f"Y{glyph_id:04d}" for glyph_id, _ in seq]  # Y-prefix = Yajnadevam

        # Reading direction
        direction = insc.get("direction", "")
        direction_norm = "RTL" if "R/L" in direction else "LTR" if "L/R" in direction else "unknown"

        records.append({
            "inscription_id_internal": f"GLOSSA-YJ-{seal_id:04d}",
            "source_name": "Yajnadevam indus-website corpus (GPL-3.0, GitHub)",
            "source_volume": "indus-website population-script.sql (2023-2024)",
            "source_page": "",
            "source_plate": "",
            "source_object_id": seal.get("external_id") or f"YJ-{seal_id}",
            "site": site_info["name"],
            "subsite_or_mound": "",
            "country": site_info["country"],
            "artifact_type": f"seal ({seal.get('material', 'unknown material')})",
            "material": seal.get("material", "unknown"),
            "period_or_phase": "Mature Harappan (2600-1900 BCE, undifferentiated)",
            "excavated_or_unprovenanced": "unknown",
            "reading_direction_if_known": direction or "unknown",
            "sign_sequence_raw": " ".join(sign_ids),
            "sign_sequence_source_ids": " ".join(sign_ids),
            "image_path_if_available": "",
            "notes": f"is_complete={insc.get('is_complete', '?')}; direction={direction}",
            "confidence": "low",
            # Normalized sequence fields
            "sequence_source_exact": " ".join(sign_ids),
            "sequence_registry_ids": " ".join(sign_ids),
            "sequence_variant_sensitive": " ".join(sign_ids),
            "sequence_variant_collapsed_light": " ".join(sign_ids),
            "sequence_unknown_markers": "",
            "sequence_damage_markers": "",
            "sequence_direction_normalized": direction_norm,
            "ingested_at": NOW,
            "source_sha256": "see logs/file_manifest.json",
            "sign_numbering_system": "Yajnadevam GLYPHID (custom; needs crosswalk to Parpola/Mahadevan)",
        })
    return records


def write_ingestion_log(records: list[dict], sites: dict) -> None:
    out = LOGS / "yajnadevam_ingestion_log.md"
    site_counter = Counter(r["site"] for r in records)
    sign_counter = Counter(
        sign for r in records for sign in r["sign_sequence_raw"].split()
    )
    total_tokens = sum(len(r["sign_sequence_raw"].split()) for r in records)

    lines = [
        "# Yajnadevam Corpus Ingestion Log",
        f"Date: {NOW}",
        "",
        "## Source",
        "- Repo: https://github.com/yajnadevam/indus-website",
        "- File: population-script.sql",
        "- License: GPL-3.0",
        "- Sign system: Yajnadevam GLYPHID (custom integer IDs, not Parpola/Mahadevan)",
        "",
        "## IMPORTANT CAVEAT",
        "Yajnadevam interprets the Indus script as proto-abugida encoding Sanskrit.",
        "We use ONLY the structural data (sign sequences, site IDs, directions).",
        "We do NOT accept the phonetic/Sanskrit interpretation.",
        "All signs are labelled Y0000–Y9999 (Yajnadevam GLYPHID prefix).",
        "A crosswalk to Parpola/Mahadevan numbering is REQUIRED before merging",
        "this corpus with the CISI corpus (which uses P-numbers).",
        "",
        "## Statistics",
        f"- Total inscriptions: {len(records)}",
        f"- Total sign tokens: {total_tokens}",
        f"- Distinct Yajnadevam signs: {len(sign_counter)}",
        f"- Sites covered: {len(site_counter)}",
        "",
        "## Site Coverage",
        "",
    ]
    for site, cnt in site_counter.most_common():
        lines.append(f"- {site}: {cnt} inscriptions")

    lines += [
        "",
        "## Sites NOW covered (fixing review gate checklist):",
        "",
    ]
    required = [
        "Mohenjo-daro", "Harappa", "Kalibangan", "Dholavira",
        "Lothal", "Chanhujo-daro", "Banawali", "Rakhigarhi", "Shortughai"
    ]
    for s in required:
        cnt = site_counter.get(s, 0)
        status = f"✓ {cnt} inscriptions" if cnt > 0 else "ABSENT"
        lines.append(f"- {s}: {status}")

    lines += [
        "",
        "## Next Steps",
        "1. Build Yajnadevam GLYPHID ↔ Parpola P-number crosswalk",
        "2. Merge with CISI corpus (once crosswalk exists)",
        "3. Re-run Phases 6-8 structural analysis on combined corpus",
        "4. Re-evaluate review gate checklist",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Log written: {out}")


def main() -> None:
    print("=" * 60)
    print("Yajnadevam SQL Parser — Glossa-Lab Corpus Ingestion")
    print("=" * 60)

    sql = SQL_PATH.read_text(encoding="utf-8", errors="replace")
    print(f"SQL file size: {len(sql):,} chars")

    print("\nParsing tables...")
    sites = parse_site_table(sql)
    print(f"  Sites: {len(sites)}")

    seals = parse_seal_table(sql)
    print(f"  Seals: {len(seals)}")

    inscriptions = parse_inscription_table(sql)
    print(f"  Inscriptions: {len(inscriptions)}")

    sequences = parse_glyphsequence_table(sql)
    print(f"  Glyph sequences: {len(sequences)}")

    # Save raw tables
    (OUT_RAW / "yajnadevam_sites.json").write_text(
        json.dumps(sites, indent=2), encoding="utf-8"
    )
    print(f"\nSites with inscriptions:")
    site_seal_map: dict[str, int] = defaultdict(int)
    for seal_id, seal in seals.items():
        if seal_id in inscriptions and seal.get("site_id"):
            site_seal_map[seal["site_id"]] += 1
    for site_id, cnt in sorted(site_seal_map.items(), key=lambda x: -x[1]):
        site_name = sites.get(site_id, {}).get("name", site_id)
        print(f"  {site_id} ({site_name}): {cnt} inscriptions")

    print("\nBuilding corpus records...")
    records = build_corpus(sites, seals, inscriptions, sequences)
    print(f"  Records: {len(records)}")

    out_path = OUT_RAW / "yajnadevam_inscriptions.json"
    out_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Saved: {out_path}")

    write_ingestion_log(records, sites)

    print("\n" + "=" * 60)
    print(f"Complete. {len(records)} inscriptions from {len(site_seal_map)} sites.")
    print("NOTE: Sign IDs are Yajnadevam GLYPHID (Y-prefix).")
    print("Crosswalk to Parpola/Mahadevan required before merging.")
    print("=" * 60)


if __name__ == "__main__":
    main()
