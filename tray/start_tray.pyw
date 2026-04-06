"""Glossa Lab tray entry point.

This file is executed directly by pythonw.exe (no console window).
It sets sys.path itself so no PYTHONPATH environment variable is required.
Task Scheduler task: pythonw.exe  <repo>\\tray\\start_tray.pyw

.pyw extension means Windows Associates it with pythonw.exe automatically.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent          # tray/
_ROOT = _HERE.parent                             # repo root
_BACKEND = _ROOT / "backend"

for _p in (str(_HERE), str(_BACKEND)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from glossa_tray.main import main  # noqa: E402

if __name__ == "__main__":
    main()
