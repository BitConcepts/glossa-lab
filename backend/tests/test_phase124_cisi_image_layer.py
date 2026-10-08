"""Tests for Phase-124 CISI image layer (catalogue parsing + crop pipeline).

Covers: caption parsing for every printed caption form (spaced side,
compact side, bis, scale note, en-dash OCR variant) and rejection of
non-caption lines (in particular Indus-sign OCR garbage, which must
never be mistaken for a caption); header parsing (printed page, site,
object type, motif) incl. missing-field behaviour; texture-band photo
segmentation and sign-region segmentation on synthetic arrays;
caption-to-photo association incl. the unpaired case; and catalogue
row assembly (DJVU corroboration basis, low-confidence flagging, and
the explicit not-printed material/dimensions fields).
"""
from __future__ import annotations

import numpy as np

from glossa_lab.cisi_image_layer import (
    NOT_PRINTED, Header, OcrLine, PageRecord, associate_captions,
    build_page_rows, find_photo_boxes, find_photo_for_caption,
    parse_caption, parse_header, segment_sign_regions, texture_bands,
)


# ---------------------------------------------------------------- captions

def test_caption_spaced_side():
    c = parse_caption("M-67 A")
    assert c is not None
    assert (c.cisi_id, c.side, c.bis, c.scale_pct) == ("M-67", "A", False, None)
    assert c.photo_key == "M-67 A"


def test_caption_impression_side_lowercase():
    c = parse_caption("M-67 a")
    assert c is not None and c.side == "a"


def test_caption_compact_side_and_bis():
    c = parse_caption("M-666abis")
    assert c is not None
    assert (c.cisi_id, c.side, c.bis) == ("M-666", "a", True)
    assert c.photo_key == "M-666 a bis"


def test_caption_spaced_bis():
    c = parse_caption("M-213 A bis")
    assert c is not None and c.side == "A" and c.bis


def test_caption_scale_note():
    c = parse_caption("H-382 A (50 %)")
    assert c is not None and c.scale_pct == 50


def test_caption_no_side():
    c = parse_caption("M-666")
    assert c is not None and c.side == "" and c.photo_key == "M-666"


def test_caption_endash_variant():
    c = parse_caption("L-104 a".replace("-", "–"))
    assert c is not None and c.cisi_id == "L-104"


def test_caption_digit_one_read_as_i_or_l():
    c = parse_caption("M-IIA")
    assert c is not None and c.cisi_id == "M-11" and c.side == "A"
    assert c.id_normalized
    c2 = parse_caption("M-1la")
    assert c2 is not None and c2.cisi_id == "M-11" and c2.side == "a"
    assert parse_caption("M-11 A").id_normalized is False


def test_non_captions_rejected():
    for junk in ("TOYAUF", "XIKOT", "MOHENJO-DARO67-69SEALS", "30",
                 "'unicorn' III", "M-", "M-67 A extra words", ""):
        assert parse_caption(junk) is None, junk


# ----------------------------------------------------------------- headers

def test_header_full():
    h = parse_header(["30", "MOHENJO-DARO 67-69 SEALS", "'unicorn' III"])
    assert h.printed_page == 30
    assert h.site == "MOHENJO-DARO"
    assert h.object_type == "SEALS"
    assert h.motif == "unicorn"


def test_header_reversed_layout():
    h = parse_header(["'unicorn' II", "SEALS", "MOHENJO-DARO 665-667", "31"])
    assert h.printed_page == 31 and h.site == "MOHENJO-DARO"
    assert h.motif == "unicorn"


def test_header_ocr_merged_runs():
    # RapidOCR merges the header into single runs and loses the
    # motif's opening quote — both occur on real plates.
    h = parse_header(["10", "MOHENJO-DARO11-12SEALS", "unicorn'I,Il"])
    assert h.printed_page == 10 and h.site == "MOHENJO-DARO"
    assert h.object_type == "SEALS" and h.motif == "unicorn"


def test_header_missing_fields_not_invented():
    h = parse_header(["ADDENDA"])
    assert h.site == "ADDENDA" and h.object_type == "" and h.printed_page is None


# -------------------------------------------------------------- segmentation

def test_texture_bands_merge_and_min_len():
    prof = [0, 0, 30, 32, 0, 30, 0, 0, 28, 29, 30, 0]
    # runs (2,4)+(5,6) merge across a 1-wide gap; (8,11) is 2 away, kept apart
    assert texture_bands(prof, thresh=20, min_len=2, merge_gap=1) == [(2, 6), (8, 11)]
    assert texture_bands(prof, thresh=20, min_len=2, merge_gap=2) == [(2, 11)]


