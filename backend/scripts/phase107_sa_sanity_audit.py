"""Phase-107 Step 1 sanity audit (spec 005, continuation audit).

Independent verification of the Step-1 held-out zero BEFORE Steps 2-5
build on it. Three audit families:

  (a) LEAKAGE — held-out signs must be excluded from the pins used in
      their fold AND from the per-fold positional-profile training gold
      (Step 2 path); folds must be disjoint and cover the pinnable set;
      the secondary (never-pinned) signs must never be pinned; the LM
      must carry no anchor-derived content (its keys are syllables of an
      external corpus, checked mechanically).
  (b) REACHABILITY — the Phase-52 target pool truncates the LM syllable
      space to the first n_cipher (=390) sorted syllables; held-out
      golds outside that pool are structurally unreachable. Recompute
      the reachable denominators and check them against the Step-1
      checkpoints' primary_reachable n_eval, fold by fold.
  (c) CONFIG — re-run fold 0 at the Phase-52 PRODUCTION config
      (5 seeds x 10 restarts x 30,000 iterations, LM-only objective,
      same pins as the harness fold 0) to confirm the 0.000 held-out
      agreement is not an artifact of the reduced harness config
      (3 x 5 x 10,000).

GPU: torch guarded per H20 pattern. Output:
reports/phase107_step1_sanity_audit.json
"""
from __future__ import annotations

import importlib.util
import json
import re
import statistics
import sys
import time
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
CKPT1 = REPO / ".glossa-state" / "phase107_checkpoints" / "step1"
OUT = REPORTS / "phase107_step1_sanity_audit.json"
PROD_CFG = dict(seeds=(0, 1, 2, 3, 4), n_restarts=10, max_iter=30_000)


