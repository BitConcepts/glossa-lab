"""Experiment Graph Nodes: Phase 427 (Spec 065 —
the two unlocated rows of Spec 057: search the
acquired documents' own text layers for the heading;
successor recovery act for S-1 and S-5).

  IndusPhase427S1S5Heading    Phase-427: step-0
  gates, the S-5 document-layer search under the
  carried heading rule, the frozen S-1 two-arm
  contract, and the two-row accounting of spec
  section 6.

The node serves the phase's committed results JSON
(reports/phase427_results.json). It recomputes via
the phase script only when the acquired S-5 file is
present at its pinned local path (spec section
2.2): the file lives in the local research store
only, and on a host without it the script would
close at step 0 — so there the node serves the
committed results rather than re-running the script
on substitute bytes. Freeze: specs/
065-s1-s5-heading-successor/freeze.md (digest
f50a6e9c...); the frozen spec's contract
registration is OSF https://osf.io/34s9u/.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_ACQUIRED_S5 = (
    Path.home() / "workspace" / "research_notes"
    / "indus-data-deep-sweep-20261008" / "downloads"
    / "hunt-without-kings-zenodo-2025"
    / "Without Kings or Conquests-Indus Deciphered_Full.pdf")


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _serve(script_name: str, results_name: str) -> dict:
    script = _SCRIPTS / script_name
    results = _REPO / "reports" / results_name
    if script.exists() and _ACQUIRED_S5.is_file():
        try:
            r = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=1200,
                cwd=str(_REPO))
            if r.returncode == 0 and results.exists():
                data = json.loads(results.read_text("utf-8"))
                if "accounting" in data:
                    return {"source": "script_recomputed",
                            **data}
        except Exception:  # noqa: BLE001
            pass
    if results.exists():
        return {"source": "committed_results",
                **json.loads(results.read_text("utf-8"))}
    return {"error": f"{results_name} not found"}


_NODE_SPECS = [
    ("IndusPhase427S1S5Heading",
     "phase427_s1_s5_heading.py",
     "phase427_results.json",
     "Phase-427 S-1/S-5 Heading Successor (spec 065)",
     "Phase-427 (spec 065): execution of the frozen Spec "
     "065 contract — the successor recovery act for the "
     "two rows Spec 057 (Phase-419) closed SOURCE "
     "UNLOCATED, S-1 (Fuls 2020, Studies on Indus "
     "Script, pp. 57–90) and S-5 (Hunt, Without Kings "
     "or Conquests, Zenodo v1 preprint). Step-0 gates "
     "in frozen order: input integrity under the Spec "
     "038 claims-store form; the acquired S-5 file "
     "asserted by size, SHA-256, and MD5 on the local "
     "file; the S-1 intake determination; order. Then "
     "the acquired S-5 document's own text layer is "
     "searched in full under Spec 057 section 5's "
     "heading rule, every occurrence listed and "
     "judged; S-1 is accounted under the frozen "
     "two-arm contract of spec section 4.2. Outcome "
     "(2026-10-22): headline class B — S-5 RESOLVED, "
     "S-1 STILL BLOCKED. S-5: HEADING ABSENT FROM "
     "DOCUMENT — exactly one occurrence in the "
     "acquired file's text layer (extraction line "
     "340, PDF page 9), sentence-initial inside a "
     "running paragraph of section 5.5, not in "
     "heading form; the sub-state HEADING NOT "
     "PRESENT IN HELD TEXT is converted to a "
     "document-level finding on the acquired file's "
     "SHA-256. S-1: STILL UNLOCATED — ACQUISITION "
     "BLOCKED (no intake-pinned document before the "
     "run; the blocker record is the row's evidence; "
     "no search was run and nothing about the "
     "chapter is found or implied). The heading "
     "record stands superseded-not-retired, by "
     "appended dated note only. This act searched "
     "two documents for a heading. It checked "
     "nothing either passage states. CPU."),
]


def _phase427_node_defs():
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
