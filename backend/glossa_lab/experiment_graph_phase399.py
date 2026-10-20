"""Experiment Graph Nodes: Phase 399 (Spec 035 —
PRED-2026-010: scoring the clean-withholding successor,
exactly as registered).

  IndusPhase399Pred010Scoring    Phase-399: step 0
  (registration re-verification, input integrity,
  training-pool reproduction, crosswalk coverage —
  fail-closed, in the frozen order), then — only
  behind a full step-0 pass — the registered scoring

The node serves the phase's committed results JSON
(reports/phase399_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
035-pred-2026-010-scoring/freeze.md (digest
d72a50e1...); the prediction's preregistration is OSF
https://osf.io/wjebq/ (DOI 10.17605/OSF.IO/WJEBQ);
the frozen spec's own contract registration is OSF
https://osf.io/qkj8d/.
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
    ("IndusPhase399Pred010Scoring",
     "phase399_pred010_step0.py",
     "phase399_results.json",
     "Phase-399 PRED-2026-010 Scoring (spec 035)",
     "Phase-399 (spec 035): execution of the frozen Spec 035 "
     "contract — PRED-2026-010 scored exactly as registered "
     "(at least 70% of the trained INITIAL signs {P000, P217, "
     "P324}, derived at registration from the CISI "
     "Mohenjo-daro-only pool, at Harappa start rate at least "
     "0.40 on the withheld Yajnadevam Harappa sequences). "
     "Step 0 runs first, fail-closed, in the frozen order: "
     "0.1 the prediction's OSF preregistration (wjebq) "
     "re-verified accepted and public; 0.2 the four "
     "registered input pins verified bytewise (the withheld "
     "file hashed only, never opened); 0.3 the training "
     "pool re-derived (179 CISI Mohenjo-daro inscriptions, "
     "manifest hash) and the recorded classification "
     "reproduced exactly; 0.4 crosswalk coverage of the "
     "trained signs under the frozen best-match reading — "
     "any unmappable trained sign (one of three is 33%, "
     "above the registered 20% cap) closes the study as "
     "CANNOT BE RUN AS WRITTEN before the withheld file is "
     "opened. In this execution 0.1–0.3 passed and 0.4 "
     "closed the study: P217 and P324 have confirmed "
     "best-match counterparts (Y0520; Y0740), but P000 has "
     "none — it appears only as a top-3 alternative on four "
     "rows — so no scoring ran and PRED-2026-010 remains "
     "unscored (neither CONFIRMED nor NOT CONFIRMED). CPU."),
]


def _phase399_node_defs():
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
