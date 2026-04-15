"""Runner: Fuls NW Semitic RTL Corrected Experiment.

Runs the RTL-corrected mapping inference with Dr. Fuls' verified anchors.
Uses run_cli() so the job appears in the Jobs panel (if backend is running).

Conditions:
  A — 20 seeds, no anchors (RTL-corrected sequences)
  B — 20 seeds, Dr. Fuls' verified anchors: 004=T, 066=M, 208=N, 133=ayin, 128=L, 080=W

Output: reports/fuls_rtl_corrected_YYYYMMDDTHHMMSS.json
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from glossa_lab.experiments.fuls_rtl_corrected import FulsRTLCorrected

if __name__ == "__main__":
    print("=" * 60)
    print("  Fuls NW Semitic RTL Corrected Experiment")
    print("  Conditions: A (no anchors) + B (Fuls verified anchors)")
    print("  Seeds: 20 per condition, parallel execution")
    print("=" * 60)
    FulsRTLCorrected().run_cli()
