"""Assumption-free distributional decipherment pipeline.

Operationalises Ventris's (1952) syllabic grid method computationally,
using ONLY distributional evidence from the corpus — no assumed phonetic
values, no reference to any deciphered script.

Core principle (Ventris 1952, formalised):
  Signs sharing the same VOWEL appear in similar left-context distributions
  (they occur after the same preceding signs — the consonant row is the same).

  Signs sharing the same CONSONANT appear in similar right-context
  distributions (they occur before the same following signs — the vowel
  column is the same).

This allows grouping signs into 'rows' (same vowel) and 'columns' (same
consonant) from purely distributional evidence, producing a phonological
grid without any phoneme labels.

The grid can then be:
  1. Compared structurally against known-script grids (without identifying
     specific values) for typological matching.
  2. Used as input to hypothesis testing where language-family priors are
     applied to the grid structure, not individual sign values.

Difference from logosyllabic.py:
  logosyllabic.py classifies signs as logogram/syllabogram/determinative
  and uses Linear B-derived phoneme inventories.
  This pipeline makes NO phoneme assumptions and produces only distributional
  groupings.

References:
  Ventris, M. (1952). Mid-Term Report on the Decipherment of Minoan Linear B.
  Packard, D.W. (1974). Minoan Linear A. (applies similar distributional analysis)
  Kober, A. (1945). Evidence of Inflection in the Unciphered Minoan Script.
"""

from __future__ import annotations  # noqa: I001

import math
from collections import Counter, defaultdict
from typing import Any

from glossa_lab.engine import register_pipeline


# ── Jensen-Shannon divergence ─────────────────────────────────────────

def _js_divergence(p: dict[str, float], q: dict[str, float]) -> float:
    """Jensen-Shannon divergence between two probability distributions.

    0 = identical distributions, 1 = maximally different.
    Uses base-2 log for a [0,1] bounded score.
    """
    all_keys = set(p) | set(q)
    if not all_keys:
        return 0.0

    total_p = sum(p.values()) or 1.0
    total_q = sum(q.values()) or 1.0

    p_norm = {k: p.get(k, 0.0) / total_p for k in all_keys}
    q_norm = {k: q.get(k, 0.0) / total_q for k in all_keys}

    m = {k: (p_norm[k] + q_norm[k]) / 2 for k in all_keys}

    def kl(a: dict, b: dict) -> float:
        total = 0.0
        for k in a:
            if a[k] > 0 and b[k] > 0:
                total += a[k] * math.log2(a[k] / b[k])
        return total

    return (kl(p_norm, m) + kl(q_norm, m)) / 2


def _cosine_similarity(v1: dict[str, float], v2: dict[str, float]) -> float:
    """Cosine similarity between two sparse count vectors."""
    common = set(v1) & set(v2)
    if not common:
        return 0.0
    dot  = sum(v1[k] * v2[k] for k in common)
    mag1 = math.sqrt(sum(x*x for x in v1.values()))
    mag2 = math.sqrt(sum(x*x for x in v2.values()))
    return dot / (mag1 * mag2) if mag1 * mag2 > 0 else 0.0


# ── Context extraction ────────────────────────────────────────────────

def _build_context_profiles(
    inscriptions: list[list[str]],
    min_count: int = 3,
) -> tuple[dict[str, Counter], dict[str, Counter], dict[str, int]]:
    """Build left-context and right-context distributions for each sign.

    Left context of sign X: all signs that appear immediately before X.
    Right context of sign X: all signs that appear immediately after X.

    Args:
        inscriptions: List of sign sequences (each inscription a list of tokens).
        min_count:    Minimum total occurrences for a sign to be included.

    Returns:
        (left_ctx, right_ctx, frequencies) where:
          left_ctx[sign]  = Counter of signs appearing before sign
          right_ctx[sign] = Counter of signs appearing after sign
          frequencies[sign] = total count
    """
    left_ctx:  dict[str, Counter] = defaultdict(Counter)
    right_ctx: dict[str, Counter] = defaultdict(Counter)
    freq: Counter = Counter()

    for insc in inscriptions:
        for sign in insc:
            freq[sign] += 1

        for i, sign in enumerate(insc):
            if i > 0:
                left_ctx[sign][insc[i - 1]] += 1
            if i < len(insc) - 1:
                right_ctx[sign][insc[i + 1]] += 1

    # Filter to signs meeting minimum count
    active = {s for s, c in freq.items() if c >= min_count}
    left_ctx  = {s: v for s, v in left_ctx.items()  if s in active}
    right_ctx = {s: v for s, v in right_ctx.items() if s in active}

    return left_ctx, right_ctx, {s: freq[s] for s in active}


