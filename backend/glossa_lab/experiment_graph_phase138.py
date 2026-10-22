"""Experiment Graph Nodes: Phase-138 (spec 024, Stage 2(d)) —
graffiti descriptive protocol.

Ledger-sequence Phase-138 (2026-10-09): the Stage 2(d) arm under
the frozen record
(specs/024-evidence-integration/stage2d-freeze.md). A DESCRIPTIVE
protocol only — no test, no p-value, no inference, and not a
member of the Stage 2 family. The population is the Phase-124
catalogue rows (CISI Vols. 1–2) with object_type exactly
'Graffiti', described by volume, catalogue site, rows-per-object
distribution, side/bis values as printed, motif_chapter (Class C)
as printed, and caption_ocr_score / scale_pct medians and IQRs,
beside a catalogue-composition context table for Seals and
Tablets rows. This node exposes the descriptive summary only;
the full results are the committed reports/phase138_results.json
and the report is reports/phase138_report.md.

  IndusPhase138GraffitiDescriptive
      Stage 2(d) graffiti descriptive summary
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_RESULTS = _REPO / "reports" / "phase138_results.json"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _summary(results: dict, source: str) -> dict:
    graffiti = results["graffiti"]["pooled"]
    return {
        "source": source,
        "phase": results["phase"],
        "family_role": results["family_role"],
        "population": results["population"],
        "distinct_objects_by_site":
            graffiti["distinct_objects_by_site"],
        "no_site_count": graffiti["no_site_count"],
        "rows_per_object_distribution":
            graffiti["rows_per_object_distribution"],
        "motif_chapter": graffiti["motif_chapter"],
        "numeric_descriptors": graffiti["numeric_descriptors"],
        "mandatory_statements": results["mandatory_statements"],
        "ai_disclosure": results["ai_disclosure"],
    }


def _run_descriptive():
    """Recompute via the script when the local store is present;
    otherwise serve the committed results (the script's inputs are
    local-store files that never enter git)."""
    script = _SCRIPTS / "phase138_graffiti_descriptive.py"
    if script.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script)], capture_output=True,
                text=True, timeout=600, cwd=str(_REPO))
            if r.returncode == 0 and _RESULTS.exists():
                return _summary(
                    json.loads(_RESULTS.read_text("utf-8")),
                    "descriptive_recomputed")
        except Exception:  # noqa: BLE001
            pass
    if _RESULTS.exists():
        return _summary(json.loads(_RESULTS.read_text("utf-8")),
                        "committed_results")
    return {"error": "phase138 results not found"}


def _phase138_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase138GraffitiDescriptive",
         "Phase-138 Graffiti Descriptive (spec 024 Stage 2(d))",
         "Phase-138 (spec 024, FROZEN Stage 2(d)): descriptive "
         "protocol only for the catalogue Graffiti population "
         "(Phase-124 CISI Vols. 1–2 rows, object_type exactly "
         "'Graffiti') — rows/objects by volume, distinct objects "
         "by catalogue site, rows-per-object distribution, "
         "side/bis and motif_chapter (Class C) values as printed, "
         "caption_ocr_score / scale_pct median + IQR, and a "
         "catalogue-composition context table for Seals and "
         "Tablets. No test, no p-value, no inference; not a "
         "Stage 2 family member; graffiti never pooled with seal "
         "or tablet texts. Recomputes from the local store when "
         "present and otherwise serves the committed results "
         "JSON. CPU."),
    ]
    nodes = []
    for nid, name, desc in specs:
        def fn(i, p):
            return {**_run_descriptive(), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
