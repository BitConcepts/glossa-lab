"""Phase-19 follow-up: A (joint sign clustering), K (genre-stratified CDLI),
and CM CAS-YAML projection against M77.

[A] Joint M77 + CISI sign clustering: run Daggumati allograph detection on
    M77 (mapped + raw) and CISI mayig separately. Compare cluster shape
    statistics. ID spaces don't overlap (Mahadevan vs Parpola), so we
    can't merge clusters directly, but we can compare *cluster-shape*
    statistics: sizes, count of clusters, fraction of the alphabet that
    falls into multi-sign clusters.
[K] Genre-stratified CDLI baselines: re-bucket cdli_cat.csv by
    (period, language, genre) and re-measure DoFs per bucket. M77's
    correct comparator may be a specific genre.
[D] Project M77 (mapped + raw) through the new cypro_minoan_morphology.yaml
    to test whether ANY small-inventory undeciphered logo-syllabic script
    matches M77 better than the four natural-language families.
"""
from __future__ import annotations

import csv, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_P16 = ROOT / "scripts" / "phase16"
sys.path.insert(0, str(SCRIPTS_P16))
from measure_signature_dofs import measure_corpus  # type: ignore
from rerun_indus_grounded import parse_yaml_constraints, project_hypothesis  # type: ignore
from sign_clusters import (  # type: ignore
    compute_features, daggumati_clusters, MIN_OCCURRENCE,
)

CAS_DIR = ROOT / "backend/glossa_lab/data/cas_models"
ALL_YAMLS = [
    "dravidian_morphology.yaml",
    "indo_aryan_morphology.yaml",
    "sumerian_morphology.yaml",
    "akkadian_morphology.yaml",
    "vedic_kalyanaraman_morphology.yaml",
    "cypro_minoan_morphology.yaml",
]

OUT_JSON = ROOT / "reports/phase19_sign_clusters_genre_cm.json"
OUT_MD = ROOT / "reports/phase19_sign_clusters_genre_cm.md"


# ---------------------------------------------------------------------------
# [A] Joint sign clustering
# ---------------------------------------------------------------------------

def load_inscriptions(path: Path) -> list[list[str]]:
    out: list[list[str]] = []
    if not path.exists(): return out
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            toks = line.strip().split()
            if toks: out.append(toks)
    return out


def cluster_corpus(name: str, inscriptions: list[list[str]],
                   min_count: int) -> dict:
    """Run Daggumati allograph detection on a corpus and report cluster stats."""
    if not inscriptions:
        return {"name": name, "n_signs": 0, "clusters": []}
    feats = compute_features(inscriptions)
    eligible = [s for s, f in feats.items() if f["count"] >= min_count]
    # Use looser thresholds for small corpora
    import sign_clusters as sc  # type: ignore
    sc.MIN_OCCURRENCE = min_count
    sc.THR_POS_JS = 0.30
    sc.THR_CTX_COS = 0.45
    clusters = daggumati_clusters(feats)
    return {
        "name": name,
        "n_signs_total": len(feats),
        "n_signs_eligible": len(eligible),
        "n_clusters": len(clusters),
        "n_signs_in_multi_clusters": sum(c["size"] for c in clusters),
        "biggest_cluster": clusters[0] if clusters else None,
        "all_clusters": clusters,
    }


# ---------------------------------------------------------------------------
# [K] Genre-stratified CDLI re-extraction + measurement
# ---------------------------------------------------------------------------

CDLI_CAT = ROOT / "corpora/downloads/external_repos/cdli_gh_data/cdli_cat.csv"
CDLI_ATF = ROOT / "corpora/downloads/external_repos/cdli_gh_data/cdliatf_unblocked.atf"

# (name, language_substr, period_substr, genre_substr)
GENRE_BUCKETS = [
    ("sum_ur3_admin",  "sumerian", "ur iii",          "administrative"),
    ("sum_ur3_lex",    "sumerian", "ur iii",          "lexical"),
    ("sum_oblit_lit",  "sumerian", "old babylonian",  "literary"),
    ("akk_ob_admin",   "akkadian", "old babylonian",  "administrative"),
    ("akk_ob_letter",  "akkadian", "old babylonian",  "letter"),
    ("akk_na_royal",   "akkadian", "neo-assyrian",    "royal"),
    ("akk_na_admin",   "akkadian", "neo-assyrian",    "administrative"),
]

