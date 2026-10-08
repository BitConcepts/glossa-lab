#!/usr/bin/env python3
"""Phase-123: Wells segmentation witness table builder.

Builds the machine-readable witness table (CSV + JSON) recording, for each
of the 113 CANDIDATE anchors and the 44 ``pending_non_sa_validation``
anchors in ``backend/reports/INDUS_FINAL_ANCHORS.json`` (157 distinct
Mahadevan-numbered signs), how Bryan K. Wells's grapheme segmentation
(MA thesis, University of Calgary, 1998; PhD thesis, Harvard, 2006) treats
the corresponding sign: SPLIT / MERGE / SAME / NOT-COVERED / INDETERMINATE.

WITNESS FRAMING (hard): this table is a witness statement, not an
adjudication. It records Wells's treatment and its *conditional*
implication only. It makes no recommendation to adopt Wells's
segmentation and asserts no anchor-status implication.

Correspondence methods (documented in the companion memo,
``reports/phase123_wells_segmentation_witness.md``):

1. REGISTRY — the program's held ``canonical_sign_registry.csv``
   (mayig CISI digitisation, MIT; per-grapheme Wells (2015) cross-match),
   aggregated Mahadevan <-> Wells. The Wells numbering in that registry is
   the Wells/ICIT list numbering whose thesis-era form is printed in the
   PhD thesis, Figure 3.2 (thesis pp. 90-92; numbers run to 958 with gaps
   left by the list's compression from >900 to 676 graphemes, PhD thesis
   pp. 67-68).
2. MA-FIG36 — Wells MA thesis Figure 3.6 (thesis p. 77), a direct
   Mahadevan (1977) <-> Wells (1997) concordance for the grapheme groups
   Wells redefined. Applies to M178, M213, M400 among the targets.
3. GLYPH — Phase-123 hand glyph-matching of the Mahadevan sign image
   (``backend/static/signs/M*.png``) against the PhD Figure 3.2 plates /
   Appendix I per-sign sheets, for signs absent from the registry.
4. HAND-VERIFICATION — 20 table rows were hand-verified against the PhD
   plates (see ``HAND_VERIFICATION`` below and the GLYPH matches):
   17 glyph-consistent (one, M389, with a recorded cross-source
   conflict), 2 partial, 1 discrepancy (M293). The attestation co-occurrence method
   (MA Appendix 1 artifact lists vs ICIT per-artifact Mahadevan sets) was
   attempted and rejected: the MA text layer is too noisy and the
   Jaccard scores were uniformly low (best 0.22); it is not used.

Outputs:
  data/crosswalks/wells_segmentation_witness_v1.csv
  data/crosswalks/wells_segmentation_witness_v1.json

Deterministic: two runs produce byte-identical outputs.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_JSON = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
REGISTRY_CSV = REPO / "data" / "crosswalks" / "canonical_sign_registry.csv"
OUT_CSV = REPO / "data" / "crosswalks" / "wells_segmentation_witness_v1.csv"
OUT_JSON = REPO / "data" / "crosswalks" / "wells_segmentation_witness_v1.json"

# --- Hand glyph matches for signs absent from the registry -----------------
# Mahadevan sign -> (Wells PhD number, thesis source, note)
GLYPH_MATCHES: dict[str, tuple[str, str, str]] = {
    "M153": ("520", "PhD 2006, Fig. 3.2, thesis p. 91",
             "Plain stemmed arrow; plate sign 520 is the plain-arrow grapheme."),
    "M213": ("092", "PhD 2006, Fig. 3.2, thesis p. 90; MA 1998, Fig. 3.6, thesis p. 77 (Wells 1997 no. 48)",
             "Inverted-triangle-on-stem glyph located in both theses' lists."),
    "M274": ("866", "PhD 2006, Appendix I per-sign sheet, thesis p. 278",
             "Diamond with a star mark above each top corner; Appendix I sheet 866 glyph matches. "
             "Fig. 3.2 plate rendering of 866 is smaller and less clear."),
    "M369": ("782", "PhD 2006, Fig. 3.2, thesis p. 92",
             "U-base with three loop-topped stems; plate sign 782 matches."),
    "M378": ("837", "PhD 2006, Fig. 3.2, thesis p. 92",
             "Plain oval with a single central vertical stroke; plate sign 837 matches exactly."),
    "M389": ("805", "PhD 2006, Fig. 3.2, thesis p. 92",
             "Oval with a three-pronged fork rising from the base inside; plate sign 805 matches by glyph, "
             "but the held registry also assigns W805 to M387 - a cross-source disagreement recorded, not resolved."),
    "M396": ("372", "PhD 2006, Fig. 3.2, thesis p. 91",
             "Stemmed circle with central dot; plate sign 372 matches modulo font rendering "
             "(thesis font draws a dot where the Mahadevan font draws a small inner oval)."),
}

# Signs whose distinctive glyph was searched for across all three PhD
# Fig. 3.2 plates and the MA Fig. 3.6 table and not found.
NOT_COVERED: dict[str, str] = {
    "M312": "A plain wide arch (single broad curve) appears nowhere in the PhD Fig. 3.2 plates "
            "(thesis pp. 90-92), whose arc signs are all narrow parenthesis/C forms (signs 900-921).",
    "M365": "A plain open V appears nowhere in the PhD Fig. 3.2 plates (thesis pp. 90-92); "
            "the 700 block is U-shaped jars/cups and no V grapheme is listed.",
}

# --- Hand verification record (Phase-123, against PhD Fig. 3.2 plates) -----
# sign -> (outcome, note)
HAND_VERIFICATION: dict[str, tuple[str, str]] = {
    "M127": ("verified", "W440 plate glyph (squared hook) matches the Mahadevan glyph."),
    "M149": ("partial", "W690 is the X-family grapheme; the Mahadevan glyph's chevron end-treatment is rendered more simply in the Wells font."),
    "M213": ("verified", "Glyph match in both theses (see GLYPH_MATCHES)."),
    "M254": ("verified", "W526 (two-band banner on a stem) matches modulo mirror orientation (seal vs impression drawing convention); W527 is the unbanded ladder variant."),
    "M262": ("verified", "W860 Appendix I sheet (thesis p. 278) shows the diamond with the small mark at the right corner, matching the Mahadevan glyph's corner fork."),
    "M287": ("verified", "W900 is the single-arc grapheme; thickness difference is font weight only."),
    "M293": ("discrepancy", "Registry assigns W920, whose Fig. 3.2 plate glyph is a plain thin arc; the Mahadevan glyph carries a closed loop on the arc. Wells's own PhD discussion (thesis pp. 73-75, Tables 3.1-3.2) treats signs 920 and 921 as separate graphemes whose distinction is subtle; which of the pair carries the looped form could not be settled from the plate rendering. Row kept as the registry states it; discrepancy recorded."),
    "M304": ("verified", "W890 plate glyph is the plain D outline, matching."),
    "M332": ("verified", "W734 (U with fringe below the base) matches the Mahadevan glyph; W732 is the side-rooted variant."),
    "M345": ("verified", "W745-W747 are the jar graphemes distinguished by rim marking, the family to which the Mahadevan glyph (jar with central rim teeth) belongs."),
    "M369": ("verified", "Glyph match (see GLYPH_MATCHES)."),
    "M378": ("verified", "Glyph match (see GLYPH_MATCHES)."),
    "M383": ("verified", "W815 (oval containing a barred compartment) matches the Mahadevan glyph's oval-with-internal-divisions form; W816 is its plainer variant."),
    "M389": ("verified_with_conflict", "Cross-source conflict recorded in the row note."),
    "M401": ("partial", "W375 is the paired-loop family; the Mahadevan glyph's barred knot form is not reproduced exactly in the Wells font rendering."),
    "M405": ("verified", "W841 (overlapping ovals with a small external mark at right) matches the Mahadevan glyph."),
    "M416": ("verified", "W217 plate glyph (barred figure-8 between verticals, |8|) matches the Mahadevan glyph exactly."),
}

INDETERMINATE_OVERRIDES: dict[str, str] = {
    "M033": ("Chain-only lead: the program's ICIT conversion layer aligns this sign with Wells/ICIT "
             "code 143 (4 tokens, kind 'chain'), a correspondence that runs through the unmerged "
             "Phase-122 crosswalk chain (PR #81). Phase-123 does not depend on unmerged artifacts "
             "in committed outputs, so the row is recorded indeterminate with the chain noted as an "
             "open lead for a future spec."),
    "M126": ("Chain-only lead: the program's ICIT conversion layer aligns this sign with Wells/ICIT "
             "codes 016 (49 tokens) and 006 (7 tokens), both kind 'chain' via the unmerged "
             "Phase-122 crosswalk chain (PR #81). Recorded indeterminate for the same reason as M033; "
             "if the chain correspondence were confirmed, the two-code alignment would indicate a "
             "SPLIT treatment - stated here as a conditional lead only, not a finding."),
}

INDETERMINATE_REASON = (
    "No correspondence in the held canonical registry, no entry in the MA thesis "
    "Fig. 3.6 concordance, and the glyph could not be located with confidence in the "
    "PhD Fig. 3.2 plates; treatment not determinable from the theses as held. "
    "No inference made."
)


def plate_page(wells_number: int) -> int:
    """PhD thesis page of the Fig. 3.2 plate carrying a Wells sign number."""
    if wells_number <= 308:
        return 90
    if wells_number <= 681:
        return 91
    return 92


def load_registry() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    m2w: dict[str, set[str]] = defaultdict(set)
    w2m: dict[str, set[str]] = defaultdict(set)
    with REGISTRY_CSV.open(newline="") as fh:
        for row in csv.DictReader(fh):
            if not row["mahadevan_ids"] or not row["wells_ids"]:
                continue
            for m in row["mahadevan_ids"].split("|"):
                m = m.strip()
                for w in row["wells_ids"].split("|"):
                    w = w.strip()
                    m2w[m].add(w)
                    w2m[w].add(m)
    return m2w, w2m


def implication(treatment: str, sign: str, wells: list[str], others: list[str]) -> str:
    wtxt = ", ".join(wells) if wells else "none recorded"
    if treatment == "SPLIT":
        base = (f"If Wells's segmentation were adopted, tokens counted under {sign} in the "
                f"Mahadevan-lineage corpus would divide among Wells graphemes {wtxt}; "
                "frequency and positional statistics computed on the pooled sign would "
                "need recomputation per grapheme.")
        if others:
            base += (f" Note: {'/'.join(others)} also map(s) to one or more of these "
                     "graphemes, so the division is not a clean partition.")
        return base
    if treatment == "MERGE":
        return (f"If Wells's segmentation were adopted, {sign} and {'/'.join(others)} would be "
                f"counted as the single Wells grapheme {wtxt}; their token counts would pool "
                "and any contrast drawn between them would disappear.")
    if treatment == "SAME":
        return (f"Wells's list carries a one-to-one counterpart ({wtxt}); if Wells's segmentation "
                "were adopted, the sign's token identity would carry over by name, though the "
                "underlying corpora differ (Wells's ECIT/ICIT vs Mahadevan 1977).")
    if treatment == "NOT-COVERED":
        return ("No counterpart grapheme was found in Wells's list; if Wells's segmentation were "
                f"adopted, {sign}'s tokens would have to be assigned to component or neighbouring "
                "graphemes - the theses do not record which (open question).")
    return "Indeterminate: no conditional implication is recorded."


def main() -> None:
    anchors_doc = json.loads(ANCHORS_JSON.read_text())
    anchors = anchors_doc["anchors"]
    candidate = sorted(k for k, v in anchors.items() if v.get("confidence") == "CANDIDATE")
    pending = sorted(
        k for k, v in anchors.items() if v.get("validation_status") == "pending_non_sa_validation"
    )
    targets = sorted(set(candidate) | set(pending))
    assert len(candidate) == 113 and len(pending) == 44 and len(targets) == 157, (
        len(candidate), len(pending), len(targets))

    m2w, w2m = load_registry()

    # MA Fig. 3.6 (thesis p. 77) direct concordance entries for target signs.
    ma_fig36: dict[str, tuple[list[str], str]] = {
        "M178": (["436-446"], "SPLIT"),
        "M213": (["48"], "SAME"),
        "M400": (["247"], "SAME"),
    }

    rows: list[dict[str, str]] = []
    for sign in targets:
        anchor_set = "pending_non_sa_validation" if sign in pending else "CANDIDATE"
        wells = sorted(m2w.get(sign, set()))
        others = sorted({m for w in wells for m in w2m[w] if m != sign})
        verif, verif_note = HAND_VERIFICATION.get(sign, ("", ""))
        if wells:
            if len(wells) >= 2:
                treatment = "SPLIT"
            elif others:
                treatment = "MERGE"
            else:
                treatment = "SAME"
            method = "REGISTRY"
            wdisp = [w[1:] if w.startswith("W") else w for w in wells]
            pages = sorted({plate_page(int(w)) for w in wdisp})
            source = ("PhD 2006, Fig. 3.2 (thesis "
                      + "/".join(f"p. {p}" for p in pages)
                      + "); numbering as cross-matched in the held canonical registry "
                        "(Wells 2015 form of the Wells/ICIT list)")
            note = verif_note
            if sign in ma_fig36:
                ma_w, _ma_t = ma_fig36[sign]
                source += "; MA 1998, Fig. 3.6 (thesis p. 77)"
                note = (f"MA Fig. 3.6 gives Wells (1997) no(s). {', '.join(ma_w)} for this sign "
                        f"(MA treatment: {ma_fig36[sign][1]}), under the MA numbering. " + note).strip()
            rows.append({
                "sign": sign, "anchor_set": anchor_set, "treatment": treatment,
                "wells_graphemes": ";".join(wdisp),
                "correspondence_method": method,
                "thesis_source": source,
                "verification": verif,
                "implication_note": implication(treatment, sign, wdisp, others),
                "note": note,
            })
        elif sign in GLYPH_MATCHES:
            wnum, source, gnote = GLYPH_MATCHES[sign]
            treatment = "MERGE" if sign == "M389" else "SAME"
            rows.append({
                "sign": sign, "anchor_set": anchor_set, "treatment": treatment,
                "wells_graphemes": wnum,
                "correspondence_method": "GLYPH",
                "thesis_source": source,
                "verification": verif or "verified",
                "implication_note": implication(treatment, sign, [wnum],
                                                 ["M387"] if sign == "M389" else []),
                "note": gnote + (" " + verif_note if verif_note else ""),
            })
        elif sign in NOT_COVERED:
            rows.append({
                "sign": sign, "anchor_set": anchor_set, "treatment": "NOT-COVERED",
                "wells_graphemes": "",
                "correspondence_method": "GLYPH-SEARCH-NEGATIVE",
                "thesis_source": "PhD 2006, Fig. 3.2 (thesis pp. 90-92); MA 1998, Fig. 3.6 (thesis p. 77)",
                "verification": "",
                "implication_note": implication("NOT-COVERED", sign, [], []),
                "note": NOT_COVERED[sign],
            })
        else:
            rows.append({
                "sign": sign, "anchor_set": anchor_set, "treatment": "INDETERMINATE",
                "wells_graphemes": "",
                "correspondence_method": "NONE",
                "thesis_source": "",
                "verification": "",
                "implication_note": implication("INDETERMINATE", sign, [], []),
                "note": INDETERMINATE_OVERRIDES.get(sign, INDETERMINATE_REASON),
            })

    counts = Counter(r["treatment"] for r in rows)
    doc = {
        "_witness_framing": (
            "Witness statement only: records Wells's segmentation treatment and its conditional "
            "implication. No recommendation to adopt Wells's segmentation; no anchor-status "
            "implication asserted."),
        "phase": 123,
        "sources": {
            "anchors": "backend/reports/INDUS_FINAL_ANCHORS.json (113 CANDIDATE + 44 pending_non_sa_validation = 157 signs)",
            "registry": "data/crosswalks/canonical_sign_registry.csv (mayig CISI digitisation, Wells 2015 cross-match)",
            "wells_ma_1998": "Wells, An Introduction to Indus Writing, MA thesis, University of Calgary, 1998 (DOI 10.11575/PRISM/23641)",
            "wells_phd_2006": "Wells, Epigraphic Approaches to Indus Writing, PhD thesis, Harvard University, 2006 (deposited scan, 296 pp.)",
        },
        "counts": dict(sorted(counts.items())),
        "n_signs": len(rows),
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(doc, indent=2, sort_keys=False) + "\n")
    with OUT_CSV.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"n": len(rows), "counts": dict(counts)}, indent=1))


if __name__ == "__main__":
    main()
