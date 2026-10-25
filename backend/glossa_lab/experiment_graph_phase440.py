"""Experiment Graph Nodes: Phase 440 (Spec 074 —
Hunt opening signs on the repaired keying
surface: are Shakti's opening-strong signs the
animal signs, on Registry v2 / Asset A v2).

  IndusPhase440HuntOpeningSigns   Phase-440:
  the frozen Spec 074 contract executed in
  order — step-0 gates 0.1 to 0.6 fail-closed
  (0.1 the repaired surface asserted against
  Spec 073's executed record: both v2 freeze
  records present, both canonical files
  recomputing to the quoted digests, Asset A
  v2's per-kind counts matching — failure
  ASSET NOT FROZEN / ASSET PIN MISMATCH; 0.2
  the Shakti intake under P-F1 S1/S2 — failure
  SHAKTI INTAKE NOT REPRODUCED; 0.3 input
  integrity over the section 3 inputs —
  failure INVALID; 0.4 the section 2 battery
  over the documented-lineage primary, the
  opening-strong set enumerated in full in
  Wells space and published before any join,
  asserted to reproduce Spec 070's recorded
  31 signs and class census exactly — failure
  POPULATION NOT REPRODUCED — and every sign
  keyed to exactly one Asset A v2 row under
  the two-leg route of DD-074-8 (the
  parpola_1982 leg of DD-070-9 over Registry
  v2 first, then Registry v2's icit_wells leg;
  zero or multiple resolutions unkeyable) —
  an unkeyable sign closes POPULATION NOT
  KEYED under DD-074-10 (DD-070-11 carried);
  0.5 the comparison census: U, every sign
  with at least 30 occurrences under the
  counting rule carried from DD-070-10, the
  S-B unicorn naming from the frozen asset's
  verbatim labels, every O and U sign shown
  to carry an Asset A v2 row — failure
  INVALID; 0.6 the freeze-order proof), then
  the one join and the section 4 test: R1,
  the animal share of the opening-strong set
  over the animal share of the inventory,
  Fisher's exact test on the disjoint 2x2
  (the one-sided p the criterion, the
  two-sided p published), the reversed arm
  R2, the section 4.3 precedence (NOT
  SUPPORTED if R1 <= 1.0 or p >= 0.05;
  SUPPORTED if R1 >= 1.5, p < 0.05 and
  R2 > 1.0; otherwise INCONCLUSIVE), and the
  three pre-registered sensitivities (S-A
  contested included, S-B the unicorn
  removed, S-C the corroborated population
  re-derived), scored only in the frozen
  section 4.6 wordings as re-pointed by
  Spec 074. The verdict is a verdict on the
  re-scoped test — a positional framework
  measured on the graded ICIT corpus, not
  the Phase-43 framework. Spec 070's closure
  stands unamended.

The node serves the phase's committed results
JSON (reports/phase440_results.json),
recomputing via the phase script when that
script's pinned inputs are present locally.
Freeze: specs/074-hunt-opening-signs-repaired-surface/
freeze.md (digest 5416a0d3...); the frozen
spec's contract registration is OSF
https://osf.io/cfe7z/.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _serve(script_name: str, results_name: str) -> dict:
    script = _SCRIPTS / script_name
    results = _REPO / "reports" / results_name
    if script.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script), "run"],
                capture_output=True, text=True, timeout=1200,
                cwd=str(_REPO))
            if r.returncode == 0 and results.exists():
                return {"source": "script_recomputed",
                        **json.loads(results.read_text("utf-8"))}
        except Exception:  # noqa: BLE001
            pass
    if results.exists():
        return {"source": "committed_results",
                **json.loads(results.read_text("utf-8"))}
    return {"error": f"{results_name} not found"}


_NODE_SPECS = [
    ("IndusPhase440HuntOpeningSigns",
     "phase440_hunt_opening_signs.py",
     "phase440_results.json",
     "Phase-440 Hunt opening signs on the repaired surface (spec 074)",
     "Phase-440 (spec 074): execution of the frozen "
     "Spec 074 contract — Spec 070's question (are "
     "Shakti's opening-strong signs the animal "
     "signs?) re-asked on the surface Spec 073 "
     "repaired. Step-0 gates in the section 5 "
     "order, fail-closed: 0.1 the repaired surface "
     "asserted against Spec 073's executed record "
     "(Registry v2 at 42ab09fb..., Asset A v2 at "
     "681e017d..., per-kind animal 30 / sky_cycle "
     "0 / object_goods 22 / human 43 / other 246 / "
     "contested 0 / unidentified 211 — failure "
     "ASSET NOT FROZEN or ASSET PIN MISMATCH); 0.2 "
     "the Shakti intake under P-F1 S1/S2 (corpus "
     "345241b1..., row grades 02394241...; census "
     "5,704 rows, 5,536 analyzable, grades "
     "3,212/2,087/405, 4,904 CISI-carrying — "
     "failure SHAKTI INTAKE NOT REPRODUCED); 0.3 "
     "input integrity (the Phase-433 record at "
     "667560a5..., Registry v1 at 8a0b2a82..., the "
     "crosswalk at 4ace1a61..., the anchors at "
     "df0cf620..., this spec's freeze digest "
     "5416a0d3... — failure INVALID); 0.4 the "
     "section 2 battery over the documented-"
     "lineage primary (sequences of length >= 2; "
     "I/M/T by position; floor total >= 5; the "
     "Phase-43 cascade, threshold-only, no chance "
     "baseline), the opening-strong set "
     "enumerated in full in Wells space and "
     "published before any join, asserted to "
     "reproduce Spec 070's recorded enumeration "
     "exactly (31 signs, per-sign I/M/T; class "
     "census 220 at the floor: TERMINAL_STRONG "
     "42, MEDIAL_STRONG 81, TERMINAL_MODERATE 37, "
     "INITIAL_MODERATE 6, MIXED 23, "
     "INITIAL_STRONG 31 — failure POPULATION NOT "
     "REPRODUCED), then keyed under the two-leg "
     "route of DD-074-8 (leg 1: the parpola_1982 "
     "rows' wells_ids over Registry v2; leg 2: "
     "Registry v2's icit_wells rows, the sign_id "
     "being the Wells id itself; zero or "
     "multiple resolutions unkeyable — an "
     "unkeyable sign closes POPULATION NOT KEYED "
     "under DD-074-10); 0.5 the comparison "
     "census: U (total >= 30 under DD-070-10's "
     "counting rule), the S-B unicorn naming "
     "from Asset A v2's verbatim labels, every O "
     "and U sign carrying an Asset A v2 row "
     "(failure INVALID); 0.6 the freeze-order "
     "proof. Then the join and the section 4 "
     "test over Asset A v2 (depicted_kind = "
     "animal is the animal set; contested and "
     "unidentified members counted, listed, and "
     "excluded from the primary's numerator and "
     "denominator — the five formerly unkeyable "
     "signs among them, classified unidentified: "
     "keying is not classification): R1 with "
     "Fisher's exact test on the disjoint 2x2, "
     "the reversed arm R2, the section 4.3 "
     "precedence, sensitivities S-A / S-B / "
     "S-C, verdicts only in the frozen section "
     "4.6 wordings. The claim stands IN "
     "QUESTION (partially supported, positional "
     "half only) as recorded; Spec 070's "
     "POPULATION NOT KEYED closure stands "
     "unamended. Outcome as recorded in "
     "reports/phase440_results.json. CPU."),
]


def _phase440_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    nodes = []
    for nid, script_name, results_name, name, desc in _NODE_SPECS:
        def fn(i, p, _s=script_name, _r=results_name):
            return {**_serve(_s, _r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
