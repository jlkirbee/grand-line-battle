# Grand Line Battle — Art & Style Bible

**Style name:** *16-bit retro console pixel art* (SNES / Sega Genesis ~1990s look),
with chibi fighters in the spirit of GBA/DS anime fighting-game sprites.

This is a fan project. We build **original, similar-style** art — we do **not** copy
specific copyrighted sprites/logos or use any "licensed by" text.

The whole game (every screen, sprite, effect, and sound) should obey this document.

---

## 1. Core principles

1. **Hard pixels, no anti-aliasing.** Canvases render with `imageSmoothingEnabled = false`;
   scaled elements use `image-rendering: pixelated`. Never let sprites blur.
2. **Integer scaling.** Art is authored at a low logical resolution and upscaled by whole
   numbers (×2, ×3, ×4…). Avoid sub-pixel positions and fractional scales where it shows.
3. **Limited palette.** Max **32 colors per sprite**; the whole game draws from the shared
   palette below. No smooth photographic gradients on sprites — use **dithering** instead.
4. **Bold readable shapes.** Chibi proportions (big head, short body), 1px dark outline,
   strong silhouettes that read at small sizes.
5. **CRT feel.** A faint global scanline + vignette overlay sits over everything
   ("faint but visible"), selling the retro-console screen.

---

## 2. Resolution, grid & scaling

| Thing | Spec |
|---|---|
| Tile size | **16×16 px** logical (environment tiles ship as 2×2 = 32×32 blocks) |
| Character sprite | **32×36 px** logical canvas, scaled up; feet on baseline |
| Character scale | **1:1 with the ship** in scene shots (crew ≈ ship deck height) |
| Upscale | integer only; `image-rendering:pixelated`, `ctx.imageSmoothingEnabled=false` |
| Logo | drawn at low res then upscaled ~×3–×4 for chunky pixel letters |

---

## 3. Color palette (limited 16-bit)

Use these; sample new colors from the same families. (Hex.)

**Night sky / space**
- deep `#070b22` · mid `#13306a` · horizon `#2f63aa` · stars `#e6edff`
- moon light `#fdf6e3` · moon shade `#cfd8e6` · crater `#96a2bc`
- cloud band hi `#3a5fa0` · cloud band lo `#2a4a86`

**Sea**
- surface `#1c4f93` · deep `#0c2452` · foam `#bfe4ff` / `#ffffff` · moon-glitter `#fdf6e3`

**Wood / dock**
- plank hi `#7a5230` · plank `#6a4a2a` · plank lo `#5a3a1a` · shadow `#3a2414`
- seam `rgba(0,0,0,.28)` · highlight `rgba(255,235,200,.10)`

**Island / foliage**
- land `#10342a` · dark `#0b261d` · palm leaf `#1f7a34`

**Skin tones**
- `#f1c79e` · `#e8b483` · `#ecc6a0` · `#d99c6a` · `#9c6b3f`

**Hair**
- black-brown `#221a14` · black `#1a1a1a` · green `#5bbf4d` · orange `#f08a2e`
- blonde `#e9c64a` · pink `#f2a0b8` · white `#f2f2f2` · blue `#49c6e8`

**Cloth accents**
- red `#d23a2e` · blue `#2c5fae` · green `#1f7a34` · gold `#ffd23f` · purple `#5e3a86`

**UI**
- paper `#fffdf4` · ink (borders/outline) `#15101c` · accent `#ff5a3c` / `#ffd23f`
- HP green `#4cd07a` · HP yellow `#f4c150` · HP red `#e85c5c`

**Flame / logo**
- `#fff2a0` → `#ffc23a` → `#ff5320`, outline `#2a0f00`

---

## 4. Characters (sprite sheet & animation)

- **Canvas:** 32×36 logical. **Outline:** 1px `#15101c` on the silhouette (goal — current
  procedural sprites are flat; add outlines as we upgrade).
- **Proportions:** chibi — head ≈ 40% of height, stubby limbs, expressive face (2px eyes).
- **Color budget:** ≤32 colors/sprite, dithered shading (no soft gradients).
- **Signature read:** each fighter identifiable by silhouette + one signature feature
  (hat, sword count, antlers, scarf, blindfold, markings…).
- **Frames (target):** `idle` (1–2), `attack` (2–3), `hurt` (1), `faint` (1).
  Today we fake idle/attack with transforms; real frames are the upgrade path.
