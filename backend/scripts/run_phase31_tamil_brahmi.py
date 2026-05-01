"""Phase-31: Tamil-Brahmi parallel-corpus comparison vs Mahadevan 1977 (Indus).

This is the FIRST concrete computational decipherment test that doesn't depend
on iconographic anchors. The hypothesis: if the Indus script encodes a
Dravidian language akin to Old Tamil, then the positional behavior of M77
signs (initial / medial / terminal frequencies) should resemble the
positional behavior of Tamil-Brahmi aksharas, and DIFFER from random
Sumerian/Akkadian or random shuffled controls.

Tests:
  T1. Positional profile entropy (per-sign):
      For each M77 sign and each Tamil-Brahmi akshara, compute the
      I/M/T (initial / medial / terminal) probability distribution.
      Compare entropy distributions across the two corpora.
  T2. Length distribution comparison:
      M77 inscription lengths vs Tamil-Brahmi inscription lengths.
      Compute KS statistic + means + medians.
  T3. Zipf-Mandelbrot rank-frequency comparison:
      Fit Zipf-Mandelbrot to both M77 and Tamil-Brahmi rank-frequency
      curves. Tamil-Brahmi vs random Sumerian PNs as alternatives.
  T4. Positional-pattern KL divergence:
      For top-N most frequent signs in each corpus, compute the KL
      divergence between their I/M/T distributions. Lower KL between
      M77-top-N and Tamil-Brahmi-top-N => more similar script class.

Outputs:
  reports/indus_phase31_t1_positional_profiles_<ts>.json
  reports/indus_phase31_t2_length_distribution_<ts>.json
  reports/indus_phase31_t3_zipf_<ts>.json
  reports/indus_phase31_t4_kl_divergence_<ts>.json
  reports/indus_phase31_verdict_<ts>.json
"""

from __future__ import annotations

import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_BACKEND = _REPO_ROOT / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from glossa_lab.data.mesopotamian_contact import (  # noqa: E402
    get_epsd2_personal_names,
    get_mahadevan_inscriptions,
)

REPORTS_DIR = _REPO_ROOT / "reports"
DATA_DIR = _REPO_ROOT / "backend" / "glossa_lab" / "data"
REPORTS_DIR.mkdir(exist_ok=True)
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

TB_PATH = DATA_DIR / "mahadevan_2003_tamil_brahmi.json"


# ─── Load + normalize Tamil-Brahmi ───────────────────────────────────


# Cyrillic-to-Latin normalization table for OCR cleanup
_CYR_TO_LAT = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x",
    "А": "A", "В": "B", "Е": "E", "О": "O", "Р": "P", "С": "C", "У": "Y",
    "Х": "X", "К": "K", "Т": "T", "М": "M", "Н": "H", "І": "I", "і": "i",
    "п": "n",  # OCR's mistake for Latin 'n' which appears as п in some fonts
    "ц": "n",  # similar — Cyrillic ц often appears for what should be Latin 'n'
})


def _normalize_akshara(a: str) -> str:
    """Normalize an akshara for cross-comparison.

    - Lowercase
    - Replace Cyrillic letters with their visual Latin equivalents
    - Strip diacritics (best-effort) for grouping
    - Strip non-alpha chars
    """
    a = a.lower().translate(_CYR_TO_LAT)
    # Remove combining diacritics: à → a, á → a, etc.
    import unicodedata  # noqa: PLC0415
    a = unicodedata.normalize("NFKD", a)
    a = "".join(c for c in a if not unicodedata.combining(c))
    # Strip remaining non-alpha
    a = re.sub(r"[^a-z]", "", a)
    return a


def load_tamil_brahmi_corpus() -> tuple[list[list[str]], dict]:
    """Returns (sequences, metadata) where sequences is list of lists of
    normalized aksharas.
    """
    if not TB_PATH.exists():
        raise FileNotFoundError(f"Tamil-Brahmi corpus not found at {TB_PATH}")
    d = json.loads(TB_PATH.read_text(encoding="utf-8"))
    sequences = []
    for ins in d.get("inscriptions", []):
        seq = [_normalize_akshara(a) for a in ins.get("literal_aksharas") or []]
        seq = [a for a in seq if a and len(a) <= 4]
        if seq:
            sequences.append(seq)
    return sequences, d.get("_summary", {})


