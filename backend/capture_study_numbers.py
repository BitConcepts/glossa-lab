"""Capture study numbers for Linear B and Linear A reports."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from tests.corpora.real import load_linear_b_signs, load_linear_a_signs
from glossa_lab.pipelines.block_entropy import compute_block_entropies
from glossa_lab.data.linear_b_language import get_corpus_symbols, encode_corpus
from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy
from glossa_lab.pipelines.hypothesis import HypothesisEngine, Hypothesis
from collections import Counter

print("=== LINEAR B ===")
lb = load_linear_b_signs()
res = compute_block_entropies(lb, max_n=4)
print(f"Corpus size: {len(lb)}")
print(f"Alphabet size: {res['alphabet_size']}")
for e in res['block_entropies']:
    print(f"H{e['n']}_norm={e['normalized']:.4f}  raw={e['raw_nats']:.4f}")

syms = get_corpus_symbols()
opaque, answer_key = encode_corpus(syms)
model = LanguageModel(syms)
result = decipher(opaque, model, seed=42, max_iterations=8000, restarts=5)
acc = score_accuracy(result['proposed_mapping'], answer_key)
print(f"Decipherment: {acc['correct']}/{acc['total']} = {acc['accuracy']:.3f}")
print(f"Kandles: {result['kandles_confidence']:.4f}")
top5_opaque = [s for s, _ in Counter(opaque).most_common(5)]
top5_c = sum(1 for s in top5_opaque if result['proposed_mapping'].get(s) == answer_key.get(s))
print(f"Top-5 correct: {top5_c}/5")

# Show full mapping
print("\nProposed mapping (opaque → proposed | true | correct):")
for opq, true_val in sorted(answer_key.items()):
    proposed = result['proposed_mapping'].get(opq, '?')
    ok = '✓' if proposed == true_val else '✗'
    print(f"  {opq:6} → {proposed:8} | {true_val:8} {ok}")

print("\n=== LINEAR A ===")
la = load_linear_a_signs()
res_la = compute_block_entropies(la, max_n=4)
print(f"Corpus size: {len(la)}")
print(f"Alphabet size: {res_la['alphabet_size']}")
for e in res_la['block_entropies']:
    print(f"H{e['n']}_norm={e['normalized']:.4f}  raw={e['raw_nats']:.4f}")
ab_frac = sum(1 for s in la if s.startswith('AB')) / len(la)
print(f"AB-sign fraction: {ab_frac:.3f}")
freq_la = Counter(la)
print("Top-10 signs:", freq_la.most_common(10))

# Hypothesis engine
LUWIAN_CORPUS = list("atimimitatiwawatarruszidandaparananturapiariwalaasiisaparamanani" * 30)
SEMITIC_CORPUS = list("abuummuahubanukalbu" * 30)

lb_model = LanguageModel(syms)
luwian_model = LanguageModel(LUWIAN_CORPUS)
semitic_model = LanguageModel(SEMITIC_CORPUS)

target_models = {
    "mycenaean-greek": lb_model,
    "luwian-anatolian": luwian_model,
    "proto-semitic": semitic_model,
}

hyps = [
    Hypothesis(id="h-greek", name="Mycenaean Greek", target_language="mycenaean-greek"),
    Hypothesis(id="h-luwian", name="Luwian/Anatolian", target_language="luwian-anatolian"),
    Hypothesis(id="h-semitic", name="Proto-Semitic", target_language="proto-semitic"),
]

engine = HypothesisEngine(cipher_signs=la)
results = engine.run_iteration(hyps, target_models, {}, max_iterations=3000)

print("\nHypothesis scores:")
for r in results:
    print(f"  {r.hypothesis_id:15} score={r.total_score:.2f}  word_matches={r.scores.get('word_matches',0):.0f}  kandles={r.scores.get('kandles',0):.4f}")