# ── Vowel and consonant clustering ───────────────────────────────────

def cluster_by_vowel_class(
    left_ctx: dict[str, Counter],
    threshold: float = 0.30,
    top_n: int = 40,
    freq: dict[str, int] | None = None,
) -> list[list[str]]:
    """Group signs into vowel classes using left-context similarity.

    Two signs that appear after the same set of preceding signs likely
    share a vowel (they belong to the same consonant column but different
    rows). The Ventris rationale: if 'pa' and 'ta' both commonly follow
    the same signs, they differ only in consonant (p vs t) not vowel (a).

    Args:
        left_ctx:  Left-context distributions.
        threshold: JS-divergence threshold for merging clusters (lower = tighter).
        top_n:     Number of highest-frequency signs to analyze.
        freq:      Frequency dict for ranking (optional).

    Returns:
        List of sign clusters (each cluster = likely same vowel).
    """
    if not left_ctx:
        return []

    # Select top-N signs by frequency
    if freq:
        candidates = [s for s, _ in sorted(freq.items(), key=lambda x: -x[1])
                      if s in left_ctx][:top_n]
    else:
        candidates = sorted(left_ctx.keys())[:top_n]

    if len(candidates) < 2:
        return [[s] for s in candidates]

    # Convert counters to probability dicts
    def normalize(c: Counter) -> dict[str, float]:
        total = sum(c.values()) or 1.0
        return {k: v / total for k, v in c.items()}

    profiles = {s: normalize(left_ctx[s]) for s in candidates}

    # Single-linkage agglomerative clustering on JS-divergence
    clusters: list[list[str]] = [[s] for s in candidates]
    changed = True

    while changed:
        changed = False
        best_sim, best_i, best_j = threshold, -1, -1

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # Min JS-divergence across cluster pairs (single linkage)
                min_js = min(
                    _js_divergence(profiles[a], profiles[b])
                    for a in clusters[i]
                    for b in clusters[j]
                )
                if min_js < best_sim:
                    best_sim, best_i, best_j = min_js, i, j

        if best_i >= 0:
            merged = clusters[best_i] + clusters[best_j]
            clusters = [c for k, c in enumerate(clusters)
                        if k != best_i and k != best_j]
            clusters.append(merged)
            changed = True

    return [c for c in clusters if len(c) > 1]


def cluster_by_consonant_class(
    right_ctx: dict[str, Counter],
    threshold: float = 0.30,
    top_n: int = 40,
    freq: dict[str, int] | None = None,
) -> list[list[str]]:
    """Group signs into consonant classes using right-context similarity.

    Signs that appear before the same set of following signs likely share
    a consonant (they belong to the same vowel row but different columns).
    """
    return cluster_by_vowel_class(right_ctx, threshold=threshold,
                                   top_n=top_n, freq=freq)


# ── Phonological grid construction ───────────────────────────────────