import re
LINENO_RE = re.compile(r"^\s*\[?\d+'?\.\]?\s*")


def clean_token(tok: str) -> str | None:
    t = tok.strip("[]<>()").rstrip("#?!")
    if not t: return None
    if re.match(r"^[\.,;:\-\[\]\(\)\?<>!]+$", t): return None
    return t


def extract_signs_from_line(line: str) -> list[str]:
    line = LINENO_RE.sub("", line)
    out = []
    for tok in line.split():
        c = clean_token(tok)
        if c: out.append(c)
    return out


def load_genre_buckets() -> dict[int, str]:
    """id_text(int) -> bucket name. First-match wins."""
    if not CDLI_CAT.exists(): return {}
    text_to_bucket: dict[int, str] = {}
    with CDLI_CAT.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        r = csv.DictReader(fh)
        for row in r:
            id_raw = (row.get("id_text") or "").strip()
            if not id_raw or not id_raw.isdigit(): continue
            id_int = int(id_raw)
            language = (row.get("language") or "").strip().lower()
            period = (row.get("period") or "").strip().lower()
            genre = (row.get("genre") or "").strip().lower()
            for name, lang_sub, period_sub, genre_sub in GENRE_BUCKETS:
                if (lang_sub in language and period_sub in period
                    and genre_sub in genre):
                    if id_int not in text_to_bucket:
                        text_to_bucket[id_int] = name
                    break
    return text_to_bucket


def stream_atf_for_buckets(text_to_bucket: dict[int, str],
                           per_bucket_cap: int = 5000) -> dict[str, list[list[str]]]:
    """Return name -> list of (per-text sign sequences). Cap per bucket to
    avoid massive runtime for the large admin buckets."""
    if not CDLI_ATF.exists(): return {}
    out: dict[str, list[list[str]]] = defaultdict(list)
    cur_id = None
    cur_bucket = None
    cur_signs: list[str] = []
    counts: dict[str, int] = defaultdict(int)
    with CDLI_ATF.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("&"):
                # finalize prev
                if cur_id is not None and cur_bucket is not None and cur_signs:
                    if counts[cur_bucket] < per_bucket_cap:
                        out[cur_bucket].append(cur_signs)
                        counts[cur_bucket] += 1
                cur_signs = []
                m = re.match(r"^&P0*(\d+)", line)
                if m:
                    iid = int(m.group(1))
                    cur_id = iid
                    cur_bucket = text_to_bucket.get(iid)
                else:
                    cur_id = None
                    cur_bucket = None
                continue
            if cur_bucket is None: continue
            if not line.strip(): continue
            if line.startswith(("#", "$", "@", ">>", "?")): continue
            cur_signs.extend(extract_signs_from_line(line))
        # final
        if cur_id is not None and cur_bucket is not None and cur_signs:
            if counts[cur_bucket] < per_bucket_cap:
                out[cur_bucket].append(cur_signs)
    return out


# ---------------------------------------------------------------------------
# [D] CM YAML projection against M77
# ---------------------------------------------------------------------------

