"""Phase-30 atomic-node implementations.

Phase-30 follow-ups to the Phase-29 verdict and the Phase-30a length-bin
spectral run:

  Phase-30b — LengthCohortReverseJanabiyahSearch
      Re-runs the Phase-29 ReverseJanabiyahSearchV3 against ePSD2 personal
      names but stratifies the candidate space by syllable count cohort
      (3-4, 5-6, 7-8, 9+). Tests whether the Janabiyah miin-pattern signal
      concentrates in any specific length cohort -- a length-aware version
      of the Phase-29d test. If signal stays flat across cohorts the
      contact-zone hypothesis loses one more degree of freedom.

  Phase-30c — ShufflePermutationNull
      Given a `stratifications` dict from LengthStratifier, computes a
      null distribution of bigram-transition spectral gaps per bin via
      N permutations (default 200). Permutation method: re-sample the
      bin's flat token list into pseudo-sequences with the same length
      profile but the temporal order destroyed. For each null draw,
      compute the spectral gap exactly as BinSpectralFingerprint does.
      Reports per-bin observed gap, null mean / sd, and one-sided p-value
      P(null >= observed) -- so the Phase-30a "all bins are gap=0"
      finding can be reported with statistical context.

Both atomic nodes reuse Phase-20 / Phase-29 helper logic (segment parsing,
spectral gap, bigram transition matrix) where it already exists.
"""

from __future__ import annotations

import random
import re
from collections import Counter, defaultdict
from typing import Any


# ---------------------------------------------------------------------------
#  Phase-30b: length-cohort reverse Janabiyah search
# ---------------------------------------------------------------------------


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


def _pn_to_segments(forms: list[str]) -> list[list[str]]:
    """Same segmentation rules as Phase-29 _epsd_pn_to_segments."""
    out: list[list[str]] = []
    for f in forms or []:
        if not f:
            continue
        clean = re.sub(r"\{[^}]+\}", "", str(f).lower())
        parts = [p for p in re.split(r"[-]+", clean) if p and not p.isspace()]
        parts = [re.sub(r"[0-9]+$", "", p) for p in parts]
        parts = [p for p in parts if p]
        if parts:
            out.append(parts)
    return out


