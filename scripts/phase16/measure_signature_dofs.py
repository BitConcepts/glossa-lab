"""Phase-16: measure language-signature DoFs on each Phase-A extracted corpus.

For each corpus we compute the same 8 free variables that the CAS-YAML
morphology schemas use:

    zipf_alpha          Zipf-Mandelbrot exponent (least-squares log-log slope)
    zipf_r2             R^2 of the Zipf log-log fit
    mi_gamma            mutual-information decay exponent  I(d) ~ d^-gamma
    mi_r2_pow           R^2 of the MI power-law fit
    epistatic_2nd_norm  normalized excess pairwise MI beyond independence
    epistatic_3rd_norm  normalized excess 3rd-order MI beyond pairwise
    h1_norm             normalized unigram entropy  H1 / log2(V)
    h1_nats             unigram entropy in nats

Inputs (auto-detected from data/phase16_corpora/):
    cdli_<bucket>_seqs.csv          (Sumerian/Akkadian sign sequences)
    kee2u_tamil_morpheme_seqs.csv   (Tamil morpheme-id sequences)
    kalyanaraman_devanagari_corpus.txt (Sanskrit/Vedic vocabulary corpus)

We also compute baselines from the project's existing reference corpora if
available -- but that requires the in-package data modules; here we keep
the script standalone and operate only on Phase-A outputs plus M77 if a
sequences file is available next to the data folder.

Output:
    backend/glossa_lab/data/phase16_corpora/phase16_measured_dofs.json
    Also a CSV summary at .../phase16_measured_dofs.csv

Run:
    py scripts/phase16/measure_signature_dofs.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPDIR = ROOT / "backend" / "glossa_lab" / "data" / "phase16_corpora"
OUT_JSON = CORPDIR / "phase16_measured_dofs.json"
OUT_CSV = CORPDIR / "phase16_measured_dofs.csv"


# ---------------------------------------------------------------------------
# Pure-Python DoF computation (no scipy/numpy dependency to keep it portable
# from this script).
# ---------------------------------------------------------------------------

def loglog_lsq(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    """Return (slope, intercept, r_squared) of log-log least-squares fit on
    (xs, ys). Filters out non-positive entries. Returns (nan, nan, 0) if too
    few valid points."""
    pts = [(math.log(x), math.log(y)) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pts) < 3:
        return float("nan"), float("nan"), 0.0
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    num = sum((p[0] - mx) * (p[1] - my) for p in pts)
    den = sum((p[0] - mx) ** 2 for p in pts)
    if den == 0:
        return float("nan"), float("nan"), 0.0
    slope = num / den
    intercept = my - slope * mx
    ss_tot = sum((p[1] - my) ** 2 for p in pts)
    ss_res = sum((p[1] - (slope * p[0] + intercept)) ** 2 for p in pts)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, intercept, max(0.0, min(1.0, r2))


def shannon_entropy(counts: list[int], base: float = 2.0) -> float:
    """Shannon entropy of an unnormalized count vector."""
    total = sum(counts)
    if total <= 0:
        return 0.0
    H = 0.0
    inv = 1.0 / total
    log_base = math.log(base)
    for c in counts:
        if c > 0:
            p = c * inv
            H -= p * math.log(p) / log_base
    return H


def block_entropy(seq: list[str], n: int) -> float:
    """H_n = entropy of n-gram block distribution, in bits."""
    if len(seq) < n:
        return 0.0
    counts: Counter = Counter()
    for i in range(len(seq) - n + 1):
        counts[tuple(seq[i:i+n])] += 1
    return shannon_entropy(list(counts.values()), base=2.0)


def zipf_fit(unigram_counts: Counter) -> tuple[float, float]:
    """Return (alpha, r2) of Zipf log-log fit on the unigram count distribution."""
    counts = sorted(unigram_counts.values(), reverse=True)
    if len(counts) < 5:
        return float("nan"), 0.0
    ranks = list(range(1, len(counts) + 1))
    slope, _, r2 = loglog_lsq([float(r) for r in ranks], [float(c) for c in counts])
    return -slope, r2  # Zipf alpha is the magnitude of the slope


def mutual_information(seq: list[str], d: int, max_pairs: int = 200_000) -> float:
    """I(X_t; X_{t+d}) in bits.  We sub-sample if seq is huge."""
    n = len(seq)
    if n <= d + 1:
        return 0.0
    pairs = []
    step = max(1, (n - d) // max_pairs) if (n - d) > max_pairs else 1
    for i in range(0, n - d, step):
        pairs.append((seq[i], seq[i + d]))
    # Joint
    pair_counts: Counter = Counter(pairs)
    n_pairs = sum(pair_counts.values())
    if n_pairs == 0:
        return 0.0
    # Marginals
    x_counts: Counter = Counter()
    y_counts: Counter = Counter()
    for (x, y), c in pair_counts.items():
        x_counts[x] += c
        y_counts[y] += c
    I = 0.0
    inv = 1.0 / n_pairs
    log2 = math.log(2.0)
    for (x, y), c in pair_counts.items():
        pxy = c * inv
        px = x_counts[x] * inv
        py = y_counts[y] * inv
        if pxy > 0 and px > 0 and py > 0:
            I += pxy * math.log(pxy / (px * py)) / log2
    return I


def mi_decay(seq: list[str], dists: list[int] = None) -> tuple[float, float]:
    """Fit MI(d) ~ d^-gamma; return (gamma, r2_power)."""
    if dists is None:
        dists = [1, 2, 3, 4, 5, 7, 10, 15, 20]
    pts = []
    for d in dists:
        v = mutual_information(seq, d)
        if v > 0:
            pts.append((d, v))
    if len(pts) < 3:
        return float("nan"), 0.0
    xs = [float(d) for d, _ in pts]
    ys = [v for _, v in pts]
    slope, _, r2 = loglog_lsq(xs, ys)
    return -slope, r2


def epistatic_orders(seq: list[str], cap: int = 200_000) -> tuple[float, float]:
    """Compute normalized excess MI beyond independence (2nd order) and beyond
    pairwise (3rd order). Returns (eps2_norm, eps3_norm), both in [0, 1].

    eps2_norm = (H1 + H1 - H2) / H1     ~ normalized pairwise excess
    eps3_norm = (3*H1 - 3*H2 + H3) / H1 (Mobius inclusion-exclusion of Iyer)
    Both clamped to [0, 1] for the CAS-YAML scale.
    """
    if len(seq) > cap:
        # Sub-sample contiguously (keeps locality)
        seq = seq[:cap]
    H1 = block_entropy(seq, 1)
    H2 = block_entropy(seq, 2)
    H3 = block_entropy(seq, 3)
    if H1 <= 0:
        return 0.0, 0.0
    eps2 = max(0.0, 2 * H1 - H2) / H1
    eps3 = max(0.0, 3 * H1 - 3 * H2 + H3) / H1
    # Clamp for CAS-YAML normalized scale
    return min(1.0, eps2), min(1.0, eps3)


def measure_corpus(name: str, seq: list[str], note: str = "") -> dict:
    """Compute all 8 DoFs on a token sequence."""
    if not seq:
        return {"name": name, "n_tokens": 0, "n_types": 0,
                "zipf_alpha": float("nan"), "zipf_r2": 0.0,
                "mi_gamma": float("nan"), "mi_r2_pow": 0.0,
                "epistatic_2nd_norm": 0.0, "epistatic_3rd_norm": 0.0,
                "h1_norm": 0.0, "h1_nats": 0.0,
                "note": note + " (empty)"}
    unigrams = Counter(seq)
    V = len(unigrams)
    H1_bits = shannon_entropy(list(unigrams.values()), base=2.0)
    H1_nats = H1_bits * math.log(2.0)
    h1_norm = H1_bits / math.log2(V) if V > 1 else 0.0
    zipf_alpha, zipf_r2 = zipf_fit(unigrams)
    mi_gamma, mi_r2 = mi_decay(seq)
    eps2, eps3 = epistatic_orders(seq)
    return {
        "name": name,
        "n_tokens": len(seq),
        "n_types": V,
        "zipf_alpha": round(zipf_alpha, 4),
        "zipf_r2": round(zipf_r2, 4),
        "mi_gamma": round(mi_gamma, 4),
        "mi_r2_pow": round(mi_r2, 4),
        "epistatic_2nd_norm": round(eps2, 4),
        "epistatic_3rd_norm": round(eps3, 4),
        "h1_norm": round(h1_norm, 4),
        "h1_nats": round(H1_nats, 4),
        "note": note,
    }


# ---------------------------------------------------------------------------
# Corpus loaders
# ---------------------------------------------------------------------------

def load_cdli_seqs(path: Path) -> list[str]:
    """Concatenate the per-text sign sequences into one stream."""
    out: list[str] = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        r = csv.DictReader(fh)
        for row in r:
            tokens = (row.get("signs_ws_joined") or "").strip().split()
            out.extend(tokens)
    return out


def load_kee2u_seqs(path: Path) -> list[str]:
    """Concatenate Tamil morpheme-id sequences."""
    out: list[str] = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        r = csv.DictReader(fh)
        for row in r:
            tokens = (row.get("morpheme_ids_ws_joined") or "").strip().split()
            out.extend(tokens)
    return out


def load_kalyanaraman_seqs(path: Path) -> list[str]:
    """Whitespace-tokenize the Devanagari corpus."""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text.split()


def main() -> int:
    if not CORPDIR.exists():
        print(f"ERROR: phase-16 corpora dir not found: {CORPDIR}", file=sys.stderr)
        return 1

    results: list[dict] = []

    # CDLI buckets
    for bucket in ["sumerian_ur3", "sumerian_ob_lit", "akkadian_ob", "akkadian_na"]:
        p = CORPDIR / f"cdli_{bucket}_seqs.csv"
        if p.exists():
            seq = load_cdli_seqs(p)
            note = f"CDLI subset {bucket}"
            r = measure_corpus(f"cdli_{bucket}", seq, note=note)
            print(f"  cdli_{bucket}: n_tokens={r['n_tokens']} V={r['n_types']} "
                  f"zipf_alpha={r['zipf_alpha']} zipf_r2={r['zipf_r2']} "
                  f"mi_gamma={r['mi_gamma']} h1_norm={r['h1_norm']}", file=sys.stderr)
            results.append(r)

    # Kee2u Tamil
    p = CORPDIR / "kee2u_tamil_morpheme_seqs.csv"
    if p.exists():
        seq = load_kee2u_seqs(p)
        r = measure_corpus("kee2u_tamil", seq, note="Kee2u Tamil morpheme-ID stream")
        print(f"  kee2u_tamil: n_tokens={r['n_tokens']} V={r['n_types']} "
              f"zipf_alpha={r['zipf_alpha']} h1_norm={r['h1_norm']}", file=sys.stderr)
        results.append(r)

    # Kalyanaraman Devanagari
    p = CORPDIR / "kalyanaraman_devanagari_corpus.txt"
    if p.exists():
        seq = load_kalyanaraman_seqs(p)
        r = measure_corpus("kalyanaraman_vedic", seq, note="Devanagari vocabulary from Kalyanaraman corpus")
        print(f"  kalyanaraman_vedic: n_tokens={r['n_tokens']} V={r['n_types']} "
              f"zipf_alpha={r['zipf_alpha']} h1_norm={r['h1_norm']}", file=sys.stderr)
        results.append(r)

    # Write outputs
    with OUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump({
            "phase": "phase16",
            "purpose": "language-signature DoF measurements on Phase-A corpora",
            "results": results,
        }, fh, indent=2)
    print(f"\nWrote {OUT_JSON}", file=sys.stderr)

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        if results:
            w = csv.DictWriter(fh, fieldnames=list(results[0].keys()))
            w.writeheader()
            for r in results:
                w.writerow(r)
    print(f"Wrote {OUT_CSV}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
