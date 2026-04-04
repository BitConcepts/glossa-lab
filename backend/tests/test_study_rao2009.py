"""Academic study replication — Rao et al. (2009).

Replicates the block entropy methodology from:
  "Entropic Evidence for Linguistic Structure in the Indus Script"
  Science 324:1165.

Compares normalized block entropy curves for English, DNA, Fortran,
and synthetic baselines against expected ranges from the published study.

This is NOT a full replication (we don't have the Indus corpus or all
the languages), but it validates that our entropy implementation
produces results consistent with the published findings:
  - Linguistic text (English): mid-range entropy
  - DNA: higher entropy than linguistic
  - Fortran: lower entropy than linguistic
  - Random: near maximum
  - Ordered: collapses for N≥2
"""

from glossa_lab.pipelines.block_entropy import compute_block_entropies
from tests.corpora.real import (
    load_dna,
    load_english,
    load_fortran,
    load_indus,
    load_sanskrit,
    load_sumerian,
    load_tamil,
)
from tests.corpora.synthetic import generate_ordered, generate_random


def _get_norm(result: dict, n: int) -> float:
    for entry in result["block_entropies"]:
        if entry["n"] == n:
            return entry["normalized"]
    raise ValueError(f"No entry for n={n}")


# ── English (linguistic system) ──────────────────────────────────────


def test_english_h1_linguistic_range():
    """English character entropy should be in the linguistic range.

    Rao et al. show English characters at H1_norm ≈ 0.78-0.85.
    With only 26 letters and highly non-uniform frequencies (e, t, a
    dominate), normalized H1 is well below 1.0.
    """
    symbols = load_english()
    result = compute_block_entropies(symbols, max_n=4)
    h1 = _get_norm(result, 1)
    assert 0.70 <= h1 <= 0.90, f"English H1_norm={h1}, expected 0.70-0.90"


def test_english_sublinear_growth():
    """English: H2/H1 < 2.0 (correlations between characters)."""
    symbols = load_english()
    result = compute_block_entropies(symbols, max_n=4)
    h1 = _get_norm(result, 1)
    h2 = _get_norm(result, 2)
    ratio = h2 / h1
    assert ratio < 1.90, f"English H2/H1={ratio:.3f}, expected < 1.90"


# ── DNA (non-linguistic, biological) ─────────────────────────────────


def test_dna_h1_higher_than_english():
    """DNA should have higher H1_norm than English.

    DNA uses 4 bases with relatively even frequencies → H1_norm closer
    to 1.0. Rao et al. show DNA entropy higher than linguistic systems.
    """
    eng = compute_block_entropies(load_english(), max_n=2)
    dna = compute_block_entropies(load_dna(), max_n=2)
    eng_h1 = _get_norm(eng, 1)
    dna_h1 = _get_norm(dna, 1)
    assert dna_h1 > eng_h1, f"DNA H1_norm={dna_h1} should be > English H1_norm={eng_h1}"


def test_dna_near_maximum():
    """DNA H1_norm should be high (near-uniform base distribution)."""
    result = compute_block_entropies(load_dna(), max_n=2)
    h1 = _get_norm(result, 1)
    assert h1 >= 0.85, f"DNA H1_norm={h1}, expected ≥ 0.85"


# ── Fortran (non-linguistic, formal language) ────────────────────────


def test_fortran_h1_lower_than_english():
    """Fortran should have lower H1_norm than English.

    Formal languages have more constrained token distributions
    (many repeated keywords). Rao et al. show Fortran entropy
    lower than natural languages.
    """
    eng = compute_block_entropies(load_english(), max_n=2)
    fort = compute_block_entropies(load_fortran(), max_n=2)
    eng_h1 = _get_norm(eng, 1)
    fort_h1 = _get_norm(fort, 1)
    assert fort_h1 < eng_h1, f"Fortran H1_norm={fort_h1} should be < English H1_norm={eng_h1}"


# ── Indus script (target of original study) ────────────────────


