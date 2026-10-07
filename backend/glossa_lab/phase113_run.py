"""Phase-113 orchestrator (spec 012 sections 7-11, 15).

Stages:
  rounds    — build (or load) the panel, then for r = 1..3: evaluate
              the round's validation gate on the ladder step L_r
              (stop: INCONCLUSIVE — GATE FAILED), freeze the round's
              final model C_r, run the custodian-side adversarial
              search (200 evaluations; the orchestrator mediates —
              feature matrices in, scalar objective + the constraint
              report out), build the round artifact A_r from a search-
              free seed, and check round control validity under C_r
              (stop: INVALID RUN — CONTROL VALIDITY FAILED).
  classify  — only if all three rounds hold: retrain C_3, classify
              every blind ID, re-check A1-A3 from their stored L3
              matrices, unblind (the event is recorded), and compute
              the verdict strictly per spec section 10.

Writes reports/phase113_blind_affiliation_results.json. Runtime
state lives under .glossa-state/phase113/ (panel, checkpoints,
optimizer traces, round artifacts, posteriors.npz).

Re-running the rounds stage after a crash restarts each unfinished
round's search from candidate 0 — determinism makes this safe: the
frozen seed streams reproduce the identical search. (Completed
rounds are recomputed too; their artifacts are rewritten with
identical content.)

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

from glossa_lab import phase113_analyst as analyst
from glossa_lab import phase113_custodian as custodian

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_PATH = REPO_ROOT / "reports" / "phase113_blind_affiliation_results.json"
STATE_DIR = custodian.STATE_DIR
LADDERS = [custodian.LADDER_L1, custodian.LADDER_L2, custodian.LADDER_L3]

ENVIRONMENT_NOTE = (
    "BLAS thread pinning (OMP_NUM_THREADS / OPENBLAS_NUM_THREADS / "
    "MKL_NUM_THREADS = 1) is set by the entry script's environment "
    "before this module is imported."
)


def _code_hash() -> dict:
    files = ["phase113_custodian.py", "phase113_features.py",
             "phase113_analyst.py", "phase113_run.py",
             "phase112_custodian.py", "phase112_analyst.py",
             "phase112_features.py"]
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


def _code_head() -> str:
    return _code_hash()["git_head"]


def _load_results() -> dict:
    return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))


def _write_results(results: dict) -> None:
    RESULTS_PATH.write_text(json.dumps(results, indent=1), encoding="utf-8")


def load_or_build_panel():
    """(panel, key, build_log) from state, building the panel first
    if panel.json does not exist (the custodian persists all three)."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if (STATE_DIR / "panel.json").exists():
        panel = json.loads((STATE_DIR / "panel.json").read_text(encoding="utf-8"))
        key = json.loads((STATE_DIR / "key.json").read_text(encoding="utf-8"))
        build_log = json.loads((STATE_DIR / "build_log.json").read_text(encoding="utf-8"))
        return panel, key, build_log
    build_log = custodian.build_panel()
    panel = json.loads((STATE_DIR / "panel.json").read_text(encoding="utf-8"))
    key = json.loads((STATE_DIR / "key.json").read_text(encoding="utf-8"))
    return panel, key, build_log


def _load_panel() -> dict:
    return json.loads((STATE_DIR / "panel.json").read_text(encoding="utf-8"))


def _extract_job(draw: list[list[int]], draw_index: int) -> list[float]:
    return custodian.extract_ladder_features(draw, draw_index=draw_index)


def _extract_rows(draws: list[list[list[int]]]) -> list[list[float]]:
    """L3 feature rows for draws, via a Pool(2) where practical.
    Extraction is per-draw deterministic, so pooling cannot change
    the values."""
    if len(draws) <= 2:
        return [_extract_job(d, i) for i, d in enumerate(draws)]
    from multiprocessing import Pool

    with Pool(2) as pool:
        return pool.starmap(_extract_job, [(d, i) for i, d in enumerate(draws)])


def _slice_rows(rows_l3: list[list[float]], feature_names: list[str]) -> np.ndarray:
    idx = [custodian.LADDER_L3.index(name) for name in feature_names]
    return np.array(rows_l3, dtype=np.float64)[:, idx]


