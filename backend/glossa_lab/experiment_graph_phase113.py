"""Experiment Graph Nodes: Phase-113 (spec 012) — blind language-affiliation study, adversarial protocol.

Ledger-sequence Phase-113 (2026-10-07): successor to the
Phase-112 blind study (spec 010), whose gate passed and whose
fixed traps S1-S4 were rejected in every draw, but whose run was
invalidated by S5, the positional-bigram template. Spec 012
replaces fixed traps with an adversarial protocol: a frozen
feature ladder (L1/L2/L3), a budgeted deterministic optimizer
searching a parametric generator family against each round's
frozen classifier, and round control validity at every step
before any section 10 verdict may fire.

  IndusPhase113BlindRounds    per-round gates + adversarial rounds (stop rules)
  IndusPhase113BlindClassify  final classification + verdict (depends on
                              IndusPhase113BlindRounds completing with all
                              three rounds held; enforced by the stage guard
                              in phase113_run.stage_classify, since node
                              definitions carry no depends_on field)
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
            data = json.loads(rp.read_text("utf-8"))
            return {"result": data, "detail": data.get("verdict") or "rounds complete"}
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


def _phase113_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase113BlindRounds", "Phase-113 Blind Affiliation: Adversarial Rounds",
         "phase113_blind_rounds.py", [], "phase113_blind_affiliation_results.json",
         "Phase-113 stage 1 (spec 012): custodian builds the blinded, "
         "size-matched panel (Phase-112 panel plus the frozen L1/L2/L3 "
         "feature ladder); for each round r = 1..3 the analyst evaluates "
         "the frozen validation gate on L_r, the round classifier C_r is "
         "frozen, a deterministic 200-evaluation custodian-side optimizer "
         "searches the adversarial generator family against C_r, and the "
         "round artifact A_r must classify non-linguistic in >= 95% of "
         "draws. Gate failure stops as INCONCLUSIVE; a round control "
         "failure stops as INVALID RUN. CPU."),
        ("IndusPhase113BlindClassify", "Phase-113 Blind Affiliation: Classify + Verdict",
         "phase113_blind_classify.py", [], "phase113_blind_affiliation_results.json",
         "Phase-113 stage 2 (spec 012): depends on IndusPhase113BlindRounds "
         "— runs only if all three rounds held. Trains C_3 (L3 features, "
         "all known draws + generator classes), re-checks S1-S5 and A1-A3 "
         "control validity under C_3, classifies the blind IDs, unblinds "
         "(event logged), and computes the verdict strictly under the "
         "frozen support / refutation thresholds (posterior >= 0.90, "
         "BF >= 10, BF < 3 or TOST +/-0.05 = no discrimination). CPU."),
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
    return nodes
