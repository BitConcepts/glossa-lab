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

# ── Sign number patterns tried on WikiMedia ────────────────────────────────
_WM_PATTERNS = [
    "Indus_script_sign_{n:03d}.svg",
    "Indus_script_sign_{n}.svg",
    "Indus_sign_{n}.svg",
    "Indus_Valley_sign_{n:03d}.svg",
    "Indus_Valley_sign_{n}.svg",
    "Indus_script_sign_{n:03d}.png",
    "Indus_script_sign_{n}.png",
]

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

def generate_fallback_icon(sign_id: str, iconic: str) -> np.ndarray:
    """Generate a clean black-on-white iconic representation using PIL."""
    img = Image.new("L", (SIGN_SIZE, SIGN_SIZE), 255)
    draw = ImageDraw.Draw(img)
    iconic_l = (iconic or "").lower()

    # Stroke / numeral signs
    for n in range(9, 0, -1):
        if f"{n} stroke" in iconic_l or f"{n} vertical" in iconic_l:
            _draw_strokes(draw, n, SIGN_SIZE)
            return np.array(img)
    if "stroke" in iconic_l or "vertical" in iconic_l:
        _draw_strokes(draw, 1, SIGN_SIZE)
        return np.array(img)

    # Fish family
    if "fish" in iconic_l:
        mod = ""
        if "roof" in iconic_l:
            mod = "roof"
        elif "trefoil" in iconic_l:
            mod = "trefoil"
        elif "fin" in iconic_l:
            mod = "fins"
        _draw_fish(draw, SIGN_SIZE, mod)
        return np.array(img)

    # Unicorn (before bull check)
    if "unicorn" in iconic_l or "one-horn" in iconic_l:
        _draw_unicorn(draw, SIGN_SIZE)
        return np.array(img)

    # Bovine family
    if any(k in iconic_l for k in ("zebu", "bull", "humped")):
        _draw_bull(draw, SIGN_SIZE, humped="zebu" in iconic_l or "humped" in iconic_l)
        return np.array(img)

    # Man / human
    if any(k in iconic_l for k in ("man", "human", "person", "figure")):
        _draw_man(draw, SIGN_SIZE)
        return np.array(img)

    # Elephant
    if "elephant" in iconic_l:
        _draw_elephant(draw, SIGN_SIZE)
        return np.array(img)

    # Gharial / crocodile
    if any(k in iconic_l for k in ("gharial", "crocodile", "alligator")):
        _draw_gharial(draw, SIGN_SIZE)
        return np.array(img)

    # Tiger / feline
    if any(k in iconic_l for k in ("tiger", "lion", "feline", "leopard")):
        _draw_animal_generic(draw, SIGN_SIZE)
        return np.array(img)

    # Jar / vessel
    if any(k in iconic_l for k in ("jar", "pot", "vessel", "cup")):
        _draw_jar(draw, SIGN_SIZE)
        return np.array(img)

    # Cross
    if "cross" in iconic_l:
        _draw_cross(draw, SIGN_SIZE)
        return np.array(img)

    # Circle / dotted circle
    if "circle" in iconic_l or "dotted" in iconic_l:
        _draw_circle(draw, SIGN_SIZE, dotted="dotted" in iconic_l)
        return np.array(img)

    # Default: labeled box
    _draw_label(draw, sign_id, SIGN_SIZE)
    return np.array(img)


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
            pass
    return {}


