#!/usr/bin/env python3
"""Phase-116 (spec 015) corpus-harmonization study runner.

Thin entry point: delegates to glossa_lab.phase116_run.run_all,
which asserts the Phase-115 baseline reproduction (spec section
3) before executing the frozen matcher and hypothesis arms, and
writes reports/phase116_harmonization_results.json +
reports/phase116_harmonization_summary.md. Diagnostic only.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.phase116_run import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
