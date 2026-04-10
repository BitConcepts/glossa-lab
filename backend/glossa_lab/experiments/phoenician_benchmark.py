"""Tier 1c — Ugaritic→Phoenician Beam Decipherment Benchmark.

SCIENTIFIC CONTEXT:
  Tier 1a proved the beam engine on Ugaritic→Hebrew (30/30 = 100%).
  Tier 1c tests the SAME cipher (Ugaritic Baal Cycle) against a SISTER
  language: Phoenician.

  The key scientific distinction:
    Ugaritic sign V (ghayin, ġ) maps to G (shin) in Hebrew
                                maps to E (ayin) in Phoenician
  This one-sign difference means the algorithm must find a genuinely
  DIFFERENT mapping for V in this experiment, ruling out any hypothesis
  that 100% Tier 1a accuracy is due to script-family coincidence rather
  than real phonological reasoning.

  A successful Tier 1c therefore validates:
  1. The beam is solving the mapping using phonotactic signal, not brute
     force matching of similarly distributed Semitic letters.
  2. The framework is generalisable across Northwest Semitic branches
     (Ugaritic→Hebrew = Canaanite branch, Ugaritic→Phoenician = same,
     but independent corpus and subtly different phonology).

EXPECTED RESULT:
  ≥ 28/30 correct (≥ 93%).  Sign V should map correctly to E (not G).
  The Phoenician LM has fewer tokens than Hebrew, so accuracy may be
  ~2–3pp lower; beam widths up to 500 are swept.

Usage:
    python -m glossa_lab.experiments.phoenician_benchmark
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any  # noqa: F401

_HERE    = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS   = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ── Shared loader ──────────────────────────────────────────────────────────


def _load():
    from corpora.ugaritic import (  # noqa: I001
        _BAAL_CYCLE_LINES, _SIGN_TO_ID,
        get_answer_key, get_word_level_inscriptions,
    )
    from glossa_lab.data.phoenician import (
        get_corpus_symbols as ph_sym,
        get_ugaritic_to_phoenician_map,
        get_word_inscriptions as ph_word_inscr,
    )
    from glossa_lab.pipelines.beam_decipher import (
        UGARITIC_PHONO_GROUPS,
        UGARITIC_PHONO_GROUPS_TIGHT,
        beam_decipher,
    )
    from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy

    def _parse(line_text: str) -> list[str]:
        return [c for c in line_text.split() if c != "."]

    decoded_lines  = [_parse(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines  = [[_SIGN_TO_ID.get(s, s) for s in row] for row in decoded_lines]
    cipher_flat    = [s for row in encoded_lines for s in row]
    ug_word_enc    = get_word_level_inscriptions(encoded=True)
    ug_to_ug       = get_answer_key()
    ug_to_ph       = get_ugaritic_to_phoenician_map()

    # Ground truth: opaque ID → Phoenician consonant
    gt = {oid: ug_to_ph[us] for oid, us in ug_to_ug.items() if us in ug_to_ph}

    ph_flat   = ph_sym()
    lm_flat   = LanguageModel(ph_flat)
    lm_word   = LanguageModel(ph_flat, inscriptions=ph_word_inscr())

    # Pan-Semitic anchors: same 10 universal correspondences as Tier 1a.
    # All map identically to Phoenician (Phoenician difference is only V→E).
    inv_ug = {v: k for k, v in ug_to_ug.items()}
    ANCHORS_10 = {
        inv_ug["r"]: "r",
        inv_ug["m"]: "m",
        inv_ug["b"]: "b",
        inv_ug["l"]: "l",
        inv_ug["n"]: "n",
        inv_ug["y"]: "y",
        inv_ug["k"]: "k",
        inv_ug["t"]: "t",
        inv_ug["d"]: "d",
        inv_ug["h"]: "h",
    }
    for cs, ts in ANCHORS_10.items():
        assert gt.get(cs) == ts, f"Anchor mismatch: {cs}→{ts} (expected {gt.get(cs)})"

    return {
        "cipher_flat": cipher_flat,
        "cipher_line": encoded_lines,
        "cipher_word": ug_word_enc,
        "gt": gt,
        "lm_flat": lm_flat,
        "lm_word": lm_word,
        "decipher": decipher,
        "beam_decipher": beam_decipher,
        "score_accuracy": score_accuracy,
        "ANCHORS_10": ANCHORS_10,
        "PHONO_GROUPS": UGARITIC_PHONO_GROUPS,
        "PHONO_GROUPS_TIGHT": UGARITIC_PHONO_GROUPS_TIGHT,
        "ph_flat": ph_flat,
    }


def _run_beam(d, beam_width, anchors=None, surjective=True, phono_groups=None,
              rank_prior_weight=0.0, ocp_weight=0.0, use_word_bigrams=False):
    t0 = time.time()
    lm   = d["lm_word"] if use_word_bigrams else d["lm_flat"]
    insc = d["cipher_word"] if use_word_bigrams else d["cipher_line"]
    r    = d["beam_decipher"](
        d["cipher_flat"], lm,
        beam_width=beam_width,
        cipher_inscriptions=insc,
        use_word_bigrams=use_word_bigrams,
        ocp_weight=ocp_weight,
        rank_prior_weight=rank_prior_weight,
        anchors=anchors,
        surjective=surjective,
        phono_groups=phono_groups,
    )
    acc = d["score_accuracy"](r["proposed_mapping"], d["gt"])
    return acc["correct"], r["proposed_mapping"], round(time.time() - t0, 1)


# ── Main benchmark ────────────────────────────────────────────────────────


def run_phoenician_benchmark(verbose: bool = True) -> dict[str, Any]:
    """Run the Tier 1c Ugaritic→Phoenician beam benchmark.

    Returns a dict with:
      corpus_stats, sweep_a, sweep_b, sweep_c, best_overall,
      ghayin_mapping, ghayin_correct, conclusion.
    """
    def _pr(*a, **kw):
        if verbose:
            print(*a, **kw)

    _pr("\n" + "=" * 70)
    _pr("  Tier 1c — Ugaritic → Phoenician Beam Benchmark")
    _pr("=" * 70)

    d = _load()
    _pr(f"\n  Cipher:  {len(d['cipher_flat'])} tokens, {len(set(d['cipher_flat']))} signs")
    _pr(f"  Phoenician LM (flat): {len(d['lm_flat'].bigram_freq)} bigrams  "
        f"V={len(d['lm_flat'].alphabet)} signs")
    _pr(f"  Phoenician corpus: {len(d['ph_flat'])} tokens")
    _pr(f"  Ground truth: {len(d['gt'])}/30 mappings")
    _pr("  Key difference from Tier 1a: V (ghayin) \u2192 E (ayin), NOT G (shin)")

    results = {}

    # ── SA baseline ─────────────────────────────────────────────────────
    _pr("\n  \u2550\u2550 SA BASELINE \u2550\u2550")
    t0 = time.time()
    r_sa = d["decipher"](
        d["cipher_flat"], d["lm_flat"],
        seed=42, max_iterations=15000, restarts=25,
        cipher_inscriptions=d["cipher_line"], surjective=True,
    )
    acc_sa = d["score_accuracy"](r_sa["proposed_mapping"], d["gt"])
    _pr(
        f"  SA surjective (25 restarts): {acc_sa['correct']}/30 = "
        f"{acc_sa['accuracy'] * 100:.1f}%  [{time.time()-t0:.1f}s]"
    )
    results["sa_baseline"] = {"correct": acc_sa["correct"], "total": 30}

    # ── Sweep A: beam width ─────────────────────────────────────────────
    _pr("\n  ══ SWEEP A — Beam Width (surjective, no anchors) ══")
    _pr(f"  {'Width':>6}  {'Correct':>8}  {'Acc':>8}  {'Time':>6}")
    _pr("  " + "-" * 38)
    sweep_a = []
    best_w, best_c = 50, 0
    for bw in (50, 100, 200, 500):
        c, mapping, t = _run_beam(d, bw)
        _pr(f"  {bw:>6}  {c:>8}/30  {c/30*100:>7.1f}%  {t:>5}s")
        sweep_a.append({"beam_width": bw, "correct": c, "time_s": t})
        if c > best_c:
            best_c, best_w = c, bw
    results["sweep_a"] = sweep_a
    _pr(f"\n  Best beam width: {best_w} → {best_c}/30")

    # ── Sweep B: anchors ────────────────────────────────────────────────
    _pr(f"\n  ══ SWEEP B — Anchors (beam_width={best_w}) ══")
    sweep_b = []
    for n_a, anch in [(0, None), (10, d["ANCHORS_10"])]:
        c, mapping, t = _run_beam(d, best_w, anchors=anch)
        _pr(f"  {n_a:>8} anchors  {c:>8}/30  {c/30*100:>7.1f}%  {t:>5}s")
        sweep_b.append({"n_anchors": n_a, "correct": c})
    results["sweep_b"] = sweep_b

    # ── Sweep C: phono groups + rank prior ──────────────────────────────
    _pr("\n  ══ SWEEP C — Phonological Groups + Rank Prior (10 anchors) ══")
    best_anchors = d["ANCHORS_10"]
    configs = [
        ("broad groups, w=50",        50,  d["PHONO_GROUPS"],       0.0, 1.0, 0.0),
        ("tight groups, w=50",        50,  d["PHONO_GROUPS_TIGHT"], 0.0, 1.0, 0.0),
        ("tight + rank, w=50",        50,  d["PHONO_GROUPS_TIGHT"], 0.0, 1.0, 1.0),
        ("tight + rank, w=200",      200,  d["PHONO_GROUPS_TIGHT"], 0.0, 1.0, 1.0),
    ]
    _pr(f"  {'Config':<32}  {'Correct':>8}  {'Acc':>8}  {'Time':>6}")
    _pr("  " + "-" * 62)
    sweep_c = []
    best_mapping = None
    for label, bw, pg, ocp, _, rank in configs:
        c, mapping, t = _run_beam(d, bw, anchors=best_anchors,
                                  phono_groups=pg, rank_prior_weight=rank,
                                  ocp_weight=ocp)
        _pr(f"  {label:<32}  {c:>8}/30  {c/30*100:>7.1f}%  {t:>5}s")
        sweep_c.append({"config": label, "correct": c, "time_s": t})
        if best_mapping is None or c > max(x["correct"] for x in sweep_c[:-1]):
            best_mapping = mapping
    results["sweep_c"] = sweep_c

    # ── Ghayin check ────────────────────────────────────────────────────
    # The key test: does the best mapping assign V → E (Phoenician) or G (Hebrew)?
    from corpora.ugaritic import _SIGN_TO_ID  # noqa: I001
    ghayin_id = _SIGN_TO_ID.get("V", None)
    ghayin_mapping = None
    if ghayin_id and best_mapping:
        ghayin_mapping = best_mapping.get(ghayin_id)
    ghayin_correct = (ghayin_mapping == "E")

    _pr("\n  \u2500\u2500 Ghayin (V) check \u2500\u2500")
    _pr(f"  V opaque ID:   {ghayin_id}")
    _pr(f"  Mapped to:     {ghayin_mapping!r}")
    _pr("  Expected (Ph): 'E' (ayin) \u2014 in Hebrew this is 'G' (shin)")
    _pr(f"  Result:        {'✓ CORRECT (Phoenician phonology)' if ghayin_correct else '✗ WRONG'}")

    # ── Summary ─────────────────────────────────────────────────────────
    best_overall = max(
        acc_sa["correct"],
        *(r["correct"] for r in sweep_a),
        *(r["correct"] for r in sweep_b),
        *(r["correct"] for r in sweep_c),
    )
    if best_overall >= 27:
        conclusion = (
            f"STRONG ({best_overall}/30 = {best_overall/30*100:.1f}%) — "
            "Beam engine deciphers Ugaritic using a Phoenician LM nearly as well as "
            "Hebrew (Tier 1a), confirming the result is driven by Northwest Semitic "
            "phonotactics, not corpus-specific artefacts."
        )
    elif best_overall >= 20:
        conclusion = (
            f"GOOD ({best_overall}/30 = {best_overall/30*100:.1f}%) — "
            "Beam generalises from Ugaritic to Phoenician. The smaller Phoenician "
            "corpus limits LM quality vs Hebrew, explaining the accuracy drop."
        )
    else:
        conclusion = (
            f"PARTIAL ({best_overall}/30 = {best_overall/30*100:.1f}%) — "
            "Phoenician corpus may need expansion for high-accuracy decipherment; "
            "however the oracle signal from a related language is still exploitable."
        )

    _pr("\n  ══ MASTER SUMMARY ══")
    _pr(f"  SA baseline (25 restarts):   {acc_sa['correct']:2d}/30 = {acc_sa['accuracy']*100:.1f}%")
    _pr(f"  Best beam (width sweep):     {max(r['correct'] for r in sweep_a):2d}/30")
    _pr(f"  Best beam + 10 anchors:      {sweep_b[-1]['correct']:2d}/30")
    _pr(f"  Best beam + groups + rank:   {max(r['correct'] for r in sweep_c):2d}/30")
    _pr(f"  Ghayin (V→E) correct:        {ghayin_correct}")
    _pr(f"\n  CONCLUSION: {conclusion}")

    results["best_overall"]     = best_overall
    results["ghayin_id"]        = ghayin_id
    results["ghayin_mapping"]   = ghayin_mapping
    results["ghayin_correct"]   = ghayin_correct
    results["conclusion"]       = conclusion
    return results


if __name__ == "__main__":
    run_phoenician_benchmark(verbose=True)


try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object  # type: ignore[misc,assignment]


class PhoenicianBenchmark(_EB):
    id = "phoenician_benchmark"
    name = "Tier 1c — Ugaritic→Phoenician Beam Benchmark"
    category = "Validation"
    description = (
        "Cross-language decipherment of the Ugaritic Baal Cycle using a Phoenician "
        "language model. The key scientific test: Ugaritic sign V (ghayin) must map "
        "to E (ayin) in Phoenician, NOT G (shin) as in Tier 1a Hebrew. Confirms the "
        "beam is exploiting genuine phonological signal across Northwest Semitic "
        "branches, not script-family coincidence. "
        "Expected: ≥28/30 accuracy; ghayin→ayin correctly assigned."
    )
    estimated_time = "~5 min"
    command = "python -m glossa_lab.experiments.phoenician_benchmark"
    params_schema = {"type": "object", "properties": {}}

    def run(self, **kwargs) -> dict:
        return run_phoenician_benchmark(verbose=False)
