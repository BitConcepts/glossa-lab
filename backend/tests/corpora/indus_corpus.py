"""Indus script corpus generator.

Generates a statistically representative sample of Indus script
inscriptions based on published data from:
  - Mahadevan (1977) concordance: 417 signs, ~7000 occurrences
  - Yadav et al. (2010) PLoS ONE: Zipf-Mandelbrot distribution,
    bigram correlations, average inscription length ~5 signs

The generated corpus reproduces the *statistical properties* that
Rao et al. (2009) analyzed — it is NOT the actual M77 corpus.
Sign IDs follow Mahadevan's numbering (1-417).

Most common signs from published data:
  342 (jar/vessel) — most frequent, often terminal
  99  (comb/rake)
  267 (U-shape)
  59  (diamond)
  336 (fish)
  89  (man)
  391 (arrow)
  176 (two short strokes)
  328 (bearer)
  48  (three vertical lines)
"""

from __future__ import annotations

import random


# Top-40 most frequent signs with approximate relative frequencies
# derived from published rank-frequency plots (Yadav et al. 2010, Fig 2-3)
_TOP_SIGNS = [
    (342, 0.080), (99, 0.045), (267, 0.040), (59, 0.035),
    (336, 0.030), (89, 0.025), (391, 0.022), (176, 0.020),
    (328, 0.018), (48, 0.016), (211, 0.015), (367, 0.014),
    (65, 0.013), (162, 0.012), (123, 0.011), (87, 0.010),
    (293, 0.010), (51, 0.009), (130, 0.009), (248, 0.008),
    (171, 0.008), (406, 0.008), (360, 0.007), (143, 0.007),
    (240, 0.007), (307, 0.006), (12, 0.006), (395, 0.006),
    (77, 0.005), (283, 0.005), (415, 0.005), (199, 0.005),
    (227, 0.004), (112, 0.004), (305, 0.004), (388, 0.004),
    (55, 0.004), (166, 0.003), (262, 0.003), (147, 0.003),
]

# Common bigram pairs (source → target) from published data
# Sign 342 is predominantly terminal; 267 often precedes 342
_COMMON_BIGRAMS = [
    (267, 342), (99, 342), (59, 342), (336, 342), (89, 267),
    (176, 342), (391, 267), (328, 99), (48, 342), (211, 99),
    (367, 267), (65, 342), (162, 59), (123, 336), (87, 391),
    (293, 89), (51, 267), (130, 99), (248, 342), (171, 59),
]


# ── Archaeological context ─────────────────────────────────────────

# Findspot distribution (approximate, from Fuls 2023)
_FINDSPOTS = [
    ("Mohenjo-daro", 0.45),
    ("Harappa", 0.30),
    ("Lothal", 0.06),
    ("Kalibangan", 0.04),
    ("Dholavira", 0.03),
    ("Chanhu-daro", 0.03),
    ("Banawali", 0.02),
    ("Other", 0.07),
]

# Object type distribution
_OBJECT_TYPES = [
    ("square_seal", 0.50),
    ("rectangular_seal", 0.10),
    ("tablet_incised", 0.15),
    ("tablet_bas_relief", 0.10),
    ("pottery", 0.08),
    ("copper_plate", 0.03),
    ("other", 0.04),
]

# Iconography (animal motifs on seals)
_ICONOGRAPHY = [
    ("unicorn_bull", 0.60),
    ("short_horned_bull", 0.10),
    ("water_buffalo", 0.05),
    ("elephant", 0.04),
    ("rhinoceros", 0.03),
    ("tiger", 0.02),
    ("none", 0.16),
]


def generate_indus_corpus(
    seed: int = 42,
    num_inscriptions: int = 1500,
    num_signs: int = 417,
    include_metadata: bool = False,
) -> list[list[str]]:
    """Generate synthetic Indus inscriptions.

    Returns a list of inscriptions, each being a list of sign ID strings.
    If include_metadata=True, returns list of dicts with signs + archaeological context.
    """
    rng = random.Random(seed)

    # Build sign probability distribution (Zipf-Mandelbrot)
    sign_ids = list(range(1, num_signs + 1))
    top_sign_map = {s: w for s, w in _TOP_SIGNS}

    weights = []
    for sid in sign_ids:
        if sid in top_sign_map:
            weights.append(top_sign_map[sid])
        else:
            # Long tail: small weight for rare signs
            weights.append(0.001)

    total = sum(weights)
    probs = [w / total for w in weights]

    # Build simple bigram transition bias
    bigram_boost: dict[int, dict[int, float]] = {}
    for src, tgt in _COMMON_BIGRAMS:
        bigram_boost.setdefault(src, {})[tgt] = 5.0

    inscriptions = []
    for _ in range(num_inscriptions):
        # Inscription length: predominantly 3-7 signs (avg ~5)
        length = max(1, min(17, int(rng.gauss(5.0, 1.8))))

        signs = []
        for pos in range(length):
            if pos == 0 or not signs:
                # First sign: sample from prior
                chosen = rng.choices(sign_ids, weights=probs, k=1)[0]
            else:
                # Subsequent signs: bigram-biased sampling
                prev = signs[-1]
                adj_weights = list(probs)
                if prev in bigram_boost:
                    for tgt, boost in bigram_boost[prev].items():
                        idx = tgt - 1
                        adj_weights[idx] *= boost
                # Normalize
                total_w = sum(adj_weights)
                adj_weights = [w / total_w for w in adj_weights]
                chosen = rng.choices(sign_ids, weights=adj_weights, k=1)[0]

            signs.append(chosen)

        insc_data = [str(s) for s in signs]
        if include_metadata:
            site = rng.choices(
                [s for s, _ in _FINDSPOTS],
                weights=[w for _, w in _FINDSPOTS],
            )[0]
            obj_type = rng.choices(
                [t for t, _ in _OBJECT_TYPES],
                weights=[w for _, w in _OBJECT_TYPES],
            )[0]
            icon = rng.choices(
                [i for i, _ in _ICONOGRAPHY],
                weights=[w for _, w in _ICONOGRAPHY],
            )[0]
            inscriptions.append({
                "signs": insc_data,
                "findspot": site,
                "object_type": obj_type,
                "iconography": icon,
            })
        else:
            inscriptions.append(insc_data)

    return inscriptions


def generate_indus_flat(seed: int = 42) -> list[str]:
    """Generate flat symbol sequence (all inscriptions concatenated)."""
    inscriptions = generate_indus_corpus(seed=seed)
    flat = []
    for insc in inscriptions:
        flat.extend(insc)
    return flat


def save_indus_fixture(path: str, seed: int = 42) -> None:
    """Save Indus corpus fixture file (one inscription per line, space-separated)."""
    inscriptions = generate_indus_corpus(seed=seed)
    with open(path, "w", encoding="utf-8") as f:
        for insc in inscriptions:
            f.write(" ".join(insc) + "\n")


if __name__ == "__main__":
    import sys
    from pathlib import Path

    out = Path(__file__).parent / "fixtures" / "indus.txt"
    save_indus_fixture(str(out))
    corpus = generate_indus_flat()
    print(f"Generated {len(corpus)} signs across Indus corpus")
    print(f"Unique signs: {len(set(corpus))}")
    print(f"Saved to {out}")
