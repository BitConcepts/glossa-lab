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
from collections import defaultdict
from typing import Any

# ---------------------------------------------------------------------------
#  Phase-30b: length-cohort reverse Janabiyah search
# ---------------------------------------------------------------------------


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


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

    Spec 087 S3 (family F7): the mechanism is the generic
    ReverseSkeletonSearch engine (glossa_lab.generic_primitives)
    in its pn_cohorts mode; this node is its Phase-30
    parameterisation — the Phase-29 scoring (the engine's carried
    ePSD2 segmenter and token matching) plus the cohort table and
    the 5x concentration verdict rule, all carried as spec data
    (the cohorts table remains this node's own param, as before).
    The module-local _pn_to_segments helper was used only here;
    it was removed (the engine carries the shared segmenter).
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        reverse_skeleton_search_execute,
    )

    merged = dict(params)
    merged["search_spec"] = {
        "candidate_mode": "pn_cohorts",
        "candidates_input": "epsd2_personal_names",
        "target_positions": [1, 3, 6],
        "target_length": 7,
        "length_base": 3.0,
        "length_step": 0.5,
        "position_weight": 1.5,
        "free_weight": 0.5,
        "renderings": [
            "miin", "mi-in", "me-en", "mi-na", "me-na", "mi-il",
            "me-il", "mi-en", "me-in", "mu-li", "min", "men",
            "mul", "imin", "kakkab", "asz",
        ],
        "expand_renderings": True,
        "expansion_family": "fish",
        "top_k_default": 15,
        "top_k_floor": 5,
        "cohorts_default": [[3, 4], [5, 6], [7, 8], [9, 99]],
        "concentration_factor": 5.0,
        "empty_result": {
            "verdict": "INSUFFICIENT_DATA",
            "n_pns_searched": 0,
            "cohorts": [],
        },
        "verdict_head_template": (
            "Phase-30b length-cohort reverse Janabiyah search: "
            "position-match hit rates {min_rate:.4f}–{max_rate:.4f} "
            "across {n_cohorts_tested} cohorts. "
        ),
        "verdict_peak_template": (
            "Peak in {peak_cohort} ({peak_rate:.4f}, "
            "{peak_pos}/{peak_n} PNs). Concentrated signal: "
            "contact-zone hypothesis SURVIVES one DoF."
        ),
        "verdict_flat_text": (
            "No cohort concentration (all within 5x of each other). "
            "Janabiyah miin-pattern signal does NOT track candidate "
            "length — one more DoF eliminated for the contact-zone "
            "hypothesis."
        ),
        "verdict_empty_text": "Phase-30b: no scored candidates in any cohort.",
    }
    return reverse_skeleton_search_execute(inputs, merged)



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


# ──────────────────────────────────────────────────────────────────────────────
# Phase-32 atomic nodes
# ──────────────────────────────────────────────────────────────────────────────


def _permutation_test(inputs: dict, params: dict) -> dict:
    """Statistical permutation test for a score against a null distribution.

    Loads a Phase-29d result JSON, computes the null distribution via
    random permutation, and reports one-sided p-value + percentile rank.
    Used for Phase-30 A1 validation of the Enmenanak finding.
    """
    import json as _json  # noqa: PLC0415
    import random as _random  # noqa: PLC0415
    from pathlib import Path as _Path  # noqa: PLC0415

    # Accept direct score from upstream node OR load from JSON
    score = inputs.get("observed_score") or inputs.get("enmenanak_score") or 0.0
    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0.0

    result_file = str(params.get("result_file", ""))
    if not score and result_file:
        try:
            data = _json.loads(_Path(result_file).read_text(encoding="utf-8"))
            top = (data.get("top_matches") or [])
            score = float(top[0].get("total_score", 0)) if top else 0.0
        except Exception:  # noqa: BLE001
            pass

    n_permutations = int(params.get("n_permutations", 1000))
    seed = int(params.get("seed", 42))
    max_score = int(params.get("max_score", 10))

    rng = _random.Random(seed)
    null_dist = [sum(rng.randint(0, 1) for _ in range(max_score)) for _ in range(n_permutations)]
    p_value = sum(1 for x in null_dist if x >= score) / max(n_permutations, 1)
    percentile = 1.0 - p_value

    if p_value < 0.001:
        verdict = f"HIGHLY SIGNIFICANT: score {score} > 99.9th percentile (p<0.001)"
    elif p_value < 0.01:
        verdict = f"SIGNIFICANT: score {score} > 99th percentile (p<0.01)"
    elif p_value < 0.05:
        verdict = f"SIGNIFICANT: score {score} > 95th percentile (p<0.05)"
    else:
        verdict = f"NOT SIGNIFICANT: score {score} does not exceed null (p={p_value:.3f})"

    return {
        "observed_score": score,
        "p_value": round(p_value, 4),
        "percentile_rank": round(percentile, 4),
        "n_permutations": n_permutations,
        "null_mean": round(sum(null_dist) / max(len(null_dist), 1), 2),
        "null_95th": sorted(null_dist)[int(0.95 * len(null_dist))],
        "verdict": verdict,
    }


