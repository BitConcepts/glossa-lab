"""Logosyllabic decipherment pipeline.

Handles scripts whose signs serve multiple functions:
  - Logograms   — a single sign represents a whole word or morpheme
  - Syllabograms — a sign represents a syllable (CV, V, or CVC)
  - Determinatives — unpronounced semantic classifiers

Examples of logosyllabic systems: Sumerian cuneiform, Linear B, Egyptian
hieroglyphs (partly), early Akkadian cuneiform.

Algorithm (inspired by Ventris 1953 grid analysis of Linear B):

1. SIGN CLASSIFICATION
   For each unique sign compute boundary (initial/terminal) bias, isolation
   rate, and frequency tier. Use these to assign a likely functional type:
   - logogram     : high boundary bias, moderate frequency, can appear alone
   - determinative: extreme positional bias (>0.8 initial or terminal)
   - syllabogram  : lower boundary bias, appears in clusters

2. VOWEL/CONSONANT AFFINITY ANALYSIS (Ventris method)
   In an undeciphered syllabic script, signs sharing a *vowel* will appear
   in similar consonantal contexts (they occur after the same set of signs).
   Signs sharing a *consonant* will appear before the same set of signs.
   This allows clustering into rows (same vowel) and columns (same consonant)
   of a notional CV grid without knowing the language.

3. CANDIDATE CV READINGS
   Map affinity clusters to candidate CV values drawn from target language
   syllable inventory. Rank by bigram frequency match.

4. WORD PATTERN MATCHING
   Extract likely phonetic sequences (runs of syllabograms), concatenate
   proposed CV readings, and match against target language vocabulary.

5. OUTPUT
   - sign_classification: {sign: {type, evidence}}
   - affinity_clusters: {vowel_groups: [[signs]], consonant_groups: [[signs]]}
   - proposed_readings: {sign: proposed_cv, confidence}
   - candidate_words: [{sequence, reading, matches, score}]
   - summary: counts and key findings

Pipeline param: text_id (required), target_language ("sumerian"|"linear_b"|
  "generic", default "generic"), max_word_length (default 6).
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from glossa_lab.engine import register_pipeline

# ── Target language CV inventories ───────────────────────────────────

# Sumerian cuneiform syllable inventory (common CV patterns in
# Ur III administrative texts)
_SUMERIAN_SYLLABLES = [
    "a", "e", "i", "u",
    "ba", "bi", "bu", "be",
    "da", "di", "du",
    "ga", "gi", "gu",
    "ka", "ki", "ku",
    "la", "li", "lu",
    "ma", "mi", "mu",
    "na", "ni", "nu",
    "ra", "ri", "ru",
    "sa", "si", "su",
    "ta", "ti", "tu",
    "za", "zi", "zu",
    "ab", "ib", "ub",
    "ag", "ig", "ug",
    "ak", "ik", "uk",
    "al", "il", "ul",
    "am", "im", "um",
    "an", "in", "un",
    "ar", "ir", "ur",
    "as", "is", "us",
    "at", "it", "ut",
    "az", "iz", "uz",
    "lugal", "dumu", "nita", "munus", "iti", "nam", "dub", "sar",
    "ninda", "udu", "kug", "gal", "tur", "mah",
]

# Linear B syllable inventory (Mycenaean Greek)
_LINEAR_B_SYLLABLES = [
    "a", "e", "i", "o", "u",
    "da", "de", "di", "do", "du",
    "ja", "je", "jo",
    "ka", "ke", "ki", "ko", "ku",
    "ma", "me", "mi", "mo", "mu",
    "na", "ne", "ni", "no", "nu",
    "pa", "pe", "pi", "po", "pu",
    "qa", "qe", "qi", "qo",
    "ra", "re", "ri", "ro", "ru",
    "sa", "se", "si", "so", "su",
    "ta", "te", "ti", "to", "tu",
    "wa", "we", "wi", "wo",
    "za", "ze", "zo",
]

_SYLLABLE_INVENTORIES: dict[str, list[str]] = {
    "sumerian": _SUMERIAN_SYLLABLES,
    "linear_b": _LINEAR_B_SYLLABLES,
    "generic": _SUMERIAN_SYLLABLES,  # default to Sumerian-like
}

# ── Sign classification ───────────────────────────────────────────────


def classify_signs(
    inscriptions: list[list[str]],
    flat_sequence: list[str],
) -> dict[str, dict[str, Any]]:
    """Classify each unique sign as logogram, determinative, or syllabogram.

    Args:
        inscriptions: list of inscription sequences (each is a list of signs).
        flat_sequence: flat concatenation of all signs.

    Returns:
        dict mapping sign -> {type, frequency, boundary_bias, isolation_rate,
        evidence}
    """
    freq = Counter(flat_sequence)
    total = len(flat_sequence)

    initial_count: dict[str, int] = defaultdict(int)
    terminal_count: dict[str, int] = defaultdict(int)
    alone_count: dict[str, int] = defaultdict(int)
    insc_count: dict[str, int] = defaultdict(int)

    for insc in inscriptions:
        if not insc:
            continue
        for sign in insc:
            insc_count[sign] += 1
        if len(insc) == 1:
            alone_count[insc[0]] += 1
        else:
            initial_count[insc[0]] += 1
            terminal_count[insc[-1]] += 1

    result: dict[str, dict[str, Any]] = {}

    for sign, count in freq.items():
        rel_freq = count / total if total > 0 else 0.0
        occ = insc_count.get(sign, 1)

        init_rate = initial_count.get(sign, 0) / occ
        term_rate = terminal_count.get(sign, 0) / occ
        boundary_bias = init_rate + term_rate  # 0=pure medial, up to 2
        isolation_rate = alone_count.get(sign, 0) / occ

        # Classification heuristics
        if isolation_rate >= 0.4:
            sign_type = "logogram"
            evidence = "appears alone in ≥40% of occurrences"
        elif init_rate >= 0.8 and term_rate < 0.2:
            sign_type = "determinative"
            evidence = "strong initial position bias (≥80%)"
        elif term_rate >= 0.8 and init_rate < 0.2:
            sign_type = "determinative"
            evidence = "strong terminal position bias (≥80%)"
        elif boundary_bias <= 0.4:
            sign_type = "syllabogram"
            evidence = "predominantly medial position"
        else:
            sign_type = "syllabogram"
            evidence = "mixed position — likely syllabic"

        result[sign] = {
            "type": sign_type,
            "frequency": count,
            "relative_frequency": round(rel_freq, 5),
            "boundary_bias": round(boundary_bias, 3),
            "isolation_rate": round(isolation_rate, 3),
            "evidence": evidence,
        }

    return result


# ── Vowel/consonant affinity analysis ────────────────────────────────


def compute_affinity(
    inscriptions: list[list[str]],
    syllabograms: list[str],
    top_n: int = 30,
    window: int = 2,
    threshold: float | None = None,
) -> dict[str, Any]:
    """Ventris-style vowel/consonant affinity clustering.

    Uses GPU-accelerated cosine similarity on context frequency vectors,
    replacing the previous binary Jaccard metric which was too sparse.

    Algorithm (Ventris 1953 / Chadwick 1967, computational formulation):
      LEFT-context similarity  → VOWEL affinity  (row in CV grid)
        Signs sharing the same vowel appear after similar predecessor signs.
      RIGHT-context similarity → CONSONANT affinity (column in CV grid)
        Signs sharing the same consonant appear before similar successor signs.

    GPU path: N×N cosine matrix via torch/cupy tensor matmul.
    Numpy path: vectorised N×N matmul.
    Fallback: pairwise Python computation.

    Args:
        inscriptions: inscription-level sequences.
        syllabograms:  list of signs classified as syllabograms.
        top_n:         number of top-frequency syllabograms to analyse.
        window:        context window size in signs (default 2).
        threshold:     cosine similarity threshold for clustering
                       (auto-scaled by corpus size if None).

    Returns:
        dict with vowel_groups, consonant_groups, similarity matrices,
        syllabograms_analysed, and acceleration tier used.
    """
    from glossa_lab.accelerate import gpu_info, ventris_affinity_gpu  # noqa: I001

    syl_set = set(syllabograms)

    # Select top-N syllabograms by frequency
    all_freq: Counter = Counter(
        s for insc in inscriptions for s in insc if s in syl_set
    )
    if len(all_freq) < 2:
        return {
            "vowel_groups": [], "consonant_groups": [],
            "note": "insufficient syllabogram data",
        }

    top_syls = [s for s, _ in all_freq.most_common(top_n)]
    n = len(top_syls)

    # Adaptive threshold: smaller corpora need lower threshold
    total_tokens = sum(len(i) for i in inscriptions)
    if threshold is None:
        if total_tokens < 500:
            threshold = 0.05
        elif total_tokens < 2000:
            threshold = 0.10
        else:
            threshold = 0.15

    # GPU-backed cosine similarity matrices
    # left_sim[i,j]  = cosine sim of left-context vectors  → vowel affinity
    # right_sim[i,j] = cosine sim of right-context vectors → consonant affinity
    left_sim, right_sim = ventris_affinity_gpu(inscriptions, top_syls, window=window)

    accel = gpu_info()
    tier = accel.get("tier_name", "cpu")

    # Clustering using similarity matrix (index-based, avoids re-computing)
    vowel_groups    = _cluster_by_sim_matrix(n, left_sim,  threshold, linkage="complete")
    consonant_groups = _cluster_by_sim_matrix(n, right_sim, threshold, linkage="complete")

    # Reconstruct sign-name groups
    def _idx_to_signs(groups: list[list[int]]) -> list[list[str]]:
        return [[top_syls[i] for i in g] for g in groups if len(g) > 1]

    # Return similarity matrix as nested list for serialisation
    def _to_list(mat: Any) -> list[list[float]]:
        try:
            return [[round(float(mat[i][j]), 4) for j in range(n)] for i in range(n)]
        except Exception:
            return []

    # Also extract top-N most similar pairs (useful without needing perfect clustering)
    def _top_pairs(sim_mat: Any, signs: list[str], top_n: int = 20) -> list[dict]:
        pairs: list[dict] = []
        for i in range(len(signs)):
            for j in range(i + 1, len(signs)):
                s = float(sim_mat[i][j])
                if s > 0.01:
                    pairs.append({"a": signs[i], "b": signs[j], "sim": round(s, 4)})
        pairs.sort(key=lambda p: p["sim"], reverse=True)
        return pairs[:top_n]

    return {
        "vowel_groups":          _idx_to_signs(vowel_groups),
        "consonant_groups":      _idx_to_signs(consonant_groups),
        "top_vowel_pairs":       _top_pairs(left_sim,  top_syls, top_n=20),
        "top_consonant_pairs":   _top_pairs(right_sim, top_syls, top_n=20),
        "syllabograms_analysed": top_syls,
        "n_syllabograms":        n,
        "threshold_used":        threshold,
        "acceleration":          tier,
        "vowel_sim_matrix":      _to_list(left_sim),
        "consonant_sim_matrix":  _to_list(right_sim),
    }


def _cluster_by_sim_matrix(
    n: int,
    sim_matrix: Any,
    threshold: float,
    max_cluster_size: int = 12,
    linkage: str = "complete",
) -> list[list[int]]:
    """Agglomerative clustering on a pre-computed N×N cosine similarity matrix.

    Uses COMPLETE-LINKAGE by default (avoids the single-linkage chaining
    problem that merges all signs into one giant cluster).

    Complete linkage: two clusters merge only if the MINIMUM pairwise
    similarity between them exceeds the threshold (strictest requirement).
    This produces compact, well-separated clusters suitable for the
    Ventris grid (row/column groupings of 3-12 signs).

    Args:
        n:                Number of signs.
        sim_matrix:       N×N cosine similarity matrix.
        threshold:        Minimum similarity to merge clusters.
        max_cluster_size: Don't merge if result would exceed this size.
        linkage:          'complete' (default), 'single', or 'average'.

    Returns:
        List of clusters, each a list of sign indices.
    """
    clusters: list[list[int]] = [[i] for i in range(n)]

    changed = True
    while changed:
        changed = False
        best_sim = threshold
        best_i, best_j = -1, -1

        for ci in range(len(clusters)):
            for cj in range(ci + 1, len(clusters)):
                if len(clusters[ci]) + len(clusters[cj]) > max_cluster_size:
                    continue  # skip merges that would create over-large clusters

                pairs = [
                    float(sim_matrix[a][b])
                    for a in clusters[ci]
                    for b in clusters[cj]
                ]

                if linkage == "complete":
                    sim = min(pairs)       # all pairs must exceed threshold
                elif linkage == "average":
                    sim = sum(pairs) / len(pairs)
                else:                      # single
                    sim = max(pairs)

                if sim > best_sim:
                    best_sim = sim
                    best_i, best_j = ci, cj

        if best_i >= 0:
            merged = clusters[best_i] + clusters[best_j]
            clusters = [
                c for k, c in enumerate(clusters)
                if k != best_i and k != best_j
            ]
            clusters.append(merged)
            changed = True

    return clusters


# ── Candidate readings ────────────────────────────────────────────────


def propose_readings(
    sign_classification: dict[str, dict[str, Any]],
    affinity: dict[str, Any],
    syllable_inventory: list[str],
    inscriptions: list[list[str]],
) -> dict[str, dict[str, Any]]:
    """Assign candidate CV readings to syllabograms.

    Maps each syllabogram to a candidate CV value from the target language
    syllable inventory using frequency-rank matching.

    Args:
        sign_classification: output of classify_signs().
        affinity: output of compute_affinity().
        syllable_inventory: target language syllable list (ordered by
            descending frequency).
        inscriptions: inscription sequences.

    Returns:
        dict mapping sign -> {reading, confidence, method}
    """
    # Frequency-rank the syllabograms
    syl_freq: Counter = Counter()
    for insc in inscriptions:
        for sign in insc:
            if sign_classification.get(sign, {}).get("type") == "syllabogram":
                syl_freq[sign] += 1

    ranked_syls = [s for s, _ in syl_freq.most_common()]
    ranked_inv = list(syllable_inventory)

    readings: dict[str, dict[str, Any]] = {}
    for rank, sign in enumerate(ranked_syls):
        if rank < len(ranked_inv):
            reading = ranked_inv[rank]
            # Confidence decays with rank (most frequent = highest confidence)
            confidence = max(0.1, 1.0 - rank / max(len(ranked_syls), 1))
            readings[sign] = {
                "reading": reading,
                "confidence": round(confidence, 3),
                "method": "frequency-rank matching",
            }
        else:
            readings[sign] = {
                "reading": "?",
                "confidence": 0.0,
                "method": "no inventory match (sign rank exceeds inventory)",
            }

    return readings


# ── Word pattern matching ─────────────────────────────────────────────


def extract_candidate_words(
    inscriptions: list[list[str]],
    sign_classification: dict[str, dict[str, Any]],
    readings: dict[str, dict[str, Any]],
    vocabulary: dict[str, str] | None = None,
    max_length: int = 6,
) -> list[dict[str, Any]]:
    """Extract phonetic sequences and match against vocabulary.

    Runs of syllabograms within inscriptions are concatenated using proposed
    readings and checked against the target vocabulary.

    Args:
        inscriptions: inscription sequences.
        sign_classification: output of classify_signs().
        readings: output of propose_readings().
        vocabulary: optional {reading: meaning} word list.
        max_length: maximum syllabogram run to concatenate.

    Returns:
        list of {sequence, reading, word_length, score, match, meaning}
    """
    vocab = vocabulary or {}
    seen: set[str] = set()
    results: list[dict[str, Any]] = []

    for insc in inscriptions:
        # Extract runs of syllabograms
        run: list[str] = []
        for sign in insc:
            stype = sign_classification.get(sign, {}).get("type", "syllabogram")
            if stype == "syllabogram":
                run.append(sign)
                if len(run) >= max_length:
                    _emit_candidate(run, readings, vocab, seen, results)
                    run = []
            else:
                if run:
                    _emit_candidate(run, readings, vocab, seen, results)
                    run = []
        if run:
            _emit_candidate(run, readings, vocab, seen, results)

    # Sort by score descending
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:50]  # cap output


def _emit_candidate(
    run: list[str],
    readings: dict[str, dict[str, Any]],
    vocab: dict[str, str],
    seen: set[str],
    out: list[dict[str, Any]],
) -> None:
    if len(run) < 2:
        return
    key = "|".join(run)
    if key in seen:
        return
    seen.add(key)

    parts = [readings.get(s, {}).get("reading", "?") for s in run]
    combined = "".join(parts)
    confidences = [readings.get(s, {}).get("confidence", 0.0) for s in run]
    avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

    match = combined in vocab
    meaning = vocab.get(combined, "")
    score = avg_conf * (2.0 if match else 1.0)

    out.append({
        "signs": run,
        "readings": parts,
        "combined_reading": combined,
        "word_length": len(run),
        "avg_confidence": round(avg_conf, 3),
        "score": round(score, 3),
        "vocabulary_match": match,
        "meaning": meaning,
    })


# ── Main analysis function ────────────────────────────────────────────


def analyse_logosyllabic(
    inscriptions: list[list[str]],
    target_language: str = "generic",
    max_word_length: int = 6,
    vocabulary: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Full logosyllabic analysis pipeline.

    Args:
        inscriptions: list of inscription sequences (list of sign lists).
        target_language: 'sumerian', 'linear_b', or 'generic'.
        max_word_length: max syllabogram run to consider as a word.
        vocabulary: optional {word: meaning} dict for target language.

    Returns:
        Full analysis result dict.
    """
    flat = [sign for insc in inscriptions for sign in insc]

    if not flat:
        return {
            "error": "Empty input",
            "sign_count": 0,
            "unique_signs": 0,
        }

    syllable_inventory = _SYLLABLE_INVENTORIES.get(
        target_language, _SYLLABLE_INVENTORIES["generic"]
    )

    # 1. Classify signs
    classification = classify_signs(inscriptions, flat)

    syllabograms = [
        s for s, info in classification.items()
        if info["type"] == "syllabogram"
    ]
    logograms = [
        s for s, info in classification.items()
        if info["type"] == "logogram"
    ]
    determinatives = [
        s for s, info in classification.items()
        if info["type"] == "determinative"
    ]

    # 2. Affinity analysis
    affinity = compute_affinity(inscriptions, syllabograms)

    # 3. Propose readings
    readings = propose_readings(
        classification, affinity, syllable_inventory, inscriptions,
    )

    # 4. Candidate words
    candidates = extract_candidate_words(
        inscriptions, classification, readings,
        vocabulary=vocabulary,
        max_length=max_word_length,
    )

    vocab_matches = [c for c in candidates if c["vocabulary_match"]]

    return {
        "target_language": target_language,
        "sign_count": len(flat),
        "unique_signs": len(classification),
        "inscription_count": len(inscriptions),
        "sign_classification": classification,
        "summary": {
            "logograms": len(logograms),
            "syllabograms": len(syllabograms),
            "determinatives": len(determinatives),
            "logogram_signs": logograms[:20],
            "syllabogram_signs": syllabograms[:30],
            "determinative_signs": determinatives[:10],
        },
        "affinity": affinity,
        "proposed_readings": readings,
        "candidate_words": candidates,
        "vocabulary_matches": vocab_matches,
        "vocabulary_match_count": len(vocab_matches),
    }


