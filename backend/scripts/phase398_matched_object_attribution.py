"""Phase-398 (spec 034) entry point for the experiment graph.

Runs the frozen matched-object attribution: step 0 builds
the object bridge through the three frozen routes (CISI
catalogue layer; the Mahadevan side's published object
references admitted through the Phase-130 intake schema;
the 44 Phase-128 dossiers) and applies the frozen gate
(>= 150 matched objects with texts of three or more signs
in both compilations). Behind the gate only, step 1
measures Phase-125's own statistic on the matched subset
and decomposes the remainder in Phase-131's categories.
Below the gate the study closes as TOO THIN TO ATTRIBUTE
with the census as the finding. The settled Phase-125
verdict is never re-judged. See
backend/glossa_lab/phase398_matched_object.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glossa_lab.phase398_matched_object import run_all  # noqa: E402

if __name__ == "__main__":
    out = run_all()
    census = out["step0_census"]["bridge"]
    verdict = out["verdict"]
    print({"matched_objects": census["matched_objects"],
           "gate_objects": census["gate"]["n_gate_objects"],
           "gate_passed": census["gate"]["gate_passed"],
           "outcome": verdict["outcome"],
           "matched_object_median_tv":
               verdict["matched_object_median_tv"],
           "anchors_unchanged": out["anchors_unchanged"]})
