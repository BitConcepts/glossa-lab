"""Experiment Graph Nodes: Phase-141 (spec 025, FROZEN
2026-10-10) — F1 leave-one-site-out sensitivity.

Ledger-sequence Phase-141 (2026-10-10): under Spec 025
sec.5 and phase141-freeze.md (frozen with PR #131),
this phase recomputes the Phase-136 F1 test (terminal-
class x object type, ICIT-lineage layer (horus84)
joined subset) on the three leave-one-site-out subsets
of its eligible strata — L-MD (drop Mohenjo-daro),
L-HA (drop Harappa), L-KA (drop Kalibangan) — with the
Phase-136 machinery unchanged and the stratum-drop
selector as the only added parameter. Estimability is
re-applied per subset mechanically (Phase-136 sec.5
rule). Robustness criterion (sec.5): F1 is stable iff
every estimable subset's MH common OR > 1 with its 95%
CI excluding 1; otherwise the dropped site is named
LOAD-BEARING. Raw p-values only; NO q-values (Q4(b));
LOSO mints no verdicts — a robustness statement about
F1 only. The full results are the committed
reports/phase141_results.json; the report is
reports/phase141_report.md.

  IndusPhase141Loso
      F1 leave-one-site-out robustness summary
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_RESULTS = _REPO / "reports" / "phase141_results.json"
_LAYER = (Path.home() / "workspace" / "research_notes"
          / "indus-data-deep-sweep-20261008" / "downloads"
          / "horus84-computational-linguistics" / "data"
          / "inscriptions.csv")


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _summary(results: dict, source: str) -> dict:
    return {
        "source": source,
        "phase": results["phase"],
        "test": results["test"],
        "lineage_label": results["lineage_label"],
        "reproduction_matches_phase136":
            results["reproduction_no_drop"]
            ["matches_committed_phase136_exactly"],
        "subsets": {
            label: {
                "dropped_site": cfg["dropped_site"],
                "estimable":
                    cfg["estimability"]["estimable"],
                "mh_common_odds_ratio": (
                    cfg["effect_sizes"] or {}).get(
                        "mh_common_odds_ratio"),
                "mh_ci95": (cfg["effect_sizes"] or {}).get(
                    "mh_ci95"),
                "raw_p": (cfg["test"] or {}).get("raw_p"),
            } for label, cfg in results["subsets"].items()},
        "robustness_outcome": results["robustness_outcome"],
        "anchors_sha256": results["anchors_sha256"],
        "ai_disclosure": results["ai_disclosure"],
    }


def _run_results():
    """Recompute via the phase script when the local-store
    inputs are present; otherwise serve the committed
    results (the script's inputs are local-store files
    that never enter git)."""
    script = _SCRIPTS / "phase141_loso.py"
    if script.exists() and _LAYER.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=1800,
                cwd=str(_REPO))
            if r.returncode == 0 and _RESULTS.exists():
                return _summary(
                    json.loads(_RESULTS.read_text("utf-8")),
                    "script_recomputed")
        except Exception:  # noqa: BLE001
            pass
    if _RESULTS.exists():
        return _summary(json.loads(_RESULTS.read_text("utf-8")),
                        "committed_results")
    return {"error": "phase141 results not found"}


def _phase141_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase141Loso",
         "Phase-141 F1 Leave-One-Site-Out Sensitivity "
         "(spec 025)",
         "Phase-141 (spec 025, FROZEN 2026-10-10): LOSO "
         "sensitivity of F1 (Phase-136: terminal-class x "
         "object type, ICIT-lineage layer (horus84) "
         "joined subset) — drop Mohenjo-daro / Harappa / "
         "Kalibangan in turn from the eligible strata "
         "and recompute the CMH / Mantel-Haenszel common "
         "OR per subset (Phase-136 machinery unchanged; "
         "B = 9,999, seed 20261009; sec.5 estimability "
         "re-applied mechanically). Robustness statement "
         "about F1 only; no verdicts minted; no q-values "
         "(Q4(b)). Recomputes from the local store when "
         "present and otherwise serves the committed "
         "results JSON. CPU."),
    ]
    nodes = []
    for nid, name, desc in specs:
        def fn(i, p):
            return {**_run_results(), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