def project_m77_with_cm(m77_dofs: dict, raw_dofs: dict) -> dict:
    """Re-run the multi-hypothesis ranker including the new CM YAML."""
    measured_vars = lambda d: {k: d[k] for k in (
        "zipf_alpha", "zipf_r2", "mi_gamma", "mi_r2_pow",
        "epistatic_2nd_norm", "epistatic_3rd_norm", "h1_norm", "h1_nats"
    ) if d[k] == d[k]}

    def project(measured):
        projs = []
        for fname in ALL_YAMLS:
            p = CAS_DIR / fname
            if not p.exists(): continue
            ydata = parse_yaml_constraints(p)
            projs.append(project_hypothesis(ydata, measured))
        ranked = sorted(projs, key=lambda p: (p["max_violation"], -1 * (p.get("score_value") or 0)))
        return [{"rank": i, "model_id": p["model_id"],
                 "max_violation": p["max_violation"],
                 "n_violations": p["n_violations"],
                 "score_value": p["score_value"]}
                for i, p in enumerate(ranked, 1)]

    return {"m77_mapped_with_cm": project(measured_vars(m77_dofs)),
            "m77_raw_with_cm":    project(measured_vars(raw_dofs))}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("Phase-19 follow-up (A/D/K) starting", file=sys.stderr)
    results = {}

    # [A] Joint sign clustering
    print("\n=== [A] Sign clustering: M77 + CISI mayig ===", file=sys.stderr)
    m77_ins = load_inscriptions(ROOT / "reports/mahadevan_corpus_flat.txt")
    raw_ins = load_inscriptions(ROOT / "backend/glossa_lab/data/phase19_corpora/m77_raw_glyphs_signs.txt")
    cisi_ins = load_inscriptions(ROOT / "backend/glossa_lab/data/phase18_corpora/cisi_mayig_signs.txt")

    m77_clust = cluster_corpus("indus_m77_mapped", m77_ins, min_count=5)
    print(f"  M77 mapped: {m77_clust['n_signs_total']} signs total, "
          f"{m77_clust['n_clusters']} clusters, "
          f"biggest: {m77_clust['biggest_cluster']['size'] if m77_clust['biggest_cluster'] else 0}",
          file=sys.stderr)
    raw_clust = cluster_corpus("indus_m77_raw", raw_ins, min_count=3)
    print(f"  M77 raw: {raw_clust['n_signs_total']} signs total, "
          f"{raw_clust['n_clusters']} clusters", file=sys.stderr)
    cisi_clust = cluster_corpus("cisi_mayig", cisi_ins, min_count=2)
    print(f"  CISI: {cisi_clust['n_signs_total']} signs total, "
          f"{cisi_clust['n_clusters']} clusters", file=sys.stderr)
    results["sign_clusters"] = {
        "m77_mapped": m77_clust,
        "m77_raw": raw_clust,
        "cisi_mayig": cisi_clust,
    }

    # [K] Genre-stratified CDLI
    print("\n=== [K] Genre-stratified CDLI ===", file=sys.stderr)
    text_to_bucket = load_genre_buckets()
    bucket_counts = Counter(text_to_bucket.values())
    for n, c in bucket_counts.most_common():
        print(f"  {n:18s} {c} texts in catalog", file=sys.stderr)

    print("  Streaming ATF (per_bucket_cap=5000) ...", file=sys.stderr)
    bucket_data = stream_atf_for_buckets(text_to_bucket, per_bucket_cap=5000)
    genre_results = {}
    for name, _, _, _ in GENRE_BUCKETS:
        ins_list = bucket_data.get(name, [])
        flat = [t for ins in ins_list for t in ins]
        if len(flat) < 1000:
            print(f"  {name}: only {len(flat)} signs, skipping", file=sys.stderr)
            continue
        r = measure_corpus(name, flat, note=f"CDLI genre-stratified {name}")
        genre_results[name] = r
        print(f"  {name:18s} n_text={len(ins_list):>5} n={r['n_tokens']:>7} V={r['n_types']:>6} "
              f"zipf_a={r['zipf_alpha']:>6} eps3={r['epistatic_3rd_norm']:>5} "
              f"h1n={r['h1_norm']:>5}", file=sys.stderr)
    results["genre_stratified_cdli"] = genre_results

    # [D] CM YAML projection
    print("\n=== [D] M77 vs all 6 hypotheses (incl Cypro-Minoan) ===", file=sys.stderr)
    m77_flat = [t for ins in m77_ins for t in ins]
    m77_dofs = measure_corpus("indus_m77", m77_flat)
    raw_flat = [t for ins in raw_ins for t in ins]
    raw_dofs = measure_corpus("indus_m77_raw", raw_flat) if raw_flat else m77_dofs
    cm_proj = project_m77_with_cm(m77_dofs, raw_dofs)
    print("  M77 (mapped) ranking with CM:", file=sys.stderr)
    for r in cm_proj["m77_mapped_with_cm"]:
        print(f"    {r['rank']}. {r['model_id']:34s}  max_v={r['max_violation']}  "
              f"n_viol={r['n_violations']}  score={r['score_value']}", file=sys.stderr)
    print("  M77 (raw) ranking with CM:", file=sys.stderr)
    for r in cm_proj["m77_raw_with_cm"]:
        print(f"    {r['rank']}. {r['model_id']:34s}  max_v={r['max_violation']}  "
              f"n_viol={r['n_violations']}  score={r['score_value']}", file=sys.stderr)
    results["cm_projection"] = cm_proj

    # Output
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump({"phase": "phase19", "results": results}, fh, indent=2)
    print(f"\nWrote {OUT_JSON}", file=sys.stderr)
    write_md(results)
    print(f"Wrote {OUT_MD}", file=sys.stderr)
    return 0


