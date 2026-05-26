"""Generate comparison report: IVS metrics vs Sproat 2014 non-linguistic systems.

Produces CSV + Markdown report in outputs/benchmarks/.
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
BENCH_DIR = pathlib.Path(__file__).resolve().parent
OUT_DIR = ROOT / "outputs" / "benchmarks"


def run():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- Compute IVS metrics ---
    from run_entropy_metrics import compute_all as compute_entropy
    from run_repetition_metrics import load_ivs_sequences, repetition_rate

    ivs_entropy = compute_entropy()
    seqs = load_ivs_sequences()
    ivs_rep = repetition_rate(seqs)

    # --- Load Sproat reference stats ---
    ref_path = BENCH_DIR / "sproat_2014_reference_stats.json"
    ref = json.loads(ref_path.read_text(encoding="utf-8"))

    # --- Build comparison table ---
    rows = []
    # IVS row
    rows.append({
        "System": "Indus Valley Script (IVS)",
        "Type": "unknown (tested)",
        "N_Texts": ivs_entropy["n_texts"],
        "N_Tokens": ivs_entropy["n_tokens"],
        "N_Types": ivs_entropy["n_types"],
        "Mean_Text_Length": ivs_entropy["mean_text_length"],
        "H0_Unigram": ivs_entropy["H0_unigram_entropy"],
        "H1_Conditional": ivs_entropy["H1_conditional_entropy"],
        "Zipf_Slope": ivs_entropy["zipf_slope"],
        "r_over_R": ivs_rep["r_over_R"],
    })

    # Non-linguistic rows (from Sproat 2014 published stats)
    for sys in ref["non_linguistic"]:
        rows.append({
            "System": sys["system"],
            "Type": "non_linguistic",
            "N_Texts": sys["n_texts"],
            "N_Tokens": sys["n_tokens"],
            "N_Types": sys["n_types"],
            "Mean_Text_Length": sys["mean_text_length"],
            "H0_Unigram": "",
            "H1_Conditional": "",
            "Zipf_Slope": "",
            "r_over_R": sys.get("r_over_R", ""),
        })

    # Linguistic reference rows
    for sys in ref["linguistic_reference"]:
        rows.append({
            "System": sys["system"],
            "Type": "linguistic",
            "N_Texts": "",
            "N_Tokens": "",
            "N_Types": "",
            "Mean_Text_Length": "",
            "H0_Unigram": "",
            "H1_Conditional": "",
            "Zipf_Slope": "",
            "r_over_R": sys.get("r_over_R", ""),
        })

    # --- Write CSV ---
    csv_path = OUT_DIR / "sproat_comparison_report.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"[CSV] {csv_path}")

    # --- Write Markdown ---
    md_path = OUT_DIR / "sproat_comparison_report.md"
    lines = [
        "# IVS vs Non-Linguistic Systems: Sproat 2014 Benchmark Comparison",
        "",
        "## Purpose",
        "",
        "This report compares IVS statistical metrics against Sproat's (2014)",
        "non-linguistic symbol system benchmarks. Per Sproat 2014, conditional",
        "entropy alone does not distinguish writing from structured non-linguistic",
        "systems. The r/R repetition rate is the cleanest discriminator.",
        "",
        "## IVS Metrics",
        "",
        f"- **H0 (unigram entropy)**: {ivs_entropy['H0_unigram_entropy']} bits",
        f"- **H1 (conditional entropy)**: {ivs_entropy['H1_conditional_entropy']} bits",
        f"- **Zipf slope**: {ivs_entropy['zipf_slope']}",
        f"- **r/R repetition rate**: {ivs_rep['r_over_R']}",
        f"- **Corpus**: {ivs_entropy['n_texts']} inscriptions, "
        f"{ivs_entropy['n_tokens']} tokens, {ivs_entropy['n_types']} types",
        "",
        "## r/R Comparison (Sproat's discriminator)",
        "",
        "| System | Type | r/R |",
        "|--------|------|-----|",
    ]

    for row in rows:
        rr = row["r_over_R"]
        if rr != "":
            lines.append(f"| {row['System']} | {row['Type']} | {rr} |")

    lines.extend([
        "",
        "## Interpretation",
        "",
        "Linguistic systems typically have r/R < 0.10; non-linguistic systems",
        "typically have r/R > 0.50 (Sproat 2014). IVS r/R should be evaluated",
        "against these thresholds. However, r/R is partially confounded with",
        "text length — non-linguistic texts tend to be shorter.",
        "",
        "**Key finding from Sproat 2014**: Neither conditional entropy (Rao et al.)",
        "nor Lee et al.'s Cr measure at published settings reliably separates",
        "linguistic from non-linguistic systems. The manuscript should not treat",
        "conditional entropy as proof of linguistic status.",
        "",
        "## References",
        "",
        "- Sproat, R. (2014). A statistical comparison of written language and",
        "  nonlinguistic symbol systems. *Language*, 90(2), 457-481.",
        "- Sproat, R. (2023). *Symbols: An Evolutionary History from the Stone Age",
        "  to the Future*. Springer.",
    ])

    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[MD]  {md_path}")

    # --- Save combined JSON ---
    combined = {
        "ivs": {**ivs_entropy, **ivs_rep},
        "sproat_reference": ref,
        "interpretation": (
            "IVS conditional entropy and r/R should be compared against "
            "both linguistic and non-linguistic reference systems. "
            "Conditional entropy alone is not a sufficient discriminator "
            "(Sproat 2014)."
        ),
    }
    json_path = OUT_DIR / "sproat_comparison_report.json"
    json_path.write_text(json.dumps(combined, indent=2), encoding="utf-8")
    print(f"[JSON] {json_path}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(BENCH_DIR))
    run()
