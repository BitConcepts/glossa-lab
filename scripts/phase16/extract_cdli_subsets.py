"""Phase-16 extraction: CDLI catalog + ATF -> per-(period, language) sign sequences.

Inputs:
    corpora/downloads/external_repos/cdli_gh_data/cdli_cat.csv     (148 MB, 353k rows)
    corpora/downloads/external_repos/cdli_gh_data/cdliatf_unblocked.atf (83 MB)

Outputs (one pair per bucket):
    backend/glossa_lab/data/phase16_corpora/cdli_<bucket>.atf      (raw ATF subset)
    backend/glossa_lab/data/phase16_corpora/cdli_<bucket>_seqs.csv (one row per text:
                                                                   id_text, n_signs,
                                                                   signs_ws_joined)

Buckets (period x language):
    sumerian_ur3        Sumerian + Ur III
    sumerian_ob_lit     Sumerian + Old Babylonian
    akkadian_ob         Akkadian + Old Babylonian
    akkadian_na         Akkadian + Neo-Assyrian

Sign extraction rules (per ATF line):
    * Skip lines starting with '&', '#', '$', '@', '>>', '?'
    * Strip leading line number like "1'." / "12." / "[3'.]"
    * Tokenize remaining whitespace-separated tokens
    * Drop punctuation-only tokens ("," ";" ":" "...")
    * Drop bracket-only tokens ("[" "]" "[..." "...]")
    * Strip trailing markers '#' (uncertain) and '?'
    * Strip surrounding brackets but keep the sign string
    * Drop empty results

We keep variant markers like '~a' as part of the sign because they encode
distinct cuneiform glyphs in CDLI's transliteration (e.g., GAL~a is a different
sign from GAL).

Run:
    py scripts/phase16/extract_cdli_subsets.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAT = ROOT / "corpora" / "downloads" / "external_repos" / "cdli_gh_data" / "cdli_cat.csv"
ATF = ROOT / "corpora" / "downloads" / "external_repos" / "cdli_gh_data" / "cdliatf_unblocked.atf"
OUTDIR = ROOT / "backend" / "glossa_lab" / "data" / "phase16_corpora"

# Bucket definitions: (name, language_match, period_match)
# Use 'startswith' on the catalog string after .strip().lower().
BUCKETS = [
    ("sumerian_ur3",     "sumerian", "ur iii"),
    ("sumerian_ob_lit",  "sumerian", "old babylonian"),
    ("akkadian_ob",      "akkadian", "old babylonian"),
    ("akkadian_na",      "akkadian", "neo-assyrian"),
]

# Patterns to clean ATF lines
LINENO_RE = re.compile(r"^\s*\[?\d+'?\.\]?\s*")
PUNCT_ONLY_RE = re.compile(r"^[\.,;:\-\[\]\(\)\?<>!]+$")
EMPTY_TOKEN_PUNCT = set([",", ";", ":", ".", "...", "?", "!", "<", ">", "(", ")"])


def load_catalog_buckets(cat_path: Path) -> tuple[dict[int, str], dict[str, int]]:
    """Map id_text (as int) -> bucket name. CDLI catalog stores id_text as a
    bare integer; the ATF dump uses zero-padded 'P000001' style. We canonicalize
    on the int so matching is symmetric."""
    text_to_bucket: dict[int, str] = {}
    bucket_counts = {b[0]: 0 for b in BUCKETS}
    with cat_path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        r = csv.DictReader(fh)
        for row in r:
            id_raw = (row.get("id_text") or "").strip()
            if not id_raw or not id_raw.isdigit():
                continue
            id_int = int(id_raw)
            language = (row.get("language") or "").strip().lower()
            period = (row.get("period") or "").strip().lower()
            for name, lang_substr, period_substr in BUCKETS:
                if lang_substr in language and period_substr in period:
                    if id_int not in text_to_bucket:  # first match wins
                        text_to_bucket[id_int] = name
                        bucket_counts[name] += 1
                    break
    return text_to_bucket, bucket_counts


def clean_token(tok: str) -> str | None:
    """Apply token-level cleanup. Return None to drop."""
    t = tok.strip()
    if not t or t in EMPTY_TOKEN_PUNCT:
        return None
    if PUNCT_ONLY_RE.match(t):
        return None
    # Strip enclosing brackets
    while t and t[0] in "[<":
        t = t[1:]
    while t and t[-1] in "]>":
        t = t[:-1]
    # Strip trailing uncertainty markers (kept for sign-shape distinction
    # is overkill at the corpus-statistics level)
    t = t.rstrip("#?!")
    if not t:
        return None
    if PUNCT_ONLY_RE.match(t):
        return None
    return t


def extract_signs(line: str) -> list[str]:
    """Extract sign tokens from one ATF text line."""
    line = LINENO_RE.sub("", line)
    raw = line.split()
    out = []
    for tok in raw:
        c = clean_token(tok)
        if c:
            out.append(c)
    return out


def stream_atf(atf_path: Path, text_to_bucket: dict[int, str]):
    """Yield (id_text_p, bucket, [list of (atf_line, signs)]) tuples for each
    text whose id is in `text_to_bucket`. id_text_p is the canonical 'P000001'
    string; we look up by int."""
    cur_id_p: str | None = None
    cur_bucket = None
    cur_lines: list[tuple[str, list[str]]] = []

    with atf_path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("&"):
                # New text header
                if cur_id_p is not None and cur_bucket is not None:
                    yield cur_id_p, cur_bucket, cur_lines
                cur_lines = []
                # parse "&P000001 = ..."
                m = re.match(r"^&P0*(\d+)", line)
                if m:
                    cur_id_p = f"P{int(m.group(1)):06d}"
                    cur_bucket = text_to_bucket.get(int(m.group(1)))
                else:
                    cur_id_p = None
                    cur_bucket = None
                continue
            if cur_id_p is None or cur_bucket is None:
                continue
            # Skip non-content lines
            if not line.strip():
                continue
            if line.startswith(("#", "$", "@", ">>", "?")):
                # Keep them in the raw ATF subset (caller wants ATF subset too)
                cur_lines.append((line, []))
                continue
            signs = extract_signs(line)
            cur_lines.append((line, signs))
        if cur_id_p is not None and cur_bucket is not None:
            yield cur_id_p, cur_bucket, cur_lines


def main() -> int:
    if not CAT.exists():
        print(f"ERROR: catalog not found: {CAT}", file=sys.stderr)
        return 1
    if not ATF.exists():
        print(f"ERROR: ATF not found: {ATF}", file=sys.stderr)
        return 1
    OUTDIR.mkdir(parents=True, exist_ok=True)

    print("Indexing catalog buckets ...", file=sys.stderr)
    text_to_bucket, bucket_counts = load_catalog_buckets(CAT)
    for name, n in bucket_counts.items():
        print(f"  {name:20s}  {n} texts in catalog", file=sys.stderr)

    # Open writers per bucket
    atf_files = {}
    csv_files = {}
    csv_writers = {}
    for name, _, _ in BUCKETS:
        atf_files[name] = (OUTDIR / f"cdli_{name}.atf").open("w", encoding="utf-8")
        csv_files[name] = (OUTDIR / f"cdli_{name}_seqs.csv").open("w", encoding="utf-8", newline="")
        csv_writers[name] = csv.writer(csv_files[name])
        csv_writers[name].writerow(["id_text", "n_signs", "signs_ws_joined"])

    # Stream ATF
    print("Streaming ATF, writing per-bucket subsets ...", file=sys.stderr)
    found_counts = {name: 0 for name, _, _ in BUCKETS}
    sign_counts = {name: 0 for name, _, _ in BUCKETS}
    for id_text, bucket, lines in stream_atf(ATF, text_to_bucket):
        found_counts[bucket] += 1
        # Write raw ATF subset (preserve the original lines)
        atf_files[bucket].write(f"&{id_text}\n")
        for raw, _ in lines:
            atf_files[bucket].write(raw + "\n")
        atf_files[bucket].write("\n")
        # Aggregate signs into one sequence
        all_signs = []
        for _, signs in lines:
            all_signs.extend(signs)
        if all_signs:
            csv_writers[bucket].writerow([id_text, len(all_signs), " ".join(all_signs)])
            sign_counts[bucket] += len(all_signs)

    for name, _, _ in BUCKETS:
        atf_files[name].close()
        csv_files[name].close()

    # Print summary
    print("", file=sys.stderr)
    print("Bucket               texts(cat)  texts(atf)   signs", file=sys.stderr)
    for name, _, _ in BUCKETS:
        print(f"  {name:18s}  {bucket_counts[name]:>10}  {found_counts[name]:>10}  {sign_counts[name]:>9}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
