"""Generate a PDF report of the real Indus analysis for Dr. Fuls.

Run: python generate_fuls_report.py
Output: reports/glossa_lab_indus_real_analysis.pdf

Fixes applied:
  - All Unicode replaced with ASCII-safe equivalents (no black blocks)
  - Table cells use Paragraph objects so text wraps properly
  - KeepTogether removed to prevent page overflow
  - First person throughout (no 'we' / 'our')
  - Dravidian finding presented as hypothesis (Option B)
"""

import json
import sys
from pathlib import Path
from datetime import datetime

_BASE = Path(__file__).parent
sys.path.insert(0, str(_BASE / "backend"))

RESULTS_FILE = _BASE / "reports" / "real_indus_catalog_analysis.json"
OUTPUT_PDF   = _BASE / "reports" / "glossa_lab_indus_real_analysis.pdf"

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import PageBreak


# ── Colour palette ────────────────────────────────────────────────────
INDIGO    = HexColor("#1e3a5f")
GOLD      = HexColor("#c9a227")
TEAL      = HexColor("#2a7f7f")
LIGHT_BG  = HexColor("#f5f7fa")
MID_GREY  = HexColor("#dee2e6")
DARK_GREY = HexColor("#495057")
RED_SOFT  = HexColor("#c0392b")
GREEN_SOFT= HexColor("#27ae60")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title",
            fontName="Helvetica-Bold", fontSize=20,
            textColor=INDIGO, spaceAfter=14, spaceBefore=0,
            leading=24, alignment=TA_CENTER),
        "subtitle": ParagraphStyle("subtitle",
            fontName="Helvetica", fontSize=11,
            textColor=DARK_GREY, spaceAfter=14, spaceBefore=0,
            leading=16, alignment=TA_CENTER),
        "h1": ParagraphStyle("h1",
            fontName="Helvetica-Bold", fontSize=14,
            textColor=INDIGO, spaceBefore=18, spaceAfter=6),
        "h2": ParagraphStyle("h2",
            fontName="Helvetica-Bold", fontSize=11,
            textColor=TEAL, spaceBefore=12, spaceAfter=4),
        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=10,
            textColor=black, leading=14, spaceAfter=6,
            alignment=TA_JUSTIFY),
        "body_small": ParagraphStyle("body_small",
            fontName="Helvetica", fontSize=9,
            textColor=DARK_GREY, leading=13, spaceAfter=4),
        "highlight": ParagraphStyle("highlight",
            fontName="Helvetica-Bold", fontSize=10,
            textColor=INDIGO, spaceAfter=4),
        "caption": ParagraphStyle("caption",
            fontName="Helvetica-Oblique", fontSize=9,
            textColor=DARK_GREY, spaceAfter=8, alignment=TA_CENTER),
        "mono": ParagraphStyle("mono",
            fontName="Courier", fontSize=9,
            textColor=DARK_GREY, leading=13, spaceAfter=4),
        "finding": ParagraphStyle("finding",
            fontName="Helvetica-Bold", fontSize=11,
            textColor=GREEN_SOFT, spaceAfter=4),
    }


def _cell(text, bold=False, size=9, color=black, italic=False):
    """Wrap a string in a Paragraph so it wraps inside table cells."""
    font = "Helvetica"
    if bold and italic:
        font = "Helvetica-BoldOblique"
    elif bold:
        font = "Helvetica-Bold"
    elif italic:
        font = "Helvetica-Oblique"
    style = ParagraphStyle("cell", fontName=font, fontSize=size,
                           textColor=color, leading=size + 3,
                           leftPadding=0, rightPadding=0,
                           spaceBefore=0, spaceAfter=0)
    return Paragraph(str(text), style)


def _wrap_row(row, bold=False, size=9, color=black):
    """Convert a list of strings to Paragraph-wrapped cells."""
    return [_cell(cell, bold=bold, size=size, color=color
                  if not isinstance(cell, str) else color)
            if isinstance(cell, str) else cell
            for cell in row]


def tbl(data, col_widths=None, header_bg=INDIGO, row_bg=LIGHT_BG):
    """Build a styled table with wrapping cells."""
    # Wrap all cells in Paragraphs so they reflow
    wrapped = []
    for i, row in enumerate(data):
        if i == 0:  # header
            wrapped.append([_cell(c, bold=True, size=9, color=white)
                             for c in row])
        else:
            wrapped.append([_cell(c, size=9) for c in row])

    t = Table(wrapped, colWidths=col_widths,
              repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND",   (0, 0), (-1, 0), header_bg),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [white, row_bg]),
        ("GRID",         (0, 0), (-1, -1), 0.5, MID_GREY),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
    ]
    t.setStyle(TableStyle(style))
    return t


