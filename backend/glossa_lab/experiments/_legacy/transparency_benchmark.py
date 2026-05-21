"""Decipherment Transparency Benchmark.

Provides a CLEAN SEPARATION of what the model achieves purely statistically
vs what it achieves through researcher-injected hypotheses.

Every published decipherment result should include a transparency row alongside
its headline accuracy number.  This experiment generates that row.

FOUR CONTRIBUTION TIERS:
  Tier 0 — Statistical floor
    Pure frequency-rank seed.  No optimizer, no priors, no anchors.
    What unigram frequency matching alone achieves.
    This is the baseline that ANY approach must beat to be meaningful.

  Tier 1 — + Optimizer (SA/beam on bigrams)
    Frequency seed + SA/beam search optimising bigram log-likelihood.
    No linguistic priors, no anchors.
    What the ALGORITHM contributes beyond frequency matching.

  Tier 2 — + Linguistic priors
    All structural constraints enabled:
      word-boundary bigrams, OCP penalty, positional weight, root co-occurrence.
    No anchors.
    What DOMAIN KNOWLEDGE about Semitic phonology contributes.

  Tier 3 — + Human knowledge (anchors)
    Full prior stack + pan-Semitic cognate anchors.
    What RESEARCHER INJECTION of known correspondences contributes.

For cross-language decipherment (Ugaritic → Hebrew), Tier 3 with beam +
tight phonological groups achieves 30/30 = 100%.  The transparency table
shows exactly how much of that performance comes from each tier.

The transparency table format:
  Tier | Method              | Accuracy | Oracle Δ | What was injected
  ─────┼─────────────────────┼──────────┼──────────┼──────────────────────
  T0   | Freq-rank only      | N/30     | N/A      | Nothing (pure statistics)
  T1   | + Bigram SA/beam    | N/30     | +Δ1      | Bigram n-gram statistics
  T2   | + Ling. priors      | N/30     | +Δ2      | OCP, positional, word-bigrams
  T3   | + Anchors           | N/30     | +Δ3      | Pan-Semitic cognate pairs

Usage:
    python -m glossa_lab.experiments.transparency_benchmark
"""
from __future__ import annotations

