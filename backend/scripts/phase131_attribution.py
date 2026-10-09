"""Phase-131 (spec 022) entry point for the experiment graph.

Runs the frozen source-of-disagreement attribution: for the
Phase-125 PRIMARY result (16 judgeable pairs, median TV
0.636931), attributes the observed disagreement to
segmentation, substitution, insertion/deletion, reading
direction, and composition under the estimators frozen in
spec 022. This phase is attribution diagnostics ONLY; it
does NOT re-score Phase-125 (FAIL — DISAGREEMENT, FINAL)
and does not touch spec 020's NO. See
backend/glossa_lab/phase131_run.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase131_run import run_all  # noqa: E402

if __name__ == "__main__":
    out = run_all()
    a = out["arms"]["a_matched_object_alignment"]
    b = out["arms"]["b_reading_direction"]
    d = out["arms"]["d_synthesis"]
    print({"matched_pairs": a["matcher"]["n_matched"],
           "pair_class_counts": a["pair_class_counts"],
           "b1_median_tv": b["b1_mayig_reversed"]["median_tv"],
           "b2_median_tv": b["b2_holdat_reversed"]["median_tv"],
           "residual_unexplained_share": d["residual_unexplained_share"],
           "anchors_unchanged": out["anchors_unchanged"]})
