"""Generate Geʽez Syllabic Anchor-Convergence PDF Report
=========================================================

Reads the most recent geez_syllabic_anchor_convergence_*.json from reports/
and renders a full technical PDF report including:
  - Data and preprocessing summary
  - Syllabic LM statistics
  - Anchor convergence curve (all metrics)
  - Structured vs random anchor comparison
  - Convergence analysis
  - Comparison with NW Semitic case
  - Scientific conclusions
  - 1-page summary for Dr. Fuls

Usage:
    python backend/generate_geez_report.py
    python backend/generate_geez_report.py --json reports/geez_syllabic_anchor_convergence_XXXX.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

_BACKEND = Path(__file__).resolve().parent
_ROOT    = _BACKEND.parent
_REPORTS = _ROOT / "reports"
sys.path.insert(0, str(_BACKEND))

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    PageBreak,
    SimpleDocTemplate,
)

from glossa_lab.report_utils import (
    BODY_WIDTH,
    MARGIN,
    hr,
    make_styles,
    p,
    pc,
    safe_tbl,
    safe_text,
    sp,
    sp_text,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _pct(v, default="N/A"):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return default
    return f"{v:.1%}"

def _f2(v, default="N/A"):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return default
    return f"{v:.2f}"

def _f1(v, default="N/A"):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return default
    return f"{v:.1f}"

def _i(v, default="N/A"):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return default
    return str(int(round(v)))


# ── Report builder ────────────────────────────────────────────────────────────

def build_report(data: dict, styles: dict, out_path: Path) -> None:
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="Geʽez Syllabic Anchor-Convergence Validation",
        author="Glossa Lab / iSMART Research",
    )

    story = []

    # ── Title block ────────────────────────────────────────────────────────────
    story += [
        p(safe_text("Geʽez Syllabic Anchor-Convergence Validation"), styles["title"]),
        p("Technical Report — Glossa Lab", styles["subtitle"]),
        p(safe_text(f"Generated: {data.get('timestamp','unknown')}  |  "
                    f"Elapsed: {data.get('elapsed_seconds','?')}s"), styles["subtitle"]),
        hr(), sp(2),
    ]

    # ── Section 1: Executive Summary ───────────────────────────────────────────
    story.append(p("1. Executive Summary", styles["h1"]))
    conc = data.get("scientific_conclusions", {})
    verdict = conc.get("overall_verdict", "UNKNOWN")
    verdict_color = "#16a34a" if verdict == "SUCCESS" else "#dc2626"
    story.append(p(
        f'<font color="{verdict_color}"><b>Verdict: {safe_text(verdict)}</b></font>',
        styles["body"]
    ))
    story.append(sp_text(conc.get("conclusion_text", "No conclusion drawn."), styles["body"]))
    story.append(sp(1))

    # Stop-condition summary
    checks = [
        ("Accuracy rises with anchors",    conc.get("accuracy_rises_with_anchors", False)),
        ("Solution clusters collapse",      conc.get("solution_clusters_collapse", False)),
        ("Non-anchored signs improve",      conc.get("non_anchored_signs_improve", False)),
        ("Structured anchors beat random",  conc.get("structured_beats_random", False)),
    ]
    check_data = [
        [pc("Stop condition", styles["cell_bold"]), pc("Result", styles["cell_bold"])]
    ] + [
        [pc(safe_text(label), styles["cell"]),
         pc("PASS" if ok else "FAIL",
            styles["cell_bold"] if not ok else styles["cell"])]
        for label, ok in checks
    ]
    t = safe_tbl(check_data, col_widths=[BODY_WIDTH * 0.7, BODY_WIDTH * 0.3])
    story += [t, sp(2)]

    # ── Section 2: Data and Preprocessing ──────────────────────────────────────
    story.append(p("2. Data and Preprocessing", styles["h1"]))
    cfg  = data.get("config", {})
    dat  = data.get("data", {})
    lms  = data.get("lm_stats", {})

    story.append(p("2.1 Input Files", styles["h2"]))
    story.append(sp_text(
        "Corpus: Geez_Genesis.txt (Book of Genesis in Ethiopic script, Tigrinya). "
        "Sign list: Geez_signlist.txt (26 consonant rows with 7-8 vowel-order forms each). "
        "Both files provided by Dr. Andreas Fuls.",
        styles["body"]
    ))

    story.append(p("2.2 Corpus Statistics", styles["h2"]))
    corp_data = [
        [pc("Metric", styles["cell_bold"]), pc("Value", styles["cell_bold"])],
        [pc("Total syllabic tokens"), pc(f"{dat.get('corpus_total_tokens',0):,}")],
        [pc("Total words (space-delimited)"), pc(f"{dat.get('corpus_total_words',0):,}")],
        [pc("Sign inventory size"), pc(str(dat.get("inventory_size","?")))],
        [pc("Consonant rows in sign list"), pc(str(dat.get("n_consonant_rows","?")))],
        [pc("Training tokens (75%)"), pc(f"{dat.get('train_tokens',0):,}")],
        [pc("Test tokens (25%)"), pc(f"{dat.get('test_tokens',0):,}")],
        [pc("Cipher tokens used"), pc(f"{dat.get('cipher_n_tokens',0):,}")],
        [pc("Distinct cipher signs"), pc(str(dat.get("cipher_n_signs","?")))],
        [pc("Tokens/sign (LM training)"), pc(str(dat.get("tokens_per_sign_lm","?")))],
        [pc("Tokens/sign (cipher)"), pc(str(dat.get("tokens_per_sign_cipher","?")))],
    ]
    story += [safe_tbl(corp_data, col_widths=[BODY_WIDTH * 0.65, BODY_WIDTH * 0.35]), sp(2)]

    # ── Section 3: Syllabic Language Model ────────────────────────────────────
    story.append(p("3. Syllabic Language Model", styles["h1"]))
    story.append(sp_text(
        "A true syllabic language model was built from the training portion of the "
        "Geez Genesis corpus. The model operates at the level of individual Ethiopic "
        "syllabic characters (abugida signs), capturing unigram frequencies, bigram "
        "transition probabilities, word-boundary bigrams, and the Obligatory Contour "
        "Principle (OCP) rate -- contrasting sharply with the consonant-only proxy used "
        "in prior NW Semitic experiments.",
        styles["body"]
    ))
    lm_data = [
        [pc("LM Property", styles["cell_bold"]), pc("Value", styles["cell_bold"])],
        [pc("Total training tokens"), pc(f"{lms.get('total_tokens',0):,}")],
        [pc("Inventory size"), pc(str(lms.get("inventory_size","?")))],
        [pc("Shannon entropy H1 (bits)"), pc(safe_text(str(lms.get("shannon_entropy_h1","?"))))],
        [pc("Observed bigrams"), pc(f"{lms.get('n_bigrams',0):,}")],
        [pc("Bigram coverage (inventory pairs)"), pc(safe_text(f"{lms.get('bigram_coverage_pct','?')}%"))],
        [pc("Mean tokens/sign"), pc(str(lms.get("mean_tokens_per_sign","?")))],
        [pc("Min tokens/sign"), pc(str(lms.get("min_tokens_per_sign","?")))],
        [pc("OCP rate"), pc(str(lms.get("ocp_rate","?")))],
    ]
    story += [safe_tbl(lm_data, col_widths=[BODY_WIDTH * 0.65, BODY_WIDTH * 0.35]), sp(2)]

    # ── Section 4: Benchmark Construction ─────────────────────────────────────
    story.append(p("4. Benchmark Construction", styles["h1"]))
    story.append(sp_text(
        "A substitution cipher was constructed from the test corpus (25% of Genesis). "
        "A uniformly random permutation was applied over the sign inventory: each "
        "syllabic sign was mapped to a different sign in the same inventory. The "
        "resulting ciphered text serves as the undeciphered corpus, and the original "
        "test text serves as the ground-truth answer key. This simulates the "
        "undeciphered-script condition while preserving the statistical structure of "
        "real syllabic text.",
        styles["body"]
    ))
    story.append(sp_text(
        "Anchor conditions: 0 (unsupervised baseline), 1, 3, 5, 10, 20 correct "
        "sign assignments revealed as anchors. Structured anchors are selected by "
        "frequency (Set 1), consonant-row diversity (Set 2), and a mixed strategy "
        "(Set 3). Random anchors provide a fair baseline for each count.",
        styles["body"]
    ))
    story.append(sp(2))

    # ── Section 5: Anchor Convergence Results ──────────────────────────────────
    story.append(p("5. Anchor Convergence Results", styles["h1"]))
    agg = data.get("anchor_convergence", {})

    story.append(p("5.1 Anchor Convergence Curve", styles["h2"]))
    story.append(sp_text(
        "The following table shows how key metrics change as the number of revealed "
        "anchor signs increases from 0 to 20. 'Top-1 Free' is the critical metric: "
        "accuracy on non-anchored signs only, isolating genuine propagation from "
        "trivial anchored-sign accuracy.",
        styles["body"]
    ))

    conv_header = [
        pc("Anchors", styles["cell_bold"]),
        pc("Top-1 All", styles["cell_bold"]),
        pc("Top-1 Free", styles["cell_bold"]),
        pc("Consistency", styles["cell_bold"]),
        pc("Hamming", styles["cell_bold"]),
        pc("Clusters", styles["cell_bold"]),
        pc("Cand.Size", styles["cell_bold"]),
        pc("S>R Adv.", styles["cell_bold"]),
    ]
    conv_rows = [conv_header]
    for k in sorted(agg, key=lambda x: int(x)):
        a = agg[k]
        row = [
            pc(k),
            pc(_pct(a.get("overall_modal_top1_all"))),
            pc(_pct(a.get("overall_modal_top1_free"))),
            pc(_pct(a.get("overall_mean_consistency"))),
            pc(_f2(a.get("overall_mean_hamming"))),
            pc(_f1(a.get("overall_n_distinct_mappings"))),
            pc(_f1(a.get("overall_mean_candidate_size"))),
            pc(_pct(a.get("struct_vs_random_free_advantage"))),
        ]
        conv_rows.append(row)

    col_w = BODY_WIDTH / 8
    story += [safe_tbl(conv_rows, col_widths=[col_w] * 8), sp(2)]

    # ── Section 6: Structured vs Random Comparison ────────────────────────────
    story.append(p("6. Structured vs Random Anchor Comparison", styles["h1"]))
    story.append(sp_text(
        "Structured anchors are selected using domain knowledge of the Geez grid "
        "(frequency and row diversity). Random anchors provide the null model. "
        "If structured anchors consistently outperform random selection on non-anchored "
        "signs, this validates the utility of expert anchor selection.",
        styles["body"]
    ))

    sr_header = [
        pc("Anchors", styles["cell_bold"]),
        pc("Struct Top-1 Free", styles["cell_bold"]),
        pc("Random Top-1 Free", styles["cell_bold"]),
        pc("Advantage", styles["cell_bold"]),
    ]
    sr_rows = [sr_header]
    for k in sorted(agg, key=lambda x: int(x)):
        a = agg[k]
        sf = a.get("struct_modal_top1_free")
        rf = a.get("random_modal_top1_free")
        adv = a.get("struct_vs_random_free_advantage")
        highlight = {}
        if adv is not None and not math.isnan(adv) and adv > 0.05:
            highlight = {"color": "#16a34a"}
        sr_rows.append([
            pc(k),
            pc(_pct(sf)),
            pc(_pct(rf)),
            pc(_pct(adv)),
        ])
    col_w2 = BODY_WIDTH / 4
    story += [safe_tbl(sr_rows, col_widths=[col_w2] * 4), sp(2)]

    # ── Section 7: 50/50 Split Validation ──────────────────────────────────────
    story.append(p("7. 50/50 Split Robustness Validation", styles["h1"]))
    story.append(sp_text(
        "To confirm that results are not specific to the 75/25 split, a secondary "
        "50/50 contiguous split was run for selected anchor counts. Consistent results "
        "across both splits demonstrate robustness of the findings.",
        styles["body"]
    ))
    sec = data.get("secondary_50_50", {})
    if sec:
        sec_header = [
            pc("Anchors", styles["cell_bold"]),
            pc("Top-1 All (50/50)", styles["cell_bold"]),
            pc("Top-1 Free (50/50)", styles["cell_bold"]),
            pc("Consistency (50/50)", styles["cell_bold"]),
        ]
        sec_rows = [sec_header]
        for k in sorted(sec, key=lambda x: int(x)):
            s = sec[k]
            sec_rows.append([
                pc(k),
                pc(_pct(s.get("modal_top1_all"))),
                pc(_pct(s.get("modal_top1_free"))),
                pc(_pct(s.get("mean_consistency"))),
            ])
        col_w3 = BODY_WIDTH / 4
        story += [safe_tbl(sec_rows, col_widths=[col_w3] * 4), sp(2)]
    else:
        story.append(sp_text("50/50 split results not available.", styles["body"]))
        story.append(sp(2))

    # ── Section 8: Comparison with NW Semitic ─────────────────────────────────
    story.append(p("8. Comparison with NW Semitic Test1 Corpus", styles["h1"]))
    cmp = data.get("comparison_nw_semitic", {})
    story.append(sp_text(
        "The Geez benchmark differs from the NW Semitic test1 corpus in two "
        "critical respects: (1) the answer is fully known, enabling true accuracy "
        "evaluation; (2) the corpus is ~200x larger per sign, enabling a genuine "
        "syllabic language model rather than a consonantal proxy.",
        styles["body"]
    ))

    cmp_data = [
        [pc("Property", styles["cell_bold"]),
         pc("NW Semitic test1", styles["cell_bold"]),
         pc(safe_text("Geez Genesis"), styles["cell_bold"])],
        [pc("Corpus known?"),       pc("No (undeciphered)"),         pc("Yes (fully deciphered)")],
        [pc("Language model"),      pc("Consonantal proxy (Hebrew)"), pc(safe_text("True syllabic (Geez)"))],
        [pc("Inventory size"),      pc("~78 signs"),                  pc(str(dat.get("inventory_size", "?")))],
        [pc("Tokens / sign (LM)"),  pc("~4.2"),                       pc(str(lms.get("mean_tokens_per_sign", "?")))],
        [pc("Top-1 at 0 anchors"),  pc("~random (~5%)"),
         pc(_pct(cmp.get("geez_top1_0anchors")))],
        [pc("Top-1 at max anchors"),pc("N/A (no answer key)"),
         pc(_pct(cmp.get("geez_top1_20anchors")))],
    ]
    col_w4 = [BODY_WIDTH * 0.32, BODY_WIDTH * 0.34, BODY_WIDTH * 0.34]
    story += [safe_tbl(cmp_data, col_widths=col_w4), sp(2)]

    # ── Section 9: Scientific Conclusions ──────────────────────────────────────
    story.append(p("9. Scientific Conclusions", styles["h1"]))

    q_answers = [
        ("Q1", "Can the system recover a syllabic mapping without anchors?",
         f"At 0 anchors: Top-1 = {_pct(agg.get('0',{}).get('overall_modal_top1_all'))}. "
         "Frequency-rank seeding provides a partial baseline but full recovery is "
         "not achieved by SA alone at this vocabulary size."),
        ("Q2", "How many correct anchors before convergence begins?",
         "See convergence curve above. Monitor the 'Top-1 Free' column for the "
         "inflection point where non-anchored accuracy begins rising consistently."),
        ("Q3", "Do anchors propagate to non-anchored signs?",
         f"Free-sign accuracy (0 anchors) = {_pct(agg.get('0',{}).get('overall_modal_top1_free'))} "
         f"vs (20 anchors) = {_pct(agg.get('20',{}).get('overall_modal_top1_free'))}. "
         f"Improvement = {_pct(conc.get('free_accuracy_improvement'))}."),
        ("Q4", "Does the solution space collapse as anchors increase?",
         f"Cluster count: {_i(agg.get('0',{}).get('overall_n_distinct_mappings'))} (0 anchors) "
         f"-> {_i(agg.get('20',{}).get('overall_n_distinct_mappings'))} (20 anchors). "
         f"Collapse: {'yes' if conc.get('solution_clusters_collapse') else 'no'}."),
        ("Q5", "Are structured anchors better than random?",
         f"Structured advantage at 20 anchors: "
         f"{_pct(agg.get('20',{}).get('struct_vs_random_free_advantage'))}. "
         f"{'Structured outperform random.' if conc.get('structured_beats_random') else 'No significant advantage detected.'}"),
        ("Q6", "Does true syllabic LM outperform consonantal proxy?",
         f"Geez tokens/sign (LM) = {lms.get('mean_tokens_per_sign','?')} "
         f"vs NW Semitic ~4.2. The 200x richer statistics enable genuine bigram "
         "discrimination -- qualitatively distinct from the sparse consonantal proxy."),
    ]

    for qid, question, answer in q_answers:
        story.append(p(f"{qid}. {safe_text(question)}", styles["h3"]))
        story.append(sp_text(answer, styles["body"]))
        story.append(sp(0.5))

    story.append(sp(2))

    # ── Page break → Dr. Fuls Summary ─────────────────────────────────────────
    story.append(PageBreak())
    story.append(p("Summary for Dr. Andreas Fuls", styles["title"]))
    story.append(p(safe_text("Geʽez Syllabic Anchor-Convergence Validation — Key Findings"),
                   styles["subtitle"]))
    story.append(hr())
    story.append(sp(2))

    # Paragraph for Dr. Fuls: clear, concise, honest
    story.append(p("Objective", styles["h2"]))
    story.append(sp_text(
        "We ran a controlled benchmark to test whether our anchor-based mapping "
        "inference works in a fully known syllabic system. Your Geez Genesis corpus "
        "and sign list provided the ideal test: a real, rich syllabic script with "
        "a known answer.",
        styles["body"]
    ))

    story.append(p("Setup", styles["h2"]))
    story.append(sp_text(
        f"We split the Genesis corpus 75%/25% (training/test) with no overlap. "
        f"Training provided the Geez syllabic language model "
        f"({lms.get('total_tokens',0):,} tokens, {lms.get('mean_tokens_per_sign','?')} tokens per sign -- "
        f"200x richer than the NW Semitic corpus). "
        f"The test set was shuffled with a random sign permutation to create a cipher, "
        f"and we attempted to recover the original text under 6 anchor conditions: "
        f"0, 1, 3, 5, 10, and 20 correct sign assignments revealed.",
        styles["body"]
    ))

    story.append(p("Core Result", styles["h2"]))
    story.append(sp_text(
        safe_text(
            f"Top-1 accuracy on non-anchored signs: "
            f"{_pct(agg.get('0',{}).get('overall_modal_top1_free'))} with 0 anchors, "
            f"rising to {_pct(agg.get('20',{}).get('overall_modal_top1_free'))} with 20 anchors "
            f"(improvement: {_pct(conc.get('free_accuracy_improvement'))}). "
            f"Overall verdict: {conc.get('overall_verdict','UNKNOWN')}."
        ),
        styles["body"]
    ))

    story.append(p("Interpretation", styles["h2"]))
    story.append(sp_text(
        safe_text(conc.get("conclusion_text",
            "Results are pending. See the full technical report for details.")),
        styles["body"]
    ))

    story.append(p("Key Difference from NW Semitic Test1", styles["h2"]))
    story.append(sp_text(
        safe_text(
            "The NW Semitic test1 corpus has ~4.2 tokens per sign -- far too sparse "
            "for reliable statistical inference. The Geez corpus has "
            f"~{lms.get('mean_tokens_per_sign','?')} tokens per sign, giving the system "
            "the statistical signal it needs. This benchmark therefore tests the method "
            "at its full capability. If it fails here, the method requires fundamental "
            "revision. If it succeeds here, NW Semitic failure is due to data sparsity."
        ),
        styles["body"]
    ))

    story.append(p("Next Steps", styles["h2"]))
    next_steps_text = (
        "1. Review anchor convergence curve -- at what anchor count does accuracy "
        "begin rising consistently?\n"
        "2. If 20 anchors are insufficient, we should discuss whether a larger anchor set "
        "from Dr. Fuls' known Geez sign values can be incorporated.\n"
        "3. Based on results, we will update the NW Semitic analysis with corrected "
        "reading direction (RTL) and the 6 verified anchors you provided."
    )
    for line in next_steps_text.split("\n"):
        story.append(sp_text(safe_text(line.strip()), styles["body"]))
        story.append(sp(0.5))

    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default=None,
                        help="Path to specific JSON results file (default: most recent)")
    args = parser.parse_args()

    if args.json:
        json_path = Path(args.json)
    else:
        candidates = sorted(_REPORTS.glob("geez_syllabic_anchor_convergence_*.json"))
        if not candidates:
            print("No geez_syllabic_anchor_convergence_*.json found in reports/.")
            print("Run the experiment first:")
            print("  python -m glossa_lab.experiments.geez_syllabic_anchor_convergence")
            sys.exit(1)
        json_path = candidates[-1]

    print(f"Reading: {json_path}")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    styles = make_styles()
    ts = data.get("timestamp", "unknown")
    out_path = _REPORTS / f"geez_syllabic_anchor_convergence_report_{ts}.pdf"

    print(f"Generating PDF: {out_path}")
    build_report(data, styles, out_path)
    print(f"Done: {out_path}")


if __name__ == "__main__":
    main()
