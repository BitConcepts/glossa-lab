"""Wrapper to run Fuls validation suite without the cli_bridge logging conflict.

Calls run_validation_suite() directly. Output goes to reports/fuls_validation_suite_<ts>.json
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(_HERE)
ROOT     = Path(_BACKEND).parent

for _p in (_BACKEND, os.path.join(_BACKEND, "tests")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Defer import until path is set
from glossa_lab.experiments._legacy.fuls_validation_suite import run_validation_suite

if __name__ == "__main__":
    print("Running Fuls Validation Suite (estimated 15-20 minutes)...")
    result = run_validation_suite(verbose=True)
    print("\n[OK] Validation suite complete.")
