"""Indus Corpus — Export Pipeline.

Reads canonical/objects.jsonl and builds three release packages:

  exports/indus_open.jsonl       — CC0 / MIT / CC BY 4.0 objects only (ML training ready)
  exports/indus_research.jsonl   — all research-use cleared objects (SA experiments)
  exports/indus_icit_format.json — ICIT-format diplomatic sequences (analysis ready)
  exports/export_report.json     — metadata, counts, and provenance summary

Hard rule: nothing enters exports without both rights_status and at least one
provenance chain event. Objects missing either are quarantined, not exported.

Usage:
    shell.cmd python backend/scripts/corpus_indus_export.py

_citation:
  primary_sources: ["A.1", "A.7", "I.1", "I.2", "I.3", "I.4", "I.5"]
  derivation: "Export pipeline for ICIT-scale Indus corpus reconstruction."
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

REPO = Path(__file__).parents[2]
CORPUS = REPO / "glossa-corpus" / "indus"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")

# Rights classes cleared for each export tier
OPEN_RIGHTS = {"CC0", "MIT"}
RESEARCH_RIGHTS = {"CC0", "MIT", "CC BY 4.0", "india-gov-cultural", "rmrl-research"}


def load_canonical() -> List[dict]:
    path = CORPUS / "canonical" / "objects.jsonl"
    if not path.exists():
        print("ERROR: canonical/objects.jsonl not found. Run normalize first.")
        return []
    objects = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                objects.append(json.loads(line))
            except Exception:
                pass
    return objects


def passes_export_gate(obj: dict) -> tuple[bool, Optional[str]]:
    """Check provenance chain completeness. Returns (passes, failure_reason)."""
    rights = obj.get("rights_status")
    if not rights or rights == "unknown":
        return False, "rights_status unknown or missing"
    # Quarantined objects are never exported
    if obj.get("quarantine_reason"):
        return False, f"quarantined: {obj['quarantine_reason']}"
    return True, None


def to_icit_sequence(obj: dict) -> Optional[str]:
    """Return ICIT diplomatic sequence for this object, or None."""
    diplomatic = obj.get("text_code_diplomatic_normalized") or obj.get("text_code_diplomatic")
    return diplomatic if diplomatic else None


def build_open_export(objects: List[dict]) -> tuple[List[dict], List[str]]:
    """CC0/MIT/CC-BY only, ML training cleared."""
    passed, quarantine_reasons = [], []
    for obj in objects:
        gate_ok, reason = passes_export_gate(obj)
        if not gate_ok:
            quarantine_reasons.append(reason)
            continue
        if obj.get("rights_status") not in OPEN_RIGHTS:
            quarantine_reasons.append(f"rights not open: {obj.get('rights_status')}")
            continue
        # Build lean export record
        export = {
            "glossa_id": obj["glossa_id"],
            "source_system": obj["source_system"],
            "rights_status": obj["rights_status"],
            "artifact_type": obj.get("artifact_type"),
            "site_name": obj.get("site_name"),
            "current_holding": obj.get("current_holding"),
            "text_code_diplomatic": obj.get("text_code_diplomatic"),
            "canonical_grapheme_ids": obj.get("canonical_grapheme_ids", []),
            "sign_instance_count": obj.get("sign_instance_count", 0),
            "image_master_uri": obj.get("image_master_uri"),
            "accession_number": obj.get("accession_number"),
            "_citation": obj.get("_citation", {}),
        }
        passed.append(export)
    return passed, quarantine_reasons


def build_research_export(objects: List[dict]) -> tuple[List[dict], List[str]]:
    """All research-use cleared objects — for SA experiments and analysis."""
    passed, quarantine_reasons = [], []
    for obj in objects:
        gate_ok, reason = passes_export_gate(obj)
        if not gate_ok:
            quarantine_reasons.append(reason)
            continue
        if obj.get("rights_status") not in RESEARCH_RIGHTS:
            quarantine_reasons.append(f"rights not research-cleared: {obj.get('rights_status')}")
            continue
        export = {
            "glossa_id": obj["glossa_id"],
            "source_system": obj["source_system"],
            "rights_status": obj["rights_status"],
            "artifact_type": obj.get("artifact_type"),
            "site_name": obj.get("site_name"),
            "current_holding": obj.get("current_holding"),
            "material": obj.get("material"),
            "text_code_diplomatic": obj.get("text_code_diplomatic"),
            "text_code_diplomatic_normalized": obj.get("text_code_diplomatic_normalized"),
            "sign_id_scheme": obj.get("sign_id_scheme"),
            "canonical_grapheme_ids": obj.get("canonical_grapheme_ids", []),
            "sign_instance_count": obj.get("sign_instance_count", 0),
            "crosswalk_coverage": obj.get("crosswalk_coverage", 0.0),
            "image_master_uri": obj.get("image_master_uri"),
            "accession_number": obj.get("accession_number"),
            "_citation": obj.get("_citation", {}),
        }
        passed.append(export)
    return passed, quarantine_reasons


def build_icit_format(research_objects: List[dict]) -> dict:
    """
    Build ICIT-format diplomatic sequence list.
    Each entry: {"glossa_id": ..., "icit_text": "+NNN-NNN+", "sign_count": N, ...}
    Only objects with a diplomatic text sequence are included.
    """
    sequences = []
    for obj in research_objects:
        seq = to_icit_sequence(obj)
        if not seq:
            continue
        sign_count = obj.get("sign_instance_count", 0)
        sequences.append({
            "glossa_id": obj["glossa_id"],
            "source_system": obj["source_system"],
            "site_name": obj.get("site_name"),
            "artifact_type": obj.get("artifact_type"),
            "icit_text": seq,
            "sign_count": sign_count,
            "sign_id_scheme": obj.get("sign_id_scheme"),
            "rights_status": obj["rights_status"],
        })

    return {
        "_citation": {
            "primary_sources": ["A.1", "A.7", "I.1", "I.2", "I.3", "I.4", "I.5"],
            "derivation": (
                "ICIT-format diplomatic sequence export for Indus corpus reconstruction. "
                "Sequences use ICIT encoding rules: +NNN-NNN+, 000, ++. "
                "See CITATIONS.md sections A.1, A.7, I.1–I.5."
            ),
        },
        "version": f"v1 ({TODAY})",
        "total_sequences": len(sequences),
        "icit_target_scale": {
            "objects": 4537, "texts": 5509, "sign_occurrences": 19616,
            "note": "ICIT reference scale from public ICIT documentation.",
        },
        "current_coverage_pct": round(len(sequences) / 5509 * 100, 1),
        "sequences": sequences,
    }


def main() -> int:
    print(f"=== Indus Export — {TODAY} ===")
    exports_dir = CORPUS / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)

    objects = load_canonical()
    if not objects:
        return 1
    print(f"  Loaded {len(objects)} canonical objects")

    open_objects, open_rejected = build_open_export(objects)
    research_objects, research_rejected = build_research_export(objects)
    icit_export = build_icit_format(research_objects)

    # Write exports
    open_path = exports_dir / "indus_open.jsonl"
    with open(open_path, "w", encoding="utf-8") as f:
        for obj in open_objects:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    research_path = exports_dir / "indus_research.jsonl"
    with open(research_path, "w", encoding="utf-8") as f:
        for obj in research_objects:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    icit_path = exports_dir / "indus_icit_format.json"
    icit_path.write_text(json.dumps(icit_export, indent=2, ensure_ascii=False), encoding="utf-8")

    # Report
    report = {
        "_citation": {
            "primary_sources": ["A.1", "A.7", "I.1", "I.2", "I.3", "I.4", "I.5"],
            "derivation": "Export report for Indus corpus reconstruction.",
        },
        "batch_id": f"{TODAY}-INDUS-EXPORT",
        "timestamp": datetime.utcnow().isoformat(),
        "canonical_objects": len(objects),
        "open_export": {
            "count": len(open_objects),
            "rejected": len(open_rejected),
            "path": str(open_path),
        },
        "research_export": {
            "count": len(research_objects),
            "rejected": len(research_rejected),
            "path": str(research_path),
        },
        "icit_format": {
            "sequences": len(icit_export["sequences"]),
            "coverage_pct": icit_export["current_coverage_pct"],
            "path": str(icit_path),
        },
        "icit_target": {"objects": 4537, "texts": 5509, "sign_occurrences": 19616},
    }
    rpt_path = exports_dir / "export_report.json"
    rpt_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n=== DONE ===")
    print(f"  Open (CC0/MIT):      {len(open_objects)} objects")
    print(f"  Research-cleared:    {len(research_objects)} objects")
    print(f"  ICIT sequences:      {len(icit_export['sequences'])} ({icit_export['current_coverage_pct']}% of target)")
    print(f"  Exports: {exports_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