def test_indus_in_linguistic_range():
    """Indus script entropy should fall in the linguistic range.

    Rao et al. showed the Indus script's entropy is close to
    natural languages and far from random or rigid sequences.
    """
    result = compute_block_entropies(load_indus(), max_n=3)
    h1 = _get_norm(result, 1)
    # Should be between random (~1.0) and very constrained (~0.5)
    assert 0.60 <= h1 <= 0.95, f"Indus H1_norm={h1}, expected 0.60-0.95"


def test_indus_sublinear_growth():
    """Indus script should show sub-linear entropy growth."""
    result = compute_block_entropies(load_indus(), max_n=3)
    h1 = _get_norm(result, 1)
    h2 = _get_norm(result, 2)
    ratio = h2 / h1
    assert ratio < 1.95, f"Indus H2/H1={ratio:.3f}, expected < 1.95"


# ── Tamil and Sanskrit (additional linguistic systems) ──────────


def test_tamil_linguistic_range():
    """Tamil should fall in the linguistic entropy range."""
    result = compute_block_entropies(load_tamil(), max_n=2)
    h1 = _get_norm(result, 1)
    assert 0.65 <= h1 <= 0.95, f"Tamil H1_norm={h1}, expected 0.65-0.95"


def test_sanskrit_linguistic_range():
    """Sanskrit should fall in the linguistic entropy range."""
    result = compute_block_entropies(load_sanskrit(), max_n=2)
    h1 = _get_norm(result, 1)
    assert 0.65 <= h1 <= 0.95, f"Sanskrit H1_norm={h1}, expected 0.65-0.95"


# ── Sumerian (ancient administrative language) ───────────────────────────


def test_sumerian_linguistic_range():
    """Sumerian transliteration should fall in the linguistic entropy range.

    Sumerian is an agglutinative language with repetitive administrative
    formulae (tablet texts). Character-level H1_norm should be similar to
    other ancient languages (Tamil, Sanskrit) in the 0.65-0.95 range.
    """
    result = compute_block_entropies(load_sumerian(), max_n=2)
    h1 = _get_norm(result, 1)
    assert 0.60 <= h1 <= 0.95, f"Sumerian H1_norm={h1}, expected 0.60-0.95"


def test_sumerian_sublinear_growth():
    """Sumerian should show sub-linear entropy growth (linguistic signature).

    Agglutinative morphology creates strong bigram dependencies
    (common morphemes like -la, -bi, -ka, -ra repeat systematically).
    """
    result = compute_block_entropies(load_sumerian(), max_n=2)
    h1 = _get_norm(result, 1)
    h2 = _get_norm(result, 2)
    ratio = h2 / h1 if h1 > 0 else 2.0
    assert ratio < 1.95, f"Sumerian H2/H1={ratio:.3f}, expected < 1.95"


# ── Ordering: Random > DNA > English > Fortran > Ordered ─────────────────────


def test_entropy_ordering():
    """Key finding from Rao et al.: entropy ordering across system types.

    Random > DNA > English > Fortran (for H1_norm).
    Ordered collapses at H2 (deterministic bigrams).
    """
    random_r = compute_block_entropies(generate_random(), max_n=2)
    dna_r = compute_block_entropies(load_dna(), max_n=2)
    eng_r = compute_block_entropies(load_english(), max_n=2)
    fort_r = compute_block_entropies(load_fortran(), max_n=2)
    ordered_r = compute_block_entropies(generate_ordered(), max_n=2)

    h1_random = _get_norm(random_r, 1)
    h1_dna = _get_norm(dna_r, 1)
    h1_eng = _get_norm(eng_r, 1)
    h1_fort = _get_norm(fort_r, 1)

    h2_ordered = _get_norm(ordered_r, 2)
    h2_random = _get_norm(random_r, 2)

    # H1 ordering
    assert h1_random > h1_dna, f"Random({h1_random}) should > DNA({h1_dna})"
    assert h1_dna > h1_eng, f"DNA({h1_dna}) should > English({h1_eng})"
    assert h1_eng > h1_fort, f"English({h1_eng}) should > Fortran({h1_fort})"

    # Ordered collapses: H2 much less than random
    assert h2_ordered < h2_random * 0.6, (
        f"Ordered H2({h2_ordered}) should be << Random H2({h2_random})"
    )
