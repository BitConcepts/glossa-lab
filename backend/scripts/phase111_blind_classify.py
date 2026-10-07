"""Phase-111 (spec 009) classification stage entry point.

Runs ONLY if the gate stage passed: trains the final model,
classifies the blind panel members, unblinds, and computes the
verdict strictly per spec 009 section 9. See
backend/glossa_lab/phase111_run.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase111_run import run_classify_stage  # noqa: E402

if __name__ == "__main__":
    out = run_classify_stage()
    print({"verdict": out["verdict"]})