import os
import sys
from collections import Counter, defaultdict
from typing import Any

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load() -> dict[str, Any]:
    from corpora.ugaritic import (
        _BAAL_CYCLE_LINES,
        _SIGN_TO_ID,
        get_answer_key,
        get_word_level_inscriptions,
    )

    from glossa_lab.data.old_hebrew import (
        get_corpus_inscriptions as heb_line_inscr,
    )
    from glossa_lab.data.old_hebrew import (
        get_corpus_symbols as heb_sym,
    )
    from glossa_lab.data.old_hebrew import (
        get_ugaritic_to_hebrew_map,
    )
    from glossa_lab.data.old_hebrew import (
        get_word_inscriptions as heb_word_inscr,
    )
    from glossa_lab.pipelines.beam_decipher import UGARITIC_PHONO_GROUPS_TIGHT, beam_decipher
    from glossa_lab.pipelines.decipher import (
        LanguageModel,
        _score_mapping,
        decipher,
        score_accuracy,
    )

    def _parse(line: str) -> list[str]:
        return [ch for ch in line.split() if ch != "."]

    decoded_lines  = [_parse(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines  = [[_SIGN_TO_ID.get(s, s) for s in l] for l in decoded_lines]
    cipher_flat    = [s for l in encoded_lines for s in l]
    ug_words_enc   = get_word_level_inscriptions(encoded=True)

    ug_to_ug  = get_answer_key()
    ug_to_heb = get_ugaritic_to_hebrew_map()
    gt        = {oid: ug_to_heb[us] for oid, us in ug_to_ug.items() if us in ug_to_heb}

    heb_flat = heb_sym()
    lm_flat  = LanguageModel(heb_flat)
    lm_word  = LanguageModel(heb_flat, inscriptions=heb_word_inscr())
    lm_line  = LanguageModel(heb_flat, inscriptions=heb_line_inscr())

    inv_ug = {v: k for k, v in ug_to_ug.items()}
    anchors_10 = {
        inv_ug["r"]: "r", inv_ug["m"]: "m", inv_ug["b"]: "b",
        inv_ug["l"]: "l", inv_ug["n"]: "n", inv_ug["y"]: "y",
        inv_ug["k"]: "k", inv_ug["t"]: "t", inv_ug["d"]: "d",
        inv_ug["h"]: "h",
    }

    return {
        "cipher_flat":       cipher_flat,
        "cipher_line_inscr": encoded_lines,
        "cipher_word_inscr": ug_words_enc,
        "gt":                gt,
        "lm_flat":           lm_flat,
        "lm_word":           lm_word,
        "lm_line":           lm_line,
        "anchors_10":        anchors_10,
        "phono_tight":       UGARITIC_PHONO_GROUPS_TIGHT,
        "decipher":          decipher,
        "beam_decipher":     beam_decipher,
        "score_accuracy":    score_accuracy,
        "_score_mapping":    _score_mapping,
    }


def _freq_rank_mapping(cipher_flat: list[str], target_model: Any) -> dict[str, str]:
    counts  = Counter(cipher_flat)
    ranked  = [s for s, _ in counts.most_common()]
    targets = list(target_model.ranked[: len(ranked)])
    while len(targets) < len(ranked):
        targets.append(f"?{len(targets)}")
    return dict(zip(ranked, targets))


def _oracle_score(
    d: dict, lm, cipher_inscr, mapping,
    use_word_bigrams=False, ocp_weight=0.0,
    positional_weight=0.005, root_prior_weight=0.0,
) -> float:
    _score_mapping = d["_score_mapping"]
    cipher_flat    = d["cipher_flat"]

    pos_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"initial": 0, "medial": 0, "terminal": 0}
    )
    for insc in cipher_inscr:
        if len(insc) >= 2:
            pos_counts[insc[0]]["initial"]  += 1
            pos_counts[insc[-1]]["terminal"] += 1
            for s in insc[1:-1]:
                pos_counts[s]["medial"] += 1
    cipher_pos = {
        sign: {k: v / (sum(pc.values()) or 1) for k, v in pc.items()}
        for sign, pc in pos_counts.items()
    }

    return _score_mapping(
        cipher_flat, mapping, lm, cipher_pos,
        use_word_bigrams=use_word_bigrams,
        cipher_inscriptions=cipher_inscr,
        ocp_weight=ocp_weight,
        positional_weight=positional_weight,
        root_prior_weight=root_prior_weight,
    )


