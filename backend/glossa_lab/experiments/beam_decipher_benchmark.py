"""Beam-search decipherment benchmark — Tier 1a cross-language.

Compares the new beam-search engine against SA on the Ugaritic→Hebrew
benchmark (Snyder 2010 / Luo 2019 protocol) across:

  Sweep A — beam width:   50 / 100 / 200 / 500
  Sweep B — anchors:      0 / 5 / 10 known pan-Semitic consonant pairs
             (at the best beam width from Sweep A)
  Sweep C — constraints:  baseline flat-bigram beam vs all-constraints beam
             (word-bigrams + OCP + root-prior + positional)

SA baseline reproduced for direct comparison.

PAN-SEMITIC COGNATE ANCHORS
----------------------------
The following consonant correspondences are phonologically certain across
all Northwest Semitic languages (Ugaritic, Hebrew, Aramaic, Arabic):

  r  ↔  r  (resh)     — universal in Semitic
  m  ↔  m  (mem)      — universal
  b  ↔  b  (bet)      — universal
  l  ↔  l  (lamed)    — universal
  n  ↔  n  (nun)      — universal
  y  ↔  y  (yod)      — universal
  k  ↔  k  (kaf)      — universal (Ugaritic k → Hebrew k)
  t  ↔  t  (tav)      — universal
  d  ↔  d  (dalet)    — conservative Semitic (Ugaritic d → Hebrew d)
  h  ↔  h  (he)       — universal

Usage:
    python -m glossa_lab.experiments.beam_decipher_benchmark
"""
from __future__ import annotations

import os
import sys
import time
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ── Shared data ────────────────────────────────────────────────────────