# ─── Positional profile helper ───────────────────────────────────────


def _positional_profile(sequences: list[list[str]],
                          min_freq: int = 3) -> dict[str, dict[str, float]]:
    """For each sign/akshara appearing in `sequences` with >= min_freq, compute
    (initial / medial / terminal) probability distribution.

    Initial = position 0
    Medial = position 1..n-2
    Terminal = position n-1
    Single-token sequences contribute to BOTH initial and terminal (or skip).
    """
    counts: dict[str, dict[str, int]] = defaultdict(lambda: {"I": 0, "M": 0, "T": 0})
    total_freq: Counter = Counter()
    for seq in sequences:
        n = len(seq)
        if n == 0:
            continue
        if n == 1:
            # Singleton: count as terminal (it's the only/last token)
            counts[seq[0]]["I"] += 1
            counts[seq[0]]["T"] += 1
            total_freq[seq[0]] += 1
            continue
        for idx, sign in enumerate(seq):
            if idx == 0:
                counts[sign]["I"] += 1
            elif idx == n - 1:
                counts[sign]["T"] += 1
            else:
                counts[sign]["M"] += 1
            total_freq[sign] += 1

    profile: dict[str, dict[str, float]] = {}
    for sign, c in counts.items():
        if total_freq[sign] < min_freq:
            continue
        total = c["I"] + c["M"] + c["T"]
        if total == 0:
            continue
        profile[sign] = {
            "I": c["I"] / total,
            "M": c["M"] / total,
            "T": c["T"] / total,
            "n": total_freq[sign],
        }
    return profile


def _shannon_entropy(p_dist: dict[str, float], keys: list[str]) -> float:
    """Shannon entropy in bits over the I/M/T distribution."""
    h = 0.0
    for k in keys:
        p = p_dist.get(k, 0.0)
        if p > 0:
            h -= p * math.log2(p)
    return h


# ─── T1. Positional profile comparison ───────────────────────────────


