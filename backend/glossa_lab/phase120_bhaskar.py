"""Phase-120: Bhaskar (2024) descriptive triage of the 44 flagged anchors.

SCOPE (read first). Bhaskar, M. V. (2024), "Markers and agencies of
anisotropy in the Indus sign system", *Indian Journal of History of
Science* (doi:10.1007/s43539-023-00102-3), and its Electronic
Supplementary Materials ESM1-ESM13, do **not** contain a per-sign
cross-compilation disagreement table. The article states its method
on p. 2: every sign and sign sequence *considered in the study* was
subjected to a three-way comparison between Mahadevan (1977) [M77],
ICIT, and CISI, and "any disagreement between these sources is noted
in each case" -- i.e. disagreements survive only as case-level notes
inside an anisotropy (sign-order / transposition) study:

  ESM1   F3 object catalogue (33 objects; frontal/dorsal signs)
  ESM2   F3-sequence simulations vs M77/ICIT; anisotropies D0-D5/Dx;
         error type E1 = corpus error / serious M77-ICIT disagreement
  ESM3   sign 99 as D1 marker: base-sign list; signs flanking 267
  ESM4   behaviour of 267a and 99-267a (line lists)
  ESM5   267 vs 267a against comparison signs
  ESM6-7 99-infix case studies (342 -> 344)
  ESM8   sign doubles; base signs of markers 97 and 123
  ESM9   sign 98 null simulation
  ESM10  sign 244 and its marked versions vs ICIT 629-642
  ESM11  intrinsic markers, fish-sign family
  ESM12  intrinsic markers outside the fish family
  ESM13  animal-behaviour catalogue (.xlsx, 2,383 object rows)

This module therefore does NOT fabricate M77/ICIT/CISI "readings"
per sign. It encodes, as data, (a) every cross-source disagreement /
conflation / adjudication case the keyword sweep of the article +
ESMs actually documents (the DISAGREEMENT_CASES register, each with
a precise location), and (b) a per-sign *mention index* recording
which list-structured ESM contexts mention a sign number at all
(behavioural attestation only -- never identity concordance).

Classification of one of the 44 flagged anchors (descriptive only):

  CONTESTED    a register case of a dispute kind names the sign's
               identity or form class.
  ALL-AGREE    requires an explicit per-sign concordance statement
               by Bhaskar. The corpus contains none (ESM2's
               concordance notes are sequence-level, for F3 strings,
               and concern sign ORDER, not sign identity), so this
               class is empty *by construction of the source*, and
               the classifier never infers it from silent use.
  NOT-COVERED  everything else, sub-flagged as
               "mentioned_behaviourally" (the sign number occurs in
               at least one parsed list / F3 sequence) or
               "not_mentioned".

Governance: this module changes no anchor status, validates
nothing, and contains no PRED content. It is a descriptive triage.
"""
from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# The disagreement register: every cross-source disagreement, conflation,
# normalisation dispute, or adjudication documented in Bhaskar (2024) +
# ESM1-ESM12 and found by the keyword sweep (conflat*, disagree*, E1,
# misprint, normalis*, doubtful, proxy, stand-alone, omits, "settles it
# in favour of", "vastly different", "does not have", "reckon*").
# Summaries are in our own words; locations are exact.
# ---------------------------------------------------------------------------

DISPUTE_KINDS = {
    "conflation_split",        # sources merge forms Bhaskar separates (or v.v.)
    "normalisation_split",     # one source normalises, another splits
    "e1_corpus_error",         # Bhaskar's E1 label
    "misprint",                # a source misprints a sign number
    "attribution_doubt",       # Bhaskar doubts an attribution to the sign
    "coverage_gap",            # a form is absent from all compilations
    "classification_dispute",  # sources classify the sign differently
    "mirrored_reckoning",      # a source reckons a mirrored form as another sign
    "omission",                # a source omits material (context only)
    "font_substitution",       # glyph unavailable; another source's glyph used
}


@dataclass(frozen=True)
class DisagreementCase:
    case_id: str
    kind: str
    signs_involved: tuple[int, ...]  # Mahadevan sign numbers whose identity/form is at issue
    sources: str                     # who disagrees with whom, in brief
    summary: str                     # our own words; no extended quotation
    location: str                    # ESM / article location incl. PDF page
    context_signs: tuple[int, ...] = ()  # sequence neighbours, NOT at issue