def _load_driver():
    spec = importlib.util.spec_from_file_location(
        "phase107_driver", REPO / "backend/scripts/phase107_sa_validation.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    driver = _load_driver()
    data = driver.base_data()
    flat, insc = data["flat"], data["insc"]
    prob, vocab = data["prob"], data["vocab"]
    pins_full, gold_all, folds = data["pins_full"], data["gold_all"], data["folds"]
    nonpin = data["nonpinnable"]
    gold_pin = {s: pins_full[s] for s in pins_full}
    corpus_signs = set(flat)
    checks: list[dict] = []

    # ── (a) leakage ──────────────────────────────────────────────────────
    flat_folds = [s for f in folds for s in f]
    checks.append({
        "check": "A1 folds disjoint and cover the 116 pinnable anchors",
        "pass": sorted(flat_folds) == sorted(pins_full)
                and len(flat_folds) == len(set(flat_folds)) == len(pins_full),
        "fold_sizes": [len(f) for f in folds], "n_pinnable": len(pins_full)})

    pin_excl, eval_recon = [], []
    for k, held in enumerate(folds):
        held_set = set(held)
        pins_used = {s: v for s, v in pins_full.items() if s not in held_set}
        ck = json.loads((CKPT1 / f"baseline_fold{k}.json").read_text("utf-8"))
        pin_excl.append({
            "fold": k, "held_in_pins_used": sorted(held_set & set(pins_used)),
            "n_pins_expected": len(pins_used), "n_pins_checkpoint": ck["n_pins"]})
        evaluable = [s for s in held if s in corpus_signs]
        eval_recon.append({
            "fold": k, "n_held": len(held),
            "held_absent_from_corpus": sorted(held_set - corpus_signs),
            "n_evaluable_recomputed": len(evaluable),
            "n_eval_checkpoint": ck["primary"]["n_eval"],
            "n_agree_checkpoint": ck["primary"]["n_agree"]})
    checks.append({
        "check": "A2 per-fold pins exclude held-out signs (checkpoint n_pins match)",
        "pass": all(not r["held_in_pins_used"]
                    and r["n_pins_expected"] == r["n_pins_checkpoint"]
                    for r in pin_excl),
        "folds": pin_excl})
    checks.append({
        "check": "A2b checkpoint evaluable denominators recomputed from corpus membership",
        "pass": all(r["n_evaluable_recomputed"] == r["n_eval_checkpoint"]
                    for r in eval_recon),
        "folds": eval_recon,
        "note": "held-out signs absent from the Holdat flat stream are not in "
                "the SA consensus map and are skipped by agreement(); they are "
                "identified per fold in held_absent_from_corpus"})

    abl_tasks = driver._ablation_tasks(("positional",), "audit", data)
    pos_excl = [{"fold": t["fold"],
                 "held_in_train_gold": sorted(set(t["held"]) & set(t["train_gold"]))}
                for t in abl_tasks]
    checks.append({
        "check": "A3 Step-2 positional train_gold excludes the fold's held-out signs "
                 "(driver task construction, the exact dicts the ablation runs consume)",
        "pass": all(not r["held_in_train_gold"] for r in pos_excl),
        "folds": pos_excl})

    sign_id = re.compile(r"^M\d{3}$")
    lm_keys_are_signs = [k for pair in prob for k in pair if sign_id.match(k)]
    checks.append({
        "check": "A4 Dravidian LM carries no anchor/sign content (bigram keys are syllables)",
        "pass": not lm_keys_are_signs,
        "n_bigram_keys_checked": 2 * len(prob), "sign_like_keys": lm_keys_are_signs[:5],
        "note": "gold extraction (sv.extract_gold) reads INDUS_FINAL_ANCHORS.json only; "
                "the LM is the external Dravidian syllabic corpus (CITATIONS A-series)"})

    checks.append({
        "check": "A5 secondary set (159 never-pinned H+M) is disjoint from the pin set",
        "pass": not (set(nonpin) & set(pins_full)) and len(nonpin) == 159,
        "n_nonpinnable": len(nonpin)})

    # ── (b) reachability ─────────────────────────────────────────────────
    n_cipher = len(corpus_signs)
    pool = sv.target_tokens_for(prob, n_cipher)[:n_cipher]
    pool_set = set(pool)
    unreachable_golds = sorted({g for g in gold_pin.values()} - pool_set)
    reach_rows = []
    for k, held in enumerate(folds):
        ck = json.loads((CKPT1 / f"baseline_fold{k}.json").read_text("utf-8"))
        # Evaluable under agreement()'s definition: held AND gold reachable
        # AND present in the consensus map (i.e. occurring in the corpus).
        # First audit run (2026-10-05) omitted the corpus-membership term
        # and flagged a spurious B1 FAIL on fold 1: held sign H003 has a
        # reachable gold but zero Holdat occurrences, so the checkpoint's
        # reachable n_eval (22) is exactly one less than the naive count
        # (23). Step-1 numbers were never wrong; the audit check was.
        reach_held = [s for s in held
                      if gold_pin[s] in pool_set and s in corpus_signs]
        reach_rows.append({
            "fold": k, "n_held": len(held), "n_reachable_gold": len(reach_held),
            "n_eval_checkpoint_reachable": ck["primary_reachable"]["n_eval"],
            "n_agree_checkpoint_reachable": ck["primary_reachable"]["n_agree"]})
    checks.append({
        "check": "B1 reachable-only denominators match Step-1 checkpoints fold by fold",
        "pass": all(r["n_reachable_gold"] == r["n_eval_checkpoint_reachable"]
                    for r in reach_rows),
        "target_pool_size": len(pool), "n_cipher": n_cipher,
        "unreachable_gold_values": unreachable_golds,
        "folds": reach_rows,
        "note": "Phase-52 init truncates the target space to the first n_cipher "
                "sorted LM syllables; golds outside it can never be assigned to a "
                "free sign (Addendum A). Reachable-only agreement in Step 1 is "
                "nevertheless 0.000 in every fold."})

    # ── (c) production-config fold 0 ─────────────────────────────────────
    held0 = folds[0]
    pins0 = {s: v for s, v in pins_full.items() if s not in set(held0)}
    objective = sv.Objective(prob, flat, insc, terms=())
    t0 = time.perf_counter()
    res = sv.run_sa(objective, flat, prob, pins0, **PROD_CFG)
    elapsed = round(time.perf_counter() - t0, 1)
    prim = sv.agreement(res["consensus"], gold_pin, held0)
    prim.pop("detail", None)
    reach0 = [s for s in held0 if gold_pin[s] in pool_set]
    prim_r = sv.agreement(res["consensus"], gold_pin, reach0)
    prim_r.pop("detail", None)
    mu, sd = sv.estimate_null(objective, flat, prob, n=30, seed=42)
    z_prod = (statistics.mean(r["score"] for r in res["seeds"]) - mu) / sd
    ck0 = json.loads((CKPT1 / "baseline_fold0.json").read_text("utf-8"))
    checks.append({
        "check": "C1 fold 0 at production config reproduces the harness held-out result",
        "pass": prim["n_agree"] == ck0["primary"]["n_agree"],
        "production_config": {"seeds": list(PROD_CFG["seeds"]),
                              "n_restarts": PROD_CFG["n_restarts"],
                              "max_iter": PROD_CFG["max_iter"]},
        "elapsed_s": elapsed,
        "primary": prim, "primary_reachable_only": prim_r,
        "z_production": round(z_prod, 3),
        "harness_fold0": {"primary": ck0["primary"], "z": ck0["z"],
                          "config": "3 seeds x 5 restarts x 10,000 iters"}})

    artifact = {
        "phase": 107, "step": "1-sanity-audit", "spec": "specs/005-phase52-v2",
        "gpu_device": DEVICE,
        "subject": "reports/phase107_step1_validation.json (Step-1 held-out zero)",
        "revision_note": ("Run 2 (2026-10-05): run 1 reported B1 FAIL — an audit-side "
                          "denominator mis-specification (reachable count omitted "
                          "corpus membership; fold 1's held sign H003 has a reachable "
                          "gold but zero Holdat occurrences, reconciling the 23-vs-22 "
                          "difference exactly, cf. check A2b). B1 was corrected to the "
                          "agreement() evaluability definition and the audit re-run in "
                          "full. No Step-1 number changed; the Step-1 zero stands."),
        "checks": checks,
        "all_pass": all(c["pass"] for c in checks),
        "verdict": ("Step-1 zero is NOT a harness artifact: no leakage path found, "
                    "reachability denominators reconcile exactly, and the production "
                    "config reproduces the harness fold-0 held-out agreement."
                    if all(c["pass"] for c in checks) else
                    "One or more audit checks FAILED — see checks[]; Step 1 must be "
                    "re-run after a protocol fix before Steps 2-5 build on it."),
    }
    OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False), "utf-8")
    print(f"Sanity audit: {OUT}  all_pass={artifact['all_pass']}")
    for c in checks:
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['check']}")


if __name__ == "__main__":
    main()