def _base_results(build_log: dict) -> dict:
    code = _code_hash()
    return {
        "spec": "012-phase113-blind-affiliation",
        "phase": "Phase-113",
        "study": "Phase-113 blind language-affiliation study (adversarial protocol)",
        "run_started_utc": datetime.now(timezone.utc).isoformat(),
        "code_head": code["git_head"],
        "code_hash": code,
        "environment": ENVIRONMENT_NOTE,
        "panel_build_log": build_log,
        "feature_names": custodian.LADDER_L3,
        "gate": None,
        "gates": {},
        "rounds": {},
        "final_control_validity": None,
        "verdict": None,
        "failing_controls": [],
        "family_posterior_medians": None,
        "margins": None,
        "exceedance_tests": None,
        "exceedance_p_values": None,
        "multiplicity": None,
        "benjamini_hochberg": None,
        "unblinding": None,
        "stop_stage": None,
        "status": "rounds_running",
    }


def _trace_summary(trace: list[dict]) -> dict:
    random_block = [rec for rec in trace if rec["eval_index"] < 120]
    refine_block = [rec for rec in trace if rec["eval_index"] >= 120]
    winner = max(trace, key=lambda rec: custodian.rank_key(
        rec["feasible"], rec["n_violations"], rec["objective"], rec["eval_index"]))
    return {
        "n_evaluations": len(trace),
        "n_feasible": int(sum(1 for rec in trace if rec["feasible"])),
        "best_objective_random_block": (
            max(rec["objective"] for rec in random_block) if random_block else None),
        "best_objective_refinement_block": (
            max(rec["objective"] for rec in refine_block) if refine_block else None),
        "winner_eval_index": winner["eval_index"],
        "winner_objective": winner["objective"],
        "winner_feasible": winner["feasible"],
        "winner_detail": winner["detail"],
    }


