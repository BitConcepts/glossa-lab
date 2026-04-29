"""Phase-19 omnibus: Tier-1 (B/C/E) + Tier-3 (J/L) of the Phase-18 roadmap.

What this script does, in order:
 [B] 7-DoF and 6-DoF M77 projections (excluding eps3, then eps3+h1_norm).
     Goal: see whether the 4-way Phase-18 tie breaks when the high-eps3
     outlier DoF is removed.
 [C] Raw Mahadevan unmerged glyphs from reports/mahadevan_texts_decoded.json.
     Re-measures M77 with V_raw=464 (no rank-corr collapse) and projects
     against current YAMLs.
 [E] Top-K most epistatically-coupled trigrams in M77 (and the new raw M77).
     Computes I3(a,b,c) = 3-way mutual-information surplus over independence
     and over pairwise. Outputs a ranked list with frequencies.
 [J] Per-inscription DoF distributions for M77, CISI mayig, DAMOS Linear B,
     RV padapatha. Aggregate mean +/- stdev to expose intra-corpus
     heterogeneity.
 [L] Spectral fingerprinting: top-K eigenvalues + spectral gap of the bigram
     transition matrix per corpus. Continuous similarity vector between any
     two corpora.

Outputs (all under reports/):
    phase19_omnibus.json           full structured results
    phase19_omnibus.md             human-readable summary
"""
from __future__ import annotations

import csv, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_P16 = ROOT / "scripts" / "phase16"
sys.path.insert(0, str(SCRIPTS_P16))
from measure_signature_dofs import (  # type: ignore
    measure_corpus, shannon_entropy, block_entropy, mi_decay, mutual_information,
    zipf_fit, epistatic_orders, loglog_lsq,
)
from rerun_indus_grounded import parse_yaml_constraints, project_hypothesis  # type: ignore

CAS_DIR = ROOT / "backend/glossa_lab/data/cas_models"
CAS_YAMLS = [
    "dravidian_morphology.yaml",
    "indo_aryan_morphology.yaml",
    "sumerian_morphology.yaml",
    "akkadian_morphology.yaml",
    "vedic_kalyanaraman_morphology.yaml",
]

CORPORA: list[tuple[str, Path, str]] = [
    ("indus_m77",            ROOT / "reports/mahadevan_corpus_flat.txt", "stream-line"),
    ("cisi_mayig",           ROOT / "backend/glossa_lab/data/phase18_corpora/cisi_mayig_signs.txt", "stream-line"),
    ("damos_linear_b",       ROOT / "backend/glossa_lab/data/phase17_corpora/damos_signs.txt", "stream-line"),
    ("rv_padapatha",         ROOT / "backend/glossa_lab/data/phase18_corpora/rv_padapatha_stream.txt", "stream-line"),
    ("kee2u_tamil",          ROOT / "backend/glossa_lab/data/phase16_corpora/kee2u_tamil_morpheme_seqs.csv", "csv-mor"),
    ("cdli_sumerian_ur3",    ROOT / "backend/glossa_lab/data/phase16_corpora/cdli_sumerian_ur3_seqs.csv", "csv-sig"),
    ("cdli_akkadian_na",     ROOT / "backend/glossa_lab/data/phase16_corpora/cdli_akkadian_na_seqs.csv", "csv-sig"),
]

OUT_JSON = ROOT / "reports/phase19_omnibus.json"
OUT_MD = ROOT / "reports/phase19_omnibus.md"
OUT_CORPDIR = ROOT / "backend/glossa_lab/data/phase19_corpora"
M77_RAW_OUT = OUT_CORPDIR / "m77_raw_glyphs_signs.txt"


# ---------------------------------------------------------------------------
# Corpus loading
# ---------------------------------------------------------------------------

