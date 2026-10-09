"""Phase-128 entry point: build the integrated evidence
dossiers for the 44 pending_non_sa_validation anchors.

Writes reports/phase128_evidence_dossiers_44.{json,csv,md}.
Descriptive only: no status recommendations, no adjudications,
no PRED content. The anchors file is asserted byte-identical
(sha256) before and after.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase128_run import run_all  # noqa: E402

if __name__ == "__main__":
    doc = run_all()
    print(
        {
            "n_dossiers": doc["n_dossiers"],
            "bucket_counts": doc["bucket_counts"],
            "anchors_unchanged": doc["anchors_unchanged"],
        }
    )
