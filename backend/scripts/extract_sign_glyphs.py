#!/usr/bin/env python3
"""Extract individual glyph images from scanned Fuls pages.

Loads each ``backend/data/fuls_page_*.png``, applies adaptive thresholding
to segment individual glyphs, filters by size/aspect-ratio, normalises each
glyph to a 64×64 white-background PNG, and saves them into
``backend/static/signs/``.

Usage::

    python backend/scripts/extract_sign_glyphs.py
"""
from __future__ import annotations

import glob
from pathlib import Path

import numpy as np
from PIL import Image

# ── Paths ────────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = _SCRIPT_DIR.parent
_DATA_DIR = _BACKEND_DIR / "data"
_OUTPUT_DIR = _BACKEND_DIR / "static" / "signs"

# ── Glyph extraction parameters ─────────────────────────────────────────
MIN_W, MAX_W = 15, 180
MIN_H, MAX_H = 15, 180
MIN_ASPECT, MAX_ASPECT = 0.2, 5.0
GLYPH_SIZE = 64  # normalised output size
PADDING = 4      # pixels of white padding inside the 64×64 canvas


def _adaptive_threshold(gray: np.ndarray, block_size: int = 31) -> np.ndarray:
    """Simple mean-based adaptive threshold (no OpenCV dependency).

    For each pixel the threshold is the local mean over a *block_size* window
    minus a small constant.  Returns a binary uint8 array (0 or 255) where
    foreground (ink) is 255.
    """
    from PIL import ImageFilter  # noqa: PLC0415

    # Use PIL box-blur as a fast local-mean approximation
    blurred = np.array(
        Image.fromarray(gray).filter(ImageFilter.BoxBlur(block_size // 2)),
        dtype=np.float32,
    )
    # Pixels darker than local mean - offset are foreground (ink)
    offset = 12.0
    binary = np.where(gray.astype(np.float32) < blurred - offset, 255, 0).astype(
        np.uint8
    )
    return binary


def _flood_fill_label(binary: np.ndarray) -> tuple[np.ndarray, int]:
    """Connected-component labelling via iterative flood fill.

    Uses scipy.ndimage.label when available; falls back to a pure-numpy BFS
    implementation otherwise.

    Returns ``(labels, num_labels)`` where *labels* is an int32 array of the
    same shape as *binary* and *num_labels* is the count of distinct components.
    """
    try:
        from scipy.ndimage import label as scipy_label  # noqa: PLC0415

        return scipy_label(binary)
    except ImportError:
        pass

    # ── Pure-numpy BFS fallback ──────────────────────────────────────────
    h, w = binary.shape
    labels = np.zeros((h, w), dtype=np.int32)
    visited = binary == 0  # background already "visited"
    current_label = 0

    ys, xs = np.where(~visited)
    for start_y, start_x in zip(ys.tolist(), xs.tolist()):
        if visited[start_y, start_x]:
            continue
        current_label += 1
        queue = [(start_y, start_x)]
        visited[start_y, start_x] = True
        while queue:
            cy, cx = queue.pop()
            labels[cy, cx] = current_label
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((ny, nx))

    return labels, current_label


def _extract_glyphs_from_image(
    img_path: Path,
) -> list[Image.Image]:
    """Return a list of normalised 64×64 glyph images from *img_path*."""
    img = Image.open(img_path).convert("L")  # grayscale
    gray = np.array(img)

    # Adaptive threshold → binary foreground mask (ink = 255)
    binary = _adaptive_threshold(gray)

    # Label connected components
    labels, num_labels = _flood_fill_label(binary)

    glyphs: list[Image.Image] = []
    for label_id in range(1, num_labels + 1):
        ys, xs = np.where(labels == label_id)
        if len(ys) == 0:
            continue

        y0, y1 = int(ys.min()), int(ys.max()) + 1
        x0, x1 = int(xs.min()), int(xs.max()) + 1
        bw = x1 - x0
        bh = y1 - y0

        # Filter by size and aspect ratio
        if not (MIN_W <= bw <= MAX_W and MIN_H <= bh <= MAX_H):
            continue
        aspect = bw / bh
        if not (MIN_ASPECT <= aspect <= MAX_ASPECT):
            continue

        # Crop the glyph region from the original grayscale image
        crop = gray[y0:y1, x0:x1].copy()

        # Create a white canvas and paste the glyph centred with padding
        canvas_inner = GLYPH_SIZE - 2 * PADDING
        scale = min(canvas_inner / bw, canvas_inner / bh, 1.0)
        new_w = max(1, int(bw * scale))
        new_h = max(1, int(bh * scale))

        glyph_img = Image.fromarray(crop).resize(
            (new_w, new_h), Image.Resampling.LANCZOS
        )
        canvas = Image.new("L", (GLYPH_SIZE, GLYPH_SIZE), 255)
        paste_x = (GLYPH_SIZE - new_w) // 2
        paste_y = (GLYPH_SIZE - new_h) // 2
        canvas.paste(glyph_img, (paste_x, paste_y))

        # Convert to RGB white-background
        rgb = Image.new("RGB", (GLYPH_SIZE, GLYPH_SIZE), (255, 255, 255))
        rgb.paste(Image.merge("RGB", [canvas, canvas, canvas]), (0, 0))
        glyphs.append(rgb)

    return glyphs


def main() -> None:
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    page_pattern = str(_DATA_DIR / "fuls_page_*.png")
    page_files = sorted(glob.glob(page_pattern))

    if not page_files:
        print(f"No fuls_page_*.png files found in {_DATA_DIR}")
        print("Nothing to extract — the script will run when page images are added.")
        return

    total_extracted = 0
    for page_path_str in page_files:
        page_path = Path(page_path_str)
        page_name = page_path.stem  # e.g. "fuls_page_01"
        # Extract page number from filename
        page_num = page_name.replace("fuls_page_", "")

        glyphs = _extract_glyphs_from_image(page_path)
        for idx, glyph_img in enumerate(glyphs):
            out_name = f"extracted_page{page_num}_{idx:04d}.png"
            glyph_img.save(_OUTPUT_DIR / out_name, "PNG")

        print(f"{page_name}: {len(glyphs)} glyphs extracted")
        total_extracted += len(glyphs)

    print(f"\nTotal: {total_extracted} glyphs saved to {_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