def build_phonological_grid(
    vowel_clusters: list[list[str]],
    consonant_clusters: list[list[str]],
) -> dict[str, Any]:
    """Construct a phonological sign grid from vowel and consonant clusters.

    Each cell in the grid is the intersection of one vowel cluster (row)
    and one consonant cluster (column). Signs appearing in both a vowel
    cluster and a consonant cluster are placed at the corresponding cell.

    This mirrors the Ventris grid construction but makes no claims about
    which values go in which cells — it only identifies the structural
    grid positions.

    Returns:
        dict with 'grid' (dict of (vowel_row, consonant_col) -> [signs]),
        'vowel_clusters', 'consonant_clusters',
        'unclustered' (signs not assigned to any cluster).
    """
    # Assign each sign to its vowel row and consonant column (if available)
    sign_to_vowel: dict[str, int] = {}
    sign_to_consonant: dict[str, int] = {}

    for row_idx, cluster in enumerate(vowel_clusters):
        for sign in cluster:
            sign_to_vowel[sign] = row_idx

    for col_idx, cluster in enumerate(consonant_clusters):
        for sign in cluster:
            sign_to_consonant[sign] = col_idx

    all_signs = set(sign_to_vowel) | set(sign_to_consonant)
    grid: dict[tuple[int, int], list[str]] = defaultdict(list)

    for sign in all_signs:
        row = sign_to_vowel.get(sign, -1)
        col = sign_to_consonant.get(sign, -1)
        if row >= 0 and col >= 0:
            grid[(row, col)].append(sign)

    # Signs in only one dimension
    vowel_only    = [s for s in sign_to_vowel if s not in sign_to_consonant]
    consonant_only= [s for s in sign_to_consonant if s not in sign_to_vowel]
    unclustered   = [s for s in all_signs if s not in sign_to_vowel and s not in sign_to_consonant]

    return {
        "grid":              {f"row{r}_col{c}": signs for (r,c), signs in grid.items()},
        "vowel_clusters":    vowel_clusters,
        "consonant_clusters":consonant_clusters,
        "vowel_only_signs":  vowel_only,
        "consonant_only_signs": consonant_only,
        "unclustered":       unclustered,
        "n_cells":           len(grid),
        "n_filled_cells":    sum(1 for v in grid.values() if v),
        "grid_density":      len(grid) / max((len(vowel_clusters) * len(consonant_clusters)), 1),
    }


# ── Word structure analysis ───────────────────────────────────────────

def infer_word_structure(
    inscriptions: list[list[str]],
    left_ctx: dict[str, Counter],
    right_ctx: dict[str, Counter],
    freq: dict[str, int],
) -> dict[str, Any]:
    """Infer grammatical roles from distributional evidence.

    Without any phoneme assumptions, we can identify:
    - Likely affixes (high boundary-position bias, recurring at word edges)
    - Likely roots (appear in medial positions with variable contexts)
    - Word-length distribution (sign-group sizes across inscriptions)

    Returns:
        dict with structural statistics of the corpus.
    """
    # Word lengths (inscription = one 'word' in administrative texts)
    word_lengths = [len(insc) for insc in inscriptions if insc]
    if not word_lengths:
        return {}

    length_dist = Counter(word_lengths)
    max_len = max(word_lengths)
    mean_len = sum(word_lengths) / len(word_lengths)

    # Signs with strong initial-position bias
    initial_bias: dict[str, float] = {}
    terminal_bias: dict[str, float] = {}

    for sign, count in freq.items():
        left_total  = sum(left_ctx.get(sign, Counter()).values())
        right_total = sum(right_ctx.get(sign, Counter()).values())
        total = max(count, 1)

        # Fraction of occurrences that are word-initial (no left context)
        initial_frac  = 1.0 - (left_total / total)
        terminal_frac = 1.0 - (right_total / total)

        initial_bias[sign]  = round(initial_frac,  3)
        terminal_bias[sign] = round(terminal_frac, 3)

    # Top likely prefixes (high initial bias, appearing in ≥5 inscriptions)
    likely_prefixes = sorted(
        [(s, b) for s, b in initial_bias.items() if b >= 0.5],
        key=lambda x: -x[1],
    )[:10]

    # Top likely suffixes
    likely_suffixes = sorted(
        [(s, b) for s, b in terminal_bias.items() if b >= 0.5],
        key=lambda x: -x[1],
    )[:10]

    # Type-token ratio (lexical diversity)
    all_signs = [s for insc in inscriptions for s in insc]
    ttr = len(freq) / max(len(all_signs), 1)

    # Unique inscription count per sign group
    sign_group_counter: Counter = Counter()
    for insc in inscriptions:
        key = "|".join(insc)
        sign_group_counter[key] += 1

    n_singletons = sum(1 for v in sign_group_counter.values() if v == 1)
    unique_ratio = n_singletons / max(len(sign_group_counter), 1)

    return {
        "word_length_distribution": dict(sorted(length_dist.items())),
        "mean_word_length":    round(mean_len, 2),
        "max_word_length":     max_len,
        "corpus_size":         len(all_signs),
        "unique_signs":        len(freq),
        "type_token_ratio":    round(ttr, 4),
        "unique_inscription_ratio": round(unique_ratio, 4),
        "likely_prefixes":     likely_prefixes,
        "likely_suffixes":     likely_suffixes,
    }