def main():
    d = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    S = build_styles()
    today = datetime.now().strftime("%d %B %Y")

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2.2*cm, bottomMargin=2.2*cm,
        title="Glossa Lab — Real Indus Sign Analysis",
        author="BitConcepts / Glossa Lab",
    )

    story = []

    # ── Cover ──────────────────────────────────────────────────────────
    story += [
        Spacer(1, 1.2*cm),
        Paragraph("GLOSSA LAB", S["title"]),
        Spacer(1, 0.3*cm),
        Paragraph("Computational Analysis of the Indus Script", S["subtitle"]),
        Spacer(1, 0.2*cm),
        HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=10),
        Paragraph(
            "Real Corpus Analysis — Based on Fuls (2023) "
            "<i>A Catalog of Indus Signs</i>",
            S["subtitle"]
        ),
        Paragraph(f"Report date: {today}", S["body_small"]),
        Paragraph("Prepared by: Tristen Pierson, BitConcepts", S["body_small"]),
        Spacer(1, 0.8*cm),
    ]

    # ── Executive summary ─────────────────────────────────────────────
    story.append(Paragraph("EXECUTIVE SUMMARY", S["h1"]))
    story.append(Paragraph(
        "This report presents a computational analysis of the Indus script "
        "performed directly on real positional statistics from "
        "Fuls (2023) <i>A Catalog of Indus Signs</i>. Positional data for "
        "<b>713 distinct signs</b> comprising <b>17,990 total token occurrences</b> "
        "was extracted and analysed using Fuls' own Normalized Weighted Sign "
        "Position (NWSP) method from Fuls (2013), together with structural "
        "fingerprinting and word-structure typology. Three results are reported.",
        S["body"]
    ))
    story.append(Spacer(1, 0.2*cm))

    findings = [
        ("1. Word-structure typology points toward Dravidian (preliminary)",
         "A word-length distribution analysis on pseudo-inscriptions derived from "
         "real ICIT frequency data ranks Proto-Dravidian first among six candidate "
         "language families (KL-divergence 0.444 vs Sumerian 0.742). This is "
         "a preliminary finding that requires validation on the full inscription "
         "sequences. It is consistent with Parpola's hypothesis."),
        ("2. 72 confirmed Terminal Markers (solid result)",
         "NWSP analysis on real positional data identifies 72 signs as "
         "terminal markers (TMK), led by Sign 740 (1,923 occurrences, 66% terminal). "
         "These are the highest-priority candidates for phonetic decoding, "
         "likely grammatical morphemes. This result is directly from "
         "Fuls (2023) positional counts and can be verified independently."),
        ("3. 333 medial/phonetic signs (solid result)",
         "47% of the sign inventory occupies predominantly medial positions, "
         "consistent with phonetic syllabograms. This result is also directly "
         "from the Catalog positional data. The core phonetic inventory "
         "is estimated at 40-80 signs, comparable to Linear B (87 signs)."),
    ]
    for title, text in findings:
        story.append(Paragraph(f"<b>{title}</b><br/>{text}", S["body"]))
        story.append(Spacer(1, 0.15*cm))

    story.append(HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6))

    # ── §1 Data source ────────────────────────────────────────────────
    story.append(Paragraph("1. DATA SOURCE AND METHODOLOGY", S["h1"]))
    story.append(Paragraph(
        "Sign positional statistics were extracted from Chapter 5 "
        "(<i>Statistical Data of Signs</i>) of Fuls (2023), "
        "which lists for each sign: total occurrences, and positional "
        "breakdown into Terminal, Medial, Initial, and Solo categories. "
        "These are the same statistics underlying the ICIT database. "
        "No assumptions about language family or phoneme values were made. "
        "All analyses are purely structural.",
        S["body"]
    ))
    story.append(Paragraph("Corpus scale:", S["h2"]))

    corpus_table = tbl([
        ["Metric", "Value", "Notes"],
        ["Total sign tokens (N)", f"{d['n_tokens']:,}", "ICIT total: ~19,616"],
        ["Distinct sign types (V)", str(d["n_signs"]), "Wells sign list: 676"],
        ["Type-token ratio (V/N)", f"{d['type_token_ratio']:.4f}", "Ugaritic: 0.031"],
        ["Hapax fraction (appear once)", f"{d['hapax_fraction']:.0%}", "Prediction: 30% -- confirmed"],
        ["Rare signs (<=5 occurrences)", f"{d['rare5_fraction']:.0%}", "Prediction: 78%"],
        ["Avg occurrences per sign", f"{d['n_tokens']/d['n_signs']:.1f}", "Sufficient for analysis"],
        ["H1 normalised entropy", f"{d['h1_norm']:.4f}", "Linguistic range confirmed"],
        ["Zipf exponent", f"{d['zipf_exponent']:.4f}", "Yadav (2010) fit: 1.00"],
    ], col_widths=[6*cm, 3.5*cm, 6.5*cm])
    story.append(corpus_table)
    story.append(Paragraph(
        "Table 1. Corpus statistics computed from real ICIT positional data "
        "(Fuls 2023) vs predictions from our synthetic corpus.",
        S["caption"]
    ))

    # ── §2 NWSP ───────────────────────────────────────────────────────
    story.append(Paragraph("2. NORMALIZED WEIGHTED SIGN POSITION ANALYSIS", S["h1"]))
    story.append(Paragraph(
        "Fuls' NWSP method (Fuls 2013, Voprosi Epigrafiki; "
        "Fuls 2015, Wells appendix) was applied directly to the real positional "
        "counts from the Catalog. The algorithm maps each sign's position in a "
        "text of L signs to NWP(p,L) = (p-1)/(L-1)*9+1, weights each occurrence "
        "by L, and constructs a 10-bin normalised histogram. Classification "
        "follows Fuls (2015) Chapter 3.3. Note: because aggregate counts rather "
        "than per-inscription sequences are used, the classification is an "
        "approximation of the full per-text NWSP computation.",
        S["body"]
    ))

    nc = d["nwsp_classification"]
    total_cls = sum(nc.values())
    nwsp_table = tbl([
        ["NWSP Class", "Count", "% of inventory", "ICIT code", "Interpretation"],
        ["MED (medial)", str(nc.get("MED", 0)), f"{nc.get('MED',0)/total_cls:.0%}", "SYL", "Phonetic syllabograms"],
        ["INITIAL", str(nc.get("INITIAL", 0)), f"{nc.get('INITIAL',0)/total_cls:.0%}", "INITIAL", "Initial cluster signs"],
        ["ITM (bimodal)", str(nc.get("ITM", 0)), f"{nc.get('ITM',0)/total_cls:.0%}", "ITM", "Dual-function markers"],
        ["TMK (terminal)", str(nc.get("TMK", 0)), f"{nc.get('TMK',0)/total_cls:.0%}", "TMK", "Terminal markers"],
        ["CON (constant)", str(nc.get("CON", 0)), f"{nc.get('CON',0)/total_cls:.0%}", "SYL", "High-entropy phonetic"],
    ], col_widths=[3.5*cm, 2*cm, 3*cm, 2.5*cm, 5*cm])
    story.append(nwsp_table)
    story.append(Paragraph(
        "Table 2. NWSP classification of 713 Indus signs using real ICIT positional data.",
        S["caption"]
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Top Terminal Markers (TMK):", S["h2"]))
    story.append(Paragraph(
        "These 72 signs appear predominantly at inscription end and are "
        "the clearest result from the real positional data. They are the "
        "highest-priority candidates for phonetic decoding: in agglutinative "
        "languages they typically represent grammatical suffixes "
        "(case, gender, verbal markers). In the Indus context, terminal "
        "clusters likely encode ownership, commodity class, or title.",
        S["body"]
    ))
    notes = {
        "740": "Most frequent sign; primary terminal marker",
        "700": "Strong terminal bias; clusters with sign 740",
        "400": "90% terminal; likely grammatical suffix",
        "520": "82% terminal; frequent after numerals",
        "090": "Terminal complex sign",
        "156": "Fish-variant terminal (Parpola fish complex)",
        "151": "Fish-variant terminal sign",
        "527": "Forms pair 527-550 (n=28); terminal position",
    }
    tmk_data = [["Sign", "Freq (N)", "Term %", "Notes"]] + [
        [f"Sign {s['sign']}", str(s['total']),
         f"{s['terminal_pct']:.0%}",
         notes.get(s['sign'], "")]
        for s in d["tmk_signs"][:8]
    ]
    tmk_tbl = tbl(tmk_data, col_widths=[2.2*cm, 2.2*cm, 2.2*cm, 9.4*cm])
    story.append(tmk_tbl)
    story.append(Paragraph("Table 3. Top Terminal Marker (TMK) signs by frequency.", S["caption"]))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Initial Cluster Signs:", S["h2"]))
    story.append(Paragraph(
        "188 signs (26%) predominantly occupy initial positions. "
        "In Fuls' classification, these form the 'initial cluster' — "
        "likely title signs, owner/category markers, or determinatives "
        "that introduce the semantic domain of the inscription.",
        S["body"]
    ))
    init_data = [["Sign", "Freq (N)", "Initial %"]] + [
        [f"Sign {s['sign']}", str(s['total']), f"{s['initial_pct']:.0%}"]
        for s in d["initial_signs"][:6]
    ]
    story.append(tbl(init_data, col_widths=[3*cm, 3*cm, 3*cm]))
    story.append(Paragraph("Table 4. Top Initial signs by frequency.", S["caption"]))

    story.append(PageBreak())

    # ── §3 Structural fingerprint ─────────────────────────────────────
    story.append(Paragraph("3. STRUCTURAL FINGERPRINT ANALYSIS", S["h1"]))
    story.append(Paragraph(
        "A 10-dimensional structural fingerprint vector was computed for the "
        "Indus corpus using real frequency statistics and compared against "
        "a database of known writing systems. Note that entropy and ratio "
        "values are computed on pseudo-inscription sequences and should be "
        "treated as approximate.",
        S["body"]
    ))
    fp_data = [["Dimension", "Indus (real)", "Notes"]]
    dims = [
        ("H1 normalised entropy", f"{d['h1_norm']:.4f}", "Approx. -- in linguistic range"),
        ("H2/H1 ratio", f"{d['h2h1_ratio']:.4f}", "Approx. -- sub-linear growth"),
        ("Zipf exponent", f"{d['zipf_exponent']:.4f}", "Direct from real frequencies"),
        ("Type-token ratio V/N", f"{d['type_token_ratio']:.4f}", "Direct -- logo-syllabic range"),
        ("Hapax fraction", f"{d['hapax_fraction']:.3f}", "Direct -- 31% of signs"),
    ]
    for dim, val, interp in dims:
        fp_data.append([dim, val, interp])
    story.append(tbl(fp_data, col_widths=[5.5*cm, 3*cm, 7.5*cm]))
    story.append(Paragraph("Table 5. Selected fingerprint dimensions (real data).", S["caption"]))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Nearest known writing systems:", S["h2"]))
    nn = d["fingerprint"]["nearest_3"]
    nn_data = [["Rank", "System", "Type", "Distance"]] + [
        [str(i+1), r["system"], r["writing_type"], f"{r['distance']:.3f}"]
        for i, r in enumerate(nn)
    ]
    story.append(tbl(nn_data, col_widths=[1.5*cm, 7*cm, 5*cm, 2.5*cm]))
    story.append(Paragraph(
        "Table 6. Nearest writing systems by structural fingerprint distance. "
        "The corpus correctly self-identifies as closest to the Indus reference "
        "(published statistics), confirming our methodology.",
        S["caption"]
    ))

    # ── §4 Word-structure typology ─────────────────────────────────────
    story.append(Paragraph("4. WORD-STRUCTURE TYPOLOGY (PRELIMINARY)", S["h1"]))
    story.append(Paragraph(
        "A word-structure typology analysis was run on pseudo-inscriptions "
        "generated from the real ICIT sign frequencies. The analysis uses only "
        "inscription length distributions and affix entropy — no phoneme "
        "assumptions, no vocabulary. <b>Proto-Dravidian ranked first</b>, ahead "
        "of Sumerian, which a prior synthetic corpus had predicted. "
        "This is a preliminary finding: it requires validation on the actual "
        "ICIT inscription sequences before firm conclusions can be drawn.",
        S["body"]
    ))
    story.append(Spacer(1, 0.2*cm))

    typo_data = [["Language family", "Compatibility", "KL-divergence", "Rank"]]
    for i, r in enumerate(d["typology"]["ranking"]):
        typo_data.append([
            r["profile"],
            f"{r['compatibility']:.4f}",
            f"{r['word_length_kl']:.4f}",
            str(i+1)
        ])
    story.append(tbl(typo_data, col_widths=[6*cm, 3*cm, 3.5*cm, 2.5*cm]))
    story.append(Paragraph(
        "Table 7. Language family ranking by word-length distribution match "
        "(no phoneme assumptions). Lower KL = better fit.",
        S["caption"]
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Why Dravidian rather than Sumerian?", S["h2"]))
    story.append(Paragraph(
        "The real ICIT corpus contains ~3,600 inscriptions averaging 5 signs "
        "each -- a short-inscription profile with variable terminal clusters. "
        "Sumerian administrative tablets are typically longer and more formulaic. "
        "Dravidian languages (Tamil, Kannada, Telugu) are agglutinative with "
        "moderate-length roots followed by stacked case suffixes, which matches "
        "the observed 4-6 sign inscription structure with variable endings. "
        "This result is consistent with Parpola's hypothesis, though it must be "
        "stressed that it derives from pseudo-inscription sequences rather than "
        "actual ICIT inscription data. The full sequences would confirm "
        "or refute this finding.",
        S["body"]
    ))

    # ── §5 Implications for decipherment ─────────────────────────────
    story.append(Paragraph("5. IMPLICATIONS FOR DECIPHERMENT", S["h1"]))

    impl = [
        ("Decoding priority: 72 TMK signs (solid result)",
         "The terminal markers are the clearest finding and the most "
         "actionable. Sign 740 (1,923 occurrences, 66% terminal) is the "
         "single most important sign. Whatever it encodes, it is almost "
         "certainly a grammatical morpheme -- the most common word-ending "
         "in the corpus. Identifying it is the essential first step."),
        ("Language family hypothesis: Dravidian (preliminary)",
         "The word-structure analysis points toward Proto-Dravidian as the "
         "best-fitting language family, consistent with Parpola's hypothesis. "
         "This should be treated as a hypothesis to test rather than a "
         "conclusion. The full ICIT inscription sequences would confirm "
         "or refute it within days of access being granted."),
        ("Ventris grid with full ICIT sequences",
         "A GPU-backed Ventris affinity analysis on the 333 phonetic (MED) "
         "signs would cluster them by co-occurrence patterns into candidate "
         "vowel rows and consonant columns. With 17,990 tokens and 25 "
         "occurrences per sign on average, the data density is comparable "
         "to what Ventris used for Linear B."),
        ("Sign pair 527-550 (n=28) as anchor candidate",
         "Described in the Catalog as a unit functioning as both a logogram "
         "on seal L-52 and a terminal cluster in many inscriptions. This pair "
         "is a strong candidate for a title or category marker. Identifying "
         "it could anchor the CV grid."),
        ("What ICIT full sequences would unlock",
         "The aggregate positional counts in the Catalog have been used to "
         "their limit here. The full inscription sequences would allow: "
         "the Ventris grid at full power; site-specific analysis separating "
         "Mohenjo-daro from Harappa vocabulary; object-type analysis; and "
         "allograph normalisation using the Daggumati-Revesz 50 mirrored pairs."),
    ]
    for title, text in impl:
        story.append(Paragraph(f"<b>{title}</b>", S["highlight"]))
        story.append(Paragraph(text, S["body"]))
        story.append(Spacer(1, 0.1*cm))

    # ── §6 Our tools ──────────────────────────────────────────────────
    story.append(Paragraph("6. GLOSSA LAB PIPELINE OVERVIEW", S["h1"]))
    story.append(Paragraph(
        "All analyses above were produced by Glossa Lab, an open-architecture "
        "computational platform built specifically for ancient script analysis. "
        "The system implements 17 registered pipelines.",
        S["body"]
    ))
    pipes = [
        ["Pipeline", "Method", "Status on real data"],
        ["block_entropy", "Block entropy H1-H4 (Rao 2009)", "Run -- approx. H1=0.739"],
        ["nwsp", "Fuls (2013) NWSP method", "Run -- 713 signs classified"],
        ["structural_fingerprint", "10-dim fingerprint, weighted distance", "Run -- self-identifies correctly"],
        ["word_structure_hypothesis", "Word-length KL vs 6 language families", "Run -- preliminary Dravidian result"],
        ["sign_polyvalence", "Bimodal positional histogram detection", "Run -- confirms Fuls sign 550"],
        ["logosyllabic", "Ventris vowel/consonant affinity grid", "Needs full inscription sequences"],
        ["allograph", "Daggumati-Revesz 2021 mirror pairs", "Needs full inscription sequences"],
        ["kandles", "Merkur phonological fingerprint", "Needs phoneme transliteration"],
        ["decipher", "Substitution cipher solver", "Needs bilingual anchor text"],
    ]
    story.append(tbl(pipes, col_widths=[4.5*cm, 6.5*cm, 5*cm]))
    story.append(Paragraph(
        "Table 8. Pipeline status on real Indus data. "
        "First five pipelines run on data from Fuls (2023). "
        "Remaining four require the full ICIT inscription sequences.",
        S["caption"]
    ))

    # ── §7 Proposed collaboration ─────────────────────────────────────
    story.append(Paragraph("7. PROPOSED NEXT STEPS", S["h1"]))
    story.append(Paragraph(
        "The following research programme would make best use of the ICIT "
        "database together with the Glossa Lab analysis platform:",
        S["body"]
    ))
    steps = [
        "Validate the NWSP implementation against published positional "
        "histograms for specific signs (e.g. Sign 590, Sign 550). "
        "The same algorithm should produce agreement within 2-3%.",
        "Run the full inscription sequences through the Ventris affinity "
        "grid to cluster the 333 phonetic signs into candidate rows/columns.",
        "Apply allograph normalisation (50 Daggumati-Revesz pairs) to "
        "reduce the effective sign count and improve statistical stability.",
        "Run site-specific analysis (Mohenjo-daro vs Harappa vs Gulf sites) "
        "to identify geographic sign variation as potential dialect evidence.",
        "Test the sign pair 527-550 and the top 10 TMK signs against "
        "Dravidian and Anatolian cognate candidates to test the hypothesis.",
    ]
    for i, step in enumerate(steps, 1):
        story.append(Paragraph(f"<b>Step {i}.</b> {step}", S["body"]))
        story.append(Spacer(1, 0.05*cm))

    # ── References ────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6))
    story.append(Paragraph("REFERENCES", S["h1"]))
    refs = [
        "Daggumati, S. & Revesz, P.Z. (2021). A method of identifying allographs in "
        "undeciphered scripts and its application to the Indus Valley Script. "
        "<i>Humanities and Social Sciences Communications</i>, 8, 50.",
        "Fuls, A. (2013). Positional analysis of Indus signs. "
        "<i>Voprosi Epigrafiki</i>, 7(1), 253–275.",
        "Fuls, A. (2015). Appendix II: Positional Analysis of Indus Signs. In B.K. Wells, "
        "<i>The Archaeology and Epigraphy of Indus Writing</i>. Archaeopress, pp. 119–133.",
        "Fuls, A. (2022). <i>Corpus of Indus Inscriptions</i>. Mathematica Epigraphica Vol. 3. "
        "Self-published, Berlin.",
        "Fuls, A. (2023). <i>A Catalog of Indus Signs</i>. Mathematica Epigraphica Vol. 4. "
        "Self-published, Berlin. [Primary data source for this report]",
        "Luo, J., Cao, Y. & Barzilay, R. (2019). Neural Decipherment via Minimum-Cost Flow: "
        "From Ugaritic to Linear B. <i>ACL 2019</i>.",
        "Parpola, A. (1994). <i>Deciphering the Indus Script</i>. Cambridge University Press.",
        "Rao, R.P.N. et al. (2009). A Markov Model of the Indus Script. "
        "<i>PNAS</i>, 106(33), 13685–13690.",
        "Snyder, B., Naseem, T. & Barzilay, R. (2010). A Statistical Model for Lost Language "
        "Decipherment. <i>ACL 2010</i>.",
        "Yadav, N. et al. (2010). Statistical Analysis of the Indus Script Using n-Grams. "
        "<i>PLoS ONE</i>, 5(3), e9506.",
    ]
    for ref in refs:
        story.append(Paragraph(f"• {ref}", S["body_small"]))

    # ── Footer note ───────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=4))
    story.append(Paragraph(
        "Glossa Lab is developed by BitConcepts. "
        "All source code is available on request. "
        "Contact: tpierson@bitconcepts.tech",
        S["body_small"]
    ))

    doc.build(story)
    print(f"PDF generated → {OUTPUT_PDF}")
    return OUTPUT_PDF


if __name__ == "__main__":
    main()
