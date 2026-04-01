"""Run the hypothesis engine on the synthetic Indus corpus.

Tests proto-Dravidian vs Vedic Sanskrit as competing hypotheses.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tests.corpora.indus_corpus import generate_indus_flat

from glossa_lab.data import dravidian, sanskrit
from glossa_lab.pipelines.decipher import LanguageModel
from glossa_lab.pipelines.hypothesis import (
    Hypothesis,
    HypothesisEngine,
)

# Load Indus corpus
indus_signs = generate_indus_flat(seed=42)
print(f"Indus corpus: {len(indus_signs)} signs, {len(set(indus_signs))} unique")

# Build language models
drav_model = LanguageModel(dravidian.get_corpus_symbols())
skt_model = LanguageModel(sanskrit.get_corpus_symbols())

print(f"Dravidian model: {drav_model.size} symbols, {len(drav_model.symbols)} tokens")
print(f"Sanskrit model: {skt_model.size} symbols, {len(skt_model.symbols)} tokens")

# Create hypotheses
hypotheses = [
    Hypothesis(
        id="h1-dravidian",
        name="Proto-Dravidian",
        target_language="proto-dravidian",
        notes="Parpola (1994): Indus = Dravidian",
    ),
    Hypothesis(
        id="h2-sanskrit",
        name="Vedic Sanskrit",
        target_language="vedic-sanskrit",
        notes="S.R. Rao (1982): Indus = Indo-Aryan",
    ),
]

target_models = {
    "proto-dravidian": drav_model,
    "vedic-sanskrit": skt_model,
}
vocabularies = {
    "proto-dravidian": dravidian.get_vocabulary(),
    "vedic-sanskrit": sanskrit.get_vocabulary(),
}

# Run
engine = HypothesisEngine(indus_signs)
print("\n=== Running hypothesis engine ===\n")
results = engine.run_iteration(
    hypotheses, target_models, vocabularies,
    max_iterations=5000,
)

# Report
print("=== RESULTS (ranked by total score) ===\n")
for r in results:
    print(f"  {r.hypothesis_id}: {r.total_score:.2f}")
    for k, v in r.scores.items():
        print(f"    {k}: {v:.4f}" if isinstance(v, float) else f"    {k}: {v}")
    if r.word_matches:
        print(f"    word matches: {[m['deciphered'] + '=' + m['meaning'][:20] for m in r.word_matches[:5]]}")
    print(f"    suggestions: {r.suggested_next}")
    print()

winner = results[0]
print(f"WINNER: {winner.hypothesis_id} (score: {winner.total_score})")
print(f"Confident mappings: {len(winner.confident_mappings)}")

# Save state
state = engine.get_state()
print(f"\nEngine state: iteration={state['iteration']}, best_score={state['best_score']:.2f}")