DISAGREEMENT_CASES: tuple[DisagreementCase, ...] = (
    DisagreementCase(
        "BH-D01", "conflation_split", (267,),
        "M77 vs Bhaskar (on CISI objects)",
        "M77 treats the rhomboid and ovoid forms as variants of one sign "
        "267 (sequences 2618/4090 vs the split sequence 6112 are called "
        "identical); Bhaskar argues the two forms cannot be conflated "
        "and distinguishes 267 from 267a on behavioural grounds.",
        "Article Sect. 3 (PDF p. 6); ESM3-ESM5",
    ),
    DisagreementCase(
        "BH-D02", "conflation_split", (97, 98),
        "ICIT (Wells/Fuls) vs Bhaskar/M77",
        "Wells and Fuls conflate signs 97 and 98 and assign a single "
        "ICIT number (001), denying 98 as a separate sign; Bhaskar "
        "keeps 97 and 98 distinct (97 a differential marker, 98 a "
        "neutral marker).",
        "Article Sect. 7 (PDF p. 18)",
    ),
    DisagreementCase(
        "BH-D03", "conflation_split", (99, 100),
        "ICIT (Wells) vs Bhaskar/M77",
        "Signs 99 and 100 are merged by Wells into a single ICIT "
        "number (002); Bhaskar keeps them distinct and argues at "
        "length (Sect. 5.6) for telling them apart.",
        "Article Sect. 7 (PDF p. 18); Sect. 5.6",
    ),
    DisagreementCase(
        "BH-D04", "attribution_doubt", (99, 100),
        "ICIT vs Bhaskar (object absent from M77)",
        "For one unicorn seal with no M77 entry, ICIT documents the "
        "first sign as its 002 (equivalent to M77 99); Bhaskar takes "
        "the sign as M77 100 instead, rationalised in Sect. 5.6.",
        "ESM1 row 23 (PDF p. 5)",
    ),
    DisagreementCase(
        "BH-D05", "normalisation_split", (244,),
        "M77 vs ICIT; Bhaskar proposes a third treatment",
        "M77 normalises visibly and behaviourally distinct forms "
        "(including forms on objects 4345 and 1550) to a single sign "
        "244, producing marker-less anisotropies (Dx); ICIT instead "
        "catalogues the forms as separate signs (ICIT 629-642). "
        "Bhaskar proposes one formative sign 244 with alphanumeric "
        "marked versions 244a-244k (ESM10).",
        "Article Sect. 8.1 (PDF p. 21); ESM10 (PDF p. 1)",
    ),
    DisagreementCase(
        "BH-D06", "misprint", (257, 197),
        "M77 internal error (noted by Bhaskar)",
        "M77 sequence 2518 (the longest frontal-sign sequence) carries "
        "a misprint: it reports sign 257 as 197. Sign 257 has only "
        "three occurrences in M77.",
        "ESM2 row 25 (PDF p. 14)",
    ),
    DisagreementCase(
        "BH-D07", "e1_corpus_error", (53, 342),
        "M77 vs ICIT",
        "Inscription 4827 (H-1393, pottery graffiti) vs ICIT 231: the "
        "two sources give materially different sequences (in the M77 "
        "version a 342 stands after 53 and another 342 before it); "
        "the first sign is obliterated, so CISI cannot settle it. "
        "Labelled E1 in ESM2.",
        "ESM2 row 14c (PDF p. 5)",
        context_signs=(287, 373),
    ),
    DisagreementCase(
        "BH-D08", "e1_corpus_error", (60, 87),
        "M77 vs ICIT (both faulted)",
        "Object C-79 (M77 6211; ICIT 75), arising in the simulation "
        "'87 after 60': both sources normalise C-79 to an extreme "
        "and produce vastly different readings. Labelled E1 in ESM2. "
        "The E1 concerns the object's whole reading; 60/87 are the "
        "simulated pair that surfaces it.",
        "ESM2 row 28f1 (PDF p. 15)",
        context_signs=(123, 305),
    ),
    DisagreementCase(
        "BH-D09", "e1_corpus_error", (60,),
        "M77 vs ICIT, one case settled by CISI, one unresolvable",
        "Three inscriptions where 342 occurs before 60: at 2456 the "
        "ICIT version differs (if it is taken, the case drops); at "
        "1090 CISI (M-740) settles the reading in favour of M77; at "
        "1125 M77 and ICIT 2423 disagree over the terminal sign and "
        "CISI (M-1732) cannot resolve it because the sign is "
        "partially lost -- an E1.",
        "ESM7 case 7 (PDF p. 1)",
        context_signs=(342, 344, 328),
    ),
    DisagreementCase(
        "BH-D10", "coverage_gap", (402,),
        "CISI object vs M77 + ICIT + the Indus font package (unanimous gap)",
        "The frontal flag/banner sign on K-39 waves left. No "
        "left-waving variant of 402 exists in M77, in ICIT, or in "
        "the font package; the only other left-waving instance "
        "(object 7065, L-115) is doubted by Bhaskar to be 402 at "
        "all, or even a variant of it. The disagreement is between "
        "the object's form and every compilation's inventory of "
        "402 -- not between the compilations themselves.",
        "ESM1, note at row 22 / K-39 (PDF p. 4)",
    ),
    DisagreementCase(
        "BH-D11", "classification_dispute", (162,),
        "M77 vs ICIT",
        "On M-223 (M77 1167), M77 treats sign 162 as a stand-alone "
        "sign; ICIT instead lists it as a proxy sign for the cult "
        "object. (Both sources note the reading direction of the "
        "object as LTR.)",
        "ESM2 row 13 header (PDF p. 2); ESM1 row 13",
    ),
    DisagreementCase(
        "BH-D12", "omission", (),
        "M77 (noted by Bhaskar)",
        "For C-23 (M77 6402) M77 reports the sequence in three lines "
        "and omits the 'double axe' element the goat faces. The "
        "omission concerns that element, not the identity of any "
        "numbered sign in the sequence, so no sign is listed as "
        "involved.",
        "ESM2 row 29 header (PDF p. 15)",
        context_signs=(267, 29, 180, 175, 28, 381, 102, 327),
    ),
    DisagreementCase(
        "BH-D13", "font_substitution", (187,),
        "M77 vs the Indus font package",
        "In sequence 1325 (M-1202) the second sign from the right is "
        "187 in M77; the font package has no exact glyph match for "
        "it, so the glyph for ICIT 257 is substituted.",
        "ESM2 row 16c (PDF p. 5)",
    ),
    DisagreementCase(
        "BH-D14", "mirrored_reckoning", (216, 217),
        "M77 reckoning (noted by Bhaskar)",
        "A mirrored form at object 7044 is reckoned in M77 as sign "
        "217 where Bhaskar's analysis treats the underlying sign as "
        "216 (mirrored).",
        "ESM8 entry 20 (PDF p. 2)",
    ),
    DisagreementCase(
        "BH-D15", "conflation_split", (244, 219),
        "Bhaskar vs a marked-version reading of the 244 family",
        "Within the ESM10 table, the unit catalogued as 244k is "
        "identified not as a marked version of 244 but as a compound "
        "of 244d with sign 219; another unit (641) is noted as not "
        "an independent sign but a double of 244a.",
        "ESM10 (PDF p. 1)",
    ),
    DisagreementCase(
        "BH-D16", "attribution_doubt", (167,),
        "Bhaskar (identity left open)",
        "For M-1793 (M77 2316) the frontal sign's identity is "
        "doubtful (given as 167 with a query, and in ESM1 as possibly "
        "a monkey per Mackay 1938); Bhaskar runs the simulation on "
        "the rest of the sequence only.",
        "ESM2 row 28 header (PDF p. 14); ESM1 row 28",
        context_signs=(60, 87, 123, 305),
    ),
)