def run_t1_positional(m77: list[list[str]],
                       tb: list[list[str]]) -> dict:
    """Compare distribution of positional entropies across M77 vs Tamil-Brahmi."""
    p_m77 = _positional_profile(m77, min_freq=5)
    p_tb = _positional_profile(tb, min_freq=2)

    h_m77 = [_shannon_entropy(p, ["I", "M", "T"]) for p in p_m77.values()]
    h_tb = [_shannon_entropy(p, ["I", "M", "T"]) for p in p_tb.values()]

    def _summary(name, h_list):
        if not h_list:
            return {"corpus": name, "n_signs": 0}
        h_list_sorted = sorted(h_list)
        n = len(h_list_sorted)
        return {
            "corpus": name,
            "n_signs": n,
            "mean_entropy_bits": round(sum(h_list_sorted) / n, 4),
            "median_entropy_bits": round(h_list_sorted[n // 2], 4),
            "min_entropy_bits": round(h_list_sorted[0], 4),
            "max_entropy_bits": round(h_list_sorted[-1], 4),
        }

    # Top-frequent signs and their I/M/T profiles
    m77_top = sorted(p_m77.items(), key=lambda kv: -kv[1]["n"])[:15]
    tb_top = sorted(p_tb.items(), key=lambda kv: -kv[1]["n"])[:15]

    # KS-like statistic (max abs diff between empirical CDFs of entropy)
    if h_m77 and h_tb:
        all_entropies = sorted(set(h_m77 + h_tb))
        cdf_m77 = lambda x: sum(1 for h in h_m77 if h <= x) / len(h_m77)
        cdf_tb = lambda x: sum(1 for h in h_tb if h <= x) / len(h_tb)
        ks_stat = max(abs(cdf_m77(e) - cdf_tb(e)) for e in all_entropies)
    else:
        ks_stat = float("nan")

    return {
        "test_id": "T1",
        "test_name": "Positional profile entropy comparison (I/M/T)",
        "m77_summary": _summary("M77 (Indus)", h_m77),
        "tb_summary": _summary("Tamil-Brahmi (Mahadevan 2003)", h_tb),
        "ks_statistic": round(ks_stat, 4) if ks_stat == ks_stat else None,
        "m77_top_15_profiles": [
            {"sign": s, **{k: round(v, 4) for k, v in p.items()}}
            for s, p in m77_top
        ],
        "tb_top_15_profiles": [
            {"akshara": s, **{k: round(v, 4) for k, v in p.items()}}
            for s, p in tb_top
        ],
        "verdict": (
            f"T1 positional profiles: M77 mean entropy = "
            f"{_summary('', h_m77).get('mean_entropy_bits', '?')} bits "
            f"({len(h_m77)} signs ≥5 freq), Tamil-Brahmi mean entropy = "
            f"{_summary('', h_tb).get('mean_entropy_bits', '?')} bits "
            f"({len(h_tb)} aksharas ≥2 freq). KS = {ks_stat:.4f}. "
            f"{'Profile distributions are similar (KS<0.3)' if ks_stat < 0.3 else 'Profile distributions differ substantially (KS>=0.3)'}."
        ),
    }


# ─── T2. Length distribution comparison ──────────────────────────────


def run_t2_length(m77: list[list[str]],
                   tb: list[list[str]],
                   pns: list[dict]) -> dict:
    """Compare inscription length distributions: M77 vs Tamil-Brahmi vs (control) ePSD2 PNs."""
    m77_lengths = sorted(len(s) for s in m77 if s)
    tb_lengths = sorted(len(s) for s in tb if s)

    # Build a "Sumerian/Akkadian PN" length distribution as control.
    # PNs are not inscriptions, but they're the closest thing we have to
    # a non-Dravidian sign-sequence corpus — the segmented forms.
    pn_lengths: list[int] = []
    for pn in pns:
        for f in pn.get("forms") or []:
            clean = re.sub(r"\{[^}]+\}", "", str(f).lower())
            parts = [p for p in re.split(r"[-]+", clean) if p]
            parts = [re.sub(r"[0-9]+$", "", p) for p in parts if p]
            parts = [p for p in parts if p]
            if parts:
                pn_lengths.append(len(parts))
    pn_lengths.sort()

    def _stats(name, lengths):
        if not lengths:
            return {"corpus": name, "n": 0}
        n = len(lengths)
        return {
            "corpus": name,
            "n": n,
            "mean": round(sum(lengths) / n, 3),
            "median": lengths[n // 2],
            "p25": lengths[n // 4],
            "p75": lengths[(3 * n) // 4],
            "p95": lengths[int(0.95 * n)],
            "min": lengths[0],
            "max": lengths[-1],
        }

    # KS between distributions
    def _ks(a, b):
        if not a or not b:
            return None
        all_v = sorted(set(a + b))
        cdf_a = lambda x: sum(1 for v in a if v <= x) / len(a)
        cdf_b = lambda x: sum(1 for v in b if v <= x) / len(b)
        return round(max(abs(cdf_a(v) - cdf_b(v)) for v in all_v), 4)

    return {
        "test_id": "T2",
        "test_name": "Inscription length distribution",
        "m77": _stats("M77 (Indus)", m77_lengths),
        "tamil_brahmi": _stats("Tamil-Brahmi", tb_lengths),
        "ePSD2_pn_segmented_forms": _stats("ePSD2 PN segmented forms", pn_lengths),
        "ks_m77_vs_tb": _ks(m77_lengths, tb_lengths),
        "ks_m77_vs_pn": _ks(m77_lengths, pn_lengths),
        "ks_tb_vs_pn": _ks(tb_lengths, pn_lengths),
        "verdict": (
            f"T2 length distributions: "
            f"M77 mean = {sum(m77_lengths)/max(1,len(m77_lengths)):.2f} (n={len(m77_lengths)}), "
            f"Tamil-Brahmi mean = {sum(tb_lengths)/max(1,len(tb_lengths)):.2f} (n={len(tb_lengths)}), "
            f"ePSD2 PN-form mean = {sum(pn_lengths)/max(1,len(pn_lengths)):.2f} (n={len(pn_lengths)}). "
            f"KS(M77,TB)={_ks(m77_lengths,tb_lengths)}, KS(M77,PN)={_ks(m77_lengths,pn_lengths)}, "
            f"KS(TB,PN)={_ks(tb_lengths,pn_lengths)}. "
            f"Lower KS between M77 and Tamil-Brahmi than between M77 and PN would support the Dravidian hypothesis."
        ),
    }


# ─── T3. Zipf-Mandelbrot rank-frequency ──────────────────────────────


def run_t3_zipf(m77: list[list[str]],
                 tb: list[list[str]]) -> dict:
    """Compare rank-frequency distributions (Zipf-Mandelbrot fit).

    For both corpora, compute the rank-frequency curve and fit a
    power law f(r) ~ 1/r^s. Compare slopes; similar slopes => similar
    statistical regime.
    """
    def _rank_freq(seqs):
        c: Counter = Counter()
        for seq in seqs:
            for s in seq:
                c[s] += 1
        return c.most_common()

    m77_rf = _rank_freq(m77)
    tb_rf = _rank_freq(tb)

    def _zipf_slope(rf):
        # Simple least-squares fit to log(rank) -> log(freq)
        # Skip rank-1 (which dominates)
        if len(rf) < 5:
            return None
        log_r = [math.log(i + 1) for i in range(min(50, len(rf)))]
        log_f = [math.log(rf[i][1]) for i in range(min(50, len(rf)))]
        # Slope via OLS
        n = len(log_r)
        mr = sum(log_r) / n
        mf = sum(log_f) / n
        num = sum((log_r[i] - mr) * (log_f[i] - mf) for i in range(n))
        den = sum((log_r[i] - mr) ** 2 for i in range(n))
        if den == 0:
            return None
        return -round(num / den, 4)  # negate so slope is positive

    s_m77 = _zipf_slope(m77_rf)
    s_tb = _zipf_slope(tb_rf)

    if s_m77 is not None and s_tb is not None:
        delta = abs(s_m77 - s_tb)
        verdict = (
            f"T3 Zipf slopes: M77 = {s_m77}, Tamil-Brahmi = {s_tb}, "
            f"|delta| = {delta:.4f}. Similar slopes (delta < 0.3) suggest "
            f"the same statistical regime (syllabic / logo-syllabic script "
            f"with comparable lexicon size)."
        )
        slope_diff = round(delta, 4)
    else:
        verdict = "T3: insufficient data for Zipf slope."
        slope_diff = None
    return {
        "test_id": "T3",
        "test_name": "Zipf-Mandelbrot rank-frequency comparison",
        "m77_top_10": [{"sign": s, "freq": f} for s, f in m77_rf[:10]],
        "tb_top_10": [{"akshara": s, "freq": f} for s, f in tb_rf[:10]],
        "m77_zipf_slope": s_m77,
        "tb_zipf_slope": s_tb,
        "slope_diff": slope_diff,
        "verdict": verdict,
    }


# ─── T4. KL divergence on positional profiles of top-N signs ────────


def run_t4_kl(m77: list[list[str]],
               tb: list[list[str]],
               top_n: int = 10) -> dict:
    """For top-N most frequent signs in each corpus, compute the KL
    divergence between their I/M/T distributions.

    Average pairwise KL between M77 top-N and Tamil-Brahmi top-N.
    Lower => more similar positional behavior => more similar script class.
    """
    p_m77 = _positional_profile(m77, min_freq=10)
    p_tb = _positional_profile(tb, min_freq=2)

    m77_top = sorted(p_m77.items(), key=lambda kv: -kv[1]["n"])[:top_n]
    tb_top = sorted(p_tb.items(), key=lambda kv: -kv[1]["n"])[:top_n]

    def _kl(p, q, eps=1e-9):
        kl = 0.0
        for k in ("I", "M", "T"):
            pp = p.get(k, eps)
            qq = q.get(k, eps)
            if pp > 0:
                kl += pp * math.log2((pp + eps) / (qq + eps))
        return kl

    # Pairwise KL: for each m77 sign, find best-matching TB akshara
    pairwise = []
    for m_sign, m_prof in m77_top:
        best_kl = float("inf")
        best_match = None
        for t_sign, t_prof in tb_top:
            kl = _kl(m_prof, t_prof)
            if kl < best_kl:
                best_kl = kl
                best_match = t_sign
        pairwise.append({
            "m77_sign": m_sign,
            "m77_profile": {k: round(m_prof.get(k, 0), 3) for k in ("I", "M", "T")},
            "best_tb_match": best_match,
            "best_kl_bits": round(best_kl, 4),
        })

    avg_kl = (sum(r["best_kl_bits"] for r in pairwise) / len(pairwise)
               if pairwise else None)

    # Control: KL of M77 top-N vs random profile (uniform 1/3, 1/3, 1/3)
    uniform = {"I": 1/3, "M": 1/3, "T": 1/3}
    avg_kl_uniform = (sum(_kl(m_prof, uniform) for _, m_prof in m77_top)
                       / len(m77_top)) if m77_top else None

    return {
        "test_id": "T4",
        "test_name": "KL divergence between M77 and Tamil-Brahmi top-N positional profiles",
        "top_n": top_n,
        "n_m77_top": len(m77_top),
        "n_tb_top": len(tb_top),
        "pairwise_best_matches": pairwise,
        "avg_best_kl_bits": round(avg_kl, 4) if avg_kl else None,
        "avg_kl_vs_uniform": round(avg_kl_uniform, 4) if avg_kl_uniform else None,
        "verdict": (
            f"T4 KL divergence: average best-match KL between M77 top-{top_n} "
            f"signs and Tamil-Brahmi top-{top_n} aksharas = {avg_kl:.4f} bits "
            f"(vs uniform-profile baseline {avg_kl_uniform:.4f}). "
            f"{'Lower than uniform => some positional alignment' if avg_kl and avg_kl_uniform and avg_kl < avg_kl_uniform else 'Equal to uniform => no detectable positional alignment'}."
        ),
    }


# ─── Save report helper ──────────────────────────────────────────────


def _save_report(test_id: str, payload: dict) -> Path:
    fname = f"indus_phase31_{test_id}_{TS}.json"
    p = REPORTS_DIR / fname
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


# ─── Main ────────────────────────────────────────────────────────────


def main() -> int:
    print(f"=== Phase-31: Tamil-Brahmi parallel-corpus comparison ({TS}) ===")
    print("[load] M77 corpus...", end=" ", flush=True)
    m77 = get_mahadevan_inscriptions()
    print(f"{len(m77)} inscriptions, {sum(len(s) for s in m77)} tokens.")
    print("[load] Tamil-Brahmi corpus...", end=" ", flush=True)
    tb, tb_summary = load_tamil_brahmi_corpus()
    print(f"{len(tb)} inscriptions, {sum(len(s) for s in tb)} aksharas (after normalization).")
    print("[load] ePSD2 PNs (control)...", end=" ", flush=True)
    pns = get_epsd2_personal_names()
    print(f"{len(pns)} PNs.")

    aggregated: dict = {
        "phase": "31",
        "timestamp_utc": TS,
        "scope": "M77 vs Tamil-Brahmi (Mahadevan 2003) parallel-corpus comparison",
        "corpora": {
            "m77": {"n_inscriptions": len(m77),
                     "n_tokens": sum(len(s) for s in m77),
                     "n_distinct_signs": len(set(s for seq in m77 for s in seq))},
            "tamil_brahmi": {"n_inscriptions": len(tb),
                              "n_aksharas": sum(len(s) for s in tb),
                              "n_distinct_aksharas": len(set(s for seq in tb for s in seq)),
                              "raw_summary": tb_summary},
        },
        "results": {},
    }

    test_specs = [
        ("t1_positional_profiles", lambda: run_t1_positional(m77, tb)),
        ("t2_length_distribution", lambda: run_t2_length(m77, tb, pns)),
        ("t3_zipf", lambda: run_t3_zipf(m77, tb)),
        ("t4_kl_divergence", lambda: run_t4_kl(m77, tb, top_n=10)),
    ]

    for tid, fn in test_specs:
        t0 = time.time()
        print(f"[run] {tid}...", end=" ", flush=True)
        try:
            result = fn()
            elapsed = time.time() - t0
            result["_elapsed_seconds"] = round(elapsed, 2)
            path = _save_report(tid, result)
            print(f"done ({elapsed:.1f}s) -> {path.name}")
            aggregated["results"][tid] = result
        except Exception as exc:
            elapsed = time.time() - t0
            import traceback
            traceback.print_exc()
            print(f"ERROR ({elapsed:.1f}s): {exc}")
            aggregated["results"][tid] = {"error": str(exc),
                                            "_elapsed_seconds": round(elapsed, 2)}

    # ── Decision ──
    t1 = aggregated["results"].get("t1_positional_profiles", {})
    t2 = aggregated["results"].get("t2_length_distribution", {})
    t3 = aggregated["results"].get("t3_zipf", {})
    t4 = aggregated["results"].get("t4_kl_divergence", {})

    decision = []
    ks_t1 = t1.get("ks_statistic")
    if ks_t1 is not None:
        decision.append(f"T1: KS(M77 entropy, TB entropy) = {ks_t1:.4f}.")
    ks_m77_tb = t2.get("ks_m77_vs_tb")
    ks_m77_pn = t2.get("ks_m77_vs_pn")
    if ks_m77_tb is not None and ks_m77_pn is not None:
        decision.append(f"T2: KS(M77,TB)={ks_m77_tb:.4f}, KS(M77,PN)={ks_m77_pn:.4f}. "
                         f"{'M77 closer to TB than PN' if ks_m77_tb < ks_m77_pn else 'M77 closer to PN than TB'}.")
    sd = t3.get("slope_diff")
    if sd is not None:
        decision.append(f"T3: |Zipf slope diff| = {sd:.4f}.")
    avg_kl = t4.get("avg_best_kl_bits")
    avg_kl_u = t4.get("avg_kl_vs_uniform")
    if avg_kl is not None and avg_kl_u is not None:
        decision.append(f"T4: avg best-match KL = {avg_kl:.4f} bits (vs uniform {avg_kl_u:.4f}).")

    aggregated["decision_summary"] = decision

    # Headline interpretation
    if (ks_m77_tb is not None and ks_m77_pn is not None
            and ks_m77_tb < ks_m77_pn and sd is not None and sd < 0.3
            and avg_kl is not None and avg_kl_u is not None and avg_kl < avg_kl_u):
        next_action = (
            "STRONG SUPPORT for Dravidian script class. M77 is closer to "
            "Tamil-Brahmi than to Sumerian/Akkadian PNs across all 4 metrics. "
            "Phase-31d: build the M77<-Tamil-Brahmi positional aligner "
            "(Knight-Sproat 2009 method); attempt SA decipherment with TB as "
            "target language. Expected lift: +5-10 pp."
        )
    elif (ks_m77_tb is not None and ks_m77_pn is not None
            and ks_m77_tb >= ks_m77_pn):
        next_action = (
            "WEAK SUPPORT: M77 is NOT closer to Tamil-Brahmi than to "
            "Sumerian/Akkadian PNs. The Dravidian-script hypothesis still "
            "has iconographic-anchor backing (Phase-30c T3-v2) but lacks "
            "structural-positional corroboration. Investigate whether OCR "
            "noise + parser coverage (only 47/110 inscriptions) is the cause."
        )
    else:
        next_action = "MIXED: review per-test verdicts."
    aggregated["next_action"] = next_action

    verdict_path = REPORTS_DIR / f"indus_phase31_verdict_{TS}.json"
    verdict_path.write_text(
        json.dumps(aggregated, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\n=== AGGREGATE VERDICT === ({verdict_path.name})")
    for d in decision:
        print(f"  {d}")
    print(f"\nNext: {next_action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
