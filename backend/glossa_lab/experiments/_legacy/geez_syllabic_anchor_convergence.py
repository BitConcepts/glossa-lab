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

# ExperimentBase removed (H15/H16: this experiment is now the graph spec geez_anchor_convergence)
# Helper functions retained as internal utilities for the graph engine.
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
    """GPU BigramScorer fast path.

    cipher_inscriptions=None is critical: passing inscriptions populates
    cipher_positional which sets _no_constraints=False even with ocp_weight=0,
    bypassing the numpy/cupy BigramScorer and causing 50-200x slowdown.
    """
    from glossa_lab.pipelines.decipher import decipher
    r = decipher(cipher_signs=ctok, target_model=lm, seed=seed,
                 max_iterations=sa_iter, restarts=sa_rest,
                 cipher_inscriptions=None,   # None = GPU BigramScorer fast path
                 use_sa=True, sa_temp_start=sa_temp, sa_cooling=sa_cool,
                 positional_weight=0.0,      # 0 = no cipher_positional built
                 ocp_weight=0.0,             # 0 = GPU BigramScorer fast path
                 use_word_bigrams=False,     # False = GPU fast path
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


# ════════════════════════════════════════════════════════════════════════════
# H15/H16 NOTE: This Python class has been removed.
# The canonical experiment is: experiments/graphs/geez_anchor_convergence.json
# Run via: shell.cmd python backend/scripts/run_geez_anchor_convergence.py
#
# The historical-reference class body that previously lived here as an
# `if False: class GeezSyllabicAnchorConvergence: ...` block has been removed
# because Python's parser still validates indentation inside `if False:` and
# the class body was malformed (single-level indent under the `if`). Git
# history retains the original implementation.
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import subprocess
    import sys
    subprocess.run([sys.executable, "backend/scripts/run_geez_anchor_convergence.py"])
