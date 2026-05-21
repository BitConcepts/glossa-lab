"""Experiment Graph Nodes: Phase-122–123 (closing the final gap).

  IndusSyllabicSA      Phase-122: SA with syllabic Dravidian LM (500 CV syllables)
                        for the 46 remaining UNKNOWN-tier signs
  IndusMundaSubstrate  Phase-123: Munda/BMAC substrate vocabulary analysis
                        for signs unresolved after Phase-122
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


def _get_device():
    try:
        from glossa_lab.gpu_utils import detect_device  # noqa: PLC0415
        return detect_device()
    except Exception:  # noqa: BLE001
        return "cpu"


def _run(script: str, timeout: int = 3600) -> dict:
    s = _SCRIPTS / script
    rp = _REPORTS / script.replace(".py", ".json")
    if not s.exists():
        return {"error": f"Script not found: {script}"}
    try:
        r = subprocess.run(
            [sys.executable, str(s)],
            capture_output=True, text=True,
            timeout=timeout, cwd=str(_REPO),
        )
        if r.returncode != 0:
            return {"error": f"exit {r.returncode}", "stderr": r.stderr[-600:]}
    except subprocess.TimeoutExpired:
        return {"error": f"timeout after {timeout}s"}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}
    if rp.exists():
        try:
            return json.loads(rp.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


def _phase122_123_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    specs = [
        (
            "IndusSyllabicSA",
            "Syllabic LM SA — Remaining 46 Signs",
            "phase122_syllabic_lm_sa.py",
            "Phase-122: Re-runs SA on the 46 remaining UNKNOWN-tier signs using "
            "the dravidian_syllabic_lm.json (500 CV syllables: ka, na, ta, pu…) "
            "instead of the word-level LM. Syllabic LM gives crisp 2-3 char readings "
            "with higher consistency. All 243 H+M anchors pinned. GPU.",
        ),
        (
            "IndusMundaSubstrate",
            "Munda/BMAC Substrate Analysis",
            "phase123_munda_substrate.py",
            "Phase-123: Analyzes signs unresolved after Phase-122 for potential "
            "Munda proto-vocabulary, BMAC substrate words (Witzel 1999), and Brahui "
            "(Dravidian outlier) cognates. Identifies which signs may be substrate "
            "loans rather than native Dravidian. CPU.",
        ),
    ]

    nodes = []
    for nid, name, script, desc in specs:
        def _make_fn(s=script):
            def fn(inputs: dict, params: dict) -> dict:
                return {**_run(s), "gpu_device": _get_device()}
            return fn

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[
                {"name": "result",     "type": "json"},
                {"name": "gpu_device", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_make_fn(),
        ))
    return nodes