def stage_rounds() -> dict:
    panel, key, build_log = load_or_build_panel()
    results = _base_results(build_log)
    gates: dict[str, dict] = {}
    rounds_detail: dict[str, dict] = {}
    results["gates"] = gates
    results["rounds"] = rounds_detail

    # Custodian-side adversary, built once from R1 in the panel's
    # int mapping. R1's blind ID is resolved custodian-side; only
    # feature matrices and scalars cross to the analyst path.
    r1_int = custodian.r1_texts_int()
    advgen = custodian.AdvGen(r1_int)
    r1_cid = next(cid for cid, entry in key.items()
                  if entry["code"] == custodian.R1_CODE)
    r1_primary_rows = np.array(panel["members"][r1_cid]["features_primary"],
                               dtype=np.float64)

    for r in (1, 2, 3):
        ladder = LADDERS[r - 1]
        gate = analyst.evaluate_gate_ladder(panel, ladder)
        gates[f"round{r}"] = gate
        if not gate["gate_passed"]:
            rounds_detail[str(r)] = {"gate": gate}
            results["gate"] = gates["round1"]
            results["verdict"] = "INCONCLUSIVE — GATE FAILED"
            results["stop_stage"] = "rounds_gate"
            results["status"] = "stopped_at_rounds_gate"
            results["invalid_at_round"] = r
            _write_results(results)
            return results

        model = analyst.train_final_model(panel, ladder)
        classes = list(model.classes_)
        col = {c: i for i, c in enumerate(classes)}
        fam_cols = [col[f] for f in analyst.FAMILIES if f in col]

        # R1 percentile intervals for the round >= 2 matching
        # constraint: per L_{r-1} feature, R1's [10%, 90%] over its
        # 100 primary panel draws (panel data, custodian-computed).
        prev_ladder = LADDERS[r - 2] if r >= 2 else None
        prev_intervals: dict[str, tuple[float, float]] = {}
        if prev_ladder is not None:
            prev_idx = [custodian.LADDER_L3.index(n) for n in prev_ladder]
            prev_rows = r1_primary_rows[:, prev_idx]
            lo, hi = np.percentile(prev_rows, [10, 90], axis=0)
            prev_intervals = {name: (float(lo[i]), float(hi[i]))
                              for i, name in enumerate(prev_ladder)}

        def eval_fn(theta, eval_index, _r=r, _model=model, _ladder=ladder,
                    _fam_cols=fam_cols, _prev_ladder=prev_ladder,
                    _prev_intervals=prev_intervals):
            # Generation happens once: raw texts in R1's token space
            # (for the unigram constraint) are remapped at 40 + r for
            # draw construction, exactly as adversarial_texts does.
            raw = custodian.generated_texts(theta, _r, eval_index, advgen)
            texts = custodian.remap_texts(raw, 40 + _r)
            draws = custodian.primary_draws(texts, 40 + _r, 16)
            rows_l3 = _extract_rows(draws)
            post = _model.posterior(_slice_rows(rows_l3, _ladder))
            objective = float(np.mean(post[:, _fam_cols].sum(axis=1)))
            if _r == 1:
                tv = custodian.unigram_tv(raw, r1_int)
                feasible = bool(tv <= 0.05)
                return objective, feasible, 0 if feasible else 1, {
                    "unigram_tv": float(tv)}
            rows_prev = _slice_rows(rows_l3, _prev_ladder)
            medians_arr = np.median(rows_prev, axis=0)
            medians: dict[str, float] = {}
            violated: list[str] = []
            for i, name in enumerate(_prev_ladder):
                med = float(medians_arr[i])
                medians[name] = med
                q10, q90 = _prev_intervals[name]
                if med < q10 or med > q90:
                    violated.append(name)
            return objective, not violated, len(violated), {
                "violated_features": violated, "medians": medians}

        trace_path = STATE_DIR / f"optimizer_trace_round{r}.jsonl"
        theta_star, trace = custodian.run_search(r, eval_fn, trace_path)
        summary = _trace_summary(trace)

        # Round artifact A_r: a seed stream never used in search.
        raw_star = custodian.generated_texts(theta_star, r, 999, advgen)
        texts_star = custodian.remap_texts(raw_star, 40 + r)
        draws100 = custodian.primary_draws(texts_star, 40 + r, 100)
        rows_star_l3 = _extract_rows(draws100)
        post_r = model.posterior(_slice_rows(rows_star_l3, ladder))
        share_r = analyst.control_share(post_r, classes)
        corpus_stats = {
            "texts": len(raw_star),
            "tokens": int(sum(len(t) for t in raw_star)),
            "unigram_tv_to_R1": float(custodian.unigram_tv(raw_star, r1_int)),
        }
        artifact = {
            "round": r,
            "theta_star": custodian.theta_to_dict(theta_star),
            "theta_star_list": [float(v) for v in theta_star],
            "trace_summary": summary,
            "corpus_stats": corpus_stats,
            "control_share": share_r,
            "classifier_feature_names": ladder,
            "model_classes": classes,
        }
        (STATE_DIR / f"adversarial_round{r}.json").write_text(
            json.dumps(artifact, indent=1), encoding="utf-8")
        (STATE_DIR / f"adversarial_round{r}_matrix.json").write_text(
            json.dumps({"feature_names": custodian.LADDER_L3,
                        "rows": rows_star_l3}), encoding="utf-8")

        rounds_detail[str(r)] = {
            "gate": gate,
            "theta_star": custodian.theta_to_dict(theta_star),
            "theta_star_list": [float(v) for v in theta_star],
            "trace_summary": summary,
            "corpus_stats": corpus_stats,
            "control_share_under_C_r": share_r,
        }
        results["gate"] = gates["round1"]
        if share_r < 0.95:
            results["verdict"] = "INVALID RUN — CONTROL VALIDITY FAILED"
            results["invalid_at_round"] = r
            results["failing_controls"] = [f"A{r}"]
            results["stop_stage"] = "rounds_control"
            results["status"] = "stopped_at_rounds_control"
            _write_results(results)
            return results

    results["status"] = "rounds_complete"
    results["stop_stage"] = None
    results["verdict"] = None
    _write_results(results)
    print("ROUNDS COMPLETE")
    return results