def save_manifest(manifest: dict[str, Any]) -> None:
    _MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


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

    manifest[sign_id] = {
        "status": "ok",
        "source": source,
        "processed_path": str(proc_path.relative_to(_BACKEND_DIR)),
        "original_path": str(orig_path.relative_to(_BACKEND_DIR)) if orig_path else None,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


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


def fetch_from_wikimedia(sign_id: str) -> tuple[np.ndarray, np.ndarray] | None:
    """Return (original_array, processed_array) from WikiMedia, or None."""
    # Extract numeric part — only attempt for M-prefixed (Mahadevan) IDs.
    # P- (Parpola), W- (Wells), F- (Fuls) etc. have no known WikiMedia pattern.
    raw_num = sign_id.lstrip("M").lstrip("0") or "0"
    if not raw_num.isdigit():
        return None  # non-numeric suffix (e.g. P324, W12a) — skip silently
    n = int(raw_num)

    for pattern in _WM_PATTERNS:
        filename = pattern.format(n=n)
        file_url = _wm_file_url(filename)
        if not file_url:
            continue

        raw_bytes = _wm_request(file_url, timeout=12)
        if not raw_bytes:
            continue

        try:
            # Handle SVG → rasterize via PIL (needs cairosvg or pillow-svg)
            if filename.endswith(".svg"):
                # Try cairosvg first, fall back to PIL
                try:
                    import cairosvg  # type: ignore[import]
                    png_bytes = cairosvg.svg2png(bytestring=raw_bytes,
                                                  output_width=256, output_height=256)
                    pil_img = Image.open(BytesIO(png_bytes)).convert("RGBA")
                except ImportError:
                    # Try PIL native SVG (limited support)
                    pil_img = Image.open(BytesIO(raw_bytes)).convert("RGBA")
            else:
                pil_img = Image.open(BytesIO(raw_bytes)).convert("RGBA")

            orig_arr = np.array(pil_img)
            processed = normalize_sign_image(orig_arr)
            _log.info("WikiMedia: fetched %s from %s", sign_id, filename)
            return orig_arr, processed

        except Exception as exc:
            _log.debug("WikiMedia: failed to decode %s: %s", filename, exc)
            continue

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
    """Return {sign_id: iconic_description} for all known signs."""
    catalog: dict[str, str] = {}

    # From crosswalk
    if _CROSSWALK_PATH.exists():
        try:
            cw = json.loads(_CROSSWALK_PATH.read_text(encoding="utf-8"))
            for sid, info in cw.get("crosswalk", {}).items():
                catalog[sid] = info.get("iconic", "")
        except Exception:
            pass

    # From anchors (to pick up IDs not in crosswalk)
    if _ANCHORS_PATH.exists():
        try:
            data = json.loads(_ANCHORS_PATH.read_text(encoding="utf-8"))
            for sid in (data.get("anchors") or {}):
                if sid not in catalog:
                    catalog[sid] = ""
        except Exception:
            pass

    return catalog


def process_single(
    sign_id: str,
    iconic: str = "",
    manifest: dict[str, Any] | None = None,
    *,
    force: bool = False,
    skip_wikimedia: bool = False,
) -> str:
    """Acquire and store image for a single sign. Returns source used."""
    if manifest is None:
        manifest = load_manifest()

    if not force and manifest.get(sign_id, {}).get("status") == "ok":
        return manifest[sign_id]["source"]

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

    # Strategy 3: Iconic fallback
    fallback = generate_fallback_icon(sign_id, iconic)
    _save_sign(sign_id, fallback, None, "fallback_icon", manifest)
    save_manifest(manifest)
    return "fallback_icon"


def run_batch(
    sign_ids: list[str] | None = None,
    *,
    force: bool = False,
    skip_wikimedia: bool = False,
    delay_secs: float = 0.5,
) -> dict[str, Any]:
    """Process all (or given) signs. Returns summary stats."""
    catalog = _load_sign_catalog()
    if sign_ids is None:
        sign_ids = sorted(catalog.keys())

    manifest = load_manifest()

    stats = {"total": len(sign_ids), "wikimedia": 0, "grid": 0, "fallback": 0, "skipped": 0}

    for i, sid in enumerate(sign_ids):
        if not force and manifest.get(sid, {}).get("status") == "ok":
            stats["skipped"] += 1
            continue

        iconic = catalog.get(sid, "")
        src = process_single(sid, iconic, manifest, force=force, skip_wikimedia=skip_wikimedia)

        if src == "wikimedia":
            stats["wikimedia"] += 1
        elif src.startswith("grid:"):
            stats["grid"] += 1
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
    args = parser.parse_args()

    if args.status:
        st = get_status()
        print(json.dumps(st, indent=2))
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
