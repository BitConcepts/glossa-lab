"""Experiment Graph Nodes: Phase 436 (Spec 073 —
the keying-surface repair: Registry v2 and
Asset A v2, built from published sources only).

  IndusPhase436KeyingSurfaceRepair   Phase-436:
  step-0 gates in order (0.1 frozen-input
  integrity and the Shakti intake reproduced;
  0.2 baseline reproduction figure by figure —
  Spec 070's 31-sign keyed split and token
  counts, Spec 071's 557-sign census split, the
  498-id Wells map, Asset A v1's census; 0.3
  sources in hand as exhibited at the freeze;
  0.4 blind-entry setup attested), then Registry
  v2 (803 v1 rows byte-identical; 210 icit_wells
  rows added on cited statements in the Fuls
  2023 Catalog's published sign list; a NO
  PUBLISHED IDENTITY schedule naming token 999),
  then Asset A v2 (187 v1 rows carried
  field-for-field; 365 new rows entered blind,
  two-pass, the rule pass first required to
  reproduce Spec 069's recorded pass-2 codings
  on all 187 carried labels), then the coverage
  measurement M1-M5 over the recorded
  populations (counts and class sizes only; no
  predecessor study re-run). Outcome: REPAIRED
  WITH NAMED SHORTFALL (31 of 31 and 556 of 557
  keyed; the celestial class remains 0).

The node serves the phase's committed results JSON
(reports/phase436_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/073-keying-surface-
repair/freeze.md (digest 5419c4c4...); the frozen
spec's contract registration is OSF
https://osf.io/9kh4a/.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _serve(script_name: str, results_name: str) -> dict:
    script = _SCRIPTS / script_name
    results = _REPO / "reports" / results_name
    if script.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=1200,
                cwd=str(_REPO))
            if r.returncode == 0 and results.exists():
                return {"source": "script_recomputed",
                        **json.loads(results.read_text("utf-8"))}
        except Exception:  # noqa: BLE001
            pass
    if results.exists():
        return {"source": "committed_results",
                **json.loads(results.read_text("utf-8"))}
    return {"error": f"{results_name} not found"}


_NODE_SPECS = [
    ("IndusPhase436KeyingSurfaceRepair",
     "phase436_coverage.py",
     "phase436_results.json",
     "Phase-436 Keying-Surface Repair (spec 073)",
     "Phase-436 (spec 073): execution of the frozen Spec "
     "073 contract — step-0 gates in order (0.1 frozen-input "
     "integrity plus the Shakti intake reproduced in census "
     "form; 0.2 baselines reproduced figure by figure; 0.3 "
     "sources in hand as exhibited at the freeze, with Wells "
     "1998 and Mahadevan 1977 struck for non-exhibition; 0.4 "
     "blind-entry setup attested), Registry v2 and Asset A v2 "
     "built under the frozen designs and frozen by digest "
     "(registry 42ab09fb..., asset 681e017d...), then the "
     "coverage measurement over Spec 070's 31-sign and Spec "
     "071's 557-sign recorded populations under the DD-070-9 "
     "route restated over Registry v2. Outcome: REPAIRED "
     "WITH NAMED SHORTFALL — 31 of 31 and 556 of 557 keyed; "
     "token 999 named as NO PUBLISHED IDENTITY; the five "
     "named signs (ICIT 136, 298, 401, 617, 824) resolved and "
     "keyed, each depicted-kind unidentified on the published "
     "labels; the celestial class is 0 beside Spec 071's "
     "floor of 30. No positional quantity computed; neither "
     "predecessor study re-run; both Hunt claims untouched. "
     "CPU."),
]


def _phase436_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    nodes = []
    for nid, script_name, results_name, name, desc in _NODE_SPECS:
        def fn(i, p, _s=script_name, _r=results_name):
            return {**_serve(_s, _r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
