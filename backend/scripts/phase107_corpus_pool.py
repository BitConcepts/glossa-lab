"""Phase-107 Step 4: corpus pooling (spec 005).

Converts the in-repo CISI subset (Parpola P-numbers) to Mahadevan
M-numbers via crosswalk v2.1, dedupes against Holdat, pools, and re-runs
the Step-1a primary held-out metric on the enlarged corpus with the best
objective from Step 2. Additional converted layers can be supplied with
--layer NAME=PATH:FORMAT (JSON {"inscriptions": [[sign, ...], ...]};
FORMAT 'm' = already M-numbers, 'p' = P-numbers to convert).

Dedupe rule (fixed before pooling, spec 005 Step 4): a converted
inscription whose sign sequence (length >= 3) exactly equals a Holdat
inscription's sequence is dropped as a probable duplicate transcription
of the same seal. Only fully-convertible inscriptions are pooled.

GPU: torch guarded per H20 pattern. Output:
reports/phase107_step4_pooling.json
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
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
CISI = REPO / "backend/glossa_lab/data/indus_cisi_corpus.json"
CROSSWALK = REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json"
OUT = REPORTS / "phase107_step4_pooling.json"
HARNESS = dict(seeds=(0, 1, 2), n_restarts=5, max_iter=10_000)
CONF_RANK = {"HIGH": 0, "MEDIUM": 1, "CANDIDATE": 2}


def p_to_m_map() -> tuple[dict[str, str], dict]:
    cw = json.loads(CROSSWALK.read_text("utf-8"))["crosswalk"]
    by_p: dict[str, list[tuple[str, str]]] = {}
    for m_id, e in cw.items():
        by_p.setdefault(e["parpola_id"], []).append((m_id, e.get("confidence", "CANDIDATE")))
    mapping, conflicts = {}, {}
    for p_id, cands in by_p.items():
        cands.sort(key=lambda t: (CONF_RANK.get(t[1], 3), t[0]))
        mapping[p_id] = cands[0][0]
        if len(cands) > 1:
            conflicts[p_id] = [c[0] for c in cands]
    return mapping, {"n_conflicts": len(conflicts), "conflicts": conflicts}


def convert_inscriptions(inscriptions: list[list[str]], p2m: dict[str, str]):
    """Returns (kept, stats): only fully-convertible inscriptions."""
    kept, n_partial = [], 0
    signs_seen, signs_covered = set(), set()
    for insc in inscriptions:
        signs_seen.update(insc)
        conv = [p2m.get(s) for s in insc]
        if all(conv):
            kept.append(conv)
            signs_covered.update(insc)
        else:
            n_partial += 1
    stats = {"n_inscriptions_in": len(inscriptions),
             "n_fully_convertible": len(kept),
             "n_partial_dropped": n_partial,
             "distinct_signs_in": len(signs_seen),
             "distinct_signs_covered": len(signs_covered),
             "tokens_in": sum(len(i) for i in inscriptions),
             "tokens_kept": sum(len(i) for i in kept)}
    return kept, stats


def dedupe(converted: list[list[str]], holdat: list[list[str]]):
    holdat_seqs = {tuple(i) for i in holdat if len(i) >= 3}
    kept, dropped = [], 0
    for insc in converted:
        if len(insc) >= 3 and tuple(insc) in holdat_seqs:
            dropped += 1
        else:
            kept.append(insc)
    return kept, dropped


def headline_on_pool(pooled_insc: list[list[str]], best_terms: tuple[str, ...],
                     data: dict) -> dict:
    flat_p = [s for insc in pooled_insc for s in insc]
    pins_full, gold_all, folds = data["pins_full"], data["gold_all"], data["folds"]
    gold_pin = {s: pins_full[s] for s in pins_full}
    rates, zs = [], []
    for k, held in enumerate(folds):
        held_set = set(held)
        logp = None
        if "positional" in best_terms:
            train_gold = {s: g for s, g in gold_all.items() if s not in held_set}
            logp = sv.build_positional_logp(train_gold, flat_p, pooled_insc, data["vocab"])
        objective = sv.Objective(data["prob"], flat_p, pooled_insc,
                                 terms=best_terms, positional_logp=logp)
        pins = {s: v for s, v in pins_full.items() if s not in held_set}
        res = sv.run_sa(objective, flat_p, data["prob"], pins, **HARNESS)
        ag = sv.agreement(res["consensus"], gold_pin, held)
        mu, sd = sv.estimate_null(objective, flat_p, data["prob"], n=30, seed=42)
        z = (statistics.mean(r["score"] for r in res["seeds"]) - mu) / sd
        rates.append(ag["rate"])
        zs.append(round(z, 3))
        print(f"  pooled fold {k}: held-out {ag['n_agree']}/{ag['n_eval']} z={z:.2f}",
              flush=True)
    return {"folds": [round(r, 4) for r in rates],
            "mean": round(statistics.mean(rates), 4),
            "sd": round(statistics.stdev(rates), 4) if len(rates) > 1 else 0.0,
            "z_folds": zs}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--layer", action="append", default=[],
                    help="NAME=PATH:FORMAT extra converted layer (repeatable)")
    args = ap.parse_args()

    s2 = json.loads((REPORTS / "phase107_step2_ablation.json").read_text("utf-8"))
    best_terms = tuple(s2["kept_terms"])
    flat, holdat_insc = sv.load_holdat_corpus()
    anchors = sv.load_anchors()
    prob, vocab = sv.load_dravidian_lm()
    pins_full = sv.phase52_pins(vocab)
    gold_all = sv.extract_gold(anchors, vocab)
    folds = sv.make_folds(pins_full, anchors, k=5, seed=107)
    data = {"prob": prob, "vocab": vocab, "pins_full": pins_full,
            "gold_all": gold_all, "folds": folds}

    p2m, conflict_info = p_to_m_map()
    cisi = json.loads(CISI.read_text("utf-8"))
    cisi_insc = [i["signs"] for i in cisi["inscriptions"]]
    converted, conv_stats = convert_inscriptions(cisi_insc, p2m)
    kept, n_dup = dedupe(converted, holdat_insc)
    layers = [{"name": "cisi_subset_inrepo", "source": "backend/glossa_lab/data/indus_cisi_corpus.json",
               "conversion": conv_stats, "dedup_dropped": n_dup,
               "inscriptions_pooled": len(kept),
               "tokens_pooled": sum(len(i) for i in kept)}]
    pooled = [list(i) for i in holdat_insc] + kept

    for spec in args.layer:
        name, rest = spec.split("=", 1)
        path, fmt = rest.rsplit(":", 1)
        raw = json.loads(Path(path).read_text("utf-8"))
        insc = raw["inscriptions"]
        if fmt == "p":
            conv, st = convert_inscriptions(insc, p2m)
        else:
            conv, st = insc, {"n_inscriptions_in": len(insc),
                              "n_fully_convertible": len(insc),
                              "tokens_kept": sum(len(i) for i in insc)}
        kept_l, dup_l = dedupe(conv, pooled)
        layers.append({"name": name, "source": path, "format": fmt,
                       "conversion": st, "dedup_dropped": dup_l,
                       "inscriptions_pooled": len(kept_l),
                       "tokens_pooled": sum(len(i) for i in kept_l)})
        pooled += kept_l

    pooled_tokens = sum(len(i) for i in pooled)
    headline = headline_on_pool(pooled, best_terms, data)

    holdat_best = None
    if s2.get("combined"):
        holdat_best = {"held_out_mean": s2["combined"]["held_out"]["mean"],
                       "held_out_sd": s2["combined"]["held_out"]["sd"]}
    claim_e = None
    if holdat_best:
        pooled_sd = ((headline["sd"] ** 2 + holdat_best["held_out_sd"] ** 2) / 2) ** 0.5
        claim_e = {"pooled_sd": round(pooled_sd, 4),
                   "pooling_helps_by_rule": (headline["mean"] - holdat_best["held_out_mean"]) > pooled_sd,
                   "falsified_by_rule": (holdat_best["held_out_mean"] - headline["mean"]) > pooled_sd}

    acquisition = None
    acq_path = REPORTS / "phase107_acquisition_log.json"
    if acq_path.exists():
        acquisition = json.loads(acq_path.read_text("utf-8"))

    artifact = {
        "phase": 107, "step": 4, "spec": "specs/005-phase52-v2",
        "gpu_device": DEVICE, "best_terms": list(best_terms),
        "crosswalk_conflicts": conflict_info,
        "layers": layers,
        "corpus_sizes": {"holdat_inscriptions": len(holdat_insc),
                         "holdat_tokens": len(flat),
                         "pooled_inscriptions": len(pooled),
                         "pooled_tokens": pooled_tokens},
        "pooled_headline_primary_cv": headline,
        "holdat_only_best_objective": holdat_best,
        "claim_E_pooling": claim_e,
        "acquisition": acquisition,
        "dedupe_rule": "converted sequence (len>=3) exactly matching a Holdat sequence is dropped",
    }
    OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False), "utf-8")
    print(f"Step 4 artifact: {OUT}")


if __name__ == "__main__":
    main()