# Form-reanalysis notes (Bhaskar's own analysis; NOT source-vs-source
# disputes, recorded for completeness of the disagreement table).
FORM_REANALYSIS_NOTES: tuple[DisagreementCase, ...] = (
    DisagreementCase(
        "BH-R01", "form_reanalysis", (59, 65, 67, 70, 72),
        "Bhaskar's analysis (M77/ICIT list the forms as separate signs)",
        "The fish-sign family: 65, 67, 70, 72 and others are treated "
        "as intrinsically marked versions of formative sign 59, used "
        "as D5 signals of anisotropy.",
        "Article Sect. 8.3; ESM11",
    ),
    DisagreementCase(
        "BH-R02", "form_reanalysis", (342, 343, 344, 345),
        "Bhaskar's analysis",
        "Signs 343, 344, 345 are analysed as 342 with an infixed/"
        "suffixed marker (343 ~ 342+97, 344 ~ 342+99, 345 ~ 342+102, "
        "the latter two tentative).",
        "Article Sect. 5.4; ESM2 intro; ESM6-ESM7",
    ),
    DisagreementCase(
        "BH-R03", "form_reanalysis", (287, 299, 303),
        "Bhaskar's analysis",
        "Sign 303 is analysed as a compound of 287 + 299 and is "
        "opposed to 287 in usage.",
        "ESM8 entries B/C/28 (PDF p. 3)",
    ),
    DisagreementCase(
        "BH-R04", "form_reanalysis", (171, 172),
        "Bhaskar's analysis",
        "Sign 172 is treated as a marked version of formative sign "
        "171, and their contrasting behaviour after sign 59 is used "
        "as D5/D1 evidence.",
        "ESM12 (PDF p. 1)",
    ),
)

