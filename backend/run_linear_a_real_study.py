"""Run the real Linear A hypothesis study and print results.
Run: shell.cmd python backend/run_linear_a_real_study.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from tests.corpora.linear_a_real_corpus import (
    generate_real_linear_a_sequence,
    translate_sequence_to_phonemes,
    extract_phoneme_only_words,
    KNOWN_LINEAR_A_WORDS,
    GORILA_TO_PHONEME,
    _ALREADY_PHONETIC,
)
from glossa_lab.pipelines.block_entropy import compute_block_entropies
from glossa_lab.pipelines.decipher import LanguageModel
from glossa_lab.pipelines.hypothesis import HypothesisEngine, Hypothesis
from glossa_lab.data.linear_b_language import get_corpus_symbols
from collections import Counter

print("=== REAL LINEAR A STUDY ===\n")

# Load corpus
signs = generate_real_linear_a_sequence(seed=42)
phonemes = translate_sequence_to_phonemes(signs)

print(f"Sign corpus: {len(signs)} tokens")

# Count phonetically decoded
phonetic_count = sum(
    1 for s in signs
    if s in _ALREADY_PHONETIC or (s in GORILA_TO_PHONEME and not GORILA_TO_PHONEME[s].startswith("?"))
)
print(f"Phonetically decoded: {phonetic_count} / {len(signs)} = {phonetic_count/len(signs):.1%}")

# Block entropy on signs
res = compute_block_entropies(signs, max_n=3)
print(f"Sign-level H1_norm = {res['block_entropies'][0]['normalized']:.4f}")
print(f"Sign-level H2/H1   = {res['block_entropies'][1]['normalized']/res['block_entropies'][0]['normalized']:.4f}")

# Block entropy on phonemes
res_ph = compute_block_entropies(phonemes, max_n=3)
print(f"Phoneme H1_norm    = {res_ph['block_entropies'][0]['normalized']:.4f}")
print(f"Phoneme H2/H1      = {res_ph['block_entropies'][1]['normalized']/res_ph['block_entropies'][0]['normalized']:.4f}")

# Extract phoneme words and check known vocab
words = extract_phoneme_only_words(signs, min_word_len=2, max_word_len=8)
word_counts = Counter(words)
print(f"\nDecoded word-groups: {len(words)} total, {len(word_counts)} unique")

known_matches = [(w, c, KNOWN_LINEAR_A_WORDS[w]) for w, c in word_counts.most_common() if w in KNOWN_LINEAR_A_WORDS]
print(f"\nKnown word matches ({len(known_matches)}):")
for w, c, meaning in known_matches[:15]:
    print(f"  {w:15} x{c:3}  {meaning[:60]}")

print(f"\nMost frequent decoded words:")
for w, c in word_counts.most_common(20):
    known = "*" if w in KNOWN_LINEAR_A_WORDS else ""
    print(f"  {w:15} x{c:3} {known}")

# Hypothesis engine
print("\n=== HYPOTHESIS ENGINE ===")

# Language models
lb_model    = LanguageModel(get_corpus_symbols())
LUWIAN_CORP = list("atimimitatiwawatarruszidandaparananturapiariwalaasiisaparamanani" * 30)
SEMITIC_CORP= list("abuummuahubanukalbu" * 30)
# Hurrian (van Soesbergen 2022 proposal): use common Hurrian morphemes
HURRIAN_CORP= list("eniattianevretiurihifattimannikketmennakiagallammewuriurihewuri" * 30)

luwian_model  = LanguageModel(LUWIAN_CORP)
semitic_model = LanguageModel(SEMITIC_CORP)
hurrian_model = LanguageModel(HURRIAN_CORP)

# Use phonemically decoded segments for hypothesis testing
phoneme_segs = [p for p in phonemes if not p.startswith("?") and not p.startswith("AB")]

hyps = [
    Hypothesis(id="greek",   name="Mycenaean Greek", target_language="greek"),
    Hypothesis(id="luwian",  name="Luwian/Anatolian",target_language="luwian"),
    Hypothesis(id="semitic", name="Proto-Semitic",   target_language="semitic"),
    Hypothesis(id="hurrian", name="Hurrian",         target_language="hurrian"),
]

# Known Linear A vocabulary for matching
known_vocab = {w: m for w, m in KNOWN_LINEAR_A_WORDS.items()}

engine = HypothesisEngine(cipher_signs=phoneme_segs)
results = engine.run_iteration(
    hyps,
    {"greek": lb_model, "luwian": luwian_model, "semitic": semitic_model, "hurrian": hurrian_model},
    {"greek": known_vocab, "luwian": {}, "semitic": {}, "hurrian": {}},
    max_iterations=3000,
)

print("\nHypothesis rankings (real phoneme-level analysis):")
for r in results:
    matches = r.scores.get("word_matches", 0)
    kandles = r.scores.get("kandles", 0)
    print(f"  {r.hypothesis_id:10} score={r.total_score:7.2f}  kandles={kandles:.4f}  word_matches={matches:.0f}")

if results:
    winner = results[0]
    print(f"\nBest fit: {winner.hypothesis_id} (score={winner.total_score:.2f})")
    print(f"Word matches: {winner.word_matches[:5]}")
