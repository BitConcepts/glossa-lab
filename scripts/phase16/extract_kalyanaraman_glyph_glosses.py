"""Phase-16 extraction: Kalyanaraman index files (zanodor) -> Devanagari vocabulary.

Realistic scope note
--------------------
Kalyanaraman's "Epigraphia Indus Script -- Hypertexts & Meanings" volumes and
related papers (in zanodor/CORPUS_INDEX) are dense expository prose with
sign-to-Sanskrit rebus claims woven through long paragraphs. Extracting clean
'sign -> gloss' pairs at scale would require manual annotation per claim and is
out of scope for an automated pass.

What we extract instead is a *vocabulary corpus*: every Devanagari (Sanskrit)
word + every ASCII transliterated Sanskrit token. This gives Phase-16:
    (a) a Vedic/Sanskrit-style positive-control corpus of token sequences
        we can compute language-signature DoFs on (Zipf, MI decay, etc.), so
        the `vedic_kalyanaraman_morphology.yaml` constraint ranges have an
        empirical basis; and
    (b) a signal of which Sanskrit words Kalyanaraman associates with the Indus
        material -- useful as a vocabulary candidate set for any future
        Indus -> Sanskrit projection node.

It is *not* a vetted sign-decipherment table. Kalyanaraman's interpretation is
contested even within the Indo-Aryan-hypothesis camp.

Inputs:
    corpora/downloads/external_repos/zanodor_CORPUS_INDEX/*.md
        Filtered to filenames matching Kalyanaraman / Indus / Meluhha.

Outputs:
    backend/glossa_lab/data/phase16_corpora/kalyanaraman_devanagari_corpus.txt
        Whitespace-tokenized concatenation of all extracted Devanagari words
        across the matched files.
    backend/glossa_lab/data/phase16_corpora/kalyanaraman_devanagari_vocab.csv
        word, count, source_file_count

Run:
    py scripts/phase16/extract_kalyanaraman_glyph_glosses.py
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ZAN = ROOT / "corpora" / "downloads" / "external_repos" / "zanodor_CORPUS_INDEX"
OUTDIR = ROOT / "backend" / "glossa_lab" / "data" / "phase16_corpora"

# Devanagari unicode range U+0900..U+097F. We define a "word" as a maximal run
# of Devanagari letters / virama / vowel signs (with internal joiners), but we
# strip out the danda/double-danda punctuation and digit characters before
# counting, because they are word *separators* not word content.
# U+0964 = DEVANAGARI DANDA, U+0965 = DOUBLE DANDA,
# U+0966..U+096F = DEVANAGARI DIGITS
DEVA_RUN = re.compile(r"[\u0900-\u0963\u0970-\u097F]+")
DEVA_LETTER = re.compile(r"[\u0904-\u0939\u0958-\u095F\u0972-\u097F]")

# Source file filter
NAME_FILTER = re.compile(
    r"(?i)(indus|kalyana|meluhha|epigraphia|hypertext|harapp|sarasvati)"
)


def main() -> int:
    if not ZAN.exists():
        print(f"ERROR: zanodor CORPUS_INDEX not at {ZAN}", file=sys.stderr)
        return 1
    OUTDIR.mkdir(parents=True, exist_ok=True)

    files = [p for p in ZAN.iterdir() if p.is_file() and p.suffix.lower() == ".md"
             and NAME_FILTER.search(p.name)]
    print(f"Matching files: {len(files)}", file=sys.stderr)
    if not files:
        return 0

    word_counts: Counter = Counter()
    word_files: dict[str, set[str]] = defaultdict(set)
    out_corpus = OUTDIR / "kalyanaraman_devanagari_corpus.txt"

    total_tokens = 0
    n_files_with_deva = 0
    with out_corpus.open("w", encoding="utf-8") as cfh:
        for f in files:
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"  skip {f.name}: {e}", file=sys.stderr)
                continue
            raw_words = DEVA_RUN.findall(text)
            # Keep only runs that contain >= 2 Devanagari letters (not just
            # vowel-signs/virama). This drops single-letter junk and isolated
            # diacritics/joiners that the OCR fragmented.
            words = [w for w in raw_words if len(DEVA_LETTER.findall(w)) >= 2]
            if not words:
                continue
            n_files_with_deva += 1
            cfh.write(" ".join(words))
            cfh.write("\n")
            total_tokens += len(words)
            for w in words:
                word_counts[w] += 1
                word_files[w].add(f.name)

    print(f"Files containing Devanagari: {n_files_with_deva}", file=sys.stderr)
    print(f"Total Devanagari tokens written: {total_tokens}", file=sys.stderr)
    print(f"Distinct Devanagari words: {len(word_counts)}", file=sys.stderr)

    out_vocab = OUTDIR / "kalyanaraman_devanagari_vocab.csv"
    with out_vocab.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["word", "count", "n_source_files"])
        for word, n in word_counts.most_common():
            w.writerow([word, n, len(word_files[word])])

    if word_counts:
        print("Top 15 Devanagari words:", file=sys.stderr)
        for word, n in word_counts.most_common(15):
            print(f"  {n:>6}  {word}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