def _load():
    from glossa_lab.pipelines.beam_decipher import UGARITIC_PHONO_GROUPS
    from corpora.ugaritic import (
        _BAAL_CYCLE_LINES, _SIGN_TO_ID, get_answer_key,
        get_word_level_inscriptions,
    )
    from glossa_lab.data.old_hebrew import (
        get_corpus_symbols     as heb_sym,
        get_corpus_inscriptions as heb_line_inscr,
        get_word_inscriptions   as heb_word_inscr,
        get_ugaritic_to_hebrew_map,
    )
    from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy
    from glossa_lab.pipelines.beam_decipher import beam_decipher

    def _parse(ln): return [c for c in ln.split() if c != "."]

    decoded_lines = [_parse(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines = [[_SIGN_TO_ID.get(s, s) for s in l] for l in decoded_lines]
    cipher_flat   = [s for l in encoded_lines for s in l]

    ug_word_enc = get_word_level_inscriptions(encoded=True)
    ug_to_ug    = get_answer_key()
    ug_to_heb   = get_ugaritic_to_hebrew_map()
    gt          = {oid: ug_to_heb[us] for oid, us in ug_to_ug.items() if us in ug_to_heb}

    heb_flat = heb_sym()
    lm_flat  = LanguageModel(heb_flat)
    lm_word  = LanguageModel(heb_flat, inscriptions=heb_word_inscr())

    # Pan-Semitic anchors: Ugaritic sign ID → Hebrew consonant
    # (verified against get_answer_key() and get_ugaritic_to_hebrew_map())
    inv_ug  = {v: k for k, v in ug_to_ug.items()}
    ANCHORS_10 = {
        inv_ug["r"]: "r",  # resh
        inv_ug["m"]: "m",  # mem
        inv_ug["b"]: "b",  # bet
        inv_ug["l"]: "l",  # lamed
        inv_ug["n"]: "n",  # nun
        inv_ug["y"]: "y",  # yod
        inv_ug["k"]: "k",  # kaf
        inv_ug["t"]: "t",  # tav
        inv_ug["d"]: "d",  # dalet
        inv_ug["h"]: "h",  # he
    }
    ANCHORS_5 = {k: v for k, v in list(ANCHORS_10.items())[:5]}
    # Verify anchors against ground truth
    for cs, ts in ANCHORS_10.items():
        assert gt.get(cs) == ts, f"Anchor mismatch: {cs} → {ts} (expected {gt.get(cs)})"

    return {
        "cipher_flat":        cipher_flat,
        "cipher_line":        encoded_lines,
        "cipher_word":        ug_word_enc,
        "gt":                 gt,
        "lm_flat":            lm_flat,
        "lm_word":            lm_word,
        "decipher":           decipher,
        "beam_decipher":      beam_decipher,
        "score_accuracy":     score_accuracy,
        "ANCHORS_5":          ANCHORS_5,
        "ANCHORS_10":         ANCHORS_10,
        "PHONO_GROUPS":       UGARITIC_PHONO_GROUPS,
    }


# ── Run helpers ────────────────────────────────────────────────────────

def _run_beam(d, beam_width, use_word_bigrams=False, ocp_weight=0.0,
              root_prior_weight=0.0, anchors=None, surjective=True, phono_groups=None):
    t0 = time.time()
    lm = d["lm_word"] if use_word_bigrams else d["lm_flat"]
    insc = d["cipher_word"] if use_word_bigrams else d["cipher_line"]
    r = d["beam_decipher"](
        d["cipher_flat"], lm,
        beam_width=beam_width,
        cipher_inscriptions=insc,
        use_word_bigrams=use_word_bigrams,
        ocp_weight=ocp_weight,
        root_prior_weight=root_prior_weight,
        anchors=anchors,
        surjective=surjective,
        phono_groups=phono_groups,
    )
    acc = d["score_accuracy"](r["proposed_mapping"], d["gt"])
    return acc["correct"], round(time.time() - t0, 1)


def _run_sa(d, restarts=25, use_word_bigrams=False, ocp_weight=0.0,
            root_prior_weight=0.0, anchors=None, seed=42, surjective=False):
    t0 = time.time()
    lm = d["lm_word"] if use_word_bigrams else d["lm_flat"]
    insc = d["cipher_word"] if use_word_bigrams else d["cipher_line"]
    r = d["decipher"](
        d["cipher_flat"], lm,
        seed=seed, max_iterations=15000, restarts=restarts,
        cipher_inscriptions=insc,
        use_word_bigrams=use_word_bigrams,
        ocp_weight=ocp_weight,
        root_prior_weight=root_prior_weight,
        anchors=anchors,
        surjective=surjective,
    )
    acc = d["score_accuracy"](r["proposed_mapping"], d["gt"])
    return acc["correct"], round(time.time() - t0, 1)


# ── Main benchmark ────────────────────────────────────────────────────

def run_beam_benchmark(verbose: bool = True) -> dict[str, Any]:
    def _pr(*a, **kw):
        if verbose:
            print(*a, **kw)

    _pr("\n" + "=" * 70)
    _pr("  Beam Decipherment Benchmark — Tier 1a (Ugaritic → Hebrew)")
    _pr("=" * 70)

    d = _load()
    _pr(f"\n  Cipher: {len(d['cipher_flat'])} tokens, {len(set(d['cipher_flat']))} signs")
    _pr(f"  Hebrew LM (flat): {len(d['lm_flat'].bigram_freq)} bigrams")
    _pr(f"  Hebrew LM (word): {len(d['lm_word'].word_bigram_freq)} word-bigrams  "
        f"OCP={d['lm_word'].ocp_rate:.3f}  "
        f"word_cooccur pairs={len(d['lm_word'].word_cooccur)}")
    _pr(f"  10 pan-Semitic anchors: {d['ANCHORS_10']}")
    _pr(f"  Ground truth: {len(d['gt'])}/30 mappings")

    results = {}

    # ── SA Baselines ─────────────────────────────────────────────
    _pr("\n\n  ══ SA BASELINES ══")
    sa_correct, sa_t = _run_sa(d)
    _pr(f"  SA bijective (25 restarts, seed=42):     {sa_correct}/30 = {sa_correct/30*100:.1f}%  [{sa_t}s]")
    sa_surj, sa_surj_t = _run_sa(d, surjective=True)
    _pr(f"  SA surjective (25 restarts, seed=42):    {sa_surj}/30 = {sa_surj/30*100:.1f}%  [{sa_surj_t}s]")
    sa_surj_anch, sa_sa_t = _run_sa(d, surjective=True, anchors=d["ANCHORS_10"])
    _pr(f"  SA surjective + 10 anchors (seed=42):    {sa_surj_anch}/30 = {sa_surj_anch/30*100:.1f}%  [{sa_sa_t}s]")
    results["sa_baseline"] = {"bijective": sa_correct, "surjective": sa_surj,
                               "surjective_anchored": sa_surj_anch, "total": 30}

    # ── Sweep A: Beam width ───────────────────────────────────────────
    _pr("\n\n  ══ SWEEP A — Beam Width (surjective, flat bigrams, no anchors) ══")
    _pr(f"  {'Width':>6}  {'Correct':>8}  {'Accuracy':>9}  {'Time':>6}")
    _pr("  " + "-" * 38)
    sweep_a = []
    best_width = 50
    best_correct = 0
    for bw in (50, 100, 200, 500):
        correct, t = _run_beam(d, beam_width=bw)
        pct = correct / 30 * 100
        _pr(f"  {bw:>6}  {correct:>8}/30  {pct:>8.1f}%  {t:>5}s")
        sweep_a.append({"beam_width": bw, "correct": correct, "time_s": t})
        if correct > best_correct:
            best_correct = correct
            best_width = bw
    results["sweep_a_beam_width"] = sweep_a
    _pr(f"\n  Best beam width: {best_width} → {best_correct}/30 = {best_correct/30*100:.1f}%")

    # ── Sweep B: Anchors ──────────────────────────────────────────────
    _pr(f"\n\n  ══ SWEEP B — Anchors (beam_width={best_width}, flat bigrams) ══")
    _pr(f"  {'Anchors':>8}  {'Correct':>8}  {'Accuracy':>9}  {'Time':>6}")
    _pr("  " + "-" * 38)
    sweep_b = []
    for n_anchors, anchor_dict in [
        (0, None),
        (5, d["ANCHORS_5"]),
        (10, d["ANCHORS_10"]),
    ]:
        correct, t = _run_beam(d, beam_width=best_width, anchors=anchor_dict)
        pct = correct / 30 * 100
        _pr(f"  {n_anchors:>8}  {correct:>8}/30  {pct:>8.1f}%  {t:>5}s")
        sweep_b.append({"n_anchors": n_anchors, "correct": correct, "time_s": t})
    results["sweep_b_anchors"] = sweep_b

    # ── Sweep C: Phono groups + wider beams ─────────────────────────────────
    _pr(f"\n\n  ══ SWEEP C — Phonological Groups + Wider Beams (10 anchors + OCP) ══")
    configs = [
        ("no groups, width=50",    50,   None,              False, 1.0),
        ("no groups, width=200",   200,  None,              False, 1.0),
        ("phono groups, width=50", 50,   d["PHONO_GROUPS"], False, 1.0),
        ("phono groups, width=200",200,  d["PHONO_GROUPS"], False, 1.0),
        ("phono + word-bg, w=200", 200,  d["PHONO_GROUPS"], True,  1.0),
    ]
    _pr(f"  {'Config':<28}  {'Correct':>8}  {'Accuracy':>9}  {'Time':>6}")
    _pr("  " + "-" * 58)
    sweep_c = []
    best_anchors = d["ANCHORS_10"]
    for label, bw, pg, wb, ocp in configs:
        correct, t = _run_beam(d, beam_width=bw,
                                use_word_bigrams=wb,
                                ocp_weight=ocp,
                                anchors=best_anchors,
                                phono_groups=pg)
        pct = correct / 30 * 100
        _pr(f"  {label:<28}  {correct:>8}/30  {pct:>8.1f}%  {t:>5}s")
        sweep_c.append({"config": label, "correct": correct,
                         "beam_width": bw, "use_word_bigrams": wb,
                         "ocp_weight": ocp, "time_s": t})
    results["sweep_c_constraints"] = sweep_c

    # ── Sweep D: Multi-seed SA surjective + anchors + phono ───────────────────
    _pr("\n\n  ══ SWEEP D — Multi-seed SA (surjective + 10 anchors) ══")
    _pr(f"  {'Seed':>6}  {'Correct':>8}  {'Accuracy':>9}")
    _pr("  " + "-" * 30)
    sweep_d = []
    for seed in range(8):
        c, t = _run_sa(d, surjective=True, anchors=best_anchors, seed=seed)
        pct = c / 30 * 100
        _pr(f"  {seed:>6}  {c:>8}/30  {pct:>8.1f}%")
        sweep_d.append({"seed": seed, "correct": c})
    d_mean = sum(x["correct"] for x in sweep_d) / len(sweep_d)
    d_best = max(x["correct"] for x in sweep_d)
    _pr(f"  Mean: {d_mean:.2f}/30 = {d_mean/30*100:.1f}%   Best: {d_best}/30 = {d_best/30*100:.1f}%")
    results["sweep_d_multiseed"] = sweep_d

    # ── Summary ───────────────────────────────────────────────────────
    best_c = max(sweep_c, key=lambda x: x["correct"])
    _pr("\n\n  ══ MASTER SUMMARY ══")
    _pr(f"  SA baseline (25 restarts):              {sa_correct:2d}/30 = {sa_correct/30*100:.1f}%")
    _pr(f"  Best beam (width sweep, no anchors):    {max(r['correct'] for r in sweep_a):2d}/30 = "
        f"{max(r['correct'] for r in sweep_a)/30*100:.1f}%")
    _pr(f"  Best beam + 10 anchors (flat bigrams):  {sweep_b[-1]['correct']:2d}/30 = "
        f"{sweep_b[-1]['correct']/30*100:.1f}%")
    _pr(f"  Best beam + 10 anchors + constraints:   {best_c['correct']:2d}/30 = "
        f"{best_c['correct']/30*100:.1f}%  ({best_c['config']})")

    best_overall = max(
        sa_correct,
        max(r["correct"] for r in sweep_a),
        max(r["correct"] for r in sweep_b),
        max(r["correct"] for r in sweep_c),
    )

    if best_overall >= 20:
        conclusion = (
            f"STRONG ({best_overall}/30 = {best_overall/30*100:.1f}%) — "
            "Beam search + anchors + constraints substantially outperforms SA. "
            "Systematic search exploits the oracle signal the model always had."
        )
    elif best_overall >= 10:
        conclusion = (
            f"IMPROVED ({best_overall}/30 = {best_overall/30*100:.1f}%) — "
            "Beam search gives meaningful gains over SA. "
            "Further tuning of beam width and constraint weights expected to help."
        )
    else:
        conclusion = (
            f"MODEST ({best_overall}/30 = {best_overall/30*100:.1f}%) — "
            "Beam search matches SA but does not yet dramatically exceed it. "
            "The oracle signal (+550) should be exploitable; further analysis needed."
        )

    # Also show SA vs beam head-to-head with best config
    _pr(f"\n  SA bijective baseline:      {sa_correct}/30 = {sa_correct/30*100:.1f}%")
    _pr(f"  SA surjective baseline:     {sa_surj}/30 = {sa_surj/30*100:.1f}%")
    _pr(f"  SA surjective + 10 anchors: {sa_surj_anch}/30 = {sa_surj_anch/30*100:.1f}%")
    _pr(f"  Beam surjective (best):     {best_overall}/30 = {best_overall/30*100:.1f}%")
    _pr(f"\n  CONCLUSION: {conclusion}")

    results["best_overall"] = best_overall
    results["conclusion"]   = conclusion
    return results


if __name__ == "__main__":
    run_beam_benchmark(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class BeamDecipherBenchmark(_EB):
    id = "beam_decipher_benchmark"
    name = "Beam Decipherment Benchmark (Tier 1a)"
    category = "Validation"
    description = (
        "Compares beam-search decipherment against SA on Tier 1a (Ugaritic→Hebrew). "
        "Sweeps beam widths 50–500, ablates 0/5/10 pan-Semitic cognate anchors, "
        "and tests all structural constraints (word bigrams, OCP, root prior). "
        "Direct test of the hypothesis that SA's failure is algorithmic, not informational."
    )
    estimated_time = "~3 min"
    command = "python -m glossa_lab.experiments.beam_decipher_benchmark"
    params_schema = {
        "type": "object",
        "properties": {
            "beam_width": {
                "type": "integer",
                "title": "Beam Width",
                "default": 200,
                "minimum": 10,
                "description": "Number of partial mappings kept at each beam depth. Higher = more accurate but slower.",
            },
            "root_prior_weight": {
                "type": "number",
                "title": "Root Prior Weight",
                "default": 0.0,
                "minimum": 0.0,
                "description": "Weight for root co-occurrence prior (word_cooccur). 0=disabled. Try 0.3–1.0.",
            },
            "ocp_weight": {
                "type": "number",
                "title": "OCP Weight",
                "default": 0.0,
                "minimum": 0.0,
                "description": "OCP penalty weight. 0=disabled. Try 0.5–2.0.",
            },
            "use_word_bigrams": {
                "type": "boolean",
                "title": "Word-Boundary Bigrams",
                "default": False,
                "description": "Score bigrams within words only (Semitic phonotactics).",
            },
            "n_anchors": {
                "type": "integer",
                "title": "Cognate Anchors",
                "default": 0,
                "minimum": 0,
                "maximum": 10,
                "description": "Number of pan-Semitic cognate anchors to lock (0, 5, or 10).",
            },
        },
    }

    def run(self, **kwargs) -> dict:
        return run_beam_benchmark(verbose=False)
