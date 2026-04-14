"""Geez Syllabic Anchor-Convergence Validation (ExperimentBase, H10/H12 compliant)

SPEED FIXES vs prior standalone script:
  ocp_weight=0.0 + use_word_bigrams=False  -- enables BigramScorer GPU/numpy fast path
  run_seeds_parallel()                     -- all seed loops use ThreadPoolExecutor

USAGE (terminal, job visible in UI):
    python -m glossa_lab.experiments.geez_syllabic_anchor_convergence

USAGE (UI):
    Experiments -> Geez Syllabic Anchor-Convergence Validation -> Run
"""
from __future__ import annotations

import csv
import json
import logging
import math
import os
import random
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from glossa_lab.experiment_base import ExperimentBase
from glossa_lab.experiments._parallel import compute_device_label, run_seeds_parallel

_log = logging.getLogger("glossa_lab.experiments.geez")

_HERE    = Path(__file__).parent
_DATA    = _HERE.parent / "data" / "geez"
_REPORTS = _HERE.parent.parent.parent / "reports"
_REPORTS.mkdir(exist_ok=True)

_PUNCT   = {chr(c) for c in range(0x1361, 0x1369)}
_NW_TPS  = 4.2


def _is_eth(c: str) -> bool:
    cp = ord(c)
    return (0x1200 <= cp <= 0x137F or 0x1380 <= cp <= 0x139F
            or 0x2D80 <= cp <= 0x2DDF or 0xAB00 <= cp <= 0xAB2F)


def _is_syl(c: str) -> bool:
    return _is_eth(c) and c not in _PUNCT


# ── Data loading ──────────────────────────────────────────────────────────────

def _parse_signlist(path: Path) -> dict[str, dict]:
    inv: dict[str, dict] = {}
    for ri, raw in enumerate(path.read_text("utf-8").splitlines()):
        parts = raw.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        name, roman = parts[0].strip(), parts[1].strip()
        order = 1
        for part in parts[2:]:
            for c in part:
                if _is_eth(c):
                    inv[c] = {"name": name, "roman": roman, "order": order,
                               "row": ri, "col": order - 1, "syl": c not in _PUNCT}
                    order += 1
    return inv


def _load_corpus(path: Path, known: set[str]) -> tuple[list[str], list[list[str]]]:
    tokens, words = [], []
    for raw in path.read_text("utf-8").splitlines():
        line = raw.strip()
        if not line or line.replace("-", "").replace(" ", "").isdigit():
            continue
        for chunk in line.split():
            ws = [c for c in chunk if c in known]
            tokens.extend(ws)
            if len(ws) >= 2:
                words.append(ws)
    return tokens, words


def _split(tokens: list[str], words: list[list[str]], r: float = 0.75) -> dict:
    idx = int(len(tokens) * r)
    tr, te = tokens[:idx], tokens[idx:]
    cum, tw, ew = 0, [], []
    for w in words:
        (tw if cum + len(w) <= idx else ew).append(w)
        cum += len(w)
    return dict(tr=tr, te=te, tw=tw, ew=ew, tr_n=len(tr), te_n=len(te))


def _build_lm(tokens: list[str], words: list[list[str]]):
    from glossa_lab.pipelines.decipher import LanguageModel
    return LanguageModel(tokens, inscriptions=words)


def _cipher(test_tok: list[str], test_w: list[list[str]],
             inv: list[str], n: int, seed: int = 42) -> dict:
    rng = random.Random(seed)
    inv_set = set(inv)
    filt = [t for t in test_tok if t in inv_set][:n]
    cw: list[list[str]] = []
    tot = 0
    for w in test_w:
        wf = [c for c in w if c in inv_set]
        if wf:
            cw.append(wf)
            tot += len(wf)
        if tot >= n:
            break
    shuf = list(inv); rng.shuffle(shuf)
    perm  = {inv[i]: shuf[i] for i in range(len(inv))}
    truth = {shuf[i]: inv[i] for i in range(len(inv))}
    return dict(tok=[perm.get(t, t) for t in filt],
                words=[[perm.get(c, c) for c in w] for w in cw],
                truth=truth, perm=perm,
                n_signs=len(set([perm.get(t, t) for t in filt])))


# ── Anchor generation ─────────────────────────────────────────────────────────