def stage_classify() -> dict:
    if not RESULTS_PATH.exists():
        raise RuntimeError(
            "classify stage requires the rounds stage results file "
            f"({RESULTS_PATH}); run the rounds stage first")
    results = _load_results()
    if results.get("verdict") is not None:
        raise RuntimeError(
            "classify stage cannot run: the rounds stage stopped with "
            f"verdict {results.get('verdict')!r} "
            f"(stop_stage={results.get('stop_stage')!r})")
    rounds_done = results.get("rounds") or {}
    if results.get("status") != "rounds_complete" or not {"1", "2", "3"} <= set(rounds_done):
        raise RuntimeError(
            "classify stage requires all three rounds complete "
            f"(status={results.get('status')!r}, rounds present: "
            f"{sorted(rounds_done)}); run the rounds stage first")

    panel, key, _build_log = load_or_build_panel()
    model = analyst.train_final_model(panel, custodian.LADDER_L3)
    classes = list(model.classes_)
    post_blind = analyst.classify_blind(panel, model, custodian.LADDER_L3)
    post_known = analyst.known_posteriors(panel, model, custodian.LADDER_L3)

    # Posteriors at every assembled size (audit trail): primary for
    # all members, sensitivity sizes for known / nonling / target.
    npz_payload: dict[str, np.ndarray] = {
        **{f"blind::{cid}": p for cid, p in post_blind.items()},
        **{f"known::{cid}": p for cid, p in post_known.items()},
        "classes": np.array(classes),
    }
    sensitivity_posts: dict[str, dict[str, np.ndarray]] = {}
    for size_label in ("sens_5000", "sens_19600"):
        posts_at_size = analyst.known_posteriors(
            panel, model, custodian.LADDER_L3, size_label)
        posts_at_size.update(analyst.classify_blind(
            panel, model, custodian.LADDER_L3, size_label))
        for cid, entry in key.items():
            if entry["role"] not in ("known", "nonling", "target"):
                continue
            if cid not in posts_at_size:
                continue
            if f"features_{size_label}" not in panel["members"][cid]:
                continue
            npz_payload[f"sens::{cid}::{size_label}"] = posts_at_size[cid]
            sensitivity_posts.setdefault(cid, {})[size_label] = posts_at_size[cid]
    np.savez(STATE_DIR / "posteriors.npz", **npz_payload)

    # ---- Unblinding event ----
    unblind_time = datetime.now(timezone.utc).isoformat()
    roles = {cid: key[cid]["code"] for cid in panel["blind_ids"]}
    known_labels = {cid: panel["members"][cid]["label"] for cid in panel["known_ids"]}

    # ---- Final control validity (section 8.4): A_r re-checked ----
    # under C_3 from their stored L3 matrices; S1-S5 shares are
    # computed inside compute_verdict from the blind posteriors.
    adv_shares: dict[str, float] = {}
    for r in (1, 2, 3):
        matrix = json.loads((STATE_DIR / f"adversarial_round{r}_matrix.json")
                            .read_text(encoding="utf-8"))
        rows = np.array(matrix["rows"], dtype=np.float64)
        adv_shares[f"A{r}"] = analyst.control_share(model.posterior(rows), classes)

    verdict = analyst.compute_verdict(post_blind, classes, roles,
                                      post_known, known_labels,
                                      control_shares_extra=adv_shares)

    # ---- Multiplicity (section 11): T1/T2 are the round-1 gate ----
    # instances (primary); T3/T4 exceedance; T5 family margin.
    gate_round1 = (results.get("gates") or {}).get("round1") or results.get("gate")
    pvals = analyst.exceedance_p_values(post_blind, classes, roles, gate_round1)
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
            post = sensitivity_posts.get(cid, {}).get(size_label)
            if post is None:
                continue
            med_fam = {f: float(np.median(post[:, col[f]])) for f in analyst.FAMILIES}
            sensitivity[code][size_label] = {
                "median_linguistic_posterior": float(
                    np.median(post[:, fam_cols].sum(axis=1))),
                "winner_family": max(med_fam, key=med_fam.get),
                "median_family_posteriors": med_fam,
            }

    results["unblinding"] = {
        "unblinded_utc": unblind_time,
        "code_head": _code_head(),
        "key": {cid: key[cid] for cid in panel["blind_ids"]},
    }
    results["final_control_validity"] = verdict.get("control_validity_shares")
    results["verdict"] = verdict["verdict"]
    results["verdict_detail"] = {
        k: v for k, v in verdict.items() if k != "verdict"}
    results["failing_controls"] = verdict.get("failing_controls", [])
    replicates = verdict.get("replicates") or {}
    results["family_posterior_medians"] = {
        code: rep.get("median_family_posteriors")
        for code, rep in replicates.items()} or None
    results["margins"] = verdict.get("family")
    results["exceedance_tests"] = pvals
    results["exceedance_p_values"] = pvals
    results["multiplicity"] = bh
    results["benjamini_hochberg"] = bh
    results["sensitivity"] = sensitivity
    results["status"] = "classified"
    results["stop_stage"] = None
    _write_results(results)
    return results


# Phase-112-style aliases.
run_rounds_stage = stage_rounds
run_classify_stage = stage_classify


def main(argv=None) -> dict:
    import sys

    args = list(sys.argv[1:] if argv is None else argv)
    stage = args[0] if args else "rounds"
    if stage == "rounds":
        out = stage_rounds()
        print(json.dumps({"status": out["status"], "verdict": out["verdict"]}, indent=1))
        return out
    if stage == "classify":
        out = stage_classify()
        print(json.dumps({"verdict": out["verdict"]}, indent=1))
        return out
    raise SystemExit(f"unknown stage {stage!r}")


if __name__ == "__main__":
    main()
