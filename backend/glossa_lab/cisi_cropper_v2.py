"""Phase-129 — CISI sign-crop pipeline v2.

Successor to the Phase-124 heuristic in
:mod:`glossa_lab.cisi_image_layer` (``segment_sign_regions``, kept
untouched as the frozen v1 baseline). v2 attacks the failure modes
Phase-124 documented for the raking-light seal photographs — signs
render as *pale grooves with dark shadow edges*:

- v1 segmented a per-column grey-level std projection of the raw
  photo, smoothed with a wide (4.5 % of width) window and cut at a
  single halfway threshold. The wide smoothing merges adjacent
  signs and amputates narrow ones; the single threshold splits
  signs at low-contrast strokes; uneven exposure (the very dark
  M-213 A plate photo) compresses the projection's dynamic range;
  blank stretches that clear the threshold are emitted as empty
  crops; and every crop spans the full band height whether or not
  the sign does.

v2 keeps v1's interpretable core signal (per-column std — contrast,
not darkness, for the reason Phase-124 gave) and fixes the stages
around it, deterministically, CPU-only, numpy + Pillow only (no
neural models, per program doctrine):

1. **Illumination normalisation** — the slow background (multi-pass
   box blur at 18 % of photo width) is subtracted before any
   measurement, flattening raking-light falloff and lifting dark
   photos' contrast into a comparable range.
2. **Sharper projection** — smoothing drops from 4.5 % to 2.0 % of
   photo width, so narrow signs and the gaps between signs survive.
3. **Hysteresis edges** — runs are seeded above the high threshold
   (as v1's), then each edge is extended down to a low threshold,
   capped at the valley between neighbouring runs so extension can
   never bridge two signs. Faint groove tails are recovered
   without lowering the seed bar.
4. **Valley splitting** — a remaining over-wide run whose
   projection dips deep between two peaks is split at the valley
   (the "two signs merged" partial class).
5. **Content rejection** — a kept run must contain actual stroke
   pixels: local-std energy above a photo-level bar, spread across
   a minimum share of its columns. Near-uniform runs (blank seal
   edge, photo margin) are dropped instead of emitted as the empty
   crops Phase-124 graded *bad*.
6. **Band localisation** — each crop's vertical extent is fitted to
   the rows where the region's local energy actually lives
   (padded), instead of always spanning the full search band.

Storage governance is Phase-124's, unchanged: source scans and all
derived crops live only in the gitignored local store; this module
is pure array logic, unit-tested on synthetic arrays.
"""
from __future__ import annotations

# Frozen v2 parameter set (Phase-129 protocol §6: tuned on synthetic
# tests and aggregate diagnostics, then applied uniformly; the
# benchmark harness asserts a re-run reproduces the graded run).
BAND_FRAC = 0.42        # projection band: top fraction of the photo (as v1)
ZONE_FRAC = 0.50        # gate / y-fit zone: top fraction of the photo
WIN_FRAC = 0.030        # local-std window for the gate, fraction of width
SMOOTH_FRAC = 0.020     # projection smoothing, fraction of photo width (v1: 0.045)
HI_FRAC = 0.50          # seed threshold: med + f*(p97.5-med) (v1: p95, same f)
LO_FRAC = 0.22          # edge-extension floor: med + f*(p97.5-med)
MIN_W_FRAC = 0.042      # minimum region width, fraction of photo width (v1: 0.045)
SPLIT_W_FRAC = 0.075    # runs wider than this are valley-split candidates
VALLEY_RATIO = 0.72     # split if valley < ratio * lower of the two peaks
PAD_FRAC = 0.020        # horizontal padding, fraction of photo width
STROKE_MIN_FRAC = 0.015  # min share of stroke pixels inside a region
COL_COV_MIN = 0.30      # min share of region columns containing a stroke
ROW_KEEP_FRAC = 0.35    # rows kept above this share of the region row peak
ROW_PAD_FRAC = 0.030    # vertical padding, fraction of photo height
MIN_CONTRAST = 3.0      # grey levels; below this the band is called flat