- **Effects (per move):** one distinct pixel FX + one synthesized SFX (already implemented;
  see `FX` and `SND` in `index.html`).

---

## 5. Environment tiles & items

- **Ocean (2×2 tile):** banded blue with foam-capped wave crests; animate by row offset.
- **Wooden deck (2×2 tile):** plank seams + worn highlights; railing with balusters for docks.
- **Island (1×1 set):** rounded land silhouette + palm trees; sits on the horizon.
- **Sandy shore (1×1):** light beach band where land meets sea.
- **Props:** chest, sword, bottle, jolly-roger flag, map, ship's wheel, skull & bones.
  Author as 16×16 items with the shared palette; provide 2–3 variations each.

---

## 6. Typography

- **Logo / display:** chunky pixel letters (low-res → upscaled) with the **flame gradient**
  (`#fff2a0`→`#ffc23a`→`#ff5320`) and `#2a0f00` outline. See `drawPixelLogo()`.
- **UI / body pixel font:** **Press Start 2P** (`--font-pixel`) as our 8×8 bitmap font for
  menus, labels, HP "Lv", and numbers. Keep lines short; uppercase for headers.
- **Rules:** crisp, no italics on pixel text; letter-spacing ~1px; dark 1px text-shadow for
  contrast on busy backgrounds.

---

## 7. UI components

- **Dialog box:** paper panel `#fffdf4`, **4px ink border** `#15101c`, slight radius, hard
  drop-shadow; pixel font, letter-by-letter typed reveal, blinking ▾ continue arrow.
- **HP plate:** paper panel with NAME + `Lv`, HP bar = dark track + green/yellow/red fill
  that animates as it drains (color tracks the value).
- **Menu:** 2×2 move buttons, ink border + hard bottom shadow, press = translate down.
- **Cursor:** blinking accent ▶ triangle.
- **Buttons:** flat fill + 3–6px ink border + hard offset shadow; no soft glows except FX.

---

## 8. CRT / post-processing

- **Scanlines:** horizontal 1px dark lines every 3px, ~15% black (`#stage::after`).
- **Vignette:** radial corner darken ~38%.
- **Optional (off by default):** subtle RGB fringe / rolling flicker — only if it stays
  "faint but visible" and never hurts readability.

---

## 9. Audio direction (already implemented)

- **4-channel chiptune** (2 pulse + triangle bass + noise drums), all synthesized in code.
- **Distinct themes:** calm **major-key** menu theme vs fast **minor-key** battle theme,
  crossfaded on battle enter/exit.
- **Per-move SFX** (family timbre + per-move pitch), plus battle-start/-end stings and a
  low-HP warning. See `SONG`, `BATTLE_SONG`, `SND`, `sfx` in `index.html`.

---

## 10. Do / Don't

**Do:** integer scale · limited palette · dither for shading · 1px outlines · bold silhouettes
· short pixel-font lines · hard shadows · CRT overlay on.

**Don't:** anti-aliased sprite edges · soft photographic gradients on sprites · sub-pixel
drift · tiny unreadable detail · smooth (bilinear) image scaling · mixing non-pixel fonts
into the game UI.

---

## 11. Where this lives in the code (`index.html`)

| Element | Location |
|---|---|
| Shared palette | inline hex in `DRAW.*` sprite functions + `:root` CSS vars |
| Character sprites | `DRAW` object + `renderChar()` |
| Attack FX | `FX` registry + `animateFx()` |
| Title harbor scene | `drawTitle()`, `drawShip()`, `drawIsland()` |
| Pixel logo | `drawPixelLogo()` |
| Fonts | `--font-display`, `--font-ui`, `--font-pixel` |
| CRT overlay | `#stage::after` |
| Music / SFX | `SONG`, `BATTLE_SONG`, `scheduleSong()`, `SND`, `sfx` |

---

## 12. Adding real PNG art later (highest fidelity path)

The game is currently **100% code-drawn** (no image files). To reach hand-crafted fidelity:

1. Drop pixel-art files into `/assets` (background scenes + character **sprite sheets**).
2. Load with `new Image()`; draw with `ctx.drawImage(...)`, keeping
   `imageSmoothingEnabled=false` and integer scaling.
3. Replace a `DRAW.<id>` function with sheet-frame blitting (idle/attack/hurt frames).
4. Author everything to this palette, 16px grid, and 32×36 sprite size so old and new art
   stay consistent.

This bible is the contract either way — procedural or asset-based, the *look* stays the same.