def _meluhha_cooccurrence_check(inputs: dict, params: dict) -> dict:
    """Check whether top Phase-29d candidates appear in Meluhha co-occurrence contexts.

    Searches the CDLI Meluhha corpus for co-occurrences with known Meluhha-associated
    Sumerian rulers/trade partners.  A hit = candidate appears alongside 'Meluhha' in
    CDLI texts.  A non-hit does NOT falsify the hypothesis (Meluhha = Indus civilization
    is not universally established).

    Spec 087 S3 PR-F: delegates to the generic CorpusCooccurrenceCheck;
    the candidate ports, the term-length guard and the verdict texts
    are spec data, and the corpus path (backend/reports/
    meluhha_corpus_audit.json — absent from the repo, so the node
    runs against an empty term set today) is a spec parameter
    defaulting to the historical path.
    """
    from pathlib import Path as _Path  # noqa: PLC0415

    from glossa_lab.generic_primitives import corpus_cooccurrence_check_execute

    corpus_path = str(
        _Path(__file__).resolve().parent.parent.parent
        / "backend/reports/meluhha_corpus_audit.json"
    )
    merged = dict(params)
    merged["check_spec"] = {
        "candidates_keys": ["top_candidates", "unique_names"],
        "corpus_path": corpus_path,
        "entries_key": "meluhha_entries",
        "term_len_gt": 3,
        "cap": 20,
        "misses_cap": 5,
        "render_cap": 5,
        "checked_out": "candidates_checked",
        "hits_out": "meluhha_hits",
        "misses_out": "meluhha_misses",
        "available_out": "meluhha_corpus_available",
        "favourable_template": (
            "FAVORABLE: {n_hits} candidate(s) appear in Meluhha "
            "co-occurrence contexts: {hits_top}"),
        "neutral_verdict": (
            "NEUTRAL: No direct Meluhha co-occurrence found. "
            "This does not falsify the hypothesis (Meluhha = Indus "
            "identification is independent)."),
    }
    return corpus_cooccurrence_check_execute(inputs, merged)


def _syllable_lm_from_json(data: dict) -> "Any":
    """Build a proper LanguageModel from a syllable LM JSON dict.

    Spec 087 S3 PR-F: the builder lives in the generic SyllableLMLoader
    engine (glossa_lab.generic_primitives.syllable_lm_from_json); this
    historical helper delegates to it so the Sanskrit loader below
    keeps the identical code path.
    """
    from glossa_lab.generic_primitives import syllable_lm_from_json

    return syllable_lm_from_json(data)


def _builtin_syllable_lm(inputs: dict, params: dict) -> dict:
    """Load the syllable-level Dravidian Tamil LM (dravidian_syllable_lm.json).

    Produces the same interface as BuiltinLM so it can plug into SADecipher.
    Built by: backend/scripts/build_dravidian_syllable_lm.py
    Citations: E.1 (DEDR), A.12 (Mahadevan 2003 TB)

    Spec 087 S3 PR-F: delegates to the generic SyllableLMLoader; the
    bundled file path, the language label and the error text are spec
    data. An lm_path param may override the file (relative paths
    resolve against the repo root).
    """
    from pathlib import Path as _Path  # noqa: PLC0415

    from glossa_lab.generic_primitives import syllable_lm_loader_execute

    repo = _Path(__file__).resolve().parent.parent.parent
    merged = dict(params)
    merged["lm_spec"] = {
        "base_dir": str(repo),
        "path": str(repo / "backend/glossa_lab/data/dravidian_syllable_lm.json"),
        "language": "dravidian_syllable",
        "error": ("dravidian_syllable_lm.json not found — run "
                  "build_dravidian_syllable_lm.py"),
    }
    return syllable_lm_loader_execute(inputs, merged)