def _synthetic_plate():
    """White page, two grey 'photos' with darker content."""
    rng = np.random.default_rng(7)
    page = np.full((400, 300), 250, dtype=np.uint8)
    for (x, y, w, h) in ((30, 40, 110, 90), (170, 40, 110, 90)):
        page[y:y + h, x:x + w] = rng.integers(90, 210, size=(h, w),
                                              dtype=np.uint8)
    return page


def test_find_photo_boxes_synthetic():
    boxes = find_photo_boxes(_synthetic_plate(), std_thresh=15.0)
    assert len(boxes) == 2
    for (x, y, w, h), (ex, ey) in zip(boxes, ((30, 40), (170, 40))):
        assert abs(x - ex) <= 6 and abs(y - ey) <= 6
        assert abs(w - 110) <= 12 and abs(h - 90) <= 12


def test_find_photo_boxes_blank_page():
    blank = np.full((400, 300), 250, dtype=np.uint8)
    assert find_photo_boxes(blank) == []


def test_segment_sign_regions_synthetic():
    rng = np.random.default_rng(3)
    photo = rng.integers(150, 200, size=(200, 300), dtype=np.uint8)
    # three dark 'signs' in the top band, spaced apart
    for x in (20, 120, 220):
        photo[10:60, x:x + 45] = 40
    regions = segment_sign_regions(photo)
    assert len(regions) == 3
    xs = [r[0] for r in regions]
    assert xs == sorted(xs)
    for (x, y, w, h) in regions:
        assert y == 0 and h == int(0.42 * 200)


def test_segment_sign_regions_blank_photo():
    photo = np.full((200, 300), 200, dtype=np.uint8)
    assert segment_sign_regions(photo) == []


def test_find_photo_for_caption_synthetic():
    rng = np.random.default_rng(11)
    page = np.full((400, 300), 252, dtype=np.uint8)
    page[40:130, 30:140] = rng.integers(90, 210, size=(90, 110),
                                        dtype=np.uint8)
    box = find_photo_for_caption(page, cx=85, caption_top=140)
    assert box is not None
    x, y, w, h = box
    assert abs(x - 30) <= 8 and abs(y - 40) <= 8
    assert abs(w - 110) <= 16 and abs(h - 90) <= 16


def test_find_photo_for_caption_none_on_blank():
    page = np.full((400, 300), 252, dtype=np.uint8)
    assert find_photo_for_caption(page, cx=85, caption_top=140) is None


# -------------------------------------------------------------- association

def _line(text, score, x, y):
    return OcrLine(text=text, score=score, x=x, y=y, w=40, h=12)


def test_associate_caption_to_photo_above():
    photos = [(30, 40, 110, 90), (170, 40, 110, 90)]
    cap = parse_caption("M-1 A")
    assoc = associate_captions(photos, [(cap, _line("M-1 A", 0.99, 60, 140))],
                               page_h=400)
    assert assoc[0][0] == (30, 40, 110, 90)


def test_associate_unpaired_when_no_photo_above():
    cap = parse_caption("M-1 A")
    assoc = associate_captions([], [(cap, _line("M-1 A", 0.99, 60, 140))],
                               page_h=400)
    assert assoc[0][0] is None


# --------------------------------------------------------------------- rows

def test_build_page_rows_fields_and_flags():
    header = Header(printed_page=30, site="MOHENJO-DARO",
                    object_type="SEALS", motif="unicorn", raw="hdr")
    rec = PageRecord(volume=1, pdf_page=66, header=header)
    cap = parse_caption("M-67 A")
    assoc = [((30, 40, 110, 90), cap, _line("M-67 A", 0.99, 60, 140))]
    rows = build_page_rows(rec, [(30, 40, 110, 90)], assoc,
                           djvu_ids={"M-67"})
    assert len(rows) == 1
    r = rows[0]
    assert r["cisi_id"] == "M-67" and r["printed_page"] == 30
    assert r["site"] == "Mohenjo-Daro" and r["object_type"] == "Seals"
    assert r["extraction_basis"] == ("fresh_ocr_rapidocr"
                                     "+djvu_sequence_corroborated")
    assert r["confidence"] == "ok"
    assert r["material"] == "" and r["material_basis"] == NOT_PRINTED
    assert r["dimensions"] == "" and r["dimensions_basis"] == NOT_PRINTED


def test_build_page_rows_low_confidence_flagged_not_cleaned():
    header = Header(printed_page=None, site="", object_type="",
                    motif="", raw="")
    rec = PageRecord(volume=2, pdf_page=10, header=header)
    cap = parse_caption("H-9 a")
    assoc = [(None, cap, _line("H-9 a", 0.62, 60, 140))]
    rows = build_page_rows(rec, [], assoc, djvu_ids=set())
    r = rows[0]
    assert r["confidence"] == "low"
    assert "no photo associated" in r["notes"]
    assert r["extraction_basis"] == "fresh_ocr_rapidocr"
