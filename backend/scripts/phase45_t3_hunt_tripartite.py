"""Phase-45 T3: Hunt Tripartite Formula — Formal Test.

Hunt's "Without Kings or Conquests" argues Indus inscriptions follow a
tripartite structure:
  [INITIAL faunal/identity signs] + [medial sign(s)] + [TERMINAL signs]

Where:
  • INITIAL_STRONG signs (avg_pos < 0.2, is_starter=True) associate with
    specific faunal/identity iconography (unicorn, zebu, elephant…)
  • TERMINAL_STRONG signs (avg_pos > 0.7, is_ending=True) are positionally
    restricted regardless of motif

This script:
  1. Classifies signs into INITIAL_STRONG / TERMINAL_STRONG / MEDIAL pools
     using the Holdat roles CSV.
  2. For each INITIAL_STRONG sign, computes its iconography distribution
     across all inscriptions it appears in — tests if it is iconographically
     restricted (favours a specific motif).
  3. For TERMINAL_STRONG signs, tests iconographic spread (Hunt: should be
     motif-independent, unlike classifiers which DO restrict by motif).
  4. Reports chi-squared tests via scipy and torch-accelerated contingency
     matrices for the iconography association.

GPU: uses torch for contingency matrix construction; CUDA if available.

Output: reports/phase45_t3_hunt_tripartite.json
"""
from __future__ import annotations
import csv, json, math
from collections import Counter, defaultdict
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None
    DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

try:
    from scipy.stats import chi2_contingency
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("[WARN] scipy not available — chi-squared values will be approximated")

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES   = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT = REPORTS / "phase45_t3_hunt_tripartite.json"

# Thresholds for sign classification
INITIAL_POS_MAX  = 0.25   # avg_position ≤ this
TERMINAL_POS_MIN = 0.70   # avg_position ≥ this
MIN_COUNT        = 8      # minimum occurrences to include a sign

# Iconography categories: faunal identity (Hunt: associated with specific owners)
FAUNAL = {"unicorn", "zebu", "elephant", "rhinoceros", "tiger", "bison",
          "gharial", "buffalo", "bull", "ram", "fish"}
# Non-faunal / abstract / geometric
NON_FAUNAL = {"geometric", "abstract", "indeterminate", "tablet",
              "terracotta", "copper", "bone", "potsherd"}


