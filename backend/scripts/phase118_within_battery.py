"""Phase-118 (spec 017) entry point for the experiment graph.

Runs the frozen within-compilation validation protocol v2
(Holdat-internal; Phase-116 R-NONE forbids the cross-corpus
gate): the carried seed-117 partition is asserted (3,531 /
3,471 tokens), judgeability is recomputed and asserted
(J94 = 67, JKUR = 29), phi is computed per cross-fit
direction, and the calibration gates fire first (positive:
VALIDATED share over J94 >= 0.50; negative: over JKUR,
VALIDATED = 0 and DEMOTE share >= 0.25). The 44 flagged
anchors are run only if the battery is accepted. See
backend/glossa_lab/phase118_run.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase118_run import run_all  # noqa: E402

if __name__ == "__main__":
    out = run_all()
    gates = out["calibration"]["gates"]
    print({"battery_accepted": gates["battery_accepted"],
           "phi": {d: rec["phi"]
                   for d, rec in out["phi"]["directions"].items()},
           "judgeability": out["judgeability"]["counts"],
           "positive_gate": gates["positive"],
           "negative_gate": gates["negative"],
           "strict_tally":
               out["calibration"]["strict94_leave_one_out"]["tally"],
           "kur_tally":
               out["calibration"]["kur113_negative_control"]["tally"],
           "main_tally": (out["main_run"] or {}).get("tally")})
