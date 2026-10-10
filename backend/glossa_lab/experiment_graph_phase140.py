"""Experiment Graph Nodes: Phase-140 (spec 025, FROZEN
2026-10-10) — G1 controlled F3 re-test.

Ledger-sequence Phase-140 (2026-10-10): under Spec 025
(spec.md sec.4/sec.11, frozen PR #129) and the Phase-139
freeze record + phase140-freeze.md (merged PR #131),
this phase re-runs the Phase-137 F3 site-repertoire test
on the ICIT-lineage layer (horus84) with permutation of
site labels WITHIN composition (Phase-137 type class x
length class) x preservation strata — the primary-
control set is exactly {preservation} (99.9% recorded;
UNRECORDED retained as a stratum level). B = 9,999,
seed 20261009. Verdict per adjudication Q4(b): BH over
G1 alone at q = 0.05 (m = 1) — SUPPORTED under control
iff raw p <= 0.05. Chronology is NOT controlled in the
primary test (period/phase remain uncontrolled
confounders); the EXPLORATORY sensitivity panel
(S-chron: composition x chron_band, 41.9% recorded;
S-depth: composition x depth_band, 51.1% recorded) is
reported as bounds alongside, never as the controlled
verdict. The full results are the committed
reports/phase140_results.json; the report is
reports/phase140_report.md.

  IndusPhase140G1Controlled
      G1 controlled site-repertoire re-test summary
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_RESULTS = _REPO / "reports" / "phase140_results.json"
_LAYER = (Path.home() / "workspace" / "research_notes"
          / "indus-data-deep-sweep-20261008" / "downloads"
          / "horus84-computational-linguistics" / "data"
          / "inscriptions.csv")


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _summary(results: dict, source: str) -> dict:
    g1 = results["g1_primary"]
    panel = results["sensitivity_panel_exploratory"]
    return {
        "source": source,
        "phase": results["phase"],
        "test": results["test"],
        "lineage_label": results["lineage_label"],
        "headline_rider": results["headline_rider"],
        "population": results["population"],
        "regression_matches_phase137_f3":
            results["regression_composition_only"]
            ["matches_committed_phase137_f3_exactly"],
        "g1": {
            "observed_chi_square": g1["observed_chi_square"],
            "permutation": g1["permutation"],
            "p_value_raw": g1["p_value_raw"],
            "benjamini_hochberg": g1["benjamini_hochberg"],
            "verdict": g1["verdict"],
            "permutable_inscriptions":
                g1["permutable_inscriptions"],
            "cramers_v_descriptive":
                g1["cramers_v_descriptive"],
        },
        "sensitivity_panel_exploratory": {
            name: {
                "observed_chi_square":
                    panel[name]["observed_chi_square"],
                "p_value_raw": panel[name]["p_value_raw"],
                "recorded_coverage":
                    panel[name]["recorded_coverage"],
                "permutable_inscriptions":
                    panel[name]["permutable_inscriptions"],
            } for name in ("S_chron", "S_depth")},
        "anchors_sha256": results["anchors_sha256"],
        "ai_disclosure": results["ai_disclosure"],
    }


def _run_results():
    """Recompute via the phase script when the local-store
    input is present; otherwise serve the committed results
    (the script's layer input is a local-store file that
    never enters git)."""
    script = _SCRIPTS / "phase140_g1_controlled.py"
    if script.exists() and _LAYER.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=3600,
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
    return {"error": "phase140 results not found"}


def _phase140_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase140G1Controlled",
         "Phase-140 G1 Controlled Site-Repertoire Re-Test "
         "(spec 025)",
         "Phase-140 (spec 025, FROZEN 2026-10-10): G1 — "
         "the Phase-137 F3 site-repertoire test on the "
         "ICIT-lineage layer (horus84; 5,410 inscriptions, "
         "7 sites) re-run with permutation of site labels "
         "within composition (type class x length class) "
         "x preservation strata (primary-control set "
         "exactly {preservation}; UNRECORDED retained as "
         "a level; B = 9,999, seed 20261009). Verdict by "
         "BH over G1 alone, q = 0.05 (m = 1). Chronology "
         "is NOT controlled in the primary test; the "
         "EXPLORATORY S-chron / S-depth sensitivity "
         "bounds are reported alongside. Recomputes from "
         "the local store when present and otherwise "
         "serves the committed results JSON. CPU."),
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
