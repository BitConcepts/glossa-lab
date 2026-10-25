"""Experiment Graph Nodes: Phase 441 (Spec 075 —
the depicted-kind endings atlas: for each kind of
thing the published sign identifications depict,
do that kind's signs gather at the ends of
inscriptions, on Registry v2 / Asset A v2).

  IndusPhase441DepictedKindEndingsAtlas
  Phase-441: the frozen Spec 075 contract
  executed in order — step-0 gates 0.1 to 0.6
  fail-closed (0.1 the asset pins asserted
  against Spec 073's executed record: both v2
  freeze records present, Asset A v2 and
  Registry v2 recomputing to the quoted digests
  with their row counts and Asset A v2's
  per-kind and dispute counts matching —
  failure ASSET NOT FROZEN / ASSET PIN
  MISMATCH; 0.2 the Shakti intake under P-F1
  S1/S2 — failure SHAKTI INTAKE NOT REPRODUCED;
  0.3 input integrity over the section 3 inputs
  (the crosswalk, Registry v1, the anchors) —
  failure INVALID; 0.4 the primary population
  (documented-lineage rows only, section 3's
  construction) reproduced as 3,045 analyzable
  rows / 557 distinct signs / 550 in sequences
  of length >= 2 — failure POPULATION NOT
  REPRODUCED — and every sign keyed to exactly
  one Asset A v2 row under the two-leg route of
  DD-075-5 (DD-074-8 carried: the parpola_1982
  rows' wells_ids over Registry v2 first, then
  Registry v2's icit_wells rows; zero or
  multiple resolutions unkeyable) — an
  unkeyable sign closes POPULATION NOT KEYED,
  token 999 excepted by name in advance as the
  named exclusion of section 4.3; 0.5 the
  census published before any rate, the floors
  of section 4.5 (20 member signs, 30 pooled
  occurrences) applied to it — a kind below a
  floor is TOO THIN in the census record; 0.6
  the freeze-order proof from the external
  records: the freeze digest recomputed, the
  freeze PR's merge state read from the repo
  record, the OSF registration read approved
  and public — failure INVALID), then the
  section 5 battery, per kind: the kind's
  pooled final-position rate against the pooled
  rate of its frequency-matched comparison
  class (the other identified kinds' signs in
  the kind's own member band; unidentified
  signs in no class and no comparison class,
  DD-075-4), Fisher's exact test (two-sided) on
  the pooled 2x2 at the 5% level, the
  half-of-occurrences condition against the
  corpus-wide final-position rate, per-sign
  tables published in full. Verdicts per kind
  under section 5.2's frozen bands (SUPPORTED
  at ratio >= 1.5 with significance and the
  half condition; NOT SUPPORTED at ratio
  <= 1.0, the falsifier's word; INCONCLUSIVE
  between; TOO THIN below a floor); four
  verdicts published together, no pooled
  verdict. The celestial class is
  pre-registered EMPTY (Asset A v2 sky_cycle
  0): reported first, never tested — Spec
  071's closing finding restated, its
  retirement untouched; this study's claim
  family (F075) is its own, not Spec 071's
  question and not Hunt's claims in any form.
  Sensitivities per kind beside the primary:
  S1 borderline removed, S2 contested included
  under CISI-governed labels (Asset A v2
  carries zero contested rows; S2 is reported
  as equal to the primary where it does), S3
  the documented + corroborated population
  recomputed, a verdict change reported as
  grade-sensitive.

The node serves the phase's committed results
JSON (reports/phase441_results.json),
recomputing via the phase script when that
script's pinned inputs are present locally.
Freeze: specs/075-depicted-kind-endings-atlas/
freeze.md (digest aa06726f...); the frozen
spec's contract registration is OSF
https://osf.io/jv74f/.
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
    ("IndusPhase441DepictedKindEndingsAtlas",
     "phase441_depicted_kind_endings_atlas.py",
     "phase441_results.json",
     "Phase-441 depicted-kind endings atlas (spec 075)",
     "Phase-441 (spec 075): execution of the frozen "
     "Spec 075 contract — for each kind the published "
     "identifications depict (other, human, animal, "
     "object_goods), do that kind's signs gather at "
     "inscription endings, on the graded Shakti corpus "
     "over the surface Spec 073 repaired. Step-0 gates "
     "in the section 6 order, fail-closed: 0.1 asset "
     "pins (Registry v2 at 42ab09fb..., 1,013 rows; "
     "Asset A v2 at 681e017d..., 552 rows; per-kind "
     "other 246 / unidentified 211 / human 43 / animal "
     "30 / object_goods 22 / sky_cycle 0; dispute none "
     "548 / borderline 4 / contested 0 — failure ASSET "
     "NOT FROZEN or ASSET PIN MISMATCH); 0.2 the Shakti "
     "intake under P-F1 S1/S2 (corpus 345241b1..., row "
     "grades 02394241...; 5,704 rows, 5,536 analyzable, "
     "grades 3,212/2,087/405 — failure SHAKTI INTAKE NOT "
     "REPRODUCED); 0.3 input integrity (the crosswalk "
     "at 4ace1a61..., Registry v1 at 8a0b2a82..., the "
     "anchors at df0cf620... — failure INVALID); 0.4 "
     "the primary population reproduced (3,045 "
     "analyzable rows, 557 distinct signs, 550 in "
     "sequences of length >= 2 — failure POPULATION NOT "
     "REPRODUCED; a replay/drift gate, as the spec "
     "flags) and keyed under the two-leg route of "
     "DD-075-5 (leg 1: the parpola_1982 rows' wells_ids "
     "over Registry v2; leg 2: Registry v2's icit_wells "
     "rows, the sign_id being the Wells id itself; zero "
     "or multiple resolutions unkeyable — failure "
     "POPULATION NOT KEYED; token 999 the named "
     "exclusion of section 4.3, counted, never classed); "
     "0.5 the census published before any rate, floors "
     "of 20 member signs / 30 pooled occurrences "
     "applied (a kind below a floor is TOO THIN in the "
     "census record); 0.6 the freeze-order proof from "
     "the external records (freeze digest aa06726f... "
     "recomputed; freeze PR #389 merged at fd9bd448 "
     "read from the repo record; OSF jv74f approved and "
     "public read from the OSF record — failure "
     "INVALID). Then the section 5 battery per kind "
     "(pooled final-position rate against the "
     "frequency-matched comparison class of the other "
     "identified kinds; Fisher exact two-sided at 5%; "
     "the half-of-occurrences condition against the "
     "corpus-wide rate; per-sign tables in full), the "
     "section 5.2 verdict bands, and sensitivities "
     "S1-S3 beside the primaries. The celestial arm is "
     "pre-registered EMPTY and reported first, never "
     "tested; Spec 071's retirement stands untouched; "
     "no pooled depicted-kinds verdict exists. Outcome "
     "as recorded in reports/phase441_results.json. "
     "CPU."),
]


def _phase441_node_defs():
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
