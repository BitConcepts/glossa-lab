"""Experiment Graph Nodes: Phase-124–125.

  IndusFishPolysemy   Phase-124: Fish-sign polysemy test (Avishai hypothesis)
                       Isolated vs compound split, site stratification,
                       Arthaśāstra maritime admin cross-reference
  IndusArthasastraMine Phase-125: Mine Martini (2025) for AdhP terms mappable
                       to Indus sign readings
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


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


def _phase124_125_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    specs = [
        (
            "IndusFishPolysemy",
            "Fish-Sign Polysemy Test (Avishai Roif 2026)",
            "phase124_fish_polysemy.py",
            "Phase-124: Tests Avishai Roif's polysemy hypothesis for the Indus fish sign. "
            "Separates M047/M001 occurrences into isolated (solo inscription) vs compound "
            "(multi-sign sequence) and runs coastal enrichment test on each subset. "
            "Cross-references compound contexts with Arthaśāstra superintendent categories "
            "(nāvadhyakṣa = Ship Superintendent) from Martini (2025). CPU.",
        ),
        (
            "IndusArthasastraMine",
            "Martini 2025 Arthaśāstra Mining",
            "phase125_arthasastra_mine.py",
            "Phase-125: Extracts Arthaśāstra (AdhP) administrative terminology from Martini "
            "(2025) that maps onto Indus sign readings. Key terms: kāra (tax), civārika "
            "(cloth/maintenance money), akṣayanīvī (perpetual endowment), viśikhā (market "
            "street), bhata/bhakta (food rations), nāvadhyakṣa (Ship Superintendent). "
            "Cross-references with DEDR anchors and generates Avishai correspondence data. CPU.",
        ),
    ]

    nodes = []
    for nid, name, script, desc in specs:
        def _make_fn(s=script):
            def fn(inputs: dict, params: dict) -> dict:
                return _run(s)
            return fn

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"}],
            params_schema={"type": "object", "properties": {}},
            fn=_make_fn(),
        ))
    return nodes
