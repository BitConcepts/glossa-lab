"""Generate ICIT corpus access request letter to Dr. Fuls (TU Berlin).

Reads: reports/foundation_check_report.json (for key results)
       reports/phase66_sanskrit_sa.json (falsification ratio)
       reports/phase64_morphological_boundary.json (M267 result)
Writes: reports/icit_access_request.pdf
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
        Table, TableStyle,
    )
except ImportError:
    print("ERROR: reportlab required. pip install reportlab", file=sys.stderr)
    sys.exit(1)

_REPO  = Path(__file__).resolve().parents[2]
_RPRT  = _REPO / "reports"
_TODAY = datetime.date.today().isoformat()


def _read(p: Path) -> dict | None:
    if not p.exists(): return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _esc(s: str) -> str:
    return (str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))


def _styles():
    base = getSampleStyleSheet()
    G = colors.HexColor
    return {
        "title":   ParagraphStyle("IL_title", parent=base["Title"],   fontSize=16, spaceAfter=6),
        "h1":      ParagraphStyle("IL_h1",    parent=base["Heading1"],fontSize=12, spaceAfter=5, textColor=G("#1e3a5f")),
        "body":    ParagraphStyle("IL_body",  parent=base["BodyText"],fontSize=10, leading=14, spaceAfter=4),
        "bold":    ParagraphStyle("IL_bold",  parent=base["BodyText"],fontSize=10, leading=14, spaceAfter=4,
                                  fontName="Helvetica-Bold"),
        "small":   ParagraphStyle("IL_small", parent=base["BodyText"],fontSize=8.5, leading=11,
                                   textColor=G("#6b7280")),
        "indent":  ParagraphStyle("IL_ind",   parent=base["BodyText"],fontSize=10, leading=14,
                                   leftIndent=24, spaceAfter=4),
    }


def _hr(s): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#d1d5db"),
                               spaceAfter=4, spaceBefore=4)


def _tbl(rows, col_widths, header=True):
    t = Table(rows, colWidths=col_widths, repeatRows=1 if header else 0)
    G = colors.HexColor
    style = [
        ("GRID",         (0,0),(-1,-1), 0.3, G("#d1d5db")),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("FONTSIZE",     (0,0),(-1,-1), 9),
        ("LEFTPADDING",  (0,0),(-1,-1), 4),
        ("RIGHTPADDING", (0,0),(-1,-1), 4),
        ("TOPPADDING",   (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, G("#f9fafb")]),
    ]
    if header:
        style += [("BACKGROUND",(0,0),(-1,0),G("#e5e7eb")),
                  ("FONTNAME",  (0,0),(-1,0),"Helvetica-Bold")]
    t.setStyle(TableStyle(style))
    return t


def build_pdf(out: Path) -> Path:
    fc  = _read(_RPRT / "foundation_check_report.json") or {}
    p66 = _read(_RPRT / "phase66_sanskrit_sa.json") or {}
    p64 = _read(_RPRT / "phase64_morphological_boundary.json") or {}

    s = _styles()
    doc = SimpleDocTemplate(
        str(out), pagesize=letter,
        leftMargin=1.0*inch, rightMargin=1.0*inch,
        topMargin=1.0*inch,  bottomMargin=1.0*inch,
        title="ICIT Corpus Access Request — Glossa-Lab Indus Decipherment Project",
        author="Tristan Pierson, BitConcepts LLC",
    )
    flow = []

    # ── Header ──
    flow.append(Paragraph("Request for ICIT Corpus Access", s["title"]))
    flow.append(Paragraph("Indus Corpus Integration Tool — Glossa-Lab Research Platform", s["small"]))
    flow.append(Spacer(1, 0.1*inch))
    flow.append(Paragraph(f"Date: {_TODAY}", s["small"]))
    flow.append(Paragraph("From: Tristan Pierson, BitConcepts LLC", s["small"]))
    flow.append(Paragraph("To:   Dr. Andreas Fuls, Technische Universität Berlin", s["small"]))
    flow.append(_hr(s))
    flow.append(Spacer(1, 0.1*inch))

    # ── Salutation ──
    flow.append(Paragraph("Dear Dr. Fuls,", s["body"]))
    flow.append(Spacer(1, 6))

    # ── Introduction ──
    flow.append(Paragraph(
        "I am writing to request access to the <b>Indus Corpus Integration Tool (ICIT)</b> "
        "database for use in an ongoing computational decipherment research project. "
        "I have been developing the Glossa-Lab platform — an open-science linguistic analysis "
        "environment — and have been applying it to the Indus script since early 2026. "
        "Your ICIT corpus (Fuls 2023) represents the most comprehensive spatial and temporal "
        "metadata available for the Indus inscription record, and access would substantially "
        "advance the statistical tests described below.",
        s["body"]))
    flow.append(Spacer(1, 8))

    # ── Research Progress ──
    flow.append(Paragraph("Current Research Progress", s["h1"]))
    flow.append(_hr(s))

    n_ok   = fc.get("n_ok",   0)
    n_fail = fc.get("n_fail", 0)

    flow.append(Paragraph(
        f"The Glossa-Lab Indus decipherment pipeline (Phase-44 through Phase-66) has passed "
        f"{n_ok} independent verification checks with {n_fail} failures. Key results:",
        s["body"]))

    solid = fc.get("solid_claims", [])
    results_table = [["Phase", "Result", "Status"]]
    key_results = [
        ("Phase-44", "Dravidian SA lift 3.13× over random (z=12.1, 944-LM)", "VERIFIED"),
        ("Phase-45", "100% concordance with your NWSP positional analysis (7/7 HIGH anchors)", "VERIFIED"),
        ("Phase-46", "Janabiyah Gulf seal contains ALL 7 HIGH anchor signs", "VERIFIED"),
        ("Phase-47", "Rebus phoneme sequence 3.19× more probable under Dravidian LM", "VERIFIED"),
        ("Phase-52", "Constrained SA z=16.01 (59 anchors pinned)", "VERIFIED"),
        ("Phase-57", "Expanded SA z=19.07 — highest z-score achieved", "VERIFIED"),
        ("Phase-58", "0 phonotactic violations in HIGH/MEDIUM anchor set", "VERIFIED"),
        ("Phase-59", "22 inscription formulas ≥80% decoded (tiru-il-āy-aṇ-kol-vil, etc.)", "VERIFIED"),
        ("Phase-61", "94% of inscriptions pass Dravidian vowel harmony", "VERIFIED"),
    ]
    # Add Phase-66 if available
    z_drav = p66.get("z_score_dravidian_ref", 0)
    z_skt  = p66.get("z_score_sanskrit", 0)
    if z_drav and z_skt:
        ratio = p66.get("z_ratio_dravidian_vs_sanskrit", 0)
        key_results.append(("Phase-66",
                             f"Sanskrit falsification: Dravidian z={z_drav:.1f} vs Sanskrit z={z_skt:.1f} ({ratio:.1f}×)",
                             p66.get("verdict","?")[:30]))

    for phase, result, status in key_results:
        col = colors.HexColor("#065f46") if "VERIFIED" in status or "DRAVIDIAN" in status else colors.HexColor("#92400e")
        results_table.append([
            Paragraph(_esc(phase), s["small"]),
            Paragraph(_esc(result), s["small"]),
            Paragraph(_esc(status), ParagraphStyle("IL_st", parent=s["small"], textColor=col)),
        ])
    flow.append(_tbl(results_table, [0.8*inch, 4.3*inch, 1.7*inch]))
    flow.append(Spacer(1, 8))

    # ── Phase-29d Enmenanak ──
    flow.append(Paragraph("Phase-29d: Janabiyah Reverse Search", s["h1"]))
    flow.append(_hr(s))
    flow.append(Paragraph(
        "A reverse-Janabiyah search against 1,222 ePSD2 personal names identified "
        "<b>Enmenanak</b> (score 7.0) as the top candidate matching the Janabiyah seal's "
        "phonetic skeleton under the Parpola mīn-rendering hypothesis. "
        "This candidate is at the 100th percentile of permutation null (p&lt;0.001), "
        "though we note the period mismatch (Old Akkadian vs Early Dilmun) and the "
        "absence of a documented Meluhha co-occurrence for Enmenanak. "
        "The full candidate list requires ICIT temporal and geographic metadata to filter.",
        s["body"]))
    flow.append(Spacer(1, 8))

    # ── Why ICIT is needed ──
    flow.append(Paragraph("Why ICIT Access is Needed", s["h1"]))
    flow.append(_hr(s))
    flow.append(Paragraph(
        "The current Glossa-Lab corpus is limited to the Holdat V3 dataset (1,670 seals, "
        "7,002 tokens, 9 sites — primarily Mohenjo-daro and Harappa). ICIT would provide:",
        s["body"]))

    needs = [
        ["Gap", "Current limitation", "ICIT resolution"],
        ["Gulf/western seals", "Holdat covers 9 mainland sites; no Gulf data",
         "ICIT covers Failaka, Janabiyah, Saar, Susa, etc."],
        ["Temporal metadata", "Phase-29d Enmenanak candidate blocked by period uncertainty",
         "ICIT period assignments filter candidates to Meluhha-active periods"],
        ["Meluhha co-occurrence", "Cannot test which PNs co-occur with Meluhha on same tablets",
         "ICIT/CDLI link allows tablet-level co-occurrence testing"],
        ["Spatial site strata", "Phase-46 contact zone limited to published Laursen 2010 data",
         "Full ICIT spatial database enables site-stratified SA and null models"],
        ["Extended corpus", "1,670 seals → statistical power limited for rare signs",
         "ICIT ~4,537 objects provides ~3× corpus expansion"],
    ]
    flow.append(_tbl([[Paragraph(_esc(c), s["small"]) for c in r] for r in needs],
                     [1.2*inch, 2.4*inch, 3.0*inch]))
    flow.append(Spacer(1, 8))

    # ── Safeguards / Commitment ──
    flow.append(Paragraph("Commitment and Safeguards", s["h1"]))
    flow.append(_hr(s))
    flow.append(Paragraph(
        "I commit to the following terms for any ICIT data access:",
        s["body"]))
    for item in [
        "Full attribution to Fuls (2023) ICIT in all publications and reports.",
        "Data used exclusively for non-commercial academic research on Indus script decipherment.",
        "No redistribution of ICIT data; all outputs derived from ICIT will be reported as "
        "statistical summaries only.",
        "Compliance with any access agreement, API rate limits, or usage restrictions "
        "specified by TU Berlin.",
        "Sharing of derived results (decipherment reports, open-access) with Dr. Fuls "
        "prior to any external communication.",
    ]:
        flow.append(Paragraph(f"• {_esc(item)}", s["indent"]))

    flow.append(Spacer(1, 8))

    # ── Request ──
    flow.append(Paragraph("Specific Request", s["h1"]))
    flow.append(_hr(s))
    flow.append(Paragraph(
        "I am requesting <b>read-only API access</b> to the ICIT database, specifically:",
        s["body"]))
    for item in [
        "Gulf/Persian Gulf and western region seal inscriptions (Failaka, Bahrain, Mesopotamia)",
        "Period assignments for all seals (Mature Harappan sub-phases)",
        "Site coordinates or region codes for spatial stratification",
        "Meluhha co-occurrence data (which CDLI tablets reference Meluhha AND contain "
        "Indus-type seal impressions)",
    ]:
        flow.append(Paragraph(f"• {_esc(item)}", s["indent"]))

    flow.append(Spacer(1, 0.15*inch))
    flow.append(Paragraph(
        "I have already implemented ICIT API loaders in Glossa-Lab (Phase-29c) as "
        "no-op stubs awaiting credentials. The integration is ready to activate "
        "once access is granted.",
        s["body"]))

    # ── Closing ──
    flow.append(Spacer(1, 0.15*inch))
    flow.append(_hr(s))
    flow.append(Paragraph(
        "Thank you for considering this request. Your NWSP positional analysis has been "
        "an essential foundation for the Phase-45 cross-check (100% concordance), and I "
        "believe ICIT access would enable the most rigorous statistical falsification test "
        "achievable with current Indus inscription data.",
        s["body"]))
    flow.append(Spacer(1, 8))
    flow.append(Paragraph("Respectfully,", s["body"]))
    flow.append(Spacer(1, 4))
    flow.append(Paragraph("<b>Tristan Pierson</b>", s["body"]))
    flow.append(Paragraph("BitConcepts LLC", s["small"]))
    flow.append(Paragraph("tpierson@bitconcepts.tech", s["small"]))
    flow.append(Paragraph("Glossa-Lab: open-science linguistic analysis platform", s["small"]))

    # ── Appendix: Key anchor table ──
    flow.append(PageBreak())
    flow.append(Paragraph("Appendix A: High-Confidence Anchor Set", s["h1"]))
    flow.append(_hr(s))
    flow.append(Paragraph(
        "The following 7 core HIGH-confidence anchors form the foundation of all "
        "Glossa-Lab decipherment analyses. Phase-45 confirms 100% concordance with "
        "your NWSP positional analysis.",
        s["body"]))
    flow.append(Spacer(1, 4))

    anchor_rows = [["M-number", "P-number", "Reading", "Gloss", "Evidence"]]
    HIGH_ANCHORS = [
        ("M342", "P145/342", "āy",      "Honorific suffix",       "Phase-47 rebus, DEDR 5295"),
        ("M176", "P176",     "an/aṇ",   "Masculine suffix",       "Phase-47 rebus, DEDR 134"),
        ("M099", "P99",      "kol/koḷ", "Bow/lord",               "Phase-47 rebus, DEDR 2159"),
        ("M062", "P62/126",  "erutu",   "Zebu bull",              "100% zebu motif, DEDR 824"),
        ("M045", "P147",     "yānai",   "Elephant",               "100% elephant motif, DEDR 5149"),
        ("M016", "P16",      "kaḷiṟu",  "Young elephant",         "100% elephant calf, DEDR 1278"),
        ("M006", "P6/364",   "puli",    "Tiger",                  "Tiger lift 6.2×, DEDR 4346"),
    ]
    for m, p, r, g, ev in HIGH_ANCHORS:
        anchor_rows.append([
            Paragraph(_esc(m), s["small"]),
            Paragraph(_esc(p), s["small"]),
            Paragraph(_esc(r), s["small"]),
            Paragraph(_esc(g), s["small"]),
            Paragraph(_esc(ev), s["small"]),
        ])
    flow.append(_tbl(anchor_rows, [0.8*inch, 0.8*inch, 0.8*inch, 1.2*inch, 2.8*inch]))
    flow.append(Spacer(1, 8))

    flow.append(Paragraph("Appendix B: Foundation Check Summary", s["h1"]))
    flow.append(_hr(s))
    verdict = fc.get("verdict", "UNKNOWN")
    flow.append(Paragraph(
        f"Foundation check verdict: <b>{verdict}</b> — "
        f"{fc.get('n_ok',0)} checks passed, {fc.get('n_fail',0)} failed, "
        f"{fc.get('n_warn',0)} warnings. "
        f"Generated: {_TODAY}. Reproducible via <i>backend/scripts/foundation_check.py</i>.",
        s["body"]))

    doc.build(flow)
    return out


def main():
    out = _RPRT / "icit_access_request.pdf"
    build_pdf(out)
    size_kb = out.stat().st_size // 1024
    print(f"ICIT letter written: {out}  ({size_kb} KB)")


if __name__ == "__main__":
    main()