def _struct_anchors(inv, perm, lm, grid, k, n_sets=3):
    if k == 0:
        return [{}]
    inv_set = set(inv)
    fr = sorted(inv, key=lambda c: -lm.unigram_freq.get(c, 0))
    rfr = {row: sum(lm.unigram_freq.get(s, 0) for s in signs if s in inv_set)
           for row, signs in grid.items()}
    rows = sorted(grid, key=lambda r: -rfr.get(r, 0))
    sets = [{perm[c]: c for c in fr[:k] if c in perm}]
    if n_sets >= 2:
        sel = []
        for row in rows:
            if len(sel) >= k: break
            opts = [s for s in grid[row] if s in inv_set]
            if opts: sel.append(max(opts, key=lambda s: lm.unigram_freq.get(s, 0)))
        sets.append({perm[c]: c for c in sel[:k] if c in perm})
    if n_sets >= 3:
        fi, ri, sel3, uf = iter(fr), iter(rows), [], True
        while len(sel3) < k:
            if uf:
                try:
                    c = next(fi)
                    if c not in sel3: sel3.append(c)
                except StopIteration: break
            else:
                try:
                    row = next(ri)
                    opts = [s for s in grid[row] if s in inv_set and s not in sel3]
                    if opts: sel3.append(max(opts, key=lambda s: lm.unigram_freq.get(s, 0)))
                except StopIteration: break
            uf = not uf
        sets.append({perm[c]: c for c in sel3[:k] if c in perm})
    return sets


def _rand_anchors(inv, perm, k, n_sets=10, base=9999):
    if k == 0:
        return [{}]
    rng = random.Random(base + k * 100)
    return [{perm[c]: c for c in rng.sample(inv, min(k, len(inv))) if c in perm}
            for _ in range(n_sets)]


# ── Single-seed inference (module-level for ThreadPoolExecutor) ───────────────

def _one_seed(seed, ctok, cwords, lm, anch, sa_iter, sa_rest, sa_temp, sa_cool):
    """ocp_weight=0 + use_word_bigrams=False -> BigramScorer GPU/numpy fast path."""
    from glossa_lab.pipelines.decipher import decipher
    r = decipher(cipher_signs=ctok, target_model=lm, seed=seed,
                 max_iterations=sa_iter, restarts=sa_rest,
                 cipher_inscriptions=cwords or None,
                 use_sa=True, sa_temp_start=sa_temp, sa_cooling=sa_cool,
                 positional_weight=0.005,
                 ocp_weight=0.0,         # enables BigramScorer GPU fast path
                 use_word_bigrams=False,  # enables BigramScorer GPU fast path
                 anchors=anch or None, surjective=False)
    return r.get("proposed_mapping", {})


# ── Metrics ───────────────────────────────────────────────────────────────────

def _mean(xs): return sum(xs) / len(xs) if xs else float("nan")


def _metrics(maps, truth, anchored):
    if not maps: return {}
    cs = list(truth); free = [s for s in cs if s not in anchored]
    n_cs, n_f = len(cs), len(free)
    t1  = [sum(1 for s, c in m.items() if truth.get(s) == c) / n_cs for m in maps]
    t1f = [(sum(1 for s in free if m.get(s) == truth.get(s)) / n_f if free
            else float("nan")) for m in maps]
    modal, cons, csz = {}, {}, []
    for sign in cs:
        props = [m.get(sign) for m in maps if m.get(sign)]
        if not props:
            modal[sign] = ""; cons[sign] = 0.0; csz.append(0); continue
        cnt = Counter(props); mo, mc = cnt.most_common(1)[0]
        modal[sign] = mo; cons[sign] = mc / len(props); csz.append(len(cnt))
    mt1  = sum(1 for s, c in modal.items() if truth.get(s) == c) / n_cs
    mt1f = (sum(1 for s in free if modal.get(s) == truth.get(s)) / n_f
            if free else float("nan"))
    ham = 0.0
    if len(maps) > 1:
        dists = [sum(1 for s in cs if maps[i].get(s) != maps[j].get(s)) / n_cs
                 for i in range(len(maps)) for j in range(i + 1, len(maps))]
        ham = _mean(dists)
    nd = len({tuple(m.get(s, "") for s in sorted(cs)) for m in maps})
    return {"n_runs": len(maps), "n_anchors": len(anchored),
            "n_cipher_signs": n_cs, "n_free_signs": n_f,
            "mean_top1_all": round(_mean(t1), 4), "modal_top1_all": round(mt1, 4),
            "mean_top1_free": round(_mean(t1f), 4), "modal_top1_free": round(mt1f, 4),
            "mean_consistency": round(_mean(list(cons.values())), 4),
            "mean_hamming": round(ham, 4), "n_distinct_mappings": nd,
            "mean_candidate_size": round(_mean(csz), 2),
            "hci75_all_pct": round(sum(1 for v in cons.values() if v >= .75) / max(1, n_cs), 4),
            "hci75_free_pct": round(sum(1 for s in free if cons.get(s, 0) >= .75) / max(1, n_f), 4)}


