"""Runner script for the Fuls NW Semitic RTL Corrected Experiment.

This is the CORRECT way to run a Glossa Lab experiment from the command line (H14).
It uses run_cli() which:
  - Registers a Job in the Jobs panel (visible in UI)
  - Streams structured log output
  - Saves the JSON result to reports/
  - Shows the GPU/CPU badge in the Jobs panel

Usage:
    shell.cmd python backend/scripts/run_fuls_rtl.py

Equivalent UI action:
    Experiments -> Fuls RTL Corrected -> Run
"""
import sys
import os

# Ensure backend is on the path
_BACKEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

from glossa_lab.experiments._legacy.fuls_rtl_corrected import FulsRTLCorrected as FulsRtlCorrected

if __name__ == "__main__":
    print("Starting Fuls RTL Corrected Experiment...")
    print("Job will appear in the Glossa Lab Jobs panel if backend is running.")
    print()
    FulsRtlCorrected().run_cli()
