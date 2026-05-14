"""Indus Corpus — Objectization Pipeline.

Converts raw source downloads into IndusObject records (JSONL).

Source formats handled:
  - mayig-cisi: JSON inscription arrays with Parpola sign IDs
  - met-open-access: JSON object arrays from Met API
  - cleveland-art: JSON object arrays from Cleveland API
  - penn-museum: CSV rows (Indus-filtered)
  - indian-culture: HTML pages (metadata extraction only, no text)
  - rmrl: HTML portal pages (metadata extraction only)
  - museums-of-india: JSON search results (metadata only)
  - internet-archive: IIIF manifests (image URL extraction only)

Output:
  glossa-corpus/indus/staging/objects_{date}.jsonl
  glossa-corpus/indus/staging/quarantine_{date}.jsonl
  glossa-corpus/indus/staging/objectize_report_{date}.json

Usage:
    shell.cmd python backend/scripts/corpus_indus_objectize.py [--date YYYY-MM-DD]

_citation:
  primary_sources: ["I.1", "I.2", "I.3", "I.4", "I.5"]
  derivation: "Objectization pipeline for ICIT-scale Indus corpus reconstruction."
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

REPO = Path(__file__).parents[2]
CORPUS = REPO / "glossa-corpus" / "indus"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")

# Glossa ID counter (in-session; loaded from existing staging if resuming)
_COUNTER = 0

def _next_glossa_id() -> str:
    global _COUNTER
    _COUNTER += 1
    return f"GLI-IND-{_COUNTER:07d}"

def _sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


# ── Minimal object record builder ─────────────────────────────────────────────
# Uses plain dicts (not Pydantic) to avoid import issues in acquisition context.
# The normalize step converts these to validated IndusObject models.

def make_object(
    source_system: str,
    source_object_id: str,
    rights_status: str,
    artifact_type: str = "unknown",
    current_holding: Optional[str] = None,
    site_name: Optional[str] = None,
    material: Optional[str] = None,
    dimensions_mm: Optional[str] = None,
    text_code_diplomatic: Optional[str] = None,
    sign_id_scheme: Optional[str] = None,
    image_master_uri: Optional[str] = None,
    accession_number: Optional[str] = None,
    extra: Optional[dict] = None,
    quarantine_reason: Optional[str] = None,
) -> dict:
    gid = _next_glossa_id()
    obj = {
        "glossa_id": gid,
        "source_system": source_system,
        "source_object_id": str(source_object_id),
        "artifact_type": artifact_type,
        "current_holding": current_holding,
        "site_name": site_name,
        "material": material,
        "dimensions_mm": dimensions_mm,
        "rights_status": rights_status,
        "text_code_diplomatic": text_code_diplomatic,
        "sign_id_scheme": sign_id_scheme,
        "image_master_uri": image_master_uri,
        "accession_number": accession_number,
        "review_state": "unreviewed",
        "pipeline_stage": "objectized",
        "quarantine_reason": quarantine_reason,
        "_source_extra": extra or {},
        "_citation": {
            "primary_sources": ["I.1", "I.2", "I.3", "I.4", "I.5"],
            "derivation": f"Objectized from {source_system} by corpus_indus_objectize.py",
        },
    }
    return obj


# ── Per-source parsers ────────────────────────────────────────────────────────

def parse_mayig(raw_dir: Path, date: str) -> tuple[List[dict], List[dict]]:
    """Parse mayig/indus-valley-script-corpus JSON files into object records."""
    objects, quarantine = [], []
    source_dir = raw_dir / "mayig-cisi" / "raw" / date
    if not source_dir.exists():
        print(f"  WARN: mayig raw dir not found: {source_dir}")
        return [], []

    json_files = list(source_dir.rglob("*.json"))
    for jf in json_files:
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as exc:
            quarantine.append({"file": str(jf), "reason": str(exc)})
            continue

        # Handle array of inscription records
        records = data if isinstance(data, list) else [data]
        for rec in records:
            if not isinstance(rec, dict):
                continue
            # Extract fields — handle both legacy and mayig formats
            obj_id = rec.get("id") or rec.get("object_id") or rec.get("name") or str(hash(str(rec)))[:8]
            site = rec.get("site") or rec.get("findspot") or rec.get("provenience")
            acc = rec.get("accession") or rec.get("museum_id") or rec.get("CISI_id")
            atype = (rec.get("type") or rec.get("object_type") or "seal").lower()

            # mayig format: graphemes[].id (Parpola P-numbers like "P121")
            graphemes = rec.get("graphemes") or []
            if graphemes and isinstance(graphemes, list):
                signs = [g["id"] for g in graphemes if isinstance(g, dict) and g.get("id")]
                # Strip leading 'P' and zero-pad to 3 digits for ICIT format
                sign_strs = []
                for s in signs:
                    if isinstance(s, str) and s.startswith("P"):
                        sign_strs.append(s[1:].zfill(3))  # "P121" -> "121"
                    else:
                        sign_strs.append(str(s))
            else:
                signs = rec.get("signs") or rec.get("sequence") or rec.get("text") or []
                if isinstance(signs, list):
                    sign_strs = [str(s) for s in signs if s]
                else:
                    sign_strs = []

            # Build ICIT diplomatic if signs is a list
            diplomatic = None
            scheme = None
            if sign_strs:
                diplomatic = "+" + "-".join(sign_strs) + "+"
                scheme = "Parpola1982"
            elif isinstance(signs, str) and signs:
                diplomatic = signs
                scheme = "unknown"

            # Quarantine if no stable ID or no inscription
            reason = None
            if not obj_id:
                reason = "no stable source identifier"
            if not signs:
                reason = (reason + "; " if reason else "") + "no inscription sequence"

            obj = make_object(
                source_system="mayig-cisi",
                source_object_id=obj_id,
                rights_status="MIT",
                artifact_type=atype if atype in ("seal","tablet","potsherd","impression") else "seal",
                site_name=site,
                accession_number=str(acc) if acc else None,
                text_code_diplomatic=diplomatic,
                sign_id_scheme=scheme,
                quarantine_reason=reason,
                extra={"source_file": str(jf.name), "raw_signs": signs},
            )
            if reason:
                quarantine.append(obj)
            else:
                objects.append(obj)

    print(f"  mayig: {len(objects)} objects, {len(quarantine)} quarantined")
    return objects, quarantine


def parse_met(raw_dir: Path, date: str) -> tuple[List[dict], List[dict]]:
    """Parse Met Open Access data — bulk CSV (primary) + API supplement (secondary).

    Met bulk CSV columns (key ones):
      Object Number, Object ID, Is Public Domain, Object Name, Title,
      Culture, Medium, Dimensions, Country, Region, Locus, Tags, Link Resource
    """
    objects, quarantine = [], []
    met_dir = raw_dir / "met-open-access" / "raw" / date
    if not met_dir.exists():
        print(f"  WARN: Met raw dir not found: {met_dir}")
        return [], []

    INDUS_KWS = ["indus", "harappan", "mohenjo", "chanhu", "dholavira", "harappa",
                 "pakistan", "seal", "steatite"]

    def _process_csv_row(row: dict) -> Optional[dict]:
        obj_id = str(row.get("Object ID") or row.get("objectID") or "")
        acc = row.get("Object Number") or row.get("accessionNumber", "")
        title = str(row.get("Title") or row.get("title") or "")
        culture = str(row.get("Culture") or row.get("culture") or "")
        medium = str(row.get("Medium") or row.get("medium") or "")
        dims = str(row.get("Dimensions") or row.get("dimensions") or "")
        country = str(row.get("Country") or "")
        region = str(row.get("Region") or "")
        dept = str(row.get("Department") or row.get("department") or "")
        is_public_str = str(row.get("Is Public Domain") or row.get("isPublicDomain") or "False")
        is_public = is_public_str.lower() in ("true", "1", "yes")
        img_url = row.get("Link Resource") or row.get("primaryImageSmall") or None
        tags = str(row.get("Tags") or "")

        combined = (title + culture + medium + dept + country + region + tags).lower()
        if not any(kw in combined for kw in INDUS_KWS):
            return None

        reason = None
        if not obj_id:
            reason = "no Object ID"
        if not is_public:
            reason = (reason + "; " if reason else "") + "not public domain"

        return make_object(
            source_system="MetOpenAccess",
            source_object_id=obj_id,
            rights_status="CC0" if is_public else "unknown",
            artifact_type="seal" if "seal" in (medium + title).lower() else "unknown",
            current_holding="Metropolitan Museum of Art, New York",
            site_name=_extract_site(culture + " " + country + " " + region + " " + title),
            material=medium[:200] if medium else None,
            dimensions_mm=dims[:100] if dims else None,
            image_master_uri=img_url,
            accession_number=str(acc),
            quarantine_reason=reason,
            extra={"title": title, "culture": culture, "department": dept, "is_public": is_public},
        )

    # Source 1: Bulk CSV (filtered)
    csv_path = met_dir / "met_indus_filtered.csv"
    if csv_path.exists():
        try:
            content = csv_path.read_text(encoding="utf-8", errors="replace")
            reader = csv.DictReader(io.StringIO(content))
            for row in reader:
                obj = _process_csv_row(row)
                if obj is None:
                    continue
                if obj.get("quarantine_reason") and "not public domain" in (obj.get("quarantine_reason") or ""):
                    quarantine.append(obj)
                else:
                    objects.append(obj)
        except Exception as exc:
            quarantine.append({"file": str(csv_path), "reason": str(exc)})
    else:
        # Fallback: old API JSON format
        api_file = met_dir / "met_indus_objects.json"
        if api_file.exists():
            try:
                recs = json.loads(api_file.read_text(encoding="utf-8"))
                for rec in recs:
                    if not isinstance(rec, dict):
                        continue
                    obj = _process_csv_row(rec)  # compatible with API dict too
                    if obj:
                        objects.append(obj) if not obj.get("quarantine_reason") else quarantine.append(obj)
            except Exception as exc:
                quarantine.append({"file": str(api_file), "reason": str(exc)})

    # Source 2: API supplement (JSON)
    api_supp = met_dir / "met_indus_api_supplement.json"
    if api_supp.exists():
        try:
            supp_recs = json.loads(api_supp.read_text(encoding="utf-8"))
            existing_ids = {o.get("source_object_id") for o in objects + quarantine}
            for rec in supp_recs:
                if not isinstance(rec, dict):
                    continue
                obj = _process_csv_row(rec)
                if obj and obj.get("source_object_id") not in existing_ids:
                    if obj.get("quarantine_reason"):
                        quarantine.append(obj)
                    else:
                        objects.append(obj)
        except Exception as exc:
            print(f"  API supplement WARN: {exc}")

    print(f"  met: {len(objects)} objects, {len(quarantine)} quarantined")
    return objects, quarantine


def parse_cleveland(raw_dir: Path, date: str) -> tuple[List[dict], List[dict]]:
    """Parse Cleveland Museum Open Access JSON."""
    objects, quarantine = [], []
    cle_file = raw_dir / "cleveland-art" / "raw" / date / "cleveland_indus_objects.json"
    if not cle_file.exists():
        print(f"  WARN: Cleveland file not found: {cle_file}")
        return [], []

    try:
        recs = json.loads(cle_file.read_text(encoding="utf-8"))
    except Exception as exc:
        quarantine.append({"file": str(cle_file), "reason": str(exc)})
        return [], quarantine

    for rec in recs:
        if not isinstance(rec, dict):
            continue
        obj_id = str(rec.get("id") or rec.get("accession_number", ""))
        title = str(rec.get("title") or "")
        medium = str(rec.get("technique") or rec.get("medium") or "")
        # culture may be a list in the Cleveland API response
        culture_raw = rec.get("culture") or ""
        culture = " ".join(culture_raw) if isinstance(culture_raw, list) else str(culture_raw)
        dept = str(rec.get("department") or "")
        creators = rec.get("creators", [])
        images = rec.get("images") or {}
        img_url = images.get("web", {}).get("url") if isinstance(images, dict) else None
        acc = rec.get("accession_number", "")
        share_license = rec.get("share_license_status", "")

        combined = (title + medium + culture + dept).lower()
        if not any(kw in combined for kw in ["indus", "harappan", "mohenjo", "seal", "pakistan"]):
            continue

        reason = None
        if not obj_id:
            reason = "no stable ID"
        rights = "CC0" if share_license in ("CC0", "open") else "unknown"

        obj = make_object(
            source_system="ClevelandArtOpenAccess",
            source_object_id=obj_id,
            rights_status=rights,
            artifact_type="seal" if "seal" in (title + medium).lower() else "unknown",
            current_holding="Cleveland Museum of Art, Cleveland OH",
            site_name=_extract_site(culture + " " + title),
            material=medium[:200] if medium else None,
            image_master_uri=img_url,
            accession_number=acc,
            quarantine_reason=reason,
            extra={"title": title, "culture": culture, "share_license": share_license},
        )
        if reason:
            quarantine.append(obj)
        else:
            objects.append(obj)

    print(f"  cleveland: {len(objects)} objects, {len(quarantine)} quarantined")
    return objects, quarantine


def parse_penn(raw_dir: Path, date: str) -> tuple[List[dict], List[dict]]:
    """Parse Penn Museum CSV (Indus-filtered rows).

    Penn Museum CSV columns (from 2026 dataset):
      Record URL, identifier, curatorialSection, onDisplay, objectName,
      nativeName, title, creditLine, description, placeName, siteName,
      culture, cultureArea, locus, period, material, technique, creator,
      iconography, iconographySubject, inscriptionMarkLanguage, dateMade,
      earlyDate, lateDate, depth, length, width, height, thickness, weight,
      outsideDiameter, measurementUnit
    """
    objects, quarantine = [], []
    penn_file = raw_dir / "penn-museum" / "raw" / date / "penn_indus_filtered.csv"
    if not penn_file.exists():
        penn_file = raw_dir / "penn-museum" / "raw" / date / "penn_collections.csv"
    if not penn_file.exists():
        print(f"  WARN: Penn CSV not found")
        return [], []

    # More specific keywords to reduce false positives ("india" is too broad)
    INDUS_KWS = ["indus", "harappan", "mohenjo", "chanhu", "dholavira",
                 "harappa", "pakistan", "steatite", "sindhian"]
    SEAL_KWS = ["seal", "impression"]  # only count as Indus seal if also near-eastern/south asian

    try:
        content = penn_file.read_text(encoding="utf-8", errors="replace")
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
    except Exception as exc:
        quarantine.append({"file": str(penn_file), "reason": str(exc)})
        return [], quarantine

    for row in rows:
        combined = " ".join(str(v) for v in row.values()).lower()
        section = str(row.get("curatorialSection") or "").lower()
        # Primary Indus keywords
        is_indus = any(kw in combined for kw in INDUS_KWS)
        # Seal/impression only counts if in a relevant section
        is_indus_seal = (any(kw in combined for kw in SEAL_KWS) and
                         any(s in section for s in ["near east", "asian", "middle east", "south"]))
        if not (is_indus or is_indus_seal):
            continue

        # Penn 2026 CSV column names
        obj_id = (row.get("identifier") or row.get("object_number") or
                  row.get("id") or row.get("objectnumber") or "")
        title = row.get("objectName") or row.get("title") or row.get("nativeName") or ""
        material = row.get("material") or row.get("medium") or ""
        dims_parts = [row.get(k, "") for k in ["depth", "length", "width", "height"] if row.get(k)]
        dims = " x ".join(dims_parts) + " " + (row.get("measurementUnit") or "") if dims_parts else ""
        culture = row.get("culture") or row.get("cultureArea") or ""
        provenience = row.get("siteName") or row.get("placeName") or row.get("locus") or ""
        img_url = row.get("Record URL") or None  # Penn URL as placeholder
        section_full = row.get("curatorialSection") or ""

        reason = None
        if not obj_id:
            reason = "no object number"

        obj = make_object(
            source_system="PennMuseum",
            source_object_id=obj_id,
            rights_status="CC BY 4.0",  # metadata; images are noncommercial-educational
            artifact_type="seal" if "seal" in (title + material).lower() else "unknown",
            current_holding="Penn Museum, Philadelphia PA",
            site_name=_extract_site(provenience + " " + culture),
            material=material[:200] if material else None,
            dimensions_mm=dims[:100] if dims else None,
            image_master_uri=img_url,
            accession_number=obj_id,
            quarantine_reason=reason,
            extra={"title": title, "culture": culture, "provenience": provenience},
        )
        if reason:
            quarantine.append(obj)
        else:
            objects.append(obj)

    print(f"  penn: {len(objects)} objects, {len(quarantine)} quarantined")
    return objects, quarantine


def _extract_site(text: str) -> Optional[str]:
    """Best-effort site name extraction from culture/provenience text."""
    sites = {
        "mohenjo-daro": "Mohenjo-daro",
        "mohenjo daro": "Mohenjo-daro",
        "harappa": "Harappa",
        "chanhu-daro": "Chanhu-Daro",
        "chanhu daro": "Chanhu-Daro",
        "dholavira": "Dholavira",
        "lothal": "Lothal",
        "kalibangan": "Kalibangan",
        "rakhigarhi": "Rakhigarhi",
        "sutkagen-dor": "Sutkagen-Dor",
        "mehrgarh": "Mehrgarh",
    }
    tl = text.lower()
    for key, name in sites.items():
        if key in tl:
            return name
    return None


# ── Main pipeline ─────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Objectize Indus corpus raw downloads")
    parser.add_argument("--date", default=TODAY, help="Acquisition date to process (YYYY-MM-DD)")
    parser.add_argument(
        "--sources", nargs="*",
        choices=["mayig", "met", "cleveland", "penn"],
        help="Specific sources to process (default: all structured sources)"
    )
    args = parser.parse_args()

    raw_dir = CORPUS / "sources"
    staging_dir = CORPUS / "staging"
    staging_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Indus Objectization — date: {args.date} ===")

    # Load existing counter from staging if resuming
    global _COUNTER
    existing = list(staging_dir.glob("objects_*.jsonl"))
    if existing:
        # Count existing records to continue numbering
        count = 0
        for f in existing:
            count += sum(1 for line in f.read_text(encoding="utf-8").splitlines() if line.strip())
        _COUNTER = count
        print(f"  Resuming from {_COUNTER} existing records")

    all_sources = [
        ("mayig", parse_mayig),
        ("met", parse_met),
        ("cleveland", parse_cleveland),
        ("penn", parse_penn),
    ]
    if args.sources:
        to_run = [(n, fn) for n, fn in all_sources if n in args.sources]
    else:
        to_run = all_sources

    all_objects: List[dict] = []
    all_quarantine: List[dict] = []

    for name, fn in to_run:
        print(f"\n--- {name} ---")
        objs, quar = fn(raw_dir, args.date)
        all_objects.extend(objs)
        all_quarantine.extend(quar)

    # Write staging outputs
    out_path = staging_dir / f"objects_{args.date}.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for obj in all_objects:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    quar_path = staging_dir / f"quarantine_{args.date}.jsonl"
    with open(quar_path, "w", encoding="utf-8") as f:
        for obj in all_quarantine:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    report = {
        "_citation": {
            "primary_sources": ["I.1", "I.2", "I.3", "I.4", "I.5"],
            "derivation": "Objectization report for Indus corpus reconstruction.",
        },
        "batch_id": f"{args.date}-INDUS-OBJECTIZE",
        "timestamp": datetime.utcnow().isoformat(),
        "date_processed": args.date,
        "sources": [n for n, _ in to_run],
        "objects_total": len(all_objects),
        "quarantine_total": len(all_quarantine),
        "output_path": str(out_path),
        "quarantine_path": str(quar_path),
        "by_source": {
            name: len([o for o in all_objects if o.get("source_system", "").lower().startswith(name.replace("-", ""))])
            for name, _ in to_run
        },
    }
    rpt_path = staging_dir / f"objectize_report_{args.date}.json"
    rpt_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n=== DONE ===")
    print(f"  Objects: {len(all_objects)}")
    print(f"  Quarantined: {len(all_quarantine)}")
    print(f"  Staging: {out_path}")
    print(f"  Report: {rpt_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