def _box_blur(a, k: int):
    """Edge-padded moving average along both axes with odd window ``k``."""
    import numpy as np

    if k <= 1:
        return a.astype(float)
    assert k % 2 == 1, "box-blur window must be odd"
    pad = k // 2
    for axis in (0, 1):
        widths = [(pad, pad) if i == axis else (0, 0) for i in range(2)]
        ap = np.pad(a, widths, mode="edge")
        c = np.cumsum(ap, axis=axis, dtype=float)
        zero = np.take(c, [0], axis=axis) * 0.0
        c = np.concatenate([zero, c], axis=axis)
        n = a.shape[axis]
        hi = c.take(indices=range(k, k + n), axis=axis)
        lo = c.take(indices=range(0, n), axis=axis)
        a = (hi - lo) / k
    return a


def illumination_normalize(gray, *, blur_frac: float = 0.18):
    """Flatten slow illumination gradients (raking-light falloff).

    Returns ``gray - background + mean(background)`` where the
    background is a multi-pass box blur at ``blur_frac`` of the photo
    width — wide enough to span several signs, so carved strokes
    (narrow) survive in the residual while the lighting slope and
    the photo's overall exposure level are removed.
    """
    import numpy as np

    a = np.asarray(gray, dtype=float)
    if a.ndim == 3:
        a = a.mean(axis=2)
    k = max(3, int(blur_frac * a.shape[1]) | 1)
    bg = a
    for _ in range(3):
        bg = _box_blur(bg, k)
    return a - bg + float(bg.mean())


def local_std_map(a, *, win: int):
    """Per-pixel local standard deviation (sliding ``win`` x ``win``)."""
    import numpy as np

    mean = _box_blur(a, win)
    sq = _box_blur(a * a, win)
    var = np.maximum(sq - mean * mean, 0.0)
    return np.sqrt(var)


def _runs_above(proj, thresh: float) -> list[tuple[int, int]]:
    """Maximal [x0, x1) runs where ``proj >= thresh``."""
    runs, x = [], 0
    n = len(proj)
    while x < n:
        if proj[x] >= thresh:
            x0 = x
            while x < n and proj[x] >= thresh:
                x += 1
            runs.append((x0, x))
        else:
            x += 1
    return runs


def _extend_runs(proj, runs, t_lo: float) -> list[tuple[int, int]]:
    """Extend each run's edges down to ``t_lo``, capped at gap valleys.

    The cap is the argmin of the projection in the gap to the
    neighbouring run: extension into a shared valley stops there,
    so two seeded runs can never be bridged by their own tails.
    """
    import numpy as np

    out = []
    for i, (x0, x1) in enumerate(runs):
        left_cap = 0
        if i > 0:
            gap = proj[runs[i - 1][1]:x0]
            left_cap = runs[i - 1][1] + int(np.argmin(gap)) if len(gap) \
                else runs[i - 1][1]
        right_cap = len(proj)
        if i + 1 < len(runs):
            gap = proj[x1:runs[i + 1][0]]
            right_cap = x1 + int(np.argmin(gap)) if len(gap) \
                else runs[i + 1][0]
        a_ = x0
        while a_ > left_cap and proj[a_ - 1] >= t_lo:
            a_ -= 1
        b_ = x1
        while b_ < right_cap and proj[b_] >= t_lo:
            b_ += 1
        out.append((a_, b_))
    return out


def _valley_split(proj, x0: int, x1: int, *, min_w: int,
                  t_hi: float, width_ref: int,
                  depth: int = 0) -> list[tuple[int, int]]:
    """Recursively split an over-wide run at its deepest interior valley."""
    if depth >= 3 or x1 - x0 <= max(int(SPLIT_W_FRAC * width_ref), 2 * min_w):
        return [(x0, x1)]
    lo = x0 + min_w
    hi = x1 - min_w
    if hi <= lo:
        return [(x0, x1)]
    import numpy as np

    seg = proj[lo:hi]
    cut = lo + int(np.argmin(seg))
    left_peak = float(proj[x0:cut + 1].max())
    right_peak = float(proj[cut:x1].max())
    if proj[cut] < VALLEY_RATIO * min(left_peak, right_peak) \
            and proj[cut] < t_hi:
        return (_valley_split(proj, x0, cut, min_w=min_w, t_hi=t_hi,
                              width_ref=width_ref, depth=depth + 1)
                + _valley_split(proj, cut, x1, min_w=min_w, t_hi=t_hi,
                                width_ref=width_ref, depth=depth + 1))
    return [(x0, x1)]


