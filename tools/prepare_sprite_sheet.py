#!/usr/bin/env python3
"""Normalize generated chroma-key sprite sheets into 128px-frame game sheets."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def is_green_key(r: int, g: int, b: int) -> bool:
    return g > 150 and r < 95 and b < 95 and g - max(r, b) > 80


def is_magenta_key(r: int, g: int, b: int) -> bool:
    return r > 150 and b > 150 and g < 105 and min(r, b) - g > 70


def detect_key(image: Image.Image) -> str:
    rgb = image.convert("RGB")
    w, h = rgb.size
    samples = []
    step = max(1, min(w, h) // 80)
    for x in range(0, w, step):
        samples.append(rgb.getpixel((x, 0)))
        samples.append(rgb.getpixel((x, h - 1)))
    for y in range(0, h, step):
        samples.append(rgb.getpixel((0, y)))
        samples.append(rgb.getpixel((w - 1, y)))

    green = sum(1 for r, g, b in samples if is_green_key(r, g, b))
    magenta = sum(1 for r, g, b in samples if is_magenta_key(r, g, b))
    return "magenta" if magenta > green else "green"


def chroma_to_alpha(image: Image.Image) -> Image.Image:
    src = image.convert("RGBA")
    key = detect_key(src)
    data = []
    pixels = src.get_flattened_data() if hasattr(src, "get_flattened_data") else src.getdata()
    for r, g, b, a in pixels:
        is_key = is_magenta_key(r, g, b) if key == "magenta" else is_green_key(r, g, b)
        data.append((r, g, b, 0) if is_key else (r, g, b, a))
    src.putdata(data)
    return src


def quantize_rgba(image: Image.Image, colors: int = 32) -> Image.Image:
    alpha = image.getchannel("A")
    matte = Image.new("RGBA", image.size, (0, 0, 0, 255))
    matte.alpha_composite(image)
    quantized = matte.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    out = quantized.convert("RGBA")
    out.putalpha(alpha)
    return out


def normalize_sheet(
    source: Path,
    output: Path,
    frame_count: int,
    frame_w: int,
    frame_h: int,
    safe_margin: int,
) -> None:
    src = chroma_to_alpha(Image.open(source))
    cell_w = src.width // frame_count
    out = Image.new("RGBA", (frame_w * frame_count, frame_h), (0, 0, 0, 0))

    for i in range(frame_count):
        cell = src.crop((i * cell_w, 0, (i + 1) * cell_w, src.height))
        bbox = cell.getchannel("A").getbbox()
        if not bbox:
            continue

        pad = max(8, min(cell_w, src.height) // 80)
        left = max(0, bbox[0] - pad)
        top = max(0, bbox[1] - pad)
        right = min(cell.width, bbox[2] + pad)
        bottom = min(cell.height, bbox[3] + pad)
        crop = cell.crop((left, top, right, bottom))

        max_w = frame_w - safe_margin * 2
        max_h = frame_h - safe_margin * 2
        scale = min(max_w / crop.width, max_h / crop.height)
        resized = crop.resize(
            (max(1, round(crop.width * scale)), max(1, round(crop.height * scale))),
            Image.Resampling.NEAREST,
        )

        x = i * frame_w + (frame_w - resized.width) // 2
        y = frame_h - resized.height - safe_margin
        out.alpha_composite(resized, (x, y))

    output.parent.mkdir(parents=True, exist_ok=True)
    quantize_rgba(out).save(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--frames", type=int, default=6)
    parser.add_argument("--frame-width", type=int, default=128)
    parser.add_argument("--frame-height", type=int, default=72)
    parser.add_argument("--safe-margin", type=int, default=6)
    args = parser.parse_args()
    normalize_sheet(args.source, args.output, args.frames, args.frame_width, args.frame_height, args.safe_margin)


if __name__ == "__main__":
    main()