def _aggregate(sm, rm):
    all_m = sm + rm
    def _avg(key, src):
        vals = [m[key] for m in src if key in m and not math.isnan(m.get(key, float("nan")))]
        return round(_mean(vals), 4) if vals else float("nan")
    keys = ["modal_top1_all", "modal_top1_free", "mean_consistency", "mean_hamming",
            "n_distinct_mappings", "mean_candidate_size", "hci75_all_pct", "hci75_free_pct"]
    agg = {"n_struct": len(sm), "n_rand": len(rm)}
    for k in keys:
        agg[f"overall_{k}"] = _avg(k, all_m)
        agg[f"struct_{k}"]  = _avg(k, sm)
        agg[f"rand_{k}"]    = _avg(k, rm)
    sf = agg.get("struct_modal_top1_free", float("nan"))
    rf = agg.get("rand_modal_top1_free",   float("nan"))
    if not (math.isnan(sf) or math.isnan(rf)):
        agg["struct_vs_rand_advantage"] = round(sf - rf, 4)
    return agg


def _conclusions(agg):
    a0  = agg.get(0,  {}); a20 = agg.get(20, {})
    f0  = a0.get("overall_modal_top1_free",  float("nan"))
    f20 = a20.get("overall_modal_top1_free", float("nan"))
    c0  = a0.get("overall_n_distinct_mappings",  float("nan"))
    c20 = a20.get("overall_n_distinct_mappings", float("nan"))
    acc = not math.isnan(f0) and not math.isnan(f20) and f20 > f0 + 0.05
    col = not math.isnan(c0) and not math.isnan(c20) and c20 < c0 * 0.7
    adv = a20.get("struct_vs_rand_advantage", float("nan"))
    success = acc and col
    txt = ("ANCHOR-AMPLIFICATION VALIDATED: Anchors cause convergence toward the true mapping "
           "in a true syllabic system. NW Semitic failure is corpus sparsity, not a method flaw."
           if success else
           "MIXED OR NEGATIVE RESULT: " +
           "; ".join([x for x, y in [
               ("accuracy does NOT rise with anchors", not acc),
               ("clusters do NOT collapse", not col)] if y]) +
           ". System may require revision before application to undeciphered corpora.")
    return {"verdict": "SUCCESS" if success else "PARTIAL/FAILURE", "conclusion": txt,
            "accuracy_rises": acc, "clusters_collapse": col,
            "struct_beats_rand": not math.isnan(adv) and adv > 0.02,
            "free_acc_0": f0, "free_acc_20": f20,
            "improvement": round(f20 - f0, 4) if not (math.isnan(f0) or math.isnan(f20)) else None}


# ═══════════════════════════════════════════════════════════════════════════════
# ExperimentBase subclass (H12 compliant)
# ═══════════════════════════════════════════════════════════════════════════════

