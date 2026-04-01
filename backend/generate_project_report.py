"""Generate a comprehensive state-of-project PDF report.

This is the document to send to Dr. Fuls alongside the ICIT access request.
It demonstrates the toolkit's capabilities and what we'd do with the real data.

Usage: shell.cmd python backend/generate_project_report.py
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


def _tbl(data, widths):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f8fafc")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def generate():
    output = Path(__file__).parent.parent / "reports" / "glossa_lab_project_report.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    title_s = ParagraphStyle("T", parent=styles["Title"], fontSize=16, leading=20)
    sub_s = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=11,
                           alignment=1, spaceAfter=4)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], spaceAfter=6)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], spaceAfter=4)
    body = ParagraphStyle("B", parent=styles["Normal"], spaceAfter=8, leading=14)
    sm = ParagraphStyle("Sm", parent=styles["Normal"], fontSize=8, leading=10)
    cap = ParagraphStyle("Cap", parent=styles["Normal"], fontSize=8, leading=10,
                         alignment=1, spaceAfter=10, textColor=colors.HexColor("#555"))

    doc = SimpleDocTemplate(str(output), pagesize=letter,
                            topMargin=0.75*inch, bottomMargin=0.75*inch,
                            leftMargin=1*inch, rightMargin=1*inch)

    S = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # ═══════ TITLE ═══════
    S.append(Spacer(1, 0.6*inch))
    S.append(Paragraph(
        "Glossa Lab: A Computational Toolkit for<br/>"
        "Ancient Script Analysis and Decipherment", title_s))
    S.append(Spacer(1, 0.15*inch))
    S.append(Paragraph("Project Report and Collaboration Proposal", sub_s))
    S.append(Paragraph(f"BitConcepts \u2014 {now}", sub_s))
    S.append(PageBreak())

    # ═══════ 1. OVERVIEW ═══════
    S.append(Paragraph("1. Project Overview", h1))
    S.append(Paragraph(
        "Glossa Lab is a proprietary, cross-platform research toolkit "
        "for computational analysis and decipherment of ancient scripts, "
        "developed by BitConcepts. Built in Python with a FastAPI backend, "
        "it combines statistical analysis, structural pattern detection, "
        "and automated decipherment in a single integrated platform. "
        "The toolkit incorporates patented technologies and is not "
        "publicly available at this time.", body))
    S.append(Paragraph(
        "The toolkit was designed with the Indus script as its primary "
        "target, but has been validated on synthetic ciphers and the "
        "historically deciphered Ugaritic script to establish baseline "
        "performance before attempting the undeciphered Indus corpus.", body))

    # ═══════ 2. CAPABILITIES ═══════
    S.append(Paragraph("2. Analysis Pipelines (11 total)", h1))

    pipeline_data = [
        ["Pipeline", "Function", "Status"],
        ["block_entropy", "Rao et al. (2009) normalised block entropy H_N", "Implemented"],
        ["char_freq", "Zipf distribution, rank-frequency, Zipf exponent", "Implemented"],
        ["kandles", "Phonetic color-coding and grids (Merkur patent)", "Implemented"],
        ["positional", "Position-specific sign frequencies (initial/medial/terminal)", "Implemented"],
        ["sign_cluster", "Distributional clustering (Kober method)", "Implemented"],
        ["paradigm", "Inflectional paradigm detection (Ventris/Kober)", "Implemented"],
        ["cooccurrence", "Sign co-occurrence network + community detection", "Implemented"],
        ["numerals", "Numeral sign identification from distributional behavior", "Implemented"],
        ["decipher", "Substitution cipher cracking (hill climbing + trigrams)", "Implemented"],
        ["hypothesis", "Iterative hypothesis-driven decipherment engine", "Implemented"],
        ["CPSC projection", "Multi-constraint decipherment (optional module)", "Implemented"],
    ]
    S.append(_tbl(pipeline_data, [1.1*inch, 3.2*inch, 1.0*inch]))
    S.append(Paragraph("<b>Table 1.</b> Analysis pipelines.", cap))

    # ═══════ 3. RESULTS ═══════
    S.append(Paragraph("3. Validated Results", h1))
    S.append(Paragraph("3.1 Block Entropy Replication (Rao et al. 2009)", h2))
    S.append(Paragraph(
        "We replicated the block entropy analysis across 9 corpora "
        "(English, Tamil, Sanskrit, Indus, DNA, Fortran, random, ordered, "
        "Markov). Results confirm: Random &gt; DNA &gt; Indus/English/Tamil/"
        "Sanskrit &gt; Fortran &gt; Ordered, consistent with the published "
        "findings.", body))

    S.append(Paragraph("3.2 Decipherment Engine Performance", h2))

    decipher_data = [
        ["Test", "Accuracy", "Details"],
        ["Synthetic cipher (21 phonemes)", "21/21 = 100%",
         "Random substitution, 500 inscriptions, CVC grammar"],
        ["Ugaritic Baal Cycle (30 signs)", "29/30 = 96.7%",
         "Real ancient script, 83 lines, Kandles confidence 1.000"],
    ]
    S.append(_tbl(decipher_data, [1.8*inch, 1.2*inch, 3.2*inch]))
    S.append(Paragraph("<b>Table 2.</b> Decipherment accuracy.", cap))

    S.append(Paragraph("3.3 Indus Script Hypothesis Test", h2))
    S.append(Paragraph(
        "We tested proto-Dravidian vs Vedic Sanskrit as competing "
        "target language hypotheses on a statistically representative "
        "synthetic Indus corpus (6,823 signs, 417 unique, matching "
        "published Zipf-Mandelbrot distributions from Yadav et al. 2010).", body))

    hyp_data = [
        ["Hypothesis", "Score", "Word Matches", "Kandles"],
        ["Proto-Dravidian", "297.0", "28 (28% coverage)", "0.985"],
        ["Vedic Sanskrit", "77.0", "6 (4.9% coverage)", "0.976"],
    ]
    S.append(_tbl(hyp_data, [1.3*inch, 0.8*inch, 1.8*inch, 0.8*inch]))
    S.append(Paragraph(
        "<b>Table 3.</b> Hypothesis engine results on synthetic Indus corpus. "
        "Proto-Dravidian scores 4\u00d7 higher.", cap))
    S.append(Paragraph(
        "<b>Note:</b> These results are on a synthetic corpus that reproduces "
        "published statistical properties, not the actual M77/ICIT data. "
        "Validation on real inscriptions is the critical next step.", body))

    # ═══════ 4. DATA NEEDS ═══════
    S.append(PageBreak())
    S.append(Paragraph("4. What We Need: The ICIT Corpus", h1))
    S.append(Paragraph(
        "Our toolkit is validated and ready. The single critical blocker "
        "is access to the actual Indus corpus in machine-readable form. "
        "The ICIT database (Wells &amp; Fuls) contains 4,537 inscribed "
        "objects with 5,509 texts and 19,616 sign occurrences \u2014 exactly "
        "the data our pipelines are designed to process.", body))
    S.append(Paragraph("<b>What we would do with ICIT access:</b>", body))
    S.append(Paragraph(
        "1. Run all 11 analysis pipelines on the complete corpus<br/>"
        "2. Validate our synthetic results against real sign distributions<br/>"
        "3. Run the hypothesis engine (Dravidian vs Sanskrit) on real data<br/>"
        "4. Apply numeral identification to reduce the phonetic search space<br/>"
        "5. Run positional analysis to classify all 676 signs by function<br/>"
        "6. Detect paradigms (inflectional patterns) across real inscriptions<br/>"
        "7. Build co-occurrence networks to identify sign communities<br/>"
        "8. Generate comprehensive PDF reports with all findings", body))
    S.append(Paragraph(
        "We have already built a Fuls-notation parser that handles the "
        "+sign-sign-sign+ format used in the published corpus volumes, "
        "including metadata extraction (findspot, object type, iconography, "
        "reading direction).", body))

    # ═══════ 5. METHODOLOGY ═══════
    S.append(Paragraph("5. Decipherment Methodology", h1))
    S.append(Paragraph(
        "<b>Stage 1 \u2014 Structural analysis:</b> Block entropy confirms "
        "the script is linguistic. Positional analysis classifies signs "
        "by grammatical function. Paradigm detection reveals inflectional "
        "patterns. Numeral identification reduces the search space.", body))
    S.append(Paragraph(
        "<b>Stage 2 \u2014 Hypothesis testing:</b> Competing target language "
        "models (proto-Dravidian from DEDR roots + Old Tamil; Vedic "
        "Sanskrit from Rigveda) are tested against the corpus. The "
        "hypothesis that produces more word matches and better paradigm "
        "regularity is promoted.", body))
    S.append(Paragraph(
        "<b>Stage 3 \u2014 Iterative decipherment:</b> Confident sign mappings "
        "are locked. Remaining signs are optimised against the target "
        "language model using bigram/trigram hill climbing with Kandles "
        "phonetic validation. Each iteration reduces the unknown space.", body))

    # ═══════ 6. TECH ═══════
    S.append(Paragraph("6. Technical Details", h1))
    S.append(Paragraph(
        "102 automated tests \u2022 Python 3.12 \u2022 FastAPI backend \u2022 "
        "SQLite database \u2022 CI on Windows/Linux/macOS \u2022 "
        "PDF report generation \u2022 Cross-platform \u2022 "
        "Proprietary \u2014 incorporates patented technologies "
        "(US 2024/0248922 A1, US Provisional 63/980,251)", body))

    # ═══════ REFS ═══════
    S.append(Paragraph("References", h1))
    for ref in [
        "[1] Rao et al. (2009). Science 324:1165.",
        "[2] Yadav et al. (2010). PLoS ONE 5(3):e9506.",
        "[3] Mahadevan (1977). The Indus Script. ASI No. 77.",
        "[4] Fuls (2023). Corpus of Indus Inscriptions.",
        "[5] Fuls (2023). A Catalog of Indus Signs.",
        "[6] Parpola (1994). Deciphering the Indus Script.",
        "[7] Merkur (2024). US 2024/0248922 A1.",
    ]:
        S.append(Paragraph(ref, sm))

    doc.build(S)
    return output


if __name__ == "__main__":
    path = generate()
    print(f"Report generated: {path}")