def write_md(results: dict):
    lines = []
    lines.append("# Phase-19 follow-up — A (sign clustering) + K (genre CDLI) + D (Cypro-Minoan)\n")
    lines.append("## [A] Sign clustering on M77 (mapped + raw) + CISI mayig\n")
    lines.append("| corpus | n_signs_total | n_eligible | n_clusters | n_signs_in_multi_clusters |")
    lines.append("|---|---:|---:|---:|---:|")
    for k in ["m77_mapped", "m77_raw", "cisi_mayig"]:
        c = results["sign_clusters"][k]
        lines.append(f"| {k} | {c['n_signs_total']} | {c['n_signs_eligible']} | "
                     f"{c['n_clusters']} | {c['n_signs_in_multi_clusters']} |")
    lines.append("")
    lines.append("Top 5 M77-mapped clusters (size, members):\n")
    for c in (results["sign_clusters"]["m77_mapped"]["all_clusters"] or [])[:5]:
        lines.append(f"- size={c['size']}: `{', '.join(c['members'])}`")
    lines.append("")
    lines.append("## [K] Genre-stratified CDLI baselines\n")
    lines.append("New per-genre Sumerian/Akkadian DoF measurements. Compare these to M77\n"
                 "to see if a *specific* genre is structurally closer than the raw\n"
                 "language baseline.\n")
    lines.append("| bucket | n_tokens | V | zipf_a | mi_gamma | eps2 | eps3 | h1_norm |")
    lines.append("|---|---:|---:|---|---|---|---|---|")
    for name, r in (results.get("genre_stratified_cdli") or {}).items():
        lines.append(f"| {name} | {r['n_tokens']} | {r['n_types']} | "
                     f"{r['zipf_alpha']} | {r['mi_gamma']} | "
                     f"{r['epistatic_2nd_norm']} | {r['epistatic_3rd_norm']} | "
                     f"{r['h1_norm']} |")
    lines.append("\n*M77 reference: zipf_a=0.978, mi_gamma=0.098, eps2=0.597, eps3=0.422, h1_norm=0.897*\n")
    lines.append("## [D] M77 vs all 6 hypotheses (incl Cypro-Minoan typological control)\n")
    lines.append("### M77 (rank-corr-mapped) ranking\n")
    lines.append("| rank | hypothesis | max_v | n_viol | score |")
    lines.append("|---|---|---|---|---|")
    for r in results["cm_projection"]["m77_mapped_with_cm"]:
        lines.append(f"| {r['rank']} | `{r['model_id']}` | {r['max_violation']} | "
                     f"{r['n_violations']} | {r['score_value']} |")
    lines.append("")
    lines.append("### M77 (raw OCR glyphs) ranking\n")
    lines.append("| rank | hypothesis | max_v | n_viol | score |")
    lines.append("|---|---|---|---|---|")
    for r in results["cm_projection"]["m77_raw_with_cm"]:
        lines.append(f"| {r['rank']} | `{r['model_id']}` | {r['max_violation']} | "
                     f"{r['n_violations']} | {r['score_value']} |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
