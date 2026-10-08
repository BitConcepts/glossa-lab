"""Phase-124 — CISI image layer: catalogue extraction + sign-crop pipeline.

Enabling asset only. This module parses the *printed plate apparatus* of
the Corpus of Indus Seals and Inscriptions (CISI) vols. 1-2 — page
headers (printed page, site, object type, motif chapter) and photo
captions (CISI object ID + side + photographic scale) — and locates
seal/object photographs and inscription-band sign regions on rendered
pages. It asserts NO sign identifications and runs NO comparison study.

Storage governance: the source scans are in-copyright research copies.
Everything this module produces from them (catalogue table, crops) is a
derived research artifact for the gitignored local store only
(``corpora/downloads/cisi_image_layer/``); only this code, its tests,
the memo and a describing manifest are committed. See
``reports/phase124_cisi_image_layer.md``.

Dependencies are deliberately light (numpy + Pillow only) so the pure
parsing/segmentation logic is unit-testable without OCR or PDF stacks.
The driver (``scripts/phase124_cisi/``) supplies OCR lines (RapidOCR)
and rendered page arrays.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------- captions

# Printed caption form (verified visually against rendered plates):
#   "M-67 A"  "M-67 a"  "M-666a bis"  "H-382 A (50 %)"  "M-213 A bis"
# i.e. <prefix>-<number>[side][bis] [(scale %)]. OCR frequently drops the
# space before the side letter ("M-666abis") or before "bis", and reads
# the digit 1 as I or l ("M-IIA", "M-1la") — the number group therefore
# accepts [0-9Il] and normalises I/l to 1, flagging the row via
# ``id_normalized`` instead of silently cleaning it.
_CAPTION_RE = re.compile(
    r"^\s*([A-Z][A-Za-z]{0,2})-([0-9Il]{1,4})\s*"
    r"(?:([ABabCc])\s*)?(bis)?\s*"
    r"(?:\(\s*(\d{1,3})\s*%\s*\))?\s*$"
)
# OCR sometimes reads the hyphen as an en-dash or the ID with inner spaces.
_CAPTION_FIXUPS = (("–", "-"), ("—", "-"), ("−", "-"))


@dataclass(frozen=True)
class Caption:
    cisi_id: str            # canonical core ID, e.g. "M-666"
    prefix: str
    number: int
    side: str               # "A" (original), "a" (impression), "B"/"b"/"C"/"" …
    bis: bool               # duplicate/second exemplar marker as printed
    scale_pct: int | None   # photographic scale when printed, e.g. 50
    raw: str                # OCR text as read (never silently cleaned)
    id_normalized: bool = False  # number contained I/l glyphs read as 1

    @property
    def photo_key(self) -> str:
        """One catalogue row per photographed side of an object."""
        suffix = self.side + (" bis" if self.bis else "")
        return f"{self.cisi_id} {suffix}".strip()


def parse_caption(text: str) -> Caption | None:
    """Parse one OCR text line as a CISI plate caption; None if not a caption."""
    t = text.strip()
    for a, b in _CAPTION_FIXUPS:
        t = t.replace(a, b)
    t = re.sub(r"\s+", " ", t)
    # compact OCR variants: "M-666abis" -> "M-666a bis"; "M-69 a" already fine
    t = re.sub(r"(\d)([AaBbCc])bis$", r"\1 \2 bis", t)
    t = re.sub(r"(\d)bis$", r"\1 bis", t)
    m = _CAPTION_RE.match(t)
    if not m:
        return None
    prefix, num_raw, side, bis, scale = m.groups()
    normalized = any(ch in num_raw for ch in "Il")
    num = int(num_raw.replace("I", "1").replace("l", "1"))
    return Caption(
        cisi_id=f"{prefix}-{num}",
        prefix=prefix, number=num,
        side=side or "", bis=bool(bis),
        scale_pct=int(scale) if scale else None,
        raw=text, id_normalized=normalized,
    )


# ----------------------------------------------------------------- headers

_OBJECT_TYPES = (
    "SEALS AND INSCRIPTIONS", "INSCRIPTIONS", "SEALS", "TABLETS",
    "SEALINGS", "GRAFFITI", "POTTERY", "OBJECTS",
)
# Site names as printed in headers (upper case, hyphenated). No word
# boundaries on either side: OCR merges header runs
# ("MOHENJO-DARO11-12SEALS", "SEALSMOHENJO-DARO209-217"), so letters or
# digits may touch the site name directly.
_SITE_RE = re.compile(
    r"(MOHENJO-DARO|HARAPPA|LOTHAL|CHANHU-DARO|KALIBANGAN|BANAWALI|"
    r"RANGPUR|DHOLAVIRA|ROJDI|SURKOTADA|DESALPUR|JHUKAR|AMRI|KOT\s*DIJI|"
    r"CHANDIGARH|DELHI|BOMBAY|CALCUTTA|PATNA|MADRAS|LUCKNOW|VARANASI|"
    r"GWALIOR|ALLAHABAD|UNKNOWN|UNCERTAIN|VARIOUS|ADDENDA)"
)
_MOTIF_RE = re.compile(r"'([^']{2,60})'")
# OCR often loses the opening quote ("unicorn'I,Il"): fall back to the
# word(s) immediately before a surviving quote.
_MOTIF_FALLBACK_RE = re.compile(r"([A-Za-z][A-Za-z\- ]{1,40}?)'")


@dataclass(frozen=True)
class Header:
    printed_page: int | None
    site: str                 # "" when no site token is printed/readable
    object_type: str          # "" likewise
    motif: str                # ''-quoted chapter title, "" likewise
    raw: str


def parse_header(top_lines: list[str]) -> Header:
    """Parse the plate-page header from OCR lines in the top strip.

    ``top_lines`` are the OCR strings whose boxes fall in the header
    strip; order does not matter. The printed page number is the bare
    integer token; site/object-type/motif are matched against the
    vocabulary the volumes actually print.
    """
    raw = " ".join(s.strip() for s in top_lines if s.strip())
    up = raw.upper()
    printed = None
    for tok in raw.split():
        if tok.isdigit() and 1 <= int(tok) <= 999:
            printed = int(tok)
            break
    site_m = _SITE_RE.search(up)
    otype = next((t for t in _OBJECT_TYPES if t in up), "")
    motif_m = _MOTIF_RE.search(raw) or _MOTIF_FALLBACK_RE.search(raw)
    motif = motif_m.group(1).strip().strip("'").strip() if motif_m else ""
    # the fallback can swallow preceding header words; keep the last word
    # unless a quoted multi-word motif was read cleanly
    if motif_m and _MOTIF_RE.search(raw) is None and " " in motif:
        motif = motif.split()[-1]
    return Header(
        printed_page=printed,
        site=site_m.group(1).replace("  ", " ") if site_m else "",
        object_type=otype,
        motif=motif,
        raw=raw,
    )


# ------------------------------------------------------- texture segmentation
# Plate photographs are continuous-tone rectangles on a near-blank page:
# rows/columns crossing a photograph have far higher grey-level variance
# than margin rows. Segmentation works on that variance profile. All
# thresholds are parameters (documented in the Phase-124 memo); they are
# scale-relative so the same code runs at any render DPI.


def _runs(mask: list[bool], min_len: int, merge_gap: int) -> list[tuple[int, int]]:
    out: list[list[int]] = []
    start = None
    for i, v in enumerate(mask):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append([start, i])
            start = None
    if start is not None:
        out.append([start, len(mask)])
    merged: list[list[int]] = []
    for r in out:
        if merged and r[0] - merged[-1][1] <= merge_gap:
            merged[-1][1] = r[1]
        else:
            merged.append(list(r))
    return [(a, b) for a, b in merged if b - a >= min_len]


def texture_bands(profile, *, thresh: float, min_len: int,
                  merge_gap: int) -> list[tuple[int, int]]:
    """Runs of ``profile`` above ``thresh`` (start, end-exclusive)."""
    return _runs([float(p) > thresh for p in profile], min_len, merge_gap)


def find_photo_boxes(gray, *, std_thresh: float = 20.0,
                     min_frac: float = 0.035) -> list[tuple[int, int, int, int]]:
    """Locate plate photographs in a rendered page (numpy 2-D array).

    Returns ``(x, y, w, h)`` boxes sorted top-to-bottom, left-to-right.
    Row bands come from the per-row grey-level std over the inner page
    width; column bands likewise within each row band. Boxes smaller
    than ``min_frac`` of the page dimension in either axis are dropped
    (captions, header glyphs and body text fall below this on plates).
    """
    import numpy as np

    a = np.asarray(gray, dtype=float)
    h, w = a.shape
    inner = a[:, int(0.03 * w): int(0.97 * w)]
    row_prof = inner.std(axis=1)
    rows = texture_bands(row_prof, thresh=std_thresh,
                         min_len=int(min_frac * h), merge_gap=int(0.012 * h))
    boxes: list[tuple[int, int, int, int]] = []
    for (y0, y1) in rows:
        col_prof = a[y0:y1, :].std(axis=0)
        cols = texture_bands(col_prof, thresh=std_thresh,
                              min_len=int(min_frac * w),
                              merge_gap=int(0.012 * w))
        for (x0, x1) in cols:
            boxes.append((x0, y0, x1 - x0, y1 - y0))
    boxes.sort(key=lambda b: (b[1], b[0]))
    return boxes


def segment_sign_regions(photo, *, band_frac: float = 0.42,
                         min_w_frac: float = 0.045,
                         pad_frac: float = 0.02) -> list[tuple[int, int, int, int]]:
    """Heuristic sign-region boxes inside one seal/object photograph.

    CISI seal photographs carry the inscription in a band across the
    top of the object. Within the top ``band_frac`` of the photo, the
    per-column grey-level std (contrast) is smoothed and segmented
    into runs at an adaptive threshold (halfway between the median
    column, i.e. stone background, and the 95th-percentile column);
    each run is
    one candidate sign region. This is a *region proposal* heuristic —
    it asserts nothing about sign identity or count (adjacent signs
    that touch merge; motif elements intruding into the band split or
    add regions). Boxes are ``(x, y, w, h)`` in photo coordinates,
    sorted left-to-right, padded by ``pad_frac`` of the photo width.
    """
    import numpy as np

    a = np.asarray(photo, dtype=float)
    h, w = a.shape[:2]
    band_h = max(1, int(band_frac * h))
    band = a[:band_h]
    if band.ndim == 3:
        band = band.mean(axis=2)
    # Contrast projection, not darkness: the seal photographs are
    # raking-light relief — signs read as pale grooves with dark
    # shadow edges, so a dark-pixel projection mostly finds the
    # animal motif. Per-column grey-level std is high exactly where
    # carved strokes cross the band.
    proj = band.std(axis=0)
    # Smooth the projection first: a sign's strokes are separated by
    # narrow light gaps *inside* the sign, while the gaps *between*
    # signs are wider — a moving-average window of ~4.5 % of the photo
    # width fills the former without closing the latter.
    win = max(1, int(0.045 * w))
    kernel = np.ones(win) / win
    proj = np.convolve(proj, kernel, mode="same")
    # Adaptive threshold: halfway between the median column (stone
    # background) and the 95th-percentile column (carved sign).
    med = float(np.median(proj))
    hi = float(np.percentile(proj, 95))
    if hi - med < 4.0:
        return []
    thresh = med + 0.5 * (hi - med)
    runs = texture_bands(proj, thresh=thresh, min_len=int(min_w_frac * w),
                         merge_gap=int(0.015 * w))
    pad = int(pad_frac * w)
    out = []
    for (x0, x1) in runs:
        xa, xb = max(0, x0 - pad), min(w, x1 + pad)
        out.append((xa, 0, xb - xa, band_h))
    return out


def find_photo_for_caption(gray, cx: float, caption_top: float, *,
                           dark: int | None = None, row_frac: float = 0.28,
                           col_frac: float = 0.30, gap: int = 3,
                           half_window_frac: float = 0.17,
                           min_h_frac: float = 0.03,
                           min_w_frac: float = 0.05,
                           max_seek_frac: float = 0.045,
                           ) -> tuple[int, int, int, int] | None:
    """Locate the photograph directly above a caption (caption-anchored).

    Grid segmentation (row/column profiles) breaks on the staggered
    layouts of dense plates, so the primary locator is anchored on the
    caption itself — captions OCR reliably. From the caption centre,
    walk up while the per-row dark-pixel fraction (pixels < ``dark``,
    in a window ``half_window_frac`` of page width either side of the
    centre) stays above ``row_frac`` (gaps up to ``gap`` px tolerated):
    that run is the photo's vertical extent. Within it, walk left and
    right from the centre on the per-column dark fraction likewise.
    Returns ``(x, y, w, h)`` or None when no photo-sized region is
    found (the row is then kept, flagged, with no box).
    """
    import numpy as np

    a = np.asarray(gray)
    h, w = a.shape[:2]
    if a.ndim == 3:
        a = a.mean(axis=2)
    if dark is None:
        # Page-adaptive threshold: the two scans have different paper
        # tones (Vol. 1 corners ~248 grey, Vol. 2 ~234), so a fixed
        # threshold counts Vol. 2's bare paper as photograph. The
        # background is estimated from the corner patches; photo and
        # print sit well below it.
        corners = np.concatenate([
            a[:40, :40].ravel(), a[:40, -40:].ravel(),
            a[-40:, :40].ravel(), a[-40:, -40:].ravel()])
        dark = float(np.median(corners)) - 22.0
    half = int(half_window_frac * w)
    x0w = max(0, int(cx) - half)
    x1w = min(w, int(cx) + half)
    rows = (a[:, x0w:x1w] < dark).mean(axis=1)
    bottom = None
    y = min(h - 1, int(caption_top) - 1)
    seek_floor = y - int(max_seek_frac * h)
    gap_run = 0
    top = None
    while y >= 0:
        if rows[y] > row_frac:
            if bottom is None:
                bottom = y
            top = y
            gap_run = 0
        elif bottom is not None:
            gap_run += 1
            if gap_run > gap:
                break
        elif y < seek_floor:
            # No photo within reach above the caption: give up rather
            # than walking into the photograph above the previous one
            # (caption text rows are too sparse to pass row_frac, but
            # an unrestricted walk would eventually find *a* photo).
            break
        y -= 1
    if bottom is None or top is None or bottom - top < min_h_frac * h:
        return None
    cols = (a[top:bottom + 1, :] < dark).mean(axis=0)
    left = None
    x = int(cx)
    gap_run = 0
    while x >= 0:
        if cols[x] > col_frac:
            left = x
            gap_run = 0
        elif left is not None:
            gap_run += 1
            if gap_run > gap:
                break
        x -= 1
    right = None
    x = int(cx)
    gap_run = 0
    while x < w:
        if cols[x] > col_frac:
            right = x
            gap_run = 0
        elif right is not None:
            gap_run += 1
            if gap_run > gap:
                break
        x += 1
    if left is None or right is None or right - left < min_w_frac * w:
        return None
    return (left, top, right - left + 1, bottom - top + 1)


# -------------------------------------------------------------- association


@dataclass
class OcrLine:
    text: str
    score: float
    x: float
    y: float
    w: float
    h: float

    @property
    def cx(self) -> float:
        return self.x + self.w / 2.0

    @property
    def cy(self) -> float:
        return self.y + self.h / 2.0


def associate_captions(photos: list[tuple[int, int, int, int]],
                       captions: list[tuple[Caption, OcrLine]],
                       page_h: int, *, max_gap_frac: float = 0.07,
                       ) -> list[tuple[tuple[int, int, int, int] | None, Caption, OcrLine]]:
    """Pair each caption with the photo directly above it.

    A caption belongs to the photo whose x-range contains the caption
    centre and whose bottom edge is nearest above the caption, within
    ``max_gap_frac`` of the page height. Unpaired captions are returned
    with photo ``None`` (kept as catalogue rows, flagged).
    """
    out = []
    for cap, line in captions:
        best, best_gap = None, None
        for box in photos:
            x, y, w, h = box
            if x - 0.02 * w <= line.cx <= x + 1.02 * w:
                gap = line.y - (y + h)
                if  -0.01 * page_h <= gap <= max_gap_frac * page_h:
                    if best_gap is None or gap < best_gap:
                        best, best_gap = box, gap
        out.append((best, cap, line))
    return out


# ------------------------------------------------------------- catalogue rows

COLUMNS = [
    "volume", "cisi_id", "photo_key", "side", "bis", "caption_raw",
    "caption_ocr_score", "pdf_page", "printed_page", "site",
    "object_type", "motif_chapter", "scale_pct", "collection_scope",
    "material", "material_basis", "dimensions", "dimensions_basis",
    "photo_box_xywh", "extraction_basis", "confidence", "notes",
]

# What the volumes print, stated once (front matter / title pages,
# visually verified): vol. 1 covers collections in India; vol. 2 the
# named Pakistani museum collections. Per-object museum, material and
# dimensions are NOT printed on the plates — rows record that absence
# explicitly instead of filling it in from outside sources.
COLLECTION_SCOPE = {
    1: "Collections in India (volume-level scope, title page)",
    2: "Collections in Pakistan: National Museum Karachi, Mohenjo-daro "
       "Museum, Harappa Museum, Lahore Museum (volume-level scope, preface)",
}
NOT_PRINTED = "not printed per object in CISI plates"


@dataclass
class PageRecord:
    volume: int
    pdf_page: int
    header: Header
    rows: list[dict] = field(default_factory=list)


def build_page_rows(rec: PageRecord, photos, captions_assoc, *,
                    djvu_ids: set[str]) -> list[dict]:
    """Assemble catalogue rows for one plate page.

    ``captions_assoc`` is the output of :func:`associate_captions`.
    A row's confidence is ``low`` when the caption OCR score is < 0.90,
    the header yielded no site, or no photo could be associated.
    ``extraction_basis`` records fresh OCR, DJVU-sequence corroboration
    (the bundled djvu.txt carries no page breaks, so it can corroborate
    an ID's presence in the volume but never its page), or visual read.
    """
    rows = []
    for box, cap, line in captions_assoc:
        basis = "fresh_ocr_rapidocr"
        if cap.cisi_id in djvu_ids:
            basis += "+djvu_sequence_corroborated"
        low = (line.score < 0.90 or not rec.header.site or box is None
               or cap.id_normalized)
        notes = []
        if cap.id_normalized:
            notes.append("caption number contained I/l glyphs, read as 1")
        if box is None:
            notes.append("no photo associated")
        if not rec.header.site:
            notes.append("site not read from header")
        rows.append({
            "volume": rec.volume,
            "cisi_id": cap.cisi_id,
            "photo_key": cap.photo_key,
            "side": cap.side,
            "bis": "yes" if cap.bis else "",
            "caption_raw": cap.raw,
            "caption_ocr_score": round(line.score, 3),
            "pdf_page": rec.pdf_page,
            "printed_page": rec.header.printed_page or "",
            "site": rec.header.site.title() if rec.header.site else "",
            "object_type": rec.header.object_type.title(),
            "motif_chapter": rec.header.motif,
            "scale_pct": cap.scale_pct if cap.scale_pct else "",
            "collection_scope": COLLECTION_SCOPE.get(rec.volume, ""),
            "material": "",
            "material_basis": NOT_PRINTED,
            "dimensions": "",
            "dimensions_basis": NOT_PRINTED,
            "photo_box_xywh": ";".join(str(v) for v in box) if box else "",
            "extraction_basis": basis,
            "confidence": "low" if low else "ok",
            "notes": "; ".join(notes),
        })
    return rows