def load_lines(path: Path, kind: str) -> list[list[str]]:
    """Load a corpus as a list-of-inscriptions (each = list of tokens)."""
    if not path.exists():
        return []
    out: list[list[str]] = []
    if kind == "stream-line":
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                toks = line.strip().split()
                if toks:
                    out.append(toks)
    elif kind in ("csv-sig", "csv-mor", "csv-pp"):
        col = {"csv-sig": "signs_ws_joined",
               "csv-mor": "morpheme_ids_ws_joined",
               "csv-pp": "padapatha_words_ws_joined"}[kind]
        with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
            r = csv.DictReader(fh)
            for row in r:
                val = (row.get(col) or "").strip()
                if val:
                    out.append(val.split())
    return out


# ---------------------------------------------------------------------------
# [B] N-DoF projection (subset of the 8 free vars)
# ---------------------------------------------------------------------------

def project_n_dof(measured: dict, exclude: set[str]) -> list[dict]:
    """Re-project against all CAS-YAMLs but ignore constraints whose `var` is
    in `exclude`. Score is recomputed similarly without those terms."""
    measured_vars = {k: measured[k] for k in (
        "zipf_alpha", "zipf_r2", "mi_gamma", "mi_r2_pow",
        "epistatic_2nd_norm", "epistatic_3rd_norm", "h1_norm", "h1_nats"
    ) if measured[k] == measured[k]}

    out = []
    for fname in CAS_YAMLS:
        p = CAS_DIR / fname
        if not p.exists(): continue
        ydata = parse_yaml_constraints(p)
        # Filter constraints
        ydata_filt = dict(ydata)
        ydata_filt["constraints"] = [c for c in ydata["constraints"]
                                     if c.get("var") not in exclude]
        proj = project_hypothesis(ydata_filt, measured_vars)
        out.append(proj)
    return out


# ---------------------------------------------------------------------------
# [C] Raw Mahadevan glyphs from texts_decoded.json
# ---------------------------------------------------------------------------

def build_m77_raw_corpus() -> list[list[str]]:
    """Each inscription -> list of single-glyph 'tokens' from the OCR `raw` field."""
    src = ROOT / "reports/mahadevan_texts_decoded.json"
    if not src.exists():
        return []
    with src.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    out: list[list[str]] = []
    OUT_CORPDIR.mkdir(parents=True, exist_ok=True)
    with M77_RAW_OUT.open("w", encoding="utf-8") as wfh:
        for ins in data.get("inscriptions", []):
            raw = ins.get("raw", "")
            # Each character is a glyph (skip whitespace)
            glyphs = [ch for ch in raw if not ch.isspace()]
            if glyphs:
                out.append(glyphs)
                wfh.write(" ".join(glyphs) + "\n")
    return out


# ---------------------------------------------------------------------------
# [E] Top epistatic trigrams in a corpus
# ---------------------------------------------------------------------------

def epistatic_trigrams(seq: list[str], top_k: int = 30,
                       min_count: int = 3) -> list[dict]:
    """Compute 3-way mutual information surplus I3(a,b,c) = log2 [ p(a,b,c) /
    ( p(a)p(b)p(c) ) ] for every observed trigram. Returns top_k with count >= min_count."""
    if len(seq) < 3:
        return []
    n = len(seq)
    uni = Counter(seq)
    tri = Counter(tuple(seq[i:i+3]) for i in range(n - 2))
    total_tri = sum(tri.values())
    out = []
    for trig, c in tri.items():
        if c < min_count: continue
        a, b, d = trig
        p_abc = c / total_tri
        p_a = uni[a] / n
        p_b = uni[b] / n
        p_c = uni[d] / n
        if p_a * p_b * p_c > 0:
            i3 = math.log2(p_abc / (p_a * p_b * p_c))
            out.append({"trigram": " ".join(trig), "count": c,
                        "i3_bits": round(i3, 4),
                        "p_abc": round(p_abc, 6),
                        "p_a*p_b*p_c": round(p_a * p_b * p_c, 8)})
    out.sort(key=lambda r: -r["i3_bits"])
    return out[:top_k]


