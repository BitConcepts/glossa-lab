"""Experiment Graph Nodes: Phase-127.

  IndusGulfCorpusAnalysis  Phase-127a: Process 3 Gulf seal catalogues
                            (Saar/Crawford 2001, Failaka Tell F6/Hojlund 2012,
                            Failaka Vol 2/David-Cuny & Neyme 2015).
                            Identifies corpus type and extracts Dilmun fish motif data.
  IndusRoifMining          Phase-127b: Mine Avishai Roif's 2 papers for sign
                            mappings and Akkadian shorthand model assessment.
  IndusFishSitePolysemy    Phase-127c: Site-level fish sign polysemy test.
                            Lothal (coastal IVC port) vs. 8 inland sites.
                            Extended Phase-124 finding to site stratification.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "backend/reports"


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


def _phase127_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    specs = [
        (
            "IndusRoifMining",
            "Avishai Roif Paper Mining (Phase-127a)",
            "phase127_gulf_corpus_roif_analysis.py",
            "Phase-127a: Mines Avishai Roif's 2 papers — 'Indus Script as Mnemonic Framework' "
            "(6pp) and 'Phonetic-Mnemonic Akkadian Shorthand Approach' (10pp). Extracts Table 1 "
            "sign mappings (Fish=/mi/ mīn, Boat=/ka/ kāy, Jar=/ku/ kūṭam, etc.) and assesses "
            "consistency with Glossa-Lab M-number anchors. Identifies that all 11 Roif sample "
            "inscriptions show fish in compound sequences — no isolated fish in his own data. "
            "Also processes 3 Gulf seal catalogues (551 pages total) and documents that Saar, "
            "Failaka Tell F6, and Failaka Vol 2 contain Dilmun-type seals (NOT Indus script). "
            "Extracts 3 Dilmun fish-in-compound examples from Tell F6 as analogical evidence. "
            "CPU.",
        ),
        (
            "IndusFishSitePolysemy",
            "Fish Sign Site Polysemy Test: Lothal vs Inland (Phase-127b)",
            "phase127_fish_site_analysis.py",
            "Phase-127b: Extended fish-sign polysemy test stratified by site. "
            "Tests 8-sign fish family (M047, M049, M052-M056, M145) across all 9 Holdat sites. "
            "Key proxy: Lothal (IVC coastal port, Gujarat) vs 8 inland administrative centres. "
            "Result: 0/113 fish-sign seals isolated at ANY site — Lothal 0/6, inland 0/107. "
            "Confirms Phase-124 finding is site-invariant; fish is exclusively compound/occupational "
            "in the formal stamp seal documentary register, consistent with Martini 2025 perishable "
            "media hypothesis for commodity tallies. CPU.",
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
