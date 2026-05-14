"""Indus Corpus — Coverage and Quality Dashboard.

Prints a structured status report showing:
  - Object count by source and pipeline stage
  - Rights status breakdown
  - Diplomatic text coverage
  - Sign instance count and crosswalk coverage
  - Quarantine count and top failure causes
  - ICIT target scale comparison

Usage:
    shell.cmd python backend/scripts/corpus_indus_status.py

Output: plain text to stdout + reports/indus_corpus_status_{date}.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import List

REPO = Path(__file__).parents[2]
CORPUS = REPO / "glossa-corpus" / "indus"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")

ICIT_TARGET = {"objects": 4537, "texts": 5509, "sign_occurrences": 19616}


def load_jsonl(path: Path) -> List[dict]:
    if not path.exists():
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


def print_section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def pct(n: int, total: int) -> str:
    if total == 0:
        return "N/A"
    return f"{n/total*100:.1f}%"


def main() -> int:
    print(f"=== Indus Corpus Status Dashboard — {TODAY} ===")

    # Load all layers
    staging_files = sorted(CORPUS.joinpath("staging").glob("objects_*.jsonl"))
    quarantine_files = sorted(CORPUS.joinpath("staging").glob("quarantine_*.jsonl"))
    canonical_path = CORPUS / "canonical" / "objects.jsonl"
    sign_instances_path = CORPUS / "canonical" / "sign_instances.jsonl"
    open_export_path = CORPUS / "exports" / "indus_open.jsonl"
    research_export_path = CORPUS / "exports" / "indus_research.jsonl"
    icit_export_path = CORPUS / "exports" / "indus_icit_format.json"

    staging = []
    for f in staging_files:
        staging.extend(load_jsonl(f))
    quarantine = []
    for f in quarantine_files:
        quarantine.extend(load_jsonl(f))
    canonical = load_jsonl(canonical_path)
    sign_instances = load_jsonl(sign_instances_path)
    open_export = load_jsonl(open_export_path)
    research_export = load_jsonl(research_export_path)

    icit_sequences = 0
    if icit_export_path.exists():
        try:
            icit_data = json.loads(icit_export_path.read_text(encoding="utf-8"))
            icit_sequences = icit_data.get("total_sequences", 0)
        except Exception:
            pass

    # ── Source inventory ──────────────────────────────────────────────────────
    print_section("SOURCE INVENTORY")
    source_dirs = list((CORPUS / "sources").iterdir()) if (CORPUS / "sources").exists() else []
    for sd in sorted(source_dirs):
        if not sd.is_dir():
            continue
        raw_dirs = list((sd / "raw").iterdir()) if (sd / "raw").exists() else []
        has_data = len(raw_dirs) > 0
        prov = sd / "provenance.yaml"
        stub = "STUB" if prov.exists() and "STUB" in prov.read_text(encoding="utf-8", errors="ignore")[:200] else ""
        status = "DATA" if has_data else ("STUB" if stub else "EMPTY")
        print(f"  {sd.name:<30} [{status}]  {len(raw_dirs)} date dirs")

    # ── Pipeline stages ───────────────────────────────────────────────────────
    print_section("PIPELINE STAGES")
    print(f"  Staging objects:      {len(staging):>6}")
    print(f"  Quarantined:          {len(quarantine):>6}")
    print(f"  Canonical (normalized):{len(canonical):>5}")
    print(f"  Open export (CC0/MIT):{len(open_export):>5}")
    print(f"  Research export:      {len(research_export):>6}")
    print(f"  ICIT sequences:       {icit_sequences:>6}")

    # ── ICIT scale comparison ─────────────────────────────────────────────────
    print_section("ICIT SCALE COMPARISON")
    print(f"  ICIT target objects:  {ICIT_TARGET['objects']:>6}  current: {len(canonical):>6} ({pct(len(canonical), ICIT_TARGET['objects'])})")
    print(f"  ICIT target texts:    {ICIT_TARGET['texts']:>6}  current: {icit_sequences:>6} ({pct(icit_sequences, ICIT_TARGET['texts'])})")
    total_si = len([s for s in sign_instances if s.get("source_sign_id") not in ("000", "++")])
    print(f"  ICIT target signs:    {ICIT_TARGET['sign_occurrences']:>6}  current: {total_si:>6} ({pct(total_si, ICIT_TARGET['sign_occurrences'])})")

    # ── By source ─────────────────────────────────────────────────────────────
    print_section("OBJECTS BY SOURCE (canonical)")
    by_source = Counter(o.get("source_system", "unknown") for o in canonical)
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"  {source:<40} {count:>6}")

    # ── Rights breakdown ──────────────────────────────────────────────────────
    print_section("RIGHTS STATUS (canonical)")
    by_rights = Counter(o.get("rights_status", "unknown") for o in canonical)
    for rights, count in sorted(by_rights.items(), key=lambda x: -x[1]):
        ml = "ML-OK" if rights in ("CC0", "MIT") else ("RES" if rights in ("CC BY 4.0",) else "    ")
        print(f"  {rights:<40} {count:>6}  {ml}")

    # ── Diplomatic text coverage ──────────────────────────────────────────────
    print_section("DIPLOMATIC TEXT COVERAGE")
    with_diplomatic = sum(1 for o in canonical if o.get("text_code_diplomatic"))
    with_canonical_ids = sum(1 for o in canonical if o.get("canonical_grapheme_ids"))
    avg_cw = 0.0
    objs_with_si = [o for o in canonical if o.get("sign_instance_count", 0) > 0]
    if objs_with_si:
        avg_cw = sum(o.get("crosswalk_coverage", 0) for o in objs_with_si) / len(objs_with_si)
    print(f"  Objects with diplomatic text:    {with_diplomatic:>6} / {len(canonical)} ({pct(with_diplomatic, len(canonical))})")
    print(f"  Objects with canonical graphemes:{with_canonical_ids:>6} / {len(canonical)} ({pct(with_canonical_ids, len(canonical))})")
    print(f"  Sign instances (non-damage):     {total_si:>6}")
    print(f"  Avg crosswalk coverage:          {avg_cw:.1%}")

    # ── Quarantine causes ─────────────────────────────────────────────────────
    print_section("QUARANTINE CAUSES")
    reasons = Counter(o.get("quarantine_reason", "unknown") for o in quarantine if o.get("quarantine_reason"))
    for reason, count in sorted(reasons.items(), key=lambda x: -x[1])[:10]:
        print(f"  {reason[:55]:<55} {count:>5}")
    if not reasons:
        print("  (no quarantined objects)")

    # ── Gaps and next actions ─────────────────────────────────────────────────
    print_section("GAPS AND NEXT ACTIONS")
    # Check what free sources have been acquired
    sources_with_data = []
    sources_empty = []
    for sd in sorted(source_dirs):
        if not sd.is_dir():
            continue
        raw_dirs = list((sd / "raw").iterdir()) if (sd / "raw").exists() else []
        if raw_dirs:
            sources_with_data.append(sd.name)
        elif not (sd / "provenance.yaml").exists() or "STUB" not in (sd / "provenance.yaml").read_text("utf-8", errors="ignore")[:200]:
            sources_empty.append(sd.name)
    print(f"  Sources with data:  {', '.join(sources_with_data) or 'none'}")
    print(f"  Sources empty/need acquisition: {', '.join(sources_empty) or 'none'}")
    print()
    print("  Run order for gaps:")
    print("    1. shell.cmd python backend/scripts/corpus_indus_acquire_free.py --tier all")
    print("    2. shell.cmd python backend/scripts/corpus_indus_objectize.py")
    print("    3. shell.cmd python backend/scripts/corpus_indus_normalize.py")
    print("    4. shell.cmd python backend/scripts/corpus_indus_export.py")
    print("    5. shell.cmd python backend/scripts/corpus_indus_status.py  (this script)")
    print()
    print("  Paid sources needing decision:")
    print("    - CISI bundle (€300) + CISI 3.3 (€220) — highest value")
    print("    - Wells books (~£60) — sign-list methodology")
    print("    - Contact RMRL early for concordance cooperation")

    # ── JSON report ───────────────────────────────────────────────────────────
    status_data = {
        "_citation": {
            "primary_sources": ["A.1", "A.7", "I.1", "I.2", "I.3", "I.4", "I.5"],
            "derivation": "Corpus status report for ICIT-scale Indus reconstruction.",
        },
        "timestamp": datetime.utcnow().isoformat(),
        "icit_target": ICIT_TARGET,
        "pipeline": {
            "staging": len(staging),
            "quarantine": len(quarantine),
            "canonical": len(canonical),
            "open_export": len(open_export),
            "research_export": len(research_export),
            "icit_sequences": icit_sequences,
            "sign_instances_total": len(sign_instances),
        },
        "coverage_pct": {
            "objects": round(len(canonical) / ICIT_TARGET["objects"] * 100, 1),
            "texts": round(icit_sequences / ICIT_TARGET["texts"] * 100, 1),
            "sign_occurrences": round(total_si / ICIT_TARGET["sign_occurrences"] * 100, 1),
        },
        "by_source": dict(by_source),
        "by_rights": dict(by_rights),
        "diplomatic_coverage_pct": round(with_diplomatic / max(len(canonical), 1) * 100, 1),
        "avg_crosswalk_coverage": round(avg_cw, 3),
    }
    rpt_dir = REPO / "backend" / "reports"
    rpt_dir.mkdir(parents=True, exist_ok=True)
    rpt_path = rpt_dir / f"indus_corpus_status_{TODAY}.json"
    rpt_path.write_text(json.dumps(status_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nJSON report: {rpt_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