class GeezSyllabicAnchorConvergence(ExperimentBase):
    """Geez Syllabic Anchor-Convergence Validation.

    Fully UI-discoverable ExperimentBase subclass.
    Appears in the Experiments list, runs as a tracked Job with GPU/CPU badge.
    All seed loops are parallelised via ThreadPoolExecutor (H10 compliant).
    BigramScorer GPU/numpy fast path enabled (ocp_weight=0, use_word_bigrams=False).
    """

    id            = "geez_syllabic_anchor_convergence"
    name          = "Geez Syllabic Anchor-Convergence Validation"
    category      = "Decipherment Benchmark"
    description   = ("Controlled benchmark on Geez Genesis corpus (85K tokens, ~200 signs). "
                     "Tests anchor-amplification under 6 anchor conditions with structured "
                     "and random anchor sets. Parallel seeds, GPU-aware BigramScorer.")
    estimated_time = "~8 min (CPU) / ~2 min (GPU)"
    results_file  = "reports/geez_syllabic_anchor_convergence.json"
    params_schema = {
        "type": "object",
        "properties": {
            "train_ratio":        {"type": "number",  "default": 0.75},
            "cipher_tokens":      {"type": "integer", "default": 12000},
            "anchor_counts":      {"type": "array",   "default": [0, 1, 3, 5, 10, 20]},
            "n_seeds_baseline":   {"type": "integer", "default": 10},
            "n_structured_sets":  {"type": "integer", "default": 3},
            "n_seeds_structured": {"type": "integer", "default": 4},
            "n_random_sets":      {"type": "integer", "default": 10},
            "n_seeds_random":     {"type": "integer", "default": 2},
            "sa_iterations":      {"type": "integer", "default": 10000},
            "sa_restarts":        {"type": "integer", "default": 8},
        },
    }

    def run(self, **kw: Any) -> dict[str, Any]:
        tr    = float(kw.get("train_ratio",        0.75))
        cn    = int(  kw.get("cipher_tokens",      12_000))
        acs   = list( kw.get("anchor_counts",      [0, 1, 3, 5, 10, 20]))
        nsb   = int(  kw.get("n_seeds_baseline",   10))
        nss   = int(  kw.get("n_structured_sets",  3))
        nsseed= int(  kw.get("n_seeds_structured", 4))
        nrs   = int(  kw.get("n_random_sets",      10))
        nrseed= int(  kw.get("n_seeds_random",     2))
        sa_it = int(  kw.get("sa_iterations",      10_000))
        sa_re = int(  kw.get("sa_restarts",        8))
        sa_t  = 1.0; sa_c = 0.9985

        dev = compute_device_label()
        _log.info("Geez anchor-convergence | device=%s", dev)
        t0 = time.time()

        # Data
        si     = _parse_signlist(_DATA / "Geez_signlist.txt")
        known  = {c for c, m in si.items() if m["syl"]}
        tok, words = _load_corpus(_DATA / "Geez_Genesis.txt", known)
        freq   = Counter(tok)
        inv    = sorted([c for c, n in freq.items()
                          if n >= 3 and c in si and si[c]["syl"]],
                         key=lambda c: si[c]["row"] * 10 + si[c]["col"])
        grid: dict[str, list[str]] = defaultdict(list)
        inv_set = set(inv)
        for c, m in si.items():
            if m["syl"] and c in inv_set:
                grid[m["name"]].append(c)

        _log.info("Corpus %d tok | inventory %d signs | %d words",
                  len(tok), len(inv), len(words))

        sp  = _split(tok, words, tr)
        lm  = _build_lm(sp["tr"], sp["tw"])
        tps = round(len(sp["tr"]) / max(1, len(inv)), 1)

        cd  = _cipher(sp["te"], sp["ew"], inv, cn)
        ctok, cwords, truth, perm = cd["tok"], cd["words"], cd["truth"], cd["perm"]
        _log.info("Cipher %d tok | %d signs | %.1f tok/sign",
                  len(ctok), cd["n_signs"], len(ctok) / max(1, cd["n_signs"]))

        def _run_set(anch: dict, n_seeds: int, base: int) -> dict:
            seeds = list(range(base, base + n_seeds))
            maps  = run_seeds_parallel(
                _one_seed, seeds,
                ctok, cwords, lm, anch, sa_it, sa_re, sa_t, sa_c
            )
            return _metrics(maps, truth, set(anch))

        # Main loop
        aggregated: dict[int, dict] = {}
        for ac in sorted(acs):
            _log.info("Running anchor_count=%d", ac)
            ssets = _struct_anchors(inv, perm, lm, dict(grid), ac, nss)
            rsets = _rand_anchors(inv, perm, ac, nrs)
            ns = nsb if ac == 0 else nsseed
            nr = 0   if ac == 0 else nrseed
            sm = [_run_set(s, ns, 1000 + ac * 100 + si2 * 200)
                  for si2, s in enumerate(ssets)]
            rm = [_run_set(s, nr, 5000 + ac * 100 + si2 * 200)
                  for si2, s in enumerate(rsets)] if nr > 0 else []
            agg = _aggregate(sm, rm)
            agg["n_anchors"] = ac
            aggregated[ac] = agg
            tf = agg.get("overall_modal_top1_free", float("nan"))
            _log.info("  ac=%d top1_free=%.1f%%", ac,
                      0.0 if math.isnan(tf) else tf * 100)

        # 50/50 robustness
        sp50 = _split(tok, words, 0.50)
        lm50 = _build_lm(sp50["tr"], sp50["tw"])
        cd50 = _cipher(sp50["te"], sp50["ew"], inv, cn, seed=99)
        sec50: dict[str, dict] = {}
        for ac in [0, 5, 20]:
            if ac > max(acs): continue
            as50 = _struct_anchors(inv, cd50["perm"], lm50, dict(grid), ac, 1)
            seeds = list(range(9000 + ac * 100, 9000 + ac * 100 + (5 if ac == 0 else 3)))
            maps  = run_seeds_parallel(_one_seed, seeds,
                                        cd50["tok"], cd50["words"], lm50, as50[0],
                                        sa_it, sa_re, sa_t, sa_c)
            sec50[str(ac)] = _metrics(maps, cd50["truth"], set(as50[0]))

        conc = _conclusions(aggregated)
        _log.info("VERDICT: %s", conc["verdict"])

        # Save CSVs
        _save_csvs(inv, si, freq, sp, aggregated)

        elapsed = round(time.time() - t0, 1)
        _log.info("Geez experiment complete in %.1fs | %s", elapsed, conc["verdict"])

        return {
            "title": self.name,
            "timestamp": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"),
            "elapsed_s": elapsed,
            "compute_device": dev,
            "data": {
                "corpus_tokens": len(tok), "inventory_size": len(inv),
                "train_tokens": sp["tr_n"], "test_tokens": sp["te_n"],
                "cipher_n_tokens": len(ctok), "cipher_n_signs": cd["n_signs"],
                "tokens_per_sign_lm": tps,
            },
            "lm_stats": {
                "total_tokens": len(sp["tr"]), "inventory_size": len(inv),
                "n_bigrams": len(lm.bigram_freq), "mean_tokens_per_sign": tps,
            },
            "anchor_convergence": {str(k): v for k, v in aggregated.items()},
            "secondary_50_50": sec50,
            "comparison_nw_semitic": {
                "nw_tokens_per_sign": _NW_TPS,
                "geez_tokens_per_sign_lm": tps,
                "geez_top1_0anchors": aggregated.get(0, {}).get("overall_modal_top1_all"),
                "geez_top1_20anchors": aggregated.get(20, {}).get("overall_modal_top1_all"),
            },
            "scientific_conclusions": conc,
        }