def load_roles() -> dict[str, dict]:
    roles: dict[str, dict] = {}
    with open(ROLES, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            sym = r["symbol"]
            roles[sym] = {
                "count": int(r.get("count", 0) or 0),
                "avg_position": float(r.get("avg_position", 0.5) or 0.5),
                "is_starter": r.get("is_starter", "False") == "True",
                "is_ending": r.get("is_ending", "False") == "True",
                "semantic_role": r.get("semantic_role", "UNKNOWN"),
            }
    return roles


def load_corpus() -> list[dict]:
    seals: dict[str, dict] = {}
    with open(CORPUS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cisi = r["cisi_number"]
            pos = int(r.get("position", 0) or 0)
            if cisi not in seals:
                seals[cisi] = {
                    "signs": [],
                    "site": r.get("site", ""),
                    "icon": (r.get("iconography") or "").strip().lower(),
                }
            while len(seals[cisi]["signs"]) <= pos:
                seals[cisi]["signs"].append("")
            seals[cisi]["signs"][pos] = r["letters"]
    inscriptions = []
    for cisi, d in seals.items():
        signs = [s for s in d["signs"] if s]
        if signs:
            inscriptions.append({
                "id": cisi,
                "signs": signs,
                "site": d["site"],
                "icon": d["icon"],
            })
    return inscriptions


def sign_icon_counter(sign: str, inscriptions: list[dict]) -> Counter:
    """Return iconography distribution for inscriptions containing *sign*."""
    c: Counter = Counter()
    for ins in inscriptions:
        if sign in ins["signs"]:
            icon = ins["icon"] or "unknown"
            c[icon] += 1
    return c


def icon_entropy(ctr: Counter) -> float:
    total = sum(ctr.values())
    if total == 0:
        return 0.0
    h = 0.0
    for v in ctr.values():
        p = v / total
        if p > 0:
            h -= p * math.log2(p)
    max_h = math.log2(len(ctr)) if len(ctr) > 1 else 1.0
    return h / max_h  # normalised


def build_contingency_torch(
    signs: list[str],
    inscriptions: list[dict],
    icons: list[str],
) -> "torch.Tensor | None":
    """Build a [signs × icons] count matrix on GPU if available."""
    if torch is None:
        return None
    sign_idx = {s: i for i, s in enumerate(signs)}
    icon_idx = {ic: i for i, ic in enumerate(icons)}
    mat = torch.zeros(len(signs), len(icons), device=DEVICE, dtype=torch.float32)
    for ins in inscriptions:
        ic = ins["icon"] or "unknown"
        if ic not in icon_idx:
            continue
        ic_i = icon_idx[ic]
        for s in set(ins["signs"]):
            if s in sign_idx:
                mat[sign_idx[s], ic_i] += 1.0
    return mat.cpu()


def chi2_approx(observed: Counter, all_icons: list[str]) -> tuple[float, float]:
    """Compute chi-squared for uniform distribution null model (no scipy)."""
    total = sum(observed.values())
    k = len(all_icons)
    if total == 0 or k <= 1:
        return 0.0, 1.0
    expected = total / k
    chi2 = sum((observed.get(ic, 0) - expected) ** 2 / expected for ic in all_icons)
    # p-value approximation (very rough — use scipy for real p-values)
    # chi2 > 2k is a heuristic for "significant"
    p_approx = 0.05 if chi2 > 2 * k else 0.5
    return chi2, p_approx


def main() -> None:
    print("Phase-45 T3: Hunt Tripartite Formula — Formal Test\n")

    roles = load_roles()
    inscriptions = load_corpus()
    print(f"Loaded {len(roles)} sign roles, {len(inscriptions)} inscriptions")

    # --- Classify signs ---
    initial_strong: list[str] = []
    terminal_strong: list[str] = []
    medial: list[str] = []

    for sym, r in roles.items():
        if r["count"] < MIN_COUNT:
            continue
        avg_p = r["avg_position"]
        if avg_p <= INITIAL_POS_MAX and r["is_starter"]:
            initial_strong.append(sym)
        elif avg_p >= TERMINAL_POS_MIN and r["is_ending"]:
            terminal_strong.append(sym)
        else:
            medial.append(sym)

    print(f"\nSign pools (count ≥ {MIN_COUNT}):")
    print(f"  INITIAL_STRONG : {len(initial_strong)}")
    print(f"  TERMINAL_STRONG: {len(terminal_strong)}")
    print(f"  MEDIAL         : {len(medial)}")

    # Collect all icon labels
    all_icons_ctr: Counter = Counter()
    for ins in inscriptions:
        all_icons_ctr[(ins["icon"] or "unknown")] += 1
    top_icons = [ic for ic, _ in all_icons_ctr.most_common(20)]

    # --- GPU contingency matrix for INITIAL_STRONG ---
    print(f"\n[GPU:{DEVICE}] Building INITIAL_STRONG contingency matrix…")
    mat_initial = build_contingency_torch(initial_strong, inscriptions, top_icons)
    print(f"[GPU:{DEVICE}] Building TERMINAL_STRONG contingency matrix…")
    mat_terminal = build_contingency_torch(terminal_strong, inscriptions, top_icons)

    # --- Per-sign iconography analysis ---
    initial_results = []
    for sym in sorted(initial_strong):
        ctr = sign_icon_counter(sym, inscriptions)
        top_icon, top_cnt = ctr.most_common(1)[0] if ctr else ("?", 0)
        total = sum(ctr.values())
        top_pct = top_cnt / total if total else 0
        ent = icon_entropy(ctr)
        faunal_cnt = sum(ctr[ic] for ic in ctr if any(ic.startswith(f) for f in FAUNAL))
        faunal_pct = faunal_cnt / total if total else 0
        # Chi-squared vs uniform null (sign appears equally across all iconographies)
        if HAS_SCIPY:
            obs_vec = [ctr.get(ic, 0) for ic in top_icons]
            total_obs = sum(obs_vec)
            if total_obs > 0 and len([v for v in obs_vec if v > 0]) >= 2:
                try:
                    # Use goodness-of-fit: observed vs uniform expected
                    import numpy as _np
                    expected_uniform = [total_obs / len(obs_vec)] * len(obs_vec)
                    from scipy.stats import chisquare
                    chi2_val, p_val = chisquare(obs_vec, f_exp=expected_uniform)
                except Exception:
                    chi2_val, p_val = chi2_approx(ctr, top_icons)
            else:
                chi2_val, p_val = 0.0, 1.0
        else:
            chi2_val, p_val = chi2_approx(ctr, top_icons)

        restricted = ent < 0.7  # icon entropy below 0.7 → restricted to few motifs
        r = roles[sym]
        print(f"  {sym} (pos={r['avg_position']:.2f}, n={total}): "
              f"top={top_icon}({top_pct:.0%}), "
              f"faunal={faunal_pct:.0%}, ent={ent:.2f}, "
              f"restricted={'YES' if restricted else 'no'}")

        initial_results.append({
            "sign": sym,
            "avg_position": r["avg_position"],
            "count_in_corpus": total,
            "top_iconography": top_icon,
            "top_iconography_pct": round(top_pct, 3),
            "faunal_pct": round(faunal_pct, 3),
            "icon_normalised_entropy": round(ent, 3),
            "iconographically_restricted": restricted,
            "chi2": round(chi2_val, 3),
            "chi2_p": round(p_val, 4),
            "icon_distribution": dict(ctr.most_common(8)),
        })

    terminal_results = []
    for sym in sorted(terminal_strong):
        ctr = sign_icon_counter(sym, inscriptions)
        if not ctr:
            continue
        total = sum(ctr.values())
        ent = icon_entropy(ctr)
        top_icon, top_cnt = ctr.most_common(1)[0]
        top_pct = top_cnt / total
        if HAS_SCIPY:
            obs_vec = [ctr.get(ic, 0) for ic in top_icons if ctr.get(ic, 0) > 0]
            chi2_val, p_val = (0.0, 1.0) if len(obs_vec) < 2 else (0.0, 1.0)
        else:
            chi2_val, p_val = chi2_approx(ctr, top_icons)

        r = roles[sym]
        print(f"  {sym}† (pos={r['avg_position']:.2f}, n={total}): "
              f"ent={ent:.2f} ({'SPREAD-uniform' if ent > 0.8 else 'RESTRICTED'})")

        terminal_results.append({
            "sign": sym,
            "avg_position": r["avg_position"],
            "count_in_corpus": total,
            "top_iconography": top_icon,
            "top_iconography_pct": round(top_pct, 3),
            "icon_normalised_entropy": round(ent, 3),
            "iconographically_uniform": ent > 0.8,
            "icon_distribution": dict(ctr.most_common(8)),
        })

    # --- Test Hunt's predictions ---
    # P1: INITIAL_STRONG signs are iconographically restricted (entropy < 0.7)
    p1_restricted = sum(1 for r in initial_results if r["iconographically_restricted"])
    p1_total = len(initial_results)
    p1_support = p1_restricted / p1_total if p1_total else 0

    # P2: INITIAL_STRONG signs predominantly appear with faunal motifs
    p2_faunal_high = sum(1 for r in initial_results if r["faunal_pct"] > 0.5)
    p2_support = p2_faunal_high / p1_total if p1_total else 0

    # P3: TERMINAL_STRONG signs are iconographically uniform (entropy > 0.8)
    p3_uniform = sum(1 for r in terminal_results if r.get("iconographically_uniform"))
    p3_total = len(terminal_results)
    p3_support = p3_uniform / p3_total if p3_total else 0

    print(f"\n=== Hunt Tripartite Test Results ===")
    print(f"P1 (INITIAL_STRONG iconog-restricted): {p1_restricted}/{p1_total} = {p1_support:.1%}")
    print(f"P2 (INITIAL_STRONG faunal > 50%):      {p2_faunal_high}/{p1_total} = {p2_support:.1%}")
    print(f"P3 (TERMINAL_STRONG iconog-uniform):   {p3_uniform}/{p3_total} = {p3_support:.1%}")

    # Overall verdict
    hunt_supported = (p1_support > 0.5 or p2_support > 0.4) and p3_support > 0.4
    if hunt_supported:
        verdict = "SUPPORTED"
        note = ("INITIAL_STRONG signs show iconographic restriction/faunal preference "
                "consistent with Hunt's identity-marker hypothesis")
    elif p1_support > 0.4 or p2_support > 0.4:
        verdict = "PARTIAL_SUPPORT"
        note = "Some predictions confirmed but not consistently across all sign groups"
    else:
        verdict = "NOT_SUPPORTED"
        note = "Iconographic distributions do not strongly align with Hunt's tripartite predictions"

    print(f"\nVerdict: {verdict}")
    print(f"Note: {note}")

    # Contingency matrix as list for JSON serialisation
    mat_initial_list = mat_initial.tolist() if mat_initial is not None else None
    mat_terminal_list = mat_terminal.tolist() if mat_terminal is not None else None

    result = {
        "_citation": {"primary_sources": ["A.1"], "hunt_ref": "without_kings_or_conquests"},
        "gpu_device": DEVICE,
        "sign_pools": {
            "initial_strong_n": len(initial_strong),
            "terminal_strong_n": len(terminal_strong),
            "medial_n": len(medial),
            "thresholds": {
                "initial_pos_max": INITIAL_POS_MAX,
                "terminal_pos_min": TERMINAL_POS_MIN,
                "min_count": MIN_COUNT,
            },
        },
        "hunt_predictions": {
            "P1_initial_iconog_restricted": {
                "support": round(p1_support, 3),
                "n_supporting": p1_restricted,
                "n_total": p1_total,
            },
            "P2_initial_faunal_majority": {
                "support": round(p2_support, 3),
                "n_supporting": p2_faunal_high,
                "n_total": p1_total,
            },
            "P3_terminal_iconog_uniform": {
                "support": round(p3_support, 3),
                "n_supporting": p3_uniform,
                "n_total": p3_total,
            },
        },
        "verdict": verdict,
        "verdict_note": note,
        "initial_strong_signs": sorted(initial_strong),
        "terminal_strong_signs": sorted(terminal_strong),
        "initial_sign_analysis": sorted(initial_results, key=lambda x: -x["count_in_corpus"]),
        "terminal_sign_analysis": sorted(terminal_results, key=lambda x: -x["count_in_corpus"]),
        "top_iconography_labels": top_icons,
        "contingency_matrix_initial_strong": mat_initial_list,
        "contingency_matrix_terminal_strong": mat_terminal_list,
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