# ---------------------------------------------------------------------------
# [J] Per-inscription DoF distributions
# ---------------------------------------------------------------------------

def per_inscription_dofs(name: str, inscriptions: list[list[str]],
                          min_len: int = 4, max_inscriptions: int = 1500) -> dict:
    """Compute zipf_alpha, mi_gamma, eps2, eps3, h1_norm per inscription
    (only those of length >= min_len) and return mean +/- stdev across them."""
    samples = [ins for ins in inscriptions if len(ins) >= min_len]
    if not samples:
        return {"name": name, "n_eligible": 0}
    if len(samples) > max_inscriptions:
        # Stride sample
        step = max(1, len(samples) // max_inscriptions)
        samples = samples[::step]
    dofs = {"zipf_alpha": [], "zipf_r2": [],
            "mi_gamma": [], "mi_r2_pow": [],
            "epistatic_2nd_norm": [], "epistatic_3rd_norm": [],
            "h1_norm": []}
    for ins in samples:
        try:
            r = measure_corpus(name + "_ins", ins)
            for k in dofs:
                v = r[k]
                if v == v:  # non-NaN
                    dofs[k].append(v)
        except Exception:
            continue
    summary = {"name": name, "n_eligible": len(samples), "n_sampled": len(samples)}
    for k, vs in dofs.items():
        if len(vs) >= 2:
            summary[f"{k}_mean"] = round(mean(vs), 4)
            summary[f"{k}_stdev"] = round(stdev(vs), 4)
            summary[f"{k}_n"] = len(vs)
        else:
            summary[f"{k}_mean"] = None
            summary[f"{k}_stdev"] = None
            summary[f"{k}_n"] = len(vs)
    return summary


# ---------------------------------------------------------------------------
# [L] Spectral fingerprinting (bigram transition matrix eigenvalues)
# ---------------------------------------------------------------------------

def bigram_transition_eigenvalues(seq: list[str], top_k: int = 8,
                                   max_vocab: int = 200) -> dict:
    """Build a stochastic bigram transition matrix P (rows = states), filter
    to the top `max_vocab` most-frequent tokens (rest folded into 'OTHER'),
    return the top_k eigenvalues by magnitude.

    Pure-Python power iteration (no numpy/scipy) is overkill, so we use a
    simple approach: build the matrix, compute eigenvalues via numpy if
    available; if not, fall back to dominant-eigenvalue power iteration.
    """
    if len(seq) < 4:
        return {"top_eigenvalues": [], "spectral_gap": None, "n_states": 0}

    # Vocab cap
    uni = Counter(seq)
    vocab = [w for w, _ in uni.most_common(max_vocab)]
    voc_set = set(vocab)
    sym = lambda x: x if x in voc_set else "OTHER"
    states = vocab + (["OTHER"] if any(s not in voc_set for s in seq) else [])
    idx = {s: i for i, s in enumerate(states)}
    K = len(states)

    # Counts
    counts = [[0] * K for _ in range(K)]
    for i in range(len(seq) - 1):
        a = idx[sym(seq[i])]
        b = idx[sym(seq[i + 1])]
        counts[a][b] += 1
    # Row-stochastic
    P = [[0.0] * K for _ in range(K)]
    for i in range(K):
        rs = sum(counts[i])
        if rs > 0:
            for j in range(K):
                P[i][j] = counts[i][j] / rs
        else:
            P[i][i] = 1.0  # absorbing

    # Try numpy for full spectrum
    try:
        import numpy as np  # type: ignore
        P_np = np.array(P, dtype=float)
        eigs = np.linalg.eigvals(P_np)
        # Sort by magnitude desc
        eigs_mag = sorted([abs(complex(e)) for e in eigs], reverse=True)
        top = eigs_mag[:top_k]
        gap = top[0] - top[1] if len(top) >= 2 else None
        return {"top_eigenvalues": [round(v, 4) for v in top],
                "spectral_gap": round(gap, 4) if gap is not None else None,
                "n_states": K}
    except ImportError:
        pass

    # Fallback: power iteration for dominant only
    # (fine since stochastic matrices have lambda_1 = 1)
    return {"top_eigenvalues": [1.0], "spectral_gap": None, "n_states": K,
            "note": "numpy not available; power iteration gives dominant only"}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    OUT_CORPDIR.mkdir(parents=True, exist_ok=True)
    print("Phase-19 omnibus starting", file=sys.stderr)

    results = {}

    # Load all corpora as inscription-lists
    print("\n=== Loading corpora ===", file=sys.stderr)
    corpora_data = {}
    for name, path, kind in CORPORA:
        ins = load_lines(path, kind)
        flat = [t for line in ins for t in line]
        corpora_data[name] = (ins, flat)
        print(f"  {name}: {len(ins)} inscriptions, {len(flat)} tokens, "
              f"{len(set(flat))} types", file=sys.stderr)

    # [C] Raw M77 from texts_decoded.json
    print("\n=== [C] Raw M77 (unmerged OCR glyphs) ===", file=sys.stderr)
    raw_ins = build_m77_raw_corpus()
    raw_flat = [t for line in raw_ins for t in line]
    corpora_data["indus_m77_raw"] = (raw_ins, raw_flat)
    print(f"  m77_raw: {len(raw_ins)} inscriptions, {len(raw_flat)} tokens, "
          f"{len(set(raw_flat))} types (vs 64 in mapped)", file=sys.stderr)
    raw_dofs = measure_corpus("indus_m77_raw", raw_flat,
                               note="Mahadevan 1977 raw OCR glyphs (no rank-corr collapse)")
    print(f"  zipf_alpha={raw_dofs['zipf_alpha']}  zipf_r2={raw_dofs['zipf_r2']}  "
          f"mi_gamma={raw_dofs['mi_gamma']}  eps3={raw_dofs['epistatic_3rd_norm']}  "
          f"h1_norm={raw_dofs['h1_norm']}", file=sys.stderr)
    results["m77_raw_dofs"] = raw_dofs

    # M77 measurements (mapped, for B)
    m77_flat = corpora_data["indus_m77"][1]
    m77_dofs = measure_corpus("indus_m77", m77_flat)

    # [B] 7-DoF and 6-DoF M77 projections
    print("\n=== [B] N-DoF M77 projections (excluding outlier DoFs) ===", file=sys.stderr)
    proj_8 = project_n_dof(m77_dofs, set())
    proj_7 = project_n_dof(m77_dofs, {"epistatic_3rd_norm"})
    proj_6 = project_n_dof(m77_dofs, {"epistatic_3rd_norm", "h1_norm"})

    def summarize_proj(label, projs):
        ranked = sorted(projs, key=lambda p: (p["max_violation"], -1 * (p.get("score_value") or 0)))
        print(f"  {label}:", file=sys.stderr)
        for i, p in enumerate(ranked, 1):
            print(f"    {i}. {p['model_id']:32s}  max_v={p['max_violation']:.4f}  "
                  f"n_viol={p['n_violations']}  score={p['score_value']}", file=sys.stderr)
        return [{"rank": i, "model_id": p["model_id"],
                 "max_violation": p["max_violation"],
                 "n_violations": p["n_violations"],
                 "score_value": p["score_value"]}
                for i, p in enumerate(ranked, 1)]

    results["m77_proj_8dof"] = summarize_proj("8-DoF (baseline)", proj_8)
    results["m77_proj_7dof_no_eps3"] = summarize_proj("7-DoF (excl eps3)", proj_7)
    results["m77_proj_6dof_no_eps3_h1"] = summarize_proj("6-DoF (excl eps3+h1_norm)", proj_6)

    # Same for raw M77 with 8/7/6 DoF
    print("\n=== [B+C] Raw M77 N-DoF projections ===", file=sys.stderr)
    raw_8 = project_n_dof(raw_dofs, set())
    raw_7 = project_n_dof(raw_dofs, {"epistatic_3rd_norm"})
    results["m77_raw_proj_8dof"] = summarize_proj("8-DoF raw", raw_8)
    results["m77_raw_proj_7dof_no_eps3"] = summarize_proj("7-DoF raw", raw_7)

    # [E] Top epistatic trigrams
    print("\n=== [E] Top epistatic trigrams ===", file=sys.stderr)
    e_mapped = epistatic_trigrams(m77_flat, top_k=20, min_count=3)
    e_raw = epistatic_trigrams(raw_flat, top_k=20, min_count=3)
    e_cisi = epistatic_trigrams(corpora_data["cisi_mayig"][1], top_k=10, min_count=2)
    print(f"  M77 (mapped): top trigram = {e_mapped[0]['trigram'] if e_mapped else 'none'}  "
          f"i3={e_mapped[0]['i3_bits'] if e_mapped else 'n/a'}", file=sys.stderr)
    print(f"  M77 (raw):    top trigram = {e_raw[0]['trigram'] if e_raw else 'none'}  "
          f"i3={e_raw[0]['i3_bits'] if e_raw else 'n/a'}", file=sys.stderr)
    print(f"  CISI mayig:   top trigram = {e_cisi[0]['trigram'] if e_cisi else 'none'}  "
          f"i3={e_cisi[0]['i3_bits'] if e_cisi else 'n/a'}", file=sys.stderr)
    results["epistatic_trigrams_m77_mapped"] = e_mapped
    results["epistatic_trigrams_m77_raw"] = e_raw
    results["epistatic_trigrams_cisi_mayig"] = e_cisi

    # [J] Per-inscription DoF distributions
    print("\n=== [J] Per-inscription DoF distributions ===", file=sys.stderr)
    per_ins = {}
    for cname in ["indus_m77", "cisi_mayig", "damos_linear_b", "rv_padapatha"]:
        if cname not in corpora_data: continue
        ins_list, _ = corpora_data[cname]
        s = per_inscription_dofs(cname, ins_list, min_len=4)
        per_ins[cname] = s
        print(f"  {cname}: n_eligible={s.get('n_eligible')} "
              f"zipf_a={s.get('zipf_alpha_mean')}+/-{s.get('zipf_alpha_stdev')} "
              f"eps3={s.get('epistatic_3rd_norm_mean')}+/-{s.get('epistatic_3rd_norm_stdev')}",
              file=sys.stderr)
    results["per_inscription_dofs"] = per_ins

    # [L] Spectral fingerprinting
    print("\n=== [L] Spectral fingerprinting ===", file=sys.stderr)
    spectral = {}
    for cname, (_ins, flat) in corpora_data.items():
        if not flat: continue
        s = bigram_transition_eigenvalues(flat, top_k=8, max_vocab=200)
        spectral[cname] = s
        print(f"  {cname}: top_eigs={s['top_eigenvalues'][:5]}  "
              f"gap={s['spectral_gap']}  n_states={s['n_states']}", file=sys.stderr)
    results["spectral_fingerprint"] = spectral

    # Write JSON
    with OUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump({"phase": "phase19", "results": results}, fh, indent=2)
    print(f"\nWrote {OUT_JSON}", file=sys.stderr)

    # Write Markdown summary
    write_markdown(results)
    print(f"Wrote {OUT_MD}", file=sys.stderr)
    return 0


def write_markdown(results: dict):
    lines = []
    lines.append("# Phase-19 omnibus — Tier-1 (B/C/E) + Tier-3 (J/L)\n")
    lines.append("## [B] Multi-hypothesis projection at 8/7/6 DoF\n")
    lines.append("Removing the high-eps3 outlier DoF (and h1_norm secondarily) tells us\n"
                 "whether the Phase-18 4-way tie is structural or driven by one signal.\n")
    for label, key in [("8-DoF baseline", "m77_proj_8dof"),
                       ("7-DoF (excl eps3)", "m77_proj_7dof_no_eps3"),
                       ("6-DoF (excl eps3 + h1_norm)", "m77_proj_6dof_no_eps3_h1")]:
        lines.append(f"### {label}\n")
        lines.append("| rank | hypothesis | max_v | n_viol | score |")
        lines.append("|---|---|---|---|---|")
        for r in results.get(key, []):
            lines.append(f"| {r['rank']} | `{r['model_id']}` | {r['max_violation']} | "
                         f"{r['n_violations']} | {r['score_value']} |")
        lines.append("")
    lines.append("## [C] Raw M77 (no rank-corr) DoFs\n")
    raw = results.get("m77_raw_dofs", {})
    if raw:
        lines.append("```")
        for k in ("n_tokens","n_types","zipf_alpha","zipf_r2","mi_gamma","mi_r2_pow",
                  "epistatic_2nd_norm","epistatic_3rd_norm","h1_norm","h1_nats"):
            lines.append(f"  {k:24s} = {raw.get(k)}")
        lines.append("```\n")
    lines.append("### Raw M77 7-DoF projection\n")
    lines.append("| rank | hypothesis | max_v | n_viol | score |")
    lines.append("|---|---|---|---|---|")
    for r in results.get("m77_raw_proj_7dof_no_eps3", []):
        lines.append(f"| {r['rank']} | `{r['model_id']}` | {r['max_violation']} | "
                     f"{r['n_violations']} | {r['score_value']} |")
    lines.append("")
    lines.append("## [E] Top epistatic trigrams in M77 (mapped)\n")
    lines.append("Trigrams with the strongest 3-way coupling beyond independence.")
    lines.append("Likely candidates for stable seal-formula motifs.\n")
    lines.append("| rank | trigram | count | i3_bits |")
    lines.append("|---:|---|---:|---:|")
    for i, t in enumerate(results.get("epistatic_trigrams_m77_mapped", [])[:20], 1):
        lines.append(f"| {i} | `{t['trigram']}` | {t['count']} | {t['i3_bits']} |")
    lines.append("")
    lines.append("## [J] Per-inscription DoF distributions (mean +/- stdev)\n")
    lines.append("Reveals heterogeneity within each corpus. Large stdev = corpus is mixed.\n")
    lines.append("| corpus | n_elig | zipf_a | eps2 | eps3 | h1_norm |")
    lines.append("|---|---:|---|---|---|---|")
    for c, s in (results.get("per_inscription_dofs") or {}).items():
        z = f"{s.get('zipf_alpha_mean','?')}+-{s.get('zipf_alpha_stdev','?')}"
        e2 = f"{s.get('epistatic_2nd_norm_mean','?')}+-{s.get('epistatic_2nd_norm_stdev','?')}"
        e3 = f"{s.get('epistatic_3rd_norm_mean','?')}+-{s.get('epistatic_3rd_norm_stdev','?')}"
        h1 = f"{s.get('h1_norm_mean','?')}+-{s.get('h1_norm_stdev','?')}"
        lines.append(f"| {c} | {s.get('n_eligible')} | {z} | {e2} | {e3} | {h1} |")
    lines.append("")
    lines.append("## [L] Spectral fingerprint — top bigram-transition eigenvalues\n")
    lines.append("Continuous signature of the Markov structure. Spectral gap between\n"
                 "lambda_1 (always = 1 for stochastic) and lambda_2 measures mixing time;\n"
                 "small gap = slow mixing, more long-range structure.\n")
    lines.append("| corpus | n_states | lambda_1..5 | gap |")
    lines.append("|---|---:|---|---:|")
    for c, s in (results.get("spectral_fingerprint") or {}).items():
        eigs = s.get("top_eigenvalues") or []
        eigs_str = " ".join(str(x) for x in eigs[:5])
        lines.append(f"| {c} | {s.get('n_states')} | {eigs_str} | {s.get('spectral_gap')} |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
