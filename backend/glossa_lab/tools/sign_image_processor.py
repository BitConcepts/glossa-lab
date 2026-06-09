"""Sign Image Processor — Indus script sign image acquisition and processing pipeline.

Acquisition pipeline (tried in priority order per sign):
  1. WikiMedia Commons  — SVG/PNG individual sign files where they exist
  2. Mahadevan grid     — Extract from a supplied sign-table page image
                          (user places page scans in static/signs/source_pages/)
  3. Iconic fallback    — PIL-rendered geometric reconstruction from iconic description

Processing (applied to every acquired image):
  • Convert to grayscale
  • Otsu threshold → pure black ink on white ground
  • Auto-crop to content bounding box with 12 % padding
  • Pad to square
  • Resize to SIGN_SIZE × SIGN_SIZE (default 128 px)

Output layout:
  static/signs/{sign_id}.png          — processed image served by the API
  static/signs/originals/{sign_id}.png — raw source crop (kept for recheck)
  static/signs/manifest.json          — per-sign provenance & status tracking

CLI usage:
  python -m glossa_lab.tools.sign_image_processor --all
  python -m glossa_lab.tools.sign_image_processor --sign M047
  python -m glossa_lab.tools.sign_image_processor --grid source_pages/mahadevan_table.png
  python -m glossa_lab.tools.sign_image_processor --status
"""
from __future__ import annotations

import argparse
import json
import logging
import time
import urllib.request
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

_log = logging.getLogger("glossa_lab.tools.sign_image_processor")

# ── Constants ──────────────────────────────────────────────────────────────
SIGN_SIZE = 128          # Output image size (square)
STROKE_WIDTH = 3         # Pen width for fallback icons
FONT_SIZE = 18

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_STATIC_SIGNS   = _BACKEND_DIR / "static" / "signs"
_ORIGINALS_DIR  = _STATIC_SIGNS / "originals"
_SOURCE_PAGES   = _STATIC_SIGNS / "source_pages"
_MANIFEST_PATH  = _STATIC_SIGNS / "manifest.json"
_CROSSWALK_PATH = _BACKEND_DIR.parent / "glossa-corpus" / "indus" / "canonical" / "sign_crosswalk.json"
_ANCHORS_PATH   = _BACKEND_DIR / "reports" / "INDUS_FINAL_ANCHORS.json"

# WikiMedia Commons API
_WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"

# Request headers (polite bot identifier)
_HEADERS = {
    "User-Agent": "GlossaLabSignProcessor/1.0 (research; contact: glossa@bitconcepts.tech)"
}

# Local Fuls catalog pages (data/fuls_page_*.png)
_DATA_DIR = _BACKEND_DIR.parent / "data"

# ── Sign number patterns tried on WikiMedia ────────────────────────────────
# Patterns are tried in order; first hit wins.  WikiMedia Commons has files
# under BOTH Parpola sign numbers and Mahadevan numbers — we try both.
# Confirmed existing patterns (from Commons category scan 2026-06):
#   "Indus sign {n}.png"          — Parpola numbers, NO zero-padding
#   "Indus script sign {n:03d}.svg" — only ~1 confirmed (sign 045)
_WM_PATTERNS_MAHADEVAN = [
    "Indus_script_sign_{n:03d}.svg",
    "Indus_script_sign_{n}.svg",
    "Indus_sign_{n}.svg",
    "Indus_Valley_sign_{n:03d}.svg",
    "Indus_Valley_sign_{n}.svg",
    "Indus_script_sign_{n:03d}.png",
    "Indus_script_sign_{n}.png",
]
# Parpola-number patterns (confirmed to exist on WikiMedia Commons)
_WM_PATTERNS_PARPOLA = [
    "Indus_sign_{n}.png",
    "Indus_script_sign_{n}.png",
    "Indus_script_sign_{n:03d}.svg",
    "Indus_sign_{n}.svg",
]
# Legacy alias kept for compatibility
_WM_PATTERNS = _WM_PATTERNS_MAHADEVAN

# ── Mahadevan concordance sign grid layout ─────────────────────────────────
# The standard Mahadevan 1977 sign table has 417 signs in a roughly 24×18 grid.
# These dimensions depend on which version of the table is used.
# User can override by placing a JSON spec alongside the source page image.
_DEFAULT_GRID = {
    "rows": 24,
    "cols": 18,
    "start_id": 1,   # Mahadevan number of first sign (top-left)
}

# ── Iconic description → draw function map ────────────────────────────────
# Maps keyword patterns to drawing functions that produce fallback icons.

def _draw_strokes(draw: ImageDraw.ImageDraw, n: int, size: int) -> None:
    """Draw n vertical strokes evenly spaced."""
    s = STROKE_WIDTH
    total_w = size * 0.7
    gap = total_w / max(n, 1)
    x_start = size * 0.15 + gap / 2
    y_top = size * 0.15
    y_bot = size * 0.85
    for i in range(n):
        x = x_start + i * gap
        draw.line([(x, y_top), (x, y_bot)], fill=0, width=s)


def _draw_fish(draw: ImageDraw.ImageDraw, size: int, modifier: str = "") -> None:
    """Draw a simple fish glyph."""
    s = STROKE_WIDTH
    cx, cy = size // 2, size // 2
    r = int(size * 0.28)
    # Body (oval)
    draw.ellipse([(cx - r, cy - int(r * 0.55)), (cx + r, cy + int(r * 0.55))],
                 outline=0, width=s)
    # Tail (two diagonal lines)
    tx = cx + r
    draw.line([(tx, cy), (tx + int(r * 0.45), cy - int(r * 0.4))], fill=0, width=s)
    draw.line([(tx, cy), (tx + int(r * 0.45), cy + int(r * 0.4))], fill=0, width=s)
    # Optional modifier above/below the body
    if "roof" in modifier:
        roof_y = cy - int(r * 0.65)
        draw.line([(cx - int(r * 0.5), roof_y), (cx + int(r * 0.5), roof_y)], fill=0, width=s)
    if "trefoil" in modifier:
        for dx in [-int(r * 0.25), 0, int(r * 0.25)]:
            draw.ellipse([(cx + dx - 4, cy - r - 12), (cx + dx + 4, cy - r - 4)],
                         outline=0, width=s - 1)
    if "fins" in modifier:
        draw.line([(cx - int(r * 0.15), cy - int(r * 0.6)), (cx, cy - int(r * 0.3))],
                  fill=0, width=s)