def _length_cohort_reverse_janabiyah(inputs: dict, params: dict) -> dict:
    """Length-cohorted reverse Janabiyah search.

    Inputs match Phase-29's M77ReverseJanabiyahSearchV3:
      epsd2_personal_names  list[dict]   ePSD2 personal-name records
      janabiyah_reading      dict        7-sign Janabiyah seal reading
      phoneme_map            dict        Parpola sign->phoneme map
      allograph_families     dict        Mahadevan sign-allograph families

    Params:
      cohorts        list[[lo, hi]]   default [[3,4],[5,6],[7,8],[9,99]]
      min_icount     int              minimum ePSD2 instance count to include
      top_k          int              top matches reported per cohort

    The Janabiyah seal has 7 sign positions with miin-tokens expected at
    positions 1, 3, 6. We keep that scoring rule from Phase-29 and ONLY
    stratify the candidate space (ePSD2 PN segment count). For each cohort:
      n_pns                — candidates in that cohort
      n_with_position_match — score-positive (positional-miin) hits
      n_with_free_miin      — anywhere-miin hits
      hit_rate_position     — fraction of cohort with positional match
      hit_rate_free         — fraction of cohort with any miin
      top_matches           — top_k highest-scored candidates in cohort
    """
    epsd2_pns = inputs.get("epsd2_personal_names") or []
    janabiyah = inputs.get("janabiyah_reading") or {}
    phoneme_map = inputs.get("phoneme_map") or {}
    families = inputs.get("allograph_families") or {}

    cohorts_param = params.get("cohorts") or [[3, 4], [5, 6], [7, 8], [9, 99]]
    if not isinstance(cohorts_param, list):
        cohorts_param = [[3, 4], [5, 6], [7, 8], [9, 99]]
    min_icount = max(1, _safe_int(params.get("min_icount", 1), 1))
    top_k = max(5, _safe_int(params.get("top_k", 15), 15))

    if not epsd2_pns or not janabiyah:
        return {
            "verdict": "INSUFFICIENT_DATA",
            "n_pns_searched": 0,
            "cohorts": [],
        }

    epsd2_pns = [
        p for p in epsd2_pns
        if int(p.get("icount", 0) or 0) >= min_icount
    ]

    # --- Build miin-token vocabulary identically to Phase-29 V3 -------------
    base_renderings = {
        "miin", "mi-in", "me-en", "mi-na", "me-na", "mi-il",
        "me-il", "mi-en", "me-in", "mu-li", "min", "men",
        "mul", "imin", "kakkab", "asz",
    }
    fish_family_members = set(
        str(m) for m in (families.get("fish") or {}).get("members") or []
    )
    for sid in fish_family_members:
        ph = (phoneme_map.get(sid) or {}).get("phoneme", "")
        for tok in re.split(r"[/\s]", ph or ""):
            t = tok.strip().lower()
            if t and len(t) >= 2:
                base_renderings.add(t)
    rendering_tokens: set[str] = set()
    for r in base_renderings:
        for t in r.split("-"):
            if t and len(t) >= 2:
                rendering_tokens.add(t)

    miin_positions = {1, 3, 6}
    n_target_segments = 7

    # --- Score every PN once, then bin by best-form segment count ----------
    def _score(headword: str, forms: list[str], periods: list[str], icount: int) -> dict | None:
        all_segs = _pn_to_segments(forms)
        if not all_segs:
            return None
        best_score = -999.0
        best_segs: list[str] = []
        best_pmatch = 0
        best_free = 0
        best_positions: list[int] = []
        for segs in all_segs:
            n_segs = len(segs)
            delta = abs(n_segs - n_target_segments)
            length_score = max(0.0, 3.0 - 0.5 * delta)
            pmatch = 0
            positions: list[int] = []
            for i, seg in enumerate(segs):
                if i in miin_positions and seg.lower() in rendering_tokens:
                    pmatch += 1
                    positions.append(i)
            free = sum(1 for s in segs if s.lower() in rendering_tokens)
            total = length_score + pmatch * 1.5 + free * 0.5
            if total > best_score:
                best_score = total
                best_segs = segs
                best_pmatch = pmatch
                best_free = free
                best_positions = positions
        return {
            "headword": headword,
            "best_form": "-".join(best_segs),
            "n_segments": len(best_segs),
            "position_match": best_pmatch,
            "positions_matched": best_positions,
            "free_miin": best_free,
            "total_score": round(best_score, 3),
            "icount": icount,
            "periods": periods,
            "n_alternate_forms": len(all_segs),
        }

    scored: list[dict] = []
    for pn in epsd2_pns:
        r = _score(
            pn.get("headword", ""),
            pn.get("forms", []),
            pn.get("periods", []),
            int(pn.get("icount", 0) or 0),
        )
        if r:
            scored.append(r)

    # --- Bin by segment count -----------------------------------------------
    def _label(lo: int, hi: int) -> str:
        return f"S{lo}-{hi}" if hi < 100 else f"S{lo}+"

    cohorts: list[dict] = []
    overall_pos = 0
    overall_free = 0
    for pair in cohorts_param:
        try:
            lo, hi = int(pair[0]), int(pair[1])
        except Exception:  # noqa: BLE001
            continue
        members = [r for r in scored if lo <= r["n_segments"] <= hi]
        if not members:
            cohorts.append({
                "cohort": _label(lo, hi),
                "lo": lo, "hi": hi,
                "n_pns": 0,
                "n_with_position_match": 0,
                "n_with_free_miin": 0,
                "hit_rate_position": 0.0,
                "hit_rate_free": 0.0,
                "top_matches": [],
            })
            continue
        n_pos = sum(1 for r in members if r["position_match"] > 0)
        n_free = sum(1 for r in members if r["free_miin"] > 0)
        overall_pos += n_pos
        overall_free += n_free
        members_sorted = sorted(
            members, key=lambda r: (-r["total_score"], -r["icount"]),
        )
        cohorts.append({
            "cohort": _label(lo, hi),
            "lo": lo, "hi": hi,
            "n_pns": len(members),
            "n_with_position_match": n_pos,
            "n_with_free_miin": n_free,
            "hit_rate_position": round(n_pos / len(members), 4),
            "hit_rate_free": round(n_free / len(members), 4),
            "top_matches": members_sorted[:top_k],
        })

    # --- Verdict -------------------------------------------------------------
    pos_rates = [c["hit_rate_position"] for c in cohorts if c["n_pns"] > 0]
    if pos_rates:
        max_rate = max(pos_rates)
        min_rate = min(pos_rates)
        rises = max_rate > 5 * max(1e-6, min_rate)
        # Look for monotonic concentration in ANY single cohort
        peak = max(cohorts, key=lambda c: c["hit_rate_position"])
        verdict = (
            f"Phase-30b length-cohort reverse Janabiyah search: "
            f"position-match hit rates {min_rate:.4f}\u2013{max_rate:.4f} across "
            f"{len(pos_rates)} cohorts. "
            + (
                f"Peak in {peak['cohort']} ({peak['hit_rate_position']:.4f}, "
                f"{peak['n_with_position_match']}/{peak['n_pns']} PNs). "
                f"Concentrated signal: contact-zone hypothesis SURVIVES one DoF."
                if rises
                else
                f"No cohort concentration (all within 5x of each other). "
                f"Janabiyah miin-pattern signal does NOT track candidate length \u2014 "
                f"one more DoF eliminated for the contact-zone hypothesis."
            )
        )
    else:
        verdict = "Phase-30b: no scored candidates in any cohort."

    return {
        "n_pns_searched": len(scored),
        "n_renderings": len(rendering_tokens),
        "n_cohorts": len(cohorts),
        "n_with_position_match_total": overall_pos,
        "n_with_free_miin_total": overall_free,
        "cohorts": cohorts,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
#  Phase-30c: per-bin permutation null on spectral gaps
# ---------------------------------------------------------------------------


def _bigram_transition_matrix(
    seqs: list[list[str]],
) -> tuple[list[str], list[list[float]]]:
    """Same construction as Phase-20's _bigram_transition_matrix."""
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for s in seqs:
        for i in range(len(s) - 1):
            counts[s[i]][s[i + 1]] += 1
    signs = sorted(counts.keys() | {b for row in counts.values() for b in row})
    idx = {s: i for i, s in enumerate(signs)}
    n = len(signs)
    P = [[0.0] * n for _ in range(n)]
    for a, row in counts.items():
        total = sum(row.values())
        if total <= 0:
            continue
        i = idx[a]
        for b, c in row.items():
            P[i][idx[b]] = c / total
    return signs, P


def _spectral_gap(P: list[list[float]]) -> float:
    if not P:
        return 0.0
    try:
        import numpy as np  # noqa: PLC0415
    except Exception:  # noqa: BLE001
        return 0.0
    a = np.array(P, dtype=float)
    if a.size == 0:
        return 0.0
    try:
        eigvals = np.linalg.eigvals(a)
    except Exception:  # noqa: BLE001
        return 0.0
    mags = sorted([abs(complex(v)) for v in eigvals], reverse=True)
    return max(0.0, 1.0 - mags[1]) if len(mags) >= 2 else 0.0


def _shuffle_permutation_null(inputs: dict, params: dict) -> dict:
    """Per-bin permutation null spectral analysis.

    Inputs:
      stratifications  dict[bin_label, list[sequences]]  from LengthStratifier

    Params:
      n_permutations  int   default 200
      seed            int   default 42

    For each bin:
      1. Compute observed spectral gap on the original sequences.
      2. Build a flat token bag for the bin (concatenation of all sequences).
      3. For n_permutations iterations: shuffle the flat bag, re-segment into
         pseudo-sequences with the same length profile as the original bin,
         and compute the null spectral gap.
      4. Report observed, null mean / sd / quantiles, and the one-sided
         empirical p-value P(null >= observed).

    A high p-value (>= 0.05) means the observed gap is indistinguishable
    from a positionally-shuffled null \u2014 i.e. the corpus's anomalously low
    spectral gap is not rescued by length stratification.
    """
    stratifications = inputs.get("stratifications") or {}
    if not isinstance(stratifications, dict) or not stratifications:
        return {"error": "stratifications input must be a non-empty dict"}

    n_perm = max(10, _safe_int(params.get("n_permutations", 200), 200))
    seed = _safe_int(params.get("seed", 42), 42)
    rng = random.Random(seed)

    per_bin: dict[str, dict] = {}
    for label, seqs in stratifications.items():
        if not seqs:
            per_bin[label] = {
                "n_seqs": 0, "observed_gap": None,
                "p_value": None, "verdict": "no data",
            }
            continue
        flat = [s for seq in seqs for s in seq]
        if len(flat) < 2:
            per_bin[label] = {
                "n_seqs": len(seqs), "n_tokens": len(flat),
                "observed_gap": None, "p_value": None,
                "verdict": "insufficient tokens",
            }
            continue

        lengths = [len(s) for s in seqs]
        _, P_obs = _bigram_transition_matrix(seqs)
        observed = _spectral_gap(P_obs)

        null_gaps: list[float] = []
        bag = list(flat)
        for _ in range(n_perm):
            rng.shuffle(bag)
            # Re-segment into pseudo-sequences with the same length profile.
            cursor = 0
            pseudo: list[list[str]] = []
            for L in lengths:
                pseudo.append(bag[cursor:cursor + L])
                cursor += L
            _, P_null = _bigram_transition_matrix(pseudo)
            null_gaps.append(_spectral_gap(P_null))

        null_gaps.sort()
        n_ge = sum(1 for g in null_gaps if g >= observed)
        p_value = (n_ge + 1) / (len(null_gaps) + 1)
        mean = sum(null_gaps) / len(null_gaps)
        var = sum((g - mean) ** 2 for g in null_gaps) / len(null_gaps)
        sd = var ** 0.5
        median = null_gaps[len(null_gaps) // 2]
        per_bin[label] = {
            "n_seqs": len(seqs),
            "n_tokens": len(flat),
            "observed_gap": round(observed, 6),
            "null_n": len(null_gaps),
            "null_mean": round(mean, 6),
            "null_sd": round(sd, 6),
            "null_median": round(median, 6),
            "null_p05": round(null_gaps[max(0, int(0.05 * len(null_gaps)) - 1)], 6),
            "null_p95": round(null_gaps[min(len(null_gaps) - 1, int(0.95 * len(null_gaps)))], 6),
            "p_value_one_sided": round(p_value, 4),
            "verdict": (
                "observed gap is significantly above a positional null "
                "(corpus has real bigram structure)"
                if p_value < 0.05
                else "observed gap is indistinguishable from a positional null "
                     "(no extra bigram structure beyond unigram frequency)"
            ),
        }

    # Aggregate verdict: how many bins are significant?
    n_total = sum(1 for d in per_bin.values() if d.get("p_value_one_sided") is not None)
    n_sig = sum(
        1 for d in per_bin.values()
        if isinstance(d.get("p_value_one_sided"), float)
        and d["p_value_one_sided"] < 0.05
    )
    if n_total == 0:
        verdict = "Phase-30c: no bin had enough tokens for a permutation null."
    else:
        verdict = (
            f"Phase-30c per-bin permutation null (N={n_perm}): "
            f"{n_sig}/{n_total} bins reach p<0.05 against a length-matched "
            f"shuffled null. "
            + (
                "The bigram structure is real and detectable at every "
                "length scale (corpus's small spectral gap is a level effect, "
                "not a level-N noise effect)."
                if n_sig == n_total
                else
                "Some length bins show no detectable bigram structure beyond "
                "unigram frequency \u2014 evidence consistent with the "
                "Phase-30a finding that the corpus is unusually deterministic."
            )
        )
    return {
        "per_bin": per_bin,
        "n_bins": len(per_bin),
        "n_significant": n_sig,
        "n_with_data": n_total,
        "n_permutations": n_perm,
        "seed": seed,
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
#  Atomic node defs for registration
# ---------------------------------------------------------------------------


def _phase30_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "LengthCohortReverseJanabiyahSearch",
            "Length-Cohort Reverse Janabiyah Search (Phase-30b)",
            "Phase-30 / Decipherment",
            "Length-stratified version of Phase-29 ReverseJanabiyahSearchV3. "
            "Bins ePSD2 personal-name candidates by syllable count cohort "
            "(default 3-4, 5-6, 7-8, 9+) and reports per-cohort positional / "
            "free miin hit rates. Tests whether the Janabiyah miin-pattern "
            "signal concentrates in any specific length cohort.",
            inputs=[
                {"name": "epsd2_personal_names", "type": "json", "required": True},
                {"name": "janabiyah_reading", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
                {"name": "allograph_families", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_pns_searched", "type": "number"},
                {"name": "n_renderings", "type": "number"},
                {"name": "n_cohorts", "type": "number"},
                {"name": "n_with_position_match_total", "type": "number"},
                {"name": "n_with_free_miin_total", "type": "number"},
                {"name": "cohorts", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "cohorts": {
                        "type": "array",
                        "default": [[3, 4], [5, 6], [7, 8], [9, 99]],
                        "description": "List of [lo, hi] segment-count pairs.",
                    },
                    "min_icount": {
                        "type": "integer", "default": 1, "minimum": 1,
                        "description": "Minimum ePSD2 instance count.",
                    },
                    "top_k": {
                        "type": "integer", "default": 15, "minimum": 5,
                        "description": "Top matches reported per cohort.",
                    },
                },
            },
            fn=_length_cohort_reverse_janabiyah,
        ),
        AtomicNodeDef(
            "ShufflePermutationNull",
            "Shuffle Permutation Null Spectral Test (Phase-30c)",
            "Phase-30 / Spectral",
            "Per-bin permutation null on bigram-transition spectral gaps. "
            "For each length bin, resamples the flat token bag into "
            "pseudo-sequences matching the original length profile, computes "
            "the null spectral gap N times, and reports the one-sided p-value "
            "P(null >= observed).",
            inputs=[
                {"name": "stratifications", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "per_bin", "type": "json"},
                {"name": "n_bins", "type": "number"},
                {"name": "n_significant", "type": "number"},
                {"name": "n_with_data", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {
                        "type": "integer", "default": 200, "minimum": 10,
                    },
                    "seed": {"type": "integer", "default": 42},
                },
            },
            fn=_shuffle_permutation_null,
        ),
    ]


__all__ = [
    "_length_cohort_reverse_janabiyah",
    "_shuffle_permutation_null",
    "_phase30_node_defs",
]
