"""Phase-127 (spec 021) entry point for the experiment graph.

Runs the frozen cross-compilation disagreement diagnostic:
for the 16 Phase-125 PRIMARY judgeable pairs, prices how
much of the observed disagreement (median TV 0.636931)
sampling noise (split-half / matched-size / inscription
bootstrap), crosswalk ambiguity (neighbourhood
decomposition), and composition (site / iconography
controls) can account for, plus a power statement for the
frozen Phase-125 gates. This phase does NOT re-score
Phase-125 and issues no verdict; the Phase-125 FAIL —
DISAGREEMENT verdict is final and unchanged. See
backend/glossa_lab/phase127_run.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase127_run import run_all  # noqa: E402

if __name__ == "__main__":
    out = run_all()
    a = out["arms"]["a_split_half"]
    b = out["arms"]["b_matched_size"]["median_tv_distribution"]
    c = out["arms"]["c_bootstrap"]["median_tv"]
    print({"noise_floor_fullsize_est": a["noise_floor_fullsize_est"],
           "matched_size_median": b["median"],
           "matched_size_share_ge_observed":
               b["share_replicates_ge_observed"],
           "bootstrap_median_tv_ci": [c["ci95_lo"], c["ci95_hi"]],
           "anchors_unchanged": out["anchors_unchanged"]})