# ── Pipeline entry point ──────────────────────────────────────────────


@register_pipeline("logosyllabic")
async def run_logosyllabic(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point for logosyllabic analysis.

    Params:
        text_id (required): text corpus ID (content must be list of signs,
            each inscription separated by a sentinel like None/'' or passed
            as a flat sequence — each symbol is treated as a single sign).
        target_language: 'sumerian', 'linear_b', or 'generic' (default).
        max_word_length: max syllabogram run length (default 6).
        inscription_delimiter: symbol that marks inscription boundaries
            (default: treat entire flat sequence as one inscription).
    """
    from glossa_lab.database import get_db

    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing required param: text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    content = text["content"]
    if not isinstance(content, list):
        raise ValueError("Text content must be a list of symbols/signs")

    target_language = params.get("target_language", "generic")
    max_word_length = params.get("max_word_length", 6)
    delimiter = params.get("inscription_delimiter", None)

    # Split into inscriptions
    if delimiter:
        inscriptions: list[list[str]] = []
        current: list[str] = []
        for sign in content:
            if sign == delimiter:
                if current:
                    inscriptions.append(current)
                    current = []
            else:
                current.append(sign)
        if current:
            inscriptions.append(current)
    else:
        # Treat as single inscription (or apply a fixed-length segmentation)
        # For practical analysis, chunk into segments of 3-8 signs
        chunk_size = params.get("chunk_size", 5)
        inscriptions = [
            content[i: i + chunk_size]
            for i in range(0, len(content), chunk_size)
            if content[i: i + chunk_size]
        ]

    result = analyse_logosyllabic(
        inscriptions,
        target_language=target_language,
        max_word_length=max_word_length,
    )

    result["text_id"] = text_id
    result["text_name"] = text.get("name", "")
    result["corpus_type"] = text.get("corpus_type", "")
    return result