def _draw_bull(draw: ImageDraw.ImageDraw, size: int, humped: bool = True) -> None:
    """Draw a simplified zebu bull / bovine silhouette."""
    s = STROKE_WIDTH
    # Body
    bx0, by0, bx1, by1 = size*0.2, size*0.38, size*0.78, size*0.72
    draw.ellipse([(bx0, by0), (bx1, by1)], outline=0, width=s)
    # Head (small circle)
    hcx = size * 0.18
    draw.ellipse([(hcx - 12, size*0.32), (hcx + 12, size*0.58)], outline=0, width=s)
    # Horns
    draw.line([(hcx - 6, size*0.32), (hcx - 16, size*0.20)], fill=0, width=s)
    draw.line([(hcx + 6, size*0.32), (hcx + 16, size*0.20)], fill=0, width=s)
    # Legs
    leg_ys = [(size*0.72, size*0.9)]
    for lx in [size*0.31, size*0.45, size*0.59, size*0.70]:
        draw.line([(lx, size*0.72), (lx, size*0.90)], fill=0, width=s)
    # Hump
    if humped:
        draw.arc([(size*0.36, size*0.24), (size*0.60, size*0.50)], 200, 340, fill=0, width=s)


def _draw_animal_generic(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Generic four-legged animal silhouette."""
    s = STROKE_WIDTH
    draw.ellipse([(size*0.22, size*0.32), (size*0.80, size*0.68)], outline=0, width=s)
    draw.ellipse([(size*0.10, size*0.28), (size*0.28, size*0.52)], outline=0, width=s)
    for lx in [size*0.30, size*0.44, size*0.58, size*0.70]:
        draw.line([(lx, size*0.68), (lx, size*0.88)], fill=0, width=s)


def _draw_man(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Stick figure with raised arm."""
    s = STROKE_WIDTH
    cx = size // 2
    # Head
    draw.ellipse([(cx-12, 8), (cx+12, 32)], outline=0, width=s)
    # Body
    draw.line([(cx, 32), (cx, 74)], fill=0, width=s)
    # Raised arm
    draw.line([(cx, 48), (cx - 22, 28)], fill=0, width=s)
    # Other arm
    draw.line([(cx, 48), (cx + 20, 62)], fill=0, width=s)
    # Legs
    draw.line([(cx, 74), (cx - 18, 100)], fill=0, width=s)
    draw.line([(cx, 74), (cx + 18, 100)], fill=0, width=s)


def _draw_jar(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Draw a pot / jar shape."""
    s = STROKE_WIDTH
    cx = size // 2
    draw.ellipse([(cx-28, size*0.38), (cx+28, size*0.85)], outline=0, width=s)
    draw.line([(cx-20, size*0.38), (cx-14, size*0.22)], fill=0, width=s)
    draw.line([(cx+20, size*0.38), (cx+14, size*0.22)], fill=0, width=s)
    draw.line([(cx-14, size*0.22), (cx+14, size*0.22)], fill=0, width=s)


def _draw_cross(draw: ImageDraw.ImageDraw, size: int) -> None:
    s = STROKE_WIDTH * 2
    m = size // 2
    draw.line([(m, size*0.15), (m, size*0.85)], fill=0, width=s)
    draw.line([(size*0.15, m), (size*0.85, m)], fill=0, width=s)


def _draw_circle(draw: ImageDraw.ImageDraw, size: int, dotted: bool = False) -> None:
    s = STROKE_WIDTH
    pad = int(size * 0.18)
    draw.ellipse([(pad, pad), (size-pad, size-pad)], outline=0, width=s)
    if dotted:
        c = size // 2
        draw.ellipse([(c-5, c-5), (c+5, c+5)], fill=0)


def _draw_gharial(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Simplified gharial / crocodile side view."""
    s = STROKE_WIDTH
    # Long body
    draw.ellipse([(size*0.18, size*0.40), (size*0.80, size*0.68)], outline=0, width=s)
    # Elongated snout
    draw.line([(size*0.18, size*0.52), (size*0.04, size*0.52)], fill=0, width=s+1)
    draw.line([(size*0.04, size*0.48), (size*0.04, size*0.56)], fill=0, width=s)
    # Tail
    draw.line([(size*0.80, size*0.54), (size*0.96, size*0.42)], fill=0, width=s)
    # Legs
    for lx in [size*0.35, size*0.55, size*0.65]:
        draw.line([(lx, size*0.68), (lx, size*0.84)], fill=0, width=s)


def _draw_elephant(draw: ImageDraw.ImageDraw, size: int) -> None:
    s = STROKE_WIDTH
    # Body
    draw.ellipse([(size*0.24, size*0.28), (size*0.84, size*0.72)], outline=0, width=s)
    # Head
    draw.ellipse([(size*0.08, size*0.24), (size*0.30, size*0.56)], outline=0, width=s)
    # Trunk
    draw.arc([(size*0.02, size*0.48), (size*0.22, size*0.82)], 0, 270, fill=0, width=s)
    # Tusk
    draw.line([(size*0.10, size*0.46), (size*0.04, size*0.60)], fill=0, width=s)
    # Legs
    for lx in [size*0.36, size*0.50, size*0.62, size*0.74]:
        draw.line([(lx, size*0.72), (lx, size*0.92)], fill=0, width=s)
    # Ear
    draw.arc([(size*0.06, size*0.20), (size*0.26, size*0.44)], 30, 200, fill=0, width=s)


def _draw_unicorn(draw: ImageDraw.ImageDraw, size: int) -> None:
    """One-horned animal (unicorn seal motif)."""
    _draw_bull(draw, size, humped=False)
    # Single horn upward from head
    hcx = int(size * 0.18)
    draw.line([(hcx, int(size * 0.28)), (hcx - 8, int(size * 0.08))], fill=0, width=STROKE_WIDTH + 1)


def _draw_label(draw: ImageDraw.ImageDraw, sign_id: str, size: int) -> None:
    """Fallback: clean label with sign ID and a border."""
    # Border
    pad = 8
    draw.rectangle([(pad, pad), (size - pad, size - pad)], outline=0, width=2)
    # Sign ID text centered
    try:
        font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()
    num_part = sign_id.replace("M", "M\n")  # "M" + number on two lines if needed
    _, _, tw, th = draw.textbbox((0, 0), sign_id, font=font)
    tx = (size - tw) // 2
    ty = (size - th) // 2
    draw.text((tx, ty), sign_id, fill=0, font=font)


# ── Fallback icon dispatcher ────────────────────────────────────────────────

def _draw_reading_icon(
    draw: ImageDraw.ImageDraw,
    sign_id: str,
    reading: str,
    confidence: str,
    size: int,
) -> None:
    """Draw a labeled fallback icon with reading text and confidence badge."""
    # Border style per confidence tier
    pad = 6
    if confidence == "HIGH":
        # Solid border
        draw.rectangle([(pad, pad), (size - pad, size - pad)], outline=0, width=3)
    elif confidence == "MEDIUM":
        # Dashed border (simulated with segments)
        _draw_dashed_rect(draw, pad, size - pad, pad, size - pad, dash_len=8, gap=4, width=2)
    else:
        # Dotted border
        _draw_dashed_rect(draw, pad, size - pad, pad, size - pad, dash_len=3, gap=4, width=2)

    # Sign ID at top-left
    try:
        small_font = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        small_font = ImageFont.load_default()
    draw.text((pad + 4, pad + 2), sign_id, fill=0, font=small_font)

    # Reading text prominently centered
    try:
        main_font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        main_font = ImageFont.load_default()
    # Truncate long readings
    display_reading = reading if len(reading) <= 12 else reading[:11] + "\u2026"
    _, _, tw, th = draw.textbbox((0, 0), display_reading, font=main_font)
    tx = (size - tw) // 2
    ty = (size - th) // 2
    draw.text((tx, ty), display_reading, fill=0, font=main_font)

    # Confidence badge at bottom-right
    badge = confidence[:3] if confidence else "?"
    try:
        badge_font = ImageFont.truetype("arial.ttf", 10)
    except OSError:
        badge_font = ImageFont.load_default()
    _, _, bw, bh = draw.textbbox((0, 0), badge, font=badge_font)
    bx = size - pad - bw - 4
    by = size - pad - bh - 3
    # Badge background
    draw.rectangle([(bx - 2, by - 1), (bx + bw + 2, by + bh + 1)], fill=0)
    draw.text((bx, by), badge, fill=255, font=badge_font)


def _draw_dashed_rect(
    draw: ImageDraw.ImageDraw,
    x0: int, x1: int, y0: int, y1: int,
    *, dash_len: int = 8, gap: int = 4, width: int = 2,
) -> None:
    """Draw a dashed rectangle."""
    for edge in [
        ((x0, y0), (x1, y0)),  # top
        ((x1, y0), (x1, y1)),  # right
        ((x1, y1), (x0, y1)),  # bottom
        ((x0, y1), (x0, y0)),  # left
    ]:
        (sx, sy), (ex, ey) = edge
        length = max(abs(ex - sx), abs(ey - sy))
        dx = (ex - sx) / max(length, 1)
        dy = (ey - sy) / max(length, 1)
        pos = 0
        while pos < length:
            seg_end = min(pos + dash_len, length)
            draw.line(
                [(sx + dx * pos, sy + dy * pos), (sx + dx * seg_end, sy + dy * seg_end)],
                fill=0, width=width,
            )
            pos = seg_end + gap


def generate_fallback_icon(sign_id: str, iconic: str) -> np.ndarray:
    """Generate a clean black-on-white iconic representation using PIL.

    If the iconic description contains a 'reading:' annotation (from anchor data),
    the icon shows the reading prominently with a confidence badge.
    """
    img = Image.new("L", (SIGN_SIZE, SIGN_SIZE), 255)
    draw = ImageDraw.Draw(img)
    iconic_l = (iconic or "").lower()

    # Check for reading-based icon (from anchor data)
    import re as _re  # noqa: PLC0415
    reading_match = _re.search(r"reading:\s*([^(]+)\s*\(([^)]+)\)", iconic or "")
    # Strip the reading annotation for iconic matching
    iconic_for_match = _re.sub(r"\s*\|?\s*reading:[^)]+\)", "", iconic or "").strip().lower()

    # Stroke / numeral signs
    for n in range(9, 0, -1):
        if f"{n} stroke" in iconic_for_match or f"{n} vertical" in iconic_for_match:
            _draw_strokes(draw, n, SIGN_SIZE)
            _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
            return np.array(img)
    if "stroke" in iconic_for_match or "vertical" in iconic_for_match:
        _draw_strokes(draw, 1, SIGN_SIZE)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Fish family
    if "fish" in iconic_for_match:
        mod = ""
        if "roof" in iconic_for_match:
            mod = "roof"
        elif "trefoil" in iconic_for_match:
            mod = "trefoil"
        elif "fin" in iconic_for_match:
            mod = "fins"
        _draw_fish(draw, SIGN_SIZE, mod)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Unicorn (before bull check)
    if "unicorn" in iconic_for_match or "one-horn" in iconic_for_match:
        _draw_unicorn(draw, SIGN_SIZE)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Bovine family
    if any(k in iconic_for_match for k in ("zebu", "bull", "humped")):
        _draw_bull(draw, SIGN_SIZE, humped="zebu" in iconic_for_match or "humped" in iconic_for_match)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Man / human
    if any(k in iconic_for_match for k in ("man", "human", "person", "figure")):
        _draw_man(draw, SIGN_SIZE)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Elephant
    if "elephant" in iconic_for_match:
        _draw_elephant(draw, SIGN_SIZE)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Gharial / crocodile
    if any(k in iconic_for_match for k in ("gharial", "crocodile", "alligator")):
        _draw_gharial(draw, SIGN_SIZE)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Tiger / feline
    if any(k in iconic_for_match for k in ("tiger", "lion", "feline", "leopard")):
        _draw_animal_generic(draw, SIGN_SIZE)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Jar / vessel
    if any(k in iconic_for_match for k in ("jar", "pot", "vessel", "cup")):
        _draw_jar(draw, SIGN_SIZE)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Cross
    if "cross" in iconic_for_match:
        _draw_cross(draw, SIGN_SIZE)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # Circle / dotted circle
    if "circle" in iconic_for_match or "dotted" in iconic_for_match:
        _draw_circle(draw, SIGN_SIZE, dotted="dotted" in iconic_for_match)
        _add_sign_id_corner(draw, sign_id, SIGN_SIZE)
        return np.array(img)

    # If we have a reading from anchors but no iconic match, show reading icon
    if reading_match:
        reading_text = reading_match.group(1).strip()
        confidence = reading_match.group(2).strip()
        _draw_reading_icon(draw, sign_id, reading_text, confidence, SIGN_SIZE)
        return np.array(img)

    # Default: labeled box with sign ID
    _draw_label(draw, sign_id, SIGN_SIZE)
    return np.array(img)


def _add_sign_id_corner(draw: ImageDraw.ImageDraw, sign_id: str, size: int) -> None:
    """Add sign ID in the bottom-left corner of an iconic fallback."""
    try:
        font = ImageFont.truetype("arial.ttf", 10)
    except OSError:
        font = ImageFont.load_default()
    draw.text((4, size - 14), sign_id, fill=0, font=font)


# ── Image normalization ─────────────────────────────────────────────────────

def normalize_sign_image(img_array: np.ndarray) -> np.ndarray:
    """Normalize any source image to SIGN_SIZE × SIGN_SIZE black-on-white PNG array."""
    # To grayscale
    if img_array.ndim == 3 and img_array.shape[2] == 4:
        # RGBA — composite onto white
        pil = Image.fromarray(img_array, mode="RGBA")
        bg = Image.new("RGBA", pil.size, (255, 255, 255, 255))
        bg.paste(pil, mask=pil.split()[3])
        gray = np.array(bg.convert("L"))
    elif img_array.ndim == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    else:
        gray = img_array.copy()

    # Otsu threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Ensure black-on-white (dark = ink)
    if binary.mean() < 128:
        binary = cv2.bitwise_not(binary)

    # Auto-crop to content bounding box
    rows = np.any(binary < 200, axis=1)
    cols = np.any(binary < 200, axis=0)
    if rows.any() and cols.any():
        r0, r1 = np.where(rows)[0][[0, -1]]
        c0, c1 = np.where(cols)[0][[0, -1]]
        pad = max(6, int(0.12 * max(r1 - r0, c1 - c0, 1)))
        r0 = max(0, r0 - pad)
        r1 = min(binary.shape[0] - 1, r1 + pad)
        c0 = max(0, c0 - pad)
        c1 = min(binary.shape[1] - 1, c1 + pad)
        content = binary[r0 : r1 + 1, c0 : c1 + 1]
    else:
        content = binary

    # Pad to square
    h, w = content.shape
    sz = max(h, w, 1)
    square = np.full((sz, sz), 255, dtype=np.uint8)
    yo = (sz - h) // 2
    xo = (sz - w) // 2
    square[yo : yo + h, xo : xo + w] = content

    # Resize to SIGN_SIZE
    out = cv2.resize(square, (SIGN_SIZE, SIGN_SIZE), interpolation=cv2.INTER_AREA)
    # Final threshold to pure B/W
    _, out = cv2.threshold(out, 127, 255, cv2.THRESH_BINARY)
    return out


# ── Manifest helpers ────────────────────────────────────────────────────────

def load_manifest() -> dict[str, Any]:
    if _MANIFEST_PATH.exists():
        try:
            return json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            _log.warning("Failed to parse manifest.json, starting fresh")
    return {}


def save_manifest(manifest: dict[str, Any]) -> None:
    _MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _save_sign(
    sign_id: str,
    processed: np.ndarray,
    original: np.ndarray | None,
    source: str,
    manifest: dict[str, Any],
) -> None:
    _STATIC_SIGNS.mkdir(parents=True, exist_ok=True)
    _ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)

    proc_path = _STATIC_SIGNS / f"{sign_id}.png"
    Image.fromarray(processed).convert("L").save(str(proc_path), optimize=True)

    orig_path = None
    if original is not None:
        orig_path = _ORIGINALS_DIR / f"{sign_id}.png"
        orig_gray = (original if original.ndim == 2
                     else cv2.cvtColor(original, cv2.COLOR_BGR2GRAY))
        Image.fromarray(orig_gray).convert("L").save(str(orig_path), optimize=True)

    # Validate PNG was actually written and is non-empty
    if not validate_png(proc_path):
        _log.warning("Saved PNG for %s failed validation — marking as suspect", sign_id)

    manifest[sign_id] = {
        "status": "ok",
        "source": source,
        "processed_path": str(proc_path.relative_to(_BACKEND_DIR)),
        "original_path": str(orig_path.relative_to(_BACKEND_DIR)) if orig_path else None,
        "timestamp": _now_iso(),
    }


# ── PNG validation ─────────────────────────────────────────────────────────

def validate_png(path: Path) -> bool:
    """Check that a PNG file exists, is non-empty, and has reasonable ink density."""
    if not path.exists() or path.stat().st_size == 0:
        return False
    try:
        img = np.array(Image.open(path).convert("L"))
        total_px = img.size
        if total_px == 0:
            return False
        black_ratio = float(np.sum(img < 128)) / total_px
        # At least 0.5% black (not blank) and under 40% (not corrupt/filled)
        return 0.005 <= black_ratio <= 0.40
    except Exception:
        return False


# ── Rebuild manifest from disk ─────────────────────────────────────────────

def rebuild_manifest() -> dict[str, Any]:
    """Scan static/signs/ for existing PNGs and reconcile with the manifest.

    Any PNG that exists on disk but is missing or has a non-'ok' status in
    the manifest gets its entry updated.  Returns a summary dict.
    """
    manifest = load_manifest()
    png_files = sorted(_STATIC_SIGNS.glob("*.png"))
    reconciled = 0
    already_ok = 0
    invalid = 0

    for png in png_files:
        sign_id = png.stem
        entry = manifest.get(sign_id, {})

        # Already tracked and ok — skip unless file is missing/corrupt
        if entry.get("status") == "ok" and entry.get("processed_path"):
            already_ok += 1
            continue

        # Validate the PNG content
        if not validate_png(png):
            manifest[sign_id] = {
                "status": "invalid",
                "source": entry.get("source", "unknown"),
                "processed_path": str(png.relative_to(_BACKEND_DIR)),
                "original_path": entry.get("original_path"),
                "timestamp": _now_iso(),
                "validation_error": "failed_pixel_density_check",
            }
            invalid += 1
            continue

        # Determine source — check if an original exists
        orig_path = _ORIGINALS_DIR / f"{sign_id}.png"
        source = entry.get("source", "disk_reconciled")

        manifest[sign_id] = {
            "status": "ok",
            "source": source,
            "processed_path": str(png.relative_to(_BACKEND_DIR)),
            "original_path": (
                str(orig_path.relative_to(_BACKEND_DIR)) if orig_path.exists() else None
            ),
            "timestamp": _now_iso(),
        }
        reconciled += 1

    save_manifest(manifest)
    summary = {
        "total_pngs_on_disk": len(png_files),
        "reconciled": reconciled,
        "already_ok": already_ok,
        "invalid": invalid,
        "manifest_entries": len(manifest),
    }
    _log.info("rebuild_manifest: %s", summary)
    return summary


# ── WikiMedia Commons fetcher ───────────────────────────────────────────────

def _wm_request(url: str, timeout: int = 8) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310
            return r.read()
    except Exception as exc:
        _log.debug("WikiMedia request failed: %s — %s", url, exc)
        return None


def _wm_file_url(filename: str) -> str | None:
    """Look up the direct download URL for a WikiMedia Commons file."""
    api_url = (
        f"{_WIKIMEDIA_API}?action=query&titles=File:{filename}"
        f"&prop=imageinfo&iiprop=url&format=json"
    )
    raw = _wm_request(api_url, timeout=6)
    if not raw:
        return None
    try:
        data = json.loads(raw)
        for page in data.get("query", {}).get("pages", {}).values():
            info = page.get("imageinfo")
            if info:
                return info[0].get("url")
    except Exception:
        pass
    return None


def _load_parpola_map() -> dict[str, int]:
    """Return {mahadevan_sign_id: parpola_number} from the crosswalk.

    Used to look up signs on WikiMedia Commons which indexes by Parpola number.
    Returns empty dict if crosswalk is unavailable.
    """
    if not _CROSSWALK_PATH.exists():
        return {}
    try:
        cw = json.loads(_CROSSWALK_PATH.read_text(encoding="utf-8"))
        result: dict[str, int] = {}
        for sid, info in cw.get("crosswalk", {}).items():
            pid = info.get("parpola_id")
            if pid is not None:
                try:
                    result[sid] = int(str(pid).lstrip("0") or "0")
                except (ValueError, TypeError):
                    pass
        return result
    except Exception:  # noqa: BLE001
        return {}


_parpola_map: dict[str, int] | None = None


def _get_parpola_number(sign_id: str) -> int | None:
    """Return the Parpola sign number for a given sign ID, or None."""
    global _parpola_map  # noqa: PLW0603
    if _parpola_map is None:
        _parpola_map = _load_parpola_map()
    return _parpola_map.get(sign_id)


def _try_fetch_wm_patterns(
    n: int, patterns: list[str], label: str
) -> tuple[np.ndarray, np.ndarray] | None:
    """Try a list of WikiMedia filename patterns for sign number *n*."""
    for pattern in patterns:
        filename = pattern.format(n=n)
        file_url = _wm_file_url(filename)
        if not file_url:
            continue
        raw_bytes = _wm_request(file_url, timeout=12)
        if not raw_bytes:
            continue
        try:
            if filename.endswith(".svg"):
                try:
                    import cairosvg  # type: ignore[import]
                    png_bytes = cairosvg.svg2png(
                        bytestring=raw_bytes, output_width=256, output_height=256
                    )
                    pil_img = Image.open(BytesIO(png_bytes)).convert("RGBA")
                except ImportError:
                    pil_img = Image.open(BytesIO(raw_bytes)).convert("RGBA")
            else:
                pil_img = Image.open(BytesIO(raw_bytes)).convert("RGBA")
            orig_arr = np.array(pil_img)
            processed = normalize_sign_image(orig_arr)
            _log.info("WikiMedia (%s): fetched sign %d from %s", label, n, filename)
            return orig_arr, processed
        except Exception as exc:
            _log.debug("WikiMedia: failed to decode %s: %s", filename, exc)
    return None


def fetch_from_wikimedia(sign_id: str) -> tuple[np.ndarray, np.ndarray] | None:
    """Return (original_array, processed_array) from WikiMedia, or None.

    Tries two numbering systems in order:
    1. Mahadevan (M-prefix) — original patterns
    2. Parpola — confirmed to exist as ``Indus_sign_{n}.png`` on WikiMedia Commons
    """
    # ── Mahadevan number ──────────────────────────────────────────────────────
    raw_num = sign_id.lstrip("M").lstrip("0") or "0"
    if raw_num.isdigit():
        n_m = int(raw_num)
        result = _try_fetch_wm_patterns(n_m, _WM_PATTERNS_MAHADEVAN, "mahadevan")
        if result is not None:
            return result

    # ── Parpola number (better WikiMedia coverage) ────────────────────────────
    p_num = _get_parpola_number(sign_id)
    if p_num is not None:
        result = _try_fetch_wm_patterns(p_num, _WM_PATTERNS_PARPOLA, "parpola")
        if result is not None:
            return result

    return None


# ── Grid extractor ─────────────────────────────────────────────────────────

def extract_from_grid(
    page_path: Path,
    sign_id_order: list[str],
    rows: int,
    cols: int,
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """Segment a sign-table page image and map cells to sign IDs.

    Args:
        page_path:    Path to the source page image (PNG/JPG/etc.)
        sign_id_order: Ordered list of sign IDs corresponding to grid cells
                       (row-major, left→right, top→bottom)
        rows, cols:   Grid dimensions

    Returns:
        dict mapping sign_id → (original_crop_array, processed_array)
    """
    img = cv2.imread(str(page_path))
    if img is None:
        raise ValueError(f"Cannot read page image: {page_path}")

    h, w = img.shape[:2]
    cell_h = h // rows
    cell_w = w // cols

    result: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    for idx, sid in enumerate(sign_id_order):
        if idx >= rows * cols:
            break
        row = idx // cols
        col = idx % cols
        y0 = row * cell_h
        x0 = col * cell_w
        cell = img[y0 : y0 + cell_h, x0 : x0 + cell_w]
        if cell.size == 0:
            continue
        processed = normalize_sign_image(cell)
        result[sid] = (cell, processed)

    return result


# ── Main batch processor ────────────────────────────────────────────────────

def _load_sign_catalog() -> dict[str, str]:
    """Return {sign_id: iconic_description} for all known signs.

    Merges crosswalk (iconic descriptions) with anchors (readings).
    Signs with anchor readings get 'reading: X (CONF)' as iconic if
    they have no better iconic description from the crosswalk.
    """
    catalog: dict[str, str] = {}

    # From crosswalk
    if _CROSSWALK_PATH.exists():
        try:
            cw = json.loads(_CROSSWALK_PATH.read_text(encoding="utf-8"))
            for sid, info in cw.get("crosswalk", {}).items():
                catalog[sid] = info.get("iconic", "")
        except Exception:
            pass

    # From anchors — enrich with reading/confidence for ALL anchor signs
    if _ANCHORS_PATH.exists():
        try:
            data = json.loads(_ANCHORS_PATH.read_text(encoding="utf-8"))
            for sid, anchor in (data.get("anchors") or {}).items():
                reading = anchor.get("reading", "")
                confidence = anchor.get("confidence", "")
                if sid not in catalog or not catalog[sid]:
                    # No crosswalk iconic — use reading as iconic
                    if reading:
                        catalog[sid] = f"reading: {reading} ({confidence})"
                    else:
                        catalog[sid] = ""
                elif reading and "reading:" not in catalog[sid]:
                    # Has crosswalk iconic but append reading info
                    catalog[sid] = f"{catalog[sid]} | reading: {reading} ({confidence})"
        except Exception:
            pass

    return catalog


def _load_anchor_data() -> dict[str, dict[str, str]]:
    """Return {sign_id: {reading, confidence}} from anchors file."""
    if not _ANCHORS_PATH.exists():
        return {}
    try:
        data = json.loads(_ANCHORS_PATH.read_text(encoding="utf-8"))
        result: dict[str, dict[str, str]] = {}
        for sid, anchor in (data.get("anchors") or {}).items():
            result[sid] = {
                "reading": anchor.get("reading", ""),
                "confidence": anchor.get("confidence", ""),
            }
        return result
    except Exception:
        return {}


# Sources that represent real extracted sign images (never overwrite with fallback)
_PROTECTED_SOURCES = frozenset({
    "wikimedia",
    "fuls_page",
})


def _source_is_real(source: str | None) -> bool:
    """Return True when *source* represents a real extracted image (not a fallback)."""
    if not source:
        return False
    if source in _PROTECTED_SOURCES:
        return True
    # mahadevan_table_iii, mahadevan_appendix_i:*, grid:*, etc.
    return (source.startswith("mahadevan_")
            or source.startswith("grid:")
            or source.startswith("fuls"))


def process_single(
    sign_id: str,
    iconic: str = "",
    manifest: dict[str, Any] | None = None,
    *,
    force: bool = False,
    skip_wikimedia: bool = False,
    allow_downgrade: bool = False,
) -> str:
    """Acquire and store image for a single sign. Returns source used.

    ``allow_downgrade=False`` (default) prevents replacing a real extracted
    image (Mahadevan/WikiMedia/Fuls) with a generated fallback icon.  Pass
    ``allow_downgrade=True`` only when explicitly re-extracting everything.
    """
    if manifest is None:
        manifest = load_manifest()

    existing = manifest.get(sign_id, {})
    existing_source = existing.get("source", "")

    # Always skip if already ok and not forcing
    if not force and existing.get("status") == "ok":
        return existing_source

    # With force=True, still protect real images unless caller explicitly allows downgrade.
    # This prevents run_batch(force=True) from nuking Mahadevan-extracted images.
    if force and not allow_downgrade and _source_is_real(existing_source):
        existing_path = _STATIC_SIGNS / f"{sign_id}.png"
        if existing_path.exists() and existing_path.stat().st_size > 0:
            # The real image is still on disk — keep it.
            return existing_source

    # Strategy 1: WikiMedia Commons
    if not skip_wikimedia:
        result = fetch_from_wikimedia(sign_id)
        if result is not None:
            orig, proc = result
            _save_sign(sign_id, proc, orig, "wikimedia", manifest)
            save_manifest(manifest)
            return "wikimedia"

    # Strategy 2: Source pages grid (if any exist)
    if _SOURCE_PAGES.exists():
        for page_file in sorted(_SOURCE_PAGES.glob("*.png")) + sorted(_SOURCE_PAGES.glob("*.jpg")):
            spec_file = page_file.with_suffix(".json")
            if not spec_file.exists():
                continue
            try:
                spec = json.loads(spec_file.read_text(encoding="utf-8"))
                if sign_id in spec.get("sign_order", []):
                    extracted = extract_from_grid(
                        page_file,
                        spec["sign_order"],
                        spec.get("rows", _DEFAULT_GRID["rows"]),
                        spec.get("cols", _DEFAULT_GRID["cols"]),
                    )
                    if sign_id in extracted:
                        orig, proc = extracted[sign_id]
                        _save_sign(sign_id, proc, orig, f"grid:{page_file.name}", manifest)
                        save_manifest(manifest)
                        return f"grid:{page_file.name}"
            except Exception as exc:
                _log.debug("Grid extraction failed for %s on %s: %s", sign_id, page_file, exc)

    # Strategy 3: Local Fuls catalog pages (data/fuls_page_*.png)
    fuls_result = fetch_from_fuls_pages(sign_id)
    if fuls_result is not None:
        orig, proc = fuls_result
        _save_sign(sign_id, proc, orig, "fuls_page", manifest)
        save_manifest(manifest)
        return "fuls_page"

    # Strategy 4: Iconic fallback
    fallback = generate_fallback_icon(sign_id, iconic)
    _save_sign(sign_id, fallback, None, "fallback_icon", manifest)
    save_manifest(manifest)
    return "fallback_icon"


def fetch_from_fuls_pages(sign_id: str) -> tuple[np.ndarray, np.ndarray] | None:
    """Try to extract a sign image from the local Fuls catalog pages.

    The Fuls catalog pages live at data/fuls_page_*.png (13 pages).
    Each page has a ``fuls_page_{N}.json`` spec alongside it that declares
    the sign ordering and grid dimensions.  If no spec exists the page is
    skipped (avoids guessing at layouts).

    The Fuls catalog uses numeric sign IDs (e.g. 159 for plain fish).
    We translate via the crosswalk ``fuls_id`` field.
    """
    # Translate sign_id to Fuls number via crosswalk
    if not _CROSSWALK_PATH.exists():
        return None
    try:
        cw = json.loads(_CROSSWALK_PATH.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    info = cw.get("crosswalk", {}).get(sign_id, {})
    fuls_id = info.get("fuls_id")
    if not fuls_id:
        return None  # no Fuls number for this sign

    fuls_n = str(fuls_id)  # Fuls IDs are numeric strings like "159"

    # Scan data/ for fuls_page_*.png files that have a matching JSON spec
    data_dir = _DATA_DIR
    if not data_dir.exists():
        return None

    for page_file in sorted(data_dir.glob("fuls_page_*.png")):
        spec_file = page_file.with_suffix(".json")
        if not spec_file.exists():
            continue
        try:
            spec = json.loads(spec_file.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        sign_order: list[str] = spec.get("sign_order", [])
        if fuls_n not in sign_order:
            continue
        try:
            extracted = extract_from_grid(
                page_file,
                sign_order,
                spec.get("rows", 6),
                spec.get("cols", 9),
            )
            if fuls_n in extracted:
                orig, proc = extracted[fuls_n]
                _log.info("Fuls page: fetched sign %s (Fuls %s) from %s",
                          sign_id, fuls_n, page_file.name)
                return orig, proc
        except Exception as exc:  # noqa: BLE001
            _log.debug("Fuls page extraction failed for %s: %s", page_file.name, exc)

    return None


def run_batch(
    sign_ids: list[str] | None = None,
    *,
    force: bool = False,
    skip_wikimedia: bool = False,
    delay_secs: float = 0.5,
    allow_downgrade: bool = False,
) -> dict[str, Any]:
    """Process all (or given) signs. Returns summary stats.

    ``allow_downgrade=False`` (default) ensures that signs already backed by a
    real extracted image (Mahadevan, WikiMedia, Fuls) are never replaced by a
    generated fallback icon, even when ``force=True``.
    """
    catalog = _load_sign_catalog()
    if sign_ids is None:
        sign_ids = sorted(catalog.keys())

    manifest = load_manifest()

    stats = {"total": len(sign_ids), "wikimedia": 0, "grid": 0, "fuls_page": 0, "fallback": 0, "skipped": 0}

    for i, sid in enumerate(sign_ids):
        if not force and manifest.get(sid, {}).get("status") == "ok":
            stats["skipped"] += 1
            continue

        iconic = catalog.get(sid, "")
        src = process_single(
            sid, iconic, manifest,
            force=force,
            skip_wikimedia=skip_wikimedia,
            allow_downgrade=allow_downgrade,
        )

        if src == "wikimedia":
            stats["wikimedia"] += 1
        elif src.startswith("grid:"):
            stats["grid"] += 1
        elif src == "fuls_page":
            stats["fuls_page"] += 1
        else:
            stats["fallback"] += 1

        if (i + 1) % 10 == 0:
            _log.info("Progress: %d/%d signs processed", i + 1, len(sign_ids))
            save_manifest(manifest)

        # Be polite to WikiMedia
        if src == "wikimedia" and delay_secs > 0:
            time.sleep(delay_secs)

    save_manifest(manifest)
    _log.info("Batch complete: %s", stats)
    return stats


def get_status() -> dict[str, Any]:
    """Return current status summary."""
    catalog = _load_sign_catalog()
    manifest = load_manifest()

    total = len(catalog)
    with_image = sum(1 for sid in catalog if manifest.get(sid, {}).get("status") == "ok")
    by_source: dict[str, int] = {}
    for sid in catalog:
        src = manifest.get(sid, {}).get("source", "none")
        by_source[src] = by_source.get(src, 0) + 1

    missing = [sid for sid in catalog if manifest.get(sid, {}).get("status") != "ok"]

    return {
        "total_signs": total,
        "with_image": with_image,
        "without_image": total - with_image,
        "coverage_pct": round(with_image / max(total, 1) * 100, 1),
        "by_source": by_source,
        "missing_sample": missing[:20],
    }


# ── Triple-check verification ──────────────────────────────────────────────

def verify_sign_images(
    *,
    sign_ids: list[str] | None = None,
    force: bool = False,
    max_age_days: int = 90,
) -> dict[str, Any]:
    """Run three-level verification on sign images.

    Check 1 (File):       PNG exists at expected path and is non-zero size.
    Check 2 (Content):    Pixel density between 1 % and 40 % black.
    Check 3 (Provenance): Manifest entry has a non-null source and the image
                          was generated within *max_age_days* (unless force).

    Signs failing any check are returned in the *requeued* list.
    """
    catalog = _load_sign_catalog()
    manifest = load_manifest()
    ids = sign_ids or sorted(catalog.keys())

    passed: list[str] = []
    failed: list[dict[str, Any]] = []
    requeued: list[str] = []

    cutoff = datetime.now(tz=timezone.utc).timestamp() - (max_age_days * 86400)

    for sid in ids:
        issues: list[str] = []
        png_path = _STATIC_SIGNS / f"{sid}.png"
        entry = manifest.get(sid, {})

        # Check 1 — file exists and non-zero
        if not png_path.exists() or png_path.stat().st_size == 0:
            issues.append("file_missing_or_empty")
        else:
            # Check 2 — pixel density
            try:
                img = np.array(Image.open(png_path).convert("L"))
                total_px = img.size
                if total_px == 0:
                    issues.append("zero_pixels")
                else:
                    black_ratio = float(np.sum(img < 128)) / total_px
                    if black_ratio < 0.01:
                        issues.append(f"too_sparse({black_ratio:.4f})")
                    elif black_ratio > 0.40:
                        issues.append(f"too_dense({black_ratio:.4f})")
            except Exception as exc:
                issues.append(f"read_error({exc})")

        # Check 3 — provenance
        source = entry.get("source")
        if not source:
            issues.append("no_source")
        if not force:
            ts_str = entry.get("timestamp", "")
            if ts_str:
                try:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00")).timestamp()
                    if ts < cutoff:
                        issues.append("stale")
                except Exception:
                    issues.append("bad_timestamp")
            else:
                issues.append("no_timestamp")

        if issues:
            failed.append({"sign_id": sid, "issues": issues})
            requeued.append(sid)
        else:
            passed.append(sid)

    summary = {
        "total_checked": len(ids),
        "passed": len(passed),
        "failed": len(failed),
        "requeued": len(requeued),
        "failures": failed[:100],  # cap response
    }
    _log.info("verify_sign_images: passed=%d failed=%d", len(passed), len(failed))
    return summary


# ── Wikimedia Commons category miner ───────────────────────────────────────

def _wm_category_members(
    category: str,
    *,
    file_type: str = "File",
    limit: int = 500,
) -> list[dict[str, str]]:
    """Return list of files in a Wikimedia Commons category."""
    results: list[dict[str, str]] = []
    cmcontinue: str | None = ""
    while cmcontinue is not None:
        url = (
            f"{_WIKIMEDIA_API}?action=query&list=categorymembers"
            f"&cmtitle=Category:{category}&cmtype=file&cmlimit={limit}"
            f"&format=json"
        )
        if cmcontinue:
            url += f"&cmcontinue={cmcontinue}"
        raw = _wm_request(url, timeout=10)
        if not raw:
            break
        try:
            data = json.loads(raw)
            for member in data.get("query", {}).get("categorymembers", []):
                title = member.get("title", "")
                if title.startswith("File:"):
                    results.append({"title": title, "pageid": str(member.get("pageid", ""))})
            cmcontinue = data.get("continue", {}).get("cmcontinue")
        except Exception as exc:
            _log.debug("Category query failed for %s: %s", category, exc)
            break
    return results


def find_missing_signs() -> dict[str, list[dict[str, str]]]:
    """Discover candidate sign images from external sources.

    Searches:
      a) Wikimedia Commons categories for Indus script signs
      b) Local data/page_previews/ directory for OCR-extracted images
      c) CDLI API for cross-referenced Indus materials

    Returns ``{sign_id: [candidate_info_dicts]}`` for review.
    """
    candidates: dict[str, list[dict[str, str]]] = {}

    # ── a) Wikimedia Commons categories ──
    wm_categories = [
        "Indus_script",
        "Indus_Valley_Civilisation_signs",
        "Indus_script_signs",
    ]
    for cat in wm_categories:
        try:
            members = _wm_category_members(cat)
            for member in members:
                title = member["title"].replace("File:", "")
                # Try to extract a sign number from the filename
                sign_id = _guess_sign_id_from_filename(title)
                if sign_id:
                    candidates.setdefault(sign_id, []).append({
                        "source": f"wikimedia_category:{cat}",
                        "filename": title,
                        "url": f"https://commons.wikimedia.org/wiki/File:{title}",
                    })
        except Exception as exc:
            _log.warning("Wikimedia category scan failed for %s: %s", cat, exc)

    # ── b) Local page_previews ──
    page_previews_dir = _BACKEND_DIR.parent / "data" / "page_previews"
    if page_previews_dir.exists():
        for f in sorted(page_previews_dir.iterdir()):
            if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
                candidates.setdefault("_local_pages", []).append({
                    "source": "local_page_preview",
                    "filename": f.name,
                    "path": str(f),
                })

    # ── c) CDLI check (best-effort) ──
    try:
        cdli_url = "https://cdli.mpiwg-berlin.mpg.de/search?q=indus+script&format=json"
        raw = _wm_request(cdli_url, timeout=8)
        if raw:
            data = json.loads(raw)
            for item in (data if isinstance(data, list) else data.get("results", []))[:20]:
                item_id = str(item.get("id", item.get("cdli_no", "")))
                if item_id:
                    candidates.setdefault("_cdli", []).append({
                        "source": "cdli",
                        "cdli_id": item_id,
                        "title": str(item.get("title", item.get("designation", ""))),
                    })
    except Exception as exc:
        _log.debug("CDLI query failed: %s", exc)

    _log.info(
        "find_missing_signs: %d sign_ids with candidates, %d total entries",
        len(candidates),
        sum(len(v) for v in candidates.values()),
    )
    return candidates


def _guess_sign_id_from_filename(filename: str) -> str | None:
    """Try to extract a Mahadevan sign ID from a Wikimedia filename."""
    import re  # noqa: PLC0415

    # Patterns like "Indus_script_sign_047.svg" → M047
    m = re.search(r"(?:sign|Sign)[_\s-]?(\d{1,4})", filename)
    if m:
        return f"M{int(m.group(1)):03d}"
    # Just a bare number
    m = re.search(r"(\d{3,4})", filename)
    if m:
        return f"M{int(m.group(1)):03d}"
    return None


# ── Wikimedia-only harvest ───────────────────────────────────────────────────

def harvest_wikimedia_only(
    sign_ids: list[str],
    *,
    delay_secs: float = 0.3,
) -> dict[str, Any]:
    """Try Wikimedia for every sign in *sign_ids*, regardless of manifest status.

    Only updates manifest if Wikimedia succeeds (keeps existing source otherwise).
    Uses a polite delay between requests.
    """
    manifest = load_manifest()
    stats = {"attempted": 0, "fetched": 0, "failed": 0, "errors": []}

    for i, sid in enumerate(sign_ids):
        stats["attempted"] += 1
        try:
            result = fetch_from_wikimedia(sid)
            if result is not None:
                orig, proc = result
                _save_sign(sid, proc, orig, "wikimedia", manifest)
                stats["fetched"] += 1
                _log.info("harvest_wikimedia_only: %s → wikimedia", sid)
            else:
                stats["failed"] += 1
        except Exception as exc:
            stats["failed"] += 1
            stats["errors"].append(f"{sid}: {exc}")
            _log.debug("harvest_wikimedia_only: %s error: %s", sid, exc)

        if (i + 1) % 25 == 0:
            save_manifest(manifest)
            _log.info("harvest_wikimedia_only: %d/%d done (%d fetched)",
                      i + 1, len(sign_ids), stats["fetched"])

        # Polite delay
        if delay_secs > 0:
            time.sleep(delay_secs)

    save_manifest(manifest)
    _log.info("harvest_wikimedia_only complete: %s", stats)
    return stats


def regenerate_all_fallback_icons() -> dict[str, Any]:
    """Regenerate every sign that still has source='fallback_icon'.

    Uses the expanded catalog (with anchor readings) so icons get
    meaningful labels where available.
    """
    catalog = _load_sign_catalog()
    manifest = load_manifest()
    stats = {"regenerated": 0, "skipped": 0}

    for sid, entry in list(manifest.items()):
        if entry.get("source") != "fallback_icon":
            stats["skipped"] += 1
            continue

        iconic = catalog.get(sid, "")
        fallback = generate_fallback_icon(sid, iconic)
        _save_sign(sid, fallback, None, "fallback_icon", manifest)
        stats["regenerated"] += 1

        if stats["regenerated"] % 50 == 0:
            save_manifest(manifest)
            _log.info("regenerate_all_fallback_icons: %d done", stats["regenerated"])

    save_manifest(manifest)
    _log.info("regenerate_all_fallback_icons complete: %s", stats)
    return stats


def run_full_pipeline() -> dict[str, Any]:
    """Run complete reharvest + regenerate + rebuild + verify pipeline."""
    results: dict[str, Any] = {}

    # Step 1: Get all fallback_icon sign IDs
    manifest = load_manifest()
    fallback_ids = sorted(
        sid for sid, entry in manifest.items()
        if entry.get("source") == "fallback_icon"
    )
    _log.info("Pipeline: %d fallback_icon signs to try Wikimedia for", len(fallback_ids))

    # Step 2: Wikimedia harvest for all fallback signs
    results["wikimedia_harvest"] = harvest_wikimedia_only(fallback_ids, delay_secs=0.3)

    # Step 3: Regenerate all remaining fallbacks with improved icons
    results["regeneration"] = regenerate_all_fallback_icons()

    # Step 4: Rebuild manifest
    results["rebuild"] = rebuild_manifest()

    # Step 5: Verify
    results["verification"] = verify_sign_images(force=True)

    # Final stats
    manifest = load_manifest()
    by_source: dict[str, int] = {}
    for entry in manifest.values():
        src = entry.get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1

    results["final_stats"] = {
        "total_signs": len(manifest),
        "by_source": by_source,
        "verification_pass_rate": round(
            results["verification"]["passed"] / max(results["verification"]["total_checked"], 1) * 100, 1
        ),
    }

    _log.info("Full pipeline complete: %s", results["final_stats"])
    return results


# ── CLI entrypoint ──────────────────────────────────────────────────────────

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Indus sign image acquisition tool")
    parser.add_argument("--all", action="store_true", help="Process all signs")
    parser.add_argument("--sign", metavar="ID", help="Process a single sign (e.g. M047)")
    parser.add_argument("--grid", metavar="PAGE_PNG", help="Extract from a sign-table grid image")
    parser.add_argument("--force", action="store_true", help="Re-process even if already done")
    parser.add_argument("--no-web", action="store_true", help="Skip WikiMedia download")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild manifest from existing PNGs")
    parser.add_argument("--verify", action="store_true", help="Run triple-check on all sign images")
    parser.add_argument("--discover", action="store_true", help="Discover missing sign images")
    args = parser.parse_args()

    if args.status:
        st = get_status()
        print(json.dumps(st, indent=2))
        return

    if args.rebuild:
        result = rebuild_manifest()
        print(json.dumps(result, indent=2))
        return

    if args.verify:
        result = verify_sign_images(force=args.force)
        print(json.dumps(result, indent=2))
        return

    if args.discover:
        result = find_missing_signs()
        # Summarize instead of dumping full URLs
        summary = {k: len(v) for k, v in result.items()}
        print(json.dumps({"candidates_by_sign": summary, "total_signs": len(result)}, indent=2))
        return

    if args.sign:
        catalog = _load_sign_catalog()
        src = process_single(
            args.sign,
            catalog.get(args.sign, ""),
            force=args.force,
            skip_wikimedia=args.no_web,
        )
        print(f"{args.sign}: {src}")
        return

    if args.grid:
        print("Grid extraction requires a spec JSON alongside the image (see docs).")
        return

    if args.all:
        stats = run_batch(force=args.force, skip_wikimedia=args.no_web)
        print(json.dumps(stats, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
