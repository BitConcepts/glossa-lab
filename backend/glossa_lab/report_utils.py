"""Safe ReportLab PDF generation utilities for Glossa Lab.

RULES (enforced by this module):
  R1  Only use fonts that are guaranteed available in ReportLab:
        Helvetica, Helvetica-Bold, Helvetica-Oblique, Helvetica-BoldOblique
        Times-Roman, Times-Bold, Times-Italic, Times-BoldItalic
        Courier, Courier-Bold, Courier-Oblique, Courier-BoldOblique
      → NO Unicode scripts (Tamil, Arabic, Devanagari, CJK …) in plain strings.
        Use ASCII romanisation inside PDFs (e.g. '-um' not 'உம்').

  R2  Table cells MUST be Paragraph objects, not bare strings.
      Bare strings cannot wrap or render markup; Paragraph objects handle
      both.  Use the convenience function `pc()` from this module.

  R3  Never use raw '\\n' in table cell strings.
      Use '<br/>' inside the Paragraph markup instead.

  R4  Every ParagraphStyle MUST set 'leading' explicitly.
      Leading = line height in points.  Omitting it can cause line overlap
      when the style inherits from a parent whose leading was calculated
      from a different fontSize.  Minimum: leading = fontSize * 1.35.

  R5  Table column widths must sum to <= available_page_width.
      Available width for A4 with 2.5 cm margins each side:
        (21.0 - 2*2.5) cm = 16.0 cm = ~453 pt.
      Always verify: sum(colWidths) <= 16*cm.

  R6  When calling t.setStyle() after initial construction, use
      TableStyle([…]) with ALL intended styles — the method REPLACES
      the existing style, not merges it.  Pass a combined style list.
"""

from __future__ import annotations

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ── Page geometry ──────────────────────────────────────────────────────────────

PAGE_WIDTH, PAGE_HEIGHT = A4            # 595.3 × 841.9 pt
MARGIN = 2.5 * cm
BODY_WIDTH = PAGE_WIDTH - 2 * MARGIN   # ~453 pt / 16 cm

# ── Colour palette ─────────────────────────────────────────────────────────────

C_NAVY   = colors.HexColor("#1e3a5f")
C_BLUE   = colors.HexColor("#2563eb")
C_GREY   = colors.HexColor("#374151")
C_LGREY  = colors.HexColor("#9ca3af")
C_ROW0   = colors.white
C_ROW1   = colors.HexColor("#f8fafc")
C_GRID   = colors.HexColor("#e5e7eb")
C_GREEN  = colors.HexColor("#dcfce7")
C_AMBER  = colors.HexColor("#fef3c7")
C_RED    = colors.HexColor("#fee2e2")


# ── Style factory ──────────────────────────────────────────────────────────────

def make_styles() -> dict[str, ParagraphStyle]:
    """Return a dict of consistently-spaced named styles.

    All styles have an explicit `leading` value (R4).
    """
    base = ParagraphStyle(
        "GlossaBase",
        fontName="Helvetica",
        fontSize=10,
        leading=14,          # R4: 10 * 1.4 = 14
        spaceAfter=5,
        alignment=TA_LEFT,
    )

    def s(name: str, **kw) -> ParagraphStyle:
        return ParagraphStyle(name, parent=base, **kw)

    return {
        "title": s("GTitle", fontSize=17, leading=24, alignment=TA_CENTER,
                   spaceAfter=6, textColor=C_NAVY, fontName="Helvetica-Bold"),
        "subtitle": s("GSub", fontSize=9, leading=12, alignment=TA_CENTER,
                      spaceAfter=3, textColor=C_LGREY),
        "h1": s("GH1", fontSize=13, leading=18, spaceAfter=5, spaceBefore=10,
                textColor=C_NAVY, fontName="Helvetica-Bold"),
        "h2": s("GH2", fontSize=11, leading=15, spaceAfter=4, spaceBefore=8,
                textColor=C_BLUE, fontName="Helvetica-Bold"),
        "h3": s("GH3", fontSize=10, leading=14, spaceAfter=3, spaceBefore=6,
                textColor=C_GREY, fontName="Helvetica-Bold"),
        "body": s("GBody", fontSize=10, leading=14, spaceAfter=5,
                  alignment=TA_JUSTIFY),
        "body_left": s("GBodyL", fontSize=10, leading=14, spaceAfter=5),
        "caption": s("GCap", fontSize=8, leading=11, textColor=C_LGREY,
                     alignment=TA_CENTER, spaceAfter=6),
        "cell": s("GCell", fontSize=8, leading=11),
        "cell_bold": s("GCellB", fontSize=8, leading=11,
                       fontName="Helvetica-Bold"),
        "code": s("GCode", fontSize=8, leading=11, fontName="Courier",
                  leftIndent=6, spaceAfter=5),
        "bullet": s("GBullet", fontSize=10, leading=14, spaceAfter=3,
                    leftIndent=12, firstLineIndent=-12),
    }


# ── Paragraph helpers ──────────────────────────────────────────────────────────

def p(text: str, style: ParagraphStyle) -> Paragraph:
    """Create a Paragraph from text (may contain basic HTML markup)."""
    return Paragraph(text, style)


def pc(text: str, style: ParagraphStyle | None = None) -> Paragraph:
    """Create a Paragraph suitable for use in a table cell.

    Uses the 'cell' style if no style provided.
    text may contain '<br/>' for line breaks (R3: no raw '\\n').
    """
    if style is None:
        style = make_styles()["cell"]
    # Safety: convert any stray bare newlines to <br/>
    text = text.replace("\n", "<br/>")
    return Paragraph(text, style)