def _save_csvs(inv, si, freq, sp, aggregated):
    with open(_REPORTS / "geez_sign_inventory.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["code", "char", "codepoint", "name", "roman", "order", "freq"])
        for i, c in enumerate(inv):
            m = si.get(c, {})
            w.writerow([f"G{i+1:03d}", c, f"U+{ord(c):04X}",
                        m.get("name","?"), m.get("roman","?"), m.get("order","?"), freq.get(c,0)])
    total = sp["tr_n"] + sp["te_n"]
    with open(_REPORTS / "geez_split_manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["split","tokens","pct"])
        w.writerow(["train", sp["tr_n"], f"{100*sp['tr_n']/total:.1f}%"])
        w.writerow(["test",  sp["te_n"], f"{100*sp['te_n']/total:.1f}%"])
    with open(_REPORTS / "geez_anchor_convergence.csv", "w", newline="", encoding="utf-8") as f:
        keys = ["overall_modal_top1_all","overall_modal_top1_free",
                "overall_mean_consistency","overall_n_distinct_mappings"]
        w = csv.DictWriter(f, fieldnames=["anchor_count"]+keys, extrasaction="ignore")
        w.writeheader()
        for ac, agg in sorted(aggregated.items()):
            w.writerow({"anchor_count": ac, **{k: agg.get(k) for k in keys}})


if __name__ == "__main__":
    GeezSyllabicAnchorConvergence().run_cli()
