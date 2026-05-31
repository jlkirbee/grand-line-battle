# Character Sprite Generation Rule

All new character sheets must start from the same frame contract:

- Output sheet: `768x72` PNG.
- Frames: six frames, each exactly `128x72`.
- Frame order: `idle`, `idle2`, `attack`, `attack2`, `hurt`, `faint`.
- Facing: author the source art facing right; the game flips opponent sprites at runtime.
- Containment: the full pose must fit inside its own 128px-wide frame. This includes weapons,
  extended limbs, slash arcs, fire, hit sparks, hair, hats, feet, and faint/knockdown poses.
- Background for generation: flat chroma key only (`#00ff00` unless the character uses green,
  then `#ff00ff`).
- Validation: run `python3 tools/validate_sprite_sheets.py` before wiring in a character.

Prompt every future image with this exact production constraint:

> every full pose must fit inside a 128px-wide frame after pixel scaling; no body part, weapon,
> or attack effect may touch or cross the frame boundary.
