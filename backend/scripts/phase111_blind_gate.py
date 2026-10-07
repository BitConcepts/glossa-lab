"""Phase-111 (spec 009) gate stage entry point for the experiment graph.

Builds the blinded panel (custodian) and evaluates the frozen
validation gate on known corpora only. See
backend/glossa_lab/phase111_run.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase111_run import run_gate_stage  # noqa: E402

if __name__ == "__main__":
    out = run_gate_stage(rebuild="--rebuild" in sys.argv)
    print({"gate_passed": out["gate"]["gate_passed"], "verdict": out["verdict"]})