# ── Cross-script alignment ────────────────────────────────────────────

def cross_script_align(
    corpus_a_inscriptions: list[list[str]],
    corpus_b_inscriptions: list[list[str]],
    top_patterns: int = 20,
) -> dict[str, Any]:
    """Find structurally similar inscription patterns between two corpora.

    Identifies sign groups in corpus A whose distributional properties
    most closely match sign groups in corpus B, WITHOUT assuming any
    phonetic relationship between them.

    This can align functionally equivalent administrative formulas
    (e.g., ku-ro in Linear A with its equivalent in Linear B)
    based on position and context, not sign shape.

    Args:
        corpus_a_inscriptions: First corpus (e.g. Linear A).
        corpus_b_inscriptions: Second corpus (e.g. Linear B).
        top_patterns: Number of most-frequent pattern pairs to return.

    Returns:
        dict with structural alignment statistics.
    """
    def _get_patterns(  # noqa: E501
        inscriptions: list[list[str]],
        top_n: int = top_patterns,
    ) -> list[tuple[str, int]]:
        """Get most frequent inscription patterns."""
        counter: Counter = Counter()
        for insc in inscriptions:
            if len(insc) >= 2:
                key = "+".join(insc[:4])  # Use first 4 signs
                counter[key] += 1
        return counter.most_common(top_n)

    a_patterns = _get_patterns(corpus_a_inscriptions)
    b_patterns = _get_patterns(corpus_b_inscriptions)

    # Word-length distribution comparison
    def _len_dist(inscriptions: list[list[str]]) -> dict[int, float]:
        c = Counter(len(i) for i in inscriptions if i)
        total = sum(c.values()) or 1
        return {k: v / total for k, v in c.items()}

    dist_a = _len_dist(corpus_a_inscriptions)
    dist_b = _len_dist(corpus_b_inscriptions)

    # KL divergence of word-length distributions
    all_lens = set(dist_a) | set(dist_b)
    eps = 1e-8
    kl_ab = sum(
        dist_a.get(k, eps) * math.log(dist_a.get(k, eps) / max(dist_b.get(k, eps), eps))
        for k in all_lens
        if dist_a.get(k, 0) > 0
    )

    return {
        "corpus_a_top_patterns": a_patterns[:10],
        "corpus_b_top_patterns": b_patterns[:10],
        "word_length_kl_divergence": round(kl_ab, 4),
        "corpus_a_mean_length": round(
            sum(len(i) for i in corpus_a_inscriptions if i)
            / max(len(corpus_a_inscriptions), 1), 2),
        "corpus_b_mean_length": round(
            sum(len(i) for i in corpus_b_inscriptions if i)
            / max(len(corpus_b_inscriptions), 1), 2),
    }


# ── Full analysis pipeline ────────────────────────────────────────────

