#!/usr/bin/env python3
"""Phase-120: Bhaskar (2024) descriptive triage of the 44 flagged anchors.

Reads (never modifies) backend/reports/INDUS_FINAL_ANCHORS.json,
classifies the 44 anchors with validation_status
pending_non_sa_validation against the curated Bhaskar disagreement
register in glossa_lab/phase120_bhaskar.py, and writes:

  reports/phase120_bhaskar_disagreements.json / .csv
      every cross-source disagreement case the article + ESMs document
  reports/phase120_bhaskar_triage_44.json
      the per-sign triage of the 44 (classification + rationale)

Optionally (--esm-dir) audits the extraction against the ESM PDFs'
text layer: counts labelled E1 blocks in ESM2 and reports whether
each register case's location file was readable. The register in
the module is the data of record; the PDFs are external source
material and are never committed.

Descriptive only: no anchor status changes, no validation, no PRED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.phase120_bhaskar import (  # noqa: E402
    disagreement_csv,
    disagreement_table_rows,
    extract_pdf_text,
    count_labelled_e1,
    triage_all,
)

ANCHORS = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--esm-dir", type=Path, default=None,
                    help="directory holding the Bhaskar ESM PDFs (audit only)")
    args = ap.parse_args()

    before = hashlib.sha256(ANCHORS.read_bytes()).hexdigest()
    rows = triage_all(ANCHORS)
    assert len(rows) == 44, f"expected 44 flagged anchors, got {len(rows)}"
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.classification] = counts.get(r.classification, 0) + 1

    audit = {}
    if args.esm_dir is not None:
        esm2 = args.esm_dir / "43539_2023_102_MOESM2_ESM.pdf"
        text = extract_pdf_text(esm2) if esm2.exists() else None
        audit = {
            "esm2_found": esm2.exists(),
            "esm2_text_extracted": text is not None,
            "esm2_labelled_e1_blocks": count_labelled_e1(text) if text else None,
            "note": (
                "Labelled-pattern extraction recovers the two ESM2 "
                "'E1 (1):' blocks; the third E1 (ESM7 case 7) is "
                "stated in prose and was recovered by the keyword "
                "sweep + hand reading, not by the label pattern."
            ),
        }

    triage_doc = {
        "phase": 120,
        "title": "Bhaskar (2024) descriptive triage of the 44 flagged anchors",
        "date": "2026-10-08",
        "source": (
            "Bhaskar (2024), Markers and agencies of anisotropy in the "
            "Indus sign system, Indian J. Hist. Sci., "
            "doi:10.1007/s43539-023-00102-3, + ESM1-ESM13"
        ),
        "scope_note": (
            "The ESMs are NOT a per-sign cross-compilation disagreement "
            "table; they are anisotropy datasets. This triage reports "
            "only disagreements Bhaskar explicitly documents (case "
            "register) and never infers concordance from silent use; "
            "hence ALL-AGREE is empty by construction of the source."
        ),
        "anchors_file_sha256_read_only": before,
        "counts": counts,
        "extraction_audit": audit,
        "rows": [asdict(r) for r in rows],
    }
    (REPORTS / "phase120_bhaskar_triage_44.json").write_text(
        json.dumps(triage_doc, indent=2, ensure_ascii=False) + "\n", "utf-8")
    (REPORTS / "phase120_bhaskar_disagreements.json").write_text(
        json.dumps({"phase": 120, "cases": disagreement_table_rows()},
                   indent=2, ensure_ascii=False) + "\n", "utf-8")
    (REPORTS / "phase120_bhaskar_disagreements.csv").write_text(
        disagreement_csv(), "utf-8")

    after = hashlib.sha256(ANCHORS.read_bytes()).hexdigest()
    assert before == after, "anchors file changed during triage (must not)"
    print(f"Phase-120 triage: {counts} (n=44); anchors file untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
