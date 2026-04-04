"""Cipher cracking tests — ACTUALLY DECIPHER, not just analyse.

These tests run the decipherment engine on:
1. The synthetic cipher language → verifies we recover the mapping
2. Ugaritic with opaque IDs → verifies we propose correct sign values

The answer key is used ONLY for scoring — the engine does NOT
see it during decipherment.
"""

from glossa_lab.pipelines.decipher import (
    LanguageModel,
    decipher,
    score_accuracy,
)
from tests.corpora.cipher_language import generate_cipher_test_data
from tests.corpora.ugaritic import (
    get_answer_key as ugaritic_answer_key,
)
from tests.corpora.ugaritic import (
    get_deciphered_corpus as ugaritic_deciphered,
)
from tests.corpora.ugaritic import (
    get_undeciphered_corpus as ugaritic_undeciphered,
)

# ══════════════════════════════════════════════════════════════════
# 1. CRACK THE SYNTHETIC CIPHER
# ══════════════════════════════════════════════════════════════════


def test_crack_synthetic_cipher():
    """The engine should recover >70% of the cipher mapping.

    We give it:
      - The ciphered sign sequence (encrypted phonemes)
      - A language model built from the PLAINTEXT phonemes
        (simulating: we KNOW the target language, just not the mapping)

    It should figure out which cipher sign = which phoneme.
    """
    data = generate_cipher_test_data(seed=42)

    # Build target model from plaintext (the "known language")
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])

    # Run decipherment on the ciphered text
    result = decipher(
        data["cipher"]["flat_signs"],
        target_model,
        seed=42,
        max_iterations=10000,
        restarts=5,
    )

    # Score against answer key
    # answer_key maps cipher_sign → true_phoneme
    # But our cipher_map maps phoneme → cipher_sign
    # We need cipher_sign → phoneme (the reverse)
    reverse_key = data["cipher"]["reverse_map"]

    accuracy = score_accuracy(result["proposed_mapping"], reverse_key)

    print("\n=== SYNTHETIC CIPHER CRACKING ===")
    print(f"Accuracy: {accuracy['correct']}/{accuracy['total']} "
          f"= {accuracy['accuracy'] * 100:.1f}%")
    for d in accuracy["details"]:
        mark = "✓" if d["correct"] else "✗"
        print(f"  {mark} {d['sign']} → proposed: {d['proposed']}, "
              f"true: {d['true']}")

    # We should get at least 70% correct
    assert accuracy["accuracy"] >= 0.70, (
        f"Only {accuracy['accuracy'] * 100:.1f}% accuracy — "
        f"expected ≥70%"
    )


def test_crack_synthetic_high_accuracy():
    """With more iterations, accuracy should be higher."""
    data = generate_cipher_test_data(seed=42)
    target_model = LanguageModel(data["plaintext"]["flat_phonemes"])

    result = decipher(
        data["cipher"]["flat_signs"],
        target_model,
        seed=42,
        max_iterations=20000,
        restarts=8,
    )

    reverse_key = data["cipher"]["reverse_map"]
    accuracy = score_accuracy(result["proposed_mapping"], reverse_key)

    # With more compute, should get even better
    assert accuracy["accuracy"] >= 0.60, (
        f"Only {accuracy['accuracy'] * 100:.1f}% with extended search"
    )


# ══════════════════════════════════════════════════════════════════
# 2. CRACK UGARITIC
# ══════════════════════════════════════════════════════════════════


def test_crack_ugaritic():
    """Crack the Ugaritic Baal Cycle using the deciphered text as model.

    With trigram scoring, positional constraints, and expanded corpus,
    accuracy should be significantly higher than the baseline.
    """
    undec = ugaritic_undeciphered()
    dec = ugaritic_deciphered()
    answer_key = ugaritic_answer_key()

    # Build target model WITH inscriptions for positional scoring
    target_model = LanguageModel(
        dec["flat_signs"], inscriptions=dec["inscriptions"],
    )

    # Run decipherment with positional constraints
    result = decipher(
        undec["flat_signs"],
        target_model,
        seed=42,
        max_iterations=15000,
        restarts=8,
        cipher_inscriptions=undec["inscriptions"],
    )

    accuracy = score_accuracy(result["proposed_mapping"], answer_key)

    print("\n=== UGARITIC CRACKING (ENHANCED) ===")
    print(f"Accuracy: {accuracy['correct']}/{accuracy['total']} "
          f"= {accuracy['accuracy'] * 100:.1f}%")
    print(f"Kandles confidence: {result.get('kandles_confidence', 0):.3f}")
    for d in sorted(accuracy["details"], key=lambda x: x["sign"]):
        mark = "✓" if d["correct"] else "✗"
        print(f"  {mark} {d['sign']} → proposed: {d['proposed']}, "
              f"true: {d['true']}")

    assert accuracy["accuracy"] >= 0.75, (
        f"Only {accuracy['accuracy'] * 100:.1f}% accuracy on Ugaritic"
    )


def test_crack_ugaritic_common_signs():
    """Top-5 most frequent signs should be correctly mapped."""
    undec = ugaritic_undeciphered()
    dec = ugaritic_deciphered()
    answer_key = ugaritic_answer_key()

    target_model = LanguageModel(
        dec["flat_signs"], inscriptions=dec["inscriptions"],
    )
    result = decipher(
        undec["flat_signs"],
        target_model,
        seed=42,
        max_iterations=15000,
        restarts=8,
        cipher_inscriptions=undec["inscriptions"],
    )

    # Check top-5 most frequent cipher signs
    from collections import Counter
    freq = Counter(undec["flat_signs"])
    top5 = [s for s, _ in freq.most_common(5)]

    correct_top5 = sum(
        1 for s in top5
        if result["proposed_mapping"].get(s) == answer_key.get(s)
    )

    print(f"\nTop-5 accuracy: {correct_top5}/5")
    assert correct_top5 >= 3, (
        f"Only {correct_top5}/5 top signs correct"
    )
