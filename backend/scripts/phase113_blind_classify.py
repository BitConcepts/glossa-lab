"""Phase-113 (spec 012) classification stage entry point.

Sets the BLAS thread-pinning environment BEFORE importing the run
module, then runs ONLY if all three adversarial rounds held:
trains C_3, classifies the blind panel members, unblinds, and
computes the verdict strictly per spec 012 section 10. See
backend/glossa_lab/phase113_run.py.
"""
import os
import sys
from pathlib import Path

for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_var] = "1"

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase114_run import stage_classify  # noqa: E402

if __name__ == "__main__":
    out = stage_classify()
    print({"verdict": out["verdict"]})
