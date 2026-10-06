"""Experiment Graph Nodes: Phase-108 (spec 006) — Anchor Provenance Audit.

Ledger-sequence Phase-108 (2026-10-06): per-anchor provenance trails,
pre-registered classification, SA-independent subset recomputation,
and the circularity / downstream impact map, after Phase-107 falsified
SA as evidence for sign values. Audit only — no anchor data changes.

  IndusProvenanceExtract    Step 1: evidence trails for all 287 anchors
  IndusProvenanceClassify   Step 2: pass-1 classification / --finalize
  IndusProvenanceRecompute  Step 3: subset recomputation
  IndusProvenanceImpact     Step 4: circularity + impact map
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _run(script: str, args: list[str], report: str, timeout: int = 1800):
    s = _SCRIPTS / script
    rp = _REPORTS / report
    if not s.exists():
        return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(s), *args], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired:
        return {"error": f"timeout {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    if rp.exists():
        try:
            return json.loads(rp.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


def _phase108_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusProvenanceExtract", "Anchor Provenance Extraction",
         "phase108_provenance_extract.py", [], "phase108_anchor_trails.json",
         "Phase-108 Step 1 (spec 006): assemble per-anchor evidence trails from in-repo sources only (entry fields, ledgers, phase artifacts, claims, crosswalk). CPU."),
        ("IndusProvenanceClassify", "Anchor Provenance Classification",
         "phase108_provenance_classify.py", [], "phase108_provenance_register_draft.json",
         "Phase-108 Step 2 (spec 006): pass-1 classification under the pre-registered taxonomy; --finalize merges hand-review decisions into the final register + summary. CPU."),
        ("IndusProvenanceRecompute", "SA-Independent Subset Recomputation",
         "phase108_provenance_recompute.py", [], "phase108_subset_recomputation.json",
         "Phase-108 Step 3 (spec 006): token coverage, Phase-58 phonotactics, Parpola agreement, Phase-69 site invariance recomputed on the SA-independent subset. CPU."),
        ("IndusProvenanceImpact", "Circularity + Impact Map",
         "phase108_provenance_impact.py", [], "phase108_impact_map.json",
         "Phase-108 Step 4 (spec 006): circular chains, 31-claims map, headline-number map, foundation-check SA-citation map. A map, not an edit. CPU."),
    ]
    nodes = []
    for nid, name, script, args, report, desc in specs:
        def fn(i, p, s=script, a=args, r=report):
            return {**_run(s, a, r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}}, fn=fn))
    return nodes
