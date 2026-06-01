#!/usr/bin/env python3
"""Validate sprite sheet frame dimensions, transparency, and safe margins."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

EXPECTED_FRAME_WIDTH = 128
DEFAULT_MIN_HORIZONTAL_MARGIN = 12


def validate_sheet(root: Path, char_id: str, spec: dict, min_margin: int, min_horizontal_margin: int) -> list[str]:
    errors: list[str] = []
    path = root / spec["src"]
    if not path.exists():
        return [f"{char_id}: missing {path}"]

    image = Image.open(path).convert("RGBA")
    frame_w = int(spec["frameWidth"])
    frame_h = int(spec["frameHeight"])
    frames = spec["frames"]
    expected_w = frame_w * len(frames)

    if frame_w != EXPECTED_FRAME_WIDTH:
        errors.append(f"{char_id}: frameWidth must be {EXPECTED_FRAME_WIDTH}px, got {frame_w}px")

    if image.size != (expected_w, frame_h):
        errors.append(f"{char_id}: expected {(expected_w, frame_h)}, got {image.size}")

    max_frame = image.width // frame_w
    for state, frame in frames.items():
        if frame < 0 or frame >= max_frame:
            errors.append(f"{char_id}/{state}: frame {frame} is outside sheet")
            continue

        cell = image.crop((frame * frame_w, 0, (frame + 1) * frame_w, frame_h))
        bbox = cell.getchannel("A").getbbox()
        if not bbox:
            errors.append(f"{char_id}/{state}: frame is empty")
            continue

        left, top, right, bottom = bbox
        margins = (left, top, frame_w - right, frame_h - bottom)
        horizontal_margin = min(left, frame_w - right)
        if min(margins) < min_margin:
            errors.append(f"{char_id}/{state}: margin {margins} is below {min_margin}px")
        if horizontal_margin < min_horizontal_margin:
            errors.append(
                f"{char_id}/{state}: horizontal margin {horizontal_margin}px is below {min_horizontal_margin}px"
            )

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("assets/characters/manifest.json"))
    parser.add_argument("--min-margin", type=int, default=6)
    parser.add_argument("--min-horizontal-margin", type=int, default=DEFAULT_MIN_HORIZONTAL_MARGIN)
    args = parser.parse_args()

    root = args.manifest.parent.parent.parent
    manifest = json.loads(args.manifest.read_text())
    errors: list[str] = []
    for char_id, spec in manifest.items():
        errors.extend(validate_sheet(root, char_id, spec, args.min_margin, args.min_horizontal_margin))

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(
        f"Validated {len(manifest)} sprite sheets with >= {args.min_margin}px margins "
        f"and >= {args.min_horizontal_margin}px horizontal margins."
    )


if __name__ == "__main__":
    main()
