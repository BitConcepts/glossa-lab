"""Deterministic synthetic corpora for regression testing.

All generators use seed=42 for reproducibility.
"""

from __future__ import annotations

import random
import string

ALPHABET = list(string.ascii_uppercase)  # A-Z, 26 symbols
SIZE = 10_000


def generate_random(seed: int = 42, size: int = SIZE) -> list[str]:
    """Uniform random from 26-char alphabet. Max entropy baseline."""
    rng = random.Random(seed)
    return [rng.choice(ALPHABET) for _ in range(size)]


def generate_ordered(size: int = SIZE) -> list[str]:
    """Repeating cycle A→B→C→...→Z→A. Min entropy baseline."""
    return [ALPHABET[i % 26] for i in range(size)]


def generate_markov(seed: int = 42, size: int = SIZE) -> list[str]:
    """First-order Markov chain with English-like bigram structure.

    Transition matrix gives higher probability to common English
    bigrams (e.g. T→H, S→T, E→R) and low probability to rare ones.
    This produces a sequence with sub-linear entropy growth — the
    signature of linguistic systems in Rao et al.'s analysis.
    """
    rng = random.Random(seed)

    # Build a simple transition matrix favouring common bigrams
    # Start with uniform small probability, boost common pairs
    n = 26
    matrix: list[list[float]] = [[1.0] * n for _ in range(n)]

    # Common English bigram pairs (source → target index)
    common_bigrams = [
        ("T", "H"), ("H", "E"), ("E", "R"), ("R", "E"), ("I", "N"),
        ("A", "N"), ("N", "D"), ("E", "D"), ("S", "T"), ("T", "O"),
        ("O", "F"), ("O", "N"), ("A", "T"), ("I", "S"), ("E", "S"),
        ("N", "G"), ("A", "L"), ("I", "T"), ("T", "I"), ("E", "N"),
    ]

    for src, tgt in common_bigrams:
        si = ord(src) - ord("A")
        ti = ord(tgt) - ord("A")
        matrix[si][ti] += 15.0  # strong bias

    # Normalize rows
    for row in matrix:
        total = sum(row)
        for j in range(n):
            row[j] /= total

    # Generate sequence
    symbols = []
    current = rng.randint(0, n - 1)
    for _ in range(size):
        symbols.append(ALPHABET[current])
        r = rng.random()
        cumulative = 0.0
        for j in range(n):
            cumulative += matrix[current][j]
            if r <= cumulative:
                current = j
                break

    return symbols