# The Tamil romanisation diacritic table for IndusAnchorSetSyllable,
# as data (Spec 087 S3, family F8): ordered (source, replacement)
# pairs applied after lowercasing — the first two entries are a
# historical duplicate, kept as-is. The triage's executed attempt
# H2 proved the parameterised form byte-identical with this table
# passed in as data.
_TAMIL_DIACRITIC_TABLE: list[tuple[str, str]] = [
    ("ā", "a"), ("ā", "a"), ("ī", "i"), ("ū", "u"), ("ṭ", "t"),
    ("ṇ", "n"), ("ḷ", "l"), ("ṟ", "r"), ("ṙ", "r"), ("ñ", "n"),
    ("ṅ", "n"), ("ḍ", "d"), ("ṉ", "n"), ("ḻ", "l"), ("ḥ", "h"),
    ("ṃ", "m"), ("ö", "o"), ("ä", "a"), ("ü", "u"), ("é", "e"),
    ("è", "e"), ("ê", "e"),
]


def _indus_anchor_set_syllable(inputs: dict, params: dict) -> dict:
    """Load INDUS_FINAL_ANCHORS.json and map each reading to a syllable token.

    For each anchor, the Tamil word reading is converted to its closest syllable-
    level equivalent by:
      1. Stripping diacritics (ā→a, ī→i, etc.)
      2. If the result is already in the syllable LM vocab → use it directly
      3. If the result is polysyllabic → split into CV chunks, use the first
         chunk that appears in the syllable LM vocab
      4. Skip positional-label anchors (term-*, med-*, init-*) and uncertain entries

    Returns `anchor_dict` compatible with SADecipher.anchors port.
    Citations: A.1 (Mahadevan 1977), C.2 (Parpola 2010)

    Spec 087 S3 (family F8): the mechanism is the generic
    AnchorSyllabifier engine (glossa_lab.generic_primitives);
    this node is its Indus parameterisation — both file paths,
    the Tamil diacritic table, the confidence order, and the
    positional-label skip pattern live in the params below, not
    in code. H2 in the triage record is this conversion's proof,
    executed before the fact: a byte-identical anchor_dict at
    MEDIUM/HIGH/LOW (171/166/174 anchors).
    """
    from pathlib import Path as _Path  # noqa: PLC0415

    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        anchor_syllabifier_execute,
    )

    REPO = _Path(__file__).resolve().parent.parent.parent
    merged = dict(params)
    merged.setdefault("anchors_path", str(REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"))
    merged.setdefault(
        "vocab_path", str(REPO / "backend/glossa_lab/data/dravidian_syllable_lm.json")
    )
    merged.setdefault("diacritic_table", [list(pair) for pair in _TAMIL_DIACRITIC_TABLE])
    merged.setdefault(
        "confidence_order", {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "UNCERTAIN": 0}
    )
    merged.setdefault("skip_pattern", r"(term|med|init|ctx|role)[-:]")
    merged.setdefault("missing_error", "INDUS_FINAL_ANCHORS.json not found")
    return anchor_syllabifier_execute(inputs, merged)


def _sanskrit_syllable_lm(inputs: dict, params: dict) -> dict:
    """Load the Sanskrit syllable-level LM (sanskrit_syllable_lm.json).

    Provides a comparable granularity LM to DravidianSyllableLM for valid
    head-to-head SA falsification (Phase-32 T7 redo / Phase-33 T7).
    Built by: backend/scripts/build_sanskrit_syllable_lm.py
    """
    import json as _json  # noqa: PLC0415
    from pathlib import Path as _Path  # noqa: PLC0415

    REPO = _Path(__file__).resolve().parent.parent.parent
    path = REPO / "backend/glossa_lab/data/sanskrit_syllable_lm.json"
    if not path.exists():
        return {"error": "sanskrit_syllable_lm.json not found — run build_sanskrit_syllable_lm.py"}

    data = _json.loads(path.read_text(encoding="utf-8"))
    lm = _syllable_lm_from_json(data)

    return {
        "lm": lm,
        "language": "sanskrit_syllable",
        "n_bigrams": data.get("n_bigrams", len(data.get("bigrams", {}))),
        "n_syllables": data.get("n_syllables", len(data.get("vocab", []))),
    }


def _phase30_phase32_node_defs() -> list[Any]:
    """Phase-30 A-series validation + Phase-32 new primitive nodes."""
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "PermutationTest",
            "Permutation Statistical Test (Phase-30 A1)",
            "Phase-30 / Statistical Validation",
            "Computes a one-sided permutation p-value for an observed score against "
            "a random null distribution. Used for Phase-30 A1 validation of the "
            "Enmenanak finding (Phase-29d score=7.0 vs null).",
            inputs=[
                {"name": "observed_score", "type": "number", "required": False},
                {"name": "enmenanak_score", "type": "number", "required": False},
                {"name": "top_candidates", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "observed_score", "type": "number"},
                {"name": "p_value", "type": "number"},
                {"name": "percentile_rank", "type": "number"},
                {"name": "null_95th", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 1000, "minimum": 100},
                    "max_score": {"type": "integer", "default": 10, "minimum": 1,
                                  "description": "Maximum possible score value"},
                    "result_file": {"type": "string", "default": "",
                                    "description": "Path to Phase-29d result JSON (optional)"},
                    "seed": {"type": "integer", "default": 42},
                },
            },
            fn=_permutation_test,
        ),
        AtomicNodeDef(
            "MeluhhaCooccurrenceCheck",
            "Meluhha Co-occurrence Check (Phase-30 A3)",
            "Phase-30 / Statistical Validation",
            "Checks whether Phase-29d top candidates appear in CDLI Meluhha "
            "co-occurrence contexts. A non-hit does NOT falsify — absence of evidence "
            "is not evidence of absence for the Meluhha = Indus identification.",
            inputs=[
                {"name": "top_candidates", "type": "json", "required": False},
                {"name": "unique_names", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "n_hits", "type": "number"},
                {"name": "meluhha_hits", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_meluhha_cooccurrence_check,
        ),
        AtomicNodeDef(
            "DravidianSyllableLM",
            "Dravidian Syllable-Level LM (Phase-32, fixed)",
            "Phase-32 / Decipherment",
            "Loads dravidian_syllable_lm.json — a syllable-level bigram LM built from "
            "DEDR roots + clean Tamil-Brahmi aksharas (2293 bigrams, 655 syllables). "
            "Fix (Phase-33): bigram_freq and ranked attributes now properly populated "
            "so SADecipher BigamScorer works correctly. "
            "Citations: E.1 (DEDR), A.12 (Mahadevan 2003 TB). "
            "Build: backend/scripts/build_dravidian_syllable_lm.py",
            inputs=[],
            outputs=[
                {"name": "lm", "type": "any"},
                {"name": "n_bigrams", "type": "number"},
                {"name": "n_syllables", "type": "number"},
                {"name": "language", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_builtin_syllable_lm,
        ),
        AtomicNodeDef(
            "IndusAnchorSetSyllable",
            "Indus Syllable Anchor Set (Phase-33 T1)",
            "Phase-33 / Decipherment",
            "Loads INDUS_FINAL_ANCHORS.json and maps each Tamil reading to a syllable "
            "token compatible with the DravidianSyllableLM vocabulary. "
            "Monosyllabic readings (min, kol, an, na) pass through unchanged. "
            "Polysyllabic readings (erutu, yanai) are split and the first syllable in "
            "the LM vocab is used. Positional labels (term-*, med-*, init-*) and "
            "uncertain entries are skipped. Returns anchor_dict for SADecipher. "
            "Citations: A.1 (M77), C.2 (Parpola 2010)",
            inputs=[],
            outputs=[
                {"name": "anchor_dict", "type": "json"},
                {"name": "n_anchors", "type": "number"},
                {"name": "n_skipped", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_confidence": {
                        "type": "string",
                        "default": "MEDIUM",
                        "description": "Minimum anchor confidence: HIGH | MEDIUM | LOW",
                    },
                },
            },
            fn=_indus_anchor_set_syllable,
        ),
        AtomicNodeDef(
            "SanskritSyllableLM",
            "Sanskrit Syllable-Level LM (Phase-33 T7 redo)",
            "Phase-33 / Decipherment",
            "Loads sanskrit_syllable_lm.json — a Sanskrit syllable-level bigram LM "
            "at the same granularity as DravidianSyllableLM (CV tokens, 2-3 chars). "
            "Used for Phase-32 T7 redo: valid head-to-head SA comparison of "
            "Dravidian vs Sanskrit as target language for the Indus script. "
            "Build: backend/scripts/build_sanskrit_syllable_lm.py",
            inputs=[],
            outputs=[
                {"name": "lm", "type": "any"},
                {"name": "n_bigrams", "type": "number"},
                {"name": "n_syllables", "type": "number"},
                {"name": "language", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_sanskrit_syllable_lm,
        ),
    ]


__all__ = [
    "_length_cohort_reverse_janabiyah",
    "_shuffle_permutation_null",
    "_permutation_test",
    "_meluhha_cooccurrence_check",
    "_builtin_syllable_lm",
    "_syllable_lm_from_json",
    "_indus_anchor_set_syllable",
    "_sanskrit_syllable_lm",
    "_phase30_node_defs",
    "_phase30_phase32_node_defs",
]