ALL_CASES = DISAGREEMENT_CASES + FORM_REANALYSIS_NOTES

# ---------------------------------------------------------------------------
# Mention index: which list-structured ESM contexts mention a sign number.
# Extracted from the ESM text layer (glyph + number pairs) and hand-checked
# (see the Phase-120 report's sanity-check section). Membership here is
# behavioural attestation ONLY; it asserts nothing about concordance.
# ---------------------------------------------------------------------------

MENTION_SOURCES: dict[str, tuple[int, ...]] = {
    # ESM1 List 1: the 19 (+2) frontal signs with M77 frequencies.
    "ESM1_list1_frontal": (
        59, 171, 99, 162, 167, 211, 342, 1, 86, 402, 242, 397, 393,
        257, 410, 267, 201, 326, 63, 64,
    ),
    # ESM1 List 2: unique dorsal signs across the listed pairs/triplets/
    # quartets/longer sequences.
    "ESM1_list2_dorsal": (
        59, 171, 162, 342, 1, 284, 109, 112, 326, 336, 53, 105, 8,
        347, 249, 32, 102, 302, 244, 67, 242, 96, 409, 15, 120, 391,
        100, 60, 87, 123, 305, 175, 28, 381, 89, 327, 29,
    ),
    # ESM3 List 1: base signs to which 99 suffixes (86 signs).
    "ESM3_list1_base_of_99": (
        3, 4, 15, 19, 25, 28, 32, 34, 47, 53, 54, 56, 57, 59, 64, 70,
        81, 83, 86, 87, 89, 92, 98, 121, 130, 131, 132, 139, 152, 155,
        162, 169, 171, 173, 174, 176, 177, 180, 182, 194, 197, 199,
        201, 202, 206, 210, 214, 223, 230, 233, 234, 245, 252, 254,
        256, 257, 261, 267, 270, 277, 284, 286, 287, 293, 298, 302,
        303, 307, 322, 327, 329, 333, 336, 341, 350, 372, 375, 381,
        384, 391, 395, 397, 398, 400, 402, 403,
    ),
    # ESM3 List 2: signs occurring on either side of 267.
    "ESM3_list2_flanking_267": (
        1, 17, 51, 55, 59, 76, 86, 89, 127, 149, 150, 155, 162, 180,
        182, 194, 197, 204, 205, 216, 230, 244, 249, 267, 284, 287,
        293, 307, 328, 336, 341, 342, 343, 373, 375, 387, 391, 402,
    ),
    # ESM5: comparison signs x tabulated against both 267 and 267a.
    "ESM5_comparison_signs": (51, 55, 59, 86, 127, 162, 287, 336, 342),
    # ESM8: signs with an adjacent or distant double (numbered entries).
    "ESM8_doubling_signs": (
        1, 10, 54, 59, 76, 87, 89, 121, 127, 134, 150, 175, 176, 194,
        211, 212, 216, 237, 244, 245, 252, 267, 287, 290, 293, 294,
        303, 307, 323, 328, 342, 373, 375, 384, 389, 391,
    ),
    # ESM8 List 1: base signs for marker 123.
    "ESM8_list1_base_of_123": (
        32, 54, 59, 86, 94, 129, 150, 162, 169, 171, 180, 195, 196,
        197, 216, 225, 233, 286, 293, 302, 305, 307, 319, 330, 342,
        353, 375, 380, 391, 402, 403, 412,
    ),
    # ESM8 List 2: base signs for marker 97 (as extracted; the article
    # itself warns this count is the less certain of the two lists).
    "ESM8_list2_base_of_97": (
        6, 8, 10, 25, 32, 40, 53, 59, 72, 87, 126, 127, 150, 151, 155,
        157, 162, 169, 180, 185, 208, 211, 214, 216, 225, 233, 286,
        293, 302, 307, 330, 342, 353, 375, 391, 402,
    ),
}


def mentions_for(sign: int) -> list[str]:
    """Sorted mention-source names whose lists contain ``sign``."""
    return sorted(name for name, signs in MENTION_SOURCES.items() if sign in signs)


def cases_for(sign: int, *, include_reanalysis: bool = False) -> list[DisagreementCase]:
    pool = ALL_CASES if include_reanalysis else DISAGREEMENT_CASES
    return [c for c in pool if sign in c.signs_involved]


