"""
Generate a clean PDF from fuls_research_brief_may2026.md using ReportLab.
Per P1-P7: Latin-1 safe fonts, Paragraph objects, explicit leading.
Output: reports/fuls_research_brief_may2026.pdf
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.report_utils import make_styles, safe_text  # noqa: E402

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
        TableStyle,
    )
    from reportlab.platypus.flowables import KeepTogether
except ImportError:
    print("ERROR: reportlab not installed. Run: pip install reportlab")
    sys.exit(1)

SRC = REPO / "reports" / "fuls_research_brief_may2026.md"
OUT = REPO / "reports" / "fuls_research_brief_may2026.pdf"

# ── Build PDF ──────────────────────────────────────────────────────────────

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=2.5 * cm,
    rightMargin=2.5 * cm,
    topMargin=2.5 * cm,
    bottomMargin=2.5 * cm,
    title="Glossa Lab Research Brief — Dr. Fuls (May 2026)",
    author="Tristen Pierson / Layer1Labs Silicon",
)

from reportlab.lib.styles import ParagraphStyle  # noqa: E402

styles = make_styles()

# Override heading styles with visible colors
styles["h1"] = ParagraphStyle(
    "h1", fontName="Helvetica-Bold", fontSize=15, leading=20,
    textColor=colors.HexColor("#1e3a5f"), spaceBefore=8, spaceAfter=4,
)
styles["h2"] = ParagraphStyle(
    "h2", fontName="Helvetica-Bold", fontSize=12, leading=16,
    textColor=colors.HexColor("#2563eb"), spaceBefore=6, spaceAfter=2,
)
styles["h3"] = ParagraphStyle(
    "h3", fontName="Helvetica-Bold", fontSize=10, leading=14,
    textColor=colors.HexColor("#1e40af"), spaceBefore=4, spaceAfter=2,
)
styles["cell_white"] = ParagraphStyle(
    "cell_white", fontName="Helvetica-Bold", fontSize=7.5, leading=11,
    textColor=colors.white,
)

story = []

text = SRC.read_text(encoding="utf-8")
lines = text.split("\n")

def _safe(s):
    # Additional safety: strip non-latin chars that reportlab can't handle
    return safe_text(s.replace("ī", "i").replace("ḷ", "l").replace("ḻ", "l")
                      .replace("ṉ", "n").replace("ḵ", "k").replace("ā", "a")
                      .replace("ū", "u").replace("ṭ", "t").replace("ṇ", "n")
                      .replace("\u2192", "->").replace("\u2190", "<-")
                      .replace("\u00b7", "·").replace("×", "x")
                      .replace("\u2264", "<=").replace("\u2265", ">=")
                      .replace("delta", "delta").replace("|delta|", "|delta|")
                      .replace("\u0394", "delta").replace("\u2014", "--")
                      .replace("\u2013", "-"))

def _para(txt, style_name="Normal"):
    return Paragraph(_safe(txt), styles[style_name])

def _flush_table(story, rows, styles):
    if not rows:
        return
    col_count = max(len(r) for r in rows)
    rows = [r + [""] * (col_count - len(r)) for r in rows]
    header = [Paragraph(f"<b>{_safe(c)}</b>", styles["cell_white"]) for c in rows[0]]
    body = [[Paragraph(_safe(c), styles["cell"]) for c in r] for r in rows[1:]]
    from reportlab.lib.units import cm as _cm  # noqa: PLC0415
    from reportlab.lib.pagesizes import A4 as _A4  # noqa: PLC0415
    body_w = _A4[0] - 5.0 * _cm
    col_w = body_w / col_count
    tbl = Table([header] + body, colWidths=[col_w] * col_count, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("FONTSIZE",   (0, 0), (-1, -1), 7.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f9fafb"), colors.white]),
        ("GRID",       (0, 0), (-1, -1), 0.3, colors.HexColor("#e5e7eb")),
        ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING",   (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 6))


i = 0
table_rows = []
in_table = False

while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Section headers
    if stripped.startswith("# ") and not stripped.startswith("## "):
        story.append(Spacer(1, 6))
        story.append(_para(stripped[2:], "h1"))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563eb")))
        story.append(Spacer(1, 4))
    elif stripped.startswith("## "):
        if in_table:
            _flush_table(story, table_rows, styles)
            table_rows = []
            in_table = False
        story.append(Spacer(1, 8))
        story.append(_para(stripped[3:], "h2"))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#9ca3af")))
        story.append(Spacer(1, 2))
    elif stripped.startswith("### "):
        if in_table:
            _flush_table(story, table_rows, styles)
            table_rows = []
            in_table = False
        story.append(Spacer(1, 4))
        story.append(_para(stripped[4:], "h3"))
    # Table rows
    elif stripped.startswith("|"):
        cells = [c.strip() for c in stripped.split("|")[1:-1]]
        if all(set(c) <= set("- :|") for c in cells):
            i += 1
            continue  # separator row
        if not in_table:
            in_table = True
            table_rows = []
        table_rows.append(cells)
    else:
        if in_table:
            _flush_table(story, table_rows, styles)
            table_rows = []
            in_table = False

        if not stripped:
            story.append(Spacer(1, 4))
        elif stripped.startswith("- ") or stripped.startswith("* "):
            story.append(_para("• " + stripped[2:], "body"))
        elif stripped.startswith("**") and stripped.endswith("**"):
            story.append(_para(stripped[2:-2], "h3"))
        elif stripped.startswith("*") and stripped.endswith("*"):
            story.append(_para(stripped[1:-1], "body"))
        elif stripped.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.3, color=colors.HexColor("#e5e7eb")))
        else:
            # Inline bold: **text** → <b>text</b>
            rendered = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", stripped)
            rendered = re.sub(r"\*(.+?)\*", r"<i>\1</i>", rendered)
            rendered = re.sub(r"`(.+?)`", r"<font name='Courier'>\1</font>", rendered)
            story.append(Paragraph(_safe(rendered), styles["body"]))

    i += 1

if in_table:
    _flush_table(story, table_rows, styles)


doc.build(story)
print(f"PDF written: {OUT}")
print(f"Size: {OUT.stat().st_size:,} bytes")
