"""Structural fingerprint for writing system classification.

A writing system's structural fingerprint is a 10-dimensional vector that
quantitatively characterises its statistical properties.  Two scripts with
similar fingerprints are structurally alike — not necessarily related by
language family, but sharing the same type of writing system.

THE SCIENTIFIC QUESTION THIS ANSWERS:
  "Where does the Indus script sit in the space of all known writing systems?
   Is it closer to an abjad like Ugaritic, a syllabary like Linear B, or a
   logo-syllabic system like Sumerian cuneiform?"

THE 10 DIMENSIONS:
  1.  H1_norm                 : Normalised unigram entropy [0,1]
                                High = rich sign distribution; low = dominated by few signs.
  2.  H2H1_ratio              : Bigram/unigram entropy ratio
                                < 1 means sequences are constrained (grammatical structure);
                                = 1 means signs are independent (no sequential pattern).
  3.  zipf_exponent           : Zipf-Mandelbrot frequency exponent (α > 0)
                                Abjads α ≈ 0.7–1.0; syllabaries α ≈ 0.8–1.2;
                                logo-syllabic α ≈ 1.0–1.6 (steeper → more rare signs).
  4.  type_token_ratio        : V / N  (distinct signs / total tokens)
                                Low (0.03) = abjad; medium (0.10) = syllabary;
                                high (0.15+) = logo-syllabic.
  5.  hapax_fraction          : Fraction of signs appearing exactly once
                                Proxy for how data-sparse the corpus is.
  6.  mean_positional_entropy : Mean of per-sign positional entropy [0,1]
                                High = signs appear uniformly across positions;
                                low = strong initial/terminal preferences (abjads).
  7.  polyvalence_fraction    : Fraction of signs with bimodal positional histograms
                                High → logo-syllabic (many signs serve double duty).
  8.  mean_inscription_length : Mean tokens per inscription
                                Seals = short (3–6); tablets = long (20+).
  9.  boundary_bias_variance  : Variance in sign initial+terminal bias scores
                                High = some signs are strongly positional (determinatives);
                                low = uniform distribution (phonetic scripts).
  10. paradigmatic_rate       : Rate of paradigmatic alternation (same context, different sign)
                                High → rich morphological system; low → restricted vocabulary.

KNOWN FINGERPRINTS (approximate, from literature):
  Ugaritic abjad:     [0.88, 0.85, 0.75, 0.031, 0.03, 0.45, 0.05, 11.5, 0.05, 0.30]
  Linear B syllabary: [0.91, 0.88, 0.90, 0.099, 0.13, 0.50, 0.07,  4.2, 0.08, 0.40]
  Indus (estimated):  [0.85, 0.82, 1.10, 0.087, 0.45, 0.40, 0.20,  5.1, 0.12, 0.25]

USAGE:
    from glossa_lab.pipelines.structural_fingerprint import compute_fingerprint, compare_scripts
    fp = compute_fingerprint(inscriptions, system_name="my_script")
    ranking = compare_scripts(fp, known_fingerprints_db())
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

from glossa_lab.engine import register_pipeline  # noqa: I001

# ── Fingerprint computation ────────────────────────────────────────────

def compute_fingerprint(
    inscriptions: list[list[str]],
    system_name: str = "unknown",
    writing_type: str = "unknown",
) -> dict[str, Any]:
    """Compute the 10-dimensional structural fingerprint of a writing system corpus.

    Args:
        inscriptions: List of inscriptions, each a list of sign strings.
        system_name:  Label for this script.
        writing_type: Tier label for human-readable output.

    Returns:
        dict with 'vector' (list[float]), 'dimensions' (dict of named values),
        'system', 'writing_type', and interpretive notes.
    """
    flat = [s for insc in inscriptions for s in insc]
    if not flat:
        return {"system": system_name, "vector": [0.0] * 10, "error": "empty corpus"}

    freq: Counter[str] = Counter(flat)
    N = len(flat)
    V = len(freq)

    # ── Dim 1: H1_norm ────────────────────────────────────────────────
    h1 = 0.0
    for c in freq.values():
        p = c / N
        h1 -= p * math.log(p)
    h1_max = math.log(V) if V > 1 else 1.0
    h1_norm = h1 / h1_max if h1_max > 0 else 0.0

    # ── Dim 2: H2/H1 ratio ────────────────────────────────────────────
    bigram_counts: Counter[tuple[str, str]] = Counter()
    for insc in inscriptions:
        for i in range(len(insc) - 1):
            bigram_counts[(insc[i], insc[i + 1])] += 1
    bg_total = sum(bigram_counts.values()) or 1
    h2 = 0.0
    for c in bigram_counts.values():
        p = c / bg_total
        h2 -= p * math.log(p)
    h2h1_ratio = (h2 / 2.0) / h1 if h1 > 0 else 1.0  # per-symbol bigram entropy

    # ── Dim 3: Zipf exponent ──────────────────────────────────────────
    # Fit log(rank) vs log(freq) by linear regression
    sorted_freqs = sorted(freq.values(), reverse=True)
    if len(sorted_freqs) >= 5:
        log_ranks = [math.log(i + 1) for i in range(len(sorted_freqs))]
        log_freqs = [math.log(max(f, 1)) for f in sorted_freqs]
        n_pts = len(log_ranks)
        mean_r = sum(log_ranks) / n_pts
        mean_f = sum(log_freqs) / n_pts
        cov = sum((log_ranks[i] - mean_r) * (log_freqs[i] - mean_f) for i in range(n_pts))
        var_r = sum((r - mean_r) ** 2 for r in log_ranks)
        zipf_exp = abs(cov / var_r) if var_r > 0 else 1.0
    else:
        zipf_exp = 1.0

    # ── Dim 4: Type-token ratio ───────────────────────────────────────
    vn_ratio = V / N

    # ── Dim 5: Hapax fraction ─────────────────────────────────────────
    hapax = sum(1 for c in freq.values() if c == 1)
    hapax_frac = hapax / V if V > 0 else 0.0

    # ── Dim 6: Mean positional entropy ───────────────────────────────
    # For each sign, compute its positional distribution (fractional
    # position in inscription) and measure its entropy. Average across signs.
    from glossa_lab.pipelines.sign_polyvalence import (
        _fractional_positions,
        _positional_histogram,
    )
    frac_pos = _fractional_positions(inscriptions)
    pos_entropies: list[float] = []
    bins = 10
    ln_bins = math.log(bins)
    for sign, positions in frac_pos.items():
        if freq[sign] < 3:  # need enough data
            continue
        hist = _positional_histogram(positions, bins)
        pe = -sum(p * math.log(p) for p in hist if p > 0) / ln_bins
        pos_entropies.append(pe)
    mean_pos_entropy = sum(pos_entropies) / len(pos_entropies) if pos_entropies else 0.5

    # ── Dim 7: Polyvalence fraction ───────────────────────────────────
    from glossa_lab.pipelines.sign_polyvalence import detect_polyvalent_signs
    poly_result = detect_polyvalent_signs(inscriptions, min_freq=3)
    poly_frac = poly_result["summary"]["candidate_fraction"]

    # ── Dim 8: Mean inscription length ────────────────────────────────
    lengths = [len(i) for i in inscriptions if i]
    mean_len = sum(lengths) / len(lengths) if lengths else 0.0

    # ── Dim 9: Boundary bias variance ────────────────────────────────
    # For each sign, compute boundary_bias = initial_rate + terminal_rate.
    # High variance → some signs are strongly positional (determinatives).
    initial_c: Counter[str] = Counter()
    terminal_c: Counter[str] = Counter()
    insc_c: Counter[str] = Counter()
    for insc in inscriptions:
        if not insc:
            continue
        insc_c.update(insc)
        if len(insc) >= 2:
            initial_c[insc[0]] += 1
            terminal_c[insc[-1]] += 1

    biases: list[float] = []
    for sign in freq:
        if freq[sign] < 3:
            continue
        occ = insc_c.get(sign, 1)
        bias = (initial_c.get(sign, 0) + terminal_c.get(sign, 0)) / occ
        biases.append(bias)
    if biases:
        mean_bias = sum(biases) / len(biases)
        bb_var = sum((b - mean_bias) ** 2 for b in biases) / len(biases)
    else:
        bb_var = 0.0

    # ── Dim 10: Paradigmatic alternation rate ────────────────────────
    # Look for pairs of inscriptions that are identical except for one sign.
    # Count how often the same position admits different signs.
    # This proxies the richness of paradigmatic oppositions.
    alternations = 0
    comparisons = 0
    # Sample pairs to keep it tractable
    sample_size = min(len(inscriptions), 500)
    sample_inscs = inscriptions[:sample_size]
    for i in range(len(sample_inscs)):
        for j in range(i + 1, len(sample_inscs)):
            a, b = sample_inscs[i], sample_inscs[j]
            if len(a) == len(b) and len(a) >= 2:
                diffs = sum(1 for x, y in zip(a, b) if x != y)
                comparisons += 1
                if diffs == 1:
                    alternations += 1
    paradigmatic_rate = alternations / max(comparisons, 1)

    # ── Assemble vector ───────────────────────────────────────────────
    vector = [
        round(h1_norm, 4),
        round(h2h1_ratio, 4),
        round(zipf_exp, 4),
        round(vn_ratio, 4),
        round(hapax_frac, 4),
        round(mean_pos_entropy, 4),
        round(poly_frac, 4),
        round(mean_len, 2),
        round(bb_var, 4),
        round(paradigmatic_rate, 4),
    ]

    dimensions = {
        "H1_norm":                  vector[0],
        "H2H1_ratio":               vector[1],
        "zipf_exponent":            vector[2],
        "type_token_ratio":         vector[3],
        "hapax_fraction":           vector[4],
        "mean_positional_entropy":  vector[5],
        "polyvalence_fraction":     vector[6],
        "mean_inscription_length":  vector[7],
        "boundary_bias_variance":   vector[8],
        "paradigmatic_rate":        vector[9],
    }

    # ── Interpretation ────────────────────────────────────────────────
    notes: list[str] = []
    if vn_ratio < 0.05 and hapax_frac < 0.10:
        notes.append("Low V/N and hapax → abjad or small alphabet profile")
    elif vn_ratio < 0.12 and hapax_frac < 0.25:
        notes.append("Moderate V/N and hapax → syllabary profile")
    else:
        notes.append("High V/N or hapax → logo-syllabic or poorly-attested corpus")

    if poly_frac > 0.15:
        notes.append(f"High polyvalence ({poly_frac:.0%}) → many signs with dual function")
    if bb_var > 0.10:
        notes.append("High boundary-bias variance → probable determinatives present")
    if h2h1_ratio < 0.80:
        notes.append("Strong sequential constraint (H2/H1 < 0.80) → rich morphological structure")

    return {
        "system":       system_name,
        "writing_type": writing_type,
        "N_tokens":     N,
        "V_types":      V,
        "vector":       vector,
        "dimensions":   dimensions,
        "notes":        notes,
    }


# ── Known script fingerprint database ─────────────────────────────────
# Hand-tuned from literature values (Rao 2009, Yadav 2010, Fuls 2014,
# Snyder 2010) for scripts we don't have direct corpus data for.
# Scripts for which we have direct corpus data override these.

_KNOWN_FINGERPRINTS: dict[str, dict[str, Any]] = {
    # ── Abjads ────────────────────────────────────────────────────────────
    "Ugaritic (abjad, 30 signs)": {
        "system": "Ugaritic (abjad, 30 signs)",
        "writing_type": "abjad",
        # Computed from our Baal Cycle corpus (82 lines, 945 tokens)
        "vector": [0.858, 0.860, 1.397, 0.031, 0.034, 0.550, 0.030, 11.5, 0.048, 0.002],
        "notes": ["Computed from Baal Cycle KTU 1.1-1.6 (82 lines / 945 tokens)"],
    },
    "Phoenician (abjad, 22 signs)": {
        "system": "Phoenician (abjad, 22 signs)",
        "writing_type": "abjad",
        "vector": [0.870, 0.855, 0.920, 0.040, 0.040, 0.535, 0.025, 5.5, 0.045, 0.010],
        "notes": ["Literature estimate (KAI corpus; Segert 1976)"],
    },
    "Old Hebrew (abjad, 22 signs)": {
        "system": "Old Hebrew (abjad, 22 signs)",
        "writing_type": "abjad",
        # Computed from our corpus module (1455 tokens)
        "vector": [0.845, 0.848, 1.080, 0.015, 0.000, 0.560, 0.020, 24.2, 0.040, 0.001],
        "notes": ["Computed from Genesis/Psalms/Proverbs consonantal corpus"],
    },
    # ── Syllabaries ───────────────────────────────────────────────────────
    "Mycenaean Linear B (syllabary, ~87 signs)": {
        "system": "Mycenaean Linear B (syllabary, ~87 signs)",
        "writing_type": "syllabary",
        # Computed from our Pylos fixture corpus (628 tokens, 62 signs)
        "vector": [0.910, 0.880, 0.920, 0.099, 0.129, 0.530, 0.070, 4.2, 0.065, 0.015],
        "notes": ["Computed from Pylos tablets Linear B fixture (628 tokens)"],
    },
    "Cypriot syllabary": {
        "system": "Cypriot syllabary",
        "writing_type": "syllabary",
        "vector": [0.880, 0.870, 0.850, 0.105, 0.150, 0.520, 0.060, 5.5, 0.060, 0.035],
        "notes": ["Literature estimate (Masson 1983; Steele 2013)"],
    },
    # ── Logo-syllabic ─────────────────────────────────────────────────────
    "Egyptian hieroglyphic": {
        "system": "Egyptian hieroglyphic",
        "writing_type": "logo-syllabic",
        "vector": [0.90, 0.80, 1.30, 0.140, 0.42, 0.45, 0.18, 6.5, 0.11, 0.22],
        "notes": ["Literature estimate (Gardiner 1957; Rosetone project)"],
    },
    "Sumerian cuneiform (Ur III)": {
        "system": "Sumerian cuneiform (Ur III)",
        "writing_type": "logo-syllabic",
        "vector": [0.87, 0.78, 1.20, 0.180, 0.38, 0.48, 0.16, 8.2, 0.13, 0.18],
        "notes": ["Literature estimate (CDLI Ur III corpus statistics)"],
    },
    "Proto-Elamite": {
        "system": "Proto-Elamite",
        "writing_type": "logo-syllabic (undeciphered)",
        "vector": [0.84, 0.76, 1.40, 0.210, 0.55, 0.42, 0.22, 4.8, 0.14, 0.12],
        "notes": ["Literature estimate (Dahl 2009; CDLI Proto-Elamite statistics)"],
    },
    "Indus (published statistics)": {
        "system": "Indus (published statistics)",
        "writing_type": "logo-syllabic (undeciphered)",
        # Based on: Yadav et al. 2010 (Zipf), Rao et al. 2009 (entropy),
        # Fuls 2014 (polyvalence, boundary bias), Parpola 1994 (inscription length)
        "vector": [0.86, 0.82, 1.05, 0.087, 0.44, 0.40, 0.19, 5.1, 0.12, 0.21],
        "notes": [
            "Based on: Yadav et al. 2010 Zipf-Mandelbrot fit (α≈1.0);",
            "Rao et al. 2009 block entropy profile;",
            "Fuls 2014 positional analysis of sign 550 and others;",
            "Parpola 1994 average seal inscription length.",
        ],
    },
}


def known_fingerprints_db(
    include_computed: dict[str, dict[str, Any]] | None = None,
) -> dict[str, dict[str, Any]]:
    """Return the combined database of known script fingerprints.

    Args:
        include_computed: Optional dict of freshly-computed fingerprints to merge.

    Returns:
        Dict mapping system_name → fingerprint dict.
    """
    db = dict(_KNOWN_FINGERPRINTS)
    if include_computed:
        db.update(include_computed)
    return db


# ── Distance / similarity ──────────────────────────────────────────────

# Normalisation ranges for each dimension (estimated from known scripts).
# Used to bring all dimensions to comparable [0, 1] scale before distance.
_NORM_RANGES: list[tuple[float, float]] = [
    (0.60, 1.00),   # H1_norm
    (0.70, 1.00),   # H2H1_ratio
    (0.50, 2.00),   # zipf_exponent
    (0.02, 0.25),   # type_token_ratio
    (0.00, 0.80),   # hapax_fraction
    (0.25, 0.70),   # mean_positional_entropy
    (0.00, 0.30),   # polyvalence_fraction
    (2.00, 15.0),   # mean_inscription_length
    (0.00, 0.20),   # boundary_bias_variance
    (0.00, 0.60),   # paradigmatic_rate
]

# Dimension weights: emphasise the most diagnostic dimensions for
# writing system classification (type-token ratio and hapax fraction
# are most discriminating).
_WEIGHTS: list[float] = [
    1.5,  # H1_norm
    1.5,  # H2H1_ratio
    2.0,  # zipf_exponent — very diagnostic
    3.0,  # type_token_ratio — MOST diagnostic
    3.0,  # hapax_fraction — MOST diagnostic
    1.5,  # mean_positional_entropy
    2.0,  # polyvalence_fraction — highly diagnostic
    1.0,  # mean_inscription_length
    1.5,  # boundary_bias_variance
    1.0,  # paradigmatic_rate
]


def _normalise(vector: list[float]) -> list[float]:
    """Normalise fingerprint vector to [0,1] per dimension."""
    normalised = []
    for v, (lo, hi) in zip(vector, _NORM_RANGES):
        if hi == lo:
            normalised.append(0.0)
        else:
            normalised.append(max(0.0, min(1.0, (v - lo) / (hi - lo))))
    return normalised


def euclidean_distance(fp_a: list[float], fp_b: list[float]) -> float:
    """Weighted Euclidean distance between two normalised fingerprints."""
    na = _normalise(fp_a)
    nb = _normalise(fp_b)
    return math.sqrt(
        sum(_WEIGHTS[i] * (na[i] - nb[i]) ** 2 for i in range(len(na)))
    )


def cosine_similarity(fp_a: list[float], fp_b: list[float]) -> float:
    """Cosine similarity between two weighted normalised fingerprints."""
    na = [_WEIGHTS[i] * v for i, v in enumerate(_normalise(fp_a))]
    nb = [_WEIGHTS[i] * v for i, v in enumerate(_normalise(fp_b))]
    dot = sum(a * b for a, b in zip(na, nb))
    mag_a = math.sqrt(sum(a * a for a in na))
    mag_b = math.sqrt(sum(b * b for b in nb))
    return dot / (mag_a * mag_b) if mag_a > 0 and mag_b > 0 else 0.0


def compare_scripts(
    target_fp: dict[str, Any],
    db: dict[str, dict[str, Any]] | None = None,
    metric: str = "euclidean",
) -> list[dict[str, Any]]:
    """Rank all known scripts by structural similarity to the target.

    Uses GPU-accelerated batch distance computation (gpu_fingerprint_compare)
    when torch/cupy+CUDA is available, falling back to numpy then Python.

    Args:
        target_fp: Fingerprint dict from compute_fingerprint().
        db:        Script fingerprint database (default: known_fingerprints_db()).
        metric:    'euclidean' (default) or 'cosine'.

    Returns:
        List of dicts sorted by ascending distance (most similar first), each
        containing: system, writing_type, distance, similarity, notes.
    """
    if db is None:
        db = known_fingerprints_db()

    target_vec = target_fp["vector"]
    target_sys = target_fp.get("system", "")

    # Filter out self-comparison
    names  = [n for n in db if n != target_sys]
    knowns = [db[n] for n in names]
    db_vecs = [k["vector"] for k in knowns]

    if metric == "euclidean":
        # GPU-accelerated batch Euclidean distance
        from glossa_lab.accelerate import gpu_fingerprint_compare
        normalised_target = _normalise(target_vec)
        normalised_db     = [_normalise(v) for v in db_vecs]
        distances = gpu_fingerprint_compare(
            normalised_target, normalised_db, weights=_WEIGHTS,
        )
        results: list[dict[str, Any]] = []
        for i, name in enumerate(names):
            dist = round(distances[i], 4)
            results.append({
                "system":       name,
                "writing_type": knowns[i].get("writing_type", "?"),
                "distance":     dist,
                "similarity":   round(1.0 / (1.0 + dist), 4),
                "notes":        knowns[i].get("notes", []),
            })
    else:
        # Cosine: use batch_cosine_similarity_matrix
        from glossa_lab.accelerate import batch_cosine_similarity_matrix
        all_vecs = [target_vec] + db_vecs
        sim_mat  = batch_cosine_similarity_matrix(all_vecs)
        results = []
        for i, name in enumerate(names):
            sim  = round(float(sim_mat[0][i + 1]), 4)
            dist = round(1.0 - sim, 4)
            results.append({
                "system":       name,
                "writing_type": knowns[i].get("writing_type", "?"),
                "distance":     dist,
                "similarity":   sim,
                "notes":        knowns[i].get("notes", []),
            })

    results.sort(key=lambda r: r["distance"])
    return results


def dimension_comparison_table(
    scripts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build a side-by-side comparison table of script fingerprints.

    Args:
        scripts: List of fingerprint dicts from compute_fingerprint() or db.

    Returns:
        List of row dicts, one per script, with all dimensions as columns.
    """
    rows = []
    for fp in scripts:
        row: dict[str, Any] = {
            "system":       fp.get("system", "?"),
            "writing_type": fp.get("writing_type", "?"),
        }
        dims = fp.get("dimensions") or {}
        vec = fp.get("vector", [0.0] * 10)
        dim_names = [
            "H1_norm", "H2H1_ratio", "zipf_exponent", "type_token_ratio",
            "hapax_fraction", "mean_positional_entropy", "polyvalence_fraction",
            "mean_inscription_length", "boundary_bias_variance", "paradigmatic_rate",
        ]
        for i, dim in enumerate(dim_names):
            row[dim] = dims.get(dim, vec[i] if i < len(vec) else 0.0)
        rows.append(row)
    return rows


# ── Pipeline entry point ──────────────────────────────────────────────

@register_pipeline("structural_fingerprint")
async def run_structural_fingerprint(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point.

    Params:
        text_id:         corpus to fingerprint
        compare_to_db:   if true (default), also rank against known scripts
        metric:          'euclidean' (default) or 'cosine'
    """
    from glossa_lab.database import get_db

    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing required param: text_id")

    db_conn = get_db()
    if db_conn is None:
        raise RuntimeError("Database not available")

    text = await db_conn.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    content = text.get("content", [])
    if content and isinstance(content[0], list):
        inscriptions = content
    else:
        inscriptions = [content]

    fp = compute_fingerprint(
        inscriptions,
        system_name=text.get("name", text_id),
    )

    result = {"text_id": text_id, "fingerprint": fp}

    if params.get("compare_to_db", True):
        db_known = known_fingerprints_db()
        ranking = compare_scripts(fp, db_known, params.get("metric", "euclidean"))
        result["ranking"] = ranking
        result["most_similar"] = ranking[0] if ranking else None

    return result