@dataclass
class TriageRow:
    sign: str            # anchor key, e.g. "M155"
    sign_number: int
    reading: str
    confidence: str
    classification: str  # ALL-AGREE | CONTESTED | NOT-COVERED
    subflag: str         # dispute kind(s) | mentioned_behaviourally | not_mentioned
    detail: str
    mention_sources: list[str] = field(default_factory=list)
    case_ids: list[str] = field(default_factory=list)


def classify_anchor(sign_key: str, reading: str, confidence: str) -> TriageRow:
    """Classify one flagged anchor against the Bhaskar register.

    ALL-AGREE is never returned: the source corpus contains no
    explicit per-sign concordance statement to return it *from*,
    and inferring agreement from silent use would fabricate the
    concordance table this phase established does not exist.
    """
    num = int(sign_key[1:])
    hits = [c for c in cases_for(num) if c.kind in DISPUTE_KINDS]
    mentions = mentions_for(num)
    if hits:
        detail = " ".join(f"[{c.case_id}] {c.summary}" for c in hits)
        return TriageRow(
            sign=sign_key, sign_number=num, reading=reading,
            confidence=confidence, classification="CONTESTED",
            subflag=",".join(sorted({c.kind for c in hits})),
            detail=detail, mention_sources=mentions,
            case_ids=[c.case_id for c in hits],
        )
    if mentions:
        return TriageRow(
            sign=sign_key, sign_number=num, reading=reading,
            confidence=confidence, classification="NOT-COVERED",
            subflag="mentioned_behaviourally",
            detail=(
                "Bhaskar's ESMs mention this sign number only as "
                "behavioural attestation (list membership / sequence "
                "participation). No passage adjudicates the sign's "
                "identity or form class across M77 / ICIT / CISI, so "
                "no concordance or disagreement can be reported."
            ),
            mention_sources=mentions, case_ids=[],
        )
    return TriageRow(
        sign=sign_key, sign_number=num, reading=reading,
        confidence=confidence, classification="NOT-COVERED",
        subflag="not_mentioned",
        detail=(
            "This sign number does not occur in any list-structured "
            "ESM context parsed for this phase, and no passage in "
            "the article or ESMs adjudicates its identity or form "
            "class across M77 / ICIT / CISI."
        ),
        mention_sources=[], case_ids=[],
    )


def load_flagged44(anchors_path: Path) -> list[tuple[str, str, str]]:
    """Return [(sign_key, reading, confidence)] for the 44 anchors
    whose validation_status is pending_non_sa_validation, sorted."""
    data = json.loads(Path(anchors_path).read_text("utf-8"))
    out = []
    for key, val in data["anchors"].items():
        if isinstance(val, dict) and val.get("validation_status") == (
            "pending_non_sa_validation"
        ):
            out.append((key, val.get("reading", ""), val.get("confidence", "")))
    return sorted(out)


def triage_all(anchors_path: Path) -> list[TriageRow]:
    return [classify_anchor(k, r, c) for k, r, c in load_flagged44(anchors_path)]


# ---------------------------------------------------------------------------
# Serialisation of the disagreement table (CSV + JSON rows).
# ---------------------------------------------------------------------------

def disagreement_table_rows() -> list[dict]:
    rows = []
    for c in ALL_CASES:
        rows.append({
            "case_id": c.case_id,
            "kind": c.kind,
            "signs_involved": " ".join(f"M{n:03d}" for n in c.signs_involved),
            "sign_numbers": " ".join(str(n) for n in c.signs_involved),
            "context_signs": " ".join(f"M{n:03d}" for n in c.context_signs),
            "sources": c.sources,
            "summary": c.summary,
            "location": c.location,
            "is_dispute": str(c.kind in DISPUTE_KINDS).lower(),
        })
    return rows


def disagreement_csv() -> str:
    rows = disagreement_table_rows()
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Optional ESM text-layer helpers (used by the phase script for the
# extraction audit; the curated register above remains the data of record).
# ---------------------------------------------------------------------------

def extract_pdf_text(pdf_path: Path) -> str | None:
    """Extract a PDF's text layer, or None if no extractor is available."""
    try:
        import pymupdf  # noqa: PLC0415
    except ImportError:
        try:
            import fitz as pymupdf  # noqa: PLC0415
        except ImportError:
            return None
    doc = pymupdf.open(str(pdf_path))
    return "\n".join(page.get_text() for page in doc)


def count_labelled_e1(text: str) -> int:
    """Count ESM2-style labelled E1 result blocks ('E1 (n):')."""
    return len(re.findall(r"E1 \(\d+\):", text))
