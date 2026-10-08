"""Phase-125 (spec 019) entry point for the experiment graph.

Runs the frozen cross-compilation positional comparison:
per-sign positional profiles computed within the mayig/CISI
compilation and within the Holdat compilation separately
(never pooled), joined only through the Phase-122
crosswalk v1; PRIMARY arm = high-confidence unambiguous
pairs, floor 8, verdict per spec section 6 (median TV,
Spearman rho on initial/terminal rates, pairing-shuffle
null B = 999 seed 125125). Sensitivity arms A/B are
reported separately and never pooled into the verdict.
No object-level join is performed (spec section 2.1).
See backend/glossa_lab/phase125_run.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase125_run import run_all  # noqa: E402

if __name__ == "__main__":
    out = run_all()
    print({"verdict": out["verdict"],
           "arms": {k: {"stats": v["stats"], "pattern": v["pattern"]}
                    for k, v in out["arms"].items()},
           "anchors_unchanged": out["anchors_unchanged"]})
