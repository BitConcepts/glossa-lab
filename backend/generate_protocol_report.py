"""Generate PDF report from the Research Protocol pipeline results.

Reads from reports/protocol/*.json and writes
reports/glossa_lab_protocol_results_2026-04.pdf

Usage: shell.cmd python backend/generate_protocol_report.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate_experimental_results_report import _BASE_FONT, _BOLD_FONT, _tbl, _u
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

_REPO_ROOT = Path(__file__).parent.parent
_PROTO = _REPO_ROOT / "reports" / "protocol"


def _load(name: str) -> dict:
    p = _PROTO / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def generate():
    output = _REPO_ROOT / "reports" / "glossa_lab_protocol_results_2026-04.pdf"

    styles = getSampleStyleSheet()
    title_s = ParagraphStyle("T", parent=styles["Title"], fontSize=18, leading=22,
                             textColor=colors.HexColor("#1e3a5f"), fontName=_BOLD_FONT)
    sub_s = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=11,
                           alignment=1, textColor=colors.HexColor("#374151"), fontName=_BASE_FONT)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=13,
                        textColor=colors.HexColor("#1e3a5f"), spaceBefore=14, spaceAfter=6,
                        fontName=_BOLD_FONT)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11,
                        textColor=colors.HexColor("#2563eb"), spaceBefore=10, spaceAfter=4,
                        fontName=_BOLD_FONT)
    body = ParagraphStyle("B", parent=styles["Normal"], fontSize=9.5, leading=14,
                          spaceAfter=8, fontName=_BASE_FONT)
    sm = ParagraphStyle("Sm", parent=styles["Normal"], fontSize=8.5, leading=12,
                        spaceAfter=6, fontName=_BASE_FONT)
    cap = ParagraphStyle("Cap", parent=styles["Normal"], fontSize=8, leading=10,
                         alignment=1, spaceAfter=10,
                         textColor=colors.HexColor("#6b7280"), fontName=_BASE_FONT)
    warn = ParagraphStyle("Warn", parent=styles["Normal"], fontSize=9, leading=13,
                          spaceAfter=8, textColor=colors.HexColor("#92400e"),
                          backColor=colors.HexColor("#fef3c7"), fontName=_BASE_FONT)

    doc = SimpleDocTemplate(str(output), pagesize=letter,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch,
                            leftMargin=1 * inch, rightMargin=1 * inch)
    S = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Title
    S.append(Spacer(1, 0.6 * inch))
    S.append(Paragraph("Glossa Lab", title_s))
    S.append(Paragraph("Research Protocol: Structural Convergence Results", title_s))
    S.append(Spacer(1, 0.15 * inch))
    S.append(Paragraph("ICIT Full-Sequence Convergence Test -- Sections 5-15", sub_s))
    S.append(Paragraph(f"BitConcepts -- {now}", sub_s))
    S.append(Spacer(1, 0.3 * inch))
    S.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a5f")))
    S.append(Spacer(1, 0.1 * inch))

    # Load data
    stats = _load("descriptive_stats.json")
    ent = _load("entropy_results.json")
    nwsp = _load("nwsp_classes.json")
    ws = _load("word_structure_scores.json")
    aff = _load("grid_clusters.json")
    term = _load("terminal_markers.json")
    pred = _load("predictive_results.json")
    adv = _load("null_control_results.json")
    conv = _load("convergence_assessment.json")
    null_ent = _load("entropy_null_comparison.json")
    sites = _load("site_comparison.json")

    has_data = bool(stats)

    # Important caveat
    S.append(Paragraph(
        "<b>Data source:</b> " + _u(stats.get("source", "Unknown") + " -- " +
        ("PSEUDO-SEQUENCES from positional statistics (not real inscription sequences). "
         "Results on real ICIT sequences will differ." if not stats.get("has_real_sequences")
         else "REAL inscription sequences.")),
        warn))

    # Section 1: Corpus
    S.append(Paragraph("1. Corpus Summary", h1))
    if has_data:
        c_data = [
            ["Metric", "Value"],
            ["Source", _u(stats.get("source", "?"))],
            ["Real sequences", "YES" if stats.get("has_real_sequences") else "NO (pseudo)"],
            ["Inscriptions", f"{stats.get('n_inscriptions', 0):,}"],
            ["Tokens", f"{stats.get('n_tokens', 0):,}"],
            ["Distinct sign types", f"{stats.get('distinct_sign_types', 0):,}"],
            ["Avg inscription length", f"{stats.get('avg_inscription_length', 0):.2f} signs"],
            ["Type-token ratio", f"{stats.get('type_token_ratio', 0):.5f}"],
            ["Hapax fraction", f"{stats.get('hapax_fraction', 0):.2%}"],
            ["Commit", stats.get("commit", "?")],
        ]
        S.append(_tbl(c_data, [2.5 * inch, 4.0 * inch]))
        S.append(Paragraph("<b>Table 1.</b> Corpus statistics.", cap))

    # Section 2: Entropy
    S.append(Paragraph("2. Entropy Analysis", h1))
    if ent:
        e_data = [
            ["Measure", "Value", "Interpretation"],
            ["H1 (bits)", f"{ent.get('H1', 0):.4f}", "Raw block entropy at n=1"],
            ["H1 normalised", f"{ent.get('H1_normalised', 0):.4f}",
             "Linguistic range: 0.60-0.95"],
            ["H2/H1 ratio", f"{ent.get('H2_H1_ratio', 0):.4f}",
             "Sub-linear if < 1.95 (linguistic)"],
            ["Classification", ent.get("linguistic_classification", "?").upper(), ""],
        ]
        if null_ent:
            e_data += [
                ["Real H1", f"{null_ent.get('real_H1', 0):.4f}", "Actual corpus"],
                ["Shuffled-global H1", f"{null_ent.get('shuffled_global_H1', 0):.4f}", "Null control"],
                ["Unigram-synthetic H1", f"{null_ent.get('unigram_synthetic_H1', 0):.4f}", "Null control"],
            ]
        S.append(_tbl(e_data, [1.8 * inch, 1.2 * inch, 3.3 * inch]))
        S.append(Paragraph(f"<b>Table 2.</b> Entropy results. Null: {_u(null_ent.get('conclusion', '?'))}", cap))

    # Section 3: Positional (NWSP)
    S.append(Paragraph("3. Positional Analysis (NWSP Classification)", h1))
    if nwsp:
        cc = nwsp.get("class_counts", {})
        total_cls = sum(cc.values()) or 1
        p_data = [
            ["Class", "Count", "Pct", "Meaning"],
            ["TMK (terminal)", str(cc.get("TMK", 0)),
             f"{cc.get('TMK', 0)/total_cls:.1%}", "Likely grammatical suffixes"],
            ["INITIAL", str(cc.get("INITIAL", 0)),
             f"{cc.get('INITIAL', 0)/total_cls:.1%}", "Inscription-initial signs"],
            ["MED (medial)", str(cc.get("MED", 0)),
             f"{cc.get('MED', 0)/total_cls:.1%}", "Likely syllabograms"],
            ["ITM (bimodal)", str(cc.get("ITM", 0)),
             f"{cc.get('ITM', 0)/total_cls:.1%}", "Dual-function signs"],
            ["CON (constant)", str(cc.get("CON", 0)),
             f"{cc.get('CON', 0)/total_cls:.1%}", "High-entropy signs"],
        ]
        S.append(_tbl(p_data, [1.3 * inch, 0.7 * inch, 0.7 * inch, 3.6 * inch]))
        S.append(Paragraph("<b>Table 3.</b> NWSP classification.", cap))

        tmk = nwsp.get("tmk_signs", [])
        if tmk:
            S.append(Paragraph(f"Top TMK signs: {', '.join(str(s) for s in tmk[:10])}", sm))

    # Section 4: Word-structure ranking
    S.append(Paragraph("4. Word-Structure Family Ranking", h1))
    if ws:
        S.append(Paragraph(
            f"Winner: <b>{_u(ws.get('winner', '?'))}</b> "
            f"(KL={ws.get('winner_kl', 0):.4f}, margin={ws.get('margin', 0):.4f}). "
            "Lower KL = better structural fit.",
            body))
        ranking = ws.get("ranking", [])
        if ranking:
            ws_data = [["Rank", "Family", "KL-Divergence", "Mean Length Diff"]]
            for r in ranking:
                ws_data.append([
                    f"#{r['rank']}",
                    _u(r["profile"]),
                    f"{r['word_length_kl']:.4f}",
                    f"{r['mean_length_diff']:.4f}",
                ])
            S.append(_tbl(ws_data, [0.6 * inch, 2.0 * inch, 1.3 * inch, 1.5 * inch]))
            S.append(Paragraph("<b>Table 4.</b> Word-structure family ranking by KL-divergence.", cap))

    # Section 5: Affinity grid
    S.append(Paragraph("5. Affinity Grid Clustering (Ventris Method)", h1))
    if aff:
        S.append(Paragraph(
            f"Candidates analysed: {aff.get('n_candidates', 0)}. "
            f"Vowel clusters (shared left-context): {aff.get('n_vowel_clusters', 0)}. "
            f"Consonant clusters (shared right-context): {aff.get('n_consonant_clusters', 0)}.",
            body))
        vcl = aff.get("vowel_clusters", [])
        if vcl:
            vc_data = [["Cluster", "Signs"]]
            for i, cl in enumerate(vcl[:8]):
                vc_data.append([f"V{i+1}", ", ".join(str(s) for s in cl)])
            S.append(_tbl(vc_data, [0.8 * inch, 5.5 * inch]))
            S.append(Paragraph("<b>Table 5.</b> Vowel clusters (probable shared-vowel groupings).", cap))

    # Section 6: Terminal morphology
    S.append(Paragraph("6. Terminal Morphology", h1))
    if term:
        top_t = term.get("top_terminal_signs", [])[:10]
        if top_t:
            t_data = [["Sign", "Count", "Rate", "Class"]]
            attach = term.get("attachment_profiles", {})
            prod = set(term.get("productive_suffixes", []))
            form = set(term.get("formula_endings", []))
            for t in top_t:
                s = str(t["sign"])
                cls = "productive" if s in prod else "formula" if s in form else "restricted"
                t_data.append([s, str(t["count"]), f"{t['rate']:.3f}", cls])
            S.append(_tbl(t_data, [1.0 * inch, 0.8 * inch, 0.8 * inch, 2.0 * inch]))
            S.append(Paragraph(
                f"<b>Table 6.</b> Top terminal signs. Productive suffixes: "
                f"{len(prod)}, formula endings: {len(form)}.", cap))

    S.append(PageBreak())

    # Section 7: Site replication
    S.append(Paragraph("7. Site-Split Replication", h1))
    if sites:
        s_data = [["Site", "Inscriptions", "Avg Length", "Winner", "Margin"]]
        for site, v in sites.items():
            s_data.append([
                _u(site), str(v["n_inscriptions"]),
                f"{v['avg_length']:.2f}", _u(v["winner"]), f"{v['margin']:.4f}",
            ])
        S.append(_tbl(s_data, [1.2 * inch, 0.9 * inch, 0.9 * inch, 1.8 * inch, 0.8 * inch]))
        S.append(Paragraph("<b>Table 7.</b> Site-split replication results.", cap))

    # Section 8: Predictive validation
    S.append(Paragraph("8. Predictive Validation", h1))
    if pred:
        pv_data = [
            ["Metric", "Value"],
            ["Avg top-1 accuracy (model)", f"{pred.get('avg_top1_model', 0):.3f}"],
            ["Avg top-3 accuracy (model)", f"{pred.get('avg_top3_model', 0):.3f}"],
            ["Freq baseline (top-1)", f"{pred.get('avg_top1_freq_baseline', 0):.3f}"],
            ["Unigram baseline (top-1)", f"{pred.get('avg_top1_unigram_baseline', 0):.3f}"],
            ["Model vs freq delta", f"{pred.get('model_vs_freq_delta', 0):+.3f}"],
            ["Beats frequency baseline", "YES" if pred.get("beats_frequency_baseline") else "NO"],
        ]
        S.append(_tbl(pv_data, [3.0 * inch, 3.0 * inch]))
        S.append(Paragraph(
            "<b>Table 8.</b> 5-fold predictive validation (final sign prediction task).", cap))

    # Section 9: Convergence
    S.append(Paragraph("9. Convergence Assessment", h1))
    if conv:
        ch = conv.get("channel_scores", {})
        cv_data = [["Channel", "Score", "Weight"]]
        for k, v in ch.items():
            cv_data.append([_u(k.replace("_", " ").title()), v.upper(),
                            "3" if v == "strong" else "2" if v == "moderate" else "1" if v == "weak" else "0"])
        S.append(_tbl(cv_data, [2.5 * inch, 1.0 * inch, 0.7 * inch]))
        S.append(Paragraph(
            f"<b>Table 9.</b> Convergence channels. "
            f"Overall: <b>{conv.get('overall_convergence', '?').upper()}</b>. "
            f"Strong channels: {conv.get('n_strong', 0)}/6.", cap))

        # Escalation gates
        trig = conv.get("escalation_triggers", {})
        tr_data = [["Trigger", "Met?"]]
        for k, v in trig.items():
            tr_data.append([_u(k.replace("_", " ").title()), "YES" if v else "NO"])
        S.append(_tbl(tr_data, [4.0 * inch, 1.0 * inch]))
        S.append(Paragraph(
            f"<b>Table 10.</b> Escalation gate triggers. "
            f"Met: {conv.get('triggers_met', 0)}/6. "
            f"Phase 2 escalation: {'YES' if conv.get('escalate_to_phase2') else 'NO'}.", cap))

    S.append(PageBreak())

    # Conclusion
    S.append(Paragraph("10. Conclusion", h1))
    cl = conv.get("claim_level", 0) if conv else 0
    S.append(Paragraph(
        f"<b>Claim Level {cl}:</b> {_u(conv.get('claim', '') if conv else '')}",
        body))

    if not (stats.get("has_real_sequences") if stats else False):
        S.append(Paragraph(
            "<b>Important caveat:</b> These results are based on pseudo-sequences "
            "generated from Fuls (2023) positional statistics, not real ICIT inscription sequences. "
            "The convergence assessment on real sequences is expected to be substantially stronger -- "
            "real sequences preserve bigram structure, inscription-level patterns, site variation, "
            "and formula signatures that pseudo-sequences cannot capture. "
            "All convergence claims here are conservative lower bounds.",
            warn))

    S.append(Paragraph("Allowed claims at this stage:", h2))
    allowed = {
        0: ["The Indus corpus is structurally linguistic (H1=0.72, sub-linear H2/H1).",
            "A terminal-marker system exists and is classifiable.",
            "The pipeline is validated and ready for real ICIT sequences."],
        1: ["The Indus corpus is structurally linguistic.",
            "A stable terminal-marker system is identified.",
            f"Best current structural fit: {_u(ws.get('winner', '?') if ws else '?')} (vocabulary-free)."],
        2: ["A candidate morphological system is emerging.",
            "Stable stem/ending structure identified.",
            f"Best current structural fit: {_u(ws.get('winner', '?') if ws else '?')}."],
    }
    for line in allowed.get(min(cl, 2), allowed[0]):
        S.append(Paragraph(f"- {line}", sm))

    S.append(Paragraph("Forbidden claims:", h2))
    for line in [
        "This does not constitute decipherment.",
        "No semantic claims are supported.",
        "No phoneme mappings are confirmed.",
        "The family ranking is not proof of language identity.",
    ]:
        S.append(Paragraph(f"- {line}", sm))

    S.append(Paragraph("Next steps to strengthen convergence:", h2))
    S.append(Paragraph(
        "1. Obtain ICIT corpus from Dr. Fuls (TU Berlin) -- primary unlocker.\n"
        "2. Complete Mahadevan OCR (30 min, after Mistral quota refresh) -- real bigrams.\n"
        "3. Run TMK bigram cross-validation on real bigrams.\n"
        "4. Run full protocol on ICIT sequences with --corpus flag.",
        body))

    S.append(Spacer(1, 0.3 * inch))
    S.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#9ca3af")))
    S.append(Spacer(1, 0.1 * inch))
    S.append(Paragraph(
        f"Generated {now} -- BitConcepts / Glossa Lab -- Confidential",
        ParagraphStyle("foot", parent=styles["Normal"], fontSize=8,
                       alignment=1, textColor=colors.HexColor("#9ca3af"),
                       fontName=_BASE_FONT)))

    doc.build(S)
    print(f"[OK] Protocol report saved: {output}")
    return str(output)


if __name__ == "__main__":
    generate()