def sp(n: float = 1.0) -> Spacer:
    """Vertical spacer.  n × 0.3 cm."""
    return Spacer(1, n * 0.3 * cm)


def hr(color: colors.Color = C_GRID) -> HRFlowable:
    """Horizontal rule."""
    return HRFlowable(width="100%", color=color, thickness=0.5)


# ── Table builder ──────────────────────────────────────────────────────────────

def safe_tbl(
    data: list[list],
    col_widths: list[float],
    header_color: colors.Color = C_NAVY,
    row_colors: list[colors.Color] | None = None,
    highlight_rows: dict[int, colors.Color] | None = None,
    font_size: int = 8,
) -> Table:
    """Build a safe ReportLab table.

    Rules enforced:
      - All cells are converted to Paragraph objects (R2).
      - Column widths are validated against BODY_WIDTH (R5).
      - A single consolidated TableStyle is set (R6).

    Args:
        data:          Row-major list of rows; first row = header.
        col_widths:    Column widths in points.  Must sum to <= BODY_WIDTH.
        header_color:  Background colour for the header row.
        row_colors:    Alternating row background colours (default: white / light grey).
        highlight_rows: {row_index: color} to override specific data rows.
        font_size:     Font size for all cells.
    """
    # R5: validate column widths
    total = sum(col_widths)
    if total > BODY_WIDTH + 2:  # 2 pt tolerance for rounding
        raise ValueError(
            f"Table column widths sum to {total:.1f} pt "
            f"but body width is only {BODY_WIDTH:.1f} pt. "
            f"Reduce column widths by {total - BODY_WIDTH:.1f} pt."
        )

    cell_style = ParagraphStyle(
        "SafeCell",
        fontName="Helvetica",
        fontSize=font_size,
        leading=int(font_size * 1.4),
        wordWrap="LTR",
    )
    bold_cell = ParagraphStyle(
        "SafeCellBold",
        parent=cell_style,
        fontName="Helvetica-Bold",
    )

    # R2: wrap all cells in Paragraph objects
    safe_data = []
    for ri, row in enumerate(data):
        safe_row = []
        for ci, cell in enumerate(row):
            if isinstance(cell, Paragraph):
                safe_row.append(cell)
            else:
                text = str(cell).replace("\n", "<br/>")  # R3
                sty = bold_cell if ri == 0 else cell_style
                safe_row.append(Paragraph(text, sty))
        safe_data.append(safe_row)

    t = Table(safe_data, colWidths=col_widths, repeatRows=1)

    # R6: single consolidated style
    if row_colors is None:
        row_colors = [C_ROW0, C_ROW1]

    style_cmds = [
        # Header
        ("BACKGROUND",   (0, 0), (-1, 0),  header_color),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        # Grid
        ("GRID",         (0, 0), (-1, -1), 0.4, C_GRID),
        # Alignment / padding
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        # Alternating rows
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), row_colors),
    ]

    # Highlighted rows
    if highlight_rows:
        for row_idx, color in highlight_rows.items():
            style_cmds.append(("BACKGROUND", (0, row_idx), (-1, row_idx), color))

    t.setStyle(TableStyle(style_cmds))
    return t


# ── Unicode safety helper ──────────────────────────────────────────────────────

# Map of non-Latin characters that appear in our research to safe ASCII equivalents.
# R1: only Latin-1 characters may appear in PDF text rendered by built-in fonts.
_UNICODE_REPLACEMENTS: dict[str, str] = {
    # Tamil script → romanised equivalents
    "உம்":  "[-um]",
    "ஏ/ஈ":  "[-e/-ee]",
    "ஏ":    "[-e]",
    "ஈ":    "[-ee]",
    "கு":   "[-ku]",
    "இல்":  "[-il]",
    "அல்":  "[-al]",
    "அன்":  "[-an]",
    "ஐ":    "[-ai]",
    "இன்":  "[-in]",
    "ஒடு":  "[-odu]",
    "வன்":  "[-van]",
    "த்து": "[-ttu]",
    "அர்":  "[-ar]",
    # Common Unicode punctuation → ASCII
    "\u2014": "--",   # em dash
    "\u2013": "-",    # en dash
    "\u2019": "'",    # right single quote
    "\u2018": "'",    # left single quote
    "\u201c": '"',    # left double quote
    "\u201d": '"',    # right double quote
    "\u2265": ">=",   # >=
    "\u2264": "<=",   # <=
    "\u00e9": "e",    # é
    "\u00e8": "e",    # è
    "\u0113": "e",    # ē (macron e)
    "\u012b": "i",    # ī
    "\u016b": "u",    # ū
    "\u1e93": "z",    # ẓ
    "\u1e6d": "t",    # ṭ
    "\u1e47": "n",    # ṇ
    "\u1e37": "l",    # ḷ
    "\u1e5f": "r",    # ṟ
    "\u1e49": "n",    # ṉ
    "\u00f1": "n",    # ñ
}


def safe_text(text: str) -> str:
    """Replace non-Latin-1 characters with safe ASCII equivalents (R1).

    Call this on ALL strings before passing to Paragraph() or table cells.
    """
    for src, dst in _UNICODE_REPLACEMENTS.items():
        text = text.replace(src, dst)
    # Final safety pass: encode to latin-1 with replace to catch anything missed
    return text.encode("latin-1", errors="replace").decode("latin-1")


def sp_text(text: str, style: ParagraphStyle) -> Paragraph:
    """Create a safe Paragraph (applies safe_text first)."""
    return Paragraph(safe_text(text), style)
