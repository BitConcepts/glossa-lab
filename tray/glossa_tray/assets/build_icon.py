"""Regenerate the Glossa Lab tray icon assets (PNG + ICO).

The design is the project's own brand tile, as used in the web UI
(frontend/src/App.tsx): a rounded square filled with a 135-degree
blue gradient (#2563eb -> #60a5fa) and a bold white "G". The tray
must not use the BitConcepts company mark or the Syncyard mark;
this is the Glossa Lab application mark.

Run with any Python that has Pillow installed:

    python build_icon.py

Outputs glossa-lab.png (256x256) and glossa-lab.ico (multi-size)
next to this file.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SIZE = 256
START = (0x25, 0x63, 0xEB)  # #2563eb
END = (0x60, 0xA5, 0xFA)  # #60a5fa

_FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "C:\\Windows\\Fonts\\arialbd.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in _FONT_CANDIDATES:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def render(size: int = SIZE) -> Image.Image:
    """Draw the brand tile at ``size`` x ``size`` (supersampled)."""
    scale = 4
    canvas = size * scale
    gradient = Image.new("RGB", (canvas, canvas))
    pixels = gradient.load()
    for y in range(canvas):
        for x in range(canvas):
            t = (x + y) / (2 * (canvas - 1))
            pixels[x, y] = tuple(
                round(START[i] + (END[i] - START[i]) * t) for i in range(3)
            )
    mask = Image.new("L", (canvas, canvas), 0)
    mask_draw = ImageDraw.Draw(mask)
    margin = round(4 * scale * size / SIZE)
    radius = round(58 * scale * size / SIZE)
    mask_draw.rounded_rectangle(
        [margin, margin, canvas - margin, canvas - margin],
        radius=radius,
        fill=255,
    )
    tile = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    tile.paste(gradient, (0, 0), mask)
    draw = ImageDraw.Draw(tile)
    font = _font(round(150 * scale * size / SIZE))
    draw.text(
        (canvas / 2, canvas / 2 + canvas * 0.03),
        "G",
        font=font,
        fill=(255, 255, 255, 255),
        anchor="mm",
    )
    return tile.resize((size, size), Image.LANCZOS)


def main() -> None:
    image = render()
    png_path = HERE / "glossa-lab.png"
    ico_path = HERE / "glossa-lab.ico"
    image.save(png_path, format="PNG")
    image.save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in (16, 20, 24, 32, 48, 64, 128, 256)],
    )
    print(f"wrote {png_path} ({png_path.stat().st_size} bytes)")
    print(f"wrote {ico_path} ({ico_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
