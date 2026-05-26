"""Compute Sproat's r/R repetition rate for the IVS corpus.

r = number of symbols that repeat AND are adjacent to the symbol they repeat
R = total number of repeated symbols in the text
r/R close to 1.0 → non-linguistic; close to 0.0 → linguistic.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]


def load_ivs_sequences() -> list[list[str]]:
    """Load sign sequences from the translation corpus."""
    corpus_path = ROOT / "outputs" / "seal_translations.json"
    data = json.loads(corpus_path.read_text(encoding="utf-8"))
    return [t["signs"] for t in data["translations"] if t["signs"]]


def repetition_rate(sequences: list[list[str]]) -> dict:
    """Compute r/R repetition rate across all sequences.

    r = count of tokens that are identical to an adjacent token
    R = count of tokens that appear more than once in the same text
    """
    total_r = 0  # adjacent-repeat tokens
    total_R = 0  # any-repeat tokens

    for seq in sequences:
        if len(seq) < 2:
            continue
        from collections import Counter

        counts = Counter(seq)
        # R: tokens that repeat (appear >1 time in this text)
        for i, sign in enumerate(seq):
            if counts[sign] > 1:
                total_R += 1
            # r: this token is adjacent to an identical token
            if i > 0 and seq[i] == seq[i - 1]:
                total_r += 1
            elif i < len(seq) - 1 and seq[i] == seq[i + 1]:
                total_r += 1

    r_over_R = total_r / total_R if total_R > 0 else 0.0
    return {
        "r_adjacent_repeats": total_r,
        "R_total_repeats": total_R,
        "r_over_R": round(r_over_R, 4),
    }


if __name__ == "__main__":
    seqs = load_ivs_sequences()
    result = repetition_rate(seqs)
    result["system"] = "Indus Valley Script (IVS)"
    result["n_texts"] = len(seqs)
    print(json.dumps(result, indent=2))

    out = ROOT / "outputs" / "benchmarks"
    out.mkdir(parents=True, exist_ok=True)
    (out / "ivs_repetition_metrics.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(f"\nSaved to {out / 'ivs_repetition_metrics.json'}")
