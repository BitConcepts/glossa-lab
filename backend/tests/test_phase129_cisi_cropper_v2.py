"""Tests for Phase-129 CISI sign-crop pipeline v2.

All fixtures are synthetic arrays (no CISI material): a "seal photo"
is a smooth stone-grey field with a slow illumination gradient and
carved signs drawn as dark-edged pale grooves in the top band —
the raking-light structure Phase-124 documented. Covers:
illumination normalisation, the local-std gate map, blank-photo
rejection, sign detection, the dark-photo case v1 failed on,
valley splitting of a merged pair, non-splitting of a single wide
sign, and determinism.
"""
from __future__ import annotations

import numpy as np

from glossa_lab.cisi_cropper_v2 import (
    illumination_normalize,
    local_std_map,
    segment_sign_regions_v2,
)


def _photo(w=420, h=300, *, gradient=60.0):
    """Stone-grey photo with a left-to-right illumination ramp."""
    ramp = np.linspace(0, gradient, w)[None, :]
    return 170.0 + ramp + np.zeros((h, w))


def _carve(photo, x0, x1, *, y0=18, y1=120, dark=70.0, pale=225.0):
    """Carve one sign: dark groove walls with a pale groove floor."""
    photo[y0:y1, x0:x1] = pale
    photo[y0:y1, x0:x0 + 5] = dark
    photo[y0:y1, x1 - 5:x1] = dark
    photo[y0:y0 + 5, x0:x1] = dark
    return photo


def _three_sign_photo(**kw):
    p = _photo(**kw)
    for x0, x1 in ((40, 95), (165, 225), (300, 355)):
        _carve(p, x0, x1)
    return p


def _overlap(a, b) -> float:
    x0 = max(a[0], b[0])
    x1 = min(a[0] + a[2], b[0] + b[2])
    return max(0, x1 - x0) / max(1, min(a[2], b[2]))


# ------------------------------------------------------------ normalisation

def test_normalize_flattens_gradient():
    p = _photo()
    n = illumination_normalize(p)
    # The 60-grey ramp is slow background: the residual keeps < 20 %
    # of the original left-to-right slope.
    slope = float(n[:, -20:].mean() - n[:, :20].mean())
    assert abs(slope) < 12.0


def test_normalize_preserves_sign_contrast():
    p = _three_sign_photo()
    n = illumination_normalize(p)
    inside = n[20:110, 45:90]
    outside = n[20:110, 110:150]
    assert inside.std() > 3 * max(outside.std(), 1.0)


def test_local_std_map_constant_image_is_zero():
    m = local_std_map(np.full((30, 30), 128.0), win=5)
    assert float(m.max()) == 0.0


# ------------------------------------------------------------- segmentation

def test_blank_photo_yields_no_regions():
    assert segment_sign_regions_v2(_photo()) == []


def test_three_signs_detected():
    boxes = segment_sign_regions_v2(_three_sign_photo())
    assert len(boxes) == 3
    for truth in ((40, 0, 55, 130), (165, 0, 60, 130), (300, 0, 55, 130)):
        assert any(_overlap(b, truth) > 0.5 for b in boxes), boxes


def test_dark_photo_still_detected():
    # Phase-124's M-213 A failure: the whole photo is dark and its
    # contrast compressed. Normalisation must recover the signs.
    p = 40.0 + 0.35 * (_three_sign_photo() - 40.0)
    boxes = segment_sign_regions_v2(p)
    assert len(boxes) == 3


def test_pale_grooves_on_mid_grey_detected():
    # Signs whose floors are *paler* than the stone and whose only
    # dark pixels are thin shadow edges — the raking-light case a
    # darkness projection misses.
    p = _photo(gradient=0.0)
    for x0, x1 in ((60, 115), (240, 300)):
        _carve(p, x0, x1, dark=120.0, pale=235.0)
    boxes = segment_sign_regions_v2(p)
    assert len(boxes) == 2


def test_merged_pair_split_at_valley():
    p = _photo()
    _carve(p, 100, 160)
    _carve(p, 168, 228)  # 8 px gap: v1's wide smoothing merged these
    boxes = segment_sign_regions_v2(p)
    assert len(boxes) == 2, boxes


def test_single_wide_sign_not_split():
    p = _photo()
    _carve(p, 140, 260)  # one wide sign, flat interior projection
    boxes = segment_sign_regions_v2(p)
    assert len(boxes) == 1, boxes


def test_boxes_within_photo_and_sorted():
    boxes = segment_sign_regions_v2(_three_sign_photo())
    assert boxes == sorted(boxes, key=lambda b: b[0])
    for x, y, w, h in boxes:
        assert 0 <= x and 0 <= y and x + w <= 420 and y + h <= 300
        assert h < 300  # fitted extent, never the whole photo


def test_deterministic():
    p = _three_sign_photo()
    assert segment_sign_regions_v2(p) == segment_sign_regions_v2(p.copy())


def test_top_border_does_not_collapse_crop_height():
    # A dark border line across the photo's top rows (the seal edge
    # against the page) is energetic at every x; the y-fit must
    # still frame the sign row below it, not the border strip.
    p = _three_sign_photo()
    p[0:3, :] = 95.0  # seal-edge strip, as dark as the groove walls
    boxes = segment_sign_regions_v2(p)
    assert boxes, "all signs lost to the border strip"
    for x, y, w, h in boxes:
        assert h >= 60, boxes  # no border-strip slivers
    for truth in ((40, 0, 55, 130), (165, 0, 60, 130), (300, 0, 55, 130)):
        assert any(_overlap(b, truth) > 0.5 for b in boxes), boxes
