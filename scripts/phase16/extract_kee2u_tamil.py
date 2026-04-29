"""Phase-16 extraction: Kee2u Tamil features.csv + logo_syllabic_tamil_sentences.csv
-> normalized Tamil-as-numeric-ID sequences.

Inputs:
    corpora/downloads/external_repos/Kee2u_Indus_Decipherment/
        Machine_Learning/features.csv  (62,834 morpheme-feature rows)
        Preprocessing/Converted_Tamil/LogoSyllabic/logo_syllabic_tamil_sentences.csv
        Preprocessing/Converted_Tamil/LogoSyllabic/lemmas_labelled.csv

Outputs:
    backend/glossa_lab/data/phase16_corpora/kee2u_tamil_morpheme_seqs.csv
        - id, n_morphemes, morpheme_ids_ws_joined  (per Tamil sentence)
    backend/glossa_lab/data/phase16_corpora/kee2u_tamil_morpheme_features.csv
        - normalized subset of features.csv (relevant columns only)

Run:
    py scripts/phase16/extract_kee2u_tamil.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEE2U = ROOT / "corpora" / "downloads" / "external_repos" / "Kee2u_Indus_Decipherment"
LOGOSYL = KEE2U / "Preprocessing" / "Converted_Tamil" / "LogoSyllabic" / "logo_syllabic_tamil_sentences.csv"
LEMMAS = KEE2U / "Preprocessing" / "Converted_Tamil" / "LogoSyllabic" / "lemmas_labelled.csv"
FEATURES = KEE2U / "Machine_Learning" / "features.csv"
OUTDIR = ROOT / "backend" / "glossa_lab" / "data" / "phase16_corpora"

# Token regex: Kee2u sentences encode each morpheme as 4-digit integer (e.g.
# "2559 2011-5131 , 2625"). Hyphens join inflected/clitic morphemes.
TOKEN_RE = re.compile(r"\d{3,5}(?:-\d{3,5})*")


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    # Sentence-level sequences
    out_seqs = OUTDIR / "kee2u_tamil_morpheme_seqs.csv"
    n_sentences = 0
    n_morphemes_total = 0
    with LOGOSYL.open("r", encoding="utf-8", errors="replace", newline="") as fh, \
         out_seqs.open("w", encoding="utf-8", newline="") as out:
        r = csv.DictReader(fh)
        w = csv.writer(out)
        w.writerow(["id", "n_morphemes", "morpheme_ids_ws_joined"])
        for row in r:
            sid = (row.get("") or row.get("Unnamed: 0") or "").strip()
            sentence = (row.get("Sentence") or "").strip()
            if not sentence:
                continue
            tokens = TOKEN_RE.findall(sentence)
            # Flatten compound tokens (a-b -> a b) so each morpheme becomes a
            # standalone observable. Keep inflected morpheme as compound too if
            # downstream wants composition info; for entropy/Zipf we want flat.
            flat: list[str] = []
            for tok in tokens:
                flat.extend(tok.split("-"))
            if not flat:
                continue
            w.writerow([sid, len(flat), " ".join(flat)])
            n_sentences += 1
            n_morphemes_total += len(flat)
    print(f"Sentence sequences: {n_sentences} sentences, {n_morphemes_total} morphemes -> {out_seqs}", file=sys.stderr)

    # Lemma table (small reference)
    if LEMMAS.exists():
        out_lemmas = OUTDIR / "kee2u_tamil_lemmas.csv"
        n_lemmas = 0
        with LEMMAS.open("r", encoding="utf-8", errors="replace", newline="") as fh, \
             out_lemmas.open("w", encoding="utf-8", newline="") as out:
            r = csv.DictReader(fh)
            w = csv.DictWriter(out, fieldnames=["id", "lemma", "type"])
            w.writeheader()
            for row in r:
                lid = (row.get("id") or "").strip()
                lemma = (row.get("lemma") or "").strip()
                ltype = (row.get("Type") or "").strip()
                if lid and lemma:
                    w.writerow({"id": lid, "lemma": lemma, "type": ltype})
                    n_lemmas += 1
        print(f"Lemma table: {n_lemmas} entries -> {out_lemmas}", file=sys.stderr)

    # Morpheme features (subset of useful columns)
    if FEATURES.exists():
        out_feat = OUTDIR / "kee2u_tamil_morpheme_features.csv"
        keep = ["key", "letters", "form", "upos", "xpos",
                "Counts", "MorphemeSeparated", "prefix", "vowel",
                "morpheme boundary", "noun", "verb"]
        n_feat = 0
        with FEATURES.open("r", encoding="utf-8", errors="replace", newline="") as fh, \
             out_feat.open("w", encoding="utf-8", newline="") as out:
            r = csv.DictReader(fh)
            available = [c for c in keep if c in r.fieldnames]
            w = csv.DictWriter(out, fieldnames=available)
            w.writeheader()
            for row in r:
                w.writerow({c: row.get(c, "") for c in available})
                n_feat += 1
        print(f"Morpheme features: {n_feat} rows -> {out_feat}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