def segment_sign_regions_v2(photo, *, band_frac: float = BAND_FRAC,
                            zone_frac: float = ZONE_FRAC,
                            ) -> list[tuple[int, int, int, int]]:
    """v2 sign-region boxes inside one seal/object photograph.

    ``photo`` is a greyscale array (photo coordinates, as in v1).
    Returns ``(x, y, w, h)`` boxes sorted left-to-right. Region
    proposals only — no sign identity or count is asserted.
    """
    import numpy as np

    a = np.asarray(photo, dtype=float)
    if a.ndim == 3:
        a = a.mean(axis=2)
    h, w = a.shape
    norm = illumination_normalize(a)
    band_h = max(1, int(band_frac * h))
    band = norm[:band_h]

    # Core signal (as v1): per-column contrast over the band — std,
    # not darkness, because raking-light signs are pale grooves with
    # dark edges. Computed on the normalised photo, lightly smoothed.
    proj = band.std(axis=0)
    swin = max(1, int(SMOOTH_FRAC * w))
    if swin > 1:
        proj = np.convolve(proj, np.ones(swin) / swin, mode="same")
    med = float(np.median(proj))
    hi_p = float(np.percentile(proj, 97.5))
    if hi_p - med < MIN_CONTRAST:
        return []
    t_hi = med + HI_FRAC * (hi_p - med)
    t_lo = med + LO_FRAC * (hi_p - med)

    min_w = max(1, int(MIN_W_FRAC * w))
    runs = [(x0, x1) for x0, x1 in _runs_above(proj, t_hi)
            if x1 - x0 >= max(1, min_w // 2)]
    runs = _extend_runs(proj, runs, t_lo)
    split: list[tuple[int, int]] = []
    for x0, x1 in runs:
        split.extend(_valley_split(proj, x0, x1, min_w=min_w,
                                   t_hi=t_hi, width_ref=w))
    runs = [(x0, x1) for x0, x1 in split if x1 - x0 >= min_w]

    # Content gate + vertical extent from the local-energy map.
    zone_h = max(1, int(zone_frac * h))
    win = max(3, int(WIN_FRAC * w) | 1)
    energy = local_std_map(norm[:zone_h], win=win)
    e_med = float(np.median(energy))
    e_hi = float(np.percentile(energy, 95))
    e_thr = e_med + 0.5 * (e_hi - e_med)
    pad = int(PAD_FRAC * w)
    row_pad = int(ROW_PAD_FRAC * h)
    out: list[tuple[int, int, int, int]] = []
    for x0, x1 in runs:
        sub = energy[:, x0:x1]
        stroke_frac = float((sub > e_thr).mean())
        col_cov = float((sub > e_thr).any(axis=0).mean())
        if stroke_frac < STROKE_MIN_FRAC or col_cov < COL_COV_MIN:
            continue
        row_prof = sub.mean(axis=1).copy()
        # The photo's own border rows are energetic at *every* x
        # (seal edge against page background); letting them win the
        # peak search collapses the crop onto the border strip.
        # Mask the outermost rows for detection (they remain
        # available via padding), then take the contiguous run
        # around the peak; if that run is implausibly short for a
        # sign row, fall back to the full v1 band.
        row_prof[:2] = 0.0
        row_prof[-2:] = 0.0
        peak_row = int(np.argmax(row_prof))
        thr_r = ROW_KEEP_FRAC * float(row_prof[peak_row])
        y0 = peak_row
        while y0 > 0 and row_prof[y0 - 1] > thr_r:
            y0 -= 1
        y1 = peak_row
        while y1 < zone_h - 1 and row_prof[y1 + 1] > thr_r:
            y1 += 1
        if y1 + 1 - y0 < 0.15 * zone_h:
            y0, y1 = 0, max(1, int(band_frac * h)) - 1
        ya = max(0, y0 - row_pad)
        yb = min(zone_h, y1 + 1 + row_pad)
        xa = max(0, x0 - pad)
        xb = min(w, x1 + pad)
        out.append((xa, ya, xb - xa, yb - ya))
    out.sort(key=lambda b: b[0])
    return out
