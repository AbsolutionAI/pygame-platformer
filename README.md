# Pygame Platformer Template

**A production-ready 2D platformer foundation with player movement, enemies, coins, particle effects, and camera scrolling — built with Pygame.**

## Quick Start

```bash
pip install -r requirements.txt
python src/main.py
```

## Controls

- Arrow keys / WASD — move
- Space / W / Up — jump (double jump enabled)
- Escape — quit

## Features

- **Player** — movement, gravity, double jump, collision
- **Enemies** — patrol AI, stomp to defeat
- **Coins** — collectible with bobbing animation
- **Particles** — on coin pickup and enemy defeat
- **Camera** — smooth scrolling with world bounds
- **Level editor** — tile-based level format (ASCII map)
- **Game states** — menu, playing, game over
- **Score** — 10 per coin, 50 per enemy

## Customization

Edit `src/config.py` to change colors, physics, and window size.
Edit `src/levels.py` to design new levels using the tile character map:
- `1` = ground block
- `P` = player start
- `E` = enemy spawn
- `C` = coin

## License

MIT

## Aspen Grove
Standalone product package (**MIT**). Meta mesh: [aspen-grove](https://github.com/AbsolutionAI/aspen-grove).  
Third-party: `THIRD_PARTY.md`. Run `make smoke`.
