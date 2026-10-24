"""Experiment Graph Nodes: Phase 435 (Spec 041 —
the site x local-label period mapping Spec 040's
closure requires).

  IndusPhase435SitePeriodMapping   Phase-435: the
  step-0 gates in order (G0.1 the ICIT-lineage
  layer (horus84) asserted at its pin c368f290...;
  G0.2 the Phase-137 F3 population reproduced —
  the seven sites, 5,410 rows; G0.3 the value-level
  label census reproducing the recorded tables and
  the Phase-139 covariates asserted against the
  layer; G0.4 anchors at the refreshed pin
  df0cf620...; G0.5 source admissibility classified
  before extraction; G0.6 the no-computation fence),
  then construction under spec section 7 (published
  determinations only, DD-039-3 carried; contested
  cells retained with binding value UNASSIGNED and
  no sensitivity label frozen, DD-041-10), the
  completeness assertion of section 5.5, and the
  section 8 placement counts under derivations
  A1 / A2 / B / C, none adopted.

The node serves the phase's committed results JSON
(reports/phase435_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/041-site-local-label-
period-mapping/freeze.md (digest fe618886...); the
frozen spec's contract registration is OSF
https://osf.io/w2vkn/.
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
                [sys.executable, str(script), "run"],
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
    ("IndusPhase435SitePeriodMapping",
     "phase435_site_period_mapping.py",
     "phase435_results.json",
     "Phase-435 Site x Local-Label Period Mapping (spec 041)",
     "Phase-435 (spec 041): execution of the frozen Spec "
     "041 contract - step-0 gates in order (G0.1 the "
     "ICIT-lineage layer (horus84) at pin c368f290...; "
     "G0.2 the Phase-137 F3 population, seven sites and "
     "5,410 rows; G0.3 the value-level label census "
     "(period 2,266 / phase 2,638 / both 1,788 / union "
     "3,116) with the Phase-139 covariates asserted "
     "against the layer; G0.4 anchors at df0cf620...; "
     "G0.5 source admissibility classified before "
     "extraction; G0.6 no G1 quantity computed), then "
     "construction under the published-determinations-"
     "only standard (DD-039-3 carried): one cell per "
     "attested (site, field, local label) triple, "
     "contested cells retaining every admissible "
     "determination with binding value UNASSIGNED and "
     "no sensitivity label frozen (DD-041-10), "
     "unassigned cells carrying exactly one enumerated "
     "reason; placement counts under derivations "
     "A1 / A2 / B / C with the 57.6 percent ceiling "
     "stated, no derivation adopted. Outcome as "
     "recorded in reports/phase435_results.json. CPU."),
]


def _phase435_node_defs():
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
