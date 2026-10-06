"""Phase-107: Phase-52 v2 — held-out validation, blind controls,
constraint ablation, delta-scaled run (spec 005, Steps 1–3).

Pre-registered protocol: specs/005-phase52-v2/spec.md. The harness
config is FIXED: 3 seeds x 5 restarts x 10,000 iterations (Step 3
equivalence + scaled run excepted), temp 1.0, cooling 0.9997.

GPU: BigramScorer is NumPy by design; torch guarded per H20 pattern.

Outputs: reports/phase107_step1_validation.json,
         reports/phase107_step2_ablation.json,
         reports/phase107_step3_scaled.json,
         reports/phase107_decipherment_table.json
Checkpoints (resume-safe): .glossa-state/phase107_checkpoints/
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).parents[2]
sys.path.insert(0, str(REPO / "backend"))

try:
    import torch

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    DEVICE = "cpu"
    print("[GPU] torch not available — CPU only (WARNING: H20 CPU path)")

from glossa_lab.pipelines import sa_validation as sv  # noqa: E402

REPORTS = REPO / "reports"
CKPT = REPO / ".glossa-state" / "phase107_checkpoints"
HARNESS = dict(seeds=(0, 1, 2), n_restarts=5, max_iter=10_000)
STEP1_OUT = REPORTS / "phase107_step1_validation.json"
STEP2_OUT = REPORTS / "phase107_step2_ablation.json"
STEP3_OUT = REPORTS / "phase107_step3_scaled.json"
TABLE_OUT = REPORTS / "phase107_decipherment_table.json"


# ── shared data ───────────────────────────────────────────────────────────

def base_data() -> dict:
    flat, insc = sv.load_holdat_corpus()
    anchors = sv.load_anchors()
    prob, vocab = sv.load_dravidian_lm()
    pins_full = sv.phase52_pins(vocab)
    gold_all = sv.extract_gold(anchors, vocab)
    folds = sv.make_folds(pins_full, anchors, k=5, seed=107)
    nonpinnable = sorted(s for s in gold_all if s not in pins_full)
    return {"flat": flat, "insc": insc, "anchors": anchors, "prob": prob,
            "vocab": vocab, "pins_full": pins_full, "gold_all": gold_all,
            "folds": folds, "nonpinnable": nonpinnable}


def lm_for(name: str, data: dict):
    if name == "dravidian":
        return data["prob"], data["vocab"]
    if name == "scrambled":
        return sv.scramble_lm(data["prob"], data["vocab"], seed=107)
    return sv.LM_LOADERS[name]()


# ── fold worker (process pool) ────────────────────────────────────────────

def _fold_task(task: dict) -> dict:
    data = base_data()
    flat, insc = data["flat"], data["insc"]
    prob, vocab = lm_for(task["lm"], data)
    logp = None
    if "positional" in task["terms"]:
        logp = sv.build_positional_logp(task["train_gold"], flat, insc, vocab)
    objective = sv.Objective(prob, flat, insc, terms=tuple(task["terms"]),
                             positional_logp=logp)
    null_mu, null_std = sv.estimate_null(objective, flat, prob, n=30, seed=42)
    t0 = time.perf_counter()
    res = sv.run_sa(objective, flat, prob, task["pins"], **HARNESS)
    elapsed = time.perf_counter() - t0
    mean_score = statistics.mean(r["score"] for r in res["seeds"])
    out = {
        "key": task["key"], "lm": task["lm"], "terms": task["terms"],
        "fold": task["fold"], "n_pins": len(task["pins"]),
        "seed_scores": [round(r["score"], 2) for r in res["seeds"]],
        "mean_score": round(mean_score, 2),
        "null_mean": round(null_mu, 2), "null_std": round(null_std, 2),
        "z": round((mean_score - null_mu) / null_std, 3),
        "elapsed_s": round(elapsed, 1),
        "primary": sv.agreement(res["consensus"], task["eval_gold"], task["held"]),
        "held_stability": round(statistics.mean(
            res["consensus_frac"].get(s, 0.0) for s in task["held"]), 4)
        if task["held"] else None,
    }
    out["primary"].pop("detail", None)
    # Addendum A decomposition: held-out rate on reachable-gold signs only
    reach = task.get("reachable")
    if reach is not None:
        reach_signs = [s for s in task["held"]
                       if task["eval_gold"].get(s) in reach]
        sub = sv.agreement(res["consensus"], task["eval_gold"], reach_signs)
        sub.pop("detail", None)
        out["primary_reachable"] = sub
    if task.get("secondary_signs"):
        sec = sv.agreement(res["consensus"], task["secondary_gold"],
                           task["secondary_signs"])
        sec.pop("detail", None)
        out["secondary"] = sec
    return out


def run_tasks(tasks: list[dict], step: str, force: bool = False) -> list[dict]:
    """Checkpointed parallel execution: one JSON per task key under
    .glossa-state/phase107_checkpoints/<step>/; existing checkpoints are
    reused unless --force."""
    ckdir = CKPT / step
    ckdir.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict] = {}
    todo = []
    for task in tasks:
        ck = ckdir / f"{task['key']}.json"
        if ck.exists() and not force:
            results[task["key"]] = json.loads(ck.read_text("utf-8"))
            print(f"  [ckpt] {task['key']}")
        else:
            todo.append(task)
    if todo:
        with ProcessPoolExecutor(max_workers=2) as ex:
            futs = {ex.submit(_fold_task, t): t for t in todo}
            for fut in as_completed(futs):
                r = fut.result()
                results[r["key"]] = r
                (ckdir / f"{r['key']}.json").write_text(
                    json.dumps(r, indent=1), "utf-8")
                prim = r["primary"]
                print(f"  [done] {r['key']}: z={r['z']} "
                      f"held-out={prim['n_agree']}/{prim['n_eval']} "
                      f"({r['elapsed_s']}s)", flush=True)
    return [results[t["key"]] for t in tasks]


def stats_of(rates: list[float]) -> dict:
    return {"mean": round(statistics.mean(rates), 4),
            "sd": round(statistics.stdev(rates), 4) if len(rates) > 1 else 0.0,
            "folds": [round(r, 4) for r in rates]}


def pooled_sd(a: dict, b: dict) -> float:
    return ((a["sd"] ** 2 + b["sd"] ** 2) / 2) ** 0.5


# ── Step 1 ────────────────────────────────────────────────────────────────

def step1(force: bool = False) -> dict:
    data = base_data()
    pins_full, gold_all, folds = data["pins_full"], data["gold_all"], data["folds"]
    nonpin = data["nonpinnable"]
    gold_pin = {s: pins_full[s] for s in pins_full}
    sec_gold = {s: gold_all[s] for s in nonpin}

    tasks = []
    n_cipher = len(set(data["flat"]))
    reach_dv = set(sv.target_tokens_for(data["prob"], n_cipher)[:n_cipher])
    for k, held in enumerate(folds):
        held_set = set(held)
        tasks.append({
            "key": f"baseline_fold{k}", "lm": "dravidian", "terms": [],
            "fold": k, "held": held,
            "pins": {s: v for s, v in pins_full.items() if s not in held_set},
            "eval_gold": gold_pin, "secondary_signs": nonpin,
            "secondary_gold": sec_gold, "train_gold": None,
            "reachable": reach_dv})
    # pin sweep on fold 0 (budget 'all' == baseline fold 0, reused)
    held0 = set(folds[0])
    avail0 = {s: v for s, v in pins_full.items() if s not in held0}
    for budget in (0, 53, 90):
        tasks.append({
            "key": f"sweep_b{budget}_fold0", "lm": "dravidian", "terms": [],
            "fold": 0, "held": folds[0],
            "pins": sv.select_pin_budget(avail0, budget, data["flat"]),
            "eval_gold": gold_pin, "secondary_signs": None,
            "secondary_gold": None, "train_gold": None,
            "reachable": reach_dv})
    # blind controls
    for lm in ("sanskrit", "geez", "scrambled"):
        prob_c, vocab_c = lm_for(lm, data)
        vset = set(vocab_c)
        reach_c = set(sv.target_tokens_for(prob_c, n_cipher)[:n_cipher])
        eval_gold_c = {s: (g if g in vset else None) for s, g in gold_pin.items()}
        for k, held in enumerate(folds):
            held_set = set(held)
            tasks.append({
                "key": f"control_{lm}_fold{k}", "lm": lm, "terms": [],
                "fold": k, "held": held,
                "pins": {s: v for s, v in pins_full.items()
                         if s not in held_set and v in vset},
                "eval_gold": eval_gold_c, "secondary_signs": None,
                "secondary_gold": None, "train_gold": None,
                "reachable": reach_c})
    results = run_tasks(tasks, "step1", force)
    by = {r["key"]: r for r in results}

    base = [by[f"baseline_fold{k}"] for k in range(5)]
    base_stats = stats_of([r["primary"]["rate"] for r in base])
    base_reach_stats = stats_of([r["primary_reachable"]["rate"] for r in base
                                 if r["primary_reachable"]["rate"] is not None])
    sec_rates = [r["secondary"]["rate"] for r in base]
    sec_stats = stats_of(sec_rates)
    sec_pooled = {"n_agree": sum(r["secondary"]["n_agree"] for r in base),
                  "n_eval": sum(r["secondary"]["n_eval"] for r in base)}
    sec_pooled["rate"] = round(sec_pooled["n_agree"] / sec_pooled["n_eval"], 4)

    sweep = {}
    for budget in (0, 53, 90):
        r = by[f"sweep_b{budget}_fold0"]
        sweep[str(budget)] = {"n_pins": r["n_pins"], "z": r["z"],
                              "held_out_rate": r["primary"]["rate"],
                              "n_eval": r["primary"]["n_eval"]}
    r_all = by["baseline_fold0"]
    sweep["all_available"] = {"n_pins": r_all["n_pins"], "z": r_all["z"],
                              "held_out_rate": r_all["primary"]["rate"],
                              "n_eval": r_all["primary"]["n_eval"]}

    controls = {}
    for lm in ("sanskrit", "geez", "scrambled"):
        rs = [by[f"control_{lm}_fold{k}"] for k in range(5)]
        st = stats_of([r["primary"]["rate"] for r in rs])
        controls[lm] = {
            "held_out": st,
            "held_out_reachable": stats_of(
                [r["primary_reachable"]["rate"] for r in rs
                 if r["primary_reachable"]["rate"] is not None]),
            "z_mean": round(statistics.mean(r["z"] for r in rs), 3),
            "stability_mean": round(statistics.mean(r["held_stability"] for r in rs), 4),
            "n_pins_fold0": rs[0]["n_pins"],
            "n_eval_fold0": rs[0]["primary"]["n_eval"],
            "pooled_sd_vs_dravidian": round(pooled_sd(base_stats, st), 4),
            "discriminating_margin": round(base_stats["mean"] - st["mean"], 4),
            "dravidian_beats_by_rule": (base_stats["mean"] - st["mean"]) > pooled_sd(base_stats, st),
        }
    discriminating = all(c["dravidian_beats_by_rule"] for c in controls.values())
    artifact = {
        "phase": 107, "step": 1, "spec": "specs/005-phase52-v2",
        "gpu_device": DEVICE,
        "harness_config": {"seeds": list(HARNESS["seeds"]),
                           "n_restarts": HARNESS["n_restarts"],
                           "max_iter": HARNESS["max_iter"],
                           "temp": 1.0, "cooling": 0.9997},
        "protocol": "k=5 stratified folds (seed 107) over the 116 Phase-52-pinnable anchors; "
                    "primary = exact-match held-out agreement; secondary = 159 never-pinned H+M anchors",
        "n_pinnable": len(pins_full), "n_nonpinnable": len(nonpin),
        "baseline_current_objective": {
            "held_out_primary": base_stats,
            "held_out_primary_reachable_only": base_reach_stats,
            "held_out_secondary_per_fold": sec_stats,
            "held_out_secondary_pooled": sec_pooled,
            "z_mean": round(statistics.mean(r["z"] for r in base), 3),
            "folds": [{"fold": r["fold"], "z": r["z"], "n_pins": r["n_pins"],
                       "primary": r["primary"], "secondary": r["secondary"]}
                      for r in base],
        },
        "phase52_table_decomposition_context": {
            "source": "reports/phase52_full_decipherment_table.json (Phase-106 artifact, 2-char prefix metric)",
            "pinned_signs": "113/116 = 0.974",
            "never_pinned_signs": "0/159 = 0.000",
            "note": "The historical 41.09% headline is entirely the pinned subset; see spec 005 Addendum A.",
        },
        "pin_sweep_fold0": sweep,
        "blind_controls": controls,
        "verdicts": {
            "discriminating_by_preregistered_rule": discriminating,
            "claim_A_generalises": controls["scrambled"]["dravidian_beats_by_rule"],
            "claim_B_dravidian_best_target": not any(
                controls[lm]["held_out"]["mean"] >= base_stats["mean"]
                for lm in ("sanskrit", "geez")),
        },
        "caveats": [
            "Held-out agreement measures consistency with the anchor programme, not with historical reality (spec 005 H13).",
            "Ge'ez held-out agreement is structurally bounded: Dravidian gold syllables are not in the Ethiopic inventory, so its evaluable n is ~0 and the metric is reported for completeness; its z/stability are the informative columns.",
            "Sanskrit evaluable n is limited to gold syllables present in the Sanskrit vocab.",
        ],
    }
    STEP1_OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False), "utf-8")
    print(f"Step 1 artifact: {STEP1_OUT}")
    return artifact


# ── Step 2 ────────────────────────────────────────────────────────────────

def _ablation_tasks(terms: tuple[str, ...], tag: str, data: dict) -> list[dict]:
    pins_full, gold_all, folds = data["pins_full"], data["gold_all"], data["folds"]
    gold_pin = {s: pins_full[s] for s in pins_full}
    tasks = []
    for k, held in enumerate(folds):
        held_set = set(held)
        tasks.append({
            "key": f"{tag}_fold{k}", "lm": "dravidian", "terms": list(terms),
            "fold": k, "held": held,
            "pins": {s: v for s, v in pins_full.items() if s not in held_set},
            "eval_gold": gold_pin, "secondary_signs": None,
            "secondary_gold": None,
            "train_gold": {s: g for s, g in gold_all.items() if s not in held_set}})
    return tasks


def step2(force: bool = False) -> dict:
    if not STEP1_OUT.exists():
        raise SystemExit("Step 1 artifact missing — run step1 first")
    s1 = json.loads(STEP1_OUT.read_text("utf-8"))
    base_stats = s1["baseline_current_objective"]["held_out_primary"]
    base_z = s1["baseline_current_objective"]["z_mean"]
    data = base_data()
    terms_report = {}
    kept: list[str] = []
    for term in ("phono", "harmony", "positional"):
        rs = run_tasks(_ablation_tasks((term,), f"abl_{term}", data), "step2", force)
        st = stats_of([r["primary"]["rate"] for r in rs])
        z_mean = round(statistics.mean(r["z"] for r in rs), 3)
        delta_pp = round((st["mean"] - base_stats["mean"]) * 100, 2)
        z_drop_rel = (base_z - z_mean) / base_z if base_z else 0.0
        keep = delta_pp >= 2.0 and z_drop_rel <= 0.10
        terms_report[term] = {"held_out": st, "z_mean": z_mean,
                              "delta_pp_vs_baseline": delta_pp,
                              "z_relative_drop": round(z_drop_rel, 4),
                              "kept_by_rule": keep}
        if keep:
            kept.append(term)
        print(f"  term {term}: held-out {st['mean']} (Δ {delta_pp:+} pp), "
              f"z {z_mean} -> {'KEPT' if keep else 'DROPPED'}", flush=True)
    combined = None
    if len(kept) >= 2:
        rs = run_tasks(_ablation_tasks(tuple(kept), "abl_combined", data), "step2", force)
        combined = {"terms": kept,
                    "held_out": stats_of([r["primary"]["rate"] for r in rs]),
                    "z_mean": round(statistics.mean(r["z"] for r in rs), 3)}
    elif len(kept) == 1:
        combined = {"terms": kept, "held_out": terms_report[kept[0]]["held_out"],
                    "z_mean": terms_report[kept[0]]["z_mean"],
                    "note": "single kept term; combined == that term's run"}
    artifact = {
        "phase": 107, "step": 2, "spec": "specs/005-phase52-v2",
        "gpu_device": DEVICE,
        "baseline_from_step1": {"held_out": base_stats, "z_mean": base_z},
        "keep_rule": "kept iff held-out agreement improves >= +2.0 pp AND mean z falls <= 10% relative",
        "terms": terms_report, "kept_terms": kept, "combined": combined,
        "weights": {"lambda_phono": 3.0, "lambda_harmony": 3.0, "positional": 1.0},
    }
    STEP2_OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False), "utf-8")
    print(f"Step 2 artifact: {STEP2_OUT}")
    return artifact


# ── Step 3 ────────────────────────────────────────────────────────────────

def step3(force: bool = False) -> dict:
    if not STEP2_OUT.exists():
        raise SystemExit("Step 2 artifact missing — run step2 first")
    s2 = json.loads(STEP2_OUT.read_text("utf-8"))
    best_terms = tuple(s2["kept_terms"])
    data = base_data()
    flat, insc, prob, vocab = data["flat"], data["insc"], data["prob"], data["vocab"]
    pins_full, gold_all = data["pins_full"], data["gold_all"]
    logp = None
    if "positional" in best_terms:
        logp = sv.build_positional_logp(gold_all, flat, insc, vocab)
    objective = sv.Objective(prob, flat, insc, terms=best_terms, positional_logp=logp)

    # equivalence: full vs delta, identical config
    eq_cfg = dict(seeds=(0, 1, 2, 3, 4), n_restarts=5, max_iter=10_000)
    full = sv.run_sa(objective, flat, prob, pins_full, **eq_cfg)
    delta_obj = sv.DeltaObjective(objective, insc)
    delt = sv.run_sa_delta(delta_obj, flat, prob, pins_full, **eq_cfg)
    full_scores = [r["score"] for r in full["seeds"]]
    delta_scores = [r["score"] for r in delt["seeds"]]
    mean_diff_pct = abs(statistics.mean(full_scores) - statistics.mean(delta_scores)) \
        / abs(statistics.mean(full_scores)) * 100
    all_signs = sorted(set(full["consensus"]) | set(delt["consensus"]))
    same = sum(1 for s in all_signs if full["consensus"].get(s) == delt["consensus"].get(s))
    agree_share = same / len(all_signs) if all_signs else 0.0
    claim_d = mean_diff_pct < 1.0 and agree_share >= 0.95

    # scaled run, checkpointed per seed
    ckdir = CKPT / "step3"
    ckdir.mkdir(parents=True, exist_ok=True)
    seed_mappings = []
    seed_scores = []
    for seed in range(10):
        ck = ckdir / f"scaled_seed{seed}.json"
        if ck.exists() and not force:
            rec = json.loads(ck.read_text("utf-8"))
            print(f"  [ckpt] scaled seed {seed}")
        else:
            t0 = time.perf_counter()
            r = sv.run_sa_delta(delta_obj, flat, prob, pins_full,
                                seeds=(seed,), n_restarts=10, max_iter=100_000)
            rec = {"seed": seed, "score": r["seeds"][0]["score"],
                   "mapping": r["seeds"][0]["mapping"],
                   "elapsed_s": round(time.perf_counter() - t0, 1)}
            ck.write_text(json.dumps(rec), "utf-8")
            print(f"  [done] scaled seed {seed}: score={rec['score']:.1f} "
                  f"({rec['elapsed_s']}s)", flush=True)
        seed_mappings.append(rec["mapping"])
        seed_scores.append(rec["score"])
    consensus, frac = sv.consensus_of(seed_mappings)
    null_mu, null_std = sv.estimate_null(objective, flat, prob, n=30, seed=42)
    z_scaled = (statistics.mean(seed_scores) - null_mu) / null_std

    from collections import Counter
    freq = Counter(flat)
    table = []
    for sign in sorted(consensus, key=lambda s: -freq.get(s, 0)):
        f = frac.get(sign, 0.0)
        tier = ("pinned" if sign in pins_full else
                "SA-supported" if f >= 0.80 else
                "probable" if f >= 0.60 else "unstable")
        anch = data["anchors"].get(sign, {})
        table.append({
            "sign": sign, "n_corpus": freq.get(sign, 0),
            "sa_reading": consensus[sign], "sa_consensus_frac": round(f, 3),
            "tier": tier,
            "anchor_reading": anch.get("reading", ""),
            "anchor_confidence": anch.get("confidence", "UNREAD"),
            "gold": gold_all.get(sign),
            "sa_agrees_gold": (consensus[sign] == gold_all[sign])
            if gold_all.get(sign) else None,
        })
    TABLE_OUT.write_text(json.dumps(table, indent=2, ensure_ascii=False), "utf-8")

    p52 = json.loads((REPORTS / "phase52_syllabic_sa.json").read_text("utf-8"))
    old_cov = p52.get("coverage", {})
    old_agree = (old_cov.get("sa_agrees_confirmed", 0)
                 / max(1, old_cov.get("n_high", 0) + old_cov.get("n_medium", 0)))
    artifact = {
        "phase": 107, "step": 3, "spec": "specs/005-phase52-v2",
        "gpu_device": DEVICE, "best_terms": list(best_terms),
        "equivalence": {
            "config": {"seeds": list(eq_cfg["seeds"]), "n_restarts": 5, "max_iter": 10_000},
            "full_best_scores": [round(s, 2) for s in full_scores],
            "delta_best_scores": [round(s, 2) for s in delta_scores],
            "mean_diff_pct": round(mean_diff_pct, 4),
            "consensus_agreement_share": round(agree_share, 4),
            "claim_D_pass": claim_d,
        },
        "scaled_run": {
            "config": {"seeds": 10, "n_restarts": 10, "max_iter": 100_000},
            "seed_scores": [round(s, 2) for s in seed_scores],
            "mean_score": round(statistics.mean(seed_scores), 2),
            "null_mean": round(null_mu, 2), "null_std": round(null_std, 2),
            "z": round(z_scaled, 3),
            "n_signs": len(consensus),
            "n_sa_supported_ge_0.80": sum(1 for t in table if t["tier"] == "SA-supported"),
            "n_probable_ge_0.60": sum(1 for t in table if t["tier"] == "probable"),
            "n_unstable": sum(1 for t in table if t["tier"] == "unstable"),
            "n_pinned": sum(1 for t in table if t["tier"] == "pinned"),
        },
        "headline_comparison": {
            "phase52_original_rerun_phase106": {
                "z": p52["results"]["z_score"], "agreement_circular": round(old_agree, 4),
                "config": "5 seeds x 10 restarts x 30k iters, LM-only, 116 pins, full rescoring"},
            "phase52_v2_scaled": {
                "z": round(z_scaled, 3), "terms": list(best_terms),
                "config": "10 seeds x 10 restarts x 100k iters, delta scoring, 116 pins"},
            "note": "z values are within-objective (each vs its own null); the honest "
                    "generalisation metric is the Step-1/2 held-out agreement, not z.",
        },
    }
    STEP3_OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False), "utf-8")
    print(f"Step 3 artifact: {STEP3_OUT}; table: {TABLE_OUT}")
    return artifact


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["step1", "step2", "step3"])
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    {"step1": step1, "step2": step2, "step3": step3}[args.step](force=args.force)


if __name__ == "__main__":
    main()
