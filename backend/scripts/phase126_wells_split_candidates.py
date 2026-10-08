"""Phase-126 entry point for the experiment graph.

Runs the Wells-split descriptive analysis of the 113 CANDIDATE
anchors: per-sign Wells treatment from the Phase-123 witness
table (split / merge / unit-same / not-covered /
indeterminate, with split components recorded), cross-tabulated
against the evidence features recorded in the anchors file
(exact field names). Descriptive design input only: no
adjudication, no promotion or demotion proposed, no anchor
changed (anchors sha256 asserted before and after).
See backend/glossa_lab/phase126_run.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase126_run import run_all  # noqa: E402

if __name__ == "__main__":
    out = run_all()
    print({"headline_counts": out["headline_counts"],
           "anchors_unchanged": out["anchors_unchanged"]})
