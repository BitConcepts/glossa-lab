"""Generate the block entropy analysis PDF report.

Usage: shell.cmd python backend/generate_report.py
"""

import sys
from pathlib import Path

# Add backend to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

from glossa_lab.pipelines.report import generate_report
from tests.corpora.real import (
    load_dna,
    load_english,
    load_fortran,
    load_indus,
    load_sanskrit,
    load_tamil,
)
from tests.corpora.synthetic import generate_markov, generate_ordered, generate_random

# Define all corpora
corpora = {
    "English": {
        "symbols": load_english(),
        "corpus_type": "linguistic",
        "description": "Opening of Moby Dick (Melville), character-level, lowercase",
    },
    "Tamil": {
        "symbols": load_tamil(),
        "corpus_type": "linguistic",
        "description": "Thirukkural (Thiruvalluvar, ~2nd c. BCE), transliterated",
    },
    "Sanskrit": {
        "symbols": load_sanskrit(),
        "corpus_type": "linguistic",
        "description": "Rigveda opening hymns (Mandala 1), transliterated",
    },
    "Indus Script": {
        "symbols": load_indus(),
        "corpus_type": "target",
        "description": "Synthetic corpus matching published statistics (Yadav et al. 2010)",
    },
    "DNA": {
        "symbols": load_dna(),
        "corpus_type": "non-linguistic",
        "description": "Human beta-globin gene segment, 4-base alphabet",
    },
    "Fortran": {
        "symbols": load_fortran(),
        "corpus_type": "non-linguistic",
        "description": "Numerical computing code, keyword-normalised tokens",
    },
    "Random": {
        "symbols": generate_random(),
        "corpus_type": "synthetic",
        "description": "Uniform random over 26-char alphabet (seed=42, max entropy)",
    },
    "Ordered": {
        "symbols": generate_ordered(),
        "corpus_type": "synthetic",
        "description": "Repeating cycle A→Z (min entropy for N≥2)",
    },
    "Markov": {
        "symbols": generate_markov(),
        "corpus_type": "synthetic",
        "description": "English-like Markov chain (seed=42, linguistic baseline)",
    },
}

output_path = Path(__file__).parent.parent / "reports" / "block_entropy_analysis.pdf"
result = generate_report(corpora, output_path, max_n=6)
print(f"Report generated: {result}")
