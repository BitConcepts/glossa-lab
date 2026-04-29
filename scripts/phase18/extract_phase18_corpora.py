"""Phase-18 extraction: build RV padapatha sequences + mayig CISI sign sequences.

Inputs:
    corpora/downloads/external_repos/sanskrit_texts_rigveda/morpho-lexical/rigveda.csv
        Hellwig 2018 morpho-lexical annotation (27 MB, # separator).
    corpora/downloads/external_repos/mayig_cisi_json/corpus/{m001_m099,m100_m199}/
        mcskware's JSON digitization of CISI (179 inscriptions covered).

Outputs:
    backend/glossa_lab/data/phase18_corpora/rv_padapatha_seqs.csv
        One verse per row: book, chapter, strophe, n_words, padapatha_words_ws_joined.
    backend/glossa_lab/data/phase18_corpora/rv_padapatha_stream.txt
        One verse per line, padapatha words whitespace-joined (drop-in for
        measure_signature_dofs.py).
    backend/glossa_lab/data/phase18_corpora/cisi_mayig_inscriptions.csv
        One inscription per row: id, description, n_signs, signs_ws_joined.
    backend/glossa_lab/data/phase18_corpora/cisi_mayig_signs.txt
        One inscription per line, Parpola sign IDs (e.g. P121 P202 P385) ws-joined.
"""
from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HELLWIG_RV = ROOT / "corpora" / "downloads" / "external_repos" / "sanskrit_texts_rigveda" / "morpho-lexical" / "rigveda.csv"
MAYIG_DIR = ROOT / "corpora" / "downloads" / "external_repos" / "mayig_cisi_json" / "corpus"
OUT_DIR = ROOT / "backend" / "glossa_lab" / "data" / "phase18_corpora"


def extract_rv_padapatha() -> tuple[int, int]:
    """Extract padapatha (surface_form) words from Hellwig morpho-lexical CSV."""
    if not HELLWIG_RV.exists():
        print(f"  SKIP: {HELLWIG_RV} not found", file=sys.stderr)
        return 0, 0
    out_csv = OUT_DIR / "rv_padapatha_seqs.csv"
    out_stream = OUT_DIR / "rv_padapatha_stream.txt"

    # Group by (book, chapter, strophe, verse)
    cur_key = None
    cur_words: list[str] = []
    n_verses, n_words = 0, 0
    rows: list[dict] = []

    with HELLWIG_RV.open("r", encoding="utf-8", errors="replace") as fh, \
         out_stream.open("w", encoding="utf-8") as stream_fh:
        # The file uses '#' as field separator
        reader = csv.DictReader(fh, delimiter="#")
        for row in reader:
            try:
                book = int(row.get("book", "") or 0)
                chapter = int(row.get("chapter", "") or 0)
                strophe = int(row.get("strophe", "") or 0)
                verse = int(row.get("verse", "") or 0)
            except (ValueError, TypeError):
                continue
            key = (book, chapter, strophe, verse)
            sf = (row.get("surface_form") or "").strip()
            if not sf:
                continue
            if key != cur_key:
                if cur_key is not None and cur_words:
                    rows.append({"book": cur_key[0], "chapter": cur_key[1],
                                 "strophe": cur_key[2], "verse": cur_key[3],
                                 "n_words": len(cur_words),
                                 "padapatha_words_ws_joined": " ".join(cur_words)})
                    stream_fh.write(" ".join(cur_words) + "\n")
                    n_verses += 1
                    n_words += len(cur_words)
                cur_key = key
                cur_words = []
            cur_words.append(sf)
        # Flush final
        if cur_key is not None and cur_words:
            rows.append({"book": cur_key[0], "chapter": cur_key[1],
                         "strophe": cur_key[2], "verse": cur_key[3],
                         "n_words": len(cur_words),
                         "padapatha_words_ws_joined": " ".join(cur_words)})
            stream_fh.write(" ".join(cur_words) + "\n")
            n_verses += 1
            n_words += len(cur_words)

    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["book", "chapter", "strophe", "verse",
                                           "n_words", "padapatha_words_ws_joined"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return n_verses, n_words


def extract_mayig_cisi() -> tuple[int, int]:
    """Extract Parpola-sign sequences from mayig JSON corpus."""
    if not MAYIG_DIR.exists():
        print(f"  SKIP: {MAYIG_DIR} not found", file=sys.stderr)
        return 0, 0
    out_csv = OUT_DIR / "cisi_mayig_inscriptions.csv"
    out_stream = OUT_DIR / "cisi_mayig_signs.txt"

    rows: list[dict] = []
    with out_stream.open("w", encoding="utf-8") as sfh:
        for jpath in sorted(MAYIG_DIR.rglob("*.json")):
            try:
                data = json.loads(jpath.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  WARN: {jpath.name}: {e}", file=sys.stderr)
                continue
            if not isinstance(data, list):
                data = [data]
            for entry in data:
                if not isinstance(entry, dict):
                    continue
                ide = entry.get("id", "")
                desc = entry.get("description", "")
                graphemes = entry.get("graphemes", [])
                signs = []
                for g in graphemes:
                    if isinstance(g, dict) and g.get("id"):
                        signs.append(str(g["id"]))
                if not signs:
                    continue
                rows.append({"id": ide, "description": desc, "n_signs": len(signs),
                             "signs_ws_joined": " ".join(signs)})
                sfh.write(" ".join(signs) + "\n")

    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "description", "n_signs", "signs_ws_joined"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    n_signs = sum(r["n_signs"] for r in rows)
    return len(rows), n_signs


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Phase-18 corpus extraction starting", file=sys.stderr)

    print("\n[1/2] Hellwig morpho-lexical RV -> padapatha sequences", file=sys.stderr)
    n_v, n_w = extract_rv_padapatha()
    print(f"  Verses: {n_v}  Words: {n_w}", file=sys.stderr)

    print("\n[2/2] mayig_cisi_json -> Parpola sign sequences", file=sys.stderr)
    n_i, n_s = extract_mayig_cisi()
    print(f"  Inscriptions: {n_i}  Signs: {n_s}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
