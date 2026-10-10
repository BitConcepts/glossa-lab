"""Experiment Graph Nodes: Phase-139 (spec 025, FROZEN
2026-10-10) — covariate audit + harmonization.

Ledger-sequence Phase-139 (2026-10-10): under the frozen
Spec 025 adjudication (specs/025-stage2-controlled-
followup/spec.md sec.11 — all six asks answered with the
recommended answers), this phase audits the candidate
confounder covariates of the Phase-137 F3 population
(ICIT-lineage layer, horus84) and applies the frozen
sec.4.2 eligibility gate. MARGINS ONLY: coverage,
missingness structure, harmonization margins (chron_band
per Q2(a) published-stratigraphy harmonization; depth_band
per Q3(a) within-site relative tertiles; preservation
collapse), permutable-inscription projections, and the
gate classification (PRIMARY CONTROL / SENSITIVITY) with
the G1 estimability verdict. No association statistic, no
repertoire comparison, and no G1 computation is performed
anywhere in this phase. The full results are the committed
reports/phase139_results.json; the report is
reports/phase139_report.md.

  IndusPhase139CovariateAudit
      Stage 2 controlled follow-up covariate audit
      summary (margins + gate + verdict)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_RESULTS = _REPO / "reports" / "phase139_results.json"
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
        "population": results["population"],
        "spec_sec3_reproduction_matches":
            results["spec_sec3_reproduction"]
            ["matches_spec_sec3"],
        "gate_classifications":
            results["gate"]["classifications"],
        "gate": results["gate"]["per_covariate"],
        "verdict": results["verdict"],
        "anchors_sha256": results["anchors_sha256"],
        "ai_disclosure": results["ai_disclosure"],
    }


def _run_results():
    """Recompute via the phase script when the local-store
    input is present; otherwise serve the committed results
    (the script's input is a local-store file that never
    enters git)."""
    script = _SCRIPTS / "phase139_covariate_audit.py"
    if script.exists() and _LAYER.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=600,
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
    return {"error": "phase139 results not found"}


def _phase139_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase139CovariateAudit",
         "Phase-139 Covariate Audit + Harmonization "
         "(spec 025)",
         "Phase-139 (spec 025, FROZEN 2026-10-10): "
         "covariate audit of the Phase-137 F3 population "
         "(ICIT-lineage layer, horus84) — sec.3 fill tables "
         "reproduced; chron_band harmonized from published "
         "stratigraphies (<= 3 bands, per-cell citations or "
         "UNRECORDED, Class C); depth_band as within-site "
         "relative tertiles; preservation collapsed; the "
         "frozen sec.4.2 eligibility gate applied verbatim "
         "(>= 70% recorded, >= 3 sites at >= 30 recorded, "
         ">= 1,000 permutable) with the adjudicated routing "
         "rule (gate-fail -> sensitivity panel; sole passer "
         "-> primary strata); G1 estimability verdict. "
         "MARGINS ONLY — no association statistic is "
         "computed. Recomputes from the local store when "
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
