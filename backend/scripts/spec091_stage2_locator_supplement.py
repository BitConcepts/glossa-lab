#!/usr/bin/env python3
"""Spec 091 Stage 2 — SUPPLEMENTARY locator pass over the recovered texts.

Owner-commissioned 2026-11-17 after the recovery hunt changed the
holdings the T202 locator pass searched. T202's census (phonetic
0/184 located, semantic 0/184) stands as a record of the holdings
actually searched at its run: Parpola 1994 and Parpola 2010 were not
held, and the Mahadevan 1977 copy searched was an unpinned backup
(its run record pins CSV ec26651f... / JSON 774e8864...).

This supplement re-runs the locator search for all 184 crosswalk
entries x both reading fields under the SAME registered search order
and the SAME three-part locator test (eligibility-defs v1 §2) as
T202, with the holdings as recovered on 2026-11-17:

- Parpola 1994, Deciphering the Indus Script (CUP 1994) — held as an
  OCR-scan custody PDF (392 pp., SHA-256 fd133822...), searched
  through its extracted text layer; every candidate hit behind a
  filed locator was verified against the rendered page image, not
  the OCR text alone;
- Parpola 2010, A Dravidian solution to the Indus script problem —
  held as the born-digital PDF recovered from git history
  (SHA-256 c58137e5...), searched through its extracted text layer;
- Mahadevan 1977 sign list — the PINNED dataset, recovered
  byte-identical to the extraction pins (CSV ce5dd5a5..., JSON
  63059d64...), now standing at the canonical source-store path;
- Wells 1998 and the phoneme compilation — as in T202 (the
  compilation remains a pointer only and can never ground a locator).

The custody PDFs are in-copyright scholarly texts in restricted
custody OUTSIDE the tracked tree; they are never committed. This
script consumes their extracted page-text JSONs and verifies the
PDFs' SHA-256 against the recovery pins before any use, refusing on
mismatch. It does not import any PDF library.

A locator is filed ONLY from the adjudication table below: sign-level
attributions read first-hand in the recovered texts, each carrying
its evidence and its verification method, and each mechanically
cross-checked at build time against the extracted page text (the
cited value's normalized form and the sign's designation must both
occur on the cited pages) — the build REFUSES if a cross-check
fails. No locator is manufactured from a search hit alone.

The landed T202 artifact and records are NOT modified. This script
writes a NEW artifact beside it; the consumer merge rule (stated in
the delta record) is: T202 artifact + supplement read together; the
supplement wins per field.

Boundary: locatability only. This pass files no eligibility
determination, no WP5 disposition, and no claim-standing change
(eligibility-defs v1; the supplement's stage record states the
boundary in full).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

_BASE_PATH = REPO_ROOT / "backend" / "scripts" / "spec091_stage2_locator_pass.py"
_spec = importlib.util.spec_from_file_location("spec091_stage2_locator_pass", _BASE_PATH)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

run_records = base.run_records
write_file_verified = base.write_file_verified
Source = base.Source
_step = base._step
LocatorPassError = base.LocatorPassError
sha256_file = base.sha256_file
FIELDS = base.FIELDS

ARTIFACT_NAME = "mahadevan_parpola_crosswalk_v2_locators_supplement"
ARTIFACT_VERSION = "v1"
TOOL_NAME = "spec091_stage2_locator_supplement.py"
TOOL_VERSION = "locator-pass supplement v1 (Spec 091 Stage 2)"

ARTIFACT_REL = "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_locators_supplement.json"
T202_ARTIFACT_REL = base.ARTIFACT_REL
SPEC_RECORDS_REL = base.SPEC_RECORDS_REL
VERIFICATION_REL = f"{SPEC_RECORDS_REL}/stage-2-supplement-sample-verification.json"
DELTA_REL = f"{SPEC_RECORDS_REL}/stage-2-supplement-delta.json"
T202_RUN_ID = "study-20261117T105335Z-4d667e"

# Recovery pins (2026-11-17 recovery hunt; custody copies verified
# byte-identical on arrival on the mini-server).
PARPOLA_1994_PDF_SHA256 = "fd133822f9999c86178a32208465e847c5288b578ad14ca2cd643efe57f0e0b6"
PARPOLA_2010_PDF_SHA256 = "c58137e54cdde3f2acdcfaf05293dfc5f5ba33def3e0b12585c451f76bd4ba84"
M77_PINNED_CSV_SHA256 = "ce5dd5a59418132f54761324ca449aa0a7d37e0dad41013aca811049b36af3a4"
M77_PINNED_JSON_SHA256 = "63059d6403898653600c3be3e2268c512550cc8f8906114ac712743f161e0ae3"

WORK_1994 = "Parpola 1994, Deciphering the Indus Script (Cambridge University Press)"
WORK_2010 = (
    "Parpola 2010, A Dravidian solution to the Indus script problem "
    "(World Classical Tamil Conference lecture)"
)

OCR_CAVEAT = (
    "OCR text layer (ABBYY FineReader 12): diacritics are degraded "
    "throughout (macrons and underdots dropped or misread), so a "
    "not-found in this layer is weaker than in born-digital text; "
    "consonant skeletons — the basis of this pass's value comparison "
    "— survived in every value word of the image-verified samples "
    "(measured verbatim word error rate 13.1% on the printed p. 3 "
    "sample paragraph, the errors concentrated in letter-spacing, "
    "token splits and diacritic loss; see the stage record)"
)


# ---------------------------------------------------------------------------
# Value normalization. A same-reading identification rule, fixed before
# outcomes: lowercase; strip diacritics (NFD); collapse doubled letters
# (the ASCII long-vowel doubling of the staged values and of the 2010
# text layer); the 2010 text layer's legacy-font capitals inside
# transliterated words (T/L/Z/N for the retroflex letters) are
# skeleton-neutral except Z (for the retroflex l), which the map
# resolves. Staged values split on '/' into alternatives; parenthetical
# material yields both the expanded and the dropped form.
# ---------------------------------------------------------------------------

_LEGACY_FONT_MAP = str.maketrans({"T": "ṭ", "L": "ḷ", "Z": "ḻ", "N": "ṇ"})


def skeleton(word: str) -> str:
    w = unicodedata.normalize("NFD", word.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    w = re.sub(r"[^a-z]", "", w)
    return re.sub(r"(.)\1+", r"\1", w)


def value_forms(value: Optional[str]) -> set[str]:
    """All normalized forms under which a staged/cited value may appear."""
    if not value:
        return set()
    forms: set[str] = set()
    for alt in value.split("/"):
        alt = alt.strip().rstrip("-").strip()
        if not alt:
            continue
        variants = {alt}
        m = re.search(r"\(([^)]*)\)", alt)
        if m:
            variants.add(alt[: m.start()] + m.group(1) + alt[m.end():])
            variants.add(alt[: m.start()] + alt[m.end():])
        for v in variants:
            s = skeleton(v)
            if s:
                forms.add(s)
    return forms


def page_tokens(text: str, *, legacy_font: bool = False) -> set[str]:
    """Whole-word skeletons of a page, with hyphenated compounds split
    and runs of >=3 single-letter tokens (the OCR's letter-spaced
    italics) rejoined."""
    if legacy_font:
        text = text.translate(_LEGACY_FONT_MAP)
    raw = re.split(r"[\s\-]+", text)
    toks = [t.strip(".,;:!?()[]'\"*") for t in raw]
    toks = [t for t in toks if t]
    out: set[str] = set()
    run: list[str] = []

    def flush():
        if len(run) >= 3:
            out.add(skeleton("".join(run)))
        run.clear()

    for t in toks:
        s = skeleton(t)
        if s:
            out.add(s)
        if len(t) == 1 and t.isalpha():
            run.append(t)
        else:
            flush()
    flush()
    # Letter-spacing also splits words unevenly ('e lu' for eḻu, from an
    # italic word the OCR broke after its first letter): join short
    # consecutive token runs that contain a single-letter token.
    for i in range(len(toks)):
        acc = ""
        has_single = False
        for j in range(i, min(i + 4, len(toks))):
            acc += toks[j]
            if len(toks[j]) == 1:
                has_single = True
            if len(acc) > 12:
                break
            if j > i and has_single:
                s = skeleton(acc)
                if s:
                    out.add(s)
    return out


def load_pages(path: Path) -> dict[int, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {int(p["pdf_page"]): p["text"] for p in data["pages"]}


def candidate_pages(
    token_sets: dict[int, set[str]], forms: set[str], *, pdf_offset: int
) -> list[str]:
    """Printed-page labels of pages carrying any form as a whole word."""
    if not forms:
        return []
    hits: list[str] = []
    for pdf_page in sorted(token_sets):
        if forms & token_sets[pdf_page]:
            printed = pdf_page + pdf_offset
            hits.append(str(printed) if printed > 0 else f"pdf {pdf_page}")
    return hits


# ---------------------------------------------------------------------------
# The adjudication table. Every row was read first-hand in the held
# texts during this pass and (for the 1994 scan) verified against the
# rendered page image. A row files a locator only when the mechanical
# cross-check in the source's locate() passes against the extracted
# page text: the cited value's skeleton and a designation keyword must
# both occur on the row's check pages.
# ---------------------------------------------------------------------------

ADJUDICATIONS: list[dict] = [
    {
        "sign": "M047", "work": "1994",
        "pinpoint": "§10.4, pp. 194–195 (the 'number' + 'fish' sequences and the "
                    "doubled plain 'fish' sign), and Epilogue fig. 15.2 no. 1, p. 275",
        "sign_scheme": "the plain 'fish' sign, identified pictorially in the work; "
                       "tied to this entry by the phoneme compilation's iconic "
                       "record for Parpola no. 47 ('plain fish') and the crosswalk",
        "cited_value": "mīn",
        "evidence": "§10.4 reads the '7' + 'fish' sequence eḻu-mīn and ties the "
                    "doubled plain 'fish' signs to the root mīn ('to twinkle, of "
                    "stars'); fig. 15.2 no. 1 gives the fish sign's shared phonetic "
                    "shape as mīn",
        "check_pages_pdf": [213, 293], "check_value_forms": ["min"],
        "check_keywords": ["fish"],
    },
    {
        "sign": "M087", "work": "1994",
        "pinpoint": "§13.2, pp. 230–231, and Epilogue fig. 15.2 nos. 14–15, p. 276",
        "sign_scheme": "the sign of 'two long vertical strokes' (the 'intermediate "
                       "space' of fig. 15.2), identified pictorially in the work; "
                       "tied to this entry by the phoneme compilation's iconic "
                       "record for Parpola no. 87",
        "cited_value": "veḷ",
        "evidence": "§13.2: 'the phonetic shape veḷ / vēḷ has emerged as the shared "
                    "component X in the compounds Muruku-X and X-mīn', the sign "
                    "being the 'two long vertical strokes' pictogram, whose rebus "
                    "is veḷi 'intervening space'; fig. 15.2 nos. 14–15 give "
                    "vēḷ(i) for the same sign",
        "check_pages_pdf": [249, 294], "check_value_forms": ["vel"],
        "check_keywords": ["strokes"],
    },
    {
        "sign": "M088", "work": "1994",
        "pinpoint": "§10.4, p. 194 (the '3' + 'fish' sequence), and Epilogue "
                    "fig. 15.2 no. 3, p. 275",
        "sign_scheme": "the numeral sign '3' (three vertical strokes), identified "
                       "in the work as the first member of the '3' + 'fish' "
                       "sequence; tied to this entry by the phoneme compilation's "
                       "iconic record for Parpola no. 88 ('3 vertical strokes')",
        "cited_value": "mu(m)",
        "evidence": "§10.4: the '3' + 'fish' sequence 'yields in Dravidian "
                    "mu-m-mīn, (constellation of) three stars', mu- being 'the "
                    "monomorphemic adjective form of the numeral 3'; fig. 15.2 "
                    "no. 3 gives the component reading mu(m)",
        "check_pages_pdf": [212, 293], "check_value_forms": ["mu", "mum"],
        "check_keywords": ["three"],
    },
    {
        "sign": "M091", "work": "1994",
        "pinpoint": "§10.4, p. 194, and Epilogue fig. 15.2 no. 4, p. 275",
        "sign_scheme": "the numeral sign '6' (six strokes), identified in the "
                       "work as the first member of the '6' + 'fish' sequence; "
                       "tied to this entry by the phoneme compilation's record "
                       "for Parpola no. 91",
        "cited_value": "aru",
        "evidence": "§10.4: 'The most frequent sequence [fish + 6] corresponds to "
                    "the native name of the Pleiades in Old Tamil: aṟu-mīṉ, "
                    "literally (the constellation consisting of) six (visible) "
                    "stars'; fig. 15.2 no. 4 gives (*c)aṟu + mīn",
        "check_pages_pdf": [212, 293], "check_value_forms": ["aru"],
        "check_keywords": ["six"],
    },
    {
        "sign": "M092", "work": "1994",
        "pinpoint": "§10.4, p. 195, and Epilogue fig. 15.2 no. 5, p. 275",
        "sign_scheme": "the numeral sign '7' (seven strokes), identified in the "
                       "work as the first member of the '7' + 'fish' sequence; "
                       "tied to this entry by the phoneme compilation's record "
                       "for Parpola no. 92",
        "cited_value": "elu",
        "evidence": "§10.4: the seal with 'the sole text 7 + fish' — 'The latter "
                    "sequence gives in Dravidian eḻu-mīn, (constellation of) "
                    "seven stars, which is the Old Tamil name of the Ursa Major'; "
                    "fig. 15.2 no. 5 gives eḻu + mīn",
        "check_pages_pdf": [213, 293], "check_value_forms": ["elu"],
        "check_keywords": ["seven"],
    },
    {
        "sign": "M261", "work": "1994",
        "pinpoint": "§13.1, p. 229, and Epilogue fig. 15.2 no. 11, p. 276",
        "sign_scheme": "the sign of 'two intersecting circles', identified "
                       "pictorially in the work; tied to this entry by the "
                       "crosswalk provenance's recorded depiction for M261 "
                       "('two intersecting circles')",
        "cited_value": "muruku",
        "evidence": "§13.1: 'strongly supports the interpretation that the sign "
                    "of two intersecting circles engraved on many Harappan "
                    "bangles denotes the Dravidian word muruku, which means "
                    "both bangle and son, boy child'; fig. 15.2 no. 11 gives "
                    "muruku for the ring(s)/bangle(s) sign",
        "check_pages_pdf": [247, 294], "check_value_forms": ["muruku"],
        "check_keywords": ["circles"],
    },
    {
        "sign": "M281", "work": "1994",
        "pinpoint": "§13.1, pp. 229–230, and Epilogue fig. 15.2 no. 13, p. 276",
        "sign_scheme": "the sign depicting the five-striped palm squirrel, "
                       "identified pictorially in the work (§7.2, fig. 7.1, as "
                       "cited in §13.1); tied to this entry by the crosswalk "
                       "provenance's recorded depiction for M281 "
                       "('five-striped palm squirrel')",
        "cited_value": "piḷḷai",
        "evidence": "§13.1 introduces the sign (in seal M-1202, after the 'two "
                    "intersecting circles' sign) as 'depicting the five-striped "
                    "palm squirrel' and gives the Tamil name aṇil / aṇiṟ piḷḷai; "
                    "p. 230 develops piḷḷai for the squirrel and the Muruku "
                    "compounds; fig. 15.2 no. 13 gives muruku + piḷḷay for "
                    "ring(s)/bangle(s) + palm squirrel",
        "check_pages_pdf": [247, 248, 294], "check_value_forms": ["pilai"],
        "check_keywords": ["squirrel"],
    },
    {
        "sign": "M311", "work": "1994",
        "pinpoint": "§14.1, p. 240, and Epilogue fig. 15.2 no. 16, p. 276",
        "sign_scheme": "the 'fig tree' sign (the three-branched fig tree; "
                       "allographs at fig. 13.15), identified pictorially in the "
                       "work; tied to this entry by the crosswalk provenance's "
                       "recorded depiction for M311 ('fig tree (three-branched)')",
        "cited_value": "vaṭa",
        "evidence": "§14.1: 'There are several reasons to think that this "
                    "ordinary reading of the fig sign was vaṭa, banyan tree, the "
                    "Indian fig, Ficus indica L.'; the section develops the "
                    "vaṭa-mīn 'star of the north' interpretation; fig. 15.2 "
                    "no. 16 gives vaṭa + mīn for fig tree + fish",
        "check_pages_pdf": [258, 294], "check_value_forms": ["vata"],
        "check_keywords": ["fig"],
    },
    {
        "sign": "M175", "work": "2010",
        "pinpoint": "p. 24 (the interpretation of the first sign of seal M-241, "
                    "introduced as 'not included in my 1994 book')",
        "sign_scheme": "the sign depicting the spinner's spindle, identified "
                       "pictorially in the work; tied to this entry by the "
                       "crosswalk provenance's recorded depiction for M175 "
                       "('spinner's spindle')",
        "cited_value": "katir",
        "evidence": "'It seems to depict the traditional Indian spinner's "
                    "spindle... In Proto-Dravidian it was called katir, which "
                    "is homophonous with the root katir, to shine, be radiant' "
                    "— the work's rebus construction throughout attributes the "
                    "depicted object's Dravidian name as the sign's value",
        "check_pages_pdf": [24], "check_value_forms": ["katir"],
        "check_keywords": ["spindle"],
    },
]

ADJ_BY_SIGN_WORK = {(a["sign"], a["work"]): a for a in ADJUDICATIONS}

# Per-entry near-miss notes, each a first-hand fact of this pass's read.
# Appended to the step result of the named work when the entry is not
# located there. Absence of a note is itself the record: nothing
# specific was found beyond the documented search.
NEAR_MISS_NOTES: dict[tuple[str, str], str] = {
    ("M001", "1994"): (
        "the compilation's proposal for this sign is āḷ (the 'man' sign), not "
        "the staged tōḷ; no passage found in the work attributes tōḷ to the sign"
    ),
    ("M032", "1994"): (
        "§13.3 (p. 233) and Epilogue fig. 15.2 no. 20 read the 'crab' sign "
        "kōḷ 'grasper, planet'; the program's records do not tie the 'crab' "
        "depiction to this entry, so that attribution cannot be filed for it"
    ),
    ("M099", "1994"): (
        "§13.3 (p. 233) and Epilogue fig. 15.2 no. 20 read the 'crab' sign "
        "kōḷ, matching this entry's staged value in form; but the program's "
        "records do not tie the 'crab' depiction to this entry — the phoneme "
        "compilation's record for Parpola no. 99 is the 'bow' sign (read "
        "vil), and the 2010 fig. 11 caption numbers the 'crab' sign 124 in "
        "the work's own numbering, which the crosswalk does not use — so "
        "the identification is contradicted, not overdetermined, and no "
        "locator is filed"
    ),
    ("M124", "1994"): (
        "§13.3 (p. 233) reads the 'crab' sign kōḷ 'seizer, planet', a "
        "different value from the staged kuTam; the compilation's iconic "
        "record for this entry is a vessel ('V-shaped offering vessel'), "
        "not the crab"
    ),
    ("M124", "2010"): (
        "no passage in the held text attributes kuTam to any sign; the "
        "compilation's source label for this entry ('Parpola 2010 sec. "
        "iconic shape… + M-478 tablet') corresponds to no passage in the "
        "recovered text — a named discrepancy, carried to the stage record"
    ),
    ("M123", "1994"): (
        "ch. 14 (§14.1) and Epilogue fig. 15.2 no. 16 attribute vaṭa to the "
        "three-branched 'fig tree' sign, which the crosswalk provenance "
        "records as M311's depiction; this entry records no depiction and "
        "stages no value, so no passage can carry a field value for it"
    ),
    ("M123", "2010"): (
        "the fig. 11 caption (p. 21) numbers the three-branched 'fig tree' "
        "sign 'no. 123' in the work's own sign numbering and pp. 20–23 read "
        "it vaṭa (vaṭa-mīn 'north star'); this entry stages no value, so "
        "the passage cannot carry a field value for it; the entry the "
        "crosswalk ties to the fig-tree depiction and the vaṭa value is M311"
    ),
    ("M050", "1994"): (
        "the 'fish' chapters attribute mīn to the plain 'fish' sign and "
        "specific values to specific modified signs; no passage attributes "
        "pār to this entry's sign"
    ),
    ("M088", "2010"): (
        "the 'three long vertical strokes' sign receives an iconic "
        "interpretation only in this work (p. 30, 'the three worlds'); no "
        "phonetic value is attributed to it here — its phonetic locator, "
        "if any, is the 1994 step's"
    ),
    ("M125", "1994"): (
        "Epilogue fig. 15.2 and the compilation concern the 'bow' reading "
        "vil for Parpola no. 99's sign; no passage in the running text "
        "attributes vil to this entry's sign"
    ),
    ("M151", "1994"): (
        "no passage in the running text attributes vil to this entry's sign"
    ),
    ("M128", "1994"): (
        "Epilogue fig. 15.2 no. 9 reads the 'dot-in-circle = eye' sign kaṇ; "
        "three entries stage kaṇ-type values (M128, M153, M391) and no "
        "program record ties that depiction to exactly one of them, so no "
        "locator is filed for any of the three"
    ),
    ("M153", "1994"): (
        "Epilogue fig. 15.2 no. 9 reads the 'dot-in-circle = eye' sign kaṇ; "
        "three entries stage kaṇ-type values (M128, M153, M391) and no "
        "program record ties that depiction to exactly one of them, so no "
        "locator is filed for any of the three"
    ),
    ("M391", "1994"): (
        "Epilogue fig. 15.2 no. 9 reads the 'dot-in-circle = eye' sign kaṇ; "
        "three entries stage kaṇ-type values (M128, M153, M391) and no "
        "program record ties that depiction to exactly one of them, so no "
        "locator is filed for any of the three"
    ),
    ("M071", "1994"): (
        "Epilogue fig. 15.2 no. 18 reads the '4' sign nāḷ in the '4' + 'fig' "
        "compound; two entries stage nal (M071, M077) and no program record "
        "ties the four-stroke sign to exactly one of them, so no locator "
        "is filed"
    ),
    ("M077", "1994"): (
        "Epilogue fig. 15.2 no. 18 reads the '4' sign nāḷ in the '4' + 'fig' "
        "compound; two entries stage nal (M071, M077) and no program record "
        "ties the four-stroke sign to exactly one of them, so no locator "
        "is filed"
    ),
}


# ---------------------------------------------------------------------------
# The held Parpola sources
# ---------------------------------------------------------------------------


def _parpola_source(
    *,
    work_key: str,
    source_id: str,
    work: str,
    pdf_sha256: str,
    pages: dict[int, str],
    legacy_font: bool,
    pdf_offset: int,
    layer_description: str,
) -> Source:
    token_sets: dict[int, set[str]] = {
        p: page_tokens(t, legacy_font=legacy_font) for p, t in pages.items()
    }

    def tokens(pdf_page: int) -> set[str]:
        return token_sets[pdf_page]

    def search(ctx: dict, field: str) -> dict:
        if field == "semantic_reading":
            return {
                "status": "searched",
                "method": (
                    "read the work for a meaning recorded separately for this "
                    "entry's sign, across the sign-reading chapters and the "
                    "work's summary of its interpretations"
                ),
                "facts": {
                    "held": True,
                    "staged_value": None,
                    "semantic_value_recorded_separately": False,
                },
                "result": (
                    "the crosswalk records no semantic value separately for "
                    "any entry (WP4 D5: WP4 records no semantic reading "
                    "separately for any entry), and this work likewise "
                    "attests no meaning for this entry's sign apart from its "
                    "phonetic proposal, so no passage in it can carry the "
                    "field's value"
                ),
            }
        forms = value_forms(ctx["staged_value"])
        found = candidate_pages(token_sets, forms, pdf_offset=pdf_offset)
        facts: dict = {
            "held": True,
            "text_layer": layer_description,
            "staged_value": ctx["staged_value"],
            "candidate_pages_printed": found[:25],
            "candidate_page_count": len(found),
        }
        if work_key == "1994":
            facts["ocr_caveat"] = OCR_CAVEAT
        if ctx["staged_value"] is None:
            result = (
                "the entry stages no phonetic value, so there is no value "
                "for a passage to carry; the work was nevertheless read for "
                "an attribution to this entry's sign, and the attributions "
                "found are recorded in this step where they bear on the entry"
            )
        else:
            result = (
                f"the staged value {ctx['staged_value']!r} was sought as a whole "
                f"word under the pass's normalization across the extracted text "
                f"of the held copy (candidate pages, printed: "
                f"{found[:25] if found else 'none'}); the sign-reading chapters "
                f"and the work's interpretation summary were read for an "
                f"attribution to this entry's sign; none attributes the staged "
                f"value to this entry's sign at an entry-level pinpoint"
            )
        note = NEAR_MISS_NOTES.get((ctx["sign"], work_key))
        if note:
            result += "; " + note
        return {"status": "searched", "method": (
            "full-text search of the extracted text layer of the held copy "
            "under the pass's value normalization, plus a read of the "
            "sign-reading chapters and the work's own interpretation "
            "summary for a sign-level attribution to this entry"
        ), "facts": facts, "result": result}

    def locate(ctx: dict, field: str) -> Optional[dict]:
        if field != "phonetic_reading":
            return None
        adj = ADJ_BY_SIGN_WORK.get((ctx["sign"], work_key))
        if adj is None:
            return None
        # The mechanical cross-check: the adjudicated cited value and
        # the sign's designation must both occur on the cited pages of
        # the extracted text. Refusal — never a manufactured locator —
        # if either fails.
        value_hit = False
        keyword_hit = False
        for pdf_page in adj["check_pages_pdf"]:
            toks = tokens(pdf_page)
            if set(adj["check_value_forms"]) & toks:
                value_hit = True
            if {skeleton(k) for k in adj["check_keywords"]} & toks:
                keyword_hit = True
        if not (value_hit and keyword_hit):
            raise LocatorPassError(
                f"adjudication cross-check failed for {ctx['sign']} in "
                f"Parpola {work_key}: value_hit={value_hit}, "
                f"keyword_hit={keyword_hit} on check pages "
                f"{adj['check_pages_pdf']} — the pass refuses to file a "
                "locator its own extracted text does not corroborate"
            )
        if not (value_forms(adj["cited_value"]) & value_forms(ctx["staged_value"])):
            raise LocatorPassError(
                f"adjudicated cited value {adj['cited_value']!r} does not "
                f"match the staged value {ctx['staged_value']!r} for "
                f"{ctx['sign']} under the pass's normalization"
            )
        return {
            "work": work,
            "pinpoint": adj["pinpoint"],
            "sign_scheme": adj["sign_scheme"],
            "cited_value": adj["cited_value"],
            "evidence": adj["evidence"],
            "verification": (
                "candidate hit verified against the rendered page image of "
                "the held scan (not the OCR text alone)"
                if work_key == "1994"
                else "born-digital text layer of the recovered PDF, read "
                     "directly"
            ),
        }

    return Source(
        source_id,
        work,
        held=True,
        held_as=(
            "restricted custody copy outside the tracked tree "
            "(mini-server work directory); never committed"
        ),
        sha256=pdf_sha256,
        can_ground_locator=True,
        search=search,
        locate=locate,
    )


def build_supplement_sources(
    repo_root: Path,
    *,
    parpola_1994_pdf: Path,
    parpola_2010_pdf: Path,
    parpola_1994_pages_path: Path,
    parpola_2010_pages_path: Path,
) -> list[Source]:
    """The registered search order, with the recovered holdings.
    Refuses on any pin mismatch or absent held source."""
    for pdf, expected, label in (
        (parpola_1994_pdf, PARPOLA_1994_PDF_SHA256, "Parpola 1994 custody PDF"),
        (parpola_2010_pdf, PARPOLA_2010_PDF_SHA256, "Parpola 2010 custody PDF"),
    ):
        if not pdf.exists():
            raise LocatorPassError(f"held custody source absent: {label} at {pdf}")
        actual = sha256_file(pdf)
        if actual != expected:
            raise LocatorPassError(
                f"{label} SHA-256 mismatch: expected the recovery pin "
                f"{expected}, found {actual} — the pass refuses to search "
                "a copy that is not the recovered text"
            )
    pages_1994 = load_pages(parpola_1994_pages_path)
    pages_2010 = load_pages(parpola_2010_pages_path)
    if len(pages_1994) != 392 or len(pages_2010) != 39:
        raise LocatorPassError(
            f"extracted page sets incomplete: Parpola 1994 carries "
            f"{len(pages_1994)} pages (expected 392), Parpola 2010 carries "
            f"{len(pages_2010)} (expected 39)"
        )
    _provenance, _crosswalk, pins = base.load_inputs(repo_root)
    if pins["mahadevan_1977_sign_list"]["sha256"] != M77_PINNED_CSV_SHA256:
        raise LocatorPassError(
            "the Mahadevan 1977 dataset at the canonical source-store path "
            "is not the pinned recovered copy (CSV sha256 "
            f"{pins['mahadevan_1977_sign_list']['sha256']}, expected the "
            f"extraction pin {M77_PINNED_CSV_SHA256})"
        )
    m77_path = repo_root / base.M77_REL
    wells_path = repo_root / base.WELLS_REL
    phoneme_path = repo_root / base.PHONEME_REL
    phoneme_map = json.loads(phoneme_path.read_text(encoding="utf-8"))["phoneme_map"]
    phoneme = base.phoneme_compilation_source(phoneme_map, phoneme_path)
    base_phoneme_search = phoneme._search

    def phoneme_search(ctx: dict, field: str) -> dict:
        step = base_phoneme_search(ctx, field)
        if step["facts"].get("hit"):
            step = dict(step)
            step["result"] = step["result"] + (
                " [supplement: the labelled primary text has since been "
                "recovered and was searched in this pass — see the Parpola "
                "1994 / Parpola 2010 steps above; the compilation itself "
                "remains a pointer and cannot ground a locator]"
            )
        return step

    phoneme._search = phoneme_search
    return [
        _parpola_source(
            work_key="1994", source_id="parpola_1994", work=WORK_1994,
            pdf_sha256=PARPOLA_1994_PDF_SHA256, pages=pages_1994,
            legacy_font=False, pdf_offset=-18,
            layer_description="ocr_scan_text_layer",
        ),
        _parpola_source(
            work_key="2010", source_id="parpola_2010", work=WORK_2010,
            pdf_sha256=PARPOLA_2010_PDF_SHA256, pages=pages_2010,
            legacy_font=True, pdf_offset=0,
            layer_description="born_digital_text_layer",
        ),
        base.mahadevan_1977_source(base.load_m77_rows(m77_path), m77_path),
        base.wells_1998_source(base.load_wells_rows(wells_path), wells_path),
        phoneme,
    ]


# ---------------------------------------------------------------------------
# The pass itself (mirrors T202's outcome construction; the not-found
# basis is corrected for the recovered holdings)
# ---------------------------------------------------------------------------


def build_outcome_supp(ctx: dict, field: str, sources: list[Source], run_date: str) -> dict:
    steps: list[dict] = []
    stated = base.stated_source_step(ctx, field, run_date)
    if stated is not None:
        steps.append(stated)
    for source in sources:
        raw = source.search(ctx, field)
        steps.append(
            _step(source, raw["status"], raw["method"], raw["facts"], raw["result"], run_date)
        )
        locator = source.locate(ctx, field)
        if locator is not None:
            return {"outcome": "located", "locator": locator, "not_found": None}
    if ctx["staged_value"] is None:
        basis = (
            "the staged entry states no value for this field, and no held "
            "copy attributes one at an entry-level primary-source pinpoint; "
            "the recovered Parpola 1994 and Parpola 2010 texts were searched "
            "in full for this entry"
        )
    else:
        basis = (
            "no held copy carries this field's value at an entry-level "
            "primary-source pinpoint for this entry's sign; the recovered "
            "Parpola 1994 and Parpola 2010 texts were searched in full and "
            "do not attribute the staged value to this entry's sign"
        )
    return {
        "outcome": "not_found",
        "locator": None,
        "not_found": {"basis": basis, "search": steps},
    }


def build_record_supp(
    provenance: dict,
    crosswalk: dict,
    sources: list[Source],
    *,
    run_id: str,
    run_date: str,
    input_pins: dict,
) -> dict:
    entries = []
    census = {field: {"located": 0, "not_found": 0} for field in FIELDS}
    for prov_entry in provenance["entries"]:
        ctx = base.entry_context(prov_entry, crosswalk.get(prov_entry["sign"]))
        record_entry: dict = {
            "sign": ctx["sign"],
            "mahadevan_id": ctx["mahadevan_id"],
            "parpola_id": ctx["parpola_id"],
        }
        for field in FIELDS:
            field_ctx = dict(ctx)
            field_ctx["staged_value"] = prov_entry[field]["value"]
            field_ctx["source_as_stated"] = prov_entry[field]["source_as_stated"]
            outcome = build_outcome_supp(field_ctx, field, sources, run_date)
            census[field]["located" if outcome["outcome"] == "located" else "not_found"] += 1
            record_entry[field] = {
                "staged_value": prov_entry[field]["value"],
                "source_as_stated": prov_entry[field]["source_as_stated"],
                **outcome,
            }
        entries.append(record_entry)
    record = {
        "artifact": ARTIFACT_NAME,
        "version": ARTIFACT_VERSION,
        "generated_by": f"{TOOL_NAME} (Spec 091 Stage 2 supplementary locator pass)",
        "run_id": run_id,
        "run_date": run_date,
        "source_revision": provenance["source_revision"],
        "supplement_to": {
            "artifact": T202_ARTIFACT_REL,
            "run_id": T202_RUN_ID,
            "merge_rule": (
                "read the T202 artifact and this supplement together; per "
                "entry per field, this supplement's outcome wins"
            ),
        },
        "inputs": input_pins,
        "search_sources": [s.registry_entry() for s in sources],
        "summary": {
            "n_entries": len(entries),
            **{field: census[field] for field in FIELDS},
        },
        "entries": entries,
    }
    base.validate_locator_record(record, [e["sign"] for e in provenance["entries"]])
    return record


def supplement_input_pins(repo_root: Path, args) -> dict:
    _p, _c, pins = base.load_inputs(repo_root)
    pins = dict(pins)
    pins["parpola_1994_pdf"] = {
        "path": "custody copy outside the tracked tree (never committed)",
        "sha256": sha256_file(args.parpola_1994_pdf),
        "recovery_pin": PARPOLA_1994_PDF_SHA256,
    }
    pins["parpola_2010_pdf"] = {
        "path": "custody copy outside the tracked tree (never committed)",
        "sha256": sha256_file(args.parpola_2010_pdf),
        "recovery_pin": PARPOLA_2010_PDF_SHA256,
    }
    pins["parpola_1994_extracted_pages"] = {
        "path": str(args.parpola_1994_pages),
        "sha256": sha256_file(args.parpola_1994_pages),
    }
    pins["parpola_2010_extracted_pages"] = {
        "path": str(args.parpola_2010_pages),
        "sha256": sha256_file(args.parpola_2010_pages),
    }
    pins["mahadevan_1977_sign_list_json"] = {
        "path": "glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list.json",
        "sha256": sha256_file(repo_root / "glossa-corpus/indus/sources/mahadevan-1977/m77_sign_list.json"),
        "extraction_pin": M77_PINNED_JSON_SHA256,
    }
    pins["t202_locator_artifact"] = {
        "path": T202_ARTIFACT_REL,
        "sha256": sha256_file(repo_root / T202_ARTIFACT_REL),
    }
    return pins


# ---------------------------------------------------------------------------
# Delta against the T202 census
# ---------------------------------------------------------------------------


def build_delta(t202: dict, supp: dict) -> dict:
    t202_by = {e["sign"]: e for e in t202["entries"]}
    changes = []
    per_entry = []
    counts = {field: {"changed": 0, "unchanged": 0} for field in FIELDS}
    for entry in supp["entries"]:
        sign = entry["sign"]
        row = {"sign": sign}
        for field in FIELDS:
            before = t202_by[sign][field]["outcome"]
            after = entry[field]["outcome"]
            if before == after:
                counts[field]["unchanged"] += 1
                row[field] = "unchanged"
            else:
                counts[field]["changed"] += 1
                row[field] = f"changed: {before} -> {after}"
                changes.append({
                    "sign": sign,
                    "field": field,
                    "from": before,
                    "to": after,
                    "locator": entry[field]["locator"],
                })
        per_entry.append(row)
    return {
        "delta_of": {
            "t202_artifact": T202_ARTIFACT_REL,
            "t202_run_id": t202["run_id"],
            "supplement_artifact": ARTIFACT_REL,
            "supplement_run_id": supp["run_id"],
        },
        "merge_rule": (
            "read the T202 artifact and the supplement together; per entry "
            "per field, the supplement's outcome wins. The T202 artifact "
            "and its records are not modified."
        ),
        "summary": {
            "n_entries": supp["summary"]["n_entries"],
            **{field: counts[field] for field in FIELDS},
            "t202_census": {f: t202["summary"][f] for f in FIELDS},
            "supplement_census": {f: supp["summary"][f] for f in FIELDS},
        },
        "changes": changes,
        "per_entry": per_entry,
    }


# ---------------------------------------------------------------------------
# Sample verification (rule fixed in the stage record before sampling,
# mirroring T202: every located outcome as a census, plus every 12th
# entry in sign order from the 1st, plus every compilation-hit entry)
# ---------------------------------------------------------------------------


def verify_sample_supp(repo_root: Path, record: dict, sources: list[Source]) -> dict:
    provenance, crosswalk, _pins = base.load_inputs(repo_root)
    run_date = record["run_date"]
    by_sign = {e["sign"]: e for e in record["entries"]}
    prov_by_sign = {e["sign"]: e for e in provenance["entries"]}
    results = []
    for sign in base.sample_signs(record):
        prov_entry = prov_by_sign[sign]
        ctx = base.entry_context(prov_entry, crosswalk.get(sign))
        per_field = {}
        ok = True
        for field in FIELDS:
            field_ctx = dict(ctx)
            field_ctx["staged_value"] = prov_entry[field]["value"]
            field_ctx["source_as_stated"] = prov_entry[field]["source_as_stated"]
            rederived = build_outcome_supp(field_ctx, field, sources, run_date)
            filed = by_sign[sign][field]
            match = (
                rederived["outcome"] == filed["outcome"]
                and rederived.get("locator") == filed.get("locator")
                and (
                    filed["outcome"] == "located"
                    or base._search_facts(rederived) == base._search_facts(filed)
                )
            )
            per_field[field] = {
                "filed_outcome": filed["outcome"],
                "rederived_outcome": rederived["outcome"],
                "match": match,
            }
            ok = ok and match
        results.append({"sign": sign, "fields": per_field, "verified": ok})
    locator_signs = {
        e["sign"] for e in record["entries"] for f in FIELDS if e[f]["outcome"] == "located"
    }
    verified_signs = {r["sign"] for r in results if r["verified"]}
    return {
        "run_id": record["run_id"],
        "sample_rule": (
            "every entry carrying a locator (census), plus every 12th entry "
            "in sign order starting with the 1st, plus every entry whose "
            "phoneme-map consultation hit"
        ),
        "n_sampled": len(results),
        "n_locators_in_record": sum(
            1 for e in record["entries"] for f in FIELDS if e[f]["outcome"] == "located"
        ),
        "all_locators_verified": locator_signs <= verified_signs,
        "results": results,
        "all_verified": all(r["verified"] for r in results),
    }


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------


def execute(repo_root: Path, args) -> dict:
    provenance, crosswalk, _pins = base.load_inputs(repo_root)
    sources = build_supplement_sources(
        repo_root,
        parpola_1994_pdf=args.parpola_1994_pdf,
        parpola_2010_pdf=args.parpola_2010_pdf,
        parpola_1994_pages_path=args.parpola_1994_pages,
        parpola_2010_pages_path=args.parpola_2010_pages,
    )
    pins = supplement_input_pins(repo_root, args)
    started = datetime.now(timezone.utc)
    run_id = run_records.mint_run_id("study", now=started)
    run_date = started.date().isoformat()
    record = build_record_supp(
        provenance, crosswalk, sources,
        run_id=run_id, run_date=run_date, input_pins=pins,
    )
    artifact_path = repo_root / ARTIFACT_REL
    payload = json.dumps(record, indent=1, ensure_ascii=True) + "\n"
    write_file_verified(artifact_path, payload.encode("utf-8"))
    artifact_sha = sha256_file(artifact_path)

    code_version = "unknown"
    try:
        import subprocess

        code_version = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repo_root,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        pass
    finished = datetime.now(timezone.utc)
    header = run_records.build_header(
        surface="study",
        tool=f"{TOOL_NAME} --execute",
        tool_version=TOOL_VERSION,
        command=f"{TOOL_NAME} --execute",
        code_version=code_version,
        input_pins={
            "spec": "091-anchor-comparison-integrity",
            "stage": "stage-2-locator-pass-supplement",
            "supplements_run": T202_RUN_ID,
            "run_defs_note": (
                "tasks.md names 'run-defs v1' for the Stage 2 run; the "
                "landed T202 run was executed and recorded under run-defs "
                "v2 (run record study-20261117T105335Z-4d667e). This "
                "supplement is likewise executed under run-defs v2 and "
                "notes the naming discrepancy the same way Stage 2 did."
            ),
            "frozen_artifacts": {
                "provenance_sha256": pins["provenance"]["sha256"],
                "crosswalk_sha256": pins["crosswalk"]["sha256"],
                "t202_locator_artifact_sha256": pins["t202_locator_artifact"]["sha256"],
            },
            "search_sources": {
                "parpola_1994_pdf_sha256": PARPOLA_1994_PDF_SHA256,
                "parpola_2010_pdf_sha256": PARPOLA_2010_PDF_SHA256,
                "mahadevan_1977_sign_list_csv_sha256": M77_PINNED_CSV_SHA256,
                "mahadevan_1977_sign_list_json_sha256": M77_PINNED_JSON_SHA256,
                "wells_1998_sign_list_sha256": pins["wells_1998_sign_list"]["sha256"],
                "phoneme_compilation_sha256": pins["phoneme_compilation"]["sha256"],
            },
            "generator_sha256": sha256_file(Path(__file__)),
            "eligibility_defs": "specs/091-anchor-comparison-integrity/eligibility-defs-v1.md",
        },
        seed=run_records.NO_SEED,
        environment_class="mini-server/linux",
        started=started,
        finished=finished,
        run_id=run_id,
    )
    run_record = run_records.build_record(
        header,
        result={
            "artifact": ARTIFACT_REL,
            "artifact_sha256": artifact_sha,
            "census": record["summary"],
        },
    )
    store = repo_root / SPEC_RECORDS_REL
    written = run_records.write_run_record(store, run_record)
    return {
        "run_id": run_id,
        "artifact": ARTIFACT_REL,
        "artifact_sha256": artifact_sha,
        "run_record": str(written.relative_to(repo_root)),
        "census": record["summary"],
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--parpola-1994-pdf", type=Path)
    parser.add_argument("--parpola-2010-pdf", type=Path)
    parser.add_argument("--parpola-1994-pages", type=Path)
    parser.add_argument("--parpola-2010-pages", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--execute", action="store_true")
    group.add_argument("--verify-sample", action="store_true")
    group.add_argument("--delta", action="store_true")
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()

    if args.delta:
        t202 = json.loads((repo_root / T202_ARTIFACT_REL).read_text(encoding="utf-8"))
        supp = json.loads((repo_root / ARTIFACT_REL).read_text(encoding="utf-8"))
        delta = build_delta(t202, supp)
        out_path = repo_root / DELTA_REL
        write_file_verified(
            out_path,
            (json.dumps(delta, indent=1, ensure_ascii=True) + "\n").encode("utf-8"),
        )
        print(json.dumps({
            "written": DELTA_REL,
            "summary": delta["summary"],
            "n_changes": len(delta["changes"]),
        }, indent=1))
        return 0

    missing = [
        name for name in (
            "parpola_1994_pdf", "parpola_2010_pdf",
            "parpola_1994_pages", "parpola_2010_pages",
        )
        if getattr(args, name) is None
    ]
    if missing:
        parser.error(
            "--execute and --verify-sample require the custody inputs: "
            + ", ".join("--" + m.replace("_", "-") for m in missing)
        )

    if args.execute:
        outcome = execute(repo_root, args)
        print(json.dumps(outcome, indent=1))
        return 0

    artifact = json.loads((repo_root / ARTIFACT_REL).read_text(encoding="utf-8"))
    sources = build_supplement_sources(
        repo_root,
        parpola_1994_pdf=args.parpola_1994_pdf,
        parpola_2010_pdf=args.parpola_2010_pdf,
        parpola_1994_pages_path=args.parpola_1994_pages,
        parpola_2010_pages_path=args.parpola_2010_pages,
    )
    verification = verify_sample_supp(repo_root, artifact, sources)
    out_path = repo_root / VERIFICATION_REL
    write_file_verified(
        out_path,
        (json.dumps(verification, indent=1, ensure_ascii=True) + "\n").encode("utf-8"),
    )
    print(json.dumps({
        "run_id": verification["run_id"],
        "n_sampled": verification["n_sampled"],
        "all_verified": verification["all_verified"],
        "written": VERIFICATION_REL,
    }, indent=1))
    return 0 if verification["all_verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
