"""Phase-113 (spec 012) rounds stage entry point for the experiment graph.

Sets the BLAS thread-pinning environment BEFORE importing the run
module, then runs the rounds stage: per-round gates, frozen round
classifiers, the adversarial searches, and the round control
checks. See backend/glossa_lab/phase113_run.py.
"""
import os
import sys
from pathlib import Path

for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_var] = "1"

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase113_run import stage_rounds  # noqa: E402

if __name__ == "__main__":
    out = stage_rounds()
    print({"status": out["status"], "verdict": out["verdict"]})