def run_transparency_benchmark(verbose: bool = True) -> dict[str, Any]:
    def _pr(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    _pr("\n" + "=" * 70)
    _pr("  Decipherment Transparency Benchmark")
    _pr("  Four-Tier Attribution — Ugaritic → Hebrew (Tier 1a)")
    _pr("=" * 70)
    _pr("""
  Separates the contributions of:
    T0  Pure frequency statistics (floor)
    T1  + Bigram optimizer (algorithm contribution)
    T2  + Linguistic priors (domain knowledge contribution)
    T3  + Human anchors (researcher injection contribution)
""")

    d    = _load()
    n_gt = len(d["gt"])
    gt   = d["gt"]

    _pr(f"  Corpus: {len(d['cipher_flat'])} tokens  Ground truth: {n_gt} mappings")

    tiers = []

    # ── T0: Frequency-rank floor (no optimizer) ───────────────────────
    _pr("\n  ── Tier 0: Frequency-rank seed (statistical floor) ──")
    freq_map    = _freq_rank_mapping(d["cipher_flat"], d["lm_flat"])
    acc_t0      = d["score_accuracy"](freq_map, gt)
    # Oracle delta meaningless at T0 (no optimizer ran)
    _pr(f"  Accuracy: {acc_t0['correct']}/{n_gt} = {acc_t0['correct']/n_gt*100:.1f}%")
    _pr("  Injected: nothing (pure frequency statistics)")
    tiers.append({
        "tier": 0, "label": "T0 — Statistical floor",
        "method": "Frequency-rank seed only",
        "accuracy": acc_t0["correct"],
        "oracle_delta": None,
        "injected": "Nothing — pure bigram/unigram statistics",
    })

    # ── T1: + Bigram SA, no priors ────────────────────────────────────
    _pr("\n  ── Tier 1: + Bigram optimizer (SA surjective, no priors) ──")
    r_t1 = d["decipher"](
        d["cipher_flat"], d["lm_flat"],
        seed=42, max_iterations=15000, restarts=15,
        cipher_inscriptions=d["cipher_line_inscr"],
        surjective=True,
        ocp_weight=0.0, positional_weight=0.0, root_prior_weight=0.0,
    )
    acc_t1  = d["score_accuracy"](r_t1["proposed_mapping"], gt)
    sc_t1   = _oracle_score(d, d["lm_flat"], d["cipher_line_inscr"], r_t1["proposed_mapping"])
    sc_gt_t1 = _oracle_score(d, d["lm_flat"], d["cipher_line_inscr"], gt)
    delta_t1 = sc_gt_t1 - sc_t1
    _pr(f"  Accuracy: {acc_t1['correct']}/{n_gt} = {acc_t1['correct']/n_gt*100:.1f}%")
    _pr(f"  Oracle Δ: {delta_t1:+.1f}")
    _pr("  Injected: bigram statistics from Hebrew corpus (no Semitic-specific constraints)")
    tiers.append({
        "tier": 1, "label": "T1 — + Optimizer",
        "method": "SA surjective (bigrams only)",
        "accuracy": acc_t1["correct"],
        "oracle_delta": round(delta_t1, 1),
        "injected": "Bigram statistics from Hebrew corpus",
    })

    # ── T2: + Linguistic priors, no anchors ──────────────────────────
    _pr("\n  ── Tier 2: + Linguistic priors (all, no anchors) ──")
    r_t2 = d["decipher"](
        d["cipher_flat"], d["lm_word"],
        seed=42, max_iterations=15000, restarts=15,
        cipher_inscriptions=d["cipher_word_inscr"],
        surjective=True,
        use_word_bigrams=True, ocp_weight=1.0,
        positional_weight=0.02, root_prior_weight=0.5,
    )
    acc_t2   = d["score_accuracy"](r_t2["proposed_mapping"], gt)
    sc_t2    = _oracle_score(d, d["lm_word"], d["cipher_word_inscr"],
                             r_t2["proposed_mapping"],
                             use_word_bigrams=True, ocp_weight=1.0,
                             positional_weight=0.02, root_prior_weight=0.5)
    sc_gt_t2 = _oracle_score(d, d["lm_word"], d["cipher_word_inscr"], gt,
                              use_word_bigrams=True, ocp_weight=1.0,
                              positional_weight=0.02, root_prior_weight=0.5)
    delta_t2 = sc_gt_t2 - sc_t2
    _pr(f"  Accuracy: {acc_t2['correct']}/{n_gt} = {acc_t2['correct']/n_gt*100:.1f}%")
    _pr(f"  Oracle Δ: {delta_t2:+.1f}")
    _pr("  Injected: OCP, positional, word-boundary bigrams, root co-occurrence prior")
    tiers.append({
        "tier": 2, "label": "T2 — + Linguistic priors",
        "method": "SA + word-bigrams + OCP + positional + root-prior",
        "accuracy": acc_t2["correct"],
        "oracle_delta": round(delta_t2, 1),
        "injected": "OCP + positional + word-bigrams + root co-occurrence (Semitic phonology)",
    })

    # ── T3: + Anchors (beam + tight phono groups) ────────────────────
    _pr("\n  ── Tier 3: + Human anchors (beam + tight phono groups) ──")
    r_t3 = d["beam_decipher"](
        d["cipher_flat"], d["lm_word"],
        beam_width=50,
        cipher_inscriptions=d["cipher_word_inscr"],
        anchors=d["anchors_10"],
        phono_groups=d["phono_tight"],
        surjective=True,
    )
    acc_t3   = d["score_accuracy"](r_t3["proposed_mapping"], gt)
    sc_t3    = _oracle_score(d, d["lm_word"], d["cipher_word_inscr"], r_t3["proposed_mapping"])
    sc_gt_t3 = _oracle_score(d, d["lm_word"], d["cipher_word_inscr"], gt)
    delta_t3 = sc_gt_t3 - sc_t3
    _pr(f"  Accuracy: {acc_t3['correct']}/{n_gt} = {acc_t3['correct']/n_gt*100:.1f}%")
    _pr(f"  Oracle Δ: {delta_t3:+.1f}")
    _pr("  Injected: 10 pan-Semitic cognate anchors + tight phonological group constraints")
    tiers.append({
        "tier": 3, "label": "T3 — + Human anchors",
        "method": "Beam + tight phono groups + 10 pan-Semitic anchors",
        "accuracy": acc_t3["correct"],
        "oracle_delta": round(delta_t3, 1),
        "injected": "10 pan-Semitic cognate anchors (Segert 1984; Huehnergard 2012) + phono groups",
    })

    # ── Attribution table ──────────────────────────────────────────────
    _pr("\n\n" + "=" * 70)
    _pr("  TRANSPARENCY TABLE — Ugaritic → Hebrew")
    _pr("=" * 70)
    _pr(f"\n  {'Tier':<4}  {'Method':<38}  {'Accuracy':>8}  {'Oracle Δ':>10}")
    _pr("  " + "-" * 68)
    for t in tiers:
        delta_str = f"{t['oracle_delta']:+.0f}" if t["oracle_delta"] is not None else "     N/A"
        _pr(f"  {t['label']:<42}  {t['accuracy']:2d}/{n_gt}={t['accuracy']/n_gt*100:4.1f}%  {delta_str:>10}")
        _pr(f"       Injected: {t['injected']}")
    _pr()

    # Per-tier attribution deltas
    prev = tiers[0]["accuracy"]
    _pr("  ── Attribution (incremental accuracy lift per tier) ──")
    for t in tiers[1:]:
        lift = t["accuracy"] - prev
        sign = "+" if lift >= 0 else ""
        _pr(f"  {t['label']:<42}  {sign}{lift:+d} signs")
        prev = t["accuracy"]

    t0_acc = tiers[0]["accuracy"]
    t3_acc = tiers[3]["accuracy"]
    alg_frac = (tiers[1]["accuracy"] - t0_acc) / max(t3_acc - t0_acc, 1) * 100
    pri_frac = (tiers[2]["accuracy"] - tiers[1]["accuracy"]) / max(t3_acc - t0_acc, 1) * 100
    anc_frac = (t3_acc - tiers[2]["accuracy"]) / max(t3_acc - t0_acc, 1) * 100

    conclusion = (
        f"Tier 3 (full stack) achieves {t3_acc}/{n_gt} = {t3_acc/n_gt*100:.1f}%. "
        f"Attribution of improvement above floor ({t0_acc}/{n_gt}): "
        f"algorithm={alg_frac:.0f}%, linguistic priors={pri_frac:.0f}%, "
        f"human anchors={anc_frac:.0f}%. "
        "This table should accompany every published benchmark result to "
        "clearly separate model capability from hypothesis injection."
    )
    _pr(f"\n  CONCLUSION: {conclusion}")

    return {
        "tiers":       tiers,
        "conclusion":  conclusion,
    }


if __name__ == "__main__":
    run_transparency_benchmark(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class TransparencyBenchmark(_EB):
    id = "transparency_benchmark"
    name = "Decipherment Transparency Benchmark"
    category = "Validation"
    description = (
        "Produces the four-tier attribution table separating model capability "
        "from hypothesis injection for the Ugaritic→Hebrew reference task. "
        "T0: frequency floor. T1: + bigram optimizer. T2: + linguistic priors. "
        "T3: + researcher anchors. "
        "Every published benchmark result should include this table."
    )
    estimated_time = "~5 min"
    command = "python -m glossa_lab.experiments.transparency_benchmark"
    params_schema: dict = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return run_transparency_benchmark(verbose=False)
