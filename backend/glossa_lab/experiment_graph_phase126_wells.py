"""Experiment Graph Nodes: Phase-126 (ledger sequence) —
Wells-split descriptive analysis of the 113 CANDIDATE anchors.

For each of the 113 anchors whose ``confidence`` field is
CANDIDATE in INDUS_FINAL_ANCHORS.json, records its Wells
treatment from the Phase-123 segmentation witness table
(split / merge / unit-same / not-covered / indeterminate;
split components recorded), cross-tabulated against the
evidence features recorded in the anchors file. Descriptive
design input only: no adjudication of any sign's status, no
promotion or demotion proposed, no anchor changed (anchors
sha256 asserted before and after).

Note: this module is NOT the legacy
experiment_graph_phase126.py node family (Phase-126 ICIT
corpus plan), which predates the ledger-sequence numbering
used here.

  IndusPhase126WellsSplitCandidates
      per-sign Wells treatments + cross-tabs + reports
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


def _run(script: str, args: list[str], report: str, timeout: int = 7200):
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


def _phase126_wells_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase126WellsSplitCandidates",
         "Phase-126 Wells-Split Descriptive Analysis (113 CANDIDATE anchors)",
         "phase126_wells_split_candidates.py", [],
         "phase126_wells_split_candidates_results.json",
         "Phase-126: descriptive design-input analysis — for each "
         "of the 113 CANDIDATE anchors, its Wells treatment from "
         "the Phase-123 witness table (split / merge / unit-same "
         "/ not-covered / indeterminate; split components "
         "recorded), cross-tabulated against the anchor evidence "
         "features recorded in INDUS_FINAL_ANCHORS.json. No "
         "adjudication, no status changes; anchors sha256 "
         "asserted before and after. CPU."),
    ]
    nodes = []
    for nid, name, script, args, report, desc in specs:
        def fn(i, p, s=script, a=args, r=report):
            return _run(s, a, r)

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"}],
            params_schema={"type": "object", "properties": {}}, fn=fn))
    return nodes
