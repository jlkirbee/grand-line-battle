# ⚓ Grand Line Battle

A One Piece × Pokémon Red/Blue-style turn-based battle game. Pick a Straw Hat, face a random crewmate, and duel turn-by-turn — then loop back to character select.

**Play it:** open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8731
# then visit http://localhost:8731/index.html
```

No build step, no dependencies — a single self-contained HTML file.

## Features
- **19 fighters across 3 series** — One Piece (Luffy, Zoro, Nami, Sanji, Usopp, Chopper, Robin, Franky, Brook), Jujutsu Kaisen (Gojo, Yuji, Megumi, Nobara, Sukuna), and Attack on Titan (Eren, Mikasa, Levi, Armin, Titan). Each has unique stats and 4 themed moves. Battles are cross-series — pick anyone, face a random rival.
- **Per-move attack FX** — every move plays its own animated effect (slashes, beams, fireballs, lightning, ODM blade-spins, titan smashes, domain expansions, etc.) and its own synthesized sound, all generated in code.
- **Procedural pixel-art sprites** drawn entirely in code on `<canvas>` — no image assets.
- **Pokémon Gen-1-style battle UI**: typed-out text box, draining HP bars, 2×2 move menu, sprite slide-ins, hit flash + screen shake, critical hits.
- **Simplified damage model** with speed-based turn order; battles resolve in ~5 turns.
- **Tiny WebAudio SFX** (blips/hits/fanfare) — no sound files.

## Game loop
Title → Choose fighter → Random rival appears → Turn-based duel → Win/Lose → back to select.

## Dev / test hooks
Query params for quick inspection:
- `?debug=select` — jump to character select
- `?debug=battle` — jump into a Luffy vs Zoro battle
- `?debug=sim` — run 2000 headless auto-battles and print a pass/fail sanity report

## Notes
Fan project for personal/educational use. One Piece and Pokémon are trademarks of their respective owners — not for commercial use.
