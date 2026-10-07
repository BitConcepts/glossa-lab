"""Phase-111 orchestrator (spec 009 section 14).

Stages:
  gate      — build the panel (custodian), evaluate the validation
              gate (analyst) on known corpora only. If the gate
              fails, the study stops here: INCONCLUSIVE.
  classify  — only if the gate passed: train the final model,
              classify the blind IDs, unblind (join with the
              custodian key — the unblinding event is recorded),
              compute the verdict strictly per spec section 9.

Writes reports/phase111_blind_affiliation_results.json.

AI disclosure: written by an AI agent (Muse Spark) at the direction
of Tristen Pierson, per constitution section VI.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from glossa_lab import phase111_analyst as analyst
from glossa_lab import phase111_custodian as custodian

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_PATH = REPO_ROOT / "reports" / "phase111_blind_affiliation_results.json"
STATE_DIR = custodian.STATE_DIR


def _code_hash() -> dict:
    files = ["phase111_custodian.py", "phase111_features.py",
             "phase111_analyst.py", "phase111_run.py"]
    base = Path(__file__).resolve().parent
    digests = {}
    for name in files:
        digests[name] = hashlib.sha256((base / name).read_bytes()).hexdigest()
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                              capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:  # noqa: BLE001
        head = "unknown"
    return {"git_head": head, "module_sha256": digests}


def _load_panel() -> dict:
    return json.loads((STATE_DIR / "panel.json").read_text(encoding="utf-8"))


def _write_results(results: dict) -> None:
    RESULTS_PATH.write_text(json.dumps(results, indent=1), encoding="utf-8")


def run_gate_stage(rebuild: bool = False) -> dict:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if rebuild or not (STATE_DIR / "panel.json").exists():
        build_log = custodian.build_panel()
    else:
        build_log = json.loads((STATE_DIR / "build_log.json").read_text(encoding="utf-8"))
    panel = _load_panel()
    gate = analyst.evaluate_gate(panel)
    results = {
        "spec": "009-phase111-blind-affiliation",
        "phase": "Phase-111",
        "run_started_utc": datetime.now(timezone.utc).isoformat(),
        "code_hash": _code_hash(),
        "panel_build_log": build_log,
        "gate": gate,
        "verdict": None if gate["gate_passed"] else "INCONCLUSIVE — GATE FAILED",
        "status": "gate_passed" if gate["gate_passed"] else "stopped_at_gate",
    }
    _write_results(results)
    return results


def run_classify_stage() -> dict:
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    if results.get("status") != "gate_passed":
        raise RuntimeError("classify stage requires a passed gate")
    panel = _load_panel()
    model, classes = analyst.train_final_model(panel)
    post_blind = analyst.classify_blind(panel, model)
    post_known = analyst.known_posteriors(panel, model)

    # Save raw posteriors in runtime state (audit trail).
    np.savez(STATE_DIR / "posteriors.npz",
             **{f"blind::{cid}": p for cid, p in post_blind.items()},
             **{f"known::{cid}": p for cid, p in post_known.items()},
             classes=np.array(classes))

    # ---- Unblinding event ----
    key = json.loads((STATE_DIR / "key.json").read_text(encoding="utf-8"))
    unblind_time = datetime.now(timezone.utc).isoformat()
    roles = {cid: key[cid]["code"] for cid in panel["blind_ids"]}
    known_labels = {cid: panel["members"][cid]["label"] for cid in panel["known_ids"]}

    verdict = analyst.compute_verdict(post_blind, classes, roles,
                                      post_known, known_labels)

    # ---- T5 exceedance (needs winner/runner-up from the verdict) ----
    pvals = analyst.exceedance_p_values(post_blind, classes, roles, results["gate"])
    fam = verdict.get("family")
    if fam and "winner" in fam:
        col = {c: i for i, c in enumerate(classes)}
        winner, runner = fam["winner"], fam["runner_up"]
        comp_posts = []
        for cid, lab in known_labels.items():
            if lab == runner:
                comp_posts.append(post_known[cid][:, col[winner]])
        comp = np.concatenate(comp_posts) if comp_posts else np.array([])
        indus_med = fam["pooled_median_family_posteriors"][winner]
        if len(comp):
            pvals["T5_family_margin"] = float(
                (1 + int(np.sum(comp >= indus_med))) / (1 + len(comp)))
    bh = analyst.benjamini_hochberg(pvals, q=0.05)

    # ---- Sensitivity (cannot upgrade the verdict; spec section 2) ----
    sensitivity: dict[str, dict] = {}
    col = {c: i for i, c in enumerate(classes)}
    fam_cols = [col[f] for f in analyst.FAMILIES if f in col]
    for cid in panel["blind_ids"]:
        code = roles[cid]
        if not code.startswith("R"):
            continue
        sensitivity[code] = {}
        for size_label in ("sens_5000", "sens_19600"):
            X = np.array(panel["members"][cid][f"features_{size_label}"], dtype=float)
            post = model.posterior(X)
            med_fam = {f: float(np.median(post[:, col[f]])) for f in analyst.FAMILIES}
            sensitivity[code][size_label] = {
                "median_linguistic_posterior": float(np.median(post[:, fam_cols].sum(axis=1))),
                "winner_family": max(med_fam, key=med_fam.get),
                "median_family_posteriors": med_fam,
            }

    results["unblinding"] = {
        "unblinded_utc": unblind_time,
        "key": {cid: key[cid] for cid in panel["blind_ids"]},
    }
    results["verdict"] = verdict["verdict"]
    results["verdict_detail"] = {
        k: v for k, v in verdict.items() if k != "verdict"}
    results["exceedance_p_values"] = pvals
    results["benjamini_hochberg"] = bh
    results["sensitivity"] = sensitivity
    results["status"] = "classified"
    _write_results(results)
    return results


if __name__ == "__main__":
    import sys

    stage = sys.argv[1] if len(sys.argv) > 1 else "gate"
    if stage == "gate":
        out = run_gate_stage(rebuild="--rebuild" in sys.argv)
        print(json.dumps({"gate_passed": out["gate"]["gate_passed"],
                          "verdict": out["verdict"]}, indent=1))
    elif stage == "classify":
        out = run_classify_stage()
        print(json.dumps({"verdict": out["verdict"]}, indent=1))
    else:
        raise SystemExit(f"unknown stage {stage!r}")