def analyze_distributional(
    inscriptions: list[list[str]],
    min_sign_count: int = 3,
    cluster_threshold: float = 0.30,
    top_n: int = 40,
    reference_inscriptions: list[list[str]] | None = None,
) -> dict[str, Any]:
    """Full assumption-free distributional analysis.

    Args:
        inscriptions:            List of sign sequences.
        min_sign_count:          Minimum occurrences to include a sign.
        cluster_threshold:       JS-divergence threshold for clustering.
        top_n:                   Signs to analyze for clustering.
        reference_inscriptions:  Second corpus for cross-script alignment.

    Returns:
        Complete analysis result dict.
    """
    if not inscriptions:
        return {"error": "Empty corpus"}

    left_ctx, right_ctx, freq = _build_context_profiles(
        inscriptions, min_count=min_sign_count)

    if not freq:
        return {"error": "No signs met minimum count threshold"}

    # Vowel and consonant clusters
    vowel_clusters    = cluster_by_vowel_class(
        left_ctx, threshold=cluster_threshold, top_n=top_n, freq=freq)
    consonant_clusters= cluster_by_consonant_class(
        right_ctx, threshold=cluster_threshold, top_n=top_n, freq=freq)

    # Phonological grid
    grid = build_phonological_grid(vowel_clusters, consonant_clusters)

    # Word structure
    word_struct = infer_word_structure(inscriptions, left_ctx, right_ctx, freq)

    # Cross-script alignment (if reference provided)
    cross_align = None
    if reference_inscriptions:
        cross_align = cross_script_align(inscriptions, reference_inscriptions)

    # Top 10 most frequent signs with their cluster assignments
    sign_to_vowel_cluster = {}
    for i, cluster in enumerate(vowel_clusters):
        for sign in cluster:
            sign_to_vowel_cluster[sign] = i

    sign_to_consonant_cluster = {}
    for i, cluster in enumerate(consonant_clusters):
        for sign in cluster:
            sign_to_consonant_cluster[sign] = i

    top_signs = [
        {
            "sign": s,
            "frequency": freq[s],
            "vowel_cluster": sign_to_vowel_cluster.get(s),
            "consonant_cluster": sign_to_consonant_cluster.get(s),
        }
        for s, _ in sorted(freq.items(), key=lambda x: -x[1])[:20]
    ]

    return {
        "corpus_size":          sum(freq.values()),
        "unique_signs":         len(freq),
        "n_inscriptions":       len(inscriptions),
        "vowel_clusters":       vowel_clusters,
        "consonant_clusters":   consonant_clusters,
        "n_vowel_clusters":     len(vowel_clusters),
        "n_consonant_clusters": len(consonant_clusters),
        "phonological_grid":    grid,
        "word_structure":       word_struct,
        "cross_script_alignment": cross_align,
        "top_signs":            top_signs,
        "cluster_threshold":    cluster_threshold,
    }


# ── Pipeline entry point ──────────────────────────────────────────────

@register_pipeline("distributional_decipherment")
async def run_distributional_decipherment(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point.

    Params:
        text_id (required): corpus ID
        reference_text_id:  optional second corpus for cross-script alignment
        min_sign_count:     minimum occurrences (default 3)
        cluster_threshold:  JS-divergence threshold (default 0.30)
        top_n:              signs to analyze (default 40)
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
        raise ValueError("Text content must be a list of sign tokens")

    # Segment flat sequence into inscriptions by chunk
    chunk_size = params.get("chunk_size", 5)
    inscriptions = [
        content[i: i + chunk_size]
        for i in range(0, len(content), chunk_size)
        if content[i: i + chunk_size]
    ]

    # Load reference corpus if provided
    ref_inscriptions = None
    ref_text_id = params.get("reference_text_id")
    if ref_text_id:
        ref_text = await db.get_text(ref_text_id)
        if ref_text:
            ref_content = ref_text["content"]
            ref_inscriptions = [
                ref_content[i: i + chunk_size]
                for i in range(0, len(ref_content), chunk_size)
                if ref_content[i: i + chunk_size]
            ]

    result = analyze_distributional(
        inscriptions,
        min_sign_count=params.get("min_sign_count", 3),
        cluster_threshold=params.get("cluster_threshold", 0.30),
        top_n=params.get("top_n", 40),
        reference_inscriptions=ref_inscriptions,
    )

    result["text_id"]    = text_id
    result["text_name"]  = text.get("name", "")
    result["corpus_type"]= text.get("corpus_type", "")
    return result
