"""Experiment Graph Nodes: Phase-107 (spec 005) — Phase-52 v2.

Ledger-sequence Phase-107 (2026-10-05): held-out SA validation, blind
controls, constraint ablation, delta-scaled run, corpus pooling,
metrology check. Node IDs are distinct from the legacy
``IndusTBNameCheck`` node (an earlier era's Phase-107 label, preserved
untouched in experiment_graph_phase104_109.py).

  IndusSAHeldOutValidation  Step 1: k-fold held-out + blind controls
  IndusSAConstraintAblation Step 2: phono/harmony/positional ablation
  IndusSAScaledDeltaRun     Step 3: delta equivalence + scaled run
  IndusSACorpusLayerBuild   Step 4a: build converted corpus layers
  IndusSACorpusPool         Step 4: CISI pooling + headline re-run
  IndusSAMetrologyCheck     Step 5: stroke-numeral constraints C1-C3
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


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


def _phase107_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusSAHeldOutValidation", "SA Held-Out Validation + Blind Controls",
         "phase107_sa_validation.py", ["step1"], "phase107_step1_validation.json",
         "Phase-107 Step 1 (spec 005): 5-fold held-out anchor CV of the Phase-52 SA objective, pin-count sweep, blind controls (Sanskrit, Ge'ez, scrambled). CPU."),
        ("IndusSAConstraintAblation", "SA Constraint Ablation",
         "phase107_sa_validation.py", ["step2"], "phase107_step2_ablation.json",
         "Phase-107 Step 2 (spec 005): one-at-a-time ablation of Phase-58/61 phonotactic, Phase-61 vowel-harmony and Phase-133 positional-grammar terms in the SA objective; pre-registered keep rule. CPU."),
        ("IndusSAScaledDeltaRun", "SA Delta-Scored Scaled Run",
         "phase107_sa_validation.py", ["step3"], "phase107_step3_scaled.json",
         "Phase-107 Step 3 (spec 005): delta-scoring equivalence test, then 10x10x100K scaled run with stability selection; writes the Phase-107 decipherment table. CPU."),
        ("IndusSACorpusPool", "SA Corpus Pooling (CISI via Crosswalk)",
         "phase107_corpus_pool.py", [], "phase107_step4_pooling.json",
         "Phase-107 Step 4 (spec 005): convert in-repo CISI subset via M<->P crosswalk v2.1, dedupe vs Holdat, pool, re-run primary held-out metric. CPU."),
        ("IndusSAMetrologyCheck", "Stroke-Numeral Metrology Check",
         "phase107_metrology_check.py", [], "phase107_step5_metrology.json",
         "Phase-107 Step 5 (spec 005): validate the strengthened SA on the additive stroke-numeral subsystem M086-M092 (constraints C1-C3). CPU."),
    ]
    nodes = []
    for nid, name, script, args, report, desc in specs:
        def fn(i, p, s=script, a=args, r=report):
            return {**_run(s, a, r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}}, fn=fn))

    def _layer_build_fn(i, p):
        # Step 4a data-prep: writes corpora/downloads/icit_fieldcady/
        # icit_converted.json + corpora/downloads/layer_build_meta.json
        # (gitignored layer outputs, not a reports/ artifact).
        s = _SCRIPTS / "phase107_build_layers.py"
        if not s.exists():
            return {"error": f"Not found: {s.name}"}
        try:
            r = subprocess.run([sys.executable, str(s)], capture_output=True,
                               text=True, timeout=1800, cwd=str(_REPO))
            if r.returncode != 0:
                return {"error": f"exit {r.returncode}", "stderr": r.stderr[-400:]}
        except subprocess.TimeoutExpired:
            return {"error": "timeout 1800s"}
        except Exception as e:  # noqa: BLE001
            return {"error": str(e)}
        meta = _REPO / "corpora" / "downloads" / "layer_build_meta.json"
        out = {"ok": True}
        if meta.exists():
            try:
                out["layer_build_meta"] = json.loads(meta.read_text("utf-8"))
            except Exception:  # noqa: BLE001
                pass
        return {**out, "gpu_device": _get_device()}

    nodes.append(AtomicNodeDef(
        id="IndusSACorpusLayerBuild", name="SA Corpus Layer Build (ICIT -> M)",
        category="Indus Decipherment",
        description="Phase-107 Step 4a (spec 005): convert the ICIT/Lipi export "
                    "(Wells numbers) to a Mahadevan M-sign layer under "
                    "corpora/downloads/ (gitignored), deduped vs Holdat; "
                    "writes layer_build_meta.json. CPU.",
        inputs=[],
        outputs=[{"name": "result", "type": "json"},
                 {"name": "gpu_device", "type": "text"}],
        params_schema={"type": "object", "properties": {}}, fn=_layer_build_fn))
    return nodes
