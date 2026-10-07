"""Phase-117 (spec 016) entry point for the experiment graph.

Runs the frozen within-compilation validation protocol
(Holdat-internal; Phase-116 R-NONE forbids the cross-corpus
gate): the seed-117 partition is asserted, phi is computed,
calibration gates fire first (STRICT94 leave-one-out >= 47/94;
KUR113 <= 5/113); the 44 flagged anchors are run only if the
battery is accepted. See backend/glossa_lab/phase117_run.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase117_run import run_all  # noqa: E402

if __name__ == "__main__":
    out = run_all()
    gates = out["calibration"]["gates"]
    print({"battery_accepted": gates["battery_accepted"],
           "phi": out["phi"]["phi"],
           "strict_tally":
               out["calibration"]["strict94_leave_one_out"]["tally"],
           "kur_tally":
               out["calibration"]["kur113_negative_control"]["tally"],
           "main_tally": (out["main_run"] or {}).get("tally")})
