"""Experiment Graph Nodes: Phase-137 (spec 024, Stage 2(c)) —
site repertoire differentiation.

Ledger-sequence Phase-137 (2026-10-09): test (c) under the
frozen Stage 2(c) record
(specs/024-evidence-integration/stage2c-freeze.md). Family
members F2 (Holdat compilation layer) and F3 (ICIT-lineage
layer, horus84) are tested SEPARATELY, never pooled: site x
sign profile tables, Pearson chi-square as a divergence
statistic only, inference by composition-controlled
permutation of site labels at inscription level within
composition strata (B = 9,999, seed 20261009). Raw p-values
only; verdict words are deferred to the combined Stage 2
report's Benjamini-Hochberg correction. This node exposes the
per-layer results summary only; the full results are the
committed reports/phase137_results.json and the report is
reports/phase137_report.md.

  IndusPhase137SiteRepertoire
      Stage 2(c) site repertoire results summary (F2 + F3)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_RESULTS = _REPO / "reports" / "phase137_results.json"
_MAIN = Path.home() / "workspace" / "glossa-lab"
_HOLDAT = (_MAIN / "corpora/downloads/external_repos"
           / "holdatllc_indus/indus_corpus 2.csv")
_HORUS = (Path.home() / "workspace" / "research_notes"
          / "indus-data-deep-sweep-20261008" / "downloads"
          / "horus84-computational-linguistics" / "data"
          / "inscriptions.csv")


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _layer_summary(layer: dict) -> dict:
    perm = layer.get("permutation") or {}
    return {
        "family_member": layer["family_member"],
        "headline_label": layer["headline_label"],
        "eligible_sites": layer["eligible_sites"],
        "table_dimensions": layer["table_dimensions"],
        "analysis_population": layer["analysis_population"],
        "observed_chi_square": layer["observed_chi_square"],
        "permutation_median": perm.get("permutation_median"),
        "permutation_p95": perm.get(
            "permutation_p95_nearest_rank"),
        "p_value_raw": layer["p_value_raw"],
        "cramers_v_descriptive":
            layer.get("cramers_v_descriptive"),
        "sparsity_disclosure":
            layer.get("sparsity_disclosure"),
        "estimability_outcome":
            layer["estimability_outcome"],
    }


def _summary(results: dict, source: str) -> dict:
    return {
        "source": source,
        "phase": results["phase"],
        "layers": {
            key: _layer_summary(layer)
            for key, layer in results["layers"].items()},
        "anchors_sha256": results["anchors_sha256"],
        "ai_disclosure": results["ai_disclosure"],
    }


def _run_results():
    """Recompute via the phase script when the local-store
    inputs are present; otherwise serve the committed results
    (the script's inputs are local-store files that never
    enter git)."""
    script = _SCRIPTS / "phase137_site_repertoire.py"
    if script.exists() and _HOLDAT.exists() and _HORUS.exists():
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
    return {"error": "phase137 results not found"}


def _phase137_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase137SiteRepertoire",
         "Phase-137 Site Repertoire Differentiation "
         "(spec 024 Stage 2(c))",
         "Phase-137 (spec 024, FROZEN Stage 2(c)): site "
         "repertoire differentiation — family members F2 "
         "(Holdat compilation layer) and F3 (ICIT-lineage "
         "layer, horus84) tested separately, never pooled; "
         "site x sign profile tables, Pearson chi-square "
         "as a divergence statistic only, composition-"
         "controlled permutation of site labels within "
         "strata (B = 9,999, seed 20261009), Cramer's V "
         "and per-site TV distances descriptive, raw "
         "p-values only (BH verdict deferred to the "
         "combined Stage 2 report). Recomputes from the "
         "local store when present and otherwise serves "
         "the committed results JSON. CPU."),
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
