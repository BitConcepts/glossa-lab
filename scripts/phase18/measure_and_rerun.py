"""Phase-18: comprehensive language-signature measurement on ALL corpora,
+ updated M77 multi-hypothesis projection with the new running-Sanskrit baseline.

This re-runs Phase-16/17 measurements with two crucial additions:
 1. RV padapatha (running Sanskrit, not bag-of-words). This re-grounds the
    indo_aryan_morphology hypothesis against genuine running Sanskrit instead
    of the artefactual Kalyanaraman BoW.
 2. mayig CISI Parpola sign sequences (Mohenjo-daro subset only, 179
    inscriptions, 1003 signs). Comparator for M77 sign distributions.

Outputs:
 backend/glossa_lab/data/phase18_corpora/phase18_all_dofs.json
 backend/glossa_lab/data/phase18_corpora/phase18_all_dofs.csv
 reports/phase18_indus_grounded_rerun.json
"""
from __future__ import annotations

import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_P16 = ROOT / "scripts" / "phase16"
sys.path.insert(0, str(SCRIPTS_P16))
from measure_signature_dofs import measure_corpus  # type: ignore
from rerun_indus_grounded import (  # type: ignore
    parse_yaml_constraints, project_hypothesis,
)

CORPORA: list[tuple[str, Path]] = [
    # Phase-16 cuneiform (existing)
    ("cdli_sumerian_ur3",   ROOT / "backend/glossa_lab/data/phase16_corpora/cdli_sumerian_ur3_seqs.csv"),
    ("cdli_sumerian_ob_lit", ROOT / "backend/glossa_lab/data/phase16_corpora/cdli_sumerian_ob_lit_seqs.csv"),
    ("cdli_akkadian_ob",    ROOT / "backend/glossa_lab/data/phase16_corpora/cdli_akkadian_ob_seqs.csv"),
    ("cdli_akkadian_na",    ROOT / "backend/glossa_lab/data/phase16_corpora/cdli_akkadian_na_seqs.csv"),
    ("kee2u_tamil",         ROOT / "backend/glossa_lab/data/phase16_corpora/kee2u_tamil_morpheme_seqs.csv"),
    ("kalyanaraman_vedic",  ROOT / "backend/glossa_lab/data/phase16_corpora/kalyanaraman_devanagari_corpus.txt"),
    # Phase-17 Linear B
    ("damos_linear_b",      ROOT / "backend/glossa_lab/data/phase17_corpora/damos_signs.txt"),
    # Phase-18 NEW running Sanskrit + CISI
    ("rv_padapatha",        ROOT / "backend/glossa_lab/data/phase18_corpora/rv_padapatha_stream.txt"),
    ("cisi_mayig",          ROOT / "backend/glossa_lab/data/phase18_corpora/cisi_mayig_signs.txt"),
    # And Indus M77 itself
    ("indus_m77",           ROOT / "reports/mahadevan_corpus_flat.txt"),
]

CAS_DIR = ROOT / "backend/glossa_lab/data/cas_models"
CAS_YAMLS = [
    "dravidian_morphology.yaml",
    "indo_aryan_morphology.yaml",
    "sumerian_morphology.yaml",
    "akkadian_morphology.yaml",
    "vedic_kalyanaraman_morphology.yaml",
]

OUT_DIR = ROOT / "backend/glossa_lab/data/phase18_corpora"
OUT_JSON = OUT_DIR / "phase18_all_dofs.json"
OUT_CSV = OUT_DIR / "phase18_all_dofs.csv"
RERUN_JSON = ROOT / "reports/phase18_indus_grounded_rerun.json"


def load_seq(name: str, path: Path) -> list[str]:
    """Load any of: csv with `signs_ws_joined`/`morpheme_ids_ws_joined`/`padapatha_words_ws_joined`,
    or plain text whitespace-separated."""
    if not path.exists():
        return []
    if path.suffix.lower() == ".csv":
        out: list[str] = []
        with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
            r = csv.DictReader(fh)
            cols_to_try = ["signs_ws_joined", "morpheme_ids_ws_joined",
                           "padapatha_words_ws_joined"]
            for row in r:
                for c in cols_to_try:
                    val = (row.get(c) or "").strip()
                    if val:
                        out.extend(val.split())
                        break
        return out
    # else: plain text
    seq: list[str] = []
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            seq.extend(line.strip().split())
    return seq


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RERUN_JSON.parent.mkdir(parents=True, exist_ok=True)

    print("Phase-18 measurement", file=sys.stderr)
    results: list[dict] = []
    for name, path in CORPORA:
        seq = load_seq(name, path)
        if not seq:
            print(f"  {name}: SKIP (empty / not found at {path})", file=sys.stderr)
            continue
        r = measure_corpus(name, seq, note=f"path={path.relative_to(ROOT)}")
        print(f"  {name:24s} n={r['n_tokens']:>7} V={r['n_types']:>6} "
              f"zipf_alpha={r['zipf_alpha']:>6} mi_gamma={r['mi_gamma']:>6} "
              f"eps2={r['epistatic_2nd_norm']:>5} eps3={r['epistatic_3rd_norm']:>5} "
              f"h1n={r['h1_norm']:>5}", file=sys.stderr)
        results.append(r)

    with OUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump({"phase": "phase18", "results": results}, fh, indent=2)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        if results:
            w = csv.DictWriter(fh, fieldnames=list(results[0].keys()))
            w.writeheader()
            for r in results:
                w.writerow(r)
    print(f"\nWrote {OUT_JSON} and {OUT_CSV}", file=sys.stderr)

    # M77 multi-hypothesis projection (with current grounded YAMLs)
    m77 = next((r for r in results if r["name"] == "indus_m77"), None)
    if m77 is None:
        print("\nNo M77 measurement; skipping projection", file=sys.stderr)
        return 0

    measured_vars = {k: m77[k] for k in (
        "zipf_alpha", "zipf_r2", "mi_gamma", "mi_r2_pow",
        "epistatic_2nd_norm", "epistatic_3rd_norm", "h1_norm", "h1_nats"
    ) if m77[k] == m77[k]}

    print("\nProjecting M77 through 5 CAS-YAMLs ...", file=sys.stderr)
    projections = []
    for fname in CAS_YAMLS:
        p = CAS_DIR / fname
        if not p.exists():
            continue
        yaml_data = parse_yaml_constraints(p)
        proj = project_hypothesis(yaml_data, measured_vars)
        projections.append(proj)
        score = proj["score_value"]
        print(f"  {proj['model_id']:32s}  max_violation={proj['max_violation']:.4f}  "
              f"n_violated={proj['n_violations']}  score={score}", file=sys.stderr)

    ranked = sorted(projections, key=lambda p: (p["max_violation"], -1 * (p.get("score_value") or 0)))
    print("\n=== Phase-18 M77 ranking (lower max_violation = better) ===", file=sys.stderr)
    for i, p in enumerate(ranked, 1):
        print(f"  {i}. {p['model_id']:32s}  max_v={p['max_violation']:.4f}  "
              f"score={p['score_value']}", file=sys.stderr)

    out = {
        "phase": "phase18",
        "purpose": "M77 multi-hypothesis projection with Phase-18 corpora context",
        "m77_measured": m77,
        "ranked_hypotheses": [
            {"rank": i, "model_id": p["model_id"],
             "max_violation": p["max_violation"], "n_violations": p["n_violations"],
             "score_value": p["score_value"]}
            for i, p in enumerate(ranked, 1)
        ],
        "details": projections,
        "all_corpora_dofs": results,
    }
    with RERUN_JSON.open("w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nWrote {RERUN_JSON}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
